# ARgentOS Refactor — Final Comparative Matrix

**Branch:** `refactor`
**Date:** 2026-10-29
**Scope:** comparative architecture study against eight external systems.

| System | Strongest external lesson | Where ARgentOS is stronger | Candidate adaptation | Decision | Priority |
|---|---|---|---|---|---|
| LangGraph | Explicit execution topology + durable checkpoint/resume | Governance, authority and lifecycle closure | Execution continuity, checkpoint/resume, idempotency; keep runtime state separate from Change Lifecycle | ADAPT | P1 |
| OpenAI Agents SDK | Small primitive set + explicit delegation/guardrails/tracing | Authority boundary, DEV/Protocol separation | Minimal delegation payload semantics, boundary-local validation, structured runtime tracing | ADAPT | P1 |
| Microsoft Agent Framework | Agent / Workflow / Harness / Middleware / Context composition | Change governance and evidence | Investigate Harness boundary, middleware/interceptors, workflow-vs-agent separation | ADAPT | P1 |
| Google ADK | Integrated build → evaluate → deploy → observe loop | Protocol/DEV/adopter governance separation | Reusable evaluation loop, machine-oriented navigation, artifact/evidence distinction | ADAPT | P1 |
| CrewAI | Scoped operational memory + extraction/ranking/consolidation | Provenance, negative knowledge and authority | Scoped DEV Memory, atomic knowledge, retrieval ranking, guarded consolidation | ADAPT | P1 |
| OpenHands | Coding-agent harness + two-tier persistent memory | Stronger governance/provenance | Compact active Memory index + on-demand evidence; explicit workspace boundary | ADAPT | P1 |
| SWE-agent / mini-SWE-agent | Agent-Computer Interface as an architectural surface | Authorization/effects/lifecycle | ACI review, bounded observations, pre-action checks, runtime history compression | ADAPT | P1 |
| Letta | Persistent identity + active memory vs historical context | Project-level governance and evidence | Active vs historical DEV Memory; bounded memory blocks; run/step evidence hierarchy | ADAPT | P1 |

## Cross-system findings

### 1. Execution is becoming an explicit architectural concern
LangGraph, Microsoft Agent Framework, CrewAI and Letta all expose more explicit runtime concepts for state, workflow, runs, persistence or resume than ARgentOS currently does.

**Implication:** ARgentOS should investigate execution continuity as a runtime concern. This does **not** justify a universal State Model or graph ontology.

### 2. Small primitives outperform universal ontologies
OpenAI Agents SDK and Microsoft Agent Framework are strong evidence that a complex agent system can remain understandable when each primitive has a narrow responsibility.

**Implication:** reject a comprehensive Unit/Relationship/State registry unless a concrete problem requires it.

### 3. Memory is not one thing
CrewAI, OpenHands and Letta independently reinforce distinctions between active context, historical information, scoped memory, runtime continuity and durable knowledge.

**Implication:** ARgentOS should explicitly separate:

```
runtime checkpoint/state
session/history
Protocol Memory
DEV Memory
```

### 4. Agent-facing interfaces matter
SWE-agent demonstrates that tool semantics and feedback formats can materially affect agent performance.

**Implication:** Agent-Computer Interface quality should become an explicit optimization surface for AgentWorker.

### 5. Evaluation should be part of the development loop
Google ADK/Agents CLI provides the clearest external example of evaluation integrated into development rather than treated solely as post-hoc verification.

**Implication:** reusable evaluation scenarios are a plausible ARgentOS improvement, especially for integration continuity and runtime behavior.

### 6. Observability is evidence, not authority
Tracing/event systems appear across the compared systems.

**Implication:** ARgentOS can consume runtime events as evidence, but must not let traces silently become authorization, correctness or lifecycle closure.

## Architectural conclusions

### Preserve
- DEV / Protocol / adopter separation.
- Change Lifecycle authority and existing lifecycle semantics.
- Orchestrator sovereign authority.
- Worker execution boundary and WorkerAdapter.
- Git/documentary provenance.
- Evidence and validation anchors.
- Non-provider-specific architecture.

### Adapt
- Runtime execution continuity.
- Checkpoint/resume semantics where needed.
- Explicit delegation payloads.
- Boundary-local validation/interception.
- Runtime tracing/events.
- Reusable evaluation scenarios.
- Agent-Computer Interface design.
- Scoped, two-tier DEV Memory retrieval.
- Memory consolidation with provenance and contradiction safeguards.

### Reject
- Universal graph architecture.
- Universal State Model.
- Universal Unit superclass.
- Global relationship database.
- Generic lifecycle for every architectural object.
- Runtime trace as authority.
- Agent identity as project identity.
- Automatic conversion of history into Memory.
- Automatic deletion based only on semantic similarity.
- Provider-specific architectural coupling.

## Emerging target architecture

```
                    ARgentOS DEV
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   Governance        Runtime          Knowledge
        │                │                │
 Change Lifecycle   Orchestrator       DEV Memory
 Authority          Worker/Harness     Protocol Memory
 Evidence           Workflow/ACI       Historical evidence
        │                │                │
        └─────────── verification ────────┘
                         │
                    Git / artifacts
```

The comparison does **not** support replacing this with a graph/database/registry-centered architecture.

## Priority ranking after comparison

1. **DEV Memory** — strongest convergence with CrewAI/OpenHands/Letta and directly aligned with Priority 4.
2. **Runtime execution continuity** — strongest convergence with LangGraph/Microsoft/CrewAI/Letta.
3. **Agent-Computer Interface** — directly illuminated by SWE-agent.
4. **Evaluation loop** — strongly supported by Google ADK.
5. **Delegation/interception contracts** — reinforced by OpenAI Agents SDK and Microsoft Agent Framework.
6. **Architectural Index / selective identity** — still useful, but less urgent than runtime/memory work.

## Decision

**The comparative study validates incremental adaptation, not architectural replacement.**

ARgentOS should learn from these systems at the mechanism level while preserving its distinctive governance model.
