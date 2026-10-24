"""Isolation and epistemic boundaries of Theoretical Execution (plan 175, S6)."""

from __future__ import annotations

import ast
import hashlib
import sys
from pathlib import Path

from test_theoretical_cli import REPO_ROOT, run_cli
from test_theoretical_overlay import build_repo

from runtime.theoretical import (
    build_skeleton,
    load_proposal,
    run_checks,
)
from runtime.theoretical.checks import check_ids


def snapshot(repo: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(repo.rglob("*")):
        if ".git" in path.parts or not path.is_file():
            continue
        files[path.relative_to(repo).as_posix()] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    return files


def test_emit_does_not_write_the_repository() -> None:
    repo = build_repo("isolation")
    before = snapshot(repo)
    proc = run_cli(repo, "--plan", "175", "--emit")
    assert proc.returncode == 0, proc.stderr
    assert snapshot(repo) == before
    assert not (repo / ".project").exists()


def test_orchestrator_does_not_import_theoretical() -> None:
    for path in sorted((REPO_ROOT / "runtime" / "orchestrator").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module == "runtime.theoretical" or module.endswith(".theoretical"):
                    raise AssertionError(f"{path.name} imports {module}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "runtime.theoretical" or alias.name.endswith(
                        ".theoretical"
                    ):
                        raise AssertionError(f"{path.name} imports {alias.name}")


def test_theoretical_package_imports_stdlib_and_runtime_only() -> None:
    from testsupport import assert_tool_imports_only_stdlib

    for path in sorted((REPO_ROOT / "runtime" / "theoretical").glob("*.py")):
        assert_tool_imports_only_stdlib(path, local_modules=("runtime",))


def test_loading_and_building_does_not_instantiate_the_orchestrator_store(
    monkeypatch,
) -> None:
    import runtime.orchestrator.store as store

    def fail(*args, **kwargs):
        raise AssertionError("the orchestrator store was instantiated by TE")

    monkeypatch.setattr(store.OrchestratorStore, "__init__", fail)
    repo = build_repo("no-store")
    proposal = load_proposal(repo, 175, "HEAD")
    checks = run_checks(proposal)
    build_skeleton(proposal, checks)


def test_engine_never_marks_semantic_dimensions_performed() -> None:
    repo = build_repo("semantic-pending")
    proposal = load_proposal(repo, 175, "HEAD")
    skeleton = build_skeleton(proposal, run_checks(proposal))
    dimensions = skeleton["coverage"]["dimensions"]
    for name in ("completeness", "consistency", "adversarial"):
        assert dimensions[name]["executor"] == "producer"
        assert dimensions[name]["status"] == "PENDING"
        assert dimensions[name]["computed"] is False
    assert dimensions["authority"]["computed"] is True
    assert dimensions["verification"]["computed"] is True
    assert set(dimensions["authority"]["evidence_refs"]) == set(check_ids())
