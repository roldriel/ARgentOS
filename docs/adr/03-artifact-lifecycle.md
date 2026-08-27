# ADR-03 — Artifact Lifecycle (D2)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D2 (2026-08-25)
**RFC:** [RFC-63](docs/rfc/63-state-and-artifact-lifecycle-model.md) (`Accepted`, plan 77)
**Plan:** [plan 77](docs/plans/77-state-artifact-lifecycle-model.md) (`Executed`)
**Clase de cambio:** MAJOR (contratos de artefactos; RFC-56)
**Problemas que resuelve:** P2, P17 (CG-01)

## Contexto

P2 y P17 muestran artefactos con `status="draft"`, `approved=false` y secciones
contradictorias mientras los gates registran PASS. El lifecycle actual es un campo
de texto sin reglas y sin verificación
(`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).

## Alternativas consideradas

### A — Lifecycle completo con 8 estados manuales

draft/validated/approved/executed/verified/superseded/rejected/archived. Cubre los
términos observados, pero vuelve a mezclar dimensiones y reproduce P2.

### B — Lifecycle mínimo derivado (3 estados + 2 propiedades)

Estados: `draft`, `validated`, `superseded`; propiedades: `archived` (ubicación) y
`rejected` (evento de corrección). Las transiciones se derivan del registro de
gates; el artefacto no duplica hechos con campos manuales.

### C — Sin lifecycle (el artefacto es un snapshot)

Mínimo, pero deja los campos sin significado.

## Decisión

**Opción B.** El Artifact Lifecycle tiene 3 estados derivados (`draft`, `validated`,
`superseded`), 2 eventos (`corrected`, `gate_failed`) y 2 propiedades (`archived`,
`rejected`). `approved` no es estado del artefacto: es la decisión del Plan Decision
del EXECUTION_PLAN registrada en el Gate State de H04. `verified` no es estado del
artefacto: es un valor de la Verification State derivada, válido solo con evidencia
(D4/D12). Los campos manuales `status`/`approved`/`validation.complete` y la
sección `state` se retiran o redefinen como metadata de solo lectura derivada
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D2`).

## Consecuencias

- Los artefactos existentes con campos manuales quedan como traza histórica bajo la
  semántica vieja (RFC-46); los nuevos siguen el lifecycle derivado.
- Los checkers pueden verificar: "todo artefacto con gate de salida PASS debe estar
  `validated`".
- La auto-consistencia interna (P17) pasa a ser un check estructural.

## Invariantes

- AL-1: el estado del artefacto es derivado; nunca escrito a mano.
- AL-2: `validated` ⇔ el gate de salida tiene PASS en state.json.
- AL-3: un artefacto `superseded` no se consume como entrada de fases posteriores.
- AL-4: secciones en conflicto dentro de un artefacto = FAIL estructural.

## Relaciones

- Depende de: D1 (dimensiones; ADR-02).
- Formalizada en: RFC-63 (`docs/rfc/63-state-and-artifact-lifecycle-model.md:Decision`),
  plan 77, con nota MAJOR en `docs/MIGRATION.md`.

## Estado de implementación

RFC-63 `Accepted` (plan 77 `Executed`, 2026-08-25); payload 5.0.0: retiro de campos
manuales de los siete contratos de artefactos (`schema_version` 2.0.0), checks de
coherencia en `gate_validator.py` y detección de campos manuales en
`check_session_artifacts.py` para sesiones `>= 5.0.0`.
