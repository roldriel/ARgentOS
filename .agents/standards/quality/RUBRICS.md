# Rubrics Standard

This document defines the quality rubrics used by the `.agents` protocol to evaluate artifacts produced during a session.

## Purpose

Rubrics provide observable, repeatable criteria for assessing artifacts. They are applied by LLM-based workers (`reviewer` before critical transitions, `verifier` during phase 07). The H06 gate only validates that the `## Rubric Evaluation` section exists and is structurally correct; it does **not** judge quality.

## Scale

Every criterion is scored with one of three levels:

- `INSUFFICIENT` — Does not meet the minimum requirement.
- `MEETS` — Satisfies the requirement.
- `EXCEEDS` — Goes beyond the requirement with clear evidence.

Critical criteria (marked with ✅) that are scored `INSUFFICIENT` force a `REWORK` recommendation from the `reviewer` or a `RECOVERY` decision from the `verifier`. `REWORK` is a recommendation from the reviewer, not a protocol state; the Orchestrator must translate it into an allowed transition.

## Rubrics

### 1. `TASK_SPECIFICATION_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Objective clarity** | ✅ | Objective is vague, missing, or not measurable. | Objective is clear, actionable, and aligned with the user's request. | Includes a measurable success condition and explicit boundaries. |
| **Scope definition** | | Scope is missing or includes unrequested changes. | Scope is bounded with clear inclusions and exclusions. | Also lists affected components and files outside of scope. |
| **Acceptance criteria (EARS)** | ✅ | Criteria are missing, not EARS, or compound. | All criteria follow EARS and are atomic. | Criteria are atomic, prioritized, and traceable to tests/validations. |
| **Constraints and assumptions** | | No constraints or assumptions are mentioned. | Relevant constraints and assumptions are documented. | Assumptions are validated as reasonable and verification steps are proposed. |
| **Unknowns** | | No unknowns are identified. | Known unknowns are listed. | A plan to resolve or mitigate them is defined. |

### 2. `CONTEXT_ARTIFACT_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Relevance** | ✅ | Context is irrelevant or generic for the task. | Technical context is relevant to the objective. | Context is deepened into the exact components to be modified. |
| **Completeness** | | Missing key components, dependencies, or current behavior. | Covers components, dependencies, behavior, and constraints. | Includes diagrams, code examples, or exact references. |
| **Consistency** | | Contradictions between sections or with the task specification. | No internal contradictions or contradictions with the task specification. | Reinforces coherence with previous artifacts and project state. |
| **Evidence-based** | ✅ | Claims without evidence (made up). | Evidence is based on files, tests, or observed real behavior. | Verifiable evidence with paths, snippets, and execution results. |
| **Unknowns identified** | | No context gaps are identified. | Gaps are recognized and it is indicated whether they are blockers. | A plan is proposed to cover the gaps. |

### 3. `CONTEXT_VALIDATION_REPORT_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Coverage** | | Does not evaluate all aspects of the context. | Evaluates completeness, relevance, consistency, and risks. | Includes evaluation of dependencies and evidence quality. |
| **Decision clarity** | ✅ | Validation decision is missing or ambiguous. | Clear decision: `VALIDATED`, `NEEDS_MORE_CONTEXT`, or `REJECTED`. | Includes justification and specific next steps. |
| **Required actions** | | Does not propose actions for problems. | Lists concrete actions if context is insufficient. | Prioritized actions with suggested responsible party (worker/role). |
| **Confidence assessment** | | Does not express confidence level. | Includes justified confidence level. | Confidence linked to evidence and residual risks. |

### 4. `EXECUTION_PLAN_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Approach alignment** | ✅ | Plan does not address the objective or contradicts the scope. | Plan aligned with objective, scope, and constraints. | Plan optimized with alternatives considered and discarded documented. |
| **Step clarity** | | Steps are ambiguous, disordered, or impossible to follow. | Steps are numbered, concrete, and ordered. | Steps with entry/exit criteria and explicit dependencies. |
| **Risk coverage** | | Does not identify risks. | Identifies risks and mitigations. | Includes technical, scope, and quality risks with contingency plans. |
| **Validation strategy** | ✅ | Does not say how to validate. | Defines how to validate each change or criterion. | Includes specific tests, commands, and verifiable acceptance criteria. |
| **Rollback considerations** | | Does not consider reverting changes. | Describes how to revert in case of failure. | Automated rollback or exact instructions per step. |

