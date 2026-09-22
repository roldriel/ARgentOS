+++
schema_version = "1.0.0"
artifact = "CHANGE_GOVERNANCE.md"
phase = "n/a"
produced_by = "orchestrator"
enforcement = "documented"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: cross-cutting
artifact: CHANGE_GOVERNANCE.md
lifecycle: null
produced_by: [core:TASK_RECEIVED]
consumed_by: [core:TASK_RECEIVED, core:ANALYZING_TASK, core:PLANNING]
---

# Contract: Change Governance Artifact

## Purpose

The Change Governance Artifact is the durable, Protocol-native representation of
the governance state of **one Change** of the Protocol payload. It survives
across sessions and lets a future Orchestrator continue governing the same
Change without private knowledge of the originating session.

Its normative source is `docs/rfc/76-change-governance-artifact.md` (RFC-76).

## Implemented scope (MVP)

This contract distinguishes what the Change Lifecycle Protocol **implements** in
the MVP from what is **DEFERRED**. The distinction is normative for readers: a
deferred operation is not a capability of this protocol version and MUST NOT be
assumed to exist.

**Implemented (v1):**

- materialization of the Change Governance Artifact as a durable per-project
  category (`.project/changes/<change_identity>.md`);
- derivation of the Change identity (`SegmentIdentity`, RFC-71) from the four
  immutable identity inputs;
- persistence of the artifact, and its reconstruction by recomputing the identity
  from the identity inputs and reading the corresponding file;
- the **structure** of the governance collections as accumulated history
  (the artifact form admits no partial overwrite of one collection);
- recording of `decisions[]`, `authorizations[]` and `closure_decisions[]` as
  entries provided by the caller at materialization time;
- append-only governance history as a **structural** property of the artifact.

**DEFERRED (see `## Deferred semantics`):**

- the **append** operation (adding one governance fact to an existing artifact);
- the derivation of **current** (`current decision` / `current authorization` /
  `current closure` as the latest applicable entry);
- the derivation of **governance_position**.

**Operational limitation of the MVP.** The runtime provides **no append
operation**. Accumulating governance history beyond a single materialization is
performed by **complete re-materialization with the accumulated history** —
providing the whole history to the materialization call and rewriting the
artifact. That mechanism is **not append**: it does not add a fact to an existing
artifact in place, and it MUST NOT be described as append. Its consequence is
that intermediate states of the artifact are not preserved, because the same path
is rewritten. This limitation is a scope decision of the MVP, not an
implementation gap to be closed silently.

`enforcement = "documented"` in this contract's front matter means exactly this:
the contract text and its invariants are the normative reference; no runtime
gate, harness gate or validation gate enforces this artifact.

## Semantic identity

The Change Governance Artifact owns the governance state of one Change. It is
not a Task, an Execution Record, a Verification Report, an Evidence container, a
Knowledge entry, an Architecture Evolution artifact, a Release record, an
authority role, or a Change State Machine.

## Structure

### Identity (IMMUTABLE)

| Field | Meaning |
|---|---|
| `target` | Reference to the governed object (protocol file, contract, mechanism). |
| `declaration` | Initial identity-bearing declaration (target + stable scope intent). |
| `protocol_version` | Semantic version governing the Change's interpretation (at creation). |
| `namespace` | Isolation component of the derived identity. Value: **`project_identity`** (D-02; RFC-71 isolation, RFC-73 project segment). |

These four fields are the identity inputs. They are immutable after creation:
modifying any of them implies a different Change identity (RFC-76 I4).

### Canonical representation (D-03)

The identity inputs are canonicalized as four ordered lines, UTF-8:

```text
target=<target>
declaration=<declaration.strip()>
protocol_version=<semver>
namespace=project_identity
```

`declaration` is trimmed and otherwise left untouched (no internal
normalization); `target` is used verbatim (no Protocol-native target
normalization rule exists); references, metadata and governance state are
excluded. The content identity is `SHA-256(canonical)` (RFC-71); the Change
identity is the RFC-71 `SegmentIdentity` over it.

### Governance (APPEND-ONLY, structural)

| Field | Meaning |
|---|---|
| `decisions[]` | Decision history. Each entry: `{decision, authority, evidence_ref, recorded_at}`. |
| `authorizations[]` | Change authorization history. Each entry: `{authorization, authority, evidence_ref, recorded_at}`. |
| `closure_decisions[]` | Closure decision history. Each entry: `{closure, authority, evidence_ref, recorded_at}`. |

**Structural meaning only.** In the MVP, "append-only" describes the **form** of
the artifact: the three collections are accumulated history and the artifact form
admits no partial in-place overwrite of one collection. It does **not** describe
an available **operation**: the protocol provides **no append operation**, so a
governance fact cannot be added to an existing artifact in place. Adding history
beyond a single materialization is done by **complete re-materialization with the
accumulated history** (`## Implemented scope (MVP)`), which is not append.

There is no mutable "current" field as source of truth. The **derivation** of the
current value of each collection is **DEFERRED** in the MVP: no current value is
computed or stored (`## Deferred semantics`). Consequently a reader MUST NOT
assume that a `current decision`, `current authorization` or `current closure` is
available from this protocol version; deriving it is a judgement performed by the
reader over the accumulated history.

### Payload identity

| Field | Meaning |
|---|---|
| `previous_content_identity` | Content identity (hash) of the baseline the Change modifies. Set once. |
| `proposed_content_identity` | Content identity (hash) of the current proposal. Mutable; a new value is a revision of the same Change. |

