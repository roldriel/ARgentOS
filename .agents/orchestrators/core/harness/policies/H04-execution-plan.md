+++
trigger = "H04"
transition = "PLANNING → PLAN_READY"
artifact = "EXECUTION_PLAN.md"
semantic_validation = true
semantic_checks = ["citation_resolution"]
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
- Reference: `TASK_SPECIFICATION.md`, `CONTEXT_ARTIFACT.md`, `CONTEXT_VALIDATION_REPORT.md`

## Checklist

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence, required-section presence, and the EARS/rubric/semantic checks declared in this policy's front matter) or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. The artifact file exists. `[machine]`
2. The plan addresses the task objective. `[agent]`
3. The plan uses validated context (no invented assumptions). `[agent]`
4. The plan defines executable, ordered steps. `[agent]`
5. Each step specifies what, where, and why. `[agent]`
6. The plan identifies risks and mitigation strategies. `[agent]`
7. The plan defines a verification strategy. `[agent]`
8. The plan does not depend on unresolved unknowns. `[agent]`
9. The plan does not exceed the task scope. `[agent]`
10. The plan is compatible with the existing architecture and conventions. `[agent]`
11. Every citation in the artifact (`` `path:section` ``, `` `path` §section ``, and TOML citation fields) resolves against the filesystem. `[machine]` (the runner's `citation_resolution` semantic check enforces this; paths naming files to be created are not citations and are not checked)

The presence of the `required_sections` resolved by the runner from the artifact contract is `[machine]` even though it is not restated as a numbered item.

## Decision Criteria

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
