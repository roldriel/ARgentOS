# RFC-71 — Modelo de Context Persistence y Cacheability

**Status:** Accepted (plan 86, 2026-08-29)
**Fecha:** 2026-08-29
**Serie:** Context Persistence & Prompt Cache (RFC-A…RFC-D)
**Origen:** Cierre de arquitectura 2026-08-29, construido sobre `docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md:2.2 Tabla de artifacts`, `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment` y `docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`.
**Pregunta:** ¿Cómo se formaliza el modelo semántico de Context Persistence y Cacheability — segmentos, identidades, scope, persistence, cacheability, memoization, isolation, lifecycle e invalidación — sin acoplar el protocolo a proveedores?
**Afectados:** —

> Convención de evidencia: toda afirmación sobre el estado actual del repo se
> cita con `ruta:sección` (existente al momento de la redacción). Las
> decisiones nuevas de esta RFC se marcan como **Decisión**; los requisitos de
> implementación futura se marcan como **Requisito de implementación futura**.

## Problema

1. **El Execution Context existe como concepto, pero no como modelo de reutilización.** La RFC-00XY define el Execution Context como "el conjunto de información preparado por el Orchestrator y entregado a un Worker antes del inicio de una ejecución" (`docs/rfc/01-execution-context-model.md:Abstract`), y su construcción es un proceso de siete responsabilidades evaluadas por juicio con criterios ordenados (`protocol/.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation`; `protocol/.agents/standards/context/CONTEXT.md:Determinism model`). El modelo no distingue qué parte del contexto es estable entre invocaciones, ni cómo identificar, persistir o invalidar esa parte.

2. **La repetición de contexto estable está documentada y no se modela.** El bootstrap del protocolo se re-lee por sesión (`protocol/.agents/INDEX.md:Before executing any task`); cada delegación obliga al worker a leer el workflow module, el rol, el perfil, las skills y los input artifacts (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Worker Execution`); el orquestador re-ensambla el payload y reescribe el resumen de la tarea en cada delegación (`protocol/.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation`). Sin clasificación estable/dinámico no existe forma de razonar sobre esa repetición.

3. **No existe cache ni memoización, y la única persistence real es la KB de discovery.** La auditoría de reutilización documenta que los artifacts de sesión no se reutilizan entre sesiones y que la única reutilización durable es el conocimiento curado (`docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md:2.2 Tabla de artifacts`); la investigación de costo concluye que una RFC de memoización/cache carece de justificación sin telemetría (`docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`) y el propio RFC-68 define que `.project/` nunca es cache ni propiedad de ARgentOS y que cachear re-lectura es Fase 2 gateada a telemetría (`docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`).

4. **Los precedentes parciales existen y deben formalizarse sin inventar.** Discovery ya implementa hashes SHA-256, TTL y freshness por claim (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Hash Calculation`, `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:TTL and Cache`, `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Freshness Rule`); el payload es inmutable y versionado en bloque (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Protocol immutability`); el estado persistente del proyecto está delimitado (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`); y la evidencia tiene clases verificables (`protocol/.agents/standards/quality/EVIDENCE.md:Evidence classes`).

5. **Sin un modelo semántico, cualquier implementación de caching acoplaría el protocolo a proveedores o confundiría correctness con lifecycle.** Esta RFC establece la fuente de verdad semántica previa; las capacidades de provider, la materialización y la telemetría pertenecen a las RFCs posteriores.

## Modelo

### 1. Vocabulario normativo

| Término | Definición normativa | Estado |
| --- | --- | --- |
| **Context Segment** | Unidad semántica mínima identificable y, cuando la política lo permita, persistible, compuesta por contenido estable con una identidad propia. | Nuevo |
| **Stable Context** | Contenido cuya representación canónica es determinista dada su identidad y cuya semántica no depende de estado mutable por ejecución. | Nuevo |
| **Dynamic Context** | Contenido dependiente de la ejecución o mutable por invocación (tarea, estado, observación, resultados, metadata de ejecución). Complemento de Stable Context. | Nuevo |
| **Context Persistence** | Capacidad/política de almacenar contexto identificado para reutilización posterior. Opcional y ortogonal a cacheability, memoization y materialization. | Nuevo |
| **Cacheability** | Elegibilidad semántica de una representación materializada de contexto estable para participar en prompt caching del provider. Distinta de la policy de admisión de ARgentOS, de la capacidad del provider y del uso efectivo del cache. | Nuevo |
| **Memoization** | Reutilización del resultado de una operación sin recalcularla, cuando la operación y su fingerprint lo permiten. Ortogonal a Prompt Cache. | Nuevo |
| **Retrieval** | Selección de conocimiento/artifacts existentes para incorporarlos como candidatos de contexto. Separado de Persistence y Memoization. | Existente (`context_discoverer`, `protocol/.agents/orchestrators/core/roles/orchestrator.md:4.2 Context Discoverer Invocation`) |
| **Scope** | Dominio semántico de procedencia del contenido. No es lifetime, persistence, cacheability ni isolation. | Nuevo (como concepto formal) |
| **Lifecycle** | Estados de vida de una unidad persistida. Independiente de correctness. | Nuevo |
| **Isolation** | Namespace de visibilidad que gobierna el reuso. | Nuevo |
| **SegmentContentIdentity** | Identidad content-addressed del contenido canónico de un segmento. | Nuevo |
| **SegmentIdentity** | Identidad semántica compuesta de un segmento: `{semantic_version, content_identity, namespace}`. | Nuevo |
| **SemanticContextIdentity** | Identidad derivada del contexto compuesto, invariante a materialización. | Nuevo |
| **MaterializationIdentity** | Identidad de las reglas de materialización. Pertenece a la RFC-B; esta RFC solo la referencia para delimitar capas. | RFC-B |
| **ProviderCacheReference** | Referencia opaca del cache del provider. No es identidad de ARgentOS ni autoridad de correctness. | RFC-B (frontera en esta RFC) |

