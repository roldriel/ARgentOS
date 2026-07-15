+++
trigger = "H04"
transition = "PLANNING → PLAN_READY"
artifact = "EXECUTION_PLAN.md"
required_sections = [
  "Metadata",
  "Task Reference",
  "Context Reference",
  "Objective",
  "Approach Summary",
  "Implementation Steps",
  "Affected Components",
  "Dependencies",
  "Risks",
  "Validation Strategy",
  "Rollback Considerations",
  "Plan Decision",
  "State Transition"
]
+++

# Harness Policy H04: Execution Plan

## Trigger

`PLANNING → PLAN_READY`

## Purpose

Validate that `EXECUTION_PLAN.md` defines an executable, safe, and scope-respecting strategy.

## Input

- Current state: `PLANNING`
- Target state: `PLAN_READY`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md`
- Contract: `.agents/contracts/EXECUTION_PLAN.md`
- Reference: `TASK_SPECIFICATION.md`, `CONTEXT_ARTIFACT.md`, `CONTEXT_VALIDATION_REPORT.md`

## Checklist

1. The artifact file exists.
2. The plan addresses the task objective.
3. The plan uses validated context (no invented assumptions).
4. The plan defines executable, ordered steps.
5. Each step specifies what, where, and why.
6. The plan identifies risks and mitigation strategies.
7. The plan defines a verification strategy.
8. The plan does not depend on unresolved unknowns.
9. The plan does not exceed the task scope.
10. The plan is compatible with the existing architecture and conventions.

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: The plan is unsafe, incomplete, out of scope, or depends on unresolved unknowns.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `PLANNING` and re-invoke the Worker as `planner`, or
3. Transition to `NEEDS_CLARIFICATION` if the plan cannot be completed safely.
