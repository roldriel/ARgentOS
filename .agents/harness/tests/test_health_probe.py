"""Tests for the state-storage probe (health_check.py).

The probe is the only mechanical item of the protocol health verification:
it proves that `.project/` is writable so `state.json` can be persisted.
The document-level checks live in the prose checklist of
`.agents/standards/runtime/PROTOCOL_HEALTH.md` and are applied by the agent.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import health_check

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PROBE_PATH = PROJECT_ROOT / ".agents" / "harness" / "health_check.py"


def test_probe_passes_on_real_project():
    result = health_check.probe()
    assert result["result"] == "PASS", result["evidence"]
    assert result["timestamp"]


def test_probe_cleans_up_probe_file():
    health_check.probe()
    assert not (PROJECT_ROOT / ".project" / ".state_check_probe").exists()


def test_probe_cli_exit_code_and_json():
    result = subprocess.run(
        [sys.executable, str(PROBE_PATH)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    output = json.loads(result.stdout)
    assert result.returncode == 0, output
    assert output["result"] == "PASS"


def test_probe_fails_on_unwritable_project_dir(monkeypatch, tmp_path):
    blocked = tmp_path / "blocked"
    monkeypatch.setattr(health_check, "PROJECT_DIR", blocked)
    # Simulate an unwritable artifacts directory by making the path a file.
    blocked.write_text("not a directory", encoding="utf-8")
    result = health_check.probe()
    assert result["result"] == "FAIL"
