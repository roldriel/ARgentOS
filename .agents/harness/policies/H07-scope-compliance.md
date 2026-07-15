+++
trigger = "H07"
transition = "VERIFYING → COMPLETED"
artifact = "VERIFICATION_REPORT.md"
required_sections = [
  "Scope Compliance"
]
semantic_validation = true
+++

# Harness Policy H07: Scope Compliance

## Trigger

`VERIFYING → COMPLETED`

## Purpose

Validate that the executed work stayed strictly within the task assigned by the user and that the agent did not take autonomous liberties or perform unrequested work.

## Input

- Current state: `VERIFYING`
- Target state: `COMPLETED`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md`
- Contract: `.agents/contracts/VERIFICATION_REPORT.md`
- Reference: `TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md`

## Checklist

1. The artifact contains a `Scope Compliance` section.
2. The section declares whether the work respected the assigned scope.
3. Any project file, dependency, configuration, or test modified outside the execution plan is listed in `unplanned_changes`.
4. Any error, bug, or inconsistency discovered outside the assigned task scope is listed in `out_of_scope_issues` and was not acted upon without explicit user authorization.
5. `user_authorized_extra_work` is `true` only if the user explicitly approved additional work in writing during the session.
6. If `scope_respected` is claimed as `true`, `unplanned_changes` MUST be empty and `user_authorized_extra_work` MUST be `false`.

## Decision Criteria

- `PASS`: The `Scope Compliance` section exists, `scope_respected` is `true`, no unplanned changes are reported, and no unauthorized extra work was performed.
- `FAIL`: The section is missing, `scope_respected` is `false`, unplanned changes exist, or extra work was performed without user authorization.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Transition to `RECOVERY`.
3. In recovery, decide whether to revert unplanned changes, request clarification from the user, or abort.

## Semantic Validation Performed by Runner

The runner enforces the following semantic checks in addition to section presence:
- For H07: `scope_respected` is `true`, `unplanned_changes` is empty, and `user_authorized_extra_work` is `false`.
