# Plan 78 — Modelo de registro de ejecución (RFC-64)

**Status:** Aprobado para ejecución
**Fecha:** 2026-08-25
**RFC:** RFC-64 (`plans/rfc/64-execution-record-model.md`)
**Clase:** A (modelo conceptual: identidad de ejecución, roles de los registros, alcance de `state.json`, semántica temporal y observabilidad de budget; RFC-56)
**Depende de:** plan 76 (4.0.0: vocabulario `clock`/`claim_class` y regla de claims) y plan 77 (5.0.0: dimensiones de estado, lifecycle de artefactos y semántica de COMPLETED); RFC-64 `Accepted` como criterio de entrada
**Origen:** `ARCHITECTURAL_DECISION_MODEL.md:D5 — Execution Identity`, `ARCHITECTURAL_DECISION_MODEL.md:D6 — Execution Record / Audit Trail`, `ARCHITECTURAL_DECISION_MODEL.md:D7 — Temporal Semantics`, `ARCHITECTURAL_DECISION_MODEL.md:D10 — Observability / Budget`; RFC-64 Proposal (2026-08-25).

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

El plan implementa solo lo que la RFC-64 define. Las clases de evidencia y la
regla VERIFIED quedan para la RFC-65; el lifecycle de conocimiento para la
RFC-67; ambos quedan fuera de alcance. El plan 76 ya introdujo el marcador
`clock` (`utc` | `agent_clock`) y la regla de claims que este modelo consume
para declarar la fuente temporal; el plan 77 ya separó las dimensiones de
estado y el lifecycle de artefactos que este modelo referencia como registros
derivados.

## Criterio de entrada

- [ ] RFC-64 en estado `Accepted` y registrada en `plans/INDEX.md` (hoy
      `Proposal`, 2026-08-25: el plan se redacta en paralelo, pero no se
      ejecuta hasta la aceptación; la clase A de RFC-56 exige RFC `Accepted`
      antes de tocar `protocol/.agents/`).
- [ ] Usuario confirma la clasificación MAJOR (`6.0.0`, siguiente a la `5.0.0`
      del plan 77 en `dev`) y la nota de migración (`docs/VERSIONING.md:3. Versionado`).
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos
      de la tabla de Afectados de la RFC existen y las secciones citadas en
      Pasos resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `plans/78-execution-record-model.md` — este plan.
2. `protocol/.agents/harness/INDEX.md` — subsección `## Execution records`
   (roles de los registros, identidad de ejecución, event keys, semántica
   temporal, información mínima de reconstrucción e invariantes EI/TR/TM/OBS
   inline en inglés) y alcance de `state.json` en §Protocol State and Hook
   Enforcement.
3. `protocol/.agents/contracts/HARNESS_REPORT.md` — ENTRY con `iteration`
   obligatorio, `clock` obligatorio, `timestamp` declarado como `event_ts` y
   `timestamp_divergence` opcional para divergencias declaradas con causa.
4. `protocol/.agents/contracts/METRICS.md` — `seq` obligatorio en todo evento,
   `iteration` obligatorio en los eventos por ejecución, `clock` obligatorio,
   y `delegation` con `context_budget` (declarado) y `attempt` opcionales.
5. `protocol/.agents/contracts/SESSION_LOG.md` — campo `Execution` por entrada
   y marcador de reloj cuando el heading no es UTC-normalizado.
6. `protocol/.agents/harness/runner_state.py` — `TRANSITION_TRIGGERS`, rechazo
   de triggers fuera de alcance, `gate_ts` canónico UTC con sufijo `Z` y
   `detect_bypass` con flag de confiabilidad.
7. `protocol/.agents/orchestrators/core/harness/policies/H15-delegation-validity.md` —
   ítem 4 del §Pre-delegation gate con la obligación de registrar el evento
   `context_budget` (declared/consumed) al delegar con budget.
8. `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md` — alineación del
   bloque `context_budget` con el pairing delegación ↔ evento `context_budget`.
9. `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` — reglas de
   registro (`seq`, `iteration`, `clock`) y pairing de budget en
   §Registration rules y §Verifiability classes.
10. `tools/aggregate_metrics.py` — `--audit` correlacionado por
    `(iteration, trigger)` y comparación de timestamps con tolerancia de 60 s
    y divergencia declarada.
