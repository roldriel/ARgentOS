"""Tests for the .agents feature flag system."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = PROJECT_ROOT / ".agents" / "harness" / "runner.py"

from feature_flags import DEFAULTS, FEATURES_TOML, load_features


def run_features_cmd(env: dict[str, str] | None = None) -> tuple[int, dict]:
    cmd = [sys.executable, str(RUNNER_PATH), "features"]
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
    """Remove AGENTS_FEATURE_* env vars before each test."""
    for key in list(os.environ):
        if key.startswith("AGENTS_FEATURE_"):
            monkeypatch.delenv(key, raising=False)


def test_features_toml_parses(clean_env):
    flags = load_features()
    for flag in DEFAULTS:
        assert flag in flags
        assert isinstance(flags[flag], bool)


def test_features_env_override(clean_env, monkeypatch):
    monkeypatch.setenv("AGENTS_FEATURE_RUBRICS", "true")
    monkeypatch.setenv("AGENTS_FEATURE_DECISION_TREES", "1")
    monkeypatch.setenv("AGENTS_FEATURE_KNOWLEDGE_BASE", "false")
    monkeypatch.setenv("AGENTS_FEATURE_CAVEMAN", "0")

    flags = load_features()
    assert flags["rubrics"] is True
    assert flags["decision_trees"] is True
    assert flags["knowledge_base"] is False
    assert flags["caveman"] is False


def test_features_env_override_invalid(clean_env, monkeypatch):
    monkeypatch.setenv("AGENTS_FEATURE_RUBRICS", "not-a-bool")
    with pytest.raises(ValueError):
        load_features()


def test_features_toml_override_invalid(tmp_path, clean_env):
    bad_toml = tmp_path / "features.toml"
    bad_toml.write_text('[features]\nrubrics = "nope"\n')
    with pytest.raises(ValueError):
        load_features(bad_toml)


def test_features_subcommand_returns_json(clean_env):
    returncode, output = run_features_cmd()
    assert returncode == 0
    assert output == dict(DEFAULTS)


def test_features_subcommand_env_override(clean_env, monkeypatch):
    monkeypatch.setenv("AGENTS_FEATURE_KNOWLEDGE_BASE", "true")
    returncode, output = run_features_cmd()
    assert returncode == 0
    assert output["knowledge_base"] is True


def test_features_subcommand_caveman_env_override(clean_env, monkeypatch):
    monkeypatch.setenv("AGENTS_FEATURE_CAVEMAN", "false")
    returncode, output = run_features_cmd()
    assert returncode == 0
    assert output["caveman"] is False
