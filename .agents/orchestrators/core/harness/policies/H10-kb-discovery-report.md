+++
trigger = "H10"
transition = "Before using KB recommendations (optional)"
artifact = "KB_RECOMMENDATION.md"
required_sections = [
  "Discovery Objective",
  "Recommended Entries",
  "Context Budget Recommendation",
  "Notes"
]
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H10
name: kb-discovery-report
state: core:GATHERING_CONTEXT
lifecycle: context
gates:
  - "core:GATHERING_CONTEXT -> core:CONTEXT_GATHERED"
artifact_validated: KB_RECOMMENDATION.md
---

# Harness Policy H10: KB Recommendation Report (optional)

## Trigger

Before using KB recommendations (optional gate)

## Purpose

Structural validation of the `KB_RECOMMENDATION.md` artifact produced by the `context_discoverer`. H10 verifies that the recommendation report exists and contains the required sections of its contract.

Validation of the discovery knowledge base itself (entries, manifest, structure, and ground truth) belongs to the discovery domain: see `D01-discovery-output` and the contracts under `.agents/orchestrators/discovery/contracts/`.

H10 does NOT participate in the discovery cycle (`discovery:DISCOVERY_VALIDATE` is gated only by `D01`). Its scope is limited to the per-task `KB_RECOMMENDATION.md` artifact produced by the `context_discoverer` during `core:GATHERING_CONTEXT`.

## Input

- Artifact: `.project/<session-uuid>/<iteration>/<order>-KB_RECOMMENDATION.md`
- Contract: `.agents/orchestrators/core/contracts/KB_RECOMMENDATION.md`

## Decision Criteria

**Evaluation audience:** each criterion is marked `[machine]` — validated deterministically by the harness runner (artifact existence and presence of the `required_sections` declared in this policy's front matter) — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

`PASS` when all of the following hold; `FAIL` otherwise:

- The artifact exists. `[machine]`
- All required sections are present: `Discovery Objective`, `Recommended Entries`, `Context Budget Recommendation`, `Notes`. `[machine]`
- The report does not include full artifacts from previous sessions. `[agent]`
- The report does not include credentials, tokens, or personal data. `[agent]`

## Note

This trigger is optional in the current state machine. The Orchestrator may invoke it when the `knowledge_base` feature flag is enabled and stricter validation is desired.
