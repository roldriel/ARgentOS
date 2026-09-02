# Plan 97 — Implementación de la Unidad C (Incremento 2): findings, corrections, lineage formal `F-n`/`C-n`, revalidación, pending decisions y formatos para el Change Lifecycle DEV

> **Naturaleza de este documento.** Este es el **tercer Implementation Plan
> ejecutable** derivado del Master Action Plan 94. Implementa la **Unidad C =
> Incremento conceptual 2** de RFC-75: operacionalizar para artifacts nuevos
> los mecanismos de **findings** (refs calificadas `<artifact>:F-<n>` y
> estados), **corrections** (registro de provenance `C-<n>` y alcance de
> revalidación), **lineage formal** `F-n`/`C-n`, **revalidación** integrada al
> modelo A1/A2 de la Decisión B, **pending decisions** per-artifact (PC-1),
> **condiciones no resueltas**, **lineage post-close**, continuidad de
> provenance y las **estructuras documentales** (formato estable) que el
> Incremento 4 consumirá como datos. No rediseña RFC-75 ni Plan 94: deriva, no
> reinterpreta (`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`).
> El cambio es **exclusivamente documental** (gobernanza DEV, templates y
> registro), sin cambios en `protocol/.agents/`, `runtime/`, `tools/`,
> `tests/`, VERSION ni `dist/`; no produce `VERSION` bump ni tag (docs-only,
> RFC-69; `docs/rfc/69-documentation-taxonomy-and-layout.md:Versionado`). No
> implementa el Incremento 4 (checkers, enforcement, registries, métricas
> operacionales) ni el Incremento 5 (handoff/coordinación).
>
> **La presente iteración es solo de creación/registro del plan**: crea este
> archivo y su registro en `docs/plans/INDEX.md`; **no ejecuta el plan**, no
> modifica ninguna fuente normativa, no crea Plan 98 y no adelanta trabajo del
> Incremento 4. Estado esperado al cierre de esta iteración:
>
> ```text
> Plan 97 = Aprobado para ejecución (PLANNED / OPEN)
> Implementation = NOT STARTED
> Executed = NO
> Committed = NO (sin commit en esta iteración; registro en el working tree)
> Closed = NO (condición derivada)
> Released = NO
> ```

**Status:** Aprobado para ejecución (plan creado y registrado; ejecución NO
iniciada — gates de autorización humana y aceptación de cierre pendientes, ver
§26)
**Fecha:** 2026-09-02
**RFC:** RFC-75 (`docs/rfc/75-change-lifecycle.md`)
**Clase:** — (no toca `protocol/.agents/`; cambio docs-only según
`docs/VERSIONING.md:3. Versionado`)
**Change Level:** L2 (clasificación prospectiva de dogfooding, declarada al
crear el plan; ver §20)
**Depende de:** RFC-75 `Accepted` (`docs/rfc/75-change-lifecycle.md`); ADR-15
`Accepted` (`docs/adr/15-change-lifecycle-continuity.md`); ADR-16 `Accepted`
(`docs/adr/16-change-lifecycle-authority.md`); RFC-46 `Accepted`; RFC-56
`Accepted`; RFC-69 `Accepted`; Plan 94 `Executed` (2026-09-02, `3acf439`);
Plan 95 `Executed` (2026-09-02, `bc21978` + `865e3ad` + `dc7425f`); Plan 96
`Executed` + condición derivada `Closed` (docs-only; C1 `9e4192f` + C2
`9844cf5`); Decisión B (`fc52c88`, semántica A1/A2/closure PASS);
**Planning Report v2** del Plan 97 (diseño de trabajo aprobado por el
mantenedor, 2026-09-02; no versionado en el repo — artefacto de sesión).
**Origen:** Solicitud explícita del mantenedor (2026-09-02): transformar el
Planning Report v2 de la Unidad C en el artifact formal de Plan 97,
registrado y listo para ejecución posterior, **sin implementar** el Incremento
2, sin avanzar al Incremento 4 y sin ejecutar commits en esta iteración.

---

## Convención de evidencia

Este documento distingue, en cada conclusión importante, las marcas usadas por
los planes de la serie y compatibles con la convención del repositorio
(`docs/CONVENTIONS.md:Convenciones`):

| Marca | Significado |
|---|---|
| `OBSERVED` | Verificado en el repositorio (git, archivos, checkers, pytest). |
| `NORMATIVE` | Impuesto por RFC `Accepted`, ADR `Accepted`, plan aprobado o convención vigente. |
| `DERIVED` | Deducción necesaria a partir de evidencia citada. |
| `PROPOSED` | Elección operativa de este plan (formato de campos, wording, algoritmo de transición); no es normativa hasta ejecutarse. |
| `OPEN` | Decisión pendiente que no impide redactar/ejecutar el plan; requiere decisión humana o plan posterior. |
| `BLOCKER` | Contradicción que impide ejecutar la Unidad C (no se detectó ninguna; ver §29). |
| `UNKNOWN` | No verificable en el estado actual; se indica cómo resolverlo. |

Las afirmaciones sobre el estado actual del repo se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`). El Planning Report v2 no se cita como
`ruta:sección` porque no es un artifact versionado del repo: es el diseño de
trabajo aprobado (provenance de sesión) y este plan lo incorpora como insumo,
no como fuente normativa (ver §2).

## Contenido requerido → sección

| Requisito del encargo | Sección de este documento |
|---|---|
| Header / metadata | Header de este archivo |
| Objective | §1, §5 y §7 |
| Context | §3 y §4 |
| Authoritative Sources | §2 |
| Scope | §5 |
| Out of Scope | §6 |
| Preconditions | §3 y §22 (Fase F0) |
| Authority Model | §14 |
| Findings Model | §9 |
| Correction Model | §10 |
| F-n / C-n Lineage | §11 |
| Revalidation Model | §12 |
| Pending / PC-1 | §13 |
| Non-Retroactivity | §15 |
| Legacy Handling | §16 |
| Repository Changes | §17 |
| Verification Strategy | §18 |
| Dogfooding | §19 |
| Dependency Graph | §20 (grafo) |
| Acceptance Criteria | §21 |
| Execution Phases | §22 |
| Commit Boundaries | §23 |
| Recovery / Rollback | §24 |
| Risks | §25 |
| Open Questions | §26 |
| Exit Criteria | §27 |
| Traceability Matrix | §28 |
| Change Level | §20 |
| Veredicto / readiness | §29 |
| Validation anchor / Checkpoint / Nota de ejecución | Secciones finales (se completan al ejecutar) |

---

## 1. Resumen ejecutivo

**[NORMATIVE + DERIVED]** RFC-75 define el rollout incremental
`0 → {1,3} → 2 → 4` (`docs/rfc/75-change-lifecycle.md:Rollout incremental`) y
el Plan 94 agrupa ese rollout en unidades de implementación — A: Incremento 0;
B: 1+3 en batch operacional; C: 2; D: 4; Incremento 5 = Deferred / Future
Track (`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`).
La secuencia ejecutada está confirmada en el repo: **Plan 95 = Unidad A
(Incremento 0)**, **Plan 96 = Unidad B (Incrementos 1+3)**, **Plan 97 = Unidad
C (Incremento 2)** y **Plan 98 = Unidad D (Incremento 4)**
(`docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:30. Grafo de dependencias`;
`docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:39. Veredicto final`).
Este plan no altera esa numeración ni planifica el Incremento 4.

La Unidad C operacionaliza — **para artifacts nuevos**, no retroactivamente —
lo que RFC-75 dejó como semántica normativa: LC-1 (toda corrección enlaza a
origen y revalidación con ref calificada) y PC-1 (toda decisión pendiente
bloqueante persiste en el artifact que bloquea)
(`docs/rfc/75-change-lifecycle.md:Invariantes`), junto con CL-6/CL-7/CL-8 y
AU-1..AU-7 (`docs/adr/15-change-lifecycle-continuity.md:Invariantes`;
`docs/adr/16-change-lifecycle-authority.md:Invariantes`). El Plan 95 declaró
LC-1/PC-1 como "semántica objetivo" exigible desde sus incrementos respectivos
(`docs/plans/95-change-lifecycle-unit-a-increment-0.md:8. Observability baseline (Incremento 0)`);
el Incremento 2 es el que las vuelve operativas sin crear maquinaria.

**Veredicto de este artifact:** **PLAN 97 READY FOR IMPLEMENTATION — GO WITH
CONDITIONS** (§29). Condiciones reales (ninguna de diseño, ninguna inventada):

- **C1** — autorización humana para ejecutar la Unidad C y para los commits
  C1/C2 en `dev` (§26 OQ-6).
- **C2** — aceptación humana de la batería al cierre según la política de
  "batería verde" (`docs/plans/94-change-lifecycle-master-action-plan.md:24.1 Política de interpretación de "batería verde"`).
- **C3** — decisión humana sobre el backfill opcional G1 / plan 91 (fuera de
  alcance por defecto; §16 y §26 OQ-1).
- **C4** — decisión humana sobre OPEN-4 (sufijo del header de RFC-75) y sobre
  registrar la Decisión B en el Amendment Log de RFC-75 (§26 OQ-2/OQ-3).
- **C5** — sin elevación de ADR candidates en esta Unidad (§26 OQ-4).

Este artifact se crea y registra en esta iteración; el estado de ejecución es
`NOT STARTED` (ver "Naturaleza de este documento").

## 2. Autoridad e insumos

**[DERIVED]** Orden de precedencia aplicado (repo factual > normativa
`Accepted` > planes ejecutados > convenciones > diseño de trabajo > inferencia
del agente):

1. **Estado factual actual del repositorio** (§3): git, checkers, artifacts.
2. **RFC-75** `Accepted`: Mecanismo 8 (findings/corrections/revalidation,
   refs `<artifact>:F-<n>`, estados, N:M, post-close), Mecanismo 9 (pending
   decisions per-artifact), Mecanismo 10 (clases de autoridad), Mecanismos
   12–15 (post-close, observabilidad, automatización, legacy), Invariantes
   (LC-1/PC-1) y rollout incremental.
3. **ADR-15**: CL-6 (corrección preserva provenance y declara alcance de
   revalidación), CL-7 (resultado trazable), CL-8 (registros no eliminados;
   resolución conserva evidencia), CL-9 y CL-10.
4. **ADR-16**: AU-1..AU-7; clases FACTUAL/NORMATIVE/DECISION/RELEASE/
   DESCRIPTIVE.
5. **RFC-46**: principio de no retroactividad y trazas históricas no
   reescribibles (`docs/rfc/46-historical-trace-policy.md:Decisión propuesta`).
6. **RFC-56**: clases A/B/C y vía de autorización de payload
   (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`); no aplica a
   este plan (no toca `protocol/.agents/`).
7. **RFC-69**: taxonomía documental y versionado docs-only
   (`docs/rfc/69-documentation-taxonomy-and-layout.md:Versionado`).
8. **Plan 94** `Executed`: §8 (autoridad por transición), §12.1 (no crear
   artifacts nuevos; checkers → Incremento 4), §18/§18.1 (Unidad C y regla
   "refs/pending solo aplican cuando existen"), Implementation Unit C (scope,
   out of scope, dependencies, migration, validation, dogfooding, exit,
   rollback, enables).
9. **Plan 95** `Executed`: regla transversal target semantics vs
   operationalización (LC-1/PC-1 exigibles desde el Incremento 2) y schema
   baseline de la métrica finding lineage coverage.
10. **Plan 96** `Executed` + `Closed`: formato v1 de Validation Anchor/SCI y
    checkpoint; asignación de numeración (Plan 97 = Unidad C).
11. **Decisión B** (`fc52c88`): A1/A2, validez relativa al anchor, consistencia
    de cierre contra el anchor del estado de cierre, PASS anclado antes de
    `Closed`; el lineage formal `F-n` llega con el Incremento 2.
12. **`docs/CONVENTIONS.md`**, **`docs/VERSIONING.md`**, **`AGENTS.md`** raíz y
    **`docs/AGENTS.md`**: hogar normativo/operativo donde se materializará la
    Unidad C.
13. **Planning Report v2** del Plan 97 (2026-09-02): diseño de trabajo
    aprobado y auditado; **no normativo**; no reemplaza RFC/ADR/planes. Este
    plan incorpora sus conclusiones verificadas (v2 §7–§27) sin rediseñarlas.

Regla de conflicto: si durante la ejecución aparece una contradicción real
entre este plan y una fuente normativa, el ejecutor **no resuelve
unilateralmente**: documenta la contradicción, se detiene si afecta la
ejecutabilidad y marca `HUMAN DECISION REQUIRED` (AU-3;
`docs/rfc/75-change-lifecycle.md:Mecanismo 10 — Authority / Conflict Resolution`).

## 3. Estado actual del repositorio (reconstrucción factual)

**[OBSERVED]** Verificado al crear este plan (2026-09-02, read-only sobre el
repo):

| Dato | Valor | Evidencia |
|---|---|---|
| Branch / HEAD | `dev` / `fc52c88` (Decisión B) | `git status`, `git log` |
| vs `origin/dev` | ahead 9, sin push | `git status` |
| Working tree | limpio antes de esta iteración | `git status` |
| VERSION | `10.3.0` | `protocol/.agents/VERSION` |
| Plan 94 | `Executed` (`3acf439`), sin `Closed` formal | INDEX + git log |
| Plan 95 | `Executed` (`bc21978` + `865e3ad` + `dc7425f`) | INDEX + git log |
| Plan 96 | `Executed` + `Closed` docs-only (`9e4192f` + `9844cf5`) | INDEX + git log |
| Plan 97 / Plan 98 | no existen antes de esta iteración | `Test-Path`, INDEX, git log |
| RFC-75 / ADR-15 / ADR-16 | `Accepted`, intactos | docs + INDEX |
| RFC-75 Amendment Log | entradas de creación y del plan 96; **sin entrada de Decisión B** | `docs/rfc/75-change-lifecycle.md:Amendment Log` |
| Batería canónica (checkers) | 6 checkers PASS en `fc52c88` (warnings esperados de `dev`) | corrido (ver §18) |
| pytest | `340 passed, 0 failed` (reportado en `fc52c88`, fuera del sandbox por ACL) | reporte Decisión B |
| Uso actual de refs lifecycle `F-n`/`C-n` | ninguno en artifacts; solo semántica en RFC-75 Mec. 8 | `rg` |
| Uso actual de pending PC-1 | ninguno; CONVENTIONS lo declara semántica objetivo | `rg` |
| Históricos bare `F-xx` (bitácora 19, auditorías F1–F7, backlog) | namespaces distintos, legítimos; no lifecycle | `rg` |

**Precondiciones de ejecución (F0):** el estado de §3 debe sostenerse al
ejecutar (branch `dev`; planes 94/95/96 en su estado ejecutado; Decisión B
commiteada; árbol limpio salvo los cambios del propio plan); la batería de §18
corre en verde o con desviación documentada aceptada por el mantenedor (§26
OQ-6 / C2).

## 4. Declaración del problema

**[NORMATIVE + DERIVED]** RFC-75 documenta el problema que esta Unidad resuelve
en la frontera operacional: validaciones sin lineage reproducible (G1),
findings/correcciones sin lineage, decisiones humanas pendientes solo en
conversación y correcciones sin trazabilidad
(`docs/rfc/75-change-lifecycle.md:Problema`). Tras los Incrementos 0 y 1+3 el
repo tiene operativa la semántica de condiciones derivadas, el anchor v1
(VC-1), el intake fallback con Change Level y el checkpoint/cierre (GC-1)
(`docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:Validation anchor`),
pero los mecanismos de **findings/corrections/revalidación formal** y de
**pending decisions** siguen siendo solo texto normativo de RFC-75: no existe
regla operacional en `docs/CONVENTIONS.md`, ni estructura en los templates, ni
formato determinista que el Incremento 4 pueda verificar. El problema concreto
de la Unidad C es esa brecha entre **semántica** y **operacionalización
documental** (mapa de aplicabilidad de la regla transversal
`docs/CONVENTIONS.md:Regla transversal — target semantics vs operationalización`).

## 5. Alcance (incluido)

**[NORMATIVE + PROPOSED]** El Plan 97 operacionaliza, para artifacts **nuevos**
creados bajo estas reglas (no retroactivo, §15):

- **Findings** con refs calificadas `<artifact>:F-<n>` y estados de metadata
  (LC-1; RFC-75 Mec. 8).
- **Corrections** con registro de provenance `C-<n>`, ref a finding(s) de
  origen y alcance de revalidación declarado (CL-6/CL-7).
- **Lineage formal** `F-n`/`C-n` con namespace por artifact (sin namespace ni
  registry globales).
- **Revalidación** integrada al modelo A1/A2 de la Decisión B (A2 referencia
  A1; A1 nunca se muta).
- **Pending decisions** per-artifact (PC-1) y **condiciones no resueltas**
  (decisiones pendientes, findings abiertos/diferidos y post-close) con
  metadata requerida.
- **Post-close lineage** por referencia (Mec. 12): la acción nueva referencia
  al artifact cerrado; `Closed` no se reabre.
- **Continuidad de provenance** (CL-9): decisiones que sobreviven a su Plan
  conservan lineage.
- **Estructuras documentales necesarias** para estos mecanismos: subsecciones
  operativas en `docs/CONVENTIONS.md`, secciones/guías en los templates de Plan
  y RFC, campos/estado de filas en `docs/VERSIONING.md` (§10/§11), alineación
  del `AGENTS.md` raíz y entrada de materialización en el Amendment Log de
  RFC-75 (§17).
- **Preparación de formatos** que consumirá el Incremento 4 (estructura
  determinista de refs, estados, metadata de pending y lineage), **sin**
  implementar los checkers del Incremento 4 (§6).

Debe respetar y citar: LC-1, PC-1, CL-6, CL-7, CL-8, CL-9, CL-10, AU-1..AU-7 y
el modelo A1/A2 de la Decisión B (§9–§14 y §28).

## 6. Fuera de alcance (exclusiones absolutas)

**[NORMATIVE]** El Plan 97 **no** incluye implementación de:

- Incremento 4 (lifecycle checkers, automatización/enforcement mecánico de
  findings o pending, métricas operacionales, verificación mecánica de
  formatos); puede aparecer **solo** como DEPENDENCY / FUTURE CONSUMER (§20).
- Finding registry, Change registry, Series registry, lifecycle database,
  universal tracker o global Change state machine.
- Entidad global de Finding, de Pending o de Correction (RFC-75 Mec. 8/9: sin
  entidad arquitectónica).
- Runtime, orchestration runtime, protocol payload, nuevas skills.
- Cambios en `protocol/.agents/` (Clase: —; RFC-56) y en `dist/`.
- Release automation, `VERSION` bump o tags (docs-only, RFC-69).
- Edición de `docs/adr/*`, de los Planes 94/95/96, de RFC-46/56/69 o de
  artifacts históricos (§15).
- Modificación de `docs/AGENTS.md` salvo evidencia explícita de necesidad
  (por defecto permanece sin cambios; §17 P10).
- Tests/pytest nuevos (el alcance documental no los requiere; §18).

Soporte: Plan 94 Unidad C — Out of scope (tracker condicional, entidades
Finding/Correction/Decision, checkers del Incremento 4)
(`docs/plans/94-change-lifecycle-master-action-plan.md:Implementation Unit C — Incremento 2 (conceptual): Findings, correcciones, revalidación y pending`);
Plan 94 §12.1 (crear nuevo: ninguno por ahora; script opcional solo si la
observabilidad lo justifica, Incremento 4)
(`docs/plans/94-change-lifecycle-master-action-plan.md:12.1 Clasificación de artifacts`).

## 7. Unidad C — alcance del Incremento 2 (conceptual)

**[DERIVED]** La Unidad C implementa exactamente el Incremento 2 conceptual de
RFC-75, sin absorber ni renumerar otros incrementos:

| Campo | Contenido (de Plan 94 Unidad C) |
|---|---|
| Increment | 2 |
| Objective | Preservar lineage finding→corrección→revalidación con refs calificadas `<artifact>:F-<n>` (LC-1) y estados; N:M; alcance de revalidación por corrección; pending per-artifact con dueño/escalación/resolución (PC-1); tabla de post-close. |
| Problem solved | G1 sin lineage; decisiones humanas solo en conversación; correcciones sin trazabilidad. |
| Scope | `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, template de Plan (sección findings/pending), RFC-75 Mec. 12 como referencia normativa. |
| Out of scope | Tracker global (condicional); entidades Finding/Correction/Decision; checkers (Incremento 4). |
| Mechanisms | Convención de refs y estados; campos de pending; tabla post-close. |
| Dependencies | Unidades A y B (incrementos 0 y 1+3: cierre y anchors definidos). |
| Migration | Legacy sin refs válido; discriminador de ausencia; backfill opcional de G1 y de la decisión del plan 91. |
| Validation | Batería + caso de uso real (el primer pending/finding real que surja). |
| Dogfooding | Los planes 95+ usan refs `F-n` y pending; este plan es el primer consumidor real (§19). |
| Rollback | Revertir commits; refs nuevas pasan a legacy. |
| Enables | Unidad D (Incremento 4: checkers de refs/pending) y métricas de lineage con datos reales. |

Fuente: `docs/plans/94-change-lifecycle-master-action-plan.md:Implementation Unit C — Incremento 2 (conceptual): Findings, correcciones, revalidación y pending`.

**Incremento 2 es exclusivamente documental** (demostrado en §17): la
verificación requisito → componente no identifica código, tools ni tests
necesarios; la ausencia de código no es arbitraria — los checkers y la
automatización pertenecen al Incremento 4 por Plan 94 §12.1/§14 y por la
regla persist → observe → automate de RFC-75 Mec. 14
(`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`). Si durante la
ejecución un componente técnico resultara realmente obligatorio por una fuente
normativa, **no se introduce silenciosamente**: se marca `HUMAN DECISION
REQUIRED`.

## 8. Modelo semántico: ya decidido vs a implementar vs diferido

**[DERIVED]** Separación explícita para evitar convertir preferencias de
implementación en normativa:

| Concepto | Estado | Hogar |
|---|---|---|
| Refs `<artifact>:F-<n>`/`C-<n>`, namespace por artifact, estados de finding, N:M, post-close por referencia, sin entidades | NORMATIVE (ya decidido en RFC-75 Mec. 8/9/12) | RFC-75 |
| Autoridad por clases; agentes detectan/registran/escalan, no resuelven | NORMATIVE (ADR-16 AU-1..7; RFC-75 Mec. 10) | ADR-16 / RFC-75 |
| A1/A2; validez relativa al anchor; `Closed` exige PASS del estado de cierre | NORMATIVE (Decisión B, `fc52c88`) | `docs/CONVENTIONS.md` / `docs/VERSIONING.md` |
| Reglas operativas de findings/corrections/pending para artifacts nuevos (dónde se escribe, qué campos, cómo se registran) | A IMPLEMENTAR en esta Unidad (documental) | CONVENTIONS, templates, VERSIONING, AGENTS.md, Amendment Log de RFC-75 (§17) |
| Mecanismo concreto de preservación de histórico en transiciones de estado (in-place con notas vs append-only vs otra representación compatible) | IMPLEMENTATION DETAIL (se elige al ejecutar sin contradicción con CL-8; §26 OQ-8) | CONVENTIONS (texto resultante) |
| Formato exacto de refs (secuencialidad local, wording de labels) | CAN DECIDE IN PLAN (§26 OQ-7) | CONVENTIONS / templates |
| Verificación mecánica de formatos, unicidad, refs rotas, pending con owner | DIFERIDO al Incremento 4 (checkers) | tools/ (futuro Plan 98) |
| Tracker condicional, registries, métricas operacionales | DIFERIDO (Incremento 4 / decisión con datos) | — |
| Handoff/coordinación entre agentes | Incremento 5 — fuera de alcance | — |

## 9. Modelo de findings

**[NORMATIVE + PROPOSED]** Texto operativo que la ejecución escribirá en
`docs/CONVENTIONS.md` (P2 de §17), derivado sin reinterpretar RFC-75 Mec. 8:

### 9.1 Cuándo y quién

- Un **finding** aparece cuando un agente o un humano detecta un
  defecto/observación en ejecución, validación, auditoría de RFC, revisión
  post-close o revisión cross-artifact (RFC-75 Mec. 8/12).
- Quién lo produce: el agente que detecta (con evidencia) o el humano.
- El finding es un **registro factual / claim registrado**: existir no otorga
  autoridad normativa (RFC-75 Mec. 10; ADR-16 AU-3).

### 9.2 Elementos inmutables vs evolucionables

**Inmutables** (no se reescriben, CL-8; RFC-46):

- identity del finding (`<artifact>:F-<n>`);
- observación original;
- evidencia original;
- estado Git donde fue observado;
- provenance original (ref a validación/anchor, estado, cita).

**Evolucionables** (metadata de estado, preservando histórico):

- estado (`open`, `partially-resolved`, `resolved`, `deferred`, `superseded`);
- resolución, resolución parcial, diferimiento, supersession y reapertura.

El mecanismo concreto para preservar el histórico — metadata actual con
histórico, modelo append-only u otra representación compatible — es
**IMPLEMENTATION DETAIL** (§8, §26 OQ-8): ninguna fuente prescribe una única
forma; la ejecución elige una representación que no contradiga CL-8 (registros
no eliminados; resolución conserva evidencia) ni invente política nueva.

### 9.3 Estados

Estados exclusivos respaldados por RFC-75 Mec. 8: `open`,
`partially-resolved`, `resolved`, `deferred` (con owner/destino) y
`superseded` (sustituido/duplicado; **≠ resolved**; nunca borrado silencioso).
Reapertura: RFC-75 sanciona **ambas** alternativas — un finding nuevo que
referencia al original **o** metadata `reopened`; el plan no obliga a una sola.

### 9.4 Evidencia y relación con Git

- El finding referencia la validación/anchor que lo descubrió, el estado Git y
  la cita `ruta:sección` cuando aplica.
- Describe un estado; la resolución ocurre en estados posteriores anclados
  (modelo A1/A2, §12).
- Cardinalidades (RFC-75 Mec. 8): 1 F → N C; N F → 1 C; 1 C → N revalidaciones
  (N:M explícito).

## 10. Modelo de corrección

**[NORMATIVE]** La ejecución conservará explícitamente esta separación (la
autoridad que autoriza la acción, el registro de que ocurrió, la evidencia
factual y la decisión de resolución son cuatro cosas distintas):

```text
Plan aprobado
    ↓
autorización normativa de la acción (NORMATIVE; RFC-75 Mec. 5; Plan 94 §8)
    ↓
Correction C-<n>  (registro de provenance / traceability; ADR-15 CL-6)
    ↓
registro de provenance / traceability (refs a finding(s) de origen)
    ↓
Git / commit / state (FACTUAL; ADR-16 AU-1)
    ↓
validation / revalidation (FACTUAL PASS; Plan 94 §8)
    ↓
decisión de resolución (DECISION humana con evidencia; ADR-16 AU-3; CL-8)
```

Reglas operativas que la ejecución escribirá:

- **`C-<n>` NO es una fuente normativa.** La acción puede estar autorizada
  normativamente por el Plan aprobado; el registro `C-<n>` es factual/de
  provenance. No se vuelve a clasificar `C-<n>` como NORMATIVE.
- Toda corrección preserva provenance hacia su origen/finding y declara su
  **alcance de revalidación** (CL-6).
- El resultado de revalidación es trazable a la corrección y a su origen
  (CL-7).
- No toda corrección es "nueva implementación": la distingue la ref a
  finding(s) de origen y el alcance de revalidación declarado.
- Efecto sobre validaciones previas: no invalida automáticamente (CL-2); si la
  corrección modifica el estado scoped relevante del contrato, aplica el modelo
  A1/A2 (revalidación antes de `Closed`; Decisión B); una corrección documental
  sin efecto scoped puede no requerir revalidación (§12).

## 11. Lineage formal `F-n` / `C-n`

**[NORMATIVE + PROPOSED]** Formato y reglas (RFC-75 Mec. 8 es la única fuente
normativa del formato):

| Aspecto | Regla |
|---|---|
| Formato | `<artifact>:F-<n>` y `<artifact>:C-<n>` (p. ej. `PLAN-97:F-01`, `PLAN-97:C-01`) |
| Namespace | pertenece al artifact que posee el registro; **no existe namespace global** |
| Registry | **no existe registry global** de findings ni corrections; los registros viven en su artifact |
| Autoridad | el número es locator de registro; **no otorga autoridad normativa** (ADR-16) |
| Históricos bare `F-xx` | namespaces históricos distintos (bitácora 19, auditorías F1–F7, backlog); **no se migran automáticamente** ni se mezclan con el lifecycle |
| Refs cross-artifact | posibles y legítimas (p. ej. `PLAN-94:C-01` → `PLAN-91:F-03`, ejemplo normativo de RFC-75 Mec. 8) |
| Numeración local/secuencial | si no está normativamente definida, queda como IMPLEMENTATION DETAIL (§26 OQ-7) |
| Unicidad | por artifact: `PLAN-97:F-01` no colisiona con `RFC-75:F-01`; dentro del mismo artifact no se duplica |
| Legacy | la ausencia de refs = legacy, no invalidez (RFC-75 Mec. 15) |

Los históricos bare `F-xx` no se convierten en refs lifecycle ni se reescriben:
son traza de otros namespaces (`docs/plans/94-change-lifecycle-master-action-plan.md:23. Deuda existente y hallazgos no bloqueantes`).

## 12. Modelo de revalidación (A1/A2 + F/C)

**[NORMATIVE]** Relación conceptual que este plan materializa (sin modificar la
Decisión B):

```text
Finding F-<n>
    ↓
Correction C-<n>
    ↓
estado posterior S2
    ↓
Revalidation V2
    ↓
Anchor A2
    ↓
evidencia
    ↓
resolución / elegibilidad de cierre
```

Reglas que la ejecución escribirá de forma explícita:

- **No toda revalidation requiere finding** (Decisión B define revalidación
  como re-ejecución del mismo contrato sobre un estado nuevo; precedente real:
  V2 del plan 96 sin finding).
- **No toda correction requiere revalidation** (CL-2 + Decisión B: mismo
  estado → nota sin A2; solo cambio scoped relevante → A2).
- Si una corrección modifica el validated state relevante, aplica el modelo
  A1/A2: **A2 referencia A1; A1 nunca se muta**; A2 es un registro nuevo con su
  propio anchor sobre S2.
- **Validaciones históricas nunca se reescriben** (RFC-46; RFC-75 Mec. 15;
  CL-8).
- A2 puede citar `C-<n>`/`F-<n>` cuando la revalidación responde a una
  corrección (CL-7 exige resultado trazable; que cite es IMPLEMENTATION
  DETAIL).
- **Plan 96 permanece intacto**: su anchor V1/A1 (tree
  `b8add7d74a41b907627b7faa4f10909af599ef2b`, delta
  `a818ed4ffe683faad9cde368f4a0718112f40f62983c63d1e459dcdd947a0d14`) y su
  checkpoint no se modifican ni reinterpretan; las reglas nuevas rigen solo
  registros futuros (§15/§16).

## 13. Pending decisions / PC-1

**[NORMATIVE + PROPOSED]** La ejecución tratará Pending como **decisión
pendiente per-artifact** (registrada en el artifact que posee la decisión, con
refs a los artifacts bloqueados; sin entidad `Decision`)
(`docs/rfc/75-change-lifecycle.md:Mecanismo 9 — Pending Decisions`). No es:
lifecycle state, entidad global, finding ni checker output.

Metadata requerida (normativa en RFC-75 Mec. 9): `blocking/no-blocking`,
`owner`, `escalación`, `resolución`, `evidencia`, `efecto downstream` y
`ADR-worthiness`. Reglas:

- **PC-1**: toda decisión pendiente **bloqueante** persiste en el artifact que
  bloquea; nunca desaparece. La persistencia obligatoria alcanza a las
  bloqueantes; las no-bloqueantes con owner se registran igualmente con su
  metadata.
- Si el owner se supersede/elimina/cierra → transferir al sucesor o escalar al
  humano; **nunca desaparece**. Si dos artifacts reclaman ownership → el humano
  decide con refs a todos los reclamantes (AU-3).
- La determinación de materialidad/blocking corresponde a **autoridad humana**
  cuando la normativa así lo determine (Plan 94 §8; ADR-16 AU-3); el agente
  registra, propone y escala, no resuelve unilateralmente.
- La resolución se registra con decisión + evidencia + artifacts afectados en
  el artifact dueño y en el registro del pendiente.

Matriz de no-confusión (cada concepto conserva su modelo; no se mezclan):

| Concepto | Naturaleza | ¿Bloquea derivar `Closed`? | Autoridad |
|---|---|---|---|
| Pending (PC-1) | decisión pendiente per-artifact | sí si blocking sin resolución/owner; no si no-blocking con dueño | resolución = humana |
| Finding `open` | estado de metadata de un finding | un open sin resolución/diferimiento → sí según matriz de governance; diferido con destino/owner → no | humana |
| Warning | salida informativa de checkers existentes | no | factual/informativa |
| GAP | evidencia faltante (p. ej. "anchor missing", RFC-75 Mec. 14) | no decide por sí; bloquea *derivación* de `Closed` cuando falta evidencia requerida | evidencia |
| FAIL | resultado de validación/checker (violación mecánica) | sí, como evidencia (batería en rojo no permite cerrar) | factual |
| Observation | finding no bloqueante registrado como observación (RFC-75 Mec. 3) | no | humana (registro) |

Nota: la frase "pending bloqueante impide `Closed`" es **operacionalización**
consistente con PC-1 y la matriz de governance, no una regla normativa nueva.

## 14. Modelo de autoridad

**[NORMATIVE]** La ejecución conservará la siguiente tabla (sin delegar
autoridad a registros):

| Elemento | Autoridad |
|---|---|
| RFC/ADR aceptado | NORMATIVE |
| Plan aprobado | NORMATIVE |
| Finding | FACTUAL / claim registrado |
| Correction `C-<n>` | FACTUAL / traceability (registro; la **acción** es NORMATIVE por el Plan aprobado) |
| Git state | FACTUAL |
| Validation / Revalidation | FACTUAL |
| Resolución humana | DECISION |
| Release / tag | RELEASE |
| INDEX | DESCRIPTIVE (nunca autoritativo; AU-4) |
| Checker output futuro (Incremento 4) | FACTUAL / evidence |

Regla transversal: `checker output = factual evidence ≠ normative authority`
(RFC-75 Mec. 10/14). Los agentes detectan, registran, proponen y escalan; **no
resuelven unilateralmente** decisiones humanas (AU-3; Plan 94 §8).

## 15. No retroactividad

**[NORMATIVE]** Regla explícita que la ejecución debe respetar:

- No se modifica retrospectivamente: Plan 94, Plan 95, Plan 96, RFC/ADR
  históricos, anchors históricos, validations históricas ni evidencia
  histórica.
- **La Decisión B no se proyecta retroactivamente sobre el Plan 96**: el V2 del
  plan 96 registrado sin bloque A2 completo es histórico pre-Decisión B y
  permanece como está (legacy, §16).
- No se fabrican: findings históricos, A2 históricos, corrections históricas ni
  evidence histórica.
- El legacy permanece legacy; los escenarios sintéticos de verificación no se
  convierten en findings reales (§18/§19).

Soporte: RFC-46 (`docs/rfc/46-historical-trace-policy.md:Decisión propuesta`);
RFC-75 Mec. 15 (`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`);
ADR-15 CL-8 (`docs/adr/15-change-lifecycle-continuity.md:Invariantes`).

## 16. Legacy / migración

**[NORMATIVE]** Reglas que la ejecución escribirá (RFC-75 Mec. 15):

- **Ausencia de campos nuevos = legacy, no invalidez** (discriminador de
  ausencia).
- Los artifacts legacy pueden ser referenciados por artifacts nuevos; el legacy
  no se reescribe para cumplir metadata nueva.
- Plan 96: su anchor/checkpoint siguen verificándose (tree/delta reproducibles,
  §12); su V2 pre-Decisión B es histórico; su `Closed` no se reabre — findings
  futuros sobre él usan refs nuevas tipo `PLAN-96:F-0x` (Mec. 12, post-close
  por referencia).
- Backfill opcional (G1 / decisión del plan 91): solo con decisión humana, sin
  editar artifacts y sin fabricar registros (Mec. 15; Plan 94 Unidad C
  Migration); fuera de alcance por defecto (§26 OQ-1).
- Coexistencia de namespaces: los históricos bare `F-xx` conviven con las refs
  lifecycle calificadas sin migración ni mezcla (§11).

## 17. Cambios propuestos en el repositorio (solo al ejecutar)

**[PROPOSED]** Candidatos validados en el Planning Report v2 (§16) y en Plan 94
Unidad C/§12.1. **En esta iteración se ejecutan únicamente P1 (crear este plan)
y la parte de registro de P9 (fila inicial del INDEX)**; el resto se ejecuta
cuando el mantenedor autorice la Unidad C. Para cada archivo se declara:
motivo, requisito, fuente, cambio, dependencia, riesgo y verificación.

| # | Archivo | Motivo | Requisito / fuente | Cambio (al ejecutar) | Dependencia | Riesgo | Verificación |
|---|---|---|---|---|---|---|---|
| P1 | `docs/plans/97-change-lifecycle-unit-c-increment-2.md` | Crear el artifact formal del Plan 97 (Unidad C / Incremento 2) | Numeración cronológica; Plan 96 §30/§39 | **YA CREADO en esta iteración** | Planes 94/95/96; RFC-75 | Fuera de scope | `check_plan_structure`, `check_plan_citations` |
| P2 | `docs/CONVENTIONS.md` | Hogar normativo-operativo de LC-1/PC-1 | RFC-75 Mec. 8/9; Plan 94 Unidad C | Nuevas subsecciones `### Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`, `### Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)` y la integración con revalidación A1/A2 (§9–§13); actualizar el mapa de aplicabilidad de la regla transversal (LC-1/PC-1 pasan de "objetivo" a operativas para artifacts nuevos) | §9–§14 de este plan | Duplicar RFC-75 (mitigar: citar, no copiar) | citations + escenarios de §18 |
| P3 | `docs/plans/_TEMPLATE.md` | Estructura para que los planes nuevos registren findings/corrections/pending | RFC-75 Mec. 8/9; Plan 94 §12.1 (extender) | Sección opcional `## Findings / Correcciones / Pending` con el formato determinista del §11/§13 (solo si existen registros reales; sin marcadores obligatorios para legacy) | P2 | Placeholders o ambigüedad (mitigar: guía sin marcadores) | `check_plan_structure`, citations |
| P4 | `docs/rfc/_TEMPLATE.md` | Guía de findings/anchors por entrada del Amendment Log de RFC | RFC-75 Mec. 3/8 | Guía breve: cómo registrar refs `F-n`/`C-n` y anchors en entradas del Amendment Log | P2 | Ambigüedad de formato | citations + escenarios |
| P5 | `docs/VERSIONING.md` | DoD y schema de métricas alineados con el Incremento 2 | RFC-75 Mec. 13; Plan 95 §8 | §11: fila finding lineage coverage declara "campos existentes desde el Incremento 2; medición → Incremento 4"; §10 DoD: bullet para artifacts nuevos — findings/corrections/pending se registran cuando existen (LC-1/PC-1), legacy intacto | P2 | Schema ≠ medición (mitigar: texto explícito) | battery + `check_version_state` |
| P6 | `AGENTS.md` (raíz) | Entry point del repositorio alineado con la norma operativa | Plan 94 §12.1 (extender AGENTS.md raíz) | `## Task lifecycle`: párrafo indicando que los artifacts nuevos registran findings/corrections/pending con refs `F-n`/`C-n` y metadata PC-1 cuando existen; legacy intacto | P2 | Entry point en inglés desalineado | citations + lectura |
| P7 | `docs/rfc/75-change-lifecycle.md` | Materialización de la RFC que este plan implementa | Precedente plan 96 E14 | Entrada en `## Amendment Log`: "2026-09-02 — Incremento 2 materializado (plan 97): findings/corrections/revalidación formal y pending operativos para artifacts nuevos; legacy intacto" — **sin tocar el header** (OPEN-4 se escala, §26 OQ-2) | P2–P6 | Alterar RFC-75 (mitigar: solo Amendment Log) | citations |
| P8 | `CHANGELOG.md` | Traza docs-only obligatoria | RFC-69; DoD `docs/VERSIONING.md:10. Definition of Done` | Ítem `(plan 97, RFC-75)` en `[Unreleased]` al ejecutar/cerrar | P7 | Posición histórica de `[Unreleased]` (mitigar: insertar sin reordenar) | `check_version_state` |
| P9 | `docs/plans/INDEX.md` | Mirror mecánico obligatorio | `docs/AGENTS.md:INDEX y CONVENTIONS` | **YA REGISTRADO en esta iteración** con Status `Aprobado para ejecución`; al ejecutar se actualiza la fila a `Executed` + nota y descripción de cierre | P1 | Fila desactualizada (mitigar: espejo en el commit del plan) | `check_plan_structure` |
| P10 | `docs/AGENTS.md` | Sin cambio por defecto | Plan 94 ("docs/AGENTS.md si hace falta") | **Sin cambio**: no se detectó necesidad explícita; si surge durante la ejecución, escalar antes de tocar | — | Cambio innecesario | — |
| P11 | backfill G1 / plan 91 (opcional) | Notas de lineage no históricas | RFC-75 Mec. 15; decisión humana | Solo con decisión humana (§26 OQ-1); fuera de alcance por defecto | — | Fabricación retroactiva (mitigar: prohibido sin decisión) | revisión humana |

**No se tocan:** `docs/adr/*`, Planes 94/95/96, `protocol/`, `runtime/`,
`tools/`, `tests/`, VERSION, `dist/`. `docs/AGENTS.md` permanece sin cambios
(P10). Cualquier desviación de esta tabla durante la ejecución se documenta y,
si cambia el alcance aprobado, se marca `HUMAN DECISION REQUIRED`.

## 18. Estrategia de verificación

**[PROPOSED]** Como el alcance es documental, **no se crea pytest nuevo** en
esta Unidad (demostrado en §7/§17); la verificación es documental/manual sobre
los textos resultantes + la batería existente del repo
(`docs/VERSIONING.md:4.1 Batería canónica de verificación`). Los escenarios
sintéticos de esta sección **no se convierten en findings reales** del Plan 97
(§19).

### 18.1 Escenarios positivos

- `F-n` correctamente calificado con namespace por artifact (§11).
- `C-n` con provenance (ref a finding origen y alcance de revalidación; CL-6).
- N:M findings/corrections/revalidaciones expresado (1→N, N→1, 1→N).
- Revalidación con A2 propio; A2 referencia A1; A1 intacto.
- Pending con metadata requerida (blocking/no-blocking, owner, escalación,
  resolución, evidencia, efecto downstream, ADR-worthiness).
- `deferred` con owner/destino; `superseded` ≠ `resolved`.
- Post-close lineage: `PLAN-97:C-0n` → artifact cerrado y `F-0m` original.
- Namespaces independientes: mismo `F-01` en artifacts distintos sin colisión.
- "No findings detected / Not Applicable" cuando no existen registros reales.

### 18.2 Escenarios negativos / adversariales

- `F-n` sin artifact dueño del namespace.
- `C-n` sin finding cuando la corrección pretende resolver un finding.
- Lineage roto (ref que no resuelve).
- `F-n` duplicado dentro del mismo namespace/artifact.
- `C-n` presentado como autoridad normativa.
- Pending bloqueante sin resolución/ownership.
- Finding `resolved` sin evidencia.
- A2 que muta A1 o revalidación sin anchor.
- Cierre sin evidencia compatible (GAP de cierre).
- Modificación retroactiva del Plan 96 o de validaciones históricas.
- Corrección que cambia el validated state relevante sin revalidación
  (imposibilidad de derivar `Closed` sobre el estado final).
- Mezcla de modelos Pending/Finding/Warning/GAP/FAIL/Observation.

### 18.3 Escenarios boundary

- Corrección documental sin efecto scoped → sin revalidación obligatoria (nota
  sin A2).
- Multi-correction sobre un finding; multi-revalidación en cadena
  (A1 → A2 → A3, cada una referencia su origen sin mutar anteriores).
- Reapertura por finding nuevo y por metadata `reopened` (ambas permitidas).
- Ref cross-artifact válida; históricos bare `F-xx` intactos como traza.

### 18.4 Comandos y juicio

- Batería canónica existente (todos PASS, warnings esperados de `dev`):
  `python tools/check_protocol_invariants.py --payload protocol .`;
  `python tools/check_plan_citations.py`;
  `python tools/check_plan_structure.py`;
  `python tools/check_taxonomy_coherence.py`;
  `python tools/check_session_artifacts.py`;
  `python tools/check_version_state.py`.
- `python -m pytest tests/` como parte de la batería del cierre
  (baseline esperado `340 passed, 0 failed`; ruido ambiental de ACL del
  sandbox sobre el basetemp documentado — correr con permisos reales si
  aplica; política de desviación en Plan 94 §24.1).
- Juicio manual: revisión de los textos resultantes contra §9–§13, unicidad de
  namespaces, ausencia de placeholders y resolución de refs.
- `git diff --check`; `git status` limpio salvo los cambios del plan.

## 19. Dogfooding

**[PROPOSED]** El Plan 97 es el **primer consumidor real** del modelo que
operacionaliza. Distinción obligatoria de tipos de datos:

1. **Datos reales del Plan 97**: findings/pending/corrections que surjan
   durante su ejecución; únicos datos que forman parte del lineage real del
   plan (namespace `PLAN-97`). Si aparecen: `PLAN-97:F-01` /
   `PLAN-97:C-01`. Si no aparecen:
   `No findings detected / Not Applicable` (permitido por RFC-75 Mec. 8/13/15 y
   por Plan 94 §18.1: las refs/pending solo aplican cuando existen
   findings/decisiones; la frase es notación operacional PROPOSED, no
   normativa).
2. **Escenarios sintéticos de verificación** (§18): validan la documentación;
   **no se persisten** como registros del plan.
3. **Ejemplos normativos**: los de RFC-75 Mec. 8 (`RFC-74:F-01`,
   `PLAN-94:C-01` → `PLAN-91:F-03`) — ilustración, no datos del plan.
4. **Datos históricos**: G1, plan 91, trackers/bitácoras `F-xx` — evidencia de
   contexto; backfill solo con decisión humana y sin editar artifacts (§16).
5. **Datos futuros del Incremento 4**: no se producen en esta Unidad.

Secuencia de dogfooding al ejecutar: baseline (F0) → planificación/registro
(ya hecho) → autorización humana → implementación documental (P2–P8) →
detección (si aparece un finding real) → correction (si aplica) → validación
V1/A1 sobre el contenido de C1 → registros de lineage reales → C1 → registros
de cierre (anchor, checkpoint, INDEX, changelog) en C2 → revalidación V2/A2
sobre el contenido final → condición derivada `Closed` (docs-only). Anti-
circularidad: los mecanismos se materializan antes del cierre del propio plan;
la validación usa la batería existente + los escenarios de §18, sin checkers
nuevos; el plan no valida su propia existencia. **Esta iteración de creación no
dogfoodea mecánicamente nada**: no detectó findings reales
(`No findings detected / N/A` para la fase de creación).

## 20. Grafo de dependencias y Change Level

**[DERIVED]**

```text
RFC-75 (Accepted) ── rollout 0 → {1,3} → 2 → 4
   │
   ├─ ADR-15 (CL-1..10) ── hard
   ├─ ADR-16 (AU-1..7) ─── hard
   ├─ RFC-46 / RFC-56 / RFC-69 ── hard
   ▼
Plan 94 (MAP, Executed) ── hard (Unidad C = Incremento 2; §8/§12/§18)
   ▼
Plan 95 (Incremento 0, Executed) ── hard (regla transversal)
   ▼
Plan 96 (Incrementos 1+3, Executed + Closed) ── hard (formato v1; numeración)
   │      └─ Decisión B (fc52c88) ── hard (A1/A2; closure PASS)
   ▼
Plan 97 / Unidad C / Incremento 2  ◄── ESTE PLAN
   │
   ├─ future consumer: Plan 98 / Incremento 4 (formatos; no impone)
   ├─ historical: G1 (fcf6ce1), plan 91 (9dd8703) — soft/informational
   └─ historical namespaces: bitácora F-xx, auditorías F1–F7 — informational
```

Tipos: **hard** (bloqueante), **soft** (recomendado), **historical**
(evidencia), **informational** (contexto), **future consumer** (Incremento 4).
Serie: la membresía de este plan en la serie «Change Lifecycle» se deriva de la
relación `RFC: RFC-75` (la RFC declara `Serie: Change Lifecycle`); no requiere
campo `Serie:` propio ni registry
(`docs/CONVENTIONS.md:Change Lifecycle — Serie e identidad derivada (regla operacional; Incremento 1)`).

**Change Level:** aplicación del modelo de RFC-75 Mec. 2 y de la matriz
operacional del Plan 94 §9:

| Dimensión | Valor | Justificación |
|---|---|---|
| coordination | 1 | 1 agente, multi-sesión (diseño v2 y creación del plan en sesiones previas; ejecución y cierre en sesiones posteriores) |
| scope (superficie) | 1 | Área acotada: gobernanza/documentación DEV (CONVENTIONS, VERSIONING, templates, AGENTS.md, Amendment Log de RFC-75, INDEX, changelog); no toca runtime/tools/tests/protocol |
| architectural impact | 1 | Cambio documental aditivo y reversible; sin módulos nuevos ni seams |
| release impact | 1 | docs-only: ítem en `[Unreleased]`, sin `VERSION` bump ni tag (RFC-69) |
| duration/complexity | 2 | multi-sesión: redacción, registro, ejecución documental, dogfooding (anchor + checkpoint) y cierre exigen más de una sesión |

```text
Level = max(1, 1, 1, 1, 2) = 2  (L2)
```

Notas: Change Level ≠ clase RFC-56 (`Clase: —`); el número de commits no es
dimensión; L2 describe el cambio, no la machinery que instala (esta Unidad no
instala machinery: la instala el Incremento 4).

## 21. Criterios de aceptación

**[PROPOSED]** Cada AC indica evidencia, método de verificación, PASS y FAIL:

| ID | Requisito | Evidencia | Método | PASS | FAIL |
|---|---|---|---|---|---|
| AC-01 | `F-n` utiliza namespace por artifact | Texto P2 + registros reales del plan | Revisión + escenarios | Refs calificadas; unicidad por artifact | Ref sin artifact o duplicada en el mismo artifact |
| AC-02 | `C-n` representa provenance/traceability y no autoridad normativa | Texto P2 + registros del plan | Revisión del modelo (§10) | `C-<n>` con ref origen; texto explícito de no-autoridad | `C-n` presentado como NORMATIVE o sin provenance |
| AC-03 | Finding identity/observación original/provenance histórica no se reescriben | Reglas §9/§15 + textos P2 | Inspección | Inmutables declarados y respetados | Reescritura de lo inmutable |
| AC-04 | Las transiciones de estado preservan histórico | Reglas §9.2/§9.3 + textos P2 | Revisión/escenarios | Histórico preservado en toda transición | Transición que pierde histórico |
| AC-05 | Finding states coinciden con RFC-75 | Texto P2 | Revisión | Solo `open`/`partially-resolved`/`resolved`/`deferred`/`superseded` | Estados inventados |
| AC-06 | N:M findings/corrections/revalidations expresado | Texto P2 + escenarios §18 | Revisión | Cardinalidades Mec. 8 documentadas | Cardinalidades inventadas/omitidas |
| AC-07 | Pending sigue PC-1 y permanece per-artifact | Texto P2 + pendientes reales | Inspección | Registro con metadata y owner; bloqueantes persistidos | Pending sin owner, global o desaparecido |
| AC-08 | Pending/Finding/Warning/GAP/FAIL/Observation no se confunden | Matriz §13 + texto P2 | Revisión | Modelos diferenciados | Modelos mezclados |
| AC-09 | A2 referencia A1 sin mutarlo | Reglas §12 + registros | Inspección | A2 nuevo con ref; A1 intacto | A1 reescrito o A2 sin ref |
| AC-10 | No toda correction obliga revalidation y no toda revalidation requiere finding | Texto §12 + escenarios | Revisión | Reglas explícitas | Regla contraria o inventada |
| AC-11 | Plan 96 y artifacts históricos permanecen intactos | diff de la ejecución | `git diff` | Solo P1–P9 tocados; 94/95/96/ADR/RFC-46/56/69 intactos | Edición de artifacts históricos |
| AC-12 | No se introducen registries/entidades/global state machines | diff + trazabilidad §17 | Revisión contra §6 | Cero abstracciones globales | Entidad/registry/state machine nueva |
| AC-13 | Incremento 4 permanece fuera de scope | diff + texto §6 | Revisión | Cero checkers/código/tests | Invasión del Incremento 4 |
| AC-14 | El formato producido es determinista para automatización posterior | Texto P2–P4 | Revisión | Campos y refs documentados sin ambigüedad | Formato ambiguo |
| AC-15 | Dogfooding utiliza datos reales y no fabrica findings | Nota/registros de ejecución | Revisión | Registros reales o `No findings detected / N/A` | Findings/pending fabricados |
| AC-16 | El plan puede ejecutarse por otro agente sin reinterpretar la arquitectura | Este artifact (P1) | Lectura por agente independiente | Pasos/reglas autocontenidos (§17–§22) | Requiere reinterpretar fuentes |

Ningún AC exige comportamiento del Incremento 4, checker nuevo ni conversión de
decisión humana en regla automática.

## 22. Fases de ejecución

**[PROPOSED]** Fases que otro agente ejecutará **solo tras autorización humana**
(OQ-6/C1):

| Fase | Objetivo | Archivos | Dependencias | Verificación | Commit | Riesgo | Criterio de salida |
|---|---|---|---|---|---|---|---|
| F0 | Premisas: estado §3 + batería | — | §3 | Batería + pytest | — | Estado distinto al planificado | Verde + árbol limpio (o desviación aceptada) |
| F1 | Normativa operativa LC-1/PC-1 | CONVENTIONS (P2) | F0 | citations; escenarios §18 | C1 | Duplicación RFC-75 | Sin contradicción; mapa actualizado |
| F2 | Templates | `_TEMPLATE.md` planes/RFC (P3/P4) | F1 | structure/citations | C1 | Placeholders/ambigüedad | Guías sin marcadores; formato determinista |
| F3 | DoD / métricas / entry point | VERSIONING (P5), AGENTS.md (P6) | F1 | battery | C1 | DoD solo para artifacts nuevos | Legacy intacto; schema ≠ medición |
| F4 | Registro normativo | RFC-75 Amendment Log (P7), changelog (P8), INDEX (P9 final) | F1–F3 | structure/citations/version | C1/C2 | OPEN-4 aparte | Materialización + espejo |
| F5 | Dogfooding | Plan 97: Nota, registros reales, Validation anchor | F1–F4 | suite §18 + V1 | — | Fabricación | Registros reales o `No findings detected / N/A` |
| F6 | Cierre | Plan 97: Checkpoint; INDEX final | F5 | V2 + git | C2 | ACL pytest | `Closed` docs-only (derivado) |

Criterio de entrada (F0 checklist): Planes 94/95/96 en estado ejecutado;
Decisión B commiteada; Plan 98 NO existe ni se crea; este plan `Aprobado para
ejecución`; autorización humana de ejecución y de commits (OQ-6) registrada;
árbol limpio salvo los cambios del plan.

## 23. Límites de commits

**[PROPOSED]** Derivados del modelo GC-1/Decisión B y del precedente del plan
96 (`docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:Checkpoint`):

- **C1 (contenido):** P2–P8 aplicados, validado por V1 (batería + escenarios)
  antes del commit; mensaje convencional propuesto:
  `docs(repo): implement change lifecycle unit C semantics (plan 97, RFC-75)`.
- **C2 (registro/cierre):** Validation anchor, Checkpoint, registros reales de
  findings/pending (si existen), espejo final del INDEX y ítem del changelog;
  precedente `9844cf5`; mensaje propuesto:
  `docs(plans): record plan 97 validation anchor and checkpoint (plan 97, RFC-75)`.
- El registro de cierre **no embebe su propio SHA/tree** (auto-referencia
  excluida); la consistencia se verifica post-commit (`git rev-parse` del
  estado final contra el anchor del estado de cierre).
- Multi-commit permitido si emerge; el checkpoint lista C1…Cn y la consistencia
  se evalúa en el estado final.
- **En la iteración de creación NO se ejecuta ningún commit** (mandato del
  mantenedor, 2026-09-02): el registro queda en el working tree; si el
  mantenedor exige un commit de creación/registro, se crea aparte y antes de
  autorizar la ejecución, sin mezclarse con C1/C2.

## 24. Rollback / contención

**[PROPOSED]** Revertir C1/C2 en `dev`; los registros nuevos (findings,
pending, refs, anchors del plan) pasan a legacy si se revierte el mecanismo
(RFC-75 Mec. 15). Sin tags, `VERSION`, `dist` ni payload (docs-only). Archivos
compartidos (CONVENTIONS, VERSIONING, INDEX) se serializan
(`docs/VERSIONING.md:8. Ejecución en paralelo`). Hallazgos en F5/F6 →
detectar → escalar al mantenedor (AU-3); nunca resolver conflictos normativos
en el rollback.

## 25. Riesgos

**[DERIVED]**

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Interpretar `C-n` como normativo | Alto | §10/§14; AC-02 |
| Ambigüedad inmutabilidad vs evolución | Alto | §9.2/§15; AC-03/AC-04 |
| Scope leakage hacia Incremento 4 | Alto | §6/§17 demostración; AC-12/AC-13 |
| Retroactividad sobre Plan 96/legacy | Alto | RFC-75 Mec. 15; §15/§16; AC-11 |
| Duplicación terminológica `F-xx`/pending | Medio | §11/§13; namespaces explícitos |
| Ambigüedad blocking/materialidad | Medio | Matriz §13; determinación humana (AU-3) |
| Duplicación normativa RFC-75 ↔ CONVENTIONS | Medio | Citar, no copiar (P2) |
| Concurrencia en archivos compartidos | Medio | Serialización (VERSIONING §8) |
| ACL del sandbox en pytest | Bajo (ambiental) | Permisos reales; reporte honesto (Plan 94 §24.1) |
| Dogfooding sin findings → parecer incompleto | Bajo | `No findings detected / N/A` (AC-15) |

