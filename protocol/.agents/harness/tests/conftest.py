"""Shared test configuration for the harness test suite."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

_harness_dir = Path(__file__).resolve().parents[1]
if str(_harness_dir) not in sys.path:
    sys.path.insert(0, str(_harness_dir))


@pytest.fixture
def payload(tmp_path):
    """A minimal but valid payload (contents of ``.agents/``)."""
    root = tmp_path / "payload"
    (root / "standards").mkdir(parents=True)
    (root / "VERSION").write_text("11.7.1\n", encoding="utf-8")
    (root / "INDEX.md").write_text("# payload index\n", encoding="utf-8")
    (root / "standards" / "X.md").write_text("x\n", encoding="utf-8")
    (root / "features.toml").write_text(
        "[features]\nrubrics = true\n", encoding="utf-8"
    )
    return root


@pytest.fixture
def project(tmp_path):
    """An empty adopter project root."""
    root = tmp_path / "project"
    root.mkdir()
    return root


@pytest.fixture
def staging_parent(tmp_path):
    """Host directory for the temporary staging root (isolation control)."""
    return tmp_path / "stage"


@pytest.fixture
def make_engine(payload, staging_parent):
    """Factory building a :class:`lifecycle.LifecycleEngine` for a project."""
    import lifecycle

    def _make(target, **kwargs):
        kwargs.setdefault("payload_dir", payload)
        kwargs.setdefault("staging_parent", staging_parent)
        return lifecycle.LifecycleEngine(target, **kwargs)

    return _make


@pytest.fixture
def make_junction():
    """Create a directory symlink/junction (no admin rights required on NT)."""

    def _make(link: Path, target: Path) -> bool:
        link.parent.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            proc = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(target)],
                capture_output=True,
                text=True,
            )
            return proc.returncode == 0
        try:
            os.symlink(target, link, target_is_directory=True)
        except OSError:
            return False
        return True

    return _make
