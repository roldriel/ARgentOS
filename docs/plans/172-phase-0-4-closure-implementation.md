# Plan 172 — Cierre de la deuda heredada de Phase 0 (Phase 0.4)

**Status:** Executed
**Fecha:** 2026-10-20
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only: `docs/`, `tools/`, `tests/` y `runtime/orchestrator/`; sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** B (RFC-56: mejora documental, de tooling y del orquestador DEV, sin efecto payload)
**Change Level:** L2 (`max(coordination=1, scope=3, architectural impact=1, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 — un agente, un Change. *scope*: 3 — `docs/`, `tools/`, `tests/`, `runtime/orchestrator/` y CI no tocado. *architectural impact*: 1 — materializa decisiones ya aceptadas de ADR-20 en el orquestador DEV; no cambia el modelo ni la frontera DEV/Protocol. *release impact*: 0 — DEV-only, sin versión ni tag. *duration/complexity*: 2 — inventario de 65 ítems, tres módulos del orquestador, un checker, dos suites y seis documentos de registro.
**Depende de:** `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md`; ADR-20 `Accepted`; ADR-21 `Accepted`; RFC-84 `Accepted`; RFC-46; RFC-69; RFC-75; Plan 171 `Closed`.
**Origen:** instrucción directa del mantenedor (2026-10-20) que ordena ejecutar Phase 0.4 en una sola vuelta: auditoría, clasificación, correcciones, tests, validación, anchor/checkpoint, cierre, commit y promoción, sin iniciar Phase 1.
**Work type:** `GAP`
**Superseded por:** —

## Objetivo

Cerrar **exhaustivamente** la deuda heredada de Phase 0.1, 0.2 y 0.3: construir el inventario completo de residuos materiales con un estado terminal por ítem, materializar las correcciones que el modelo existente permite (sin inventar garantías ni mecanismos), corregir los registros derivados desactualizados y clasificar formalmente lo que sigue existiendo como límite real.

**Este Plan no inicia Phase 1**, no añade invariantes, properties, gates, estados de lifecycle, registries, autoridades ni garantías semánticas/epistémicas, no modifica `protocol/`, `dist/` ni el contenido gobernante de ningún plan, RFC o ADR cerrado, y no crea un sistema nuevo de historial, de autoridad ni de enforcement.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Cerrar la deuda heredada de Phase 0 con estados terminales explícitos, correcciones donde el modelo lo permita y clasificación formal donde no | humano | instrucción del mantenedor (2026-10-20); `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md:A` |
| `P-2` Confianza de intención | `HIGH` — la instrucción fija el método, los estados terminales, las validaciones y las prohibiciones; no requiere una decisión nueva de alcance | agente | el contrato de Phase 0.4 |
| `P-3` Conjunto de contexto | inventario Phase 0.4; cierre de diseño 0.2; contrato 0.3; ADR-20; ADR-21; RFC-84; Plan 170; Plan 171; `docs/INVARIANTS.md`; `docs/plans/INDEX.md`; `docs/working/proposals/INDEX.md`; `docs/VERSIONING.md` §9; los tres módulos del orquestador afectados; `tools/check_plan_citations.py` y su suite | agente | las rutas citadas |
| `P-4` Derivabilidad | `DERIVABLE` — las decisiones de 0.2 y 0.3 están tomadas; las que exigían autoridad superior (`D-0.3-12`, `D-0.3-23`) se resuelven dentro de las reglas existentes (riesgo residual aceptado y rechazo por diseño), no por inferencia de autoridad nueva | agente | ADR-20 `E1-D3`/`E1-D4`; RFC-46; ADR-21; este Plan |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`) |
| `P-6` Conocimiento vigente | RFC-84, ADR-20 y ADR-21 `Accepted`; Planes 170 y 171 `Closed`; release `12.3.0` en `master`/`dev`/`dist`; las superficies derivadas (`INDEX`, §9) estaban desactualizadas | documento | `protocol/.agents/VERSION`; `git tag --list`; `origin/dist` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-56 Clase B, RFC-69, RFC-75, ADR-16, ADR-20, ADR-21, RFC-46, VC-1, GC-1, LC-1, PC-1, `docs/VERSIONING.md` §4.1. `NOT_APPLICABLE`: RFC-56 Clase A (sin payload), release (docs-only/tooling). | agente | `docs/CONVENTIONS.md`; `docs/VERSIONING.md` |
| `P-8` Autoridad y scope | Autoridad: mantenedor para ejecutar Phase 0.4 y para aceptar los riesgos residuales que el inventario declara. Scope declarado: las rutas de `## Entregables`. No se amplía por inferencia. | humano | este Plan; inventario Phase 0.4 |

