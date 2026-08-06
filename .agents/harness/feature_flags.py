#!/usr/bin/env python3
"""
Feature flag loader for the .agents protocol.

Priority (highest first):
1. Environment variables with prefix AGENTS_FEATURE_<FLAG>
2. `.agents/features.toml`
3. Defaults defined in this module
"""

from __future__ import annotations

import os
import tomllib
import warnings
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FEATURES_TOML = PROJECT_ROOT / ".agents" / "features.toml"
ENV_PREFIX = "AGENTS_FEATURE_"

import technical_practices

DEFAULTS: dict[str, bool] = {
    "decision_trees": True,
    "rubrics": True,
    "knowledge_base": True,
    "caveman": True,
    # Discovery subsystem boolean flags (consumed declaratively by the
    # discovery agents; no harness code reads them yet).
    "llm_discovery": True,
    "discovery_orchestrator": True,
    # Technical-practice flags default to True and come from the canonical
    # catalog in technical_practices.py.
    **{flag: True for flag in technical_practices.TECHNICAL_PRACTICES},
    # Declared in features.toml but without a rubric/standard catalog entry
    # yet; defaults to disabled (see technical_practices.TECHNICAL_PRACTICES).
    "architecture_contract": False,
}

# Non-boolean discovery settings. Like the boolean flags, they resolve from
# `.agents/features.toml` [features] with an AGENTS_FEATURE_<NAME> override.
INT_SETTINGS: dict[str, int] = {
    "discovery_sample_size": 10,
    "discovery_environment_ttl_hours": 6,
    "discovery_project_ttl_hours": 24,
}


def _toml_to_bool(value: Any) -> bool:
    """Coerce a TOML value to bool, raising ValueError on unsupported types."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "1", "yes", "on"):
            return True
        if normalized in ("false", "0", "no", "off"):
            return False
        raise ValueError(f"Cannot coerce string to bool: {value!r}")
    raise ValueError(f"Cannot coerce {type(value).__name__} to bool")


def _env_override(flag: str) -> bool | None:
    """Return the environment override for a flag, or None if not set."""
    env_name = f"{ENV_PREFIX}{flag.upper()}"
    value = os.environ.get(env_name)
    if value is None:
        return None
    try:
        return _toml_to_bool(value)
    except ValueError as exc:
        raise ValueError(
            f"Environment variable {env_name}={value!r} is not a valid boolean"
        ) from exc


def _env_int_override(name: str) -> int | None:
    """Return the environment override for an int setting, or None if not set."""
    env_name = f"{ENV_PREFIX}{name.upper()}"
    value = os.environ.get(env_name)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(
            f"Environment variable {env_name}={value!r} is not a valid integer"
        ) from exc


def load_features(path: Path | None = None) -> dict[str, Any]:
    """Load feature flags and settings from TOML and environment overrides.

    Returns the resolved map of boolean flags (DEFAULTS) and integer settings
    (INT_SETTINGS). Unknown keys in the TOML file produce a warning instead of
    being silently discarded.
    """
    path = path or FEATURES_TOML
    flags: dict[str, Any] = dict(DEFAULTS)
    settings: dict[str, int] = dict(INT_SETTINGS)

    if path.exists():
        raw = path.read_text(encoding="utf-8")
        data = tomllib.loads(raw)
        toml_flags = data.get("features", {})
        known = set(flags) | set(settings)
        for key in toml_flags:
            if key not in known:
                warnings.warn(
                    f"Unknown feature flag {key!r} in {path}; ignoring it",
                    stacklevel=2,
                )
        for flag in flags:
            if flag in toml_flags:
                try:
                    flags[flag] = _toml_to_bool(toml_flags[flag])
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid value for feature flag {flag!r} in {path}: {exc}"
                    ) from exc
        for name in settings:
            if name in toml_flags:
                try:
                    settings[name] = int(toml_flags[name])
                except (ValueError, TypeError) as exc:
                    raise ValueError(
                        f"Invalid value for setting {name!r} in {path}: "
                        f"{toml_flags[name]!r} is not a valid integer"
                    ) from exc

    for flag in flags:
        override = _env_override(flag)
        if override is not None:
            flags[flag] = override

    for name in settings:
        override = _env_int_override(name)
        if override is not None:
            settings[name] = override

    return {**flags, **settings}


def is_enabled(flag: str, path: Path | None = None) -> bool:
    """Return True if the named feature flag is enabled."""
    flags = load_features(path)
    if flag not in flags:
        raise KeyError(f"Unknown feature flag: {flag!r}")
    value = flags[flag]
    if not isinstance(value, bool):
        raise KeyError(f"Feature flag {flag!r} is not boolean (value: {value!r})")
    return value


def get_setting(name: str, path: Path | None = None) -> int:
    """Return the resolved value of a non-boolean setting."""
    flags = load_features(path)
    if name not in INT_SETTINGS:
        raise KeyError(f"Unknown setting: {name!r}")
    return int(flags[name])


def all_flags(path: Path | None = None) -> dict[str, Any]:
    """Return a copy of the resolved feature flag and settings map."""
    return dict(load_features(path))


def load_health_check_config(path: Path | None = None) -> dict[str, Any]:
    """Load health-check configuration from TOML and environment overrides."""
    path = path or FEATURES_TOML
    config: dict[str, Any] = {"ttl_hours": 24}

    if path.exists():
        raw = path.read_text(encoding="utf-8")
        data = tomllib.loads(raw)
        toml_config = data.get("health_check", {})
        if "ttl_hours" in toml_config:
            try:
                config["ttl_hours"] = int(toml_config["ttl_hours"])
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Invalid ttl_hours value in {path}: {toml_config['ttl_hours']!r}"
                ) from exc

    env_ttl = os.environ.get("AGENTS_HEALTH_CHECK_TTL_HOURS")
    if env_ttl is not None:
        try:
            config["ttl_hours"] = int(env_ttl)
        except ValueError as exc:
            raise ValueError(
                f"Invalid AGENTS_HEALTH_CHECK_TTL_HOURS value: {env_ttl!r}"
            ) from exc

    return config


def health_check_ttl_hours(path: Path | None = None) -> int:
    """Return the configured health-check TTL in hours."""
    return load_health_check_config(path)["ttl_hours"]
