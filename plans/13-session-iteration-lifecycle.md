# Plan 13 — Session & Iteration Lifecycle Model

**Status:** Aprobado para redacción. Independiente; paralelizable con cualquier otro plan.

**Depends on:** — (ninguno).

**Referencia:** análisis de explicitud (gap 4); `standards/runtime/PROTOCOL_BOUNDARIES.md`; `orchestrators/core/states/AGENT_STATE_MACHINE.md`; `orchestrators/core/roles/orchestrator.md` §1.

---

# Objetivo

Definir conceptualmente el **ciclo de vida de una sesión y de sus iteraciones**, hoy disperso y definido solo por ejemplos: cuándo empieza y termina una sesión, cuándo se abre una iteración nueva, cómo se secuencian los artefactos (`<order>`), y qué integridad deben mantener `SESSION_LOG.md` y `SESSION_BRIEF.md`.

---

# Contenido

## A. RFC — Session & Iteration Lifecycle Model

- **Pregunta que responde:** ¿Qué es una sesión, qué es una iteración, y qué reglas conceptuales gobiernan su ciclo de vida?
- **Contenido mínimo:**
  1. **Límites de sesión:** qué inicia una sesión, qué la termina, qué significa reanudarla (`kimi resume`, estado persistido, cron tasks).
  2. **Límites de iteración:** cuándo el trabajo abre `.project/<session-uuid>/<iteration>/` nuevo vs. continúa en el actual (hoy solo ejemplos en BOUNDARIES).
  3. **Secuencia de artefactos:** regla conceptual de `<order>` dentro de una iteración.
  4. **Integridad de artefactos de sesión:** qué hace íntegro a un `SESSION_LOG.md` / `SESSION_BRIEF.md` (tienen contrato pero ningún trigger los valida) y qué clase de fallo es su violación (hook a la taxonomía del plan 10 cuando exista).
  5. **Artefactos retroactivos:** concepto de *desviación retroactiva* (crear un artefacto fuera de su fase), hoy disperso entre BOUNDARIES, la regla no-skip de la state machine y orchestrator §1.

## B. Aplicación transversal

- Consolidar las reglas dispersas (BOUNDARIES + state machine + orchestrator §1) en referencias autocontenidas al modelo.
- Declarar como Future Extension la validación por harness de integridad de sesión (no implementarla).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Session & Iteration Lifecycle Model | `plans/rfc/` (número libre) |
| 2 | Updates a BOUNDARIES / state machine / orchestrator.md | archivos existentes |

# Fuera de alcance

- Políticas de retención, limpieza o archivado de sesiones.
- Nuevas policies de harness (quedan declaradas como Future Extension).
- Cambios al layout de `.project/`.
