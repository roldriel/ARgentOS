# Plan 173 — Corrección del cierre inválido de Phase 0.4

**Status:** Executed (implementación y validación completas; cierre pendiente — Validation Anchor y Checkpoint)
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

**Validation anchor (VC-1).** <!-- pending closure -->

## Checkpoint / cierre

**Checkpoint / cierre (GC-1).** <!-- pending closure -->

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

La implementación real se ejecutó como el diseño estabilizado en `docs/working/proposals/PHASE_0_4_CLOSURE_CORRECTION_THEORY_2026-10-21.md`; la comparación teoría↔realidad y los resultados finales se registran al cerrar (commit B).

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
