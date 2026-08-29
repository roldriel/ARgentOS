# Plan 84 — Eliminación de project-map.md y technical-analysis.md en favor de la KB de discovery

**Status:** Executed
**Fecha:** 2026-08-28
**RFC:** RFC-70 (`docs/rfc/70-project-context-in-discovery-kb.md`)
**Clase:** A
**Depende de:** — (gated a RFC-70 `Accepted`)
**Origen:** RFC-70; decisión del usuario del 2026-08-28.

## Objetivo

Implementar la RFC-70: eliminar `project-map.md` y `technical-analysis.md` como
artefactos del protocolo (ni raíz ni entradas de KB nuevas) y eliminar
`PROJECT_ARTIFACTS.md` por completo (incluidas las plantillas de dominio 9.3/9.4),
declarando que su contenido ya vive en la KB de discovery, y realinear
consumidores y adopción.

## Criterio de entrada

- [ ] RFC-70 `Accepted` (Clase A, RFC-56; `docs/CONVENTIONS.md:Convenciones`).
- [ ] Batería canónica en verde previa a la ejecución (paso 0 de verificación contra el repo).
- [ ] Rama de trabajo `dev` (`docs/VERSIONING.md:1. Ramas y roles`).
- [ ] Confirmación del usuario del bump MAJOR a `10.0.0` (`docs/VERSIONING.md:3. Versionado`).

## Entregables

1. `protocol/.agents/standards/context/PROJECT_ARTIFACTS.md` eliminado (incluidas las plantillas de dominio 9.3/9.4) y su entrada fuera de `protocol/.agents/standards/INDEX.md`.
2. Actualizaciones de consumidores: `CONTEXT.md`, `PREFLIGHT_CHECKLIST.md`, `CONTEXT_ARTIFACT.md`, `RESOLUTION_TIE_BREAKING.md`, `RESOLUTION_DEDUPLICATION.md`, `RESOLUTION_MERGE.md` y `standards/INDEX.md`.
3. Cambios de adopción y versionado: `docs/ADOPTION.md`, `docs/MIGRATION.md`, `CHANGELOG.md` y `protocol/.agents/VERSION` (`10.0.0`).
4. Registro en `docs/rfc/INDEX.md` (RFC-70 `Accepted`) y `docs/plans/INDEX.md` (plan 84 `Executed`), `Nota de ejecución` y Amendment Log de la RFC-70.
5. Alineación de `tools/` si la batería lo exige (listas de artefactos de evidencia en `tools/check_architecture_traceability.py` y coherencia de salidas en `tools/check_taxonomy_coherence.py`).

## Pasos

1. **Verificación de cobertura:** confirmar contra `protocol/.agents/orchestrators/discovery/contracts/` que las entradas existentes cubren cada sección de ambos artefactos y de las plantillas de dominio (mapeo de `docs/rfc/70-project-context-in-discovery-kb.md:Decisión propuesta`); si falta algo (p. ej. integraciones externas con manejo de fallos, o estados/transiciones/invariantes de dominio), documentarlo en el contrato per-entry existente correspondiente (`DEPENDENCIES.md`, `ARCHITECTURE.md` o `BUSINESS_RULES.md`), sin crear artefactos nuevos.
2. **Estándar:** eliminar `protocol/.agents/standards/context/PROJECT_ARTIFACTS.md` y su entrada en `protocol/.agents/standards/INDEX.md`.
3. **Consumidores:** actualizar `protocol/.agents/standards/context/CONTEXT.md:1. Priority of information`, `protocol/.agents/standards/quality/PREFLIGHT_CHECKLIST.md:5. Context Awareness`, `protocol/.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md:Relationship to project artifacts`, `protocol/.agents/standards/context/RESOLUTION_TIE_BREAKING.md:2. Criteria, in order of application`, `protocol/.agents/standards/context/RESOLUTION_DEDUPLICATION.md:2. Detection criteria`, `protocol/.agents/standards/context/RESOLUTION_MERGE.md:2. When to merge` y `protocol/.agents/standards/INDEX.md` para referir `executive_summary.md` y las entradas de discovery con su frescura.
4. **Adopción:** actualizar `docs/ADOPTION.md:2. Qué configurar` (eliminar la creación manual de ambos archivos; indicar que el contexto del proyecto se obtiene de la KB de discovery) y agregar en `docs/MIGRATION.md` la migración de adoptantes existentes (eliminar los archivos raíz; dejan de ser normativos).
5. **Versionado y cierre:** `CHANGELOG.md` (sección `## [10.0.0]` con ítem `(plan 84, RFC-70)` en `Removed`/`Changed`), `protocol/.agents/VERSION` → `10.0.0`, RFC-70 → `Accepted` con Amendment Log, plan → `Executed` con `Nota de ejecución` y registro en ambos INDEX.
6. **Verificación:** correr la batería canónica y dejar constancia en la `Nota de ejecución`.

## Criterios de salida

- [ ] No queda ninguna referencia normativa a `project-map.md`, `technical-analysis.md` ni `PROJECT_ARTIFACTS.md` en `protocol/.agents/` ni en `docs/ADOPTION.md`.
- [ ] `PROJECT_ARTIFACTS.md` está eliminado.
- [ ] Los consumidores citan la KB de discovery.
- [ ] RFC-70 `Accepted`; plan 84 `Executed`; INDEXes actualizados.
- [ ] Batería canónica en verde; `check_version_state.py` sin errores (warnings OK en `dev`).

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

H13 por juicio. `check_dist_sync.py` solo tras la promoción en `master` (roja en `dev` por diseño — `docs/VERSIONING.md:4.1 Batería canónica de verificación`).

## Riesgos

- **Bump MAJOR:** requiere confirmación del usuario y nota de migración (`docs/VERSIONING.md:3. Versionado`); sin confirmación, el plan no se ejecuta.
- **Huecos de contenido:** si alguna sección de los artefactos o plantillas eliminados no está cubierta por una entrada de discovery, se documenta en el contrato per-entry existente correspondiente (incluido `BUSINESS_RULES.md` para estados/transiciones/invariantes de dominio); no se crean artefactos nuevos.
- **Checkers dev con listas hardcodeadas:** `tools/check_architecture_traceability.py` y `tools/check_taxonomy_coherence.py` pueden exigir alineación; se ajustan como parte del entregable 5 si la batería falla.

## Trazabilidad

Decisión del usuario (2026-08-28) → RFC-70 → plan 84 → entregables.

## Nota de ejecución

**2026-08-28** — Ejecutado en `dev`. Cobertura verificada contra
`protocol/.agents/orchestrators/discovery/contracts/`: las secciones de los
artefactos eliminados y de las plantillas de dominio están cubiertas por las
entradas existentes (`executive_summary.md`, `file_map.md`, `entrypoint.md`,
`glossary.md`, `api.md`, `architecture.md`, `stack.md`, `dependencies.md`,
`technical_debt.md`, `known_errors.md`, `project_flow.md`,
`business_rules.md`, `configuration.md`); las integraciones externas se cubren
como dependencias (`DEPENDENCIES.md`) y contenido cualitativo (`## Summary`
del contrato base), sin agregar secciones obligatorias. `PROJECT_ARTIFACTS.md`
eliminado; consumidores, `docs/ADOPTION.md` y `docs/MIGRATION.md`
actualizados. Batería canónica en verde (checkers + pytest). RFC-70 `Accepted`,
versión `10.0.0`.
