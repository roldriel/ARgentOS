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
  "gates": {"H04": {"result": "PASS", "timestamp": "<ISO-8601 UTC with Z>"}},
  "last_gate": "H04",
  "status": "in_progress",   # or ABORT / COMPLETED (terminal)
  "updated": "<ISO-8601>"
}
```

Scope: `state.json` records transition gates of the core state machine and
the terminal status only. The accepted transition triggers are H00–H07 and
H11 (`TRANSITION_TRIGGERS`); every other gate (D*, H09/H10, H15, S00, REVIEW)
is recorded in `HARNESS_REPORT.md` only and is rejected by the `pass` action.
`gates[HXX].timestamp` is the canonical `gate_ts` of the transition (UTC,
normalized with a `Z` suffix).

CLI (state recording only):

    python .argentos/.agents/harness/runner_state.py \
        --project-root <project> --session <uuid> --trigger <HXX> \
        [--iteration <N>] pass

Records the PASS for a transition trigger (H00–H07, H11) in state.json.
`--iteration` defaults to the session's latest iteration folder. Any other
trigger is rejected with exit 2 (non-transition gates live in
`HARNESS_REPORT.md` only). For trigger H04 it additionally runs the post-hoc
bypass scan and prints any alert to stderr without blocking. Exit 0 on
success; exit 2 with a clear message on stderr on error.

    python .argentos/.agents/harness/runner_state.py \
        --project-root <project> --session <uuid> --state ABORT terminal

Records a terminal state (`ABORT` or `COMPLETED`) in state.json, preserving
the recorded gate passes. Same transactional write and exit conventions.

H15 schema support (no session required):

    python .argentos/.agents/harness/runner_state.py --input <json> validate-delegation
    python .argentos/.agents/harness/runner_state.py --input <json> validate-return

Validates the delegation payload or the worker return report against the
delegation contract fields. The H15 gate remains the Orchestrator's judgment;
these subcommands are mechanical schema support.

Roots follow the adopted layout contract (``harness/roots.py``): the session
state lives under ``ARGENTOS_ROOT/.project`` and the post-hoc bypass scan walks
the real ``PROJECT_ROOT`` provided by the entry point. ``PROJECT_ROOT`` is
never discovered by fixed parent depth. Standard library only.
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

# The harness scripts are self-contained entry points; the harness directory
# hosts the shared root contract. Registering it here keeps the import local
# (no packaging) and works under pytest, direct execution and importlib loads.
_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import roots as _roots  # noqa: E402  (import after the sys.path registration)

# Roots of the adopted layout. PROJECT_ROOT is provided by the entry point
# (--project-root or ARGENTOS_PROJECT_ROOT); it is never derived from this
# file's location. ARTIFACTS_DIR is ARGENTOS_ROOT/.project. They are module
# globals so a caller (or a test) can inject the roots explicitly.
PROJECT_ROOT: Path | None = None
ARGENTOS_ROOT: Path | None = None
PAYLOAD_ROOT: Path | None = None
ARTIFACTS_DIR: Path | None = None


def configure_roots(project_root: str | Path) -> _roots.Roots:
    """Adopt the root contract from a project root provided by the caller."""
    global PROJECT_ROOT, ARGENTOS_ROOT, PAYLOAD_ROOT, ARTIFACTS_DIR
    resolved = _roots.resolve(project_root)
    PROJECT_ROOT = resolved.project_root
    ARGENTOS_ROOT = resolved.argentos_root
    PAYLOAD_ROOT = resolved.payload_root
    ARTIFACTS_DIR = resolved.project_dir
    return resolved


def _require_artifacts_dir() -> Path:
    if ARTIFACTS_DIR is None:
        raise RuntimeError(
            "PROJECT_ROOT is not configured: provide it with --project-root "
            f"or {_roots.ENV_PROJECT_ROOT}"
        )
    return ARTIFACTS_DIR

# Directories that never count as project deliverables for the post-hoc
# bypass scan (VCS, caches, dependency folders). `.agents` and `.project` are
# excluded by their location under ARGENTOS_ROOT, not by basename: the
# exclusion is relative to ARGENTOS_ROOT, as the root contract requires.
_BYPASS_SCAN_EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
}

_BYPASS_SCAN_MAX_FILES = 20

# Valid task profiles; anything else resolves to "standard" (full cycle).
_VALID_PROFILES = ("trivial", "standard", "complex")
TERMINAL_STATES = ("ABORT", "COMPLETED")

# Transition triggers of the core state machine recorded in state.json
# (D-005). Every other gate (D*, H09/H10, H15, S00, REVIEW) is recorded in
# HARNESS_REPORT.md only.
TRANSITION_TRIGGERS = frozenset(
    {"H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07", "H11"}
)

_PROFILE_SECTION_RE = re.compile(
    r"^##\s+Task Profile\s*\n(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
)
_PROFILE_VALUE_RE = re.compile(r'^\s*value\s*=\s*"([^"]+)"', re.MULTILINE)


def iteration_dirs(session_uuid: str) -> list[Path]:
    """Return sorted list of numeric iteration directories for a session."""
    session_dir = _require_artifacts_dir() / session_uuid
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
    return _require_artifacts_dir() / session_uuid / iteration / "state.json"


def _persist(session_uuid: str, iteration: str, data: dict[str, Any]) -> Path:
    """Write state.json transactionally (temp file + atomic rename)."""
    path = state_path(session_uuid, iteration)
    return _write_json(path, data)


def _write_json(path: Path, data: dict[str, Any]) -> Path:
    """Write a JSON file transactionally (temp file + atomic rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix="." + path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return path


def sessions_mapping_file() -> Path:
    """Path of the CLI-session -> protocol-uuid mapping (.project/.sessions.json)."""
    return _require_artifacts_dir() / ".sessions.json"


def link_session(cli_session: str, session_uuid: str) -> Path:
    """Bind a CLI session id to a protocol session uuid in .project/.sessions.json.

    The hook (`hook_gate.py`) resolves sessions by this mapping first; explicit
    linking is useful when a CLI conversation resumes a protocol session across
    conversations (the CLI session id differs from the protocol uuid).
    """
    mapping_path = sessions_mapping_file()
    try:
        mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        mapping = {}
    if not isinstance(mapping, dict):
        mapping = {}
    mapping[cli_session] = session_uuid
    return _write_json(mapping_path, mapping)


DELEGATION_REQUIRED = (
    "session_uuid",
    "current_state",
    "target_phase",
    "role_to_adopt",
    "input_artifacts",
    "harness_policy",
    "task_summary",
)

VALID_PROFILES = {
    "backend_engineer",
    "database_engineer",
    "integration_engineer",
    "qa_engineer",
    "tech_writer",
    "functional_writer",
    "intent_reflector",
    "intent_reflection_reviewer",
    None,
}

RETURN_REQUIRED = (
    "output_artifact",
    "role_executed",
    "profile_executed",
    "phase_completed",
    "summary",
    "blockers",
    "deviations",
)

DEVIATION_PREFIXES = ("deviation:", "ambiguity:", "inconsistency:")


def validate_delegation(data: Any) -> list[str]:
    """Return the schema errors of a delegation payload (empty when valid)."""
    if not isinstance(data, dict):
        return ["payload is not an object"]
    errors = [f"missing required field: {f}" for f in DELEGATION_REQUIRED if f not in data]
    if "input_artifacts" in data and not isinstance(data["input_artifacts"], list):
        errors.append("input_artifacts must be a list")
    profile = data.get("profile")
    if profile not in VALID_PROFILES:
        errors.append(f"invalid profile: {profile!r}")
    budget = data.get("context_budget")
    if budget is not None and (not isinstance(budget, (int, float)) or budget <= 0):
        errors.append("context_budget must be a finite positive number")
    return errors


def validate_return(data: Any) -> list[str]:
    """Return the schema errors of a worker return report (empty when valid)."""
    if not isinstance(data, dict):
        return ["report is not an object"]
    errors = [f"missing required field: {f}" for f in RETURN_REQUIRED if f not in data]
    for field in ("blockers", "deviations"):
        value = data.get(field)
        if value is not None and not isinstance(value, list):
            errors.append(f"{field} must be a list")
    for entry in data.get("deviations", []) or []:
        if not isinstance(entry, str) or not entry.lower().startswith(DEVIATION_PREFIXES):
            errors.append(f"deviation entry without class prefix: {entry!r}")
    return errors


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
    now = (timestamp or datetime.now(timezone.utc).isoformat()).replace(
        "+00:00", "Z"
    )
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

    return _persist(session_uuid, iteration, state)


def record_terminal_state(
    session_uuid: str, iteration: str, state: str, timestamp: str | None = None
) -> Path:
    """Record a terminal protocol state (ABORT or COMPLETED) in state.json.

    Preserves the recorded gate passes and marks the iteration terminal via
    `status`; the write is transactional like every other state update.
    """
    if state not in TERMINAL_STATES:
        raise ValueError(f"invalid terminal state: {state!r}")
    data = load_state(session_uuid, iteration)
    now = (timestamp or datetime.now(timezone.utc).isoformat()).replace(
        "+00:00", "Z"
    )
    data["session"] = session_uuid
    data["iteration"] = iteration
    data["status"] = state
    data["updated"] = now
    return _persist(session_uuid, iteration, data)


def _excluded_scan_roots() -> tuple[Path, ...]:
    """Roots that are never project deliverables for the bypass scan.

    The ARgentOS space is excluded by **location**, not by basename: the root
    contract places `.agents` and `.project` under `ARGENTOS_ROOT`, so
    excluding those names anywhere in the tree would both hide real project
    deliverables and leak ARgentOS state into the scan.
    """
    excluded: list[Path] = []
    for value in (ARGENTOS_ROOT, PAYLOAD_ROOT, ARTIFACTS_DIR):
        if value is None:
            continue
        try:
            resolved = Path(value).resolve()
        except OSError:
            continue
        if resolved not in excluded:
            excluded.append(resolved)
    return tuple(excluded)


def _is_excluded_dir(candidate: Path, excluded: tuple[Path, ...]) -> bool:
    """True when ``candidate`` is, or lives inside, an excluded root."""
    try:
        resolved = candidate.resolve()
    except OSError:
        return False
    return any(resolved == ex or ex in resolved.parents for ex in excluded)


def detect_bypass(
    session_uuid: str, iteration: str, gate_timestamp: str
) -> tuple[list[str], bool]:
    """Post-hoc bypass scan run when the plan gate (H04) passes.

    Returns ``(suspects, reliable)``: paths of would-be deliverables (project files outside the
    protocol and cache directories) modified after the session directory was
    created but before the H04 PASS timestamp: writes that happened during a
    window where no plan was approved — e.g. while the enforcement hook was
    fail-open (crash/timeout) or not installed (declarative mode). The result
    is an audit alert, never a gate failure. ``reliable`` is ``False`` when the
    gate timestamp is not UTC-normalized (the scan consumes the canonical
    `gate_ts`; a non-canonical timestamp makes the scan unreliable).

    The walk root is the real ``PROJECT_ROOT``; the ARgentOS space under
    ``ARGENTOS_ROOT`` (payload + session state) is pruned by location.
    """
    try:
        gate_dt = datetime.fromisoformat(gate_timestamp.replace("Z", "+00:00"))
    except ValueError:
        return [], False
    reliable = gate_timestamp.endswith("Z") or gate_timestamp.endswith("+00:00")
    session_dir = _require_artifacts_dir() / session_uuid
    try:
        window_start = session_dir.stat().st_mtime
    except OSError:
        return [], reliable
    suspects: list[str] = []
    root = PROJECT_ROOT
    if root is None:
        # Without the real project root there is no trustworthy tree to scan.
        return [], reliable
    root = Path(root).resolve()
    excluded = _excluded_scan_roots()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in _BYPASS_SCAN_EXCLUDED_DIRS
            and not _is_excluded_dir(Path(dirpath) / d, excluded)
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
                    return suspects, reliable
    return suspects, reliable


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
            "Record a gate PASS or a terminal state (judged by the "
            "Orchestrator) into the iteration state.json. This script only "
            "registers results."
        )
    )
    parser.add_argument(
        "--session",
        default=None,
        help="session uuid (required for pass/terminal/link actions)",
    )
    parser.add_argument(
        "--trigger",
        default=None,
        help="gate trigger id (e.g. H04); required for the 'pass' action",
    )
    parser.add_argument(
        "--iteration",
        default=None,
        help="iteration folder (default: session's latest iteration)",
    )
    parser.add_argument(
        "--state",
        default=None,
        help="terminal state for the 'terminal' action (ABORT or COMPLETED)",
    )
    parser.add_argument(
        "--cli-session",
        default=None,
        help="CLI session id to bind for the 'link' action",
    )
    parser.add_argument(
        "--input",
        default=None,
        help="JSON file for validate-delegation/validate-return ('-' for stdin)",
    )
    parser.add_argument(
        "--project-root",
        default=None,
        help=(
            "real project root of the adopted layout (default: the "
            f"{_roots.ENV_PROJECT_ROOT} environment variable). It is never "
            "discovered from this script's location."
        ),
    )
    parser.add_argument(
        "action",
        choices=["pass", "terminal", "link", "validate-delegation", "validate-return"],
        help="outcome to record ('pass' for a gate PASS, 'terminal' for ABORT/COMPLETED, "
        "'link' to bind a CLI session to this protocol session, "
        "'validate-delegation'/'validate-return' for H15 schema support)",
    )
    args = parser.parse_args(argv)

    project_root = args.project_root or os.environ.get(_roots.ENV_PROJECT_ROOT)
    if project_root:
        try:
            configure_roots(project_root)
        except _roots.RootResolutionError as exc:
            return _cli_error(str(exc))

    if args.action in ("validate-delegation", "validate-return"):
        if not args.input:
            return _cli_error("validate actions require --input <file> or '-' (stdin)")
        if args.input == "-":
            raw = sys.stdin.read()
        else:
            try:
                raw = Path(args.input).read_text(encoding="utf-8")
            except OSError as exc:
                return _cli_error(f"could not read input: {exc}")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            return _cli_error(f"invalid JSON input: {exc}")
        errors = (
            validate_delegation(data)
            if args.action == "validate-delegation"
            else validate_return(data)
        )
        if errors:
            print(f"{args.action}: FAIL")
            for error in errors:
                print(f"  - {error}")
            return 2
        print(f"{args.action}: PASS")
        return 0

    if ARTIFACTS_DIR is None:
        return _cli_error(
            "PROJECT_ROOT is not configured: pass --project-root or set "
            f"{_roots.ENV_PROJECT_ROOT} (the session state lives under "
            "ARGENTOS_ROOT/.project)"
        )

    if not args.session:
        return _cli_error("--session is required for the pass/terminal/link actions")

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

    if args.action == "pass" and not args.trigger:
        return _cli_error("the 'pass' action requires --trigger")
    if args.action == "pass" and args.trigger not in TRANSITION_TRIGGERS:
        return _cli_error(
            f"trigger {args.trigger!r} is not a transition trigger "
            "(allowed: H00-H07, H11); non-transition gates (D*, H10, H15, "
            "S00, REVIEW) are recorded in HARNESS_REPORT.md only"
        )

    if args.action == "link":
        if not args.cli_session:
            return _cli_error("the 'link' action requires --cli-session")
        try:
            path = link_session(args.cli_session, args.session)
        except OSError as exc:
            return _cli_error(f"could not write .sessions.json: {exc}")
        print(
            f"CLI session linked: {args.cli_session} -> {args.session} "
            f"({path})"
        )
        return 0

    if args.action == "terminal":
        if args.state not in TERMINAL_STATES:
            return _cli_error(
                f"invalid terminal state {args.state!r}; use ABORT or COMPLETED"
            )
        try:
            path = record_terminal_state(args.session, iteration, args.state)
        except OSError as exc:
            return _cli_error(f"could not write state.json: {exc}")
        print(f"Terminal state recorded: {args.state} -> {path}")
        return 0

    try:
        path = record_gate_pass(args.session, iteration, args.trigger)
    except OSError as exc:
        return _cli_error(f"could not write state.json: {exc}")

    if args.trigger == "H04":
        state = load_state(args.session, iteration)
        timestamp = state.get("gates", {}).get(args.trigger, {}).get("timestamp")
        if isinstance(timestamp, str):
            try:
                suspects, reliable = detect_bypass(
                    args.session, iteration, timestamp
                )
            except Exception as exc:  # noqa: BLE001 - audit scan never blocks
                print(
                    f"runner_state: bypass scan failed (non-blocking): {exc}",
                    file=sys.stderr,
                )
            else:
                if not reliable:
                    print(
                        "runner_state: bypass scan not reliable (gate_ts is "
                        "not UTC-normalized)",
                        file=sys.stderr,
                    )
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
