---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: state_machine
domain: discovery
actor: discovery_orchestrator
states_defined:
  - DISCOVERY_INIT
  - DISCOVERY_RUNNING
  - DISCOVERY_ENV
  - DISCOVERY_STACK
  - DISCOVERY_FRAMEWORK
  - DISCOVERY_PATTERNS
  - DISCOVERY_BUSINESS
  - DISCOVERY_MERGE
  - DISCOVERY_VALIDATE
  - DISCOVERY_READY
  - DISCOVERY_FAILED
---

# Discovery State Machine

## Purpose

Define the lifecycle states of a knowledge-base discovery run of the `discovery`
domain and the allowed transitions between them.

This state machine is independent from the task state machine of the `core`
domain (`.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`). The
Discovery Orchestrator does not govern the user task; it only produces and
maintains the knowledge base under `.project/knowledge/discovery/`. Outside the
domain, its states are referenced as `discovery:DISCOVERY_*`.

The same core rules apply:

* A state represents a verifiable condition of the discovery run, not just a
  workflow position.
* Every transition must be justified by a valid transition rule and, where
  required, by a produced or validated artifact.
* The Discovery Orchestrator must not skip states to simplify a run. Partial
  scopes (`env`, `stack`, `patterns`, `business`) enter the pipeline at the
  state that owns the scope and rejoin it at `DISCOVERY_MERGE`; they do not
  invent transitions.

---

# Transition Graph

```text
DISCOVERY_INIT
    |
    v
DISCOVERY_RUNNING
    |
    |---> DISCOVERY_ENV ---------+
    |---> DISCOVERY_STACK        |
    |          |                 |
    |          v                 |
    |     DISCOVERY_FRAMEWORK    |
    |---> DISCOVERY_PATTERNS     |
    |---> DISCOVERY_BUSINESS     |
    |                            |
    +------------+---------------+
                 v
          DISCOVERY_MERGE
                 |
                 v
          DISCOVERY_VALIDATE
                 |
       +---------+---------+
       v                 v
DISCOVERY_READY    DISCOVERY_FAILED
```

* `DISCOVERY_ENV`, `DISCOVERY_STACK`, `DISCOVERY_PATTERNS` and
  `DISCOVERY_BUSINESS` may run in parallel.
* `DISCOVERY_FRAMEWORK` depends on `DISCOVERY_STACK`.
* `DISCOVERY_MERGE` depends on all discovery states selected by the scope.
* Any state may transition to `DISCOVERY_FAILED` on an unrecoverable failure.
* `DISCOVERY_FAILED` may transition back to `DISCOVERY_INIT` for a retry.

---

# States

## DISCOVERY_INIT

### Description

Initialize the discovery run: read the previous KB
(`.project/knowledge/discovery/`) and the relevant session artifacts, compute
hash-based invalidations, mark legacy entries, and prepare the structured input
for the workers.

### Worker

`init_worker` (`.agents/orchestrators/discovery/roles/workers/init_worker.md`).

### Required Output Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
.project/<session-uuid>/discovery/invalidation_report.json
.project/<session-uuid>/<iteration>/D<order>-KB_DISCOVERY_REPORT.md
.project/knowledge/discovery/file_map.md
```

### Harness

The exit transition is gated by harness trigger `D00`
(`.agents/orchestrators/discovery/harness/policies/D00-discovery-init.md`).

### Allowed Transitions

```text
DISCOVERY_INIT
    |
    v
DISCOVERY_RUNNING
```

On unrecoverable failure:

```text
DISCOVERY_INIT
    |
    v
DISCOVERY_FAILED
```

---

## DISCOVERY_RUNNING

### Description

The discovery session is initialized and the run may proceed. This is a
coordination state: the Discovery Orchestrator selects the discovery states to
enter according to the invocation `scope`.

### Required Input Artifact

```text
.project/<session-uuid>/<iteration>/D<order>-KB_DISCOVERY_REPORT.md
```

### Allowed Transitions

According to the scope, to any of:

```text
DISCOVERY_RUNNING
    |
    |---> DISCOVERY_ENV
    |---> DISCOVERY_STACK
    |---> DISCOVERY_PATTERNS
    |---> DISCOVERY_BUSINESS
```

On unrecoverable failure:

```text
DISCOVERY_RUNNING
    |
    v
DISCOVERY_FAILED
```

---

## DISCOVERY_ENV

### Description

Detect the execution environment of the project (OS, shell, tools, runtime).

### Worker

`environment_worker`
(`.agents/orchestrators/discovery/roles/workers/environment_worker.md`).

### Required Input Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
```

### Required Output Artifacts

```text
.project/<session-uuid>/discovery/worker_environment.json
.project/knowledge/discovery/environment.md
```

### Allowed Transitions

```text
DISCOVERY_ENV
    |
    v
DISCOVERY_MERGE
```

On unrecoverable failure:

```text
DISCOVERY_ENV
    |
    v
DISCOVERY_FAILED
```

---

## DISCOVERY_STACK

### Description

Detect the technology stack: languages, dependencies, containers, databases.

### Worker

`stack_worker` (`.agents/orchestrators/discovery/roles/workers/stack_worker.md`).

