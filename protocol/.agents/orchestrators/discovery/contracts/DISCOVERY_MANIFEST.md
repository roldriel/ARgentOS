+++
schema_version = "1.0.0"
artifact = "DISCOVERY_MANIFEST.md"
phase = "n/a"
produced_by = "synthesis_worker"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: DISCOVERY_MANIFEST.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_MERGE]
consumed_by: [discovery:DISCOVERY_INIT, discovery:DISCOVERY_VALIDATE]
---

# DISCOVERY_MANIFEST Contract

## Purpose

Define the format of the manifest of the accumulative knowledge base. The manifest tracks KB metadata, invalidation hashes, active and stale entries, and worker execution status.

## Location

`.project/knowledge/discovery/.discovery_manifest`

> **Naming note:** this contract document is `DISCOVERY_MANIFEST.md`; the
> runtime artifact it defines is `.discovery_manifest` (TOML) under
> `.project/knowledge/discovery/`. The contract filename is not an artifact
> path.

## Format

TOML.

## Required sections

### `[knowledge_base]`

- `version`: string
- `generated_at`: ISO 8601
- `updated_at`: ISO 8601
- `ttl_hours`: integer
- `role_version`: string
- `task_scope`: string
- `project_root`: string
- `project_shape`: string; one of `library`, `cli`, `service`, `application`, `monorepo` or `unknown` (classified by `init_worker`)

### `[hashes]`

- `config_files_hash`: string
- `sample_files_hash`: string
- `environment_hash`: string
- `structure_hash`: string (hash of the directory tree shape; invalidates `file_map.md`)

### `[entries]`

- `active`: list of strings
- `stale`: list of strings

### `[workers]`

- `invoked`: list of strings
- `completed`: list of strings

### `[runtime]`

- `model_used`: string (optional)
- `execution_time_seconds`: float (optional)

## Example

```toml
[knowledge_base]
version = "1.0.0"
generated_at = "2026-07-21T05:00:00Z"
updated_at = "2026-07-21T05:00:00Z"
ttl_hours = 24
role_version = "discovery_orchestrator:v1"
task_scope = "full"
project_root = "/home/user/project"
project_shape = "library"

[hashes]
config_files_hash = "sha256:abc123..."
sample_files_hash = "sha256:def456..."
environment_hash = "sha256:ghi789..."
structure_hash = "sha256:jkl012..."

[entries]
active = [
  "executive_summary.md",
  "entrypoint.md",
  "file_map.md",
  "glossary.md",
  "api.md",
  "distribution.md",
  "stack.md",
  "dependencies.md",
  "environment.md",
  "development_patterns.md"
]
stale = [
  "old_feature.md"
]

[workers]
invoked = ["environment_worker", "stack_worker", "framework_worker", "patterns_worker", "business_worker", "synthesis_worker"]
completed = ["environment_worker", "stack_worker"]

[runtime]
model_used = "kimi-k2"
execution_time_seconds = 42.5
```

## Notes

- Entries are never deleted without a trace: invalidated entries move from `active` to `stale` in `[entries]`, following the KB merge rules.
- `[runtime]` fields are optional; all other sections and fields are required.
