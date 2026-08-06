"""Tests for sync_required_sections (policy/contract section sync)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import sync_required_sections as sync

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = PROJECT_ROOT / ".agents" / "harness" / "sync_required_sections.py"


def test_policies_are_in_sync_with_contracts():
    """Fails when any policy required_sections drift from its contract."""
    assert sync.sync_policies(check=True) == 0


def test_check_mode_detects_drift(tmp_path, monkeypatch):
    policies = tmp_path / "policies"
    contracts = tmp_path / "contracts"
    policies.mkdir()
    contracts.mkdir()

    (contracts / "WIDGET.md").write_text(
        '+++\nartifact = "WIDGET.md"\n+++\n\n'
        "# Widget Contract\n\n## Purpose\n\nDoc.\n\n"
        "# Widget\n\n## Alpha\n\n## Beta\n",
        encoding="utf-8",
    )
    (policies / "H99-widget.md").write_text(
        "+++\n"
        'trigger = "H99"\n'
        'artifact = "WIDGET.md"\n'
        'required_sections = [\n  "Beta",\n  "Nonexistent"\n]\n'
        "+++\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(sync, "POLICIES_DIRS", [policies])
    monkeypatch.setattr(
        sync, "load_contract_map", lambda: {"WIDGET.md": contracts / "WIDGET.md"}
    )

    assert sync.sync_policies(check=True) == 1


def test_sync_fixes_case_and_order(tmp_path, monkeypatch):
    policies = tmp_path / "policies"
    contracts = tmp_path / "contracts"
    policies.mkdir()
    contracts.mkdir()

    (contracts / "WIDGET.md").write_text(
        '+++\nartifact = "WIDGET.md"\n+++\n\n'
        "# Widget Contract\n\n## Purpose\n\nDoc.\n\n"
        "# Widget\n\n## Alpha\n\n## Beta\n",
        encoding="utf-8",
    )
    policy = policies / "H99-widget.md"
    policy.write_text(
        "+++\n"
        'trigger = "H99"\n'
        'artifact = "WIDGET.md"\n'
        'required_sections = [\n  "beta",\n  "Alpha"\n]\n'
        "+++\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(sync, "POLICIES_DIRS", [policies])
    monkeypatch.setattr(
        sync, "load_contract_map", lambda: {"WIDGET.md": contracts / "WIDGET.md"}
    )

    assert sync.sync_policies(check=False) == 0
    updated = policy.read_text(encoding="utf-8")
    assert '"Alpha",\n  "Beta"' in updated
    assert sync.sync_policies(check=True) == 0


def test_sync_script_cli_check_passes():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