### Required Input Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
```

### Required Output Artifacts

```text
.project/<session-uuid>/discovery/worker_stack.json
.project/knowledge/discovery/stack.md
.project/knowledge/discovery/dependencies.md
.project/knowledge/discovery/containers.md
.project/knowledge/discovery/database.md
.project/knowledge/discovery/distribution.md  (only for library/cli project shapes)
```

### Allowed Transitions

```text
DISCOVERY_STACK
    |
    v
DISCOVERY_FRAMEWORK
```

On unrecoverable failure:

```text
DISCOVERY_STACK
    |
    v
DISCOVERY_FAILED
```

---

## DISCOVERY_FRAMEWORK

### Description

Detect the framework architecture and configuration of the project.

### Worker

`framework_worker`
(`.agents/orchestrators/discovery/roles/workers/framework_worker.md`).

### Required Input Artifacts

```text
.project/<session-uuid>/discovery/worker_stack.json
```

### Required Output Artifacts

```text
.project/<session-uuid>/discovery/worker_framework.json
.project/knowledge/discovery/architecture.md
.project/knowledge/discovery/configuration.md
.project/knowledge/discovery/entrypoint.md
.project/knowledge/discovery/api.md
```

### Allowed Transitions

```text
DISCOVERY_FRAMEWORK
    |
    v
DISCOVERY_MERGE
```

On unrecoverable failure:

```text
DISCOVERY_FRAMEWORK
    |
    v
DISCOVERY_FAILED
```

---

## DISCOVERY_PATTERNS

### Description

Detect code and style patterns of the project.

### Worker

`patterns_worker`
(`.agents/orchestrators/discovery/roles/workers/patterns_worker.md`).

### Required Input Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
```

plus the code sample selected by `init_worker`.

### Required Output Artifacts

```text
.project/<session-uuid>/discovery/worker_patterns.json
.project/knowledge/discovery/development_patterns.md
```

### Allowed Transitions

```text
DISCOVERY_PATTERNS
    |
    v
DISCOVERY_MERGE
```

On unrecoverable failure:

```text
DISCOVERY_PATTERNS
    |
    v
DISCOVERY_FAILED
```

---

## DISCOVERY_BUSINESS

### Description

Detect business rules, flows, technical debt and known errors.

### Worker

`business_worker`
(`.agents/orchestrators/discovery/roles/workers/business_worker.md`).

### Required Input Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
```

plus the README, service code and tests selected by `init_worker`.

### Required Output Artifacts

```text
.project/<session-uuid>/discovery/worker_business.json
.project/knowledge/discovery/business_rules.md
.project/knowledge/discovery/project_flow.md
.project/knowledge/discovery/technical_debt.md
.project/knowledge/discovery/known_errors.md
.project/knowledge/discovery/glossary.md
```

### Allowed Transitions

```text
DISCOVERY_BUSINESS
    |
    v
DISCOVERY_MERGE
```

On unrecoverable failure:

```text
DISCOVERY_BUSINESS
    |
    v
DISCOVERY_FAILED
```

---

## DISCOVERY_MERGE

### Description

Merge the partial worker outputs, resolve conflicts against the previous KB,
enrich entries with session artifacts, and write the consolidated KB and its
manifest.

### Worker

`synthesis_worker`
(`.agents/orchestrators/discovery/roles/workers/synthesis_worker.md`).

### Required Input Artifacts

The intermediate outputs of every discovery state selected by the scope:

```text
.project/<session-uuid>/discovery/worker_environment.json
.project/<session-uuid>/discovery/worker_stack.json
.project/<session-uuid>/discovery/worker_framework.json
.project/<session-uuid>/discovery/worker_patterns.json
.project/<session-uuid>/discovery/worker_business.json
```

plus the previous KB and the session artifacts.

### Required Output Artifacts

```text
.project/knowledge/discovery/executive_summary.md
.project/knowledge/discovery/.discovery_manifest
```

and the consolidated KB entries.

### Allowed Transitions

```text
DISCOVERY_MERGE
    |
    v
DISCOVERY_VALIDATE
```

On unrecoverable failure:

```text
DISCOVERY_MERGE
    |
    v
DISCOVERY_FAILED
```

---

## DISCOVERY_VALIDATE

### Description

Validate the merged KB before publishing it:

* `D01-discovery-output` validates the KB structure and ground truth
  (`.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`).

### Required Input Artifacts

```text
.project/knowledge/discovery/.discovery_manifest
```

and the consolidated KB entries.

### Required Output Artifacts

Validation results are recorded in the session `HARNESS_REPORT.md`.

### Harness

This state's exit transitions are gated by the harness trigger `D01`.

### Allowed Transitions

If the validation passes:

```text
DISCOVERY_VALIDATE
    |
    v
DISCOVERY_READY
```

If validation fails and cannot be recovered:

```text
DISCOVERY_VALIDATE
    |
    v
DISCOVERY_FAILED
```

If validation fails with recoverable findings (inconsistent or incomplete merge):

```text
DISCOVERY_VALIDATE
    |
    v
