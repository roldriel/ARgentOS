# Context Engineering Standard

This document defines how the Orchestrator assembles context for workers in the `.agents` protocol.

## Priority of information

When building a worker payload, the Orchestrator includes context in this order of priority:

1. Task specification for the current session.
2. Previous artifacts produced in the current session.
3. Relevant Knowledge Base entries (summaries only, not full artifacts).
4. The workflow module for the target phase.

## Omission rules

The Orchestrator must never include:

- Full artifacts from previous sessions.
- Logs or reports from other sessions.
- Binary files, credentials, tokens, or personal data.
- Any content that is not directly relevant to the current phase.

## Knowledge Base context budgets

The following budgets limit only the portion of context that comes from `.project/knowledge/`. They do not limit the task specification, current-session artifacts, or workflow module.

| Phase group | Budget (characters) |
|---|---|
| Analysis and context gathering | 8000 |
| Planning, execution, and verification | 4000 |

The `context_discoverer` recommends a budget; the Orchestrator applies it when assembling the final payload.

## Budget distribution

If N entries are selected, each entry receives at most `budget / N` characters, with a minimum of 500 characters per entry. If the budget does not allow at least 500 characters per selected entry, the Orchestrator reduces the number of entries until the minimum is satisfied.

## Selection criteria

A KB entry is relevant when it shares tags, modified files, or objective keywords with the current task. The `context_discoverer` documents the reason for each recommendation in `KB_DISCOVERY_REPORT.md`.

## Session Brief

`.project/<session-uuid>/SESSION_BRIEF.md` is a session-scoped artifact that accumulates confirmed intent, clarifications, constraints, and open unknowns. It is not part of the Knowledge Base and must not be stored in `.project/knowledge/`.

The Orchestrator includes `SESSION_BRIEF.md` in the payload when:

- Re-entering `ANALYZING_TASK` after a clarification or correction.
- Entering `CONFIRMING_INTENT` or `BUILDING_TASK_SPECIFICATION`.

Its purpose is to prevent the agent from re-asking questions that have already been resolved in the same session.

## Session log

The Orchestrator records every context decision in `.project/<session-uuid>/SESSION_LOG.md`, including which KB entries were consulted, whether `SESSION_BRIEF.md` was included, and why.
