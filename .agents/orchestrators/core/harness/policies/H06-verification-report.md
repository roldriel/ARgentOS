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

1. The artifact file exists.
2. The report summarizes what was verified.
3. Each acceptance criterion from `TASK_SPECIFICATION.md` is evaluated.
4. The report includes test results or equivalent evidence.
5. The report identifies any issues or failures.
6. The report explicitly recommends either `COMPLETED` or `RECOVERY`.
7. If the recommendation is `COMPLETED`, all acceptance criteria are met.
8. The report does not rely on assumptions to claim success.

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
