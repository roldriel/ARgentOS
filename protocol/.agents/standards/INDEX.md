# Standards Index

This document maps the cross-cutting standards in `.agents/standards/` by category.

## Feature flags

The protocol supports *feature flags* to enable improvements independently. Configuration lives in `.agents/features.toml` and can be overridden via environment variables with prefix `AGENTS_FEATURE_`.

Priority: environment variables > `.agents/features.toml` > defaults.

Boolean flags default to `true` unless explicitly set otherwise in `.agents/features.toml` (currently only `architecture_contract` defaults to `false`). The discovery flags include two non-boolean tunables (`discovery_sample_size`, `discovery_environment_ttl_hours`, `discovery_project_ttl_hours`). The orchestrator must consult them before enabling any improvement and record active flags in `SESSION_LOG.md`.

### Flag categories and declarative compliance

Flags are classified by who consumes them:

- **`[code]` flags** are resolved by the Orchestrator when evaluating the «Gate Checklist» of the H01 policy (resolution order: `AGENTS_FEATURE_*` environment variable > `.agents/features.toml` > default enabled). Compliance is mechanical: the gated behavior happens or a check fails. No declarative evidence is needed.
- **`[declarative]` flags** are consumed by agents reading `.agents/features.toml` directly. Compliance is behavioral: an enabled declarative flag creates an obligation — the consuming agent MUST read its value before the flow point where it conditions behavior, and MUST act on it at that point.
- **Dual flags** (the technical-practice flags) are both: checked by the Orchestrator at gate evaluation (standards presence in the health checklist, H01/H05 gate items) and consumed declaratively by workers during execution.

Ignoring an enabled declarative flag — not reading it, or reading it without acting — is a **deviation** (class F2: difference between specified and executed behavior): it must be logged as such, and if the omission is material to acceptance criteria or scope it escalates to recovery or clarification per the deviation reclassification rule. Disabling a flag (via `AGENTS_FEATURE_`) is never a deviation; the obligation ends with the flag.

**Compliance evidence** is auditable as a two-part join: (1) the initial `SESSION_LOG.md` entry records the active flags — the session's standing obligations; (2) when a declarative flag conditions an agent's behavior, that condition is declared in the produced artifact or in the corresponding session-log entry, naming the flag and the applied effect (e.g. a delegation declaring the `caveman` level; a Discovery Orchestrator invocation logged as an event; TDD red-green-refactor evidence in `EXECUTION_SUMMARY.md` for dual flags). An active declarative flag with no consumption declaration and no logged deviation is *unevidenced compliance*. Evidence is never rewritten retroactively: a late-discovered omission is logged as a deviation, not patched.

### Compliance evidence (canonical procedure)

The evidence join is defined operationally as follows:

1. **Expected flags**: the `declarative_flags` list of the session's
   `session_start` event in `METRICS.md` (contract:
   `.agents/contracts/METRICS.md`) — the session's standing obligations.
2. **Evidenced flags**: the `flag_evidence` events in `METRICS.md` — each
   names a declarative flag whose consumption was declared in a produced
   artifact or in a session-log entry.
3. **Unevidenced flags**: `expected − evidenced` per session. An enabled
   declarative flag with no `flag_evidence` event and no logged deviation is
   *unevidenced compliance*: detectable via this join, and subject to the
   deviation rule when the omission is material.
4. **Mechanism**: the metrics aggregation tool of the development repository
   computes the three sets mechanically (dev-only; see
   `standards/runtime/PROTOCOL_METRICS.md`, §Aggregation); the agent may
   compute them by judgment in an adopting project.

Honesty note: the events are self-reported (see `harness/INDEX.md`,
§Enforcement model); the join is as accurate as the events recorded.

