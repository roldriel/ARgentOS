#!/usr/bin/env python3
"""Shared lifecycle hook for CLI-level enforcement of the .agents protocol.

Reads one hook event as JSON from stdin (Kimi Code / Claude Code format:
`session_id`, `cwd`, `hook_event_name`, `tool_name`, `tool_input`) and
decides allow/deny against the iteration state written by runner_state
(`.project/<session-uuid>/<iteration>/state.json`).

Decision (in order):

1. The tool call does not touch a project deliverable (not a
   ``PreToolUse`` on ``Write``/``Edit``, or the target path lives inside
   ``.project/`` / ``.agents/``) -> allow (exit 0).
2. ``PreToolUse`` on ``Write``/``Edit`` whose ``tool_input`` is a dict that
   names no target (``file_path``/``path``/``filename``) -> deny (exit 2);
   a missing ``tool_input`` remains fail-open (missing-field property).
3. ``PreToolUse`` on ``Write``/``Edit`` targeting a deliverable without a
   current H04 (plan) PASS in state.json -> deny (exit 2) with a recovery
   instruction on stderr.
4. ``Stop`` without iteration closure (H06 PASS, NEEDS_CLARIFICATION
   recorded in TASK_ANALYSIS.md, a terminal status (ABORT/COMPLETED)
   recorded in state.json, or no task started in the session) -> deny
   (exit 2) with a recovery instruction on stderr.

Fail-open honesty: malformed stdin, missing event fields, or any internal
error resolve to allow (exit 0). A crash or a CLI-side timeout of this
script also means allow — hook enforcement protects against agent
omission, not against the hook itself failing. Post-hoc detection
compensates: runner_state.detect_bypass runs when the runner_state CLI
records the H04 gate.

Usage (CLI hook configuration): ``python .agents/harness/hook_gate.py``
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_DIR = PROJECT_ROOT / ".project"

WRITE_TOOLS = {"Write", "Edit"}
PROTOCOL_DIRS = (".project", ".agents")

# Gates that mark "plan approved" (PreToolUse) and "iteration closed"
# (Stop) in the core gate numbering (.agents/harness/INDEX.md).
PLAN_GATE = "H04"
CLOSE_GATE = "H06"

_MAX_STDIN_BYTES = 1_000_000


def _allow() -> int:
    return 0


def _deny(reason: str) -> int:
    print(reason, file=sys.stderr)
    return 2


def _read_event() -> dict | None:
    """Read and parse the hook event from stdin; None when unusable."""
    try:
        raw = sys.stdin.buffer.read(_MAX_STDIN_BYTES + 1)
    except OSError:
        return None
    if not raw or len(raw) > _MAX_STDIN_BYTES:
        return None
    try:
        event = json.loads(raw.decode("utf-8", errors="replace"))
    except json.JSONDecodeError:
        return None
    return event if isinstance(event, dict) else None


def _resolve_session(event: dict) -> Path | None:
    """Locate the active session directory under .project/ deterministically.

    Resolution order:
    1. Mapping: ``.project/.sessions.json`` (CLI session id -> protocol uuid).
    2. Exact directory: ``.project/<session_id>/`` exists.
    3. The only session directory.
    4. The most recently modified session directory — used only on the first
       event of a CLI session; the mapping is then recorded so subsequent
       events of that CLI session resolve identically.
    """
    mapping = _load_sessions_mapping()
    session_id = event.get("session_id")
    if isinstance(session_id, str) and session_id:
        if session_id in mapping:
            candidate = PROJECT_DIR / mapping[session_id]
            if candidate.is_dir():
                return candidate
        candidate = PROJECT_DIR / session_id
        if candidate.is_dir():
            return candidate
    sessions = _session_dirs()
    if not sessions:
        return None
    if len(sessions) == 1:
        resolved = sessions[0]
    else:
        resolved = max(sessions, key=lambda p: p.stat().st_mtime)
    if isinstance(session_id, str) and session_id and resolved is not None:
        mapping[session_id] = resolved.name
        _save_sessions_mapping(mapping)
    return resolved


def _session_dirs() -> list[Path]:
    """Return the session directories under .project/ (excluding persistent
    state and dot entries)."""
    if not PROJECT_DIR.is_dir():
        return []
    return [
        p
        for p in PROJECT_DIR.iterdir()
        if p.is_dir()
        and not p.name.startswith(".")
        and p.name not in ("knowledge", "skills")
    ]


def _sessions_mapping_file() -> Path:
    return PROJECT_DIR / ".sessions.json"


def _load_sessions_mapping() -> dict:
    """Load the CLI-session -> protocol-uuid mapping (best-effort)."""
    try:
        data = json.loads(_sessions_mapping_file().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _save_sessions_mapping(mapping: dict) -> None:
    """Persist the mapping transactionally; failures are non-blocking."""
    path = _sessions_mapping_file()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(
            dir=str(path.parent), prefix=".sessions.", suffix=".tmp"
        )
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(mapping, handle, indent=2)
            handle.write("\n")
        os.replace(tmp, path)
    except OSError:
        pass  # the mapping is best-effort; resolution still works without it


def _latest_iteration(session_dir: Path) -> Path | None:
    """Return the latest numeric iteration directory of the session."""
    iterations = [
        p
        for p in session_dir.iterdir()
        if p.is_dir() and re.fullmatch(r"\d+", p.name)
    ]
    if not iterations:
        return None
    return max(iterations, key=lambda p: int(p.name))


def _load_state(session_dir: Path) -> tuple[Path | None, dict]:
    """Load state.json of the latest iteration; missing/corrupt = no gates."""
    iter_dir = _latest_iteration(session_dir)
    if iter_dir is None:
        return None, {"gates": {}}
    try:
        state = json.loads((iter_dir / "state.json").read_text(encoding="utf-8"))
        if not isinstance(state, dict) or not isinstance(state.get("gates"), dict):
            return iter_dir, {"gates": {}}
        return iter_dir, state
    except (OSError, json.JSONDecodeError):
        return iter_dir, {"gates": {}}


def _gate_passed(state: dict, trigger: str) -> bool:
    entry = state.get("gates", {}).get(trigger)
    return isinstance(entry, dict) and entry.get("result") == "PASS"


def _target_path(event: dict) -> str | None:
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    for key in ("file_path", "path", "filename"):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _is_protocol_path(raw_path: str) -> bool:
    """True when the target lives inside .project/ or .agents/ (not a
    deliverable), resolved relative to the project root."""
    normalized = raw_path.replace("\\", "/")
    parts = [p for p in normalized.split("/") if p not in ("", ".")]
    if parts and parts[0] in PROTOCOL_DIRS:
        return True
    try:
        resolved = (PROJECT_ROOT / raw_path).resolve()
        relative = resolved.relative_to(PROJECT_ROOT)
    except (OSError, ValueError):
        return False
    return bool(relative.parts) and relative.parts[0] in PROTOCOL_DIRS


def _needs_clarification_recorded(session_dir: Path) -> bool:
    """True when the latest TASK_ANALYSIS.md recommends NEEDS_CLARIFICATION."""
    iter_dir = _latest_iteration(session_dir)
    if iter_dir is None:
        return False
    candidates = sorted(iter_dir.glob("*TASK_ANALYSIS.md"))
    if not candidates:
        return False
    try:
        content = candidates[-1].read_text(encoding="utf-8")
    except OSError:
        return False
    section = re.search(
        r"^##\s+Recommended Next State\s*\n(.*?)(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not section:
        return False
    match = re.search(
        r'recommended_next_state\s*=\s*"([^"]+)"', section.group(1)
    )
    return bool(match) and match.group(1).strip() == "NEEDS_CLARIFICATION"


def _runner_hint(session_dir: Path, iter_dir: Path | None, trigger: str) -> str:
    iteration = iter_dir.name if iter_dir is not None else "00"
    return (
        f"Complete the Gate Checklist of the {trigger} policy in "
        f".agents/orchestrators/core/harness/policies/, then record the PASS "
        f"with: python .agents/harness/runner_state.py "
        f"--session {session_dir.name} --trigger {trigger} "
        f"--iteration {iteration} pass"
    )


def decide(event: dict) -> int:
    """Apply the hook decision rules; returns the process exit code."""
    hook_event = event.get("hook_event_name") or event.get("event") or ""

    if hook_event == "PreToolUse":
        tool_name = event.get("tool_name") or event.get("tool") or ""
        if tool_name not in WRITE_TOOLS:
            return _allow()
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict):
            # Missing tool_input is a missing field: fail-open (documented).
            return _allow()
        target = _target_path(event)
        if target is None:
            # Write/Edit with a tool_input that names no target: deny. The
            # event is well-formed but does not say what would be written, so
            # allowing it would be a craftable bypass of the plan gate.
            return _deny(
                "Enforcement hook: Write/Edit without an identifiable target "
                "(tool_input must include file_path, path or filename)."
            )
        if _is_protocol_path(target):
            return _allow()
        session_dir = _resolve_session(event)
        if session_dir is None:
            return _deny(
                "Enforcement hook: no protocol session found under .project/. "
                "Start the task through the Orchestrator (TASK_ANALYSIS gate "
                "H00) before writing project deliverables."
            )
        iter_dir, state = _load_state(session_dir)
        if not _gate_passed(state, PLAN_GATE):
            return _deny(
                f"Enforcement hook: writing deliverables requires gate "
                f"{PLAN_GATE} (approved EXECUTION_PLAN) PASS for the current "
                f"iteration, and state.json does not record it. Run: "
                f"{_runner_hint(session_dir, iter_dir, PLAN_GATE)}"
            )
        return _allow()

    if hook_event == "Stop":
        session_dir = _resolve_session(event)
        if session_dir is None:
            return _allow()  # session without a started task
        iter_dir, state = _load_state(session_dir)
        if not state.get("gates"):
            return _allow()  # session without a started task
        if _gate_passed(state, CLOSE_GATE):
            return _allow()
        if _needs_clarification_recorded(session_dir):
            return _allow()
        if state.get("status") in ("ABORT", "COMPLETED"):
            return _allow()
        return _deny(
            f"Enforcement hook: the iteration is not closed (no {CLOSE_GATE} "
            "verification PASS, no NEEDS_CLARIFICATION recorded, no terminal "
            "status recorded). Close the iteration before stopping. Run: "
            f"{_runner_hint(session_dir, iter_dir, CLOSE_GATE)}"
        )

    # Any other event is not gated.
    return _allow()


def main() -> int:
    try:
        event = _read_event()
        if event is None:
            return _allow()  # malformed input: fail-open (documented)
        return decide(event)
    except Exception as exc:  # noqa: BLE001 - hooks must never crash closed
        print(
            f"Enforcement hook internal error (fail-open allow): {exc}",
            file=sys.stderr,
        )
        return _allow()


if __name__ == "__main__":
    sys.exit(main())
