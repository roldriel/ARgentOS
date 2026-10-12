# Plan 162 — Instrumento de decisión de `OD-1`: alcance canónico de `F-C`

**Status:** Executed
**Fecha:** 2026-10-12
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only, docs-only, sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=0, release impact=0, duration/complexity=0)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, una capa (documentación de gobernanza DEV). *scope*: área acotada — tres rutas de contenido de gobernanza más este artefacto. *architectural impact*: **0** — no crea capacidad, entidad, estado, autoridad, contrato ni mecanismo; **no decide nada**: prepara la forma decision-ready de una decisión que pertenece al mantenedor. *release impact*: ninguno. *duration/complexity*: menos de una sesión.
**Depende de:** plan 161 (resultado de Etapa A: `Capability & Guarantee Matrix`), plan 160 (contrato y autorización de Etapa A), plan 159 (`F-B`), `docs/adr/19-autonomy-envelope-authority.md` (envelope)
**Origen:** directiva del mantenedor (2026-10-12) de resolver `OD-1`. La verificación de autoridad de este Change concluye que **la decisión no está presente en el repositorio**: este Plan materializa el instrumento mínimo para que pueda ejercerse y registra el estado `OD1_BLOCKED`.
**Work type:** `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change; no se deriva ni se inventa.

## Objetivo

Determinar con trazabilidad documental qué significa hoy `F-C`, qué relación tiene con Etapa B y qué parte de la autonomía quedó cubierta por `F-A` y `F-B`; y, como la resolución de `OD-1` es una **decisión de alcance** que la gobernanza vigente reserva al mantenedor y que **no está presente en el repositorio**, dejar preparado el material mínimo para que esa decisión pueda tomarse —sin tomarla— y registrar el estado `OD1_BLOCKED`.

Este Plan **no** define `F-C`, **no** elige entre las interpretaciones conocidas, **no** autoriza ni inicia Etapa B y **no** implementa ninguna capacidad.

## Verificación de autoridad (paso determinante)

### Regla aplicable

| Fuente | Regla | Consecuencia |
|---|---|---|
| `.agents/policies/authority.md` (`## Authority classes`) | `DECISION` = «final authority to resolve conflicts» → **the human maintainer**; delegación a la inferencia del agente **no** admitida | una interpretación del agente no es una decisión |
| `.agents/policies/authority.md` (`## Stop conditions (authority)`) | «A human decision is required (approval, conflict resolution, resolution of a finding, ADR-worthiness, materiality) → **STOP** at the gate, ask»; «Normative authority for the change does not exist → **STOP**, propose/escalate» | `OD-1` cae en la reserva: **STOP** y preparar |
| `.agents/AGENTS.md` (regla fundamental 3) | «**Never convert your inference into a human decision.** You detect, classify, register and escalate; the maintainer decides» | prohibido canonizar la lectura dominante |
| `.agents/policies/supervised-autonomous-execution.md` §8 (`Human boundary`) | el humano es la autoridad exclusiva para «authorizing scope, and authorizing scope changes» | delimitar `F-C` **es** autorizar alcance |
| `docs/adr/16-change-lifecycle-authority.md:Invariantes` (`AU-3`, `AU-5`, `AU-6`) | conflictos y decisiones normativas se escalan; un Plan no modifica silenciosamente la decisión normativa; la elevación a ADR es juicio humano | sin acto humano no hay cambio de alcance |

### Estado verificado de la autorización

| Comprobación | Resultado | Evidencia |
|---|---|---|
| ¿Existe una decisión del mantenedor que fije el alcance de `F-C`? | **NO** | ninguna fuente viva lo hace: todas las menciones son **exclusiones de alcance** (`no se implementa F-C/Etapa B`) o remisiones a una decisión futura |
| ¿`OD-1` está registrado como pendiente con owner? | **SÍ** — decisión **bloqueante**, owner **mantenedor** | `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md:Pending decisions`; fila de blocker en `ROADMAP.md` |
| ¿El ROADMAP declara que requiere autorización propia? | **SÍ** | `ROADMAP.md` (`NEXT`: «requiere su propio Change autorizado») y la fila `OD-1` de la tabla de bloqueos |
| ¿Algún ADR decide el alcance de `F-C`? | **NO** — ADR-19 decide el **envelope** (`AE-1`…`AE-10`), no el alcance de `F-C` | `docs/adr/19-autonomy-envelope-authority.md:Decisión` |
| ¿La consigna de intake aporta la decisión? | **NO** — ordena resolver `OD-1` y prohíbe expresamente elegir R1/R2 arbitrariamente; en la rama bloqueada ordena **preparar** | consigna de intake de esta sesión (registrada en `P-1`) |
| ¿Etapa A la aporta? | **NO** por sí misma — su matriz es **evidencia**, y su propio texto lo declara | `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` §4 (encabezado de la sección de resultado) |

