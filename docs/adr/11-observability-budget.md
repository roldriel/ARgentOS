# ADR-11 — Observability / Budget (D10)

**Status:** Accepted (decisión registrada; formalización pendiente: RFC-64 `Proposal`, plan 78 gated)
**Fecha:** 2026-08-27
**Decisión original:** D10 (2026-08-25)
**RFC:** [RFC-64](docs/rfc/64-execution-record-model.md) (`Proposal`, plan 78 gated)
**Plan:** [plan 78](docs/plans/78-execution-record-model.md) (`Aprobado para ejecución`, gated)
**Clase de cambio:** MAJOR (contratos de métricas; RFC-56)
**Problemas que resuelve:** P4 (CG-03/CG-02; NBI-1)

## Contexto

P4 muestra claims de budget sin par declared/consumed. Sin separar budget,
measurement, metrics, evidence y audit trail, todo se convierte en evidencia o nada
se mide (`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).
El catálogo de métricas y el evento `context_budget` ya existen (3.25.0); el
problema es el registro, no el concepto.

## Alternativas consideradas

### A — Todo como evidencia (estado actual sin registro)

Cero cambios, pero reproduce P4.

### B — Separación en cuatro capas + registro obligatorio de cumplimiento

Capas: Budget (límite declarado), Measurement (cantidad derivada del payload real),
Metrics (agregados advisory) y Evidence/Audit trail. Regla: una claim de "budget
respetado" exige el evento `context_budget` (declared/consumed) en METRICS; sin el
par, la claim se marca como atestación.

### C — Medición mecánica en runtime

Registro garantizado, pero exige runtime en adoptantes y choca con el modo
declarativo.

## Decisión

**Opción B.** Cuatro capas separadas; el evento `context_budget` es la evidencia de
cumplimiento de budget; las métricas siguen siendo advisory. `session.duration_ms`
se corrige para usar una sola fuente temporal (D7, NBI-1)
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D10`).

## Consecuencias

- Las delegaciones con budget registran `context_budget` (declared/consumed).
- Las claims sin par quedan marcadas como atestación (D4).
- Las métricas no se convierten en gates.

## Invariantes

- OBS-1: toda delegación con `context_budget` tiene evento `context_budget` en
  METRICS.
- OBS-2: una claim de cumplimiento de budget sin par declared/consumed es
  atestación.
- OBS-3: `session.duration_ms` usa una sola fuente temporal.

## Relaciones

- Depende de: D4 (clasificación de la claim; ADR-05), D6/D7 (registro y reloj;
  ADR-07, ADR-08).
- Formalizada en: RFC-64 (`docs/rfc/64-execution-record-model.md:Decision`), plan 78.

## Estado de implementación

Decisión `DECIDED` en el modelo (2026-08-25). RFC-64 `Proposal`, plan 78
`Aprobado para ejecución` gated (Clase A, RFC-56); el ADR registra la decisión, no
habilita cambios de payload. La parte de confianza de métricas ya publicada
(3.25.0/plan 74, RFC-60) no se modifica.
