# Plan 18 — Segunda Materialización (runtime MCP/tools/memoria)

**Status:** Executed (5 ago 2026). Entregables: anexo A `plans/18-anexo-a-comparativa-y-decision.md`, implementación de referencia en `runtime/` (tool calls), reporte de verificación de la tesis `plans/18-anexo-b-reporte-verificacion-tesis.md`, enmiendas Compatibility en RFC-00YK y RFC-00YM. Veredicto: la tesis se verifica — el modelo conceptual sobrevivió intacto.

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
2. **Tool calls:** capacidades invocables bajo demanda (materialización lazy real de skills, análogo conceptual a `references/` — lectura bajo demanda por el worker, ver `.agents/orchestrators/core/contracts/WORKER_DELEGATION_CONTRACT.md` — pero invocable por el runtime en vez de leído por el agente).
3. **Runtime memory:** parte del Execution Context persistida y recuperada dinámicamente en vez de inyectada.

Decidir en el arranque del plan con una comparativa corta (costo, valor, riesgo) — no implementar las tres.

## B. Implementación de la materialización

- Adaptador que toma un Execution Context (o la porción elegida: skills como primer candidato, vía RFC-00YM) y lo materializa por el mecanismo elegido.
- Criterios de conformidad explícitos (del plan 07): qué debe cumplir la materialización para ser conforme al modelo.
- Interacción con el Budget materializado (plan 15): qué consume este mecanismo y cómo se estima.

## C. Verificación de la tesis (entregable central)

- **Cero modificaciones** a `plans/rfc/00–05` ni a los conceptos de `.agents/`: si algo conceptual debe tocarse, la tesis falla y se documenta como hallazgo. Umbral: falla de la tesis = cambio en la responsabilidad de una etapa del pipeline; las enmiendas aclaratorias (precisar definiciones ambiguas descubiertas al materializar) se documentan como hallazgo menor, no como falla.
- Ejercicio comparativo: la misma tarea ejecutada con ambas materializaciones, documentando diferencias observables (costo, latencia, calidad). La calidad se declara explícitamente cualitativa: no existe rúbrica aplicable en `.agents/standards/quality/RUBRICS.md` (sus rúbricas cubren artefactos de sesión); si se quiere evaluación rúbrica, el plan define una rúbrica de comparación al arrancar.
- Enmienda a los RFCs de materialización solo en sus secciones "Compatibility": declarar si el runtime queda conforme por construcción o si hay desviación (como exige el plan 07).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Comparativa y decisión de mecanismo | `plans/` (anexo de este plan) |
| 2 | Segunda materialización funcional | directorio `runtime/` en la raíz del repo, con su propio README que declare sus convenciones y su frontera respecto de `.agents/` (no es protocolo: es una implementación de referencia) |
| 3 | Reporte de verificación de la tesis | `plans/` (¿el modelo sobrevivió intacto?) |
| 4 | Updates de Compatibility en RFCs 00YK/00YM (si esos RFCs existen al momento de ejecutar) | `plans/rfc/` |

# Fuera de alcance

- Tercera y cuarta materialización (quedan como ejercicios futuros si la tesis se verifica).
- Deprecar la materialización prompt (coexisten; el modelo lo permite explícitamente).
