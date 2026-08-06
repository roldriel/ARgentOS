"""Tests for runner_policies.resolve_required_sections (single-source sections).

The contract cited by a policy's `artifact` key is the source of truth for
required sections. Policies migrated in plan 24 no longer declare
`required_sections`; the runner derives them by reference. The EXPECTED lists
below are the pre-migration snapshots, kept as a permanent invariant: editing
a contract's sections intentionally updates the gate, editing them
accidentally fails here.
"""

from __future__ import annotations

import pytest

import runner_policies

EXPECTED = {
    "H00": [
        "Metadata",
        "User Request",
        "Interpreted Objective",
        "Expected Outcome",
        "Explicit Requirements",
        "Explicit Restrictions",
        "Detected Ambiguities",
        "Intent Confidence Assessment",
        "Sufficiency Assessment",
        "Recommended Next State",
        "Confidence",
    ],
    "H02": [
        "Metadata",
        "Task Reference",
        "Context Objective",
        "Project Context",
        "Relevant Components",
        "Existing Behavior",
        "Dependencies",
        "Constraints Discovered",
        "Available Evidence",
        "Unknowns",
        "Context Validation",
        "State",
    ],
    "H03": [
        "Metadata",
        "Context Reference",
        "Validation Objective",
        "Completeness Evaluation",
        "Relevance Evaluation",
        "Consistency Evaluation",
        "Risk Evaluation",
        "Validation Decision",
        "Required Actions",
        "Confidence",
        "State Transition",
    ],
    "H04": [
        "Metadata",
        "Task Reference",
        "Context Reference",
        "Objective",
        "Approach Summary",
        "Implementation Steps",
        "Affected Components",
        "Dependencies",
        "Risks",
        "Validation Strategy",
        "Rollback Considerations",
        "Plan Decision",
        "State Transition",
    ],
    "H05": [
        "Metadata",
        "Task Reference",
        "Execution Plan Reference",
        "Summary of Changes",
        "Steps Executed",
        "Project Files Modified",
        "Intermediate Validations",
        "Technical Practice Evidence",
        "Issues or Deviations",
        "Final Project State",
        "Confidence",
    ],
    "H09": [
        "Metadata",
        "Failure Reference",
        "Failure Summary",
        "Root Cause Classification",
        "Analysis Summary",
        "Corrective Action Recommendation",
        "Updated Artifacts",
        "Confidence",
    ],
    "H10": [
        "Discovery Objective",
        "Recommended Entries",
        "Context Budget Recommendation",
        "Notes",
    ],
    "H11": [
        "Metadata",
        "Original Request",
        "Detected Intent",
        "Reflection",
        "Confidence",
        "Correction Cycle",
        "User Response",
        "Next State",
    ],
}


@pytest.mark.parametrize("trigger", sorted(EXPECTED))
def test_resolved_sections_match_pre_migration_snapshot(trigger):
    policy = runner_policies.load_policy(trigger)
    front_matter = open(policy["_source"], encoding="utf-8").read().split("+++")[1]
    assert "required_sections" not in front_matter
    assert policy["required_sections"] == EXPECTED[trigger]


def test_explicit_subset_override_takes_precedence():
    policy = runner_policies.load_policy("H07")
    assert policy["required_sections"] == ["Scope Compliance"]


def test_resolution_fails_closed_on_missing_contract():
    with pytest.raises(ValueError, match="no contract declares it"):
        runner_policies.resolve_required_sections(
            {"trigger": "H99", "artifact": "NO_SUCH_ARTIFACT.md"}
        )
