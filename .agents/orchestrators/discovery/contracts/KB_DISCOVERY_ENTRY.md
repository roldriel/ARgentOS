+++
artifact = "KB_DISCOVERY_ENTRY.md"
phase = "n/a"
produced_by = "project_discovery"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: KB_DISCOVERY_ENTRY.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_INIT]
consumed_by: [core:GATHERING_CONTEXT]
---

# KB Discovery Entry Contract

## Purpose

Define the structure and requirements of a knowledge-base entry produced by the project discovery module.

These entries live in `.project/knowledge/discovery/` and provide pre-processed project context for future agent sessions.

---

# KB Discovery Entry

## Metadata

```yaml
artifact: "KB_DISCOVERY_ENTRY.md"
title: "Stack"
generated_at: ""
tags:
  - "discovery"
  - "stack"
source_files:
  - "pyproject.toml"
```

---

## Required Front Matter

Every discovery entry MUST include TOML front matter with:

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title of the entry.
- `generated_at`: ISO 8601 timestamp when the entry was generated.
- `tags`: list including `discovery` and the entry category.
- `source_files`: list of project files that contributed facts to this entry.

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
