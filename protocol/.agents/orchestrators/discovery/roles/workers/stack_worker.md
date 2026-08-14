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
output_artifacts: [stack.md, dependencies.md, containers.md, database.md, distribution.md]
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
- `distribution.md`, written to `.project/knowledge/discovery/`, only when the
  `project_shape` is `library` or `cli`: how the project is packaged and
  published (registry such as PyPI/npm/crates, current version, extras, build
  backend, release command). For any other shape the entry is omitted; the
  omission is legitimate and is not a validation failure.
- A `partial_output` message (`INTER_WORKER_MESSAGE` contract, provenance
  mandatory) written to `.project/<session-uuid>/discovery/worker_stack.json`.
  This message is the input of `framework_worker` and uses the compact tag
  format.

## Tasks

1. Detect languages and frameworks by file extension and configuration files.
2. List dependencies from `package.json`, `requirements.txt`, `Cargo.toml`, etc.
3. Detect `Dockerfile`, `docker-compose.yml` and other container definitions.
4. Detect database configurations.
5. Write `distribution.md` for `library`/`cli` shapes (packaging and
   publication); omit it for other shapes.
6. Ensure `database.md` includes the section `## Main Models`.
7. Ensure `dependencies.md` includes the section `## Internal Dependencies`
   (internal modules/packages of the project).
8. Ensure `stack.md` includes the section `## Compatibility Constraints`
   (supported runtime versions, zero-dependency guarantees, typing guarantees
   such as PEP 561) where evidenced.
9. Record provenance (`source_files`, `source_workers`, `source_sessions`) in
   every entry.

## Sampling

Apply the general sampling rules of the Discovery Orchestrator, bounded by
`context_budget`, `sample_size` and `sample_size_per_language` as given in
`discovery_input.json` (never worker-local defaults):

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
