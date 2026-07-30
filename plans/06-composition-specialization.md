# Plan — Nivel 3: Especialización de Context Composition

**Status:** Plan aprobado para redacción de RFCs

**Depends on:** Nivel 1 (RFC-00YD Composition Model — este nivel extiende Composition, no puede redactarse antes).

**Referencia:** `feature.md` → Planned Evolution → Nivel 3; sección "Future Extensions" de RFC-00YC

---

# Objetivo

Refinar cómo un Resolved Candidate Set se transforma en un Execution Context **bajo las restricciones del Context Budget**, sin modificar la responsabilidad general de Context Composition.

---

# RFCs del nivel

Los dos RFCs son independientes entre sí y paralelizables una vez cerrado el Nivel 1:

## RFC-00YI: Context Compression Model

- **Pregunta:** ¿Cómo se reduce el costo de representación de un conjunto ya resuelto?
- Opera **después** de Resolution: la compresión nunca reabre conflictos ni altera la membresía del Resolved Candidate Set; solo reduce su costo de representación.
- Debe explicitar la relación con el Budget: la compresión es una de las formas en que Composition satisface las restricciones (el Budget restringe; la compresión reduce costo; no son lo mismo).
- Non Goals: unidades de costo, algoritmos de compresión, límites concretos (heredado de RFC-00YA: el Budget no define unidades ni representación).

## RFC-00YJ: Context Optimization Model

- **Pregunta:** ¿Cómo se optimiza la representación final del Execution Context bajo las restricciones del Budget?
- Distinto de Compression: Compression reduce costo; Optimization mejora la adecuación de la representación al propósito de ejecución (p. ej., qué forma conceptual toma el contexto para el Worker), siempre sin redecidir prioridades ni conflictos.
- Debe declarar su orden conceptual respecto a Compression si ambos aplican (aunque sea solo a nivel conceptual: cuál opera primero y por qué), para no dejar ambigüedad en Composition.

---

# Riesgo a vigilar

La frontera Compression/Optimization es el punto más débil del roadmap: ambos "mejoran la representación bajo el Budget". Cada RFC debe incluir una sección "Relationship with the other model" que los distinga por la pregunta que responden, no por mecanismos. Si en la redacción resulta que responden la misma pregunta, escalar antes de escribir el segundo RFC (posible fusión en uno solo).

## Segunda frontera: Optimization (este nivel) ↔ Materialization (Nivel 4)

Optimization define "qué forma conceptual toma el contexto para el Worker"; Materialization (RFC-00YK) define "la transformación del Execution Context en una representación propia de un runtime". La diferencia entre *forma conceptual para el Worker* y *representación del runtime* es tan tenue como la de Compression/Optimization. Regla de corte sugerida para RFC-00YJ: Optimization opera **dentro** del modelo conceptual del protocolo (transforma el Execution Context sin salir de él); cualquier transformación que produzca una representación propia de un runtime pertenece al Nivel 4. RFC-00YJ debe declarar esta frontera explícitamente en su sección de relación con extensiones futuras.

---

# Actualizaciones transversales al cerrar el nivel

1. `feature.md` → Nivel 3: marcar ✔ y actualizar el índice de RFCs.
2. RFC-00YD: actualizar "Future Extensions" con referencias a 00YI/00YJ.
3. RFC-00YC: su "Future Extensions" ya menciona ambos modelos; reemplazar descripción por referencia.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC-00YI Compression | `plans/rfc/11-context-compression-model.md` |
| 2 | RFC-00YJ Optimization | `plans/rfc/12-context-optimization-model.md` |
| 3 | Updates a RFC-00YD, RFC-00YC y `feature.md` | archivos existentes |

# Fuera de alcance

- Materialización (→ Nivel 4): estos modelos siguen siendo conceptuales; no definen cómo un runtime representa el contexto comprimido u optimizado.