```text
OD1_BLOCKED = TRUE
MOTIVO      = la resolución de OD-1 es una decisión de ALCANCE reservada al mantenedor
              y NO está presente en el repositorio; el agente no puede convertir
              su lectura dominante en una definición canónica.
```

## Evidencia disponible para la decisión

### Lo que la evidencia **sí** determina

| # | Determinación | Evidencia |
|---|---|---|
| D-1 | `F-C` designa trabajo **no iniciado** y **fuera de alcance** de todo lo ejecutado hasta ahora | `docs/plans/159-autonomy-envelope-implementation.md:Objetivo` y su `### Nota de ejecución`; `docs/plans/INDEX.md` (fila del Plan 159); `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` §4.4 |
| D-2 | `F-A` cubrió la **capacidad de autonomía DEV** (host, bucle, SAE, modelo de autoridad) y `F-B` el **envelope** (admisión de efectos, `Effect ⊥ Scope`, techo de recurso como terminación) | `docs/plans/159-autonomy-envelope-implementation.md` (`Closed`); `docs/adr/19-autonomy-envelope-authority.md:Estado de implementación tras el acto del 2026-10-11` |
| D-3 | Quedan **fuera** de `F-A`/`F-B`: actor con provider/modelo, aislamiento/sandbox, integración de Memory, objetivos multi-Change | `docs/adr/19-autonomy-envelope-authority.md:Amendment Log` (entrada del 2026-10-11, «Lo que este acto sigue dejando fuera») |
| D-4 | La **superficie de derivación parcial** está **descartada** (`D-6b = NO`) y **no** pertenece a `F-C` | `docs/CONVENTIONS.md` (viñeta «Fuera de este acto», subsección adoptada el 2026-10-11) y `docs/adr/19-autonomy-envelope-authority.md:Amendment Log` (reconciliación del 2026-10-12) |
| D-5 | Un **eje de recurso como autorización** está prohibido de forma permanente y **no** pertenece a `F-C` | `docs/adr/19-autonomy-envelope-authority.md:Invariantes` (`AE-6`); `docs/CONVENTIONS.md` (decisión `D-3`) |
| D-6 | `F-C` es **posterior** a Etapa A, y el resultado de Etapa A puede **reducir** el alcance de Etapa B | `ROADMAP.md` (`NEXT` y dependencias); `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md:Checkpoint / cierre` |
| D-7 | Etapa A dejó disponible la matriz 28 × 9 como insumo, con estas capacidades condicionando una autonomía más amplia y sin demostrar: `C-08` (actor real), `C-02` (contención de autoridad fuera del host), `C-26` (recuperación con fallos reales) | `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` §4.2/§4.3/§4.4 |

### Las interpretaciones conocidas y su soporte

| Interpretación | Formulación | Soporte documental | Tensión que deja abierta |
|---|---|---|---|
| **R1** | `F-C` = la **totalidad** de Etapa B / «Complete ARgentOS Autonomy» | `docs/plans/159-autonomy-envelope-implementation.md:Checkpoint / cierre` («La línea `LATER` "Complete ARgentOS Autonomy (Etapa B)" no se re-prioriza: `F-C` sigue siendo trabajo futuro con su propia autorización»); `CHANGELOG.md` (ítem del Plan 159); `docs/plans/INDEX.md` (fila del Plan 159); `ROADMAP.md` (`LATER`, «Complete ARgentOS Autonomy (Etapa B)») | Etapa A mostró que buena parte de las capacidades con menor madurez (`C-16`, `C-17`, `C-21`) son del **payload del Protocol** y su garantía depende de una adopción real, no de trabajo de autonomía del DEV; bajo R1, Etapa B las heredaría |
| **R2** | `F-C` = sólo el **residuo del envelope** posterior a `F-A` + `F-B` (actor con provider/modelo, aislamiento/sandbox, Memory, objetivos multi-Change) | `docs/adr/19-autonomy-envelope-authority.md:Amendment Log` (los cuatro ítems enumerados bajo el rótulo `F-C`/Etapa B); `Estado de implementación` de ADR-19: `AE-7` y `AE-8` son los únicos invariantes «vigentes, sin materializar»; `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` (residuo ya reducido por la decisión `OD-2`) | deja **sin nombre** el resto de la línea de autonomía amplia que el ROADMAP sí representa (Etapa B) y no explica qué ocurre con las fronteras candidatas de la Etapa B que no son envelope |
| **R3** (opción derivable, **no adoptada**) | `F-C` = **subconjunto** de Etapa B delimitado por el resultado de Etapa A: la frontera de autonomía (actor real, contención de autoridad, recuperación, Memory, objetivo multi-Change), excluyendo explícitamente las brechas del payload (`C-16`, `C-17`, `C-21`) | `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` §4.2/§4.4 (las capacidades que condicionan autonomía son `C-08`/`C-02`/`C-26`; las de menor madurez son del payload); `ROADMAP.md` («su resultado puede **reducir** el alcance de la Etapa B») | **ninguna fuente lo declara**; es una lectura posible del mandato de reducción, no una decisión registrada |

