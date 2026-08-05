"""Tests for tools/check_plan_citations.py (TDD: written before the module).

Covers acceptance criteria AC-1..AC-8 of the task specification
(.project/d4ab6a93-8e75-4880-baf3-676fce992936/00/04-TASK_SPECIFICATION.md).
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOL = REPO_ROOT / "tools" / "check_plan_citations.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_plan_citations as cpc  # noqa: E402


def make_repo(tmp_path: Path, files: dict[str, str]) -> Path:
    """Create a fake repo with a tools/ copy layout: root/plans/... files."""
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp_path


# --- AC-1: recursive scan of plans/*.md, both citation forms ----------------

def test_extracts_colon_form():
    text = "See `plans/INDEX.md:Convenciones` for details."
    citations = cpc.extract_citations(text)
    assert len(citations) == 1
    assert citations[0].path == "plans/INDEX.md"
    assert citations[0].section == "Convenciones"


def test_extracts_section_sign_form():
    text = "Según `plans/INDEX.md` §Convenciones\ny otra línea."
    citations = cpc.extract_citations(text)
    assert len(citations) == 1
    assert citations[0].path == "plans/INDEX.md"
    assert citations[0].section == "Convenciones"


def test_scan_is_recursive(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md:Sec`\n",
        "plans/rfc/c.md": "`plans/b.md` §Sec\n",
        "plans/INDEX.md": "sin citas\n",
        "other/d.md": "`plans/b.md:Sec`\n",  # outside plans/: must be ignored
    })
    found = cpc.scan_plan_documents(tmp_path)
    sources = {c.source for c in found}
    assert sources == {Path("plans/a.md"), Path("plans/rfc/c.md")}


def test_ignores_non_citation_backticks(tmp_path):
    text = "Run `pytest -v` and see `README` for more."
    assert cpc.extract_citations(text) == []


# --- AC-2: missing file ------------------------------------------------------

def test_missing_file_reported_with_source_and_path(tmp_path):
    make_repo(tmp_path, {"plans/a.md": "`plans/nope.md:Sec`\n"})
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 1
    assert broken[0].reason == "file not found"
    assert broken[0].citation.path == "plans/nope.md"
    assert broken[0].citation.source == Path("plans/a.md")


# --- AC-3: missing section ----------------------------------------------------

def test_missing_section_reported_with_path_and_section(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md:Fantasma`\n",
        "plans/b.md": "# Real\n\ntexto\n",
    })
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 1
    assert broken[0].reason == "section not found"
    assert broken[0].citation.path == "plans/b.md"
    assert broken[0].citation.section == "Fantasma"


# --- AC-4: normalized heading match ------------------------------------------

@pytest.mark.parametrize("cited,heading", [
    ("Convenciones", "## Convenciones"),
    ("convenciones", "## Convenciones"),
    ("Convenciones.", "## Convenciones"),
    ("The marker", "### The marker:"),
    ("  Convenciones  ", "## Convenciones"),
])
def test_normalized_section_match(cited, heading):
    assert cpc.section_exists(cited, heading + "\n\ntexto\n")


def test_section_not_matching_when_different():
    assert not cpc.section_exists("Otra", "## Convenciones\n")


# --- AC-8: numeric-only anchor ------------------------------------------------

@pytest.mark.parametrize("anchor", ["196", "12,39", "6.2"])
def test_numeric_anchor_reported_as_non_heading(tmp_path, anchor):
    make_repo(tmp_path, {
        "plans/a.md": f"`plans/b.md:{anchor}`\n",
        "plans/b.md": "# Real\n",
    })
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 1
    assert broken[0].reason == "non-heading anchor"


# --- AC-5 / AC-6: exit codes and messages -------------------------------------

def run_tool(root: Path, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True, text=True, cwd=str(cwd or root),
    )


def test_clean_repo_exits_0_with_confirmation(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md:Real`\n",
        "plans/b.md": "# Real\n",
    })
    res = run_tool(tmp_path)
    assert res.returncode == 0
    assert "roken" not in res.stdout.splitlines()[0] or "no" in res.stdout.lower()


def test_broken_repo_exits_1_and_lists_citation(tmp_path):
    make_repo(tmp_path, {"plans/a.md": "`plans/nope.md:Sec`\n"})
    res = run_tool(tmp_path)
    assert res.returncode == 1
    assert "plans/nope.md" in res.stdout
    assert "plans/a.md" in res.stdout


def test_runs_from_other_cwd(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md:Real`\n",
        "plans/b.md": "# Real\n",
    })
    other = tmp_path / "elsewhere"
    other.mkdir()
    res = run_tool(tmp_path, cwd=other)
    assert res.returncode == 0


# --- AC-7: stdlib only ----------------------------------------------------------

_STDLIB = set(sys.stdlib_module_names)


def test_tool_uses_only_stdlib():
    tree = ast.parse(TOOL.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    local = {"check_plan_citations"}
    third_party = imported - _STDLIB - local
    assert third_party == set(), f"third-party imports: {third_party}"
