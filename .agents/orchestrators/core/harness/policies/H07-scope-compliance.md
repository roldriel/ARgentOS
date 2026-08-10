+++
trigger = "H07"
transition = "VERIFYING → COMPLETED"
artifact = "VERIFICATION_REPORT.md"
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

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` have objectively verifiable structure and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.

1. The artifact contains a `Scope Compliance` section. `[gate]` (see §"Gate Checklist", item 2)
2. The section declares whether the work respected the assigned scope. `[gate]` (see §"Gate Checklist", item 3, which verifies the declared `scope_respected` value)
3. Any project file, dependency, configuration, or test modified outside the execution plan is listed in `unplanned_changes`. `[agent]` (the §"Gate Checklist" verifies the declared list is empty when `scope_respected` is `true`; judging that nothing was omitted from the list is agent judgment)
4. Any error, bug, or inconsistency discovered outside the assigned task scope is listed in `out_of_scope_issues` and was not acted upon without explicit user authorization. `[agent]`
5. `user_authorized_extra_work` is `true` only if the user explicitly approved additional work in writing during the session. `[agent]` (the §"Gate Checklist" verifies the declared value; judging that the written approval exists is agent judgment — the verifier may activate the `decision-extractor` skill to recover confirmed user decisions from `SESSION_LOG.md` and the session artifacts before judging)
6. If `scope_respected` is claimed as `true`, `unplanned_changes` MUST be empty and `user_authorized_extra_work` MUST be `false`. `[gate]` (see §"Gate Checklist", items 3–5)

## Decision Criteria

- `PASS`: The `Scope Compliance` section exists, `scope_respected` is `true`, no unplanned changes are reported, and no unauthorized extra work was performed.
- `FAIL`: The section is missing, `scope_respected` is `false`, unplanned changes exist, or extra work was performed without user authorization.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Transition to `RECOVERY`.
3. In recovery, decide whether to revert unplanned changes, request clarification from the user, or abort.

## Gate Checklist

The Orchestrator evaluates each item below by judgment when the gate fires and MUST cite evidence per item (artifact path, declared value) in `HARNESS_REPORT.md`.

1. Verify that `VERIFICATION_REPORT.md` exists in the current iteration directory (`.project/<session-uuid>/<iteration>/`). Cite the resolved artifact path as evidence.
2. Verify that the artifact contains a `## Scope Compliance` section with a parseable TOML block. Cite the section.
3. Verify that `scope_compliance.scope_respected` is `true`. Cite the declared value.
4. Verify that `scope_compliance.unplanned_changes` is present and is an empty list. Cite the declared value.
5. Verify that `scope_compliance.user_authorized_extra_work` is `false`. Cite the declared value.

## Recovery Decision Table

When H07 fails, the Orchestrator populates the context variables from the session (`scope_violation_severe`, `scope_expansion_requested`, `scope_compliant`) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `scope_violation_severe == true` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Scope violation is severe or repeated. |
| 2 | `scope_expansion_requested == true` | `NEEDS_CLARIFICATION` | — | — | User needs to approve scope expansion. |
| 3 | `scope_compliant == false` | `RETRY_WORKER` | `06-execute.md` | `executor` | Scope reported as not compliant; retry executor once with corrected scope. If the retry also fails, generic recovery will be used. |
| 4 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Scope compliance check failed; falling back to generic recovery. |