### 2. Modelo de contexto

**Decisión:** el flujo es `Context Sources → Context Composition → Context Classification → {Stable Context | Dynamic Context}`. La clasificación ocurre después de la composición y no retroalimenta la composición.

La clasificación se ancla en las categorías existentes del Execution Context: Identity Context (perfil) y Capability Context (skills) (`protocol/.agents/standards/orchestration/SKILLS.md:Skill vs. profile`), más las categorías de composición Identity / Task / Knowledge / Capability / Execution Metadata (`protocol/.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation`).

**Regla de clasificación:**

- **Stable:** contenido de Identity y Capability (bootstrap, state machines, policies, workflow, rol, perfil, skills activadas) y contenido de Knowledge persistente y fresco (KB de discovery como project segment).
- **Dynamic:** Task (resumen de tarea reescrito por delegación), Knowledge excerpts re-derivados, Execution Metadata, artifacts de sesión, estado, observación y resultados.

No son equivalentes: `Stable ≠ Persisted`, `Dynamic ≠ Ephemeral`, `Stable ≠ Prompt Cache`. Son propiedades distintas.

**Decisión (frontera de determinismo):** la composición determina la **membresía semántica** del contexto; no se le exige determinismo de bytes (es juicio con criterios ordenados, `protocol/.agents/standards/context/CONTEXT.md:Determinism model`). `SemanticContextIdentity` identifica el contexto semántico resultante. El determinismo de representación es responsabilidad de la materialización: para la misma `SemanticContextIdentity` y la misma `MaterializationIdentity` (RFC-B), la materialización canónica MUST ser determinista.

### 3. Segmentos

**Decisión:** un Segment es la unidad mínima identificable y persistible. Los segmentos estables actuales son:

| Segmento | Contenido | Evidencia |
| --- | --- | --- |
| **Core** | Bootstrap del protocolo: `_AGENTS.md`, `INDEX.md`, rol system, `SYSTEM_STATE_MACHINE.md`, `AGENT_STATE_MACHINE.md`, rol orchestrator | `protocol/.agents/INDEX.md:Before executing any task` |
| **Project** | KB de discovery (entradas + `executive_summary.md` read-first + manifest), entradas curadas/lessons, skills de proyecto | `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`; `protocol/.agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md:Purpose` |
| **Worker** | Workflow module de la fase, policy del gate, rol/perfil, skills activadas | `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Worker Execution` |

**Decisión:** no se introducen segmentos `session`, `execution`, `artifact`, `discovery` ni `tool result`: el reuso de artifacts entre sesiones está prohibido (`protocol/.agents/standards/context/CONTEXT.md:2. Omission rules`) y no existe evidencia de otros segmentos estables. Tampoco existe una categoría abierta "otros segmentos".

**Decisión:** Core/Project/Worker **no** son mecanismos de cache independientes; son dominios semánticos de un único modelo de persistencia.

### 4. Identidades

#### SegmentContentIdentity

**Decisión:** `SegmentContentIdentity = hash(contenido canónico del segmento)`, con las propiedades:

- hashing determinista sobre una entrada canónica (orden, encoding y serialización de bytes fijos);
- encoding estable (UTF-8, sin normalización no declarada);
- semántica de igualdad: dos contenidos canónicos idénticos producen la misma identidad.

**Decisión:** el algoritmo sigue la convención existente del repositorio: SHA-256, la misma que Discovery ya exige para sus hashes (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Hash Calculation`). No se introducen garantías criptográficas más fuertes que las del mecanismo elegido.

**Decisión (distinción normativa):** `SegmentContentIdentity` responde "¿el contenido canónico es igual?"; `SegmentIdentity` es la **identidad semántica scoped** del segmento y responde "¿es el mismo segmento versionado semánticamente y aislado?". `SegmentIdentity` nunca se reduce al hash de contenido.

Ejemplo: Proyecto A y Proyecto B con el mismo contenido canónico X, misma versión semántica V y namespaces A y B:

```text
SegmentContentIdentity(A) == SegmentContentIdentity(B)
SegmentIdentity(A) != SegmentIdentity(B)   // el namespace difiere
```

Este ejemplo impide la deduplicación cross-project accidental (sección 9).

#### SegmentIdentity

**Decisión:** identidad compuesta:

```text
SegmentIdentity = {
    semantic_version,   // protocol_version que gobierna el significado contractual del contenido
    content_identity,   // SegmentContentIdentity
    namespace           // isolation: protocol-global | project_identity
}
```

- **semantic_version:** bajo el modelo actual de versionado en bloque del protocolo, `protocol_version` es la versión semántica que gobierna el contenido del segmento; el payload es inmutable en sesión (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Protocol immutability`). Esta elección está acotada al modelo actual: la posibilidad futura de versiones semánticas por segmento más finas queda diferida y no se decide en esta RFC.
- **content_identity:** la `SegmentContentIdentity`.
- **namespace:** el aislamiento. Para contenido de proyecto, `project_identity` pertenece al **namespace**, no al content identity (decisión isolation-first, sección 9).

