# ARgentOS Refactor Study — Google ADK

**Study date:** 2026-10-29
**Decision:** ADAPT

## Scope
Compare Google ADK and its surrounding Agents CLI lifecycle with ARgentOS on agent composition, sessions/state, workflows, artifacts, evaluation, observability, deployment and coding-agent support.

## Evidence
Current Google material shows ADK as an agent development framework with agent/tool orchestration, graph workflow APIs, callbacks, state management, sessions, memory and evaluation. The newer Agents CLI wraps ADK with a development lifecycle covering scaffold, build, evaluate, deploy, publish and observe, and provides coding-agent skills for ADK development.

Sources:
- https://google.github.io/adk-docs/
- https://google.github.io/adk-docs/tutorials/coding-with-ai/
- https://google.github.io/agents-cli/guide/development/
- https://google.github.io/agents-cli/guide/evaluation/
- https://google.github.io/agents-cli/reference/skills/

## 1. Architecture
The notable design is that ADK is not only an agent runtime. The surrounding tooling treats development as a lifecycle: scaffold → build → evaluate → deploy → observe, with explicit skills/context for coding agents.

This is unusually relevant to ARgentOS because ARgentOS itself is concerned with agent development and evolution, not merely inference.

However, Google Agents CLI remains a product development toolchain, while ARgentOS is a documental protocol/governance system. The layers should not be conflated.

## 2. Agents and workflows
ADK supports agent composition and workflow patterns, including graph-style workflow APIs and callbacks.

The useful lesson is to provide explicit runtime composition primitives without making them the same thing as governance concepts.

**Decision:** ADAPT the separation of agent composition from lifecycle governance.

## 3. Sessions, state and memory
Google's ecosystem distinguishes session continuity from broader memory/context capabilities. Agents CLI can select session storage and ADK supports stateful multi-step workflows.

This reinforces the existing ARgentOS direction that execution continuity and durable semantic knowledge should be separate concerns.

**Decision:** ADAPT the separation; no new universal Memory/State model.

## 4. Artifacts
ADK tooling treats generated files/artifacts as explicit outputs of agent work and provides artifact persistence for coding/runtime scenarios.

This is relevant to ARgentOS WorkerResult/evidence because the system needs to distinguish:

```
agent output
repository effect
artifact
verification evidence
authority
```

An artifact existing should not itself prove the change is correct or integrated.

## 5. Evaluation
Google's current tooling places structured evaluation inside the development loop. Agents CLI can generate evaluation cases, run inference, grade traces and iterate through an eval-fix loop.

This is a strong external precedent for treating evaluation as a first-class development activity rather than a final test afterthought.

ARgentOS already has validation anchors and lifecycle gates, but the comparative lesson is to make evaluation datasets/scenarios reusable and explicitly connected to agent behavior.

**Decision:** ADAPT the evaluation-loop principle.

## 6. Observability and deployment
Agents CLI exposes tracing/observability, deployment targets and lifecycle commands. This is broader operational tooling than ARgentOS currently provides.

ARgentOS should not reproduce cloud deployment infrastructure. The useful lesson is the explicit lifecycle boundary between development, evaluation, deployment and observation.

## 7. Coding-agent workflow
Google's current Agents CLI is particularly interesting because it installs skills into coding agents and uses a documented workflow to scaffold, build, evaluate and deploy agents. It also maintains machine-readable documentation indexes.

This resembles ARgentOS's concern with providing agents enough structured context to act correctly.

Potential lesson: **agent-facing documentation should be intentionally machine-navigable and lifecycle-aware**, not only human-readable.

## 8. What ARgentOS does better
- Protocol/DEV/adopter separation.
- Explicit authority and Change Lifecycle.
- Git-anchored closure.
- Findings/corrections/revalidation provenance.
- Provider-neutral governance.

## 9. What Google ADK/Agents CLI does better
- Integrated build/evaluate/deploy/observe workflow.
- Reusable evaluation datasets and eval-fix loop.
- Strong scaffolding and recipe model.
- Machine-readable documentation entry points.
- Explicit artifacts and runtime/deployment integration.

## 10. Proposed adaptations
### ADAPT-1 — Evaluation as an explicit development loop
Investigate reusable evaluation scenarios for AgentWorker/Orchestrator behavior, especially integration continuity and recovery.

### ADAPT-2 — Machine-oriented architecture navigation
Explore whether selected ARgentOS architectural information should have a stable machine-readable index, supporting the proposed Architectural Index without making it authoritative.

### ADAPT-3 — Recipe/skill pattern
Study whether common DEV workflows can be exposed through reusable skills/recipes while preserving the DEV operational layer as the authority.

### ADAPT-4 — Artifact/evidence distinction
Clarify WorkerResult/evidence semantics around generated artifacts.

## 11. Reject
- Google Cloud deployment as an ARgentOS architectural concern.
- Provider-specific lifecycle assumptions.
- A second governance layer implemented through skills.
- Treating eval scores as lifecycle authority.

## 12. Experiment
Create one small reusable evaluation set for a representative Orchestrator/Worker behavior and run it before/after a controlled runtime change. Measure whether it improves regression detection without creating redundant test infrastructure.

## Final decision
**ADAPT** — the strongest contribution is not a runtime primitive but the integrated development/evaluation loop and machine-oriented agent development experience. This supports the emerging ARgentOS direction around selective navigation, verification and evolutionary learning.
