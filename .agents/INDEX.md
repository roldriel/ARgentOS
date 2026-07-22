# Agent Bootstrap

This repository uses a state-based work protocol governed by an **orchestrator** role.

The human- and agent-facing entry point is `AGENTS.md` at the project root. This document is the protocol bootstrap; it states the loading sequence and points to the canonical rule files.

## Before executing any task

1. Load the system role:
   → `orchestrators/system/roles/argentos.md`

2. The **ArgentOS** system agent verifies protocol health and initializes `.project/` (including `.project/knowledge/`).

3. Load the state machine:
   → `orchestrators/core/states/AGENT_STATE_MACHINE.md`

4. Load the orchestrator role:
   → `orchestrators/core/roles/orchestrator.md`

5. The orchestrator will delegate each workflow phase to a **worker** invoked as a subagent.

Do not execute actions outside the permitted state.

The orchestrator is the only role authorized to:

- Change state.
- Trigger the validation harness.
- Decide whether to continue, request clarification, or enter recovery.

---

## Single-source documentation policy

Protocol rules live in exactly one canonical file. Other files summarize or link; they do not duplicate full explanations, examples, or checklists.

For the canonical boundaries of the protocol (artifact locations, immutability rules, and agent autonomy), see:

→ `standards/runtime/PROTOCOL_BOUNDARIES.md`

## Standards

Cross-cutting rules are organized in `standards/`. See the full map at:

→ `standards/INDEX.md`

## Harness

Validation triggers, runner usage, and recovery are documented in:

→ `harness/INDEX.md`
