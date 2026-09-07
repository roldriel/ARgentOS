# Plan 98 — Implementación de la Unidad D (Incremento 4): automatización segura mínima del Change Lifecycle DEV (C-1 lifecycle anchor checker y C-2 lifecycle checkpoint checker)

> **Naturaleza de este documento.** Este es el **cuarto Implementation Plan
> ejecutable** derivado del Master Action Plan 94 (plan 94). Implementa la
> **Unidad D = Incremento conceptual 4** de RFC-75 con el alcance mínimo
> viable demostrado por el corpus actual: **C-1 — lifecycle anchor
> validation** y **C-2 — lifecycle checkpoint validation**, como mecanismos
> deterministas, factuales y advisory, DEV-only (`tools/` + `tests/`). No
> automatiza findings/corrections (`F-n`/`C-n`), pending, stale detection,
> series ni métricas; no incorpora CI; no modifica `protocol/.agents/` ni
> crea `.agents/` en la raíz; no produce `VERSION` bump ni tag; no introduce
> autoridad normativa en checkers (ADR-16). No rediseña RFC-75 ni Plan 94:
> deriva, no reinterpreta
> (`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`).
> El cambio es **DEV-only** (checkers y tests del repo fuente), sin efecto
> sobre el payload del Protocol (`docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera`).
>
> **La presente iteración es solo de creación/registro del plan**: crea este
> archivo y su registro en `docs/plans/INDEX.md`; **no ejecuta el plan**, no
> crea `tools/check_lifecycle_anchor.py`, no crea
> `tools/check_lifecycle_checkpoint.py`, no crea tests, no modifica código,
> `runtime/`, `tests/`, `tools/`, `protocol/` ni fuentes normativas. Estado
> esperado al cierre de esta iteración:
>
> ```text
> Plan 98 = Aprobado para ejecución (PLANNED / OPEN)
> Implementation = NOT STARTED
> Executed = NO
> Committed = NO (sin commit en esta iteración; registro en el working tree)
> Closed = NO (condición derivada)
> Released = NO
> ```

**Status:** Executed
**Fecha:** 2026-09-02
**RFC:** RFC-75 (`docs/rfc/75-change-lifecycle.md`)
**Clase:** — (no toca `protocol/.agents/`; cambio DEV-only del repo fuente con
tooling y tests propios; sin `VERSION` bump ni tag; RFC-56 no aplica)
**Change Level:** L2 (clasificación prospectiva de dogfooding, declarada al
crear el plan; ver §19)
**Depende de:** RFC-75 `Accepted` (`docs/rfc/75-change-lifecycle.md`); ADR-15
`Accepted` (`docs/adr/15-change-lifecycle-continuity.md`); ADR-16 `Accepted`
(`docs/adr/16-change-lifecycle-authority.md`); RFC-46 `Accepted`; RFC-56
`Accepted`; RFC-69 `Accepted`; Plan 94 `Executed` (2026-09-02, `3acf439`);
Plan 95 `Executed` (2026-09-02, `bc21978` + `865e3ad` + `dc7425f`); Plan 96
`Executed` + condición derivada `Closed` (docs-only; C1 `9e4192f` + C2
`9844cf5`); Plan 97 `Executed` + condición derivada `Closed` (docs-only; C1
`236735b` + C2 `4513077`); Decisión B (`fc52c88`, semántica A1/A2/closure
PASS); **Planning Report de Plan 98** (auditado con veredicto GO WITH
CONDITIONS; artefacto de sesión no versionado en el repo — insumo, no fuente
normativa; ver §2); batería canónica según la política de "batería verde" del
plan 94 (`docs/plans/94-change-lifecycle-master-action-plan.md:24.1 Política de interpretación de "batería verde"`).
**Origen:** Solicitud explícita del mantenedor (2026-09-02): crear físicamente
el Plan 98 (Unidad D / Incremento 4) a partir del Planning Report ya auditado
**sin implementar** la Unidad D, sin cerrar el Plan y sin adelantar cambios
fuera del registro documental.

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
| `BLOCKER` | Contradicción que impide ejecutar la Unidad D (no se detectó ninguna; ver §28). |
| `UNKNOWN` | No verificable en el estado actual; se indica cómo resolverlo. |

Las afirmaciones sobre el estado actual del repo se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`). El Planning Report no se cita como
`ruta:sección` porque no es un artifact versionado del repo: es el diseño de
trabajo auditado (provenance de sesión) y este plan lo incorpora como insumo,
no como fuente normativa (ver §2).

## Contenido requerido → sección

| Requisito del encargo | Sección de este documento |
|---|---|
| Header / metadata e identidad | Header de este archivo |
| Naturaleza / esta iteración no implementa | Banner de apertura |
| Resumen ejecutivo y propósito del Incremento 4 | §1 |
| Autoridad e insumos | §2 |
| Estado actual del repositorio | §3 |
| Declaración del problema | §4 |
| Alcance exacto C-1 + C-2 | §5 |
| Fuera de alcance (out of scope) | §6 |
| Alcance conceptual del Incremento 4 | §7 |
| Población del Change Lifecycle regime | §8 |
| Legacy y no retroactividad | §9 |
| C-1 — especificación de implementación futura | §10 |
| C-2 — especificación de implementación futura | §11 |
| Modelo A1/A2 | §12 |
| Checkpoint semantics (GC-1) | §13 |
| Autoridad | §14 |
| CI e integración | §15 |
| Estrategia de testing futura | §16 |
| Dogfooding | §17 |
| Commits futuros C1/C2 | §18 |
| Change Level | §19 |
| Métricas | §20 |
| SCI / Context Identity | §21 |
| Pending y Open Questions | §22 |
| Acceptance Criteria | §23 |
| Recovery / Stop Conditions | §24 |
| Riesgos | §25 |
| Criterios de salida y verificación | §26 |
| Matriz de trazabilidad | §27 |
| Auditoría adversarial interna | §28 |
| Veredicto / readiness | §29 |
| Validation anchor / Checkpoint / Nota de ejecución | Secciones finales (se completan al ejecutar, no en esta iteración) |

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
(`docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:30. Grafo de dependencias`).
Este plan no altera esa numeración y no planifica el Incremento 5.

La Unidad D materializa el **Incremento 4 conceptual de RFC-75 — safe
automation** (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`),
gated en observabilidad: la regla persist → observe → automate exige datos de
lifecycle reales producidos por las unidades A–C antes de automatizar un check.
Ese gate está satisfecho para el MVP de este plan: el corpus actual contiene
**dos registros reales completos** de Validation Anchor y Checkpoint (planes 96
y 97), campos v1 definidos en `docs/CONVENTIONS.md` y formato consumible en el
template de Plan (`docs/plans/_TEMPLATE.md`), producidos por los Incrementos
1+3 y 2 (`docs/VERSIONING.md:11. Métricas del Change Lifecycle (observability schema baseline)`).

**[DERIVED + PROPOSED]** Plan 98 introduce la **primera automatización
operativa** del Change Lifecycle DEV mediante mecanismos deterministas
(checkers), comenzando deliberadamente con el mínimo viable demostrado por el
corpus actual:

- **C-1 — lifecycle anchor validation** (`tools/check_lifecycle_anchor.py` +
  `tests/test_check_lifecycle_anchor.py` propuestos): verifica forma y
  consistencia de los Validation Anchors registrados en artifacts del régimen
  nuevo, distinguiendo `GAP` (información requerida ausente o no verificable;
  advisory) de anomalía/contradicción (información presente pero incompatible).
- **C-2 — lifecycle checkpoint validation**
  (`tools/check_lifecycle_checkpoint.py` +
  `tests/test_check_lifecycle_checkpoint.py` propuestos): verifica la relación
  closure↔estado Git (checkpoint) contra el anchor de la validación cuyo
  estado validado es el estado de cierre (GC-1), con **tree identity** como
  identidad material y commit SHA solo como locator.

No debe presentarse el Incremento 4 como una automatización completa del Change
Lifecycle: automatiza únicamente C-1 + C-2; todo lo demás (F-n/C-n/pending/
stale/series/métricas/enforcement) queda fuera de scope (§6) por diseño y por
evidencia insuficiente o inexistente.

**Veredicto de este artifact:** **PLAN 98 READY FOR IMPLEMENTATION — GO WITH
CONDITIONS** (§29). Condiciones reales (ninguna de diseño, ninguna inventada;
ninguna bloquea esta iteración de creación):

- **C1** — autorización humana para ejecutar la Unidad D y para los commits
  C1/C2 en `dev` (§22 OQ-6).
- **C2** — aceptación humana de la batería al cierre según la política de
  "batería verde" del plan 94 (§26; §22 OQ-6).
- **C3** — si al implementar aparece una ambigüedad de población/identidad no
  resoluble con las fuentes normativas actuales, **STOP** y escalación humana
  (AU-3); no se inventa regla (§24).
- **C4** — sin elevación de ADR candidates en esta Unidad (§22 OQ-4/OQ-5) y sin
  registrar la Decisión B en el Amendment Log de RFC-75 salvo decisión humana
  (§22 OQ-3).

Este artifact se crea y registra en esta iteración; el estado de ejecución es
`NOT STARTED` (ver banner de apertura).

