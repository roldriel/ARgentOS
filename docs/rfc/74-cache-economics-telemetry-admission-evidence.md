# RFC-74 — Modelo de economía del cache, telemetría y evidencia de admisión

**Status:** Accepted (plan 93, 2026-08-31)
**Fecha:** 2026-08-29
**Serie:** Context Persistence & Prompt Cache (RFC-A…RFC-D)
**Origen:** RFC-71 (Context Persistence & Cacheability), RFC-72 (Provider Prompt Cache Capability), RFC-73 (Project & Discovery Context Persistence) y estado actual de telemetría del repo: `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Purpose`, `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`, `docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`.
**Pregunta:** ¿Cómo puede ARgentOS medir si persistence, memoization y Provider Prompt Cache realmente reducen costo y latencia sin degradar correctness, freshness, calidad o aislamiento?
**Afectados:** —

> Convención de evidencia: las afirmaciones sobre el estado actual del repo se
> citan con `ruta:sección`; las capacidades que esta RFC exige pero que no
> existen hoy se marcan como **Requisito de implementación futura**; las
> métricas no obtenibles hoy se marcan como **Measurement limitation**. Esta
> RFC no modifica la semántica de RFC-71/72/73: solo define cómo medirla y
> evaluarla.

## Problema

1. **La telemetría actual mide proceso, no economía.** El catálogo de `PROTOCOL_METRICS.md` registra transiciones, delegaciones, fallos, flags y budget declarado/consumido (`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Metric catalog`); no existen input/output/cached tokens, latencia por request, costo de provider, ni conteo de invocaciones LLM por sesión (`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Purpose`). La investigación de costo concluyó que la magnitud de cada fuente de costo es desconocida y que una RFC de memoización/cache carece de justificación sin telemetría (`docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`).

2. **El propio repo gatea la implementación de cache a telemetría.** RFC-68 define que cachear re-lectura es Fase 2 gateada a telemetría (`docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`). RFC-74 es el contrato de medición que habilita ese gate.

3. **Sin modelo de atribución, un "hit" puede leerse como ahorro sin serlo.** Un hit del provider, un reuse de discovery y un reuse de Project Knowledge son mecanismos distintos con costos distintos; mezclarlos en una sola métrica `cache_hit` produce falsa economía.

4. **RFC-71/72/73 definen qué puede cachearse, persistirse y materializarse; nadie define todavía cómo medir si vale la pena.** Esta RFC llena esa capa sin redefinir las anteriores.

## Modelo

### 1. Principio fundamental

**Decisión:** la economía es una dimensión de evaluación subordinada a `correctness`, `isolation`, `freshness`, `provenance`, `policy` y `Context Budget`. No se convierte:

```text
cache hit    → correctness
cache miss   → invalid knowledge
higher hit rate → better system
```

La pregunta central de esta RFC no es "¿cuántos cache hits tenemos?" sino "¿cuánto trabajo/costo evitamos realmente, cuál fue el overhead de conseguir ese ahorro, y podemos demostrar que la optimización no degradó correctness, freshness, isolation ni calidad?".

### 2. Estado actual de telemetría (FACT)

#### Señales encontradas

| Signal | Source | Current availability | Granularity | Reliability | Owner |
| --- | --- | --- | --- | --- | --- |
| Transiciones de estado | `METRICS.md` events (`state_transition`) | Disponible | por evento | Recorded | Orchestrator |
| Delegaciones | `METRICS.md` events (`delegation`) | Disponible | por delegación | Recorded | Orchestrator |
| Fallos por clase | `METRICS.md` events (`failure`) | Disponible | por evento | Recorded | Orchestrator |
| `context.budget_declared/consumed` | `METRICS.md` events (`context_budget`); medidor dev `tools/measure_context_budget.py` | Definido (catálogo) y medible; **no registrado en la muestra real** (`docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`) | por delegación | Verified (si se registra) | Orchestrator / runtime |
| `session.duration_ms` | agregador dev `tools/aggregate_metrics.py` (timestamps de HARNESS/METRICS) | Disponible pero poco confiable (valores 0 o mezcla de relojes en la muestra) | por sesión | Recorded | Orchestrator / agregador |
| `model_used`, `execution_time_seconds` (discovery) | `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections` ([runtime]) | Opcional, solo manifest de discovery | por run | Recorded (si se declara) | Discovery |
| Flags evidenciados | `METRICS.md` events (`flag_evidence`) | Disponible | por sesión | Recorded | Orchestrator |

