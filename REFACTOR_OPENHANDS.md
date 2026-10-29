# ARgentOS Refactor Study — OpenHands

**Study date:** 2026-10-29
**Decision:** ADAPT

## Scope
Compare OpenHands' coding-agent harness, workspace/tool boundaries, events, observability and persistent project memory with ARgentOS DEV.

## Evidence
OpenHands' current SDK architecture separates agent behavior from workspace/tool execution and conversation/session concerns. Its documentation also describes OpenTelemetry-based execution tracing. Its persistent-memory design is especially relevant: an opt-in two-tier memory has a small curated MEMORY.md index plus daily logs, with user-level and project-level scopes.

Primary evidence reviewed:
- OpenHands SDK documentation/repository material.
- Persistent memory design available in the OpenHands SDK documentation mirror.

## 1. Harness architecture
OpenHands treats the coding agent as a system operating against a workspace, with explicit tools/events/session concepts.

This is close to ARgentOS's DEV use case: an agent changes a repository under a controlled execution boundary.

ARgentOS already has a stronger governance layer around authorization, scope, effects, WorkerResult and Git verification.

**Finding:** OpenHands is a strong reference for the execution/harness side, not for replacing ARgentOS governance.

## 2. Workspace boundary
The agent can operate against a workspace while the execution environment can vary.

This reinforces an important ARgentOS distinction:

```
agent capability
    ≠
repository authority
    ≠
execution environment
```

ARgentOS should preserve provider/environment agnosticism while making the workspace boundary explicit.

## 3. Events and observability
OpenHands supports tracing of agent steps, tool executions, model calls and conversation lifecycle through OpenTelemetry.

This is useful because an agentic execution is a sequence of meaningful events rather than one opaque WorkerResult.

ARgentOS should investigate whether a compact runtime event stream could improve evidence reconstruction.

However, events are observations. They should not become authority automatically.

**Decision:** ADAPT selectively.

## 4. Persistent memory
OpenHands' persistent memory model is unusually close to the ARgentOS DEV Memory problem.

It uses two tiers:

```
user memory
project memory
```

Each tier contains a curated MEMORY.md index of durable, high-value facts plus daily logs for detail. Only the concise index is injected automatically; detailed logs are retrieved on demand. The design explicitly encourages pruning stale/duplicate information and avoiding trivially rediscoverable facts.

This is strong evidence for a **small always-available memory index + deeper on-demand evidence** pattern.

## 5. Comparison with ARgentOS Priority 4
The overlap is substantial:

ARgentOS wants:
- durable operational knowledge;
- compaction of transient work;
- avoidance of repository-history noise;
- future-useful conclusions;
- reduced rediscovery.

OpenHands demonstrates a concrete implementation pattern for exactly that retrieval problem.

The difference is provenance: ARgentOS DEV Memory should preserve stronger evidence class, applicability, contradiction/supersession and authority relationships.

**Decision:** ADAPT the two-tier retrieval pattern.

## 6. What ARgentOS does better
- Explicit authority and lifecycle.
- Stronger evidence/provenance semantics.
- DEV/Protocol boundary.
- Architectural distinction between runtime and governance.

## 7. What OpenHands does better
- Concrete coding-agent harness/workspace integration.
- Event-oriented execution visibility.
- Practical two-tier persistent memory.
- Keeping the automatically injected memory surface small.
- Project-scoped memory as a natural unit.

## 8. Proposed adaptations
### ADAPT-1 — Two-tier DEV Memory
Consider a compact curated index plus on-demand detailed evidence rather than injecting the full knowledge store into every session.

### ADAPT-2 — Project-scoped knowledge
Allow knowledge to be scoped to the ARgentOS DEV project while retaining a clear distinction from Protocol Memory.

### ADAPT-3 — Runtime event evidence
Investigate whether Worker execution events should be persisted as evidence summaries rather than reconstructing every action from raw transcripts.

### ADAPT-4 — Workspace as explicit execution boundary
Document the distinction between the agent actor, workspace and authority scope.

## 9. Reject
- Copying OpenHands memory files as the final DEV Memory model without provenance semantics.
- Treating daily logs as durable knowledge by default.
- Making agent-maintained memory authoritative over governance artifacts.
- Binding ARgentOS to OpenHands runtime.

## 10. Experiment
Create a 5–10 entry DEV Memory pilot with a compact index and linked detailed evidence. Compare retrieval quality and rediscovery cost against direct search through Plans/RFCs/ADRs.

## Final decision
**ADAPT** — OpenHands provides one of the strongest practical references for the memory/retrieval and coding-agent harness problems ARgentOS is considering. The two-tier memory pattern should materially influence Priority 4.
