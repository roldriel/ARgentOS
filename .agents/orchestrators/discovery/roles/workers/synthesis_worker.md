---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: discovery
worker_id: synthesis_worker
subsystem: discovery
state: discovery:DISCOVERY_MERGE
lifecycle: discovery
actor: discovery_orchestrator
input_artifacts: [worker_environment.json, worker_stack.json, worker_framework.json, worker_patterns.json, worker_business.json]
output_artifacts: [summary.md, .discovery_manifest]
---

# Worker: synthesis_worker

## Purpose

Merge the partial outputs of all workers, resolve conflicts against the previous
KB, enrich the result with session artifacts, and write the consolidated KB and
its manifest. It runs in the `DISCOVERY_MERGE` state and is the single merge
point of the pipeline.

## Input

- All available partial outputs (`worker_<name>.json` files under
  `.project/<session-uuid>/discovery/`, `INTER_WORKER_MESSAGE` contract).
- The previous KB (`.project/knowledge/discovery/` + `.discovery_manifest`).
- The session artifacts (`SESSION_LOG.md`, `CONTEXT_ARTIFACT.md`,
  `EXECUTION_SUMMARY.md`, `RECOVERY_REPORT.md`, `VERIFICATION_REPORT.md`).
- The `invalidation_report.json` produced by `init_worker`.

## Output

- `summary.md`, written to `.project/knowledge/discovery/summary.md`.
- `.discovery_manifest`, written to
  `.project/knowledge/discovery/.discovery_manifest`, following the contract
  `.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md`.
- The consolidated KB entries, updated with provenance fields (`updated_at`,
  `source_workers`, `source_sessions`, `status`).

## Tasks

1. Merge the partial outputs.
2. Apply the KB merge rules:
   - If a new finding contradicts a previous one:
     - New `confidence: high` vs previous `confidence: low` → replace.
     - Both `confidence: high` → report the conflict in `summary.md` and in the
       entry's `## Notes`.
     - Previous entry comes from a recent session → keep the previous one and
       mark the new finding as `confidence: low`.
   - Never delete an entry without leaving a trace in the manifest.
   - Invalidated entries are marked `status: stale` in the manifest, not
     removed from history.
3. Resolve conflicts.
4. Enrich entries with session artifacts.
5. Preserve every `source_files` and `source_workers` value from the partial
   outputs — no provenance may be lost in the merge.
6. Write the manifest (`[knowledge_base]`, `[hashes]`, `[entries]`, `[workers]`,
   `[runtime]`), recording which workers were invoked and which completed
   (including partial degradations).

## Guardrails

- Pure instruction text; model-agnostic; no Python assumptions.
- Writes only to `.project/knowledge/discovery/`.
- No unresolved conflicts may remain: every contradiction must be resolved by
  the merge rules or explicitly reported in `summary.md` (validated by
  `D01-discovery-output`).

## Retries

- Maximum 3 retries, backoff 1s, 2s, 4s.
- This worker is critical: if it fails after all retries, the Discovery
  Orchestrator reports `discovery:DISCOVERY_FAILED`.
