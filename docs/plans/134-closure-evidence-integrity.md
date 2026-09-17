# Plan 134 — Integridad de la evidencia de cierre (closure state vs. commit tree)

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; Clase B documental + tooling DEV, sin efecto sobre `protocol/.agents/`)
**Clase:** B (no aplica efecto payload; el Change no toca `protocol/.agents/`)
**Change Level:** L2
**Depende de:** plan 133 (`Closed`)
**Origen:** `<PLAN-133>:F-5` y su corrección `<PLAN-133>:C-4`; observación de que
el closure tree declarado puede no coincidir con el árbol material del commit de
cierre; evidencia de un patrón equivalente en los Planes 120 y 123–132. Consigna
del mantenedor (2026-09-15) que autoriza investigar el mecanismo y corregirlo si
la evidencia demuestra un defecto real.

## Objetivo

Determinar con precisión, y con evidencia verificable, la semántica y la cadena
de evidencia de `baseline`, `anchor`, `validated state`, `checkpoint`,
`closure state`, `closure tree`, `commit tree`, `committed state` y `Closed`; y
responder:

> ¿Qué estado exacto certifica un Plan cuando declara su closure tree, y qué
> relación debe existir entre ese estado, el anchor, la validación y el commit
> que materializa el cierre?

Corregir únicamente aquello que la evidencia demuestre defectuoso, sin forzar
una corrección si el modelo resulta correcto.

## Criterio de entrada

- [x] Autorización del mantenedor registrada en la consigna del Change.
- [x] `dev` limpio; baseline `git rev-parse HEAD` = `b0072145f2d6d3d4a065e439a27d631ed68ad28b`.
- [x] Batería canónica y gates C-1/C-2/C-3 en verde antes de tocar el repositorio.
- [x] Fuentes normativas localizadas y leídas (ADR-15, ADR-16, RFC-75 Mecanismos 5/6/7/14, `docs/VERSIONING.md`, `docs/CONVENTIONS.md`, `.agents/policies/validation-closure.md`, `.agents/workflows/change-lifecycle.md`, `_TEMPLATE.md`, C-1/C-2/C-3).
- [x] Próximo número libre de plan verificado = 134.

## Entregables

1. `docs/plans/134-closure-evidence-integrity.md` — este registro, con baseline, modelo semántico, cadena de evidencia, reproducción, análisis histórico, findings y corrección.
2. `docs/CONVENTIONS.md` — modelo normativo del estado de cierre y de la relación GC-1.
3. `.agents/policies/validation-closure.md` — §5 con la definición precisa del registro de cierre y del contrato de C-2.
4. `.agents/workflows/change-lifecycle.md` — §8 con la secuencia de cierre correcta.
5. `.agents/policies/lifecycle-checkers.md` — contrato de C-2 corregido; C-1/C-3 declarados `NOT_REQUIRED`.
6. `docs/plans/_TEMPLATE.md` — campo de cierre que distingue inequívocamente los conceptos.
7. `tools/check_lifecycle_checkpoint.py` — contrato de C-2 alineado con el modelo normativo.
8. `tests/test_check_lifecycle_checkpoint.py` — regresiones del contrato corregido.
9. `docs/plans/INDEX.md` y `CHANGELOG.md` — registro del Change.

## Pasos

1. **Baseline.** Registrar HEAD, rama, working tree, refs, `VERSION` y estado del Plan 133.
2. **Modelo semántico.** Definir cada término y sus relaciones desde las fuentes normativas, sin colapsar conceptos.
3. **Cadena de evidencia.** Tabla `input → validation → checkpoint → closure → commit → closed` con source of truth por elemento.
4. **Reproducción.** Demostrar o falsar el patrón F-5 bajo el mecanismo actual.
5. **Análisis histórico.** Planes 120 y 123–133: anchor, validated state, checkpoint, closure tree declarado, commit, commit tree y relación; clasificar cada caso.
6. **Determinar defectos** en modelo, procedimiento, C-2 y formato, con evidencia.
7. **Corregir** lo que corresponda y declarar `NOT_REQUIRED` lo que no.
8. **Verificar** con la batería canónica, C-1/C-2/C-3, la suite de C-2 y la reproducción.
9. **Registrar** el Plan, el índice, el changelog y las determinaciones de impacto.

## Criterios de salida

