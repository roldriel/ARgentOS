+++
trigger = "H01"
transition = "BUILDING_TASK_SPECIFICATION → TASK_READY"
artifact = "TASK_SPECIFICATION.md"
# Explicit subset of the contract sections (not derivable by reference).
required_sections = [
  "Objective",
  "Expected Outcome",
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
semantic_checks = ["technical_approach"]
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H01
name: task-specification
state: core:BUILDING_TASK_SPECIFICATION
lifecycle: task
gates:
  - "core:BUILDING_TASK_SPECIFICATION -> core:TASK_READY"
artifact_validated: TASK_SPECIFICATION.md
---

# Harness Policy H01: Task Specification

## Trigger

`BUILDING_TASK_SPECIFICATION → TASK_READY`

## Purpose

Validate that `TASK_SPECIFICATION.md` exists and complies with its contract before allowing the task to enter the context-gathering phase.

## Input

- Current state: `BUILDING_TASK_SPECIFICATION`
- Target state: `TASK_READY`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md`
- Contract: `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md`

## Checklist

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence, required-section presence, and the EARS/rubric/semantic checks declared in this policy's front matter) or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. The artifact file exists. `[machine]`
2. The artifact contains an `Objective` section. `[machine]`
3. The artifact contains an `Expected outcome` section. `[machine]`
4. The artifact contains a `Scope` section. `[machine]`
5. The artifact contains a `Constraints` section. `[machine]`
6. The artifact contains `Acceptance Criteria`. `[machine]`
7. The artifact contains `Assumptions`. `[machine]`
8. The artifact contains `Unknowns`. `[machine]`
9. The artifact contains a `Validation` section. `[machine]`
10. The acceptance criteria are specific and verifiable. `[agent]`
11. Each acceptance criterion follows one of the EARS patterns defined in `.agents/standards/requirements/EARS.md`. `[machine]`
12. No acceptance criterion is compound: it must describe a single action or condition. A criterion is compound when "and" or "or" separate independent actions or conditions (for example, "create X and send Y", "validate A or B"). A criterion is not compound when "and" or "or" enumerate values within the same domain (for example, "return HTTP 200 or 201", "accept JSON and XML"). `[agent]`
13. The scope is bounded and does not introduce unplanned work. `[agent]`
14. Every practice listed in `technical_approach.enabled` corresponds to an enabled technical-practice feature flag (for example, `tdd`, `srp`, `ocp`, `lsp`, `isp`, `dip`). `[machine]`
15. If `technical_approach.enabled` is non-empty, `technical_approach.notes` explains why each listed practice applies to this task. `[machine]` (notes present and non-empty) / `[agent]` (the explanation actually justifies each practice).
16. No acceptance criterion is derived from an unconfirmed assumption. `[agent]`
17. Every entry under `Assumptions` is an object with `assumption` text and an accessible `user_confirmed` field, or resolved through a prior clarification exchange. `[agent]`

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: Any required section is missing or any criterion is not met.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `BUILDING_TASK_SPECIFICATION` and re-invoke the Worker as `task_specification_writer`, or
3. Transition to `NEEDS_CLARIFICATION` if the specification cannot be completed without user input.
