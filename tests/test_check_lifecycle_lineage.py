"""Tests for tools/check_lifecycle_lineage.py (C-3, Plan 100 / RFC-75).

Covers the C-3 matrix T01..T28 of
docs/plans/100-change-lifecycle-lineage-integrity.md §18 plus the permanent
adversarial scenarios of §20: opener namespace, duplicate identities
(same subsection and across subsections), required finding fields (CL-8),
state vocabulary, reopened boundary, resolution consistency, cross-artifact
target existence, correction origins (CL-6), revalidation-claim support from
the artifact's own Validation Anchor / checkpoint (CL-7), absence markers,
unparseable content, RFC- namespace refs, container without level-3
subsections, semicolons inside field values (parser splits by labels, never
by ``;`` blindly), F-3 ambiguity (GAP without tie-break), legacy
no-retroactivity, determinism, repeated execution, exit codes, dogfooding
over the real repository and stdlib-only. Fixtures build synthetic repo trees
under tmp_path; no network, no git and no dependency on the real repository
state except the dogfooding test.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_lifecycle_lineage.py"

import check_lifecycle_lineage as cll  # noqa: E402
from testsupport import assert_tool_imports_only_stdlib  # noqa: E402


def write_plan(root: Path, doc: str, name: str = "99-sample.md") -> Path:
    path = root / "docs" / "plans" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")
    return path


def run_tool(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True, text=True, cwd=str(root),
    )


def one_finding(root: Path) -> cll.LineageFinding:
    findings = cll.verify_all(root)
    assert len(findings) == 1
    return findings[0]


def lineage_doc(
    *,
    number: int = 99,
    status: str = "Executed",
    findings: str = "",
    corrections: str = "",
    anchor: str = "",
    checkpoint: str = "",
    pending: str = "",
    container: bool = True,
    container_preamble: str = "Registros reales (fixture).",
) -> str:
    """Minimal numbered plan carrying the Increment-2 lineage container."""
    parts = [
        f"# Plan {number} — Sample",
        "",
        f"**Status:** {status}",
        "**Change Level:** L2",
        "",
        "## Objetivo",
        "",
        "Texto.",
        "",
    ]
    if anchor:
        parts += ["## Validation anchor", anchor.strip(), ""]
    if checkpoint:
        parts += ["## Checkpoint / cierre", checkpoint.strip(), ""]
    if container:
        parts += [
            "## Findings / Correcciones / Pending",
            "",
            container_preamble,
            "",
        ]
        if findings:
            parts += ["### Findings", findings.strip(), ""]
        if corrections:
            parts += ["### Correcciones", corrections.strip(), ""]
        if pending:
            parts += ["### Pending decisions", pending.strip(), ""]
    return "\n".join(parts) + "\n"


def finding_record(
    state: str = "`open`",
    *,
    resolution: str | None = None,
    extra_fields: str = "",
    ref: str = "<PLAN-99>:F-1",
    observation: str = "sample observation",
) -> str:
    fields = [
        f"estado: {state}",
        f"observación: {observation}",
        "evidencia original: observed behaviour at HEAD `abc1234`",
        "estado Git observado: `dev` @ working tree, limpio",
        "provenance original: session audit",
    ]
    if resolution is not None:
        fields.append(f"resolución: {resolution}")
    if extra_fields:
        fields.append(extra_fields)
    return f"- `{ref}` — " + "; ".join(fields) + ";"


def correction_record(
    *,
    ref: str = "<PLAN-99>:C-1",
    refs_origen: str = "`<PLAN-99>:F-1`",
    alcance: str = "batería del repo sobre el estado corregido",
    evidencia: str = "commit C1 `abc1234`; suite ejecutada",
    extra_fields: str = "",
) -> str:
    fields = [
        f"refs origen: {refs_origen}",
        f"alcance de revalidación: {alcance}",
        f"evidencia (Git/commit/estado): {evidencia}",
    ]
    if extra_fields:
        fields.append(extra_fields)
    return f"- `{ref}` — " + "; ".join(fields) + ";"


def anchor_with_v2() -> str:
    return (
        "- Declared scope: battery of the repo.\n"
        "- Validation command-set: `python -m pytest tests/`\n"
        "- Effective inputs (repo content): repo content.\n"
        "- Observed dependencies: no instrumentado\n"
        "- Environmental factors: OS Windows; sin red.\n"
        "- Scoped Content Identity:\n"
        "  - State identity: T1 = `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0`\n"
        "  - Delta scoped identity: `b1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0`\n"
        "- Validity / stale: `vigente` (V1); revalidada por **V2** "
        "(batería completa).\n"
    )


def checkpoint_record(consistency: str = "V1 == C1 tree → **PASS**.") -> str:
    return (
        "- Commits de cierre:\n"
        "  - C1 `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0` — commit.\n"
        "- Estado validado: V1 sobre C1.\n"
        "- Estado de cierre: tree id del commit final.\n"
        f"- Consistencia checkpoint↔anchor: {consistency}\n"
        "- Governance aplicada: docs-only.\n"
        "- Condición derivada: **`Closed` (docs-only, sin release)**\n"
    )


def real_finding(state: str = "`resolved`", *, resolution: str = "") -> str:
    """Corpus-style rich finding used by the happy-path chain tests."""
    res = (
        ""
        if not resolution
        else f"; resolución: {resolution}"
    )
    return (
        f"- `<PLAN-99>:F-1` — estado: {state}; "
        "observación: detector seleccionaba el anchor por recencia; "
        "evidencia original: comportamiento descrito en §12; "
        "estado Git observado: `dev` @ `abc1234`, working tree limpio; "
        "provenance original: audit de sesión"
        + res
        + ";"
    )


# --- T01..T03 happy path ----------------------------------------------------


def test_t01_finding_open_complete_is_valid(tmp_path):
    """T01: an open finding with all five required fields is VALID."""
    doc = lineage_doc(findings=finding_record("`open`"))
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "VALID"
    assert run_tool(tmp_path).returncode == 0


def test_t02_resolved_finding_with_correction_and_anchor_support_is_valid(
    tmp_path,
):
    """T02: F-1 resolved with a registered C-1 and revalidation evidence in
    the artifact's Validation Anchor is VALID (plan 99 corpus shape)."""
    resolution = "corregido por `<PLAN-99>:C-1`; selección por "
    "correspondencia de estado implementada"
    doc = lineage_doc(
        findings=real_finding(
            "`resolved`", resolution=resolution
        ),
        corrections=correction_record(
            alcance="suite C-2 sobre C1 (V1) y sobre el estado final (V2)",
            evidencia="commit C1 `abc1234`; adversarial review PASS",
        ),
        anchor=anchor_with_v2(),
        checkpoint=checkpoint_record(),
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "VALID"
    assert run_tool(tmp_path).returncode == 0


def test_t03_complete_correction_is_valid(tmp_path):
    """T03: a complete correction (refs origen, alcance, evidencia) whose
    scope does not claim a revalidation result is VALID."""
    doc = lineage_doc(
        findings=finding_record("`open`"),
        corrections=correction_record(),
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "VALID"
    assert run_tool(tmp_path).returncode == 0


# --- T04..T06 population -----------------------------------------------------


def test_t04_declared_absence_is_na(tmp_path):
    """T04: declared absence markers make the member N/A."""
    doc = lineage_doc(
        findings="- `No findings detected / N/A` "
        "(no se fabrican findings sintéticos).",
        corrections="- `N/A` (ninguna corrección).",
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "N/A"
    assert run_tool(tmp_path).returncode == 0


def test_t05_legacy_without_container_is_excluded(tmp_path):
    """T05: a legacy plan without the lineage container is EXCLUDED
    (no-retroactivity; absence of fields is not invalidity)."""
    doc = (
        "# Plan 01 — Legacy\n\n"
        "**Status:** Executed\n\n"
        "## Objetivo\n\nTexto.\n"
    )
    write_plan(tmp_path, doc, "01-legacy.md")
    finding = one_finding(tmp_path)
    assert finding.classification == "EXCLUDED"
    assert run_tool(tmp_path).returncode == 0


def test_t06_lifecycle_refs_in_prose_without_container_is_boundary(
    tmp_path,
):
    """T06: qualified lifecycle refs in prose without the container are
    BOUNDARY (structural ambiguity; human review; exit code 0)."""
    doc = (
        "# Plan 02 — Boundary\n\n"
        "**Status:** Executed\n\n"
        "Corpus mention: `<PLAN-98>:F-1` without a container.\n"
    )
    write_plan(tmp_path, doc, "02-boundary.md")
    finding = one_finding(tmp_path)
    assert finding.classification == "BOUNDARY"
    assert run_tool(tmp_path).returncode == 0


# --- T07..T18 rule semantics ------------------------------------------------


def test_t07_missing_required_field_is_gap(tmp_path):
    """T07: a finding without `evidencia original` is GAP (exit code 0)."""
    record = finding_record("`open`").replace(
        "evidencia original: observed behaviour at HEAD `abc1234`; ", ""
    )
    doc = lineage_doc(findings=record)
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "evidencia original" in finding.reasons[0]
    assert run_tool(tmp_path).returncode == 0


def test_t08_unknown_state_is_anomaly(tmp_path):
    """T08: a state outside the documented vocabulary is ANOMALY (exit 1)."""
    doc = lineage_doc(findings=finding_record("`waiting`"))
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert run_tool(tmp_path).returncode == 1


def test_t09_reopened_state_is_gap_boundary(tmp_path):
    """T09: `reopened` is a documented v1 boundary (GAP, human review)."""
    doc = lineage_doc(
        findings=finding_record(
            "`reopened`",
            extra_fields="owner: mantenedor; destino: plan posterior",
        )
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "reopened" in finding.reasons[0]
    assert run_tool(tmp_path).returncode == 0


def test_t10_alien_namespace_opener_is_anomaly(tmp_path):
    """T10: a record opener in a namespace different from the artifact
    (PLAN-98 ref inside plan 99) is ANOMALY (R-L1-1)."""
    doc = lineage_doc(
        findings=finding_record("`open`", ref="<PLAN-98>:F-1")
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "R-L1-1" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 1


def test_t11_duplicate_identity_is_anomaly(tmp_path):
    """T11: the same record identity twice in the same subsection is
    ANOMALY (R-L1-2)."""
    record = finding_record("`open`")
    doc = lineage_doc(findings=record + "\n" + record)
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "duplicate lineage record identity" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 1


def test_t12_resolved_without_resolution_is_gap(tmp_path):
    """T12: resolved/partially-resolved without a resolución field is GAP."""
    doc = lineage_doc(findings=finding_record("`resolved`"))
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "without a resolución field" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 0


def test_t13_contradictory_resolution_is_anomaly(tmp_path):
    """T13: `resolved` with a resolution that says `sin resolver` is
    ANOMALY (R-L1-5)."""
    doc = lineage_doc(
        findings=finding_record("`resolved`", resolution="sin resolver")
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "contradicts estado resolved" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 1


def test_t14_resolution_references_missing_correction_is_anomaly(tmp_path):
    """T14: a resolution referencing `<PLAN-99>:C-9` without a C-9 record
    is ANOMALY (R-L1-7)."""
    doc = lineage_doc(
        findings=finding_record(
            "`resolved`",
            resolution="corregido por `<PLAN-99>:C-9`",
        )
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "R-L1-7" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 1


def test_t15_deferred_without_owner_or_destino_is_gap(tmp_path):
    """T15: deferred without owner/destino is GAP (R-L1-6)."""
    doc = lineage_doc(findings=finding_record("`deferred`"))
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "deferred without owner or destino" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 0


def test_t16_correction_without_origin_is_gap(tmp_path):
    """T16: a correction without refs origen (or without an F- ref) is
    GAP (R-L1-8)."""
    doc = lineage_doc(
        findings=finding_record("`open`"),
        corrections=correction_record(refs_origen="audit interno"),
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "without a qualified F- ref" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 0


def test_t17_revalidation_claim_without_support_is_gap(tmp_path):
    """T17: a correction declaring a revalidation result without declared
    evidence in the Validation Anchor or PASS in the checkpoint is GAP
    (R-L1-9; anti-circularity)."""
    doc = lineage_doc(
        findings=finding_record("`open`"),
        corrections=correction_record(
            alcance="revalidación V2 sobre el estado final",
            evidencia="resultado PASS",
        ),
        anchor=(
            "- Declared scope: battery.\n"
            "- Validation command-set: `python -m pytest tests/`\n"
            "- Validity / stale: `vigente` (V1).\n"
        ),
        checkpoint=checkpoint_record(
            consistency="V1 == C1 tree (revisión manual)."
        ).replace(
            "- Condición derivada: **`Closed` (docs-only, sin release)**\n",
            "",
        ),
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "R-L1-9" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 0


def test_t18_absence_marker_with_real_record_is_anomaly(tmp_path):
    """T18: `No findings detected / N/A` together with a real record in the
    same subsection is ANOMALY (R-L1-10)."""
    doc = lineage_doc(
        findings=(
            "- `No findings detected / N/A` (no se fabrican findings).\n"
            + finding_record("`open`")
        )
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "absence marker declared together with real records" in " ".join(
        finding.reasons
    )
    assert run_tool(tmp_path).returncode == 1


# --- T19..T22 cross-artifact, RFC refs, unparseable -------------------------


def test_t19_cross_artifact_ref_resolvable_is_valid(tmp_path):
    """T19: a correction in plan 99 referencing a real finding of plan 98
    (when one exists in the scanned corpus) is VALID."""
    doc98 = lineage_doc(
        number=98,
        findings=finding_record(
            "`open`", ref="<PLAN-98>:F-1"
        ),
    )
    doc99 = lineage_doc(
        number=99,
        findings=finding_record("`open`"),
        corrections=correction_record(
            refs_origen="`<PLAN-98>:F-1`"
        ),
    )
    write_plan(tmp_path, doc98, "98-other.md")
    write_plan(tmp_path, doc99)
    result = run_tool(tmp_path)
    assert result.returncode == 0
    assert "98-other.md: VALID" in result.stdout
    assert "99-sample.md: VALID" in result.stdout


def test_t20_cross_artifact_ref_missing_is_anomaly(tmp_path):
    """T20: a correction referencing `<PLAN-98>:F-1` when plan 98 registers
    no such finding is ANOMALY (R-L1-8)."""
    doc = lineage_doc(
        corrections=correction_record(refs_origen="`<PLAN-98>:F-1`")
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "not registered in the scanned corpus" in " ".join(
        finding.reasons
    )
    assert run_tool(tmp_path).returncode == 1


def test_t21_rfc_namespace_ref_is_format_valid(tmp_path):
    """T21: RFC- namespace F- refs are format-verified only (resolution out
    of the v1 domain): VALID, exit 0."""
    doc = lineage_doc(
        findings=finding_record("`open`"),
        corrections=correction_record(
            refs_origen="`<RFC-75>:F-1`",
            alcance="revisión del formato (sin claim de resultado)",
        ),
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "VALID"
    assert run_tool(tmp_path).returncode == 0


def test_t22_unparseable_bullet_is_gap(tmp_path):
    """T22: a bullet without a canonical opener under ### Findings is
    content not parseable as a record or absence: GAP (R-L1-11)."""
    doc = lineage_doc(
        findings="- bare text without a qualified lifecycle ref.",
        corrections="- `N/A`.",
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "not parseable" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 0


# --- T23..T26 determinism, repetition, exit codes, comments -----------------


def test_t23_determinism(tmp_path):
    """T23: identical inputs produce identical reports and findings."""
    doc = lineage_doc(
        findings=real_finding(),
        corrections=correction_record(
            alcance="suite C-2 sobre C1 (V1) y sobre el estado final (V2)",
        ),
        anchor=anchor_with_v2(),
        checkpoint=checkpoint_record(),
    )
    write_plan(tmp_path, doc)
    first = cll.format_report(cll.verify_all(tmp_path))
    second = cll.format_report(cll.verify_all(tmp_path))
    assert first == second
    assert cll.verify_all(tmp_path) == cll.verify_all(tmp_path)
    out1 = run_tool(tmp_path).stdout
    out2 = run_tool(tmp_path).stdout
    assert out1 == out2


def test_t24_repeated_execution_is_stable(tmp_path):
    """T24: running C-3 twice in a row keeps classifications and exit code
    stable (read-only, no state change)."""
    doc = lineage_doc(
        findings=finding_record("`open`"),
        corrections=correction_record(),
    )
    write_plan(tmp_path, doc)
    res1 = run_tool(tmp_path)
    res2 = run_tool(tmp_path)
    assert res1.returncode == res2.returncode == 0
    assert (
        "99-sample.md: VALID" in res1.stdout
        and "99-sample.md: VALID" in res2.stdout
    )


def test_t25_exit_codes_gap_zero_anomaly_one(tmp_path):
    """T25: GAP corpora exit 0; ANOMALY corpora exit 1."""
    gap_dir = tmp_path / "gap"
    gap_dir.mkdir()
    gap_doc = lineage_doc(
        findings=finding_record("`open`").replace(
            "provenance original: session audit; ", ""
        )
    )
    write_plan(gap_dir, gap_doc)
    assert run_tool(gap_dir).returncode == 0

    anomaly_dir = tmp_path / "anomaly"
    anomaly_dir.mkdir()
    anomaly_doc = lineage_doc(findings=finding_record("`waiting`"))
    write_plan(anomaly_dir, anomaly_doc)
    assert run_tool(anomaly_dir).returncode == 1


def test_t26_html_comments_are_not_content(tmp_path):
    """T26: template guidance in HTML comments has no effect: a member whose
    subsections only carry comments is N/A, and comments mixed with records
    do not add GAP/ANOMALY reasons."""
    doc = lineage_doc(
        findings="<!-- Template guidance: - `<PLAN-99>:F-01` ... -->",
        corrections="<!-- Se completa al ejecutar. -->",
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "N/A"
    assert run_tool(tmp_path).returncode == 0

    mixed = lineage_doc(
        findings=(
            "<!-- Note: format below. -->\n"
            + finding_record("`open`")
        )
    )
    second = tmp_path / "second"
    second.mkdir()
    write_plan(second, mixed, "99-mixed.md")
    findings = {f.rel.name: f for f in cll.verify_all(second)}
    assert findings["99-mixed.md"].classification == "VALID"


# --- T27/T28 dogfooding and stdlib ------------------------------------------


def test_t27_real_repo_dogfooding():
    """T27: dogfooding over the real repository (plan 100 §19): plan 98 N/A
    (declared absence), plan 99 VALID (real F-1 -> C-1 chain), plans 96/97
    and legacy EXCLUDED, GAP=4 (the declared legacy Closed+open cases
    155/158/168/169), ANOMALY=0. Plan 100 is lifecycle-stable: it
    is BOUNDARY while it carries qualified lifecycle refs without its own
    lineage container (its creation phase, §14.1) and N/A (or VALID) once its
    container is registered at closure (C2)."""
    result = run_tool(REPO_ROOT)
    assert result.returncode == 0, result.stdout
    assert (
        "96-change-lifecycle-unit-b-increments-1-3.md: EXCLUDED"
        in result.stdout
    )
    assert (
        "97-change-lifecycle-unit-c-increment-2.md: EXCLUDED"
        in result.stdout
    )
    assert "98-change-lifecycle-unit-d-increment-4.md: N/A" in result.stdout
    assert "99-change-lifecycle-f1-c2-gc1-correction.md: VALID" in result.stdout
    assert re.search(
        r"100-change-lifecycle-lineage-integrity\.md: "
        r"(?:BOUNDARY|N/A|VALID|EXCLUDED)",
        result.stdout,
    )
    assert "94-change-lifecycle-master-action-plan.md: EXCLUDED" in result.stdout
    assert "95-change-lifecycle-unit-a-increment-0.md: EXCLUDED" in result.stdout
    assert "GAP=4" in result.stdout
    assert "ANOMALY=0" in result.stdout


def test_t29_closed_with_open_finding_is_anomaly(tmp_path):
    """T29 (R-L1-13): a plan that declares Closed cannot keep an open
    finding; this is a verifiable contradiction, not a GAP."""
    doc = lineage_doc(
        checkpoint=checkpoint_record(),
        findings=finding_record("`open`"),
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "R-L1-13" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 1


def test_t30_legacy_closed_open_finding_is_gap(tmp_path):
    """T30 (R-L1-13 legacy): the four real-corpus cases are declared legacy;
    they are recorded by reference and reported as GAP, never ANOMALY."""
    doc = lineage_doc(
        number=155,
        checkpoint=checkpoint_record(),
        findings=finding_record("`open`", ref="<PLAN-155>:F-1"),
    )
    write_plan(tmp_path, doc, "155-legacy.md")
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "legacy" in " ".join(finding.reasons)
    assert "R-L1-13" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 0


def test_t28_tool_uses_only_stdlib():
    assert_tool_imports_only_stdlib(TOOL)


# --- Adversarial scenarios (plan 100 §20) -----------------------------------


def test_adversarial_reference_to_nonexistent_artifact_is_anomaly(tmp_path):
    """A correction referencing a finding of an artifact number absent from
    the scanned corpus is ANOMALY (never silently tolerated)."""
    doc = lineage_doc(
        corrections=correction_record(refs_origen="`<PLAN-101>:F-1`")
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert run_tool(tmp_path).returncode == 1


@pytest.mark.parametrize(
    "bad_bullet",
    [
        "- PLAN-99:F-1 — estado: `open`; observación: x; evidencia original: "
        "e; estado Git observado: dev; provenance original: p;",
        "- F-1 — estado: `open`; observación: x; evidencia original: e; "
        "estado Git observado: dev; provenance original: p;",
        "- `<PLAN-99>:F-01` — estado: `open`; observación: x; evidencia "
        "original: e; estado Git observado: dev; provenance original: p;",
        "- `<PLAN-99>: f-1` — estado: `open`; observación: x; evidencia "
        "original: e; estado Git observado: dev; provenance original: p;",
        "- `<PLAN-99>:F-1` estado: `open`; observación: x; evidencia "
        "original: e; estado Git observado: dev; provenance original: p;",
    ],
)
def test_adversarial_record_format_variants_are_never_valid(
    tmp_path, bad_bullet
):
    """Ref format variants outside the §14 contract (bare, unbackticked,
    zero-padded, lowercased or missing separator) are GAP via R-L1-11 —
    never VALID by invented tolerance."""
    doc = lineage_doc(findings=bad_bullet)
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification != "VALID"
    assert finding.classification in {"GAP", "ANOMALY"}
    assert run_tool(tmp_path).returncode in {0, 1}


def test_adversarial_superseded_without_replacement_has_no_new_rule(
    tmp_path,
):
    """superseded carries no v1 replacement-content rule (no corpus exemplar
    and no invented normative requirement): a complete record is VALID."""
    doc = lineage_doc(
        findings=finding_record(
            "`superseded`",
            resolution="reemplazado por un finding nuevo posterior",
        )
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "VALID"
    assert run_tool(tmp_path).returncode == 0


def test_adversarial_revalidation_pass_with_checkpoint_fail_is_anomaly(
    tmp_path,
):
    """R-L1-9 extended: a correction declaring revalidation PASS while the
    artifact's checkpoint declares explicit FAIL is ANOMALY (exit 1)."""
    doc = lineage_doc(
        findings=finding_record("`open`"),
        corrections=correction_record(
            alcance="revalidación V2 sobre el estado final",
            evidencia="resultado PASS",
        ),
        anchor=anchor_with_v2(),
        checkpoint=checkpoint_record(consistency="V2 sobre C2 → **FAIL**."),
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "checkpoint declares FAIL" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 1


def test_adversarial_duplicate_across_subsections_is_anomaly(tmp_path):
    """An F-1 record listed under both Findings and Correcciones is a
    duplicate identity (R-L1-2): ANOMALY."""
    record = finding_record("`open`")
    doc = lineage_doc(findings=record, corrections=record)
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "ANOMALY"
    assert "duplicate lineage record identity" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 1


def test_adversarial_container_without_level3_is_never_excluded(tmp_path):
    """A container without level-3 lineage subsections is N/A when empty and
    GAP when it carries visible unstructured content — never EXCLUDED."""
    empty_doc = lineage_doc(
        findings="",
        corrections="",
        container_preamble="",
    )
    write_plan(tmp_path, empty_doc, "01-empty.md")
    empty_finding = one_finding(tmp_path)
    assert empty_finding.classification == "N/A"
    assert run_tool(tmp_path).returncode == 0

    messy_dir = tmp_path / "messy"
    messy_dir.mkdir()
    messy_doc = lineage_doc(
        findings="",
        corrections="",
        container_preamble="contenido visible sin estructura de nivel 3.",
    )
    write_plan(messy_dir, messy_doc, "02-messy.md")
    findings = {f.rel.name: f for f in cll.verify_all(messy_dir)}
    assert findings["02-messy.md"].classification == "GAP"


def test_adversarial_semicolons_inside_values_split_by_labels(tmp_path):
    """Values may contain `;` (dates, lists); the parser splits by labels,
    never by a blind `;` (R-L1-11): the finding stays VALID and the value
    keeps its inner separators."""
    observation = (
        "primera parte; segunda parte (2026-09-02; 2026-09-03); "
        "con `estado Git observado: x` citado como texto"
    )
    doc = lineage_doc(
        findings=finding_record("`open`", observation=observation)
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "VALID"
    assert run_tool(tmp_path).returncode == 0


def test_adversarial_multiple_anchor_validation_records_are_gap(tmp_path):
    """F-3 (duplicate validation records) is never resolved: multiple
    revalidation markers in the Validation Anchor make declared support
    ambiguous — GAP, without an invented tie-break (R-L1-9)."""
    anchor = (
        "- Declared scope: battery.\n"
        "- Validation command-set: `python -m pytest tests/`\n"
        "- Validity / stale: `vigente` (V1); revalidada por **V2** "
        "(batería sobre C2) y por **V2** (batería sobre C3).\n"
    )
    doc = lineage_doc(
        findings=finding_record("`open`"),
        corrections=correction_record(
            alcance="revalidación V2 sobre el estado final",
            evidencia="resultado PASS",
        ),
        anchor=anchor,
        checkpoint=checkpoint_record(
            consistency="V1 == C1 tree (revisión manual)."
        ).replace(
            "- Condición derivada: **`Closed` (docs-only, sin release)**\n",
            "",
        ),
    )
    write_plan(tmp_path, doc)
    finding = one_finding(tmp_path)
    assert finding.classification == "GAP"
    assert "ambiguous" in " ".join(finding.reasons)
    assert run_tool(tmp_path).returncode == 0
