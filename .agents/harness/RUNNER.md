# Harness Runner

This document describes the executable runner (`runner.py`) that the Orchestrator invokes to validate artifacts, list feature flags, run health checks, and evaluate recovery decision trees.

For the harness concept, trigger catalog, and policies, see `.agents/harness/INDEX.md`.

## Module layout

The runner is split into focused modules under `.agents/harness/`; `runner.py` is the CLI entry point and re-exports the public API (`import runner` keeps working):

- `runner_paths.py` — shared filesystem locations (policy/tree dirs, artifacts dir).
- `runner_models.py` — `CheckResult` / `HarnessResult` dataclasses.
- `runner_markdown.py` — TOML front matter and Markdown section parsing helpers.
- `runner_policies.py` — policy loading across domains (core `H*`, discovery `D*`, system `S*`, cross-cutting).
- `runner_artifacts.py` — artifact path resolution inside iteration folders.
- `runner_validators.py` — section, EARS, rubric and semantic validators, plus `run_trigger`.
- `runner_report.py` — `HARNESS_REPORT.md` generation.

## Artifact validation

The Orchestrator invokes the runner from the CLI:

```bash
python .agents/harness/runner.py --session <uuid> --trigger H01 [--iteration 00]
```

If `--iteration` is not specified, the runner finds the most recent iteration containing the target artifact.

The runner:

- Reads the corresponding policy from `.agents/orchestrators/core/harness/policies/`.
- Validates the artifact against the contract.
- Applies the semantic validators declared by the policy front matter (`semantic_checks = [...]` when `semantic_validation = true`). A declared validator name the runner does not know is an explicit `FAIL` (`semantic_validator_<name>_known`), never silently ignored. Known validators live in `runner_validators.SEMANTIC_VALIDATORS`.
- Updates `HARNESS_REPORT.md` at the session root. Pre-existing entries that cannot be re-parsed are discarded with a visible `WARNING` on stderr and counted in the report's `## Summary` section (`Corrupt entries discarded: N`).
- Returns JSON with result `PASS`/`FAIL`.

## Cross-cutting subcommands

```bash
# List active feature flags
python .agents/harness/runner.py features

# Verify global protocol health
python .agents/harness/runner.py health-check
```

## Health check

The protocol exposes a global health check via:

```bash
python .agents/harness/runner.py health-check
```

The orchestrator runs it automatically at the start of a session if `.project/.last_health_check` does not exist or is older than `ttl_hours` (default 24, configurable in `.agents/features.toml` or via `AGENTS_HEALTH_CHECK_TTL_HOURS`). `health_check.should_run_health_check()` applies that configured TTL when the caller does not pass an explicit value.

The `health-check` subcommand verifies that critical directories exist, index files are readable, and features enabled by feature flags are well-formed. If it passes, it updates `.project/.last_health_check` with the current timestamp.

Decision-tree validation covers every domain that provides a `decision_trees/` directory (core `H*`, discovery `D*`, system `S*`): the expected triggers are derived from that domain's policy files (minus the documented exemptions H09/H10), and every tree is structurally validated (start node, branches, node references, cycles) via `decision_tree_evaluator._validate_tree`.

## Policy/contract section sync

Policy `required_sections` are derived from the artifact contracts (source of truth for section names and order). To regenerate them or detect drift:

```bash
# Rewrite policies in place when out of sync
python .agents/harness/sync_required_sections.py

# Fail (exit 1) if any policy is out of sync with its contract
python .agents/harness/sync_required_sections.py --check
```

The test suite runs the `--check` mode, so a contract change that renames or reorders sections fails the tests until the policies are re-synced.

## Recovery decision trees

When a harness trigger fails and the `decision_trees` feature flag is enabled, the Orchestrator evaluates recovery routing via:

```bash
python .agents/harness/runner.py decide \
  --session <uuid> \
  --trigger <HXX> \
  --vars '<json>'
```

## Harness metrics

Each trigger execution records its duration in `HARNESS_REPORT.md`. The report includes a `## Metrics` section with invocations, `PASS`/`FAIL` results, and average duration per trigger.

## Runner tests

Automated runner tests live in `.agents/harness/tests/` and run with:

```bash
python -m pytest .agents/harness/tests/ -v
```

They are separate from user-project tests.
