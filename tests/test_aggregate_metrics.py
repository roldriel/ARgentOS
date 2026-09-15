"""Tests for tools/aggregate_metrics.py (dev-only, no payload dependency)."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

REPO_ROOT = Path(__file__).resolve().parents[1]

import aggregate_metrics as am  # noqa: E402


def build_session(tmp_path: Path) -> Path:
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "01").mkdir()
    (session / "00" / "01-TASK_ANALYSIS.md").write_text("# a\n", encoding="utf-8")
    (session / "00" / "05-EXECUTION_PLAN.md").write_text("# b\n", encoding="utf-8")
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "01" / "07-VERIFICATION_REPORT.md").write_text("# c\n", encoding="utf-8")
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-14T10:00:00+00:00", "trigger": "H04", '
        '"transition": "A -> B", "result": "PASS", "checks": []} -->\n'
        '<!-- ENTRY: {"timestamp": "2026-08-14T10:05:00+00:00", "trigger": "H06", '
        '"transition": "B -> C", "result": "FAIL", "checks": []} -->\n',
        encoding="utf-8",
    )
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-14T09:59:00+00:00", "type": "session_start", '
        '"declarative_flags": ["tdd"], "protocol_version": "3.11.0"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-14T10:01:00+00:00", "type": "state_transition", '
        '"from": "EXECUTING", "to": "RECOVERY", "iteration": "00"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-14T10:02:00+00:00", "type": "failure", '
        '"class": "blocker", "audience": "agent"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-14T10:03:00+00:00", "type": "delegation", '
        '"phase": "06", "profile": "backend_engineer", "skills": [], "h15": "PASS"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-14T10:04:00+00:00", "type": "flag_evidence", '
        '"flag": "tdd"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-14T10:04:30+00:00", "type": "context_budget", '
        '"phase": "06", "declared": 1000, "consumed": 800} -->\n',
        encoding="utf-8",
    )
    return tmp_path


def test_aggregation_catalog(tmp_path):
    root = build_session(tmp_path)
    report = am.aggregate(root)
    assert report["harness.invocations"] == 2
    assert report["harness.pass"] == 1
    assert report["harness.fail"] == 1
    assert report["failures.harness_by_domain"] == {"H": 1}
    assert report["flow.transitions"] == 1
    assert report["flow.recovery_entries"] == 1
    assert report["failures.by_class"] == {"blocker": 1}
    assert report["failures.agent_evaluated"] == 1
    assert report["delegation.count"] == 1
    assert report["delegation.profiles"] == {"backend_engineer": 1}
    assert report["context.budget_declared"] == 1000
    assert report["context.budget_consumed"] == 800
    assert report["flags.expected"] == ["tdd"]
    assert report["flags.evidenced"] == ["tdd"]
    assert report["flags.unevidenced"] == []
    assert report["session.iterations"] == 2
    assert report["session.artifacts_per_iteration"] == [{"s1": {"00": 2, "01": 1}}]
    assert report["corrupt"] == {"entry": 0, "metric": 0}
    assert report["session.duration_ms"] is not None
    assert report["health.recovery_rate"] == 1.0
    assert report["health.clarification_rate"] == 0.0
    assert report["health.reviewer_rework_rate"] == 0.0


def test_corrupt_comments_counted(tmp_path):
    session = tmp_path / ".project" / "s1"
    session.mkdir(parents=True)
    (session / "HARNESS_REPORT.md").write_text(
        "<!-- ENTRY: {not json -->\n", encoding="utf-8"
    )
    (session / "METRICS.md").write_text(
        "<!-- METRIC: {also not json -->\n", encoding="utf-8"
    )
    report = am.aggregate(tmp_path)
    assert report["corrupt"] == {"entry": 1, "metric": 1}


def test_no_project_dir(tmp_path):
    report = am.aggregate(tmp_path)
    assert report["session.iterations"] == 0
    assert report["corrupt"] == {"entry": 0, "metric": 0}


def build_session_two(tmp_path: Path) -> Path:
    session = tmp_path / ".project" / "s2"
    (session / "00").mkdir(parents=True)
    (session / "00" / "07-VERIFICATION_REPORT.md").write_text("# v\n", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-14T11:00:00+00:00", "type": "session_start", '
        '"declarative_flags": ["srp"], "protocol_version": "3.16.0"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-14T11:01:00+00:00", "type": "state_transition", '
        '"from": "PLANNING", "to": "PLAN_READY", "iteration": "00"} -->\n',
        encoding="utf-8",
    )
    return tmp_path


def test_per_session_catalog(tmp_path):
    build_session(tmp_path)
    build_session_two(tmp_path)
    s1 = am.aggregate_session(tmp_path / ".project" / "s1")
    s2 = am.aggregate_session(tmp_path / ".project" / "s2")
    assert s1["flow.transitions"] == 1
    assert s1["delegation.count"] == 1
    assert s1["flags.expected"] == ["tdd"]
    assert s2["flow.transitions"] == 1
    assert s2["delegation.count"] == 0
    assert s2["flags.expected"] == ["srp"]

    project = am.aggregate(tmp_path)
    assert project["flow.transitions"] == 2
    assert project["delegation.count"] == 1
    assert project["flags.expected"] == ["srp", "tdd"]
    assert project["session.iterations"] == 3
    assert len(project["session.artifacts_per_iteration"]) == 2


def test_budget_overruns_counted(tmp_path):
    session = tmp_path / ".project" / "s1"
    session.mkdir(parents=True)
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "t", "type": "context_budget", '
        '"phase": "06", "declared": 100, "consumed": 150} -->\n'
        '<!-- METRIC: {"timestamp": "t", "type": "context_budget", '
        '"phase": "05", "declared": 200, "consumed": 50} -->\n',
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["context.budget_overruns"] == 1
    assert report["context.budget_declared"] == 300
    assert report["context.budget_consumed"] == 200


def build_reuse_session(tmp_path: Path) -> Path:
    """A session with reuse/provider-cache events (plan 91 fixtures)."""
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:00Z", "type": "reuse_event", '
        '"layer": "discovery", "operation": "lookup", "lookup_result": "HIT"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:01Z", "type": "reuse_event", '
        '"layer": "knowledge", "operation": "eligibility", '
        '"eligibility_decision": "REJECTED", "reason": "availability"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:02Z", "type": "reuse_event", '
        '"layer": "materialization", "operation": "reuse_attempt", '
        '"reuse_outcome": "SUCCESSFUL"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:03Z", "type": '
        '"provider_cache_event", "result": "hit", "tokens_cached": 500, '
        '"latency_ms": 120} -->\n',
        encoding="utf-8",
    )
    return tmp_path


def test_reuse_events_aggregated_by_layer(tmp_path):
    build_reuse_session(tmp_path)
    report = am.aggregate(tmp_path)
    assert report["reuse.lookup_hits"] == {"discovery": 1}
    assert report["reuse.lookup_misses"] == {}
    assert report["reuse.eligibility_rejected"] == {"knowledge": 1}
    assert report["reuse.outcome_successful"] == {"materialization": 1}
    assert report["reuse.outcome_failed"] == {}
    assert report["reuse.invalidated"] == {}
    assert report["corrupt"] == {"entry": 0, "metric": 0}


def test_provider_cache_events_aggregated(tmp_path):
    build_reuse_session(tmp_path)
    report = am.aggregate(tmp_path)
    assert report["cache.provider_hits"] == 1
    assert report["cache.provider_misses"] == 0
    assert report["cache.provider_unavailable"] == 0
    assert report["cache.tokens_cached"] == 500
    assert report["cache.latency_ms"] == [120]


def test_provider_tokens_unavailable_not_fabricated(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:00Z", "type": '
        '"provider_cache_event", "result": "hit"} -->\n',
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["cache.provider_hits"] == 1
    assert report["cache.tokens_cached"] is None
    assert report["cache.tokens_uncached"] is None
    assert report["cache.latency_ms"] is None
    assert report["evidence.availability"]["cache.tokens_cached"] == "NOT AVAILABLE"


def test_no_global_cache_hit_or_savings(tmp_path):
    build_reuse_session(tmp_path)
    report = am.aggregate(tmp_path)
    assert "cache_hit" not in report
    assert "savings" not in report
    assert "hit_rate" not in report
    assert not any(key.startswith("economics") for key in report)


def test_no_double_counting_provider_cache_hit(tmp_path):
    # A provider cache HIT and a materialization reuse event must not be summed
    # as one generic economic benefit: each layer keeps its own attribution.
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:00Z", "type": '
        '"provider_cache_event", "result": "hit", "tokens_cached": 500} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:01Z", "type": "reuse_event", '
        '"layer": "materialization", "operation": "lookup", '
        '"lookup_result": "HIT"} -->\n',
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["cache.provider_hits"] == 1
    assert report["cache.tokens_cached"] == 500
    assert report["reuse.lookup_hits"] == {"materialization": 1}
    assert not any(key in report for key in ("reuse.savings", "cache.savings", "savings"))


def test_freshness_not_lookup_result(tmp_path):
    # FRESH/STALE/UNKNOWN are freshness metadata (reason=availability), never
    # HIT/MISS lookup results: the knowledge eligibility event below must not
    # create a lookup hit or miss, and a lookup event without a result must not
    # fabricate one.
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:00Z", "type": "reuse_event", '
        '"layer": "knowledge", "operation": "eligibility", '
        '"eligibility_decision": "REJECTED", "reason": "availability"} -->\n'
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:01Z", "type": "reuse_event", '
        '"layer": "knowledge", "operation": "lookup"} -->\n',
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["reuse.lookup_hits"] == {}
    assert report["reuse.lookup_misses"] == {}
    assert report["reuse.eligibility_rejected"] == {"knowledge": 1}


def test_unknown_events_and_fields_ignored(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "t", "type": "future_event_type"} -->\n'
        '<!-- METRIC: {"timestamp": "t", "type": "delegation", "phase": "06", '
        '"profile": null, "skills": [], "h15": "PASS", '
        '"unknown_extra_field": "ignored"} -->\n',
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["delegation.count"] == 1
    assert report["corrupt"] == {"entry": 0, "metric": 0}
    assert "future_event_type" not in report


def test_evidence_classification_reported(tmp_path):
    build_reuse_session(tmp_path)
    # Valid discovery evidence: fresh marker + active entries -> Derived value
    # with DISPONIBLE availability (the no-evidence case is covered by the
    # C-3 Unavailable tests).
    marker = tmp_path / ".project" / ".last_discovery"
    marker.write_text(
        json.dumps({"timestamp": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )
    manifest_dir = tmp_path / ".project" / "knowledge" / "discovery"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / ".discovery_manifest").write_text(
        json.dumps(
            {
                "knowledge_base": {"ttl_hours": 24},
                "entries": {"active": ["stack.md"], "stale": []},
            }
        ),
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["evidence.classes"]["reuse.lookup_hits"] == "Recorded"
    assert report["evidence.classes"]["discovery.reuse_opportunities"] == "Derived"
    assert report["evidence.availability"]["cache.provider_hits"] == "NOT AVAILABLE"
    assert (
        report["evidence.availability"]["discovery.reuse_opportunities"]
        == "DISPONIBLE"
    )
    assert report["discovery.reuse_opportunities"] == 1


def test_append_only_artifacts_unchanged(tmp_path):
    build_reuse_session(tmp_path)
    metrics_file = tmp_path / ".project" / "s1" / "METRICS.md"
    before = metrics_file.read_bytes()
    am.aggregate(tmp_path)
    am.aggregate_session(tmp_path / ".project" / "s1")
    assert metrics_file.read_bytes() == before


def test_corrupt_reuse_event_counted(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "t", "type": "reuse_event", '
        '"operation": "lookup", "lookup_result": "HIT"} -->\n'
        '<!-- METRIC: {"timestamp": "t", "type": "provider_cache_event", '
        '"tokens_cached": 1} -->\n',
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["corrupt"]["metric"] == 2
    assert report["reuse.lookup_hits"] == {}
    assert report["cache.provider_hits"] == 0


def test_no_economic_admission(tmp_path):
    build_reuse_session(tmp_path)
    report = am.aggregate(tmp_path)
    assert not any("admission" in key or "gate" in key for key in report)


def test_discovery_reuse_opportunities_derived(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:00Z", "type": "session_start", '
        '"declarative_flags": [], "protocol_version": "10.3.0"} -->\n',
        encoding="utf-8",
    )
    now = datetime.now(timezone.utc)
    marker = tmp_path / ".project" / ".last_discovery"
    marker.write_text(
        json.dumps({"timestamp": now.isoformat()}), encoding="utf-8"
    )
    manifest_dir = tmp_path / ".project" / "knowledge" / "discovery"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / ".discovery_manifest").write_text(
        json.dumps(
            {
                "knowledge_base": {"ttl_hours": 24},
                "entries": {
                    "active": ["stack.md", "env.md"],
                    "stale": ["old.md"],
                },
            }
        ),
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["discovery.reuse_opportunities"] == 2
    assert report["evidence.availability"]["discovery.reuse_opportunities"] == "DISPONIBLE"


def test_discovery_reuse_opportunities_stale_zero(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    marker = tmp_path / ".project" / ".last_discovery"
    old = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    marker.write_text(json.dumps({"timestamp": old}), encoding="utf-8")
    manifest_dir = tmp_path / ".project" / "knowledge" / "discovery"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / ".discovery_manifest").write_text(
        json.dumps(
            {
                "knowledge_base": {"ttl_hours": 24},
                "entries": {"active": ["stack.md"], "stale": []},
            }
        ),
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["discovery.reuse_opportunities"] == 0
    assert report["evidence.availability"]["discovery.reuse_opportunities"] == "DISPONIBLE"


def test_discovery_reuse_opportunities_missing_artifacts_unavailable(tmp_path):
    # Case A: missing .last_discovery / manifest -> Unavailable (None), never 0.
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    report = am.aggregate(tmp_path)
    assert report["discovery.reuse_opportunities"] is None
    assert report["evidence.availability"]["discovery.reuse_opportunities"] == "NOT AVAILABLE"


def test_discovery_reuse_opportunities_invalid_metadata_unavailable(tmp_path):
    # Case D: invalid discovery metadata -> Unavailable, never 0.
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    marker = tmp_path / ".project" / ".last_discovery"
    manifest_dir = tmp_path / ".project" / "knowledge" / "discovery"
    manifest_dir.mkdir(parents=True)

    # D1: malformed marker JSON.
    marker.write_text("{not json", encoding="utf-8")
    (manifest_dir / ".discovery_manifest").write_text(
        json.dumps(
            {
                "knowledge_base": {"ttl_hours": 24},
                "entries": {"active": ["stack.md"], "stale": []},
            }
        ),
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["discovery.reuse_opportunities"] is None
    assert report["evidence.availability"]["discovery.reuse_opportunities"] == "NOT AVAILABLE"

    # D2: manifest without a parseable TTL.
    marker.write_text(
        json.dumps({"timestamp": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )
    (manifest_dir / ".discovery_manifest").write_text(
        json.dumps({"knowledge_base": {}, "entries": {"active": ["stack.md"]}}),
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["discovery.reuse_opportunities"] is None


def test_discovery_reuse_opportunities_valid_zero_fresh(tmp_path):
    # Case B: valid evidence, zero fresh active entries -> 0 (not Unavailable).
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    marker = tmp_path / ".project" / ".last_discovery"
    marker.write_text(
        json.dumps({"timestamp": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )
    manifest_dir = tmp_path / ".project" / "knowledge" / "discovery"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / ".discovery_manifest").write_text(
        json.dumps(
            {
                "knowledge_base": {"ttl_hours": 24},
                "entries": {"active": [], "stale": ["old.md"]},
            }
        ),
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["discovery.reuse_opportunities"] == 0
    assert report["evidence.availability"]["discovery.reuse_opportunities"] == "DISPONIBLE"


def test_reuse_opportunities_not_observed_events(tmp_path):
    # C-2 semantics: the derived discovery estimate must not feed observed
    # counters. A fresh KB yields N derived opportunities with no reuse_event
    # or provider_cache_event present, and N never increments lookup/miss/
    # outcome/provider counters.
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-31T10:00:00Z", "type": "session_start", '
        '"declarative_flags": [], "protocol_version": "10.3.0"} -->\n',
        encoding="utf-8",
    )
    marker = tmp_path / ".project" / ".last_discovery"
    marker.write_text(
        json.dumps({"timestamp": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )
    manifest_dir = tmp_path / ".project" / "knowledge" / "discovery"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / ".discovery_manifest").write_text(
        json.dumps(
            {
                "knowledge_base": {"ttl_hours": 24},
                "entries": {"active": ["stack.md", "env.md"], "stale": []},
            }
        ),
        encoding="utf-8",
    )
    report = am.aggregate(tmp_path)
    assert report["discovery.reuse_opportunities"] == 2
    assert report["reuse.lookup_hits"] == {}
    assert report["reuse.lookup_misses"] == {}
    assert report["reuse.outcome_successful"] == {}
    assert report["reuse.outcome_failed"] == {}
    assert report["cache.provider_hits"] == 0
    assert report["corrupt"] == {"entry": 0, "metric": 0}


def test_audit_matching_gates_no_alerts(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text(
        json.dumps({"gates": {"H04": {"result": "PASS", "timestamp": "t"}}}),
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    assert am.audit_cross_checks(tmp_path) == []


def test_audit_state_gate_without_entry_alerted(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text(
        json.dumps({"gates": {"H04": {"result": "PASS", "timestamp": "t"}}}),
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H00", "transition": "X -> Y", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    alerts = am.audit_cross_checks(tmp_path)
    assert any("H04" in a and "without a matching PASS entry" in a for a in alerts)


def test_audit_entry_without_state_alerted(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "00" / "state.json").write_text("{}", encoding="utf-8")
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-14T11:00:00+00:00", "type": '
        '"session_start", "declarative_flags": [], "protocol_version": "4.0.0"} -->\n',
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    alerts = am.audit_cross_checks(tmp_path)
    assert any("H04" in a and "without a matching PASS in state.json" in a for a in alerts)


def test_audit_legacy_entry_without_state_ok(tmp_path):
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-14T11:00:00+00:00", "type": '
        '"session_start", "declarative_flags": [], "protocol_version": "3.16.0"} -->\n',
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    assert am.audit_cross_checks(tmp_path) == []


# --- Execution record model audit (>= 11.0.0; plan 78, RFC-64) --------------


def _record_session(tmp_path, version="11.0.0"):
    """Write a session declaring a protocol version (no gate records yet)."""
    session = tmp_path / ".project" / "s1"
    (session / "00").mkdir(parents=True)
    (session / "01").mkdir()
    (session / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "2026-08-14T11:00:00+00:00", "type": '
        '"session_start", "declarative_flags": [], "protocol_version": "'
        + version
        + '"} -->\n',
        encoding="utf-8",
    )
    return session


def test_audit_iteration_correlation_no_alerts(tmp_path):
    session = _record_session(tmp_path)
    (session / "00" / "state.json").write_text(
        json.dumps(
            {
                "gates": {
                    "H04": {
                        "result": "PASS",
                        "timestamp": "2026-08-14T10:00:00+00:00",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-14T10:00:30+00:00", '
        '"iteration": "00", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    assert am.audit_cross_checks(tmp_path) == []


def test_audit_iteration_disparity_alerted(tmp_path):
    session = _record_session(tmp_path)
    (session / "00" / "state.json").write_text(
        json.dumps(
            {
                "gates": {
                    "H04": {
                        "result": "PASS",
                        "timestamp": "2026-08-14T10:00:00+00:00",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-14T10:00:30+00:00", '
        '"iteration": "01", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    alerts = am.audit_cross_checks(tmp_path)
    assert any(
        "H04" in a
        and "in iteration 00" in a
        and "without a matching PASS entry" in a
        for a in alerts
    )


def test_audit_timestamp_divergence_without_cause_alerted(tmp_path):
    session = _record_session(tmp_path)
    (session / "00" / "state.json").write_text(
        json.dumps(
            {
                "gates": {
                    "H04": {
                        "result": "PASS",
                        "timestamp": "2026-08-14T10:00:00+00:00",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-14T10:05:00+00:00", '
        '"iteration": "00", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    alerts = am.audit_cross_checks(tmp_path)
    assert any(
        "diverges more than 60s" in a
        and "without timestamp_divergence.cause" in a
        for a in alerts
    )


def test_audit_timestamp_divergence_with_cause_ok(tmp_path):
    session = _record_session(tmp_path)
    (session / "00" / "state.json").write_text(
        json.dumps(
            {
                "gates": {
                    "H04": {
                        "result": "PASS",
                        "timestamp": "2026-08-14T10:00:00+00:00",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-14T10:05:00+00:00", '
        '"iteration": "00", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": [], "timestamp_divergence": '
        '{"cause": "retroactive reconstruction reviewed"}} -->\n',
        encoding="utf-8",
    )
    assert am.audit_cross_checks(tmp_path) == []


def test_audit_60s_tolerance_no_alert(tmp_path):
    session = _record_session(tmp_path)
    (session / "00" / "state.json").write_text(
        json.dumps(
            {
                "gates": {
                    "H04": {
                        "result": "PASS",
                        "timestamp": "2026-08-14T10:00:00+00:00",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-14T10:00:50+00:00", '
        '"iteration": "00", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    assert am.audit_cross_checks(tmp_path) == []


def test_audit_legacy_band_without_iteration_keeps_trigger_correlation(tmp_path):
    session = _record_session(tmp_path, version="10.3.0")
    (session / "00" / "state.json").write_text(
        json.dumps(
            {
                "gates": {
                    "H04": {
                        "result": "PASS",
                        "timestamp": "2026-08-14T10:00:00+00:00",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (session / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "2026-08-14T10:00:30+00:00", '
        '"trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": []} -->\n',
        encoding="utf-8",
    )
    assert am.audit_cross_checks(tmp_path) == []
