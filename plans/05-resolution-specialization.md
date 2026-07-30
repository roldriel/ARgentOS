# Plan — Nivel 2: Especialización de Context Resolution

**Status:** Plan aprobado para redacción de RFCs

**Depends on:** RFC-00YC (Context Resolution), ya existente. **No** depende del Nivel 1: ninguna RFC de este nivel (00YE–00YH) toca Composition. Puede ejecutarse en paralelo al Nivel 1; la única coordinación necesaria es al cerrar el nivel (índice de RFCs y updates a `feature.md`, que el Nivel 1 también toca).

**Referencia:** `feature.md` → Planned Evolution → Nivel 2; sección "Future Extensions" de RFC-00YC

---

# Objetivo

Especializar los mecanismos conceptuales de resolución de conflictos **sin modificar** la responsabilidad general de Context Resolution (RFC-00YC). Cada RFC introduce exactamente una responsabilidad nueva (Incremental Evolution).

---

# Orden y dependencias internas

```text
RFC-00YE  Context Conflict Classification Model   ← primero (base conceptual)
    ├── RFC-00YF  Context Tie-Breaking Model
    ├── RFC-00YG  Context Merge Model
    └── RFC-00YH  Context Deduplication Model     ← 00YF/00YG/00YH paralelizables
```

## Paso 1 — RFC-00YE: Context Conflict Classification Model

- **Pregunta:** ¿Qué tipos de conflicto existen conceptualmente entre candidatos?
- Clasifica los conflictos que RFC-00YC dejó como lista abierta: incompatibilidad, exclusión mutua, redundancia, conflicto derivado del Budget, empate (equivalencia de prioridad).
- Cada clase queda disponible como dominio de una especialización posterior: empate → Tie-Breaking; redundancia → Deduplication; compatibles fusionables → Merge.
- **Por qué primero:** las tres RFCs siguientes consumen estas clases; sin clasificación, cada una definiría su propia taxonomía y se solaparían.

## Paso 2 — RFCs 00YF / 00YG / 00YH (paralelizables)

Cada una sigue la estructura estándar de la serie (Abstract con encadenamiento, Goals/Non Goals, Terminology, Conceptual Model, Relationship with Context Budget, Future Extensions, Alternatives, Compatibility, Documentation Impact):

| RFC | Pregunta | Extiende |
| --- | -------- | -------- |
| RFC-00YF Tie-Breaking | ¿Cómo se decide entre candidatos equivalentes en prioridad? | Resolution (sobre la clase "empate" de 00YE) |
| RFC-00YG Merge | ¿Cuándo dos candidatos compatibles se fusionan en uno? | Resolution (sobre la clase "compatibles/redundantes parciales") |
| RFC-00YH Deduplication | ¿Cómo se eliminan redundancias conceptuales del conjunto? | Resolution (sobre la clase "redundancia") |

Restricciones comunes (Non Goals de las tres): sin algoritmos, sin políticas concretas de desempate/fusión/deduplicación, sin administración del Budget, sin tocar Composition.

Nota: esto corrige la caracterización de RFC-00YC, cuyo *Future Extensions* describe Tie-Breaking como "definir **políticas** de desempate" — el update a RFC-00YC al cerrar el nivel debe enmendar también esa descripción.

# Riesgo a vigilar

La frontera Merge/Deduplication es débil: la tabla asigna a Merge la clase "compatibles/**redundantes parciales**" y a Deduplication la clase "redundancia". Son clases solapadas. RFC-00YE debe definirlas de forma disjunta (cada RFC incluirá una sección "Relationship with the other models"); si en la redacción resulta que una redundancia parcial es indistinguible de una redundancia, escalar antes de escribir el segundo RFC.

---

# Actualizaciones transversales al cerrar el nivel

1. `feature.md` → Nivel 2: marcar los cuatro ítems ✔ y actualizar el índice de RFCs.
2. RFC-00YC: actualizar "Future Extensions" reemplazando las descripciones por referencias a los RFCs concretos.
3. Verificar que ninguna RFC de este nivel reasigne responsabilidades: Resolution sigue produciendo un único Resolved Candidate Set; las especializaciones solo refinan *cómo* se obtiene.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC-00YE Conflict Classification | `plans/rfc/07-context-conflict-classification-model.md` |
| 2 | RFC-00YF Tie-Breaking | `plans/rfc/08-context-tie-breaking-model.md` |
| 3 | RFC-00YG Merge | `plans/rfc/09-context-merge-model.md` |
| 4 | RFC-00YH Deduplication | `plans/rfc/10-context-deduplication-model.md` |
| 5 | Updates a RFC-00YC y `feature.md` | archivos existentes |

# Fuera de alcance

- Compression / Optimization (→ Nivel 3).
- Políticas concretas de resolución y comportamiento ante conflictos irresolubles (ya diferido por RFC-00YC a "futuras RFCs de políticas").
