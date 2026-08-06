---
name: completeness-checker
description: Detect missing information in an artifact or input set against an explicit set of requirements — required sections, fields, evidence, or unresolved unknowns. Use when asked to check whether a deliverable contains everything a stated requirement demands. Evaluates only; never fills gaps and never edits artifacts.
when_to_activate: The delegated task requires determining whether an artifact or input set contains everything its governing requirements demand — e.g., deciding whether a deliverable is complete enough to accept or must be sent back for more input.
when_not: The task is contract structure validation (use artifact-validator), contradiction detection (use consistency-checker), or quality scoring (use rubric-checker). Completeness asks "is something missing?", not "is it well-formed?" or "is it good?".
---

# Mission

Determine what information the stated requirements demand that is absent from the artifacts at hand, and whether each gap blocks acceptance or can be tolerated. The verdict belongs to the invoker; this skill supplies the gap inventory with evidence.

---

# Protocol Boundary

This skill describes a capability: it performs the completeness check requested by its invoker and delivers its output in whatever format or structure the invoker asks for (by default, the output format below). On any conflict between this skill and the invoker's instructions, the invoker's instructions win. This skill grants no authority or permissions.

---

# Workflow

1. **Establish what is required**: read the requirement sources identified by the invoker (e.g. specification documents, contracts, checklists) and any artifacts they consume and produce. The stated requirements define completeness — not intuition.
2. **Inventory what exists**: list the artifacts and sections actually present in the material under review.
3. **Diff requirements against reality**, looking for:
   - required artifacts or sections entirely absent
   - required fields present but empty or placeholder
   - claims that cite evidence (files, tests, outputs) that is not included or does not exist
   - unknowns declared in earlier artifacts (e.g. an `unknowns` list, unconfirmed `[[assumptions]]`) that the requirements expected to be resolved but were not
4. **Classify each gap**: BLOCKER (the deliverable cannot validly be accepted without it) vs. NON-BLOCKER (noted, but work can proceed). A gap is a blocker when a downstream decision or execution depends on the missing information.
5. **Report** each gap with the exact requirement source (document and section) so the finding is auditable.

---

# Rules

- Judge completeness only against written requirements (specifications, contracts, checklists provided by the invoker); do not invent "nice-to-have" gaps.
- Never fill a gap yourself, never suggest content for it, never modify any artifact — report what is missing and why it matters.
- Distinguish "missing" from "present but wrong" (wrong belongs to consistency-checker or rubric-checker) and from "present but malformed" (artifact-validator).
- Every finding cites the requirement source and the location where the information should appear.
- If nothing is missing, say so and list the requirements checked.

---

# Output Format

```markdown
## Completeness Check

- Requirements: <requirement source paths>
- Artifacts examined: <list>

### Gaps

| # | Severity | Requirement Source | Missing Information | Impact |
|---|----------|--------------------|---------------------|--------|
| 1 | BLOCKER | requirements.md §inputs | context document absent | validation cannot run |

### Summary

- BLOCKER: n — NON-BLOCKER: n
- Result: COMPLETE | INCOMPLETE (blockers listed)
- Requirements checked: <list>
```
