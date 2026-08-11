# Plan 29 — Recovery a fases tempranas

**Status:** Executed
**Fecha:** 2026-08-11
**Aprobación:** Autorización explícita del usuario (2026-08-11) para implementar el plan; RFC-30 pasó a `Accepted`. Criterios de salida verificados: invariantes y citas OK.
**RFC:** RFC-30 (`plans/rfc/30-recovery-to-early-phases.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.2 / 3.1
**Revisión:** 2026-08-11 — correcciones de auditoría (No-Skip Rule, H03 On Failure/Decision mapping, aristas y condiciones enumeradas, semántica de `artifact_exists`, gate de gobernanza).

## Objetivo

Cerrar el hueco que obliga a registrar desviaciones para corregir artefactos de fases tempranas tras un fallo de gate.

## Criterio de entrada

- [ ] RFC-30 existe en `plans/rfc/` con status `Proposal`.
- [ ] Gate de gobernanza para ejecución: RFC-30 `Accepted`, o plan `Aprobado para ejecución` con justificación, antes de modificar `.agents/` (regla RFC-42 en `plans/INDEX.md` §Convenciones).
- [ ] Verificación contra el repo de las secciones citadas (máquina de estados, H01, H03, workflow 08). Las tablas de recovery vigentes viven en los policies (sección `## Recovery Decision Table`); las referencias a `decision_trees/` del anexo 19 (F-02/F-03) son históricas y no se usan como anclas.

## Entregables

1. Máquina de estados con aristas explícitas `RECOVERY → ANALYZING_TASK | BUILDING_TASK_SPECIFICATION | GATHERING_CONTEXT | VALIDATING_CONTEXT` (se mantienen `PLANNING`, `NEEDS_CLARIFICATION` y `ABORT`) y `RETRY_WORKER` definido como acción correctiva sin transición; §No-Skip Rule actualizada.
2. Policy H01 con rama de retry para fallos de formato y "On Failure" alineado.
3. Workflow 08 con la distinción retry-sin-transición vs transición a fase temprana y el mapeo artefacto → fase destino.
4. Revisión de coherencia de H00/H02/H03/H04/H11 (tablas de recovery, "On Failure" y "Decision mapping") con las aristas nuevas.

## Pasos

1. Editar `AGENT_STATE_MACHINE.md`: en `RECOVERY`, agregar las aristas a `ANALYZING_TASK`, `BUILDING_TASK_SPECIFICATION`, `GATHERING_CONTEXT` y `VALIDATING_CONTEXT` (manteniendo `PLANNING`, `NEEDS_CLARIFICATION` y `ABORT`) y definir `RETRY_WORKER` como acción correctiva que no cambia estado; actualizar §No-Skip Rule para que sus destinos de recovery incluyan las fases tempranas.
2. Editar la tabla de recovery de H01: agregar, entre la rama de ambigüedad y la rama `retry_count >= 1`, la rama `RETRY_WORKER` con condición `artifact_exists == true`, `objective_is_ambiguous == false`, `scope_is_clear == true`, `retry_count == 0`, destino `02-build-task-specification.md` (retry sin transición). Definir `artifact_exists`: `false` = artefacto ausente o a regenerar; `true` = artefacto presente con fallo de formato.
3. Alinear la sección "On Failure" de H01 con la tabla.
4. Editar `08-recovery.md`: documentar las salidas a fases tempranas con el mapeo artefacto → destino (`TASK_ANALYSIS` → `ANALYZING_TASK`, `TASK_SPECIFICATION` → `BUILDING_TASK_SPECIFICATION`, `CONTEXT_ARTIFACT` → `GATHERING_CONTEXT`, `CONTEXT_VALIDATION_REPORT` → `VALIDATING_CONTEXT`, `EXECUTION_PLAN` → `PLANNING`), la distinción retry-sin-transición vs transición, y el registro de causa en `SESSION_LOG.md`.
5. Alinear H03: actualizar su "On Failure" y "Decision mapping" para que el retorno a `GATHERING_CONTEXT` se modele con la arista nueva y definir `VALIDATING_CONTEXT` como destino para la reescritura del `CONTEXT_VALIDATION_REPORT`. Auditar H00/H02/H04/H11: confirmar que sus `RETRY_WORKER` apuntan a la fase actual (sin arista) y que las fases destino son alcanzables desde `RECOVERY`.
6. Actualizar el backlog B-2 de `plans/INDEX.md` para reflejar la resolución.

## Criterios de salida

- [ ] Ninguna corrección de artefacto requiere una desviación de máquina de estados (incluye "On Failure" y "Decision mapping" de H03).
- [ ] Las tablas de recovery, las secciones "On Failure"/"Decision mapping" y la máquina de estados usan los mismos `target_phase` y destinos legales.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Simulación documental de los escenarios: fallo de formato (retry sin transición), fallo con corrección de fase temprana (arista nueva, incluido H03 → `GATHERING_CONTEXT`), fallo no recuperable (ABORT).
- Consistencia entre tablas de recovery y máquina de estados (skill `consistency-checker`).

## Riesgos

- Ampliar las aristas de `RECOVERY` sin acotar el retry: mitigado con `retry_count` y reglas existentes de re-invocación única.
- Cambio MAJOR del modelo de estados: requiere `CHANGELOG.md` y `MIGRATION.md` al ejecutarse.

## Trazabilidad

- RFC-30; fricciones F-02 y F-03 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-2.
