#!/usr/bin/env python3
"""State-storage probe for the .agents protocol.

`state.json` (see `runner_state.py`) is the single source of truth for hook
enforcement, so the runtime requires that `ARGENTOS_ROOT/.project/` is
writable. This module performs a write/read/delete round-trip of a probe file
inside it and reports PASS/FAIL as JSON. It is the only mechanical remnant of
the former health check: the document-level checks live in the prose checklist
of `.agents/standards/runtime/PROTOCOL_HEALTH.md`, applied by the ArgentOS
System Agent.

The roots follow the adopted layout contract (`harness/roots.py`): the project
root is provided by the entry point (`--project-root` or
`ARGENTOS_PROJECT_ROOT`) and is never discovered from this file's location.

Usage: python .argentos/.agents/harness/health_check.py --project-root <project>
Exit code 0 when the probe passes, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# The harness scripts are self-contained entry points; the harness directory
# hosts the shared root contract. Registering it here keeps the import local
# (no packaging) and works under pytest, direct execution and importlib loads.
_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import roots as _roots  # noqa: E402  (import after the sys.path registration)

#: Roots of the adopted layout; PROJECT_DIR is ARGENTOS_ROOT/.project.
PROJECT_ROOT: Path | None = None
ARGENTOS_ROOT: Path | None = None
PROJECT_DIR: Path | None = None


def configure_roots(project_root: str | Path) -> _roots.Roots:
    """Adopt the root contract from a project root provided by the caller."""
    global PROJECT_ROOT, ARGENTOS_ROOT, PROJECT_DIR
    resolved = _roots.resolve(project_root)
    PROJECT_ROOT = resolved.project_root
    ARGENTOS_ROOT = resolved.argentos_root
    PROJECT_DIR = resolved.project_dir
    return resolved


def probe() -> dict:
    """Verify that session state (state.json) can be written and read.

    Returns a dict with ``result`` ("PASS" or "FAIL"), ``evidence`` and a
    ``timestamp``.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    if PROJECT_DIR is None:
        return {
            "result": "FAIL",
            "evidence": (
                "PROJECT_ROOT is not configured: provide it with "
                f"--project-root or {_roots.ENV_PROJECT_ROOT}"
            ),
            "timestamp": timestamp,
        }
    probe_file = PROJECT_DIR / ".state_check_probe"
    payload = '{"probe": true}\n'
    try:
        PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        probe_file.write_text(payload, encoding="utf-8")
        read_back = probe_file.read_text(encoding="utf-8")
        probe_file.unlink()
    except OSError as exc:
        return {
            "result": "FAIL",
            "evidence": f"Cannot write/read state.json probe in {PROJECT_DIR}: {exc}",
            "timestamp": timestamp,
        }
    ok = read_back == payload
    return {
        "result": "PASS" if ok else "FAIL",
        "evidence": (
            "state.json write/read probe succeeded"
            if ok
            else "state.json probe read-back mismatch"
        ),
        "timestamp": timestamp,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--project-root",
        "--root",
        dest="project_root",
        default=None,
        help=(
            "real project root of the adopted layout (default: the "
            f"{_roots.ENV_PROJECT_ROOT} environment variable)"
        ),
    )
    args = parser.parse_args(argv)
    project_root = args.project_root or os.environ.get(_roots.ENV_PROJECT_ROOT)
    if project_root:
        try:
            configure_roots(project_root)
        except _roots.RootResolutionError as exc:
            print(
                json.dumps(
                    {"result": "FAIL", "evidence": str(exc)}, indent=2
                )
            )
            return 1
    result = probe()
    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
