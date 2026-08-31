# Plan 91 — Implementación de RFC-74 (Cache Observability & Economics)

**Status:** Executed
**Fecha:** 2026-08-30
**RFC:** RFC-74 (`docs/rfc/74-cache-economics-telemetry-admission-evidence.md`)
**Clase:** A (vía RFC `Accepted`; toca contratos y standards de `protocol/.agents/`
de forma aditiva — `contracts/METRICS.md` y `standards/runtime/PROTOCOL_METRICS.md` —
por lo que exige RFC-74 `Accepted` según RFC-56; la clase es la vía de
autorización, no el bump — ver `## Versionado`)
**Depende de:** RFC-71 `Accepted` (plan 86) y plan 88 `Executed` (semántica de
identidad materializada en
`protocol/.agents/standards/context/CONTEXT.md:Identity`); RFC-72 `Accepted`
(plan 87) y plan 89 `Executed` (runtime de materialización/provider, productores
de U4); RFC-73 `Accepted` (plan 92) y plan 90 `Executed` (persistence de
proyecto, productores de U4); **gate de gobernanza:** RFC-74 `Accepted` vía plan
93 (cumplido, 2026-08-31). Las unidades de catálogo/agregador (U1–U3) son schema-first
y no dependen de planes 89/90; U4 (productores) sí. Tipos de dependencia y
estado actual: ver `## Dependencias (tipos y estado)`.
**Gate de ejecución:** RFC-74 `Accepted` — cumplido por el plan 93
(2026-08-31, aceptación docs-only; ver Amendment Log de la RFC-74,
`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` y `CHANGELOG.md`).
**Origen:** `docs/rfc/74-cache-economics-telemetry-admission-evidence.md:2. Estado actual de telemetría (FACT)`,
`:6. Reuse value`, `:8. Cache/reuse metrics`, `:9. Miss taxonomy`,
`:11. Token economics`, `:24. Double Counting Prevention`,
`:27. Provider-dependent vs independent metrics`, `:28. Observability schema (requisitos)`,
`:29. Privacy / data minimization`, `:31. Confidence / evidence quality`,
`:33. Ownership`, `:34. Matrices`, `:35. Invariantes`, `:36. Testable properties`;
estado actual de `protocol/.agents/contracts/METRICS.md:Event catalog`,
`:Constraints`, `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Metric catalog`,
`:Verifiability classes`, `tools/aggregate_metrics.py` (docstring y `main`),
`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Invocation Conditions`.

## Distinción de rol

```text
RFC-71 = semántica de cacheability/memoization/isolation (Accepted; plan 88)
RFC-72 = capacidad de Provider Prompt Cache (Accepted, plan 87; plan 89 la implementa en runtime)
RFC-73 = persistence de Project Knowledge (Accepted, plan 92; plan 90 la implementa)
RFC-74 = MEDICIÓN y economía (Accepted, plan 93; plan 91 la implementa)
Plan 91 = catálogo de eventos + agregador + productores (ESTE plan)
```

RFC-74 mide, no define capacidades: no redefine `MaterializationIdentity`,
Canonical Materialization, Stable Prefix ni `ProviderCacheReference` (owner
RFC-72), ni freshness/validity/eligibility de Project Knowledge (owner RFC-73).
Tampoco crea un telemetry framework nuevo ni thresholds: extiende el catálogo
existente (`METRICS.md` + `PROTOCOL_METRICS.md`) y el agregador dev
(`tools/aggregate_metrics.py`).

## Dependencias (tipos y estado)

Se distinguen tres tipos de dependencia; no son intercambiables:

- **Dependencia normativa:** la RFC que RFC-74 consume como fuente de verdad
  (`docs/rfc/74-cache-economics-telemetry-admission-evidence.md:37. Dependencias`):
  RFC-71, RFC-72 y RFC-73 deben estar `Accepted`.
- **Dependencia de implementación:** los planes que materializan los productores
  que U4 conecta (plan 89: coordinator/materialización/provider; plan 90:
  project segment/reuse eligibility) y la semántica materializada (plan 88).
- **Gate de gobernanza:** condición de ejecución que no es ni normativa ni de
  implementación — RFC-74 `Accepted` (vía plan 93) y la confirmación del usuario
  para el bump MINOR.

| Dependencia | Tipo | Estado actual |
| --- | --- | --- |
| RFC-71 `Accepted` (plan 86) + plan 88 `Executed` | Normativa + implementación (semántica en standards) | Cumplida |
| RFC-72 `Accepted` (plan 87) + plan 89 `Executed` | Normativa + implementación (productores U4) | Cumplida (estados de RFC-72 y plan 87 en el working tree, pendientes de commit del mantenedor) |
| RFC-73 `Accepted` (plan 92) + plan 90 `Executed` | Normativa + implementación (productores U4) | Cumplida (estados de RFC-73 y plan 92 en el working tree, pendientes de commit del mantenedor) |
| RFC-74 `Accepted` (plan 93, 2026-08-31) | Gate de gobernanza | **CUMPLIDO** |
| Confirmación del usuario para MINOR 10.3.0 | Gate de gobernanza | Pendiente al ejecutar |

Gate de gobernanza cumplido (RFC-74 `Accepted`, plan 93, 2026-08-31): este plan
es ejecutable cuando el mantenedor lo autorice; no se retrocede estado
(`docs/VERSIONING.md:7. Estados de planes y RFCs`).

## Objetivo

Implementar la capa de medición que RFC-74 define: extender el contrato
`METRICS.md` con los eventos de reuse/cache (`reuse_event`,
`provider_cache_event`) y el standard `PROTOCOL_METRICS.md` con el catálogo de
métricas por capa (Discovery reuse, Knowledge reuse, Materialization reuse,
Provider Prompt Cache), la separación measurement vs decision policy, la
prevención de doble conteo (I-ECO-004), las clases de evidencia (reuso de las
Verifiability classes existentes) y la regla de que la economía nunca sobreescribe
la validez (I-ECO-001). Extender `tools/aggregate_metrics.py` para agregar los
eventos nuevos y derivar las oportunidades de Discovery reuse desde los
artifacts existentes (`.last_discovery` + manifest), y consumir la
metadata/estado que los productores del runtime (planes 89/90) exponen,
documentando el seam de registro host/orchestrator (sin writer de referencia en
este repositorio). Sin umbrales, sin gates, sin rediseño de Budget ni de
Discovery.

## Alcance

### Included

1. Contrato `METRICS.md`: `schema_version` `1.1.0` → `1.2.0` y dos tipos de
   evento nuevos (`reuse_event`, `provider_cache_event`) con campos exactos
   derivados del vocabulario de RFC-74 §6/§9 y del esquema de observabilidad
   §28. Aditivo: la regla existente "unknown event types are ignored" preserva
   la compatibilidad con agregadores viejos.
2. Standard `PROTOCOL_METRICS.md`: sección `### Reuse and cache` en el catálogo
   con filas por capa y su disponibilidad (PARCIAL / NOT AVAILABLE), y sección
   corta de economía de reuse/cache con los invariantes I-ECO-001…I-ECO-006 sin
   umbrales.
3. Agregador dev `tools/aggregate_metrics.py`: parseo y agregación de los
   eventos nuevos; derivación (clase Derived) de oportunidades de Discovery
   reuse desde `.last_discovery` + manifest, sin productor nuevo.
4. Productores (gated a planes 89/90): metadata de eventos expuesta por
   `runtime/toolcalls/cache_coordinator.py` (plan 89) y
   `runtime/toolcalls/project_segment.py` (plan 90); el Orchestrator registra
   según la regla de registro existente (sin cambios en `orchestrator.md`).
5. Tests de comportamiento mecánico nuevo (agregador + eventos).
6. Al ejecutar: RFC-74 Amendment Log, `docs/rfc/INDEX.md`, `CHANGELOG.md`
   `[10.3.0]`, `protocol/.agents/VERSION` → `10.3.0`.

### Excluded

