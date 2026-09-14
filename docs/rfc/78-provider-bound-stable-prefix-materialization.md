# RFC-78 — Materialización provider-bound del stable prefix Core + Worker

**Status:** Accepted (plan 121, 2026-09-14; autorización humana del mantenedor)
**Fecha:** 2026-09-14
**Serie:** Context Persistence & Prompt Cache (continuación de RFC-71…74)
**Change Level:** L3
**Origen:** `docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md` (Phase 1, terminada `PHASE_1_READY_FOR_HUMAN_DECISIONS`) y las decisiones humanas HD-1b, HD-2b, HD-3, HD-4, HD-5, HD-6 y HD-7 emitidas por el mantenedor (2026-09-14), más las preguntas de acotación HD-1b/bootstrap y HD-7/HD-3 resueltas por el mantenedor en la misma fecha (Worker-scope; completitud de F-1 autorizada, restricción HD-3 limitada a `session_uuid`).
**Pregunta:** ¿Cómo debe ARgentOS Protocol producir una representación provider-bound determinística cuyo prefijo inicial contenga el contexto estable reusable Core + Worker, manteniendo separados el significado semántico, la materialización y la autoridad del provider sobre su propio cache?
**Afectados:** si se acepta y se implementa, `protocol/.agents/standards/context/CONTEXT.md` (semántica del prefijo estable y su frontera con la compresión) y, condicionalmente, `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md`. `runtime/`, `tests/` y `docs/` por la vía del Plan.

> **Convención de evidencia:** toda afirmación sobre el estado actual del repo se
> cita con `ruta:sección`. Las decisiones se marcan como **Decisión**; los
> conceptos que la arquitectura exige pero que no existen hoy se marcan como
> **Requisito de implementación futura**; lo que el repositorio no permite
> determinar se marca **UNKNOWN**.

> **Autorización.** Esta RFC queda `Accepted` por **autorización humana explícita
> del mantenedor (2026-09-14)**, que confirmó las decisiones humanas HD-1b,
> HD-1b/bootstrap, HD-2b, HD-3, HD-4, HD-5, HD-6, HD-7 y HD-7/HD-3 y autorizó su
> aceptación siguiendo el Change Lifecycle, sin introducir decisiones nuevas.
> La aceptación habilita la modificación de `protocol/.agents/` por la vía
> Clase A de RFC-56 y se ejecuta mediante el Plan 121
> (`docs/plans/121-provider-bound-stable-prefix-readiness-mvp.md`). La aceptación
> **no** constituye autorización de release, tag, promoción a `master` ni
> publicación.

---

## Problema

1. **La materialización canónica existe y es correcta, pero su prefijo útil es prácticamente nulo.** El runtime de referencia implementa una Canonical Materialization determinista y byte-verificable (`runtime/toolcalls/canonical.py`; `runtime/README.md:Canonical materialization contract (RFC-72)`), y `docs/rfc/72-…md:3` declara el invariante I-MAT-001. Sin embargo, la representación que un Provider Adapter recibe se construye sobre un `ExecutionContext` de ocho campos (`runtime/toolcalls/context.py`), y esa representación **no contiene el contenido estable** que domina el prompt real.

2. **Medición del estado actual (FACT).** En el caso representativo de Phase 1 la materialización canónica mide **606 bytes**, y la porción común entre dos invocaciones que difieren únicamente en `session_uuid` es de **117 bytes**, correspondientes a estructura/labels JSON y al comienzo del hash de `SemanticContextIdentity`. El orden de facto del runtime (`runtime/toolcalls/canonical.py`) coloca cuatro campos volátiles —`session`, `state`, `phase`, `role`— antes que todo lo demás.

3. **El contenido estable llega por lecturas posteriores, fuera del artefacto dirigido al provider.** El contrato del producto ordena al Worker leer el módulo de workflow, el perfil, las skills y los input artifacts durante la ejecución (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Worker Execution`), y los `SKILL.md` completos (campo `skills` del mismo contrato). Ese contenido **no** participa de la materialización canónica: en la variante prompt los renderers emiten únicamente los **nombres** de las skills (`runtime/toolcalls/prompt_rendering.py`).

4. **Drift de completitud entre Delegation Payload y `ExecutionContext` (FACT).** El payload transporta trece campos (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`); `ExecutionContext` representa ocho y omite `profile`, `input_artifacts`, `harness_policy`, `communication_style` y `technical_approach`, pese a que el módulo declara mapear «every field» del payload (`runtime/toolcalls/context.py`). Consecuencia mecánica: dos payloads que difieren sólo en `input_artifacts` producen la misma `SemanticContextIdentity`, la misma `MaterializationIdentity` y la misma materialización canónica.

