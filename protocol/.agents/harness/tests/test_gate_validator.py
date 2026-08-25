"""Tests for gate_validator.py (optional structural validator, RFC-57)."""

from __future__ import annotations

import json
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

import gate_validator

HARNESS = Path(__file__).resolve().parents[1]
VALIDATOR = HARNESS / "gate_validator.py"


def make_artifact(tmp_path: Path, artifact_name: str, sections: dict[str, str]) -> Path:
    """Build a fake adoption layout and an artifact with the given sections."""
    session = tmp_path / ".project" / f"test-{uuid.uuid4()}" / "00"
    session.mkdir(parents=True)
    parts = ["# Artifact"]
    for heading, body in sections.items():
        parts.append(f"## {heading}")
        parts.append(body)
    artifact = session / artifact_name
    artifact.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return artifact


def set_rubrics(tmp_path: Path, enabled: bool) -> None:
    (tmp_path / ".agents").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".agents" / "features.toml").write_text(
        f"rubrics = {str(enabled).lower()}\n", encoding="utf-8"
    )


def rubric_block() -> str:
    body = []
    for name in gate_validator.BASE_RUBRICS:
        body.append(f"### {name}")
        body.append("- Criterion")
        body.append("  - Level: MEETS")
        body.append("  - Evidence: ok")
    return "\n".join(body)


def h06_sections(extra: dict | None = None) -> dict:
    sections = {
        "Metadata": "- id: x",
        "Task Reference": "- spec",
        "Execution Plan Reference": "- plan",
        "Verification Objective": "- v",
        "Acceptance Criteria Evaluation": (
            "```toml\n[[acceptance_criteria]]\nclaim_id = \"AC-01\"\n"
            'criterion = "c"\nresult = "PASS"\nclaim_class = "attested"\n```'
        ),
        "Test Results": "- none",
        "Issues Found": "- none",
        "Final Decision": "```toml\n[decision]\nresult = \"COMPLETED\"\n```",
        "Confidence": "- high",
        "State Transition": "- x",
    }
    if extra:
        sections.update(extra)
    return sections


