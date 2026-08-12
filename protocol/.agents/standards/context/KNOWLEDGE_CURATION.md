# Knowledge Curation Standard

## Purpose

Define what deserves to become a Knowledge Base entry under `.project/knowledge/entries/` and how existing entries are kept clean over time. Without a filter, the KB fills with trivialities that dilute the valuable entries and burn the context budget of every session.

## Inclusion rules

An entry is only justified when it records knowledge that **cannot be inferred from the repository itself**. Concretely:

- **Decisions**: an entry about a decision is valid only if an alternative was discarded for a stated technical reason. Without an alternative, it is not a decision — it is a chronicle.
- **Explorations**: an entry about an open question is valid only if the question is concrete and its answer is not yet in the codebase or docs.
- **Lessons**: an entry about a lesson is valid only if the lesson is non-obvious. The test: "does the agent now know something it could not have derived from `git log`, the code, or existing docs?"

The following MUST NOT be recorded:

- TODOs, reminders, or task-tracking notes.
- Anything derivable from `git log`, source code, or existing documentation.
- Mechanical protocol steps ("phase 06 executed", "artifact written").

## Before creating an entry

1. Search for duplicates or overlapping entries; update the existing one instead of creating a new one.
2. Keep it concise: at most three sentences of substantive content.
3. Answer the inclusion test above explicitly; if it fails, do not create the entry.

## Entry lifecycle: `curation_status`

Entries are never deleted without a trace. Their front matter carries a `curation_status` field:

| Value | Meaning |
|---|---|
| `active` | Current and useful; eligible for recommendation. |
| `noisy` | Detected as low-value or redundant; kept for traceability but downgraded. |
| `retired` | No longer applicable (superseded or obsolete); excluded from recommendations. |

Transitions:

- The `context_discoverer` marks an entry `noisy` when it fails the inclusion rules or duplicates a better entry, and records the reason in `KB_RECOMMENDATION.md` under `## Notes`.
- An entry moves to `retired` when its knowledge is superseded or no longer true; the superseding entry (if any) is referenced.
- Default status for new entries is `active`.

## Curation duties of the `context_discoverer`

- When selecting entries for a phase, `noisy` entries are recommended only with explicit justification; `retired` entries are never recommended.
- When refining entries copied into `.project/knowledge/entries/`, apply the inclusion rules and the conciseness limit.
- Record every curation action (status change, merge, refusal to create) in the `## Notes` section of `KB_RECOMMENDATION.md`.