5. **Tamaño del conjunto estable (FACT).** Para una delegación de fase 06, nueve documentos representativos del conjunto estable suman **55 945 bytes (≈13 987 tokens estimados)**: `_AGENTS.md` (3 418), `.agents/INDEX.md` (1 739), `AGENT_STATE_MACHINE.md` (22 733), `SYSTEM_STATE_MACHINE.md` (3 735), `workflow/06-execute.md` (8 683), `roles/executor.md` (1 825), `HARNESS H05` (6 460), `self-review/SKILL.md` (3 362), `tdd-reviewer/SKILL.md` (3 990). El Context Budget de una delegación completa es de 1 000 estimated tokens (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:4`). La decisión de qué entra en el prefijo **no es marginal**: re-caracteriza el costo de cada delegación, y es exactamente lo que RFC-68 gatea a telemetría (`docs/rfc/68-…md:687-699`).

6. **Sin modelo, cualquier implementación inventaría el prefijo.** Sin una decisión normativa sobre *qué* contenido estable forma el prefijo y *dónde* vive la decisión de orden, la implementación elegiría por conveniencia. Esto es el riesgo que el trabajo previo de la serie ya señaló (`docs/rfc/71-…md:25`).

7. **Estado de la serie.** RFC-71/72/73/74 están `Accepted` (`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`) y los planes 86–93 las materializaron parcialmente. RFC-72 dejó explícitamente el orden concreto como **OPEN / DEFERRED** (`docs/rfc/72-…md:131-138`) y declaró el contrato de materialización canónica como requisito de implementación (misma RFC, sección 3). Esta RFC resuelve esa deuda acotada, sin redefinir el modelo semántico.

---

## Decisiones humanas que autorizan el cambio

Las siguientes decisiones fueron emitidas por el mantenedor (autoridad DECISION,
`.agents/policies/authority.md:Authority classes`). Se incorporan aquí como autoridad del cambio,
no como inferencia del agente.

| ID | Decisión | Efecto |
| --- | --- | --- |
| **HD-1b** | **APROBADO.** El stable prefix reusable del MVP queda acotado a **CORE + WORKER**. Incluye, cuando formen parte de la composición efectiva: bootstrap de Protocol, workflow module, role, profile, harness policy y skills activadas. El segmento **PROJECT / KB queda FUERA** del prefijo del MVP, por su dinámica de invalidación de freshness. La exclusión es **DEFERRED, no una prohibición futura**. | Acota el alcance del prefijo |
| **HD-1b/bootstrap** | **Worker-scope.** «Contexto efectivo» se interpreta en el scope del **Worker** que el Orchestrator delega: se incluye únicamente lo que el Worker lee demostrablemente. El paso `protocol-bootstrap` del orden queda **declarado vacío** para el scope Worker, con su razón documentada. | Elimina la ambigüedad de bootstrap |
| **HD-2b** | **APROBADO.** El orden de materialización provider-bound es **responsabilidad del runtime**, bajo `MaterializationIdentity.ordering_contract_version`. **NO** se convierte el layout en parte de `SemanticContextIdentity`. **NO** se introduce identity primitive nueva. El Protocol define la semántica/clasificación estable/dinámica; el layout byte-level pertenece al runtime. `ordering_contract_version = "2"`. | Ubica la decisión de orden |
| **HD-3** | **NO CHANGE.** `session_uuid` mantiene su posición y semántica. No se elimina de `SemanticContextIdentity`. No se altera el aislamiento cross-session. Se acepta reutilización **intra-session y no cross-session**. La restricción se limita a `session_uuid` y al aislamiento. | Preserva aislamiento |
| **HD-4** | **NO SIMULAR PROVIDER EVIDENCE.** El objetivo es un **INFRASTRUCTURE / READINESS MVP**, no un *proven economic savings MVP*. Prohibido inventar hits, tokens cacheados, ahorro o `provider_cache_event`; prohibido presentar una attestation como evidencia `Observed`. | Fija el target de cierre |
| **HD-5** | **NO AUTHORIZATION** para provider real. `NullProviderAdapter(mechanism="none")` permanece. La integración de provider queda DEFERRED. | Preserva la frontera |
| **HD-6** | No fabricar conclusión económica; **tampoco declarar ahorro**. El beneficio económico queda `UNKNOWN`. | Fija la evidencia admisible |
| **HD-7** | Resolver F-1 antes de implementar. `harness_policy` → entra en materialización. `profile` → entra en materialización. `communication_style` → metadata de ejecución. `technical_approach` → metadata de ejecución. `input_artifacts` → no resolver por inferencia si afecta correctness. | Reconciliación |
| **HD-7/HD-3** | **HD-3 prohíbe únicamente lo relativo a `session_uuid`.** La corrección de completitud de F-1 está **autorizada**: la definición de `SemanticContextIdentity` (`{protocol_version, project_identity, segments[]}`) no cambia; `session_uuid` permanece; el aislamiento cross-session no se altera. | Habilita el cierre de F-1 |

---

## Modelo

### 1. Frontera: semántica vs representación

**Decisión:** se preserva íntegramente la frontera de RFC-71/72. Nada de esta RFC
mueve responsabilidades entre capas.

```text
Context Composition        (Orchestrator; juicio con criterios ordenados)
        ↓
Delegation Payload         (transporte — protocolo)
        ↓
═══ protocol / runtime boundary ═══
        ↓
Materialization            (runtime; determinista por contrato)
        ↓
Canonical Materialization  (runtime; prefijo estable + sufijo dinámico)
        ↓
Provider Adapter → Provider API → provider-side cache
```

- `SemanticContextIdentity` sigue siendo **invariante a materialización** (I-005).
- `MaterializationIdentity` sigue siendo la identidad de **reglas de representación**.
- `ProviderCacheReference` sigue siendo **opaca** y sin rol de correctness (I-MAT-004).
- El Protocol **no** gana conocimiento del cache del provider (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`).

