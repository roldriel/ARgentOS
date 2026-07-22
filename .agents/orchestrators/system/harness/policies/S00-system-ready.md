+++
trigger = "S00"
transition = "VERIFYING_PROTOCOL_HEALTH → ENVIRONMENT_READY"
artifact = ".project/.last_health_check"
required_sections = []
+++

# Harness Policy S00: System Ready

## Trigger

`VERIFYING_PROTOCOL_HEALTH → ENVIRONMENT_READY` (domain `system`)

## Purpose

Validate that the protocol runtime environment is healthy before the System Agent hands control to the core Orchestrator at `core:SYSTEM_READY`.

## Input

- Current state: `VERIFYING_PROTOCOL_HEALTH`
- Target state: `ENVIRONMENT_READY`
- Evidence: output of `python .agents/harness/runner.py health-check`
- Timestamp file: `.project/.last_health_check`

## Checklist

1. `python .agents/harness/runner.py health-check` exits with code `0` and reports `"result": "PASS"`.
2. `.project/.last_health_check` exists and its timestamp is within the configured TTL.
3. `.project/knowledge/INDEX.md` and `.project/knowledge/entries/` exist.
4. No required protocol directory reported by the health check is missing.

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: The health check fails, or any required runtime artifact is missing or stale.

## On Failure

The System Agent must:

1. Report the failing checks to the user.
2. Transition to `BOOTSTRAP_FAILED` and stop; control MUST NOT be handed to the core Orchestrator.
