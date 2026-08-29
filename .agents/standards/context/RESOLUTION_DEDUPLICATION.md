# Resolution Policy — Deduplication

This policy defines how redundant context candidates are detected and eliminated when the Orchestrator assembles a worker payload. It is one of the Resolution policies of `.agents/standards/context/`.

## 1. Concept

A candidate is **redundant** with respect to another when the information it contributes is **completely contained** in the other. The relation is total containment: removing the redundant candidate takes no information away from the payload. This is the policy's operational invariant:

> A deduplication step may only remove a candidate whose information is fully preserved by another candidate that remains.

Partial overlap is **not** redundancy: two candidates that share some information but each contribute something the other lacks belong to `RESOLUTION_MERGE.md`, not to this policy.

**Evaluation audience:** all rules in this policy are `[agent]` — containment of *information* is a judgment, not a string comparison. A future machine check (exact duplicate paths, identical excerpts) would cover only the trivial subset and is a harness Future Extension, not part of this policy.

## 2. Detection criteria

Treat a candidate as redundant when any of these holds:

1. **Same source, same section.** Two candidates resolve to the same document and the same section (e.g., a standard cited inline twice, or a KB entry that reproduces a protocol standard already referenced).
2. **Summary subsumed by source.** A KB summary is included while the artifact it summarizes (or a fuller, still-budget-compatible excerpt of it) is also included.
3. **Transitive inclusion.** A candidate is included as part of a larger unit (e.g., a rule already conveyed by an active compact tag of `CONTEXT.md` §8.1, or content inside an artifact included whole).

## 3. Resulting action

- Remove the redundant candidate; keep the containing one. When neither strictly contains the other, the situation is not redundancy — do not deduplicate.
- Between a redundant pair, the survivor is the candidate with higher authority per the source precedence of `RESOLUTION_TIE_BREAKING.md` §2 (criterion 2): the original beats its summary; the current-session artifact beats the KB note about it.
- Every removal is recorded in `SESSION_LOG.md` with the removed candidate and the containing candidate that preserves its information. `[agent]`
- Never deduplicate across the omission boundary: content excluded by `CONTEXT.md` §2 (e.g., full previous-session artifacts) stays excluded even if "redundant" with included content.

## 4. Examples

- The payload references `NO_ASSUMPTIONS.md` via the `[NO_ASSUME]` tag and also pastes the standard's clarification rule inline. The inline paste is redundant (criterion 3): remove it; the tag preserves the information by reference.
- A Knowledge Base entry from a previous session summarizes `executive_summary.md`, and the current phase includes `executive_summary.md` itself. The accumulated entry is redundant (criterion 2): remove it; the discovery entry preserves the information with provenance.
- Two KB entries from different sessions each restate the same project constraint, with identical content. One is kept (the more recent, per `RESOLUTION_TIE_BREAKING.md` §2 criterion 3); the other is removed and logged.
