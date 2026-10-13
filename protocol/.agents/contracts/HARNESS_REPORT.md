+++
schema_version = "2.0.0"
artifact = "HARNESS_REPORT.md"
phase = "all"
produced_by = "orchestrator"
enforcement = "informational"
+++
schema_version = "2.0.0"


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

## Declared actor provenance

Each entry MAY carry a **declared provenance** block identifying the actor that declares having executed
the work. Minimum fields:

| Field | Meaning |
|---|---|
| `actor` | Identifier of the actor, as declared by the reporting side. |
| `harness` | Name of the harness/agent environment that ran the work. |
| `mechanism` | How the work was executed, as declared (the invocation mechanism). |
| `declared_by` | Who made the declaration. |

The provenance is **declared, not verified**: `enforcement = "informational"` is unchanged, this report
remains **self-reported** and **not independently verified evidence**, and the provenance MUST NOT be
presented as authentication, as an authenticity guarantee, or as an independent verification of the
actor. It records *who declares* having executed the work, and *through which harness and mechanism* —
nothing more.

No `provider`, `model`, `SDK`, `CLI` or concrete invocation implementation is required, recorded or
prescribed by this contract, and naming them is outside its scope. Declared provenance grants no
authority: authority remains where the Protocol already places it — Change authorization in the Change
Governance Artifact, effect authorization in RFC-66.
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
   - `Execution`: the numeric iteration folder (`<iteration>`) of the
     execution; the `execution_id` is shared with `state.json` (the event key
     of the gate is `(session_uuid, iteration, trigger)`).
   - `Timestamp`: ISO-8601 timestamp of the invocation.
   - `Artifact checked`: present only when the trigger validates an artifact.
   - `Checks`: one bullet per check, formatted as `` `<check-id>`: <result> — <evidence> `` with an optional `` `claim_class` `` marker. Every check cites its evidence or declares an explicit `claim_class`: with non-empty `evidence` the implicit class is `verified`; without `evidence`, the check MUST declare `claim_class: attested` or `claim_class: inference` (`verified` requires `evidence`). A skipped gate records a single check `gate_required_for_profile` with result `SKIP`, evidence `skipped: profile — …` and no claim class.
   - `Evidence entries` (optional): when the entry cites structured evidence, an
     `evidence` array at the entry level records one item per supported check:
     `{"class": "...", "claim_id": "<check-id>", "ref": "..."}`, with optional
     `command`/`exit_code` for `measurement` and `actor`/`statement` for
     `attestation`. Classes and sufficiency rules follow
     `.agents/standards/quality/EVIDENCE.md`.
   - `Alert` (optional): one `- Alert: <message>` line per post-hoc audit alert (for example, a suspected enforcement-hook bypass detected by `.agents/harness/runner_state.py` when files were modified before the plan gate PASS). Alerts never change the gate result.

   Each entry ends with a machine-readable HTML comment so history is preserved across updates:

   ```markdown
   <!-- ENTRY: {"timestamp": "...", "clock": "utc", "iteration": "<N>", "trigger": "...", "transition": "...", "result": "...", "checks": [{"id": "...", "result": "...", "evidence": "...", "claim_class": "verified"}], "evidence": [{"class": "reference", "claim_id": "<check-id>", "ref": "..."}], "artifact": "...", "duration_ms": 0, "rubric_scores": {...}, "alerts": [...]} -->
   ```

   The `alerts` array is optional (absent or empty when no alert was raised).
   `iteration` and `clock` are required on every ENTRY: `iteration` is the
   numeric iteration folder of the execution (string) and `clock` is `utc` |
   `agent_clock` — mechanically written records default to `utc`;
   agent-written timestamps produced without a reliable clock MUST declare
   `clock: agent_clock` (G-004). `timestamp` is the `event_ts` of the trail
   (the registration moment); the canonical `gate_ts` of a transition gate
   lives in `state.json`. When `event_ts` differs from the `gate_ts` of the
   same gate, the ENTRY MUST declare the divergence with its cause:
   `"timestamp_divergence": {"cause": "<reason>"}` (TR-002).
   `claim_class` on each check
   (`verified` | `attested` | `inference`) is optional in the JSON only when
   the check carries non-empty `evidence`; a check without `evidence` MUST
   carry an explicit `claim_class` of `attested` or `inference` (G-002/G-003).
   A check with `claim_class: verified` (or with non-empty `evidence`, which
   implies `verified`) requires at least one item in the entry's `evidence`
   array whose `claim_id` equals the check id and whose `class` is other than
   `attestation` (EV-004); a check supported only by `attestation` items MUST
   declare `claim_class: attested`.
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
- The deviation `evidence` is a `reference` citation (an artifact path or a
  session-log entry), never an unmarked attestation of the Orchestrator; it is
  the only way a `[gate]` item supported only by attestation is recorded as
  `PASS` (EV-001).
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
