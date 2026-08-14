+++
artifact = "PROJECT_FLOW.md"
phase = "n/a"
produced_by = "business_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: PROJECT_FLOW.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_BUSINESS]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# PROJECT_FLOW Contract

## Purpose

Define the format of the `project_flow.md` knowledge-base entry produced by
the `business_worker`. It records the main business flows of the project:
triggers, steps and outcomes.

## Location

`.project/knowledge/discovery/project_flow.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Project Flow`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `project_flow`.
- `source_files`: the README, service code and tests that evidence the flows.

Provenance fields:

- `source_workers`: MUST include `"business_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the main flows.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **flow_count**: 4
- **main_flow**: user onboarding
```

### `## Flows`

One bullet per flow, with trigger, steps and outcome:

```text
- **<flow name>**: <trigger> → <steps> → <outcome> (source: <file>)
```

## Constraints

- Every flow must trace to a real source file or session artifact; never
  invent flows.
- Mermaid sequence diagrams are allowed as a supporting format but never
  replace the bullet description of each flow.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (flows traced to README/service code/tests):
  harness `D01-discovery-output` (discovery domain).
