# Plan 66 — Validador estructural opcional del harness (F1-B/C, RFC-57)

**Status:** Executed
**Fecha:** 2026-08-15
**RFC:** RFC-57 (`plans/rfc/57-harness-structural-validator.md`)
**Clase:** A (código del payload; respaldo RFC-57 `Accepted`)
**Depende de:** plan 64 (F1-A)
**Origen:** `AUDITORIA_SISTEMA.md` F1 (opción C, decisión del usuario 2026-08-15)

## Objetivo

Implementar el validador estructural opcional del harness en el payload, como
soporte mecánico de los ítems `[gate]`, sin cambiar el modelo de gates (el
juicio del Orchestrator sigue siendo el árbitro).

## Criterio de entrada

- [ ] RFC-57 `Accepted`.
- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `.agents/harness/gate_validator.py` (stdlib pura; triggers H00–H07, H09–H11
   y D00).
2. `.agents/harness/tests/test_gate_validator.py`.
3. `harness/INDEX.md`: Enforcement model y How the Harness Works mencionan el
   validador opcional.
4. `PYTHON_DEPENDENCIES.md` y `docs/ADOPTION.md`: cuatro scripts del payload.
5. `protocol/.agents/VERSION` = `3.17.0`; changelog; INDEX; tracker.

## Pasos

1. Implementar `gate_validator.py` (checks estructurales por trigger).
2. Agregar tests del harness.
3. Actualizar docs (Enforcement model, PYTHON_DEPENDENCIES, ADOPTION).
4. Bump `3.17.0`, changelog, INDEX, tracker.

## Criterios de salida

- [ ] `gate_validator.py --list` muestra los triggers soportados.
- [ ] Los tests del harness cubren PASS/FAIL de secciones, TOML, enums, citas,
      EARS y rubricas.
- [ ] El modelo de gates (juicio del Orchestrator) no cambia.
- [ ] Batería canónica en verde (incluye tests del harness).

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

- Bajo: el validador es opcional y fail-open; no cambia la semántica de los
  gates ni el modo declarativo.

## Trazabilidad

- RFC-57 → este plan → `.agents/harness/gate_validator.py`.

## Nota de ejecución

Ejecutado el 2026-08-15. Versión `3.17.0` (MINOR: adición compatible de
soporte mecánico opcional). Verificación: invariantes OK, citas OK, estructura
OK, taxonomía OK, tests OK; `check_dist_sync` verde tras la promoción.
