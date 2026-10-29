# ARgentOS Refactor Study — Letta

**Study date:** 2026-10-29
**Decision:** ADAPT

## Scope
Compare Letta's persistent-agent identity, memory blocks, message history, runs/steps and cross-conversation state with ARgentOS Priority 4 DEV Memory.

## Evidence
Letta defines a stateful agent as a persistent identity with memory, model/tool configuration and message history. Memory blocks can be attached to agents and shared; messages remain retrievable even after context compaction/eviction. Runs contain multiple steps, and multiple conversations can share the same underlying agent identity and memory.

Sources:
- https://docs.letta.com/concepts/stateful-agents
- https://docs.letta.com/v1-sdk/concepts/stateful-agents

## 1. Persistent identity
Letta treats the agent itself as a durable stateful object rather than reconstructing identity from each conversation.

This is relevant to ARgentOS because DEV Memory is intended to survive individual sessions and support future work.

However, ARgentOS should not equate project identity with agent identity. The durable subject is the project/system knowledge, not a specific model persona.

**Decision:** ADAPT the persistence principle; reject identity coupling.

## 2. Memory blocks
Letta keeps some memory explicitly in-context through attached memory blocks and retains older messages outside the active context.

This creates a useful two-level distinction:

```
active memory/context
        vs
historical retrievable memory
```

This aligns strongly with the emerging ARgentOS Memory model.

## 3. Message history vs memory
Letta's documentation makes it possible to retrieve historical messages after context compaction/eviction.

ARgentOS should preserve a similar distinction:

```
raw historical experience
        ↓
curated durable knowledge
        ↓
active context
```

Raw history should not automatically become Memory.

## 4. Runs and steps
Letta distinguishes an agent run from the individual inference/tool steps inside it.

This is useful for ARgentOS runtime evidence because it provides a natural hierarchy:

```
Change / task
  → run
     → step
        → action/tool
```

But this should not be confused with Change Lifecycle states.

## 5. What ARgentOS does better
- Strong evidence/provenance requirements.
- Explicit negative knowledge and rejected approaches.
- Lifecycle/authority semantics.
- DEV/Protocol separation.
- Git-backed historical truth.

## 6. What Letta does better
- Persistent agent identity.
- Clear active-memory vs historical-message distinction.
- Memory blocks as explicit context units.
- Cross-conversation memory sharing.
- Natural run/step hierarchy.

## 7. Proposed adaptations
### ADAPT-1 — Active vs historical DEV Memory
Separate the small knowledge subset injected/retrieved automatically from the larger historical evidence corpus.

### ADAPT-2 — Memory blocks as a retrieval concept
Investigate whether durable DEV knowledge should be grouped into bounded blocks/subjects rather than one flat store.

### ADAPT-3 — Run/step evidence hierarchy
Consider whether AgentWorker evidence should preserve a run/step structure for debugging without making it authoritative.

### ADAPT-4 — Cross-session continuity
Treat DEV Memory as project continuity across agent sessions, independent of the specific agent/model used.

## 8. Reject
- Persistent model/persona identity as an ARgentOS architectural primitive.
- Treating every message as Memory.
- Letting active memory override RFC/ADR/Plan authority.
- Making memory persistence equivalent to lifecycle persistence.

## 9. Experiment
Construct a small DEV Memory pilot with active knowledge entries linked to historical evidence. Measure whether an agent can answer recurring architecture questions with less rediscovery while avoiding stale/irrelevant retrieval.

## Final decision
**ADAPT** — Letta is a strong reference for the distinction between persistent identity, active memory and historical context. Its most useful lesson for ARgentOS is not an agent-memory API but a disciplined separation between what stays active and what remains retrievable.
