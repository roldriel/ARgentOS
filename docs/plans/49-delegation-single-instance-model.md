# Plan 49 — Modelo de ejecución de delegaciones en una sola instancia

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-50 (`plans/rfc/50-delegation-single-instance-model.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 5.1

## Objetivo

Modelar el modo single-instance sin degradar la separación de roles ni el valor del harness.

## Criterio de entrada

- [ ] RFC-50 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: secciones citadas en orquestador, DECISIONS y SESSION_LOG.

## Entregables

1. `orchestrator.md` con modos de ejecución y mitigaciones.
2. `SESSION_LOG.md` con declaración de modo.
3. `DECISIONS.md` con la nota de autoridad independiente del modo.

## Pasos

1. Definir los dos modos y sus condiciones en `orchestrator.md` (`5. Worker Delegation`).
2. Definir las mitigaciones del modo single-instance (verificación separada, evidencia escrita, registro de riesgo).
3. Agregar la declaración de modo al contrato `SESSION_LOG.md` y a la entrada inicial.
4. Actualizar `DECISIONS.md` (`D1 — Transition acceptance`) con la nota de modo.
5. Actualizar el backlog B-8 de `plans/INDEX.md` (resolución de F-09).
6. Ejecutar la verificación documental.

## Criterios de salida

- [ ] Los modos están declarados y son auditablemente distintos.
- [ ] Las mitigaciones del single-instance están especificadas.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Revisión de la traza del dogfooding contra el modelo propuesto (qué habría cambiado con las mitigaciones).

## Riesgos

- Medio: toca el modelo de ejecución; requiere acuerdo sobre las restricciones del modo single-instance.

## Trazabilidad

- RFC-50; fricción F-09 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-8.

## Nota de ejecución

Ejecutado el 2026-08-12 (vía RFC-50 Accepted). Modos de ejecución declarados
en la sección 5 (Worker Delegation) del rol orquestador (subagente recomendado; single-instance permitido
con tres mitigaciones: verificación como pasada de juicio separada con
evidencia escrita por ítem, prohibición de auto-aceptar sin evidencia,
registro del modo como riesgo en `METRICS.md`); declaración de modo en el
encabezado de `SESSION_LOG.md`; nota de autoridad independiente del modo en
`DECISIONS.md` (D1). Con estas mitigaciones, la traza del dogfooding (F-09)
habría exigido una pasada de verificación separada con evidencia escrita.
Resuelve B-8. Versión 3.5.0. Verificación: invariantes OK, citas OK,
estructura OK, 121 passed.
