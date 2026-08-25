+++
trigger = "H04"
transition = "PLANNING → PLAN_READY"
artifact = "EXECUTION_PLAN.md"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H04
name: execution-plan
state: core:PLANNING
lifecycle: planning
gates:
  - "core:PLANNING -> core:PLAN_READY"
artifact_validated: EXECUTION_PLAN.md
---

# Harness Policy H04: Execution Plan

## Trigger

`PLANNING → PLAN_READY`

## Purpose

Validate that `EXECUTION_PLAN.md` defines an executable, safe, and scope-respecting strategy.

## Input

- Current state: `PLANNING`
- Target state: `PLAN_READY`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md`
- Contract: `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`
- Reference: `TASK_SPECIFICATION.md`, `CONTEXT_ARTIFACT.md`, `CONTEXT_VALIDATION_REPORT.md` (for `trivial`-profile tasks, `TASK_ANALYSIS.md` replaces `TASK_SPECIFICATION.md` and no context artifacts are produced)

## Checklist

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` are structurally checkable and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.

1. The artifact file exists. `[gate]`
2. The plan addresses the task objective. `[agent]`
3. The plan uses validated inputs without invented assumptions (for `trivial`-profile tasks, the task analysis; otherwise the validated context artifacts). `[agent]`
4. The plan defines executable, ordered steps. `[agent]`
5. Each step specifies what, where, and why. `[agent]`
6. The plan identifies risks and mitigation strategies. `[agent]`
7. The plan defines a verification strategy. `[agent]`
8. The plan does not depend on unresolved unknowns. `[agent]`
9. The plan does not exceed the task scope. `[agent]`
10. The plan is compatible with the existing architecture and conventions. `[agent]`
11. Every citation in the artifact (`` `path:section` ``, `` `path` §section ``, and TOML citation fields) resolves against the filesystem. `[gate]` (see §"Gate Checklist", item 2; paths naming files to be created are not citations and are not checked)
12. The plan does not declare out-of-frontier effects beyond those covered by the task specification's `Effects` section (or, for `trivial`-profile tasks, by `SESSION_BRIEF.md`). `[agent]`

The presence of the sections required by the artifact contract is `[gate]` even though it is not restated as a numbered item; the Orchestrator verifies it against the contract cited in §"Input".

## Gate Checklist

The Orchestrator evaluates each item below by judgment when the gate fires and MUST cite evidence per item (artifact path, declared value, or broken reference) in `HARNESS_REPORT.md`.

1. Verify that `EXECUTION_PLAN.md` exists in the current iteration directory (`.project/<session-uuid>/<iteration>/`). Cite the resolved artifact path as evidence.
2. Verify that every citation in the artifact resolves against the filesystem. Recognized citation forms: backtick-quoted `` `path:section` ``, backtick-quoted path followed by `§section`, and the string values of the TOML keys `specification` and `execution_plan` inside ` ```toml ` blocks. A citation resolves when its path exists relative to the project root, the session directory, or any of the session's iteration directories; when the target is a `.md` file and the anchor is not numeric-only, the cited section MUST exist as an ATX heading in the target (normalized, case-insensitive comparison). Paths containing `<`/`>` placeholders are skipped. On failure, cite each broken citation (line, path, reason); on success, cite the number of citations verified. For `trivial`-profile tasks, the `specification` citation field references the iteration's `TASK_ANALYSIS.md`.
3. Verify the authorization boundary of the plan: the plan must not contain its own `Effects` section or otherwise declare new authorizations; every out-of-frontier effect the plan requires must be covered by the task specification's `Effects` section (or, for `trivial`-profile tasks, by `SESSION_BRIEF.md`). Cite the covered effects and any undeclared effect.

## Decision Criteria
**Structural validator:** the Orchestrator MUST run `python .agents/harness/gate_validator.py --trigger H04 --artifact <path>` before judging PASS; a structural FAIL blocks PASS unless recorded as a documented deviation.
For `trivial`-profile tasks the validator applies the profile-aware section
set: `## Context Reference` is not required (the contract omits it in the
reduced cycle; the profile is read from the session's `TASK_ANALYSIS.md`).

- `PASS`: All checklist items are satisfied.
- `FAIL`: The plan is unsafe, incomplete, out of scope, or depends on unresolved unknowns.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `PLANNING` and re-invoke the Worker as `planner`, or
3. Transition to `NEEDS_CLARIFICATION` if the plan cannot be completed safely.

## Examples

### PASS examples

1. The plan contains all required sections, implementation steps are numbered, and each step includes what, where, and why.
2. Each implementation step has a corresponding verification criterion (e.g., a test or manual check).
3. The plan references the exact context from `CONTEXT_ARTIFACT.md` and `CONTEXT_VALIDATION_REPORT.md` and does not introduce new assumptions.

### FAIL examples

1. The plan includes a step that depends on an undocumented API that was never mentioned in the context.
2. The plan adds a new database table even though the task specification only requested a query change.
3. The plan lists implementation steps but does not define how to verify any of them.

### Yes/no questions for the evaluator

1. Does the plan reference every section defined in the `EXECUTION_PLAN.md` contract?
2. Does every step have a verification criterion?
3. Are there any steps that depend on undeclared information?

## Recovery Decision Table

When H04 fails, the Orchestrator populates the context variables from the session (`plan_out_of_scope`, `plan_depends_on_user`, `retry_count` = retries already attempted for this failure) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `plan_out_of_scope == true` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Plan is unsafe or out of scope. |
| 2 | `plan_depends_on_user == true` | `NEEDS_CLARIFICATION` | — | — | Plan depends on unresolved user decisions. |
| 3 | `retry_count >= 1` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Repeated failure after retry; route to generic recovery. |
| 4 | otherwise | `RETRY_WORKER` | `05-plan.md` | `planner` | Plan is incomplete but correctable; retry planner. |
