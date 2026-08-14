+++
trigger = "H15"
transition = "pre-delegation and post-return delegation gate"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H15
name: delegation-validity
state: null
lifecycle: null
tag: delegation
gates: []
artifact_validated: null
---

# Harness Policy H15: Delegation Validity

## Trigger

H15 is **not** a state-transition gate over a session artifact: it gates Worker delegations at two points of the delegation flow:

1. **Pre-delegation** — the Orchestrator, before invoking the Worker (checklist items 1–4).
2. **Post-return** — the Orchestrator, upon receiving the return report and before applying the harness trigger of the protected transition (checklist item 5).

The Worker re-verifies items 1 and 3 upon receiving the payload (pre-execution), because it cannot assume the Orchestrator verified them.

## Purpose

Validate that a delegation payload is not only well formed but **executable** — every reference resolves and the Context Budget materialization is coherent — and that the Worker return report complies with the delegation contract, before the delegation proceeds or the phase is considered complete.

## Input

- Delegation payload: `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Required Invocation Payload".
- Return report: `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Worker Return Report".
- Profile catalog: `.agents/roles/profiles/`.
- Skill locations: `.project/skills/` (project level, wins on name collision) and `.agents/skills/` (protocol level), per `.agents/standards/orchestration/SKILLS.md`.
- Session artifacts: `.project/<session-uuid>/<iteration>/`.
- Budget materialization for the current runtime: `.agents/standards/context/BUDGET_MATERIALIZATION.md`.

## Failure classes

Each violation is reported with its failure class, as defined inline in the delegation contract (§"Failure classes in `blockers` and `deviations`"):

- **F1 (blocker)** — prevents completing the phase; destination recovery. Applies to items 1, 3, 4 (non-finite budget) and 5.
- **F2 (deviation)** — does not prevent completing the phase; destination logged warning. Applies to item 2 (the Worker reports the unresolvable skill as a deviation and never invents its content) and to item 4 when the budget is finite but the Orchestrator cannot justify its coherence with the session Budget.

## Checklist

**Evaluation audience:** the harness runner no longer exists; each item is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` are structurally checkable (file existence, path resolution, schema shape); items marked `[agent]` are declared judgment.

### Pre-delegation gate

1. If `profile` is present and not `null`, its value resolves exactly to a file under `.agents/roles/profiles/` (without the `.md` extension). `[gate]` — violation class F1.
2. Each entry of `skills` resolves under `.project/skills/` or `.agents/skills/` (project level wins on collision). `[gate]` — violation class F2, non-blocking: the phase continues without that capability and the deviation is logged.
3. Each path of `input_artifacts` exists inside the session (`.project/<session-uuid>/<iteration>/`). `[gate]` — violation class F1.
4. If `context_budget` is present, its value is a finite, positive constraint on the resource the runtime uses to represent the Budget (for the prompt-based runtime: estimated tokens, per `.agents/standards/context/BUDGET_MATERIALIZATION.md`). `[gate]` — violation class F1 when the value is not finite and positive; `[agent]` — class F2 when the value is finite but the Orchestrator cannot justify its coherence with the session Budget.

### Post-return gate

5. The return report complies with the contract schema (§"Worker Return Report"): required fields present, `blockers` a list of class-`blocker` entries, and every `deviations` entry prefixed with its failure class (`deviation:`, `ambiguity:` or `inconsistency:`). `[gate]` — violation class F1 over the protected transition.
6. Every violation detected at either gate is reported with the failure class declared in §"Failure classes". `[agent]`

## Decision Criteria

- `PASS`: All checklist items are satisfied (item 2 violations are logged deviations, not gate failures).
- `FAIL`: Any F1 item is violated: unresolvable profile, missing input artifact, non-finite or non-positive budget, or invalid return report.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md` with the failure class of each violation.
2. Apply the §"Recovery Decision Table" of this policy (which encodes the contract's retry rules).
3. Correct the delegation and re-delegate once (per the contract's §"Retry Rules"); if the second attempt fails, transition to `RECOVERY`.

## Validation

There is no executable test suite for H15: the Orchestrator applies the checklist above by
judgment at both delegation gates and records the outcome in `HARNESS_REPORT.md`.

## Recovery Decision Table

When H15 fails, the Orchestrator populates the context variables from the delegation (`profile_unresolvable`, `input_artifact_missing`, `budget_incoherent`, `return_report_invalid`, `retry_count` = correction attempts already made for this failure) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | (`profile_unresolvable == true` or `input_artifact_missing == true` or `budget_incoherent == true`) and `retry_count >= 1` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Delegation payload still invalid after one correction (unresolvable profile, missing input artifact, or incoherent budget); route to generic recovery. |
| 2 | `profile_unresolvable == true` or `input_artifact_missing == true` or `budget_incoherent == true` | `RETRY_WORKER` | `06-execute.md` | `worker` | Delegation payload is invalid (F1 blocker); the Orchestrator corrects the profile, input artifact paths, or context_budget and re-delegates once. target_phase/role name the primary delegation point; apply to the phase actually delegated. |
| 3 | `return_report_invalid == true` and `retry_count >= 1` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Return report still invalid after one corrective re-invocation; route to generic recovery per the delegation contract retry rules. |
| 4 | `return_report_invalid == true` | `RETRY_WORKER` | `06-execute.md` | `worker` | Return report invalid (F1 blocker over the protected transition); re-invoke the Worker once with corrective instructions. target_phase/role name the primary delegation point; apply to the phase actually delegated. |
| 5 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Delegation validity failure without a specific route; falling back to generic recovery. |
