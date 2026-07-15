+++
artifact = "KB_DISCOVERY_REPORT.md"
phase = "02b"
produced_by = "context_discoverer"
+++

# Contract: KB Discovery Report

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
