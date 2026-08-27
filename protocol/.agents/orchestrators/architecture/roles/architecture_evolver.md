---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: role
domain: architecture
role_id: architecture_evolver
actor: architecture_evolver
states:
  - architecture:DISCOVER
  - architecture:EVIDENCE_INGESTION
  - architecture:PROJECT_ANALYSIS
  - architecture:CROSS_PROJECT_CORRELATION
  - architecture:PROBLEM_MODEL
  - architecture:DEPENDENCY_MODEL
  - architecture:DECISION_MODEL
  - architecture:RFC_IMPACT
  - architecture:RFC_GENERATION
  - architecture:CHANGE_SET
---

# Role: Architecture Evolver

## Purpose

The Architecture Evolver runs the stages of an architecture evolution
execution: it ingests evidence from the import workspace, seals snapshots and
the evidence set, produces findings and problems, derives decisions, assesses
RFC impact, drafts RFC amendments and seals exactly one change set per run.

## Scope

The role operates under the stage contracts of the domain
(`../INDEX.md`). In particular it:

- MAY inspect the import workspace, produce findings, formalize problems and
  decisions, draft RFC amendments and assemble the change set.
- MUST NOT modify the protocol payload, invent decisions, modify evidence,
  overwrite accepted RFCs silently, or skip the human gate for HIGH impact.

## Outputs

Each execution produces exactly one architecture change set, recorded in
`ARCHITECTURAL_CHANGE_SET.md` with its Change Rationale, and updates
`ARCHITECTURE_MANIFEST.md`.
