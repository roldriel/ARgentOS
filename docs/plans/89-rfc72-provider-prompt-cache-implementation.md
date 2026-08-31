# Plan 89 — Implementación de RFC-72 (Provider Prompt Cache Capability)

**Status:** Executed
**Fecha:** 2026-08-30
**RFC:** RFC-72 (`docs/rfc/72-provider-prompt-cache-capability.md`)
**Clase:** — (no toca `protocol/.agents/`; implementación del runtime de
referencia; la vía de autorización se aplica por conservadurismo — RFC-56 —
porque implementa el contrato normativo de la RFC-72; ver `## Versionado`)
**Depende de:** plan 88 `Executed` (RFC-71 materializada en `protocol/.agents/`,
versión 10.1.0; semántica de `SegmentIdentity`/`SemanticContextIdentity`
disponible en `protocol/.agents/standards/context/CONTEXT.md:Context segments,
identity, scope and isolation`). **Gate de ejecución:** RFC-72 `Accepted` (hoy
`Proposal`; el plan 87 `87-provider-prompt-cache-capability.md` — aceptación
docs-only — está `Aprobado para ejecución` sin ejecutar y es la vía pendiente
declarada en `docs/plans/INDEX.md:Vigésima segunda serie`).
**Origen:** `docs/rfc/72-provider-prompt-cache-capability.md:2. MaterializationIdentity`,
`:3. Canonical Materialization`, `:4. Orden (Ordering Contract)`,
`:5. Stable Prefix`, `:6. Provider Prompt Cache Capability`,
`:7. Provider Adapter Boundary`, `:8. ProviderCacheReference`,
`:9. Semántica de hit / miss`, `:10. Invalidación`,
`:11. Frontera de admisión (Cache Admission)`, `:20. Implicaciones de
implementación`, `:21. Propiedades testables`; estado actual de
`runtime/README.md:Materializaciones implementadas`,
`runtime/README.md:Criterios de conformidad de una materialización`,
`runtime/toolcalls/prompt_rendering.py` y `runtime/toolcalls/toolcalls_rendering.py`;
`docs/rfc/13-execution-context-materialization-model.md:Conceptual Model`,
`docs/rfc/14-prompt-rendering-model.md:Rendering Variants`.

## Distinción de rol

```text
Plan 86 = aceptación docs-only de RFC-71 (Executed)
Plan 87 = aceptación docs-only de RFC-72 (Aprobado para ejecución; NO ejecutado)
Plan 88 = materialización normativa de RFC-71 en protocol/.agents/ (Executed, 10.1.0)
Plan 89 = implementación de RFC-72 en el runtime de referencia (ESTE plan)
```

