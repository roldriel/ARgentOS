# ADR-19 — Autonomy Envelope: Authority Decisions (Plan 151)

**Status:** Accepted
**Fecha:** 2026-10-07
**Decisión original:** — (no deriva del modelo arquitectónico D#)
**RFC:** — (docs-only; no toca `protocol/.agents/`, RFC-56 no aplica)
**Plan:** plan 151 (`docs/plans/151-autonomy-authority-decision-closure.md`)
**Clase de cambio:** — (sin efecto payload)
**Problemas que resuelve:** — (frontera de autoridad del envelope de autonomía DEV)

## Contexto

El modelo de autoridad de ARgentOS DEV fija `autonomy ⊆ authorized scope ∩ granted authority` (política
operacional **Supervised Autonomous Execution**, formalizada por
`docs/plans/135-supervised-autonomous-execution.md:Objetivo`) y declara la
orquestación y el handoff **fuera del alcance** de RFC-75
(`docs/rfc/75-change-lifecycle.md:Rollout incremental`). Sobre esa base quedaban **abiertas**, sin
decisión de autoridad trazable, varias cuestiones del *envelope* que un ejecutor autónomo necesita
resueltas antes de implementarse: cuál es la unidad de aceptación; dónde y cómo se admiten los
efectos fuera de la frontera inmediata; si existe un eje de recurso autorizado; qué clase de actor
está autorizada; qué papel tiene el conocimiento y Memory; y si existen formas parciales de
autorización o de derivación.

El corpus contenía respuestas **materializadas pero no autorizadas**: el commit `b556741`
(2026-10-06) introdujo texto que afirmaba un acto humano del 2026-10-05 cuya existencia **no está
verificada** (`HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`), y el commit `d8bd284` (2026-10-06)
introdujo dos reglas normativas sin plan citado. Ninguna de esas materializaciones constituye
autoridad (`docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera`).

## Alternativas consideradas

### A — Dejar las cuestiones del envelope en materializaciones sin acto

Rechazada: la autoridad no se infiere de la presencia documental. Una materialización no es un acto
de autoridad y no puede sostener la implementación de un ejecutor.

### B — Resolver el envelope ampliando el alcance (payload, provider, presupuesto, Memory)

Rechazada: introduciría mecanismos no autorizados y tocaría `protocol/.agents/` sin necesidad
demostrada, cuando el ejecutor DEV decide su propia frontera.

### C — Registrar en un único acto de autoridad los invariantes del envelope (elegida)

Un acto humano explícito (Plan 151, mantenedor, 2026-10-07) resuelve las decisiones del envelope y
las registra como invariantes, sin crear mecanismo, entidad, state machine ni autoridad nueva.

## Decisión

**Opción C.** Se adoptan los siguientes invariantes del envelope de autonomía DEV. Registran
**principios**, no esquemas de implementación:

1. La unidad primaria de aceptación es el **Change**; el objetivo global multi-Change queda fuera del
   cierre actual y requiere un mecanismo/trigger posterior explícito.
2. La admisión de efectos fuera de la frontera inmediata se decide y se declara en **DEV**; no se
   hereda la política de efectos del Protocol.
3. **`Effect` es ortogonal a `Scope`**: Scope responde por objetos/paths; Effect, por clases de acción
   que pueden no tener path. Ninguno sustituye al otro.
4. La declaración de efectos vive **donde vive la autorización** —el Plan—, como superficie paralela
   a la delegación; no crea una clase de autoridad ni un mecanismo nuevo.
5. La derivación de autoridad ocurre **antes de la delegación**.
6. **No se incorpora un eje de recurso** (`resource budget`) como dimensión de autorización.
7. La clase de actor autorizada es la **acotada por la autoridad existente**; la selección de
   provider/modelo queda **diferida**.
8. El conocimiento es **documental** (`P-6`); **Memory es contexto**.
9. **No existe autorización parcial** separada.
10. **No existe continuación válida** sobre una derivación incompleta.

## Consecuencias

- El `AUTONOMY_MODEL` (redacción futura) hereda estos invariantes y **no** puede declarar éxito sobre
  una unidad distinta del Change, ni admitir efectos por proximidad, ni tratar un límite operativo
  como autorización, ni apoyarse en una autorización o derivación parcial.
- Los esquemas de implementación (gate de efectos, enum de clases de efecto, presupuesto de recurso,
  actor con provider/modelo, aislamiento, integración de Memory) quedan **fuera** de este acto y
  requieren su propia autorización.
- Este ADR **no** habilita cambios de payload ni ejecución: `docs/adr/16-change-lifecycle-authority.md:Decisión`
  mantiene que el ADR registra la decisión y la autorización de ejecución sigue siendo el Plan.

## Invariantes

- AE-1: la unidad primaria de aceptación es el Change; el objetivo global no se infiere.
- AE-2: la admisión de efectos fuera de frontera se decide y se declara en DEV, sin herencia del Protocol.
- AE-3: `Effect` es ortogonal a `Scope`; un efecto puede existir sin write-target.
- AE-4: la declaración de efectos vive en el Plan y no crea una clase de autoridad.
- AE-5: la derivación de autoridad precede a la delegación.
- AE-6: ningún límite operativo (iteraciones, timeout, pasos del worker, no-progress) es autorización.
- AE-7: el actor autorizado está acotado por la autoridad existente; provider/modelo/red/credenciales/sandbox no se materializan, y el invoker inyectado no es garantía de aislamiento.
- AE-8: `P-6` es conocimiento documental; Memory no es autoridad ni premisa de derivación.
- AE-9: `Plan + Scope + execution state` no crean una segunda autoridad.
- AE-10: una derivación incompleta no autoriza continuar; produce `GAP`/pendiente/diferido y detiene el paso dependiente.

## Relaciones

- Depende de: `docs/adr/16-change-lifecycle-authority.md` (clases de autoridad y ADR-worthiness `AU-6`);
  la política operacional **Supervised Autonomous Execution** (frontera SAE), formalizada por
  `docs/plans/135-supervised-autonomous-execution.md:Objetivo`.
- Formalizada en: plan 151 (`docs/plans/151-autonomy-authority-decision-closure.md`), cuyas decisiones
  `D-1`, `D-2a`, `D-2b`, `D-2c`, `D-2d`, `D-3`, `D-4`, `D-5`, `D-6a` y `D-6b` este ADR registra.
- Materializa en reglas: `docs/CONVENTIONS.md:Modelo de autonomía — decisiones de autoridad del Plan 151`.

## Estado de implementación

Decisión adoptada por el acto de autoridad del Plan 151 (mantenedor, 2026-10-07); docs-only, sin
`VERSION` bump ni tag (`docs/rfc/69-documentation-taxonomy-and-layout.md`). Los invariantes quedan
vigentes como norma; **su implementación** (gate de efectos, enum de clases de efecto, presupuesto de
recurso, actor con provider/modelo, aislamiento, integración de Memory, superficie de derivación) es
trabajo futuro con su propia autorización. Este ADR **no** habilita cambios de payload: la vía sigue
siendo RFC `Accepted` + plan (`docs/CONVENTIONS.md:Convenciones`).
