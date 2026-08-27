# ADR-12 — Enforcement Boundaries (D11)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D11 (2026-08-25)
**RFC:** [RFC-62](docs/rfc/62-guarantee-model-and-enforcement-boundaries.md) (`Accepted`, plan 76), [RFC-66](docs/rfc/66-authorization-and-capability-model.md) (`Accepted`, plan 80)
**Plan:** [plan 76](docs/plans/76-guarantee-model-enforcement-boundaries.md) (`Executed`), [plan 80](docs/plans/80-authorization-and-capability-model.md) (`Executed`)
**Clase de cambio:** MAJOR (matriz de enforcement; RFC-56)
**Problemas que resuelve:** P1, P3, P4, P10, P15, P16, P18 (RC-01)

## Contexto

D0 define las garantías; D11 las conecta con la capa que las verifica, cerrando
RC-01 de forma operativa: dónde termina el juicio del agente y dónde empieza el
enforcement mecánico (`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).
El modo declarativo no requiere runtime; los hooks son fail-open por contrato.

## Alternativas consideradas

### A — Matriz sin cambios (todo juzgado por el agente)

Cero cambios, pero reproduce los problemas de enforcement.

### B — Matriz explícita de verificación por garantía

Matriz por capa (agente / harness / runtime / externo / humano) con reglas de
frontera: lo mecánicamente comprobable se verifica por Runtime/External cuando
existe; lo semántico es juicio del agente con checks estructurales de apoyo; toda
celda vacía significa "no aplica", no "sin control".

### C — Mover todo lo posible a Runtime

Máximo enforcement, pero rompe el modo declarativo.

## Decisión

**Opción B.** Se adopta la matriz como frontera operativa. El juicio del agente
permanece donde la celda dice Agent/Harness; el enforcement mecánico queda limitado
a Runtime/External y es opcional en modo declarativo. En single-instance, la
independencia de verificación se declara como atestación
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D11`).

## Consecuencias

- Los checkers dev implementan las celdas External.
- El payload documenta la matriz (sección de enforcement).
- Las claims de garantía citan su capa de verificación.

## Invariantes

- ENF-1: ninguna garantía etiquetada "mecánica" depende de juicio del agente.
- ENF-2: en modo declarativo, toda garantía verificable se declara y se verifica
  post-hoc por dev tool o se marca atestación.
- ENF-3: los hooks siguen fail-open; la matriz no los declara como control absoluto.

## Relaciones

- Depende de: D0, D4, D6 (ADR-01, ADR-05, ADR-07).
- Formalizada en: RFC-62 (plan 76, matriz y catálogo) y RFC-66 (plan 80, frontera de
  autorización y efectos) — caso real many-to-many de la matriz
  `D# ↔ ADR ↔ RFC ↔ plan`.

## Estado de implementación

RFC-62 `Accepted` (plan 76 `Executed`, 2026-08-25; payload 4.0.0) con el catálogo y
la matriz; RFC-66 `Accepted` (plan 80 `Executed`, 2026-08-25; payload 8.0.0) con la
frontera de efectos. Celdas External implementadas en `check_session_artifacts.py`,
`aggregate_metrics.py --audit` y `audit_gates.py`.
