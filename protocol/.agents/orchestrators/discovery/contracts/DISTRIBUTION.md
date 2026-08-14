+++
artifact = "DISTRIBUTION.md"
phase = "n/a"
produced_by = "stack_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: DISTRIBUTION.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_STACK]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# DISTRIBUTION Contract

## Purpose

Define the format of the `distribution.md` knowledge-base entry produced by
the `stack_worker`. It documents how a `library` or `cli` project is packaged
and published: target registry, current version, extras, build backend and
release command.

## Location

`.project/knowledge/discovery/distribution.md`

## Applicability

The entry is written only when the `project_shape` is `library` or `cli`
(as declared in the manifest). For any other shape the entry is omitted and
the omission is legitimate; it is not a validation failure.

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Distribution`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `distribution`.
- `source_files`: the packaging and publication files (`pyproject.toml`,
  `package.json`, `Cargo.toml`, CI release workflow, etc.).

Provenance fields:

- `source_workers`: MUST include `"stack_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of how the project is distributed.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **registry**: PyPI
- **package_name**: mypackage
- **current_version**: 1.2.3
- **extras**: [dev, test]
```

### `## Build and Release`

The build backend and the release command or workflow, with the evidence
file for each:

```text
- **build_backend**: hatchling (source: pyproject.toml)
- **release_command**: python -m build && twine upload dist/* (source: CONTRIBUTING.md)
```

## Constraints

- Every claim must trace to a real packaging or release file (`source_files`);
  ground truth is validated by `D01-discovery-output`.
- The `project_shape` implied by this entry must match the `project_shape`
  declared in the manifest.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (packaging and release traced to real files):
  harness `D01-discovery-output` (discovery domain).
