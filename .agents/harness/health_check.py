#!/usr/bin/env python3
"""State-storage probe for the .agents protocol.

`state.json` (see `runner_state.py`) is the single source of truth for hook
enforcement, so the runtime requires that `.project/` is writable. This
module performs a write/read/delete round-trip of a probe file inside
`.project/` and reports PASS/FAIL as JSON. It is the only mechanical remnant
of the former health check: the document-level checks live in the prose
checklist of `.agents/standards/runtime/PROTOCOL_HEALTH.md`, applied by the
ArgentOS System Agent.

Usage: python .agents/harness/health_check.py
Exit code 0 when the probe passes, 1 otherwise.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_DIR = PROJECT_ROOT / ".project"


def probe() -> dict:
    """Verify that session state (state.json) can be written and read.

    Returns a dict with ``result`` ("PASS" or "FAIL"), ``evidence`` and a
    ``timestamp``.
    """
    probe_file = PROJECT_DIR / ".state_check_probe"
    payload = '{"probe": true}\n'
    timestamp = datetime.now(timezone.utc).isoformat()
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


if __name__ == "__main__":
    result = probe()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["result"] == "PASS" else 1)