| Flag | Description |
|------|-------------|
| `rubrics` | Enables the `reviewer` role and the `## Rubric Evaluation` section in verification. |
| `knowledge_base` | Enables the `context_discoverer` role and enrichment with KB entries. |
| `caveman` | Applies `.agents/standards/communication/CAVEMAN.md` to all protocol communication. |
| `llm_discovery` | Enables LLM-based project discovery. |
| `discovery_orchestrator` | Enables the Discovery Orchestrator of the `discovery` domain. |
| `discovery_require_consent` | Requires explicit user consent before any automatic discovery invocation (default `true`). |
| `discovery_sample_size` | Number of files sampled during discovery (default 10; not boolean). |
| `discovery_environment_ttl_hours` | TTL of the environment discovery entry (default 6; not boolean). |
| `discovery_project_ttl_hours` | TTL of the project discovery KB (default 24; not boolean). |
| `tdd` | Enables `.agents/standards/testing/TDD.md` to enforce red-green-refactor. |
| `srp` | Enables `.agents/standards/development/design/SOLID/SRP.md`. |
| `ocp` | Enables `.agents/standards/development/design/SOLID/OCP.md`. |
| `lsp` | Enables `.agents/standards/development/design/SOLID/LSP.md`. |
| `isp` | Enables `.agents/standards/development/design/SOLID/ISP.md`. |
| `dip` | Enables `.agents/standards/development/design/SOLID/DIP.md`. |
| `screaming_architecture` | Enables `.agents/standards/development/design/SCREAMING_ARCHITECTURE.md`. |
| `clean_architecture` | Enables `.agents/standards/development/design/CLEAN_ARCHITECTURE.md`. |
| `layered_architecture` | Enables `.agents/standards/development/design/LAYERED_ARCHITECTURE.md`. |
| `dry` | Enables `.agents/standards/development/design/DRY.md`. |
| `grasp` | Enables `.agents/standards/development/design/GRASP.md`. |
| `ddd_tactical` | Enables `.agents/standards/development/design/DDD_TACTICAL.md`. |
| `ddd_strategic` | Enables `.agents/standards/development/design/DDD_STRATEGIC.md`. |
| `architecture_contract` | Enables `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md` as the operational architecture ruleset. |

### Technical-practice catalog

The technical-practice flags map each flag to the rubric that scores it and the standard document that defines it. This table is the canonical flag → (rubric, standard) mapping (previously `technical_practices.py`, now removed); the protocol health checklist (`.agents/standards/runtime/PROTOCOL_HEALTH.md`) uses it to verify that every enabled practice has its standard on disk.

| Flag | Rubric | Standard |
|------|--------|----------|
| `tdd` | `TDD_RUBRIC` | `.agents/standards/testing/TDD.md` |
| `srp` | `SRP_RUBRIC` | `.agents/standards/development/design/SOLID/SRP.md` |
| `ocp` | `OCP_RUBRIC` | `.agents/standards/development/design/SOLID/OCP.md` |
| `lsp` | `LSP_RUBRIC` | `.agents/standards/development/design/SOLID/LSP.md` |
| `isp` | `ISP_RUBRIC` | `.agents/standards/development/design/SOLID/ISP.md` |
| `dip` | `DIP_RUBRIC` | `.agents/standards/development/design/SOLID/DIP.md` |
| `screaming_architecture` | `SCREAMING_ARCHITECTURE_RUBRIC` | `.agents/standards/development/design/SCREAMING_ARCHITECTURE.md` |
| `clean_architecture` | `CLEAN_ARCHITECTURE_RUBRIC` | `.agents/standards/development/design/CLEAN_ARCHITECTURE.md` |
| `dry` | `DRY_RUBRIC` | `.agents/standards/development/design/DRY.md` |
| `layered_architecture` | `LAYERED_ARCHITECTURE_RUBRIC` | `.agents/standards/development/design/LAYERED_ARCHITECTURE.md` |
| `grasp` | `GRASP_RUBRIC` | `.agents/standards/development/design/GRASP.md` |
| `ddd_tactical` | `DDD_TACTICAL_RUBRIC` | `.agents/standards/development/design/DDD_TACTICAL.md` |
| `ddd_strategic` | `DDD_STRATEGIC_RUBRIC` | `.agents/standards/development/design/DDD_STRATEGIC.md` |

## Communication

- `communication/OUTPUT_EFFICIENCY.md` — universal rules for minimal, efficient worker output (English).
- `communication/CAVEMAN.md` — optional compressed communication mode applied to all protocol communication when the `caveman` feature flag is enabled. Uses English for internal communication and neutral Spanish for user-facing communication.

## Requirements

- `requirements/EARS.md` — syntax for acceptance criteria.
- `requirements/NO_ASSUMPTIONS.md` — when the agent must ask for clarification instead of assuming.
- `requirements/INTENT_CONFIDENCE.md` — objective criteria for assessing confidence in intent interpretation.

