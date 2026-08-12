# Composition Policy — Compression

This policy defines the concrete compression techniques for the worker payload and integrates the compression rules already operative in `CONTEXT.md` §8. It is one of the Composition policies of `.agents/standards/context/`.

## 1. Concept

**Compression** reduces the representation cost of a context set whose membership was already decided (by relevance assessment and the Resolution policies of this directory). Compression never changes *which* candidates are in the payload — removing a task-relevant candidate is a Resolution decision (see `RESOLUTION_UNRESOLVABLE_CONFLICTS.md` for budget conflicts), not compression. Compression only changes *how* the same decided content is represented.

**Evaluation audience:** all rules in this policy are `[agent]`, except the size measurement of `CONTEXT.md` §8.4 and the 10 % threshold of `CONTEXT.md` §8.2, which are `[machine]`-computable in principle (character counts) and currently applied by the agent; a deterministic harness check of payload size is a harness Future Extension.

## 2. Permitted techniques (integrated from `CONTEXT.md` §8)

The following techniques are the complete, closed set of compression techniques for the prompt-based runtime:

1. **Reference instead of inline** (`CONTEXT.md` §8.2): stable, documented content is cited, not pasted; the 10 % threshold rule applies (content exceeding 10 % of the phase KB budget is referenced, not inlined).
2. **Compact tags** (`CONTEXT.md` §8.1): bracketed tokens replace prose rules; only listed tags are valid.
3. **One-shot examples** (`CONTEXT.md` §8.3): a compact example replaces a prose format description.
4. **Summarization** (`CONTEXT.md` §8.4, step 2): KB entries are summarized preserving acceptance criteria and constraints.
5. **Omission by relevance** (`CONTEXT.md` §8.4, step 1): only as part of the compression budget rule, and only over the KB portion it scopes — dropping the lowest-relevance KB entries when the budget is exceeded. This is the single sanctioned exception to §1: it is a budget-rule action over KB entries, logged per entry, and never touches the four protected elements of §3 below.
6. **Split** (`CONTEXT.md` §8.4 step 4, §8.5): multi-turn decomposition when compression cannot fit the content.

## 3. Lossless rule

Compression is **lossless-by-decision**: every compression step must preserve the information the payload decided to carry. Concretely (integrating `CONTEXT.md` §8.4), after compression the payload must still contain:

- Authority: the canonical sources that apply.
- Acceptance criteria from `TASK_SPECIFICATION.md`.
- Critical constraints (security, dependencies, layers).
- Current protocol state.

If a compression step would lose any of these, that step is forbidden. Compression with verifiable information loss is out of scope of machine checking and remains agent judgment.

## 4. Order with Optimization

Compression applies **before** Optimization (`COMPOSITION_OPTIMIZATION.md`): optimization chooses the final form of the payload, and that choice must be made over a representation whose cost is already reduced, so that no later compression step undoes the chosen form. In practice the Orchestrator first applies §8 of `CONTEXT.md` until the payload fits its budgets, then applies the Optimization policy.

## 5. Examples

- A 1200-character KB excerpt needed for execution: the phase KB budget is 4000 characters, so the 10 % threshold (400 characters) is exceeded → reference the entry with a one-line summary instead of inlining it.
- Payload over budget after referencing: summarize the remaining KB entries (preserving constraints), then — if still over — omit the lowest-relevance entry and log it, then — if still over — split the task per `CONTEXT.md` §8.5.
- Replacing the prose "ask for clarification if anything is unclear; keep output minimal" with `[NO_ASSUME]` and `[OUTPUT:minimal]`.
