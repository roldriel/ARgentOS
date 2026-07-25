# Standards Index

This document maps the cross-cutting standards in `.agents/standards/` by category.

## Feature flags

The protocol supports *feature flags* to enable improvements independently. Configuration lives in `.agents/features.toml` and can be overridden via environment variables with prefix `AGENTS_FEATURE_`.

Priority: environment variables > `.agents/features.toml` > defaults.

Boolean flags default to `true` unless explicitly set otherwise in `.agents/features.toml` (currently only `architecture_contract` defaults to `false`). The discovery flags include two non-boolean tunables (`discovery_sample_size`, `discovery_environment_ttl_hours`, `discovery_project_ttl_hours`). The orchestrator must consult them before enabling any improvement and record active flags in `SESSION_LOG.md`.

| Flag | Description |
|------|-------------|
| `decision_trees` | Enables TOML decision trees for recovery. |
| `rubrics` | Enables the `reviewer` role and the `## Rubric Evaluation` section in verification. |
| `knowledge_base` | Enables the `context_discoverer` role and enrichment with KB entries. |
| `caveman` | Applies `.agents/standards/communication/CAVEMAN.md` to all protocol communication. |
| `llm_discovery` | Enables LLM-based project discovery. |
| `discovery_orchestrator` | Enables the Discovery Orchestrator of the `discovery` domain. |
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
- `quality/CONFIDENCE.md` — general confidence model (HIGH/MEDIUM/LOW) with falsable level definitions and the anti-inflation rule, applied to verification reports, recovery analyses and KB recommendations.

## Context

- `context/CONTEXT.md` — context engineering, knowledge-base budgets, context compression techniques, and compact tags.
- `context/PROJECT_ARTIFACTS.md` — standard for project-level context artifacts `project-map.md` and `technical-analysis.md`.
- `context/ENVIRONMENT_PROBE.md` — rules for probing the execution environment (OS, shell, tools) before acting.
- `context/USING_PATTERNS.md` — how workers consume the discovery knowledge base (detected environment and development patterns).
- `context/KNOWLEDGE_CURATION.md` — anti-noise inclusion rules and `curation_status` lifecycle (`active`/`noisy`/`retired`) for KB entries under `.project/knowledge/entries/`.

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

- `runtime/PROTOCOL_BOUNDARIES.md` — file-system boundaries, artifact locations, and agent autonomy rules.
- `runtime/PROTOCOL_TAXONOMY.md` — master dictionary of the protocol: domains, lifecycles, states, artifacts, harness policies, actors, roles and workers, with `<domain>:<state>` references. Every state machine, workflow, harness policy, contract and role carries a YAML metadata block pointing to it (`taxonomy`, `kind`, `domain` as minimum). Files that already start with a TOML front matter block (`+++`) — policies and contracts — carry the YAML block immediately after the TOML block; all other files carry it at the top. Coherence is validated by harness policy `.agents/harness/policies/H13-protocol-taxonomy.md` (cross-cutting; `H08` and `H12` are intentionally absent) and `.agents/harness/tests/test_protocol_taxonomy.py`.
- `runtime/EXTERNAL_DEPENDENCIES.md` — `.agents/` must not depend on project-specific technologies or third-party runtime dependencies.
- `runtime/PYTHON_DEPENDENCIES.md` — concrete application of the external-dependencies policy for the current Python runtime.
