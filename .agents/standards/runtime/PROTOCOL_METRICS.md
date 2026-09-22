# Protocol Metrics Standard

## Purpose

Define the protocol metrics model: what is measured, where each data point is recorded, and how measurements are aggregated. Metrics exist so that the evolution of the protocol is prioritized with evidence instead of static analysis.

This standard measures the **protocol process**, never the content of artifacts nor the quality of the user product. It defines no thresholds and no automatic alerts: those require a data history that does not yet exist.

## Core concepts

### Data point

A single recorded observation of the protocol process. Every data point is one of two kinds:

- **Trigger data point** — produced by a harness trigger evaluation. It is recorded by the Orchestrator in `HARNESS_REPORT.md` (`.agents/contracts/HARNESS_REPORT.md`, §"Required structure": the `ENTRY` comments and the `## Metrics` section) as part of the gate evaluation entry.
- **Event data point** — produced by an agent decision or observation that does not pass through a harness trigger. It is recorded by the Orchestrator as a machine-readable `METRIC` entry in the session-level artifact `METRICS.md` (contract: `.agents/contracts/METRICS.md`).

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
| `context.budget_declared` / `context.budget_consumed` | Context Budget declared vs. consumed per delegation, in the materialized unit of `.agents/standards/context/BUDGET_MATERIALIZATION.md`; `consumed` is computed with the estimation rule (Verified) | `event:context_budget` |
| `context.candidates` | Context candidates prioritized vs. resolved vs. composed | `event:context_candidates` |

### Discovery

| Metric | Definition | Source |
|---|---|---|
| `discovery.consent_by_decision` | Distribution of discovery consent-gate decisions (chosen scope, rejection, non-interactive bypass) | `event:discovery_consent` |

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

### Reuse and cache

Metrics of the reuse/cache layers. They are layer-specific, dimension-specific
and attribution-aware: there is no global `cache_hit`, no global `savings` and
no cross-layer total; Discovery reuse, Project Knowledge reuse, Materialization
reuse and Provider Prompt Cache are never summed as the same benefit.

| Metric | Definition | Source | Evidence class | Availability | Scope | Provider dependency | Invariant |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `reuse.lookup_hits` / `reuse.lookup_misses` | Lookup outcomes per layer (`discovery`/`knowledge`/`materialization`) | `event:reuse_event` | Recorded (Observed) | PARCIAL (until producers) | session/project | NO | I-ECO-002, I-ECO-006 |
| `reuse.eligibility_accepted` / `reuse.eligibility_rejected` | Eligibility decisions per layer | `event:reuse_event` | Recorded (Observed) | PARCIAL | session/project | NO | I-ECO-001 |
| `reuse.outcome_successful` / `reuse.outcome_failed` | Reuse attempt outcomes per layer | `event:reuse_event` | Recorded (Observed) | PARCIAL | session/project | NO | I-ECO-001 |
| `reuse.invalidated` | Post-reuse lifecycle invalidations per layer | `event:reuse_event` | Recorded (Observed) | PARCIAL | session/project | NO | I-ECO-001 |
| `reuse.materialization_*` | Materialization slice of the per-layer reuse metrics (`layer=materialization`) | `event:reuse_event` | Recorded (Observed) | NOT AVAILABLE until producers | session/project | NO | I-ECO-002, I-ECO-004 |
| `cache.provider_hits` / `cache.provider_misses` / `cache.provider_unavailable` | Provider prompt-cache state observed through the adapter | `event:provider_cache_event` | Recorded (Observed, provider-reported) | NOT AVAILABLE until a real adapter | session/project | YES | I-ECO-003, I-ECO-006 |
| `cache.tokens_cached` / `cache.tokens_uncached` | Tokens reported by the provider | `event:provider_cache_event` | Recorded when provider-reported; Verified (Estimated, `ceil(chars/4)` rule) when recomputable against a captured payload; Unavailable otherwise | NOT AVAILABLE | session/project | YES | I-ECO-005, I-ECO-006 |
| `cache.latency_ms` | Provider request latency | `event:provider_cache_event` | Recorded (Observed) | NOT AVAILABLE | session/project | YES | I-ECO-005 |
| `discovery.reuse_opportunities` | Derived state-based estimate of currently reusable active discovery knowledge entries within the configured freshness window (`.last_discovery` + manifest `ttl_hours` + `[entries] active`); NOT a lookup, reuse-attempt, reuse-success, cache-hit or observed-event count | `fs` | Derived | DISPONIBLE with valid evidence; NOT AVAILABLE when discovery artifacts/metadata are missing or invalid | project | NO | I-ECO-004, I-ECO-005 |

