"""Task profile model for the harness runner.

Every session's TASK_ANALYSIS.md assigns a task profile (`trivial`,
`standard`, or `complex`) that determines which harness gates are mandatory
for the task. Gates a profile does not require are not silently absent: when
the runner is invoked for one of them, it records the gate as
`skipped: profile` instead of validating.
"""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import re

from runner_artifacts import artifact_path

VALID_PROFILES = ("trivial", "standard", "complex")

# Gates mandatory for the `trivial` profile. `standard` and `complex` require
# every gate, so they have no entry: a profile absent from this mapping
# requires the full cycle.
PROFILE_REQUIRED_TRIGGERS = {
    "trivial": {"H00", "H05", "H10"},
}

_PROFILE_VALUE_RE = re.compile(r'^\s*value\s*=\s*"([^"]+)"', re.MULTILINE)


def read_task_profile(session_uuid: str) -> str:
    """Return the task profile recorded in the session's TASK_ANALYSIS.md.

    The profile is read from the `value` key of the `Task Profile` section of
    the latest TASK_ANALYSIS.md found across the session's iterations. A
    missing artifact, a missing field, or an unrecognized value resolves to
    `standard`: when in doubt, the full cycle applies.
    """
    path = artifact_path(session_uuid, "TASK_ANALYSIS.md")
    if not path.exists():
        return "standard"
    content = path.read_text(encoding="utf-8")
    section = re.search(
        r"^##\s+Task Profile\s*\n(.*?)(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not section:
        return "standard"
    match = _PROFILE_VALUE_RE.search(section.group(1))
    if match and match.group(1) in VALID_PROFILES:
        return match.group(1)
    return "standard"


def is_gate_required(trigger: str, profile: str) -> bool:
    """Return True when the gate is mandatory for the given task profile."""
    required = PROFILE_REQUIRED_TRIGGERS.get(profile)
    if required is None:
        return True
    return trigger in required
