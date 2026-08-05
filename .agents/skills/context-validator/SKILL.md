---
name: context-validator
description: Assist the validation of the gathered Project Context (CONTEXT_ARTIFACT.md) by evaluating completeness, relevance, consistency, and risk, and drafting the inputs for the CONTEXT_VALIDATION_REPORT.md decision. Use when a worker executes phase 04-validate-context. Assists only; the phase and its contract govern, and the skill never writes the report itself.
when_to_activate: The delegated phase is 04-validate-context (state VALIDATING_CONTEXT) and the worker must evaluate whether the gathered context is sufficient to proceed to planning.
when_not: The task is to gather context (phase 03), to verify claims against repository evidence as an audit (use hallucination-checker), or no CONTEXT_ARTIFACT.md exists to validate.
---

# Mission

Evaluate the `CONTEXT_ARTIFACT.md` of the current iteration against the task specification and produce the evaluation material for `CONTEXT_VALIDATION_REPORT.md` (contract: `.agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md`). The report contains no new context — it only evaluates the existing context artifact. The delegating Worker owns the report; this skill supplies the evaluations and a recommended decision.

---

# Protocol Boundary

This skill assists the Worker inside phase 04-validate-context; the phase and its contract continue to govern — this skill only assists the Worker. Its output is embedded as a section inside the artifact that governs that phase; the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Workflow

1. **Read the inputs**: `TASK_SPECIFICATION.md` and `CONTEXT_ARTIFACT.md` of the current iteration (phase inputs per `.agents/orchestrators/core/workflow/04-validate-context.md`).
2. **Completeness**: does the context cover the information the task specification requires? List each missing item. Verdict: COMPLETE or INCOMPLETE.
3. **Relevance**: is every piece of collected information related to the task? List irrelevant items. Verdict: VALID or INVALID.
4. **Consistency**: does the context contradict itself (or the specification)? List each conflict with both sides quoted. Verdict: CONSISTENT or CONFLICTING.
5. **Risk**: identify risks caused by insufficient or uncertain context, each with severity LOW / MEDIUM / HIGH.
6. **Recommend a decision** with reasoning, per the contract's vocabulary:
   - VALIDATED — context suffices; transition VALIDATING_CONTEXT → CONTEXT_READY.
   - NEEDS_MORE_CONTEXT — specific gaps exist; list the required actions (gather files, resolve conflicts).
   - REJECTED — context is unusable or contradictory beyond repair.
   - If the gap is missing or ambiguous *information only the user can provide*, the transition target is NEEDS_CLARIFICATION, per the contract.
7. **State confidence** (LOW / MEDIUM / HIGH) with a short explanation of what limits it.

---

# Rules

- Evaluate only the existing context artifact; never add new context, never edit `CONTEXT_ARTIFACT.md` or write `CONTEXT_VALIDATION_REPORT.md` — hand the evaluation to the delegating Worker.
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
- Transition: VALIDATING_CONTEXT → <CONTEXT_READY|NEEDS_CLARIFICATION>
- Confidence: <LOW|MEDIUM|HIGH> — <explanation>
```

The delegating Worker maps these values into the `CONTEXT_VALIDATION_REPORT.md` fields defined by the contract.
