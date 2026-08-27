+++
schema_version = "1.0.0"
artifact = "ARCHITECTURE_MANIFEST.md"
phase = "n/a"
produced_by = "architecture_evolver"
enforcement = "documented"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: architecture
artifact: ARCHITECTURE_MANIFEST.md
lifecycle: architecture
produced_by: [architecture:DISCOVER, architecture:CHANGE_SET]
consumed_by: [architecture:DISCOVER, architecture:EVIDENCE_INGESTION]
---

# Contract: Architecture Manifest

## Purpose

The Architecture Manifest is the current-state pointer of the Architecture
Evolution workflow: which change set was last sealed, which evidence set was
the base, which projects are known and where the models live.

## Fields

- **last_change_set** — ID of the last sealed change set.
- **base_evidence_set** — `EVIDENCE-<n>` used as the input base.
- **projects** — project keys known to the workflow.
- **models** — pointers (git refs) to the problem, dependency and decision
  models.
- **rfcs** — pointer to the RFC index version.

## Semantics

The manifest is a mutable projection updated by each execution. It does not
introduce a parallel versioning scheme for the architecture model: the protocol
versioning rules remain the only version source, and the history of the
manifest itself lives in git.
