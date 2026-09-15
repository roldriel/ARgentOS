# Plan 124 — Cierre de los hallazgos accionables de arquitectura de `tests/`

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (un solo dominio —tooling— sin impacto arquitectónico ni de release)
**Depende de:** —
**Origen:** Revisión integral de arquitectura de `tests/` (read-only) sobre `dev` @ `4aa2617`; hallazgos F-01, F-02 y F-03.

## Objetivo

Cerrar los tres hallazgos accionables de la revisión de arquitectura de `tests/`
sin rediseñar el sistema de testing:

- **F-01** — establecer **un** mecanismo de importación coherente para las
  herramientas de primera parte, eliminando los `sys.path.insert` por archivo de
  test.
- **F-02** — corregir `tests/AGENTS.md` para que describa con precisión la
  distinción entre tests aislados (repositorio sintético) y tests anclados
  intencionalmente al repositorio real.
- **F-03** — centralizar la verificación «solo stdlib» hoy duplicada en siete
  archivos de test.

La revisión concluyó `KEEP + REFACTOR SELECTIVE`: la organización plana de
`tests/` es intencional y se conserva; `tests/fixtures/skills/` permanece donde
está; `.agents/skills/` no se crea; no se introduce split
`unit/`/`integration/`/`contract/`; DEV y Protocol permanecen separados.

## Criterio de entrada

- [x] `dev` limpio en `4aa2617` (verificado con `git status --short --branch` y `git rev-parse HEAD`).
- [x] Revisión de arquitectura de `tests/` completada con evidencia (hallazgos F-01/F-02/F-03).
- [x] Autorización del mantenedor para crear y ejecutar este plan (decisión registrada en la sesión de ejecución).
- [x] Confirmado que `tests/fixtures/skills/` es fixture (no canónico) y que no se mueve.

## Entregables

1. `tests/testsupport.py` (**nuevo**) — helper acotado que materializa el chequeo
   «solo stdlib» para una herramienta de `tools/`.
2. `conftest.py` — bootstrap único de importación de `tools/` para la sesión DEV.
3. Los siete archivos de test que hoy duplican el chequeo, sin la copia local.
4. Los archivos de test que hoy hacen `sys.path.insert(..., "tools")`, sin ese insert.
5. `tests/AGENTS.md` — distinción normativa aislado vs. repositorio real.
6. `docs/plans/INDEX.md` — registro de este plan (tabla + serie) y encabezado de estado.

## Pasos

1. **F-03 — helper de chequeo stdlib.** Crear `tests/testsupport.py` con una
   función `assert_tool_imports_only_stdlib(tool_path: Path, local_modules: Iterable[str] = ())`
   que parsee `tool_path` con `ast` (sin importar el módulo, para no depender de
   `sys.path`) y falle con `AssertionError` si algún módulo importado no es de la
   stdlib ni está declarado como local.
2. **F-03 — reemplazo en los siete archivos.** En cada uno, sustituir el bloque
   local por una llamada al helper conservando el nombre del test y el conjunto
   `local_modules` propio del archivo (incluido el conjunto **vacío** de
   `tests/test_check_lifecycle_lineage.py`, que es la aserción más estricta).
3. **F-01 — bootstrap único.** En `conftest.py`, añadir el directorio `tools/` a
   `sys.path` una sola vez a nivel de módulo, junto al `tests/` que ya inserta,
   documentando por qué se usa bootstrap y no un paquete.
4. **F-01 — eliminar inserts por archivo.** Retirar el
   `sys.path.insert(0, ... / "tools")` de los archivos que lo hacían cuando el
   bootstrap del paso 3 ya lo garantiza.
5. **F-02 — documentación.** Reescribir las reglas de `tests/AGENTS.md` para
   distinguir: (a) tests aislados con repositorio sintético en `tmp_path`;
   (b) tests anclados intencionalmente al repositorio real (incluido el dogfood
   sobre `protocol/`), con su contrato de estabilidad y la exigencia de ser
   estrictamente read-only.
6. **Verificación** según la sección homónima, incluida la falsificación exigida.

## Criterios de salida

