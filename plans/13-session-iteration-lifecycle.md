# Plan 13 — Session & Iteration Lifecycle Model

**Status:** Executed (5 ago 2026): RFC-22 (`rfc/22-session-iteration-lifecycle-model.md`) Accepted + updates a BOUNDARIES, state machine y orchestrator.md. Health-check PASS, pytest 278 passed.

**Depends on:** — (ninguno).

**Referencia:** `plans/analisis-explicitud.md` (gap 4); `standards/runtime/PROTOCOL_BOUNDARIES.md`; `orchestrators/core/states/AGENT_STATE_MACHINE.md`; `orchestrators/core/roles/orchestrator.md` (§"1. Session Management").

---

# Objetivo

Definir conceptualmente el **ciclo de vida de una sesión y de sus iteraciones**, hoy distribuido entre varios archivos y sin modelo conceptual que lo justifique: cuándo empieza y termina una sesión, cuándo se abre una iteración nueva, cómo se secuencian los artefactos (`<order>`), y qué integridad deben mantener `SESSION_LOG.md` y `SESSION_BRIEF.md`.

---

# Contenido

## A. RFC — Session & Iteration Lifecycle Model

- **Pregunta que responde:** ¿Qué es una sesión, qué es una iteración, y qué reglas conceptuales gobiernan su ciclo de vida?
- **Contenido mínimo:**
  1. **Límites de sesión:** qué inicia una sesión, qué la termina, qué significa reanudarla (reanudación de sesión por el runtime — p. ej. el comando de resume del CLI actual — y continuidad vía estado persistido).
  2. **Límites de iteración:** cuándo el trabajo abre `.project/<session-uuid>/<iteration>/` nuevo vs. continúa en el actual (hoy definido como regla MUST en BOUNDARIES §"Artifact Safety Rule", pero sin modelo conceptual que la justifique ni criterio para casos borde: reanudación, iteración parcial).
  3. **Secuencia de artefactos:** regla conceptual de `<order>` dentro de una iteración.
  4. **Integridad de artefactos de sesión:** qué hace íntegro a un `SESSION_LOG.md` / `SESSION_BRIEF.md` (tienen contrato pero ningún trigger los valida) y qué clase de fallo es su violación (hook a la taxonomía del plan 10 cuando exista).
  5. **Artefactos retroactivos:** concepto de *desviación retroactiva* (crear un artefacto fuera de su fase), hoy definido solo en dos lugares: la No-Skip Rule de `AGENT_STATE_MACHINE.md` ("A retroactive artifact created after execution to 'fill a gap' is a deviation…") y la constraint de `contracts/SESSION_LOG.md` (§"Constraints") que prohíbe reescribir el log retroactivamente.

## B. Aplicación transversal

- Consolidar las reglas hoy distribuidas (BOUNDARIES §"Artifact Safety Rule", state machine §"No-Skip Rule", contrato de SESSION_LOG §"Constraints", orchestrator §"1. Session Management"). Respetando la frontera documental (`.agents/` no referencia `plans/`): la regla canónica permanece inline en cada archivo de `.agents/`; la RFC solo documenta el modelo conceptual y los archivos de `.agents/` se reescriben autocontenidos, sin mencionar la RFC.
- Declarar como Future Extension la validación por harness de integridad de sesión (no implementarla).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Session & Iteration Lifecycle Model | `plans/rfc/` (a partir de `rfc/16`; 06–15 reservados por el roadmap EC, convención de `plans/INDEX.md`) |
| 2 | Updates a BOUNDARIES / state machine / orchestrator.md | archivos existentes |

# Fuera de alcance

- Políticas de retención, limpieza o archivado de sesiones.
- Nuevas policies de harness (quedan declaradas como Future Extension).
- Cambios al layout de `.project/`.
