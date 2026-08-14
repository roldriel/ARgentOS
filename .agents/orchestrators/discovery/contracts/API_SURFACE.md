+++
schema_version = "1.0.0"
artifact = "API_SURFACE.md"
phase = "n/a"
produced_by = "framework_worker"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: API_SURFACE.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_FRAMEWORK]
consumed_by: [core:GATHERING_CONTEXT]
---

# API_SURFACE Contract

## Purpose

Define the format of the `api.md` knowledge-base entry produced by the `framework_worker`. It documents the contract surface the project exposes to the outside. Every piece of software has a surface, so the entry always exists; its content variant depends on the `project_shape` recorded in the manifest and in `discovery_input.json`.

## Location

`.project/knowledge/discovery/api.md`

## Content variants per `project_shape`

- `service`: main endpoints, request/response schemas, external integrations.
- `library`: the public API surface — exports (`__all__`, facades), public classes and functions, exception hierarchy, extension points (hooks, plugins, custom registries).
- `cli`: commands, subcommands, flags, exit codes.
- `application`: main screens, jobs and startup commands.
- `monorepo`: one section per sub-project, each following the variant of its own shape.
- `unknown`: state explicitly that the project shape could not be determined and list the best-effort surface observed.

## Constraints

- The base format follows the base KB entry contract (`KB_DISCOVERY_ENTRY.md`): TOML front matter and `## Discovered Facts` are required.
- Every claim must trace to real source files via `source_files` (provenance per the base contract); ground truth is validated by `D01-discovery-output`.
- The declared `project_shape` of the entry must match the `project_shape` field of the manifest; a mismatch is a validation failure.