11. `tools/check_session_artifacts.py` — checks para sesiones `>= 6.0.0`:
    alcance de `state.json`, `iteration`/`clock` en ENTRY, `seq`/`iteration`/
    `clock` en METRIC, `seq` monotónico y pairing de `context_budget`.
12. `tools/measure_context_budget.py` — `--phase`/`--iteration` opcionales en
    el reporte JSON.
13. Tests de los checkers dev (`tests/test_check_session_artifacts.py`,
    `tests/test_aggregate_metrics.py`, `tests/test_measure_context_budget.py`)
    y del producto (`protocol/.agents/harness/tests/test_runner_state.py`).
14. `docs/MIGRATION.md` — sección nueva tras §7 con la nota MAJOR `6.0.0`;
    `protocol/.agents/VERSION` → `6.0.0`; `CHANGELOG.md` con `## [6.0.0]`;
    `plans/INDEX.md` — plan 78 registrado en su serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el payload y git
   que existen los archivos citados y que las secciones referenciadas en los
   pasos 1–8 resuelven: `protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement`,
   `protocol/.agents/harness/INDEX.md:State dimensions` y
   `protocol/.agents/harness/INDEX.md:Enforcement boundaries`;
   `protocol/.agents/contracts/HARNESS_REPORT.md:Required structure`;
   `protocol/.agents/contracts/METRICS.md:Event catalog`;
   `protocol/.agents/contracts/SESSION_LOG.md:Required content`;
   `protocol/.agents/orchestrators/core/harness/policies/H15-delegation-validity.md:Pre-delegation gate`;
   `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:context_budget`;
   `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Registration rules`;
   `docs/MIGRATION.md:7. Modelo de estado y lifecycle de artefactos`. Confirmar
   RFC-64 `Accepted` y la clasificación MAJOR (criterios de entrada).

1. **Contratos de registro (event keys y fuente temporal).**
   a. `protocol/.agents/contracts/HARNESS_REPORT.md:Required structure`:
      agregar a la lista de campos del ENTRY `- Execution: <iteration>` (el
      folder numérico de la iteración; `execution_id` compartido con
      `state.json`). En el bloque JSON del comentario `ENTRY`, `iteration`
      pasa a ser obligatorio (string con el folder numérico) y `clock` pasa a
      ser obligatorio (`utc` | `agent_clock`); declarar que `timestamp` es el
      `event_ts` del trail (momento de registro) y que el `gate_ts` canónico
      vive en `state.json`; agregar el campo opcional
      `"timestamp_divergence": {"cause": "<reason>"}` para cuando `event_ts`
      difiere del `gate_ts` del mismo gate (TR-002). El event key del gate es
      `(session_uuid, iteration, trigger)` y es la clave compartida con
      `state.json` (EI-002, TR-001).
   b. `protocol/.agents/contracts/METRICS.md:Event catalog`: `seq` (entero,
      monotónico estricto por sesión) y `clock` (`utc` | `agent_clock`)
      obligatorios en todo evento; `iteration` obligatorio en los eventos por
      ejecución (`state_transition`, `reviewer_retry`, `failure`, `delegation`,
      `skill_override`, `flag_evidence`, `context_budget`,
      `context_candidates`, `discovery_consent`); `session_start` es de nivel
      sesión y no lleva `iteration`. En `delegation`, agregar `context_budget`
      opcional (el budget declarado del payload, número finito positivo) y
      `attempt` opcional (ordinal 1-based del intento de delegación, D-003).
      El event key de métricas es `(session_uuid, iteration, seq)` (D-002,
      EI-003).
   c. `protocol/.agents/contracts/SESSION_LOG.md:Required content`: agregar a
      los campos aplicables `- **Execution**: <iteration>` y, cuando el heading
      `## <timestamp>` no sea UTC-normalizado (sin `Z`/`+00:00`), la entrada
      declara `- **Clock**: agent_clock` y se trata como no canónica (TM-001);
      los headings son `event_ts` de la narrativa, no `gate_ts`.