- [ ] Los nueve términos quedan definidos sin ambigüedad y con su source of truth.
- [ ] La pregunta central queda respondida de forma verificable.
- [ ] El resultado es A (defecto confirmado y corregido) o B (falso positivo), no un híbrido sin evidencia.
- [ ] Si hay corrección: contrato establecido, comportamiento evitado y regresión demostrada.
- [ ] Los Planes históricos no se modifican; su estado se clasifica.
- [ ] `protocol/.agents/`, `dist/`, los RFCs, los ADRs y los planes cerrados sin cambios.
- [ ] Batería canónica en verde; C-1/C-2/C-3 sin `ANOMALY`; suite de C-2 en verde.
- [ ] Commit atómico; sin push, merge, tag, release ni promoción.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
python -m pytest tests/test_check_lifecycle_checkpoint.py -q
python -m pytest tests/ -q
```

## Resultado de la investigación

### 1. Baseline

| Elemento | Valor |
|---|---|
| HEAD | `b0072145f2d6d3d4a065e439a27d631ed68ad28b` (`docs(plans): correct the plan 133 closure-state declaration (plan 133, C-4)`) |
| Rama | `dev` (`origin/dev` @ `4aa261774c034eba3bb6f4e51810513ce9e25933`; 12 commits sin push) |
| Working tree | limpio |
| `protocol/.agents/VERSION` | `11.5.0` |
| `master` | `dc21458`; último tag `11.2.0` (50 tags) |
| Plan 133 | `Executed`, condición derivada `Closed`, commits `c7ac44e` + `b007214` |
| Reproducción | `python tools/check_lifecycle_checkpoint.py` → 133 planes, `ANOMALY=0` (1 `GAP` preexistente: Plan 116) |

### 2. Semantic model

Los nueve términos **no son equivalentes**. Modelo derivado de ADR-15 (CL-3 y su
principio *persisted state ≠ materialized view*) y RFC-75 Mecanismo 7.

| Término | Definición | Identidad | Source of truth |
|---|---|---|---|
| **Baseline** | estado del repositorio al iniciar el Change (locator + refs) | commit SHA (locator) | Git |
| **Anchor** | registro de una validación: declared scope, command-set, effective inputs, environmental factors y Scoped Content Identity | su propio registro | `## Validation anchor` del artifact |
| **Validated state** | el estado del repositorio que la validación **consumió** | Scoped Content Identity (delta + state identity) | anchor |
| **Checkpoint** | relación **closure ↔ estado Git** documentada; no es artifact, ni "tener un commit", ni un SHA | — (relación) | sección de cierre del Plan |
| **Closure state** | el estado que el checkpoint **certifica**, definido por correspondencia GC-1 con el anchor aplicable | el del anchor aplicable (A1 o A2) | sección de cierre + anchor referenciado |
| **Closure tree** | **término ambiguo**: usado en el corpus para el tree id del estado de cierre (= el del estado validado). No debe usarse para el árbol del commit | — | — |
| **Commit tree** | tree id del commit de Git que materializa el cierre | tree id de Git | Git (`git rev-parse <commit>^{tree}`) |
| **Committed state** | estado del **repositorio** tras el commit atómico; no es status de Plan (CL-5) | tree id del commit | Git |
| **Closed** | condición derivada: `Executed` ∧ governance ∧ ∃ checkpoint ∧ consistencia ∧ evidencia PASS para el estado de cierre | — (predicado) | derivada de los anteriores |

**Relaciones normativas.**

```text
validated state identity  ==  closure state identity        (GC-1: obligatoria)
closure state identity     ≠  commit tree                   (permitido y esperado)
commit tree                 =  materialización del cierre   (hecho de Git)
Closed                      ⊃  consistencia GC-1 + evidencia PASS
```

`A ≠ B` (árbol validado ≠ árbol del commit de cierre) **es esperado**: RFC-75
Mecanismo 7 declara que *el commit de cierre puede incluir governance* (INDEX,
CHANGELOG, ADR, docs). Exigir `A == B` prohibiría lo que la RFC permite
explícitamente. `Closed` **no** requiere `A == B`; requiere la igualdad de
**identidad scoped** de GC-1 y la localizabilidad de la materialización en Git.

### 3. Evidence chain

| Etapa | Dato | Naturaleza | Source of truth | Verificado por |
|---|---|---|---|---|
| input | contenido del repo en el estado S1 | observado | Git | — |
| validation | command-set + resultado | declarado + observado | Nota de ejecución | batería |
| anchor | Scoped Content Identity de S1 | calculado (declarado) | `## Validation anchor` | C-1 |
| checkpoint | commits de cierre, estado validado, identidad del estado de cierre, consistencia | declarado (+ resuelto de Git) | `## Checkpoint / cierre` | C-2 |
| closure | estado de cierre = S1 + registros de gobernanza | **declarado** (identidad = la del anchor) | sección de cierre | C-2 (R2) |
| commit | commit atómico que materializa el cierre | observado | Git | C-2 (R4) |
| closed | condición derivada | derivada | — | C-2 |

