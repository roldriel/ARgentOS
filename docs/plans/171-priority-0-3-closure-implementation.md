# Plan 171 — Implementación de las correcciones de cierre de Priority 0.3

**Status:** Aprobado para redacción
**Fecha:** 2026-10-20
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only: `docs/`, `tools/`, `tests/` y CI; sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** B (RFC-56: mejora documental y de tooling, sin efecto payload)
**Change Level:** L2 (`max(coordination=1, scope=3, architectural impact=0, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 — un agente, un Change. *scope*: 3 — `docs/`, `tools/`, `tests/` y CI. *architectural impact*: 0 — no cambia el modelo ni la frontera DEV/Protocol. *release impact*: 0 — DEV-only, sin versión ni tag. *duration/complexity*: 2 — varias correcciones documentales, tres checkers y sus tests.
**Depende de:** Priority 0.3 canonical contract en `55a11a7`; RFC-84 `Accepted`; ADR-20 `Accepted`; ADR-21 `Accepted`; Plan 170 `Executed`/`Closed`.
**Origen:** instrucción directa del mantenedor (2026-10-20) y cierre canónico de Priority 0.3 (`docs/working/proposals/PRIORITY_0_3_FAILURE_MODEL_AND_IMPLEMENTATION_CONTRACT_2026-10-20.md`). El plan materializa el alcance acotado de 0.3; no reabre su diagnóstico.
**Work type:** `GAP`
**Superseded por:** —

## Objetivo

Implementar **exactamente** el contrato acotado de Priority 0.3: corregir las inconsistencias vivas de `docs/INVARIANTS.md`, reconciliar el registro derivado de `docs/plans/INDEX.md` y el registro post-close de las inconsistencias históricas, extender los tres checkers existentes con reglas deterministas y tests, incorporar la equivalencia canónica al CI, y actualizar `CHANGELOG.md` **sólo** en `[Unreleased]`.

**Este Plan no implementa** G-06, G-07, DEV Memory, garantías semánticas/epistémicas, una garantía más fuerte de integridad histórica ni ninguna edición de planes/RFC/ADR cerrados. Tampoco toca `protocol/`, `runtime/` ni `dist/`.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Implementar el alcance acotado de 0.3 sin reabrir el diagnóstico: correcciones de consistencia, detección determinista y blindaje de `CHANGELOG.md` | humano | `docs/working/proposals/PRIORITY_0_3_FAILURE_MODEL_AND_IMPLEMENTATION_CONTRACT_2026-10-20.md:A. Executive conclusion` |
| `P-2` Confianza de intención | `HIGH` — el contrato fija el scope, los artefactos, los criterios de aceptación y los negativos; el pedido no requiere una decisión nueva | agente | `docs/working/proposals/PRIORITY_0_3_FAILURE_MODEL_AND_IMPLEMENTATION_CONTRACT_2026-10-20.md:C. Final decision table` |
| `P-3` Conjunto de contexto | Contrato 0.3; `docs/INVARIANTS.md`; `docs/plans/INDEX.md`; `docs/plans/169-regularizacion-de-81bbde1-y-reconciliacion-de-pendientes.md`; Plan 170; RFC-84; ADR-20; ADR-21; `docs/VERSIONING.md` §4.1; `.agents/policies/validation-closure.md`; checkers y tests existentes | agente | las rutas citadas |
| `P-4` Derivabilidad | `DERIVABLE` — no hay decisión de autoridad pendiente para el alcance acotado; la única puerta es la aprobación de ejecución del mantenedor (`Aprobado para ejecución`) | agente | `docs/working/proposals/PRIORITY_0_3_FAILURE_MODEL_AND_IMPLEMENTATION_CONTRACT_2026-10-20.md:D.4 Implementation authorization` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`) |
| `P-6` Conocimiento vigente | RFC-84, ADR-20 y ADR-21 `Accepted`; Plan 170 `Executed`/`Closed`; `docs/INVARIANTS.md` activo y con una interpretación local desactualizada; `docs/plans/INDEX.md` derivado y mutable | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-56 Clase B, RFC-69, RFC-75, ADR-16, VC-1, GC-1, LC-1, PC-1, `docs/VERSIONING.md` §4.1. `NOT_APPLICABLE`: RFC-56 Clase A (no payload), RFC-46 (no se reescribe historia), RFC-69 release (docs-only). | agente | `docs/CONVENTIONS.md`; `docs/VERSIONING.md` |
| `P-8` Autoridad y scope | Autoridad: mantenedor para `Aprobado para ejecución`. Scope declarado: las rutas de `## Entregables`. No se amplía por inferencia. | humano | este Plan |

