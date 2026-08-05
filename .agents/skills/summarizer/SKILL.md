---
name: summarizer
description: Condense extensive information into a short summary that preserves every decision-relevant point, with a declared compression ratio and no new content. Use when a worker must shrink large material for downstream consumption during context gathering (phase 03, core:GATHERING_CONTEXT).
when_to_activate: The delegated task requires condensing long documents, discussions, or collected context into a brief that preserves what decisions depend on, during phase 03.
when_not: The task needs citable individual facts (use extractor), quality evaluation, or the source is already short enough to include verbatim.
---

# Mission

Produce a summary that a decision-maker can act on without reading the original.

The objective is not maximum brevity.

The objective is lossless compression of *decision-relevant* content: conclusions, constraints, open questions, numbers, and commitments survive; redundancy, examples, and rhetoric do not.

Optimize for:

* preservation of decisional content
* faithfulness (nothing added, nothing softened)
* honest declaration of what was dropped

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`03-gather-context`). Its output is embedded as a section inside the phase artifact (`CONTEXT_ARTIFACT.md`): the phase contract defines the envelope, this skill defines the content of the summary section. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

* Never add information that is not in the source — no inference, no extrapolation, no "helpful" completion.
* Never drop a decision-relevant point to hit a length target; if it matters, it stays.
* Preserve open questions and disagreements as open; do not summarize them away into false consensus.
* Numbers, names, versions, and constraints are quoted exactly, never paraphrased loosely.

---

# Workflow

1. **Read fully first.** No summarizing while reading; understand the whole before cutting.
2. **Identify the decisional core.** Conclusions, constraints, decisions, open questions, action items, hard data.
3. **Draft the summary.** Lead with the core; keep original terminology for anything normative.
4. **Verify against the source.** Check each surviving claim resolves to the source; check nothing decisional was omitted.
5. **Declare omissions.** List categories of content deliberately dropped (examples, background, repetition).
6. **Produce output** in the format below.

---

# Output Format

Embedded as a section inside `CONTEXT_ARTIFACT.md`:

```markdown
## Summary: <source title>

Source: <path / URL> | Original size: ~<n words/pages> | Compression: ~<x>%

<summary body, typically 3–10 sentences or a short bullet list>

### Preserved Open Questions
- <unresolved point from the source>

### Deliberately Omitted
- <categories dropped, e.g. examples, historical background>
```
