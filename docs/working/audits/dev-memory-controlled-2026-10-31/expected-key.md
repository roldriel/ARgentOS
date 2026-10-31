# Expected-answer key — controlled DEV Memory experiment (plan 181)

**Class:** Working / Audit — non-normative evidence for grading, not authority.
**Derived from commit:** `a5f97c163b56b82dc8fadd4e3f65646899e9c245` (prepared ground-truth tree).
**Generated:** 2026-10-31 (local, `-03:00`).
**Companion artifact:** `expected-key.json` (the machine-readable key, Q01–Q12).

## Method

1. Claimed shared `task-1`, then read **only** the prepared workspace `C:\Users\rolda\AppData\Local\ARgentOS-dev-memory-2026-10-31\groundtruth` (a working tree of the commit above **without `.git`**, with `DEV_MEMORY_PILOT.md` and all experiment meta-documents removed). The real repository working tree was **not** read as evidence; it was used only as the write destination for these two files.
2. Read the eight individual comparative studies, then the two secondary summaries, and applied the stated precedence rule: **the individual study governs** where a summary conflicts. Then cross-checked against the historical artifacts the studies cite (`docs/plans/180-comparative-architecture-refactor-study.md`, `docs/plans/INDEX.md`, `docs/rfc/80-memory-system.md` via `docs/rfc/INDEX.md`, `docs/plans/150-memory-system-implementation.md` header, `protocol/.agents/standards/context/MEMORY_SYSTEM.md`, `ROADMAP.md`) to separate what the study concluded from what the repository had recorded or implemented.
3. For each of the 12 fixed questions (verbatim, not reworded) I recorded the conclusion the sources support, the scope where it applies and must not be generalized, the files that actually state it, the over-claims the sources do not support, and an explicit uncertainty note.
4. Cross-check performed: every `supporting_sources` entry was opened (or, for `docs/plans/INDEX.md`, read in the plan-180 section) in the prepared workspace. No conclusion is drawn from `DEV_MEMORY_PILOT.md`, from the real-repository experiment materials, or from a question's framing.

## Files read

Primary evidence surface (all read in full):

- `REFACTOR_LANGGRAPH.md`
- `REFACTOR_OPENAI_AGENTS_SDK.md`
- `REFACTOR_MICROSOFT_AGENT_FRAMEWORK.md`
- `REFACTOR_GOOGLE_ADK.md`
- `REFACTOR_CREWAI.md`
- `REFACTOR_OPENHANDS.md`
- `REFACTOR_SWE_AGENT.md`
- `REFACTOR_LETTA.md`
- `REFACTOR_SYNTHESIS.md` (secondary summary, cross-check only)
- `REFACTOR_MATRIX.md` (secondary summary, cross-check only)

Corroborating repository artifacts (read where a question needed them):

- `docs/plans/180-comparative-architecture-refactor-study.md` (full)
- `docs/plans/INDEX.md` (plan-180 section, lines 1–40)
- `protocol/.agents/standards/context/MEMORY_SYSTEM.md` (full; corroboration for Q05 and the DEV/Protocol Memory distinction)
- `docs/rfc/INDEX.md` (RFC-80 row only, to confirm the Memory System is the adopter/project-scoped Protocol Memory)
- `docs/plans/150-memory-system-implementation.md` (lines 1–60 only; confirmation of RFC-80 scope)
- `ROADMAP.md` (full; confirms it records **no** initiative derived from the comparative study — it was last updated 2026-10-14)

Directories inspected (names only): ground-truth root, `docs/`, `docs/plans/`, `docs/rfc/`, `docs/working/audits/`, `protocol/.agents/standards/context/`, `runtime/memory/`, `sessions/`.

## Evidence posture per question

