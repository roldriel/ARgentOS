# Theoretical Execution — DEV Operational Policy (Plans 175, 176)

Operational procedure for **Theoretical Execution (TE)** in this repository: the
complete DEV capability, not only its first increment. TE evaluates a committed
Implementation Plan without executing it, without writing the repository and
without producing factual evidence.

Normative depth: RFC-75 governs the Change Lifecycle, ADR-16 the authority
classes and RFC-56 the payload authorization path. This policy **conducts** a
read-only analysis; it does not extend the lifecycle, create an authority, add a
gate, or define a Plan/RFC status. The implementation lives in
`runtime/theoretical/`. Design and acceptance criteria: Plan 175 (v1) and Plan
176 (complete scope); the scope reconstruction and the gap matrix are recorded in
`docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md`.

## 1. What TE is and is not

```text
THEORETICAL EXECUTION = a declared, non-mutative evaluation of a committed
                        proposal against a resolvable base state, through a
                        declared overlay whose unexecuted content is unknown.

TE ≠ real execution        TE ≠ verification       TE ≠ authorization
TE ≠ factual evidence      TE ≠ a test runner      TE ≠ a second lifecycle
TE ≠ an ExecutionHost      TE ≠ a persistent store TE ≠ an orchestrator
TE ≠ discovery/audit       TE ≠ post-execution     TE ≠ a gate
```

The result can only say `CONVERGED`, `OPEN_FINDINGS`, `REQUIRES_HUMAN`, `GAP`,
`NO_PROGRESS` or `RESOURCE_LIMIT`. It never says `PASS`, `VALID`, `VERIFIED`,
`EXECUTED`, `COMMITTED` or `RELEASED`.

TE is **complete** as a DEV capability in this sense: it reads a committed
proposal from a base commit, enumerates every declared item, records CH-1…CH-9,
accepts a producer attestation for the semantic dimensions, derives the status
mechanically, and bridges every non-evaluable claim to a verification
obligation. It is not a planner, an execution engine or a governance mechanism;
§14 states what it excludes and why.

## 2. Unit, inputs and outputs

- **Unit:** one committed revision of a Plan (`docs/plans/NN-*.md`). A change
  without a Plan (a Class C direct commit, for example) declares its proposal in
  the commit message, not in a proposal artifact TE can traverse; TE does not
  evaluate it.
- **Inputs:** factual base commit/tree; proposal path/blob/status; check-set;
  tool version; optionally a previous result (for no-progress) and a revision
  ceiling.
- **Output:** a `TE_RESULT` value (JSON on stdout, schema 2). TE never writes it;
  the caller decides where to keep it (§11).

## 3. Declared overlay and determinism

```text
DeclaredOverlay(base, declared_paths, effects, content_policy="DECLARED_UNKNOWN")
```

- a declared path is `DECLARED_UNKNOWN` in content and existence;
- an undeclared path is answered from the **base commit**, never from the
  working tree and never from the index;
- no patch, no virtual filesystem, no path→content for declared paths.

`declared_paths` is the set of `## Entregables`. The editable
`## Delegación agentiva` Scope is a different set: it may include the Plan itself
as a governance record. Editable is not the same as measured.

**Determinism boundary (schema 2).** Every check, and therefore the whole
`checks[]` record, is a function of the base commit: citations, artifact statuses
and the scope identity of a declared Validation Anchor are read from the base
tree. A dirty working tree or a staged change cannot alter a check signal. Two
runs over the same `InputIdentity` produce the same check record.

## 4. Identity and provenance

```text
FactualContentIdentity   = {commit, tree}
ProjectedContentIdentity = {kind:"declared_overlay", base, paths, effects, content:"unknown"}
InputIdentity            = {factual, projected, tool_version, check_set}
RunIdentity (te_id)      = {input_identity, producer, created_at, nonce}
```

`InputIdentity` governs staleness and is deterministic. `te_id` labels one run and
is never a staleness input; its nonce is derived from the declared content
(inputs, timestamp, producer and plan), so an interrupted skeleton is
recomputable. There is no `ResultContentIdentity`: semantic findings depend on the
producer, and two runs over the same inputs may legitimately differ. `producer`
is declared, not verified.

