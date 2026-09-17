# Change Lifecycle — Operational Workflow (ARgentOS DEV)

Purpose: let an agent execute (or stop before executing) any repository change
without a human explaining the procedure. Decision rules are deterministic:
if X, do Y; if X is absent, STOP.

## 0. Intake: state before anything

1. Read the root `AGENTS.md`, then `.agents/AGENTS.md`.
2. Verify repository state (factual): `git status --short --branch`,
   `git rev-parse HEAD`. A dirty working tree is a fact to record, not a
   blocker by itself; concurrent edits to shared governance files are a risk
   (`docs/VERSIONING.md:8. Ejecución en paralelo`).

## 1. Change detection and classification

Ask: does this task modify repository content?

- **No** (answer, explain, review, report, diagnose): not a lifecycle
  execution. Produce the response with read-only evidence. No Plan is needed;
  if you later cite a validation as evidence inside a governance artifact,
  anchor it (VC-1).
- **Yes**: classify before any modification:

| Axis | Question | Where it is decided |
|---|---|---|
| Origin/type | feature, bug, problem, debt, audit finding, observation, direct maintainer action, agent proposal | first artifact (RFC draft, Plan, Note, commit message); RFC-75 Mecanismo 1 |
| RFC-56 class | only for payload effect on `protocol/.agents/`: A (model/contracts) → RFC `Accepted`; B (compatible documentary) → plan `Aprobado para ejecución`; C (mechanical) → direct commit | `docs/rfc/56-governance-fast-track.md` |
| Change Level | `max(coordination, scope, architectural impact, release impact, duration/complexity)`, coarse 0–3; commit count is never a dimension | RFC-75 Mecanismo 2; declared in the Plan header (`**Change Level:**`) |
| Change domain | payload (`protocol/`), DEV docs (`AGENTS.md`, `docs/`), tooling (`tools/`, `tests/`), runtime (`runtime/`), release | scope of the task |

Rules:

- Do not invent categories; reuse the origin/type vocabulary above.
- **L0 is provisional.** Recompute the Level before continuing when a trigger
  fires: a finding, a required revalidation, an ADR-worthy decision, multiple
  RFCs, or release-critical/architectural impact. If the change stops being
  L0, it goes through the Plan path.
- Classification is mutable: upgrade is mandatory when complexity appears;
  downgrade requires a documented justification in the owning artifact.
- When no origin tracker exists, the classification is recorded in the first
  artifact of the change (RFC-75 Mecanismo 1).
- There is no `Change` entity, no global tracker, no intake workflow: the
  Plan (or the commit message for Class C / direct action) is the record.

## 2. Authorization gate

Before touching the repository, resolve authority (`policies/authority.md`):

```text
Is the change pre-authorized?
  ├─ Yes: existing Plan `Aprobado para ejecución` (or RFC `Accepted` + plan
  │        for payload) with entry criteria satisfied → continue to §4.
  ├─ No, and payload effect → RFC `Accepted` required first; escalate.
  ├─ No, and documentary/implementation change → new Plan required; STOP and
  │        propose the plan (never create it silently, never execute it).
  └─ Mechanical Class C (typo, format, link; zero semantic change) → direct
           commit allowed after the battery is green; register in the next
           changelog entry.
```

Never execute an unapproved plan, never "execute" a plan whose entry criteria
are unmet (document the pending gate as a clarification instead), and never
convert your own proposal into approval.

## 3. Plan lifecycle

The Plan is the primary artifact of a tracked change.

- **Create** a Plan only when authorized to do so (maintainer request /
  approved backlog item). Use `docs/plans/_TEMPLATE.md`; take the next free
  number from `docs/plans/INDEX.md` (chronological order, never reused);
  register the plan in the INDEX in the same commit; declare `**Change
  Level:**` in the header (intake classification, Increment 1).
- **Consult** an existing plan when the task matches its scope; read its
  `Objetivo`, `Criterio de entrada`, `Pasos`, `Criterios de salida` and
  `Verificación`.
- **Execute** only under `Aprobado para ejecución` with entry criteria met.
- **Statuses are the existing ones**: `Aprobado para redacción`,
  `Aprobado para ejecución`, `Executed`, `Executed (parcial: …)`,
  `Superseded`. Do not invent states.
- Derived conditions: `Verified = ∃ validation(PASS, anchor)`;
  `Executed = implementation + validation` (legal without commit);
  `Committed` = repository state, not a Plan status; `Closed` = derived (see
  §9); `Released` = promoted + tagged (maintainer action). Do not mark
  `Executed` while exit criteria are unmet; use
  `Executed (parcial: <qué falta>)`.
- Never modify RFCs/ADRs/plans outside the authorized scope of your Plan;
  never rewrite closed history (RFC-46).

## 4. Execution on `dev`

1. Apply the plan's `Pasos` on `dev`, in scope. No feature branches.
2. Keep shared-file edits serialized or reserved before touching them.
3. Produce the change's evidence as you go (see §5). Preserve every existing
   field and record; additions for new plans follow the active rules, legacy
   artifacts are never rewritten to "comply".
