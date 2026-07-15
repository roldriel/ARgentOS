"""Extractors for container and orchestration files."""

from __future__ import annotations

import re
from pathlib import Path

from ..models import DiscoveryResult, Fact
from .base import Extractor


class ContainerExtractor(Extractor):
    """Extract facts from Docker and docker-compose files."""

    @property
    def filenames(self) -> set[str]:
        return {"Dockerfile", "docker-compose.yml", "docker-compose.yaml"}

    def extract(self, path: Path, result: DiscoveryResult) -> None:
        result.add(
            Fact(
                category="stack",
                key="containerization",
                value="Docker",
                source_file=str(path),
            )
        )

        if path.name == "Dockerfile":
            self._extract_dockerfile(path, result)
        else:
            self._extract_compose(path, result)

    def _extract_dockerfile(self, path: Path, result: DiscoveryResult) -> None:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.upper().startswith("FROM"):
                parts = stripped.split(None, 1)
                if len(parts) == 2:
                    result.add(
                        Fact(
                            category="containers",
                            key="base_image",
                            value=parts[1],
                            source_file=str(path),
                        )
                    )
            elif stripped.upper().startswith("EXPOSE"):
                ports = re.findall(r"\d+", stripped)
                for port in ports:
                    result.add(
                        Fact(
                            category="containers",
                            key="exposed_port",
                            value=port,
                            source_file=str(path),
                        )
                    )

    def _extract_compose(self, path: Path, result: DiscoveryResult) -> None:
        """Best-effort regex extraction without third-party YAML parser."""
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        # Find the services block.
        in_services = False
        service_indent: int | None = None
        current_service: str | None = None
        current_ports_indent: int | None = None

        for idx, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            indent = len(line) - len(line.lstrip())

            if not in_services:
                if re.match(r"^services:\s*$", stripped):
                    in_services = True
                continue

            # End of services block: a top-level key at the same level as services.
            if indent == 0 and not stripped.startswith("services"):
                break

            # First non-empty indented line after services: defines service indentation level.
            if service_indent is None and indent > 0:
                service_indent = indent

            if service_indent is not None and indent == service_indent:
                service_match = re.match(r"^([a-zA-Z0-9_-]+):\s*$", stripped)
                if service_match:
                    current_service = service_match.group(1)
                    current_ports_indent = None
                    continue

            if (
                current_service
                and service_indent is not None
                and indent > service_indent
            ):
                image_match = re.match(r"^image:\s*(.+)$", stripped)
                if image_match:
                    result.add(
                        Fact(
                            category="containers",
                            key=f"service:{current_service}:image",
                            value=image_match.group(1).strip().strip("\"'"),
                            source_file=str(path),
                        )
                    )
                    current_ports_indent = None
                    continue

                ports_inline = re.match(r"^ports?:\s*(.*)$", stripped)
                if ports_inline:
                    value = ports_inline.group(1).strip()
                    current_ports_indent = indent
                    if value:
                        for port in re.findall(r"\d+", value):
                            result.add(
                                Fact(
                                    category="containers",
                                    key=f"service:{current_service}:port",
                                    value=port,
                                    source_file=str(path),
                                )
                            )
                    continue

                if current_ports_indent is not None and indent > current_ports_indent:
                    for port in re.findall(r"\d+", stripped):
                        result.add(
                            Fact(
                                category="containers",
                                key=f"service:{current_service}:port",
                                value=port,
                                source_file=str(path),
                            )
                        )
                    continue

                # Any other key at the same level as ports ends the ports block.
                if current_ports_indent is not None and indent <= current_ports_indent:
                    current_ports_indent = None
