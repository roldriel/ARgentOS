# Architectural Decision Model

> Modelo de decisiones arquitectónicas de ARgentOS, derivado de
> `ARCHITECTURAL_PROBLEM_MODEL.md`. Su propósito es llegar al punto inmediatamente anterior a la
> redacción de RFCs: cada decisión define opciones, una decisión tomada, consecuencias, invariantes,
> componentes afectados, límite de RFC, impacto de implementación, dependencias y estado.
>
> **Regla operativa:** si una decisión tiene suficiente evidencia para avanzar, se decide. Si queda
> incertidumbre no bloqueante, se usa `PROVISIONALLY_DECIDED`. Si una cuestión no puede resolverse
> con la información disponible, se marca `OPEN DECISION` y se continúa.
>
> No se modifica código, policies, contracts, RFCs, artefactos ni BeaconRBX. No se redactan RFCs.

---

## Mapping de identificadores

El Problem Model usaba D1–D13 como preguntas abiertas. Este documento reutiliza esos identificadores
como **decisiones** con contenido propio:

| Decisión | Tema | Pregunta del Problem Model que responde |
|---|---|---|
| D0 | Guarantee Model | D11 (restricción RC-01) + criterio de qué garantías existen |
| D1 | State Semantics (dimensiones) | D2, D3, D5 (CG-01) |
| D2 | Artifact Lifecycle | D5 (CG-01) |
| D3 | Completion Semantics | D3 (CG-01) |
| D4 | Evidence Model | D13 (CG-03) |
| D5 | Execution Identity | D1 (CG-02) |
| D6 | Execution Record / Audit Trail | D1, D6, D9, D12 (CG-02) |
| D7 | Temporal Semantics | D6 (CG-02) |
| D8 | Authorization Model | D4 (CG-05) |
| D9 | Knowledge Lifecycle | D7 (CG-04) |
| D10 | Observability / Budget | D6 (CG-02/CG-03) |
| D11 | Enforcement Boundaries | D11, D13 (RC-01) |
| D12 | Artifact / State / Evidence Relationship | D5, D13 (CG-01/CG-03) |
| D13 | Implementation Priority | D12 (meta) |

---

## Newly Discovered Blocking Issue

- **NBI-1 (no bloqueante):** `tools/aggregate_metrics.py` calcula `session.duration_ms` como
  `max(timestamps) − min(timestamps)` mezclando los relojes de HARNESS_REPORT y METRICS, que bajo P3
  divergen. La métrica de duración es, por lo tanto, no confiable tal como está calculada. Afecta a
  D10 (la capa de measurement debe declarar la fuente temporal de cada evento). No bloquea ninguna
  decisión; se corrige como parte de D7/D10.
- **NBI-2:** ninguna otra observación nueva afecta directamente a las decisiones. No se abre una
  fase de auditoría.

---

## D0 — Guarantee Model

### Question

¿Qué garantías pretende proporcionar ARgentOS, qué NO garantiza, y en qué capa vive cada garantía
(declarativa, verificable, mecánicamente enforceable, dependiente de juicio, dependiente de
actores externos)?

### Why

RC-01 del Problem Model identifica que la causa estructural de P1/P3/P4/P10/P15/P16/P18 es el
modelo "documentos + juicio del agente" con una capa mecánica mínima. Sin una decisión sobre qué
garantiza el sistema, cada decisión posterior (evidencia, enforcement, auditoría) queda sin criterio.
Además, términos como "zero hallucinations" se usan sin semántica operacional.

### Affected Problems

P1, P3, P4, P10, P15, P16, P18; CG-02, CG-03; RC-01.

### Constraints

- Modo declarativo sin requisito de Python para adoptantes (`harness/INDEX.md`); cualquier
  enforcement mecánico nuevo debe ser stdlib-only y opcional.
- El modelo de tres capas (enforced / reviewed / verified) ya está declarado y debe extenderse, no
  contradecirse.
- `.agents/` inmutable; cambios vía RFC/plan (RFC-56). MAJOR requiere confirmación del usuario.
- "Zero hallucinations" no es una garantía técnica; debe reemplazarse por una formulación
  operacional.

### Options

#### Option A — Garantías declarativas puras

Mantener el estado actual: las garantías son declaraciones de intención y la verificación es juicio
del agente.

Pros: cero cambios de modelo; coherente con el modo declarativo.

Cons: deja P1/P3/P4/P10/P15/P16 sin respuesta; reproduce los problemas observados en BeaconRBX.

#### Option B — Modelo híbrido con catálogo de garantías clasificadas

Definir un catálogo cerrado de garantías, cada una con una clase:

