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

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` are structurally checkable and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.

1. The artifact file exists. `[gate]`
2. The artifact identifies the relevant project files and components. `[agent]`
3. The artifact describes the current behavior of the system in the task scope. `[agent]`
4. The artifact lists technical constraints (libraries, frameworks, versions). `[agent]`
5. The artifact notes dependencies and relationships between components. `[agent]`
6. The context is relevant to the task specification. `[agent]`
7. The context does not rely on unstated assumptions. `[agent]`
8. Every citation in the artifact (`` `path:section` ``, `` `path` §section ``, and TOML citation fields) resolves against the filesystem. `[gate]` (see §"Gate Checklist", item 2)

The presence of the sections required by the artifact contract is `[gate]` even though it is not restated as a numbered item; the Orchestrator verifies it against the contract cited in §"Input".

## Gate Checklist

The Orchestrator evaluates each item below by judgment when the gate fires and MUST cite evidence per item (artifact path, declared value, or broken reference) in `HARNESS_REPORT.md`.

1. Verify that `CONTEXT_ARTIFACT.md` exists in the current iteration directory (`.project/<session-uuid>/<iteration>/`). Cite the resolved artifact path as evidence.
2. Verify that every citation in the artifact resolves against the filesystem. Recognized citation forms: backtick-quoted `` `path:section` ``, backtick-quoted path followed by `§section`, and the string values of the TOML keys `specification` and `execution_plan` inside ` ```toml ` blocks. A citation resolves when its path exists relative to the project root, the session directory, or any of the session's iteration directories; when the target is a `.md` file and the anchor is not numeric-only, the cited section MUST exist as an ATX heading in the target (normalized, case-insensitive comparison). Paths containing `<`/`>` placeholders are skipped. On failure, cite each broken citation (line, path, reason); on success, cite the number of citations verified.

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

## Recovery Decision Table

When H02 fails, the Orchestrator populates the context variables from the session (`artifact_exists`, `context_user_specific`, `retry_count` = retries already attempted for this failure) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `artifact_exists == false` | `RETRY_WORKER` | `03-gather-context.md` | `context_gatherer` | CONTEXT_ARTIFACT.md is missing or incomplete; retry context gatherer. |
| 2 | `context_user_specific == true` | `NEEDS_CLARIFICATION` | — | — | Context depends on user-specific knowledge. |
| 3 | `retry_count >= 1` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Repeated failure after retry; route to generic recovery. |
| 4 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Context artifact validation failed; falling back to generic recovery. |