DISCOVERY_MERGE
```

---

## DISCOVERY_READY

### Description

The KB is updated and valid. Terminal state. The Discovery Orchestrator
returns control to the core Orchestrator with status `DISCOVERY_READY`.

On entering this state, the Discovery Orchestrator writes the marker file
`.project/.last_discovery` (see "Invocation Conditions" below).

### Required Input Artifacts

```text
.project/knowledge/discovery/.discovery_manifest
```

### Allowed Transitions

No transitions. Terminal state.

---

## DISCOVERY_FAILED

### Description

The discovery run failed. Terminal state until retried. The Discovery
Orchestrator reports the failure to the core Orchestrator with status
`DISCOVERY_FAILED`; the core Orchestrator decides whether to abort the task,
route to `core:RECOVERY`, or continue with a minimal discovery.

### Allowed Transitions

A new discovery attempt re-enters the machine:

```text
DISCOVERY_FAILED
    |
    v
DISCOVERY_INIT
```

---

# Invocation Conditions

The core Orchestrator detects a discovery need when:

1. `.project/knowledge/discovery/` does not exist.
2. `.last_discovery` exceeds the project TTL (24h).
3. The hash of the configuration files changed.
4. The hash of the code sample changed.
5. The user requested an explicit refresh.
6. An execution worker reports an inconsistency.
7. The environment TTL (6h) expired and the scope is `env`.

Detection does not imply invocation: with `discovery_require_consent` enabled
(default), a detected need produces a consent consultation with the user (see
`.agents/orchestrators/core/roles/orchestrator.md` §"4.3 Discovery Orchestrator
Invocation"); the Discovery Orchestrator is invoked only after explicit
consent or via the user-invoked `/discovery` skill. In a non-interactive
session discovery is not invoked. With `discovery_require_consent = false`,
detection invokes directly (legacy automatic behavior).

## The `.last_discovery` marker

`.project/.last_discovery` is a small JSON file written by the Discovery
Orchestrator when a run reaches `DISCOVERY_READY`. It is the discovery
equivalent of `.project/.last_health_check` and drives condition 2 (and the
TTL checks of condition 7). It is the **only** discovery marker: the legacy
marker at `.project/knowledge/discovery/.last_discovery` is deprecated and
MUST be removed when found (the canonical file prevails on any conflict).
Shape:

```json
{
  "timestamp": "<ISO-8601 UTC>",
  "scope": "full|lite|env|stack|patterns|business",
  "status": "DISCOVERY_READY"
}
```

If the file is missing or unparsable, the core Orchestrator treats the TTL as
expired (i.e., a discovery need is detected).

# Scopes

| Scope | Workers invoked | Use |
|-------|-----------------|-----|
| `full` | All | First run or major change. |
| `lite` | `init_worker`, `environment_worker`, `stack_worker`, `framework_worker`, `synthesis_worker` | Environment, language, stack and architecture, without deep qualitative analysis. |
| `env` | `init_worker`, `environment_worker`, `synthesis_worker` | Tooling change. |
| `stack` | `init_worker`, `stack_worker`, `framework_worker`, `synthesis_worker` | New dependencies. |
| `patterns` | `init_worker`, `patterns_worker`, `synthesis_worker` | Convention change. |
| `business` | `init_worker`, `business_worker`, `synthesis_worker` | Business logic change. |

# Hash Calculation

The `init_worker` computes the hashes as part of its task and records them in
`discovery_input.json` and in the manifest's `[hashes]` section. The core
Orchestrator only requests the scope and receives the result; it never
computes hashes itself. The hashes are:

1. **Config files hash:** SHA-256 of the relevant configuration files in
   deterministic order.
2. **Sample files hash:** SHA-256 of the selected code sample.
3. **Environment hash:** SHA-256 of the environment probe results.

The `init_worker` uses these hashes to determine invalidations and records them
in `invalidation_report.json`.

# TTL and Cache

| Aspect | TTL | Detail |
|--------|-----|--------|
| Project | 24h | Re-invoke the whole pipeline on change. |
| Environment | 6h | Re-invoke only `environment.md`. |
| Stack | 24h | Re-invoke `stack_worker` + `framework_worker` if the config hash changed. |
| Patterns | 24h | Re-invoke `patterns_worker` if the code sample changed. |
| Business | 24h | Re-invoke `business_worker` if the README or main services changed. |

The TTL values are configured in `.agents/features.toml`
(`discovery_project_ttl_hours`, `discovery_environment_ttl_hours`).

# Freshness Rule

KB entries are consumed only while fresh. Before delegating any phase that
consumes `environment.md` or `development_patterns.md`, the Orchestrator
verifies the entry's freshness against its TTL (via `.last_discovery` and the
manifest's provenance fields). An expired entry is marked `[entries] stale`
in the manifest, is excluded from recommendations, and is revalidated through
the pipeline (scope `env` or the corresponding scope) before the delegation.
KB entries are updated **only** through the discovery pipeline: manual edits
are recorded as deviations and trigger `init_worker` for formal revalidation.

---

## Protocol boundaries

Artifact locations, project boundaries, immutability rules, and agent autonomy
rules are defined in:

→ `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`
