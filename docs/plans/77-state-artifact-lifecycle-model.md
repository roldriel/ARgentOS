# Plan 77 — Modelo de estado y lifecycle de artefactos (RFC-63)

**Status:** Executed
**Fecha:** 2026-08-25
**RFC:** RFC-63 (`plans/rfc/63-state-and-artifact-lifecycle-model.md`)
**Clase:** A (modelo conceptual: dimensiones de estado, lifecycle de artefactos, semántica de COMPLETED y de los campos de estado manuales; RFC-56)
**Depende de:** plan 76 (4.0.0: vocabulario `verified`/`attested`/`inference` y `claim_class`); RFC-63 `Accepted` como criterio de entrada
**Origen:** `ARCHITECTURAL_DECISION_MODEL.md:D1 — State Semantics (dimensiones de estado)`, `ARCHITECTURAL_DECISION_MODEL.md:D2 — Artifact Lifecycle`, `ARCHITECTURAL_DECISION_MODEL.md:D3 — Completion Semantics`; RFC-63 Proposal (2026-08-25).

## Objetivo

Implementar el modelo de estado de la RFC-63 en el payload: separar el estado en
tres dimensiones con entidad propia (Task State, Gate State y Artifact Lifecycle)
y cuatro conceptos derivados (Execution State, Verification State, Approval State
y Plan State), con sus fuentes de verdad declaradas; hacer que el Artifact
Lifecycle sea derivado del registro de gates y nunca escrito a mano; definir
COMPLETED como completitud relativa al alcance confirmado, con aprobaciones
humanas diferidas explícitamente registradas (`Deferred Items` en
`VERIFICATION_REPORT.md` y en `SESSION_BRIEF.md`); y resolver el "review gate"
como Gate State sobre `REVIEW_REPORT.md`, no como estado de tarea.

El plan implementa solo lo que la RFC-63 define. El detalle de las clases de
evidencia y la regla VERIFIED completa quedan para la RFC-65 (el invariante
REL-001 de la RFC se deja señalado como pendiente, sin inventar semántica); el
registro de eventos y la temporalidad completa quedan para la RFC-64. El plan 76
ya introdujo el vocabulario mínimo `verified` / `attested` / `inference` que este
modelo consume para distinguir dimensiones (Approval/Verification) sin redefinir
clases de evidencia.

## Criterio de entrada

- [ ] RFC-63 en estado `Accepted` y registrada en `plans/INDEX.md` (hoy
      `Proposal`, 2026-08-25: el plan se redacta en paralelo, pero no se ejecuta
      hasta la aceptación; la clase A de RFC-56 exige RFC `Accepted` antes de
      tocar `protocol/.agents/`).
- [ ] Usuario confirma la clasificación MAJOR (`5.0.0`, siguiente a la `4.0.0`
      del plan 76 en curso en `dev`) y la nota de migración
      (`docs/VERSIONING.md:3. Versionado`).
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos de
      la tabla de Afectados de la RFC existen y las secciones citadas en Pasos
      resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `plans/77-state-artifact-lifecycle-model.md` — este plan.
2. `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` — Task
   Profiles sin "the review gate" como gate de tarea, review gate como Gate
   State sobre `REVIEW_REPORT.md`, y semántica de COMPLETED relativa al alcance
   confirmado.
3. Los siete contratos de artefactos afectados (TASK_ANALYSIS, TASK_SPECIFICATION,
   CONTEXT_ARTIFACT, CONTEXT_VALIDATION_REPORT, EXECUTION_PLAN, EXECUTION_SUMMARY
   y VERIFICATION_REPORT) — retiro de los campos manuales `status`/`state`/
   `approved`/`validation.complete`, metadata de solo lectura derivada y
   `schema_version` 2.0.0.
4. `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md` —
   sección `## Deferred Items` con confirmación de usuario.
5. `protocol/.agents/contracts/SESSION_BRIEF.md` — registro de aprobaciones
   diferidas (`deferred: true` + confirmación del usuario).
6. Policies H05/H06/H07 — ítems de checklist sobre dimensión de estado,
   lifecycle derivado y diferidos.
