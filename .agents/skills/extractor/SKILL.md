---
name: extractor
description: Extract relevant facts from extensive material (code, docs, logs, configs) with source citations and no loss of decision-relevant detail. Use when a worker must distill large inputs into citable facts during context gathering (phase 03, core:GATHERING_CONTEXT).
when_to_activate: The delegated task involves reading extensive source material and recording the facts relevant to the task specification into CONTEXT_ARTIFACT.md during phase 03.
when_not: The material is small enough to quote directly, or the task needs a prose summary for a human reader (use summarizer) or evaluation of quality.
---

# Mission

Extract the facts that matter for the task specification from large or scattered source material, each fact traceable to its origin.

The objective is not to read everything.

The objective is to identify and record exactly the facts the task depends on — relevant components, existing behavior, constraints, dependencies, unknowns — so they can populate `CONTEXT_ARTIFACT.md` (phase 03, `.agents/orchestrators/core/workflow/03-gather-context.md`).

Optimize for:

* relevance to the task specification
* traceability (every fact has a source)
* no fabricated or inferred "facts"

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`03-gather-context`). Its output is embedded as a section inside the phase artifact: the phase contract defines the envelope of `CONTEXT_ARTIFACT.md`, this skill defines the content of the extracted-facts section. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

* Every extracted fact MUST carry a source citation (file path with line, document section, or URL). A fact without a source is an unknown.
* Never fill gaps with assumptions; record them under Unknowns.
* Extract only what the task specification requires — phase 03 explicitly says: do not collect unnecessary information.
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

Embedded as a section inside `CONTEXT_ARTIFACT.md`:

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