`tool_version = 2` and the check-set is versioned per check (`CH-3` and `CH-7`
are version 2; `CH-9` is new). A result produced under a different tool version or
check-set is `INCOMPARABLE`, never `fresh`.

## 5. The five dimensions

| Dimension | Executor | Required record |
|---|---|---|
| `completeness` | producer | `capability`, non-empty `probed`, claims/findings |
| `consistency` | producer | `capability`, non-empty `probed`, findings |
| `adversarial` | producer | `capability`, non-empty `probed`, claims/findings |
| `authority` | engine + producer | `computed=true`, evidence refs, `probed`, escalations |
| `verification` | engine | `computed=true`, obligations for every non-evaluable claim |

The engine **never** marks a producer dimension `PERFORMED`. A dimension is
`PERFORMED` only when its executor's record is complete. `PENDING` blocks
`CONVERGED`.

The producer is the agent or human who invokes TE. TE does not invoke a model,
a provider or the producer. There is no skill runtime: the producer may read the
capability instructions under `protocol/.agents/skills/` as guidance, never as
rules for this workspace.

## 6. Producer workflow

```bash
python -m runtime.theoretical --plan N --base HEAD --emit > /tmp/te-skeleton.json
# the producer performs completeness/consistency/adversarial and fills the
# claims, findings, dimensions and provenance in the JSON
python -m runtime.theoretical --validate /tmp/te-skeleton.json
```

`--emit` marks the producer dimensions `PENDING`, computes the engine ones and
records `checks[]`. `--validate` recomputes everything the engine owns: the
proposal enumeration, the identity, the check record, the required findings and
obligations, and the `status`; the declared status must match. On a mismatch it
prints the problems and the derived status and exits 1; update the file and rerun.
The producer must not edit the engine's computed facts to make a status pass.

`--validate` also prints `computed_fingerprint`: the value the producer must copy
into `no_progress.fingerprint` of the *next* result to declare no-progress (§8).

## 7. Deterministic checks

CH-1 class vs payload paths · CH-2 deliverable outside Scope · CH-3
broken/outdated citation (resolved against the base) · CH-4 write to a closed
artifact · CH-5 undeclared payload obligations · CH-6 criterion without
verification · CH-7 declared anchor identity not recomposable (delta recomputed
from the base commit) · CH-8 proposal not committed/base unreadable · CH-9
declaration integrity.

CH-3 special rule: a citation to a path this proposal declares is `GAP` plus a
verification obligation (its content is unknown); an absent undeclared path is
`ANOMALY`; a `Superseded` target is `BOUNDARY` plus an obligation.

CH-9 special rule: a declared deliverable with no resolvable repository-relative
path is `GAP` plus an obligation; a path that escapes the repository (or is not
relative) is `ANOMALY`; an effect class outside the closed DEV vocabulary
(`network`, `remote_git`, `install`, `destructive`, `write_outside_project`) is
`ANOMALY`. The closed vocabulary is read from the existing DEV checker, never
redefined here.

## 8. Result, status and no-progress

A finding uses the repository vocabulary (`ANOMALY`, `BOUNDARY`, `GAP`) and a
disposition (`OPEN`, `ESCALATED`, `RESIDUAL`). `RESIDUAL` requires `accepted_by`
resolving to a committed `path:section`. Corrections are always `applied: false`.
A `PREDICTION` claim is always `NOT_EVALUABLE` and carries an obligation; it is
never `CHECKED`.

`checks[]` is the engine-owned record of every check (including `VALID` and
`N/A`). The producer may not add, remove, reorder or reword a check; every check
that is not `VALID`/`N/A` must survive as a finding, and every engine obligation
must survive as a verification obligation. This is what makes a dropped finding —
a false convergence — invalid instead of invisible.

`status` is derived by `runtime/theoretical/result.py`:

```text
CONVERGED
  > RESOURCE_LIMIT
  > NO_PROGRESS
  > GAP
  > REQUIRES_HUMAN
  > OPEN_FINDINGS
```

`CONVERGED` means: no open/escalated material finding, no unchecked claim, the
five dimensions performed, every non-evaluable claim with an obligation, the
check record recomposed and the limits declared. It does **not** mean correct,
verified, safe or ready for release.

