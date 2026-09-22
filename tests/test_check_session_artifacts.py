"""Tests for tools/check_session_artifacts.py (dev-only, no payload dependency)."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

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


def test_reuse_and_provider_cache_events_pass(tmp_path):
    _write_session(tmp_path)
    session = tmp_path / ".project" / "uuid"
    (session / "METRICS.md").write_text(
        (session / "METRICS.md").read_text(encoding="utf-8")
        + '<!-- METRIC: {"timestamp": "2026-08-31T10:00:00Z", "clock": "utc", '
        '"type": "reuse_event", "layer": "knowledge", "operation": "eligibility", '
        '"eligibility_decision": "REJECTED", "reason": "availability"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:01Z", "clock": "utc", '
        '"type": "provider_cache_event", "result": "unavailable"} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_reuse_event_missing_required_flagged(tmp_path):
    _write_session(tmp_path)
    session = tmp_path / ".project" / "uuid"
    (session / "METRICS.md").write_text(
        (session / "METRICS.md").read_text(encoding="utf-8")
        + '<!-- METRIC: {"timestamp": "2026-08-31T10:00:00Z", "clock": "utc", '
        '"type": "reuse_event", "operation": "lookup"} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any(
        "METRIC" in x and "missing fields" in x and "layer" in x for x in v
    )


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
    parsed_version = csa._parse_version(version) if version is not None else None
    if (
        parsed_version is not None
        and parsed_version >= csa.EVIDENCE_PROTOCOL
    ):
        entry["evidence"] = [
            {
                "class": "reference",
                "claim_id": "c",
                "ref": "05-EXECUTION_PLAN.md",
            }
        ]
    if parsed_version is not None and parsed_version >= csa.RECORD_PROTOCOL:
        entry["iteration"] = "00"
    (session / "HARNESS_REPORT.md").write_text(
        f"<!-- ENTRY: {json.dumps(entry)} -->\n", encoding="utf-8"
    )
    metric_data = {
        "timestamp": "2026-08-25T10:01:00Z",
        "clock": "utc",
        "type": "session_start",
        "declarative_flags": [],
        "protocol_version": version or "3.26.0",
    }
    if parsed_version is not None and parsed_version >= csa.RECORD_PROTOCOL:
        metric_data["seq"] = 1
    metric = f"<!-- METRIC: {json.dumps(metric_data)} -->\n"
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


def _authorization_spec(entries: str) -> str:
    return (
        "# Spec\n\n## Effects\n\n```toml\n" + entries + "```\n"
    )


def _authorization_summary(entries: str) -> str:
    return (
        "# Summary\n\n## Effects Executed\n\n```toml\n" + entries + "```\n"
    )


def test_authorization_protocol_session_passes(tmp_path):
    _write_session(tmp_path, version="8.0.0")
    assert csa.scan(tmp_path) == []


def test_effects_executed_undetermined_flagged(tmp_path):
    session = _write_session(tmp_path, version="8.0.0")
    (session / "00" / "02-TASK_SPECIFICATION.md").write_text(
        _authorization_spec(
            '[[effects]]\nname = "fetch"\nkind = "network"\n'
            'authorized_by = "user"\nevidence_ref = "SESSION_BRIEF.md"\n'
            'status = "authorized"\n'
        ),
        encoding="utf-8",
    )
    (session / "00" / "06-EXECUTION_SUMMARY.md").write_text(
        _authorization_summary(
            '[[effects_executed]]\neffect = "clone"\nexecuted = true\n'
            'authorization_ref = "SESSION_BRIEF.md"\n'
        ),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("AUTHORIZATION_UNDETERMINED" in x for x in v)
    assert all("UNAUTHORIZED)" not in x for x in v)


def test_effects_executed_unauthorized_flagged(tmp_path):
    session = _write_session(tmp_path, version="8.0.0")
    (session / "00" / "02-TASK_SPECIFICATION.md").write_text(
        _authorization_spec(
            '[[effects]]\nname = "fetch"\nkind = "network"\n'
            'authorized_by = "user"\nevidence_ref = "SESSION_BRIEF.md"\n'
            'status = "not_authorized"\n'
        ),
        encoding="utf-8",
    )
    (session / "00" / "06-EXECUTION_SUMMARY.md").write_text(
        _authorization_summary(
            '[[effects_executed]]\neffect = "fetch"\nexecuted = true\n'
            'authorization_ref = "SESSION_BRIEF.md"\n'
        ),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("UNAUTHORIZED" in x for x in v)


def test_effects_executed_authorized_passes(tmp_path):
    session = _write_session(tmp_path, version="8.0.0")
    (session / "00" / "02-TASK_SPECIFICATION.md").write_text(
        _authorization_spec(
            '[[effects]]\nname = "fetch"\nkind = "network"\n'
            'authorized_by = "user"\nevidence_ref = "SESSION_BRIEF.md"\n'
            'status = "authorized"\n'
        ),
        encoding="utf-8",
    )
    (session / "00" / "06-EXECUTION_SUMMARY.md").write_text(
        _authorization_summary(
            '[[effects_executed]]\neffect = "fetch"\nexecuted = true\n'
            'authorization_ref = "SESSION_BRIEF.md"\n'
        ),
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_effects_bad_shape_flagged(tmp_path):
    session = _write_session(tmp_path, version="8.0.0")
    (session / "00" / "02-TASK_SPECIFICATION.md").write_text(
        _authorization_spec(
            '[[effects]]\nname = "fetch"\nkind = "ssh"\n'
            'authorized_by = "user"\nevidence_ref = "x"\nstatus = "authorized"\n'
        ),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("bad kind 'ssh'" in x for x in v)


def test_legacy_session_effects_not_flagged(tmp_path):
    session = _write_session(tmp_path, version="7.0.0")
    (session / "00" / "06-EXECUTION_SUMMARY.md").write_text(
        _authorization_summary(
            '[[effects_executed]]\neffect = "clone"\nexecuted = true\n'
            'authorization_ref = "x"\n'
        ),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert all("AUTHORIZATION_UNDETERMINED" not in x for x in v)
    assert all("UNAUTHORIZED" not in x for x in v)


def _invalidated_facts_summary(entries: str) -> str:
    return (
        "# Summary\n\n## Invalidated Facts\n\n```toml\n"
        + entries
        + "```\n"
    )


def _recommendation_report(json_body: str) -> str:
    return (
        "# Recommendation\n\n## Recommended Entries\n\n```json\n"
        + json_body
        + "\n```\n"
    )


def _lesson_file(front_matter: str) -> str:
    return "+++\n" + front_matter + "\n+++\n\n# Lesson\n"


def test_knowledge_protocol_session_passes(tmp_path):
    _write_session(tmp_path, version="9.0.0")
    assert csa.scan(tmp_path) == []


def test_invalidated_facts_missing_reason_flagged(tmp_path):
    session = _write_session(tmp_path, version="9.0.0")
    (session / "00" / "06-EXECUTION_SUMMARY.md").write_text(
        _invalidated_facts_summary(
            '[[invalidated_facts]]\nfact = "stack is Django"\n'
            'entry = ".project/knowledge/discovery/stack.md"\n'
            'reason = ""\n'
        ),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("SUMMARY" in x and "missing reason" in x for x in v)


def test_invalidated_facts_without_entries_flagged(tmp_path):
    session = _write_session(tmp_path, version="9.0.0")
    (session / "00" / "06-EXECUTION_SUMMARY.md").write_text(
        "# Summary\n\n## Invalidated Facts\n\nnone.\n",
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("without [[invalidated_facts]] entries" in x for x in v)


def test_recommendation_missing_path_flagged(tmp_path):
    session = _write_session(tmp_path, version="9.0.0")
    (session / "00" / "04-KB_RECOMMENDATION.md").write_text(
        _recommendation_report(
            '{"recommended_entries": [{"kind": "discovery", "path": ""}]}'
        ),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("RECOMMENDATION" in x and "missing path" in x for x in v)


def test_recommendation_bad_kind_flagged(tmp_path):
    session = _write_session(tmp_path, version="9.0.0")
    (session / "00" / "04-KB_RECOMMENDATION.md").write_text(
        _recommendation_report(
            '{"recommended_entries": [{"kind": "snapshot", "path": "x"}]}'
        ),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("RECOMMENDATION" in x and "bad kind" in x for x in v)


def test_recommendation_valid_passes(tmp_path):
    session = _write_session(tmp_path, version="9.0.0")
    (session / "00" / "04-KB_RECOMMENDATION.md").write_text(
        _recommendation_report(
            '{"recommended_entries": [{"kind": "lesson", '
            '"path": ".project/knowledge/entries/lesson-01.md"}]}'
        ),
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_lesson_missing_provenance_flagged(tmp_path):
    _write_session(tmp_path, version="9.0.0")
    entries = tmp_path / ".project" / "knowledge" / "entries"
    entries.mkdir(parents=True)
    (entries / "lesson-01.md").write_text(
        _lesson_file('kind = "lesson"\nprotocol_version = "9.0.0"\n'),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("LESSON" in x and "missing session_id" in x for x in v)
    assert any("LESSON" in x and "missing evidence" in x for x in v)


def test_lesson_valid_passes(tmp_path):
    _write_session(tmp_path, version="9.0.0")
    entries = tmp_path / ".project" / "knowledge" / "entries"
    entries.mkdir(parents=True)
    (entries / "lesson-01.md").write_text(
        _lesson_file(
            'kind = "lesson"\nsession_id = "uuid"\n'
            'protocol_version = "9.0.0"\n'
            "[evidence]\nclass = \"reference\"\n"
            'ref = "00/00-SESSION_LOG.md"\n'
        ),
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_legacy_session_knowledge_not_flagged(tmp_path):
    session = _write_session(tmp_path, version="8.0.0")
    (session / "00" / "06-EXECUTION_SUMMARY.md").write_text(
        _invalidated_facts_summary(
            '[[invalidated_facts]]\nfact = "x"\nentry = "y"\nreason = ""\n'
        ),
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert all("invalidated_facts" not in x for x in v)


# --- Execution record model (>= 11.0.0; plan 78, RFC-64) ---------------------


def test_record_model_session_passes(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    (session / "METRICS.md").write_text(
        (session / "METRICS.md").read_text(encoding="utf-8")
        + '<!-- METRIC: {"timestamp": "2026-08-25T10:02:00Z", "clock": "utc", '
        '"seq": 2, "iteration": "00", "type": "delegation", "phase": "06", '
        '"profile": null, "skills": [], "h15": "PASS"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:03:00Z", "clock": "utc", '
        '"seq": 3, "iteration": "00", "type": "reuse_event", "layer": '
        '"knowledge", "operation": "lookup", "lookup_result": "HIT"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:04:00Z", "clock": "utc", '
        '"seq": 4, "iteration": "00", "type": "provider_cache_event", '
        '"result": "hit"} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_record_model_entry_requires_iteration_and_clock(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00Z", "trigger": "H04", '
        '"transition": "PLANNING -> PLAN_READY", "result": "PASS", '
        '"checks": []} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("ENTRY" in x and "clock is required" in x for x in v)
    assert any("ENTRY" in x and "iteration must be a numeric string" in x for x in v)


def test_record_model_timestamp_divergence_requires_cause(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:06:00Z", "clock": "utc", '
        '"iteration": "00", "trigger": "H04", '
        '"transition": "PLANNING -> PLAN_READY", "result": "PASS", '
        '"checks": [], "timestamp_divergence": {"cause": ""}} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any(
        "timestamp_divergence.cause must be a non-empty string" in x for x in v
    )


def test_record_model_metric_seq_must_be_strictly_increasing(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00Z", "clock": "utc", '
        '"seq": 1, "type": "session_start", "declarative_flags": [], '
        '"protocol_version": "11.0.0"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:02:00Z", "clock": "utc", '
        '"seq": 1, "iteration": "00", "type": "delegation", "phase": "06", '
        '"profile": null, "skills": [], "h15": "PASS"} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any(
        "seq must be strictly increasing within the session file" in x for x in v
    )


def test_record_model_metric_requires_iteration_for_execution_events(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00Z", "clock": "utc", '
        '"seq": 1, "type": "session_start", "declarative_flags": [], '
        '"protocol_version": "11.0.0"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:02:00Z", "clock": "utc", '
        '"seq": 2, "type": "reuse_event", "layer": "discovery", '
        '"operation": "lookup", "lookup_result": "MISS"} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("reuse_event" in x and "iteration must be a numeric string" in x for x in v)


def test_record_model_delegation_optional_fields_validated(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00Z", "clock": "utc", '
        '"seq": 1, "type": "session_start", "declarative_flags": [], '
        '"protocol_version": "11.0.0"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:02:00Z", "clock": "utc", '
        '"seq": 2, "iteration": "00", "type": "delegation", "phase": "06", '
        '"profile": null, "skills": [], "h15": "PASS", "context_budget": -1, '
        '"attempt": 0} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("context_budget must be a finite positive number" in x for x in v)
    assert any("attempt must be a positive integer" in x for x in v)


def test_record_model_delegation_requires_paired_budget_event(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00Z", "clock": "utc", '
        '"seq": 1, "type": "session_start", "declarative_flags": [], '
        '"protocol_version": "11.0.0"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:02:00Z", "clock": "utc", '
        '"seq": 2, "iteration": "00", "type": "delegation", "phase": "06", '
        '"profile": null, "skills": [], "h15": "PASS", '
        '"context_budget": 100} -->\n',
        encoding="utf-8",
    )
    v = csa.scan(tmp_path)
    assert any("no paired context_budget event" in x for x in v)


def test_record_model_budget_pair_passes(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00Z", "clock": "utc", '
        '"seq": 1, "type": "session_start", "declarative_flags": [], '
        '"protocol_version": "11.0.0"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:02:00Z", "clock": "utc", '
        '"seq": 2, "iteration": "00", "type": "delegation", "phase": "06", '
        '"profile": null, "skills": [], "h15": "PASS", '
        '"context_budget": 100} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:03:00Z", "clock": "utc", '
        '"seq": 3, "iteration": "00", "type": "context_budget", "phase": "06", '
        '"declared": 100, "consumed": 80} -->\n',
        encoding="utf-8",
    )
    assert csa.scan(tmp_path) == []


def test_record_model_state_out_of_scope_flagged(tmp_path):
    session = _write_session(tmp_path, version="11.0.0")
    state_path = session / "00" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["gates"]["H10"] = {
        "result": "PASS",
        "timestamp": "2026-08-25T10:10:00Z",
    }
    state_path.write_text(json.dumps(state), encoding="utf-8")
    v = csa.scan(tmp_path)
    assert any("H10" in x and "outside the transition scope" in x for x in v)


def test_legacy_published_band_record_model_not_flagged(tmp_path):
    session = _write_session(tmp_path, version="10.3.0")
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-25T10:05:00Z", "trigger": "H04", '
        '"transition": "PLANNING -> PLAN_READY", "result": "PASS", '
        '"checks": []} -->\n',
        encoding="utf-8",
    )
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-25T10:01:00Z", "clock": "utc", '
        '"type": "session_start", "declarative_flags": [], '
        '"protocol_version": "10.3.0"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-25T10:02:00Z", "clock": "utc", '
        '"type": "delegation", "phase": "06", "profile": null, "skills": [], '
        '"h15": "PASS", "context_budget": 100} -->\n',
        encoding="utf-8",
    )
    state_path = session / "00" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["gates"]["H10"] = {
        "result": "PASS",
        "timestamp": "2026-08-25T10:10:00Z",
    }
    state_path.write_text(json.dumps(state), encoding="utf-8")
    v = csa.scan(tmp_path)
    assert all(
        "clock is required" not in x
        and "iteration must be a numeric string" not in x
        and "outside the transition scope" not in x
        and "no paired context_budget event" not in x
        for x in v
    )
