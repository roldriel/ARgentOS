+++
schema_version = "1.0.0"
artifact = "PROJECT_REGISTRY.md"
phase = "n/a"
produced_by = "architecture_evolver"
enforcement = "documented"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: architecture
artifact: PROJECT_REGISTRY.md
lifecycle: architecture
produced_by: [architecture:EVIDENCE_INGESTION, architecture:CHANGE_SET]
consumed_by: [architecture:DISCOVER, architecture:EVIDENCE_INGESTION, architecture:PROJECT_ANALYSIS, architecture:CROSS_PROJECT_CORRELATION]
---

# Contract: Project Registry

## Purpose

The Project Registry is the current-state projection of the projects known to
the Architecture Evolution workflow: their stable identity, their physical
locator, their status and the evidence version they were last analyzed at.

## Fields

- **Project ID** — stable identity assigned by the workflow (`PRJ-0001`);
  never derived from the project name or path.
- **Project Name** — mutable human label.
- **Project Location** — last resolved locator; not identity; may go stale.
- **Source Type** — `external_workspace | evidence_import | snapshot`.
- **Status** — `REGISTERED | ACTIVE | MISSING | ARCHIVED | INVALID`.
- **First Seen / Last Seen** — UTC timestamps.
- **Evidence Version** — `EVIDENCE-<n>` of the last processed evidence set.
- **Last Analysis** — reference to the AE execution / change set that analyzed
  the project.
- **Content Fingerprint / Revision** — hash of the project evidence index.
- **Provenance** — mapping to the source (location + source type + access
  method).

## Identity and locator

Logical Source Identity is not the Physical Locator. In Phase 1 the workflow
consumes the imported copy under `sessions/<project-key>/.project/`; the
`<project-key>` is a local key of the import workspace, not the project
identity. Changing the locator (moving or renaming the import) updates the
Location field without creating a new project.

## Semantics

The registry is a mutable current-state projection: fields such as Last Seen,
Status, Location, Evidence Version and Last Analysis are updated by each
execution. Its history lives in git and in the immutable execution artifacts
(evidence snapshots, AE records, change sets); there is no separate event
store. Replacing or updating `sessions/<project-key>/.project/` does not modify
sealed evidence.
