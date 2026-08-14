+++
schema_version = "1.0.0"
artifact = "SESSION_BRIEF.md"
phase = "all"
produced_by = "orchestrator"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: cross-cutting
artifact: SESSION_BRIEF.md
lifecycle: null
produced_by: [core:TASK_RECEIVED]
consumed_by: [core:ANALYZING_TASK, core:CONFIRMING_INTENT]
---

# Session Brief Contract

## Purpose

Define the structure of `SESSION_BRIEF.md`, an ephemeral artifact that accumulates the confirmed intent, clarifications, constraints, and open unknowns of the current session. It acts as short-term memory for the conversation, complementing the long-term Knowledge Base.

## Relationship to Knowledge Base

`SESSION_BRIEF.md` is **not** a replacement for the Knowledge Base (`.project/knowledge/`). The Knowledge Base stores reusable lessons learned across sessions. `SESSION_BRIEF.md` stores the agreed-upon context of the current session only.

## Location

```text
.project/<session-uuid>/SESSION_BRIEF.md
```

It must never be written inside `.project/knowledge/`.

## Structure

```toml
constraints = [""]
open_unknowns = [""]

[metadata]
id = ""
created_at = ""
updated_at = ""
session = ""

[confirmed_intent]
summary = ""
reflected_in = ""

[[clarifications]]
question = ""
answer = ""
source = ""
```

`source` records where the answer came from: `user` for a direct user answer, or `unattended_default` for a default applied under unattended mode (such entries stay `PENDING_USER_CONFIRMATION` until the user reviews them).

## Sections

### Metadata

Identification and timestamps.

### Confirmed Intent

Summary of what the user wants, with a reference to the `INTENT_REFLECTION.md` artifact that confirmed it.

### Clarifications

List of question/answer pairs obtained through `NEEDS_CLARIFICATION`.

### Constraints

Fixed rules or limitations accepted during the session.

### Open Unknowns

Information still missing that may block execution.

## Lifecycle

- Created during `CONFIRMING_INTENT` when the user confirms intent.
- Updated during `BUILDING_TASK_SPECIFICATION` when ambiguities are resolved.
- Updated during `NEEDS_CLARIFICATION` when new answers are received.
- Read by `task_analyst` when re-entering `ANALYZING_TASK`.

## Completion Criteria

The session brief is valid when:

* It contains a `metadata` section.
* It contains a `confirmed_intent` section after intent confirmation.
* It is stored in the correct session directory.
* It does not contain sensitive or user-specific data intended only for the current task.
