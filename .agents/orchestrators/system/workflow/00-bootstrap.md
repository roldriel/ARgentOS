---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: system
state: VERIFYING_PROTOCOL_HEALTH
lifecycle: system
previous_states: [system:SYSTEM_INIT, system:BOOTSTRAP_FAILED]
next_states: [system:ENVIRONMENT_READY, system:BOOTSTRAP_FAILED]
input_artifacts: []
output_artifacts: [.project/.last_health_check]
harness: [S00-system-ready]
actor: system_agent
profile: null
---

# System Bootstrap

## Purpose

Prepare and verify the protocol runtime environment before any task session begins.

This module is executed by the ArgentOS System Agent (domain `system`). It must not analyze user tasks, produce task artifacts, or perform any orchestration of the `core` domain.

Its only responsibility is ensuring the protocol environment is healthy and then handing control to the core Orchestrator at `core:SYSTEM_READY`.

---

# State

## Required Initial State

```text
SYSTEM_INIT
```

The agent must enter this module at the start of every session, before loading the core Orchestrator role.

---

## Possible Output States

### ENVIRONMENT_READY

The health check passed and the runtime environment is initialized.

Hand control to the core Orchestrator:

```text
core:SYSTEM_READY
```

The core Orchestrator continues from `SYSTEM_READY` as defined in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`.

---

### BOOTSTRAP_FAILED

The health check failed or the runtime environment could not be initialized.

Report the failing checks to the user and stop. Do not hand control to the core Orchestrator.

---

# Procedure

1. Initialize `.project/` and `.project/knowledge/` (including `INDEX.md` and `entries/`) if missing.
2. Run the protocol health check:

```bash
python .agents/harness/runner.py health-check
```

3. Evaluate the result through harness trigger `S00` (`.agents/orchestrators/system/harness/policies/S00-system-ready.md`).
4. On `PASS`, transition to `ENVIRONMENT_READY` and hand control to the core Orchestrator.
5. On `FAIL`, transition to `BOOTSTRAP_FAILED`, report the failing checks, and stop.

---

# Harness

This module's `VERIFYING_PROTOCOL_HEALTH → ENVIRONMENT_READY` transition is gated by harness trigger `S00` (`.agents/orchestrators/system/harness/policies/S00-system-ready.md`).
