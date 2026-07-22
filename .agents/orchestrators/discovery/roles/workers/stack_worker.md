---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: discovery
worker_id: stack_worker
subsystem: discovery
state: discovery:DISCOVERY_STACK
lifecycle: discovery
actor: discovery_orchestrator
input_artifacts: [discovery_input.json]
output_artifacts: [stack.md, dependencies.md, containers.md, database.md]
---

# Worker: stack_worker

## Purpose

Detect the technology stack of the project: languages, frameworks, dependencies,
containers and databases.

## Input

- `discovery_input.json` produced by `init_worker` (includes `project_root`,
  `context_budget`, `sample_size` and the previous KB entries to consider).

## Output

- `stack.md`, `dependencies.md`, `containers.md`, `database.md`, written to
  `.project/knowledge/discovery/`, each following the base KB entry contract
  `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`.
- A `partial_output` message (`INTER_WORKER_MESSAGE` contract, provenance
  mandatory) written to `.project/<session-uuid>/discovery/worker_stack.json`.
  This message is the input of `framework_worker` and uses the compact tag
  format.

## Tasks

1. Detect languages and frameworks by file extension and configuration files.
2. List dependencies from `package.json`, `requirements.txt`, `Cargo.toml`, etc.
3. Detect `Dockerfile`, `docker-compose.yml` and other container definitions.
4. Detect database configurations.
5. Record provenance (`source_files`, `source_workers`, `source_sessions`) in
   every entry.

## Sampling

Apply the general sampling rules of the Discovery Orchestrator, bounded by
`context_budget` and `sample_size` (default 10 files per directory, 50 per
language, from `.agents/features.toml`):

1. Exclude dependency and build directories.
2. Group by extension and functional directory.
3. Select up to `sample_size` files per group, prioritizing representative names.
4. Cap the total by `context_budget`.

## Guardrails

- Pure instruction text; model-agnostic; no Python assumptions.
- Read-only with respect to the project.
- Every claim must trace back to a real configuration or manifest file
  (`source_files`); ground truth is validated by `D01-discovery-output`.

## Retries

- Maximum 3 retries, backoff 1s, 2s, 4s.
- On persistent failure the Discovery Orchestrator may continue without this
  output (partial degradation), unless the scope is `stack`, in which case it
  reports `discovery:DISCOVERY_FAILED`.
