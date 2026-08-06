---
name: deduplicator
description: Remove redundancy across gathered sources by detecting repeated or overlapping information and preserving a single canonical instance with its citation. Use when asked to consolidate material where multiple sources repeat the same facts before building a consolidated deliverable. Never merges semantically distinct content and never resolves factual contradictions — those are reported.
when_to_activate: The task involves consolidating gathered material where several sources repeat the same facts, code excerpts, or statements, and the redundancy would bloat or confuse the resulting deliverable.
when_not: The inconsistency is terminological rather than redundant content (use normalizer), the task is to compress length without duplication (use summarizer), or sources contradict each other factually (report the conflict back to the invoker instead of picking one).
---

# Mission

Collapse duplicated information from gathered sources into one canonical instance per fact, keeping its citation, so the requested deliverable states each thing exactly once without losing provenance.

Deduplication is about *sameness*, not style: two sources saying the same thing in different words are duplicates; two sources saying different things are not, no matter how similar they look.

---

# Protocol Boundary

This skill describes a capability: it is given a deduplication task, performs it, and delivers its output in the format or structure the invoker requests. On any conflict between this skill and the invoker's instructions, the invoker's instructions win. This skill does not grant authority or permissions.

---

# Workflow

1. **Inventory the gathered material**: list every information unit (fact, excerpt, statement) with its source and location, from the sources provided with the task.
2. **Group duplicates**: cluster units that assert the same fact or quote the same content, even when wording differs. When in doubt, keep units in separate groups — a false merge loses information.
3. **Elect the canonical instance** per group, by precedence:
   - The most precise and complete formulation.
   - The most authoritative source (project code/docs over external notes).
   - The most recent, when the fact is time-sensitive.
4. **Preserve citations**: record every source where the fact appeared; the canonical instance keeps its own citation and the group records the rest as corroborating sources.
5. **Report near-duplicates and contradictions**: units that overlap partially (same subject, different details) are flagged, not merged. Units that assert incompatible facts are reported as conflicts, not deduplicated.
6. **Deliver the deduplicated set** to the invoker; never edit source documents or the deliverable directly.

---

# Rules

- Never merge units that differ in meaning, scope, or conditions; similarity is not sameness.
- Every canonical instance must retain a citation to its original source; no orphan facts.
- Never drop a minority source silently: if a corroborating source adds any detail the canonical instance lacks, that detail survives in the output.
- Do not fabricate sameness: if you cannot state what two units share, they are not a group.
- Do not alter quoted code or external citations to force them into one instance.

---

# Output Format

```markdown
## Deduplicated Content

- <canonical fact/excerpt> — canonical source: <path:loc>; also in: <path:loc>, <path:loc>

## Near-Duplicates (kept separate)

- <unit A> vs <unit B> — shared subject: <subject>; difference: <what differs>

## Conflicts (not deduplicated)

- <subject> — source X states <value/claim>, source Y states <value/claim>; requires resolution outside this skill
```

The third section is omitted when empty. The invoker embeds the confirmed content into the requested deliverable (e.g., a context document).