## Criterio de entrada

- [x] Instrucción del mantenedor que autoriza Phase 0.4 completa (auditoría, clasificación, corrección, validación, commit y promoción; sin Phase 1).
- [x] Inventario construido **antes** de modificar archivos: `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md`.
- [x] Baseline identificado: `dev` = `master` = `0bcce23` (release `12.3.0`); dos untracked del usuario preservados.
- [x] Las decisiones heredadas que exigían autoridad superior tienen una vía de cierre dentro de las reglas existentes (`D-0.3-12` → riesgo residual aceptado; `D-0.3-23` → rechazo por diseño por `INV-04`).
- [x] Ningún pendiente bloqueante sin resolución. **Satisfecha.**
- [x] Plan registrado en `docs/plans/INDEX.md` con `Status` coincidente.

**Estado:** el Plan fue ejecutado bajo la autorización registrada; la evidencia, los resultados AC/N y el cierre están en `## Nota de ejecución` y `## Checkpoint / cierre`.

## Entregables

1. `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md` — inventario de 65 ítems con estado terminal, evidencia y rationale (nuevo).
2. `docs/working/proposals/INDEX.md` — fila del inventario 0.4 y reconciliación de las filas 0.2/0.3.
3. `docs/plans/INDEX.md` — estado del Plan 171 corregido y registro del Plan 172.
4. `docs/VERSIONING.md` §9 — snapshot de estado actual reconciliado a `12.3.0`.
5. `docs/INVARIANTS.md` — interpretación local de INV-01/INV-04/INV-08 y estado terminal de los doce gaps en `## Trabajo pendiente`.
6. `docs/adr/20-closed-artifact-governance-and-execution-records.md` — `## Estado de implementación` actualizado y `## Amendment Log` con `E1-G1`…`E1-G5`.
7. `runtime/orchestrator/observation.py` — `PlanWriteAuthority`, `derive_plan_write_authority`, `ChangeObservation.closure_declared`.
8. `runtime/orchestrator/governance.py` — verificación de autoridad de escritura en cada escritor de plan.
9. `runtime/orchestrator/host.py` — autoridad derivada en toda ruta (sin `plan_authorized=True` fijo), negativa convertida en stop, registro externo de ejecución.
10. `tools/check_plan_citations.py` — falso positivo de path legacy y resolución de heading numerado.
11. `tests/test_autonomous_orchestrator.py` — pruebas de autoridad derivada, `Executed` ≠ `Closed`, cierre y registro externo.
12. `tests/test_check_plan_citations.py` — pruebas del falso positivo y del heading numerado.
13. `CHANGELOG.md` — una entrada en `[Unreleased]` `(plan 172)`; N-9.
14. `## Validation anchor` y `## Checkpoint / cierre` de este Plan, completados en la ejecución.

## Pasos

### Paso 0 — Preflight y baseline

- **Archivo:** ninguno (lectura).
- **Modificación:** ninguna.
- **Motivo:** fijar el estado de partida y detectar cambios ajenos.
- **Precondición:** instrucción del mantenedor.
- **Resultado esperado:** `git status` sólo con los dos untracked del usuario; HEAD `0bcce23`; `dev` = master.
- **Evidencia:** `git status --porcelain=v2 --branch`; `git rev-parse HEAD dev master`.

