# Composition Policy — Optimization

This policy defines the criteria for adapting the final form of the worker payload to the execution purpose, for the prompt-based runtime. It is one of the Composition policies of `.agents/standards/context/` and applies after `COMPOSITION_COMPRESSION.md`.

## 1. Concept

**Optimization** improves the *adequacy* of the payload's form to the Worker's execution purpose: how the already-decided, already-compressed content is structured and presented. Optimization does not reduce cost as a goal (that is Compression), does not change which candidates are included (that is Resolution), and does not produce runtime-specific rendering mechanics beyond the prompt conventions already declared in `CONTEXT.md`.

**Evaluation audience:** all rules in this policy are `[agent]` — adequacy to a purpose is judgment. No machine gate applies; deterministic format validators would be a harness Future Extension.

## 2. Criteria for the prompt runtime

When composing the final payload, the Orchestrator optimizes its form by these criteria:

1. **Ordering by consumption.** Content appears in the priority order of `CONTEXT.md` §1: what the Worker must act on first (task specification, protocol state, output mode) precedes supporting material (session artifacts, KB summaries). The Worker should not have to read the whole payload to find its obligations.
2. **Compact structural form over prose.** Where the payload expresses rules, use the compact tags of `CONTEXT.md` §8.1; where it expresses a strict output format or repeated pattern, use a one-shot example (`CONTEXT.md` §8.3). Prose is reserved for task-specific content with no established compact form.
3. **Single representation per fact.** Each rule or fact appears exactly once, in one form (tag, inline, or reference), with declared precedence if a standard is both tagged and referenced (`CONTEXT.md` §9 anti-patterns).
4. **Purpose-fit granularity.** Detail is proportional to the phase: an execution payload carries exact signatures, values, and error messages inline (`CONTEXT.md` §8.2); an analysis payload carries questions and options. Content whose granularity does not match the phase's purpose is re-expressed, not merely copied.
5. **Worker-legible boundaries.** The payload makes explicit where the task ends and the context begins (sections or field structure per the delegation contract, `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` §"Required Invocation Payload"), so the Worker can distinguish obligations from background.

## 3. Order and invariants

- Optimization applies **after** Compression (see `COMPOSITION_COMPRESSION.md` §4). No optimization choice may be undone by a later compression step; if the payload still exceeds its budget after optimization, the flow returns to compression — or, when compression is exhausted, to the Resolution policies (budget conflict, `RESOLUTION_UNRESOLVABLE_CONFLICTS.md`).
- Optimization never adds, removes, or substitutes content candidates, never changes their priority, and never weakens the four protected elements of `COMPOSITION_COMPRESSION.md` §3 (authority, acceptance criteria, critical constraints, protocol state).
- Optimization stays inside the protocol's conceptual payload: it shapes *what the prompt text conveys and how it is organized*. It does not define rendering mechanics of other runtimes; a non-prompt runtime declares its own optimization criteria in its own materialization document (the same pattern as `.agents/standards/context/BUDGET_MATERIALIZATION.md` §6).

## 4. Examples

- A payload that opens with three KB excerpts and buries the task specification at the end violates criterion 1: reorder so the specification, `[STATE:...]` and `[OUTPUT:...]` lead.
- A naming rule pasted as a full paragraph when `[NAMING:Suffix]` is an active valid tag violates criterion 2: use the tag.
- A dependency rule conveyed both as `[DEPENDENCY:Views->Services->Models]` and as an inline paraphrase with different wording violates criterion 3: keep one form; if both must remain, declare which prevails.
- An execution-phase payload that inlines a 900-character standard section "for completeness" instead of the exact two lines the Worker must apply violates criterion 4: re-express at execution granularity.