- [x] F-01: un único mecanismo de importación de `tools/` en la sesión de test; ningún `sys.path.insert` por archivo apuntando a `tools/`.
- [x] F-01: ejecución directa por CLI de las herramientas afectadas intacta.
- [x] F-02: `tests/AGENTS.md` distingue explícitamente tests aislados de tests sobre el repositorio real y no afirma que todos sean autocontenidos.
- [x] F-02: ningún test del repositorio real fue eliminado, debilitado ni convertido en sintético.
- [x] F-03: el chequeo «solo stdlib» existe una sola vez; los siete casos previos siguen cubiertos con su aserción específica.
- [x] `tests/fixtures/skills/` sin cambios de ubicación ni de contenido.
- [x] `.agents/skills/` no existe.
- [x] `tests/` permanece plano; sin directorios `unit/`/`integration/`/`contract/`.
- [x] Sin cambios en `protocol/`; sin dependencias nuevas de producción hacia `tests/`.
- [x] Ningún temporal de pytest dentro del repositorio.
- [x] Batería canónica y `python -m pytest tests/` registrados con su resultado real.

## Verificación

Batería canónica (`docs/VERSIONING.md` §4.1) más las invocaciones relevantes al
cambio:

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python -m pytest tests/ -k stdlib          # los siete casos consolidados (F-03)
python tools/scoped_content_identity.py <scope>   # identidades del anchor
python -m mypy tests/ --no-incremental --cache-dir nul   # evidencia de F-01
python -m ruff check tests/ --no-cache                   # evidencia de lint
```

Ejecución directa por CLI de las herramientas afectadas por F-01:

```bash
python tools/check_plan_citations.py
python tools/check_architecture_traceability.py --help
python tools/determine_execution_state.py --help
```

Juicio manual: la distinción documental de F-02 debe corresponder a
comportamiento observable de los tests (al menos un test aislado y al menos un
test anclado al repositorio real identificados por `ruta:sección`).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** el cambio del Plan 124: `conftest.py`, `docs/plans/124-tests-architecture-findings.md`, `docs/plans/INDEX.md`, `tests/AGENTS.md`, `tests/testsupport.py` y los 18 archivos de test que portaban el bootstrap de `tools/` (`tests/test_aggregate_metrics.py`, `tests/test_audit_gates.py`, `tests/test_check_architecture_traceability.py`, `tests/test_check_dist_sync.py`, `tests/test_check_lifecycle_anchor.py`, `tests/test_check_lifecycle_checkpoint.py`, `tests/test_check_lifecycle_lineage.py`, `tests/test_check_plan_citations.py`, `tests/test_check_plan_structure.py`, `tests/test_check_protocol_invariants.py`, `tests/test_check_session_artifacts.py`, `tests/test_check_taxonomy_coherence.py`, `tests/test_check_version_state.py`, `tests/test_determine_execution_state.py`, `tests/test_legacy_paths.py`, `tests/test_measure_context_budget.py`, `tests/test_repo_containment.py`, `tests/test_scoped_content_identity.py`). Total 23 paths.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python -m pytest tests/`; `python -m pytest tests/ -k stdlib`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`.
- **Effective inputs (repo content):** el scope declarado (23 paths) más `docs/plans/` completo y `protocol/.agents/` consumidos por los checkers canónicos y por los tests anclados al repositorio real.
- **Observed dependencies:** `git` (identidad de contenido, `ls-files`, repositorios desechables de las suites); `python` (intérprete de los checkers y de la suite); el resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.3; pytest 9.0.3; mypy 1.19.1; ruff 0.15.17; sin red. **Clase ambiental declarada para `python -m pytest tests/`:** la pierna completa de la suite no es verificable en el entorno de ejecución de este agente. El sandbox no permite crear directorios bajo el padre del temporal de plataforma y `tests/pytest_isolation.py` —correctamente— rechaza un root temporal dentro del repositorio, de modo que la corrida con `ARGENTOS_PYTEST_TMP` apuntando fuera del repo produce **3 failed / 324 passed / 457 errors**. Los 457 `errors` son `PermissionError [WinError 5]` al crear `pytest-of-<user>`/`pytest-cache-files-*` (mecánica de temporales de pytest) y los 3 `failed` son de la misma clase (los tests `test_non_git_root_content_not_applicable`, `test_tmp_path_basetemp_is_outside_the_repository` y `test_pytest_cache_is_outside_the_repository`). Una corrida previa, antes de registrar los findings y correcciones de este plan, daba 4 `failed`: el cuarto era el dogfooding C-3 `t27` de `tests/test_check_lifecycle_lineage.py`, que registraba `GAP=1` por el propio Plan 124 sin registros y pasó a verde al registrarlos (`GAP=0`), confirmando que era una consecuencia esperada del artifact y no un defecto del producto. El resultado de la pierna completa se clasifica **GAP** (ausencia de evidencia obtenible en este entorno), nunca `PASS`; se declara y **no** se reinterpreta como defecto del producto. Los subconjuntos exigibles corren por separado y en verde. Es la misma clase ambiental que declararon los Planes 121, 122 y 123.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** T1 = `23317bc2a0ccf9a276620c7c9092b8878402be1c`.
  - **Delta scoped identity (scope S = los 23 paths del cambio, ordenados; serialización `scoped-v1`):** `64810a6126fdb3158802b7e78baad266b373624c73291b1bf2329308a6587745`.
  - **State identity (A2 de A1, estado revalidado = estado de cierre):** T2 = `23317bc2a0ccf9a276620c7c9092b8878402be1c`.
  - **Revalidación (A2 de A1):** V2 re-ejecutó el mismo contrato sobre el estado de cierre (`23317bc2a0ccf9a276620c7c9092b8878402be1c`); A1 permanece como registro histórico y no se muta ni se reinterpreta.
- **Validity / stale:** `vigente`; revalidada por A2 sobre el estado de cierre.

*Resultado real de la ejecución:* verification-01: PASS (exit 0, 215 files / 10227 references); verification-02: PASS (exit 0); verification-03: PASS (exit 0); verification-04: PASS (exit 0); verification-05: PASS (exit 0); verification-06: PASS (exit 0, con warnings de tags esperados en `dev`); verification-07 declarada (clase ambiental de temporales; 3 failed / 324 passed / 457 errors, ver arriba); verification-08 (`-k stdlib`): PASS (7 passed); C-1: `N/A` al validar (anchor sin registrar aún), `VALID` sobre el árbol final; C-2: `N/A` al validar (checkpoint sin registrar aún), `VALID` sobre el árbol final; C-3: `GAP=1` al validar (el propio Plan 124 sin registros), `VALID` con `GAP=0` sobre el árbol final.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio autorizada por el mantenedor en esta ejecución: `fix(tests): consolidate tools imports and stdlib checks (plan 124)`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `64810a6126fdb3158802b7e78baad266b373624c73291b1bf2329308a6587745`, tree `23317bc2a0ccf9a276620c7c9092b8878402be1c`.
- **Estado de cierre (tree id):** `23317bc2a0ccf9a276620c7c9092b8878402be1c` — el árbol del índice que la validación A1 consumió, con el scope declarado (23 paths) y este registro de cierre. Difieren **sólo** en los registros de gobernanza que el propio cierre escribe en este artifact (el `## Validation anchor`, este `## Checkpoint / cierre`, la `## Nota de ejecución` y los registros de findings/correcciones); la delta scoped identity de S es estable y reproducible: editar el artifact de gobernanza en sus registros de cierre no cambia ningún blob de S. La diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120 y 123) y es verificable con `git rev-parse HEAD^{tree}` tras el commit.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por A1 aplicable (mismo tree id); la consistencia se verificó con C-2 sobre el árbol final.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 124 (tabla + serie, Quincuagésima sexta) y su encabezado de estado; `## Validation anchor` registrado; findings `F-1`..`F-3` y correcciones `C-1`..`C-3` registrados; `**Status:** Executed`; `## Nota de ejecución` registra los comandos y resultados reales.
- **Documentation impact (§5.1):** **REQUIRED** — documentos afectados: `tests/AGENTS.md` (aspecto: describía la suite como enteramente autocontenida y `sys.path` por archivo; actualización: distinción normativa tests aislados vs. tests anclados al repositorio real, tabla de los ocho casos, contrato de estabilidad, excepción del dogfood y regla de bootstrap único; evidencia: `python -m pytest tests/ -k stdlib` 7 passed y `grep` de los cinco nombres de test citados) y `docs/plans/INDEX.md` (aspecto: registro del plan y encabezado de estado; actualización: fila del Plan 124 + serie Quincuagésima sexta + encabezado; evidencia: `python tools/check_plan_structure.py` exit 0). El cambio no altera el modelo conceptual de `tests/` descrito en el `AGENTS.md` raíz (`## Repository layout`): `tests/` sigue siendo «centralized test suites for `tools/` and `runtime/`» que nunca dependen del payload salvo el dogfood declarado, por lo que no se requiere edición adicional de documentos de estado actual.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS; `Committed` es estado del repositorio y `Released` requiere autoridad humana. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-124>:F-1` — estado: `resolved`; observación: `tools/` no es un paquete importable y 18 archivos de test compensaban con el mismo bootstrap duplicado de `sys.path` hacia `tools/` (17 con `REPO_ROOT / "tools"` y uno con `Path(__file__).resolve().parents[1] / "tools"`); evidencia original: revisión de arquitectura de `tests/` sobre `4aa2617` (18 coincidencias de `sys.path.insert` hacia `tools/`); resolución: bootstrap único en `conftest.py` y eliminación de los 18 inserts, manteniendo `tools/` como directorio de scripts ejecutables; estado Git observado: `dev` @ `4aa2617`, working tree limpio; provenance original: revisión read-only de `tests/`.
- `<PLAN-124>:F-2` — estado: `resolved`; observación: `tests/AGENTS.md` afirmaba que los tests son autocontenidos y basados en repositorios falsos, cuando ocho tests dependen intencionalmente del repositorio real o del payload real, y el dogfood sobre `protocol/` contradecía literalmente la regla «un cambio en el payload nunca debe romper un test aquí»; evidencia original: revisión de arquitectura de `tests/` sobre `4aa2617`; resolución: `tests/AGENTS.md` distingue normativamente tests aislados de tests anclados al repositorio real, enumera los ocho casos con lo que protege cada uno, declara su contrato de estabilidad y nombra la excepción deliberada del dogfood, sin eliminar, debilitar ni convertir ningún test; estado Git observado: `dev` @ `4aa2617`, working tree limpio; provenance original: revisión read-only de `tests/`.
- `<PLAN-124>:F-3` — estado: `resolved`; observación: el test «solo stdlib» estaba duplicado en siete archivos con lógica idéntica, difiriendo sólo en el conjunto de módulos locales declarados; evidencia original: revisión de arquitectura de `tests/` sobre `4aa2617`; resolución: helper acotado en `tests/testsupport.py` (`assert_tool_imports_only_stdlib`, con `tool_path` y `local_modules` como parámetros) que parsea con `ast` (independiente de `sys.path`) y conserva el conjunto local de cada caso, incluido el conjunto vacío del test t28 de `tests/test_check_lifecycle_lineage.py`; los siete nombres de test se conservan; estado Git observado: `dev` @ `4aa2617`, working tree limpio; provenance original: revisión read-only de `tests/`.

### Correcciones

- `<PLAN-124>:C-1` — refs origen: `<PLAN-124>:F-1`; alcance de revalidación: `conftest.py` y los 18 archivos de test que portaban el bootstrap de `tools/`; evidencia (Git/commit/estado): diff del scope con bootstrap único en `conftest.py` (revisión C-1 `vigente`, `GAP=0`); `grep` de `sys.path.insert` hacia `tools/` en `tests/` = 0 coincidencias; falsificación: sin bootstrap la importación falla (`ModuleNotFoundError: No module named 'check_plan_citations'`) y con `conftest.py` ejecutado resuelven `check_plan_citations`, `legacy_paths`, `scoped_content_identity`, `check_lifecycle_anchor`, `check_dist_sync` y `testsupport`; ejecución directa por CLI verificada (exit 0 en las tres herramientas con imports internos planos); el commit de cierre atómico en `dev` se identifica por su mensaje.
- `<PLAN-124>:C-2` — refs origen: `<PLAN-124>:F-2`; alcance de revalidación: `tests/AGENTS.md`; evidencia (Git/commit/estado): diff del scope con el documento reescrito (revisión C-1 `vigente`, `GAP=0`); los cinco nombres de test citados en la tabla se verificaron existentes en el árbol; el commit de cierre atómico en `dev` se identifica por su mensaje.
- `<PLAN-124>:C-3` — refs origen: `<PLAN-124>:F-3`; alcance de revalidación: las siete suites de checkers y el helper nuevo `tests/testsupport.py`; evidencia (Git/commit/estado): `python -m pytest tests/ -k stdlib` → 7 passed (revisión C-1 `vigente`, `GAP=0`); los siete call sites conservan su conjunto local propio, incluido el vacío de lineage; el commit de cierre atómico en `dev` se identifica por su mensaje.

Los tres hallazgos quedan `resolved` como **propuesta del agente**; la resolución formal de un finding es decisión humana (ADR-16 AU-3).

### Pending decisions

- `<PLAN-124>:PC-1` — decisión: si conviene declarar la ruta de importación de `tools/` para el type checker (p. ej. `MYPYPATH=tools` o un `mypy_path` en configuración), dado que la corrección de F-01 no elimina los errores `import-not-found` de mypy; blocking: no; owner: mantenedor; escalación: sólo si mypy pasa a ser parte de la batería canónica; resolución: pendiente; evidencia: con mypy sin ruta declarada `mypy tests/` reporta **49 errores en 23 archivos** (29 `arg-type`, 19 `import-not-found`, 1 `assignment`, 1 `annotation-unchecked`); con `MYPYPATH` apuntando a `tools/` los `import-not-found` caen a **0** y el total a **42 errores en 10 archivos**, lo que demuestra que los 19 son un artefacto de configuración de la herramienta y no un defecto del producto. Ni `mypy` ni `ruff` son hoy parte de la batería canónica: no hay configuración ni invocación en CI (`docs/VERSIONING.md` §4.1 y `.github/workflows/check-protocol.yml` no los mencionan), por lo que introducir esa configuración queda fuera del alcance de este plan.
- `<PLAN-124>:PC-2` — decisión: si `tools/` debe convertirse en paquete Python en el futuro; blocking: no; owner: mantenedor; escalación: sólo si un cambio futuro requiere importación estilo paquete; resolución: pendiente; evidencia: el prototipo muestra que con `tools/__init__.py` presente la importación estilo paquete de `check_plan_citations`/`check_architecture_traceability` falla con `ModuleNotFoundError: No module named 'legacy_paths'`, mientras que la ejecución como script y la importación plana siguen funcionando; convertir `tools/` en paquete obligaría a reescribir los imports internos de tres herramientas, los 18 imports de test y el contrato `PYTHONPATH=tools` de `tests/test_scoped_content_identity.py`, creando doble identidad de módulo (`legacy_paths` y `tools.legacy_paths`).

## Riesgos

- **Cambiar imports de `tools/` de forma accidental.** Mitigación: no se toca ningún archivo de `tools/`; el bootstrap mantiene el layout plano existente.
- **Perder cobertura en F-03.** Mitigación: conservar nombre de test y conjunto `local_modules` por archivo, incluido el conjunto vacío de lineage; verificar por colección que los siete casos siguen existiendo.
- **Debilitar F-02 convirtiendo tests reales en sintéticos.** Mitigación: criterio de salida explícito de no eliminación ni debilitamiento.

## Trazabilidad

Revisión de arquitectura de `tests/` (read-only, `dev` @ `4aa2617`) → este plan →
`tests/testsupport.py`, `conftest.py`, siete suites de checkers, `tests/AGENTS.md`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `4aa2617`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica completa: los seis checkers
canónicos en verde (`check_protocol_invariants` 215 files / 10227 references;
`check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`,
`check_session_artifacts`, `check_version_state` exit 0). Gates de lifecycle
sobre el árbol final: **C-1 `VALID`, C-2 `VALID` (GC-1: A1), C-3 `VALID`**
(lineage `F-1`..`F-3` + `C-1`..`C-3`), con `GAP=0` en el corpus para C-1 y C-3.
`python -m pytest tests/ -k stdlib` → **7 passed**. `python -m pytest tests/` →
**3 failed / 324 passed / 457 errors**: los 457 `errors` y los 3 `failed` son de
la clase ambiental declarada (mecánica de temporales de pytest en este sandbox:
`test_non_git_root_content_not_applicable`,
`test_tmp_path_basetemp_is_outside_the_repository`,
`test_pytest_cache_is_outside_the_repository`), sin relación con el cambio. La
corrida anterior a la clausura del propio Plan 124 daba 4 `failed`; el cuarto
(el dogfooding C-3 `t27`) pasó a verde al registrarse los findings y
correcciones de este plan, confirmando que era consecuencia esperada del
artifact y no un defecto. `mypy tests/` → 49 errores (42 preexistentes de tipo
`arg-type`/`assignment`; los 19 `import-not-found` caen a 0 declarando
`MYPYPATH=tools`, ver pending decision). `ruff check tests/` → 7 errores
preexistentes sin cambios respecto del baseline en archivos fuera del scope.
Ejecución directa por CLI de las tres herramientas con imports internos planos
verificada (exit 0).

**Resultado.** F-01, F-02 y F-03 corregidos. El alcance se mantuvo en 23 paths;
las correcciones automáticas de `F401` en cuatro archivos fuera del scope
(`test_autonomous_orchestrator.py`, `test_canonical_materialization_v2.py`,
`test_prompt_cache_dogfood.py`, `test_toolcalls.py`) se **revirtieron** por
disciplina de alcance y quedan como deuda preexistente registrada.

**Incumplido / no verificado.** La pierna completa de `python -m pytest tests/`
no es verificable en el entorno de este agente (clase ambiental declarada, ver
`## Validation anchor`); se registra como GAP y nunca como PASS. La resolución
formal de los hallazgos es decisión humana y queda como propuesta.
