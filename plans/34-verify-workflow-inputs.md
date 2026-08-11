# Plan 34 — Workflow 07: inputs y decisión coherentes

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-35 (`plans/rfc/35-verify-workflow-inputs.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.2
**Vía de autorización:** Vía plan (RFC-42): plan `Aprobado para ejecución` con justificación documentada — el usuario autorizó el 2026-08-11 corregir y dejar implementables los planes 34–36 tras la auditoría (RFC-35 sigue en `Proposal`; la vía plan habilita el cambio de `.agents/`).
**Nota de ejecución (2026-08-11):** implementado por decisión del usuario; criterios de salida verificados (`check_protocol_invariants.py` y `check_plan_citations.py` en verde); registro en `CHANGELOG.md` 3.0.2.

## Objetivo

Alinear front matter, cuerpo y rol de la fase 07 entre sí, con el contrato `VERIFICATION_REPORT.md` y con la taxonomía (`PROTOCOL_TAXONOMY.md`).

## Criterio de entrada

- [ ] RFC-35 existe en `plans/rfc/` (status `Proposal` o `Accepted`; la vía plan no depende del status de la RFC).
- [ ] Vía de autorización declarada (este plan: `Aprobado para ejecución` + justificación en `**Vía de autorización:**`; registro en `CHANGELOG.md` al ejecutar).
- [ ] Verificación contra el repo de las secciones citadas.

## Entregables

1. `07-verify.md` con front matter de inputs corregido y cuerpo con la subsección `## Execution Summary`.
2. `07-verify.md` con `COMPLETED`/`RECOVERY` como valores de decisión.
3. `verifier.md` verificado contra el front matter (sin cambios funcionales).
4. `PROTOCOL_TAXONOMY.md` con el entry `workflow:07-verify` alineado.

## Pasos

1. Editar el front matter de `07-verify.md`: `input_artifacts: [TASK_SPECIFICATION.md, EXECUTION_PLAN.md, EXECUTION_SUMMARY.md]`.
2. Agregar en el cuerpo, dentro de `## Input Artifacts` y después de `## Execution Plan`, una subsección `## Execution Summary` con fuente `.project/<session-uuid>/<iteration>/<order>-EXECUTION_SUMMARY.md` y uso: "verificar que los pasos planificados se ejecutaron y que los resultados declarados coinciden con lo verificado". `## Project State` queda como input contextual (no artefacto).
3. Editar el cuerpo, en `## Process` §4 (Generate Verification Report): en el bullet "Final decision:", reemplazar el valor `FAILED` por `RECOVERY` (queda `COMPLETED` or `RECOVERY`). No tocar otros textos con "fail"/"failed" (p. ej. "failed criteria" o el encabezado "Verification Failed") ni estados `DISCOVERY_FAILED`/`BOOTSTRAP_FAILED`. `## State Transitions` ya usa `RECOVERY`; no requiere cambios.
4. Verificar `.agents/roles/verifier.md:Inputs` contra el nuevo front matter: confirmar que `TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md` y `EXECUTION_SUMMARY.md` figuran en la lista del rol. El rol lista además `CONTEXT_ARTIFACT.md`, `CONTEXT_VALIDATION_REPORT.md` y el draft de `VERIFICATION_REPORT.md` (superset permitido); no se edita el rol y la diferencia se registra en `EXECUTION_SUMMARY.md`.
5. Actualizar en `PROTOCOL_TAXONOMY.md` el entry `workflow:07-verify`: `input_artifacts: [TASK_SPECIFICATION.md, EXECUTION_PLAN.md, EXECUTION_SUMMARY.md]`. Verificar que el entry de estado `core:VERIFYING` ya lista los tres (sin cambio).
6. Buscar `FAILED` como valor de decisión de verificación (`decision.result`) en `.agents/` y corregir apariciones residuales. Los únicos matches esperados fuera de la decisión son los estados `DISCOVERY_FAILED`/`BOOTSTRAP_FAILED` y los resultados `PASS`/`FAIL` de las policies; no se modifican.
7. Registrar la vía de autorización en `CHANGELOG.md`.
8. Ejecutar la verificación documental (tools + H13 por juicio).

## Criterios de salida

- [ ] Front matter, cuerpo (`## Input Artifacts`) y taxonomía (`workflow:07-verify`) de 07 listan los mismos inputs: `TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md`, `EXECUTION_SUMMARY.md`.
- [ ] `decision.result` usa solo `COMPLETED`/`RECOVERY` en contrato, workflow y gate (H06).
- [ ] `verifier.md` incluye los tres inputs y no fue editado.
- [ ] H13 aplicado por juicio: `workflow:07-verify` y `core:VERIFYING` coherentes con el archivo.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Búsqueda textual de `FAILED` en `.agents/` y revisión de cada aparición: solo la línea de decisión de `07-verify.md` (`## Process` §4) debe cambiar; `DISCOVERY_FAILED`/`BOOTSTRAP_FAILED` se reportan como no-decisión.
- Aplicar H13 (`harness/policies/H13-protocol-taxonomy.md`, reglas 2 y 10) por juicio sobre `PROTOCOL_TAXONOMY.md`.

## Riesgos

- Bajo: cambio documental; sin impacto en contratos. Requiere tocar `PROTOCOL_TAXONOMY.md` (fuente única según H13); verificar coherencia con H13.

## Trazabilidad

- RFC-35; punto 2.2 de la auditoría; correcciones de la auditoría de planes 34–36 (2026-08-11).
