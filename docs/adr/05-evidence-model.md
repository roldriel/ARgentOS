# ADR-05 — Evidence Model (D4)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D4 (2026-08-25)
**RFC:** [RFC-65](docs/rfc/65-evidence-and-verification-model.md) (`Accepted`, plan 79)
**Plan:** [plan 79](docs/plans/79-evidence-and-verification-model.md) (`Executed`)
**Clase de cambio:** MAJOR (significado de PASS/"verificado"; RFC-56)
**Problemas que resuelve:** P16, P4 (CG-03)

## Contexto

P16 muestra un gate PASS sustentado en "escritos sin abrir sources/" (atestación del
mismo agente); P4 muestra claims de budget sin par declared/consumed. Sin clases de
evidencia, "esto fue verificado" equivale a "el agente dijo que lo verificó"
(`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).

## Alternativas consideradas

### A — Evidencia como texto libre

Estado actual. Cero cambios, pero no hay forma de distinguir atestación de
observación.

### B — Clases mínimas de evidencia + marca de atestación

Cinco clases: `observation`, `measurement`, `attestation`, `assertion`, `reference`,
con reglas mínimas de suficiencia por ítem `[gate]`/`[agent]` y bloque estructurado
`[[evidence]]` con `class`/`claim_id`/`ref`.

### C — Modelo formal completo (ontología de evidencia)

Máximo rigor, pero sobre-ingeniería para el objetivo.

## Decisión

**Opción B.** Se adoptan las cinco clases con las cuatro reglas mínimas. Una
atestación **puede** justificar ítems `[agent]`, pero **nunca** un ítem `[gate]` sin
desviación documentada, y siempre con la marca. Un "verificado" en un reporte exige
al menos una entrada de evidencia con clase distinta de `attestation`; sin ella el
término permitido es "atestado"
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D4`).

## Consecuencias

- Los reportes de verificación distinguen "verificado por evidencia re-ejecutable"
  de "atestado".
- H06 puede chequear mecánicamente que cada criterio PASS tenga evidencia con clase.
- Los ítems `[agent]` con atestación se vuelven visibles para auditoría.

## Invariantes

- EV-1: todo gate PASS tiene por cada ítem `[gate]` evidencia
  `observation`/`measurement`/`reference` (o desviación documentada).
- EV-2: toda `attestation` lleva actor + enunciado + marca.
- EV-3: toda entrada de evidencia tiene `class`, `claim_id` y `ref`.
- EV-4: "verificado" en un reporte ⇒ existe entrada de evidencia con clase distinta
  de `attestation` para ese claim (o se usa "atestado").

## Relaciones

- Depende de: D0 (qué significa "verificado"; ADR-01).
- Formalizada en: RFC-65 (`docs/rfc/65-evidence-and-verification-model.md:Decision`),
  plan 79. D12 (relación artifact/estado/evidencia) depende formalmente de esta
  decisión (ADR-13).

## Estado de implementación

RFC-65 `Accepted` (plan 79 `Executed`, 2026-08-25); payload 7.0.0: bloques
`[[evidence]]` en VERIFICATION_REPORT y HARNESS_REPORT, checks de H06 en
`gate_validator.py`, detección de atestaciones sin marcar en `audit_gates.py`.
