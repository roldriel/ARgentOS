"""Project discovery orchestrator."""

from __future__ import annotations

from pathlib import Path

from .extractors import DEFAULT_EXTRACTORS, Extractor
from .models import DiscoveryResult

# Files and directories we never want to scan.
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    "target",
    "build",
    "dist",
}

# Priority order for config files at the project root.
CONFIG_FILENAMES = {
    "pyproject.toml",
    "requirements.txt",
    "setup.py",
    "setup.cfg",
    "package.json",
    "package-lock.json",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "README.md",
    ".gitignore",
}


def _should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith(".")


def _collect_files(project_root: Path, max_depth: int = 2) -> list[Path]:
    """Collect candidate files up to ``max_depth`` levels."""
    found: list[Path] = []
    found_names: set[str] = set()

    # First, root-level priority files.
    for name in CONFIG_FILENAMES:
        path = project_root / name
        if path.is_file():
            found.append(path)
            found_names.add(name)

    # Then walk subdirectories.
    for depth in range(1, max_depth + 1):
        pattern = "/".join(["*"] * depth) + "/*"
        for path in project_root.glob(pattern):
            if not path.is_file():
                continue
            if path.name in found_names:
                continue
            if path.name not in CONFIG_FILENAMES:
                continue
            if any(
                _should_skip_dir(part)
                for part in path.relative_to(project_root).parts[:-1]
            ):
                continue
            found.append(path)
            found_names.add(path.name)

    return found


def run_discovery(
    project_root: Path,
    extractors: list[type[Extractor]] | None = None,
) -> DiscoveryResult:
    """Run project discovery and return the aggregated result."""
    extractors = extractors or DEFAULT_EXTRACTORS
    instances: list[Extractor] = [cls() for cls in extractors]
    result = DiscoveryResult()

    for path in _collect_files(project_root):
        for extractor in instances:
            if extractor.can_handle(path):
                extractor.extract(path, result)

    return result
