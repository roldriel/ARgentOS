# Política de migración — Protocolo ARgentOS

Cómo migrar un proyecto que adoptó el protocolo ARgentOS (`.agents/` + `AGENTS.md`)
de una versión a otra. Este archivo vive **fuera de `.agents/`** a propósito
(origen: `docs/plans/20-release-adoption.md` §A): una migración no debe modificar su
propia política.

La versión vigente está declarada en `.agents/VERSION` (una línea semver). El
historial de cambios está en [`CHANGELOG.md`](../CHANGELOG.md). La guía de
adopción inicial está en [`ADOPTION.md`](ADOPTION.md).

---

## 1. Esquema de versión

Semver conceptual (`docs/plans/20-release-adoption.md` §A):

| Componente | Cuándo sube | Ejemplo |
|---|---|---|
| **MAJOR** | Cambios del modelo conceptual o contratos incompatibles: un contrato de artefacto cambia campos obligatorios, una fase del workflow se renombra o elimina, una policy cambia su criterio de PASS de forma incompatible. | Un `TASK_SPECIFICATION.md` válido en 1.x deja de serlo en 2.0. |
| **MINOR** | Adiciones compatibles: policies nuevas, contratos nuevos que no rompen los existentes, skills nuevas, secciones opcionales. | Aparece una nueva policy H21; los artefactos 1.x siguen siendo válidos. |
| **PATCH** | Fixes documentales: redacción, ejemplos, enlaces, typos; sin cambio de comportamiento. | Se corrige un ejemplo en un contrato. |

## 2. Procedimiento de migración

Para pasar un proyecto adoptante de la versión `X` a la versión `Y`:

1. **Leer el changelog** entre `X` e `Y` en `CHANGELOG.md`. Cada ítem referencia
   la policy, plan o RFC que lo originó; esas son las fuentes de detalle.
2. **Revisar contratos modificados** (`.agents/contracts/`,
   `.agents/orchestrators/*/contracts/`): para cada contrato listado en el
   changelog, comparar campos obligatorios (front matter `artifact`, `phase`,
   `produced_by`, `schema_version`) y secciones requeridas contra los
   artefactos que el proyecto ya produce. `schema_version` es semver: un salto
   **MAJOR** (campos obligatorios incompatibles) exige actualizar las
   plantillas o los artefactos vivos del proyecto; **MINOR** (adiciones
   compatibles) y **PATCH** (fixes documentales) no rompen los artefactos
   válidos existentes.
3. **Revisar artifacts renombrados o eliminados**: todo rename/removal aparece en
   la sección **Removed** del changelog. Actualizar referencias en roles, workflow
   y artefactos propios del proyecto.
4. **Adoptar policies nuevas**: revisar `.agents/harness/policies/` y
   `.agents/orchestrators/*/harness/policies/`. Las policies nuevas (MINOR)
   empiezan a validar en cuanto se copian; verificar que los artefactos del
   proyecto las cumplen antes de habilitar el trigger correspondiente.
5. **Revisar flags**: comparar `.agents/features.toml` contra la versión nueva;
   los flags nuevos llegan con default seguro (deshabilitado salvo indicación del
   changelog).
6. **Sincronizar el directorio**: reemplazar `.agents/` y `AGENTS.md` por los de
   la versión `Y`. `.agents/` es autocontenido: no referencia `docs/plans/` ni RFCs, así
   que no hace falta copiar nada más del repo de origen.
7. **Validar**: la checklist documental de
   `.agents/standards/runtime/PROTOCOL_HEALTH.md` (la aplica el system agent en
   el bootstrap) debe terminar en `PASS`. Si el proyecto opera en modo
   enforced, ejecutar además la sonda de almacenamiento de estado
   (`python .agents/harness/health_check.py` → PASS). La suite de tests
   (`python -m pytest .agents/harness/tests/`) es solo para desarrollo del
   protocolo, no un requisito del adoptante.
8. **Actualizar la versión adoptada**: registrar en el proyecto qué versión de
   `.agents/VERSION` quedó adoptada.

## 3. Cambios de modelo y contratos — planes 28-30 (2026-08-11)

Implementación autorizada explícitamente por el usuario (RFC-29…31 `Accepted`,
planes 28–30 `Executed`). Puntos que un adoptante debe revisar al adoptar esta
versión:

