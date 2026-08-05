---
name: reference-resolver
description: Resolve references between project and protocol documents (file paths, artifact names, contract citations, section anchors) into verified concrete targets. Use during phases 03-gather-context and 06-execute when a document cites other documents and the Worker must confirm each citation resolves. Never guesses a target; unresolved references are reported, not fabricated.
when_to_activate: The delegated task requires following or validating cross-document references — e.g. contracts citing `consumed_by`/`produced_by` states, workflow files citing harness policies, or artifacts citing project files — during context gathering or execution.
when_not: The task has no cross-document references to resolve, or a reference is ambiguous in a way that requires a user decision (route to NEEDS_CLARIFICATION instead).
---

# Mission

Turn every reference encountered during the phase into a verified, concrete target — or an explicit, reported failure.

A resolved reference names an exact file that exists on disk (and a section or anchor when cited). A reference that cannot be verified is a finding, never an assumption.

---

# Workflow

## 1. Extract references

Scan the input documents for references:

- Protocol documents: contract cross-references (e.g. `produced_by` / `consumed_by` fields in `.agents/orchestrators/core/contracts/*.md`), workflow citations of policies and standards (e.g. `.agents/orchestrators/core/workflow/03-gather-context.md` citing harness trigger policies), and taxonomy paths (`.agents/standards/runtime/PROTOCOL_TAXONOMY.md`).
- Session artifacts: artifact file names under `.project/<session-uuid>/<iteration>/` cited by other artifacts.
- Project documents: file paths, modules, and docs cited by the task specification or context artifact.

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

During 06-execute, unresolved or ambiguous references in plan inputs are blockers to report per the phase rules in `.agents/orchestrators/core/workflow/06-execute.md` (document, do not act autonomously). During 03-gather-context, feed them into the artifact's `Unknowns` section.

---

# Rules

- Never fabricate a path or section; every resolved reference must have been verified on disk.
- Never treat a probable-looking path as resolved without checking it exists.
- Never fix broken references by editing the citing document; that decision belongs to the Orchestrator and the user.
- Keep the search bounded to the repository; do not resolve references against external systems unless the task explicitly allows it.

---

# Output Format

A reference-resolution section to embed in the delegating phase's artifact:

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

This skill assists the Worker within the phase that delegates it (typically 03-gather-context or 06-execute); its output is embedded as a section inside the artifact of that phase, whose contract defines the surrounding envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it does not grant authority or permissions.
