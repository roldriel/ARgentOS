# Plan 117 — Adopción de la feature DEV de deliberación adversarial (Adversarial Deliberation Feature Adoption)

**Status:** Executed (2026-09-12; los 10 criterios de salida satisfechos; condición derivada `Closed` — docs-only, sin release; ver `## Checkpoint / cierre`)
**Fecha:** 2026-09-12
**RFC:** — (vía plan; sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (sin efecto en payload)
**Change Level:** L1 (`max(coordination=1, scope=1, architectural=0, release=0, duration=1)`: cambio DEV docs-only, un área documental (`docs/`), sin impacto arquitectónico ni de release)
**Depende de:** Plan 114 (`Closed`) y Plan 116 (`Closed`) — la Working Convention y los cuatro Trials son la evidencia contractual de la capacidad adoptada
**Origen:** Phase 4 — DEV Jury Trial Feature Adoption Specification (decisión humana `DEFINITION-B = ACCEPTED`); planes 114 y 116; `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`

## Creación

**H1 = GO** otorgado por el mantenedor mediante el prompt de Phase 5 (2026-09-12), que autoriza exclusivamente: (i) crear la autorización de este cambio (Clase B, docs-only); (ii) materializar el contrato de adopción de la feature DEV de deliberación adversarial especificado en Phase 4; (iii) cerrar el `GAP-02` (regla de record-home) con el mínimo texto; (iv) actualizar el banner de la convención, `docs/working/proposals/INDEX.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`; (v) validar con la batería canónica y los gates de lifecycle existentes; (vi) registrar el acto humano de cierre como decisión separada; (vii) commitear el cambio si y solo si los gates aplicables están satisfechos.

Decisiones del mantenedor registradas en el mismo prompt (**no se reabren en este Plan**): `D-1` **Definition-B aceptada** (la feature DEV es una capacidad Working, no normativa y reutilizable de deliberación adversarial, reconocible, invocable, reutilizable y disponible, nunca obligatoria, normativa, gate, lifecycle state, autoridad ni integración obligatoria al Change Lifecycle); `D-2` naturaleza `ADOPTED + WORKING + NON-NORMATIVE`, **sin crear un lifecycle state nuevo**; `D-3` nombre canónico DEV `Adversarial Deliberation` (el término «Jury Trial» solo permanece en los identificadores del predicate: `JURY_TRIAL_CLOSED`, `JURY_TRIAL_DEV_FEATURE_CLOSED`; sin semántica de jurado, panel, votación, N jurados ni ranking); `D-4` el Protocol-native Jury Trial permanece **FUTURE / NOT STARTED / OUT OF SCOPE**; `D-5` sin nueva arquitectura; `D-6` sin integración al Change Lifecycle; `D-7` sin routing operacional; `D-8` sin dogfood adicional.

Alcance de la autorización: **no** promueve la convención a gobernanza, **no** la vuelve obligatoria, **no** crea mecanismo alguno, **no** toca `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `ROADMAP.md`, `AGENTS.md`, plantillas, `docs/CONVENTIONS.md` ni `docs/VERSIONING.md`, y **no** desarrolla el Jury Trial del Protocol.

## Objetivo

Materializar documentalmente la adopción de la feature DEV de deliberación adversarial —definición de feature, contrato de adopción, límites, evidencia y predicate de cierre—, cerrar el `GAP-02` de record-home con el mínimo texto que hace explícita la regla ya vigente en `PC-1`/`LC-1`, validar el cambio con la batería canónica y los gates de lifecycle existentes, registrar el acto humano de cierre como decisión separada, y **derivar** `JURY_TRIAL_DEV_FEATURE_CLOSED = TRUE` únicamente si C1–C8 resultan verificables con evidencia.

## Alcance

**Dentro del alcance:** este Plan; `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` (una sección nueva de registro —record home— y el banner de estado de adopción); `docs/working/proposals/INDEX.md` (fila descriptiva de la convención); `docs/plans/INDEX.md` (fila + serie de este Plan); `CHANGELOG.md` (ítem `[Unreleased]`).

**Fuera del alcance:** `protocol/` (incluido `protocol/.agents/VERSION`); `dist/`; `runtime/`; `tools/`; `tests/`; `.agents/`; `ROADMAP.md`; `AGENTS.md` raíz; plantillas (`docs/plans/_TEMPLATE.md`, `docs/rfc/_TEMPLATE.md`, `docs/adr/_TEMPLATE.md`); `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; Planes 114 y 116 (no se modifican, no se reabren); RFCs; ADRs; `master`; tags; release; VERSION bump; integración con el Change Lifecycle; routing operacional; código, Tools, Skills, Workers, Capabilities, checkers, tests automatizados de la feature, registry, entidad `Trial`, ID global, capa de persistencia, schema, state machine, lifecycle state nuevo, telemetría, métricas, instrumentación de costo, aislamiento técnico, ACL, sandbox, enforcement runtime, votación, N jurados, ranking y dogfood adicional.

## Criterio de entrada

- [x] Repositorio en `dev`, HEAD confirmado (`git rev-parse HEAD` = `9f70ad0`), working tree sin cambios fuera de los preexistentes (`.codegraph/` untracked; directorios de pytest del sandbox).
- [x] Plan 114 `Executed` con condición derivada `Closed` (docs-only) y Plan 116 `Executed` con condición derivada `Closed` (docs-only).
- [x] `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` existe con sus 14 secciones y banner Working/no normativa.
- [x] Convención registrada en `docs/working/proposals/INDEX.md`.
- [x] Siguiente número libre confirmado en `docs/plans/INDEX.md` (117; último registrado: 116).
- [x] Ningún artifact equivalente a Phase 5 existe (verificado: sin `docs/plans/117*`, sin fila de adopción en los INDEX).
- [x] `protocol/.agents/VERSION` = `11.2.0` (sin tag; `11.0.0`/`11.0.1` taggeadas en `master`).
- [x] H1 = GO del mantenedor registrado en `## Creación`; `**Status:**` fijado en `Aprobado para ejecución`.
- [x] Batería canónica verde en el estado baseline (los 6 checkers PASS; la pierna `pytest` presenta la clase ambiental preexistente de permisos del sandbox, documentada en la Nota de ejecución y no causada por este cambio).

## Entregables

1. `docs/plans/117-adversarial-deliberation-feature-adoption.md` — este Plan (definición de feature, contrato de adopción, predicate de cierre, evidencia, limitaciones, decisión humana, validación, verificación y cierre).
2. `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` — sección de registro (record home) y banner de estado de adopción.
3. `docs/working/proposals/INDEX.md` — fila descriptiva de la convención (adopted / available / Working / non-normativa).
4. `docs/plans/INDEX.md` — fila + serie de este Plan.
5. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 117, —)`.

## Pasos

1. **Baseline e intake:** `git status --short --branch`, `git rev-parse HEAD`; verificar Planes 114/116, convención, INDEXes, `VERSION` y ausencia de artifact equivalente; registrar la clasificación (RFC-56 clase —; Change Level L1; dominio DEV docs).
2. **GO:** registrar H1 = GO y las decisiones D-1…D-8 del mantenedor; fijar `**Status:**` en `Aprobado para ejecución`.
3. **GAP-02:** agregar a la convención la sección de registro que hace explícita la regla ya vigente en `docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)` y `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`, con la restricción de contenedores de lineage y la prohibición de crear artifacts para alojar un Trial.
4. **Definición y contrato:** persistir en este Plan la definición final de la feature DEV, el contrato de adopción (15 elementos) y el predicate `JURY_TRIAL_DEV_FEATURE_CLOSED` con C1–C8 y su relación explícita con el predicate del MVP `JURY_TRIAL_CLOSED` (precondition, nunca sustituto).
5. **Evidencia y límites:** registrar la evidencia existente (cuatro Trials, dos Planes, dos configuraciones de ejecutor, confrontación acotada, NO CHANGE, reconstruibilidad, checkers canónicos) y las limitaciones declaradas, sin métricas inventadas, sin afirmar independencia epistemológica, sin afirmar Q6 y sin afirmar mejora causal de la decisión.
6. **Registros:** actualizar el banner de la convención, `docs/working/proposals/INDEX.md`, `docs/plans/INDEX.md` y `CHANGELOG.md:[Unreleased]`.
7. **Validación A1:** batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) sobre el estado de contenido (antes de los registros de cierre).
8. **Verificación C1–C8:** tabla explícita con evidencia concreta por condición (ninguna condición se marca verdadera por apariencia).
9. **Cierre:** completar `## Validation anchor` (VC-1) y `## Checkpoint / cierre` (GC-1); revalidar (A2) sobre el estado final; registrar el acto humano de cierre como decisión separada; derivar la condición `Closed` (docs-only, sin release).
10. **Commit:** revisar `git diff`, `git status` y el change surface; confirmar ausencia de cambios en Protocol y en las capas excluidas; commit atómico en `dev` (Conventional Commit en inglés).

