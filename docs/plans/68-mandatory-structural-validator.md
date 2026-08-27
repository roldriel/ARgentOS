# Plan 68 — Remediación F1-B (validador estructural obligatorio)

**Status:** Executed
**Fecha:** 2026-08-15
**RFC:** RFC-58 (`plans/rfc/58-mandatory-structural-validator.md`)
**Clase:** A (semántica de gates; respaldo RFC-58 `Accepted`)
**Depende de:** plan 66 (RFC-57)
**Origen:** `AUDITORIA_SISTEMA.md` F1 (opción B, decisión del usuario 2026-08-15)

## Objetivo

Convertir el validador estructural en obligatorio para los triggers
soportados: un FAIL estructural bloquea el PASS del gate salvo desviación
documentada, sin tocar el fail-open de los hooks ni los ítems `[agent]`.

## Criterio de entrada

- [ ] RFC-58 `Accepted`.
- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. Policies H00–H07, H09–H11 y D00: MUST invocar `gate_validator.py` antes
   del PASS.
2. `harness/INDEX.md`: Enforcement model (layer 2) y How the Harness Works
   actualizados (obligatorio para triggers soportados).
3. Docstring de `gate_validator.py` actualizado.
4. `protocol/.agents/VERSION` = `3.19.0`; changelog; INDEX; tracker.

## Pasos

1. Editar las 12 policies soportadas (bulk insert tras `## Decision
   Criteria`).
2. Editar `harness/INDEX.md` y `gate_validator.py` (docstring).
3. Bump `3.19.0`, changelog, INDEX, tracker.

## Criterios de salida

- [ ] Ninguna policy soportada permite juzgar PASS sin el validador.
- [ ] El modelo de enforcement distingue: obligatorio a nivel de gate, fail-open
      a nivel de hooks.
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

- Bajo: el validador ya está probado; el cambio es de proceso (MUST), no de
  infraestructura.

## Trazabilidad

- RFC-58 → este plan → policies + Enforcement model.

## Nota de ejecución

Ejecutado el 2026-08-15. Versión `3.19.0` (MINOR: cambio de proceso
compatible). Verificación: invariantes OK, citas OK, estructura OK, tests OK.
