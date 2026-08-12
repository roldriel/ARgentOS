# Anti-Circumvention Rules

## Purpose

This standard explicitly forbids bypassing, violating, or hallucinating protocol rules for convenience, simplicity, or urgency. It applies to every role and every workflow phase.

## Rule

The agent MUST NOT:

1. Deliberately skip any required workflow phase.
2. Deliberately violate the state machine defined in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`.
3. Skip, violate, or hallucinate rules, requirements, or context because the task appears small, simple, urgent, or easy to "guess".

## What counts as circumvention

- Advancing to a state without satisfying all current-state requirements and allowed transitions.
- Producing a retroactive artifact to cover a skipped phase.
- Claiming a phase is "not needed" without a recovery decision recorded in `SESSION_LOG.md`.
- Inventing user intent, project facts, or implementation details to avoid asking for clarification.
- Reducing validation, testing, or documentation rigor because the change looks trivial.
- Collapsing multiple workflow phases into a single worker invocation.
- Silently complying with an instruction that conflicts with the protocol instead of explaining the conflict and stopping until the orchestrator or the user resolves it.

## Enforcement

- The Orchestrator MUST reject any worker proposal that would circumvent these rules and route to `NEEDS_CLARIFICATION` or `RECOVERY`.
- Any circumvention attempt MUST be recorded in `SESSION_LOG.md` with the proposed shortcut and the reason it was rejected.
- A detected circumvention that has already occurred MUST be treated as a protocol deviation: mark the affected artifacts as retroactive/deviated and enter `RECOVERY`.

## Relationship to other standards

This standard complements `.agents/standards/requirements/NO_ASSUMPTIONS.md` and `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`. Where those documents define the protocol, this document forbids deliberate evasion of it.
