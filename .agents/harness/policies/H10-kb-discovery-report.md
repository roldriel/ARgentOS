+++
trigger = "H10"
transition = "Before using KB discovery (optional)"
artifact = "KB_DISCOVERY_REPORT.md"
required_sections = [
  "Discovery Objective",
  "Recommended Entries",
  "Context Budget Recommendation",
  "Notes"
]
+++

# Harness Policy H10: KB Discovery Report (optional)

## Trigger

Before using KB discovery (optional gate)

## Purpose

Validate that `KB_DISCOVERY_REPORT.md` exists and contains the required sections when the knowledge_base feature is enabled.

## Input

- Artifact: `.project/<session-uuid>/<iteration>/<order>-KB_DISCOVERY_REPORT.md`
- Contract: `.agents/contracts/KB_DISCOVERY_REPORT.md`

## Decision Criteria

- `PASS`: The artifact exists and contains all required sections.
- `FAIL`: The artifact is missing or incomplete.

## Note

This trigger is optional in the current state machine. The Orchestrator may invoke it when the `knowledge_base` feature flag is enabled and stricter validation is desired.