2. **Alcance de `state.json` y runner.**
   a. `protocol/.agents/harness/runner_state.py`: agregar la constante
      `TRANSITION_TRIGGERS = frozenset({"H00","H01","H02","H03","H04","H05",
      "H06","H07","H11"})`; en la acción `pass` del CLI, rechazar cualquier
      `--trigger` fuera del conjunto con exit 2 y un mensaje que indique que
      los gates no transicionales (D*, H10, H15, S00, REVIEW) se registran solo
      en `HARNESS_REPORT.md` (D-005, D-103). Actualizar el docstring de layout
      y de CLI: `state.json` registra gates de transición y status terminal
      únicamente; `gates[HXX].timestamp` es el `gate_ts` canónico (UTC,
      TM-002).
   b. En `record_gate_pass` y `record_terminal_state`, normalizar el timestamp
      a sufijo `Z` (`datetime.now(timezone.utc).isoformat().replace("+00:00",
      "Z")`) para cumplir "ISO-8601 con Z" (D-007).
   c. En `detect_bypass`, parsear el `gate_ts` normalizando `Z` → `+00:00`
      antes de `fromisoformat`, y devolver `(suspects, reliable)` donde
      `reliable` es `False` cuando el timestamp no es UTC-normalizado; el
      caller (`main`) imprime "bypass scan not reliable" a stderr en ese caso
      (el scan usa `gate_ts` canónico; si no lo es, se marca no confiable).
      El hook (`hook_gate.py`) no cambia: solo consume el estado persistido.

