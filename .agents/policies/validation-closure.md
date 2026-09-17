# Validation, Revalidation, Checkpoint and Closure (ARgentOS DEV)

These are operational definitions of mechanisms materialized by RFC-75
Increments 1+3/2 (plans 96/97). Normative depth:
`docs/CONVENTIONS.md` (Change Lifecycle sections) and RFC-75 mechanisms 6–9.
This file defines only what an agent needs to execute.

## 1. Registered validation and anchors (VC-1)

A **registered validation** is any validation cited as evidence in a DEV
governance artifact (plan execution note, RFC audit round, plan closure).
Every registered validation has a **Validation Anchor** recorded in the
artifact that owns the validation.

Anchor fields (v1):

| Field | Meaning |
|---|---|
| Declared scope | what the author claims the validation covers |
| Validation command-set | exact commands that constitute the validation |
| Effective inputs (repo content) | content the command-set actually consumes |
| Observed dependencies | discovered subset of effective inputs (or `no instrumentado`) |
| Environmental factors | non-repo inputs consumed (tool versions, env vars, interpreter, network) |
| Scoped Content Identity | deterministic identity of the scoped repo content (below) |
| Validity / stale | current applicability of the anchor |

**Scoped Content Identity** (algorithm v1):

- Delta identity: for the scope set (repo-relative paths, sorted), blob id per
  path + `sha256` over the canonical serialization `scoped-v1` of
  path + blob pairs.
- State identity: when the command-set consumes the whole repo, the Git
  **tree id** (`git write-tree` over the staged state). Tree ids are
  content-addressed: identical content → identical tree id, independent of
  history.
- A commit SHA is a locator, never semantic identity. Rebase/amend with
  identical scoped content does not invalidate identity; different content →
  evaluate applicability / revalidate.

## 2. Validity is relative to the anchor (CL-2)

- `anchor changed ≠ semantic validity changed`. A later state S2 does not
  automatically invalidate V1 (valid for S1). If relevant scoped content
  changed and no applicable revalidation exists, V1 is `stale` for S2: before
  `Closed`, a revalidation PASS over S2 is required.
- A change outside the scope does not alter delta identity; a changed tree id
  triggers applicability evaluation, not automatic invalidation.
- Unknown environmental dependencies are an accepted limit: they are the
  author's responsibility, and revalidation is the backstop.

## 3. Revalidation (A2)

Revalidation = re-running the **same contract** over a new relevant Git state
(S2).

- A2 is its own registered validation with its own anchor **on S2**.
- A2 may reference A1 as lineage origin, but never replaces, mutates or
  reinterprets A1. Chain: `A1 → A2` (historical), never `A1 becomes A2`.
