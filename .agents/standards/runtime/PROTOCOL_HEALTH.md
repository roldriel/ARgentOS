# Protocol Health Standard

## Purpose

Define what "a healthy protocol environment" means and how the ArgentOS System Agent verifies it during bootstrap (`system:VERIFYING_PROTOCOL_HEALTH`, gated by harness trigger `S00`).

The guiding criterion: **documents are verified against documents by the agent; claims against the filesystem that gate execution stay mechanical**. Most of the health check is judgment applied over the repository (required files exist, front matter is consistent); only the `state.json` write/read probe remains executable, because hook enforcement depends on `.project/` being writable and that claim must be verified against the filesystem itself.

## When it runs

The System Agent applies this checklist at session bootstrap when either condition holds:

- `.project/.last_health_check` does not exist, or
- its timestamp is older than the configured TTL: `ttl_hours` in `.agents/features.toml` `[health_check]` (default 24), overridable via the `AGENTS_HEALTH_CHECK_TTL_HOURS` environment variable.

On PASS, the System Agent writes the current UTC timestamp (ISO-8601) to `.project/.last_health_check`. On FAIL, the blocking rule of `.agents/orchestrators/system/states/SYSTEM_STATE_MACHINE.md` (`BOOTSTRAP_FAILED`, canonical rule) applies.

## Checklist

Each item is marked `[machine]` — verified deterministically by executable harness code — or `[agent]` — verified by the System Agent reading the protocol tree.

1. **Required directories exist.** `[agent]`
   - `.agents/orchestrators/core/states/`
   - `.agents/roles/`
   - `.agents/orchestrators/core/workflow/`
   - `.agents/contracts/`
   - `.agents/harness/policies/`
2. **Required index files exist and are non-empty.** `[agent]`
   - `.agents/INDEX.md`
   - `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`
   - `.agents/orchestrators/core/roles/orchestrator.md`
3. **Contract front matter is consistent.** `[agent]` Every contract in `.agents/contracts/*.md` and `.agents/orchestrators/*/contracts/*.md` starts with a TOML front matter block (`+++`) declaring `artifact`, `phase` and `produced_by`, and the `artifact` value matches the file name.
4. **Rubrics configuration (only when the `rubrics` flag is enabled).** `[agent]` `.agents/standards/quality/RUBRICS.md`, `.agents/roles/reviewer.md` and `.agents/roles/verifier.md` exist.
5. **Knowledge base layout (only when the `knowledge_base` flag is enabled).** `[agent]` `.project/knowledge/INDEX.md`, `.agents/standards/context/CONTEXT.md`, `.agents/roles/context_discoverer.md`, `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md` and `.agents/contracts/SESSION_LOG.md` exist. (The System Agent initializes `.project/knowledge/` before applying this item; see `.agents/orchestrators/system/roles/argentos.md`.)
6. **Technical-practice standards (one per enabled technical-practice flag).** `[agent]` For every technical-practice flag enabled in `.agents/features.toml`, its standard document exists. The flag → standard mapping is the technical-practice catalog of `.agents/standards/INDEX.md` (e.g. `tdd` → `.agents/standards/testing/TDD.md`, `srp` → `.agents/standards/development/design/SOLID/SRP.md`).
7. **Project skills (non-blocking).** `[agent]` When `.project/skills/` exists, each skill directory contains a `SKILL.md` with YAML front matter declaring `name` (matching the directory name) and `description`, and every `references/<file>` cited in the body exists on disk (format contract: `.agents/skills/README.md`). An invalid project skill produces a WARNING, is excluded from activation for the session, and never fails this checklist.
8. **State storage probe.** `[machine]` `python .agents/harness/health_check.py` exits with code `0` and reports `"result": "PASS"`: a write/read/delete round-trip of a probe file inside `.project/` succeeds, so `state.json` (`.agents/harness/runner_state.py`) can be persisted.
9. **Timestamp sanity.** `[agent]` If `.project/.last_health_check` exists, its timestamp is not in the future.

## Decision

- **PASS**: items 1–6, 8 and 9 hold (item 7 only emits warnings).
- **FAIL**: any of items 1–6, 8 or 9 fails. The System Agent reports the failing items and transitions to `system:BOOTSTRAP_FAILED`.