- **Thresholds y gates:** ningún umbral (`reuse >= N`, `hit rate >= X%`,
  `savings >= Y%`); la métricas siguen advisory ("No metric gates anything",
  `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Aggregation`);
  RFC-74 §26.
- **Rediseño de RFC-72/73:** sin cambios en identidades, materialización,
  persistence, freshness, provenance ni eligibilidad.
- **Telemetry framework nuevo:** los eventos se registran en el catálogo
  existente; sin dashboards, sin agentes de telemetría, sin backends.
- **Pricing:** sin precios de provider, sin función monetaria universal
  (RFC-74 §4/§25).
- **Cambios en Discovery, state machines, workflows, roles, harness,
  `features.toml` y en el Delegation Payload.**
- **Doble conteo:** ninguna métrica suma Discovery reuse + Provider cache como
  el mismo ahorro (RFC-74 §23-24; I-ECO-004).

### Non-goals (explícitos)

Los siguientes ítems NO forman parte de este plan, ni como implementación ni
como subproducto; si alguno aparece en el diff de la ejecución es un error de
scope y debe revertirse:

```text
provider pricing / price tables / hardcoded prices
billing integration / actual provider billing
CostModel / PricingModel / ProviderPricing (no existen en el repo y RFC-74 no los exige)
dashboards
telemetry backend / telemetry agents
A/B testing infrastructure
sampling framework
canary framework
economic admission gate
thresholds (reuse >= N, hit rate >= X%, savings >= Y%, TTL = X)
new cache mechanism
new persistence mechanism
new identity (incl. tipos de identidad de conocimiento nuevos)
new state machine
Context Budget redesign
```

Toda dimensión de costo que RFC-74 requiera y que no pueda observarse con la
información disponible se declara `Unavailable` (ver U2 y `## Failure modes`);
no se inventa ninguna métrica ni capacidad.

## Criterio de entrada

- [ ] RFC-74 `Accepted` (plan 93, 2026-08-31;
      `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`).
- [ ] RFC-71 `Accepted` (plan 86) y plan 88 `Executed` (semántica de identidad
      materializada en `protocol/.agents/standards/context/CONTEXT.md:Identity`);
      RFC-72 `Accepted` (plan 87) y RFC-73 `Accepted` (plan 92) — normativa que
      RFC-74 mide
      (`docs/rfc/74-cache-economics-telemetry-admission-evidence.md:37. Dependencias`).
      NOTA: la versión actual de `protocol/.agents/VERSION` es `10.2.0` (plan 90);
      `10.1.0` fue la versión del plan 88 y no se usa como condición de entrada.
- [ ] Para U4 (productores): planes 89/90 `Executed` (verificado; metadata de
      eventos disponible en el runtime). U1–U3 pueden ejecutarse sin 89/90
      (schema-first).
- [ ] `protocol/.agents/contracts/METRICS.md:Event catalog` y
      `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Metric catalog`
      en su estado actual; `tools/aggregate_metrics.py` con la arquitectura de
      eventos actual; `.last_discovery` y manifest disponibles para la
      derivación de Discovery reuse.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`); pytest sin
      fallos ajenos.
- [ ] Confirmación del usuario para el bump MINOR al ejecutar
      (`docs/VERSIONING.md:3. Versionado`).

## Entregables

1. `docs/plans/91-rfc74-cache-observability-implementation.md` — este plan.
2. `protocol/.agents/contracts/METRICS.md` — `schema_version` `1.2.0` + eventos
   `reuse_event` y `provider_cache_event` en `## Event catalog`.
3. `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` — sección
   `### Reuse and cache` + sección de economía (I-ECO) en `## Metric catalog`.
4. `tools/aggregate_metrics.py` — agregación de los eventos nuevos + derivación
   de Discovery reuse.
5. `tests/test_aggregate_metrics.py` — casos nuevos (o archivo de test nuevo si
   la suite existente lo justifica).
6. `runtime/toolcalls/cache_coordinator.py` y `runtime/toolcalls/project_segment.py`
   — exposición de metadata de eventos (solo si 89/90 están ejecutados).
7. Al ejecutar: RFC-74 Amendment Log, `docs/rfc/INDEX.md`, `CHANGELOG.md`
   `[10.3.0]`, `protocol/.agents/VERSION` → `10.3.0`.

## Unidades de implementación

### U1 — `protocol/.agents/contracts/METRICS.md` (eventos nuevos)

