"""Tests for tools/check_plan_structure.py.

Covers the structural rules enforced on numbered docs/plans/, docs/rfc/ and
docs/adr/ documents (docs/CONVENTIONS.md:Convenciones, bullet "Plantillas"):
filename, status cycle, template placeholders, RFC Amendment Log and the
per-kind governance INDEX mirror.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_plan_structure.py"

import check_plan_structure as cps  # noqa: E402
from testsupport import assert_tool_imports_only_stdlib  # noqa: E402


PLAN_OK = (
    "# Plan 01 — Sample\n\n"
    "**Status:** Aprobado para redacción\n\n"
    "## Objetivo\n\nTexto.\n"
)

RFC_OK = (
    "# RFC-01 — Sample\n\n"
    "**Status:** Proposal\n\n"
    "## Problema\n\nTexto.\n\n"
    "## Amendment Log\n\n- 2026-08-12 — Creación.\n"
)

ADR_OK = (
    "# ADR-01 — Sample\n\n"
    "**Status:** Accepted\n\n"
    "## Contexto\n\nTexto.\n"
)


def make_repo(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp_path


def base_repo(tmp_path: Path) -> Path:
    """A minimal conforming repo: one plan, one RFC, one ADR, per-kind INDEXes."""
    return make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": PLAN_OK,
        "docs/rfc/01-sample-rfc.md": RFC_OK,
        "docs/adr/01-sample-adr.md": ADR_OK,
        "docs/plans/INDEX.md": "# INDEX\n\n01-sample-plan.md\n",
        "docs/rfc/INDEX.md": "# INDEX\n\n01-sample-rfc.md\n",
        "docs/adr/INDEX.md": "# INDEX\n\n01-sample-adr.md\n",
    })


# --- Scope -----------------------------------------------------------------

def test_scan_covers_plans_rfc_and_adr_recursively(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/01-a.md": "",
        "docs/rfc/02-b.md": "",
        "docs/adr/03-c.md": "",
        "docs/plans/INDEX.md": "",
        "docs/adr/INDEX.md": "",
        "docs/plans/_TEMPLATE.md": "",
        "docs/rfc/_TEMPLATE.md": "",
        "docs/adr/_TEMPLATE.md": "",
        "docs/plans/analisis-explicitud.md": "",
        "other/03-c.md": "",
    })
    found = {rel.as_posix() for rel, _ in cps.scan_documents(tmp_path)}
    assert found == {
        "docs/plans/01-a.md", "docs/rfc/02-b.md", "docs/adr/03-c.md",
    }


def test_annexes_are_excluded(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/18-anexo-a-reporte.md": "",
        "docs/plans/18-plan.md": "",
        "docs/plans/INDEX.md": "18-plan.md\n",
    })
    found = {rel.name for rel, _ in cps.scan_documents(tmp_path)}
    assert found == {"18-plan.md"}


# --- Filename ---------------------------------------------------------------

def test_bad_filename_reported(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/01-Bad_Name.md": PLAN_OK,
        "docs/plans/INDEX.md": "01-Bad_Name.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "filename" for v in violations)


# --- Status cycle -------------------------------------------------------------

def test_missing_status_field_reported(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": "# Plan 01\n\n## Objetivo\n\nX\n",
        "docs/plans/INDEX.md": "01-sample-plan.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "status" and "missing" in v.detail for v in violations)


def test_unknown_status_reported(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": PLAN_OK.replace(
            "Aprobado para redacción", "Approved"
        ),
        "docs/plans/INDEX.md": "01-sample-plan.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "status" and "Approved" in v.detail for v in violations)


@pytest.mark.parametrize("status", [
    "Aprobado para redacción",
    "Aprobado para ejecución",
    "Executed",
    "Executed (parcial: falta X)",
    "Executed (2026-08-12). Notas varias.",
    "Executed. Criterio de entrada: plan 01 cerrado.",
    "Superseded",
])
def test_plan_status_cycle_accepted(tmp_path, status):
    make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": PLAN_OK.replace(
            "Aprobado para redacción", status
        ),
        "docs/plans/INDEX.md": "01-sample-plan.md\n",
    })
    assert not [v for v in cps.verify_all(tmp_path) if v.rule == "status"]


@pytest.mark.parametrize("status", [
    "Proposal",
    "Accepted",
    "Accepted (2026-08-12, autorización explícita del usuario).",
    "Superseded",
])
def test_rfc_status_cycle_accepted(tmp_path, status):
    make_repo(tmp_path, {
        "docs/rfc/01-sample-rfc.md": RFC_OK.replace("Proposal", status),
        "docs/rfc/INDEX.md": "01-sample-rfc.md\n",
    })
    assert not [v for v in cps.verify_all(tmp_path) if v.rule == "status"]


@pytest.mark.parametrize("status", [
    "Proposal",
    "Accepted",
    "Accepted (decisión registrada; formalización pendiente).",
    "Superseded",
])
def test_adr_status_cycle_accepted(tmp_path, status):
    make_repo(tmp_path, {
        "docs/adr/01-sample-adr.md": ADR_OK.replace("Accepted", status),
        "docs/adr/INDEX.md": "01-sample-adr.md\n",
    })
    assert not [v for v in cps.verify_all(tmp_path) if v.rule == "status"]


def test_adr_rejects_plan_statuses(tmp_path):
    make_repo(tmp_path, {
        "docs/adr/01-sample-adr.md": ADR_OK.replace(
            "Accepted", "Aprobado para ejecución"
        ),
        "docs/adr/INDEX.md": "01-sample-adr.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "status" for v in violations)


def test_rfc_rejects_plan_statuses(tmp_path):
    make_repo(tmp_path, {
        "docs/rfc/01-sample-rfc.md": RFC_OK.replace(
            "Proposal", "Aprobado para redacción"
        ),
        "docs/rfc/INDEX.md": "01-sample-rfc.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "status" for v in violations)


# --- Placeholders -------------------------------------------------------------

@pytest.mark.parametrize("placeholder", [
    "Plan NN", "RFC-NN", "NN-slug", "YYYY-MM-DD",
])
def test_leftover_placeholder_reported(tmp_path, placeholder):
    make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": PLAN_OK + f"\nVer {placeholder}.\n",
        "docs/plans/INDEX.md": "01-sample-plan.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(
        v.rule == "placeholder" and placeholder in v.detail
        for v in violations
    )


def test_schema_angle_brackets_are_not_placeholders(tmp_path):
    """Legitimate schema placeholders like <session-uuid> must not flag."""
    make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": PLAN_OK + "\n`<session-uuid>` y `<order>`.\n",
        "docs/plans/INDEX.md": "01-sample-plan.md\n",
    })
    assert not [v for v in cps.verify_all(tmp_path) if v.rule == "placeholder"]


# --- Amendment Log (RFCs only) --------------------------------------------------

def test_rfc_without_amendment_log_reported(tmp_path):
    make_repo(tmp_path, {
        "docs/rfc/01-sample-rfc.md": RFC_OK.replace("## Amendment Log", "## Otro"),
        "docs/rfc/INDEX.md": "01-sample-rfc.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "amendment-log" for v in violations)


def test_plan_without_amendment_log_is_fine(tmp_path):
    base_repo(tmp_path)
    assert not [
        v for v in cps.verify_all(tmp_path) if v.rule == "amendment-log"
    ]


# --- INDEX mirror ---------------------------------------------------------------

def test_document_missing_from_index_reported(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/02-ghost-plan.md": PLAN_OK,
        "docs/plans/INDEX.md": "# INDEX\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "index-mirror" for v in violations)


def test_rfc_missing_from_rfc_index_reported(tmp_path):
    make_repo(tmp_path, {
        "docs/rfc/02-ghost-rfc.md": RFC_OK,
        "docs/rfc/INDEX.md": "# INDEX\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "index-mirror" for v in violations)


def test_adr_missing_from_adr_index_reported(tmp_path):
    make_repo(tmp_path, {
        "docs/adr/02-ghost-adr.md": ADR_OK,
        "docs/adr/INDEX.md": "# INDEX\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "index-mirror" for v in violations)


# --- Status / INDEX mirror -------------------------------------------------------

def index_row(basename: str, status: str) -> str:
    return f"| `{basename}` | — | {status} | sample description | active |\n"


def test_status_index_match_is_fine(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": PLAN_OK.replace(
            "Aprobado para redacción", "Executed"
        ),
        "docs/plans/INDEX.md": index_row("01-sample-plan.md", "Executed"),
    })
    assert not [
        v for v in cps.verify_all(tmp_path)
        if v.rule in {"status-index", "status-index-gap"}
    ]
    assert run_tool(tmp_path).returncode == 0


def test_status_index_mismatch_is_a_violation(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": PLAN_OK.replace(
            "Aprobado para redacción", "Executed"
        ),
        "docs/plans/INDEX.md": index_row(
            "01-sample-plan.md", "Aprobado para ejecución"
        ),
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "status-index" for v in violations)
    assert run_tool(tmp_path).returncode == 1


def test_legacy_status_index_is_gap_not_violation(tmp_path):
    """157/158 are historical legacy cases: advisory GAP, exit 0."""
    make_repo(tmp_path, {
        "docs/plans/157-canonical-visual-roadmap.md": PLAN_OK.replace(
            "Aprobado para redacción", "Aprobado para ejecución"
        ),
        "docs/plans/INDEX.md": index_row(
            "157-canonical-visual-roadmap.md", "Executed"
        ),
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "status-index-gap" for v in violations)
    assert not any(v.rule == "status-index" for v in violations)
    res = run_tool(tmp_path)
    assert res.returncode == 0
    assert "GAP:status-index-gap" in res.stdout


# --- CLI ------------------------------------------------------------------------

def run_tool(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True, text=True, cwd=str(root),
    )


def test_clean_repo_exits_0(tmp_path):
    base_repo(tmp_path)
    res = run_tool(tmp_path)
    assert res.returncode == 0
    assert "conform" in res.stdout


def test_dirty_repo_exits_1_and_lists_violation(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/01-sample-plan.md": PLAN_OK + "\nFecha: YYYY-MM-DD\n",
        "docs/plans/INDEX.md": "# INDEX\n",
    })
    res = run_tool(tmp_path)
    assert res.returncode == 1
    assert "01-sample-plan.md" in res.stdout
    assert "placeholder" in res.stdout
    assert "index-mirror" in res.stdout


def test_real_repo_has_no_violations():
    res = run_tool(REPO_ROOT)
    assert res.returncode == 0, res.stdout


# --- stdlib only ------------------------------------------------------------------

def test_tool_uses_only_stdlib():
    assert_tool_imports_only_stdlib(TOOL, {"check_plan_structure"})
