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

Validate that the executed work stayed within the task assigned by the user — including any expansion the user explicitly authorized in writing during the session — and that the agent did not take autonomous liberties or perform unrequested work.

## Input

- Current state: `VERIFYING`
- Target state: `COMPLETED`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md`
- Contract: `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`
- Reference: `TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md`

## Checklist

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` are structurally checkable and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.
Evidence is cited per item with a class from the evidence standard
(`.agents/standards/quality/EVIDENCE.md`): `observation`/`measurement`/
`reference`/`assertion` when the evidence is citable; `attestation` only with
actor and statement.

1. The artifact contains a `Scope Compliance` section. `[gate]` (see §"Gate Checklist", item 2)
2. The section declares whether the work respected the assigned scope. `[gate]` (see §"Gate Checklist", item 3, which verifies the declared `scope_respected` value)
3. Any project file, dependency, configuration, or test modified outside the execution plan is listed in `unplanned_changes`. `[agent]` (the §"Gate Checklist" verifies the declared list is empty when `scope_respected` is `true`; judging that nothing was omitted from the list is agent judgment)
4. Any error, bug, or inconsistency discovered outside the assigned task scope is listed in `out_of_scope_issues` and was not acted upon without explicit user authorization. `[agent]`
5. `user_authorized_extra_work` is `true` only if there is work outside the approved plan that the user explicitly approved in writing during the session and the report cites the evidence (`SESSION_LOG.md` entry or session artifact). `[agent]` (the §"Gate Checklist" verifies the declared value; judging that the written approval exists is Orchestrator judgment when the gate fires — the Orchestrator may activate the `decision-extractor` skill to recover confirmed user decisions from `SESSION_LOG.md` and the session artifacts before judging)
6. The section satisfies exactly one scope branch. Branch A: `scope_respected` is `true`, `unplanned_changes` is empty and `user_authorized_extra_work` is `false`. Branch B: `scope_respected` is `true`, `unplanned_changes` lists the changes and `user_authorized_extra_work` is `true` with the written authorization cited. `scope_respected` equal to `false` is a scope failure under both branches. `[gate]` (see §"Gate Checklist", items 3–6)

## Decision Criteria
**Structural validator:** the Orchestrator MUST run `python .agents/harness/gate_validator.py --trigger H07 --artifact <path>` before judging PASS; a structural FAIL blocks PASS unless recorded as a documented deviation.

- `PASS`: The `Scope Compliance` section exists and satisfies Branch A, or Branch B with cited written authorization.
- `FAIL`: The section is missing, `scope_respected` is `false`, the declared branch is mixed or incoherent (for example, a non-empty `unplanned_changes` with `user_authorized_extra_work = false`, or `user_authorized_extra_work = true` without cited evidence), or extra work was performed without user authorization.

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
4. Verify that `scope_compliance.unplanned_changes` is present. When `scope_compliance.user_authorized_extra_work` is `false` (Branch A), the list MUST be empty; when it is `true` (Branch B), the list may be non-empty and the written authorization MUST be cited in the report. Cite the declared value and the evidence.
5. Verify the declared `scope_compliance.user_authorized_extra_work` value. For Branch B (`true`), the Orchestrator MUST judge the written authorization evidence (the report references `SESSION_LOG.md` or a session artifact) and MAY activate the `decision-extractor` skill to recover the confirmed user decision; the evidence citation is recorded in `HARNESS_REPORT.md`. Cite the declared value and the evidence.
6. Verify the branch is coherent: `scope_respected = true` with a non-empty `unplanned_changes` requires `user_authorized_extra_work = true` with cited evidence; a mixed declaration is a FAIL. Cite the declared values.
7. Verify the evidence-or-attestation rule: every check of this gate is recorded in `HARNESS_REPORT.md` citing evidence with a class per `.agents/standards/quality/EVIDENCE.md` or declaring `claim_class` (`verified` requires a non-attestation evidence entry; `attested`/`inference` are declared explicitly). For Branch B, the written authorization is cited as `reference` (a `SESSION_LOG.md` entry or session artifact) or `assertion` (a user decision recovered via the `decision-extractor` skill); if the Orchestrator cannot cite it, the PASS is recorded as `attested`, not as external verification.
8. Verify dimension coherence: `scope_compliance` records approval/scope
   decisions (Approval/Gate State), never the artifact lifecycle; when citing
   each check, indicate the state dimension it belongs to (ST-004).

## Recovery Decision Table

When H07 fails, the Orchestrator populates the context variables from the session (`scope_violation_severe`, `scope_expansion_requested`, `scope_compliant`) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `scope_violation_severe == true` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Scope violation is severe or repeated. |
| 2 | `scope_expansion_requested == true` | `NEEDS_CLARIFICATION` | — | — | User needs to approve scope expansion. |
| 3 | `scope_compliant == false` | `RETRY_WORKER` | `06-execute.md` | `executor` | Scope reported as not compliant; retry executor once with corrected scope. If the retry also fails, generic recovery will be used. |
| 4 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Scope compliance check failed; falling back to generic recovery. |
