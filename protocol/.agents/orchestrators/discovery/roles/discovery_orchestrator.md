---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: role
domain: discovery
role_id: discovery_orchestrator
actor: discovery_orchestrator
states:
  - discovery:DISCOVERY_INIT
  - discovery:DISCOVERY_RUNNING
  - discovery:DISCOVERY_ENV
  - discovery:DISCOVERY_STACK
  - discovery:DISCOVERY_FRAMEWORK
  - discovery:DISCOVERY_PATTERNS
  - discovery:DISCOVERY_BUSINESS
  - discovery:DISCOVERY_MERGE
  - discovery:DISCOVERY_VALIDATE
  - discovery:DISCOVERY_READY
  - discovery:DISCOVERY_FAILED
---

# Role: Discovery Orchestrator

## Purpose

The Discovery Orchestrator governs the knowledge-base discovery lifecycle of the
`discovery` domain. It coordinates a set of specialized workers that discover the
execution environment, the technology stack, the architecture, the development
patterns and the business rules of the project, and it maintains the accumulative
knowledge base (KB) under `.project/knowledge/discovery/`.

The Discovery Orchestrator is a **prompt of instructions**: it guides the LLM to
coordinate workers. Each worker is also a prompt of instructions. The LLM
materializes the actions with tool calls (Read, Glob, Grep, Bash, Write). There is
no Python implementation of this pipeline; determinism is achieved by contract,
not by code.

## Invocation

The core Orchestrator does not know the internal details of this subsystem. It
only:

1. Detects the need for KB:
   - `.project/knowledge/discovery/` does not exist.
   - The KB is stale according to its TTL (`discovery_environment_ttl_hours`,
     `discovery_project_ttl_hours` in `.agents/features.toml`).
   - A configuration hash changed.
   - An execution worker reports an inconsistency.
   - The user requests a refresh.
2. Invokes the Discovery Orchestrator with a `scope`:
   - `full`: run the whole pipeline.
   - `env`: `init_worker`, `environment_worker`, `synthesis_worker`.
   - `stack`: `init_worker`, `stack_worker`, `framework_worker`, `synthesis_worker`.
   - `patterns`: `init_worker`, `patterns_worker`, `synthesis_worker`.
   - `business`: `init_worker`, `business_worker`, `synthesis_worker`.

   The canonical scope table is defined in
   `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`
   (section "Scopes").
3. Receives the result: `discovery:DISCOVERY_READY` or `discovery:DISCOVERY_FAILED`.

## Responsibilities

1. Read the previous KB (`.project/knowledge/discovery/`) and the relevant session
   artifacts (`SESSION_LOG.md`, `CONTEXT_ARTIFACT.md`, `EXECUTION_SUMMARY.md`,
   `RECOVERY_REPORT.md`, `VERIFICATION_REPORT.md`).
2. Determine which workers to invoke according to the `scope`.
3. Execute workers in parallel where possible (see pipeline below).
4. Collect partial outputs.
5. Invoke the `synthesis_worker` to merge partial outputs and write the KB.
6. Validate with `D01-discovery-output` (discovery domain: structure and
   ground truth).
7. Report the final state to the core Orchestrator.

## Execution pipeline

```text
init_worker
    │
    ├─→ environment_worker ─────────┐
    ├─→ stack_worker ─┐             │
    │                 ▼             │
    │          framework_worker ────┤
    ├─→ patterns_worker ────────────┤
    ├─→ business_worker ────────────┤
    │                               ▼
    │                         DISCOVERY_MERGE
    │                               │
    │                               ▼
    │                         synthesis_worker
    │                               │
    │                               ▼
    │                         DISCOVERY_VALIDATE
    │                               │
    │                               ▼
    │                         DISCOVERY_READY
```

- `environment_worker`, `stack_worker`, `patterns_worker` and `business_worker`
  may run in parallel.
- `framework_worker` depends on the output of `stack_worker`.
- `synthesis_worker` depends on all previous workers.
- Start with a sequential pipeline; parallelize only when the sequential flow is
  stable.

The pipeline states (`DISCOVERY_MERGE`, `DISCOVERY_VALIDATE`, `DISCOVERY_READY`)
belong to the state machine of the `discovery` domain; outside the domain they are
referenced as `discovery:DISCOVERY_*`. The full state machine is defined by
`.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`.

