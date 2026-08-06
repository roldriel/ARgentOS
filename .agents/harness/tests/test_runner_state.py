"""Tests for runner_state.py (protocol state persistence).

`state.json` is the single source of truth for hook enforcement: written
transactionally by the runner after each gate PASS, and fail-closed for
consumers (missing or corrupt means no gate has passed).
"""

import json
import os
import time
import uuid
from pathlib import Path

import pytest

import runner_paths
import runner_state
from runner_validators import run_trigger


@pytest.fixture
def session(tmp_path, monkeypatch):
    """Temporary session under a throwaway artifacts dir and project root."""
    session_uuid = f"test-{uuid.uuid4()}"
    artifacts_dir = tmp_path / ".project"
    (artifacts_dir / session_uuid / "00").mkdir(parents=True)
    monkeypatch.setattr(runner_paths, "ARTIFACTS_DIR", artifacts_dir)
    monkeypatch.setattr(runner_paths, "PROJECT_ROOT", tmp_path)
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


def test_run_trigger_pass_updates_state_json(session):
    session_uuid, artifacts_dir, _ = session
    # H10 is optional and has no required artifact sections; a PASS without a
    # real artifact flow keeps this test focused on the state integration.
    # Instead, use H00 with a minimal valid TASK_ANALYSIS.md.
    iter_dir = artifacts_dir / session_uuid / "00"
    (iter_dir / "01-TASK_ANALYSIS.md").write_text(
        "# Task Analysis\n\n"
        "## Metadata\n\n```toml\nid = \"TA-1\"\n```\n\n"
        "## User Request\n\n```toml\noriginal_request = \"x\"\n```\n\n"
        "## Interpreted Objective\n\n```toml\n[objective]\ndescription = \"x\"\n```\n\n"
        "## Expected Outcome\n\n```toml\n[expected_outcome]\ndescription = \"x\"\n```\n\n"
        "## Explicit Requirements\n\n```toml\nrequirements = []\n```\n\n"
        "## Explicit Restrictions\n\n```toml\nrestrictions = []\n```\n\n"
        "## Detected Ambiguities\n\nNone.\n\n"
        "## Intent Confidence Assessment\n\n```toml\n[intent_confidence]\nlevel = \"HIGH\"\n```\n\n"
        "## Sufficiency Assessment\n\n```toml\n[sufficiency]\nready_for_specification = true\n```\n\n"
        "## Recommended Next State\n\n```toml\nrecommended_next_state = \"BUILDING_TASK_SPECIFICATION\"\n```\n\n"
        "## Confidence\n\n```toml\n[confidence]\nlevel = \"HIGH\"\n```\n\n"
        "## Task Profile\n\n```toml\n[task_profile]\nvalue = \"standard\"\n```\n",
        encoding="utf-8",
    )

    result = run_trigger(session_uuid, "H00", "00")

    assert result.result == "PASS"
    state = runner_state.load_state(session_uuid, "00")
    assert runner_state.gate_passed(state, "H00")
    assert state["task_profile"] == "standard"


def test_run_trigger_fail_does_not_touch_state_json(session):
    session_uuid, artifacts_dir, _ = session

    result = run_trigger(session_uuid, "H01", "00")  # artifact missing -> FAIL

    assert result.result == "FAIL"
    assert not (artifacts_dir / session_uuid / "00" / "state.json").exists()


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
