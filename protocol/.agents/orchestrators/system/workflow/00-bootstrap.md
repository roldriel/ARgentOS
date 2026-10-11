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

The protocol health verification (checklist + probe) passed and the runtime environment is initialized.

Hand control to the core Orchestrator:

```text
core:SYSTEM_READY
```

The core Orchestrator continues from `SYSTEM_READY` as defined in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`.

---

### BOOTSTRAP_FAILED

The protocol health verification failed or the runtime environment could not be initialized.

Report the failing checks to the user and stop. The blocking rule for the handoff and its only exception are those defined in `.agents/orchestrators/system/states/SYSTEM_STATE_MACHINE.md` (`BOOTSTRAP_FAILED`, canonical rule).

---

# Procedure

1. Initialize `.project/` and `.project/knowledge/` (including `INDEX.md` and `entries/`) if missing.
2. Apply the protocol health checklist of `.agents/standards/runtime/PROTOCOL_HEALTH.md` and run the state-storage probe:

```bash
python .argentos/.agents/harness/health_check.py --project-root <PROJECT_ROOT>
```

3. Evaluate the result through harness trigger `S00` (`.agents/orchestrators/system/harness/policies/S00-system-ready.md`).
4. On `PASS`, transition to `ENVIRONMENT_READY` and hand control to the core Orchestrator.
5. On `FAIL`, transition to `BOOTSTRAP_FAILED` and report the failing checks. The blocking rule and its only exception are those defined in `.agents/orchestrators/system/states/SYSTEM_STATE_MACHINE.md` (`BOOTSTRAP_FAILED`, canonical rule).

---

# Harness

This module's `VERIFYING_PROTOCOL_HEALTH → ENVIRONMENT_READY` transition is gated by harness trigger `S00` (`.agents/orchestrators/system/harness/policies/S00-system-ready.md`).
