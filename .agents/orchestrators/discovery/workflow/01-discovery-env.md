---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_ENV
lifecycle: discovery
previous_states: [discovery:DISCOVERY_RUNNING]
next_states: [discovery:DISCOVERY_MERGE, discovery:DISCOVERY_FAILED]
input_artifacts: [discovery_input.json]
output_artifacts: [worker_environment.json, environment.md]
harness: []
actor: discovery_orchestrator
profile: environment_worker
---

# Discovery Env

## Purpose

Detect the execution environment of the project (OS, shell, tools, runtime)
and record it in the discovery knowledge base.

This module must not:

* Modify project source files.
* Execute arbitrary commands beyond the probe defined in
  `.agents/standards/context/ENVIRONMENT_PROBE.md`.
* Expose secrets or sensitive values in its outputs.

Its only responsibility is producing the environment discovery entry.

---

# State

## Required Initial State

```text
DISCOVERY_RUNNING
```

The Discovery Orchestrator enters this module when the invocation scope is
`full` or `env`, after `DISCOVERY_INIT` produced the structured input.

---

## Input Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
```

---

## Possible Output States

### DISCOVERY_MERGE

The environment was detected and the output is ready for synthesis.

---

### DISCOVERY_FAILED

The environment could not be detected and the failure is unrecoverable.

---

# Procedure

1. Delegate to the `environment_worker` profile.
2. Probe the environment according to `.agents/standards/context/ENVIRONMENT_PROBE.md`.
3. Write the intermediate output `.project/<session-uuid>/discovery/worker_environment.json`
   according to `.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`.
4. Write the knowledge-base entry `.project/knowledge/discovery/environment.md`
   according to `.agents/orchestrators/discovery/contracts/ENVIRONMENT_DISCOVERY.md`.

---

# Output Artifacts

```text
.project/<session-uuid>/discovery/worker_environment.json
.project/knowledge/discovery/environment.md
```

---

# Harness

This module has no exit gate. The merged output is validated later in
`DISCOVERY_VALIDATE` (`D01`).