### Paso 1 — Inventario antes de modificar

- **Archivo:** `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md`.
- **Modificación:** inventario completo de Phase 0.1, 0.2, 0.3 y legacy con los once campos por ítem y estado terminal.
- **Motivo:** no se corrige nada sin saber qué conjunto se está cerrando.
- **Resultado esperado:** 65 ítems, `UNCLASSIFIED = 0`.
- **Evidencia:** el documento; §D del inventario.

### Paso 2 — Materializar `E1-G2`/`E1-G3`/`E1-G4`

- **Archivo:** `runtime/orchestrator/observation.py`, `governance.py`, `host.py`.
- **Modificación:** autoridad de escritura derivada del artefacto (`PlanWriteAuthority`), verificación en cada escritor, distinción `Executed`/`Closed`, rechazo de escritura sobre contenido gobernante cerrado y conversión de la negativa en `STOP_FORBIDDEN_ACTION`.
- **Motivo:** ADR-20 `E1-D3`/`E1-D4`; los gaps `E1-G2`, `E1-G3`, `E1-G4` siguen abiertos.
- **Precondición:** Paso 0.
- **Resultado esperado:** ninguna ruta de producción fija `plan_authorized=True`; una aserción del caller no abre un plan cerrado.
- **Evidencia:** tests del Paso 5; `git diff`.

### Paso 3 — Materializar `E1-G5`

- **Archivo:** `runtime/orchestrator/host.py`.
- **Modificación:** la corrida se registra en `.project/orchestrator/plan-NNN/runs/<run_id>.md`; el plan recibe sólo una referencia marcada como registro externo y no la recibe si ya declara `Closed`.
- **Motivo:** ADR-20 `E1-D2`; el registro externo estaba definido y no materializado.
- **Resultado esperado:** el plan no contiene el registro; la referencia y el registro externo existen.
- **Evidencia:** tests del Paso 5.

### Paso 4 — Corregir el checker de citas

- **Archivo:** `tools/check_plan_citations.py` y `tests/test_check_plan_citations.py`.
- **Modificación:** (a) un path que resuelve canónicamente no es una referencia legacy, de modo que la capa operativa DEV `.agents/` deja de confundirse con el mapeo pre-migración; (b) un heading numerado puede citarse sin su número (`§Enforcement deferred` → «24. Enforcement deferred»).
- **Motivo:** eliminar un falso positivo y una cita rota que no lo eran, sin tocar artefactos cerrados.
- **Resultado esperado:** `check_plan_citations` pasa de 26 citas rotas + 1 referencia legacy a **25 + 0**, sin corregir historia.
- **Evidencia:** salida del checker; tests.

### Paso 5 — Pruebas

- **Archivo:** `tests/test_autonomous_orchestrator.py`, `tests/test_check_plan_citations.py`.
- **Modificación:** pruebas positivas y negativas de la autoridad derivada, `Executed` ≠ `Closed`, negativa a escribir un plan cerrado, stop con evidencia, referencia al registro externo, falso positivo legacy y heading numerado.
- **Motivo:** demostrar que las reglas fallan cuando deben fallar.
- **Resultado esperado:** las pruebas nuevas pasan y las existentes no regresan.
- **Evidencia:** `python -m pytest tests/`.

### Paso 6 — Registros derivados y documentación operativa

- **Archivo:** `docs/plans/INDEX.md`, `docs/working/proposals/INDEX.md`, `docs/VERSIONING.md` §9, `docs/INVARIANTS.md`, `docs/adr/20-closed-artifact-governance-and-execution-records.md`, `CHANGELOG.md`.
- **Modificación:** corregir el estado del Plan 171 y registrar el 172; reconciliar las filas 0.2/0.3 y añadir la 0.4; reconciliar §9 a `12.3.0`; corregir INV-08 y el estado terminal de los gaps; registrar el `Amendment Log` de ADR-20; entrada en `[Unreleased]`.
- **Motivo:** FM-10 (documentación obsoleta en superficies vivas); D-0.3-18.
- **Resultado esperado:** ninguna superficie viva contradice su fuente; el contenido gobernante de artefactos cerrados no se edita.
- **Evidencia:** diffs por archivo; checkers.