#### Señales NO disponibles

```text
input tokens            → NOT CURRENTLY AVAILABLE
output tokens           → NOT CURRENTLY AVAILABLE
cached tokens           → NOT CURRENTLY AVAILABLE
prompt cache hit/miss   → NOT CURRENTLY AVAILABLE
latency por request     → NOT CURRENTLY AVAILABLE
provider cost / model cost → NOT CURRENTLY AVAILABLE
LLM invocation count por sesión/fase → NOT CURRENTLY AVAILABLE
retry count por fase (métrico) → DERIVABLE FROM EXISTING ARTIFACTS (HARNESS_REPORT: prior FAIL entries por trigger; `protocol/.agents/harness/INDEX.md:Recovery Mechanism`)
discovery recomputation cost → PARCIAL (model_used/execution_time_seconds opcionales)
reuse / memoization counters → NOT CURRENTLY AVAILABLE
```

**Measurement limitation:** las métricas de tokens, latencia y costo del provider dependen del runtime y del provider; no pueden obtenerse hoy desde el protocolo.

### 3. Capas de economía

**Decisión:** se separan cinco capas, no confluibles:

```text
Discovery economics              → costo de discovery/revalidación/reuse
Project Knowledge reuse economics → valor del conocimiento persistido reutilizado
Context Composition economics     → costo de componer/validar/seleccionar contexto
Materialization economics         → costo de materializar (RFC-72)
Provider Prompt Cache economics   → tokens/latencia/costo del cache del provider
```

`Discovery saved work` y `Provider cache saved tokens` representan mecanismos distintos y **no** se suman como el mismo ahorro.

### 4. Modelo de costo

**Decisión:** modelo abstracto, sin precios concretos:

```text
Baseline Cost   = costo esperado/observado sin la optimización evaluada
Avoided Cost    = parte del baseline realmente evitada
Reuse Overhead  = costo incremental introducido por obtener/usar/mantener el reuse
                  (retrieval, validation, storage, maintenance, materialization,
                   provider-specific overhead)
Net Benefit     = dimension-specific Avoided Cost − Reuse Overhead correspondiente
```

Cada costo tiene **un único lugar de atribución**; `Reuse Overhead` no es una bolsa que duplique componentes ya contabilizados. Se distinguen unidades no intercambiables:

```text
token cost          (tokens)
latency cost        (tiempo)
compute cost        (cómputo local)
provider monetary cost (precio; provider-dependent)
engineering/storage cost (mantenimiento/almacenamiento)
```

`Net Benefit` es **dimension-specific**: no se mezclan tokens, ms, USD ni storage como si fueran la misma unidad. Solo se introducen las variables necesarias para responder la pregunta de §1; ninguna es un threshold.

### 5. Avoided Work

**Decisión:** **Avoided Work** es el trabajo (cómputo, tokens, latencia, dinero) que una optimización evita realmente respecto de un baseline comparable. **No es equivalente a un cache hit**:

```text
cache hit
+ expensive retrieval / validation
+ large cache maintenance
= possibly no economic benefit
```

Regla central:

```text
Hit Rate ≠ Economic Value
```

### 6. Reuse value

**Decisión:** se definen los eventos de reuse medibles con tres niveles de vocabulario, sin política de umbral:

```text
Lookup result        → HIT / MISS
Eligibility decision → ACCEPTED / REJECTED
Reuse outcome        → SUCCESSFUL / FAILED
Post-use lifecycle   → INVALIDATED
```

```text
lookup → HIT/MISS → candidate evaluation → ACCEPTED/REJECTED
       → reuse attempt → SUCCESSFUL/FAILED → possibly INVALIDATED later
```