**Consecuencias (resolución de la ambigüedad contenido vs semántica):** un mismo contenido canónico bajo dos versiones semánticas distintas produce **dos SegmentIdentity distintas** (cambia `semantic_version`); la semántica puede cambiar sin cambiar bytes y ese cambio lo detecta el componente `semantic_version`, no el hash de contenido. La identidad es **compuesta** (content-addressed + semantic-addressed + aislada), no exclusivamente content-addressed.

#### SemanticContextIdentity

**Decisión:** identidad **derivada** del contexto compuesto:

```text
SemanticContextIdentity = {
    protocol_version,   // ancla legible de composición; consistente con los segmentos (I-012)
    project_identity,   // namespace de la composición (null para core)
    segments: { core: SegmentIdentity, worker: SegmentIdentity,
                project: SegmentIdentity, ... }   // solo los participantes
}
```

Es determinista (`I-001`, `I-004`) e **independiente de** provider, model, serialization, ordering y cache internals (`I-005`). No incluye `provider`, `model`, `model_version`, `serialization_format`, `ordering`, `TTL`, `cache_policy` ni `ProviderCacheReference`.

**Decisión (ancla de versión de composición):** `SemanticContextIdentity.protocol_version` es un ancla de composición, no una segunda autoridad de versión. MUST ser consistente con los `semantic_version` de todos los segmentos participantes y MUST NOT constituir una autoridad semántica independiente. Si los valores discrepan (p. ej., `SCI.protocol_version = X` y `segment.semantic_version = Y`), la `SemanticContextIdentity` es **inválida** (I-012).

**Decisión (semántica de igualdad de SemanticContextIdentity):** dos `SemanticContextIdentity` son iguales si y solo si representan el mismo namespace de composición, el mismo conjunto lógico de `SegmentIdentity` participantes y un ancla de versión de protocolo consistente. El orden de representación de los segmentos no forma parte de la identidad semántica. No se define aquí un algoritmo de hash para `SemanticContextIdentity` (el repo no tiene una convención que lo exija); la igualdad es por comparación de los componentes.

**Decisión (ancla de namespace de composición):** `SemanticContextIdentity.project_identity` es un ancla de namespace de composición. Debe ser consistente con los namespaces de los `SegmentIdentity` participantes (`SegmentIdentity.namespace` + `SemanticContextIdentity.project_identity`); para un contexto de scope project, el project segment, cuando está presente, usa el namespace de proyecto correspondiente. `project_identity` no entra en `SegmentContentIdentity` ni se convierte en identidad de contenido; no introduce deduplicación cross-project (sección 9). Si el namespace de composición es inconsistente con los namespaces de los segmentos participantes, la `SemanticContextIdentity` es **inválida**.

#### MaterializationIdentity y ProviderCacheReference (frontera)

**Decisión:** la relación es `SemanticContextIdentity + MaterializationIdentity → Canonical Materialization`; la `MaterializationIdentity` y la `Canonical Materialization` son de la RFC-B. Esta RFC solo establece la frontera: la identidad semántica no contiene información de materialización.

**Decisión:** el identificador del cache del provider se llama **`ProviderCacheReference`** (se rechaza `ProviderCacheIdentity`): es opaco para ARgentOS, lo controla el provider/adapter, no forma parte de `SegmentIdentity` ni de `SemanticContextIdentity`, y nunca es autoridad de correctness (`I-007`). Sus detalles pertenecen a la RFC-B.

#### Matrix C — Componentes de identidad

| Component | Segment Identity | Semantic Context Identity | Materialization Identity | Provider Cache Reference |
| --- | ---: | ---: | ---: | ---: |
| Content | YES (`content_identity`) | derivado (vía segment identities) | NO | NO |
| Semantic version | YES (`semantic_version`) | derivado (vía segmentos; ancla `protocol_version`) | NO | NO |
| Namespace | YES | YES (`project_identity`) | NO | NO |
| Project identity | en el namespace del segmento | YES (`project_identity`) | NO | NO |
| Protocol version | YES (como `semantic_version`) | YES (ancla derivada, I-012) | NO | NO |
| Ordering | NO | NO | YES (vía `materialization_version`; RFC-B) | NO |
| Provider | NO | NO | YES | NO |
| Model | NO | NO | YES | NO |
| Serialization | NO | NO | YES (vía `materialization_version`; RFC-B) | NO |
| TTL | NO | NO | NO (lifecycle) | estado del provider, no identidad |
| Cache policy | NO | NO | NO (estado del adapter) | estado del provider |

### 5. Scope y atributos ortogonales

**Decisión:** "scope" designa únicamente el **dominio semántico de procedencia**. No es sinónimo de lifetime, persistence, cacheability, memoization, security boundary ni TTL.

| Concepto | Definición | Valores |
| --- | --- | --- |
| **Scope** | Dominio semántico de procedencia del contenido | `core`, `project`, `worker`, `session`, `execution` |
| **Lifecycle** | Estados de vida de una unidad persistida | create → active → reuse → refresh → invalidate → expire → delete |
| **Persistence** | Política de almacenamiento | `persisted` / `ephemeral` |
| **Cacheability** | Capacidad de participar en prompt caching del provider | `cacheable` / no |
| **Memoization** | Reutilización de resultados de operaciones | `memoizable` (con fingerprint) / no |
| **Isolation** | Namespace de visibilidad | `protocol-global`, `per-project`, `per-session` |

