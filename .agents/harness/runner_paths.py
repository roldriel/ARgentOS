"""Shared filesystem locations for the harness runner modules."""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = PROJECT_ROOT / ".agents"
HARNESS_DIR = AGENTS_DIR / "harness"
POLICIES_DIR = AGENTS_DIR / "orchestrators" / "core" / "harness" / "policies"
POLICIES_DIRS = [
    POLICIES_DIR,
    AGENTS_DIR / "orchestrators" / "discovery" / "harness" / "policies",
    AGENTS_DIR / "orchestrators" / "system" / "harness" / "policies",
    HARNESS_DIR / "policies",
]
DECISION_TREE_DIRS = [
    AGENTS_DIR / "orchestrators" / "core" / "harness" / "decision_trees",
    AGENTS_DIR / "orchestrators" / "discovery" / "harness" / "decision_trees",
]
ARTIFACTS_DIR: Path = PROJECT_ROOT / ".project"