### 2. Definición del stable prefix

**Decisión:** el **stable prefix** es la porción inicial de la Canonical
Materialization compuesta exclusivamente por contenido **Stable** en el sentido
de `protocol/.agents/standards/context/CONTEXT.md:Context classification (Stable / Dynamic)`, en el scope del Worker delegado. Es una **propiedad de
la materialización**, no un segmento, no una identidad y no un objeto de
persistence (consistente con `docs/rfc/72-…md:140-147`).

**Decisión (regla de pertenencia al prefijo).** Un elemento pertenece al prefijo
si y sólo si se cumplen las tres condiciones:

```text
(a) es contenido Stable según la clasificación de CONTEXT.md:236-241;
(b) pertenece al scope de la delegación (Core o Worker);
(c) el protocolo dirige demostrablemente al Worker a consumirlo — o es
    resoluble determinísticamente desde el Delegation Payload.
```

Si un elemento de Core/Worker no satisface (c) sin inferencia, **no se incluye**:
se registra como cuestión abierta. Esta regla es la aplicación directa de la
instrucción de HD-1b («no lo incluyas por inferencia»).

### 3. Contenido del prefijo (alcance HD-1b/bootstrap = Worker-scope)

El prefijo se compone de **seis elementos**, todos resolubles
determinísticamente desde el Delegation Payload o desde el contrato de
delegación. No se inventa ningún elemento.

| # | Elemento del prefijo | Origen de la resolución | Estabilidad | Evidencia de que el Worker lo consume |
| --- | --- | --- | --- | --- |
| 1 | **Workflow module de la fase** | `target_phase` (payload) → `orchestrators/<domain>/workflow/<XX-name>.md` | STABLE | `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Worker Execution` («Reads the target workflow module») |
| 2 | **Role** | `role_to_adopt` (payload) → `roles/<role_to_adopt>.md` | STABLE | `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Worker Execution` («Adopts the specified role») |
| 3 | **Profile** (si `profile != null`) | `profile` (payload) → `roles/profiles/<profile>.md` | STABLE | `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:profile` |
| 4 | **Harness policy del gate** | `harness_policy` (payload) → ruta del payload | STABLE | `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload` |
| 5 | **Skills activadas** (`SKILL.md` por cada nombre) | `skills[]` (payload) → `skills/<name>/SKILL.md` | STABLE | `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:skills` |
| 6 | **Worker bootstrap** | ruta fija `roles/worker.md` | STABLE | `protocol/_AGENTS.md:Active roles` |

**Decisión (paso `protocol-bootstrap` del orden).** El orden aprobado por HD-2b
nombra `protocol-bootstrap` como paso 1. La verificación de este RFC establece
que **el bootstrap del Protocol no pertenece al scope del Worker**:

```text
`protocol/_AGENTS.md:Before any task`              →  «Load the system role …
                                                      Load the state machine …
                                                      Load the orchestrator role»
`protocol/.agents/INDEX.md:Before executing any task`
                                                   →  la secuencia de carga nombra
                                                      al orchestrator, no al Worker
`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Worker Execution`
                                                   →  la ejecución del Worker lee
                                                      workflow module, perfil,
                                                      skills y input artifacts;
                                                      ningún documento de bootstrap
`protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`
                                                   →  ningún estado exige leer un
                                                      documento de bootstrap
```

