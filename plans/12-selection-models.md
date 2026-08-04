# Plan 12 — Selection Models (Profile & Skill)

**Status:** Aprobado para redacción.

**Depends on:** plan 11 (define la validez de la selección resultante) y planes 04–07 (reutiliza los conceptos de Context Candidate, Prioritization y Resolution de la serie de Execution Context).

**Referencia:** `plans/analisis-explicitud.md` (gap 3); `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`; `.agents/standards/orchestration/SKILLS.md`; `.agents/skills/INDEX.md`.

---

# Objetivo

Reemplazar los dos últimos mecanismos de delegación basados en "juicio del Orchestrator" — selección de perfil y activación de skills — por **modelos conceptuales de candidatura y selección**, análogos a los que la serie de contexto definió para candidates. Sin algoritmos: candidatura, selección, exclusión y empate como conceptos.

---

# Contenido

## A. RFC — Profile Selection Model

- **Pregunta que responde:** ¿Qué hace a una tarea candidata a un perfil especializado?
- **Contenido mínimo:**
  - Concepto de *candidatura de perfil* (hoy: 7 preguntas keyword-based en la guía, sin modelo de clasificación).
  - Concepto de *exclusión mutua* y de *empate entre perfiles*: hoy se resuelve con "dividir en subtareas secuenciales" — la decisión de división (orden, fronteras) es juicio sin concepto. Definir los conceptos de *divisibilidad* y *frontera de subtarea*.
  - Relación con la tabla de perfiles prohibidos (ya explícita; queda como instancia del concepto de exclusión).

## B. RFC — Skill Activation Model

- **Pregunta que responde:** ¿Qué hace a una skill candidata a activarse para una tarea?
- **Contenido mínimo:**
  - Concepto de *suficiencia de descripción*: qué debe contener la `description` de una skill para ser activable. Hoy la tabla de activación de `.agents/skills/INDEX.md` (§"Activation table") tiene estructura y eje de clasificación definidos (fase + perfil) pero ninguna entrada (`_(none yet)_`): el 100 % de las activaciones actuales es por juicio, porque la tabla no tiene entradas pese a tener eje definido — un criterio sin límites.
  - Concepto de *override justificado* (ya existe como práctica loggeada; formalizarlo conceptualmente).
  - Evaluar si la estructura existente de la tabla de activación (fase + perfil) es suficiente para el modelo de candidatura; si no, enmendar `.agents/skills/INDEX.md` §"Activation table" con los campos conceptuales que falten (p. ej. criterio de exclusión, override), manteniendo el eje fase+perfil.
  - Relación con RFC-00XX (Skill Capability Model): la activación opera sobre la capacidad conceptual, no sobre el mecanismo.

## C. Aplicación transversal

- Actualizar `ORCHESTRATION_GUIDE.md` y `SKILLS.md` con referencias conceptuales autocontenidas (sin citar `plans/`).
- Aplicar en `.agents/skills/INDEX.md` §"Activation table" el resultado de B (confirmar la estructura existente o enmendar los campos); las entradas concretas siguen fuera de alcance.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Profile Selection Model | `plans/rfc/` (a partir de `rfc/16`) |
| 2 | RFC Skill Activation Model | `plans/rfc/` (a partir de `rfc/16`) |
| 3 | Updates a guía, SKILLS.md y skills/INDEX.md | `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`, `.agents/standards/orchestration/SKILLS.md`, `.agents/skills/INDEX.md` |

# Fuera de alcance

- Algoritmos de matching, scoring o clasificación.
- Entradas concretas de la tabla de activación (se llenan por skill, caso por caso).
- Validación por harness de las selecciones (hook declarado en plan 11).