RFC-72 es una RFC de **frontera protocolo/runtime**: sus conceptos
(`MaterializationIdentity`, Canonical Materialization, Ordering Contract,
Stable Prefix, capacidad abstracta del provider, Provider Adapter Boundary,
`ProviderCacheReference`, hit/miss, invalidación de materialización, admisión)
son del lado runtime/provider, no del protocolo semántico. El plan 88 ya
materializó la frontera ("Materialization and provider caching are
runtime/provider concerns") en
`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`;
este plan implementa el lado runtime sin volver a tocar el payload.

## Objetivo

Implementar en el runtime de referencia las capacidades que la RFC-72 define
como requisito de implementación futura, de modo que el invariant I-MAT-001
sea mecánicamente verificable: `MaterializationIdentity` con sus reglas
condicionales, la Canonical Materialization (variant + serialization +
ordering contract versionados), el Stable Prefix como propiedad de la
representación, la frontera del Provider Adapter con la capacidad abstracta,
`ProviderCacheReference` opaca, el flujo lookup → hit/miss → request →
reference update con los tres dominios de invalidación y la frontera de
admisón como policy sin umbrales. No se invoca ningún provider, no se
implementa telemetría (RFC-74) ni persistence de proyecto (RFC-73), y no se
modifica el protocolo.

## Alcance

### Included

1. Módulo de identidades del runtime (`identity.py`): derivación determinista
   de `SegmentContentIdentity`/`SegmentIdentity`/`SemanticContextIdentity`
   desde el contexto entregado (semántica de RFC-71, sin redefinirla) y de
   `MaterializationIdentity` con `materialization_version` y las dimensiones
   condicionales (provider/model/model_version) según las reglas de la RFC-72
   §2.
2. Contrato de Canonical Materialization (`canonical.py`): representación
   determinista dirigida al provider a partir de `SemanticContextIdentity +
   MaterializationIdentity` (I-MAT-001), reutilizando los serializadores
   existentes de las dos materializaciones como variantes versionadas.
3. Ordering Contract del runtime de referencia: declaración versionada del
   orden de facto ya implementado por ambos renderers (evidencia, no diseño
   nuevo); el orden normativo del protocolo permanece OPEN/DEFERRED (RFC-72
   §4).
4. Stable Prefix: cómputo de la porción de la representación que permanece
   idéntica entre invocaciones compatibles (propiedad de la materialización,
   no identidad ni segmento).
5. Provider Adapter Boundary (`provider_cache.py`): capacidad abstracta del
   provider (campos exactos de RFC-72 §6), adaptador base, `ProviderCacheReference`
   opaca y adaptador `null` (capability `none`) para tests y default.
6. Flujo de cache del runtime (`cache_coordinator.py`): lookup, hit/miss,
   request, reference update, invalidación en tres dominios y frontera de
   admisión sin umbrales. No es una state machine de protocolo.
7. Documentación del runtime (`runtime/README.md`) y tests de comportamiento
   mecánico nuevo.

### Excluded

- **RFC-71:** no se redefine `SegmentContentIdentity`/`SegmentIdentity`/
  `SemanticContextIdentity`; el runtime solo las deriva/consume (semántica ya
  materializada en `protocol/.agents/standards/context/CONTEXT.md:Identity`).
- **RFC-73:** persistence de proyecto, Project Segment store, `ProjectIdentity`
  como entidad, Discovery persistence, namespaces físicos.
- **RFC-74:** métricas, eventos de telemetría registrados, economía, umbrales,
  evidencia de admisión, dashboards. Los eventos conceptuales de RFC-72 §14 se
  exponen como metadata de salida del coordinator (para que RFC-74 los mida),
  no como catálogo de métricas.
- API concreta de ningún provider (OpenAI/Anthropic/Gemini), pricing, TTL
  universal, cache keys ni evicción universal.
- Cambios en `protocol/.agents/` (standards, contratos, state machines,
  workflows, roles, harness, `features.toml`), en `runtime/` salvo los módulos
  nuevos y `README.md`, y en `tests/` salvo los archivos de test nuevos.
- No se crea una state machine nueva, un capability registry ni un model
  registry (no existen en el repo y la RFC no los exige).

## Criterio de entrada

- [ ] RFC-72 `Accepted` (hoy `Proposal` en
      `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`); vía pendiente:
      plan 87 ejecutado u otra vía de aceptación equivalente.
- [ ] RFC-71 `Accepted (plan 86, 2026-08-29)` y plan 88 `Executed`
      (`protocol/.agents/VERSION` = `10.1.0`; semántica de identidad en
      `protocol/.agents/standards/context/CONTEXT.md:Identity`).
- [ ] Plan 87 intacto en `Aprobado para ejecución` (no se reutiliza su número;
      no se ejecuta en este plan).
- [ ] `runtime/toolcalls/` existe con `prompt_rendering.py`,
      `toolcalls_rendering.py`, `context.py` y `budget.py`; `tests/test_toolcalls.py`
      verde.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`); pytest sin fallos ajenos.
- [ ] Paso 0 verificado contra el repo: no existe en `runtime/` ni en
      `protocol/.agents/` una abstracción de provider, adapter, capability
      registry ni model registry que este plan pueda reutilizar (FACT a
      confirmar con `rg`).

## Entregables

1. `docs/plans/89-rfc72-provider-prompt-cache-implementation.md` — este plan.
2. `runtime/toolcalls/identity.py` — identidades semánticas (consumo) y
   `MaterializationIdentity` (RFC-72).
3. `runtime/toolcalls/canonical.py` — Canonical Materialization + Ordering
   Contract v1 del runtime de referencia + Stable Prefix.
4. `runtime/toolcalls/provider_cache.py` — capacidad abstracta del provider,
   Provider Adapter Boundary y `ProviderCacheReference` opaca.
5. `runtime/toolcalls/cache_coordinator.py` — flujo lookup/hit/miss/request/
   reference update, invalidación en tres dominios y admisión sin umbrales.
6. `runtime/README.md` — secciones nuevas (contrato de materialización
   canónica, orden v1, frontera del adapter).
7. `tests/test_canonical_materialization.py` — tests de I-MAT-001…I-MAT-012
   implementables.

## Unidades de implementación

### U1 — `runtime/toolcalls/identity.py` (nuevo)

- **Path:** `runtime/toolcalls/identity.py`
- **Current owner:** NONE — no existe módulo de identidades en `runtime/`; la
  semántica normativa vive en
  `protocol/.agents/standards/context/CONTEXT.md:Identity` (sin estructuras
  ejecutables) y la definición de `MaterializationIdentity` en RFC-72 §2.
- **Current relevant content:** `protocol/.agents/standards/context/CONTEXT.md:Identity`
  (composición de `SegmentIdentity`, derivación de `SemanticContextIdentity`,
  consistencia I-012); `docs/rfc/72-provider-prompt-cache-capability.md:2. MaterializationIdentity`
  (dimensiones y reglas condicionales).
- **Exact module:** archivo nuevo con:
  - `segment_content_identity(content: bytes) -> str` — SHA-256 hex del
    contenido canónico (convención SHA-256 de
    `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Hash Calculation`).
  - `segment_identity(semantic_version: str, content_identity: str, namespace: str) -> str` —
    identidad compuesta serializada de forma determinista; igualdad por
    componentes (I-001, I-003); distintos namespaces o versiones ⇒ identidades
    distintas.
  - `semantic_context_identity(protocol_version: str, project_identity: str | None, segments: tuple[Segment]) -> SemanticContextIdentity` —
    derivada, determinista por componentes, invariante a materialización
    (I-004, I-005); valida consistencia de versión y namespace (I-012) y
    lanza `ValueError` ante inconsistencia.
  - `materialization_identity(provider=None, model=None, model_version=None, materialization_version) -> str` —
    `materialization_version` SIEMPRE participa; provider/model/model_version
    participan solo si la regla condicional de RFC-72 §2 se cumple; la función
    codifica esas reglas sin inventar una séptima dimensión.
- **Exact change:** archivo nuevo, stdlib únicamente (`hashlib`, `dataclasses`).
- **RFC source:** `docs/rfc/72-provider-prompt-cache-capability.md:2. MaterializationIdentity`,
  `:15. Invariantes` (I-MAT-002, I-MAT-012);
  `docs/rfc/71-context-persistence-cacheability-model.md:4. Identidades`.
- **Why this target:** el runtime necesita identidades ejecutables para que
  I-MAT-001 sea verificable; el payload del Delegation Payload NO transporta
  identidades hoy
  (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`),
  por lo que el runtime de referencia las deriva del contexto entregado
  (frontera: el protocolo no las transmite; esto no es un cambio de contrato).
