---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_PATTERNS
lifecycle: discovery
previous_states: [discovery:DISCOVERY_RUNNING]
next_states: [discovery:DISCOVERY_MERGE, discovery:DISCOVERY_FAILED]
input_artifacts: [discovery_input.json]
output_artifacts: [worker_patterns.json, DEVELOPMENT_PATTERNS.md]
harness: []
actor: discovery_orchestrator
profile: patterns_worker
---

# Discovery Patterns

## Purpose

Detect the code and style patterns of the project: conventions, idioms and
team habits, with verifiable examples.

This module must not:

* Modify project source files.
* Assert patterns without `source_files` evidence.
* Exceed the `context_budget` and `sample_size` bounds of the discovery input.

Its only responsibility is producing the development patterns entry.

---

# State

## Required Initial State

```text
DISCOVERY_RUNNING
```

The Discovery Orchestrator enters this module when the invocation scope is
`full` or `patterns`, after `DISCOVERY_INIT` produced the structured input.

---

## Input Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
```

plus the code sample selected by `init_worker`.

---

## Possible Output States

### DISCOVERY_MERGE

The patterns were detected and the output is ready for synthesis.

---

### DISCOVERY_FAILED

The patterns could not be detected and the failure is unrecoverable.

---

# Procedure

1. Delegate to the `patterns_worker` profile.
2. Analyze the code sample and any style guides to detect patterns with
   verifiable examples.
3. Write the intermediate output `.project/<session-uuid>/discovery/worker_patterns.json`
   according to `.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`.
4. Write the knowledge-base entry `.project/knowledge/discovery/development_patterns.md`
   according to `.agents/orchestrators/discovery/contracts/DEVELOPMENT_PATTERNS.md`.

---

# Output Artifacts

```text
.project/<session-uuid>/discovery/worker_patterns.json
.project/knowledge/discovery/development_patterns.md
```

---

# Harness

This module has no exit gate. The merged output is validated later in
`DISCOVERY_VALIDATE` (`core:H10` / `D01`).
