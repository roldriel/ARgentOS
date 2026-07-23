---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_STACK
lifecycle: discovery
previous_states: [discovery:DISCOVERY_RUNNING]
next_states: [discovery:DISCOVERY_FRAMEWORK, discovery:DISCOVERY_FAILED]
input_artifacts: [discovery_input.json]
output_artifacts: [worker_stack.json]
harness: []
actor: discovery_orchestrator
profile: stack_worker
---

# Discovery Stack

## Purpose

Detect the technology stack of the project: languages, dependencies,
containers and databases.

This module must not:

* Modify project source files.
* Infer technologies without evidence in configuration files.
* Exceed the `context_budget` and `sample_size` bounds of the discovery input.

Its only responsibility is producing the stack discovery outputs.

---

# State

## Required Initial State

```text
DISCOVERY_RUNNING
```

The Discovery Orchestrator enters this module when the invocation scope is
`full` or `stack`, after `DISCOVERY_INIT` produced the structured input.

---

## Input Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
```

---

## Possible Output States

### DISCOVERY_FRAMEWORK

The stack was detected; framework detection may proceed, since it depends on
the stack output.

---

### DISCOVERY_FAILED

The stack could not be detected and the failure is unrecoverable.

---

# Procedure

1. Delegate to the `stack_worker` profile.
2. Detect languages, dependencies, containers and databases from the project
   configuration files, applying the sampling rules.
3. Write the intermediate output `.project/<session-uuid>/discovery/worker_stack.json`
   according to `.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`.
4. Write the knowledge-base entries `stack.md`, `dependencies.md`,
   `containers.md` and `database.md` under `.project/knowledge/discovery/`.

---

# Output Artifacts

```text
.project/<session-uuid>/discovery/worker_stack.json
.project/knowledge/discovery/stack.md
.project/knowledge/discovery/dependencies.md
.project/knowledge/discovery/containers.md
.project/knowledge/discovery/database.md
```

---

# Harness

This module has no exit gate. The merged output is validated later in
`DISCOVERY_VALIDATE` (`D01`).
