# RFC-72 — Modelo de la capacidad de Provider Prompt Cache

**Status:** Proposal
**Fecha:** 2026-08-29
**Serie:** Context Persistence & Prompt Cache (RFC-A…RFC-D)
**Origen:** RFC-71 (Modelo de Context Persistence y Cacheability) y cierre de arquitectura 2026-08-29, sobre `docs/rfc/13-execution-context-materialization-model.md:Abstract`, `docs/rfc/14-prompt-rendering-model.md:Conceptual Model` y `runtime/README.md:Materializaciones implementadas`.
**Pregunta:** ¿Cómo se formaliza la capacidad de materialización y prompt caching del provider — `MaterializationIdentity`, canonical materialization, ordering contract, stable prefix, `ProviderCacheReference` y su frontera — sin acoplar el protocolo a proveedores?
**Afectados:** —

> Convención de evidencia: toda afirmación sobre el estado actual del repo se
> cita con `ruta:sección` (existente al momento de la redacción). Los
> conceptos que la arquitectura exige pero que no existen hoy se marcan como
> **Requisito de implementación futura**, nunca como capacidad existente. Esta
> RFC consume el modelo semántico de RFC-71 sin redefinirlo.

## Problema

1. **La frontera semántica ya está cerrada, pero la frontera de materialización no está modelada.** RFC-71 define `SegmentIdentity`, `SemanticContextIdentity`, scope, persistence, cacheability, isolation y correctness, y deja explícitamente fuera de la identidad semántica la materialización (`docs/rfc/71-context-persistence-cacheability-model.md:4. Identidades`). Sin un modelo de materialización, no existe contrato para transformar un contexto semántico en una representación estable dirigida a un provider ni para razonar sobre prompt caching.

2. **La materialización hoy es runtime-specific y múltiple.** El modelo de materialización (RFC-00YK) y el de prompt rendering (RFC-00YL) formalizan que la representación pertenece al runtime y que múltiples variantes pueden coexistir (`docs/rfc/14-prompt-rendering-model.md:Rendering Variants`); el runtime de referencia implementa dos materializaciones y declara explícitamente que "ninguna es la correcta; la elección pertenece al runtime" (`runtime/README.md:Materializaciones implementadas`). No existe un contrato de **materialización canónica** ni de orden canónico.

3. **Prompt caching no está modelado como capacidad.** La relación entre identidad semántica, materialización y cache del provider está ausente: no hay distinción entre hit/miss del provider y validez semántica, ni entre invalidación semántica, invalidación de materialización y evicción del provider.

4. **El propio repo gatea la implementación de cache a telemetría.** RFC-68 define que cachear re-lectura es Fase 2 gateada a telemetría (`docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`) y la investigación de costo exige telemetría antes de umbrales económicos (`docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`). Esta RFC define el contrato conceptual; los umbrales y la economía pertenecen a la RFC-D.

## Modelo

### 1. Frontera arquitectónica

**Decisión:** se preservan tres conceptos distintos, en capas distintas:

```text
Semantic Identity      → correctness (RFC-71)
Materialization Identity → reglas de representación (esta RFC)
Provider Cache Reference → estado opaco del provider (esta RFC, frontera en RFC-71)
```

La relación conceptual es:

```text
SemanticContextIdentity
        + MaterializationIdentity
        ↓
Canonical Materialization
        ↓
Stable Prefix
        ↓
Provider Prompt Cache Capability
        ↓
ProviderCacheReference
```

Es un modelo de dependencias/identidad, no un pipeline de runtime obligatorio.

#### Representación, aislamiento y estado del cache del provider

**Decisión:** son tres conceptos distintos y no deben fusionarse:

| Concern | Meaning | Owner |
| --- | --- | --- |
| MaterializationIdentity | Identidad del contrato de representación | RFC-72 |
| Provider cache isolation | Dónde puede reutilizarse el estado del cache del provider | Provider / Adapter |
| Provider cache state | Estado actual de optimización del lado del provider | Provider |

#### Matrix A — Identity Ownership