3. **Declaración canónica en el harness.** En
   `protocol/.agents/harness/INDEX.md`, bajo §Protocol State and Hook
   Enforcement, declarar el alcance de `state.json` explícitamente (gates de
   transición H00–H07, H11 + status terminal; D*/H10/H15/S00/REVIEW solo en
   `HARNESS_REPORT.md`) y agregar una subsección `## Execution records`
   autocontenida (inglés, sin referencias a `plans/`), con:
   - Tabla de roles disjuntos: `state.json` = verdad mecánica de gates de
     transición y status; `HARNESS_REPORT.md` = trail de revisión de gates;
     `SESSION_LOG.md` = narrativa de decisiones; `METRICS.md` = observables de
     proceso; Artifacts = objetos durables con lifecycle derivado (RFC-63,
     ya declarado en §State dimensions).
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
      ítem 4: agregar la obligación de registrar el evento `context_budget`
      (`METRICS.md`, §Event catalog) con `declared` y `consumed` medidos por la
      regla de estimación (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:2`)
      para toda delegación con `context_budget`, y que sin el par
      declared/consumed la claim de cumplimiento es atestación (OBS-002); el
      registro es `[agent]` con verificación dev (OBS-001).
   b. `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:context_budget`:
      alinear el bloque "Enforcement status: measured" con el pairing: el
      evento `context_budget` se registra junto al evento `delegation` de la
      misma delegación (`iteration`, `phase` y `context_budget` declarado).
   c. `tools/measure_context_budget.py`: agregar `--phase` y `--iteration`
      opcionales que se incluyen en el reporte JSON, para que la salida alimente
      directamente el evento `context_budget`.
   d. `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Registration rules`
      y `:Verifiability classes`: declarar que todo evento lleva `seq` y
      `clock`, los eventos por ejecución llevan `iteration`, y que toda
      delegación con budget declara `context_budget` en su evento `delegation`
      y está pareada con un evento `context_budget` (OBS-001); la clase
      Verified del par se mantiene.

5. **Reconciliación dev (D-009, TR-001/TR-002).** En
   `tools/aggregate_metrics.py` (`audit_cross_checks`):
   a. Correlacionar por `(iteration, trigger)` cuando el ENTRY declara
      `iteration`; para sesiones previas sin el campo, mantener la correlación
      actual por `trigger` (trazas históricas, RFC-46).
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
   `RECORD_PROTOCOL = (6, 0, 0)` y aplicar a sesiones `>= 6.0.0`:
   a. ENTRY: `iteration` obligatorio (string numérico) y `clock` obligatorio en
      `{utc, agent_clock}`; `timestamp` validado contra el `clock` (regla ya
      existente) y `timestamp_divergence.cause` no vacío cuando está presente.
   b. METRIC: `seq` obligatorio (entero, estrictamente creciente dentro del
      archivo de la sesión), `clock` obligatorio, `iteration` obligatorio en
      los tipos por ejecución; `delegation` con `context_budget` numérico
      positivo y `attempt` entero positivo cuando están presentes.
   c. `state.json`: las claves de `gates` deben pertenecer a
      `TRANSITION_TRIGGERS` (alcance, D-005); cada `timestamp` de gate debe ser
      UTC-normalizado (TM-002).
   d. OBS-001: para cada evento `delegation` con `context_budget` declarado,
      debe existir un evento `context_budget` con la misma `phase`/`iteration`
      y `declared` igual; sin el par, se reporta la violación.
   Actualizar el docstring del módulo.

7. **Tests.**
   a. `tests/test_check_session_artifacts.py`: fixtures de sesión `6.0.0` —
      ENTRY sin `iteration`/`clock`, METRIC sin `seq`, `seq` no monotónico,
      `state.json` con gate fuera de alcance (p. ej. `H10`), delegación con
      `context_budget` sin evento pareado (todas deben reportarse); sesión
      `5.0.0` equivalente no debe reportarse (RFC-46).
   b. `tests/test_aggregate_metrics.py`: `--audit` con `(iteration, trigger)`
      — disparidad por iteración, divergencia de timestamps sin
      `timestamp_divergence` alertada y con causa declarada OK, tolerancia de
      60 s sin alerta.
   c. `tests/test_measure_context_budget.py`: `--phase`/`--iteration` en el
      reporte.
   d. `protocol/.agents/harness/tests/test_runner_state.py`: `pass` con trigger
      no transicional (`H10`, `D01`, `H15`, `REVIEW`) → exit 2; `pass` con
      trigger transicional → exit 0 y timestamp con sufijo `Z`;
      `detect_bypass` con timestamp no canónico → `reliable == False`.

8. **Documentación y versión.**
   - `docs/MIGRATION.md`: nueva sección tras §7, "## 8. Modelo de registro de
     ejecución — 6.0.0 (plan 78, RFC-64)": `state.json` limitado a gates de
     transición H00–H07/H11 + status; ENTRY con `iteration` y `clock`
     obligatorios; METRICS con `seq`/`iteration`/`clock` y pairing de
     `context_budget`; `gate_ts` canónico UTC (`Z`); timestamps del agente con
     `clock: agent_clock` no canónicos; trazas históricas bajo semántica previa
     (RFC-46); ninguna acción sobre artefactos de sesión previos.
   - `protocol/.agents/VERSION` → `6.0.0`. En `CHANGELOG.md`, nueva sección
     `## [6.0.0] — 2026-08-25` con `Added` (identidad de ejecución y event
     keys, roles de registros, `seq`/`iteration` en METRICS, pairing de
     `context_budget`), `Changed` (alcance de `state.json`, ENTRY con
     `iteration`/`clock`, `gate_ts` canónico UTC-Z, `--audit` con comparación
     de timestamps), `Removed` (registro de gates no transicionales en
     `state.json`) y `Modelo conceptual` (RFC-64 Accepted), todo referenciando
     `(plan 78, RFC-64)`.

9. **Registro.** En `plans/INDEX.md`, registrar el plan 78 en su serie con
   status `Aprobado para ejecución` (pasa a `Executed` al cerrar este plan); la
   RFC-64 queda `Accepted` en el commit de aceptación previo y su Amendment Log
   registra la fecha y el plan. Agregar la `## Nota de ejecución` al ejecutar.

## Criterios de salida

- [ ] El payload declara el alcance de `state.json` (gates de transición
      H00–H07, H11 + status terminal) en `harness/INDEX.md` y `runner_state.py`
      lo hace cumplir mecánicamente (criterio de aceptación de la RFC).
- [ ] Los ENTRY y `state.json` comparten event keys: ENTRY con `iteration`
      obligatorio, `state.json` con `(session, iteration, trigger)`, y
      `--audit` correlaciona por `(iteration, trigger)` (EI-002, TR-001).
- [ ] `--audit` es bidireccional y compara timestamps con divergencia
      declarada (`timestamp_divergence.cause`, tolerancia 60 s) (TR-002).
- [ ] Toda delegación con budget registra el par declared/consumed: evento
      `context_budget` pareado con el evento `delegation` (OBS-001); sin el par,
      la claim es atestación (OBS-002) declarada en H15 y el contrato de
      delegación.
