+++
schema_version = "1.0.0"
artifact = "EVIDENCE_SET.md"
phase = "n/a"
produced_by = "architecture_evolver"
enforcement = "documented"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: architecture
artifact: EVIDENCE_SET.md
lifecycle: architecture
produced_by: [architecture:EVIDENCE_INGESTION]
consumed_by: [architecture:PROJECT_ANALYSIS]
---

# Contract: Evidence Set

## Purpose

An Evidence Set is the immutable, per-execution input of Project Analysis
(`EVIDENCE-<n>`). It enumerates, by reference, the Evidence Snapshots that the
execution consumes; it never contains snapshot content.

## Semantics

- The set is an index of references: for each session, the ID of the snapshot
  that represents its analyzed state in that execution.
- In an incremental execution, the set references the existing snapshots of
  unchanged sessions and the new snapshots of modified sessions; content is
  never recreated.
- Lifecycle: OPEN (during ingestion) → SEALED (the execution fixes its input;
  immutable) → SUPERSEDED (a later execution seals a new set). Sealed sets are
  never rewritten.
- The sealed set is the input of Project Analysis and is recorded in the
  evolution manifest as `base_evidence_set`.

## Reproducibility

Because the set references immutable snapshots that capture the exact
fingerprint and derived evidence of what was observed, any execution can
reconstruct its analyzed input without re-reading the source.
