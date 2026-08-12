---
name: formatter
description: Reformat content into a declared target structure — Markdown, JSON, YAML, CSV, or a table — as requested by the invoker. Use when asked to deliver output in a specific format or convert content between formats. Covers all per-format outputs as use cases of one skill; never alters the semantic content being reformatted.
when_to_activate: The task requires output in a declared target format (e.g. "as JSON", "as a CSV", "as a table", "restructure this YAML") or a conversion between formats.
when_not: The target is Markdown that must follow specific document conventions (use markdown-formatter), the content itself must change (that is authoring, not formatting), or no explicit target format is declared.
---

# Mission

Reshape existing content into the target structure declared in the request, preserving every fact, value, and citation. One skill covers all supported formats — Markdown, JSON, YAML, CSV, and tables — as use cases of the same capability; no per-format variant exists.

Formatting is a structural transformation only: same content, different shape.

---

# Protocol Boundary

This skill describes a capability: it does not grant authority or permissions. Its output is delivered to the invoker, ready to be embedded wherever the invoker needs it; the invoker defines the surrounding envelope. On any conflict between this skill and instructions from the invoker, the invoker's instructions win.

---

# Workflow

1. **Read the declared target**: the request states the destination structure (format and, when relevant, schema, column set, or key layout). If no target is declared, stop and report it — do not guess one.
2. **Extract the content units** from the source: facts, records, fields, and their relationships. Build a neutral in-memory representation before choosing any syntax.
3. **Map to the target structure**:
   - *Markdown*: headings, lists, and fenced blocks with explicit language tags.
   - *JSON*: valid JSON, no trailing commas, no comments; arrays of objects for record sets.
   - *YAML*: plain YAML, explicit types, no anchors unless the source had them.
   - *CSV*: header row first, one record per line, quote fields containing commas or quotes.
   - *Table*: Markdown table, one column per declared field, one row per record.
4. **Validate the output** against its own format: JSON/YAML must parse, CSV must have uniform column counts, tables must have aligned columns, Markdown structure must render. Fix structural errors only.
5. **Verify content preservation**: every unit extracted in step 2 appears exactly once in the output; nothing added, nothing dropped, no value reworded.
6. **Deliver the formatted content** to the invoker; never write the destination artifact directly.

---

# Rules

- Never change, summarize, translate, or reinterpret content while reformatting; ambiguity is reported, not rewritten.
- Never invent fields, columns, keys, or values the source does not contain.
- Emit syntactically valid output for the chosen format; invalid JSON or unaligned tables are defects, not style.
- One format per output: never mix (e.g. YAML inside a CSV field) unless the request explicitly asks for it.
- When a content unit cannot be represented in the target format (e.g. free prose into CSV), report it as unmappable instead of forcing it.

---

# Output Format

The formatted content itself, in the declared target format, ready to be embedded as a section inside the deliverable requested by the invoker. Preceded by a single line:

```text
Format: <target>; units mapped: <n>; unmappable: <m> (<reasons, or "none">)
```

No commentary, no changelog beyond that line.
