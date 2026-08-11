# Plan 31 — Perfil unificado de la fase 02

**Status:** Executed
**Fecha:** 2026-08-11
**Ejecutado:** 2026-08-11 — autorización explícita del usuario (justificación documentada del gate de gobernanza); RFC-32 permanece `Proposal` (regularización pendiente).
**RFC:** RFC-32 (`plans/rfc/32-phase-02-profile-unification.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.4 (informe externo, no versionado en el repo)

## Objetivo

Eliminar la contradicción entre workflow, tabla de activación y guía de orquestación sobre quién ejecuta la fase 02.

## Criterio de entrada

- [ ] RFC-32 existe en `plans/rfc/` con status `Proposal`.
- [ ] Gobernanza: RFC-32 `Accepted` o plan re-clasificado a `Aprobado para ejecución` con justificación (regla de `plans/INDEX.md` §Convenciones). Sin ese gate no se ejecutan los Pasos sobre `.agents/`.
- [ ] Verificación contra el repo (estado actual esperado): front matter de `.agents/orchestrators/core/workflow/02-build-task-specification.md` con `profile: task_specification_writer`; fila `02-build-task-specification` de `.agents/skills/INDEX.md` con perfil `functional_writer`; fila `02-build-task-specification.md` de `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` §7. Mapping to workflow phases, con decisión `Generic worker`. Si el estado difiere, detener y reportar; no asumir.

## Entregables

1. `.agents/skills/INDEX.md` con la fila de fase 02 corregida (perfil → `task_specification_writer`).
2. `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` §7. Mapping to workflow phases, con el alcance de la guía aclarado y la celda de decisión de la fase 02 corregida.
3. `.agents/roles/task_specification_writer.md` verificado: lista de skills consistente con la tabla (sin cambio esperado: ya lista `ears-writer` y `task-spec-validator`).

## Pasos

1. En `.agents/skills/INDEX.md`, corregir la fila `02-build-task-specification`: columna Profile `functional_writer` → `task_specification_writer`; columna Skills sin cambios (`ears-writer, task-spec-validator`).
2. En `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` §7. Mapping to workflow phases:
   a. En la fila `02-build-task-specification.md`, reemplazar la celda Decision `Generic worker` por `Rol de fase fijo task_specification_writer (ver worker.md §Phase roles)`.
   b. Agregar bajo la tabla una nota: "La guía de 7 preguntas aplica solo a `06-execute.md`. Las fases 00–05 usan roles fijos asignados por su workflow (roles de fase, o perfiles fijos de fase como `intent_reflector` en 01); la columna Decision de 00–05 no se resuelve con las 7 preguntas."
3. Verificar `.agents/roles/task_specification_writer.md`: sus skills deben coincidir con la fila corregida de la tabla (`ears-writer`, `task-spec-validator`). Si coinciden, no editar; si difieren, alinear el rol a la tabla.
4. Verificar la nota del doble significado de `profile` en `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` §profile, y que `.agents/roles/worker.md` §Phase roles, incluye `task_specification_writer` para la fase 02. Cualquier inconsistencia adicional (p. ej. la categorización de `intent_reflector` en la fase 01) queda fuera del alcance: reportarla como `inconsistency` sin corregirla.
5. Ejecutar la verificación documental (comandos de Criterios de salida) y registrar la salida como evidencia.
6. Rollback si falla la verificación: `git restore` de `.agents/skills/INDEX.md` y `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`, o `git revert` del commit correspondiente.

## Criterios de salida

- [ ] Las tres fuentes nombran `task_specification_writer` para la fase 02: front matter del workflow 02, fila de `.agents/skills/INDEX.md` y celda Decision de la guía §7.
- [ ] `functional_writer` no aparece en `.agents/skills/INDEX.md`; sus apariciones restantes corresponden al perfil de documentación funcional (guía §3, catálogo de perfiles, contrato de delegación, `worker.md`, taxonomía).
- [ ] `.agents/roles/task_specification_writer.md` y la fila de la tabla declaran las mismas skills (`ears-writer`, `task-spec-validator`).
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Búsqueda del término `functional_writer` en `.agents/` y revisión de cada aparición: ninguna debe quedar en la tabla de activación; las apariciones como perfil de documentación funcional se mantienen.
- Búsqueda de `task_specification_writer` en las tres fuentes citadas (workflow 02, tabla de activación, guía §7).
- Consistencia tabla de activación ↔ roles de fase (skill `consistency-checker`).

## Riesgos

- Bajo: cambio documental de una fila y una aclaración; sin impacto en contratos. Mitigación: verificación mecánica (`check_protocol_invariants.py`, `check_plan_citations.py`) y rollback con `git restore`/`git revert`.

## Trazabilidad

- RFC-32; punto 1.4 de la auditoría (informe externo).
