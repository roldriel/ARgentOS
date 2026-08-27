# Plan 64 — Remediación F1-A (modelo de enforcement declarado honestamente)

**Status:** Executed
**Fecha:** 2026-08-14
**RFC:** —
**Clase:** B (rewordings y sección canónica; sin cambio de comportamiento)
**Depende de:** —
**Origen:** `AUDITORIA_SISTEMA.md` F1 (opción A, decisión del usuario
2026-08-14)

## Objetivo

Alinear el lenguaje del payload con el modelo real de enforcement, en tres
capas: **enforced** (caparazón de hooks, fail-open), **reviewed** (gates por
juicio del Orchestrator, trail auto-reportado) y **verified** (checkers de
desarrollo, dev-only). Eliminar las frases que implican machine-gateability en
policies, `HARNESS_REPORT.md` y H13.

## Criterio de entrada

- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `harness/INDEX.md`: sección canónica "Enforcement model" + Purpose alineado.
2. Policies H00–H07, H09–H11, H15, D00, D01, S00, H13: `[gate]` =
   "structurally checkable"; sin "gateable without interpretation".
3. `HARNESS_REPORT.md`: "review trail" auto-reportado.
4. `H13`: nota de checkers dev-only.
5. `protocol/.agents/VERSION` = `3.15.0`; changelog; INDEX; tracker.

## Pasos

1. Editar `.agents/harness/INDEX.md` (Purpose + sección Enforcement model).
2. Rewrite mecánico de las frases en las policies de harness.
3. Editar `.agents/contracts/HARNESS_REPORT.md` y
   `.agents/harness/policies/H13-protocol-taxonomy.md`.
4. Bump `3.15.0`, changelog, INDEX, tracker.

## Criterios de salida

- [ ] Ninguna policy dice que un ítem `[gate]` es machine-gateable.
- [ ] El modelo de tres capas está declarado en `harness/INDEX.md`.
- [ ] Batería canónica en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/
```

## Riesgos

- Bajo: rewordings; los checkers de desarrollo ya cubren la parte estructural.

## Trazabilidad

- `AUDITORIA_SISTEMA.md` F1 (opción A).

## Nota de ejecución

Ejecutado el 2026-08-14. Versión `3.15.0` (MINOR: adición de la sección
Enforcement model + rewordings). Verificación: invariantes OK, citas OK,
estructura OK, taxonomía OK, tests OK; `check_dist_sync` rojo en `dev` por
diseño.
