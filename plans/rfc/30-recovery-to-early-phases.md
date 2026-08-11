# RFC-30 — Recovery a fases tempranas

**Status:** Accepted
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.2 (y 3.1)
**Pregunta:** ¿Qué transiciones legales permiten corregir un artefacto de una fase temprana después de un fallo de gate, sin normalizar desviaciones?
**Afectados:** `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`, `.agents/orchestrators/core/harness/policies/H01-task-specification.md`, `.agents/orchestrators/core/workflow/08-recovery.md`, policies H00/H02/H03/H04/H11.

## Problema

La máquina de estados solo permite `RECOVERY → PLANNING | NEEDS_CLARIFICATION | ABORT` (`.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:RECOVERY`). Las tablas de decisión de recovery usan la acción `RETRY_WORKER` con `target_phase` apuntando a fases tempranas (por ejemplo `02-build-task-specification.md` en `.agents/orchestrators/core/harness/policies/H01-task-specification.md:Recovery Decision Table`), pero el modelo de estados no tiene aristas que permitan volver a esas fases desde `RECOVERY`.

La policy H01 se contradice internamente: su sección "On Failure" dice *"Return to BUILDING_TASK_SPECIFICATION y re-invocar"*, mientras su tabla de recovery mapea el caso residual a `RECOVERY_GENERIC` con destino `08-recovery.md` (`.agents/orchestrators/core/harness/policies/H01-task-specification.md:On Failure`). El dogfooding ya registró la desviación real: `RECOVERY → BUILDING_TASK_SPECIFICATION` no existe en la máquina y se ejecutó como desviación justificada (`plans/19-anexo-a-bitacora-fricciones.md:F-03`). Un fallo de formato puro (artefacto existente, sin ambigüedad) no tiene rama de retry en la tabla de H01 y entra a RECOVERY sin salida legal (`plans/19-anexo-a-bitacora-fricciones.md:F-02`).

## Decisión propuesta

Modelar dos mecanismos complementarios:

1. **`RETRY_WORKER` como acción correctiva sin transición**: cuando la tabla de recovery de un gate fallido indica `RETRY_WORKER` con la fase actual como destino, el Orchestrator re-invoca al worker en el mismo estado; no es una transición de estado y no requiere arista nueva. Es el comportamiento ya previsto para `artifact_exists == false`.
2. **Aristas explícitas de `RECOVERY` a fases tempranas**: cuando la tabla indica `RETRY_WORKER` con una fase anterior como destino (por ejemplo corregir la spec tras un fallo de H01), la máquina debe permitir `RECOVERY → ANALYZING_TASK | BUILDING_TASK_SPECIFICATION | GATHERING_CONTEXT | VALIDATING_CONTEXT | PLANNING` según el artefacto a corregir. `RECOVERY → NEEDS_CLARIFICATION` y `RECOVERY → ABORT` se mantienen. La arista a `GATHERING_CONTEXT` cubre el retorno pedido por H03 ("On Failure" y "Decision mapping"); la arista a `VALIDATING_CONTEXT` cubre la reescritura del `CONTEXT_VALIDATION_REPORT`.

Además, H01 debe ganar una rama de retry acotado para fallos de formato: `artifact_exists == true`, `objective_is_ambiguous == false`, `scope_is_clear == true` y `retry_count == 0` → `RETRY_WORKER` sobre `02-build-task-specification.md` (no recovery). `artifact_exists` se define así: `false` = artefacto ausente o a regenerar; `true` = artefacto presente con fallo de formato.

El cambio de aristas requiere actualizar también la enumeración de destinos del recovery en §No-Skip Rule de la máquina de estados (hoy limita el recovery a `PLANNING`/`NEEDS_CLARIFICATION`), y las secciones "On Failure"/"Decision mapping" de H03 que ordenan volver a `GATHERING_CONTEXT` sin modelar la transición.

## Alternativas consideradas

- **Prohibir la corrección de fases tempranas**: obliga a replanear o re-clarificar para corregir formato; costoso y ya demostrado insuficiente en el dogfooding.
- **Convertir todo fallo de formato en `NEEDS_CLARIFICATION`**: fabrica preguntas al usuario que no existen.
- **Reintroducir un runner mecánico**: fuera del alcance de la dirección "menos Python, más texto" de 2.0.0.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `AGENT_STATE_MACHINE.md` | Agregar aristas de `RECOVERY` a fases tempranas y definir `RETRY_WORKER` como acción sin transición. |
| `H01-task-specification.md` | Nueva rama `RETRY_WORKER` para fallos de formato; alinear "On Failure" con la tabla. |
| `08-recovery.md` | Documentar las salidas a fases tempranas y la distinción retry-sin-transición. |
| `H00/H02/H03/H04/H11` | Verificar que sus tablas de recovery usan el mecanismo de forma coherente y alinear sus secciones "On Failure"/"Decision mapping" (en particular H03 → `GATHERING_CONTEXT`) con las aristas nuevas. |

## Criterios de aceptación

- [ ] Un fallo de formato de H01 se corrige con `RETRY_WORKER` sin entrar a `RECOVERY`.
- [ ] Un fallo que requiere volver a una fase temprana desde `RECOVERY` tiene arista legal.
- [ ] Ninguna desviación de máquina de estados es necesaria para corregir artefactos.
- [ ] §No-Skip Rule y las secciones "On Failure"/"Decision mapping" de H03 quedan coherentes con las aristas nuevas.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 1.2 / 3.1; F-02/F-03 |
| 2026-08-11 | Correcciones de auditoría: No-Skip Rule, H03 On Failure/Decision mapping, semántica de `artifact_exists` y condiciones exactas de la rama de H01 | Auditoría de planes 28-30 |
| 2026-08-11 | Aceptada (Accepted): implementación del plan 29 autorizada explícitamente por el usuario | Plan 29 Executed |