| Concept | Owner | Consumer | Provider-owned? |
| --- | --- | --- | ---: |
| SegmentContentIdentity | RFC-71 | RFC-72 | NO |
| SegmentIdentity | RFC-71 | RFC-72 | NO |
| SemanticContextIdentity | RFC-71 | RFC-72 | NO |
| MaterializationIdentity | RFC-72 | Runtime / Provider Adapter | NO |
| Canonical Materialization | RFC-72 | Provider Adapter | NO |
| Stable Prefix | RFC-72 | Provider Adapter | NO |
| ProviderCacheReference | RFC-72 (frontera) | Runtime | YES |

### 2. MaterializationIdentity

**Decisión:** `MaterializationIdentity` identifica las **reglas** que transforman un contexto semántico en una representación canónica dirigida al provider. Es distinta de `SemanticContextIdentity`: el mismo contexto semántico puede materializarse de formas distintas bajo contratos de materialización distintos (`docs/rfc/14-prompt-rendering-model.md:Conceptual Model`).

**Principio (identidad de representación vs aislamiento de cache):** una dimensión pertenece a `MaterializationIdentity` cuando cambiarla puede cambiar la representación canónica dirigida al provider, o cuando el contrato de materialización exige explícitamente identificar una representación distinta. Una restricción de aislamiento del cache del provider (p. ej., "el cache es model-scoped") **no** convierte automáticamente esa dimensión en parte de `MaterializationIdentity`.

| Dimension | Status | Normative reason |
| --- | --- | --- |
| Provider | CONDITIONAL / YES según evidencia | Solo si el provider cambia el contrato de representación dirigida al provider; dos providers que reciben representación canónica byte-idéntica bajo el mismo contrato no obligan a que provider participe |
| Model | CONDITIONAL | Solo si el modelo cambia o restringe la materialización canónica o el contrato exige representaciones model-scoped; no se usa solo porque el cache del provider sea model-scoped |
| Model version | CONDITIONAL / DEFERRED | Solo si la versión cambia el contrato de materialización o se exige aislamiento de representación por versión; no se incluye solo por tokenización |
| Serialization | YES | Cambia la representación canónica (representación textual vs tool declarations; `runtime/README.md:Criterios de conformidad de una materialización`) |
| Ordering contract | YES | Cambia la representación canónica (ordering contract version; sección 4) |
| Materialization version | YES | Identifica el contrato/versión de materialización (variant + serialization + ordering) |

**Regla (provider):** `provider` pertenece a `MaterializationIdentity` cuando el contrato de representación dirigida al provider difiere por provider. No se inventa un mecanismo de reuso cross-provider: si no hay representación byte-idéntica demostrada, cada provider con contrato distinto produce una `MaterializationIdentity` distinta. Provider identity ≠ provider cache state; provider cache isolation ≠ automáticamente `MaterializationIdentity`.

**Regla (model):** `model` pertenece a `MaterializationIdentity` solo cuando el modelo seleccionado cambia o restringe el contrato de materialización canónica, o cuando el contrato exige representaciones model-scoped. No se usa model porque el prompt caching del provider sea model-scoped.

**Regla (model version):** `model_version` pertenece a `MaterializationIdentity` solo cuando cambiarla puede cambiar el contrato de materialización canónica o un contrato explícito exige aislamiento de representación por versión.

**Decisión (tokenización):** la tokenización es un concern del provider/model. Solo afecta a `MaterializationIdentity` si cambia el contrato de materialización canónica. Esta RFC no define una abstracción de tokenizer.

**Decisión (serialización):** la serialización es un concern directo de representación: `serialization change → different canonical representation → different MaterializationIdentity`. No se traslada a la capacidad de cache del provider.

**Definición:**

```text
MaterializationIdentity = {
    provider?,                // CONDITIONAL: según regla de provider
    model?,                   // CONDITIONAL: según regla de model
    model_version?,           // CONDITIONAL/DEFERRED: según regla de model version
    materialization_version   // { variant, ordering_contract_version, serialization_version }
}
```