- **Dependencies:** U1 no depende de otras unidades; es la base de U2/U4.
  Define las primitivas de identidad del runtime; el plan 90 replica la misma
  fórmula en `project_segment.py` con invariante de paridad (sin dependencia
  de implementación entre planes; I-006).
- **Behavior:** determinista; sin estado; sin provider; sin persistence.
- **Tests:** unit (ver `## Tests y verificación`).
- **Verification:** pytest del módulo + batería canónica.
- **Rollback:** reversión del commit del plan; sin datos.

### U2 — `runtime/toolcalls/canonical.py` (nuevo)

- **Path:** `runtime/toolcalls/canonical.py`
- **Current owner:** `runtime/toolcalls/prompt_rendering.py` y
  `runtime/toolcalls/toolcalls_rendering.py` implementan las dos
  materializaciones existentes; ninguna es "la correcta"
  (`runtime/README.md:Materializaciones implementadas`).
- **Current relevant content:** orden de campos idéntico en ambos `render_prompt`
  (session → state → phase → role → task → context_budget → knowledge_entries →
  skills); no existe contrato de materialización canónica (FACT declarado en
  RFC-72 §3).
- **Exact module:** archivo nuevo con:
  - `OrderingContract` (dataclass versionado: `version`, `field_order`).
  - `CanonicalMaterialization` (dataclass: `semantic_context_identity`,
    `materialization_identity`, `variant`, `ordering_contract_version`,
    `serialization_version`, `payload: bytes`).
  - `canonical_materialize(context, mi, variant) -> CanonicalMaterialization` —
    reutiliza `prompt_rendering.render_prompt` / `toolcalls_rendering.render_prompt`
    como serializadores de variante y envuelve su salida en la serialización
    canónica (UTF-8, sin BOM, saltos `\n`, sin trailing whitespace variable).
  - `stable_prefix(m1: CanonicalMaterialization, m2: CanonicalMaterialization) -> bytes | None` —
    la porción común de los payloads entre invocaciones compatibles (misma
    SCI + misma MI); `None` si no son comparables (RFC-72 §5).
- **Exact change:** `ordering_contract_version = "1"` del runtime de referencia,
  con `field_order` = el orden de facto de los renderers existentes. **Decisión
  documentada (no bloqueante):** formalizar el orden existente como el Current
  Ordering Choice del runtime dentro de un Ordering Contract versionado cumple
  RFC-72 §4 (el runtime declara la elección que aplica); NO resuelve el estado
  OPEN/DEFERRED del orden normativo del protocolo, que queda sujeto a medición
  (RFC-74).
- **RFC source:** `docs/rfc/72-provider-prompt-cache-capability.md:3. Canonical Materialization`
  (I-MAT-001), `:4. Orden (Ordering Contract)`, `:5. Stable Prefix`,
  `:10. Invalidación` (cambio de ordering/serialization ⇒ invalidación de
  materialización ⇒ miss).