**Auto-referencia.** El artifact de cierre modifica el estado que declara. Sin
resolución explícita, la identidad no alcanza punto fijo. Resolución
(implementada como modelo, sin primitiva nueva): el scope declarado se fija
**antes** de escribir los registros de cierre; el estado de cierre se declara con
la identidad del anchor aplicable; el commit se localiza por su mensaje y su
árbol se verifica desde Git. No se introduce identidad, estado ni registry
nuevos.

### 4. Reproduction (patrón F-5)

**Reproducido.** Secuencia mínima sobre el mecanismo previo:

1. estado S con tree `T_S` validado (anchor A1 con State identity `T_S`);
2. checkpoint declara `Estado de cierre (tree id): T_S`;
3. el commit de cierre **materializa S + registros de gobernanza** → tree
   `T_C ≠ T_S`;
4. `closure tree declarado (T_S) ≠ commit tree (T_C)`.

**Con el corpus real (entradas de commit identificadas por mensaje, sin SHA),
C-2 devolvía `VALID`**: `ordered_closing_commits` no encuentra entradas `C<n>`,
`final_tree` es `None`, no hay contradicción, y la correspondencia declarada
`T_S` ↔ anchor `T_S` se satisface. La relación `closure tree == commit tree`
**no se verificaba nunca** en el corpus real: era código alcanzable solo desde
la suite sintética. El caso del Plan 133 **no fue un error documental aislado**:
fue la manifestación de una discrepancia entre el contrato documentado de C-2 y
su comportamiento efectivo.

### 5. Historical analysis (Planes 120, 123–133)

Declaración de closure/commit tree verificada contra `git log` y
`git rev-parse <commit>^{tree}`:

| Plan | Anchor state (A1) | Closure declarado | Commit | Commit tree | Relación | Clasificación |
|---|---|---|---|---|---|---|
| 120 | `27990f3d` | `27990f3d` | `4314d5ee` | `3f51f71e` | closure = validated ≠ commit | **CORRECT** |
| 123 | `a640c483` | `3544804b` (= A2) | `4f85e67b` | `b0e2f795` | closure = A2 ≠ commit | **CORRECT** |
| 124 | `23317bc2` | `23317bc2` | `4cd11ed7` | `086648fb` | closure = validated ≠ commit | **CORRECT** |
| 125 | `063275d9` | `063275d9` | `bbc45a65` | `c710d355` | closure = validated ≠ commit | **CORRECT** |
| 126 | `32658020` | `32658020` | `50771b6c` | `90e9a7ad` | closure = validated ≠ commit | **CORRECT** |
| 127 | `95bee054` | `95bee054` | `a70f1c67` | `d6328c76` | closure = validated ≠ commit | **CORRECT** |
| 128 | `ef2278ce` | `ef2278ce` | `0bc4e676` | `f6e16b09` | closure = validated ≠ commit | **CORRECT** |
| 129 | `e6b4723b` | `e6b4723b` | `4608176` (contenido) / `b888ad9` (cierre) | `a2b4cd16` / `8bd65b00` | closure = validated ≠ ambos commits | **CORRECT** |
| 130 | `ddc29a98` | `ddc29a98` | `b888ad9` | `8bd65b00` | closure = validated ≠ commit | **CORRECT** |
| 131 | `05a1362b` | `05a1362b` | `65a1113` (contenido) | — | closure = validated | **CORRECT** |
| 132 | `ad5fe5e6` | `ad5fe5e6` | `35fef6d9` | `7af222e0` | closure = validated ≠ commit | **CORRECT** |
| 133 | `02dcd35f` | `02dcd35f` | `c7ac44e` + `b007214` | `d17503fe` / `3ba73df7` | closure = validated ≠ commit | **CORRECT** |

**Ningún Plan histórico requiere corrección.** Los doce declaran como estado de
cierre el estado validado (o el A2 aplicable, en el 123), que es exactamente lo
que GC-1 exige. El Plan 133 ya había sido precisado por `<PLAN-133>:C-4`. El Plan
116 (`GAP` preexistente por ambigüedad de revalidaciones múltiples) permanece
`AMBIGUOUS`: es BOUNDARY de revisión humana, ajeno a este Change.

### 6. Findings

Ver `### Findings` más abajo: `<PLAN-134>:F-1` (defecto de contrato de C-2),
`<PLAN-134>:F-2` (ambiguëdad terminológica «closure tree»), `<PLAN-134>:F-3`
(código muerto de la rama de commit final) y `<PLAN-134>:F-4` (auto-referencia no
resuelta normativamente).

### 7. Resultado

