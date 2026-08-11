# Plan 35 — Workflow 05: inputs completos

**Status:** Aprobado para ejecución
**Fecha:** 2026-08-11
**RFC:** RFC-36 (`plans/rfc/36-plan-workflow-inputs.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.3
**Vía de autorización:** Vía plan (RFC-42): plan `Aprobado para ejecución` con justificación documentada — el usuario autorizó el 2026-08-11 corregir y dejar implementables los planes 34–36 tras la auditoría (RFC-36 sigue en `Proposal`; la vía plan habilita el cambio de `.agents/`).

## Objetivo

Completar la lista de inputs del workflow 05, del rol `planner` y de la taxonomía con `CONTEXT_ARTIFACT.md`.

## Criterio de entrada

- [ ] RFC-36 existe en `plans/rfc/` (status `Proposal` o `Accepted`; la vía plan no depende del status de la RFC).
- [ ] Vía de autorización declarada (este plan: `Aprobado para ejecución` + justificación en `**Vía de autorización:**`; registro en `CHANGELOG.md` al ejecutar).
- [ ] Verificación contra el repo de las secciones citadas.

## Entregables

1. `05-plan.md` con front matter de inputs corregido.
2. `planner.md` con inputs alineados.
3. `PROTOCOL_TAXONOMY.md` con `workflow:05-plan` y `core:PLANNING` alineados.

## Pasos

1. Editar el front matter de `05-plan.md`: `input_artifacts: [TASK_SPECIFICATION.md, CONTEXT_ARTIFACT.md, CONTEXT_VALIDATION_REPORT.md]`.
2. Editar `.agents/roles/planner.md:Inputs`: misma lista (agregar `CONTEXT_ARTIFACT.md`).
3. Verificar que el contrato `EXECUTION_PLAN.md` (`Context Reference`) es consistente (ya referencia `artifact` y `validation_report`; sin cambio).
4. Actualizar `PROTOCOL_TAXONOMY.md`: en `workflow:05-plan` (`input_artifacts`) y en el estado `core:PLANNING` (`artifacts_input`), agregar `CONTEXT_ARTIFACT.md`.
5. Registrar la vía de autorización en `CHANGELOG.md`.
6. Ejecutar la verificación documental (tools + H13 por juicio).

## Criterios de salida

- [ ] Front matter y cuerpo de 05 concuerdan (el cuerpo ya lista `CONTEXT_ARTIFACT.md` y `CONTEXT_VALIDATION_REPORT.md`).
- [ ] `planner.md` concuerda con el front matter.
- [ ] H13 aplicado por juicio: `workflow:05-plan` y `core:PLANNING` coherentes con el archivo.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Comparación front matter ↔ cuerpo ↔ rol ↔ taxonomía para las fases 00-08 (skill `consistency-checker`); aplicar H13 regla 10 por juicio.

## Riesgos

- Bajo: cambio documental. Requiere tocar `PROTOCOL_TAXONOMY.md` (fuente única según H13); verificar coherencia con H13.

## Trazabilidad

- RFC-36; punto 2.3 de la auditoría; correcciones de la auditoría de planes 34–36 (2026-08-11).
