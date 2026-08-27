# Plan 67 — Remediación B-6 (soporte estructural de H15 en el runner)

**Status:** Executed
**Fecha:** 2026-08-15
**RFC:** —
**Clase:** B (adición compatible de subcomandos de validación; sin cambio de
comportamiento de los subcomandos existentes)
**Depende de:** —
**Origen:** Backlog B-6 (fricción F-08, `plans/INDEX.md`); `AUDITORIA_SISTEMA.md`
punto 2

## Objetivo

Cerrar el último ítem del backlog evidenciado: dar soporte mecánico de schema
al gate H15 con subcomandos del runner (`validate-delegation` y
`validate-return`), que antes requería importar el módulo a mano.

## Criterio de entrada

- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `runner_state.py`: acciones `validate-delegation` y `validate-return`
   (`--input <json>` o `-` para stdin).
2. Tests del harness para ambos subcomandos.
3. `harness/INDEX.md`: nota de soporte mecánico de H15.
4. `protocol/.agents/VERSION` = `3.18.0`; changelog; INDEX; tracker.

## Pasos

1. Implementar `validate_delegation`/`validate_return` y las acciones CLI en
   `.agents/harness/runner_state.py`.
2. Agregar tests en `.agents/harness/tests/test_runner_state.py`.
3. Editar `.agents/harness/INDEX.md` (sección H15).
4. Bump `3.18.0`, changelog, INDEX, tracker.

## Criterios de salida

- [ ] `validate-delegation` valida campos requeridos, `profile` (enum),
      `input_artifacts` (lista) y `context_budget` (finito positivo).
- [ ] `validate-return` valida campos requeridos, listas y prefijos de clase
      en `deviations`.
- [ ] El gate H15 sigue siendo juicio del Orchestrator (soporte, no
      enforcement).
- [ ] Batería canónica en verde (incluye tests del harness).

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/
```

## Riesgos

- Bajo: adición compatible; los subcomandos existentes no cambian.

## Trazabilidad

- Backlog B-6 (fricción F-08) → este plan → `runner_state.py`.

## Nota de ejecución

Ejecutado el 2026-08-15. Versión `3.18.0` (MINOR: adición compatible).
Verificación: invariantes OK, citas OK, estructura OK, tests OK.
