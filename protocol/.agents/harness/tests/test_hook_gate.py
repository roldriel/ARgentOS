"""Tests for hook_gate.py (shared CLI lifecycle hook).

The hook decides allow (exit 0) / deny (exit 2) from a JSON event, reading
only the iteration state.json written by runner_state. Malformed input is
fail-open allow — a documented property, verified here via a real subprocess.
"""

import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

import hook_gate

PROJECT_ROOT = Path(__file__).resolve().parents[3]
HOOK_PATH = PROJECT_ROOT / ".agents" / "harness" / "hook_gate.py"


@pytest.fixture
def project(tmp_path, monkeypatch):
    """Isolated project root with a session the hook can resolve."""
    session_uuid = f"test-{uuid.uuid4()}"
    project_dir = tmp_path / ".project"
    iter_dir = project_dir / session_uuid / "00"
    iter_dir.mkdir(parents=True)
    monkeypatch.setattr(hook_gate, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(hook_gate, "PROJECT_DIR", project_dir)
    return session_uuid, project_dir, tmp_path


def write_state(project_dir, session_uuid, gates, status="in_progress"):
    state = {
        "session": session_uuid,
        "iteration": "00",
        "task_profile": "standard",
        "gates": {
            gate: {"result": "PASS", "timestamp": "2026-08-06T00:00:00+00:00"}
            for gate in gates
        },
        "last_gate": gates[-1] if gates else None,
        "status": status,
        "updated": "2026-08-06T00:00:00+00:00",
    }
    (project_dir / session_uuid / "00" / "state.json").write_text(
        json.dumps(state), encoding="utf-8"
    )


def pre_tool_use(tool="Write", file_path="src/app.py", session_uuid=""):
    return {
        "hook_event_name": "PreToolUse",
        "session_id": session_uuid,
        "cwd": ".",
        "tool_name": tool,
        "tool_input": {"file_path": file_path},
    }


def stop_event(session_uuid=""):
    return {"hook_event_name": "Stop", "session_id": session_uuid, "cwd": "."}


# --- Rule 1: not a deliverable -> allow -----------------------------------


def test_non_write_tool_is_allowed(project):
    session_uuid, _, _ = project
    assert hook_gate.decide(pre_tool_use(tool="Read")) == 0
    assert hook_gate.decide(pre_tool_use(tool="Bash")) == 0


def test_writes_inside_protocol_dirs_are_allowed(project):
    session_uuid, _, _ = project
    event = pre_tool_use(file_path=".project/x/00/TASK_ANALYSIS.md")
    assert hook_gate.decide(event) == 0
    event = pre_tool_use(tool="Edit", file_path=".agents/harness/INDEX.md")
    assert hook_gate.decide(event) == 0


def test_write_without_target_is_denied(project, capsys):
    session_uuid, _, _ = project
    event = pre_tool_use(file_path=None)
    code = hook_gate.decide(event)
    assert code == 2
    assert "identifiable target" in capsys.readouterr().err


def test_write_with_empty_tool_input_is_denied(project):
    session_uuid, _, _ = project
    event = {
        "hook_event_name": "PreToolUse",
        "session_id": session_uuid,
        "cwd": ".",
        "tool_name": "Write",
        "tool_input": {},
    }
    assert hook_gate.decide(event) == 2


def test_write_without_tool_input_stays_fail_open(project):
    session_uuid, _, _ = project
    event = {
        "hook_event_name": "PreToolUse",
        "session_id": session_uuid,
        "cwd": ".",
        "tool_name": "Write",
    }
    assert hook_gate.decide(event) == 0


def test_other_events_are_allowed(project):
    assert hook_gate.decide({"hook_event_name": "SessionStart"}) == 0


# --- Rule 2: PreToolUse on deliverable without H04 PASS -> deny ------------


def test_deliverable_write_without_h04_is_denied(project, capsys):
    session_uuid, project_dir, _ = project
    write_state(project_dir, session_uuid, ["H00"])

    code = hook_gate.decide(pre_tool_use(session_uuid=session_uuid))

    assert code == 2
    err = capsys.readouterr().err
    assert "H04" in err
    assert "Gate Checklist" in err
    assert "python .agents/harness/runner_state.py" in err


def test_deliverable_write_without_any_session_is_denied(project, capsys):
    session_uuid, project_dir, _ = project
    for child in sorted(project_dir.iterdir()):
        if child.is_dir():
            for p in sorted(child.rglob("*"), reverse=True):
                p.rmdir() if p.is_dir() else p.unlink()
            child.rmdir()

    assert hook_gate.decide(pre_tool_use()) == 2


def test_deliverable_write_with_h04_pass_is_allowed(project):
    session_uuid, project_dir, _ = project
    write_state(project_dir, session_uuid, ["H00", "H04"])

    assert hook_gate.decide(pre_tool_use(session_uuid=session_uuid)) == 0


def test_corrupt_state_is_fail_closed_for_pretooluse(project, capsys):
    session_uuid, project_dir, _ = project
    (project_dir / session_uuid / "00" / "state.json").write_text(
        "{ corrupt", encoding="utf-8"
    )

    assert hook_gate.decide(pre_tool_use(session_uuid=session_uuid)) == 2


# --- Rule 3: Stop without iteration closure -> deny ------------------------


def test_stop_without_task_started_is_allowed(project):
    session_uuid, project_dir, _ = project
    # Session dir exists but no state.json: no task started.
    assert hook_gate.decide(stop_event(session_uuid)) == 0


def test_stop_without_h06_is_denied(project, capsys):
    session_uuid, project_dir, _ = project
    write_state(project_dir, session_uuid, ["H00", "H04"])

    code = hook_gate.decide(stop_event(session_uuid))

    assert code == 2
    err = capsys.readouterr().err
    assert "H06" in err
    assert "Gate Checklist" in err
    assert "python .agents/harness/runner_state.py" in err


def test_stop_with_h06_pass_is_allowed(project):
    session_uuid, project_dir, _ = project
    write_state(project_dir, session_uuid, ["H04", "H06"])

    assert hook_gate.decide(stop_event(session_uuid)) == 0


def test_stop_with_needs_clarification_recorded_is_allowed(project):
    session_uuid, project_dir, _ = project
    write_state(project_dir, session_uuid, ["H00"])
    (project_dir / session_uuid / "00" / "01-TASK_ANALYSIS.md").write_text(
        "# Task Analysis\n\n"
        "## Recommended Next State\n\n"
        "```toml\nrecommended_next_state = \"NEEDS_CLARIFICATION\"\n```\n",
        encoding="utf-8",
    )

    assert hook_gate.decide(stop_event(session_uuid)) == 0


def test_stop_with_abort_terminal_status_is_allowed(project):
    session_uuid, project_dir, _ = project
    write_state(project_dir, session_uuid, ["H00", "H04"], status="ABORT")

    assert hook_gate.decide(stop_event(session_uuid)) == 0


def test_stop_with_completed_terminal_status_is_allowed(project):
    session_uuid, project_dir, _ = project
    write_state(project_dir, session_uuid, ["H04", "H06"], status="COMPLETED")

    assert hook_gate.decide(stop_event(session_uuid)) == 0


def test_stop_with_abort_only_as_gate_name_is_denied(project, capsys):
    session_uuid, project_dir, _ = project
    # A gate named H09 does not close the iteration; only a terminal status
    # in state.json does.
    write_state(project_dir, session_uuid, ["H00", "H04", "H09"])

    code = hook_gate.decide(stop_event(session_uuid))

    assert code == 2
    assert "H06" in capsys.readouterr().err


# --- Fail-open on malformed input (documented property) ---------------------


def test_malformed_stdin_is_fail_open_allow():
    result = subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input="{ not json",
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        env=os.environ.copy(),
    )
    # Documented fail-open: a hook that cannot parse its event must allow.
    assert result.returncode == 0


