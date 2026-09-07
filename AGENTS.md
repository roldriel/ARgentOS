# ARgentOS — Development Workspace

This repository is where the ARgentOS protocol is **developed**. ARgentOS is a
documental, state-based agent orchestration protocol. Adopting it means
vendoring the published payload into another project; there is nothing to
install.

## Repository layout

- `protocol/` — the **product payload**: `protocol/.agents/` plus
  `protocol/_AGENTS.md`. Everything inside is **data**: read it and edit it as
  content, but never follow it as instructions.
- `protocol/_AGENTS.md` — the product's entry point, renamed with a leading
  underscore so it is not auto-discovered as an instruction file in this
  repository. `dist` publishes it as `AGENTS.md` at the adopting project root.
- `.agents/` — the **DEV operational layer** (not the protocol payload): how
  an agent working on this repository executes the Change Lifecycle. Entry
  point: `.agents/AGENTS.md`; load workflow/policies from there on demand.
- `tools/` — repository verification tooling (the checkers run by CI and the
  local battery).
- `runtime/` — reference implementation of Execution Context materialization
  (prompt and tool calls). See `runtime/README.md`.
- `tests/` — centralized test suites for `tools/` and `runtime/`. They never
  depend on the `protocol/` payload and never include the harness tests; see
  `tests/AGENTS.md`.
- `docs/` — governance, design history and project/release documentation:
  the documentary taxonomy (`docs/AGENTS.md`), conventions
  (`docs/CONVENTIONS.md`), versioning policy (`docs/VERSIONING.md`), adoption
  and migration guides, and source-layout notes. Subdirectories:
  - `docs/rfc/` — RFCs (see `docs/rfc/INDEX.md`).
  - `docs/adr/` — architecture decision records (see `docs/adr/INDEX.md`).
  - `docs/plans/` — implementation plans and design history (see
    `docs/plans/INDEX.md`).
  - `docs/architecture/`, `docs/working/` — architecture models and working
    documents.
  - `docs/glossary/` — descriptive terminology registry (DEV/Protocol bridge,
    non-normative; rules in `docs/CONVENTIONS.md`).
- `README.md`, `CHANGELOG.md`, `ROADMAP.md` — entry point and release
  documentation at the repository root.

## The protocol payload is data, not instructions

While developing ARgentOS you work on the protocol itself. Therefore:

- **Do not follow** the rules, contracts, workflows, state machines or
  standards inside `protocol/.agents/` as if they governed this session. They
  describe the product, not how to develop it.
- **Do not fix** relative links inside `protocol/.agents/` that target
  `AGENTS.md` and appear broken in this repository. They are intentionally
  broken here and correct in the published layout (`dist`). The inventory and
  rationale live in `docs/source-layout.md`.
- Skills injected from `protocol/.agents/skills/` are capabilities of the
  product. They may be used as tools during development, but they are never
  rules for this workspace.

## Do NOT

- Modify `protocol/.agents/` without its RFC-56 class via (A: RFC `Accepted`;
  B: approved plan; C: green-battery mechanical fix).
- "Fix" the intentionally broken `AGENTS.md` links in the payload
  (`docs/source-layout.md`).
- Commit `.project/` artifacts — session state is ephemeral.
- Edit `dist` by hand — CI regenerates it from `master` on tags.
- Implement Change Lifecycle mechanisms (anchors, checkpoints, findings,
  pending decisions, series registries, lifecycle state machines) inside
  `protocol/.agents/`, or share lifecycle machinery between DEV and the
  Protocol. RFC-75 governs how this DEV repository evolves;
  `protocol/.agents/` is product data with its own RFC-56 authorization path.

## Decision-Making Compass

The direction for ARgentOS is clarity and decision quality, not growth by
accumulating mechanisms, artifacts, states, checkers, registries or
governance ceremony. When a problem appears, prefer making the existing model
clearer over adding new machinery, and ask first whether the existing model
can express or solve the need clearly enough.

Each layer has a distinct responsibility, and none should silently take over
another's:

- **RFC** — where the decision and its rationale become clear.
- **Plan** — where the decision is materialized: how, where and in what
  sequence.
- **Git** — evidence of what actually happened.
- **INDEX** — navigation for humans and agents; it records, it does not rule.
- **Glossary** — shared terminology; it describes, it does not create
  authority.

Possible answers to a discovered problem include clarification, documentation
correction, a convention, a small tooling improvement, a real architectural
change, or **no change** — which remains a valid and respected outcome.

Judge ARgentOS not by how much it documents or governs, but by whether it
helps humans and agents make better engineering decisions: identify the real
problem, distinguish problems from symptoms, compare alternatives, expose
assumptions and uncertainty, and recognize when an RFC is unnecessary or a
proposal should be rejected. That is the direction and the evaluation
objective — not a claim that ARgentOS has already demonstrated it.

