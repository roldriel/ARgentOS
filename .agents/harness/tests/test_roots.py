"""Tests for the root resolution contract (GATE 1, Test A).

``roots.py`` is the single implementation of::

    PROJECT_ROOT -> ARGENTOS_ROOT = PROJECT_ROOT/.argentos
                 -> PAYLOAD_ROOT  = ARGENTOS_ROOT/.agents

PROJECT_ROOT is an input; these tests exercise the contract and its declared
path anchors, and prove that the module refuses to invent a root.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import roots


def make_project(tmp_path):
    project = tmp_path / "my-project"
    (project / ".argentos" / ".agents").mkdir(parents=True)
    return project


def test_roots_contract_from_project_root(tmp_path):
    """Test A — the three roots and their fixed relationship."""
    project = make_project(tmp_path)

    resolved = roots.resolve(project)

    assert resolved.project_root == project.resolve()
    assert resolved.argentos_root == (project / ".argentos").resolve()
    assert resolved.payload_root == (project / ".argentos" / ".agents").resolve()
    assert resolved.project_dir == (project / ".argentos" / ".project").resolve()


def test_roots_are_distinct(tmp_path):
    resolved = roots.resolve(make_project(tmp_path))

    assert resolved.project_root != resolved.argentos_root
    assert resolved.argentos_root != resolved.payload_root
    assert resolved.project_root != resolved.payload_root


def test_declared_path_anchors(tmp_path):
    """``.agents``/``.project``/``features.toml`` anchor to ARGENTOS_ROOT."""
    resolved = roots.resolve(make_project(tmp_path))

    assert (
        resolved.resolve_reference(".agents/standards/context/CONTEXT.md")
        == resolved.payload_root / "standards/context/CONTEXT.md"
    )
    assert (
        resolved.resolve_reference(".project/<uuid>/00/ARTIFACT.md")
        == resolved.project_dir / "<uuid>/00/ARTIFACT.md"
    )
    assert (
        resolved.resolve_reference(".argentos/features.toml")
        == resolved.features_file
    )
    assert resolved.resolve_reference("features.toml") == resolved.features_file
    assert (
        resolved.resolve_reference("src/app.py")
        == resolved.project_root / "src/app.py"
    )


def test_resolve_requires_a_project_root():
    """The contract forbids inventing PROJECT_ROOT."""
    for value in (None, "", "   "):
        with pytest.raises(roots.RootResolutionError):
            roots.resolve(value)


def test_env_channel_is_declared(tmp_path):
    resolved = roots.resolve(make_project(tmp_path))

    assert roots.from_env({roots.ENV_PROJECT_ROOT: str(resolved.project_root)}) == resolved
    assert roots.from_env({}) is None


def test_resolve_reference_rejects_traversal(tmp_path):
    """F6 — a declared reference must not escape its anchor with ``..``."""
    resolved = roots.resolve(make_project(tmp_path))

    for ref in (
        ".agents/../escape.md",
        ".agents/../../etc/passwd",
        ".project/../escape.md",
        ".argentos/../escape.md",
        "src/../../escape.md",
        "features.toml/../x",
    ):
        with pytest.raises(roots.RootResolutionError):
            resolved.resolve_reference(ref)


def test_resolve_reference_rejects_drive_relative(tmp_path):
    """F6 — a drive-relative reference (``C:x``) is ambiguous and rejected."""
    resolved = roots.resolve(make_project(tmp_path))

    for ref in ("C:relative.md", "c:relative.md", "Z:file.txt"):
        with pytest.raises(roots.RootResolutionError):
            resolved.resolve_reference(ref)


def test_resolve_reference_keeps_explicit_absolute(tmp_path):
    """F6 — an absolute reference is explicit and returned as given."""
    resolved = roots.resolve(make_project(tmp_path))

    assert resolved.resolve_reference("/abs/path.md") == Path("/abs/path.md")
    assert resolved.resolve_reference("C:/abs/path.md") == Path("C:/abs/path.md")
