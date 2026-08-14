# RFC-47 — Dogfooding del modo enforced

**Status:** Accepted (2026-08-12, revisión individual RFC-56; diseño aprobado, ejecución pendiente vía su plan)
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 4.2
**Pregunta:** ¿Cómo se valida empíricamente el modo enforced (state.json + hooks) antes de prometerlo en la adopción?
**Afectados:** `.agents/harness/runner_state.py`, `.agents/harness/hook_gate.py`, `.agents/harness/health_check.py`, `ADOPTION.md`, `plans/INDEX.md`.

## Problema

El modo enforced está implementado (tres scripts stdlib) y documentado (`ADOPTION.md:6. Modos de enforcement: declarativo (default) y enforced`), pero nunca se ejecutó end-to-end: no existe ningún `state.json` en `.project/`, `runner_state.py` nunca fue invocado en una sesión, y los planes 26/27 figuran `Executed` con "dogfooding pendiente" (`plans/INDEX.md:Quinta serie: de protocolo declarativo a protocolo enforced (5 ago 2026)`). El ciclo completo — H04 PASS registrado, hook `PreToolUse` permitiendo la escritura, hook `Stop` cerrando la iteración, detección de bypass — es teoría no verificada.

## Decisión propuesta

1. Ejecutar una sesión de prueba (o una simulación de harness con fixtures) que ejercite: registro de gates en `state.json` vía `runner_state.py`, decisión de `hook_gate.py` en `PreToolUse` (allow/deny antes y después de H04), cierre por `Stop` (H06 y `NEEDS_CLARIFICATION`), y el scan de bypass post-H04.
2. Ampliar la suite de tests de `.agents/harness/tests/` con un test de integración del flujo completo (fixtures de sesión e iteración).
3. Documentar el resultado en `ADOPTION.md` (comportamiento verificado) o ajustar las afirmaciones si el flujo falla; marcar los planes 26/27 como `Executed` solo cuando el dogfooding pase.

## Alternativas consideradas

- **Seguir sin dogfooding**: deja una promesa de adopción sin evidencia.
- **Eliminar el modo enforced**: descarta una capacidad ya implementada y documentada.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `.agents/harness/tests/` | Test de integración del flujo enforced. |
| `ADOPTION.md` | Resultado verificado o afirmaciones ajustadas. |
| `plans/INDEX.md` | Status de planes 26/27 actualizado. |

## Criterios de aceptación

- [ ] El flujo enforced completo se ejecuta de forma verificable.
- [ ] `state.json` se crea, lee y cierra correctamente en la prueba.
- [ ] `ADOPTION.md` describe comportamiento verificado.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 4.2 |
| 2026-08-12 | Accepted (revisión individual, RFC-56/plan 57): diseño aprobado; la ejecución sigue el track de su plan asociado. | Revisión de la serie Proposal (RFC-56) |
