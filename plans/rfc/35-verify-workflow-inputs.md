# RFC-35 — Workflow 07: inputs y decisión coherentes

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.2
**Pregunta:** ¿Qué artefactos consume la fase de verificación y con qué valores decide su resultado?
**Afectados:** `.agents/orchestrators/core/workflow/07-verify.md`, `.agents/orchestrators/core/roles/verifier.md`, `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`.

## Problema

El front matter del workflow 07 declara `input_artifacts: [EXECUTION_SUMMARY.md]` (`.agents/orchestrators/core/workflow/07-verify.md:Verify`), pero el cuerpo exige leer `TASK_SPECIFICATION.md` y `EXECUTION_PLAN.md` además del estado del proyecto, y el rol `verifier` lista spec, plan y summary como entradas (`.agents/roles/verifier.md:Inputs`). Además, el cuerpo del workflow dice que la decisión final es `COMPLETED` o `FAILED` (`.agents/orchestrators/core/workflow/07-verify.md:Process`), mientras el contrato `VERIFICATION_REPORT.md` restringe `decision.result` a `COMPLETED` o `RECOVERY` (`.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md:Final Decision`).

Consecuencia: un orquestador que confía en el front matter delegaría la verificación sin la spec ni el plan; y un verifier que usa el workflow escribiría `FAILED`, que el gate H06 rechaza.

## Decisión propuesta

1. Front matter de `07-verify.md`: `input_artifacts: [TASK_SPECIFICATION.md, EXECUTION_PLAN.md, EXECUTION_SUMMARY.md]`, con el estado del proyecto como input contextual (no artefacto).
2. Cuerpo del workflow: la decisión final es `COMPLETED` o `RECOVERY`, nunca `FAILED`.
3. Rol `verifier.md`: sin cambios funcionales (ya lista los tres artefactos), solo verificación de coherencia.

## Alternativas consideradas

- **Aceptar `FAILED` como sinónimo de `RECOVERY`**: crea dos vocabularios para el mismo valor; viola la taxonomía de contratos.
- **Quitar spec/plan del rol**: degrada la verificación a solo el resumen de ejecución.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `07-verify.md` | Front matter de inputs; valor de decisión en el cuerpo. |
| `verifier.md` | Verificación de coherencia (sin cambio funcional). |

## Criterios de aceptación

- [ ] Front matter y cuerpo del workflow 07 listan los mismos inputs.
- [ ] Ningún documento del protocolo usa `FAILED` como decisión de verificación.
- [ ] H06 y contrato usan el mismo enum.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.2 |
