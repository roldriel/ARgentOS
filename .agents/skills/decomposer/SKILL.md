---
name: decomposer
description: Break a complex problem into independent, self-contained subproblems that can be analyzed or solved separately. Use when a worker faces a problem too large or tangled to address as a single unit, typically during planning (phase 05, core:PLANNING) supporting the planner role.
when_to_activate: The delegated task requires splitting a complex objective or problem into independent subproblems during phase 05, supporting the planner role (.agents/roles/planner.md).
when_not: The task is to order the steps of an already-defined solution (use planner: decomposer divides the PROBLEM, planner orders the PASOS of the solution), or the problem is already small enough to plan directly.
---

# Mission

Make a hard problem tractable by dividing it into subproblems that can be understood, estimated, and solved independently.

The objective is not a list of activities.

The objective is a partition of the problem space where each subproblem is self-contained (solvable without waiting on the others), independently verifiable, and small enough to reason about without further decomposition — or explicitly flagged as needing another round.

Optimize for:

* independence (minimal coupling between subproblems)
* completeness (the union of subproblems covers the whole problem)
* clear interfaces where subproblems do touch

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (commonly `05-plan`, `.agents/orchestrators/core/workflow/05-plan.md`). Its output is embedded as a section inside the phase artifact (e.g. `EXECUTION_PLAN.md`, contract `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`); the phase contract defines the envelope, this skill defines the decomposition content. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

* Never decompose around an unknown: if part of the problem depends on an unstated decision, flag it for clarification instead of guessing (`.agents/standards/requirements/NO_ASSUMPTIONS.md`).
* Independence over convenience: if two candidate subproblems share state or order, either merge them or declare the interface between them explicitly.
* Do not sequence the subproblems into steps: ordering, dependencies, and verification criteria per step belong to the planner skill; this skill only partitions the problem.
* Do not modify project files or write artifacts directly; hand the decomposition to the delegating worker.

---

# Workflow

1. **State the whole problem** in one sentence, from the specification or task at hand. If it cannot be stated, it is not ready to decompose.
2. **Identify natural seams**: subsystems, data boundaries, user-visible behaviors, or risk clusters along which the problem can be split.
3. **Split along the seams** into subproblems. Each must be statable as a self-contained question with its own done-condition.
4. **Test independence**: for each pair, ask whether solving one requires the other's result. Where it does, declare the shared interface or merge them.
5. **Test completeness**: map every requirement of the original problem to at least one subproblem; flag anything uncovered.
6. **Right-size**: subproblems still too tangled get a `needs further decomposition` note instead of being force-planned.
7. **Produce output** in the format below.

---

# Output Format

Embedded as a section inside the phase artifact:

```markdown
## Problem Decomposition

- Problem: <one-sentence statement>

### Subproblems

| # | Subproblem | Done-condition | Coupling |
|---|-----------|----------------|----------|
| 1 | <self-contained question> | <checkable condition> | none / shares <interface> with #n |

### Coverage Check
- <original requirement> → subproblem(s) <n>

### Open Points
- <subproblem needing further decomposition or user clarification>
```

The "Open Points" section is omitted when empty.