### 5. `EXECUTION_SUMMARY_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Change documentation** | | Does not list modified files or changes made. | Lists modified files and main changes. | Includes conceptual diff, motivation for each change, and impact. |
| **Plan adherence** | ✅ | Changes do not match the plan. | Executed changes match the execution plan. | Deviations documented and justified. |
| **Validation evidence** | | Does not show validation evidence. | Includes test/validation results. | Evidence traceable to acceptance criteria. |
| **Issue transparency** | | Hides problems or errors found. | Documents issues, workarounds, and limitations. | Classifies issues by severity and proposes follow-up. |

### 6. `VERIFICATION_REPORT_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Criteria evaluation** | ✅ | Does not evaluate each acceptance criterion. | Each EARS criterion has explicit evaluation. | Evaluation with evidence and traceability to tests. |
| **Test evidence** | | Does not include test results. | Includes test and validation results. | Automated + manual tests, logs, screenshots, or metrics. |
| **Issue transparency** | | Does not document issues found. | Documents issues with severity and proposed action. | Issues linked to criteria and resolution plan. |
| **Scope compliance** | ✅ | Does not verify whether scope was respected. | Confirms scope was respected under Branch A (no out-of-scope changes, no authorized extra work claimed). | Verifies the two branches coherently and checks explicit written authorization with cited evidence for any extra work (Branch B). |
| **Final decision clarity** | ✅ | Final decision is missing or ambiguous. | Clear decision: `COMPLETED` or `RECOVERY`. | Decision with justification, residual risks, and next steps. |

## Critical criteria summary

| Rubric | Critical criteria |
|---|---|
| `TASK_SPECIFICATION_RUBRIC` | Objective clarity, Acceptance criteria (EARS) |
| `CONTEXT_ARTIFACT_RUBRIC` | Relevance, Evidence-based |
| `CONTEXT_VALIDATION_REPORT_RUBRIC` | Decision clarity |
| `EXECUTION_PLAN_RUBRIC` | Approach alignment, Validation strategy |
| `EXECUTION_SUMMARY_RUBRIC` | Plan adherence |
| `VERIFICATION_REPORT_RUBRIC` | Criteria evaluation, Scope compliance, Final decision clarity |

## `## Rubric Evaluation` section format

When rubrics are enabled, the `verifier` adds a `## Rubric Evaluation` section to `VERIFICATION_REPORT.md` with the following structure:

```markdown
## Rubric Evaluation

### TASK_SPECIFICATION_RUBRIC

- ✅ Objective clarity
  - Level: MEETS
  - Evidence: objective is specific and testable
- Acceptance criteria (EARS)
  - Level: EXCEEDS
  - Evidence: all criteria follow EARS and are atomic
```

Each criterion entry must include:
- The criterion name (with ✅ if critical).
- A `Level` line with value `INSUFFICIENT`, `MEETS`, or `EXCEEDS`.
- An `Evidence` line with a brief justification.


## Technical Practice Rubrics

When a technical-practice feature flag is enabled and selected in the task specification, the corresponding rubric is applied by the verifier during phase 07 and may be applied by the reviewer before critical transitions.

### 7. `TDD_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Failing test first** | ✅ | No evidence of a failing test before the production change. | Evidence shows a test was written or updated and failed before the fix. | Test clearly reproduces the bug or captures the new behavior before any production code. |
| **Production change minimal** | | Production change is unrelated to the test or excessive. | Production change is the minimum needed to pass the test. | Production change is minimal and includes a brief justification. |
| **Test result recorded** | ✅ | No final test result recorded. | Final test result is PASS or FAIL with evidence. | Final test result is PASS, with command/output evidence. |
| **Refactor step documented** | | Refactor step missing or unclear. | Refactor step is mentioned if performed. | Refactor improved design while keeping tests green, with specific changes noted. |

