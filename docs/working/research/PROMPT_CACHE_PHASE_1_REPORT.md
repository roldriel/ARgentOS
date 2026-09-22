# Prompt Cache Protocol — Phase 1 Report

**Fase:** 1 — Arquitectura, Semántica, Readiness & MVP Definition
**Modo:** READ-ONLY. No se modificó, creó ni borró ningún archivo del repositorio; no se ejecutaron commits; no se crearon RFCs, ADRs ni planes. El único artefacto escrito es este informe, en `docs/working/research/` (Working, no normativo).
**Baseline auditado:** `dev` @ `4314d5e`; `protocol/.agents/VERSION` = `11.4.0`; ancla del runtime `PROTOCOL_VERSION` = `11.4.0`; working tree limpio salvo `.codegraph/` untracked.
**Convención de evidencia:** HECHO (demostrado por archivo/código/test/salida de comando citada), INFERENCIA (derivada de hechos), PROPUESTA (recomendación sin autoridad), UNKNOWN (el repo no contiene la información), HUMAN DECISION REQUIRED (autoridad humana).

---

## 1. Executive Summary

**El hallazgo central: Prompt Cache en ARgentOS Protocol no está en fase de diseño. Está parcialmente construido, y lo que falta no es el mecanismo de cache — es el prefijo que ese mecanismo debería reutilizar.**

Facts que sostienen esa afirmación:

1. **Existe una serie de gobernanza completa y aceptada.** RFC-71 (Context Persistence & Cacheability), RFC-72 (Provider Prompt Cache Capability), RFC-73 (Project & Discovery Context Persistence) y RFC-74 (Cache Economics, Telemetry, Admission Evidence) están `Accepted` (`docs/rfc/INDEX.md:82-85`), y ocho planes (86–93) las materializaron: seis `Executed` con cambios en payload/runtime/tools/tests (`docs/plans/INDEX.md:128-129,150-152,165-166`).

2. **Existe un modelo semántico materializado en el payload.** `protocol/.agents/standards/context/CONTEXT.md:230-352` define clasificación Stable/Dynamic, segmentos Core/Project/Worker, `SegmentContentIdentity`, `SegmentIdentity` y `SemanticContextIdentity`. Esto es normativa del producto, no documentación suelta.

3. **Existe una implementación de referencia de la capacidad.** `runtime/toolcalls/identity.py`, `canonical.py`, `provider_cache.py` y `cache_coordinator.py` implementan identidades derivadas, materialización canónica determinista, la frontera del adapter y el flujo lookup/hit/miss/admisión. `runtime/README.md:50-118` declara el contrato.

4. **Existe el contrato de observabilidad.** `protocol/.agents/contracts/METRICS.md:67-68` define `reuse_event` y `provider_cache_event`; `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:85-168` define el catálogo `Reuse and cache` y los invariantes I-ECO-001…I-ECO-006 sin umbrales.

5. **NO existe integración real con ningún proveedor.** Búsqueda completa del repositorio: cero ocurrencias de `cache_control`, `prompt_cache`, `cache_creation_input_tokens`, `cache_read_input_tokens`, `cached_tokens`; cero ocurrencias de `anthropic`, `openai`, `bedrock`, `vertex`, ni de `requests.`/`urllib`/`httpx` en `runtime/`. El único adapter es `NullProviderAdapter` con `mechanism="none"` (`runtime/toolcalls/provider_cache.py:131-155`). **El repo implementa la capacidad, no su uso** (`docs/plans/89-…md:493-497`).

6. **NO existe un componente que escriba la telemetría.** `reuse_event`/`provider_cache_event` aparecen únicamente en el contrato, en `tools/aggregate_metrics.py` (lector) y en tests. No hay productor. El plan 91 lo declara explícitamente "NOT IMPLEMENTED… a defined architectural integration limit, not an implemented end-to-end execution path".

