# Plan 100 — Continuación post-roadmap A–D: integridad de lineage del Change Lifecycle DEV (C-3 — lifecycle lineage checker, LC-1/CL-6/CL-7)

> **Naturaleza de este documento.** Este es el primer Implementation Plan
> ejecutable **posterior al roadmap A–D** de la serie Change Lifecycle DEV
> gobernada por RFC-75. No es una unidad histórica del roadmap A–D y no
> inventa un "Incremento 5": el roadmap original (planes 94–99, unidades
> A–D) está completo y el Plan 100 representa **nuevo trabajo de
> materialización posterior**, dentro de la misma serie, para automatizar una
> capacidad funcional especificada y aún no suficientemente materializada:
> la **integridad de lineage de findings/corrections/revalidación (LC-1)**,
> verificada por un checker determinista nuevo, **C-3 — lifecycle lineage
> checker** (`tools/check_lifecycle_lineage.py` + `tests/test_check_lifecycle_lineage.py`
> propuestos). La capacidad se materializa como mecanismo factual, advisory,
> DEV-only, read-only y sin autoridad normativa (ADR-16), sin entidades,
> registries, state machines, CI, runtime ni dependencias externas.
>
> **La presente iteración es solo de creación/registro del plan**: crea este
> archivo y su registro en `docs/plans/INDEX.md`; **no implementa** C-3, no
> modifica C-1/C-2, no modifica tests, no crea registros de findings/
> corrections/pending, no ejecuta commits y no modifica RFC-75, ADR-15,
> ADR-16 ni los Planes 94–99. Estado esperado al cierre de esta iteración:
>
> ```text
> Plan 100 = Aprobado para ejecución (PLANNED / OPEN)
> Implementation = NOT STARTED
> Executed = NO
> Committed = NO (sin commit en esta iteración; registro en el working tree)
> Closed = NO (condición derivada)
> Released = NO
> ```

**Status:** Executed
**Fecha:** 2026-09-02
**RFC:** RFC-75 (`docs/rfc/75-change-lifecycle.md`)
**Clase:** — (no toca `protocol/.agents/`; cambio DEV-only del repo fuente
sobre tooling y tests propios; sin `VERSION` bump ni tag; RFC-56 no aplica)
**Change Level:** L2 (clasificación prospectiva declarada al crear el plan;
ver §30)
**Depende de:** RFC-75 `Accepted` (`docs/rfc/75-change-lifecycle.md`); ADR-15
`Accepted` (`docs/adr/15-change-lifecycle-continuity.md`); ADR-16 `Accepted`
(`docs/adr/16-change-lifecycle-authority.md`); RFC-46 `Accepted`; RFC-56
`Accepted`; RFC-69 `Accepted`; Plan 94 `Executed`; Plan 95 `Executed`; Plan 96
`Executed` + condición derivada `Closed` (docs-only); Plan 97 `Executed` +
condición derivada `Closed` (docs-only); Plan 98 `Executed` + condición
derivada `Closed` (docs-only); Plan 99 `Executed` + condición derivada
`Closed` (docs-only, corrección post-close de F-1); Decisión B (`fc52c88`,
semántica A1/A2/closure PASS); estado factual del repositorio al 2026-09-02
(HEAD `51cabb2`, branch `dev`, working tree limpio; §3).
**Origen:** Solicitud explícita del mantenedor (2026-09-02): crear físicamente
el Plan 100 para continuar la materialización del Change Lifecycle DEV,
seleccionando con evidencia del repositorio la siguiente capacidad funcional
a implementar, **sin implementar** esa capacidad, sin cerrar el Plan y sin
adelantar cambios fuera del registro documental.

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
| `PROPOSED` | Elección operativa de este plan (especificación de implementación futura); no es normativa hasta ejecutarse. |
| `OPEN` | Decisión pendiente que no impide redactar/ejecutar el plan; requiere decisión humana o plan posterior. |
| `BLOCKER` | Contradicción que impide ejecutar la capacidad (no se detectó ninguna; ver §28/§32). |
| `UNKNOWN` | No verificable en el estado actual; se indica cómo resolverlo. |

Las afirmaciones sobre el estado actual del repo se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`). El C1/C2 Read-Only Audit Report (origen
de los findings F-1…F-9) no se cita como `ruta:sección` porque no es un
artifact versionado del repo: es provenance de sesión (insumo), no fuente
normativa (ADR-16 AU-4; §29).

## Contenido requerido → sección

| Requisito del encargo | Sección de este documento |
|---|---|
| Header / metadata e identidad | Header de este archivo |
| Naturaleza / esta iteración no implementa | Banner de apertura |
| Executive Summary | §1 |
| Historical Context | §2 |
| Current Repository Baseline | §3 |
| Problem Statement | §4 |
| Objective | §5 |
| Selected Functional Capability | §6 |
| Selection Rationale | §7 |
| Normative Basis | §8 |
| Current State | §9 |
| Target State | §10 |
| Scope | §11 |
| Out of Scope | §12 |
| Functional Specification | §13 |
| Data / Artifact Contract | §14 |
| Classification Semantics | §15 |
| Implementation Design | §16 |
| Test Strategy | §17 |
| Test Matrix | §18 |
| Dogfooding Strategy | §19 |
| Adversarial Scenarios | §20 |
| Governance Constraints | §21 |
| Change Lifecycle for Plan 100 | §22 |
| Validation Strategy | §23 |
| Anchor Strategy | §24 |
| Checkpoint Strategy | §25 |
| Acceptance Criteria | §26 |
| Commit Strategy | §27 |
| Recovery / Stop Conditions | §28 |
| Known Deferred Findings | §29 |
| Risks | §30 |
| Dependencies | §31 |
| Execution Gates | §32 |
| Closure Criteria | §33 |
| Post-Plan State | §34 |
| Traceability Matrix | §35 |

---

## 1. Resumen ejecutivo

**[NORMATIVE + DERIVED]** El roadmap A–D del Change Lifecycle DEV
(RFC-75) terminó con el cierre de Plan 99 (2026-09-02): Plan 94 (master
action plan), Plan 95 (Incremento 0), Plan 96 (Incrementos 1+3), Plan 97
(Incremento 2), Plan 98 (Unidad D / Incremento 4, materialización mínima de
automatización segura C-1/C-2) y Plan 99 (corrección post-close de F-1 en
C-2) están `Executed`, y los planes 96–99 alcanzaron la condición derivada
`Closed` (docs-only, sin release)
(`docs/plans/INDEX.md:Trigésima primera serie: Change Lifecycle DEV — Corrección post-close F-1 (C-2/GC-1) (02 sep 2026)`).
La automatización segura del Incremento 4 quedó **parcialmente** materializada
por diseño: Plan 98 automatizó únicamente C-1 (lifecycle anchor checker) y
C-2 (lifecycle checkpoint checker), y dejó explícitamente fuera la
automatización de findings/corrections (`F-n`/`C-n`), pending, stale, series y
métricas
(`docs/plans/98-change-lifecycle-unit-d-increment-4.md:6. Fuera de alcance (out of scope)`).

**[DERIVED]** El Plan 100 continúa esa materialización con la siguiente
capacidad que el estado factual del repositorio demuestra más madura y más
desbloqueante: **integridad de lineage de findings/corrections/revalidación
(LC-1/CL-6/CL-7)**, materializada como un checker determinista nuevo,
**C-3 — lifecycle lineage checker**. La selección se apoya en cuatro hechos
verificados (§3/§9): (a) existe corpus real del formato del Incremento 2 —
Plan 99 contiene la primera cadena completa de lineage
(`<PLAN-99>:F-1` → `<PLAN-99>:C-1` → revalidación V1/V2 → `resolved`) y Plan
98 contiene la declaración canónica de ausencia (`No findings detected /
N/A`); (b) no existe verificación mecánica determinista de ese formato y de
esas relaciones (Plan 94 §7 lo asignó al Incremento 4; Plan 98 lo difirió);
(c) la verificación no requiere resolver F-3 (duplicate validation records,
dominio de C-1) ni ninguna deuda F-2…F-9; (d) la capacidad habilita
verificaciones futuras de cierre/gobernanza (findings resueltos o diferidos
antes de `Closed`) y la métrica finding lineage coverage de RFC-75
(`docs/rfc/75-change-lifecycle.md:Mecanismo 13 — Observability`).

**Veredicto de este artifact:** **PLAN 100 READY FOR IMPLEMENTATION — GO WITH
CONDITIONS** (§32). Condiciones reales (ninguna de diseño, ninguna inventada;
ninguna bloquea esta iteración de creación):

- **C1** — autorización humana para ejecutar la capacidad y para los commits
  futuros en `dev` (§28/§31).
- **C2** — aceptación humana de la batería al cierre según la política de
  "batería verde" del plan 94 (§23/§26).
- **C3** — si al implementar aparece una ambigüedad de parseo del corpus o de
  semántica de registros (estado `reopened` como valor de `estado`, variantes
  de encabezado, refs no resueltas) no resoluble con las reglas de §14/§16,
  **STOP** y escalación humana; no se inventa regla (§28).
- **C4** — si la ejecución demuestra que el dogfooding del corpus real difiere
  de las invariantes de §19 (p. ej. GAP/ANOMALY nuevo sobre planes 98/99 no
  explicado por la semántica especificada), **STOP** antes del commit y
  escalación humana (§28).

Este artifact se crea y registra en esta iteración; el estado de ejecución es
`NOT STARTED` (banner de apertura).

## 2. Historical Context

**[NORMATIVE + DERIVED]** RFC-75 define el Change Lifecycle DEV con rollout
incremental `0 → {1,3} → 2 → 4` y un Incremento 5 (coordinación/handoff)
fuera de alcance, como track futuro deferido
(`docs/rfc/75-change-lifecycle.md:Rollout incremental`);
el Plan 94 agrupó el rollout en unidades de implementación A–D y registró el
catálogo de mecanismos futuros con su incremento: **LC-1 (findings/refs) →
"Checker de formato de refs (incremento 4)"** y **PC-1 (pending) → "Checker de
ownership/presencia (incremento 4)"**
(`docs/plans/94-change-lifecycle-master-action-plan.md:7. Mapeo RFC-75 → mecanismos`).
La Unidad D (Incremento 4) se definió como automatización segura "gated en
observabilidad": persistir primero, observar después, automatizar solo lo
observado como útil
(`docs/plans/94-change-lifecycle-master-action-plan.md:Implementation Unit D — Incremento 4 (conceptual): Automatización segura (gated en observabilidad)`).

Secuencia ejecutada verificada en el repo (§3): Plan 95 (Unidad A / Incremento
0), Plan 96 (Unidad B / Incrementos 1+3), Plan 97 (Unidad C / Incremento 2),
Plan 98 (Unidad D / Incremento 4 — C-1 + C-2 únicamente) y Plan 99 (corrección
post-close de F-1 en C-2). El Plan 99 registró además el primer uso real de la
maquinaria del Incremento 2: un finding (`<PLAN-99>:F-1`, `open` → `resolved`)
y una correction (`<PLAN-99>:C-1`) con refs origen, alcance de revalidación y
evidencia (secciones finales de
`docs/plans/99-change-lifecycle-f1-c2-gc1-correction.md`).

**[DERIVED]** Al terminar el roadmap A–D, la siguiente materialización del
Change Lifecycle DEV es **nuevo trabajo posterior**, no una unidad histórica:
el Plan 100 no se describe como "Incremento 5" ni como unidad del roadmap
A–D. Continúa, dentro de la serie Change Lifecycle DEV (RFC-75), los
candidatos de automatización que el Incremento 4 dejó diferidos, comenzando
por el de mayor madurez de datos y menor acoplamiento: el lineage
findings/corrections/revalidación (LC-1).

## 3. Current Repository Baseline

**[OBSERVED]** Verificado al crear este plan (2026-09-02, read-only sobre el
repo):

| Dato | Valor | Evidencia |
|---|---|---|
| Branch / HEAD | `dev` / `51cabb20ae34ed2d20100ddb386c358a3972bbfb` (plan 99: registro de anchor y checkpoint) | `git status`, `git rev-parse HEAD` |
| vs `origin/dev` | en sync (sin commits propios pendientes) | `git status --short --branch` |
| Working tree | limpio antes de esta iteración | `git status --porcelain` |
| VERSION del payload | `10.3.0` | `protocol/.agents/VERSION` |
| Plan 99 | `Executed` + condición derivada `Closed` (docs-only; corrección post-close F-1; `<PLAN-99>:C-1` registrado) | INDEX + archivo + git log |
| **Plan 100** | **no existe antes de esta iteración** | `Test-Path docs/plans/100*.md`, INDEX, git log |
| Último plan existente | 99 | `docs/plans/INDEX.md`; `rg --files docs/plans` |
| **Siguiente número libre** | **100** | secuencia cronológica de ejecución (`docs/CONVENTIONS.md:Convenciones`) |
| C-1 (anchor checker) | existe: `tools/check_lifecycle_anchor.py` + `tests/test_check_lifecycle_anchor.py` (19 escenarios) | git log, archivos |
| C-2 (checkpoint checker) | existe: `tools/check_lifecycle_checkpoint.py` + `tests/test_check_lifecycle_checkpoint.py` (29 escenarios: 21 + 8 regresiones F-1) | git log, archivos |
| RFC-75 / ADR-15 / ADR-16 | `Accepted`, intactos | docs + INDEX |
| Corpus del régimen del Incremento 2 | Plan 98 (`## Findings / Correcciones / Pending` con marcadores `No findings detected / N/A` y `N/A`); Plan 99 (mismo contenedor con `<PLAN-99>:F-1` y `<PLAN-99>:C-1` reales); Plan 97 (sin contenedor; pendings registrados en §26); legacy sin contenedor | `rg` + lectura de archivos |
| pytest (baseline reportado) | `388 passed, 0 failed` (registrado al cerrar Plan 99) | Plan 99 `Nota de ejecución` |
| Registries / entidades lifecycle | ninguno | `rg` |
| `.agents/` en raíz | **NO existe** | `Test-Path` |
| `protocol/.agents/` | existe; payload del Protocol, **fuera de scope** | estructura del repo |

