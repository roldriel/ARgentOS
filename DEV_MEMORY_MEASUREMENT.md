# DEV Memory Measurement — Structural Benchmark

**Plan:** 181  
**Branch:** refactor  
**Date:** 2026-10-29

## Result

The controlled repository-side benchmark compares direct historical retrieval against the 8-entry DEV Memory pilot.

This is a structural measurement, not an independent-agent timing benchmark.

## Test

24 benchmark questions were evaluated against the pilot corpus.

### Condition A — direct retrieval

Each question starts from the comparative study material and must locate the relevant conclusion in source documents.

### Condition B — DEV Memory first

Each question starts from the compact DEV Memory surface. Source material is consulted only when the conclusion needs verification or additional detail.

## Measured structural effects

| Metric | Direct retrieval | DEV Memory first |
|---|---:|---:|
| Initial knowledge surface | 8 study files | 1 memory file |
| Questions with an immediate mapped conclusion | 0/24 | 24/24 |
| Questions requiring cross-source synthesis | 8/24 | 4/24 |
| Evidence rehydration needed for material claims | yes | yes |
| Memory authority | none | none |
| Provenance available | source documents | memory entry -> source document |

### Retrieval-surface reduction

Initial navigation surface changes from **8 study documents to 1 compact memory document**, an **87.5% reduction in initial document surface**.

This is a structural result. It is not an 87.5% claim about time, tokens or cost.

### Synthesis reduction

The benchmark questions were designed so that the direct condition needs cross-document synthesis for 8 questions. With the memory-first condition, 4 questions still require source synthesis because they deliberately combine multiple knowledge entries or ask for a broader conclusion.

This is a **50% reduction in questions requiring initial cross-source synthesis** under the benchmark design.

## Accuracy and authority checks

The treatment was required to preserve:

- provenance;
- applicability;
- distinction between inference and verification;
- source rehydration for material claims;
- no transfer of authority to Memory.

No unsupported authority transfer was introduced by the pilot design.

## What was not measured

The current tooling does not provide a second independent agent with controlled instrumentation for:

- wall-clock time;
- token consumption;
- search count;
- files opened by the independent agent;
- decision quality under blinded conditions.

Therefore those metrics are explicitly **UNMEASURED**, not estimated.

## Interpretation

The experiment now has a positive structural signal:

1. A compact memory surface substantially reduces initial navigation breadth.
2. The memory surface provides a direct candidate conclusion for all benchmark questions.
3. Provenance preserves the ability to rehydrate source evidence.
4. Memory does not remove the need for evidence.
5. The benefit is retrieval compression, not authority substitution.

## Decision

**CONTINUE — EXPAND TO CONTROLLED AGENT TEST.**

The current result is sufficient to justify a second-stage test with an independently instrumented agent, but not sufficient to productize DEV Memory or choose a final storage/data model.

The next test should compare the two conditions with identical questions and record actual search operations, files opened, context consumption, time, unsupported claims, scope errors and evidence rehydration.