def test_valid_h01_passes(tmp_path):
    artifact = make_artifact(tmp_path, "TASK_SPECIFICATION.md", {
        "Objective": "Build X.",
        "Expected Outcome": "X works.",
        "Scope": "Only X.",
        "Constraints": "None.",
        "Acceptance Criteria": (
            "- The API shall return HTTP 200.\n"
            "- When the id is missing, the API shall return HTTP 400.\n"
        ),
        "Assumptions": "- none",
        "Unknowns": "- none",
        "Validation": "- pending",
        "Technical Approach": "```toml\n[technical_approach]\nenabled = [\"tdd\"]\n```",
    })
    checks, decision = gate_validator.validate("H01", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_missing_section_fails(tmp_path):
    artifact = make_artifact(tmp_path, "TASK_SPECIFICATION.md", {
        "Objective": "Build X.",
        "Acceptance Criteria": "- The API shall return HTTP 200.",
    })
    checks, decision = gate_validator.validate("H01", artifact)
    assert decision == "FAIL"
    assert any(c["id"] == "section" and "Validation" in c["evidence"] for c in checks)


def test_non_ears_bullet_fails(tmp_path):
    artifact = make_artifact(tmp_path, "TASK_SPECIFICATION.md", {
        "Objective": "Build X.",
        "Expected Outcome": "X works.",
        "Scope": "X.",
        "Constraints": "None.",
        "Acceptance Criteria": "- It should probably work.",
        "Assumptions": "- none",
        "Unknowns": "- none",
        "Validation": "- pending",
    })
    checks, decision = gate_validator.validate("H01", artifact)
    assert decision == "FAIL"
    assert any(c["id"] == "ears" for c in checks)


def test_h05_bad_final_state_fails(tmp_path):
    artifact = make_artifact(tmp_path, "EXECUTION_SUMMARY.md", {
        "Final Project State": "```toml\n[final_state]\nstatus = \"BROKEN\"\n```",
        "Steps Executed": "```toml\n[[steps_executed]]\norder = 1\naction = \"a\"\nstatus = \"COMPLETED\"\n```",
    })
    checks, decision = gate_validator.validate("H05", artifact)
    assert decision == "FAIL"
    assert any("bad status" in c["evidence"] for c in checks)


def test_h06_bad_decision_fails(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path, "VERIFICATION_REPORT.md",
        h06_sections({"Final Decision": "```toml\n[decision]\nresult = \"DONE\"\n```"}),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any("bad decision.result" in c["evidence"] for c in checks)


def test_h07_branch_incoherence_fails(tmp_path):
    artifact = make_artifact(tmp_path, "VERIFICATION_REPORT.md", {
        "Scope Compliance": "```toml\n[scope_compliance]\nscope_respected = true\nunplanned_changes = [\"x\"]\nuser_authorized_extra_work = false\n```",
    })
    checks, decision = gate_validator.validate("H07", artifact)
    assert decision == "FAIL"
    assert any("Branch A/B incoherent" in c["evidence"] for c in checks)


def test_broken_citation_fails(tmp_path):
    artifact = make_artifact(tmp_path, "TASK_SPECIFICATION.md", {
        "Objective": "Build X.",
        "Validation": "See `missing-file.md` §Nowhere.",
    })
    checks, decision = gate_validator.validate("H01", artifact)
    assert decision == "FAIL"
    assert any("broken citation" in c["evidence"] for c in checks)


def test_valid_citation_resolves(tmp_path):
    session = tmp_path / ".project" / f"test-{uuid.uuid4()}" / "00"
    session.mkdir(parents=True)
    (session / "notes.md").write_text("# Real\n\ncontent\n", encoding="utf-8")
    artifact = session / "TASK_SPECIFICATION.md"
    sections = {
        "Objective": "Build X.",
        "Expected Outcome": "X works.",
        "Scope": "X.",
        "Constraints": "None.",
        "Acceptance Criteria": "- The API shall return HTTP 200.",
        "Assumptions": "- none",
        "Unknowns": "- none",
        "Validation": "See `notes.md` §Real.",
    }
    parts = ["# Artifact"]
    for heading, body in sections.items():
        parts.append(f"## {heading}")
        parts.append(body)
    artifact.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    checks, decision = gate_validator.validate("H01", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_rubrics_missing_fails(tmp_path):
    set_rubrics(tmp_path, True)
    artifact = make_artifact(tmp_path, "VERIFICATION_REPORT.md", h06_sections())
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any("missing ## Rubric Evaluation" in c["evidence"] for c in checks)


def test_rubrics_valid_passes(tmp_path):
    set_rubrics(tmp_path, True)
    artifact = make_artifact(
        tmp_path, "VERIFICATION_REPORT.md",
        h06_sections({"Rubric Evaluation": rubric_block()}),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_unsupported_trigger_raises(tmp_path):
    artifact = make_artifact(tmp_path, "X.md", {"Objective": "x"})
    with pytest.raises(ValueError):
        gate_validator.validate("Z99", artifact)


def test_list_lists_supported_triggers():
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--list"],
        capture_output=True,
        text=True,
        cwd=str(HARNESS),
    )
    assert result.returncode == 0
    assert "H00 ->" in result.stdout
    assert "D00 ->" in result.stdout


def test_cli_exit_codes(tmp_path):
    ok = make_artifact(tmp_path, "TASK_SPECIFICATION.md", {
        "Objective": "Build X.",
        "Expected Outcome": "X works.",
        "Scope": "X.",
        "Constraints": "None.",
        "Acceptance Criteria": "- The API shall return HTTP 200.",
        "Assumptions": "- none",
        "Unknowns": "- none",
        "Validation": "- pending",
    })
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--trigger", "H01", "--artifact", str(ok)],
        capture_output=True,
        text=True,
        cwd=str(HARNESS),
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["decision"] == "PASS"


def make_h04_plan(tmp_path: Path, profile: str, with_context_reference: bool) -> Path:
    """Build an EXECUTION_PLAN for the given task profile in a fake session."""
    session = tmp_path / ".project" / f"test-{uuid.uuid4()}" / "00"
    session.mkdir(parents=True)
    (session / "TASK_ANALYSIS.md").write_text(
        "# Analysis\n\n"
        "## Task Profile\n\n"
        "```toml\n"
        "[task_profile]\n"
        f'value = "{profile}"\n'
        'justification = "bounded change"\n'
        "```\n",
        encoding="utf-8",
    )
    sections = {
        "Metadata": "- x",
        "Task Reference": "- spec",
        "Objective": "- o",
        "Approach Summary": "- a",
        "Technical Approach": "- t",
        "Implementation Steps": "- s",
        "Affected Components": "- c",
        "Dependencies": "- d",
        "Risks": "- r",
        "Validation Strategy": "- v",
        "Rollback Considerations": "- rb",
        "Plan Decision": "- p",
        "State Transition": "- st",
    }
    if with_context_reference:
        sections["Context Reference"] = "- ctx"
    parts = ["# Plan"]
    for heading, body in sections.items():
        parts.append(f"## {heading}")
        parts.append(body)
    artifact = session / "EXECUTION_PLAN.md"
    artifact.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return artifact


def test_h04_trivial_omits_context_reference_passes(tmp_path):
    artifact = make_h04_plan(tmp_path, "trivial", with_context_reference=False)
    checks, decision = gate_validator.validate("H04", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "profile" and c["result"] == "PASS" for c in checks)


def test_h04_standard_requires_context_reference(tmp_path):
    artifact = make_h04_plan(tmp_path, "standard", with_context_reference=False)
    checks, decision = gate_validator.validate("H04", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "section" and "Context Reference" in c["evidence"]
        for c in checks
    )


def test_h04_trivial_with_context_reference_passes(tmp_path):
    artifact = make_h04_plan(tmp_path, "trivial", with_context_reference=True)
    checks, decision = gate_validator.validate("H04", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def make_h06_report(
    tmp_path: Path,
    test_results_toml: str,
    session_log: str | None = None,
    evidence: str | None = None,
    evidence_toml: str | None = None,
) -> Path:
    """Build a VERIFICATION_REPORT with a test_results TOML block."""
    session = tmp_path / ".project" / f"test-{uuid.uuid4()}" / "00"
    session.mkdir(parents=True)
    if session_log is not None:
        (session.parent / "SESSION_LOG.md").write_text(session_log, encoding="utf-8")
    if evidence is not None:
        (session / evidence).write_text("evidence\n", encoding="utf-8")
    sections = {
        "Metadata": "- x",
        "Task Reference": "- spec",
        "Execution Plan Reference": "- plan",
        "Verification Objective": "- v",
        "Acceptance Criteria Evaluation": (
            "```toml\n[[acceptance_criteria]]\nclaim_id = \"AC-01\"\n"
            'criterion = "c"\nresult = "PASS"\nclaim_class = "attested"\n```'
        ),
        "Test Results": test_results_toml,
        "Issues Found": "- none",
        "Final Decision": "```toml\n[decision]\nresult = \"COMPLETED\"\n```",
        "Confidence": "- high",
        "State Transition": "- x",
        "Rubric Evaluation": rubric_block(),
    }
    if evidence_toml is not None:
        sections["Evidence"] = evidence_toml
    parts = ["# Report"]
    for heading, body in sections.items():
        parts.append(f"## {heading}")
        parts.append(body)
    artifact = session / "VERIFICATION_REPORT.md"
    artifact.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return artifact


def test_h06_test_results_evidence_passes(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\nclaim_id = \"TR-01\"\ntest = \"pytest -q\"\n"
        'result = "PASS"\ndetails = ""\nevidence = "results.log"\n```',
        evidence="results.log",
        evidence_toml=(
            "```toml\n[[evidence]]\nclass = \"reference\"\nclaim_id = \"TR-01\"\n"
            'ref = "results.log"\n```'
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "test_results" and c["result"] == "PASS" for c in checks)


def test_h06_test_results_session_log_fallback_passes(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\nclaim_id = \"TR-01\"\ntest = \"pytest -q\"\n"
        'result = "PASS"\ndetails = ""\nclaim_class = "attested"\n```',
        session_log="ran: pytest -q\n",
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_h06_test_results_missing_evidence_fails(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\ntest = \"pytest -q\"\nresult = \"PASS\"\n"
        'details = ""\n```',
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any("test command not found in SESSION_LOG.md" in c["evidence"] for c in checks)


def test_h06_test_results_unresolved_evidence_fails(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\ntest = \"pytest -q\"\nresult = \"PASS\"\n"
        'details = ""\nevidence = "missing.log"\n```',
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any("evidence does not resolve" in c["evidence"] for c in checks)


def test_h06_test_results_skipped_exempt(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\ntest = \"pytest -q\"\nresult = \"SKIPPED\"\n"
        'details = ""\n```',
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def h00_sections(sufficiency: bool, next_state: str, intent_level: str) -> dict:
    """Build the full H00 section set of a TASK_ANALYSIS."""
    return {
        "Metadata": "- x",
        "User Request": "- u",
        "Interpreted Objective": "- o",
        "Expected Outcome": "- e",
        "Explicit Requirements": "- r",
        "Explicit Restrictions": "- c",
        "Detected Ambiguities": "- none",
        "Intent Confidence Assessment": (
            f"```toml\n[intent_confidence]\nlevel = \"{intent_level}\"\n```"
        ),
        "Sufficiency Assessment": (
            f"```toml\n[sufficiency]\nready_for_specification = {str(sufficiency).lower()}\n```"
        ),
        "Recommended Next State": (
            f"```toml\nrecommended_next_state = \"{next_state}\"\n```"
        ),
        "Confidence": "- high",
        "Task Profile": (
            "```toml\n[task_profile]\nvalue = \"standard\"\njustification = \"x\"\n```"
        ),
    }


def test_h00_coherent_sections_pass(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "TASK_ANALYSIS.md",
        h00_sections(True, "BUILDING_TASK_SPECIFICATION", "HIGH"),
    )
    checks, decision = gate_validator.validate("H00", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(
        c["id"] == "conflicting_sections" and c["result"] == "PASS"
        for c in checks
    )


def test_h00_sufficiency_next_state_conflict_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "TASK_ANALYSIS.md",
        h00_sections(True, "NEEDS_CLARIFICATION", "HIGH"),
    )
    checks, decision = gate_validator.validate("H00", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "conflicting_sections"
        and c["result"] == "FAIL"
        and "NEEDS_CLARIFICATION" in c["evidence"]
        for c in checks
    )


def test_h00_high_intent_confirm_conflict_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "TASK_ANALYSIS.md",
        h00_sections(True, "CONFIRMING_INTENT", "HIGH"),
    )
    checks, decision = gate_validator.validate("H00", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "conflict_high_intent_confirm"
        and c["result"] == "FAIL"
        and "HIGH" in c["evidence"]
        for c in checks
    )


def h03_sections(decision_result: str, completeness: str, consistency: str) -> dict:
    """Build the full H03 section set of a CONTEXT_VALIDATION_REPORT."""
    return {
        "Metadata": "- x",
        "Context Reference": "- ctx",
        "Validation Objective": "- o",
        "Completeness Evaluation": (
            f"```toml\n[completeness]\nstatus = \"{completeness}\"\n```"
        ),
        "Relevance Evaluation": "```toml\n[relevance]\nstatus = \"VALID\"\n```",
        "Consistency Evaluation": (
            f"```toml\n[consistency]\nstatus = \"{consistency}\"\n```"
        ),
        "Risk Evaluation": "- none",
        "Validation Decision": (
            f"```toml\n[decision]\nresult = \"{decision_result}\"\n```"
        ),
        "Required Actions": "- none",
        "Confidence": "- high",
        "State Transition": "- st",
    }


def test_h03_coherent_decision_passes(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "CONTEXT_VALIDATION_REPORT.md",
        h03_sections("VALIDATED", "COMPLETE", "CONSISTENT"),
    )
    checks, decision = gate_validator.validate("H03", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(
        c["id"] == "conflicting_sections" and c["result"] == "PASS"
        for c in checks
    )


def test_h03_validated_with_incomplete_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "CONTEXT_VALIDATION_REPORT.md",
        h03_sections("VALIDATED", "INCOMPLETE", "CONSISTENT"),
    )
    checks, decision = gate_validator.validate("H03", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "conflicting_sections"
        and c["result"] == "FAIL"
        and "INCOMPLETE" in c["evidence"]
        for c in checks
    )


def test_h03_validated_with_conflicting_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "CONTEXT_VALIDATION_REPORT.md",
        h03_sections("VALIDATED", "COMPLETE", "CONFLICTING"),
    )
    checks, decision = gate_validator.validate("H03", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "conflicting_sections"
        and c["result"] == "FAIL"
        and "CONFLICTING" in c["evidence"]
        for c in checks
    )


def deferred_items_toml(entries: str) -> str:
    return "```toml\n" + entries + "```"


def test_h06_deferred_items_valid_passes(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Deferred Items": deferred_items_toml(
                    '[[deferred_items]]\nitem = "sign-off"\ndeferred = true\n'
                    'confirmed_by = "user"\nconfirmation_date = "2026-08-25"\n'
                ),
                "Rubric Evaluation": rubric_block(),
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "deferred_items" and c["result"] == "PASS" for c in checks)


def test_h06_deferred_items_missing_confirmation_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Deferred Items": deferred_items_toml(
                    '[[deferred_items]]\nitem = "sign-off"\ndeferred = false\n'
                ),
                "Rubric Evaluation": rubric_block(),
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "deferred_items"
        and c["result"] == "FAIL"
        and "deferred is not true" in c["evidence"]
        for c in checks
    )


def test_h06_deferred_items_absent_skips(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections({"Rubric Evaluation": rubric_block()}),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "deferred_items" and c["result"] == "SKIP" for c in checks)


def set_task_profile(artifact: Path, profile: str) -> None:
    (artifact.parent / "TASK_ANALYSIS.md").write_text(
        "# Analysis\n\n"
        "## Task Profile\n\n"
        "```toml\n"
        "[task_profile]\n"
        f'value = "{profile}"\n'
        'justification = "x"\n'
        "```\n",
        encoding="utf-8",
    )


def test_h06_complex_without_review_report_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections({"Rubric Evaluation": rubric_block()}),
    )
    set_task_profile(artifact, "complex")
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "review_report"
        and c["result"] == "FAIL"
        and "REVIEW_REPORT.md" in c["evidence"]
        for c in checks
    )


def test_h06_complex_with_review_report_passes(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections({"Rubric Evaluation": rubric_block()}),
    )
    set_task_profile(artifact, "complex")
    (artifact.parent / "REVIEW_REPORT.md").write_text(
        "# Review\n\n## Recommendation\n\nAPPROVE\n", encoding="utf-8"
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "review_report" and c["result"] == "PASS" for c in checks)


def test_h06_standard_review_report_skips(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections({"Rubric Evaluation": rubric_block()}),
    )
    set_task_profile(artifact, "standard")
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "review_report" and c["result"] == "SKIP" for c in checks)


def test_h06_verified_criterion_without_evidence_fails(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Acceptance Criteria Evaluation": (
                    "```toml\n[[acceptance_criteria]]\nclaim_id = \"AC-01\"\n"
                    'criterion = "c"\nresult = "PASS"\nclaim_class = "verified"\n```'
                ),
                "Rubric Evaluation": rubric_block(),
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any(
        "verified criterion without non-attestation evidence" in c["evidence"]
        for c in checks
    )


def test_h06_verified_criterion_with_measurement_passes(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Acceptance Criteria Evaluation": (
                    "```toml\n[[acceptance_criteria]]\nclaim_id = \"AC-01\"\n"
                    'criterion = "c"\nresult = "PASS"\nclaim_class = "verified"\n```'
                ),
                "Rubric Evaluation": rubric_block(),
                "Evidence": (
                    "```toml\n[[evidence]]\nclass = \"measurement\"\n"
                    'claim_id = "AC-01"\nref = "results.log"\n'
                    'command = "pytest -q"\nexit_code = 0\n```'
                ),
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "evidence" and c["result"] == "PASS" for c in checks)


