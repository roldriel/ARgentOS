# `runtime/` — Implementaciones de referencia de materialización

**Origen:** planes 07 y 18 (RFC-00YK, RFC-00YM del roadmap Execution Context).

Este directorio contiene **implementaciones de referencia** de materializaciones del Execution Context. No es protocolo: es el lado del runtime de la frontera protocolo/runtime.

## Frontera respecto de `protocol/.agents/`

- `protocol/.agents/` define el protocolo: qué es un Execution Context, cómo se construye y cómo se entrega (Delegation Payload). Nada de lo que hay aquí modifica, extiende ni reinterpreta `protocol/.agents/`.
- `runtime/` define cómo un runtime concreto **representa** lo entregado: la transformación de un Execution Context en una representación propia del runtime (materialización). La entrega (payload) es el último acto del protocolo; la materialización es el primer acto del runtime.
- Dependencia en un solo sentido: `runtime/` lee `protocol/.agents/` (p. ej. los `SKILL.md` como fuente de capacidades); `protocol/.agents/` nunca referencia `runtime/`.
- Nada aquí es normativo. Un runtime real puede adoptar, adaptar o ignorar estas implementaciones; la corrección conceptual vive en el Execution Context, no en la representación.

## Convenciones

- Python 3.11+, stdlib únicamente (sin dependencias externas).
- Tests propios en `tests/test_toolcalls.py` (raíz del repo), ejecutables con `python -m pytest tests/test_toolcalls.py`. Son independientes de `protocol/.agents/harness/tests/` (que valida el protocolo, no el runtime).
- Las citas a documentos del repo usan el formato `ruta:sección`.

## Materializaciones implementadas

| Materialización | Módulo | Descripción |
| --- | --- | --- |
| Prompt (referencia, existente de facto) | `runtime/toolcalls/prompt_rendering.py` | El Execution Context se representa como texto de prompt: los nombres de las skills viajan en el payload y el Worker lee cada `SKILL.md` antes de ejecutar. |
| Tool calls (segunda materialización) | `runtime/toolcalls/toolcalls_rendering.py` | Cada skill se representa como una tool declaration invocable (nombre + descripción); el contenido de la skill se obtiene bajo demanda invocando la tool, no por adelantado. |