**Precondiciones de ejecución (F0):** el estado de §3 debe sostenerse al
ejecutar (branch `dev`; planes 94–99 en su estado registrado; árbol limpio
salvo los cambios del propio plan); la batería de §23 corre en verde o con
desviación documentada aceptada por el mantenedor (Plan 94 §24.1).

## 4. Problem Statement

**[NORMATIVE + DERIVED]** El Incremento 2 (Plan 97) operacionalizó — para
artifacts nuevos — el formato documental de findings (`<artifact>:F-<n>`,
estados, N:M), corrections (`<artifact>:C-<n>` como registro factual de
provenance), revalidación y pending (LC-1/PC-1)
(`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`;
`docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`).
Ese formato ya produjo datos reales: el Plan 99 cerró con la primera cadena
completa de lineage (`<PLAN-99>:F-1` → `<PLAN-99>:C-1` → revalidación V1/V2 →
`resolved`, con `<PLAN-99>:C-1` registrado como traceability factual).

El problema concreto es la brecha entre **registro documental** (Incremento
2, estable y con datos reales) y **verificación mecánica determinista** de ese
registro. Hoy no existe ningún mecanismo que detecte de forma reproducible:

- refs mal formadas o en namespace ajeno al artifact (`<PLAN-98>:F-1` dentro
  del Plan 99, refs sin `PLAN-`/`RFC-`, números duplicados);
- estados de findings fuera del vocabulario documentado (`open`,
  `partially-resolved`, `resolved`, `deferred`, `superseded`);
- registros incompletos respecto de los elementos inmutables del finding
  (identidad, observación, evidencia original, estado Git observado,
  provenance original; CL-8/RFC-46);
- corrections sin provenance a origen (refs origen ausentes) o sin alcance de
  revalidación declarado (CL-6);
- contradicciones de resolución (finding `resolved` cuya resolución declara
  `FAIL`/`sin resolver`; resolución que referencia una correction inexistente
  en el corpus escaneado);
- declaraciones contradictorias de ausencia y presencia (marcador
  `No findings detected / N/A` junto a registros reales en la misma
  subsección).

Esa brecha fue el motivo por el que el Plan 99 requirió revisión humana
adversarial (el C1/C2 Read-Only Audit Report) para detectar F-1: la
verificación de lineage no está mecanizada. C-3 cierra la brecha **sin** crear
entidades, registries, state machines ni autoridad normativa
(`docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation`;
`docs/rfc/75-change-lifecycle.md:No-objetivos`).

## 5. Objective

**[DERIVED]** Objetivo del Plan 100: **materializar la verificación mecánica
determinista, factual y advisory de la integridad de lineage
findings/corrections/revalidación (LC-1/CL-6/CL-7)** sobre los artifacts del
repo DEV que registran findings/corrections bajo las reglas del Incremento 2,
de modo que:

- un agente de implementación pueda ejecutar el Plan 100 sin requerir otra
  ronda de auditorías conceptuales;
- el mecanismo sea pequeño, determinista, read-only, stdlib-only, sin Git en
  v1 y sin autoridad normativa (GAP ≠ invalidación; ANOMALY solo ante
  contradicción verificable);
- la capacidad se demuestre sobre el corpus real (Plan 98 ausencia declarada,
  Plan 99 cadena real) y sobre fixtures adversariales;
- no dependa de resolver F-3 ni ninguna deuda F-2…F-9;
- no introduzca infraestructura innecesaria ni decisiones arquitectónicas
  ocultas (sin RFC/ADR nuevos; RFC-75/ADR-15/16 intactos).

## 6. Selected Functional Capability

**[DERIVED + PROPOSED]** Capacidad seleccionada: **B — integridad de lineage
de Findings/Corrections/Revalidation (LC-1)**, materializada como el checker
determinista **C-3 — lifecycle lineage checker**:

- archivo propuesto: `tools/check_lifecycle_lineage.py`;
- tests propuestos: `tests/test_check_lifecycle_lineage.py`;
- dominio (v1): subsecciones `### Findings` y `### Correcciones` del contenedor
  `## Findings / Correcciones / Pending` en planes numerados de
  `docs/plans/` (el formato y los registros del Incremento 2; §14);
- verifica forma, completitud mínima y consistencia de los registros de
  findings/corrections/revalidación según §13–§16, preservando la distinción
  de clases de autoridad (FACTUAL/NORMATIVE/DECISION/RELEASE/DESCRIPTIVE):
  el checker produce evidencia factual, nunca autoridad normativa ni decisión
  humana (ADR-16 AU-1/AU-3/AU-5).

La capacidad **no** es una nueva unidad del roadmap A–D ni el Incremento 5:
es continuación post-A–D de la automatización segura que el Incremento 4
dejó diferida para el formato de refs (Plan 94 §7) y cuyo gate de
observabilidad quedó satisfecho por los datos reales del Plan 99 (§7).

## 7. Selection Rationale

**[DERIVED]** Las capacidades candidatas del encargo (A: validation
integrity; B: findings/corrections; C: pending; D: lifecycle composition)
se evaluaron con los criterios del encargo y la evidencia del repo (§3/§9):

| Criterio | B — lineage findings/corrections/revalidación (elegida) | A — validation integrity | C — pending (PC-1) | D — lifecycle composition |
|---|---|---|---|---|
| 1. Dependencia (desbloquea) | Alta: habilita la derivación futura de `Closed` con findings resueltos/diferidos (matriz de governance) y la métrica finding lineage coverage (RFC-75 Mec. 13) | Media: profundiza C-1; no desbloquea otra capacidad nueva | Media: sirve a continuity/handoff (track futuro), no al loop implement→validate→correct | Baja: depende de la madurez de todos los checkers previos |
| 2. Valor funcional | Alto: verifica el único eslabón del lifecycle (corregir/revalidar) sin verificación mecánica hoy | Bajo incremental: C-1 ya cubre forma/completitud mínima de anchors | Medio: decisiones pendientes con metadata; corpus sin pending bloqueante real | Bajo hoy: meta-vista; solapa con INDEX/métricas |
| 3. Madurez normativa | Alta: RFC-75 Mec. 8 + ADR-15 CL-6/7/8 + CONVENTIONS LC-1 + template + corpus real | Media: abarca el dominio de C-1 y roza la deuda F-3 | Alta: RFC-75 Mec. 9 + CONVENTIONS PC-1 | Media: requiere definir semántica de composición nueva (riesgo de decisión arquitectónica) |
| 4. Riesgo | Bajo: parser acotado al formato documentado; ambigüedad → GAP; sin Git | Medio: solapa con findings diferidos F-2…F-9 del dominio de C-1 | Bajo | Medio-alto: riesgo de infraestructura/meta-mecanismo no mínimo |
| 5. Scope | Pequeño: 1 tool + 1 suite + registros de cierre | Medio: requiere decidir qué invariantes nuevas verificar | Pequeño | Mayor: composición de N checkers + reporte derivado |
| 6. Dogfooding | Alto: corpus real con cadena completa (Plan 99) y ausencia declarada (Plan 98) | Medio: corpus de anchors ya cubierto por C-1 | Bajo: 13 pendings reales, todos no-bloqueantes; sin caso PC-1 bloqueante para dogfood | Bajo: sin sujeto real adicional |
| 7. No dependencia de F-3 | Sí: verifica registros F/C; F-3 (duplicate validation records) es dominio de C-1 y no bloquea | No del todo: colinda con F-3 | Sí | Sí, pero depende de C-1/C-2 con F-3 abierto |
| 8. Continuidad | Alta: materializa lifecycle (tooling) en lugar de solo documentación | Media | Media | Media |

