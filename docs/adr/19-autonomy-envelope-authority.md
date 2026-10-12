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

### Amendment Log

- **2026-10-11 — acto de autoridad del Plan 159 (materialización de `F-B`).** El mantenedor cerró las
  dos cuestiones que el acto del 2026-10-07 dejó fuera, mediante directiva de ejecución
  (`docs/plans/159-autonomy-envelope-implementation.md`). El acto anterior **no se modifica**: este
  Amendment Log **agrega** y preserva su texto íntegro.
  - **`OPD-1` — vocabulario de clases de efecto: ADOPTADO.** El vocabulario DEV de clases de efecto
    pasa a ser el que el repositorio ya había materializado y verificado para sus artefactos de sesión
    del Protocol (`tools/check_session_artifacts.py`): `network`, `remote_git`, `install`,
    `destructive`, `write_outside_project`, con `AUTHORIZED_BY` ∈ {`user`, `unattended_default`} y
    `EFFECT_STATUS` ∈ {`authorized`, `not_authorized`, `pending_user_confirmation`}. Es una
    **adopción**, no una taxonomía nueva: hay un solo vocabulario, y el runtime y el checker lo
    comparten (verificado por dogfood anclado). Una clase no reconocida **no** se interpreta como
    autorizada: produce `STOP` con autoridad humana (`REQUIRES_HUMAN`).
  - **`OPD-2` — techo de recurso: guarda operativa de terminación.** El Plan declara un techo de
    ejecuciones delegadas en la misma superficie que declara `Task` y `Scope`; el runtime lo lee,
    acumula el consumo desde las delegaciones efectivamente registradas en el journal (nunca desde la
    numeración de iteraciones) y detiene la autonomía al agotarse, con `STOP_MAX_ITERATIONS`.
    `resource ceiling ≠ authorization`: el techo **no** entra en `AutonomyEnvelope.declared`, **no**
    produce veredicto `AUTHORIZED_EXISTING` y **no** amplía autoridad. Esto preserva `AE-6` y `D-3`
    sin excepción: `PR-2` del audit de capacidades
    (`docs/working/audits/architecture-capability-review.md`) queda resuelto como **frontera de
    terminación**, no como eje de autorización.
  - **Invariantes materializados por este acto:** `AE-2`, `AE-3`, `AE-4` (admisión de efectos antes de
    delegar, ortogonalidad `Effect` ⊥ `Scope`, consumidor de la declaración del Plan) y `AE-6` (el
    techo de recurso como límite operativo, nunca autorización). La frontera `BLK-1` y `BLK-2` del
    relevamiento de cierre quedan cerradas.
  - **Lo que este acto sigue dejando fuera:** actor con provider/modelo, aislamiento/sandbox,
    integración de Memory, superficie de derivación parcial y objetivos multi-Change (`F-C`/Etapa B).
    Nada de eso habilita este Amendment Log.
- **2026-10-12 — reconciliación `OD-2`: la entrada del 2026-10-11 no abre trabajo diferido.** El
  relevamiento de cierre de `F-C` detectó que la entrada anterior enumera la «superficie de derivación
  parcial» entre lo que el acto del 2026-10-11 dejaba fuera, mientras que `D-6b = NO` (acto del
  2026-10-07) **descarta** esa capacidad: no se crea superficie ni mecanismo, y el pending del Plan 151
  la registra `NOT_APPLICABLE`. La decisión efectiva es `D-6b = NO`. La enumeración se corrige **hacia
  adelante** —el texto de la entrada anterior se preserva íntegro (RFC-46)— y su efecto operativo queda
  en `docs/CONVENTIONS.md` (subsección «Modelo de autonomía — vocabulario de efectos y techo de recurso
  (adoptado 2026-10-11)»). Esta reconciliación **no** crea capacidad, superficie ni autorización, **no**
  constituye trabajo futuro y **no** modifica los invariantes de este ADR. Change que la registra:
  `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md:Objetivo`.
- **2026-10-08 — cierre residual del Plan 151** (`docs/plans/153-plan-151-residual-closure.md`):
  disposición de las diez filas `HD-*` por evidencia y decisión posterior, sin retroactividad. No
  modifica los invariantes de este ADR.

### Estado de implementación tras el acto del 2026-10-11

| Invariante | Estado | Evidencia |
|---|---|---|
| `AE-1` unidad = el Change | vigente | el host conduce un Change por corrida (`runtime/orchestrator/host.py`) |
| `AE-2` admisión de efectos en DEV | **implementado** | `admit_declared_effects` (`runtime/orchestrator/autonomy.py`), parseo de `## Efectos declarados` (`runtime/orchestrator/observation.py`), gate previo a la delegación (`ExecutionHost._apply_autonomy_gate`) |
| `AE-3` `Effect` ⊥ `Scope` | **implementado** | la admisión no consulta paths; un efecto autorizado sin `write-target` es admisible (`tests/test_autonomy_effects.py`) |
| `AE-4` declaración en el Plan | **implementado** | `## Efectos declarados` es leído por el runtime y por `docs/plans/_TEMPLATE.md` (`tests/test_autonomy_effects_dogfood.py`) |
| `AE-5` derivación antes de delegar | implementado (plan 138) | `_apply_autonomy_gate` en `iterate()` |
| `AE-6` límite operativo ≠ autorización | **implementado** | techo de recurso sin veredicto de autoridad (`tests/test_autonomy_effects.py`, prueba `test_resource_exhaustion_is_never_an_authorization`) |
| `AE-7` actor acotado; provider/modelo diferidos | vigente, sin materializar | `runtime/orchestrator/agent_worker.py` no usa provider ni red |
| `AE-8` Memory es contexto | vigente | `runtime/memory/` no se consume desde el orquestador |
| `AE-9` sin segunda autoridad | implementado | `runtime/orchestrator/authority.py` |
| `AE-10` sin continuación sobre derivación incompleta | implementado | `evaluate_autonomy` / `evaluate_candidate` |

