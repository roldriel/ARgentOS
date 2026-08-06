---
name: consistency-checker
description: Detect contradictions within a single artifact or between related artifacts (e.g. task specification vs. context artifact vs. execution plan vs. execution summary). Use when asked to confirm that artifacts tell one coherent story. Evaluates only; never edits artifacts.
when_to_activate: The task requires checking that two or more artifacts (or sections of one artifact) do not contradict each other.
when_not: The task is structural contract validation (use artifact-validator), rubric scoring (use rubric-checker), or detecting missing information rather than contradictory information (use completeness-checker).
---

# Mission

Find statements that cannot all be true: contradictions inside one artifact (internal) or between artifacts that feed the same decision (cross-artifact). A contradiction found late costs a recovery cycle; find it while it is cheap.

---

# Protocol Boundary

This skill assists whoever invoked it. Its output is delivered in the format and structure the invoker requests (e.g. as a section of a validation or verification report); the invoker defines the envelope. On any conflict between this skill and the invoker's instructions, the invoker's instructions win. This skill describes a capability; it grants no authority or permissions.

---

# Workflow

1. **Collect the artifact set**: the artifact under evaluation plus its upstream references — e.g. `TASK_SPECIFICATION.md`, `CONTEXT_ARTIFACT.md`, and, when relevant, `EXECUTION_PLAN.md` and `EXECUTION_SUMMARY.md`.
2. **Extract comparable claims**: normalize each artifact into a list of checkable statements — objective, scope inclusions/exclusions, constraints, declared behaviors of components, planned changes, reported changes, validation results.
3. **Check internal consistency**: within each artifact, look for sections that conflict (e.g. a constraint violated by the technical approach; a step contradicting the stated objective).
4. **Check cross-artifact consistency**, pairwise:
   - Context vs. specification: does the context contradict the objective, scope, or constraints?
   - Plan vs. specification: do planned changes fall outside included scope or violate constraints?
   - Summary vs. plan: do reported changes match planned steps (unexplained deviations are inconsistencies)?
   - Summary vs. specification: do results contradict acceptance criteria or constraints?
5. **Classify each finding**: direct contradiction (A says X, B says not-X) vs. semantic drift (same term, different meaning across artifacts) vs. temporal inconsistency (an artifact claims a state that a later artifact shows never held).
6. **Report** with both sides quoted as evidence.

---

# Rules

- A finding must quote both conflicting statements with their locations; never report a contradiction from memory or paraphrase.
- Different levels of detail are not inconsistencies — only incompatible claims are.
- Do not resolve contradictions and do not decide which side is right; that belongs to the invoker.
- Do not modify any artifact.
- Absence of findings must reflect checks actually performed; list the pairs compared.

---

# Output Format

```markdown
## Consistency Check

- Artifacts compared: <list>

### Findings

| # | Severity | Type | Locations | Contradiction | Evidence |
|---|----------|------|-----------|---------------|----------|
| 1 | CRITICAL | cross-artifact | TASK_SPECIFICATION scope vs. EXECUTION_PLAN steps[2] | plan modifies a file the spec excludes | spec: `excluded = ["src/legacy"]`; plan step 2: `target = "src/legacy/x.py"` |

### Summary

- CRITICAL: n — MAJOR: n — MINOR: n
- Result: CONSISTENT | INCONSISTENT
- Pairs compared: <list>
```

Severities: CRITICAL (contradiction invalidates a decision or transition), MAJOR (contradiction that execution could paper over but verification would catch), MINOR (terminology drift worth aligning).