**Decisión:** `execution` es un scope válido aunque sus contenidos sean típicamente ephemeral, non-cacheable o solo parcialmente persistidos. No valen las equivalencias `execution == dynamic`, `dynamic == non-persistible` ni `non-cacheable == non-persistible`: un tool result es scope `execution`, puede persistirse como evidencia con clase `measurement` (`protocol/.agents/standards/quality/EVIDENCE.md:Evidence classes`), puede ser memoizable con fingerprint, y no es prompt-cacheable.

#### Matrix A — Propiedades ortogonales

| Concept | Scope | Lifecycle | Persistence (eligibility) | Cacheability | Memoization | Isolation |
| --- | --- | --- | --- | --- | --- | --- |
| Core | core | por versión del payload | YES | eligible (materializable) | NO aplica (contenido, no resultado) | protocol-global |
| Project | project | TTL/hash de Discovery (6h/24h) + versión | YES | eligible (project segment) | CONDICIONAL (no re-derivar mientras fresco) | per-project |
| Worker | worker | por versión + activación | YES | eligible (worker segment) | NO aplica | protocol-global; skills de proyecto per-project |
| Session | session | sesión/iteración | CONDITIONAL | NO (re-lectura intra-sesión, no prefijo) | NO | per-session |
| Execution | execution | single call | CONDITIONAL | NO | CONDICIONAL (resultados con fingerprint) | execution |
| Tool Result | execution | registro | CONDITIONAL | NO | CONDICIONAL (con fingerprint) | execution/session |
| Discovery Result | project | TTL/hash | YES | CONDICIONAL (solo vía materialización del project segment) | CONDICIONAL (mientras fresco) | per-project |
| Artifact | session | artifact lifecycle (draft/validated/superseded) | CONDITIONAL | NO | NO | per-session |

**Eligibilidad de persistence vs estado actual del repo:**

| Concept | Persistence Eligibility | Currently Persisted |
| --- | --- | --- |
| Core | YES | NO (no existe store de segmentos en el repo) |
| Project | YES | YES (KB de discovery; `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`) |
| Worker | YES | NO (no existe store) |
| Session | CONDITIONAL | YES como traza (artifacts; `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Artifact Safety Rule`) |
| Execution | CONDITIONAL | YES como traza cuando se registra (`protocol/.agents/standards/quality/EVIDENCE.md:Recording locations`) |
| Tool Result | CONDITIONAL | CONDITIONAL (según se registre como evidencia) |
| Discovery Result | YES | YES (KB + manifest; `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`) |
| Artifact | CONDITIONAL | YES como traza |
| Task | NO | NO |

**Decisión:** la elegibilidad de persistence es una propiedad normativa del modelo; el estado actual ("Currently Persisted") es un hecho del repo y no la determina. Si el repo no estableciera el estado exacto de una fila, se marcaría `UNKNOWN`; ninguna fila lo requiere hoy.

### 6. Persistence

**Decisión:** Context Persistence es una capacidad/política **opcional** y **ortogonal** a cacheability, memoization y materialization. Persistir no implica Prompt Cache y Prompt Cache no implica persistir.

**Decisión:** la unidad de persistence es el **Segment** (`Persistence Unit = Segment`), porque la segmentación permite: reuso incremental por segmento (un segmento cambia sin reconstruir la identidad de los demás, sección 10); identidad requerida para correctness y deduplicación dentro del namespace; aislamiento vía namespace; y correctness del contenido persistido = identidad válida (contenido + versión semántica) + namespace correcto.

**Requisito de implementación futura:** las claves de persistence deben respetar el namespace de aislamiento; el backend, el schema y el eviction no son parte de esta RFC.

La tabla "Eligibilidad de persistence vs estado actual del repo" (sección 5) separa la elegibilidad normativa del estado de implementación.

### 7. Cacheability

**Decisión:** Cacheability es la **elegibilidad semántica** de una representación materializada de contexto estable para participar en prompt caching del provider. Se distinguen cuatro conceptos:

```text
Semantic eligibility        → ¿puede semánticamente participar?
ARgentOS admission policy   → ¿ARgentOS decide admitirlo? (policy, no algoritmo; RFC-B)
Provider capability         → ¿el provider lo soporta? (RFC-B)
Actual provider cache usage → ¿el provider efectivamente lo cachea? (observado; RFC-D)
```

Esta cadena expresa **responsabilidades**, no un pipeline secuencial obligatorio. No se definen aquí algoritmo de admisión ni umbrales; `reuse >= 3` no es normativo y queda diferido a RFC-B/economía.

Ejemplo:

```text
Stable Worker Segment
        ↓
semantically eligible = YES

ARgentOS admission policy
        ↓
NO

Provider capability
        ↓
YES

Actual cache use
        ↓
NO
```

Por lo tanto: `provider capability = YES` no implica `actual cache use = YES`, y `semantic eligibility = YES` no implica `actual cache use = YES`. No valen las equivalencias `cacheable == persisted` ni `cacheable == stable`.

**Decisión (Stable Context vs Stable Prefix):** Stable Context es un concepto **semántico**; Stable Prefix es una **propiedad de una materialización concreta**. Reglas de identidad:

```text
same SemanticContextIdentity + same MaterializationIdentity
    → same canonical materialization

same SemanticContextIdentity + different MaterializationIdentity
    → potentially different canonical materialization
```

Un Stable Context puede producir distintos prefixes bajo distintas `MaterializationIdentity`, pero bajo el mismo contrato de materialización no son válidos prefixes incompatibles simultáneos. El cambio de prefix sin cambio semántico lo detecta la `MaterializationIdentity` (RFC-B), no la `SemanticContextIdentity`.

### 8. Memoization

**Decisión:** Memoization es reutilización del resultado de una operación sin recalcularla, ortogonal a Prompt Cache. Ejemplos habilitados por el repo: tool results registrados como evidencia con clase `measurement` (`protocol/.agents/standards/quality/EVIDENCE.md:Evidence classes`) y resultados de discovery cuyo reuso sin re-derivación está **condicionado** a su frescura y hashes (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:TTL and Cache`). Los mecanismos de freshness/hash existentes permiten reutilizar conocimiento mientras está fresco, pero esta RFC **no redefine** ese mecanismo como un framework general de memoization.

**Decisión:** esta RFC no define un framework de memoization general. Memoization no es otra forma de Prompt Cache, y el memoization de artifacts no es reutilización de contexto entre sesiones (prohibida por `protocol/.agents/standards/context/CONTEXT.md:2. Omission rules`).

### 9. Isolation

**Decisión:** política inicial **isolation-first**. `ProjectIdentity` define un namespace de persistence; **no** forma parte del content identity del segmento.

**Decisión normativa:** el reuso cross-project está **prohibido salvo autorización explícita**. No se implementa deduplicación cross-project; la igualdad de contenido **no** implica permiso de reutilización. Se distinguen formalmente:

- **content equality**: hecho detectable (mismo `content_identity`);
- **reuse authorization**: permiso explícito (aislamiento);
- **security isolation**: contenido sensible nunca se mezcla entre namespaces ni se persiste fuera de ellos;
- **deduplication**: optimización económica diferida, requiere decisión explícita de seguridad.

La política no depende de hashes: los hashes detectan igualdad; la autorización la decide la política.

### 10. Lifecycle e invalidación

**Decisión:** el lifecycle conceptual es `create → active → reuse → refresh → invalidate → expire → delete`. No todo objeto persistido debe atravesar todos los estados.

**Decisión (correctness):** la invalidación de correctness es exclusivamente por cambio de identidad:

```text
content_identity change  →  invalidación semántica
semantic_version change  →  invalidación semántica
```

**Decisión (lifecycle):** TTL/expiración gobierna freshness y lifecycle, **nunca** correctness (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`, `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Invalidation`). No se define un valor de TTL universal ni comportamiento TTL de proveedores.

**Decisión (GC):** garbage collection es limpieza de almacenamiento. Borrar un objeto no redefine su identidad semántica; expirar no vuelve semánticamente incorrecto retroactivamente contenido que fue válido.

**Matriz de invalidación:**

| Change | Segment | Semantic Context | Materialization | Provider Cache |
| --- | --- | --- | --- | --- |
| Protocol version | sí (semantic_version de cada segmento) | sí | sí | miss |
| Core content | sí (core) | sí | sí | miss |
| Project content | sí (project) | sí | sí | miss |
| Worker content | sí (worker) | sí | sí | miss |
| Tool schema | sí (worker) | sí | sí | miss |
| Harness | sí (core/worker) | sí | sí | miss |
| Policy | sí (core/worker) | sí | sí | miss |
| State machine | sí (core) | sí | sí | miss |
| Discovery knowledge | sí (project; hashes/TTL) | sí | sí | miss |
| Ordering change | no (contenido intacto) | no (identidad invariante) | sí (RFC-B) | miss |
| Serialization change | no | no | sí (RFC-B) | miss |
| Provider change | no | no | sí (RFC-B) | miss |
| Model change | no | no | sí (RFC-B) | miss |

### 11. Context Budget

**Decisión:** el caching no modifica silenciosamente los límites semánticos del Context Budget (`I-010`). Se distinguen tres magnitudes:

- **semantic context size**: el tamaño del Execution Context compuesto, limitado por el Budget (hoy medido sobre la porción KB; `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:7. Enforcement status`);
- **cached token accounting**: contabilidad post-materialización de tokens con hit del provider (RFC-D);
- **economic cost**: costo de procesamiento (RFC-D).

El Budget limita la composición, no el costo; el cache reduce el costo de lectura del contexto estable sin ampliar el contexto componible. No se definen reglas de contabilidad de providers.

### 12. Participación de dominios

**Decisión:** State Machines, Workers, Tools, Harnesses y Policies **no** tienen arquitecturas de cache propias; esta sección solo explica cómo participan en el modelo — qué puede ser estable, dinámico, persistido, memoizado o potencialmente cacheable — sin redefinir la arquitectura de ninguno de esos dominios ni introducir mecanismos de cache por dominio.

