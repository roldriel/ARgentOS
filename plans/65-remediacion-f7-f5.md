# Plan 65 — Remediación F7-A (evidencia de flags) y F5-A (determinismo de contexto)

**Status:** Executed
**Fecha:** 2026-08-14
**RFC:** —
**Clase:** B (declaraciones canónicas y procedimiento documentado; sin cambio
de comportamiento)
**Depende de:** plan 64 (F1-A), Nivel 4 (agregación de métricas)
**Origen:** `AUDITORIA_SISTEMA.md` F7 y F5 (opción A)

## Objetivo

1. **F7:** documentar canónicamente el procedimiento de evidencia de flags
   (expected / evidenced / unevidenced) y declarar la agregación de métricas
   como mecanismo; la "unevidenced compliance" pasa a ser detectable.
2. **F5:** declarar el modelo de determinismo de contexto (juicio con
   criterios ordenados; determinismo procedimental, no machine-enforced),
   coherente con el budget advisory (P2.1).

## Criterio de entrada

- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `standards/INDEX.md`: sección "Compliance evidence (canonical procedure)".
2. `features.toml`: puntero al procedimiento canónico.
3. `PROTOCOL_METRICS.md`: nota de la agregación mecánica dev-only.
4. `standards/context/CONTEXT.md`: sección "Determinism model".
5. `protocol/.agents/VERSION` = `3.16.0`; changelog; INDEX; tracker.

## Pasos

1. Editar `.agents/standards/INDEX.md` (procedimiento canónico y descripción
   de `CONTEXT.md`).
2. Editar `.agents/features.toml` (header).
3. Editar `.agents/standards/runtime/PROTOCOL_METRICS.md` (§Aggregation).
4. Editar `.agents/standards/context/CONTEXT.md` (Determinism model).
5. Bump `3.16.0`, changelog, INDEX, tracker.

## Criterios de salida

- [ ] El procedimiento de evidencia de flags es canónico y el join
      expected/evidenced/unevidenced queda definido.
- [ ] El modelo de determinismo de contexto está declarado.
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

- Bajo: declaraciones y procedimiento; sin cambio de comportamiento.

## Trazabilidad

- `AUDITORIA_SISTEMA.md` F7 y F5 (opción A).

## Nota de ejecución

Ejecutado el 2026-08-14. Versión `3.16.0` (MINOR). Verificación: invariantes
OK, citas OK, estructura OK, taxonomía OK, tests OK; `check_dist_sync` rojo en
`dev` por diseño.
