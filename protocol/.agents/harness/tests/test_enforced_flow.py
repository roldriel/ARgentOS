"""End-to-end integration test of the enforced mode (RFC-47, plan 46).

Copies the two enforced-mode scripts into a scratch adoption layout
(`.agents/harness/` at a project root) and exercises the real flow through
subprocesses, exactly as an adopting CLI would:

1. No state.json -> the hook denies PreToolUse on a project deliverable.
2. runner_state records the H04 (plan) PASS -> the hook allows the write.
3. Stop without iteration closure -> deny; after H06 PASS -> allow.
4. A project file modified before the H04 PASS triggers the post-hoc
   bypass-scan alert on stderr when H04 is recorded.

Evidence: this suite IS the dogfooding evidence of the enforced flow; the
execution note lives in `plans/46-enforced-mode-dogfooding.md`.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

HARNESS = Path(__file__).resolve().parents[1]
RUNNER = HARNESS / "runner_state.py"
HOOK = HARNESS / "hook_gate.py"


@pytest.fixture()
def adopted_project(tmp_path: Path) -> Path:
    """A scratch project with the adopted layout and the two scripts in it."""
    harness_dir = tmp_path / ".agents" / "harness"
    harness_dir.mkdir(parents=True)
    shutil.copy(RUNNER, harness_dir / "runner_state.py")
    shutil.copy(HOOK, harness_dir / "hook_gate.py")
    (tmp_path / ".project").mkdir()
    return tmp_path


def run_runner(project: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(project / ".agents/harness/runner_state.py"),
         *args],
        capture_output=True, text=True, cwd=project,
    )


def run_hook(project: Path, event: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(project / ".agents/harness/hook_gate.py")],
        input=json.dumps(event),
        capture_output=True, text=True, cwd=project,
    )


def write_event(project: Path, session: str, target: str) -> dict:
    return {
        "session_id": session,
        "cwd": str(project),
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": str(project / target)},
    }


def stop_event(project: Path, session: str) -> dict:
    return {
        "session_id": session,
        "cwd": str(project),
        "hook_event_name": "Stop",
        "tool_name": "Stop",
        "tool_input": {},
    }


def test_full_enforced_flow(adopted_project):
    project = adopted_project
    session = str(uuid.uuid4())
    iteration = "00"
    iter_dir = project / ".project" / session / iteration
    iter_dir.mkdir(parents=True)

    # 1. No state.json yet: the write to a deliverable is denied.
    event = write_event(project, session, "src/app.py")
    res = run_hook(project, event)
    assert res.returncode == 2, res.stderr

    # 2. A write inside .project/ is not a deliverable: allowed even now.
    res = run_hook(
        project, write_event(project, session, ".project/notes.md")
    )
    assert res.returncode == 0, res.stderr

    # 3. Record the H04 (plan approved) PASS via the CLI: state.json exists.
    res = run_runner(
        project, "--session", session, "--trigger", "H04",
        "--iteration", iteration, "pass",
    )
    assert res.returncode == 0, res.stderr
    state = json.loads((iter_dir / "state.json").read_text(encoding="utf-8"))
    assert state["gates"]["H04"]["result"] == "PASS"
    assert state["status"] == "in_progress"

    # 4. The same write is now allowed.
    res = run_hook(project, event)
    assert res.returncode == 0, res.stderr

    # 5. Stop before closure (H06) is denied.
    res = run_hook(project, stop_event(project, session))
    assert res.returncode == 2, res.stderr

    # 6. Record the H06 (verification) PASS: Stop is allowed.
    res = run_runner(
        project, "--session", session, "--trigger", "H06",
        "--iteration", iteration, "pass",
    )
    assert res.returncode == 0, res.stderr
    res = run_hook(project, stop_event(project, session))
    assert res.returncode == 0, res.stderr


def test_bypass_scan_alerts_on_pre_pass_modification(adopted_project):
    project = adopted_project
    session = str(uuid.uuid4())
    iter_dir = project / ".project" / session / "00"
    iter_dir.mkdir(parents=True)
    (project / "src").mkdir()
    (project / "src" / "sneaky.py").write_text("# modified before H04\n")

    res = run_runner(
        project, "--session", session, "--trigger", "H04", "pass",
    )
    assert res.returncode == 0, res.stderr
    assert "sneaky.py" in res.stderr or "bypass" in res.stderr.lower()


def test_terminal_state_allows_stop(adopted_project):
    project = adopted_project
    session = str(uuid.uuid4())
    (project / ".project" / session / "00").mkdir(parents=True)

    res = run_runner(
        project, "--session", session, "--state", "COMPLETED", "terminal",
    )
    assert res.returncode == 0, res.stderr
    res = run_hook(project, stop_event(project, session))
    assert res.returncode == 0, res.stderr
