+++
trigger = "H01"
transition = "BUILDING_TASK_SPECIFICATION → TASK_READY"
artifact = "TASK_SPECIFICATION.md"
required_sections = [
  "Objective",
  "Expected outcome",
  "Scope",
  "Constraints",
  "Acceptance Criteria",
  "Assumptions",
  "Unknowns",
  "Validation"
]
ears_validation = true
ears_section = "Acceptance Criteria"
semantic_validation = true
+++

# Harness Policy H01: Task Specification

## Trigger

`BUILDING_TASK_SPECIFICATION → TASK_READY`

## Purpose

Validate that `TASK_SPECIFICATION.md` exists and complies with its contract before allowing the task to enter the context-gathering phase.

## Input

- Current state: `BUILDING_TASK_SPECIFICATION`
- Target state: `TASK_READY`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md`
- Contract: `.agents/contracts/TASK_SPECIFICATION.md`

## Checklist

1. The artifact file exists.
2. The artifact contains an `Objective` section.
3. The artifact contains an `Expected outcome` section.
4. The artifact contains a `Scope` section.
5. The artifact contains a `Constraints` section.
6. The artifact contains `Acceptance Criteria`.
7. The artifact contains `Assumptions`.
8. The artifact contains `Unknowns`.
9. The artifact contains a `Validation` section.
10. The acceptance criteria are specific and verifiable.
11. Each acceptance criterion follows one of the EARS patterns defined in `.agents/standards/requirements/EARS.md`.
12. No acceptance criterion is compound (contains "and" or "or" connecting multiple requirements).
13. The scope is bounded and does not introduce unplanned work.
14. Every practice listed in `technical_approach.enabled` corresponds to an enabled technical-practice feature flag (for example, `tdd`, `srp`, `ocp`, `lsp`, `isp`, `dip`).
15. If `technical_approach.enabled` is non-empty, `technical_approach.notes` explains why each listed practice applies to this task.
16. No acceptance criterion is derived from an unconfirmed assumption.
17. Every entry under `Assumptions` is explicitly marked as `user_confirmed` or resolved through a prior clarification exchange.

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: Any required section is missing or any criterion is not met.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `BUILDING_TASK_SPECIFICATION` and re-invoke the Worker as `task_specification_writer`, or
3. Transition to `NEEDS_CLARIFICATION` if the specification cannot be completed without user input.
