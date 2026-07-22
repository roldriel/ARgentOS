+++
trigger = "H05"
transition = "EXECUTING → VERIFYING"
artifact = "EXECUTION_SUMMARY.md"
required_sections = [
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
  "Confidence"
]
semantic_validation = true
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H05
name: execution-completed
state: core:EXECUTING
lifecycle: execution
gates:
  - "core:EXECUTING -> core:VERIFYING"
artifact_validated: EXECUTION_SUMMARY.md
---

# Harness Policy H05: Execution Completed

## Trigger

`EXECUTING → VERIFYING`

## Purpose

Validate that the execution phase completed all planned steps and left the project in a verifiable state before verification begins.

## Input

- Current state: `EXECUTING`
- Target state: `VERIFYING`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-EXECUTION_SUMMARY.md`
- Reference: `.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md`

## Checklist

1. Every step in `EXECUTION_PLAN.md` has been executed or explicitly documented as skipped with justification.
2. No project files outside the plan scope were modified.
3. No unplanned requirements or assumptions were introduced.
4. Intermediate validations defined in the plan were run.
5. The project is in a verifiable state (tests can run, app can start, etc.).
6. No step caused an unrecoverable error.
7. For each practice listed in `technical_approach.enabled`, the `EXECUTION_SUMMARY.md` contains a corresponding entry in `## Technical Practice Evidence` with `applied` and, when applicable, supporting evidence.

## Decision Criteria

- `PASS`: All planned steps are complete and the project is verifiable.
- `FAIL`: Steps were skipped, scope was exceeded, or the project is not verifiable.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Transition to `RECOVERY`.
3. In recovery, decide whether to replan or request clarification.

## Semantic Validation Performed by Runner

The runner enforces the following semantic checks in addition to section presence:
- For H05: `EXECUTION_SUMMARY.md` exists, `final_state.status` is `VERIFIABLE`, and every step is `COMPLETED` or `SKIPPED` with notes.
