+++
artifact = "CONFIGURATION.md"
phase = "n/a"
produced_by = "framework_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: CONFIGURATION.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_FRAMEWORK]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# CONFIGURATION Contract

## Purpose

Define the format of the `configuration.md` knowledge-base entry produced by
the `framework_worker`. It documents the configuration of the project:
settings files, environment variables and how to run, build and release it.

## Location

`.project/knowledge/discovery/configuration.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Configuration`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `configuration`.
- `source_files`: the configuration files (`settings.py`, `.env.example`,
  blueprints, etc.).

Provenance fields:

- `source_workers`: MUST include `"framework_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the configuration model.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **settings_files**: config/settings.py
- **env_example**: .env.example
- **config_layers**: defaults, environment, secrets
```

### `## Run, Build and Release`

How to run the application AND how to build and release the project (for a
library, how to build and publish it). One bullet per command or workflow,
with the evidence file:

```text
- **run**: uvicorn app.main:app (source: README.md)
- **build**: python -m build (source: pyproject.toml)
- **release**: git tag + CI publish (source: .github/workflows/release.yml)
```

## Constraints

- The section covers running an application and publishing a library,
  whichever applies to the declared `project_shape`.
- Every claim must trace to a real configuration or documentation file
  (`source_files`); ground truth is validated by `D01-discovery-output`.
- No secret values are recorded: configuration facts never include actual
  secret strings or environment variable values.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (commands and settings traced to real files):
  harness `D01-discovery-output` (discovery domain).
