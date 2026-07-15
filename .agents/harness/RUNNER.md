# Harness Runner

This document describes the executable runner (`runner.py`) that the Orchestrator invokes to validate artifacts, list feature flags, run health checks, and evaluate recovery decision trees.

For the harness concept, trigger catalog, and policies, see `.agents/harness/INDEX.md`.

## Artifact validation

The Orchestrator invokes the runner from the CLI:

```bash
python .agents/harness/runner.py --session <uuid> --trigger H01 [--iteration 00]
```

If `--iteration` is not specified, the runner finds the most recent iteration containing the target artifact.

The runner:

- Reads the corresponding policy from `.agents/harness/policies/`.
- Validates the artifact against the contract.
- Updates `HARNESS_REPORT.md` at the session root.
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

The orchestrator runs it automatically at the start of a session if `.project/.last_health_check` does not exist or is older than `ttl_hours` (default 24, configurable in `.agents/features.toml` or via `AGENTS_HEALTH_CHECK_TTL_HOURS`).

The `health-check` subcommand verifies that critical directories exist, index files are readable, and features enabled by feature flags are well-formed. If it passes, it updates `.project/.last_health_check` with the current timestamp.

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
