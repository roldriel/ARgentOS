# RFC-32 — Perfil unificado de la fase 02

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.4
**Pregunta:** ¿Quién redacta la `TASK_SPECIFICATION.md` y qué skills activa, cuando tres documentos del protocolo responden distinto?
**Afectados:** `.agents/orchestrators/core/workflow/02-build-task-specification.md`, `.agents/skills/INDEX.md`, `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`, `.agents/roles/task_specification_writer.md`, `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.

## Problema

Tres fuentes definen de forma distinta el perfil de la fase 02:

1. El front matter del workflow 02 declara `profile: task_specification_writer` (`.agents/orchestrators/core/workflow/02-build-task-specification.md:Build Task Specification`).
2. La tabla de activación de skills mapea `02-build-task-specification | functional_writer` (`.agents/skills/INDEX.md:Activation table`).
3. La guía de orquestación dice que la fase 02 usa *Generic worker* (`.agents/standards/orchestration/ORCHESTRATION_GUIDE.md:7. Mapping to workflow phases`).

`functional_writer` es un perfil de documentación funcional para stakeholders de negocio (`.agents/roles/profiles/README.md:Profile list`), no la redacción de una task specification. La raíz del conflicto es el doble significado de `profile` documentado en el contrato de delegación (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md:profile`): rol de fase vs perfil especializado.

## Decisión propuesta

1. La fase 02 usa el **rol de fase** `task_specification_writer`, nunca un perfil de ingeniería ni el worker genérico a secas.
2. La tabla de activación de skills cambia su columna de fase 02 a `task_specification_writer` (manteniendo `ears-writer` y `task-spec-validator`).
3. `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md:7. Mapping to workflow phases` aclara que la guía de 7 preguntas solo aplica a la fase 06 y que las fases 00-05 usan roles de fase fijos.
4. El rol `task_specification_writer` se mantiene como el portador de las skills de la fase 02, alineado con `worker.md`.

## Alternativas consideradas

- **Usar `functional_writer` en fase 02**: mezcla el modelo de perfiles de negocio con la redacción de specs técnicas; se descarta.
- **Dejar la guía en "generic worker"**: pierde la declaración del rol de fase y sus skills; se descarta.
- **Crear un perfil nuevo**: innecesario; el rol de fase ya existe y cubre la responsabilidad.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `02-build-task-specification.md` | Sin cambio de rol (ya dice `task_specification_writer`); verificar coherencia. |
| `skills/INDEX.md` | Fila de fase 02 con `task_specification_writer`. |
| `ORCHESTRATION_GUIDE.md` | §7: aclarar alcance de la guía (solo fase 06). |
| `worker.md` | Confirmar que fase 01/02/... usan roles de fase. |

## Criterios de aceptación

- [ ] Las tres fuentes nombran el mismo rol para la fase 02.
- [ ] `functional_writer` solo aparece donde corresponde (documentación funcional en fase 06).
- [ ] La tabla de activación y el rol `task_specification_writer` declaran las mismas skills.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 1.4 |
| 2026-08-11 | Plan 31 ejecutado: cambios aplicados en `.agents/`; status permanece `Proposal` (regularización de gobernanza pendiente) | Plan 31 |