Por lo tanto, en el contrato v2 el paso 1 existe como **categoría declarada y
vacía** para el scope Worker. Su contenido correcto para otros scopes es
**UNKNOWN** y no se define aquí.

### 4. Contenido FUERA del prefijo

**Decisión (HD-1b):** el segmento **Project / KB queda fuera** del stable prefix
del MVP. Fundamento: su freshness/lifecycle introduce una dinámica de
invalidación distinta de la invalidación por identidad (`docs/rfc/73-…md:89-100`;
`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`) y no es necesaria para demostrar el mecanismo de
prefijo provider-bound.

**Decisión:** la exclusión es **DEFERRED, no una prohibición**. La reutilización
de Project/KB como prefijo queda diferida a una fase posterior basada en
evidencia.

**Decisión:** el **sufijo dinámico** comprende `task_summary`, `knowledge_entries`,
`input_artifacts` (referencias) y la metadata de ejecución/sesión
(`session_uuid`, `current_state`, `target_phase`, `context_budget`). El sufijo
dinámico **no** forma parte del prefijo estable y su variación no debe alterar el
prefijo.

### 5. Ordering Contract v2

**Decisión (HD-2b):** el orden pertenece al **runtime**, identificado por
`MaterializationIdentity.ordering_contract_version`. `"2"` está **disponible**:
el único valor implementado hoy es `ORDERING_CONTRACT_V1 = "1"`
(`runtime/toolcalls/canonical.py`) y no existe ninguna otra ocurrencia del
literal `"2"` para ese campo en `runtime/`, `tests/` ni `docs/`.

**Decisión:** el contrato v2 establece el orden siguiente. Es la materialización
de la clasificación real del sistema (`protocol/.agents/standards/context/CONTEXT.md:Context classification (Stable / Dynamic)`), no una lista
inventada para obtener cache hits.

```text
Ordering Contract v2
  1. protocol-bootstrap      CORE     declarado y vacío (scope Worker; §3)
  2. workflow-module         WORKER   STABLE
  3. role / profile          WORKER   STABLE
  4. harness-policy          WORKER   STABLE
  5. skills                  WORKER   STABLE
  6. input-artifact-refs     TASK     referencias; identidad-sensible (§6)
  7. task-summary            TASK     DINÁMICO
  8. execution-metadata      META     DINÁMICO
       session_uuid, current_state, target_phase, context_budget
```

**Decisión (preservación del prefijo).** Ningún elemento del sufijo dinámico
puede preceder a un elemento estable. Un cambio en el sufijo dinámico **no debe**
alterar los bytes del prefijo.

**Aclaración de implementación (2026-09-14, durante la ejecución del Plan 121).**
La verificación empírica mostró que `SemanticContextIdentity` es sensible a
`session_uuid` (PC-006), por lo que colocar el ancla de identidad *después* de la
región estable la volvía no-invariante y hacía PC-003 falso a nivel de bytes. La
representación se compone entonces como: **anclas de identidad → región estable →
resto parametrizado**. Los dos anclas son estáticas por construcción para un
contexto entregado dado (`materialization_version` siempre lo es;
`SemanticContextIdentity` lo es por contexto), de modo que la región estable queda
como **prefijo de bytes** del payload e invariante a `session_uuid`, `task` y
referencias de artifacts, que es exactamente lo que PC-002/PC-003 exigen.

**Precisión de contrato.** `ordering_contract_version` ordena los **steps de
contenido** de la representación (los seis elementos estables y el sufijo
dinámico). Las **anclas de identidad** (`materialization_identity`,
`semantic_context_identity`) no son steps de contenido: se representan para
preservar I-MAT-001 y el prefijo, y preceden al primer step de contenido. Esto no
cambia el orden de ningún elemento de contenido y **no** modifica
`SemanticContextIdentity`.

**Decisión (incompatibilidad de contrato).** Un runtime que no implemente el
contrato v2 debe rechazar la materialización, como ya ocurre con
`ordering_contract_version` (`runtime/toolcalls/canonical.py`). La implementación **no**
debe aceptar silenciosamente una representación distinta bajo la misma
`MaterializationIdentity`.

### 6. Reconciliación `ExecutionContext` ↔ Delegation Payload (HD-7)

**Decisión:** se resuelve F-1 con el tratamiento aprobado. Ningún campo se
resuelve por inferencia.

