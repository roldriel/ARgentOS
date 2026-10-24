# Theoretical Execution — DEV Operational Policy (Plan 175)

Operational procedure for **Theoretical Execution (TE) v1** in this repository.
TE evaluates a committed Implementation Plan without executing it, without
writing the repository and without producing factual evidence.

Normative depth: RFC-75 governs the Change Lifecycle, ADR-16 the authority
classes and RFC-56 the payload authorization path. This policy **conducts** a
read-only analysis; it does not extend the lifecycle, create an authority, add a
gate, or define a Plan/RFC status. The implementation lives in
`runtime/theoretical/`; the authoritative design and acceptance criteria live in
`docs/plans/175-theoretical-execution-dev-v1.md`.

## 1. What TE is and is not

```text
THEORETICAL EXECUTION = a declared, non-mutative evaluation of a committed
                        proposal against a resolvable base state, through a
                        declared overlay whose unexecuted content is unknown.

TE ≠ real execution        TE ≠ verification       TE ≠ authorization
TE ≠ factual evidence      TE ≠ a test runner      TE ≠ a second lifecycle
TE ≠ an ExecutionHost      TE ≠ a persistent store TE ≠ an orchestrator
```

The result can only say `CONVERGED`, `OPEN_FINDINGS`, `REQUIRES_HUMAN`, `GAP`,
`NO_PROGRESS` or `RESOURCE_LIMIT`. It never says `PASS`, `VALID`, `VERIFIED`,
`EXECUTED`, `COMMITTED` or `RELEASED`.

## 2. Unit, inputs and outputs

- **Unit:** one committed revision of a Plan (`docs/plans/NN-*.md`).
- **Inputs:** factual base commit/tree; proposal path/blob/status; check-set;
  tool version; optionally a previous result and a revision ceiling.
- **Output:** a `TE_RESULT` value (JSON on stdout). TE never writes it; the
  caller decides where to keep it.

## 3. Declared overlay

```text
DeclaredOverlay(base, declared_paths, effects, content_policy="DECLARED_UNKNOWN")
```

- a declared path is `DECLARED_UNKNOWN` in content and existence;
- an undeclared path is answered from the **base commit**, never from the
  working tree;
- no patch, no virtual filesystem, no path→content for declared paths.

`declared_paths` is the set of `## Entregables`. The editable `## Delegación
agentiva` Scope is a different set: it may include the Plan itself as a
governance record. Editable is not the same as measured.

## 4. Identity and provenance

```text
FactualContentIdentity   = {commit, tree}
ProjectedContentIdentity = {kind:"declared_overlay", base, paths, effects, content:"unknown"}
InputIdentity            = {factual, projected, tool_version, check_set}
RunIdentity (te_id)      = {input_identity, producer, created_at, nonce}
```

`InputIdentity` governs staleness and is deterministic. `te_id` labels one run
and is never a staleness input. There is no `ResultContentIdentity`: semantic
findings depend on the producer, and two runs over the same inputs may
legitimately differ. `producer` is declared, not verified.

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

`--emit` marks the producer dimensions `PENDING` and computes the engine ones.
`--validate` recomputes the `status`; the declared status must match. On a
mismatch, it prints the derived status and exits 1; update the file and rerun.
The producer must not edit the engine's computed facts to make a status pass.

## 7. Deterministic checks

CH-1 class vs payload paths · CH-2 deliverable outside Scope · CH-3
broken/outdated citation · CH-4 write to a closed artifact · CH-5 undeclared
payload obligations · CH-6 criterion without verification · CH-7 declared
identity not recomposable · CH-8 proposal not committed/base unreadable.

CH-3 special rule: a citation to a path this proposal declares is `GAP` plus a
verification obligation (its content is unknown); an absent undeclared path is
`ANOMALY`; a `Superseded` target is `BOUNDARY` plus an obligation.

## 8. Result and status

A finding uses the repository vocabulary (`ANOMALY`, `BOUNDARY`, `GAP`) and a
disposition (`OPEN`, `ESCALATED`, `RESIDUAL`). `RESIDUAL` requires `accepted_by`
resolving to a committed `path:section`. Corrections are always
`applied: false`. A `PREDICTION` claim is always `NOT_EVALUABLE` and carries an
obligation; it is never `CHECKED`.

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
five dimensions performed, every non-evaluable claim with an obligation, and the
limits declared. It does **not** mean correct, verified, safe or ready for
release.

## 9. Authority

TE may observe, analyse, detect, propose, derive obligations, classify
escalations, recommend and stop. It must escalate scope, RFC-56 class/Level,
normative contradictions, RFC/ADR/Protocol changes, genuinely equivalent
alternatives, irreversible decisions and anything reserved to the human. It
does not create pending decisions; if one must persist, the owning artifact
records it (PC-1).

## 10. Verification bridge

```text
claim / prediction → verification obligation → real mechanism → factual evidence
```

Candidates: `structural_checker`, `unit_test`, `integration_test`,
`dogfood_test`, `runtime_check`, `manual_review`, `git_evidence`,
`declared_environmental_gap`. `falsified_if` refutes a prediction while its
premises hold; `depends_on` names the assumptions. If a premise is invalidated,
the obligation is `NOT_APPLICABLE`, not `FAILED`. TE never satisfies an
obligation.

## 11. CLI and persistence

```text
--emit               print the producer skeleton (exit 0; 2 unreadable/not committed)
--validate FILE      validate and derive status (0 valid; 1 invalid; 2 unreadable)
--stale FILE         fresh/stale/incomparable/gap (0/1/1/2)
--compare PREV CUR   structural differences (0 same/no divergence; 1 divergence; 2 input changed)
```

The CLI never writes files, uses no shell, network, model or credentials. TE
has no store: the result is ephemeral unless the caller keeps it. A durable
record, when a Change needs one, is a **Working design record** written by the
Change (for Plan 175: `docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md`),
never a `.project` store.

## 12. Failure and recovery

Missing base, missing/uncommitted proposal, `Superseded` proposal, unreadable
Git and incomplete attestations are `GAP`/exit 2 or validation errors; they are
never converted into positive evidence. Recovery is re-execution from the same
inputs; there is no resume of a partial run. A new revision is a new commit and
a new TE result.

## 13. Boundaries

TE is DEV-only. It does not import `ExecutionHost`, does not write
`protocol/.agents/`, does not create a second Change/findings/decisions system,
and does not authorize, commit, promote or release. A checker result is factual
evidence about the base, never authority; a TE result is theoretical and never
factual evidence.
