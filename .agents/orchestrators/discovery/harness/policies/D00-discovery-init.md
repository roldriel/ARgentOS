+++
trigger = "D00"
transition = "DISCOVERY_INIT → DISCOVERY_RUNNING"
artifact = "KB_DISCOVERY_REPORT.md"
required_sections = []
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: discovery
harness_id: D00
name: discovery-init
state: discovery:DISCOVERY_INIT
lifecycle: discovery
gates:
  - "discovery:DISCOVERY_INIT -> discovery:DISCOVERY_RUNNING"
artifact_validated: KB_DISCOVERY_REPORT.md
---

# Harness Policy D00: Discovery Init

## Trigger

`DISCOVERY_INIT → DISCOVERY_RUNNING` (domain `discovery`)

## Purpose

Validate that the discovery session was initialized correctly and that the discovery report artifact complies with its contract before the discovery run proceeds.

## Input

- Current state: `DISCOVERY_INIT`
- Target state: `DISCOVERY_RUNNING`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-KB_DISCOVERY_REPORT.md`
- Contract: `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md`

## Checklist

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence and presence of the `required_sections` declared in this policy's front matter) — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. The discovery report artifact file exists. `[machine]`
2. The artifact complies with the contract in `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md`. `[agent]` (this policy declares no `required_sections` or semantic checks; contract compliance is judged by the agent)
3. Each discovery entry referenced by the report complies with `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`. `[agent]`
4. The discovery scope and inputs used for the run are recorded in the artifact. `[agent]`

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: The artifact is missing, invalid, or does not record the discovery scope.

## On Failure

The Discovery Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `DISCOVERY_INIT` and re-run the initialization, or
3. End the run as `discovery:DISCOVERY_FAILED` and return control to the core Orchestrator if the discovery request cannot be initialized without user input; the core Orchestrator decides the `core:NEEDS_CLARIFICATION` transition.
