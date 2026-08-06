+++
trigger = "D01"
transition = "DISCOVERY_VALIDATE → DISCOVERY_READY"
artifact = "KB_DISCOVERY_ENTRY.md"
required_sections = []
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: discovery
harness_id: D01
name: discovery-output
lifecycle: discovery
tag: discovery
state: discovery:DISCOVERY_VALIDATE
gates:
  - "discovery:DISCOVERY_VALIDATE -> discovery:DISCOVERY_READY"
artifact_validated: KB_DISCOVERY_ENTRY.md
---

# Harness Policy D01: Discovery Output

## Trigger

`DISCOVERY_VALIDATE → DISCOVERY_READY` (domain `discovery`)

## Purpose

Validate the discovery output before publishing it. D01 is responsible for
BOTH the structural validation and the ground truth of the knowledge base:

- **Structural:** every KB entry and the manifest comply with their contracts
  (required fields and sections present, provenance fields populated).
- **Ground truth:** every claim in the knowledge base must have a source in
  the real project or in the real execution environment, and the merge
  performed by the `synthesis_worker` must not have introduced
  inconsistencies.

D01 is the single validation gate of the discovery domain
(`DISCOVERY_VALIDATE → DISCOVERY_READY`). The core trigger
`core:H10-kb-discovery-report` does NOT participate in the discovery cycle;
it only validates the per-task `KB_RECOMMENDATION.md` artifact in
`core:GATHERING_CONTEXT`.

## Input

- Current state: `DISCOVERY_VALIDATE`
- Target state: `DISCOVERY_READY`
- KB entries: `.project/knowledge/discovery/*.md`
- Manifest: `.project/knowledge/discovery/.discovery_manifest`
- Entry contract: `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`

## Checklist

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment. Today this policy declares no `required_sections` or semantic checks in its front matter, so every item is `[agent]`; per §"Implementation Note", the items with deterministic structure (entry existence, `source_files` path existence, required fields and sections) are the candidates to become `[machine]` when D01 is implemented in code.

1. **Real stack:** every language/framework listed in `stack.md` comes from a
   real configuration file (e.g., `pyproject.toml`, `package.json`,
   `Dockerfile`). `[agent]`
2. **Real dependencies:** every dependency listed in `dependencies.md` appears
   in a real configuration file. `[agent]`
3. **Observed patterns:** every pattern in `development_patterns.md` has a
   verifiable example in its `source_files`. `[agent]`
4. **Environment without secrets:** `environment.md` contains no sensitive
   strings and no environment variable values. `[agent]`
5. **Real source files:** every `source_files` entry points to an existing
   path, except `"system_probe"` (valid only for environment entries). `[agent]`
6. **No unsourced claims:** qualitative claims are backed by `source_files` or
   by session artifacts. `[agent]`
7. **Consistent merge:** the `synthesis_worker` did not lose information and
   did not leave conflicts unmarked; every entry carries `source_workers` and
   `source_files` preserving provenance. `[agent]`
8. **Structural compliance:** every KB entry exists, is non-empty, and
   contains the required fields and sections of its contract
   (`.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md` and the
   per-entry contracts), and the manifest lists every published entry. `[agent]`
9. **New entries present:** `executive_summary.md`, `file_map.md`,
   `entrypoint.md`, `api.md` and `glossary.md` exist and follow their
   contracts; `executive_summary.md` declares the `project_shape` in its first
   line, matching the manifest. `[agent]`
10. **Distribution rule:** `distribution.md` is present when the declared
    `project_shape` is `library` or `cli`; it may be legitimately absent for
    any other shape. `[agent]`
11. **API surface matches shape:** the content of `api.md` matches the
    `project_shape` declared in the manifest (variant rules of
    `.agents/orchestrators/discovery/contracts/API_SURFACE.md`). `[agent]`
12. **Required sections:** `architecture.md` contains
    `## Module Responsibilities`, `## Strong Couplings`, `## Security` and
    `## Extension Points`; `configuration.md` contains
    `## Run, Build and Release`; `database.md` contains `## Main Models`;
    `dependencies.md` contains `## Internal Dependencies`; `stack.md` contains
    `## Compatibility Constraints`; `development_patterns.md` covers
    `## Testing`, `## Logging and Errors` and `## Validation`;
    `technical_debt.md` contains `## Top Risks`. `## Performance Invariants`
    is required only when evidenced. `[agent]`

## Rejection of Invented Outputs

If D01 detects a claim without a source:

1. Mark the offending file as invalid.
2. Report it to the Discovery Orchestrator.
3. The Discovery Orchestrator decides to retry the affected worker or to
   report `discovery:DISCOVERY_FAILED`.

## Decision Criteria

- `PASS`: All checklist items are satisfied (structure and ground truth).
- `FAIL`: Any entry violates its contract, contains unsourced claims,
  nonexistent `source_files`, leaked secrets, or provenance lost during the
  merge.

## On Failure

The Discovery Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Re-invoke the worker that produced the invalid entry (once), or
3. Transition to `discovery:DISCOVERY_FAILED` if the failure repeats, and
   report to the core Orchestrator (see
   `.agents/orchestrators/discovery/harness/decision_trees/D01_FAIL.toml`).

## Implementation Note

D01 may be implemented in Python as part of the harness. The harness is the
guardian of the protocol and may contain code; this does not violate the
principle that `.agents/` are instructions, because the harness is not an
instruction for the agent.