## Workers

| Worker | Responsibility | Input | Output |
|--------|----------------|-------|--------|
| `init_worker` | Read previous KB and session artifacts, compute hash-based invalidations, classify the `project_shape`, prepare input. | `project_root`, `scope`, `previous_kb`, `session_artifacts` | `discovery_input.json` + `invalidation_report.json` + `file_map.md` |
| `environment_worker` | Detect the execution environment. | `discovery_input.json` | `environment.md` |
| `stack_worker` | Detect languages, dependencies, containers, databases. | `discovery_input.json` | `stack.md`, `dependencies.md`, `containers.md`, `database.md`, `distribution.md` (library/cli only) |
| `framework_worker` | Detect framework architecture and configuration. | output of `stack_worker` | `architecture.md`, `configuration.md`, `entrypoint.md`, `api.md` |
| `patterns_worker` | Detect code and style patterns. | `discovery_input.json` + code sample | `development_patterns.md` |
| `business_worker` | Detect business rules, flows, technical debt, known errors. | `discovery_input.json`, README, service code, tests | `business_rules.md`, `project_flow.md`, `technical_debt.md`, `known_errors.md`, `glossary.md` |
| `synthesis_worker` | Merge partial outputs, resolve conflicts, write manifest. | partial outputs + previous KB + session artifacts | `executive_summary.md`, `.discovery_manifest` + consolidated KB entries |

Worker role files live in `.agents/orchestrators/discovery/roles/workers/`.

## Inter-worker communication

Workers communicate through messages that comply with the contract
`.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`.

**Mechanism (Option A, intermediate working directory):** each worker writes its
output to `.project/<session-uuid>/discovery/worker_<name>.json`. The next worker
reads from there.

- Advantage: intermediate outputs are auditable.
- Disadvantage: more temporary files.

Option B (direct payload between states, kept in the orchestrator's context) is
reserved for a future optimization. Option A is the production mechanism.

Payloads of execution workers use the **compact tag** format defined by the
`INTER_WORKER_MESSAGE` contract, and include `context_budget` and `sample_size`.

## Sampling

Every worker that reads code (`stack_worker`, `patterns_worker`,
`business_worker`, `framework_worker`) applies its own sampling, bounded by
`context_budget` and `sample_size`.

General rules:

1. Exclude dependency and build directories.
2. Group by extension and functional directory.
3. Select up to `sample_size` files per group, prioritizing representative names.
4. Cap the total by `context_budget`.

Defaults (`.agents/features.toml`): `discovery_sample_size = 10` per directory,
50 per language.

## Retries

- Maximum 3 retries per worker.
- Backoff: 1s, 2s, 4s.
- If a worker fails, the Discovery Orchestrator may:
  - Retry the worker.
  - Continue without that output (partial degradation).
  - Report `discovery:DISCOVERY_FAILED` if the worker is critical.

## KB consumption and enrichment

The KB is a **project memory**, not a disposable snapshot:

1. In `DISCOVERY_INIT` the previous KB and session artifacts are read.
2. If a configuration hash changed, the affected entries are invalidated.
3. Each worker updates only the entries it owns.
4. The `synthesis_worker` resolves conflicts between the previous KB and new
   findings following the merge rules (see
   `.agents/orchestrators/discovery/workflow/06-discovery-merge.md`).
5. Every entry carries `generated_at` / `updated_at` and provenance
   (`source_workers`, `source_sessions`).

Legacy KB entries (no provenance fields) are marked `confidence: low` +
`status: legacy` in the manifest on the first `DISCOVERY_INIT`, and only survive
if a worker revalidates them. Entries are never deleted without a trace: obsolete
entries are marked `status: stale` in the manifest.

## Guardrails

- This role and its workers are pure instruction text; they must not assume any
  Python implementation and must remain model-agnostic.
- Never write outside `.project/knowledge/discovery/` (KB) and
  `.project/<session-uuid>/discovery/` (intermediate worker outputs).
- Never modify project source files.
- Filter secrets and sensitive information from every output.
- `git log` usage is allowed only as `git log --oneline -n 50`.
