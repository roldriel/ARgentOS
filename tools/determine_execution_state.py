#!/usr/bin/env python3
"""Determine the terminal Task State of every execution from its records.

DEV-only, read-only. For each execution (a numeric iteration folder of a
protocol session under ``<root>/.project/``), reads the execution record's
``state.json`` and reports the terminal Task State it declares.

The determination is the terminal state recorded as ``status`` in the
iteration ``state.json`` (``ABORT`` | ``COMPLETED``). ``state.json`` is the
mechanical truth of the protocol state per execution: it records transition
gates (H00-H07, H11) and the terminal status only (RFC-64; ``harness/INDEX.md``
"Protocol State and Hook Enforcement" and "Execution records"). This is the
existing model's canonical representation of how a finished execution ended;
no new field, artifact, state or semantic category is introduced.

Determinability boundary (no inference):

- ``status`` terminal (``ABORT`` | ``COMPLETED``) -> determination = that
  terminal state.
- ``status`` non-terminal (``no_gates_passed`` | ``in_progress``) -> no
  determination. Under the record model an iteration that did not reach a
  terminal state before the session ended is a partial iteration
  (``standards/runtime/PROTOCOL_BOUNDARIES.md``); the tool does not infer a
  terminal value from gate records or narrative.
- Missing or corrupt ``state.json`` -> no determination. Consumers treat a
  missing/corrupt file as "no gate has passed" (fail-closed, ``runner_state``
  semantics).

This tool does not replace the session-artifact validator
(``tools/check_session_artifacts.py``) or the bidirectional gate audit
(``tools/aggregate_metrics.py --audit``). Run those first to establish record
validity; this tool only reads the terminal declaration the record actually
contains.

Usage:
  python tools/determine_execution_state.py [--root REPO_ROOT] [--session UUID]

Prints a deterministic JSON report and exits 0. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TERMINAL_STATES = ("ABORT", "COMPLETED")
SESSION_SKIP = {"knowledge", "skills"}
_VERSION_RE = re.compile(r"^-\s*Protocol version:\s*(\S+)", re.MULTILINE)
_METRIC_RE = re.compile(r"<!-- METRIC: (.*?) -->", re.DOTALL)


def session_dirs(root: Path) -> list[Path]:
    """Return the protocol session directories under ``<root>/.project/``."""
    project = root / ".project"
    if not project.is_dir():
        return []
    return sorted(
        p
        for p in project.iterdir()
        if p.is_dir() and not p.name.startswith(".") and p.name not in SESSION_SKIP
    )


def iteration_dirs(session: Path) -> list[Path]:
    """Return the numeric iteration directories of a session, sorted."""
    return sorted(
        (p for p in session.iterdir() if p.is_dir() and re.fullmatch(r"\d+", p.name)),
        key=lambda p: int(p.name),
    )


def protocol_version(session: Path) -> str | None:
    """Return the protocol version declared by a session, if any.

    The declaration lives in the ``SESSION_LOG.md`` header or, failing that,
    in the ``session_start`` metric event (same sources as the session
    checkers).
    """
    log = session / "SESSION_LOG.md"
    if log.is_file():
        try:
            text = log.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        match = _VERSION_RE.search(text)
        if match:
            return match.group(1)
    metrics = session / "METRICS.md"
    if metrics.is_file():
        try:
            text = metrics.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        for raw in _METRIC_RE.finditer(text):
            try:
                data = json.loads(raw.group(1).strip())
            except json.JSONDecodeError:
                continue
            if (
                isinstance(data, dict)
                and data.get("type") == "session_start"
                and isinstance(data.get("protocol_version"), str)
            ):
                return data["protocol_version"]
    return None


def determine_iteration(session: Path, iteration: Path) -> dict[str, Any]:
    """Return the terminal-state determination for one execution record."""
    entry: dict[str, Any] = {
        "session": session.name,
        "iteration": iteration.name,
        "protocol_version": protocol_version(session),
        "state_json": "missing",
        "status": None,
        "terminal_task_state": None,
        "determined": False,
        "reason": None,
    }
    state_file = iteration / "state.json"
    if not state_file.is_file():
        entry["reason"] = "state_json_missing"
        return entry
    try:
        data = json.loads(state_file.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        entry["state_json"] = "corrupt"
        entry["reason"] = "state_json_corrupt"
        return entry
    if not isinstance(data, dict) or not isinstance(data.get("status"), str):
        entry["state_json"] = "corrupt"
        entry["reason"] = "state_json_corrupt"
        return entry
    entry["state_json"] = "present"
    status = data["status"]
    entry["status"] = status
    if status in TERMINAL_STATES:
        entry["terminal_task_state"] = status
        entry["determined"] = True
    else:
        entry["reason"] = "status_not_terminal"
    return entry


def determine(
    root: Path, session_filter: str | None = None
) -> dict[str, Any]:
    """Determine the terminal Task State of every execution under root.

    Returns a deterministic JSON-ready report with one entry per execution
    (sorted by session and iteration) and a summary. No file is written.
    """
    executions: list[dict[str, Any]] = []
    for session in session_dirs(root):
        if session_filter is not None and session.name != session_filter:
            continue
        for iteration in iteration_dirs(session):
            executions.append(determine_iteration(session, iteration))
    determined = sum(1 for e in executions if e["determined"])
    return {
        "executions": executions,
        "summary": {
            "total": len(executions),
            "determined": determined,
            "undetermined": len(executions) - determined,
        },
    }


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: print the per-execution terminal-state report."""
    parser = argparse.ArgumentParser(
        description=(
            "Determine the terminal Task State declared by each execution "
            "record (state.json status) under .project/."
        )
    )
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument(
        "--session",
        default=None,
        help="only report executions of this protocol session uuid",
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    report = determine(root, session_filter=args.session)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
