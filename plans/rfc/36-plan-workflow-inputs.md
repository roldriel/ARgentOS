# RFC-36 — Workflow 05: inputs completos

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.3
**Pregunta:** ¿Qué artefactos debe recibir el worker de planificación para producir un plan válido?
**Afectados:** `.agents/orchestrators/core/workflow/05-plan.md`, `.agents/orchestrators/core/roles/planner.md`.

## Problema

El front matter del workflow 05 declara `input_artifacts: [TASK_SPECIFICATION.md, CONTEXT_VALIDATION_REPORT.md]` (`.agents/orchestrators/core/workflow/05-plan.md:Plan`), omitiendo `CONTEXT_ARTIFACT.md`, que el cuerpo exige explícitamente como input (`.agents/orchestrators/core/workflow/05-plan.md:Input Artifacts`). El rol `planner` también lista solo spec y validation report (`.agents/roles/planner.md:Inputs`).

Consecuencia: el plan se construye sobre la validación sin el contexto validado, y H15 pre-delegación (que verifica los inputs contra el front matter) no exigiría el contexto.

## Decisión propuesta

1. Front matter de `05-plan.md`: `input_artifacts: [TASK_SPECIFICATION.md, CONTEXT_ARTIFACT.md, CONTEXT_VALIDATION_REPORT.md]`.
2. Rol `planner.md`: misma lista de inputs.
3. `EXECUTION_PLAN.md` (contrato): su sección `Context Reference` ya referencia ambos artefactos; sin cambio.

## Alternativas consideradas

- **Quitar `CONTEXT_ARTIFACT.md` del cuerpo**: degrada la planificación, que necesita el contenido, no solo su validación.
- **Dejar el front matter incompleto**: H15 no validaría un input real; se descarta.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `05-plan.md` | Front matter con los tres inputs. |
| `planner.md` | Inputs alineados. |

## Criterios de aceptación

- [ ] Front matter, cuerpo y rol de planificación listan los mismos inputs.
- [ ] H15 pre-delegación exige `CONTEXT_ARTIFACT.md` para la fase 05.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.3 |
