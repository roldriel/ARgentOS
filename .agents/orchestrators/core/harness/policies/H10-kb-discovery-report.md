+++
trigger = "H10"
transition = "Before using KB discovery (optional)"
artifact = "KB_DISCOVERY_REPORT.md"
required_sections = [
  "Discovery Objective",
  "Recommended Entries",
  "Context Budget Recommendation",
  "Notes"
]
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H10
name: kb-discovery-report
state: core:GATHERING_CONTEXT
lifecycle: context
gates:
  - "core:GATHERING_CONTEXT -> core:CONTEXT_GATHERED"
artifact_validated: KB_DISCOVERY_REPORT.md
---

# Harness Policy H10: KB Discovery Report (optional)

## Trigger

Before using KB discovery (optional gate)

## Purpose

Structural validation of the discovery knowledge base. H10 verifies that the KB entries exist and are structurally conformant with their contracts. H10 does **not** verify ground truth (that `source_files` are real project paths, that examples are verifiable, or that `environment.md` is secret-free): that is the exclusive responsibility of `D01-discovery-output` (discovery domain).

## Input

- KB entries: `.project/knowledge/discovery/*.md`
- Manifest: `.project/knowledge/discovery/.discovery_manifest`
- Contracts:
  - `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`
  - `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md`
  - `.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md`
  - `.agents/orchestrators/discovery/contracts/DEVELOPMENT_PATTERNS.md`
  - `.agents/orchestrators/discovery/contracts/ENVIRONMENT_DISCOVERY.md`

## Decision Criteria

`PASS` when all of the following hold; `FAIL` otherwise:

- All expected KB entries exist and satisfy the base entry contract (`KB_DISCOVERY_ENTRY.md`).
- The TOML front-matter headers of the entries are valid.
- The required fields are present in every entry.
- The manifest is complete (all required sections of `DISCOVERY_MANIFEST.md` are present).
- Every pattern in `development_patterns.md` has `source_files`, `confidence` and an `example`.
- `environment.md` and `development_patterns.md` exist.

Explicitly out of scope (D01, not H10):

- Verifying that `source_files` are real paths in the project.
- Verifying that detected facts match real configuration files.
- Verifying that `environment.md` contains no secrets.

## Note

This trigger is optional in the current state machine. The Orchestrator may invoke it when the `knowledge_base` feature flag is enabled and stricter validation is desired.
