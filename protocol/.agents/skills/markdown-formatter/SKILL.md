---
name: markdown-formatter
description: Produce or normalize Markdown so it matches the protocol artifact conventions defined by the contracts in .agents/contracts/ and .agents/orchestrators/core/contracts/. Use when asked to draft or rewrite an artifact section, report, or document and the output must stay structurally consistent with the protocol's Markdown style. Never alters artifact semantics or contract-required fields.
when_to_activate: The task involves producing or rewriting Markdown content for a protocol artifact (e.g. CONTEXT_ARTIFACT.md, EXECUTION_SUMMARY.md) or a project document that must follow protocol formatting conventions.
when_not: The task changes artifact structure or contract fields (that belongs to the governing contract, not to formatting), or the content is not Markdown.
---

# Mission

Produce Markdown that is structurally consistent with the protocol's artifact contracts and the style of the surrounding document.

Formatting is a mechanical concern: this skill never invents content, never removes contract-required sections, and never reinterprets the artifact's meaning.

---

# Workflow

## 1. Identify the governing contract

Determine which contract governs the target artifact:

- Cross-cutting artifacts: `.agents/contracts/` (e.g. `SESSION_LOG.md`, `REVIEW_REPORT.md`).
- Core orchestrator artifacts: `.agents/orchestrators/core/contracts/` (e.g. `CONTEXT_ARTIFACT.md`, `EXECUTION_SUMMARY.md`).

Read the contract before writing. The contract defines required sections, section order, and typed blocks (e.g. the `toml` fenced blocks used in `CONTEXT_ARTIFACT.md`). Formatting never overrides them.

## 2. Match the surrounding style

When editing an existing document, mirror its conventions:

- Heading levels and separator rules (`---` between major sections, as in the protocol's workflow and artifact documents).
- List style (`*` vs `-`), fenced code blocks with explicit language tags, and concise line length.
- Front matter format already present in the file family (YAML `---` vs TOML `+++`); never mix them in one file.

## 3. Apply communication standards

If the `caveman` feature flag is enabled, free-text sections follow `.agents/standards/communication/CAVEMAN.md`. Apply output-efficiency rules from `.agents/standards/communication/OUTPUT_EFFICIENCY.md`: no filler, no decorative prose.

## 4. Verify structural integrity

Before delivering, check:

- Every contract-required section is present, in order, with its exact heading.
- Typed blocks keep their declared language (`toml`, `text`, `bash`) and parse cleanly.
- Links and file references resolve against the repository.
- No trailing whitespace, no mixed list markers, no broken tables.

---

# Rules

- Never add, rename, or remove contract-defined sections or fields.
- Never change the semantic content while reformatting; if content is ambiguous, report it instead of rewriting it.
- Never fabricate contract citations; only cite contracts that exist on disk.
- Keep formatting minimal and diff-friendly: change only what is inconsistent.
- Do not format files inside `.agents/` unless the delegated task explicitly covers them (see the project boundary policy in `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`).

---

# Output Format

The formatted Markdown content itself, ready to be embedded as a section inside the deliverable requested by the invoker. When only a reformat was applied, precede the content with a one-line summary of the inconsistencies fixed. No commentary, no changelog beyond that line.

---

# Protocol Boundary

This skill describes a capability. Its output is delivered in the format and structure the invoker requests, and on any conflict between this skill and the invoker's instructions, the invoker wins. This skill does not grant authority or permissions.