### Lo que la evidencia **no** determina

La evidencia **acota** pero **no resuelve**: no existe fuente que diga si el rótulo `F-C` nombra la totalidad de Etapa B (R1), sólo su residuo de envelope (R2) o un subconjunto reducido por Etapa A (R3), ni qué ocurre con las fronteras de la Etapa B que no son de autonomía. Ese vacío **no es un defecto documental**: es el objeto de la decisión pendiente. Canonizar una de las tres lecturas sería convertir una inferencia del agente en una definición normativa de alcance.

## Pregunta de decisión (a ejercer por el mantenedor)

```text
OD-1 — ¿Cuál es el alcance canónico de F-C?
```

| # | Pregunta | Opciones | Qué queda determinado si se elige |
|---|---|---|---|
| `Q-a` | ¿`F-C` nombra la totalidad de Etapa B o un subconjunto? | **R1** (Etapa B completa) · **R2** (sólo el residuo del envelope) · **R3** (subconjunto de frontera de autonomía) | el universo de capacidades que `F-C` deberá cerrar y el nombre que conserva el resto |
| `Q-b` | Si `F-C` ⊂ Etapa B, ¿qué representa el resto de Etapa B? | mantener Etapa B como iniciativa separada · disolver Etapa B en `F-C` + trabajo de payload · otra | la forma del mapa operativo (`ROADMAP.md`) |
| `Q-c` | ¿Qué capacidades de la matriz de Etapa A son **condiciones** de `F-C`? | `C-08`, `C-02`, `C-26` (frontera de autonomía) · incluir también `C-16`/`C-17`/`C-21` (payload) · otro conjunto | las precondiciones de la futura implementación |
| `Q-d` | ¿El acto requiere ADR? (`AU-6`) | sí · no (con justificación registrada) | dónde vive la decisión (ADR + registro, o sólo registro normativo) |

**Consecuencia de no decidir:** `F-C` permanece `NOT_IMPLEMENTED`, Etapa B `NOT_STARTED` y ninguna capacidad se implementa; el repositorio queda en el estado actual, que es coherente y no bloquea nada más que el tramo posterior.

## Qué NO debe inferirse (protección contra scope creep)

1. Que `F-C` incluya **implementar** algo por el hecho de estar nombrado en esta evidencia.
2. Que `C-16`, `C-17` o `C-21` pertenezcan a `F-C` por su madurez baja: pertenecen al **payload del Protocol** y su garantía depende de una adopción real; su inclusión exige justificación de alcance, no simpatía por el hallazgo.
3. Que `C-02`/`C-08`/`C-26` sean requisitos de implementación: son **condiciones de garantía** identificadas por Etapa A.
4. Que la Etapa B esté autorizada, iniciada o tenga alcance cerrado.
5. Que el resultado de Etapa A autorice por sí mismo una reducción: **informa** la reducción; la decide el mantenedor.
6. Que `--sae` cambie de default, que el techo de recurso se vuelva autorización o que el envelope de `F-B` se modifique: todas están decididas en contra y `OD-2`/`OD-4` están cerradas.
7. Que este instrumento sea la decisión: es el **soporte** de la decisión.

## Registro del acto (dónde debe quedar)

