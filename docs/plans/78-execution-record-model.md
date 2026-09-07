# Plan 78 — Modelo de registro de ejecución (RFC-64)

**Status:** Executed
**Fecha:** 2026-08-25 (creación); rebasado 2026-09-04 contra el estado 10.3.0
(ver `## Nota de rebase`)
**RFC:** RFC-64 (`docs/rfc/64-execution-record-model.md`)
**Clase:** A (modelo conceptual: identidad de ejecución, roles de los
registros, alcance de `state.json`, semántica temporal y observabilidad de
budget; RFC-56)
**Change Level:** L3 (RFC-75 Mecanismo 2: coordination 0; scope 3 — payload
multi-área (contratos + harness) + tooling dev + tests + docs/release;
architectural impact 3 — semántica de contratos e invariantes de registros,
MAJOR irreversible; release impact 3 — MAJOR `11.0.0`; duration/complexity 1
— multi-sesión; `Level = max = 3`)
**Depende de:** plan 76 (4.0.0: vocabulario `clock`/`claim_class` y regla de
claims) y plan 77 (5.0.0: dimensiones de estado, lifecycle de artefactos y
semántica de COMPLETED); RFC-64 `Accepted` (plan 103, 2026-09-03) como
criterio de entrada
**Origen:** `ARCHITECTURAL_DECISION_MODEL.md:D5 — Execution Identity`,
`ARCHITECTURAL_DECISION_MODEL.md:D6 — Execution Record / Audit Trail`,
`ARCHITECTURAL_DECISION_MODEL.md:D7 — Temporal Semantics`,
`ARCHITECTURAL_DECISION_MODEL.md:D10 — Observability / Budget`; RFC-64
(Proposal 2026-08-25 → `Accepted` por plan 103, 2026-09-03); condiciones de
revisión C-3…C-6 de la aceptación, preservadas como contexto en el Amendment
Log de la RFC-64 e incorporadas a este plan por el rebase (2026-09-04).

## Objetivo

Implementar en el payload el modelo de registro de ejecución de la RFC-64:
definir la identidad de ejecución por composición (`execution_id =
(session_id, iteration)`), asignar roles disjuntos a los cuatro registros
(`state.json`, `HARNESS_REPORT`, `SESSION_LOG`, `METRICS`) y a los artefactos,
declarar que `state.json` solo registra gates de transición core (H00–H07,
H11) más el status terminal, fijar UTC con fuente declarada como reloj
canónico (el marcador `clock` ya introducido por el plan 76), correlacionar
eventos por event keys (`(execution_id, trigger)` en gates, `(execution_id,
seq)` en métricas, `(execution_id, phase, attempt#)` en delegaciones), y hacer
verificable el registro de `context_budget` para toda delegación con budget.
No introduce Event Sourcing ni cambia la arquitectura declarativa.

El plan se materializa como versión `11.0.0` (MAJOR) desde la última versión
publicada en `master` (`10.3.0`; `docs/VERSIONING.md:3. Versionado`). La
versión `6.0.0` del borrador original nunca fue publicada y queda descartada
por este rebase.

El plan implementa solo lo que la RFC-64 define. Las clases de evidencia y la
regla VERIFIED quedan para la RFC-65; el lifecycle de conocimiento para la
RFC-67; ambos quedan fuera de alcance. El plan 76 ya introdujo el marcador
`clock` (`utc` | `agent_clock`) y la regla de claims que este modelo consume
para declarar la fuente temporal; el plan 77 ya separó las dimensiones de
estado y el lifecycle de artefactos que este modelo referencia como registros
derivados. Las tres lecturas de implementación aceptadas por el mantenedor al
aceptar la RFC-64 (plan 103) forman parte de la decisión que este plan
implementa, sin reinterpretarlas: (1) `clock` implementa la fuente
`agent_clock` — sin renombrar `clock` a `source`; (2) `seq` estrictamente
monótono por sesión para EI-003/TR-004; (3) TR-002 con tolerancia de 60
segundos y divergencias que registran `timestamp_divergence.cause`.

## Criterio de entrada

- [ ] RFC-64 en estado `Accepted` (plan 103, 2026-09-03; verificable en
      `docs/rfc/64-execution-record-model.md` y en `docs/rfc/INDEX.md`). La
      clase A de RFC-56 exige RFC `Accepted` antes de tocar
      `protocol/.agents/`; la aceptación por el plan 103 no autoriza por sí
      sola esta ejecución, que queda habilitada por este plan `Aprobado para
      ejecución` con sus criterios de entrada cumplidos.
- [ ] Usuario confirma la clasificación MAJOR y la versión objetivo `11.0.0`
      (siguiente a la última versión publicada en `master`: `10.3.0`;
      `docs/VERSIONING.md:3. Versionado`) y la nota de migración de la
      sección 13 nueva de `docs/MIGRATION.md` (MAJOR exige nota de migración).
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos
      de la tabla de Afectados de la RFC existen y las secciones citadas en
      Pasos resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `docs/plans/78-execution-record-model.md` — este plan.
2. `protocol/.agents/harness/INDEX.md` — subsección `## Execution records`
   (roles de los registros, identidad de ejecución, event keys, semántica
   temporal, información mínima de reconstrucción e invariantes EI/TR/TM/OBS
   inline en inglés) e **integración** (no duplicación) del alcance de
   `state.json` en §Protocol State and Hook Enforcement / §State dimensions:
   la declaración existe desde 5.0.0 (plan 77) y se extiende para cerrar el
   alcance explícitamente (gates de transición core H00–H07, H11 + status
   terminal; D*/H10/H15/S00/REVIEW solo en `HARNESS_REPORT.md`), sin
   contradecir ST-002 ni las invariantes CMP-001/CMP-003 ya declaradas.