- **`VERIFICATION_REPORT.md` — Scope Compliance con dos ramas**: los reportes
  existentes que cumplen la Rama A (sin extra, `unplanned_changes = []`,
  `user_authorized_extra_work = false`) siguen siendo válidos. La Rama B
  (`user_authorized_extra_work = true` con cambios fuera del plan) solo pasa H07
  con autorización escrita del usuario citada en el reporte (`SESSION_LOG.md` o
  artefacto de sesión). `scope_respected = false` es fallo en ambas ramas.
- **`RECOVERY_REPORT.md` — `ABORT` en la recomendación**: el enum de
  `corrective_action.recommended_next_state` ahora admite `ABORT`, válido solo
  como abort fundado (causa registrada en `SESSION_LOG.md`, per `DECISIONS.md`
  D5).
- **Máquina de estados — aristas de recovery a fases tempranas**:
  `RECOVERY → ANALYZING_TASK | BUILDING_TASK_SPECIFICATION | GATHERING_CONTEXT |
  VALIDATING_CONTEXT` son transiciones legales para corregir artefactos de fases
  tempranas; `RETRY_WORKER` sobre la fase actual es una acción correctiva sin
  transición de estado. H01 incorpora una rama de retry acotado
  (`retry_count == 0`) para fallos de formato.
- **Modo enforced — cierre terminal**: `runner_state.py` registra estados
  terminales (`python .agents/harness/runner_state.py --session <uuid> --state
  ABORT|COMPLETED terminal`); el hook deja cerrar la sesión por `Stop` cuando
  `state.json.status` es `ABORT`/`COMPLETED`, además de las condiciones
  anteriores (H06 PASS o `NEEDS_CLARIFICATION` registrado).

Este cambio se publica como versión `3.0.0` (2026-08-11); esta sección es la
guía de migración del cambio.

## 3.1 Cambios de forma y nomenclatura — planes 31-33 (2026-08-11)

Release 3.0.1 (PATCH): correcciones documentales sin cambios de modelo.

- **`TASK_SPECIFICATION.md` — criterios de aceptación**: la forma canónica de
  `## Acceptance Criteria` son los bullets Markdown EARS. Las specs históricas
  con criterios solo en el bloque TOML `acceptance_criteria` deben migrar los
  criterios a bullets; el bloque TOML queda como representación opcional y
  derivada (no reemplaza los bullets).
- **`EXECUTION_SUMMARY.md` — lista de pasos**: el nombre canónico de la lista es
  `[[steps_executed]]`. Los resúmenes históricos con `[[steps]]` son no
  conformes y deben migrar la clave a `[[steps_executed]]`.
- **Fase 02 — rol**: la tabla de activación y la guía de orquestación usan el
  rol de fase `task_specification_writer`; `functional_writer` queda limitado a
  la documentación funcional de la fase 06.

Este cambio se publica como versión `3.0.1` (2026-08-11); esta sección es la
guía de migración del cambio.

## 3.2 Namespacing de artefactos de discovery — plan 40 (2026-08-12)

Desde `3.3.0`, los artefactos de sesión del dominio discovery usan prefijo
`D<order>-` (p. ej. `D01-KB_DISCOVERY_REPORT.md`) y los intermedios de workers
viven en `.project/<session-uuid>/discovery/` sin `<order>`. No requiere
acción en proyectos adoptantes: las iteraciones previas quedan como traza
histórica (no se renombran); la regla aplica a ejecuciones futuras.

## 4. Qué NO migra

- **Artefactos de sesión** (`.project/`): son efímeros y específicos del proyecto;
  no se migran ni se versionan con el protocolo.
- **Knowledge base** (`.project/knowledge/`): se conserva; si un contrato de KB
  cambió (sección del changelog), regenerar o re-curar las entradas afectadas.
- **Skills propias del proyecto** (`.project/skills/` o las del usuario): se
  conservan; revalidarlas contra el estándar de skills si la sección
  correspondiente del changelog indica cambios estructurales.

## 5. Soporte de versiones

Se soporta una sola línea de versión: la vigente. No hay ramas de mantenimiento
de versiones anteriores (fuera de alcance declarado en
`docs/plans/20-release-adoption.md` §Fuera de alcance).

## 6. Modelo de garantías y fronteras de enforcement — 4.0.0 (plan 76, RFC-62)

Cambio **MAJOR** del modelo conceptual: cambia el significado declarado de
"verificado" y agrega obligaciones de registro.

- **Nueva semántica de "verificado".** Un claim puede llamarse "verificado"
  solo cuando cita evidencia de clase distinta de atestación. Sin evidencia
  citable, el término permitido es "atestado". El detalle de las clases de
  evidencia se define en el modelo de evidencia posterior.