**Conclusión:** B es la capacidad con mejor combinación dependencia × valor ×
madurez × riesgo × scope × dogfooding × no-F-3 × continuidad para ser el Plan
100. La evidencia decisiva es la existencia de una **cadena real completa** de
lineage (Plan 99) más la declaración canónica de ausencia (Plan 98): el gate
persist → observe → automate que Plan 98 aplicó a C-1/C-2 (dos pares
anchor/checkpoint reales antes de automatizar) queda satisfecho para el
formato de refs con datos reales.

### 7.1 Alternativas rechazadas (resumen)

- **A — Validation integrity (ampliar C-1):** rechazada. C-1 ya verifica
  forma/completitud/consistencia mínima de Validation Anchors; profundizarla
  colinda con la deuda conocida F-3 (duplicate validation records, dominio de
  C-1) y con los findings diferidos F-2…F-9, cuyo detalle no está versionado
  en el repo (§29). No es la capacidad menos acoplada al momento de elegir.
- **C — Pending (PC-1):** diferida. El corpus tiene pendings reales
  (planes 98/99) pero todos **no-bloqueantes y resueltos**; el núcleo de PC-1
  (persistencia de un pending **bloqueante** en el artifact que bloquea) no
  tiene sujeto real de dogfooding. Es candidata natural de un Plan posterior
  (un checker PC-1), no del Plan 100.
- **D — Lifecycle composition:** rechazada. Requiere madurez previa de los
  checkers individuales (incluido el lineage de este Plan), solapa con vistas
  derivadas/INDEX y métricas, y su especificación mínima exige decisiones de
  semántica de composición que no están autorizadas; riesgo de infraestructura
  no mínima.
- **E — otra capacidad:** no se identificó con evidencia del repo una
  capacidad más fundamental que B para el siguiente paso.

## 8. Normative Basis

**[NORMATIVE]** Fuentes que este Plan implementa sin modificar:

| Fuente | Regla relevante |
|---|---|
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation` | refs calificadas `<artifact>:F-<n>`/`C-<n>`; N:M; estados; post-close por referencia; sin entidad Finding |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 9 — Pending Decisions` | pending per-artifact (fuera del dominio v1 de C-3; §12) |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors` y `Mecanismo 7 — Git Checkpoints` | contenedores que C-3 consulta solo como evidencia declarada de revalidación (§16) |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation` | checker output = evidencia factual ≠ autoridad; GAP ≠ invalidación |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy` | ausencia de campos/contenedor = legacy, no invalidez; sin backfill |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 13 — Observability` | finding lineage coverage como consumidor futuro de C-3 |
| ADR-15 `docs/adr/15-change-lifecycle-continuity.md:Invariantes` | CL-6 (provenance + alcance de revalidación), CL-7 (resultado trazable), CL-8 (registros no eliminados), CL-10 (escala por impacto) |
| ADR-16 `docs/adr/16-change-lifecycle-authority.md:Invariantes` | AU-1…AU-7; clases FACTUAL/NORMATIVE/DECISION/RELEASE/DESCRIPTIVE; checker factual |
| CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)` | formato, estados, inmutables, N:M, no-confusión con `F-xx` bare legacy |
| CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)` | frontera conceptual Pending ≠ finding ≠ GAP ≠ FAIL (aplica al diseño de C-3) |
| CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)` | formato de anchor que C-3 consulta para evidencia de revalidación |
| CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)` | evidencia de PASS de checkpoint como soporte declarado de revalidación |
| VERSIONING `docs/VERSIONING.md:7. Estados de planes y RFCs` y `10. Definition of Done` | condición derivada `Closed`; findings/pending resueltos o diferidos para artifacts nuevos |
| RFC-46 / RFC-56 / RFC-69 | trazas históricas; clases de payload (no aplica); taxonomía/docs-only |
| Plan 94 `docs/plans/94-change-lifecycle-master-action-plan.md:7. Mapeo RFC-75 → mecanismos` y `docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental` | candidato "Checker de formato de refs (incremento 4)"; roadmap A–D terminado; trabajo posterior |
| Plan 98 `docs/plans/98-change-lifecycle-unit-d-increment-4.md:8. Población del Change Lifecycle regime` y `docs/plans/98-change-lifecycle-unit-d-increment-4.md:14. Autoridad` | población estructural por señales; checker factual/advisory; GAP vs ANOMALY |

Este Plan **no** crea RFC ni ADR, no enmienda RFC-75 y no modifica ADR-15/16:
la capacidad implementa normativa existente (LC-1/CL-6/CL-7) ya operacional
para artifacts nuevos desde el Incremento 2.

## 9. Current State

**[OBSERVED]** Estado específico del dominio que C-3 automatizará:

- **Formato normativo-operativo:** CONVENTIONS LC-1 (Incremento 2) define
  refs calificadas, estados (`open`, `partially-resolved`, `resolved`,
  `deferred` con owner/destino, `superseded`), elementos inmutables del
  finding, cardinalidades N:M y el rol factual de `C-<n>`
  (`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`).
- **Template:** `docs/plans/_TEMPLATE.md` define el contenedor opcional
  `## Findings / Correcciones / Pending` con las subsecciones `### Findings`,
  `### Correcciones` y `### Pending decisions`, y el marcador de ausencia
  `No findings detected / N/A` (archivo `docs/plans/_TEMPLATE.md`).
- **Corpus real con contenedor:**
  - Plan 98: `### Findings` → `No findings detected / N/A`; `### Correcciones`
    → `N/A`; `### Pending decisions` → OQ-1…OQ-8 no-bloqueantes (registro
    completo en `docs/plans/98-change-lifecycle-unit-d-increment-4.md`, sección
    final).
  - Plan 99: `### Findings` → `<PLAN-99>:F-1` (`resolved`, con `estado
    previo: open`, observación, evidencia original, estado Git observado,
    provenance original y resolución); `### Correcciones` → `<PLAN-99>:C-1`
    (refs origen `<PLAN-99>:F-1`, origen histórico Plan 98, alcance de
    revalidación con V1/V2, evidencia con commit `42da250`); `### Pending
    decisions` → OQ-1…OQ-5 no-bloqueantes (sección final de
    `docs/plans/99-change-lifecycle-f1-c2-gc1-correction.md`).
  - Plan 97: **sin contenedor**; sus pendings no-bloqueantes quedaron en §26
    (patrón de registro previo a la consolidación del contenedor; legacy
    válido, no invalidez).
  - RFC-75 Amendment Log: sin registros `F-n`/`C-n` aún.
- **Verificación mecánica:** C-1/C-2 existen y verifican anchors/checkpoints;
  **no existe** checker de refs/lineage ni de pending. F-3 (duplicate
  validation records) permanece `open` como deuda diferida del dominio de C-1
  (§29).

## 10. Target State

**[PROPOSED]** Estado objetivo al cerrar el Plan 100 (ejecución futura):

- existe `tools/check_lifecycle_lineage.py` (C-3): clasifica cada plan
  numerado de `docs/plans/` como `EXCLUDED`, `BOUNDARY`, `N/A`, `VALID`,
  `GAP` o `ANOMALY` según el contrato de §14/§15;
- existe `tests/test_check_lifecycle_lineage.py` con la matriz de §18 en
  verde;
- el dogfooding sobre el corpus real es consistente: Plan 98 → `N/A` (ausencia
  declarada), Plan 99 → `VALID` (cadena real completa), planes 96/97 y legacy
  01–95 → `EXCLUDED`, `ANOMALY=0`, `GAP=0` (§19);
- el Plan 100 queda `Executed` + condición derivada `Closed` (docs-only, sin
  release) con su propio Validation Anchor y Checkpoint (§24/§25), sin
  modificar RFC-75/ADR-15/16, C-1/C-2, Planes 94–99, `protocol/.agents/` ni
  `.agents/` en la raíz;
- la verificación de lineage es re-ejecutable y determinista: misma entrada →
  misma salida; GAP advisory nunca invalida; ANOMALY solo ante contradicción
  verificable; salida factual (ADR-16).

## 11. Scope

### 11.1 Esta iteración de planificación (incluido ahora)

**[PROPOSED — esta iteración]** Creación física del Plan 100 en
`docs/plans/100-change-lifecycle-lineage-integrity.md` y su registro en
`docs/plans/INDEX.md` (Trigésima segunda serie del INDEX; requisito
estructural del mirror, `tools/check_plan_structure.py`). No implementa C-3,
no ejecuta commits y no modifica ninguna fuente normativa ni de código
(secciones finales sin anchor/checkpoint fabricados).

### 11.2 Ejecución futura del plan (incluido entonces; NO se ejecuta ahora)

**[PROPOSED — Future Implementation]** La ejecución autorizada del Plan 100
implementa **exclusivamente**:

- **C-3 — Lifecycle Lineage Checker**: archivo propuesto
  `tools/check_lifecycle_lineage.py`;
- tests propuestos: `tests/test_check_lifecycle_lineage.py`;
- comportamiento según §13–§16;
- registros documentales de gobernanza del propio plan al ejecutar: este
  artifact (secciones finales de Validation Anchor/Checkpoint/registros),
  `docs/plans/INDEX.md` (espejo) y `CHANGELOG.md:[Unreleased]` (ítem
  `(plan 100, RFC-75)`; precedente planes 95–99). **Sin** entrada en el
  Amendment Log de RFC-75 (precedente planes 98/99: cambio tools/tests-only).

