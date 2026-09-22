+++
schema_version = "1.0.0"
artifact = "DATABASE.md"
phase = "n/a"
produced_by = "stack_worker"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: DATABASE.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_STACK]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# DATABASE Contract

## Purpose

Define the format of the `database.md` knowledge-base entry produced by the
`stack_worker`. It records the database configuration of the project: engines,
connections and main data models.

## Location

`.project/knowledge/discovery/database.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Database`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `database`.
- `source_files`: the configuration, migration and model files that evidence
  the database setup.

Provenance fields:

- `source_workers`: MUST include `"stack_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the database setup.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **engine**: postgres
- **connection_config**: config/settings.py
- **migration_tool**: alembic
```

### `## Main Models`

The main data models of the project. One bullet per model:

```text
- **<model>**: <purpose> (source: <file>)
```

## Constraints

- Every model and connection must trace to a real file (`source_files`);
  ground truth is validated by `D01-discovery-output`.
- If the project has no database, the section states
  `_No database configuration found._`. An absence is a claim established by
  scanning the project tree, so its `source_files` carries the reserved value
  `"project_scan"` (`.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`,
  §Optional Front Matter (provenance)); it does not name a file that does not
  exist.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (models traced to model/configuration files):
  harness `D01-discovery-output` (discovery domain).
