+++
schema_version = "1.0.0"
artifact = "GLOSSARY.md"
phase = "n/a"
produced_by = "business_worker"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: GLOSSARY.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_BUSINESS]
consumed_by: [discovery:DISCOVERY_MERGE, core:GATHERING_CONTEXT]
---

# GLOSSARY Contract

## Purpose

Define the format of the `glossary.md` knowledge-base entry produced by the
`business_worker`. It records the domain terms of the project with their
definition and the source file evidencing each term.

## Location

`.project/knowledge/discovery/glossary.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Glossary`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `glossary`.
- `source_files`: the README, service code and tests that evidence the terms.

Provenance fields:

- `source_workers`: MUST include `"business_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the domain vocabulary.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **term_count**: 11
- **primary_source**: README.md
```

### `## Terms`

One bullet per term, with the definition and the evidence source:

```text
- **<term>**: <definition> (source: <file>)
```

## Constraints

- Every term MUST carry a source file evidencing it; terms without evidence
  are not allowed.
- The glossary is a vocabulary of the project domain, not of the protocol.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (terms traced to README/service code/tests):
  harness `D01-discovery-output` (discovery domain).
