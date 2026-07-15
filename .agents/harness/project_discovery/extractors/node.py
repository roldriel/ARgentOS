"""Extractors for Node.js project files."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import DiscoveryResult, Fact
from .base import Extractor


class NodeExtractor(Extractor):
    """Extract facts from Node.js project files."""

    @property
    def filenames(self) -> set[str]:
        return {"package.json", "package-lock.json"}

    def extract(self, path: Path, result: DiscoveryResult) -> None:
        result.add(
            Fact(
                category="stack",
                key="language",
                value="JavaScript/Node.js",
                source_file=str(path),
            )
        )

        if path.name == "package.json":
            self._extract_package_json(path, result)

    def _extract_package_json(self, path: Path, result: DiscoveryResult) -> None:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return

        if "name" in data:
            result.add(
                Fact(
                    category="stack",
                    key="project_name",
                    value=data["name"],
                    source_file=str(path),
                )
            )
        if "version" in data:
            result.add(
                Fact(
                    category="stack",
                    key="version",
                    value=data["version"],
                    source_file=str(path),
                )
            )

        for key in ("dependencies", "devDependencies", "peerDependencies"):
            for name, version in data.get(key, {}).items():
                result.add(
                    Fact(
                        category="dependencies",
                        key=key,
                        value=f"{name}@{version}",
                        source_file=str(path),
                    )
                )

        for name, command in data.get("scripts", {}).items():
            result.add(
                Fact(
                    category="configuration",
                    key=f"script:{name}",
                    value=command,
                    source_file=str(path),
                )
            )

        if "engines" in data:
            for engine, version in data["engines"].items():
                result.add(
                    Fact(
                        category="stack",
                        key=f"engine:{engine}",
                        value=version,
                        source_file=str(path),
                    )
                )