| Domain | Definition | Version | Config | Execution State | Result |
| --- | --- | --- | --- | --- | --- |
| State Machine | Stable segment (core) | semantic_version | n/a | Dynamic (`state.json`) | Dynamic/traza |
| Worker | Stable segment (worker: workflow+rol) | semantic_version | clasificada por rol semántico; esta RFC no asume que toda configuración pertenezca al segmento estable | Dynamic | Persisted artifact (sesión) |
| Tool | Stable segment (worker: definición/schema/instrucciones) | semantic_version | n/a | Dynamic | Dynamic + memoizable condicional (`measurement`) |
| Harness | Stable segment (core/worker: policies) | semantic_version | n/a | Dynamic (`state.json`/HARNESS) | Persisted trace |
| Policy | Stable segment (core/worker) | semantic_version | n/a | n/a | n/a (constriñe; no produce resultado) |

**Decisión (configuración de worker):** la configuración se clasifica según su rol semántico; RFC-71 no asume que toda configuración pertenezca al Worker Segment estable. Perfil y skills afectan la composición del segmento (`protocol/.agents/orchestrators/core/roles/orchestrator.md:5.1 Profile Selection Before Execution`, `protocol/.agents/orchestrators/core/roles/orchestrator.md:5.2 Skill Selection`); parámetros como timeout, retry count, parámetros de runtime y modo de ejecución son potencialmente execution-specific y no se asignan aquí al segmento estable. Los ítems sin evidencia suficiente quedan declarados como no clasificados (OPEN), no se inventa su ubicación.

**Discovery:** se preserva la distinción `Discovery Persistence ≠ Context Persistence ≠ Memoization ≠ Provider Prompt Cache`. El flujo conceptual es `Discovery → Project Knowledge → Stable Project Segment → Semantic Context`; la persistence y frescura específicas de Discovery permanecen bajo el RFC-C y la arquitectura existente (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:TTL and Cache`).

### 13. Matrix B — Semántica de reutilización

| Data | Stable | Persistible | Memoizable | Prompt-cacheable | Why |
| --- | ---: | ---: | ---: | ---: | --- |
| Core | YES | YES | NO | CONDITIONAL | Contenido de protocolo inmutable por versión; persiste como segmento; su materialización puede cachearse si el provider lo permite |
| Project Knowledge | YES (mientras fresca) | YES | YES | CONDITIONAL | KB ya persiste (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`); no se re-deriva mientras fresca; solo la porción materializada del project segment es cacheable |
| Worker Definition | YES | YES | NO | CONDITIONAL | Definición de fase/rol estable por versión; segmento persistible; materialización cacheable |
| Tool Definition | YES | YES | NO | CONDITIONAL | Definición/schema estables; parte del worker segment |
| Tool Result | NO | YES (evidencia) | CONDITIONAL (con fingerprint) | NO | Depende de la ejecución; clase `measurement` (`protocol/.agents/standards/quality/EVIDENCE.md:Evidence classes`) |
| Discovery Result | YES (mientras fresca) | YES | CONDITIONAL | CONDITIONAL (solo vía project segment) | Snapshot con TTL/hash; reuso sin re-derivación solo mientras fresco; el resultado en sí no se materializa como cache |
| State Machine Definition | YES | YES | NO | CONDITIONAL | Contenido estable del core |
| Execution State | NO | YES (traza) | NO | NO | Cambia por transición; traza en `state.json` |
| Artifact | NO (intra-sesión) | YES (traza) | NO | NO | Reuso entre sesiones prohibido (`protocol/.agents/standards/context/CONTEXT.md:2. Omission rules`) |
| Task | NO | NO | NO | NO | Se reescribe por delegación (`protocol/.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation`) |

### 14. Invariantes

- **I-001 — Deterministic Segment Identity:** para el mismo `semantic_version`, contenido canónico y namespace, `SegmentIdentity` es idéntica.
- **I-002 — Content Identity:** contenidos canónicos distintos no comparten intencionalmente la misma `SegmentContentIdentity`; no se afirman garantías criptográficas más fuertes que las de SHA-256.
- **I-003 — Semantic Versioning:** cambiar `semantic_version` cambia `SegmentIdentity` aunque el contenido canónico sea idéntico.
- **I-004 — Context Identity Determinism:** los mismos `SegmentIdentity` participantes producen la misma `SemanticContextIdentity`.
- **I-005 — Materialization Independence:** `SemanticContextIdentity` no depende de materialización específica del provider.
- **I-006 — Persistence Independence:** Context Persistence no es prerrequisito de Materialization ni de Provider Prompt Cache, y viceversa.
- **I-007 — Provider Reference Opacity:** `ProviderCacheReference` nunca es autoridad de correctness de ARgentOS.
- **I-008 — Isolation:** no hay reuso cross-project sin autorización explícita.
- **I-009 — TTL:** la expiración por TTL nunca es el mecanismo de correctness.
- **I-010 — Budget:** el caching no modifica silenciosamente los límites semánticos del Context Budget.
- **I-011 — Orthogonality:** Scope, Lifecycle, Persistence, Cacheability, Memoization e Isolation no son sinónimos.
- **I-012 — Composition-version consistency:** `SemanticContextIdentity.protocol_version` es un ancla de composición: MUST ser consistente con los `semantic_version` de todos los segmentos participantes y MUST NOT constituir una autoridad semántica independiente. Un `protocol_version` inconsistente con el `semantic_version` de un segmento participante ⇒ `SemanticContextIdentity` **inválida**.

### 15. Trazabilidad con el cierre de arquitectura

