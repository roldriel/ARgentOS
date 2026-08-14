---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: discovery
worker_id: business_worker
subsystem: discovery
state: discovery:DISCOVERY_BUSINESS
lifecycle: discovery
actor: discovery_orchestrator
input_artifacts: [discovery_input.json]
output_artifacts: [business_rules.md, project_flow.md, technical_debt.md, known_errors.md, glossary.md]
---

# Worker: business_worker

## Purpose

Detect the business rules, project flows, technical debt and known errors of the
project.

## Input

- `discovery_input.json` produced by `init_worker` (includes `project_root`,
  `context_budget`, `sample_size` and the previous KB entries to consider).
- The project README, the code of the main services and the tests.
- Session artifacts that report problems (e.g. `RECOVERY_REPORT.md`).

## Output

- `business_rules.md`, `project_flow.md`, `technical_debt.md`,
  `known_errors.md`, `glossary.md`, written to
  `.project/knowledge/discovery/`, each following the base KB entry contract
  `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`.
- A `partial_output` message (`INTER_WORKER_MESSAGE` contract, provenance
  mandatory, compact tag format) written to
  `.project/<session-uuid>/discovery/worker_business.json`.

## Tasks

1. Read the README and the main services.
2. Identify the business flows.
3. Detect technical debt and known errors (comments, `TODO`, `FIXME`,
   `RECOVERY_REPORT.md`).
4. Write `glossary.md`: domain terms with their definition and the source file
   evidencing each term.
5. Ensure `technical_debt.md` includes a `## Top Risks` section: technical debt
   plus known errors ranked by impact.
6. Record provenance in every entry.

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
- Every claim must trace back to a real source file or session artifact; never
  invent business rules.

## Retries

- Maximum 3 retries, backoff 1s, 2s, 4s.
- On persistent failure the Discovery Orchestrator may continue without this
  output (partial degradation), unless the scope is `business`, in which case it
  reports `discovery:DISCOVERY_FAILED`.
