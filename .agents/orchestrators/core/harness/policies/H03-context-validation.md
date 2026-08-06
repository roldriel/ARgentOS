+++
trigger = "H03"
transition = "VALIDATING_CONTEXT → CONTEXT_READY"
artifact = "CONTEXT_VALIDATION_REPORT.md"
required_sections = [
  "Metadata",
  "Context Reference",
  "Validation Objective",
  "Completeness Evaluation",
  "Relevance Evaluation",
  "Consistency Evaluation",
  "Risk Evaluation",
  "Validation Decision",
  "Required Actions",
  "Confidence",
  "State Transition"
]
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

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence, required-section presence, and the EARS/rubric/semantic checks declared in this policy's front matter) or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. The artifact file exists. `[machine]`
2. The report explicitly states whether the context is sufficient. `[agent]`
3. The report identifies any missing or ambiguous context. `[agent]`
4. The report evaluates relevance of the gathered context to the task. `[agent]`
5. The report evaluates consistency between context and task specification. `[agent]`
6. If context is insufficient, the report specifies what is missing. `[agent]`
7. The report does not invent context to cover gaps. `[agent]`

The presence of the `required_sections` declared in this policy's front matter is `[machine]` even though it is not restated as a numbered item.

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
