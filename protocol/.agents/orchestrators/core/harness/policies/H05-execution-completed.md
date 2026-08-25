+++
trigger = "H05"
transition = "EXECUTING → VERIFYING"
artifact = "EXECUTION_SUMMARY.md"
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

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` are structurally checkable and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.
Evidence is cited per item with a class from the evidence standard
(`.agents/standards/quality/EVIDENCE.md`): `observation`/`measurement`/
`reference` when the evidence is citable; `attestation` only with actor and
statement.

1. Every step in `EXECUTION_PLAN.md` has been executed or explicitly documented as skipped with justification. `[gate]` (see §"Gate Checklist", item 3: every step is `COMPLETED` or `SKIPPED` with notes)
2. No project files outside the plan scope were modified. `[agent]`
3. No unplanned requirements or assumptions were introduced. `[agent]`
4. Intermediate validations defined in the plan were run. `[agent]`
5. The project is in a verifiable state (tests can run, app can start, etc.). `[agent]` (item 2 of the §"Gate Checklist" verifies the declared value `final_state.status = VERIFIABLE`; judging that the project is actually verifiable is agent judgment)
6. No step caused an unrecoverable error. `[agent]`
7. For each practice listed in `technical_approach.enabled`, the `EXECUTION_SUMMARY.md` contains a corresponding entry in `## Technical Practice Evidence` with `applied` and, when applicable, supporting evidence. `[gate]` (see §"Gate Checklist", item 4)

The presence of the sections required by the artifact contract is `[gate]` even though it is not restated as a numbered item; the Orchestrator verifies it against the contract cited in §"Input".

## Decision Criteria
**Structural validator:** the Orchestrator MUST run `python .agents/harness/gate_validator.py --trigger H05 --artifact <path>` before judging PASS; a structural FAIL blocks PASS unless recorded as a documented deviation.

- `PASS`: All planned steps are complete and the project is verifiable.
- `FAIL`: Steps were skipped, scope was exceeded, or the project is not verifiable.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Transition to `RECOVERY`.
3. In recovery, decide whether to replan or request clarification.

## Gate Checklist

The Orchestrator evaluates each item below by judgment when the gate fires and MUST cite evidence per item (artifact path, declared value, or offending entry) in `HARNESS_REPORT.md`, with an evidence class per `.agents/standards/quality/EVIDENCE.md` (`observation`/`measurement`/`reference` when citable, marked `attestation` otherwise).

1. Verify that `EXECUTION_SUMMARY.md` exists in the current iteration directory (`.project/<session-uuid>/<iteration>/`). Cite the resolved artifact path as evidence.
2. Verify that `## Final Project State` contains a parseable TOML block and that `final_state.status` is one of `VERIFIABLE` or `BLOCKED`. The gate FAILS unless the declared status is `VERIFIABLE`. Cite the declared value.
3. Verify that `## Steps Executed` contains a parseable TOML block whose `steps_executed` is a list, that every step has a `status` in {`COMPLETED`, `SKIPPED`, `BLOCKED`}, that no step is `BLOCKED`, and that every `SKIPPED` step carries non-empty `notes`. Cite each offending step.
4. Verify the technical practice evidence. Read `technical_approach.enabled` from the `## Technical Approach` TOML block of `TASK_SPECIFICATION.md` in the same iteration. If either input is missing, or the `enabled` list is empty, record that this item is skipped. Otherwise verify, in the `## Technical Practice Evidence` TOML block of the summary, that each enabled practice has an entry with an `applied` field: when `applied = false`, a non-empty `reason` is required; when `applied = true`, at least one additional non-empty evidence field is required. Cite each practice entry and each violation.
5. Verify that the `## Metadata` block of the summary declares no manual
   lifecycle field (`status`, `state`, `approved`, `validation.complete`): the
   artifact lifecycle is derived from the gate record (this artifact is
   `validated` by the H05 PASS), never written by the executor (AL-001). Cite
   any offending field.

## Recovery Decision Table

When H05 fails, the Orchestrator populates the context variables from the session (`project_unrecoverable`, `execution_blocked`, `execution_complete`) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `project_unrecoverable == true` | `ABORT` | — | — | Project state is unrecoverable; abort session. |
| 2 | `execution_blocked == true` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Execution blocked by unexpected issue. |
| 3 | `execution_complete == false` | `RETRY_WORKER` | `06-execute.md` | `executor` | Some steps remain pending; retry executor. |
| 4 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Execution validation failed; falling back to generic recovery. |