| Architecture Decision | RFC Section |
| --- | --- |
| SegmentIdentity compuesta (semantic_version + content_identity + namespace) | §4 (Identidades) |
| SegmentContentIdentity distinta de SegmentIdentity | §4 |
| SemanticContextIdentity derivada e invariante a materialización | §4 |
| Scope model (scope = dominio semántico; atributos ortogonales) | §5 |
| Persistence independiente de Materialization | §6 |
| Cacheability ortogonal a persistence | §7 |
| Stable Context ≠ Stable Prefix | §7 |
| Memoization ≠ Prompt Cache | §8 |
| Isolation-first; ProjectIdentity en namespace | §9 |
| Correctness = identity; TTL = lifecycle; GC = storage | §10 |
| Context Budget no modificado por caching | §11 |
| ProviderCacheReference opaca y sin rol de correctness | §4 |

### 16. Dependencias

- [RFC-00XY — Execution Context Model](docs/rfc/01-execution-context-model.md): define el Execution Context que esta RFC clasifica.
- [RFC-00XZ — Execution Context Assembly Process](docs/rfc/02-execution-context-assembly-process.md): las siete responsabilidades de composición.
- [RFC-00YA — Context Budget Model](docs/rfc/03-context-budget-model.md): el Budget semántico que esta RFC no rediseña.
- [RFC-00YB — Context Candidate Prioritization Model](docs/rfc/04-context-candidate-prioritization-model.md): priorización sin selección.
- [RFC-00YK — Execution Context Materialization Model](docs/rfc/13-execution-context-materialization-model.md) y [RFC-00YL — Prompt Rendering Model](docs/rfc/14-prompt-rendering-model.md): la frontera protocolo/runtime que esta RFC respeta.
- [RFC-65 — Evidence and Verification Model](docs/rfc/65-evidence-and-verification-model.md): clases de evidencia para memoization.
- [RFC-67 — Knowledge Lifecycle Model](docs/rfc/67-knowledge-lifecycle-model.md): freshness/invalidación del conocimiento.
- [RFC-68 — Architecture Evolution Workflow](docs/rfc/68-architecture-evolution-workflow.md): gate de telemetría para cache.
- [RFC-70 — Project Context in Discovery KB](docs/rfc/70-project-context-in-discovery-kb.md): el project segment se nutre de la KB de discovery.

### 17. Relación con RFC-B, RFC-C y RFC-D

#### Roles normativos (owner / consumer / implementer)

**Decisión:** en este modelo, *owner* es la autoridad/fuente de la definición normativa de un concepto; *consumer* es un componente que puede leer/usar el concepto; *implementer* es el componente responsable de ejecutar el comportamiento. "Un único owner" no significa "una sola capa puede conocer el concepto": otras capas lo consumen o implementan sin ser su autoridad normativa. Ejemplo: `MaterializationIdentity` tiene owner en RFC-B; RFC-71 la referencia como consumer sin definirla; el runtime la implementará como implementer.

#### RFC-B — Provider Prompt Cache Capability

- **Define:** provider cache capability, canonical ordering contract, `MaterializationIdentity`, canonical materialization, stable prefix, interacción con el provider, `ProviderCacheReference`.
- **Usa de esta RFC:** la distinción semántica estable/dinámico y la `SemanticContextIdentity` invariante a materialización.
- **Esta RFC no duplica:** no define APIs de provider, cache keys, breakpoints, TTL de provider, formatos de materialización ni el orden canónico concreto.

#### RFC-C — Project & Discovery Context Persistence

- **Define:** `ProjectIdentity`, persistence namespace, integración Discovery → Project Knowledge, frescura, comportamiento de persistence de proyecto/discovery.
- **Usa de esta RFC:** la política isolation-first, la unidad de persistence = segmento y el model de invalidation.
- **Esta RFC no duplica:** no rediseña Discovery ni define el backend de persistence.

#### RFC-D — Cache Observability & Economics

- **Define:** observabilidad, métricas, economía del cache, experimentos y medición.
- **Usa de esta RFC:** el significado semántico de identidad y cacheability.
- **Esta RFC no duplica:** no define umbrales económicos ni instrumentación concreta.

### 18. Implicaciones de implementación

Requisitos que la implementación futura debe respetar (sin plan de implementación):

- La identidad de segmento debe ser determinista y componerse de `semantic_version + content_identity + namespace`.
- Las claves de persistence deben respetar el namespace de aislamiento.
- El runtime no debe tomar decisiones de cache de proveedores dentro del modelo semántico.
- Materialization y Persistence deben permanecer separadas; ninguna es prerequisito de la otra.
- Cacheability debe permanecer ortogonal a persistence.
- La correctness se gobierna por identidad (contenido + versión); TTL solo lifecycle.
- La composición no requiere determinismo de bytes (es juicio con criterios); los segmentos y la materialización sí (I-001, I-004 y RFC-B).
- La elegibilidad de persistence es independiente del estado actual de implementación (sección 5); persistir lo elegible no requiere que exista hoy.
- La materialización canónica debe ser determinista para la misma `SemanticContextIdentity` + `MaterializationIdentity`; el determinismo no se exige a la composición (sección 2).

### 19. Propiedades testables

