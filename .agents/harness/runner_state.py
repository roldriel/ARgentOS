"""Protocol state persistence for the harness.

There is no validation runner anymore: the Orchestrator judges each gate in
prose and this script only RECORDS the outcome. It is the single writer of
`state.json` (`.project/<session-uuid>/<iteration>/state.json`), the source
of truth for the protocol state of an iteration. Writes are transactional
(temp file + atomic rename) after each gate PASS. Consumers (the
`hook_gate.py` lifecycle hook, the Orchestrator) read it; a missing or
corrupt `state.json` means *no gate has passed* (fail-closed for consumers).

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

CLI (state recording only):

    python .agents/harness/runner_state.py \
        --session <uuid> --trigger <HXX> [--iteration <N>] pass

Records the PASS for the trigger in state.json. `--iteration` defaults to
the session's latest iteration folder. For trigger H04 it additionally runs
the post-hoc bypass scan and prints any alert to stderr without blocking.
Exit 0 on success; exit 2 with a clear message on stderr on error.

Self-contained: stdlib only, no other harness module imports.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / ".project"

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

# Valid task profiles; anything else resolves to "standard" (full cycle).
_VALID_PROFILES = ("trivial", "standard", "complex")

_PROFILE_SECTION_RE = re.compile(
    r"^##\s+Task Profile\s*\n(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
)
_PROFILE_VALUE_RE = re.compile(r'^\s*value\s*=\s*"([^"]+)"', re.MULTILINE)


def iteration_dirs(session_uuid: str) -> list[Path]:
    """Return sorted list of numeric iteration directories for a session."""
    session_dir = ARTIFACTS_DIR / session_uuid
    if not session_dir.is_dir():
        return []
    dirs = [
        p for p in session_dir.iterdir() if p.is_dir() and re.fullmatch(r"\d+", p.name)
    ]
    return sorted(dirs, key=lambda p: int(p.name))


def read_task_profile(session_uuid: str) -> str:
    """Return the task profile from the session's latest TASK_ANALYSIS.md.

    Searches files ending in `TASK_ANALYSIS.md` across the session's
    iteration folders (highest iteration wins) and reads the `value` key of
    the `Task Profile` section. Missing artifact, missing field, or
    unrecognized value resolves to `standard`. Advisory metadata only.
    """
    for iter_dir in reversed(iteration_dirs(session_uuid)):
        candidates = sorted(iter_dir.glob("*TASK_ANALYSIS.md"))
        if not candidates:
            continue
        try:
            content = candidates[-1].read_text(encoding="utf-8")
        except OSError:
            return "standard"
        section = _PROFILE_SECTION_RE.search(content)
        if not section:
            return "standard"
        match = _PROFILE_VALUE_RE.search(section.group(1))
        if match and match.group(1) in _VALID_PROFILES:
            return match.group(1)
        return "standard"
    return "standard"


def state_path(session_uuid: str, iteration: str) -> Path:
    """Return the state.json path for a session iteration."""
    return ARTIFACTS_DIR / session_uuid / iteration / "state.json"


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
        state["task_profile"] = read_task_profile(session_uuid)
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
    session_dir = ARTIFACTS_DIR / session_uuid
    try:
        window_start = session_dir.stat().st_mtime
    except OSError:
        return []
    suspects: list[str] = []
    root = PROJECT_ROOT
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


def _cli_error(message: str) -> int:
    print(f"runner_state: error: {message}", file=sys.stderr)
    return 2


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: record a gate PASS judged in prose by the Orchestrator."""
    parser = argparse.ArgumentParser(
        description=(
            "Record a gate PASS (judged by the Orchestrator) into the "
            "iteration state.json. This script only registers results."
        )
    )
    parser.add_argument("--session", required=True, help="session uuid")
    parser.add_argument("--trigger", required=True, help="gate trigger id (e.g. H04)")
    parser.add_argument(
        "--iteration",
        default=None,
        help="iteration folder (default: session's latest iteration)",
    )
    parser.add_argument(
        "action",
        choices=["pass"],
        help="outcome to record (only 'pass' is supported)",
    )
    args = parser.parse_args(argv)

    session_dir = ARTIFACTS_DIR / args.session
    if not session_dir.is_dir():
        return _cli_error(
            f"session not found: {session_dir} "
            "(start the task through the Orchestrator first)"
        )

    iteration = args.iteration
    if iteration is None:
        iteration = latest_iteration(args.session)
    elif not re.fullmatch(r"\d+", iteration):
        return _cli_error(f"invalid iteration: {iteration!r} (must be numeric)")
    elif not (session_dir / iteration).is_dir():
        return _cli_error(
            f"iteration folder not found: {session_dir / iteration}"
        )

    try:
        path = record_gate_pass(args.session, iteration, args.trigger)
    except OSError as exc:
        return _cli_error(f"could not write state.json: {exc}")

    if args.trigger == "H04":
        state = load_state(args.session, iteration)
        timestamp = state.get("gates", {}).get(args.trigger, {}).get("timestamp")
        if isinstance(timestamp, str):
            try:
                suspects = detect_bypass(args.session, iteration, timestamp)
            except Exception as exc:  # noqa: BLE001 - audit scan never blocks
                print(
                    f"runner_state: bypass scan failed (non-blocking): {exc}",
                    file=sys.stderr,
                )
            else:
                if suspects:
                    print(
                        "runner_state: BYPASS ALERT - files modified between "
                        "session start and the H04 PASS (no approved plan in "
                        "that window):",
                        file=sys.stderr,
                    )
                    for suspect in suspects:
                        print(f"  - {suspect}", file=sys.stderr)

    print(f"PASS recorded: {args.trigger} -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
