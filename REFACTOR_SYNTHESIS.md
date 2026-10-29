# ARgentOS Refactor — Comparative Synthesis

**Branch:** `refactor`
**Date:** 2026-10-29

## 1. Executive conclusion

The eight comparisons do **not** support a broad architectural rewrite of ARgentOS.

They support a more precise conclusion:

> **ARgentOS has a coherent governance architecture, but several runtime and knowledge mechanisms are less explicit and less mature than comparable agent systems. The correct response is selective adaptation, not replacement.**

The external systems consistently solve adjacent problems by making specific mechanisms explicit: execution topology, durable state, delegation, middleware, evaluation, memory retrieval, agent-computer interaction and runtime observability.

None of the comparisons demonstrated that ARgentOS needs a universal Unit Model, Relationship Model, State Model, Lineage database or filesystem reorganization.

That is the most important negative result of the study.

## 2. What the market comparison actually changed

Before the study, the main architectural hypothesis was that ARgentOS might need a cross-cutting representation layer for capabilities, relationships, state, lineage and knowledge.

The comparisons refine that hypothesis.

### Original broad hypothesis

```
system complexity
      ↓
universal architectural model
      ↓
units + relationships + states + lineage + knowledge
```

### Evidence-supported direction

```
concrete recurring problem
      ↓
small explicit mechanism
      ↓
measured improvement
      ↓
only then institutionalize
```

This is consistent with ARgentOS's existing decision-making compass: clarity and decision quality over accumulation of mechanisms.

## 3. Strongest convergence: Memory

Three systems independently provide useful evidence for Priority 4.

### CrewAI
Shows the value of scoped memory, atomic extraction, relevance ranking and consolidation.

### OpenHands
Shows a practical two-tier model: a small curated durable-memory surface plus deeper historical detail retrieved on demand.

### Letta
Shows the separation between active memory/context and historical information that remains retrievable outside the active context.

Together they support a stronger DEV Memory hypothesis:

```
experience
   ↓
curated knowledge
   ↓
small active retrieval surface
   ↓
on-demand supporting evidence
```

That is highly compatible with Priority 4's objective of reducing rediscovery and compacting transient work.

However, ARgentOS needs stronger governance than a typical runtime memory system:
- provenance;
- applicability;
- contradiction handling;
- supersession;
- negative knowledge;
- authority distinction;
- evidence linkage.

Therefore the external lesson is **retrieval and maintenance behavior**, not a ready-made memory schema.

## 4. Strongest runtime convergence: execution continuity

LangGraph provides the clearest evidence for explicit durable execution.

Microsoft Agent Framework and CrewAI reinforce the same direction through workflow state, checkpointing and resumability.

Letta adds a useful run/step hierarchy.

The common lesson is:

```
long-running execution
       ↓
explicit execution identity
       ↓
state
       ↓
checkpoint / interruption
       ↓
resume / replay
```

ARgentOS currently has strong governance around an execution but less explicit semantics for preserving and resuming runtime execution itself.

That is a legitimate architectural investigation.

It must remain separate from Change Lifecycle.

**Execution state is not lifecycle state.**

## 5. Strongest interface convergence: Agent-Computer Interface

SWE-agent provides the clearest lesson that an agent's tool interface is not merely plumbing.

Tool names, output shape, bounded observations, search behavior, edit validation and feedback semantics directly influence what the agent can reliably accomplish.

This suggests a new question for ARgentOS:

> Is AgentWorker's execution surface optimized for an agent, or merely exposing the capabilities available to the host?

This should be tested empirically.

Possible measures:
- context consumed;
- tool calls;
- invalid edits;
- recovery steps;
- task success;
- time/cost.

No architectural abstraction should be added until this experiment demonstrates a real problem.

## 6. Evaluation becomes more important

Google ADK/Agents CLI provides the strongest evidence for an explicit development loop around evaluation.

ARgentOS already has tests, validation anchors and lifecycle verification, but those mechanisms are not identical to reusable behavioral evaluation scenarios.

A useful future distinction is:

```
unit/integration tests
       ↓
implementation correctness

evaluation scenarios
       ↓
agent behavior / trajectory / outcome

lifecycle verification
       ↓
authorized change closure
```

These should complement each other rather than collapse into one generic verification mechanism.

## 7. Delegation and composition

OpenAI Agents SDK and Microsoft Agent Framework reinforce a second architectural principle:

**boundaries should make transferred responsibility explicit.**

For ARgentOS this means documenting the Orchestrator → Worker boundary in terms of:
- task;
- authority;
- execution context;
- tools/capabilities;
- verification expectations;
- result;
- evidence.

That is more valuable than introducing a generic `depends_on` relationship graph.

