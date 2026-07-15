+++
trigger = "H02"
transition = "GATHERING_CONTEXT → CONTEXT_GATHERED"
artifact = "CONTEXT_ARTIFACT.md"
required_sections = [
  "Metadata",
  "Task Reference",
  "Context Objective",
  "Project Context",
  "Relevant Components",
  "Existing Behavior",
  "Dependencies",
  "Constraints Discovered",
  "Available Evidence",
  "Unknowns",
  "Context Validation",
  "State"
]
+++

# Harness Policy H02: Context Artifact

## Trigger

`GATHERING_CONTEXT → CONTEXT_GATHERED`

## Purpose

Validate that `CONTEXT_ARTIFACT.md` exists and captures sufficient technical context before context validation begins.

## Input

- Current state: `GATHERING_CONTEXT`
- Target state: `CONTEXT_GATHERED`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md`
- Contract: `.agents/contracts/CONTEXT_ARTIFACT.md`
- Reference: `TASK_SPECIFICATION.md`

## Checklist

1. The artifact file exists.
2. The artifact identifies the relevant project files and components.
3. The artifact describes the current behavior of the system in the task scope.
4. The artifact lists technical constraints (libraries, frameworks, versions).
5. The artifact notes dependencies and relationships between components.
6. The context is relevant to the task specification.
7. The context does not rely on unstated assumptions.

## Decision Criteria

- `PASS`: The artifact exists and the context is sufficient for planning.
- `FAIL`: The artifact is missing, incomplete, or relies on critical unstated assumptions.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `GATHERING_CONTEXT` and re-invoke the Worker as `context_gatherer`, or
3. Transition to `NEEDS_CLARIFICATION` if the missing context requires user input.
