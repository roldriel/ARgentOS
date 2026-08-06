---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: discovery
worker_id: patterns_worker
subsystem: discovery
state: discovery:DISCOVERY_PATTERNS
lifecycle: discovery
actor: discovery_orchestrator
input_artifacts: [discovery_input.json]
output_artifacts: [development_patterns.md]
---

# Worker: patterns_worker

## Purpose

Detect the development patterns of the team: style, conventions and habits
observable in the code.

## Input

- `discovery_input.json` produced by `init_worker` (includes `project_root`,
  `context_budget`, `sample_size` and the previous KB entries to consider).
- A representative code sample, selected by this worker under the sampling rules.

## Output

- `development_patterns.md`, written to
  `.project/knowledge/discovery/development_patterns.md`, following the contract
  `.agents/orchestrators/discovery/contracts/DEVELOPMENT_PATTERNS.md`.
- A `partial_output` message (`INTER_WORKER_MESSAGE` contract, provenance
  mandatory, compact tag format) written to
  `.project/<session-uuid>/discovery/worker_patterns.json`.

## Tasks

1. Select a representative code sample.
2. Detect style conventions, naming, imports, error handling, testing, logging
   and typing.
3. Document exceptions to the detected conventions.
4. Ensure `development_patterns.md` covers the sections `## Testing`,
   `## Logging and Errors` and `## Validation` explicitly.
5. Add a `## Performance Invariants` section with performance budgets or
   benchmarks that act as functional requirements, only when evidenced
   (benchmark suites, documented guarantees).
6. Every pattern must include category, description, example, `source_files`,
   `source_workers`, `source_sessions`, confidence and scope, as required by the
   contract.

## Sampling

Apply the general sampling rules, bounded by `context_budget` and `sample_size`
(default 10 files per directory, 50 per language, from `.agents/features.toml`):
exclude dependency/build directories, group by extension and functional
directory, select up to `sample_size` files per group prioritizing
representative names, and cap the total by `context_budget`.

## Guardrails

- Pure instruction text; model-agnostic; no Python assumptions.
- Read-only with respect to the project.
- Every pattern must be verifiable in its `source_files` (ground truth validated
  by `D01-discovery-output`); never assert a pattern without a source.

## Retries

- Maximum 3 retries, backoff 1s, 2s, 4s.
- On persistent failure the Discovery Orchestrator may continue without this
  output (partial degradation), unless the scope is `patterns`, in which case it
  reports `discovery:DISCOVERY_FAILED`.
