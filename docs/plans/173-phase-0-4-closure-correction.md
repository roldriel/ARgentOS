# Plan 173 — Corrección del cierre inválido de Phase 0.4

**Status:** Executed
**Fecha:** 2026-10-21
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only: `docs/`, `tools/`, `tests/`, `.agents/policies/`; el sub-cambio de tests del payload se ejecuta como Clase C separada, ver §Sub-cambio Clase C)
**Clase:** B (RFC-56: corrección documental y de tooling DEV) + C (sub-cambio tests-only del payload, G-08)
**Change Level:** L2 (`max(coordination=1, scope=3, architectural impact=1, release impact=1, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 — un agente, un Change. *scope*: 3 — `docs/`, `tools/`, `tests/`, `.agents/policies/`, CI y un archivo de tests del payload. *architectural impact*: 1 — añade dos reglas de detección y un checker; no cambia el modelo ni la frontera DEV/Protocol. *release impact*: 1 — el sub-cambio Clase C toca `protocol/.agents/harness/tests/` y queda pendiente de la próxima versión; no hay bump ni tag. *duration/complexity*: 2 — 11 ítems, tres checkers, tres suites, documentos de estado.
**Depende de:** Plan 172 `Closed` (f77cd3f); auditoría adversarial de la clausura (`PHASE_0_4_CLOSURE_NOT_VALID`); ADR-20; ADR-21; RFC-46; RFC-56; RFC-69; RFC-75; `docs/VERSIONING.md` §3/§4.1/§9.
**Origen:** instrucción directa del mantenedor (2026-10-21) que ordena corregir la clausura inválida de Phase 0.4 con el ciclo PLAN → IMPLEMENTACIÓN TEÓRICA → ATAQUE → ESTABILIDAD → IMPLEMENTACIÓN REAL → COMPARACIÓN → VALIDACIÓN → CIERRE.
**Work type:** `GAP`
**Superseded por:** —

## Objetivo

Convertir los 11 ítems del inventario de Phase 0.4 que la auditoría adversarial calificó `MISCLASSIFIED` (9) o `INSUFFICIENT_EVIDENCE` (2) en estados terminales **genuinos**, sin tocar los 22 residual risks que la auditoría declaró genuinos, y corregir la evidencia de cierre de Phase 0.4 que la misma auditoría invalidó.

Resultado buscado:

```text
INVENTORY_TOTAL = 65 · TERMINAL_ITEMS = 65
MISCLASSIFIED = 0 · INSUFFICIENT_EVIDENCE = 0 · REAL_UNCLOSED_DEBT = 0
GENUINE_RESIDUAL_RISKS = 22
```

## Antecedentes

La auditoría adversarial posterior a f77cd3f determinó:

- **Evidencia inválida.** El Anchor/Checkpoint del Plan 172 declaran `8be252… / 785152…`, pero el contenido validado del commit es `58cee8… / c2492e83…`: dos archivos del scope medido cambiaron después de calcular la identidad. Planes 170 y 171 demuestran que la convención del corpus es exacta, no aproximada.
- **9 ítems reclasificados** como `ACCEPTED_RESIDUAL_RISK` aunque una implementación acotada era posible: `P02-G-04`, `P02-G-07`, `P02-G-08`, `P03-FM-05`, `P03-FM-07`, `P03-D-0.3-12`, `P03-D-0.3-13`, `P03-R-03`, `P03-R-04`.
- **2 ítems declarados `RESOLVED` sin evidencia suficiente:** `P03-FM-10`, `DOC-04` (`docs/VERSIONING.md` §9 conserva una nota que afirma que `origin/dist` = `12.1.0` es el payload de los adoptantes).
- **1 sobreafirmación de verificación:** el inventario afirma que `check_plan_structure` implementa un «espejo INDEX↔archivo»; el checker es unidireccional (archivo→INDEX).

## Autoridad

- **Mantenedor (2026-10-21):** instrucción directa que autoriza la corrección de la clausura, el Plan 173, el sub-cambio Clase C de tests del payload y el cierre. Es la autoridad de decisión (`policies/authority.md`); su declaración vive en el primer artefacto del Change (este Plan) y en los mensajes de commit (RFC-75 Mecanismo 1).
- **Clase B (RFC-56):** corrección documental/tooling DEV; plan `Aprobado para ejecución` + batería en verde.
- **Clase C (RFC-56):** sub-cambio **tests-only** del payload (`G-08`). La clasificación está registrada en el cierre de diseño de Priority 0.2 (`docs/working/proposals/PRIORITY_0_2_FINAL_DESIGN_CLOSURE_2026-10-20.md` §14: «G-08 … Clase C (sólo tests)»). No cambia comportamiento, contratos ni resultado de ningún checker; se registra en `[Unreleased]` para la próxima versión. No hay bump de `VERSION` ni tag.
- **No se crea autoridad nueva.** La corrección de la identidad de cierre del Plan 172 se registra **por referencia** (el Plan 172 está cerrado y no se edita, `INV-04`).

## Scope

Rutas que el Plan puede modificar (el propio Plan queda fuera del scope medido, convención anti-auto-referencia):

1. `CHANGELOG.md` — entradas `[Unreleased]` de ambos sub-cambios.
2. `docs/VERSIONING.md` — §4.1 (nuevo checker en la batería) y §9 (nota `dist`/`dev` reconciliada).
3. `docs/INVARIANTS.md` — `## Trabajo pendiente`: G-04/G-07 dejan de ser residuales.
4. `docs/plans/INDEX.md` — registro del Plan 173.
5. `docs/working/proposals/INDEX.md` — registro del documento de teoría.
6. `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md` — reclasificación de los 11 ítems con provenance.
7. `docs/working/proposals/PHASE_0_4_CLOSURE_CORRECTION_THEORY_2026-10-21.md` — implementación teórica, hallazgos y `EXPECTED_FINAL_STATE` (nuevo).
8. `.agents/policies/lifecycle-checkers.md` — contrato R5 de C-2.
9. `tools/check_lifecycle_checkpoint.py` — regla R5 (post-close).
10. `tools/check_plan_structure.py` — regla INDEX→archivo.
11. `tools/check_enforcement_declarations.py` — verificación de `ENF-001`…`ENF-003` (nuevo).
12. `tests/test_check_lifecycle_checkpoint.py` — fixtures R5.
13. `tests/test_check_plan_structure.py` — fixtures INDEX→archivo.
14. `tests/test_check_enforcement_declarations.py` — fixtures del nuevo checker (nuevo).
15. `tests/AGENTS.md` — alta del dogfood anclado del nuevo checker.
16. `.github/workflows/check-protocol.yml` — paso del nuevo checker.
17. `protocol/.agents/harness/tests/test_lifecycle_update_uninstall.py` — tres tests de idempotencia (`G-08`, **commit Clase C separado**, contenido final antes del commit de implementación del Plan 173).

### Sub-cambio Clase C (G-08)

Se ejecuta como **commit directo Clase C** en `dev`, separado y anterior al commit de implementación del Plan 173:

- modifica únicamente `protocol/.agents/harness/tests/test_lifecycle_update_uninstall.py` (tests-only, cero cambio de significado/comportamiento);
- no toca `VERSION`, no crea tag, no toca `dist`;
- se registra en `CHANGELOG.md` `[Unreleased]` (la próxima versión lo consolida);
- deja el payload de `dev` por delante de `dist` hasta la próxima release: `check_dist_sync` rojo en `dev` es el estado esperado por diseño (§9).

## Non-goals

- No iniciar Phase 1.
- No revertir f77cd3f; se preservan sus cambios válidos.
- No convertir ninguno de los 22 residual risks genuinos en trabajo.
- No añadir invariantes, properties, gates conceptuales, estados de lifecycle, registries ni namespaces.
- No modificar `dist`, `VERSION`, `PROTOCOL_VERSION`, tags ni `runtime/`.
- No editar el contenido gobernante de planes, RFC o ADR cerrados (Plan 172 incluido).
- No crear un sistema nuevo de historial, autoridad o enforcement.
- No declarar garantías más fuertes que las implementadas.

## Elementos a corregir

| ID | Grupo | Estado actual | Acción | Estado terminal buscado |
|---|---|---|---|---|
| P03-D-0.3-12 | A | ACCEPTED_RESIDUAL_RISK | R5 de C-2: detecta modificación no commiteada del contenido gobernante de un plan cerrado | IMPLEMENTED (LIMIT declarado) |
| P03-FM-05 | A | ACCEPTED_RESIDUAL_RISK | ídem | IMPLEMENTED |
| P03-R-03 | A | ACCEPTED_RESIDUAL_RISK | ídem | IMPLEMENTED |
| P02-G-07 | B | ACCEPTED_RESIDUAL_RISK | `check_plan_structure`: toda fila del INDEX debe resolver a su archivo | IMPLEMENTED |
| P03-FM-07 | B | ACCEPTED_RESIDUAL_RISK | ídem | IMPLEMENTED |
| P03-D-0.3-13 | B | ACCEPTED_RESIDUAL_RISK | ídem | IMPLEMENTED |
| P03-R-04 | B | ACCEPTED_RESIDUAL_RISK | ídem | IMPLEMENTED |
| P02-G-08 | C | ACCEPTED_RESIDUAL_RISK | 3 tests de idempotencia en la suite del payload (Clase C) | IMPLEMENTED |
| P02-G-04 | D | ACCEPTED_RESIDUAL_RISK | checker de declaraciones `ENF-001`…`ENF-003` en la batería y CI | IMPLEMENTED |
| P03-FM-10 | E | RESOLVED (insuficiente) | reconciliar `docs/VERSIONING.md` §9 | RESOLVED |
| DOC-04 | E | RESOLVED (insuficiente) | ídem | RESOLVED |

## Dependencias

- Auditoría adversarial (hallazgos C1/A1–A4, B1–B7) — origen de los 11 ítems.
- Plan 172 `Closed` en f77cd3f — objeto de la corrección post-close.
- `docs/VERSIONING.md` §3 (Clase C), §4.1 (batería), §9 (snapshot).
- `docs/adr/20-…` (`E1-D1`…`E1-D4`), `docs/adr/21-…` (G-03/G-06).
- `tests/AGENTS.md` (dogfood anclado), `protocol/.agents/harness/INDEX.md` (matriz ENF).

## Tests esperados

- `tests/test_check_lifecycle_checkpoint.py`: R5 positivo/negativo (objetivo editado → ANOMALY; findings apéndice → sin hallazgo; bullet «Commits de cierre» → sin hallazgo; HEAD no cerrado → sin hallazgo; sin cambios → sin hallazgo).
- `tests/test_check_plan_structure.py`: fila de plan sin archivo → violación; fila RFC/ADR sin archivo → violación; corpus válido → sin violación.
- `tests/test_check_enforcement_declarations.py`: mecánico verificado sólo por agente → FAIL; «Verifiable» verificado sólo por humano → FAIL; falta la declaración fail-open → FAIL; matriz válida → PASS; dogfood sobre el payload real → PASS.
- `protocol/.agents/harness/tests/test_lifecycle_update_uninstall.py`: segundo `uninstall` → NOOP y artefactos preservados intactos; `doctor` dos veces → mismo estado y sin efectos; segundo/tercer `recover` → NOOP.
- Suites completas: `pytest tests/`, `pytest protocol/.agents/harness/tests/`.

## Evidencia esperada

- Salidas de los 8 repository checkers + C-1/C-2/C-3 + ambas legs de pytest.
- `git diff --name-only` dentro del scope; cero `protocol/` fuera del sub-cambio Clase C; cero `dist/`, `VERSION`, tags.
- Recomputación del Scoped Content Identity del Plan 173 sobre el estado final: `DECLARED_DELTA == RECOMPUTED_DELTA`, `ANCHOR_STATE == tree del commit de implementación`, `CHECKPOINT_STATE ==` el mismo, y el delta en `HEAD` igual al declarado.
- Recomposición de la identidad de cierre de Phase 0.4: `f77cd3f` tree `58cee8…`; delta del scope del Plan 172 en f77cd3f `c2492e83…`.
- N-9 PASS (CHANGELOG sólo `[Unreleased]`).

## Criterios de cierre

- **AC-1** Los 11 ítems tienen estado terminal genuino y evidencia; `MISCLASSIFIED = 0`, `INSUFFICIENT_EVIDENCE = 0`, `REAL_UNCLOSED_DEBT = 0`.
- **AC-2** Los 22 residual risks genuinos no cambian de estado.
- **AC-3** R5 de C-2 detecta una modificación de contenido gobernante de un plan cerrado en el working tree y no marca apéndices legítimos.
- **AC-4** `check_plan_structure` verifica INDEX→archivo en los tres índices y falla ante una fila sin target.
- **AC-5** El checker ENF verifica `ENF-001`…`ENF-003` con límite declarado, está en la batería y en CI.
- **AC-6** Los tres tests de idempotencia existen y pasan en la suite del payload (Clase C).
- **AC-7** `docs/VERSIONING.md` §9 es internamente coherente con `origin/dist` = `12.3.0` y con el payload de `dev` pendiente de release.
- **AC-8** La identidad del Plan 173 satisface la recomputación exigida (Fase 9).
- **AC-9** La identidad de cierre de Phase 0.4 queda corregida por referencia; el Plan 172 no se edita.
- **AC-10** Batería completa, C-1/C-2/C-3 y ambas legs de tests en verde; N-9 PASS.
- **AC-11** Cero scope leaks, cero violaciones históricas, cero overclaims.

## Criterios negativos

- **N-1** Ningún cambio en `dist/`, `VERSION`, `PROTOCOL_VERSION` ni tags.
- **N-2** Ninguna edición de contenido gobernante de un plan/RFC/ADR cerrado (Plan 172 incluido).
- **N-3** Ningún invariante, property, gate conceptual, estado, registry ni namespace nuevo.
- **N-4** Ningún residual risk genuino convertido en trabajo.
- **N-5** Ningún riesgo aceptado sin acto de autoridad.
- **N-6** Ningún `git add -A`; no se commitean `.project/` ni los untracked del usuario.
- **N-7** Ningún tag, release ni promoción a `master` (el sub-cambio Clase C deja la release pendiente).
- **N-8** Ninguna garantía declarada por encima de la evidencia (LIMIT explícito en cada regla).

## Riesgos

1. **Repetir la falla de identidad del Plan 172.** Mitigación: cómputo al final, gate de recomputación, commit de cierre que sólo toca el Plan (excluido del scope).
2. **Falsos positivos de R5.** Mitigación: región append-only + bullet «Commits de cierre»; fixtures positivos/negativos.
3. **Falsos positivos de INDEX→archivo.** Mitigación: formas de fila específicas por namespace; verificación sobre el corpus real.
4. **ENF checker vacuo o sobreafirmado.** Mitigación: reglas explícitas + LIMIT declarado; fixtures de fallo.
5. **Frontera del payload (Clase C).** Mitigación: commit separado tests-only, sin VERSION/tag/dist; release pendiente declarada; `check_dist_sync` rojo en `dev` por diseño.
6. **Editar el inventario como si fuera historia cerrada.** Mitigación: sección de corrección con estados previos y provenance; el inventario es Working, no un artefacto cerrado.

## Lifecycle

```text
PLAN (este documento)
  → IMPLEMENTACIÓN TEÓRICA (documento de teoría; sin tocar el repositorio)
  → ESTADO HIPOTÉTICO
  → ATAQUE ADVERSARIAL (iteraciones)
  → ESTABILIDAD TEÓRICA
  → IMPLEMENTACIÓN REAL
      ├─ commit Clase C (tests payload, G-08)
      ├─ commit A (implementación del Plan 173)
      └─ commit B (anchor/checkpoint del Plan 173)
  → COMPARACIÓN TEORÍA vs REALIDAD
  → VALIDACIÓN FINAL
  → CIERRE (Closed en dev; Released = NO)
```

`IMPLEMENTED ≠ EXECUTED ≠ VERIFIED ≠ CLOSED ≠ PROMOTED`: cada estado se respalda con su evidencia. El Plan cierra en `dev` con `Closed` derivado; no se promueve mientras el sub-cambio Clase C deje el payload de `dev` sin publicar.

## Criterio de estabilidad de la implementación teórica

La implementación real no comienza hasta que una pasada adversarial completa sobre el estado hipotético produzca:

```text
NEW_PROBLEMS = 0
UNRESOLVED_THEORETICAL_FINDINGS = 0
SCOPE_LEAKS = 0
GOVERNANCE_CONFLICTS = 0
LIFECYCLE_CONFLICTS = 0
EVIDENCE_CONFLICTS = 0
HISTORICAL_CONFLICTS = 0
ENFORCEMENT_OVERCLAIMS = 0
UNEXPECTED_REGRESSIONS = 0
```

El registro de iteraciones, hallazgos y `EXPECTED_FINAL_STATE` vive en `docs/working/proposals/PHASE_0_4_CLOSURE_CORRECTION_THEORY_2026-10-21.md`.

## Verificación

### Comandos exactos

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_invariants_equivalence.py
python tools/check_enforcement_declarations.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
git diff --check
git diff --name-only f77cd3f..HEAD
git status --porcelain=v2 --branch
git diff -U0 HEAD~1..HEAD -- CHANGELOG.md
```

### Recomputación de identidad (condición de cierre)

```bash
python tools/scoped_content_identity.py --root . <scope del Plan 173>
git rev-parse '<commit A>^{tree}'
git diff --quiet HEAD -- <cada ruta del scope>   # debe ser 0 tras el commit A
```

Regla: `DECLARED_DELTA == recomputado en A == recomputado en HEAD`;
`ANCHOR_STATE == CHECKPOINT_STATE == tree(A)`; el commit de cierre (B) sólo agrega
el Plan (excluido del scope medido). Si el delta recomputado difiere, el cierre
se detiene (no se fuerza).

### Guard N-9

El guard de `CHANGELOG.md` es el definido en el Plan 172 (sección **Verificación**, «Guard N-9 de `CHANGELOG.md`»), ejecutado
con baseline `f77cd3f` después de cada commit (Clase C y Plan 173). Sólo se
acepta un hunk dentro de `[Unreleased]` y la secuencia de headings históricos
idéntica.

## Corrección post-close del cierre de Phase 0.4 (Plan 172)

**Registro por referencia (ADR-20 `E1-D4`; RFC-46; `.agents/AGENTS.md` regla 5).** El Plan 172 está `Closed` y **no se edita**. La auditoría adversarial demostró que su Anchor/Checkpoint declaran una identidad que no corresponde al contenido validado:

| Elemento | Valor declarado por el Plan 172 | Valor real del estado de cierre (recomputado) |
|---|---|---|
| State identity | `8be252568b2c77fae5e99f31cbb7132f41920390` | `58cee8cfe3a26098a208ae5fcd7d19838d4b9bf3` (tree de `f77cd3f`) |
| Delta scoped identity (scope de 13 rutas del Plan 172) | `785152b94df1f215aa409b60ba76738ca7abf18287bc2a0cc4f15873a63a16b1` | `c2492e83b42c779ca23e71b2a0da84a453d51b62846c6d8d463305fa4e13be7a` |

**Causa.** La identidad se calculó antes de la validación final y dos archivos del scope medido —`docs/adr/20-closed-artifact-governance-and-execution-records.md` y `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md`— cambiaron después; el árbol declarado y el árbol de `f77cd3f` difieren exactamente en esos dos archivos más el propio Plan (excluido del scope por anti-auto-referencia):

```text
git diff --name-status 8be252… 58cee8…:
  M docs/adr/20-closed-artifact-governance-and-execution-records.md
  M docs/plans/172-phase-0-4-closure-implementation.md        (fuera del scope)
  M docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md
```

**Tratamiento.** Los literales del Plan 172 quedan **superseded por referencia** por este registro; el Plan 172 no se modifica. La identidad de cierre de Phase 0.4 es la de `f77cd3f` (tree y delta de la tabla) y el delta sobre el scope del Plan 172 se recomputa idéntico al declarado en esta corrección. La corrección se apoya en evidencia reproducible (los comandos de `## Verificación`), no en la coincidencia de dos literales entre sí.

**Alcance.** Este registro corrige la evidencia de cierre de Phase 0.4 y reclasifica los 11 ítems del inventario; no reabre el Plan 172 ni reescribe su contenido. Los 22 residual risks genuinos de la auditoría permanecen.

## Validation anchor

**Validation anchor (VC-1).**

- **Declared scope:** las diecisiete rutas de la corrección: `.agents/policies/lifecycle-checkers.md`, `.github/workflows/check-protocol.yml`, `CHANGELOG.md`, `docs/INVARIANTS.md`, `docs/VERSIONING.md`, `docs/plans/INDEX.md`, `docs/working/proposals/INDEX.md`, `docs/working/proposals/PHASE_0_4_CLOSURE_CORRECTION_THEORY_2026-10-21.md`, `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md`, `protocol/.agents/harness/tests/test_lifecycle_update_uninstall.py`, `tests/AGENTS.md`, `tests/test_check_enforcement_declarations.py`, `tests/test_check_lifecycle_checkpoint.py`, `tests/test_check_plan_structure.py`, `tools/check_enforcement_declarations.py`, `tools/check_lifecycle_checkpoint.py` y `tools/check_plan_structure.py`. Este Plan queda **fuera** del scope medido (anti-auto-referencia).
- **Validation command-set:** los ocho repository checkers de `docs/VERSIONING.md` §4.1 (`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `check_invariants_equivalence`, `check_enforcement_declarations`); los tres lifecycle checks C-1/C-2/C-3; las dos legs de `pytest` (`tests/` y `protocol/.agents/harness/tests/`); `git diff --check`; la recomputación del Scoped Content Identity; y el guard N-9.
- **Effective inputs (repo content):** las diecisiete rutas del scope en el commit de implementación `86a05c9`; el scope del Plan 172 en `f77cd3f` para la corrección post-close; los hallazgos de la auditoría adversarial; el registro teórico; el catálogo de garantías del payload (lectura).
- **Observed dependencies:** intérprete Python con biblioteca estándar (`tools/`, `tests/`), `pytest`, CLI `git`. Sin red, sin servicios externos, sin instalación de componentes del payload.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; `pytest` 9.1.1; `git` 2.55; `core.autocrlf = true`; `check_dist_sync.py` no aplica (local-only; rojo en `dev` por el cambio tests-only pendiente); `check_plan_citations.py` conserva **25** citas históricas rotas y **0** referencias legacy falsas; `check_plan_structure.py` reporta los 2 `GAP` declarados (157/158); C-2 el `GAP` del Plan 116; C-3 los cuatro `GAP` declarados (155/158/168/169); `check_version_state.py` emite los 9 warnings históricos de versiones sin tag.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `1c577188d9eca99086c60523d7952ae250ee85cd` (tree del commit de implementación `86a05c9`).
  - **Delta scoped identity:** `281772317353e87be3ba9988e465213c9950449d65d8fdcdf3f305a255782c28` (scope = las diecisiete rutas declaradas; serialización `scoped-v1`, orden canónico).
  - **Scope set (repo-relative paths, ordenados):** las diecisiete rutas del scope.
- **Validity / stale:** `vigente`. El commit de cierre (B) agrega únicamente este Plan, excluido del scope medido; el delta recomputado en `HEAD` es idéntico al declarado y el árbol del estado validado es el de `86a05c9`.
- **Battery result:** 8 repository checkers: 7 PASS + `check_plan_citations` en su baseline (25); `check_enforcement_declarations` PASS (12/12 filas); C-1 `VALID=79 GAP=0 ANOMALY=0`; C-2 `VALID=78 GAP=1 (Plan 116) ANOMALY=0`; C-3 `VALID=37 GAP=4 N/A=33 ANOMALY=0`; `pytest tests/` **1413 passed**; `pytest protocol/.agents/harness/tests/` **207 passed, 1 skipped**; N-9 PASS; `git diff --check` limpio; recomputación de identidad PASS. Detalle en `## Nota de ejecución`.

## Checkpoint / cierre

**Checkpoint / cierre (GC-1).**

- **Commits de cierre:** `86a05c9` (implementación del Plan 173 y sus diecisiete rutas) y el commit de cierre de este Plan en `dev`, que incorpora este Validation Anchor, este Checkpoint y la nota de ejecución. El sub-cambio Clase C de tests del payload se ejecutó antes, en `b51d93c`. Sin amend, rebase, squash ni force-push.
- **Estado validado (ref al Validation anchor):** State identity `1c577188d9eca99086c60523d7952ae250ee85cd`; Delta scoped identity `281772317353e87be3ba9988e465213c9950449d65d8fdcdf3f305a255782c28`.
- **Estado de cierre (identidad):** State identity `1c577188d9eca99086c60523d7952ae250ee85cd`; Delta scoped identity `281772317353e87be3ba9988e465213c9950449d65d8fdcdf3f305a255782c28` (el mismo estado validado, por correspondencia con el anchor aplicable).
- **Árbol material del commit de cierre:** no declarado; el commit aún no existe al escribir este checkpoint y agrega únicamente este Plan (excluido del scope). `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** **PASS** — el estado de cierre declarado es el que la validación consumió (commit `86a05c9`), y el delta recomputado en `HEAD` coincide.
- **Governance aplicada:** RFC-56 Clase B (plan `Aprobado para ejecución`; sin payload en el commit del Plan) + Clase C tests-only (`b51d93c`); RFC-69 (sin release, sin tag); RFC-75 (Mecanismo 7, checkpoint); ADR-16 (autoridad del Change Lifecycle); ADR-20 (`E1-D2`…`E1-D4`); ADR-21; RFC-46 (no se reescribe historia); VC-1/GC-1/LC-1/PC-1.
- **Documentation impact:** `REQUIRED` — actualizados: `.agents/policies/lifecycle-checkers.md` (R5), `docs/VERSIONING.md` (§4.1 con el checker ENF; §9 reconciliado completo), `docs/INVARIANTS.md` (`## Trabajo pendiente`), `docs/plans/INDEX.md`, `docs/working/proposals/INDEX.md`, el inventario (§B/§C.1/§D/§G), `tests/AGENTS.md` (dogfood anclado) y `CHANGELOG.md` (`[Unreleased]`).
- **Roadmap impact:** `NOT_REQUIRED` — corregir una clausura y su clasificación no crea, completa, cancela, reclasifica ni re-prioriza una iniciativa de dirección en `ROADMAP.md`.
- **Condición derivada:** **`Closed`** (plan `Executed` + governance aplicada + checkpoint + consistencia + PASS). `Committed` es estado del repositorio; `Released` es `NO` (el sub-cambio Clase C deja el payload pendiente de la próxima versión; el Plan no se promueve).

## Nota de ejecución

**Ejecutado el 2026-10-21.** Change DEV Clase B + sub-cambio Clase C tests-only, conducido en `dev` bajo la instrucción del mantenedor.

```text
PLAN_ID                   = 173
AUTHORIZATION             = MAINTAINER_AUTHORIZED_FOR_EXECUTION (Phase 0.4 correction)
AUTHORITY_CLASS           = DEV_CLASS_B + PAYLOAD_CLASS_C_TESTS_ONLY
EXECUTION_AUTHORIZED      = YES
RFC_REQUIRED              = NO
PROTOCOL_AUTHORITY        = UNCHANGED (sólo tests del payload; sin VERSION/tag/dist)
EXECUTION_BASELINE_HEAD   = f77cd3f
CLASS_C_COMMIT            = b51d93c
THEORETICAL_ITERATIONS    = 3
THEORETICAL_FINDINGS      = 18 (TF-01…TF-18, todos resueltos)
```

La implementación real se ejecutó como el diseño estabilizado en `docs/working/proposals/PHASE_0_4_CLOSURE_CORRECTION_THEORY_2026-10-21.md`.

### Comparación teoría ↔ realidad

| Elemento del `EXPECTED_FINAL_STATE` | Esperado | Real | Resultado |
|---|---|---|---|
| Ítems terminales | 65 | 65 (15/16/4/22/8) | MATCH |
| `MISCLASSIFIED` / `INSUFFICIENT_EVIDENCE` | 0 / 0 | 0 / 0 | MATCH |
| R5 de C-2 | detecta edición y borrado; permite findings y bullet de commits | 7 fixtures, todas PASS | MATCH |
| INDEX→archivo | 3 namespaces, 0 falsos positivos | 6 fixtures + corpus 0 filas sin target | MATCH |
| Checker ENF | 12/12 PASS, en batería y CI | 12/12 PASS, §4.1 + CI | MATCH |
| Tests Clase C | 3 nuevos, sin VERSION/tag/dist | 3 nuevos; `VERSION` sin cambios; `dist` sin cambios | MATCH |
| §9 | `origin/dist` = `12.3.0`; tests-only pendiente en `dev` | coherente; nota corregida | MATCH |
| Identidad | delta estable, estado = tree(A) | `1c577188…` / `28177231…`; recomputado igual en HEAD | MATCH |
| Corrección de Plan 172 | por referencia, sin editar | Plan 172 intacto; registro en este Plan | MATCH |
| Scope | 0 leaks; payload sólo tests | 17 rutas + Plan; único payload = `b51d93c` | MATCH |
| Batería | checkers + C-1/C-2/C-3 + 2 legs | 7 PASS + baseline 25; C-1 `79/0/0`; C-2 `78/1/0`; C-3 `37/4/33/0`; `1413` / `207+1` | MATCH |

### Resultados finales

| Comando | Resultado |
|---|---|
| `check_protocol_invariants` | PASS — 217 archivos, 10.537 referencias |
| `check_plan_citations` | baseline **25** citas históricas + 0 legacy; exit 1 por baseline |
| `check_plan_structure` | PASS — 0 violaciones; 2 `GAP` declarados (157/158); 0 filas sin target |
| `check_taxonomy_coherence` | PASS |
| `check_session_artifacts` | PASS |
| `check_version_state` | PASS; 9 warnings históricos |
| `check_invariants_equivalence` | PASS — `IDENTICAL: YES`; `ENFORCED=7/15` |
| `check_enforcement_declarations` | PASS — 12/12 filas |
| C-1 | `VALID=79 GAP=0 ANOMALY=0` |
| C-2 | `VALID=78 GAP=1` (Plan 116) `ANOMALY=0` |
| C-3 | `VALID=37 GAP=4` (155/158/168/169) `N/A=33 ANOMALY=0` |
| `pytest tests/` | **1413 passed** |
| `pytest protocol/.agents/harness/tests/` | **207 passed, 1 skipped** |
| N-9 (contra `f77cd3f`) | PASS — 1 hunk en `[Unreleased]`; headings idénticos (71) |
| Recomputación de identidad | PASS — `DECLARED_DELTA == recomputado(A) == recomputado(HEAD)`; `ANCHOR_STATE == CHECKPOINT_STATE == tree(A)` |

**Archivos del Change:** las diecisiete rutas del `## Validation anchor` más este Plan; el sub-cambio Clase C tocó un único archivo de tests del payload (`b51d93c`). `VERSION`, `PROTOCOL_VERSION`, `dist` y tags sin cambios. **`Released = NO`**: el payload tests-only queda pendiente de la próxima versión y el Plan no se promueve.

**Límite declarado:** R5 detecta el vector no commiteado; el checker ENF verifica la declaración, no la verdad de la clase (`INV-12`). Los 22 residual risks genuinos siguen siendo límites reales.

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A.

### Correcciones

N/A — no hay correcciones registradas.

### Pending decisions

N/A — no hay pending decisions.

## Trazabilidad

```text
Auditoría adversarial (PHASE_0_4_CLOSURE_NOT_VALID)
        ↓
Plan 173 (corrección) → implementación teórica → ataque → estabilidad
        ↓
Clase C (G-08) + commit A (10 ítems) + commit B (anchor/checkpoint)
        ↓
Corrección post-close del cierre de Phase 0.4 (Plan 172, por referencia)
        ↓
Closed (dev) · Released = NO
```
