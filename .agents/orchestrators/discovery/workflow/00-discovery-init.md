---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_INIT
lifecycle: discovery
previous_states: []
next_states: [discovery:DISCOVERY_RUNNING, discovery:DISCOVERY_FAILED]
input_artifacts: []
output_artifacts: [KB_DISCOVERY_REPORT.md]
harness: [D00-discovery-init]
actor: discovery_orchestrator
profile: init_worker
---

# Discovery Init

## Purpose

Initialize a discovery session for the `discovery` domain.

This module is responsible for starting the knowledge-base discovery flow: verifying that discovery inputs are available and producing the initial discovery report. It must not synthesize knowledge-base entries or modify project files beyond the session artifacts.

This module must not:

* Implement solutions.
* Modify project source files.
* Perform task orchestration of the `core` domain.

Its only responsibility is initializing the discovery run and recording its outcome in the discovery report artifact.

---

# State

## Required Initial State

```text
DISCOVERY_INIT
```

The Discovery Orchestrator enters this module when a discovery run is requested and no discovery session is active.

---

## Possible Output States

### DISCOVERY_RUNNING

The discovery session was initialized and the run may proceed.

---

### NEEDS_CLARIFICATION

The discovery request is missing critical information (scope, target, or required inputs).

The agent must request additional information from the user.

---

# Procedure

1. Verify the discovery request scope and required inputs.
2. Produce the discovery report artifact according to `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md`.
3. Evaluate harness trigger `D00` (`.agents/orchestrators/discovery/harness/policies/D00-discovery-init.md`) before leaving `DISCOVERY_INIT`.

---

# Harness

This module's exit transition is gated by harness trigger `D00` (`.agents/orchestrators/discovery/harness/policies/D00-discovery-init.md`).
