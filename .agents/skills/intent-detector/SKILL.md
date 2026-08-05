---
name: intent-detector
description: Assess the agent's confidence in its interpretation of the user's intent using the objective scoring model in .agents/standards/requirements/INTENT_CONFIDENCE.md. Use when a worker must decide whether a request can proceed to specification or requires intent confirmation. Analyzes only; never writes artifacts and never resolves ambiguity by assumption.
when_to_activate: The delegated phase is 00-analyze-task (state core:ANALYZING_TASK) and the TASK_ANALYSIS.md artifact must record an intent_confidence assessment, or any phase that must re-evaluate confidence in the interpreted intent.
when_not: The task is to extract requirements, goals, or constraints from the request (use requirement-extractor or goal-extractor), to confirm intent with the user (that is phase 01-confirm-intent), or a valid TASK_ANALYSIS.md with intent_confidence already exists.
---

# Mission

Produce an auditable intent-confidence assessment: a numeric score, the criteria applied, and the resulting level (HIGH / MEDIUM / LOW), following exactly the model defined in `.agents/standards/requirements/INTENT_CONFIDENCE.md`.

This skill supplies the content of the `intent_confidence` section of `TASK_ANALYSIS.md` (contract: `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`). It does not decide the next state; it provides the objective input the `task_analyst` profile uses to recommend one.

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`00-analyze-task`). Its output is embedded as a section inside the phase artifact; the phase contract (`TASK_ANALYSIS.md`) defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

- Apply only the criteria in `.agents/standards/requirements/INTENT_CONFIDENCE.md`; never invent new criteria or adjust weights.
- A criterion applies or it does not — no partial credit, no rounding.
- Never inflate the level to avoid `CONFIRMING_INTENT`; the anti-inflation rule of `.agents/standards/quality/CONFIDENCE.md` applies.
- Never resolve vague terms or contradictions by assumption (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`); score them as negative criteria.
- Do not modify any artifact; hand the assessment to the delegating worker.

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

The delegating worker embeds this into the `[intent_confidence]` section of `TASK_ANALYSIS.md` and uses the level to recommend the next state (`BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION` when unresolved ambiguities block progression regardless of score).