| Campo del payload | Tratamiento decidido | Racional |
| --- | --- | --- |
| `harness_policy` | **Entra en la materialización** (Worker, STABLE) | Documento estable del protocolo que gobierna el gate de la fase |
| `profile` | **Entra en la materialización** (Worker, STABLE) | El contrato obliga a leer `roles/profiles/<profile>.md` (`:104`) |
| `input_artifacts` | **Entra en la materialización como referencias** (TASK) | Ver decisión siguiente. Las **referencias** son identidad-sensibles; el **contenido** no se materializa |
| `communication_style` | **Metadata de ejecución** | Afecta el formato de salida del Worker, no la identidad del contexto |
| `technical_approach` | **Metadata de ejecución** | Se copia desde `TASK_SPECIFICATION.md`; es una decisión de la especificación, no contexto estable |

**Decisión (`input_artifacts`).** Se materializan **las referencias**, no el
contenido:

1. **Las referencias entran en la derivación de identidad.** Dos delegaciones que
   reciben conjuntos distintos de input artifacts son contextos distintos; hoy
   colisionan en `SemanticContextIdentity` y eso es un **false hit potencial**,
   que la política vigente prohíbe («false miss es aceptable; false hit NO es
   aceptable»).
2. **El contenido de los artifacts NO se materializa como prefijo.** Es contenido
   dinámico de sesión, y `protocol/.agents/standards/context/CONTEXT.md:2` prohíbe incluir artefactos completos
   de sesiones previas. Las referencias son el mecanismo ya usado por el
   protocolo (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`).

**Decisión (efecto sobre `SemanticContextIdentity`).** La corrección de
completitud de F-1 está autorizada por HD-7/HD-3. Concretamente:

```text
NO cambia:  la definición de SCI ({protocol_version, project_identity, segments[]})
NO cambia:  session_uuid (permanece en su posición y semántica)
NO cambia:  el aislamiento cross-session
SÍ cambia:  el conjunto de campos del contexto entregado que participan de la
            derivación — pasa a cubrir el payload completo (cierra F-1)
```

Esta es la lectura autorizada explícitamente: la restricción de HD-3 se limita a
`session_uuid` y al aislamiento.

### 7. `MaterializationIdentity` — efecto

**Decisión:** el cambio de representación **debe** reflejarse en
`MaterializationIdentity`, o I-MAT-001 se vuelve falso. Mecánicamente:

```text
MaterializationIdentity = {
    materialization_version: {
        variant:                   sin cambio (prompt | toolcalls)
        ordering_contract_version: "2"     ← cambia
        serialization_version:     según la implementación del Plan
    }
    provider? / model? / model_version?    sin cambio (condicionales; sin evidencia
                                           que obligue a incluirlos)
}
```

**Decisión (`variant`).** La extensión del contenido no exige un `variant` nuevo:
el conjunto de contenido forma parte del contrato de materialización que el
runtime declara, y el par `(variant, ordering_contract_version)` identifica la
representación de forma suficiente en el alcance de este MVP. **Requisito de
implementación futura:** si el Plan demuestra que dos conjuntos de contenido
distintos pueden coexistir bajo el mismo par, debe introducirse una dimensión de
contenido. Esto es una obligación de honestidad del contrato, no una preferencia.

**Decisión:** `provider`, `model` y `model_version` **no** participan. RFC-72 §2
los hace condicionales «según evidencia» y no hay provider integrado (HD-5). Su
participación queda DEFERRED.

### 8. Preservación de aislamiento (HD-3)

**Decisión:** el aislamiento se preserva sin cambios:

- `session_uuid` permanece dentro del contenido canónico del segmento worker
  (`runtime/toolcalls/identity.py`) y por lo tanto en
  `SemanticContextIdentity`.
- El reuso del prefijo es **intra-session**. La reutilización **cross-session no
  se busca** como optimización lateral.
- El aislamiento por `ProjectIdentity` permanece intacto y **no** se toca: el
  Project/KB no participa del prefijo (HD-1b).
- El reuso cross-project sigue prohibido salvo autorización explícita (I-008).

**Decisión:** ninguna parte de esta RFC obtiene reutilización a costa de
aislamiento. Es la aplicación de la regla de HD-3 («prioriza correctness/isolation
sobre maximización de cache hit»).

### 9. Observabilidad (HD-4)

**Decisión:** el MVP es de **readiness**. No se simula evidencia de provider.

- El contrato de observabilidad existente (`reuse_event`,
  `provider_cache_event`; `protocol/.agents/contracts/METRICS.md:Event catalog`) y su
  catálogo (`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Reuse and cache`) se preservan sin cambios.
- **Prohibido:** fabricar `provider_cache_event`; declarar hits, tokens cacheados
  o ahorro; presentar una attestation como evidencia `Observed`
  (`protocol/.agents/standards/quality/EVIDENCE.md:The VERIFIED invariant`).
- El **writer de telemetría** entra en el alcance del Plan **únicamente** si es
  necesario para el readiness MVP, y sin fingir observaciones de provider.
- La ausencia de evidencia provider-side queda como **limitación explícita**.

**Decisión:** el beneficio económico permanece `UNKNOWN` (HD-6). No se declara
ahorro.

### 10. Frontera con la política de composición (aclaración, no cambio)

**Decisión:** esta RFC **no** modifica `protocol/.agents/standards/context/COMPOSITION_COMPRESSION.md` ni `protocol/.agents/standards/context/CONTEXT.md`
§8. Se declara explícitamente la distinción de capas para evitar una futura
lectura contradictoria:

| Capa | Qué gobierna | Efecto del prefijo |
| --- | --- | --- |
| **Composición** (`protocol/.agents/standards/context/COMPOSITION_COMPRESSION.md:2`) | La forma del **payload del protocolo**: el contenido estable se **cita por referencia**, no se pega inline | Sin cambio |
| **Materialización** (esta RFC) | La **representación dirigida al provider** producida por el runtime a partir del Execution Context resuelto | El runtime resuelve las referencias a contenido estable en el prefijo |

**Decisión (fundamento de la no-contradicción).** La regla «reference instead of
inline» gobierna **qué escribe el Orchestrator en el payload**; el prefijo
materializado es la representación que el runtime produce **a partir de** ese
payload. Son magnitudes distintas, ya separadas por
`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:8` (semantic budget ≠ physical/provider cost ≠
prompt materialization cost). Esta RFC no altera la primera.

**Decisión:** el prefijo **no** modifica los límites semánticos del Context
Budget (I-010 / `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:8`). Un prefijo cacheado no vuelve
más pequeño el contexto semántico.

### 11. Invariantes

- **PC-001 — Prefijo determinístico:** la misma `(SemanticContextIdentity,
  MaterializationIdentity)` produce la misma Canonical Materialization, incluido
  su prefijo (extiende I-MAT-001 al prefijo).
- **PC-002 — Prefijo antes del sufijo:** ningún elemento dinámico precede a un
  elemento estable en el contrato ordenado.
- **PC-003 — Sufijo sin efecto sobre el prefijo:** un cambio en el sufijo
  dinámico no altera los bytes del prefijo.
- **PC-004 — Completitud de la composición:** el conjunto de campos del Delegation
  Payload que constituyen el contexto entregado participa de la derivación de
  identidad; dos payloads que difieren en un campo del contexto entregado no
  comparten `SemanticContextIdentity` (cierra F-1).
- **PC-005 — Separación semántica/materialización:** un cambio de orden produce
  `MaterializationIdentity` distinta y `SemanticContextIdentity` idéntica
  (instancia de I-MAT-012).
- **PC-006 — Aislamiento preservado:** `session_uuid` permanece en la identidad;
  el reuso es intra-session; el aislamiento cross-project no se altera (I-008).
- **PC-007 — Frontera del provider:** ninguna semántica de provider entra en el
  core; `ProviderCacheReference` permanece opaca y sin rol de correctness
  (I-MAT-004).
- **PC-008 — Sin evidencia fabricada:** ninguna afirmación de hit, tokens
  cacheados, ahorro o costo se emite sin observación del provider (I-ECO-005,
  I-ECO-006).
- **PC-009 — Resolución genuina:** un elemento del prefijo que no pueda
  resolverse produce un fallo declarado, nunca contenido inventado
  (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:skills`; `protocol/.agents/standards/conduct/ANTI_CIRCUMVENTION.md:Rule`).
