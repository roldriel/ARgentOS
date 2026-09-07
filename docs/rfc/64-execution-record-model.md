# RFC-64 — Execution Record Model

**Status:** Accepted (plan 103, 2026-09-03)
**Fecha:** 2026-08-25
**Serie:** Arquitectura post-auditoría (25 ago 2026)
**Origen:** `ARCHITECTURAL_DECISION_MODEL.md:D5 — Execution Identity`, `ARCHITECTURAL_DECISION_MODEL.md:D6 — Execution Record / Audit Trail`, `ARCHITECTURAL_DECISION_MODEL.md:D7 — Temporal Semantics`, `ARCHITECTURAL_DECISION_MODEL.md:D10 — Observability / Budget`
**Pregunta:** ¿Cuál es la unidad canónica de "algo ocurrió", cómo se registra una ejecución y cómo se reconstruye sin Event Sourcing?
**Afectados:** protocol/.agents/contracts/HARNESS_REPORT.md, SESSION_LOG.md, METRICS.md; documentación de state.json; protocol/.agents/harness/runner_state.py, hook_gate.py; tools/aggregate_metrics.py, check_session_artifacts.py, measure_context_budget.py

## Status

ACCEPTED

Aceptada el 2026-09-03 por decisión humana del mantenedor (RFC-64 = ACCEPT,
plan 103). La aceptación incorpora tres lecturas de implementación que forman
parte de la decisión: (1) `clock` implementa la fuente `agent_clock` — no
renombrar `clock` a `source`, conservando el contrato existente; (2) `seq`
estrictamente monótono por sesión para EI-003/TR-004; (3) TR-002 con tolerancia
de 60 segundos y divergencias que deben registrar `timestamp_divergence.cause`.
La aceptación NO autoriza la ejecución del plan 78 (implementación pendiente;
Clase A, RFC-56).

## Summary

ARgentOS define la identidad de ejecución por composición (`session_id`, `execution_id =
session_id/iteration`, event keys por trigger o por seq) sin agregar UUIDs nuevos, asigna roles
disjuntos a los cuatro registros (state.json, HARNESS_REPORT, SESSION_LOG, METRICS), declara el
alcance de state.json (gates de transición core: H00–H07, H11), establece UTC como reloj canónico
con fuente declarada, y define checks de reconciliación bidireccional y de timestamps. No introduce
Event Sourcing.

## Motivation

- Problems: P3, P15, P18, P11, P1, P10, P4; CG-02
  (`ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`,
  `ARCHITECTURAL_PROBLEM_MODEL.md:7. Conceptual Gaps`).
- Decisions: D5, D6, D7, D10 (`ARCHITECTURAL_DECISION_MODEL.md:D5 — Execution Identity`,
  `ARCHITECTURAL_DECISION_MODEL.md:D6 — Execution Record / Audit Trail`,
  `ARCHITECTURAL_DECISION_MODEL.md:D7 — Temporal Semantics`,
  `ARCHITECTURAL_DECISION_MODEL.md:D10 — Observability / Budget`).

BeaconRBX demuestra que los timestamps de state.json y HARNESS_REPORT divergen en el 100 % de los
gates con doble registro (P3), que el alcance de state.json es ambiguo y puede faltar H07 (P15), que
un gate puede reconstruirse retroactivamente (P18) y que eventos obligatorios de budget nunca se
registran (P4).

## Context

`state.json` es el único registro mecánico, escrito por `runner_state.py` con reloj UTC, y el
`harness/INDEX.md` lo declara "canonical source" del "protocol state" con "gates passed with
timestamps" sin excluir D*/H10/H15
(`protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement`). El tool dev
`aggregate_metrics.py` declara en su docstring que la dirección inversa no se marca porque H15
"legitimately lack[s] a state.json record". Los contratos exigen ISO-8601 pero no fijan reloj.

## Decision

ARgentOS MUST:

- D-001: Definir la identidad de ejecución por composición: `execution_id = (session_id, iteration)`;
  no agregar UUIDs de ejecución ni de evento.
