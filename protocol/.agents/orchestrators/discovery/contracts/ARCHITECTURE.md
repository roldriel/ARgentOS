+++
artifact = "ARCHITECTURE.md"
phase = "n/a"
produced_by = "framework_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: ARCHITECTURE.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_FRAMEWORK]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# ARCHITECTURE Contract

## Purpose

Define the format of the `architecture.md` knowledge-base entry produced by
the `framework_worker`. It documents the architectural patterns of the main
framework: module responsibilities, strong couplings, security surfaces and
extension points.

## Location

`.project/knowledge/discovery/architecture.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Architecture`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `architecture`.
- `source_files`: the source files that evidence the architecture.

Provenance fields:

- `source_workers`: MUST include `"framework_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the detected architecture.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **main_framework**: FastAPI
- **architecture_style**: layered
- **module_count**: 12
```

### `## Module Responsibilities`

One bullet per main module: `- **<module>**: <responsibility>`.

### `## Strong Couplings`

Modules with hard or circular dependencies, with the evidence file for each
coupling.

### `## Security`

Auth model, secrets handling and sensitive surfaces of the project.

### `## Extension Points`

Hooks, plugins and registries the project exposes (especially relevant for
`library` and `cli` shapes).

## Constraints

- Mermaid diagrams are allowed as a supporting format but never replace the
  factual content of the required sections.
- Every claim must trace to real source files via `source_files`; ground truth
  is validated by `D01-discovery-output`.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (claims trace to `source_files`): harness
  `D01-discovery-output` (discovery domain).
