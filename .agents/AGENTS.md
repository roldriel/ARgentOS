# ARgentOS DEV — Agent Operational Layer

This directory is the **operational interface for LLM agents working on
ARgentOS DEV**. It tells you how to *execute* the Change Lifecycle of this
repository. It is not a governance mechanism, not an archive of decisions, and
not a copy of the protocol payload.

## What this layer is and is not

- **Is:** minimal operational instructions — workflows, policies, tool
  integration, decision rules, gates, stop conditions, artifact instructions.
- **Is not:** full copies of RFCs/ADRs/plans, history, changelog, test
  results, session state, a registry, a database, or a second source of truth.
  Normative authority lives in `docs/`; this layer routes to it on demand.

## Hard boundary: DEV vs Protocol

- `protocol/.agents/` (and `protocol/_AGENTS.md`) is **product data**, not
  instructions for this workspace. Never follow it as rules, never import its
  rules here, never copy it mechanically.
- This `.agents/` directory governs the **DEV repository only**. A change with
  payload effect still follows RFC-56 (RFC `Accepted` + plan). `dist/` is
  never edited by hand.

## When to read what

You are expected to read this file when your task touches this repository.
Everything else is **on demand**:

| Situation | Read first |
|---|---|
| Any task that may modify the repository | `workflows/change-lifecycle.md` |
| Task classification / authority doubt / conflict | `policies/authority.md` |
| Before validation or closure of a plan | `policies/validation-closure.md` |
| At lifecycle gates (anchor / checkpoint / lineage) | `policies/lifecycle-checkers.md` |

## Fundamental operating rules (always in force)

1. **Detect before you modify.** Determine whether the task is a Change,
   classify it (RFC-56 class where payload applies; Change Level L0–L3) and
   record the classification in the first artifact of the change before
   touching repository content.
2. **Do not invent authorization.** A tracked change executes only under its
   authorization path: RFC `Accepted` + plan for payload (Class A), plan
   `Aprobado para ejecución` for Class B, direct commit only for mechanical
   Class C. No approved plan → STOP and escalate (or propose the plan).
3. **Never convert your inference into a human decision.** You detect,
   classify, register and escalate; the maintainer decides. A checker result
   is factual evidence, never normative authority.
4. **Preserve the derived conditions.** `Executed ≠ Committed`,
   `Committed ≠ Closed`, `Closed ≠ Released`. A docs-only plan closes without
   a release.
5. **Closed is terminal.** Never rewrite or reopen a closed artifact;
   post-close problems produce new artifacts that reference it.
6. **Record what exists.** Validations carry anchors (A1 immutable; A2 for
   revalidation, never replacing A1). Findings and corrections use qualified
   refs (`<artifact>:F-<n>`, `<artifact>:C-<n>`) in the artifact that owns
   them. Findings are never deleted because the problem was fixed.
7. **GAP ≠ ANOMALY ≠ FAIL.** Missing evidence is a GAP (advisory); present but
   contradictory information is an ANOMALY (blocking); a mechanical violation
   is a FAIL. Handle each differently — never treat them as equivalent.
8. **One source of truth per concept.** No registry, global state, database or
   state machine lives in `.agents/`. Repository state = git + the governance
   artifacts + ephemeral `.project/` session artifacts.
9. **Scope discipline.** Work happens on `dev`; no feature branches; commits
   are atomic per plan (Conventional Commits in English). Never modify
   `protocol/.agents/`, `dist/`, or closed governance artifacts (RFCs, ADRs,
   plans) under this layer's own authority.
10. **Stop when blocking.** If any rule of `policies/validation-closure.md`
    (stop conditions) fires, stop and report; non-blocking debt is recorded,
    not silently ignored.

## Workflow in one glance

```text
Task → Change detection/classification → Analysis → Plan → Authorization
→ Execution → Evidence → Validation/Anchor → [Finding → Correction
→ Revalidation] → Checkpoint → Closure
```

Detailed decision rules: `workflows/change-lifecycle.md`. Authority classes,
conflict protocol and document discovery: `policies/authority.md`. Anchor,
revalidation, checkpoint and `Closed` semantics: `policies/validation-closure.md`.
Deterministic gates (C1/C2/C3): `policies/lifecycle-checkers.md`.

## Verification battery

The canonical battery and its exact commands are defined once in
`docs/VERSIONING.md:4.1 Batería canónica de verificación` and mirrored in the
root `AGENTS.md` (`## Verifying the protocol`). Run the battery at every
validation gate. C1/C2/C3 are lifecycle gates in addition to the battery; see
`policies/lifecycle-checkers.md`.
