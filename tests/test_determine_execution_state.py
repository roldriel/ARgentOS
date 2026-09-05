"""Tests for tools/determine_execution_state.py (dev-only, no payload dependency)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import determine_execution_state as des  # noqa: E402


def _write_state(session: Path, iteration: str, status: str, gates: dict) -> None:
    """Write a state.json for an iteration of a fixture session."""
    iter_dir = session / iteration
    iter_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "session": session.name,
        "iteration": iteration,
        "task_profile": "standard",
        "gates": gates,
        "last_gate": max(gates) if gates else None,
        "status": status,
        "updated": "2026-09-05T12:00:00Z",
    }
    (iter_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")


def _write_session_log(session: Path, version: str = "11.0.0") -> None:
    """Write the minimal SESSION_LOG header declaring the protocol version."""
    session.mkdir(parents=True, exist_ok=True)
    (session / "SESSION_LOG.md").write_text(
        f"# Session Log\n\n- Session UUID: {session.name}\n"
        f"- Protocol version: {version}\n",
        encoding="utf-8",
    )


def _session_uuid(tmp_path: Path, name: str = "uuid-session") -> Path:
    session = tmp_path / ".project" / name
    _write_session_log(session)
    return session


def test_no_project_dir_is_empty(tmp_path):
    report = des.determine(tmp_path)
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_completed_terminal_state_is_determined(tmp_path):
    session = _session_uuid(tmp_path)
    gates = {
        trigger: {"result": "PASS", "timestamp": "2026-09-05T12:00:00Z"}
        for trigger in ("H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07")
    }
    _write_state(session, "00", "COMPLETED", gates)
    report = des.determine(tmp_path)
    entry = report["executions"][0]
    assert entry["session"] == session.name
    assert entry["iteration"] == "00"
    assert entry["state_json"] == "present"
    assert entry["determined"] is True
    assert entry["terminal_task_state"] == "COMPLETED"
    assert entry["reason"] is None
    assert report["summary"] == {"total": 1, "determined": 1, "undetermined": 0}


def test_abort_terminal_state_is_determined(tmp_path):
    session = _session_uuid(tmp_path)
    gates = {"H00": {"result": "PASS", "timestamp": "2026-09-05T11:00:00Z"}}
    _write_state(session, "00", "ABORT", gates)
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["determined"] is True
    assert entry["terminal_task_state"] == "ABORT"


def test_in_progress_status_is_not_determined_even_with_closure_gates(tmp_path):
    """A record without terminal status must not yield an inferred result."""
    session = _session_uuid(tmp_path)
    gates = {
        trigger: {"result": "PASS", "timestamp": "2026-09-05T12:00:00Z"}
        for trigger in ("H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07")
    }
    _write_state(session, "00", "in_progress", gates)
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["determined"] is False
    assert entry["terminal_task_state"] is None
    assert entry["reason"] == "status_not_terminal"


def test_no_gates_passed_status_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "no_gates_passed", {})
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["determined"] is False
    assert entry["reason"] == "status_not_terminal"


def test_missing_state_json_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    (session / "00").mkdir()
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["state_json"] == "missing"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_missing"


def test_corrupt_state_json_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    iter_dir = session / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "state.json").write_text("{not json", encoding="utf-8")
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_corrupt"


def test_non_dict_state_json_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    iter_dir = session / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "state.json").write_text('"not-an-object"', encoding="utf-8")
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False


def test_state_json_without_status_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    iter_dir = session / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "state.json").write_text('{"gates": {}}', encoding="utf-8")
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False


def test_session_filter_limits_report(tmp_path):
    first = _session_uuid(tmp_path, "session-a")
    second = _session_uuid(tmp_path, "session-b")
    _write_state(first, "00", "COMPLETED", {"H00": {}})
    _write_state(second, "00", "ABORT", {})
    report = des.determine(tmp_path, session_filter="session-a")
    assert [e["session"] for e in report["executions"]] == ["session-a"]
    assert report["summary"]["total"] == 1


def test_multiple_iterations_report_in_numeric_order(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(tmp_path)
    assert [e["iteration"] for e in report["executions"]] == ["00", "01"]
    assert report["summary"] == {"total": 2, "determined": 2, "undetermined": 0}


def test_protocol_version_reported_from_session_log(tmp_path):
    session = tmp_path / ".project" / "uuid-version"
    _write_session_log(session, "10.3.0")
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["protocol_version"] == "10.3.0"


def test_cli_prints_json_report(tmp_path, capsys):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    assert des.main(["--root", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert report["summary"] == {"total": 1, "determined": 1, "undetermined": 0}


def test_iteration_query_returns_only_the_requested_execution(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="00"
    )
    assert [e["iteration"] for e in report["executions"]] == ["00"]
    assert report["summary"] == {"total": 1, "determined": 1, "undetermined": 0}
    entry = report["executions"][0]
    assert entry["session"] == session.name
    assert entry["determined"] is True
    assert entry["terminal_task_state"] == "COMPLETED"


def test_iteration_query_distinguishes_same_iteration_across_sessions(tmp_path):
    first = _session_uuid(tmp_path, "session-a")
    second = _session_uuid(tmp_path, "session-b")
    _write_state(first, "00", "COMPLETED", {"H00": {}})
    _write_state(second, "00", "ABORT", {})
    report = des.determine(
        tmp_path, session_filter="session-a", iteration_filter="00"
    )
    assert [e["session"] for e in report["executions"]] == ["session-a"]
    assert report["executions"][0]["terminal_task_state"] == "COMPLETED"


def test_iteration_query_non_terminal_execution_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "in_progress", {})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="00"
    )
    assert len(report["executions"]) == 1
    entry = report["executions"][0]
    assert entry["determined"] is False
    assert entry["reason"] == "status_not_terminal"
    assert report["summary"] == {"total": 1, "determined": 0, "undetermined": 1}


def test_iteration_query_missing_state_json_is_fail_closed(tmp_path):
    session = _session_uuid(tmp_path)
    (session / "00").mkdir()
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="00"
    )
    assert len(report["executions"]) == 1
    entry = report["executions"][0]
    assert entry["state_json"] == "missing"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_missing"


def test_iteration_query_corrupt_state_json_is_fail_closed(tmp_path):
    session = _session_uuid(tmp_path)
    iter_dir = session / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "state.json").write_text("{not json", encoding="utf-8")
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="00"
    )
    assert len(report["executions"]) == 1
    entry = report["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_corrupt"


def test_iteration_query_nonexistent_iteration_is_empty(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="99"
    )
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_iteration_query_unknown_session_is_empty(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    report = des.determine(
        tmp_path, session_filter="unknown-session", iteration_filter="00"
    )
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_iteration_without_session_fails_deterministically(tmp_path):
    with pytest.raises(SystemExit) as excinfo:
        des.main(["--root", str(tmp_path), "--iteration", "00"])
    assert excinfo.value.code == 2


def test_full_session_query_keeps_reporting_all_iterations(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(tmp_path, session_filter=session.name)
    assert [e["iteration"] for e in report["executions"]] == ["00", "01"]
    assert report["summary"] == {"total": 2, "determined": 2, "undetermined": 0}