## 2. Autoridad e insumos

**[DERIVED]** Orden de precedencia aplicado (repo factual > normativa
`Accepted` > planes ejecutados > convenciones > diseño de trabajo > inferencia
del agente):

1. **Estado factual actual del repositorio** (§3): git, checkers, artifacts.
2. **RFC-75** `Accepted`: Mecanismo 6 (Validation Anchors: declared scope /
   command-set / effective inputs / observed dependencies / environmental
   factors / Scoped Content Identity / validity relativa), Mecanismo 7 (Git
   Checkpoints: checkpoint = relación, no artifact; consistencia con el anchor;
   SHA = locator), Mecanismo 13 (observabilidad), Mecanismo 14 (safe automation
   y regla checker output = evidencia factual ≠ autoridad normativa; GAP),
   Mecanismo 15 (legacy/migración), invariantes VC-1/GC-1 y rollout incremental.
3. **ADR-15**: CL-1 (anchorability), CL-2 (validez relativa al anchor),
   CL-3 (cierre Git-verificable), CL-4 (`Executed` no implica commit), CL-5
   (`Committed` es estado del repo), CL-6/CL-7 (lineage de correcciones),
   CL-8 (registros no eliminados), CL-9 (decision lineage), CL-10 (escala por
   impacto).
4. **ADR-16**: AU-1..AU-7; clases FACTUAL/NORMATIVE/DECISION/RELEASE/
   DESCRIPTIVE; checker = evidencia factual; INDEX descriptivo.
5. **RFC-46**: no retroactividad y trazas históricas no reescribibles.
6. **RFC-56**: clases A/B/C y vía de autorización de payload; no aplica a este
   plan (no toca `protocol/.agents/`).