## Definición final de la feature DEV

> **Adversarial Deliberation (DEV)** es una **capacidad Working, no normativa y reutilizable** del entorno DEV de ARgentOS para obtener **evidencia adversarial trazable sobre una decisión candidata antes de que la decisión se tome**. Una deliberación se **invoca por decisión explícita, justificada y con motivo registrado** —nunca automáticamente— sobre una decisión con al menos dos direcciones materiales posibles o cuya viabilidad esté en duda real. Declara un marco (referencia al problema, candidata, criterios obligatorios evaluables, modo y límites), produce **al menos dos pasadas de evaluación atribuidas** cuyas conclusiones se **comprometen antes de la revelación**, declara **procedencia** (mismo/distinto ejecutor, material compartido, relación con conclusiones previas) y **nunca afirma independencia epistemológica**, puede sostener **una confrontación acotada y con propósito declarado**, **sintetiza** sin introducir contenido no soportado preservando el **desacuerdo**, emite un **veredicto** (`VIABLE`|`NOT_VIABLE`|`UNDETERMINED`; `PREFERRED(A)`|`PREFERRED(B)`|`TIE`|`UNDETERMINED`) con **base declarada** y **razón de terminación**, puede emitir una **recomendación advisory opcional**, y deja la **decisión humana fuera del mecanismo**. Su producto es **evidencia adicional útil**, nunca una decisión; `NO CHANGE` y «valor no demostrado» son resultados legítimos. Su registro se asienta **en el artifact que posee la decisión** —o, si ese artifact está cerrado, en un **artifact nuevo que lo referencia**— fuera de los contenedores de lineage del lifecycle, y es reconstruible por un tercero. No crea gate, lifecycle state, obligación, autoridad ni mecanismo nuevo, y **no** es el Jury Trial del Protocol.

## Contrato de adopción de la feature DEV

