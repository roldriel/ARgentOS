# RFC-46 — Política de trazas históricas no reproducibles

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 4.1
**Pregunta:** ¿Cómo se interpretan los artefactos de sesión producidos por una versión anterior del protocolo con un harness que ya no existe?
**Afectados:** `.agents/contracts/SESSION_LOG.md`, `.agents/contracts/METRICS.md`, `.agents/contracts/HARNESS_REPORT.md`, `plans/INDEX.md`.

## Problema

La única sesión ejecutada end-to-end (dogfooding, 2026-08-05) registró gates con checks machine (`ears_criteria_present`, `rubric_evaluation_all_rubrics_present`) y scripts (`runner.py`, `delegation_validity.py`, árboles TOML) que la migración 2.0.0 eliminó (`.agents/contracts/HARNESS_REPORT.md` de la sesión `d4ab6a93-8e75-4880-baf3-676fce992936`; `CHANGELOG.md`). Un auditor que compare la traza contra el harness documentado hoy (checklists en prosa) concluirá que la traza no es reproducible. La traza es válida para su versión, pero nada en los artefactos declara la versión del protocolo ni el modo de evaluación usado.

## Decisión propuesta

1. Toda sesión declara su versión de protocolo y su modo de evaluación: agregar `protocol_version` al encabezado de `SESSION_LOG.md` y a `session_start` de `METRICS.md`; `HARNESS_REPORT.md` gana una nota de versión.
2. Definir la regla de interpretación: los artefactos de sesión son registros inmutables del protocolo vigente al momento de la sesión; no se reescriben ni se regeneran para "reproducir" con una versión nueva (coherente con la regla de no retroactividad de `PROTOCOL_BOUNDARIES.md`).
3. Documentar en `plans/INDEX.md` (o en la bitácora) que las entradas de gates previas a 2.0.0 fueron evaluadas por runner y las posteriores por juicio, para que la comparación sea legible.

## Alternativas consideradas

- **Reescribir la traza antigua**: viola la no retroactividad y falsifica el registro.
- **Ignorar la traza**: pierde el único dato empírico de ejecución del protocolo.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `SESSION_LOG.md` | Campo `protocol_version`. |
| `METRICS.md` | Campo `protocol_version` en `session_start`. |
| `HARNESS_REPORT.md` | Nota de versión en el encabezado. |
| `plans/INDEX.md` | Nota histórica de modos de evaluación. |

## Criterios de aceptación

- [ ] Toda sesión nueva declara su versión de protocolo.
- [ ] La regla de interpretación de trazas históricas está documentada.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 4.1 |