### 11.3 Excluido incluso en la ejecución futura

Resumen de exclusiones absolutas; detalle completo en §12. En particular, la
ejecución futura **no** agrega C-3 a la batería canónica de
`docs/VERSIONING.md:4.1 Batería canónica de verificación`, no crea CI, no
verifica pending (`### Pending decisions` queda fuera del dominio v1), no
introduce registries/state machines/métricas y no toca `protocol/`,
`runtime/`, `.agents/`, `dist/` ni el harness.

## 12. Out of Scope

**[NORMATIVE]** El Plan 100 **no** incluye, ni en esta iteración ni en su
ejecución futura:

- **F-3** (duplicate validation records): deuda conocida del dominio de C-1;
  no se resuelve, no se implementa incidentalmente y no se cierra por
  interpretación (§29);
- F-2…F-9 del C1/C2 Read-Only Audit Report: deferidos (§29);
- verificación mecánica de **pending decisions (PC-1)** — la subsección
  `### Pending decisions` no se parsea ni se clasifica en v1 (candidata de un
  Plan posterior, no inventado aquí);
- ampliación de C-1 (validation integrity) ni modificación de C-1/C-2 y sus
  tests;
- lifecycle composition (vista/derivación del estado operativo de un Change);
- stale detection, series automation, métricas operacionales (finding lineage
  coverage se consume como dependencia futura, no se instrumenta);
- modificación de RFC-75 (incluido su Amendment Log), ADR-15, ADR-16;
- modificación o reapertura de Planes 94–99 (historia, status, anchors,
  checkpoints, findings/corrections, commits);
- creación de registros `F-n`/`C-n`/pending en esta iteración (solo al
  ejecutar y solo si surgen registros reales);
- incorporación de C-3 a la batería canónica o a CI;
- runtime/orchestrator, skills, registry, base de datos, state machine
  global, servidor, API, framework o dependencia externa;
- modificación de `protocol/.agents/` ni creación de `.agents/` en la raíz;
- cambio de `VERSION`, creación de release/tag, promoción a `master`, push;
- verificación Git de evidencia de correcciones (los claims de commit/tree en
  `evidencia` son texto en v1; la resolución de locators pertenece a C-2;
  §16/§20);
- uso de "future work" como cajón de scope ambiguo: los pendings de
  §29/§31/§34 son decisiones abiertas reales con owner/escalación.

## 13. Functional Specification

**[PROPOSED — Future Implementation]** C-3 — lifecycle lineage checker:

### 13.1 CLI / tool

- Nombre: `tools/check_lifecycle_lineage.py`; invocación:
  `python tools/check_lifecycle_lineage.py [--root REPO_ROOT]`.
- Argumentos: `--root` (ruta al repo; default: padre del directorio del
  script), idéntico a C-1/C-2.
- Exit codes: `0` salvo que exista al menos un `ANOMALY`; `1` si hay uno o
  más. `GAP`, `BOUNDARY`, `N/A`, `EXCLUDED` y `VALID` nunca producen exit
  code no-cero (GAP advisory; RFC-75 Mecanismo 14).
- stdout: reporte determinista por artifact:
  `- <rel>: <classification> — <reason(s)>`, y línea de resumen
  `Summary: N plans inspected; EXCLUDED=…, BOUNDARY=…, N/A=…, VALID=…, GAP=…, ANOMALY=…`.
- stderr: sin salida en operación normal; errores de lectura no recuperables
  se reportan y terminan con código `2` documentado en el docstring (sin
  red ni escrituras).
- Determinismo: escaneo ordenado (rutas relativas ordenadas), sin
  dependencias de orden de filesystem, sin reloj, sin red, sin git en v1;
  ejecuciones repetidas sobre la misma entrada producen salida idéntica.
- Read-only: no escribe archivos ni invoca comandos que muten estado; sin Git
  en v1 (§16).
- Dependencias: stdlib y herramientas ya presentes; sin dependencias externas.

### 13.2 Semántica verificada (v1)

C-3 verifica **forma, completitud mínima y consistencia interna** de los
registros de findings y corrections del Incremento 2 (§14). No verifica:
veracidad semántica de observaciones, autoridad de resoluciones, transiciones
de estado históricas (salvo contradicciones explícitas), semántica de
reapertura (estado `reopened`), pending, ni la existencia física de commits/
trees citados como evidencia (§12/§16).

## 14. Data / Artifact Contract

**[PROPOSED — Future Implementation]** Contrato que C-3 consume y verifica:

### 14.1 Población (dominio)

- Artefactos: planes numerados con prefijo numérico y slug en minúsculas
  directamente bajo `docs/plans/`, excluyendo anexos (`-anexo-`) y
  `_TEMPLATE.md` (mismo criterio estructural que C-1/C-2; §8 de Plan 98).
- Señal de membresía del dominio de lineage: contenedor de nivel 2 con heading
  normalizado exacto `findings / correcciones / pending`.
- Señal de ambigüedad (BOUNDARY): refs calificadas lifecycle
  (`<PLAN-nn>:(F|C)-nn` o `<RFC-nn>:(F|C)-nn`) en el cuerpo del artifact sin
  contenedor.
- Legacy: artifact sin contenedor y sin refs calificadas lifecycle =
  `EXCLUDED` (ausencia de campos/contenedor = legacy, no invalidez; RFC-75
  Mecanismo 15). Los `F-xx` bare de bitácoras/auditorías históricas no son
  refs lifecycle y no afectan la clasificación.

### 14.2 Subsecciones y registros

- Subsecciones de nivel 3 dentro del contenedor: `### Findings` y
  `### Correcciones` (headings normalizados `findings` / `correcciones`).
  `### Pending decisions` **no** es dominio v1 (se ignora; §12).
- Registro de finding: bullet cuyo texto comienza con una ref calificada en
  backticks `` `<PLAN-nn>:F-<n>` `` (o variante `RFC-nn`) seguida de `—` o
  `:`. Campos `clave: valor` separados por `;` en el mismo bullet; las líneas
  de continuación indentadas pertenecen al mismo registro; el registro
  termina en el siguiente bullet o en el fin de la subsección.
- Registro de correction: idem con ref `` `<PLAN-nn>:C-<n>` ``.
- Marcadores de ausencia (sin registros): contenido visible de la subsección
  sin refs de registro que incluya el token `N/A` (formato del corpus:
  `` `No findings detected / N/A` ``; `` `N/A` ``). Comentarios HTML no son
  contenido.
- Vocabulario de campos (labels case-insensitive, prefijo más largo primero;
  el valor es el texto entre el `:` y el siguiente label o el fin del
  registro):
  - Finding — requeridos v1: `estado`, `observación`, `evidencia original`,
    `estado Git observado`, `provenance original`. Informacionales: `estado
    previo`, `severidad`, `clasificación`, `tipo`, `origin`, `source`,
    `resolución`, `owner`, `destino`.
  - Correction — requeridos v1: `refs origen` (con al menos una ref calificada
    `F-`), `alcance de revalidación`, `evidencia` (label puede aparecer como
    `evidencia (Git/commit/estado)`).
- Vocabulario de estados (valor de `estado` = primer token entre backticks, o
  primera palabra si no hay backticks): `open`, `partially-resolved`,
  `resolved`, `deferred`, `superseded`.

## 15. Classification Semantics

**[PROPOSED — Future Implementation]** Clasificación por artifact (precedencia
de severidad: ANOMALY > GAP > VALID > N/A > BOUNDARY > EXCLUDED), con la
semántica del encargo adaptada al dominio de lineage:

| Clase | Semántica en C-3 |
|---|---|
| `EXCLUDED` | Legacy: sin contenedor de lineage y sin refs lifecycle calificadas en el cuerpo |
| `BOUNDARY` | Ambigüedad estructural: refs lifecycle calificadas en prosa sin contenedor (revisión humana; no invalidez) |
| `N/A` | Miembro del dominio sin registros que verificar: contenedor con marcadores de ausencia declarados (o subsecciones vacías) |
| `VALID` | Registros presentes, completos y consistentes con el contrato de §14 |
| `GAP` | Información requerida ausente o no verificable; ambigüedad de parseo; claim sin soporte declarado (advisory; RFC-75 Mecanismo 14) |
| `ANOMALY` | Información presente pero incompatible (contradicción verificable; §16) |

La clasificación es evidencia factual, no autoridad: `GAP` nunca invalida un
registro y `ANOMALY` nunca decide gobernanza ni resolución humana (ADR-16
AU-1/AU-3/AU-5). La distinción FACTUAL/NORMATIVE/DECISION/RELEASE/DESCRIPTIVE
se preserva: C-3 solo reporta hechos del contenido (FACTUAL); no interpreta
`C-<n>` como fuente normativa (la acción la autoriza el Plan aprobado), no
decide resoluciones (DECISION) y no lee INDEX como autoridad (DESCRIPTIVE).

## 16. Implementation Design

**[PROPOSED — Future Implementation]** C-3 como módulo autocontenido (sin
imports cruzados entre tools; cada checker es independiente, precedente
C-1/C-2), stdlib-only, con funciones al estilo de C-1/C-2:

- escaneo de planes numerados y extracción de headings/secciones
  (helpers equivalentes a `is_numbered_plan`, `level2_headings`,
  `section_text`, `strip_comments`, `visible_content`);
- reglas de clasificación **R-L1-1…R-L1-12** (detalle abajo), con reporte de
  reasons agregables y determinista;
- sin invocación a git en v1; `--root` idéntico a C-1/C-2;
- docstring con semántica, población, clasificaciones, uso y advertencia de
  no-autoridad.

Reglas verificadas (v1; GAP advisory salvo indicación ANOMALY):

- **R-L1-1** — El registro de finding/correction abre con ref calificada en el
  namespace del artifact (`PLAN-<nn>` = número del archivo; p. ej.
  `docs/plans/99-…` → `PLAN-99`). Namespace distinto en el opener →
  `ANOMALY`.
- **R-L1-2** — Identidad duplicada en la misma subsección (mismo
  `<artifact>:F-<n>` o `<artifact>:C-<n>` dos veces) → `ANOMALY`.
- **R-L1-3** — Finding sin campo requerido (`estado`, `observación`,
  `evidencia original`, `estado Git observado`, `provenance original`) → `GAP`
  con detalle de campos faltantes.
