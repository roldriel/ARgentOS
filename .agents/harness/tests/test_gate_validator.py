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


def adopted_session(tmp_path: Path) -> Path:
    """Create an iteration folder of a fresh session in the adopted layout."""
    session = tmp_path / ".argentos" / ".project" / f"test-{uuid.uuid4()}" / "00"
    session.mkdir(parents=True)
    return session


def validate(trigger: str, artifact: Path, *args, **kwargs):
    """Validate an artifact of the adopted layout, injecting PROJECT_ROOT.

    Production callers pass ``--project-root`` (the entry point provides it);
    the tests derive it from the artifact's ``.argentos`` ancestor.
    """
    for parent in artifact.resolve().parents:
        if parent.name == ".argentos":
            kwargs.setdefault("project_root", parent.parent)
            break
    return gate_validator.validate(trigger, artifact, *args, **kwargs)


def make_artifact(tmp_path: Path, artifact_name: str, sections: dict[str, str]) -> Path:
    """Build a fake adoption layout and an artifact with the given sections."""
    session = adopted_session(tmp_path)
    parts = ["# Artifact"]
    for heading, body in sections.items():
        parts.append(f"## {heading}")
        parts.append(body)
    artifact = session / artifact_name
    artifact.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    return artifact


def set_rubrics(tmp_path: Path, enabled: bool) -> None:
    (tmp_path / ".argentos").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".argentos" / "features.toml").write_text(
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
    checks, decision = validate("H01", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_missing_section_fails(tmp_path):
    artifact = make_artifact(tmp_path, "TASK_SPECIFICATION.md", {
        "Objective": "Build X.",
        "Acceptance Criteria": "- The API shall return HTTP 200.",
    })
    checks, decision = validate("H01", artifact)
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
    checks, decision = validate("H01", artifact)
    assert decision == "FAIL"
    assert any(c["id"] == "ears" for c in checks)


def h01_sections(extra: dict | None = None) -> dict:
    """Build a minimal valid H01 section set."""
    sections = {
        "Objective": "Build X.",
        "Expected Outcome": "X works.",
        "Scope": "Only X.",
        "Constraints": "None.",
        "Acceptance Criteria": "- The API shall return HTTP 200.",
        "Assumptions": "- none",
        "Unknowns": "- none",
        "Validation": "- pending",
    }
    if extra:
        sections.update(extra)
    return sections


def effects_toml(entries: str) -> str:
    return "```toml\n" + entries + "```"


def test_h01_valid_effects_passes(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "TASK_SPECIFICATION.md",
        h01_sections(
            {
                "Effects": effects_toml(
                    '[[effects]]\nname = "fetch_remote_sources"\n'
                    'kind = "network"\nauthorized_by = "user"\n'
                    'evidence_ref = "SESSION_BRIEF.md clarification 5A"\n'
                    'status = "authorized"\n'
                )
            }
        ),
    )
    checks, decision = validate("H01", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "effects" and c["result"] == "PASS" for c in checks)


def test_h01_effects_missing_authorized_by_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "TASK_SPECIFICATION.md",
        h01_sections(
            {
                "Effects": effects_toml(
                    '[[effects]]\nname = "fetch"\nkind = "network"\n'
                    'evidence_ref = "x"\nstatus = "authorized"\n'
                )
            }
        ),
    )
    checks, decision = validate("H01", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "effects" and "bad authorized_by" in c["evidence"]
        for c in checks
    )


def test_h01_effects_bad_kind_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "TASK_SPECIFICATION.md",
        h01_sections(
            {
                "Effects": effects_toml(
                    '[[effects]]\nname = "fetch"\nkind = "ssh"\n'
                    'authorized_by = "user"\nevidence_ref = "x"\n'
                    'status = "authorized"\n'
                )
            }
        ),
    )
    checks, decision = validate("H01", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "effects" and "bad kind 'ssh'" in c["evidence"]
        for c in checks
    )


def test_h01_effects_missing_section_skips(tmp_path):
    artifact = make_artifact(tmp_path, "TASK_SPECIFICATION.md", h01_sections())
    checks, decision = validate("H01", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "effects" and c["result"] == "SKIP" for c in checks)


def test_h05_bad_final_state_fails(tmp_path):
    artifact = make_artifact(tmp_path, "EXECUTION_SUMMARY.md", {
        "Final Project State": "```toml\n[final_state]\nstatus = \"BROKEN\"\n```",
        "Steps Executed": "```toml\n[[steps_executed]]\norder = 1\naction = \"a\"\nstatus = \"COMPLETED\"\n```",
    })
    checks, decision = validate("H05", artifact)
    assert decision == "FAIL"
    assert any("bad status" in c["evidence"] for c in checks)