Las dimensiones condicionales participan cuando la regla correspondiente se cumple para el contrato de materialización concreto; `materialization_version` siempre participa. `TTL`, `cache policy` y las keys internas del provider son estado del adapter, no identidad de materialización.

**Requisito de implementación futura:** un adapter puede declarar que una misma `MaterializationIdentity` cubre varios providers solo si la representación materializada es byte-idéntica entre ellos bajo el mismo contrato; en caso contrario, cada provider/model genera una `MaterializationIdentity` distinta.

### 3. Canonical Materialization

**Decisión:** la Canonical Materialization es la representación determinista dirigida al provider producida a partir de `SemanticContextIdentity + MaterializationIdentity`. El determinismo es responsabilidad de la materialización; la composición semántica no requiere determinismo de bytes (RFC-71, sección 2).

**I-MAT-001 (invariante normativo):**

```text
Same SemanticContextIdentity
+ Same MaterializationIdentity
= Same Canonical Materialization
```

**Honestidad sobre el estado actual (FACT):** el repo no tiene hoy un contrato de materialización canónica: el runtime de referencia implementa dos materializaciones coexistentes y declara que la elección pertenece al runtime (`runtime/README.md:Materializaciones implementadas`). El contrato que falta es exactamente el **contrato de materialización canónica** (variant + serialization + ordering) que haga verificable I-MAT-001. Esta RFC define el invariante como requisito normativo del contrato futuro; no afirma que hoy se cumpla.

### 4. Orden (Ordering Contract)

**Decisión:** el orden **no** pertenece a `SemanticContextIdentity` (RFC-71, sección 4); pertenece a la materialización. Se distinguen:

- **Ordering Contract:** contrato versionado que define el orden de materialización de los segmentos estables y del sufijo dinámico. Forma parte de `materialization_version.ordering_contract_version`.
- **Current Ordering Choice:** la elección concreta que el runtime aplica en un momento dado, dentro de un Ordering Contract.

**Estado del orden concreto: OPEN / DEFERRED.** No existe evidencia en el repo de un orden de materialización normativo: `protocol/.agents/standards/context/CONTEXT.md:1. Priority of information` define la prioridad de **inclusión** (semántica), no el orden de **bytes** de la materialización; RFC-00YL define variantes de rendering, no orden (`docs/rfc/14-prompt-rendering-model.md:Rendering Variants`). La hipótesis `core → project → worker → dynamic` queda registrada como candidato no normativo, sujeto a medición (RFC-D), no como invariant.

### 5. Stable Prefix

**Decisión:** el Stable Prefix es una **propiedad de la representación materializada canónica**: la porción del prompt dirigido al provider que permanece sin cambios entre invocaciones compatibles. **No** es un Segment, ni la `SemanticContextIdentity`, ni un objeto de persistence, ni la `ProviderCacheReference`.

```text
Stable Context  = propiedad semántica (RFC-71)
Stable Prefix   = propiedad de una materialización concreta (esta RFC)
```

### 6. Provider Prompt Cache Capability

**Decisión:** la capacidad de prompt caching del provider se modela con cuatro conceptos de responsabilidad, no como un pipeline secuencial obligatorio:

```text
Semantic eligibility        → ¿puede semánticamente participar? (RFC-71, sección 7)
ARgentOS admission policy   → ¿ARgentOS decide intentarlo? (policy; esta RFC, sección 10)
Provider capability         → ¿el provider lo soporta? (contrato abstracto)
Actual provider cache usage → ¿el provider efectivamente lo cachea? (observado; RFC-D)
```

**Contrato abstracto de capacidad (conceptual; futuro):** ARgentOS necesita conocer del provider solo las capacidades abstractas que afectan la decisión de materialización y la lectura de resultados:

```text
mechanism:            none | implicit | explicit
prefix_only:          bool
breakpoints:          bool
min_cacheable_tokens: int
ttl:                  {min, max}
extended_ttl:         bool
model_scoped:         bool
isolation_scope:      account | org | project
```