| Aspecto | Determinación |
|---|---|
| **Artefacto que debe autorizarse** | el **acto del mantenedor** sobre `Q-a`…`Q-d`. Su vehículo natural es este mismo Plan —o un Plan sucesor— en una sección `## Acto de autoridad registrado (fecha)` con los resultados nominados, siguiendo el precedente de `docs/plans/151-autonomy-authority-decision-closure.md` y `docs/plans/152-authority-decisions-gov-1-10.md` |
| **Registro normativo** | subsección **aditiva** en `docs/CONVENTIONS.md` (familia «Modelo de autonomía»), preservando el texto de las subsecciones adoptadas el 2026-10-07 y el 2026-10-11 (precedente del Plan 159) |
| **ADR** | se decide en `Q-d` (`AU-6`); si se eleva, el destino es `docs/adr/` con registro en `docs/adr/INDEX.md` en el mismo commit |
| **Propiedad del pending** | permanece en **`<PLAN-161>`** (`### Pending decisions`): `OD-1` es su decisión bloqueante, owner mantenedor. Este Plan **no** la duplica ni la resuelve |
| **Reconciliación derivada** | `ROADMAP.md` (card de Etapa B y fila de blocker `OD-1`), `docs/plans/INDEX.md` y `CHANGELOG.md` del Change que ejerza el acto |
| **Criterios de cierre del acto** (`AC-1`…`AC-12`) | interpretación elegida · definición precisa de `F-C` · relación `F-C` ↔ Etapa B · boundary con `F-A` · boundary con `F-B` · capacidades/hallazgos dentro · exclusiones explícitas · qué no debe inferirse · dependencias y precondiciones · registro normativo hecho · ADR-worthiness resuelta · 0 implementación |

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Directiva del mantenedor (2026-10-12): resolver `OD-1` (alcance canónico de `F-C`) tomando como evidencia primaria el resultado cerrado de Etapa A; no asumir R1/R2; si falta autoridad, no inventar la decisión y dejar `OD1_BLOCKED` con el material preparado. `origin_type` = direct maintainer action | humano | consigna de intake de esta sesión |
| `P-2` Confianza de intención | `HIGH` — la consigna fija el objeto (`OD-1`), las interpretaciones conocidas, la evidencia primaria, la prohibición de elegir arbitrariamente, la rama bloqueada con sus entregables y el formato del informe | agente | `INTENT_CONFIDENCE` aplicado sobre la consigna |
| `P-3` Conjunto de contexto | `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`; `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md`; `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md`; `docs/plans/159-autonomy-envelope-implementation.md`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/adr/16-change-lifecycle-authority.md`; `docs/CONVENTIONS.md` (modelo de autonomía); `ROADMAP.md`; `docs/plans/INDEX.md`; `CHANGELOG.md`; `.agents/policies/authority.md`; `.agents/policies/supervised-autonomous-execution.md`; `.agents/AGENTS.md`; `docs/VERSIONING.md` §7 | agente | las citas de cada fila |
| `P-4` Derivabilidad | **`REQUIRES_HUMAN`** — la resolución de `OD-1` es una decisión de **alcance** (reserva humana: `.agents/policies/supervised-autonomous-execution.md` §8; `.agents/policies/authority.md` `## Stop conditions (authority)`), registrada como bloqueante con owner mantenedor y sin acto presente en el repositorio. La rama autorizada y ejecutada es la **preparación**: este instrumento. Sin `ANOMALY`: no hay contradicción entre fuentes, hay **vacío de decisión** | agente | `.agents/policies/authority.md`; `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md:Pending decisions` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change y **no se inventa** | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`); `docs/plans/152-authority-decisions-gov-1-10.md:Acto de autoridad registrado (2026-10-07)` |
| `P-6` Conocimiento vigente | `Plan 159`, `160` y `161` `Executed`; `ADR-19` y `ADR-16` `Accepted`; `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md` activos; el producto de Etapa A es Working (`active`, no normativo) | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md`; `docs/working/audits/INDEX.md` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (Change Lifecycle DEV), RFC-69 (taxonomía y placement), ADR-16 (autoridad, `AU-3`/`AU-5`/`AU-6`), ADR-19 (envelope), `docs/VERSIONING.md` §4/§4.1/§7, VC-1/GC-1/LC-1/PC-1, `.agents/policies/authority.md`. `NOT_APPLICABLE`: RFC-56 (sin efecto payload), RFC-46 (no se reescriben artefactos históricos) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **directiva del mantenedor (2026-10-12)** que ordena preparar el material mínimo en la rama bloqueada. Scope declarado: `docs/plans/162-instrumento-decision-od1-alcance-f-c.md` (este artefacto), `docs/plans/INDEX.md`, `CHANGELOG.md`, `ROADMAP.md` | **humano** | la declaración del humano en la consigna de intake |

## Criterio de entrada

- [x] Baseline verificada (rama `dev`, `HEAD` `b70751a`, `git status --porcelain` vacío).
- [x] `F-A`, `F-B` y Etapa A confirmadas `Closed` en sus artefactos.
- [x] `OD-1` localizado como pending decision **bloqueante** con owner mantenedor (`<PLAN-161>`) y como fila de blocker en `ROADMAP.md`.
- [x] **Verificación de autoridad ejecutada**: ninguna fuente viva contiene la decisión de alcance → `OD1_BLOCKED` (ver `## Verificación de autoridad`).
- [x] Evidencia primaria de Etapa A leída en el producto cerrado (matriz 28 × 9) y en su `## Checkpoint / cierre`.
- [x] Batería canónica de baseline registrada (`check_plan_citations` = 26 citas rotas históricas).

## Alcance

### IN SCOPE

1. La **verificación de autoridad** de `OD-1` y su registro (`OD1_BLOCKED`).
2. La **evidencia trazable** que acota la decisión: lo que sí determina (D-1…D-7), las interpretaciones R1/R2/R3 con su soporte y su tensión, y lo que no determina.
3. La **forma decision-ready** del acto: pregunta `OD-1`, opciones `Q-a`…`Q-d`, consecuencias, protección contra inferencias indebidas, registro exigido y criterios de cierre del acto (`AC-1`…`AC-12`).
4. La reconciliación mínima derivada: `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`.

### OUT OF SCOPE