## Criterio de entrada

- [x] Contrato canónico de Priority 0.3 en `dev` (`55a11a7`), con 15 modos dispositionados, 23 decisiones y 11 riesgos.
- [x] `docs/INVARIANTS.md`, `docs/plans/INDEX.md`, los tres checkers, sus tests y el workflow existen en el baseline.
- [x] Worktree sin cambios preexistentes tracked; los dos untracked del usuario permanecen intactos.
- [x] Plan registrado en `docs/plans/INDEX.md`.
- [ ] **Autorización de ejecución:** el Plan debe pasar de `Aprobado para redacción` a `Aprobado para ejecución` por el mantenedor. **No satisfecha en esta sesión.**
- [x] **Ningún pendiente bloqueante** del Plan sin resolución/escalación. **Satisfecha.**

**Estado:** el Plan está completo y listo para autorización, pero **no puede ejecutarse** hasta que el mantenedor lo apruebe para ejecución. La sesión de planificación no ejecuta, no valida la implementación y no cierra el Plan.

## Entregables

1. `docs/INVARIANTS.md` — interpretación local de `INV-07`, vocabulario de enforcement y estado de gaps corregidos; bloque canónico intacto.
2. `docs/plans/INDEX.md` — fila del Plan 169 corregida a `Executed`.
3. `docs/plans/171-priority-0-3-closure-implementation.md` — sección `## Post-close record` con las inconsistencias de 157/158 y los cuatro casos de findings en estado `open` (155, 158, 168, 169), sin editar los planes cerrados.
4. `tools/check_plan_structure.py` — regla status/INDEX.
5. `tools/check_lifecycle_lineage.py` — regla `Closed` + finding `open`.
6. `tools/check_invariants_equivalence.py` — regla de vocabulario y recuento de enforcement.
7. `.github/workflows/check-protocol.yml` — paso de equivalencia canónica.
8. `tests/test_check_plan_structure.py`, `tests/test_check_lifecycle_lineage.py`, `tests/test_check_invariants_equivalence.py` — fixtures positivos y negativos.
9. `CHANGELOG.md` — una entrada en `[Unreleased]`, `(plan 171)`, con N-9.
10. `## Validation anchor` y `## Checkpoint / cierre` del Plan, completados en la ejecución.

## Pasos

### Paso 0 — Preflight y baseline

- **Archivo:** ninguno (lectura).
- **Modificación:** ninguna.
- **Motivo:** fijar el estado del que parte la ejecución y detectar cambios ajenos.
- **Precondición:** Plan `Aprobado para ejecución`.
- **Resultado esperado:** `git status` sólo con los dos untracked del usuario; HEAD registrado; el contrato 0.3 en `55a11a7`.
- **Evidencia:** `git status --porcelain=v2 --branch`; `git rev-parse HEAD`.
- **Validación posterior:** si aparece un cambio tracked ajeno, `STOP`; no se ejecuta.

### Paso 1 — Corregir `docs/INVARIANTS.md`

- **Archivo:** `docs/INVARIANTS.md`.
- **Modificación:** (a) reemplazar la interpretación de `INV-07` para reflejar el hook del proyecto adoptante y su límite fail-open, aclarando que en DEV la vía es RFC-56/release; (b) añadir `ENFORCED:session-hook` a la tabla de vocabulario; (c) reconciliar `## Trabajo pendiente` para distinguir gaps implementados (E1-G1, G-05, G-09), rechazados (G-03, G-06) y pendientes (con referencia a Plan 170 `PC-2` y ADR-21). **No tocar** el bloque `canonical-invariants-v1` ni la copia Protocol.
- **Motivo:** eliminar la contradicción viva de enforcement (FM-12) y la afirmación de estado obsoleta (FM-10).
- **Precondición:** Paso 0.
- **Resultado esperado:** el bloque canónico permanece byte-idéntico; la interpretación local y el vocabulario son coherentes con el bloque y con el hook.
- **Evidencia:** `git diff -- docs/INVARIANTS.md`; `python tools/check_invariants_equivalence.py`.
- **Validación posterior:** AC-1, AC-7.

