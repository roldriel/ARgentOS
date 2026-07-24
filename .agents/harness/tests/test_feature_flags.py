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

from feature_flags import (
    DEFAULTS,
    FEATURES_TOML,
    INT_SETTINGS,
    get_setting,
    load_features,
)


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
    assert output == {**dict(DEFAULTS), **dict(INT_SETTINGS)}


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


def test_discovery_flags_are_registered(clean_env):
    """Discovery keys from features.toml must resolve, not be discarded."""
    flags = load_features()
    assert flags["llm_discovery"] is True
    assert flags["discovery_orchestrator"] is True
    assert flags["discovery_sample_size"] == 10
    assert flags["discovery_environment_ttl_hours"] == 6
    assert flags["discovery_project_ttl_hours"] == 24


def test_discovery_settings_env_override(clean_env, monkeypatch):
    monkeypatch.setenv("AGENTS_FEATURE_LLM_DISCOVERY", "false")
    monkeypatch.setenv("AGENTS_FEATURE_DISCOVERY_SAMPLE_SIZE", "25")
    flags = load_features()
    assert flags["llm_discovery"] is False
    assert get_setting("discovery_sample_size") == 25


def test_discovery_settings_invalid_env_override(clean_env, monkeypatch):
    monkeypatch.setenv("AGENTS_FEATURE_DISCOVERY_SAMPLE_SIZE", "not-an-int")
    with pytest.raises(ValueError):
        load_features()


def test_unknown_toml_keys_warn(clean_env, tmp_path):
    """Unknown keys in [features] must produce a warning, not silent ignore."""
    toml = tmp_path / "features.toml"
    toml.write_text("[features]\nrubrics = false\nmade_up_flag = true\n")
    with pytest.warns(UserWarning, match="Unknown feature flag 'made_up_flag'"):
        flags = load_features(toml)
    assert flags["rubrics"] is False
    assert "made_up_flag" not in flags


def test_registered_keys_do_not_warn(clean_env, tmp_path, recwarn):
    toml = tmp_path / "features.toml"
    toml.write_text(
        "[features]\nllm_discovery = true\ndiscovery_orchestrator = false\n"
        "discovery_sample_size = 5\ndiscovery_environment_ttl_hours = 1\n"
        "discovery_project_ttl_hours = 2\n"
    )
    load_features(toml)
    assert [w for w in recwarn.list if "Unknown feature flag" in str(w.message)] == []