- **PC-010 — Project/KB fuera:** el segmento Project/KB no forma parte del
  prefijo de este MVP (DEFERRED, no prohibido).

### 12. Carga de trabajo / tamaño (limitación declarada)

**Requisito de implementación futura:** el prefijo del contrato v2 tendrá un
tamaño sustancial (los seis elementos de §3; el orden de magnitud observado en los
documentos representativos es de decenas de KB por delegación). El prefijo se
envía en **cada** invocación.

**Limitación explícita:** sin telemetría y sin provider no puede demostrarse que
el net benefit sea positivo. Esto **no** invalida el readiness MVP (cuyo objetivo
declarado es la representación, el determinismo y el contrato), pero **debe**
quedar registrado como limitación y **no** puede presentarse como ahorro.

---

## Alcance

### In scope (si se acepta y se implementa por Plan)

- A. Materialización del stable prefix Core + Worker (§3).
- B. Ordering Contract v2 (§5).
- C. Actualización de `MaterializationIdentity` necesaria para representar
  correctamente la nueva representación (§7).
- D. Reconciliación `ExecutionContext` ↔ Delegation Payload / F-1 (§6).
- E. Corrección de los invariantes y tests afectados — incluida F-2.
- F. Writer de telemetría únicamente si es necesario para el readiness MVP, sin
  fingir observaciones de provider (§9).
