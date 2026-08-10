+++
trigger = "H03"
transition = "VALIDATING_CONTEXT → CONTEXT_READY"
artifact = "CONTEXT_VALIDATION_REPORT.md"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H03
name: context-validation
state: core:VALIDATING_CONTEXT
lifecycle: context
gates:
  - "core:VALIDATING_CONTEXT -> core:CONTEXT_READY"
artifact_validated: CONTEXT_VALIDATION_REPORT.md
---

# Harness Policy H03: Context Validation Report

## Trigger

`VALIDATING_CONTEXT → CONTEXT_READY`

## Purpose

Validate that the context validation report justifies whether the gathered context is sufficient, relevant, and consistent.

## Input

- Current state: `VALIDATING_CONTEXT`
- Target state: `CONTEXT_READY`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md`
- Contract: `.agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md`
- Reference: `TASK_SPECIFICATION.md`, `CONTEXT_ARTIFACT.md`

## Checklist

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` have objectively verifiable structure and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.

1. The artifact file exists. `[gate]`
2. The report explicitly states whether the context is sufficient. `[agent]`
3. The report identifies any missing or ambiguous context. `[agent]`
4. The report evaluates relevance of the gathered context to the task. `[agent]`
5. The report evaluates consistency between context and task specification. `[agent]`
6. If context is insufficient, the report specifies what is missing. `[agent]`
7. The report does not invent context to cover gaps. `[agent]`

The presence of the sections required by the artifact contract is `[gate]` even though it is not restated as a numbered item in the checklist above; see §"Gate Checklist", item 2.

## Gate Checklist

The Orchestrator evaluates each item below by judgment when the gate fires and MUST cite evidence per item (artifact path, section name, or declared value) in `HARNESS_REPORT.md`.

1. Verify that `CONTEXT_VALIDATION_REPORT.md` exists in the current iteration directory (`.project/<session-uuid>/<iteration>/`). Cite the resolved artifact path as evidence.
2. Verify that the report contains the normative sections of its contract: read the contract cited in §"Input" (`.agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md`), and verify that each normative `##` heading of the contract is present in the report (case-insensitive comparison), excluding non-normative sections such as examples. Cite any missing section as failure evidence.

## Decision Criteria

- `PASS`: The report exists, the context is declared sufficient (`VALIDATED`), and no critical gaps remain.
- `FAIL`: The report declares context insufficient (`NEEDS_MORE_CONTEXT` or `REJECTED`) or the validation is incomplete.

### Decision mapping

- `VALIDATED` → transition to `CONTEXT_READY`.
- `NEEDS_MORE_CONTEXT` → return to `GATHERING_CONTEXT` if the gaps can be filled automatically, or `NEEDS_CLARIFICATION` if user input is required.
- `REJECTED` → transition to `NEEDS_CLARIFICATION`.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. If gaps can be filled by the Worker, return to `GATHERING_CONTEXT`.
3. If gaps require user input, transition to `NEEDS_CLARIFICATION`.

## Examples

### PASS examples

1. The report states `VALIDATED` and cites how each context item supports a task requirement.
2. The report identifies one missing item (the exact version of a dependency) and specifies that it can be obtained automatically.
3. The report explicitly discards an outdated context item and explains why it is irrelevant.

### FAIL examples

1. The report declares context sufficient without referencing any specific context item.
2. The report ignores a direct contradiction between the task specification and an observed project file.
3. The report invents a project convention ("the team always uses PostgreSQL") without evidence.

### Yes/no questions for the evaluator

1. Is every context item used in the plan or execution?
2. Are there explicit contradictions between context and task specification?
3. Was irrelevant context explicitly discarded or justified?

## Recovery Decision Table

When H03 fails, the Orchestrator populates the context variables from the session (`context_contradictory`, `gaps_actionable`, `context_user_specific`) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `context_contradictory == true` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Context is contradictory or unresolvable. |
| 2 | `gaps_actionable == true` | `RETRY_WORKER` | `03-gather-context.md` | `context_gatherer` | Actionable context gaps found; retry context gatherer. |
| 3 | `context_user_specific == true` | `NEEDS_CLARIFICATION` | — | — | Gaps require user-specific information. |
| 4 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Context validation failed; falling back to generic recovery. |
