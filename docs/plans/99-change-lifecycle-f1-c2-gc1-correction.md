# Plan 99 — Corrección de F-1: selección del anchor aplicable en C-2 (GC-1)

> **Naturaleza de este documento.** Este es un **correction Plan post-close**
> de la serie Change Lifecycle DEV gobernada por RFC-75. Corrige
> exclusivamente el defecto de materialización **F-1** detectado por el
> **C1/C2 Read-Only Audit Report** posterior al cierre de Plan 98: la
> selección del Validation Anchor aplicable en el lifecycle checkpoint
> checker C-2 (`tools/check_lifecycle_checkpoint.py`) no implementa la
> semántica GC-1 (correspondencia del estado de cierre con la validación
> cuyo estado validado lo cubre), sino una selección por recencia
> ("latest A2 wins") combinada con pertenencia genérica del tree entre los
> commits de cierre.
>
> **La presente iteración es solo de creación/registro del plan**: crea este
> archivo y su registro en `docs/plans/INDEX.md`; **no ejecuta la corrección**,
> no modifica `tools/check_lifecycle_checkpoint.py`, no modifica tests, no
> crea `C-n`, no reabre ni modifica Plan 98, no modifica RFC-75, ADR-15 ni
> ADR-16, no toca `protocol/.agents/`, no crea `.agents/`, no introduce
> runtime/harness/CI/registries/métricas y no crea commits. Estado esperado al
> cierre de esta iteración:
>
> ```text
> Plan 99 = Aprobado para ejecución (PLANNED / OPEN)
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
ver §11)
**Depende de:** RFC-75 `Accepted` (`docs/rfc/75-change-lifecycle.md`); ADR-15
`Accepted` (`docs/adr/15-change-lifecycle-continuity.md`); ADR-16 `Accepted`
(`docs/adr/16-change-lifecycle-authority.md`); RFC-46 `Accepted`; RFC-56
`Accepted`; RFC-69 `Accepted`; Plan 94 `Executed`; Plan 95 `Executed`; Plan 96
`Executed` + `Closed` (docs-only); Plan 97 `Executed` + `Closed` (docs-only);
Plan 98 `Executed` + condición derivada `Closed` (docs-only, sin release);
Decisión B (`fc52c88`, semántica A1/A2/closure PASS); **C1/C2 Read-Only Audit
Report posterior a Plan 98** (origen de F-1; artefacto de sesión no versionado
en el repo — insumo, no fuente normativa; ver §5/§7).
**Origen:** Hallazgo post-close **F-1** del C1/C2 Read-Only Audit Report
(2026-09-02), posterior a la ejecución/cierre de Plan 98; defecto MAJOR de
implementación/materialización de GC-1 en C-2. Solicitud explícita del
mantenedor: crear físicamente este Plan de corrección **sin implementar**
F-1, sin cerrar el Plan y sin adelantar cambios fuera del registro documental.

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
| `PROPOSED` | Elección operativa de este plan (especificación de la corrección futura); no es normativa hasta ejecutarse. |
| `OPEN` | Decisión pendiente que no impide redactar/ejecutar el plan; requiere decisión humana o plan posterior. |
| `BLOCKER` | Contradicción que impide ejecutar la corrección (no se detectó ninguna; ver §25/§32). |
| `UNKNOWN` | No verificable en el estado actual; se indica cómo resolverlo. |

Las afirmaciones sobre el estado actual del repo se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`). El C1/C2 Read-Only Audit Report no se
cita como `ruta:sección` porque no es un artifact versionado del repo: es la
provenance de sesión del hallazgo (insumo), y este plan lo incorpora sin
convertirlo en fuente normativa (ADR-16 AU-4; ver §5).

## Contenido requerido → sección

| Requisito del encargo | Sección de este documento |
|---|---|
| Header / metadata e identidad | Header de este archivo |
| Naturaleza / esta iteración no implementa | Banner de apertura |
| Resumen ejecutivo | §1 |
| Autoridad e insumos | §2 |
| Estado actual del repositorio | §3 |
| Declaración del problema | §4 |
| Origen / Provenance | §5 |
| F-1 Finding | §7 (+ registro formal en secciones finales) |
| Base normativa | §8 |
| Frontera histórica — Plan 98 | §6 |
| Alcance | §9 |
| No-alcance | §10 |
| Clasificación del cambio | §11 |
| Comportamiento actual | §12 |
| Comportamiento requerido | §13 |
| Requisitos del algoritmo GC-1 | §14 |
| Semántica A1/A2 | §15 |
| Semántica de identidad Git | §16 |
| Escenarios adversariales | §17 |
| Plan de testing | §18 |
| Plan de dogfooding | §19 |
| Plan de validación | §20 |
| Plan de anchor | §21 |
| Plan de checkpoint | §22 |
| Trazabilidad C-n | §23 |
| Estrategia de commits | §24 |
| Recovery / stop conditions | §25 |
| Criterios de aceptación | §26 |
| Riesgos | §27 |
| Pending / Open Questions | §28 |
| Execution Gates | §29 |
| Condiciones de cierre | §30 |
| Referencias | §31 |
| Veredicto / readiness | §32 |
| Validation anchor / Checkpoint / C-n / Nota de ejecución | Secciones finales (se completan al ejecutar, no en esta iteración) |

## 1. Resumen ejecutivo

**[NORMATIVE + DERIVED]** Plan 98 (Unidad D / Incremento 4) materializó la
primera automatización operativa del Change Lifecycle DEV: C-1 (lifecycle
anchor checker) y C-2 (lifecycle checkpoint checker)
(`docs/plans/INDEX.md:Trigésima serie: Change Lifecycle DEV — Unidad D / Incremento 4`).
C-2 declara implementar GC-1: "GC-1 compares the closure state with the anchor
of the validation whose validated state is the closure state"
(`tools/check_lifecycle_checkpoint.py`). El C1/C2 Read-Only Audit Report
posterior al cierre de Plan 98 detectó que la **materialización** de esa regla
en C-2 no corresponde a la semántica normativa: la selección del anchor
aplicable usa el **último** estado validado registrado cuando el artifact
declara una revalidación (A2), y la comparación se hace por **pertenencia
genérica** del tree elegido entre **todos** los commits de cierre, en lugar de
identificar el estado de cierre y emparejarlo con la validación cuyo estado
validado lo cubre (hallazgo **F-1**, MAJOR, implementación/materialización;
§5/§7).

**[DERIVED]** Este Plan corrige **únicamente F-1**:

- alcance físico futuro máximo: `tools/check_lifecycle_checkpoint.py` y los
  tests relacionados con C-2 (`tests/test_check_lifecycle_checkpoint.py`),
  más los registros documentales de gobernanza del propio plan al ejecutarse
  (plan + INDEX + changelog `[Unreleased]` si las convenciones lo exigen al
  ejecutar); ver §9;
- la corrección materializa la cadena GC-1:
  `closure state → identificar la validación cuyo estado validado corresponde
  al estado de cierre → comparar contra el anchor de esa validación`
  (§13/§14), preservando tree identity, SHA = locator, no-reachability,
  GAP advisory ≠ ANOMALY, A1 inmutable y A2 con lineage hacia A1
  (§15/§16/§26);
- los escenarios adversariales que demostraron F-1 (Casos A/B/C del audit,
  §6 del encargo) quedan como regresiones obligatorias permanentes (§17/§18);
- el dogfooding del corpus real existente (planes 96/97/98) no sufre
  regresiones de clasificación: continúa sin ANOMALY y con las clasificaciones
  verificadas en la ejecución (§19); no se reescriben registros históricos.

**Veredicto de este artifact:** **PLAN 99 READY FOR IMPLEMENTATION — GO WITH
CONDITIONS** (§32). Condiciones reales (ninguna de diseño, ninguna inventada;
ninguna bloquea esta iteración de creación):

- **C1** — autorización humana para ejecutar la corrección y para los commits
  futuros en `dev` (§28 OQ-1).
- **C2** — aceptación humana de la batería al cierre según la política de
  "batería verde" del plan 94 (§29 Gate 3/Gate 7; §28 OQ-2).
- **C3** — si al implementar aparece una ambigüedad de parseo del corpus
  (texto exacto de declaraciones de revalidación, encabezados, campos) no
  resoluble con las reglas de §14/§17, **STOP** y escalación humana; no se
  inventa regla (§25/§28 OQ-3).
- **C4** — si la ejecución demuestra que la clasificación dogfooding del
  corpus real difiere de las invariantes de §19 (p. ej. GAP nuevo sobre
  planes 96/97/98 no explicado por la semántica corregida), **STOP** antes
  del commit y escalación humana (§25/§28 OQ-4).

Este artifact se crea y registra en esta iteración; el estado de ejecución es
`NOT STARTED` (ver banner de apertura).

## 2. Autoridad e insumos

**[DERIVED]** Orden de precedencia aplicado (repo factual > normativa
`Accepted` > planes ejecutados > convenciones > diseño de trabajo > inferencia
del agente):

1. **Estado factual actual del repositorio** (§3): git, checkers, artifacts,
   registro de Plan 98 y de sus checkers.
2. **RFC-75** `Accepted`: Mecanismo 6 (Validation Anchors), Mecanismo 7 (Git
   Checkpoints: checkpoint = relación, consistencia contra el anchor de la
   validación cuyo estado validado corresponde al estado de cierre; SHA =
   locator), Mecanismo 8 (findings/corrections/revalidation como relaciones de
   lineage), Mecanismo 12 (post-close por referencia; `Closed` nunca se
   reabre), Mecanismo 14 (safe automation; `checker output = factual evidence
   ≠ normative authority`; GAP), Mecanismo 15 (legacy; ausencia de campos =
   legacy, no invalidez), invariantes VC-1/GC-1 y rollout incremental.