# --- Session mapping (deterministic resolution, P4.2) -----------------------


def test_mapping_locks_cli_session_to_protocol_session(project):
    session_uuid, project_dir, _ = project
    event = pre_tool_use(session_uuid="cli-1")
    first = hook_gate._resolve_session(event)
    assert first is not None and first.name == session_uuid

    # A newer session appears afterwards: the mapping must keep the CLI
    # session bound to the original protocol session.
    second_dir = project_dir / "second"
    (second_dir / "00").mkdir(parents=True)
    future = time.time() + 1000
    os.utime(second_dir, (future, future))

    again = hook_gate._resolve_session(event)
    assert again is not None and again.name == session_uuid

    mapping = json.loads((project_dir / ".sessions.json").read_text(encoding="utf-8"))
    assert mapping["cli-1"] == session_uuid


def test_unmapped_cli_session_uses_most_recent(project):
    session_uuid, project_dir, _ = project
    other = project_dir / "other"
    (other / "00").mkdir(parents=True)
    future = time.time() + 2000
    os.utime(other, (future, future))

    resolved = hook_gate._resolve_session(pre_tool_use(session_uuid="cli-2"))
    assert resolved is not None and resolved.name == "other"

    mapping = json.loads((project_dir / ".sessions.json").read_text(encoding="utf-8"))
    assert mapping["cli-2"] == "other"