- Minimal A2 record: reference to A1, revalidated state (locator + new
  Scoped Content Identity), command-set (may reference A1's when identical),
  relevant environmental changes (others confirmed unchanged), result.
- Re-running on the same state (no relevant scoped change) is a note on the
  same validation, not a new A2.
- No entity/registry/state machine exists for revalidation: it is an evidence
  relationship between validations.

## 4. Findings / corrections / revalidation lineage (LC-1)

- Finding: qualified ref `<artifact>:F-<n>` registered in the owning
  artifact. Immutable: identity, original observation, original evidence,
  observed Git state, original provenance. Evolvable: lifecycle metadata
  (`open`, `partially-resolved`, `resolved`, `deferred` with owner/destino,
  `superseded`; reopening = new finding referencing the original or a
  `reopened` metadata record).
- Correction: qualified ref `<artifact>:C-<n>`; FACTUAL / traceability
  record. Preserves provenance to origin/finding and declares its
  revalidation scope (CL-6). Never a normative source by itself.
- N:M cardinalities apply: 1 finding → N corrections; N findings → 1
  correction; 1 correction → N revalidations.
- Post-close findings live in new artifacts referencing the closed one; the
  closed artifact is never reopened.
- A finding's resolution (`resolved`, etc.) is a human decision with evidence.

## 5. Checkpoint (GC-1)

A checkpoint is the documented relation **closure ↔ Git state**; it is not an
artifact, not "having a commit", not a SHA.

Record (plan `## Checkpoint / cierre`):

- Closure commits (list; multi-commit legal).
- Validated state (reference to the anchor whose validated state corresponds
  to the closure state).
- Closure state (Git tree id).
- Consistency checkpoint↔anchor: PASS/FAIL + evidence.
- Governance applied and derived condition.
- Documentation impact determination (5.1).
- Roadmap impact determination (5.2).

Consistency rule: `Closed` requires the scoped content identity of the closure
state to equal that of the applicable anchor **and** declared environmental
factors unchanged. If a revalidation A2 covers the closure state, evaluate
against A2; if the closure state is still A1's state, against A1. Existence of
A2 never removes A1. Any difference → **revalidate before `Closed`**.

### 5.1 Documentation impact (closure determination)

Every DEV Change determines, at closure, its impact on **current-state
documentation**. This is a governance record inside the closure that already
exists, not a phase, a state, a gate, an entity, an authority, an ID
namespace, a registry or a tracker. Git remains the authority on the effective
state; the determination is a statement about documentation, never a source of
truth for the repository state.

Exactly one classification, never a fourth value and never silence:

| Classification | Meaning |
|---|---|
| `REQUIRED` | the Change modifies, invalidates, makes obsolete or otherwise alters information that must stay correct in current-state documentation |
| `NOT_REQUIRED` | the Change does not alter any current-state documentation that must stay in sync |
| `DEFERRED` | a documentation impact is identified, but the update cannot or must not be made yet |

Minimum record:

- **`REQUIRED`** — affected documentation (exact repo-relative paths), the
  aspect affected, the update that corresponds, and the evidence that the
  update was made or correctly incorporated into the Change before closure. An
  empty `REQUIRED` is not acceptable.
- **`NOT_REQUIRED`** — an explicit, verifiable reason tied to the real scope of
  the Change. The bare classification is not acceptable: "creo que no afecta",
  "parece que no", "no fue necesario" or "se revisó documentación" without the
  result are not evidence.
- **`DEFERRED`** — the documentation left pending, why it is deferred, and the
  **existing** pending decision (PC-1) that governs the deferral and holds the
  continuity, with owner. `DEFERRED` creates no new pending mechanism: it
  reuses per-artifact pending decisions. An impact deferred without an owning
  pending decision is not `DEFERRED`; it is an unresolved blocking condition.

**Current-state scope.** A document is current-state when it describes how the
repository currently works or in what state it currently is. Consider at
least: `docs/VERSIONING.md` (in particular its current-state snapshot),
`docs/plans/INDEX.md` (navigation and current-state information), `ROADMAP.md`,
`README.md`, `AGENTS.md` and `.agents/AGENTS.md` when active
behaviour/instructions change, active policies under `.agents/policies/`,
active workflows under `.agents/workflows/`, and active contracts whose
semantics the Change modifies; plus any other document the Change itself
identifies as current-state.

**Historical exclusion.** Historical documentation is never updated merely
because it describes an older state: historical RFCs, historical ADRs, closed
plans, historical reports, audits, historical changelog entries and archived
documents. Historical documentation keeps its historical context (RFC-46);
post-close problems produce new artifacts that reference the closed one.

**Preemption.** Changes to `protocol/.agents/` preempt this rule and keep their
own obligation: the `CHANGELOG.md` entry and the `protocol/.agents/VERSION`
bump per `docs/VERSIONING.md` §3/§5. This determination neither replaces nor
weakens the changelog rule, and it never requires a changelog entry of its own.

**VERSIONING snapshot.** The current-state snapshot of `docs/VERSIONING.md` §9
is reconciled at promotion/release, or when the Change has an explicit impact
on that snapshot; it is never updated in every Change. A divergence between the
snapshot and Git is never used to invent a version or to modify that document
arbitrarily; Git (`git tag` + `protocol/.agents/VERSION`) prevails.

**Where it is recorded.** In the `## Checkpoint / cierre` record of the Plan
(the template carries the field), so the determination is part of the closure
the checkpoint documents. For a change with no Plan (Class C / direct action),
it goes with the intake classification in the commit message — `REQUIRED:
<paths> — <evidence>` or `NOT_REQUIRED: <reason>`, or `DEFERRED: <paths> —
<pending-decision ref>` —, in the place where the Change Lifecycle already
requires the classification of a Plan-less change.

**Enforcement.** The obligation is governance, not a semantic validation. No
checker interprets prose or decides whether a document is up to date, and no
checker is added for this. Absence of the determination, or a classification
outside the three values, is a stop condition (see §7).

### 5.2 Roadmap impact (closure determination)

Every DEV Change determines, at closure and **independently of §5.1**, its
impact on the **operational map of future work**. Same vocabulary — exactly one
of `REQUIRED` / `NOT_REQUIRED` / `DEFERRED`, never a fourth value and never
silence — and the same governance nature: a record inside the closure that
already exists, not a phase, state, gate, entity, authority, ID namespace,
registry or tracker.

The question is not "was `ROADMAP.md` edited?" but *does this Change alter the
operational representation of future work, in the source of truth that owns it?*

| Classification | Meaning |
|---|---|
| `REQUIRED` | the Change materially modifies the operational map of future work: it creates future work, completes work of the map, cancels work, changes an item's state, priority or dependency, discovers new work, turns a candidate into active work or active work into blocked/requires-authorization, or substantially changes the nature of an item |
| `NOT_REQUIRED` | the Change does not modify the operational map of future work: an internal refactor without scope change, a purely technical fix with no backlog impact, a historical correction that does not alter future work, or documentation that does not change the operational map |
| `DEFERRED` | an impact or potential impact exists, but its update requires a decision or an authority that is not yet available |

Rules:

- **`REQUIRED` does not mean "always edit `ROADMAP.md`".** It means the
  operational state the map represents must be **reconciled before closure**,
  unless an explicit authorized deferment exists. Which artifact must be updated
  follows **ownership / source of truth**: `ROADMAP.md` (the operational map),
  `docs/plans/INDEX.md` (plan registry), `docs/rfc/INDEX.md` /
  `docs/adr/INDEX.md` (RFC/ADR registries), an active plan, or the operational
  documentation that actually owns the state.
- `ROADMAP.md` remains an **operational map, not a changelog**: it does not
  catalogue closed history and does not duplicate the detailed state of plans.
- **The two determinations are independent.** Every combination is valid —
  `Documentation impact: REQUIRED` with `Roadmap impact: NOT_REQUIRED`,
  `Documentation impact: REQUIRED` with `Roadmap impact: REQUIRED`, or
  `Documentation impact: NOT_REQUIRED` with `Roadmap impact: REQUIRED`. Neither
  implies nor replaces the other and they are never merged into one value.
- **Minimum record.** `REQUIRED` — the artifacts/items added, completed,
  cancelled, reclassified or re-prioritized, the update made and its evidence.
  `NOT_REQUIRED` — an explicit, verifiable reason tied to the real scope of the
  Change (the bare classification is not acceptable). `DEFERRED` — the impact
  left pending, why it is deferred, and the **existing** pending decision (PC-1)
  that governs the deferral and holds the continuity, with owner. An impact
  deferred without an owning pending decision is not `DEFERRED`; it is an
  unresolved blocking condition.
- **Historical exclusion and payload preemption** are the same as §5.1, and the
  `docs/VERSIONING.md` current-state snapshot is likewise reconciled at
  promotion/release, never in every Change.

**Where it is recorded.** Next to the §5.1 determination in the Plan's
`## Checkpoint / cierre` record (the template carries the field). For a change
with no Plan (Class C / direct action) it goes with the intake classification in
the commit message — `Roadmap impact: REQUIRED: <items> — <evidence>`,
`Roadmap impact: NOT_REQUIRED: <reason>` or `Roadmap impact: DEFERRED: <items> —
<pending-decision ref>`.

**Enforcement.** Identical to §5.1: governance, not a semantic validation; no
checker interprets prose; absence of the determination or a classification
outside the three values is a stop condition.

Full normative semantics of both determinations:
`docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de cierre: impacto
documental e impacto de Roadmap (regla operacional)`.

## 6. Derived conditions

```text
Verified   = ∃ validation(PASS, anchor)
Executed   = Plan status "Executed" (implementation + validation)
Committed  = repository state (atomic dev commit), not a Plan status
Closed     = Executed ∧ governance applied ∧ ∃ checkpoint ∧ consistency
             ∧ PASS evidence for the closure state (derived, not a status)
Released   = promoted to master and tagged (maintainer action)
```

- `Committed ≠ Closed ≠ Released`. Docs-only plans close without a release
  (RFC-69).
- Closed is terminal for the plan; later changes are new artifacts.

## 7. Stop conditions (validation/closure)

Blocking (STOP — do not close, escalate with evidence):

- A critical checker reports ANOMALY (present-but-contradictory evidence).
- Closure state differs from the validated state and no revalidation PASS
  covers it (GC-1 consistency fails).
- Findings are open without resolution or explicit deferral with owner;
  a blocking pending decision persists without resolution/escalation (PC-1).
- Closure without an explicit Documentation impact determination (5.1) or
  without an explicit Roadmap impact determination (5.2), or with a
  classification outside `REQUIRED` / `NOT_REQUIRED` / `DEFERRED` in either.
- Attempted modification of closed history or out-of-scope artifacts.
- A human decision is required for a mandatory resolution.

Non-blocking debt (record, continue):

- GAP outputs (advisory missing evidence) where the gate does not require it.
- Observations/findings without blocking impact; legacy artifacts without the
  new fields (absence = legacy, not invalidity).
- Minor imperfections that do not affect the declared validation scope.