1. **Identidad / nombre.** Nombre canónico DEV: **Adversarial Deliberation**. El label de continuidad en los identificadores del predicate es `JURY_TRIAL_*`. «Jury Trial» **no** significa jurado, panel, votación, N jurados ni ranking —todo ello explícitamente excluido de DEV—. Hogar documental: `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`.
2. **Scope.** Deliberación adversarial de decisiones candidatas en el repositorio DEV, ejecutada por agentes y/o el humano, registrada en el artifact que posee la decisión. Alcance DEV únicamente.
3. **Naturaleza.** Working, no normativa, pre-canónica, sin autoridad. Adoptada como **disponible**, nunca como **obligatoria**. No crea gate, lifecycle state, obligación ni gobernanza. Adopción ≠ promoción; reutilizable ≠ obligatorio; disponible ≠ requerido.
4. **Invocación.** Explícita, declarada, con motivo registrado, opcional, neutral respecto del estado del repositorio y nunca automática; corresponde solo a decisiones con ≥2 direcciones materiales o viabilidad en duda real donde el resultado pueda cambiar lo que se hará.
5. **Registro requerido.** Un registro en el artifact que posee la decisión (o, si está cerrado, en un artifact nuevo que lo referencia) con: marco declarado; ≥2 pasadas atribuidas con ejecutor, material recibido/compartido y relación con conclusiones previas; condición de compromiso; procedencia declarada; confrontación (si la hubo); síntesis con orígenes y desacuerdo preservado; veredicto con base declarada y razón de terminación; recomendación o su ausencia deliberada; y el estado de la decisión humana. Fuera de los contenedores de lineage del lifecycle. Sin registry, ID, schema, plantilla ni almacenamiento.
6. **Procedimiento.** Marco declarado → pasadas atribuidas → compromiso → revelación → confrontación acotada opcional → síntesis → veredicto con base declarada → recomendación advisory opcional → decisión humana fuera del mecanismo. La terminación es una **razón registrada**, no un lifecycle state.
7. **Frontera de autoridad.** Puede: invocar, enmarcar, solicitar perspectivas, evaluar, atacar, confrontar, sintetizar, emitir veredicto, emitir recomendación, registrar y escalar. No puede: decidir, autorizar, aprobar, resolver findings, cambiar el lifecycle, crear gobernanza, liberar releases, reemplazar la validación ni reemplazar la verificación. `Verdict ≠ Recommendation ≠ Human Decision`. Contractual/documental — sin enforcement.
8. **Claim de independencia.** A lo sumo: **ejecutores distintos, declarados, como condición necesaria y no suficiente**, más la no exposición declarada a conclusiones previas. La independencia epistemológica nunca se afirma y no es requisito. El aislamiento técnico está prohibido.
9. **Claim de valor.** La capacidad debe producir **evidencia adicional útil** para una decisión real. **No** se le exige mejorar decisiones y no existe métrica, umbral ni tasa de éxito. `NO CHANGE`, `UNDETERMINED` y «valor no demostrado» son resultados legítimos.
10. **Frontera de la decisión humana.** La decisión pertenece siempre a la autoridad DEV existente y se registra **fuera** del mecanismo (acto separado, o pending decision con owner en el artifact que posee la decisión). El mecanismo nunca la improvisa.
11. **Reutilización.** Reutilizable aplicando el procedimiento documentado a una decisión real distinta y registrando el resultado conforme al elemento 5; demostrada sobre 4 decisiones reales en 2 Planes con 2 configuraciones de ejecutor, 1 confrontación acotada y 1 NO CHANGE.
12. **Discoverability.** Un hogar documental fijo, registrado en `docs/working/proposals/INDEX.md`, alcanzable por la discovery documental existente del repositorio, con reglas de invocación explícitas. Sin routing operacional.
13. **Limitaciones.** Sin garantía de corrección; sin independencia epistemológica; sin impacto observado sobre decisiones humanas; sin enforcement; sin comparabilidad entre Trials; un solo modo ejercitado (`viability`); ramas de degradación especificadas pero no ejercitadas exhaustivamente; sin datos de costo; ejecución manual y declarativa.
14. **No-requisitos explícitos.** Promoción a gobernanza; RFC; ADR; Skill; Worker; Tool; checker; gate; state machine; lifecycle state; registry; entidad `Trial`; ID global de Trial; capa de persistencia; plantilla; telemetría; métricas; votación; N jurados; ranking; sandbox; ACL; aislamiento; enforcement runtime; tests automatizados; integración al Change Lifecycle; routing desde `.agents/`, `ROADMAP.md` o `AGENTS.md` raíz.
15. **Frontera con el Protocol.** Distinta del Protocol-native Jury Trial, que permanece **FUTURE / NOT STARTED / OUT OF SCOPE** y no es condición de cierre.

## Closure predicate

```text
JURY_TRIAL_CLOSED              = predicate del MVP (contrato ∧ arquitectura ∧ implementación
                                 ∧ integración ∧ validación ∧ verificación ∧ dogfood
                                 ∧ documentación ∧ governance) — SATISFECHO en el cierre
                                 del Plan 116. Se usa aquí SOLO como precondition;
                                 nunca se reevalúa ni sustituye al predicate de la feature.

JURY_TRIAL_DEV_FEATURE_CLOSED  = predicate de adopción de la feature:

      JURY_TRIAL_CLOSED
   ∧  C1  contrato de adopción persistido y autorizado por el mantenedor
   ∧  C2  procedimiento especificado y reutilizable en la convención
   ∧  C3  record home y regla de contenedor especificados (GAP-02 cerrado)
   ∧  C4  frontera de autoridad especificada y sin cambios
   ∧  C5  la capacidad permanece Working/no normativa y no existe mecanismo nuevo
   ∧  C6  discoverability y standing adoptado explícitos
   ∧  C7  evidencia y limitaciones declaradas y acotadas
   ∧  C8  cambio materializador validado y acto humano de cierre registrado
```

