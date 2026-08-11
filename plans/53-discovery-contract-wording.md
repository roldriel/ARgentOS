# Plan 53 — Redacción de contratos de discovery (F-15 y F-19)

**Status:** Aprobado para redacción
**Fecha:** 2026-08-11
**RFC:** RFC-54 (`plans/rfc/54-discovery-contract-wording.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 6.4

## Objetivo

Eliminar las dos ambigüedades de redacción de discovery: ubicación del `project_shape` y actor del cálculo de hashes.

## Criterio de entrada

- [ ] RFC-54 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo de las secciones citadas.

## Entregables

1. `EXECUTIVE_SUMMARY.md` con sección `## Project Shape`.
2. `D01-discovery-output.md` ítem 9 alineado.
3. `DISCOVERY_STATE_MACHINE.md` con actor único de hashes.
4. `init_worker.md` con confirmación del actor.

## Pasos

1. Editar `EXECUTIVE_SUMMARY.md`: reemplazar "primera línea" por `## Project Shape` como primera sección de contenido.
2. Editar D01 ítem 9: verificar la sección `## Project Shape` en lugar de la primera línea.
3. Editar `DISCOVERY_STATE_MACHINE.md` (`Hash Calculation`): actor único `init_worker`; nota de que el core Orchestrator solo solicita el scope.
4. Verificar `init_worker.md` (`Tasks`) para consistencia.
5. Actualizar el backlog B-4 de `plans/INDEX.md` (resolución de F-15/F-19).
6. Ejecutar la verificación documental.

## Criterios de salida

- [ ] Ningún contrato exige "primera línea" literal.
- [ ] Un solo actor calcula hashes en la especificación.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Revisión de `executive_summary.md` real: su `## Summary`/contenido debe ajustarse a la nueva sección cuando se ejecute el plan.

## Riesgos

- Bajo: redacción de contratos; requiere regenerar o ajustar `executive_summary.md` en la KB al ejecutarse.

## Trazabilidad

- RFC-54; fricciones F-15 y F-19 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-4.
