# DEV Memory Pilot

**Pilot:** Plan 181
**Branch:** `refactor`
**Status:** closed — REJECT; retained as experimental evidence, non-authoritative
**Created:** 2026-10-29

## Purpose

This file was the experimental **active retrieval surface** for durable DEV knowledge extracted from the comparative architecture study. The retrieval hypothesis was tested and rejected on 2026-10-31.

It is not a registry, source of authority, replacement for the individual studies, or implementation of Protocol Memory.

The source artifacts remain authoritative for what they actually state.

## Pilot closure

The controlled agent experiment on 2026-10-31 executed 12 paired questions with a real DeepSeek agent. The pilot was discovered in 11/12 treatment runs, but treatment increased file-open events by 20.0%, searches by 22.7%, historical source consultations by 29.9%, and elapsed time by 6.1%; total tokens changed by only -0.5%. The pre-registered decision is **REJECT**.

This file therefore must not be treated as a recommended retrieval layer. In particular, `DEV-MEM-004` is superseded by the controlled result: a compact active surface plus on-demand history was plausible before measurement but did not reduce retrieval work in the tested configuration.

The entries below are retained as experimental evidence and historical learning, not as an active retrieval contract.

## Retrieval contract

Use an entry when its scope matches the question.

If a claim is material, surprising, contested, or implementation-sensitive, rehydrate the cited source before treating it as verified.

Historical source artifacts remain necessary for detailed rationale and evidence.

## Memory entries

### DEV-MEM-001 — Execution continuity is a distinct runtime concern
- **Type:** lesson
- **Claim:** External comparisons consistently expose explicit mechanisms for long-running execution: state, persistence, checkpointing, interruption, resume or run/step continuity. ARgentOS should investigate these as runtime concerns without merging them into Change Lifecycle.
- **Applicable when:** evaluating long-running or resumable DEV execution.
- **Not applicable when:** discussing Protocol lifecycle semantics or generic architectural state.
- **Epistemic state:** inferred
- **Lifecycle:** active
- **Observed:** 2026-10-29
- **Evidence:** `REFACTOR_LANGGRAPH.md`, `REFACTOR_MICROSOFT_AGENT_FRAMEWORK.md`, `REFACTOR_CREWAI.md`, `REFACTOR_LETTA.md`
- **Decision impact:** investigate execution continuity; reject a universal State Model.

### DEV-MEM-002 — Small primitives are safer than a universal ontology
- **Type:** lesson
- **Claim:** The comparisons reinforce that narrow runtime primitives can solve concrete orchestration problems without requiring a universal Unit/Relationship/State ontology.
- **Applicable when:** considering new architectural abstractions or registries.
- **Not applicable when:** a concrete measured problem already requires a durable semantic representation.
- **Epistemic state:** inferred
- **Lifecycle:** active
- **Observed:** 2026-10-29
- **Evidence:** `REFACTOR_OPENAI_AGENTS_SDK.md`, `REFACTOR_MICROSOFT_AGENT_FRAMEWORK.md`, `REFACTOR_MATRIX.md`, `REFACTOR_SYNTHESIS.md`
- **Decision impact:** require a measurable problem before adding cross-cutting architecture machinery.

### DEV-MEM-003 — Runtime memory is not DEV Memory
- **Type:** constraint
- **Claim:** Runtime/session memory, Protocol Memory and DEV Memory solve different problems and must not silently become one authority or storage model.
- **Applicable when:** designing memory, session, context, persistence or knowledge features.
- **Not applicable when:** none identified; the distinction is currently foundational.
- **Epistemic state:** inferred
- **Lifecycle:** active
- **Observed:** 2026-10-29
- **Evidence:** `REFACTOR_CREWAI.md`, `REFACTOR_OPENHANDS.md`, `REFACTOR_LETTA.md`, `protocol/.agents/standards/context/MEMORY_SYSTEM.md`
- **Decision impact:** keep DEV Memory separate from Protocol Memory and runtime continuity.

### DEV-MEM-004 — Two-tier retrieval is a promising DEV Memory pattern
- **Type:** lesson
- **Claim:** A compact active knowledge surface plus on-demand supporting history is a plausible way to reduce context/retrieval cost while preserving detailed provenance.
- **Applicable when:** designing retrieval for durable DEV knowledge.
- **Not applicable when:** the active surface would become authoritative or the supporting evidence cannot be rehydrated.
- **Epistemic state:** inferred
- **Lifecycle:** superseded by controlled test on 2026-10-31
- **Observed:** 2026-10-29
- **Evidence:** `REFACTOR_OPENHANDS.md`, `REFACTOR_LETTA.md`, `DEV_MEMORY_CONTROLLED_RESULT.md`
- **Decision impact:** test compact-memory-first retrieval before considering a larger memory system.