1. **Decidir** `OD-1`: elegir R1/R2/R3, definir `F-C`, fijar su boundary o autorizar Etapa B.
2. Crear un Plan de `F-C` o de Etapa B, o declararlos `Aprobado para ejecución`.
3. **Implementar** cualquier capacidad: provider/modelo, aislamiento/sandbox, Memory, objetivos multi-Change, Discovery, Skills, Agent Worker, retry/recovery, concurrencia, telemetría, u otra.
4. Modificar `docs/CONVENTIONS.md`, `docs/adr/**`, `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` o `dist/`.
5. Cambiar defaults de autonomía, activar `--sae`, alterar el envelope de efectos de `F-B` o los techos de recurso.
6. Convertir hallazgos de Etapa A (madurez baja) en requisitos: son **evidencia para delimitar**, nunca autorización de desarrollo.
7. Limpieza documental lateral, refactors, renombrados o reorganización.

### DEPENDENCIES

```text
F-A        = CLOSED
F-B        = CLOSED
OD-2       = CLOSED          (derivación parcial descartada: no pertenece a F-C)
OD-4       = ALREADY_CLOSED  (--sae permanece opt-in)
OD-6       = CLOSED
OD-7       = ALREADY_CLOSED
Etapa A    = CLOSED          (Capability & Guarantee Matrix disponible como evidencia)
F-C        = NOT_IMPLEMENTED
Etapa B    = NOT_STARTED
OD-1       = PENDING_AUTHORITY — bloqueante, owner mantenedor
```

## Entregables

1. `docs/plans/162-instrumento-decision-od1-alcance-f-c.md` (**este archivo**) — instrumento decision-ready.
2. `ROADMAP.md` — fila de blocker `OD-1` con el artefacto accionable (instrumento) y su owner de pending; card de `NEXT` con el instrumento.
3. `docs/plans/INDEX.md` — serie **Nonagésima primera**, fila del Plan 162 y encabezado de estado.
4. `CHANGELOG.md` — ítem `[Unreleased]` del Change.

## Pasos

1. **Paso 0 — preflight.** Baseline, dependencias y baseline de checkers.
2. **Paso 1 — verificación de autoridad.** Aplicar las reglas de `.agents/policies/authority.md`, `.agents/AGENTS.md`, ADR-16 y SAE §8; comprobar si existe acto del mantenedor sobre el alcance de `F-C`; concluir `OD1_BLOCKED` y registrarlo.
3. **Paso 2 — evidencia.** Reconstruir D-1…D-7 desde los artefactos cerrados y las interpretaciones R1/R2/R3 con su soporte y su tensión.
4. **Paso 3 — forma decision-ready.** Fijar `Q-a`…`Q-d`, las consecuencias, lo que no debe inferirse, el registro exigido y `AC-1`…`AC-12`.
5. **Paso 4 — reconciliación mínima.** Actualizar `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`; **no** tocar `docs/CONVENTIONS.md` ni ADRs (el registro normativo pertenece al acto).
6. **Paso 5 — verificación.** Batería canónica, gates C-1/C-2/C-3, verificación de coherencia de las menciones a `F-C`/Etapa B/`OD-1` y de scope.
7. **Paso 6 — cierre.** `## Validation anchor`, `## Checkpoint / cierre`, nota de ejecución y commits atómicos.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | Este Change no produce efectos fuera de la frontera inmediata: escribe únicamente paths locales dentro de su `Scope` declarado y no ejecuta red, git remoto, instalaciones ni cambios destructivos. | — (declaración negativa; no requiere autorización de efecto) | `authorized` |

## Criterios de salida

