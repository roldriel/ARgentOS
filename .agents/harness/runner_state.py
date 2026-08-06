"""Protocol state persistence for the harness runner.

`state.json` (`.project/<session-uuid>/<iteration>/state.json`) is the single
source of truth for the protocol state of an iteration. Only the runner writes
it, transactionally (temp file + rename), after each gate PASS. Consumers (the
`hook_gate.py` lifecycle hook, the Orchestrator) read it; a missing or corrupt
`state.json` means *no gate has passed* (fail-closed for consumers).

Layout:

```json
{
  "session": "<uuid>",
  "iteration": "00",
  "task_profile": "standard",
  "gates": {"H04": {"result": "PASS", "timestamp": "..."}},
  "last_gate": "H04",
  "status": "in_progress",
  "updated": "<ISO-8601>"
}
```
"""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import json
import os
import tempfile
from datetime import datetime, timezone
from typing import Any

import runner_paths
import runner_profiles
from runner_artifacts import iteration_dirs

# Directories that never count as project deliverables for the post-hoc
# bypass scan (protocol internals, VCS, caches, dependency folders).
_BYPASS_SCAN_EXCLUDED_DIRS = {
    ".agents",
    ".git",
    ".project",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
}

_BYPASS_SCAN_MAX_FILES = 20


def state_path(session_uuid: str, iteration: str) -> Path:
    """Return the state.json path for a session iteration."""
    return runner_paths.ARTIFACTS_DIR / session_uuid / iteration / "state.json"


def empty_state(session_uuid: str, iteration: str) -> dict[str, Any]:
    """Return the canonical empty state: no gate has passed."""
    return {
        "session": session_uuid,
        "iteration": iteration,
        "task_profile": None,
        "gates": {},
        "last_gate": None,
        "status": "no_gates_passed",
        "updated": None,
    }


def load_state(session_uuid: str, iteration: str) -> dict[str, Any]:
    """Load state.json; a missing or corrupt file yields the empty state.

    Fail-closed for consumers: any read/parse problem is indistinguishable
    from "no gate has passed".
    """
    path = state_path(session_uuid, iteration)
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return empty_state(session_uuid, iteration)
    if not isinstance(state, dict) or not isinstance(state.get("gates"), dict):
        return empty_state(session_uuid, iteration)
    return state


def gate_passed(state: dict[str, Any], trigger: str) -> bool:
    """Return True when the state records a PASS for the given trigger."""
    entry = state.get("gates", {}).get(trigger)
    return isinstance(entry, dict) and entry.get("result") == "PASS"


def record_gate_pass(
    session_uuid: str, iteration: str, trigger: str, timestamp: str | None = None
) -> Path:
    """Record a gate PASS in state.json with a transactional write.

    The update is read-modify-write over the current state (tolerating a
    missing/corrupt file as the empty state) and is persisted via a temp
    file plus atomic rename, so readers never observe a partial file.
    """
    state = load_state(session_uuid, iteration)
    now = timestamp or datetime.now(timezone.utc).isoformat()
    state["session"] = session_uuid
    state["iteration"] = iteration
    try:
        state["task_profile"] = runner_profiles.read_task_profile(session_uuid)
    except Exception:
        # The profile is advisory metadata in state.json; never let its
        # resolution break the state update of a gate that already passed.
        state["task_profile"] = state.get("task_profile")
    state["gates"][trigger] = {"result": "PASS", "timestamp": now}
    state["last_gate"] = trigger
    state["status"] = "in_progress"
    state["updated"] = now

    path = state_path(session_uuid, iteration)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=".state.json.", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2)
            handle.write("\n")
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return path


def detect_bypass(
    session_uuid: str, iteration: str, gate_timestamp: str
) -> list[str]:
    """Post-hoc bypass scan run when the plan gate (H04) passes.

    Returns paths of would-be deliverables (project files outside the
    protocol and cache directories) modified after the session directory was
    created but before the H04 PASS timestamp: writes that happened during a
    window where no plan was approved — e.g. while the enforcement hook was
    fail-open (crash/timeout) or not installed (declarative mode). The result
    is an audit alert, never a gate failure.
    """
    try:
        gate_dt = datetime.fromisoformat(gate_timestamp)
    except ValueError:
        return []
    session_dir = runner_paths.ARTIFACTS_DIR / session_uuid
    try:
        window_start = session_dir.stat().st_mtime
    except OSError:
        return []
    suspects: list[str] = []
    root = runner_paths.PROJECT_ROOT
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if d not in _BYPASS_SCAN_EXCLUDED_DIRS
        ]
        for name in filenames:
            path = Path(dirpath) / name
            try:
                mtime = path.stat().st_mtime
            except OSError:
                continue
            if window_start <= mtime <= gate_dt.timestamp():
                suspects.append(str(path.relative_to(root)))
                if len(suspects) >= _BYPASS_SCAN_MAX_FILES:
                    return suspects
    return suspects


def latest_iteration(session_uuid: str) -> str:
    """Return the latest iteration folder name for a session (default 00)."""
    dirs = iteration_dirs(session_uuid)
    return dirs[-1].name if dirs else "00"
