+++
schema_version = "2.0.0"
artifact = "KB_RECOMMENDATION.md"
phase = "n/a"
produced_by = "context_discoverer"
enforcement = "gated"
gated_by = ["H10"]
+++
schema_version = "2.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: KB_RECOMMENDATION.md
lifecycle: context
produced_by: [core:GATHERING_CONTEXT]
consumed_by: [core:PLANNING, core:EXECUTING, core:VERIFYING]
---

# Contract: KB Recommendation

## Scope

This artifact is produced by the `context_discoverer` worker. It is **not** a main workflow phase artifact; it is optional and runs during context gathering when the `knowledge_base` feature flag is enabled.

Do not confuse it with `KB_DISCOVERY_REPORT.md` (discovery domain), which is the initialization report of a discovery run produced by `init_worker` in `discovery:DISCOVERY_INIT`.

## Purpose

The `KB_RECOMMENDATION.md` artifact records which Knowledge Base entries the `context_discoverer` recommends for the current phase, why they are relevant, and the recommended context budget.

## Required sections

1. `## Discovery Objective` — what the discoverer was asked to find.
2. `## Recommended Entries` — list of recommended KB entries with priority, relevance confidence (`HIGH`/`MEDIUM`/`LOW` per `.agents/standards/quality/CONFIDENCE.md`), sections to include, and reason. Each entry declares:
   - `- **Kind**: discovery | knowledge | lesson` — the type of the recommended
     entry (`discovery` for snapshots under `.project/knowledge/discovery/`,
     `knowledge` for curated entries under `.project/knowledge/entries/`,
     `lesson` for lesson claims under `.project/knowledge/entries/`).
   - `- **Path**: <resolvable location>` — the actual location of the entry
     (e.g. `.project/knowledge/discovery/environment.md` or
     `.project/knowledge/entries/<file>.md`). `session_uuid` is provenance,
     never the location.
3. `## Context Budget Recommendation` — recommended KB context budget in characters.
4. `## Notes` — caveats, reasons to ignore recommendations, curation actions (entries marked `noisy`/`retired` per `.agents/standards/context/KNOWLEDGE_CURATION.md`), and entries recommended with `LOW` relevance confidence.

## Optional embedded JSON

The report may include a machine-readable JSON block (for example, inside a fenced code block) with the following shape:

```json
{
  "discovery_objective": "string",
  "recommended_entries": [
    {
      "session_uuid": "string",
      "kind": "discovery",
      "path": ".project/knowledge/discovery/environment.md",
      "priority": 1,
      "confidence": "HIGH",
      "include_sections": ["lessons_learned"],
      "reason": "string"
    }
  ],
  "context_budget_recommendation": 4000,
  "notes": "string"
}
```

## Constraints

- The report must not include full artifacts from previous sessions.
- The report must not include credentials, tokens, or personal data.
- A claim that is expired or whose provenance does not resolve is never
  recommended (`.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` §Freshness
  per claim).
- Every recommendation is type-labeled: an entry without `kind` and `path` is
  non-conforming; snapshot, current knowledge and historical knowledge are
  never mixed without the tag.