- [x] La verificación de autoridad está registrada y concluye `OD1_BLOCKED` con la regla aplicable citada, sin elegir interpretación.
- [x] La evidencia está trazada: D-1…D-7, R1/R2/R3 con soporte y tensión, y la distinción explícita entre lo que la evidencia determina y lo que no.
- [x] La forma decision-ready está completa: `Q-a`…`Q-d`, consecuencias de no decidir, protección contra inferencias indebidas, registro exigido y `AC-1`…`AC-12`.
- [x] **`F-C` permanece `NOT_IMPLEMENTED`, Etapa B `NOT_STARTED` y `OD-1` `PENDING_AUTHORITY`**: no se definió alcance, no se creó Plan de `F-C`, no se modificó `docs/CONVENTIONS.md` ni ningún ADR.
- [x] `F-A`, `F-B` y Etapa A permanecen `Closed`; 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`.
- [x] Coherencia de menciones: ninguna fuente viva afirma que `F-C` esté definida, autorizada o iniciada; el instrumento queda como artefacto accionable de `OD-1`.
- [x] Batería canónica en verde (con el rojo preexistente declarado) y sin aumento de citas rotas.
- [x] `## Validation anchor` y `## Checkpoint / cierre` registrados; `Status: Executed` con condición derivada evaluada.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Verificación factual adicional: coherencia de las menciones a `F-C`, Etapa B y `OD-1` en las fuentes vivas (grep dirigido, sin contradicciones); `git diff --name-only HEAD` ⊆ `Scope`; 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`.
## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** las tres rutas que la identidad de contenido mide — `CHANGELOG.md`, `ROADMAP.md` y `docs/plans/INDEX.md`. Queda fuera del scope **medido** la governance del propio Change (este artefacto), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 149/155–161). El scope autorizado por `P-8` tiene una ruta más: este artefacto.
- **Validation command-set:** los siete comandos de `docs/VERSIONING.md` §4.1 + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + la verificación factual del Change: la comprobación de autoridad registrada en `## Verificación de autoridad`, la coherencia de las menciones vivas a `F-C`, Etapa B y `OD-1`, y la verificación de scope.
- **Effective inputs (repo content):** el scope declarado; `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` (pending de `OD-1`); `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` (evidencia primaria de Etapa A); `docs/adr/19-autonomy-envelope-authority.md` y `docs/adr/16-change-lifecycle-authority.md`; `docs/CONVENTIONS.md`; `.agents/policies/authority.md` y `.agents/policies/supervised-autonomous-execution.md`; el corpus completo de `docs/plans/`, `docs/rfc/` y `docs/adr/` como población de `check_plan_citations` y de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada de `check_protocol_invariants`; y el estado Git de `dev`.
- **Observed dependencies:** stdlib únicamente; el CLI `git`; `pytest` con basetemp externo al repositorio (`tests/pytest_isolation.py`). Sin red.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; `pytest` 9.0.3; repositorio bajo OneDrive. **Clase ambiental declarada:** `check_dist_sync.py` **no** aplica (local-only, verde sólo en `master`); `check_plan_citations.py` sigue rojo por las **26** citas rotas históricas, **sin aumento**. No se consumió red, provider ni credenciales.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `243a01c1d709af4db5623fe9f11975da961f678a` — tree id del índice staged del scope medido (`tools/scoped_content_identity.py`, source `staged`), computado antes de escribir los registros de cierre.
  - **Delta scoped identity (scope S = las tres rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `ae8399c00342149937824a918181e4102c7e68565a04ca0dc72572df0cc2c59d`.
  - **Scope set (repo-relative paths, ordenados):** `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/INDEX.md`
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): **PASS** (216 archivos, 10457 referencias); verification-02 (`check_plan_citations`): **FAIL preexistente** — 26 citas rotas, sin aumento; verification-03 (`check_plan_structure`): **PASS**; verification-04 (`check_taxonomy_coherence`): **PASS**; verification-05 (`check_session_artifacts`): **PASS**; verification-06 (`check_version_state`): **PASS**; verification-07 (`python -m pytest tests/`): **PASS** — `1316 passed` en 317,53 s; verification-08 (C-1): **ANOMALY=0**; verification-09 (C-2): **ANOMALY=0**; verification-10 (C-3): **GAP=0**, `ANOMALY=0`. Verificación factual: la comprobación de autoridad concluye `OD1_BLOCKED` con su regla citada; ninguna fuente viva afirma que `F-C` esté definida, autorizada o iniciada; `git diff --name-only` ⊆ el scope de `P-8`; **0 diff** en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio del mantenedor: `docs(governance): prepare the OD-1 decision instrument for the F-C scope (plan 162)`. Se identifica por su mensaje (convención anti-circularidad). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `243a01c1d709af4db5623fe9f11975da961f678a`, delta scoped identity `ae8399c00342149937824a918181e4102c7e68565a04ca0dc72572df0cc2c59d`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `ae8399c00342149937824a918181e4102c7e68565a04ca0dc72572df0cc2c59d` / `243a01c1d709af4db5623fe9f11975da961f678a`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de cierre incluye la governance del Change (este artefacto), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); C-2 clasificó el corpus sin `ANOMALY`.
- **Governance aplicada:** instrumento decision-ready creado (este artefacto); `ROADMAP.md` (fila de blocker `OD-1` con el artefacto accionable y el owner del pending; card de `NEXT` con el instrumento); `docs/plans/INDEX.md` (encabezado de estado y serie **Nonagésima primera** + fila); `CHANGELOG.md` `[Unreleased]`; `## Findings`/`## Correcciones` con `<PLAN-162>:F-1`/`C-1`; `**Status:** Executed`. Sin RFC-56 (0 diff en `protocol/`), sin ADR nuevo, sin `VERSION` bump ni tag.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados y su aspecto: `ROADMAP.md` (aspecto: la fila de blocker `OD-1` nombraba sólo el pending del Plan 161 y no el artefacto accionable, de modo que el próximo paso no era ejecutable desde el mapa; actualización: la fila cita el instrumento y el owner del pending, y la card de `NEXT` lo enlaza; evidencia: el diff). `docs/plans/INDEX.md` (aspecto: el Plan 162 no existía en el registro; actualización: encabezado de estado, serie Nonagésima primera y fila con el resultado `OD1_BLOCKED` y el material preparado; evidencia: el diff). `CHANGELOG.md` (aspecto: el Change no figuraba; actualización: ítem `[Unreleased]` con la verificación de autoridad, el material preparado y lo no realizado; evidencia: el diff). **No** se actualizó `docs/CONVENTIONS.md` ni ningún ADR: el registro normativo pertenece al acto que aún no se ejerció. **No** se actualiza ningún documento histórico (RFC-46), y `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/` quedan con **0 diff** (fueron inspeccionados como evidencia, nunca escritos).
- **Roadmap impact:** `REQUIRED` — reconciliado en el artefacto que posee el estado. Ítems afectados: la fila de blocker `OD-1` pasa a nombrar el **instrumento accionable** además del owner del pending, y la card de `NEXT` («Revisión del alcance de `F-C`/Etapa B») enlaza el instrumento. **No** se crea, completa ni re-prioriza ninguna iniciativa: `NOW` y `LATER` conservan sus ítems y Etapa B permanece en `LATER` sin cambio de estado, prioridad ni dependencia. La decisión **no** se toma, de modo que el mapa no cambia de dirección.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.
## Findings / Correcciones / Pending

