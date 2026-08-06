---
name: context-validator
description: Assist the validation of a gathered Project Context (CONTEXT_ARTIFACT.md) by evaluating completeness, relevance, consistency, and risk, and drafting the inputs for a CONTEXT_VALIDATION_REPORT.md decision. Use when asked to evaluate whether a gathered context artifact is sufficient to proceed. Assists only; the invoker and the applicable contract govern, and the skill never writes the report itself.
when_to_activate: The task is to evaluate whether a gathered context artifact is complete, relevant, consistent, and low-risk enough to support the next step, and to recommend a validation decision.
when_not: The task is to gather context itself, to verify claims against repository evidence as an audit (use hallucination-checker), or no context artifact exists to validate.
---

# Mission

Evaluate a context artifact (e.g. `CONTEXT_ARTIFACT.md`) against the task specification and produce the evaluation material for a validation report (e.g. `CONTEXT_VALIDATION_REPORT.md`, contract: `.agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md`). The report contains no new context — it only evaluates the existing context artifact. The invoker owns the report; this skill supplies the evaluations and a recommended decision.

---

# Protocol Boundary

This skill describes a capability; it grants no authority or permissions. It assists whoever invokes it; the invoker and any instructions they provide govern, and on any conflict the invoker's instructions win. Its output is delivered in whatever format or structure the invoker requests.

---

# Workflow

1. **Read the inputs**: the task specification (e.g. `TASK_SPECIFICATION.md`) and the context artifact (e.g. `CONTEXT_ARTIFACT.md`) to be evaluated.
2. **Completeness**: does the context cover the information the task specification requires? List each missing item. Verdict: COMPLETE or INCOMPLETE.
3. **Relevance**: is every piece of collected information related to the task? List irrelevant items. Verdict: VALID or INVALID.
4. **Consistency**: does the context contradict itself (or the specification)? List each conflict with both sides quoted. Verdict: CONSISTENT or CONFLICTING.
5. **Risk**: identify risks caused by insufficient or uncertain context, each with severity LOW / MEDIUM / HIGH.
6. **Recommend a decision** with reasoning, per the contract's vocabulary:
   - VALIDATED — context suffices.
   - NEEDS_MORE_CONTEXT — specific gaps exist; list the required actions (gather files, resolve conflicts).
   - REJECTED — context is unusable or contradictory beyond repair.
   - If the gap is missing or ambiguous *information only the user can provide*, recommend clarification instead, per the contract.
7. **State confidence** (LOW / MEDIUM / HIGH) with a short explanation of what limits it.

---

# Rules

- Evaluate only the existing context artifact; never add new context, never edit the context artifact or write the validation report — hand the evaluation to the invoker.
- Every evaluation item must point to concrete evidence: the missing requirement, the irrelevant entry, the conflicting pair.
- Use only the verdict and decision vocabularies defined in the contract; do not invent new states or transitions.
- Do not lower the bar because the task looks small — reducing validation rigor for convenience is circumvention (`.agents/standards/conduct/ANTI_CIRCUMVENTION.md`).
- An honest INCOMPLETE or CONFLICTING verdict is a good outcome; forcing VALIDATED to unblock planning is a protocol violation.

---

# Output Format

```markdown
## Context Validation Assistance

- Context artifact: <path>
- Objective: <what was evaluated>

### Evaluations

- Completeness: <COMPLETE|INCOMPLETE> — missing: [...]
- Relevance: <VALID|INVALID> — irrelevant: [...]
- Consistency: <CONSISTENT|CONFLICTING> — conflicts: [...]

### Risks

| Description | Severity |
|-------------|----------|
| <risk> | LOW/MEDIUM/HIGH |

### Recommended Decision

- Result: <VALIDATED|NEEDS_MORE_CONTEXT|REJECTED>
- Reasoning: <...>
- Required actions: [...]
- Confidence: <LOW|MEDIUM|HIGH> — <explanation>
```

The invoker maps these values into the validation report fields defined by the applicable contract.
