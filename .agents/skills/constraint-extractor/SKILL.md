---
name: constraint-extractor
description: Detect technical, scope, and business constraints that bound how a task may be executed — stated restrictions plus constraints implied by the request context. Use when asked to inventory the restrictions of a task or to audit what limits a plan must respect. Analyzes only; never writes artifacts and never relaxes a constraint by assumption.
when_to_activate: The task asks to identify explicit restrictions of a request or change, or to re-check which constraints a plan or change must respect.
when_not: The task is to extract functional requirements (use requirement-extractor), to identify goals (use goal-extractor), to score intent confidence (use intent-detector), or to evaluate risks of a proposal (use risk-detector).
---

# Mission

Build an evidence-backed inventory of every constraint that bounds the task: what must not change, which technology or pattern is mandated, what scope limit applies, and which business rule restricts the solution. The output is a constraint inventory delivered in the format the invoker requests (e.g., the restrictions section of a task analysis document).

A constraint missed in analysis becomes a violation discovered in verification. Prefer over-reporting with evidence over silent omission.

---

# Protocol Boundary

This skill describes a capability: it is asked to do a job, does it, and delivers the result. It yields to any instruction from the invoker, grants no authority or permissions, and delivers its output in whatever format or structure the invoker requests.

---

# Safety Rules

- Every constraint carries a verbatim quote or a named source (artifact, file, convention); no unsourced constraints.
- Separate stated constraints from derived ones; never present a derivation as something the user said.
- Never relax, reinterpret, or drop a constraint to make the task easier (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`); conflicting constraints are reported as conflicts, not resolved.
- Do not propose how to satisfy the constraints; that belongs to planning.
- Do not modify any artifact; hand the inventory to the invoker.

---

# Workflow

1. **Copy the original request verbatim**; read prior session artifacts (`SESSION_BRIEF.md`, confirmed clarifications) when available.
2. **Extract technical constraints**: mandated or forbidden technologies, libraries, patterns, compatibility or performance bounds ("use Flask", "do not touch X", "keep it under N").
3. **Extract scope constraints**: boundaries on what may change — files, modules, behaviors declared out of scope, "keep existing behavior intact".
4. **Extract business constraints**: domain rules, deadlines, process requirements (e.g. TDD, review policy) that restrict the solution space.
5. **Derive implicit constraints** only when the request cannot be honored without them; mark each as derived with its evidence.
6. **Detect conflicts**: pairs of constraints that cannot both hold; report both sides with evidence.
7. **Produce output** in the format below.

---

# Output Format

```markdown
## Constraint Extraction

### Technical Constraints
- TC-1: <constraint> — source: stated | derived — evidence: "<verbatim quote or reference>"

### Scope Constraints
- SC-1: <constraint> — source: stated | derived — evidence: "<...>"

### Business Constraints
- BC-1: <constraint> — source: stated | derived — evidence: "<...>"

### Conflicting Constraints
- CC-1: <constraint A> vs <constraint B> — evidence for both — requires user resolution
```

Empty sections are omitted. When the deliverable is a task analysis document, stated constraints typically map to its restrictions array and conflicts are surfaced as open questions with at least two resolution options each.