7. **RFC-69**: taxonomía documental y versionado docs-only.
8. **Plan 94** `Executed`: §14 (estrategia de checkers), §18/Implementation
   Unit D (scope, out of scope, gate de observabilidad, migration legacy,
   validación, dogfooding, exit, rollback, enables), §19 (dogfooding del
   Incremento 4: "los checkers se corren sobre el propio repo; la decisión de
   automatizar usa los datos de lifecycle producidos por las unidades A–C").
9. **Plan 95** `Executed`: observability schema baseline y regla target
   semantics vs operationalización.
10. **Plan 96** `Executed` + `Closed`: formato v1 del Validation Anchor/SCI y
    del checkpoint; asignación de numeración (Plan 98 = Unidad D).
11. **Plan 97** `Executed` + `Closed`: formatos deterministas de refs/pending y
    estructuras documentales que el Incremento 4 consumirá como datos.
12. **Decisión B** (`fc52c88`): A1/A2, validez relativa al anchor, consistencia
    de cierre contra el anchor del estado de cierre.
13. **`docs/CONVENTIONS.md`**, **`docs/VERSIONING.md`**, **`AGENTS.md`** raíz y
    **`docs/AGENTS.md`**: hogar normativo/operativo donde viven los campos que
    los checkers C-1/C-2 consumirán.
14. **Planning Report de Plan 98** (2026-09-02, veredicto GO WITH CONDITIONS):
    diseño de trabajo auditado; **no normativo**; no reemplaza RFC/ADR/planes.
    Este plan incorpora sus decisiones verificadas (alcance C-1+C-2, población
    por señales documentales, GAP/anomalía, A1/A2, tree identity, no
    reachability, no autoridad, commits separados, dogfooding posterior) sin
    rediseñarlas.

Regla de conflicto: si durante la ejecución aparece una contradicción real
entre este plan y una fuente normativa, el ejecutor **no resuelve
unilateralmente**: documenta la contradicción, se detiene si afecta la
ejecutabilidad y marca `HUMAN DECISION REQUIRED` (AU-3;
`docs/adr/16-change-lifecycle-authority.md:Decisión`).

## 3. Estado actual del repositorio (reconstrucción factual)

**[OBSERVED]** Verificado al crear este plan (2026-09-02, read-only sobre el
repo):

| Dato | Valor | Evidencia |
|---|---|---|
| Branch / HEAD | `dev` / `4513077121370dffa6ec68fcf06555e14281b55a` (plan 97: registro de anchor y checkpoint) | `git status`, `git rev-parse HEAD` |
| vs `origin/dev` | ahead 11; `origin/dev` = `fcf6ce1` (G1) | `git status`, `git log` |
| Working tree | limpio antes de esta iteración | `git status` |
| VERSION | `10.3.0` | `protocol/.agents/VERSION` |
| Plan 94 | `Executed` (`3acf439`); sin secciones `## Validation anchor` / `## Checkpoint / cierre` (legacy para C-1/C-2) | INDEX + git log + estructura del archivo |
| Plan 95 | `Executed` (`bc21978` + `865e3ad` + `dc7425f`); sin secciones de anchor/checkpoint (legacy para C-1/C-2) | INDEX + git log + estructura del archivo |
| Plan 96 | `Executed` + `Closed` docs-only (`9e4192f` + `9844cf5`); con Validation Anchor y Checkpoint reales | INDEX + archivo |
| Plan 97 | `Executed` + `Closed` docs-only (`236735b` + `4513077`); con Validation Anchor y Checkpoint reales | INDEX + archivo |
| Plan 98 | no existe antes de esta iteración | `Test-Path`, INDEX, git log |
| RFC-75 / ADR-15 / ADR-16 | `Accepted`, intactos | docs + INDEX |
| RFC-75 Amendment Log | entradas de creación, plan 96 y plan 97; **sin entrada de Decisión B** (OQ-3) | `docs/rfc/75-change-lifecycle.md:Amendment Log` |
| Batería canónica (checkers) | 6 checkers PASS en `4513077` (warnings esperados de `dev`); `check_dist_sync.py` rojo esperado en `dev` (semántica local/release) | corrido (ver §26) |
| pytest | `340 passed, 0 failed` (reportado en el baseline del Planning Report; re-verificación en §26) | reporte baseline |
| Corpus para C-1 | 2 artifacts con `## Validation anchor` poblado (planes 96, 97) + sección en `docs/plans/_TEMPLATE.md`; 0 anchors en Amendment Logs de RFC | `rg` |
| Corpus para C-2 | 2 artifacts con `## Checkpoint / cierre` poblado (planes 96, 97) + sección en `docs/plans/_TEMPLATE.md` | `rg` |
| Registries / entidades lifecycle | ninguno (sin Change entity, sin tracker global, sin DB) | `rg` |
| `.agents/` en raíz | **NO existe** | `Test-Path` |
| `protocol/.agents/` | existe; payload del Protocol, **fuera de scope** | estructura del repo |

**Precondiciones de ejecución (F0):** el estado de §3 debe sostenerse al
ejecutar (branch `dev`; planes 94–97 en su estado registrado; Decisión B
commiteada; árbol limpio salvo los cambios del propio plan); la batería de §26
corre en verde o con desviación documentada aceptada por el mantenedor (§22
OQ-6 / C2).

## 4. Declaración del problema

**[NORMATIVE + DERIVED]** Tras los Incrementos 0, 1+3 y 2 (planes 95/96/97),
los Validation Anchors y los checkpoints se registran **manualmente** en los
artifacts nuevos con un formato v1 documentado (`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`).
No existe verificación mecánica determinista de:

- la presencia y completitud de los campos mínimos del anchor (VC-1) cuando un
  artifact declara una validación registrada;
- la consistencia entre el anchor y el checkpoint al declarar la condición
  derivada `Closed` (GC-1), incluida la semántica A1/A2 de la Decisión B;
- la identidad material comparada (tree identity) y la distinción explícita
  entre commit SHA (locator) e identidad semántica.

RFC-75 Mecanismo 14 lista entre la automatización segura: checks de presencia
de anchor, existencia de ref Git, consistencia de status y detección de stale,
con la regla `checker output = factual evidence ≠ normative authority`
(`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`). El gate de
observabilidad del Incremento 4 se evalúa con datos reales de lifecycle de las
unidades B/C (`docs/VERSIONING.md:11. Métricas del Change Lifecycle (observability schema baseline)`):
el corpus contiene dos pares anchor↔checkpoint reales (planes 96 y 97) más el
formato de template; no hay gate circular con el schema baseline del
Incremento 0.

El problema concreto que resuelve la Unidad D es la brecha entre **registro
documental manual** (estable, formato v1) y **verificación mecánica
determinista** de ese registro: errores humanos de forma (campos faltantes,
duplicados, inconsistentes) y de consistencia closure↔anchor no son hoy
detectables salvo por revisión manual. La automatización mínima C-1 + C-2
cierra esa brecha sin crear autoridad normativa, registries, entidades ni
enforcement total.

## 5. Alcance exacto

### 5.1 Esta iteración de planificación (incluido ahora)

**[PROPOSED — esta iteración]** Creación física del Plan 98 en
`docs/plans/98-change-lifecycle-unit-d-increment-4.md` y su registro en
`docs/plans/INDEX.md` (nueva serie del INDEX; requisito estructural del mirror,
`tools/check_plan_structure.py`). No implementa C-1/C-2, no ejecuta commits y
no modifica ninguna fuente normativa (secciones finales sin anchor/checkpoint
fabricados).

### 5.2 Ejecución futura del plan (incluido entonces; NO se ejecuta ahora)

**[PROPOSED — Future Implementation]** La ejecución autorizada del Plan 98
implementa **exclusivamente**:

- **C-1 — Lifecycle Anchor Checker**:
  - archivo propuesto: `tools/check_lifecycle_anchor.py`;
  - tests propuestos: `tests/test_check_lifecycle_anchor.py`;
  - comportamiento según §10.
- **C-2 — Lifecycle Checkpoint Checker**:
  - archivo propuesto: `tools/check_lifecycle_checkpoint.py`;
  - tests propuestos: `tests/test_check_lifecycle_checkpoint.py`;
  - comportamiento según §11.

Ambos se ejecutan de forma **DEV-only / local invocation** (§15), con tests
deterministas (§16), dogfooding sobre el repo real (§17), commits separados
C1/C2 (§18) y registro de anchor/checkpoint del propio plan al cerrar
(secciones finales).

### 5.3 Excluido incluso en la ejecución futura

Resumen de exclusiones absolutas; detalle completo en §6. En particular, la
ejecución futura **no** agrega los nuevos checkers a la batería canónica de
`docs/VERSIONING.md:4.1 Batería canónica de verificación`, no crea workflows de
CI, no automatiza stale/series/metrics/F-n/C-n, no introduce registries y no
toca `protocol/`, `runtime/`, `.agents/`, `dist/` ni el harness.

## 6. Fuera de alcance (out of scope)

**[NORMATIVE]** El Plan 98 **no** incluye, ni en esta iteración ni en su
ejecución futura:

- Automatización de findings (`F-n`) o corrections (`C-n`); verificación
  mecánica de refs o de metadata de pending.
- Pending decisions automation (ownership/presencia mecánica).
- Stale detection (detección mecánica de validaciones stale).
- Series detection/verificación mecánica de series.
- Lifecycle metrics (medición/agregación de las cuatro métricas permanentes o
  de cualquier métrica derivada).
- Métricas basadas en denominadores; umbrales; coverage/tasa de findings/
  stale rate/correction rate.
- Automatic closure o automatic release.
- Integración CI (`.github/workflows/`), pre-commit hooks o integración
  Makefile.
- Registries globales nuevos; Change entity; Finding entity; Pending/Decision
  entity; Change state machine global; lifecycle database; tracker universal.
- Cambios en `runtime/`, en el harness, en orchestrators/workers del producto o
  en prompts LLM.
- Cambios en el payload del Protocol: `protocol/.agents/`, `protocol/_AGENTS.md`,
  `protocol/.agents/VERSION`, skills del producto.
- Creación de `.agents/` en la raíz del repo fuente.
- Cambios en `dist/` o en la rama `dist`.
- Infraestructura, servicios externos o dependencia de red.
- Backfill automático de artifacts legacy (§9).
- Edición de `docs/adr/*`, de los planes 94/95/96/97, de RFC-46/56/69 o de
  artifacts históricos.
- Modificación de `docs/AGENTS.md` salvo evidencia explícita de necesidad en la
  ejecución (por defecto permanece sin cambios).
- Verificación mecánica de anchors registrados en Amendment Logs de RFCs
  (extensión futura; corpus actual sin ejemplos; §22 OQ-8).

El hecho de que alguno de estos elementos pueda ser útil en el futuro **no
autoriza su inclusión en Plan 98** (RFC-75 Mecanismo 14: solo se automatiza lo
observado como útil y con datos; `docs/plans/94-change-lifecycle-master-action-plan.md:Implementation Unit D — Incremento 4 (conceptual): Automatización segura (gated en observabilidad)`).

## 7. Alcance conceptual del Incremento 4

**[DERIVED]** La Unidad D implementa exactamente el Incremento 4 conceptual de
RFC-75, sin absorber ni renumerar otros incrementos:

| Campo | Contenido (de Plan 94, Implementation Unit D) |
|---|---|
| Increment | 4 |
| Objective | Mecanizar solo lo observado como útil: presencia de anchor, consistencia checkpoint↔anchor, distinción SHA vs tree identity; vistas derivadas opcionales fuera de alcance. |
| Problem solved | Errores humanos de registro; verificación manual costosa; consistencia closure↔anchor no comprobable mecánicamente. |
| Scope | `tools/` (checkers dev nuevos) + `tests/` (suites stdlib con fixtures `tmp_path`); **sin** incorporación a la batería canónica inicial. |
| Out of scope | Autoridad normativa en checkers; umbrales de métricas; backend de telemetría; enforcement total; F-n/C-n/stale/series/metrics. |
| Mechanisms | Checkers opcionales factual/advisory (C-1 y C-2). |
| Dependencies | Unidades A–C (incrementos 0–3); gate de observabilidad satisfecho con datos reales (planes 96/97). |
| Migration | Checkers solo sobre artifacts del régimen nuevo (§8); legacy excluido (§9). |
| Validation | Suites pytest de cada checker + batería canónica existente (según §24.1 del plan 94). |
| Dogfooding | Checkers corriendo sobre el propio repo; planes 96/97/98 como primeros sujetos. |
| Exit criteria | Checkers opcionales implementados con tests; sin cambios normativos de autoridad; batería canónica según §24.1. |
| Rollback | Revertir checkers; nada normativo queda atado a ellos. |
| Enables | Enforcement parcial y observabilidad para decisiones futuras (tracker condicional, handoff). |

Fuente: `docs/plans/94-change-lifecycle-master-action-plan.md:Implementation Unit D — Incremento 4 (conceptual): Automatización segura (gated en observabilidad)`.

**El Incremento 4 no automatiza el Change Lifecycle completo**: C-1 + C-2 son el
mínimo viable demostrado por el corpus actual. Si en la ejecución un
componente adicional resultara realmente obligatorio por una fuente normativa,
**no se introduce silenciosamente**: se marca `HUMAN DECISION REQUIRED`.

## 8. Población del Change Lifecycle regime

**[NORMATIVE + DERIVED]** No existe ni se crea registry global, base de datos de
cambios, entidad universal `Change`, tracker universal ni registro central de
series (ADR-15 opción A rechazada; RFC-75 Mecanismos 8/9/15; ADR-16 AU-4). La
pertenencia al régimen debe derivarse de **señales documentales existentes y
verificables en el propio artifact**, sin reinterpretar retroactivamente
artifacts legacy (§9) y sin convertir una señal documental en autoridad
semántica.

### 8.1 Señales de membresía (C-1 y C-2)

**[PROPOSED — Future Implementation]** Un Plan es miembro del **Change Lifecycle
regime** (inspeccionable por C-1/C-2) si **todas** las siguientes condiciones
se cumplen sobre el artifact mismo:

1. **Nivel de archivo**: es un Plan numerado bajo `docs/plans/` (archivo con
   prefijo numérico y slug en minúsculas, excluyendo anexos `-anexo-`; mismo
   filtro estructural que aplica `tools/check_plan_structure.py` a los
   documentos numerados de gobernanza).
2. **Estructura de Plan del régimen nuevo**: contiene las secciones contenedoras
   del template vigente de Plan — `## Validation anchor` y
   `## Checkpoint / cierre` (encabezados presentes en
   `docs/plans/_TEMPLATE.md`). Estas secciones fueron introducidas al template
   por el Incremento 1+3 (plan 96) y son el discriminador estructural
   determinista de "nacido bajo el régimen actual" (ausencia de campos =
   legacy, RFC-75 Mecanismo 15).
3. **Metadata/relación corroborante (no suficiente por sí sola)**: el header
   declara `**Change Level:**` (intake operacional desde el Incremento 1) y/o
   referencia la serie (`RFC: RFC-75` o cadena de dependencia a la serie).
   Estas señales corroboran pero **no definen** la membresía, para no hacer de
   "tiene Change Level" la regla (RFCs con Change Level opcional y artifacts
   híbridos no entran por esa vía).
4. **Tipo de artifact**: no es RFC, ADR, INDEX, CHANGELOG, template, artifact
   de sesión ni archivo del payload del Protocol.

La membresía se evalúa por artifact, por estado de contenido al momento de
correr el checker; no se mantiene estado entre ejecuciones (sin registry; INDEX
es descriptivo, ADR-16 AU-4).

### 8.2 Caso límite / híbrido

**[PROPOSED]** Un artifact con señales de intake del régimen nuevo (p. ej.,
`**Change Level:**`) pero **sin** las secciones contenedoras del template
(`## Validation anchor` / `## Checkpoint / cierre`) es un **caso límite**: no se
clasifica por inferencia. El checker lo reporta como `BOUNDARY`/`GAP` advisory
(evidencia estructural ambigua, discriminador de ausencia de RFC-75 Mecanismo
15) sin tratarlo como miembro ni como legacy firme, y deja la decisión a
revisión humana (AU-3). No se inventa una regla de membresía nueva.

### 8.3 Población por checker (perímetro de inspección)

**[PROPOSED — Future Implementation]**

- **C-1 (anchor)** inspecciona los miembros que **registran o declaran una
  validación**: miembros cuya sección `## Validation anchor` tiene contenido o
  cuyo estado/registros declaran resultados de validación (status `Executed` /
  condición derivada `Closed` en la sección de cierre, o `## Nota de ejecución`
  con claims de verificación). Un miembro en estado `Aprobado para ejecución`
  (PLANNED) con la sección vacía no declara validación registrada: se reporta
  `N/A` (sin claim que verificar), no como GAP ni anomalía.
- **C-2 (checkpoint)** inspecciona los miembros cuya sección
  `## Checkpoint / cierre` tiene contenido (registran la relación de cierre o
  declaran la condición derivada `Closed`). Miembros sin contenido de cierre:
  `N/A` (no cerrados; `Executed` sin `Closed` es legal, CL-4). Legacy sin la
  sección: `EXCLUDED`.
- **Fuera de la población** (siempre): RFCs, ADRs, INDEX, CHANGELOG, templates,
  artifacts de sesión, `protocol/.agents/`, `.agents/` raíz (no existe),
  `dist/`, runtime, harness y cualquier artifact legacy (§9).

Si aparece una ambigüedad de población no resoluble con las fuentes actuales,
se documenta como **decisión/pending de planificación** (no se inventa la
regla) y se escala (§22 OQ-7; §24).

## 9. Legacy y no retroactividad

**[NORMATIVE]** Regla incorporada explícitamente:

> Los checkers no deben reinterpretar silenciosamente artefactos legacy como si
> hubieran sido creados bajo el régimen actual.

Consecuencias operativas:

- **Discriminador de legacy** (RFC-75 Mecanismo 15): la ausencia de los campos
  nuevos (secciones contenedoras de anchor/checkpoint del template) indica
  legacy, **no invalidez**. Planes 94/95 (y anteriores) no llevan las secciones:
  no entran al régimen y ningún checker los reporta como defectuosos.
- **Sin backfill automático**: no se introduce ningún mecanismo que migre,
  complete o "repare" artifacts legacy; el backfill (p. ej., relación G1 o la
  serie RFC-71..74) sigue siendo opcional y humano, nunca mecánico.
- **Coexistencia**: un artifact nuevo puede referenciar uno legacy; el legacy no
  se reescribe para cumplir metadata nueva.
- **In-flight**: un Plan en vuelo durante un incremento puede terminar bajo
  reglas previas (legacy) o adoptar las nuevas; el trabajo nuevo adopta las
  reglas nuevas (RFC-75 Mecanismo 15).
- La ejecución futura debe incluir tests que demuestren: exclusión correcta de
  legacy; inclusión correcta de artifacts del régimen nuevo; ausencia de falsos
  positivos por estructuras históricas (§16).

## 10. C-1 — Lifecycle Anchor Checker (especificación de implementación futura)

**[PROPOSED — Future Implementation]** Esta sección especifica el comportamiento
futuro de C-1 para que otro agente lo implemente sin reinterpretar decisiones;
ningún archivo se crea en esta iteración.

### 10.1 Archivos propuestos

- `tools/check_lifecycle_anchor.py`
- `tests/test_check_lifecycle_anchor.py`

### 10.2 Input

- Raíz del repositorio (convención de los checkers existentes: root por defecto
  desde la ubicación del script o argumento explícito, p. ej. `--root`); paths
  opcionales para inspección acotada durante dogfooding.
- Lectura **solo** de archivos: planes numerados bajo `docs/plans/`, template
  de referencia y fuentes normativas si se usan como diccionario de campos.
- Sin red; sin servicios externos; sin estado externo; sin escritura.

### 10.3 Output

- Reporte humano en stdout, determinista y estable, con una línea por artifact
  sujeto clasificada como:
  - `EXCLUDED` — no miembro del régimen (legacy u otro tipo);
  - `N/A` — miembro sin validación registrada que verificar (p. ej., PLANNED);
  - `VALID` — anchor presente y estructuralmente consistente;
  - `GAP` — información requerida ausente o no verificable (advisory);
  - `ANOMALY` — información presente pero incompatible (contradicción).
- Resumen final de conteos por clasificación.

### 10.4 Exit semantics

- `exit 0`: sin anomalías detectadas.
- `exit 1`: al menos una anomalía (información presente pero incompatible).
- Los `GAP` se reportan en el output pero **no convierten por sí solos el exit
  en no-cero**: la ausencia de evidencia no es invalidación
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`; regla
  transversal de `docs/CONVENTIONS.md:Regla transversal — target semantics vs operationalización`).
- `EXCLUDED`/`N/A` nunca generan infracción.

### 10.5 Reglas

1. **R-C1-1 (membresía)**: aplicar §8.1.
2. **R-C1-2 (forma)**: para todo miembro con contenido en
   `## Validation anchor`, verificar la presencia de los campos mínimos v1
   (`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`):
   declared scope; validation command-set; effective inputs (repo content);
   observed dependencies (`no instrumentado` permitido); environmental factors;
   Scoped Content Identity (state identity y delta scoped identity según el
   formato v1 de `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:13. Scoped Content Identity (algoritmo v1)`);
   validity / stale.
3. **R-C1-3 (GAP)**: miembro que declara validación registrada (status
   `Executed`, condición derivada `Closed` o claims de verificación en su
   `## Nota de ejecución`) con sección de anchor vacía o campo requerido
   ausente → `GAP` (advisory). El checker **no** convierte la ausencia en
   invalidación ni en autoridad normativa inexistente.
4. **R-C1-4 (anomalía)**: campos presentes pero incompatibles — p. ej., campo
   duplicado con valores distintos; formato de identidad inválido (tree id /
   delta id fuera del formato esperado por el algoritmo v1); `Validity / stale`
   con valores contradictorios (p. ej., `vigente` y `stale` a la vez);
   revalidación A2 declarada sin la referencia mínima a A1 (registro mínimo de
   revalidación de `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`) → `ANOMALY`.
5. **R-C1-5 (autoridad)**: C-1 no aprueba decisiones humanas, no resuelve
   conflictos normativos, no crea excepciones y no cambia estados de
   RFC/ADR/Plan (§14). El reporte es evidencia factual.

### 10.6 Población, GAP, anomalías, exclusiones

- Población: §8.3 (C-1).
- GAP: ausencia/no verificabilidad de información requerida (advisory).
- Anomalía: contradicción interna o contra el formato/estado factual
  verificable sin Git.
- Exclusiones: legacy (sin secciones contenedoras), RFCs/ADRs/INDEX/CHANGELOG/
  templates/sesión/payload, miembros sin claims de validación (`N/A`).

### 10.7 Determinismo, dependencias, entorno

- Determinismo: iteración ordenada de artifacts; sin timestamps ni estado en la
  lógica de decisión; mismo repo → mismo reporte.
- Dependencia de Git: **ninguna en v1** (C-1 verifica forma/estructura; la
  identidad Git material se verifica en C-2).
- Sin red; sin estado externo; sin autoridad normativa.
- Implementación preferida: stdlib (`pathlib`, `re`, `argparse`) + mecanismos
  ya existentes en el repo (`tools/check_plan_structure.py`,
  `tools/check_plan_citations.py` como referencia de convención), sin
  dependencias nuevas.

## 11. C-2 — Lifecycle Checkpoint Checker (especificación de implementación futura)

**[PROPOSED — Future Implementation]** Esta sección especifica el comportamiento
futuro de C-2; ningún archivo se crea en esta iteración.

### 11.1 Archivos propuestos

- `tools/check_lifecycle_checkpoint.py`
- `tests/test_check_lifecycle_checkpoint.py`

### 11.2 Input

- Raíz del repositorio (convención de los checkers existentes); lectura de
  planes miembros con sección `## Checkpoint / cierre` poblada (§8.3).
- Primitivas Git **locales y read-only** (las mismas del algoritmo v1:
   `git rev-parse`, `git cat-file`, `git ls-tree`; `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md:13. Scoped Content Identity (algoritmo v1)`).
- Sin red; sin servicios externos; sin escritura; sin dependencia de `origin` ni
  de la rama `dev` para decidir identidad material.

### 11.3 Obtención del Git tree e identidad comparada

- **Tree identity** = identidad material del estado validado/cerrado, obtenida
  por primitivas content-addressed de git (tree id de `git write-tree`/`git
  rev-parse <commit>^{tree}` sobre el estado que el checkpoint declara).
- El commit SHA registrado es **locator** (contexto Git), nunca identidad
  semántica del checkpoint
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`;
  `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`).
- C-2 verifica la **existencia** del objeto (tree) en la base de objetos local
  (`git cat-file -e`) y compara **tree ids**; **no** exige reachability desde
  `dev`/`origin` ni ancestría (no existe regla normativa que lo requiera; §24).

### 11.4 Información mínima que debe existir en el checkpoint

Campos del registro de checkpoint (formato v1 del plan 96 y template):

- commits de cierre (lista de locators);
- estado validado (ref al anchor A1 y, si existe, A2);
- estado de cierre (tree id);
- consistencia checkpoint↔anchor (PASS/FAIL + evidencia);
- governance aplicada;
- condición derivada (`Closed` docs-only | `Closed` con release pendiente | no
  cerrado (motivo)).

### 11.5 Reglas y detección de discrepancia

1. **R-C2-1 (GC-1)**: para todo miembro que registra cierre, determinar el
   anchor de la validación cuyo estado validado corresponde al estado de
   cierre (A1 si el estado de cierre es el de A1; A2 si existe una revalidación
   cuyo estado revalidado es el estado de cierre) y comparar la identidad
   scoped del estado de cierre con la del anchor correspondiente
   (`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`).
2. **R-C2-2 (revalidation)**: si el checkpoint declara revalidación (A2), A2
   debe estar registrada en el mismo artifact con la referencia a A1, estado
   revalidado, command-set (por ref si idéntico), cambios de factores y
   resultado; A2 **no** muta ni reemplaza A1 (§12).
3. **R-C2-3 (tree vs SHA)**: mismo tree con SHA distinto (rebase/amend/
   cherry-pick de contenido scoped idéntico) → **válido**; tree distinto →
   evaluar contra los anchors; SHA distinto por sí solo nunca es discrepancia.
4. **R-C2-4 (discrepancia/anomalía)**: discrepancia real cuando la información
   presente es incompatible — p. ej., el tree id declarado como estado de
   cierre no coincide con el tree del/los commit(s) de cierre declarado(s); el
   estado de cierre no coincide con A1 ni con ningún A2 aplicable mientras el
   texto declara consistencia PASS; A2 declarada sin A1; contradicción entre
   la condición derivada declarada y el contenido.
5. **R-C2-5 (GAP)**: información insuficiente — anchor referenciado no
   resoluble en el artifact; tree/commit locator no verificable en la base de
   objetos; factores relevantes ausentes del registro. `GAP` es advisory; la
   falta de evidencia no invalida el estado (CL-2).
6. **R-C2-6 (no reachability)**: nunca se exige que el commit/tree sea
   ancestro de `dev` o de `origin/dev`; objetos existentes no alcanzables desde
   `dev` son verificables y válidos.
7. **R-C2-7 (autoridad)**: C-2 es factual/advisory; no cierra planes, no
   resuelve conflictos normativos, no fabrica evidencia (§14).

### 11.6 Exit semantics de C-2

- `exit 0`: sin anomalías; incluye casos `VALID`, `GAP` (advisory) y `N/A`/
  `EXCLUDED`.
- `exit 1`: al menos una anomalía (discrepancia real de identidad/consistencia
  o contradicción interna).
- Casos advisory: GAP (evidencia insuficiente), casos límite de población.
- Casos válidos: checkpoint consistente con el anchor correspondiente (A1 o
  A2), tree identity idéntica, SHA distinto con tree idéntico, objetos válidos
  no alcanzables desde `dev`.

### 11.7 Determinismo, dependencias, entorno

- Determinismo: mismas primitivas git read-only, iteración ordenada, sin
  timestamps en la lógica; mismo repo → mismo reporte.
- Dependencia de Git: local/read-only, necesaria y suficiente; sin red; sin
  estado externo; sin dependencia de ramas remotas.
- Stdlib + subprocess de git read-only (mecanismo ya usado por los checkers y
  por el algoritmo v1); sin dependencias nuevas.

## 12. Modelo A1/A2 (obligatorio)

**[NORMATIVE]** Se preserva exactamente la decisión arquitectónica ya tomada
(Decisión B, `fc52c88`; `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`):

- A1 = anchor original de la primera validación.
- A2 = nuevo anchor correspondiente a una revalidación.
- **A2 no muta ni reemplaza A1**: A1 conserva su significado histórico (valida
  S1) y nunca se reescribe ni se reinterpreta.
- **A2 referencia A1** (lineage histórico `A1 → A2`, no mutación).
- El estado de validación es **relativo al anchor correspondiente** (CL-2):
  V1 es vigente para S1; un estado S2 relevante requiere revalidación aplicable
  antes de usarse como evidencia de cierre.
- Un cambio de anchor **no implica automáticamente** que la validación anterior
  sea semánticamente inválida.
- C-2 debe poder distinguir: validación original (A1); revalidación (A2 con ref
  a A1); estado actualizado (cierre contra A2); ausencia de evidencia
  suficiente (GAP advisory).
- No se inventa una state machine global para A1/A2: es una relación de
  evidencia entre validaciones del mismo contrato.

## 13. Checkpoint semantics

**[NORMATIVE]** Regla incorporada explícitamente y dejada implementable:

> GC-1 compara el estado de cierre con el anchor correspondiente a la
> validación cuyo estado validado es el estado de cierre.

- El checkpoint es una **relación documentada/verificable** closure↔estado Git,
   no una entidad global ni "tener un commit"
   (`docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`).
- No se diseñan: `Checkpoint` como entidad global; registry de checkpoints;
   base de datos; IDs globales; workflow externo; servicio central.
- `Closed` es condición derivada (Executed + governance + checkpoint +
   consistencia con revalidación si el estado de cierre difiere), no un status
   (`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`).

## 14. Autoridad

**[NORMATIVE]** Los futuros checkers NO son autoridades normativas: detectan y
reportan hechos observables (ADR-16). Clases de autoridad:

| Clase | Fuente |
|---|---|
| FACTUAL | Git / tests / checkers / tags |
| NORMATIVE | RFC `Accepted` / ADR / Plan aprobado |
| DECISION | humano / mantenedor |
| RELEASE | tag / dist |
| DESCRIPTIVE | INDEX |

Un checker no puede: aprobar una decisión humana; resolver un conflicto
normativo; crear una excepción; convertir una observación en política; cambiar
el estado de un RFC/ADR; cerrar automáticamente un Plan. Si encuentra una
contradicción normativa, la reporta/escala según las convenciones existentes
(`docs/adr/16-change-lifecycle-authority.md:Invariantes`; AU-3). `checker
output = factual evidence ≠ normative authority` y `anchor missing = GAP, no
invalidación` (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).

## 15. CI e integración

**[NORMATIVE + PROPOSED]**

- La integración inicial queda definida como **DEV-only / local invocation**:
  los checkers C-1/C-2 se ejecutan manualmente sobre el repo fuente durante el
  dogfooding (§17).
- **No** se agregan archivos a `.github/workflows/`; no pre-commit; no
  Makefile; no integración con la batería canónica de
  `docs/VERSIONING.md:4.1 Batería canónica de verificación` en esta Unidad.
- Los nuevos checkers no se incorporan a la batería canónica hasta que exista
  evidencia suficiente de estabilidad y falsos positivos controlados (los
  resultados del dogfooding de §17 alimentan esa decisión futura, que no
  pertenece a este Plan).
- Ejecución manual propuesta durante dogfooding (CLI exacta según la
  convención de los checkers existentes en la implementación):
  - `python tools/check_lifecycle_anchor.py` (y argumentos de root según la
    convención `--root`);
  - `python tools/check_lifecycle_checkpoint.py` (ídem);
  - interpretación del reporte según §10.4/§11.6; los `GAP`/`ANOMALY` se
    evalúan por revisión humana antes de cualquier acción.

## 16. Estrategia de testing futura

**[PROPOSED — Future Implementation]** Tests deterministas; preferencia:

- `pytest` con `tmp_path`;
- repositorios Git temporales/fake cuando sea necesario (C-2);
- fixtures mínimas;
- sin red; sin servicios externos; sin depender de un estado concreto de
  `origin`; sin depender de la rama `dev` para determinar identidad material.

Cobertura mínima exigida:

### 16.1 C-1

1. anchor válido (todos los campos v1 presentes y consistentes);
2. anchor ausente (miembro con validación declarada y sección vacía → GAP);
3. anchor incompleto (campo requerido faltante → GAP);
4. GAP (información requerida no verificable → advisory, exit 0);
5. contradicción/anomalía (campos duplicados/incompatibles → exit 1);
6. artifact legacy excluido (sin secciones contenedoras → EXCLUDED);
7. artifact nuevo incluido (miembro del régimen con claims → sujeto);
8. comportamiento determinista (mismo repo → mismo reporte).

### 16.2 C-2

1. checkpoint válido;
2. tree identity válida (estado de cierre == tree del commit de cierre);
3. tree identity incorrecta (discrepancia → anomalía);
4. checkpoint ausente (miembro sin cierre declarado → N/A);
5. información insuficiente/GAP;
6. A1 válido (cierre contra A1);
7. A2 válido (cierre contra A2);
8. A2 que referencia A1 (lineage presente);
9. estado de cierre coincidente con anchor correcto;
10. estado de cierre incompatible (no coincide con A1 ni A2 aplicable → anomalía);
11. commit SHA diferente pero tree idéntico (válido; SHA ≠ identidad);
12. tree diferente (evaluación de aplicabilidad, no invalidación automática);
13. no exigir reachability desde `dev` (objeto válido no alcanzable → válido);
14. comportamiento determinista.

No se agregan tests que requieran inventar estructuras normativas inexistentes.

## 17. Dogfooding

Distinción obligatoria:

### 17.1 Creación física del Plan 98 (esta iteración)

No implementa ni ejecuta C-1/C-2; no corre los checkers (no existen); no fabrica
anchor/checkpoint de ejecución (secciones finales).

### 17.2 Ejecución futura del Plan 98

**[PROPOSED — Future Implementation]** Deberá:

1. implementar C-1 (§10);
2. testear C-1 (§16.1);
3. commit C1 (§18);
4. implementar C-2 (§11);
5. testear C-2 (§16.2);
6. commit C2 (§18);
7. ejecutar ambos sobre el repositorio real (dev, working tree limpio salvo los
   cambios del plan);
8. registrar resultados (outputs completos o resumen con clasificaciones y
   conteos en la `## Nota de ejecución`);
9. evaluar falsos positivos/negativos contra una verificación manual previa de
   los sujetos esperados (planes 96/97 como `VALID`, legacy 94/95 como
   `EXCLUDED`, este plan como `N/A` en estado PLANNED);
10. crear el Validation Anchor de la ejecución (V1 sobre C1; V2 sobre el estado
    final si difiere, según el patrón de los planes 96/97);
11. crear el Checkpoint de cierre con consistencia GC-1 (secciones finales);
12. verificar closure (governance + consistencia + batería según §24.1 del plan
    94);
13. cerrar el Plan (registro en INDEX, changelog docs-only según convención,
    condición derivada `Closed` docs-only; sin `VERSION` bump ni tag).

Los resultados del dogfooding son evidencia factual; no autorizan por sí mismos
cambios normativos ni la incorporación de los checkers a la batería canónica
(decisión humana posterior).

## 18. Commits futuros

**[PROPOSED — Future Implementation]** Se mantienen dos commits de
implementación:

```text
C1 = Lifecycle Anchor Checker
C2 = Lifecycle Checkpoint Checker
```

- C1 no debe mezclar implementación de C2.
- C2 no debe reescribir C1 salvo corrección estrictamente necesaria y
  justificada.
- Los commits deben ser auditables; no se hace un único commit monolítico si
  puede evitarse.
- Los commits **no constituyen por sí mismos el cierre del Plan**:

```text
Executed != Committed
Committed != Closed
Closed != Released
```

- Mensajes propuestos (Conventional Commits, inglés):
  - C1: `feat(tools): add lifecycle anchor checker (plan 98, RFC-75)`
  - C2: `feat(tools): add lifecycle checkpoint checker (plan 98, RFC-75)`
- El registro de cierre no embebe su propio SHA/tree (auto-referencia
  excluida); la consistencia se verifica post-commit
  (`git rev-parse <C2>^{tree}` contra el anchor del estado de cierre).
- En la iteración de creación **no se ejecuta ningún commit** (mandato del
  mantenedor, 2026-09-02); el registro queda en el working tree. Si el
  mantenedor exige un commit de creación/registro, se crea aparte y antes de
  autorizar la ejecución, sin mezclarse con C1/C2.

## 19. Change Level

**[PROPOSED]** Clasificación prospectiva de dogfooding declarada al crear el
plan (regla operacional de intake; `docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)`):

| Dimensión | Valor | Justificación |
|---|---|---|
| coordination | 1 | Un solo cambio DEV, serie cerrada, un ejecutor |
| scope | 2 | Dos checkers + dos suites de tests en `tools/` y `tests/` |
| architectural impact | 1 | Mecanismos factuales/advisory, fuera de la batería canónica, sin autoridad |
| release impact | 1 | Sin payload, sin `VERSION`, sin tag |
| duration/complexity | 2 | Dos checkers con lógica Git read-only y 22 escenarios de test |
| **Level = max** | **L2** | `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels` |

Mutable con justificación documentada (upgrade obligatorio ante triggers;
downgrade con nota). Change Level ≠ clase RFC-56 (ejes independientes;
`docs/CONVENTIONS.md:Change Lifecycle — Change Levels (modelo objetivo)`).

## 20. Métricas

**[NORMATIVE + DERIVED]** No se implementan métricas de lifecycle en Plan 98:

- La observabilidad futura es necesaria, pero pertenece a decisiones posteriores
  (posible tracker condicional / handoff), no a esta Unidad.
- El corpus actual es demasiado pequeño para métricas significativas (2
  anchors/checkpoints reales); cualquier métrica que dependa de denominadores
  insuficientes debe permanecer `N/A` (schema ≠ medición;
  `docs/VERSIONING.md:11. Métricas del Change Lifecycle (observability schema baseline)`).
- No se inventan números de cobertura, tasas de findings, stale rate,
  correction rate ni similares; 0 registros = `not applicable / insufficient
  sample`, no "0% compliance".
- Los checkers C-1/C-2 **no** computan métricas; su salida puede alimentar
  futuras métricas derivadas por decisión humana posterior.

## 21. SCI / Context Identity

**[DERIVED + OPEN]** El Planning Report identificó la evaluación de
SCI/Scoped Content Identity como una cuestión que puede merecer tratamiento
arquitectónico. Plan 98:

- **documenta la observación** (¿el SCI v1 requiere semántica adicional para
  ser identidad de correctness de validación DEV? Es el ADR candidate que el
  plan 94 registra en su sección de candidatos
  (`docs/plans/94-change-lifecycle-master-action-plan.md:22. Candidatos a ADR`);
  la elevación es decisión humana diferida);
- **evalúa la necesidad real**: C-1/C-2 consumen los valores de SCI **ya
  registrados** (tree id / delta) como datos, sin definir semántica nueva;
- **prepara evidencia** para un ADR/RFC futuro si el consumo cruzado lo
  justifica;
- **NO decide silenciosamente una semántica nueva de SCI** (§22 OQ-4/OQ-5).

Si durante la creación o ejecución se detecta que una regla no está
suficientemente autorizada: no se inventa; se marca como decisión pendiente con
la autoridad humana/normativa que debería resolverla; no se bloquea el resto del
Plan si la cuestión no es necesaria para C-1/C-2 (aquí no lo es: el formato v1
es dato consumido, no rediseñado).

## 22. Pending y Open Questions

**[OPEN]** No existe **blocking pending**: las cuestiones abiertas son
no-bloqueantes y no impiden la creación de este artifact ni la futura ejecución
de C-1/C-2. Registro PC-1 en la sección final `## Findings / Correcciones /
Pending`.

| # | Pregunta / decisión | Tipo | Resolución propuesta / estado |
|---|---|---|---|
| OQ-1 | ¿Backfillear G1 (plan 91) como ejemplar? | HUMAN | No por defecto (Mec. 15); backfill opcional, nunca mecánico |
| OQ-2 | ¿Ajustar el sufijo "implementación pendiente" del header de RFC-75 (OPEN-4)? | HUMAN | Heredado de la serie; fuera de scope; escalar sin decidir en el plan |
| OQ-3 | ¿Registrar la Decisión B en el Amendment Log de RFC-75? | HUMAN | Recomendado; nunca silencioso; fuera de esta Unidad |
| OQ-4 | ¿Elevar el ADR candidate de SCI/Scoped Content Identity? | HUMAN | Diferido al primer consumo/evidencia (criterio ADR-16) |
| OQ-5 | ¿Elevar el ADR candidate de Change Level como eje independiente? | HUMAN | Diferido; no aplica en esta Unidad |
| OQ-6 | Autorización humana de ejecución y de commits C1/C2; aceptación de cierre (batería) | HUMAN | Gates de ejecución (§17.2, §26) |
| OQ-7 | Ambigüedades de población/parseo si aparecen en la implementación (casos límite, texto exacto de secciones) | CAN DECIDE IN PLAN / ESCALAR | Resolver en la implementación con las reglas de §8; si no resoluble → STOP + escalación (AU-3, §24) |
| OQ-8 | Extensión futura a anchors de Amendment Logs de RFC | HUMAN (futuro) | Fuera del MVP; corpus actual sin ejemplos; no se diseña ahora |

No se convierten automáticamente estas cuestiones en scope de Plan 98.

## 23. Acceptance Criteria

Checklist de aceptación del artifact físico (esta iteración) y del alcance que
define:

- [ ] **AC-01** — El Plan 98 existe en la ubicación/naming correcto
      (`docs/plans/98-change-lifecycle-unit-d-increment-4.md`).
- [ ] **AC-02** — Está registrado según las convenciones vigentes (INDEX mirror,
      status del ciclo vigente, sin placeholders).
- [ ] **AC-03** — Su alcance es exclusivamente C-1 + C-2 (§5/§6/§7).
- [ ] **AC-04** — La población del régimen nuevo está definida sin crear
      autoridad semántica accidental (§8).
- [ ] **AC-05** — C-1 tiene especificación suficientemente determinista para
      futura implementación (§10).
- [ ] **AC-06** — C-2 tiene especificación suficientemente determinista para
      futura implementación (§11).
- [ ] **AC-07** — Se preservan las semánticas A1/A2 (§12).
- [ ] **AC-08** — Se preserva tree identity frente a commit SHA (§11/§13).
- [ ] **AC-09** — No se exige reachability desde `dev` sin autorización
      normativa (§11.5/§24).
- [ ] **AC-10** — Legacy queda fuera del régimen sin backfill automático (§9).
- [ ] **AC-11** — Los checkers son descritos como mecanismos
      FACTUAL/advisory (§10/§11/§14).
- [ ] **AC-12** — No se crea ningún mecanismo de autoridad global (§6/§8/§13).
- [ ] **AC-13** — No se modifica Protocol ni `protocol/.agents/` (§6; verificación
      git en §26).
- [ ] **AC-14** — No se crea root `.agents/` (§6; verificación git en §26).
- [ ] **AC-15** — No se incorpora CI (§6/§15).
- [ ] **AC-16** — F-n/C-n/stale/series/metrics quedan fuera de scope (§6).
- [ ] **AC-17** — El futuro testing strategy cubre positivos, negativos y
      boundaries (§16).
- [ ] **AC-18** — Se especifican commits C1/C2 separados (§18).
- [ ] **AC-19** — Se especifica dogfooding posterior (§17).
- [ ] **AC-20** — El Plan define anchor/checkpoint/closure para su propia futura
      ejecución (secciones finales).
- [ ] **AC-21** — El Plan no se declara Executed/Closed durante esta tarea
      (header `Aprobado para ejecución`; banner de apertura).

## 24. Recovery / Stop Conditions

**[PROPOSED]** La ejecución futura debe **detenerse** si ocurre cualquiera de
estos casos:

- RFC-75/ADR-15/ADR-16 presentan una contradicción no resoluble;
- la implementación requiere modificar Protocol (`protocol/.agents/`);
- la implementación requiere crear `.agents/` en la raíz;
- aparece una necesidad de registry global;
- aparece una necesidad de state machine global;
- C-1 no puede distinguir razonablemente población nueva de legacy;
- C-2 requiere una semántica de identidad que no está autorizada;
- la implementación requiere CI para funcionar;
- los tests requieren red/servicios externos;
- aparece un requisito de F-n/C-n/stale/series/metrics no previsto;
- el cambio deja de ser DEV-only;
- surge una DECISION humana nueva no autorizada.

En esos casos:

**STOP.** No se improvisa una solución arquitectónica; se documenta, se escala
al mantenedor (AU-3) y se espera decisión.

## 25. Riesgos

**[DERIVED]**

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Checker como autoridad normativa | Alto | §14; GAP ≠ invalidación; output factual |
| Población mal definida (todo lo que tenga Change Level) | Alto | §8: señales estructurales + discriminador de legacy; caso límite a humano |
| Falsos positivos sobre legacy | Alto | §9: exclusión estructural; tests de legacy (§16) |
| SHA como identidad semántica | Alto | §11/§13: tree identity; tests de SHA distinto/tree igual |
| Reachability desde `dev` exigida por error | Medio | §11.5/§16: tests explícitos sin ancestría |
| Scope leakage (automatizar F-n/stale/series/metrics) | Alto | §6/§7; AC-16 |
| Ambigüedad A1/A2 mal implementada | Alto | §12; tests C-2 6–10 |
| Concurrencia en archivos compartidos | Medio | Serialización (`docs/VERSIONING.md:8. Ejecución en paralelo`) |
| ACL del sandbox en pytest | Bajo (ambiental) | Permisos reales; reporte honesto (plan 94 §24.1) |
| Dogfooding sin sujetos suficientes | Bajo | Corpus real (96/97) + este plan como `N/A` + legacy como `EXCLUDED` |

## 26. Criterios de salida y verificación

Criterios de salida de la **iteración de creación** (esta tarea):

- [ ] Artifact físico del Plan 98 creado y registrado en INDEX (status
      `Aprobado para ejecución`; sin placeholders; sin commits).
- [ ] Sin cambios fuera de alcance (git diff: solo `docs/plans/98-…` +
      `docs/plans/INDEX.md`).
- [ ] Checkers documentales pertinentes en verde (abajo).
- [ ] Estado `Planned`: no `Executed`/`Closed`; secciones finales sin anchor/
      checkpoint fabricados.

Verificación de esta iteración (checkers documentales canónicos pertinentes;
sin implementar C-1/C-2 para validarlos):

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

`check_dist_sync.py` permanece rojo en `dev` por su semántica local/release y no
se reinterpreta como fallo de este Plan. La batería al ejecutar la Unidad D usa
la política de "batería verde" del plan 94 (§24.1): PASS real o desviación
documentada aceptada por el mantenedor.

## 27. Matriz de trazabilidad

**[DERIVED]**

| Requisito | Fuente | Sección del Plan | Implementación futura | Verificación |
|---|---|---|---|---|
| VC-1 / anchor verificable | `docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors`; CONVENTIONS VC-1 | §10 | C-1 + tests | Suite C-1 (§16.1) |
| GC-1 / checkpoint ↔ anchor | `docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`; CONVENTIONS GC-1 | §11/§13 | C-2 + tests | Suite C-2 (§16.2) |
| Tree identity ≠ SHA | RFC-75 Mec. 7; Plan 96 v1 | §11.3/§11.5 | C-2 | Tests 11–12 (§16.2) |
| Safe automation / GAP / checker ≠ autoridad | `docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation` | §10/§11/§14 | C-1/C-2 | Revisión de autoridad |
| Legacy no retroactivo | `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`; RFC-46 | §8.1/§9 | C-1/C-2 | Tests de exclusión (§16) |
| Población sin registry | ADR-15; RFC-75 Mec. 8/9/15; ADR-16 AU-4 | §8 | C-1/C-2 | Revisión + caso límite |
| A1/A2 | Decisión B `fc52c88`; CONVENTIONS VC-1 | §12 | C-2 | Tests 6–10 (§16.2) |
| Gate de observabilidad | Plan 94 Unit D; VERSIONING §11 | §1/§7 | — | Corpus 96/97 real |
| Sin CI / DEV-only | Plan 94 Unit D | §6/§15 | — | Diff de la ejecución |
| Commits C1/C2 | Plan 94 Unit D; precedente 96/97 | §18 | Ejecución | Checkpoint |
| Dogfooding | Plan 94 §19 | §17 | Ejecución | Nota de ejecución |

## 28. Auditoría adversarial interna

**[DERIVED]**

| Criterio | Verdict | Evidencia / mitigación |
|---|---|---|
| Scope inflation | OK | §6/§7: solo C-1+C-2; F-n/stale/series/metrics fuera |
| Authority confusion | OK | §14: factual/advisory; GAP ≠ invalidación |
| Registry/entidad accidental | OK | §8/§13: sin registries, sin Change/Finding/Checkpoint entity |
| Git identity confusion | OK | §11/§13: tree identity; SHA locator; tests específicos |
| Legacy reinterpretado | OK | §9: discriminador estructural; tests de exclusión |
| Gate circular de observabilidad | OK | Datos reales 96/97 + template; no mediciones del Incremento 0 |
| Checker antes que datos | OK | Corpus con 2 anchors/checkpoints reales antes de automatizar |
| Protocol contamination | OK | DEV-only; `protocol/.agents/` intacto |
| No-alucinación | OK | Todo estado actual anclado a `ruta:sección` o verificación local; futuros como `PROPOSED` |

## 29. Veredicto final

**[DERIVED]** Sin BLOCKER ni contradicción arquitectónica detectados: la
secuencia `Plan 95 (0) → Plan 96 (1+3) → Plan 97 (2) → Plan 98 (4)` está
confirmada en los artifacts ejecutados y en el rollout de RFC-75; el alcance de
la Unidad D está determinado por Plan 94 (Implementation Unit D); el gate de
observabilidad está satisfecho con datos reales (planes 96/97); C-1/C-2 quedan
especificados sin crear autoridad, registries ni entidades. Estado de este
artifact al cierre de la iteración de creación:

```text
Plan 98 = Aprobado para ejecución (PLANNED / OPEN)
Implementation = NOT STARTED
Executed = NO
Committed = NO (sin commit en esta iteración)
Closed = NO
Released = NO
```

**PLAN 98 READY FOR IMPLEMENTATION — GO WITH CONDITIONS** (condiciones C1–C4,
§1/§22). Próximo paso: autorización humana de ejecución (OQ-6) y ejecución de
las fases de §17.2 sobre `dev`; esta tarea no implementa C-1/C-2 ni cierra el
Plan.

---

## Validation anchor

Registrado al ejecutar la Unidad D (Fases de §17.2). La validación **V1**
corrió sobre el contenido de implementación de C-1 (commit de contenido C1
`669a576`) **antes** de implementar C-2 y antes de agregar los registros de
cierre de esta sección (anti-circularidad, §18).

- Declared scope: C-1 — lifecycle anchor checker (`tools/check_lifecycle_anchor.py`
  + `tests/test_check_lifecycle_anchor.py`): suite de tests C-1 + batería
  canónica del repo + dogfooding sobre el contenido de implementación de C-1
  (especificación §10/§16.1).
- Validation command-set:
  - `python -m pytest tests/test_check_lifecycle_anchor.py`
  - `python -m pytest tests/`
  - `python tools/check_lifecycle_anchor.py`
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `git diff --check`
- Effective inputs (repo content): contenido completo del repo en el estado
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`,
  `runtime/` y la raíz; pytest consume `tests/` + `tools/` + `runtime/`);
  representado por el State identity (tree id). El working tree validado
  incluía además los registros de creación del Plan 98 (`docs/plans/INDEX.md`
  modificado + este plan sin trackear, pendientes de commit), ajenos al
  contenido de C-1 inspeccionado por la suite.
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en
  esta Unidad); el consumo por comando se observa de la documentación de cada
  checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 10.3.0; pytest ejecutado fuera
  del sandbox por ACL del basetemp `pytest-of-rolda` (ruido ambiental
  documentado); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `1a3e93e9a77ea9d89b436c22410a29dfc24f5806` (tree id; igual a
    `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 2 archivos del cambio de C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `9d523cce73a25d3482fde361d5b129231cd3c8787cb2954f367b4bff3c855e44`.
    Pares path → blob (C1): `tests/test_check_lifecycle_anchor.py` →
    `d00959df31c7ad5a7934f632e4d5ab47773650be`; `tools/check_lifecycle_anchor.py`
    → `3c5051727a8df48bd1392d0e437e385fee532caf`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería completa
  sobre el contenido final de la Unidad D, incluidos C-2 y los registros de
  cierre) antes del cierre (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7; §13 y §17.2 de
este plan). Se registra en el commit de registro C3, posterior a los commits de
contenido C1/C2 (multi-commit del plan).