- [ ] METRICS con `seq` monotónico y `clock` en todo evento; los timestamps del
      agente sin reloj llevan `clock: agent_clock` y se tratan como no
      canónicos (TM-001); `gate_ts` canónico UTC con `Z` (TM-002).
- [ ] `check_session_artifacts.py` aplica los checks nuevos solo a sesiones
      `>= 6.0.0`; las sesiones previas no se re-reportan (RFC-46); tests de
      checkers dev y del producto en verde.
- [ ] `docs/MIGRATION.md` tiene la sección 8 con la nota MAJOR `6.0.0`;
      `protocol/.agents/VERSION` = `6.0.0`; changelog `[6.0.0]` con
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
python -m pytest tests/
```

Adicional, fuera de la batería canónica:

```bash
python -m pytest protocol/.agents/harness/tests/
python tools/aggregate_metrics.py --audit
```

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por
diseño; debe quedar verde en `master` tras la promoción.

Juicios manuales: coherencia H13 de las secciones nuevas (la subsección
Execution records de `protocol/.agents/harness/INDEX.md`, contratos
HARNESS_REPORT/METRICS/SESSION_LOG, ítem 4 de H15, bloque `context_budget` del
contrato de delegación); verificación de que la frontera documental se
mantiene (el payload no cita `plans/` ni RFCs); revisión de que ningún gate no
transicional queda registrable en `state.json`.

## Riesgos

- **RFC-64 `Proposal`:** el plan se redacta en paralelo, pero no se ejecuta
  hasta la aceptación; la clase A de RFC-56 lo exige antes de tocar
  `protocol/.agents/`.
- **MAJOR 6.0.0:** requiere confirmación explícita del usuario y nota de
  migración (`docs/VERSIONING.md:3. Versionado`); sin confirmación, el plan no
  se ejecuta (criterio de entrada).
- **`clock` vs `source: agent_clock`:** la RFC-64 nombra el marcador
  `source: agent_clock`; el payload ya usa el campo `clock` (`utc` |
  `agent_clock`) desde 4.0.0 (plan 76). Este plan conserva `clock` y lo declara
  como la implementación del marcador de fuente; renombrar a `source` sería
  churn de contratos sin cambio de semántica. Confirmar esa lectura con el
  mantenedor al aceptar la RFC.
- **Comparación de timestamps:** `event_ts` (ENTRY) y `gate_ts` (state.json)
  se escriben en momentos distintos de la misma invocación; exigir igualdad
  exacta generaría ruido. El plan define tolerancia de 60 s y divergencia
  declarada para el resto; es una lectura operacional de TR-002 a confirmar.
- **`seq` a nivel sesión:** el modelo dice "monotónico dentro de la ejecución";
  el plan lo implementa como secuencia estrictamente creciente a nivel sesión
  (satisface la restricción por ejecución y es verificable). Confirmar con el
  mantenedor.
- **Trazas históricas (RFC-46):** los checks nuevos aplican solo a sesiones
  `>= 6.0.0`; las previas no se re-reportan ni se invalidan.
- **Frontera con RFC-65/RFC-67:** no implementar clases de evidencia ni
  lifecycle de conocimiento; el plan solo declara que sin el par
  declared/consumed la claim de budget es atestación (OBS-002).
- **Campos opcionales nuevos:** `timestamp_divergence`, `context_budget` y
  `attempt` en `delegation` son aditivos y compatibles; no hacer obligatorios
  para reportes previos.
- **Coherencia estructural:** cambios en contratos pueden romper citas o la
  coherencia taxonómica; correr la batería en cada paso de payload, no solo al
  final.

## Trazabilidad

`ARCHITECTURAL_DECISION_MODEL.md:D5 — Execution Identity` +
`ARCHITECTURAL_DECISION_MODEL.md:D6 — Execution Record / Audit Trail` +
`ARCHITECTURAL_DECISION_MODEL.md:D7 — Temporal Semantics` +
`ARCHITECTURAL_DECISION_MODEL.md:D10 — Observability / Budget` → RFC-64
(Proposal 2026-08-25; `Accepted` como criterio de entrada) → Plan 78 →
entregables 1–14.
