# ADR-13 — Artifact / State / Evidence Relationship (D12)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D12 (2026-08-25)
**RFC:** [RFC-63](docs/rfc/63-state-and-artifact-lifecycle-model.md) (`Accepted`, plan 77), [RFC-65](docs/rfc/65-evidence-and-verification-model.md) (`Accepted`, plan 79)
**Plan:** [plan 77](docs/plans/77-state-artifact-lifecycle-model.md) (`Executed`), [plan 79](docs/plans/79-evidence-and-verification-model.md) (`Executed`)
**Clase de cambio:** MAJOR (lenguaje de reportes y validador; RFC-56)
**Problemas que resuelve:** P16, P17 (CG-01/CG-03)

## Contexto

P16/P17 muestran artefactos que declaran estados sin sustento y con secciones en
conflicto. La relación entre artefacto y evidencia debe ser un invariante, no una
convención (`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).
La dimensión de evidencia (D4) ya define clases; esta decisión define la relación.

## Alternativas consideradas

### A — El artefacto puede declarar cualquier estado

Estado actual. Cero cambios, pero reproduce P16/P17.

### B — Relaciones mínimas con invariantes

Artifact → Gate (el gate de salida es su transición a `validated`); Gate → Evidence
(cada ítem cita evidencia con clase); Artifact → Evidence (un artefacto declara
"verified"/"validated" solo con Gate State PASS + evidencia asociada); Verification →
Artifact (cada criterio PASS referencia el artefacto y su evidencia); State →
Evidence (ninguna transición terminal se registra sin el gate correspondiente).

### C — Modelo de derivación formal completo

Rigor total, pero sobre-ingeniería.

## Decisión

**Opción B.** Regla central: *un artifact puede declarar "verified" solo con Gate
State PASS y evidencia asociada con clase; sin ella, el término permitido es
"atestado"*. `validated` del lifecycle ⇔ PASS del gate de salida en state.json
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D12`).

## Consecuencias

- Los reportes existentes que usan "verificado" sin evidencia quedan como traza
  histórica; los nuevos deben ajustarse.
- El validador H06/H07 agrega el check de relación.
- La auto-consistencia de secciones (AL-4) se aplica junto con esta relación.

## Invariantes

- REL-1: un artefacto declara "verified" ⇔ Gate State PASS + evidencia con clase
  distinta de `attestation` para el claim (o usa "atestado").
- REL-2: `validated` del lifecycle ⇔ PASS del gate de salida en state.json.
- REL-3: toda entrada de evidencia referencia el artifact y el claim que sustenta.

## Relaciones

- Depende de: D1, D2 (ADR-02, ADR-03) y formalmente de D4 (ADR-05).
- Formalizada en: RFC-63 (relaciones e invariantes; plan 77) con dependencia formal
  de RFC-65 (clases de evidencia; plan 79).

## Estado de implementación

RFC-63 y RFC-65 `Accepted` (planes 77 y 79 `Executed`, 2026-08-25); payload 5.0.0 +
7.0.0: lenguaje verificado/atestado en reportes, check de relación en H06 y
`gate_validator.py`, detección de "verificado" sin evidencia en `audit_gates.py`.
