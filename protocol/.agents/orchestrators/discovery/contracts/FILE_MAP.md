+++
artifact = "FILE_MAP.md"
phase = "n/a"
produced_by = "init_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: FILE_MAP.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_INIT]
consumed_by: [discovery:DISCOVERY_MERGE, core:GATHERING_CONTEXT]
---

# FILE_MAP Contract

## Purpose

Define the format of the `file_map.md` knowledge-base entry produced by the
`init_worker`. It is an annotated `path → responsibility` index of the main
folders and relevant files of the project, so an agent can navigate the
project without exploratory search.

## Location

`.project/knowledge/discovery/file_map.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `File Map`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `file_map`.
- `source_files`: the sampled files and folders that evidence the map.

Provenance fields:

- `source_workers`: MUST include `"init_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the project layout.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **root**: src/
- **main_folders**: src/app, src/core, tests
- **structure_hash**: sha256:jkl012...
```

### `## Map`

Annotated index of the main folders and relevant files. One bullet per entry:

```text
- **src/app/main.py**: application entry point
- **src/core/**: domain services
```

## Constraints

- The map is a navigable index, NOT a full directory tree: it includes only
  what an agent needs to orient itself and locate relevant code.
- The `structure_hash` recorded in `## Discovered Facts` must match the
  `[hashes]` section of the manifest; the manifest invalidates this entry
  when the directory tree shape changes.
- Every claim must trace to real project paths; ground truth is validated by
  `D01-discovery-output`.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (paths exist, map is not a full tree): harness
  `D01-discovery-output` (discovery domain).