4. If the task would touch `protocol/.agents/` and your plan is not RFC-56
   authorized: STOP, escalate.

## 5. Evidence

Every claim about the repository state must be backed by evidence or explicit
attestation. Evidence classes:

| Class | Produces | Example |
|---|---|---|
| FACTUAL | Git, tests, checkers | `git diff`, pytest result, C1/C2/C3 output |
| NORMATIVE | RFC/ADR/Plan (authority, not evidence) | `docs/rfc/75-change-lifecycle.md` |
| DECISION | human decision | maintainer approval of a plan |
| RELEASE | tags, `dist` | annotated tag on `master` |
| DESCRIPTIVE | INDEXes | `docs/plans/INDEX.md` (never authority) |

Record in the Plan's execution note: exact commands run, observed results, and
anything environmental that could affect reproducibility (tool versions,
interpreter, OS, network state).

## 6. Validation and anchors

Every registered validation is anchored (VC-1). Full field semantics:
`policies/validation-closure.md`.

1. Define the validation's declared scope and command-set.
2. Run the command-set (canonical battery + lifecycle gates as applicable).
3. Record the **Validation Anchor** in the owning artifact
   (`## Validation anchor` of the Plan template, or the RFC Amendment Log for
   audit rounds): declared scope, validation command-set, effective inputs
   (repo content), observed dependencies, environmental factors, Scoped
   Content Identity (state identity + delta identity), validity/stale.
4. Run C-1 (`policies/lifecycle-checkers.md`) — advisory check of the anchor.
5. PASS is evidence of execution within a declared environment, not a
   semantic guarantee. `anchor changed ≠ semantic validity changed`: evaluate
   applicability; revalidate or mark stale.

## 7. Findings, corrections and revalidation

Discovering a problem is an **expected workflow event**, not a failure of the
agent. Full semantics: `docs/CONVENTIONS.md` (Change Lifecycle — Findings y
correcciones; Incremento 2) and `policies/validation-closure.md`.

1. **Finding**: register `<artifact>:F-<n>` (namespace of the artifact that
   owns the record) with immutable elements — identity, original observation,
   original evidence (validation/anchor ref, Git state, `ruta:sección`),
   observed Git state, original provenance. State metadata evolves:
   `open`, `partially-resolved`, `resolved`, `deferred` (owner/destination),
   `superseded`. Never delete a finding because you fixed it; never rewrite
   the immutable elements.
2. **Correction**: the correction *action* is authorized by the approved Plan
   (or RFC-56 / Class C path). The `C-<n>` record is FACTUAL/TRACEABILITY,
   never normative: provenance to origin/finding + declared revalidation
   scope. A Plan authorizing a correction does not make the correction
   normative.
3. **Revalidation**: if the correction changes relevant scoped content or a
   declared environmental factor, re-run the **same contract** over the new
   state (S2) and register a **new anchor A2** referencing A1. A2 never
   replaces or mutates A1. Re-running on the same state is a note on the same
   validation, not an A2.
4. **Resolution** of a finding is a human decision with evidence (ADR-16
   AU-3). The agent registers, proposes and escalates; it does not resolve
   findings unilaterally.
5. Run C-3 after any real finding/correction records, before closure.

## 8. Checkpoint (before `Closed`)

Full semantics: `policies/validation-closure.md`; gate tool: C-2.

Do not collapse three distinct concepts: the **validated state** (what the
validation consumed), the **closure state** (what the checkpoint certifies, by
GC-1 correspondence with the applicable anchor) and the **materialized closing
commit tree** (a Git fact about the closing commit). The closing commit may
carry governance (RFC-75 `Mecanismo 7 — Git Checkpoints`), so
`validated tree == commit tree` is **not** a requirement.

1. Before declaring `Closed`, complete the plan's
   `## Checkpoint / cierre` record: closure commits (list; multi-commit is
   legal), validated state (reference to the anchor whose validated state
   corresponds to the closure state), the **closure state identity** (the
   anchor's delta scoped identity + state identity — the tree id of the staged
   index at validation time), the **materialized closing commit tree** when the
   commit already exists, and consistency checkpoint↔anchor.
2. Keep the declared Scoped Content Identity scope **fixed before** writing the
   closure records, so the closure state's identity over that scope is the
   anchor's by construction and the self-reference of the closure artifact
   cannot change it.
3. Run C-2. Consistency requires the scoped content identity of the closure
   state to equal the applicable anchor's and the declared environmental factors
   to be unchanged. If they differ → **revalidate first** (A2 on the closure
   state); do not derive `Closed` with a stale anchor. C-2 also verifies the
   materialized closing commit when it is declared (see `policies/
   validation-closure.md:5. Checkpoint (GC-1)`).
4. `Closed` is derived, not written as a status: `Executed` + applicable
   governance + checkpoint + consistency + PASS validation evidence for the
   closure state. A docs-only plan closes without a release (RFC-69).

## 9. Closure and handoff

1. Governance applied: INDEX mirrors updated; RFC Amendment Log entries when
   applicable; findings resolved or explicitly deferred with owner; no
   blocking pending decision without resolution/escalation (PC-1).
