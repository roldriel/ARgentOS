# Protocol Skills Index

Protocol skills live under `.agents/skills/<name>/`. They are general, generic capabilities, immutable like the rest of `.agents/`. The format contract is defined in `.agents/skills/README.md`; activation mechanics in `.agents/standards/orchestration/SKILLS.md`.

## Skill inventory

One row per protocol skill. The structural test `.agents/harness/tests/test_protocol_skills.py` validates that every row exists on disk with valid front matter, and that every skill directory is listed here.

| Skill | Description |
| --- | --- |
| suggest-commits | Analyze git changes and propose logical Conventional Commits grouped by intent rather than file boundaries. Activated by judgment (its `description` covers the triggers); intentionally not in the activation table below, because commit suggestion is a standalone task rather than a phase+profile combination. |

## Activation table

Declarative, auditable mapping used by the Orchestrator during `ANALYZING_TASK`/`PLANNING`. Its classification axis reuses decisions the Orchestrator already makes — **workflow phase + selected profile** — so no parallel task taxonomy is introduced. The Orchestrator MAY also activate a skill outside this table when the skill's `description` justifies it, recording the activation and its reason in `SESSION_LOG.md` (see `.agents/standards/orchestration/SKILLS.md`).

| Workflow phase | Profile | Skills |
| --- | --- | --- |
| _(none yet)_ | | |

Format example:

```text
| 06-execute | database_engineer | db-migration-semver |
```