- **R-L1-4** — `estado` fuera del vocabulario de §14 → `ANOMALY`
  (incompatible con el vocabulario documentado); el valor `reopened` como
  estado → `GAP` (ambigüedad documentada: reapertura por metadata/finding
  nuevo; semántica fuera de v1; revisión humana).
- **R-L1-5** — `resolved`/`partially-resolved` sin campo `resolución` → `GAP`;
  `resolución` que contiene `FAIL`, `sin resolver` o `no resuelto` →
  `ANOMALY` (contradicción con el estado).
- **R-L1-6** — `deferred` sin `owner` ni `destino` declarados → `GAP`.
- **R-L1-7** — `resolución` con ref calificada `C-` cuyo registro destino no
  existe en el corpus escaneado (planes numerados) → `ANOMALY`; ref destino en
  namespace `RFC-` → formato verificado, resolución fuera de dominio v1 (sin
  reason).
- **R-L1-8** — Correction sin `refs origen`, sin al menos una ref calificada
  `F-` en `refs origen`, o sin `alcance de revalidación`/`evidencia` → `GAP`;
  ref origen `F-` con registro destino inexistente en el corpus escaneado →
  `ANOMALY`; ref origen `RFC-` → formato verificado, sin resolución en v1.
- **R-L1-9** — Cuando una correction declara resultado de revalidación
  (vocabulario `A2`/`V2`/`revalidad…`/`revalidaci…`/`PASS`) y el artifact no
  declara evidencia de revalidación en su `## Validation anchor` (marker
  `A2`/`V2`/`revalidad…`/`revalidaci…`) ni `PASS` en su checkpoint → `GAP`
  (claim sin soporte declarado). Duplicados de registros de validación en el
  anchor no se resuelven ni se detectan (F-3): si la presencia de múltiples
  registros hace ambiguo el marker, el resultado es `GAP`, nunca un
  tie-break inventado.
- **R-L1-10** — Marcador de ausencia (`N/A`/`No findings detected`) junto a
  registros reales en la misma subsección → `ANOMALY` (declaración
  contradictoria). Contenido visible sin registros y sin marcador `N/A` →
  `GAP` (contenido no interpretable como registros ni como ausencia
  declarada).
- **R-L1-11** — Contenido de subsección no parseable (bullet sin ref
  calificada, estructura ambigua) → `GAP`, nunca `ANOMALY` por ambigüedad de
  parseo.
- **R-L1-12** — Clasificación del artifact: ANOMALY si alguna razón es
  ANOMALY; si no, GAP si alguna razón es GAP; si no, VALID si hay registros
  consistentes; N/A si solo hay ausencia declarada; BOUNDARY/EXCLUDED según
  §14.1. Exit code 1 solo con ANOMALY.

**Anti-circularidad:** C-3 deriva hechos solo de los contenedores de lineage
del artifact y de la sección `## Validation anchor` del mismo artifact (como
evidencia declarada de revalidación); nunca deriva validez de cierre ni
autoridad (R-L1-9; §21).

## 17. Test Strategy

**[PROPOSED — Future Implementation]** Suite `tests/test_check_lifecycle_lineage.py`
con pytest y `tmp_path` (sin red, sin git, sin archivos del repo real salvo el
test de dogfooding), estilo C-1/C-2:

- fixtures de repo mínimo: crear `docs/plans/` con artifacts sintéticos
  (textos de contenedores/registros) bajo `tmp_path`; correr `verify_all`/
  `format_report`/`main`;
- cobertura semántica: happy paths por estado y por tipo de registro; datos
  faltantes; datos malformados; datos conflictivos; artifacts legacy;
  boundary cases (estado `reopened`, refs `RFC-`, contenedor vacío);
  no-retroactividad (legacy sin contenedor nunca GAP/ANOMALY); determinismo
  (dos corridas idénticas); ejecución repetida; casos adversariales (§20);
  dogfooding sobre el repo real (§19);
- test de stdlib-only por AST (precedente C-1/C-2);
- test de exit codes (`GAP` → 0; `ANOMALY` → 1);
- los tests prueban semántica (clasificaciones y reasons), no cobertura de
  líneas.

## 18. Test Matrix

**[PROPOSED — Future Implementation]** Matriz concreta (ID, escenario, input,
expected, exit):

| ID | Escenario | Input | Expected | Exit |
|---|---|---|---|---|
| T01 | Finding `open` completo | Finding con ref `PLAN-99` + 5 requeridos + estado `open` | VALID | 0 |
| T02 | Finding `resolved` con resolución + correction destino existente | F-1 `resolved` + C-1 en `### Correcciones` + evidencia de revalidación en el anchor | VALID | 0 |
| T03 | Correction completa | C con `refs origen: F-1`, `alcance de revalidación`, `evidencia` | VALID | 0 |
| T04 | Ausencia declarada | Subsecciones con `No findings detected / N/A` y `N/A` | N/A | 0 |
| T05 | Legacy sin contenedor | Plan legacy sin `## Findings / Correcciones / Pending` | EXCLUDED | 0 |
| T06 | Refs lifecycle en prosa sin contenedor | Plan sin contenedor con `` `<PLAN-98>:F-1` `` en texto | BOUNDARY | 0 |
| T07 | Campo requerido faltante | Finding sin `evidencia original` | GAP | 0 |
| T08 | Estado desconocido | `estado: `waiting`` | ANOMALY | 1 |
| T09 | Boundary `reopened` como estado | `estado: `reopened`` con metadata | GAP (ambigüedad; regla semántica fuera de v1) | 0 |
| T10 | Namespace ajeno en opener | Registro `<PLAN-98>:F-1` dentro del Plan 99 | ANOMALY | 1 |
| T11 | Identidad duplicada | Dos registros `<PLAN-99>:F-1` | ANOMALY | 1 |
| T12 | `resolved` sin resolución | F sin campo `resolución` | GAP | 0 |
| T13 | Resolución contradictoria | F `resolved` con resolución "sin resolver" | ANOMALY | 1 |
| T14 | Resolución referencia correction inexistente | `resolución` con `<PLAN-99>:C-9` sin registro C-9 | ANOMALY | 1 |
| T15 | `deferred` sin owner/destino | F `deferred` sin esos campos | GAP | 0 |
| T16 | Correction sin origen | C sin `refs origen` o sin ref F | GAP | 0 |
| T17 | Claim de revalidación sin soporte | C declara V2/PASS y el anchor no declara revalidación | GAP | 0 |
| T18 | Marcador de ausencia + registros | `No findings detected / N/A` + F real en la misma subsección | ANOMALY | 1 |
| T19 | Ref destino cross-artifact resoluble | C en Plan 99 refiere F real del Plan 98 (si existiera) | VALID | 0 |
| T20 | Ref destino cross-artifact inexistente | C refiere `<PLAN-98>:F-1` sin registro en Plan 98 | ANOMALY | 1 |
| T21 | Ref `RFC-` destino | C refiere `<RFC-75>:F-1` (formato válido) | VALID (formato; resolución fuera de v1) | 0 |
| T22 | Contenido no parseable | Bullet sin ref calificada en `### Findings` | GAP | 0 |
| T23 | Determinismo | Mismo repo dos corridas | Salidas idénticas | 0 |
| T24 | Ejecución repetida | Correr C-3 dos veces seguidas | Sin cambio de estado, mismas clasificaciones | 0 |
| T25 | Exit codes | Corpus con GAP vs corpus con ANOMALY | GAP → 0; ANOMALY → 1 | según caso |
| T26 | Comentarios ignorados | Guía del template en comentarios HTML | Sin efecto en clasificación | 0 |
| T27 | Dogfooding repo real | Repo ARgentOS actual | §19 invariantes | 0 |
| T28 | Stdlib only | AST de imports del tool | Sin imports third-party | 0 |

## 19. Dogfooding Strategy

**[PROPOSED — Future Implementation]** Al ejecutar el Plan 100, C-3 se corre
sobre el propio repositorio (plan 94 §19; precedente C-1/C-2). Invariantes
esperadas sobre el corpus real:

- Plan 96 y Plan 97 → `EXCLUDED` (sin contenedor de lineage; sus anchors/
  checkpoints siguen verificados por C-1/C-2 — dominios distintos por
  checker, no regresión);
- Plan 98 → `N/A` (ausencia declarada en `### Findings`/`### Correcciones`);
- Plan 99 → `VALID` (cadena `<PLAN-99>:F-1` → `<PLAN-99>:C-1` completa y
  consistente: required fields presentes, refs origen resueltas en el mismo
  artifact, claim de revalidación V1/V2 soportado por su `## Validation
  anchor`);
- Plan 100 → `EXCLUDED`/`N/A`/`VALID` según su fase al ejecutar (regex
  lifecycle-stable en el test de dogfooding, precedente C-2);
- legacy 01–95 → `EXCLUDED`; `_TEMPLATE.md` y anexos → no escaneados;
- `ANOMALY=0` y `GAP=0` en el estado final de cierre.

La demostración de que C-3 no está diseñado solo para fixtures: el registro
real de Plan 99 (prosa rica, campos informacionales, continuaciones
indentadas, refs cruzadas) debe clasificar `VALID` sin reglas ad hoc; el
registro de ausencia real de Plan 98 debe clasificar `N/A`. Si el corpus real
produjera una clasificación distinta, **STOP** y escalación (condición C4,
§28).

## 20. Adversarial Scenarios

**[PROPOSED — Future Implementation]** Casos adversariales obligatorios como
tests permanentes (§18) y revisión manual al ejecutar:

- ref calificada con namespace correcto pero número de artifact inexistente
  en el corpus (`<PLAN-98>:F-5` sin registros en Plan 98);
- ref sin backticks o con formato alternativo (`PLAN-99:F-1`, `F-1` bare,
  `F-01` con cero a la izquierda, `<PLAN-99>: f-1`); las variantes fuera del
  contrato de §14 → GAP o ANOMALY según R-L1-1/R-L1-11 (nunca VALID por
  tolerancia inventada);
- finding `superseded` sin referencia a reemplazo: en v1 no hay regla nueva de
  contenido (sin corpus ejemplar); la ausencia de regla se declara en §16 y no
  genera ANOMALY (sin invento normativo);
- correction que declara revalidación con PASS pero el artifact declara
  checkpoint FAIL (contradicción con C-2-style semantics) → ANOMALY (regla
  R-L1-9 extendida a FAIL explícito en el checkpoint del mismo artifact);