### Paso 7 — Validar, registrar anchor/checkpoint y cerrar

- **Archivo:** este Plan (`## Validation anchor`, `## Checkpoint / cierre`, `## Nota de ejecución`).
- **Modificación:** registrar command-set, effective inputs, factores ambientales, Scoped Content Identity y la consistencia checkpoint↔anchor; declarar `Closed` sólo si `Executed` + governance + checkpoint + PASS.
- **Motivo:** cerrar según RFC-75/GC-1.
- **Resultado esperado:** `Executed` con `Closed` derivado, sin release.
- **Evidencia:** anchor/checkpoint; salidas de la batería.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: el Change es DEV-only documental/tooling/tests/orquestador; no hay red, git remoto, instalación, operación destructiva ni escritura fuera del proyecto | este Plan | authorized |

## Criterios de salida

**Resultado esperado de cada AC: PASS.**

- **AC-1** Existe un inventario completo con estado terminal por ítem y evidencia; `UNCLASSIFIED = 0`. **Verificación:** inventario §B/§D.
- **AC-2** Todo estado terminal pertenece al conjunto canónico; `DEFERRED`, `OUT_OF_SCOPE`, `ESCALATED`, `PENDING`, `OPEN` y `UNCLASSIFIED` no aparecen como estado de ningún ítem. **Verificación:** inventario §D + revisión.
- **AC-3** `E1-G2`/`E1-G3`/`E1-G4` materializados y cubiertos por pruebas positivas y negativas. **Verificación:** tests + diff.
- **AC-4** `E1-G5` materializado: registro externo con referencia desde el plan y sin escritura sobre planes cerrados. **Verificación:** tests.
- **AC-5** Ninguna ruta de producción fija `plan_authorized=True`. **Verificación:** búsqueda en `runtime/`.
- **AC-6** `check_plan_citations` baja su baseline a 25 citas históricas rotas y 0 referencias legacy falsas, sin editar artefactos cerrados. **Verificación:** salida del checker.
- **AC-7** Los registros derivados reflejan el estado real (Plan 171, filas 0.2/0.3, §9 a `12.3.0`, INV-08, ADR-20). **Verificación:** diffs + checkers.
- **AC-8** Cero cambios en `protocol/`, `dist/` y `runtime/` fuera del orquestador. **Verificación:** `git diff --name-only`.
- **AC-9** Ningún plan, RFC o ADR cerrado fue editado en su contenido gobernante; ADR-20 sólo recibe su estado de implementación y su `Amendment Log`. **Verificación:** diff de los artefactos cerrados.
- **AC-10** Batería completa: 6 de los 7 repository checkers en verde + `check_plan_citations` en su nuevo baseline; C-1/C-2/C-3 con `ANOMALY=0`; ambas legs de `pytest` verdes. **Verificación:** salidas registradas.
- **AC-11** Sin phase 1: no se crea ninguna capacidad, decisión ni artefacto de Phase 1. **Verificación:** diff + revisión.

## Criterios negativos

- **N-1** Ningún cambio en `protocol/`, `dist/` ni `runtime/` fuera de `runtime/orchestrator/`.
- **N-2** Ningún invariante, property, gate, estado de lifecycle, registry, namespace, autoridad ni garantía semántica/epistémica nuevos.
- **N-3** Ninguna edición del bloque canónico `canonical-invariants-v1` ni de la copia Protocol.
- **N-4** Ninguna reescritura del contenido gobernante de un plan, RFC o ADR cerrado.
- **N-5** Ningún riesgo marcado como aceptado sin acto de autoridad citado.
- **N-6** Ninguna modificación del `CHANGELOG.md` fuera de `[Unreleased]`; sin reordenar, duplicar ni reformatear historia (N-9).
- **N-7** Ningún `git add -A` ni staging masivo; no se commitean `.project/` ni los dos untracked del usuario.
- **N-8** Ningún `AUTHORIZED FOR IMPLEMENTATION` ni trabajo de Phase 1.

