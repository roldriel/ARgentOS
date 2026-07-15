"""Tests for the project discovery module."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_harness_dir = Path(__file__).resolve().parents[1]
if str(_harness_dir) not in sys.path:
    sys.path.insert(0, str(_harness_dir))

from project_discovery.discovery import _collect_files, run_discovery
from project_discovery.extractors import DEFAULT_EXTRACTORS
from project_discovery.models import DiscoveryResult, Fact
from project_discovery.writers import write_kb_entries


@pytest.fixture
def python_project(tmp_path: Path) -> Path:
    root = tmp_path / "python_project"
    root.mkdir()
    (root / "pyproject.toml").write_text(
        """
[project]
name = "example-app"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["fastapi", "pydantic"]

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[tool.pytest.ini_options]
testpaths = ["tests"]
""",
        encoding="utf-8",
    )
    (root / "requirements.txt").write_text(
        "requests>=2.0\nhttpx\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text(
        "# Example App\n\nA sample Python application.\n\nMore details here.\n",
        encoding="utf-8",
    )
    return root


@pytest.fixture
def node_project(tmp_path: Path) -> Path:
    root = tmp_path / "node_project"
    root.mkdir()
    (root / "package.json").write_text(
        """
{
  "name": "example-ui",
  "version": "1.2.3",
  "dependencies": {
    "react": "^18.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "scripts": {
    "build": "vite build",
    "test": "jest"
  },
  "engines": {
    "node": ">=18"
  }
}
""",
        encoding="utf-8",
    )
    return root


@pytest.fixture
def container_project(tmp_path: Path) -> Path:
    root = tmp_path / "container_project"
    root.mkdir()
    (root / "Dockerfile").write_text(
        "FROM python:3.11-slim\nEXPOSE 8000\n",
        encoding="utf-8",
    )
    (root / "docker-compose.yml").write_text(
        """
services:
  web:
    image: example-web
    ports:
      - "8000:8000"
  db:
    image: postgres:15
    ports:
      - "5432:5432"
""",
        encoding="utf-8",
    )
    return root


def test_python_extractor(python_project: Path) -> None:
    result = run_discovery(python_project)
    keys = {f.key for f in result.facts}

    assert any(f.value == "Python" for f in result.facts)
    assert "project_name" in keys
    assert "requires_python" in keys
    assert "fastapi" in [f.value for f in result.facts]
    assert "pytest" in [f.value for f in result.facts]


def test_node_extractor(node_project: Path) -> Path:
    result = run_discovery(node_project)
    values = [f.value for f in result.facts]

    assert "JavaScript/Node.js" in values
    assert "react@^18.0.0" in values
    assert "jest@^29.0.0" in values
    assert any("script:test" == f.key and f.value == "jest" for f in result.facts)


def test_container_extractor(container_project: Path) -> None:
    result = run_discovery(container_project)
    values = [f.value for f in result.facts]

    assert "python:3.11-slim" in values
    assert "8000" in values
    assert "postgres:15" in values
    assert "5432" in values


def test_generic_extractor_reads_readme_and_gitignore(tmp_path: Path) -> None:
    root = tmp_path / "generic_project"
    root.mkdir()
    (root / "README.md").write_text(
        "# Generic Project\n\nThis project does things.\n",
        encoding="utf-8",
    )
    (root / ".gitignore").write_text(
        "__pycache__/\n*.pyc\nnode_modules/\n",
        encoding="utf-8",
    )

    result = run_discovery(root)
    values = [f.value for f in result.facts]

    assert "Generic Project" in values
    assert "This project does things." in values
    assert "Python" in values
    assert "Node.js" in values


def test_collect_files_limits_depth(tmp_path: Path) -> None:
    root = tmp_path / "deep"
    root.mkdir()
    (root / "README.md").write_text("# root", encoding="utf-8")
    nested = root / "a" / "b" / "c"
    nested.mkdir(parents=True)
    (nested / "README.md").write_text("# nested", encoding="utf-8")

    found = _collect_files(root, max_depth=2)
    assert any(p.name == "README.md" and p.parent == root for p in found)
    assert not any("c" in p.parts for p in found)


def test_kb_writer_creates_entries(tmp_path: Path) -> None:
    result = DiscoveryResult()
    result.add(Fact("stack", "language", "Python", "pyproject.toml"))
    result.add(Fact("dependencies", "runtime", "fastapi", "pyproject.toml"))

    output_dir = tmp_path / "discovery"
    written = write_kb_entries(result, output_dir)

    assert len(written) == 10  # one per catalog entry
    assert (output_dir / "stack.md").is_file()
    assert (output_dir / "dependencies.md").is_file()

    stack_text = (output_dir / "stack.md").read_text(encoding="utf-8")
    assert "Python" in stack_text
    assert "+++" in stack_text


def test_kb_writer_creates_project_unknown_when_empty(tmp_path: Path) -> None:
    result = DiscoveryResult()
    output_dir = tmp_path / "discovery"
    written = write_kb_entries(result, output_dir)

    assert (output_dir / "project_unknown.md").is_file()
    text = (output_dir / "project_unknown.md").read_text(encoding="utf-8")
    assert "project type could not be determined" in text