- **Why this target:** el contrato faltante identificado por la propia RFC es
  "variant + serialization + ordering"; el runtime de referencia es el único
  lugar del repo donde existen serializadores de materialización; duplicar el
  modelo en `protocol/.agents/` violaría la frontera
  (`runtime/README.md:Frontera respecto de protocol/.agents/`).
- **Dependencies:** U1 (identidades), `prompt_rendering.py`/`toolcalls_rendering.py`
  (serializadores existentes).
- **Behavior:** determinista: misma SCI + misma MI ⇒ mismo payload (I-MAT-001);
  distinta MI ⇒ representación potencialmente distinta (I-MAT-002); cambio de
  orden/serialización ⇒ nueva versión de MI ⇒ miss/rebuild sin invalidación
  semántica (RFC-72 §10).
- **Tests:** determinismo byte-idéntico; stable prefix; cambio de MI.
- **Verification:** pytest + batería canónica.
- **Rollback:** reversión del commit; sin datos.

### U3 — `runtime/toolcalls/provider_cache.py` (nuevo)

- **Path:** `runtime/toolcalls/provider_cache.py`
- **Current owner:** NONE — verificado: no existe provider abstraction, adapter
  abstraction, LLM client abstraction, capability registry ni model registry en
  `runtime/` ni en `protocol/.agents/` (FACT; `rg` en paso 0). Esta es la
  primera abstracción, mínima y exigida por RFC-72 §6-7.
- **Current relevant content:** frontera declarada en
  `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`
  ("Materialization and provider caching are runtime/provider concerns").
- **Exact module:** archivo nuevo con:
  - `ProviderCapability` (dataclass inmutable): `mechanism: str` (`none`|
    `implicit`|`explicit`), `prefix_only: bool`, `breakpoints: bool`,
    `min_cacheable_tokens: int`, `ttl: tuple[int | None, int | None]`,
    `extended_ttl: bool`, `model_scoped: bool`, `isolation_scope: str`
    (`account`|`org`|`project`). Campos exactos de RFC-72 §6.
  - `ProviderCacheReference` (dataclass opaco): `opaque: str`; sin semántica
    para ARgentOS; metadata de observabilidad/diagnóstico/correlación (I-MAT-004).
  - `ProviderAdapter` (ABC): `capability() -> ProviderCapability`;
    `request(prompt: bytes, reference: ProviderCacheReference | None) -> ProviderResponse`;
    `ProviderResponse(reference, cache_result: str)` con `cache_result` en
    `hit|miss|unavailable`.
  - `NullProviderAdapter` — `mechanism="none"`; default y tests (RFC-72 §13:
    provider no soporta cache ⇒ cache no disponible; la materialización sigue
    válida).
- **RFC source:** `docs/rfc/72-provider-prompt-cache-capability.md:6. Provider Prompt Cache Capability`,
  `:7. Provider Adapter Boundary`, `:8. ProviderCacheReference`,
  `:13. Failure modes`.
- **Why this target:** el repo no tiene capa de provider; la RFC define la
  capacidad abstracta "se instancia por provider en el Provider Adapter; no es
  API de provider ni configuración del protocolo" — el runtime de referencia es
  el único lugar autorizado para esta abstracción.
- **Dependencies:** independiente de U1/U2 (puede construirse en paralelo);
  consumida por U4.
- **Behavior:** sin llamadas de red; sin pricing; sin TTL universal.
- **Tests:** contract del adapter; opacidad de la referencia.
- **Verification:** pytest + batería canónica.
- **Rollback:** reversión del commit; sin datos.

### U4 — `runtime/toolcalls/cache_coordinator.py` (nuevo)

- **Path:** `runtime/toolcalls/cache_coordinator.py`
- **Current owner:** NONE — el flujo de cache del provider no existe en el repo.
- **Current relevant content:** semántica de hit/miss e invalidación en tres
  dominios (RFC-72 §9-10); admisión como policy sin umbrales (RFC-72 §11).
- **Exact module:** archivo nuevo con:
  - `CacheLookup(result: str, reference)` — `HIT`/`MISS`/`UNAVAILABLE`;
    hit/miss NO implica validez semántica (I-MAT-005).
  - `ProviderCacheCoordinator.lookup(adapter, sci, mi) -> CacheLookup`;
    `request(...)`; `update_reference(...)`.
  - Invalidación: semántica (cambio de SCI → miss/rebuild), de materialización
    (cambio de MI → miss/rebuild), del provider (evicción/TTL/unavailable →
    miss sin efecto semántico; I-MAT-006, I-MAT-007).
  - `admission_policy(eligible: bool, capability: ProviderCapability, ...) -> bool` —
    frontera de decisión sin umbrales (`reuse >= 3` NO es invariant; RFC-72
    §11; los umbrales requieren evidencia RFC-74).
  - Salida de eventos conceptuales (RFC-72 §14): `cache eligible | admitted |
    requested | hit | miss | unavailable` como metadata del coordinator, SIN
    escribir telemetría (eso es RFC-74).