Ambas operan sobre el mismo `ExecutionContext` (`runtime/toolcalls/context.py`), construido a partir de los mismos campos que el Delegation Payload (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`). Coexisten: ninguna es «la correcta»; la elección pertenece al runtime.

## Criterios de conformidad de una materialización

Una representación producida aquí es conforme al modelo de materialización si:

1. **Representa sin alterar**: no incorpora, elimina ni sustituye contenido conceptual del Execution Context; solo decide su forma.
2. **Capacidad efectiva**: toda skill del Execution Context queda disponible para el Worker durante la ejecución (en la materialización prompt, leyendo el `SKILL.md`; en la de tool calls, invocando la tool). El contenido de la capacidad activada es el mismo en ambas.
3. **No retroalimenta el pipeline**: la materialización consume el Execution Context ya producido; ninguna decisión de representación modifica su construcción.
4. **Budget respetado**: el costo de la representación se estima con la regla declarada y no excede el `context_budget` del contexto.

## Interacción con el Budget materializado

El Budget del runtime prompt se materializa en tokens estimados con la regla `ceil(chars/4)` (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:2. Estimation rule`). Ese estándar prevé explícitamente otros runtimes (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:6. Other runtimes`): un runtime no-prompt declara su propia unidad y regla de estimación. Este runtime declara:

- **Unidad dual**: tokens estimados (misma regla `ceil(chars/4)`) para la porción textual del contexto, más **número de tool declarations** para la porción invocable.
- **Estimación**: el costo inicial de una skill materializada como tool es el costo textual de su declaración (nombre + descripción), no el del `SKILL.md` completo; el contenido se paga solo si se invoca (carga diferida real).
- **Lo que no cambia**: el Budget es finito, limita la construcción del Execution Context, y todo valor materializado es una cota finita y positiva en la unidad declarada (`runtime/toolcalls/budget.py`).

## Ejercicio comparativo

El plan 18 ejecutó un ejercicio comparativo entre ambas materializaciones (misma tarea, Execution Context construido desde skills reales de `protocol/.agents/skills/`, reporte de costo en tokens estimados, latencia y equivalencia de la capacidad activada). Resultados y veredicto de la tesis en `docs/plans/18-anexo-b-reporte-verificacion-tesis.md`; el script del ejercicio se descartó una vez congelada la evidencia.

## Canonical materialization contract (RFC-72)

The canonical materialization is the deterministic representation directed at
the provider, produced from `SemanticContextIdentity` +
`MaterializationIdentity` (`docs/rfc/72-provider-prompt-cache-capability.md:3. Canonical Materialization`).
It makes the invariant I-MAT-001 mechanically verifiable: same semantic
identity + same materialization identity ⇒ byte-identical canonical payload.

The contract that RFC-72 identifies as missing — **variant + serialization +
ordering** — lives here, not in `protocol/.agents/` (the protocol/runtime
boundary). Concretely (`runtime/toolcalls/canonical.py`):

- **Variants**: the two existing materializations are the versioned variant
  serializers (`prompt` and `toolcalls`); the canonical envelope wraps either.
- **Serialization**: UTF-8, no BOM, LF line endings, no variable trailing
  whitespace; `serialization_version = "1"`.
- **Ordering Contract v1** (historical): the runtime declares its Current
  Ordering Choice as the de facto field order already implemented by both
  renderers (session → state → phase → role → task → context_budget →
  knowledge_entries → skills). This formalizes the runtime's choice inside a
  versioned contract; it does **not** resolve the protocol's normative
  OPEN/DEFERRED ordering state, which remains subject to measurement
  (`docs/rfc/72-provider-prompt-cache-capability.md:4. Orden (Ordering Contract)`).
  It is preserved unchanged: payloads and identities produced under v1 stay
  valid byte for byte.
- **Ordering Contract v2** (current; `docs/rfc/78-provider-bound-stable-prefix-materialization.md:5`):
  stable content first, dynamic suffix last, with the resolved stable region as
  the reusable prefix. The step `protocol-bootstrap` is **declared and empty**
  in the Worker scope: the bootstrap sequence loads the system role, the state
  machine and the orchestrator role into the **Orchestrator**, and the Worker
  execution contract does not direct the Worker to read any bootstrap document.
  Composition (`runtime/toolcalls/canonical.py`):

  ```text
  [materialization-identity banner (static)]  [stable region]  [sci anchor]  [dynamic suffix]
  ```

  The banner is static by construction, so `stable_prefix_bytes` (banner +
  stable region) is invariant to `session_uuid`, task and artifact references,
  and is a byte prefix of the payload. `stable_region` is the reusable content
  alone, independent of the banner and therefore identical across variants.
- **Stable region**: the Core + Worker stable content resolved from the payload
  (`runtime/toolcalls/segment_resolution.py`): workflow module (`target_phase`),
  role (`role_to_adopt`), profile (`profile`), harness policy
  (`harness_policy`), activated skills (`skills`) and the Worker role document.
  The Project/KB segment is **not** part of the prefix, and the **content** of
  the input artifacts never enters it — only their references participate, in
  the dynamic suffix and in the identity. An element named by the delegation
  that cannot be resolved raises `SegmentResolutionError`: the runtime reports
  the failure and never substitutes invented content.
- **Content contract**: because two different content sets must never share one
  `MaterializationIdentity`, ordering contract v2 names its content set
  explicitly (`content_contract_version`). The runtime refuses to materialize
  when the identity does not describe the contract it implements.
- **Stable Prefix**: the portion of the representation identical between
  compatible invocations (same SCI + same MI) is computed as a property of
  the materialization — not a segment, not an identity
  (`docs/rfc/72-provider-prompt-cache-capability.md:5. Stable Prefix`). The
  stable prefix is the representational counterpart of the Protocol's Stable
  Context (`protocol/.agents/standards/context/CONTEXT.md:Stable prefix (provider-bound materialization)`).
- **Reuse scope**: the prefix is reusable **intra-session**. `session_uuid`
  participates in `SemanticContextIdentity` (I-MAT-001 fidelity), so the
  runtime makes **no** claim and seeks **no** reuse across sessions.
- **Protocol version anchor**: the runtime's `PROTOCOL_VERSION`
  (`runtime/toolcalls/canonical.py`) is the semantic anchor of derived
  identities (RFC-71: `semantic_version` = protocol version governing the
  content under block versioning). It MUST equal `protocol/.agents/VERSION`
  and is enforced by `tools/check_version_state.py`; `materialization_version`
  and contract `schema_version` remain independent.

The existing materializations remain a runtime choice ("ninguna es la
correcta"); the canonical materialization is the RFC-72 contract that names
the representation produced under a `MaterializationIdentity`. This runtime
implements the **capability**, not its use: no provider is invoked, no
telemetry is written (RFC-74), and the Context Budget semantics are
untouched (I-MAT-010).

## Provider adapter boundary (RFC-72)

All provider-specific behavior stays behind the Provider Adapter boundary
(`docs/rfc/72-provider-prompt-cache-capability.md:7. Provider Adapter Boundary`).
The runtime exposes only the abstract pieces (`runtime/toolcalls/provider_cache.py`):

- **ProviderPrompt Cache Capability**: the abstract contract of
  `docs/rfc/72-provider-prompt-cache-capability.md:6. Provider Prompt Cache Capability`
  (`mechanism`, `prefix_only`, `breakpoints`, `min_cacheable_tokens`, `ttl`,
  `extended_ttl`, `model_scoped`, `isolation_scope`). It describes what the
  provider supports; it says nothing about whether ARgentOS attempts or the
  provider effectively uses the cache (I-MAT-008/009).
- **`ProviderCacheReference`**: opaque, provider-owned metadata
  (observability/diagnostic/correlation). ARgentOS never interprets it and it
  is never an authority of correctness (I-MAT-004).
- **Adapter**: the concrete provider API lives behind the adapter; the
  `NullProviderAdapter` (mechanism `none`) is the default and the test
  boundary. A cache failure degrades optimization, never semantic
  correctness (RFC-72, section 13).
- **Coordinator** (`runtime/toolcalls/cache_coordinator.py`): the runtime flow
  lookup → hit/miss → request → reference update with invalidation in the
  three non-conflatable domains (semantic, materialization, provider) and
  admission as a policy without thresholds (RFC-72, sections 9-11).
  Conceptual events (eligible/admitted/requested/hit/miss/unavailable) are
  exposed as coordinator metadata; telemetry and economics are RFC-74.

There is no provider API, no pricing, no universal TTL/eviction and no
telemetry in this directory.

## DEV Autonomous Orchestrator (Plan 122)

`runtime/orchestrator/` is a **DEV host**: it conducts the Change Lifecycle of
this repository, it does not extend it. The distinction matters:

- the lifecycle (`docs/rfc/75-change-lifecycle.md`) keeps being the single
  source of truth; the host only *reads* it and records evidence into the
  artifact the authorized plan already owns;
- the host is **not** part of the protocol payload and imports nothing from
  `protocol/.agents/`. The relation is **conformance + reference**: the DEV host
  conforms to the Protocol's behavioural contracts and patterns (Orchestrator,
  Worker, delegation, Execution Context, context assembly, recovery, authority
  boundary) and implements them in DEV terms;
- it introduces no state machine, no `next_state`, no registry, no global
  Change entity and no second persistent representation of the state. The next
  action is **derived** from `current state + Git + artifacts + evidence +
  authority + applicable gates + pending decisions + stop conditions`.

The loop (`runtime/orchestrator/host.py`) is
`observe → derive → authorize → delegate → execute → ingest → verify → decide →
continue/stop`, with explicit stop conditions and with the two structural rules
of the mechanism:

- **`exit code 0` is never workflow completion.** A worker classifies each
  command by the classification the command itself publishes (C-1/C-2/C-3), by
  its exit status and by the environmental classes **declared in the authorized
  plan**. A declared environmental class yields `GAP` — declared absence of
  obtainable evidence — and never `PASS`.
- **A worker recommendation is never an authorization.**
  `recommended_next_action` is advisory; the authority boundary
  (`runtime/orchestrator/authority.py`) returns `AUTHORIZED_EXISTING`,
  `REQUIRES_HUMAN` or `FORBIDDEN`, and release/promotion/tag are `FORBIDDEN`
  regardless of any authorization.

Modules: `contracts.py` (closed vocabularies + the M4 Worker Result contract),
`store.py` (persistent, append-only evidence under `.project/orchestrator/`,
atomic writes, fail-closed reads), `observation.py` (read-only observation of
the change), `derivation.py` (next-action derivation), `authority.py`,
`worker.py` (worker boundary + `CommandWorker`), `governance.py` (mechanical,
section-scoped, idempotent records for the authorized plan), `host.py` (M1) and
`__main__.py` (CLI: run / `--observe` / `--reconstruct`).

Operational policy: `.agents/policies/autonomous-orchestration.md`. Suite:
`tests/test_autonomous_orchestrator.py`. Standard library only; the host reuses
`tools/scoped_content_identity.py` (plan 109) instead of duplicating the Scoped
Content Identity algorithm, and it never writes `protocol/.agents/`, `dist/` or
an artifact of another plan.

## DEV Agent Worker (Plan 123)

`runtime/orchestrator/agent_worker.py` adds a **third implementation of the same
`WorkerAdapter` boundary**: `AgentWorker`. It is not a second architecture — the
host delegates through the same protocol, the result travels through the same
`WorkerResult` contract (M4, unchanged) and the host keeps conducting the
lifecycle.

```text
Human Authority → Change Lifecycle → Host → WorkerAdapter
                                              ├── CommandWorker   (executes a command-set)
                                              ├── NullWorker      (executes nothing)
                                              └── AgentWorker     (performs a task)
                                                     ↓
                                                AgentInvoker
                                                     ↓
                                                WorkerResult
```

**What it does.** It receives the delegated `task` and the reconstructed
Execution Context, asks an **`AgentInvoker`** to perform the work, observes from
**content snapshots** what really changed in the repository, runs the plan's
declared verification itself with the existing `worker.classify`, records its own
problems (including writing outside the authorized scope) and persists exactly
one `WorkerResult` plus the invocation transcript and request as evidence.

**The invocation boundary.** `AgentInvoker` is an injectable protocol with a
single method; `NullAgentInvoker` is the honest default and the test boundary. It
distinguishes three situations that must never be conflated — the invocation was
**not available**, it was **incomplete**, or it **completed** — and it never
fabricates a step, a command or a transcript. This repository ships **no provider,
no model, no network and no credentials**: the real invoker belongs to the
execution environment, which injects it with
`ExecutionHost(..., worker=AgentWorker(invoker=...))`.
`ProviderAdapter`/`NullProviderAdapter` (RFC-72) are the Prompt Cache boundary and
are deliberately **not** reused as a model-invocation mechanism.

**Authority boundary (binding).** The worker has execution capability, never
sovereign authority. It cannot approve, accept an RFC, change scope, resolve a
human decision or a finding, decide ADR-worthiness, release, promote, tag or
publish; `claims.self_reported_completion` is always `false` and
`recommended_next_action` is always advisory with `action: None`. Its internal
`observe → reason → act → inspect → verify → correct` loop is **worker-local**: it
is not an ARgentOS state machine, nothing about it is persisted as protocol state,
and the transcript is evidence, never authority.

**The delegation.** `Delegation` gained two **additive-optional** fields: `task`
(the plan's authorized instruction) and `input_artifacts` (references, never
artifact content). Both default to empty, so every delegation persisted before
plan 123 is still read unchanged. The plan declares the work and the scope in its
`## Delegación agentiva` section, which the host reads with `parse_agent_task`
(absent section ⇒ no semantic work is delegated).

**Derivation and scope verification.** When the plan declares an agent task and no
Worker Result covers the *current* content state, the host derives
`RUN_IMPLEMENTATION_TASK` **before** validation — validating first would produce
evidence about a state the implementation is about to change. After any
delegation the host verifies the scope **outside the worker**, by comparing
content snapshots of the working tree: a path that changed and is not in
`declared_scope` yields `STOP_FORBIDDEN_ACTION` with verdict `REQUIRES_HUMAN`.
Verification is deliberately independent of the worker's own account: a worker
that under-reports its changes must not escape the only check that binds it.

**Why content snapshots and not `git status`.** A scope path that is already
modified before the delegation yields the same dirty answer before and after, so
a dirty-path comparison reports neither a change nor a violation. Plan 123 found
this while dogfooding: see `<PLAN-123>:F-02`. The same defect made
`host._committed()` report `Committed=sí` for a path git does not track
(`<PLAN-123>:F-01`).

**CLI.** `python -m runtime.orchestrator --plan N --worker agent` runs the loop
with the Agent Worker. The CLI can only build the honest default
(`NullAgentInvoker`); a real invoker is injected programmatically.

**Declared limits.** No provider, model, network or credentials. No skills and no
profiles: DEV has no skill consumer and **does not read `protocol/.agents/` as
operational instructions** — the MVP works with `skills = ()`, and creating a
skill system is explicitly out of scope. No telemetry or economics (RFC-74
untouched). The correspondence between a Worker Result and the content it acted
on is established by the declared scope and the content snapshots, not by a causal
link to project content. And the Agent Worker **does not prove autonomous model
reasoning**: it proves that a worker performing authorized semantic work fits the
existing boundary without changing it.
