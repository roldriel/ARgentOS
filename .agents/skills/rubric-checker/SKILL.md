---
name: rubric-checker
description: Evaluate a phase deliverable against the applicable rubric from .agents/standards/quality/RUBRICS.md (artifact rubrics 1-6 and technical-practice rubrics 7-19), producing a per-criterion level with evidence. Use when a reviewer or verifier must score an artifact before a critical transition or during phase 07-verify. Evaluates only; never modifies the deliverable.
when_to_activate: The delegated task requires scoring an artifact against a named rubric — typically the reviewer role before TASK_READY, CONTEXT_READY, PLAN_READY, or VERIFYING, or the verifier during phase 07-verify.
when_not: Rubrics are disabled by feature flag, no rubric applies to the artifact, or the task is structural contract validation (use artifact-validator) rather than quality scoring.
---

# Mission

Apply a rubric from `.agents/standards/quality/RUBRICS.md` faithfully and produce a per-criterion evaluation with observable evidence. The scale is `INSUFFICIENT`, `MEETS`, `EXCEEDS`. A critical criterion (✅) scored `INSUFFICIENT` forces a `REWORK` recommendation (reviewer) or a `RECOVERY` decision (verifier) — this skill reports the scores; the delegating role issues the recommendation.

---

# Protocol Boundary

This skill assists the Worker inside the phase that delegated it. Its output is embedded as the `## Rubric Evaluation` section defined by RUBRICS.md inside the artifact that governs that phase (e.g. `VERIFICATION_REPORT.md` or a Review Report per `.agents/contracts/REVIEW_REPORT.md`); the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Workflow

1. **Identify the rubric**: from the artifact type (e.g. `TASK_SPECIFICATION.md` → `TASK_SPECIFICATION_RUBRIC`) or from the delegation. When a technical-practice flag is enabled and selected in the task specification's `technical_approach`, apply the matching practice rubric (TDD, SRP, OCP, LSP, ISP, DIP, DRY, GRASP, architecture rubrics) in addition.
2. **Read the deliverable** and the reference artifacts the rubric implies (e.g. plan adherence requires the EXECUTION_PLAN; criteria evaluation requires the TASK_SPECIFICATION).
3. **Score every criterion**: pick the level whose description matches the observable evidence. Do not average, skip, or invent criteria.
4. **Record evidence** per criterion: quote or cite the exact artifact location that justifies the level. `EXCEEDS` requires explicit evidence of going beyond; `INSUFFICIENT` requires stating what is missing.
5. **Flag critical failures**: list every ✅ criterion scored `INSUFFICIENT` separately, since each one forces REWORK/RECOVERY at the role level.
6. **Report** using the section format below.

---

# Rules

- Evaluate only: never modify the deliverable or the reference artifacts.
- Evidence must come from the artifact itself or its references — never from assumptions about what "must have happened".
- Score what the rubric says, not personal quality opinion; if the rubric does not cover an aspect, it does not affect the score.
- When evidence is ambiguous between two levels, choose the lower one and say why.
- Never leave a criterion without a level or without an evidence line.

---

# Output Format

Follow the `## Rubric Evaluation` structure defined in RUBRICS.md:

```markdown
## Rubric Evaluation

### <RUBRIC_NAME>

- ✅ <Criterion name>            (✅ only when the criterion is critical)
  - Level: INSUFFICIENT | MEETS | EXCEEDS
  - Evidence: <brief justification with artifact location>

### Critical Failures

- <criterion>: <what is missing>   (section omitted when empty)
```

Repeat the rubric block for each applicable rubric (artifact rubric plus selected technical-practice rubrics).
