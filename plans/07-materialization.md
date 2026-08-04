# Plan — Nivel 4: Materialización

**Status:** Plan aprobado para redacción de RFCs

**Depends on:** Nivel 1 (RFC-00YD). Conceptualmente también del Nivel 3 (Compression/Optimization), porque la materialización opera sobre el Execution Context ya compuesto.

**Referencia:** `feature.md` → Planned Evolution → Nivel 4, Stages 10–11

---

# Objetivo

Separar completamente el modelo conceptual del protocolo de los mecanismos concretos que un runtime usa para entregar el Execution Context a un Worker. Es el nivel que toca la frontera protocolo/runtime: los RFCs deben dejar esa frontera explícita, no difuminarla.

---

# RFCs del nivel

## RFC-00YK: Execution Context Materialization Model — primero

- **Pregunta:** ¿Cómo se define conceptualmente la transformación de un Execution Context en una representación propia de un runtime?
- Es el marco general del nivel: introduce el concepto de materialización, la frontera protocolo/runtime, y la regla de que múltiples materializaciones pueden coexistir para el mismo Execution Context sin alterar el modelo conceptual.
- Debe definir explícitamente la relación entre **Context Delivery** (la responsabilidad Context Delivery definida en RFC-00XZ: transporte del Execution Context vía Delegation Payload) y **Materialization** (representación propia del runtime). Hoy ningún documento define si Delivery es una forma de materialización, un paso posterior a ella, o un concepto ortogonal. Esta es la principal laguna conceptual que este nivel debe cerrar (ver `feature.md`, que omite Delivery por completo — fix C.7 del Nivel 1).
- Los otros dos RFCs del nivel son especializaciones de este (ver la salvedad de RFC-00YM más abajo).

## RFC-00YL: Prompt Rendering Model

- **Pregunta:** ¿Cómo materializa un runtime basado en prompts el Execution Context?
- Es la materialización que el runtime actual ya realiza de facto ("el runtime actual lo materializa como contexto inyectado al prompt" — `feature.md`, Philosophy). El RFC formaliza conceptualmente lo que hoy es implícito.
- Debe cubrir **todas** las variantes listadas en `feature.md` Stage 10 (prompt tradicional, system prompt, tool calls, MCP, retrieval dinámico, structured context, multi-message, runtime memory) o justificar explícitamente cuáles quedan fuera y por qué.
- **Declaración de frontera:** `feature.md` §Stage 10 declara que esa etapa "pertenece al runtime. No al protocolo"; por tanto 00YL modela la interfaz conceptual de esas variantes (qué preguntas responde cada una), no su mecanismo. Se preserva Runtime Independence (principio de `feature.md` §Architectural Principles).

## RFC-00YM: Skill Materialization Model

- **Pregunta:** ¿Cómo se materializa una Skill (capacidad conceptual reutilizable) en un runtime concreto?
- **Depende de RFC-00XX** (`plans/rfc/00-skill-capability-model.md`, Accepted): la definición conceptual de Skill como capacidad reutilizable independiente del mecanismo. Declararla explícitamente en "Relationship with Previous RFCs".
- **Salvedad sobre la jerarquía:** 00YM no es estrictamente una especialización de 00YK — sujeto distinto: 00YK materializa el Execution Context (resultado del pipeline); 00YM materializa una Skill, que es un *candidate* dentro del pipeline. La relación correcta es lateral: la materialización de una Skill ocurre como parte de la materialización del Execution Context que la contiene (en el runtime actual, las skills entran como fuente en Collection y viajan en el campo `skills: [...]` del delegation payload — ver `.agents/orchestrators/core/roles/orchestrator.md` §5, que describe Collection/Composition y la lista de campos del payload). Redactar la relación con 00YK en esos términos, no como herencia. (Nota 2 ago 2026: la cita original —"inyección de contexto durante Collection/Composition, ver `plans/skills-mechanism.md`"— era parcialmente fabricada: `skills-mechanism.md` no menciona Collection ni Composition (grep = 0); se reemplazó por la fuente real. Queda registrada.)

---

# Orden

```text
RFC-00YK  Materialization Model (marco general)
    ├── RFC-00YL  Prompt Rendering
    └── RFC-00YM  Skill Materialization     ← paralelizables
```

---

# Riesgo a vigilar

Este es el único nivel con impacto potencial más allá de "Conceptual": al formalizar Prompt Rendering se está describiendo lo que el runtime actual hace. Los RFCs deben declarar explícitamente en "Compatibility" si el runtime actual queda conforme por construcción o si existe desviación entre el modelo y la práctica actual (y en ese caso, si se documenta como deuda).

---

# Actualizaciones transversales al cerrar el nivel

1. `feature.md` → Nivel 4: marcar ✔; roadmap completo.
2. `feature.md` → Nivel 4: reordenar la lista de RFCs — hoy figura Prompt Rendering → Skill Materialization → Execution Context Materialization (`feature.md` §Planned Evolution → Nivel 4); debe quedar 00YK (Execution Context Materialization) → 00YL (Prompt Rendering) → 00YM (Skill Materialization), coherente con el orden y las dependencias de este plan.
3. Índice de RFCs en `feature.md` actualizado.
4. Verificar que la línea divisoria protocolo/runtime del diagrama (fix del Nivel 1) queda respaldada por RFC-00YK.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC-00YK Materialization Model | `plans/rfc/13-execution-context-materialization-model.md` |
| 2 | RFC-00YL Prompt Rendering | `plans/rfc/14-prompt-rendering-model.md` |
| 3 | RFC-00YM Skill Materialization | `plans/rfc/15-skill-materialization-model.md` |
| 4 | Updates a `feature.md` | archivo existente |

# Fuera de alcance

- Implementación real de renderers, tool calls, MCP o memoria en el runtime (los RFCs son conceptuales; la implementación sería un plan posterior fuera de este roadmap).