`JURY_TRIAL_CLOSED` **no** se reutiliza como sustituto de `JURY_TRIAL_DEV_FEATURE_CLOSED`: el primero pertenece al MVP DEV cerrado por el Plan 116 y se conserva únicamente como condición previa satisfecha.

## Evidencia

- **Capacidad materializada y demostrada:** `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` (14 secciones, clase Working, no normativa) creada y registrada en `docs/working/proposals/INDEX.md` por el Plan 114.
- **Cuatro Trials reales sobre decisiones reales y verificables**, registrados conforme a la convención: `<PLAN-105>` (elevación ADR de la arquitectura terminológica), `<PLAN-114>:F-1`/`F-2` (reconocimiento formal de findings), `<PLAN-114>:F-3` (intervención sobre el ejemplo del template) y el release batch `11.1.0`/`11.2.0`. Registros: `docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending` y el Plan 116 (registros de los Escenarios A, B y C).
- **Dos Planes** (`docs/plans/114-adversarial-deliberation-mvp.md` y `docs/plans/116-adversarial-deliberation-mvp-closure.md`), ambos `Executed` con condición derivada `Closed`.
- **Dos configuraciones de ejecutor:** `ejecutores: mismo` (Plan 114, Escenarios B y C) y `ejecutores: distinto` con subagente de deliberación en contexto separado (Escenario A del Plan 116), declarado como condición de procedencia y **sin** afirmación de independencia epistemológica.
- **Confrontación acotada** según §7 de la convención, ejercitada una vez (Escenario C), terminada por el criterio de valor.
- **`NO CHANGE` como resultado legítimo** registrado en el Escenario B, sin diffs asociados.
- **Reconstruibilidad:** los cuatro registros contienen los campos contractuales de §5 (doce campos por pasada) y §9 (base declarada del veredicto), con premisas citadas como `ruta:sección` y razón de terminación `VERDICT` en los cuatro casos.
- **Frontera de autoridad respetada:** ninguna decisión humana fue improvisada; tres decisiones deliberadas quedaron como pending decisions escaladas con owner y la aceptación del cierre del MVP fue un acto humano separado.
- **Evidencia de checkers** (estado del repositorio al iniciar este Plan): los 6 checkers canónicos PASS; C-1 `VALID=21 GAP=1` (Plan 115), C-2 `VALID=20 GAP=2` (Planes 115 y 116; asunto ajeno a este cierre, ver `## Riesgos`), C-3 `GAP=0 ANOMALY=0`.

## Limitaciones declaradas