`Hit/Miss` **no** significa semantic validity, eligibility ni successful reuse. `ACCEPTED/REJECTED` pertenece a la decisión de elegibilidad; `SUCCESSFUL/FAILED` al resultado del reuse; `INVALIDATED` a un evento de lifecycle posterior. No se establece `reuse >= N` (rechazado en RFC-71/73; se preserva).

### 7. Admission evidence

**Decisión:** se separan dos conceptos:

```text
Semantic admissibility → determina si el reuse está semánticamente permitido
                         (validity + freshness + provenance + scope + policy + budget)
Economic evaluation    → determina si persistence/reuse parece económicamente beneficioso
```

Regla normativa:

```text
Semantic validity MUST precede Economic evaluation.
Economic evidence informs future admission policy.
```

RFC-74 **no define un economic admission gate**: la evaluación económica es una capa observacional/evaluativa; puede informar una futura policy de admisión, pero **no autoriza por sí misma persistence ni reuse en runtime**. Un artifact puede ser semánticamente válido y económicamente no digno de persistir; un artifact económicamente atractivo pero semánticamente inválido **nunca** se admite.

### 8. Cache/reuse metrics

**Decisión:** métricas independientes por capa; no existe un único `cache_hit`:

```text
Discovery reuse hit
Project Knowledge reuse hit
Materialization reuse
Provider Prompt Cache hit
Provider Prompt Cache miss
```

```text
Discovery reuse ≠ Knowledge reuse ≠ Materialization reuse ≠ Provider Prompt Cache hit
```

La semántica hit/miss de RFC-72 se mantiene: hit/miss del provider no determina validez semántica (`docs/rfc/72-provider-prompt-cache-capability.md:9. Semántica de hit / miss`).

**Decisión (materialization reuse):** `Materialization reuse = reuse of an RFC-72-defined materialization artifact/reference`. RFC-74 mide `materialization reuse opportunity`, `materialization lookup`, `materialization hit/miss` y `materialization reuse outcome`, pero **no redefine** `MaterializationIdentity`, Canonical Materialization, Stable Prefix ni `ProviderCacheReference` (owner: RFC-72).

### 9. Miss taxonomy

**Decisión:** taxonomía de misses, sin inventar causas no observables:

```text
semantic miss      (candidato inválido)
policy miss        (candidato rechazado por policy)
budget miss        (candidato excede Context Budget)
identity miss      (mismatch de identidad)
provider miss      (cache del provider: miss/unavailable/eviction)
availability miss  (artifact no persistido/disponible)
```

Un miss de una capa no es miss de otra; un miss del provider nunca es invalidación semántica (RFC-72).

### 10. Latencia

**Decisión:** medir, no asumir:

```text
baseline latency
reuse latency
cache lookup latency
validation latency
materialization latency
provider request latency
```

Se definen `latency saved`, `latency overhead` y `net latency benefit`. Un cache hit **no** implica menor latencia; debe medirse.

### 11. Token economics

**Decisión:** medición de:

```text
baseline input tokens
reused input tokens
output tokens
cached/prompt-cache tokens
tokens avoided
tokens spent validating/retrieving cache
```

