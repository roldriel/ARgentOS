"""Tests for tools/check_session_artifacts.py (dev-only, no payload dependency)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_session_artifacts as csa  # noqa: E402


def test_no_project_dir_is_ok(tmp_path):
    assert csa.scan(tmp_path) == []


def test_valid_artifacts_pass(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md").write_text(
        '<!-- ENTRY: {"timestamp": "t", "trigger": "H04", "transition": "A -> B", '
        '"result": "PASS", "checks": [{"id": "c", "result": "PASS", "evidence": "e"}]} -->\n',
        encoding="utf-8",
    )
    (tmp_path / ".project" / "uuid" / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "t", "type": "delegation", "phase": "06", '
        '"profile": null, "skills": [], "h15": "PASS"} -->\n',
        encoding="utf-8",
    )
    state = {
        "session": "uuid",
        "iteration": "00",
        "task_profile": "standard",
        "gates": {"H04": {"result": "PASS", "timestamp": "t"}},
        "last_gate": "H04",
        "status": "in_progress",
        "updated": "t",
    }
    (session / "state.json").write_text(json.dumps(state), encoding="utf-8")
    assert csa.scan(tmp_path) == []


def test_invalid_artifacts_flagged(tmp_path):
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md").write_text(
        "<!-- ENTRY: {not json -->\n", encoding="utf-8"
    )
    (tmp_path / ".project" / "uuid" / "METRICS.md").write_text(
        '<!-- METRIC: {"timestamp": "t", "type": "delegation"} -->\n'
        '<!-- METRIC: {"timestamp": "t", "type": "unknown_type"} -->\n',
        encoding="utf-8",
    )
    (session / "state.json").write_text('{"gates": {}}', encoding="utf-8")
    v = csa.scan(tmp_path)
    assert any("invalid JSON" in x for x in v)
    assert any("unknown type" in x for x in v)
    assert any("missing fields" in x and "METRIC" in x and "delegation" in x for x in v)
    assert any("missing fields" in x and "STATE" in x for x in v)