- D-002: Correlacionar eventos de gate por `(execution_id, trigger)` y eventos de METRICS por
  `(execution_id, seq)`.
- D-003: Correlacionar delegaciones por `(execution_id, phase, attempt#)`.
- D-004: Registrar el actor como `(role_id, mode)`; no persistir identidad de instancia de worker.
- D-005: Limitar el alcance de state.json a los gates de transición core (H00–H07, H11); D*/H10/H15/
  S00 se registran solo en HARNESS_REPORT.
- D-006: Declarar roles disjuntos: state.json = verdad mecánica de gates de transición y status;
  HARNESS_REPORT = trail de revisión de gates; SESSION_LOG = narrativa de decisiones; METRICS =
  observables de proceso.
- D-007: Usar UTC (ISO-8601 con Z) como reloj canónico; cuando el agente escribe timestamps sin
  reloj disponible, marcar `source: agent_clock` y tratarlos como no canónicos.
- D-008: Registrar el evento `context_budget` (declared/consumed) para toda delegación con budget;
  sin el par, la claim de cumplimiento es atestación (RFC-65).
- D-009: Detectar inconsistencias con checks bidireccionales (state.json ⇄ HARNESS) y comparación de
  timestamps.

ARgentOS MUST NOT:

- D-101: Introducir Event Sourcing como mecanismo de registro.
- D-102: Usar timestamps como mecanismo de correlación primaria (se usan event keys).
- D-103: Pretender que state.json es "toda" la verdad de la ejecución.

ARgentOS SHOULD:

- D-201: Documentar que la auditoría post-hoc depende del proyecto original (el trail no es
  autocontenido por requisito).

## Scope

Cubre: identidad de sesión/ejecución/evento, roles de los cuatro registros, alcance de state.json,
semántica temporal, orden, detección de divergencias, información mínima para reconstrucción y capa
de observabilidad/budget.

## Non-Goals

- No define clases de evidencia (RFC-65).
- No define el conocimiento (RFC-67).
- No introduce un kernel de ejecución obligatorio.

## Terminology

- **Session:** contenedor canónico identificado por UUID (carpeta en `.project/`).
- **Execution:** unidad de ejecución = una iteración (una petición de usuario);
  `execution_id = (session_id, iteration)`.
- **Event:** unidad de "algo ocurrió", identificada por `(execution_id, event_type, key)`.
- **Event key:** `trigger` para gates; `seq` para métricas.
- **Correlation key:** `(execution_id, trigger)` o `(execution_id, phase, attempt#)`.
- **Actor:** `(role_id, mode)`; sin identidad de instancia.
- **Kernel:** no se modela como entidad; el runtime se describe con metadata
  (`protocol_version`, `mode`).

## Model

### Roles de los registros

| Registro | Rol | Fuente | Alcance |
|---|---|---|---|
| state.json | verdad mecánica del estado del protocolo | runner_state (UTC) | gates de transición H00–H07, H11 + status terminal |
| HARNESS_REPORT | trail de revisión de gates | orquestador (auto-reportado) | toda invocación de gate (ENTRY) |
| SESSION_LOG | narrativa de decisiones y eventos no-gate | orquestador (append-only) | version + decisiones + correcciones |
| METRICS | observables de proceso | orquestador (auto-reportado) | eventos catalogados con `seq` |
| Artifacts | objetos durables con lifecycle derivado (RFC-63) | writer + derivación | evidencia referenciada por path + hash |

```mermaid
flowchart LR
    Execution[execution_id] --> Gates[Gate events (trigger)]
    Execution --> MetricsEvents[Metrics events (seq)]
    Gates --> StateJson[state.json: PASS/FAIL/SKIP + status]
    Gates --> Harness[HARNESS_REPORT: checks + evidencia]
    MetricsEvents --> Metrics[METRICS: catalogados]
    Execution --> Log[SESSION_LOG: narrativa]
    Harness -. correlación por (execution, trigger) .-> StateJson
    Metrics -. correlación por (execution, seq) .-> Execution
```

