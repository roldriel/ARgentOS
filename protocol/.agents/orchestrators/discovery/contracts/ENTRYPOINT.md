+++
artifact = "ENTRYPOINT.md"
phase = "n/a"
produced_by = "framework_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: ENTRYPOINT.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_FRAMEWORK]
consumed_by: [discovery:DISCOVERY_MERGE, core:GATHERING_CONTEXT]
---

# ENTRYPOINT Contract

## Purpose

Define the format of the `entrypoint.md` knowledge-base entry produced by the
`framework_worker`. It documents where execution starts and how the project
boots: entry file(s), bootstrap sequence, services started and local run
commands. The content variant depends on the `project_shape`.

## Location

`.project/knowledge/discovery/entrypoint.md`

## Content variants per `project_shape`

- `service`: the server start entry (e.g. `uvicorn app.main:app`) and the
  services started at boot.
- `library`: the import entry point — what importing the package exposes and
  initializes (facades, `__init__` side effects).
- `cli`: the command dispatch entry (console script, `argparse`/`click` root
  command).
- `application`: the main executable or startup command.
- `monorepo`: one subsection per sub-project, each following the variant of
  its own shape.
- `unknown`: state explicitly that the entry point could not be determined
  and list the best-effort entry observed.

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Entry Point`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `entrypoint`.
- `source_files`: the entry files and run scripts that evidence the entry.

Provenance fields:

- `source_workers`: MUST include `"framework_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of how the project starts.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **entry_file**: src/app/main.py
- **entry_command**: uvicorn app.main:app --port 8000
- **services_started**: api, background_worker
```

### `## Bootstrap Sequence`

The ordered steps executed when the project starts: entry file(s), bootstrap
sequence and services started. If the project exposes no runnable entry (e.g.
a pure library), the section documents the import entry instead.

### `## Local Run Commands`

The local commands to run the project (or to use the library locally), with
the evidence file for each:

```text
- **run**: uvicorn app.main:app (source: README.md)
- **test**: pytest (source: CONTRIBUTING.md)
```

## Constraints

- The declared `project_shape` must match the `project_shape` declared in the
  manifest; a mismatch is a validation failure.
- Every claim must trace to real files via `source_files`; ground truth is
  validated by `D01-discovery-output`.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (entry and commands traced to real files): harness
  `D01-discovery-output` (discovery domain).