## 26. Preguntas abiertas y decisiones humanas

**[OPEN]** Solo decisiones realmente abiertas (no se convierten Implementation
Details en Human Decisions innecesarios):

| # | Pregunta / decisión | Tipo | Resolución propuesta |
|---|---|---|---|
| OQ-1 | ¿Backfillear G1 y la decisión del plan 91? | HUMAN | No por defecto; nota opcional autorizada (Mec. 15) |
| OQ-2 | ¿Ajustar el sufijo "implementación pendiente" del header de RFC-75? | HUMAN | Heredado (OPEN-4); fuera de P7; escalar sin decidir en el plan |
| OQ-3 | ¿Registrar la Decisión B en el Amendment Log de RFC-75? | HUMAN | Recomendado; nunca silencioso |
| OQ-4 | ¿Elevar ADR candidates (SCI, Change Level)? | HUMAN | Diferido al primer consumo (Plan 94 §22) |
| OQ-5 | ¿Activar tracker condicional de findings? | HUMAN (con datos) | Diferido a observabilidad (Incremento 4) |
| OQ-6 | Autorización de ejecución y de commits C1/C2; aceptación de cierre | HUMAN | Gates F0/F6 (§22/§23) |
| OQ-7 | Formato exacto de secciones/registros (bullets, labels, wording) | CAN DECIDE IN PLAN | Especificado en P2–P4 al ejecutar; sin nuevos requisitos normativos |
| OQ-8 | Mecanismo de registro de transiciones de estado de findings (in-place con notas vs append-only vs compatible) | IMPLEMENTATION DETAIL | Elegir en P2 sin contradicción con CL-8 (§9.2) |

Descartadas como decisiones humanas (se resuelven en la ejecución por
convención): idioma de cada documento (español en docs/gobernanza; inglés en
`AGENTS.md` raíz), nombre del archivo (P1 ya resuelto), numeración local
secuencial de refs (IMPLEMENTATION DETAIL, §11) y wording de la frase
`No findings detected / N/A` (notación operacional PROPOSED, §19).

## 27. Criterios de salida

Checklist específico del plan (complementa el DoD general de
`docs/VERSIONING.md:10. Definition of Done`, no lo reemplaza):

- [ ] Vía de autorización verificada (RFC-75 `Accepted`; este plan `Aprobado
      para ejecución`; autorización humana OQ-6 registrada antes de ejecutar).
- [ ] P2–P8 aplicados según §17; P10 sin cambios; cero archivos fuera de
      alcance en el diff (protocolo/runtime/tools/tests/ADR/planes 94/95/96/
      VERSION/dist).
- [ ] CONVENTIONS con subsecciones operativas (§9–§13) y mapa de aplicabilidad
      actualizado; sin duplicación normativa (citas a RFC-75).
- [ ] Templates de Plan y RFC con guía opcional de findings/corrections/pending
      sin placeholders ni obligaciones para legacy.
- [ ] VERSIONING §10/§11 alineados (schema ≠ medición); AGENTS.md raíz
      alineado.
- [ ] RFC-75 con entrada de materialización en su Amendment Log; header sin
      cambios; OPEN-4 escalado si surge.
- [ ] Ítem `(plan 97, RFC-75)` en `CHANGELOG.md:[Unreleased]`; INDEX espejo a
      `Executed` + nota.
- [ ] Dogfooding honesto: registros reales o `No findings detected / N/A`;
      escenarios sintéticos no persistidos.
- [ ] Batería canónica en verde o desviación documentada aceptada por el
      mantenedor (Plan 94 §24.1).
- [ ] Validation anchor y Checkpoint registrados (V1 sobre C1; V2 sobre el
      estado final antes de `Closed`) y condición derivada `Closed` (docs-only)
      declarada **solo al ejecutar**; esta iteración de creación no los
      completa ni declara `Executed`/`Closed`.

## 28. Matriz de trazabilidad

**[DERIVED]**

| Requisito | Fuente | Sección del Plan | Implementación futura | Verificación |
|---|---|---|---|---|
| RFC-75 Mec. 8 → findings/corrections/revalidation | `docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation` | §9–§12, §17 (P2/P3) | Refs en artifacts nuevos; verificación mecánica en Incremento 4 | Escenarios §18 + citations |
| RFC-75 Mec. 9 → Pending | `docs/rfc/75-change-lifecycle.md:Mecanismo 9 — Pending Decisions` | §13, §17 (P2) | Presencia/metadata en artifacts nuevos; checker de presencia en Incremento 4 | Inspección §13/§18 |
| ADR-15 CL-6/CL-7/CL-8 → provenance/revalidation/history | `docs/adr/15-change-lifecycle-continuity.md:Invariantes` | §10/§12/§15/§16 | Formatos P2–P4 | Escenarios positivos/negativos §18 |
| ADR-16 AU-1..AU-7 → autoridad | `docs/adr/16-change-lifecycle-authority.md:Invariantes` | §14 | Sin automatización de juicio humano | Revisión de autoridad |
| Decisión B → A1/A2 | `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`; `fc52c88` | §12, §23 | Consistencia de cierre (Incremento 4) | `git rev-parse`/SCI al cierre |
| Plan 94 Unidad C → scope | `docs/plans/94-change-lifecycle-master-action-plan.md:Implementation Unit C — Incremento 2 (conceptual): Findings, correcciones, revalidación y pending` | §5–§7, §17 | — | Diff contra §17 |
| Plan 96 → dependencia/numeración | `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:30. Grafo de dependencias` | §1/§7/§16/§20 | Plan 98 = Unidad D | INDEX + lectura |
| Incremento 4 → future consumer | `docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`; `docs/plans/94-change-lifecycle-master-action-plan.md:Implementation Unit D — Incremento 4 (conceptual): Automatización segura (gated en observabilidad)` | §6/§17/§20 | Checkers y métricas de refs/pending | Sin implementación en esta Unidad |
| No retroactividad / legacy | `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`; RFC-46 | §15/§16 | — | `git diff` + revisión |

## 29. Veredicto final

**[DERIVED]** Sin BLOCKER ni contradicción arquitectónica detectados: la
secuencia `Plan 95 (0) → Plan 96 (1+3) → Plan 97 (2) → Plan 98 (4)` está
confirmada en los artifacts ejecutados y en el rollout de RFC-75; el alcance de
la Unidad C está determinado por Plan 94 Unidad C; el Incremento 2 es
exclusivamente documental (demostrado, no asumido); los modelos de §9–§14
derivan de fuentes `Accepted` sin rediseño. Estado de este artifact al cierre
de la iteración de creación:

```text
Plan 97 = Aprobado para ejecución (PLANNED / OPEN)
Implementation = NOT STARTED
Executed = NO
Committed = NO (sin commit en esta iteración)
Closed = NO
Released = NO
```

**PLAN 97 READY FOR IMPLEMENTATION — GO WITH CONDITIONS** (condiciones
C1–C5, §1/§26). Próximo paso: autorización humana de ejecución (OQ-6) y
ejecución de las fases F0–F6 (§22) sobre `dev`; no se avanza al Incremento 4
ni se crea el Plan 98 en esta tarea.

---

## Validation anchor

Pendiente — se completa al ejecutar la Unidad C (Fase F5 de §22; regla
operacional VC-1 del Incremento 1,
`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`):
declared scope, validation command-set, effective inputs, observed
dependencies, environmental factors y Scoped Content Identity (state identity
por `git write-tree` y delta scoped identity) sobre el contenido validado de
C1. Esta iteración de creación no valida implementación alguna.

## Checkpoint / cierre

Pendiente — se completa al cerrar (Fase F6 de §22; regla operacional GC-1 del
Incremento 3,
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`):
commits de cierre C1/C2, estado validado (ref al Validation anchor), estado de
cierre (tree id), consistencia checkpoint↔anchor, governance aplicada y
condición derivada `Closed` (docs-only, sin release). Esta iteración **no**
cierra el plan.

## Nota de ejecución

Pendiente — se agrega al ejecutar (convención del template). Registro de esta
iteración (2026-09-02): Plan 97 creado y registrado en `docs/plans/INDEX.md`
(Vigésima novena serie; Status `Aprobado para ejecución`) a partir del Planning
Report v2 aprobado, sin ejecutar la Unidad C, sin commits y sin cambios fuera
del artifact del plan y su espejo en el INDEX. Resultado de los checkers
existentes al crear/registrar el plan: ver el reporte de creación entregado al
mantenedor.

