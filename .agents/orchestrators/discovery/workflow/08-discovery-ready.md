---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_READY
lifecycle: discovery
previous_states: [discovery:DISCOVERY_VALIDATE]
next_states: []
input_artifacts: [DISCOVERY_MANIFEST.md]
output_artifacts: []
harness: []
actor: discovery_orchestrator
profile: null
---

# Discovery Ready

## Purpose

Publish the validated knowledge base and return control to the core
Orchestrator with status `discovery:DISCOVERY_READY`.

This module must not:

* Modify project source files.
* Modify the KB after validation.
* Respond to the user or produce session artifacts of the task; the core
  Orchestrator is the only role that governs the task lifecycle.

---

# State

## Required Initial State

```text
DISCOVERY_VALIDATE
```

`D01` must have passed before entering this module.

---

## Input Artifacts

```text
.project/knowledge/discovery/.discovery_manifest
```

---

## Possible Output States

`DISCOVERY_READY` is a terminal state. There are no further transitions
inside the discovery domain.

---

# Procedure

1. Confirm the manifest and the consolidated KB entries are in place under
   `.project/knowledge/discovery/`.
2. Return the structured result to the core Orchestrator:

```json
{
  "status": "DISCOVERY_READY",
  "knowledge_base_path": ".project/knowledge/discovery/",
  "manifest": ".project/knowledge/discovery/.discovery_manifest",
  "harness_report": ".project/<session-uuid>/HARNESS_REPORT.md"
}
```

The core Orchestrator then continues its own state machine
(`core:PLANNING → core:EXECUTING → core:VERIFYING → core:COMPLETED`) with the
KB available for `core:GATHERING_CONTEXT`, `core:PLANNING` and
`core:EXECUTING`.

---

# Harness

This module has no harness gate; entry into `DISCOVERY_READY` was already
gated by `D01` in `DISCOVERY_VALIDATE`.
