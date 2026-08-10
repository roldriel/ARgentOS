# Orchestrator Decisions Standard

## Purpose

Define the conceptual catalog of the Orchestrator's discretionary decision points: each point is defined by the question it answers, its conceptual inputs, and its concept of authority. This standard defines no decision algorithms, heuristics, or numeric thresholds; concrete criteria belong to policies.

## Core concepts

### Authority over recommendations

Every recommendation the Orchestrator receives — a worker's `recommendation.next_state`, a reviewer's outcome, a discovery result — is advisory. Final authority over the transition belongs to the Orchestrator, bounded by the state machine and the harness, which outrank both the recommendation and the Orchestrator's judgment. The user has the final word on every scope and abort decision. Every override and its reason MUST be recorded in `SESSION_LOG.md`.

### Retry bound

Corrections of the same artifact under the same reviewer `REWORK` recommendation are bounded by a finite, session-visible limit. Once the limit is exhausted, routing stops being correction and becomes `RECOVERY`. The retry bound exists so that rework is never an open-ended cycle; its concrete value is a policy matter.

### KB criticality

The criticality of the discovery knowledge base for a task, in three conceptual classes: **indispensable** (the task cannot execute correctly without the KB), **useful** (the KB improves execution but the task can continue degraded), **optional** (the KB does not materially affect the task).

### Founded abort

Every transition to `ABORT` requires a cause recorded in `SESSION_LOG.md`: a user decision, a decision-tree action, or a judgment of infeasibility. No worker may abort; a worker that detects infeasibility reports it and the Orchestrator decides.

## Decision point catalog

### D1 — Transition acceptance

- **Question:** does the Orchestrator accept the worker's `recommendation.next_state` or override it?
- **Inputs:** the recommendation and its reasoning; the harness result for the candidate transition; the transitions allowed by the state machine; the recommendation confidence (see `.agents/standards/quality/CONFIDENCE.md`).
- **Authority:** the worker recommends; the Orchestrator decides. The state machine and the harness veto: a recommendation never enables a disallowed transition nor exempts the harness.

### D2 — Reviewer outcome routing

- **Question:** given the reviewer's `APPROVE`, `REWORK`, or `NEEDS_CLARIFICATION`, what happens to the artifact?
- **Inputs:** the reviewer's recommendation and Review Report; the retry bound; the artifact's originating phase.
- **Authority:** the reviewer recommends; the Orchestrator routes. `REWORK` is a recommendation, not a protocol state. On `REWORK`, the artifact returns to the corresponding worker role within the retry bound; once the bound is exhausted, the routing becomes `RECOVERY`.

### D3 — `NEEDS_CLARIFICATION` ↔ `RECOVERY` boundary

- **Question:** is a detected deviation an ambiguity requiring a user decision (clarification-worthy) or a failure recoverable without new user information?
- **Inputs:** the conceptual nature of the deviation (decision ambiguity vs. execution/artifact failure); the confidence model — intent confidence (`.agents/standards/requirements/INTENT_CONFIDENCE.md`) when the doubt is about what the user wants, recommendation confidence when the doubt is about a received recommendation; the no-assumption rule (`.agents/standards/requirements/NO_ASSUMPTIONS.md`), which biases toward `NEEDS_CLARIFICATION` whenever proceeding would require assuming.
- **Authority:** the user is the only source of resolution for decision ambiguities; `RECOVERY` is the path for failures that require no new user information.

### D4 — Discovery failure criticality

- **Question:** given a discovery failure, does the task abort, route to `RECOVERY`, or continue with minimal discovery?
- **Inputs:** the KB criticality for the task (indispensable / useful / optional); the status reported by the Discovery Orchestrator; the task's scope.
- **Authority:** the Discovery Orchestrator reports; the Orchestrator decides the course and records it in `SESSION_LOG.md`. Criticality classification is Orchestrator judgment informed by the task specification, not a computation.

### D5 — Abort authority

- **Question:** who may abort a task, and under what concept?
- **Inputs:** the source of the abort (user decision, decision-tree `ABORT` action, indispensable criticality in D4, infeasibility detected in `RECOVERY`).
- **Authority:** the user may abort at any time and their word is final. The Orchestrator is the only role that may take the state machine to `ABORT`, always as a founded abort. Workers never abort.

### D6 — Degraded bootstrap

- **Question:** given a protocol health `FAIL`, may the session start or continue?
- **Inputs:** the protocol health result; the existence of explicit user authorization.
- **Authority and rule:** a protocol health `FAIL` blocks the handoff to the core Orchestrator; the only exception is explicit user authorization, recorded in `SESSION_LOG.md`. The canonical statement of this rule lives in `.agents/orchestrators/system/states/SYSTEM_STATE_MACHINE.md` (`BOOTSTRAP_FAILED`); this point models it conceptually without reformulating it. Only the user may degrade the verified environment, and that degradation is always logged as a warning.

## Relationship to other standards

- `.agents/standards/quality/CONFIDENCE.md` — general confidence model; its recommendation-confidence specialization feeds D1 and D3.
- `.agents/standards/requirements/INTENT_CONFIDENCE.md` — intent-interpretation specialization; feeds D3.
- `.agents/standards/requirements/NO_ASSUMPTIONS.md` — biases D3 toward `NEEDS_CLARIFICATION`.
- `.agents/orchestrators/core/roles/orchestrator.md` — the role applies this catalog; operational procedures (reviewer invocation, discovery invocation, recovery mapping) live there.