def h05_sections(extra: dict | None = None) -> dict:
    """Build a minimal valid H05 section set."""
    sections = {
        "Metadata": "- x",
        "Task Reference": "- spec",
        "Execution Plan Reference": "- plan",
        "Summary of Changes": "- changed",
        "Steps Executed": (
            "```toml\n[[steps_executed]]\norder = 1\naction = \"a\"\n"
            'status = "COMPLETED"\n```'
        ),
        "Project Files Modified": "- none",
        "Intermediate Validations": "- none",
        "Issues or Deviations": "- none",
        "Final Project State": (
            '```toml\n[final_state]\nstatus = "VERIFIABLE"\n```'
        ),
        "Confidence": "- high",
    }
    if extra:
        sections.update(extra)
    return sections


def test_h05_invalidated_facts_valid_passes(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "EXECUTION_SUMMARY.md",
        h05_sections(
            {
                "Invalidated Facts": (
                    "```toml\n[[invalidated_facts]]\n"
                    'fact = "stack is Django"\n'
                    'entry = ".project/knowledge/discovery/stack.md"\n'
                    'reason = "migrated to FastAPI"\n```'
                )
            }
        ),
    )
    checks, decision = validate("H05", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(
        c["id"] == "invalidated_facts" and c["result"] == "PASS"
        for c in checks
    )


def test_h05_invalidated_facts_missing_reason_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "EXECUTION_SUMMARY.md",
        h05_sections(
            {
                "Invalidated Facts": (
                    "```toml\n[[invalidated_facts]]\n"
                    'fact = "stack is Django"\n'
                    'entry = ".project/knowledge/discovery/stack.md"\n'
                    'reason = ""\n```'
                )
            }
        ),
    )
    checks, decision = validate("H05", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "invalidated_facts" and "missing reason" in c["evidence"]
        for c in checks
    )