### Findings

- `<PLAN-162>:F-1` — estado: `resolved`; severidad: `medium`; observación: dos citas del instrumento usaban un **número de línea** como ancla de sección, que el checker clasifica `non-heading anchor`: habrían sumado **dos citas rotas nuevas** al baseline del corpus (26 → 28); evidencia original: la salida de `python tools/check_plan_citations.py` («Broken citations: 28», con las dos entradas del Plan 162); estado git observado: worktree de `dev` sobre `b70751a`, sin commit; provenance original: verificación de cierre durante la ejecución (Paso 5); resolución: `resolved` por `<PLAN-162>:C-1`.
- `<PLAN-162>:F-2` — estado: `resolved`; severidad: `medium`; observación: una sustitución de texto durante el cierre usó como marcador una mención literal que aparecía **dentro** del Paso 6, de modo que el reemplazo consumió el resto de ese paso y tres secciones del propio artefacto (`## Efectos declarados`, `## Criterios de salida` y `## Verificación`); habría quedado estructuralmente incompleto sin que ningún checker canónico lo detectara (el checker de estructura verifica nombre, header, placeholders y espejo del INDEX, no la presencia de secciones); evidencia original: la lectura del árbol de encabezados tras el cierre frente al contenido de la creación; estado git observado: worktree de `dev` sobre `b70751a`, sin commit; provenance original: verificación estructural durante el cierre (Paso 6); resolución: `resolved` por `<PLAN-162>:C-2`.

### Correcciones

- `<PLAN-162>:C-1` — refs origen: `<PLAN-162>:F-1`; alcance de revalidación: `docs/plans/162-instrumento-decision-od1-alcance-f-c.md` (dos citas sustituidas por anclas de sección resolubles), sin efecto sobre el scope medido; evidencia: `check_plan_citations` vuelve a **26** citas rotas — el baseline — sin citas nuevas.
- `<PLAN-162>:C-2` — refs origen: `<PLAN-162>:F-2`; alcance de revalidación: `docs/plans/162-instrumento-decision-od1-alcance-f-c.md` (restitución del Paso 6 completo y de las tres secciones consumidas, con los ocho criterios de salida en `[x]` y el bloque de verificación íntegro), sin efecto sobre el scope medido (el artefacto está fuera de él); evidencia: el árbol de encabezados vuelve a contener las tres secciones entre `## Pasos` y `## Validation anchor`, y `check_plan_structure` sigue conforme.
### Pending decisions

- **`OD-1` — propiedad: `<PLAN-161>`** (`docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md:Pending decisions`), que la registra como decisión **bloqueante** con owner **mantenedor**. Este instrumento **no la duplica y no la resuelve**: materializa la forma decision-ready (pregunta, opciones, consecuencias, boundary, registro exigido y criterios de cierre del acto) para que el acto pueda ejercerse. Estado: **`PENDING_AUTHORITY`** (sin cambio); `blocking` = **sí** para el tramo posterior; `owner` = mantenedor; `efecto downstream` = `F-C` y Etapa B permanecen sin definir, autorizar ni iniciar; `ADR-worthiness` = **a resolver en el acto** (`Q-d`).

## Riesgos

