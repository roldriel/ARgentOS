+++
artifact = "EXECUTIVE_SUMMARY.md"
phase = "n/a"
produced_by = "synthesis_worker"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: EXECUTIVE_SUMMARY.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_MERGE]
consumed_by: [core:GATHERING_CONTEXT]
---

# EXECUTIVE_SUMMARY Contract

## Purpose

Define the format of the `executive_summary.md` knowledge-base entry produced by the `synthesis_worker`. It is the canonical read-first entry of the KB: the first file an agent session reads to orient itself in the project.

## Location

`.project/knowledge/discovery/executive_summary.md`

## Required sections

1. **First line: project shape** — the first line of the entry declares the `project_shape` (`library`, `cli`, `service`, `application`, `monorepo` or `unknown`), matching the `[knowledge_base]` field of the manifest. This tells the reader which other KB entries to expect.
2. `## Project Purpose` — what the project does, in 2-3 lines.
3. `## Stack in One Line` — the technology stack summarized in a single line.
4. `## Entry Point` — where execution (or import, for libraries) starts; details live in `entrypoint.md`.
5. `## Key Modules` — the top 5 modules with a one-line responsibility each.
6. `## Top Risks` — the top 3 risks, aligned with the `## Top Risks` section of `technical_debt.md`.
7. `## KB Status` — active and stale entries, and the timestamp of the last discovery run, taken from the manifest.

## Constraints

- The entry synthesizes other KB entries; it must not introduce facts not present in another KB entry.
- Provenance follows the base KB entry contract (`KB_DISCOVERY_ENTRY.md`): TOML front matter and `## Discovered Facts` are required; `source_files` aggregate the sources of the synthesized entries.
- Keep it short: this entry is optimized for a fast first read, not for completeness.
