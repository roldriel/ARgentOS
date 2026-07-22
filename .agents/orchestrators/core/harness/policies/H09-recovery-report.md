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


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H09
name: recovery-report
state: core:RECOVERY
lifecycle: exception
gates:
  - "core:RECOVERY -> core:PLANNING"
artifact_validated: RECOVERY_REPORT.md
---

# Harness Policy H09: Recovery Report (optional)

## Trigger

`RECOVERY → PLANNING` (optional gate)

## Purpose

Validate that `RECOVERY_REPORT.md` exists and contains the required sections before replanning.

## Input

- Artifact: `.project/<session-uuid>/<iteration>/<order>-RECOVERY_REPORT.md`
- Contract: `.agents/orchestrators/core/contracts/RECOVERY_REPORT.md`

## Decision Criteria

- `PASS`: The artifact exists and contains all required sections.
- `FAIL`: The artifact is missing or incomplete.

## Note

This trigger is optional in the current state machine. The Orchestrator may invoke it when stricter validation is desired. It does not replace the recovery decision logic.