- **Declarativa:** política del protocolo sin verificación mecánica (p. ej., "la KB solo se actualiza
  por pipeline").
- **Verificable:** comprobable desde artefactos por herramientas (presencia, versión, timestamps,
  evidencia asociada, consistencia bidireccional de gates).
- **Mecánicamente enforceada:** ejecutada por runtime/hooks (registro de gates, sonda de estado,
  deny de escritura sin H04 en modo enforced, stop sin cierre).
- **Dependiente del juicio del agente:** toda evaluación semántica no cubierta por las anteriores;
  su resultado se registra como atestación o juicio con evidencia citada.
- **Dependiente de actores externos:** aprobaciones humanas, herramientas externas, reproductibilidad
  de salidas de comandos (best-effort).

Pros: resuelve la ambigüedad de RC-01; da criterio a D4/D6/D11; es compatible con el modo
declarativo (las clases se declaran; solo el subconjunto mecánico se enforcea cuando hay runtime).

Cons: requiere tocar contratos y documentación (MAJOR); exige disciplina para no etiquetar todo como
"declarativo".

#### Option C — Enforcement mecánico total

Convertir la mayoría de las garantías en checks de runtime.

Pros: máximo determinismo.

Cons: rompe el modo declarativo sin Python; incompatible con la filosofía de adopción; inviable en el
horizonte inmediato.

### Decision

**Option B.** ARgentOS garantiza un conjunto acotado y clasificado de propiedades; no garantiza
corrección semántica del juicio, ni independencia de verificación en single-instance, ni ausencia
de alucinación. "Zero hallucinations" se redefine operacionalmente como: *todo claim emitido por el
protocolo debe ser evidencia-citado o estar marcado explícitamente como atestación/inferencia*.

Catálogo adoptado:

| Garantía | Clase | Verificable por |
|---|---|---|
| Identidad y versionado de sesión (protocol_version, UUID) | Verificable | Runtime (dev tool) + agente |
| Presencia de registros de sesión (state.json, HARNESS, METRICS, SESSION_LOG) | Verificable | Runtime (dev tool) + agente |
| Registro de gates (qué gate, resultado, cuándo) | Mecánica | runner_state (estado) + agente (review) |
| Coherencia state.json ↔ HARNESS (bidireccional, tiempos) | Verificable | Runtime (dev tool) |
| Estructura de artefactos (secciones, ENTRY/METRIC, EARS) | Verificable | gate_validator (estructural) + agente |
| Evidencia asociada a claims (clase + referencia) | Verificable | agente + dev tool (D4) |
| Autorización determinable para efectos fuera de frontera | Verificable | agente + humano (D8) |
| Freshness/invalidación de knowledge | Verificable | agente + dev tool (D9) |
| Cumplimiento de budget (par declared/consumed) | Verificable | runtime + agente (D10) |
| Reproducibilidad de ítems `[gate]` | Verificable (best-effort) | dev tool (`audit_gates`) |
| Independencia de verificación | Dependiente de actores externos | solo multi-agent; en single-instance se declara atestación |
| Aprobaciones humanas | Dependiente de actores externos | humano |

### Rationale

El Problem Model demostró que los problemas confirmados son mayormente de enforcement y semántica
indefinida, no de ausencia de reglas. Option B ataca exactamente eso: declara qué es verificable y
qué no, mantiene el modo declarativo y permite implementar el subconjunto mecánico con scripts
stdlib (igual que los actuales). Option A reproduce el estado actual; Option C rompe la adopción.

### Consequences

- Los artefactos y registros ganan campos de clase de garantía/evidencia (D4).
- El Runtime puede implementar checks mecánicos nuevos (presencia, versión, reconciliación) sin
  cambiar la filosofía documental.
- Las claims de "verificado" dejan de ser auto-suficientes: exigen evidencia o marca de atestación.
- Se elimina el uso literal de "zero hallucinations" como garantía técnica.

### Invariants

- G-1: toda sesión declara `protocol_version` y produce los registros raíz.
- G-2: todo gate PASS identifica su evidencia (o declara atestación).
- G-3: toda claim de "verificado" referencia una entrada de evidencia con clase.
- G-4: los timestamps de registros mecánicos usan reloj UTC; los del agente se marcan
  `source: agent_clock` cuando no hay reloj disponible.
- G-5: ninguna garantía se etiqueta "mecánica" si depende de juicio del agente.

### Affected Components

`PROTOCOL_HEALTH.md`, `harness/INDEX.md` (enforcement model), contratos SESSION_LOG/METRICS/
HARNESS_REPORT/VERIFICATION_REPORT, `runner_state.py` (registro de garantías mecánicas),
`aggregate_metrics.py`/`check_session_artifacts.py` (checks verificables), policies H01/H06/H07.

### RFC Boundary

RFC-A "Guarantee Model & Enforcement Boundaries": catálogo de garantías, clases, matriz de quién
verifica cada una, redefinición operacional de "zero hallucinations", invariantes G-1…G-5. Incluye
D11. NO incluye: clases de evidencia detalladas (D4), modelo de autorización (D8), conocimiento (D9).

### Implementation Impact

Alto nivel: documentación de payload (contratos/estándares) + campos nuevos en artefactos +
extensiones stdlib a los checkers dev. Sin cambios de runtime obligatorios para adoptantes.

### Dependencies

Ninguna (fundacional).

### Status

DECIDED.

---

## D1 — State Semantics (dimensiones de estado)

### Question

¿Qué dimensiones de estado existen realmente en ARgentOS, cuáles son independientes, cuáles son
derivadas, y quién produce cada transición?

### Why

CG-01 agrupa P2, P8, P9 y P17 bajo una semántica de estado indefinida: `status`, `approved`,
`validation.complete`, `state`, COMPLETED y "review gate" se usan sin modelo. Sin separar
dimensiones, ningún check de coherencia ni estado terminal es definible.

### Affected Problems

P2, P8, P9, P17; CG-01; RC-02.

### Constraints

- La máquina de estados core (18 estados) existe y es la base del orquestador; no se propone
  reemplazarla.
- `state.json` ya registra gates y status terminal; su schema debe seguir siendo stdlib-parseable.
- No mezclar con el lifecycle de artefactos (D2) ni con la dimensión de evidencia (D4).

### Options

#### Option A — Dimensión única (Task State) + atributos

Todo "estado" es el estado de la tarea; `status` de artefacto, aprobación, etc. son atributos sin
máquina.

Pros: mínimo.

Cons: no resuelve P2/P8/P9 (los campos siguen sin semántica; "approved" no tiene dueño).

#### Option B — Separación completa (7 dimensiones independientes)

Task, Artifact Lifecycle, Execution, Verification, Approval, Plan y Gate como máquinas separadas.

Pros: máxima claridad.

Cons: sobre-ingeniería; la evidencia no justifica 7 máquinas.

#### Option C — Separación mínima con derivaciones explícitas

Tres dimensiones con entidad propia (Task State, Gate State, Artifact Lifecycle) y cuatro conceptos
derivados (Execution State ≡ Task State; Verification State = derivada de Gate State + reporte;
Approval State = conjunto de registros de aprobación; Plan State = gobernanza externa referenciada,
no definida).

Pros: resuelve los cuatro problemas con el mínimo de máquinas nuevas; cada derivación tiene una
fuente determinable.

Cons: requiere documentar explícitamente las derivaciones para evitar re-mezcla.

### Decision

**Option C.** Dimensiones:

| Dimensión | Tipo | Fuente de verdad | Transiciones producidas por |
|---|---|---|---|
| Task State | entidad (máquina core existente, 18 estados) | state.json + AGENT_STATE_MACHINE | orquestador |
| Gate State | entidad (por gate: pending/passed/failed/skipped:profile) | state.json (gates de transición) + HARNESS ENTRY | orquestador (juicio) + runner_state (registro) |
| Artifact Lifecycle | entidad (D2) | derivada del Gate State + registro de gates | derivación (no escritura manual) |
| Execution State | derivada | ≡ Task State (alias; no entidad nueva) | — |
| Verification State | derivada | Gate State (H06/H07) + VERIFICATION_REPORT + REVIEW_REPORT | — |
| Approval State | derivada | SESSION_BRIEF (confirmaciones) + registros de pendientes humanos | usuario |
| Plan State | externa | docs/plans del proyecto (no ARgentOS) | gobernanza del proyecto |

Relaciones:

- Task State y Artifact Lifecycle **coexisten** (un artefacto puede estar "validated" mientras la
  tarea está en EXECUTING).
- Gate State es **por gate**; Task State es único por tarea.
- Approval State y Task State **no se mezclan**: COMPLETED es relativo al alcance (D3).
- "review required" es un valor del Gate State sobre REVIEW_REPORT (ver D2), no un estado de tarea.
- Terminal: Task terminal = COMPLETED/ABORT; Gate terminal = passed/failed/skipped; Artifact
  terminal = superseded/archived; Approval terminal = approved/rejected/deferred.

### Rationale

La evidencia (P2/P17: campos sin semántica; P8: review gate sin dimensión; P9: COMPLETED con
pendientes) muestra que el problema no es sincronización sino factorización. Option C da a cada
concepto una fuente determinable con el mínimo de entidades nuevas, y mantiene la máquina core
intacta.

### Consequences

- Los campos `status`/`approved`/`validation.complete`/`state` de los artefactos dejan de ser
  estados manuales (ver D2).
- El "review gate" deja de ser un estado de tarea: es un Gate State sobre REVIEW_REPORT.
- COMPLETED pasa a tener semántica de alcance (D3).

### Invariants

- ST-1: Task State solo cambia por transiciones permitidas de AGENT_STATE_MACHINE.
- ST-2: todo gate de transición (H00–H07, H11) tiene Gate State registrado en state.json.
- ST-3: el Artifact Lifecycle nunca es escrito a mano; es derivado del Gate State.
- ST-4: ningún documento del payload declara "estado" sin indicar la dimensión.

### Affected Components

AGENT_STATE_MACHINE.md (tabla de perfiles/review gate), contratos de artefactos, state.json
(documentación de schema), harness policies H00–H07/H11.

### RFC Boundary

RFC-B "State & Artifact Lifecycle Semantics": dimensiones, derivaciones, tabla de actores,
eliminación del review gate como estado de tarea. Incluye D2, D3 y la parte de D12 que no depende de
evidencia. NO incluye: evidencia (D4), registro de eventos (D6).

### Implementation Impact

Documental (payload) + validador: checks de coherencia de dimensiones y existencia de REVIEW_REPORT
para complex.

### Dependencies

D0 (informativa: define qué significa "verified", pero D1 no la bloquea).

### Status

DECIDED.

---

## D2 — Artifact Lifecycle

### Question

¿Qué lifecycle tienen los artefactos de sesión, qué términos son estados, cuáles eventos, cuáles
propiedades, y quién produce cada transición?

### Why

P2 y P17 muestran artefactos con `status="draft"`, `approved=false` y secciones contradictorias
mientras los gates registran PASS. El lifecycle actual es un campo de texto sin reglas.

### Affected Problems

P2, P17; CG-01.

### Constraints

- No mezclar con Task State (D1).
- El registro de gates (state.json + HARNESS) es la fuente de hechos; el artefacto no debe duplicar
  ese hecho con un campo manual.
- Los contratos usan `schema_version`; los cambios de campos son compatibles o MAJOR según
  `MIGRATION.md`.

### Options

#### Option A — Lifecycle completo con 8 estados manuales (draft/validated/approved/executed/verified/superseded/rejected/archived)

Pros: cubre todos los términos observados.

Cons: vuelve a mezclar dimensiones (approved/verified pertenecen a Gate/Verification); exige
escritura manual; reproduce P2.

#### Option B — Lifecycle mínimo derivado (3 estados + 2 propiedades)

Estados: `draft` (producido, sin gate de salida PASS), `validated` (gate de salida PASS registrado),
`superseded` (reemplazado por un artefacto posterior). Propiedades: `archived` (iteración parcial
preservada; propiedad de ubicación) y `rejected` (gate FAIL que requirió corrección; evento, no
estado persistente).

Transiciones:

- `draft → validated`: el runner registra el PASS del gate de salida (mecánico).
- `draft → draft (corregido)`: el escritor re-invocado corrige tras FAIL (evento `corrected`).
- `validated → superseded`: un artefacto posterior (mismo rol, iteración mayor) lo reemplaza.

Actores: el escritor produce; el orquestador juzga gates; runner_state registra; recovery re-invoca.

Pros: elimina la escritura manual de estado; cada transición tiene un productor mecánico o un evento
registrado; resuelve P2/P17.

Cons: requiere retirar/renombrar los campos `status`/`approved` de los contratos (cambio MAJOR).

#### Option C — Sin lifecycle (el artefacto es un snapshot)

Pros: mínimo.

Cons: deja los campos sin significado; no resuelve P2.

### Decision

**Option B.** El Artifact Lifecycle tiene 3 estados derivados (`draft`, `validated`, `superseded`),
2 eventos (`corrected`, `gate_failed`) y 2 propiedades (`archived` en el path de iteración parcial;
`rejected` como evento de corrección). Los campos `status`/`approved`/`validation.complete` de los
contratos se retiran o se redefinen como metadata de solo lectura derivada del registro de gates
(decisión de schema: eliminación compatible de significado → MAJOR, con nota en MIGRATION). El
campo `state` al pie de los artefactos se elimina (duplica Task State, ST-1).

`approved` no es un estado del artefacto: es la decisión del Plan Decision del EXECUTION_PLAN,
registrada como parte del Gate State de H04. `verified` no es un estado del artefacto: es un valor de
la Verification State derivada (D1), válido solo con evidencia (D4/D12).

### Rationale

La evidencia muestra que los campos manuales se escriben mal y no se detectan. Derivar el lifecycle
del registro de gates elimina la clase de error, mantiene un solo lugar de verdad (state.json +
HARNESS) y da a `superseded`/`archived` un propósito real (iteraciones e historia).

### Consequences

- Los artefactos existentes con `status` manual quedan como traza histórica válida bajo la semántica
  vieja (RFC-46: no se reescriben); los nuevos siguen el lifecycle derivado.
- Los checkers pueden verificar: "todo artefacto con gate de salida PASS debe estar `validated`".
- La auto-consistencia interna (P17) pasa a ser un check del validador sobre secciones en conflicto.

### Invariants

- AL-1: el estado del artefacto es derivado; nunca escrito a mano.
- AL-2: `validated` ⇔ el gate de salida tiene PASS en state.json.
- AL-3: un artefacto `superseded` no se consume como entrada de fases posteriores.
- AL-4: secciones en conflicto dentro de un artefacto = FAIL estructural.

### Affected Components

Contratos TASK_ANALYSIS/TASK_SPECIFICATION/CONTEXT_ARTIFACT/CONTEXT_VALIDATION_REPORT/EXECUTION_PLAN/
EXECUTION_SUMMARY/VERIFICATION_REPORT; `gate_validator.py` (check de coherencia);
`check_session_artifacts.py` (presencia).

### RFC Boundary

RFC-B (con D1/D3): lifecycle derivado, retiro de campos manuales, invariantes AL-1…AL-4.
NO incluye: evidencia (D4), autorización (D8).

### Implementation Impact

Cambio de contratos (MAJOR) + actualización del validador estructural + guía de migración para
artefactos históricos.

### Dependencies

D1 (dimensiones).

### Status

DECIDED.

---

## D3 — Completion Semantics

### Question

¿Qué significa COMPLETED, y debe existir como estado global de tarea?

### Why

P9 muestra sesiones que cierran COMPLETED con gates humanos pendientes ("el gate de cierre de Fase 2
no puede declararse formal"). Sin semántica de completitud, el estado terminal no representa las
condiciones que afirma y los hooks/reanudación no pueden operar sobre él.

### Affected Problems

P9; CG-01; INV-08.

### Constraints

- `state.json` ya soporta `status ∈ {no_gates_passed, in_progress, ABORT, COMPLETED}`; el cambio de
  schema es MAJOR y debe mantenerse stdlib-parseable.
- La máquina core define COMPLETED como terminal; no se propone agregar estados a la máquina.
- Los pendientes humanos fueron, en BeaconRBX, excluidos del alcance por el usuario; esa práctica es
  legítima y debe modelarse, no prohibirse.

### Options

#### Option A — COMPLETED = ejecución terminada (sin verificación)

Pros: simple.

Cons: colisiona con el estado actual (COMPLETED ya exige H06/H07).

#### Option B — COMPLETED = completitud absoluta (todos los gates y aprobaciones, incluso humanos)

Pros: semántica fuerte.

Cons: bloquea todos los planes con gates humanos; contradice la práctica confirmada de BeaconRBX.

#### Option C — COMPLETED = completitud relativa al alcance confirmado, con pendientes diferidos explícitos

COMPLETED significa: la máquina core alcanzó terminal Y todos los gates en-scope tienen PASS en
state.json Y el Verification Report no declara criterios en-scope FAIL/PENDING Y toda aprobación
humana en-scope está completada o **diferida con confirmación del usuario**.

Los diferidos se registran en: (a) SESSION_BRIEF (confirmación del usuario: `deferred` + owner +
condición), (b) nueva sección `Deferred Items` del VERIFICATION_REPORT, (c) el plan del proyecto
como `Executed (parcial: <qué falta>)` cuando la gobernanza del proyecto lo defina.

Pros: operacionalizable (el verifier y H06 pueden chequearlo); respeta la práctica real; no cambia
el schema de state.json (status sigue COMPLETED; los diferidos viven en el reporte y el brief).

Cons: requiere que la semántica "relativa al alcance" quede explícita para no ser mal usada.

### Decision

**Option C.** COMPLETED = completitud relativa al alcance confirmado. Definición operacional:

1. El Task State alcanzó COMPLETED por la vía normal (H06 + H07 PASS).
2. Todos los gates en-scope tienen PASS en state.json (INV-05).
3. El Verification Report no declara ningún criterio en-scope como FAIL ni PENDING.
4. Toda aprobación humana en-scope está completada o diferida con confirmación de usuario
   registrada en SESSION_BRIEF (`source: user`, `deferred: true`).

`approved`, `verified`, `validated` y `executed` no son sinónimos de COMPLETED: pertenecen a sus
dimensiones (D1/D2).

### Rationale

BeaconRBX demuestra que la práctica real es cerrar tareas con diferidos confirmados. Option C
convierte esa práctica en semántica explícita y verificable sin agregar estados a la máquina core,
ni cambiar el schema de state.json.

### Consequences

- El Verification Report gana `Deferred Items` (obligatorio cuando hay diferidos; ausente si no).
- H06 agrega el check: "COMPLETED válido solo si no hay criterios en-scope pendientes y los
  diferidos están confirmados".
- La distinción "cierre técnico" vs "cierre de gobernanza" queda explícita (el plan usa
  "Executed (parcial)" cuando corresponda).

### Invariants

- CMP-1: COMPLETED ⇒ todos los gates en-scope PASS en state.json.
- CMP-2: COMPLETED ⇒ ningún criterio en-scope FAIL/PENDING en el reporte.
- CMP-3: todo item diferido tiene confirmación de usuario (SESSION_BRIEF) y aparece en `Deferred
  Items`.
- CMP-4: ningún item diferido se presenta como "completado".

### Affected Components

VERIFICATION_REPORT (contrato), H06 policy (checklist), SESSION_BRIEF (semántica de `deferred`),
orchestrator §Phase 07, state.json (documentación, sin cambio de schema).

### RFC Boundary

RFC-B (con D1/D2): semántica de completitud, `Deferred Items`, invariantes CMP-1…CMP-4.
NO incluye: evidencia (D4), registro (D6).

### Implementation Impact

Contrato del reporte + checklist H06 + guía de cierre; verificable mecánicamente por dev tool.

### Dependencies

D1 (dimensiones).

### Status

DECIDED.

---

## D4 — Evidence Model

### Question

¿Qué puede considerarse evidencia suficiente para justificar una afirmación o un gate, y cómo se
distinguen la atestación del agente de la evidencia verificable externamente?

### Why

P16 muestra un gate PASS sustentado en "escritos sin abrir sources/" (atestación del mismo agente);
P4 muestra claims de budget sin par declared/consumed. Sin clases de evidencia, "esto fue verificado"
equivale a "el agente dijo que lo verificó".

### Affected Problems

P16, P4; CG-03; INV-06/INV-07.

### Constraints

- El modelo de tres capas ya distingue ítems `[gate]` (estructurales) vs `[agent]` (juicio); la
  clasificación de evidencia debe montarse sobre esa distinción, no reemplazarla.
- No diseñar un sistema académico: mínimo operable por agentes y por scripts stdlib.
- Los contratos usan `schema_version`; agregar campos es MINOR si es aditivo.

### Options

#### Option A — Evidencia como texto libre (estado actual)

Pros: cero cambios.

Cons: reproduce P16/P4; no hay forma de distinguir atestación de observación.

#### Option B — Clases mínimas de evidencia + marca de atestación

Definir cinco clases:

- `observation` — lectura directa de un objeto durable (archivo, artefacto, config); re-verificable
  re-leyendo.
- `measurement` — salida de herramienta/comando (tests, linters, type checker) con comando, código de
  salida y referencia a la salida; re-ejecutable best-effort bajo entorno registrado.
- `attestation` — afirmación del agente sobre su propio proceso o estado no re-derivable de objetos
  durables; debe llevar actor + enunciado + marca `attestation`.
- `assertion` — dato/confirmación del usuario (clarificaciones); registrado en SESSION_BRIEF.
- `reference` — cita a artifact/regla con path + hash (opcional) + sección.

Reglas mínimas:

1. Todo ítem `[gate]` de un gate PASS exige `observation` o `measurement` (o `reference` a un
   artifact verificado); una `attestation` no satisface un ítem `[gate]` salvo desviación
   documentada.
2. Todo ítem `[agent]` exige evidencia citada; si la evidencia es `attestation`, debe estar marcada.
3. Un "verificado" en un reporte exige al menos una entrada de evidencia con clase y referencia; sin
   ella, el reporte solo puede decir "atestado".
4. Cada entrada de evidencia tiene `class`, `claim_id` (criterio que sustenta) y `ref`
   (path/comando/id).

Pros: mínimo y operacional; distingue exactamente la confianza que P16 cuestiona; verificable por
agente y por dev tools (formato JSON en TOML o bloque estructurado).

Cons: requiere tocar VERIFICATION_REPORT y los checklist H05/H06/H07 (MAJOR si cambia el significado
de PASS).

#### Option C — Modelo formal completo (ontology de evidencia, confianza por clase, cadenas de
derivación)

Pros: máximo rigor.

Cons: sobre-ingeniería; no es necesario para el objetivo.

### Decision

**Option B.** Se adoptan las cinco clases con las cuatro reglas mínimas. La evidencia se registra en
un bloque estructurado (`[[evidence]]` con `class`, `claim_id`, `ref`, `ts_source`) en
VERIFICATION_REPORT y en los ENTRY de HARNESS_REPORT cuando el checklist lo cite. Una atestación
**puede** justificar ítems `[agent]`, pero **nunca** un ítem `[gate]` sin desviación documentada, y
siempre con la marca.

### Rationale

El problema demostrado es la indistinguibilidad, no la ausencia de evidencia. Option B da la
distinción mínima que permite afirmar "esto fue verificado" con una base re-verificable, mantiene el
modelo documental y es implementable con bloques TOML/JSON ya usados.

### Consequences

- Los reportes de verificación distinguen "verificado por evidencia re-ejecutable" de "atestado".
- H06 puede chequear mecánicamente que cada criterio PASS tenga una entrada de evidencia con clase.
- Los ítems `[agent]` con atestación se vuelven visibles para auditoría (dev tool).

### Invariants

- EV-1: todo gate PASS tiene por cada ítem `[gate]` evidencia `observation`/`measurement`/`reference`
  (o desviación documentada).
- EV-2: toda `attestation` lleva actor + enunciado + marca.
- EV-3: toda entrada de evidencia tiene `class`, `claim_id` y `ref`.
- EV-4: "verificado" en un reporte ⇒ existe entrada de evidencia con clase distinta de
  `attestation` para ese claim (o se usa "atestado").

### Affected Components

VERIFICATION_REPORT (contrato), HARNESS_REPORT (ENTRY), H05/H06/H07 policies, `gate_validator.py`
(H06 evidence check), `audit_gates.py` (detección de atestaciones no marcadas).

### RFC Boundary

RFC-D "Evidence Semantics": clases, reglas mínimas, invariantes EV-1…EV-4, formato estructurado.
NO incluye: modelo de autorización (D8), knowledge (D9).

### Implementation Impact

Contrato + validador + dev tools; sin cambios de runtime obligatorios.

### Dependencies

D0 (qué significa "verificado").

### Status

DECIDED.

---

## D5 — Execution Identity

### Question

¿Cuál es la unidad canónica que representa que algo ocurrió, y qué identificadores son necesarios?

### Why

CG-02 agrupa P3/P15/P18/P11 bajo la ausencia de identidad de eventos y de una fuente canónica. Sin
una unidad de "ocurrencia", los registros no pueden correlacionarse ni reconstruirse.

### Affected Problems

P3, P15, P18; CG-02.

### Constraints

- La sesión ya tiene UUID (`session_id`) y las iteraciones son carpetas numéricas.
- No agregar identificadores sin función semántica.
- El modo declarativo no garantiza reloj ni secuenciador global; la identidad debe funcionar sin
  runtime.

### Options

#### Option A — Solo session_id (estado actual)

Pros: cero cambios.

Cons: no permite correlacionar eventos dentro de una iteración (P3/P15).

#### Option B — Identidad mínima por composición

Definir:

- `session_id` (existente): contenedor canónico.
- `execution_id = (session_id, iteration)` — la iteración es la unidad de ejecución (una petición de
  usuario). Sin UUID nuevo.
- `event key = (execution_id, trigger)` para eventos de gate (correlación HARNESS ↔ state.json).
- `event seq = (execution_id, seq)` para eventos de METRICS (orden monotónico por ejecución).
- `delegation_id = (execution_id, phase, attempt#)` para correlacionar pre/post H15.
- `actor = (role_id, mode)` — la identidad del worker es transitoria; no se persiste instancia.

Pros: cada identificador tiene una función (correlación); no se agregan UUIDs; funciona sin runtime
(los keys son derivables de la estructura de carpetas y nombres).

Cons: requiere que HARNESS/METRICS declaren los keys (cambio de contrato).

#### Option C — UUID por evento (event_id global)

Pros: identidad global única.

Cons: sin función real adicional; exige runtime para generarlos; viola "solo si tiene función".

### Decision

**Option B.** La unidad canónica de "algo ocurrió" es el **evento**, identificado por composición:
`(execution_id, event_type, key)` donde `key` es `trigger` (gates) o `seq` (métricas). No se agregan
UUIDs nuevos. El actor se registra como `(role_id, mode)`; la instancia de worker no se persiste.

### Rationale

Los keys por composición son derivables de la estructura existente (carpeta de sesión + iteración +
trigger), funcionan en modo declarativo y resuelven la correlación que P3/P15 necesitan sin
infraestructura nueva.

### Consequences

- HARNESS ENTRY y state.json comparten el key `(execution_id, trigger)`; METRICS usan `(execution_id,
  seq)`.
- La reanudación puede identificar el "último evento" sin ambigüedad.
- El concepto `kernel` no se modela como entidad; el runtime se describe con metadata
  (`protocol_version`, `mode`), no con identidad.

### Invariants

- EI-1: todo evento registrado tiene un event key derivable.
- EI-2: un gate PASS en state.json y su ENTRY en HARNESS comparten el mismo `(execution_id,
  trigger)`.
- EI-3: los eventos METRICS tienen `seq` monotónico dentro de la ejecución.

### Affected Components

Contratos HARNESS_REPORT/METRICS/SESSION_LOG (campos de key), `runner_state.py` (registro de key),
dev tools de reconciliación.

### RFC Boundary

RFC-C "Execution Identity & Record Model": identidades, event keys, correlación, invariantes
EI-1…EI-3. Incluye D6 y D7.
NO incluye: evidencia (D4), conocimiento (D9).

### Implementation Impact

Campos nuevos en registros + ajuste de runner_state y dev tools; stdlib-only.

### Dependencies

Ninguna (independiente de D0–D4).

### Status

DECIDED.

---

## D6 — Execution Record / Audit Trail

### Question

¿Cómo debe representarse una ejecución después de ocurrida: cuál registro es fuente de verdad, cuáles
son proyecciones/derivados, cómo se correlacionan y cómo se detecta inconsistencia?

### Why

P3 (timestamps), P15 (alcance de state.json), P18 (backfill) y P11 (autocontención) muestran cuatro
registros que divergen sin detección. Se necesita un modelo de registros que permita reconstruir
qué ocurrió, cuándo, bajo qué autoridad y con qué resultado.

### Affected Problems

P3, P15, P18, P11, P1, P10; CG-02; INV-02/INV-03/INV-05/INV-12.

### Constraints

- No se asume Event Sourcing: debe evaluarse junto a alternativas simples.
- Modo declarativo sin Python obligatorio; cualquier mecanismo nuevo es stdlib-only y opcional.
- Los cuatro registros existen y tienen contratos; el cambio debe preservar compatibilidad de
  lectura histórica (RFC-46).

### Options

#### Option A — Event Sourcing (log único de eventos del que se renderizan los cuatro registros)

Pros: fuente única; reconstrucción perfecta.

Cons: exige runtime de escritura/lectura en adoptantes; rompe el modo declarativo; colisiona con la
filosofía documental; sobre-ingeniería para el objetivo.

#### Option B — Registros con roles disjuntos + invariantes de reconciliación

Asignar a cada registro un rol exclusivo:

- `state.json` = fuente de verdad **mecánica** para el estado del protocolo: gates de transición
  (H00–H07, H11) con PASS + status terminal + timestamps UTC. Alcance declarado explícitamente;
  D00/D01/H10/H15/S00 no entran (se registran solo en HARNESS).
- `HARNESS_REPORT.md` = trail de revisión de gates (ENTRY por invocación, con checks, evidencia,
  deviation/recovery, event key).
- `SESSION_LOG.md` = narrativa de decisiones y eventos no-gate (append-only, UTC, event keys).
- `METRICS.md` = observables de proceso (eventos catalogados con `seq`).
- `Artifacts` = objetos durables con lifecycle derivado (D2); las entradas de evidencia referencian
  path + hash.

Correlación: por event key (D5). Detección de inconsistencia: checks dev-only (y opcionalmente un
script stdlib en el payload) que verifican: (1) bidireccionalidad state.json ↔ HARNESS para gates
de transición; (2) igualdad o divergencia declarada de timestamps; (3) presencia de los cuatro
registros y de `protocol_version`; (4) `seq` monotónico en METRICS.

Reconstrucción mínima: session+version, execution, gate records con evidencia, hashes de artefactos
citados, status terminal, diferidos.

Pros: compatible con el diseño actual; no requiere runtime obligatorio; resuelve P3/P15/P18/P10/P1
con invariantes; los checks son implementables en stdlib.

Cons: requiere decidir el alcance de state.json (se decide aquí) y tocar los cuatro contratos.

#### Option C — Mantener todo como está con clases de confianza declaradas

Pros: mínimo.

Cons: deja la divergencia sin detección; no resuelve P3/P15.

### Decision

**Option B.** Roles disjuntos + invariantes de reconciliación. **No Event Sourcing.** Alcance de
state.json: gates de transición core (H00–H07, H11); D*/H10/H15/S00 quedan en HARNESS (coherente
con la práctica observada y con el docstring del tool). La autocontención total del trail (auditar
tras extraer el proyecto) **no es requisito**; se documenta que la auditoría depende del proyecto
(respuesta a la pregunta abierta P11).

### Rationale

La evidencia muestra que los registros ya cumplen roles parcialmente disjuntos; el problema es la
falta de alcance declarado y de reconciliación. Option B cierra ambos sin infraestructura nueva y
respeta el modo declarativo.

### Consequences

- state.json deja de pretender ser "toda" la verdad: es la verdad mecánica de los gates de
  transición.
- Los ENTRY y state.json comparten event keys; las herramientas de reconciliación pasan a ser
  bidireccionales y con comparación de tiempos.
- La reconstrucción post-ejecución es posible para sesiones conformes; 246d4da2 queda como caso de
  no-conformidad (P1).

### Invariants

- TR-1: todo gate de transición PASS existe en state.json y en HARNESS (bidireccional).
- TR-2: los timestamps del mismo gate coinciden o declaran divergencia con causa.
- TR-3: toda sesión tiene los cuatro registros y `protocol_version`.
- TR-4: los eventos METRICS tienen `seq` monotónico.
- TR-5: la reconstrucción de una ejecución usa event keys, no timestamps, como correlación.

### Affected Components

Contratos HARNESS/METRICS/SESSION_LOG/state.json (documentación), `runner_state.py`,
`aggregate_metrics.py --audit` (bidireccional + tiempos), `check_session_artifacts.py` (presencia).

### RFC Boundary

RFC-C (con D5/D7): roles de registros, alcance de state.json, invariantes TR-1…TR-5, tools de
reconciliación.
NO incluye: evidencia (D4), conocimiento (D9).

### Implementation Impact

Documentación + runner_state (registro de event key) + dev tools; stdlib-only.

### Dependencies

D5 (identidad). D7 (temporal) es necesaria para TR-2.

### Status

DECIDED.

---

## D7 — Temporal Semantics

### Question

¿Qué significado tienen los timestamps, cuál es el reloj canónico y qué ordenamiento se necesita?

### Why

P3 demuestra timestamps divergentes entre registros (hora local etiquetada como UTC, tiempos
estimados). Sin semántica temporal, la causalidad y el bypass scan post-H04 son incorrectos.

### Affected Problems

P3; CG-02; INV-04.

### Constraints

- El modo declarativo no garantiza reloj del sistema accesible al agente; debe existir una vía para
  registrar eventos sin reloj.
- No agregar complejidad innecesaria: no se necesita secuenciador global si los event keys (D5)
  correlacionan.

### Options

#### Option A — Timestamps libres (estado actual)

Pros: cero cambios.

Cons: reproduce P3.

#### Option B — UTC canónico + fuente declarada + reconciliación

Reglas:

- Todo timestamp del protocolo es UTC (ISO-8601 con Z).
- Los registros escritos por runtime/runner_state usan el reloj del sistema (canónico).
- Cuando el agente escribe un timestamp sin reloj disponible (modo declarativo), debe marcar
  `source: agent_clock` y el valor es **no canónico**; los tools de reconciliación lo marcan como
  discrepancia cuando difiere del mecánico.
- Semántica: `created_at` (creación de artefacto), `started_at`/`completed_at` (ventana de
  ejecución), `event_ts` (momento de registro), `gate_ts` (momento de PASS en state.json).
- Orden: dentro de una ejecución, los gates se ordenan por `gate_ts` de state.json; la correlación
  cruzada usa event keys, no timestamps.
- No se introduce secuenciador global ni versionado de artefactos general; los artefactos citados
  como evidencia llevan hash (D4), no versión.

Pros: resuelve P3 con reglas declarables y checks mecánicos; sin infraestructura.

Cons: requiere que los agentes declaren la fuente del timestamp (disciplina + check).

#### Option C — Secuenciador global (log ordenado mecánico)

Pros: orden total.

Cons: exige runtime; rompe modo declarativo; innecesario con event keys.

### Decision

**Option B.** UTC canónico, fuente declarada, sin secuenciador global.

### Rationale

P3 muestra dos relojes (mecánico y agente) sin reconciliación. Declarar la fuente y reconciliar por
checks resuelve el problema con el mínimo de cambios y mantiene el modo declarativo.

### Consequences

- Los timestamps escritos por el agente sin reloj quedan marcados y son tratados como no canónicos.
- El bypass scan post-H04 usa `gate_ts` canónico; si es no canónico, el scan se marca como
  no confiable.
- `session.duration_ms` de métricas deja de mezclar relojes (NBI-1).

### Invariants

- TM-1: todo timestamp del protocolo es UTC o lleva `source: agent_clock`.
- TM-2: `gate_ts` de state.json es canónico (runtime).
- TM-3: la correlación de eventos usa event keys, nunca timestamps.

### Affected Components

Contratos (campos de timestamp y fuente), `runner_state.py`, `aggregate_metrics.py`,
`hook_gate.py` (bypass scan), documentación de PROTOCOL_HEALTH (timestamp sanity).

### RFC Boundary

RFC-C (con D5/D6): semántica temporal, invariantes TM-1…TM-3, ajuste del bypass scan.
NO incluye: evidencia (D4).

### Implementation Impact

Documentación + dev tools + runner_state; stdlib-only.

### Dependencies

D5, D6.

### Status

DECIDED.

---

## D8 — Authorization Model

### Question

¿Cuándo una capability está realmente autorizada para producir un efecto, y cómo se distingue de la
capacidad disponible?

### Why

CG-05/P6: en BeaconRBX la autorización del acceso a red es indeterminable (suposición
`user_confirmed=false`, ejecución efectiva). No se asume violación; se asume falta de registro.

### Affected Problems

P6; CG-05; INV-10.

### Constraints

- Las skills "never grant permissions" (SKILLS.md); la autorización es del protocolo/usuario, no del
  skill.
- NO_ASSUMPTIONS y modo desatendido ya existen (defaults + PENDING_USER_CONFIRMATION).
- H01 items 16–17 actuales permiten suposiciones no confirmadas; la decisión ajusta esa interacción.

### Options

#### Option A — Autorización por consentimiento explícito por acción

Pros: máxima seguridad.

Cons: bloquea la ejecución plan-driven y desatendida; contradice la práctica real.

#### Option B — Frontera por defecto + registro de autorización a nivel de plan/spec

Modelo:

- **Capability**: disponibilidad de una herramienta/skill (hecho del runtime).
- **Permission**: regla del protocolo (frontera por defecto + políticas).
- **Authorization**: registro que vincula una capability con un efecto permitido para una ejecución.
- **Execution**: uso efectivo de la capability.
- **Effect**: cambio observable producido.

Frontera por defecto (sin autorización explícita): leer/ejecutar dentro del proyecto y del
protocolo; escribir solo lo planificado. Fuera de frontera (requiere autorización): red/HTTP,
operaciones git remotas, instalaciones, cambios destructivos, escrituras fuera del proyecto.

El TASK_SPECIFICATION gana un bloque `effects`:

```toml
[[effects]]
name = "fetch_remote_sources"
kind = "network"
authorized_by = "user"          # o "unattended_default"
evidence_ref = "SESSION_BRIEF clarification 5A"
status = "authorized"           # o "not_authorized" / "pending_user_confirmation"
```

Reglas:

1. H01/H04 verifican que todo efecto fuera de frontera tenga entrada `effects` con `authorized_by`
   no vacío y status distinto de `not_authorized`.
2. Una suposición no confirmada (`user_confirmed=false`) **no** puede servir como autorización;
   solo la confirmación del usuario o un default declarado en modo desatendido
   (PENDING_USER_CONFIRMATION) autorizan.
3. El worker registra en EXECUTION_SUMMARY los efectos ejecutados con referencia a su entrada
   `effects` (invariante INV-10).
4. La aprobación del plan por el usuario autoriza **los efectos listados y confirmados**, no efectos
   implícitos no declarados.

Pros: implementable; resuelve la determinabilidad; respeta modo desatendido; no asume violación en
BeaconRBX (solo registra que faltaba el registro).

Cons: toca TASK_SPECIFICATION/EXECUTION_PLAN y policies H01/H04 (MAJOR).

#### Option C — Matriz de permisos por skill/rol completa

Pros: control fino.

Cons: sobre-ingeniería; la evidencia no la justifica.

### Decision

**Option B.** Frontera por defecto + bloque `effects` en TASK_SPECIFICATION + verificación en
H01/H04 + registro de ejecución en EXECUTION_SUMMARY. Capability, Permission, Authorization,
Execution y Effect quedan como conceptos separados.

### Rationale

El caso BeaconRBX demuestra indeterminabilidad, no violación. Option B hace determinable la
autorización con un registro declarativo mínimo, sin bloquear la ejecución plan-driven.

### Consequences

- Las suposiciones no confirmadas dejan de poder habilitar efectos fuera de frontera.
- La traza permite responder "¿estaba autorizado?" consultando el bloque `effects` + SESSION_BRIEF.
- El caso de red de BeaconRBX se reinterpreta como "falta el registro", no como "violación".

### Invariants

- AUTH-1: todo efecto fuera de frontera tiene entrada `effects` con `authorized_by` y `status`.
- AUTH-2: `user_confirmed=false` nunca constituye autorización.
- AUTH-3: todo efecto ejecutado se registra en EXECUTION_SUMMARY con referencia a su autorización.

### Affected Components

TASK_SPECIFICATION (contrato), EXECUTION_PLAN (check de efectos), policies H01/H04,
EXECUTION_SUMMARY (contrato), NO_ASSUMPTIONS, PROTOCOL_BOUNDARIES (frontera por defecto).

### RFC Boundary

RFC-E "Authorization Model": conceptos, frontera por defecto, bloque `effects`, invariantes
AUTH-1…AUTH-3.
NO incluye: estado/lifecycle (RFC-B), evidencia (RFC-D) salvo la referencia mínima.

### Implementation Impact

Contratos + policies + guía; verificable por el agente (H01/H04) y auditable post-hoc.

### Dependencies

Ninguna (independiente). Referencia débil a D4 (la entrada `effects` cita evidencia de la
confirmación).

### Status

PROVISIONALLY_DECIDED (el formato del bloque `effects` puede ajustarse en la RFC).

---

## D9 — Knowledge Lifecycle

### Question

¿Qué ciclo mínimo necesita Knowledge (discovery, observación, claim, freshness, invalidación,
revalidación, proveniencia, aprendizaje) para ser reutilizable con confianza?

### Why

CG-04 agrupa P5 (KB stale post-ejecución), P12 (identidad de entradas), P13 (sin aprendizaje) y P14
(costo). Sin transiciones formales, la KB es un snapshot sin ciclo.

### Affected Problems

P5, P12, P13, P14; CG-04; INV-11.

### Constraints

- No diseñar una Knowledge Base completa; solo el lifecycle mínimo.
- El pipeline de discovery y sus TTL/hashes ya existen; la decisión los extiende.
- 3.26.0 ya agrega el cierre "What we learned"; la decisión lo integra, no lo reemplaza.

### Options

#### Option A — Knowledge como snapshot inmutable (estado actual)

Pros: cero cambios.

Cons: reproduce P5/P13.

#### Option B — Lifecycle mínimo con tres tipos y transiciones explícitas

Tipos:

- `snapshot` (entradas de discovery; point-in-time; TTL + hashes).
- `claim` (unidad dentro de una entrada; la frescura aplica por claim, no solo por entrada).
- `lesson` (aprendizaje de sesión con proveniencia; escrito por el cierre "What we learned").

Transiciones:

- Discovery produce/actualiza `snapshot` (pipeline, D00/D01).
- Una ejecución que cambia hechos descubiertos registra `invalidated_facts` en EXECUTION_SUMMARY
  (campo nuevo obligatorio); el pipeline revalida las entradas afectadas (scope por entrada).
- El cierre de sesión produce `lesson` con `session_id`, `protocol_version` y referencia de
  evidencia; una lesson es un tipo de claim.
- Reutilización: un claim es reutilizable si está fresco (TTL por claim) y su proveniencia resuelve
  (source_files/source_sessions existen).
- Identidad: KB_RECOMMENDATION gana `kind` (`discovery|knowledge|lesson`) y `path` (resuelve P12).

Pros: mínimo; resuelve P5/P12/P13; da a la frescura una unidad operable.

Cons: requiere campo `invalidated_facts` y cambio del contrato KB_RECOMMENDATION (MAJOR).

#### Option C — Motor de conocimiento completo (claims, confianza, derivación)

Pros: rigor total.

Cons: sobre-ingeniería; fuera del objetivo.

### Decision

**Option B.** Lifecycle mínimo: `snapshot` / `claim` / `lesson`, invalidación post-ejecución vía
`invalidated_facts`, reutilización por claim fresco con proveniencia, identidad con `kind`+`path`.

### Rationale

P5 demuestra que el disparador de invalidación post-ejecución no existe; P12 demuestra que la
identidad de entradas es ambigua; P13 muestra que la vía de aprendizaje recién existe. Option B
cierra las tres con el mínimo de campos y transiciones.

### Consequences

- El executor declara qué hechos descubiertos cambió; el pipeline revalida solo esas entradas
  (reduce también el costo de P14).
- Las recomendaciones de KB resuelven su ubicación.
- Las lessons son claims con proveniencia, reutilizables bajo las mismas reglas de frescura.

### Invariants

- KN-1: toda entrada de discovery es `snapshot` con TTL y hashes.
- KN-2: toda `lesson` tiene `session_id`, `protocol_version` y referencia de evidencia.
- KN-3: una claim fresca requiere proveniencia resoluble.
- KN-4: toda ejecución que cambia hechos descubiertos declara `invalidated_facts`.

### Affected Components

EXECUTION_SUMMARY (campo `invalidated_facts`), KB_RECOMMENDATION (contrato), KNOWLEDGE_CURATION,
DISCOVERY_STATE_MACHINE (disparadores), orchestrador §Closing Feedback.

### RFC Boundary

RFC-F "Knowledge Lifecycle": tipos, transiciones, invariantes KN-1…KN-4, identidad de entradas.
NO incluye: registro de ejecución (RFC-C) salvo el campo `invalidated_facts`.

### Implementation Impact

Contratos + pipeline de discovery (revalidación scoped) + cierre de sesión; stdlib-only.

### Dependencies

D6 (los eventos de ejecución alimentan `invalidated_facts`).

### Status

PROVISIONALLY_DECIDED.

---

## D10 — Observability / Budget

### Question

¿Cómo se separan budget, measurement, metrics, evidence y audit trail, y qué información se necesita
para demostrar consumo, límites, resultados y cumplimiento?

### Why

P4 muestra claims de budget sin par declared/consumed. Sin separar las capas, todo se convierte en
evidencia o nada se mide.

### Affected Problems

P4; CG-03/CG-02; NBI-1; INV-06.

### Constraints

- El catálogo de métricas y el evento `context_budget` ya existen (3.25.0); el problema es el
  registro, no el concepto.
- Las métricas son advisory ("nothing gates on them"); la decisión no las vuelve bloqueantes.

### Options

#### Option A — Todo como evidencia (estado actual sin registro)

Pros: cero cambios.

Cons: reproduce P4.

#### Option B — Separación en cuatro capas + registro obligatorio de cumplimiento

Capas:

- **Budget**: límite declarado (chars/tokens) por delegación.
- **Measurement**: cantidad derivada (consumed por regla de estimación) calculada del payload real.
- **Metrics**: agregados de observabilidad (advisory).
- **Evidence**: sustenta claims; no toda medición es evidencia.
- **Audit trail**: los cuatro registros.

Regla de cumplimiento: una claim de "budget respetado" exige el evento `context_budget`
(declared/consumed) en METRICS; sin el par, la claim no es falsable y debe marcarse como
atestación. La presencia del evento pasa a ser verificada por dev tool cuando H15 declara
`budget_coherent`.

Pros: resuelve P4 con una regla de registro; separa medición de evidencia; sin runtime nuevo.

Cons: exige disciplina de registro (check dev).

#### Option C — Medición mecánica en runtime (medir el payload al delegar)

Pros: registro garantizado.

Cons: exige runtime en adoptantes; choca con el modo declarativo.

### Decision

**Option B.** Cuatro capas separadas; el evento `context_budget` es la evidencia de cumplimiento de
budget; las métricas siguen siendo advisory. `session.duration_ms` se corrige para usar una sola
fuente temporal (D7).

### Rationale

P4 no requiere un runtime de medición; requiere que la claim tenga un par verificable. Option B
mantiene el modo declarativo y hace falsable la afirmación.

### Consequences

- Las delegaciones con budget registran `context_budget` (declared/consumed).
- Las claims sin par quedan marcadas como atestación (D4).
- Las métricas no se convierten en gates.

### Invariants

- OBS-1: toda delegación con `context_budget` tiene evento `context_budget` en METRICS.
- OBS-2: una claim de cumplimiento de budget sin par declared/consumed es atestación.
- OBS-3: `session.duration_ms` usa una sola fuente temporal.

### Affected Components

METRICS (contrato), H15 policy (verificación), `measure_context_budget.py`, `aggregate_metrics.py`
(NBI-1), BUDGET_MATERIALIZATION (documentación).

### RFC Boundary

RFC-C (con D5/D6/D7): capas de observabilidad, registro obligatorio de `context_budget`,
invariantes OBS-1…OBS-3.
NO incluye: clases de evidencia detalladas (RFC-D) salvo la regla de atestación.

### Implementation Impact

Documentación + dev tools; stdlib-only.

### Dependencies

D4 (clasificación de la claim), D6/D7 (registro y reloj).

### Status

DECIDED.

---

## D11 — Enforcement Boundaries

### Question

Para cada garantía importante, ¿la verifica el agente, el harness, el runtime, una herramienta
externa o un humano?

### Why

D0 define las garantías; D11 las conecta con la capa que las verifica, cerrando RC-01 de forma
operativa: dónde termina el juicio y dónde empieza el enforcement.

### Affected Problems

P1, P3, P4, P10, P15, P16, P18; RC-01.

### Constraints

- Modo declarativo = sin runtime obligatorio; las celdas "Runtime" son opcionales.
- Hooks son fail-open por contrato.
- Los checkers de desarrollo son dev-only (no se distribuyen).

### Options

#### Option A — Matriz sin cambios (todo juzgado por el agente)

Pros: cero cambios.

Cons: reproduce los problemas.

#### Option B — Matriz explícita de verificación por garantía

Adoptar la matriz siguiente como decisión:

| Property | Agent | Harness (gates) | Runtime (scripts/hooks) | External (dev tools/CI) | Human |
|---|---|---|---|---|---|
| Identidad/versión de sesión | declara | — | registra | verifica | — |
| Presencia de registros raíz | produce | chequea (item [gate]) | — | verifica | — |
| Registro de gates (PASS/FAIL/SKIP) | juzga | — | registra en state.json | reconcilia (bidireccional) | — |
| Estructura de artefactos (secciones, EARS, ENTRY) | produce | evalúa con gate_validator | — | verifica post-hoc | — |
| Evidencia con clase y asociación | cita | evalúa (H05/H06) | — | detecta atestaciones sin marca | — |
| Timestamps canónicos | marca fuente | — | escribe UTC (runner_state) | compara | — |
| Autorización de efectos | declara (effects) | verifica (H01/H04) | — | audita | confirma/deniega |
| Budget (declared/consumed) | declara | — | mide (opcional) | verifica presencia | — |
| Reproducibilidad de ítems `[gate]` | — | — | — | re-ejecuta (audit_gates) | — |
| Independencia de verificación | — | — | — | — | solo multi-agent; en single-instance se declara atestación |
| Aprobaciones humanas | — | — | — | — | decide |
| Discovery consent | consulta | — | — | — | decide (3.26.0) |

Reglas de la frontera:

1. Lo mecánicamente comprobable (presencia, versión, estructura, timestamps, bidireccionalidad) se
   verifica por Runtime/External cuando existe; en modo declarativo, el agente lo declara y el dev
   tool lo verifica post-hoc.
2. Lo semántico (evidencia suficiente, autorización, completitud) es juicio del agente con checks
   estructurales de apoyo.
3. Toda celda vacía significa "no aplica", no "sin control".

Pros: convierte RC-01 en una frontera operable; cada garantía tiene dueño de verificación.

Cons: requiere mantener la matriz en el payload (documentación) y alinear los checkers.

#### Option C — Mover todo lo posible a Runtime

Pros: máximo enforcement.

Cons: rompe modo declarativo.

### Decision

**Option B.** Se adopta la matriz como frontera operativa. El juicio del agente permanece donde la
celda dice Agent/Harness; el enforcement mecánico queda limitado a Runtime/External y es opcional en
modo declarativo.

### Rationale

La matriz responde la pregunta de RC-01 con una conclusión operativa: el modelo documental es válido
para lo semántico; el enforcement mecánico se limita a un subconjunto finito y declarado. No se
debate más.

### Consequences

- Los checkers dev implementan las celdas External.
- El payload documenta la matriz (sección de enforcement).
- Las claims de garantía citan su capa de verificación.

### Invariants

- ENF-1: ninguna garantía etiquetada "mecánica" depende de juicio del agente.
- ENF-2: en modo declarativo, toda garantía verificable se declara y se verifica post-hoc por dev
  tool o se marca atestación.
- ENF-3: los hooks siguen fail-open; la matriz no los declara como control absoluto.

### Affected Components

`harness/INDEX.md` (sección de matriz), policies, `check_session_artifacts.py`, `aggregate_metrics.py`,
`audit_gates.py`, documentación de adopción.

### RFC Boundary

RFC-A (con D0): matriz de enforcement, invariantes ENF-1…ENF-3, frontera del juicio.
NO incluye: evidencia (D4), autorización (D8).

### Implementation Impact

Documentación + dev tools; sin runtime obligatorio.

### Dependencies

D0, D4, D6.

### Status

DECIDED.

---

## D12 — Artifact / State / Evidence Relationship

### Question

¿Puede un artifact decir "verified" sin evidencia asociada? ¿Cuáles son las relaciones mínimas entre
Artifact, State, Evidence, Verification y Gate?

### Why

P16/P17 muestran artefactos que declaran estados sin sustento y con secciones en conflicto. La
relación entre artefacto y evidencia debe ser un invariante, no una convención.

### Affected Problems

P16, P17; CG-01/CG-03; INV-06/INV-07/INV-09.

### Constraints

- La dimensión de evidencia (D4) ya define clases; esta decisión define la relación, no las clases.
- El lifecycle derivado (D2) ya define cómo un artefacto llega a `validated`.

### Options

#### Option A — El artefacto puede declarar cualquier estado (estado actual)

Pros: cero cambios.

Cons: reproduce P16/P17.

#### Option B — Relaciones mínimas con invariantes

Relaciones:

- **Artifact → Gate**: el gate de salida del artefacto es su transición a `validated` (D2).
- **Gate → Evidence**: cada ítem del checklist cita entradas de evidencia con clase (D4).
- **Artifact → Evidence**: un artefacto puede declarar "verified"/"validated" solo si existe el
  Gate State PASS y las entradas de evidencia asociadas; en caso contrario solo puede declarar
  "draft" o "atestado".
- **Verification → Artifact**: el VERIFICATION_REPORT evalúa artefactos; cada criterio PASS referencia
  el artefacto y su evidencia.
- **State → Evidence**: ninguna transición de estado a `validated`/terminal se registra sin el
  registro del gate (state.json) correspondiente.

Regla central: **un artifact no puede decir "verified" sin evidencia asociada**. Si no hay
evidencia, el término permitido es "atestado" (D4).

Pros: invariante directo y chequeable; cierra P16/P17.

Cons: requiere que los reportes distingan "verificado" de "atestado" (cambio de lenguaje).

#### Option C — Modelo de derivación formal completo

Pros: rigor total.

Cons: sobre-ingeniería.

### Decision

**Option B.** Regla central adoptada: *un artifact puede declarar "verified" solo con Gate State PASS
y evidencia asociada con clase; sin ella, el término permitido es "atestado"*.

### Rationale

Es la consecuencia directa de D2 + D4: el lifecycle es derivado del gate y el gate exige evidencia.
La relación se convierte en invariante chequeable por el validador y los dev tools.

### Consequences

- Los reportes existentes que usan "verificado" sin evidencia quedan como traza histórica; los
  nuevos deben ajustarse.
- El validador H06/H07 agrega el check de relación.
- La auto-consistencia de secciones (AL-4) se aplica junto con esta relación.

### Invariants

- REL-1: un artefacto declara "verified" ⇔ Gate State PASS + evidencia con clase distinta de
  `attestation` para el claim (o usa "atestado").
- REL-2: `validated` del lifecycle ⇔ PASS del gate de salida en state.json.
- REL-3: toda entrada de evidencia referencia el artifact y el claim que sustenta.

### Affected Components

VERIFICATION_REPORT (lenguaje), H06/H07 policies, `gate_validator.py`, contratos de artefactos.

### RFC Boundary

RFC-B (relaciones e invariantes REL-1…REL-3) con dependencia formal de RFC-D (clases).
NO incluye: el diseño de las clases en sí (RFC-D).

### Implementation Impact

Contratos + validador + guía de lenguaje en reportes.

### Dependencies

D1, D2, D4.

### Status

DECIDED.

---

## D13 — Implementation Priority

### Question

¿En qué orden mínimo deben implementarse las decisiones para comenzar a modificar ARgentOS?

### Why

Sin un orden por dependencias directas, la implementación acumularía parches sobre un modelo aún
indefinido.

### Affected Problems

Todos (meta).

### Constraints

- El orden es por dependencias, no por severidad.
- La primera RFC debe habilitar la mayor cantidad de checks mecánicos con el menor cambio conceptual.

### Options

#### Option A — Orden por severidad (P8/P3 primero)

Pros: ataca lo más visible.

Cons: sin semántica de estado/evidencia previa, cristaliza modelos indefinidos.

#### Option B — Orden por dependencias

Cadena adoptada:

```text
D1 (state) → D2 (lifecycle) → D3 (completion)
D0 (guarantees) → D4 (evidence) → D12 (relación)
D5 (identity) → D6 (record) → D7 (temporal)
D11 (enforcement) depende de D0 + D4 + D6
D8 (authorization) independiente
D9 (knowledge) depende de D6
D10 (observability) depende de D4 + D6
```

Primera RFC: **RFC-B (State & Artifact Lifecycle)** formalizando D1+D2+D3, porque habilita los
checks mecánicos de coherencia de estado (P2/P17), la existencia de REVIEW_REPORT (P8) y la
semántica de COMPLETED (P9) sin depender de los modelos de evidencia/registro más pesados.

Pros: cada RFC se apoya en decisiones ya tomadas; sin ciclos.

Cons: requiere documentar D0/D4 en paralelo para no bloquear D11/D12.

#### Option C — Todo en una RFC

Pros: un solo cambio.

Cons: inmanejable; MAJOR gigante.

### Decision

**Option B.** Orden de implementación:

1. RFC-B (D1+D2+D3) — primera.
2. RFC-A (D0+D11) — en paralelo o inmediatamente después (define el lenguaje de garantías que
   RFC-D necesita).
3. RFC-D (D4) — evidencia.
4. RFC-C (D5+D6+D7+D10) — registro e identidad.
5. RFC-E (D8) — autorización (puede adelantarse; independiente).
6. RFC-F (D9) — knowledge (última; depende de D6).

### Rationale

RFC-B es la única que desbloquea checks mecánicos inmediatos (coherencia de estado, REVIEW_REPORT,
completitud) con cambio mayormente documental; las demás dependen de sus conceptos.

### Consequences

- El orden de redacción de RFCs queda fijado por dependencias, no por severidad.
- RFC-B puede redactarse sin esperar a D4/D6.

### Invariants

- PR-1: ninguna RFC se redacta antes que las decisiones de las que depende.
- PR-2: la implementación de un check mecánico espera a la RFC que define su semántica.

### Affected Components

Plan de trabajo de RFCs (meta).

### RFC Boundary

No aplica (decisión de secuencia).

### Implementation Impact

Define el orden de redacción e implementación.

### Dependencies

Todas las anteriores.

### Status

DECIDED.

---

## Decision Summary

| ID | Decision | Status | Depends On | RFC Candidate |
|---|---|---|---|---|
| D0 | Guarantee Model (híbrido con catálogo clasificado) | DECIDED | — | RFC-A |
| D1 | State Semantics (3 dimensiones + 4 derivadas) | DECIDED | D0 (informativa) | RFC-B |
| D2 | Artifact Lifecycle derivado (3 estados + eventos) | DECIDED | D1 | RFC-B |
| D3 | Completion Semantics relativa al alcance + diferidos | DECIDED | D1 | RFC-B |
| D4 | Evidence Model (5 clases, atestación marcada) | DECIDED | D0 | RFC-D |
| D5 | Execution Identity (composición; sin UUID nuevos) | DECIDED | — | RFC-C |
| D6 | Execution Record (roles disjuntos + reconciliación; sin Event Sourcing) | DECIDED | D5, D7 | RFC-C |
| D7 | Temporal Semantics (UTC canónico + fuente declarada) | DECIDED | D5, D6 | RFC-C |
| D8 | Authorization Model (frontera + bloque `effects`) | PROVISIONALLY_DECIDED | — | RFC-E |
| D9 | Knowledge Lifecycle (snapshot/claim/lesson) | PROVISIONALLY_DECIDED | D6 | RFC-F |
| D10 | Observability/Budget (4 capas + evento obligatorio) | DECIDED | D4, D6, D7 | RFC-C |
| D11 | Enforcement Boundaries (matriz por garantía) | DECIDED | D0, D4, D6 | RFC-A |
| D12 | Artifact/State/Evidence Relationship ("verified" ⇒ evidencia) | DECIDED | D1, D2, D4 | RFC-B (depende de RFC-D) |
| D13 | Implementation Priority (RFC-B primero) | DECIDED | todas | — |

---

## Implementation Entry Point

1. **Qué RFC debería escribirse primero:** **RFC-B — "State & Artifact Lifecycle Semantics"**,
   formalizando las decisiones **D1 + D2 + D3** (dimensiones de estado, lifecycle derivado de
   artefactos, completitud relativa al alcance con diferidos).

2. **Qué decisión debe formalizar:** D1 (tres dimensiones con entidad: Task State, Gate State,
   Artifact Lifecycle; cuatro derivadas), D2 (lifecycle derivado: `draft`/`validated`/`superseded`;
   retiro de los campos manuales `status`/`approved`/`validation.complete`), D3 (COMPLETED =
   completitud relativa al alcance; `Deferred Items` con confirmación de usuario).

3. **Qué parte del código/documentación probablemente será afectada:**
   - `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` (tabla de perfiles;
     redefinición del "review gate" como Gate State sobre REVIEW_REPORT).
   - Contratos de artefactos (`TASK_SPECIFICATION`, `EXECUTION_PLAN`, `VERIFICATION_REPORT`, etc.):
     eliminación/derivación de campos de estado.
   - `protocol/.agents/orchestrators/core/harness/policies/H06-verification-report.md` y
     `H07-scope-compliance.md` (checks de completitud y evidencia).
   - `protocol/.agents/harness/gate_validator.py` (checks: existencia de REVIEW_REPORT para
     complex, coherencia de dimensiones, secciones en conflicto).
   - `tools/check_session_artifacts.py` (presencia de registros y `protocol_version`).
   - Documentación: `docs/MIGRATION.md` (nota MAJOR), CHANGELOG.

4. **Qué decisión NO necesitamos resolver todavía para empezar:** el modelo completo de evidencia
   (D4), el registro de ejecución e identidad (D5/D6/D7), la autorización (D8) y el knowledge
   lifecycle (D9). RFC-B puede redactarse e implementarse sin ellos; solo la parte REL-1 de D12
   (que depende de D4) se difiere a RFC-D.

**La próxima acción es:** redactar RFC-B con las decisiones D1+D2+D3, anclar cada sección a los
problemas P2/P8/P9/P17, declarar las invariantes ST-1…ST-4, AL-1…AL-4 y CMP-1…CMP-4, y marcar la
clase de cambio (MAJOR) con nota de migración para los artefactos históricos de BeaconRBX. A
continuación, en paralelo: RFC-A (D0+D11) para fijar el lenguaje de garantías que RFC-D consumirá.
