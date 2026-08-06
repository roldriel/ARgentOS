+++
trigger = "H02"
transition = "GATHERING_CONTEXT → CONTEXT_GATHERED"
artifact = "CONTEXT_ARTIFACT.md"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H02
name: context-artifact
state: core:GATHERING_CONTEXT
lifecycle: context
gates:
  - "core:GATHERING_CONTEXT -> core:CONTEXT_GATHERED"
artifact_validated: CONTEXT_ARTIFACT.md
---

# Harness Policy H02: Context Artifact

## Trigger

`GATHERING_CONTEXT → CONTEXT_GATHERED`

## Purpose

Validate that `CONTEXT_ARTIFACT.md` exists and captures sufficient technical context before context validation begins.

## Input

- Current state: `GATHERING_CONTEXT`
- Target state: `CONTEXT_GATHERED`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md`
- Contract: `.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md`
- Reference: `TASK_SPECIFICATION.md`

## Checklist

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence, required-section presence, and the EARS/rubric/semantic checks declared in this policy's front matter) or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. The artifact file exists. `[machine]`
2. The artifact identifies the relevant project files and components. `[agent]`
3. The artifact describes the current behavior of the system in the task scope. `[agent]`
4. The artifact lists technical constraints (libraries, frameworks, versions). `[agent]`
5. The artifact notes dependencies and relationships between components. `[agent]`
6. The context is relevant to the task specification. `[agent]`
7. The context does not rely on unstated assumptions. `[agent]`

The presence of the `required_sections` resolved by the runner from the artifact contract is `[machine]` even though it is not restated as a numbered item.

## Decision Criteria

- `PASS`: The artifact exists and the context is sufficient for planning.
- `FAIL`: The artifact is missing, incomplete, or relies on critical unstated assumptions.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `GATHERING_CONTEXT` and re-invoke the Worker as `context_gatherer`, or
3. Transition to `NEEDS_CLARIFICATION` if the missing context requires user input.

## Examples

### PASS examples

1. The artifact names `app/routes/users.py` and `app/services/user_service.py` and explains how each is relevant to adding a user endpoint.
2. The artifact lists Flask 2.3 and SQLAlchemy 2.0 as dependencies and notes that the project uses an in-memory SQLite database for tests.
3. Every section links back to a requirement in `TASK_SPECIFICATION.md`; no new assumptions are introduced.

### FAIL examples

1. The artifact describes "the backend" generically without naming any files, modules, or classes.
2. The artifact states that "the database already enforces uniqueness" without providing evidence or a schema reference.
3. The artifact describes dependencies that were not found in the project files.

### Yes/no questions for the evaluator

1. Does the context name at least one relevant file?
2. Does the context contain no unstated assumptions?
3. Can every section be linked to a task requirement?
