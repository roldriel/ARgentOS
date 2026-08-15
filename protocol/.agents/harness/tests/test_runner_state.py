"""Tests for runner_state.py (protocol state persistence).

`state.json` is the single source of truth for hook enforcement: written
transactionally by runner_state (the only writer) after the Orchestrator
judges a gate PASS in prose, and fail-closed for consumers (missing or
corrupt means no gate has passed).
"""

import json
import os
import time
import uuid
from pathlib import Path

import pytest

import runner_state


@pytest.fixture
def session(tmp_path, monkeypatch):
    """Temporary session under a throwaway artifacts dir and project root."""
    session_uuid = f"test-{uuid.uuid4()}"
    artifacts_dir = tmp_path / ".project"
    (artifacts_dir / session_uuid / "00").mkdir(parents=True)
    monkeypatch.setattr(runner_state, "ARTIFACTS_DIR", artifacts_dir)
    monkeypatch.setattr(runner_state, "PROJECT_ROOT", tmp_path)
    return session_uuid, artifacts_dir, tmp_path


def test_record_gate_pass_writes_state_with_expected_fields(session):
    session_uuid, artifacts_dir, _ = session

    path = runner_state.record_gate_pass(session_uuid, "00", "H04")

    state = json.loads(path.read_text(encoding="utf-8"))
    assert path == artifacts_dir / session_uuid / "00" / "state.json"
    assert state["session"] == session_uuid
    assert state["iteration"] == "00"
    assert state["task_profile"] == "standard"  # no TASK_ANALYSIS -> default
    assert state["gates"]["H04"]["result"] == "PASS"
    assert state["gates"]["H04"]["timestamp"]
    assert state["last_gate"] == "H04"
    assert state["status"] == "in_progress"
    assert state["updated"]


def test_record_gate_pass_is_transactional_and_cumulative(session):
    session_uuid, artifacts_dir, _ = session

    runner_state.record_gate_pass(session_uuid, "00", "H00")
    runner_state.record_gate_pass(session_uuid, "00", "H04")

    iter_dir = artifacts_dir / session_uuid / "00"
    leftovers = [p.name for p in iter_dir.iterdir() if p.name != "state.json"]
    assert leftovers == [], "no temp files may survive the rename"

    state = runner_state.load_state(session_uuid, "00")
    assert set(state["gates"]) == {"H00", "H04"}
    assert state["last_gate"] == "H04"


def test_record_terminal_state_preserves_gates(session):
    session_uuid, artifacts_dir, _ = session
    runner_state.record_gate_pass(session_uuid, "00", "H04")

    path = runner_state.record_terminal_state(session_uuid, "00", "ABORT")

    state = json.loads(path.read_text(encoding="utf-8"))
    assert state["status"] == "ABORT"
    assert state["gates"]["H04"]["result"] == "PASS"
    assert state["updated"]


def test_record_terminal_state_rejects_unknown_state(session):
    session_uuid, _, _ = session

    with pytest.raises(ValueError):
        runner_state.record_terminal_state(session_uuid, "00", "BOGUS")


def test_cli_terminal_records_state(session, capsys):
    session_uuid, artifacts_dir, _ = session
    runner_state.record_gate_pass(session_uuid, "00", "H04")

    exit_code = runner_state.main(
        ["--session", session_uuid, "--state", "ABORT", "terminal"]
    )

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "ABORT" in out
    state = runner_state.load_state(session_uuid, "00")
    assert state["status"] == "ABORT"
    assert runner_state.gate_passed(state, "H04")


def test_cli_terminal_rejects_invalid_state(session, capsys):
    session_uuid, _, _ = session

    exit_code = runner_state.main(
        ["--session", session_uuid, "--state", "BOGUS", "terminal"]
    )

    assert exit_code == 2
    assert "ABORT" in capsys.readouterr().err


def test_read_task_profile_from_latest_iteration(session):
    session_uuid, artifacts_dir, _ = session
    iter00 = artifacts_dir / session_uuid / "00"
    (iter00 / "01-TASK_ANALYSIS.md").write_text(
        "## Task Profile\n\n```toml\n[task_profile]\nvalue = \"trivial\"\n```\n",
        encoding="utf-8",
    )
    iter01 = artifacts_dir / session_uuid / "01"
    iter01.mkdir()
    (iter01 / "TASK_ANALYSIS.md").write_text(
        "## Task Profile\n\n```toml\n[task_profile]\nvalue = \"complex\"\n```\n",
        encoding="utf-8",
    )

    assert runner_state.read_task_profile(session_uuid) == "complex"