**Resultado A — defecto confirmado y corregido.** El defecto **no** está en la
semántica de `Committed`/`Closed`/`Released` (que se preservan), ni en los Planes
históricos (todos correctos), ni en C-1/C-3 (`NOT_REQUIRED`). Está en (a) la
ausencia de un modelo normativo que distinga estado de cierre, grafo de commit y
árbol material; (b) el contrato documentado de C-2, que declaraba la relación
equivocada; y (c) el formato del registro de cierre, que usaba «tree id» para un
concepto que no es un árbol de commit. La corrección es de modelo, de contrato y
de formato; no cambia `Closed`, no agrega estados ni identidades.

## Validation anchor

*Registrado al validar (VC-1).*

- **Declared scope:** el Change de integridad de la evidencia de cierre, 10 paths
  repo-relative: `.agents/policies/lifecycle-checkers.md`,
  `.agents/policies/validation-closure.md`,
  `.agents/workflows/change-lifecycle.md`, `CHANGELOG.md`,
  `docs/CONVENTIONS.md`,
  `docs/plans/134-closure-evidence-integrity.md`, `docs/plans/INDEX.md`,
  `docs/plans/_TEMPLATE.md`, `tests/test_check_lifecycle_checkpoint.py`,
  `tools/check_lifecycle_checkpoint.py`. Total 10 paths.
- **Validation command-set:** los seis checkers canónicos, los gates C-1/C-2/C-3
  y las dos suites de test afectadas:
  `python tools/check_protocol_invariants.py --payload protocol .`,
  `python tools/check_plan_citations.py`, `python tools/check_plan_structure.py`,
  `python tools/check_taxonomy_coherence.py`,
  `python tools/check_session_artifacts.py`, `python tools/check_version_state.py`,
  `python tools/check_lifecycle_anchor.py`,
  `python tools/check_lifecycle_checkpoint.py`,
  `python tools/check_lifecycle_lineage.py`,
  `python -m pytest tests/test_check_lifecycle_checkpoint.py -q`,
  `python -m pytest tests/ -q`.
- **Effective inputs (repo content):** el árbol completo para los seis checkers
  canónicos y la suite completa; el corpus de planes numerados para C-1/C-2/C-3;
  el propio checker para la suite de C-2.
- **Observed dependencies:** `tools/check_lifecycle_checkpoint.py` (sujeto de la
  corrección), `tests/test_check_lifecycle_checkpoint.py` (regresiones),
  `docs/plans/*.md` (corpus del dogfooding real), `.agents/policies/*` y
  `docs/*.md` (destinos de cita), `.project/**`
  (`check_session_artifacts`), `protocol/.agents/**` y todas las citas
  `ruta:sección` (`check_protocol_invariants`, `check_plan_citations`).
- **Environmental factors:** Windows/PowerShell 7, `python` 3.13,
  `core.autocrlf=true` con index canónico LF; estado Git `dev` al inicio en
  `b0072145f2d6d3d4a065e439a27d631ed68ad28b` con working tree limpio; sin red.
  No se declara GAP ambiental: este Change **sí** toca `tools/` y `tests/`, por lo
  que la pierna `python -m pytest tests/` es parte obligatoria del command-set y
  se ejecutó completa.
- **Scoped Content Identity:**
  - **State identity:** `e415e03e2587986a5e866dd3ac3631c3895c4f02` (tree id del índice staged del estado validado, con los 10 paths y los registros de cierre de este artifact).
  - **Delta scoped identity:** `7a4a18b1a87e2a561f7535941711920bcfd40ec92b30bc8b83bd7c5ae7823b47` (sha256 `scoped-v1` sobre los 10 paths, en orden lexicográfico, en ese mismo estado).
  - Alcance declarado reconstruible desde este artifact: los 10 paths listados
    arriba, en orden lexicográfico.
  - **Aplicación del modelo de este Change:** el alcance se fijó **antes** de
    escribir los registros de cierre; el estado de cierre se declara abajo con
    esta misma identidad, y el árbol material del commit de cierre **no** se usa
    como identidad (se registra como hecho de Git cuando el commit exista).
- **Validity / stale:** vigente.

