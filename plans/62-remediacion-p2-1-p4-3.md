# Plan 62 — Remediación P2.1 (budget advisory) y P4.3 (schema de contratos)

**Status:** Executed
**Fecha:** 2026-08-14
**RFC:** —
**Clase:** B (mejoras documentales compatibles y metadata aditiva; justificación en Objetivo)
**Depende de:** plan 61 (P1.2)
**Origen:** `AUDITORIA_SISTEMA.md` P2.1 y P4.3

## Objetivo

1. **P2.1:** declarar explícitamente que el Context Budget materializado
   (`context_budget`) es **advisory**: el protocolo no lo mide ni lo trunca
   mecánicamente; el cumplimiento se registra por el evento de métricas
   `context_budget`, nunca por un enforcement. Justificación de clase:
   secciones aclaratorias, sin cambio de significado.
2. **P4.3:** versionar los esquemas de contrato con `schema_version` (semver)
   en el front matter TOML, con regla machine-checkable en el checker de
   coherencia taxonómica y nota de migración en `MIGRATION.md`. Justificación
   de clase: adición compatible de metadata (los artefactos válidos previos
   siguen siendo válidos; el health check ya exige el front matter), por lo
   que se clasifica B y no A.

## Criterio de entrada

- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `WORKER_DELEGATION_CONTRACT.md` §`context_budget`: estado de enforcement
   advisory.
2. `BUDGET_MATERIALIZATION.md`: sección "Enforcement status".
3. `.agents/standards/context/CONTEXT.md` §3: nota advisory.
4. `PROTOCOL_HEALTH.md` ítem 3: `schema_version` requerido (semver).
5. Todos los contratos con `schema_version = "1.0.0"`.
6. Checker: `schema_version` presente y en formato semver.
7. `MIGRATION.md`: reglas de `schema_version` para adoptantes.
8. `protocol/.agents/VERSION` = `3.13.0`; changelog; INDEX; tracker.

## Pasos

1. Editar `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` (§`context_budget`),
   `.agents/standards/context/BUDGET_MATERIALIZATION.md` y
   `.agents/standards/context/CONTEXT.md` (§3).
2. Agregar `schema_version = "1.0.0"` al front matter TOML de todos los
   contratos (rewrite mecánico en bloque, sin tocar el resto del contenido).
3. Editar `.agents/standards/runtime/PROTOCOL_HEALTH.md` (ítem 3).
4. Extender `tools/check_taxonomy_coherence.py` y sus tests.
5. Editar `docs/MIGRATION.md` (§2).
6. Bump `3.13.0`, changelog, INDEX, tracker.

## Criterios de salida

- [ ] El estado advisory del budget está declarado en contrato y estándares.
- [ ] Todo contrato declara `schema_version` semver y el checker lo valida.
- [ ] `MIGRATION.md` documenta el uso de `schema_version`.
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

- Bajo: clarificación y metadata aditiva; sin cambio de artefactos válidos.

## Trazabilidad

- `AUDITORIA_SISTEMA.md` P2.1 y P4.3.

## Nota de ejecución

Ejecutado el 2026-08-14. Versión `3.13.0` (MINOR: adiciones compatibles de
metadata y clarificaciones documentales). Verificación: invariantes OK, citas
OK, estructura OK, taxonomía OK, tests OK; `check_dist_sync` rojo en `dev` por
diseño.