- G. Dogfood mediante un Change real.
- H. Documentación de limitations y deferred work.

### Out of scope (no autorizado)

provider real; reutilización de cache cross-session; Project/KB como stable prefix;
identity primitive nueva; registry nuevo; estado nuevo; workflow phase nueva;
authority class nueva; cache database; implementación provider-specific; cache
correctness gate; release.

### Esta RFC no define

- APIs de provider, cache keys, breakpoints, TTL de provider ni evicción;
- implementación de adapters;
- backend de persistence, schema ni eviction;
- umbrales económicos ni pricing;
- un orden concreto para scopes distintos del Worker;
- el contenido del paso `protocol-bootstrap` (declarado vacío; UNKNOWN fuera del
  scope Worker);
- telemetría de provider.

---

## Alternativas consideradas

1. **No hacer nada.** Mantiene un prefijo útil de ~117 bytes y deja el contrato de
   materialización canónica incumplido respecto de su propósito (`docs/rfc/72-…md:3`).
   Descartada por la autoridad de HD-1b.
2. **Incluir el bootstrap del Protocol en el prefijo del Worker.** Añadiría ~32 KB
   de documentos que el Worker no lee demostrablemente (`protocol/_AGENTS.md:Before any task` ordena
   su lectura al Orchestrator). Descartada por la regla de HD-1b («no incluir por
   inferencia»); el paso queda declarado vacío.
3. **Incluir Project/KB en el prefijo.** Introduce invalidación de freshness dentro
   del prefijo y tensiona la separación de dominios de invalidación. Diferida por
   HD-1b.
4. **Ordenar con el contenido estable al final.** Destruye el prefijo reutilizable,
   que es el objeto del cambio. Descartada.
5. **Fijar el orden en el Protocol (normativo payload).** El layout de bytes es
   representación y la representación pertenece al runtime
   (`docs/rfc/13-…md:145-152`). Descartada por HD-2b.
6. **Incluir el contenido de los `input_artifacts` en el prefijo.** Contenido
   dinámico de sesión; `protocol/.agents/standards/context/CONTEXT.md:2` prohíbe incluir artefactos completos de
   sesiones previas. Descartada; se materializan las **referencias**.
7. **Crear una identidad o un hash de prefijo.** RFC-71 rechazó
   `ProviderCacheIdentity` y el par `(SCI, MI)` es suficiente. Descartada.
8. **Eliminar `session_uuid` de la identidad para habilitar reuso cross-session.**
   Sacrifica aislamiento por hits. Descartada explícitamente por HD-3.
9. **Simular un provider que reporte hits.** Falsificaría la evidencia. Descartada
   por HD-4/HD-5.

---

## Impacto en el protocolo

**Clase RFC-56: A** (modelo conceptual / contratos). Si se acepta:

| Artefacto del payload | Cambio | Motivo |
| --- | --- | --- |
| `standards/context/CONTEXT.md` | Adición de la sección de **stable prefix provider-bound** y de la aclaración de frontera con la política de compresión (§3–§6, §10 de esta RFC) | El Protocol debe definir la semántica que determina qué contenido es estable y por qué; el layout queda en el runtime |
| `standards/context/BUDGET_MATERIALIZATION.md` | **Condicional**, sólo si el Plan demuestra que la interacción prefijo↔Budget necesita una precisión adicional | I-010 ya está normado; no se anticipa cambio |
| `VERSION` | Bump **MINOR** (aditivo y compatible) si se toca el payload | `docs/VERSIONING.md:3` |

**Sin cambio de significado en:** `SemanticContextIdentity`,
`SegmentIdentity`, `SegmentContentIdentity`, `MaterializationIdentity` (su
*forma* no cambia; cambia el valor de un componente versionado),
`ProviderCacheReference`, los tres dominios de invalidación, el Context Budget,
la política de composición y las state machines.

**Compatibilidad:** aditiva. Un runtime que no implemente el contrato v2 debe
rechazar la materialización (comportamiento ya presente en
`runtime/toolcalls/canonical.py`), no reinterpretarla.