- Commits de cierre:
  - C1 `669a5769ae6932e9280331365f5d5b7bc8b5af48` —
    `feat(tools): add lifecycle anchor checker (plan 98, RFC-75)`
    (contenido de C-1 validado por V1).
  - C2 `9b5b8a163a44904965d40b94b3f30c429b18cf4a` —
    `feat(tools): add lifecycle checkpoint checker (plan 98, RFC-75)`.
  - C3 — este commit de registro
    (`docs(plans): record plan 98 validation anchor and checkpoint (plan 98,
    RFC-75)`); su SHA se identifica por el mensaje y el árbol no embebe su
    propia identidad (auto-referencia excluida, §18).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `1a3e93e9a77ea9d89b436c22410a29dfc24f5806`; Delta scoped identity =
  `9d523cce73a25d3482fde361d5b129231cd3c8787cb2954f367b4bff3c855e44`.
- Estado de cierre: tree id del último commit de cierre (C3) =
  `git rev-parse C3^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C3^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`1a3e93e9…`) → **PASS**.
  - Estado final (C3): difiere de C1 en C-2 y en los registros de cierre
    (anchor/checkpoint de este plan, INDEX y changelog); **revalidación V2**
    (batería canónica completa + checkers C-1/C-2 sobre el contenido final
    staged, ejecutada antes del commit) → PASS. GC-1 queda satisfecho por
    revalidación antes de `Closed` (la consistencia del estado de cierre se
    evalúa contra A2/V2).
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 98, RFC-75)` en `CHANGELOG.md:[Unreleased]`; docs-only, sin `VERSION`
  bump ni tag.
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (C1 + C2 + C3 en `dev`), `Closed` (condición derivada con
  checkpoint y consistencia), `Released` (no aplica: sin promoción ni tag).