`discovery.reuse_opportunities` is a Derived state-based metric. It estimates
the number of currently reusable active discovery knowledge entries within the
configured freshness window. It is NOT: a lookup count; a reuse-attempt count;
a reuse-success count; a cache-hit count; or an observed event count. The same
knowledge may contribute to this derived value in more than one aggregation or
session if the underlying discovery state remains fresh. The metric MUST NOT be
interpreted as cumulative reuse activity or economic savings.

#### Evidence classes

Every metric above carries an evidence class and an availability annotation:

- **Observed** (the runtime or provider reports the value) → **Recorded**
  (single report) or **Verified** (corroborated by a second artifact the
  reporter does not control).
- **Estimated** (local estimation, e.g. the `ceil(chars/4)` rule of
  `BUDGET_MATERIALIZATION.md`) → **Verified** when the rule is mechanically
  recomputable against the captured payload (precedent:
  `context.budget_consumed`), otherwise **Recorded**. Local estimation is never
  billing and never monetary savings.
- **Derived** (computed from other data) → **Derived**.
- **Unavailable** (not obtainable) → no data point is fabricated; the metric's
  Availability column declares it.

#### Unavailable dimensions

The following measurement dimensions are not instrumented by this catalog and
are declared **Unavailable**; no instrumentation is added to make them
disappear:

- Latency: baseline, reuse, cache lookup, validation and materialization
  latency, and latency saved/overhead/net benefit (only provider request
  latency is instrumented as `cache.latency_ms`).
- Tokens: baseline input, reused input, output, avoided, and validation/
  retrieval tokens (only `tokens_cached`/`tokens_uncached` are instrumented,
  provider-reported).
- Cost: monetary cost, pricing and provider billing (no pricing model exists;
  no price table or hardcoded price is introduced).
- Context budget: `budget_rejected` (only `budget_declared`/`budget_consumed`
  exist in this catalog).
- Storage: artifact size, retention, storage growth and GC (not instrumented).

### Reuse and cache economics

Rules of the measurement layer. No thresholds are defined and no metric gates
anything ("No metric gates anything", `## Aggregation`):

- **I-ECO-001 — Economy does not override validity:** economic metrics never
  override semantic validity; an invalid artifact is never admitted for
  economic value.
- **I-ECO-002 — Hit rate ≠ economic value:** a high hit rate is not economic
  value by itself.
- **I-ECO-003 — Provider cache ≠ Project Knowledge:** provider cache state is
  never Project Knowledge.
- **I-ECO-004 — No double counting:** the same avoided work is never attributed
  to two layers; layer attributions stay separate and are never summed as the
  same benefit.
- **I-ECO-005 — Evidence quality:** conclusions distinguish observed from
  estimated/derived data; every metric reports its class.
- **I-ECO-006 — Provider dependency:** provider-dependent measurements are
  never generalized as provider-independent facts.

Economic evaluation is an observational layer: it does not admit or reject
persistence or reuse at runtime, and it never trades away correctness,
freshness, provenance or isolation.

## Registration rules

- If a data point already passes through a harness trigger, it is recorded in `HARNESS_REPORT.md` by the Orchestrator as part of the gate evaluation; no duplicate event is recorded.
- Every other data point is recorded by the Orchestrator as a `METRIC` comment in `METRICS.md` at the moment the event occurs (not retroactively at session end).
- Events are append-only: a wrong event is corrected by a later event, never by editing or deleting the recorded one.
- Every `METRIC` event carries `seq` (an integer, strictly increasing per
  session), `timestamp` and `clock` (`utc` | `agent_clock`); execution-scoped
  events additionally carry `iteration` (the numeric iteration folder of the
  execution). This applies to every catalogued type, including
  `reuse_event` and `provider_cache_event` (contract:
  `.agents/contracts/METRICS.md`, §Event catalog).