7. `protocol/.agents/orchestrators/core/roles/orchestrator.md` — §4.1
   determinista: review gate obligatorio para `complex` con `rubrics` habilitado,
   registrado como Gate State en `HARNESS_REPORT.md`.
8. `protocol/.agents/harness/INDEX.md` — §Protocol State and Hook Enforcement
   declara las tres dimensiones + cuatro derivadas, el Artifact Lifecycle y los
   invariantes ST/AL/CMP.
9. `protocol/.agents/contracts/REVIEW_REPORT.md` — mapeo de la recomendación a
   `review_passed` / `review_failed`.
10. `protocol/.agents/harness/gate_validator.py` — checks de secciones en
    conflicto (H00/H03), existencia de `REVIEW_REPORT.md` para `complex` (H06) y
    estructura de `Deferred Items`.
11. `tools/check_session_artifacts.py` — celdas External del lifecycle para
    sesiones `>= 5.0.0` (sin campos manuales; COMPLETED con gates in-scope PASS).
12. Tests de los checkers dev (`tests/test_check_session_artifacts.py`) y del
    validador del producto (`protocol/.agents/harness/tests/test_gate_validator.py`).
13. `docs/MIGRATION.md` — sección nueva tras §5 Soporte de versiones con la nota
    MAJOR `5.0.0`; `protocol/.agents/VERSION` → `5.0.0`; `CHANGELOG.md` con
    `## [5.0.0]`.
14. `plans/INDEX.md` — plan 77 registrado en su serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el payload y git que
   existen los archivos citados y que las secciones referenciadas en los pasos
   1–8 resuelven: `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`
   y `:COMPLETED`; `protocol/.agents/orchestrators/core/roles/orchestrator.md:4.1 Reviewer invocation and review gate`;
   `protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement`;
   `protocol/.agents/contracts/HARNESS_REPORT.md:Required structure`;
   `protocol/.agents/contracts/REVIEW_REPORT.md:Scope`;
   `protocol/.agents/contracts/SESSION_BRIEF.md:Structure`; las secciones
   `Metadata`, `Validation`/`State`/`Context Validation`/`Plan Decision` de los
   contratos de la tabla de Afectados; §Gate Checklist de H05, H06 y H07;
   `docs/MIGRATION.md:5. Soporte de versiones`. Confirmar RFC-63 `Accepted` y la
   clasificación MAJOR (criterios de entrada).

1. **Dimensiones y semántica en la máquina de estados.** En
   `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`:
   a. En §Task Profiles, la fila `complex` de la columna "Mandatory gates" deja
      de listar "the review gate" (queda "The full cycle"); agregar una regla en
      el bloque de reglas de la tabla: para `complex`, la revisión de
      `REVIEW_REPORT.md` es un Gate State sobre el artefacto
      (`review_required` → `review_passed` | `review_failed`) evaluado por el
      Orchestrator cuando el flag `rubrics` está habilitado; no es un estado de
      tarea ni un gate de transición, y no se registra en `state.json` sino en
      `HARNESS_REPORT.md` (D-009, AL-001).
   b. En §COMPLETED, la descripción declara la semántica de completitud
      relativa al alcance confirmado: `COMPLETED` ⇔ H06 + H07 PASS, todos los
      gates en-scope con PASS, sin criterios en-scope FAIL/PENDING en el reporte,
      y toda aprobación humana en-scope completada o diferida con confirmación
      del usuario (`Deferred Items` + `SESSION_BRIEF.md`) (D-007, D-008,
      CMP-001…CMP-004).

