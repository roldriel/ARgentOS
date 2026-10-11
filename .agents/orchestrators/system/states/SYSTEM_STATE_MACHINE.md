---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: state_machine
domain: system
actor: system_agent
states_defined:
  - SYSTEM_INIT
  - VERIFYING_PROTOCOL_HEALTH
  - ENVIRONMENT_READY
  - BOOTSTRAP_FAILED
---

# System State Machine

## Purpose

Define the lifecycle states of the ArgentOS System Agent bootstrap (domain `system`) and the allowed transitions between them.

The System Agent must not hand control to the core Orchestrator until the protocol runtime environment is verified as healthy.

States in this file belong to the `system` domain. The final transition **hands control to `core:SYSTEM_READY`**, which is and remains a state of the `core` domain, defined in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`. The `system` domain does NOT redefine `SYSTEM_READY`.

---

# Core Rules

- Every transition must be justified by a verifiable condition of the runtime environment, not by the agent's confidence.
- If the environment cannot be verified, the System Agent reports the failure and stops. The canonical blocking rule and its only exception are defined under `BOOTSTRAP_FAILED` below.
- The bootstrap workflow is documented in `.agents/orchestrators/system/workflow/00-bootstrap.md`.

---

## SYSTEM_INIT

### Description

The ArgentOS System Agent role has been loaded and the protocol bootstrap has started.

No verification has been performed yet.

### Required Action

- Load the system role: `.agents/orchestrators/system/roles/argentos.md`.

### Allowed Transition

```text
SYSTEM_INIT
        |
        v
VERIFYING_PROTOCOL_HEALTH
```

---

## VERIFYING_PROTOCOL_HEALTH

### Description

The System Agent verifies protocol health and prepares the runtime environment.

### Required Action

- Initialize `.project/` and `.project/knowledge/` if missing.
- Apply the protocol health checklist (`.agents/standards/runtime/PROTOCOL_HEALTH.md`) and run the state-storage probe (`python .argentos/.agents/harness/health_check.py --project-root <PROJECT_ROOT>`); evaluate the combined result.

### Allowed Transitions

```text
VERIFYING_PROTOCOL_HEALTH
        |
        v
ENVIRONMENT_READY            (protocol health PASS)

VERIFYING_PROTOCOL_HEALTH
        |
        v
BOOTSTRAP_FAILED             (protocol health FAIL)
```

The `VERIFYING_PROTOCOL_HEALTH → ENVIRONMENT_READY` transition is gated by harness trigger `S00` (`.agents/orchestrators/system/harness/policies/S00-system-ready.md`).

---

## ENVIRONMENT_READY

### Description

The protocol health verification passed and the runtime environment is initialized.

### Allowed Transition

```text
ENVIRONMENT_READY
        |
        v
core:SYSTEM_READY            (hand control to the core Orchestrator)
```

On this transition the System Agent hands control to the core Orchestrator, which continues from `SYSTEM_READY` as defined in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`.

---

## BOOTSTRAP_FAILED

### Description

The protocol health verification failed or the runtime environment could not be initialized.

### Required Action

- Report the failing checks to the user.
- Do NOT hand control to the core Orchestrator.

**Canonical rule:** a protocol health `FAIL` blocks the handoff to the core Orchestrator; the only exception is explicit user authorization, recorded in `SESSION_LOG.md`. Every other protocol document that covers this situation (policy `S00`, the bootstrap workflow, the Orchestrator role) references this rule as stated here, without reformulating it.

### Allowed Transition

```text
BOOTSTRAP_FAILED
        |
        v
VERIFYING_PROTOCOL_HEALTH    (after the environment is repaired)
```
