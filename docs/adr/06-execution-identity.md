# ADR-06 — Execution Identity (D5)

**Status:** Accepted (decisión registrada; formalización por RFC-64 `Accepted` (plan 103, 2026-09-03); implementación materializada en 11.0.0 por plan 78 (2026-09-04))
**Fecha:** 2026-08-27
**Decisión original:** D5 (2026-08-25)
**RFC:** [RFC-64](docs/rfc/64-execution-record-model.md) (`Accepted` (plan 103, 2026-09-03); implementada en 11.0.0 por plan 78)
**Plan:** [plan 78](docs/plans/78-execution-record-model.md) (`Executed`, 2026-09-04; cierre en `dev`, release pendiente)
**Clase de cambio:** MAJOR (contratos de registros; RFC-56)
**Problemas que resuelve:** P3, P15, P18 (CG-02)

## Contexto

CG-02 agrupa P3, P15, P18 y P11 bajo la ausencia de identidad de eventos y de una
fuente canónica. Sin una unidad de "ocurrencia", los registros no pueden
correlacionarse ni reconstruirse
(`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:3. Problem Inventory`).

## Alternativas consideradas

### A — Solo session_id

Estado actual. No permite correlacionar eventos dentro de una iteración.

### B — Identidad mínima por composición

`execution_id = (session_id, iteration)`; `event key = (execution_id, trigger)` para
gates; `event seq = (execution_id, seq)` para métricas; `delegation_id =
(execution_id, phase, attempt#)`; `actor = (role_id, mode)`. Sin UUIDs nuevos y
funciona sin runtime (los keys derivan de la estructura de carpetas).

### C — UUID por evento

Identidad global única, pero sin función real adicional y exige runtime.

## Decisión

**Opción B.** La unidad canónica de "algo ocurrió" es el **evento**, identificado por
composición: `(execution_id, event_type, key)` con `key` = `trigger` (gates) o `seq`
(métricas). No se agregan UUIDs nuevos; el actor se registra como `(role_id, mode)`
y la instancia de worker no se persiste
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D5`).

## Consecuencias

- HARNESS ENTRY y state.json comparten el key `(execution_id, trigger)`; METRICS
  usan `(execution_id, seq)`.
- La reanudación identifica el "último evento" sin ambigüedad.
- El `kernel` no se modela como entidad; el runtime se describe con metadata
  (`protocol_version`, `mode`), no con identidad.

## Invariantes

- EI-1: todo evento registrado tiene un event key derivable.
- EI-2: un gate PASS en state.json y su ENTRY en HARNESS comparten el mismo
  `(execution_id, trigger)`.
- EI-3: los eventos METRICS tienen `seq` monotónico dentro de la ejecución.

## Relaciones

- Depende de: — (independiente de D0–D4).
- Formalizada en: RFC-64 (`docs/rfc/64-execution-record-model.md:Decision`), plan 78.
  Comparte RFC con D6/D7/D10 (ADR-07, ADR-08, ADR-11).

## Estado de implementación

Decisión `DECIDED` en el modelo (2026-08-25). RFC-64 `Accepted` (plan 103,
2026-09-03); implementación materializada en `11.0.0` por el plan 78
(2026-09-04, `Executed`/`Closed` en `dev`, release pendiente de promoción).
El ADR registra la decisión; no habilita cambios de payload (RFC-56).
