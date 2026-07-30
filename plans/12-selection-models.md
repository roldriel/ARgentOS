# Plan 12 — Selection Models (Profile & Skill)

**Status:** Aprobado para redacción.

**Depends on:** plan 11 (define la validez de la selección resultante) y planes 04–07 (reutiliza los conceptos de Context Candidate, Prioritization y Resolution de la serie de Execution Context).

**Referencia:** análisis de explicitud (gap 3); `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`; `.agents/standards/orchestration/SKILLS.md`; `.agents/skills/INDEX.md`.

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
  - Concepto de *suficiencia de descripción*: qué debe contener la `description` de una skill para ser activable. Hoy la tabla de activación de `.agents/skills/INDEX.md` está **vacía** (`_(none yet)_`) y el 100 % de la activación es juicio con obligación de log — un criterio sin límites.
  - Concepto de *override justificado* (ya existe como práctica loggeada; formalizarlo conceptualmente).
  - Definir la estructura conceptual de la tabla de activación (qué campos conceptuales tiene una entrada) para que deje de ser una lista vacía sin modelo.
  - Relación con RFC-00XX (Skill Capability Model): la activación opera sobre la capacidad conceptual, no sobre el mecanismo.

## C. Aplicación transversal

- Actualizar `ORCHESTRATION_GUIDE.md` y `SKILLS.md` con referencias conceptuales autocontenidas (sin citar `plans/`).
- Poblar la estructura de la tabla de activación en `.agents/skills/INDEX.md` (la estructura, no las entradas).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Profile Selection Model | `plans/rfc/` (número libre) |
| 2 | RFC Skill Activation Model | `plans/rfc/` (número libre) |
| 3 | Updates a guía, SKILLS.md y skills/INDEX.md | archivos existentes |

# Fuera de alcance

- Algoritmos de matching, scoring o clasificación.
- Entradas concretas de la tabla de activación (se llenan por skill, caso por caso).
- Validación por harness de las selecciones (hook declarado en plan 11).