def test_read_task_profile_defaults_to_standard(session):
    session_uuid, artifacts_dir, _ = session
    iter00 = artifacts_dir / session_uuid / "00"
    (iter00 / "TASK_ANALYSIS.md").write_text(
        "## Task Profile\n\n```toml\n[task_profile]\nvalue = \"bogus\"\n```\n",
        encoding="utf-8",
    )

    assert runner_state.read_task_profile(session_uuid) == "standard"


def test_missing_state_is_fail_closed(session):
    session_uuid, _, _ = session

    state = runner_state.load_state(session_uuid, "00")

    assert state["gates"] == {}
    assert state["status"] == "no_gates_passed"
    assert not runner_state.gate_passed(state, "H04")


def test_corrupt_state_is_fail_closed(session):
    session_uuid, artifacts_dir, _ = session
    path = artifacts_dir / session_uuid / "00" / "state.json"
    path.write_text("{ not json", encoding="utf-8")

    state = runner_state.load_state(session_uuid, "00")
    assert state["gates"] == {}
    assert not runner_state.gate_passed(state, "H04")

    path.write_text('{"gates": "not-a-dict"}', encoding="utf-8")
    state = runner_state.load_state(session_uuid, "00")
    assert state["gates"] == {}


def test_detect_bypass_flags_files_modified_before_plan_pass(session):
    session_uuid, artifacts_dir, project_root = session
    now = time.time()
    session_dir = artifacts_dir / session_uuid
    old = now - 120
    for path in (session_dir, session_dir / "00"):
        os.utime(path, (old, old))

    suspect = project_root / "deliverable.py"
    suspect.write_text("x = 1\n", encoding="utf-8")
    os.utime(suspect, (now - 10, now - 10))
    after = project_root / "after.py"
    after.write_text("x = 2\n", encoding="utf-8")
    os.utime(after, (now + 10, now + 10))
    protocol_file = artifacts_dir / session_uuid / "00" / "notes.md"
    protocol_file.write_text("notes\n", encoding="utf-8")
    os.utime(protocol_file, (now - 10, now - 10))

    gate_ts = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now))
    suspects = runner_state.detect_bypass(session_uuid, "00", gate_ts)

    assert "deliverable.py" in suspects
    assert "after.py" not in suspects
    assert not any("notes.md" in s for s in suspects)


def test_cli_pass_records_state(session, capsys):
    session_uuid, artifacts_dir, _ = session

    exit_code = runner_state.main(
        ["--session", session_uuid, "--trigger", "H04", "pass"]
    )

    assert exit_code == 0
    out = capsys.readouterr().out
    state_path = artifacts_dir / session_uuid / "00" / "state.json"
    assert str(state_path) in out
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["gates"]["H04"]["result"] == "PASS"


def test_cli_pass_with_explicit_iteration(session, capsys):
    session_uuid, artifacts_dir, _ = session
    (artifacts_dir / session_uuid / "01").mkdir()

    exit_code = runner_state.main(
        ["--session", session_uuid, "--trigger", "H00",
         "--iteration", "01", "pass"]
    )

    assert exit_code == 0
    state = runner_state.load_state(session_uuid, "01")
    assert runner_state.gate_passed(state, "H00")


def test_cli_h04_bypass_alert_does_not_block(session, capsys):
    session_uuid, artifacts_dir, project_root = session
    now = time.time()
    session_dir = artifacts_dir / session_uuid
    old = now - 120
    for path in (session_dir, session_dir / "00"):
        os.utime(path, (old, old))
    suspect = project_root / "deliverable.py"
    suspect.write_text("x = 1\n", encoding="utf-8")
    os.utime(suspect, (now - 10, now - 10))

    exit_code = runner_state.main(
        ["--session", session_uuid, "--trigger", "H04", "pass"]
    )

    # The CLI used "now" as the gate timestamp; the suspect file sits inside
    # the [session start, gate PASS] window, so the alert fires on stderr
    # while the exit code stays 0 (non-blocking).
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "BYPASS ALERT" in captured.err
    assert "deliverable.py" in captured.err


def test_cli_missing_session_exits_2(session, capsys):
    _, artifacts_dir, _ = session

    exit_code = runner_state.main(
        ["--session", "no-such-session", "--trigger", "H04", "pass"]
    )

    assert exit_code == 2
    assert "session not found" in capsys.readouterr().err


