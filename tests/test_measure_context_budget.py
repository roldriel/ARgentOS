"""Tests for tools/measure_context_budget.py (dev-only, no payload dependency)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import measure_context_budget as mcb  # noqa: E402


def test_string_entries_measured():
    payload = {
        "context_budget": 100,
        "knowledge_entries": ["abcd", "abcdefgh"],  # 1 + 2 = 3 tokens
    }
    assert mcb.measure(payload) == {
        "declared": 100,
        "consumed": 3,
        "overrun": False,
    }


def test_object_entries_use_lessons_learned():
    payload = {
        "context_budget": 10,
        "knowledge_entries": [
            {"session_uuid": "u", "objective": "ignored", "lessons_learned": "abcdefghijkl"},  # 3 tokens
        ],
    }
    report = mcb.measure(payload)
    assert report["consumed"] == 3
    assert report["overrun"] is False


def test_overrun_flagged():
    payload = {"context_budget": 2, "knowledge_entries": ["abcdefghijkl"]}  # 3 tokens
    report = mcb.measure(payload)
    assert report["consumed"] == 3
    assert report["overrun"] is True


def test_missing_budget_flagged_as_overrun():
    payload = {"knowledge_entries": ["abcdefghijkl"]}
    report = mcb.measure(payload)
    assert report["declared"] == 0
    assert report["overrun"] is True


def test_cli_exit_codes(tmp_path):
    ok = tmp_path / "ok.json"
    ok.write_text(
        '{"context_budget": 100, "knowledge_entries": ["abcd"]}',
        encoding="utf-8",
    )
    bad = tmp_path / "bad.json"
    bad.write_text(
        '{"context_budget": 1, "knowledge_entries": ["abcdefghijkl"]}',
        encoding="utf-8",
    )
    res_ok = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "measure_context_budget.py"), "--payload", str(ok)],
        capture_output=True,
        text=True,
    )
    res_bad = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "measure_context_budget.py"), "--payload", str(bad)],
        capture_output=True,
        text=True,
    )
    assert res_ok.returncode == 0
    assert res_bad.returncode == 1


def test_cli_phase_and_iteration_in_report(tmp_path):
    payload = tmp_path / "delegation.json"
    payload.write_text(
        '{"context_budget": 100, "knowledge_entries": ["abcd"]}',
        encoding="utf-8",
    )
    res = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "measure_context_budget.py"),
            "--payload",
            str(payload),
            "--phase",
            "06",
            "--iteration",
            "00",
        ],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    report = json.loads(res.stdout)
    assert report["phase"] == "06"
    assert report["iteration"] == "00"
    assert report["declared"] == 100
    assert report["consumed"] == 1
