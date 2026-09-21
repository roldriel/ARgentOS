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
- **Validity / stale:** A1 (arriba) valida el estado del commit `f6884c5`, que
  incluía los registros de cierre originales de este artifact. **A1 es `stale`
  respecto del estado corregido** por el cierre formal (2026-09-15): las
  correcciones `<PLAN-134>:C-3`/`<PLAN-134>:C-4` modifican este artifact, que
  pertenece al scope declarado. Se registra la **revalidación A2** en este mismo
  anchor (abajo); A1 conserva su significado histórico y no se muta.
- **Revalidación A2 (estado corregido, 2026-09-15).** Referencia a A1: la cadena
  es histórica (`A1 → A2`), nunca una mutación de A1. Motivo: los registros de
  cierre del Change «Close Closure Evidence Integrity» (F-5/C-3 y F-6/C-4)
  modifican este artifact, que forma parte del scope declarado en A1; A1 pasa a
  `stale` para el estado corregido (CL-2). Command-set: idéntico al de A1.
  Cambios de factores ambientales: ninguno. Resultado: **PASS** (ver
  `## Nota de ejecución`, «Cierre formal y verificación de baseline»).
  - **State identity (A2, estado revalidado):** `751d7c7d07652082397a33aa737885fe219a8070` (tree id del índice staged del scope declarado con los 10 paths, incluidos los registros de cierre corregidos).
  - **Delta scoped identity (A2):** `b580f8940b0ec573a05ce2226b34e7b0c0cfd1516581ec30397e666020105c7f` (sha256 `scoped-v1` sobre los 10 paths, en orden lexicográfico).
  - **Límite declarado:** el delta declarado se midió antes de escribir este
    enunciado, por lo que no se auto-referencia; el árbol material del commit que
    materializa A2 se resuelve con `git rev-parse <commit>^{tree}` en lugar de
    transcribirse aquí. Los checkers no verifican mecánicamente este resultado:
    es evidencia textual declarada.

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
  `fix(dev): correct closure evidence integrity and the C-2 contract (plan 134)`
  (`f6884c5`). Su SHA se identifica por el mensaje (el artifact no puede embeber
  su propio SHA sin ampliar el scope después de validar); verificable con
  `git log`. El cierre formal posterior (`<PLAN-134>:C-3`/`<PLAN-134>:C-4`) se
  materializa en su propio commit atómico, identificado igualmente por su
  mensaje.
- **Estado validado (ref al Validation anchor):** **A2** (revalidación sobre el
  estado corregido, arriba), state identity
  `751d7c7d07652082397a33aa737885fe219a8070`, delta scoped identity
  `b580f8940b0ec573a05ce2226b34e7b0c0cfd1516581ec30397e666020105c7f`. A1
  (`e415e03e…` / `7a4a18b1…`) conserva su significado histórico como la
  validación del estado del commit `f6884c5`.
- **Estado de cierre (identidad):** `751d7c7d07652082397a33aa737885fe219a8070`
  (state identity) + delta scoped identity
  `b580f8940b0ec573a05ce2226b34e7b0c0cfd1516581ec30397e666020105c7f`
  — la identidad del estado validado por A2 sobre el scope declarado (10 paths),
  es decir el estado que este checkpoint **certifica** por correspondencia GC-1.
  Es una identidad de **contenido scoped**, no el árbol de un commit.
- **Árbol material del commit de cierre (tree id):** no se transcribe como
  identidad. El commit de cierre materializa el estado validado más los registros
  de gobernanza que este artifact escribe al cerrar, de modo que su árbol difiere
  legítimamente del declarado (RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo
  7 — Git Checkpoints`); su valor correcto es el que resuelva
  `git rev-parse <commit>^{tree}` sobre el commit de cierre. Esta es exactamente la
  relación que este Change documenta y **no** considera una violación de GC-1.
- **Consistencia checkpoint↔anchor:** **PASS** — el estado de cierre declarado
  tiene la identidad de contenido scoped del anchor aplicable **A2** (mismos 10
  paths, misma delta scoped identity y misma state identity), y los factores
  ambientales declarados no cambiaron; verificado con C-2, que clasificó este
  artifact conforme a GC-1 sobre el árbol validado.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 134 (fila, serie
  Sexagésima sexta y encabezado de estado); `CHANGELOG.md` `[Unreleased]` registra
  el par (plan 134); el modelo del estado de cierre queda en
  `docs/CONVENTIONS.md`, su semántica operativa en
  `.agents/policies/validation-closure.md:5`, el workflow en
  `.agents/workflows/change-lifecycle.md:8`, el contrato de C-2 en
  `.agents/policies/lifecycle-checkers.md` y el template en
  `docs/plans/_TEMPLATE.md`; findings `<PLAN-134>:F-1`…`F-4` (`resolved`) y
  correcciones `<PLAN-134>:C-1`/`<PLAN-134>:C-2` registrados; C-1 y C-3
  declarados `NOT_REQUIRED`; `**Status:** Executed`. **Cierre formal
  (2026-09-15, post-commit `f6884c5`):** se agrega `<PLAN-134>:F-5` (`resolved`)
  y su corrección `<PLAN-134>:C-3` (enunciado término por término de las seis
  condiciones derivadas) y se registra la verificación de cierre del Change
  «Close Closure Evidence Integrity»; ningún otro artifact se modifica.
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
- **Condiciones derivadas, una por una** (cada una reconstruible de este artifact
  y de Git; ninguna se confunde con otra):

  | Condición | Valor | Evidencia en este artifact |
  |---|---|---|
  | `Verified` | **YES** | `## Validation anchor`, «Resultado real de la ejecución»: seis checkers canónicos + C-1/C-2/C-3 PASS, `pytest tests/test_check_lifecycle_checkpoint.py` 32 passed, `pytest tests/` 837 passed |
  | `Executed` | **YES** | `**Status:** Executed`; criterios de salida cumplidos |
  | `Committed` | **YES** | commit atómico `fix(dev): correct closure evidence integrity and the C-2 contract (plan 134)` (`f6884c5`) en `dev` |
  | `Closed` | **YES** | `Executed` ∧ governance aplicada ∧ ∃ checkpoint ∧ consistencia checkpoint↔anchor **PASS** ∧ evidencia de validación PASS para el estado de cierre |
  | `Promoted` | **NO** | sin merge `dev` → `master`; `origin/dev` en `4aa261774c034eba3bb6f4e51810513ce9e25933` |
  | `Released` | **NO** | sin tag, sin release, sin regeneración de `dist` |

  La cadena de implicación `Verified ⊆ Executed ⊆ Closed ⊆ Promoted ⊆ Released`
  se respeta: las cuatro primeras son verdaderas, las dos últimas falsas, y
  `Closed ≠ Released`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-134>:F-6` — estado: `resolved`; severidad: `medium`; observación:
  verificación final de cierre — el estado validado declarado por A1
  (`e415e03e2587986a5e866dd3ac3631c3895c4f02`, delta `7a4a18b1…`) es un objeto
  git **válido y presente en la base de objetos, pero nunca fue árbol de ningún
  commit** (`git log --all --format='%H %T'` no lo contiene; el árbol del commit
  de cierre `f6884c5` es `d51f8edb…`), y la delta declarada no es reproducible
  desde el estado commiteado (calculada con la misma serialización `scoped-v1`
  sobre los blobs de `f6884c5` da `d193a4a8…`, distinta). Es decir: la identidad
  declarada identificaba correctamente el *contenido* staged sobre el que se
  corrió la validación, pero **el estado no era reconstruible desde el commit**,
  que es justamente lo que ADR-15 CL-3 exige («un estado Git verificable que
  permita reconstruir el estado efectivamente validado y gobernado»), y es la
  misma clase de defecto que `<PLAN-133>:F-5`; evidencia original: `git cat-file
  -t e415e03e…` → `tree`; `git rev-parse f6884c5^{tree}` → `d51f8edb…`; `git log
  --all` sin `e415e03e`; recálculo de la identidad scoped sobre los blobs de
  `f6884c5` → `d193a4a8…`; estado Git observado: `dev` @
  `f6884c53790b482e169df27dd7769463932f0479`, working tree limpio; provenance
  original: Change de cierre «Close Closure Evidence Integrity» (2026-09-15);
  resolución: **corregido** por `<PLAN-134>:C-4` — A1 se marca `stale` para el
  estado corregido (conservando su significado histórico), se agrega la
  revalidación **A2** sobre el estado reconstruible y el checkpoint certifica el
  estado de A2. Semántica, R4, C-2, Plan 116 e historia: sin cambios.
- `<PLAN-134>:F-5` — estado: `resolved`; severidad: `low`; observación: verificación
  final de cierre (post-commit `f6884c5`) — el registro de cierre de este artifact
  declaraba la condición derivada `Closed` y enumeraba «sin tag, sin push, sin
  merge, sin promoción», pero **no** enunciaba una por una las condiciones
  derivadas (`Verified`, `Executed`, `Committed`, `Closed`, `Promoted`,
  `Released`): `Promoted` no aparecía nombrado en ningún punto del registro y
  `Released` sólo de forma incidental, de modo que el estado de cierre no era
  reconstruible término por término desde el artifact sin inferencia; evidencia
  original: búsqueda de los seis términos en este mismo artifact (`Promoted` → 0
  ocurrencias; `Verified` → 1, ajena al predicado) y `git rev-parse HEAD` =
  `f6884c53790b482e169df27dd7769463932f0479` con `origin/dev` sin cambios;
  estado Git observado: `dev` @ `f6884c5`, working tree limpio; provenance
  original: Change de cierre «Close Closure Evidence Integrity» (2026-09-15);
  resolución: **corregido** por `<PLAN-134>:C-3` — se agregó la tabla de las seis
  condiciones con su valor y su evidencia, sin cambiar la semántica del modelo,
  sin alterar R4, sin tocar el Plan 116 y sin modificar ningún otro artifact.
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

- `<PLAN-134>:C-4` — refs origen: `<PLAN-134>:F-6` (el estado validado de A1 no
  era reconstruible desde el commit); alcance de revalidación: **A2** (arriba),
  sobre el estado corregido del scope declarado; documento:
  `docs/plans/134-closure-evidence-integrity.md` (secciones `## Validation
  anchor` y `## Checkpoint / cierre`); evidencia (Git/estado): A1 marcado `stale`
  sin mutarlo, A2 registrado con state identity
  `751d7c7d07652082397a33aa737885fe219a8070` y delta `b580f894…`, y el checkpoint
  certificando el estado de A2; los seis checkers canónicos, C-1/C-2/C-3 y la
  suite completa vuelven a pasar sobre el árbol corregido (ver `## Nota de
  ejecución`). No se modificó el modelo semántico, R4, C-2, el Plan 116 ni ningún
  Plan histórico.
- `<PLAN-134>:C-3` — refs origen: `<PLAN-134>:F-5`; alcance de revalidación: —
  (corrección documental pura y acotada al registro de cierre de este artifact:
  no cambia contenido scoped validado de ningún otro artefacto de gobernanza y no
  altera el modelo semántico, R4, C-2, el Plan 116 ni la historia; la verificación
  de este Change es la re-ejecución de los checkers y gates, declarada en la
  `## Nota de ejecución`); documento: `docs/plans/134-closure-evidence-integrity.md`
  (sección `## Checkpoint / cierre`); evidencia (Git/estado): tabla de las seis
  condiciones derivadas con valor y evidencia por condición; los seis checkers
  canónicos, C-1/C-2/C-3 y la suite completa vuelven a pasar sobre el árbol
  corregido (ver `## Nota de ejecución`). Semántica de Plan 134 intacta: la
  corrección agrega el enunciado explícito de las condiciones, no su significado.
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
  resolución: **resuelta** (decisión humana del mantenedor, determinada por el Plan 141 el 2026-09-21): se adopta como **práctica recomendada**, no obligatoria, que es exactamente lo que la regla vigente ya declara (`.agents/policies/validation-closure.md` §5: embeber el SHA o el tree id una vez que el commit existe «is legal and recommended»); evidencia: `<PLAN-134>:F-3` y el contrato R4.

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

### Cierre formal y verificación de baseline (2026-09-15)

*Change «Close Closure Evidence Integrity». Ejecutado sobre `dev` @
`f6884c53790b482e169df27dd7769463932f0479`, working tree limpio.*

**Verificación del estado, punto por punto** (ninguno se dio por supuesto; los
trece se comprobaron contra el repositorio antes de decidir si hacía falta una
corrección):

| # | Comprobación | Resultado |
|---|---|---|
| 1 | baseline Git | `f6884c5`; rama `dev`; `origin/dev` = `4aa2617` (13 commits locales sin publicar); `protocol/.agents/VERSION` = `11.5.0`; 50 tags, ninguno en `HEAD` |
| 2 | Plan 134 existe | `docs/plans/134-closure-evidence-integrity.md` presente; registrado en `docs/plans/INDEX.md` (fila + Sexagésima sexta serie + encabezado) |
| 3 | cierre/corrección materializados | commit `f6884c5` (`fix(dev): correct closure evidence integrity and the C-2 contract (plan 134)`, 10 archivos); su contenido en `HEAD` |
| 4 | working tree | limpio antes y después de la verificación |
| 5 | C-1 | 134 planes, `VALID=40`, `GAP=0`, `ANOMALY=0` |
| 6 | C-2 | 134 planes, `VALID=39`, `GAP=1`, `ANOMALY=0` |
| 7 | C-3 | 134 planes, `VALID=19`, `GAP=0`, `ANOMALY=0` |
| 8 | seis checkers canónicos | `check_protocol_invariants` (215 files / 10256 refs), `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`: los seis exit 0 |
| 9 | C-2 `ANOMALY=0` | confirmado (el único `GAP` es el esperado) |
| 10 | Plan 116 sigue siendo el `GAP` preexistente | sí: «multiple declared revalidations could correspond to the closure state; ambiguity, evidence insufficient» |
| 11 | cambios pendientes de Plan 134 | ninguno: `git status` limpio; el árbol commiteado contiene todo el contenido del Change |
| 12 | Protocol sin modificaciones | `git diff f6884c5 -- protocol` vacío; `VERSION` 11.5.0 sin cambios |
| 13 | Planes históricos 120–133 | `git diff f6884c5 -- 'docs/plans/1[23][0-9]-*.md'` y el Plan 116: sin cambios |

**Discrepancia de premisa registrada (no es un defecto del repositorio).** La
consigna describía el Change anterior como «corrección posterior ya realizada
según `<PLAN-134>:F-5` / `<PLAN-134>:C-*`» y esperaba `F-1`…`F-5` `resolved` en
este Plan. Verificado el repositorio: `<PLAN-134>:F-5` **no existía**, y el
`F-5`/`C-4` reales pertenecen al **Plan 133** (`<PLAN-133>:F-5`: el closure tree
declarado no coincidía con el árbol material del commit; `<PLAN-133>:C-4`: su
corrección). El Plan 134 tenía `F-1`…`F-4`, todas `resolved`, con `C-1`/`C-2`. La
premisa confundía los namespaces de los dos Planes; el repositorio era y es
coherente, y **no se cambió nada para hacerla coincidir**. El `F-5` del Plan 134
que ahora existe es el hallazgo **nuevo** de esta verificación de cierre
(enunciado explícito de las condiciones derivadas), no un renombrado del de
Plan 133.

**Corrección documental mínima aplicada.** Único defecto real encontrado: el
registro de cierre no enunciaba una por una las seis condiciones derivadas
(`Promoted` no aparecía; `Released` sólo incidentalmente), de modo que el estado
de cierre no era reconstruible término por término sin inferencia. Se agregó la
tabla `Verified/Executed/Committed/Closed/Promoted/Released` con valor y
evidencia, y se registró como `<PLAN-134>:F-5` + `<PLAN-134>:C-3`. **No** se
modificó el modelo semántico, **no** se alteró R4, **no** se tocó el Plan 116,
**no** se agregó el SHA del commit de cierre como requisito del template, **no**
se modificó ningún Plan histórico y **no** se reabrió el Plan 133.

**Pendientes que permanecen pendientes (sin resolver, por diseño).**

1. **R4 / locator del commit de cierre** — `PENDING DECISION`, owner: mantenedor,
   scope: cambio futuro de procedimiento del lifecycle. Registrado en
   `### Pending decisions` de este artifact. Determinará si (a) los Planes
   futuros deben registrar el SHA del cierre, (b) R4 permanece opcional, o (c) se
   adopta otra forma de locator reproducible. **No se eligió ninguna opción** y R4
   **no** se modificó para fabricar evidencia inexistente. Los Planes 120–133 no
   se tocan retroactivamente.
2. **Plan 116 — ambigüedad de revalidaciones múltiples** — `GAP` **preexistente**
   de C-2, boundary que requiere interpretación humana. No se modificó el Plan
   116, no se inventó tie-breaker, no se cambió C-2 para ocultarlo, no se convirtió
   en `ANOMALY` y no se mezcló con R4. Bajo las reglas actuales **no bloquea el
   cierre**: `GAP` es advisory y nunca cambia el exit code.

**Verificación posterior a la corrección.** Los seis checkers canónicos, C-1
(`GAP=0`, `ANOMALY=0`), C-2 (`ANOMALY=0`, `GAP=1` = Plan 116) y C-3 (`GAP=0`,
`ANOMALY=0`) y la suite completa (`python -m pytest tests/ -q`) vuelven a pasar
sobre el árbol corregido, sin que ninguna comprobación se haya ajustado para
obtener verde. C-2 clasifica este artifact `VALID` con anchor aplicable **A2**,
seleccionado por **correspondencia de estado** (no por recencia), que es
exactamente la semántica que el Plan 99/F-1 fijó.

**Hallazgo adicional de la verificación (F-6/C-4).** Al comprobar la
reconstruibilidad del registro se detectó que el estado validado por A1
(`e415e03e…`) era un objeto git válido pero **nunca fue árbol de ningún commit**,
y su delta no era reproducible desde el estado commiteado: identificaba el
contenido staged sobre el que se corrió la validación, pero el estado **no** era
reconstruible desde el commit — justo lo que ADR-15 CL-3 exige, y la misma clase
de defecto que `<PLAN-133>:F-5`. Se corrigió marcando A1 `stale` (sin mutarlo),
registrando la **revalidación A2** sobre el estado reconstruible
(`751d7c7d…` / `b580f894…`) y certificando el estado de A2 en el checkpoint. Es
una limitación heredada del procedimiento vigente —las identidades se midieron
sobre el índice staged— y **no** se ocultó ni se cambió el modelo semántico, R4,
C-2, el Plan 116 ni ningún Plan histórico para resolverla.

**Estado de cierre final (reconstruible desde este artifact).** `Verified = YES`,
`Executed = YES`, `Committed = YES`, `Closed = YES`, `Promoted = NO`,
`Released = NO`. Sin tag, sin release, sin promoción, sin merge, sin push. El
baseline resultante para el próximo trabajo es el commit atómico de este Change
de cierre en `dev`.

