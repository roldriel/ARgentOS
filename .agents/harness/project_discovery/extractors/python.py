"""Extractors for Python project files."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from ..models import DiscoveryResult, Fact
from .base import Extractor


class PythonExtractor(Extractor):
    """Extract facts from Python project files."""

    @property
    def filenames(self) -> set[str]:
        return {
            "pyproject.toml",
            "requirements.txt",
            "setup.py",
            "setup.cfg",
        }

    def extract(self, path: Path, result: DiscoveryResult) -> None:
        result.add(
            Fact(
                category="stack",
                key="language",
                value="Python",
                source_file=str(path),
            )
        )

        if path.name == "pyproject.toml":
            self._extract_pyproject(path, result)
        elif path.name == "requirements.txt":
            self._extract_requirements(path, result)
        elif path.name == "setup.py":
            self._extract_setup_py(path, result)
        elif path.name == "setup.cfg":
            self._extract_setup_cfg(path, result)

    def _extract_pyproject(self, path: Path, result: DiscoveryResult) -> None:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError:
            return

        project = data.get("project", {})
        if project:
            if "name" in project:
                result.add(
                    Fact(
                        category="stack",
                        key="project_name",
                        value=project["name"],
                        source_file=str(path),
                    )
                )
            if "version" in project:
                result.add(
                    Fact(
                        category="stack",
                        key="version",
                        value=project["version"],
                        source_file=str(path),
                    )
                )
            if "requires-python" in project:
                result.add(
                    Fact(
                        category="stack",
                        key="requires_python",
                        value=project["requires-python"],
                        source_file=str(path),
                    )
                )
            all_deps = list(project.get("dependencies", []))
            for deps in project.get("optional-dependencies", {}).values():
                all_deps.extend(deps)

            for dep in all_deps:
                result.add(
                    Fact(
                        category="dependencies",
                        key="runtime",
                        value=dep,
                        source_file=str(path),
                    )
                )
                lower = dep.lower()
                for hint, framework in self.FRAMEWORK_HINTS.items():
                    if lower.startswith(hint):
                        result.add(
                            Fact(
                                category="stack",
                                key="framework",
                                value=framework,
                                source_file=str(path),
                            )
                        )

        build_system = data.get("build-system", {})
        if "build-backend" in build_system:
            result.add(
                Fact(
                    category="stack",
                    key="build_backend",
                    value=build_system["build-backend"],
                    source_file=str(path),
                )
            )

        tool = data.get("tool", {})
        if "pytest" in tool:
            result.add(
                Fact(
                    category="configuration",
                    key="test_runner",
                    value="pytest",
                    source_file=str(path),
                )
            )

    FRAMEWORK_HINTS: dict[str, str] = {
        "flask": "Flask",
        "django": "Django",
        "fastapi": "FastAPI",
        "tornado": "Tornado",
        "bottle": "Bottle",
    }

    def _extract_requirements(self, path: Path, result: DiscoveryResult) -> None:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            result.add(
                Fact(
                    category="dependencies",
                    key="runtime",
                    value=stripped,
                    source_file=str(path),
                )
            )
            lower = stripped.lower()
            for hint, framework in self.FRAMEWORK_HINTS.items():
                if lower.startswith(hint):
                    result.add(
                        Fact(
                            category="stack",
                            key="framework",
                            value=framework,
                            source_file=str(path),
                        )
                    )

    def _extract_setup_py(self, path: Path, result: DiscoveryResult) -> None:
        text = path.read_text(encoding="utf-8")
        name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', text)
        if name_match:
            result.add(
                Fact(
                    category="stack",
                    key="project_name",
                    value=name_match.group(1),
                    source_file=str(path),
                )
            )
        version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', text)
        if version_match:
            result.add(
                Fact(
                    category="stack",
                    key="version",
                    value=version_match.group(1),
                    source_file=str(path),
                )
            )

    def _extract_setup_cfg(self, path: Path, result: DiscoveryResult) -> None:
        text = path.read_text(encoding="utf-8")
        name_match = re.search(r"^name\s*=\s*(.+)$", text, re.MULTILINE)
        if name_match:
            result.add(
                Fact(
                    category="stack",
                    key="project_name",
                    value=name_match.group(1).strip(),
                    source_file=str(path),
                )
            )
