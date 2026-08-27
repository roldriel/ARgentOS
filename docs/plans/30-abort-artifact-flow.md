# Plan 30 — ABORT en el flujo de artefacto y de cierre

**Status:** Executed
**Fecha:** 2026-08-11
**Aprobación:** Autorización explícita del usuario (2026-08-11) para implementar el plan; RFC-31 pasó a `Accepted`. Criterios de salida verificados: tests del harness (36 OK), invariantes y citas OK.
**RFC:** RFC-31 (`plans/rfc/31-abort-artifact-flow.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.3 / 3.4
**Revisión:** 2026-08-11 — correcciones de auditoría (registro de estado terminal en `runner_state.py`, alineación de `harness/INDEX.md`, mecanismo de `NEEDS_CLARIFICATION` explícito, gate de gobernanza).

## Objetivo

Dar soporte de artefacto y de cierre a la transición `RECOVERY → ABORT` ya existente en la máquina de estados.

## Criterio de entrada

- [ ] RFC-31 existe en `plans/rfc/` con status `Proposal`.
- [ ] Gate de gobernanza para ejecución: RFC-31 `Accepted`, o plan `Aprobado para ejecución` con justificación, antes de modificar `.agents/` (regla RFC-42 en `plans/INDEX.md` §Convenciones).
- [ ] Verificación contra el repo: secciones citadas existen en contrato, workflow, hook, `runner_state.py`, `harness/INDEX.md` y `DECISIONS.md`.

## Entregables

1. Contrato `RECOVERY_REPORT.md` con `ABORT` en el enum de recomendación.
2. Workflow `08-recovery.md` con el procedimiento de abort fundado.
3. `runner_state.py` con registro de estado terminal (`status` = `ABORT`/`COMPLETED`) y tests.
4. `hook_gate.py` con reconocimiento de estado terminal en `Stop`.
5. `.agents/harness/INDEX.md` (§Protocol State and Hook Enforcement) alineado con la condición de cierre.
6. Referencias cruzadas en `DECISIONS.md`.

## Pasos

1. Editar el contrato `RECOVERY_REPORT.md`: agregar `ABORT` a los valores posibles de `recommended_next_state` y su regla de causa fundada.
2. Editar `08-recovery.md`: documentar `RECOVERY → ABORT` como salida posible, con registro de causa en `SESSION_LOG.md` y sin trabajo posterior.
3. Editar `runner_state.py`: agregar una acción de CLI que registre estado terminal (p. ej. `terminal --state ABORT|COMPLETED`) escribiendo `status` en `state.json`, manteniendo la escritura transaccional y la invariante "solo `runner_state.py` escribe `state.json`".
4. Editar `hook_gate.py`: en el evento `Stop`, permitir cierre cuando `state.json.status` es `ABORT` o `COMPLETED`, manteniendo las condiciones actuales (H06 PASS o `NEEDS_CLARIFICATION` registrado en `TASK_ANALYSIS.md`).
5. Actualizar `.agents/harness/INDEX.md` (§Protocol State and Hook Enforcement): layout de `state.json` con `status` terminal y condición de cierre por `Stop`.
6. Actualizar `DECISIONS.md` (`D5`) para referenciar el artefacto (`RECOVERY_REPORT.md`) como portador de la causa.
7. Agregar o actualizar tests de `hook_gate.py` (cierre por `ABORT` con fixture de estado terminal) y de `runner_state.py` (registro de estado terminal).

## Criterios de salida

- [ ] El enum del contrato incluye `ABORT`.
- [ ] `runner_state.py` puede registrar `ABORT`/`COMPLETED` en `state.json` (test incluido).
- [ ] El hook no bloquea `Stop` tras `ABORT` con `state.json` en estado terminal (test incluido) y sigue bloqueando sin él.
- [ ] `python -m pytest .agents/harness/tests/` pasa (modo desarrollo).
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Test unitario del hook para cierre terminal: `ABORT` con estado registrado → allow; `ABORT` sin estado registrado → deny; sin H06 ni estado terminal → deny.
- Revisión de consistencia contrato ↔ workflow ↔ máquina de estados (skill `consistency-checker`).

## Riesgos

- Ampliar el cierre del hook a `ABORT` sin causa: la causa se exige en el artefacto y en `SESSION_LOG.md`; la revisión post-hoc sigue siendo posible.
- Cambio de contrato MAJOR: registrar en `CHANGELOG.md` al ejecutarse.

## Trazabilidad

- RFC-31; punto 1.3 / 3.4 de la auditoría.
