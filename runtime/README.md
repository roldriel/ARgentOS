# `runtime/` — Implementaciones de referencia de materialización

**Origen:** planes 07 y 18 (RFC-00YK, RFC-00YM del roadmap Execution Context).

Este directorio contiene **implementaciones de referencia** de materializaciones del Execution Context. No es protocolo: es el lado del runtime de la frontera protocolo/runtime.

## Frontera respecto de `protocol/.agents/`

- `protocol/.agents/` define el protocolo: qué es un Execution Context, cómo se construye y cómo se entrega (Delegation Payload). Nada de lo que hay aquí modifica, extiende ni reinterpreta `protocol/.agents/`.
- `runtime/` define cómo un runtime concreto **representa** lo entregado: la transformación de un Execution Context en una representación propia del runtime (materialización). La entrega (payload) es el último acto del protocolo; la materialización es el primer acto del runtime.
- Dependencia en un solo sentido: `runtime/` lee `protocol/.agents/` (p. ej. los `SKILL.md` como fuente de capacidades); `protocol/.agents/` nunca referencia `runtime/`.
- Nada aquí es normativo. Un runtime real puede adoptar, adaptar o ignorar estas implementaciones; la corrección conceptual vive en el Execution Context, no en la representación.

## Convenciones

- Python 3.11+, stdlib únicamente (sin dependencias externas).
- Tests propios en `tests/test_toolcalls.py` (raíz del repo), ejecutables con `python -m pytest tests/test_toolcalls.py`. Son independientes de `protocol/.agents/harness/tests/` (que valida el protocolo, no el runtime).
- Las citas a documentos del repo usan el formato `ruta:sección`.

## Materializaciones implementadas

| Materialización | Módulo | Descripción |
| --- | --- | --- |
| Prompt (referencia, existente de facto) | `runtime/toolcalls/prompt_rendering.py` | El Execution Context se representa como texto de prompt: los nombres de las skills viajan en el payload y el Worker lee cada `SKILL.md` antes de ejecutar. |
| Tool calls (segunda materialización) | `runtime/toolcalls/toolcalls_rendering.py` | Cada skill se representa como una tool declaration invocable (nombre + descripción); el contenido de la skill se obtiene bajo demanda invocando la tool, no por adelantado. |

Ambas operan sobre el mismo `ExecutionContext` (`runtime/toolcalls/context.py`), construido a partir de los mismos campos que el Delegation Payload (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`). Coexisten: ninguna es «la correcta»; la elección pertenece al runtime.

## Criterios de conformidad de una materialización

Una representación producida aquí es conforme al modelo de materialización si:

1. **Representa sin alterar**: no incorpora, elimina ni sustituye contenido conceptual del Execution Context; solo decide su forma.
2. **Capacidad efectiva**: toda skill del Execution Context queda disponible para el Worker durante la ejecución (en la materialización prompt, leyendo el `SKILL.md`; en la de tool calls, invocando la tool). El contenido de la capacidad activada es el mismo en ambas.
3. **No retroalimenta el pipeline**: la materialización consume el Execution Context ya producido; ninguna decisión de representación modifica su construcción.
4. **Budget respetado**: el costo de la representación se estima con la regla declarada y no excede el `context_budget` del contexto.

## Interacción con el Budget materializado

El Budget del runtime prompt se materializa en tokens estimados con la regla `ceil(chars/4)` (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:2. Estimation rule`). Ese estándar prevé explícitamente otros runtimes (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:6. Other runtimes`): un runtime no-prompt declara su propia unidad y regla de estimación. Este runtime declara:

- **Unidad dual**: tokens estimados (misma regla `ceil(chars/4)`) para la porción textual del contexto, más **número de tool declarations** para la porción invocable.
- **Estimación**: el costo inicial de una skill materializada como tool es el costo textual de su declaración (nombre + descripción), no el del `SKILL.md` completo; el contenido se paga solo si se invoca (carga diferida real).
- **Lo que no cambia**: el Budget es finito, limita la construcción del Execution Context, y todo valor materializado es una cota finita y positiva en la unidad declarada (`runtime/toolcalls/budget.py`).

## Ejercicio comparativo

El plan 18 ejecutó un ejercicio comparativo entre ambas materializaciones (misma tarea, Execution Context construido desde skills reales de `protocol/.agents/skills/`, reporte de costo en tokens estimados, latencia y equivalencia de la capacidad activada). Resultados y veredicto de la tesis en `plans/18-anexo-b-reporte-verificacion-tesis.md`; el script del ejercicio se descartó una vez congelada la evidencia.