- **Obligaciones nuevas.** Todo claim emitido por el protocolo es
  evidencia-citado o está marcado explícitamente como atestación/inferencia
  (regla de claims). Los gate checks de `HARNESS_REPORT.md` y los criterios y
  resultados de `VERIFICATION_REPORT.md` distinguen `verified` de
  `attested`/`inference`; los timestamps mecánicos usan reloj UTC y los
  agentes sin reloj confiable marcan `clock: agent_clock`; `SESSION_LOG.md`
  puede citar `Evidence` por decisión.
- **Campos nuevos opcionales.** `claim_class` (HARNESS_REPORT y
  VERIFICATION_REPORT), `clock` (HARNESS_REPORT y METRICS) y `Evidence`
  (SESSION_LOG) son adiciones compatibles: los artefactos válidos previos
  siguen siendo válidos (schema 1.1.0).
- **Trazas históricas.** Las sesiones previas a 4.0.0 son registros inmutables
  bajo la semántica vieja (RFC-46): no se reescriben ni se re-reportan. Los
  checkers de desarrollo no las reportan.
- **Adopción.** Leer `.agents/harness/INDEX.md`, secciones "Guarantee
  catalog" y "Enforcement boundaries", para la matriz completa por capa y el
  comportamiento en modo declarativo vs. enforced. No se requiere ninguna
  acción de migración sobre artefactos existentes; los reportes nuevos deben
  cumplir la regla de claims.

## 7. Modelo de estado y lifecycle de artefactos — 5.0.0 (plan 77, RFC-63)

Cambio **MAJOR** del modelo conceptual: separa el estado en dimensiones y
convierte el lifecycle de los artefactos en un estado derivado.

- **Campos manuales retirados.** Los contratos de TASK_ANALYSIS,
  TASK_SPECIFICATION, CONTEXT_ARTIFACT, CONTEXT_VALIDATION_REPORT,
  EXECUTION_PLAN, EXECUTION_SUMMARY y VERIFICATION_REPORT dejan de declarar
  `status` (Metadata), `state` (sección `## State`), `validation.complete` y
  `approved` (Plan Decision). El lifecycle del artefacto (`draft` /
  `validated` / `superseded`) se deriva del registro de gates y nunca se
  escribe a mano. `schema_version` de los siete contratos pasa a 2.0.0.
- **Semántica de COMPLETED.** `COMPLETED` significa completitud relativa al
  alcance confirmado: H06/H07 PASS, gates en-scope con PASS, sin criterios
  FAIL/PENDING y aprobaciones humanas completadas o diferidas con confirmación.
- **Aprobaciones diferidas.** `VERIFICATION_REPORT.md` gana la sección
  `## Deferred Items` y `SESSION_BRIEF.md` registra las aprobaciones diferidas
  con `deferred: true` y confirmación del usuario.
- **Review gate.** Para tareas `complex` con `rubrics` habilitado, la revisión
  de `REVIEW_REPORT.md` es un Gate State sobre el artefacto
  (`review_required` → `review_passed` | `review_failed`) registrado en
  `HARNESS_REPORT.md`; no es un estado de tarea ni un gate de transición.
- **Trazas históricas.** Las sesiones previas a 5.0.0 son registros inmutables
  bajo la semántica vieja (RFC-46): los checkers de desarrollo no las reportan.
- **Adopción.** Leer `.agents/harness/INDEX.md`, sección "State dimensions",
  para el modelo completo de dimensiones e invariantes. Los artefactos
  existentes no requieren acción: los reportes nuevos no declaran campos de
  estado manuales e incluyen `Deferred Items` (vacío si no hay diferidos).

## 8. Modelo de evidencia y verificación — 7.0.0 (plan 79, RFC-65)

Cambio **MAJOR** del modelo conceptual: define qué cuenta como evidencia y
cuándo un claim puede declararse VERIFIED.

- **Cinco clases de evidencia.** `observation`, `measurement`, `attestation`,
  `assertion` y `reference` (`.agents/standards/quality/EVIDENCE.md`). Toda
  entrada de evidencia lleva `class`, `claim_id` y `ref`; una atestación lleva
  además `actor` y `statement`.
- **Bloques `[[evidence]]`.** `VERIFICATION_REPORT.md` gana la sección
  `## Evidence` y sus criterios/resultados declaran `claim_id` (schema
  `3.0.0`); los ENTRY de `HARNESS_REPORT.md` pueden registrar el array
  `evidence` con clase por check.