### 8. `SRP_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Responsibility identified** | ✅ | No responsibility is identified before extraction. | The responsibility that justified extraction is documented. | Multiple responsibilities are identified with concrete code references. |
| **Extraction documented** | | No extraction or split documented. | Extraction is documented with `from` and `to` locations. | Extraction includes reasoning and verifies the original module remains focused. |
| **Scope respected** | ✅ | Extraction introduces changes outside the task scope. | Extraction stays within the task scope. | Extraction stays within scope and does not break existing callers. |

### 9. `OCP_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Extension point defined** | ✅ | No extension point or abstraction is introduced. | An extension point (interface, strategy, hook) is documented. | Extension point is designed for future variants with minimal friction. |
| **Base code preserved** | | Existing code was modified unnecessarily. | Stable code is left unchanged; new behavior is added via extension. | Existing tests remain green without modification. |
| **Justified abstraction** | | Abstraction added without justification. | Abstraction is justified by the change. | Alternatives considered and trade-offs documented. |

### 10. `LSP_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Substitutability verified** | ✅ | No evidence that subclasses respect the base contract. | Substitution tests or reasoning are documented. | Automated substitution tests pass for all subclasses. |
| **Contract preserved** | | Subclass weakens postconditions or strengthens preconditions. | Preconditions, postconditions, and invariants are preserved. | Contract is explicitly documented and verified. |
| **Hierarchy justified** | | Inheritance used where composition is better. | Inheritance is appropriate for the relationship. | Both inheritance and composition were considered; choice is justified. |

### 11. `ISP_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Client needs analyzed** | ✅ | No analysis of which methods each client uses. | Clients and the methods they use are identified. | Analysis includes code references for each client. |
| **Interfaces split** | | Large interface remains unchanged. | Interface is split into smaller role-specific interfaces. | Split reduces unused method exposure for all clients. |
| **Clients updated correctly** | | Clients depend on the wrong interface or break. | Clients depend only on the interfaces they need. | All clients verified to use only their required interface methods. |

### 12. `DIP_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Abstraction introduced** | ✅ | High-level module still depends directly on low-level details. | An abstraction is introduced and the high-level module depends on it. | Abstraction is stable, well-named, and reusable. |
| **Dependency injected** | | Dependency is still hard-coded. | Dependency is injected via constructor, parameter, or setter. | Injection mechanism is consistent with project conventions. |
| **Justified inversion** | | Inversion added where the detail is stable and unlikely to change. | Inversion is justified by volatility or testability needs. | Tests can now use stubs/mocks thanks to the abstraction. |

### 13. `SCREAMING_ARCHITECTURE_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Domain-first structure** | ✅ | Project layout is organized by technical layer only. | Top-level directories are named after domains or use cases. | Every module's responsibility is clear from its path; no generic `utils/` dumping ground. |
| **Framework isolation** | | Framework or database details are mixed with business modules. | Framework and infrastructure code live in identifiable edge modules. | A reader can locate business rules without encountering framework imports. |
| **Evidence documented** | | No structural rationale or module list provided. | Evidence lists domain modules and their responsibilities. | Evidence includes before/after comparison and explains exceptions. |

### 14. `CLEAN_ARCHITECTURE_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Dependency rule respected** | ✅ | Inner layers import outer layers. | Inner layers depend only on inner layers or abstractions defined internally. | A dependency graph or import check confirms no inward-to-outward dependency. |
| **Use-case clarity** | | Use cases are missing or mixed with framework code. | Each use case has a single responsibility and is independent of delivery mechanism. | Use cases are named after user goals and documented with input/output boundaries. |
| **Abstractions for volatile details** | | Business logic depends directly on database, HTTP, or external APIs. | Ports/adapters separate volatile details from business rules. | Multiple adapters exist or could be added without changing core logic. |
| **Evidence documented** | | No layer list or rationale provided. | Evidence lists layers touched and any dependency-rule violations fixed. | Evidence includes a concrete example of an inverted dependency. |