3. **ADR-15**: CL-1 (anchorability), CL-2 (validez relativa al anchor),
   CL-3 (cierre Git-verificable), CL-4 (`Executed` no implica commit),
   CL-5 (`Committed` es estado del repo), CL-6/CL-7 (lineage de correcciones),
   CL-8 (registros no eliminados), CL-9 (decision lineage), CL-10 (escala por
   impacto).
4. **ADR-16**: AU-1..AU-7; clases FACTUAL/NORMATIVE/DECISION/RELEASE/
   DESCRIPTIVE; checker = evidencia factual; INDEX descriptivo; AU-3 (no
   auto-resolución por código).
5. **RFC-46**: no retroactividad y trazas históricas no reescribibles.
6. **RFC-56**: clases A/B/C; no aplica a este plan (no toca
   `protocol/.agents/`).
7. **RFC-69**: taxonomía documental y versionado docs-only.
8. **Plan 94** `Executed`: roadmap incremental, política de "batería verde"
   (§24.1), dogfooding y criterios de cierre de la serie.
9. **Planes 96/97** `Executed` + `Closed`: formato v1 de Validation
   Anchor/SCI, checkpoint y semántica A1/A2/A2-no-muta-A1 (Decisión B).
10. **Plan 98** `Executed` + `Closed` (docs-only): especificación C-1/C-2,
    reglas R-C2-1..R-C2-7, población del régimen, testing y dogfooding;
    origen histórico de F-1. **Plan 98 no se modifica** (§6).
11. **C1/C2 Read-Only Audit Report** (2026-09-02): origen de F-1; artefacto
    de sesión no versionado; **insumo**, no fuente normativa.
12. **`docs/CONVENTIONS.md`**, **`docs/VERSIONING.md`**, **`AGENTS.md`** raíz
    y **`docs/AGENTS.md`**: hogar normativo/operativo donde viven VC-1/GC-1/
    LC-1/PC-1, el ciclo de status de planes y el DoD.

Regla de conflicto: si durante la planificación o la ejecución aparece una
contradicción real entre este plan y una fuente normativa, el ejecutor **no
resuelve unilateralmente**: documenta la contradicción, se detiene si afecta la
ejecutabilidad y marca `HUMAN DECISION REQUIRED` (AU-3;
`docs/adr/16-change-lifecycle-authority.md:Invariantes`). No se detectó
ninguna contradicción en esta iteración (§32).

## 3. Estado actual del repositorio (reconstrucción factual)

**[OBSERVED]** Verificado al crear este plan (2026-09-02, read-only sobre el
repo):

| Dato | Valor | Evidencia |
|---|---|---|
| Branch / HEAD | `dev` / `aa68704cbc293a38cb7814cfac72bd531eee9721` (plan 98: registro de anchor y checkpoint) | `git status`, `git rev-parse HEAD` |
| vs `origin/dev` | en sync (sin commits propios pendientes) | `git status` |
| Working tree | limpio antes de esta iteración | `git status --porcelain` |
| VERSION del payload | `10.3.0` | `protocol/.agents/VERSION` |
| Plan 98 | `Executed` + condición derivada `Closed` (docs-only, sin release); commits C1 `669a576` (C-1), C2 `9b5b8a1` (C-2), C3 registro `aa68704` | INDEX + git log + archivo |
| Último plan existente | 98 | `docs/plans/INDEX.md`; `rg --files docs/plans` |
| **Siguiente número libre** | **99** | secuencia cronológica de ejecución (`docs/CONVENTIONS.md:Convenciones`) |
| C-2 (checkpoint checker) | existe: `tools/check_lifecycle_checkpoint.py` (21 escenarios en `tests/test_check_lifecycle_checkpoint.py`) | `git log`, archivos |
| C-1 (anchor checker) | existe: `tools/check_lifecycle_anchor.py` (19 escenarios) | archivos |
| RFC-75 / ADR-15 / ADR-16 | `Accepted`, intactos | docs + INDEX |
| Corpus del régimen C-2 | planes 96/97/98 (regime members con `## Validation anchor` y `## Checkpoint`/`## Checkpoint / cierre`) | `rg` + dogfooding de Plan 98 |
| Dogfooding actual de C-2 (registrado) | planes 96/97 `VALID`; plan 98 `VALID` tras cierre; legacy 01–95 `EXCLUDED`; GAP=0; ANOMALY=0 | `docs/plans/98-change-lifecycle-unit-d-increment-4.md:Nota de ejecución` |
| pytest (baseline reportado) | `380 passed, 0 failed` (Plan 98) | INDEX Trigésima serie |
| Registries / entidades lifecycle | ninguno | `rg` |
| `.agents/` en raíz | **NO existe** | `Test-Path` |
| `protocol/.agents/` | existe; payload del Protocol, **fuera de scope** | estructura del repo |

**Precondiciones de ejecución (F0):** el estado de §3 debe sostenerse al
ejecutar (branch `dev`; planes 94–98 en su estado registrado; Decisión B
commiteada; árbol limpio salvo los cambios del propio plan); la batería de §20
corre en verde o con desviación documentada aceptada por el mantenedor
(§28 OQ-2).

## 4. Declaración del problema

**[NORMATIVE + DERIVED]** GC-1 exige que la consistencia del cierre se evalúe
contra el anchor de la validación **cuyo estado validado corresponde al estado
de cierre**, y no contra otro anchor:

> `Closed` exige que la identidad scoped del estado de cierre sea igual a la
> del anchor de la validación cuyo estado validado corresponde al estado de
> cierre […] Si existe una revalidación A2 sobre el estado de cierre, la
> consistencia se evalúa contra A2; si el estado de cierre sigue siendo el
> estado de A1, contra A1. La existencia de A2 no elimina A1.
> (`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`)

La especificación de C-2 en Plan 98 incorporó esa regla como R-C2-1
(`docs/plans/98-change-lifecycle-unit-d-increment-4.md:11. C-2 — Lifecycle Checkpoint Checker`).
La implementación actual de C-2 **no la materializa**: en
`tools/check_lifecycle_checkpoint.py`, el bloque GC-1 selecciona el anchor
aplicable como el **último** estado validado registrado (`state_trees[-1]`)
cuando el artifact declara revalidación, y compara ese tree contra **cualquier**
tree de los commits de cierre (`applicable not in closing_trees`), no contra el
estado de cierre final (§12). Consecuencias observables:

- falsa **ANOMALY** cuando el estado de cierre corresponde a A1 o al primer A2
  y existe un A2 posterior cuyo tree no figura entre los commits de cierre
  (Casos A/B adversariales del audit);
- falsa **validación** (VALID) cuando el estado de cierre no corresponde a
  ninguna validación aplicable pero el tree de A1 figura entre commits
  intermedios de cierre (Caso C / AC-5);
- el anchor aplicable reportado/verificado no se determina por correspondencia
  de estados, violando la semántica normativa aunque el veredicto de exit code
  pueda coincidir por casualidad en algunas construcciones (pertenencia
  genérica del tree).

F-1 es un defecto de **implementación/materialización**, no una ambigüedad
normativa (decisión D3 del encargo): la normativa ya establece la relación
`closure state ↕ validated state → corresponding validation anchor`. No se
modifica RFC-75, ADR-15 ni ADR-16.

## 5. Origen / Provenance

**[DERIVED]** Cadena histórica de F-1 (decisiones D1/D2 del encargo, cerradas):

```text
Plan 98 CLOSED (docs-only, 2026-09-02)
    ↓
post-close audit (C1/C2 Read-Only Audit Report, read-only)
    ↓
F-1 discovered (MAJOR; implementación/materialización de GC-1 en C-2)
    ↓
Plan 99 (este artifact; corrección post-close)
```

- **Origin artifact:** Plan 98 (`docs/plans/98-change-lifecycle-unit-d-increment-4.md`),
  en su estado `Closed` histórico.
- **Source:** C1/C2 Read-Only Audit Report posterior a la ejecución/cierre de
  Plan 98; artefacto de sesión no versionado en el repo (insumo, no fuente
  normativa).
- **Finding:** F-1 (namespace del audit); severidad MAJOR; clasificación
  implementación/materialización defect.
- **No retroactividad:** la existencia posterior de F-1 no invalida
  retrospectivamente Plan 98, sus anchors, sus checkpoints, sus commits ni sus
  notas históricas (§6); la corrección se autoriza por este Plan nuevo, no por
  la evidencia (§23).
- **Serie:** Change Lifecycle DEV (RFC-75); este Plan no crea serie ni
  registry: la membresía se deriva de la referencia RFC↔Plan
  (`docs/CONVENTIONS.md:Change Lifecycle — Serie e identidad derivada (regla operacional; Incremento 1)`).

## 6. Frontera histórica — Plan 98 (no retroactividad)

**[NORMATIVE + DERIVED]** Este Plan preserva explícitamente la historia
(decisión D1/D2 y §20 del encargo):

- **Plan 98 permanece CLOSED**; no se reabre, no se modifica su status, su
  execution report, sus closure records, sus anchors históricos, su evidencia,
  sus commits ni sus notas históricas.
- La existencia de F-1 es **posterior** a la ejecución/cierre de Plan 98 y no
  reinterpreta la ejecución original.
- Los anchors y checkpoints de los planes 96/97/98 permanecen históricos; la
  corrección **no reutiliza** el anchor de Plan 98 como anchor propio de este
  Plan (§21/§22).