- A delegation that declares `context_budget` carries it in its `delegation`
  event and is paired with a `context_budget` event of the same delegation
  (same `iteration`/`phase`, same declared value) (OBS-001); without the
  declared/consumed pair, a budget-compliance claim is an attestation
  (OBS-002).
- The event catalog (types and required fields) is defined by `.agents/contracts/METRICS.md`; this standard defines what the events mean.

## Aggregation

Aggregation is performed by the agent on demand (metrics are advisory; nothing gates on them):

1. Choose the scope: one session (`.project/<session-uuid>/`) or the whole project (every session under `.project/`).
2. Parse the `ENTRY` comments of each session's `HARNESS_REPORT.md` and the `METRIC` comments of its `METRICS.md`; count the iteration folders and their artifacts from the filesystem layout. Unparseable comments are counted separately as corrupt data points, never silently discarded.
3. Compute every metric of the catalog from those data points: flow metrics from the trigger entries, failure/delegation/context/session metrics from the events, and the computed ratios.
4. Emit the aggregated report (JSON or a summary table) with one value per catalog metric.

The aggregation consolidates the data points of one session or of the whole project (`.project/`). It never modifies session artifacts.
The development repository provides a metrics aggregation tool that implements
this procedure mechanically (dev-only; not part of the distributed protocol);
adopting projects may aggregate by judgment or with their own tooling.

## Verifiability classes

Every metric data point belongs to one of three classes, declared here and
tagged in the aggregated report:

- **Derived** — computable from the session filesystem or persisted state
  without trusting the reporter: `session.iterations`,
  `session.artifacts_per_iteration`, and the cross-check between `state.json`
  gate records and `HARNESS_REPORT.md` entries.
- **Recorded** — the event is the only record; its value is accepted as the
  report of what happened: `state_transition`, `failure`, `delegation`,
  `reviewer_retry`, `skill_override`, `flag_evidence`, `discovery_consent`,
  `session_risk`.
- **Verified** — corroborated by a second artifact the reporter does not
  control in that step: `context.budget_declared` / `context.budget_consumed`
  against the estimation rule of `BUDGET_MATERIALIZATION.md` when the payload
  is captured; `flags.evidenced` against the consumption declaration in a
  produced artifact; harness `PASS` entries against `state.json` gate records.

No metric gates anything; the class only declares the trust boundary. The
aggregation report tags each metric with its class, and the development-side
`--audit` mode reports discrepancies between the mechanical cross-checks.

Every event carries `seq`, `timestamp` and `clock` (`utc` | `agent_clock`;
contract: `.agents/contracts/METRICS.md`, §Event catalog): `utc` is the
default for mechanically written records; agent-written timestamps without a
reliable clock declare `clock: agent_clock` (G-004). Execution-scoped events
carry `iteration`. A `delegation` event that declares `context_budget` is
paired with a `context_budget` event of the same delegation (same
`iteration`/`phase`, same declared value); the `Verified` class of the
declared/consumed pair is kept. The `Verified` class means "corroborated by a
second artifact", not external verification of the event: a data point
without that corroboration is a recorded report, and a claim about it that
cannot cite evidence is an attestation (`.agents/harness/INDEX.md`,
§Enforcement boundaries).

## Health signals

Three signals summarize protocol health. Each has a conceptual interpretation; none has a threshold — their value is comparative across time.

- **Recovery rate** (`flow.recovery_entries / flow.transitions`): how often the protocol has to correct itself. A rising trend signals that upstream phases (analysis, specification, planning) are degrading or that policies are miscalibrated.
- **Clarification rate** (`flow.clarification_entries / flow.transitions`): how often the protocol needs the user to proceed. A rising trend signals ambiguous intake or over-eager escalation to `NEEDS_CLARIFICATION`; a near-zero trend alongside rising deviations signals under-escalation (assumptions being made).
- **Reviewer rework rate** (`flow.reviewer_retries / delegation.count`): how much correction the reviewer loop absorbs. A rising trend signals that execution quality is degrading or that rubrics are drifting from acceptance criteria.

## Use in protocol evolution

The aggregated report is an explicit input of protocol planning: every proposed change to the protocol declares which metric justifies it or which metric it intends to move. A change that no metric can justify or measure needs an explicit rationale for that absence.
