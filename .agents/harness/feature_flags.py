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
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FEATURES_TOML = PROJECT_ROOT / ".agents" / "features.toml"
ENV_PREFIX = "AGENTS_FEATURE_"

DEFAULTS: dict[str, bool] = {
    "decision_trees": True,
    "rubrics": True,
    "knowledge_base": True,
    "caveman": True,
    "project_discovery": True,
    "tdd": True,
    "srp": True,
    "ocp": True,
    "lsp": True,
    "isp": True,
    "dip": True,
    "screaming_architecture": True,
    "clean_architecture": True,
    "dry": True,
    "layered_architecture": True,
    "grasp": True,
    "ddd_tactical": True,
    "ddd_strategic": True,
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


def load_features(path: Path | None = None) -> dict[str, bool]:
    """Load feature flags from TOML and environment overrides."""
    path = path or FEATURES_TOML
    flags = dict(DEFAULTS)

    if path.exists():
        raw = path.read_text(encoding="utf-8")
        data = tomllib.loads(raw)
        toml_flags = data.get("features", {})
        for flag in flags:
            if flag in toml_flags:
                try:
                    flags[flag] = _toml_to_bool(toml_flags[flag])
                except ValueError as exc:
                    raise ValueError(
                        f"Invalid value for feature flag {flag!r} in {path}: {exc}"
                    ) from exc

    for flag in flags:
        override = _env_override(flag)
        if override is not None:
            flags[flag] = override

    return flags


def is_enabled(flag: str, path: Path | None = None) -> bool:
    """Return True if the named feature flag is enabled."""
    flags = load_features(path)
    if flag not in flags:
        raise KeyError(f"Unknown feature flag: {flag!r}")
    return flags[flag]


def all_flags(path: Path | None = None) -> dict[str, bool]:
    """Return a copy of the resolved feature flag map."""
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
