# Plan 46 — Dogfooding del modo enforced

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-47 (`plans/rfc/47-enforced-mode-dogfooding.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 4.2

## Objetivo

Verificar empíricamente el modo enforced y dejar evidencia reproducible de su comportamiento.

## Criterio de entrada

- [ ] RFC-47 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: ausencia de `state.json` y estado de los planes 26/27.

## Entregables

1. Test de integración del flujo enforced en `.agents/harness/tests/`.
2. Evidencia de ejecución (salida de la simulación).
3. `ADOPTION.md` con comportamiento verificado.
4. `plans/INDEX.md` con status actualizado.

## Pasos

1. Diseñar la simulación: sesión e iteración de fixture, gates H04/H06 simulados.
2. Ejercitar `runner_state.py` (registro, lectura, estado vacío fail-closed).
3. Ejercitar `hook_gate.py` (deny antes de H04, allow después, deny de `Stop` sin cierre, allow con H06/`NEEDS_CLARIFICATION`).
4. Ejercitar el scan de bypass post-H04 con archivos modificados en la ventana.
5. Agregar el test de integración a la suite.
6. Actualizar `ADOPTION.md` y `plans/INDEX.md` con los resultados.
7. Ejecutar `python -m pytest .agents/harness/tests/`.

## Criterios de salida

- [ ] El test de integración cubre allow/deny y cierre.
- [ ] `state.json` se crea y se consume correctamente.
- [ ] `python -m pytest .agents/harness/tests/` pasa.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Revisión de la evidencia de ejecución y de los resultados en `ADOPTION.md`.

## Riesgos

- Medio: puede revelar fallos del flujo enforced; el resultado esperado es ajustar el código o la documentación.

## Trazabilidad

- RFC-47; punto 4.2 de la auditoría; planes 26/27 de `plans/INDEX.md`.

## Nota de ejecución

Ejecutado el 2026-08-12 (vía RFC-47 Accepted). Diseño de la simulación: los
scripts se copian a un layout adoptado en tmp y se ejercitan por subprocess
(sin monkeypatching), exactamente como los invocaría un CLI adoptante.
Cobertura verificada: deny de `Write`/`Edit` sin H04; allow dentro de
`.project/`; registro de H04/H06 vía CLI de `runner_state.py` con
`state.json` creado y consumido; deny de `Stop` sin cierre; allow con H06 y
con estado terminal `COMPLETED`; alerta del scan de bypass ante un archivo
del proyecto modificado antes del PASS. Resultado: 3 tests nuevos, suite del
harness 39/39 en verde — el flujo enforced funciona como está documentado;
no fue necesario ajustar código. `docs/ADOPTION.md` gana §6.2
(comportamiento verificado); planes 25/26 actualizados a "dogfooding
verificado" en el INDEX. Versión 3.7.0. Verificación: invariantes OK, citas
OK, estructura OK, 121 passed (repo) + 39/39 (harness).