2. **Contratos de artefactos (retiro de campos manuales).** En los siete
   contratos de la lista de Afectados, sin tocar los demás:
   a. `protocol/.agents/orchestrators/core/contracts/TASK_ANALYSIS.md:Metadata`,
      `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Metadata`,
      `protocol/.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md:Metadata`,
      `protocol/.agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md:Metadata`,
      `protocol/.agents/orchestrators/core/contracts/EXECUTION_PLAN.md:Metadata`,
      `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md:Metadata`
      y `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md:Metadata`:
      retirar el campo `status = ""` y
      declarar que el estado de lifecycle del artefacto es derivado del registro
      de gates (`draft` → `validated`; `superseded` si es reemplazado) y que el
      autor no lo escribe (D-201, AL-001).
   b. `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Validation`
      y `protocol/.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md:Context Validation`:
      retirar `[validation] complete`; la validación pasa a ser derivada del PASS
      del gate de salida (H01/H03) (D-201, AL-002).
   c. En `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md` y
      `protocol/.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md`:
      eliminar la sección `## State` por completo; el Task State es único por
      tarea y vive en la máquina core + `state.json`, nunca en el artefacto
      (D-103, ST-004).
   d. `protocol/.agents/orchestrators/core/contracts/EXECUTION_PLAN.md:Plan Decision`:
      retirar `approved` de `[decision]`; la
      aprobación del plan es un Approval/Gate State derivado del PASS de H04, no
      una declaración del planner (D-201, D-103). Se conserva `reasoning`.
   e. `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md`:
      se conservan `final_state.status`
      (`VERIFIABLE`/`BLOCKED`, estado del proyecto declarado por el executor y
      consumido por H05) y `steps_executed[].status` (estado de cada paso); el
      contrato etiqueta ambos como estado de proyecto/paso, no como lifecycle del
      artefacto (ST-004).
   f. Bump de `schema_version` a `2.0.0` en el front matter `+++` y en la línea
      del cuerpo de los siete contratos: el retiro de campos y la prohibición de
      escribirlos vuelve no conformes a los artefactos que los declaren (MAJOR de
      contrato, alineado con `docs/MIGRATION.md:2. Procedimiento de migración`).

3. **Aprobaciones diferidas.** 
   a. `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`:
      nueva sección `## Deferred Items` entre §Scope Compliance y §Final Decision,
      con bloque TOML `[[deferred_items]] item = ""`, `deferred = true`,
      `confirmed_by = ""`, `confirmation_date = ""`, `reason = ""`; regla: todo
      ítem diferido es una aprobación humana en-scope diferida con confirmación
      del usuario (nunca se presenta como completado) (D-008, CMP-003, CMP-004).
      Agregar la sección a la lista de secciones requeridas de §Completion
      Criteria y al bloque machine-readable.
   b. `protocol/.agents/contracts/SESSION_BRIEF.md`: nueva sección
      `## Deferred Approvals` con `[[deferred_approvals]] item = ""`,
      `deferred = true`, `confirmed_by = ""`, `confirmation_date = ""`, y la
      regla de que las aprobaciones diferidas quedan `PENDING_USER_CONFIRMATION`
      hasta la confirmación; el Approval State se deriva de `SESSION_BRIEF.md` +
      `Deferred Items` (D-008, D-004).

4. **Policies H05/H06/H07.** En el §Gate Checklist de cada policy:
   - H05: ítem `[gate]` — el `EXECUTION_SUMMARY.md` no declara campos manuales de
     lifecycle (`status`/`state`/`approved`/`validation.complete`) en su
     `Metadata`; el lifecycle del artefacto es derivado del PASS de H05 (AL-001).
   - H06: ítem `[gate]` — `## Deferred Items` está presente, es TOML parseable,
     cada entrada tiene `deferred = true` y `confirmed_by` no vacío, y ningún
     ítem diferido se declara completado; COMPLETED exige que ningún criterio
     en-scope quede FAIL/PENDING y que toda aprobación en-scope esté completada o
     diferida con confirmación (CMP-002…CMP-004).
   - H07: nota de coherencia de dimensiones — `scope_compliance` registra
     decisiones de aprobación/alcance (Approval/Gate State), no el lifecycle del
     artefacto; la dimensión se indica al citar cada check (ST-004, D-103).

