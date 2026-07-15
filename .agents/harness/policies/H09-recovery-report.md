+++
trigger = "H09"
transition = "RECOVERY → PLANNING (optional)"
artifact = "RECOVERY_REPORT.md"
required_sections = [
  "Metadata",
  "Failure Reference",
  "Failure Summary",
  "Root Cause Classification",
  "Analysis Summary",
  "Corrective Action Recommendation",
  "Updated Artifacts",
  "Confidence"
]
+++

# Harness Policy H09: Recovery Report (optional)

## Trigger

`RECOVERY → PLANNING` (optional gate)

## Purpose

Validate that `RECOVERY_REPORT.md` exists and contains the required sections before replanning.

## Input

- Artifact: `.project/<session-uuid>/<iteration>/<order>-RECOVERY_REPORT.md`
- Contract: `.agents/contracts/RECOVERY_REPORT.md`

## Decision Criteria

- `PASS`: The artifact exists and contains all required sections.
- `FAIL`: The artifact is missing or incomplete.

## Note

This trigger is optional in the current state machine. The Orchestrator may invoke it when stricter validation is desired. It does not replace the recovery decision logic.
