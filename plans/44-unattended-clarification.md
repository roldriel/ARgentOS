# Plan 44 — Modo desatendido de clarificación

**Status:** Aprobado para redacción
**Fecha:** 2026-08-11
**RFC:** RFC-45 (`plans/rfc/45-unattended-clarification.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 3.3

## Objetivo

Agregar un modo desatendido opt-in para sesiones sin usuario en línea, con defaults declarados y confirmación diferida.

## Criterio de entrada

- [ ] RFC-45 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo de las secciones citadas.

## Entregables

1. `AGENT_STATE_MACHINE.md` con nota de modo desatendido.
2. `NO_ASSUMPTIONS.md` con la sección de modo desatendido.
3. `SESSION_BRIEF.md` con `source: unattended_default`.
4. `SESSION_LOG.md` con el registro de confirmación pendiente.

## Pasos

1. Definir el formato de la política de defaults (clase de ambigüedad → default → condición).
2. Editar `NO_ASSUMPTIONS.md`: nueva sección que delimita el modo desatendido y su opt-in.
3. Editar `AGENT_STATE_MACHINE.md` (`NEEDS_CLARIFICATION`): flujo desatendido vs bloqueo.
4. Editar `SESSION_BRIEF.md`: campo `source` con valor `unattended_default`.
5. Editar `SESSION_LOG.md`: evento/registro `PENDING_USER_CONFIRMATION`.
6. Actualizar el backlog B-5 de `plans/INDEX.md` (resolución de F-05).
7. Ejecutar la verificación documental.

## Criterios de salida

- [ ] El modo desatendido es opt-in y está delimitado.
- [ ] Toda decisión desatendida queda marcada pendiente de confirmación.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Simulación documental: sesión desatendida con ambigüedad cubierta → default aplicado y marcado; ambigüedad no cubierta → detención.

## Riesgos

- Alto si se diseña mal: puede normalizar asumir. Mitigación: opt-in + límite de cobertura + confirmación diferida obligatoria.

## Trazabilidad

- RFC-45; fricción F-05 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-5.