### DEV-MEM-009 — Retrieval-surface pilot was rejected
- **Type:** negative knowledge
- **Claim:** Making a compact, provenance-backed DEV Memory surface available and discoverable did not reduce retrieval work in the controlled 2026-10-31 test. It increased file-open events, searches, historical source consultations and elapsed time, while total tokens were effectively flat.
- **Applicable when:** evaluating whether DEV Memory should be introduced primarily as a parallel retrieval/navigation layer.
- **Not applicable when:** evaluating a materially different Memory purpose or treatment, such as decision continuity or an explicitly instructed workflow; those require separate evidence.
- **Epistemic state:** verified for the tested configuration
- **Lifecycle:** active as negative knowledge
- **Observed:** 2026-10-31
- **Evidence:** `DEV_MEMORY_CONTROLLED_RESULT.md`, `docs/working/audits/dev-memory-controlled-2026-10-31/evidence/analysis.json`
- **Decision impact:** do not expand this retrieval architecture; any future DEV Memory proposal must state a distinct measurable value proposition.

### DEV-MEM-005 — Memory consolidation needs stronger governance than similarity
- **Type:** constraint
- **Claim:** Semantic similarity alone is insufficient to safely merge/delete DEV knowledge because provenance, applicability, negative knowledge and supersession can be lost.
- **Applicable when:** evaluating consolidation, deduplication or automatic compaction.
- **Not applicable when:** a human explicitly performs a governed consolidation with preserved evidence.
- **Epistemic state:** inferred
- **Lifecycle:** active
- **Observed:** 2026-10-29
- **Evidence:** `REFACTOR_CREWAI.md`
- **Decision impact:** no automatic deletion in the pilot; provenance and semantic non-regression remain mandatory.

### DEV-MEM-006 — ACI is an independent optimization surface
- **Type:** lesson
- **Claim:** Agent-facing tool semantics, bounded observations and validation feedback can materially affect coding-agent performance and should be evaluated independently from general runtime architecture.
- **Applicable when:** improving AgentWorker's interaction with code/workspace tools.
- **Not applicable when:** designing governance authority or lifecycle semantics.
- **Epistemic state:** inferred
- **Lifecycle:** active
- **Observed:** 2026-10-29
- **Evidence:** `REFACTOR_SWE_AGENT.md`
- **Decision impact:** consider a separate ACI experiment after the DEV Memory pilot.

### DEV-MEM-007 — Evaluation and lifecycle verification are different
- **Type:** constraint
- **Claim:** Behavioral evaluation scenarios, implementation tests and Change Lifecycle verification answer different questions and should not be collapsed into one generic verification mechanism.
- **Applicable when:** designing evaluation or verification loops.
- **Not applicable when:** a simple deterministic unit test fully answers the question.
- **Epistemic state:** inferred
- **Lifecycle:** active
- **Observed:** 2026-10-29
- **Evidence:** `REFACTOR_GOOGLE_ADK.md`, `REFACTOR_SYNTHESIS.md`
- **Decision impact:** future evaluation work should complement, not replace, existing lifecycle verification.

### DEV-MEM-008 — Runtime evidence is not automatically authority
- **Type:** invariant
- **Claim:** Traces/events can provide evidence for a claim but do not automatically establish authorization, correctness or lifecycle closure.
- **Applicable when:** designing observability, runtime events or evidence ingestion.
- **Not applicable when:** an explicit authoritative artifact independently establishes the relevant fact.
- **Epistemic state:** inferred
- **Lifecycle:** active
- **Observed:** 2026-10-29
- **Evidence:** `REFACTOR_OPENAI_AGENTS_SDK.md`, `REFACTOR_OPENHANDS.md`, `REFACTOR_GOOGLE_ADK.md`, `REFACTOR_SYNTHESIS.md`
- **Decision impact:** preserve authority boundaries when introducing runtime observability.

## Pilot invariants
1. Every entry has source provenance.
2. Every entry declares applicability.
3. `inferred` remains distinct from `verified`.
4. Memory does not create authority.
5. Memory can require source rehydration.
6. No entry is deleted during this pilot.
7. Contradictory knowledge is not silently merged.
8. The corpus is intentionally small.

## What is deliberately absent
- embeddings;
- vector database;
- automatic consolidation;
- automatic deletion;
- global graph;
- universal Memory API;
- Protocol payload changes;
- runtime integration;
