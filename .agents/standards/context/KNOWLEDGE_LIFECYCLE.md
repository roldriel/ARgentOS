# Knowledge Lifecycle Standard

## Purpose

Define the minimum lifecycle that makes knowledge reusable, revalidable and
able to learn from execution: three knowledge types (`snapshot`, `claim`,
`lesson`), freshness evaluated per claim with resolvable provenance, an
explicit execution → invalidation transition (`invalidated_facts` in
`EXECUTION_SUMMARY.md`) and pipeline-scoped revalidation. This standard does
not design a full Knowledge Base (indexes, search, per-claim trust).

## Knowledge types

| Type | Definition | Freshness basis |
|---|---|---|
| `snapshot` | A discovery entry, point-in-time, with TTL and hashes (contract `KB_DISCOVERY_ENTRY.md`). | Entry TTL + hashes. |
| `claim` | A unit of knowledge inside an entry; the object of freshness and invalidation. | TTL per claim (by default inherited from the owning entry's scope) + resolvable provenance. |
| `lesson` | A claim produced by a session's closing feedback, with its own provenance (`session_id`, `protocol_version`, evidence reference). | Same as `claim`; provenance is the session artifact reference. |

Every knowledge-bearing artifact carries a type tag (`kind`). Snapshot,
current knowledge and historical knowledge are never mixed without the tag.

## Observation → knowledge transition

An observation becomes knowledge when all of the following hold:

1. It is produced by a worker with registered provenance
   (`source_files`/`source_sessions`).
2. It passes the discovery pipeline validation (`DISCOVERY_VALIDATE`, gate
   `D01`) or, for lessons, the session closing feedback with its evidence
   reference.
3. Its claim is fresh and its provenance resolves.

## Freshness per claim

A claim is reusable when:

- it is fresh: the per-claim TTL has not expired (by default the TTL of the
  owning entry, per its discovery scope); and
- its provenance resolves: `source_files`/`source_sessions` exist at
  consumption time.

A claim that is expired or whose provenance does not resolve is never reused,
recommended or consumed (KN-005). The owning entry is then marked stale and
revalidated through the pipeline before any further consumption.

## Invalidation

Invalidation is separated into three distinct domains that are not
interchangeable:

1. **Semantic invalidation (correctness).** Occurs exclusively by identity
   change: a change of `content_identity` or of `semantic_version`. A namespace
   inconsistency is expressed as a difference or invalidity of the
   corresponding identity, not as an independent category. TTL/freshness
   expiration and physical deletion are never correctness mechanisms.
2. **Freshness expiration (lifecycle / reuse eligibility).** TTL expiry or
   unresolvable provenance marks a claim as not reusable until the required
   revalidation succeeds (KN-005); stale does not imply semantically invalid.
3. **Physical deletion (storage).** Garbage collection or manual deletion
   affects availability, not the semantic identity of the knowledge it
   represented.

The operational triggers that mark a claim or snapshot as not reusable remain:
TTL expiry, hash change (configuration, code sample, environment), user
request, executor inconsistency report, and **post-execution invalidation**
(the execution declares `invalidated_facts` in `EXECUTION_SUMMARY.md` when it
changed discovered facts).

No execution may modify the knowledge base without passing through this
transition (`invalidated_facts` → pipeline revalidation) (KN-004, KN-006).

## Revalidation

Entries are updated only through the discovery pipeline (KN-006). Revalidation
triggered by `invalidated_facts` is scoped per affected entry: the pipeline
re-runs the scope that owns the entry (`env`, `stack`, `patterns`, `business`),
never a full rediscovery by default. A detected need does not imply invocation:
the discovery consent gate of `DISCOVERY_STATE_MACHINE.md` (Invocation
Conditions) still applies.

## Historical vs current knowledge

- **Historical knowledge**: past snapshots and lessons, kept as trace.
- **Current knowledge**: fresh claims with resolvable provenance, eligible for
  reuse and recommendation.

The distinction is declared through the `kind` tag; nothing is reclassified
retroactively.

## TTL changes require measurement

TTL values are a tradeoff: a short TTL increases rediscovery cost, a long TTL
increases staleness risk. Before changing any TTL, measure the rediscovery cost
(time, tokens, entries rewritten) and keep the measurement with the change.
Without measurement, the configured values in `.agents/features.toml` remain.

## Invariants

```text
KN-001:
Every discovery entry is a snapshot with TTL and hashes.

KN-002:
Every lesson has session_id, protocol_version and an evidence reference.

KN-003:
A fresh claim requires resolvable provenance.

KN-004:
Every execution that changes discovered facts declares invalidated_facts.

KN-005:
An expired claim or one without resolvable provenance is not reusable.

KN-006:
Knowledge-base entries are updated only through the discovery pipeline.
```

## Related documents

- `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md` — snapshot
  entry contract and claim semantics.
- `.agents/orchestrators/core/contracts/KB_RECOMMENDATION.md` — recommendations
  with `kind` and `path`.
- `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md` —
  `invalidated_facts` declaration.
- `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` —
  invocation conditions, freshness rule and scoped revalidation.
- `.agents/standards/context/KNOWLEDGE_CURATION.md` — inclusion rules and
  `curation_status` lifecycle.