- **RFC source:** `docs/rfc/72-provider-prompt-cache-capability.md:9. Semántica de hit / miss`,
  `:10. Invalidación`, `:11. Frontera de admisión (Cache Admission)`,
  `:14. Frontera de observabilidad`.
- **Why this target:** el comportamiento de cache del provider debe permanecer
  detrás de la frontera runtime/adapter (RFC-72 §7); no existe state machine ni
  worker que lo albergue en el protocolo, y crear uno sería inventar
  arquitectura.
- **Dependencies:** U1 (identidades), U3 (adapter/referencia), U2 (canonical
  payload para request).
- **Behavior:** no es una state machine de protocolo; es un componente de
  runtime con flujo determinista; un fallo del adapter degrada optimización,
  nunca correctness (RFC-72 §13).
- **Tests:** lookup/hit/miss; invalidación por dominio; admisión sin umbrales.
- **Verification:** pytest + batería canónica.
- **Rollback:** reversión del commit; sin datos.

### U5 — `runtime/README.md`

- **Path:** `runtime/README.md`
- **Current owner:** documentación del runtime de referencia.
- **Current relevant content:** `## Materializaciones implementadas` y
  `## Criterios de conformidad de una materialización`.
- **Exact section to modify:** agregar dos secciones al final, en inglés:
  `## Canonical materialization contract (RFC-72)` (variant + serialization +
  ordering contract versionados; I-MAT-001 verificable; distinción explícita
  entre las materializaciones existentes — elección del runtime — y la
  materialización canónica — contrato RFC-72) y `## Provider adapter boundary
  (RFC-72)` (capacidad abstracta, `ProviderCacheReference` opaca, sin API de
  provider, sin telemetría).
- **Exact change:** contenido autocontenido; el README es docs del repo, puede
  citar la RFC; el payload no la cita.
- **RFC source:** `docs/rfc/72-provider-prompt-cache-capability.md:3. Canonical Materialization`,
  `:7. Provider Adapter Boundary`.
- **Why this target:** el README ya declara la frontera y las materializaciones;
  es el dueño natural de la documentación del runtime.
- **Dependencies:** U1–U4.
- **Behavior:** documental.
- **Tests:** NONE (documental).
- **Verification:** revisión manual + batería.
- **Rollback:** reversión del commit.

### U6 — `tests/test_canonical_materialization.py` (nuevo)

- **Path:** `tests/test_canonical_materialization.py`
- **Current owner:** `tests/test_toolcalls.py` (suites de runtime del repo).
- **Current relevant content:** patrón de fixtures con `tmp_path` y contextos
  construidos desde `runtime/toolcalls/context.py`
  (`tests/AGENTS.md:Rules`).
- **Exact change:** archivo nuevo con casos de RFC-72 §21 (propiedades
  testables): I-MAT-001 (determinismo), I-MAT-002 (MI no cambia SCI),
  I-MAT-003 (SCI distinta no se preserva por MI igual), I-MAT-004 (referencia
  opaca), I-MAT-005 (hit/miss ≠ validez), I-MAT-006/007 (evicción/TTL no
  invalidan), I-MAT-008/009 (capability/eligibility ≠ uso), I-MAT-011
  (aislamiento cross-project), I-MAT-012 (MI fuera de SCI); cambio de ordering
  contract ⇒ MI cambia ⇒ miss/rebuild; stable prefix estable entre
  invocaciones compatibles; admisión sin umbrales.
- **RFC source:** `docs/rfc/72-provider-prompt-cache-capability.md:21. Propiedades testables`.
- **Why this target:** `tests/` es la suite dev del repo; los tests de
  `protocol/.agents/harness/tests/` son del producto y no aplican (no hay
  cambio de payload).
- **Dependencies:** U1–U4.
- **Behavior:** mecánico, stdlib-only, sin red.
- **Tests:** este archivo ES la suite.
- **Verification:** `python -m pytest tests/test_canonical_materialization.py`.
- **Rollback:** reversión del commit.

## Matriz RFC-72 → capa de implementación

