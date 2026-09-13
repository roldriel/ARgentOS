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

### Governance (APPEND-ONLY)

| Field | Meaning |
|---|---|
| `decisions[]` | Append-only decision history. Each entry: `{decision, authority, evidence_ref, recorded_at}`. |
| `authorizations[]` | Append-only Change authorization history. Each entry: `{authorization, authority, evidence_ref, recorded_at}`. |
| `closure_decisions[]` | Append-only closure decision history. Each entry: `{closure, authority, evidence_ref, recorded_at}`. |

There is no mutable "current" field as source of truth. The current value of
each collection is **derived** (the latest applicable entry).

### Payload identity

| Field | Meaning |
|---|---|
| `previous_content_identity` | Content identity (hash) of the baseline the Change modifies. Set once. |
| `proposed_content_identity` | Content identity (hash) of the current proposal. Mutable; a new value is a revision of the same Change. |

Only identities/hashes are persisted, never the repository payload.

### References (APPEND-ONLY)

| Field | Meaning |
|---|---|
| `executions[]` | `execution_id` references to the executions that materialized the Change. |

The Task↔Change relation is derived through `executions[]` (no direct task
reference, no cardinality constraint).

### Derived (NOT STORED)

| Field | Meaning |
|---|---|
| `change_identity` | `SegmentIdentity` (RFC-71) over the identity inputs. |
| `governance_position` | Derived governance position of the Change. |
| `current decision` / `current authorization` / `current closure` | Derived latest entries of the corresponding collections. |

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
The Change governance position is a **derived** condition, distinct from the
artifact lifecycle state. No Change State Machine is introduced.

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

## Invariants

```text
CGA-001: change_identity derives only from {target, declaration, protocol_version, namespace}.
CGA-002: identity-bearing fields are immutable after creation.
CGA-003: governance collections are append-only; current values are derived, never stored.
CGA-004: Change authorization is distinct from RFC-66 effect authorization.
CGA-005: evidence does not become authority.
CGA-006: artifact lifecycle state is distinct from Change governance position.
CGA-007: execution history is referenced, not duplicated.
CGA-008: Change Closed is a human closure decision (v1), distinct from release.
CGA-009: reflexive target is representable; bootstrap is deferred.
```

## Invalid states

Derived from the approved decisions (RFC-76):

- Modifying an identity-bearing input after creation.
- Overwriting governance history (a non-append mutation).
- Using RFC-66 effect authorization as Change authorization.
- Treating closure as Artifact validation.
- Treating closure as release.
- Changing `declaration` without creating a new Change.

No invalid states are defined from deferred mechanisms.

## Completion criteria

The artifact is valid when it declares `target`, `declaration`,
`protocol_version` and `namespace`; its governance collections are append-only
entries with `authority` and `evidence_ref`; its payload identity fields are
content identities; and its identity is derivable per RFC-71.