**Resultado esperado de los criterios negativos: ninguno de N-1…N-8 ocurre.**

## Evidence contract

1. **Qué se modificó:** `git diff --name-only 0bcce23..HEAD` y diff por archivo.
2. **Qué no se modificó:** cero rutas de `protocol/`, `dist/`, `runtime/` fuera del orquestador y de los dos untracked.
3. **Tests:** `python -m pytest tests/` y `python -m pytest protocol/.agents/harness/tests/` con sus conteos.
4. **Checkers:** los siete repository checkers y C-1/C-2/C-3 con la taxonomía de `## Verificación`.
5. **Baseline que permanece:** 25 citas históricas rotas (todas a secciones de `ROADMAP.md` eliminadas por los planes 157/158, en artefactos cerrados); `check_version_state` con los 9 warnings históricos de `3.7.0`–`3.15.0`; C-2 `GAP=1` (Plan 116); C-3 `GAP=4` (155/158/168/169); `check_plan_structure` `GAP=2` (157/158).
6. **Negativos evaluados:** N-1…N-8 con su evidencia.
7. **CHANGELOG sin corrupción:** guard N-9 y `git diff -U0 -- CHANGELOG.md` con un único hunk en `[Unreleased]`.

## Verificación

### Taxonomía

| Categoría | Miembros exactos | Qué prueba | Qué no prueba |
|---|---|---|---|
| Repository checkers (7) | `check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `check_invariants_equivalence` | Invariantes estructurales/documentales | Verdad semántica ni completitud |
| Lifecycle checks (3) | C-1 `check_lifecycle_anchor`, C-2 `check_lifecycle_checkpoint`, C-3 `check_lifecycle_lineage` | Presencia/forma/consistencia de anchors, checkpoints y lineage | Verdad del contenido validado |
| Tests (2 legs) | `pytest tests/`; `pytest protocol/.agents/harness/tests/` | Comportamiento especificado | Propiedades no cubiertas |
| Auxiliary | `git diff --check`, `git diff --name-only`, `git status`, `git diff -U0 -- CHANGELOG.md` | Limpieza, scope y N-9 | Corrección del contenido |

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
git diff --name-only 0bcce23..HEAD
git status --porcelain=v2 --branch
git diff -U0 -- CHANGELOG.md
```

### Guard N-9 de `CHANGELOG.md`

El guard es una verificación del Change, no un checker nuevo. Se ejecuta con el baseline `0bcce23` y el working tree como estado nuevo:

```powershell
@'
import subprocess, re

BASE = "0bcce23"
OLD = subprocess.check_output(["git", "show", f"{BASE}:CHANGELOG.md"], text=True, encoding="utf-8").splitlines()
NEW = open("CHANGELOG.md", encoding="utf-8").read().splitlines()

def region(lines):
    u = next((i for i, l in enumerate(lines) if l.strip() == "## [Unreleased]"), None)
    if u is None:
        raise SystemExit("N-9 FAIL: no [Unreleased] heading")
    nxt = [i for i, l in enumerate(lines) if i > u and l.startswith("## [")]
    if not nxt:
        raise SystemExit("N-9 FAIL: no historical release heading after [Unreleased]")
    return u + 1, nxt[0]

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

## Validation anchor

**Validation anchor (VC-1).**

- **Declared scope:** las trece rutas de la implementación: `CHANGELOG.md`, `docs/INVARIANTS.md`, `docs/VERSIONING.md`, `docs/adr/20-closed-artifact-governance-and-execution-records.md`, `docs/plans/INDEX.md`, `docs/working/proposals/INDEX.md`, `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md`, `runtime/orchestrator/governance.py`, `runtime/orchestrator/host.py`, `runtime/orchestrator/observation.py`, `tests/test_autonomous_orchestrator.py`, `tests/test_check_plan_citations.py` y `tools/check_plan_citations.py`. Este Plan queda **fuera** del scope medido: convención anti-auto-referencia.
- **Validation command-set:** los siete repository checkers de `docs/VERSIONING.md` §4.1; los tres lifecycle checks C-1/C-2/C-3; las dos legs de `pytest` (`tests/` y `protocol/.agents/harness/tests/`); `git diff --check`; el guard N-9 de `CHANGELOG.md`.
- **Effective inputs (repo content):** las trece rutas del scope; el baseline de ejecución `0bcce23`; el índice staged sobre el que se calculó la identidad; el inventario Phase 0.4; ADR-20/ADR-21/RFC-84.
- **Observed dependencies:** intérprete Python con biblioteca estándar (`tools/`, `runtime/`, `tests/`), `pytest`, CLI `git`. Sin red, sin servicios externos, sin instalación de componentes del payload.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; `pytest` 9.1.1; `git` 2.55; `core.autocrlf = true` (blobs LF, working tree puede materializarse CRLF); `check_dist_sync.py` no aplica (local-only; verde sólo en `master`); `check_plan_citations.py` conserva **25** citas históricas rotas y **0** referencias legacy falsas; `check_version_state.py` emite los 9 warnings históricos de versiones sin tag (esperados); `check_plan_structure.py` reporta los 2 `GAP` declarados de 157/158; C-2 el `GAP` del Plan 116; C-3 los cuatro `GAP` declarados (155/158/168/169).
- **Scoped Content Identity:**
  - **State identity:** T1 = `8be252568b2c77fae5e99f31cbb7132f41920390`.
  - **Delta scoped identity:** `785152b94df1f215aa409b60ba76738ca7abf18287bc2a0cc4f15873a63a16b1`.
  - **Scope set (repo-relative paths, ordenados):** las trece rutas del scope.
- **Validity / stale:** `vigente`. La transcripción de estos literales y del `## Checkpoint / cierre` es governance añadida al estado validado (convención anti-auto-referencia): el commit de cierre puede materializar un árbol distinto, y esa divergencia no es un requisito de C-2.
- **Battery result:** ver `## Nota de ejecución`.

## Checkpoint / cierre

**Checkpoint / cierre (GC-1).**