| Concepto RFC-72 | Current owner | Capa requerida | Archivo/módulo objetivo | Por qué | Dependencia |
| --- | --- | --- | --- | --- | --- |
| `MaterializationIdentity` | RFC-72 (definición) | runtime state (derivación) | `runtime/toolcalls/identity.py` | El protocolo no transporta identidades hoy; el runtime las deriva del contexto entregado | RFC-71 `protocol/.agents/standards/context/CONTEXT.md:Identity` |
| Canonical Materialization (I-MAT-001) | RFC-72 | runtime contract | `runtime/toolcalls/canonical.py` | Contrato faltante (variant+serialization+ordering); serializadores solo existen en el runtime | U1 |
| Ordering Contract | RFC-72 | runtime contract (versionado) | `runtime/toolcalls/canonical.py` | El orden normativo está OPEN/DEFERRED; el runtime declara su Current Ordering Choice | U2 |
| Stable Prefix | RFC-72 | runtime (propiedad de representación) | `runtime/toolcalls/canonical.py` | Propiedad de la materialización, no identidad ni segmento (RFC-72 §5) | U2 |
| Provider Prompt Cache Capability | RFC-72 | provider adapter (capacidad abstracta) | `runtime/toolcalls/provider_cache.py` | El contrato se instancia por provider en el adapter; no es config del protocolo | — |
| Provider Adapter Boundary | RFC-72 | runtime (frontera) | `runtime/toolcalls/provider_cache.py` | No existe abstracción previa; la RFC exige la frontera | — |
| `ProviderCacheReference` | RFC-72 (frontera) | runtime (opaca) | `runtime/toolcalls/provider_cache.py` | Metadata opaca de observabilidad; nunca correctness (I-MAT-004) | — |
| hit/miss semantics | RFC-72 | runtime flow | `runtime/toolcalls/cache_coordinator.py` | Flujo de runtime; no state machine ni worker | U1, U2, U3 |
| Tres dominios de invalidación | RFC-72 (materialización) / RFC-71 (semántica) / provider | runtime | `runtime/toolcalls/cache_coordinator.py` | Miss nunca es invalidación semántica (RFC-72 §9-10) | U1–U3 |
| Admission policy | RFC-72 (policy boundary) | runtime/adapter | `runtime/toolcalls/cache_coordinator.py` | Policy sin umbrales; economía/evidencia es RFC-74 | U3 |
| Eventos conceptuales (eligible/admitted/requested/hit/miss/unavailable) | RFC-72 §14 | runtime (metadata de salida) | `runtime/toolcalls/cache_coordinator.py` | Eventos semánticos; métricas y telemetría son RFC-74 | U4 |

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo: RFC-72
   `Proposal` y plan 87 `Aprobado para ejecución` (no ejecutado); RFC-71
   `Accepted` y plan 88 `Executed`; `protocol/.agents/VERSION` = `10.1.0`;
   `runtime/toolcalls/` con los cuatro módulos existentes; ausencia de
   abstracciones de provider (búsqueda `rg -i "provider|adapter|capability"` en
   `runtime/`); batería inicial verde; rama `dev`.
1. **U1 — identity.py.** Crear el módulo con las funciones y reglas condicionales
   de RFC-72 §2. Sin estructuras en `protocol/.agents/`.
2. **U2 — canonical.py.** Crear el contrato de materialización canónica con
   `ordering_contract_version = "1"` (orden de facto de los renderers) y
   `stable_prefix`. Registrar la decisión documentada (no resuelve el orden
   normativo OPEN/DEFERRED).
3. **U3 — provider_cache.py.** Crear capacidad abstracta, adaptador base,
   `ProviderCacheReference` opaca y `NullProviderAdapter`.
4. **U4 — cache_coordinator.py.** Crear el flujo lookup/hit/miss/request/
   reference update, invalidación en tres dominios y `admission_policy` sin
   umbrales; exponer eventos conceptuales como metadata.
5. **U5 — runtime/README.md.** Agregar las dos secciones nuevas.
6. **U6 — tests.** Crear `tests/test_canonical_materialization.py` y correr la
   suite de runtime (`tests/test_toolcalls.py` sin regresión).
7. **Verificación.** Batería canónica + checklist semántico (ver sección
   siguiente); H13 por juicio (sin cambios estructurales del payload, el juicio
   es trivial).
8. **Cierre.** Plan → `Executed` con `Nota de ejecución`; commit atómico en
   `dev` (Conventional Commit en inglés). NO se ejecuta el plan 87, NO se
   acepta RFC-72 en este plan (es tarea del plan 87 u otra vía de aceptación),
   NO se tocan RFCs, `protocol/.agents/`, VERSION ni CHANGELOG.

## Tests y verificación

- **Runtime behavioral tests:** `tests/test_canonical_materialization.py`
  (I-MAT-001…I-MAT-012 implementables) + regresión de `tests/test_toolcalls.py`.
- **Protocol structural checks:** la batería canónica de
  `docs/VERSIONING.md:4.1 Batería canónica de verificación`
  (`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`,
  `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`,
  `python -m pytest tests/`). `check_dist_sync` rojo por diseño en `dev`.
