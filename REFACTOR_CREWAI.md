# ARgentOS Refactor Study — CrewAI

**Study date:** 2026-10-29
**Decision:** ADAPT

## Scope
Compare CrewAI's Agents/Crews/Flows composition, unified Memory, persistence/resume, scopes, consolidation and observability with ARgentOS.

## Evidence
Current CrewAI documentation presents Agents, Crews and Flows as core concepts. Flows provide explicit start/listen/router-style execution and persistent state/resume. CrewAI's current unified Memory supports scopes, slices, semantic/recency/importance ranking, memory extraction and consolidation; memories can be shared or private by scope.

Sources:
- https://github.com/crewAIInc/crewAI/blob/main/docs/v1.15.1/en/index.mdx
- https://github.com/crewAIInc/crewAI/blob/main/docs/v1.12.1/en/concepts/memory.mdx

## 1. Architecture
CrewAI separates collaborative agent groups (Crews) from deterministic/event-oriented execution (Flows). That distinction is useful: not every orchestration problem is an agent-to-agent collaboration problem.

ARgentOS similarly distinguishes Orchestrator/Worker execution from optional adversarial deliberation.

**Finding:** preserve the distinction between execution orchestration and multi-agent deliberation.

## 2. Flows
Flows provide explicit lifecycle hooks, routing and state, with persistence and resume for longer-running executions.

This overlaps with the LangGraph finding: execution continuity benefits from an explicit runtime composition model.

**Decision:** ADAPT selectively; do not introduce a universal Flow abstraction into governance.

## 3. Memory
CrewAI's unified Memory is particularly relevant to Priority 4. It can infer scope/categories/importance, extract atomic memories, recall using composite scoring and consolidate similar records. It supports hierarchical scopes and read-only slices.

This is a materially stronger implementation pattern than simple append-only history.

However, CrewAI's memory is agent runtime memory. ARgentOS DEV Memory has a stronger governance/provenance requirement.

Useful principles:
- atomic knowledge units;
- hierarchical scope;
- read-only views;
- relevance ranking;
- deduplication/consolidation;
- explicit stale/superseded handling.

**Decision:** ADAPT the retrieval/maintenance principles; do not copy the unified Memory API.

## 4. Memory consolidation
CrewAI automatically compares new memory against existing records and can keep, update, delete or insert based on similarity and LLM judgment. This directly addresses memory growth.

This is highly relevant to the ARgentOS compaction problem, but it exposes a governance risk: automatic deletion based on semantic similarity can erase negative knowledge or provenance if the policy is too weak.

ARgentOS should therefore require provenance and supersession semantics before any automated deletion/consolidation.

**Decision:** ADAPT consolidation as a future experiment, with stronger provenance constraints.

## 5. What ARgentOS does better
- Durable knowledge is explicitly tied to evidence/provenance and future reuse.
- Negative knowledge and rejected approaches are first-class conceptual concerns.
- Memory must not become a second authority source.
- Change Lifecycle provides stronger closure semantics.

## 6. What CrewAI does better
- Easy runtime memory access.
- Hierarchical memory scopes.
- Atomic memory extraction.
- Composite relevance scoring.
- Automated consolidation/deduplication.
- Explicit Flow execution model.

## 7. Architectural lesson
CrewAI provides a strong example of **operational memory as an active subsystem**, not a passive log.

ARgentOS should consider retrieval and maintenance behavior, not only a storage schema.

## 8. Proposed adaptations
### ADAPT-1 — Scoped DEV Memory
Investigate project/subject scopes so future memory retrieval can be bounded instead of searching all historical knowledge.

### ADAPT-2 — Atomic knowledge extraction
Capture one reusable conclusion per memory item where possible.

### ADAPT-3 — Consolidation
Experiment with duplicate/contradiction detection, but require provenance, applicability and supersession handling.

### ADAPT-4 — Read-only memory views
Allow an agent/session to consume relevant DEV knowledge without implicitly acquiring authority to mutate it.

## 9. Reject
- Automatic memory deletion based only on semantic similarity.
- Treating runtime agent memory as equivalent to DEV Memory.
- Universal hierarchical scope taxonomy before retrieval needs are measured.
- Making memory authoritative over RFC/ADR/Plan/Git sources.

## 10. Experiment
Build a small DEV Memory pilot from 5–10 durable conclusions. Compare flat retrieval against scoped + relevance-ranked retrieval and measure rediscovery time, stale retrieval and scope errors.

## Final decision
**ADAPT** — CrewAI is a strong reference for operational memory retrieval and maintenance. Its most valuable contribution to ARgentOS is not the unified API but the idea that useful memory requires scope, ranking, atomic extraction and active consolidation.
