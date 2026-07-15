"""Tests for the .agents protocol health check."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = PROJECT_ROOT / ".agents" / "harness" / "runner.py"
LAST_HEALTH_CHECK_FILE = PROJECT_ROOT / ".project" / ".last_health_check"

import feature_flags
import health_check


def run_health_check_cmd(env: dict[str, str] | None = None) -> tuple[int, dict]:
    cmd = [sys.executable, str(RUNNER_PATH), "health-check"]
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
    )
    try:
        output = json.loads(result.stdout) if result.stdout else {}
    except json.JSONDecodeError:
        output = {"raw_stdout": result.stdout, "stderr": result.stderr}
    return result.returncode, output


@pytest.fixture
def clean_env(monkeypatch):
    for key in list(os.environ):
        if key.startswith("AGENTS_FEATURE_") or key == "AGENTS_HEALTH_CHECK_TTL_HOURS":
            monkeypatch.delenv(key, raising=False)


def test_health_check_passes_on_valid_protocol(clean_env):
    returncode, output = run_health_check_cmd()
    assert returncode == 0
    assert output["result"] == "PASS"


def test_health_check_fails_on_missing_directory(clean_env, monkeypatch, tmp_path):
    fake_root = tmp_path / "agents"
    fake_root.mkdir()
    monkeypatch.setattr(health_check, "AGENTS_DIR", fake_root)
    monkeypatch.setattr(health_check, "HARNESS_DIR", fake_root / "harness")

    result = health_check.run_health_check()
    assert result.result == "FAIL"
    assert any("Missing directory" in c["evidence"] for c in result.checks)


def test_health_check_fails_on_invalid_toml(clean_env, monkeypatch, tmp_path):
    monkeypatch.setenv("AGENTS_FEATURE_DECISION_TREES", "true")
    fake_trees = tmp_path / "decision_trees"
    fake_trees.mkdir(parents=True)
    bad_toml = fake_trees / "H01_FAIL.toml"
    bad_toml.write_text("this is not valid toml [[", encoding="utf-8")
    monkeypatch.setattr(health_check, "DECISION_TREES_DIR", fake_trees)

    result = health_check.run_health_check()
    assert result.result == "FAIL"
    assert any("TOML error" in c["evidence"] for c in result.checks)


def _write_minimal_tree(directory: Path, trigger: str, cycle: bool = False) -> None:
    if cycle:
        body = """
[nodes.start]
condition = "true"

[nodes.start.true]
next = "middle"

[nodes.start.false]
action = "ABORT"

[nodes.middle]
condition = "true"

[nodes.middle.true]
next = "start"

[nodes.middle.false]
action = "ABORT"
"""
    else:
        body = """
[nodes.start]
condition = "true"

[nodes.start.true]
action = "ABORT"

[nodes.start.false]
action = "ABORT"
"""
    (directory / f"{trigger}_FAIL.toml").write_text(body, encoding="utf-8")


def test_health_check_fails_on_cycle(clean_env, monkeypatch, tmp_path):
    monkeypatch.setenv("AGENTS_FEATURE_DECISION_TREES", "true")
    fake_trees = tmp_path / "decision_trees"
    fake_trees.mkdir(parents=True)
    triggers = [f"H{i:02d}" for i in range(8)] + ["H11"]
    for trigger in triggers:
        _write_minimal_tree(fake_trees, trigger, cycle=(trigger == "H01"))
    monkeypatch.setattr(health_check, "DECISION_TREES_DIR", fake_trees)

    result = health_check.run_health_check()
    assert result.result == "FAIL"
    assert any("Cycle detected" in c["evidence"] for c in result.checks)


def test_last_health_check_is_updated(clean_env):
    if LAST_HEALTH_CHECK_FILE.exists():
        LAST_HEALTH_CHECK_FILE.unlink()
    result = health_check.run_health_check()
    assert result.result == "PASS"
    assert LAST_HEALTH_CHECK_FILE.exists()
    timestamp = datetime.fromisoformat(
        LAST_HEALTH_CHECK_FILE.read_text(encoding="utf-8").strip()
    )
    assert timestamp.tzinfo is not None


def test_should_run_health_check_when_missing(clean_env):
    if LAST_HEALTH_CHECK_FILE.exists():
        LAST_HEALTH_CHECK_FILE.unlink()
    assert health_check.should_run_health_check() is True


def test_should_run_health_check_after_ttl(clean_env, monkeypatch):
    old = datetime.now(timezone.utc) - timedelta(hours=25)
    LAST_HEALTH_CHECK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LAST_HEALTH_CHECK_FILE.write_text(old.isoformat(), encoding="utf-8")
    assert health_check.should_run_health_check(ttl_hours=24) is True


def test_should_skip_health_check_within_ttl(clean_env, monkeypatch):
    recent = datetime.now(timezone.utc) - timedelta(hours=1)
    LAST_HEALTH_CHECK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LAST_HEALTH_CHECK_FILE.write_text(recent.isoformat(), encoding="utf-8")
    assert health_check.should_run_health_check(ttl_hours=24) is False


def test_health_check_ttl_env_override(clean_env, monkeypatch):
    monkeypatch.setenv("AGENTS_HEALTH_CHECK_TTL_HOURS", "12")
    assert feature_flags.health_check_ttl_hours() == 12