- **Sin independencia epistemológica:** no está garantizada y está prohibido afirmarla; lo demostrado es disciplina adversarial con procedencia declarada (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md:6. Independence / Provenance`).
- **Q6 no observable:** no se demostró —ni puede demostrarse con la evidencia existente— que un Trial haya inducido una decisión humana; la decisión pertenece a la autoridad humana y se registra fuera del mecanismo.
- **Un solo modo ejercitado:** los cuatro Trials usaron el modo `viability`; el modo `comparative` está especificado y no ejercitado.
- **Ramas de degradación especificadas pero no ejercitadas exhaustivamente** (§11 y §14 de la convención): `UNDETERMINED`, `LIMIT`, `NO_VALUE`, `FAILURE`, perspectiva única y fallo de ejecutor.
- **Sin datos de costo:** no hay instrumentación de tokens, tiempo ni contexto; las métricas están fuera de alcance.
- **Ejecución manual y declarativa:** la condición de compromiso y la independencia se sostienen por declaración registrada, no por evidencia técnica; el aislamiento técnico está prohibido.
- **Sin enforcement y sin garantía de corrección:** el veredicto es evidencia atribuida, no verificación de la candidata; el mecanismo no decide ni cambia estado.
- **Cuatro Trials con el mismo patrón de resultado** (el ataque prevaleció sobre la conclusión de una sola pasada): compatible tanto con refutación genuina como con asimetría adversarial bajo un mismo ejecutor sintetizador; cuatro Trials no permiten distinguirlas.

## Decisión humana — fuera del mecanismo

**Tomada por el mantenedor y registrada como acto humano separado (2026-09-12).**

- **Fecha:** 2026-09-12.
- **Actor:** mantenedor (autoridad de decisión DEV). **Autoridad:** DECISION humana; no del mecanismo, no de un checker y no del agente.
- **Decisión:** **`JURY_TRIAL_DEV_FEATURE_CLOSED = TRUE`** — la feature DEV `Adversarial Deliberation` queda adoptada y su predicate de cierre queda satisfecho, sobre la base de la decisión `DEFINITION-B = ACCEPTED` (D-1) y de las condiciones D-2…D-8 del prompt de Phase 5.
- **Base (evidencia):** este Plan (definición de la feature, contrato de adopción de 15 elementos, predicate C1–C8 con evidencia por condición), la sección 15 de registro y el banner de adopción de la convención, la fila de `docs/working/proposals/INDEX.md`, los Planes 114 y 116 como evidencia de la capacidad, y la validación canónica más los gates C-1/C-2/C-3.
- **Fundamento:** la definición de la feature, su contrato de adopción, sus límites, su evidencia y su predicate quedan persistidos; el `GAP-02` queda cerrado con el mínimo texto derivado de `PC-1`/`LC-1`; la capacidad permanece Working/no normativa sin crear mecanismo, autoridad, gate ni lifecycle state.
- **Distinción (obligatoria):** esta decisión humana **no** es el veredicto de ningún Trial, **no** es una recomendación advisory y **no** es una conclusión automática del mecanismo ni de un checker. `Verdict ≠ Recommendation ≠ Human Decision`.
- **Efecto downstream:** `Adversarial Deliberation` queda **disponible** como capability DEV (adoptada, no obligatoria); la convención sigue Working/no normativa sin cambio de lifecycle; este Plan pasa a `Executed` con condición derivada `Closed` (docs-only, sin release); el Protocol-native Jury Trial permanece FUTURE / NOT STARTED / OUT OF SCOPE. Las decisiones deliberadas de los Planes 114/116 (reconocimiento de `<PLAN-114>:F-1`/`F-2`, resolución de `<PLAN-114>:F-3`, release de `11.1.0`/`11.2.0`) permanecen pendientes con owner y son independientes de esta decisión.

## Verificación C1–C8

Registrada antes de cerrar este Plan (Phase 5, paso 8). Ninguna condición se marca verdadera por apariencia: cada una cita evidencia concreta.

| Predicate | Requirement | Evidence | Status |
| --- | --- | --- | --- |
| C1 | contrato de adopción persistido y autorizado por el mantenedor | `## Contrato de adopción de la feature DEV` (15 elementos) + `## Definición final de la feature DEV` + `## Creación` (H1 = GO; D-1…D-8) + fila del Plan 117 en `docs/plans/INDEX.md` | **TRUE** |
| C2 | procedimiento especificado y reutilizable en la convención | `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` §2–§13 (invocación, marco, pasadas, compromiso, procedencia, confrontación, síntesis, veredicto, recomendación, terminación) + cuatro registros en los Planes 114/116 con los doce campos de §5 y la base declarada de §9 | **TRUE** |
| C3 | record home y regla de contenedor especificados (`GAP-02` cerrado) | convención `15. Record / Registration (record home)`, derivada de `PC-1` (artifact que posee la decisión) y `LC-1` (post-close por referencia), con restricción de contenedores de lineage; sin schema, registry, ID, plantilla, entidad `Trial` ni lifecycle | **TRUE** |
| C4 | frontera de autoridad especificada y sin cambios | convención `12. Authority Boundary` + contrato elemento 7 + `Verdict ≠ Recommendation ≠ Human Decision` declarado en los cuatro registros y en la decisión humana de este Plan; contractual/documental, sin enforcement | **TRUE** |
| C5 | la capacidad permanece Working/no normativa y no existe mecanismo nuevo | banner de adopción de la convención; fila descriptiva en `docs/working/proposals/INDEX.md`; change surface = cinco paths `docs/`; sin cambios en `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `ROADMAP.md`, `AGENTS.md`, plantillas, `docs/CONVENTIONS.md` ni `docs/VERSIONING.md` | **TRUE** |
| C6 | discoverability y standing adoptado explícitos | banner de la convención (`ADOPTED + WORKING + NON-NORMATIVE`) + fila de `docs/working/proposals/INDEX.md` + contrato elemento 12 (discovery documental, sin routing operacional) | **TRUE** |
| C7 | evidencia y limitaciones declaradas y acotadas | `## Evidencia` + `## Limitaciones declaradas` + contrato elementos 8, 9 y 13 (sin independencia epistemológica, sin Q6, sin métricas, sin costo) | **TRUE** |
| C8 | cambio materializador validado y acto humano de cierre registrado | `## Validation anchor` (A1 más el registro de la segunda validación) + `## Checkpoint / cierre` + `## Decisión humana — fuera del mecanismo` | **TRUE** |

Resultado: `JURY_TRIAL_CLOSED` (precondition, MVP del Plan 116) ∧ C1 ∧ C2 ∧ C3 ∧ C4 ∧ C5 ∧ C6 ∧ C7 ∧ C8 ⇒ **`JURY_TRIAL_DEV_FEATURE_CLOSED = TRUE`**.

## Criterios de salida

- [x] 1. El contrato de adopción, la definición de la feature y el predicate `JURY_TRIAL_DEV_FEATURE_CLOSED` quedan persistidos en este Plan.
- [x] 2. El `GAP-02` queda cerrado en la convención con el mínimo texto, derivado de `PC-1`/`LC-1` y sin crear schema, plantilla, registry, ID, entidad `Trial` ni lifecycle.
- [x] 3. El banner de la convención declara `ADOPTED + WORKING + NON-NORMATIVE` sin cambiar su lifecycle state ni volverla normativa.
- [x] 4. `docs/working/proposals/INDEX.md` refleja descriptivamente el standing adoptado, sin nuevo lifecycle state.
- [x] 5. `docs/plans/INDEX.md` registra este Plan (fila + serie) y `CHANGELOG.md` el ítem `[Unreleased]`.
- [x] 6. La tabla C1–C8 queda verificada con evidencia concreta por condición.
- [x] 7. La batería canónica pasa y los gates C-1/C-2/C-3 se clasifican para este Plan; `git diff --check` limpio; change surface contenido.
- [x] 8. El acto humano de cierre queda registrado como decisión separada, con actor, fecha, opción, base y efecto downstream.
- [x] 9. Sin code, sin arquitectura nueva, sin mecanismo nuevo, sin routing operacional, sin cambio de Protocol, sin `VERSION` bump, sin tag y sin dogfood adicional.
- [x] 10. `JURY_TRIAL_DEV_FEATURE_CLOSED` derivado de C1–C8 (no declarado arbitrariamente).

## Verificación

Batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (comandos exactos en los pasos 7–9) + gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + juicios manuales de conformidad del contrato de adopción con la convención + `git diff --check`, `git status --short --branch` y `git diff --stat` contenidos en el change surface declarado. `tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por diseño; no se ejecuta como gate de este Plan.

## Validation anchor

Registrado al validar el Plan 117 (2026-09-12). La validación **A1** corrió sobre el estado de contenido del cambio materializador (los cinco paths del change surface, antes de agregar esta sección y el `## Checkpoint / cierre`) — anti-circularidad; precedente Planes 96–116.

- Declared scope: los cinco paths del change surface — `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` (sección 15 de registro y banner de adopción), `docs/working/proposals/INDEX.md` (fila de la convención), `docs/plans/117-adversarial-deliberation-feature-adoption.md` (nuevo), `docs/plans/INDEX.md` (fila y serie) y `CHANGELOG.md` (ítem `[Unreleased]`) — más la batería canónica del repo y los gates C-1/C-2/C-3 sobre ese scope.
- Validation command-set: los 7 comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` más `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3), más `git diff --check` y `git status --short --branch`.
- Effective inputs (repo content): contenido completo del repo en el estado validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`, `runtime/` y la raíz; `pytest` consume `tests/`, `tools/` y `runtime/`); representado por la State identity (tree id).
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en esta ejecución; el consumo por comando se observa en la documentación de cada checker).
- Environmental factors: Windows + OneDrive; Python 3.14.3 con pytest 9.0.3; git 2.55.0.windows.5; git advierte normalización LF→CRLF en los archivos nuevos; `protocol/.agents/VERSION` = `11.2.0` (sin tag, esperado en `dev`); sin red. **Adaptación ambiental declarada:** bajo la política de archivos del sandbox los directorios temporales de pytest no son enumerables (`PermissionError [WinError 5]`), por lo que la pierna `pytest` se ejecutó con `--basetemp=.pytest-basetemp-117 -p no:cacheprovider`; la clase es preexistente al cambio y no produce fallos nuevos (idéntica al baseline documentado del Plan 116: `1 failed, 130 passed, 404 errors`, con los dos tests content-sensitive del repo en verde).
- Scoped Content Identity:
  - State identity (estado validado de A1 = index staged del change surface): T1 = `56e4407f2058a8c38a289bff6ff21acc73426856` (calculado con `git write-tree` sobre el estado staged).
  - Delta scoped identity (scope S = los cinco paths del change surface, ordenados; serialización `scoped-v1` más pares `path NUL blob NUL`): `f725d0c0fab65dd45a9f940090390167de8e6fc74a287a1a931687945b29ea8e` (generado con `tools/scoped_content_identity.py` sobre los cinco paths).
- Validity / stale: `vigente` (A1 sobre el estado de contenido); el cierre se apoya además en el registro de la segunda validación que sigue.

**A1 — resultados observados (estado de contenido, tree `56e4407f…`):**

| Comando | Resultado |
|---|---|
| `check_protocol_invariants.py --payload protocol .` | **PASS** — "Protocol invariants OK: 213 files checked, 9948 references verified" |
| `check_plan_citations.py` | **PASS** — "All citations resolve: no broken ruta:sección citations found" |
| `check_plan_structure.py` | **PASS** — "All numbered documents conform: no structural violations found" |
| `check_taxonomy_coherence.py` | **PASS** — "Taxonomy coherence OK" |
| `check_session_artifacts.py` | **PASS** — "Session artifacts OK" |
| `check_version_state.py` | **PASS** — "Version state OK" (warnings de secciones de changelog sin tag: esperados en `dev`) |
| `pytest tests/` (adaptado) | **clase ambiental** — `1 failed, 130 passed, 404 errors`, con `PermissionError [WinError 5]` en directorios temporales del sandbox; **idéntica al baseline pre-cambio**; los dos tests content-sensitive del repo (dogfooding real del checker de lineage y estructura real del repo) **2 passed** |
| C-1 (`check_lifecycle_anchor.py`) | Plan 117 `GAP` **esperado en A1** (anchor aún sin registrar — esta misma sección); resto del corpus sin cambios: `EXCLUDED=94, VALID=21, GAP=2 (planes 115 y 117), ANOMALY=0` |
| C-3 (`check_lifecycle_lineage.py`) | Plan 117 `N/A` — ausencia declarada de registros de lineage; `117 plans inspected; EXCLUDED=96, BOUNDARY=0, N/A=16, VALID=5, GAP=0, ANOMALY=0` |
| C-2 (`check_lifecycle_checkpoint.py`) | Plan 117 `GAP` **esperado en A1** (checkpoint aún sin registrar); `EXCLUDED=94, VALID=20, GAP=3 (planes 115, 116 y 117), ANOMALY=0` |
| `git diff --check` | limpio |

**A2 — segunda validación sobre el estado staged del cambio materializador (estado de cierre del Plan):** ejecutada con la misma command-set sobre el estado que incluye este `## Validation anchor`, el `## Checkpoint / cierre`, la nota de ejecución, el resultado final, la tabla C1–C8, el registro de la decisión humana y la fila del Plan 117 actualizada en `docs/plans/INDEX.md`; resultado: los 6 checkers canónicos **PASS**, C-1 Plan 117 **`VALID`**, C-2 Plan 117 **`VALID`**, C-3 Plan 117 **`N/A`** (ausencia declarada de registros de lineage, con `GAP=0` y `ANOMALY=0`), los dos tests content-sensitive **`2 passed`** y la pierna `pytest` con la misma clase ambiental del baseline sin fallos nuevos (`1 failed, 130 passed, 404 errors`). La State identity de A2 se computa con `git write-tree` sobre el estado staged de esta validación; su valor no se embebe por auto-referencia (precedente Planes 114/116) y es verificable tras el commit.