## Conduct

- `conduct/ANTI_CIRCUMVENTION.md` — explicit prohibition against skipping phases, violating the state machine, or hallucinating context for convenience or simplicity.
- `conduct/OPERATIONAL_RULES.md` — index that maps each operational rule for workers to its canonical conduct standard.

## Quality

- `quality/RUBRICS.md` — rubric evaluation format and scoring levels.
- `quality/PREFLIGHT_CHECKLIST.md` — pre-flight self-checklist for workers.
- `quality/CONFIDENCE.md` — general confidence model (HIGH/MEDIUM/LOW) with falsable level definitions and the anti-inflation rule, applied to verification reports, recovery analyses and KB recommendations; includes the recommendation-confidence specialization for Orchestrator accept-or-override decisions.
- `quality/EVIDENCE.md` — evidence model: five evidence classes
  (`observation`/`measurement`/`attestation`/`assertion`/`reference`),
  `[[evidence]]` entries, sufficiency rules per `[gate]`/`[agent]` item, and the
  VERIFIED invariant (non-attestation evidence or the term "attested").

## Context

- `context/CONTEXT.md` — context engineering, the determinism model, knowledge-base budgets, context compression techniques, and compact tags. Also defines stable/dynamic context classification, context segments (Core/Project/Worker), semantic identity, scope and semantic isolation.
- `context/BUDGET_MATERIALIZATION.md` — materialization of the Context Budget for the prompt-based runtime: unit (estimated tokens), estimation rule, and conversion from the character-denominated KB budgets. Also declares that persistence and cacheability do not change the semantic limits of the Context Budget.
- `context/RESOLUTION_TIE_BREAKING.md` — Resolution policy: ordered criteria for deciding between equivalent context candidates (explicit directive, source precedence, recency, coverage, first-fit).
- `context/RESOLUTION_DEDUPLICATION.md` — Resolution policy: detection of fully-contained (redundant) candidates and their lossless removal.
- `context/RESOLUTION_MERGE.md` — Resolution policy: when partially overlapping compatible candidates are fused, and the form of the merged result.
- `context/RESOLUTION_UNRESOLVABLE_CONFLICTS.md` — Resolution policy: behavior before incompatibility, mutual exclusion, and budget conflicts (report as F3/F4/F1, never guess).
- `context/COMPOSITION_COMPRESSION.md` — Composition policy: closed set of compression techniques (integrates `CONTEXT.md` §8.2/§8.4), lossless rule, and order before Optimization.
- `context/COMPOSITION_OPTIMIZATION.md` — Composition policy: criteria for adapting the payload's final form to the execution purpose, applied after Compression.
- `context/ENVIRONMENT_PROBE.md` — rules for probing the execution environment (OS, shell, tools) before acting.
- `context/USING_PATTERNS.md` — how workers consume the discovery knowledge base (detected environment and development patterns).
- `context/KNOWLEDGE_CURATION.md` — anti-noise inclusion rules and `curation_status` lifecycle (`active`/`noisy`/`retired`) for KB entries under `.project/knowledge/entries/`.
- `context/KNOWLEDGE_LIFECYCLE.md` — knowledge lifecycle model: `snapshot`/`claim`/`lesson` types, per-claim freshness with resolvable provenance, post-execution invalidation (`invalidated_facts`) and pipeline-scoped revalidation. Separates semantic invalidation, freshness expiration and physical deletion into distinct domains.

## Testing

- `testing/TDD.md` — Test-Driven Development cycle and evidence format, applied when the `tdd` feature flag is enabled.

## Development

### Design / Architecture

