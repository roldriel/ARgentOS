# RFC-48 — Contratos por entrada del discovery

**Status:** Accepted (2026-08-12, revisión individual RFC-56; diseño aprobado, ejecución pendiente vía su plan)
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 4.3 (y 6.3)
**Pregunta:** ¿Dónde se definen las secciones y campos requeridos de cada entrada de la KB de discovery?
**Afectados:** `.agents/orchestrators/discovery/contracts/`, `.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`, `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`.

## Problema

Existen contratos para 8 tipos de entrada de discovery (`KB_DISCOVERY_ENTRY.md`, `DISCOVERY_MANIFEST.md`, `DEVELOPMENT_PATTERNS.md`, `ENVIRONMENT_DISCOVERY.md`, `EXECUTIVE_SUMMARY.md`, `API_SURFACE.md`, `INTER_WORKER_MESSAGE.md`, `KB_DISCOVERY_REPORT.md`), pero los estados de la máquina de discovery producen además `stack.md`, `dependencies.md`, `containers.md`, `database.md`, `distribution.md`, `architecture.md`, `configuration.md`, `entrypoint.md`, `business_rules.md`, `project_flow.md`, `technical_debt.md`, `known_errors.md`, `glossary.md` y `file_map.md` sin contrato dedicado (`.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:States`). La policy D01 compensa hardcodeando secciones requeridas en su ítem 12 (`.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist`), lo que duplica contenido de contrato dentro de una policy y viola la política single-source (`plans/INDEX.md:Convenciones`).

## Decisión propuesta

1. Crear contratos por entrada para los 14 tipos sin contrato, siguiendo el formato base de `KB_DISCOVERY_ENTRY.md` (front matter TOML, `# <Title>`, `## Summary`, `## Discovered Facts`) más sus secciones específicas.
2. D01 referencia los contratos por entrada y elimina el listado duplicado de secciones de su ítem 12 (verifica contra los contratos).
3. Registrar las nuevas entidades de contrato en `PROTOCOL_TAXONOMY.md`.

## Alternativas consideradas

- **Un único contrato consolidado para entradas de discovery**: reduce archivos pero pierde la especificidad por entrada; se descarta en favor de contratos por entrada.
- **Dejar las secciones en D01**: mantiene la violación single-source.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `discovery/contracts/` | 14 contratos nuevos. |
| `D01-discovery-output.md` | Ítem 12 refactorizado a verificación contra contratos. |
| `PROTOCOL_TAXONOMY.md` | Entidades de contrato nuevas. |

## Criterios de aceptación

- [ ] Cada entrada publicada tiene contrato.
- [ ] D01 no duplica secciones requeridas definidas en contratos.
- [ ] La taxonomía registra los contratos nuevos.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, puntos 4.3 / 6.3 |
| 2026-08-12 | Accepted (revisión individual, RFC-56/plan 57): diseño aprobado; la ejecución sigue el track de su plan asociado. | Revisión de la serie Proposal (RFC-56) |
