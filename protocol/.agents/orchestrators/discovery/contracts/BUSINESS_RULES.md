+++
artifact = "BUSINESS_RULES.md"
phase = "n/a"
produced_by = "business_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: BUSINESS_RULES.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_BUSINESS]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# BUSINESS_RULES Contract

## Purpose

Define the format of the `business_rules.md` knowledge-base entry produced by
the `business_worker`. It records the business rules of the project detected
from the README, service code and tests.

## Location

`.project/knowledge/discovery/business_rules.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Business Rules`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `business_rules`.
- `source_files`: the README, service code and tests that evidence the rules.

Provenance fields:

- `source_workers`: MUST include `"business_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the business domain.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **rule_count**: 9
- **source_docs**: README.md
```

### `## Rules`

One bullet per rule, with the evidence source:

```text
- **<rule name>**: <statement> (source: <file>)
```

## Constraints

- Every rule must trace to a real source file or session artifact; never
  invent business rules.
- Qualitative claims are reserved for `## Summary`; the rules themselves are
  deterministic statements with evidence.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (rules traced to README/service code/tests):
  harness `D01-discovery-output` (discovery domain).
