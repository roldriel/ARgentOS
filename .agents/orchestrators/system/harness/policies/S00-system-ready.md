+++
trigger = "S00"
transition = "VERIFYING_PROTOCOL_HEALTH → ENVIRONMENT_READY"
artifact = ".project/.last_health_check"
required_sections = []
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: system
harness_id: S00
name: system-ready
state: system:VERIFYING_PROTOCOL_HEALTH
lifecycle: system
gates:
  - "system:VERIFYING_PROTOCOL_HEALTH -> system:ENVIRONMENT_READY"
artifact_validated: .project/.last_health_check
---

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

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the health-check command itself (its exit code and JSON output) or by the harness runner — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. `python .agents/harness/runner.py health-check` exits with code `0` and reports `"result": "PASS"`. `[machine]`
2. `.project/.last_health_check` exists and its timestamp is within the configured TTL. `[machine]`
3. `.project/knowledge/INDEX.md` and `.project/knowledge/entries/` exist. `[machine]` (verified by the health check)
4. No required protocol directory reported by the health check is missing. `[machine]`

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: The health check fails, or any required runtime artifact is missing or stale.

## On Failure

The System Agent must:

1. Report the failing checks to the user.
2. Transition to `BOOTSTRAP_FAILED` and stop. The blocking rule and its only exception are those defined in `.agents/orchestrators/system/states/SYSTEM_STATE_MACHINE.md` (`BOOTSTRAP_FAILED`, canonical rule).
