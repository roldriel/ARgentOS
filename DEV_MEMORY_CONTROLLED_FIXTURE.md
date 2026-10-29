# DEV Memory — Controlled Test Fixture

**Plan:** 181  
**Branch:** `refactor`  
**Date:** 2026-10-29  
**Status:** fixture definition

## Purpose

This fixture freezes the evaluation target for the next controlled DEV Memory test.

The fixture deliberately separates **retrieval efficiency** from **answer correctness**. A memory-first result is useful only if it reduces discovery work without increasing unsupported claims, scope errors, provenance failures, or authority mistakes.

## Conditions

### Control

The agent receives the repository state with the DEV Memory pilot hidden from retrieval.

It may use the comparative study artifacts and their synthesis/matrix.

### Treatment

The agent receives the same repository state plus `DEV_MEMORY_PILOT.md`.

The agent is instructed to use Memory as a retrieval aid, not as authority, and to rehydrate cited sources when required.

## Questions

| ID | Question | Expected evidence family |
|---|---|---|
| Q01 | Should runtime execution continuity remain separate from Change Lifecycle? | LangGraph / Microsoft / CrewAI / Letta |
| Q02 | Does the comparative study justify a universal Unit/Relationship/State ontology? | OpenAI SDK / Microsoft / synthesis |
| Q03 | Is runtime memory the same problem as DEV Memory? | CrewAI / OpenHands / Letta / Protocol Memory |
| Q04 | Is two-tier retrieval a plausible DEV Memory pattern? | OpenHands / Letta |
| Q05 | Is semantic similarity sufficient for automatic Memory deletion? | CrewAI |
| Q06 | Is Agent-Computer Interface design an independent optimization surface? | SWE-agent |
| Q07 | Are behavioral evaluation and lifecycle verification interchangeable? | Google ADK / synthesis |
| Q08 | Do runtime traces establish authority or lifecycle closure? | OpenAI SDK / OpenHands / Google ADK |
| Q09 | What evidence supports explicit checkpoint/resume investigation? | LangGraph / Microsoft / CrewAI / Letta |
| Q10 | What evidence supports two-tier DEV Memory? | OpenHands / Letta |
| Q11 | What should ARgentOS adapt without copying external architectures? | synthesis / matrix |
| Q12 | What is the current architectural decision after the comparative study? | synthesis / matrix |

## Scoring

Each answer receives binary checks:

- **Correct conclusion**
- **Correct scope**
- **Provenance present**
- **Authority boundary preserved**
- **No unsupported claim**

A separate efficiency record captures:

- files opened;
- searches issued;
- source artifacts rehydrated;
- context consumed, if available;
- wall-clock time, if available.

### Primary outcome

The treatment is successful only if it reduces retrieval work while preserving correctness.

A reduction in files/searches with worse epistemic quality is a **failure**, not an improvement.

## Required reporting

The eventual result must distinguish:

1. measured observations;
2. derived metrics;
3. qualitative judgments;
4. unmeasured dimensions.

No estimate should be reported as measurement.

## Current limitation

This repository fixture does not itself provide an independent agent runtime or controlled timing instrumentation. Until such a runner exists, any repository-side replay remains a structural proxy and must be labeled accordingly.

## Falsification

Reject the current DEV Memory approach if the controlled test shows any of the following:

- no meaningful retrieval reduction;
- worse correctness;
- more scope errors;
- more unsupported claims;
- provenance loss;
- authority transfer from Memory;
- maintenance cost that outweighs retrieval benefit.

A negative result should cause redesign or abandonment, not expansion of Memory infrastructure.
