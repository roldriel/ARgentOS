# RFC-34 — Forma canónica de Acceptance Criteria (EARS)

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.1
**Pregunta:** ¿Cuál es la forma canónica de los criterios de aceptación: bullets Markdown o bloque TOML?
**Afectados:** `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md`, `.agents/orchestrators/core/harness/policies/H01-task-specification.md`, `.agents/skills/ears-writer/SKILL.md`.

## Problema

El contrato `TASK_SPECIFICATION.md` muestra como forma canónica el array TOML `acceptance_criteria = [""]` en la sección `## Acceptance Criteria` (`.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria`), y los bullets EARS aparecen solo en un bloque de ejemplo. La policy H01 exige que la sección contenga bullets Markdown y valida cada bullet contra los patrones EARS (`.agents/orchestrators/core/harness/policies/H01-task-specification.md:Gate Checklist`).

El dogfooding ya falló exactamente por esto: la spec v1 puso los criterios dentro del bloque TOML y H01 falló con `ears_criteria_present: FAIL` (`plans/19-anexo-a-bitacora-fricciones.md:F-01`). La fricción persiste en 2.0.1: un artefacto conforme al contrato falla el gate.

## Decisión propuesta

1. **Los bullets Markdown son la forma canónica** de `## Acceptance Criteria`: un bullet por criterio EARS, atómico y verificable.
2. El bloque TOML `acceptance_criteria` queda como representación machine-readable **opcional y derivada**, con la nota explícita de que no reemplaza a los bullets.
3. El contrato se reescribe para declarar los bullets como forma canónica y el bloque TOML como opcional; el ejemplo pasa a ser la forma principal.
4. H01 queda sin cambios estructurales (ya valida bullets) y gana una aclaración: criterios solo en TOML se reportan como violación de forma.

## Alternativas consideradas

- **Elegir el bloque TOML como canónico**: obligaría a que H01 valide TOML y a reinterpretar el dogfooding; contrario a la legibilidad de las specs.
- **Aceptar ambas formas**: crea dos fuentes de verdad y complica la validación.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `TASK_SPECIFICATION.md` | Bullets canónicos; TOML opcional y derivado. |
| `H01-task-specification.md` | Aclaración de violación de forma. |
| `ears-writer` | Alinear su procedimiento con los bullets canónicos. |

## Criterios de aceptación

- [ ] Un artefacto conforme al contrato (bullets) pasa H01.
- [ ] Un artefacto con criterios solo en TOML falla H01 con evidencia clara.
- [ ] El contrato no muestra dos formas canónicas.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.1; F-01 |
| 2026-08-11 | Plan 33 ejecutado: cambios aplicados en `.agents/`; status permanece `Proposal` (regularización de gobernanza pendiente) | Plan 33 |
