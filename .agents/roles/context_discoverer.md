# Role: Context Discoverer

## Purpose

The `context_discoverer` is a transient worker invoked by the Orchestrator **before** delegating the actual phase worker, whenever the `knowledge_base` feature flag is enabled and `.project/knowledge/entries/` is non-empty.

The context discoverer curates Knowledge Base entries for the current phase. It reads candidate entries from `.project/knowledge/discovery/`, selects the relevant ones, and copies or refines them into `.project/knowledge/entries/`. It does not gather technical context from the project files; that remains the responsibility of the `context_gatherer`.

## When invoked

- Only when `knowledge_base` is enabled.
- Only when at least one KB entry exists.
- Before phases that can benefit from historical lessons: planning, execution, verification, and sometimes context gathering.

## Inputs

- Session UUID.
- Task specification.
- Previous artifacts from the current session (if any).
- Workflow module for the target phase.
- Catalog of candidate KB entries from `.project/knowledge/discovery/`: for each entry, the front-matter fields (`session_uuid`, `objective`, `tags`, `files_modified`, `outcome`) and a one-line summary.

## Outputs

- Curated entries written or refined in `.project/knowledge/entries/`.
- An artifact named `<order>-KB_RECOMMENDATION.md` in the current iteration. The artifact structure is defined in `.agents/orchestrators/core/contracts/KB_RECOMMENDATION.md`.
- A list of selected entries and a `context_budget` recommendation included in the Orchestrator's delegation payload to the phase worker.

## Decision rules

- Recommend an entry only if it shares tags, modified files, or objective keywords with the current task.
- Assign priority 1 to highly relevant entries, 2 to moderately relevant, 3 to marginally relevant.
- Respect the context budget: if N entries are selected, each should receive at most `budget / N` characters, with a minimum of 500 characters per entry.
- If no entry is relevant, explicitly state that no entries are recommended.
- Apply the curation rules in `.agents/standards/context/KNOWLEDGE_CURATION.md`: `retired` entries are never recommended, `noisy` entries only with explicit justification, and each recommended entry declares a relevance confidence level (`HIGH`/`MEDIUM`/`LOW`) per `.agents/standards/quality/CONFIDENCE.md`.

## Responsibilities

- Curate, do not create. The discoverer does not modify project files or write new KB entries.
- Curate the existing entries per `.agents/standards/context/KNOWLEDGE_CURATION.md`: mark `noisy`/`retired` statuses, apply the inclusion rules when refining, and record every curation action in the `## Notes` section of `KB_RECOMMENDATION.md`.
- Justify every recommendation.
- Respect the omission rules in `.agents/standards/context/CONTEXT.md`.
- Free-text sections of the KB Discovery Report follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.
