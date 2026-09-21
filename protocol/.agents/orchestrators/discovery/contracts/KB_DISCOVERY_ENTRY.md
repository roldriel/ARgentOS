+++
schema_version = "2.0.0"
artifact = "KB_DISCOVERY_ENTRY.md"
phase = "n/a"
produced_by = ["environment_worker", "stack_worker", "framework_worker", "patterns_worker", "business_worker", "synthesis_worker"]
enforcement = "gated"
gated_by = ["D01"]
+++
schema_version = "2.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: KB_DISCOVERY_ENTRY.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_INIT, discovery:DISCOVERY_ENV, discovery:DISCOVERY_STACK, discovery:DISCOVERY_FRAMEWORK, discovery:DISCOVERY_PATTERNS, discovery:DISCOVERY_BUSINESS, discovery:DISCOVERY_MERGE]
consumed_by: [discovery:DISCOVERY_MERGE, core:GATHERING_CONTEXT]
---

# KB Discovery Entry Contract

## Purpose

Define the structure and requirements of a knowledge-base entry produced by the Discovery Orchestrator subsystem.

These entries live in `.project/knowledge/discovery/` and provide pre-processed project context for future agent sessions.

---

## Naming convention

Per-entry contracts are named after the entry type (e.g.
`ENVIRONMENT_DISCOVERY.md`, `DEVELOPMENT_PATTERNS.md`, `ARCHITECTURE.md`); the
runtime artifact they define is the lowercase KB file (e.g. `environment.md`,
`development_patterns.md`, `architecture.md`) under
`.project/knowledge/discovery/`. The contract filename is not the artifact
path: workflow `output_artifacts` and state machine "Required Output
Artifacts" use the KB file names.

---

# KB Discovery Entry

## Metadata

```toml
artifact = "KB_DISCOVERY_ENTRY.md"
kind = "snapshot"
title = "Stack"
generated_at = ""
updated_at = ""
tags = ["discovery", "stack"]
source_files = ["pyproject.toml"]
source_workers = ["stack_worker"]
source_sessions = ["session-68c54119"]
status = "active"
previous_versions = []
```

---

## Required Front Matter

Every discovery entry MUST include TOML front matter with:

- The block is delimited by **`+++`** on its own line, opening the file and
  closing the block. `+++` is the front-matter delimiter of a KB entry; the
  taxonomy metadata block of `.agents/` artifacts, delimited with `---`, is a
  different block and is not used in KB entries.
- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `kind`: must be `snapshot`. Every discovery entry is a snapshot:
  point-in-time knowledge with TTL and hashes (see
  `.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`).
- `title`: human-readable title of the entry.
- `generated_at`: ISO 8601 timestamp when the entry was generated.
- `tags`: list including `discovery` and the entry category.
- `source_files`: list of project files that contributed facts to this entry.

## Optional Front Matter (provenance)

Entries of the accumulative KB MAY also include:

- `updated_at`: ISO 8601 timestamp of the last update.
- `source_workers`: list of workers that produced or revalidated the entry.
- `source_sessions`: list of sessions that contributed facts to the entry.
- `status`: `active`, `stale` or `legacy`.
  - `active`: current knowledge.
  - `stale`: invalidated; kept as trace, not consumed as current.
  - `legacy`: inherited from a KB written **without provenance fields** and not
    yet revalidated by a worker. A `legacy` entry is treated as low-confidence
    until a worker revalidates it (it becomes `active`) or it is invalidated (it
    becomes `stale`); it is never deleted without a trace.
- `previous_versions`: list of references to previous versions of the entry (optional).

`source_files` admits two reserved values besides project paths:

- `"system_probe"`: the fact comes from probing the execution environment rather
  than from project files. It is a valid source **only for environment entries**.
- `"project_scan"`: the fact was established by **scanning the project tree** —
  an absence or a structural/tree fact — not by reading a project file. It is
  valid **only** for that class of claim: it does not substitute for a resolvable
  path when a file evidences the fact, and it is **not** valid in an environment
  entry (that class belongs to `"system_probe"`). Conversely, `"system_probe"`
  is not valid outside an environment entry.

Provenance applies per claim: every fact bullet of `## Discovered Facts` is a
claim whose reuse requires its `source_files`/`source_sessions` to resolve.

---

## Sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Reserved for LLM-synthesized qualitative content in Phase 2 (architecture, business rules, technical debt, known errors, project flow). Phase 1 entries contain a placeholder explaining that synthesis is pending.

### `## Discovered Facts`

Bullet list of deterministic facts extracted from project files. Each bullet should follow:

```text
- **<key>**: <value>
```

Each bullet is a **claim**: freshness is evaluated per claim (by default the
entry's TTL per its discovery scope, see `DISCOVERY_STATE_MACHINE.md` §TTL and
Cache) and its provenance must resolve (`source_files`/`source_sessions` exist
at consumption time). A claim may declare its own freshness/provenance only as
an explicit override; the entry itself remains `kind: snapshot`. A claim that
is expired or whose provenance does not resolve is not reusable and marks the
entry stale for pipeline revalidation (`.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`).

If no deterministic facts are available, the section should state:

```text
_No deterministic facts found for this category._
```

---

## Completion Criteria

The entry is valid when:

* Front matter contains all required fields.
* The `artifact` field equals `KB_DISCOVERY_ENTRY.md`.
* The `#` title matches the `title` front-matter value.
* The `## Discovered Facts` section is present.