*Resultado real de la ejecución:* verification-01
(`check_protocol_invariants --payload protocol .`): PASS (exit 0, «215 files
checked, 10256 references verified»); verification-02 (`check_plan_citations`):
PASS (exit 0, «All citations resolve»); verification-03 (`check_plan_structure`):
PASS (exit 0, «All numbered documents conform»); verification-04
(`check_taxonomy_coherence`): PASS (exit 0); verification-05
(`check_session_artifacts`): PASS (exit 0); verification-06
(`check_version_state`): PASS (exit 0, con los warnings de tags esperados en
`dev`); verification-07 (C-1 `check_lifecycle_anchor`): `ANOMALY=0`, `GAP=0`;
verification-08 (C-2 `check_lifecycle_checkpoint`): `ANOMALY=0` sobre 134 planes;
verification-09 (C-3 `check_lifecycle_lineage`): `VALID` para este artifact,
`ANOMALY=0`; verification-10
(`pytest tests/test_check_lifecycle_checkpoint.py -q`): **32 passed**;
verification-11 (`pytest tests/ -q`): **836 passed, 0 failed**. Verificación
factual de la reproducción: la rama «declared closure tree differs from the tree
of the final closing commit» era inalcanzable en el corpus (ninguna entrada
«Commits de cierre» de los Planes 120–133 embebe SHA); con el contrato corregido
la divergencia produce `GAP` advisory y R2 sigue produciendo `ANOMALY`.

## Checkpoint / cierre

*Registrado al cerrar (GC-1).*

- **Commits de cierre:** el commit atómico de este Change en `dev`, acción de
  repositorio del mantenedor:
  `fix(dev): correct closure evidence integrity and the C-2 contract (plan 134)`.
  Su SHA se identifica por el mensaje (el artifact no puede embeber su propio SHA
  sin ampliar el scope después de validar); verificable con `git log`.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity
  `e415e03e2587986a5e866dd3ac3631c3895c4f02`, delta scoped identity
  `7a4a18b1a87e2a561f7535941711920bcfd40ec92b30bc8b83bd7c5ae7823b47`.
- **Estado de cierre (identidad):** `e415e03e2587986a5e866dd3ac3631c3895c4f02`
  (state identity) + delta scoped identity
  `7a4a18b1a87e2a561f7535941711920bcfd40ec92b30bc8b83bd7c5ae7823b47`
  — la identidad del estado validado por A1 sobre el scope declarado (10 paths),
  es decir el estado que este checkpoint **certifica** por correspondencia GC-1.
  Es una identidad de **contenido scoped**, no el árbol de un commit.
