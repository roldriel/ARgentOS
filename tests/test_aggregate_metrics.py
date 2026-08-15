"""Tests for tools/aggregate_metrics.py (dev-only, no payload dependency)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

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