- F-1 no es un defecto de los registros históricos ni de la normativa: es un
  defecto de materialización del checker; los registros históricos se leen bajo
  las reglas con las que se produjeron y no se reescriben
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).
- Cambios posteriores al cierre no invalidan un checkpoint: generan artifacts
  nuevos que referencian al cerrado
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 12 — Post-close Changes`).

## 7. F-1 — Finding

**[DERIVED]** Registro formal del hallazgo en este artifact (post-close por
referencia; namespace del artifact; sin entidad global `Finding`; reglas
operativas del Incremento 2:
`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`).
La entrada completa vive en la sección final `## Findings / Correcciones /
Pending`; aquí se resumen identidad y hechos:

- **Ref calificada en este artifact:** `<PLAN-99>:F-1` (preserva el número del
  audit F-1 en el namespace del artifact que registra).
- **Tipo:** post-close finding.
- **Origin:** Plan 98 (CLOSED).
- **Source:** C1/C2 Read-Only Audit Report (read-only, posterior a Plan 98).
- **Severity:** MAJOR.
- **Classification:** implementation/materialization defect (no ambigüedad
  normativa; D3).
- **Observación:** C-2 selecciona el anchor aplicable por recencia (`latest A2
  wins`) y compara por pertenencia genérica del tree entre los commits de
  cierre, en lugar de identificar el estado de cierre y seleccionar el anchor
  de la validación cuyo estado validado corresponde a ese estado (GC-1).
- **Estado:** `open` (este Plan es la autorización normativa para corregirlo;
  la resolución/metadata se actualiza al ejecutar; el cierre del finding se
  registra con evidencia en la sección final).
- **F-2…F-9:** permanecen **deferidos** y fuera del alcance de este Plan
  (§10); no se convierten silenciosamente en scope.

## 8. Base normativa

**[NORMATIVE]** Fuentes que este Plan implementa sin modificar:

| Fuente | Regla relevante |
|---|---|
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints` | checkpoint = relación closure↔estado Git; consistencia con la identidad scoped del anchor correspondiente; SHA = locator |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors` | anchor representa el estado relevante de una validación; validez relativa al anchor (CL-2) |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 8 — Findings / Corrections / Revalidation` | lineage post-close por referencia; A2 referencia A1; corrección registrada en artifact que la posee |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 12 — Post-close Changes` | `Closed` no se reabre; la nueva acción referencia al cerrado |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation` | checker output = evidencia factual ≠ autoridad; GAP ≠ invalidación |
| RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy` | ausencia de campos nuevos = legacy, no invalidez; sin backfill obligatorio |
| CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)` | GC-1 operacional: consistencia contra el anchor de la validación cuyo estado validado corresponde al estado de cierre; A2 sobre el estado de cierre → contra A2; A1 si el estado de cierre sigue siendo el de A1; A2 no elimina A1 |
| CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)` | campos v1, tree identity, SHA = locator, revalidación A2 propia con referencia a A1 |
| CONVENTIONS `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)` | refs calificadas; C-n = registro FACTUAL no autoritativo |
| ADR-15 `docs/adr/15-change-lifecycle-continuity.md:Invariantes` | CL-1…CL-10 |
| ADR-16 `docs/adr/16-change-lifecycle-authority.md:Invariantes` | AU-1…AU-7; checker = factual; INDEX descriptivo |
| VERSIONING `docs/VERSIONING.md:7. Estados de planes y RFCs` | semántica de condiciones derivadas; consistencia de cierre contra el anchor correspondiente |
| VERSIONING `docs/VERSIONING.md:10. Definition of Done` | anchor + checkpoint + consistencia GC-1; docs-only sin release (RFC-69) |
| RFC-46 / RFC-69 / RFC-56 | trazas históricas; taxonomía/docs-only; clases de payload (no aplica) |

Este Plan **no** crea RFC ni ADR, no enmienda RFC-75 y no modifica ADR-15/16
(decisión D6): la corrección implementa normativa existente.

## 9. Alcance exacto

### 9.1 Esta iteración de planificación (incluido ahora)

**[PROPOSED — esta iteración]** Creación física del Plan 99 en
`docs/plans/99-change-lifecycle-f1-c2-gc1-correction.md` y su registro en
`docs/plans/INDEX.md` (nueva serie del INDEX; requisito estructural del mirror,
`tools/check_plan_structure.py`). No implementa F-1, no ejecuta commits y no
modifica ninguna fuente normativa ni de código (secciones finales sin
anchor/checkpoint fabricados).

### 9.2 Ejecución futura del plan (incluido entonces; NO se ejecuta ahora)

**[PROPOSED — Future Implementation]** La ejecución autorizada del Plan 99
corrige **exclusivamente** la materialización de GC-1 en C-2:

- archivo a corregir: `tools/check_lifecycle_checkpoint.py` (bloque GC-1 de
  `classify_checkpoint` y docstring si refleja la semántica corregida);
- tests a corregir/añadir: `tests/test_check_lifecycle_checkpoint.py`
  (regresiones F-1 obligatorias §17/§18; actualizaciones de aserciones de
  razones cuando el mensaje de clasificación cambie, sin alterar las
  clasificaciones esperadas de la suite existente);
- registros documentales de gobernanza del propio plan al ejecutar: este
  artifact (secciones finales), `docs/plans/INDEX.md` (espejo) y
  `CHANGELOG.md:[Unreleased]` si las convenciones lo exigen al ejecutar
  (ítem `(plan 99, RFC-75)`; precedente planes 95–98).

Regla transversal de la ejecución futura: **modificar solamente los archivos
estrictamente necesarios**.

### 9.3 Excluido incluso en la ejecución futura

Resumen de exclusiones absolutas; detalle completo en §10. En particular, la
ejecución futura **no** corrige C-1 (`tools/check_lifecycle_anchor.py`), no
modifica F-2…F-9, no crea `C-n` durante la implementación (solo al cerrar,
§23), no agrega los checkers a la batería canónica, no crea CI, no introduce
registries/state machines/métricas y no toca `protocol/`, `runtime/`,
`.agents/`, `dist/` ni el harness.

## 10. Fuera de alcance (out of scope)

**[NORMATIVE]** El Plan 99 **no** incluye, ni en esta iteración ni en su
ejecución futura:

- F-2…F-9 del C1/C2 Read-Only Audit Report (deferidos; decisión D5);
- reapertura o modificación de Plan 98 (estado, execution report, closure
  records, anchors, evidencia, commits, notas); decisión D1;
- modificación de RFC-75 (incluido su Amendment Log), ADR-15 o ADR-16;
  decisión D3/D6;
- modificación de C1 (`tools/check_lifecycle_anchor.py`) ni de sus tests;
- creación de `C-n` en esta iteración (§23);
- implementación de la corrección, commits o push;
- modificación de `protocol/.agents/` ni creación de `.agents/` en la raíz;
- introducción de runtime/harness orchestration, registry, state machine,
  base de datos, CI, métricas, telemetría ni entidades nuevas
  (`docs/rfc/75-change-lifecycle.md:No-objetivos`);
- cambio de `VERSION`, creación de release/tag, promoción a `master`
  (§11/§30);
- requisitos nuevos de reachability desde `dev`/`origin` (§16);
- cambios normativos sobre GAP/ANOMALY (§13/§14);
- rediseño de la población del régimen (señales estructurales de Plan 98
  permanecen).

## 11. Clasificación del cambio

### 11.1 Clase RFC-56

**[DERIVED]** No aplica: el cambio no toca `protocol/.agents/`; es un cambio
DEV-only del repo fuente (tooling + tests + registros documentales). Sin
`VERSION` bump ni tag: la ejecución es docs/tools-only y se registra bajo
`[Unreleased]` del changelog (RFC-69; `docs/VERSIONING.md:3. Versionado`).

### 11.2 Change Level

**[PROPOSED]** Clasificación prospectiva declarada al crear el plan (regla
operacional de intake;
`docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)`):

| Dimensión | Valor | Justificación |
|---|---|---|
| coordination | 1 | Un solo cambio DEV de la serie cerrada; un ejecutor |
| scope | 2 | Corrección de checker + suite de tests en `tools/` y `tests/` (dos capas del repo; precedente Plan 98 §19) |
| architectural impact | 1 | Corrección interna, local y reversible de un checker factual/advisory; sin módulo, seam ni contrato nuevo |
| release impact | 1 | Sin payload, sin `VERSION`, sin tag; ítem changelog-only al ejecutar |
| duration/complexity | 2 | Semántica Git/GC-1 sutil + suite de regresiones adversariales + dogfooding + anchor/checkpoint propio |
| **Level = max** | **L2** | `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels` |

La clasificación es mutable con justificación documentada (upgrade obligatorio
ante triggers; downgrade con nota). Change Level ≠ clase RFC-56 (ejes
independientes; `docs/CONVENTIONS.md:Change Lifecycle — Change Levels (modelo objetivo)`).

## 12. Comportamiento actual (defectuoso)

**[OBSERVED + DERIVED]** En `tools/check_lifecycle_checkpoint.py`, la lógica
GC-1 actual equivale conceptualmente a:

```text
anchors
   ↓
collect state trees (State identity del Validation Anchor, en orden del documento)
   ↓
si revalidación declarada y hay ≥ 2 state trees:
    applicable = state_trees[-1]          # latest A2 wins
sino:
    applicable = state_trees[0]           # A1
   ↓
si applicable no pertenece al conjunto de trees de los commits de cierre:
    inconsistencia (PASS → ANOMALY; sin PASS → GAP)
