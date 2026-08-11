# RFC-44 — INTENT_REFLECTION auto-confirmada sin estado productor

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 3.2
**Pregunta:** ¿En qué estado se produce la `INTENT_REFLECTION.md` cuando la confianza es HIGH y no hay confirmación del usuario?
**Afectados:** `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`, `.agents/orchestrators/core/roles/orchestrator.md`, `.agents/orchestrators/core/workflow/00-analyze-task.md`.

## Problema

El workflow 00 ordena generar `INTENT_REFLECTION.md` para trazabilidad aun con confianza HIGH, con confirmación opcional (`.agents/orchestrators/core/workflow/00-analyze-task.md:Process`), y el rol del orquestador instruye lo mismo en su sección de enforcement de reflexión de intención (`.agents/orchestrators/core/roles/orchestrator.md:Intent Reflection Enforcement`). Pero la máquina de estados solo produce `INTENT_REFLECTION.md` en `CONFIRMING_INTENT` (`.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:CONFIRMING_INTENT`), y `ANALYZING_TASK` solo tiene `TASK_ANALYSIS.md` como artefacto de salida (`.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:ANALYZING_TASK`).

El dogfooding lo registró como ambigüedad: la reflexión se generó y se gateó con H11 sin que un estado la produjera (`plans/19-anexo-a-bitacora-fricciones.md:F-04`).

## Decisión propuesta

1. Cuando la confianza es HIGH y no hay ambigüedad bloqueante, la `INTENT_REFLECTION.md` se produce en `ANALYZING_TASK` como artefacto de trazabilidad (orden posterior a `TASK_ANALYSIS.md`), antes de `BUILDING_TASK_SPECIFICATION`.
2. La máquina de estados declara `INTENT_REFLECTION.md` como salida opcional de `ANALYZING_TASK` (vía HIGH) y salida obligatoria de `CONFIRMING_INTENT` (vía MEDIUM/LOW).
3. H11 conserva su rol: gatea la reflexión antes de `BUILDING_TASK_SPECIFICATION` cuando se genera; en HIGH la confirmación del usuario no es requisito, pero la reflexión debe ser coherente con `TASK_ANALYSIS.md`.
4. `orchestrator.md` y el workflow 00 describen explícitamente ambas vías de producción.

## Alternativas consideradas

- **No generar reflexión en HIGH**: contradice la política de trazabilidad del protocolo.
- **Forzar `CONFIRMING_INTENT` en HIGH**: obliga a confirmación innecesaria y contradice el modelo de confianza.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `AGENT_STATE_MACHINE.md` | Salida opcional de reflexión en `ANALYZING_TASK` (HIGH). |
| `orchestrator.md` | Vías HIGH vs MEDIUM/LOW explícitas. |
| `00-analyze-task.md` | Procedimiento de generación en HIGH. |

## Criterios de aceptación

- [ ] Toda `INTENT_REFLECTION.md` tiene un estado productor declarado.
- [ ] La vía HIGH no exige confirmación del usuario.
- [ ] La reflexión HIGH es trazable y coherente con el análisis.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 3.2; F-04 |
