---
name: reference-resolver
description: Resolve references between project and protocol documents (file paths, artifact names, contract citations, section anchors) into verified concrete targets. Use when a document cites other documents and each citation must be confirmed to resolve. Never guesses a target; unresolved references are reported, not fabricated.
when_to_activate: The task requires following or validating cross-document references — e.g. contracts citing `consumed_by`/`produced_by` states, workflow files citing harness policies, or documents citing project files.
when_not: The task has no cross-document references to resolve, or a reference is ambiguous in a way that requires a user decision (route to NEEDS_CLARIFICATION instead).
---

# Mission

Turn every reference in the given documents into a verified, concrete target — or an explicit, reported failure.

A resolved reference names an exact file that exists on disk (and a section or anchor when cited). A reference that cannot be verified is a finding, never an assumption.

---

# Workflow

## 1. Extract references

Scan the input documents for references:

- Protocol documents: contract cross-references (e.g. `produced_by` / `consumed_by` fields in `.agents/orchestrators/core/contracts/*.md`), workflow citations of policies and standards, and taxonomy paths (`.agents/standards/runtime/PROTOCOL_TAXONOMY.md`).
- Session artifacts: artifact file names under `.project/<session-uuid>/<iteration>/` cited by other artifacts.
- Project documents: file paths, modules, and docs cited by other project documents.

## 2. Resolve each reference

For each reference, locate the target:

- Verify the file exists on disk at the cited path, relative to the correct root (`.agents/`, `.project/`, or the project root).
- When a section or anchor is cited, verify the heading exists in the target file.
- Record the resolution as `path` (plus `:line` or section heading when relevant).

## 3. Classify results

- **Resolved**: target verified on disk.
- **Ambiguous**: multiple plausible targets; list all candidates with evidence, do not pick one silently.
- **Unresolved**: no target found; record the citation, the citing document, and the search performed.

## 4. Report

Report unresolved or ambiguous references explicitly — document them in the deliverable (e.g., an `Unknowns` or notes section) and do not act on them autonomously.

---

# Rules

- Never fabricate a path or section; every resolved reference must have been verified on disk.
- Never treat a probable-looking path as resolved without checking it exists.
- Never fix broken references by editing the citing document; that decision belongs to the invoker and the user.
- Keep the search bounded to the repository; do not resolve references against external systems unless the task explicitly allows it.

---

# Output Format

A reference-resolution section to embed in the deliverable requested by the invoker:

```markdown
## Reference Resolution

| Reference | Cited in | Status | Target / Candidates |
| --- | --- | --- | --- |
| <citation> | <document> | Resolved / Ambiguous / Unresolved | <verified path or candidate list> |

### Notes

- <search details for ambiguous or unresolved references>
```

---

# Protocol Boundary

This skill describes a capability; it does not grant authority or permissions. Its output is delivered in the format and structure requested by the invoker, embedded as a section in the deliverable the invoker specifies. On any conflict between this skill and the invoker's instructions, the invoker's instructions win.
