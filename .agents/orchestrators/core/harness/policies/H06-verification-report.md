+++
trigger = "H06"
transition = "VERIFYING → COMPLETED"
artifact = "VERIFICATION_REPORT.md"
required_sections = [
  "Metadata",
  "Task Reference",
  "Execution Plan Reference",
  "Verification Objective",
  "Acceptance Criteria Evaluation",
  "Test Results",
  "Issues Found",
  "Final Decision",
  "Confidence",
  "State Transition"
]
rubric_validation = true
semantic_validation = true
semantic_checks = ["final_decision", "acceptance_criteria_evaluation"]
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H06
name: verification-report
state: core:VERIFYING
lifecycle: execution
gates:
  - "core:VERIFYING -> core:COMPLETED"
artifact_validated: VERIFICATION_REPORT.md
---

# Harness Policy H06: Verification Report

## Trigger

`VERIFYING → COMPLETED`

## Purpose

Validate that `VERIFICATION_REPORT.md` demonstrates the task was completed and verified before marking the session as completed.

## Input

- Current state: `VERIFYING`
- Target state: `COMPLETED`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md`
- Contract: `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`
- Reference: `TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md`

## Checklist

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence, required-section presence, and the EARS/rubric/semantic checks declared in this policy's front matter) or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. The artifact file exists. `[machine]`
2. The report summarizes what was verified. `[agent]`
3. Each acceptance criterion from `TASK_SPECIFICATION.md` is evaluated. `[agent]`
4. The report includes test results or equivalent evidence. `[agent]`
5. The report identifies any issues or failures. `[agent]`
6. The report explicitly recommends either `COMPLETED` or `RECOVERY`. `[machine]` (the runner's `final_decision` semantic check enforces the declared value)
7. If the recommendation is `COMPLETED`, all acceptance criteria are met. `[machine]` (the runner's `acceptance_criteria_evaluation` semantic check enforces that no criterion is `FAIL` and that `PARTIAL` criteria carry `action_plan`)
8. The report does not rely on assumptions to claim success. `[agent]`

The presence of the `required_sections` declared in this policy's front matter, and the `rubric_validation` declared in the front matter when the `rubrics` feature flag is enabled, are `[machine]` even though they are not restated as numbered items.

## Decision Criteria

- `PASS`: The report exists, recommends `COMPLETED`, and all acceptance criteria are met.
- `FAIL`: The report recommends `RECOVERY`, criteria are unmet, or the report is incomplete.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Transition to `RECOVERY`.
3. In recovery, decide whether to replan, request clarification, or abort.

## Semantic Validation Performed by Runner

The runner enforces the following semantic checks in addition to section presence:
- For H06: `decision.result` is `COMPLETED` and no acceptance criterion has `result: FAIL`; `PARTIAL` criteria must have `action_plan`. The only other valid decision value is `RECOVERY`.