- **Cross-reference verification:** `check_plan_citations.py` (citas de este
  plan contra el repo).
- **Semantic verification (juicio manual):** checklist obligatorio:

| Check | Mecanismo |
|---|---|
| I-MAT-001 verificable en el runtime | Tests de determinismo byte-idéntico |
| Frontera RFC-73 intacta | `git diff` sin cambios en persistence/discovery; checklist de Exclusiones |
| Frontera RFC-74 intacta | Sin catálogo de métricas, sin umbrales, sin telemetría escrita |
| `protocol/.agents/` sin cambios | `git diff -- protocol/.agents/` vacío |
| Ordering v1 = orden de facto existente | Comparación manual con ambos `render_prompt` |
| Sin abstracción inventada | Paso 0 (ausencia de abstracciones previas) documentado |

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

Juicios manuales: orden v1 igual al de facto; sin conceptos de RFC-73/74;
`protocol/.agents/` sin diff; sin llamadas de red ni pricing en el runtime.

## Migración

Sin migración para adoptantes: no cambia `protocol/.agents/`, contratos,
state machines, workflows ni el Delegation Payload. El runtime de referencia
gana módulos nuevos; un runtime real puede adoptar, adaptar o ignorar esta
implementación (`runtime/README.md:Frontera respecto de protocol/.agents/`).
No hay datos que migrar.

## Rollback

Commit atómico en `dev`; rollback = `git revert` del commit del plan. No hay
datos generados, estado persistido ni cache provider-owned creado por el plan
(las referencias son metadata en memoria). Los tags solo existen en `master`
y no se crean en este plan (`docs/VERSIONING.md:6. Tags`).

## Riesgos

- **Scope creep hacia RFC-73/74.** Mitigación: Excluded explícito; U4 expone
  eventos conceptuales sin registrar telemetría; sin persistence de proyecto.
- **"Inventar" el orden canónico.** Mitigación: el orden v1 se formaliza del
  estado de facto de los renderers (evidencia), se declara como decisión
  documentada del runtime y NO se resuelve el OPEN/DEFERRED normativo (RFC-72
  §4; sujeto a medición RFC-74).
- **Confundir capability con uso efectivo.** Mitigación: I-MAT-008/009
  testeados; la capacidad del adapter no implica cache activo.
- **Convertir el flujo en state machine.** Mitigación: `cache_coordinator.py`
  es componente de runtime; sin cambios en `SYSTEM_STATE_MACHINE.md` ni en
  `AGENT_STATE_MACHINE.md`.
- **Versionado mal clasificado.** Mitigación: `## Versionado` con evidencia;
  sin bump porque no toca el payload.

## Impacto en prompt caching

| Materialización | ¿Se carga en cada ejecución? | ¿Estable? | ¿Candidato a stable prefix? | ¿Aumenta el prompt obligatorio? | ¿Referenciable/cargable condicionalmente? |
|---|---|---|---|---|---|
| `identity.py` | Solo cuando el runtime deriva identidades | Sí | No (cómputo, no texto) | No | n/a |
| `canonical.py` | Por invocación de materialización canónica | Sí (contrato versionado) | Sí (produce el payload del prefix) | No | Sí |
| `provider_cache.py` | Frontera del adapter | Sí | n/a | No | Sí |
| `cache_coordinator.py` | Por request | Sí | n/a | No | Sí |
| `runtime/README.md` | No (docs) | Sí | n/a | No | Sí |

Regla global: este plan implementa la **capacidad**, no el uso: no reduce
tokens por sí mismo, no invoca providers y no produce telemetría. El Stable
Prefix se vuelve computable; el ahorro demostrable es RFC-74. El Context
Budget permanece intacto (I-MAT-010;
`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:8. Interaction with caching and persistence`).

## Versionado

