"""Tests for tools/scoped_content_identity.py (Plan 109; dev-only).

Verifies the v1 Scoped Content Identity algorithm
(docs/plans/96-change-lifecycle-unit-b-increments-1-3.md §13;
docs/CONVENTIONS.md VC-1): deterministic delta scoped identity (sha256 of
"scoped-v1" + path NUL blob NUL pairs, lexicographic scope order, index blob
after ``git add`` or working-tree ``hash-object`` for untracked files) and
state identity (staged tree id via ``git write-tree`` or ``<ref>^{tree}``),
plus fail-closed semantics. Fixtures build real git repositories in tmp_path;
no network and no dependency on the real repository state.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "scoped_content_identity.py"

import scoped_content_identity as sci  # noqa: E402

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None, reason="git CLI not available"
)


_GIT_ENV = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@t",
    "PATH": os.environ.get("PATH", ""),
    "HOME": os.environ.get("HOME", ""),
    "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
}


def git(repo: Path, *args: str) -> str:
    """Run git in ``repo`` and return trimmed stdout; raises on failure."""
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        env=_GIT_ENV,
    )
    return result.stdout.strip()


def init_repo(tmp_path: Path, name: str = "repo") -> Path:
    """Create an isolated git repository with one committed baseline file."""
    repo = tmp_path / name
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    (repo / "baseline.txt").write_text("baseline\n", encoding="utf-8")
    git(repo, "add", "baseline.txt")
    git(repo, "commit", "-q", "-m", "initial")
    return repo


def run_tool(repo: Path, paths: list[str], *extra: str) -> subprocess.CompletedProcess:
    """Run the tool CLI against an isolated repository."""
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(repo), *extra, *paths],
        capture_output=True,
        text=True,
        env={**_GIT_ENV, "PYTHONPATH": str(REPO_ROOT / "tools")},
    )


def report_of(result: subprocess.CompletedProcess) -> dict:
    """Parse the deterministic JSON report of a successful run."""
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def expected_delta(repo: Path, paths: list[str]) -> str:
    """Independently recompute the delta identity from raw git primitives."""
    payload = bytearray(b"scoped-v1")
    for rel in sorted(paths):
        entry = git(repo, "ls-files", "-s", "--", rel)
        blob = entry.split()[1] if entry else git(
            repo, "hash-object", f"--path={rel}", str(repo / rel)
        )
        payload += rel.encode("utf-8") + b"\x00" + blob.encode("ascii") + b"\x00"
    return hashlib.sha256(bytes(payload)).hexdigest()


def test_staged_scope_matches_independent_computation(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    for name in ("a.txt", "b.txt"):
        (repo / name).write_text(f"content of {name}\n", encoding="utf-8")
    git(repo, "add", "a.txt", "b.txt")

    result = run_tool(repo, ["a.txt", "b.txt"])
    report = report_of(result)

    assert report["scope"] == ["a.txt", "b.txt"]
    assert report["delta_scoped_identity"] == expected_delta(
        repo, ["a.txt", "b.txt"]
    )
    assert report["state_identity"] == {
        "source": "staged",
        "ref": None,
        "tree": git(repo, "write-tree"),
    }


def test_deterministic_output(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    (repo / "a.txt").write_text("same\n", encoding="utf-8")
    git(repo, "add", "a.txt")

    first = run_tool(repo, ["a.txt"])
    second = run_tool(repo, ["a.txt"])

    assert first.stdout == second.stdout
    assert report_of(first) == report_of(second)


def test_path_order_is_irrelevant(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    for name in ("a.txt", "b.txt"):
        (repo / name).write_text(f"{name}\n", encoding="utf-8")
    git(repo, "add", "a.txt", "b.txt")

    forward = report_of(run_tool(repo, ["a.txt", "b.txt"]))
    reversed_ = report_of(run_tool(repo, ["b.txt", "a.txt"]))

    assert forward == reversed_
    assert forward["scope"] == ["a.txt", "b.txt"]


def test_content_change_in_scope_changes_delta(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    (repo / "a.txt").write_text("v1\n", encoding="utf-8")
    git(repo, "add", "a.txt")
    before = report_of(run_tool(repo, ["a.txt"]))

    (repo / "a.txt").write_text("v2\n", encoding="utf-8")
    git(repo, "add", "a.txt")
    after = report_of(run_tool(repo, ["a.txt"]))

    assert before["delta_scoped_identity"] != after["delta_scoped_identity"]
    assert before["state_identity"]["tree"] != after["state_identity"]["tree"]


def test_out_of_scope_change_keeps_delta(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    (repo / "a.txt").write_text("scope\n", encoding="utf-8")
    git(repo, "add", "a.txt")
    before = report_of(run_tool(repo, ["a.txt"]))

    (repo / "outside.txt").write_text("outside\n", encoding="utf-8")
    git(repo, "add", "outside.txt")
    after = report_of(run_tool(repo, ["a.txt"]))

    assert before["delta_scoped_identity"] == after["delta_scoped_identity"]
    assert before["state_identity"]["tree"] != after["state_identity"]["tree"]


def test_untracked_file_uses_hash_object(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    (repo / "new.txt").write_text("untracked\n", encoding="utf-8")

    report = report_of(run_tool(repo, ["new.txt"]))

    assert report["scope"] == ["new.txt"]
    assert report["delta_scoped_identity"] == expected_delta(repo, ["new.txt"])


def test_ref_mode_matches_committed_tree(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    (repo / "a.txt").write_text("committed\n", encoding="utf-8")
    git(repo, "add", "a.txt")
    git(repo, "commit", "-q", "-m", "add a.txt")
    head_tree = git(repo, "rev-parse", "HEAD^{tree}")

    ref_report = report_of(run_tool(repo, ["a.txt"], "--ref", "HEAD"))
    staged_report = report_of(run_tool(repo, ["a.txt"]))

    assert ref_report["state_identity"] == {
        "source": "ref",
        "ref": "HEAD",
        "tree": head_tree,
    }
    assert ref_report["delta_scoped_identity"] == staged_report["delta_scoped_identity"]
    assert ref_report["state_identity"]["tree"] == head_tree


def test_missing_path_fail_closed(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)

    result = run_tool(repo, ["missing.txt"])

    assert result.returncode == 1
    assert result.stdout == ""
    assert "path not found" in result.stderr


def test_directory_path_fail_closed(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    (repo / "adir").mkdir()
    (repo / "adir" / "f.txt").write_text("f\n", encoding="utf-8")
    git(repo, "add", "adir/f.txt")

    result = run_tool(repo, ["adir"])

    assert result.returncode == 1
    assert result.stdout == ""
    assert "directory" in result.stderr


def test_not_a_git_repository_fail_closed(tmp_path: Path) -> None:
    plain = tmp_path / "plain"
    plain.mkdir()

    result = run_tool(plain, ["a.txt"])

    assert result.returncode == 1
    assert result.stdout == ""
    assert "not a git repository" in result.stderr


def test_unresolved_ref_fail_closed(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)

    result = run_tool(repo, ["baseline.txt"], "--ref", "no-such-ref")

    assert result.returncode == 1
    assert result.stdout == ""
    assert "unresolved ref" in result.stderr


def test_absolute_path_inside_repo_normalized(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)

    relative = report_of(run_tool(repo, ["baseline.txt"]))
    absolute = report_of(run_tool(repo, [str(repo / "baseline.txt")]))

    assert absolute == relative
    assert absolute["scope"] == ["baseline.txt"]


def test_path_outside_repository_fail_closed(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("out\n", encoding="utf-8")

    result = run_tool(repo, [str(outside)])

    assert result.returncode == 1
    assert result.stdout == ""
    assert "path outside repository" in result.stderr


def test_duplicate_paths_deduplicated(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    (repo / "a.txt").write_text("dedupe\n", encoding="utf-8")
    git(repo, "add", "a.txt")

    single = report_of(run_tool(repo, ["a.txt"]))
    double = report_of(run_tool(repo, ["a.txt", "a.txt"]))

    assert double == single
    assert double["scope"] == ["a.txt"]


def test_library_api_matches_cli(tmp_path: Path) -> None:
    repo = init_repo(tmp_path)
    (repo / "a.txt").write_text("api\n", encoding="utf-8")
    git(repo, "add", "a.txt")

    cli = report_of(run_tool(repo, ["a.txt"]))
    api = sci.compute(repo, ["a.txt"])

    assert api == cli


def make_submodule_layout(tmp_path: Path) -> tuple[Path, Path]:
    """A superproject whose ``.argentos/.agents`` is a git submodule.

    Built with the gitlink primitive (``--cacheinfo 160000``) so it needs no
    network and no ``submodule add`` file-protocol permission; the nested
    working tree is a real repository, exactly like an initialized submodule.
    """
    project = init_repo(tmp_path, "project")
    (project / "src").mkdir()
    (project / "src" / "app.py").write_text("print(1)\n", encoding="utf-8")
    git(project, "add", "src/app.py")
    git(project, "commit", "-q", "-m", "project file")

    payload_source = init_repo(tmp_path, "payload")
    (payload_source / "INDEX.md").write_text("# payload index\n", encoding="utf-8")
    git(payload_source, "add", "INDEX.md")
    git(payload_source, "commit", "-q", "-m", "payload")

    payload_root = project / ".argentos" / ".agents"
    payload_root.parent.mkdir(parents=True)
    shutil.copytree(payload_source, payload_root)
    sha = git(payload_root, "rev-parse", "HEAD")

    (project / ".gitmodules").write_text(
        '[submodule ".argentos/.agents"]\n'
        "\tpath = .argentos/.agents\n"
        "\turl = ../payload\n",
        encoding="utf-8",
    )
    git(project, "add", ".gitmodules")
    git(
        project,
        "update-index",
        "--add",
        "--cacheinfo",
        f"160000,{sha},.argentos/.agents",
    )
    git(project, "commit", "-q", "-m", "register payload submodule")
    return project, payload_root


def test_content_identity_uses_project_root_not_the_payload_submodule(
    tmp_path: Path,
) -> None:
    """Test F — the payload submodule never becomes the project's repo root."""
    project, payload_root = make_submodule_layout(tmp_path)

    # The correct behavior is preserved: with the real project root the scope
    # is identified against PROJECT_ROOT.
    report = sci.compute(
        project,
        [str(project / "src" / "app.py")],
        expected_toplevel=project,
    )
    assert report["scope"] == ["src/app.py"]

    # Rooted at the payload, an expected project root makes the computation
    # fail closed instead of silently identifying the payload's repository.
    for paths in ([str(project / "src" / "app.py")], ["INDEX.md"]):
        with pytest.raises(sci.ToolError):
            sci.compute(payload_root, paths, expected_toplevel=project)


def test_content_identity_cli_expected_root_guard(tmp_path: Path) -> None:
    """Test F (CLI) — ``--expected-root`` guards the declared project root."""
    project, payload_root = make_submodule_layout(tmp_path)

    ok = run_tool(
        project,
        [str(project / "src" / "app.py")],
        "--expected-root",
        str(project),
    )
    assert report_of(ok)["scope"] == ["src/app.py"]

    bad = run_tool(payload_root, ["INDEX.md"], "--expected-root", str(project))
    assert bad.returncode == 1
    assert "repository root mismatch" in bad.stderr
