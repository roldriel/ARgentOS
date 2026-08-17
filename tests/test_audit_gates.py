"""Tests for tools/audit_gates.py (dev-only; the validator subprocess is mocked)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import audit_gates  # noqa: E402


def make_report(tmp_path: Path, entry: str) -> Path:
    session = tmp_path / ".project" / "uuid" / "00"
    session.mkdir(parents=True)
    (session / "01-TASK_ANALYSIS.md").write_text("# Analysis\n", encoding="utf-8")
    report = tmp_path / ".project" / "uuid" / "HARNESS_REPORT.md"
    report.write_text(f"<!-- ENTRY: {entry} -->\n", encoding="utf-8")
    return report


def fake_result(returncode: int) -> subprocess.CompletedProcess:
    decision = "PASS" if returncode == 0 else "FAIL"
    return subprocess.CompletedProcess(
        ["python", "gate_validator.py"],
        returncode,
        stdout='{"decision": "%s"}' % decision,
        stderr="",
    )


def test_no_violations_when_structural_pass(tmp_path, monkeypatch):
    make_report(
        tmp_path,
        '{"timestamp": "t", "trigger": "H00", "transition": "A -> B", '
        '"result": "PASS", "checks": [], "artifact": ".project/uuid/00/01-TASK_ANALYSIS.md"}',
    )
    monkeypatch.setattr(audit_gates, "_run_validator", lambda *a, **k: fake_result(0))
    violations, summary = audit_gates.audit(tmp_path)
    assert violations == []
    assert summary["audited"] == 1


def test_violation_when_pass_but_structural_fail(tmp_path, monkeypatch):
    make_report(
        tmp_path,
        '{"timestamp": "t", "trigger": "H00", "transition": "A -> B", '
        '"result": "PASS", "checks": [], "artifact": ".project/uuid/00/01-TASK_ANALYSIS.md"}',
    )
    monkeypatch.setattr(audit_gates, "_run_validator", lambda *a, **k: fake_result(1))
    violations, summary = audit_gates.audit(tmp_path)
    assert len(violations) == 1
    assert "no deviation is recorded" in violations[0]


def test_override_with_deviation_ok(tmp_path, monkeypatch):
    make_report(
        tmp_path,
        '{"timestamp": "t", "trigger": "H00", "transition": "A -> B", '
        '"result": "PASS", "checks": [], "artifact": ".project/uuid/00/01-TASK_ANALYSIS.md", '
        '"deviation": {"cause": "trivial profile", "evidence": "01-TASK_ANALYSIS.md"}}',
    )
    monkeypatch.setattr(audit_gates, "_run_validator", lambda *a, **k: fake_result(1))
    violations, summary = audit_gates.audit(tmp_path)
    assert violations == []
    assert summary["overrides"] == 1


def test_unsupported_trigger_skipped(tmp_path, monkeypatch):
    make_report(
        tmp_path,
        '{"timestamp": "t", "trigger": "H15", "transition": "n/a", '
        '"result": "PASS", "checks": []}',
    )
    monkeypatch.setattr(audit_gates, "_run_validator", lambda *a, **k: fake_result(0))
    violations, summary = audit_gates.audit(tmp_path)
    assert violations == []
    assert summary["skipped"] == 1


def test_missing_artifact_skipped(tmp_path, monkeypatch):
    make_report(
        tmp_path,
        '{"timestamp": "t", "trigger": "H00", "transition": "A -> B", '
        '"result": "PASS", "checks": [], "artifact": ".project/uuid/00/ghost.md"}',
    )
    monkeypatch.setattr(audit_gates, "_run_validator", lambda *a, **k: fake_result(0))
    violations, summary = audit_gates.audit(tmp_path)
    assert violations == []
    assert summary["skipped"] == 1


def test_no_project_dir_is_ok(tmp_path):
    violations, summary = audit_gates.audit(tmp_path)
    assert violations == []
    assert summary["entries"] == 0