### Paso 2 — Corregir el registro derivado `docs/plans/INDEX.md`

- **Archivo:** `docs/plans/INDEX.md`.
- **Modificación:** fila del Plan 169: `Aprobado para ejecución` → `Executed`. No cambiar filas de 157/158 (su `Status` es materia de D-0.3-23).
- **Motivo:** eliminar el desajuste status/INDEX (FM-09) en el registro derivado mutable.
- **Precondición:** Paso 0.
- **Resultado esperado:** la fila 169 coincide con el header `Executed` del Plan 169.
- **Evidencia:** `git diff -- docs/plans/INDEX.md`.
- **Validación posterior:** AC-3.

### Paso 3 — Crear el registro post-close

- **Archivo:** `docs/plans/171-priority-0-3-closure-implementation.md`.
- **Modificación:** añadir `## Post-close record` con: (a) la inconsistencia factual de 157/158 (`Status: Aprobado para ejecución`, cuerpo declara `Closed`) y el estado derivado declarado por el cuerpo, **sin decidir D-0.3-23**; (b) los cuatro planes `Closed` con findings en estado `open` (155, 158, 168, 169), con su estado real y la nota de que 152 está `Executed`, no `Closed`.
- **Motivo:** registrar por referencia, sin editar artefactos cerrados (ADR-20 `E1-D4`; RFC-46).
- **Precondición:** Paso 0.
- **Resultado esperado:** el registro existe en un artefacto nuevo; `git diff` de los planes 155/157/158/168/169 vacío.
- **Evidencia:** `git diff -- docs/plans/155-* docs/plans/157-* docs/plans/158-* docs/plans/168-* docs/plans/169-*` vacío; sección nueva en el Plan 171.
- **Validación posterior:** AC-4.

### Paso 4 — Extender `tools/check_plan_structure.py`

- **Archivo:** `tools/check_plan_structure.py` y `tests/test_check_plan_structure.py`.
- **Modificación:** comparar el `**Status:**` base del header con el status base de la fila del INDEX. 157/158 se reportan `GAP` (legacy declarado), no `ANOMALY`; cualquier otro plan debe coincidir. Añadir fixtures: coincidencia, desajuste, legacy.
- **Motivo:** detectar FM-09 de forma determinista y evitar el desajuste 169.
- **Precondición:** Paso 2.
- **Resultado esperado:** el checker detecta el desajuste; 157/158 quedan como `GAP`; el corpus actual pasa tras corregir 169.
- **Evidencia:** `python -m pytest tests/test_check_plan_structure.py -q`; `python tools/check_plan_structure.py`.
- **Validación posterior:** AC-3.

### Paso 5 — Extender `tools/check_lifecycle_lineage.py`

- **Archivo:** `tools/check_lifecycle_lineage.py` y `tests/test_check_lifecycle_lineage.py`.
- **Modificación:** reportar `ANOMALY` cuando un plan contiene `## Checkpoint / cierre` con `Condición derivada: **Closed**` (o declaración `Closed` equivalente) y un finding en estado `open`. 155/158/168/169 se reportan `GAP` (legacy declarado); cualquier otro plan sigue la regla. Añadir fixtures positivo/negativo/legacy.
- **Motivo:** hacer verificable la condición de stop de cierre que hoy no se comprueba (FM-09).
- **Precondición:** Paso 3.
- **Resultado esperado:** el checker detecta `Closed` + `open`; los cuatro legacy quedan como `GAP`; C-3 no introduce `ANOMALY` sobre el corpus actual.
- **Evidencia:** `python -m pytest tests/test_check_lifecycle_lineage.py -q`; `python tools/check_lifecycle_lineage.py`.
- **Validación posterior:** AC-4.

### Paso 6 — Extender `tools/check_invariants_equivalence.py`