- registros duplicados entre subsecciones (`F-1` listado bajo Findings y bajo
  Correcciones) → ANOMALY (R-L1-2);
- contenedor presente pero sin subsecciones de nivel 3 → N/A (vacío) o GAP
  (contenido visible sin estructura); nunca EXCLUDED;
- texto del corpus con `;` dentro de valores de campos (p. ej. fechas) → el
  parser separa por labels, no por `;` ciego (R-L1-11; §14.2);
- múltiples registros de validación en el anchor (deuda F-3) que vuelven
  ambiguo el soporte de revalidación → GAP, nunca resolución de F-3 (§16
  R-L1-9).

## 21. Governance Constraints

**[NORMATIVE]** El Plan 100 no modifica, ni en esta iteración ni al ejecutar:

- RFC-75 (header y Amendment Log intactos; sin enmienda), ADR-15, ADR-16;
- Planes 94–99 (status, historia, anchors, checkpoints, findings/corrections,
  commits) — Plan 99 permanece CLOSED y no se reabre;
- `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `AGENTS.md` raíz,
  `docs/AGENTS.md`, templates (el formato de §14 ya existe y no requiere
  cambios);
- C-1/C-2 y sus tests; `protocol/.agents/`; `.agents/` raíz; `dist/`.

Si la ejecución demostrara que es imprescindible modificar alguno de esos
artifacts, el Plan no lo hará silenciosamente: se identifica como decisión
previa requerida y se escala (AU-3/AU-5; §28). C-3 no se incorpora a la
batería canónica ni a CI en este Plan (precedente Plan 98 §15); sigue siendo
invocación local opcional.

## 22. Change Lifecycle for Plan 100

**[PROPOSED]** Estrategia de lifecycle del propio Plan 100 al ejecutar:

```text
Baseline (G0)
   ↓
Implementation C-3 (G1)
   ↓
Tests (G2)
   ↓
Dogfooding corpus real (G3)
   ↓
Adversarial (G4)
   ↓
Validation V1 + Validation Anchor propio (G5)
   ↓
Corrections si aparecen (C-n del propio plan; nunca silenciosas)
   ↓
A2 / revalidación V2 si corresponde (G5/G6)
   ↓
Checkpoint / cierre (G6)
   ↓
Closed (docs-only) (G7)
```

- No reutiliza el anchor de Plan 99 (ni de ningún plan previo); tendrá sus
  propios registros de validación (A1/A2 o V1/V2) y checkpoint (§24/§25).
- A1 original permanece inmutable; A2 es una nueva validación, no reemplaza
  A1; el cierre corresponde al estado validado; el checkpoint comprueba esa
  relación (Decisión B; GC-1).
- Los findings/corrections que surjan durante la ejecución se registran en
  este artifact bajo las reglas del Incremento 2 (§29/§34); no se fabrican
  registros.

## 23. Validation Strategy

**[PROPOSED]** Al ejecutar, la validación del contenido de C-1 (commit de
contenido C1, §27) corre **antes** de agregar los registros de cierre de este
artifact (anti-circularidad; precedente planes 96–99):

- validation command-set: suite C-3
  (`python -m pytest tests/test_check_lifecycle_lineage.py`), suite completa
  (`python -m pytest tests/`), checkers canónicos
  (`python tools/check_protocol_invariants.py --payload protocol .`,
  `python tools/check_plan_citations.py`,
  `python tools/check_plan_structure.py`,
  `python tools/check_taxonomy_coherence.py`,
  `python tools/check_session_artifacts.py`,
  `python tools/check_version_state.py`), C-1/C-2 sobre el corpus, dogfooding
  C-3 (§19) y `git diff --check`;
- declared scope / effective inputs / observed dependencies / environmental
  factors / Scoped Content Identity (state identity + delta scoped identity
  v1): se registran en la sección `## Validation anchor` al ejecutar
  (formato VC-1; §24);
- política de "batería verde" del plan 94 §24.1: PASS real o desviación
  documentada aceptada por el mantenedor (condición C2).

## 24. Anchor Strategy

**[PROPOSED]** Al ejecutar, este artifact registrará su propio Validation
Anchor en una sección `## Validation anchor` (no existe en esta iteración de
creación; no se fabrica): V1 sobre el contenido del commit C1 (antes de los
registros de cierre), con state identity (tree id de C1) y delta scoped
identity (serialización `scoped-v1` sobre el scope de C1: tool + tests),
según el formato v1 de `docs/CONVENTIONS.md:Change Lifecycle — Validation
anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`.
No reutiliza anchors de Planes 96–99.

## 25. Checkpoint Strategy

**[PROPOSED]** Al ejecutar, este artifact registrará su Checkpoint de cierre
en una sección `## Checkpoint / cierre` (no existe en esta iteración):
commits de cierre C1 (contenido) y C2 (registros de cierre), estado validado
(ref al Validation Anchor), estado de cierre (tree id del commit final, sin
embeker la propia identidad — auto-referencia excluida), consistencia
checkpoint↔anchor (V1 ↔ C1 PASS; revalidación V2 sobre el estado final antes
de `Closed`), governance aplicada y condición derivada `Closed` (docs-only,
sin release), conforme a GC-1
(`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`).

## 26. Acceptance Criteria

Checklist verificable PASS/FAIL (sin criterios vagos). Esta iteración de
creación satisface AC-01/AC-02/AC-19/AC-20; el resto corresponde a la
ejecución futura:

- [ ] **AC-01** — El Plan 100 existe en `docs/plans/100-change-lifecycle-lineage-integrity.md` con el naming correcto.
- [ ] **AC-02** — Plan 100 registrado en `docs/plans/INDEX.md` (Trigésima segunda serie; Status `Aprobado para ejecución`; sin placeholders).
- [ ] **AC-03** — La capacidad seleccionada es exclusivamente integridad de lineage findings/corrections/revalidación (LC-1) (§6/§11).
- [ ] **AC-04** — C-3 queda especificado de forma determinista para implementación sin nueva auditoría (§13–§16).
- [ ] **AC-05** — La población del dominio usa señales estructurales sin crear autoridad (§14).
- [ ] **AC-06** — La semántica GAP advisory ≠ ANOMALY queda definida y sin autoridad normativa (§15/§16).
- [ ] **AC-07** — No se exige Git en C-3 v1 (§13/§16).
- [ ] **AC-08** — Legacy (incluidos planes 96/97 y 01–95) queda fuera del dominio sin backfill (§12/§14).
- [ ] **AC-09** — Pending (`### Pending decisions`) queda fuera del dominio v1 explícitamente (§12).
- [ ] **AC-10** — F-3 no se resuelve, no se implementa incidentalmente y no se convierte en objetivo (§12/§29).
- [ ] **AC-11** — RFC-75, ADR-15, ADR-16 y Planes 94–99 permanecen intactos (§21).
- [ ] **AC-12** — No se crean entidades, registries, state machines, CI, runtime ni dependencias externas (§12).
- [ ] **AC-13** — La test matrix de §18 cubre happy path, missing, malformed, conflicting, legacy, boundary, no-retroactivity, determinismo, ejecución repetida, adversarial y dogfooding.
- [ ] **AC-14** — Los escenarios adversariales de §20 quedan como tests permanentes.
- [ ] **AC-15** — El dogfooding de §19 usa datos reales (Plan 98/99) y no fabrica findings.
- [ ] **AC-16** — El Plan define su propia validación/anchor/checkpoint/cierre (§22–§25).
- [ ] **AC-17** — El Plan no se declara `Executed`/`Closed` en esta iteración (Status `Aprobado para ejecución`).
- [ ] **AC-18** — La ejecución futura no mezcla cambios ajenos (commits C1/C2; §27) y no hace push/tag/release.
- [ ] **AC-19** — Esta iteración no modifica código, tests, C-1, C-2, RFC/ADR ni `protocol/` (verificable por git diff).
- [ ] **AC-20** — El estado documental de esta iteración es `Planned: YES; Executed: NO; Committed: NO; Verified: NO; Closed: NO; Released: NO`.

## 27. Commit Strategy

**[PROPOSED — Future Implementation]** Al ejecutar (no en esta iteración):

- **C1 (contenido):** `tools/check_lifecycle_lineage.py` +
  `tests/test_check_lifecycle_lineage.py`; mensaje convencional propuesto:
  `feat(tools): add lifecycle lineage checker (plan 100, RFC-75)`; validado
  por V1 antes del commit.
- **C2 (registro/cierre):** Validation Anchor, Checkpoint, registros reales de
  findings/corrections/pending si surgen, espejo del INDEX y ítem
  `(plan 100, RFC-75)` en `CHANGELOG.md:[Unreleased]`; mensaje propuesto:
  `docs(plans): record plan 100 validation anchor and checkpoint (plan 100,
  RFC-75)`.
- Sin push, sin tag, sin release, sin `VERSION` bump, sin modificar
  `protocol/VERSION`. Multi-commit permitido si emerge; el registro de cierre
  no embebe su propio SHA/tree (auto-referencia excluida).

## 28. Recovery / Stop Conditions

**[PROPOSED]** La ejecución futura se **detiene** y escala (AU-3) si ocurre
cualquiera de estos casos:

- tests fallan (suite C-3, pytest global o checkers canónicos) sin desviación
  aceptada;
- el dogfooding real difiere de las invariantes de §19 (condición C4);
- aparece una ambigüedad normativa real (no un defecto de implementación):
  p. ej., necesidad de modificar RFC-75/ADR-15/16 o de definir semántica
  nueva de estados/reapertura/pending; se documenta como blocker y se escala;
- aparece un cambio fuera de scope (F-3, pending, C-1/C-2, batería/CI,
  payload);
- un checker existente entra en conflicto con C-3 (p. ej., C-1/C-2 o
  estructural) sin resolución documentada;
- la implementación requiere una decisión arquitectónica nueva (registry,
  Git en v1, lectura de RFCs, composición);
- la implementación requiere Git o red para funcionar en v1.

Regla: no resolver silenciosamente una decisión normativa; un defecto de
implementación (p. ej., parseo del corpus) no es una decisión normativa y se
corrige en el alcance del Plan (R-L1-x) con evidencia y tests.

## 29. Known Deferred Findings

**[DERIVED]** Deudas conocidas, **no-bloqueantes** para el Plan 100:

- **F-1** (`<PLAN-99>:F-1`): `resolved` por `<PLAN-99>:C-1` (corrección de
  C-2/GC-1). Histórica; Plan 99 CLOSED; no se reabre (§12).
- **F-3**: duplicate validation records, dominio de C-1, `open` (deuda
  diferida del C1/C2 Read-Only Audit Report, no versionado). **No bloquea**
  C-3: C-3 verifica registros F/C y solo consulta markers de revalidación del
  anchor; ante ambigüedad por duplicados → GAP, nunca resolución (§16
  R-L1-9). No se convierte en objetivo del Plan 100 (§11/§12).
- **F-2, F-4…F-9**: deferidos (identificadores del C1/C2 Read-Only Audit
  Report; detalle no versionado en el repo). No son blockers salvo evidencia
  concreta en contrario; no se convierten en scope.
- **Deuda de cierre/gobernanza**: verificación de "findings resueltos o
  diferidos antes de `Closed`" y pending bloqueantes en la derivación de
  `Closed` (matriz de governance) queda habilitada por C-3 pero **fuera** del
  scope v1 (§12/§34).

## 30. Risks

**[DERIVED]**

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Checker como autoridad normativa | Alto | §15/§21: factual/advisory; GAP ≠ invalidación; ANOMALY ≠ decisión |
| Parser frágil sobre prosa real del corpus | Medio | Contrato §14 basado en el corpus real; ambigüedad → GAP; STOP si no resuelve (C3) |
| Scope leakage (F-3, pending, C-1/C-2, battery/CI, métricas) | Alto | §11/§12; Gates 1 y 5 (§32) |
| Clasificación del corpus real distinta de §19 | Medio | Invariantes §19; STOP antes del commit (C4) |
| Confusión de identidad C-3 (checker) vs `<PLAN-nn>:C-n` (correction) | Bajo | Namespaces calificados; texto explícito en docstring/INDEX |
| Interpretación de claims de revalidación como verdad | Alto | R-L1-9 solo exige soporte declarado (marker), nunca verifica semántica |
| F-3 arrastrado al scope por proximidad | Medio | §12/§29; regla R-L1-9 GAP sin tie-break |
| ACL del sandbox en pytest | Bajo (ambiental) | Permisos reales; reporte honesto (plan 94 §24.1) |

## 31. Dependencies

**[DERIVED]**

- Normativas: RFC-75 `Accepted` (Mec. 6/8/9/12/13/14/15); ADR-15/16
  `Accepted`; RFC-46/56/69; CONVENTIONS (LC-1/PC-1/VC-1/GC-1); VERSIONING
  (§7/§10/§11); Planes 94–99 (estado registrado).
- De datos: corpus real del Incremento 2 (Plan 98 ausencia declarada; Plan 99
  cadena real) — gate persist → observe → automate satisfecho.
- De código: stdlib Python; patrón estructural de C-1/C-2 (sin imports
  cruzados); pytest con `tmp_path`.
- Sin dependencias externas, sin red, sin Git en v1, sin CI.
- Pending no-bloqueantes de la serie (owners registrados en planes 97–99):
  no afectan esta iteración; se listan como contexto (§34).

## 32. Execution Gates

**[PROPOSED — Future Implementation]** La ejecución futura no omite ningún
gate; cada gate tiene entrada, acciones, evidencia, condición PASS y
condición STOP:

| Gate | Entrada | Acciones | Evidencia | PASS | STOP |
|---|---|---|---|---|---|
| G0 Baseline | Branch `dev`; HEAD conocido; árbol limpio salvo cambios del plan | Capturar estado §3; batería/pytest baseline | `git status`, pytest | Estado sostenido o desviación aceptada (C2) | Estado distinto sin autorización |
| G1 Implementation | G0 PASS | Crear `tools/check_lifecycle_lineage.py` según §13–§16 | Diff limitado a tool | Tool presente; solo scope §11 | Scope leakage o decisión nueva |
| G2 Tests | G1 PASS | Implementar `tests/test_check_lifecycle_lineage.py` (matriz §18) | pytest suite C-3 verde | T01–T28 PASS | Fallo sin desviación |
| G3 Dogfooding | G2 PASS | Correr C-3 sobre el repo real | Salida C-3 | Invariantes §19 (98 N/A; 99 VALID; legacy EXCLUDED; ANOMALY=0) | Clasificación fuera de invariantes (C4) |
| G4 Adversarial | G3 PASS | Revisar §20; regresiones permanentes | Tests adversariales | §20 casos PASS sobre la implementación nueva | Ambigüedad normativa (C3) |
| G5 Validation | G4 PASS | Batería canónica completa + pytest global + V1 | Anchor V1 (§24) | Batería verde o desviación aceptada (C2) | Blocker de §28 |
| G6 Checkpoint | G5 PASS | Registros de cierre + revalidación V2 sobre estado final staged | Checkpoint (§25); C-1/C-2/C-3 dogfooding PASS | GC-1 consistencia PASS | Inconsistencia checkpoint↔anchor |
| G7 Closure | G6 PASS | Ítem changelog; espejo INDEX; condición derivada | Estado final | AC-03…AC-18 + §33 | Cualquier AC FAIL |

## 33. Closure Criteria

**[PROPOSED]** Condición derivada `Closed` de este Plan = `Executed` +
governance aplicable + checkpoint propio + consistencia checkpoint↔anchor
(GC-1) + evidencia de validación PASS para el estado de cierre (§24/§25).
Cierre **docs-only/tools-only sin release** (sin `VERSION` bump, sin tag;
RFC-75 Mecanismo 5; RFC-69). No se reutiliza el anchor de Plan 99; Plan 99 es
solo precedente histórico.

## 34. Post-Plan State

**[PROPOSED]** Estado posterior al cierre del Plan 100:

- C-3 operativo como checker local opcional (no en la batería canónica, no en
  CI); verificaciones de lineage re-ejecutables;
- Plan 100: `Executed` + `Closed` (docs-only); `Committed` (C1 + C2 en `dev`);
  `Released` NO aplica;
- registro del propio Plan con su Validation Anchor y Checkpoint;
- habilitados para trabajo futuro (no planificado aquí, sin inventar roadmap):
  verificación PC-1 de pending, composición de checkers, verificación de la
  implicación "findings resueltos/diferidos antes de `Closed`", métrica
  finding lineage coverage (RFC-75 Mec. 13) — cada uno con su propio gate de
  observabilidad y decisión humana;
- deuda F-2…F-9 y F-3 permanecen diferidas; sin cierre por interpretación.

## 35. Traceability Matrix

**[DERIVED]**

