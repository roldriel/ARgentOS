#!/usr/bin/env python3
"""Shared lifecycle hook for CLI-level enforcement of the .agents protocol.

Reads one hook event as JSON from stdin (Kimi Code / Claude Code format:
`session_id`, `cwd`, `hook_event_name`, `tool_name`, `tool_input`) and
decides allow/deny against the iteration state written by runner_state
(`.project/<session-uuid>/<iteration>/state.json`).

Decision (in order):

1. The tool call does not touch a project deliverable (not a
   ``PreToolUse`` on ``Write``/``Edit``, or the target path lives in the
   ARgentOS space outside the payload: ``ARGENTOS_ROOT/.project`` /
   ``ARGENTOS_ROOT/features.toml`` / ``ARGENTOS_ROOT/.backup``) -> allow
   (exit 0). A target inside ``ARGENTOS_ROOT/.agents`` is the protocol
   payload and is denied: it is immutable during normal session execution.
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

Roots follow the adopted layout contract (``harness/roots.py``): the hook
receives the project root from its entry-point context (the event ``cwd``, or
``ARGENTOS_PROJECT_ROOT``/``--project-root``) and never derives it from this
file's location. Paths are classified against the three roots: the ARgentOS
space (``ARGENTOS_ROOT``) is never a project deliverable.

Fail-open honesty: malformed stdin, missing event fields, or any internal
error resolve to allow (exit 0). A crash or a CLI-side timeout of this
script also means allow — hook enforcement protects against agent
omission, not against the hook itself failing. Post-hoc detection
compensates: runner_state.detect_bypass runs when the runner_state CLI
records the H04 gate.

Usage (CLI hook configuration): ``python .argentos/.agents/harness/hook_gate.py``
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# The harness scripts are self-contained entry points; the harness directory
# hosts the shared root contract. Registering it here keeps the import local
# (no packaging) and works under pytest, direct execution and importlib loads.
_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import roots as _roots  # noqa: E402  (import after the sys.path registration)

# Roots of the adopted layout, resolved from the entry-point context and never
# from this file's location. PROJECT_DIR is ARGENTOS_ROOT/.project.
PROJECT_ROOT: Path | None = None
ARGENTOS_ROOT: Path | None = None
PAYLOAD_ROOT: Path | None = None
PROJECT_DIR: Path | None = None

WRITE_TOOLS = {"Write", "Edit"}

def configure_roots(project_root: str | Path) -> _roots.Roots:
    """Adopt the root contract from a project root provided by the caller."""
    global PROJECT_ROOT, ARGENTOS_ROOT, PAYLOAD_ROOT, PROJECT_DIR
    resolved = _roots.resolve(project_root)
    PROJECT_ROOT = resolved.project_root
    ARGENTOS_ROOT = resolved.argentos_root
    PAYLOAD_ROOT = resolved.payload_root
    PROJECT_DIR = resolved.project_dir
    return resolved


def _ensure_roots(event: dict) -> bool:
    """Resolve the roots from the entry-point context; False when unavailable.

    Resolution order: an already-injected root, the event's ``cwd`` (the hook
    event schema declares it as the project root), then
    ``ARGENTOS_PROJECT_ROOT``. The event context wins so an inherited
    environment value from another project cannot silently override the
    session being gated; the process working directory is never used as
    authority.
    """
    if PROJECT_ROOT is not None:
        return True
    hint = event.get("cwd")
    if not (isinstance(hint, str) and hint.strip()):
        hint = os.environ.get(_roots.ENV_PROJECT_ROOT)
    if not (isinstance(hint, str) and hint.strip()):
        return False
    try:
        configure_roots(hint)
    except _roots.RootResolutionError:
        return False
    return True

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
    """Locate the active session directory under ARGENTOS_ROOT/.project/.

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
    if PROJECT_DIR is None:
        return []
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
    if PROJECT_DIR is not None:
        return PROJECT_DIR / ".sessions.json"
    return Path(".sessions.json")


def _load_sessions_mapping() -> dict:
    """Load the CLI-session -> protocol-uuid mapping (best-effort)."""
    if PROJECT_DIR is None:
        return {}
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