- **Archivo:** `tools/check_invariants_equivalence.py` y `tests/test_check_invariants_equivalence.py`.
- **Modificación:** parsear la columna `ENFORCEMENT_STATUS` del bloque canónico y la tabla de vocabulario de `docs/INVARIANTS.md`: toda etiqueta `ENFORCED:*` usada debe estar definida; el recuento declarado `7/15 ENFORCED · 2/15 VALIDATED · 6/15 NONE` debe coincidir con el bloque. Añadir fixtures de etiqueta no definida, recuento incorrecto y caso correcto.
- **Motivo:** detectar la sobredeclaración de enforcement (FM-12) en la capa donde es determinista.
- **Precondición:** Paso 1.
- **Resultado esperado:** el checker falla con etiqueta/recuento inconsistente y pasa con el estado corregido; la equivalencia byte a byte sigue verificándose.
- **Evidencia:** `python -m pytest tests/test_check_invariants_equivalence.py -q`; `python tools/check_invariants_equivalence.py`.
- **Validación posterior:** AC-1, AC-7.

### Paso 7 — Incorporar la equivalencia al CI

- **Archivo:** `.github/workflows/check-protocol.yml`.
- **Modificación:** añadir `python tools/check_invariants_equivalence.py` al job de checkers, junto a los demás comandos deterministas.
- **Motivo:** convertir la detección manual del drift canónico en una detección de CI (FM-13, alcance estructural acotado).
- **Precondición:** Paso 6.
- **Resultado esperado:** el workflow ejecuta el checker y falla si el bloque diverge.
- **Evidencia:** `git diff -- .github/workflows/check-protocol.yml`; YAML válido.
- **Validación posterior:** AC-2.

### Paso 8 — Añadir/ajustar los tests

- **Archivo:** los tres archivos de test del Paso 4–6.
- **Modificación:** completar fixtures positivos, negativos y legacy; un test negativo de equivalencia que altere una copia y espere fallo.
- **Motivo:** demostrar que las nuevas reglas fallan cuando deben fallar, no sólo que pasan.
- **Precondición:** Pasos 4–6.
- **Resultado esperado:** todos los tests nuevos y existentes pasan.
- **Evidencia:** `python -m pytest tests/ -q`; salida por archivo.
- **Validación posterior:** AC-2, AC-3, AC-4.

### Paso 9 — Actualizar `CHANGELOG.md` sólo en `[Unreleased]`

- **Archivo:** `CHANGELOG.md`.
- **Modificación:** una única entrada en `[Unreleased]`, `(plan 171)`, que describa la implementación acotada de 0.3. **No** tocar releases históricos, no reordenar, no duplicar, no insertar en secciones cerradas, no reformatear.
- **Motivo:** registrar el Change docs-only/tooling en el lugar previsto, sin repetir el incidente de corrupción histórica.
- **Precondición:** Pasos 1–8.
- **Resultado esperado:** un solo hunk dentro de `[Unreleased]`; la secuencia de headings históricos no cambia.
- **Evidencia:** `git diff -U0 -- CHANGELOG.md`; salida del guard N-9 de `## Verificación`.
- **Validación posterior:** AC-11, N-9.

### Paso 10 — Validar, registrar anchor/checkpoint y cerrar

- **Archivo:** `docs/plans/171-priority-0-3-closure-implementation.md` (Validation anchor, Checkpoint / cierre, Nota de ejecución).
- **Modificación:** registrar el command-set, los effective inputs, los factores ambientales, la Scoped Content Identity y la consistencia checkpoint↔anchor; declarar la condición derivada `Closed` sólo si `Executed` + governance + checkpoint + PASS.
- **Motivo:** cerrar el Plan según RFC-75/GC-1, no por apariencia.
- **Precondición:** Pasos 1–9 y AC-1…AC-11.
- **Resultado esperado:** Plan `Executed` con `Closed` derivado; sin release (docs-only, RFC-69).
- **Evidencia:** anchor/checkpoint; salidas de checkers, C-1/C-2/C-3, tests; `git diff --name-only` dentro del scope.
- **Validación posterior:** AC-9, `## J` del contrato 0.3.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: el Change es DEV-only documental/tooling/tests/CI; no hay red, git remoto, instalación, operación destructiva ni escritura fuera del proyecto | este Plan | authorized |

## Criterios de salida

