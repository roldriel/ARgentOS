"""Tests for the protocol metrics aggregation (runner_metrics.py + CLI).

Covers the aggregation rule of `.agents/standards/runtime/PROTOCOL_METRICS.md`
and the event catalog of `.agents/contracts/METRICS.md`.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import runner_metrics

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = PROJECT_ROOT / ".agents" / "harness" / "runner.py"


@pytest.fixture
def project(tmp_path):
    """Temporary artifacts directory with two sessions."""
    artifacts_dir = tmp_path / ".project"
    for uuid in ("sess-a", "sess-b"):
        (artifacts_dir / uuid / "00").mkdir(parents=True)
    return artifacts_dir


def _write_harness_report(session_dir: Path, entries: list[dict]) -> None:
    lines = ["# Harness Report", "", "## Entries", ""]
    for entry in entries:
        lines.append(f"### {entry['trigger']}")
        lines.append("")
        lines.append(f"<!-- ENTRY: {json.dumps(entry)} -->")
        lines.append("")
    (session_dir / "HARNESS_REPORT.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def _write_metrics(session_dir: Path, events: list[dict]) -> None:
    lines = ["# Protocol Metrics", "", "- Session UUID: `x`", "", "## Entries", ""]
    for event in events:
        lines.append(f"<!-- METRIC: {json.dumps(event)} -->")
    (session_dir / "METRICS.md").write_text("\n".join(lines), encoding="utf-8")


def _entry(trigger, result, duration_ms=10, timestamp="2026-08-05T10:00:00Z"):
    return {
        "timestamp": timestamp,
        "trigger": trigger,
        "transition": "X → Y",
        "result": result,
        "checks": [],
        "artifact": None,
        "duration_ms": duration_ms,
        "rubric_scores": {},
    }


# ---------------------------------------------------------------------------
# Harness data points
# ---------------------------------------------------------------------------


def test_harness_entries_aggregated_per_trigger_and_domain(project):
    session_dir = project / "sess-a"
    _write_harness_report(
        session_dir,
        [
            _entry("H01", "PASS", 10),
            _entry("H01", "FAIL", 30, "2026-08-05T10:01:00Z"),
            _entry("D00", "FAIL", 20, "2026-08-05T10:02:00Z"),
            _entry("S00", "PASS", 5, "2026-08-05T10:03:00Z"),
        ],
    )
    result = runner_metrics.aggregate_session(session_dir)

    h01 = result["harness"]["per_trigger"]["H01"]
    assert h01 == {
        "invocations": 2,
        "pass": 1,
        "fail": 1,
        "duration_ms": 40,
        "avg_duration_ms": 20,
    }
    assert result["harness"]["fails_by_domain"]["H"] == {
        "invocations": 2,
        "fail": 1,
    }
    assert result["harness"]["fails_by_domain"]["D"] == {
        "invocations": 1,
        "fail": 1,
    }
    assert result["harness"]["fails_by_domain"]["S"] == {
        "invocations": 1,
        "fail": 0,
    }


def test_missing_reports_yield_empty_metrics(project):
    result = runner_metrics.aggregate_session(project / "sess-a")
    assert result["harness"]["per_trigger"] == {}
    assert result["flow"]["transitions"] == 0
    assert result["flags"]["expected"] == []
    assert result["corrupt_entries_discarded"] == 0


def test_corrupt_comments_are_counted_not_fatal(project):
    session_dir = project / "sess-a"
    (session_dir / "HARNESS_REPORT.md").write_text(
        "<!-- ENTRY: {broken -->\n"
        f"<!-- ENTRY: {json.dumps(_entry('H01', 'PASS'))} -->\n",
        encoding="utf-8",
    )
    (session_dir / "METRICS.md").write_text(
        "<!-- METRIC: not-json -->\n", encoding="utf-8"
    )
    result = runner_metrics.aggregate_session(session_dir)
    assert result["corrupt_entries_discarded"] == 2
    assert result["harness"]["per_trigger"]["H01"]["invocations"] == 1


# ---------------------------------------------------------------------------
# Event data points
# ---------------------------------------------------------------------------


def test_flow_events_counted(project):
    session_dir = project / "sess-a"
    _write_metrics(
        session_dir,
        [
            {"timestamp": "2026-08-05T10:00:00Z", "type": "state_transition", "from": "PLANNING", "to": "PLAN_READY", "iteration": "00"},
            {"timestamp": "2026-08-05T10:01:00Z", "type": "state_transition", "from": "EXECUTING", "to": "RECOVERY", "iteration": "00"},
            {"timestamp": "2026-08-05T10:02:00Z", "type": "state_transition", "from": "ANALYZING_TASK", "to": "NEEDS_CLARIFICATION", "iteration": "00"},
            {"timestamp": "2026-08-05T10:03:00Z", "type": "reviewer_retry", "artifact": "EXECUTION_SUMMARY.md", "cycle": 1},
        ],
    )
    flow = runner_metrics.aggregate_session(session_dir)["flow"]
    assert flow == {
        "transitions": 3,
        "recovery_entries": 1,
        "clarification_entries": 1,
        "reviewer_retries": 1,
    }


def test_failure_events_by_class_and_audience(project):
    session_dir = project / "sess-a"
    _write_metrics(
        session_dir,
        [
            {"timestamp": "t", "type": "failure", "class": "F1"},
            {"timestamp": "t", "type": "failure", "class": "F2", "audience": "agent"},
            {"timestamp": "t", "type": "failure", "class": "F2", "audience": "machine"},
            {"timestamp": "t", "type": "failure", "class": "F9"},  # unknown: ignored
        ],
    )
    failures = runner_metrics.aggregate_session(session_dir)["failures"]
    assert failures["by_class"] == {"F1": 1, "F2": 2}
    assert failures["agent_evaluated"] == 1


def test_delegation_and_skill_override_events(project):
    session_dir = project / "sess-a"
    _write_metrics(
        session_dir,
        [
            {"timestamp": "t", "type": "delegation", "phase": "06", "profile": "backend_engineer", "skills": ["self-review"], "h15": "PASS"},
            {"timestamp": "t", "type": "delegation", "phase": "06", "profile": None, "skills": [], "h15": "FAIL"},
            {"timestamp": "t", "type": "skill_override", "skill": "critic"},
        ],
    )
    delegation = runner_metrics.aggregate_session(session_dir)["delegation"]
    assert delegation == {
        "count": 2,
        "validity_violations": 1,
        "skill_overrides": 1,
        "profiles": {"backend_engineer": 1},
    }


def test_context_and_flag_events(project):
    session_dir = project / "sess-a"
    _write_metrics(
        session_dir,
        [
            {"timestamp": "t", "type": "session_start", "declarative_flags": ["caveman", "knowledge_base"]},
            {"timestamp": "t", "type": "flag_evidence", "flag": "caveman"},
            {"timestamp": "t", "type": "context_budget", "phase": "06", "declared": 4000, "consumed": 3100},
            {"timestamp": "t", "type": "context_candidates", "prioritized": 12, "resolved": 8, "composed": 5},
        ],
    )
    result = runner_metrics.aggregate_session(session_dir)
    assert result["flags"] == {
        "expected": ["caveman", "knowledge_base"],
        "evidenced": ["caveman"],
        "unevidenced": ["knowledge_base"],
    }
    assert result["context"] == {
        "budget_declared": 4000,
        "budget_consumed": 3100,
        "candidates": {"prioritized": 12, "resolved": 8, "composed": 5},
    }


def test_unknown_event_types_and_fields_ignored(project):
    session_dir = project / "sess-a"
    _write_metrics(
        session_dir,
        [
            {"timestamp": "t", "type": "future_event", "foo": 1},
            {"timestamp": "t", "type": "skill_override", "skill": "x", "extra": "ok"},
        ],
    )
    result = runner_metrics.aggregate_session(session_dir)
    assert result["delegation"]["skill_overrides"] == 1


# ---------------------------------------------------------------------------
# Session metrics from the filesystem
# ---------------------------------------------------------------------------


def test_session_metrics_from_layout_and_timestamps(project):
    session_dir = project / "sess-a"
    (session_dir / "01").mkdir()
    (session_dir / "00" / "01-TASK_ANALYSIS.md").write_text("x", encoding="utf-8")
    (session_dir / "00" / "notes.txt").write_text("x", encoding="utf-8")
    (session_dir / "01" / "a.md").write_text("x", encoding="utf-8")
    (session_dir / "01" / "b.md").write_text("x", encoding="utf-8")
    _write_harness_report(
        session_dir,
        [
            _entry("H01", "PASS", timestamp="2026-08-05T10:00:00Z"),
            _entry("H01", "PASS", timestamp="2026-08-05T10:00:10Z"),
        ],
    )
    metrics = runner_metrics.aggregate_session(session_dir)["session_metrics"]
    assert metrics["iterations"] == 2
    assert metrics["artifacts_per_iteration"] == {"00": 1, "01": 2}
    assert metrics["duration_ms"] == 10000


# ---------------------------------------------------------------------------
# Project aggregation and health signals
# ---------------------------------------------------------------------------


def test_project_aggregation_health_signals(project):
    for uuid, events in (
        (
            "sess-a",
            [
                {"timestamp": "t", "type": "state_transition", "from": "A", "to": "RECOVERY", "iteration": "00"},
                {"timestamp": "t", "type": "state_transition", "from": "A", "to": "B", "iteration": "00"},
                {"timestamp": "t", "type": "delegation", "phase": "06", "profile": None, "skills": [], "h15": "PASS"},
                {"timestamp": "t", "type": "reviewer_retry", "artifact": "X.md", "cycle": 1},
            ],
        ),
        (
            "sess-b",
            [
                {"timestamp": "t", "type": "state_transition", "from": "A", "to": "NEEDS_CLARIFICATION", "iteration": "00"},
                {"timestamp": "t", "type": "state_transition", "from": "A", "to": "B", "iteration": "00"},
                {"timestamp": "t", "type": "delegation", "phase": "06", "profile": None, "skills": [], "h15": "PASS"},
            ],
        ),
    ):
        _write_metrics(project / uuid, events)

    report = runner_metrics.aggregate_project(project)
    assert report["sessions"] == 2
    assert len(report["per_session"]) == 2
    assert report["health_signals"] == {
        "recovery_rate": 0.25,
        "clarification_rate": 0.25,
        "reviewer_rework_rate": 0.5,
    }


def test_health_signals_null_without_data(project):
    report = runner_metrics.aggregate_project(project)
    assert report["health_signals"] == {
        "recovery_rate": None,
        "clarification_rate": None,
        "reviewer_rework_rate": None,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RUNNER_PATH), *args],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )


def test_cli_metrics_session(project):
    _write_metrics(
        project / "sess-a",
        [{"timestamp": "t", "type": "skill_override", "skill": "critic"}],
    )
    proc = _run_cli(
        "metrics", "--session", "sess-a", "--artifacts-dir", str(project)
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["session"] == "sess-a"
    assert data["delegation"]["skill_overrides"] == 1


def test_cli_metrics_project(project):
    proc = _run_cli("metrics", "--artifacts-dir", str(project))
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["sessions"] == 2
    assert "health_signals" in data


def test_cli_metrics_unknown_session_fails(project):
    proc = _run_cli(
        "metrics", "--session", "nope", "--artifacts-dir", str(project)
    )
    assert proc.returncode == 1
    assert json.loads(proc.stdout)["error"]["code"] == "SESSION_NOT_FOUND"