## Findings / Correcciones / Pending

Registros reales de esta iteración de creación (artefactos nuevos bajo las
reglas del Incremento 2; la ausencia de registros no es invalidez):

### Findings

- `No findings detected / N/A` (no se fabrican findings sintéticos).

### Correcciones

- `N/A` (ninguna corrección en esta iteración).

### Pending decisions

Pendings **no-bloqueantes** (PC-1), owner: mantenedor, escalación: humana
(AU-3); registro completo y detalle en §22:

- **OQ-1** — backfill G1 / plan 91: decisión humana opcional; blocking: no.
- **OQ-2** — OPEN-4 (sufijo del header de RFC-75): decisión humana;
  blocking: no.
- **OQ-3** — registro eventual de la Decisión B en el Amendment Log de
  RFC-75; decisión humana; blocking: no.
- **OQ-4** — ADR candidate SCI/Scoped Content Identity; elevación
  diferida; blocking: no.
- **OQ-5** — ADR candidate Change Level; elevación diferida; blocking: no.
- **OQ-6** — autorización de ejecución y commits C1/C2; gate humano;
  blocking: no (no bloquea esta iteración de creación).
- **OQ-7** — ambigüedades de población/parseo si aparecen al implementar;
  resolución en la implementación con STOP/escalación; blocking: no.