- **Árbol material del commit de cierre (tree id):** no se transcribe como
  identidad. El commit de cierre materializa el estado validado más los registros
  de gobernanza que este artifact escribe al cerrar, de modo que su árbol difiere
  legítimamente del declarado (RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo
  7 — Git Checkpoints`); su valor correcto es el que resuelva
  `git rev-parse HEAD^{tree}` sobre el commit de cierre. Esta es exactamente la
  relación que este Change documenta y **no** considera una violación de GC-1.
- **Consistencia checkpoint↔anchor:** **PASS** — el estado de cierre declarado
  tiene la identidad de contenido scoped del anchor aplicable A1 (mismos 10 paths,
  misma delta scoped identity y misma state identity), y los factores ambientales
  declarados no cambiaron; verificado con C-2, que clasificó este artifact
  conforme a GC-1 sobre el árbol validado.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 134 (fila, serie
  Sexagésima sexta y encabezado de estado); `CHANGELOG.md` `[Unreleased]` registra
  el par (plan 134); el modelo del estado de cierre queda en
  `docs/CONVENTIONS.md`, su semántica operativa en
  `.agents/policies/validation-closure.md:5`, el workflow en
  `.agents/workflows/change-lifecycle.md:8`, el contrato de C-2 en
  `.agents/policies/lifecycle-checkers.md` y el template en
  `docs/plans/_TEMPLATE.md`; findings `<PLAN-134>:F-1`…`F-4` (`resolved`) y
  correcciones `<PLAN-134>:C-1`/`<PLAN-134>:C-2` registrados; C-1 y C-3
  declarados `NOT_REQUIRED`; `**Status:** Executed`.
- **Documentation impact:** **REQUIRED** — documentos afectados y actualizados
  dentro de este Change: `docs/CONVENTIONS.md` (aspecto: no existía modelo
  normativo que distinguiera estado validado, estado de cierre y árbol material
  del commit; la regla GC-1 se enunciaba solo como «identidad scoped =
  identidad del anchor» sin definir el estado de cierre ni resolver la
  auto-referencia; actualización: subsección `### Change Lifecycle — Estado de
  cierre, grafo de commit y árbol material (modelo, Plan 134)`; evidencia: el
  documento en el árbol validado, `check_plan_citations` PASS y
  `check_plan_structure` PASS), `.agents/policies/validation-closure.md`
  (aspecto: el registro de cierre pedía «Closure state (Git tree id)»,
  colapsando identidad de contenido scoped y árbol de commit; actualización: §5
  con los tres conceptos separados, el campo de árbol material, la resolución de
  la auto-referencia y el contrato R1–R4 de C-2),
  `.agents/workflows/change-lifecycle.md` (aspecto: §8 pedía «closure state (Git
  **tree id**)»; actualización: §8 con los tres conceptos, el scope fijo antes de
  los registros y la verificación de la materialización),
  `.agents/policies/lifecycle-checkers.md` (aspecto: el contrato documentado de
  C-2 declaraba «closure state = tree id del commit de cierre final», relación
  que contradice RFC-75 Mecanismo 7; actualización: contrato R1–R4 y
  `NOT_REQUIRED` explícito para C-1/C-3),
  `docs/plans/_TEMPLATE.md` (aspecto: el campo «Estado de cierre (tree id)»
  nombraba mal el dato; actualización: estado de cierre como identidad (delta +
  state identity) y campo separado para el árbol material), `CHANGELOG.md`
  (aspecto: par del plan 134; actualización: ítem `[Unreleased]`) y
  `docs/plans/INDEX.md` (aspecto: registro del Change; actualización: fila, serie
  y encabezado). `docs/VERSIONING.md` §9 no se toca (sin release). `README.md`,
  `AGENTS.md`, `.agents/AGENTS.md`, `ROADMAP.md` y `docs/AGENTS.md` **no**
  requieren cambio: ninguna instrucción activa de esas capas cambia (el modelo
  vive donde ya viven los mecanismos del lifecycle, y su única referencia de
  descubrimiento es la ruta a `.agents/`, que no cambia). No se actualiza ningún
  documento histórico (RFC-46). Sin `VERSION` bump ni tag.
- **Roadmap impact:** **NOT_REQUIRED** — el Change no modifica el mapa operativo
  del trabajo futuro: no crea, completa, cancela, reclasifica, re-prioriza ni
  re-dependencia ningún ítem, no descubre trabajo nuevo y no mueve ningún ítem
  entre candidato / activo / bloqueado. `ROADMAP.md` no se toca y su mapa
  (trabajo activo/dogfood, pendientes que requieren autorización, candidatos)
  sigue siendo factual: la corrección es de contrato interno del lifecycle y de
  precisión de la evidencia de cierre, sin efecto sobre el backlog. La única
  consecuencia operativa (adoptar el registro del SHA del commit de cierre) queda
  **escalada como pending decision** en este artifact, no convertida en trabajo
  del mapa.
- **Condición derivada:** **`Closed`** (docs-only + tooling DEV, sin release) —
  `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS.
  Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-134>:F-1` — estado: `resolved`; severidad: `high`; observación: el
  contrato documentado de C-2 declaraba que el **closure state es el tree id del
  commit de cierre final** («Closure state = Git **tree id** of the final closing
  commit», `.agents/policies/lifecycle-checkers.md`) y contradecía la semántica
  normativa de GC-1 (identidad scoped del estado de cierre = identidad del anchor
  aplicable) y la autorización explícita de RFC-75 Mecanismo 7 («el commit de
  cierre puede incluir governance»); evidencia original: `.agents/policies/
  lifecycle-checkers.md` §C-2, docstring de `tools/check_lifecycle_checkpoint.py`
  («Closure state is the tree of the **final** closing commit … or the declared
  closure tree»), `docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git
  Checkpoints` y ADR-15 CL-3; estado Git observado: `dev` @ `b007214`; provenance
  original: investigación del Change; resolución: **corregido** por
  `<PLAN-134>:C-1`.
- `<PLAN-134>:F-2` — estado: `resolved`; severidad: `medium`; observación: el
  término **«closure tree»** y la etiqueta «Estado de cierre (tree id)» eran
  ambiguos: nombraban un *tree id* de Git un concepto (el estado que el checkpoint
  certifica) cuya identidad es una **Scoped Content Identity**; el corpus
  resolvía la ambigüedad declarando el tree id del estado validado, con lo cual
  la etiqueta describía mal el dato; evidencia original: los 12 registros de
  cierre listados en §5 y el `_TEMPLATE.md`; estado Git observado: `dev` @
  `b007214`; provenance original: investigación del Change; resolución:
  **corregido** por `<PLAN-134>:C-1` (modelo normativo + template que separa
  estado de cierre y árbol material).
- `<PLAN-134>:F-3` — estado: `resolved`; severidad: `medium`; observación: la
  rama de C-2 que exige «declared closure tree == tree of the final closing
  commit» era **inalcanzable en el corpus real**: las entradas de commits de
  cierre de los Planes 120–133 declaran el commit **por mensaje y sin SHA**
  (convención anti-auto-referencia), de modo que `ordered_closing_commits`
  devuelve una lista vacía, `final_tree` es `None` y la contradicción nunca se
  evaluaba; la relación que realmente aplicaba en todo el corpus era la
  correspondencia con el anchor, documentada solo como fallback; evidencia
  original: `tools/check_lifecycle_checkpoint.py` (función
  `ordered_closing_commits`) +
  extracción de SHAs embebidos en las entradas «Commits de cierre» de los Planes
  129–133 → ninguna coincide; estado Git observado: `dev` @ `b007214`; provenance
  original: investigación del Change; resolución: **corregido** por
  `<PLAN-134>:C-1` y `<PLAN-134>:C-2` (contrato R1–R4 explícito y verificación
  efectiva de la materialización).
- `<PLAN-134>:F-4` — estado: `resolved`; severidad: `medium`; observación: la
  **auto-referencia** del artifact de cierre (el registro contiene la identidad
  del estado que él mismo modifica) no estaba resuelta normativamente, y admitía
  dos lecturas incompatibles: (a) el estado de cierre es `S + registros de
  cierre`, lo que hace la identidad no computable sin punto fijo, o (b) el estado
  validado, lo que difiere del commit material; evidencia original:
  `<PLAN-133>:F-5` / `<PLAN-133>:C-4` y los 12 registros históricos; estado Git
  observado: `dev` @ `b007214`; provenance original: consigna del Change y
  `<PLAN-133>:F-5`; resolución: **corregido** por `<PLAN-134>:C-1` (regla
  declarativa: scope fijo antes de escribir los registros; identidad del estado
  de cierre = par delta + state identity del anchor aplicable; commit localizado
  por mensaje).

### Correcciones

- `<PLAN-134>:C-1` — refs origen: `<PLAN-134>:F-1`, `<PLAN-134>:F-2`,
  `<PLAN-134>:F-4`; alcance de revalidación: — (corrección documental pura: no
  cambia contenido scoped validado de ningún artefacto de gobernanza; la
  evidencia de este Change es el `## Validation anchor` y la verificación
  declarada abajo); documentos: `docs/CONVENTIONS.md`,
  `.agents/policies/validation-closure.md`,
  `.agents/workflows/change-lifecycle.md`, `.agents/policies/lifecycle-checkers.md`,
  `docs/plans/_TEMPLATE.md`; evidencia (Git/estado): modelo normativo nuevo
  (`### Change Lifecycle — Estado de cierre, grafo de commit y árbol material
  (modelo, Plan 134)`), §5 de la policy con los tres conceptos separados y el
  contrato R1–R4, §8 del workflow y el template con los campos separados;
  `check_plan_citations` PASS y `check_plan_structure` PASS sobre el árbol
  validado. No cambia `Committed`/`Closed`/`Released` ni la condición derivada
  `Closed`; no crea estado, entidad, identidad ni registry.
