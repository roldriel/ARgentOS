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
- **Ordering Contract v1**: the runtime declares its Current Ordering Choice
  as the de facto field order already implemented by both renderers
  (session → state → phase → role → task → context_budget →
  knowledge_entries → skills). This formalizes the runtime's choice inside a
  versioned contract; it does **not** resolve the protocol's normative
  OPEN/DEFERRED ordering state, which remains subject to measurement
  (`docs/rfc/72-provider-prompt-cache-capability.md:4. Orden (Ordering Contract)`).
- **Stable Prefix**: the portion of the representation identical between
  compatible invocations (same SCI + same MI) is computed as a property of
  the materialization — not a segment, not an identity
  (`docs/rfc/72-provider-prompt-cache-capability.md:5. Stable Prefix`).

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
