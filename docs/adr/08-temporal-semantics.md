# ADR-08 — Temporal Semantics (D7)

**Status:** Accepted (decisión registrada; formalización pendiente: RFC-64 `Proposal`, plan 78 gated)
**Fecha:** 2026-08-27
**Decisión original:** D7 (2026-08-25)
**RFC:** [RFC-64](docs/rfc/64-execution-record-model.md) (`Proposal`, plan 78 gated)
**Plan:** [plan 78](docs/plans/78-execution-record-model.md) (`Aprobado para ejecución`, gated)
**Clase de cambio:** MAJOR (semántica temporal de registros; RFC-56)
**Problemas que resuelve:** P3 (CG-02)

## Contexto

P3 demuestra timestamps divergentes entre registros (hora local etiquetada como UTC,
tiempos estimados). Sin semántica temporal, la causalidad de la traza y el bypass
scan post-H04 son incorrectos
(`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).

## Alternativas consideradas

### A — Timestamps libres

Estado actual. Cero cambios, pero reproduce P3.

### B — UTC canónico + fuente declarada + reconciliación

Todo timestamp del protocolo es UTC (ISO-8601 con Z); los escritos por
runtime/runner_state son canónicos; cuando el agente escribe sin reloj disponible
debe marcar `source: agent_clock` (no canónico). Semánticas por campo
(`created_at`, `started_at`/`completed_at`, `event_ts`, `gate_ts`); la correlación
cruzada usa event keys, no timestamps. Sin secuenciador global.

### C — Secuenciador global

Orden total mecánico, pero exige runtime, rompe el modo declarativo y es innecesario
con event keys.

## Decisión

**Opción B.** UTC canónico, fuente declarada, sin secuenciador global. El bypass
scan post-H04 usa `gate_ts` canónico; si es no canónico, el scan se marca como no
confiable. `session.duration_ms` deja de mezclar relojes (NBI-1)
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D7`).

## Consecuencias

- Los timestamps escritos por el agente sin reloj quedan marcados y son tratados
  como no canónicos.
- La causalidad de la traza es reconstruible con `gate_ts` de state.json.
- Las herramientas de reconciliación comparan tiempos y declaran divergencias.

## Invariantes

- TM-1: todo timestamp del protocolo es UTC o lleva `source: agent_clock`.
- TM-2: `gate_ts` de state.json es canónico (runtime).
- TM-3: la correlación de eventos usa event keys, nunca timestamps.

## Relaciones

- Depende de: D5, D6 (ADR-06, ADR-07).
- Formalizada en: RFC-64 (`docs/rfc/64-execution-record-model.md:Decision`), plan 78.

## Estado de implementación

Decisión `DECIDED` en el modelo (2026-08-25). RFC-64 `Proposal`, plan 78
`Aprobado para ejecución` gated (Clase A, RFC-56); el ADR registra la decisión, no
habilita cambios de payload.
