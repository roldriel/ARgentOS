+++
artifact = "KB_DISCOVERY_REPORT.md"
phase = "n/a"
produced_by = "context_discoverer"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: KB_DISCOVERY_REPORT.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_INIT]
consumed_by: [core:GATHERING_CONTEXT]
---

# Contract: KB Discovery Report

## Scope

This artifact is produced by the `context_discoverer` worker. It is **not** a main workflow phase artifact; it is optional and runs during context gathering when the `knowledge_base` feature flag is enabled.

## Purpose

The `KB_DISCOVERY_REPORT.md` artifact records which Knowledge Base entries the `context_discoverer` recommends for the current phase, why they are relevant, and the recommended context budget.

## Required sections

1. `## Discovery Objective` — what the discoverer was asked to find.
2. `## Recommended Entries` — list of recommended KB entries with priority, sections to include, and reason.
3. `## Context Budget Recommendation` — recommended KB context budget in characters.
4. `## Notes` — caveats or reasons to ignore recommendations.

## Optional embedded JSON

The report may include a machine-readable JSON block (for example, inside a fenced code block) with the following shape:

```json
{
  "discovery_objective": "string",
  "recommended_entries": [
    {
      "session_uuid": "string",
      "priority": 1,
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
