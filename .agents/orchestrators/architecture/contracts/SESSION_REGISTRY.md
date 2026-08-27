+++
schema_version = "1.0.0"
artifact = "SESSION_REGISTRY.md"
phase = "n/a"
produced_by = "architecture_evolver"
enforcement = "documented"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: architecture
artifact: SESSION_REGISTRY.md
lifecycle: architecture
produced_by: [architecture:EVIDENCE_INGESTION]
consumed_by: [architecture:PROJECT_ANALYSIS, architecture:CROSS_PROJECT_CORRELATION]
---

# Contract: Session Registry

## Purpose

The Session Registry is the current-state projection of the sessions known to
the Architecture Evolution workflow. It records which state of each session was
analyzed and which evidence snapshot represents that state.

## Fields

- **Session ID** — the declared session identity (session_id in the session
  artifacts); never a file name or path.
- **Project ID** — the owning project.
- **Source** — locator relative to the import workspace + source type.
- **First Seen / Last Seen** — UTC timestamps.
- **Fingerprint** — content hash of the analyzed source artifacts.
- **Analysis Status** — `NEW | ANALYZED | SUPERSEDED | REMOVED | INVALID`.
- **Evidence Status** — state of the derived evidence of the session.
- **Workflow Execution** — AE id that analyzed the session.
- **Analysis Version** — protocol version + analysis contract version.
- **Evidence Snapshot** — ID of the snapshot that represents the analyzed
  state (`E-<session>-v<n>`).

## Detection

Changes are detected by content fingerprint, never by file name or mtime:

- **NEW** — Session ID absent from the registry: ingest and analyze.
- **UNCHANGED** — fingerprint and analysis version current: skip, update Last
  Seen only.
- **MODIFIED** — fingerprint differs: seal a new snapshot, mark the previous
  one SUPERSEDED and re-analyze.
- **REMOVED** — source absent: mark REMOVED; the last snapshot remains
  immutable; provenance becomes unresolved.
- **MOVED** — fingerprint equal, locator different: update Source.
- **INVALID** — no declared identity, unreadable or conflicting IDs: exclude
  with a recorded reason.

## Semantics

The registry is a mutable projection; its history lives in git and in the
immutable execution artifacts. The Evidence Snapshot pointer identifies the
analyzed state of the session; updating the import never rewrites sealed
snapshots.
