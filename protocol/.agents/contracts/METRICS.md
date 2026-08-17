+++
schema_version = "1.0.0"
artifact = "METRICS.md"
phase = "all"
produced_by = "orchestrator"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: cross-cutting
artifact: METRICS.md
lifecycle: null
produced_by: [core:TASK_RECEIVED]
consumed_by: [core:COMPLETED]
---

# Contract: Protocol Metrics

## Purpose

`METRICS.md` records the event data points of the protocol metrics model (`.agents/standards/runtime/PROTOCOL_METRICS.md`): observations of the protocol process that do not pass through a harness trigger. Trigger data points live in `HARNESS_REPORT.md`; this artifact holds everything else. It lives at the root of every session (`.project/<session-uuid>/METRICS.md`).

## Location and ownership

- Path: `.project/<session-uuid>/METRICS.md` (session root, not inside an iteration folder).
- Producer: the Orchestrator, who appends one machine-readable entry at the moment each event occurs.
- Consumers: the agent-driven aggregation procedure of the metrics standard (`.agents/standards/runtime/PROTOCOL_METRICS.md`, §"Aggregation") and any audit of the session.

## Required structure

1. **Header**:

   ```markdown
   # Protocol Metrics

   - Session UUID: `<uuid>`
   ```

2. **`## Entries`** — one HTML comment per event, in chronological order:

   ```markdown
   <!-- METRIC: {"timestamp": "...", "type": "...", ...} -->
   ```

   These `METRIC` comments are part of the contract: they must remain valid JSON, one event per comment, and must not be removed or edited. Human-readable notes between comments are allowed but carry no metric meaning.

## Event catalog

Every event carries `timestamp` (ISO-8601) and `type`. Required fields per type:

| `type` | Required fields | Meaning |
|---|---|---|
| `session_start` | `declarative_flags` (list of strings), `protocol_version` (string) | Active declarative feature flags at session start: the session's standing evidence obligations. `protocol_version` is the value of `.agents/VERSION` at session start; session artifacts are immutable records of the protocol version in force at that moment and are never rewritten or "reproduced" with a newer version. |
| `state_transition` | `from`, `to`, `iteration` | A state-machine transition applied by the Orchestrator. `to` uses the state name (e.g. `RECOVERY`, `NEEDS_CLARIFICATION`). |
| `reviewer_retry` | `artifact`, `cycle` | One reviewer `REWORK` correction cycle over an artifact; `cycle` is the 1-based retry ordinal. |
| `failure` | `class` | A reported failure. `class` is one of `F1` (blocker), `F2` (deviation), `F3` (ambiguity), `F4` (inconsistency), `F5` (harness FAIL). Optional: `policy` (e.g. `H15`), `audience` (`machine` or `agent`). |
| `delegation` | `phase`, `profile`, `skills`, `h15` | One worker delegation. `profile` is the profile name or `null`; `skills` is the activated skill list; `h15` is `PASS`, `FAIL`, or `null` when the gate did not apply. |
| `skill_override` | `skill` | A skill activated by judgment override of the activation table. |
| `flag_evidence` | `flag` | A declarative flag whose consumption was declared in an artifact or log entry. |
| `context_budget` | `phase`, `declared`, `consumed` | Context Budget declared vs. consumed for one delegation, in estimated tokens (`.agents/standards/context/BUDGET_MATERIALIZATION.md`). |
| `context_candidates` | `prioritized`, `resolved`, `composed` | Candidate counts across the context pipeline of one delegation. |

## Constraints

- Events are append-only and recorded when they occur, never reconstructed retroactively. A wrong event is corrected by a later event, not by editing the recorded one.
- Events record identifiers and quantities only — never artifact prose, user text, or task content (privacy rule of `.agents/standards/runtime/PROTOCOL_METRICS.md`).
- Unknown event types and unknown extra fields are ignored by aggregation, never errors.
- The artifact must not include credentials, tokens, or personal data.
- Events are self-reported by the Orchestrator; the verifiability class of
  each event type is declared in `.agents/standards/runtime/PROTOCOL_METRICS.md`
  (§Verifiability classes).