## Checkpoint / cierre

- Commits de cierre: commit atómico de cierre de este Plan en `dev` — `feat(dev): adopt adversarial deliberation as a reusable DEV capability (plan 117)`; su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable en `git log` tras el commit). Base del cambio: `9f70ad0` (plan 116, cierre del MVP DEV). Sin commits adicionales, sin amend, sin merge, sin rebase, sin push, sin tag.
- Estado validado (ref al Validation anchor): **A1** sobre el estado de contenido (tree `56e4407f…`) más el registro de la segunda validación sobre el estado staged de cierre.
- Estado de cierre (tree id): el árbol del commit de cierre es `git rev-parse HEAD^{tree}` tras el commit, no embebido por auto-referencia.
- Consistencia checkpoint↔anchor: **PASS** (GC-1). El registro de la segunda validación declarado en el `## Validation anchor` cubre el estado staged de cierre: los 6 checkers canónicos PASS, C-1 Plan 117 `VALID`, C-2 Plan 117 `VALID`, C-3 `N/A` (ausencia declarada, con `GAP=0` y `ANOMALY=0`), los dos tests content-sensitive `2 passed` y la pierna `pytest` con la clase ambiental preexistente sin fallos nuevos.
- Governance aplicada: Plan `Executed` (header y espejo en `docs/plans/INDEX.md`); ítem `(plan 117, —)` en `CHANGELOG.md:[Unreleased]`; sección 15 de registro y banner de adopción en la convención; fila de `docs/working/proposals/INDEX.md` con el standing adoptado (descriptivo, sin lifecycle state nuevo); decisión humana de cierre como acto separado; sin RFC/ADR nuevo; sin `VERSION` bump (permanece `11.2.0`) ni tag (RFC-69).
- Condición derivada: **`Closed` (docs-only, sin release)** — `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia PASS ∧ evidencia PASS para el estado de cierre ∧ acto humano de cierre registrado ∧ commit atómico de cierre. `Executed ≠ Committed ≠ Closed ≠ Released`; ni `Promoted` ni `Released`. Residuo declarado no bloqueante y **ajeno a este cierre**: la discrepancia de C-2 del Plan 116 permanece clasificada como MVP ARTIFACT HYGIENE (no se modifica, no se reabre y no se resuelve aquí).

## Findings / Correcciones / Pending

Registros reales de este artifact (las reglas del Incremento 2 aplican a artifacts nuevos; la ausencia de registros no es invalidez).

### Findings

- `No findings detected / N/A` (no se fabrican findings sintéticos).

### Correcciones

- `N/A` (ninguna corrección en esta iteración).

### Pending decisions

- `N/A` (ninguna decisión pendiente bloqueante de este Plan; las decisiones deliberadas de los Planes 114/116 permanecen en sus artifacts dueños y no forman parte de este cierre).

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Convertir la adopción en normativa u obligatoria | El contrato la declara `available`, no `required`; el banner y la fila del INDEX la declaran Working/no normativa; no se toca `.agents/`, `ROADMAP.md` ni `AGENTS.md` |
| Crear un lifecycle state `adopted` | Prohibido: el standing se registra descriptivamente; `docs/AGENTS.md:Lifecycle` no se modifica |
| Introducir arquitectura alrededor de la capacidad | Change surface limitado a 5 paths documentales; `git diff --stat` verificado antes del commit |
| Que el registro de un Trial colisione con los checkers de lifecycle | La sección de registro de la convención fija la restricción de contenedores; el contenedor de lineage real de este Plan es `## Findings / Correcciones / Pending` |
| Citas `ruta:sección` que no resuelven | `check_plan_citations.py` en la validación; solo se citan encabezados verificados |
| Confundir el predicate del MVP con el de la feature | La relación se declara explícitamente: `JURY_TRIAL_CLOSED` es precondition y nunca sustituto |
| Absorber la discrepancia de C-2 del Plan 116 en este cierre | Se clasifica como MVP ARTIFACT HYGIENE, ajena a este Plan; el Plan 116 no se modifica, no se reabre y su finding no se resuelve aquí |
| Deriva de alcance (Protocol, tooling, gobernanza) | `## Alcance` + criterios de salida + verificación del change surface |