### Semántica temporal

- `created_at`: creación del artefacto.
- `started_at` / `completed_at`: ventana de la ejecución.
- `event_ts`: momento de registro del evento.
- `gate_ts`: momento del PASS en state.json (canónico, UTC).
- Orden dentro de una ejecución: por `gate_ts` (gates) y por `seq` (métricas).
- Timestamps del agente sin reloj: `source: agent_clock`, no canónicos.

### Información mínima para reconstruir una ejecución

1. `session_id` + `protocol_version` + `mode`.
2. `execution_id` (iteración).
3. Registros de gates con resultado, evidencia (clase+ref) y `gate_ts`.
4. Hashes de artefactos citados como evidencia.
5. Status terminal y diferidos (RFC-63).
6. Eventos METRICS con `seq`.

### Detección de divergencias

Checks dev-only (y opcionales stdlib en el payload):

1. state.json ⊆ HARNESS y HARNESS ⊆ state.json para gates de transición.
2. `gate_ts` igual o divergencia declarada con causa.
3. Presencia de los cuatro registros y de `protocol_version`.
4. `seq` monotónico en METRICS.
5. Presencia del evento `context_budget` cuando hay budget declarado.

## Invariants

```text
EI-001:
Todo evento registrado tiene un event key derivable.

EI-002:
Un gate PASS en state.json y su ENTRY en HARNESS comparten el mismo
(execution_id, trigger).

EI-003:
Los eventos METRICS tienen seq monotónico dentro de la ejecución.

TR-001:
Todo gate de transición PASS existe en state.json y en HARNESS (bidireccional).

TR-002:
Los timestamps del mismo gate coinciden o declaran divergencia con causa.

TR-003:
Toda sesión tiene los cuatro registros y protocol_version.

TR-004:
Los eventos METRICS tienen seq monotónico.

TR-005:
La reconstrucción de una ejecución usa event keys, no timestamps, como correlación.

TM-001:
Todo timestamp del protocolo es UTC o lleva source: agent_clock.

TM-002:
gate_ts de state.json es canónico (runtime).

TM-003:
La correlación de eventos usa event keys, nunca timestamps.

OBS-001:
Toda delegación con context_budget tiene evento context_budget en METRICS.

OBS-002:
Una claim de cumplimiento de budget sin par declared/consumed es atestación.

OBS-003:
session.duration_ms usa una sola fuente temporal.
```

## Alternativas consideradas

- **Event Sourcing (log único renderizado):** se descarta por exigir runtime en adoptantes, romper
  el modo declarativo y ser sobre-ingeniería para el objetivo.
- **Mantener registros sin invariantes:** reproduce P3/P15.
- **No hacer nada:** se descarta.

## Impacto en el protocolo

- Contratos HARNESS_REPORT/METRICS/SESSION_LOG: campos de event key, `seq`, `source` de timestamp.
- `runner_state.py`: registro del event key y del alcance de gates de transición.
- `aggregate_metrics.py --audit`: bidireccional y con comparación de timestamps.
- `check_session_artifacts.py`: presencia de registros y version.
- `measure_context_budget.py` + H15: registro obligatorio de `context_budget`.
- `hook_gate.py`: bypass scan usa `gate_ts` canónico; si es no canónico, el scan se marca no
  confiable.
- Compatibilidad: MAJOR (semántica de state.json y de timestamps); nota en `docs/MIGRATION.md`.
- Deja de ser válido: la afirmación de que state.json cubre "todos" los gates.

## Criterios de aceptación

- [ ] El payload declara el alcance de state.json (gates de transición H00–H07, H11).
- [ ] Los ENTRY y state.json comparten event keys.
- [ ] `--audit` es bidireccional y compara timestamps.
- [ ] Toda delegación con budget registra `context_budget`.
- [ ] Los timestamps del agente llevan `source` cuando no hay reloj.

## Amendment Log

