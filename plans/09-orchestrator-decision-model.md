# Plan 09 — Orchestrator Decision Model

**Status:** Aprobado para redacción.

**Depends on:** plan 08 (elimina la contradicción de bootstrap que este plan modela). Conceptualmente independiente de 04–07, pero se recomienda redactarlo después para reutilizar su terminología.

**Referencia:** `plans/analisis-explicitud.md` (gaps 1 y 8); `orchestrators/core/roles/orchestrator.md`; `standards/requirements/INTENT_CONFIDENCE.md`; `standards/quality/CONFIDENCE.md`.

---

# Objetivo

Convertir las decisiones del Orchestrator — hoy dispersas como prosa en su rol — en un **modelo conceptual de decisiones**: una enumeración explícita de cada punto de decisión, su pregunta, sus inputs y su concepto de autoridad, sin algoritmos. Es el equivalente a RFC-00XZ (descomposición conceptual de Context Assembly) pero para el comportamiento decisorio del Orchestrator.

---

# Contenido

## A. RFC — Orchestrator Decision Model

Redactar `plans/rfc/` (los RFCs de la serie de explicitud numeran a partir de `rfc/16`; convención de `plans/INDEX.md`) con la estructura estándar:

- **Pregunta que responde:** ¿Qué decisiones toma el Orchestrator, sobre qué inputs, y con qué autoridad?
- **Contenido mínimo — el catálogo de puntos de decisión:**
  1. **Aceptación de transición:** cuándo el Orchestrator acepta el `recommendation.next_state` del worker y cuándo lo overridea. Introducir el concepto de autoridad sobre recomendaciones (hoy indefinido).
  2. **Routing de outcomes del reviewer:** APPROVE / REWORK / retry, incluyendo el *retry bound* (hoy: "typically one retry", prosa en `orchestrators/core/roles/orchestrator.md`, §"4.1 Optional reviewer invocation").
  3. **Frontera `NEEDS_CLARIFICATION` ↔ `RECOVERY`:** qué hace a una ambigüedad clarification-worthy vs. recuperable. Consume el modelo de confianza (B).
  4. **Criticidad de fallos de discovery:** abort / recovery / minimal-discovery — definir el concepto de criticidad de la KB para la tarea (hoy: "según cuán crítica sea", sin criterio).
  5. **Autoridad de aborto:** quién puede abortar una tarea y bajo qué concepto.
  6. **Bootstrap degradado:** modelizar conceptualmente la regla que resulte de ejecutar el plan 08 §A (decisión recomendada: FAIL bloquea salvo autorización explícita del usuario). Paso 0: verificar la enmienda aplicada en `.agents/orchestrators/system/`.
- **Non Goals:** algoritmos de decisión, heurísticas concretas, umbrales numéricos, cambios de runtime. Cada decisión queda definida por su *pregunta*, sus *inputs conceptuales* y su *concepto de autoridad*; el criterio concreto pertenece a futuras políticas.
- Decidir la ubicación canónica del modelo: ¿nuevo estándar `standards/orchestration/DECISIONS.md` o sección del rol? (El plan 08 no resuelve esto; es decisión de este plan.)

## B. Unificación de modelos de confianza

- La relación canónico/especialización ya existe: `standards/quality/CONFIDENCE.md` (§"Relationship to other standards") declara a `standards/requirements/INTENT_CONFIDENCE.md` como su especialización para interpretación de intención, y el propio `INTENT_CONFIDENCE.md` (§"Relationship to other standards") se declara especialización de CONFIDENCE. No hay que construirla.
- El gap real es doble (gap 8 de `plans/analisis-explicitud.md`): (a) el score numérico de INTENT_CONFIDENCE (0–8) no se mapea explícitamente a los niveles HIGH/MEDIUM/LOW de CONFIDENCE más allá de la etiqueta final; (b) no existe especialización para "confianza en recomendación", que los puntos de decisión A.1 y A.3 de este plan necesitan.
- Entregable: **enmienda a ambos estándares** (`INTENT_CONFIDENCE.md` + `CONFIDENCE.md`) que agregue el mapeo score→nivel y la especialización para recomendación. No es una RFC nueva.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Orchestrator Decision Model | `plans/rfc/` (a partir de `rfc/16`) |
| 2 | Mapeo score→nivel + especialización para recomendación (enmienda) | `standards/requirements/INTENT_CONFIDENCE.md` + `standards/quality/CONFIDENCE.md` |
| 3 | Updates a `orchestrator.md` (referencias conceptuales autocontenidas, sin citar `plans/`) | `.agents/orchestrators/core/roles/orchestrator.md` |

# Fuera de alcance

- Taxonomía de fallos que alimenta el routing (→ plan 10).
- Validez de delegaciones (→ plan 11).
- Criterios concretos de decisión (umbrales, políticas): quedan diferidos, igual que la serie de contexto difiere políticas.
