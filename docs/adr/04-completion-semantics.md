# ADR-04 — Completion Semantics (D3)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D3 (2026-08-25)
**RFC:** [RFC-63](docs/rfc/63-state-and-artifact-lifecycle-model.md) (`Accepted`, plan 77)
**Plan:** [plan 77](docs/plans/77-state-artifact-lifecycle-model.md) (`Executed`)
**Clase de cambio:** MAJOR (semántica del estado terminal; RFC-56)
**Problemas que resuelve:** P9 (CG-01)

## Contexto

P9 muestra sesiones que cierran COMPLETED con gates humanos pendientes ("el gate de
cierre de Fase 2 no puede declararse formal"). Sin semántica de completitud, el
estado terminal no representa las condiciones que afirma y los hooks/reanudación no
pueden operar sobre él (`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).

## Alternativas consideradas

### A — COMPLETED = ejecución terminada (sin verificación)

Simple, pero colisiona con el estado actual (COMPLETED ya exige H06/H07).

### B — COMPLETED = completitud absoluta

Semántica fuerte, pero bloquea los planes con gates humanos y contradice la práctica
confirmada de cerrar tareas con diferidos.

### C — COMPLETED = completitud relativa al alcance confirmado, con diferidos explícitos

COMPLETED significa: máquina core en terminal Y todos los gates en-scope PASS en
state.json Y el Verification Report sin criterios en-scope FAIL/PENDING Y toda
aprobación humana en-scope completada o diferida con confirmación del usuario.

## Decisión

**Opción C.** COMPLETED es completitud relativa al alcance confirmado, con las
cuatro condiciones operacionales del modelo. Los diferidos se registran en
SESSION_BRIEF (confirmación `source: user`, `deferred: true`), en la sección
`Deferred Items` del VERIFICATION_REPORT y, si la gobernanza del proyecto lo define,
en el plan como `Executed (parcial: <qué falta>)`. `approved`, `verified`,
`validated` y `executed` no son sinónimos de COMPLETED: pertenecen a sus
dimensiones (D1/D2) (`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D3`).

## Consecuencias

- El Verification Report gana `Deferred Items` (obligatorio cuando hay diferidos).
- H06 agrega el check de COMPLETED válido.
- La distinción "cierre técnico" vs "cierre de gobernanza" queda explícita.

## Invariantes

- CMP-1: COMPLETED ⇒ todos los gates en-scope PASS en state.json.
- CMP-2: COMPLETED ⇒ ningún criterio en-scope FAIL/PENDING en el reporte.
- CMP-3: todo item diferido tiene confirmación de usuario (SESSION_BRIEF) y aparece
  en `Deferred Items`.
- CMP-4: ningún item diferido se presenta como "completado".

## Relaciones

- Depende de: D1 (dimensiones; ADR-02).
- Formalizada en: RFC-63 (`docs/rfc/63-state-and-artifact-lifecycle-model.md:Decision`),
  plan 77.

## Estado de implementación

RFC-63 `Accepted` (plan 77 `Executed`, 2026-08-25); payload 5.0.0: `Deferred Items`
en VERIFICATION_REPORT, check de COMPLETED en H06 y detección de COMPLETED sin gates
en-scope en `check_session_artifacts.py` para sesiones `>= 5.0.0`.
