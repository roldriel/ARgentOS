# ADR-14 — Implementation Priority (D13)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D13 (2026-08-25)
**RFC:** [RFC-62](docs/rfc/62-guarantee-model-and-enforcement-boundaries.md) … [RFC-68](docs/rfc/68-architecture-evolution-workflow.md) (serie derivada)
**Plan:** [plan 76](docs/plans/76-guarantee-model-enforcement-boundaries.md) … [plan 82](docs/plans/82-architecture-evolution-workflow.md) (serie ejecutada)
**Clase de cambio:** — (decisión de secuencia; sin RFC propia)
**Problemas que resuelve:** todos (meta)

## Contexto

Sin un orden por dependencias directas, la implementación de las decisiones D0–D12
acumularía parches sobre un modelo aún indefinido. La primera RFC debía habilitar la
mayor cantidad de checks mecánicos con el menor cambio conceptual
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D13`).

## Alternativas consideradas

### A — Orden por severidad

Atacar primero lo más visible (P8/P3), pero cristaliza modelos indefinidos sin
semántica de estado/evidencia previa.

### B — Orden por dependencias

Cadena conceptual: D1→D2→D3 (estado/lifecycle); D0→D4→D12 (garantías/evidencia);
D5→D6→D7 (registro); D11 depende de D0+D4+D6; D8 independiente; D9 depende de D6;
D10 depende de D4+D6. Primera RFC: RFC-B (D1+D2+D3).

### C — Todo en una RFC

Un solo cambio, pero inmanejable (MAJOR gigante).

## Decisión

**Opción B.** Orden de redacción e implementación por dependencias: RFC-B
(D1+D2+D3) primero, luego RFC-A (D0+D11), RFC-D (D4), RFC-C (D5+D6+D7+D10), RFC-E
(D8, independiente) y RFC-F (D9, última)
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D13`).

## Consecuencias

- El orden de redacción de RFCs quedó fijado por dependencias, no por severidad.
- RFC-B pudo redactarse sin esperar a D4/D6.
- La serie resultante (RFCs 62–68, planes 76–82) ejecutó la secuencia con RFC-62/63
  en paralelo y el workflow de evolución arquitectónica (RFC-68) como cierre.

## Invariantes

- PR-1: ninguna RFC se redacta antes que las decisiones de las que depende.
- PR-2: la implementación de un check mecánico espera a la RFC que define su
  semántica.

## Relaciones

- Depende de: todas las anteriores (D0–D12; ADR-01…ADR-13).
- Formalizada en: — (decisión de secuencia); la serie RFC-62…68 / planes 76–82 es su
  materialización.

## Estado de implementación

Secuencia ejecutada por los planes 76–82 (2026-08-25…27): RFC-62…63 y 65…68
`Accepted` con sus planes `Executed`; RFC-64 `Proposal` con plan 78
`Aprobado para ejecución` gated. El backfill ADR (plan 83) cierra la conversión de
las decisiones D0–D13 en ADRs individuales.