5. **Review gate en el rol y en el contrato del reporte.**
   a. `protocol/.agents/orchestrators/core/roles/orchestrator.md:4.1 Reviewer invocation and review gate`:
      renombrar la sección a "Reviewer invocation and review gate". Regla nueva:
      cuando el perfil de la tarea es `complex` y `rubrics` está habilitado, la
      invocación del `reviewer` y la evaluación del review gate sobre
      `REVIEW_REPORT.md` son obligatorias antes de `VERIFYING → COMPLETED`: el
      Orchestrator registra en `HARNESS_REPORT.md` una entrada con
      `trigger: "REVIEW"`, transición `VERIFYING → COMPLETED` y resultado PASS
      (`review_passed`, recomendación `APPROVE`) o FAIL (`review_failed`,
      `REWORK`/`NEEDS_CLARIFICATION`); `REWORK` se enruta por el retry bound y
      luego a `RECOVERY`; `NEEDS_CLARIFICATION` transita a ese estado. Para
      `standard`/`trivial` o con `rubrics` deshabilitado, la invocación sigue
      siendo opcional (MAY) y no genera Gate State. El review gate no es un gate
      de transición: no se registra en `state.json` (D-009, ST-002).
   b. `protocol/.agents/contracts/REVIEW_REPORT.md:Scope`: declarar que el
      reporte se produce por el `reviewer` cuando el review gate es requerido
      (`complex` + `rubrics`) o cuando el Orchestrator lo invoca opcionalmente, y
      que la recomendación se mapea a `review_passed` (`APPROVE`) o
      `review_failed` (`REWORK`/`NEEDS_CLARIFICATION`) como Gate State del
      artefacto, registrado por el Orchestrator en `HARNESS_REPORT.md`.

6. **Dimensiones y lifecycle en el harness.** En
   `protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement`,
   agregar una subsección `## State dimensions` (autocontenida, sin referencias a
   `plans/`):
   - Tabla de dimensiones: Task State (entidad, máquina core + `state.json`),
     Gate State (entidad por gate, `state.json` para gates de transición +
     `HARNESS_REPORT.md` para los demás), Artifact Lifecycle (derivada del Gate
     State), Execution State (≡ Task State), Verification State (Gate State
     H06/H07 + reportes), Approval State (`SESSION_BRIEF.md` + `Deferred Items`),
     Plan State (externa, gobernanza del proyecto).
   - Artifact Lifecycle: estados `draft`, `validated`, `superseded`; eventos
     `produced`, `corrected`, `gate_failed`, `gate_passed`; propiedades
     `archived` y `rejected`; `approved`/`verified`/`executed` NO son estados del
     artefacto (pertenecen a otras dimensiones).
   - Invariantes ST-001…ST-004, AL-001…AL-004 y CMP-001…CMP-004 redactados
     inline en inglés; REL-001 se anota como "semantics detailed in the evidence
     model" sin citar RFCs (frontera documental), porque depende de la RFC-65.
   - Actualizar el párrafo de `state.json` para que distinga Task State + gates
     de transición (en `state.json`) de Gate States no transicionales y Artifact
     Lifecycle (en `HARNESS_REPORT.md`, derivado).

7. **Validador estructural.** En `protocol/.agents/harness/gate_validator.py`:
   a. Checks de secciones en conflicto (AL-004):
      - H00 (TASK_ANALYSIS): `sufficiency.ready_for_specification = true` con
        `recommended_next_state = NEEDS_CLARIFICATION` → FAIL; `intent_confidence.level = HIGH`
        con `recommended_next_state = CONFIRMING_INTENT` → FAIL (camino
        auto-confirmado, P17).
      - H03 (CONTEXT_VALIDATION_REPORT): `decision.result = VALIDATED` con
        `completeness.status = INCOMPLETE` o `consistency.status = CONFLICTING`
        → FAIL.
   b. H06 profile-aware: cuando el perfil de la sesión (leído de TASK_ANALYSIS,
      como ya hace `read_task_profile`) es `complex`, el validador exige un
      `REVIEW_REPORT.md` en el directorio de la iteración (criterio de aceptación
      "complex sin REVIEW_REPORT").
   c. H06: si `## Deferred Items` está presente, validar que el bloque TOML sea
      parseable y que cada entrada tenga `deferred = true` y `confirmed_by` no
      vacío; sin bloque, el check es SKIP (compatible con reportes previos a
      5.0.0).
   d. Tests nuevos en `protocol/.agents/harness/tests/test_gate_validator.py`
      para los casos a–c (stdlib-only, fixtures en `tmp_path`).

