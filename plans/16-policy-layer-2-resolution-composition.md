# Plan 16 — Policy Layer II: Resolution & Composition Policies

**Status:** Aprobado para redacción.

**Depends on:** planes 05 y 06 (RFCs 00YE–00YJ: Conflict Classification, Tie-Breaking, Merge, Deduplication, Compression, Optimization) y plan 15 (marco de policies H15: formato, decision trees, clasificación de fallos).

**Referencia:** `plans/05-resolution-specialization.md`; `plans/06-composition-specialization.md`; `plans/rfc/05-context-resolution-model.md` (RFC-00YC, que difiere explícitamente las políticas concretas).

---

# Objetivo

Definir las **políticas concretas** que la serie de Execution Context difirió deliberadamente: cómo se desempata, cómo se deduplica, cómo se fusiona y cómo se comprime en la práctica. Es el paso de los modelos de contexto de "conceptualmente definidos" a "operativos".

---

# Contenido

## A. Policies de Resolution

Para el runtime actual, definiendo criterios concretos sobre las clases de RFC-00YE:

1. **Tie-Breaking Policy** (sobre RFC-00YF): criterio concreto de desempate entre candidatos equivalentes (p. ej. precedencia de fuente: protocolo > proyecto > externo; recencia; explícita del usuario).
2. **Deduplication Policy** (sobre RFC-00YH): criterio de redundancia detectable (solape de contenido, misma fuente, misma sección) y acción resultante.
3. **Merge Policy** (sobre RFC-00YG): cuándo dos candidatos compatibles se fusionan y qué forma conceptual tiene el resultado.
4. **Conflictos irresolubles:** política de comportamiento ante conflictos que la implementación no puede resolver (diferido por RFC-00YC a "futuras RFCs de políticas" — esta es esa RFC): reportar como qué clase de fallo, con qué información.

## B. Policies de Composition

1. **Compression Policy** (sobre RFC-00YI): técnicas concretas permitidas (referencia en vez de inline, resumen, truncado) y su relación con la regla inline-vs-referencia ya existente en `standards/context/CONTEXT.md` — integrar, no duplicar.
2. **Optimization Policy** (sobre RFC-00YJ): criterio de adecuación de la representación al propósito de ejecución para el runtime prompt.
3. Orden de aplicación Compression → Optimization, coherente con lo declarado por los RFCs del plan 06.

## C. Forma de entrega

- Cada política como documento de policy con su decisión, criterio y ejemplos, ubicación a decidir (`standards/context/` o policies del harness si son gateables).
- Las que sean verificables por máquina se declaran como Future Extensions del harness; las de juicio quedan como política agente-evaluada (convención del plan 10).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Policies de Resolution (4) | `standards/context/` o `harness/policies/` |
| 2 | Policies de Composition (2) | ídem |
| 3 | Update a `CONTEXT.md` (integración inline/referencia) | `.agents/standards/context/CONTEXT.md` |

# Fuera de alcance

- Modificar los modelos conceptuales 00YE–00YJ (si una policy revela un defecto del modelo, se reporta como enmienda, no se parcha).
- Compresión con pérdida semántica verificable por máquina (juicio del agente).