- **"Verificado" exige evidencia no-atestación.** Un claim se declara
  `verified` solo con una entrada de evidencia de clase distinta de
  `attestation`; sin ella el término es `attested` (o `inference` declarado
  explícitamente). Un ítem `[gate]` se satisface con
  observación/medición/referencia, o con desviación documentada; la atestación
  nunca lo satisface sola.
- **Detección de atestaciones sin marca.** `gate_validator.py` (H06) rechaza un
  criterio PASS sin evidencia con clase válida; `audit_gates.py` (dev) marca
  atestaciones sin etiquetar en los PASS registrados.
- **Trazas históricas.** Las sesiones previas a 7.0.0 son registros inmutables
  bajo la semántica previa (RFC-46): no se reescriben ni se re-reportan.
- **Adopción.** Los reportes nuevos de `VERIFICATION_REPORT.md` incluyen
  `## Evidence` y `claim_id`; los checks de `HARNESS_REPORT.md` citan evidencia
  con clase o declaran `claim_class`. Los reportes 6.0.0 que declaraban
  "verificado" con evidencia solo en texto libre dejan de ser conformes.

## 9. Modelo de autorización y capacidades — 8.0.0 (plan 80, RFC-66)

Cambio **MAJOR** del modelo conceptual: distingue capability de autorización y
hace verificable la frontera de efectos externos.

- **Vocabulario.** Capability (disponibilidad de herramienta/skill),
  Permission (regla del protocolo), Authorization (registro que vincula una
  capability con un efecto permitido para una ejecución), Execution (uso
  efectivo) y Effect (cambio observable). La capability nunca es autorización.
- **Frontera por defecto.** Lectura/ejecución dentro del proyecto y del
  protocolo y escritura planificada no requieren autorización explícita;
  red/HTTP, operaciones git remotas, instalaciones, cambios destructivos y
  escrituras fuera del proyecto sí (`AUTHORIZATION.md`).
- **Bloque `effects`.** `TASK_SPECIFICATION.md` gana la sección `## Effects`
  (schema `3.0.0`) con `name`/`kind`/`authorized_by`/`evidence_ref`/`status`,
  obligatoria cuando hay efectos fuera de frontera; `EXECUTION_SUMMARY.md` gana
  `## Effects Executed` (schema `3.0.0`) con `effect`/`executed`/
  `authorization_ref`; `SESSION_BRIEF.md` registra `[[effects]]` cuando la
  autorización proviene de una clarificación o de un default desatendido.
- **Quién autoriza.** Solo el usuario (clarificación/confirmación de plan) o un
  default declarado en modo desatendido con `status:
  pending_user_confirmation`; `user_confirmed: false` nunca constituye
  autorización.
- **Estados.** AUTHORIZED / UNAUTHORIZED (denegación registrada) /
  AUTHORIZATION_UNDETERMINED (sin registro suficiente); nunca se infiere
  UNAUTHORIZED por ausencia de registro.
- **Policies.** H01/H04 exigen autorización registrada para efectos fuera de
  frontera; H05 verifica el registro de efectos ejecutados. El validador
  estructural valida la forma del bloque (H01) y rechaza autorizaciones propias
  del plan (H04).
- **Trazas históricas.** Las sesiones previas a 8.0.0 son registros inmutables
  bajo la semántica previa (RFC-46): no se reescriben ni se re-reportan. El
  caso BeaconRBX se clasifica por semántica como AUTHORIZATION_UNDETERMINED,
  sin re-juzgar la sesión.
- **Adopción.** Las task specifications nuevas con efectos fuera de frontera
  incluyen `## Effects`; los execution summaries registran
  `## Effects Executed`; los planes no declaran autorizaciones propias.

## 10. Modelo de lifecycle de conocimiento — 9.0.0 (plan 81, RFC-67)

Cambio **MAJOR** del modelo conceptual: define el ciclo mínimo del
conocimiento (tipos, frescura por claim, invalidación post-ejecución y
revalidación scoped).

- **Tipos de conocimiento.** `snapshot` (entrada de discovery point-in-time con
  TTL y hashes, `kind: snapshot` en `KB_DISCOVERY_ENTRY.md`, schema `2.0.0`),
  `claim` (unidad dentro de una entrada; objeto de frescura e invalidación) y
  `lesson` (claim de aprendizaje de sesión con `session_id`,
  `protocol_version` y evidencia RFC-65). El modelo vive en
  `.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`.
- **Frescura por claim.** Una claim es reutilizable si está fresca (TTL por
  claim; por defecto hereda el de su entrada) y su proveniencia resuelve
  (`source_files`/`source_sessions` existen). Una claim vencida o sin
  proveniencia no se recomienda ni se consume.
