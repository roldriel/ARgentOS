# ARgentOS Refactor Study — OpenAI Agents SDK

**Study date:** 2026-10-29
**Decision:** ADAPT

## Scope
Compare the SDK's small-primitives philosophy, delegation/handoffs, guardrails, sessions, human-in-the-loop, tracing and sandbox/workspace support with ARgentOS.

## Evidence
The current SDK deliberately exposes a small set of core primitives: Agents, Agents-as-tools/Handoffs and Guardrails, with sessions, human-in-the-loop, MCP and tracing around them. Agents + Runner manage turns, tools, handoffs, guardrails and sessions. Tracing records workflow, agent, turn, generation, tool, guardrail and handoff spans. Guardrails validate inputs/outputs and can block execution. Sessions persist conversation history across runs.

Sources:
- https://openai.github.io/openai-agents-python/
- https://openai.github.io/openai-agents-python/handoffs/
- https://openai.github.io/openai-agents-python/guardrails/
- https://openai.github.io/openai-agents-python/sessions/
- https://openai.github.io/openai-agents-python/tracing/

## 1. Architecture
The strongest lesson is restraint: the SDK keeps the conceptual surface small while composing capabilities around an Agent/Runner loop.

ARgentOS has more governance concepts because its target includes change authority, lifecycle, evidence and Protocol/DEV separation. That does not mean its runtime needs more primitives.

**Finding:** the SDK is a strong counterexample to the idea that a richer agent system requires a larger universal ontology.

## 2. Delegation and handoffs
Handoffs explicitly transfer execution to a selected receiving agent. The SDK distinguishes handoff metadata from application context and allows input filtering/history mapping.

ARgentOS already has a stronger governance boundary: Orchestrator delegates to WorkerAdapter and the worker cannot acquire authority from the delegation.

Useful lesson: delegation should be explicit about what crosses the boundary, what context is transferred and what remains local.

**Decision:** ADAPT the boundary-contract discipline; KEEP ARgentOS authority semantics.

## 3. Guardrails
OpenAI's guardrails provide executable validation around agent input/output, with blocking and parallel execution modes.

ARgentOS has validation gates and evidence semantics at a different level. The useful idea is not another universal gate/state system; it is explicit placement of checks at the boundary where the claim can be invalidated.

**Decision:** ADAPT the principle of boundary-local validation; REJECT a generic ARgentOS guardrail taxonomy unless a concrete runtime case requires it.

## 4. Sessions
Sessions encapsulate persistent working conversation context for an agent loop.

ARgentOS should preserve the distinction between session/transcript context, execution checkpoint state and durable semantic Memory.

**Decision:** ADAPT the separation, not the storage implementation.

## 5. Tracing
The SDK has built-in hierarchical tracing across workflow, agent, turn, generation, tool, guardrail and handoff events.

This is stronger than a WorkerResult alone for runtime observability.

However, tracing is evidence of what happened; it is not authority, lifecycle closure or architectural truth.

**Decision:** ADAPT event-level runtime evidence where it materially improves verification/debugging.

## 6. What ARgentOS does better
- Explicit sovereign-authority boundary.
- Change Lifecycle and Git-verifiable closure.
- Findings/corrections/revalidation lineage.
- DEV/Protocol separation.
- Provider/model agnosticism as an architectural boundary.

## 7. What the SDK does better
- Small and learnable primitive set.
- Explicit delegation semantics.
- Built-in guardrail placement.
- Built-in session abstraction.
- Rich default runtime tracing.
- Clear distinction between agent-as-tool and handoff.

## 8. Architectural lesson
The major lesson is **minimum sufficient primitives**. ARgentOS should resist introducing Unit/Relationship/State/Lineage abstractions merely because the system is complex.

The SDK also demonstrates that a strong runtime contract can expose only a few primitives while allowing complex composition.

## 9. Proposed adaptations
### ADAPT-1 — Minimize runtime primitives
Review Orchestrator/Worker interfaces for unnecessary concepts and ensure each primitive has a distinct responsibility.

### ADAPT-2 — Explicit delegation payload semantics
Document the exact information crossing Orchestrator → Worker and distinguish task, authority, context, verification commands and evidence.

### ADAPT-3 — Boundary-local checks
Place runtime checks at the earliest boundary where a bad input/output can be prevented, without creating a global guardrail model.

### ADAPT-4 — Structured runtime tracing
Investigate a compact event/span model for worker execution that can feed evidence without becoming authority.

## 10. Reject
- Copying the SDK's Agent abstraction as ARgentOS's universal unit.
- Treating handoff as equivalent to Change Lifecycle delegation.
- Treating traces as lifecycle evidence by default.
- Coupling ARgentOS to OpenAI.

## 11. Experiment
Take one Orchestrator → AgentWorker execution and compare the current delegation contract with a minimal SDK-inspired contract table: task, authority, context, tools, verification, result and evidence. Measure ambiguity and missing-boundary fields.

## Final decision
**ADAPT** — mainly for its discipline of small primitives, explicit delegation context and runtime observability. The result reinforces rather than weakens the current ARgentOS architecture direction.