7. **El problema real (HECHO, medido):** la materialización canónica es el `ExecutionContext` de 8 campos (`runtime/toolcalls/context.py:47-63`), y su payload completo mide **606 bytes** en un caso de prueba. La porción común entre dos invocaciones que solo difieren en `session_uuid` es de **117 bytes** — y esos 117 bytes son la etiqueta JSON fija, no contexto. Dentro de una misma sesión, `state`, `phase` y `task` cambian por delegación y están **antes** de `knowledge_entries` y `skills` en el orden de facto (`runtime/toolcalls/canonical.py:56-68`).

   Y el contenido estable que sí se repite entre invocaciones —bootstrap del protocolo, módulos de workflow, roles, policies, gates, `SKILL.md` de skills activadas y entradas KB— **no está en la materialización canónica**. Llega al modelo por lecturas de archivo que el Worker ejecuta después, gobernadas por el contrato (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:111-122`: "Reads the target workflow module… reads each skill's `SKILL.md`"), fuera del artefacto que el adapter del provider recibe.

**Conclusión arquitectónica.** La infraestructura de Prompt Cache (identidad, materialización canónica, frontera de provider, admisión, contrato de observabilidad) está construida y es correcta en su diseño; el prefijo estable que debería alimentarla no está dentro de la representación que llega al provider. Por lo tanto el MVP de Prompt Cache **no es "conectar un adapter real"**: eso produciría misses sistemáticos contra un prefijo de 117 bytes. El MVP es (a) decidir qué contenido estable entra en la materialización dirigida al provider y en qué orden, (b) preservar la semántica de identidad ya definida, y (c) obtener evidencia del provider de que el hit ocurre y reduce tokens.

**Terminal status:** `PHASE_1_READY_FOR_HUMAN_DECISIONS` — hay dos decisiones normativas que ninguna evidencia del repositorio resuelve por sí sola (HD-1: qué entra en la materialización; HD-2: si el orden de materialización pasa a ser normativo).

---

## 2. Repository Baseline

| Hecho | Evidencia |
|---|---|
| Rama `dev`, HEAD `4314d5e` (`feat(protocol): add adversarial-deliberation capability (plan 120, RFC-77, v11.4.0)`) | `git log --oneline -5` |
| Working tree limpio salvo `.codegraph/` untracked | `git status --porcelain` |
| `protocol/.agents/VERSION` = `11.4.0` | `protocol/.agents/VERSION` |
| Ancla semántica del runtime = `11.4.0` | `runtime/toolcalls/canonical.py:37`; verificado por `tools/check_version_state.py:87-101` |
| METRICS contract schema = `2.0.0` (ambas ocurrencias) | `protocol/.agents/contracts/METRICS.md:2,8` |
| Payload: `protocol/.agents/` (producto) + `protocol/_AGENTS.md`; DEV: `.agents/` (5 archivos); tooling: `tools/` (17), `runtime/` (13), `tests/` (24) | inventario de árbol |
| No hay runtime ejecutable del protocolo: el "runtime" es un agente LLM leyendo documentos | `docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md:25` |

**Capas y su rol en esta investigación** (frontera declarada por el propio repo):

- `protocol/.agents/` = **producto** (data, no instrucciones de DEV). Define el protocolo.
- `runtime/` = **implementación de referencia del lado runtime**; "no es protocolo: es el lado del runtime de la frontera protocolo/runtime" (`runtime/README.md:6`).
- `tools/`, `tests/` = tooling dev; `docs/` = autoridad/historia.

---

## 3. Current Protocol Architecture

### 3.1 Pipeline de primera clase (reconstruido del repo)

```text
Orchestrator (rol)
  │  Execution Context Assembly Process — 7 responsabilidades:
  │  Source Discovery → Context Collection → Context Organization →
  │  Candidate Prioritization → Context Resolution → Context Composition →
  │  Context Delivery
  │  (protocol/.agents/orchestrators/core/roles/orchestrator.md:317)
  ↓
Delegation Payload  (transporte — protocolo)
  │  protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:21-60
  ↓
═══ protocol / runtime boundary ═══   (docs/rfc/13-…md:162-182)
  ↓
Materialization  (representación — runtime)
  │  runtime/toolcalls/prompt_rendering.py | toolcalls_rendering.py
  ↓
Canonical Materialization  (determinista — RFC-72)
  │  runtime/toolcalls/canonical.py:95-157
  ↓
Provider Adapter (runtime/toolcalls/provider_cache.py) → Provider API → provider-side cache
```

### 3.2 Naturaleza real del pipeline de contexto

HECHO: el pipeline de contexto **no tiene enforcement mecánico ni determinismo de bytes**. `protocol/.agents/standards/context/CONTEXT.md:5-18` lo declara canónico: "Context assembly… is **judgment with ordered criteria**… every criterion is evaluated by the Orchestrator by judgment when assembling a payload. Nothing in the context pipeline is machine-enforced".

HECHO: el harness **no gatea** la composición ni el budget de contexto. `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:50-62`: "The protocol does not truncate or block at delegation time; compliance is measured and auditable, never silent."

**Consecuencia arquitectónica (INFERENCIA):** la composición semántica es juicio; el determinismo de bytes solo puede exigirse —y solo se exige— a la materialización. Esto coincide exactamente con la frontera que RFC-71 §2 y RFC-72 §3 establecen, y es la razón por la que el modelo separa `SemanticContextIdentity` (semántica, invariante a materialización) de `MaterializationIdentity` (representación).

### 3.3 Alcance REAL de esta feature

HECHO: Prompt Cache es una feature **del Protocol**, no de DEV. El payload del producto contiene la normativa (`CONTEXT.md`, `PROTOCOL_BOUNDARIES.md`, `BUDGET_MATERIALIZATION.md`, `KNOWLEDGE_LIFECYCLE.md`, `METRICS.md`, `PROTOCOL_METRICS.md`); `runtime/` es la implementación de referencia del lado runtime; `.agents/` (capa DEV) no contiene ni una línea sobre cache.

HECHO: DEV fue contexto histórico de investigación únicamente (auditorías y research de `docs/working/`). No se diseñó Prompt Cache para DEV.

---

## 4. Prompt Cache Semantics

### 4.1 Los diez conceptos, separados

La consigna pedía distinguir diez conceptos. Estado real de cada uno en ARgentOS:

| # | Concepto | ¿Existe? | Dónde / estado | Pertenece al problema |
|---|---|---|---|---|
| 1 | **Context Persistence** | Normativo, parcialmente implementado | `CONTEXT.md:264-352`; store derivado `.project/knowledge/project_segment.json` (`runtime/toolcalls/project_store.py`) | **Ortogonal.** `I-006` |
| 2 | **Context Reuse** | Existe como transporte, no como cómputo | `input_artifacts` en el payload; `WORKER_DELEGATION_CONTRACT.md:111-122` | No es Prompt Cache |
| 3 | **Memoization** | Conceptual; condicional en Discovery | `docs/rfc/71-…md:263-267`; frescura/hashes de Discovery | **Ortogonal.** `docs/rfc/71-…md:8` |
| 4 | **Retrieval** | Existe (selección) | `context_discoverer` → `KB_RECOMMENDATION.md`; `orchestrator.md:148-157` | No es Prompt Cache |
| 5 | **Local cache owned by ARgentOS** | **No existe** | — (no hay store de materializaciones ni de prompts) | **Fuera** (ver §20) |
| 6 | **Provider-side Prompt Cache** | Frontera implementada; **no integrada** | `runtime/toolcalls/provider_cache.py`; `NullProviderAdapter` | **Es el problema** |
| 7 | **Provider cache reference / handle** | Existe, deliberadamente opaco | `ProviderCacheReference` (`provider_cache.py:75-85`); `docs/rfc/72-…md:183-189` | **Sí, encapsulado** |
| 8 | **Stable prompt prefix** | **Definido, pero hoy vacío en la práctica** | Definición en `docs/rfc/72-…md:140-147`; cómputo en `canonical.py:160-182`; medición: 117/606 bytes | **Es el problema** |
| 9 | **Semantic equivalence** | Definido y ejecutable | `SegmentContentIdentity`/`SegmentIdentity`/`SemanticContextIdentity` (`CONTEXT.md:280-322`; `identity.py`) | **Correctness**, no cache |
| 10 | **Materialization equivalence** | Definido y ejecutable | `MaterializationIdentity` + I-MAT-001 (`identity.py:280-309`; `canonical.py`) | **Representación**, no cache hit |

### 4.2 Qué debe ocurrir para que dos invocaciones reutilicen una porción procesada

**Respuesta (fundamentada, no intuitiva):** para que el provider pueda reutilizar una porción previamente procesada, deben cumplirse **cuatro** condiciones independientes, y ARgentOS solo controla las dos primeras:

```text
(1) ARgentOS: la representación dirigida al provider contiene una porción
    inicial byte-idéntica entre las dos invocaciones.
        → responsabilidad: materialización (runtime)   [HOY: NO se cumple más
          allá de 117 bytes]
(2) ARgentOS: esa representación es determinista dada la misma identidad
    semántica y la misma identidad de materialización.
        → responsabilidad: Canonical Materialization   [HOY: SÍ se cumple;
          verificado por I-MAT-001 y sus tests]
(3) Adapter: la capacidad del provider existe y se declara.
        → responsabilidad: adapter                     [HOY: solo
          NullProviderAdapter; UNKNOWN para cualquier provider real]
(4) Provider: decide crear, mantener, reutilizar y cobrar el cache.
        → responsabilidad: provider                    [HOY: UNKNOWN]
```

(1) ∧ (2) son condición necesaria, no suficiente. (3) ∧ (4) no son controlables por ARgentOS.

### 4.3 Responsabilidad por capa (frontera reconstruida)

```text
ARgentOS context construction   → Orchestrator por juicio; sin determinismo de bytes
context assembly                → Orchestrator; 7 responsabilidades, todo [agent]
prompt/materialization          → runtime; determinista por contrato (I-MAT-001)
provider adapter                → traduce capacidad abstracta a API del provider
provider API                    → UNKNOWN (no implementado)
provider-side prompt caching    → provider-owned; ARgentOS no lo modela
```

**Regla de diseño ya establecida por el repo (HECHO):** "todo comportamiento específico de provider… permanece detrás de la frontera del Provider Adapter. El protocolo semántico no depende de esos campos" (`docs/rfc/72-…md:177-181`). Esta regla es correcta y no requiere cambio.

---

## 5. Context Composition

### 5.1 Quién hace qué (HECHO)

| Pregunta | Respuesta | Evidencia |
|---|---|---|
| ¿Quién decide qué contexto se incluye? | El Orchestrator, por juicio con criterios ordenados | `orchestrator.md:317`; `CONTEXT.md:5-18` |
| ¿Quién lo ensambla? | El Orchestrator (Execution Context Assembly Process) | `orchestrator.md:315-335` |
| ¿Quién puede agregar contexto? | El Orchestrator; el `context_discoverer` **recomienda** (no incluye) | `orchestrator.md:148-157` |
| ¿Quién puede mutarlo? | El Orchestrator. El Worker lo **consume**; `runtime/` solo lo **representa** | `runtime/README.md:31-36` (criterio 3: "No retroalimenta el pipeline") |
| ¿Quién conoce el orden de composición? | El Orchestrator (juicio). El orden **de bytes** lo conoce el runtime | `COMPOSITION_OPTIMIZATION.md:15,29` |
| ¿Quién conoce la identidad? | Nadie hoy: **el payload no transporta identidades**; el runtime las deriva | `runtime/toolcalls/identity.py:3-4` |
| ¿Quién conoce el provider? | Solo el adapter | `docs/rfc/72-…md:177-181` |
| ¿Quién conoce el cache? | Solo el adapter y el coordinator | `cache_coordinator.py` |
| ¿Quién debe permanecer agnóstico? | Orchestrator, Worker, Skill, y todo `protocol/.agents/` | `PROTOCOL_BOUNDARIES.md:113-119` |

### 5.2 Categorías de composición y sus fuentes

El modelo del Protocol clasifica el Execution Context en cinco categorías (`orchestrator.md:315-317`): **Identity, Task, Knowledge, Capability, Execution Metadata**.

La estructura jerárquica solicitada (`Core → Project → Execution/Task → Worker/Skill → Dynamic`) **no existe exactamente así**. El modelo real es de **segmentos semánticos** (no jerárquicos): Core / Project / Worker (`CONTEXT.md:266-278`), con clasificación ortogonal Stable/Dynamic que ocurre *después* de la composición y no la retroalimenta (`CONTEXT.md:232-234`).

### 5.3 Tabla de clasificación por fuente de contexto

| Fuente | Origen | Ownership | Estabilidad | Mutabilidad | Lifecycle | Scope | Identity | Orden | Dependencias | ¿Reutilizable? | Invalidación |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bootstrap (`_AGENTS.md`, `INDEX.md`, state machines, rol orquestador) | Core | Protocolo | **STABLE** | inmutable por sesión | por versión del payload | core | `SegmentIdentity(core)` | no normado | versión de protocolo | Sí (semánticamente) | cambio de payload |
| Workflow module de la fase | Worker | Protocolo | **STABLE** | inmutable | por versión | worker | `SegmentIdentity(worker)` | no normado | fase | Sí | cambio de payload |
| Role / profile | Worker | Protocolo | **STABLE** | inmutable | por versión | worker | idem | no normado | fase | Sí | cambio de payload |
| Harness policy del gate | Worker | Protocolo | **STABLE** | inmutable | por versión | worker | idem | no normado | trigger | Sí | cambio de payload |
| Skills activadas (`SKILL.md`) | Worker | Protocolo / proyecto | **SEMI-STABLE** | inmutable; la **selección** cambia | por versión + activación | worker (protocol-global) / project | idem | no normado | fase + perfil | Sí | cambio de skill o de selección |
| Standards citados por referencia | Core/Worker | Protocolo | **STABLE** | inmutable | por versión | core/worker | idem | no normado | fase | Sí | cambio de payload |
| KB de discovery (`executive_summary.md` + entradas + manifest) | Project | Proyecto | **SEMI-STABLE** | cambia por rediscovery | TTL 6h/24h + hashes | project | `SegmentIdentity(project)` | no normado | frescura, provenance | Sí, si fresca | TTL, hash, `invalidated_facts` |
| Entradas curadas / lessons | Project | Proyecto | **SEMI-STABLE** | curación | freshness por claim | project | entry key (no identidad semántica) | no normado | curación | Sí | expiración / provenance rota |
| `task_summary` | Task | Orchestrator | **DYNAMIC** | reescrito por delegación | por delegación | execution | no tiene | no normado | spec | No | siempre cambia |
| `input_artifacts` (paths) | Task | Sesión | **DYNAMIC** | cambia por fase | artifact lifecycle | session | no tiene | no normado | fase | No (reuso entre sesiones prohibido) | nueva fase |
| `knowledge_entries` (excerpts) | Knowledge | Orchestrator | **DYNAMIC–SEMI** | re-resumidos | por delegación | execution | no tiene | no normado | selección + budget | Parcialmente | cambio de selección |
| `session_uuid`, `current_state`, `target_phase`, `context_budget` | Execution Metadata | Orchestrator/runtime | **DYNAMIC** | por invocación | por invocación | execution/session | no tienen | no normado | — | No | siempre |
| Tool results / measurements | Execution | Worker | **DYNAMIC** | append | registro | execution | no tienen | no normado | comando | Memoizable (con fingerprint) | cambio de código/entorno |
| Estado de ejecución (`state.json`) | Execution | Runner | **DYNAMIC** | por transición | session | session | no tiene | no normado | gates | No | transición |
| `communication_style`, `technical_approach`, `profile`, `harness_policy` | Execution Metadata | Orchestrator | **SEMI/DYNAMIC** | según flags | por delegación | execution | **no participan** | no normado | flags | No | cambio de flags |

Evidencia de la columna "Estabilidad": `CONTEXT.md:236-244` (clasificación) y `docs/rfc/71-…md:56-58` (regla de clasificación). Evidencia de "no normado" en Orden: `docs/rfc/72-…md:131-138` ("**Estado del orden concreto: OPEN / DEFERRED.** No existe evidencia en el repo de un orden de materialización normativo").

---

## 6. Stable / Semi-Stable / Dynamic Context

### 6.1 Las tres categorías (no se inventan categorías nuevas)

El Protocol formaliza **dos** categorías: Stable y Dynamic (`CONTEXT.md:230-262`), complementarias y exhaustivas. **SEMI-STABLE no existe como categoría del Protocol.** La consigna la pide; se reporta aquí como lente analítica, no como normativa del repo, y se marca como tal.

### 6.2 STABLE — qué es, en concreto

**Definición normativa:** "contenido cuya representación canónica es determinista dada su identidad y cuya semántica no depende de estado mutable por ejecución" (`CONTEXT.md:236-241`).

Ejemplos concretos del Protocol:
- Bootstrap: `protocol/_AGENTS.md`, `protocol/.agents/INDEX.md`, `SYSTEM_STATE_MACHINE.md`, `AGENT_STATE_MACHINE.md`, `orchestrator.md` (`docs/rfc/71-…md:70`).
- Worker: workflow module de la fase, policy del gate, rol y perfil, skills activadas (`docs/rfc/71-…md:72`).
- Knowledge persistente y fresco: KB de discovery como project segment (`docs/rfc/71-…md:71`).

Qué provoca cambios: cambio de versión del payload (todo), cambio de skill, cambio de KB.
Cómo se detecta: `content_identity` (SHA-256 del contenido canónico) + `semantic_version` (`CONTEXT.md:282-301`).
¿Debe invalidar reutilización? **Sí, es invalidación semántica** (`CONTEXT.md:339-352`).
¿Puede permanecer dentro de un prefix cacheable? Definido como elegible; **en la implementación actual no está en la materialización** (§9.4).
¿Su posición afecta el caching? Sí: es la única porción que *debería* ir primero.

### 6.3 SEMI-STABLE (lente analítica, no categoría del Protocol)

Contenido que cambia bajo condiciones pero puede mantenerse estable durante una secuencia de operaciones:

- Skills activadas: la lista cambia por delegación (activación por fase/perfil), pero cada `SKILL.md` es inmutable. HECHO: la activación se decide por delegación (`orchestrator.md:352-358`).
- KB excerpts: mismo contenido de entrada, distinto recorte por budget. HECHO: el budget por fase cambia (8000/4000 chars, `CONTEXT.md:42-47`).
- `input_artifacts`: los paths cambian por fase, pero un artefacto ya producido es inmutable dentro de la iteración (`PROTOCOL_BOUNDARIES.md:48-53`).

¿Detectable el cambio? Solo por juicio + selección registrada en `SESSION_LOG.md` (`CONTEXT.md:74-76`). No hay fingerprint de la selección.

### 6.4 DYNAMIC — qué es, en concreto

**Definición normativa:** "contenido dependiente de la ejecución o mutable por invocación… Complemento de Stable Context" (`CONTEXT.md:242-244`).

Ejemplos: Task (`task_summary` reescrito por delegación), knowledge excerpts re-derivados, Execution Metadata, artefactos de sesión, estado, observaciones y resultados (`CONTEXT.md:242-244`).

### 6.5 No-equivalencias que el Protocol ya declara (HECHO)

```text
stable ≠ persisted
dynamic ≠ ephemeral
stable ≠ provider prompt cache          (CONTEXT.md:253-259)
Stable Context  ≠ Stable Prefix         (docs/rfc/72-…md:140-147)
provider capability = YES  ⇏  actual cache use = YES   (I-MAT-008)
semantic eligibility = YES ⇏  actual cache use = YES   (I-MAT-009)
provider cache miss        ⇏  semantic invalidation     (I-MAT-005/006)
```

Estas separaciones son correctas y cubren la mayoría de las confusiones que la consigna pedía evitar. **No requieren cambio.**

---

## 7. Context Assembly and Ordering

### 7.1 ¿Existe un orden canónico actualmente?

**Respuesta: NO a nivel Protocol; SÍ a nivel runtime de referencia, y son inconsistentes entre sí.**

| Nivel | ¿Orden definido? | Evidencia |
|---|---|---|
| **Protocolo — prioridad de inclusión** | SÍ (semántica, no bytes) | `CONTEXT.md:20-27`: (1) task spec, (2) artefactos de la sesión, (3) entradas KB, (4) workflow module |
| **Protocolo — orden de bytes de la materialización** | **NO — OPEN / DEFERRED** | `docs/rfc/72-…md:131-138`: "No existe evidencia en el repo de un orden de materialización normativo"; "La hipótesis `core → project → worker → dynamic` queda registrada como candidato no normativo, sujeto a medición (RFC-D), no como invariant" |
| **Protocolo — forma del payload** | SÍ (adecuación, no orden de bytes) | `COMPOSITION_OPTIMIZATION.md:13-19`, criterio 1: "Ordering by consumption… Content appears in the priority order of `CONTEXT.md` §1" |
| **Runtime de referencia** | SÍ — `OrderingContract` v1 | `canonical.py:44-68`: `session → state → phase → role → task → context_budget → knowledge_entries → skills` |

### 7.2 Clasificación del orden actual

- **Explícitamente normativo:** la *prioridad de inclusión* (`CONTEXT.md:1`) y el *criterio de ordenamiento por consumo* (`COMPOSITION_OPTIMIZATION.md:2.1`). Ambos son `[agent]` — juicio, sin gate mecánico (`COMPOSITION_OPTIMIZATION.md:9`).
- **Implícitamente determinístico:** nada.
- **Dependiente de implementación:** el orden de bytes. El runtime lo declara versionado y lo documenta como "evidencia, no diseño nuevo" (`docs/plans/89-…md:76-79`).
- **Accidental / no definido a nivel Protocol:** el orden de bytes.

### 7.3 DRIFT NORMATIVO (hallazgo)

El orden de facto del runtime (`session, state, phase, role, task, context_budget, knowledge_entries, skills`) **no es el orden de prioridad de consumo del Protocol** (`CONTEXT.md:20-27`): la task spec es prioridad 1 en el Protocolo pero aparece **quinta** en el runtime; el workflow module es prioridad 4 pero no está en la materialización; `knowledge_entries` es prioridad 3 pero aparece séptimo.

Ambas cosas pueden ser legítimas —una es prioridad semántica de inclusión, la otra es layout de bytes— pero el repo **no declara explícitamente esa distinción como resuelta**. `COMPOSITION_OPTIMIZATION.md:15` dice "Content appears in the priority order of `CONTEXT.md` §1", lo que leído literalmente contradice el orden del runtime. Se reporta como **NORMATIVE DRIFT (no bloqueante para correctness, bloqueante para cache)**.

### 7.4 Por qué el orden es necesario para Prompt Cache (fundamento)

Los providers con prompt caching reutilizan **prefijos**. Consecuencias directas, sin asumir mecánica propietaria:

1. Un byte volátil en posición temprana trunca el prefijo reutilizable en ese punto.
2. El orden actual pone **cuatro campos volátiles primero** (`session`, `state`, `phase`, `role`) — `canonical.py:56-68`.
3. Medición empírica (HECHO, reproducible): dos invocaciones con idéntico `state`, `phase`, `role`, `task`, `budget` y distintos solo en `session_uuid` → payload de 606 bytes cada una, **prefijo común de 117 bytes**. Los 117 bytes son `semantic_context_identity: {"project_identity":null,"protocol_version":"11.4.0","segments":["{...` — es decir, la etiqueta y el comienzo del hash. El hash del SCI ya difiere porque `session_uuid` participa en el contenido del segmento worker (`identity.py:216-227`).
4. Dentro de una misma sesión, `current_state` y `target_phase` cambian por delegación (`orchestrator.md:320-322`).

**Conclusión:** el orden actual hace que el prefijo cacheable sea, en el mejor caso, ~117 bytes — por debajo de cualquier mínimo cacheable declarable (`min_cacheable_tokens` existe en el contrato abstracto: `provider_cache.py:49`).

### 7.5 Mínimo mecanismo necesario (PROPUESTA, no decisión)

1. Declarar qué porción de la materialización es **estable-por-construcción** y debe ir primero.
2. Versionar ese orden como parte de `MaterializationIdentity.ordering_contract_version` — **ya existe** (`identity.py:255-277`).
3. Registrar la elección en el contrato de materialización del runtime — **ya existe** (`canonical.py:44-68`, `runtime/README.md:66-72`).

Lo que **falta** es únicamente (1): el *contenido* estable todavía no está en la materialización (§9.4). La gobernanza para (2) y (3) ya está construida y es suficiente.

### 7.6 ¿Requiere nueva gobernanza?

- **No** para versionar el orden: `ordering_contract_version` ya es un componente de `MaterializationIdentity` (`docs/rfc/72-…md:89,104-111`) y está cubierto por tests (`tests/test_canonical_materialization.py:610-624`).
- **Sí, probablemente** para declarar normativamente **qué** entra en la materialización dirigida al provider. Eso toca la frontera protocolo/runtime (`docs/rfc/13-…md:145-152`) y el alcance de RFC-72. → **HUMAN DECISION REQUIRED (HD-1)**.

---

## 8. Identity Analysis

### 8.1 Las identidades existentes

| Identidad | Qué identifica | Qué NO identifica | Inputs | Estabilidad | Owner | Depende de provider/model | Depende de materialización | ¿Detecta equivalencia para Prompt Cache? |
|---|---|---|---|---|---|---|---|---|
| `SegmentContentIdentity` | Igualdad del contenido canónico de un segmento | No identifica versión ni namespace; no identifica semántica | `SHA-256(canonical_content)` | Determinista | RFC-71 | No | No | Parcial (solo content equality) |
| `SegmentIdentity` | Identidad semántica *scoped* de un segmento | No identifica representación ni provider | `{semantic_version, content_identity, namespace}` | Determinista (I-001) | RFC-71 | No | No | Parcial |
| `SemanticContextIdentity` | El contexto semántico compuesto | **No** identifica materialización, orden, serialización, provider, model, TTL, cache policy (I-005) | `{protocol_version, project_identity, segments[]}` | Determinista (I-004) | RFC-71 | No | **No, por diseño** | **Correctness, no hit** |
| `MaterializationIdentity` | Las *reglas* de representación | No identifica contenido semántico | `{materialization_version{variant, ordering_contract_version, serialization_version}, provider?, model?, model_version?}` | Determinista | RFC-72 | Condicional | Es materialización | Aproxima el hit |
| `ProviderCacheReference` | Nada que ARgentOS pueda interpretar | No es identidad; no es autoridad de correctness (I-MAT-004) | `{opaque: str}` | **Opaca** | Provider/adapter | Sí | No | **Explícitamente no** |
| `change_identity` (RFC-76) | Un Change del payload | — | RFC-71 `SegmentIdentity` sobre `{target, declaration, protocol_version, namespace}` | Determinista | RFC-76 | No | No | No aplica |

Evidencia: `identity.py:54-198`, `identity.py:255-309`, `provider_cache.py:75-85`, `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:83-110`.

### 8.2 La regla crítica, verificada

> Semantic equivalence NO necesariamente implica cache equivalence.
> Materialization equivalence NO necesariamente implica provider cache equivalence.
> `SegmentIdentity` NO necesariamente es suficiente para determinar que un provider puede reutilizar una porción previamente cacheada.

HECHO: las tres afirmaciones están **correctamente** modeladas por el Protocol:
- `docs/rfc/72-…md:191-200`: "`Semantic identity match ≠ provider cache hit`; `Provider cache miss ≠ semantic context invalid`".
- `docs/rfc/72-…md:301-308` (Matrix C): cuatro de las cinco combinaciones producen resultados distintos de "reuse".
- `docs/rfc/71-…md:251-261`: un Stable Context puede producir prefixes distintos bajo distintas `MaterializationIdentity`.

### 8.3 ¿Dónde termina ARgentOS y dónde empieza el provider?

```text
ARgentOS garantiza (y puede verificar):
  · SegmentContentIdentity / SegmentIdentity / SemanticContextIdentity  → correctness
  · MaterializationIdentity                                             → reglas de representación
  · Canonical Materialization determinista (I-MAT-001)                  → bytes reproducibles
  · Separación de los tres dominios de invalidación                     → no conflación

El adapter garantiza (y debe declarar):
  · ProviderCapability abstracta (mechanism, prefix_only, breakpoints,
    min_cacheable_tokens, ttl, extended_ttl, model_scoped, isolation_scope)
  · Traducción a la API concreta
  · Reportar hit | miss | unavailable

El provider posee (UNKNOWN para ARgentOS):
  · cuándo crea/reutiliza/expira/evicta
  · cómo calcula equivalencia internamente
  · cómo cobra; qué tokens considera cache-read/cache-write
  · qué modelos soporta; headers y flags concretos
  · el valor y la semántica de ProviderCacheReference
```

### 8.4 Hallazgo de completitud de identidad (HECHO, y es un defecto)

`SemanticContextIdentity` se deriva de `ExecutionContext`, que es un **subconjunto** del Delegation Payload:

| Campo del Delegation Payload | ¿En `ExecutionContext`? |
|---|---|
| `session_uuid`, `current_state`, `target_phase`, `role_to_adopt`, `task_summary`, `knowledge_entries`, `skills`, `context_budget` | SÍ (`context.py:56-63`) |
| `profile` | **NO** |
| `input_artifacts` | **NO** |
| `harness_policy` | **NO** |
| `communication_style` | **NO** |
| `technical_approach` | **NO** |

Evidencia: `WORKER_DELEGATION_CONTRACT.md:21-60` vs `runtime/toolcalls/context.py:47-63`. El módulo declara "It introduces no new concepts: every field corresponds to a field of the invocation payload" (`context.py:6-9`) — afirmación **inexacta**.

**Consecuencia:** dos payloads que difieren solo en `input_artifacts` (por ejemplo, una iteración que lee `TASK_SPECIFICATION.md` vs otra que lee además `EXECUTION_PLAN.md`) producen **la misma** `SemanticContextIdentity`, el mismo `MaterializationIdentity` y el mismo payload canónico. El test `test_semantic_context_identity_covers_delivered_composition` (`tests/test_canonical_materialization.py:239-247`) solo verifica sensibilidad a `session_uuid`, no cobertura completa.

Clasificación: **IMPLEMENTATION DRIFT** respecto del propio modelo que el módulo declara consumir. No rompe la correctness semántica del cache (un miss es aceptable) pero **degrada la premisa de I-MAT-001**: la materialización no cubre el contexto entregado, solo parte de él.

---

## 9. Materialization Analysis

### 9.1 Qué significa materializar (HECHO)

"La transformación de un Execution Context en una representación propia de un runtime: aquella que solo ese runtime puede producir y consumir" (`docs/rfc/13-…md:119-131`). Ocurre **después** del pipeline, **pertenece al runtime**, **no altera el contenido conceptual**, **no es única**, **no retroalimenta el pipeline**.

### 9.2 Parámetros que influyen

`MaterializationIdentity = { provider?, model?, model_version?, materialization_version{variant, ordering_contract_version, serialization_version} }` (`docs/rfc/72-…md:104-111`; `identity.py:280-309`).

Reglas de participación (HECHO, normativas): `provider`/`model`/`model_version` son **condicionales**; `materialization_version` **siempre** participa. La regla explícita: "una restricción de aislamiento del cache del provider (p. ej., 'el cache es model-scoped') **no** convierte automáticamente esa dimensión en parte de `MaterializationIdentity`" (`docs/rfc/72-…md:81`).

### 9.3 ¿Qué hace que dos materializaciones sean equivalentes?

```text
same SemanticContextIdentity + same MaterializationIdentity
    → same Canonical Materialization            (I-MAT-001)
```

Implementado en `canonical.py:95-157` y verificado por `tests/test_canonical_materialization.py:310-317`. Propiedades verificadas:
- Serialización determinista: UTF-8, sin BOM, LF, sin whitespace final variable (`canonical.py:1-16`; test `:319-324`).
- Variante, ordering contract y serialization version deben coincidir con el contrato implementado, o se levanta `ValueError` (`canonical.py:112-131`).
- `MI change` no cambia `SCI` (I-MAT-002, test `:326-333`); `SCI change` no se preserva por mismo `MI` (I-MAT-003, test `:335-343`); materialización fuera de `SCI` (I-MAT-012, test `:345-355`).

### 9.4 HALLAZGO CENTRAL — la materialización canónica no contiene el contexto estable

**HECHO.** La materialización canónica se construye sobre `ExecutionContext`, cuyos únicos campos son los 8 listados en §8.4. Los renderers (`prompt_rendering.render_prompt`, `toolcalls_rendering.render_prompt`) emiten **nombres** de skills, no su contenido:

```python
# runtime/toolcalls/prompt_rendering.py:37-44
if context.skills:
    lines.append("skills:")
    for skill in context.skills:
        lines.append(f"  - {skill.name}")
    lines.append("instruction: read each skill's SKILL.md before executing the phase; ...")
```

**HECHO.** El contenido estable que se repite entre invocaciones llega al modelo por lecturas posteriores, gobernadas por el contrato del producto: "the Worker MUST read each skill's `SKILL.md` before executing the phase" (`WORKER_DELEGATION_CONTRACT.md:92`); el workflow module y el perfil se leen en la ejecución del Worker (`:114,116`).

**HECHO (medido).** El payload canónico completo de una invocación representativa mide 606 bytes y contiene: header (`semantic_context_identity`, `materialization_identity`, `variant`, `ordering_contract_version`, `serialization_version`), y el cuerpo con session/state/phase/role/task/budget/knowledge_entries/skills-names. Los documentos que dominan el prompt real (bootstrap, workflow, rol, policy, `SKILL.md`, KB) no están en él.

**INFERENCIA (fuerte).** Bajo el contrato actual, la porción estable disponible para prompt caching es aproximadamente nula más allá del header. Integrar un adapter real **hoy** produciría misses sistemáticos.

### 9.5 Respuesta a la pregunta obligatoria

> ¿Prompt Cache debe operar sobre Context Identity, sobre Materialization Identity, sobre una identidad derivada, o dejar completamente la equivalencia de cache en manos del provider?

**Respuesta fundamentada: sobre ninguna identidad de ARgentOS para determinar el hit; solo sobre `MaterializationIdentity` para determinar qué representación es comparable.**

Fundamento:
1. La equivalencia de cache **pertenece al provider** y es UNKNOWN para ARgentOS. `docs/rfc/72-…md:183-189` ya decidió que `ProviderCacheReference` es opaca y que ARgentOS "no infiere correctness a partir de ella". Esa decisión es correcta: ARgentOS no puede saber cómo el provider calcula equivalencia.
2. `SemanticContextIdentity` responde a *correctness*, y su uso indebido para decidir un hit introduciría exactamente el falso positivo que la consigna prohíbe ("false hit unacceptable"): dos contextos con la misma semántica pueden materializarse distinto.
3. `MaterializationIdentity` es la única identidad que **ARgentOS controla y que correlaciona con bytes**. Es lo que permite decir "estas dos invocaciones produjeron la misma representación byte a byte". Eso es condición necesaria, no suficiente, y por eso el resultado sigue siendo `hit | miss | unavailable` reportado por el adapter.
4. **No se requiere identidad derivada nueva.** `(SemanticContextIdentity, MaterializationIdentity)` ya es la clave de lookup del coordinator (`cache_coordinator.py:85-88`) y es suficiente.

**Sí se requiere un cambio distinto y no-identitario:** que la representación contenga el contenido estable. Eso es materialización, no identidad.

---

## 10. Provider Boundary

### 10.1 ¿Existe una abstracción `ProviderCacheIdentity` / `CacheHandle` / `CacheKey` / `Cache-Control`?

**NO, y la ausencia es una decisión normativa tomada, no un olvido.**

| Concepto pedido | ¿Existe? | Qué existe en su lugar | Evidencia |
|---|---|---|---|
| `ProviderCacheIdentity` | **No** — nombre explícitamente rechazado | `ProviderCacheReference` | `docs/rfc/71-…md:460` (alternativa 6 rechazada) |
| `ProviderCacheReference` | **Sí** | `@dataclass(frozen=True) ProviderCacheReference(opaque: str)` | `provider_cache.py:75-85` |
| `CacheHandle` | No | idem | — |
| `CacheKey` | **No** — "una cache key universal" está en el alcance excluido de RFC-72 | lookup key local = `(SCI, MI)` | `docs/rfc/72-…md:410`; `cache_coordinator.py:85-88` |
| `Cache-Control` | **No** — cero ocurrencias en el repo | `ProviderCapability` abstracta | búsqueda completa |
| Capacidad abstracta | **Sí** — contrato exacto | `mechanism, prefix_only, breakpoints, min_cacheable_tokens, ttl, extended_ttl, model_scoped, isolation_scope` | `docs/rfc/72-…md:160-175`; `provider_cache.py:26-73` |

### 10.2 Evaluación de la regla de diseño propuesta

> ARgentOS no debería intentar modelar internamente detalles propietarios del mecanismo de caching de cada provider salvo que exista una necesidad arquitectónica demostrada.

**HECHO: el estado actual ya cumple esta regla, y de forma ejemplar.** Tres capas separadas explícitamente (`docs/rfc/72-…md:57-63`):

| Concern | Owner | Provider-owned |
|---|---|---|
| `MaterializationIdentity` | RFC-72 / ARgentOS | NO |
| Provider cache isolation | Provider / Adapter | Sí |
| Provider cache state | Provider | Sí |

No hay campos de OpenAI/Anthropic/Gemini en el payload; no hay pricing; no hay TTL universal; no hay eviction universal. La regla se cumple sin necesidad de cambio.

### 10.3 ¿Hace falta algo más en la frontera?

HECHO: la frontera está completa **como contrato** y vacía **como implementación**. `NullProviderAdapter` es el default y el límite de tests (`provider_cache.py:131-155`).

UNKNOWN (y correctamente marcado como tal por el repo):
- si algún provider real concreto satisface el contrato abstracto;
- si el prefijo de 117 bytes supera el `min_cacheable_tokens` de algún provider;
- si el reporting de tokens cacheados existe y con qué nombres;
- si `ProviderCacheReference` es persistible entre procesos.

Estos huecos **no deben rellenarse con supuestos** en Phase 2; deben resolverse contra la documentación del provider elegido, en el momento de elegirlo.

### 10.4 Estrategia de inicio: provider-neutral core, evidencia empírica después (PROPUESTA)

Propuesta de secuenciación para Phase 2 (no decisión):
1. Elegir **un** provider con prompt caching documentado y escribir **un** adapter real que solo declare capacidad y traduzca el prefijo.
2. Usar el **mecanismo más simple disponible** (implicit prefix caching si existe) antes de introducir breakpoints explícitos.
3. No añadir dimensiones provider-específicas a `MaterializationIdentity` salvo que la representación canónica difiera por provider (`docs/rfc/72-…md:92`).

---

## 11. Orchestrator / Worker / Skill Responsibilities

| Pregunta | Respuesta (HECHO) | Evidencia |
|---|---|---|
| ¿Quién selecciona contexto? | Orchestrator (juicio); `context_discoverer` recomienda | `orchestrator.md:317`, `:148-157` |
| ¿Quién ensambla contexto? | Orchestrator | `orchestrator.md:315-335` |
| ¿Quién puede agregar contexto? | Orchestrator. El Worker **no** construye su Execution Context | `orchestrator.md:488` ("MUST NOT invoke more than one phase per worker instance"); `WORKER_DELEGATION_CONTRACT.md:184-188` |
| ¿Quién puede mutarlo? | Solo el Orchestrator | idem |
| ¿Quién conoce el orden? | Protocolo: nadie normativamente. Runtime: `OrderingContract` v1 | §7 |
| ¿Quién conoce la identidad? | **Nadie en el protocolo**; el runtime la deriva | `identity.py:3-4` |
| ¿Quién conoce el provider? | El adapter | `docs/rfc/72-…md:177-181` |
| ¿Quién conoce el cache? | El adapter y el coordinator | `cache_coordinator.py` |
| ¿Quién debe permanecer agnóstico? | Orchestrator, Worker, Skill, todo `protocol/.agents/` | `PROTOCOL_BOUNDARIES.md:113-119` |

### 11.1 La regla existente que Prompt Cache puede usar

HECHO (regla ya establecida, útil): "el Worker no debería construir su propio Execution Context cuando el modelo actual ya establece que el Orchestrator lo construye". El repo la enuncia como constraint del Orchestrator y del Worker (`orchestrator.md:485-490`; `WORKER_DELEGATION_CONTRACT.md:182-188`).

**Evaluación:** esta garantía es **suficiente** para Prompt Cache y **no necesita endurecerse** para el MVP, porque:

1. La materialización consume el Execution Context ya producido y "no retroalimenta el pipeline" (`runtime/README.md:31-36`, criterio 3).
2. La selección de skills y perfil se registra y es auditable (`orchestrator.md:347,356`).
3. La frontera protocolo/runtime está modelada y es de responsabilidad, no de implementación (`docs/rfc/13-…md:145-152`).

**Lo que sí falta** no es un endurecimiento de esta regla, sino declarar **qué** constituye el Execution Context a efectos de materialización (§9.4). Es un problema de completitud de la representación, no de autoridad.

---

## 12. Scope and Isolation

### 12.1 Scopes existentes (HECHO)

Scope = "dominio semántico de procedencia". Valores: `core`, `project`, `worker`, `session`, `execution` (`CONTEXT.md:324-330`). **Scope no es** lifetime, persistence, cacheability, memoization, isolation, frontera de seguridad ni TTL (`CONTEXT.md:326-330`).

Isolation = "cada scope semántico es un namespace de aislamiento, y contenido igual en distintos scopes no es el mismo contexto" (`CONTEXT.md:332-337`).

### 12.2 Qué puede reutilizarse

| Ámbito | ¿Reutilizable? | Condición | Evidencia |
|---|---|---|---|
| Dentro del mismo project | SÍ | namespace = `ProjectIdentity` | `docs/rfc/71-…md:271-280` |
| Entre sesiones del mismo project | SÍ (knowledge), sujeto a frescura | TTL + hashes + provenance | `docs/rfc/73-…md:89-100` |
| Entre projects | **NO** por defecto. "el reuso cross-project está **prohibido salvo autorización explícita**" | I-008 | `docs/rfc/71-…md:271-280` |
| Contexto externo importado | No definido como reutilizable | — | UNKNOWN (no hay mecanismo en el repo) |
| Contextos derivados (Project Segment) | SÍ, dentro del namespace | store derivado, rebuildable | `docs/rfc/73-…md:206-225` |
| Cambio de governance rule | Invalida (payload versionado en bloque) | `semantic_version` | `docs/rfc/71-…md:301-313` |
| Cambio de Skill | Invalida el Worker segment | `content_identity` | idem |
| Cambio de Worker | Invalida el Worker segment | idem | idem |
| Cambio de Protocol version | Invalida **todo** | `semantic_version` | idem |

### 12.3 Política isolation-first y sus consecuencias

**Regla obligatoria de la consigna, evaluada:** "false hit unacceptable; false miss acceptable".

Consecuencia arquitectónica directa (INFERENCIA): **el MVP debe preferir la sobre-invalidación a la sub-invalidación en todo punto de duda.** Eso tiene tres consecuencias concretas y verificables:

1. `session_uuid` dentro del content del segmento (`identity.py:216-227`) garantiza que **dos sesiones nunca comparten SCI**. Esto es una sobre-invalidación maximalista: imposible un false hit cross-session, imposible también un hit real cross-session. Es coherente con isolation-first, y es la causa de que el prefijo sea de 117 bytes (§7.4). **HUMAN DECISION REQUIRED (HD-3)**: ¿se acepta el costo (cero reuso cross-session) o se separa el identificador de sesión del contenido semántico?
2. No implementar deduplicación cross-project es la decisión correcta y ya está tomada; el contenido igual **no** implica permiso (`docs/rfc/71-…md:271-280`).
3. El aislamiento del store derivado es por `ProjectIdentity` = `PROJECT_REGISTRY.project_id`, sin fallback derivado de path (`runtime/toolcalls/project_segment.py:57-72`). HECHO correcto: proyectos sin Project ID no tienen store.

---

## 13. Invalidation / Freshness

### 13.1 Los tres dominios (HECHO, ya modelados y no conflables)

```text
1. Invalidación semántica   → correctness      (cambio de content_identity o semantic_version)
2. Invalidación de materialización → representación (cambio de MaterializationIdentity)
3. Cache del provider       → provider-owned   (TTL, eviction, invalidación, unavailability)
```

Evidencia: `docs/rfc/72-…md:202-233`; `CONTEXT.md:339-352`; `KNOWLEDGE_LIFECYCLE.md:47-62`.

Regla normativa: "un cache miss del provider **nunca** es invalidación semántica" (`docs/rfc/72-…md:210`).

### 13.2 Clasificación de eventos

| Evento | Clasificación | Fundamento |
|---|---|---|
| Cambio de Protocol version | **MUST INVALIDATE** (semántica + materialización) | `semantic_version` es componente (`CONTEXT.md:288-301`); payload inmutable por versión (`PROTOCOL_BOUNDARIES.md:144-153`) |
| Cambio de governance | **MUST INVALIDATE** (vía versión de payload) | `docs/rfc/71-…md:306` |
| Cambio de AGENTS/instructions | **MUST INVALIDATE** (Core segment) | `docs/rfc/71-…md:303` |
| Cambio de Skill | **MUST INVALIDATE** (Worker segment) | `docs/rfc/71-…md:304` |
| Cambio de Worker (workflow/rol/policy) | **MUST INVALIDATE** (Worker segment) | `docs/rfc/71-…md:306` |
| Cambio de Project context (KB) | **MUST INVALIDATE** (Project segment) | `docs/rfc/71-…md:303`; frescura |
| Cambio de Session context | **MUST INVALIDATE** de hecho | `session_uuid` en content → SCI distinto |
| Cambio de Execution Context | **MUST INVALIDATE** | `SegmentContentIdentity` cambia |
| Cambio de tools (schema) | **MUST INVALIDATE** (Worker segment) | `docs/rfc/71-…md:305` |
| Cambio de tool state | **DOES NOT INVALIDATE** el contexto semántico | tool result es scope `execution`, no cacheable (`docs/rfc/71-…md:349`) |
| Cambio de provider | **MUST INVALIDATE materialización** (si el contrato difiere) | `docs/rfc/72-…md:85,92` |
| Cambio de model | **MAY INVALIDATE** (condicional, solo si cambia el contrato de representación) | `docs/rfc/72-…md:86,94` |
| Cambio de model version | **MAY INVALIDATE / DEFERRED** | `docs/rfc/72-…md:87,96` |
| Cambio de materialization version | **MUST INVALIDATE materialización** | `docs/rfc/72-…md:90,230` |
| Cambio de prompt format | **MUST INVALIDATE materialización** | serialization/variant son componentes |
| Cambio de configuration (flags) | **UNKNOWN / MAY** | `communication_style`/`technical_approach` no están en `ExecutionContext` → **hoy NO invalidan, y deberían** (§8.4) |
| Cambio de relevant runtime state | **DOES NOT INVALIDATE** el SCI | `state.json` no participa |
| TTL del provider | **PROVIDER OWNED** | I-MAT-007 |
| Eviction del provider | **PROVIDER OWNED** | I-MAT-006 |

### 13.3 ¿Qué necesita el MVP?

| Mecanismo | ¿Necesario? | Fundamento |
|---|---|---|
| TTL | **NO** | "el TTL nunca es el mecanismo de correctness" (I-009); el TTL del provider es provider-owned |
| Invalidación explícita | **NO como mecanismo nuevo** | La invalidación semántica es por identidad, y ya es mecánica |
| Invalidación derivada | **NO** | No hay grafo de dependencias de materializaciones |
| Invalidación por versión | **SÍ — ya existe y es suficiente** | `semantic_version` + `materialization_version` |
| Cleanup manual | **NO** | No hay store ARgentOS-owned que limpiar |
| Persistencia de la referencia del provider | **UNKNOWN** | Depende del provider; hoy in-memory (`cache_coordinator.py:84-88`) |

**Conclusión:** el MVP **no necesita ningún mecanismo de invalidación nuevo**. La invalidación por identidad ya implementada cubre el 100% de los casos MUST INVALIDATE de la tabla anterior. El único hueco (flags que no invalidan) es un defecto de completitud de `ExecutionContext`, no un mecanismo faltante.

---

## 14. Observability / Telemetry

### 14.1 Contrato disponible

HECHO: `protocol/.agents/contracts/METRICS.md:67-68` define dos tipos de evento:

```text
reuse_event            layer(discovery|knowledge|materialization)
                       operation(lookup|eligibility|reuse_attempt|post_use)
                       + lookup_result | eligibility_decision | reason |
                         reuse_outcome | invalidated
provider_cache_event   result(hit|miss|unavailable)
                       + tokens_cached | tokens_uncached | latency_ms |
                         reference_present
```

HECHO: `PROTOCOL_METRICS.md:85-110` define el catálogo `Reuse and cache` con columnas de Evidence class, Availability, Scope, Provider dependency e Invariante; y `:146-168` los invariantes I-ECO-001…I-ECO-006.

HECHO: `tools/aggregate_metrics.py:375,416` **lee** ambos tipos y agrega por capa sin doble conteo.

### 14.2 Clasificación de cada señal pedida

| Señal | Clasificación | Evidencia |
|---|---|---|
| Intento de reutilización | **Derivable** del contrato; **no producido** | `reuse_event(operation=reuse_attempt)` definido; cero productores |
| Cache hit | **Requiere provider + adapter**; contrato listo, no producido | `provider_cache_event(result=hit)` |
| Cache miss | idem | idem |
| Bypass | **Derivable** (admission policy falsa) | `cache_coordinator.py:60-72`; `events` expone `cache unavailable` |
| Invalidation | **Derivable** vía `reuse_event(operation=post_use, invalidated=true)`; no producido | `METRICS.md:67` |
| Provider rejection | **Derivable** como `result=unavailable` | `provider_cache.py:23` |
| Provider cache-read | **Requiere provider** (UNKNOWN si el provider lo expone) | — |
| Provider cache-write | **Requiere provider** (UNKNOWN) | — |
| Tokens procesados | **Requiere nueva instrumentación** en el runtime; hoy Unavailable | `PROTOCOL_METRICS.md:130-144` (declara tokens no instrumentados salvo cached/uncached) |
| Tokens cacheados / no cacheados | **Requiere provider**; "Unavailable" declarado | `PROTOCOL_METRICS.md:100` |
| Coste | **Imposible actualmente** (sin pricing, por decisión) | `METRICS.md:90-92`; RFC-74 no define pricing |
| Latencia | Parcial: solo `cache.latency_ms`, "NOT AVAILABLE" | `PROTOCOL_METRICS.md:101` |
| Contador de invocaciones LLM | **Imposible con el catálogo actual** | solo hay `delegation` (por delegación), no por llamada |
| Retrieval counter | **Imposible** | no existe |

### 14.3 El hueco crítico (HECHO)

**No existe productor de telemetría.** El plan 91 lo declara: el writer host/orchestrator está "NOT IMPLEMENTED"; la frontera productor→artefacto es "a defined architectural integration limit, not an implemented end-to-end execution path"; y el plan **prohíbe** afirmar "fully connected"/"end-to-end implemented"/"producer integrated".

Evidencia independiente verificada por búsqueda completa: `reuse_event` y `provider_cache_event` aparecen en `METRICS.md`, `aggregate_metrics.py`, `check_session_artifacts.py` y tests. **Cero ocurrencias en `runtime/`.**

### 14.4 ¿Cómo demostraríamos que Prompt Cache redujo tokens y no solo que "intentamos" usarlo?

**Respuesta:** la única evidencia admisible es **provider-reported**. Todo lo demás es attestation.

```text
EVIDENCIA VÁLIDA (clase measurement / verification externa):
  provider reporta tokens_cached > 0 y/o cache_read_input_tokens
  para la segunda invocación, con el mismo prefijo que la primera,
  y el conteo se corrobora contra un payload capturado.

EVIDENCIA INVÁLIDA:
  "nuestro código llamó a admission_policy y devolvió True"
  "calculamos el prefijo común por nuestra cuenta y es grande"
  "el hit rate subió"
  "el adapter devolvió hit" sin tokens asociados
```

Fundamento normativo ya existente: `protocol/.agents/standards/quality/EVIDENCE.md:54-63` — una afirmación es `verified` solo con evidencia de clase distinta de `attestation`; REL-001 exige "Gate State PASS + non-attestation evidence". Y `PROTOCOL_METRICS.md:112-126` exige que toda métrica declare su clase (Observed / Estimated / Derived / Unavailable) y prohíbe fabricar data points.

**Regla para el MVP (PROPUESTA):** el closure predicate de Prompt Cache debe exigir evidencia de clase `Observed` (provider-reported). Sin ella, el resultado máximo admisible es "capacidad implementada, ahorro no demostrado".

---

## 15. Security

### 15.1 Riesgos y su tratamiento

| Riesgo | Estado en el repo | Tratamiento requerido |
|---|---|---|
| **Secretos / credenciales** | Ya prohibido incluir en payload: `CONTEXT.md:29-36` ("must never include: Binary files, credentials, tokens, or personal data"); `METRICS.md:101` | Ninguno nuevo |
| **PII** | idem | Ninguno nuevo |
| **Contenido sensible** | `ENVIRONMENT_PROBE.md:83-111` define whitelist, filtrado de strings prohibidas y anonimización de paths | Reutilizar |
| **Cross-project leakage** | Prohibido por I-008; namespace por `ProjectIdentity`; test de aislamiento existe (`tests/test_project_segment.py:568-611`) | Reutilizar |
| **Cross-session leakage** | Imposible por construcción (`session_uuid` en SCI) | Ver HD-3 |
| **Stale context** | Tres dominios de invalidación + freshness por claim (KN-005) | Reutilizar |
| **Authorization** | `AUTHORIZATION.md`; `effects` en `TASK_SPECIFICATION.md` | Ninguno nuevo |
| **Governance state** | Change Governance Artifact (`CHANGE_GOVERNANCE.md`) | Ninguno nuevo |
| **Human decisions** | Registradas como pending decisions con owner (PC-1) | Ninguno nuevo |
| **Normative verdicts** | Verdict = attestation, nunca verification (`orchestrator.md:292-298`) | Ninguno nuevo |
| **Closed artifacts** | Inmutables por política de trazas históricas (RFC-46) | Ninguno nuevo |
| **External imported context** | UNKNOWN — no hay mécanismo en el repo | Marcar UNKNOWN; no inventar |

### 15.2 Qué contenido NO debe formar parte de un segmento reutilizable

HECHO, ya normado o derivable sin mecanismo nuevo:

```text
NUNCA en un segmento reutilizable:
  · credenciales, tokens, secretos, datos personales   (CONTEXT.md:29-36)
  · contenido de proyecto de otro namespace            (I-008)
  · artefactos completos de sesiones previas           (CONTEXT.md:29-36, Omission rules)
  · logs o reportes de otras sesiones                  (idem)
  · contenido no relevante a la fase actual            (idem)

PUEDE formar parte de contexto estable:
  · bootstrap, workflow, rol, perfil, policies, gates  (Core/Worker segments)
  · SKILL.md de skills activadas                       (Worker segment)
  · KB de discovery fresca con provenance resoluble    (Project segment)

REQUIERE isolation:
  · todo el Project segment → namespace = ProjectIdentity
  · skills de proyecto → per-project

REQUIERE invalidation:
  · cualquier segmento cuyo content_identity o semantic_version cambie

FUERA DEL MVP:
  · un sistema de clasificación de datos completo (no es necesario; las
    reglas de omisión existentes alcanzan)
  · telemetría que persista contenido semántico (prohibido por la Privacy
    rule: METRICS.md:97-99)
```

**Conclusión de seguridad:** el MVP **no requiere un sistema de clasificación de datos nuevo**. Las omisiones de `CONTEXT.md:2`, la Privacy rule de `PROTOCOL_METRICS.md` y el aislamiento por namespace ya cubren los riesgos identificados. Añadir clasificación sería complejidad sin evidencia.

---

## 16. Governance

### 16.1 Qué governance controla cada dominio hoy

| Dominio | Gobernanza existente | Naturaleza |
|---|---|---|
| Context | `CONTEXT.md` + 7 policies de contexto + `BUDGET_MATERIALIZATION.md` | Normativa (`[agent]`, sin gate) |
| Skills | `SKILLS.md` + `skills/INDEX.md` + `skill-lifecycle` (RFC-24) | Normativa + activación por tabla |
| Workers | `WORKER_DELEGATION_CONTRACT.md` + roles + profiles | Contrato |
| Execution Context | RFC-01/02 + `orchestrator.md:5` | Normativa conceptual |
| Materialization | RFC-13/14 + RFC-72 | Normativa + contrato runtime |
| Provider | RFC-72 §6-7; `provider_cache.py` | Contrato abstracto |
| Changes | RFC-56 (clases A/B/C) + RFC-75 (Change Lifecycle) + RFC-76 (CGA) | Normativa |
| Artifacts | RFC-63 + contratos | Normativa |
| Authority | `DECISIONS.md` + `AUTHORIZATION.md` + ADR-16 | Normativa |

### 16.2 Qué parte de Prompt Cache necesita cada tipo de gobernanza

| Elemento | Tipo requerido | Estado |
|---|---|---|
| Semántica Stable/Dynamic, segmentos, identidades, aislamiento | **Normativa** | **HECHO: ya existe** (`CONTEXT.md:230-352`) |
| Separación de dominios de invalidación | **Normativa** | **HECHO: ya existe** (`CONTEXT.md:339-352`) |
| Frontera de cache / no implementación de provider cache | **Normativa** | **HECHO: ya existe** (`PROTOCOL_BOUNDARIES.md:107-119`) |
| No-modificación del Context Budget por caching | **Normativa** | **HECHO: ya existe** (`BUDGET_MATERIALIZATION.md:64-82`) |
| `MaterializationIdentity`, I-MAT-001…012 | **Contractual** | **HECHO: ya existe** (RFC-72 + `canonical.py`) |
| `ProviderCacheReference` opaca | **Contractual** | **HECHO: ya existe** |
| Eventos `reuse_event`/`provider_cache_event` | **Contractual** | **HECHO: ya existe** (`METRICS.md`) |
| Invariantes I-ECO-001…006 | **Contractual** | **HECHO: ya existe** |
| Orden de materialización normativo | **Decisión no tomada** | OPEN/DEFERRED (`docs/rfc/72-…md:138`) |
| Escritura de telemetría | **Runtime** | **AUSENTE** |
| Adapter real de provider | **Runtime-enforced** | **AUSENTE** |

### 16.3 Advertencia sobre garantías documentales vs runtime

HECHO, y es el punto más delicado: **`protocol/.agents/` declara garantías que el runtime no respeta.** El propio repo lo reconoce en dos lugares:

- `CONTEXT.md:5-18`: "Nothing in the context pipeline is machine-enforced: the budget is measured but not truncated or blocked at delegation time… the deterministic checks named as 'harness Future Extensions' across the Resolution/Composition policies are possibilities, not guarantees."
- `PROTOCOL_METRICS.md:220-235` y `harness/INDEX.md:96-100`: las clases Declarative / Verifiable / Mechanically enforced / Agent-judgment-dependent / External-actor-dependent determinan quién verifica; "Hooks remain fail-open; this matrix does not declare them an absolute control (ENF-003)".

**Consecuencia para Prompt Cache:** el MVP **no debe apoyarse en ninguna garantía documental que no sea mecánicamente verificable**. Las únicas garantías que Prompt Cache puede usar como base son:
1. I-MAT-001 (determinismo de materialización) — **verificado por tests**.
2. Determinismo de identidad (I-001/I-004) — **verificado por tests**.
3. Opacidad de la referencia (I-MAT-004) — **verificado por tests**.
4. Ausencia de reuso cross-project (I-MAT-011) — **verificado por tests**.

Todo lo demás (que el Orchestrator efectivamente incluya X, que el Worker efectivamente lea Y, que el budget se respete) es juicio sin gate. **No debe convertirse en premisa de un mecanismo de cache.**

### 16.4 ¿Hace falta governance nueva?

**Evaluación honesta: probablemente no.**

- La semántica está.
- El contrato de materialización está.
- El contrato de observabilidad está.
- La separación de dominios está.

Lo que falta es **decisión** (HD-1/HD-2/HD-3) e **implementación** (contenido estable en la materialización; adapter real; writer de telemetría). Ninguno de esos tres requiere un artefacto de gobernanza nuevo si la decisión humana sobre HD-1/HD-2 se registra como enmienda de RFC-72 (que ya es `Accepted` y tiene `Amendment Log` — camino ya usado cuatro veces por la propia serie).

---

## 17. Change Lifecycle Integration

### 17.1 El Change Lifecycle existente (a usar, no a rediseñar)

HECHO: pipeline vigente = **authorize → execute → verify → close → commit → promote** (RFC-56 + RFC-75 + `docs/VERSIONING.md:4`).

Clases de cambio (RFC-56): Clase A = RFC `Accepted`; Clase B = plan aprobado; Clase C = fix mecánico.

HECHO: el propio repo ya ejecutó esta serie por el camino correcto: RFC-71/72/73/74 → `Accepted` (planes 86/87/92/93) → implementación (planes 88/89/90/91) → verificación (batería) → commit atómico → `Executed`.

### 17.2 Qué necesitaría Prompt Cache Phase 2

| Elemento | Requerido | Fundamento |
|---|---|---|
| Artefactos que forman parte del Change | Enmienda a RFC-72 (decisión HD-1/HD-2); un plan de implementación; cambios en `runtime/`; posiblemente `protocol/.agents/` si HD-1 es normativo | RFC-56 |
| Validaciones necesarias | Batería canónica (`docs/VERSIONING.md:4.1`), Ver `## 17.3` | `docs/VERSIONING.md:4.1` |
| Evidencia que debe quedar | Validation Anchor (`declaration scope`, `command-set`, `effective inputs`, `Scoped Content Identity`) + Git checkpoint | RFC-75, Incrementos 1+3 (plan 96) |
| Cómo se hace dogfood | Ver §18 | — |
| Cómo se demuestra el cierre | `Closed` = `Executed` ∧ governance ∧ checkpoint ∧ consistencia; **derivada, no declarada** | `AGENTS.md:Task lifecycle` |
| Qué es informational evidence | El evento `provider_cache_event` es `informational` por contrato (`METRICS.md:6`); el hit observado | Contrato |
| Qué requiere enforcement | Nada nuevo. La garantía de determinismo (I-MAT-001) ya es verificable por tests | — |

**Diferencia obligatoria (HECHO):** `Executed ≠ Committed ≠ Closed ≠ Released` (`AGENTS.md:Task lifecycle`).

### 17.3 Batería canónica (verbatim, `docs/VERSIONING.md:4.1`)

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

HECHO: `check_dist_sync.py` es local-only y se espera **rojo en `dev`** por diseño (`AGENTS.md:Verifying the protocol`).

HECHO: si HD-1 modifica `protocol/.agents/`, se requiere bump de `VERSION` + sección de changelog + ancla `PROTOCOL_VERSION` del runtime sincronizada — y `tools/check_version_state.py:97-101` **falla** si no se sincroniza. Ese enforcement ya existe y es mecánico.

**No se modifica el Change Lifecycle en esta fase.**

---

## 18. Dogfood Design

### 18.1 Escenario propuesto (tentativo; NO ejecutado)

Objetivo: demostrar comportamiento real, no tests unitarios.

**Precondición:** un adapter real para **un** provider con prompt caching documentado, con `mechanism != "none"`.

```text
PASO 1 — Primera invocación (cache cold)
  · Construir el Execution Context con el contenido estable resuelto (HD-1).
  · Derivar SCI y MI; materializar canónicamente.
  · Capturar y CONSERVAR el payload byte-exacto (evidencia).
  · Enviar al provider. Registrar: tokens_cached=0 (o ausente),
    tokens_uncached=N1, latency_ms=L1, reference_present=?

PASO 2 — Verificar estabilidad del contexto
  · Recalcular SCI y MI con los mismos inputs.
  · Assert: SCI_1 == SCI_2 y MI_1 == MI_2.
  · Assert: payload_2 es byte-idéntico a payload_1 (I-MAT-001).
  · Assert: prefijo común == longitud total del payload.
  → Si esto falla, el dogfood se detiene: no hay prefijo, no hay nada que probar.

PASO 3 — Segunda invocación (cache warm)
  · Misma materialización, mismo provider, misma sesión y namespace.
  · Registrar: tokens_cached=N2 (> 0 esperado), tokens_uncached=N3, latency_ms=L2.

PASO 4 — Diferencia dinámica controlada
  · Cambiar SOLO el campo dinámico (p.ej. task_summary o el sufijo dinámico).
  · Assert: SCI cambia; MI NO cambia.
  · Registrar si el provider sigue reportando tokens_cached > 0
    (evidencia de que el prefijo cacheado se reutilizó pese al sufijo distinto).

PASO 5 — Evidencia del provider
  · tokens_cached_2 > 0 reportado por el provider; idealmente corroborable
    contra un segundo artefacto (clase Verified, no Recorded).
  · Si el provider NO expone tokens: declarar "saving no demostrado"
    y NO cerrar el MVP.

PASO 6 — Evidencia de ARgentOS
  · Payloads capturados, SCI/MI registrados, prefijo común calculado.
  · Eventos provider_cache_event/reuse_event efectivamente escritos
    en el METRICS.md de la sesión (requiere el writer: hoy ausente).

PASO 7 — Verificación de isolation
  · Ejecutar PASO 1 en un proyecto/namespace distinto con el MISMO payload.
  · Assert: ninguna referencia del namespace A es visible desde B.
  · Assert: ProviderCacheReference no cruza namespace.
  (Precedente de test: tests/test_project_segment.py:568-611.)

PASO 8 — Condición de invalidation
  · Cambiar el contenido estable (p.ej. una skill, una policy o la versión).
  · Assert: content_identity cambia → SCI cambia → MI cambia
    (si cambió el contrato de materialización).
  · Assert: el cache del provider da miss; el contexto semántico sigue válido.
  · Assert: NO se declara invalidación semántica por el miss.

PASO 9 — Comportamiento de fallback
  · Simular: provider sin soporte (mechanism=none) → cache unavailable;
    materialización y semántica válidas.
  · Simular: adapter devuelve unavailable → igual.
  · Simular: cache expira/evicta → miss; semántica intacta.
  (Todos ya cubiertos por tests unitarios: :464-482, :524-541, :541-554.)
```

### 18.2 Qué resultado SÍ sería suficiente para afirmar "Prompt Cache funciona"

```text
(1) El prefijo estable existe y es byte-idéntico entre las invocaciones
    comparables (PASO 2).
(2) El provider reporta tokens cacheados > 0 en la segunda invocación
    (PASO 5) — evidencia Observed, no Estimated.
(3) Ese conteo se corrobora contra un artefacto que el reporter no controla
    (clase Verified: EVIDENCE.md:112-118).
(4) El MISMO contexto semántico sigue siendo válido en todos los casos
    (ningún miss se interpretó como invalidación).
(5) El aislamiento cross-namespace se mantiene (PASO 7).
(6) El caso de invalidación produce miss sin alterar correctness (PASO 8).
(7) Los eventos quedaron registrados en METRICS.md (PASO 6).
```

### 18.3 Qué resultado NO sería suficiente

```text
✗ "admission_policy devolvió True"                      — no es uso
✗ "el adapter devolvió hit"                              — sin tokens no hay
                                                            evidencia de ahorro
✗ "calculamos que el prefijo común es grande"            — Estimated, no Observed
✗ "el hit rate subió"                                    — Hit rate ≠ Economic
                                                            Value (I-ECO-002)
✗ "los tests unitarios de I-MAT-001 pasan"               — prueba determinismo,
                                                            no reutilización real
✗ "reducimos el tamaño del payload"                      — puede excluir contexto
                                                            necesario
✗ Unidades mixtas sumadas (tokens + ms + USD)            — I-ECO-004/005
✗ Cualquier afirmación sin `provider_cache_event` escrito — attestation
```

### 18.4 Riesgo principal del dogfood

INFERENCIA: si HD-1 se resuelve como "sí, incluir el contenido estable", el payload canónico crecerá de ~600 bytes a potencialmente decenas de miles. Eso tensiona:
- el Context Budget (I-010 prohíbe que el caching altere sus límites semánticos);
- la regla "el caching no modifica silenciosamente los límites del Context Budget" (`BUDGET_MATERIALIZATION.md:64-82`);
- la distinción, ya normada, entre *semantic budget* / *physical cost* / *prompt materialization cost* (`BUDGET_MATERIALIZATION.md:77-82`).

Este riesgo **debe** ser tratado explícitamente en Phase 2, no descubierto en el dogfood.

---

## 19. Architectural Alternatives

Evaluación contra el estado real del repo.

### A — Provider-only: ARgentOS solo garantiza contexto estable; el provider cachea

| Dimensión | Evaluación |
|---|---|
| Beneficios | Cero complejidad nueva; ya es casi el estado actual |
| Costes | Ninguno directo |
| Complejidad | Mínima |
| Riesgos | **No funciona**: el contexto estable no está en la materialización (§9.4) → el provider no tiene prefijo que cachear |
| Seguridad | Igual |
| Observabilidad | Ninguna (sin adapter) |
| Aislamiento | Igual |
| Dependencia del provider | Total |
| Portabilidad | Total |
| Relación con la arquitectura | Respeta la frontera |
| Impacto en autonomy | Nulo |
| Entidades nuevas | Ninguna |
| Governance nueva | Ninguna |
| **Veredicto** | **Insuficiente por sí sola** — asume que el contexto estable ya está en el prompt del provider, y no lo está |

### B — Context Governance + Provider Cache: garantías mínimas de estabilidad/orden/identidad + adapter maneja el provider cache

| Dimensión | Evaluación |
|---|---|
| Beneficios | Usa la infraestructura existente (identidad, materialización canónica, frontera); añade solo lo que falta (contenido estable en la representación + orden); mantiene el core provider-agnóstico |
| Costes | Requiere decidir HD-1/HD-2; el payload canónico crece; requiere un adapter real y un writer de telemetría |
| Complejidad | Media, y **concentrada en el runtime** |
| Riesgos | Confundir "garantizar estabilidad" con "garantizar hit" (mitigado por I-MAT-005/008/009, ya normados) |
| Seguridad | Isolation-first ya normado; sin cambio |
| Observabilidad | Habilitada por el contrato existente; requiere el writer |
| Aislamiento | Ya normado y testeado |
| Dependencia del provider | Encapsulada en el adapter |
| Portabilidad | Alta (capacidad abstracta) |
| Relación con la arquitectura | **Alineada**: es la continuación natural de RFC-72, cuya §3 declara el contrato de materialización canónica como requisito |
| Impacto en autonomy | Positivo (ver §26) |
| Entidades nuevas | **Ninguna** — reusa SCI/MI/ProviderCacheReference |
| Governance nueva | Solo una enmienda a RFC-72 (camino ya usado) |
| **Veredicto** | **RECOMENDADA** |

### C — ARgentOS-owned cache: cache propia de prompts/contextos/materializaciones

| Dimensión | Evaluación |
|---|---|
| Beneficios | Control total; independiente del provider; posible reuso cross-session |
| Costes | Store, schema, eviction, GC, aislamiento físico, migraciones, invalidación por dependencia, fingerprinting de artifacts (que el repo **no tiene**: `docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md:369-376`) |
| Complejidad | **Alta** |
| Riesgos | **False hit**: reutilizar una materialización bajo inputs que cambiaron sin fingerprint verificable. Exactamente el riesgo que la consigna prohíbe |
| Seguridad | Requiere aislamiento físico nuevo (fuera del alcance que RFC-71/73 declararon) |
| Observabilidad | Requiere instrumentación nueva completa |
| Aislamiento | Requiere mecanismo nuevo |
| Dependencia del provider | Ninguna |
| Relación con la arquitectura | **Contradice** `docs/rfc/71-…md:206-214` (persistence es ortogonal y **no** prerrequisito) y `:458` (alternativa 5 rechazada) |
| Entidades nuevas | Store, schema, lifecycle, isolation |
| Governance nueva | Extensa |
| **Veredicto** | **Rechazada para el MVP** — ya rechazada por RFC-71, y sin fingerprint de artifacts produciría false hits |

### D — Hybrid: metadata/identidad local + cache real en el provider

| Dimensión | Evaluación |
|---|---|
| Beneficios | Es **exactamente** lo que existe hoy + el adapter que falta |
| Costes | Ninguno arquitectónico |
| Complejidad | Ya está construida |
| Riesgos | Ninguno nuevo |
| Relación con la arquitectura | Es el estado actual |
| Entidades nuevas | Ninguna |
| **Veredicto** | **Es la forma de B, ya construida en un 80%.** B = D + el contenido estable en la materialización + adapter real + writer |

### E — Alternativa adicional: Runtime-only optimization (declarar que el caching de re-lecturas pertenece al host)

| Dimensión | Evaluación |
|---|---|
| Descripción | ARgentOS no produce prefijo cacheable; el host/runtime cachea las lecturas de archivo (workflow, rol, skills) antes del provider. El protocolo solo mantiene la semántica |
| Beneficios | Cero cambio al protocolo; honesto con la frontera (RFC-13: la materialización es del runtime) |
| Costes | El ahorro no es atribuible a ARgentOS ni medible por su telemetría; el adoptante debe implementarlo |
| Riesgos | El "Prompt Cache Protocol MVP" se vuelve indistinguible de "no hacer nada" desde el payload |
| Relación con la arquitectura | **Compatible**, y reconocida por RFC-68 (`docs/rfc/68-…md:687-699`: "No hay cache en Fase 1; cachear re-lectura es Fase 2, gated a telemetría") |
| **Veredicto** | **Registrada como alternativa legítima.** Debe considerarse explícitamente porque el argumento de RFC-68 (gate a telemetría) sigue vigente y **la telemetría sigue sin existir** |

### 19.1 Recomendación

**B / D** — completar la materialización con el prefijo estable y conectar el provider cache detrás del adapter existente, reutilizando íntegramente las identidades, la frontera y el contrato de observabilidad ya construidos.

**Con una condición de secuenciación (fundada en evidencia):** la telemetría debe existir **antes o al mismo tiempo** que el adapter, porque (a) RFC-68 gatea la Fase 2 de cache a telemetría, y (b) sin writer de `provider_cache_event` el dogfood no produce evidencia admisible (§14.3, §18.2).

**Y con una advertencia:** la alternativa E es más barata y podría ser la respuesta correcta si HD-1 se resuelve como "el contenido estable no debe entrar en la materialización canónica". En ese caso el MVP correcto **no es construir cache en ARgentOS**, sino declarar que la optimización pertenece al host y cerrar el Change como "no change" — resultado legítimo según el Decision-Making Compass del repo (`AGENTS.md`).

---

## 20. Rejected / Deferred Scope

Cada rechazo se funda en evidencia, no en dogma.

| Elemento | Veredicto | Fundamento |
|---|---|---|
| Cache local genérico | **Rechazado** | Ortogonal por I-006; sin fingerprint de artifacts produciría false hits (`docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md:369-376`) |
| Database de cache | **Rechazado** | El repo es stdlib-only por convención (`runtime/README.md:16`); el store derivado existente es filesystem y rebuildable (`project_store.py`) |
| Registry global | **Rechazado** | `CHANGE_GOVERNANCE.md:197-198`: retrieval content-addressed, "no registry, no global index, no identity service". Precedente directo |
| Nueva state machine | **Rechazado** | `cache_coordinator.py:8-11` declara explícitamente que **no** es una state machine de protocolo |
| Nueva authority class | **Rechazado** | No hay decisión nueva de autoridad; la admisión es policy sin umbrales (`docs/rfc/72-…md:237`) |
| Nuevo workflow phase | **Rechazado** | La materialización no retroalimenta el pipeline (`runtime/README.md:35`) |
| Nuevo lifecycle | **Rechazado** | Los tres dominios de invalidación ya existen y son suficientes (§13.3) |
| Nueva identity primitive | **Rechazado** | `(SCI, MI)` es clave suficiente; RFC-71 rechazó explícitamente `ProviderCacheIdentity` (`docs/rfc/71-…md:460`) |
| Cross-project deduplication | **Rechazado** | I-008 lo prohíbe salvo autorización explícita |
| N-level cache hierarchy | **Rechazado** | No hay evidencia de más de una capa necesaria |
| Distributed cache | **Rechazado** | Sin evidencia; el store derivado asume single-writer (`project_store.py:14-20`) |
| TTL complejo | **Rechazado** | I-009: TTL nunca es correctness; el TTL del provider es provider-owned |
| Automatic semantic equivalence | **Rechazado** | La equivalencia semántica ya está definida y es por identidad; automatizarla no añade valor |
| Model-specific optimization abstractions | **Rechazado** | `model` es dimensión condicional de MI; no se crea abstracción de tokenizer (`docs/rfc/72-…md:98`) |
| Provider-specific behavior en el core | **Rechazado** | Viola la frontera de `docs/rfc/72-…md:177-181` |
| UI | **Rechazado** | Fuera del alcance del Protocol |
| Automatic invocation | **Rechazado** | La admisión es policy; `reuse >= 3` fue rechazado por RFC-71/72/73/74 |
| Cost optimizer | **Rechazado** | RFC-74 prohíbe pricing y umbrales; `CostModel`/`PricingModel` explícitamente non-goal del plan 91 |
| Generic memoization framework | **Rechazado** | `docs/rfc/71-…md:267`: "esta RFC no define un framework de memoization general" |
| Escribir `provider_cache_event` desde `runtime/` hacia `METRICS.md` | **DEFERRED** (no rechazado) | El writer es responsabilidad del Orchestrator/host por contrato; el plan 91 lo documenta como seam. Phase 2 debe decidir si el MVP lo requiere |

---

## 21. Minimum Viable Architecture

### EXISTING AND SUFFICIENT (no requiere modificación)

1. **Modelo semántico de contexto** — `CONTEXT.md:230-352`: Stable/Dynamic, segmentos Core/Project/Worker, scope, isolation, correctness por identidad.
2. **Identidades** — `SegmentContentIdentity`, `SegmentIdentity`, `SemanticContextIdentity` (`CONTEXT.md:280-322`; `identity.py:54-198`), con I-001/I-004/I-005/I-012 verificados por tests.
3. **`MaterializationIdentity` y sus reglas condicionales** — `docs/rfc/72-…md:77-115`; `identity.py:255-309`.
4. **I-MAT-001 verificable** — `canonical.py:95-157`; tests `:310-317`, `:319-324`.
5. **Serialización canónica determinista** — UTF-8, sin BOM, LF (`canonical.py:1-16`).
6. **Stable Prefix computable** — `canonical.py:160-182`; tests `:387-408`.
7. **Frontera del Provider Adapter** — `provider_cache.py:103-155`; `docs/rfc/72-…md:177-181`.
8. **`ProviderCacheReference` opaca** — `provider_cache.py:75-85`; I-MAT-004 testeado (`:449-462`).
9. **Coordinador lookup/hit/miss/admisión sin umbrales** — `cache_coordinator.py`; tests `:483-523`, `:627-642`.
10. **Tres dominios de invalidación** — `docs/rfc/72-…md:202-233`; tests `:524-554`, `:610-624`.
11. **Contrato de observabilidad** — `METRICS.md:67-68`; `PROTOCOL_METRICS.md:85-168`; agregador (`aggregate_metrics.py:375,416`).
12. **Aislamiento por ProjectIdentity** — `project_segment.py:57-72`; `project_store.py`; tests `:568-611`.
13. **Regla de no-modificación del Budget por caching** — `BUDGET_MATERIALIZATION.md:64-82`.
14. **Ancla de versión enforced mecánicamente** — `tools/check_version_state.py:97-101`.
15. **Batería canónica** — `docs/VERSIONING.md:4.1`.

### EXISTING BUT INSUFFICIENT (existe, requiere endurecimiento/extensión)

| # | Mecanismo | Por qué es insuficiente | Extensión mínima |
|---|---|---|---|
| 1 | **Canonical Materialization** | No contiene el contenido estable que el Worker lee después (§9.4). El prefijo útil es de 117 bytes | Incluir en la materialización dirigida al provider el contenido estable que hoy se lee aparte, o declarar explícitamente que esa porción no es responsabilidad de ARgentOS (ver HD-1) |
| 2 | **`ExecutionContext`** | Subconjunto del Delegation Payload: omite `profile`, `input_artifacts`, `harness_policy`, `communication_style`, `technical_approach` (§8.4) | Completar el mapeo o corregir la afirmación del módulo |
| 3 | **Ordering Contract v1** | Pone los campos volátiles primero (§7.4) | Reordenar estable-primero (ver HD-2) |
| 4 | **`session_uuid` en el content del segmento** | Impide todo reuso cross-session | Ver HD-3 |
| 5 | **Telemetría de reuse/cache** | Contrato completo, **cero productores** | Writer del host/orchestrator (o decisión explícita de que no es MVP) |
| 6 | **`ProviderCapability`** | Contrato abstracto sin ninguna instancia real | Un adapter real |

### MISSING (realmente ausente)

| # | Mecanismo | Estado |
|---|---|---|
| 1 | **Contenido estable dentro de la representación dirigida al provider** | Ausente. Es la pieza que decide si Prompt Cache puede existir |
| 2 | **Adapter de un provider real** | Ausente (`NullProviderAdapter` únicamente). Requiere decisión de qué provider |
| 3 | **Producer de `reuse_event`/`provider_cache_event`** | Ausente en runtime y en protocolo |
| 4 | **Evidencia provider-reported de tokens cacheados** | Ausente; la única medición válida de ahorro |

### PROVIDER OWNED (no debe pertenecer a ARgentOS)

- cuándo se crea/reutiliza/expira/evicta el cache;
- cómo el provider calcula equivalencia;
- pricing y billing;
- tokens cache-read/cache-write y sus nombres concretos;
- TTL del provider y evicción;
- la semántica de `ProviderCacheReference`;
- headers/flags concretos de la API.

### DEFERRED (útil, no necesario para el MVP)

- persistencia de `ProviderCacheReference` entre procesos;
- `model_version` como dimensión de MI (`docs/rfc/72-…md:87`);
- cache de tool results / memoización de mediciones (evidencia de alto valor pero ortogonal: `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:554` O5);
- evitación de rediscovery por TTL con hash sin cambio (O6);
- fingerprint de policy/prompt/worker (P2 del research);
- dashboards y experimentación económica (RFC-74 §18).

---

## 22. MVP Boundary

### IN SCOPE

1. **Decidir y materializar el prefijo estable** dentro de la representación dirigida al provider (HD-1/HD-2), preservando `SemanticContextIdentity` invariante a materialización (I-005).
2. **Un adapter real** para un provider con prompt caching documentado, que declare `ProviderCapability` y traduzca el prefijo, sin exponer semántica propietaria al core.
3. **Escritura efectiva de `provider_cache_event`** (result, tokens_cached, tokens_uncached, latency_ms, reference_present) en el `METRICS.md` de la sesión, para que el ahorro sea medible.
4. **Un dogfood** conforme a §18, con evidencia de clase `Observed` del provider.
5. **Corregir el mapeo `ExecutionContext` ↔ Delegation Payload** (§8.4) o corregir la afirmación del módulo.
6. **Enmienda de RFC-72** (Amendment Log) registrando las decisiones HD-1/HD-2/HD-3, si alteran el contrato de materialización.

### OUT OF SCOPE

- store de prompts o materializaciones owned by ARgentOS;
- backend de persistencia, schema, eviction, GC;
- deduplicación cross-project;
- jerarquía de cache de N niveles;
- cache distribuido;
- TTL universal o política de expiración de ARgentOS;
- pricing, billing, `CostModel`, `PricingModel`, tablas de precios;
- dashboards y framework de experimentación;
- umbrales económicos (`reuse >= N`, hit rate objetivo);
- framework general de memoization;
- clasificación de datos nueva;
- abstracción de tokenizer;
- registry global de identidades o de cache;
- state machine, workflow phase, lifecycle, authority class o identity primitive nueva;
- UI.

### NON-GOALS (podrían confundirse con Prompt Cache)

```text
✗ Context Persistence         → ortogonal (I-006); ya implementada para project
✗ Memoization                 → ortogonal (docs/rfc/71-…md:8)
✗ Retrieval                   → selección de conocimiento, no cache
✗ Context Reuse (transporte)  → reuso de artifacts vía input_artifacts
✗ Discovery freshness         → TTL + hashes, ya existente
✗ Project Segment store       → derivado, rebuildable, no autoritativo
✗ Reducir tamaño del payload  → es compresión de contexto, no cache
✗ Reducir costo de inferencia → es memoization o pruning, no cache
✗ Garantizar un hit           → imposible: provider-owned (I-MAT-008/009)
✗ Un "hit rate" como KPI      → prohibido por I-ECO-002
✗ Modelar la semántica del provider → viola la frontera de RFC-72 §7
```

---

## 23. Proposed Closure Predicate

```text
PROMPT_CACHE_PROTOCOL_MVP_CLOSED =
      P1  ∧ P2  ∧ P3  ∧ P4  ∧ P5  ∧ P6  ∧ P7  ∧ P8
    ∧ P9  ∧ P10 ∧ P11 ∧ P12 ∧ P13 ∧ P14 ∧ P15 ∧ P16
```

### Arquitectura y gobernanza

- **P1 — Decisión registrada.** HD-1, HD-2 y HD-3 tienen decisión humana registrada con evidencia y fecha. *Verificable:* la enmienda existe en el `Amendment Log` de RFC-72 o en el artefacto de gobernanza que corresponda.
- **P2 — Frontera preservada.** Cero campos, flags o semántica propietaria de provider en `protocol/.agents/`. *Verificable:* búsqueda de `cache_control`, nombres de provider y `Cache-Control` en el payload devuelve cero; `check_protocol_invariants.py` PASS.
- **P3 — Sin entidad nueva.** Ninguna identity primitive, state machine, lifecycle, registry ni authority class nueva. *Verificable:* el diff de `protocol/.agents/` no añade contratos ni archivos de state machine.

### Implementación

- **P4 — Prefijo estable materializado.** La materialización canónica contiene una porción inicial byte-idéntica entre invocaciones con el mismo `(SCI, MI)`, y esa porción incluye el contenido estable que la decisión HD-1 determine. *Verificable:* test que mide el prefijo común y lo compara contra un umbral declarado.
- **P5 — I-MAT-001 extendido.** Mismo `(SCI, MI)` ⇒ payload byte-idéntico, ahora sobre el alcance completo de la materialización. *Verificable:* `tests/test_canonical_materialization.py::test_imat001_materialization_determinism` PASS, con el nuevo contenido incluido.
- **P6 — Cobertura de identidad.** `SemanticContextIdentity` cubre todos los campos del Delegation Payload que afectan el contexto, o la omisión está declarada y justificada. *Verificable:* test que varía cada campo del payload y comprueba sensibilidad de SCI (o su exclusión declarada).
- **P7 — Adapter real.** Existe un `ProviderAdapter` concreto con `mechanism != "none"` que declara `ProviderCapability` y traduce el prefijo. *Verificable:* el adapter existe, no realiza llamadas de red en tests, y su `capability()` es válida.
- **P8 — Orden versionado.** El orden de materialización está registrado en `ordering_contract_version` y una cambio de ese contrato cambia `MI` y no `SCI`. *Verificable:* test existente `test_ordering_contract_change_invalidates_materialization_only` PASS con la nueva versión.

### Isolation, invalidación y seguridad

- **P9 — Aislamiento verificado.** Ninguna `ProviderCacheReference` cruza namespace; ningún contexto se reutiliza cross-project. *Verificable:* `test_imat011_cross_project_isolation` y `test_cross_project_no_contamination` PASS.
- **P10 — Domainios de invalidación separados.** Un miss/eviction/TTL del provider no altera la validez semántica; un cambio de `MI` no altera `SCI`. *Verificable:* I-MAT-002/003/005/006/007/012 cada uno con test PASS.
- **P11 — Sin secretos en segmentos reutilizables.** Ningún segmento persistido o materializado contiene credenciales, tokens, PII ni artefactos de sesiones previas. *Verificable:* la regla de omisión de `CONTEXT.md:2` es aplicada y registrada; no se introduce telemetría con contenido semántico (`METRICS.md:97-99`).

### Observabilidad

- **P12 — Eventos producidos.** `provider_cache_event` se escribe efectivamente en el `METRICS.md` de la sesión durante el dogfood. *Verificable:* el archivo contiene al menos un `provider_cache_event` con `result` y, cuando el provider lo reporte, `tokens_cached`.
- **P13 — Evidencia provider-reported.** Existe evidencia de clase `Observed` (provider-reported) de `tokens_cached > 0` para la segunda invocación comparable, corroborada por un segundo artefacto (clase `Verified`). *Verificable:* `EVIDENCE.md:112-118`; el reporte declara la clase.
- **P14 — Sin falsa economía.** No se reporta `hit rate` como valor económico; ninguna métrica mezcla dimensiones; ninguna atribución se cuenta dos veces. *Verificable:* I-ECO-001…006 con tests PASS; el reporte declara clase por métrica.

### Tests, dogfood y cierre

- **P15 — Dogfood completo.** Los nueve pasos de §18 se ejecutaron y sus resultados quedaron registrados, incluidos los casos de isolation, invalidación y fallback. *Verificable:* un artefacto de dogfood con los nueve pasos y su salida.
- **P16 — Verificación completa.** Batería canónica en verde (`docs/VERSIONING.md:4.1`), Validation Anchor registrado (alcance, command-set, inputs efectivos, Scoped Content Identity) y Git checkpoint consistente. *Verificable:* `check_lifecycle_anchor.py` y `check_lifecycle_checkpoint.py` reportan `VALID` para el plan.

### Separación de estados (no confundir)

```text
IMPLEMENTATION COMPLETE = P2 ∧ P3 ∧ P4 ∧ P5 ∧ P6 ∧ P7 ∧ P8
VERIFICATION COMPLETE  = P16
DOGFOOD COMPLETE       = P15 ∧ P12 ∧ P13
MVP CLOSED             = P1 ∧ … ∧ P16   (todos)
RELEASE AUTHORIZED     = MVP CLOSED ∧ autorización humana explícita
                         de release (autoridad RELEASE, ADR-16)

IMPLEMENTATION COMPLETE ⇏ DOGFOOD COMPLETE ⇏ MVP CLOSED ⇏ RELEASED
```

**Predicados que deliberadamente NO se incluyen** (serían ceremonia):
- un umbral de hit rate objetivo (prohibido: I-ECO-002, y no hay datos para calibrarlo);
- un objetivo de ahorro en USD (no hay pricing, por decisión);
- "el provider soporta prompt caching" (provider-owned, no verificable por ARgentOS);
- "el prefijo supera N tokens" (dependiente del provider elegido);
- "existe un store de materializaciones" (fuera de alcance por I-006).

---

## 24. Human Decisions

### HD-1 — ¿Qué contenido entra en la materialización dirigida al provider?

```text
Decision ID:      HD-1
Question:         ¿Debe la materialización canónica (la representación que el
                  Provider Adapter recibe) incluir el contenido estable que hoy
                  el Worker lee por separado —bootstrap, módulos de workflow,
                  roles, policies de gate, SKILL.md de skills activadas, KB
                  fresca— o esa porción pertenece al host/runtime y queda fuera
                  del alcance de ARgentOS?
Why it matters:   Es la decisión que determina si Prompt Cache puede existir.
                  Con el alcance actual (8 campos, 606 bytes, prefijo útil de
                  117 bytes), ningún provider puede reutilizar nada: la
                  integración de un adapter produciría misses sistemáticos.
                  Determina también si el MVP es "construir cache en ARgentOS"
                  o "declarar que la optimización pertenece al host" (no change).
Options:          A) Ampliar la materialización canónica para incluir el
                     contenido estable resuelto (el prefijo pasa a ser el
                     contenido, no el header).
                  B) Mantener el alcance actual y declarar que el caching de
                     re-lecturas pertenece al host (alternativa E, §19).
                  C) Ampliar solo la porción declarada estable-por-construcción
                     (bootstrap + workflow + rol + policy + skills), dejando la
                     KB fuera por su lifecycle de frescura.
Recommended:      C, con evidencia a favor y una condición. A favor: (i) el
                  modelo ya clasifica Core/Worker como Stable
                  (CONTEXT.md:266-278); (ii) el contenido es inmutable por
                  versión de payload (PROTOCOL_BOUNDARIES.md:144-153), lo que
                  hace el prefijo determinista sin mecanismo nuevo;
                  (iii) excluye la KB, cuyo lifecycle de frescura introduce
                  invalidación de lifecycle dentro de un prefijo y tensiona la
                  separación de dominios de §13. Condición: requiere resolver
                  el riesgo de Budget (§18.4) y no puede alterar los límites
                  semánticos del Budget (I-010).
Evidence:         runtime/toolcalls/context.py:47-63 (8 campos);
                  runtime/toolcalls/prompt_rendering.py:37-44 (skills por
                  nombre); WORKER_DELEGATION_CONTRACT.md:92,114,116 (lecturas
                  posteriores); CONTEXT.md:266-278 (segmentos);
                  PROTOCOL_BOUNDARIES.md:144-153 (inmutabilidad);
                  BUDGET_MATERIALIZATION.md:64-82 (I-010);
                  docs/rfc/72-…md:129 (honestidad: el contrato canónico "no
                  existe hoy"; hoy sí existe la implementación pero no el
                  contenido).
Consequence:      A/C: el payload crece; requiere re-evaluar el Budget y
                  re-versionar ordering/serialization. B: Prompt Cache como
                  feature del Protocol se cierra como "no change", y el
                  ahorro queda fuera de la telemetría de ARgentOS.
Blocking:         SÍ — bloquea la materialización de Phase 2.
```

### HD-2 — ¿El orden de materialización pasa a ser normativo en el Protocol?

```text
Decision ID:      HD-2
Question:         ¿Se mantiene el orden de materialización como concern
                  exclusivo del runtime (Open/DEFERRED, como hoy), o se
                  declara normativamente que la porción estable precede a la
                  dinámica?
Why it matters:   El orden actual pone cuatro campos volátiles primero
                  (canonical.py:56-68) y hace que el prefijo cacheable sea de
                  117 bytes. Un orden estable-primero es condición necesaria
                  de cualquier hit. La pregunta es de gobernanza: si el orden
                  queda en el runtime, cada runtime puede cachear distinto y
                  el Protocol no puede prometer portabilidad de cache; si pasa
                  al Protocol, se toca protocol/.agents/ y se requiere bump.
Options:          A) Mantener OPEN/DEFERRED; el runtime decide (orden
                     estable-primero como elección del runtime, versionada en
                     ordering_contract_version).
                  B) Declarar normativamente en el Protocol el principio
                     "estable antes que dinámico" sin fijar el orden exacto.
                  C) Fijar el orden exacto en el Protocol.
Recommended:      A, por mínima complejidad y por coherencia con la frontera
                  ya modelada (docs/rfc/13-…md:145-152): el orden de bytes es
                  representación, y la representación es del runtime. A es
                  suficiente porque el contrato ya es versionado y verificable
                  (ordering_contract_version + I-MAT-001 + tests). B/C
                  añadirían normativa sin cambiar el resultado observable,
                  salvo que se requiera portabilidad de cache entre runtimes
                  — necesidad no demostrada en el repo.
                  Si se elige A, la elección del runtime DEBE registrarse y
                  justificarse (ya ocurre: runtime/README.md:66-72 declara el
                  Current Ordering Choice).
Evidence:         canonical.py:44-68 (orden v1); docs/rfc/72-…md:131-138
                  (OPEN/DEFERRED); docs/rfc/72-…md:135-136 (Ordering Contract
                  vs Current Ordering Choice); identity.py:255-277
                  (ordering_contract_version como componente de MI);
                  tests/test_canonical_materialization.py:373-384, :610-624.
Consequence:      A: el cambio es runtime-only, sin bump de VERSION, sin
                  changelog de protocolo, y la gobernanza de RFC-72 absorbe la
                  decisión como Amendment Log si se cambia el contrato.
                  B/C: cambio de payload → bump MINOR + changelog + ancla del
                  runtime + batería.
Blocking:         SÍ — bloquea la materialización de Phase 2 (no se puede
                  reordenar sin decidir dónde vive la decisión).
```

### HD-3 — ¿El identificador de sesión debe participar del contenido semántico?

```text
Decision ID:      HD-3
Question:         ¿`session_uuid` debe seguir siendo parte del contenido del
                  segmento worker (y por lo tanto de SegmentContentIdentity y
                  SemanticContextIdentity), o debe excluirse del contenido
                  semántico y permanecer solo como metadata de ejecución?
Why it matters:   Con session_uuid dentro del contenido, dos sesiones nunca
                  comparten SCI: el reuso cross-session es imposible incluso
                  con contexto idéntico. Es una sobre-invalidación maximalista
                  (isolation-first, correcta frente a false hits) que también
                  anula el beneficio. Afecta directamente el tamaño del prefijo
                  reutilizable entre sesiones.
Options:          A) Mantener el comportamiento actual (isolation-first
                     máximo); aceptar reuso intra-sesión únicamente.
                  B) Excluir session_uuid del contenido semántico; conservarlo
                     como campo de la representación pero fuera de la
                     identidad.
Recommended:      A para el MVP, y registrar B como mejora diferida evaluable
                  con telemetría. Fundamento: (i) isolation-first es la
                  política inicial declarada (docs/rfc/71-…md:271-280);
                  (ii) false hit unacceptable / false miss acceptable;
                  (iii) el beneficio de B es real pero requiere medición para
                     justificarse, y RFC-68 gatea la Fase 2 de cache a
                     telemetría. Si el dogfood (§18) demuestra que el reuso
                     intra-sesión ya produce ahorro medible, B puede diferirse
                     indefinidamente sin costo.
Evidence:         identity.py:216-227 (session_uuid en el content del
                  segmento); tests/test_canonical_materialization.py:239-247
                  (el test exige que session_uuid afecte el SCI);
                  docs/rfc/71-…md:271-280 (isolation-first);
                  docs/rfc/68-…md:687-699 (gate a telemetría);
                  medición propia: prefijo común de 117/606 bytes.
Consequence:      A: reuso limitado a la misma sesión (y dentro de ella, a las
                  invocaciones cuyo state/phase/role/task no cambien antes del
                  prefijo). B: habilitaría reuso cross-sesión del prefijo
                  estable, con el riesgo de reutilizar contexto de una sesión
                  en otra (mitigable por namespace de proyecto).
Blocking:         SÍ — determina el valor máximo del MVP.
```

### HD-4 — ¿El MVP incluye el writer de telemetría?

```text
Decision ID:      HD-4
Question:         ¿El MVP de Prompt Cache incluye el productor que escribe
                  `provider_cache_event`/`reuse_event` en el METRICS.md de la
                  sesión, o el MVP se cierra sin evidencia end-to-end?
Why it matters:   Sin writer no hay evidencia admisible de ahorro, y el dogfood
                  no puede satisfacer P12/P13 del closure predicate. Pero el
                  contrato asigna la escritura al Orchestrator/host, no al
                  runtime, y el plan 91 declaró ese seam como límite
                  arquitectónico, no como gap.
Options:          A) Incluir el writer en el MVP (responsabilidad
                     Orchestrator/host, documentada en el contrato).
                  B) Diferir el writer; cerrar el MVP como "capacidad
                     implementada, ahorro no demostrado".
Recommended:      A. Fundamento: RFC-68 gatea la Fase 2 de cache a telemetría
                  (docs/rfc/68-…md:698-699); sin evidencia provider-reported el
                  resultado máximo admisible es una attestation, y el
                  closure predicate P13 quedaría insatisfacible. B convertiría
                  el MVP en algo indistinguible de "no change".
Evidence:         METRICS.md:67-68 (contrato); PROTOCOL_METRICS.md:85-110
                  (catálogo); plan 91 "NOT IMPLEMENTED" (writer);
                  búsqueda completa: cero ocurrencias de provider_cache_event
                  en runtime/; EVIDENCE.md:112-118 (clases);
                  docs/rfc/68-…md:698-699 (gate).
Consequence:      A: agrega alcance al MVP (una responsabilidad del
                  Orchestrator, no una entidad nueva). B: MVP cerrable pero
                  sin demostración de valor.
Blocking:         NO bloqueante para empezar; SÍ bloqueante para cerrar el MVP
                  con P13.
```

### HD-5 — ¿Qué provider concreto se integra primero?

```text
Decision ID:      HD-5
Question:         ¿Cuál es el primer provider real cuya capacidad de prompt
                  caching se integra, y con qué mecanismo (implícito o
                  explícito / breakpoints)?
Why it matters:   Todas las incógnitas del provider boundary (§10.3) solo se
                  resuelven contra documentación de un provider concreto: si el
                  prefijo mínimo es alcanzable, si reporta tokens cacheados, si
                  el cache es model-scoped, si expone referencia. Elegir
                  determina qué parte del contrato abstracto queda ejercitada.
Options:          No se enumeran (dependen del entorno de adopción objetivo y
                  de documentación externa al repositorio).
Recommended:      No se recomienda un provider: el repositorio no contiene
                  evidencia para elegir y la decisión depende de factores
                  externos (disponibilidad, contrato comercial, modelos).
                  Criterio recomendado: preferir el provider cuyo reporte de
                  tokens cacheados sea más explícito y cuyo mecanismo sea
                  implícito (menos estado que administrar en el adapter).
Evidence:         docs/rfc/72-…md:160-175 (contrato abstracto);
                  runtime/toolcalls/provider_cache.py (solo NullProviderAdapter);
                  búsqueda: cero ocurrencias de anthropic/openai/bedrock/vertex.
Consequence:      Determina las dimensiones condicionales de
                  MaterializationIdentity (provider/model/model_version) y el
                  contenido de la propuesta de adapter.
Blocking:         SÍ para implementar P7; NO para las demás decisiones.
```

### HD-6 — ¿Se acepta el crecimiento del prompt obligatorio?

```text
Decision ID:      HD-6
Question:         Si HD-1 = A/C, el payload dirigido al provider crece
                  sustancialmente. ¿Se acepta que el prefijo estable se envíe en
                  cada invocación (pagando su costo de escritura de cache) bajo
                  el principio "el caching no altera los límites semánticos del
                  Budget"?
Why it matters:   I-010 prohíbe que el caching modifique silenciosamente los
                  límites del Context Budget (BUDGET_MATERIALIZATION.md:64-82).
                  Incluir el contenido estable en la materialización no viola
                  I-010 (el Budget limita la composición semántica; la
                  materialización es otra magnitud), pero sí aumenta el costo
                  físico por invocación. Sin medición, no se puede saber si el
                  net benefit es positivo.
Options:          A) Aceptar y medir con telemetría antes de decidir la
                     política de admisión.
                  B) No incluir el contenido estable (equivale a HD-1=B).
Recommended:      A, condicionado a que el dogfood mida el net benefit por
                  dimensión (tokens, latencia) sin sumar unidades
                  (I-ECO-004/005).
Evidence:         BUDGET_MATERIALIZATION.md:64-82 (tres magnitudes distintas);
                  docs/rfc/74-…md:86-109 (modelo de costo, Net Benefit
                  dimension-specific); docs/rfc/74-…md:159-163 (semantic
                  validity precede economic evaluation).
Consequence:      Aceptación con medición obligatoria; no se fija umbral.
Blocking:         SÍ, dependiente de HD-1.
```

---

## 25. Phase 2 Materialization Impact

Ninguno de estos cambios se realizó. Se listan como impactos probables, con su justificación.

| Categoría | Artefacto probable | Cambio | ¿Por qué es necesario? |
|---|---|---|---|
| **Documentation** | `docs/rfc/72-…md` (`## Amendment Log`) | Registrar HD-1/HD-2/HD-3 y la extensión del contrato de materialización canónica | La RFC es la fuente de verdad de `MaterializationIdentity`, Canonical Materialization y Stable Prefix; su §3 declara que el contrato "no existe hoy" |
| **Documentation** | `docs/working/research/` | Este informe como provenance de Phase 1 | Reconstruction inputs |
| **Governance** | `docs/plans/NN-…md` (nuevo plan) | Plan de implementación con Validation Anchor | RFC-56 Clase A/B |
| **Governance** | `docs/plans/INDEX.md`, `CHANGELOG.md`, `docs/MIGRATION.md` | Registro del plan y notas de migración si cambia el payload | Ciclo de cierre |
| **Contract** | `protocol/.agents/contracts/METRICS.md` | Solo si HD-4 requiere ajustar campos de `provider_cache_event` | El contrato ya tiene los campos necesarios; probablemente **sin cambio** |
| **Context (normativa)** | `protocol/.agents/standards/context/CONTEXT.md` | Solo si HD-1/HD-2 deciden normar el contenido o el orden de materialización | Hoy el orden es OPEN/DEFERRED |
| **Runtime** | `runtime/toolcalls/context.py` | Completar los campos faltantes (o corregir la afirmación del módulo) | §8.4: implementación diverge del payload que declara mapear |
| **Runtime** | `runtime/toolcalls/canonical.py` | Extender la materialización con la porción estable; posiblemente bump de `ordering_contract_version` y `serialization_version`; nueva `OrderingContract` | §9.4: es la pieza ausente |
| **Runtime** | `runtime/toolcalls/prompt_rendering.py` / `toolcalls_rendering.py` | Incluir contenido estable si HD-1 = A/C | Los renderers son los serializadores de variante |
| **Runtime** | `runtime/toolcalls/provider_cache.py` | Nuevo adapter concreto (nuevo módulo o implementación) | §10.3: solo existe `NullProviderAdapter` |
| **Runtime** | `runtime/toolcalls/cache_coordinator.py` | Posible ajuste si HD-4 asigna la emisión de eventos al runtime | Hoy solo expone metadata |
| **Runtime** | `runtime/README.md` | Documentar el contrato extendido y el adapter | `runtime/README.md:50-118` es la fuente descriptiva del contrato |
| **Provider integration** | Nuevo módulo de adapter | Traducción a la API del provider elegido (HD-5) | Frontera de RFC-72 §7 |
| **Identity** | `runtime/toolcalls/identity.py` | Solo si HD-3 = B (excluir `session_uuid` del contenido) — y sería un cambio semántico que requiere enmienda de RFC-71/72 | Riesgo alto; probablemente diferido |
| **Harness** | *Ninguno* | No hay gate que tocar. El enforcement de la batería ya cubre el determinismo | Evitar governance innecesaria |
| **Tests** | `tests/test_canonical_materialization.py` | Nuevos tests: prefijo real > umbral; cobertura de identidad por campo del payload; adapter concreto | P4/P5/P6 del closure predicate |
| **Tests** | `tests/test_toolcalls.py` | Regresión de las dos materializaciones | — |
| **Tests** | Nuevo `tests/test_<provider>_adapter.py` | Comportamiento del adapter sin red (contrato de capacidad, traducción, fallback) | P7 |
| **Telemetry** | Productor de `reuse_event`/`provider_cache_event` | Escribir en `.project/<uuid>/METRICS.md` | §14.3, P12/P13 |
| **Telemetry** | `tools/aggregate_metrics.py` | Solo si cambian las formas de evento | Hoy ya agrega ambos tipos |
| **Artifacts** | `protocol/.agents/VERSION` | Bump MINOR **solo si** HD-1/HD-2 tocan `protocol/.agents/` | `docs/VERSIONING.md:3` |
| **Artifacts** | `runtime/toolcalls/canonical.py::PROTOCOL_VERSION` | Sincronizar con VERSION si hay bump | `tools/check_version_state.py:97-101` falla si no |
| **Skill** | *Ninguna* | No hay skill que tocar | Evitar scope creep |
| **Orchestrator** | `orchestrator.md` o contrato de METRICS | Solo la obligación de escribir los eventos (HD-4) | El contrato asigna la escritura al Orchestrator |
| **Worker** | *Ninguno* | El Worker no cambia | La frontera lo mantiene agnóstico |

**Cambios que NO se proponen** (evitar governance y complejidad sin evidencia): nuevos standards; nuevos contratos de state machine; nuevas skills; nuevas entidades de identidad; nuevos gates de harness; nuevos flags en `features.toml`; changes al Discovery subsystem; changes al Change Lifecycle.

---

## 26. Autonomy Relevance

Evaluación breve. No es un diseño de autonomía.

**Mecanismos que serían infraestructura útil para autonomía futura:**

1. **`SemanticContextIdentity` + `SegmentIdentity`** — permiten a un agente decidir si dos contextos son el mismo **sin** leer el contenido. Es la primitiva necesaria para cualquier reutilización de razonamiento o de decisiones.
2. **`MaterializationIdentity` + I-MAT-001 (determinismo byte-verificable)** — permite afirmar "esta representación es reproducible" sin confiar en el reporter. Es la base de cualquier caché verificable y de cualquier replay auditable.
3. **Tres dominios de invalidación no conflables** — es la distinción que impide que una degradación de performance se interprete como pérdida de validez. Necesaria para que un agente autónomo pueda degradar gracefulmente.
4. **Frontera del Provider Adapter con capacidad abstracta** — permite que un agente opere sobre capacidades declaradas en vez de sobre detalles de implementación. Es el patrón que la autonomía necesita para no acoplarse a un proveedor.
5. **Contrato de evidencia por clase + verifiability classes** (`EVIDENCE.md`, `PROTOCOL_METRICS.md`) — es la infraestructura que permite que un agente autónomo **sepa qué sabe** y distinga `Observed` de `Estimated`, `Derived` y `Unavailable`.
6. **`ProjectIdentity` + aislamiento por namespace + store derivado rebuildable** (RFC-73, `project_store.py`) — la base de memoria durable aislada.
7. **Separación `SemanticContextIdentity` (correctness) / estado del provider (performance)** — el principio que impide que una señal de performance se convierta en señal de correctness. Crítico para autonomía.
8. **Change Governance Artifact con identidad derivada por `SegmentIdentity`** — ya demuestra que las primitivas de RFC-71 son reutilizables fuera del contexto de prompt cache (precedente real, no hipótesis).

**Mecanismos estrictamente específicos de cache (no infraestructura general):**

1. `ProviderCacheReference` — opaca, sin uso fuera del flujo de cache.
2. `CacheLookup` / `HIT` / `MISS` / `UNAVAILABLE` — vocabulario de cache.
3. `admission_policy` — decisión binaria de intentar cache.
4. `stable_prefix()` — cómputo del prefijo común.
5. Los eventos `reuse_event` con `layer=materialization` y `provider_cache_event`.
6. `OrderingContract` — específico de la representación (aunque el versionado sí es general).
7. Catálogo `Reuse and cache` y I-ECO — específicos de economía de cache.

**Respuesta a la pregunta:** el saldo es favorable. De los mecanismos construidos para Prompt Cache, **ocho son infraestructura general reutilizable** y **siete son específicos**. La serie RFC-71→74, aunque se originó en un objetivo de cache, produjo primitivas de identidad, determinismo, evidencia y aislamiento que sirven a la autonomía con independencia de que Prompt Cache llegue a producir un hit real.

---

## 27. Consistency / Drift Findings

Ninguna se corrigió.

### 27.1 BLOCKING

**B-1 — La materialización canónica no cubre el contexto entregado (IMPLEMENTATION DRIFT).**
`runtime/toolcalls/context.py:6-9` afirma: "It introduces no new concepts: every field corresponds to a field of the invocation payload defined in `WORKER_DELEGATION_CONTRACT.md`". Es inexacto: el payload tiene `profile`, `input_artifacts`, `harness_policy`, `communication_style` y `technical_approach` (`WORKER_DELEGATION_CONTRACT.md:29,30,34,48,52`) que **no** están en `ExecutionContext` (`context.py:56-63`). Consecuencia: dos payloads que difieren solo en `input_artifacts` producen la misma `SemanticContextIdentity`, el mismo `MaterializationIdentity` y el mismo payload canónico. Ver §8.4.

**B-2 — `docs/rfc/72-…md:129` declara que el contrato de materialización canónica "no existe hoy", mientras la implementación ya existe.**
La RFC dice: "**Honestidad sobre el estado actual (FACT):** el repo no tiene hoy un contrato de materialización canónica: el runtime de referencia implementa dos materializaciones coexistentes y declara que la elección pertenece al runtime". Pero el plan 89 lo implementó (`canonical.py`, `tests/test_canonical_materialization.py`, `runtime/README.md:50-89`) y la RFC nunca se enmendó para reflejarlo. **NORMATIVE DRIFT**: la RFC subestima el estado del repositorio.

**B-3 — Contradicción mutua de orden de ejecución entre planes.**
Los planes 92 y 93 afirman que los planes 90 y 91 **no** se ejecutaron ("NO se ejecuta el plan 90: permanece `Aprobado para ejecución`"; "Plan 91 NO ejecutado"). Los planes 90 y 91 afirman que **sí** se ejecutaron el 2026-08-31, con su gate cumplido **por** esos mismos planes de aceptación. El estado real del repo (git: `bf63b21` plan 90, `9dd8703` plan 91; `docs/plans/INDEX.md:151-152` ambos `Executed`) confirma a 90/91. **NORMATIVE DRIFT** en 92/93.

### 27.2 NON-BLOCKING

- **NB-1 — Ningún plan de la serie declara `Closed`.** `docs/plans/INDEX.md:128-129,150-152,165-166` los registra `Executed`. Con RFC-75 Incrementos 1+3 operativos (plan 96), la condición derivada `Closed` sería exigible. No es invalidez (los planes son anteriores o paralelos), pero es una condición derivada no registrada.
- **NB-2 — `RFC-74` y el plan 91 declaran `METRICS.md` schema `1.2.0`; el contrato está en `2.0.0`.** `docs/rfc/74-…md:559,595`; `docs/plans/91-…md` (§U1); vs `protocol/.agents/contracts/METRICS.md:2,8` = `2.0.0` (bump del plan 78, versión 11.0.0). El bump posterior es correcto y trazable; las citas de la serie 91/74 quedaron obsoletas. **DESCRIPTIVE DRIFT.**
- **NB-3 — La fila del plan 91 en `docs/plans/INDEX.md:152` registra "pytest 316 passed"; la `Nota de ejecución` del plan 91 registra 331 passed.** **TEST/HARNESS DRIFT.**
- **NB-4 — Los totales de pytest varían sin explicación consistente entre planes de la misma serie:** 240 (86), 243 (87), 53 (88), 279 (89), 316 (90), 331 (91), 279 (92), 316 (93). El plan 88 atribuye su total a errores ambientales del sandbox; los demás mencionan workarounds de basetemp. **TEST/HARNESS DRIFT** (los números no son comparables entre sí).
- **NB-5 — Cabeceras de planes con gate obsoleto.** El plan 90 declara en su cabecera que RFC-73 es `Proposal` y el plan 92 "pendiente de ejecución"; el plan 93 declara plan 87 `Executed` y en la misma frase "(hoy `Aprobado para ejecución` sin ejecutar)". **DESCRIPTIVE DRIFT.**
- **NB-6 — Fechas internas inconsistentes.** Plan 87: cabecera 2026-08-29 vs nota 2026-08-31. Plan 93: entregable 2026-08-30 vs `Accepted (plan 93, 2026-08-31)`. **DESCRIPTIVE DRIFT.**
- **NB-7 — Los ocho planes mantienen sus `Criterios de salida` con checkboxes `- [ ]` pese a `Executed`.** La completitud se evidencia solo en las notas de ejecución y el INDEX. **DESCRIPTIVE DRIFT.**
- **NB-8 — `PROTOCOL_METRICS.md:98-101` mantiene anotaciones de disponibilidad que referencian productores ya "ejecutados"** ("NOT AVAILABLE until a real adapter", "PARCIAL (until producers)"). Es correcto respecto del estado real (no hay adapter ni productores), pero el plan 91 describía el catálogo como "consumido sin duplicarlos". **DESCRIPTIVE DRIFT** menor.
- **NB-9 — `tools/check_architecture_traceability.py` y los checkers `check_lifecycle_*` existen y se usan en las Validation Anchors de los planes, pero no aparecen en la batería canónica de `docs/VERSIONING.md:4.1`.** No es contradicción (la batería es una lista mínima), pero conviene saberlo al planificar verificaciones. **DESCRIPTIVE DRIFT.**

### 27.3 Contradicciones preservadas explícitamente (no resueltas)

- **C-1 — `docs/rfc/72-…md:138` mantiene el orden normativo como OPEN/DEFERRED, mientras `runtime/README.md:66-72` declara un `Ordering Contract v1`.** Ambas afirmaciones coexisten correctamente en el modelo (Ordering Contract vs Current Ordering Choice), pero el repo no declara explícitamente que la tensión está resuelta. Ver HD-2.
- **C-2 — `COMPOSITION_OPTIMIZATION.md:15` ordena "in the priority order of `CONTEXT.md` §1", mientras `canonical.py:56-68` implementa un orden distinto.** Ambas pueden ser correctas (prioridad de inclusión ≠ orden de bytes), pero el repo no lo declara. Ver §7.3.
- **C-3 — `docs/rfc/71-…md:227` afirma que `reuse >= 3` "no es normativo y queda diferido a RFC-B/economía", y `docs/rfc/72-…md:237` lo repite; `cache_coordinator.py:60-72` lo implementa correctamente (sin umbral).** Esta cadena es **consistente**; se registra para dejar constancia de que fue verificada y no es un drift.
- **C-4 — `docs/rfc/73-…md:288` afirma que "la persistence semántica de RFC-71 (project segment + store) es un requisito de implementación futura", mientras el store ya existe** (`runtime/toolcalls/project_store.py`; `PROTOCOL_BOUNDARIES.md:121-127`). La RFC fue enmendada al aceptarse (plan 92) y su Amendment Log registra la implementación por plan 90, pero el cuerpo mantiene el texto de "requisito futuro". **DESCRIPTIVE DRIFT** interna a la RFC.

---

## 28. Reconstruction Inputs

Un agente que no participó de esta investigación necesita lo siguiente para reconstruirla.

### 28.1 Por qué Prompt Cache existe

- RFC-68 §G "Cache vs Source of Truth" — `docs/rfc/68-architecture-evolution-workflow.md:687-699`: "No hay cache en Fase 1; cachear re-lectura es Fase 2, gated a telemetría (AEW-015)".
- Investigación de costo — `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:761-769` (Final Assessment): no había evidencia suficiente para una RFC de reuse; la instrumentación P0 era el requisito previo.
- Auditoría de reutilización — `docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md`: inventario de artifacts, dependencias, cacheability, independencia de verificación, telemetría faltante.
- Intención de la feature (enunciado de esta fase): aprovechar el sistema de governance y composición de contexto para producir porciones estables del prompt y reducir tokens, costo y latencia cuando el provider lo permita.

### 28.2 Qué problema resuelve

Reducir el procesamiento repetido del contexto estable entre invocaciones al LLM, cuando el provider lo soporta, sin degradar correctness, aislamiento, frescura ni calidad. La pregunta operativa: cómo producir, identificar, ordenar, materializar y reutilizar de forma segura el contexto estable.

### 28.3 Qué arquitectura utiliza

Flujo: `Context Sources → Context Composition → Context Classification → {Stable | Dynamic}` (RFC-71) y `SemanticContextIdentity + MaterializationIdentity → Canonical Materialization → Stable Prefix → Provider Prompt Cache Capability → ProviderCacheReference` (RFC-72).

Documentos normativos mínimos: `docs/rfc/71-…md`, `docs/rfc/72-…md`, `docs/rfc/73-…md`, `docs/rfc/74-…md`; `protocol/.agents/standards/context/CONTEXT.md:230-352`; `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:107-127`; `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:64-82`; `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:47-62`; `protocol/.agents/contracts/METRICS.md:51-104`; `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:85-168`.

Código: `runtime/toolcalls/identity.py`, `canonical.py`, `provider_cache.py`, `cache_coordinator.py`, `project_segment.py`, `project_store.py`, `context.py`, `prompt_rendering.py`, `toolcalls_rendering.py`, `budget.py`.

Tests: `tests/test_canonical_materialization.py` (I-MAT-001…012, stable prefix, ordering, adapter), `tests/test_project_segment.py` (identidad, aislamiento, frescura, atomicidad), `tests/test_aggregate_metrics.py` (eventos de reuse/cache), `tests/test_toolcalls.py` (dos materializaciones).

### 28.4 Qué queda fuera

Ver §22 (OUT OF SCOPE y NON-GOALS) y §20 (Rejected / Deferred).

### 28.5 Qué decisiones ya están tomadas (no reabrir)

1. `ProviderCacheReference` es opaca y no es autoridad de correctness (I-007/I-MAT-004).
2. Un cache miss del provider nunca es invalidación semántica (I-MAT-005/006).
3. `SemanticContextIdentity` es invariante a materialización (I-005).
4. Persistence y Materialization son independientes (I-006).
5. El caching no modifica los límites semánticos del Context Budget (I-009/I-010/I-MAT-010).
6. Isolation-first: sin reuso cross-project sin autorización explícita (I-008).
7. TTL nunca es mecanismo de correctness (I-009).
8. Sin umbrales: `reuse >= 3` está rechazado en las cuatro RFCs.
9. Sin pricing, sin billing, sin `CostModel`.
10. La admisión es policy sin umbral; la equivalencia de cache la determina el provider.
11. El Protocol no implementa provider prompt cache (frontera declarada).
12. Sin state machine, sin identity primitive ni registry nuevos.
13. El orden concreto de materialización está OPEN/DEFERRED a nivel Protocol y declarado a nivel runtime.
14. `PROTOCOL_VERSION` del runtime debe igualar `protocol/.agents/VERSION` (enforced).

### 28.6 Qué decisiones siguen abiertas

HD-1 (contenido de la materialización), HD-2 (dónde vive la decisión de orden), HD-3 (participación de `session_uuid`), HD-4 (writer de telemetría en el MVP), HD-5 (provider inicial), HD-6 (aceptación del crecimiento del prompt). Ver §24.

### 28.7 Qué debe materializarse en Phase 2

En orden de dependencia:

1. **Resolver HD-1…HD-6** (autoridad humana) y registrar las decisiones.
2. **Registrar la decisión como enmienda de RFC-72** (o el artefacto de gobernanza que corresponda según la clase RFC-56).
3. **Materializar el prefijo estable** en la representación dirigida al provider, con `OrderingContract` y versiones actualizadas si corresponde (HD-1/HD-2).
4. **Completar o corregir el mapeo `ExecutionContext` ↔ Delegation Payload** (B-1).
5. **Implementar un adapter real** del provider elegido (HD-5).
6. **Implementar/decidir el writer de telemetría** (HD-4).
7. **Ampliar los tests**: prefijo real, cobertura de identidad por campo, adapter concreto sin red.
8. **Ejecutar el dogfood de §18** y registrar los nueve pasos.
9. **Verificar** con la batería canónica, Validation Anchor y checkpoint.
10. **Cerrar** conforme al closure predicate de §23 — o registrar `NO CHANGE` si HD-1 se resuelve como B.

---

## 29. Final Recommendation

**Recomendación arquitectónica:** el MVP de Prompt Cache en ARgentOS Protocol debe ser **completar la materialización canónica con el prefijo estable y conectar un único provider real detrás de la frontera de adapter ya existente**, reutilizando íntegramente las identidades, el contrato de determinismo, la separación de dominios de invalidación y el contrato de observabilidad construidos por la serie RFC-71…74. **No se necesita ninguna entidad, state machine, lifecycle, registry ni identity primitive nueva.**

**Fundamento (evidencia, no preferencia):**

1. La infraestructura está construida y verificada: identidades deterministas, materialización canónica byte-verificable (I-MAT-001), frontera de adapter con capacidad abstracta, referencia opaca, coordinador de admisión sin umbrales, tres dominios de invalidación, contrato de telemetría por capa. Todo con tests.
2. La pieza ausente es **una sola**: el contenido estable no está dentro de la representación que llega al provider. Medido: 606 bytes de payload, 117 bytes de prefijo común entre invocaciones que difieren solo en `session_uuid`.
3. Por eso la conclusión correcta **no** es "falta una pieza arquitectónica grande" sino "falta decidir un alcance". Es el caso en el que el MVP es pequeño: una decisión (HD-1), un reordenamiento (HD-2), un adapter (HD-5) y un writer de telemetría (HD-4).
4. La única incógnita que el repositorio **no puede resolver** es el comportamiento real del provider. Correctamente marcada como UNKNOWN; no debe rellenarse con supuestos.
5. La alternativa honesta —que la optimización pertenezca al host, no a ARgentOS (alternativa E)— debe considerarse seriamente. Si HD-1 se resuelve como B, el resultado correcto es **`NO CHANGE`**, y el repo tiene doctrina explícita que lo respalda: "Possible answers to a discovered problem include… or **no change** — which remains a valid and respected outcome" (`AGENTS.md:Decision-Making Compass`).

**Condición de secuenciación, fundada en evidencia:** la telemetría debe existir antes o al mismo tiempo que el adapter. RFC-68 gatea la Fase 2 de cache a telemetría, la telemetría sigue sin productor, y sin ella el dogfood no puede producir evidencia de clase `Observed` de ahorro. Sin esa evidencia, el máximo resultado admisible es "capacidad implementada, ahorro no demostrado" — y eso no satisface el closure predicate propuesto.

**Advertencia final, explícita:** la conclusión puede ser que el MVP sea pequeño. También puede ser que la respuesta correcta sea no construir cache en ARgentOS. Ambas son compatibles con la evidencia recogida; la que no es compatible es construir un adapter real contra el prefijo actual y declarar éxito.

---

## 30. Terminal Status

```text
PHASE_1_READY_FOR_HUMAN_DECISIONS
```

**Justificación:** la arquitectura está suficientemente determinada para materializar —todas las primitivas existen, están verificadas y sus fronteras están modeladas—, pero quedan decisiones que **requieren autoridad humana** y que ninguna evidencia del repositorio resuelve por sí sola:

- **HD-1** (qué contenido entra en la materialización dirigida al provider) — bloqueante.
- **HD-2** (dónde vive la decisión de orden de materialización) — bloqueante.
- **HD-3** (participación de `session_uuid` en la identidad semántica) — bloqueante para el valor máximo del MVP.
- **HD-5** (provider inicial) — bloqueante para la implementación del adapter.
- **HD-6** (aceptación del crecimiento del prompt obligatorio) — bloqueante, dependiente de HD-1.
- **HD-4** (writer de telemetría en el MVP) — no bloqueante para empezar, bloqueante para cerrar.

**No se usa `PHASE_1_BLOCKED`:** no falta información esencial que el repositorio pudiera contener. La única incógnita (comportamiento real del provider) es intrínsecamente externa y correctamente clasificada como UNKNOWN.

---

*Informe producido en modo READ-ONLY. Ningún archivo del repositorio fue modificado, creado ni eliminado, salvo este informe en `docs/working/research/`. No se crearon RFCs, ADRs ni planes. No se hicieron commits. No se modificó `VERSION`.*
