"""Tests for tools/check_plan_citations.py.

Covers citation extraction (both forms), broken-file and broken-section
reporting, normalized/prefix heading matching, numeric anchors, CLI exit
codes, legacy payload path mapping and the stdlib-only constraint.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
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
    found = cpc.scan_documents(tmp_path)
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


# --- Prefix heading match -----------------------------------------------------

@pytest.mark.parametrize("cited,heading", [
    ("B", "## B. Actualizar RFC-00XZ"),
    ("B.", "## B. Actualizar RFC-00XZ"),
    ("Stage 10", "# Stage 10 — Prompt Rendering"),
    ("Paso 1", "## Paso 1 — RFC-00YE"),
    ("4.2", "### 4.2 Context Discoverer Invocation"),
    ("D3", "### D3. Dos niveles de ubicación"),
])
def test_prefix_section_match(cited, heading):
    assert cpc.section_exists(cited, heading + "\n\ntexto\n")


@pytest.mark.parametrize("cited,heading", [
    ("5", "### 52 semanas"),          # prefix not followed by allowed char
    ("B", "## Budget overview"),       # next char is a letter
])
def test_prefix_section_rejected_when_not_an_anchor(cited, heading):
    assert not cpc.section_exists(cited, heading + "\n")


# --- Numeric anchors -----------------------------------------------------------

def test_numeric_anchor_valid_when_heading_starts_with_number(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md:5`\n",
        "plans/b.md": "### 5. Worker Delegation\n",
    })
    assert cpc.verify_all(tmp_path) == []


def test_line_range_rejected_even_with_numeric_headings(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md:904-979`\n",
        "plans/b.md": "### 904. Algo\n",
    })
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 1
    assert broken[0].reason == "non-heading anchor"


# --- Greedy § capture trimming --------------------------------------------------

@pytest.mark.parametrize("cited,heading", [
    ("Input from Orchestrator y", "## Input from Orchestrator"),
    ("Skill vs. profile y", "## Skill vs. profile"),
    ("Stage 10 declara que esa etapa", "# Stage 10 — Prompt Rendering"),
    ("Stage 10 o justificar explícitamente las exclusiones",
     "# Stage 10 — Prompt Rendering"),
])
def test_greedy_capture_trimmed_until_heading_match(cited, heading):
    assert cpc.section_exists(cited, heading + "\n")


def test_greedy_capture_trims_to_numeric_anchor(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md` §9 y su plantilla de IDE era específica\n",
        "plans/b.md": "## 9. Example Templates\n",
    })
    assert cpc.verify_all(tmp_path) == []


def test_greedy_capture_still_rejects_unknown_section(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md` §Fantasma total y absoluto\n",
        "plans/b.md": "# Real\n",
    })
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 1
    assert broken[0].reason == "section not found"


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


# --- Legacy payload citations (RFC-55 source containment) --------------------


def test_legacy_agents_path_resolves_to_protocol(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": (
            "`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Project Boundary`\n"
        ),
        "protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md": (
            "# Project Boundary\n"
        ),
    })
    assert cpc.verify_all(tmp_path) == []


def test_legacy_agents_md_resolves_to_payload_entry(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`AGENTS.md:Repository layout`\n",
        "protocol/_AGENTS.md": "# Development Workspace\n\n## Repository layout\n",
    })
    assert cpc.verify_all(tmp_path) == []


def test_legacy_feature_md_resolves_to_vision_doc(tmp_path):
    """feature.md moved to plans/ec-pipeline-vision.md (12 ago 2026)."""
    make_repo(tmp_path, {
        "plans/a.md": "`feature.md:Stage 10`\n",
        "plans/ec-pipeline-vision.md": "# Vision\n\n# Stage 10 — Prompt Rendering\n",
    })
    assert cpc.verify_all(tmp_path) == []


def test_legacy_mapping_does_not_hide_missing_file(tmp_path):
    make_repo(tmp_path, {"plans/a.md": "`.agents/does-not-exist.md:Sec`\n"})
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 1
    assert broken[0].reason == "file not found"


def test_project_session_citations_are_exempt(tmp_path):
    """Citations to ephemeral .project/ artifacts are not verified."""
    make_repo(tmp_path, {
        "plans/a.md": "`.project/d4ab6a93/SESSION_LOG.md:Session Log`\n",
    })
    assert cpc.verify_all(tmp_path) == []


def test_runs_from_other_cwd(tmp_path):
    make_repo(tmp_path, {
        "plans/a.md": "`plans/b.md:Real`\n",
        "plans/b.md": "# Real\n",
    })
    other = tmp_path / "elsewhere"
    other.mkdir()
    res = run_tool(tmp_path, cwd=other)
    assert res.returncode == 0


# --- Root documents as citation sources --------------------------------------


def test_root_docs_are_scanned(tmp_path):
    make_repo(tmp_path, {
        "VERSIONING.md": "Ver `plans/b.md:Real` aquí.\n",
        "plans/b.md": "# Real\n",
    })
    found = cpc.scan_documents(tmp_path)
    assert any(c.source == Path("VERSIONING.md") for c in found)


def test_root_doc_broken_citation_reported(tmp_path):
    make_repo(tmp_path, {"AGENTS.md": "`plans/nope.md:Sec`\n"})
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 1
    assert broken[0].citation.source == Path("AGENTS.md")


def test_scratch_root_docs_are_not_scanned(tmp_path):
    """Working docs (feature.md, audit notes) are not canonical sources."""
    make_repo(tmp_path, {
        "feature.md": "`plans/nope.md:Sec`\n",
        "AUDITORIA_DOCUMENTACION.md": "`plans/nope.md:Sec`\n",
    })
    assert cpc.verify_all(tmp_path) == []


def test_component_docs_are_scanned(tmp_path):
    """runtime/README.md and docs/source-layout.md are canonical sources."""
    make_repo(tmp_path, {
        "runtime/README.md": "`plans/nope.md:Sec`\n",
        "docs/source-layout.md": "`plans/nope.md:Sec`\n",
    })
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 2
    assert {b.citation.source.as_posix() for b in broken} == {
        "runtime/README.md",
        "docs/source-layout.md",
    }


def test_legacy_bare_payload_filename_resolves(tmp_path):
    make_repo(tmp_path, {
        "CHANGELOG.md": "(`ORCHESTRATION_GUIDE.md` §7)\n",
        "protocol/.agents/standards/orchestration/ORCHESTRATION_GUIDE.md": (
            "# Orchestration Guide\n\n## 7. Mapping to workflow phases\n"
        ),
    })
    assert cpc.verify_all(tmp_path) == []


def test_legacy_bare_filename_does_not_hide_missing_file(tmp_path):
    make_repo(tmp_path, {"CHANGELOG.md": "`ORCHESTRATION_GUIDE.md` §7\n"})
    broken = cpc.verify_all(tmp_path)
    assert len(broken) == 1
    assert broken[0].reason == "file not found"


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
