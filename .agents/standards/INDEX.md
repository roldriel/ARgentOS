# Standards Index

This document maps the cross-cutting standards in `.agents/standards/` by category.

## Feature flags

The protocol supports *feature flags* to enable improvements independently. Configuration lives in `.agents/features.toml` and can be overridden via environment variables with prefix `AGENTS_FEATURE_`.

Priority: environment variables > `.agents/features.toml` > defaults.

All flags default to `true`. The orchestrator must consult them before enabling any improvement and record active flags in `SESSION_LOG.md`.

| Flag | Description |
|------|-------------|
| `decision_trees` | Enables TOML decision trees for recovery. |
| `rubrics` | Enables the `reviewer` role and the `## Rubric Evaluation` section in verification. |
| `knowledge_base` | Enables the `context_discoverer` role and enrichment with KB entries. |
| `caveman` | Applies `.agents/standards/communication/CAVEMAN.md` to all protocol communication. |
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
- `conduct/OPERATIONAL_RULES.md` — operational contract for workers, referencing canonical conduct standards.

## Quality

- `quality/RUBRICS.md` — rubric evaluation format and scoring levels.
- `quality/PREFLIGHT_CHECKLIST.md` — pre-flight self-checklist for workers.

## Context

- `context/CONTEXT.md` — context engineering and knowledge-base budgets.

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

## Runtime

- `runtime/PROTOCOL_BOUNDARIES.md` — file-system boundaries, artifact locations, and agent autonomy rules.
- `runtime/EXTERNAL_DEPENDENCIES.md` — `.agents/` must not depend on project-specific technologies or third-party runtime dependencies.
- `runtime/PYTHON_DEPENDENCIES.md` — concrete application of the external-dependencies policy for the current Python runtime.