- **Commits de cierre:** el commit de cierre de este Plan en `dev`, que incorpora el inventario, las correcciones, este Plan, su Validation Anchor, este Checkpoint y el registro del Plan 172 en `docs/plans/INDEX.md`. Sin amend, rebase, squash ni force-push.
- **Estado validado (ref al Validation anchor):** State identity `8be252568b2c77fae5e99f31cbb7132f41920390`; Delta scoped identity `785152b94df1f215aa409b60ba76738ca7abf18287bc2a0cc4f15873a63a16b1`.
- **Estado de cierre (identidad):** State identity `8be252568b2c77fae5e99f31cbb7132f41920390`; Delta scoped identity `785152b94df1f215aa409b60ba76738ca7abf18287bc2a0cc4f15873a63a16b1` (el mismo estado validado, por correspondencia con el anchor aplicable).
- **Árbol material del commit de cierre:** no declarado; el commit aún no existe al escribir este checkpoint y añade governance sobre el estado validado. `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** **PASS** — el estado de cierre declarado es el que la validación consumió.
- **Governance aplicada:** RFC-56 Clase B (plan `Aprobado para ejecución`; sin payload); RFC-69 (registro en el INDEX, sin release); RFC-75 (Mecanismo 7, checkpoint); ADR-16 (autoridad del Change Lifecycle); ADR-20 (`E1-D2`…`E1-D4`); ADR-21; RFC-46 (no se reescribe historia); VC-1/GC-1/LC-1/PC-1.
- **Documentation impact:** `REQUIRED` — actualizados: inventario 0.4, `docs/plans/INDEX.md`, `docs/working/proposals/INDEX.md`, `docs/VERSIONING.md` §9, `docs/INVARIANTS.md`, ADR-20 (estado de implementación y Amendment Log) y `CHANGELOG.md` (`[Unreleased]`).
- **Roadmap impact:** `NOT_REQUIRED` — cerrar deuda heredada no crea, completa, cancela, reclasifica ni re-prioriza una iniciativa de dirección en `ROADMAP.md`.
- **Condición derivada:** **`Closed`** (plan `Executed` + governance aplicada + checkpoint + consistencia + PASS). `Committed` es estado del repositorio; `Released` requiere autoridad humana y no ocurre en este Change (docs-only/tooling, RFC-69).

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A.

### Correcciones

N/A — no hay correcciones registradas.

### Pending decisions

N/A — no hay pending decisions; el Plan fue ejecutado y su condición derivada es `Closed`.

## Riesgos

1. **Scope creep hacia `protocol/` o `dist/`.** Mitigación: `## Efectos declarados`, N-1, AC-8, `git diff --name-only`.
2. **Convertir la aceptación de riesgos en una garantía.** Mitigación: §C.1 del inventario declara qué no se garantiza, por qué, el impacto y el disparador de reapertura; ninguna entrada cambia su `ENFORCEMENT_STATUS`.
3. **Edición de artefactos cerrados.** Mitigación: las correcciones históricas van por referencia; ADR-20 sólo recibe estado de implementación y Amendment Log; `git diff` de planes/RFC cerrados vacío.
4. **Regresión del orquestador.** Mitigación: pruebas positivas y negativas; las 219 pruebas del host y de SAE existentes se ejecutan.
5. **Corrupción histórica del `CHANGELOG.md`.** Mitigación: N-9 + guard de diff; sólo `[Unreleased]`.
6. **Falso verde por confundir checkers con semántica.** Mitigación: taxonomía de verificación; el inventario no declara garantías semánticas.

## Trazabilidad

```text
contrato Phase 0.4 (instrucción del mantenedor)
        ↓
inventario PHASE_0_4_INHERITED_DEBT_CLOSURE (65 ítems, estado terminal)
        ↓
Plan 172 (este Plan) → E1-G2/G3/G4/G5 · checker de citas · registros derivados
        ↓
Validation anchor + Checkpoint → Executed → Closed (derivado) → commit en dev → promoción a master
```

## Nota de ejecución

**Ejecutado el 2026-10-20.** Change DEV Clase B, sin payload, conducido en `dev` bajo la instrucción del mantenedor registrada al inicio.

```text
PLAN_ID                  = 172
AUTHORIZATION            = MAINTAINER_AUTHORIZED_FOR_EXECUTION (Phase 0.4)
AUTHORITY_CLASS          = DEV_CLASS_B
EXECUTION_AUTHORIZED     = YES
RFC_REQUIRED             = NO
PROTOCOL_AUTHORITY       = UNCHANGED
EXECUTION_BASELINE_HEAD  = 0bcce23
```

### Resultados AC

