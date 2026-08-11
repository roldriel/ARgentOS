# Plan 40 — Fronteras de artefactos de discovery y namespacing de `<order>`

**Status:** Aprobado para redacción
**Fecha:** 2026-08-11
**RFC:** RFC-41 (`plans/rfc/41-discovery-artifact-boundaries.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.8 / 5.2

## Objetivo

Documentar la excepción de intermedios de discovery en la regla de artefactos y evitar colisiones de `<order>` entre dominios.

## Criterio de entrada

- [ ] RFC-41 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: ubicaciones de outputs en la máquina de estados y la regla de `<order>` en `PROTOCOL_BOUNDARIES.md`.

## Entregables

1. `PROTOCOL_BOUNDARIES.md` con excepción de discovery y namespacing por dominio.
2. `DISCOVERY_STATE_MACHINE.md` con outputs numerados con prefijo de dominio.
3. `D01-discovery-output.md` sin requisito de artefacto puente.

## Pasos

1. Editar `PROTOCOL_BOUNDARIES.md` (`Artifact Safety Rule`): agregar la excepción de `.project/<session-uuid>/discovery/` y la regla de unicidad de `<order>` por dominio (`D<order>-` para discovery).
2. Editar `DISCOVERY_STATE_MACHINE.md`: renombrar los outputs de sesión de discovery a `D<order>-ARTIFACT.md` en los estados que los producen.
3. Editar `D01-discovery-output.md`: `artifact_validated` apunta a las entradas en `knowledge/discovery/`; eliminar la referencia al puente.
4. Actualizar el backlog B-1 y B-4 de `plans/INDEX.md` (resolución de F-11 y F-20).
5. Ejecutar la verificación documental.

## Criterios de salida

- [ ] No hay `<order>` duplicado entre dominios en la especificación.
- [ ] La excepción de discovery está en el doc canónico de fronteras.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Revisión de la iteración real (sesión `d4ab6a93-...`) como caso de referencia: los nombres históricos quedan tal cual; los futuros siguen la nueva regla.

## Riesgos

- Medio: cambio de convención de nombres con impacto en adoptantes que usan discovery; se registra en `CHANGELOG.md`/`MIGRATION.md` al ejecutarse.

## Trazabilidad

- RFC-41; fricciones F-11 y F-20 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-1, B-4.