3. `protocol/.agents/contracts/HARNESS_REPORT.md` — `schema_version` 1.1.0 →
   2.0.0 (MAJOR de contrato: obligaciones nuevas para sesiones nuevas);
   ENTRY con `iteration` obligatorio, `clock` obligatorio, `timestamp`
   declarado como `event_ts` y `timestamp_divergence` opcional para
   divergencias declaradas con causa.
4. `protocol/.agents/contracts/METRICS.md` — `schema_version` 1.2.0 → 2.0.0
   (MAJOR de contrato); `seq` obligatorio en todo evento, `iteration`
   obligatorio en los eventos por ejecución — incluyendo `reuse_event` y
   `provider_cache_event` del catálogo 1.2.0 (plan 91, RFC-74) —, `clock`
   obligatorio, y `delegation` con `context_budget` (declarado) y `attempt`
   opcionales.
5. `protocol/.agents/contracts/SESSION_LOG.md` — `schema_version` 1.1.0 →
   2.0.0 (MAJOR de contrato); campo `Execution` por entrada y marcador de
   reloj cuando el heading no es UTC-normalizado.
6. `protocol/.agents/harness/runner_state.py` — `TRANSITION_TRIGGERS`, rechazo
   de triggers fuera de alcance, `gate_ts` canónico UTC con sufijo `Z` y
   `detect_bypass` con flag de confiabilidad.
7. `protocol/.agents/orchestrators/core/harness/policies/H15-delegation-validity.md` —
   extensión del ítem 4 del §Pre-delegation gate con la obligación de
   registrar el evento `context_budget` (declared/consumed) al delegar con
   budget.
8. `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md` — alineación del
   bloque `context_budget` con el pairing delegación ↔ evento `context_budget`.
9. `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` — reglas de
   registro (`seq`, `iteration`, `clock`, incluidos los eventos reuse/cache
   del catálogo vigente) y pairing de budget en §Registration rules y
   §Verifiability classes.
10. `tools/aggregate_metrics.py` — `--audit` correlacionado por
    `(iteration, trigger)` para sesiones `>= 11.0.0` y comparación de
    timestamps con tolerancia de 60 s y divergencia declarada; correlación por
    `trigger` preservada para trazas previas sin `iteration` (RFC-46).
11. `tools/check_session_artifacts.py` — checks para sesiones `>= 11.0.0`:
    alcance de `state.json`, `iteration`/`clock` en ENTRY, `seq`/`iteration`/
    `clock` en METRIC, `seq` monotónico y pairing de `context_budget`. Las
    sesiones de la banda legacy 7.0.0–10.3.0 no se re-reportan (RFC-46).
12. `tools/measure_context_budget.py` — `--phase`/`--iteration` opcionales en
    el reporte JSON.
13. Tests de los checkers dev (`tests/test_check_session_artifacts.py`,
    `tests/test_aggregate_metrics.py`, `tests/test_measure_context_budget.py`)
    y del producto (`protocol/.agents/harness/tests/test_runner_state.py`).
14. `docs/MIGRATION.md` — sección nueva 13 tras §12 con la nota MAJOR
    `11.0.0`; `protocol/.agents/VERSION` → `11.0.0`; `CHANGELOG.md` con
    `## [11.0.0]`; `docs/plans/INDEX.md` — plan 78 registrado en su serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el payload y git
   que existen los archivos citados y que las secciones referenciadas en los
   pasos 1–8 resuelven: `protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement`,
   `protocol/.agents/harness/INDEX.md:State dimensions` y
   `protocol/.agents/harness/INDEX.md:Enforcement boundaries`;
   `protocol/.agents/contracts/HARNESS_REPORT.md:Required structure`;
   `protocol/.agents/contracts/METRICS.md:Event catalog` (schema vigente
   1.2.0);
   `protocol/.agents/contracts/SESSION_LOG.md:Required content`;
   `protocol/.agents/orchestrators/core/harness/policies/H15-delegation-validity.md:Pre-delegation gate`;
   `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:context_budget`;
   `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Registration rules`;
   `docs/MIGRATION.md:12. Eliminación de artefactos de contexto manuales`.
   Confirmar RFC-64 `Accepted` y la clasificación MAJOR con versión objetivo
   `11.0.0` confirmada por el usuario (criterios de entrada).

