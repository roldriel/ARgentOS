# Protocol Skills Index

Protocol skills live under `.agents/skills/<name>/`. They are general, generic capabilities, immutable like the rest of `.agents/`. The format contract is defined in `.agents/skills/README.md`; activation mechanics in `.agents/standards/orchestration/SKILLS.md`.

## Skill inventory

One row per protocol skill. The structural test `.agents/harness/tests/test_protocol_skills.py` validates that every row exists on disk with valid front matter, and that every skill directory is listed here.

| Skill | Description |
| --- | --- |
| suggest-commits | Analyze git changes and propose logical Conventional Commits grouped by intent rather than file boundaries. Activated by judgment (its `description` covers the triggers); intentionally not in the activation table below, because commit suggestion is a standalone task rather than a phase+profile combination. |
| ears-writer | Draft requirements in EARS notation during task specification. |
| task-spec-validator | Verify a Task Specification against its contract and the EARS standard. |
| artifact-validator | Validate a protocol artifact against its contract. |
| rubric-checker | Evaluate a deliverable against the protocol rubrics. |
| execution-plan-reviewer | Review an execution plan before approval. |
| critic | Critique a proposal, identifying weaknesses before execution. Activated by judgment. |
| ambiguity-detector | Detect ambiguities that must trigger `NEEDS_CLARIFICATION`. |
| consistency-checker | Detect inconsistencies within or between artifacts. Activated by judgment. |
| completeness-checker | Detect missing information against what a phase requires. Activated by judgment. |
| requirement-extractor | Extract functional and non-functional requirements from the user's request. |
| extractor | Extract relevant facts from extensive material, with citations. Activated by judgment. |
| summarizer | Summarize extensive material preserving decision-relevant content. Activated by judgment. |
| planner | Decompose an objective into ordered, verifiable steps. Activated by judgment. |
| self-review | Self-evaluate the result before reporting it. |
| markdown-formatter | Produce Markdown consistent with the protocol's artifact conventions. Activated by judgment. |
| normalizer | Normalize terminology and format across sources. Activated by judgment. |
| reference-resolver | Resolve references between project and protocol documents. Activated by judgment. |
| intent-detector | Detect the intent of a task and its confidence level. |
| goal-extractor | Identify explicit and implicit objectives of the user's request. |
| constraint-extractor | Detect technical, scope, and business constraints. |
| risk-detector | Detect potential risks of a plan or proposal. |
| decision-extractor | Identify decisions already made in session artifacts. Activated by judgment. |
| decomposer | Divide complex problems into independent subproblems. Activated by judgment. |
| tradeoff-analyzer | Analyze advantages and disadvantages of alternatives. Activated by judgment. |
| counterargument | Build reasoned objections to a position. Activated by judgment. |
| hypothesis-generator | Generate falsifiable hypotheses for a failure or unexpected behavior. |
| reflection | Re-evaluate an in-progress solution before finalizing it. Activated by judgment. |
| hallucination-checker | Confront an artifact's claims with available evidence. Activated by judgment. |
| tdd-reviewer | Review a plan or change for TDD-cycle compatibility. Activated by judgment. |
| context-validator | Assist validation of the gathered context against its report contract. Activated by judgment. |
| deduplicator | Remove redundancy across gathered sources, preserving a canonical cited instance. Activated by judgment. |
| formatter | Reformat output into a declared target structure (JSON, YAML, CSV, table, Markdown). Activated by judgment. |
| terminology-enforcer | Enforce the protocol's canonical vocabulary in artifacts. Activated by judgment. |

## Activation table

Declarative, auditable mapping used by the Orchestrator during `ANALYZING_TASK`/`PLANNING`. Its classification axis — **workflow phase + selected profile** — is confirmed as the complete structure for declarative candidacy: it reuses decisions the Orchestrator already makes, so no parallel task taxonomy is introduced. The concepts the axis does not express (description sufficiency, justified override in its activation and omission forms) are properties of the activation process, defined in `.agents/standards/orchestration/SKILLS.md` (§"Activation"), not missing columns of this table. The Orchestrator MAY also activate a skill outside this table when the skill's `description` justifies it, recording the activation and its reason in `SESSION_LOG.md` (see `.agents/standards/orchestration/SKILLS.md`).

| Workflow phase | Profile | Skills |
| --- | --- | --- |
| 00-analyze-task | task_analyst | intent-detector, goal-extractor, constraint-extractor, requirement-extractor |
| 01-confirm-intent | intent_reflector | ambiguity-detector |
| 02-build-task-specification | functional_writer | ears-writer, task-spec-validator |
| 07-verify | qa_engineer | rubric-checker, self-review |
| 08-recovery | recovery_analyst | hypothesis-generator, risk-detector |

Format example:

```text
| 06-execute | database_engineer | db-migration-semver |
```
