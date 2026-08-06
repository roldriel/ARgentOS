+++
trigger = "H15"
transition = "pre-delegation and post-return delegation gate"
validation_type = "delegation"
required_sections = []
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

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness module `.agents/harness/delegation_validity.py` (`validate_delegation_payload` / `validate_return_report`) and by this policy's test suite (`.agents/harness/tests/test_delegation_validity.py`) — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment. The runner CLI does not execute H15: a delegation payload is not a session artifact, so machine evaluation lives in the module and the test suite, and the agents apply the same checks at the two gates.

### Pre-delegation gate

1. If `profile` is present and not `null`, its value resolves exactly to a file under `.agents/roles/profiles/` (without the `.md` extension). `[machine]` — violation class F1.
2. Each entry of `skills` resolves under `.project/skills/` or `.agents/skills/` (project level wins on collision). `[machine]` — violation class F2, non-blocking: the phase continues without that capability and the deviation is logged.
3. Each path of `input_artifacts` exists inside the session (`.project/<session-uuid>/<iteration>/`). `[machine]` — violation class F1.
4. If `context_budget` is present, its value is a finite, positive constraint on the resource the runtime uses to represent the Budget (for the prompt-based runtime: estimated tokens, per `.agents/standards/context/BUDGET_MATERIALIZATION.md`). `[machine]` — violation class F1 when the value is not finite and positive; `[agent]` — class F2 when the value is finite but the Orchestrator cannot justify its coherence with the session Budget.

### Post-return gate

5. The return report complies with the contract schema (§"Worker Return Report"): required fields present, `blockers` a list of class-`blocker` entries, and every `deviations` entry prefixed with its failure class (`deviation:`, `ambiguity:` or `inconsistency:`). `[machine]` — violation class F1 over the protected transition.
6. Every violation detected at either gate is reported with the failure class declared in §"Failure classes". `[agent]`

## Decision Criteria

- `PASS`: All checklist items are satisfied (item 2 violations are logged deviations, not gate failures).
- `FAIL`: Any F1 item is violated: unresolvable profile, missing input artifact, non-finite or non-positive budget, or invalid return report.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md` with the failure class of each violation.
2. Apply the recovery decision tree `.agents/orchestrators/core/harness/decision_trees/H15_FAIL.toml` when the `decision_trees` feature flag is enabled; otherwise apply the contract's retry rules directly.
3. Correct the delegation and re-delegate once (per the contract's §"Retry Rules"); if the second attempt fails, transition to `RECOVERY`.

## Validation

```bash
python -m pytest .agents/harness/tests/test_delegation_validity.py
```
