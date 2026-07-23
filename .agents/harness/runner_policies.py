"""Policy loading for the harness runner."""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

from typing import Any

import runner_markdown
import runner_paths


def load_policy(trigger: str) -> dict[str, Any]:
    # Policies are named like H01-task-specification.md, H02-context-artifact.md, etc.
    # Require an exact prefix match "<trigger>-" to avoid ambiguous globs.
    # Policies are searched in every domain: core (H*), discovery (D*),
    # system (S*) and cross-cutting (.agents/harness/policies, e.g. H13).
    candidates = []
    for policies_dir in runner_paths.POLICIES_DIRS:
        candidates = list(policies_dir.glob(f"{trigger}-*.md"))
        if not candidates:
            candidates = list(policies_dir.glob(f"{trigger.lower()}-*.md"))
        if candidates:
            break
    if not candidates:
        raise FileNotFoundError(f"Policy not found for trigger {trigger}")
    if len(candidates) > 1:
        raise FileNotFoundError(
            f"Multiple policies found for trigger {trigger}: {', '.join(str(c) for c in candidates)}"
        )

    policy_path = candidates[0]
    content = policy_path.read_text(encoding="utf-8")
    meta = runner_markdown.parse_front_matter(content)
    meta["_source"] = str(policy_path)
    return meta

