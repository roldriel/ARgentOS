# Plan 16 — Policy Layer II: Resolution & Composition Policies

**Status:** Aprobado para redacción.

**Depends on:** planes 05 y 06 y plan 15 (marco de policies H15: formato, decision trees, clasificación de fallos). Este plan no cita contenido de 00YE–00YJ (aún inexistentes: `plans/rfc/` solo tiene 00–05); define las policies sobre las clases que 00YE deberá definir. Criterio de entrada verificable: los planes 05 y 06 están Executed y las clases citadas existen en las RFCs resultantes. Dependencia blanda del plan 10: si no está cerrado, la convención máquina/agente se define inline (ver §C).

**Referencia:** `plans/05-resolution-specialization.md`; `plans/06-composition-specialization.md`; `plans/rfc/05-context-resolution-model.md` (RFC-00YC, que difiere explícitamente las políticas concretas).

---

# Objetivo

Definir las **políticas concretas** que la serie de Execution Context difirió deliberadamente: cómo se desempata, cómo se deduplica, cómo se fusiona y cómo se comprime en la práctica. Es el paso de los modelos de contexto de "conceptualmente definidos" a "operativos".

---

# Contenido

## A. Policies de Resolution

Para el runtime actual, definiendo criterios concretos sobre las clases que RFC-00YE deberá definir (las referencias 00YF–00YJ que siguen son a RFCs planeadas, aún inexistentes):

1. **Tie-Breaking Policy** (sobre RFC-00YF): criterio concreto de desempate entre candidatos equivalentes (p. ej. precedencia de fuente: protocolo > proyecto > externo; recencia; explícita del usuario).
2. **Deduplication Policy** (sobre RFC-00YH): criterio de redundancia detectable (solape de contenido, misma fuente, misma sección) y acción resultante.
3. **Merge Policy** (sobre RFC-00YG): cuándo dos candidatos compatibles se fusionan y qué forma conceptual tiene el resultado.
4. **Conflictos irresolubles:** política de comportamiento ante conflictos que la implementación no puede resolver (responde al deferral de RFC-00YC, que lo asigna a "futuras RFCs de políticas"; este plan lo resuelve como policy, no como RFC): reportar como qué clase de fallo, con qué información.

## B. Policies de Composition

1. **Compression Policy** (sobre RFC-00YI): técnicas concretas permitidas (referencia en vez de inline, resumen, truncado) y su relación con la Compression Policy de facto ya existente en `.agents/standards/context/CONTEXT.md` — §8.2 (regla inline-vs-referencia con threshold del 10 %) y §8.4 (esquema Omit / Summarize / Reference / Split) — que esta policy debe INTEGRAR explícitamente para no duplicar.
2. **Optimization Policy** (sobre RFC-00YJ): criterio de adecuación de la representación al propósito de ejecución para el runtime prompt.
3. Orden de aplicación Compression → Optimization, coherente con el orden declarado en el plan 06 (00YI → 00YJ).

## C. Forma de entrega

- Cada política como documento de policy con su decisión, criterio y ejemplos. Ubicación fija: policies agente-evaluadas → `.agents/standards/context/`; si alguna resulta gateable, su versión harness va a `.agents/orchestrators/core/harness/policies/` con su registro en taxonomía (mismo proceso que H15 del plan 15).
- Las que sean verificables por máquina se declaran como Future Extensions del harness; las de juicio quedan como política agente-evaluada (convención del plan 10 si está cerrado; si no, marcado inline definido en este plan).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Policies de Resolution (4) | `.agents/standards/context/` (o `.agents/orchestrators/core/harness/policies/` para las gateables) |
| 2 | Policies de Composition (2) | ídem |
| 3 | Update a `CONTEXT.md` (integración inline/referencia) | `.agents/standards/context/CONTEXT.md` |
| 4 | Enmienda a RFC-00YC §Future Extensions registrando dónde quedaron las policies | `plans/rfc/05-context-resolution-model.md` |

# Fuera de alcance

- Modificar los modelos conceptuales 00YE–00YJ (si una policy revela un defecto del modelo, se reporta como enmienda, no se parcha).
- Compresión con pérdida semántica verificable por máquina (juicio del agente).