**Decisión (métricas):** los valores de métricas/reporte del cache (p. ej., tokens leídos o escritos) son **metadata de observabilidad/costo**, no capacidades del mismo tipo que `mechanism`, `prefix_only`, `breakpoints`, `min_cacheable_tokens`, `ttl` o `extended_ttl`. Pertenecen conceptualmente a la frontera de la RFC-D; esta RFC no rediseña el sistema de métricas.

**Requisito de implementación futura:** este contrato se instancia por provider en el Provider Adapter; no es API de provider ni configuración del protocolo.

### 7. Provider Adapter Boundary

**Decisión:** todo comportamiento específico de provider (campos de cache de OpenAI, Anthropic, Gemini, etc.) permanece detrás de la frontera del Provider Adapter. El protocolo semántico no depende de esos campos. No se diseña una API universal copiando la semántica de un provider: se define la capacidad abstracta (sección 6) y el adapter la traduce.

**Regla:** ARgentOS conoce la capacidad abstracta y consume la representación materializada; el adapter conoce la API del provider; el provider posee su cache.

### 8. ProviderCacheReference

**Decisión (detalle que RFC-71 solo delimita):** `ProviderCacheReference` es una referencia opaca propiedad del provider/adapter al estado de cache del provider. El provider puede crearla, devolverla, cambiarla, expirarla, invalidarla o reemplazarla. ARgentOS:

- no la usa como identidad semántica, `SegmentIdentity`, `SemanticContextIdentity` ni `MaterializationIdentity`;
- no infiere correctness a partir de ella;
- puede retenerla como metadata de **observabilidad, diagnóstico o correlación** sin interpretar su semántica de provider; no se define un formato universal de referencia.

### 9. Semántica de hit / miss

**Decisión (obligatoria):**

```text
Semantic identity match  ≠  provider cache hit
Provider cache miss      ≠  semantic context invalid
SemanticContextIdentity  →  correctness (RFC-71)
Provider cache state     →  performance / economics (RFC-D)
```

### 10. Invalidación

**Decisión:** tres dominios de invalidación, no confluibles:

- **Invalidación semántica** (RFC-71): cambio de `content_identity`, `semantic_version` o inconsistencia de namespace.
- **Invalidación de materialización** (esta RFC): cambio de `MaterializationIdentity`.
- **Invalidación del cache del provider**: comportamiento, TTL, evicción o invalidation del provider.

**Regla:** un cache miss del provider **nunca** es invalidación semántica.

**No equivalencias (obligatorias):**

```text
Provider cache miss                   ≠ semantic invalidation
Provider eviction                     ≠ semantic invalidation
Provider TTL expiry                   ≠ semantic invalidation
MaterializationIdentity change        ≠ SemanticContextIdentity change
```

#### Matrix B — Dominios de invalidación

| Change | Semantic Context | Materialization | Provider Cache |
| --- | --- | --- | --- |
| Segment content | invalidated | invalidated | miss/rebuild |
| Semantic version | invalidated | invalidated | miss/rebuild |
| Namespace | invalidated | invalidated | isolated |
| Ordering | unchanged | invalidated | miss/rebuild |
| Serialization | unchanged | invalidated | miss/rebuild |
| Materialization version | unchanged | invalidated | miss/rebuild |
| Provider cache eviction | unchanged | unchanged | miss |
| Provider TTL expiry | unchanged | unchanged | miss |
| Provider unavailable | unchanged | unchanged | unavailable |

### 11. Frontera de admisión (Cache Admission)

**Decisión:** la admisión es la decisión conceptual "¿ARgentOS debe intentar usar prompt cache para esta materialización?". Es una **policy** del runtime/adapter, no un algoritmo ni un umbral normativo. `reuse >= 3` no es invariant; los umbrales económicos requieren evidencia de telemetría y pertenecen a la RFC-D.

### 12. Interacción con Context Budget

**Decisión:** se respeta el invariant I-010 de RFC-71 (`docs/rfc/71-context-persistence-cacheability-model.md:14. Invariantes`):

```text
Context Budget  = restricción semántica de composición
Prompt Cache    = optimización de reuso del lado del provider
```

Un prefijo cacheado no significa que el contexto sea semánticamente más pequeño. No se redefine Context Budget.

