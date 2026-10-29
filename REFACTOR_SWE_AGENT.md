# ARgentOS Refactor Study — SWE-agent / mini-SWE-agent

**Study date:** 2026-10-29
**Decision:** ADAPT

## Scope
Compare the SWE-agent Agent-Computer Interface, environment isolation, history compression, tool design and execution backend with ARgentOS DEV.

## Evidence
SWE-agent's architecture separates Agent reasoning from an environment/backend. The project emphasizes an Agent-Computer Interface (ACI): tools and feedback formats are deliberately designed for model use. The documented ACI includes a syntax-checking edit gate, a bounded file viewer, focused search, and explicit success feedback for empty command output. Current documentation states that SWE-agent has been superseded by mini-SWE-agent, which is simpler and more flexible while retaining performance.

Sources:
- https://swe-agent.com/latest/background/architecture/
- https://swe-agent.com/latest/background/aci/
- https://swe-agent.com/latest/

## 1. ACI as an architectural layer
The most important lesson is that the interface between an agent and a computer is itself an engineering surface.

Instead of exposing raw shell/file primitives and expecting the model to use them well, SWE-agent designs commands, context windows and feedback around agent behavior.

ARgentOS currently focuses strongly on authorization and execution boundaries, but less on the quality of the Agent-Computer Interface delivered to AgentWorker.

**Finding:** this is a real candidate for ARgentOS improvement.

## 2. Tool design
SWE-agent reports concrete gains from:
- syntax validation before accepting edits;
- bounded file viewing;
- focused repository search;
- explicit feedback when a command succeeds with no output.

These are small mechanisms with large agent ergonomics impact.

ARgentOS should investigate whether its AgentWorker tool surface is too generic or too expensive in context.

## 3. Environment separation
SWE-agent uses an environment/backend boundary so the Agent operates through a controlled execution environment.

This reinforces ARgentOS's WorkerAdapter concept: the agent should interact with an execution boundary rather than directly own the repository.

ARgentOS additionally has stronger authority/effect declarations. Preserve those.

## 4. History compression
SWE-agent uses a HistoryProcessor to compress long action/observation histories before sending them back to the model.

This is directly relevant to ARgentOS's context/memory concerns.

Important distinction:

```
history compression
    ≠
semantic knowledge compaction
```

Compression is a runtime context-budget mechanism. DEV Memory compaction is knowledge governance.

**Decision:** ADAPT the runtime technique conceptually; keep it separate from Priority 4 Memory.

## 5. What ARgentOS does better
- Explicit authorization/scope/effects.
- Change Lifecycle and evidence.
- DEV/Protocol boundary.
- Worker authority constraints.

## 6. What SWE-agent does better
- Agent-centric tool ergonomics.
- Explicit ACI design discipline.
- Feedback designed for model interpretation.
- History compression integrated into execution.
- Clear environment/backend separation.

## 7. Proposed adaptations
### ADAPT-1 — Agent-Computer Interface review
Audit AgentWorker's actual tool surface as an interface optimized for an agent, not merely a set of available commands.

### ADAPT-2 — Bounded observation tools
Investigate bounded file viewing and focused search to reduce context noise.

### ADAPT-3 — Pre-action validation
Test whether inexpensive syntax/structural checks should block invalid edits before execution proceeds.

### ADAPT-4 — Runtime history compression
Evaluate a history processor for long worker-local reasoning loops without turning compressed history into authoritative evidence.

## 8. Reject
- Copying SWE-agent's tool syntax wholesale.
- Treating model-oriented tool feedback as governance evidence.
- Coupling ARgentOS to SWE-ReX or Docker.
- Confusing runtime history compression with durable memory compaction.

## 9. Experiment
Run a representative repository-editing task through the current AgentWorker interface and a small ACI-inspired interface. Measure task success, context consumption, invalid edit rate, number of tool calls and recovery steps.

## Final decision
**ADAPT** — SWE-agent provides strong evidence that tool/feedback design is part of agent architecture. ARgentOS should explicitly treat the Agent-Computer Interface as an optimization surface while preserving its existing governance boundary.
