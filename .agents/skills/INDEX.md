# Protocol Skills Index

Protocol skills live under `.agents/skills/<name>/`. They are general, generic capabilities, immutable like the rest of `.agents/`. The format contract is defined in `.agents/skills/README.md`; activation mechanics in `.agents/standards/orchestration/SKILLS.md`.

Every skill in this index is *integrated*: it is referenced by name from a worker role, workflow phase, or harness policy outside `.agents/skills/` (see `plans/rfc/24-skill-lifecycle-model.md`). Skills without such a consumer are removed from the catalog.

## Skill inventory

One row per protocol skill. There is no executable structural test anymore: the Orchestrator verifies by judgment (protocol health checklist, item 7, for project skills; H13 coherence for protocol files) that every row exists on disk with valid front matter and that every skill directory is listed here.

| Skill | Description |
| --- | --- |
| ears-writer | Draft requirements and acceptance criteria in EARS notation. |
| task-spec-validator | Verify a Task Specification against its contract and the EARS standard. |
| artifact-validator | Validate a protocol artifact against its contract. |
| rubric-checker | Evaluate a deliverable against the protocol rubrics. |
| execution-plan-reviewer | Review an execution plan before approval. Activated by judgment (reviewer delegations over `EXECUTION_PLAN.md`; see `.agents/roles/reviewer.md`). |
| critic | Critique a proposal, identifying weaknesses before execution. |
| ambiguity-detector | Detect ambiguities that require explicit clarification before proceeding. |
| consistency-checker | Detect inconsistencies within or between artifacts. |
| completeness-checker | Detect missing information against what the requested deliverable requires. |
| requirement-extractor | Extract functional and non-functional requirements from the user's request. |
| extractor | Extract relevant facts from extensive material, with citations. |
| summarizer | Summarize extensive material preserving decision-relevant content. |
| planner | Decompose an objective into ordered, verifiable steps. |
| self-review | Self-evaluate the result before reporting it. |
| markdown-formatter | Produce Markdown consistent with the protocol's artifact conventions. Activated by judgment (artifact-producing delegations; see `.agents/roles/worker.md` §"Skill Consumption"). |
| normalizer | Normalize terminology and format across sources. |
| reference-resolver | Resolve references between project and protocol documents. |
| intent-detector | Detect the intent of a task and its confidence level. |
| goal-extractor | Identify explicit and implicit objectives of the user's request. |
| constraint-extractor | Detect technical, scope, and business constraints. |
| risk-detector | Detect potential risks of a plan or proposal. |
| decision-extractor | Identify decisions already made in session artifacts. Activated by judgment (scope-compliance verification; see policy H07). |
| tradeoff-analyzer | Analyze advantages and disadvantages of alternatives. |
| hypothesis-generator | Generate falsifiable hypotheses for a failure or unexpected behavior. |
| reflection | Re-evaluate an in-progress solution before finalizing it. Activated by judgment. |
| hallucination-checker | Confront an artifact's claims with available evidence. |
| tdd-reviewer | Review a plan or change for TDD-cycle compatibility. |
| context-validator | Assist validation of the gathered context against its report contract. |
| deduplicator | Remove redundancy across gathered sources, preserving a canonical cited instance. |
| formatter | Reformat output into a declared target structure (JSON, YAML, CSV, table, Markdown). Activated by judgment (artifact-producing delegations; see `.agents/roles/worker.md` §"Skill Consumption"). |
| terminology-enforcer | Enforce the protocol's canonical vocabulary in artifacts. Activated by judgment (see policy H13, §"Agent-side enforcement"). |
| suggest-commits | Analyze git changes and propose logical Conventional Commits grouped by intent. Utility skill for the adopting project (user-invoked, not part of the task workflow; outside the activation table by design). |

## Activation table

Declarative, auditable mapping used by the Orchestrator during `ANALYZING_TASK`/`PLANNING`. Its classification axis — **workflow phase + selected profile** — is confirmed as the complete structure for declarative candidacy: it reuses decisions the Orchestrator already makes, so no parallel task taxonomy is introduced. The concepts the axis does not express (description sufficiency, justified override in its activation and omission forms) are properties of the activation process, defined in `.agents/standards/orchestration/SKILLS.md` (§"Activation"), not missing columns of this table. The Orchestrator MAY also activate a skill outside this table when the skill's `description` justifies it, recording the activation and its reason in `SESSION_LOG.md` (see `.agents/standards/orchestration/SKILLS.md`).

| Workflow phase | Profile | Skills |
| --- | --- | --- |
| 00-analyze-task | task_analyst | requirement-extractor, goal-extractor, constraint-extractor, ambiguity-detector, intent-detector |
| 01-confirm-intent | intent_reflector | ambiguity-detector |
| 02-build-task-specification | functional_writer | ears-writer, task-spec-validator |
| 03-gather-context | context_gatherer | extractor, deduplicator, normalizer, summarizer |
| 04-validate-context | context_validator | context-validator, completeness-checker |
| 05-plan | planner | planner, risk-detector, tradeoff-analyzer, critic |
| 06-execute | executor (any execution profile) | self-review, tdd-reviewer |
| 07-verify | qa_engineer | rubric-checker, artifact-validator, consistency-checker, hallucination-checker, reference-resolver |
| 08-recovery | recovery_analyst | hypothesis-generator, risk-detector |

Format example:

```text
| 06-execute | database_engineer | db-migration-semver |
```
