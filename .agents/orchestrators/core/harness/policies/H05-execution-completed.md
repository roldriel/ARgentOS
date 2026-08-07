+++
trigger = "H05"
transition = "EXECUTING → VERIFYING"
artifact = "EXECUTION_SUMMARY.md"
semantic_validation = true
semantic_checks = ["execution_summary", "technical_practice_evidence"]
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

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence, required-section presence, and the semantic checks declared in this policy's front matter) or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. Every step in `EXECUTION_PLAN.md` has been executed or explicitly documented as skipped with justification. `[machine]` (the runner's `execution_summary` semantic check enforces that every step is `COMPLETED` or `SKIPPED` with notes)
2. No project files outside the plan scope were modified. `[agent]`
3. No unplanned requirements or assumptions were introduced. `[agent]`
4. Intermediate validations defined in the plan were run. `[agent]`
5. The project is in a verifiable state (tests can run, app can start, etc.). `[agent]` (the runner verifies the declared value `final_state.status = VERIFIABLE`; judging that the project is actually verifiable is agent judgment)
6. No step caused an unrecoverable error. `[agent]`
7. For each practice listed in `technical_approach.enabled`, the `EXECUTION_SUMMARY.md` contains a corresponding entry in `## Technical Practice Evidence` with `applied` and, when applicable, supporting evidence. `[machine]` (the runner's `technical_practice_evidence` semantic check)

The presence of the `required_sections` resolved by the runner from the artifact contract is `[machine]` even though it is not restated as a numbered item.

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

## Recovery Decision Table

When H05 fails, the Orchestrator populates the context variables from the session (`project_unrecoverable`, `execution_blocked`, `execution_complete`) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `project_unrecoverable == true` | `ABORT` | — | — | Project state is unrecoverable; abort session. |
| 2 | `execution_blocked == true` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Execution blocked by unexpected issue. |
| 3 | `execution_complete == false` | `RETRY_WORKER` | `06-execute.md` | `executor` | Some steps remain pending; retry executor. |
| 4 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Execution validation failed; falling back to generic recovery. |
