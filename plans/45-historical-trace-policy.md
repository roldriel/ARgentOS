# Plan 45 — Política de trazas históricas no reproducibles

**Status:** Aprobado para redacción
**Fecha:** 2026-08-11
**RFC:** RFC-46 (`plans/rfc/46-historical-trace-policy.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 4.1

## Objetivo

Declarar la versión de protocolo en las trazas de sesión y definir la interpretación de trazas de versiones anteriores.

## Criterio de entrada

- [ ] RFC-46 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: encabezados actuales de los contratos de sesión.

## Entregables

1. `SESSION_LOG.md` con `protocol_version`.
2. `METRICS.md` con `protocol_version` en `session_start`.
3. `HARNESS_REPORT.md` con nota de versión.
4. Nota histórica en `plans/INDEX.md`.

## Pasos

1. Editar el contrato `SESSION_LOG.md`: campo `protocol_version` en el encabezado y en la entrada inicial.
2. Editar `METRICS.md`: `protocol_version` en el evento `session_start`.
3. Editar `HARNESS_REPORT.md`: nota de versión en el encabezado.
4. Agregar la nota histórica en `plans/INDEX.md` (runner hasta 2.0.0; juicio desde 2.0.0).
5. Ejecutar la verificación documental.

## Criterios de salida

- [ ] Los tres contratos de sesión declaran versión.
- [ ] La nota histórica explica la diferencia de modos de evaluación.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Lectura de la traza `d4ab6a93-...` como caso de validación de la regla (sin reescribirla).

## Riesgos

- Bajo: cambio de contrato aditivo (campos nuevos opcionales).

## Trazabilidad

- RFC-46; punto 4.1 de la auditoría.
