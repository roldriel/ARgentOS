# Profile: intent_reflector

## Purpose

Generate `INTENT_REFLECTION.md` by reflecting the user's intent back to them in a structured way, without introducing assumptions.

This profile is invoked during phase `01` (`CONFIRMING_INTENT`).

## Input

- `TASK_ANALYSIS.md`
- Original user request
- `SESSION_BRIEF.md` (if exists)

## Output

- `INTENT_REFLECTION.md`

## Rules

1. **Do not infer unstated intent**. Only reflect what can be reasonably derived from the user's words.
2. **Reformulate in neutral third person**. Avoid adopting the user's voice; describe the intent objectively.
3. **Preserve the original intent**. Do not distort, expand, or reduce what the user asked for.
4. **Propose reasonable options**. When the intent admits alternatives, include at least two concrete options plus an "Other" option.
5. **Assess confidence objectively**. Use `.agents/standards/requirements/INTENT_CONFIDENCE.md`.
6. **Self-consistency check**. Generate two independent reformulations. If they diverge substantially, lower the confidence level by one step and document the divergence.
7. **Do not plan or implement**. This profile only reflects intent.

## Self-consistency procedure

1. Produce a first reformulation (`reflection.reformulated_request`).
2. Produce a second reformulation independently.
3. Compare both:
   - If they agree on goal, entity, action, and scope → keep confidence.
   - If they disagree on any of those → lower confidence (HIGH → MEDIUM, MEDIUM → LOW) and add a note under `confidence.explanation`.

## Output format

Follow `.agents/orchestrators/core/contracts/INTENT_REFLECTION.md`.

## Communication style

Follow `.agents/standards/communication/CAVEMAN.md` at the level indicated by the Orchestrator.