1. **Contratos de registro (event keys y fuente temporal).**
   a. `protocol/.agents/contracts/HARNESS_REPORT.md:Required structure`:
      `schema_version` del front matter → `2.0.0` (MAJOR de contrato: campos
      obligatorios nuevos para sesiones nuevas; trazas previas exentas,
      RFC-46). Agregar a la lista de campos del ENTRY `- Execution:
      <iteration>` (el folder numérico de la iteración; `execution_id`
      compartido con `state.json`). En el bloque JSON del comentario `ENTRY`,
      `iteration` pasa a ser obligatorio (string con el folder numérico) y
      `clock` pasa a ser obligatorio (`utc` | `agent_clock`); declarar que
      `timestamp` es el `event_ts` del trail (momento de registro) y que el
      `gate_ts` canónico vive en `state.json`; agregar el campo opcional
      `"timestamp_divergence": {"cause": "<reason>"}` para cuando `event_ts`
      difiere del `gate_ts` del mismo gate (TR-002). El event key del gate es
      `(session_uuid, iteration, trigger)` y es la clave compartida con
      `state.json` (EI-002, TR-001).
   b. `protocol/.agents/contracts/METRICS.md:Event catalog`: el contrato
      vigente es `schema_version` 1.2.0 (10.3.0, plan 91/RFC-74) con
      `reuse_event` y `provider_cache_event`; pasa a `2.0.0` (MAJOR de
      contrato). `seq` (entero, monótono estricto por sesión — lectura
      Accepted de EI-003/TR-004) y `clock` (`utc` | `agent_clock`)
      obligatorios en todo evento; `iteration` obligatorio en los eventos por
      ejecución: `state_transition`, `reviewer_retry`, `failure`, `delegation`,
      `skill_override`, `flag_evidence`, `context_budget`,
      `context_candidates`, `discovery_consent`, `reuse_event` y
      `provider_cache_event`; `session_start` es de nivel sesión y no lleva
      `iteration`. En `delegation`, agregar `context_budget` opcional (el
      budget declarado del payload, número finito positivo) y `attempt`
      opcional (ordinal 1-based del intento de delegación, D-003). El event
      key de métricas es `(session_uuid, iteration, seq)` (D-002, EI-003).
   c. `protocol/.agents/contracts/SESSION_LOG.md:Required content`:
      `schema_version` del front matter → `2.0.0` (MAJOR de contrato). Agregar
      a los campos aplicables `- **Execution**: <iteration>` y, cuando el
      heading `## <timestamp>` no sea UTC-normalizado (sin `Z`/`+00:00`), la
      entrada declara `- **Clock**: agent_clock` y se trata como no canónica
      (TM-001); los headings son `event_ts` de la narrativa, no `gate_ts`.

2. **Alcance de `state.json` y runner.**
   a. `protocol/.agents/harness/runner_state.py`: agregar la constante
      `TRANSITION_TRIGGERS = frozenset({"H00","H01","H02","H03","H04","H05",
      "H06","H07","H11"})` (el conjunto de gates de transición core del
      payload, sin D*/H09/H10/H15/S00/REVIEW); en la acción `pass` del CLI,
      rechazar cualquier `--trigger` fuera del conjunto con exit 2 y un
      mensaje que indique que los gates no transicionales (D*, H10, H15, S00,
      REVIEW) se registran solo en `HARNESS_REPORT.md` (D-005, D-103).
      Actualizar el docstring de layout y de CLI: `state.json` registra gates
      de transición y status terminal únicamente; `gates[HXX].timestamp` es
      el `gate_ts` canónico (UTC, TM-002).
   b. En `record_gate_pass` y `record_terminal_state`, normalizar el timestamp
      a sufijo `Z` (`datetime.now(timezone.utc).isoformat().replace("+00:00",
      "Z")`) para cumplir "ISO-8601 con Z" (D-007).
   c. En `detect_bypass`, parsear el `gate_ts` normalizando `Z` → `+00:00`
      antes de `fromisoformat`, y devolver `(suspects, reliable)` donde
      `reliable` es `False` cuando el timestamp no es UTC-normalizado; el
      caller (`main`) imprime "bypass scan not reliable" a stderr en ese caso
      (el scan usa `gate_ts` canónico; si no lo es, se marca no confiable).
      El hook (`hook_gate.py`) no cambia: solo consume el estado persistido.

3. **Declaración canónica en el harness (integración, no duplicación).** En
   `protocol/.agents/harness/INDEX.md`, integrar la declaración del alcance de
   `state.json` que ya existe desde 5.0.0 en §Protocol State and Hook
   Enforcement y §State dimensions (`state.json` = gates de transición;
   ST-002; review gate nunca en `state.json`): extenderla — sin duplicarla ni
   contradecirla — para cerrar el alcance explícitamente (gates de transición
   core H00–H07, H11 + status terminal; D*/H10/H15/S00/REVIEW solo en
   `HARNESS_REPORT.md`) y agregar una subsección `## Execution records`
   autocontenida (inglés, sin referencias a `plans/`), con:
   - Tabla de roles disjuntos: `state.json` = verdad mecánica de gates de
     transición y status; `HARNESS_REPORT.md` = trail de revisión de gates;
     `SESSION_LOG.md` = narrativa de decisiones; `METRICS.md` = observables de
     proceso; Artifacts = objetos durables con lifecycle derivado (ya
     declarado en §State dimensions).
   - Identidad de ejecución: `execution_id = (session_id, iteration)`, sin
     UUIDs nuevos; actor como `(role_id, mode)` sin identidad de instancia
     (D-001, D-004); kernel descrito con metadata (`protocol_version`, `mode`).
   - Semántica temporal: `created_at`, `started_at`/`completed_at`, `event_ts`,
     `gate_ts` (canónico, UTC); orden por `gate_ts` (gates) y por `seq`
     (métricas); timestamps del agente sin reloj con `clock: agent_clock`, no
     canónicos (D-007, TM-001…TM-003).
   - Información mínima para reconstruir una ejecución (los 6 ítems del
     modelo) y la nota D-201: la auditoría post-hoc depende del proyecto
     original; el trail no es autocontenido por requisito.
   - Invariantes EI-001…EI-003, TR-001…TR-005, TM-001…TM-003 y
     OBS-001…OBS-003 redactados inline en inglés, reutilizando el vocabulario
     `clock`/`claim_class` ya presente.

