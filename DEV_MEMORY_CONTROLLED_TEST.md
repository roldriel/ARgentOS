# DEV Memory — Controlled Retrieval Replay

**Plan:** 181  
**Branch:** `refactor`  
**Date:** 2026-10-29  
**Status:** replay executed; independent-agent validation still pending

## Purpose

This phase tightens the structural benchmark into a fixed, reproducible retrieval replay.

It does **not** claim to be an independent-agent experiment. The current tooling does not provide a second isolated agent with controlled instrumentation, so the result is explicitly a repository-side replay.

## Fixed question set

The benchmark uses 12 questions derived from recurring conclusions in the comparative study:

1. Should runtime execution continuity be modeled separately from Change Lifecycle?
2. Does the comparative study justify a universal Unit/Relationship/State ontology?
3. Is runtime memory the same problem as DEV Memory?
4. Is a compact active-memory surface compatible with source rehydration?
5. Is semantic similarity sufficient for automatic Memory deletion?
6. Is Agent-Computer Interface design an independent optimization surface?
7. Are behavioral evaluation and lifecycle verification interchangeable?
8. Do runtime traces establish authority or lifecycle closure?
9. What evidence supports explicit checkpoint/resume investigation?
10. What evidence supports two-tier DEV Memory?
11. What mechanisms from external systems should be adapted without copying their architecture?
12. What is the current architectural decision after the comparative study?

## Conditions

### A — historical-first

The retrieval surface is the eight comparative study files:

- `REFACTOR_LANGGRAPH.md`
- `REFACTOR_OPENAI_AGENTS_SDK.md`
- `REFACTOR_MICROSOFT_AGENT_FRAMEWORK.md`
- `REFACTOR_GOOGLE_ADK.md`
- `REFACTOR_CREWAI.md`
- `REFACTOR_OPENHANDS.md`
- `REFACTOR_SWE_AGENT.md`
- `REFACTOR_LETTA.md`

The synthesis and matrix are treated as secondary summaries rather than the primary evidence surface.

### B — Memory-first

The first retrieval surface is:

- `DEV_MEMORY_PILOT.md`

The cited source artifact is rehydrated when the answer is material, contested, implementation-sensitive, or requires detail not present in Memory.

## Replay rubric

For each question:

- **Candidate answer available:** whether the first retrieval surface contains a directly usable conclusion.
- **Source rehydration:** whether supporting evidence must be reopened.
- **Cross-source synthesis:** whether multiple source artifacts must be combined.
- **Authority transfer:** whether the retrieval path incorrectly treats Memory as authoritative.
- **Scope error:** whether a conclusion is applied outside its declared applicability.
- **Provenance:** whether the answer can be traced to a source artifact.

## Replay result

| Metric | A: historical-first | B: Memory-first |
|---|---:|---:|
| Initial files required by the benchmark design | 8 | 1 |
| Questions with a direct candidate conclusion | 0/12 | 12/12 |
| Questions requiring cross-source synthesis | 4/12 | 2/12 |
| Evidence rehydration for material claims | required | required |
| Authority transfer permitted | no | no |
| Provenance preserved | yes | yes |

### Derived structural effects

- Initial retrieval surface: **87.5% smaller** (8 files → 1).
- Cross-source synthesis burden: **50% lower** (4/12 → 2/12).
- Candidate-answer coverage: **12/12** in the Memory-first condition.

These are structural retrieval measurements. They are **not** measurements of time, token consumption, cost, or independent-agent decision quality.

## What this replay establishes

1. The current Memory corpus is capable of acting as a compact index of recurring comparative conclusions.
2. The Memory entries preserve explicit applicability and provenance.
3. Source rehydration remains part of the protocol for material claims.
4. The compact surface reduces the amount of historical material that must be considered initially.
5. The pilot does not require Memory to become an authority layer.

## What it does not establish

- independent-agent behavior;
- wall-clock reduction;
- token reduction;
- search-operation reduction by an independent agent;
- maintenance cost over time;
- freshness under repository evolution;
- contradiction resolution at scale;
- optimal Memory corpus size;
- improved final decision quality.

## Decision

**CONTINUE.**

The experiment remains research-only. Do not implement a production DEV Memory system from this result.

## Next falsifiable test

Run the same 12 questions in two isolated retrieval environments:

- **Control:** repository without `DEV_MEMORY_PILOT.md`.
- **Treatment:** repository with `DEV_MEMORY_PILOT.md`.

Instrumentation should record:

1. files opened;
2. search operations;
3. context consumed;
4. source rehydrations;
5. unsupported claims;
6. applicability/scope errors;
7. provenance failures;
8. final-answer quality;
9. wall-clock time.

Acceptance should require a meaningful retrieval reduction **without** worse authority accuracy, provenance, or scope correctness.

Failure of that test should reject or redesign the current Memory approach rather than justify more Memory infrastructure.
