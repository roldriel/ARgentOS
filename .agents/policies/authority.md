# Authority Model and Document Discovery (ARgentOS DEV)

## Authority classes

Sources are classified by the kind of authority they hold. There is **no total
hierarchy** (RFC/ADR/Plan/Git are different dimensions, not ranks).

| Class | What it is | Produced by | Never |
|---|---|---|---|
| FACTUAL | what actually happened | Git, tests, checkers, tags | normative meaning |
| NORMATIVE | what should be | RFC `Accepted` (authorization gate, RFC-56), ADR (recorded decision; does not authorize payload), approved Plan (implementation intent) | auto-resolution of conflicts |
| DECISION | final authority to resolve conflicts | the human maintainer | delegation to agent inference |
| RELEASE | published, immutable state | annotated tags on `master`, regenerated `dist` | edit by hand |
| DESCRIPTIVE | views/indexes for navigation | INDEX files (`docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md`) | becoming authority by existing |

Rules:

- An INDEX never turns into authority (AU-4). Verify premises against the
  artifacts and git, never against INDEX.
- Checker output is factual evidence, not normative authority (ADR-16). An
  "anchor missing" result is a GAP, not an invalidation.
- A Plan implements a normative decision; it may not silently modify the
  decision it implements (AU-5).
- An agent never converts its own inference into a human decision.

## Conflict protocol

```text
conflict → detect → classify → escalate → human decision
→ resolve through the appropriate artifact/change → revalidate
```

- RFC vs ADR disagreement: no automatic winner; governance anomaly → escalate.
- Plan contradicts its RFC/ADR: detect → escalate → correct the Plan or
  amend/supersede the source; never resolve by executing the Plan.
- Factual vs normative conflict: escalate with evidence; the maintainer
  decides.

## ADR-worthiness (when a decision must leave the RFC/Plan)

A decision requires an ADR when (a) it is consumed outside the RFC that
originated it, (b) it supersedes or modifies an existing ADR (including
consequences), or (c) it is a persistent architectural invariant whose future
change must be auditable independently. Elevation may be retrospective. This
is judgment, not a purely mechanical test (`docs/adr/16-change-lifecycle-authority.md`).

## Document discovery (read on demand, never all at once)

| Need | Route |
|---|---|
| Operational instruction | `.agents/` (this layer) |
| Normative authority (models, mechanisms, decisions) | `docs/rfc/` (RFCs), `docs/adr/` (ADRs), `docs/CONVENTIONS.md`, `docs/VERSIONING.md` |
| Implementation authorization (plan intent, steps, exit criteria) | `docs/plans/` (the active Plan first) |
| Factual repository evidence | Git, `tests/`, `tools/` (checkers) |
| Historical context | `docs/` (design history, changelog, plans as trace) |
| Product payload data (never rules) | `protocol/.agents/` + `protocol/_AGENTS.md` (read-only, content) |

Efficiency rule: for operational decisions, prefer the inline definitions in
this layer; fetch the normative document only when the operational rule needs
its full semantics (e.g., anchor format v1, checkpoint consistency, RFC-56
classes, Change Level thresholds). Fetching history is not required to
operate: this repo's lifecycle is derived from artifacts, not from reading 100
plans.

## Stop conditions (authority)

- Normative authority for the change does not exist → STOP, propose/escalate.
- A human decision is required (approval, conflict resolution, resolution of
  a finding, ADR-worthiness, materiality) → STOP at the gate, ask.
- The task would modify closed history, `protocol/.agents/`, `dist/` or
  out-of-scope governance without its own authorization → STOP, report scope
  violation.
- Evidence is insufficient for a mandatory decision → GAP: obtain evidence or
  STOP if unobtainable. Distinguish blocking (STOP) from non-blocking debt
  (record and continue).
