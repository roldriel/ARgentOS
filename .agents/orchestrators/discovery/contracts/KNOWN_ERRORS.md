+++
schema_version = "1.0.0"
artifact = "KNOWN_ERRORS.md"
phase = "n/a"
produced_by = "business_worker"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: KNOWN_ERRORS.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_BUSINESS]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# KNOWN_ERRORS Contract

## Purpose

Define the format of the `known_errors.md` knowledge-base entry produced by
the `business_worker`. It records the known errors of the project with their
symptoms, impact, workaround (when known) and evidence.

## Location

`.project/knowledge/discovery/known_errors.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Known Errors`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `known_errors`.
- `source_files`: the code, tests and session artifacts that evidence the
  errors (e.g. `RECOVERY_REPORT.md`).

Provenance fields:

- `source_workers`: MUST include `"business_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the error profile.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **known_error_count**: 5
- **source_sessions**: session-68c54119
```

### `## Known Errors`

One bullet per known error, with symptom, impact, workaround (when known) and
evidence:

```text
- **<error>**: <symptom> — impact: <impact>; workaround: <workaround or none> (source: <file>)
```

## Constraints

- Every error must trace to a real source file or session artifact
  (`source_files`); never invent errors.
- If no known errors are evidenced, the section states
  `_No known errors evidenced._`.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (errors traced to code/tests/session artifacts):
  harness `D01-discovery-output` (discovery domain).
