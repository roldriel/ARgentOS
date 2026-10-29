# DEV Memory Experiment — Initial Retrieval Benchmark

**Plan:** 181
**Branch:** `refactor`
**Date:** 2026-10-29
**Status:** initial pilot result

## 1. Experimental question

Does a small, provenance-backed DEV Memory surface reduce historical retrieval work for recurring architecture questions while preserving scope and authority boundaries?

## 2. Test corpus

The treatment corpus contains 8 entries in `DEV_MEMORY_PILOT.md`, extracted from the 8 comparative studies in Plan 180.

The corpus is intentionally small. This is a retrieval experiment, not a production memory implementation.

## 3. Questions

| ID | Question | Primary knowledge needed |
|---|---|---|
| Q1 | What should ARgentOS learn from durable execution systems? | DEV-MEM-001 |
| Q2 | Why are we rejecting a universal architecture ontology? | DEV-MEM-002 |
| Q3 | What memory boundaries must remain separate? | DEV-MEM-003 |
| Q4 | What memory retrieval pattern should we test? | DEV-MEM-004 |
| Q5 | Why should memory consolidation not use similarity alone? | DEV-MEM-005 |
| Q6 | What is the next likely experiment after Memory? | DEV-MEM-006 |
| Q7 | How should evaluation relate to lifecycle verification? | DEV-MEM-007 |
| Q8 | Can runtime traces become authority? | DEV-MEM-008 |
| Q9 | Which conclusions came from multiple systems rather than one? | 001, 002, 003, 004, 007, 008 |
| Q10 | What should we explicitly not build yet? | 002, 003, 005, 008 |

## 4. Baseline vs treatment

### Baseline A — direct historical retrieval

An agent starts without the pilot memory and must recover answers from the individual comparison artifacts and relevant Protocol context.

For Q1–Q8, the direct route requires locating and opening at least one source artifact per question. Q9 and Q10 require cross-document synthesis.

### Treatment B — DEV Memory first

An agent reads `DEV_MEMORY_PILOT.md` first. Q1–Q8 have a direct candidate entry. Q9–Q10 use the cited entries to identify the minimum source set and then rehydrate evidence where needed.

## 5. Structural retrieval result

| Metric | Baseline A | Treatment B | Interpretation |
|---|---:|---:|---|
| Primary retrieval surface | 8 individual studies + Protocol context as needed | 1 compact pilot file | Treatment reduces initial navigation surface |
| Direct coverage for Q1–Q8 | source-dependent | 8/8 memory entries | Memory gives immediate candidate answers |
| Cross-document synthesis for Q9 | required | bounded to cited entries | Memory narrows search scope |
| Cross-document synthesis for Q10 | required | bounded to cited entries | Memory narrows search scope |
| Source rehydration | required for detailed verification | still required for material claims | Memory does not replace evidence |
| Authority transfer | possible failure mode | explicitly prohibited by pilot contract | Treatment adds a guardrail |

## 6. What this does and does not demonstrate

### Demonstrated at pilot level
- A small memory surface can encode recurring conclusions from the comparative study.
- Each entry can retain explicit provenance and applicability.
- Retrieval can begin from durable conclusions instead of reopening every study.
- The memory surface can direct rehydration instead of pretending to be evidence.

### Not demonstrated
- Real wall-clock time reduction.
- Token reduction under a controlled agent benchmark.
- Long-term memory freshness.
- Contradiction handling at scale.
- Maintenance cost over multiple refactor cycles.
- Whether 8 entries remain optimal as the repository evolves.
- Whether the approach improves decision quality rather than only navigation.

These require a larger and controlled experiment.

## 7. Initial observations

### O-01 — Retrieval compression looks promising
The pilot collapses 8 separate comparison artifacts into one small retrieval surface without copying their full content.

### O-02 — Provenance is necessary
The memory entries are useful precisely because they point back to the source studies. Removing those references would turn a navigation aid into an unsupported assertion store.

### O-03 — Applicability is not optional
Several lessons are only safe under a specific question. For example, execution continuity concerns apply to runtime execution and do not redefine Change Lifecycle state.

### O-04 — Memory must remain subordinate to evidence
The pilot explicitly requires rehydration for material or implementation-sensitive claims. This preserves the distinction between useful knowledge and authority.

### O-05 — The pilot is already exposing a maintenance question
Several entries are derived from multiple studies. As the comparison corpus grows, explicit relations between entries and their evidence will become important to avoid duplicate or contradictory knowledge.

## 8. Preliminary conclusion

**PILOT SIGNAL: POSITIVE, NOT YET VALIDATED.**

The experiment provides enough evidence to continue the DEV Memory investigation, but not enough to justify a production Memory subsystem.

The strongest result is not a storage design. It is the retrieval pattern:

```
compact durable conclusion
        ↓
scope / applicability
        ↓
source provenance
        ↓
rehydrate evidence when required
```

## 9. Next measurement

Expand the pilot from 8 to approximately 20–30 durable conclusions drawn from existing Plans/ADRs/RFCs and completed experiments, while keeping the same retrieval contract.

Then run a blinded New-Agent Test with:
- the current repository only;
- repository + DEV Memory pilot;
- identical questions and acceptance rubric.

Measure:
- files opened;
- searches performed;
- context consumed where measurable;
- time to correct answer;
- unsupported claims;
- scope errors;
- stale conclusions;
- evidence rehydration rate;
- maintenance operations required.

Do not implement automatic consolidation or deletion before this measurement.

## 10. Decision

**CONTINUE EXPERIMENT — DO NOT PRODUCTIZE YET.**

The pilot supports Priority 4 as a real engineering problem and supports the two-tier retrieval hypothesis observed in the comparative study. It does not yet establish the final DEV Memory data model.
