"""Tests for the state-storage probe (health_check.py).

The probe is the only mechanical item of the protocol health verification: it
proves that `ARGENTOS_ROOT/.project/` is writable so `state.json` can be
persisted. The document-level checks live in the prose checklist of
`.agents/standards/runtime/PROTOCOL_HEALTH.md` and are applied by the agent.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import health_check

HARNESS = Path(__file__).resolve().parents[1]
PROBE_PATH = HARNESS / "health_check.py"


def configure(monkeypatch, project_root: Path):
    """Inject the adopted layout's roots without deriving them from a location."""
    resolved = health_check._roots.resolve(project_root)
    monkeypatch.setattr(health_check, "PROJECT_ROOT", resolved.project_root)
    monkeypatch.setattr(health_check, "ARGENTOS_ROOT", resolved.argentos_root)
    monkeypatch.setattr(health_check, "PROJECT_DIR", resolved.project_dir)
    return resolved


def test_probe_passes_in_the_adopted_layout(tmp_path, monkeypatch):
    configure(monkeypatch, tmp_path)

    result = health_check.probe()

    assert result["result"] == "PASS", result["evidence"]
    assert result["timestamp"]


def test_probe_cleans_up_probe_file(tmp_path, monkeypatch):
    resolved = configure(monkeypatch, tmp_path)

    health_check.probe()

    assert not (resolved.project_dir / ".state_check_probe").exists()


def test_probe_cli_exit_code_and_json(tmp_path):
    result = subprocess.run(
        [sys.executable, str(PROBE_PATH), "--project-root", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    output = json.loads(result.stdout)
    assert result.returncode == 0, output
    assert output["result"] == "PASS"


def test_probe_requires_project_root(monkeypatch):
    monkeypatch.setattr(health_check, "PROJECT_DIR", None)

    result = health_check.probe()

    assert result["result"] == "FAIL"
    assert "PROJECT_ROOT" in result["evidence"]


def test_probe_fails_on_unwritable_project_dir(monkeypatch, tmp_path):
    blocked = tmp_path / "blocked"
    monkeypatch.setattr(health_check, "PROJECT_DIR", blocked)
    # Simulate an unwritable artifacts directory by making the path a file.
    blocked.write_text("not a directory", encoding="utf-8")
    result = health_check.probe()
    assert result["result"] == "FAIL"
