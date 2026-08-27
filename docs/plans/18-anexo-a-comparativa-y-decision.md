# Plan 18 — Anexo A: Comparativa de mecanismos y decisión

**Status:** Executed (anexo del plan `plans/18-segunda-materializacion.md`, §A. Selección del mecanismo).

**Fecha:** 2026-08-05.

---

# Criterio de selección

El plan fija el criterio (`plans/18-segunda-materializacion.md`, §A):

> la de mayor valor práctico para el runtime actual, no la más exótica.

El runtime actual es un agente CLI basado en prompts con soporte nativo de tool calls (el Worker ya invoca herramientas de lectura, edición y shell durante la ejecución — observable en `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §Worker Execution, donde el Worker lee archivos bajo demanda).

# Comparativa

| Dimensión | 1. MCP | 2. Tool calls | 3. Runtime memory |
| --- | --- | --- | --- |
| Costo de implementación | Alto: exige levantar un servidor MCP externo y configurar el host del runtime para conectarse. Infraestructura fuera del repo. | Bajo: el runtime ya invoca tools; la materialización es un adaptador que representa skills como declaraciones invocables + dispatcher. Implementable íntegramente dentro del repo como implementación de referencia en Python. | Medio-alto: exige un store persistente entre ejecuciones con semántica de recuperación; el runtime actual no expone uno controlable desde el repo. |
| Valor práctico para el runtime actual | Bajo hoy: no hay servidor MCP del protocolo ni consumidor que lo requiera. | Alto: convierte la carga diferida de skills —hoy lectura de `SKILL.md` por el Worker (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §`skills`)— en invocación bajo demanda por el runtime: materialización lazy real, análoga conceptualmente a `references/` pero invocable. Reduce el costo inicial del contexto (solo declaraciones, no contenido). | Medio: útil para conocimiento histórico (KB), pero la porción skills no se beneficia de persistencia entre ejecuciones. |
| Riesgo | Alto: dependencia externa; posible instalación de herramientas fuera del repo (bloqueo declarado por el protocolo de ejecución del plan). | Bajo: sin dependencias externas; verificable con el toolchain existente (Python + pytest del repo). | Medio: semántica de invalidación y frescura sin modelo; riesgo de deriva respecto del Execution Context. |
| Verificabilidad de la tesis | Indirecta: el servidor MCP sería código nuevo sin anclaje en la práctica actual. | Directa: la variante «Tool Calls» ya está modelada en RFC-00YL (`plans/rfc/14-prompt-rendering-model.md`, §Rendering Variants: «¿Qué parte del Execution Context se representa como capacidades invocables en lugar de texto leído?») y en RFC-00YM (`plans/rfc/15-skill-materialization-model.md`, §Conceptual Model: «futuros runtimes: herramientas invocables»). | Directa pero más costosa de evidenciar. |

# Decisión

**Se elige la opción 2: Tool calls**, con las skills como porción materializada del Execution Context (primer candidato declarado por el plan, §B, vía RFC-00YM).

Justificación: es la única opción que (a) no requiere infraestructura externa al repo, (b) tiene anclaje directo en la práctica actual del runtime (tool calls ya existen; la lectura diferida de `references/` ya es el patrón conceptual), y (c) produce diferencias observables medibles con la vara del Budget materializado (`.agents/standards/context/BUDGET_MATERIALIZATION.md`, §2: tokens estimados = `ceil(chars/4)`).

Las opciones 1 (MCP) y 3 (runtime memory) quedan como ejercicios futuros, coherentes con el «Fuera de alcance» del plan (`plans/18-segunda-materializacion.md`, §Fuera de alcance: tercera y cuarta materialización).

# Alcance de la implementación

- Porción del Execution Context materializada: **skills** (campo `skills: [...]` del Delegation Payload, `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §Required Invocation Payload).
- Materialización de referencia (existente): prompt tradicional — los nombres viajan en el payload y el Worker lee cada `SKILL.md` (RFC-00YM, §Compatibility).
- Segunda materialización (nueva): cada skill se representa como una **tool declaration** (nombre + descripción, extraídas del front matter del `SKILL.md`) y su contenido se obtiene por **invocación bajo demanda** del runtime.
- Criterios de conformidad, interacción con el Budget y ejercicio comparativo: ver `runtime/README.md` y `plans/18-anexo-b-reporte-verificacion-tesis.md`.
