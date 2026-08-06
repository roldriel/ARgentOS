"""Tests for harness policy H15: delegation validity.

Covers the pre-delegation gate (V1 profile resolvability, V2 skill
resolvability, V3 budget coherence, V4 input artifact existence), the
post-return gate (V5 return report schema and failure classes), the
registration of the policy in the runner, and the H15 recovery decision
tree.

See `.agents/orchestrators/core/harness/policies/H15-delegation-validity.md`.
"""

from __future__ import annotations

import json
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

import delegation_validity
import runner_policies
from decision_tree_evaluator import evaluate_tree

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = PROJECT_ROOT / ".agents" / "harness" / "runner.py"
TREE_PATH = (
    PROJECT_ROOT
    / ".agents"
    / "orchestrators"
    / "core"
    / "harness"
    / "decision_trees"
    / "H15_FAIL.toml"
)

import tomllib


@pytest.fixture
def project(tmp_path):
    """A fake project root with a session artifact tree (no protocol files)."""
    session_uuid = f"test-{uuid.uuid4()}"
    iter_dir = tmp_path / ".project" / session_uuid / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "01-TASK_SPECIFICATION.md").write_text("# Spec\n", encoding="utf-8")
    return tmp_path, session_uuid


def _results_by_id(checks):
    return {c.id: c for c in checks}


# ---------------------------------------------------------------------------
# Valid cases
# ---------------------------------------------------------------------------


def test_valid_payload_without_optionals_passes(project):
    root, session_uuid = project
    payload = {
        "profile": None,
        "input_artifacts": [
            f".project/{session_uuid}/00/01-TASK_SPECIFICATION.md"
        ],
        "context_budget": 1000,
    }
    checks = delegation_validity.validate_delegation_payload(payload, root)
    assert checks, "expected checks"
    assert all(c.result == "PASS" for c in checks), [
        c.evidence for c in checks if c.result != "PASS"
    ]


def test_valid_payload_with_profile_and_skills_passes():
    payload = {
        "profile": "backend_engineer",
        "skills": ["planner", "ears-writer"],
        "input_artifacts": [],
        "context_budget": 1000,
    }
    checks = delegation_validity.validate_delegation_payload(payload)
    assert all(c.result == "PASS" for c in checks), [
        c.evidence for c in checks if c.result != "PASS"
    ]


def test_optional_fields_absent_pass():
    checks = delegation_validity.validate_delegation_payload({})
    assert all(c.result == "PASS" for c in checks)


# ---------------------------------------------------------------------------
# V1 — profile resolvability (F1)
# ---------------------------------------------------------------------------


def test_unresolvable_profile_fails():
    payload = {"profile": "nonexistent_profile"}
    checks = delegation_validity.validate_delegation_payload(payload)
    check = _results_by_id(checks)["v1_profile_resolvable"]
    assert check.result == "FAIL"
    assert "F1" in check.evidence


def test_every_catalog_profile_resolves():
    profiles_dir = PROJECT_ROOT / ".agents" / "roles" / "profiles"
    for profile_file in profiles_dir.glob("*.md"):
        if profile_file.name == "README.md":
            continue
        payload = {"profile": profile_file.stem}
        checks = delegation_validity.validate_delegation_payload(payload)
        check = _results_by_id(checks)["v1_profile_resolvable"]
        assert check.result == "PASS", f"catalog profile does not resolve: {profile_file.stem}"


# ---------------------------------------------------------------------------
# V2 — skill resolvability (F2, non-blocking)
# ---------------------------------------------------------------------------


def test_unresolvable_skill_fails_as_f2_deviation():
    payload = {"skills": ["nonexistent-skill"]}
    checks = delegation_validity.validate_delegation_payload(payload)
    check = _results_by_id(checks)["v2_skill_resolvable_nonexistent-skill"]
    assert check.result == "FAIL"
    assert "F2" in check.evidence


def test_project_level_skill_wins_on_collision(tmp_path):
    skill_dir = tmp_path / ".project" / "skills" / "planner"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: planner\ndescription: project override\n---\n", encoding="utf-8"
    )
    payload = {"skills": ["planner"]}
    checks = delegation_validity.validate_delegation_payload(payload, tmp_path)
    check = _results_by_id(checks)["v2_skill_resolvable_planner"]
    assert check.result == "PASS"
    assert ".project" in check.evidence


# ---------------------------------------------------------------------------
# V3 — budget coherence (F1)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_budget", [0, -5, "4000", float("inf"), float("nan"), True])
def test_incoherent_budget_fails(bad_budget):
    payload = {"context_budget": bad_budget}
    checks = delegation_validity.validate_delegation_payload(payload)
    check = _results_by_id(checks)["v3_budget_coherent"]
    assert check.result == "FAIL", f"budget {bad_budget!r} should be incoherent"
    assert "F1" in check.evidence