8. **Checker dev de lifecycle.** En `tools/check_session_artifacts.py`:
   - Agregar `LIFECYCLE_PROTOCOL = (5, 0, 0)` y aplicar los checks nuevos solo a
     sesiones que declaren `protocol_version >= 5.0.0`; las sesiones previas se
     siguen tratando como traza histórica (RFC-46).
   - AL-001/ST-004: para cada artefacto core de los siete tipos de la RFC en la
     sesión, detectar declaraciones de campos manuales retirados (`status = ""`,
     `## State`, `validation.complete`, `approved` en `Plan Decision`) y
     reportarlas como violaciones.
   - CMP-001: cuando `state.json.status == COMPLETED`, el dict `gates` debe
     contener los gates de transición en-scope del perfil declarado (`trivial`:
     H00/H04/H06; `standard`: H00–H07; `complex`: H00–H07), con H11 requerido
     solo cuando la sesión entró a `CONFIRMING_INTENT` (por `HARNESS_REPORT.md` o
     el evento `state_transition` de `METRICS.md`), y para `complex` una entrada
     `REVIEW` PASS en `HARNESS_REPORT.md`.
   - CMP-003/CMP-004: las entradas de `Deferred Items` de los reportes de sesión
     tienen `deferred = true` y confirmación; ningún ítem diferido aparece como
     completado.
   - Tests nuevos en `tests/test_check_session_artifacts.py` (fixtures en
     `tmp_path`, stdlib-only, sin dependencia de `protocol/`).

9. **Documentación y versión.**
   - `docs/MIGRATION.md`: nueva sección tras §5 Soporte de versiones,
     "## 7. Modelo de estado y lifecycle de artefactos — 5.0.0 (plan 77,
     RFC-63)": los campos manuales `status`/`state`/`approved`/
     `validation.complete` de los siete contratos se retiran y el lifecycle se
     deriva del registro de gates; `Deferred Items` y la semántica de COMPLETED
     relativa al alcance; el review gate como Gate State sobre `REVIEW_REPORT.md`;
     `schema_version` 2.0.0 en los siete contratos; trazas históricas bajo
     semántica previa (RFC-46); ninguna acción sobre artefactos previos.
   - `protocol/.agents/VERSION` → `5.0.0`. En `CHANGELOG.md`, nueva sección
     `## [5.0.0] — 2026-08-25` con `Added` (dimensiones de estado, `Deferred
     Items`, review gate), `Changed` (semántica de COMPLETED, policies
     H05/H06/H07, contratos), `Removed` (campos manuales de estado) y `Modelo
     conceptual` (RFC-63 Accepted), todo referenciando `(plan 77, RFC-63)`.

10. **Registro.** En `plans/INDEX.md`, registrar el plan 77 en su serie con
    status `Aprobado para ejecución` (pasa a `Executed` al cerrar este plan); la
    RFC-63 queda `Accepted` en el commit de aceptación previo y su Amendment Log
    registra la fecha y el plan. Agregar la `## Nota de ejecución` al ejecutar.

## Criterios de salida

- [ ] El payload declara las 3 dimensiones con entidad propia + las 4 derivadas,
      con sus fuentes de verdad (`AGENT_STATE_MACHINE.md` + `harness/INDEX.md`,
      §State dimensions) (criterio de aceptación de la RFC).
- [ ] El review gate aparece resuelto como Gate State sobre `REVIEW_REPORT.md`
      (`review_required` → `review_passed` | `review_failed`); la tabla de Task
      Profiles ya no lo lista como gate de tarea, y el validador rechaza
      `complex` sin `REVIEW_REPORT.md`.
- [ ] COMPLETED tiene semántica de alcance confirmado; `## Deferred Items` está
      en el contrato de `VERIFICATION_REPORT.md` y `SESSION_BRIEF.md` registra
      los diferidos con confirmación (CMP-001…CMP-004).
- [ ] Los siete contratos no llevan campos de estado manuales
      (`status`/`state`/`approved`/`validation.complete`); `schema_version`
      2.0.0; los demás contratos quedan intactos.
- [ ] El validador rechaza secciones en conflicto (H00/H03) y `Deferred Items`
      inválidos; H05/H06/H07 citan la dimensión de cada check en sus Gate
      Checklists.