| AC | Resultado | Evidencia |
|---|---|---|
| AC-1 | **PASS** | Inventario con 65 ítems y estado terminal por ítem; `UNCLASSIFIED = 0`. |
| AC-2 | **PASS** | Sólo los cinco estados canónicos aparecen como estado terminal. |
| AC-3 | **PASS** | `PlanWriteAuthority` + verificación en cada escritor; pruebas positivas y negativas. |
| AC-4 | **PASS** | Registro externo en `.project/orchestrator/plan-NNN/runs/`; referencia desde el plan; sin escritura sobre planes cerrados. |
| AC-5 | **PASS** | Cero construcciones `AuthorityBoundary(plan_authorized=True)` en producción (la única aparición del literal es la cita del ADR-20 en un docstring); toda construcción deriva de la observación. |
| AC-6 | **PASS** | `check_plan_citations`: 25 citas históricas + 0 legacy; sin editar cerrados. |
| AC-7 | **PASS** | INDEX 171, filas 0.2/0.3, §9 a `12.3.0`, INV-08, ADR-20. |
| AC-8 | **PASS** | Sin cambios en `protocol/`, `dist/` ni `runtime/` fuera del orquestador. |
| AC-9 | **PASS** | Sin ediciones al contenido gobernante de artefactos cerrados. |
| AC-10 | **PASS** | Batería completa; C-1/C-2/C-3 `ANOMALY=0`; ambas legs de tests verdes. |
| AC-11 | **PASS** | Ningún artefacto ni decisión de Phase 1. |

### Resultados N

| N | Resultado | Evidencia |
|---|---|---|
| N-1 | **PASS** | Diff sin `protocol/`, `dist/` ni `runtime/` fuera del orquestador. |
| N-2 | **PASS** | 0 invariantes, properties, gates, estados, registries, autoridades o garantías nuevas. |
| N-3 | **PASS** | Bloque canónico y copia Protocol intactos (`check_invariants_equivalence`: `IDENTICAL: YES`). |
| N-4 | **PASS** | 0 ediciones de contenido gobernante de planes/RFC/ADRs cerrados. |
| N-5 | **PASS** | R-01…R-11 y G-04/G-07/G-08 aceptados citando la instrucción del mantenedor; R-10/R-11 además por RFC-84/ADR-21. |
| N-6 | **PASS** | N-9 PASS; un único hunk en `[Unreleased]`. |
| N-7 | **PASS** | Staging por archivo; `.project/`, `PRIORITY.md` y el documento de planificación fuera del commit. |
| N-8 | **PASS** | Sin trabajo de Phase 1. |

### Comandos y resultados

- `check_protocol_invariants --payload protocol .`: **PASS** — 217 archivos, 10.537 referencias.
- `check_plan_citations`: **25** citas históricas rotas (baseline nuevo; antes 26) + **0** referencias legacy falsas (antes 1); sin citas nuevas del Plan 172. Exit 1 por el baseline histórico declarado, no por el Change.
- `check_plan_structure`: **PASS** — sin violaciones; 2 `GAP` advisory declarados (157/158, `status-index-gap`).
- `check_taxonomy_coherence`: **PASS**.
- `check_session_artifacts`: **PASS**.
- `check_version_state`: **PASS**; 9 warnings históricos de secciones sin tag (`3.7.0`–`3.15.0`), esperados.
- `check_invariants_equivalence`: **PASS** — bloque idéntico (`IDENTICAL: YES`); `ENFORCED=7/15`, `VALIDATED=2/15`, `NONE=6/15`.
- C-1 `check_lifecycle_anchor`: `VALID=78`, `GAP=0`, `ANOMALY=0`.
- C-2 `check_lifecycle_checkpoint`: `VALID=77`, `GAP=1` (Plan 116 legacy), `ANOMALY=0`.
- C-3 `check_lifecycle_lineage`: `VALID=37`, `GAP=4` (155/158/168/169 legacy), `N/A=32`, `BOUNDARY=1`, `ANOMALY=0`.
- `pytest tests/`: **1391 passed** (6:11).
- `pytest protocol/.agents/harness/tests/`: **204 passed, 1 skipped** (9,4 s).
- N-9 guard (contra `HEAD`): **PASS** — 1 hunk, dentro de `[Unreleased]`; secuencia de headings históricos idéntica.
- `git diff --check` y `git diff --cached --check`: limpios.

**Límite declarado:** los checkers verdes son evidencia estructural/documental; no prueban verdad semántica ni epistémica. `DETECT` sigue siendo `DETECT` y los riesgos aceptados siguen siendo límites reales.
