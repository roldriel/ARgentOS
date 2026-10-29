# ARgentOS Refactor Study — LangGraph

**Study date:** 2026-10-29
**Decision:** ADAPT

## Scope

Comparison of LangGraph's orchestration/runtime design with ARgentOS DEV, focusing on execution topology, state, durable execution, persistence, interruption/resume, observability and memory separation.

## Evidence reviewed

LangGraph currently describes itself as a low-level orchestration framework/runtime for long-running, stateful agents. Its core model is State + Nodes + Edges, compiled into an executable graph. It explicitly supports durable execution, human-in-the-loop, persistence and memory. Its persistence layer separates thread-scoped graph checkpoints from cross-thread application-defined stores. Checkpoints are created at super-step boundaries, with task-level writes supporting pending-write recovery; durability can be tuned with `sync`, `async` and `exit`. LangGraph also documents idempotency/re-execution requirements and graph/state migration concerns.

Primary sources:
- https://docs.langchain.com/oss/python/langgraph/overview
- https://docs.langchain.com/oss/python/langgraph/graph-api
- https://docs.langchain.com/oss/python/langgraph/persistence
- https://docs.langchain.com/oss/python/langgraph/checkpointers
- https://github.com/langchain-ai/langgraph

## 1. Architecture

LangGraph makes execution topology explicit:

```
State + Nodes + Edges
        ↓
Compiled graph
        ↓
execution / interrupts / persistence / resume
```

This is a strong design when workflow branching, loops and resumability are central.

ARgentOS currently has a different strong boundary:

```
Orchestrator
   ↓
WorkerAdapter
   ↓
CommandWorker / AgentWorker
   ↓
WorkerResult
   ↓
Host continues lifecycle
```

The AgentWorker has execution capability but no sovereign authority; it cannot approve, change scope, resolve human decisions, release, promote or self-certify completion. That governance separation must remain.

**Finding:** LangGraph is stronger on explicit execution topology and durable runtime semantics. ARgentOS is stronger on authority separation and lifecycle governance.

## 2. State

LangGraph treats execution state as a first-class runtime primitive. Nodes read/write state and reducers combine concurrent updates.

ARgentOS should **not** respond by introducing a universal state model. The useful lesson is narrower:

> long-running resumable execution needs explicit runtime state that can be persisted and restored.

Execution state should remain distinct from Change Lifecycle state.

**Decision:** ADAPT conceptually; no universal ARgentOS State Model.

## 3. Durable execution

LangGraph's checkpoint/thread model makes recovery a runtime primitive. Its durability modes explicitly trade persistence guarantees against performance.

This exposes a capability that ARgentOS currently models only indirectly: what exact runtime state is sufficient to resume an interrupted worker/orchestration process.

Potential ARgentOS improvement:
- execution identity;
- resumable execution state;
- checkpoint boundary;
- interruption;
- resume semantics;
- idempotency/replay expectations.

This should live in runtime execution, not in Change Lifecycle.

## 4. Persistence and Memory

LangGraph distinguishes:

```
Checkpointer = thread-scoped execution state / continuity
Store       = durable application-defined cross-thread information
```

This is a valuable distinction for ARgentOS because:

```
execution checkpoint
    ≠ transcript/history
    ≠ Protocol Memory
    ≠ DEV Memory
```

The distinction should inform Priority 4 without copying LangGraph's implementation.

**Decision:** ADAPT the conceptual separation.

## 5. Human-in-the-loop

LangGraph treats interrupts as execution-control primitives tied to persisted state.

Useful lesson: a paused execution is not automatically a new lifecycle state.

ARgentOS already has stronger authority semantics around pending human decisions. Preserve that distinction.

**Decision:** KEEP current authority model; ADAPT the runtime notion of resumable interruption if needed.

## 6. Observability and evidence

LangGraph/LangSmith provide strong runtime tracing, checkpoint and task visibility.

That should not replace ARgentOS evidence semantics. A runtime trace can evidence execution, but it does not establish authorization, architectural correctness or lifecycle closure.

Potential use:

```
runtime event / checkpoint
        ↓
execution evidence
        ↓
ARgentOS verification
```

not:

```
trace exists
   ↓
therefore authorized/correct/closed
```

**Decision:** ADAPT selectively.

## 7. Runtime evolution

LangGraph explicitly documents how graph topology and state can change while persisted threads exist, including compatibility limits for interrupted executions and state-key changes.

This is relevant to ARgentOS because durable execution introduces a new form of evolution problem: code/runtime changes while old execution state remains resumable.

ARgentOS currently has strong repository/change lineage but not an equally explicit runtime-resume compatibility model.

**Decision:** INVESTIGATE through a focused experiment; do not build a migration framework yet.

## 8. What ARgentOS does better

- Explicit authority boundary between host and worker.
- Clear DEV vs Protocol separation.
- Distinction between `Executed`, `Committed`, `Closed` and `Released`.
- Validation anchors and Git-verifiable closure.
- Findings/corrections/revalidation provenance.
- Runtime remains provider/model agnostic.

These properties should not be sacrificed to gain runtime convenience.

## 9. What LangGraph does better

- Explicit workflow topology.
- Explicit execution state.
- Durable checkpoint/resume.
- Interrupt/recovery semantics.
- Runtime persistence separation.
- Runtime migration/idempotency guidance.
- Rich execution observability.

## 10. Why it is better

The important design choice is co-location of execution topology and durable execution semantics. Because LangGraph owns the runtime, it can make topology, state, checkpointing, interrupts and resume behavior coherent primitives.

ARgentOS deliberately separates governance from runtime. That is valuable, but it leaves a potential runtime-level gap.

## 11. What to adopt/adapt

### ADAPT-1 — Runtime execution continuity

Investigate a small runtime abstraction for execution identity, checkpoint boundary, interruption and resume.

### ADAPT-2 — Separate checkpointing from memory

Do not use one memory mechanism for resumable state and durable semantic knowledge.

### ADAPT-3 — Explicit topology when complexity warrants it

For workflows with real branching/loops/multi-step execution, test whether an explicit topology representation reduces bespoke orchestration logic.

### ADAPT-4 — Idempotency and replay guidance

Add explicit runtime semantics only if experiments demonstrate the need.

## 12. What not to adopt

- Universal graph model for all ARgentOS architecture.
- Universal state model.
- Runtime checkpoint as governance authority.
- Runtime trace as proof of authorization or closure.
- Mandatory LangGraph dependency.

## 13. Proposed experiment

Pick one representative long-running multi-step DEV execution.

Compare:
1. current Orchestrator/Worker design;
2. a minimal explicit state/topology design inspired by LangGraph.

Interrupt and resume both.

Measure:
- orchestration code;
- state reconstruction cost;
- recovery correctness;
- duplicate side effects;
- verification/evidence quality;
- conceptual complexity.

Adopt only if the explicit model produces measurable improvement.

## Final decision

**ADAPT**

LangGraph demonstrates a stronger runtime model for durable, stateful execution. The correct ARgentOS response is not a rearchitecture around graphs. It is a focused investigation of execution continuity, checkpoint/resume semantics, runtime state, idempotency and the separation between execution persistence and semantic memory.