- `development/design/SOLID/SRP.md` — Single Responsibility Principle, applied when the `srp` feature flag is enabled.
- `development/design/SOLID/OCP.md` — Open/Closed Principle, applied when the `ocp` feature flag is enabled.
- `development/design/SOLID/LSP.md` — Liskov Substitution Principle, applied when the `lsp` feature flag is enabled.
- `development/design/SOLID/ISP.md` — Interface Segregation Principle, applied when the `isp` feature flag is enabled.
- `development/design/SOLID/DIP.md` — Dependency Inversion Principle, applied when the `dip` feature flag is enabled.
- `development/design/SCREAMING_ARCHITECTURE.md` — domain-first project structure, applied when the `screaming_architecture` feature flag is enabled.
- `development/design/CLEAN_ARCHITECTURE.md` — layered architecture with inward dependencies, applied when the `clean_architecture` feature flag is enabled.
- `development/design/LAYERED_ARCHITECTURE.md` — horizontal layers with downward dependencies, applied when the `layered_architecture` feature flag is enabled.
- `development/design/DRY.md` — elimination of duplicated knowledge, applied when the `dry` feature flag is enabled.
- `development/design/GRASP.md` — responsibility assignment patterns, applied when the `grasp` feature flag is enabled.
- `development/design/DDD_TACTICAL.md` — DDD patterns inside a bounded context, applied when the `ddd_tactical` feature flag is enabled.
- `development/design/DDD_STRATEGIC.md` — bounded contexts and context maps, applied when the `ddd_strategic` feature flag is enabled.
- `development/design/ARCHITECTURE_CONTRACT.md` — operational architecture contract that unifies layers, dependency rules, naming suffixes and self-verification, applied when the `architecture_contract` feature flag is enabled.

### Languages

- `development/languages/INDEX.md` — placeholder index for language-specific conventions.

## Orchestration

- `orchestration/ORCHESTRATION_GUIDE.md` — decision procedure for selecting worker profiles and delegation payloads.
- `orchestration/DECISIONS.md` — conceptual catalog of the Orchestrator's discretionary decision points (question, inputs, authority), including the retry bound, KB criticality, and founded abort concepts.
- `orchestration/SKILLS.md` — skill mechanism: activation (table + judgment), two-level locations and precedence, validation, authority hierarchy, and coexistence rules. Skill format contract: `.agents/skills/README.md`.
- `orchestration/README.md` — overview of orchestration standards.

### Worker profiles

Specialized worker profiles live in `.agents/roles/profiles/` and are enabled by the `profile` field in `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.

- `.agents/roles/profiles/README.md` — catalog and usage guide.
- `.agents/roles/profiles/backend_engineer.md` — business logic, endpoints, services.
- `.agents/roles/profiles/database_engineer.md` — schemas, migrations, queries, persistence models.
- `.agents/roles/profiles/integration_engineer.md` — external APIs, providers, adapters.
- `.agents/roles/profiles/qa_engineer.md` — tests, cases, mocks, coverage.
- `.agents/roles/profiles/tech_writer.md` — technical documentation for developers and agents.
- `.agents/roles/profiles/functional_writer.md` — business documentation for non-technical stakeholders.

## Runtime

- `runtime/PROTOCOL_BOUNDARIES.md` — file-system boundaries, artifact locations, agent autonomy rules, and the derived project segment store rule.
- `runtime/AUTHORIZATION.md` — authorization and capability model: default frontier, `effects` block, who can authorize, and the AUTHORIZED / UNAUTHORIZED / AUTHORIZATION_UNDETERMINED states.
- `runtime/PROTOCOL_TAXONOMY.md` — master dictionary of the protocol: domains, lifecycles, states, artifacts, harness policies, actors, roles and workers, with `<domain>:<state>` references. Every state machine, workflow, harness policy, contract and role carries a YAML metadata block pointing to it (`taxonomy`, `kind`, `domain` as minimum). Files that already start with a TOML front matter block (`+++`) — policies and contracts — carry the YAML block immediately after the TOML block; all other files carry it at the top. Coherence is validated by the Orchestrator's judgment against harness policy `.agents/harness/policies/H13-protocol-taxonomy.md` (cross-cutting; `H08`, `H12` and `H14` are intentionally absent).
- `runtime/EXTERNAL_DEPENDENCIES.md` — `.agents/` must not depend on project-specific technologies or third-party runtime dependencies.
- `runtime/PYTHON_DEPENDENCIES.md` — concrete application of the external-dependencies policy for the current Python runtime.
- `runtime/PROTOCOL_METRICS.md` — protocol metrics model: metric catalog (flow, failures, delegation, context, session, declarative flags), registration rule (trigger data points in `HARNESS_REPORT.md`, event data points in the session `METRICS.md`), agent-driven aggregation procedure, and the protocol health signals (no thresholds).
- `runtime/PROTOCOL_HEALTH.md` — protocol health checklist applied by the ArgentOS System Agent at bootstrap (required structure, contract front matter, flag-gated standards, project skills, state-storage probe, `.last_health_check` TTL rule).
