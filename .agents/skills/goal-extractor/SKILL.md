---
name: goal-extractor
description: Identify the explicit and implicit goals of a user request — what the user wants to achieve and what the successful outcome looks like from their perspective. Use when a worker must populate the objective and expected-outcome sections of TASK_ANALYSIS.md. Analyzes only; never writes artifacts and never infers goals without evidence.
when_to_activate: The delegated phase is 00-analyze-task (state core:ANALYZING_TASK) and the objective or expected outcome of the request must be articulated, or any phase that must restate the goal behind an artifact.
when_not: The task is to extract requirements, restrictions, or ambiguities (use requirement-extractor or constraint-extractor), to score intent confidence (use intent-detector), or the request is to plan, implement, or verify rather than to analyze the goal.
---

# Mission

State what the user wants to achieve, separating what they said from what follows from it. The output feeds the `[objective]` and `[expected_outcome]` sections of `TASK_ANALYSIS.md` (contract: `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`).

The objective is fidelity, not generosity: an implicit goal is only valid when the request cannot be satisfied without it, and it must be marked as implicit.

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`00-analyze-task`). Its output is embedded as a section inside the phase artifact; the phase contract (`TASK_ANALYSIS.md`) defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

- Never invent goals the user did not state or directly imply.
- Mark every implicit goal as implicit and attach the evidence that forces it.
- If two readings of the goal are plausible, report both as an ambiguity instead of choosing (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`).
- Do not decompose the goal into implementation steps; planning belongs to phase 05.
- Do not modify any artifact; hand the extraction to the delegating worker.

---

# Workflow

1. **Copy the original request verbatim** as the evidence base; read `SESSION_BRIEF.md` if it exists to reuse confirmed intent.
2. **Extract the explicit goal**: the single achievement the request asks for (fix, add, refactor, document, configure...).
3. **Extract the expected outcome**: what "done" looks like from the user's perspective, in their terms — not in implementation terms.
4. **Identify implicit goals**: achievements not stated but required for the explicit goal to hold (e.g. "keep existing tests green" behind "refactor X"). Each needs quoted evidence and a one-line justification.
5. **Flag goal-level ambiguities**: when the goal itself admits more than one reasonable reading, record each reading with its impact.
6. **Produce output** in the format below.

---

# Output Format

```markdown
## Goal Extraction

### Explicit Goal
- <goal> — evidence: "<verbatim quote>"

### Expected Outcome
- <outcome from the user's perspective> — evidence: "<verbatim quote or 'not stated'>"

### Implicit Goals
- IG-1: <goal> — evidence: "<verbatim quote>" — why required: <one line>

### Goal Ambiguities
- GA-1: <ambiguous point> | readings: A) ... B) ... | impact: <what changes>
```

The `Implicit Goals` and `Goal Ambiguities` sections are omitted when empty. The delegating worker maps the explicit goal and expected outcome into `[objective]` and `[expected_outcome]`, and routes goal ambiguities into `[[ambiguities]]`.
