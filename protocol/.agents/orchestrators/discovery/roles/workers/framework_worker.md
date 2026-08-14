---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: discovery
worker_id: framework_worker
subsystem: discovery
state: discovery:DISCOVERY_FRAMEWORK
lifecycle: discovery
actor: discovery_orchestrator
input_artifacts: [worker_stack.json]
output_artifacts: [architecture.md, configuration.md, entrypoint.md, api.md]
---

# Worker: framework_worker

## Purpose

Detect the architectural patterns of the main framework and document the project
configuration, based on the output of `stack_worker`.

## Input

- The `partial_output` message of `stack_worker`
  (`.project/<session-uuid>/discovery/worker_stack.json`), plus the project
  configuration files it references.
- The previous KB entries listed in `discovery_input.json` (`context_budget`
  and `sample_size` apply as inherited from the run input).
- The `project_shape` classified by `init_worker`, read from
  `discovery_input.json`; it drives the content variant of `api.md` and
  `entrypoint.md`.

## Output

- `architecture.md`, `configuration.md`, `entrypoint.md`, `api.md`, written to
  `.project/knowledge/discovery/`, each following the base KB entry contract
  `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md` (`api.md`
  also follows the parametrized contract
  `.agents/orchestrators/discovery/contracts/API_SURFACE.md`).
- A `partial_output` message (`INTER_WORKER_MESSAGE` contract, provenance
  mandatory, compact tag format) written to
  `.project/<session-uuid>/discovery/worker_framework.json`.

## Tasks

1. Detect the architectural patterns of the main framework.
2. Read configuration files (settings, blueprints, etc.).
3. Document build, test and deploy scripts.
4. Write `entrypoint.md`: how the application starts — entry file(s), bootstrap
   sequence, services started, local run commands. For `project_shape:
   library` it documents the import entry point instead (what importing the
   package exposes and initializes, facades); for `cli`, the command dispatch
   entry.
5. Write `api.md` following the `API_SURFACE.md` contract, with the content
   variant driven by the `project_shape` read from `discovery_input.json`.
6. Ensure `architecture.md` includes the required sections
   `## Module Responsibilities`, `## Strong Couplings`, `## Security` (auth,
   secrets handling, sensitive surfaces) and `## Extension Points` (hooks,
   plugins, registries — especially relevant for `library` and `cli` shapes).
   Mermaid diagrams are allowed as a supporting format but never replace
   factual content.
7. Ensure `configuration.md` includes the section `## Run, Build and Release`
   (covers running an application AND publishing a library).
8. Record provenance in every entry.

## Sampling

Apply the general sampling rules, bounded by `context_budget`, `sample_size`
and `sample_size_per_language` as given in `discovery_input.json` (never
worker-local defaults):
exclude dependency/build directories, group by extension and functional
directory, select up to `sample_size` files per group prioritizing
representative names, and cap the total by `context_budget`.

## Guardrails

- Pure instruction text; model-agnostic; no Python assumptions.
- Read-only with respect to the project.
- Depends on `stack_worker`: if its input is missing due to partial degradation,
  report the dependency failure instead of guessing the stack.

## Retries

- Maximum 3 retries, backoff 1s, 2s, 4s.
- On persistent failure the Discovery Orchestrator may continue without this
  output (partial degradation), unless the scope is `stack`, in which case it
  reports `discovery:DISCOVERY_FAILED`.
