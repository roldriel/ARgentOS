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
- Evidence: the completed protocol health checklist (`.agents/standards/runtime/PROTOCOL_HEALTH.md`) and the output of `python .agents/harness/health_check.py` (state-storage probe)
- Timestamp file: `.project/.last_health_check`

## Checklist

**Evaluation audience:** the harness runner no longer exists; an item is `[machine]` only when validated deterministically by the state-storage probe (its exit code and JSON output); every other item is `[agent]` — evaluated by agent judgment when applying this policy or the health checklist. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. `python .agents/harness/health_check.py` (state-storage probe) exits with code `0` and reports `"result": "PASS"`. `[machine]`
2. Every `[agent]` item of the protocol health checklist (`.agents/standards/runtime/PROTOCOL_HEALTH.md`) passes: required directories and index files, contract front matter, flag-gated rubrics/KB/technical-practice standards, timestamp sanity. `[agent]`
3. `.project/.last_health_check` exists and its timestamp is within the configured TTL. `[agent]`
4. `.project/knowledge/INDEX.md` and `.project/knowledge/entries/` exist. `[agent]`

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: The probe or the health checklist fails, or any required runtime artifact is missing or stale.

## On Failure

The System Agent must:

1. Report the failing checks to the user.
2. Transition to `BOOTSTRAP_FAILED` and stop. The blocking rule and its only exception are those defined in `.agents/orchestrators/system/states/SYSTEM_STATE_MACHINE.md` (`BOOTSTRAP_FAILED`, canonical rule).
