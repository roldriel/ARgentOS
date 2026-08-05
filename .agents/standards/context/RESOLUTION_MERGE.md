# Resolution Policy — Merge

This policy defines when two compatible context candidates with partial overlap are fused into one, and what form the fused result takes, when the Orchestrator assembles a worker payload. It is one of the Resolution policies of `.agents/standards/context/`.

## 1. Concept

Two or more candidates present **mergeable overlap** when they are mutually compatible (no contradiction), neither fully contains another, and they share part of their information. Composing them separately would duplicate the shared part and fragment one conceptual unit into two payload elements. Merging integrates them into a single candidate.

The boundary with deduplication is the containment test: total containment belongs to `RESOLUTION_DEDUPLICATION.md`; partial overlap without containment belongs here. A pair never satisfies both.

**Evaluation audience:** all rules in this policy are `[agent]` — judging that two candidates form one conceptual unit and rewriting them without loss is agent judgment. No machine gate applies; deterministic fragment-joining would be a harness Future Extension.

## 2. When to merge

Merge when **all** of the following hold:

1. The candidates are compatible: merging them introduces no contradiction.
2. They share information (the overlap is real, not incidental wording).
3. They belong to one conceptual unit for the task at hand — e.g., two excerpts of the same document section, two fragments of one rule, a constraint and its example.
4. The merged result fits the applicable budget (`CONTEXT.md` §3–§4) without triggering compression of other content.

Do **not** merge candidates that merely share a topic but answer different questions of the task; they stay separate elements of the payload.

## 3. Form of the merged result

- A single payload element that contains the shared information **once**, plus the non-shared parts of each source, preserving every acceptance criterion, constraint, and authority declaration of the sources. No information of either source is lost.
- If the sources mix inline content and references, the merged element declares which form prevails for the shared part (per `CONTEXT.md` §9, mixing inline and reference for the same standard without precedence is an anti-pattern).
- The merged element keeps the citations of all its sources, so the worker can read any source in full.
- The merge is recorded in `SESSION_LOG.md` with the sources and the resulting element. `[agent]`

## 4. Examples

- The task needs a domain rule whose statement lives in a standard and whose project-specific values live in `technical-analysis.md`. Merge: one element stating the rule once with the project values attached, citing both sources.
- Two KB excerpts quote overlapping halves of the same architecture decision. Merge: one element with the decision stated once and the non-overlapping rationale from both excerpts.
- A task-specification constraint and a KB note give *different* values for the same parameter. This is not mergeable overlap (they are not compatible): the situation belongs to `RESOLUTION_UNRESOLVABLE_CONFLICTS.md`.
