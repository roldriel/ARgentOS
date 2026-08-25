+++
schema_version = "1.1.0"
artifact = "SESSION_LOG.md"
phase = "all"
produced_by = "orchestrator"
enforcement = "informational"
+++
schema_version = "1.1.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: cross-cutting
artifact: SESSION_LOG.md
lifecycle: null
produced_by: [core:TASK_RECEIVED]
consumed_by: [core:COMPLETED, core:RECOVERY]
---

# Contract: Session Log

## Purpose

`SESSION_LOG.md` is maintained by the Orchestrator at the root of every session. It records the lifecycle of the session for auditability and as input for future Knowledge Base entries.

## Required content

The log must contain one entry per significant event, typically under a `## <ISO-8601-timestamp>` heading.

Each entry should include as many of the following fields as applicable:

- **State transition**: source state → target state.
- **Trigger**: harness trigger executed, if any.
- **Harness result**: `PASS` or `FAIL`.
- **Worker**: role adopted by the worker.
- **Knowledge entries consulted**: UUIDs of KB entries used, or `none`.
- **Decision**: orchestrator decision (`proceed`, `retry`, `recovery`, `needs_clarification`, `abort`).
- **Evidence** (optional): citation of an artifact path or of another entry in
  this log that supports the recorded decision, bypass or applied default
  (claims rule of `.agents/harness/INDEX.md`, §Enforcement boundaries: every
  claim is evidence-cited or explicitly marked as attestation/inference).
- **Pending confirmation**: any default applied under unattended mode is recorded as `PENDING_USER_CONFIRMATION` with the ambiguity, the applied default, and the policy entry that covered it.
- **Feature flags active**: list of enabled feature flags at session start.

## Initial entry template

At session start, the Orchestrator MUST create `SESSION_LOG.md` with a header block and an initial entry:

```markdown
# Session Log

- Session UUID: `<uuid>`
- Created: `<ISO-8601-timestamp>`
- Protocol version: `<X.Y.Z>` (`.agents/VERSION` at session start)
- Delegation mode: `subagent` | `single-instance` (see orchestrator's delegation execution modes)
- Active feature flags: <comma-separated list or `all enabled`>

## <ISO-8601-timestamp>

- **Event**: session started
- **State transition**: SYSTEM_READY → TASK_RECEIVED
- **Feature flags active**: <list>
- **Health-check status**: <PASS/FAIL and timestamp>
- **Decision**: proceed to task analysis
```

## Example entry

```markdown
## 2026-07-08T20:15:00Z

- **State transition**: `BUILDING_TASK_SPECIFICATION` → `TASK_READY`
- **Trigger**: H01
- **Harness result**: PASS
- **Worker**: task_specification_writer
- **Knowledge entries consulted**: none
- **Decision**: proceed to context gathering
```

## Constraints

- The Orchestrator must write the initial entry at session start, including the active feature flags.
- The Orchestrator must record every harness invocation and worker delegation.
- The log must not include credentials, tokens, or personal data.
- The Orchestrator must not retroactively rewrite the log to hide skipped phases or failed transitions. If a phase was skipped, the log must note the deviation explicitly.
