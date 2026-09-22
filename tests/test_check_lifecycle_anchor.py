"""Tests for tools/check_lifecycle_anchor.py (C-1, Plan 98 / Increment 4).

Covers the C-1 rules from
docs/plans/98-change-lifecycle-unit-d-increment-4.md §10/§16.1: population by
structural signals (not by Change Level alone), the v1 Validation Anchor
minimum fields, GAP vs ANOMALY semantics, legacy exclusion, A1/A2 lineage and
deterministic behavior. Tests are self-contained (tmp_path fixtures), stdlib
only, with no network and no dependency on the real origin state.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_lifecycle_anchor.py"

import check_lifecycle_anchor as cla  # noqa: E402
from testsupport import assert_tool_imports_only_stdlib  # noqa: E402


TREE_ID = "a" * 40
DELTA_ID = "b" * 64

ANCHOR_FIELDS = """
- Declared scope: canonical battery of the repo.
- Validation command-set: `python -m pytest tests/`
- Effective inputs (repo content): repo content consumed by the battery.
- Observed dependencies: no instrumentado
- Environmental factors: OS Windows; Python 3.14; sin red.
- Scoped Content Identity:
  - State identity (estado validado): T1 = `{tree}`
  - Delta scoped identity (scope S): `{delta}`
- Validity / stale: `vigente`
""".format(tree=TREE_ID, delta=DELTA_ID)


def plan_doc(status: str, anchor_body: str = "", checkpoint_body: str = "") -> str:
    """A new-regime numbered plan (template container sections present)."""
    return (
        "# Plan 99 — Sample\n\n"
        f"**Status:** {status}\n"
        "**Change Level:** L2\n"
        "**RFC:** RFC-75\n\n"
        "## Objetivo\n\nTexto.\n\n"
        "## Validation anchor\n"
        f"{anchor_body}\n"
        "## Checkpoint / cierre\n"
        f"{checkpoint_body}\n"
    )


def legacy_doc() -> str:
    """A legacy plan without the template container sections."""
    return (
        "# Plan 01 — Legacy\n\n"
        "**Status:** Executed\n\n"
        "## Objetivo\n\nTexto.\n"
    )


def make_repo(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return tmp_path


def run_tool(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True, text=True, cwd=str(root),
    )


# --- Population --------------------------------------------------------------


def test_legacy_artifact_excluded(tmp_path):
    """Legacy plan without container sections is EXCLUDED, never flagged."""
    root = make_repo(tmp_path, {"docs/plans/01-legacy.md": legacy_doc()})
    findings = cla.verify_all(root)
    assert len(findings) == 1
    assert findings[0].classification == "EXCLUDED"


def test_new_regime_artifact_is_included(tmp_path):
    """New-regime member with a recorded validation is a subject, not
    EXCLUDED, and classifies as VALID when its anchor is complete."""
    root = make_repo(tmp_path, {
        "docs/plans/99-sample.md": plan_doc("Executed", ANCHOR_FIELDS),
    })
    findings = cla.verify_all(root)
    assert len(findings) == 1
    assert findings[0].classification == "VALID"


def test_change_level_alone_is_not_membership(tmp_path):
    """Intake signal without container sections is BOUNDARY, not a member."""
    doc = (
        "# Plan 01 — Boundary\n\n"
        "**Status:** Aprobado para ejecución\n"
        "**Change Level:** L2\n\n"
        "## Objetivo\n\nTexto.\n"
    )
    root = make_repo(tmp_path, {"docs/plans/01-boundary.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "BOUNDARY"


def test_annexes_and_templates_are_not_scanned(tmp_path):
    make_repo(tmp_path, {
        "docs/plans/99-sample.md": plan_doc("Executed", ANCHOR_FIELDS),
        "docs/plans/99-anexo-a-reporte.md": legacy_doc(),
        "docs/plans/_TEMPLATE.md": "## Validation anchor\n## Checkpoint / cierre\n",
        "docs/plans/INDEX.md": "99-sample.md\n",
        "docs/rfc/75-sample.md": "## Validation anchor\n",
    })
    rels = [f.rel.as_posix() for f in cla.verify_all(tmp_path)]
    assert rels == ["docs/plans/99-sample.md"]


# --- Anchor validity -----------------------------------------------------------


def test_valid_anchor_a1_is_valid(tmp_path):
    root = make_repo(tmp_path, {
        "docs/plans/99-sample.md": plan_doc("Executed", ANCHOR_FIELDS),
    })
    findings = cla.verify_all(root)
    assert findings[0].classification == "VALID"
    res = run_tool(root)
    assert res.returncode == 0
    assert "99-sample.md: VALID" in res.stdout


def test_declared_validation_with_empty_anchor_is_gap(tmp_path):
    """Executed plan with an empty (comment-only) anchor section -> GAP."""
    doc = plan_doc(
        "Executed",
        "<!-- Se completa al validar (sin contenido en esta iteración). -->",
    )
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "GAP"
    assert "section empty" in findings[0].reasons[0]


def test_missing_required_field_is_gap(tmp_path):
    """Anchor missing one v1 field -> GAP (advisory, exit 0)."""
    incomplete = ANCHOR_FIELDS.replace("- Environmental factors:", "- Entorno:")
    doc = plan_doc("Executed", incomplete)
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "GAP"
    assert "Environmental factors" in findings[0].reasons[0]
    assert run_tool(root).returncode == 0


def test_missing_sci_subfield_is_gap(tmp_path):
    body = ANCHOR_FIELDS.replace(
        "  - Delta scoped identity (scope S): `%s`" % DELTA_ID, ""
    )
    doc = plan_doc("Executed", body)
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "GAP"
    assert "Delta scoped identity" in findings[0].reasons[0]


def test_gap_never_turns_exit_code_nonzero(tmp_path):
    """Absence of evidence is advisory: GAP alone exits 0 (R-C1-3)."""
    doc = plan_doc("Executed", "<!-- vacío -->")
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    assert run_tool(root).returncode == 0


# --- Anomalies ----------------------------------------------------------------


def test_duplicated_conflicting_field_is_anomaly(tmp_path):
    body = ANCHOR_FIELDS + "\n- Validity / stale: `stale (cambio posterior)`"
    doc = plan_doc("Executed", body)
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "ANOMALY"
    assert "duplicated field" in findings[0].reasons[0]
    assert run_tool(root).returncode == 1


def test_contradictory_validity_values_is_anomaly(tmp_path):
    body = ANCHOR_FIELDS.replace("`vigente`", "`vigente` y `stale`")
    doc = plan_doc("Executed", body)
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "ANOMALY"
    assert "contradictory Validity" in findings[0].reasons[0]


def test_invalid_identity_format_is_anomaly(tmp_path):
    body = ANCHOR_FIELDS.replace(f"`{TREE_ID}`", "`not-a-tree-id`")
    doc = plan_doc("Executed", body)
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "ANOMALY"
    assert "invalid State identity format" in findings[0].reasons[0]


# --- Deferred identity literals (plan 147, F1) -----------------------------------
#
# The corpus anti-self-reference convention (plan 96 §13; plans 114/116/134/
# 140-146) lets the Validation anchor declare its identity resolved outside
# itself and transcribe the literals in the closing commit. The released
# `master` tree of plan 146 carries exactly that revision, and C-1 used to
# reject it as an ANOMALY (invalid format) even though no value was presented.

DEFERRED_ANCHOR_FIELDS = """
- Declared scope: release change of the repository.
- Validation command-set: `python -m pytest tests/`
- Effective inputs (repo content): repo content consumed by the battery.
- Observed dependencies: no instrumentado
- Environmental factors: OS Linux; Python 3.12; sin red.
- Scoped Content Identity:
  - State identity (estado validado): resuelta sobre el árbol del commit de
    este Change — ver `## Checkpoint / cierre`.
  - Delta scoped identity (scope S): resuelta por
    `tools/scoped_content_identity.py` sobre el estado del Change — ver
    `## Checkpoint / cierre`.
  - Límite declarado: las literales de identidad se transcriben en el commit de
    cierre (convención anti-auto-referencia).
