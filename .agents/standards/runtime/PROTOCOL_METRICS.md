# Protocol Metrics Standard

## Purpose

Define the protocol metrics model: what is measured, where each data point is recorded, and how measurements are aggregated. Metrics exist so that the evolution of the protocol is prioritized with evidence instead of static analysis.

This standard measures the **protocol process**, never the content of artifacts nor the quality of the user product. It defines no thresholds and no automatic alerts: those require a data history that does not yet exist.

## Core concepts

### Data point

A single recorded observation of the protocol process. Every data point is one of two kinds:

- **Trigger data point** — produced by a harness trigger execution. It is recorded by the runner in `HARNESS_REPORT.md` (`.agents/contracts/HARNESS_REPORT.md`, §"Required structure": the `ENTRY` comments and the `## Metrics` section). No agent records these by hand.
- **Event data point** — produced by an agent decision or observation that does not pass through a runner trigger. It is recorded by the Orchestrator as a machine-readable `METRIC` entry in the session-level artifact `METRICS.md` (contract: `.agents/contracts/METRICS.md`).

### Metric

An aggregate computed over data points of one or more sessions. Metrics are never read from free text: they are computed from `ENTRY` comments of `HARNESS_REPORT.md`, from `METRIC` comments of `METRICS.md`, and from the session filesystem layout (iteration folders and their artifacts).

### Privacy rule

Metrics describe the process, not the content. A data point may record identifiers (state names, trigger IDs, failure classes, flag names, skill names, profile names) and quantities (counts, durations, budget figures), never artifact prose, user text, or task content.

## Metric catalog

Metrics are grouped by what they measure. The `Source` column states where the data points live; `harness` means `HARNESS_REPORT.md` entries, `event:<type>` means a `METRICS.md` event of that type, `fs` means derived from the session filesystem layout.

### Flow

| Metric | Definition | Source |
|---|---|---|
| `flow.transitions` | State transitions recorded in the session | `event:state_transition` |
| `flow.recovery_entries` | Transitions whose target is `RECOVERY` | `event:state_transition` |
| `flow.clarification_entries` | Transitions whose target is `NEEDS_CLARIFICATION` | `event:state_transition` |
| `flow.reviewer_retries` | Reviewer `REWORK` correction cycles (bounded by the retry bound of `.agents/standards/orchestration/DECISIONS.md`, §"Retry bound") | `event:reviewer_retry` |

### Failures

| Metric | Definition | Source |
|---|---|---|
| `failures.by_class` | Distribution of reported failures by class (blocker, deviation, ambiguity, inconsistency, harness FAIL) | `event:failure` |
| `failures.harness_by_domain` | Harness FAILs grouped by policy domain prefix (`H` = core, `D` = discovery, `S` = system, per the `harness_prefix` of `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`) | `harness` |
| `failures.agent_evaluated` | Failures reported on agent-evaluated policy items | `event:failure` with `audience: "agent"` |

### Delegation

| Metric | Definition | Source |
|---|---|---|
| `delegation.count` | Delegations performed in the session | `event:delegation` |
| `delegation.validity_violations` | Delegation-validity (H15) FAIL results, pre-delegation or post-return | `event:delegation` with `h15: "FAIL"` |
| `delegation.skill_overrides` | Skill activations decided by judgment override of the activation table (`.agents/standards/orchestration/SKILLS.md`) | `event:skill_override` |
| `delegation.profiles` | Distribution of specialized worker profiles used | `event:delegation` |

### Context

| Metric | Definition | Source |
|---|---|---|
| `context.budget_declared` / `context.budget_consumed` | Context Budget declared vs. consumed per delegation, in the materialized unit of `.agents/standards/context/BUDGET_MATERIALIZATION.md` | `event:context_budget` |
| `context.candidates` | Context candidates prioritized vs. resolved vs. composed | `event:context_candidates` |

### Session

| Metric | Definition | Source |
|---|---|---|
| `session.iterations` | Number of iteration folders of the session | `fs` |
| `session.artifacts_per_iteration` | Artifact files per iteration folder | `fs` |
| `session.duration_ms` | Elapsed time between the first and last recorded data point | `harness` + all `event:*` |

### Declarative flags

| Metric | Definition | Source |
|---|---|---|
| `flags.expected` | Active declarative flags declared at session start (obligations, per `.agents/standards/INDEX.md`, §"Flag categories and declarative compliance") | `event:session_start` |
| `flags.evidenced` | Declarative flags with a recorded consumption declaration | `event:flag_evidence` |
| `flags.unevidenced` | Expected flags with no recorded evidence | computed |

## Registration rules

- If a data point already passes through a runner trigger, it is recorded in `HARNESS_REPORT.md` by the runner; no duplicate event is recorded.
- Every other data point is recorded by the Orchestrator as a `METRIC` comment in `METRICS.md` at the moment the event occurs (not retroactively at session end).
- Events are append-only: a wrong event is corrected by a later event, never by editing or deleting the recorded one.
- The event catalog (types and required fields) is defined by `.agents/contracts/METRICS.md`; this standard defines what the events mean.

## Aggregation

Aggregation is performed by the agent on demand (metrics are advisory; nothing gates on them):

1. Choose the scope: one session (`.project/<session-uuid>/`) or the whole project (every session under `.project/`).
2. Parse the `ENTRY` comments of each session's `HARNESS_REPORT.md` and the `METRIC` comments of its `METRICS.md`; count the iteration folders and their artifacts from the filesystem layout. Unparseable comments are counted separately as corrupt data points, never silently discarded.
3. Compute every metric of the catalog from those data points: flow metrics from the trigger entries, failure/delegation/context/session metrics from the events, and the computed ratios.
4. Emit the aggregated report (JSON or a summary table) with one value per catalog metric.

The aggregation consolidates the data points of one session or of the whole project (`.project/`), following the runner metrics pattern (`.agents/harness/RUNNER.md`, §"Harness metrics"). It never modifies session artifacts.

## Health signals

Three signals summarize protocol health. Each has a conceptual interpretation; none has a threshold — their value is comparative across time.

- **Recovery rate** (`flow.recovery_entries / flow.transitions`): how often the protocol has to correct itself. A rising trend signals that upstream phases (analysis, specification, planning) are degrading or that policies are miscalibrated.
- **Clarification rate** (`flow.clarification_entries / flow.transitions`): how often the protocol needs the user to proceed. A rising trend signals ambiguous intake or over-eager escalation to `NEEDS_CLARIFICATION`; a near-zero trend alongside rising deviations signals under-escalation (assumptions being made).
- **Reviewer rework rate** (`flow.reviewer_retries / delegation.count`): how much correction the reviewer loop absorbs. A rising trend signals that execution quality is degrading or that rubrics are drifting from acceptance criteria.

## Use in protocol evolution

The aggregated report is an explicit input of protocol planning: every proposed change to the protocol declares which metric justifies it or which metric it intends to move. A change that no metric can justify or measure needs an explicit rationale for that absence.