- **Vía de autorización:** RFC-72 `Accepted` (Clase A de RFC-56 aplicada por
  conservadurismo: se implementa el contrato normativo de una RFC del modelo).
  La clase NO es el bump (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`).
- **Bump:** `docs/VERSIONING.md:3. Versionado` ata la versión a "cada plan
  ejecutado que toca `protocol/.agents/` (o el layout del payload fuente)".
  Este plan NO toca `protocol/.agents/` ni el layout del payload → **sin bump
  de `protocol/.agents/VERSION`**, sin sección de changelog de protocolo y sin
  tag. El cambio queda documentado en `runtime/README.md` y en este plan.
- Respuesta única: **sin cambio de versión (runtime de referencia)**.

## Grafo de dependencias

```text
RFC-71 Accepted (plan 86) ── plan 88 Executed (10.1.0, semántica en CONTEXT.md)
        │
        ▼
RFC-72 Proposal ── plan 87 (aceptación docs-only, NO ejecutado) ──► gate: RFC-72 Accepted
        │
        ▼
Plan 89 (este plan)
        ├── U1 identity.py ──► U2 canonical.py ──► U5 README.md
        │        └──────────► U4 cache_coordinator.py ──► U6 tests
        ├── U3 provider_cache.py ──► U4
        └── U6 tests (depende de U1–U4)

Sin dependencia de planes 90/91. Downstream (consumidores futuros, no
dependencias): plan 90 (persistence independiente, I-006) y plan 91
(mide lo que este plan implementa).
```

## Trazabilidad

`docs/rfc/72-provider-prompt-cache-capability.md:2. MaterializationIdentity` +
`:3. Canonical Materialization` + `:4. Orden (Ordering Contract)` +
`:5. Stable Prefix` + `:6. Provider Prompt Cache Capability` +
`:7. Provider Adapter Boundary` + `:8. ProviderCacheReference` +
`:9. Semántica de hit / miss` + `:10. Invalidación` +
`:11. Frontera de admisión (Cache Admission)` + `:20. Implicaciones de
implementación` + `:21. Propiedades testables` → Plan 89 → U1…U6. La frontera
semántica viene de RFC-71 materializada por el plan 88; este plan no redefine
ningún concepto semántico y no invade RFC-73/74.

## Criterios de salida

- [ ] U1–U4 implementados en el runtime de referencia, U5 documentado, U6 en
      verde.
- [ ] I-MAT-001…I-MAT-012 implementables verificados por tests; ordering v1
      igual al orden de facto; stable prefix computable.
- [ ] Sin cambios en `protocol/.agents/` (diff vacío), `VERSION` y CHANGELOG
      intactos; RFC-72 intacta en `Proposal` (la aceptación es del plan 87);
      plan 87 intacto.
- [ ] Sin conceptos de RFC-73/74 (checklist de Exclusiones); sin state machine
      nueva; sin flags en `features.toml`; sin harness/policies modificadas.
- [ ] Batería canónica en verde; pytest sin fallos ajenos.
- [ ] RFC-72 `Accepted` como criterio de entrada cumplido antes de ejecutar
      (gate de gobernanza).
- [ ] Plan → `Executed` con `Nota de ejecución`; commit atómico en `dev`
      (Conventional Commit en inglés).

## Nota de ejecución

Se completa al ejecutar, con fecha, verificación realizada y resultado. Si el
gate RFC-72 `Accepted` no está cumplido al momento de intentar la ejecución,
el plan permanece `Aprobado para ejecución` y NO se ejecuta (no se retrocede
estado sin justificación; `docs/VERSIONING.md:7. Estados de planes y RFCs`).

- 2026-08-31 — Ejecutado en el working tree sobre `dev` (commit atómico
  separado; el plan 87 y la serie 90–93 permanecen pendientes del mantenedor).
  Gate RFC-72 `Accepted` cumplido (plan 87 `Executed` en el working tree,
  `docs/rfc/INDEX.md`). Entregables 1–6 completados: `runtime/toolcalls/identity.py`
  (identidades semánticas de RFC-71 consumidas sin redefinir + `MaterializationIdentity`
  con reglas condicionales de RFC-72 §2), `runtime/toolcalls/canonical.py`
  (Canonical Materialization con I-MAT-001 byte-verificable, Ordering Contract
  v1 = orden de facto de los renderers sin resolver el OPEN/DEFERRED normativo,
  Stable Prefix), `runtime/toolcalls/provider_cache.py` (capacidad abstracta,
  Provider Adapter Boundary, `ProviderCacheReference` opaca, `NullProviderAdapter`),
  `runtime/toolcalls/cache_coordinator.py` (flujo lookup/hit/miss/request/reference
  update, invalidación en tres dominios, admisión sin umbrales, eventos
  conceptuales como metadata sin telemetría), dos secciones nuevas en
  `runtime/README.md` y `tests/test_canonical_materialization.py` (36 tests,
  I-MAT-001…I-MAT-012 implementables, stable prefix y cambio de ordering
  contract). Verificación: seis checkers de la batería canónica en verde y
  `python -m pytest tests/` con 279 passed (basetemp fresco por la ACL del
  `pytest-of-rolda` por defecto en sandbox Windows, mismo workaround que la
  nota del plan 87). `check_dist_sync` rojo por diseño en `dev`. Sin cambios
  en `protocol/.agents/` (diff vacío), `VERSION` ni CHANGELOG; RFC-72 intacta
  en `Accepted`; RFCs 73–74 intactas en `Proposal`; sin conceptos de RFC-73/74
  (sin persistence, sin catálogo de métricas, sin umbrales, sin llamadas de
  red ni pricing).
