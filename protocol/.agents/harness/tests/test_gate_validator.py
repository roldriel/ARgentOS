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
            "```toml\n[[acceptance_criteria]]\ncriterion = \"c\"\nresult = \"PASS\"\n```"
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