- **Invalidación post-ejecución.** `EXECUTION_SUMMARY.md` gana la sección
  `## Invalidated Facts` (schema `4.0.0`, `fact`/`entry`/`reason`), obligatoria
  cuando la ejecución cambió hechos descubiertos; el pipeline de discovery
  revalida las entradas afectadas con el scope que las posee (condición de
  invocación nueva del state machine), nunca un rediscovery full por defecto.
- **Recomendaciones.** `KB_RECOMMENDATION.md` (schema `2.0.0`) resuelve la
  ubicación de cada entrada con `kind` + `path`; `session_uuid` queda como
  proveniencia, no como ubicación (P12).
- **Lessons del cierre.** El Closing Feedback persiste lessons con
  `kind: lesson`, `session_id`, `protocol_version` y evidencia; sin
  proveniencia no se registran.
- **TTL.** Cambiar un TTL exige medición previa del costo de rediscovery
  (D-201); sin medición se mantienen los valores vigentes.
- **Trazas históricas.** Las sesiones previas a 9.0.0 son registros inmutables
  bajo la semántica previa (RFC-46): no se reescriben ni se re-reportan; las
  lessons previas sin `kind` no se reclasifican.
- **Adopción.** Los discovery entries nuevos declaran `kind: snapshot`; los
  execution summaries que cambian hechos descubiertos declaran
  `invalidated_facts`; las recomendaciones nuevas llevan `kind`/`path`; los
  reportes previos siguen siendo válidos como traza.

## 11. Architecture Evolution Workflow — 9.1.0 (plan 82, RFC-68)

Cambio **MINOR**: capability nueva (aditiva) que no modifica contratos
existentes.

- **Capability nueva.** `orchestrators/architecture/` define el workflow de
  evolución arquitectónica en dos niveles (Project Analysis / Architecture
  Evolution) con diez stages, Change Set con NO_CHANGE y trazabilidad
  verificable; los contratos nuevos (registries de proyecto/sesión, Evidence
  Snapshot/Set, ACS, manifest) no rompen los existentes.
- **Import Workspace.** Los proyectos analizados se importan manualmente a
  `sessions/<project-key>/.project/` (gitignored salvo `.gitkeep`); el workflow
  no referencia ubicaciones externas en Fase 1 y nunca versiona el raw.
- **Material de evidencia.** El `reference/.project/` de BeaconRBX se movió a
  `sessions/BeaconRBX/.project/` fuera del seguimiento de git; los Evidence
  Snapshots derivados conservan lo analizado (RFC-46: las trazas no se
  reescriben).
- **Adopción.** El workflow corre a nivel del proyecto adoptante o del repo
  ARgentOS; no exige runtime ni hooks nuevos.

## 12. Eliminación de artefactos de contexto manuales — 10.0.0 (plan 84, RFC-70)

Cambio **MAJOR**: remoción de artefactos y de un estándar.

- **Qué se elimina.** `project-map.md` y `technical-analysis.md` dejan de ser
  artefactos del protocolo y el estándar
  `.agents/standards/context/PROJECT_ARTIFACTS.md` (incluidas sus plantillas
  de dominio) se elimina. No se crean ni se mantienen documentos de contexto
  manuales.
- **Qué lo reemplaza.** La Knowledge Base de discovery
  (`.project/knowledge/discovery/`) contiene el contexto estructural y técnico
  del proyecto: `executive_summary.md` es la entrada read-first y las entradas
  por tipo (`file_map.md`, `entrypoint.md`, `architecture.md`, `stack.md`,
  `dependencies.md`, `technical_debt.md`, `known_errors.md`, `project_flow.md`,
  `business_rules.md`, `glossary.md`, etc.) cubren el contenido de los
  artefactos eliminados, con frescura por claim y provenance.
- **Migración para adoptantes.** 1) Ejecutar una corrida de discovery (sujeta
  a `discovery_require_consent`) si la KB no está poblada. 2) Eliminar
  `project-map.md` y `technical-analysis.md` de la raíz del proyecto. 3)
  Actualizar las referencias locales (README, scripts, hooks) a las entradas
  de la KB. Los archivos existentes dejan de ser normativos; si se conservan,
  son copias locales no mantenidas.

## 13. Modelo de registro de ejecución — 11.0.0 (plan 78, RFC-64)

Cambio **MAJOR** del modelo conceptual: define la identidad de ejecución por
composición, los roles disjuntos de los cuatro registros, el alcance de
`state.json`, la semántica temporal UTC con fuente declarada y la
observabilidad de budget.