- **OQ-8** — extensión futura a anchors de Amendment Logs de RFC;
  decisión humana futura; blocking: no.

## Trazabilidad

Origen → RFC-75 (`Accepted`) + ADR-15/16 (`Accepted`) → Plan 94 (Master Action
Plan; Unidad D / Incremento 4) → Plan 95 (Incremento 0) → Plan 96 (Incrementos
1+3) → Plan 97 (Incremento 2) → **Plan 98 (Unidad D / Incremento 4, este
artifact)** → ejecución futura (C-1 → C-2 → dogfooding) → validación anclada →
checkpoint → cierre docs-only. Este plan no autoriza cambios de payload
(RFC-56); la autorización de la ejecución es humana (OQ-6).

## Nota de ejecución

- 2026-09-02 — **Creación/registro (planificación).** Plan 98 creado y
  registrado en `docs/plans/INDEX.md` (Trigésima serie; Status inicial
  `Aprobado para ejecución`, PLANNED / OPEN) a partir del Planning Report
  auditado (GO WITH CONDITIONS) y del estado factual del repo, **sin ejecutar
  la Unidad D** y sin commits (estado previo del working tree: `4513077` +
  los cambios de creación de este plan). Verificación de la iteración: checkers
  documentales canónicos en verde — `check_protocol_invariants.py` (212 files,
  9720 references), `check_plan_citations.py`, `check_plan_structure.py`,
  `check_taxonomy_coherence.py`, `check_session_artifacts.py` y
  `check_version_state.py` (warnings esperados de `dev`) — y pytest `340
  passed, 0 failed` (ejecutado fuera del sandbox por la ACL del basetemp
  `pytest-of-rolda`; ruido ambiental documentado). `check_dist_sync.py` no se
  reinterpreta en `dev` (semántica local/release). Sin cambios en `protocol/`,
  `runtime/`, `tests/`, `tools/`, VERSION, CHANGELOG, ADRs, RFCs ni planes
  94–97; sin creación de `.agents/` en la raíz; sin push.
