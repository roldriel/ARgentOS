+++
trigger = "H09"
transition = "RECOVERY → PLANNING (optional)"
artifact = "RECOVERY_REPORT.md"
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
**Structural validator:** the Orchestrator MUST run `python .argentos/.agents/harness/gate_validator.py --project-root <PROJECT_ROOT> --trigger H09 --artifact <path>` before judging PASS; a structural FAIL blocks PASS unless recorded as a documented deviation.

**Evaluation audience:** the harness runner no longer exists; both criteria are evaluated by the Orchestrator's judgment when the gate fires (artifact existence and presence of the sections required by the artifact contract). A structural failure is checkable without interpretation; this policy contains no purely agent-judgment items.

- `PASS`: The artifact exists and contains all required sections (verified by the Orchestrator against the contract cited in §"Input").
- `FAIL`: The artifact is missing or incomplete.

## Note

This trigger is optional in the current state machine. The Orchestrator may invoke it when stricter validation is desired. It does not replace the recovery decision logic.
