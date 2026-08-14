+++
artifact = "TECHNICAL_DEBT.md"
phase = "n/a"
produced_by = "business_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: TECHNICAL_DEBT.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_BUSINESS]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# TECHNICAL_DEBT Contract

## Purpose

Define the format of the `technical_debt.md` knowledge-base entry produced by
the `business_worker`. It records the technical debt and known errors of the
project ranked by impact, with the evidence for each item.

## Location

`.project/knowledge/discovery/technical_debt.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Technical Debt`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `technical_debt`.
- `source_files`: the code, comments and session artifacts that evidence the
  debt (e.g. `RECOVERY_REPORT.md`).

Provenance fields:

- `source_workers`: MUST include `"business_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the debt profile.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **todo_count**: 14
- **fixme_count**: 3
- **known_error_count**: 5
```

### `## Top Risks`

Technical debt plus known errors ranked by impact. One bullet per risk:

```text
- **<risk>**: <impact> (source: <file>)
```

### `## Performance Invariants`

Performance invariants of the project (latency budgets, throughput bounds,
resource limits). Required only when evidenced; if none are evidenced, the
section is omitted.

## Constraints

- Every risk must trace to a real source file or session artifact
  (`source_files`); ground truth is validated by `D01-discovery-output`.
- The `## Top Risks` section must stay aligned with the `## Top Risks`
  section of `executive_summary.md`.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (risks traced to code/comments/session artifacts):
  harness `D01-discovery-output` (discovery domain).