4. **Observabilidad de budget (D-008, OBS-001/OBS-002).**
   a. `protocol/.agents/orchestrators/core/harness/policies/H15-delegation-validity.md:Pre-delegation gate`,
      ítem 4 (sin renumerar el checklist): extender la obligación para exigir
      el registro del evento `context_budget` (`METRICS.md`, §Event catalog)
      con `declared` y `consumed` medidos por la regla de estimación
      (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:2`) para
      toda delegación con `context_budget`, y que sin el par
      declared/consumed la claim de cumplimiento es atestación (OBS-002); el
      registro es `[agent]` con verificación dev (OBS-001).
   b. `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:context_budget`:
      alinear el bloque "Enforcement status: measured" con el pairing: el
      evento `context_budget` se registra junto al evento `delegation` de la
      misma delegación (`iteration`, `phase` y `context_budget` declarado).
   c. `tools/measure_context_budget.py`: agregar `--phase` y `--iteration`
      opcionales que se incluyen en el reporte JSON, para que la salida
      alimente directamente el evento `context_budget`.
   d. `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Registration rules`
      y `:Verifiability classes`: declarar que todo evento lleva `seq` y
      `clock`, los eventos por ejecución llevan `iteration` (incluidos los del
      catálogo `Reuse and cache` — `reuse_event`/`provider_cache_event`), y
      que toda delegación con budget declara `context_budget` en su evento
      `delegation` y está pareada con un evento `context_budget` (OBS-001);
      la clase Verified del par se mantiene. No se modifican las invariantes
      I-ECO-001…I-ECO-006 ni la semántica de los eventos de RFC-74.

5. **Reconciliación dev (D-009, TR-001/TR-002).** En
   `tools/aggregate_metrics.py` (`audit_cross_checks`):
   a. Correlacionar por `(iteration, trigger)` cuando el ENTRY declara
      `iteration` (sesiones `>= 11.0.0`); para sesiones previas sin el campo
      (banda 7.0.0–10.3.0 y anteriores), mantener la correlación actual por
      `trigger` (trazas históricas, RFC-46).
   b. Mantener la bidireccionalidad actual (state.json ⊆ HARNESS siempre;
      HARNESS ⊆ state.json para gates de transición H00–H07/H11 en sesiones
      `>= 4.0.0`) con la nueva correlación por iteración.
   c. Comparar `gate_ts` (`state.json`) con `event_ts` (ENTRY) en pares
      coincidentes: alertar cuando la diferencia absoluta supera 60 segundos y
      el ENTRY no declara `timestamp_divergence.cause` (TR-002). La tolerancia
      de 60 s evita ruido por skew normal dentro de la misma invocación; la
      divergencia mayor sin causa declarada es el caso de reconstrucción
      retroactiva (P18). Actualizar el docstring del módulo.

6. **Checker dev de sesión.** En `tools/check_session_artifacts.py`, agregar
   `RECORD_PROTOCOL = (11, 0, 0)` y aplicar a sesiones `>= 11.0.0`:
   a. ENTRY: `iteration` obligatorio (string numérico) y `clock` obligatorio en
      `{utc, agent_clock}`; `timestamp` validado contra el `clock` (regla ya
      existente) y `timestamp_divergence.cause` no vacío cuando está presente.
   b. METRIC: `seq` obligatorio (entero, estrictamente creciente dentro del
      archivo de la sesión), `clock` obligatorio, `iteration` obligatorio en
      los tipos por ejecución — incluidos `reuse_event` y
      `provider_cache_event` —; `delegation` con `context_budget` numérico
      positivo y `attempt` entero positivo cuando están presentes.
   c. `state.json`: las claves de `gates` deben pertenecer a
      `TRANSITION_TRIGGERS` (alcance, D-005); cada `timestamp` de gate debe ser
      UTC-normalizado (TM-002).
   d. OBS-001: para cada evento `delegation` con `context_budget` declarado,
      debe existir un evento `context_budget` con la misma `phase`/`iteration`
      y `declared` igual; sin el par, se reporta la violación.
   Actualizar el docstring del módulo (guard `>= 11.0.0`; banda legacy
   7.0.0–10.3.0 no re-reportada, RFC-46).

7. **Tests.**
   a. `tests/test_check_session_artifacts.py`: fixtures de sesión `11.0.0` —
      ENTRY sin `iteration`/`clock`, METRIC sin `seq`, `seq` no monotónico,
      `state.json` con gate fuera de alcance (p. ej. `H10`), delegación con
      `context_budget` sin evento pareado (todas deben reportarse); sesiones
      legacy de la banda publicada 7.0.0–10.3.0 equivalentes no deben
      reportarse (RFC-46) — incluir al menos una sesión `10.3.0` y verificar
      que las fixtures ya existentes de 7.0.0/8.0.0/9.0.0 no se ven afectadas
      por el guard nuevo.
   b. `tests/test_aggregate_metrics.py`: `--audit` con `(iteration, trigger)`
      — disparidad por iteración, divergencia de timestamps sin
      `timestamp_divergence` alertada y con causa declarada OK, tolerancia de
      60 s sin alerta; traza legacy 10.3.0 sin `iteration` sigue correlacionada
      por `trigger`.
   c. `tests/test_measure_context_budget.py`: `--phase`/`--iteration` en el
      reporte.
   d. `protocol/.agents/harness/tests/test_runner_state.py`: `pass` con trigger
      no transicional (`H10`, `D01`, `H15`, `REVIEW`) → exit 2; `pass` con
      trigger transicional → exit 0 y timestamp con sufijo `Z`;
      `detect_bypass` con timestamp no canónico → `reliable == False`.

8. **Documentación y versión.**
   - `docs/MIGRATION.md`: nueva sección tras §12, con título
     `## 13. Modelo de registro de ejecución — 11.0.0 (plan 78, RFC-64)`
     (el texto no debe escribirse como cita `ruta:sección` hasta que la
     sección exista): `state.json` limitado a gates de transición H00–H07/H11
     + status; ENTRY con `iteration` y `clock` obligatorios; METRICS con
     `seq`/`iteration`/`clock` (incluidos `reuse_event` y
     `provider_cache_event`) y pairing de `context_budget`; `gate_ts` canónico
     UTC (`Z`); timestamps del agente con `clock: agent_clock` no canónicos;
     `schema_version` 2.0.0 de HARNESS_REPORT/METRICS/SESSION_LOG (MAJOR de
     contrato); trazas históricas bajo semántica previa (RFC-46); ninguna
     acción sobre artefactos de sesión previos.
   - `protocol/.agents/VERSION` → `11.0.0`. En `CHANGELOG.md`, nueva sección
     `## [11.0.0]` (fecha real del corte de la versión al ejecutar) con
     `Added` (identidad de ejecución y event keys, roles de registros,
     `seq`/`iteration` en METRICS incluyendo los eventos reuse/cache del
     catálogo 1.2.0, pairing de `context_budget`), `Changed` (alcance de
     `state.json`, ENTRY con `iteration`/`clock`, `gate_ts` canónico UTC-Z,
     `--audit` con comparación de timestamps, `schema_version` 2.0.0 de los
     contratos de registro), `Removed` (registro de gates no transicionales en
     `state.json`) y `Modelo conceptual` (RFC-64 Accepted), todo referenciando
     `(plan 78, RFC-64)`.

9. **Registro.** En `docs/plans/INDEX.md`, mantener el plan 78 registrado en
   su serie con status `Aprobado para ejecución` (pasa a `Executed` al cerrar
   este plan); la RFC-64 queda `Accepted` con su Amendment Log (registro de la
   aceptación por el plan 103 y entrada de ejecución de este plan al cerrar).
   Agregar la `## Nota de ejecución` al ejecutar y, conforme al DoD vigente
   (`docs/VERSIONING.md:10. Definition of Done`), las secciones
   `## Validation anchor` y `## Checkpoint / cierre` con los gates C-1/C-2/C-3
   antes de derivar `Closed`.

## Criterios de salida

- [ ] El payload declara el alcance de `state.json` (gates de transición
      H00–H07, H11 + status terminal) en `harness/INDEX.md`, integrado con la
      declaración existente (ST-002/§State dimensions) sin duplicación, y
      `runner_state.py` lo hace cumplir mecánicamente (criterio de aceptación
      de la RFC).
- [ ] Los ENTRY y `state.json` comparten event keys: ENTRY con `iteration`
      obligatorio, `state.json` con `(session, iteration, trigger)`, y
      `--audit` correlaciona por `(iteration, trigger)` para sesiones
      `>= 11.0.0` (EI-002, TR-001); las trazas previas sin `iteration` se
      siguen correlacionando por `trigger` (RFC-46).
- [ ] `--audit` es bidireccional y compara timestamps con divergencia
      declarada (`timestamp_divergence.cause`, tolerancia 60 s) (TR-002).
- [ ] Toda delegación con budget registra el par declared/consumed: evento
      `context_budget` pareado con el evento `delegation` (OBS-001); sin el
      par, la claim es atestación (OBS-002) declarada en H15 y el contrato de
      delegación.
- [ ] METRICS con `seq` monótono estricto por sesión y `clock` en todo evento
      (incluidos `reuse_event`/`provider_cache_event`); los timestamps del
      agente sin reloj llevan `clock: agent_clock` y se tratan como no
      canónicos (TM-001); `gate_ts` canónico UTC con `Z` (TM-002); las tres
      lecturas Accepted de la RFC-64 preservadas sin reinterpretación.
- [ ] `schema_version` de HARNESS_REPORT, METRICS (desde 1.2.0) y SESSION_LOG
      pasa a 2.0.0; el catálogo METRICS 1.2.0 queda cubierto por las reglas de
      registro nuevas sin alterar la semántica de RFC-74.
- [ ] `check_session_artifacts.py` aplica los checks nuevos solo a sesiones
      `>= 11.0.0`; las sesiones de la banda 7.0.0–10.3.0 y anteriores no se
      re-reportan (RFC-46); tests de checkers dev y del producto en verde.
- [ ] `docs/MIGRATION.md` tiene la sección 13 con la nota MAJOR `11.0.0`;
      `protocol/.agents/VERSION` = `11.0.0`; changelog `[11.0.0]` con
      `(plan 78, RFC-64)`.
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
python -m pytest tests/ -q --basetemp .pytest_cache\basetemp
```

Adicional, fuera de la batería canónica:

```bash
python -m pytest protocol/.agents/harness/tests/
python tools/aggregate_metrics.py --audit
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
git diff --check
```

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por
diseño; debe quedar verde en `master` tras la promoción.

Juicios manuales: coherencia H13 de las secciones nuevas (la subsección
Execution records de `protocol/.agents/harness/INDEX.md` y la integración con
State dimensions, contratos HARNESS_REPORT/METRICS/SESSION_LOG con
`schema_version` 2.0.0, ítem 4 de H15, bloque `context_budget` del contrato de
delegación); verificación de que la frontera documental se mantiene (el
payload no cita `plans/` ni RFCs); revisión de que ningún gate no transicional
queda registrable en `state.json`; revisión de que los eventos
`reuse_event`/`provider_cache_event` y sus invariantes I-ECO no cambian de
semántica.

## Riesgos

- **RFC-64 ya `Accepted` (plan 103):** la aceptación no ejecuta este plan; la
  vía de autorización completa (RFC-56) queda cerrada por este plan aprobado,
  pero la ejecución exige además la confirmación humana del MAJOR `11.0.0`
  (criterio de entrada).
- **MAJOR 11.0.0:** requiere confirmación explícita del usuario y nota de
  migración (`docs/VERSIONING.md:3. Versionado`); sin confirmación, el plan no
  se ejecuta (criterio de entrada). `6.0.0` queda descartado: no existe tag
  6.0.0 y publicarlo tras 10.3.0 violaría la regla de versión siguiente.
- **`clock` vs `source: agent_clock`:** lectura Accepted por el mantenedor
  (plan 103): el campo `clock` (`utc` | `agent_clock`, vigente desde 4.0.0)
  implementa el marcador de fuente sin renombrar a `source`; este plan
  conserva el contrato existente.
- **Comparación de timestamps:** lectura Accepted (plan 103): tolerancia de
  60 s y divergencia declarada con `timestamp_divergence.cause`; exigir
  igualdad exacta generaría ruido por skew normal dentro de la misma
  invocación.
- **`seq` a nivel sesión:** lectura Accepted (plan 103): secuencia
  estrictamente creciente por sesión para EI-003/TR-004 (satisface la
  restricción por ejecución y es verificable).
- **Catálogo METRICS 1.2.0 (plan 91, RFC-74):** los eventos
  `reuse_event`/`provider_cache_event` y el catálogo `Reuse and cache` de
  `PROTOCOL_METRICS.md` deben quedar cubiertos por `seq`/`iteration`/`clock`;
  no se modifica la semántica de los eventos ni las invariantes I-ECO.
- **Declaración existente de `state.json` (5.0.0, plan 77):** integrar sin
  duplicar ni contradecir ST-002/§State dimensions; la subsección `## Execution
  records` complementa, no reemplaza, la declaración vigente.
- **Trazas históricas (RFC-46):** los checks nuevos aplican solo a sesiones
  `>= 11.0.0`; las de la banda 7.0.0–10.3.0 y anteriores no se re-reportan ni
  se invalidan.
- **Frontera con RFC-65/RFC-67:** no implementar clases de evidencia ni
  lifecycle de conocimiento; el plan solo declara que sin el par
  declared/consumed la claim de budget es atestación (OBS-002).
- **Campos opcionales nuevos:** `timestamp_divergence`, `context_budget` y
  `attempt` en `delegation` son aditivos y compatibles; no hacer obligatorios
  para reportes previos. Los campos obligatorios nuevos (`iteration`, `seq`,
  `clock`) aplican solo a sesiones nuevas (schema 2.0.0; RFC-46).
- **Coherencia estructural:** cambios en contratos pueden romper citas o la
  coherencia taxonómica; correr la batería en cada paso de payload, no solo al
  final.

## Trazabilidad

`ARCHITECTURAL_DECISION_MODEL.md:D5 — Execution Identity` +
`ARCHITECTURAL_DECISION_MODEL.md:D6 — Execution Record / Audit Trail` +
`ARCHITECTURAL_DECISION_MODEL.md:D7 — Temporal Semantics` +
`ARCHITECTURAL_DECISION_MODEL.md:D10 — Observability / Budget` → RFC-64
(Proposal 2026-08-25 → `Accepted` por plan 103, 2026-09-03) → Plan 78
(creado 2026-08-25; rebasado 2026-09-04 contra el estado 10.3.0) →
entregables 1–14.

## Nota de rebase

Registro documental del rebase de este plan contra el estado real del repo
(2026-09-04), previo a su ejecución.

- **Estado factual al rebasar:** branch `dev`; HEAD `dce442a`; working tree
  limpio; `protocol/.agents/VERSION` = `10.3.0` (última versión publicada en
  `master`; sin tag 6.0.0); RFC-64 `Accepted` (plan 103, 2026-09-03); Plan 78
  `Aprobado para ejecución` sin ejecutar. No existe autorización para ejecutar
  ninguna otra Change.
- **Clasificación de esta iteración:** origen/tipo = acción directa del
  mantenedor (rebase pre-ejecución del Plan 78); clase RFC-56 = — (cambio
  docs-only, sin tocar `protocol/.agents/` en esta iteración); Change Level =
  L1 (coordination 0, scope 1 — capa de gobernanza documental DEV —,
  architectural impact 0, release impact 0, duration/complexity 0); dominio =
  `docs/plans/`.
- **Alcance:** actualización exclusiva del artifact Plan 78 y del espejo
  descriptivo en `docs/plans/INDEX.md`. No se ejecuta el plan, no se modifica
  payload/runtime/checkers funcionales/VERSION/METRICS/state.json, no hay
  bump ni tag, no se cierra el plan.
- **Condiciones de la revisión de aceptación (C-3…C-6) incorporadas:**
  - C-3 (versión): objetivo `11.0.0` (no `6.0.0`) en criterio de entrada,
    entregables, pasos y criterios de salida; verificado contra
    `docs/VERSIONING.md:3. Versionado` y los tags de `master` (10.3.0 última
    publicada; 6.0.0 nunca publicada). Clasificación: REQUIRED.
  - C-4 (guard y fixtures): `RECORD_PROTOCOL = (11, 0, 0)`; checks nuevos
    solo para sesiones `>= 11.0.0`; banda legacy 7.0.0–10.3.0 cubierta en
    tests como no re-reportada (RFC-46). Clasificación: REQUIRED.
  - C-5 (METRICS schema 1.2.0): `reuse_event`/`provider_cache_event`
    integrados a las reglas de `seq`/`iteration`/`clock`; contrato 1.2.0 →
    2.0.0; `PROTOCOL_METRICS.md` alineado sin alterar RFC-74.
    Clasificación: REQUIRED.
  - C-6 (MIGRATION y `state.json`): sección de migración nueva 13 tras §12
    (no §8) y redacción del paso 3 como integración con la declaración
    existente de `state.json` (ST-002/§State dimensions), sin duplicación.
    Clasificación: REQUIRED.
  - C-1/C-2 (lecturas Accepted y registro de la aceptación) ya fueron
    resueltas por el plan 103 y quedan como contexto normativo vigente.
- **Otras correcciones de rebase:** rutas legacy del header y del registro
  (`plans/rfc/…`, `plans/INDEX.md`) actualizadas al layout de RFC-69
  (`docs/rfc/…`, `docs/plans/INDEX.md`); referencias a RFC-64 `Proposal`
  reemplazadas por su estado `Accepted` (plan 103); declaración de `Change
  Level` agregada al header conforme al intake vigente (RFC-75 Mecanismo 2);
  `schema_version` 2.0.0 de los contratos de registro especificado conforme a
  `docs/MIGRATION.md` (§2).
- **Validación de esta iteración:** el rebase es preparación documental; no
  registra una validación anclada propia en el plan (los checkers y pytest
  corren como verificación operacional antes del commit). Al ejecutar, el
  plan registrará su `## Validation anchor` y `## Checkpoint / cierre` y
  correrá C-1/C-2/C-3 antes de derivar `Closed` (DoD, `docs/VERSIONING.md:10.
  Definition of Done`).
- **Gate pendiente de la ejecución:** confirmación humana de la clasificación
  MAJOR y de la versión objetivo `11.0.0` + nota de migración (criterio de
  entrada; `docs/VERSIONING.md:3. Versionado`).

## Nota de ejecución

- 2026-09-04 — **Ejecutado el Plan 78 sobre `dev`** (autorización explícita
  del mantenedor: «Execute Plan 78 — RFC-64 Execution Record Model», con
  confirmación del MAJOR `11.0.0`; RFC-64 `Accepted` por plan 103). Estado
  inicial: branch `dev`, HEAD `8f0d339` (rebase), working tree limpio,
  `protocol/.agents/VERSION` = `10.3.0`; batería canónica en verde (checkers
  PASS; pytest `428 passed`).
  Clasificación: origen = ejecución autorizada del plan; clase RFC-56 = A
  (payload); Change Level = L3 (header); dominio = payload + tooling dev +
  tests + docs/versioning.
  Implementación (commit C1 `d94f33a`, contenido validado por V1): contratos
  HARNESS_REPORT/METRICS/SESSION_LOG con `schema_version` 2.0.0 (ENTRY con
  `iteration`/`clock`/`timestamp_divergence`, METRICS con `seq`/`iteration`/
  `clock` incluidos `reuse_event`/`provider_cache_event`, SESSION_LOG con
  `Execution`/`Clock`); `harness/INDEX.md` con alcance integrado de
  `state.json` (ST-005) y subsección `## Execution records`; `runner_state.py`
  con `TRANSITION_TRIGGERS`, rechazo de triggers no transicionales,
  timestamps UTC-`Z` y `detect_bypass` con flag de confiabilidad; H15 +
  contrato de delegación + `PROTOCOL_METRICS.md` con la obligación y el
  pairing de `context_budget`; `aggregate_metrics.py --audit` con correlación
  `(iteration, trigger)` y comparación de timestamps (tolerancia 60 s) para
  sesiones `>= 11.0.0`; `check_session_artifacts.py` con guard
  `RECORD_PROTOCOL = (11, 0, 0)`; `measure_context_budget.py` con
  `--phase`/`--iteration`; tests dev y del producto; MIGRATION §13; VERSION
  → `11.0.0`; CHANGELOG `[11.0.0]`; ancla semántica del runtime
  (`canonical.py PROTOCOL_VERSION`) alineada por `<PLAN-78>:C-1`.
  Registro/cierre: este artifact (nota, anchor V1, checkpoint), espejo en
  `docs/plans/INDEX.md`, Amendment Log de RFC-64 y metadatos de estado de
  ADR-06/07/08/11 + `docs/adr/INDEX.md`; revalidación V2 (batería canónica
  completa + pytest sobre el estado final) y gates C-1/C-2/C-3 sin ANOMALY
  antes de `Closed`; `git diff --check` limpio; commit C2 de registro en
  `dev`. Sin push, sin tag, sin release: versión `11.0.0` queda en `dev`
  hasta la promoción autorizada por el mantenedor.

## Validation anchor

Registrado al ejecutar el Plan 78 (2026-09-04). La validación **V1** corrió
sobre el contenido del commit de contenido C1, **antes** de agregar los
registros de cierre de esta sección (anti-circularidad; precedente Planes
96–103).

- Declared scope: contenido del commit C1 del Plan 78 — contratos
  HARNESS_REPORT/METRICS/SESSION_LOG (schema 2.0.0), `harness/INDEX.md`
  (alcance de `state.json` + `## Execution records`), `runner_state.py`,
  H15-delegation-validity, WORKER_DELEGATION_CONTRACT, PROTOCOL_METRICS,
  `protocol/.agents/VERSION` (11.0.0), `runtime/toolcalls/canonical.py`
  (ancla), `tools/aggregate_metrics.py`, `tools/check_session_artifacts.py`,
  `tools/measure_context_budget.py`, tests dev (3) y del producto
  (`test_runner_state.py`), `docs/MIGRATION.md` (§13), `CHANGELOG.md`
  (`[11.0.0]`) — + batería canónica del repo (checkers dev + pytest) y tests
  del producto sobre ese estado.
- Validation command-set:
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `python -m pytest tests/ -q --basetemp .pytest_cache\basetemp`
  - `python -m pytest protocol/.agents/harness/tests/ -q --basetemp .pytest_cache\basetemp`
  - `git diff --check`
- Effective inputs (repo content): contenido completo del repo en el estado
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`,
  `runtime/` y la raíz; pytest consume `tests/` + `tools/` + `runtime/` +
  `protocol/.agents/harness/tests/`); representado por el State identity
  (tree id).
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación
  en esta ejecución); el consumo por comando se observa de la documentación
  de cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica
  de verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 11.0.0 (versión objetivo del
  plan); pytest ejecutado con basetemp local `.pytest_cache\basetemp` por ACL
  del basetemp `pytest-of-rolda` (ruido ambiental documentado en planes
  96–102); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `3e016ed1ad58ad43deb9d87bae30f8844b98ccf1` (tree id; igual a
    `git write-tree` del estado staged y a `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 19 archivos del commit C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `d1fd0f468a4cb5a2bf0eb2a913176e88e908601dc847540110dbc44f9b1bd12e`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa + pytest sobre el estado final de la ejecución, incluidos los
  registros de cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `d94f33aac69fb10cf197a706ac75d3b18f7406bb` — `feat(protocol):
    implement execution record model (plan 78, RFC-64)` (contenido validado
    por V1).
  - C2 — este commit de registro (`docs(plans): close plan 78 execution
    record model (plan 78, RFC-64)`); su SHA se identifica por el mensaje y el
    árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity
  T1 = `3e016ed1ad58ad43deb9d87bae30f8844b98ccf1`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`3e016ed…`) → **PASS**.
  - Estado final (C2): difiere de C1 únicamente en los registros de cierre
    (este artifact, INDEX de planes, Amendment Log de RFC-64 y metadatos de
    estado de ADR-06/07/08/11 + ADR INDEX); **revalidación V2** (batería
    canónica completa + pytest sobre el contenido final, ejecutada antes del
    commit) → PASS. GC-1 queda satisfecho por revalidación antes de `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); RFC-64 con
  entrada de implementación en su Amendment Log; ADR-06/07/08/11 + ADR INDEX
  con metadatos de estado alineados (sin contenido normativo nuevo); VERSION
  `11.0.0` + changelog `[11.0.0]` + MIGRATION §13; corrección `<PLAN-78>:C-1`
  con revalidación declarada.
- Condición derivada: **`Closed` (version-producing, con release pendiente)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (C1 + C2 en `dev`), `Closed` (condición derivada con checkpoint
  y consistencia), `Released` (no aplica: sin promoción ni tag).

## Findings / Correcciones / Pending

Registros reales de esta ejecución (el plan adopta las reglas del Incremento
2 al cerrar; RFC-75 Mecanismo 15).

### Findings

- `<PLAN-78>:F-1` — estado: `resolved` (2026-09-04; resuelto por la
  corrección `<PLAN-78>:C-1` con evidencia V1/V2 y checkpoint de este
  artifact); estado previo: `open` (registrado durante la ejecución del paso
  8, 2026-09-04); observación: el paso 8 del plan (versión objetivo
  `11.0.0`) no lista `runtime/toolcalls/canonical.py`, pero la invariante de
  anclaje semántico del runtime exige `PROTOCOL_VERSION ==
  protocol/.agents/VERSION` (`tools/check_version_state.py`; RFC-71/G1); sin
  el ajuste, la batería canónica falla tras el bump; clasificación: GAP de
  inventario del plan (corrección mecánica); tipo: execution finding;
  origin: Plan 78 (paso 8); source: ejecución del Plan 78 (2026-09-04);
  evidencia original: `runtime/toolcalls/canonical.py` (constante
  `PROTOCOL_VERSION`) = `"10.3.0"` frente a `protocol/.agents/VERSION` →
  `11.0.0`, invariante de `tools/check_version_state.py`; estado Git
  observado: `dev` @ `8f0d339`, working tree con los cambios del paso 8 sin
  commitear; provenance original: ejecutor del Plan 78 (2026-09-04);
  resolución: actualización mecánica de la constante implementada y
  verificada (`<PLAN-78>:C-1`; `check_version_state` PASS y batería completa
  sobre el estado final, V2).

### Correcciones

- `<PLAN-78>:C-1` — refs origen: `<PLAN-78>:F-1`; origen: Plan 78 (paso 8);
  autorización: ejecución del Plan 78 autorizada por el mantenedor
  («Correcciones menores estrictamente necesarias para completar Plan 78…
  dentro del alcance autorizado»; este registro es FACTUAL/TRACEABILITY, no
  fuente normativa); qué se corrigió: actualización mecánica de
  `PROTOCOL_VERSION = "11.0.0"` en `runtime/toolcalls/canonical.py` (sin
  cambio de comportamiento; la constante declara la versión del protocolo que
  el runtime implementa y debe igualar `protocol/.agents/VERSION`);
  alcance de revalidación (CL-6): invariante versión ↔ changelog ↔ tag y
  ancla runtime (`python tools/check_version_state.py`), batería canónica
  completa y pytest sobre el estado final (V2); evidencia (Git/commit/estado):
  commit C1 `d94f33a` (ancla `11.0.0`), `check_version_state` OK (warning
  esperado de `dev`: sin tag), pytest `445 passed`, checkers canónicos PASS,
  gates C-1/C-2/C-3 sin ANOMALY sobre el estado de cierre; resultado:
  `<PLAN-78>:F-1` `resolved`.

### Pending decisions

- `N/A` (no hay decisiones pendientes de este artifact: la confirmación del
  MAJOR `11.0.0` fue provista por el mantenedor en la autorización de
  ejecución; la promoción/release queda como acción futura del mantenedor,
  no como pending de este plan).
