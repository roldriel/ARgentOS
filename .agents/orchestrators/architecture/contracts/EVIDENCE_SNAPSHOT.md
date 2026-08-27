+++
schema_version = "1.0.0"
artifact = "EVIDENCE_SNAPSHOT.md"
phase = "n/a"
produced_by = "architecture_evolver"
enforcement = "documented"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: architecture
artifact: EVIDENCE_SNAPSHOT.md
lifecycle: architecture
produced_by: [architecture:EVIDENCE_INGESTION]
consumed_by: [architecture:PROJECT_ANALYSIS]
---

# Contract: Evidence Snapshot

## Purpose

An Evidence Snapshot is the immutable representation of what one evolution
execution observed about one session. It is the unit of Derived Evidence: the
external `.project/` may change, the snapshot never does.

## Identity and sealing

- Identity: `E-<session>-v<n>`, monotonically increasing per session.
- Sealed exactly once per (session, fingerprint, analysis version).
- Created only when the session fingerprint differs from the last analyzed
  state or the session is analyzed for the first time.

## Contents

- The session fingerprint at analysis time (content hash of the declared source
  artifacts).
- Evidence blocks with class, claim_id and ref, following the protocol evidence
  classes.
- The cited excerpts actually consumed by the analysis.
- References to the source artifacts (locator + content hash).

## Semantics

A sealed snapshot is never modified. If the session changes later, a new
snapshot is sealed and the previous one becomes SUPERSEDED while remaining
immutable and referenced. Replacing the import under
`sessions/<project-key>/.project/` does not rewrite snapshots.
