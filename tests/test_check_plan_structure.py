"""Tests for tools/check_plan_structure.py.

Covers the five structural rules enforced on numbered plans/ and
plans/rfc/ documents (plans/INDEX.md §Convenciones, bullet "Plantillas"):
filename, status cycle, template placeholders, RFC Amendment Log and the
plans/INDEX.md mirror.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_plan_structure.py"

sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_plan_structure as cps  # noqa: E402


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


def make_repo(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp_path


def base_repo(tmp_path: Path) -> Path:
    """A minimal conforming repo: one plan, one RFC, INDEX mentioning both."""
    return make_repo(tmp_path, {
        "plans/01-sample-plan.md": PLAN_OK,
        "plans/rfc/01-sample-rfc.md": RFC_OK,
        "plans/INDEX.md": (
            "# INDEX\n\n01-sample-plan.md\n01-sample-rfc.md\n"
        ),
    })


# --- Scope -----------------------------------------------------------------

def test_scan_covers_plans_and_rfc_recursively(tmp_path):
    make_repo(tmp_path, {
        "plans/01-a.md": "",
        "plans/rfc/02-b.md": "",
        "plans/INDEX.md": "",
        "plans/_TEMPLATE.md": "",
        "plans/rfc/_TEMPLATE.md": "",
        "plans/analisis-explicitud.md": "",
        "other/03-c.md": "",
    })
    found = {rel.as_posix() for rel, _ in cps.scan_documents(tmp_path)}
    assert found == {"plans/01-a.md", "plans/rfc/02-b.md"}


def test_annexes_are_excluded(tmp_path):
    make_repo(tmp_path, {
        "plans/18-anexo-a-reporte.md": "",
        "plans/18-plan.md": "",
        "plans/INDEX.md": "18-plan.md\n",
    })
    found = {rel.name for rel, _ in cps.scan_documents(tmp_path)}
    assert found == {"18-plan.md"}


# --- Filename ---------------------------------------------------------------

def test_bad_filename_reported(tmp_path):
    make_repo(tmp_path, {
        "plans/01-Bad_Name.md": PLAN_OK,
        "plans/INDEX.md": "01-Bad_Name.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "filename" for v in violations)


# --- Status cycle -------------------------------------------------------------

def test_missing_status_field_reported(tmp_path):
    make_repo(tmp_path, {
        "plans/01-sample-plan.md": "# Plan 01\n\n## Objetivo\n\nX\n",
        "plans/INDEX.md": "01-sample-plan.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "status" and "missing" in v.detail for v in violations)


def test_unknown_status_reported(tmp_path):
    make_repo(tmp_path, {
        "plans/01-sample-plan.md": PLAN_OK.replace(
            "Aprobado para redacción", "Approved"
        ),
        "plans/INDEX.md": "01-sample-plan.md\n",
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
        "plans/01-sample-plan.md": PLAN_OK.replace(
            "Aprobado para redacción", status
        ),
        "plans/INDEX.md": "01-sample-plan.md\n",
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
        "plans/rfc/01-sample-rfc.md": RFC_OK.replace("Proposal", status),
        "plans/INDEX.md": "01-sample-rfc.md\n",
    })
    assert not [v for v in cps.verify_all(tmp_path) if v.rule == "status"]


def test_rfc_rejects_plan_statuses(tmp_path):
    make_repo(tmp_path, {
        "plans/rfc/01-sample-rfc.md": RFC_OK.replace(
            "Proposal", "Aprobado para redacción"
        ),
        "plans/INDEX.md": "01-sample-rfc.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "status" for v in violations)


# --- Placeholders -------------------------------------------------------------

@pytest.mark.parametrize("placeholder", [
    "Plan NN", "RFC-NN", "NN-slug", "YYYY-MM-DD",
])
def test_leftover_placeholder_reported(tmp_path, placeholder):
    make_repo(tmp_path, {
        "plans/01-sample-plan.md": PLAN_OK + f"\nVer {placeholder}.\n",
        "plans/INDEX.md": "01-sample-plan.md\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(
        v.rule == "placeholder" and placeholder in v.detail
        for v in violations
    )


def test_schema_angle_brackets_are_not_placeholders(tmp_path):
    """Legitimate schema placeholders like <session-uuid> must not flag."""
    make_repo(tmp_path, {
        "plans/01-sample-plan.md": PLAN_OK + "\n`<session-uuid>` y `<order>`.\n",
        "plans/INDEX.md": "01-sample-plan.md\n",
    })
    assert not [v for v in cps.verify_all(tmp_path) if v.rule == "placeholder"]


# --- Amendment Log (RFCs only) --------------------------------------------------

def test_rfc_without_amendment_log_reported(tmp_path):
    make_repo(tmp_path, {
        "plans/rfc/01-sample-rfc.md": RFC_OK.replace("## Amendment Log", "## Otro"),
        "plans/INDEX.md": "01-sample-rfc.md\n",
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
        "plans/02-ghost-plan.md": PLAN_OK,
        "plans/INDEX.md": "# INDEX\n",
    })
    violations = cps.verify_all(tmp_path)
    assert any(v.rule == "index-mirror" for v in violations)


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
        "plans/01-sample-plan.md": PLAN_OK + "\nFecha: YYYY-MM-DD\n",
        "plans/INDEX.md": "# INDEX\n",
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

_STDLIB = set(sys.stdlib_module_names)


def test_tool_uses_only_stdlib():
    tree = ast.parse(TOOL.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    third_party = imported - _STDLIB - {"check_plan_structure"}
    assert third_party == set(), f"third-party imports: {third_party}"
