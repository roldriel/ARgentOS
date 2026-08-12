---
name: reflection
description: Reevaluate work in progress before declaring it finished — check whether the current approach still serves the objective, whether drift has crept in, and whether to continue, adjust, or stop. Use when asked to reassess an ongoing solution while the result is still in course.
when_to_activate: The task requires a mid-course reassessment of an ongoing solution, e.g. after a failed step, a scope question, or before a point of no return.
when_not: The result is already finished and must be audited before reporting (use self-review: reflection reevalúa el resultado EN CURSO, self-review audita el resultado TERMINADO), or the task is to generate new content.
---

# Mission

Catch a wrong trajectory while there is still time to correct it.

The objective is not to re-do the work.

The objective is a structured pause: compare the work in progress against the objective it serves, detect drift, sunk-cost attachment, or changed premises, and produce a continue / adjust / stop recommendation with reasons. Reflection questions the *direction*; it does not audit the finished deliverable.

Optimize for:

* honesty about drift over loyalty to the current path
* premise checking (is what we assumed at the start still true?)
* actionable recommendations, not vague unease

---

# Protocol Boundary

This skill describes a capability: given a reassessment task, it performs it and delivers its output. Its output is embedded wherever the invoker requires it (e.g., as a section inside a summary or report document); the invoker defines the envelope. On any conflict between this skill and instructions from the invoker, the invoker's instructions win. This skill grants no authority or permissions.

---

# Safety Rules

* This skill REEVALUATES: it does not rewrite the work, does not modify artifacts, and does not audit the finished deliverable (that is self-review). Its product is a reflection report handed to the invoker.
* Check premises, not just progress: if a starting assumption turned out false, say so even when execution is "on track".
* Sunk cost is not evidence: work already invested does not justify continuing a wrong approach.
* No silent pivots: if the recommendation is to change direction, state what changes and why; the decision to replan belongs to the invoker.
* If reassessment reveals an unstated user decision, escalate per `.agents/standards/requirements/NO_ASSUMPTIONS.md` instead of resolving it.

---

# Workflow

1. **Restate the objective** from the task specification, and the approach currently being followed.
2. **Check premises**: are the assumptions the approach was chosen under still true?
3. **Check alignment**: does the work in progress still serve the acceptance criteria, or has the target drifted (or the work drifted from the target)?
4. **Check trajectory**: is the current approach converging? Signs it is not: growing complexity, repeated failures at the same point, workarounds stacking up.
5. **Consider the alternatives honestly**: given what is now known, would this approach still be chosen? What would be chosen instead?
6. **Recommend**: `continue` (approach sound, premises intact), `adjust` (sound direction, course correction needed — specify it), or `stop` (premises broken or wrong direction — flag for replan or clarification).
7. **Produce output** in the format below.

---

# Output Format

Delivered in the format requested by the invoker; by default, as a section to embed in a report:

```markdown
## Reflection

- Objective: <restated>
- Current approach: <one or two sentences>
- Recommendation: continue | adjust | stop

### Premise Check
- <assumption> — still valid? yes/no — evidence: <observation>

### Alignment & Trajectory
- <drift, convergence signals, or confirmation of alignment>

### Rationale
- <why this recommendation; if adjust/stop: what changes and what decision the invoker or user must take>
```