## Trazabilidad

Phase 3 (DEV Jury Trial Feature Completion Analysis: MVP `CLOSED`, feature no cerrada, `GAP-01` decisión de definición, `GAP-02` record-home) → Phase 4 (DEV Jury Trial Feature Adoption Specification: `DEFINITION-B` aceptada, contrato de adopción, predicate C1–C8) → **este Plan** → definición final + contrato de adopción + predicate + registros (convención, INDEX de propuestas, INDEX de planes, changelog) → validación (batería + C-1/C-2/C-3) → decisión humana de cierre → `JURY_TRIAL_DEV_FEATURE_CLOSED`.

Referencias verificables usadas: `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`; `docs/working/proposals/INDEX.md`; `docs/plans/114-adversarial-deliberation-mvp.md` (`:Findings / Correcciones / Pending`, `:Validation anchor`, `:Checkpoint / Closure`, `:Resultado final del Plan`); `docs/plans/116-adversarial-deliberation-mvp-closure.md` (`:Resultado final del Plan`, `:Checkpoint / cierre`, `:Pending decisions`); `docs/CONVENTIONS.md` (`:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`, `:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`); `docs/AGENTS.md` (`:Lifecycle`, `:INDEX y CONVENTIONS`); `.agents/policies/authority.md:Authority classes`; `docs/VERSIONING.md:4.1 Batería canónica de verificación`.

## Nota de ejecución

**2026-09-12 — ejecución del Plan 117 (H1 = GO, decisiones D-1…D-8 del prompt de Phase 5).**

