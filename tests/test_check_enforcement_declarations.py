"""Tests for tools/check_enforcement_declarations.py (G-04, Plan 173).

Covers ENF-001/ENF-002/ENF-003 as declaration-level rules: a mechanically
enforced guarantee needs a runtime/mechanism verifier, a verifiable guarantee
cannot be verified by a human alone, and the document must keep the fail-open
statement without declaring an absolute control. The last test is an anchored
dogfood over the real payload catalog.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_enforcement_declarations.py"
REAL_INDEX = REPO_ROOT / "protocol" / ".agents" / "harness" / "INDEX.md"

import check_enforcement_declarations as ced  # noqa: E402
from testsupport import assert_tool_imports_only_stdlib  # noqa: E402


def catalog(
    rows: list[tuple[str, str, str]],
    *,
    fail_open: bool = True,
    absolute: bool = False,
) -> str:
    body = "\n".join(f"| {g} | {c} | {v} |" for g, c, v in rows)
    tail = (
        "Hooks remain fail-open; this matrix "
        + ("declares them an absolute control" if absolute else "does not declare them an absolute control")
        + " (ENF-003)."
        if fail_open
        else "This matrix declares an absolute control."
    )
    return (
        "# Harness\n\n## Guarantee catalog\n\n"
        "| Guarantee | Class | Verified by |\n|---|---|---|\n"
        f"{body}\n\n"
        "A guarantee labeled \"mechanically enforced\" MUST NOT depend on agent "
        "judgment (ENF-001). In declarative mode every verifiable guarantee is "
        "declared and verified post-hoc or attested (ENF-002). "
        f"{tail}\n"
    )


def write_index(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "protocol" / ".agents" / "harness" / "INDEX.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def run_tool(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True, text=True, cwd=str(root),
    )


GOOD_ROWS = [
    ("Session identity", "Verifiable", "Runtime (dev tool) + agent"),
    ("Gate registration", "Mechanically enforced", "`runner_state` (state) + agent (review)"),
    ("Human approvals", "External-actor-dependent", "human"),
]


def test_valid_catalog_passes(tmp_path):
    path = write_index(tmp_path, catalog(GOOD_ROWS))
    assert ced.verify(path) == []
    assert run_tool(tmp_path).returncode == 0


def test_mechanically_enforced_without_a_mechanism_fails_enf001(tmp_path):
    rows = [("Gate registration", "Mechanically enforced", "agent (review)")]
    failures = ced.verify(write_index(tmp_path, catalog(rows)))
    assert any("ENF-001" in failure for failure in failures)
    assert run_tool(tmp_path).returncode == 1


def test_verifiable_by_a_human_alone_fails_enf002(tmp_path):
    rows = [("Determinable authorization", "Verifiable", "human")]
    failures = ced.verify(write_index(tmp_path, catalog(rows)))
    assert any("ENF-002" in failure for failure in failures)


def test_verifiable_with_a_tool_passes_enf002(tmp_path):
    rows = [("Determinable authorization", "Verifiable", "agent + human (authorization model)")]
    assert ced.verify(write_index(tmp_path, catalog(rows))) == []


def test_missing_fail_open_statement_fails_enf003(tmp_path):
    failures = ced.verify(write_index(tmp_path, catalog(GOOD_ROWS, fail_open=False)))
    assert any("ENF-003" in failure for failure in failures)


def test_absolute_control_claim_fails_enf003(tmp_path):
    failures = ced.verify(
        write_index(tmp_path, catalog(GOOD_ROWS, absolute=True))
    )
    assert any("absolute control" in failure for failure in failures)


def test_class_outside_the_catalog_fails(tmp_path):
    rows = [("Something", "Probably enforced", "runtime")]
    failures = ced.verify(write_index(tmp_path, catalog(rows)))
    assert any("class outside" in failure for failure in failures)


def test_missing_table_is_an_error(tmp_path):
    path = write_index(tmp_path, "# Harness\n\nNo catalog here.\n")
    result = run_tool(tmp_path)
    assert result.returncode == 2
    try:
        ced.verify(path)
    except ced.DeclarationError:
        pass
    else:  # pragma: no cover - the assertion above is the contract
        raise AssertionError("missing catalog must raise DeclarationError")


def test_real_payload_catalog_passes():
    assert ced.verify(REAL_INDEX) == []


def test_tool_uses_only_stdlib():
    assert_tool_imports_only_stdlib(TOOL, {"check_enforcement_declarations"})
