# Plan 61 — Remediación P1.2 (dominios de `produced_by` y `profile`)

**Status:** Executed
**Fecha:** 2026-08-14
**RFC:** —
**Clase:** B (normalización documental compatible y definición de dominio; sin cambio de significado)
**Depende de:** plan 60, Nivel 4 (checkers)
**Origen:** `AUDITORIA_SISTEMA.md` P1.2; contradicción §18.9

## Objetivo

Definir y normalizar el dominio de valores de `produced_by` en el front matter
TOML de los contratos y de `profile` en el front matter de workflows, y hacerlo
machine-checkable con el checker de coherencia taxonómica.

## Criterio de entrada

- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `PROTOCOL_HEALTH.md` ítem 3: `produced_by` usa nombres canónicos de la
   taxonomía (actor, `role_id` o `worker_id`); los estados solo viven en el
   bloque YAML del taxonomy.
2. Contratos normalizados: `KNOWLEDGE_INDEX.md` y `PROJECT_README.md`
   (`argentos_system_agent` → `system_agent`); `KB_DISCOVERY_ENTRY.md`
   (estados → roles de workers).
3. Checker: validación de `produced_by` (contratos), `profile` (workflows) y
   catálogo de perfiles ↔ taxonomía.
4. `protocol/.agents/VERSION` = `3.12.0`; changelog; INDEX; tracker.

## Pasos

1. Editar `.agents/standards/runtime/PROTOCOL_HEALTH.md` (ítem 3): regla de
   dominio de `produced_by`.
2. Normalizar los tres contratos
   (`.agents/contracts/KNOWLEDGE_INDEX.md`,
   `.agents/contracts/PROJECT_README.md`,
   `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`).
3. Extender `tools/check_taxonomy_coherence.py` y sus tests.
4. Bump `3.12.0`, changelog, INDEX, tracker.

## Criterios de salida

- [ ] `produced_by` de todos los contratos usa nombres canónicos.
- [ ] El checker valida `produced_by`/`profile`/catálogo de perfiles.
- [ ] Batería canónica en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

## Riesgos

- Bajo: normalización de metadata; el health check solo exige presencia del
  campo, así que ningún adoptante se rompe.

## Trazabilidad

- `AUDITORIA_SISTEMA.md` P1.2 y contradicción §18.9.

## Nota de ejecución

Ejecutado el 2026-08-14. Versión `3.12.0` (MINOR: normalización compatible de
metadata + regla de dominio). Verificación: invariantes OK, citas OK,
estructura OK, taxonomía OK, tests OK; `check_dist_sync` rojo en `dev` por
diseño.
