# RFC-70 — El conocimiento de contexto del proyecto en la KB de discovery

**Status:** Accepted
**Fecha:** 2026-08-28
**Serie:** Vigésima serie — artefactos de contexto del proyecto y la KB de discovery
**Origen:** Decisión del usuario del 2026-08-28: `project-map.md` y `technical-analysis.md` no son necesarios como archivos propios porque su contenido ya lo produce el discovery.
**Pregunta:** ¿Son necesarios `project-map.md` y `technical-analysis.md` como artefactos propios si su contenido ya vive en la KB de discovery?
**Afectados:** `protocol/.agents/standards/context/PROJECT_ARTIFACTS.md`, `protocol/.agents/standards/context/CONTEXT.md`, `protocol/.agents/standards/context/RESOLUTION_TIE_BREAKING.md`, `protocol/.agents/standards/context/RESOLUTION_DEDUPLICATION.md`, `protocol/.agents/standards/context/RESOLUTION_MERGE.md`, `protocol/.agents/standards/quality/PREFLIGHT_CHECKLIST.md`, `protocol/.agents/standards/INDEX.md`, `protocol/.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md`, `docs/ADOPTION.md`, `docs/MIGRATION.md`, `protocol/.agents/VERSION`, `CHANGELOG.md`, `tools/`.

## Problema

1. **El discovery ya produce exactamente esa información.** Bajo `.project/knowledge/discovery/` el discovery genera las entradas que cubren el contenido de ambos archivos (`protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`):
   - `project-map.md` (resumen, estructura de carpetas, entry points, componentes) → `executive_summary.md`, `file_map.md`, `entrypoint.md`, `glossary.md`, `api.md` y `architecture.md`.
   - `technical-analysis.md` (stack, arquitectura, integraciones, riesgos y deuda) → `stack.md`, `architecture.md`, `dependencies.md`, `technical_debt.md`, `known_errors.md`, `project_flow.md` y `configuration.md`.
   Además, `executive_summary.md` ya es la entrada read-first de orientación: "the first file an agent session reads to orient itself in the project" (`protocol/.agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md:Purpose`).

