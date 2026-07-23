+++
artifact = "KB_DISCOVERY_REPORT.md"
phase = "00-discovery-init"
produced_by = "init_worker"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: KB_DISCOVERY_REPORT.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_INIT]
consumed_by: [discovery:DISCOVERY_RUNNING]
---

# Contract: KB Discovery Report

## Scope

This artifact is the initialization report of a discovery run. It is produced by the `init_worker` during `discovery:DISCOVERY_INIT` and validated by gate `D00-discovery-init` before the run proceeds to `discovery:DISCOVERY_RUNNING`.

Do not confuse it with `KB_RECOMMENDATION.md` (core domain), which records the per-task KB entry recommendations of the `context_discoverer`.

## Purpose

The `KB_DISCOVERY_REPORT.md` artifact records how the discovery run was initialized: the scope and inputs used, which previous KB entries were invalidated, and which workers were selected for the run.

## Required sections

1. `## Discovery Objective` — what the discovery run was asked to analyze.
2. `## Scope and Inputs` — the discovery scope (`full`, `env`, `stack`, `patterns`, or `business`) and the inputs used (project root, previous KB, session artifacts).
3. `## Invalidation Summary` — previous KB entries that became stale, with the reason (hash change, TTL, legacy), or an explicit "none" statement. Details live in `invalidation_report.json`.
4. `## Selected Workers` — the workers selected for the run according to the scope.
5. `## Notes` — caveats, assumptions, or reasons the run may be partial.

## Constraints

- The report must record the discovery scope and inputs used for the run (gate D00 checklist).
- The report must not include credentials, tokens, or personal data.
- Machine-readable outputs of the initialization (`discovery_input.json`, `invalidation_report.json`) live in `.project/<session-uuid>/discovery/`; this report summarizes them, it does not replace them.
