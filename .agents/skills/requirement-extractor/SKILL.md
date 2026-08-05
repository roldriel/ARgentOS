---
name: requirement-extractor
description: Extract functional and non-functional requirements, restrictions, and ambiguities from a raw user request, with verbatim evidence for each item. Use when a worker must turn an unstructured request into an auditable requirements list during task analysis (phase 00, core:ANALYZING_TASK).
when_to_activate: The delegated task requires identifying explicit requirements, restrictions, and ambiguities from the user request to populate TASK_ANALYSIS.md during phase 00.
when_not: The task already has a validated TASK_SPECIFICATION.md, or the request is to implement, plan, or verify rather than to analyze the request.
---

# Mission

Extract every functional and non-functional requirement the user actually stated, plus the restrictions and ambiguities that follow from the request. Nothing more.

The objective is not to interpret charitably.

The objective is a faithful, evidence-backed inventory of what the user asked for, so that phase 00 (`core:ANALYZING_TASK`) can populate the Explicit Requirements, Explicit Restrictions, and Detected Ambiguities sections of `TASK_ANALYSIS.md` (contract: `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`).

Optimize for:

* fidelity to the user's words
* completeness (no dropped requirement)
* separation of stated fact from inference

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`00-analyze-task`). Its output is embedded as a section inside the phase artifact: the phase contract (`TASK_ANALYSIS.md`) defines the envelope, this skill defines the content of the requirements-extraction section. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

* Never invent requirements the user did not state or imply directly.
* Never resolve ambiguities silently: an ambiguity with an implementation impact MUST be reported, not assumed away (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`).
* Never gather technical context, propose solutions, or plan implementation: that belongs to later phases.
* Do not modify project files.

---

# Workflow

1. **Restate the source.** Copy the original request verbatim; all evidence quotes resolve against it.
2. **Extract functional requirements.** Each describes *what* the outcome must do. Attach a verbatim quote as evidence.
3. **Extract non-functional requirements.** Quality attributes and constraints on *how*: performance, security, compatibility, style, tooling, process constraints (e.g. TDD, language, deadlines).
4. **Extract explicit restrictions.** Things the user forbade or bounded ("do not touch X", "keep it under N").
5. **Detect ambiguities.** Points where more than one reasonable reading exists and the choice changes implementation. For each, record impact and at least two concrete options plus an "Other" escape, per the `[[ambiguities]]` contract.
6. **Classify confidence.** HIGH when every requirement has direct evidence; downgrade when inference or unresolved ambiguity remains.
7. **Produce output** in the format below.

---

# Output Format

Embedded as a section inside `TASK_ANALYSIS.md`:

```markdown
## Requirement Extraction

### Functional Requirements
- FR-1: <requirement> — evidence: "<verbatim quote>"

### Non-Functional Requirements
- NFR-1: <requirement> — evidence: "<verbatim quote>"

### Explicit Restrictions
- R-1: <restriction> — evidence: "<verbatim quote>"

### Ambiguities
- A-1: <ambiguity> | impact: <what it changes> | options: A) ... B) ... Other) user-defined

### Extraction Confidence
HIGH | MEDIUM | LOW — <one-line reason>
```