- 2026-09-02 — **Ejecución de la Unidad D sobre `dev`.** Estado previo: HEAD
  `4513077`, working tree con los cambios de creación del plan (INDEX + este
  artifact, sin commit), pytest `340 passed, 0 failed`, checkers canónicos
  PASS (warnings esperados de `dev`). **C-1:** `tools/check_lifecycle_anchor.py`
  + `tests/test_check_lifecycle_anchor.py` implementados (19 tests; población
  por señales estructurales §8 — secciones contenedoras del template + `Change
  Level` corroborante; sin registry; legacy excluido; GAP advisory exit 0;
  anomalía exit 1; sin Git en v1). **Commit C1:** `669a576` (2 archivos; tree
  `1a3e93e9`). **C-2:** `tools/check_lifecycle_checkpoint.py` +
  `tests/test_check_lifecycle_checkpoint.py` implementados (21 tests; Git
  local read-only; tree identity = identidad material; SHA = locator; GC-1
  contra A1/A2; sin reachability desde `dev`). **Commit C2:** `9b5b8a1` (2
  archivos; tree `0a2cae5a`). **Gates:** pytest global `359 passed` (C-1) y
  `380 passed` (C-2); checkers canónicos en verde en ambos gates; `git diff
  --check` limpio. **Dogfooding conjunto (C-1 + C-2 sobre el repo real):**
  98 planes inspeccionados; planes 96/97 `VALID` (C-1: anchors v1 completos;
  C-2: `git rev-parse C1^{tree}` == T1 declarado — `b8add7d7…`/`0df8920c…`
  PASS), plan 98 `N/A` en estado PLANNED, legacy 01–95 `EXCLUDED`, GAP=0,
  ANOMALY=0 — sin falsos positivos/negativos respecto de la verificación
  manual. **Validación adversarial:** mismos árboles/SHA distinto (válido),
  árbol distinto sin A2 (anomalía), A1→A2 con lineage (válido), A1 no mutado
  (96/97 verificables), legacy excluido, anchor/checkpoint incompletos (GAP),
  contradicciones explícitas (anomalía), commit válido no alcanzable desde
  `dev` (válido), Protocol payload fuera del dominio. **Resolución de caso
  límite (OQ-7, §8.2):** el Plan 96 registra su contenedor de cierre bajo el
  encabezado `## Checkpoint` (variante del `## Checkpoint / cierre` del
  template); ambos checkers aceptan un heading level-2 cuyo texto normalizado
  comienza con "checkpoint", regla de parseo explícita y anclada al corpus,
  documentada en los docstrings de ambos tools. **Anchor/checkpoint de este
  plan:** V1 sobre C1 (T1 `1a3e93e9…`; delta `9d523cce…`), V2 (batería
  completa sobre el estado final staged) y checkpoint de cierre en las
  secciones finales; cierre docs-only. **Scope audit:** sin cambios en
  `protocol/`, `runtime/`, `tests/`/`tools/` ajenos a C-1/C-2, `.agents/` raíz,
  CI, VERSION, ADRs/RFCs ni planes 94–97; sin push.
