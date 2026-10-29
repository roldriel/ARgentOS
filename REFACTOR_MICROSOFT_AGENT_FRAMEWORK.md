# ARgentOS Refactor Study — Microsoft Agent Framework

**Study date:** 2026-10-29
**Decision:** ADAPT

## Scope
Compare Agent Framework's separation of Agents, Workflows, Agent Harness, sessions/memory, middleware, checkpoints/resume and hosting with ARgentOS.

## Evidence
Microsoft Agent Framework currently groups four primary areas: Agents, Harness Agent, Workflows and Integrations. The framework exposes sessions, context providers, middleware, workflows, human-in-the-loop, checkpoints/resuming and orchestration. Its Harness composes chat client, chat pipeline, context providers, middleware/decorators and UX rather than creating a separate runtime.

Sources:
- https://learn.microsoft.com/agent-framework
- https://learn.microsoft.com/agent-framework/overview/agent-framework-overview
- https://learn.microsoft.com/agent-framework/agents/harness
- https://learn.microsoft.com/agent-framework/concepts/

## 1. Architecture
The most relevant design is the separation of concerns without forcing each concern into a new top-level runtime.

```
Agent
  +
Session / Context
  +
Middleware
  +
Workflow
  +
Harness
```

This is notably close to the problem ARgentOS is facing: several capabilities can compose without becoming one universal architectural entity.

**Finding:** this is strong evidence against a monolithic Unit/Component/Capability registry.

## 2. Agent Harness
The Harness is described as runtime scaffolding for long multi-step work. It combines model/client invocation, context/history persistence, compaction, todo/planning state, approvals, middleware and bounded looping.

ARgentOS AgentWorker currently provides a narrower execution boundary and deliberately does not prescribe a provider/model. Its internal reasoning loop is worker-local, not protocol state.

The Harness suggests that long-running agent work benefits from an explicit composition layer between raw model invocation and application governance.

**Decision:** ADAPT the concept of a compositional harness boundary, without importing provider-specific behavior.

## 3. Workflows
Agent Framework supports functional and graph-based workflows with explicit execution paths, state and advanced composition.

This overlaps with the LangGraph finding but adds a useful distinction: a workflow is an execution composition, while an Agent remains an executable actor.

ARgentOS should preserve this distinction between runtime composition and governance/lifecycle.

**Decision:** ADAPT selectively; no universal graph model.

## 4. Middleware
Middleware can intercept agent actions and provide approval handling, observability and bounded-loop behavior.

This is relevant to ARgentOS because some concerns currently distributed between host, worker and verification code may be naturally expressed as boundary interception.

Potential principle:

```
execution boundary
      ↓
interception / policy
      ↓
actual operation
      ↓
evidence
```

Do not turn middleware into authority. It is an execution mechanism.

## 5. Memory and persistence
Agent Framework separates sessions/state from context providers for memory. Workflows also support checkpoints and resuming.

This reinforces the emerging ARgentOS distinction:

```
execution state
session context
semantic memory
DEV Memory
```

These should not be collapsed into one Memory abstraction.

## 6. What ARgentOS does better
- Explicit Change Lifecycle authority.
- Worker has execution capability but not sovereign authority.
- Git-based closure and validation anchors.
- DEV/Protocol boundary.
- Provider/model agnosticism.

## 7. What Microsoft Agent Framework does better
- Clear composition between Agent, Workflow and Harness.
- Middleware as an explicit interception mechanism.
- Built-in long-running task scaffolding.
- Context providers as a dedicated extension point.
- Checkpoint/resume as a workflow capability.
- Broad hosting/integration surface.

## 8. Architectural lesson
The strongest lesson is **composition by responsibility**: Harness, Workflow, Middleware and Context Provider each solve a concrete runtime concern without becoming a universal ontology.

This maps well to the earlier ARgentOS conclusion that we should add selective layers rather than rebuild the architecture.

## 9. Proposed adaptations
### ADAPT-1 — Explicit Harness boundary
Investigate whether AgentWorker needs a stable harness-facing interface for planning loop, context, approvals, execution and evidence, while preserving host authority.

### ADAPT-2 — Middleware/interceptor concept
Test whether some repetitive pre/post execution checks belong at WorkerAdapter boundaries rather than being scattered through individual workers.

### ADAPT-3 — Workflow vs Agent separation
Keep execution topology separate from agent identity and from Change Lifecycle.

### ADAPT-4 — Context provider seam
Use a provider seam for context/memory so future DEV Memory can be injected without making Memory part of the Orchestrator's authority model.

## 10. Reject
- Generic middleware registry without a concrete interception problem.
- Microsoft-specific provider/hosting assumptions.
- Universal Harness as the new ARgentOS architecture root.
- Merging Workflow state with Change Lifecycle state.

## 11. Experiment
Model one existing AgentWorker execution as: Host → Harness → Agent/Invoker → Tools, while keeping Host authority unchanged. Compare complexity, boundary clarity and evidence completeness.

## Final decision
**ADAPT** — Microsoft Agent Framework provides strong evidence for compositional runtime boundaries, especially Harness + Workflow + Middleware + Context Provider. This is a refinement of ARgentOS runtime architecture, not a reason to replace its governance model.
