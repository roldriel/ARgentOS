"""Tests for tools/check_dist_sync.py.

Covers the diff logic (missing / extra / content mismatch) and the CLI
behavior against real git repositories built in tmp_path, including the
line-ending normalization case (CRLF working tree vs LF blobs).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_dist_sync.py"

import check_dist_sync as cds  # noqa: E402
from testsupport import assert_tool_imports_only_stdlib  # noqa: E402

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None, reason="git CLI not available"
)


# --- diff logic -------------------------------------------------------------


def test_diff_clean():
    assert cds.diff({"a.md": b"x"}, {"a.md": b"x"}) == []


def test_diff_missing_extra_and_different():
    issues = cds.diff(
        {"a.md": b"1", "b.md": b"2"},
        {"a.md": b"CHANGED", "c.md": b"3"},
    )
    assert issues == [
        "content differs: a.md",
        "missing in dist: b.md",
        "extra in dist: c.md",
    ]


# --- CLI against real git repos ----------------------------------------------


_GIT_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
    "PATH": os.environ.get("PATH", ""),
    "HOME": os.environ.get("HOME", ""),
    "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
}


def git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True, capture_output=True, env=_GIT_ENV,
    )


def make_repo(tmp_path: Path, dist_files: dict[str, bytes]) -> Path:
    """Repo with protocol/ committed on master and a dist branch."""
    (tmp_path / "protocol" / ".agents").mkdir(parents=True)
    (tmp_path / "protocol" / ".agents" / "INDEX.md").write_bytes(b"# I\n")
    (tmp_path / "protocol" / "_AGENTS.md").write_bytes(b"# Entry\n")
    git(tmp_path, "init", "-q", "-b", "master")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "payload")
    git(tmp_path, "checkout", "-qb", "dist")
    for rel, content in dist_files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
    git(tmp_path, "rm", "-rq", "protocol")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "dist")
    git(tmp_path, "checkout", "-q", "master")
    return tmp_path


def run_tool(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True, text=True,
    )


SYNCED = {".agents/INDEX.md": b"# I\n", "AGENTS.md": b"# Entry\n"}


def test_synced_repo_exits_0(tmp_path):
    make_repo(tmp_path, SYNCED)
    res = run_tool(tmp_path)
    assert res.returncode == 0, res.stdout
    assert "in sync" in res.stdout


def test_drifted_repo_exits_1_and_reports(tmp_path):
    make_repo(tmp_path, {
        ".agents/INDEX.md": b"# CHANGED\n",
        "AGENTS.md": b"# Entry\n",
        "extra.txt": b"x",
    })
    res = run_tool(tmp_path)
    assert res.returncode == 1
    assert "content differs: .agents/INDEX.md" in res.stdout
    assert "extra in dist: extra.txt" in res.stdout


def test_missing_branch_exits_1(tmp_path):
    git(tmp_path, "init", "-q", "-b", "master")
    res = run_tool(tmp_path)
    assert res.returncode == 1
    assert "not found" in res.stdout


def test_crlf_working_tree_does_not_fool_the_check(tmp_path):
    """Committed blobs are compared, so a CRLF checkout stays in sync."""
    make_repo(tmp_path, SYNCED)
    (tmp_path / "protocol" / "_AGENTS.md").write_bytes(b"# Entry\r\n")
    res = run_tool(tmp_path)
    assert res.returncode == 0, res.stdout


# --- stdlib only ---------------------------------------------------------------


def test_tool_uses_only_stdlib():
    assert_tool_imports_only_stdlib(TOOL, {"check_dist_sync"})

