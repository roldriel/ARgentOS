---
name: normalizer
description: Normalize terminology and formatting across heterogeneous sources (code, docs, configs, external notes) into a single consistent vocabulary and style for a context deliverable. Use when asked to consolidate collected information that arrives with conflicting names, units, or formats. Never invents terms and never resolves semantic contradictions — those are reported as unknowns.
when_to_activate: The task involves consolidating context from multiple sources with inconsistent terminology, naming, or formats before assembling a context deliverable (e.g., a context document).
when_not: Sources already share a consistent vocabulary, or the inconsistency is a semantic contradiction that must be escalated for clarification rather than normalized.
---

# Mission

Turn heterogeneous collected context into a single, consistent vocabulary and format, so the context artifact is readable and unambiguous.

Normalization is mechanical alignment, not interpretation: when two sources genuinely disagree about facts, that is a contradiction to report, not a spelling to fix.

---

# Workflow

## 1. Collect the raw variants

From the gathered sources (repository files, documentation, configuration, tests — whatever sources the invoker supplied or pointed to), extract every distinct term or format used for the same concept: component names, module paths, versions, units, date/number formats.

## 2. Choose the canonical form

Apply this precedence:

1. The protocol taxonomy `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` for protocol-level terms (states, artifacts, actors).
2. Project conventions documented in the project itself (glossaries, naming standards, existing artifact usage).
3. The most frequent form in the project's own code and docs.
4. The form used by the task specification.

Never invent a new canonical term; pick one that already exists.

## 3. Apply the mapping

Rewrite the collected context using canonical forms consistently: one name per component, one format per date/unit/identifier. Keep a mapping table of every substitution made (variant → canonical), with the source where each variant appeared.

## 4. Report unresolved conflicts

When sources contradict each other semantically (different values, incompatible behaviors), do not normalize. Record them in the deliverable's `Unknowns` section (or the equivalent structure the invoker requests) so the invoker can escalate them for clarification.

---

# Rules

- Every canonical term must come from an existing source; never coin terms.
- Every substitution must be traceable to its variant and source in the mapping table.
- Never silently pick a side in a factual contradiction; report it.
- Do not alter quoted code or external citations to force terminological consistency; normalize prose around them and note the divergence.
- Output stays within the requested deliverable: this skill feeds the deliverable; it does not edit the source documents.

---

# Output Format

A normalized-context section to embed in the requested deliverable, containing:

```markdown
## Normalized Terminology

| Concept | Canonical form | Variants found | Sources |
| --- | --- | --- | --- |

## Normalized Content

<context rewritten with canonical terms and formats>

## Unresolved Conflicts

- <contradiction, sources, values per source> (or "None")
```

---

# Protocol Boundary

This skill describes a capability: it performs the normalization task it is given and delivers its output in the format and structure the invoker requests. On any conflict between this skill and instructions from the invoker, the invoker's instructions win. This skill does not grant authority or permissions.
