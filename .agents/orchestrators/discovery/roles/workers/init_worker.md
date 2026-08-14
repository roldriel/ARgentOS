---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: discovery
worker_id: init_worker
subsystem: discovery
state: discovery:DISCOVERY_INIT
lifecycle: discovery
actor: discovery_orchestrator
input_artifacts: []
output_artifacts: [discovery_input.json, invalidation_report.json, KB_DISCOVERY_REPORT.md, file_map.md]
---

# Worker: init_worker

## Purpose

Prepare the context of a discovery run: read the previous KB and the session
artifacts, compute hash-based invalidations and produce the structured input for
the remaining workers.

## Input

- `project_root`: root path of the project under discovery.
- `scope`: one of `full`, `env`, `stack`, `patterns`, `business`.
- `previous_kb`: contents of `.project/knowledge/discovery/`, if present.
- `session_artifacts`: relevant artifacts from previous sessions
  (`SESSION_LOG.md`, `CONTEXT_ARTIFACT.md`, `EXECUTION_SUMMARY.md`,
  `RECOVERY_REPORT.md`, `VERIFICATION_REPORT.md`).

## Output

- `discovery_input.json` — an `INTER_WORKER_MESSAGE` message with
  `payload_type: "discovery_input"`, addressed to each worker selected by the
  scope. `provenance` does not apply to this message (see the contract).
- `invalidation_report.json` — list of KB entries that became stale, with the
  reason (hash change, TTL, etc.).
- `KB_DISCOVERY_REPORT.md` — the initialization report of the run (objective,
  scope and inputs, invalidation summary, selected workers), following
  `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_REPORT.md`. Written to
  the session artifact directory as `<order>-KB_DISCOVERY_REPORT.md`; validated
  by gate `D00-discovery-init`.
- `file_map.md` — an annotated `path → responsibility` index of the main
  folders and relevant files of the project, written to
  `.project/knowledge/discovery/file_map.md` and following the base KB entry
  contract `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`.
  It is NOT a full directory tree: only what an agent needs to navigate.

The intermediate outputs are written to `.project/<session-uuid>/discovery/`
following the intermediate-working-directory mechanism (Option A).

## Tasks

1. Read the previous KB: `.project/knowledge/discovery/` entries and
   `.discovery_manifest` (contract: `DISCOVERY_MANIFEST.md`).
2. Read the relevant session artifacts.
3. Compute the hashes of the configuration files, sample files and environment,
   and compare them against the `[hashes]` section of the manifest to determine
   which entries are stale.
4. On the first run over a legacy KB (entries without provenance fields), mark
   those entries in the manifest with `confidence: low` and `status: legacy`.
   Legacy entries are never deleted without a trace.
5. Prepare `discovery_input.json` for the workers selected by the scope,
   reading `discovery_context_budget`, `discovery_sample_size` and
   `discovery_sample_size_per_language` from `.agents/features.toml` and
   writing them as `context_budget`, `sample_size` and
   `sample_size_per_language`, plus the list of previous KB entries
   each worker must consider.
6. Classify the project into a `project_shape` — one of `library`, `cli`,
   `service`, `application`, `monorepo` or `unknown` — using deterministic
   signals:
   - Distributable package manifest without run scripts and with an empty
     entry-point table → `library`.
   - `console_scripts` entry points or a `bin/` directory → `cli`.
   - A web framework in the dependencies → `service`.
   - A `Dockerfile` plus a main entry → `application`.
   - Multiple package manifests of the shapes above → `monorepo`.
   Signal priority when several match: `cli` > `service` > `library` >
   `application`; `monorepo` overrides every other shape when multiple
   sub-projects exist. If no signal matches, the shape is `unknown`.
7. Record the `project_shape` in the `discovery_input.json` payload so every
   downstream worker knows which contract variant to produce, and in the
   `[knowledge_base]` section of the manifest (via `synthesis_worker`).
8. Build `file_map.md` during the sampling walk the worker already performs:
   annotate each main folder and relevant file with its responsibility, so an
   agent can navigate the project without exploratory search.
9. Compute the `structure_hash` (hash of the directory tree shape) so the
   manifest can invalidate `file_map.md` when the tree changes.

## Guardrails

- Pure instruction text; model-agnostic; no Python assumptions.
- Read-only with respect to the project: never modify project source files.
- Writes only to `.project/<session-uuid>/discovery/` and to
  `.project/knowledge/discovery/file_map.md`.
- Never delete KB entries; invalidations are reported, not applied.

## Retries

- Maximum 3 retries, backoff 1s, 2s, 4s.
- This worker is critical: if it fails after all retries, the Discovery
  Orchestrator reports `discovery:DISCOVERY_FAILED`.