- **AC-1** `docs/INVARIANTS.md` no usa etiquetas `ENFORCED:*` sin definir; `INV-07` coincide con el bloque y con el hook del adoptante; la lista de gaps distingue implementados, rechazados y pendientes. **Verificación:** test/checker + lectura contra `hook_gate.py`, RFC-84 y ADR-21.
- **AC-2** `check_invariants_equivalence.py` corre en CI y falla si una copia del bloque diverge. **Verificación:** workflow + test negativo.
- **AC-3** `check_plan_structure.py` detecta status/INDEX divergentes; la fila 169 es `Executed`; 157/158 quedan como legacy declarado. **Verificación:** fixture + `git diff`.
- **AC-4** `check_lifecycle_lineage.py` detecta `open` en un plan que declara `Closed`; los cuatro legacy están registrados. **Verificación:** fixture + post-close record.
- **AC-5** El artefacto 0.3 sigue siendo canónico; el INDEX de propuestas lo apunta; no hay citas rotas nuevas. **Verificación:** `check_plan_citations` (baseline 26 + 1) + diff.
- **AC-6** 0 cambios en `protocol/.agents/`, `protocol/_AGENTS.md`, `runtime/` y `dist/`. **Verificación:** `git diff --name-only`.
- **AC-7** 0 invariantes/properties nuevos; bloque canónico byte-idéntico. **Verificación:** `check_invariants_equivalence.py` + diff.
- **AC-8** El contrato 0.3 declara las no-garantías y `Closed` procedural. **Verificación:** lectura de §A/§K del contrato.
- **AC-9** Batería ejecutada con la taxonomía de `## Verificación`: 7 repository checkers (6 pass + baseline de citations), 2 legs de tests, C-1/C-2/C-3 con `ANOMALY=0`; anchor/checkpoint. **Verificación:** salidas registradas.
- **AC-10** Un lector puede implementar el alcance sin re-derivar el modelo de fallos ni el estado de las decisiones. **Verificación:** checklist de §C.1 del contrato + revisión.
- **AC-11** `CHANGELOG.md` sólo cambió dentro de `[Unreleased]`; ningún release histórico fue modificado, reordenado, duplicado, insertado, borrado o reformateado; la secuencia de headings históricos es idéntica. **Verificación:** `git diff -U0 -- CHANGELOG.md` + guard N-9.

## Verificación

### Taxonomía (sin ambigüedad)

| Categoría | Miembros exactos | Qué prueba | Qué no prueba |
|---|---|---|---|
| Repository checkers (7) | `check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `check_invariants_equivalence` | Invariantes estructurales/documentales del repo | Verdad semántica, completitud o corrección de una decisión |
| Lifecycle checks (3) | C-1 `check_lifecycle_anchor`, C-2 `check_lifecycle_checkpoint`, C-3 `check_lifecycle_lineage` | Presencia/forma/consistencia de anchors, checkpoints y lineage | Verdad del contenido; C-2 no exige `validated tree == closing commit tree` |
| Tests (2 legs) | `pytest tests/`; `pytest protocol/.agents/harness/tests/` | Comportamiento especificado por los tests | Propiedades no cubiertas; verdad semántica |
| Auxiliary | `git diff --check`, `git diff --name-only`, `git status`, `git diff -U0 -- CHANGELOG.md` | Limpieza, scope y N-9 | Corrección del contenido |

**"Seis de siete"** se refiere exclusivamente a los **7 repository checkers**: seis pasan y `check_plan_citations` conserva su baseline (26 citas históricas rotas + 1 referencia legacy). No cuenta C-1/C-2/C-3, los tests ni los comandos auxiliares.

### Comandos exactos

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_invariants_equivalence.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_lineage.py
python tools/check_lifecycle_checkpoint.py
git diff --check
git diff --name-only 55a11a7..HEAD
git status --porcelain=v2 --branch
git diff -U0 -- CHANGELOG.md
```

### Guard N-9 de `CHANGELOG.md`

Ejecutar antes del commit de cierre, con el baseline `55a11a7` y el working tree como estado nuevo. El script es una verificación del Change, **no** un checker nuevo del repositorio:

