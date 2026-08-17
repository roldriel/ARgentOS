# Plan 69 — Bloque 0 de la auditoría de sistema 3.1 (quick wins)

**Status:** Executed
**Fecha:** 2026-08-16
**RFC:** —
**Clase:** B (vía plan; los ítems 1 y 2 son correcciones mecánicas consolidadas
en este plan; el ítem 6 alinea metadata semántica de la taxonomía con el
comportamiento ya ejecutado)
**Depende de:** —
**Origen:** `AUDITORIA_SISTEMA_2026-08-16.md` §Plan de remediación por bloques
(Bloque 0, ítems 1–6); autorizado por instrucción directa del usuario el
2026-08-16 (guardar el análisis nuevo y ejecutar el bloque cero).

## Objetivo

Ejecutar el bloque 0 de la auditoría de sistema 3.1: seis quick wins que
eliminan afirmaciones stale o contradictorias del payload y de la
documentación del repo, sin cambio del modelo conceptual:

1. `harness/INDEX.md` declara "Three pure-stdlib Python scripts" pero el
   payload tiene cuatro (`gate_validator.py` quedó fuera del conteo en 3.17.0).
2. El ejemplo de invocación al Discovery Orchestrator en `orchestrator.md`
   muestra `context_budget: 100000`, contradictorio con
   `discovery_context_budget = 32000` de `features.toml`.
3. El header de `plans/INDEX.md` muestra un snapshot stale (3.6.3 / dev 2
   commits adelante) contradictorio con el estado real (3.19.0 en sync).
4. `[Unreleased]` del CHANGELOG contiene claims stale sobre planes ya
   ejecutados.
5. Conteos stale en `docs/AUDITORIA_DOCUMENTACION.md` y `AUDITORIA_SISTEMA.md`.
6. La taxonomía declara productores/consumidores inexactos para
   `INTER_WORKER_MESSAGE.md` y `KB_DISCOVERY_ENTRY.md` (dice INIT; los
   productores reales son los workers por scope).

## Criterio de entrada

- [ ] Batería canónica en verde en `dev` antes de tocar archivos
      (`docs/VERSIONING.md` §4.1).
- [ ] `AUDITORIA_SISTEMA_2026-08-16.md` existe en la raíz con el bloque 0.
- [ ] `dev` en sync con `master` (3.19.0).

## Entregables

1. `protocol/.agents/harness/INDEX.md` — conteo corregido (cuatro scripts).
2. `protocol/.agents/orchestrators/core/roles/orchestrator.md` — literal
   `context_budget` alineado con `features.toml` y nota de fuente.
3. `plans/INDEX.md` — snapshot del header actualizado + registro del plan 69.
4. `CHANGELOG.md` — `[Unreleased]` sin claims stale + sección `[3.20.0]`.
5. `docs/AUDITORIA_DOCUMENTACION.md` y `AUDITORIA_SISTEMA.md` — conteos
   actualizados (145 tests de desarrollo, 64 tests del harness).
6. `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` —
   `produced_by`/`consumed_by` de `INTER_WORKER_MESSAGE.md` y
   `KB_DISCOVERY_ENTRY.md` alineados con el front matter TOML de los contratos.
7. `protocol/.agents/VERSION` — bump a 3.20.0.

## Pasos

1. Corregir el conteo de scripts en `protocol/.agents/harness/INDEX.md`
   §Enforcement model.
2. Corregir el ejemplo de payload en
   `protocol/.agents/orchestrators/core/roles/orchestrator.md` §4.3 Discovery
   Orchestrator Invocation.
3. Actualizar el snapshot del header de `plans/INDEX.md` y registrar el plan 69
   en la sección de la novena serie.
4. Reescribir `[Unreleased]` de `CHANGELOG.md` y agregar `## [3.20.0]`.
5. Actualizar conteos en `docs/AUDITORIA_DOCUMENTACION.md` y
   `AUDITORIA_SISTEMA.md`.
6. Alinear las entidades de contrato `INTER_WORKER_MESSAGE.md` y
   `KB_DISCOVERY_ENTRY.md` en
   `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`.
7. Bump de `protocol/.agents/VERSION` a 3.20.0.

## Criterios de salida

- [ ] La batería canónica de `docs/VERSIONING.md` §4.1 corre en verde
      (`check_dist_sync` roja por diseño en `dev`).
- [ ] `check_plan_citations` resuelve las citas del plan 69.
- [ ] `check_plan_structure` conforma (plan numerado, status válido, sin
      placeholders, registrado en INDEX).
- [ ] `check_taxonomy_coherence` verde con las nuevas listas
      `produced_by`/`consumed_by`.
- [ ] Plan `Executed` con `Nota de ejecución`, INDEX actualizado, changelog
      `[3.20.0]` y `VERSION` bumped.

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

Bajo: los cambios son documentales/de metadata. El único cambio semántico
(ítem 6) alinea la taxonomía con el comportamiento ya ejecutado y declarado en
el front matter TOML de los contratos; si un checker rechazara la lista, se
ajusta sin tocar el modelo.

## Trazabilidad

`AUDITORIA_SISTEMA_2026-08-16.md` (Bloque 0, ítems 1–6) → este plan → ítems
del changelog `[3.20.0]` → commit atómico en `dev`.

## Nota de ejecución

2026-08-16: ejecutado en `dev`. Batería canónica en verde
(`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`,
`check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`
con warnings de dev esperados, 145 tests de desarrollo); ítems 1–6 del bloque 0
aplicados; changelog `[3.20.0]` y `protocol/.agents/VERSION` bumped; INDEX
actualizado. Commit atómico en `dev`.
