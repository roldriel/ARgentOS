# RFC-33 — Schema único de pasos en EXECUTION_SUMMARY

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.5
**Pregunta:** ¿Cuál es el nombre canónico de la lista de pasos ejecutados en `EXECUTION_SUMMARY.md`?
**Afectados:** `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md`, `.agents/orchestrators/core/harness/policies/H05-execution-completed.md`.

## Problema

El contrato `EXECUTION_SUMMARY.md` usa dos nombres para la misma lista:

- En el template del cuerpo de la sección `## Steps Executed`, la lista es `[[steps]]` (`.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md:Steps Executed`).
- En la sección machine-readable del mismo contrato, la lista es `[[steps_executed]]` (`.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md:Machine-readable TOML blocks`).

La policy H05 valida `steps_executed` (`.agents/orchestrators/core/harness/policies/H05-execution-completed.md:Gate Checklist`). Un worker que sigue el template del cuerpo produce un artefacto que H05 rechaza, y no hay forma de saber cuál nombre es el canónico sin leer la policy.

## Decisión propuesta

`steps_executed` es el único nombre canónico de la lista en todo el contrato. El template del cuerpo y el bloque machine-readable usan `[[steps_executed]]`; se elimina `[[steps]]`. La policy H05 queda sin cambios (ya valida el nombre canónico), y el contrato gana una nota de compatibilidad: los artefactos históricos con `[[steps]]` se consideran no conformes y deben migrarse.

## Alternativas consideradas

- **Elegir `[[steps]]` como canónico**: obligaría a cambiar H05 y a reinterpretar los artefactos del dogfooding, que ya usan `steps_executed` (verificado en `HARNESS_REPORT.md` de la sesión `d4ab6a93-8e75-4880-baf3-676fce992936`).
- **Aceptar ambos nombres**: crea dos formatos válidos y complica la validación; se descarta por la política single-source.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `EXECUTION_SUMMARY.md` | Unificar en `[[steps_executed]]` en template y bloque machine-readable. |
| `H05-execution-completed.md` | Sin cambio funcional; opcional nota de canonicalización. |

## Criterios de aceptación

- [ ] `[[steps` no aparece como lista en el contrato (salvo `steps_executed`).
- [ ] Un resumen conforme al contrato pasa H05 sin ambigüedad de nombre.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 1.5 |
| 2026-08-11 | Plan 32 ejecutado: cambios aplicados en `.agents/`; status permanece `Proposal` (regularización de gobernanza pendiente) | Plan 32 |
