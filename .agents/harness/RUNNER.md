# Harness Runner

This document describes the executable runner (`runner.py`) that the Orchestrator invokes to validate artifacts.

For the harness concept, trigger catalog, and policies, see `.agents/harness/INDEX.md`.

## Module layout

The runner is split into focused modules under `.agents/harness/`; `runner.py` is the CLI entry point and re-exports the public API (`import runner` keeps working):

- `runner_paths.py` — shared filesystem locations (policy dirs, artifacts dir).
- `runner_models.py` — `CheckResult` / `HarnessResult` dataclasses.
- `runner_markdown.py` — TOML front matter and Markdown section parsing helpers.
- `runner_policies.py` — policy loading across domains (core `H*`, discovery `D*`, system `S*`, cross-cutting).
- `runner_artifacts.py` — artifact path resolution inside iteration folders.
- `runner_validators.py` — section, EARS, rubric and semantic validators, plus `run_trigger`.
- `runner_citations.py` — mechanical semantic checks: citation resolution (`path:section`, `path` §section and TOML citation fields must resolve against the filesystem) and test evidence (every executed `[[test_results]]` command needs an existing evidence file or a `SESSION_LOG.md` entry).
- `runner_report.py` — `HARNESS_REPORT.md` generation.
- `health_check.py` — state-storage probe: write/read round-trip inside `.project/` proving that `state.json` can be persisted. It is the only mechanical item of the protocol health verification; the document-level checklist lives in `.agents/standards/runtime/PROTOCOL_HEALTH.md` and is applied by the ArgentOS System Agent.
- `runner_state.py` — transactional `state.json` persistence (single source of truth of the iteration protocol state) and post-hoc bypass detection.
- `hook_gate.py` — standalone CLI lifecycle hook (stdlib only, run as a script): allows/denies `PreToolUse` writes to deliverables and `Stop` events against `state.json`. See `.agents/harness/INDEX.md` §Protocol State and Hook Enforcement.
- `delegation_validity.py` — delegation payload and return-report validity checks (policy H15; machine-evaluated via its test suite, not via the trigger CLI).

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

## Protocol health verification

Protocol health is verified by the ArgentOS System Agent, not by the runner: it applies the prose checklist of `.agents/standards/runtime/PROTOCOL_HEALTH.md` (required directories and files, contract front matter, flag-gated standards, project skills) and runs the state-storage probe:

```bash
python .agents/harness/health_check.py
```

The probe exits `0` when a write/read/delete round-trip inside `.project/` succeeds. The checklist runs at bootstrap when `.project/.last_health_check` is missing or older than `ttl_hours` (default 24, configured in `.agents/features.toml` `[health_check]`, overridable via `AGENTS_HEALTH_CHECK_TTL_HOURS`); on PASS the System Agent refreshes `.project/.last_health_check`.

## Policy/contract section resolution

Policy `required_sections` are resolved by reference from the artifact contracts (source of truth for section names and order): `runner_policies.resolve_required_sections()` parses the `##` headings of the contract cited by the policy's `artifact` key, excluding the non-normative headings listed in `runner_policies.NON_NORMATIVE_SECTIONS`. A policy that needs a deliberate subset of (or an opt-out from) the contract sections may still declare `required_sections` explicitly in its front matter; that declaration takes precedence. A policy whose contract cannot be resolved fails closed, as a malformed policy.

## Recovery decision tables

When a harness trigger fails, the Orchestrator applies the §"Recovery Decision Table" of the failed trigger's policy: an ordered rules table (conditions → recommended action and target phase) evaluated by agent judgment. There is no executable recovery component.

## Harness metrics

Each trigger execution records its duration in `HARNESS_REPORT.md`. The report includes a `## Metrics` section with invocations, `PASS`/`FAIL` results, and average duration per trigger.

## Protocol metrics aggregation

Protocol metrics (`.agents/standards/runtime/PROTOCOL_METRICS.md`) are aggregated by the agent on demand, following the procedure in that standard: read the `ENTRY` comments of `HARNESS_REPORT.md`, the `METRIC` comments of the session-level `METRICS.md` (contract: `.agents/contracts/METRICS.md`) and the iteration filesystem layout, and compute the metric catalog — per session or across every session under `.project/`. Aggregation is read-only; it never modifies session artifacts.

## Runner tests

Automated runner tests live in `.agents/harness/tests/` and run with:

```bash
python -m pytest .agents/harness/tests/ -v
```

They are separate from user-project tests.