2. **Los archivos raíz son una segunda fuente de verdad manual.** Se crean a mano en la adopción (`docs/ADOPTION.md:2. Qué configurar`) y el estándar exige que vivan en la raíz del proyecto (`protocol/.agents/standards/context/PROJECT_ARTIFACTS.md:3. Location of Actual Artifacts`). Sin frescura ni provenance, pueden divergir de la KB que produce el mismo contenido de forma revalidable (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`, `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Invalidation`).

3. **La auditoría de reutilización ya los marcó como derivados no producidos por el protocolo** (`docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md:2.2 Tabla de artifacts`), y los consumidores los tratan como fuentes estables sin ciclo de vida (`protocol/.agents/standards/context/CONTEXT.md:1. Priority of information`, `protocol/.agents/standards/quality/PREFLIGHT_CHECKLIST.md:5. Context Awareness`, `protocol/.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md:Relationship to project artifacts`, `protocol/.agents/standards/context/RESOLUTION_TIE_BREAKING.md:2. Criteria, in order of application`, `protocol/.agents/standards/context/RESOLUTION_DEDUPLICATION.md:2. Detection criteria`, `protocol/.agents/standards/context/RESOLUTION_MERGE.md:2. When to merge`).

4. **Fricción operativa observada.** El usuario verificó que `technical-analysis.md` se genera fuera de `.project/` en una adopción real (HikariClub) y confirmó que los archivos no aportan nada que el discovery no produzca.

## Decisión propuesta

1. **`project-map.md` y `technical-analysis.md` se eliminan como artefactos del protocolo.** No se crean en la raíz del proyecto ni se agregan como entradas nuevas de KB: su contenido ya es producido por el discovery en las entradas existentes (mapeo del Problema, punto 1). No hay síntesis redundante: la orientación read-first es `executive_summary.md` (`protocol/.agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md:Purpose`), complementada por las entradas por tipo.
2. **`PROJECT_ARTIFACTS.md` se elimina por completo, incluidas las plantillas de dominio 9.3/9.4.** El discovery ya produce el contenido que esas plantillas pedían: reglas de negocio, flujos y glosario (`BUSINESS_RULES.md`, `PROJECT_FLOW.md`, `GLOSSARY.md`, producidos por el `business_worker` en `DISCOVERY_BUSINESS`); el resto (estados válidos, transiciones, invariantes globales) puede expresarse como reglas en `business_rules.md` si se necesita. Ningún adoptante materializó las plantillas y conservarlas mantendría la misma duplicación manual que esta RFC elimina.
3. **Si el análisis revela un hueco de contenido** (por ejemplo, integraciones externas con manejo de fallos, o estados/transiciones/invariantes de dominio sin sección explícita), se documenta en el contrato per-entry existente correspondiente (`DEPENDENCIES.md`, `ARCHITECTURE.md` o `BUSINESS_RULES.md`), nunca en un documento manual nuevo.
4. **Los consumidores pasan a referir la KB de discovery**: `protocol/.agents/standards/context/CONTEXT.md:1. Priority of information`, `protocol/.agents/standards/quality/PREFLIGHT_CHECKLIST.md:5. Context Awareness`, `protocol/.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md:Relationship to project artifacts`, `protocol/.agents/standards/context/RESOLUTION_TIE_BREAKING.md:2. Criteria, in order of application`, `protocol/.agents/standards/context/RESOLUTION_DEDUPLICATION.md:2. Detection criteria` y `protocol/.agents/standards/context/RESOLUTION_MERGE.md:2. When to merge` citan `executive_summary.md` y las entradas de discovery con su frescura.
5. **Adopción y migración:** `docs/ADOPTION.md:2. Qué configurar` deja de instruir la creación manual; `docs/MIGRATION.md` indica a los adoptantes existentes eliminar los archivos raíz.
6. **Versionado:** MAJOR `10.0.0` (remoción de artefactos y de un estándar) — requiere confirmación del usuario y nota de migración (`docs/VERSIONING.md:3. Versionado`).

## Alternativas consideradas

1. **No hacer nada.** Mantiene la duplicación manual y la divergencia; descartada.
2. **Que discovery genere `project_map.md` y `technical_analysis.md` como entradas de KB nuevas.** Descartada: serían síntesis redundantes de entradas ya existentes, sin hechos nuevos; la síntesis orientativa ya existe en `executive_summary.md`.
3. **Discovery materializa los archivos en la raíz del proyecto.** Descartada: contradice la frontera del workflow de discovery, que no modifica archivos fuente del proyecto (`protocol/.agents/orchestrators/discovery/workflow/08-discovery-ready.md:Purpose`), y mantiene dos copias del mismo contenido.
4. **Reducir `PROJECT_ARTIFACTS.md` a un estándar de dominio conservando 9.3/9.4.** Descartada: las plantillas de dominio duplican lo que el discovery ya produce (reglas, flujos, glosario), no tienen uso real en ningún adoptante, y su origen (`docs/plans/INDEX.md:Archivo`) fue una idea rescatada de un plan descartado que esta RFC supera.

## Impacto en el protocolo

- **Removidos:** los artefactos `project-map.md` y `technical-analysis.md` como concepto normativo y el estándar `PROJECT_ARTIFACTS.md` completo (incluidas las plantillas de dominio 9.3/9.4).
- **Cambiados:** `CONTEXT.md`, `PREFLIGHT_CHECKLIST.md`, `CONTEXT_ARTIFACT.md`, `RESOLUTION_TIE_BREAKING.md`, `RESOLUTION_DEDUPLICATION.md`, `RESOLUTION_MERGE.md`, `standards/INDEX.md`, `docs/ADOPTION.md`, `docs/MIGRATION.md`, `CHANGELOG.md`, `protocol/.agents/VERSION`.
- **Sin cambios en discovery:** no se agregan contratos ni entradas; el contenido ya está cubierto por las entradas existentes.
- **Compatibilidad:** breaking (remoción) → MAJOR. Los archivos existentes en adoptantes dejan de ser normativos y pueden eliminarse.

## Criterios de aceptación

- [ ] No queda ninguna referencia normativa a `project-map.md`, `technical-analysis.md` ni `PROJECT_ARTIFACTS.md` en `protocol/.agents/` ni en `docs/ADOPTION.md`.
- [ ] `PROJECT_ARTIFACTS.md` está eliminado.
- [ ] Los consumidores citan la KB de discovery (`executive_summary.md` y entradas por tipo).
- [ ] `docs/MIGRATION.md` tiene nota de migración; bump MAJOR `10.0.0` confirmado por el usuario.
- [ ] Batería canónica en verde.

## Amendment Log

- 2026-08-28 — Creación.
- 2026-08-28 — Status `Proposal` → `Accepted` (aprobada por el usuario; plan 84).