### 13. Failure modes

**Decisión general:** el fallo del cache del provider degrada la **optimización**, no la correctness semántica, salvo que el contrato del provider haga el caching obligatorio por una razón separada (caso no identificado en el repo). Comportamiento conceptual para:

| Condición | Comportamiento conceptual |
| --- | --- |
| Provider no soporta prompt caching | Cache no disponible; la materialización y la semántica siguen válidas |
| Provider no cachea silenciosamente | Miss observado; sin efecto semántico |
| Provider cache expira | Miss; la identidad semántica no cambia |
| Provider cache evicta | Miss; la identidad semántica no cambia |
| Provider no devuelve referencia | Sin `ProviderCacheReference`; sin efecto semántico |
| Provider devuelve referencia cambiada | Referencia nueva opaca; sin efecto semántico |
| Provider cache no disponible | Cache unavailable; materialización normal |
| Provider adapter falla | Fallo de materialización (dominio runtime), no de identidad semántica |
| Materialization contract cambia | `MaterializationIdentity` cambia; la identidad semántica no |
| Semantic context cambia | `SemanticContextIdentity` cambia (RFC-71); el cache del provider se evalúa aparte |

### 14. Frontera de observabilidad

**Decisión:** esta RFC define los **eventos semánticos** que existen conceptualmente:

```text
cache eligible
cache admitted
cache requested
cache hit
cache miss
cache unavailable
```

Las métricas detalladas, dashboards, cálculo de costo y experimentos pertenecen a la RFC-D; no se construye la arquitectura de observabilidad aquí.

### 15. Invariantes

- **I-MAT-001 — Materialization Determinism:** misma `SemanticContextIdentity` + misma `MaterializationIdentity` ⇒ misma Canonical Materialization.
- **I-MAT-002 — MI does not change SCI:** cambiar `MaterializationIdentity` no cambia `SemanticContextIdentity`.
- **I-MAT-003 — SCI change is semantic:** cambiar `SemanticContextIdentity` no preserva la identidad semántica solo porque `MaterializationIdentity` no cambie.
- **I-MAT-004 — Reference opacity:** `ProviderCacheReference` no es autoridad de correctness.
- **I-MAT-005 — Hit/miss ≠ validity:** el hit/miss del provider no determina la validez semántica.
- **I-MAT-006 — Eviction ≠ invalidation:** la evicción del provider no invalida el contexto semántico.
- **I-MAT-007 — TTL ≠ correctness:** el TTL del provider no determina la correctness semántica de ARgentOS.
- **I-MAT-008 — Capability ≠ use:** la capacidad del provider no implica uso efectivo del cache.
- **I-MAT-009 — Eligibility ≠ use:** la elegibilidad semántica no implica uso efectivo del cache.
- **I-MAT-010 — Budget:** el prompt caching no cambia la semántica del Context Budget.
- **I-MAT-011 — Isolation:** el aislamiento cross-project permanece gobernado por RFC-71.
- **I-MAT-012 — Materialization outside SCI:** los cambios específicos de materialización permanecen fuera de `SemanticContextIdentity`.

### 16. Escenarios de reuso

#### Matrix C — Reuse Outcomes

| Semantic Identity | Materialization Identity | Provider Capability | Provider Cache | Outcome |
| --- | --- | --- | --- | --- |
| same | same | supported | hit | reuse |
| same | same | supported | miss | materialize/rebuild |
| same | different | supported | any | new materialization |
| different | same | supported | any | different semantic context |
| same | same | unsupported | n/a | no provider prompt cache |

#### Casos normativos

- **Caso A — same SCI + same MI + provider hit:** se reutiliza la materialización canónica; la optimización del provider está activa.
- **Caso B — same SCI + same MI + provider miss:** el contexto semántico sigue válido; la materialización canónica sigue válida; la optimización no está disponible para esta request.
- **Caso C — same SCI + different MI:** el contexto semántico sigue válido; la materialización puede diferir; el estado del cache del provider se evalúa de forma independiente.
- **Caso D — different SCI + same MI:** son contextos semánticos distintos; no deben tratarse como el mismo contexto cacheable.
- **Caso E — mismo contenido + distinto namespace de proyecto:** `SegmentIdentity` distinta (RFC-71, sección 4); sin reuso cross-project sin autorización explícita.

