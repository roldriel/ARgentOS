"""Tests for tools/check_session_artifacts.py (dev-only, no payload dependency)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_session_artifacts as csa  # noqa: E402


def test_no_project_dir_is_ok(tmp_path):
    assert csa.scan(tmp_path) == []


def test_valid_artifacts_pass(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": [{"id": "c", "result": "PASS", "evidence": "e"}]} -->\n',
        encoding="utf-8",
    )
    (tmp_path / ".project" / "uuid" / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "t", "type": "delegation", "phase": "06", '
        '"profile": null, "skills": [], "h15": "PASS"} -->\n',
        encoding="utf-8",
    )
    state = {
        "session": "uuid",
        "iteration": "00",
        "task_profile": "standard",
        "gates": {"H04": {"result": "PASS", "timestamp": "t"}},
        "last_gate": "H04",
        "status": "in_progress",
        "updated": "t",
    }
    (session / "state.json").write_text(json.dumps(state), encoding="utf-8")
    assert csa.scan(tmp_path) == []


def test_invalid_artifacts_flagged(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md").write_text(
        "<!-- ENTRY: {not json -->\n", encoding="utf-8"
    )
    (tmp_path / ".project" / "uuid" / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "t", "type": "delegation"} -->\n'
        '<!-- METRIC: {"timestamp": "t", "type": "unknown_type"} -->\n',
        encoding="utf-8",
    )
    (session / "state.json").write_text('{"gates": {}}', encoding="utf-8")
    v = csa.scan(tmp_path)
    assert any("invalid JSON" in x for x in v)
    assert any("unknown type" in x for x in v)
    assert any("missing fields" in x and "METRIC" in x and "delegation" in x for x in v)
    assert any("missing fields" in x and "STATE" in x for x in v)


def test_budget_accounting_flagged(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "t", "type": "context_budget", '
        '"phase": "06", "declared": 100, "consumed": 150} -->\n'
        '<!-- METRIC: {"timestamp": "t", "type": "context_budget", '
        '"phase": "05", "declared": -5, "consumed": 0} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("exceeds declared" in x for x in v)
    assert any("must be a finite positive number" in x for x in v)


def test_valid_deviation_passes(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": [{"id": "c", "result": "PASS", "evidence": "e"}], '
        '"deviation": {"cause": "trivial profile", "evidence": "01-TASK_ANALYSIS.md"}} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_malformed_deviation_flagged(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": [], "deviation": {"cause": ""}} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("deviation.cause must be a non-empty string" in x for x in v)
    assert any("deviation.evidence must be a non-empty string" in x for x in v)


def test_valid_recovery_passes(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H00", "transition": "A -> B", '
        '"result": "FAIL", "checks": [], '
        '"recovery": {"variables": {"artifact_exists": false, "retry_count": 0}, '
        '"matched_rule": "RETRY_WORKER", "target_phase": "00-analyze-task.md"}} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_malformed_recovery_flagged(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H00", "transition": "A -> B", '
        '"result": "FAIL", "checks": [], '
        '"recovery": {"matched_rule": "", "variables": []}} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("recovery.matched_rule must be a non-empty string" in x for x in v)
    assert any("recovery.variables must be an object" in x for x in v)


def _session_log(version: str = "4.0.0") -> str:
    return (
        "# Session Log\n\n"
        "- Session UUID: uuid\n"
        "- Created: 2026-08-25T10:00:00Z\n"
        f"- Protocol version: {version}\n"
    )


def _write_session(tmp_path, version: str | None = "4.0.0"):
    """Write a minimal 4.x-style session with all root records."""
    session = tmp_path / ".project" / "uuid"
    (session / "00").mkdir(parents=True)
    if version is not None:
        (session / "SESSION_LOG.md").write_text(_session_log(version), encoding="utf-8")
    entry = {
        "timestamp": "2026-08-25T10:05:00Z",
        "clock": "utc",
        "trigger": "H04",
        "transition": "PLANNING -> PLAN_READY",
        "result": "PASS",
        "checks": [
            {"id": "c", "result": "PASS", "evidence": "05-EXECUTION_PLAN.md"}
        ],
    }
    if (
        version is not None
        and csa._parse_version(version) >= csa.EVIDENCE_PROTOCOL
    ):
        entry["evidence"] = [
            {
                "class": "reference",
                "claim_id": "c",
                "ref": "05-EXECUTION_PLAN.md",
            }
        ]
    (session / "HARNESS_REPORT.md").write_text(
        f"<!-- ENTRY: {json.dumps(entry)} -->\n", encoding="utf-8"
    )
    metric = (
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00Z", "clock": "utc", '
        '"type": "session_start", "declarative_flags": [], '
        '"protocol_version": "' + (version or "3.26.0") + '"} -->\n'
    )
    (session / "METRICS.md").write_text(metric, encoding="utf-8")
    state = {
        "session": "uuid",
        "iteration": "00",
        "task_profile": "standard",
        "gates": {"H04": {"result": "PASS", "timestamp": "2026-08-25T10:05:00Z"}},
        "last_gate": "H04",
        "status": "in_progress",
        "updated": "2026-08-25T10:05:00Z",
    }
    (session / "00" / "state.json").write_text(
        json.dumps(state), encoding="utf-8"
    )
    return session


def test_new_protocol_session_passes(tmp_path):
    _write_session(tmp_path)
    assert csa.scan(tmp_path) == []


def test_new_protocol_session_missing_records_flagged(tmp_path):
    session = tmp_path / ".project" / "uuid"
    (session / "00").mkdir(parents=True)
    (session / "SESSION_LOG.md").write_text(_session_log(), encoding="utf-8")
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    v = csa.scan(tmp_path)
    assert any("missing root record HARNESS_REPORT.md" in x for x in v)
    assert any("missing root record METRICS.md" in x for x in v)


def test_unmarked_attestation_flagged(tmp_path):
    session = _write_session(tmp_path)
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00Z", "trigger": "H04", '
        '"transition": "PLANNING -> PLAN_READY", "result": "PASS", '
        '"checks": [{"id": "c", "result": "PASS"}]} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("unmarked attestation" in x for x in v)


def test_verified_requires_evidence_flagged(tmp_path):
    session = _write_session(tmp_path)
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00Z", "trigger": "H04", '
        '"transition": "PLANNING -> PLAN_READY", "result": "PASS", '
        '"checks": [{"id": "c", "result": "PASS", "claim_class": "verified"}]} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("claim_class 'verified' without evidence" in x for x in v)


def test_attested_check_without_evidence_passes(tmp_path):
    session = _write_session(tmp_path)
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00Z", "trigger": "H04", '
        '"transition": "PLANNING -> PLAN_READY", "result": "PASS", '
        '"checks": [{"id": "c", "result": "PASS", "claim_class": "attested"}]} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_legacy_session_not_flagged(tmp_path):
    _write_session(tmp_path, version="3.26.0")
    session = tmp_path / ".project" / "uuid"
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H04", '
        '"transition": "A -> B", "result": "PASS", '
        '"checks": [{"id": "c", "result": "PASS"}]} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert all("unmarked attestation" not in x for x in v)
    assert all("missing root record" not in x for x in v)


def test_agent_clock_timestamp_allowed(tmp_path):
    session = _write_session(tmp_path)
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00-03:00", '
        '"clock": "agent_clock", "type": "session_start", '
        '"declarative_flags": [], "protocol_version": "4.0.0"} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_non_utc_timestamp_flagged(tmp_path):
    session = _write_session(tmp_path)
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00-03:00", '
        '"trigger": "H04", "transition": "A -> B", "result": "PASS", '
        '"checks": [{"id": "c", "result": "PASS", "evidence": "e"}]} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("utc timestamps must end with 'Z'" in x for x in v)


def test_bad_clock_value_flagged(tmp_path):
    session = _write_session(tmp_path)
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00Z", "clock": "local", '
        '"type": "session_start", "declarative_flags": [], '
        '"protocol_version": "4.0.0"} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("bad clock 'local'" in x for x in v)


def test_lifecycle_manual_status_flagged(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    (session / "00" / "00-TASK_ANALYSIS.md").write_text(
        "# Analysis\n\n## Metadata\n\n```toml\nid = \"x\"\ncreated_at = \"t\"\n"
        'status = ""\n```\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("ARTIFACT" in x and "manual lifecycle field" in x for x in v)


def test_lifecycle_state_section_flagged(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    (session / "00" / "03-CONTEXT_ARTIFACT.md").write_text(
        "# Artifact\n\n## State\n\n```toml\nstate = \"\"\n```\n",
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("ARTIFACT" in x and "`## State` section" in x for x in v)


def test_lifecycle_clean_artifacts_pass(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    (session / "00" / "00-TASK_ANALYSIS.md").write_text(
        "# Analysis\n\n## Metadata\n\n```toml\nid = \"x\"\ncreated_at = \"t\"\n```\n",
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_legacy_session_manual_status_not_flagged(tmp_path):
    session = _write_session(tmp_path, version="3.26.0")
    (session / "00" / "00-TASK_ANALYSIS.md").write_text(
        "# Analysis\n\n## Metadata\n\n```toml\nid = \"x\"\ncreated_at = \"t\"\n"
        'status = ""\n```\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert all("manual lifecycle" not in x for x in v)


def test_completed_without_in_scope_gates_flagged(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    state = {
        "session": "uuid",
        "iteration": "00",
        "task_profile": "standard",
        "gates": {"H04": {"result": "PASS", "timestamp": "2026-08-25T10:05:00Z"}},
        "last_gate": "H04",
        "status": "COMPLETED",
        "updated": "2026-08-25T10:05:00Z",
    }
    (session / "00" / "state.json").write_text(json.dumps(state), encoding="utf-8")
    v = csa.scan(tmp_path)
    assert any("COMPLETED without in-scope gate PASS" in x for x in v)


def test_completed_with_all_gates_passes(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    gates = {
        h: {"result": "PASS", "timestamp": "2026-08-25T10:05:00Z"}
        for h in ("H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07")
    }
    state = {
        "session": "uuid",
        "iteration": "00",
        "task_profile": "standard",
        "gates": gates,
        "last_gate": "H07",
        "status": "COMPLETED",
        "updated": "2026-08-25T10:05:00Z",
    }
    (session / "00" / "state.json").write_text(json.dumps(state), encoding="utf-8")
    assert csa.scan(tmp_path) == []


def test_complex_completed_without_review_gate_flagged(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    gates = {
        h: {"result": "PASS", "timestamp": "2026-08-25T10:05:00Z"}
        for h in ("H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07")
    }
    state = {
        "session": "uuid",
        "iteration": "00",
        "task_profile": "complex",
        "gates": gates,
        "last_gate": "H07",
        "status": "COMPLETED",
        "updated": "2026-08-25T10:05:00Z",
    }
    (session / "00" / "state.json").write_text(json.dumps(state), encoding="utf-8")
    v = csa.scan(tmp_path)
    assert any("REVIEW gate PASS" in x for x in v)


def test_complex_completed_with_review_gate_passes(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    gates = {
        h: {"result": "PASS", "timestamp": "2026-08-25T10:05:00Z"}
        for h in ("H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07")
    }
    state = {
        "session": "uuid",
        "iteration": "00",
        "task_profile": "complex",
        "gates": gates,
        "last_gate": "H07",
        "status": "COMPLETED",
        "updated": "2026-08-25T10:05:00Z",
    }
    (session / "00" / "state.json").write_text(json.dumps(state), encoding="utf-8")
    (session / "HARNESS_REPORT.md").write_text(
        (session / "HARNESS_REPORT.md").read_text(encoding="utf-8")
        + '<!-- ENTRY: {"timestamp": "2026-08-25T10:06:00Z", "clock": "utc", '
        '"trigger": "REVIEW", "transition": "VERIFYING -> COMPLETED", '
        '"result": "PASS", "checks": [{"id": "c", "result": "PASS", '
        '"evidence": "07-REVIEW_REPORT.md"}]} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_deferred_items_without_confirmation_flagged(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    (session / "00" / "07-VERIFICATION_REPORT.md").write_text(
        "# Report\n\n## Deferred Items\n\n```toml\n"
        '[[deferred_items]]\nitem = "sign-off"\ndeferred = false\n```\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("REPORT" in x and "`deferred = true`" in x for x in v)
    assert any("REPORT" in x and "`confirmed_by`" in x for x in v)


def test_deferred_items_with_confirmation_passes(tmp_path):
    session = _write_session(tmp_path, version="5.0.0")
    (session / "00" / "07-VERIFICATION_REPORT.md").write_text(
        "# Report\n\n## Deferred Items\n\n```toml\n"
        '[[deferred_items]]\nitem = "sign-off"\ndeferred = true\n'
        'confirmed_by = "user"\nconfirmation_date = "2026-08-25"\n```\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_evidence_protocol_session_passes(tmp_path):
    _write_session(tmp_path, version="7.0.0")
    assert csa.scan(tmp_path) == []


def test_evidence_entry_bad_class_flagged(tmp_path):
    session = _write_session(tmp_path, version="7.0.0")
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00Z", "clock": "utc", '
        '"trigger": "H04", "transition": "PLANNING -> PLAN_READY", '
        '"result": "PASS", "checks": [{"id": "c", "result": "PASS", '
        '"claim_class": "verified"}], '
        '"evidence": [{"class": "hearsay", "claim_id": "c", "ref": "x"}]} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("bad class 'hearsay'" in x for x in v)


def test_verified_without_non_attestation_evidence_flagged(tmp_path):
    session = _write_session(tmp_path, version="7.0.0")
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00Z", "clock": "utc", '
        '"trigger": "H04", "transition": "PLANNING -> PLAN_READY", '
        '"result": "PASS", "checks": [{"id": "c", "result": "PASS", '
        '"claim_class": "verified"}], '
        '"evidence": [{"class": "attestation", "claim_id": "c", "ref": "-", '
        '"actor": "executor", "statement": "did it"}]} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("without non-attestation evidence" in x for x in v)


def test_attested_with_marked_attestation_passes(tmp_path):
    session = _write_session(tmp_path, version="7.0.0")
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00Z", "clock": "utc", '
        '"trigger": "H04", "transition": "PLANNING -> PLAN_READY", '
        '"result": "PASS", "checks": [{"id": "c", "result": "PASS", '
        '"claim_class": "attested"}], '
        '"evidence": [{"class": "attestation", "claim_id": "c", "ref": "-", '
        '"actor": "executor", "statement": "did it"}]} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_verification_report_verified_without_evidence_flagged(tmp_path):
    session = _write_session(tmp_path, version="7.0.0")
    (session / "00" / "07-VERIFICATION_REPORT.md").write_text(
        "# Report\n\n"
        "## Acceptance Criteria Evaluation\n\n```toml\n"
        '[[acceptance_criteria]]\nclaim_id = "AC-01"\ncriterion = "c"\n'
        'result = "PASS"\nclaim_class = "verified"\n```\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any(
        "REPORT" in x and "without non-attestation evidence" in x for x in v
    )


def test_verification_report_measurement_evidence_passes(tmp_path):
    session = _write_session(tmp_path, version="7.0.0")
    (session / "00" / "07-VERIFICATION_REPORT.md").write_text(
        "# Report\n\n"
        "## Acceptance Criteria Evaluation\n\n```toml\n"
        '[[acceptance_criteria]]\nclaim_id = "AC-01"\ncriterion = "c"\n'
        'result = "PASS"\nclaim_class = "verified"\n```\n\n'
        "## Evidence\n\n```toml\n"
        '[[evidence]]\nclass = "measurement"\nclaim_id = "AC-01"\n'
        'ref = "results.log"\ncommand = "pytest -q"\nexit_code = 0\n```\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []
