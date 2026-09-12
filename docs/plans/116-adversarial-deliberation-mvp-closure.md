# Plan 116 — Cierre del MVP de deliberación adversarial DEV (Adversarial Deliberation MVP Closure)

**Status:** Executed (2026-09-12; los 12 criterios de salida satisfechos) — condición derivada **`Closed` (docs-only, sin release)** materializada por la aceptación del mantenedor (decisión humana D-1, 2026-09-12: `ACCEPT CLOSURE OF THE DEV ADVERSARIAL DELIBERATION MVP`) y el commit atómico de cierre de este Plan (identificable por el mensaje `feat(dev): close adversarial deliberation MVP (plan 116)`; auto-referencia: el árbol no embebe su propia identidad). Ver `## Checkpoint / cierre` y `## Nota de ejecución`.
**Fecha:** 2026-09-12
**RFC:** —
**Clase:** — (sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Change Level:** L2 (`max(coordination=2, scope=1, architectural=0, release=0, duration=1)`: el Escenario A usa un segundo ejecutor de deliberación (subagente) como productor de contenido; la superficie del cambio es un área documental (`docs/`), sin impacto arquitectónico ni de release)
**Depende de:** Plan 114 (`Closed`) — la convención y el primer Trial son la base normativa del experimento
**Origen:** decisiones humanas D-1/D-2 del prompt de Phase 2 (2026-09-12; cierre del Adversarial Deliberation MVP DEV); análisis de cierre de Phase 1 (predicates A–I); `docs/plans/114-adversarial-deliberation-mvp.md` (`Closed`, 2026-09-09)

## Creación

**H1 = GO** otorgado por el mantenedor mediante las decisiones D-1/D-2 del prompt de Phase 2 (2026-09-12), que autorizan exclusivamente: (i) cerrar el **Adversarial Deliberation MVP** del entorno DEV en su forma materializada actual (Working Convention + registros embebidos + lifecycle documental existente), sin promoción a gobernanza, sin mecanismo Protocol-native y sin nueva arquitectura; y (ii) ejecutar los **tres escenarios de dogfood** (A: decisión real con ejecutores diferenciados y decisión humana observable; B: resultado legítimo NO CHANGE; C: camino no canónico, confrontacional o de degradación).

Alcance de la autorización: no aprueba ninguna feature del Protocol; no inicia el desarrollo Protocol-native; no convierte el veredicto de ninguna deliberación en autorización; no delega la autoridad humana de decisión.

## Objetivo

Ejecutar el dogfood final del MVP de deliberación adversarial de DEV (escenarios A/B/C sobre decisiones reales y verificables del repositorio), registrar cada deliberación conforme a `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`, registrar las decisiones humanas como actos separados (o escaladas con owner cuando no estén disponibles), validar con la batería canónica y los gates de lifecycle existentes, y evaluar el closure predicate `JURY_TRIAL_CLOSED = A ∧ B ∧ C ∧ D ∧ E ∧ F ∧ G ∧ H ∧ I` establecido en el análisis de Phase 1, proponiendo el estado final del MVP sin afirmar nada sobre una futura feature Protocol-native.

## Alcance

**Dentro del alcance:** este Plan; los registros de los Tres Trials (A/B/C) embebidos en este Plan; los registros de decisiones humanas (acto separado o pendiente escalada); el banner de estado de la convención; `docs/working/proposals/INDEX.md`; `docs/plans/INDEX.md` (fila + serie de este Plan); `CHANGELOG.md:[Unreleased]` (ítem `(plan 116, —)`); la mecánica de lifecycle documental existente (Validation anchor, checkpoint, findings/corrections/pending).

**Fuera del alcance:** `protocol/` (incluido `protocol/.agents/`, `protocol/.agents/VERSION`); `runtime/`; `tools/`; `tests/`; `.agents/`; plantillas; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; RFCs; ADRs; `master`; tags; `dist/`; state machines; registries; identities nuevas; skills; workers; capabilities runtime; Change Governance Artifact; Change Lifecycle del Protocol; aislamiento multi-agent; votación; métricas de costo; sandboxing; release del Protocol.

## Criterio de entrada

- [x] Repositorio en `dev`, HEAD confirmado (`git rev-parse HEAD` = `b8c6ce0`), working tree sin cambios fuera de los preexistentes (`.codegraph/` untracked; ver Step 1).
- [x] Plan 114 `Executed` con condición derivada `Closed` (docs-only) — la convención y el primer Trial existen y están registrados.
- [x] `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` existe con sus 14 secciones y banner Working/no normativa.
- [x] Siguiente número libre confirmado en `docs/plans/INDEX.md` (116; último registrado: 115).
- [x] GO del mantenedor registrado en `## Creación` (H1, decisiones D-1/D-2).
- [x] `**Status:**` fijado exactamente en `Aprobado para ejecución`.
- [x] Batería canónica verde en el estado baseline (pre-cambio): los 6 checkers PASS; la pierna `pytest` presenta fallos ambientales de permisos del sandbox (documentados en la Nota de ejecución; no causados por este cambio).

## Entregables

1. `docs/plans/116-adversarial-deliberation-mvp-closure.md` — este Plan, con los registros de los Tres Trials y la evaluación del closure predicate.
2. `docs/plans/INDEX.md` — fila + serie (Cuadragésima octava) del Plan 116.
3. `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` — solo el banner de estado (resultado de la evaluación de cierre; sin cambios de cuerpo).
4. `docs/working/proposals/INDEX.md` — status de la convención actualizado.
5. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 116, —)`.

## Pasos

1. **Baseline e intake:** `git status --short --branch`, `git rev-parse HEAD`; registrar clasificación (RFC-56 clase —; Change Level L2; dominio DEV docs).
2. **GO:** verificar que D-1/D-2 (prompt de Phase 2) están registradas en `## Creación` y que el `Status` es `Aprobado para ejecución`.
3. **Escenario A** (`## Registro del Trial — Escenario A`): marco declarado; perspectiva `E-A` (agente principal, comprometida antes de revelación); perspectiva `E-B` producida por un **subagente de deliberación** sin acceso a la conclusión de `E-A` (ejecutores diferenciados; sin afirmación de independencia epistemológica); síntesis; veredicto; recomendación; registro de la decisión humana como acto separado o pendiente escalada.
4. **Escenario B** (`## Registro del Trial — Escenario B`): decisión cuyo resultado legítimo puede ser NO CHANGE; mismas reglas de registro; ejecutor único declarado (`ejecutores: mismo`).
5. **Escenario C** (`## Registro del Trial — Escenario C`): camino no canónico — confrontación acotada conforme a `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md:7. Optional Confrontation`; registro del comportamiento, lo que el mecanismo esperaba, lo que pudo y no pudo resolver, recuperación e intervención humana.
6. **Decisiones humanas:** registrar cada decisión como acto separado (fecha, actor, opción, fundamento, `Trial Verdict ≠ Recommendation ≠ Human Decision`) o como pendiente escalada con owner en `### Pending decisions` (PC-1). Nunca improvisar una decisión humana.
7. **Validación:** batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + gates C-1 y C-3; juicios manuales de conformidad de cada registro con la convención.
8. **Correcciones:** si aparecen findings, registrar `<PLAN-116>:F-<n>`/`C-<n>` (LC-1) y revalidar (A2) dentro del scope.
9. **Cierre:** completar `## Validation anchor` (VC-1) y `## Checkpoint / cierre` (GC-1); correr C-2; status `Executed`; condición derivada según el estado del commit del mantenedor (sin commit propio: el commit es acción del mantenedor — `.agents/workflows/change-lifecycle.md:9. Closure and handoff`).
10. **Documentación:** actualizar banner de la convención, `docs/working/proposals/INDEX.md`, `docs/plans/INDEX.md`, `CHANGELOG.md:[Unreleased]`.
11. **Evaluación final:** tabla A–I del closure predicate con evidencia por letra; propuesta `READY TO CLOSE` / `NOT READY TO CLOSE`; sección explícita sobre la feature Protocol-native (FUTURE / NOT STARTED / OUT OF SCOPE).

## Registro del Trial — Escenario A (Steps 3 y 6)

> **Este registro es contenido experimental del Plan 116.** No crea gobernanza, no posee autoridad y no convierte el veredicto en decisión: la resolución formal de los findings deliberados pertenece a la autoridad humana (owner: mantenedor).

### Marco declarado

| Elemento | Valor |
|---|---|
| Problema / cuestión (referencia) | Reconocimiento formal de los findings `<PLAN-114>:F-1` y `<PLAN-114>:F-2`, registrados en estado `partially-resolved` con la nota "la resolución formal del finding corresponde a la autoridad humana (owner: mantenedor)" (`docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending`) |
| Candidata | `C-1` — reconocer formalmente a `<PLAN-114>:F-1` y `<PLAN-114>:F-2` como `resolved`, sobre la evidencia de las correcciones `<PLAN-114>:C-1`/`<PLAN-114>:C-2` y de la revalidación A2 del Plan 114 |
| Modo | `viability` |
| Criterios | `K-1` la corrección aplicada elimina la causa observada de cada finding · `K-2` la revalidación cubre el estado de cierre del Plan 114 · `K-3` no persiste riesgo material no cubierto por los registros · `K-4` el acto de reconocimiento respeta la frontera de autoridad: la resolución de findings es decisión humana con evidencia (AU-3; `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`) |
| Límites declarados | máximo 2 pasadas de evaluación; sin confrontación; una síntesis; ejecutores diferenciados: `E-A` (agente DEV principal) y `E-B` (subagente de deliberación, contexto separado) |
| Motivo de invocación | Escenario A del dogfood de cierre autorizado por D-2: decisión DEV real, con alternativas materiales (reconocer / mantener `partially-resolved` / exigir evidencia nueva) y con dueño claro (mantenedor) |

### Perspectiva E-A — postura: sostener la viabilidad de `C-1`

- **Etiqueta local:** `E-A`.
- **Ejecutor:** agente DEV (sesión principal de ejecución del Plan 116).
- **Material recibido:** registro de findings del Plan 114 (`docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending`); regla operacional de findings (`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`); modelo de autoridad (`docs/adr/16-change-lifecycle-authority.md:Decisión`, `docs/adr/16-change-lifecycle-authority.md:Invariantes`); anchor y checkpoint del Plan 114 (`docs/plans/114-adversarial-deliberation-mvp.md:Validation anchor`, `docs/plans/114-adversarial-deliberation-mvp.md:Checkpoint / Closure`); política operacional de cierre (`.agents/policies/validation-closure.md:4. Findings / corrections / revalidation lineage (LC-1)`).
- **Material compartido:** encuadre, criterios `K-1..K-4` y el material común anterior.
- **Relación con conclusiones previas:** ninguna (primera pasada del Trial).
- **Condición de compromiso:** conclusión registrada antes de que `E-B` conociera conclusión alguna; el registro de `E-A` queda escrito en este Plan **antes** de despachar al ejecutor de `E-B`.
- **Conclusión:** **VIABLE** — reconocer formalmente `F-1` y `F-2` como `resolved` es viable con la evidencia existente, **siempre que** el reconocimiento sea un acto de la autoridad humana y no del mecanismo.
- **Razones por criterio:**
  - `K-1` **a favor.** `F-1` (4 citas rotas a `docs/adr/16-change-lifecycle-authority.md`) fue corregido por `<PLAN-114>:C-1` (repunte a `:Decisión`, punto 3) y `check_plan_citations.py` PASS en V2 y A2. `F-2` (registros de lineage no parseables, `GAP=1`) fue corregido por `<PLAN-114>:C-2` (forma canónica `F-<n>`/`C-<n>`, primer dígito 1–9) y `tools/check_lifecycle_lineage.py` reporta `VALID`, `GAP=0`, `ANOMALY=0` para el Plan 114. La causa observada de cada finding quedó eliminada, con evidencia de checker.
  - `K-2` **a favor.** La revalidación **A2** se ejecutó sobre el estado que incluye los registros de cierre (checkers PASS; `python -m pytest tests/` canónico `524 passed`), declarado en `docs/plans/114-adversarial-deliberation-mvp.md:Validation anchor`. El Plan 114 declara la consistencia checkpoint↔anchor contra **A2** (C-2 `VALID`, GC-1) en `docs/plans/114-adversarial-deliberation-mvp.md:Checkpoint / Closure`.
  - `K-3` **a favor, con reserva registrada.** El riesgo residual detectado (`F-3`: el ejemplo `F-01`/`C-01` de `docs/plans/_TEMPLATE.md` frente al contrato del checker C-3) vive en el registro de `F-3` (estado `deferred`, owner: mantenedor), no en `F-1`/`F-2`. Reconocer `F-1`/`F-2` no debilita ni cierra la trazabilidad de `F-3`; la reserva es que la causa raíz de `F-2` sigue abierta como `F-3`, y un reconocimiento de `F-2` debe citar esa dependencia para no sugerir que la causa raíz desapareció.
  - `K-4` **a favor de la candidata como recomendación; en contra como acto del mecanismo.** La resolución de un finding es decisión humana con evidencia (CL-8; AU-3); el Trial no puede ejecutar el reconocimiento. La candidata es viable exactamente como **recomendación a la autoridad**, nunca como acto del agente o del mecanismo.
- **Premisas:** (P1) `resolved` no borra historia: los elementos inmutables del finding se preservan y la resolución conserva evidencia (`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`); (P2) la reapertura es posible si el reconocimiento resultara incorrecto (finding nuevo que referencia al original o metadata `reopened`); (P3) las correcciones `C-1`/`C-2` son registros FACTUAL/TRACEABILITY aplicados dentro del change surface autorizado del Plan 114.
- **Supuestos:** que la A2 registrada es aplicable al estado de cierre del Plan 114 (el propio Plan 114 declara C-2 `VALID` con `A2 (declared)`); que el mantenedor no exige una revalidación nueva sobre el HEAD actual de `dev`.
- **Incertidumbres:** si el mantenedor prefiere reconocer cada finding por separado; si el estado del HEAD actual de `dev` (posterior a R3 del Plan 114, con los Planes 115 y 116 en vuelo) exige una revalidación adicional antes de reconocer.

### Perspectiva E-B — postura: atacar `C-1`

*(Registro producido por el ejecutor E-B — subagente de deliberación — y transcrito sin edición. Declaración de procedencia del ejecutor incluida tal cual.)*

- **Etiqueta local:** E-B
- **Ejecutor:** subagente de deliberación (sesión/contexto separado del agente principal; sin acceso a la conclusión de E-A). Declaración de procedencia: no recibió, no buscó y no intentó reconstruir la conclusión de E-A. Un grep transversal sobre `docs/` arrojó coincidencias incidentales en `docs/plans/116-adversarial-deliberation-mvp-closure.md` (el marco declarado de este Trial y una línea sobre F-3/el template); **no** abrió el registro de evaluaciones de ese documento y ninguna conclusión de su pasada se funda en ese contenido — los hechos equivalentes se citan desde el propio Plan 114.
- **Material recibido:** `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` completo (en particular §5, §6, §8, §9, §12, §13, §14); `docs/plans/114-adversarial-deliberation-mvp.md` completo (577 líneas: `## Status`, `## Validation anchor` filas A1/A2, `## Checkpoint / Closure`, `## Findings / Correcciones / Pending`, `## Nota de ejecución`, `## Resultado final del Plan`); `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)` y `:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`; `docs/adr/16-change-lifecycle-authority.md:Decisión` y `:Invariantes` (AU-1…AU-7); `.agents/policies/validation-closure.md` (§3 Revalidation (A2), §4 Findings/corrections/revalidation lineage (LC-1), §5 Checkpoint (GC-1)); `.agents/AGENTS.md` (reglas operativas fundamentales 1–10); `docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation`; `git log --oneline -8` (verificación de la historia declarada: A `eecb62e`, C1 `4f6a3a4`, C2 `7434167`, R2 `e7008fd`, R3 `e30f979` — coincide con el Plan 114); grep transversal en `docs/` por `<PLAN-114>:F-1`/`<PLAN-114>:F-2`/`partially-resolved` (coincidencias incidentales en el Plan 116 declaradas arriba; sin registro de resolución de F-1/F-2 fuera del propio Plan 114).
- **Material compartido:** encuadre, criterios `K-1..K-4` y el material común anterior.
- **Relación con conclusiones previas:** ninguna (no recibió la conclusión de E-A).
- **Condición de compromiso:** conclusión registrada antes de la revelación de la conclusión de E-A.
- **Conclusión:** **NOT_VIABLE** — C-1, tal como está enunciada, no sobrevive al ataque. El defecto no está en la autenticidad de la evidencia (las correcciones existen, A2 fue verde y la historia de commits coincide), sino en la forma del acto propuesto: no declara actor, no declara vía de registro, y para F-2 afirma una eliminación de causa que los propios registros desmienten a nivel de causa raíz.
- **Razones por criterio:**
  - **K-1 (la corrección elimina la causa observada).** Para F-1 el ataque no encuentra falla: la causa observada eran 4 citas a una sección inexistente (`:ADR-worthiness`), C-1 las repuntó a `:Decisión` y `check_plan_citations.py` quedó PASS en V2 y A2 (commit C2 `7434167`) — causa eliminada. Para F-2 la corrección C-2 eliminó la causa **a nivel de instancia** (los registros de lineage del Plan reescritos a la forma del contrato; checker `VALID`, `GAP=0`, `ANOMALY=0`; `524 passed` en A2), pero la propia observación de F-2 — que es inmutable (CL-8) — nombra como parte de la cadena causal el ejemplo del template: "la forma canónica del parser … no reconoce la numeración `F-01`/`C-01` **que ejemplifica `docs/plans/_TEMPLATE.md`**" (`docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending`), y el propio Plan registra que F-3 — ese ejemplo defectuoso del template — "**es la causa raíz de `<PLAN-114>`:F-2**" y queda "**no corregido**" (`:Nota de ejecución`; F-3 `deferred`, owner: mantenedor, templates fuera del change surface). Reconocer F-2 como `resolved` **sin calificación de alcance** afirma la eliminación de una causa que los registros declaran activa, y el vocabulario de estados no prevé un "resolved de instancia" (`docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation`). El escenario de recurrencia es concreto y falsificable: cualquier Plan futuro que copie el ejemplo del template reproduce el mismo `GAP=1`. K-1 falla para F-2 tal como C-1 está enunciada.
  - **K-2 (la revalidación cubre el estado de cierre).** Es fáctico que A2 cubrió el estado de cierre del Plan 114 — pero ese estado es exactamente aquel en el que F-1/F-2 figuran `partially-resolved` (`:Validation anchor`, fila A2; `:Checkpoint / Closure`: consistencia checkpoint↔anchor PASS contra A2). El reconocimiento es un cambio **posterior** a ese estado validado: ninguna validación cubre un estado en el que los findings lean `resolved`. Y la vía de registro está bloqueada en ambos cuernos: (a) editarlo en el contenedor del Plan 114 es modificar un artifact `Closed`, terminal (`.agents/AGENTS.md` reglas 5 y 9; la regla post-close: los cambios posteriores al cierre generan artifacts nuevos que referencian al cerrado); (b) registrarlo en un artifact nuevo por referencia deja el registro canónico del estado en `partially-resolved` (único lugar que el checker de lineage lee) y parte el estado en dos textos, sin validación que cubra el nuevo registro. Por tanto A2 no cubre el estado que C-1 produciría: K-2 no sostiene a C-1.
  - **K-3 (no persiste riesgo material no cubierto por los registros).** El riesgo material conocido — el template que enseña la forma no parseable — sí está cubierto por los registros (F-3, `deferred` con owner y destino: mantenedor; template + checker C-3). Pero C-1 introduce un riesgo que **ningún registro cubre**: la vía de registro del reconocimiento. El contenedor `### Pending decisions` del Plan 114 no contiene ninguna decisión pendiente sobre el reconocimiento de F-1/F-2 (solo las dos decisiones del mantenedor del 2026-09-09); LC-1 declara que la metadata de estado "puede evolucionar" pero no dice cómo evoluciona la de un finding cuyo artifact dueño está `Closed`; y la provisión post-close de RFC-75 (`:Mecanismo 8`) cubre correcciones, no la transición de resolución. El riesgo de terminar en (a) una edición no autorizada del artifact cerrado o (b) un registro partido con dos fuentes de verdad es real, concreto y no está cubierto por registro alguno. K-3 se satisface solo parcialmente.
  - **K-4 (el acto respeta la frontera de autoridad).** Es el criterio decisivo y C-1 no lo demuestra. La resolución de un finding es **decisión humana con evidencia**; el agente "detecta, registra, propone y escala, **no resuelve unilateralmente**" (`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`); "A finding's resolution … is a human decision with evidence" (`.agents/policies/validation-closure.md:4. Findings / corrections / revalidation lineage (LC-1)`); AU-3: sin auto-resolución por código (`docs/adr/16-change-lifecycle-authority.md:Invariantes`); y la propia convención prohíbe al mecanismo "resolver findings" (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md:12. Authority Boundary`). El Plan 114 lo registra dos veces: "la resolución formal del finding corresponde a la autoridad humana (owner: mantenedor)" (`:Findings / Correcciones / Pending`, F-1) y "su reconocimiento formal pertenece a la autoridad humana y **no se modifica unilateralmente**" (`:Nota de ejecución`). C-1 está enunciada como **acto** ("Reconocer formalmente… como `resolved`"), no como recomendación, y no declara actor. Bajo la lectura en que el mecanismo o el agente ejecuta el reconocimiento, C-1 viola directamente la frontera. Bajo la lectura caritativa (el humano decide con esa evidencia), el mecanismo solo puede evaluar y recomendar, y la decisión se registra fuera de él — con lo cual C-1 deja de ser un acto del Trial, y su enunciado no distingue entre ambas lecturas. En ninguna de las dos, tal como está enunciada, queda demostrado K-4.
- **Debilidades detectadas en una posición a favor de C-1:**
  1. Tratar `partially-resolved → resolved` como mera evolución de metadata ignora que el artifact dueño está `Closed` y que LC-1 no especifica cómo evoluciona la metadata de un finding en artifact cerrado: la premisa implícita "es solo cambiar una palabra" colisiona con la terminalidad (`.agents/AGENTS.md` regla 5; regla post-close).
  2. Tratar "la evidencia existe (C-1/C-2 + A2)" como suficiente para el reconocimiento ignora que A2 validó el estado **previo** al reconocimiento: la evidencia cubre las correcciones, no el acto de reconocer.
  3. Tratar la autoridad humana como algo que vuelve todo permisible ignora que el acto humano necesita un vehículo de registro que los registros no designan (el plan cerrado no puede hospedarlo; un artifact nuevo deja el registro canónico sin actualizar).
  4. Tratar la corrección de F-2 como completa ignora que el propio Plan registra la causa raíz (F-3) como no corregida: un `resolved` sin calificación contradice la observación original del finding, que es inmutable (CL-8).
- **Premisas:** (P1) la resolución de un finding es decisión humana con evidencia; el agente no resuelve unilateralmente — `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`; (P2) "A finding's resolution … is a human decision with evidence" — `.agents/policies/validation-closure.md:4. Findings / corrections / revalidation lineage (LC-1)`; (P3) AU-3: conflictos detectados y escalados al humano; sin auto-resolución por código — `docs/adr/16-change-lifecycle-authority.md:Invariantes`; (P4) el mecanismo no puede "resolver findings" ni cambiar el lifecycle — `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md:12. Authority Boundary`; (P5) F-1/F-2 registrados `partially-resolved`; F-1 lleva la nota "la resolución formal del finding corresponde a la autoridad humana (owner: mantenedor)"; la observación de F-2 cita el ejemplo de `docs/plans/_TEMPLATE.md`; F-3 `deferred` (owner: mantenedor) — `docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending`; (P6) F-3 "es la causa raíz de `<PLAN-114>`:F-2" y queda registrado, no corregido; "su reconocimiento formal pertenece a la autoridad humana y no se modifica unilateralmente" — `docs/plans/114-adversarial-deliberation-mvp.md:Nota de ejecución`; (P7) A2 cubrió el estado de cierre con los findings en `partially-resolved`; condición derivada `Closed`; residual declarado no bloqueante — `docs/plans/114-adversarial-deliberation-mvp.md:Validation anchor` y `:Checkpoint / Closure`; (P8) cambios posteriores al cierre generan artifacts nuevos que referencian al cerrado; el cerrado no se reabre — `docs/CONVENTIONS.md` (post-close) y `.agents/AGENTS.md` reglas 5 y 9; (P9) estados válidos de finding y semántica de `resolved` (sin calificadores de alcance) — `docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation`; (P10) historia de commits verificada en git: A `eecb62e`, C1 `4f6a3a4`, C2 `7434167`, R2 `e7008fd`, R3 `e30f979` (`git log --oneline -8`).
- **Supuestos:** que "reconocer formalmente como `resolved`" exige actualizar el campo de estado del contenedor de findings en el artifact dueño (único lugar que el checker de lineage lee); que C-1, tal como fue enunciada en el encuadre, no declara actor ni vía de registro (el ataque evalúa ambas lecturas — mecanismo/agente vs. humano — y ninguna queda demostrada por el enunciado); que los resultados registrados de A2 (checkers PASS; `python -m pytest tests/` `524 passed`) son fieles a lo ocurrido (no re-ejecutó la batería); que ningún artifact posterior ya registró un reconocimiento humano de F-1/F-2 (verificado por grep sobre `docs/`).
- **Incertidumbres:** si LC-1 ("la metadata de lifecycle … puede evolucionar") está pensada para permitir la evolución de estado de findings cuyo artifact dueño está `Closed`, y mediante qué artifact (el corpus normativo no lo dice explícitamente); si los checkers de lifecycle detectarían una edición in-place del contenedor de findings de un plan cerrado (no los ejecutó; la divergencia del tree del estado de cierre registrado sería verificable en git, pero no fue verificada por él); si el silencio del mantenedor del 2026-09-09 (decidió sobre `<PLAN-105>` y sobre la convención, pero no sobre F-1/F-2) implica diferimiento deliberado del reconocimiento; si el vocabulario de estados admite un `resolved` calificado como "de instancia" sin contradecir RFC-75 (hoy solo existe `resolved` sin calificadores).
- **Nota de honestidad del ataque (qué sobrevivió y qué probó):** la cadena factual de la candidata sobrevive — probó y no encontró falla en: la existencia y forma de C-1/C-2 (provenance, alcance de revalidación, carácter FACTUAL/TRACEABILITY, conforme a LC-1); la correspondencia entre la historia de commits declarada y git; la cobertura real de A2 sobre el estado de cierre; y K-1 para F-1 (causa eliminada y revalidada). Lo que no sobrevive es la forma del acto propuesto: actor no declarado (K-4), vía de registro bloqueada por la terminalidad del Plan 114 (K-2/K-3) y un `resolved` sin calificar para F-2 frente a una causa raíz registrada como activa (K-1).

### Síntesis

**Entradas consideradas:** `E-A` y `E-B` (ambas comprometidas antes de la revelación; ejecutores diferenciados: agente principal y subagente de deliberación — condición de procedencia necesaria, **no** independencia epistemológica). **Ninguna conclusión fue suprimida ni reescrita.**

**Convergencias (derivadas, con origen):**

- `S-1` — *la evidencia factual de las correcciones es sólida*: C-1/C-2 existen con provenance, la historia de commits coincide con git (A `eecb62e`, C1 `4f6a3a4`, C2 `7434167`, R2 `e7008fd`, R3 `e30f979`) y A2 cubrió el estado de cierre con checkers PASS y `524 passed`. Deriva de `docs/plans/114-adversarial-deliberation-mvp.md:Validation anchor` y `:Checkpoint / Closure` (asumida por ambas evaluaciones; `E-B` declara haberla probado sin encontrar falla).
- `S-2` — *el reconocimiento formal es decisión humana, no acto del mecanismo*: deriva de `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`, de `docs/adr/16-change-lifecycle-authority.md:Invariantes` (AU-3) y de la convención §12. `E-A` la registra como condición de su propio `VIABLE`; `E-B` la usa como criterio decisivo.
- `S-3` — *la causa raíz de F-2 (el ejemplo del template, F-3) permanece activa*: deriva de `docs/plans/114-adversarial-deliberation-mvp.md:Nota de ejecución` (F-3 "es la causa raíz de `<PLAN-114>`:F-2", no corregido). `E-A` la registra como reserva de `K-3`; `E-B` la convierte en fallo de `K-1` para un `resolved` sin calificación.

**Contradicciones identificadas (no adjudicadas):**

- `X-1` — **lectura de C-1**: `E-A` lee la candidata como recomendación a la autoridad (bajo esa lectura, `VIABLE`); `E-B` la lee como acto sin actor declarado (bajo esa lectura, `NOT_VIABLE`). La contradicción es sobre la forma del enunciado, no sobre los hechos; **no se adjudica**.
- `X-2` — **alcance de `resolved` para F-2**: `E-A` sostiene que la causa de instancia quedó eliminada y que el riesgo raíz vive en el registro de F-3; `E-B` sostiene que un `resolved` sin calificación afirma la eliminación de una causa que los registros declaran activa. **No se adjudica.**

**Dependencias y condiciones (derivadas):**

- `D-1` — la viabilidad del reconocimiento depende de (i) el actor (humano), (ii) la vía de registro (artifact nuevo post-close por referencia, dado que el Plan 114 está `Closed` y no se reabre — regla post-close), y (iii) la calificación del estado de F-2 respecto de F-3. Ninguna de las tres estaba en el enunciado de C-1.
- `D-2` — mientras no exista ese acto humano, el estado correcto y registrado de F-1/F-2 es `partially-resolved` (el que hoy figura en el artifact dueño).

**Desacuerdo preservado (explícito, sin adjudicar):** `X-1` y `X-2` quedan registrados a nivel de criterio; **no se resuelven por mayoría, por conteo ni por preferencia del sintetizador**.

**Sin contenido nuevo:** la síntesis no introdujo hechos externos, evidencia nueva ni argumentos materiales no fundados. Las condiciones `D-1`/`D-2` derivan de premisas presentes en ambas pasadas (P1–P10 de `E-B`; premisas de `E-A`). No fue necesaria ninguna pasada adicional: ningún argumento material nuevo exigió registrarse como nueva evaluación.

### Veredicto

| Campo | Valor |
|---|---|
| **Valor** | `NOT_VIABLE` — C-1, tal como está enunciada (acto de reconocimiento sin actor declarado, sin vía de registro y sin calificación de alcance), no es viable |
| **¿Hubo ataque?** | Sí (`E-B`) |
| **Ejecutores** | `distinto` — `E-A` producida por el agente DEV principal; `E-B` por un subagente de deliberación en contexto separado sin acceso a la conclusión de `E-A` (condición de procedencia; **no** se afirma independencia epistemológica: ambos ejecutores son agentes LLM del mismo entorno asistente) |
| **Material compartido** | encuadre, criterios `K-1..K-4`, registro de findings del Plan 114, regla operacional LC-1, ADR-16, política de cierre, convención |
| **Criterios** | declarados: `K-1..K-4` |
| **Qué quedó sin hacer** | sin confrontación (declarada opcional; este Escenario ejercita ejecutores diferenciados, la confrontación se ejercita en el Escenario C); sin participación humana como ejecutor; límite de 2 pasadas respetado |
| **Razones por criterio** | `K-1` satisfecho para F-1; **en disputa para F-2** (`X-2`: causa raíz F-3 activa) · `K-2` **no sostiene a C-1** (A2 valida el estado previo al reconocimiento; vía de registro bloqueada por la terminalidad del Plan 114) · `K-3` **parcial** (el riesgo de vía de registro no está cubierto) · `K-4` **no demostrado** (acto sin actor declarado; la resolución es decisión humana) |
| **Desacuerdo** | `X-1` y `X-2`, preservados sin adjudicar |
| **Relación con cada evaluación** | **coincide con `E-B`** (valor `NOT_VIABLE` sobre el enunciado de C-1); **diverge parcialmente de `E-A`** (que concluyó `VIABLE` bajo la lectura "recomendación a la autoridad" — lectura que C-1 no declara); la divergencia queda registrada con sus razones |
| **Limitaciones** | veredicto relativo a la evidencia disponible y al enunciado literal de C-1; `ejecutores: distinto` es condición necesaria y no suficiente (sin independencia epistemológica); el veredicto **no** impide que el mantenedor decida reconocer los findings por otra vía — eso sería una decisión humana posterior, no una corrección de este veredicto |
| **Razón de terminación** | `VERDICT` |

### Recomendación (advisory)

**Se emite,** separada del veredicto y de la decisión:

> **No reconocer por la vía de C-1.** Elevar al mantenedor con esta base: puede reconocer `<PLAN-114>:F-1` como `resolved` (causa eliminada y revalidada) y `<PLAN-114>:F-2` como `resolved` **con calificación explícita** (corrección de instancia revalidada; la causa raíz `<PLAN-114>:F-3` permanece `deferred` con su owner), registrando el reconocimiento como **acto humano en un artifact nuevo que referencie al Plan 114** (el cerrado no se reabre — regla post-close), con evidencia citada de C-1/C-2 y A2. Hasta que ese acto humano exista, el estado registrado `partially-resolved` es el correcto y no debe modificarse.

Esta recomendación es **advisory**: no autoriza, no aprueba, no decide y no modifica gobernanza.

### Decisión humana — fuera del mecanismo

**No tomada durante esta ejecución.** No hubo decisión del mantenedor disponible al ejecutar el Trial.

`Trial Verdict ≠ Recommendation ≠ Human Decision`

Registro durante la ejecución: el reconocimiento formal de `<PLAN-114>:F-1`/`F-2` **permaneció pendiente** de la autoridad humana (owner: mantenedor), sin resolución improvisada, y este Plan no los declaró resueltos. La decisión queda registrada como pendiente en `### Pending decisions` de este Plan (PC-1).

## Registro del Trial — Escenario B (Steps 4 y 6)

> **Este registro es contenido experimental del Plan 116.** No crea gobernanza, no posee autoridad y no resuelve el finding deliberado: la resolución de `F-3` pertenece a su owner (mantenedor).

### Marco declarado

| Elemento | Valor |
|---|---|
| Problema / cuestión (referencia) | Decisión sobre `<PLAN-114>:F-3` (estado `deferred`, owner: mantenedor): el ejemplo `F-01`/`C-01` de `docs/plans/_TEMPLATE.md` (líneas 118 y 126) frente al contrato del checker C-3, que solo reconoce `F-<n>`/`C-<n>` con primer dígito 1–9 (`docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending`) |
| Candidata | `C-1` — intervenir ahora sobre `F-3`: corregir el ejemplo del template a la forma canónica sin cero a la izquierda (y, alternativamente, adaptar `tools/check_lifecycle_lineage.py` para aceptar ambas formas) |
| Modo | `viability` |
| Criterios | `K-1` impacto actual del defecto (¿qué rompe hoy?) · `K-2` costo y riesgo de intervenir ahora · `K-3` riesgo de no intervenir · `K-4` frontera de autoridad y estado normativo del finding (resolución = decisión humana; `deferred` con owner) |
| Límites declarados | máximo 2 pasadas de evaluación; sin confrontación; una síntesis; mismo ejecutor para ambas pasadas (`ejecutores: mismo` — declarado, sin afirmación de independencia) |
| Motivo de invocación | Escenario B del dogfood de cierre autorizado por D-2: una decisión cuyo resultado correcto puede ser NO CHANGE / no modificar, para demostrar que la deliberación no presupone que siempre debe producir cambios |

### Perspectiva E-A — postura: sostener la viabilidad de `C-1`

- **Etiqueta local:** `E-A`.
- **Ejecutor:** agente DEV (sesión de ejecución del Plan 116).
- **Material recibido:** registro `<PLAN-114>:F-3` (`docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending`); contrato del checker C-3 (`.agents/policies/lifecycle-checkers.md:C-3 — Lifecycle lineage check`); regla operacional de findings (`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`); ejemplo del template (`docs/plans/_TEMPLATE.md:Findings / Correcciones / Pending`); estado de la batería en este repo (baseline de este Plan, Step 1).
- **Material compartido:** encuadre, criterios `K-1..K-4` y el material común anterior.
- **Relación con conclusiones previas:** ninguna (primera pasada del Trial).
- **Condición de compromiso:** conclusión registrada antes de que `E-B` conociera conclusión alguna.
- **Conclusión:** **VIABLE** — intervenir ahora es viable técnicamente: el defecto es real, la corrección del template es de una línea y elimina la trampa documentada en su origen.
- **Razones por criterio:**
  - `K-1` **a favor de la existencia del problema.** El defecto es real y ya produjo daño una vez: el Plan 114 copió el ejemplo y el checker lo clasificó `GAP=1` (causa raíz de `<PLAN-114>:F-2`, registrada en `F-3`). Hoy el corpus vigente usa la forma canónica y el workaround (declarar la forma correcta en cada Plan) funciona, pero la trampa sigue viva en el template.
  - `K-2` **costo bajo en la variante mínima; alto en la variante amplia.** Corregir solo el ejemplo del template es un cambio de una línea (Clase B o C según juicio, con batería verde). Adaptar el checker para aceptar ambas formas es un cambio de contrato con impacto en `tests/` (los escenarios adversariales permanentes del §20 de `docs/plans/100-change-lifecycle-lineage-integrity.md` incluyen variantes con cero a la izquierda que deben seguir siendo inválidas) — costo y riesgo sensiblemente mayores, y toca `tools/` y `tests/`.
  - `K-3` **a favor.** No intervenir deja una trampa para todo Plan futuro que copie el ejemplo; la mitigación actual (declarar la forma correcta en cada Plan, como hace este) es manual y no elimina la causa raíz.
  - `K-4` **en contra parcial.** `F-3` está `deferred` con owner: mantenedor; la resolución de un finding es decisión humana con evidencia (CL-8; AU-3). La candidata es viable como **recomendación** de intervención, no como acto autónomo del agente: intervenir sobre el template sin decisión del mantenedor sería resolver un finding por cuenta propia.
- **Premisas:** (P1) el contrato del checker C-3 es la forma canónica (`F-<n>`/`C-<n>`, primer dígito 1–9) — `.agents/policies/lifecycle-checkers.md:C-3 — Lifecycle lineage check`; (P2) el template es el origen del ejemplo defectuoso — `docs/plans/_TEMPLATE.md:Findings / Correcciones / Pending`; (P3) un `GAP` es advisory y no invalida (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).
- **Supuestos:** que corregir el template no requiere tocar el checker (el ejemplo corregido quedaría alineado al contrato vigente); que el mantenedor no considera la trampa como protección deliberada del vocabulario estricto.
- **Incertidumbres:** si el mantenedor prefiere que el checker acepte ambas formas (normalizar con ceros) en lugar de corregir el ejemplo; si existe un motivo normativo oculto para el ejemplo con ceros (no hay evidencia de ello).

### Perspectiva E-B — postura: atacar `C-1`

- **Etiqueta local:** `E-B`.
- **Ejecutor:** **el mismo** agente DEV (misma sesión) → `ejecutores: mismo`.
- **Material recibido:** el mismo material común que `E-A` (registro `<PLAN-114>:F-3`; `.agents/policies/lifecycle-checkers.md:C-3 — Lifecycle lineage check`; `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`; `docs/plans/_TEMPLATE.md:Findings / Correcciones / Pending`; baseline del Plan 116) **más** el alcance autorizado de este Plan (`## Alcance` del Plan 116) y las reglas de cambio de la capa operacional (`.agents/workflows/change-lifecycle.md:1. Change detection and classification`). **No** recibió la conclusión de `E-A`.
- **Material compartido:** encuadre, criterios `K-1..K-4` y el material común anterior.
- **Relación con conclusiones previas:** ninguna (no conocía `E-A`).
- **Condición de compromiso:** conclusión registrada antes de la revelación de `E-A`.
- **Conclusión:** **NOT_VIABLE** — intervenir **ahora** no es viable: la vía autorizada de este cambio excluye `tools/` y `tests/`, la variante mínima (template) queda fuera del change surface autorizado de este Plan, y la resolución del finding es decisión del mantenedor que este cambio no tiene autoridad para ejecutar. **NO CHANGE es el resultado correcto de esta deliberación.**
- **Razones por criterio:**
  - `K-1` **el problema existe, pero su impacto presente es advisory.** `GAP ≠ FAIL`: un Plan que copie el ejemplo produce un `GAP` detectable y corregible en su propia validación (exactamente lo que el Plan 114 hizo con `C-2`). No hay evidencia de un segundo incidente desde el 2026-09-09. Un defecto real no implica urgencia de intervención.
  - `K-2` **el costo no es el del escenario ideal.** La variante mínima (template solo) es barata en diffs, pero su costo de gobernanza no es cero: toca un template normativo del repo, exige clasificación (Clase B/C), batería verde y un registro de corrección con provenance (LC-1) — y el change surface autorizado de **este** Plan no lo incluye. La variante amplia (checker) multiplica el costo: contrato del checker + regresiones adversariales del §20 que exigen que `F-01`/`C-01` sigan siendo inválidos. Intervenir ahora, dentro de este cambio, expandiría el scope autorizado (prohibido: `## Stop Conditions`).
  - `K-3` **el riesgo de no intervenir está mitigado y acotado.** El workaround es barato y ya está operando (este Plan declara la forma canónica); la trampa solo afecta a quien copie el ejemplo literal, y el daño resultante es un `GAP` advisory corregible. No intervenir no compromete el cierre del MVP.
  - `K-4` **decisivo.** `F-3` tiene owner (mantenedor) y estado `deferred`: una decisión consciente de no resolverlo ahora. Reabrir la decisión corresponde a la autoridad humana (AU-3), no al mecanismo ni al agente. La candidata "intervenir ahora" es, en sentido estricto, una resolución de finding encubierta si se ejecutara sin esa autoridad.
- **Debilidades de `E-A` detectadas:** (i) presenta el costo de la variante mínima sin contar el costo de gobernanza (clasificación, batería, corrección con lineage) ni el límite de scope de este cambio; (ii) no distingue "defecto real" de "urgencia de intervención" — K-1 no responde si intervenir **ahora**; (iii) asume que el mantenedor no tiene un motivo para el estado `deferred`, cuando el registro de `F-3` declara explícitamente un owner y un destino (`docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending`).
- **Evidencia faltante (declarada):** no existe registro de un segundo incidente causado por el ejemplo del template; no existe pedido del mantenedor de resolver `F-3`; no existe autorización de este cambio que incluya `docs/plans/_TEMPLATE.md` en el change surface.
- **Consecuencias negativas de intervenir ahora:** expansión del scope autorizado; precedente de resolver findings por agencia propia contra el owner declarado; costo de gobernanza sin ganancia funcional (el workaround ya mitiga).
- **Supuestos:** que el estado `deferred` de `F-3` refleja la preferencia vigente del mantenedor (es la lectura directa del registro).
- **Incertidumbres:** si el mantenedor querrá resolver `F-3` junto con el cierre de este Plan (en cuyo caso la vía correcta es una decisión humana + un cambio Clase B/C propio, no este Plan); si el vocabulario estricto del checker es intencional y el ejemplo es un error documental puro.

### Síntesis

**Entradas consideradas:** `E-A` y `E-B` (ambas comprometidas antes de la revelación; mismo ejecutor declarado). **Ninguna conclusión fue suprimida ni reescrita.**

**Convergencias (derivadas, con origen):**

- `S-1` — *el defecto es real y tiene causa raíz en el template*: deriva de `<PLAN-114>:F-3` (`docs/plans/114-adversarial-deliberation-mvp.md:Findings / Correcciones / Pending`) y del contrato del checker (`.agents/policies/lifecycle-checkers.md:C-3 — Lifecycle lineage check`). Ambas evaluaciones la asumen; solo discrepan en la urgencia de la intervención.
- `S-2` — *la resolución del finding es decisión humana*: deriva de `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)` y de `docs/adr/16-change-lifecycle-authority.md:Invariantes` (AU-3). Ambas evaluaciones la asumen; `E-B` la usa como criterio decisivo.

**Contradicciones identificadas (no adjudicadas):**

- `X-1` — **urgencia**: `E-A` sostiene que el defecto vivo justifica intervenir ahora; `E-B` sostiene que el impacto presente es advisory (`GAP ≠ FAIL`), mitigado y sin segundo incidente registrado. No se adjudica por el sintetizador.

**Dependencias y condiciones (derivadas):**

- `D-1` — la intervención sobre el template o el checker solo es viable **fuera** del change surface de este Plan y bajo la autoridad del owner de `F-3`.

**Desacuerdo preservado (explícito, sin adjudicar):** la divergencia se concentra en `X-1` (urgencia) y en si el costo de gobernanza de la variante mínima debe contarse en `K-2`; **no se resuelve por mayoría, por conteo ni por preferencia del sintetizador**.

**Sin contenido nuevo:** la síntesis no introdujo hechos externos, evidencia nueva ni argumentos materiales no fundados. No fue necesaria ninguna pasada adicional.

### Veredicto

| Campo | Valor |
|---|---|
| **Valor** | `NOT_VIABLE` — intervenir **ahora** sobre `F-3` no es viable dentro del alcance autorizado de este cambio y sin decisión del owner; **NO CHANGE es el resultado legítimo** |
| **¿Hubo ataque?** | Sí (`E-B`) |
| **Ejecutores** | `mismo` — dos pasadas del mismo ejecutor (agente DEV de esta sesión) |
| **Material compartido** | encuadre, criterios `K-1..K-4`, registro `<PLAN-114>:F-3`, contrato del checker C-3, regla operacional LC-1, template, baseline |
| **Criterios** | declarados: `K-1..K-4` |
| **Qué quedó sin hacer** | sin confrontación (declarada opcional y no usada en este Escenario); sin participación humana como ejecutor; límite de 2 pasadas respetado |
| **Razones por criterio** | `K-1` defecto real con impacto advisory · `K-2` costo de gobernanza + límite de scope en contra · `K-3` riesgo mitigado por workaround operando · `K-4` decisivo: resolución = decisión humana, `deferred` con owner |
| **Desacuerdo** | `X-1`, preservado sin adjudicar |
| **Relación con cada evaluación** | **coincide con `E-B`** (valor `NOT_VIABLE`); **diverge de `E-A`** (que concluyó `VIABLE`); la divergencia queda registrada con sus razones |
| **Limitaciones** | veredicto relativo a la evidencia disponible y al scope autorizado de este cambio; mismo ejecutor (sin afirmación de independencia); no impide que el mantenedor decida resolver `F-3` por otra vía en el futuro |
| **Razón de terminación** | `VERDICT` |

### Recomendación (advisory)

**Se emite,** separada del veredicto y de la decisión:

> **NO CHANGE — no intervenir sobre `F-3` en este cambio.** Mantener el finding `deferred` con owner (mantenedor). Si el mantenedor decide resolverlo en el futuro, la vía mínima es corregir únicamente el ejemplo del template (`docs/plans/_TEMPLATE.md`) a la forma canónica sin cero a la izquierda, como cambio Clase B/C propio con batería verde y registro de corrección con provenance; adaptar el checker para aceptar ambas formas es innecesario y costoso (las regresiones adversariales del §20 exigen que `F-01`/`C-01` sigan siendo inválidos). Mientras tanto, los Planes nuevos declaran la forma canónica en sus registros, como hace este Plan.

Esta recomendación es **advisory**: no autoriza, no aprueba, no decide y no modifica gobernanza.

### Decisión humana — fuera del mecanismo

**No tomada durante esta ejecución.** No hubo decisión del mantenedor disponible al ejecutar el Trial.

`Trial Verdict ≠ Recommendation ≠ Human Decision`

Registro durante la ejecución: `<PLAN-114>:F-3` **permaneció `deferred`** con owner (mantenedor), sin resolución improvisada, y este Plan no lo declaró resuelto. La decisión queda registrada como pendiente en `### Pending decisions` de este Plan (PC-1).

### NO CHANGE como resultado legítimo (registro obligatorio del Escenario B)

El resultado de esta deliberación es **no modificar**: el finding `F-3` sigue `deferred`, el template y el checker no se tocan, y no se produce ningún diff asociado a este Escenario. La deliberación demostró que el mecanismo puede concluir NO CHANGE con argumentos explícitos (K-2/K-4) sin presuponer que deliberar implica cambiar.

## Registro del Trial — Escenario C (Steps 5 y 6)

> **Este registro es contenido experimental del Plan 116.** No crea gobernanza, no posee autoridad y no autoriza ninguna release: la promoción a `master` con tags es autoridad RELEASE del mantenedor (`docs/adr/16-change-lifecycle-authority.md:Decisión`).

### Marco declarado

| Elemento | Valor |
|---|---|
| Problema / cuestión (referencia) | Decisión de release pendiente: las versiones `11.1.0` y `11.2.0` están materializadas en `dev` con secciones de changelog propias y **sin tag**; `master` ya recibió el batch `11.0.0`/`11.0.1` (commit de promoción `2dfb99f`, tags anotados, `dist` regenerado en `bfdd63c`). La promoción de lo restante es decisión del mantenedor (`docs/VERSIONING.md:1. Ramas y roles`; `docs/adr/16-change-lifecycle-authority.md:Decisión` — clase RELEASE). Evidencia factual: `git tag --list '11.*'` = `11.0.0`, `11.0.1`; `check_version_state.py` reporta "changelog section [11.1.0] has no tag" y "VERSION 11.2.0 has no tag" |
| Candidata | `C-1` — promover **ahora** en batch las versiones restantes `11.1.0` y `11.2.0` a `master` con sus tags anotados |
| Modo | `viability` |
| Criterios | `K-1` completitud y verificación de las versiones acumuladas · `K-2` compatibilidad y notas de migración del batch (las MINOR `11.1.0`/`11.2.0` tienen sus notas en `docs/MIGRATION.md`) · `K-3` urgencia y demanda (adoptantes sobre `dist`/`master` en `11.0.1`) · `K-4` política de autorización de release vigente (MINOR requiere confirmación del usuario — `docs/VERSIONING.md:3. Versionado`) |
| Límites declarados | máximo 2 pasadas de evaluación; **una ronda de confrontación acotada** (propósito declarado; §7 de la convención); una síntesis; mismo ejecutor para ambas pasadas (`ejecutores: mismo` — declarado, sin afirmación de independencia) |
| Motivo de invocación | Escenario C del dogfood de cierre autorizado por D-2: ejercitar un camino **no canónico** del mecanismo — la confrontación opcional (§7), definida en la convención pero nunca ejercitada en el dogfood previo — sobre una decisión DEV real (release) |

### Perspectiva E-A — postura: sostener la viabilidad de `C-1`

- **Etiqueta local:** `E-A`.
- **Ejecutor:** agente DEV (sesión de ejecución del Plan 116).
- **Material recibido:** política de versionado (`docs/VERSIONING.md:1. Ramas y roles`, `docs/VERSIONING.md:2. Invariantes`, `docs/VERSIONING.md:3. Versionado`, `docs/VERSIONING.md:9. Estado actual (2026-09-05)`); notas de migración (`docs/MIGRATION.md:14. Change Governance Artifact — 11.1.0 (plan 115, RFC-76)`, `docs/MIGRATION.md:15. Change Governance Artifact — identidad y persistencia — 11.2.0 (plan 115, RFC-76)`); secciones del changelog `[11.1.0]` y `[11.2.0]`; evidencia factual de git (`git tag --list '11.*'`, `git log master --oneline`, `git log dist --oneline`, salida de `check_version_state.py`).
- **Material compartido:** encuadre, criterios `K-1..K-4` y el material común anterior.
- **Relación con conclusiones previas:** ninguna (primera pasada del Trial).
- **Condición de compromiso:** conclusión registrada antes de que `E-B` conociera conclusión alguna.
- **Conclusión:** **VIABLE** — el batch es técnicamente viable: las dos versiones están materializadas, validadas (batería verde en el plan 115) y con changelog y notas de migración completos; el batch tiene precedente inmediato (el batch `11.0.0`/`11.0.1` promovido en `2dfb99f`).
- **Razones por criterio:**
  - `K-1` **a favor.** `11.1.0` y `11.2.0` están atadas al plan 115 (`Executed`, RFC-76) con validación registrada; el changelog tiene secciones `[11.1.0]` y `[11.2.0]` con sus ítems; el invariante versión↔changelog se verifica con `check_version_state.py` (OK con warnings esperados en `dev`).
  - `K-2` **a favor.** Ambas son MINOR aditivas con sus notas de migración (`docs/MIGRATION.md:14...` y `:15...`); el modelo del artifact ya fue sincronizado en `11.2.0` (D-01/D-02/D-03). El batch no omite ninguna obligación de migración.
  - `K-3` **a favor, con reserva.** El batch `11.0.0`/`11.0.1` ya está publicado; `master`/`dist` quedan **una versión minor detrás** del estado validado de `dev` (`11.2.0`), por lo que el adoptante recibe un payload sin el Change Governance Artifact completo. La reserva: no existe un registro de demanda explícita de adoptantes; el argumento es de frescura, no de bloqueo.
  - `K-4` **en contra parcial.** La promoción es autoridad RELEASE del mantenedor (`docs/VERSIONING.md:1. Ramas y roles`: tags solo en `master`; `docs/adr/16-change-lifecycle-authority.md:Decisión` clase RELEASE) y `docs/VERSIONING.md:3. Versionado` exige confirmación del usuario para MINOR. La candidata es viable como **recomendación** al mantenedor, nunca como acto del agente.
- **Premisas:** (P1) los releases batch tienen precedente explícito e inmediato (tags `11.0.0`/`11.0.1` sobre el commit de promoción `2dfb99f`; `dist` regenerado en `bfdd63c`); (P2) las secciones de changelog con fecha sin tag son "releases en curso que se oficializan al promover" (`docs/VERSIONING.md:5. Changelog`); (P3) `dist` se regenera por CI al taggear (`docs/VERSIONING.md:1. Ramas y roles`).
- **Supuestos:** que la validación del plan 115 sigue aplicable al HEAD actual de `dev` para el dominio de `11.1.0`/`11.2.0`.
- **Incertidumbres:** si el mantenedor prefiere promoción por versión individual en lugar de batch; si el batch debe esperar a que este Plan 116 se cierre para incluir su registro documental en el mismo release.

### Perspectiva E-B — postura: atacar `C-1`

- **Etiqueta local:** `E-B`.
- **Ejecutor:** **el mismo** agente DEV (misma sesión) → `ejecutores: mismo`.
- **Material recibido:** el mismo material común que `E-A` más la política de autoridad (`docs/adr/16-change-lifecycle-authority.md:Decisión`, `docs/adr/16-change-lifecycle-authority.md:Invariantes`) y la política operacional (`.agents/policies/authority.md:Stop conditions (authority)`). **No** recibió la conclusión de `E-A`.
- **Material compartido:** encuadre, criterios `K-1..K-4` y el material común anterior.
- **Relación con conclusiones previas:** ninguna (no conocía `E-A`).
- **Condición de compromiso:** conclusión registrada antes de la revelación de `E-A`.
- **Conclusión:** **NOT_VIABLE** — promover **ahora** no es viable: `K-4` no se satisface (no existe confirmación del usuario para las MINOR `11.1.0`/`11.2.0`, y la promoción es autoridad RELEASE del mantenedor), y la urgencia de `K-3` no está soportada por evidencia de demanda.
- **Razones por criterio:**
  - `K-1` **aceptado.** No ataca la completitud: las versiones están materializadas y validadas. `K-1` es condición necesaria pero no suficiente.
  - `K-2` **aceptado con observación.** Las notas de migración existen; la observación es que ambas versiones pertenecen al mismo plan 115, cuya fila en `docs/plans/INDEX.md` declara todavía "Sin commit, sin tag (release pendiente)" mientras git muestra los commits `14e7fc4`/`b8c6ce0` en `dev`: un rezago descriptivo INDEX↔git (AU-4: el INDEX no es autoridad) que, si no se reconcilia antes de promover, dejaría la traza descriptiva del release desalineada con la factual.
  - `K-3` **no soportado.** No existe registro de demanda ni de bloqueo de adoptantes: `dist` en `11.0.1` es un release publicado y funcional; "una minor detrás" no es un defecto del release vigente. El argumento de frescura no constituye urgencia.
  - `K-4` **decisivo y no satisfecho.** `docs/VERSIONING.md:3. Versionado` exige confirmación del usuario para MINOR; la clase RELEASE es autoridad del mantenedor (`docs/adr/16-change-lifecycle-authority.md:Decisión`); `.agents/policies/authority.md:Stop conditions (authority)` detiene cualquier agente sin autorización normativa para el cambio. No existe confirmación registrada para `11.1.0`/`11.2.0`. Sin `K-4`, el resto de los criterios no habilita nada.
- **Debilidades de `E-A` detectadas:** (i) trata la validez técnica (`K-1`/`K-2`) como si implicara autorización de release, cuando `K-4` es un gate independiente; (ii) usa "precedente de batch" como evidencia de que este batch debe hacerse ahora, sin registrar que el batch `11.0.0`/`11.0.1` también requirió la decisión del mantenedor (commit de promoción `2dfb99f`); (iii) la reserva de `K-3` debilita su propio caso de urgencia.
- **Evidencia faltante (declarada):** no existe confirmación del usuario registrada para `11.1.0`/`11.2.0`; no existe demanda registrada de adoptantes.
- **Consecuencias negativas de promover sin `K-4`:** release sin autorización (violación de la clase RELEASE); tags inmutables creados sin confirmación (los tags no se borran — `docs/VERSIONING.md:6. Tags`); precedente de que la evidencia técnica sustituye a la decisión humana de release.
- **Supuestos:** que "confirmación del usuario" no se satisface por ausencia de objeción (la política exige confirmación positiva para MINOR).
- **Incertidumbres:** si el mantenedor otorgará la confirmación al leer este registro (en cuyo caso el veredicto cambia de `NOT_VIABLE` a viable por autorización sobrevenida, y debe registrarse como decisión humana posterior, no como corrección del veredicto).

### Confrontación (§7 — una ronda acotada; camino no canónico del mecanismo)

- **Propósito declarado:** verificar si el argumento decisivo de `K-4` (ausencia de confirmación del usuario) puede ser superado por evidencia registrada, y si el argumento de urgencia de `K-3` tiene soporte factual.
- **Intercambio 1 — `E-B` → `E-A`:** *¿Existe alguna confirmación del usuario registrada para `11.1.0`/`11.2.0`, o algún registro de demanda de adoptantes? Si no existe, el caso "promover ahora" descansa sobre inferencia, y `K-4` exige una decisión positiva que este mecanismo no puede producir.*
- **Intercambio 2 — `E-A` → `E-B` (respuesta):** *No existe confirmación registrada: el changelog registra `[11.1.0]` y `[11.2.0]` sin tags y `check_version_state.py` reporta "changelog section [11.1.0] has no tag" y "VERSION 11.2.0 has no tag"; no hay registro de demanda de adoptantes. El argumento de urgencia queda sin soporte factual. La base de evidencia no cambia con más intercambios.*
- **Aporte registrado de la confrontación:** precisó que el único criterio insatisfecho es `K-4` (autoridad), no la evidencia técnica; descartó dos argumentos de urgencia no soportados (frescura general, precedente de batch) como motores de la decisión; confirmó que ningún intercambio adicional puede cambiar la base.
- **Terminación de la confrontación:** por el **criterio de valor** de `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md:7. Optional Confrontation` — el intercambio no puede cambiar la base de evidencia ni introducir un contraargumento material nuevo ⇒ la confrontación termina.

### Síntesis

**Entradas consideradas:** `E-A`, `E-B` y el registro de la confrontación (una ronda, terminada por criterio de valor). **Ninguna conclusión fue suprimida ni reescrita.**

**Convergencias (derivadas, con origen):**

- `S-1` — *la evidencia técnica del batch está completa* (`K-1`/`K-2` aceptadas por ambas evaluaciones): deriva de las secciones del changelog `[11.1.0]`/`[11.2.0]` y de las notas de migración (`docs/MIGRATION.md:14...`, `:15...`).
- `S-2` — *no existe confirmación del usuario registrada*: deriva de la salida de `check_version_state.py` (secciones sin tag) y de la ausencia verificada en el changelog/git.
- `S-3` — *la promoción es autoridad RELEASE del mantenedor*: deriva de `docs/adr/16-change-lifecycle-authority.md:Decisión` (clase RELEASE) y `docs/VERSIONING.md:1. Ramas y roles`.

**Contradicciones identificadas (no adjudicadas):**

- `X-1` — **urgencia de `K-3`**: `E-A` la sostiene por frescura general; `E-B` la rechaza por ausencia de demanda registrada. La confrontación dejó sin soporte factual el argumento de `E-A`; la contradicción queda registrada sin adjudicar.

**Dependencias y condiciones (derivadas):**

- `D-1` — la viabilidad de `C-1` depende íntegramente de `K-4` (confirmación del usuario); todos los demás criterios están satisfechos.

**Desacuerdo preservado (explícito, sin adjudicar):** la divergencia se concentra en `X-1`; **no se resuelve por mayoría, por conteo ni por preferencia del sintetizador**.

**Sin contenido nuevo:** la síntesis no introdujo hechos externos, evidencia nueva ni argumentos materiales no fundados. No fue necesaria ninguna pasada adicional.

### Veredicto

| Campo | Valor |
|---|---|
| **Valor** | `NOT_VIABLE` — promover **ahora** no es viable: `K-4` (confirmación del usuario para las MINOR `11.1.0`/`11.2.0`) no está satisfecho y es autoridad RELEASE del mantenedor |
| **¿Hubo ataque?** | Sí (`E-B`) |
| **¿Hubo confrontación?** | Sí — una ronda acotada (§7), terminada por criterio de valor (registro arriba) |
| **Ejecutores** | `mismo` — dos pasadas del mismo ejecutor (agente DEV de esta sesión) |
| **Material compartido** | encuadre, criterios `K-1..K-4`, política de versionado, notas de migración, changelog, evidencia git |
| **Criterios** | declarados: `K-1..K-4` |
| **Qué quedó sin hacer** | sin participación humana como ejecutor; sin verificación externa de las premisas; límites respetados (2 pasadas + 1 ronda) |
| **Razones por criterio** | `K-1` satisfecho · `K-2` satisfecho (con observación de rezago descriptivo INDEX↔git de la fila del plan 115) · `K-3` no soportado (sin demanda registrada) · `K-4` no satisfecho y decisivo |
| **Desacuerdo** | `X-1`, preservado sin adjudicar |
| **Relación con cada evaluación** | **coincide con `E-B`** (valor `NOT_VIABLE`); **diverge de `E-A`** (que concluyó `VIABLE` condicionado a `K-4`); la divergencia queda registrada con sus razones |
| **Limitaciones** | veredicto relativo a la evidencia disponible; mismo ejecutor (sin afirmación de independencia); una confirmación sobrevenida del mantenedor lo cambiaría por autorización externa, y debe registrarse como decisión humana posterior, no como corrección del veredicto |
| **Razón de terminación** | `VERDICT` |

### Recomendación (advisory)

**Se emite,** separada del veredicto y de la decisión:

> **No promover ahora.** Mantener las versiones `11.1.0` y `11.2.0` acumuladas en `dev` y elevar al mantenedor la decisión de release: la evidencia técnica está completa (changelog + migración + validaciones) y el batch tiene precedente inmediato (`11.0.0`/`11.0.1`), pero MINOR requiere confirmación del usuario (`docs/VERSIONING.md:3. Versionado`) y la promoción es autoridad RELEASE (`docs/adr/16-change-lifecycle-authority.md:Decisión`). Antes de promover conviene reconciliar la fila descriptiva del plan 115 en `docs/plans/INDEX.md` (dice "sin commit" contra los commits `14e7fc4`/`b8c6ce0` en git). Si el mantenedor confirma, la vía operativa es el playbook de `docs/VERSIONING.md:4. Flujo por plan (playbook)` (merge + tags anotados + `publish-dist`).

Esta recomendación es **advisory**: no autoriza, no aprueba, no decide y no modifica gobernanza.

### Decisión humana — fuera del mecanismo

**No tomada durante esta ejecución.** No hubo decisión del mantenedor disponible al ejecutar el Trial.

`Trial Verdict ≠ Recommendation ≠ Human Decision`

Registro durante la ejecución: la decisión de release (promoción de `11.1.0`/`11.2.0`) **permaneció pendiente** de la autoridad RELEASE del mantenedor, sin autorización improvisada. La decisión queda registrada como pendiente en `### Pending decisions` de este Plan (PC-1).

### Comportamiento observado del camino no canónico (registro obligatorio del Escenario C)

- **Qué ocurrió:** se ejecutó el camino con confrontación acotada (§7): dos pasadas comprometidas, una ronda de intercambio `E-B → E-A → E-A responde`, y la confrontación terminó por el criterio de valor (el intercambio no podía cambiar la base de evidencia).
- **Qué esperaba el mecanismo:** que la confrontación solo continúe si puede cambiar la base de evidencia o introducir un contraargumento material (§7); que el desacuerdo residual de criterio no se adjudique (§8).
- **Qué pudo resolver:** precisar el único criterio insatisfecho (`K-4`); descartar dos argumentos de urgencia sin soporte factual.
- **Qué no pudo resolver:** la ausencia de confirmación del usuario — correctamente: no es resoluble por el mecanismo (§12 de la convención; autoridad RELEASE).
- **Recuperación:** no requerida; el camino terminó en `VERDICT` sin degradación.
- **Intervención humana:** no requerida durante la ejecución; la decisión de release queda escalada al mantenedor como acto pendiente separado.
- **Afecta el cierre del MVP:** **no** — el ejercicio demuestra el camino confrontacional definido en la convención; la limitación observada es de autoridad (deseada y normativa), no del mecanismo.

## Criterios de salida

- [x] 1. Los escenarios A/B/C fueron ejecutados sobre decisiones reales y verificables del repositorio y registrados en este Plan conforme a la convención.
- [x] 2. El Escenario A tiene dos perspectivas atribuidas con ejecutores diferenciados y compromiso antes de revelación.
- [x] 3. El Escenario B registra NO CHANGE como resultado legítimo y explícito.
- [x] 4. El Escenario C ejercita un camino no canónico (confrontación acotada) conforme a la convención.
- [x] 5. Cada registro contiene marco, perspectivas, síntesis con desacuerdo preservado, veredicto con base declarada y recomendación separada.
- [x] 6. Cada decisión humana queda registrada como acto separado o como pendiente escalada con owner; nunca improvisada por el agente.
- [x] 7. No hubo cambios fuera del change surface autorizado.
- [x] 8. Batería canónica en verde; C-1 `VALID`; C-3 sin `ANOMALY` (C-2 con resultado declarado según el estado del commit del mantenedor — pendiente).
- [x] 9. Todas las citas `ruta:sección` resuelven (`check_plan_citations.py`).
- [x] 10. Documentación actualizada: banner de la convención, `docs/working/proposals/INDEX.md`, `docs/plans/INDEX.md`, `CHANGELOG.md:[Unreleased]`.
- [x] 11. El closure predicate A–I queda evaluado letra por letra con evidencia.
- [x] 12. Las limitaciones quedan declaradas: sin afirmaciones de independencia epistemológica; sin autoridad transferida al mecanismo; sin trabajo Protocol-native.

## Verificación

Batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (comandos exactos en Step 7) + gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + juicios manuales de conformidad de los registros con la convención + `git status --short --branch` y `git diff --stat` contenidos en el change surface. `tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por diseño; no se ejecuta como gate de este Plan.

## Validation anchor

Registrado al validar el Plan 116 (2026-09-12). La validación **A1** corre sobre el estado de contenido del working tree staged (antes de agregar los registros de esta sección y del checkpoint — anti-circularidad, precedente Planes 96–115).

- **Declared scope:** el change surface autorizado del Plan 116 — `docs/plans/116-adversarial-deliberation-mvp-closure.md` (nuevo), `docs/plans/INDEX.md` (fila + serie), `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` (solo banner de estado), `docs/working/proposals/INDEX.md` (fila) y `CHANGELOG.md` (ítem `[Unreleased]`) — + la batería canónica del repo (checkers DEV + `pytest`) sobre ese scope.
- **Validation command-set:** los 7 comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `python -m pytest tests/`) + `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + juicios manuales de conformidad de los Tres Trials con la convención + `git diff --check`.
- **Effective inputs (repo content):** los 5 paths del change surface (los checkers de la batería escanean además `docs/`, `protocol/`, `tools/`, `tests/`, `runtime/` y la raíz; `pytest` consume `tests/` + `tools/` + `runtime/`); representados por la State identity (tree id del index staged).
- **Observed dependencies:** `no instrumentado` (sin tooling de instrumentación en esta ejecución; el consumo por comando se observa en la documentación de cada checker — `docs/VERSIONING.md:4.1 Batería canónica de verificación`).
- **Environmental factors:** Windows + OneDrive; Python 3.14.3 (`C:\Program Files\Python314`) con `pytest` 9.0.3 en `AppData\Roaming\Python\Python314\site-packages`; git 2.55.0.windows.5; git advierte normalización LF→CRLF en los archivos nuevos; `protocol/.agents/VERSION` = 11.2.0 (sin tag, esperado en `dev`); sin red. **Adaptación ambiental declarada:** bajo la política de archivos del sandbox, el fixture `tmp_path`/los directorios temporales de pytest no son enumerables (`PermissionError [WinError 5]` en `AppData\Local\Temp\dsh-…` y en basetemps del workspace), por lo que la pierna `pytest` se ejecutó con `--basetemp=.pytest-basetemp-116 -p no:cacheprovider`; el resultado queda clasificado por clase (ver resultados A1 abajo); este fallo ambiental es **preexistente al baseline** de este Plan y no es causado por el cambio.
- **Scoped Content Identity:**
  - State identity (estado validado = index staged del working tree; A1): T1 = `cf0358b061750db322561bac2b89bc44c2048056` (generado con `git write-tree` sobre el estado staged).
  - Delta scoped identity (scope S = los cinco paths del change surface, ordenados; serialización `scoped-v1` + pares `path NUL blob NUL`): `835bd6c6e9affcd4f2a69714caddf1e00a9cf33ba99c8882ef80a5efdedcbaf6` (generado con `tools/scoped_content_identity.py` sobre los cinco paths).
- **Validity / stale:** `vigente` (A1, estado de contenido previo a los registros de cierre); **revalidada por A2** sobre el estado final (ver `## Checkpoint / cierre`).

**A1 — resultados observados (estado de contenido, tree `cf0358b0…`):**

| Comando | Resultado |
|---|---|
| `check_protocol_invariants.py --payload protocol .` | **PASS** — "Protocol invariants OK: 213 files checked, 9948 references verified" |
| `check_plan_citations.py` | **PASS** — "All citations resolve" |
| `check_plan_structure.py` | **PASS** — "All numbered documents conform: no structural violations found" |
| `check_taxonomy_coherence.py` | **PASS** — "Taxonomy coherence OK" |
| `check_session_artifacts.py` | **PASS** — "Session artifacts OK" |
| `check_version_state.py` | **PASS** — "Version state OK" (warnings de secciones `[x.y.z]` sin tag: esperados en `dev`; incluye `[11.1.0]` y `VERSION 11.2.0`) |
| `pytest tests/` (adaptado) | **clasificación ambiental** — fallos por `PermissionError [WinError 5]` en directorios temporales del sandbox (misma clase documentada en el Plan 114 A1 y en la nota del Plan 115); **los tests content-sensitive del repo pasan**: la prueba de dogfooding real del lineage checker (`test_t27_real_repo_dogfooding` de `tests/test_check_lifecycle_lineage.py`) y la prueba de estructura real del repo (`test_real_repo_has_no_violations` de `tests/test_check_plan_structure.py`) — 2 passed (sin `tmp_path`); el resto de los ERRORs/FAILs son la clase ambiental preexistente, verificado contra el baseline pre-cambio de este Plan |
| C-1 (`check_lifecycle_anchor.py`) | plan 116 `GAP` esperado en A1 (anchor aún sin registrar — esta misma sección); resto del corpus sin cambios: `EXCLUDED=94, VALID=20, GAP=2 (planes 115 y 116), ANOMALY=0` |
| C-3 (`check_lifecycle_lineage.py`) | plan 116 `VALID` — `116 plans inspected; EXCLUDED=96, BOUNDARY=0, N/A=16, VALID=4, GAP=0, ANOMALY=0` |
| C-2 (`check_lifecycle_checkpoint.py`) | pendiente del commit del mantenedor (ver `## Checkpoint / cierre`) |
| Juicios manuales de conformidad | **PASS** — cada Trial: marco declarado, perspectivas atribuidas, compromiso antes de revelación, procedencia, síntesis sin contenido nuevo con desacuerdo preservado, veredicto con base, recomendación separada, decisión humana separada/pendiente |
| `git diff --check` | limpio |

**A2 — revalidación sobre el estado final de registros:** ejecutada con la misma command-set sobre el estado staged que incluye `## Validation anchor`, `## Checkpoint / cierre`, `## Nota de ejecución`, `## Resultado final del Plan`, el contenedor `## Findings / Correcciones / Pending` (con `<PLAN-116>:F-1`/`C-1`), el banner de la convención, la fila de `docs/working/proposals/INDEX.md`, la fila/serie del Plan 116 en `docs/plans/INDEX.md` y el ítem de `CHANGELOG.md`; resultado: todos los checkers **PASS** (`check_plan_citations` con "All citations resolve" tras `<PLAN-116>:C-1`), `check_lifecycle_anchor.py` → Plan 116 **`VALID`** (`EXCLUDED=94, VALID=21, GAP=1 (plan 115 preexistente), ANOMALY=0`), `check_lifecycle_lineage.py` → Plan 116 **`VALID`** (`GAP=0`, `ANOMALY=0`), `check_lifecycle_checkpoint.py` → Plan 116 `GAP` declarado (commit del mantenedor pendiente — precedente Plan 115), las dos pruebas content-sensitive del repo **pasan** y la pierna `pytest` completa mantiene la clase ambiental preexistente sin fallos nuevos (idéntica a la del baseline: 1 failed + 404 errors por `PermissionError [WinError 5]`, el failed preexistente es la prueba de non-git-root de `tests/test_determine_execution_state.py`). Identidades A2: computadas con `tools/scoped_content_identity.py` (delta) y `git write-tree` (state identity) sobre el estado staged de revalidación; los valores finales no se embeben por auto-referencia y se verifican en git tras el commit del mantenedor (precedente Planes 114/115).

## Checkpoint / cierre

- **Commits de cierre:** commit atómico de cierre de este Plan en `dev` — `feat(dev): close adversarial deliberation MVP (plan 116)`; su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable en `git log` tras el commit). Baseline del change: `b8c6ce0` (plan 115, RFC-76). Sin commits adicionales, sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** **A1** sobre el estado de contenido (tree `cf0358b0…`) + **A2** de revalidación sobre el estado final de registros (este estado, con `## Validation anchor`, `## Checkpoint / cierre`, `## Nota de ejecución`, `## Resultado final del Plan` y la fila del Plan 116 actualizada en `docs/plans/INDEX.md`).
- **Estado de cierre (tree id):** tree del index staged final = `git write-tree` (no embebido por auto-referencia; verificable en git tras el commit del mantenedor).
- **Consistencia checkpoint↔anchor:** evaluada contra **A2** (GC-1). **Evidencia PASS de la revalidación A2 sobre el estado final staged** (state identity verificada con `git write-tree` sobre el index staged; el valor no se embebe por auto-referencia — precedente Planes 114/115): los 6 checkers canónicos PASS (`check_plan_citations` "All citations resolve" tras `<PLAN-116>:C-1`); C-1 → Plan 116 `VALID`; C-3 → Plan 116 `VALID`, `GAP=0`, `ANOMALY=0`; las dos pruebas content-sensitive del repo pasan (la prueba de dogfooding real del lineage checker y la prueba de estructura real del repo, 2 passed); la pierna `pytest` completa mantiene la clase ambiental preexistente de permisos del sandbox sin fallos nuevos (idéntica al baseline); C-2 → `GAP` declarado por ausencia de commits (el commit es acción del mantenedor, precedente Plan 115). `Closed` se deriva solo cuando el commit del mantenedor exista y su tree corresponda al estado validado por A2.
- **Governance aplicada:** Plan `Executed` (header + espejo en `docs/plans/INDEX.md`); ítem `(plan 116, —)` en `CHANGELOG.md:[Unreleased]`; banner de estado de la convención y fila de `docs/working/proposals/INDEX.md` actualizados; pending decisions registradas con owner (PC-1); sin RFC/ADR nuevo; sin `VERSION` bump (permanece `11.2.0`) ni tag (RFC-69).
- **Condición derivada:** **`Closed` (docs-only, sin release)** — `Executed` (status) ∧ governance aplicada ∧ checkpoint ∧ consistencia (A2) ∧ evidencia PASS para el estado de cierre ∧ **aceptación del mantenedor** (decisión humana D-1 del Human Checkpoint, 2026-09-12) ∧ **commit atómico de cierre**. `Executed ≠ Committed ≠ Closed ≠ Released`; ni `Promoted` ni `Released` (docs-only, RFC-69). Residuo declarado no bloqueante: C-2 puede seguir reportando `GAP` por auto-referencia del commit único (el commit no puede embeber su propio SHA); las tres decisiones deliberadas (F-1/F-2, F-3, release `11.1.0`/`11.2.0`) permanecen pendientes con owner (mantenedor) y **no** forman parte de este cierre.

## Findings / Correcciones / Pending

Registros reales de este artifact (las reglas del Incremento 2 aplican a
artifacts nuevos; la ausencia de registros no es invalidez).

### Findings

- `<PLAN-116>:F-1` — estado: `partially-resolved` (vía `<PLAN-116>:C-1`); observación: la tabla de resultados A1 del `## Validation anchor` citaba las dos pruebas content-sensitive del repo en la forma `tests/<archivo>.py::<nombre-de-prueba>`, y `check_plan_citations.py` las parseó como citas `path:sección` con sección inexistente (2 broken citations en la línea del anchor); evidencia original: salida de `python tools/check_plan_citations.py` en la primera corrida de A2 ("Broken citations: 2"); estado git observado: `dev` @ `b8c6ce0`, working tree con el Plan 116 en vuelo, estado staged pre-corrección (tree `1a573d9f…`); provenance original: registro del anchor escrito por el agente durante la ejecución del Plan 116 (Steps 7–9); resolución: la redacción de la celda se reformuló para nombrar las pruebas sin la forma `path:sección` mediante `<PLAN-116>:C-1` y se revalidó con la batería (ver A2); la resolución formal del finding corresponde a la autoridad humana (owner: mantenedor).

### Correcciones

- `<PLAN-116>:C-1` — refs origen: `<PLAN-116>:F-1`; alcance de revalidación: la celda de resultados A1 del `## Validation anchor` de este Plan sobre la batería canónica completa del estado corregido (A2), en particular `check_plan_citations.py`; evidencia: salida de la revalidación A2 ("All citations resolve") sobre el estado final staged; carácter: FACTUAL/TRACEABILITY (no normativo); autorización: Plan 116 `Aprobado para ejecución` (Steps 7–9); qué se corrigió: la forma de la referencia a las pruebas (sin cambiar el contenido factual del resultado).

### Pending decisions

- `<PLAN-116>` — decisión (Escenario A): reconocimiento formal (o no) de los findings `<PLAN-114>:F-1`/`F-2` como `resolved`; blocking: no; owner: mantenedor; escalación: mantenedor; resolución: **pendiente** — el Trial concluyó `NOT_VIABLE` para la candidata tal como estaba enunciada (acto sin actor declarado, sin vía de registro, sin calificación de alcance); la recomendación advisory describe la vía posible (acto humano en artifact nuevo post-close por referencia; F-1 `resolved`, F-2 `resolved` con calificación respecto de la causa raíz F-3); evidencia: registro del Escenario A de este Plan; efecto downstream: `<PLAN-114>:F-1`/`F-2` permanecen `partially-resolved` (estado correcto mientras no exista el acto humano); ADR-worthiness: no aplica.
- `<PLAN-116>` — decisión (Escenario B): resolver o mantener deferred el finding `<PLAN-114>:F-3` (ejemplo `F-01`/`C-01` del template frente al contrato del checker C-3); blocking: no; owner: mantenedor; escalación: mantenedor; resolución: **pendiente** — el Trial concluyó `NOT_VIABLE` para intervenir ahora (NO CHANGE legítimo); el finding permanece `deferred` con su owner; evidencia: registro del Escenario B de este Plan; efecto downstream: ninguno (sin cambios); ADR-worthiness: no aplica.
- `<PLAN-116>` — decisión (Escenario C): promover (o no) las versiones `11.1.0`/`11.2.0` a `master` con tags (autoridad RELEASE); blocking: no; owner: mantenedor; escalación: mantenedor; resolución: **pendiente** — el Trial concluyó `NOT_VIABLE` para promover ahora (K-4: confirmación del usuario para MINOR no registrada); evidencia: registro del Escenario C de este Plan + `check_version_state.py` ("changelog section [11.1.0] has no tag", "VERSION 11.2.0 has no tag"); efecto downstream: `dev` sigue acumulando `11.1.0`/`11.2.0` sin tag; ADR-worthiness: no aplica.
- `<PLAN-116>` — decisión (predicate I del cierre): aceptación del cierre del MVP DEV de deliberación adversarial (`READY TO CLOSE`) como acto humano separado, y commit atómico de este cambio en `dev`; blocking: **sí** para la condición derivada `Closed` de este Plan; owner: mantenedor; escalación: mantenedor; resolución: **resuelta por el mantenedor (2026-09-12) — Human Checkpoint: D-1 = `ACCEPT CLOSURE OF THE DEV ADVERSARIAL DELIBERATION MVP`; D-2 = `ACCEPT FINAL DOGFOOD A/B/C`; commit atómico `feat(dev): close adversarial deliberation MVP (plan 116)` en `dev`**; evidencia: este Plan completo (registros A/B/C, Validation anchor A1/A2, checkpoint, evaluación A–I) + la aceptación humana registrada en `## Nota de ejecución` y `## Resultado final del Plan`; efecto downstream: el MVP DEV queda `Closed` (docs-only, sin release); la convención permanece Working/no normativa; la feature Protocol-native sigue FUTURE / NOT STARTED / OUT OF SCOPE; ADR-worthiness: no aplica (sin decisión normativa nueva).

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Que el registro se lea como autoridad o como decisión | Declaración de clase en cada registro; `Verdict ≠ Recommendation ≠ Decision`; decisiones humanas como acto separado |
| Contaminación de `E-B` por la conclusión de `E-A` | Compromiso antes de revelación: `E-A` queda escrito en este Plan antes de despachar a `E-B`; el ejecutor de `E-B` no recibe la conclusión de `E-A` |
| Atribuir independencia epistemológica a ejecutores diferenciados | Registro explícito: `ejecutores: distinto` es condición necesaria y no suficiente; ambos ejecutores son agentes LLM; se declara la limitación |
| Registro que colisiona con los checkers de lifecycle | Los encabezados de los registros de Trial evitan los contenedores `## Findings`/`### Findings`/`### Correcciones`; el contenedor real de lineage vive al final del Plan |
| Citas `ruta:sección` que no resuelven | `check_plan_citations.py` en validación; corrección `C-<n>` + revalidación si aparece un finding (precedente Plan 114) |
| Deriva de alcance (Protocol, tooling, gobernanza) | `## Alcance` + `## Stop Conditions` + `git diff --name-only` final |

## Trazabilidad

Decisiones humanas D-1/D-2 (prompt de Phase 2, 2026-09-12) → este Plan → registros de los Tres Trials → decisiones humanas separadas/pendientes → validación (batería + C-gates) → checkpoint → evaluación del closure predicate A–I → propuesta de estado final del MVP DEV. La feature Protocol-native queda declarada FUTURE / NOT STARTED / OUT OF SCOPE.

## Stop Conditions

Detenerse inmediatamente, registrando condición, evidencia, impacto y decisión humana requerida — sin improvisar, sin ampliar alcance y sin crear Planes adicionales — si: un cambio necesario queda fuera del scope autorizado; una decisión requiere autoridad humana y no puede registrarse como pendiente escalada; un checker revela una contradicción normativa (ANOMALY) que impide continuar; el closure predicate exige una condición nueva no autorizada; para cerrar resulta necesario modificar `protocol/`; resulta necesario crear RFC/ADR; resulta necesario crear arquitectura nueva; aparece una modificación inesperada del working tree; no puede demostrarse que un escenario ocurrió realmente; no puede separarse la decisión humana del resultado de la deliberación; la documentación existente contradice materialmente D-1/D-2; no puede determinarse de forma verificable el siguiente Plan válido; o aparece cualquier necesidad de resolver el diseño futuro Protocol-native.

## Nota de ejecución

**2026-09-12 — ejecución del Plan 116 (H1 = GO, decisiones D-1/D-2 del prompt de Phase 2).**

- **Intake y baseline:** `dev` @ `b8c6ce0` (HEAD confirmado); working tree limpio salvo `.codegraph/` (untracked preexistente) y directorios de pytest con permisos del sandbox; `master` @ `2dfb99f` (batch `11.0.0`/`11.0.1` ya promovido y taggeado; `dist` @ `bfdd63c`); `protocol/.agents/VERSION` = `11.2.0`. Batería baseline: los 6 checkers PASS; la pierna `pytest` presentaba **antes de este cambio** fallos ambientales por `PermissionError [WinError 5]` sobre directorios temporales del sandbox (clase documentada en el Plan 114 A1 y en la nota del Plan 115) — clasificados como ambientales, no regresiones.
- **Step 2 (GO):** D-1/D-2 registradas en `## Creación`; `Status` `Aprobado para ejecución`.
- **Steps 3–6 (Tres Trials):** ejecutados sobre decisiones reales y registrados en este Plan — **Escenario A** (reconocimiento formal de `<PLAN-114>:F-1`/`F-2`): dos perspectivas atribuidas con **ejecutores diferenciados** (`E-A` agente principal, `E-B` subagente de deliberación sin acceso a la conclusión de `E-A`; compromiso antes de revelación; `ejecutores: distinto` declarado como condición de procedencia, **sin** afirmación de independencia epistemológica), síntesis con desacuerdo preservado (`X-1`, `X-2`), veredicto `NOT_VIABLE` sobre la candidata tal como estaba enunciada, recomendación advisory con la vía posible; **Escenario B** (intervención sobre `<PLAN-114>:F-3`): veredicto `NOT_VIABLE` y **NO CHANGE registrado como resultado legítimo** (sin diffs asociados); **Escenario C** (release batch `11.1.0`/`11.2.0`): camino no canónico con **confrontación acotada (§7)** — nunca antes ejercitada — terminada por criterio de valor; veredicto `NOT_VIABLE` (`K-4`: confirmación del usuario para MINOR no registrada). Las decisiones humanas **no** fueron tomadas durante la ejecución y quedaron registradas como pendientes escaladas con owner en `### Pending decisions` (PC-1); `Trial Verdict ≠ Recommendation ≠ Human Decision` en cada registro.
- **Corrección factual declarada (Escenario C):** el marco del Escenario C se redactó inicialmente sobre el supuesto de que las cuatro versiones 11.x estaban sin promover; al verificar contra git (`git tag --list '11.*'`, `git log master`) se constató que el batch `11.0.0`/`11.0.1` **ya estaba promovido** (`2dfb99f`), y el registro se corrigió a la decisión real pendiente (promoción de `11.1.0`/`11.2.0`). La corrección ocurrió durante la ejecución (registro en vuelo, pre-validación) y quedó declarada aquí.
- **Steps 7–9 (validación y cierre):** batería canónica PASS en A1 (estado de contenido, tree `cf0358b0…`) y revalidación A2 sobre el estado final (ver `## Validation anchor`); C-1 `VALID` para el Plan 116 tras registrar el anchor; C-3 `VALID` (`GAP=0`, `ANOMALY=0`); C-2 pendiente del commit del mantenedor; los tests content-sensitive del repo (T27 dogfooding de lineage, estructura real del repo) **pasan**; el resto de la pierna `pytest` mantiene la clase ambiental preexistente (sin fallos nuevos respecto del baseline).
- **Step 10 (documentación):** banner de la convención (solo estado de cierre), `docs/working/proposals/INDEX.md`, `docs/plans/INDEX.md` (serie + fila) y `CHANGELOG.md:[Unreleased]` actualizados.
- **Step 11 (closure predicate):** evaluación letra por letra A–I en `## Resultado final del Plan`; propuesta `READY TO CLOSE` sujeta a la aceptación del mantenedor (predicate I pendiente).
- **Alcance:** `git status`/`git diff --name-only` contenidos en el change surface autorizado (5 paths docs); sin cambios en `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, plantillas, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`; sin RFC/ADR; sin `VERSION` bump, sin tag, sin push, sin merge. Residuo ambiental: `.pytest-basetemp-116/` (ignorado por git; no removible bajo el sandbox — misma clase que `.pytest-basetemp/` preexistente).
- **Estado:** los 12 criterios de salida satisfechos (el 6 con las decisiones humanas registradas como pendientes escaladas con owner) → `Executed`.

**2026-09-12 — Human Checkpoint y cierre del Plan (Phase 2.1).**

- **Auditoría previa al commit:** `git status` / `git diff` / `git diff --cached` verificados; change surface = exactamente los 5 paths autorizados (este Plan, `docs/plans/INDEX.md`, `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`, `docs/working/proposals/INDEX.md`, `CHANGELOG.md`); sin cambios fuera de scope; sin cambios unstaged; HEAD baseline `b8c6ce0`; `protocol/.agents/VERSION` = `11.2.0` sin cambios; sin tags nuevos; artifacts ambientales/preexistentes (`.codegraph/`, directorios de pytest) excluidos del commit.
- **Decisión humana (Human Checkpoint):** **D-1 = `ACCEPT CLOSURE OF THE DEV ADVERSARIAL DELIBERATION MVP`** y **D-2 = `ACCEPT FINAL DOGFOOD A/B/C`**, registradas como acto humano separado. Con la aceptación, el predicate **I pasa de `BLOCKED` a `PASS`** y la condición derivada **`Closed` (docs-only, sin release)** queda materializada por la aceptación + el commit atómico de este Plan. `Trial Verdict ≠ Recommendation ≠ Human Decision`: el cierre **no** convierte ningún veredicto en decisión normativa, **no** resuelve findings del Plan 114, **no** autoriza ningún release y **no** habilita ningún mecanismo Protocol-native.
- **Decisiones deliberadas que permanecen pendientes (no resueltas por este cierre):** reconocimiento de `<PLAN-114>:F-1`/`F-2`; resolución de `<PLAN-114>:F-3`; release de `11.1.0`/`11.2.0`. Siguen registradas como pendientes con owner (mantenedor) en `### Pending decisions`.
- **Validación pre-commit:** repetida sobre el estado staged — 6 checkers canónicos PASS, C-1 `VALID`, C-3 `VALID` (`GAP=0`, `ANOMALY=0`), tests content-sensitive del repo 2 passed; pierna `pytest` completa con la clase ambiental preexistente sin fallos nuevos (`1 failed, 130 passed, 404 errors`, idéntica al baseline); `git diff --check` limpio.

## Resultado final del Plan

### `ADVERSARIAL DELIBERATION MVP (DEV) — CLOSED`

**Fundamento — derivado de la evidencia registrada, no elegido previamente.**

- **Dogfood final ejecutado:** los Tres Escenarios A/B/C ocurrieron sobre decisiones reales y verificables del repositorio y quedaron registrados conforme a la convención: A (reconocimiento de F-1/F-2) con ejecutores diferenciados y compromiso antes de revelación; B (intervención sobre F-3) con **NO CHANGE** como resultado legítimo y sin diffs; C (release batch 11.1.0/11.2.0) con **confrontación acotada** terminada por criterio de valor. En los tres casos el veredicto fue `NOT_VIABLE` con base declarada, desacuerdo preservado y recomendación advisory separada — el mecanismo demostró que puede atacar candidatas sin adjudicar ni autorizar.
- **Autoridad intacta:** ninguna decisión humana fue improvisada por el agente; las tres decisiones deliberadas (A, B, C) permanecen registradas como pendientes escaladas con owner (PC-1) y **no** fueron resueltas por este cierre; la única decisión humana consumada es la aceptación del cierre del MVP DEV (D-1/D-2 del Human Checkpoint), registrada como acto separado; `Trial Verdict ≠ Recommendation ≠ Human Decision` en cada registro; el mecanismo no autorizó, no resolvió findings y no promovió releases.
- **Closure predicate:** A (contract) PASS · B (architecture) PASS · C (implementation) PASS · D (integration/lifecycle) PASS (C-2 puede seguir `GAP` por auto-referencia del commit único; advisory, sin contradicción) · E (validation) PASS · F (verification/reconstruction) PASS · G (dogfood) PASS con las limitaciones declaradas (Q6 no observable durante la ejecución en los tres casos; ejecutores diferenciados solo en A; sin independencia epistemológica) · H (documentation) PASS · **I (governance) PASS** — aceptación del mantenedor (D-1) + commit atómico de cierre. `JURY_TRIAL_CLOSED = A ∧ B ∧ C ∧ D ∧ E ∧ F ∧ G ∧ H ∧ I` **satisfecho para el MVP DEV**.
- **Limitaciones declaradas (aceptables para el MVP):** `ejecutores: distinto` es condición de procedencia necesaria y no suficiente (ambos ejecutores son agentes LLM); las decisiones humanas no fueron observables durante la ejecución (registradas como pendientes — el patrón exacto del Plan 114); la pierna `pytest` tiene la clase ambiental preexistente de permisos del sandbox (los tests content-sensitive pasan); sin medición de tokens/tiempo.
- **Fuera de este cierre (declarado, no iniciado):** la feature Protocol-native Jury Trial — FUTURE / NOT STARTED / OUT OF SCOPE; sin diseño, sin RFC/ADR/Plan, sin artefactos. El conocimiento del MVP DEV queda disponible como input de una futura decisión del mantenedor.
