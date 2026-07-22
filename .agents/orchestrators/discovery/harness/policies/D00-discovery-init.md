+++
trigger = "D00"
transition = "DISCOVERY_INIT → DISCOVERY_RUNNING"
artifact = "KB_DISCOVERY_REPORT.md"
required_sections = []
+++

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

1. The discovery report artifact file exists.
2. The artifact complies with the contract in `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md`.
3. Each discovery entry referenced by the report complies with `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`.
4. The discovery scope and inputs used for the run are recorded in the artifact.

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: The artifact is missing, invalid, or does not record the discovery scope.

## On Failure

The Discovery Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `DISCOVERY_INIT` and re-run the initialization, or
3. Transition to `NEEDS_CLARIFICATION` if the discovery request cannot be initialized without user input.
