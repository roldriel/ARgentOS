# Plan 18 — Anexo B: Reporte de verificación de la tesis

**Status:** Executed (anexo del plan `plans/18-segunda-materializacion.md`, §C. Verificación de la tesis).

**Fecha:** 2026-08-05.

**Tesis bajo prueba** (`plans/18-segunda-materializacion.md`, §Objetivo): el modelo conceptual del Execution Context (RFC-00XX a RFC-00YM) no se modifica en lo más mínimo al implementar una materialización distinta de la inyección de prompt.

**Umbral de falla** (declarado por el plan, §C): falla de la tesis = cambio en la responsabilidad de una etapa del pipeline; las enmiendas aclaratorias se documentan como hallazgo menor.

---

# 1. Segunda materialización implementada

Mecanismo elegido: **tool calls** (decisión y comparativa en `plans/18-anexo-a-comparativa-y-decision.md`, §Decisión). Porción materializada: skills (primer candidato declarado por el plan, §B).

Implementación de referencia: `runtime/toolcalls/toolcalls_rendering.py` — cada skill se representa como una tool declaration (nombre + descripción del front matter del `SKILL.md`) y su contenido se obtiene por invocación bajo demanda (`invoke_tool`). Coexiste con la materialización prompt (`runtime/toolcalls/prompt_rendering.py`) sobre el mismo `ExecutionContext` (`runtime/toolcalls/context.py`), conforme a la Coexistence Rule (`plans/rfc/13-execution-context-materialization-model.md`, §Coexistence Rule). Convenciones, frontera protocolo/runtime, criterios de conformidad e interacción con el Budget: `runtime/README.md`.

# 2. Cero modificaciones al modelo conceptual

Verificación contra el criterio del plan (§C: «Cero modificaciones a `plans/rfc/00–05` ni a los conceptos de `.agents/`»):

- **RFCs 00–05 y 06–12** (pipeline conceptual): sin cambios. `git status` confirma que los únicos RFCs tocados por este plan son 13 y 15, y solo en sus secciones Compatibility y Amendment Log (entregable 4 del plan).
- **`.agents/`**: sin cambios atribuibles a este plan. Ningún concepto, contrato, estándar, policy ni rol del protocolo fue tocado: la segunda materialización vive íntegramente en `runtime/`, del lado del runtime de la frontera (RFC-00YK, §Protocol/Runtime Boundary: Delivery es el último acto del protocolo, Materialization el primero del runtime).
- **Responsabilidades de las etapas del pipeline**: intactas. La materialización consume el Execution Context ya producido y no retroalimenta su construcción (criterio de conformidad 3, `runtime/README.md`, §Criterios de conformidad).

**Hallazgos menores (enmiendas aclaratorias): ninguno.** La implementación no reveló definiciones ambiguas que exigieran precisar el modelo: la variante «Tool Calls» ya estaba contemplada como pregunta de representación en RFC-00YL (`plans/rfc/14-prompt-rendering-model.md`, §Rendering Variants) y como dirección de runtime futuro en RFC-00YM (`plans/rfc/15-skill-materialization-model.md`, §Conceptual Model), por lo que la segunda materialización no agregó conceptos: instanció los existentes.

# 3. Criterios de conformidad verificados

Los cuatro criterios declarados en `runtime/README.md` (§Criterios de conformidad) quedan verificados por tests ejecutables (`runtime/tests/test_toolcalls.py`, sección «Conformance criteria»):

| Criterio | Test | Resultado |
| --- | --- | --- |
| Representa sin alterar (declaraciones desde el front matter propio de la skill; contenido verbatim) | `test_declarations_come_from_front_matter`, `test_invoke_tool_loads_content_on_demand` | PASS |
| Capacidad efectiva idéntica en ambas materializaciones | `test_effective_capability_is_identical_across_materializations` | PASS |
| No retroalimenta el pipeline (misma entrada, dos representaciones; el contexto no cambia) | `test_both_materializations_coexist_on_same_context` | PASS |
| Budget respetado (unidad dual declarada; carga diferida real) | `test_estimate_tokens_ceil_rule`, `test_toolcalls_defers_real_cost` | PASS |

Suite completa: `python -m pytest runtime/tests/` → **12 passed**. La suite del protocolo sigue intacta: `python -m pytest .agents/harness/tests/` → **323 passed, 2 skipped**; `python .agents/harness/runner.py health-check` → **PASS**.

# 4. Ejercicio comparativo

Misma tarea (delegación de fase 05-plan con skills `planner`, `risk-detector`, `tradeoff-analyzer`, resueltas desde `.agents/skills/` reales) ejecutada con ambas materializaciones por `runtime/examples/compare.py`. Resultados de la corrida del 2026-08-05:

| Métrica | Prompt (referencia) | Tool calls (segunda) |
| --- | --- | --- |
| Tokens estimados iniciales | 95 | 310 |
| Tokens estimados diferidos (contenido de skills) | 2697 | 2697 |
| Total si se carga todo | 2792 | 3007 |
| Tool declarations | 0 | 3 |
| Latencia de producir la representación (ms) | 15.857 | 1.223 |
| Contenido de la capacidad activada (`planner`) | idéntico | idéntico |

Lectura de las diferencias observables:

- **Costo**: la materialización prompt paga los 2697 tokens del contenido completo de las tres skills antes de ejecutar (el contrato exige leer cada `SKILL.md`), total efectivo pre-ejecución 2792. La de tool calls paga 310 iniciales y solo paga el contenido de cada skill **si se invoca**: con una sola capacidad activada, el ahorro efectivo es del orden de la mitad del costo; con ninguna, el 89%. El costo diferido total es idéntico: la capacidad no cambia, cambia cuándo se paga.
- **Latencia**: ambas son despreciables en absoluto (milisegundos; la diferencia observada es ruido de I/O local, no una propiedad del mecanismo). Se reporta por completitud, sin pretensión de significancia.
- **Calidad**: cualitativa, como declara el plan (§C: no existe rúbrica aplicable en `.agents/standards/quality/RUBRICS.md`). Lo verificable es la equivalencia de la capacidad: el contenido que el Worker recibe al activar una skill es byte-idéntico en ambas materializaciones (test de conformidad 2). La diferencia restante es de forma de acceso (lectura anticipada vs. invocación bajo demanda), no de capacidad — exactamente lo que el Rendering Invariant predice.

# 5. Veredicto

**La tesis se verifica.** Una segunda materialización funcional, distinta del prompt, coexiste con la primera sobre el mismo Execution Context sin que el modelo conceptual (RFCs 00–15) ni `.agents/` requieran modificación alguna. El único toque a los RFCs de materialización es el declarado por el propio plan como entregable: la declaración de conformidad en sus secciones Compatibility (enmiendas del 2026-08-05 en RFC-00YK y RFC-00YM, registradas en sus Amendment Logs).

Las materializaciones MCP y runtime memory quedan como ejercicios futuros (`plans/18-segunda-materializacion.md`, §Fuera de alcance).