### 17. Trazabilidad con el cierre de arquitectura

| Closed Architecture Decision | RFC-72 Section |
| --- | --- |
| Materialization independiente de la identidad semántica | §1, §2 |
| MaterializationIdentity | §2 |
| Stable Prefix | §5 |
| ProviderCacheReference | §8 |
| Provider capability boundary | §6, §7 |
| Provider cache ≠ correctness | §9, §15 (I-MAT-004/005) |
| Provider cache miss ≠ invalidación semántica | §9, §10 |
| Persistence independiente de Prompt Cache | heredado de RFC-71 (no redefinido) |
| Context Budget no afectado | §12 (I-MAT-010) |
| Isolation heredada de RFC-71 | §15 (I-MAT-011) |

### 18. Dependencias

- [RFC-71 — Context Persistence & Cacheability Model](docs/rfc/71-context-persistence-cacheability-model.md): **dependencia normativa**. RFC-72 consume `SegmentIdentity`, `SemanticContextIdentity`, clasificación estable/dinámico, persistence, cacheability, isolation y correctness sin redefinirlos.
- [RFC-00YK — Execution Context Materialization Model](docs/rfc/13-execution-context-materialization-model.md): la frontera protocolo/runtime.
- [RFC-00YL — Prompt Rendering Model](docs/rfc/14-prompt-rendering-model.md): variantes de rendering que la materialización canónica especializa.
- [RFC-68 — Architecture Evolution Workflow](docs/rfc/68-architecture-evolution-workflow.md): gate de telemetría para implementación de cache.

### 19. Relación con RFC-71, RFC-C y RFC-D

#### RFC-71

```text
RFC-71 define:  SegmentIdentity, SemanticContextIdentity, clasificación stable/dynamic,
                persistence semantics, cacheability semantics, isolation, correctness invalidation.
RFC-72 define:  MaterializationIdentity, Canonical Materialization, Stable Prefix,
                Provider Prompt Cache Capability, Provider Adapter Boundary,
                ProviderCacheReference, provider cache lifecycle.
```

Ambas RFCs no se redefinen entre sí: RFC-72 referencia RFC-71 para todo concepto semántico y RFC-71 no define materialización ni cache del provider.

#### RFC-C (Project & Discovery Context Persistence)

La RFC-C definirá persistence de proyecto, integración Discovery → Project Knowledge, frescura y lifecycle de persistence de proyecto. RFC-72 no implementa ni redefine esos dominios.

#### RFC-D (Cache Observability & Economics)

La RFC-D definirá métricas, telemetría, costo, economía del cache, experimentos y evidencia de admisión. RFC-72 no introduce umbrales económicos.

### 20. Implicaciones de implementación

- El comportamiento de cache específico del provider debe permanecer detrás de los adapters.
- La materialización canónica debe ser determinista para la misma `SemanticContextIdentity` + `MaterializationIdentity` (I-MAT-001); el contrato faltante (variant + serialization + ordering) es un requisito de implementación futura.
- El estado del cache del provider no debe convertirse en estado de correctness.
- Los cache misses del provider degradan optimización, nunca invalidan contexto.
- `MaterializationIdentity` debe permanecer separada de `SemanticContextIdentity`.
- Las referencias del provider deben permanecer opacas.
- La admisión es policy, no umbral normativo; requiere evidencia de telemetría (RFC-D).

### 21. Propiedades testables

- Misma `SemanticContextIdentity` + misma `MaterializationIdentity` → misma materialización canónica.
- Misma `SemanticContextIdentity` + distinta `MaterializationIdentity` → `SemanticContextIdentity` permanece igual.
- Distinta `SemanticContextIdentity` + misma `MaterializationIdentity` → contextos semánticos distintos.
- Provider cache miss → el contexto semántico permanece válido.
- Provider cache eviction → el contexto semántico permanece válido.
- Provider unsupported → Prompt Cache no disponible; el contexto semántico permanece válido.
- Mismo namespace de proyecto + misma `SemanticContextIdentity` + misma `MaterializationIdentity` → reuso permitido sujeto a policy.
- Distinto namespace de proyecto → sin reuso no autorizado.
- Cambio de `MaterializationIdentity` → solo invalidación de materialización; sin cambio de `SemanticContextIdentity`.

