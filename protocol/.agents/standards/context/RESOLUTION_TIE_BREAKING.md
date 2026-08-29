# Resolution Policy — Tie-Breaking

This policy defines the concrete criteria for deciding between **equivalent context candidates** when the Orchestrator assembles a worker payload. It is one of the Resolution policies of `.agents/standards/context/`; the concept it operationalizes — Context Resolution, the transformation of a prioritized set of context candidates into a consistent set that can be composed into the payload — is defined inline here and needs no external reference.

## 1. Concept

A **priority tie** occurs when two or more context candidates are judged equivalent in relevance for the current task and the payload cannot carry all of them (because they compete for the same slot of a budget, or because including both would violate the omission rules of `CONTEXT.md` §2). Tie-breaking decides which candidate stays, without changing the priority of any other candidate.

**Evaluation audience:** every criterion in this policy is `[agent]` — evaluated by agent judgment when the Orchestrator assembles the payload. No tie-break criterion is currently machine-verifiable, because equivalence of relevance is a judgment call. Any future deterministic rule (e.g., comparing declared timestamps of KB entries) would be a harness Future Extension, not part of this policy.

## 2. Criteria, in order of application

Apply the criteria top-down; the first criterion that discriminates decides.

1. **Explicit user directive.** A candidate the user explicitly requested (in the current request or a session clarification) prevails over any candidate that was merely inferred as relevant.
2. **Source precedence.** A candidate from a more authoritative source prevails:
   - current-session artifacts (task specification, artifacts of the current iteration) >
   - protocol standards (`.agents/standards/`) >
   - discovery Knowledge Base entries (`.project/knowledge/discovery/`, with
     freshness) >
   - accumulated Knowledge Base entries from previous sessions
     (`.project/knowledge/entries/`, summaries only) >
   - any other external source.
3. **Recency.** Between candidates from the same source tier, the one produced or confirmed more recently prevails (a stale summary loses to a fresh artifact).
4. **Coverage.** If still tied, the candidate that strictly covers more of the task's acceptance criteria prevails.
5. **First-fit.** If no criterion discriminates, keep the first candidate in assembly order and record the tie. Do not treat an arbitrary-but-logged decision as a conflict.

## 3. Obligations

- Every tie decided by criteria 1–4 is recorded in `SESSION_LOG.md` with the discarded candidate and the criterion applied. `[agent]`
- A tie decided by criterion 5 is recorded as a tie with "no discriminating criterion". `[agent]`
- Tie-breaking never re-decides priorities: it only selects among candidates already judged equivalent. If the candidates are not actually equivalent, the error is in the relevance assessment, not in this policy — re-assess relevance instead of forcing a tie-break.
- If the tied candidates are mutually exclusive alternatives (not equivalent relevance, but alternative answers to the same question), this policy does not apply: that situation belongs to `RESOLUTION_UNRESOLVABLE_CONFLICTS.md`.

## 4. Examples

- Two KB entries summarize the same previous session's findings; only the payload budget for one remains. Criterion 3: the more recent entry stays.
- A KB entry and the current `SESSION_BRIEF.md` both cover an open unknown. Criterion 2: `SESSION_BRIEF.md` (current-session artifact) prevails; the KB entry is referenced or omitted.
- The user wrote "keep using the naming rule from ARCHITECTURE_CONTRACT", and a KB note suggests a different convention. Criterion 1: the explicit directive wins.