- Mismo contenido canónico + misma versión semántica + mismo namespace → misma `SegmentIdentity`.
- Mismo contenido canónico + distinta versión semántica → distinta `SegmentIdentity`.
- Mismo contenido canónico + misma versión semántica + distinto namespace → distinta `SegmentIdentity`.
- Mismos `SegmentIdentity` participantes → misma `SemanticContextIdentity`.
- Misma `SemanticContextIdentity` → independiente de provider/model/ordering.
- Misma `SemanticContextIdentity` + misma `MaterializationIdentity` → misma materialización canónica.
- Misma `SemanticContextIdentity` + distinta `MaterializationIdentity` → potencialmente distinta materialización canónica.
- Persistence deshabilitada → materialization sigue siendo conceptualmente válida.
- Provider capability = YES → no implica actual cache use = YES.
- Mismo proyecto + mismo contenido → reutilizable dentro del namespace.
- Distinto proyecto + mismo contenido → sin reuso cross-project sin autorización explícita.
- Cambio de `content_identity` o `semantic_version` → invalidación de correctness; cambio de TTL → solo efecto de lifecycle, no cambio de correctness.

## Alternativas consideradas

1. **No hacer nada.** Mantiene la ausencia de un modelo semántico de reutilización; cualquier implementación posterior carecería de fuente de verdad y acoplaría el protocolo a proveedores. Descartada.
2. **CoreCache / ProjectCache / WorkerCache como sistemas independientes.** Duplicaría identity, invalidación y observabilidad para un solo hecho (el payload se versiona en bloque); contradice el modelo de un único mecanismo de persistence con scopes. Descartada.
3. **`prompt.cache = true` como propiedad del prompt.** Acopla el protocolo a la semántica del provider y viola la frontera protocolo/runtime (`docs/rfc/14-prompt-rendering-model.md:Rendering Variants`). Descartada.
4. **TTL-only correctness.** Contradice el precedente de Discovery (hash = correctness, TTL = frescura) y el RFC-68. Descartada.
5. **Context Persistence como paso obligatorio antes de Materialization.** Introduce una dependencia artificial; Prompt Cache puede funcionar sobre una composición estable sin persistirla (I-006). Descartada.
6. **`ProviderCacheIdentity` como identidad de ARgentOS.** Es opaca y no controlada por ARgentOS; el nombre y el rol de correctness son incorrectos. Se adopta `ProviderCacheReference` (I-007). Descartada.
7. **`reuse >= 3` como invariant arquitectónico.** Convierte una optimización económica en una regla de correctness sin evidencia; es política métrico-dirigida de la RFC-B. Descartada.
8. **`execution == dynamic == non-persistible`.** Confunde dimensiones ortogonales; el scope execution admite contenido persistido y memoizable. Descartada.
9. **Discovery Persistence == Prompt Cache.** Confunde memoización de conocimiento con materialización delegada. Descartada.
10. **Artifact Memoization == Prompt Cache.** El reuso de artifacts entre sesiones está prohibido y la memoización de resultados es otro dominio. Descartada.

## Alcance

Esta RFC **no define**:

- APIs de cache de proveedores, cache keys, breakpoints, TTL mechanics ni pricing de proveedores;
- implementación de adapters de provider;
- backend de persistence, schema de base de datos ni algoritmo de eviction;
- implementación de Discovery ni de Retrieval;
- framework de memoization;
- umbrales de cache admission ni umbrales económicos;
- implementación concreta de observabilidad;
- formato concreto de materialización ni la elección concreta del orden canónico.

**Impacto en el protocolo:** ninguno. Es una RFC conceptual: no modifica `protocol/.agents/`, no cambia contratos, no cambia state machines, no produce bump de `VERSION` ni entrada de changelog. En `Proposal` no habilita tocar el payload (RFC-56; `docs/CONVENTIONS.md:Convenciones`).

## Criterios de aceptación

- [ ] El vocabulario distingue Prompt Cache / Context Persistence / Memoization / Retrieval / Artifact reuse.
- [ ] `SegmentIdentity` es compuesta (`semantic_version + content_identity + namespace`) y `SegmentContentIdentity` es distinta.
- [ ] `SemanticContextIdentity` es derivada y materialization-invariante (I-005).
- [ ] Persistence y Materialization son independientes (I-006).
- [ ] `ProviderCacheReference` es opaca y sin rol de correctness (I-007).
- [ ] Scope y lifecycle son conceptos distintos; `execution` es scope válido.
- [ ] Las matrices A, B y C están presentes y no contienen celdas inventadas.
- [ ] Los invariantes I-001…I-012 están definidos.
- [ ] No hay definiciones de provider, adapters, backends, umbrales ni formatos de materialización.
- [ ] Las citas `ruta:sección` resuelven contra el repo; la batería de verificación está en verde.

## Amendment Log

- 2026-08-29 — Creación.
- 2026-08-29 — Surgical revision after architectural consistency review: ancla de versión de composición aclarada (I-012); `SegmentContentIdentity` vs `SegmentIdentity` distinguidas con ejemplo; elegibilidad semántica vs admisión/provider capability/uso efectivo separadas; memoization de Discovery downgraded a condicional; frontera de determinismo de materialización explicitada; elegibilidad de persistence separada del estado actual; configuración de worker acotada por rol semántico; participación de dominios acotada; roles owner/consumer/implementer aclarados.
- 2026-08-29 — Finalización: semántica de igualdad de `SemanticContextIdentity` y `project_identity` como ancla de namespace de composición explicitadas; sin cambios arquitectónicos.
- 2026-08-29 — Aceptada (plan 86): modelo semántico de Context Persistence y Cacheability formalizado como fuente de verdad; cambio docs-only, sin impacto en `protocol/.agents/`; la implementación de persistence, materialización y telemetría queda en las RFCs 72–74.
