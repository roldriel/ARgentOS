+++
schema_version = "1.0.0"
artifact = "DEPENDENCIES.md"
phase = "n/a"
produced_by = "stack_worker"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: DEPENDENCIES.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_STACK]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# DEPENDENCIES Contract

## Purpose

Define the format of the `dependencies.md` knowledge-base entry produced by
the `stack_worker`. It records the dependencies of the project as declared in
real configuration files, separating external dependencies from internal
modules of the project.

## Location

`.project/knowledge/discovery/dependencies.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Dependencies`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `dependencies`.
- `source_files`: the manifest and lock files that evidence the dependencies.

Provenance fields:

- `source_workers`: MUST include `"stack_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the dependency footprint.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **managers**: pip, npm
- **external_count**: 42
- **internal_count**: 7
```

### `## External Dependencies`

Third-party dependencies. One bullet per dependency:

```text
- **<name>**: <version constraint> (source: <file>)
```

### `## Internal Dependencies`

Internal modules/packages of the project and what depends on them. One bullet
per internal package:

```text
- **<package>**: <modules that consume it>
```

## Constraints

- Every dependency listed must appear in a real configuration or lock file
  (`source_files`); ground truth is validated by `D01-discovery-output`.
- If the project has no external or internal dependencies, the corresponding
  section states that explicitly.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (dependencies traced to configuration files):
  harness `D01-discovery-output` (discovery domain).