**Qué deja de ser válido:** el `Ordering Contract v1` deja de ser el contrato
vigente del runtime de referencia. No se elimina: queda como contrato histórico
identificado por `ordering_contract_version = "1"`.

> **Nota de honestidad.** `docs/rfc/72-…md:129` afirma que el repositorio «no
> tiene hoy un contrato de materialización canónica». Tras el plan 89 el runtime
> sí lo implementa. Esta RFC no enmienda RFC-72 durante su redacción; la
> corrección de esa afirmación es el defecto **F-3** y se registra como
> **deferred**, no se resuelve incidentalmente aquí.

---

## Criterios de aceptación

Verificables por el Plan que la ejecute. Diferidos a ese Plan los que dependan de
la implementación.

- [ ] `CONTEXT.md` define el stable prefix provider-bound, la regla de pertenencia
      y la frontera con la política de compresión, sin redefinir Stable/Dynamic.
- [ ] El Execution Context del runtime cubre el Delegation Payload completo según
      el tratamiento de §6; `communication_style` y `technical_approach` quedan
      clasificados como metadata de ejecución.
- [ ] Las referencias de `input_artifacts` participan de la derivación de
      identidad; su **contenido** no se materializa.
- [ ] Existe `OrderingContract` v2 con el orden de §5 y el paso
      `protocol-bootstrap` declarado vacío con su razón.
- [ ] Un cambio de orden produce `MaterializationIdentity` distinta y
      `SemanticContextIdentity` idéntica (PC-005).
- [ ] `session_uuid` permanece en la identidad y el aislamiento no se altera (PC-006).
- [ ] El Project/KB no participa del prefijo (PC-010).
- [ ] Dos payloads que difieren en un campo del contexto entregado no comparten
      `SemanticContextIdentity` (PC-004).
- [ ] Un elemento del prefijo irresoluble produce un fallo declarado y nunca
      contenido inventado (PC-009).
- [ ] F-2 corregido: el test prueba la composición relevante y no sólo
      `session_uuid`.
- [ ] No existe ninguna afirmación de hit, tokens cacheados, ahorro ni costo sin
      observación de provider (PC-008).
- [ ] `NullProviderAdapter(mechanism="none")` permanece; ningún provider real
      incorporado.
- [ ] La batería canónica está en verde, con la clase ambiental de basetemp
      declarada como factor ambiental y no como FAIL.
- [ ] Las limitaciones (tamaño del prefijo, ausencia de evidencia de provider,
      beneficio económico `UNKNOWN`) están registradas.

---

## Amendment Log

- 2026-09-14 — Creación. Incorpora las decisiones humanas HD-1b, HD-2b, HD-3,
  HD-4, HD-5, HD-6 y HD-7, y las dos acotaciones resueltas por el mantenedor
  (Worker-scope para «contexto efectivo»; restricción de HD-3 limitada a
  `session_uuid`, con la completitud de F-1 autorizada). Derivada de
  `docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md` y del Phase 2 Report
  (`PHASE_2_STOPPED_AT_AUTHORIZATION_GATE`). `Status: Proposal`: no habilita tocar
  `protocol/.agents/`. DEFERRED registrados: Project/KB como prefijo (`docs/rfc/71-…md`
  y `73-…md` como base), F-3/F-4/F-6/F-7/F-8, participación de
  `provider`/`model`/`model_version` en `MaterializationIdentity`, y toda
  evidencia provider-side.
- 2026-09-14 — **Aceptada (plan 121)** por autorización humana explícita del
  mantenedor: confirmadas HD-1b, HD-1b/bootstrap, HD-2b, HD-3, HD-4, HD-5, HD-6,
  HD-7 y HD-7/HD-3, y autorizada la aceptación siguiendo el Change Lifecycle sin
  introducir decisiones nuevas. Habilita la vía Clase A de RFC-56 para modificar
  `protocol/.agents/`; la ejecución queda en el Plan 121. No autoriza release,
  tag, promoción a `master` ni publicación.
- 2026-09-14 — **Aclaración registrada durante la ejecución del plan 121** (§5):
  la composición de la representación v2 es *banner de identidad estático →
  región estable → resto parametrizado*, para que la región estable sea un
  **prefijo de bytes** invariante a `session_uuid`/`task`/artefactos (PC-002,
  PC-003), dado que `SemanticContextIdentity` participa de `session_uuid`
  (PC-006). Precisión de contrato: `ordering_contract_version` ordena los **steps
  de contenido**; las anclas de identidad no son steps de contenido y las
  preceden. No cambia el orden de ningún elemento de contenido ni modifica
  `SemanticContextIdentity`.