## Alternativas consideradas

1. **`Provider cache key == SemanticContextIdentity`.** Rechazada: la identidad del cache del provider es provider-owned; `SemanticContextIdentity` es de ARgentOS.
2. **`ProviderCacheReference == correctness identity`.** Rechazada: el estado del provider no es verdad semántica.
3. **`MaterializationIdentity` dentro de `SemanticContextIdentity`.** Rechazada: la identidad semántica debe ser materialization-independent (RFC-71, I-005).
4. **Ordering dentro de `SemanticContextIdentity`.** Rechazada: el orden es un concern de materialización (RFC-71, sección 4).
5. **Cache miss == invalidación semántica.** Rechazada: el estado del cache es optimización, no correctness.
6. **Prompt Cache == Persistence.** Rechazada: ownership y lifecycle distintos (RFC-71, sección 6).
7. **Prompt Cache == Memoization.** Rechazada: operan en niveles semánticos distintos (RFC-71, sección 8).
8. **`reuse >= 3` como invariant.** Rechazada: es política métrico-dirigida de la RFC-D; sin umbrales en esta RFC.
9. **Un API universal copiando la semántica de un provider.** Rechazada: la capacidad abstracta se define en §6; la semántica concreta queda en el adapter.

## Alcance

Esta RFC **no define**:

- APIs concretas de provider ni implementación de SDK;
- pricing de provider;
- TTL universal ni evicción universal;
- persistence de base de datos;
- persistence de proyecto/discovery;
- memoization general;
- identidad de contexto ni de segmento (RFC-71);
- rediseño del Context Budget;
- umbrales económicos;
- implementación de telemetría ni dashboards;
- un orden concreto (OPEN/DEFERRED, sección 4);
- una cache key universal del provider.

**Impacto en el protocolo:** ninguno. Es una RFC conceptual: no modifica `protocol/.agents/`, no cambia contratos, no cambia state machines, no produce bump de `VERSION` ni entrada de changelog. En `Proposal` no habilita tocar el payload (RFC-56; `docs/CONVENTIONS.md:Convenciones`).

## Criterios de aceptación

- [ ] RFC-72 depende de RFC-71 y no redefine sus conceptos.
- [ ] `MaterializationIdentity` está definida con sus dimensiones y justificaciones (sección 2).
- [ ] La Canonical Materialization y el invariant I-MAT-001 están definidos, con el contrato faltante identificado explícitamente.
- [ ] El Ordering Contract está definido; el orden concreto está marcado OPEN/DEFERRED.
- [ ] El Stable Prefix está definido como propiedad de materialización, no como segmento/identidad/objeto de persistence.
- [ ] `ProviderCacheReference` está definida como opaca y sin rol de correctness.
- [ ] Hit/miss, invalidación en tres dominios y admission están separados.
- [ ] No hay umbrales económicos, APIs de provider, ni rediseño de Context Budget/Discovery.
- [ ] Los invariantes I-MAT-001…I-MAT-012 están definidos.
- [ ] Las citas `ruta:sección` resuelven contra el repo; la batería de verificación está en verde.

## Amendment Log

- 2026-08-29 — Creación.
- 2026-08-29 — Finalización: identidad de representación separada del aislamiento y del estado del cache del provider; dimensiones de `MaterializationIdentity` revisadas (provider/model/model_version condicionales según evidencia; serialización y ordering contract siempre representación); tokenizer ya no se deriva de model_version; métricas del contrato abstracto aclaradas como observabilidad (RFC-D); `ProviderCacheReference` como metadata de observabilidad/diagnóstico/correlación; no-equivalencias de invalidación explicitadas; sin cambios arquitectónicos.