- **`state.json` limitado a gates de transición.** `state.json` registra los
  gates de transición del core (H00–H07, H11) y el status terminal
  únicamente; los gates no transicionales (D*, H09/H10, H15, S00, REVIEW) se
  registran solo en `HARNESS_REPORT.md`. `runner_state.py` rechaza cualquier
  `--trigger` fuera de ese conjunto (exit 2).
- **ENTRY con `iteration` y `clock` obligatorios.** Cada ENTRY de
  `HARNESS_REPORT.md` declara la iteración numérica de la ejecución y su
  fuente de reloj (`utc` | `agent_clock`); `timestamp` es el `event_ts` del
  trail y el `gate_ts` canónico vive en `state.json` (UTC, sufijo `Z`).
  Cuando difieren, el ENTRY declara `timestamp_divergence.cause`.
- **METRICS con `seq`/`iteration`/`clock`.** Todo evento METRIC lleva `seq`
  (entero, estrictamente creciente por sesión), `timestamp` y `clock`; los
  eventos por ejecución llevan además `iteration`, incluidos `reuse_event` y
  `provider_cache_event` del catálogo 1.2.0 (10.3.0). `delegation` puede
  declarar `context_budget` y `attempt`. `session_start` es de nivel sesión.
- **Pairing de `context_budget`.** Toda delegación con `context_budget`
  registra el evento `context_budget` (declared/consumed) junto al evento
  `delegation` de la misma delegación; sin el par, la claim de cumplimiento
  es atestación.
- **`schema_version` 2.0.0.** `HARNESS_REPORT.md`, `METRICS.md` y
  `SESSION_LOG.md` pasan su `schema_version` a 2.0.0 (obligaciones nuevas
  para sesiones nuevas; MAJOR de contrato según §2).
- **Trazas históricas.** Las sesiones previas a 11.0.0 (incluida la banda
  publicada 7.0.0–10.3.0) son registros inmutables bajo la semántica previa
  (RFC-46): no se reescriben, no se re-reportan y no requieren acción de
  migración. Los checkers de desarrollo aplican las reglas nuevas solo a
  sesiones `>= 11.0.0`.
- **Adopción.** Leer `.agents/harness/INDEX.md`, sección "Execution records",
  para el modelo completo (roles, identidad, semántica temporal e invariantes
  EI/TR/TM/OBS). Los reportes nuevos deben incluir los campos obligatorios;
  los artefactos de sesión existentes no se migran.

## 14. Change Governance Artifact — 11.1.0 (plan 115, RFC-76)

Adición **MINOR** (compatible): nuevo contrato `CHANGE_GOVERNANCE.md` y nueva
categoría de estado persistente (Change Governance Artifacts), sin romper
contratos existentes.

- **Contrato nuevo.** `CHANGE_GOVERNANCE.md` describe el governance state durable
  de un Change. Es una capacidad nueva opcional: los proyectos existentes no
  requieren producir este artifact.
- **Identidad derivada.** La identidad del Change reutiliza `SegmentIdentity`
  (RFC-71); los identity inputs `{target, declaration, protocol_version,
  namespace}` son inmutables. `namespace` value y canonical representation
  quedan diferidos (RFC-76).
- **Elementos diferidos.** namespace value, canonical representation, closure
  predicate, reflexive bootstrap, Task↔Change cardinality, GC semantics y
  ubicación física permanecen sin decisión normativa (RFC-76).
- **Adopción.** Leer `docs/rfc/76-change-governance-artifact.md` y
  `.agents/contracts/CHANGE_GOVERNANCE.md`. Sin migración de datos: no existe
  storage previo.

## 15. Change Governance Artifact — identidad y persistencia — 11.2.0 (plan 115, RFC-76)

Adición **MINOR** (compatible): concretiza la identidad y la persistencia del
Change Governance Artifact (decisiones D-01/D-02/D-03).

- **Ubicación.** `.project/changes/<change_identity>.md` — categoría durable
  per-project, content-addressed, sin registry ni índice global.
- **Namespace.** `project_identity` (RFC-71 isolation, RFC-73 project segment).
- **Canonical representation.** Cuatro líneas ordenadas (`target` /
  `declaration` / `protocol_version` / `namespace`), UTF-8, SHA-256;
  `declaration` con trim, `target` verbatim.
- **Sin migración de datos:** no existe storage previo.

## 16. Change Governance Artifact — alcance del MVP: append/current/governance_position diferidos — 11.3.0 (plan 119, RFC-76)

