# Plan 09 — Orchestrator Decision Model

**Status:** Aprobado para redacción.

**Depends on:** plan 08 (elimina la contradicción de bootstrap que este plan modela). Conceptualmente independiente de 04–07, pero se recomienda redactarlo después para reutilizar su terminología.

**Referencia:** análisis de explicitud (gaps 1 y 8); `orchestrators/core/roles/orchestrator.md`; `standards/requirements/INTENT_CONFIDENCE.md`; `standards/quality/CONFIDENCE.md`.

---

# Objetivo

Convertir las decisiones del Orchestrator — hoy dispersas como prosa en su rol — en un **modelo conceptual de decisiones**: una enumeración explícita de cada punto de decisión, su pregunta, sus inputs y su concepto de autoridad, sin algoritmos. Es el equivalente a RFC-00XZ (descomposición conceptual de Context Assembly) pero para el comportamiento decisorio del Orchestrator.

---

# Contenido

## A. RFC — Orchestrator Decision Model

Redactar `plans/rfc/` (siguiente número libre de la serie) con la estructura estándar:

- **Pregunta que responde:** ¿Qué decisiones toma el Orchestrator, sobre qué inputs, y con qué autoridad?
- **Contenido mínimo — el catálogo de puntos de decisión:**
  1. **Aceptación de transición:** cuándo el Orchestrator acepta el `recommendation.next_state` del worker y cuándo lo overridea. Introducir el concepto de autoridad sobre recomendaciones (hoy indefinido).
  2. **Routing de outcomes del reviewer:** APPROVE / REWORK / retry, incluyendo el *retry bound* (hoy: "típicamente un reintento", prosa).
  3. **Frontera `NEEDS_CLARIFICATION` ↔ `RECOVERY`:** qué hace a una ambigüedad clarification-worthy vs. recuperable. Consume el modelo de confianza unificado (B).
  4. **Criticidad de fallos de discovery:** abort / recovery / minimal-discovery — definir el concepto de criticidad de la KB para la tarea (hoy: "según cuán crítica sea", sin criterio).
  5. **Autoridad de aborto:** quién puede abortar una tarea y bajo qué concepto.
  6. **Bootstrap degradado:** modelizar conceptualmente la regla canónica fijada en el plan 08 (FAIL bloquea; excepción = autorización explícita del usuario).
- **Non Goals:** algoritmos de decisión, heurísticas concretas, umbrales numéricos, cambios de runtime. Cada decisión queda definida por su *pregunta*, sus *inputs conceptuales* y su *concepto de autoridad*; el criterio concreto pertenece a futuras políticas.
- Decidir la ubicación canónica del modelo: ¿nuevo estándar `standards/orchestration/DECISIONS.md` o sección del rol? (El plan 08 no resuelve esto; es decisión de este plan.)

## B. Unificación de modelos de confianza

- `standards/requirements/INTENT_CONFIDENCE.md` (confianza en la interpretación del intent) y `standards/quality/CONFIDENCE.md` (confianza en artefactos) coexisten sin relación definida.
- Definir **un único modelo conceptual de confianza** con especializaciones por aplicación (intent, artefacto, recomendación), de modo que el punto de decisión A.3 tenga un concepto único que consumir.
- Entregable: RFC o enmienda a ambos estándares dejando uno como canónico y el otro como especialización.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Orchestrator Decision Model | `plans/rfc/` (número libre) |
| 2 | Modelo de confianza unificado | estándares de requirements/quality |
| 3 | Updates a `orchestrator.md` (referencias conceptuales autocontenidas, sin citar `plans/`) | `.agents/orchestrators/core/roles/orchestrator.md` |

# Fuera de alcance

- Taxonomía de fallos que alimenta el routing (→ plan 10).
- Validez de delegaciones (→ plan 11).
- Criterios concretos de decisión (umbrales, políticas): quedan diferidos, igual que la serie de contexto difiere políticas.
