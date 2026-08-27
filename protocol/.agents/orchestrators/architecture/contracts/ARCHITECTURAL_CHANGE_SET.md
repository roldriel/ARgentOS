+++
schema_version = "1.0.0"
artifact = "ARCHITECTURAL_CHANGE_SET.md"
phase = "n/a"
produced_by = "architecture_evolver"
enforcement = "documented"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: architecture
artifact: ARCHITECTURAL_CHANGE_SET.md
lifecycle: architecture
produced_by: [architecture:CHANGE_SET]
consumed_by: []
---

# Contract: Architecture Change Set

## Purpose

The Architecture Change Set is the reviewable output of one evolution
execution. It records what changed and why, with traceability from evidence to
the proposed change.

## Required sections

1. `## Base` — architecture model pointer and base evidence set.
2. `## Trigger` — projects and sessions included.
3. `## Evidence` — list of claim_ids with evidence class.
4. `## Findings` — findings with their change kind.
5. `## Problems` — problems with their status transition.
6. `## Dependencies` — dependencies with their change kind.
7. `## Decisions` — decisions with their status transition.
8. `## RFC Impact` — affected and unaffected RFCs.
9. `## RFC Changes` — summary of each RFC amendment.
10. `## Change Rationale` — the traceable chain
    Evidence → Finding → Problem → Decision → Proposed Change, explaining why
    the evidence justifies the proposed change. Not a free opinion: every link
    cites the corresponding IDs.
11. `## Change Kinds` — NEW, MODIFIED, CONFIRMED, INVALIDATED, SUPERSEDED,
    UNAFFECTED.
12. `## Confidence` — HIGH | MEDIUM | LOW.
13. `## Human Gate` — LOW (automatic) | MEDIUM (review) | HIGH (approval).
14. `## Result` — CHANGE | NO_CHANGE.

## Semantics

- Generated does not imply approved: the change set is a proposal; approval
  lives in the governance gates and application in a later execution plan.
- NO_CHANGE is a first-class result: it still lists the examined evidence and
  findings.
- Every execution produces exactly one change set.