- **Intake y baseline:** `dev` @ `9f70ad0` (HEAD confirmado); working tree limpio salvo `.codegraph/` (untracked preexistente) y directorios de pytest del sandbox; Planes 114/116 `Executed` con condición derivada `Closed`; `protocol/.agents/VERSION` = `11.2.0` (sin tag); siguiente número libre verificado (117) y ausencia de artifact equivalente. Batería baseline: los 6 checkers PASS; la pierna `pytest` presentaba **antes de este cambio** la clase ambiental de permisos del sandbox (`1 failed, 130 passed, 404 errors`), clasificada como ambiental y no como regresión.
- **Pasos 1–2 (baseline y GO):** H1 = GO y D-1…D-8 registrados en `## Creación`; `**Status:**` fijado en `Aprobado para ejecución`; Plan registrado en `docs/plans/INDEX.md` (fila y serie Cuadragésima novena) en el mismo commit.
- **Paso 3 (`GAP-02`):** agregada a la convención la sección `15. Record / Registration (record home)` — el registro pertenece al artifact que posee la decisión (`PC-1`); si ese artifact está cerrado, se asienta en un artifact nuevo que lo referencia (`LC-1`, post-close por referencia); el cerrado no se reabre; no se crea un artifact únicamente para alojar un Trial; prohibición de ocupar o usar como encabezado los contenedores de lineage. Sin schema, plantilla, registry, ID, entidad `Trial` ni lifecycle.
- **Pasos 4–5 (definición, contrato, predicate, evidencia y límites):** persistidos en este Plan la definición final de la feature, el contrato de adopción de 15 elementos, el predicate `JURY_TRIAL_DEV_FEATURE_CLOSED` con C1–C8 y su relación explícita con el predicate del MVP (precondition, nunca sustituto), la evidencia de los cuatro Trials y las limitaciones declaradas (sin independencia epistemológica, sin Q6, sin métricas, sin costo).
- **Paso 6 (registros):** banner de la convención, `docs/working/proposals/INDEX.md`, `docs/plans/INDEX.md` y `CHANGELOG.md:[Unreleased]` actualizados.
- **Pasos 7–8 (validación y verificación):** A1 sobre el estado de contenido (tree `56e4407f…`, delta `f725d0c0…`) y segunda validación sobre el estado staged de cierre; tabla C1–C8 verificada con evidencia concreta por condición.
- **Paso 9 (cierre):** `## Validation anchor` (VC-1) y `## Checkpoint / cierre` (GC-1) completados; acto humano de cierre registrado como decisión separada; condición derivada `Closed` (docs-only, sin release).
- **Paso 10 (commit):** `git diff` y `git status` revisados; change surface = los cinco paths declarados; sin cambios en `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `ROADMAP.md`, `AGENTS.md`, plantillas, `docs/CONVENTIONS.md` ni `docs/VERSIONING.md`; commit atómico en `dev` con el mensaje `feat(dev): adopt adversarial deliberation as a reusable DEV capability (plan 117)`; sin `VERSION` bump, sin tag, sin push.
- **Desviaciones declaradas:** (i) adaptación ambiental de la pierna `pytest` (`--basetemp` y `-p no:cacheprovider`) por la clase preexistente de permisos del sandbox, declarada en el `## Validation anchor`; (ii) `tools/check_dist_sync.py` no ejecutado (rojo esperado en `dev` por diseño; sin release).
- **Resultado:** ver `## Resultado final del Plan`.

## Resultado final del Plan

### `ADVERSARIAL DELIBERATION (DEV) — ADOPTED — JURY_TRIAL_DEV_FEATURE_CLOSED = TRUE`

**Fundamento — derivado de la evidencia registrada, no elegido previamente.**

- **Adopción materializada:** definición final de la feature, contrato de adopción de 15 elementos y predicate `JURY_TRIAL_DEV_FEATURE_CLOSED` (C1–C8) persistidos en este Plan; `GAP-02` cerrado en la convención con el mínimo texto derivado de `PC-1`/`LC-1`; standing `ADOPTED + WORKING + NON-NORMATIVE` declarado en el banner de la convención y en la fila de `docs/working/proposals/INDEX.md`, sin lifecycle state nuevo.
- **C1–C8 verificados con evidencia** (ver `## Verificación C1–C8`): el predicate se **deriva**, no se declara. `JURY_TRIAL_CLOSED` (MVP, Plan 116) permanece únicamente como precondition y no se reutiliza como sustituto del predicate de la feature.
- **Naturaleza preservada:** la capacidad queda **disponible**, nunca obligatoria; no se creó código, tool, checker, registry, state machine, entidad `Trial`, ID global, capa de persistencia, plantilla, telemetría, métrica, routing operacional, integración al Change Lifecycle, enforcement ni aislamiento; el change surface son cinco paths `docs/`.
- **Sin release:** cambio docs-only (RFC-69): sin `VERSION` bump (permanece `11.2.0`) ni tag; `Executed ≠ Committed ≠ Closed ≠ Released`.
- **Autoridad intacta:** la decisión humana de cierre se registró como acto separado (`Verdict ≠ Recommendation ≠ Human Decision`); ningún veredicto de Trial se convirtió en autoridad; las decisiones deliberadas de los Planes 114/116 permanecen pendientes con owner y son independientes de este cierre.
- **Fuera de este cierre (declarado, no iniciado):** el Protocol-native Jury Trial — FUTURE / NOT STARTED / OUT OF SCOPE; la discrepancia de C-2 del Plan 116 (MVP ARTIFACT HYGIENE); y el resto de pendientes ajenos al alcance de este Plan.