**No-progress** is mechanical, not declarative. The fingerprint is the canonical
JSON of the items, the check record and the material findings (residual findings
excluded). The declared `status` does **not** participate: the status is the
output of the comparison, so including it would make `NO_PROGRESS` unreachable.
A result may carry `previous_fingerprint` and `previous_te_id` **together**; the
id must equal `input.previous_te_id`; the fingerprint must be the previous
result's. `--validate` recomputes the current fingerprint and rejects a
declaration that does not match it. `CONVERGED` always outranks `NO_PROGRESS`.

## 9. Authority

| TE may | TE escalates |
|---|---|
| Observe, analyse, detect, simulate | Scope |
| Propose corrections | RFC-56 class / Change Level |
| Derive obligations | Normative contradiction |
| Classify escalations | RFC/ADR/Protocol/payload |
| Recommend and stop | Irreversible / reserved decisions |

TE does not create pending decisions; if one must persist, the owning artifact
records it (PC-1). TE does not resolve findings, apply corrections, authorize,
commit, close, promote or release.

## 10. Verification bridge

```text
claim / prediction → verification obligation → real mechanism → factual evidence
```

Candidates: `structural_checker`, `unit_test`, `integration_test`,
`dogfood_test`, `runtime_check`, `manual_review`, `git_evidence`,
`declared_environmental_gap`. `falsified_if` refutes a prediction while its
premises hold; `depends_on` names the assumptions. If a premise is invalidated,
the obligation is `NOT_APPLICABLE`, not `FAILED`. TE never satisfies an
obligation; the obligation is incorporated into the Plan (or the record that
cites it) in the next revision, and its evaluation belongs to its owner.

## 11. CLI, persistence and recovery

```text
--emit               print the producer skeleton (exit 0; 2 unreadable/not committed)
--validate FILE      validate, recompute and derive status (0 valid; 1 invalid; 2 unreadable)
--stale FILE         fresh/stale/incomparable/gap (0/1/1/2)
--compare PREV CUR   structural differences (0 same/no divergence; 1 divergence; 2 input changed)
```

The CLI never writes files, uses no shell, network, model or credentials. TE has
no store: the result is ephemeral unless the caller keeps it. **Persistence is
owned by the consumer**, never by TE: a governance artifact that cites a TE result
persists it in itself (inline `TE_RESULT` or a Working design record written by
the Change), and a TE result cited as evidence without its artifact violates
`docs/INVARIANTS.md:INV-11 — Governance Record Persistence`. TE is not a
`.project` store and does not create one.

**Recovery is artifact-based, not conversational.** TE keeps no partial state: a
run is one pass, and interrupting it loses nothing that the base commit plus the
declared inputs do not determine. Recovery is re-execution from the same
`InputIdentity`; `--emit` is recomputable (the `te_id` nonce is content-derived)
and the producer reconciles its attestation against a fresh skeleton. A new
revision is a new commit and a new TE result; `--stale` decides whether an
existing result is still applicable to HEAD. There is no resume of a partial run
and no session memory involved.

## 12. Failure and recovery

| Case | Behaviour |
|---|---|
| Base missing/unreadable | `--emit` exit 2, structured error, no partial JSON |
| Proposal not committed | `GAP` (`PROPOSAL_NOT_IN_BASE`), exit 2 |
| Plan `Superseded` | `GAP` (`PROPOSAL_SUPERSEDED`), exit 2 |
| Declared content unknown | Normal: overlay `DECLARED_UNKNOWN`; CH-3 → GAP + obligation |
| Input stale | `--stale` exit 1; not applicable to HEAD |
| Input incomparable | `--stale` exit 1 (tool version or check-set differs) |
| Information GAP | `status=GAP`; the producer obtains the input |
| Incomplete attestation | `--validate` exit 1, dimension `PENDING` |
| Dropped check, finding or obligation | `--validate` exit 1 |
| Fingerprint not recomputable | `--validate` exit 1 |
| No-progress | `status=NO_PROGRESS` if a previous fingerprint is declared and matches |
| Resource limit | `status=RESOURCE_LIMIT`; it does not authorize |
| Invalid schema | exit 1 with deterministic problems |
| Git absent | `GAP` (environmental factor) |
| Plan without `premises(D)` | `GAP` finding + obligation; does not block `--emit`, blocks `CONVERGED` unless accepted as `RESIDUAL` |

