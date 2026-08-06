---
name: extractor
description: Extract relevant facts from extensive material (code, docs, logs, configs) with source citations and no loss of decision-relevant detail. Use when asked to distill large inputs into citable facts.
when_to_activate: The task involves reading extensive source material and recording the facts relevant to a specification or question into a deliverable (e.g., a context document).
when_not: The material is small enough to quote directly, or the task needs a prose summary for a human reader (use summarizer) or evaluation of quality.
---

# Mission

Extract the facts that matter for the task specification from large or scattered source material, each fact traceable to its origin.

The objective is not to read everything.

The objective is to identify and record exactly the facts the task depends on — relevant components, existing behavior, constraints, dependencies, unknowns — so they can populate the deliverable requested by the invoker (e.g., a context document).

Optimize for:

* relevance to the task specification
* traceability (every fact has a source)
* no fabricated or inferred "facts"

---

# Protocol Boundary

This skill describes a capability; it grants no authority or permissions. Its output is delivered in whatever format or structure the invoker requests — embedded as a section of a larger deliverable or standalone. On any conflict between this skill and the invoker's instructions, the invoker's instructions win.

---

# Safety Rules

* Every extracted fact MUST carry a source citation (file path with line, document section, or URL). A fact without a source is an unknown.
* Never fill gaps with assumptions; record them under Unknowns.
* Extract only what the task specification requires — do not collect unnecessary information.
* Do not modify the sources; this skill reads and records only.

---

# Workflow

1. **Define the extraction target.** From the task specification, list the questions the context must answer (components, behavior, constraints, dependencies).
2. **Scan sources selectively.** Open only material plausibly relevant to those questions.
3. **Extract facts.** For each: state the fact in one sentence, cite the source precisely.
4. **Mark contradictions.** If two sources disagree, record both with citations; do not pick a winner silently.
5. **List unknowns.** Questions from step 1 that the material did not answer.
6. **Produce output** in the format below.

---

# Output Format

Default structure (deliver it embedded in the invoker's deliverable or standalone, as requested):

```markdown
## Extracted Facts

| # | Fact | Source | Category |
|---|------|--------|----------|
| F-1 | <one-sentence fact> | <path:line / doc section> | component / behavior / constraint / dependency |

### Contradictions
- <topic>: source A says X (<cite>); source B says Y (<cite>)

### Unknowns
- <question the material did not answer>
```