```

Defectos de materialización identificados por F-1:

- **D-A — selección por recencia.** `applicable = state_trees[-1]` elige el
  último estado validado registrado cuando el artifact declara revalidación
  (señal `A2`/`V2`/`revalidaci[oó]n` en Validity/stale o Consistencia), sin
  comprobar que el estado validado de esa revalidación corresponda al estado de
  cierre. La existencia de un A2 posterior altera la selección aunque el cierre
  corresponda a A1 o a un A2 anterior.
- **D-B — pertenencia genérica del tree.** La comparación
  `applicable not in closing_trees` evalúa si el tree del anchor elegido figura
  entre **cualquiera** de los commits de cierre, no si el **estado de cierre**
  (estado del último commit de cierre) coincide con el estado validado del
  anchor correspondiente. Un A1 cuyo tree figura en un commit intermedio
  "valida" un cierre cuyo estado final es distinto (falsa validación); y un A2
  reciente cuyo tree no figura produce anomalía aunque el cierre corresponda a
  A1/A2 anterior (falsa anomalía).
- **D-C — sin identificación del estado de cierre ni reporte del anchor
  aplicable.** La implementación no deriva el estado de cierre como el tree del
  commit de cierre final y no expone en el reporte qué anchor aplicó
  (A1/A2), impidiendo auditar la correspondencia.

Consecuencias sobre los casos adversariales del audit (§17), ejecutados sobre
la implementación actual:

| Caso adversarial | Construcción | Clasificación actual (defectuosa) |
|---|---|---|
| Caso A (variante con tree de A2 entre commits) | A1→T1, A2→T2; cierre T1 con commits C1(T1), C2(T2), C3(T1) | VALID con anchor erróneo (A2/latest); no se reporta A1 |
| Caso A (variante sin tree de A2 entre commits) | A1→T1, A2→T2; cierre T1; commits C1(T1), C2(sin T2) | **ANOMALY falsa** (A2/latest elegido por recencia) |
| Caso B | A1→T1, A2a→T2, A2b→T3; cierre T2; T3 no figura entre commits | **ANOMALY falsa** (A2b elegido) |
| Caso C (multi-commit) | A1→T1; cierre T2; commits C1(T1), C2(T2); PASS + Closed; sin A2 | **VALID falsa** (T1 ∈ closing trees) |
| Caso C (commit único, ya cubierto) | A1→T1; cierre T2; commit único C1(T2); PASS + Closed | ANOMALY (única construcción que la suite actual detecta) |

La suite actual (`tests/test_check_lifecycle_checkpoint.py`, 21 escenarios)
no contiene los Casos A/B/C multi-commit; el único caso de cierre sin
correspondencia usa commit único y por eso la falsa validación multi-commit
no está cubierta (brecha de regresión que F-1 exige cerrar; §17/§18).

## 13. Comportamiento requerido

**[NORMATIVE]** La corrección debe materializar:

```text
closure state
      ↓
identify validation whose validated state matches closure state
      ↓
identify that validation's anchor
      ↓
compare closure state against that anchor
```

El criterio fundamental (decisión D3; AC-1):

> **GC-1 debe seleccionar el anchor correspondiente a la validación cuyo estado
> validado coincide con el estado de cierre.**

La selección **no** puede depender de:

- recencia (p. ej. "latest A2");
- posición textual o de lista de los anchors;
- pertenencia genérica del tree a cualquier commit de cierre;
- reachability o ancestría;
- SHA como identidad semántica.

La distinción **GAP vs ANOMALY** se conserva (§11 del encargo;
`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`):

- **GAP** = evidencia insuficiente; advisory; no implica inconsistencia; exit 0.
- **ANOMALY** = evidencia suficiente de una contradicción real; failure; exit 1.
- La ausencia de evidencia no se convierte automáticamente en anomalía.

## 14. Requisitos del algoritmo GC-1 corregido (reglas R-99-x)

**[PROPOSED — Future Implementation]** La implementación corregida de C-2
reemplaza el bloque GC-1 de `classify_checkpoint` (D-A/D-B/D-C de §12) por las
siguientes reglas deterministas. Cada regla tiene criterio observable; no se
usan frases vagas.

### R-99-1 — Commit de cierre final

El campo "Commits de cierre" es una **lista ordenada** (bullets `C1…Cn` en
orden documental). El **último ítem** de la lista es el commit de cierre final
del Plan. Un commit intermedio **nunca** define el estado de cierre.

Criterio observable: dado el texto del campo, el último bullet resuelto es el
final; los anteriores no pueden satisfacer la correspondencia GC-1 por sí
solos.

### R-99-2 — Resolución del estado de cierre

El estado de cierre es el tree id del commit de cierre final, resuelto con
primitivas Git locales read-only (`git rev-parse --verify --quiet <sha>^{tree}`),
cuando ese locator existe en el registro:

- (a) si el locator del commit final resuelve, `closure_state = tree(final)`.
- (b) si el registro declara un literal "Estado de cierre" (tree id) y el
  estado de (a) es conocido, el literal **debe** ser igual a `tree(final)`;
  si difiere → **ANOMALY** (evidencia contradictoria). La comparación del
  literal se hace contra el commit **final**, nunca contra la pertenencia a
  cualquier commit de la lista (corrige D-B sobre literales).
- (c) si el locator del commit final no está en el registro (convención
  corpus: commit de registro identificado por mensaje, sin auto-embebido de su
  identidad; planes 96–98) y no hay literal → el estado de cierre por tree es
  **UNKNOWN**; la correspondencia se evalúa por la regla de declaración
  R-99-5 y, si no aplica, se clasifica GAP (R-99-6).

Criterio observable: para cada artifact, la implementación determina unívocamente
`closure_state` (tree) o `UNKNOWN` con el motivo declarado.

### R-99-3 — Estados validados (anti-circularidad)

Los candidatos de "estado validado" se toman **solo** de la sección
`## Validation anchor` del artifact (registro de la validación), nunca del
registro de cierre:

- (a) trees embebidos en bullets `State identity` del SCI, en orden de
  registro (A1 primero; cada A2 en el orden en que aparece en el documento);
