+++
schema_version = "1.1.0"
artifact = "HARNESS_REPORT.md"
phase = "all"
produced_by = "orchestrator"
enforcement = "informational"
+++
schema_version = "1.1.0"


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

`HARNESS_REPORT.md` is the **review trail** of the protocol harness. It lives at the root of every session (`.project/<session-uuid>/HARNESS_REPORT.md`) and records every harness trigger invocation with its result, evidence, and aggregated metrics. It is written by the Orchestrator after every gate evaluation; no other agent edits it. It is self-reported: it records the Orchestrator's judgment (see `.agents/harness/INDEX.md`, §Enforcement model); it is not independently verified evidence.

## Location and ownership

- Path: `.project/<session-uuid>/HARNESS_REPORT.md` (session root, not inside an iteration folder).
- Producer: the Orchestrator, after every trigger evaluation (`PASS` or `FAIL`).
- Consumers: the Orchestrator (recovery and completion decisions), the Discovery Orchestrator (its result payload points to this file), and any audit of the session.
- Version note: the report header records the `protocol_version` in force at session start. Entries are evaluated under that version's harness (runner-evaluated before 2.0.0, prose-judgment from 2.0.0 on) and are immutable records of it.

## Required structure

The report follows a fixed declarative structure that the Orchestrator must respect. It contains, in this order:

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
   - `Checks`: one bullet per check, formatted as `` `<check-id>`: <result> — <evidence> `` with an optional `` `claim_class` `` marker. Every check cites its evidence or declares an explicit `claim_class`: with non-empty `evidence` the implicit class is `verified`; without `evidence`, the check MUST declare `claim_class: attested` or `claim_class: inference` (`verified` requires `evidence`). A skipped gate records a single check `gate_required_for_profile` with result `SKIP`, evidence `skipped: profile — …` and no claim class.
   - `Alert` (optional): one `- Alert: <message>` line per post-hoc audit alert (for example, a suspected enforcement-hook bypass detected by `.agents/harness/runner_state.py` when files were modified before the plan gate PASS). Alerts never change the gate result.

   Each entry ends with a machine-readable HTML comment so history is preserved across updates:

   ```markdown
   <!-- ENTRY: {"timestamp": "...", "clock": "utc", "trigger": "...", "transition": "...", "result": "...", "checks": [{"id": "...", "result": "...", "evidence": "...", "claim_class": "verified"}], "artifact": "...", "duration_ms": 0, "rubric_scores": {...}, "alerts": [...]} -->
   ```

   The `alerts` array is optional (absent or empty when no alert was raised).
   `clock` is optional (`utc` | `agent_clock`): mechanically written records
   default to `utc`; agent-written timestamps produced without a reliable clock
   MUST declare `clock: agent_clock` (G-004). `claim_class` on each check
   (`verified` | `attested` | `inference`) is optional in the JSON only when
   the check carries non-empty `evidence`; a check without `evidence` MUST
   carry an explicit `claim_class` of `attested` or `inference` (G-002/G-003).
   The `deviation` field is optional: when the Orchestrator records a `PASS`
   on a gate whose structural validator returned FAIL, the entry MUST carry a
   `deviation` object `{"cause": "<short reason>", "evidence": "<citation of
   the artifact or session-log entry>"}` (see §"Documented deviations").
   The `recovery` field is optional: when a FAIL routes through a recovery
   decision table, the entry carries `{"variables": {<condition>: <value>},
   "matched_rule": "<action or rule number>", "target_phase": "<module or ->"}`
   (see §"Recovery context").

   These `ENTRY` comments are part of the contract: they must remain valid JSON and must not be removed or edited.

4. **`## Documented deviations`** — the only way a structural FAIL becomes a
   recorded `PASS`; every override carries cause and evidence (see below).

## Documented deviations

A documented deviation is the only way a structural FAIL becomes a recorded
`PASS`: the Orchestrator overrides a structural validator FAIL and records the
override in the gate's `ENTRY` comment as a `deviation` object with a
non-empty `cause` and a non-empty `evidence` (an artifact path or a
session-log entry that supports the override).

Rules:

- A deviation is never silent: every override is recorded in the same entry it
  affects, with cause and evidence.
- A deviation never changes the fail-open behavior of the enforcement hooks
  (`.agents/harness/INDEX.md`, §Enforcement model).
- A deviation is auditable post-hoc: recorded `PASS` entries are recomputed
  against the artifacts and compared with the recorded result.
- `deviation` is optional in every other entry: an entry without it is
  presumed to reflect a structural PASS.

## Recovery context

When a trigger fails and the Orchestrator applies the failed policy's Recovery
Decision Table, the evaluation is recorded in the gate's FAIL entry as an
optional `recovery` object:

```json
{
  "variables": {"artifact_exists": false, "retry_count": 0},
  "matched_rule": "RETRY_WORKER",
  "target_phase": "00-analyze-task.md"
}
```

- `variables`: the conditions evaluated for the table, as derived per
  `.agents/harness/INDEX.md` (§Recovery Mechanism): mechanical conditions from
  the structural validator output or the filesystem, judgment conditions
  recorded with evidence at failure time.
- `matched_rule`: the action of the first matching rule, or `RECOVERY_GENERIC`
  when no rule matches.
- `target_phase`: the workflow module of the destination (or `-` when the
  action is `NEEDS_CLARIFICATION` or `ABORT`).

The object is optional: an entry without it means no recovery table was
applied (for example, a `SKIP` entry or a failure recorded without routing).

5. **`## Metrics`** — aggregated per trigger across all entries. `SKIP` entries count toward `Invocations` but toward neither `PASS` nor `FAIL`:

   ```markdown
   | Trigger | Invocations | PASS | FAIL | Avg Duration (ms) |
   |---|---|---|---|---|
   ```

7. **`## Rubric Scores`** (optional) — present only when the latest entry carries `rubric_scores`; one bullet per rubric: `- <rubric>: <score>`.

8. **`## Final Decision`** — the result and trigger of the most recent invocation:

   ```markdown
   - Last result: `<PASS|FAIL|SKIP>`
   - Last trigger: `<trigger-id>`
   ```

## Constraints

- Only the Orchestrator may write or rewrite this file; entries are append-only in effect (every update preserves the previous `ENTRY` comments).
- Every harness invocation in a session must appear exactly once in `## Entries` and `## Summary`.
- The report must not include credentials, tokens, or personal data.
- Failures recorded here feed the recovery flow described in `.agents/harness/INDEX.md`.
- The `ENTRY` comments are the trigger data points of the protocol metrics model (`.agents/standards/runtime/PROTOCOL_METRICS.md`); the agent-driven aggregation procedure of that standard reads them.