Cambio **MINOR** (compatible): acota explícitamente el alcance del MVP del
Change Lifecycle Protocol sin cambiar el modelo del Change Governance Artifact.
No rompe contratos ni requiere migración.

- **Qué se declara diferido.** La operación de **append**, la derivación de
  **current** (`current decision` / `current authorization` / `current closure`) y
  la derivación de **governance_position** quedan **DEFERRED** (invariante
  `CGA-010`). No se implementa runtime, campo, endpoint, evento, estado ni método
  para ellas.
- **Por qué es compatible.** Ninguna de las tres operaciones existía: el runtime
  sólo expone la materialización completa del artifact. Un adoptante no puede
  consumir una capacidad que nunca estuvo disponible, por lo que no hay
  comportamiento eliminado.
- **Qué cambia en la lectura del contrato.** "Append-only" pasa a describir la
  **forma** del artifact (historia acumulada que no admite sobrescritura parcial
  de una colección), no una operación disponible. El contrato incorpora una
  sección `## Implemented scope (MVP)` que separa lo implementado de lo diferido.
- **Mecanismo disponible en el MVP.** La acumulación posterior de historia se
  realiza por **re-materialización completa con historia acumulada**: se provee la
  historia completa a la llamada de materialización y se reescribe el artifact.
  **No es append** y no debe documentarse como tal. Consecuencia declarada: los
  estados intermedios del artifact no se preservan, porque se reescribe el mismo
  path.
- **Adopción.** Leer `.agents/contracts/CHANGE_GOVERNANCE.md` (secciones
  `## Implemented scope (MVP)` y `## Deferred semantics`) y
  `docs/rfc/76-change-governance-artifact.md:Governance history`. Sin migración de
  datos.

## 17. Capacidad Protocol-native de deliberación adversarial — 11.4.0 (plan 120, RFC-77)

- **Qué se agrega.** La capacidad `adversarial-deliberation`: una Skill
  (`skills/adversarial-deliberation/SKILL.md`), un contrato de artefacto
  (`contracts/DELIBERATION_REPORT.md`), un punto de decisión
  (`standards/orchestration/DECISIONS.md`, `D7`) y una subsección del rol del
  Orchestrator (§4.4 *Deliberation Invocation*), más sus registros en taxonomía,
  boundaries e inventario de skills.
- **Por qué es compatible (MINOR).** Es una adición **opcional y aditiva**: no
  redefine ningún campo existente, no altera la semántica de ningún contrato
  previo y no rompe payloads anteriores. Un adoptante que no invoque la capacidad
  no observa ningún cambio de comportamiento: la Skill no se activa, no inyecta
  contexto y no crea obligación alguna.
- **Qué no cambia.** No se introduce ninguna entidad, `kind` de taxonomía, rol,
  perfil de worker, fase de workflow, estado, lifecycle state, authority class,
  registry, ID global de Trial/Jury ni primitive de identidad. No hay feature
  flag, gate, clasificador automático, voting, confrontación, telemetría ni Prompt
  Cache. La máquina de estados y el harness no se modifican: una deliberación
  **no** produce transiciones y **no** satisface ningún ítem `[gate]`.
- **Frontera de autoridad (importante para el adoptante).** El resultado de una
  deliberación es `attestation` y recomendación **advisory**. Nunca es
  verificación independiente, autoridad normativa, decisión humana, autorización,
  resolución de findings, transición de estado, autorización de release ni
  autorización de gobernanza. `Verdict ≠ Recommendation ≠ Decision`.
- **Independencia.** La independencia se registra como **condición de
  procedencia** (`ejecutores: mismo | distinto`), no como garantía
  epistemológica. Afirmar independencia epistemológica o presentar la deliberación
  como verificación independiente está **prohibido**. En ejecución de instancia
  única debe declararse `ejecutores: mismo` y el resultado se trata como
  `attestation`.
- **Persistencia.** `DELIBERATION_REPORT.md` es un artefacto **de sesión**
  (`.project/<session-uuid>/<iteration>/<order>-DELIBERATION_REPORT.md`),
  inmutable dentro de la sesión e `informational`. No hay categoría durable,
  registry, ID global, retención ni cleanup. No se escribe en `.project/changes/`.
- **Adopción.** Leer `.agents/contracts/DELIBERATION_REPORT.md` (secciones
  `## Authority boundary`, `## Provenance` y `## Limitations`),
  `docs/rfc/77-protocol-native-adversarial-deliberation.md` y
  `.agents/standards/orchestration/DECISIONS.md: D7 — Deliberation invocation`.
  Sin migración de datos.

