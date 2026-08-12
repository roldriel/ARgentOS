# Resolution Policy — Unresolvable Conflicts

This policy defines the protocol's behavior when Context Resolution meets a conflict the implementation cannot resolve, so no consistent candidate set can be produced for the worker payload. It is one of the Resolution policies of `.agents/standards/context/`; it complements the resolvable cases covered by `RESOLUTION_TIE_BREAKING.md`, `RESOLUTION_DEDUPLICATION.md` and `RESOLUTION_MERGE.md`.

## 1. Concept

Resolution conflicts fall into two groups:

- **Resolvable by policy:** priority ties (tie-breaking), redundancies (deduplication), mergeable overlaps (merge).
- **Not resolvable by policy:**
  - **Incompatibility** — candidates that cannot coexist in a consistent payload (their joint presence contradicts coherence).
  - **Mutual exclusion** — candidates that are alternatives for the same conceptual role: each is consistent alone, but at most one may remain.
  - **Budget conflict** — the candidates are mutually consistent, but the set exceeds the applicable budget and no policy-removable redundancy or merge resolves the excess.

For these classes the Orchestrator must not guess. Picking one of two contradictory constraints, or silently dropping a relevant candidate to fit a budget, is a circumvention of the no-assumption rule (`.agents/standards/requirements/NO_ASSUMPTIONS.md`) and of the anti-circumvention standard (`.agents/standards/conduct/ANTI_CIRCUMVENTION.md`).

**Evaluation audience:** all rules in this policy are `[agent]` — detecting that candidates contradict each other is agent judgment. Reporting obligations follow the failure classes defined inline in the delegation contract (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Failure classes in `blockers` and `deviations`").

## 2. Policy

When an unresolvable conflict is detected:

1. **Stop the assembly of the affected portion.** No payload is built over an unresolved conflict; a partially consistent payload that hides the conflict is worse than no payload.
2. **Classify and report:**
   - If resolving the conflict requires a user decision (contradictory requirements, alternative approaches the user must choose between, dropping task-relevant content to fit a budget), report it as an **ambiguity (F3)** and transition to clarification per `NO_ASSUMPTIONS.md`, presenting at least two concrete resolution options.
   - If the conflict is a contradiction inside protocol or project documents themselves (two canonical sources stating incompatible rules), report it as an **inconsistency report (F4)**: the conflict is evidence for a documentation fix; the affected task portion is blocked until resolved or clarified.
   - If neither clarification nor a documentation fix unblocks the phase, report it as a **blocker (F1)** with destination recovery.
3. **Report content.** The report names: the conflict class (incompatibility, mutual exclusion, or budget conflict), the conflicting candidates with their sources (`path:section`), what decision or information would resolve it, and which resolution options were considered. `[agent]`
4. **Log.** The conflict and its report are recorded in `SESSION_LOG.md`, whether or not clarification succeeds. `[agent]`

## 3. Boundary with the resolvable policies

Before declaring a conflict unresolvable, the Orchestrator must verify it is not a resolvable case in disguise: a tie (apply `RESOLUTION_TIE_BREAKING.md`), a redundancy (apply `RESOLUTION_DEDUPLICATION.md`), or a mergeable overlap (apply `RESOLUTION_MERGE.md`). A budget conflict, in particular, is declared only after deduplication, merge, and the compression budget rule of `CONTEXT.md` §8.4 have been applied and the excess remains.

## 4. Examples

- `TASK_SPECIFICATION.md` requires output mode `verbose`; the active communication standard mandates `minimal` and the user is not available in-session. Mutual exclusion → F3 clarification with both options presented.
- Two protocol standards state incompatible dependency rules for the same layer. Incompatibility between canonical sources → F4 inconsistency report; the affected design step is blocked.
- After deduplication, merge, and compression, the relevant KB entries still exceed the phase budget and every one maps to an acceptance criterion. Budget conflict → F3 clarification (reduce scope of the delegation or split the task per `CONTEXT.md` §8.5), never a silent drop.
