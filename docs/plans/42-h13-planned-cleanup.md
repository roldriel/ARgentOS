# Plan 42 — Limpieza de la regla de entidades `planned` en H13

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-43 (`plans/rfc/43-h13-planned-cleanup.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.10

## Objetivo

Eliminar la referencia vigente a entidades `planned` que ya no existen.

## Criterio de entrada

- [ ] RFC-43 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: ausencia de `status: planned` en la taxonomía.

## Entregables

1. `H13-protocol-taxonomy.md` sin regla vigente de entidades `planned` (nota histórica opcional).
2. Verificación de `PROTOCOL_TAXONOMY.md`.

## Pasos

1. Editar la regla 9 de H13: convertirla en nota histórica o eliminarla.
2. Ejecutar búsqueda de `planned` en la taxonomía y en el protocolo.
3. Ejecutar la verificación documental.

## Criterios de salida

- [ ] H13 no presupone entidades `planned`.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Búsqueda textual de `planned` en `.agents/`.

## Riesgos

- Bajo: cambio documental.

## Trazabilidad

- RFC-43; punto 2.10 de la auditoría.

## Nota de ejecución

Ejecutado el 2026-08-12 (vía RFC-43 Accepted). Regla 9 de H13 convertida en
nota histórica (con instrucción de restauración si el mecanismo se
reintroduce). Verificado: ninguna entidad con `status: planned` en la
taxonomía; las demás apariciones de "planned" en el payload son prosa sin
relación (deviation/unplanned_changes). Versión 3.3.1. Verificación:
invariantes OK, citas OK, estructura OK, 116 passed.