## 13. Boundaries

TE is DEV-only. It does not import `ExecutionHost`, does not write
`protocol/.agents/`, does not create a second Change/findings/decisions system,
and does not authorize, commit, promote or release. A checker result is factual
evidence about the base, never authority; a TE result is theoretical and never
factual evidence.

## 14. Scope: what TE DEV includes, excludes and why

`FACT` — Plan 175 excluded these areas from **v1**; Plan 176 determined which of
them belong to the complete DEV capability. The classification is:

| Area | Class | Reason |
|---|---|---|
| Base-relative checks, check record, verified fingerprint, deterministic run label, declaration integrity | `REQUIRED` | Implemented by Plan 176: without them the record is not a function of its inputs and a finding can disappear. |
| Real execution of the Plan | `OUT_OF_SCOPE_PERMANENT` | TE would stop being theoretical; execution belongs to the host. |
| Post-execution as a TE input | `OUT_OF_SCOPE_PERMANENT` | Consuming real results as evidence is verification, owned by the Change Lifecycle (RFC-75 mechanisms 6 and 8). |
| Authorization, governance, promotion, release | `OUT_OF_SCOPE_PERMANENT` | Constitutive: `recommendation ≠ authorization`. |
| Own persistence, store, `.project` | `OWNED_BY_OTHER_COMPONENT` | The durable record belongs to the Change that cites the result (§11). |
| Own lifecycle, new gates/fases/states | `OUT_OF_SCOPE_PERMANENT` | A mandatory TE gate would be a governance decision this capability cannot take; TE stays invocable. |
| Embedded orchestrator / second orchestrator | `OUT_OF_SCOPE_PERMANENT` | The host exists; the boundary is the CLI (§15). |
| Discovery / audit as a TE input | `OWNED_BY_OTHER_COMPONENT` | A problem without a proposal has no proposal to traverse; pre-plan analysis belongs to the Change Lifecycle and `docs/working/audits/`. |
| Step-by-step hypothetical execution (operation simulation) | `OUT_OF_SCOPE_PERMANENT` | It would require an effect interpreter and mutable state: a second execution engine. Scenario coverage is recorded in `dimensions.adversarial.probed`. |
| Effect admission at execution time (SAE) | `OWNED_BY_OTHER_COMPONENT` | The frontier lives in the host/SAE policy; TE only reports an unrecognised class (CH-9). |
| `ResultContentIdentity` | `OUT_OF_SCOPE_PERMANENT` | Semantic findings depend on the producer; the identity would assert a reproducibility that does not exist. |
| `scenarios[]` | `OPTIONAL` | Covered by `dimensions.adversarial.probed`; a second record would not add verifiability. |
| RFC/ADR adapter (evaluating a non-Plan proposal) | `DEFERRED` | The DEV change proposal is the Plan; a non-Plan proposal model is not defined. |

## 15. Integration with DEV

TE is an **invocable capability**, not a phase, a gate, a lifecycle state or a
registry. The Change that needs a theoretical evaluation invokes the CLI, keeps
the result where it cites it, and records the obligations it derives. The
canonical battery is not extended with TE: the semantic dimensions are
producer-attested and cannot be a host-independent gate.

- **Host boundary:** `runtime/orchestrator/` does not import TE and TE does not
  import the host (enforced by `tests/test_theoretical_isolation.py`). A host that
  wants a theoretical evaluation invokes the CLI; it never embeds TE. There is no
  second orchestrator, worker or decision path.
- **Lifecycle boundary:** TE does not own findings, corrections, pending
  decisions or anchors. Its findings are per-run (`TF-nn`); durable findings
  belong to the artifact that owns them (`<artifact>:F-<n>`, LC-1).
- **Protocol boundary:** nothing here is promoted to `protocol/`. DEV experience
  is a candidate for a future Protocol adaptation, never normative by itself.