## 18. Stable prefix provider-bound — 11.5.0 (plan 121, RFC-78)

- **Qué se agrega.** La definición del **stable prefix** de la materialización
  dirigida al provider en `standards/context/CONTEXT.md` («Stable prefix
  (provider-bound materialization)»): la regla de pertenencia (Stable Context ∧
  scope de la delegación ∧ consumido demostrablemente por el Worker o resoluble
  determinísticamente del Delegation Payload), el alcance **Core + Worker** del
  prefijo, el paso **`protocol-bootstrap` declarado y vacío** en el scope del
  Worker, la exclusión **deliberada y diferida** del segmento **Project/KB**, la
  frontera con las policies de composición y las no-equivalencias
  (`Stable Context ≠ Stable Prefix`; `Stable Prefix ≠ Segment ≠ identity ≠
  persistence ≠ autorización de reuso`; `resolver contenido ≠ cache hit`).
- **Por qué es compatible (MINOR).** Es una **adición documental**: define una
  semántica que hasta ahora no estaba escrita y **no** redefine ningún campo,
  contrato, máquina de estados, workflow, rol, policy de composición ni límite
  del Context Budget. Nada de lo que un adoptante hacía deja de ser válido.
- **Qué NO cambia en el Protocol.**
  - La definición de `SemanticContextIdentity` es la misma
    (`{protocol_version, project_identity, segments[]}`).
  - `session_uuid` mantiene su posición y su semántica en la derivación de
    identidad: el aislamiento **cross-session** no se altera y el reuso del
    prefijo es **intra-session**.
  - El aislamiento por proyecto y la prohibición de reuso cross-project (I-008)
    no se tocan.
  - No se introduce identity primitive, registry, estado, fase de workflow,
    authority class, base de datos de cache, feature flag ni gate nuevos.
  - El Protocol **no** implementa prompt cache del provider: el Provider posee su
    cache (creación, reuso, evicción, vida útil y billing). El Protocol **no**
    declara ahorro alguno.
- **Contrato de runtime (referencia, no Protocol).** La implementación de
  referencia del runtime introduce el **Ordering Contract v2**
  (`ordering_contract_version = "2"`) y un componente de contenido explícito en
  la identidad de materialización (`content_contract_version`), de modo que dos
  conjuntos de contenido distintos **nunca** comparten una misma
  `MaterializationIdentity`. El contrato v1 se conserva y sigue siendo válido: un
  runtime que implemente v1 sigue produciendo las mismas representaciones que
  antes. Un runtime que **no** implemente un contrato de orden nombrado por la
  identidad debe **rechazar** la materialización, no reinterpretarla.
- **Contrato de orden v2 (referencia para un runtime que lo adopte).** El banner
  de identidad (estático) precede a la **región estable** resuelta; el ancla
  `SemanticContextIdentity` y el sufijo dinámico la siguen, porque
  `session_uuid` participa de esa identidad. Así la región estable queda como
  **prefijo de bytes** invariante a `session_uuid`, task y referencias de
  artifacts. El paso `protocol-bootstrap` es **vacío** en el scope del Worker:
  no incluye `_AGENTS.md`, `.agents/INDEX.md`, state machines ni el rol del
  orquestador — su lectura corresponde al **Orchestrator**, y el contrato de
  ejecución del Worker no ordena al Worker leerlos.
- **Qué puede requerir atención del adoptante.** Si el adoptante tiene su propio
  runtime de materialización y quiere beneficiarse del prefijo estable, debe
  implementar el contrato v2 y resolver el contenido estable desde el payload:
  módulo de workflow (`target_phase`), rol (`role_to_adopt`), perfil (`profile`),
  policy del gate (`harness_policy`), skills (`skills`) y el rol del Worker. Los
  `input_artifacts` participan **como referencias**; su contenido nunca entra al
  prefijo. Un elemento nombrado que no se pueda resolver debe producir un **fallo
  explícito**, nunca contenido inventado.
- **Limitaciones declaradas.** El prefijo se envía en cada invocación y su
  tamaño es sustancial; sin evidencia del provider **no** puede afirmarse que el
  net benefit sea positivo. La evidencia de cache del provider
  (hit / tokens cacheados / costo) permanece **DEFERRED / NOT VERIFICABLE**
  porque no existe adapter real autorizado, y el beneficio económico permanece
  **UNKNOWN**.
- **Adopción.** Leer `docs/rfc/78-provider-bound-stable-prefix-materialization.md`
  y `.agents/standards/context/CONTEXT.md` (sección «Stable prefix
  (provider-bound materialization)»). Sin migración de datos.