- 2026-08-25 — Creación.
- 2026-09-03 — Aceptada (plan 103): la RFC-64 queda formalizada como modelo
  aceptado de identidad de ejecución por composición (`execution_id =
  (session_id, iteration)`), roles disjuntos de los cuatro registros
  (state.json, HARNESS_REPORT, SESSION_LOG, METRICS), alcance de `state.json`
  (gates de transición H00–H07, H11 + status terminal), semántica temporal UTC
  con fuente declarada, correlación por event keys y observabilidad de budget
  (invariantes EI-001…EI-003, TR-001…TR-005, TM-001…TM-003, OBS-001…OBS-003).
  Decisión humana del mantenedor (2026-09-03, RFC-64 = ACCEPT) con tres
  lecturas de implementación que forman parte de la decisión: (1) `clock`
  implementa la fuente `agent_clock` — no renombrar `clock` a `source`,
  conservando el contrato existente de RFC-64; (2) `seq` estrictamente monótono
  por sesión para EI-003/TR-004; (3) TR-002 con tolerancia de 60 segundos y
  divergencias que deben registrar `timestamp_divergence.cause`. Cambio
  docs-only: sin impacto en `protocol/.agents/`, sin `VERSION` bump ni tag
  (RFC-69). NO autoriza la ejecución del plan 78: permanece `Aprobado para
  ejecución` sin ejecutar (Clase A, RFC-56; la aceptación de la RFC no habilita
  por sí sola modificar el payload). Condiciones conocidas para la futura
  ejecución del plan 78, preservadas como contexto normativo y NO ejecutadas:
  objetivo de versión 11.0.0 (no 6.0.0); actualizar el guard del checker y los
  fixtures legacy 7.0.0–10.3.0; integrar METRICS schema 1.2.0, incluyendo
  `reuse_event` y `provider_cache_event`; integrar la declaración de
  `state.json` en lugar de duplicarla; resolver las condiciones C3–C6
  identificadas en la revisión.
- 2026-09-04 — Implementada (plan 78, versión `11.0.0`; `Closed` en `dev`,
  release pendiente). El payload materializa el modelo: alcance de `state.json`
  limitado a gates de transición H00–H07/H11 + status terminal con enforcement
  mecánico en `runner_state.py` (`TRANSITION_TRIGGERS`; timestamps UTC con
  `Z`; `detect_bypass` con flag de confiabilidad); sección `## Execution
  records` e integración del alcance en `harness/INDEX.md` (ST-005); contratos
  HARNESS_REPORT/METRICS/SESSION_LOG con `schema_version` 2.0.0 (ENTRY con
  `iteration`/`clock` obligatorios y `timestamp_divergence.cause`; METRICS con
  `seq`/`iteration`/`clock` en todo evento, incluidos `reuse_event` y
  `provider_cache_event`, y `delegation` con `context_budget`/`attempt`;
  SESSION_LOG con `Execution` y marcador `Clock`); pairing obligatorio de
  `context_budget` en H15, contrato de delegación y `PROTOCOL_METRICS.md`;
  `aggregate_metrics.py --audit` con correlación `(iteration, trigger)` y
  tolerancia de 60 s (TR-002) para sesiones `>= 11.0.0`;
  `check_session_artifacts.py` con guard `>= 11.0.0` (banda legacy
  7.0.0–10.3.0 no re-reportada, RFC-46); `measure_context_budget.py` con
  `--phase`/`--iteration`; `docs/MIGRATION.md` §13; `VERSION` `11.0.0` y
  changelog `[11.0.0]`. Las tres lecturas Accepted se preservan sin
  reinterpretación. Corrección registrada `<PLAN-78>:C-1` (ancla semántica
  `PROTOCOL_VERSION` del runtime alineada a `11.0.0`). Validado con la batería
  canónica (checkers PASS), pytest (`445 passed`), tests del harness del
  producto (`109 passed`) y gates C-1/C-2/C-3 sin ANOMALY. Sin push ni tag.