Only identities/hashes are persisted, never the repository payload.

### References (accumulated history)

| Field | Meaning |
|---|---|
| `executions[]` | `execution_id` references to the executions that materialized the Change. |

The Task↔Change relation is derived through `executions[]` (no direct task
reference, no cardinality constraint). As with the governance collections, the
MVP provides no in-place append: references are provided as accumulated history
at materialization time (`## Implemented scope (MVP)`).

### Derived (NOT STORED)

| Field | Meaning | Status in the MVP |
|---|---|---|
| `change_identity` | `SegmentIdentity` (RFC-71) over the identity inputs. | **Available** — computed on materialization; recorded inside the artifact for readability, never as an independent source of truth. |
| `governance_position` | Governance position of the Change. | **DEFERRED** — not computed, not stored, not defined operationally. |
| `current decision` / `current authorization` / `current closure` | Latest entries of the corresponding collections. | **DEFERRED** — not derived by the protocol; a reader may judge them over the accumulated history. |

## Authorization boundary

Change authorization (`authorizations[]`) is semantically distinct from RFC-66
effect authorization (`effects`, `AUTHORIZATION.md`). RFC-66 is not redefined.
Modifying the Protocol payload is not an effect authorizable by the RFC-66
`effects` block.

## Closure

For v1, `Change Closed` is an explicit human closure decision recorded in
`closure_decisions[]`. No derived closure predicate is required (deferred).

`Change Closed` is distinct from: Artifact validated, Execution completed,
Verification passed, Change authorized, and Payload released.

## Revisions

- `declaration` is frozen (identity-bearing). Changing it is a **new Change**.
- Changing `proposed_content_identity` is a **revision** of the same Change.
- Supersession uses the RFC-63 Artifact Lifecycle (`draft → validated →
  superseded`); no Change-specific lifecycle states exist.

## Lifecycle relation

The artifact uses the RFC-63 Artifact Lifecycle (derived from gate records).
The Change governance position is a condition **distinct** from the artifact
lifecycle state; its **derivation is DEFERRED** in the MVP (CGA-010), so no
governance position is computed or stored. No Change State Machine is introduced.

## Persistence / retrieval

The Change Governance Artifact is a durable, per-project Protocol-native
category, materialized at `.project/changes/<change_identity>.md` (D-01). The
filename is derived from the Change Identity (filesystem-safe); the path is not
part of the identity. Retrieval is content-addressed and the locator is the
derived Change Identity (no registry, no global index, no identity service).

## Reflexivity

`target` MAY reference the protocol's own governance mechanism. Reflexive
bootstrap is deferred; no bootstrap exception, authority, state or gate is
introduced.

## Deferred semantics

The following remain explicitly deferred (RFC-76): closure predicate;
reflexive bootstrap; Task↔Change cardinality; GC semantics.

The following are **DEFERRED by the MVP scope decision H-3** (maintainer,
2026-09-13; RFC-76 `## Amendment Log`). They are not implemented, and no runtime,
field, endpoint, event, state or method exists for them:

- **append** — the operation of adding one governance fact to an existing
  artifact in place. Not implemented. History beyond a single materialization is
  accumulated by **complete re-materialization with the accumulated history**,
  which is not append (`## Implemented scope (MVP)`).
- **current** — the derivation of `current decision` / `current authorization` /
  `current closure` as the latest applicable entry. Not implemented; no current
  value is computed or stored.
- **governance_position** — the derivation of the Change's governance position.
  Not implemented, and not operationally defined.

Implementing any of these three requires a new decision and its own authorized
Plan; it is out of scope for the MVP and MUST NOT be inferred from this contract.

## Invariants

```text
CGA-001: change_identity derives only from {target, declaration, protocol_version, namespace}.
CGA-002: identity-bearing fields are immutable after creation.
CGA-003: governance collections are structurally append-only history; no current value is stored as an independent source of truth (derivation of current is deferred, see CGA-010).
CGA-004: Change authorization is distinct from RFC-66 effect authorization.
CGA-005: evidence does not become authority.
CGA-006: artifact lifecycle state is distinct from Change governance position.
CGA-007: execution history is referenced, not duplicated.
CGA-008: Change Closed is a human closure decision (v1), distinct from release.
CGA-009: reflexive target is representable; bootstrap is deferred.
CGA-010: the append operation and the derivation of current and governance_position are deferred; no implementation, field or gate exists for them in this protocol version.
```

## Invalid states

Derived from the approved decisions (RFC-76):

- Modifying an identity-bearing input after creation.
- Overwriting governance history (a non-append mutation).
- Using RFC-66 effect authorization as Change authorization.
- Treating closure as Artifact validation.
- Treating closure as release.
- Changing `declaration` without creating a new Change.

No invalid states are defined from deferred mechanisms. In particular, the
absence of an append operation is a **deferred capability**, not an invalid
state: re-materializing the artifact with the accumulated history is the
mechanism available in the MVP.

## Completion criteria

The artifact is valid when it declares `target`, `declaration`,
`protocol_version` and `namespace`; its governance collections are accumulated
history entries with `authority` and `evidence_ref`; its payload identity fields
are content identities; and its identity is derivable per RFC-71.

The artifact is **not** required to expose an append operation, a derived
`current` value or a `governance_position`: those are deferred (CGA-010) and
their absence is not a validity defect.
