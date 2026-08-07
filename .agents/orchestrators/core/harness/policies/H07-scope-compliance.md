+++
trigger = "H07"
transition = "VERIFYING → COMPLETED"
artifact = "VERIFICATION_REPORT.md"
# Explicit subset of the contract sections (this gate checks Scope Compliance only).
required_sections = [
  "Scope Compliance"
]
semantic_validation = true
semantic_checks = ["scope_compliance"]
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H07
name: scope-compliance
state: core:VERIFYING
lifecycle: execution
gates:
  - "core:VERIFYING -> core:COMPLETED"
artifact_validated: VERIFICATION_REPORT.md
---

# Harness Policy H07: Scope Compliance

## Trigger

`VERIFYING → COMPLETED`

## Purpose

Validate that the executed work stayed strictly within the task assigned by the user and that the agent did not take autonomous liberties or perform unrequested work.

## Input

- Current state: `VERIFYING`
- Target state: `COMPLETED`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md`
- Contract: `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`
- Reference: `TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md`

## Checklist

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence, required-section presence, and the semantic checks declared in this policy's front matter) or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. The artifact contains a `Scope Compliance` section. `[machine]` (declared in `required_sections`)
2. The section declares whether the work respected the assigned scope. `[machine]` (the runner's `scope_compliance` semantic check reads the declared `scope_respected` value)
3. Any project file, dependency, configuration, or test modified outside the execution plan is listed in `unplanned_changes`. `[agent]` (the runner verifies the declared list is empty when `scope_respected` is `true`; judging that nothing was omitted from the list is agent judgment)
4. Any error, bug, or inconsistency discovered outside the assigned task scope is listed in `out_of_scope_issues` and was not acted upon without explicit user authorization. `[agent]`
5. `user_authorized_extra_work` is `true` only if the user explicitly approved additional work in writing during the session. `[agent]` (the runner verifies the declared value; judging that the written approval exists is agent judgment — the verifier may activate the `decision-extractor` skill to recover confirmed user decisions from `SESSION_LOG.md` and the session artifacts before judging)
6. If `scope_respected` is claimed as `true`, `unplanned_changes` MUST be empty and `user_authorized_extra_work` MUST be `false`. `[machine]` (the runner's `scope_compliance` semantic check)

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

## Recovery Decision Table

When H07 fails, the Orchestrator populates the context variables from the session (`scope_violation_severe`, `scope_expansion_requested`, `scope_compliant`) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `scope_violation_severe == true` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Scope violation is severe or repeated. |
| 2 | `scope_expansion_requested == true` | `NEEDS_CLARIFICATION` | — | — | User needs to approve scope expansion. |
| 3 | `scope_compliant == false` | `RETRY_WORKER` | `06-execute.md` | `executor` | Scope reported as not compliant; retry executor once with corrected scope. If the retry also fails, generic recovery will be used. |
| 4 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Scope compliance check failed; falling back to generic recovery. |