- (b) revalidaciones declaradas **en la propia sección del anchor**
  (Validity/stale y/o bloques A2) cuyo sujeto de estado validado refiere al
  estado de cierre / contenido final / commit de cierre final del Plan
  (patrón corpus de los planes 96–98, p. ej. "revalidada por V2 sobre el
  contenido final C2 antes del cierre").

Prohibido (anti-circularidad, §10 del encargo): derivar el estado validado de
la propia evidencia de cierre ("closure record → contiene su propio tree final
→ el checker confía en ese tree"). El checker **no** toma como evidencia de
validación un tree literal contenido en el registro de cierre; el tree del
estado de cierre, cuando se conoce, proviene de Git (hecho externo read-only).

Criterio observable: la implementación itera únicamente bloques de la sección
`## Validation anchor` para construir la lista de validaciones; el registro de
cierre solo aporta locators/literales del estado de cierre (R-99-2) y señales
de PASS/FAIL/Closed (R-99-7), nunca estados validados.

### R-99-4 — Correspondencia por identidad (Tier 1, primaria)

Si `closure_state` es conocido, el anchor aplicable es la **primera** validación
registrada (en orden de registro; A1 primero) cuyo tree de estado validado
embebido sea **igual** al estado de cierre (tree identity). La selección es por
igualdad de estado, **nunca** por la última posición de la lista ni por
recencia:

- cierre == estado de A1 (aunque existan A2 posteriores) → aplicable **A1**
  (Caso A);
- cierre == estado del primer A2 (aunque exista un A2 posterior) → aplicable
  **ese A2** (Caso B);
- cierre == estado del segundo A2 → aplicable ese A2; la recencia no decide.

Si varias validaciones registran el mismo tree (re-ejecución sobre el mismo
estado, que según la Decisión B debería ser nota y no A2), aplica la primera en
orden de registro; no es discrepancia por sí misma salvo contradicción
explícita.

Criterio observable: dada una lista de pares `(etiqueta, tree)` y un
`closure_state`, la implementación elige el primer par con tree igual; nunca
accede al último elemento por defecto.

### R-99-5 — Correspondencia declarada (Tier 2, patrón corpus v1)

Si Tier 1 no produce match (porque `closure_state` es `UNKNOWN` o ningún tree
embebido coincide), el anchor aplicable puede ser la revalidación declarada
**única** que cumpla todas estas condiciones:

1. la sección `## Validation anchor` declara exactamente **una** revalidación
   (A2/V2) cuyo sujeto de estado validado refiere al estado de cierre del Plan
   (contenido final / estado final staged antes del cierre / commit de cierre
   final); el patrón del corpus 96–98 es la referencia explícita al cierre
   ("sobre el contenido final C2 antes del cierre", "sobre el contenido final
   de la Unidad D", "sobre el estado final staged antes del commit");
2. la revalidación referencia a A1 (lineage presente; regla R-99-8);
3. la consistencia del checkpoint declara **PASS** para esa revalidación
   antes de `Closed` (regla R-99-7);
4. no existe contradicción con trees embebidos presentes (si un A2 embebido
   declara un estado distinto del cierre y el texto lo declara como cubriendo
   el cierre → evidencia contradictoria; ver R-99-6).

Si más de una revalidación declarada califica (ambigüedad) o ninguna → **no
aplica Tier 2** (R-99-6).

Esta regla reconoce la convención de no auto-embebido del tree final en los
registros de cierre (planes 96–98) y trata el registro de la validación en la
sección del anchor como evidencia declarada de su propio alcance (modelo de
evidencia declarada ya usado por C-2 para PASS), sin convertir el registro de
cierre en fuente del estado validado (R-99-3).

Criterio observable: para el corpus real, planes 96/97/98 producen un match
Tier 2 (única V2 declarada con sujeto = cierre, lineage A1, PASS) → `VALID`
con anchor aplicable A2 (declarado), sin ANOMALY (§19).

### R-99-6 — Sin validación aplicable → GAP / ANOMALY

Cuando no existe validación aplicable (ni Tier 1 ni Tier 2) para el estado de
cierre:

- si la consistencia declara **PASS** para el cierre y/o la condición declara
  **Closed** → **ANOMALY** (contradicción real: PASS/Closed afirma evidencia de
  validación que ningún registro de validación del artifact provee para ese
  estado; Caso C / AC-5);
- si la evidencia es insuficiente (estado de cierre `UNKNOWN` sin Tier 2, o
  ambigüedad de Tier 2 con ≥ 2 revalidaciones declaradas sin trees embebidos,
  o sin PASS declarado) → **GAP** (advisory; exit 0; no se convierte ausencia
  de evidencia en anomalía);
- si existe evidencia contradictoria dentro de Tier 2 (p. ej. una revalidación
  declarada cubre el cierre pero su estado embebido es distinto del cierre con
  PASS declarado) → **ANOMALY** (información presente pero incompatible).

Criterio observable: cada uno de los escenarios de §17 produce exactamente la
clasificación esperada de su fila.

### R-99-7 — PASS / Closed (sin cambios)

- `Closed` declarado sin evidencia PASS en el registro del checkpoint → GAP.
- `Closed` declarado junto a FAIL explícito → ANOMALY.
- PASS declarado para el cierre sin validación aplicable → R-99-6.

### R-99-8 — Lineage A2 (sin cambios)

Revalidación (A2/V2) declarada sin referencia al anchor original (A1/V1) →
**ANOMALY**.

### R-99-9 — Identidad Git y alcance (sin cambios)

- Tree identity = identidad material; SHA = locator; mismo tree con SHA
  distinto → válido; tree distinto → evaluación de aplicabilidad, nunca
  invalidación automática (CL-2).
- Sin requisitos de reachability desde `dev`/`origin`; objetos locales válidos
  no alcanzables → válidos.
- Checker read-only, local, sin red, stdlib + git read-only; sin autoridad
  normativa (R-C2-7).

### R-99-10 — Reporte auditable del anchor aplicable

El reporte de `VALID` debe identificar el anchor aplicable de forma
determinista (p. ej. razón "checkpoint consistent with the applicable
validation anchor (GC-1): A1" / "…: A2" / "…: A2 (declared)"). Las
clasificaciones (`VALID`/`GAP`/`ANOMALY`/`N/A`/`BOUNDARY`/`EXCLUDED`) y la
semántica de exit code (0 salvo ANOMALY) no cambian. El reporte no fabrica
evidencia: la etiqueta del anchor se deriva de la regla aplicada
(R-99-4/R-99-5).

Criterio observable: los tests de regresión F-1 asertan la etiqueta del anchor
en la razón de `VALID` (Casos A/B) y la ausencia de ANOMALY.

## 15. Semántica A1/A2 (obligatoria)

**[NORMATIVE]** Se preserva exactamente la decisión arquitectónica ya tomada
(Decisión B `fc52c88`;
`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`):

- A1 = anchor original de la primera validación; A2 = anchor de una
  revalidación.
- **A2 no muta ni reemplaza A1**: A1 conserva su significado histórico y nunca
  se reescribe ni se reinterpreta.
- **A2 referencia A1** (lineage `A1 → A2`); representa una validación
  independiente.
- La corrección **prohíbe** explícitamente una implementación que destruya o
  sustituya A1 cuando aparece A2.
- El cierre se evalúa contra A1 si el estado de cierre es el de A1, aunque
  existan A2 posteriores (AC-3/AC-9); contra el A2 cuyo estado revalidado es el
  estado de cierre, aunque existan A2 posteriores (AC-4/AC-10).

## 16. Semántica de identidad Git

**[NORMATIVE]** Se mantiene el modelo existente:

- **Tree identity** = identidad material del estado Git.
- **Commit SHA** = locator, nunca identidad semántica.
- El Plan no autoriza usar SHA como identidad semántica, exigir ancestry, ni
  exigir reachability desde `dev` o `origin/dev`.
- El checker permanece read-only (sin escritura, sin red).

(`docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`;
`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`).

## 17. Escenarios adversariales obligatorios

**[PROPOSED — Future Implementation]** Los siguientes escenarios se convierten
en regresiones permanentes de la suite C-2. La columna "esperado" es el
comportamiento exigido por GC-1 (§13/§14); sobre la implementación actual
producen los resultados defectuosos de §12.

### 17.1 Casos A/B/C del audit (obligatorios)

| Caso | Fixture (resumen) | Resultado esperado |
|---|---|---|
| A | A1 → T1; A2 → T2; cierre → T1 (commit final con tree T1; T2 puede existir o no entre commits de cierre) | `VALID`; anchor aplicable = **A1**; nunca ANOMALY por la existencia posterior de A2 |
| B | A1 → T1; A2a → T2; A2b → T3; cierre → T2 (commit final con tree T2; T3 no figura entre commits de cierre) | `VALID`; anchor aplicable = **A2** (el que valida T2); nunca A2b por ser más reciente; nunca ANOMALY |
| C | A1 → T1; cierre → T2; no existe validación correspondiente a T2; consistencia declara PASS y/o condición `Closed` | **ANOMALY** (contradicción real: PASS/Closed sin validación aplicable); variante sin PASS → **GAP** |

### 17.2 Casos adicionales obligatorios (requeridos por el encargo)

| # | Escenario | Resultado esperado |
|---|---|---|
| 1 | Múltiples anchors (A1 + A2a + A2b embebidos) | Selección por igualdad de estado (R-99-4); sin recencia |
| 2 | Múltiples commits de cierre | Solo el commit final define el estado de cierre (R-99-1/R-99-2) |
| 3 | Mismo tree con SHA diferente | `VALID` (tree identity; SHA = locator) |
| 4 | Commit válido pero no alcanzable desde `dev` | `VALID` (sin reachability) |
| 5 | Ausencia de anchor aplicable | GAP (insuficiente) o ANOMALY (PASS/Closed contradictorio), según R-99-6 |
| 6 | Mismatch entre validated state y closure state | ANOMALY cuando PASS declarado; GAP si evidencia insuficiente |
| 7 | Preservación de A1 | A1 no mutado ni reemplazado; cierre sobre estado de A1 → VALID/A1 pese a A2 posterior |
| 8 | Preservación de A2 | Cada A2 conserva lineage hacia A1 y su estado; cierre sobre su estado → VALID con ese A2 |
| 9 | Múltiples revalidaciones independientes | Correspondencia por estado; ambigüedad sin trees embebidos → GAP (R-99-5/R-99-6) |
| 10 | Verdadera anomalía de checkpoint | ANOMALY: p. ej. literal de cierre ≠ tree del commit final; PASS sin validación aplicable; FAIL + `Closed`; A2 sin A1 |

No se introducen requisitos nuevos de reachability en ningún escenario.

## 18. Plan de testing (ejecución futura)

**[PROPOSED — Future Implementation]** Tests deterministas con `pytest` +
`tmp_path` y repositorios Git temporales (mismas convenciones de la suite C-2
existente); sin red; sin dependencia de `origin` ni de la rama `dev`.

### 18.1 Suite existente

Los **21 escenarios existentes** de `tests/test_check_lifecycle_checkpoint.py`
conservan sus clasificaciones esperadas (verificación de §12 en el análisis de
este plan): `VALID`/`ANOMALY`/`GAP`/`N/A`/`EXCLUDED` se mantienen para cada
test. Pueden ajustarse únicamente:

- aserciones de texto de razones cuando el mensaje cambie por la corrección
  (p. ej. la razón de ANOMALY de cierre sin correspondencia ya no contendrá
  "inconsistent with the applicable anchor (A1)" porque ya no existe
  "anchor aplicable" en ese caso; pasa a la razón de R-99-6);
- el docstring/helpers si la semántica lo requiere.

### 18.2 Regresiones F-1 obligatorias (nuevas)

Al menos los siguientes tests nuevos (nombres indicativos; el ejecutor puede
ajustarlos a la convención de la suite):

1. `test_closure_on_a1_state_with_later_a2_is_valid_anchor_a1` — Caso A;
   aserta `VALID` y razón con anchor **A1**; sin ANOMALY.
2. `test_closure_on_a1_state_with_later_a2_not_in_closing_trees_is_valid_anchor_a1`
   — Caso A (variante sin tree de A2 entre commits); aserta `VALID` + A1
   (sobre la implementación actual produce ANOMALY falsa).
3. `test_closure_on_first_a2_with_later_a2_is_valid_anchor_a2` — Caso B;
   aserta `VALID` + A2 (sobre la implementación actual produce ANOMALY falsa
   por recencia).
4. `test_closure_state_without_corresponding_validation_and_pass_is_anomaly`
   — Caso C multi-commit; aserta ANOMALY (sobre la implementación actual
   produce VALID falsa).
5. `test_closure_state_without_corresponding_validation_without_pass_is_gap`
   — Caso C sin PASS; aserta GAP y exit 0 (GAP ≠ invalidación).
6. `test_declared_closure_tree_must_match_final_closing_commit_not_any_commit`
   — literal de cierre = tree de un commit intermedio ≠ tree final → ANOMALY
   (sobre la implementación actual: sin discrepancia por pertenencia).
7. `test_corpus_declared_revalidation_over_final_state_is_valid` — patrón
   corpus v1 (A1 embebido + V2 declarada sobre el contenido final sin tree
   embebido; commit final sin locator) → `VALID` + anchor A2 (declarado);
   protege la invariante de dogfooding del corpus real (§19).
8. `test_multiple_declared_revalidations_without_embedded_trees_are_gap` —
   ambigüedad Tier 2 → GAP (no VALID falsa, no ANOMALY sin contradicción).
9. `test_multiple_embedded_revalidations_selection_by_state_not_recency` —
   A2a→T2 y A2b→T3 embebidos; cierre T2 → `VALID` (selección por estado).
10. `test_valid_unreachable_commit_unchanged` y
    `test_same_tree_different_sha_unchanged` — regresiones de §16 (se cubren
    con los tests existentes 4/17; se mantienen).
11. `test_real_repo_dogfooding_no_regression` — actualiza el test de
    dogfooding real: planes 96/97/98 sin ANOMALY/GAP/EXCLUDED (clasificaciones
    verificadas en §19), plan 99 `N/A|VALID` según su ciclo, legacy 01–95
    `EXCLUDED`, `ANOMALY=0`.

No se agregan tests que requieran inventar estructuras normativas inexistentes.

## 19. Plan de dogfooding (ejecución futura)

**[PROPOSED — Future Implementation]** Tras la corrección, C-2 se ejecuta
sobre el repo real. Invariantes esperadas (a verificar en la ejecución y
registrar con su salida; **no se inventan resultados**):

- Planes 96/97/98: **sin regresiones** — permanecen sin ANOMALY y sin GAP
  introducido por la corrección; clasificación esperada `VALID` (por Tier 2
  declarada cuando el tree final no está embebido) verificable en la salida;
- Plan 99 (este artifact): `N/A` mientras esté `Aprobado para ejecución` con
  secciones de anchor/checkpoint vacías; `VALID` tras su propio cierre;
- legacy 01–95: `EXCLUDED`; GAP=0 y ANOMALY=0 en el corpus del régimen;
- ningún cambio en los artifacts históricos (diff de ejecución limitado a §9.2).

Si la salida real contradice una invariante, la ejecución **STOP** antes del
commit, registra la evidencia y escala (Gate 4/§25; §28 OQ-4).

## 20. Plan de validación (ejecución futura)

**[PROPOSED — Future Implementation]**

### 20.1 Baseline (Gate 0)

Registrar antes de implementar: branch (`dev`), HEAD, working tree, baseline
pytest y baseline de la batería canónica (§3).

### 20.2 Implementación

Corregir únicamente C-2 y los tests relacionados (§9.2); ningún otro archivo de
código.

### 20.3 Validación

Ejecutar y registrar:

- suite C-2 existente (21 escenarios) + regresiones F-1 (§18);
- suite C-1 existente (regresión: C-1 no se modifica pero su suite debe
  permanecer verde);
- batería canónica del repo (`docs/VERSIONING.md:4.1 Batería canónica de verificación`);
- dogfooding sobre el corpus real (§19);
- `git diff --check`.

Los resultados se registran durante la ejecución (anchor/checkpoint del propio
plan), no se anticipan en este artifact.

## 21. Plan de anchor (propio)

**[PROPOSED — Future Implementation]** Al ejecutar, este Plan registra su
**propio** Validation Anchor en la sección final `## Validation anchor`
(VC-1; formato v1 de planes 96–98), con su estado validado y Scoped Content
Identity; **no reutiliza** el anchor de Plan 98. Cadena esperada:

```text
Plan 99 → implementation state → validation → nuevo anchor → nuevo checkpoint
→ Closed
```

Anti-circularidad de la propia validación: la validación sobre el contenido de
implementación corre antes de agregar los registros de cierre de este artifact
(precedente planes 96–98), y la revalidación V2 sobre el estado final precede a
`Closed`. La sección no se fabrica en esta iteración.

## 22. Plan de checkpoint (propio)

**[PROPOSED — Future Implementation]** Al cerrar, este Plan registra su
**propio** checkpoint en la sección final `## Checkpoint / cierre` (GC-1;
formato v1), con commits de cierre, estado validado, estado de cierre,
consistencia, governance y condición derivada. El cierre es **docs-only sin
release** (sin `VERSION` bump, sin tag; RFC-69) salvo evidencia contraria
verificada que la ejecución deba escalar antes de continuar. La sección no se
fabrica en esta iteración.

## 23. Trazabilidad C-n (futura, no se crea ahora)

**[DERIVED]** La autorización de la corrección es **este Plan aprobado**; la
evidencia (F-1) y el futuro registro `C-n` no son autorización (decisión D7;
`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`).

Al ejecutar y cerrar, se registra en este artifact (sección final
`## Correcciones`) un registro **FACTUAL/TRACEABILITY** con ref calificada
`<PLAN-99>:C-1`, que documenta:

- qué se corrigió (selección del anchor aplicable en C-2/GC-1);
- relación con F-1 (`<PLAN-99>:F-1`) y con Plan 98 (origen histórico, CLOSED);
- evidencia (salidas de tests/checkers/dogfooding);
- commits de la corrección (§24);
- nueva validación (anchor/checkpoint propios; §21/§22);
- lineage y alcance de revalidación (CL-6/CL-7).

No se crea `C-n` durante esta iteración ni durante la implementación; el
registro se agrega al cerrar con la evidencia real.

## 24. Estrategia de commits (futura; no se ejecuta ahora)

**[PROPOSED — Future Implementation]** Siguiendo los precedentes de la serie
(planes 96–98, commits separados contenido/registro):

- **C1 — corrección de contenido**: `tools/check_lifecycle_checkpoint.py` +
  `tests/test_check_lifecycle_checkpoint.py` (incluidas regresiones F-1).
  Antes de C1: suite C-2/C-1 y regresiones verdes; `git diff --check` limpio.
- **C2 — registros de cierre** (cuando aplique): secciones finales de este
  artifact (anchor/checkpoint/`C-1`), espejo en `docs/plans/INDEX.md` e ítem
  `(plan 99, RFC-75)` en `CHANGELOG.md:[Unreleased]` si las convenciones lo
  exigen. Antes de C2: revalidación V2 sobre el estado final
  (anti-circularidad; §21/§22).

Commits atómicos, Conventional Commits en inglés, en `dev`, con la referencia
`(plan 99, RFC-75)`; sin push en esta iteración ni sin autorización explícita.

## 25. Recovery / Stop Conditions (ejecución futura)

**[PROPOSED]** La ejecución futura debe **detenerse**, registrar evidencia y
escalar al mantenedor (AU-3) si ocurre cualquiera de estos casos:

- tests fallan (suite C-2/C-1, regresiones F-1 o pytest global) sin desviación
  aceptada;
- dogfooding falla (corpus real con ANOMALY/GAP inesperado sobre 96/97/98/99;
  §19);
- la batería canónica falla (Gate 3);
- el checkpoint/consistencia propio falla (Gate 6);
- el working tree está inesperadamente sucio (cambios ajenos al plan);
- el scope se excede (archivos fuera de §9.2);
- aparece una necesidad normativa (p. ej. nueva decisión sobre
  anti-circularidad o sobre el modelo de evidencia declarada);
- aparece una dependencia con Protocol (`protocol/.agents/`);
- aparece un cambio de clasificación del corpus no explicable por §14.

En todos esos casos:

> **STOP → registrar evidencia → escalar según autoridad.**

No se permite scope creep automático; no se resuelve por código una decisión
normativa (ADR-16 AU-3).

## 26. Criterios de aceptación

Checklist de aceptación del artifact físico (esta iteración) y del alcance que
define:

- [ ] **AC-1** — GC-1 determina el anchor por correspondencia:
      `validated state == closure state` (R-99-4/R-99-5).
- [ ] **AC-2** — La selección no depende de `latest A2` ni de posición de
      lista/textual (R-99-4; tests 1–3 de §18.2).
- [ ] **AC-3** — A1 acompañado posteriormente por A2 no provoca falsa anomalía
      cuando el cierre corresponde a A1 (Caso A).
- [ ] **AC-4** — El primer A2 no es reemplazado por un segundo A2 cuando el
      cierre corresponde al primero (Caso B).
- [ ] **AC-5** — No existe falsa validación cuando el closure state no
      corresponde a ninguna validación aplicable (Caso C; R-99-6).
- [ ] **AC-6** — Tree identity continúa siendo la identidad material.
- [ ] **AC-7** — Commit SHA continúa siendo locator.
- [ ] **AC-8** — No existe requisito de reachability.
- [ ] **AC-9** — A1 permanece inmutable.
- [ ] **AC-10** — A2 conserva lineage hacia A1.
- [ ] **AC-11** — Los escenarios adversariales que demostraron F-1 quedan
      convertidos en tests permanentes (§17/§18).
- [ ] **AC-12** — La batería existente permanece verde (Gate 3).
- [ ] **AC-13** — El dogfooding del corpus existente permanece consistente
      (sin ANOMALY/GAP regresivo; §19).
- [ ] **AC-14** — No se modifican RFC-75, ADR-15 ni ADR-16.
- [ ] **AC-15** — No se modifica Plan 98.
- [ ] **AC-16** — El cambio no introduce dependencia con Protocol
      (`protocol/.agents/` intacto).

## 27. Riesgos

**[DERIVED]**

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Selección por recencia persiste tras la corrección | Alto | R-99-4; regresiones Caso A/B (§17) |
| Falsa validación multi-commit no detectada | Alto | Caso C multi-commit; test 4 de §18.2 |
| Dogfooding regresivo sobre planes 96/97/98 | Alto | Tier 2 corpus (§14/R-99-5); invariantes §19; STOP si difiere |
| Anti-circularidad (validated state derivado del cierre) | Alto | R-99-3; verificación de diseño y tests |
| Scope leakage (F-2…F-9, C-1, C-n, CI, registries) | Alto | §9/§10; Gates 1 y 5 |
| SHA/reachability reintroducidos como identidad | Medio | §16; tests existentes 4/17 |
| Ambigüedad de parseo del corpus (texto de declaraciones) | Medio | Reglas §14 explícitas; caso límite → STOP/escalar (§25; §28 OQ-3) |
| ACL del sandbox en pytest | Bajo (ambiental) | Permisos reales; reporte honesto (plan 94 §24.1) |

## 28. Pending / Open Questions

**[DERIVED]** Pendings **no-bloqueantes** para esta iteración de creación
(PC-1; owner mantenedor; escalación humana AU-3); registro completo en la
sección final:

- **OQ-1** — autorización humana de ejecución y commits futuros; gate humano;
  blocking: no (no bloquea esta iteración de creación).
- **OQ-2** — aceptación humana de la batería al cierre ("batería verde" del
  plan 94); blocking: no.
- **OQ-3** — ambigüedades de parseo del corpus si aparecen al implementar
  (texto exacto de declaraciones de revalidación, variantes de encabezado);
  resolución con las reglas de §14; si no resoluble → STOP + escalación;
  blocking: no.
- **OQ-4** — confirmación humana si el dogfooding real difiere de las
  invariantes de §19 antes de commit; blocking: no.
- **OQ-5** — registro del `C-1` de este Plan al cerrar (contenido y evidencia
  exactos); se completa en la ejecución; blocking: no.

## 29. Execution Gates

**[PROPOSED — Future Implementation]** La ejecución futura no omite ningún
gate:

| Gate | Contenido | Criterio |
|---|---|---|
| Gate 0 | Baseline | Estado del repo capturado (branch/HEAD/árbol/batería/pytest; §20.1) |
| Gate 1 | Implementación | Solo C-2 + tests relacionados (§9.2) |
| Gate 2 | Tests unitarios/regresión | Suite C-2 existente + regresiones F-1 en verde (§18) |
| Gate 3 | Validación canónica | Checkers canónicos de §20.3 en verde (o desviación aceptada) |
| Gate 4 | Dogfooding | Corpus real consistente (§19) |
| Gate 5 | Anchor | Nuevo Validation Anchor registrado (§21) |
| Gate 6 | Checkpoint | GC-1 valida el cierre contra el anchor correcto (§22) |
| Gate 7 | Cierre | Solo después de toda la evidencia en verde (§30) |

## 30. Condiciones de cierre

**[PROPOSED]** Condición derivada `Closed` de este Plan =
`Executed` + governance aplicable + checkpoint propio + consistencia
checkpoint↔anchor propio (GC-1) + evidencia de validación PASS para el estado
de cierre (§21/§22). Cierre **docs-only sin release** (sin `VERSION` bump, sin
tag; `docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle`;
`docs/VERSIONING.md:3. Versionado`). No se reutiliza el anchor de Plan 98 como
anchor de este Plan; Plan 98 es únicamente el origen histórico del finding
(§6/§21).

## 31. Referencias

**[DERIVED]** Lista de referencias utilizadas:

- `docs/rfc/75-change-lifecycle.md` (Mecanismos 2, 5, 6, 7, 8, 12, 14, 15;
  Modelo de lifecycle; No-objetivos; Rollout incremental);
- `docs/adr/15-change-lifecycle-continuity.md`; `docs/adr/16-change-lifecycle-authority.md`;
- `docs/CONVENTIONS.md` (Convenciones; Change Lifecycle DEV — alcance y
  frontera; Change Levels; Intake; VC-1/GC-1/LC-1/PC-1; Serie);
- `docs/VERSIONING.md` (§3, §4.1, §7, §10);
- `docs/plans/94-change-lifecycle-master-action-plan.md`;
- `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md`;
- `docs/plans/97-change-lifecycle-unit-c-increment-2.md`;
- `docs/plans/98-change-lifecycle-unit-d-increment-4.md`;
- `tools/check_lifecycle_checkpoint.py`; `tests/test_check_lifecycle_checkpoint.py`;
- C1/C2 Read-Only Audit Report (2026-09-02; insumo de sesión, no versionado).

## 32. Veredicto final

**[DERIVED]** Sin BLOCKER ni contradicción con las decisiones D1–D7 del encargo
detectados durante la inspección: F-1 es un defecto de materialización
(D3); Plan 98 permanece CLOSED sin modificaciones (D1/D2); el nuevo Plan es la
autoridad normativa de la corrección (D4); el alcance es F-1 únicamente (D5);
sin RFC/ADR nuevos (D6); el `C-n` futuro no se crea y no es autorización (D7);
el diseño de §14/§15/§16 preserva anti-circularidad, GAP vs ANOMALY, A1/A2,
tree identity y no-reachability conforme a la normativa existente. Estado de
este artifact al cierre de la iteración de creación:

```text
Plan 99 = Aprobado para ejecución (PLANNED / OPEN)
Implementation = NOT STARTED
Executed = NO
Committed = NO (sin commit en esta iteración)
Closed = NO
Released = NO
```

**PLAN 99 READY FOR IMPLEMENTATION — GO WITH CONDITIONS** (condiciones C1–C4,
§1/§28). Próximo paso: revisión humana del Plan y, solo tras su aprobación
explícita, ejecución de la corrección sobre `dev` (§29); esta tarea no
implementa F-1 ni cierra el Plan.

---

## Validation anchor

Registrado al ejecutar la corrección F-1 (2026-09-02). La validación **V1**
corrió sobre el contenido de implementación de la corrección (commit de
contenido C1 `42da250`) **antes** de agregar los registros de cierre de esta
sección (anti-circularidad, §21/§26 del encargo de ejecución; precedente
planes 96–98).

- Declared scope: corrección de la selección del anchor aplicable de GC-1 en
  C-2 (`tools/check_lifecycle_checkpoint.py`) + suite C-2 existente y
  regresiones F-1 nuevas (`tests/test_check_lifecycle_checkpoint.py`) + batería
  canónica del repo + dogfooding C-1/C-2 sobre el corpus real.
- Validation command-set:
  - `python -m pytest tests/test_check_lifecycle_checkpoint.py`
  - `python -m pytest tests/`
  - `python tools/check_lifecycle_checkpoint.py`
  - `python tools/check_lifecycle_anchor.py`
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `git diff --check`
- Effective inputs (repo content): contenido completo del repo en el estado
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/` y
  la raíz; pytest consume `tests/` + `tools/`); representado por el State
  identity (tree id). El working tree validado incluía además los registros de
  creación del Plan 99 (`docs/plans/INDEX.md` modificado + este artifact sin
  trackear, pendientes de C2), ajenos al contenido de C-1 inspeccionado por la
  suite.
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en
  esta corrección); el consumo por comando se observa de la documentación de
  cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 10.3.0; pytest ejecutado fuera
  del sandbox por ACL del basetemp `pytest-of-rolda` (ruido ambiental
  documentado en planes 96–98); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `e9b47b1c2297cb61c9e931fbe12171f01234d0c9` (tree id; igual a
    `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 2 archivos del cambio de C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `dfb76a4d699e95547366131a7ced35c1776169f70e30e0e334fa0abdb879137a`.
    Pares path → blob (C1): `tests/test_check_lifecycle_checkpoint.py` →
    `1e1172970a859af257d297f40592e880a0fc20f0`; `tools/check_lifecycle_checkpoint.py`
    → `104fe5604de1fafb76a672a81edc9876f1dbb2f9`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería completa +
  dogfooding C-1/C-2 sobre el estado final de la corrección, incluidos los
  registros de cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7; §22/§24 de
este plan). Se registra en el commit de registro C2, posterior al commit de
contenido C1.

- Commits de cierre:
  - C1 `42da25010ad0505e63a9566aba71f061f16da2bb` —
    `fix(tools): select C-2 checkpoint anchor by closure-state correspondence
    (plan 99, RFC-75)` (contenido de la corrección validado por V1).
  - C2 — este commit de registro
    (`docs(plans): record plan 99 validation anchor and checkpoint (plan 99,
    RFC-75)`); su SHA se identifica por el mensaje y el árbol no embebe su
    propia identidad (auto-referencia; §22).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `e9b47b1c2297cb61c9e931fbe12171f01234d0c9`; Delta scoped identity =
  `dfb76a4d699e95547366131a7ced35c1776169f70e30e0e334fa0abdb879137a`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit).
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`e9b47b1c…`) → **PASS**.
  - Estado final (C2): difiere de C1 en los registros de cierre (anchor/
    checkpoint de este plan, INDEX y changelog); **revalidación V2** (batería
    canónica completa + dogfooding C-1/C-2 sobre el contenido final de la
    corrección, ejecutada antes del commit) → PASS. GC-1 queda satisfecho por
    revalidación antes de `Closed` (la consistencia del estado de cierre se
    evalúa contra A2; correspondencia por estado, nunca por recencia).
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 99, RFC-75)` en `CHANGELOG.md:[Unreleased]`; corrección registrada
  como `<PLAN-99>:C-1` (sección final); docs-only, sin `VERSION` bump ni tag.
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (C1 + C2 en `dev`), `Closed` (condición derivada con checkpoint
  y consistencia), `Released` (no aplica: sin promoción ni tag).

## Findings / Correcciones / Pending

Registros reales de esta iteración de creación (artefactos nuevos bajo las
reglas del Incremento 2; la ausencia de registros no es invalidez):

### Findings

- `<PLAN-99>:F-1` — estado: `resolved` (2026-09-02; resuelto por la corrección
  `<PLAN-99>:C-1` con evidencia V1/V2 y checkpoint de este artifact); estado
  previo: `open` (registrado en la creación del Plan, 2026-09-02); observación:
  C-2 (`tools/check_lifecycle_checkpoint.py`) seleccionaba el anchor aplicable
  de GC-1 por recencia (`latest A2 wins`) y comparaba por pertenencia genérica
  del tree entre los commits de cierre, en lugar de identificar el estado de
  cierre y seleccionar el anchor de la validación cuyo estado validado
  corresponde a ese estado; severidad: MAJOR; clasificación:
  implementation/materialization defect; tipo: post-close finding; origin:
  Plan 98 (CLOSED, docs-only); source: C1/C2 Read-Only Audit Report (read-only
  posterior a Plan 98); evidencia original: comportamiento descrito en §12 y
  Casos A/B/C en §17 (sobre la implementación en HEAD `aa68704`); estado Git
  observado: `dev` @ `aa68704`, working tree limpio; provenance original:
  audit de sesión (no versionado) + este artifact; resolución: selección del
  anchor por correspondencia de estado implementada y verificada (reglas
  R-99-1…R-99-10; regresiones F-1 permanentes; dogfooding del corpus real sin
  regresión; commit C1 `42da250`).

### Correcciones

- `<PLAN-99>:C-1` — refs origen: `<PLAN-99>:F-1`; origen histórico: Plan 98
  (CLOSED); autorización: Plan 99 aprobado para ejecución (este registro es
  FACTUAL/TRACEABILITY, no fuente normativa); qué se corrigió: materialización
  de GC-1 en C-2 (`tools/check_lifecycle_checkpoint.py`) — selección del
  anchor aplicable por correspondencia `validated state == closure state`
  (estado de cierre = tree del commit final o literal declarado; Tier 1 por
  tree identity en orden de registro; Tier 2 por revalidación declarada única
  sobre el cierre, patrón corpus 96–98; GAP/ANOMALY y no-reachability
  preservados; reporte del anchor aplicable); eliminación de la selección por
  recencia y de la pertenencia genérica del tree; alcance de revalidación
  (CL-6): suite C-2 (29 tests: 21 existentes + 8 regresiones F-1), suite C-1,
  batería canónica y dogfooding del corpus real, sobre C1 (V1) y sobre el
  estado final (V2); evidencia (Git/commit/estado): commit C1 `42da250`
  (2 archivos; tree `e9b47b1c…`; delta `dfb76a4d…`), pytest `388 passed,
  0 failed`, checkers canónicos PASS, dogfooding C-2 `VALID` planes 96/97/98 y
  `ANOMALY=0`, adversarial review PASS (los 3 casos del bug original fallan
  sobre la implementación anterior y pasan sobre la corregida); resultado:
  `<PLAN-99>:F-1` `resolved`; cierre docs-only de Plan 99 (sin release).

### Pending decisions

Pendings **no-bloqueantes** (PC-1), owner: mantenedor, escalación: humana
(AU-3); registro completo y detalle en §28:

- `<PLAN-99>` — decisión: OQ-1 autorización de ejecución y commits; blocking:
  no; owner: mantenedor; escalación: humana; resolución: autorización explícita
  otorgada por el mantenedor (Execution Prompt 2026-09-02); ejecución y commits
  C1/C2 realizados en `dev`; resuelto.
- `<PLAN-99>` — decisión: OQ-2 aceptación de la batería al cierre; blocking:
  no; owner: mantenedor; escalación: humana; resolución: batería aceptada al
  cierre (pytest `388 passed, 0 failed`; checkers canónicos PASS; dogfooding
  `ANOMALY=0`); resuelto.
- `<PLAN-99>` — decisión: OQ-3 ambigüedades de parseo del corpus; blocking: no;
  owner: ejecutor/mantenedor; escalación: humana; resolución: sin ambigüedad
  residual — reglas R-99-x implementadas y cubiertas por tests; no se
  requirió STOP; resuelto.
- `<PLAN-99>` — decisión: OQ-4 dogfooding real fuera de invariantes; blocking:
  no; owner: mantenedor; escalación: humana; resolución: dogfooding real
  cumplió las invariantes de §19 (96/97/98 `VALID`, plan 99 `VALID` tras su
  cierre, legacy `EXCLUDED`, GAP=0, ANOMALY=0); no se requirió STOP; resuelto.
- `<PLAN-99>` — decisión: OQ-5 contenido exacto del registro `C-1`; blocking:
  no; owner: ejecutor; escalación: humana; resolución: registro
  `<PLAN-99>:C-1` completado en esta sección con la evidencia real de la
  ejecución; resuelto.

## Trazabilidad

Origen → C1/C2 Read-Only Audit Report (post-close de Plan 98) → F-1 → este
Plan 99 (corrección post-close, serie Change Lifecycle DEV / RFC-75) →
ejecución futura (C-2 + regresiones F-1) → dogfooding → validación anclada →
checkpoint → cierre docs-only → registro `<PLAN-99>:C-1`. Este plan no autoriza
cambios de payload (RFC-56); la autorización de la ejecución es humana (OQ-1).

## Nota de ejecución

- 2026-09-02 — **Creación/registro (planificación).** Plan 99 creado y
  registrado en `docs/plans/INDEX.md` (Trigésima primera serie; Status inicial
  `Aprobado para ejecución`, PLANNED / OPEN) a partir del C1/C2 Read-Only
  Audit Report (F-1) y del estado factual del repo (HEAD `aa68704`, working
  tree limpio), **sin implementar F-1** y sin commits. Verificación de la
  iteración: checkers documentales canónicos pertinentes en verde
  (`check_protocol_invariants.py`, `check_plan_citations.py`,
  `check_plan_structure.py`, `check_taxonomy_coherence.py`,
  `check_session_artifacts.py`, `check_version_state.py`); `check_dist_sync.py`
  no se reinterpreta en `dev` (semántica local/release); pytest no se re-corrió
  en esta iteración (cambio exclusivamente documental; baseline reportado
  `380 passed, 0 failed`). Sin cambios en `protocol/`, `runtime/`, `tests/`,
  `tools/`, VERSION, CHANGELOG, ADRs, RFCs, `docs/CONVENTIONS.md`,
  `docs/VERSIONING.md` ni planes 94–98; sin creación de `.agents/` en la raíz;
  sin push. **STOP:** la implementación de F-1 queda pendiente de revisión
  humana del Plan y de su aprobación explícita.
- 2026-09-02 — **Ejecución de la corrección sobre `dev`.** Estado previo: HEAD
  `aa68704`, working tree con los cambios de creación del plan (INDEX + este
  artifact, sin commit), pytest `380 passed, 0 failed`, checkers canónicos
  PASS. **C1 (contenido):** `tools/check_lifecycle_checkpoint.py` corregido
  (reglas R-99-1…R-99-10 — estado de cierre = tree del commit final o literal
  declarado; Tier 1 correspondencia por tree identity; Tier 2 revalidación
  declarada única sobre el cierre, patrón corpus 96–98; sin recencia, sin
  pertenencia genérica del tree; GAP/ANOMALY y no-reachability preservados;
  reporte del anchor aplicable) + `tests/test_check_lifecycle_checkpoint.py`
  (21 tests existentes conservados con sus clasificaciones; actualización de
  una aserción de razón; 8 regresiones F-1 nuevas: Casos A/B/C, literal de
  cierre vs commit final, Tier 2 corpus, ambigüedad → GAP, FAIL+Closed →
  ANOMALY; real-repo test con Plan 99). **Commit C1:** `42da250` (2 archivos;
  tree `e9b47b1c`). **Gates:** pytest `388 passed, 0 failed` (GATE 2); C-1
  suite verde sin cambios (GATE 1/2); checkers canónicos PASS (GATE 3);
  dogfooding C-1/C-2 sobre el corpus real: 96/97/98 `VALID` (anchor aplicable
  A2 declarado), plan 99 `N/A` pre-cierre, legacy 01–95 `EXCLUDED`, GAP=0,
  ANOMALY=0 (GATE 4); `git diff --check` limpio. **Adversarial review
  (GATE):** los 3 casos del bug original fallan sobre la implementación
  anterior (HEAD `aa68704`, scratch copy): Caso A → ANOMALY falsa (hoy VALID
  con A1), Caso B → ANOMALY falsa (hoy VALID con A2), Caso C → VALID falsa
  (hoy ANOMALY). **C2 (registros de cierre):** Status `Executed`; Validation
  Anchor V1 (T1 `e9b47b1c…`; delta `dfb76a4d…`) y Checkpoint con revalidación
  V2 (batería completa + dogfooding sobre el estado final staged) antes de
  `Closed` en este artifact; espejo en `docs/plans/INDEX.md`; ítem
  `(plan 99, RFC-75)` en `CHANGELOG.md:[Unreleased]`; `<PLAN-99>:C-1`
  registrado; condición derivada `Closed` (docs-only, sin release). Scope
  audit: sin cambios en `protocol/`, `runtime/`, C-1, ADRs/RFCs,
  `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, VERSION, Plan 98 ni planes
  94–98; sin push.
