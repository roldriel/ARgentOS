"""Coverage invariant: every recovery-gated policy declares a decision table.

Each harness policy whose failure routes to recovery carries a
``## Recovery Decision Table`` section (the prose replacement of the former
TOML decision trees). The documented exemptions (H09, H10 — generic fallback
only; S00 — system gate; H13 — suite-enforced taxonomy policy) intentionally
have none.
"""

from __future__ import annotations

import sys
from pathlib import Path

_harness_dir = Path(__file__).resolve().parents[1]
if str(_harness_dir) not in sys.path:
    sys.path.insert(0, str(_harness_dir))

import runner_markdown
import runner_paths

POLICIES_WITH_RECOVERY_TABLE = {
    "H00",
    "H01",
    "H02",
    "H03",
    "H04",
    "H05",
    "H06",
    "H07",
    "H11",
    "H15",
    "D00",
    "D01",
}

EXEMPT_TRIGGERS = {"H09", "H10", "H13", "S00"}


def _policy_files() -> dict[str, Path]:
    files: dict[str, Path] = {}
    for policies_dir in runner_paths.POLICIES_DIRS:
        if not policies_dir.is_dir():
            continue
        for path in sorted(policies_dir.glob("*.md")):
            try:
                meta = runner_markdown.parse_front_matter(
                    path.read_text(encoding="utf-8")
                )
            except ValueError:
                continue
            if meta.get("trigger"):
                files[meta["trigger"]] = path
    return files


def test_every_expected_policy_has_recovery_table():
    policies = _policy_files()
    for trigger in POLICIES_WITH_RECOVERY_TABLE:
        path = policies.get(trigger)
        assert path is not None, f"policy for {trigger} not found"
        content = path.read_text(encoding="utf-8")
        assert "## Recovery Decision Table" in content, (
            f"{path.name} lacks a Recovery Decision Table section"
        )
        for action in ("RECOVERY_GENERIC",):
            assert action in content, f"{path.name} table lacks {action}"


def test_exempt_policies_have_no_recovery_table():
    policies = _policy_files()
    for trigger in EXEMPT_TRIGGERS:
        path = policies.get(trigger)
        if path is None:
            continue
        content = path.read_text(encoding="utf-8")
        assert "## Recovery Decision Table" not in content, (
            f"{path.name} is exempt but declares a Recovery Decision Table"
        )


def test_no_unexpected_policy_lacks_a_decision():
    """Every recovery-routing policy is either listed or explicitly exempt."""
    policies = _policy_files()
    unknown = set(policies) - POLICIES_WITH_RECOVERY_TABLE - EXEMPT_TRIGGERS
    assert not unknown, f"unclassified policies: {sorted(unknown)}"
