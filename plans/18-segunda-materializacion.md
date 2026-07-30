# Plan 18 — Segunda Materialización (runtime MCP/tools/memoria)

**Status:** Aprobado para redacción.

**Depends on:** plan 07 (RFC-00YK Materialization Model, RFC-00YM Skill Materialization). Recomendado también 15 (Budget materializado, para medir la segunda materialización con la misma vara).

**Referencia:** `plans/07-materialization.md`; `feature.md` (Philosophy: "Futuros runtimes podrían materializarlo mediante herramientas, memoria, APIs, recuperación dinámica, MCP u otros mecanismos sin modificar este modelo conceptual").

---

# Objetivo

**La prueba de fuego de la tesis central de ARgentOS.** Implementar una materialización del Execution Context distinta de la inyección de prompt — vía MCP, tool calls o memoria de runtime — demostrando empíricamente que el modelo conceptual (RFCs 00XX–00YM) no se modifica en lo más mínimo.

---

# Contenido

## A. Selección del mecanismo

Elegir **una** segunda materialización (criterio: la de mayor valor práctico para el runtime actual, no la más exótica):

1. **MCP:** skills o conocimiento entregados como herramientas MCP en vez de texto inyectado.
2. **Tool calls:** capacidades invocables bajo demanda (materialización lazy real de skills, extendiendo el mecanismo de `references/`).
3. **Runtime memory:** parte del Execution Context persistida y recuperada dinámicamente en vez de inyectada.

Decidir en el arranque del plan con una comparativa corta (costo, valor, riesgo) — no implementar las tres.

## B. Implementación de la materialización

- Adaptador que toma un Execution Context (o la porción elegida: skills como primer candidato, vía RFC-00YM) y lo materializa por el mecanismo elegido.
- Criterios de conformidad explícitos (del plan 07): qué debe cumplir la materialización para ser conforme al modelo.
- Interacción con el Budget materializado (plan 15): qué consume este mecanismo y cómo se estima.

## C. Verificación de la tesis (entregable central)

- **Cero modificaciones** a `plans/rfc/00–05` ni a los conceptos de `.agents/`: si algo conceptual debe tocarse, la tesis falla y se documenta como hallazgo.
- Ejercicio comparativo: la misma tarea ejecutada con ambas materializaciones, documentando diferencias observables (costo, latencia, calidad percibida).
- Enmienda a los RFCs de materialización solo en sus secciones "Compatibility": declarar si el runtime queda conforme por construcción o si hay desviación (como exige el plan 07).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Comparativa y decisión de mecanismo | `plans/` (anexo de este plan) |
| 2 | Segunda materialización funcional | runtime (fuera de `.agents/` salvo estándar) |
| 3 | Reporte de verificación de la tesis | `plans/` (¿el modelo sobrevivió intacto?) |
| 4 | Updates de Compatibility en RFCs 00YK/00YM | `plans/rfc/` |

# Fuera de alcance

- Tercera y cuarta materialización (quedan como ejercicios futuros si la tesis se verifica).
- Deprecar la materialización prompt (coexisten; el modelo lo permite explícitamente).