Similarly, Microsoft Agent Framework's Agent / Workflow / Harness distinction reinforces that runtime composition and actor identity can remain separate.

## 8. Observability does not become authority

Several compared systems have strong tracing and runtime event systems.

ARgentOS should learn from this, but preserve a critical invariant:

```
event / trace
    ≠
authorization
    ≠
correctness
    ≠
lifecycle closure
```

A trace can be evidence for a claim.
It does not automatically establish the claim.

This principle should remain explicit in any future runtime-event design.

## 9. The Architectural Index hypothesis survives, but its priority falls

The comparisons did not invalidate the Architectural Index idea.

They did, however, reduce its urgency relative to Memory, execution continuity and ACI.

The index remains useful for a narrow question:

> Which enduring architectural subjects exist, and where is their current authority?

It should remain:
- small;
- selected;
- derived-first where possible;
- non-authoritative;
- resistant to becoming a second architecture database.

The market study therefore strengthens the earlier recommendation to avoid a comprehensive registry.

## 10. What the study falsified

The study gives us several explicit negative conclusions.

### Falsified / unsupported
- ARgentOS needs a universal graph model.
- ARgentOS needs a universal state ontology.
- Every architectural concept needs a stable registry entry.
- Every relationship needs to be persisted explicitly.
- A lineage database is required.
- Agent memory should be the same thing as project knowledge.
- Runtime traces can serve as lifecycle authority.
- ARgentOS should adopt a provider-specific runtime architecture.
- Complexity itself justifies more abstraction.

These are important results because they prevent the refactor branch from becoming a mechanism-accumulation branch.

## 11. What is now strongly supported

### Supported direction A — DEV Memory
Priority 4 should proceed as a concrete research/design problem.

### Supported direction B — Runtime continuity
Investigate execution identity, checkpointing, interruption, resume and idempotency.

### Supported direction C — ACI
Experiment with the AgentWorker tool/feedback surface.

### Supported direction D — Evaluation
Experiment with reusable behavioral evaluation scenarios.

### Supported direction E — Delegation contract
Make transferred context/authority/result/evidence semantics more explicit.

## 12. Proposed next experimental sequence

Do **not** implement all five simultaneously.

### Experiment 1 — DEV Memory
Small corpus of 5–10 durable conclusions.

Compare:
1. direct search through historical artifacts;
2. compact active-memory index + supporting evidence.

Measure rediscovery time, stale retrieval, scope errors and maintenance cost.

### Experiment 2 — Execution continuity
Take one long-running multi-step execution.

Compare current execution with a minimal explicit checkpoint/resume model.

Measure recovery correctness, duplicate side effects, state reconstruction cost and complexity.

### Experiment 3 — ACI
Compare current AgentWorker tool surface against a minimal ACI-inspired interface.

Measure tool calls, context consumption, invalid edits, recovery and success.

### Experiment 4 — Evaluation
Create a small reusable evaluation scenario around one behavior that is currently difficult to verify.

Measure regression detection and maintenance cost.

### Experiment 5 — Delegation
Formalize one Orchestrator → Worker delegation contract.

Measure ambiguity, missing fields and evidence completeness.

## 13. Architectural guardrails for the refactor branch

The study suggests the following constraints should govern subsequent work:

1. **No universal ontology without a demonstrated problem.**
2. **No new abstraction solely to name an existing distinction.**
3. **Runtime state remains distinct from lifecycle state.**
4. **Runtime memory remains distinct from DEV Memory and Protocol Memory.**
5. **Evidence never becomes authority merely by existing.**
6. **Derived metadata cannot silently become canonical authority.**
7. **Persistent knowledge requires provenance and scope.**
8. **Automatic compaction must preserve durable meaning and negative knowledge.**
9. **Every new mechanism requires a measurable reason to exist.**
10. **External systems are sources of mechanisms to test, not architectures to copy.**

## 14. Final architectural position

ARgentOS should not become a generalized agent framework by absorbing the strongest feature of every competitor.

That would destroy the very property that differentiates it.

The better strategy is:

```
ARgentOS governance
        +
proven runtime mechanisms
        +
curated durable knowledge
        +
measured evolutionary adaptation
```

The refactor branch should therefore remain an **evolutionary laboratory**.

Each external comparison contributes hypotheses.
Each hypothesis becomes an experiment.
Each experiment produces evidence.
Only successful adaptations become architecture.

## Final decision

**KEEP the current architectural foundation. ADAPT selectively. EXPERIMENT before institutionalizing.**

The most consequential next area is **DEV Memory**, followed by **runtime execution continuity** and **Agent-Computer Interface quality**.

No broad architectural rewrite is justified by this study.
