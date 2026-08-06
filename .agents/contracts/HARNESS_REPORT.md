+++
artifact = "HARNESS_REPORT.md"
phase = "all"
produced_by = "harness"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: cross-cutting
artifact: HARNESS_REPORT.md
lifecycle: null
produced_by: [core:TASK_RECEIVED]
consumed_by: [core:RECOVERY, core:COMPLETED, discovery:DISCOVERY_READY]
---

# Contract: Harness Report

## Purpose

`HARNESS_REPORT.md` is the audit trail of the validation harness. It lives at the root of every session (`.project/<session-uuid>/HARNESS_REPORT.md`) and records every harness trigger invocation with its result, evidence, and aggregated metrics. It is written exclusively by the harness runner (`update_report` in `.agents/harness/runner.py`); agents must not edit it by hand.

## Location and ownership

- Path: `.project/<session-uuid>/HARNESS_REPORT.md` (session root, not inside an iteration folder).
- Producer: the harness runner, after every trigger evaluation (`PASS` or `FAIL`).
- Consumers: the Orchestrator (recovery and completion decisions), the Discovery Orchestrator (its result payload points to this file), and any audit of the session.

## Required structure

The report is rebuilt from a template on every update. It contains, in this order:

1. **Header**:

   ```markdown
   # Harness Report

   - Session UUID: `<uuid>`
   - Last updated: `<ISO-8601-timestamp>`
   ```

2. **`## Summary`** — one table row per recorded entry:

   ```markdown
   | Trigger | Transition | Result | Timestamp |
   |---|---|---|---|
   ```

3. **`## Entries`** — one subsection per invocation, headed `### <trigger>`, with the fields:

   - `Transition`: the gated transition (for example `EXECUTING → VERIFYING`).
   - `Result`: `PASS`, `FAIL`, or `SKIP`. `SKIP` means `skipped: profile`: the gate is not mandatory for the task profile assigned in the session's `TASK_ANALYSIS.md`; the omission is a system decision, not an oversight.
   - `Timestamp`: ISO-8601 timestamp of the invocation.
   - `Artifact checked`: present only when the trigger validates an artifact.
   - `Checks`: one bullet per check, formatted as `` `<check-id>`: <result> — <evidence> ``. A skipped gate records a single check `gate_required_for_profile` with result `SKIP` and evidence `skipped: profile — …`.
   - `Alert` (optional): one `- Alert: <message>` line per post-hoc audit alert (for example, a suspected enforcement-hook bypass detected by the runner when files were modified before the plan gate PASS). Alerts never change the gate result.

   Each entry ends with a machine-readable HTML comment so the runner can preserve history across updates:

   ```markdown
   <!-- ENTRY: {"timestamp": "...", "trigger": "...", "transition": "...", "result": "...", "checks": [{"id": "...", "result": "...", "evidence": "..."}], "artifact": "...", "duration_ms": 0, "rubric_scores": {...}, "alerts": [...]} -->
   ```

   The `alerts` array is optional (absent or empty when no alert was raised).

   These `ENTRY` comments are part of the contract: they must remain valid JSON and must not be removed or edited.

4. **`## Metrics`** — aggregated per trigger across all entries. `SKIP` entries count toward `Invocations` but toward neither `PASS` nor `FAIL`:

   ```markdown
   | Trigger | Invocations | PASS | FAIL | Avg Duration (ms) |
   |---|---|---|---|---|
   ```

5. **`## Rubric Scores`** (optional) — present only when the latest entry carries `rubric_scores`; one bullet per rubric: `- <rubric>: <score>`.

6. **`## Final Decision`** — the result and trigger of the most recent invocation:

   ```markdown
   - Last result: `<PASS|FAIL|SKIP>`
   - Last trigger: `<trigger-id>`
   ```

## Constraints

- Only the harness runner may write or rewrite this file; entries are append-only in effect (the runner rebuilds the report preserving previous `ENTRY` comments).
- Every harness invocation in a session must appear exactly once in `## Entries` and `## Summary`.
- The report must not include credentials, tokens, or personal data.
- Failures recorded here feed the recovery flow described in `.agents/harness/INDEX.md`.
- The `ENTRY` comments are the trigger data points of the protocol metrics model (`.agents/standards/runtime/PROTOCOL_METRICS.md`); the runner `metrics` subcommand reads them for aggregation.
