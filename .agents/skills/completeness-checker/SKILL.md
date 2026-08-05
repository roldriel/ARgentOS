---
name: completeness-checker
description: Detect missing information in a protocol artifact or input set against what the current phase explicitly requires — required sections, fields, evidence, or unresolved unknowns. Use during phase 04-validate-context or phase 07-verify. Evaluates only; never fills gaps and never edits artifacts.
when_to_activate: The delegated task requires determining whether an artifact or context set contains everything its phase demands — typically the context validator deciding between VALIDATED and NEEDS_MORE_CONTEXT in phase 04, or the verifier in phase 07.
when_not: The task is contract structure validation (use artifact-validator), contradiction detection (use consistency-checker), or quality scoring (use rubric-checker). Completeness asks "is something missing?", not "is it well-formed?" or "is it good?".
---

# Mission

Determine what information the current phase requires that is absent from the artifacts at hand, and whether each gap blocks the workflow or can be tolerated. The verdict belongs to the delegating role; this skill supplies the gap inventory with evidence.

---

# Protocol Boundary

This skill assists the Worker inside the phase that delegated it. Its output is embedded as a section inside that phase's artifact (e.g. `CONTEXT_VALIDATION_REPORT.md` or `VERIFICATION_REPORT.md`); the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Workflow

1. **Establish what is required**: read the delegating phase's workflow module (e.g. `.agents/orchestrators/core/workflow/04-validate-context.md` or `07-verify.md`) and the artifact contracts it consumes and produces. The required inputs/outputs define completeness — not intuition.
2. **Inventory what exists**: list the artifacts and sections actually present in the current iteration.
3. **Diff requirements against reality**, looking for:
   - required artifacts or sections entirely absent
   - required fields present but empty or placeholder
   - claims that cite evidence (files, tests, outputs) that is not included or does not exist
   - unknowns declared in earlier artifacts (`TASK_SPECIFICATION.md` `unknowns`, unconfirmed `[[assumptions]]`) that the phase was supposed to resolve but did not
4. **Classify each gap**: BLOCKER (the phase cannot validly conclude without it) vs. NON-BLOCKER (noted, but the phase can proceed). A gap is a blocker when the phase's decision or the next phase's execution depends on the missing information.
5. **Report** each gap with the exact requirement source (workflow module or contract section) so the finding is auditable.

---

# Rules

- Judge completeness only against written requirements (workflow modules, contracts); do not invent "nice-to-have" gaps.
- Never fill a gap yourself, never suggest content for it, never modify any artifact — report what is missing and why it matters.
- Distinguish "missing" from "present but wrong" (wrong belongs to consistency-checker or rubric-checker) and from "present but malformed" (artifact-validator).
- Every finding cites the requirement source and the location where the information should appear.
- If nothing is missing, say so and list the requirements checked.

---

# Output Format

```markdown
## Completeness Check

- Phase requirements: <workflow module / contract paths>
- Artifacts examined: <list>

### Gaps

| # | Severity | Requirement Source | Missing Information | Impact |
|---|----------|--------------------|---------------------|--------|
| 1 | BLOCKER | 04-validate-context.md input_artifacts | CONTEXT_ARTIFACT.md absent | validation cannot run |

### Summary

- BLOCKER: n — NON-BLOCKER: n
- Result: COMPLETE | INCOMPLETE (blockers listed)
- Requirements checked: <list>
```
