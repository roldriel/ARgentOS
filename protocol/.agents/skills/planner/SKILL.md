---
name: planner
description: Decompose a validated objective into an ordered sequence of concrete, verifiable steps with dependencies and verification criteria per step. Use when asked to produce an execution plan from a specification and its supporting context.
when_to_activate: The task requires building an execution plan (e.g., EXECUTION_PLAN.md) from a specification and validated context.
when_not: Specification or context is missing/invalid, or the task is to execute steps rather than plan them.
---

# Mission

Turn "what must be achieved" into an ordered, verifiable sequence of steps.

The objective is not a wish list of activities.

The objective is a plan where each step is concrete enough to execute without further design decisions, verifiable enough to know when it is done, and ordered by real dependencies — the content of an execution plan deliverable (e.g., `EXECUTION_PLAN.md`; contract reference: `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`).

Optimize for:

* step granularity (executable, not aspirational)
* explicit dependency ordering
* per-step verification criteria
* coverage of every acceptance criterion

---

# Protocol Boundary

This skill describes a capability: it decomposes an objective into verifiable steps and delivers that output in the format and structure the invoker requests, typically embedded as a section inside a larger plan document. On any conflict between this skill and the invoker's instructions, the invoker's instructions win. It grants no authority or permissions.

---

# Safety Rules

* Never plan from assumptions: if context has a critical unknown, escalate to `NEEDS_CLARIFICATION` instead of planning around it.
* Never modify project files: this skill produces a plan only; applying the plan's changes is a separate task.
* Every step MUST be verifiable: a step without a checkable done-condition is not a step, split or rewrite it.
* Do not introduce work not implied by the specification's acceptance criteria.

---

# Workflow

1. **Anchor on acceptance criteria.** List every criterion from the specification (e.g., `TASK_SPECIFICATION.md`); the plan must cover all of them.
2. **Decompose.** Break the objective into steps small enough that each has one clear owner-action and one clear done-condition.
3. **Order by dependency.** A step that consumes another step's output comes after it; note the dependency explicitly.
4. **Attach verification.** For each step, state how whoever executes or checks the step will confirm completion (test passes, file exists, command output, review check).
5. **Map coverage.** Cross-check that every acceptance criterion is satisfied by at least one step; flag any uncovered criterion.
6. **Identify risks.** Steps with uncertainty, external dependencies, or irreversibility get a note.
7. **Produce output** in the format below.

---

# Output Format

Embedded as a section inside the requested deliverable (e.g., `EXECUTION_PLAN.md`):

```markdown
## Step Decomposition

| Step | Action | Depends on | Verification |
|------|--------|-----------|--------------|
| 1 | <concrete action> | — | <done-condition> |
| 2 | <concrete action> | 1 | <done-condition> |

### Acceptance Coverage
- <criterion> → steps <n, m>

### Risks
- <step n>: <risk and mitigation>
```