def test_h06_attestation_only_for_verified_fails(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Acceptance Criteria Evaluation": (
                    "```toml\n[[acceptance_criteria]]\nclaim_id = \"AC-01\"\n"
                    'criterion = "c"\nresult = "PASS"\nclaim_class = "verified"\n```'
                ),
                "Rubric Evaluation": rubric_block(),
                "Evidence": (
                    "```toml\n[[evidence]]\nclass = \"attestation\"\n"
                    'claim_id = "AC-01"\nref = "-"\nactor = "executor"\n'
                    'statement = "wrote the code"\n```'
                ),
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any(
        "verified criterion without non-attestation evidence" in c["evidence"]
        for c in checks
    )


def test_h06_attested_criterion_with_marked_attestation_passes(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Rubric Evaluation": rubric_block(),
                "Evidence": (
                    "```toml\n[[evidence]]\nclass = \"attestation\"\n"
                    'claim_id = "AC-01"\nref = "-"\nactor = "executor"\n'
                    'statement = "wrote the code"\n```'
                )
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_h06_unmarked_criterion_fails(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Acceptance Criteria Evaluation": (
                    "```toml\n[[acceptance_criteria]]\nclaim_id = \"AC-01\"\n"
                    'criterion = "c"\nresult = "PASS"\n```'
                ),
                "Rubric Evaluation": rubric_block(),
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any(
        "criterion without evidence and without claim_class" in c["evidence"]
        for c in checks
    )


def test_h06_evidence_bad_class_fails(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Rubric Evaluation": rubric_block(),
                "Evidence": (
                    "```toml\n[[evidence]]\nclass = \"hearsay\"\n"
                    'claim_id = "AC-01"\nref = "x"\n```'
                )
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any("bad class" in c["evidence"] for c in checks)


def test_h06_evidence_missing_ref_fails(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections(
            {
                "Rubric Evaluation": rubric_block(),
                "Evidence": (
                    "```toml\n[[evidence]]\nclass = \"observation\"\n"
                    'claim_id = "AC-01"\n```'
                )
            }
        ),
    )
    checks, decision = gate_validator.validate("H06", artifact)
    assert decision == "FAIL"
    assert any("missing ref" in c["evidence"] for c in checks)