### 15. `DRY_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Duplication identified** | ✅ | No duplication is reported even when obvious copies exist. | Duplicated knowledge is listed with locations and the rule it represents. | Every duplication found names the single piece of knowledge it duplicates. |
| **Consolidation appropriate** | | Abstraction is forced on coincidental similarity. | Duplicated knowledge is consolidated behind a named abstraction or source of truth. | Consolidation reduces maintenance cost without creating inappropriate coupling. |
| **Intentional duplication documented** | | Duplication is kept without explanation. | Any duplication kept by design is justified in the evidence. | Trade-off between abstraction and separation is explained. |
| **Evidence documented** | | No consolidation strategy or impact recorded. | Evidence includes strategy and at least one resolved duplication. | Evidence estimates maintenance impact (e.g., lines saved, files simplified). |

### 16. `LAYERED_ARCHITECTURE_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Layers clearly defined** | ✅ | No layer structure is documented or layers are mixed arbitrarily. | Each module is assigned to a named layer with a clear responsibility. | Layer responsibilities are documented and consistent across the project. |
| **Downward dependencies only** | | Higher layers depend on lower layers in both directions or layers are circular. | Dependencies point downward only. | A tool or manual review confirms no upward or circular dependencies. |
| **Business logic placement** | | Business rules live in presentation or infrastructure. | Business rules live in domain/application layers. | Business rules are reusable across multiple delivery mechanisms. |
| **Evidence documented** | | No layer list or rationale provided. | Evidence lists layers affected and any violations fixed. | Evidence explains why Layered Architecture was chosen over alternatives. |

### 17. `GRASP_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Patterns named and justified** | ✅ | No GRASP pattern is mentioned or patterns are misapplied. | At least one pattern is named with a clear justification for the responsibility assignment. | Multiple patterns are applied and linked to concrete files and decisions. |
| **Coupling/cohesion addressed** | | Responsibilities are moved without explaining coupling or cohesion impact. | The evidence identifies coupling or cohesion issues and how they were resolved. | Before/after comparison shows measurable improvement in focus or dependency count. |
| **Appropriate pattern choice** | | A forced pattern is used where a simpler assignment would suffice. | The chosen pattern is the most appropriate among the GRASP options. | Alternatives were considered and the selected pattern is justified. |
| **Evidence documented** | | No concrete files or decisions are listed. | Evidence links patterns to files and responsibility changes. | Evidence includes a brief rationale for each pattern application. |

### 18. `DDD_TACTICAL_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Tactical patterns identified** | ✅ | No entities, value objects, aggregates, or services are identified. | At least one tactical pattern is applied and named with its location. | Multiple patterns (aggregate, value object, repository, domain event, service) are applied cohesively. |
| **Invariants enforced** | | Business rules remain scattered or implicit. | Aggregate roots protect stated invariants. | Invariants are explicit, testable, and documented. |
| **Domain isolation** | | Domain models depend on frameworks, ORM, or HTTP. | Domain layer has no infrastructure dependencies. | Domain layer can be unit-tested without database or framework setup. |
| **Evidence documented** | | No patterns, invariants, or refactored files listed. | Evidence includes patterns applied and invariants enforced. | Evidence shows before/after of anemic models becoming rich domain models. |

### 19. `DDD_STRATEGIC_RUBRIC`

| Criterion | Critical | INSUFFICIENT | MEETS | EXCEEDS |
|---|---|---|---|---|
| **Bounded contexts identified** | ✅ | No bounded contexts are named or boundaries are vague. | Bounded contexts align with business subdomains or team boundaries. | Each context has explicit responsibilities and a defined ubiquitous language. |
| **Context map documented** | | Integration between contexts is undocumented. | Relationships between contexts use recognized patterns (ACL, customer-supplier, etc.). | Context map includes direction of dependency and rationale for each pattern. |
| **Model separation respected** | | Entities or value objects are shared across contexts. | Each context owns its model; translations happen at boundaries. | Anti-corruption layers or adapters isolate external/legacy models. |
| **Evidence documented** | | No contexts, terms, or integration patterns listed. | Evidence documents contexts, patterns, and any ACLs added. | Evidence includes ubiquitous language terms per context and integration examples. |