- **Path:** `protocol/.agents/contracts/METRICS.md`
- **Current owner:** contrato de sesión `METRICS.md` (orchestrator; sesión).
- **Current relevant content:** `## Event catalog` (tabla de tipos con campos
  requeridos) y `## Constraints` ("Unknown event types and unknown extra fields
  are ignored by aggregation, never errors"; privacy rule).
- **Exact section to modify:** `## Event catalog`, agregar filas y su semántica;
  `schema_version` `1.1.0` → `1.2.0` en las DOS ocurrencias del archivo (la del
  front matter `+++` y la línea `schema_version = "1.1.0"` del cuerpo del
  header); ambas deben quedar en `1.2.0` y consistentes.
- **Exact change:** dos tipos nuevos (aditivos):
  - `reuse_event` — Required: `layer` (`discovery` | `knowledge` |
    `materialization`), `operation` (`lookup` | `eligibility` | `reuse_attempt`
    | `post_use`). Optional según operación: `lookup_result` (`HIT`|`MISS`),
    `eligibility_decision` (`ACCEPTED`|`REJECTED`), `reason` (`semantic`|
    `policy`|`budget`|`identity`|`provider`|`availability` — taxonomía de
    misses de RFC-74 §9), `reuse_outcome` (`SUCCESSFUL`|`FAILED`),
    `invalidated` (bool). Registra el vocabulario de RFC-74 §6 sin fusionar
    hit/miss con validez semántica.
  - `provider_cache_event` — Required: `result` (`hit`|`miss`|`unavailable`).
    Optional: `tokens_cached` (int), `tokens_uncached` (int), `latency_ms`
    (int), `reference_present` (bool). Provider-dependent; `hit` NO implica
    validez (RFC-72 §9; I-ECO-003).
  - Constraint nuevo (una línea): estos eventos registran identificadores y
    cantidades únicamente; nunca contenido de prompt ni de conocimiento
    (RFC-74 §29; privacy rule existente).
  - Nota de scope/identidad (sin campos nuevos): `METRICS.md` es un artifact por
    sesión, por lo que session identity y project scope son implícitos al
    artifact; `knowledge identity where applicable` (RFC-74 §28) se representa
    con el entry key existente (`title`/path + `kind`, RFC-73 §7) — addressing
    de persistence, nunca una identidad semántica nueva (I-PROJ-011). No se
    agrega ningún campo de identidad nuevo.
  - Nota de costo (D1): la dimensión `cost metrics` de RFC-74 §28 NO se
    instrumenta: monetary pricing, actual provider billing y un universal
    monetary cost model NO se implementan (RFC-74 §4/§25); la disponibilidad de
    la dimensión de costo es `Unavailable`. No aparecen `CostModel`,
    `PricingModel`, `ProviderPricing`, price tables ni precios hardcodeados.
- **RFC source:** `docs/rfc/74-cache-economics-telemetry-admission-evidence.md:6. Reuse value`,
  `:8. Cache/reuse metrics`, `:9. Miss taxonomy`, `:28. Observability schema (requisitos)`,
  `:29. Privacy / data minimization`.
- **Why this target:** el contrato
  `protocol/.agents/contracts/METRICS.md:Event catalog` es el catálogo canónico
  de eventos de sesión; RFC-74 §28 exige extenderlo, no crear un framework
  nuevo.
- **Dependencies:** RFC-74 `Accepted`; U1 precede a U2/U3.
- **Behavior:** aditivo; agregadores viejos ignoran los tipos desconocidos
  (compatibilidad conservada por el constraint existente).
- **Tests:** validación del contrato por el checker de sesión
  (`check_session_artifacts.py`) con fixtures de sesión.
- **Verification:** batería canónica.
- **Rollback:** revertir el commit (schema_version y filas).

### U2 — `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` (catálogo y economía)

- **Path:** `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`
- **Current owner:** Protocol Metrics Standard — catálogo, registro y
  agregación (`## Metric catalog`, `## Registration rules`, `## Aggregation`,
  `## Verifiability classes`).
- **Current relevant content:** el catálogo mide proceso (Flow/Failures/
  Delegation/Context/Discovery/Session/Declarative flags); `## Verifiability
  classes` define Derived/Recorded/Verified; "No metric gates anything".
- **Exact section to modify:** dentro de `## Metric catalog`, nueva subsección
  `### Reuse and cache` (tabla con columnas Metric | Definition | Source |
  Evidence class | Availability | Scope | Provider dependency | Invariant), y
  una subsección corta `### Reuse and cache economics` con los invariantes
  I-ECO sin umbrales.
- **Exact change — métricas (solo las justificadas por RFC-74):**

| Metric | Definition | Source | Evidence class | Availability | Scope | Provider dep. | Invariant |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `reuse.lookup_hits` / `reuse.lookup_misses` | Resultados de lookup por capa | `event:reuse_event` | Recorded (Observed) | PARCIAL (hasta productores) | sesión/proyecto | NO | I-ECO-002, I-ECO-006 |
| `reuse.eligibility_accepted` / `reuse.eligibility_rejected` | Decisiones de elegibilidad | `event:reuse_event` | Recorded (Observed) | PARCIAL | sesión/proyecto | NO | I-ECO-001 |
| `reuse.outcome_successful` / `reuse.outcome_failed` | Resultado del intento de reuse | `event:reuse_event` | Recorded (Observed) | PARCIAL | sesión/proyecto | NO | I-ECO-001 |
| `reuse.invalidated` | Eventos de lifecycle post-reuse | `event:reuse_event` | Recorded (Observed) | PARCIAL | sesión/proyecto | NO | I-ECO-001 |
| `reuse.materialization_*` | Oportunidad/lookup/outcome de materialización (RFC-72) | `event:reuse_event` (`layer=materialization`) | Recorded (Observed) | NOT AVAILABLE hasta plan 89 | sesión/proyecto | NO | I-ECO-002, I-ECO-004 |
| `cache.provider_hits` / `cache.provider_misses` / `cache.provider_unavailable` | Estado del cache del provider | `event:provider_cache_event` | Recorded (Observed, provider-reported) | NOT AVAILABLE hasta adapter real (plan 89) | sesión/proyecto | SÍ | I-ECO-003, I-ECO-006 |
| `cache.tokens_cached` / `cache.tokens_uncached` | Tokens del cache del provider | `event:provider_cache_event` | Recorded (Observed) si el provider reporta; Verified (Estimated, regla chars/4) si recomputable contra payload capturado; Unavailable si no | NOT AVAILABLE | sesión/proyecto | SÍ | I-ECO-005, I-ECO-006 |
| `cache.latency_ms` | Latencia del request del provider | `event:provider_cache_event` | Recorded (Observed) | NOT AVAILABLE | sesión/proyecto | SÍ | I-ECO-005 |
| `discovery.reuse_opportunities` | Estimación derivada (estado) de entradas activas de conocimiento de discovery actualmente reutilizables dentro de la ventana de frescura (`.last_discovery` + manifest `ttl_hours` + `[entries] active`); NO es conteo de lookup, de intento de reuse, de reuse exitoso, de cache hit ni de eventos observados | `fs` (`.last_discovery` + manifest) | Derived | DISPONIBLE con evidencia válida; NOT AVAILABLE sin artifacts/metadata válida | proyecto | NO | I-ECO-004, I-ECO-005 |

**Clasificación de evidencia por métrica (RFC-74 §31 → Verifiability classes):**

- **Observed** (el provider/runtime reporta el valor): `reuse.lookup_*`,
  `reuse.eligibility_*`, `reuse.outcome_*`, `reuse.invalidated`,
  `reuse.materialization_*`, `cache.provider_*`, `cache.latency_ms`,
  `cache.tokens_cached`/`cache.tokens_uncached` (cuando el provider los reporta)
  → clase **Recorded** (reporte único) o **Verified** cuando existe un segundo
  artifact que lo corrobora.
- **Estimated** (estimación local): la estimación de tokens con la regla
  existente `ceil(chars/4)`
  (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:2. Estimation rule`)
  se usa SOLO donde RFC-74 §11 lo permite y se clasifica **Verified** cuando la
  regla es mecánicamente recomputable contra el payload capturado (precedente
  `context.budget_consumed` en
  `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Verifiability classes`);
  si no hay payload capturado, **Recorded**. La estimación local NUNCA es
  factura ni ahorro monetario.
- **Derived** (calculado de otros datos): `discovery.reuse_opportunities`
  (agregador) y cualquier ratio/atribución futura → clase **Derived**.
- **Unavailable** (no obtenible): declarado en la columna Availability; sin
  data point fabricado.

**Métricas de RFC-74 NO instrumentadas por este plan → `Unavailable` (D2):**

No se agrega instrumentación para hacer desaparecer `Unavailable`. Las
siguientes dimensiones de RFC-74 quedan explícitamente `Unavailable` en el
catálogo (columna Availability) porque la información requerida no está
disponible de forma confiable en el runtime/provider actual:

| Dimensión RFC-74 | Ítems | Estado |
| --- | --- | --- |
| Latencia (§10) | `baseline latency`, `reuse latency`, `cache lookup latency`, `validation latency`, `materialization latency`, `latency saved/overhead/net` | Unavailable (solo `provider request latency` vía `cache.latency_ms` se instrumenta) |
| Tokens (§11) | `baseline input tokens`, `reused input tokens`, `output tokens`, `tokens avoided`, `tokens spent validating/retrieving` | Unavailable (requieren baseline/telemetría del provider inexistentes; solo `tokens_cached`/`tokens_uncached` se instrumentan) |
| Costo (§4/§25/§28) | monetary cost / pricing / billing | Unavailable (D1; sin pricing, sin billing) |
| Context Budget (§12) | `budget_rejected` | Unavailable (solo `budget_declared`/`budget_consumed` existen en el catálogo actual) |
| Storage (§15) | artifact size, retention, storage growth, GC | Unavailable (RFC-74 §15: "si corresponde"; este plan no instrumenta storage) |

Regla: si la información necesaria no está disponible de forma confiable en el
runtime/provider actual, la dimensión se registra como `Unavailable`, nunca se
inventa ni se estima sin autorización normativa.

**Definición de `discovery.reuse_opportunities` (C-2):** métrica derivada
basada en estado. Estima el número de entradas activas de conocimiento de
discovery actualmente reutilizables dentro de la ventana de frescura
configurada. NO es: un conteo de lookup; un conteo de intentos de reuse; un
conteo de reuses exitosos; un conteo de cache hits; ni un conteo de eventos
observados. El mismo conocimiento puede contribuir a este valor derivado en
más de una agregación/sesión si el estado de discovery sigue fresco; por lo
tanto NO debe interpretarse como actividad acumulada de reuse ni como ahorro
económico. Clase: **Derived** (nunca Observed). Disponibilidad: `DISPONIBLE`
con evidencia válida; `NOT AVAILABLE` (sin data point fabricado) cuando
faltan o son inválidos `.last_discovery`/manifest/TTL — `0` solo significa
"cero entradas frescas con evidencia válida", nunca "sin datos".

**Reglas normativas de la subsección (en inglés, autocontenido):** hit rate ≠
economic value (I-ECO-002); la economía nunca sobreescribe validez (I-ECO-001);
el estado del cache del provider no es Project Knowledge (I-ECO-003); sin doble
conteo entre capas (I-ECO-004); evidencia por clase (I-ECO-005); mediciones
provider-dependent no se generalizan (I-ECO-006); ningún threshold (RFC-74 §26);
las métricas siguen sin gatear nada
(`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Aggregation`).
- **Exact change — clases de evidencia:** el vocabulario de RFC-74 §31
  (Observed/Estimated/Derived/Unavailable) es una anotación de calidad/
  disponibilidad del data point que se mapea a las Verifiability classes
  existentes (`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Verifiability classes`)
  sin crear una segunda taxonomía: Observed → Recorded (reporte único) o
  Verified (corroborado por segundo artifact); Estimated → Verified cuando la
  regla de estimación local es mecánicamente recomputable contra el payload
  capturado (precedente `context.budget_consumed`) o Recorded en caso contrario;
  Derived → Derived (agregador); Unavailable → sin data point / declarado en la
  columna Availability. El reporte del agregador etiqueta cada métrica con su
  clase de evidencia y su disponibilidad.
- **RFC source:** `docs/rfc/74-cache-economics-telemetry-admission-evidence.md:8. Cache/reuse metrics`,
  `:27. Provider-dependent vs independent metrics`, `:31. Confidence / evidence quality`,
  `:35. Invariantes`, `:34. Matrices` (A, B, C).
- **Why this target:** el standard es el dueño del catálogo y de las clases de
  evidencia; duplicar el modelo en otro archivo violaría single-source.
- **Dependencies:** U1.
- **Behavior:** normativo (define qué miden los eventos y con qué clase).
- **Tests:** batería canónica (payload).
- **Verification:** `check_protocol_invariants` + checklist semántico.
- **Rollback:** revertir el commit.

### U3 — `tools/aggregate_metrics.py` (agregación)

- **Path:** `tools/aggregate_metrics.py`
- **Current owner:** agregador dev de métricas (docstring: agrega `ENTRY` +
  `METRIC` + filesystem; dev-only; advisory).
- **Current relevant content:** parseo de `METRIC` comments; `aggregate_session`
  / `aggregate` / `main` (docstring del módulo); evento desconocido ignorado.
- **Exact change:** extender `_scan_session` (o la función equivalente de
  parseo de eventos) para reconocer `reuse_event` y `provider_cache_event`;
  agregar al reporte las métricas de `### Reuse and cache` de U2; añadir
  derivación (clase Derived) de oportunidades de Discovery reuse desde
  `.last_discovery` (timestamp/scope) + manifest (`ttl_hours`, `[entries]
  active/stale`) —
  `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Invocation Conditions`
  — sin productor nuevo (Derived state-based; nunca un conteo de eventos
  observados; ausencia de artifacts/metadata → `Unavailable`, `0` solo con
  evidencia válida de cero entradas frescas); preservar el comportamiento de
  eventos desconocidos
  ignorados y la emisión JSON; `--audit` sin cambios de contrato.
  Comportamiento preservado: `unknown events → ignored` (constraint existente
  `protocol/.agents/contracts/METRICS.md:Constraints`), `corrupt events →
  counted as corrupt` (nunca descartados en silencio), `known events →
  aggregated`.
  Reglas de agregación económica: dimension-specific y layer-specific — el
  reporte agrega por capa (`layer`) y NUNCA produce un único `cache_hit`, un
  único `savings` global ni suma ahorros de capas distintas como el mismo
  ahorro (I-ECO-004; RFC-74 §23-24). No se inventa ningún algoritmo de
  atribución que RFC-74 no defina: la única derivación es el conteo de
  oportunidades de Discovery reuse (`discovery.reuse_opportunities`, clase
  Derived) y los totales por capa.
- **RFC source:** `docs/rfc/74-cache-economics-telemetry-admission-evidence.md:2. Estado actual de telemetría (FACT)`,
  `:8. Cache/reuse metrics`, `:9. Miss taxonomy`, `:13. Discovery economics`.
- **Why this target:** el agregador es el único consumidor mecánico del
  catálogo en el repo; los eventos nuevos deben agregarse aquí (dev-only, no
  parte del payload distribuido).
- **Dependencies:** U1/U2 (nombres de eventos y métricas).
- **Behavior:** derivado de la metadata; nunca modifica artifacts de sesión
  (append-only).
- **Tests:** `tests/test_aggregate_metrics.py` con fixtures de sesión
  (`METRICS.md` con los eventos nuevos + `.last_discovery` + manifest).
- **Verification:** pytest del tool + batería.
- **Rollback:** revertir el commit; sin datos.

### U4 — Productores (gated a planes 89/90 `Executed`)

- **Path:** `runtime/toolcalls/cache_coordinator.py` (plan 89) y
  `runtime/toolcalls/project_segment.py` (plan 90)
- **Current owner:** runtime de referencia (planes 89/90 si están ejecutados).
- **Exact change:** el coordinator de cache expone la metadata de eventos
  conceptuales de RFC-72 §14 (`eligible | admitted | requested | hit | miss |
  unavailable`) como estructura de retorno (sin escribir `METRICS.md`: el
  runtime no escribe artifacts de sesión); `project_segment.py` expone
  `reuse_eligibility` para que el host registre `reuse_event` de
  knowledge/discovery. El Orchestrator registra según la regla existente
  (`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Registration rules`:
  todo data point no-trigger se registra como `METRIC` en `METRICS.md` al
  momento del evento) — sin cambios en `orchestrator.md`.

  **Frontera productor → telemetría (C-1):** Plan 91 implementa el contrato de
  telemetría, la clasificación de evidencia, la agregación y las métricas
  derivadas. Los componentes del runtime exponen el estado/metadata fuente
  requerido para la telemetría (coordinator/provider y project segment). El
  registro de los eventos METRIC permanece como responsabilidad del
  host/orchestrator bajo la arquitectura existente de artifacts de sesión.
  Este repositorio NO implementa un writer de `METRICS.md` dedicado para
  `reuse_event` ni `provider_cache_event`; por lo tanto, el seam
  productor→artifact es un límite de integración arquitectónico definido, no un
  camino de ejecución end-to-end implementado. No afirmar "fully connected",
  "end-to-end implemented" ni "producer integrated" respecto del writer
  persistente.

  Mapeo productor → catálogo (transformación que el host/orchestrator aplica al
  registrar el METRIC; documenta la dependencia de U4, no asumida):

  Transformación explícita, no implícita. Cada fila responde: ¿qué evento de
  runtime produce el dato?, ¿quién lo registra?, ¿en qué artifact?, ¿qué campo
  lo representa?, ¿puede ser UNKNOWN/Unavailable?, ¿qué clase de evidencia
  tiene?

  | Runtime source | RFC-72 concept | RFC-74 evento (campo) | Quién registra | Artifact | ¿UNKNOWN/Unavailable? | Clase de evidencia |
  | --- | --- | --- | --- | --- | --- | --- |
  | `cache_coordinator` — evento `cache eligible` | eligible | `reuse_event` (`layer=materialization`, `operation=eligibility`, `eligibility_decision=ACCEPTED`) | Orchestrator | `METRICS.md` | No (decisión binaria) | Recorded |
  | `cache_coordinator` — evento `cache admitted` | admitted | `reuse_event` (`operation=eligibility`, `eligibility_decision=ACCEPTED`, `reason=policy`) | Orchestrator | `METRICS.md` | No | Recorded |
  | `cache_coordinator` — evento `cache requested` | requested | `reuse_event` (`operation=reuse_attempt`) | Orchestrator | `METRICS.md` | No | Recorded |
  | `cache_coordinator.lookup` → `HIT`/`MISS`/`UNAVAILABLE` | hit / miss / unavailable | `reuse_event` (`operation=lookup`, `lookup_result=HIT|MISS`) + `provider_cache_event` (`result=hit|miss|unavailable`) | Orchestrator | `METRICS.md` | Sí — `UNAVAILABLE` cuando el adapter reporta unavailable | Recorded |
  | `ProviderResponse.cache_result` (`hit`/`miss`/`unavailable`) | hit / miss / unavailable | `provider_cache_event` (`result`) + `reuse_event` (`reuse_outcome=SUCCESSFUL|FAILED`) | Orchestrator | `METRICS.md` | Sí | Recorded |
  | `ProviderResponse.reference` | `ProviderCacheReference` | `provider_cache_event` (`reference_present=true|false`) | Orchestrator | `METRICS.md` | Sí (sin referencia → `false`) | Recorded |
  | MI change detectada | invalidación de materialización | `reuse_event` (`operation=post_use`, `invalidated=true`, `reason=identity`) | Orchestrator | `METRICS.md` | No | Recorded |
  | TTL/evicción/unavailable reportado por el adapter | provider invalidation / unavailable | `provider_cache_event` (`result=miss|unavailable`) o `reuse_event` (`reason=provider|availability`) | Orchestrator | `METRICS.md` | Sí | Recorded |

  | Runtime source (plan 90) | Concepto | RFC-74 evento (campo) | Quién registra | Artifact | ¿UNKNOWN/Unavailable? | Clase de evidencia |
  | --- | --- | --- | --- | --- | --- | --- |
  | `project_segment.reuse_eligibility` (`FRESH`/`STALE`/`UNKNOWN`) | freshness / reuse eligibility (RFC-73 §9) — NO es lookup ni eligibility decision | `reuse_event` (`layer=discovery|knowledge`) con `reason=availability` cuando aplica; NUNCA `lookup_result`/`eligibility_decision` derivados solo de freshness | Orchestrator | `METRICS.md` | Sí — `UNKNOWN` es un estado válido | Recorded (proxy de freshness documentado) |
  | `[entries] active/stale` + `.last_discovery` + manifest | oportunidad de Discovery reuse | derivación en el agregador (`discovery.reuse_opportunities`) | Agregador | reporte JSON (derivado) | No (count; 0 si no hay datos) | Derived |

  **Non-equivalencias normativas (D3):** `FRESH ≠ HIT`, `STALE ≠ MISS`,
  `UNKNOWN ≠ MISS`, `STALE ≠ REJECTED`, `FRESH ≠ ACCEPTED`. `freshness` es una
  propiedad de lifecycle/eligibility (RFC-73 §9); `HIT/MISS` es un resultado de
  lookup y `ACCEPTED/REJECTED` una decisión de eligibilidad/admisión (RFC-74
  §6). `reuse_eligibility` se registra como metadata/proxy de freshness
  (`reason=availability`), nunca como reinterpretación de `HIT/MISS` ni de
  `ACCEPTED/REJECTED`. No se crea un enum nuevo y no se modifica RFC-73.
- **RFC source:** `docs/rfc/74-cache-economics-telemetry-admission-evidence.md:28. Observability schema (requisitos)`,
  `:2. Estado actual de telemetría (FACT)`.
- **Why this target:** los eventos de provider/materialización solo existen
  cuando los planes 89/90 los implementan; esta unidad conecta productor y
  catálogo sin duplicar la semántica.
- **Dependencies:** planes 89/90 `Executed`; U1.
- **Behavior:** metadata pura; sin telemetría escrita por el runtime.
- **Tests:** unit del coordinator (si 89/90 están ejecutados); fixtures de
  sesión para el agregador.
- **Verification:** pytest + batería.
- **Rollback:** revertir el commit; los eventos registrados en sesiones son
  traza (no se editan).

### U5 — Gobernanza y traza (al ejecutar)

- RFC-74: entrada en `## Amendment Log` (implementada por plan 91) y corrección
  del "Impacto en el protocolo" de `## Alcance` (de "ninguno" a
  "materialización parcial por plan 91: eventos de reuse/cache en `METRICS.md`
  y catálogo en `PROTOCOL_METRICS.md`; sin thresholds ni gates").
- `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`: fila de la RFC-74
  actualizada según la aceptación.
- `CHANGELOG.md`: sección `[10.3.0]` con ítem `(plan 91, RFC-74)`.
- `protocol/.agents/VERSION`: `10.3.0` (con confirmación del usuario).
- Distinción explícita (no afirmar implicación): **Clase A NO implica MINOR ni
  MAJOR**. Clase A es la vía de autorización (RFC-74 `Accepted`); el bump se
  determina por compatibilidad (`docs/VERSIONING.md:3. Versionado`). Precedente:
  plan 88 (Clase A + MINOR 10.1.0) y plan 90 (Clase A + MINOR 10.2.0).

## Matriz RFC-74 → capa de implementación

| Concepto RFC-74 | Capa requerida | Archivo/módulo objetivo | Por qué | Dependencia |
| --- | --- | --- | --- | --- |
| Eventos de reuse/cache | contrato (aditivo) | `protocol/.agents/contracts/METRICS.md:Event catalog` | El catálogo canónico de eventos vive en el contrato | U1 |
| Catálogo de métricas por capa | standard | `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Metric catalog` | Owner del catálogo y de las clases de evidencia | U2 |
| Miss taxonomy | contrato + agregador | `METRICS.md` (`reason`) + `aggregate_metrics.py` | El `reason` se registra y se agrega | U1/U3 |
| Clases de evidencia | standard | `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Verifiability classes` (mapeo) | Sin taxonomía paralela | U2 |
| Aggregation | dev tool | `tools/aggregate_metrics.py` | Único consumidor mecánico del catálogo | U3 |
| Discovery reuse (derivación) | dev tool (Derived) | `aggregate_metrics.py` (`.last_discovery` + manifest) | Sin productor nuevo; datos existentes | U3 |
| Productores de provider/materialización | runtime | `cache_coordinator.py` + `project_segment.py` | Metadata/estado expuestos por planes 89/90; registro host/orchestrator (seam); se consume, no se duplica | U4 (planes 89/90 `Executed`) |
| Economics / I-ECO | standard (reglas sin umbrales) | `PROTOCOL_METRICS.md` (`### Reuse and cache economics`) | Normativa de medición, no policy de admisión | U2 |
| Measurement vs decision policy | NONE (regla) | `PROTOCOL_METRICS.md` | RFC-74 §7: evaluación económica no autoriza runtime | U2 |

## Matriz de state machines

| RFC | State machine existente | Cambio requerido | Por qué | ¿State machine nueva? |
| --- | --- | --- | --- | --- |
| RFC-74 | `SYSTEM_STATE_MACHINE.md`, `AGENT_STATE_MACHINE.md`, `DISCOVERY_STATE_MACHINE.md` | NONE | Los eventos se registran como METRIC (datos), no como transiciones; el modelo experimental de RFC-74 §32 es proceso de evaluación, no máquina de runtime | NO |

## Workers / Harness / Policies

- **Workers:** NONE — ningún worker nuevo; el Orchestrator registra eventos
  según la regla existente
  (`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Registration rules`).
- **Harness:** NONE — sin gates nuevos; las métricas siguen advisory
  (`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Aggregation`).
- **Policies/features.toml:** NONE — sin flags nuevos; la instrumentación es
  runtime/adapter, no configuración del protocolo (RFC-72 §6; RFC-74 §33).

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo: RFC-74
   `Accepted` (plan 93, 2026-08-31); RFC-71/72/73 `Accepted` (RFC-72/73 vía
   planes 87/92, en el working tree); planes 88/89/90 `Executed` (U4 incluida;
   re-verificar al ejecutar); estado actual de `METRICS.md` (`schema_version
   1.1.0` en ambas ocurrencias), `PROTOCOL_METRICS.md` y `aggregate_metrics.py`;
   batería inicial verde; rama `dev`.
1. **U1 — METRICS.md.** Bump `schema_version` a `1.2.0`; agregar los dos tipos
   de evento y el constraint de privacidad de una línea.
2. **U2 — PROTOCOL_METRICS.md.** Agregar `### Reuse and cache` y
   `### Reuse and cache economics` con el mapeo de clases de evidencia.
3. **U3 — aggregate_metrics.py.** Extender parseo/agregación y la derivación de
   Discovery reuse; tests.
4. **U4 — productores.** Planes 89/90 `Executed` (verificado al ejecutar):
   exponer la metadata de eventos según el mapeo explícito de U4; si la
   verificación encuentra que no están ejecutados, U4 queda fuera del commit y
   se documenta en la `Nota de ejecución` (el catálogo ya está definido) — no
   se crea un mecanismo tercero.
5. **U5 — gobernanza.** RFC-74 Amendment Log, `docs/rfc/INDEX.md`,
   `CHANGELOG.md` `[10.3.0]`, `protocol/.agents/VERSION` → `10.3.0` (con
   confirmación del usuario).
6. **Verificación.** Batería canónica + checklist semántico + H13 por juicio.
7. **Cierre.** Plan → `Executed` con `Nota de ejecución`; commit atómico en
   `dev` (Conventional Commit en inglés). Si la verificación de U4 fallara,
   `Executed (parcial: U4 pendiente)`.

## Tests y verificación

- **Runtime behavioral tests:** `tests/test_aggregate_metrics.py` (eventos
  nuevos, derivación de Discovery reuse, doble conteo ausente, eventos
  desconocidos ignorados); unit del coordinator si U4 aplica.
- **Protocol structural checks:** batería canónica
  (`docs/VERSIONING.md:4.1 Batería canónica de verificación`); el checker de
  sesión valida los eventos nuevos con fixtures.

**Matriz de tests requeridos (requerimiento → invariant → test):**

| Requerimiento | Invariant / contrato | Test exigido |
| --- | --- | --- |
| Compatibilidad de eventos desconocidos | `protocol/.agents/contracts/METRICS.md:Constraints` (unknown ignored) | `test_aggregate_metrics`: eventos desconocidos ignorados, sin error |
| Parsing de eventos nuevos | U1 (schema 1.2.0) | `test_aggregate_metrics`: `reuse_event`/`provider_cache_event` parseados y agregados |
| Disponibilidad provider-dependent | I-ECO-006 | Test: métricas provider-dependent marcadas `Unavailable` sin adapter real; no generalizadas |
| Clasificación de evidencia | I-ECO-005 | Test: cada métrica del reporte con su clase (Recorded/Verified/Derived) y disponibilidad |
| Aislamiento de capas | I-ECO-003, I-ECO-006 | Test: capas discovery/knowledge/materialization/provider agregadas por separado |
| Sin doble conteo | I-ECO-004 | Test: suma por capa; ausencia de total global que sume capas distintas |
| Sin admisión económica | I-ECO-001 | Test: el agregador no produce gates ni admisión; ninguna métrica admite/rechaza reuse |
| Hit rate ≠ valor económico | I-ECO-002 | Test: ausencia de métrica `hit_rate`/`savings` global en el reporte |
| Append-only | `protocol/.agents/contracts/METRICS.md:Constraints` (RFC-46) | Test: el agregador no modifica artifacts de sesión (solo lectura) |
| Corrupt handling | `protocol/.agents/contracts/METRICS.md:Constraints` | Test: comentarios corruptos contados como corrupt, no descartados en silencio |

**Fuerza de evidencia de los tests (C-4):**

| Nivel | Cobertura |
| --- | --- |
| A — E2E / productor real → artifact | **NONE** |
| B — integración productor → artifact | **NONE** |
| C — unit / in-process | **PRESENT** (agregador, metadata del coordinator, checker) |
| D — fixture sintético | **PRESENT** (eventos inyectados en `METRICS.md` de fixtures) |

Razón arquitectónica: el registro de eventos METRIC es responsabilidad del
host/orchestrator y no existe un writer de referencia en este repositorio. Los
tests demuestran que el contrato, el checker y el agregador procesan
correctamente eventos de telemetría válidos; **NO demuestran que las
operaciones de runtime generen y persistan automáticamente esos eventos en
`METRICS.md`**. No se declara cobertura E2E inexistente (no false closure).

- **Semantic verification (juicio manual):**

| Check | Mecanismo |
|---|---|
| Sin thresholds/gates | Ausencia de umbrales numéricos en el diff de standards/contratos |
| Sin doble conteo | Métricas por capa separadas; I-ECO-004 declarado |
| Frontera RFC-72/73 intactas | Sin redefiniciones de identidad/materialización/persistence en el diff |
| Privacy preservada | Eventos con identificadores/cantidades únicamente |
| Hit rate ≠ valor económico | I-ECO-002 normativo; sin métrica `hit_rate` primaria |
| Sin telemetry framework nuevo | Solo extensión del catálogo existente |
| Sin pricing ni billing | Ausencia de `CostModel`/`PricingModel`/`ProviderPricing`/price tables/precios en el diff |
| Métricas no instrumentadas | Checklist del catálogo (U2) contra RFC-74 §10/§11: declaradas `Unavailable` |

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

`check_dist_sync` rojo por diseño en `dev`; verde solo en `master`.

## Failure modes

Los modos de fallo afectan la **confiabilidad de la medición**, nunca la
correctness del runtime (RFC-74 §30): no se convierten en mecanismos de runtime
ni en políticas de recovery nuevas. Donde RFC-74 o los contratos existentes no
definen recovery, se declara `UNSPECIFIED`.

| Modo | Tratamiento | Recovery definido por |
| --- | --- | --- |
| Provider no reporta cache status | Sin `cache_result` → sin evento o `result=unavailable`; `lookup_result` ausente | RFC-72 §13 (degradación de optimización) / RFC-74 §30 (limitación) |
| Provider reports unavailable | `provider_cache_event` (`result=unavailable`) | RFC-72 §13 |
| Telemetry data unavailable | Métricas declaradas `Unavailable` en la columna Availability; sin data point fabricado | RFC-74 §30 (limitación) |
| Event duplication / retry duplication | Contados como eventos; corrección con evento posterior, nunca edición (append-only) | `protocol/.agents/contracts/METRICS.md:Constraints`; RFC-46 |
| Event loss | Sin re-construcción retroactiva | `protocol/.agents/contracts/METRICS.md:Constraints` (append-only); recovery **UNSPECIFIED** |
| Clock skew | Campo `clock: utc/agent_clock` existente (G-004) | `protocol/.agents/contracts/METRICS.md:Constraints`; RFC-74 §30 |
| Pricing unavailable | Costo monetario `Unavailable`; sin pricing ni billing | RFC-74 §4/§25/§26 |
| Escritura de telemetría fallida | No definido por RFC-74; el artifact es append-only | **UNSPECIFIED** (sin recovery inventado) |
| Restart de sesión/proceso | Los eventos no se re-emiten | **UNSPECIFIED** (sin re-emisión inventada) |
| Adapter failure | Degrada optimización, nunca correctness; `unavailable` | RFC-72 §13 |

Distinción central: `measurement unavailable` ≠ `runtime correctness failure`.
Un dato faltante o `Unavailable` jamás invalida un contexto semántico, nunca
admite/rechaza reuse y nunca modifica el resultado de una ejecución.

## Source of truth

Se preservan las fuentes de verdad sin mezcla. Nunca: telemetry → Project
Segment, telemetry → KB, telemetry → `SemanticContextIdentity`, telemetry →
`MaterializationIdentity`, telemetry → `ProviderCacheReference`.

| Dato | Fuente de verdad | Clasificación |
| --- | --- | --- |
| Eventos de sesión registrados | `METRICS.md` (artifact de sesión, append-only) | Source of truth (recorded telemetry) |
| Conocimiento de proyecto | manifest + entradas de la KB de discovery | Source of truth (project knowledge) |
| `project_segment.json` | derivado de la KB | Derived metadata (nunca autoritativo) |
| Reportes del agregador | derivados de eventos + KB | Derived analytical output |
| Estado de cache del provider | provider/adapter (opaco) | External fact; no es source of truth del protocolo |

## Migración

Sesiones y proyectos existentes: **sin migración de datos**. Los eventos nuevos
solo aparecen en sesiones posteriores a la versión; los agregadores viejos
ignoran tipos desconocidos (`protocol/.agents/contracts/METRICS.md:Constraints`);
los artifacts de sesión son inmutables (RFC-46) y no se reescriben. No hay
cambios de formato de persistence ni de discovery.

## Rollback

- **Code rollback:** `git revert` del commit del plan (contrato + standard +
  agregador + gobernanza).
- **Data rollback:** NONE — los eventos registrados en sesiones son traza
  inmutable (RFC-46); el rollback detiene el registro futuro, no edita lo
  registrado.
- **Protocol rollback:** revertir `schema_version` y filas de `METRICS.md`/
  `PROTOCOL_METRICS.md`; VERSION/changelog revertidos en el mismo commit.
- **Cache/provider state:** NONE — RFC-74 no crea estado de provider.

## Riesgos

- **Convertir métricas en gates.** Mitigación: "No metric gates anything" y
  I-ECO-001/002 explícitos; sin thresholds.
- **Doble conteo de ahorro.** Mitigación: métricas por capa con `layer`;
  I-ECO-004 testeado en el agregador.
- **Confundir `hit` con validez o con Project Knowledge.** Mitigación:
  I-ECO-003 + semántica de RFC-72 §9 citada en el contrato.
- **Taxonomía de evidencia paralela.** Mitigación: mapeo a las Verifiability
  classes existentes; sin clases nuevas.
- **Scope creep hacia telemetry framework.** Mitigación: extensión del
  catálogo existente; sin dashboards ni backends.
- **Versionado mal clasificado.** Mitigación: MINOR con evidencia (aditivo,
  compatible por la regla de eventos desconocidos); confirmación del usuario.

## Impacto en prompt caching

Este plan mide, no optimiza: no reduce tokens ni costo por sí mismo; habilita
la evidencia que RFC-68 exige para decidir la Fase 2 de cache
(`docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`).
Las métricas de provider dependen de los adapters del plan 89 y las de
knowledge/discovery de los productores del plan 90; el Context Budget
permanece autoritativo (I-ECO;
`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:8. Interaction with caching and persistence`).

## Versionado

- **Clase A** = vía de autorización (RFC-74 `Accepted`; RFC-56). No es bump.
  Clase A NO implica MAJOR ni MINOR: la clase es la vía de autorización
  (RFC-56); el bump es impacto de compatibilidad
  (`docs/VERSIONING.md:3. Versionado`). Precedente: planes 88 y 90 (ambos
  Clase A, ambos MINOR).
- **Bump:** adición compatible de tipos de evento al contrato `METRICS.md`
  (compatibilidad garantizada por la regla de eventos desconocidos) + filas
  nuevas en el catálogo → **MINOR** (`docs/VERSIONING.md:3. Versionado`).
- **Transición esperada al ejecutar:** `protocol/.agents/VERSION` `10.2.0` →
  `10.3.0` (asignación serial: `10.1.0` = plan 88, `10.2.0` = plan 90;
  `docs/VERSIONING.md:8. Ejecución en paralelo`), con confirmación del usuario
  (MINOR).
- Respuesta única: **Clase A (RFC-74 Accepted) + MINOR 10.3.0**.

## Grafo de dependencias

```text
RFC-71 Accepted (plan 86) ── plan 88 Executed (10.1.0)
        │
        ▼
RFC-72 Accepted ──► plan 89 Executed ──┐
RFC-73 Accepted ──► plan 90 Executed ──┴──► U4 productores (metadata de eventos)
        │
        ▼
RFC-74 Accepted (plan 93, 2026-08-31) ──► gate de gobernanza cumplido
        │
        ▼
Plan 91 (este plan)
        ├── U1 METRICS.md (schema 1.2.0, eventos) ──► U2 PROTOCOL_METRICS.md
        │        └──► U3 aggregate_metrics.py ──► tests
        └── U4 productores (gated a planes 89/90 Executed) ──► U5 gobernanza

U1–U3 son schema-first y no dependen de 89/90; U4 depende de planes 89/90
`Executed` (cumplidos). Sin otras dependencias.
```

## Trazabilidad

`docs/rfc/74-cache-economics-telemetry-admission-evidence.md:2. Estado actual de telemetría (FACT)` +
`:6. Reuse value` + `:8. Cache/reuse metrics` + `:9. Miss taxonomy` +
`:24. Double Counting Prevention` + `:27. Provider-dependent vs independent metrics` +
`:28. Observability schema (requisitos)` + `:29. Privacy / data minimization` +
`:31. Confidence / evidence quality` + `:33. Ownership` + `:34. Matrices` +
`:35. Invariantes` → Plan 91 → U1…U5. RFC-74 no redefine RFC-71/72/73; este
plan mide sus mecanismos sin tocar su semántica.

**Trazabilidad por unidad (RFC → requisito → archivo → test → criterio de salida):**

| Unidad | RFC section | Requisito del plan | Archivo | Test | Criterio de salida |
| --- | --- | --- | --- | --- | --- |
| U1 | RFC-74 §6, §9, §28, §29 | Eventos `reuse_event`/`provider_cache_event`; schema 1.2.0; compatibilidad aditiva; costo Unavailable | `protocol/.agents/contracts/METRICS.md` | `check_session_artifacts` con fixtures | Contrato `1.2.0`; eventos registrados; unknown ignorados |
| U2 | RFC-74 §8, §27, §31, §34, §35 | Catálogo por capa; clases de evidencia; I-ECO sin umbrales; métricas Unavailable declaradas | `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` | Batería canónica + checklist semántico | Catálogo `### Reuse and cache` + economía; clasificación explícita por métrica |
| U3 | RFC-74 §2, §8, §9, §13 | Agregación por capa; derivación Derived; sin doble conteo | `tools/aggregate_metrics.py` | `tests/test_aggregate_metrics.py` | Agregador procesa eventos nuevos; sin cross-layer sum |
| U4 | RFC-72 §14; RFC-74 §28; planes 89/90 | Productores expuestos como metadata/estado; mapeo explícito (host); seam declarado; sin mecanismo tercero; FRESH ≠ HIT | `runtime/toolcalls/cache_coordinator.py` + `runtime/toolcalls/project_segment.py` (solo lectura de metadata) | Unit del coordinator + fixtures de sesión | Mapeo documentado; non-equivalencias D3; sin duplicación de planes 89/90; sin writer de referencia |
| U5 | RFC-74 Amendment; `docs/VERSIONING.md:3. Versionado` | Gobernanza: Amendment Log, INDEX, changelog, VERSION 10.3.0 | RFC-74, `docs/rfc/INDEX.md`, `CHANGELOG.md`, `protocol/.agents/VERSION` | Batería + `check_version_state` | VERSION 10.3.0 MINOR; plan `Executed`; commit atómico |

## Criterios de salida

- [ ] `METRICS.md` con `schema_version` `1.2.0` (ambas ocurrencias) y los tipos
      `reuse_event`/`provider_cache_event` registrados en `## Event catalog`.
- [ ] Eventos desconocidos y campos extra siguen ignorados (compatibilidad
      preservada; verificado por test).
- [ ] `PROTOCOL_METRICS.md` con `### Reuse and cache` y `### Reuse and cache
      economics`; cada métrica con clase de evidencia, disponibilidad, scope y
      provider dependency; dimensiones no instrumentadas declaradas
      `Unavailable`.
- [ ] `aggregate_metrics.py` procesa los eventos nuevos; agregación por capa;
      sin doble conteo cross-layer (test); sin métrica global `cache_hit` ni
      `savings`.
- [ ] U4 aplicada: productores de planes 89/90 expuestos como metadata/estado;
      mapeo explícito documentado; seam host/orchestrator declarado (sin writer
      de referencia); FRESH/STALE/UNKNOWN no reinterpretados como HIT/MISS/
      ACCEPTED/REJECTED.
- [ ] I-ECO-001…I-ECO-006 cubiertos por tests (matriz de `## Tests y
      verificación`).
- [ ] Sin pricing, sin billing, sin `CostModel`/`PricingModel`/`ProviderPricing`,
      sin price tables, sin thresholds, sin telemetry backend, sin
      infraestructura experimental (verificado por diff).
- [ ] Sin redefiniciones de RFC-72/73; sin cambios en Discovery, state
      machines, workflows, roles, harness ni `features.toml`.
- [ ] Batería canónica en verde; pytest sin fallos ajenos.
- [ ] RFC-74 con Amendment Log e "Impacto en el protocolo" corregido;
      `docs/rfc/INDEX.md` actualizado; `CHANGELOG.md` `[10.3.0]` +
      `protocol/.agents/VERSION` `10.3.0` (MINOR, con confirmación del usuario).
- [ ] RFC-74 `Accepted` como criterio de entrada cumplido antes de ejecutar.
- [ ] Plan → `Executed` con `Nota de ejecución`; commit atómico en `dev`
      (Conventional Commit en inglés).

## Nota de ejecución

Se completa al ejecutar, con fecha, verificación realizada y resultado. Si el
gate RFC-74 `Accepted` no está cumplido, el plan permanece `Aprobado para
ejecución` y NO se ejecuta (`docs/VERSIONING.md:7. Estados de planes y RFCs`).
Si los planes 89/90 no están `Executed`, ejecutar solo U1–U3/U5 y registrar
`Executed (parcial: U4 pendiente de planes 89/90)`.

**2026-08-31 — Plan hardening (sin ejecución).** Auditoría de implementabilidad
de RFC-74 completada; este plan se corrigió documentalmente para eliminar
ambigüedades: (1) **D1** — costo monetario/pricing/billing declarado
`Unavailable` y non-goal explícito (sin `CostModel`/`PricingModel`/
`ProviderPricing`/price tables/precios hardcodeados); (2) **D2** —
clasificación explícita Observed/Estimated/Derived/Unavailable por métrica y
lista de dimensiones de RFC-74 §10/§11 no instrumentadas (Unavailable);
(3) **D3** — non-equivalencias FRESH/STALE/UNKNOWN vs HIT/MISS/ACCEPTED/REJECTED
documentadas y mapping de U4 corregido (freshness = metadata `reason`, nunca
reinterpretación de lookup/eligibility); (4) **event mapping** de U4 explícito
(runtime source → RFC-72 concept → RFC-74 field → quién registra → artifact →
UNKNOWN/Unavailable → clase de evidencia); (5) dependencias tipadas (normativa /
implementación / gate), failure modes, source of truth, non-goals, trazabilidad
por unidad y criterios de salida verificables agregados. No se ejecutó este
plan; no se modificaron `runtime/`, `protocol/.agents/`, `tests/`, RFC-74,
VERSION ni CHANGELOG por este hardening. Estado: `Aprobado para ejecución`.
- 2026-08-31 — **Ejecutado** en el working tree sobre `dev` (commit atómico
  pendiente de decisión del mantenedor: los archivos de gobernanza compartidos
  están entrelazados con cambios preexistentes de los planes 87/92/93; ver
  `docs/plans/INDEX.md` y el reporte de ejecución). U1–U5 completados:
  - **U1** `protocol/.agents/contracts/METRICS.md`: `schema_version` 1.2.0
    (ambas ocurrencias); `reuse_event` y `provider_cache_event` en el event
    catalog; constraint de privacidad; notas de identidad (entry key existente,
    sin identidad nueva) y costo (`Unavailable`; sin pricing).
  - **U2** `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`: `### Reuse
    and cache` (tabla con Evidence class / Availability / Scope / Provider
    dependency / Invariant), clasificación Observed/Estimated/Derived/
    Unavailable, dimensiones Unavailable (latencia, tokens, costo, budget
    rejected, storage) y `### Reuse and cache economics` (I-ECO-001…I-ECO-006
    sin umbrales).
  - **U3** `tools/aggregate_metrics.py`: parsing de los eventos nuevos;
    agregación layer-specific sin métrica global `cache_hit`/`savings` y sin
    doble conteo (I-ECO-004); reporte de `evidence.classes`/`evidence.availability`;
    derivación `discovery.reuse_opportunities` (Derived) desde `.last_discovery`
    + manifest; unknown ignored / corrupt counted preservados.
  - **U4** metadata/estado de planes 89/90 expuestos (`cache_coordinator.events`
    + `project_segment.reuse_eligibility`) y mapeo host/orchestrator
    documentado; sin cambios en `runtime/`; sin writer de METRICS en este
    repositorio (seam); sin mecanismo tercero; FRESH/STALE/UNKNOWN ≠
    HIT/MISS/ACCEPTED/REJECTED (mapping documentado y testeado).
  - **U5** `protocol/.agents/VERSION` → `10.3.0` (MINOR, autorizado por el
    mantenedor al ejecutar); `CHANGELOG.md` `[10.3.0]`; RFC-74 Amendment Log e
    "Impacto en el protocolo" (implementada por plan 91, distinguida de la
    aceptación del plan 93); `docs/rfc/INDEX.md`; `docs/plans/INDEX.md`.
  - Soporte: `tools/check_session_artifacts.py` (METRIC_REQUIRED con los tipos
    nuevos) y tests nuevos en `tests/test_aggregate_metrics.py` (I-ECO-001…006,
    no double counting de provider cache HIT, FRESH/STALE/UNKNOWN ≠ HIT/MISS,
    Unavailable sin fabricación, unknown ignored, append-only, corrupt) y
    `tests/test_check_session_artifacts.py` (fixtures de eventos nuevos).
  Verificación: los seis checkers de la batería canónica en verde
  (`check_protocol_invariants` 212 files / 9716 refs, `check_plan_citations`,
  `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`,
  `check_version_state`) y `python -m pytest tests/` con **331 passed** (basetemp
  fresco por la ACL del `pytest-of-rolda` por defecto en sandbox Windows, mismo
  workaround que los planes 87/89/90/92/93). `check_dist_sync` rojo por diseño
  en `dev`. Sin pricing, sin billing, sin thresholds, sin telemetry backend, sin
  infraestructura experimental, sin identidades nuevas, sin cambios en Discovery
  ni en state machines; RFC-71/72/73 consumidas sin redefinirse. No se ejecutó
  ningún otro plan.

**2026-08-31 — Post-execution hardening (C-1…C-4, corrección documental/
semántica; no es una nueva versión).**

```text
IMPLEMENTED:
- telemetry contract (METRICS.md 1.2.0)
- event schema (reuse_event / provider_cache_event)
- evidence classification (Observed / Estimated / Derived / Unavailable)
- aggregator (layer-specific, dimension-specific, sin doble conteo)
- checker (validación de forma de los eventos)
- derived discovery metric (discovery.reuse_opportunities, Derived)

EXISTING RUNTIME SOURCES:
- provider cache metadata (cache_coordinator / ProviderResponse)
- project knowledge freshness / reuse eligibility
  (project_segment.reuse_eligibility: FRESH / STALE / UNKNOWN)
- existing discovery artifacts (.last_discovery + manifest)

NOT IMPLEMENTED:
- host/orchestrator METRICS writer
- runtime → METRICS.md automatic event persistence
```

El seam productor→artifact es un límite de integración arquitectónico
documentado (responsabilidad del host/orchestrator bajo la arquitectura
existente de artifacts de sesión), no un fallo de RFC-74 ni una desviación
nueva de este plan. `discovery.reuse_opportunities` queda definida como métrica
derivada basada en estado (C-2): no es conteo de lookup/reuse/cache-hit ni de
eventos observados; ausencia de artifacts/metadata inválida → `Unavailable`
(`None`), `0` solo con evidencia válida de cero entradas frescas (C-3). La
estrategia de tests declara la fuerza de evidencia A/B/C/D (C-4): sin cobertura
E2E del writer, que no existe en este repositorio. `protocol/.agents/VERSION`
permanece `10.3.0`; sin bump nuevo.
