---
name: terminology-enforcer
description: Enforce the protocol's canonical vocabulary in artifacts by detecting non-canonical terms and proposing the correct term from the master dictionary .agents/standards/runtime/PROTOCOL_TAXONOMY.md. Use in any phase that writes or rewrites protocol artifacts. Reports corrections to the delegating worker; never edits the artifact directly and never renames project-level (non-protocol) terms.
when_to_activate: The delegated phase produces or revises a protocol artifact (TASK_SPECIFICATION.md, CONTEXT_ARTIFACT.md, EXECUTION_PLAN.md, or similar) and its protocol-level terms (states, artifacts, actors, harness IDs) must match the canonical taxonomy.
when_not: The vocabulary to align is project-level terminology across gathered sources (use normalizer), the task is to validate artifact contract structure (use artifact-validator), or the content contains no protocol-level terms.
---

# Mission

Keep protocol artifacts speaking the protocol's own language: every state, artifact, actor, lifecycle, and harness ID named in an artifact must match the master dictionary exactly, so references stay unambiguous across sessions and domains.

The dictionary of record is `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, validated by harness policy H13 (`test_protocol_taxonomy.py`). This skill detects deviations from it; it does not extend or reinterpret it.

---

# Protocol Boundary

This skill assists the Worker within the phase that delegates it (any phase that writes artifacts); its output is embedded as a section inside the artifact of that phase, and the phase contract defines the surrounding envelope. On any conflict between this skill and the protocol — including the taxonomy itself — the protocol wins. This skill describes a capability; it does not grant authority or permissions.

---

# Workflow

1. **Read the taxonomy**: load `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` and extract the canonical names for the entity kinds relevant to the artifact (states, artifacts, actors, roles, lifecycles, harness IDs), including reference forms such as `<domain>:<state>` (e.g. `core:ANALYZING_TASK`).
2. **Scan the artifact content** provided by the delegating worker for protocol-level term usage: capitalized state-like names, artifact file names, role names, harness IDs (`HNN`/`DNN`/`SNN`).
3. **Classify each occurrence**:
   - *Canonical*: matches the dictionary exactly — no action.
   - *Non-canonical*: clearly refers to a dictionary entity under a wrong or outdated name (wrong casing, old ID, alias) — propose the canonical term.
   - *Unknown*: looks protocol-level but matches no dictionary entity — flag; never map it by guessing.
4. **Respect scope**: project-level terms (component names, business vocabulary, user wording) are out of scope even when they resemble protocol terms. Quoted user text and external citations are never rewritten.
5. **Deliver the correction report** to the delegating worker, who applies accepted corrections to the artifact. This skill never edits the artifact itself.

---

# Rules

- Every proposed correction must cite the exact canonical term as it appears in the taxonomy file; never fabricate a term or a dictionary entry.
- Never "correct" a term to something the dictionary does not contain; unknown terms are flagged, not mapped.
- Do not touch quoted code, user quotes, or external citations; note the divergence instead.
- A clean scan is a valid result: if everything is canonical, say so and list what was checked.
- The taxonomy file is read-only for this skill; gaps or errors in it are reported to the delegating worker, not fixed here.

---

# Output Format

```markdown
## Terminology Enforcement

- Artifact scanned: <path or description>
- Canonical occurrences verified: <n>

### Corrections Proposed

| # | Location | Non-canonical term | Canonical term | Evidence |
|---|----------|--------------------|----------------|----------|
| 1 | section X | "planning phase" | `core:PLANNING` state `PLANNING` | PROTOCOL_TAXONOMY.md states entry |

### Unknown Protocol-Level Terms (flagged, not mapped)

- <term> at <location> — no matching dictionary entry (or "None")
```

Both sections are reported as empty/none when there are no findings; the delegating worker embeds the result per the phase contract.
