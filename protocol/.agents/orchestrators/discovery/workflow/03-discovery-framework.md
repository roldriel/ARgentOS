---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_FRAMEWORK
lifecycle: discovery
previous_states: [discovery:DISCOVERY_STACK]
next_states: [discovery:DISCOVERY_MERGE, discovery:DISCOVERY_FAILED]
input_artifacts: [worker_stack.json]
output_artifacts: [worker_framework.json, architecture.md, configuration.md, entrypoint.md, api.md]
harness: []
actor: discovery_orchestrator
profile: framework_worker
---

# Discovery Framework

## Purpose

Detect the framework architecture and configuration of the project, based on
the stack detected in `DISCOVERY_STACK`.

This module must not:

* Modify project source files.
* Run before the stack output is available.
* Exceed the `context_budget` and `sample_size` bounds of the discovery input.

Its only responsibility is producing the framework discovery outputs.

---

# State

## Required Initial State

```text
DISCOVERY_STACK
```

The Discovery Orchestrator enters this module when the invocation scope is
`full` or `stack`, after `stack_worker` produced its output.

---

## Input Artifacts

```text
.project/<session-uuid>/discovery/worker_stack.json
```

plus the `project_shape` recorded in `discovery_input.json` (it drives the
content variant of `entrypoint.md` and `api.md`) and the project configuration
files referenced by the stack output.

---

## Possible Output States

### DISCOVERY_MERGE

The framework was detected and the output is ready for synthesis.

---

### DISCOVERY_FAILED

The framework could not be detected and the failure is unrecoverable.

---

# Procedure

1. Delegate to the `framework_worker` profile.
2. Detect the framework, the architecture and the configuration of the project.
3. Write the intermediate output `.project/<session-uuid>/discovery/worker_framework.json`
   according to `.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`.
4. Write the knowledge-base entries `architecture.md`, `configuration.md`,
   `entrypoint.md` and `api.md` under `.project/knowledge/discovery/`.

---

# Output Artifacts

```text
.project/<session-uuid>/discovery/worker_framework.json
.project/knowledge/discovery/architecture.md
.project/knowledge/discovery/configuration.md
.project/knowledge/discovery/entrypoint.md
.project/knowledge/discovery/api.md
```

---

# Harness

This module has no exit gate. The merged output is validated later in
`DISCOVERY_VALIDATE` (`D01`).
