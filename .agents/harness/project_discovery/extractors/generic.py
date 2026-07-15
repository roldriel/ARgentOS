"""Generic extractors for ecosystem hints."""

from __future__ import annotations

from pathlib import Path

from ..models import DiscoveryResult, Fact
from .base import Extractor


class GenericExtractor(Extractor):
    """Extract high-level facts from README and .gitignore."""

    @property
    def filenames(self) -> set[str]:
        return {"README.md", ".gitignore"}

    def extract(self, path: Path, result: DiscoveryResult) -> None:
        if path.name == "README.md":
            self._extract_readme(path, result)
        elif path.name == ".gitignore":
            self._extract_gitignore(path, result)

    def _extract_readme(self, path: Path, result: DiscoveryResult) -> None:
        text = path.read_text(encoding="utf-8")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        title = ""
        description_lines: list[str] = []

        for line in lines:
            if line.startswith("#") and not title:
                title = line.lstrip("#").strip()
                continue
            if title and not description_lines and not line.startswith("#"):
                description_lines.append(line)
            elif description_lines and not line.startswith("#"):
                description_lines.append(line)
                if len(description_lines) >= 2:
                    break

        if title:
            result.add(
                Fact(
                    category="stack",
                    key="project_title",
                    value=title,
                    source_file=str(path),
                )
            )
        if description_lines:
            result.add(
                Fact(
                    category="stack",
                    key="description",
                    value=" ".join(description_lines),
                    source_file=str(path),
                )
            )

    def _extract_gitignore(self, path: Path, result: DiscoveryResult) -> None:
        text = path.read_text(encoding="utf-8")
        hints: list[str] = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("__pycache__") or stripped.endswith(".pyc"):
                if "Python" not in hints:
                    hints.append("Python")
            elif stripped.startswith("node_modules") or stripped.endswith(
                "package-lock.json"
            ):
                if "Node.js" not in hints:
                    hints.append("Node.js")
            elif stripped.startswith("vendor/") or stripped.endswith("go.sum"):
                if "Go" not in hints:
                    hints.append("Go")
            elif stripped.startswith("target/") or stripped.endswith(".class"):
                if "Java" not in hints:
                    hints.append("Java")

        for hint in hints:
            result.add(
                Fact(
                    category="stack",
                    key="language_hint",
                    value=hint,
                    source_file=str(path),
                )
            )