```powershell
@'
import subprocess, re, sys

BASE = "55a11a7"
OLD = subprocess.check_output(["git", "show", f"{BASE}:CHANGELOG.md"], text=True, encoding="utf-8").splitlines()
NEW = open("CHANGELOG.md", encoding="utf-8").read().splitlines()

def region(lines):
    u = next((i for i, l in enumerate(lines) if l.strip() == "## [Unreleased]"), None)
    if u is None:
        raise SystemExit("N-9 FAIL: no [Unreleased] heading")
    nxt = [i for i, l in enumerate(lines) if i > u and l.startswith("## [")]
    if not nxt:
        raise SystemExit("N-9 FAIL: no historical release heading after [Unreleased]")
    return u + 1, nxt[0]  # 0-based allowed content indices

old_start, old_end = region(OLD)
new_start, new_end = region(NEW)

old_hist = [l for l in OLD if l.startswith("## [") and not l.startswith("## [Unreleased]")]
new_hist = [l for l in NEW if l.startswith("## [") and not l.startswith("## [Unreleased]")]
if old_hist != new_hist:
    raise SystemExit("N-9 FAIL: historical heading sequence changed")

diff = subprocess.check_output(["git", "diff", "-U0", "--", "CHANGELOG.md"], text=True, encoding="utf-8")
for line in diff.splitlines():
    m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
    if not m:
        continue
    a, b, c, d = (int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1))
    if b and not (old_start + 1 <= a and a + b - 1 <= old_end):
        raise SystemExit(f"N-9 FAIL: old hunk outside [Unreleased]: {line}")
    if d and not (new_start + 1 <= c and c + d - 1 <= new_end):
        raise SystemExit(f"N-9 FAIL: new hunk outside [Unreleased]: {line}")

print("N-9 PASS: only [Unreleased] changed; historical headings unchanged")
'@ | python -
```

**Lectura:** un `FAIL` del guard es un fallo del Change; no se corrige reformateando historia. Se restaura el archivo desde el baseline y se rehace la entrada.

## Validation anchor

**No aplica todavía.** El Plan está `Aprobado para redacción` y no fue ejecutado; este anchor se completa en el Paso 10, sólo después de la validación. No hay una validación registrada que anclar en esta sesión.

## Checkpoint / cierre

**No aplica todavía.** El Plan no está `Executed`; no hay checkpoint ni condición derivada `Closed`. Se completa en el Paso 10, sólo si `Executed` + governance aplicada + checkpoint + consistencia + PASS.

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A al momento de la planificación.

### Correcciones

N/A — no hay correcciones en la planificación.

### Pending decisions

N/A — la ejecución está gobernada por el gate de autorización del Plan (`Aprobado para ejecución`), no por una pending decision de 0.3.

## Riesgos

1. **Corrupción histórica del `CHANGELOG.md`.** Mitigación: N-9 + guard de diff; sólo `[Unreleased]`; prohibido tocar releases históricos.
2. **Scope creep hacia `protocol/` o runtime.** Mitigación: `## Efectos declarados`, N-1, AC-6, `git diff --name-only`.
3. **Falso verde por confundir checkers con semántica.** Mitigación: taxonomía de verificación; `DETECT` de FM-13 acotado; el plan no declara garantías semánticas.
4. **Edición de planes cerrados.** Mitigación: post-close record en el Plan 171; `git diff` de 155/157/158/168/169 vacío; D-0.3-23 no se decide.
5. **Regresión de los checkers existentes.** Mitigación: tests positivos y negativos; corpus legacy declarado; C-1/C-2/C-3 `ANOMALY=0`.
6. **Entorno de tests no ejecutable.** Mitigación: declarar `GAP` ambiental, nunca PASS; el baseline de esta sesión sí ejecutó ambas legs.

## Trazabilidad

```text
Priority 0.3 canonical contract @ 55a11a7
        ↓
Plan 171 (este Plan, Aprobado para redacción)
        ↓
docs/INVARIANTS.md · docs/plans/INDEX.md · post-close record · 3 checkers + tests · CI · CHANGELOG [Unreleased]
        ↓
Validation anchor + Checkpoint → Executed → Closed (derivado) → commit en dev
```

El Plan no se cierra en la sesión de planificación: `Aprobado para redacción` no es `Executed`; no hay `## Validation anchor`, `## Checkpoint / cierre` ni condición derivada `Closed` hasta la ejecución autorizada.