- [ ] `check_session_artifacts.py` detecta campos manuales y COMPLETED sin gates
      in-scope para sesiones `>= 5.0.0`; no reporta sesiones previas (RFC-46);
      tests nuevos en verde.
- [ ] `docs/MIGRATION.md` tiene la sección 7 con la nota MAJOR `5.0.0`;
      `protocol/.agents/VERSION` = `5.0.0`; changelog `[5.0.0]` con
      `(plan 77, RFC-63)`.
- [ ] Batería canónica del repo en verde y H13 aplicado por juicio sobre las
      secciones y campos nuevos.

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

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por
diseño; debe quedar verde en `master` tras la promoción.

Juicios manuales: coherencia H13 de las secciones nuevas (Task Profiles de
`protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`, la subsección
State dimensions de `protocol/.agents/harness/INDEX.md`, contratos, policies);
verificación de que ningún artefacto nuevo de los siete tipos declara campos de
estado manuales; revisión de que la frontera documental se mantiene (el payload
no cita `plans/` ni RFCs).

## Riesgos

- **Frontera con RFC-64/RFC-65:** este plan no implementa REL-001 (clases de
  evidencia detalladas y regla VERIFIED completa) ni el registro de eventos;
  REL-001 queda anotado como dependencia del modelo de evidencia sin inventar
  semántica. No diseñar más allá de la distinción mínima de `claim_class` del
  plan 76.
- **Trazas históricas (RFC-46):** los checks dev nuevos deben aplicarse solo a
  sesiones `>= 5.0.0`; las sesiones previas no se re-reportan ni se invalidan.
- **MAJOR 5.0.0:** requiere confirmación explícita del usuario y nota de
  migración; sin confirmación, el plan no se ejecuta (criterio de entrada).
- **Campos residuales fuera de alcance:** `RECOVERY_REPORT.md` e
  `INTENT_REFLECTION.md` también declaran `status` en su Metadata, pero no están
  en la lista de Afectados de la RFC-63; este plan no los toca. Si al cerrar la
  batería el invariante ST-004 se aplica de forma transversal, registrar el
  pendiente como enmienda futura de la RFC, no ampliar el alcance aquí.
- **Condicionamiento del review gate:** la RFC no fija si el review gate depende
  del flag `rubrics` (el rol `reviewer` solo existe con ese flag); este plan lo
  condiciona a `complex` + `rubrics` y lo declara así en la máquina y en el rol.
  Confirmar esa lectura con el mantenedor al aceptar la RFC.
- **Coherencia estructural:** retirar secciones de contratos puede romper citas o
  la coherencia taxonómica (p. ej. la lista de secciones de `gate_validator.py`
  o de H13); correr la batería en cada paso de payload, no solo al final.
- **Schema de contratos:** el bump a 2.0.0 refleja el retiro de campos (MAJOR de
  contrato); no tocar contratos fuera de la lista de la RFC y no hacer
  obligatorios campos nuevos como `Deferred Items` para reportes previos.

## Trazabilidad

`ARCHITECTURAL_DECISION_MODEL.md:D1 — State Semantics (dimensiones de estado)` +
`ARCHITECTURAL_DECISION_MODEL.md:D2 — Artifact Lifecycle` +
`ARCHITECTURAL_DECISION_MODEL.md:D3 — Completion Semantics` → RFC-63 (Proposal
2026-08-25; `Accepted` como criterio de entrada) → Plan 77 → entregables 1–14.

## Nota de ejecución

2026-08-25: ejecutado en `dev` con la RFC-63 aceptada el mismo día y la
clasificación MAJOR (`5.0.0`) confirmada por el mantenedor. Batería canónica en
verde: invariantes, citas, estructura, coherencia taxonómica, artefactos de
sesión y estado de versiones (warnings de `dev` esperados por tags pendientes);
suite de desarrollo en verde (189 tests) y suite de producto del harness en
verde (87 tests). H13 aplicado por juicio sobre las secciones nuevas. VERSION
`5.0.0` y changelog `[5.0.0]` bumpados; plan 77 registrado como `Executed` en
`plans/INDEX.md`. Commit atómico en `dev`.