- `<PLAN-134>:C-2` — refs origen: `<PLAN-134>:F-1`, `<PLAN-134>:F-3`; alcance de
  revalidación: — (regresión mecánica: la suite de C-2 cubre el contrato
  corregido y el corpus real se re-verifica con C-2 sobre el árbol validado;
  evidencia en el `## Checkpoint / cierre`);
  documentos: `tools/check_lifecycle_checkpoint.py`,
  `tests/test_check_lifecycle_checkpoint.py`; evidencia (Git/estado): el estado de  cierre declarado es la identidad declarada (el tree del commit final queda como
  fallback y como materialización verificada por R4); la divergencia
  estado-de-cierre ↔ árbol-material pasa a **GAP advisory con requisito de
  atribución** en lugar de ANOMALY, preservando R2 (correspondencia con el anchor)
  como el nivel ANOMALY; 2 regresiones de la suite que codificaban la semántica
  superada fueron reemplazadas y se agregaron 2 regresiones nuevas del contrato
  (divergencia = GAP, declarar el árbol material como estado de cierre = ANOMALY);
  `python -m pytest tests/test_check_lifecycle_checkpoint.py -q` → 32 passed;
  C-2 sobre el corpus real → 38 `VALID`, 0 `ANOMALY` (sin cambios respecto del
  baseline salvo los `GAP` esperados de planes en curso y el preexistente del
  Plan 116).

### Pending decisions

- `<PLAN-134>` — decisión: si el corpus del Change Lifecycle debe adoptar la
  práctica de **embeber el SHA del commit de cierre** (o su tree id junto al SHA)
  en el registro de cierre una vez que el commit existe, de modo que R4 tenga
  datos y la materialización quede verificada en todos los Planes y no solo en
  aquellos que declaren locators; blocking: no; owner: mantenedor; escalación:
  cambio de práctica del Change Lifecycle (afecta a todos los Planes futuros);
  resolución: pendiente; evidencia: `<PLAN-134>:F-3` y el contrato R4.