La disponibilidad de estas métricas es **provider-dependent**; `token reduction ≠ monetary savings` sin pricing. La estimación local usa la regla existente `ceil(chars/4)` (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:2. Estimation rule`) solo como estimación, no como factura.

### 12. Context Budget economics

**Decisión:** se respeta `persisted knowledge ≠ free context` (RFC-73, sección 13). Se miden, cuando sea posible:

```text
context bytes/chars/tokens
budget allocated
budget consumed
budget rejected
```

Pregunta que esta capa debe poder responder: "¿cuánto conocimiento persistido termina entrando realmente en contexto y cuánto costo produce?" No se modifica Context Budget (`protocol/.agents/standards/context/CONTEXT.md:3. Knowledge Base context budgets`).

### 13. Discovery economics

**Decisión:** evaluar por separado `full discovery`, `partial discovery`, `revalidation`, `reuse` y `no-op`:

```text
Discovery reuse     → evita trabajo LLM de discovery
Provider Prompt Cache → puede reducir procesamiento repetido del prompt
```

`discovery avoided ≠ provider cache avoided`; no se mezclan en una métrica única. El manifest ya puede declarar `model_used`/`execution_time_seconds` (opcional; `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`).

### 14. Revalidation economics

**Decisión:** medir `cost of revalidation` y `value of reuse after revalidation`, de modo que se pueda detectar `revalidation cost > avoided recomputation cost` sin imponer un threshold universal (RFC-73, sección 9).

### 15. Storage economics

**Decisión:** medir (si corresponde) `persisted artifact size`, `number of persisted artifacts`, `retention`, `storage growth` y `GC`; `storage overhead` se mantiene **separado** de `LLM token cost`. No se asume que el storage sea económicamente relevante en todos los providers.

### 16. Quality / correctness guardrail

**Decisión:** métricas para detectar `economic optimization → quality regression`:

```text
reuse acceptance
revalidation failure
stale reuse attempt
invalid reuse attempt
incorrect context reuse
```

No se inventa una métrica de "quality" sin evidencia del repo; donde no exista, se declara **measurement requirement**.

### 17. False Economy

**Decisión:** la optimización debe evaluarse **end-to-end**. Casos explícitos:

```text
high hit rate, negligible savings
large persistence, little reuse
frequent invalidation, expensive storage
cheap cache, expensive validation
provider cache hit, Context Composition sigue cara
reduced tokens, increased latency
reduced latency, increased provider cost
```

### 18. Experiment model

**Decisión:** marco experimental sin thresholds numéricos:

```text
Baseline
Treatment
Control
Observation window
Workload
Metrics
Confounders
Success criteria
Rollback criteria
```

Los criterios de éxito/rollback son descripciones cualitativas hasta que los datos los calibren.

### 19. Baseline

**Decisión:** toda evaluación económica requiere un baseline comparable:

```text
sin Discovery reuse        vs  con Discovery reuse
sin Project Knowledge reuse vs  con Project Knowledge reuse
sin Provider Prompt Cache  vs  con Provider Prompt Cache
```

No todos los baselines son ejecutables hoy (Measurement limitation).

### 20. Experiment isolation

**Decisión:** los experimentos deben distinguir Discovery reuse, Project Knowledge reuse y Provider Prompt Cache; si varias optimizaciones cambian a la vez, el experimento se etiqueta como **combined treatment** y no se atribuye el ahorro a una sola.

### 21. Metric hierarchy

**Decisión:**

```text
Economic dimensions: monetary cost, token consumption, latency, compute, storage
Safety constraints:  correctness, freshness, provenance, isolation
```

Cada experimento define su **experiment-specific primary metric** según su objetivo (p. ej., provider monetary cost, end-to-end latency o input tokens); no existe una prioridad universal `economic value > latency > tokens`. Las safety constraints no son objetivos económicos: son condiciones que **no pueden violarse**. `Economic optimization MUST NOT trade away correctness/freshness/provenance/isolation`.

### 22. Normalization

**Decisión:** métricas normalizadas cuando corresponda:

```text
cost per execution
cost per successful task
tokens per task
latency per task
reuse per opportunity
```

Evitar métricas absolutas dependientes solo del volumen.

### 23. Attribution

**Decisión:** cada ahorro se atribuye a una capa: Discovery reuse, Project Knowledge persistence, Context reuse, Materialization reuse o Provider Prompt Cache. No se contabiliza dos veces el mismo ahorro; un ahorro combinado (p. ej., Project Knowledge reuse + Provider Prompt Cache) se registra con atribución por capa y un total no duplicado.

### 24. Double Counting Prevention

**Decisión:** cada unidad de avoided work tiene un **owner/attribution** único:

```text
work avoided upstream   (discovery/knowledge reuse)
work reduced downstream (materialization/provider cache)
```

Se separan y **no** se suman como el mismo ahorro.

### 25. Economic measurement model

**Decisión (métrica, no policy):**

```text
Baseline Cost  = costo esperado/observado sin la optimización evaluada
Avoided Cost   = parte del baseline realmente evitada
Reuse Overhead = costo incremental del reuse (retrieval, validation, storage,
                 maintenance, materialization, provider-specific)
Net Benefit    = dimension-specific Avoided Cost − Reuse Overhead correspondiente
```

`Net Benefit` es **dimension-specific** (tokens, latencia, compute, money, storage por separado) salvo que exista una función de normalización válida a unidad común; no se define pricing ni una función monetaria universal. No convierte la ecuación en una política de admisión.

### 26. Thresholds

**Decisión:** esta RFC **no establece thresholds** (`reuse >= 3`, `hit rate >= 50%`, `savings >= X%`, `TTL = X`, `minimum value = X`). Cualquier umbral futuro será experimentalmente derivado, workload-dependent, provider-dependent y policy-controlled.

### 27. Provider-dependent vs independent metrics

```text
Provider-independent: reuse opportunities, reuse decisions, Context Budget,
                      Project Knowledge lifecycle, Discovery reuse
Provider-dependent:   prompt cache hit, cached token count, provider pricing,
                      provider cache TTL, provider cache eviction
```

No se inventan capacidades comunes entre providers (RFC-72).

### 28. Observability schema (requisitos)

**Decisión:** dimensiones de un futuro evento de telemetría (requisitos, no framework):

```text
event type, timestamp, project scope, execution/session identity,
knowledge identity where applicable, cache layer, operation, decision,
reason, latency, token metrics, cost metrics, outcome
```

No se crea un telemetry framework nuevo; los eventos se registran según el catálogo existente (`protocol/.agents/contracts/METRICS.md:Event catalog`), extendido por la RFC-D como requisito futuro.

### 29. Privacy / data minimization

**Decisión:** telemetry captura metadata de atribución suficiente **sin persistir contenido semántico innecesario** (ni prompt content ni knowledge content). Se respeta la Privacy rule existente: "Metrics describe the process, not the content" (`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Privacy rule`). Project/provider identifiers solo como metadata de scope.

### 30. Failure modes

**Decisión:** los modos de fallo afectan la **confiabilidad de la medición**, no la correctness:

```text
missing telemetry, partial telemetry, provider metrics unavailable,
inconsistent metrics, clock skew, duplicate events, retry duplication,
cache result unavailable
```

No se convierten en nuevos mecanismos de runtime; se registran como limitaciones de la medición.

### 31. Confidence / evidence quality

**Decisión:** toda medición se clasifica:

```text
Observed      (el provider/runtime reporta el valor)
Estimated     (derivado local, p. ej. chars/4)
Derived       (calculado de otros datos)
Unavailable   (no obtenible)
```

`provider reports cached tokens` y `tokens inferred from local context` tienen calidad de evidencia distinta; no se tratan igual. Se reutiliza la distinción de clases de `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Verifiability classes` y de claims (`protocol/.agents/standards/quality/EVIDENCE.md:Claim classes`).

### 32. Experimental decision model

**Decisión:** proceso de evaluación arquitectónica (no State Machine de runtime):

```text
Observe → Measure → Compare baseline → Estimate economic value
       → Evaluate safety constraints → Decide whether to retain/change policy
```

### 33. Ownership

| Concern | Owner |
| --- | --- |
| Cacheability semantics | RFC-71 |
| Provider prompt cache capability | RFC-72 |
| Project Knowledge persistence semantics | RFC-73 |
| Measurement / economic evaluation | RFC-74 |
| Telemetry catalog (proceso) | `PROTOCOL_METRICS.md` + `METRICS.md` (existente) |

### 34. Matrices

#### Matrix A — Measurement layers

| Layer | Signal | Current availability | Provider dependency | Economic meaning |
| --- | --- | --- | --- | --- |
| Discovery | `model_used`, `execution_time_seconds` | PARCIAL (opcional, manifest) | NO | costo de discovery/revalidación |
| Discovery reuse | reuse events | NOT AVAILABLE | NO | trabajo LLM evitado |
| Project Knowledge reuse | reuse events | NOT AVAILABLE | NO | valor del conocimiento reutilizado |
| Context Composition | budget declared/consumed | PARCIAL (catálogo; no registrado en la muestra) | NO | costo de composición/selección |
| Materialization | cost estimate (chars/4) | PARCIAL (runtime de referencia) | NO | costo de representación |
| Provider Prompt Cache | cached/uncached tokens, hit/miss | NOT AVAILABLE | SÍ | tokens/costo/latencia del provider |

#### Matrix B — Cache/reuse events

| Event | Opportunity | Lookup | Lookup result | Eligibility decision | Reuse outcome | Invalidation |
| --- | --- | --- | --- | --- | --- | --- |
| Discovery reuse | candidato fresco | KB/entrada | HIT / MISS | ACCEPTED / REJECTED (fresh/valid/provenance) | SUCCESSFUL / FAILED | fuente/versión cambiaron |
| Knowledge reuse | entrada persistida elegible | KB/entrada | HIT / MISS | ACCEPTED / REJECTED (stale/invalid/scope) | SUCCESSFUL / FAILED | revalidación requerida |
| Materialization reuse | SCI+MI estables (RFC-72) | materialización | HIT / MISS | ACCEPTED / REJECTED (según RFC-72) | SUCCESSFUL / FAILED | MI cambia |
| Provider cache | prefijo estable | provider | HIT / MISS | n/a (no eligibility decision) | n/a (provider state) | provider TTL/eviction |

#### Matrix C — Economic attribution

| Mechanism | Work avoided | Cost avoided | Overhead | Net benefit |
| --- | --- | --- | --- | --- |
| Discovery reuse | discovery recomputation | discovery tokens/compute/time | retrieval/validation | measure by dimension |
| Project Knowledge reuse | knowledge re-derivation | derivation cost | retrieval/revalidation/storage | measure by dimension |
| Materialization reuse | re-materialization | materialization cost | lookup/order | measure by dimension |
| Provider Prompt Cache | repeated provider processing | provider token/monetary/latency cost | provider cache operations | measure by dimension |

#### Matrix D — Experimentation

| Experiment | Baseline | Treatment | Primary metric | Safety metric | Confounders |
| --- | --- | --- | --- | --- | --- |
| Discovery reuse | sin reuse | con reuse | avoided discovery work | freshness/provenance | carga de trabajo |
| Knowledge reuse | sin reuse | con reuse | avoided derivation | validity/isolation | KB freshness |
| Provider cache | cache off | cache on | cached tokens/cost | correctness | modelo/workload |
| Combined | todo off | todo on | net economic value | todas | interacciones entre capas |

### 35. Invariantes

- **I-ECO-001 — Economy does not override validity:** las métricas económicas MUST NOT sobreescribir la validez semántica. (Normativo: subordina economía a correctness; testable: un artifact inválido nunca se admite por valor económico; owner: RFC-74 + RFC-73 eligibility.)
- **I-ECO-002 — Hit rate ≠ economic value:** el hit rate MUST NOT tratarse como valor económico por sí mismo. (Normativo: evita falsa economía; testable: hit alto sin ahorro neto detectable; owner: RFC-74.)
- **I-ECO-003 — Provider cache ≠ Project Knowledge:** el estado del cache del provider MUST NOT tratarse como Project Knowledge. (Deriva de RFC-73 I-PROJ-009; owner: RFC-74 + RFC-73.)
- **I-ECO-004 — No double counting:** la atribución económica MUST NOT contabilizar dos veces el mismo avoided work. (Normativo; testable: suma de atribuciones ≤ total observado; owner: RFC-74.)
- **I-ECO-005 — Evidence quality:** las conclusiones experimentales MUST distinguir observed de estimated/derived. (Normativo; testable: toda métrica reporta su clase; owner: RFC-74 + PROTOCOL_METRICS Verifiability.)
- **I-ECO-006 — Provider-dependency:** mediciones provider-dependent MUST NOT generalizarse como hechos provider-independent. (Normativo; testable: etiquetado por capa; owner: RFC-74.)

### 36. Testable properties

**Currently testable (con telemetría de proceso existente):**

- La telemetría de proceso existente no establece el estado del cache del provider.
- La telemetría de proceso existente no establece reuse de Project Knowledge.
- Freshness/validity no son modificados por la telemetría en sí.
- Invalid knowledge nunca se admite económicamente solo porque el reuse sea barato.

**Future testable (requisito de instrumentación):**

- Un hit del provider no implica Project Knowledge reuse.
- Un evento de reuse de Project Knowledge no implica hit del Provider Prompt Cache.
- Un hit rate mayor no produce automáticamente mayor valor económico.
- Avoided upstream work no se cuenta de nuevo como ahorro downstream de cache.
- `Net Benefit` (dimension-specific) es medible por capa sin doble conteo.

### 37. Dependencias

- [RFC-71 — Context Persistence & Cacheability Model](docs/rfc/71-context-persistence-cacheability-model.md): cacheability, memoization, persistence, identity, isolation, correctness.
- [RFC-72 — Provider Prompt Cache Capability](docs/rfc/72-provider-prompt-cache-capability.md): hit/miss semántica, admission boundary, ProviderCacheReference.
- [RFC-73 — Project & Discovery Context Persistence](docs/rfc/73-project-discovery-context-persistence.md): freshness, provenance, reuse eligibility, project isolation.
- [RFC-68 — Architecture Evolution Workflow](docs/rfc/68-architecture-evolution-workflow.md): gate de telemetría.
- [RFC-60 — Budget Accounting and Metrics Trust](docs/rfc/60-budget-accounting-metrics-trust.md): verifiability classes de las métricas.
- Estándares existentes: `PROTOCOL_METRICS.md`, `METRICS.md`, `EVIDENCE.md`, `DISCOVERY_MANIFEST.md`, `BUDGET_MATERIALIZATION.md`, `CONTEXT.md`.

### 38. Relación con RFC-71, RFC-72 y RFC-73

- **RFC-71** define cacheability/memoization/persistence/isolation; RFC-74 **hereda** sin redefinir.
- **RFC-72** define la capability de Provider Prompt Cache; RFC-74 **mide** su economía y evidencia; no redefine `MaterializationIdentity`, Canonical Materialization, Stable Prefix ni `ProviderCacheReference`.
- **RFC-73** define Project Knowledge, persistence, freshness, provenance, reuse eligibility y project isolation; RFC-74 **mide** si esos mecanismos producen valor económico; no modifica Freshness/Validity/Eligibility/ProjectIdentity/SegmentIdentity.

### 39. Fact vs future requirement

```text
FACT:    el catálogo de PROTOCOL_METRICS.md existe y mide proceso.
FACT:    no existe telemetría de tokens/cost/latencia del provider.
DECISIÓN: la economía se subordina a correctness/isolation/freshness/provenance/policy/budget.
FUTURO:  eventos de telemetría de capas de reuse/cache (requisito de implementación).
```

## Alternativas consideradas

1. **Un único `cache_hit` para todo el sistema.** Rechazada: confunde capas con mecanismos y costos distintos (sección 3).
2. **Hit rate como métrica primaria.** Rechazada: `Hit Rate ≠ Economic Value` (sección 5).
3. **Definir thresholds ahora.** Rechazada: no hay datos; los umbrales serán experimentalmente derivados (sección 26).
4. **Crear un telemetry framework en esta RFC.** Rechazada: RFC-74 define requisitos; la implementación es futura (sección 28).
5. **Tratar métricas provider-reported como hechos provider-independent.** Rechazada: calidad de evidencia por clase (sección 31; I-ECO-006).

## Alcance

**IN SCOPE:** telemetry requirements, economic model, attribution, measurement, experiments, evidence quality, cache economics, avoided work, false economy, admission evidence.

**OUT OF SCOPE:** cache implementation, provider adapters, provider pricing, cache key design, Project Knowledge persistence, Context Budget redesign, Discovery redesign, nuevas State Machines, telemetry implementation framework, thresholds.

**Impacto en el protocolo:** materialización parcial por plan 91 (versión
10.3.0, MINOR): tipos de evento `reuse_event`/`provider_cache_event` en el
contrato `METRICS.md` (schema 1.2.0) y catálogo `Reuse and cache` + economía
(I-ECO-001…I-ECO-006) en `PROTOCOL_METRICS.md`, con agregador dev y productores
del runtime consumidos sin duplicarlos; sin thresholds, sin pricing, sin
telemetry backend, sin cambios en contratos existentes ni en state machines.

## Criterios de aceptación

- [ ] No modifica la semántica de RFC-71/72/73.
- [ ] No inventa capacidades de provider ni telemetría actual.
- [ ] Distingue hit rate de economic value.
- [ ] Define avoided work y economic attribution.
- [ ] Previene double counting.
- [ ] Separa provider-independent de provider-dependent metrics.
- [ ] Separa observed / estimated / derived / unavailable.
- [ ] Define baseline/control/treatment.
- [ ] No establece thresholds arbitrarios.
- [ ] Mantiene correctness/freshness/isolation como safety constraints.
- [ ] No crea State Machine de runtime ni telemetry framework.
- [ ] Las métricas futuras están marcadas como requisitos de implementación.
- [ ] Toda afirmación sobre el estado actual del repo tiene evidencia.
- [ ] Las referencias documentales resuelven contra el repo; las verificaciones ejecutadas se reportan por separado.

## Amendment Log

- 2026-08-29 — Creación.
- 2026-08-29 — Final correction patch: `Economic admissibility` sustituida por `Economic evaluation` (capa observacional/evaluativa; sin economic admission gate; semantic validity precede); modelo de costo normalizado (Baseline Cost / Avoided Cost / Reuse Overhead / Net Benefit dimension-specific; `C_cache` eliminado como bolsa ambigua); sin unidades mezcladas ni pricing universal; vocabulario de eventos normalizado (Lookup HIT/MISS; Eligibility ACCEPTED/REJECTED; Reuse SUCCESSFUL/FAILED; Lifecycle INVALIDATED); materialization reuse hereda RFC-72 sin redefinir sus conceptos; metric hierarchy flexible (experiment-specific primary metric; safety constraints no se sacrifican); propiedades de hit/reuse movidas a future testable; retry count clasificado como derivable de HARNESS; matrices B/C actualizadas; sin cambios arquitectónicos.
- 2026-08-31 — Aceptada (plan 93): el modelo de economía del cache, telemetría
  y evidencia de admisión queda formalmente aceptado como fuente de verdad de
  medición (capas de economía, avoided work, eventos de reuse, taxonomía de
  misses, experimentos, invariantes I-ECO-001…I-ECO-006; sin thresholds ni
  pricing). Aceptación docs-only: sin impacto en `protocol/.agents/`, sin bump
  de `VERSION` ni tag; NO implica implementación automática — la implementación
  (eventos/catálogo/agregador) queda en el plan 91; sin cambios en `runtime/`
  mediante este plan.
- 2026-08-31 — Implementada (plan 91): materialización parcial de la medición/
  economía del cache — eventos `reuse_event` y `provider_cache_event` en el
  contrato `METRICS.md` (schema 1.2.0, aditivo; compatibilidad preservada por
  la regla de eventos desconocidos ignorados), catálogo `### Reuse and cache`
  y sección de economía (invariantes I-ECO-001…I-ECO-006 sin umbrales) en
  `PROTOCOL_METRICS.md`, agregación en `tools/aggregate_metrics.py` con
  derivación de Discovery reuse (clase Derived) y productores del runtime
  (planes 89/90) expuestos como metadata/estado; el registro de telemetría en
  `METRICS.md` permanece como responsabilidad del Orchestrator/host (seam
  arquitectónico documentado; sin writer de referencia en este repositorio).
  Distingue Observed/Estimated/Derived/Unavailable; sin pricing, sin
  thresholds, sin telemetry backend; no redefine RFC-71/72/73. Aceptada por
  plan 93; implementada por plan 91. Versión 10.3.0 (MINOR).
- 2026-09-21 — **Aclaración de la línea de versiones de `schema_version`**
  (Plan 141, `HD-12 F-7`). Las citas «`schema 1.2.0`» de la sección de impacto y
  de esta bitácora describen correctamente el bump `1.1.0 → 1.2.0` que **el
  propio plan 91** ejecutó sobre `protocol/.agents/contracts/METRICS.md`. El
  contrato vigente ya **no** está en esa versión: el plan 78 (versión 11.0.0) lo
  subió a **`2.0.0`**, que es el valor que declara hoy. Las entradas históricas
  se conservan sin reescribir (RFC-46); esta entrada fija la línea de versiones
  para que una lectura corriente no tome `1.2.0` como el estado actual. No
  cambia ninguna decisión de esta RFC.
