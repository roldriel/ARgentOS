# Plan 51 — Catálogo de fases y skills en los roles de worker

**Status:** Aprobado para redacción
**Fecha:** 2026-08-11
**RFC:** RFC-52 (`plans/rfc/52-worker-role-phase-catalog.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 6.1

## Objetivo

Completar el catálogo de fases en `worker.md` y alinear las skills de los roles de fase con la tabla de activación.

## Criterio de entrada

- [ ] RFC-52 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: secciones citadas de `worker.md`, `recovery_analyst.md` y la tabla de activación.

## Entregables

1. `worker.md` con la fase 01 en "Phase roles".
2. `recovery_analyst.md` con skills alineadas.
3. Auditoría transversal de roles ↔ tabla de activación.

## Pasos

1. Editar `worker.md`: agregar `intent_reflector` (fase 01, perfil de fase) al catálogo.
2. Editar `.agents/roles/recovery_analyst.md:Skills`: agregar `risk-detector`.
3. Comparar cada rol de fase (`task_analyst`, `task_specification_writer`, `context_gatherer`, `context_validator`, `planner`, `executor`, `verifier`, `recovery_analyst`) contra la tabla de activación.
4. Corregir desfases encontrados.
5. Ejecutar la verificación documental.

## Criterios de salida

- [ ] Las 9 fases están en el catálogo.
- [ ] Rol y tabla coinciden en skills por fase.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Comparación programática de la sección `Skills` de cada rol contra la tabla de activación.

## Riesgos

- Bajo: cambio documental.

## Trazabilidad

- RFC-52; punto 6.1 de la auditoría.