1. **Convertir la lectura dominante en decisión.** Mitigación: `OD1_BLOCKED` registrado; `Q-a`…`Q-d` sin resultado nominado; prohibición explícita de elegir R1/R2/R3.
2. **Convertir hallazgos de Etapa A en requisitos de implementación.** Mitigación: `## Qué NO debe inferirse` (puntos 1–3) y `OUT OF SCOPE` ítem 6.
3. **Duplicar la propiedad de `OD-1`.** Mitigación: la sección `### Pending decisions` **referencia** `<PLAN-161>` y declara que no la duplica (regla `PC-1`: la decisión bloqueante persiste en el artefacto que la posee).
4. **Registrar normativa antes del acto.** Mitigación: `docs/CONVENTIONS.md` y los ADRs están **fuera de alcance**; el registro normativo pertenece al acto.
5. **Ampliar el alcance hacia Etapa B.** Mitigación: `OUT OF SCOPE` 1–2; el Plan no crea ningún Plan de `F-C`/Etapa B ni los autoriza.
## Trazabilidad

```text
Etapa A (Plan 161, Closed)  →  Capability & Guarantee Matrix (evidencia)
        │
        ▼
OD-1  →  VERIFICACIÓN DE AUTORIDAD  →  OD1_BLOCKED (decisión de alcance, reserva humana)
        │
        ▼
Plan 162  →  instrumento decision-ready (Q-a…Q-d, AC-1…AC-12, registro exigido)
        │
        ▼
ACTO DEL MANTENEDOR  →  registro normativo (CONVENTIONS ± ADR)  →  OD-1 RESOLVED
        │
        ▼
Change de F-C (sólo entonces)  →  Etapa B
```

## Nota de ejecución

*2026-10-12. Ejecutado en `dev` @ `b70751a` (baseline del preflight: worktree limpio; `dev` ahead 13 de `origin/dev`; `VERSION` del payload `12.0.1` sin tag; batería canónica en verde).*

Una sola pasada, en el orden del `## Pasos`:

1. **Paso 0 — preflight.** Baseline, dependencias (`F-A`, `F-B` y Etapa A `Closed`) y baseline de citas rotas registrado (**26**).
2. **Paso 1 — verificación de autoridad.** Aplicadas las reglas de `.agents/policies/authority.md`, del `AGENTS.md` raíz (regla 3), de la frontera humana de SAE §8 y de ADR-16 (`AU-3`/`AU-5`/`AU-6`); comprobado que **ninguna fuente viva** contiene el acto del mantenedor sobre el alcance de `F-C`; concluido y registrado **`OD1_BLOCKED`**. **No** se eligió entre R1, R2 y R3.
3. **Paso 2 — evidencia.** Reconstruidos D-1…D-7 y las tres interpretaciones con su soporte documental y su tensión, distinguiendo explícitamente lo que la evidencia determina de lo que no.
4. **Paso 3 — forma decision-ready.** Fijados `Q-a`…`Q-d`, las consecuencias de no decidir, las siete inferencias prohibidas, el registro exigido del acto y los criterios de cierre `AC-1`…`AC-12`.
5. **Paso 4 — reconciliación mínima.** `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`. `docs/CONVENTIONS.md` y los ADRs **no** se tocaron: el registro normativo pertenece al acto.
6. **Paso 5 — verificación.** Batería canónica (`1316 passed`), seis checkers en verde con **26** citas rotas (baseline) y gates C-1/C-2/C-3 sin `ANOMALY`; verificación factual de coherencia de las menciones a `F-C`, Etapa B y `OD-1` y de scope (0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`).
7. **Paso 6 — cierre.** `## Validation anchor` A1, `## Checkpoint / cierre`, esta nota y commit atómico.

**Dos findings reales, ambos resueltos antes de la validación y declarados en `## Findings`:** `<PLAN-162>:F-1` (dos citas con ancla de número de línea producían `non-heading anchor` y habrían sumado dos citas rotas al baseline) y `<PLAN-162>:F-2` (una sustitución de texto durante el cierre consumió `## Efectos declarados`, `## Criterios de salida` y `## Verificación` del propio artefacto; restituidas y verificadas estructuralmente). La identidad de contenido A1 se computó después de `C-1`; `C-2` no altera el scope medido (el artefacto está fuera de él).

**Resultado.** `OD1_BLOCKED` por falta de autoridad, con el instrumento decision-ready completo. **No** se decidió, **no** se definió `F-C`, **no** se creó un Plan de `F-C`/Etapa B, **no** se modificó `docs/CONVENTIONS.md` ni ningún ADR y **no** se implementó ninguna capacidad.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1).
Committed = TRUE  — commit atómico en `dev`, identificado por su mensaje.
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump, sin tag, sin promoción a `master`, sin `dist`.
```

`F-C = NOT_IMPLEMENTED` · `Etapa B = NOT_STARTED` · `OD-1 = PENDING_AUTHORITY` (owner: mantenedor).

**Próximo paso exacto.** El mantenedor ejerce el acto de `OD-1` —`Q-a`…`Q-d`— registrándolo según `## Registro del acto (dónde debe quedar)`; sólo después se crea el Change de `F-C`.