def test_cli_missing_iteration_exits_2(session, capsys):
    session_uuid, _, _ = session

    exit_code = runner_state.main(
        ["--session", session_uuid, "--trigger", "H04",
         "--iteration", "07", "pass"]
    )

    assert exit_code == 2
    assert "iteration folder not found" in capsys.readouterr().err


def test_cli_invalid_iteration_exits_2(session, capsys):
    session_uuid, _, _ = session

    exit_code = runner_state.main(
        ["--session", session_uuid, "--trigger", "H04",
         "--iteration", "abc", "pass"]
    )

    assert exit_code == 2
    assert "invalid iteration" in capsys.readouterr().err


# --- CLI session linking (P4.2) ----------------------------------------------


def test_link_session_persists(session):
    session_uuid, artifacts_dir, _ = session
    runner_state.link_session("cli-y", session_uuid)
    mapping = json.loads(
        (artifacts_dir / ".sessions.json").read_text(encoding="utf-8")
    )
    assert mapping["cli-y"] == session_uuid


def test_cli_link_writes_mapping(session, capsys):
    session_uuid, artifacts_dir, _ = session
    exit_code = runner_state.main(
        ["--session", session_uuid, "--cli-session", "cli-x", "link"]
    )
    assert exit_code == 0
    mapping = json.loads(
        (artifacts_dir / ".sessions.json").read_text(encoding="utf-8")
    )
    assert mapping["cli-x"] == session_uuid


def test_cli_link_requires_cli_session(session, capsys):
    session_uuid, _, _ = session
    exit_code = runner_state.main(["--session", session_uuid, "link"])
    assert exit_code == 2
    assert "--cli-session" in capsys.readouterr().err


# --- H15 schema support (B-6) ------------------------------------------------


def valid_delegation() -> dict:
    return {
        "session_uuid": "u",
        "current_state": "EXECUTING",
        "target_phase": "orchestrators/core/workflow/06-execute.md",
        "role_to_adopt": "worker",
        "input_artifacts": ["a.md"],
        "harness_policy": "H05-execution-completed.md",
        "task_summary": "x",
    }


def test_validate_delegation_valid(tmp_path, capsys):
    f = tmp_path / "delegation.json"
    f.write_text(json.dumps(valid_delegation()), encoding="utf-8")
    assert runner_state.main(["--input", str(f), "validate-delegation"]) == 0
    assert "PASS" in capsys.readouterr().out


def test_validate_delegation_missing_field(tmp_path, capsys):
    f = tmp_path / "delegation.json"
    f.write_text('{"session_uuid": "u"}', encoding="utf-8")
    assert runner_state.main(["--input", str(f), "validate-delegation"]) == 2
    out = capsys.readouterr().out
    assert "FAIL" in out and "missing required field" in out


def test_validate_delegation_bad_profile(tmp_path, capsys):
    payload = valid_delegation()
    payload["profile"] = "bogus"
    f = tmp_path / "delegation.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    assert runner_state.main(["--input", str(f), "validate-delegation"]) == 2
    assert "invalid profile" in capsys.readouterr().out


def test_validate_delegation_bad_budget(tmp_path, capsys):
    payload = valid_delegation()
    payload["context_budget"] = -1
    f = tmp_path / "delegation.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    assert runner_state.main(["--input", str(f), "validate-delegation"]) == 2
    assert "context_budget" in capsys.readouterr().out


def valid_return() -> dict:
    return {
        "output_artifact": "a.md",
        "role_executed": "executor",
        "profile_executed": None,
        "phase_completed": "06",
        "summary": "s",
        "blockers": [],
        "deviations": ["deviation: note"],
    }


def test_validate_return_valid(tmp_path, capsys):
    f = tmp_path / "return.json"
    f.write_text(json.dumps(valid_return()), encoding="utf-8")
    assert runner_state.main(["--input", str(f), "validate-return"]) == 0
    assert "PASS" in capsys.readouterr().out


def test_validate_return_bad_deviation_prefix(tmp_path, capsys):
    report = valid_return()
    report["deviations"] = ["note without class"]
    f = tmp_path / "return.json"
    f.write_text(json.dumps(report), encoding="utf-8")
    assert runner_state.main(["--input", str(f), "validate-return"]) == 2
    assert "without class prefix" in capsys.readouterr().out


def test_validate_requires_input(tmp_path, capsys):
    assert runner_state.main(["validate-delegation"]) == 2
    assert "--input" in capsys.readouterr().err