def test_h05_without_invalidated_facts_skips(tmp_path):
    artifact = make_artifact(
        tmp_path, "EXECUTION_SUMMARY.md", h05_sections()
    )
    checks, decision = validate("H05", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(
        c["id"] == "invalidated_facts" and c["result"] == "SKIP"
        for c in checks
    )


def h10_sections(extra: dict | None = None) -> dict:
    """Build a minimal valid H10 section set."""
    sections = {
        "Discovery Objective": "- find relevant knowledge",
        "Recommended Entries": "- none",
        "Context Budget Recommendation": "- 4000",
        "Notes": "- none",
    }
    if extra:
        sections.update(extra)
    return sections


def recommendation_json(body: str) -> str:
    return "```json\n" + body + "\n```"


def test_h10_valid_recommendation_passes(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "KB_RECOMMENDATION.md",
        h10_sections(
            {
                "Recommended Entries": recommendation_json(
                    '{"discovery_objective": "x", "recommended_entries": ['
                    '{"session_uuid": "s", "kind": "discovery", '
                    '"path": ".project/knowledge/discovery/environment.md", '
                    '"priority": 1, "confidence": "HIGH"}]}'
                )
            }
        ),
    )
    checks, decision = validate("H10", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(
        c["id"] == "recommendation" and c["result"] == "PASS"
        for c in checks
    )


def test_h10_recommendation_bad_kind_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "KB_RECOMMENDATION.md",
        h10_sections(
            {
                "Recommended Entries": recommendation_json(
                    '{"recommended_entries": [{"kind": "snapshot", '
                    '"path": "x"}]}'
                )
            }
        ),
    )
    checks, decision = validate("H10", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "recommendation" and "bad kind" in c["evidence"]
        for c in checks
    )


def test_h10_recommendation_missing_path_fails(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "KB_RECOMMENDATION.md",
        h10_sections(
            {
                "Recommended Entries": recommendation_json(
                    '{"recommended_entries": [{"kind": "lesson", '
                    '"path": ""}]}'
                )
            }
        ),
    )
    checks, decision = validate("H10", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "recommendation" and "missing path" in c["evidence"]
        for c in checks
    )


def test_h10_without_json_skips(tmp_path):
    artifact = make_artifact(
        tmp_path, "KB_RECOMMENDATION.md", h10_sections()
    )
    checks, decision = validate("H10", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(
        c["id"] == "recommendation" and c["result"] == "SKIP"
        for c in checks
    )


def test_h06_bad_decision_fails(tmp_path):
    set_rubrics(tmp_path, False)
    artifact = make_artifact(
        tmp_path, "VERIFICATION_REPORT.md",
        h06_sections({"Final Decision": "```toml\n[decision]\nresult = \"DONE\"\n```"}),
    )
    checks, decision = validate("H06", artifact)
    assert decision == "FAIL"
    assert any("bad decision.result" in c["evidence"] for c in checks)


def test_h07_branch_incoherence_fails(tmp_path):
    artifact = make_artifact(tmp_path, "VERIFICATION_REPORT.md", {
        "Scope Compliance": "```toml\n[scope_compliance]\nscope_respected = true\nunplanned_changes = [\"x\"]\nuser_authorized_extra_work = false\n```",
    })
    checks, decision = validate("H07", artifact)
    assert decision == "FAIL"
    assert any("Branch A/B incoherent" in c["evidence"] for c in checks)


def test_broken_citation_fails(tmp_path):
    artifact = make_artifact(tmp_path, "TASK_SPECIFICATION.md", {
        "Objective": "Build X.",
        "Validation": "See `missing-file.md` §Nowhere.",
    })
    checks, decision = validate("H01", artifact)
    assert decision == "FAIL"
    assert any("broken citation" in c["evidence"] for c in checks)


def test_valid_citation_resolves(tmp_path):
    session = adopted_session(tmp_path)
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
    checks, decision = validate("H01", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_citations_anchor_to_the_three_roots(tmp_path):
    """Test D — `.agents`/`.project` anchor to ARGENTOS_ROOT, files to PROJECT_ROOT."""
    session = adopted_session(tmp_path)
    standard = tmp_path / ".argentos" / ".agents" / "standards" / "X.md"
    standard.parent.mkdir(parents=True, exist_ok=True)
    standard.write_text("# Section\n\ncontent\n", encoding="utf-8")
    (session / "notes.md").write_text("# Notes\n\ncontent\n", encoding="utf-8")
    (tmp_path / "src").mkdir(exist_ok=True)
    (tmp_path / "src" / "app.py").write_text("x = 1\n", encoding="utf-8")

    sections = {
        "Objective": "Build X.",
        "Expected Outcome": "X works.",
        "Scope": "X.",
        "Constraints": "None.",
        "Acceptance Criteria": "- The API shall return HTTP 200.",
        "Assumptions": "- none",
        "Unknowns": "- none",
        "Validation": (
            "```toml\n"
            "[refs]\n"
            'specification = ".agents/standards/X.md"\n'
            f'execution_plan = ".project/{session.parent.name}/00/notes.md"\n'
            'artifact = "src/app.py"\n'
            "```"
        ),
    }
    parts = ["# Artifact"]
    for heading, body in sections.items():
        parts.append(f"## {heading}")
        parts.append(body)
    artifact = session / "TASK_SPECIFICATION.md"
    artifact.write_text("\n\n".join(parts) + "\n", encoding="utf-8")

    checks, decision = validate("H01", artifact)

    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(
        c["id"] == "citations" and c["result"] == "PASS" for c in checks
    )


def test_features_reads_argentos_root_only(tmp_path):
    """Test E — the active configuration is ARGENTOS_ROOT/features.toml."""
    (tmp_path / ".argentos").mkdir()
    (tmp_path / ".argentos" / "features.toml").write_text(
        "rubrics = false\n", encoding="utf-8"
    )
    payload = tmp_path / ".argentos" / ".agents"
    payload.mkdir()
    (payload / "features.toml").write_text("rubrics = true\n", encoding="utf-8")

    assert gate_validator.features(tmp_path / ".argentos") == {"rubrics": False}


def test_h06_rubrics_follow_the_argentos_root_configuration(tmp_path):
    """Test E — no silent fallback to the payload's features.toml."""
    set_rubrics(tmp_path, False)
    payload = tmp_path / ".argentos" / ".agents"
    payload.mkdir(parents=True, exist_ok=True)
    (payload / "features.toml").write_text("rubrics = true\n", encoding="utf-8")
    artifact = make_artifact(tmp_path, "VERIFICATION_REPORT.md", h06_sections())

    checks, decision = validate("H06", artifact)

    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(
        c["id"] == "rubrics" and c["result"] == "SKIP" for c in checks
    )


def test_rubrics_missing_fails(tmp_path):
    set_rubrics(tmp_path, True)
    artifact = make_artifact(tmp_path, "VERIFICATION_REPORT.md", h06_sections())
    checks, decision = validate("H06", artifact)
    assert decision == "FAIL"
    assert any("missing ## Rubric Evaluation" in c["evidence"] for c in checks)


def test_rubrics_valid_passes(tmp_path):
    set_rubrics(tmp_path, True)
    artifact = make_artifact(
        tmp_path, "VERIFICATION_REPORT.md",
        h06_sections({"Rubric Evaluation": rubric_block()}),
    )
    checks, decision = validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_unsupported_trigger_raises(tmp_path):
    artifact = make_artifact(tmp_path, "X.md", {"Objective": "x"})
    with pytest.raises(ValueError):
        validate("Z99", artifact)


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
        [
            sys.executable,
            str(VALIDATOR),
            "--project-root",
            str(tmp_path),
            "--trigger",
            "H01",
            "--artifact",
            str(ok),
        ],
        capture_output=True,
        text=True,
        cwd=str(HARNESS),
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["decision"] == "PASS"


def make_h04_plan(tmp_path: Path, profile: str, with_context_reference: bool) -> Path:
    """Build an EXECUTION_PLAN for the given task profile in a fake session."""
    session = adopted_session(tmp_path)
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
    checks, decision = validate("H04", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "profile" and c["result"] == "PASS" for c in checks)


def test_h04_standard_requires_context_reference(tmp_path):
    artifact = make_h04_plan(tmp_path, "standard", with_context_reference=False)
    checks, decision = validate("H04", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "section" and "Context Reference" in c["evidence"]
        for c in checks
    )


def test_h04_trivial_with_context_reference_passes(tmp_path):
    artifact = make_h04_plan(tmp_path, "trivial", with_context_reference=True)
    checks, decision = validate("H04", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_h04_plan_with_effects_section_fails(tmp_path):
    artifact = make_h04_plan(tmp_path, "standard", with_context_reference=True)
    artifact.write_text(
        artifact.read_text(encoding="utf-8")
        + "\n## Effects\n\n```toml\n[[effects]]\nname = \"x\"\n```\n",
        encoding="utf-8",
    )
    checks, decision = validate("H04", artifact)
    assert decision == "FAIL"
    assert any(
        c["id"] == "effects"
        and "must not declare an Effects section" in c["evidence"]
        for c in checks
    )


def make_h06_report(
    tmp_path: Path,
    test_results_toml: str,
    session_log: str | None = None,
    evidence: str | None = None,
    evidence_toml: str | None = None,
) -> Path:
    """Build a VERIFICATION_REPORT with a test_results TOML block."""
    session = adopted_session(tmp_path)
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
    checks, decision = validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "test_results" and c["result"] == "PASS" for c in checks)


def test_h06_test_results_session_log_fallback_passes(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\nclaim_id = \"TR-01\"\ntest = \"pytest -q\"\n"
        'result = "PASS"\ndetails = ""\nclaim_class = "attested"\n```',
        session_log="ran: pytest -q\n",
    )
    checks, decision = validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]


def test_h06_test_results_missing_evidence_fails(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\ntest = \"pytest -q\"\nresult = \"PASS\"\n"
        'details = ""\n```',
    )
    checks, decision = validate("H06", artifact)
    assert decision == "FAIL"
    assert any("test command not found in SESSION_LOG.md" in c["evidence"] for c in checks)


def test_h06_test_results_unresolved_evidence_fails(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\ntest = \"pytest -q\"\nresult = \"PASS\"\n"
        'details = ""\nevidence = "missing.log"\n```',
    )
    checks, decision = validate("H06", artifact)
    assert decision == "FAIL"
    assert any("evidence does not resolve" in c["evidence"] for c in checks)


def test_h06_test_results_skipped_exempt(tmp_path):
    artifact = make_h06_report(
        tmp_path,
        "```toml\n[[test_results]]\ntest = \"pytest -q\"\nresult = \"SKIPPED\"\n"
        'details = ""\n```',
    )
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H00", artifact)
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
    checks, decision = validate("H00", artifact)
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
    checks, decision = validate("H00", artifact)
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
    checks, decision = validate("H03", artifact)
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
    checks, decision = validate("H03", artifact)
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
    checks, decision = validate("H03", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
    assert decision == "PASS", [c for c in checks if c["result"] == "FAIL"]
    assert any(c["id"] == "review_report" and c["result"] == "PASS" for c in checks)


def test_h06_standard_review_report_skips(tmp_path):
    artifact = make_artifact(
        tmp_path,
        "VERIFICATION_REPORT.md",
        h06_sections({"Rubric Evaluation": rubric_block()}),
    )
    set_task_profile(artifact, "standard")
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
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
    checks, decision = validate("H06", artifact)
    assert decision == "FAIL"
    assert any("missing ref" in c["evidence"] for c in checks)