## Riesgos

- **Corregir C-2 para que pase, en lugar de corregir el modelo.** Mitigación: el contrato se deriva de ADR-15/RFC-75 §7 antes de tocar el checker, y cualquier cambio de relación se acompaña de una regresión que falla bajo la semántica anterior.
- **Declarar defectuosos doce planes sin evidencia.** Mitigación: la clasificación se decide por la semántica normativa (ADR-15 CL-3 + RFC-75 §7), no por conveniencia; se verifica plan por plan.
- **Introducir una primitiva de identidad nueva.** Mitigación: el modelo se expresa con los conceptos existentes (Scoped Content Identity, tree id, locator); no se crea entidad, estado ni registry.
- **Romper el corpus histórico de C-2.** Mitigación: la suite debe seguir clasificando los Planes 96–99 y 120–133 como hoy; se corre la suite completa y el dogfooding.

## Trazabilidad

`<PLAN-133>:F-5` (closure tree declarado ≠ árbol material del commit) →
`<PLAN-133>:C-4` (corrección local del registro del Plan 133) → **este Change**
(Plan 134: determinación del modelo e integridad de la evidencia de cierre).

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `b0072145f2d6d3d4a065e439a27d631ed68ad28b`,
working tree limpio al inicio.*

**Resultado A — defecto confirmado y corregido.** La investigación determinó que
la semántica de `Committed`/`Closed`/`Released` y de la condición derivada
`Closed` **es correcta** y se preserva; los 12 Planes históricos examinados
(120, 123–133) **declaran correctamente** el estado de cierre como el estado
validado, que es lo que GC-1 exige; C-1 y C-3 no leen el estado de cierre y se
declararon `NOT_REQUIRED`. Los defectos reales fueron otros: el **contrato
documentado** de C-2 declaraba una relación (`closure state = tree del commit de
cierre final`) que contradice RFC-75 Mecanismo 7 y que además era **código
inalcanzable** en el corpus real, porque las entradas «Commits de cierre» de los
Planes 120–133 identifican el commit por mensaje y sin SHA; el **formato** del
registro usaba «tree id» para un concepto cuya identidad es una Scoped Content
Identity; y el **modelo** no distinguía estado de cierre, grafo de commit y árbol
material ni resolvía la auto-referencia.

**Qué se corrigió.** Modelo normativo nuevo en `docs/CONVENTIONS.md` con los tres
conceptos, la regla de que `A ≠ B` es esperado (RFC-75 Mecanismo 7 autoriza
governance en el commit de cierre) y la resolución declarativa de la
auto-referencia (scope fijo antes de los registros; identidad del estado de cierre
= par delta + state identity del anchor aplicable; commit localizado por mensaje).
§5 de `validation-closure.md` con el contrato **R1–R4** de C-2 y el campo de árbol
material. §8 del workflow y `_TEMPLATE.md` con los tres conceptos separados.
`lifecycle-checkers.md` con el contrato de C-2 corregido. Y el checker: el estado
de cierre declarado es la identidad declarada (el árbol del commit final queda
como fallback para registros sin identidad declarada), la divergencia
estado-de-cierre ↔ árbol material es **GAP advisory con requisito de atribución**
—no ANOMALY—, y R2 (correspondencia con un anchor registrado) conserva el nivel
ANOMALY. Dos regresiones de la suite que codificaban la semántica superada fueron
reemplazadas y se añadieron dos regresiones del contrato corregido.

**Límite residual explícito.** R4 solo puede verificar la materialización cuando
el registro declara un locator resoluble; hoy el corpus no lo hace, así que en la
práctica R4 permanece sin datos para los Planes históricos. A diferencia de antes,
esto ya **no** es una relación mal definida: el contrato declara exactamente qué
se verifica y qué no, y la materialización se verifica en cuanto el registro
declare el SHA. Adoptar esa práctica queda como pending decision de este artifact
(owner: mantenedor), porque cambia el procedimiento de todos los Planes futuros.

**No realizado (por diseño).** Sin cambios en `Committed`, `Closed`, `Released`
ni en la condición derivada `Closed`; sin estado, entidad, identity primitive,
lifecycle, registry, tracker ni clasificación de checker nuevos; sin corregir
ningún Plan histórico; sin reabrir Plan 121/122/123/132/133, Placement Contract,
Prompt Cache, Jury Trial, C-2/CI como incidente de infraestructura, ni pytest
isolation; sin D01 Mechanical Checker (sigue siendo el próximo dogfood); sin
`protocol/.agents/`, `dist/`, CI, `VERSION` ni tags; sin push, merge, release ni
promoción.