| Requirement / Decision | Source | Plan Section | Implementation Evidence |
|---|---|---|---|
| Findings como relaciones con refs calificadas y estados | RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation` | §6/§8/§14 | C-3 R-L1-1…R-L1-12 + tests T01–T28 |
| CL-6/CL-7/CL-8 (provenance, alcance de revalidación, trazabilidad, no eliminación) | ADR-15 `docs/adr/15-change-lifecycle-continuity.md:Invariantes` | §8/§14/§16 | R-L1-5/R-L1-8/R-L1-9 + tests |
| Checker factual ≠ autoridad; GAP ≠ invalidación | ADR-16 `docs/adr/16-change-lifecycle-authority.md:Invariantes`; RFC-75 Mec. 14 | §13/§15/§21 | Exit codes; clasificación; docstring |
| Formato operativo LC-1 (Incremento 2) para artifacts nuevos | CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)` | §8/§9/§14 | Corpus Plan 99 VALID (dogfooding) |
| Pending per-artifact (PC-1) fuera de v1 | CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)` | §12/§15 | Sin parseo de `### Pending decisions` |
| Candidato "Checker de formato de refs" diferido del Incremento 4 | Plan 94 `docs/plans/94-change-lifecycle-master-action-plan.md:7. Mapeo RFC-75 → mecanismos` | §2/§6/§7 | Este Plan 100 |
| Población estructural y GAP/anomalía | Plan 98 `docs/plans/98-change-lifecycle-unit-d-increment-4.md:8. Población del Change Lifecycle regime` | §14/§15 | Fixtures T05/T06/T27 |
| Legacy/no-retroactividad | RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`; RFC-46 | §12/§14/§29 | T05/T27; planes 96/97 EXCLUDED |
| Gate persist → observe → automate | Plan 94 Unit D; RFC-75 Mec. 14 | §1/§7/§9 | Corpus real Plan 98/99 |
| F-3 no bloqueante / no objetivo | Estado factual del repo; C1/C2 Read-Only Audit Report (insumo) | §12/§29 | R-L1-9 GAP sin tie-break |
| Mecanismo de cierre del propio Plan | RFC-75 Mec. 5/7; Decisión B; precedentes 96–99 | §22–§25 | Anchor/Checkpoint al ejecutar |

---

## Validation anchor

Registrado al ejecutar el Plan 100 (2026-09-02). La validación **V1** corrió
sobre el contenido de implementación de C-3 (commit de contenido C1
`1ffe24c`) **antes** de agregar los registros de cierre de esta sección
(anti-circularidad, §23/§25; precedente planes 96–99).

- Declared scope: materialización de C-3 — lifecycle lineage checker
  (`tools/check_lifecycle_lineage.py`, reglas R-L1-1…R-L1-12 del §16) + suite
  nueva (`tests/test_check_lifecycle_lineage.py`: matriz T01–T28 y escenarios
  adversariales permanentes del §20) + batería canónica del repo + dogfooding
  C-1/C-2/C-3 sobre el corpus real.
- Validation command-set:
  - `python -m pytest tests/test_check_lifecycle_lineage.py`
  - `python -m pytest tests/`
  - `python tools/check_lifecycle_lineage.py`
  - `python tools/check_lifecycle_anchor.py`
  - `python tools/check_lifecycle_checkpoint.py`
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `git diff --check`
- Effective inputs (repo content): contenido completo del repo en el estado
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/` y la
  raíz; pytest consume `tests/` + `tools/`); representado por el State
  identity (tree id). El working tree validado incluía además los registros de
  creación del Plan 100 (`docs/plans/INDEX.md` modificado + este artifact sin
  trackear, pendientes de C2), ajenos al contenido de C-1 inspeccionado por la
  suite.
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en
  esta ejecución); el consumo por comando se observa de la documentación de
  cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica de
  verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 10.3.0; pytest ejecutado fuera
  del sandbox por ACL del basetemp `pytest-of-rolda` (ruido ambiental
  documentado en planes 96–99); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `2f348f379fe627021e43f39a69b89a3813977602` (tree id; igual a
    `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 2 archivos del cambio de C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `e4f715ecb3831900817ec842a4ded357a0a4085259a4180003682487737416b1`.
    Pares path → blob (C1): `tests/test_check_lifecycle_lineage.py` →
    `34a0d5965ac136b0930302c82b183b25065e86af`;
    `tools/check_lifecycle_lineage.py` →
    `b411bccff1d16d0c3f146524a4514640c03cee6d`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería completa +
  dogfooding C-1/C-2/C-3 sobre el estado final de la ejecución, incluidos los
  registros de cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7; §25 de este
plan). Se registra en el commit de registro C2, posterior al commit de
contenido C1.

- Commits de cierre:
  - C1 `1ffe24cef571fde35c0ce1269b18734f00f49add` —
    `feat(tools): add lifecycle lineage checker (plan 100, RFC-75)`
    (contenido de C-3 validado por V1).
  - C2 — este commit de registro
    (`docs(plans): record plan 100 validation anchor and checkpoint (plan 100,
    RFC-75)`); su SHA se identifica por el mensaje y el árbol no embebe su
    propia identidad (auto-referencia excluida, §27).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `2f348f379fe627021e43f39a69b89a3813977602`; Delta scoped identity =
  `e4f715ecb3831900817ec842a4ded357a0a4085259a4180003682487737416b1`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`2f348f37…`) → **PASS**.
  - Estado final (C2): difiere de C1 en los registros de cierre (anchor/
    checkpoint de este plan, contenedor de findings/correcciones, INDEX y
    changelog); **revalidación V2** (batería canónica completa + pytest +
    dogfooding C-1/C-2/C-3 sobre el contenido final de la ejecución, ejecutada
    antes del commit) → PASS. GC-1 queda satisfecho por revalidación antes de
    `Closed` (la consistencia del estado de cierre se evalúa contra A2/V2;
    correspondencia por estado, nunca por recencia).
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 100, RFC-75)` en `CHANGELOG.md:[Unreleased]`; tooling/tests DEV-only
  sin incorporación a la batería canónica ni a CI (§11.3); docs-only, sin
  `VERSION` bump ni tag.
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (C1 + C2 en `dev`), `Closed` (condición derivada con checkpoint
  y consistencia), `Released` (no aplica: sin promoción ni tag).

## Findings / Correcciones / Pending

Registros reales de esta ejecución (artefactos nuevos bajo las reglas del
Incremento 2; la ausencia de registros no es invalidez):

### Findings

- `No findings detected / N/A` (no se fabrican findings sintéticos).

### Correcciones

- `N/A` (ninguna corrección en esta iteración).

### Pending decisions

Pendings **no-bloqueantes** (PC-1), owner: mantenedor, escalación: humana
(AU-3); condiciones reales del Plan (§1/§28) resueltas al ejecutar:

- `<PLAN-100>` — decisión: OQ-1 autorización de ejecución y commits; blocking:
  no; owner: mantenedor; escalación: humana; resolución: autorización explícita
  otorgada por el mantenedor (Execution Prompt 2026-09-02); ejecución y commits
  C1/C2 realizados en `dev`; resuelto.
- `<PLAN-100>` — decisión: OQ-2 aceptación de la batería al cierre; blocking:
  no; owner: mantenedor; escalación: humana; resolución: batería aceptada al
  cierre (pytest `428 passed, 0 failed`; checkers canónicos PASS; dogfooding
  GAP=0, ANOMALY=0); resuelto.
- `<PLAN-100>` — decisión: OQ-3 ambigüedades de parseo del corpus; blocking:
  no; owner: ejecutor/mantenedor; escalación: humana; resolución: sin
  ambigüedad residual — reglas R-L1-x implementadas con separación por labels
  (nunca `;` ciego) y soporte del wrap de línea del corpus (dogfooding real:
  Plan 99 `VALID` sin reglas ad hoc); no se requirió STOP; resuelto.
- `<PLAN-100>` — decisión: OQ-4 dogfooding real fuera de invariantes; blocking:
  no; owner: mantenedor; escalación: humana; resolución: dogfooding real
  cumplió las invariantes de §19 (96/97 `EXCLUDED`, 98 `N/A`, 99 `VALID`,
  legacy 01–95 `EXCLUDED`, GAP=0, ANOMALY=0; plan 100 lifecycle-stable:
  `BOUNDARY` en su fase de creación y `N/A` tras registrar el contenedor de
  este plan en C2); no se requirió STOP; resuelto.

## Trazabilidad

Origen → RFC-75 `Accepted` + ADR-15/16 (Accepted) + Planes 94–99 (CLOSED,
históricos) → este Plan 100 (continuación post-roadmap A–D: C-3 lifecycle
lineage checker) → ejecución (tool + suite + dogfooding) → validación V1 →
checkpoint con revalidación V2 → cierre docs-only. Este plan no autoriza
cambios de payload (RFC-56); la autorización de la ejecución es humana (OQ-1).

## Nota de ejecución

- 2026-09-02 — **Creación/registro (planificación).** Plan 100 creado y
  registrado en `docs/plans/INDEX.md` (Trigésima segunda serie; Status inicial
  `Aprobado para ejecución`, PLANNED / OPEN) a partir del estado factual del
  repo (HEAD `51cabb2`, working tree limpio, planes 94–99 cerrados) y de la
  selección con evidencia de la capacidad de lineage findings/corrections/
  revalidación (LC-1) como continuación post-roadmap A–D, **sin implementar**
  C-3 y sin commits. Verificación de la iteración: checkers documentales
  canónicos pertinentes en verde (`check_protocol_invariants.py`,
  `check_plan_citations.py`, `check_plan_structure.py`,
  `check_taxonomy_coherence.py`, `check_session_artifacts.py`,
  `check_version_state.py`); `check_dist_sync.py` no se reinterpreta en `dev`
  (semántica local/release); pytest no se re-corrió en esta iteración (cambio
  exclusivamente documental; baseline reportado `388 passed, 0 failed`). Sin
  cambios en `protocol/`, `runtime/`, `tests/`, `tools/`, VERSION, CHANGELOG,
  ADRs, RFCs, `docs/CONVENTIONS.md`, `docs/VERSIONING.md` ni planes 94–99; sin
  creación de `.agents/` en la raíz; sin push. **STOP:** la implementación de
  C-3 queda pendiente de revisión humana del Plan y de su aprobación
  explícita.
- 2026-09-02 — **Ejecución de la continuación post-roadmap sobre `dev`.**
  Estado previo: HEAD `51cabb2`, working tree con los cambios de creación del
  plan (INDEX + este artifact, sin commit), pytest `388 passed, 0 failed`,
  checkers canónicos PASS. **C1 (contenido):**
  `tools/check_lifecycle_lineage.py` (C-3 — reglas R-L1-1…R-L1-12 del §16;
  población por señales estructurales del §14; GAP advisory ≠ ANOMALY; sin
  autoridad normativa; read-only, stdlib-only, sin Git en v1) +
  `tests/test_check_lifecycle_lineage.py` (matriz T01–T28 del §18 + 12
  escenarios adversariales permanentes del §20 = 40 tests). Defectos de
  implementación detectados y corregidos durante el desarrollo, antes de V1
  (regex canónica del ref `<PLAN-nn>:F-<n>` con un solo par de ángulos; labels
  con wrap de línea del corpus real; separación por labels y no por `;` ciego),
  cubiertos por regresiones permanentes de la suite (dogfooding T27,
  determinismo T23, adversarial de `;` en valores): no persistieron al estado
  validado y no generan registros F/C post-validación. **Commit C1:** `1ffe24c`
  (2 archivos; tree `2f348f37`). **Gates:** pytest suite C-3 `40 passed`
  (GATE 2); pytest global `428 passed, 0 failed` (GATE 2); checkers canónicos
  PASS — `check_protocol_invariants.py` (212 files, 9720 references),
  `check_plan_citations.py`, `check_plan_structure.py`,
  `check_taxonomy_coherence.py`, `check_session_artifacts.py` y
  `check_version_state.py` (warnings esperados de `dev`) (GATE 5);
  `git diff --check` limpio (GATE 5). **Dogfooding (GATE 3):** C-3 sobre el
  corpus real — 96/97 `EXCLUDED`, 98 `N/A` (ausencia declarada), 99 `VALID`
  (cadena `<PLAN-99>:F-1` → `<PLAN-99>:C-1` con soporte V2 en su anchor),
  legacy 01–95 `EXCLUDED`, plan 100 `BOUNDARY` en su fase de creación (refs
  calificadas en prosa sin contenedor; §14.1) y `N/A` tras registrar el
  contenedor de este plan en C2; GAP=0, ANOMALY=0; C-1/C-2 sin regresión
  (100 planes; GAP=0, ANOMALY=0). **Adversarial review (GATE 4):** los
  escenarios del §20 quedan como tests permanentes y pasan sobre la
  implementación final (refs inexistentes en el corpus, variantes de formato
  → nunca VALID, `superseded` sin regla nueva, claim PASS + checkpoint FAIL →
  ANOMALY, duplicados entre subsecciones → ANOMALY, contenedor sin nivel 3 →
  N/A/GAP nunca EXCLUDED, `;` en valores → parseo por labels, F-3 →
  ambigüedad → GAP sin tie-break). **C2 (registros de cierre):** Status
  `Executed`; Validation Anchor V1 (T1 `2f348f37…`; delta `e4f715ec…`) y
  Checkpoint con revalidación V2 (batería completa + dogfooding C-1/C-2/C-3
  sobre el estado final staged) antes de `Closed` en este artifact; espejo en
  `docs/plans/INDEX.md`; ítem `(plan 100, RFC-75)` en
  `CHANGELOG.md:[Unreleased]`; contenedor findings/correcciones con ausencia
  declarada y pendings no-bloqueantes OQ-1…OQ-4 resueltos; condición derivada
  `Closed` (docs-only, sin release). Scope audit: sin cambios en `protocol/`,
  `runtime/`, C-1/C-2 y sus tests, RFC-75/ADR-15/16, `docs/CONVENTIONS.md`,
  `docs/VERSIONING.md`, VERSION, Planes 94–99, batería canónica, CI, tags ni
  releases; sin push.