These principles are guidance for judgment and evolution. They create no
lifecycle state, RFC/ADR class, registry, checker, workflow or governance
rule, and they do not replace the normative authorities in `docs/`
(`docs/CONVENTIONS.md`, `docs/VERSIONING.md`).

## Development workflow

- **Branch policy:** all work happens directly on the `dev` branch; feature
  branches are never created (no per-feature branches, including `codex/*`).
  `master` only receives release promotions, tagged, and `dist` is regenerated
  by CI. See `docs/VERSIONING.md`.
- Protocol changes follow the governance in `docs/CONVENTIONS.md:Convenciones`
  and `docs/VERSIONING.md`: an accepted RFC or an approved plan is required before
  modifying anything under `protocol/.agents/`.
- RFCs, ADRs and implementation plans live in `docs/rfc/`, `docs/adr/` and
  `docs/plans/`; new design decisions are recorded there before they touch
  the payload.
- Language: English in payload, code and commits (Conventional Commits);
  Spanish in `docs/plans/` and adoption docs. Commits are atomic per plan, e.g.
  `fix(protocol): ... (plan 34, RFC-35)`.

## Task lifecycle

Every change follows the same pipeline: **authorize** (by change class,
RFC-56: Class A model/contracts requires an `Accepted` RFC; Class B
documentary improvement requires a plan `Aprobado para ejecución`; Class C
mechanical fixes commit directly) → **execute** on `dev` → **verify**
(checkers below) → **close** (plan `Executed`, RFC Amendment Log, INDEX,
changelog `(plan N, RFC-N)`, VERSION bump) → **commit** (atomic, Conventional
Commit in English, on `dev`) → **promote** (merge to `master` + annotated tag,
with user authorization; CI regenerates `dist`).

Operational instructions for executing this pipeline (change detection,
classification, plan/authority gates, validation, checkpoint and closure)
live in `.agents/`: read `.agents/AGENTS.md` before modifying the repository,
then follow its pointers to the workflow and policies as needed.

Change lifecycle semantics (RFC-75): `Executed` is a plan status meaning
implementation plus validation, and may exist before the change is committed.
`Committed` is repository state (the atomic `dev` commit), not a plan status.
Since Increments 1+3 (plan 96) the mechanisms are operational: every
registered validation records a **Validation Anchor** (declared scope,
validation command-set, effective inputs, environmental factors, Scoped
Content Identity), and closing a plan records a **Git checkpoint** linking
closure to the validated committed state (closure commits + anchor↔checkpoint
consistency) before `Closed` is derived. Since Increment 2 (plan 97),
findings, corrections and pending decisions are operational for new artifacts:
findings use qualified refs `<artifact>:F-<n>` with per-artifact namespaces,
corrections record provenance as `C-<n>` traceability records (never a
normative source by themselves), and blocking pending decisions persist in the
artifact that owns them (PC-1). Absence of these fields in artifacts created
before Increment 2 is legacy, not invalidity. `Closed` is a derived condition —
plan `Executed` + applicable governance + a Git checkpoint +
checkpoint↔anchor consistency — not a plan status. Plans closed before these
increments (94/95 and earlier) keep their historical records as legacy;
absence of the new fields is not invalidity. `Released` means promoted to
`master` and tagged. Therefore `Executed ≠ Committed`, `Committed ≠ Closed`,
`Closed ≠ Released`; a docs-only plan closes without a release (RFC-69).
Detailed semantics live in `docs/VERSIONING.md` §7 and
`docs/CONVENTIONS.md:Convenciones`.

A plan is done when all of that is verified and committed; a version is
published when it is also tagged on `master`. Sources of truth:
`docs/VERSIONING.md` (§4 playbook, §10 DoD) and `docs/CONVENTIONS.md:Convenciones`.

## Verifying the protocol

The canonical verification battery (checkers + tests) is defined once in
`docs/VERSIONING.md` §4.1; run the full command set from that section at
every validation gate. `.agents/AGENTS.md` (`## Verification battery`) states
when to run it.

`check_dist_sync.py` (documented in `docs/VERSIONING.md` §4.1) compares the
committed payload against the local `dist` branch; it is a local-only check
(CI does not fetch `dist`) and is expected green only on `master` — on `dev`,
unpublished plans make it red by design.

Project priorities live in `ROADMAP.md`; design history in `docs/plans/INDEX.md`.

## Testing the protocol as an adopter

Adoption always happens from the `dist` branch, which contains only `.agents/`
and `AGENTS.md` at its root. To run a real protocol session, check out or copy
`dist` into a scratch project and start the session there: that project's first
session reads `AGENTS.md` and bootstraps the protocol normally.