@pytest.mark.parametrize("good_budget", [1, 1000, 4000, 250.5])
def test_coherent_budget_passes(good_budget):
    payload = {"context_budget": good_budget}
    checks = delegation_validity.validate_delegation_payload(payload)
    check = _results_by_id(checks)["v3_budget_coherent"]
    assert check.result == "PASS"


# ---------------------------------------------------------------------------
# V4 — input artifact existence (F1)
# ---------------------------------------------------------------------------


def test_missing_input_artifact_fails(project):
    root, session_uuid = project
    payload = {
        "input_artifacts": [f".project/{session_uuid}/00/02-MISSING.md"]
    }
    checks = delegation_validity.validate_delegation_payload(payload, root)
    check = _results_by_id(checks)["v4_input_artifact_exists_02-MISSING.md"]
    assert check.result == "FAIL"
    assert "F1" in check.evidence


def test_artifact_outside_session_tree_fails(project):
    root, _ = project
    payload = {"input_artifacts": [".agents/roles/worker.md"]}
    checks = delegation_validity.validate_delegation_payload(payload, root)
    check = _results_by_id(checks)["v4_input_artifact_exists_worker.md"]
    assert check.result == "FAIL"


# ---------------------------------------------------------------------------
# V5 — return report validity (F1)
# ---------------------------------------------------------------------------


def _valid_report():
    return {
        "output_artifact": ".project/u/00/06-EXECUTION_SUMMARY.md",
        "role_executed": "worker",
        "phase_completed": "orchestrators/core/workflow/06-execute.md",
        "summary": "done",
        "blockers": [],
        "deviations": ["deviation: skill x not found"],
    }


def test_valid_return_report_passes():
    checks = delegation_validity.validate_return_report(_valid_report())
    assert all(c.result == "PASS" for c in checks), [
        c.evidence for c in checks if c.result != "PASS"
    ]


def test_return_report_missing_field_fails():
    report = _valid_report()
    del report["summary"]
    checks = delegation_validity.validate_return_report(report)
    check = _results_by_id(checks)["v5_field_present_summary"]
    assert check.result == "FAIL"
    assert "F1" in check.evidence


def test_deviation_without_class_prefix_fails():
    report = _valid_report()
    report["deviations"] = ["skill x not found"]
    checks = delegation_validity.validate_return_report(report)
    check = _results_by_id(checks)["v5_deviation_1_class_prefixed"]
    assert check.result == "FAIL"


def test_blocker_with_deviation_class_prefix_fails():
    report = _valid_report()
    report["blockers"] = ["ambiguity: unclear target"]
    checks = delegation_validity.validate_return_report(report)
    check = _results_by_id(checks)["v5_blocker_1_class_blocker"]
    assert check.result == "FAIL"


# ---------------------------------------------------------------------------
# Runner registration and decision tree
# ---------------------------------------------------------------------------


def test_policy_loads_via_runner():
    policy = runner_policies.load_policy("H15")
    assert policy["trigger"] == "H15"
    assert "H15-delegation-validity.md" in policy["_source"]


def test_runner_cli_accepts_h15(tmp_path):
    """H15 has no session artifact: the CLI loads the policy and passes."""
    session_uuid = f"test-{uuid.uuid4()}"
    artifacts_dir = tmp_path / ".project"
    (artifacts_dir / session_uuid).mkdir(parents=True)
    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER_PATH),
            "--session",
            session_uuid,
            "--trigger",
            "H15",
            "--artifacts-dir",
            str(artifacts_dir),
            "--no-report",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    output = json.loads(result.stdout)
    assert result.returncode == 0, output
    assert output["result"] == "PASS"
    assert output["transition"] == "pre-delegation and post-return delegation gate"


def _evaluate_h15(vars_):
    tree = tomllib.loads(TREE_PATH.read_text(encoding="utf-8"))
    return evaluate_tree(tree, {"trigger": "H15", "artifact_exists": True, **vars_})


def test_tree_invalid_payload_retries_then_recovers():
    result = _evaluate_h15({"profile_unresolvable": True, "retry_count": 0})
    assert result.result == "DECISION"
    assert result.action == "RETRY_WORKER"

    result = _evaluate_h15({"input_artifact_missing": True, "retry_count": 1})
    assert result.result == "DECISION"
    assert result.action == "RECOVERY_GENERIC"


def test_tree_invalid_return_report_retries_then_recovers():
    result = _evaluate_h15({"return_report_invalid": True, "retry_count": 0})
    assert result.result == "DECISION"
    assert result.action == "RETRY_WORKER"

    result = _evaluate_h15({"return_report_invalid": True, "retry_count": 1})
    assert result.result == "DECISION"
    assert result.action == "RECOVERY_GENERIC"


def test_tree_unknown_failure_falls_back_to_generic_recovery():
    result = _evaluate_h15({"retry_count": 0})
    assert result.result == "DECISION"
    assert result.action == "RECOVERY_GENERIC"