| Q | Strength in the historical corpus |
|---|---|
| Q01 | Strong and explicit (separation stated in LangGraph, Synthesis, Matrix, and the Microsoft reject list). |
| Q02 | Strong: the negative result is called the study's most important one. |
| Q03 | Strong on the distinction; the corpus defines what DEV Memory is *not* more sharply than what it is. |
| Q04 | Plausibility supported (OpenHands/Letta/Synthesis), effectiveness **not** demonstrated — a pilot is proposed. |
| Q05 | Strong and explicit rejection (CrewAI §4/Reject; Matrix Reject; Synthesis guardrail 8). |
| Q06 | Strong on the ACI surface; an abstraction is explicitly withheld until measured. |
| Q07 | Strong: three-layer distinction plus the ADK "eval scores as lifecycle authority" reject. |
| Q08 | Strong: repeated invariant across four studies and both summaries. |
| Q09 | Strong comparative convergence for an **investigation**; benefit unmeasured. |
| Q10 | Convergence evidence (OpenHands two-tier, Letta active-vs-historical, CrewAI scoped retrieval), analogical rather than controlled. |
| Q11 | Direction explicit (guardrail 10 and §14); each adaptation remains a hypothesis plus experiment. |
| Q12 | Recorded conclusion explicit; its **procedural** status is partial — see ambiguities. |

## Genuinely ambiguous points

1. **Q12 — "current architectural decision" has two readings.** The synthesis/matrix record a clear decision (*KEEP + ADAPT selectively + EXPERIMENT before institutionalizing*, no broad rewrite, DEV Memory first). But the procedural record is weaker: `docs/plans/180-…md` is still `**Status:** Aprobado para ejecución` with entry/exit criteria unchecked and Validation/Checkpoint sections pending, and `docs/plans/INDEX.md` lists it as `Aprobado para ejecución` / active. Plan 180 also says derived architectural changes must wait for separate, explicitly authorized changes. So the key states the recorded decision while flagging that **no adoption, closure or implementation is recorded** in this tree. A grader should not treat the study as an authorization.
2. **Q04 vs Q10 overlap.** Both concern two-tier DEV Memory. Q04 asks whether the pattern is plausible (verdict: plausible to pilot) while Q10 asks what evidence supports it (comparative convergence plus a proposed 5–10 entry experiment). The corpus never validates two-tier retrieval *inside* ARgentOS, so any answer asserting measured benefit is unsupported; the key splits verdict from evidence deliberately.
3. **"Priority 4" is an external, unversioned pointer.** Several studies frame DEV Memory as "Priority 4", but the maintainer's `PRIORITY.md` is an untracked local input, absent from the prepared workspace and repeatedly declared non-citable in repository governance. The key therefore restates only how the studies describe Priority 4's objective (reduce rediscovery, compact transient work) and invents nothing from that missing file.
4. **DEV Memory scope is inferred, not specified.** No historical artifact defines the DEV Memory schema or its owner. The only implemented Memory System in the tree is RFC-80 / plan 150's project-scoped Protocol Memory (adopting project's episodic/semantic knowledge). The key's Q03 distinguishes DEV Memory from it on the strength of the comparative studies plus the RFC-80 scope, and says so.
5. **Q09 scope of "checkpoint" vs "lifecycle checkpoint".** ARgentOS already has lifecycle *Git checkpoints* (RFC-75 closure), which are unrelated to LangGraph-style runtime checkpoints. The key keeps them separate (Q01 expected_scope) to prevent a name collision in grading; the corpus itself only ever discusses runtime checkpoints in this context.
6. **Composite dating.** All eight studies and both summaries are dated 2026-10-29; `docs/plans/INDEX.md` reports repository state "al 2026-10-25" and `ROADMAP.md` "última actualización: 2026-10-14". There is a small documentary drift window between the study date and the rest of the tree, so "current" in Q12 is anchored to the commit under analysis, not to wall-clock time.

## Constraints respected

- Read-only on the ground-truth workspace; the real repository was not read.
- Wrote exactly two files, both under `docs/working/audits/dev-memory-controlled-2026-10-31/`; no code, docs, or git state was modified.
- No commit, no release, no payload change. `DEV_MEMORY_PILOT.md` never opened.