- Validity / stale: vigente
"""


def test_deferred_identity_literals_are_gap_not_anomaly(tmp_path):
    """A declared absence of the literal is missing evidence, not a contradiction."""
    root = make_repo(tmp_path, {
        "docs/plans/99-sample.md": plan_doc("Executed", DEFERRED_ANCHOR_FIELDS),
    })
    findings = cla.verify_all(root)
    assert findings[0].classification == "GAP"
    assert any(
        "declares it resolved outside itself" in reason
        for reason in findings[0].reasons
    )
    assert run_tool(root).returncode == 0


def test_deferral_falsification_malformed_literal_is_still_anomaly(tmp_path):
    """The deferral rule must not become a way to smuggle an invalid value.

    A malformed literal carries no hex token, exactly like a deferral, so the
    rule must not treat "no hex" as sufficient. Here the subfield declares
    ``T1 = `not-a-tree-id` `` *and* the anchor also points at the checkpoint
    section: the declared value decides, and it is still an ANOMALY.
    """
    body = ANCHOR_FIELDS.replace(
        f"`{TREE_ID}`", "`not-a-tree-id`"
    ).replace(
        "- Validity / stale: `vigente`",
        "- Validity / stale: `vigente` (identidad resuelta fuera; "
        "ver `## Checkpoint / cierre`)",
    )
    assert "not-a-tree-id" in body
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": plan_doc("Executed", body)})
    findings = cla.verify_all(root)
    assert findings[0].classification == "ANOMALY"
    assert "invalid State identity format" in findings[0].reasons[0]
    assert run_tool(root).returncode == 1


def test_absent_identity_without_deferral_is_anomaly(tmp_path):
    """Absence without a declared deferral is still the invalid-format signal."""
    body = ANCHOR_FIELDS.replace(f"`{TREE_ID}`", "`pending`").replace(
        f"`{DELTA_ID}`", "`pending`"
    )
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": plan_doc("Executed", body)})
    findings = cla.verify_all(root)
    assert findings[0].classification == "ANOMALY"


def test_identity_divergent_from_the_materialized_commit_tree_stays_valid(
    tmp_path,
):
    """Closure identity and the closing commit tree are not the same concept.

    C-1 checks the anchor's own structure: a state identity that differs from the
    tree of some other commit is not a C-1 contradiction (the closing commit may
    legitimately carry governance; RFC-75 `Mecanismo 7`).
    """
    other_tree = "c" * 40
    body = ANCHOR_FIELDS.replace(
        "- Validity / stale: `vigente`",
        "- Validity / stale: `vigente`\n"
        f"- Árbol material del commit de cierre: `{other_tree}`",
    )
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": plan_doc("Executed", body)})
    findings = cla.verify_all(root)
    assert findings[0].classification == "VALID"


# --- A1 / A2 lineage -----------------------------------------------------------


def test_a1_original_anchor_valid(tmp_path):
    """A1 alone (original validation) is valid."""
    root = make_repo(tmp_path, {
        "docs/plans/99-sample.md": plan_doc("Executed", ANCHOR_FIELDS),
    })
    assert cla.verify_all(root)[0].classification == "VALID"


def test_a2_revalidation_referencing_a1_is_valid(tmp_path):
    """A2 records a new validation; it references A1 and does not replace it."""
    a2 = (
        ANCHOR_FIELDS
        + "\n- **A2 (revalidación)** — referencia al anchor original: **A1**; "
        "estado revalidado (C2): State identity "
        f"T2 = `{TREE_ID[:39]}2`; command-set idéntico al de A1; "
        "factores ambientales sin cambios; resultado PASS."
    )
    doc = plan_doc("Executed", a2)
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "VALID"


def test_a2_without_a1_reference_is_anomaly(tmp_path):
    """A revalidation anchor block without a minimal A1 lineage -> ANOMALY."""
    a2 = ANCHOR_FIELDS + (
        "\n- **A2 (revalidación)** — estado revalidado (C2): "
        "State identity T2 = `%s`; resultado PASS."
        % (TREE_ID[:39] + "2")
    )
    doc = plan_doc("Executed", a2)
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "ANOMALY"
    assert "without reference to A1" in findings[0].reasons[0]


# --- Status and N/A -------------------------------------------------------------


def test_planned_member_without_validation_is_na(tmp_path):
    """A PLANNED member with empty sections has no claim: N/A, not a GAP."""
    doc = plan_doc(
        "Aprobado para ejecución",
        "<!-- Se completa al ejecutar. -->",
        "<!-- Se completa al cerrar. -->",
    )
    root = make_repo(tmp_path, {"docs/plans/99-sample.md": doc})
    findings = cla.verify_all(root)
    assert findings[0].classification == "N/A"
    assert run_tool(root).returncode == 0


# --- Determinism -----------------------------------------------------------------


def test_deterministic_report(tmp_path):
    root = make_repo(tmp_path, {
        "docs/plans/01-legacy.md": legacy_doc(),
        "docs/plans/99-sample.md": plan_doc("Executed", ANCHOR_FIELDS),
    })
    first = cla.format_report(cla.verify_all(root))
    second = cla.format_report(cla.verify_all(root))
    assert first == second
    assert cla.verify_all(root) == cla.verify_all(root)


# --- CLI / real repo (dogfooding) -------------------------------------------------


def test_real_repo_expected_classifications():
    """Dogfooding expectations on the real repo (Plan 98 §17.2/§36):
    plans 96/97 VALID, legacy plans EXCLUDED, plan 98 is a regime member —
    N/A while PLANNED and VALID once its own anchor is registered (self-
    dogfooding); never EXCLUDED/GAP/ANOMALY."""
    res = run_tool(REPO_ROOT)
    assert res.returncode == 0, res.stdout
    assert "96-change-lifecycle-unit-b-increments-1-3.md: VALID" in res.stdout
    assert "97-change-lifecycle-unit-c-increment-2.md: VALID" in res.stdout
    assert re.search(
        r"98-change-lifecycle-unit-d-increment-4\.md: (?:N/A|VALID)", res.stdout
    )
    assert "94-change-lifecycle-master-action-plan.md: EXCLUDED" in res.stdout
    assert "95-change-lifecycle-unit-a-increment-0.md: EXCLUDED" in res.stdout
    # Plan 146 is never an ANOMALY. On `dev` its anchor carries the literals
    # (VALID); on the released `master` tree its anchor declares them deferred
    # to the checkpoint section (GAP). Both are non-blocking; neither is an
    # invalid value (plan 147, F1).
    assert re.search(
        r"146-release-promotion-11-6-1\.md: (?:VALID|GAP)", res.stdout
    ), res.stdout
    assert "ANOMALY=0" in res.stdout


# --- stdlib only ------------------------------------------------------------------

def test_tool_uses_only_stdlib():
    assert_tool_imports_only_stdlib(TOOL, {"check_lifecycle_anchor"})