2. **Impact determinations (closure).** Record in the Plan's
   `## Checkpoint / cierre` exactly one of `REQUIRED` / `NOT_REQUIRED` /
   `DEFERRED` for **each** of two independent determinations (no fourth value,
   no silence, and never one value covering both):

   **a. Documentation impact** — *did this Change leave any current-state
   documentation obsolete or incomplete?* The documents that must stay correct
   (`docs/VERSIONING.md` §9 snapshot, `docs/plans/INDEX.md`, `ROADMAP.md`,
   `README.md`, `AGENTS.md` / `.agents/AGENTS.md` when active instructions
   change, and the active policies, workflows or contracts this Change
   modifies). Historical documents (RFCs, ADRs, closed plans, reports, audits,
   historical changelog entries, archived documents) are never updated for
   describing an old state (RFC-46). `REQUIRED` names the affected documents,
   the aspect affected, the update and its evidence (an empty `REQUIRED` is not
   acceptable); `NOT_REQUIRED` carries an explicit reason tied to the real
   scope (the bare value is not acceptable); `DEFERRED` reuses an **existing**
   pending decision (PC-1) with owner as its continuity — no new pending
   mechanism.

   **b. Roadmap impact** — *does this Change alter the operational map of
   future work?* Not "was `ROADMAP.md` edited": `REQUIRED` covers creating,
   completing, cancelling, reclassifying, re-prioritizing or re-dependency-ing
   work, discovering new work, or moving an item between candidate / active /
   blocked; `NOT_REQUIRED` covers changes with no effect on that map (internal
   refactor without scope change, purely technical fix, historical correction,
   documentation that does not move the map); `DEFERRED` covers a real impact
   whose update needs a decision or an authority not yet available, and reuses
   an **existing** pending decision (PC-1) with owner.

   `REQUIRED` in either one means the represented state must be reconciled
   before closure, **but it does not mean "always edit `ROADMAP.md`"**: the
   artifact to update follows ownership / source of truth (`ROADMAP.md` for the
   operational map, `docs/plans/INDEX.md` for the plan registry, the RFC/ADR
   indexes, an active plan, or the operational documentation that owns the
   state). `ROADMAP.md` stays an operational map, never a changelog. The two
   determinations are independent: `Documentation impact: REQUIRED` with
   `Roadmap impact: NOT_REQUIRED` is perfectly valid, and so are
   `REQUIRED`/`REQUIRED` and `NOT_REQUIRED`/`REQUIRED`.

   Payload changes keep their own changelog/`VERSION` rule; neither
   determination adds a changelog obligation. Full semantics and the Plan-less
   (Class C) form: `policies/validation-closure.md:5.1 Documentation impact
   (closure determination)` and `policies/validation-closure.md:5.2 Roadmap
   impact (closure determination)`. A missing determination blocks closure
   (stop condition).
3. Changelog: docs-only plans add an `[Unreleased]` item `(plan N, RFC-N)`;
   no `VERSION` bump, no tag.
4. Mark the plan `Executed` and derive `Closed` only after the checkpoint
   above. Committing on `dev` (atomic, Conventional Commit in English) is the
   maintainer's repository action; `Closed` may exist before the commit, but
   the checkpoint records the validated closure state.
5. Post-close problems: create new artifacts referencing the closed plan
   (post-close by reference); never reopen or rewrite it.

## 10. GAP vs ANOMALY vs STOP

| Signal | Meaning | Action |
|---|---|---|
| GAP | required evidence absent / not verifiable | advisory: obtain or complete the evidence; record it; continue only when the gate needs it |
| ANOMALY | information present but contradictory, or demonstrable violation | STOP; register finding/correction; fix via authorized path; revalidate before continuing |
| BOUNDARY | structural ambiguity (checker signal) | human review; never guess or invent a tie-break |
| N/A / EXCLUDED | not applicable / legacy | expected; not invalidity |
| FAIL | mechanical violation (battery) | fix or document deviation accepted by the maintainer; never report as PASS |

Do not use STOP to freeze on minor imperfection: classify non-blocking debt
and record it. Stop conditions that always block are listed in
`policies/validation-closure.md` (stop conditions).

## 11. Dogfooding example (this repository)

Task: "Add a new DEV operational policy document (docs-only change)."

```text
Intake: dev clean; confirm branch and HEAD (`git status`, `git rev-parse
        HEAD`).
Classify: origin = maintainer request; domain = DEV docs + new layer;
         RFC-56 class: none (no payload effect);
         Change Level = L2 (multi-area scope, new operational seam).
Authorize: an existing Plan `Aprobado para ejecución` with entry criteria
          met? → Yes: execute its steps. No: STOP; propose the Plan and wait
          for maintainer authorization. Drafts live in the gitignored staging
          area (`sessions/`), never committed.
After authorization: execute plan steps → materialize → battery + C1/C2/C3
→ anchor → checkpoint → Closed (docs-only) → commit on dev per the plan.
```

This demonstrates the full loop without executing an unauthorized change:
detection, classification, authority lookup, plan proposal, gate, and the
validation/closure machinery that will verify the result.