def _argentos_root() -> Path | None:
    """ARGENTOS_ROOT, derived from PROJECT_ROOT when it was not injected."""
    if ARGENTOS_ROOT is not None:
        return Path(ARGENTOS_ROOT)
    if PROJECT_ROOT is not None:
        return Path(PROJECT_ROOT) / _roots.ARGENTOS_DIRNAME
    return None


def _is_payload(raw_path: str) -> bool:
    """True when the resolved target lives inside PAYLOAD_ROOT.

    Payload immutability (``PROTOCOL_BOUNDARIES: Protocol immutability``): a
    normal session does not write the protocol payload, which is
    ``ARGENTOS_ROOT/.agents``. The rest of the ARgentOS space — session state
    under ``.project/``, ``features.toml`` and the lifecycle backups under
    ``.backup/`` — stays writable; only the payload is denied.

    Classification is by resolved containment, never by a textual prefix, so a
    target that escapes the payload through ``..`` is not denied here.
    """
    payload = PAYLOAD_ROOT
    if payload is None:
        argentos = _argentos_root()
        if argentos is None:
            return False
        payload = argentos / _roots.AGENTS_DIRNAME
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        if PROJECT_ROOT is None:
            return False
        candidate = Path(PROJECT_ROOT) / candidate
    try:
        resolved = candidate.resolve()
        payload = Path(payload).resolve()
    except OSError:
        return False
    return resolved == payload or payload in resolved.parents


def _is_argentos_space(raw_path: str) -> bool:
    """True when the resolved target lives inside ARGENTOS_ROOT.

    Classification is decided by **resolved containment**, never by a textual
    prefix: a path such as ``.agents/../../src/app.py`` starts with a
    protocol-looking segment but escapes the ARgentOS space, so it is a project
    deliverable, not protocol state. Relative targets are resolved against
    ``PROJECT_ROOT``; a target is ARgentOS space only when it resolves inside
    ``ARGENTOS_ROOT`` (which is ``PROJECT_ROOT/.argentos``).
    """
    argentos = _argentos_root()
    if argentos is None:
        return False
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        if PROJECT_ROOT is None:
            return False
        candidate = Path(PROJECT_ROOT) / candidate
    try:
        resolved = candidate.resolve()
    except OSError:
        return False
    argentos = argentos.resolve()
    return resolved == argentos or argentos in resolved.parents


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


def _runner_command() -> str:
    """The runner_state invocation path, anchored in the ARgentOS space.

    The payload is installed at ``ARGENTOS_ROOT/.agents``; a command that
    assumed ``.agents/harness/...`` at the project root would be wrong in the
    adopted layout.
    """
    if PROJECT_ROOT is not None and PAYLOAD_ROOT is not None:
        script = Path(PAYLOAD_ROOT) / "harness" / "runner_state.py"
        try:
            return "python " + script.relative_to(Path(PROJECT_ROOT)).as_posix()
        except ValueError:
            pass
    return "python .argentos/.agents/harness/runner_state.py"


def _runner_hint(session_dir: Path, iter_dir: Path | None, trigger: str) -> str:
    iteration = iter_dir.name if iter_dir is not None else "00"
    return (
        f"Complete the Gate Checklist of the {trigger} policy in "
        f".argentos/.agents/orchestrators/core/harness/policies/, then record "
        f"the PASS with: {_runner_command()} "
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
        if not _ensure_roots(event):
            # No project root in the entry-point context and none injected: the
            # target cannot be classified. Missing-field property: allow.
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
        if _is_argentos_space(target):
            if _is_payload(target):
                # Payload immutability: the protocol payload is not a session
                # deliverable and must not be written during normal execution.
                return _deny(
                    "Enforcement hook: target is inside the protocol payload "
                    "(.agents/), which is immutable during normal session "
                    "execution (PROTOCOL_BOUNDARIES: Protocol immutability). "
                    "Change the payload outside a normal session, through the "
                    "authorized path (release or RFC-56)."
                )
            return _allow()
        session_dir = _resolve_session(event)
        if session_dir is None:
            return _deny(
                "Enforcement hook: no protocol session found under "
                ".argentos/.project/. "
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
        if not _ensure_roots(event):
            return _allow()  # session without a started task
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
