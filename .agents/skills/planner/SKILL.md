---
name: planner
description: Decompose a validated objective into an ordered sequence of concrete, verifiable steps with dependencies and verification criteria per step. Use when a worker must produce the execution plan during planning (phase 05, core:PLANNING).
when_to_activate: The delegated task requires building EXECUTION_PLAN.md from TASK_SPECIFICATION.md and the validated context during phase 05.
when_not: Specification or context is missing/invalid, or the task is to execute steps rather than plan them (that is phase 06).
---

# Mission

Turn "what must be achieved" into an ordered, verifiable sequence of steps.

The objective is not a wish list of activities.

The objective is a plan where each step is concrete enough to execute without further design decisions, verifiable enough to know when it is done, and ordered by real dependencies — the content of `EXECUTION_PLAN.md` (contract: `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`), produced by the planner role (`.agents/roles/planner.md`) during phase 05 (`.agents/orchestrators/core/workflow/05-plan.md`).

Optimize for:

* step granularity (executable, not aspirational)
* explicit dependency ordering
* per-step verification criteria
* coverage of every acceptance criterion

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`05-plan`). Its output is embedded as a section inside the phase artifact: the `EXECUTION_PLAN.md` contract defines the envelope, this skill defines the content of the step-decomposition section. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

* Never plan from assumptions: if context has a critical unknown, escalate to `NEEDS_CLARIFICATION` instead of planning around it (phase 05 forbids replacing missing context with assumptions).
* Never modify project files: the planner role produces a plan only; project changes belong to phase 06 (`executor`).
* Every step MUST be verifiable: a step without a checkable done-condition is not a step, split or rewrite it.
* Do not introduce work not implied by the specification's acceptance criteria.

---

# Workflow

1. **Anchor on acceptance criteria.** List every criterion from `TASK_SPECIFICATION.md`; the plan must cover all of them.
2. **Decompose.** Break the objective into steps small enough that each has one clear owner-action and one clear done-condition.
3. **Order by dependency.** A step that consumes another step's output comes after it; note the dependency explicitly.
4. **Attach verification.** For each step, state how the executor or verifier will confirm completion (test passes, file exists, command output, review check).
5. **Map coverage.** Cross-check that every acceptance criterion is satisfied by at least one step; flag any uncovered criterion.
6. **Identify risks.** Steps with uncertainty, external dependencies, or irreversibility get a note.
7. **Produce output** in the format below.

---

# Output Format

Embedded as a section inside `EXECUTION_PLAN.md`:

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
