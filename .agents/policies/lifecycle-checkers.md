# Lifecycle Gates — C1/C2/C3 (tool integration)

The three deterministic lifecycle checkers are **advisory, factual, DEV-only**
evidence. They have no normative authority: GAP never turns the exit code
non-zero; only ANOMALY does. They complement — they do not replace — the
canonical battery (root `AGENTS.md`, `## Verifying the protocol`).

Common output vocabulary per inspected plan artifact:

| Signal | Meaning | Agent action |
|---|---|---|
| `VALID` | record present and consistent | proceed |
| `GAP` | required information missing/not verifiable (advisory) | complete evidence or record why not; proceed unless the gate needs it |
| `ANOMALY` | information present but contradictory | STOP; register finding/correction; fix via authorized path; revalidate before continuing |
| `BOUNDARY` | structural ambiguity / intake signals without container | human review; never guess |
| `N/A` | no record to verify (empty section, declared absence) | expected for planned/open or clean artifacts |
| `EXCLUDED` | legacy artifact outside the new regime | expected; not invalidity |

Exit codes: `0` unless at least one ANOMALY is found (`1`); C-3 returns `2`
only on unrecoverable read errors.

## C-1 — Lifecycle anchor check

- Tool: `python tools/check_lifecycle_anchor.py` (optional `--root REPO_ROOT`).
- What: verifies the `## Validation anchor` section of numbered plans under
  `docs/plans/` that belong to the new Change Lifecycle regime (structural
  membership: both template container sections present).
- When: after any registered validation is recorded in a plan (VC-1 gate),
  including revalidations.
- Meaning: `VALID` = anchor present and structurally consistent with the v1
  minimum fields; `GAP` = field missing/not verifiable; `ANOMALY` =
  contradiction (e.g., declared FAIL as PASS).
- **Identity literals present vs. deferred (contract fixed by Plan 147).** The
  Scoped Content Identity literals are `State identity` (40-hex tree id) and
  `Delta scoped identity` (64-hex sha256). R-C1-4 judges their **format**: a
  literal that is **present but malformed** is an `ANOMALY` (contradiction). A
  subfield that presents no value and **declares the identity resolved outside
  the anchor** — the corpus anti-self-reference convention (plan 96 §13;
  precedent plans 114/116/134/140–146), which transcribes the literals in the
  closing commit and is what `master`'s released revision of plan 146 carries —
  is a declared **absence**, classified `GAP` (advisory), never `ANOMALY`.
  Missing evidence is not a contradiction (`.agents/AGENTS.md` rule 7). The
  discriminator is whether the subfield **declares a value after its label**,
  not the shape of the token: a malformed literal also carries no hex, so a
  width test alone could not separate an invalid value from a legitimate
  deferral. The rule does not weaken format checking: any presented value that
  is not the expected hex remains an `ANOMALY`.
- Action: on `VALID`, cite the output as anchor evidence; on `GAP`, fill the
  missing fields or record the gap; on `ANOMALY`, STOP and follow the
  finding/correction path.

## C-2 — Lifecycle checkpoint check

- Tool: `python tools/check_lifecycle_checkpoint.py` (optional `--root`).
- What: verifies the checkpoint/closure record (`## Checkpoint / cierre`)
  and its consistency with the applicable validation anchor (GC-1).
- **What it verifies, and what it does not (contract fixed by Plan 134).** C-2
  distinguishes three concepts that are not interchangeable — the **validated
  state**, the **closure state** (what the checkpoint certifies) and the
  **materialized closing commit tree** — and verifies only the normative
  relations: (R2) the declared closure state corresponds to the applicable
  anchor's validated state, selected by correspondence; (R3) `Closed` carries
  PASS evidence for that state; (R4) a declared materialized closing commit is
  resolved and checked. It does **not** require the declared closure state to
  equal the tree of the final closing commit: RFC-75
  `docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints` allows the
  closing commit to carry governance, so `validated tree == commit tree` is not
  a requirement. The closure state is the Git **tree id** of the staged index at
  closure time; commit SHAs are locators only. Anchor selection is by
  correspondence of validated state to closure state — never by recency
  ("latest A2 wins") and never by generic tree membership.
- When: before declaring `Closed` (GC-1 gate) and after any revalidation
  that changes the applicable anchor.
- Meaning: `VALID` = checkpoint present and consistent (A1 or A2 per
  correspondence); `GAP` = insufficient evidence; `ANOMALY` = contradiction
  (declared closure state contradicting a declared materialized commit tree,
  A2 without A1 lineage, declared FAIL while Closed, etc.).
- Action: on `VALID`, derive `Closed`; on `GAP`, complete the checkpoint
  record; on `ANOMALY`, STOP — do not close; correct and revalidate first.
- Model: `docs/CONVENTIONS.md:Change Lifecycle — Estado de cierre, grafo de
  commit y árbol material (modelo, Plan 134)`. Plan 134 declared C-1 and C-3
  `NOT_REQUIRED` for this chain: neither reads the closure state.

## C-3 — Lifecycle lineage check

- Tool: `python tools/check_lifecycle_lineage.py` (optional `--root`).
- What: verifies form, minimal completeness and internal consistency of
  finding/correction/revalidation lineage (LC-1) in the
  `## Findings / Correcciones / Pending` container (subsections
  `### Findings` / `### Correcciones`; `### Pending decisions` is out of v1
  scope): qualified refs `<artifact>:F-<n>`/`C-<n>`, state vocabulary,
  immutable finding elements, correction provenance/origin and declared
  revalidation scope, support for revalidation claims from the artifact's own
  anchor/checkpoint, absence markers, resolution consistency.
- When: after any real finding/correction record, before closure; also after
  revalidation when corrections exist (lineage gate).
- Meaning: `VALID` = records complete and consistent; `GAP` = missing or
  ambiguous (advisory; includes `reopened` and duplicate-validation
  ambiguity — human review); `ANOMALY` = verifiable contradiction
  (e.g., duplicate identity, cross-artifact ref to a nonexistent artifact,
  resolution referencing a missing correction).
- Action: on `VALID`, proceed to checkpoint; on `GAP`, complete the records or
  escalate ambiguity to the human (never invent a tie-break); on `ANOMALY`,
  STOP, register a finding/correction and fix before closure.

## Where they run in the workflow

```text
Validation recorded → C-1
Finding/correction records exist → C-3
Before Closed → C-2 (after C-1/C-3 signals are resolved)
Revalidation A2 recorded → C-1 (and C-3 if corrections exist), then C-2
```

Run from the repository root (default `--root` resolves to the repo root when
the script lives in `tools/`). All are read-only; C-2 additionally performs
local read-only git resolution of declared SHAs to tree ids. Their code lives
in `tools/` — never copy their implementation into `.agents/`; this file only
tells you when and how to use them and what the signals mean.
