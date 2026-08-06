---
name: intent-detector
description: Assess the confidence in an interpretation of a user's intent using the objective scoring model in .agents/standards/requirements/INTENT_CONFIDENCE.md. Use when asked to decide whether a request is clear enough to proceed or requires intent confirmation. Analyzes only; never writes artifacts and never resolves ambiguity by assumption.
when_to_activate: The task is to score how confident the interpretation of a request is — e.g., to produce an intent_confidence assessment for a task analysis deliverable, or to re-evaluate confidence in the interpreted intent at any point.
when_not: The task is to extract requirements, goals, or constraints from the request (use requirement-extractor or goal-extractor), to confirm intent directly with the user, or a valid intent_confidence assessment already exists.
---

# Mission

Produce an auditable intent-confidence assessment: a numeric score, the criteria applied, and the resulting level (HIGH / MEDIUM / LOW), following exactly the model defined in `.agents/standards/requirements/INTENT_CONFIDENCE.md`.

This skill supplies the content of an `intent_confidence` section for the deliverable requested by the invoker (e.g., a task analysis document). It does not decide what happens next; it provides the objective input the invoker uses to recommend a course of action.

---

# Protocol Boundary

This skill describes a capability: it analyzes and delivers an assessment. Its output is embedded as a section inside whatever deliverable the invoker requests; the invoker defines the envelope. On any conflict between this skill and the invoker's instructions, the invoker's instructions win. This skill grants no authority or permissions.

---

# Safety Rules

- Apply only the criteria in `.agents/standards/requirements/INTENT_CONFIDENCE.md`; never invent new criteria or adjust weights.
- A criterion applies or it does not — no partial credit, no rounding.
- Never inflate the level to avoid `CONFIRMING_INTENT`; the anti-inflation rule of `.agents/standards/quality/CONFIDENCE.md` applies.
- Never resolve vague terms or contradictions by assumption (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`); score them as negative criteria.
- Do not modify any artifact; hand the assessment to the invoker.

---

# Workflow

1. **Copy the original request verbatim** as the scoring basis.
2. **Apply positive criteria** (+2 each): concrete technology/framework/library/tool named; measurable action verb (create, edit, query, refactor, fix, add, remove); main entity or object of work defined; concrete success criterion or expected output stated.
3. **Apply negative criteria**: vague terms requiring substantial interpretation (-2); explicit contradictions between requirements (-3); missing subject, action, or main object (-2); multiple tasks without priority or relationship (-1).
4. **Compute the score** as the sum of applicable weights.
5. **Derive the level**: score >= 6 → HIGH; 2–5 → MEDIUM; < 2 → LOW.
6. **Record evidence**: list each applied criterion with the fragment of the request that triggered it.
7. **Produce output** in the format below.

---

# Output Format

```markdown
## Intent Confidence Assessment

- Score: <number>
- Level: HIGH | MEDIUM | LOW
- Applied positive criteria:
  - <criterion> (+2) — evidence: "<verbatim fragment>"
- Applied negative criteria:
  - <criterion> (-N) — evidence: "<verbatim fragment>"
- Explanation: <one or two sentences>
```

The invoker embeds this into the intent-confidence section of the requested deliverable (e.g., the `[intent_confidence]` section of a task analysis document) and uses the level to recommend the next step — proceed, confirm intent with the user, or request clarification when unresolved ambiguities block progression regardless of score.
