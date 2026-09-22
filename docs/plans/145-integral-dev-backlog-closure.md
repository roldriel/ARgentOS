# Plan 145 — Cierre integral del backlog accionable DEV I-1…I-8 (Integral Closure of the Actionable DEV Backlog)

**Status:** Executed (2026-09-21; implementación y validación completadas, condición derivada `Closed` — docs-only + tooling DEV, sin release; ver `## Checkpoint / cierre`)
**Fecha:** 2026-09-21
**RFC:** — (vía plan; DEV-only sobre `tests/`, `runtime/`, `conftest.py`, `docs/`, `.agents/policies/` y `CHANGELOG.md`, sin efecto en `protocol/.agents/`, por lo que RFC-56 no aplica)
**Clase:** — (sin efecto de payload; ningún archivo de `protocol/.agents/` se toca)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural=1, release=0, duration=1)`: una única autorización y un único Change integral con dieciocho rutas repartidas en cuatro capas —el harness de tests, el runtime DEV de referencia, tres artefactos de gobernanza y la documentación current-state—; el impacto arquitectónico es 1 porque `observation.py` y `autonomy.py` cambian una política de lectura y una semántica de métrica **dentro del runtime DEV**, no el modelo ni un contrato del payload; sin release y sin tag)
**Depende de:** plan 144 (inventario global posterior del que salen `I-1`…`I-8`), plan 143 (estado del backlog operativo), plan 141 (ejecución del Plan 137 y precedente de transición de metadata evolucionable), plan 131 (implementación del Placement Contract), plan 135 y plan 138 (SAE y su frontera de Scope/Authority), plan 124 (`tests/AGENTS.md` y el bootstrap de importación)
**Origen:** pedido directo del mantenedor (Change «Plan 145 — Cierre Integral del Backlog Accionable DEV I-1…I-8», 2026-09-21), que autoriza crear y ejecutar este Plan como una única Change integral y resolver en la misma iteración los ocho items accionables que el inventario global posterior al Plan 144 identificó

## Objetivo

Cerrar integralmente el backlog accionable DEV `I-1`…`I-8` en un único Change, corrigiendo la **causa** de cada item —no su síntoma—, con regresión y falsación por item, y dejando el repositorio en un estado coherente y verificable.

El objetivo no es marcar ocho casillas. Para cada item este Plan inspecciona el artefacto real, determina la causa, corrige la causa, agrega la regresión correspondiente, la falsifica contra la implementación anterior, ejecuta la verificación aplicable, preserva la evidencia histórica y actualiza los espejos y la documentación current-state afectados. Donde no hay frontera real de autoridad, **resuelve**; no inventa un `DEFERRED` para evitar el trabajo.

## Problema

El inventario read-only posterior al Plan 144 dejó ocho items accionables. Tres de ellos son defectos reales ya observados, no inconsistencias documentales:

1. **La suite no es determinista.** `conftest.py` limpiaba un scratch root **compartido** (`<TEMP>/argentos-pytest/scratch`) al inicio de **cada** sesión, de modo que una segunda sesión pytest destruía los repositorios desechables que otra sesión todavía estaba usando. En siete corridas completas de `python -m pytest tests/`, cuatro fallaron —cada una en un test **distinto**: `test_host_with_the_gate_on_conducts_authorized_work_without_a_handoff` (`assert record["autonomy"] is not None`), `test_full_loop_derives_closed_from_real_evidence` (una vez `STOP_PLAN_NOT_FOUND` y otra `STOP_FORBIDDEN_ACTION`) y el dogfood de `test_sae_scope_enforcement.py` (`FileNotFoundError` sobre un `docs/plans/901-sae-enforcement.md` que el propio test acababa de escribir). Una limpieza de temporales del sistema operativo durante una corrida tiene el mismo efecto. Además, `_run_git` convertía cualquier `OSError` o salida no-cero en `None`, de modo que un recurso vital perdido se leía como «no existe».
2. **La métrica `recoveries` contaba conducción ordinaria como recuperación.** `_RECOVERY_ACTIONS` incluía `RUN_IMPLEMENTATION_TASK` y `RUN_LIFECYCLE_GATES`, que son pasos normales del flujo: una corrida completamente autónoma que terminaba en `CLOSED_DERIVED` con **cero** stops reportaba `Recoveries: 3`.
3. **`findings_autonomously_corrected` era una constante presentada como valor derivado.** `summarize_autonomy` pasaba `0` literal mientras `findings_corrected_autonomously` —la función que sí sabía derivarlo— no era llamada por ningún módulo del runtime, y `runtime/README.md` y la policy §11 afirmaban que el resumen se deriva del journal y de los Worker Results.

Los cinco items restantes son la deriva que los tres anteriores ayudaron a ocultar: dos headers de Plan ejecutados que seguían declarando `Aprobado para ejecución`, la fila del Plan 137 en el INDEX y su autodescripción contradictoria, las filas `B-4`/`B-7` del backlog evidenciado que seguían presentando como abierto lo que la RFC-79 y el Plan 142 materializaron, la afirmación del Placement Contract de que el enforcement «no existe» contra `runtime/placement/` implementado desde el Plan 131, y la ausencia de `test_placement_contract_drift.py` en el conjunto anclado que `tests/AGENTS.md` declara.

## Criterio de entrada

- [x] `**Status:**` inicial de este Plan es `Aprobado para ejecución`: la autorización del mantenedor es explícita, integral y previa a la ejecución.
- [x] Cada `I-N` fue reconstruido desde el repositorio real (no desde el inventario) antes de escribir código: causa, evidencia y artefacto afectado observados en el árbol.
- [x] Los tres defectos de runtime se reprodujeron: la no-determinancia de la suite, el `Recoveries: 3` de una corrida sin stops y el `findings_autonomously_corrected = 0` constante.
- [x] Baseline del repositorio identificable: `dev @ a90e50753d09c922178f436932e1c713d49be57f`, working tree limpio salvo el artefacto externo untracked `MASTER_PENDING_WORK_INVENTORY.md`.
- [x] Autoridad válida: la del propio Plan aprobado; sin RFC/ADR requerido y sin cambio de payload involucrado.
- [x] Batería canónica en verde en el baseline (seis checkers PASS, C-1 `GAP=0`, C-3 `GAP=0`, `ANOMALY=0`).
- [x] Sin pending decision bloqueante para la ejecución (`<PLAN-125>:PC-1`/`PC-2`, `<PLAN-137>:PC-2`, `<PLAN-131>:PC-1`/`PC-2`, `<PLAN-138>:PC-2` no bloquean este Change).

## Entregables

1. `docs/plans/145-integral-dev-backlog-closure.md` — este Plan, con la matriz de resolución, los anclajes, el checkpoint y los registros de lineage.
2. `tests/pytest_isolation.py` — scratch root **por sesión**: token declarado, limpieza de lo propio y poda acotada por edad.
3. `conftest.py` — declara el token de sesión en import time, limpia sólo el scratch propio y reporta la sesión y la poda en el header.
4. `tests/test_pytest_isolation.py` — regresiones de `I-1` (secciones 5 y 6).
5. `runtime/orchestrator/observation.py` — `GitState.git_available` y `observe()` que falla ruidosamente ante un recurso vital ilegible.
6. `tests/test_autonomous_orchestrator.py` — regresiones de la frontera de observación (`I-1`).
7. `runtime/orchestrator/autonomy.py` — semántica correcta de `recoveries` y derivación real de `findings_autonomously_corrected`.
8. `tests/test_autonomous_scope.py` — regresiones de `I-7` e `I-8` (secciones 15 y 16).
9. `runtime/README.md` — la frontera de observación y las dos reglas de métrica, en la documentación current-state del runtime.
10. `.agents/policies/supervised-autonomous-execution.md` — §11 con la semántica estrecha de `recoveries` y `findings_autonomously_corrected`.
11. `docs/plans/143-empty-remaining-backlog.md` y `docs/plans/144-dev-documentation-test-hygiene.md` — headers al estado corriente `Executed`.
12. `docs/plans/137-ears-structural-validator.md` — autodescripción corriente reconciliada, con la nota de reconciliación del `## Criterio de entrada`.
13. `docs/plans/INDEX.md` — fila y serie del Plan 137, registro del Plan 145, reconciliación de `## Backlog evidenciado - plan 19` y de las dos narraciones de estado superadas.
14. `docs/placement-contract.md` — `PC-72.1` (estado corriente del enforcement autorizado) y §23/§24 precisadas.
15. `tests/AGENTS.md` — conjunto anclado completo (14 filas) y la regla de scratch por sesión.
16. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 145, RFC-—)`.

## Matriz de resolución (resultado observado)

| Item | Causa observada en el repositorio | Corrección | Falsación |
|---|---|---|---|
| `I-1` | el `pytest_configure` de `conftest.py` hacía `rmtree` del scratch **compartido** en cada inicio de sesión; `_run_git`/`git_state` colapsaban «no pude leerlo» con «no existe» | token de sesión declarado; `scratch_root` por sesión; `clear_own_scratch`; `prune_stale_sessions` por edad; `GitState.git_available` y `observe()` que eleva `ObservationError` | 12 regresiones nuevas fallan contra la implementación anterior y pasan contra la nueva; 127 tests de las suites SAE corrieron sin interferencia mientras tres sesiones concurrentes arrancaban |
| `I-2` | el header nunca se transicionó tras la ejecución; el checker de estructura valida el valor de status, no su acuerdo con el espejo | transición a `Executed` con la fecha y la referencia al Plan 145 | el checker `check_plan_structure.py` no detectaba la divergencia: la evidencia de la corrección es la comparación header↔fila del INDEX, verificada en el árbol |
| `I-3` | fila stale `Aprobado para redacción` en el INDEX, título de serie «preparación» y §35 del Plan declarando que no estaba autorizado a ejecutarse | fila a `Executed`, serie sin «preparación», §35 reemplazado por la nota de estado corriente y `## Criterio de entrada` con nota de reconciliación | no queda ninguna fila de plan con status no terminal en el INDEX (verificado por barrido) |
| `I-4` | el párrafo de resolución del backlog evidenciado cerraba `B-4`/`B-7`/`B-8` en la Sexta serie (planes 37-58) y **no** nombraba la RFC-79 ni el Plan 142, que fueron quienes materializaron esos residuos | banner de registro histórico + filas `B-4`/`B-7`/`B-8` anotadas como resueltas + párrafo de resolución corriente que nombra RFC-79 y Plan 142 (11.6.0) | `ROADMAP.md:## Pendientes que requieren autorización` ya declaraba los tres resueltos: la divergencia era verificable contra una fuente normativa existente |
| `I-5` | §22/§23/§24 afirmaban que el enforcement «no está implementado» y que «no existe resolver», contra `runtime/placement/` existente desde el Plan 131 | `PC-72.1` describe el estado real con sus tres calificaciones (librería, no integrada, advisory) y §23/§24 distinguen «enforcement como obligación operativa» de «realización mecánica de la tabla de reglas» | `test_placement_contract_drift.py` falló cuando una edición introdujo un par de backticks vacío: la guarda lee el contrato real y detecta el drift |
| `I-6` | `tests/AGENTS.md` declaraba 13 filas omitiendo `test_placement_contract_drift.py`, que lee el contrato real en seis puntos | fila agregada con lo que protege; la fila de `test_pytest_isolation.py` precisa la propiedad de propiedad de sesión | barrido de módulos que derivan `REPO_ROOT` y leen de él: el módulo omitido es el único lector real ausente de la tabla |
| `I-7` | `_RECOVERY_ACTIONS` incluía `RUN_IMPLEMENTATION_TASK` y `RUN_LIFECYCLE_GATES`, pasos ordinarios del flujo | `_RECOVERY_ACTIONS = {RUN_REVALIDATION}`, con la razón declarada: `RUN_REVALIDATION` es la rama de recuperación de la derivación (anchor A1 stale) | 5 regresiones nuevas fallan contra la implementación anterior; corrida real por el host pasa de `Recoveries: 3` a `Recoveries: 0` |
| `I-8` | `findings_autonomously_corrected=0` literal, con `findings_corrected_autonomously` sin llamadores en el runtime | derivación desde los registros `RECORD_FINDING_CORRECTION` del journal bajo la regla anti-fabricación existente, con la frontera declarada en una nota del resumen | 5 regresiones nuevas fallan contra la implementación anterior (todas leían `0`); el conteo ahora responde a la evidencia |

## Pasos

1. **Observar el estado real (read-only).** Reconstruir cada `I-1`…`I-8` desde el árbol: `git status`, HEAD, `protocol/.agents/VERSION`, headers de los planes 137/143/144, filas del INDEX, `docs/placement-contract.md` §22-§24, `tests/AGENTS.md`, `runtime/orchestrator/{observation,autonomy}.py`, `tests/pytest_isolation.py` y `conftest.py`.
2. **`I-1` — aislamiento por sesión.** Reescribir `tests/pytest_isolation.py` con token declarado, `session_scratch_root`, `clear_own_scratch` y `prune_stale_sessions`; declarar el token en `conftest.py` antes de importar cualquier módulo de test, limpiar sólo lo propio y podar por edad.
3. **`I-1` — frontera de observación.** Agregar `GitState.git_available` y `git_available()`; elevar `ObservationError` cuando el CLI está disponible y el root existe pero el repositorio no se lee; conservar el `GAP` declarado para el CLI ausente; no convertir un `TimeoutExpired` en `None`.
4. **`I-7` — semántica de `recoveries`.** Reducir `_RECOVERY_ACTIONS` a `RUN_REVALIDATION` con la razón declarada en el código.
5. **`I-8` — derivación del conteo de correcciones.** Recolectar los registros `RECORD_FINDING_CORRECTION` del journal y contarlos con `findings_corrected_autonomously`; agregar la nota de frontera cuando el conteo es cero.
6. **`I-2`/`I-3`/`I-4` — reconciliación de registro.** Transicionar los headers 143/144; corregir fila, serie y autodescripción del Plan 137; reconciliar el backlog evidenciado con la RFC-79 y el Plan 142.
7. **`I-5`/`I-6` — contrato y conjunto anclado.** Registrar `PC-72.1` y precisar §23/§24; agregar la fila faltante al conjunto anclado y la regla de propiedad de sesión.
8. **Regresiones y falsación.** Agregar las regresiones por item y falsificarlas contra la implementación anterior.
9. **Verificar.** Correr las suites afectadas, la suite completa, el harness del payload, los seis checkers canónicos, C-1/C-2/C-3 y los checkers específicos de placement, taxonomía, EARS y D01; registrar anchor y checkpoint.
10. **Cerrar.** Registrar el Plan y su serie en `docs/plans/INDEX.md`, el ítem en `CHANGELOG.md`, las determinaciones de impacto, el anchor y el checkpoint; commit atómico en `dev`. Sin push, merge, tag, release ni promotion.

## Delegación agentiva

- **Task:** Ejecutar los Pasos 1–10 de este Plan: observar read-only los ocho items; corregir el aislamiento del pytest harness a un scratch root por sesión con token declarado y poda acotada por edad; corregir la frontera de observación del runtime DEV para que un recurso vital ilegible no se convierta en un estado indistinguible de «no existe»; corregir la semántica de `recoveries` y derivar `findings_autonomously_corrected` de la evidencia del journal; reconciliar los espejos documentales de los Planes 137/143/144, el backlog evidenciado `B-4`/`B-7`, el Placement Contract y el conjunto anclado de `tests/AGENTS.md` contra su fuente autoritativa sin reescribir evidencia histórica; agregar las regresiones de cada item y falsificarlas; verificar la batería completa, los gates C-1/C-2/C-3 y el 0 diff de los artefactos protegidos; registrar anchor y checkpoint; commit atómico en `dev`. **No** crear ningún mecanismo, policy, checker, estado, registry, authority class, taxonomía ni workflow nuevos; **no** modificar `protocol/.agents/`, `dist/`, `ROADMAP.md`, `docs/adr/` ni ningún artefacto cerrado fuera de la metadata evolucionable y los espejos declarados en el `## Scope`; **no** promover, taggear, publicar, empujar ni inventar evidencia.
- **Scope:** `tests/pytest_isolation.py`, `conftest.py`, `tests/test_pytest_isolation.py`, `runtime/orchestrator/observation.py`, `runtime/orchestrator/autonomy.py`, `tests/test_autonomous_orchestrator.py`, `tests/test_autonomous_scope.py`, `runtime/README.md`, `.agents/policies/supervised-autonomous-execution.md`, `tests/AGENTS.md`, `docs/placement-contract.md`, `docs/plans/137-ears-structural-validator.md`, `docs/plans/143-empty-remaining-backlog.md`, `docs/plans/144-dev-documentation-test-hygiene.md`, `docs/plans/INDEX.md`, `docs/plans/145-integral-dev-backlog-closure.md`, `CHANGELOG.md`

## SAE execution boundary

Este Plan declara `## Delegación agentiva` (sección aditiva-optional, regla operacional del Plan 123) y por lo tanto **habilita** al DEV Autonomous Orchestrator a conducir el trabajo semántico declarado bajo su frontera. El Agent Worker no adquiere autoridad propia: la autoridad es este Plan aprobado. Un cambio de `protocol/.agents/` está fuera del `Scope` y sigue su propia vía RFC-56; si la ejecución revelara esa necesidad, se registra como finding con su pending decision y se detiene.

## Human authority boundary

Release, promoción, tag, merge y push quedan **fuera** de este Plan y de la autoridad del agente (`FORBIDDEN`). El Plan cierra con condición derivada `Closed` sin release. Ninguna decisión humana se ejerce por inferencia: las pending decisions que este Plan no resuelve conservan su estado y su owner.

## Stop conditions

- Un cambio necesario fuera del `Scope` declarado: `STOP_SCOPE_VIOLATION`, registrar la necesidad y **no** ampliar el Scope.
- Una corrección que exija RFC `Accepted` o una decisión normativa nueva: registrar la pending decision y continuar con los items independientes.
- Un `ANOMALY` de gate o un `FAIL` de checker no explicado al cerrar: detener y reportar.
- Cualquier modificación de `protocol/.agents/`: frontera de payload, fuera de este Plan.

## Criterios de salida

- [x] `I-1`: corrección verificable (aislamiento por sesión + frontera de observación), con regresiones propias falsificadas contra la implementación anterior.
- [x] `I-2`: resuelto — headers 143/144 en `Executed`.
- [x] `I-3`: resuelto — fila, serie y autodescripción del Plan 137 reconciliadas.
- [x] `I-4`: resuelto — backlog evidenciado reconciliado con RFC-79 y Plan 142.
- [x] `I-5`: resuelto — Placement Contract al estado corriente, con la distinción implementado/integrado.
- [x] `I-6`: resuelto — conjunto anclado completo (14 filas).
- [x] `I-7`: resuelto — `recoveries` cuenta recuperación, no conducción.
- [x] `I-8`: resuelto — `findings_autonomously_corrected` derivado de la evidencia del journal.
- [x] Cada resolución tiene evidencia registrada en la matriz, en las regresiones y en `## Nota de ejecución`.
- [x] Las regresiones relevantes pasan; la suite global pasa sin fallos sin clasificar.
- [x] C-1/C-2/C-3 en estado válido según sus contratos vigentes (C-2 conserva el `GAP` histórico del Plan 116, que es contrato y no se reabre).
- [x] Sin `ANOMALY` no explicadas.
- [x] Sin cambios fuera del `Scope`.
- [x] `protocol/.agents/` intacto: **0 diff**.
- [x] Sin authority, state machine, registry ni change entity nuevos.
- [x] Sin release, tag, merge ni push.

## Verificación

```bash
python -m pytest tests/test_pytest_isolation.py tests/test_autonomous_scope.py tests/test_autonomous_orchestrator.py -q
python -m pytest tests/ -q
python -m pytest protocol/.agents/harness/tests/ -q
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
python tools/check_ears_coverage.py
python tools/check_discovery_output.py
git diff HEAD --name-only -- protocol/ dist/ ROADMAP.md docs/adr/
```

Además, las dos falsaciones por ejecución:

```bash
# I-1: dos sesiones concurrentes no comparten scratch (corrida simultánea)
# I-7/I-8: comparar corrida normal, con recovery real y con múltiples recoveries
```

## Validation anchor

- **Declared scope:** las diecisiete rutas del `## Scope` (dieciséis modificadas más este Plan): `CHANGELOG.md`, `.agents/policies/supervised-autonomous-execution.md`, `conftest.py`, `docs/placement-contract.md`, `docs/plans/137-ears-structural-validator.md`, `docs/plans/143-empty-remaining-backlog.md`, `docs/plans/144-dev-documentation-test-hygiene.md`, `docs/plans/145-integral-dev-backlog-closure.md`, `docs/plans/INDEX.md`, `runtime/README.md`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/observation.py`, `tests/AGENTS.md`, `tests/pytest_isolation.py`, `tests/test_autonomous_orchestrator.py`, `tests/test_autonomous_scope.py`, `tests/test_pytest_isolation.py`.
- **Validation command-set:** los 7 comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `python -m pytest tests/`) + `python -m pytest protocol/.agents/harness/tests/` + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + los checkers específicos `tools/check_ears_coverage.py` y `tools/check_discovery_output.py` + las suites de placement (resolver, contrato-drift y dogfood) + `git diff HEAD --name-only -- protocol/ dist/ ROADMAP.md docs/adr/` como frontera de 0 diff.
- **Effective inputs (repo content):** el scope declarado, `tests/pytest_isolation.py` y el `conftest.py` raíz (el harness de aislamiento), `runtime/orchestrator/{observation,autonomy,host,derivation,contracts}.py` (la frontera de observación y el resumen de autonomía), el corpus de `docs/plans/` y `docs/plans/INDEX.md`, `docs/placement-contract.md` con `runtime/placement/`, `tests/AGENTS.md` y el árbol de `tests/`.
- **Observed dependencies:** stdlib únicamente (`os`, `shutil`, `tempfile`, `time`, `subprocess`, `pathlib`, `re`, `hashlib`) y el CLI `git` disponible en el entorno; sin dependencias externas instrumentadas.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; pytest 9.0.3; el CLI `git` presente; `%TEMP%` en `C:\Users\rolda\AppData\Local\Temp` (fuera de OneDrive) y expuesto a la limpieza de temporales del sistema operativo (`SilentCleanup` / Storage Sense), que es justamente el factor que la corrección de `I-1` deja de poder convertir en pérdida de scratch de una sesión viva.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `c855669393723190b64094f777b2031d7e1c431b` (`git write-tree` sobre el índice staged con el Change completo).
  - **Delta scoped identity (scope S = las diecisiete rutas del `## Scope`, ordenadas; serialización `scoped-v1`):** `66b1d02e0853ea44fb02c84211f11ddd21cd11b29addbf77b045d54b0c24ba8e`.
  - **Límite declarado:** el delta se mide sobre el índice staged **antes** de transcribir los literales de identidad de este registro y del `Checkpoint`; esa transcripción es la única diferencia declarada entre el estado medido y el estado de cierre (convención anti-auto-referencia, precedente Planes 114/116/134/140/141/142/143/144).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `.agents/policies/supervised-autonomous-execution.md`, `CHANGELOG.md`, `conftest.py`, `docs/placement-contract.md`, `docs/plans/137-ears-structural-validator.md`, `docs/plans/143-empty-remaining-backlog.md`, `docs/plans/144-dev-documentation-test-hygiene.md`, `docs/plans/145-integral-dev-backlog-closure.md`, `docs/plans/INDEX.md`, `runtime/README.md`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/observation.py`, `tests/AGENTS.md`, `tests/pytest_isolation.py`, `tests/test_autonomous_orchestrator.py`, `tests/test_autonomous_scope.py`, `tests/test_pytest_isolation.py`.
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* ver `## Nota de ejecución`. El estado de cierre se validó sobre el índice staged con las diecisiete rutas del `## Scope`: los seis checkers canónicos PASS, `check_ears_coverage.py` y `check_discovery_output.py` PASS, las tres suites de placement PASS, `python -m pytest tests/` **1147 passed, 0 failed**, `python -m pytest protocol/.agents/harness/tests/ -q` **109 passed**, C-1 `VALID=50, GAP=0, ANOMALY=0`, C-2 `VALID=49, GAP=1, ANOMALY=0` (el `GAP` histórico del Plan 116, no reabierto) y C-3 `VALID=27, GAP=0, ANOMALY=0`.

## Checkpoint / cierre

- **Commits de cierre:** dos (2) commits en `dev`, identificados por sus mensajes: (1) `fix(dev): close the actionable DEV backlog I-1..I-8 (plan 145)` —el Change completo, SHA `c3131221a7e7d9804a3d670e6e5dfd7f59cd8261`—; (2) `docs(plans): record the plan 145 closure checkpoint (plan 145, C-1)` —este registro de checkpoint, que añade el SHA y el tree id material del primer commit. GC-1 admite el cierre multi-commit; los SHA y los tree id quedan como locators, no como identidad.
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `66b1d02e0853ea44fb02c84211f11ddd21cd11b29addbf77b045d54b0c24ba8e` / `c855669393723190b64094f777b2031d7e1c431b`. Es el estado que el checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** `5b06e5b3e7385228445a586d4149f19230c67c6a` (resuelto de `c313122`). Es un hecho de Git y **no** la identidad del estado de cierre: el commit de cierre incluye governance (este Plan y su registro de cierre), de modo que su árbol difiere legítimamente del estado validado (RFC-75 `Mecanismo 7 — Git Checkpoints`; modelo del Plan 134).
- **Consistencia checkpoint↔anchor:** PASS — C-2 lo verifica sobre el artefacto de este Plan.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 145 y su serie; `CHANGELOG.md` con el ítem `[Unreleased]` `(plan 145, RFC-—)`; los espejos reconciliados; sin RFC, sin ADR, sin payload, sin `VERSION` bump, sin tag.
- **Documentation impact:** `REQUIRED` — reconciliado en la ejecución. Documentos afectados: `runtime/README.md` (frontera de observación y reglas de métrica), `.agents/policies/supervised-autonomous-execution.md` §11 (semántica de las dos métricas), `tests/AGENTS.md` (conjunto anclado y regla de scratch por sesión), `docs/placement-contract.md` (`PC-72.1` y §23/§24), `docs/plans/INDEX.md` (registro y espejos), `docs/plans/137-…`, `docs/plans/143-…`, `docs/plans/144-…` (estado corriente y reconciliación). `docs/VERSIONING.md` **no** se modifica: su snapshot §9 se reconcilia en la promoción y este Change no tiene impacto explícito sobre él.
- **Roadmap impact:** `NOT_REQUIRED` — el mapa operativo ya declaraba «Sin trabajo activo» y «Pendientes que requieren autorización: Ninguno», y ninguna entrada del mapa cambia de estado: los ocho items son backlog DEV interno (harness, runtime de referencia, metadata y documentación), no trabajo registrado en `ROADMAP.md`.
- Condición derivada: **`Closed` (docs-only + tooling DEV, sin release)** — `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor ∧ evidencia PASS para el estado de cierre. `Executed ≠ Committed ≠ Closed ≠ Released`; ni `Promoted` ni `Released`: requieren autorización separada del mantenedor.

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia: la ejecución no detectó ningún defecto propio dentro del `Scope` que exigiera una corrección posterior a la verificación. Las dos observaciones que sí aparecieron durante la ejecución se resolvieron **dentro** del mismo Change y del mismo `Scope`, y quedan registradas en `## Nota de ejecución` en lugar de abrir un finding: (a) el par de backticks vacío que introdujo una edición al Placement Contract y que `test_placement_contract_drift.py` detectó —la guarda funcionando como está diseñada—; (b) el carácter CRLF que Git advierte al normalizar los archivos tocados, que es comportamiento preexistente del entorno y no un defecto del Change.

### Correcciones

No findings detected / N/A — declaración de ausencia: la ejecución no detectó ningún defecto propio dentro del `Scope` que exigiera una corrección posterior a la verificación.

### Pending decisions

No se registran pending decisions nuevas. Este Change no abre ninguna decisión:

- la corrección de `I-1` no necesita autoridad adicional (es el harness de tests DEV),
- las correcciones de `I-7`/`I-8` implementan la semántica que la policy §11 ya declara, en el runtime DEV de referencia,
- las reconciliaciones de `I-2`…`I-6` corrigen espejos y estado corriente contra fuentes que ya declaran el estado, sin cambiar ninguna norma,
- la frontera que `I-8` deja declarada (el host detiene la iteración ante un finding abierto en lugar de conducir una corrección) **no** es una pending decision nueva: es el comportamiento que la policy §6 autoriza («the host **may** correct») y que el Change registra explícitamente en el resumen en lugar de disimular con una heurística.

Las pending decisions que siguen abiertas en el repositorio (`<PLAN-125>:PC-1`/`PC-2`, `<PLAN-137>:PC-2`, `<PLAN-123>` materialidad ambiental) conservan su estado, su owner y su vía: ninguna de ellas está en el `Scope` de este Plan y este Plan no las resuelve por inferencia.

## Riesgos

- **Convertir la corrección de aislamiento en una pérdida de limpieza.** Mitigación: la sesión limpia su propio directorio (vacío por construcción) y la poda es acotada por edad; `test_pruning_*` verifica que una sesión viva nunca es candidata.
- **Hacer ruidosa una ausencia ambiental legítima.** Mitigación: la frontera distingue tres casos —CLI ausente (`GAP` declarado), root inexistente (sin error) y root legible con repositorio ilegible (`ObservationError`)— y las tres tienen regresión propia.
- **Reescribir evidencia histórica al reconciliar los Planes 137/143/144.** Mitigación: sólo se toca metadata evolucionable y prosa de estado corriente; no se marcan casillas retrospectivamente, no se alteran observaciones, commits ni resultados, y la reconciliación queda declarada como tal con su fecha.
- **Presentar como resuelto lo que sigue abierto al tocar el backlog evidenciado.** Mitigación: el banner de registro histórico y el párrafo de resolución corriente distinguen explícitamente historia, backlog histórico y estado actual.
- **Ampliar el Scope ante una inconsistencia nueva.** Mitigación: el `## Scope` enumera las diecisiete rutas; una necesidad fuera de él detiene la ejecución (`STOP_SCOPE_VIOLATION`) en lugar de ampliarse.

## Trazabilidad

Inventario read-only posterior al Plan 144 (`I-1`…`I-8`) → **Plan 145 (este Plan)**. `I-1` → `conftest.py` (la limpieza del scratch en `pytest_configure`) + `tests/pytest_isolation.py` + `runtime/orchestrator/observation.py` (las funciones `_run_git` y `git_state`) + el factor ambiental `%TEMP%`. `I-2` → `docs/plans/143-…:3` + `docs/plans/144-…:3` + `docs/plans/INDEX.md` (filas `Executed`). `I-3` → `docs/plans/INDEX.md` (fila y serie del Plan 137) + `docs/plans/137-…` (§Objetivo y §Criterio de entrada) + la ejecución del Plan 137 por el Plan 141. `I-4` → `docs/plans/INDEX.md:## Backlog evidenciado - plan 19` + RFC-79 + Plan 142 + `ROADMAP.md:## Pendientes que requieren autorización`. `I-5` → `docs/placement-contract.md` §22/§23/§24 + `runtime/placement/` (Plan 131) + `tests/test_placement_contract_drift.py`. `I-6` → `tests/AGENTS.md:Two kinds of test, by repository dependency` + `tests/test_placement_contract_drift.py`. `I-7`/`I-8` → `runtime/orchestrator/autonomy.py` (la función `summarize_autonomy`) + `.agents/policies/supervised-autonomous-execution.md` §11 + `runtime/README.md:## Supervised Autonomous Execution (Plan 135, hardened by Plan 138)`.

## Nota de ejecución

**Ejecutado el 2026-09-21** sobre el baseline `a90e50753d09c922178f436932e1c713d49be57f`, working tree limpio salvo el artefacto externo untracked `MASTER_PENDING_WORK_INVENTORY.md`.

**Qué se hizo, item por item.** `I-1`: el scratch root pasó de compartido a **propio de cada sesión**. `tests/pytest_isolation.py` declara un token de sesión explícito (`set_session_id`), resuelve `scratch_root` bajo `scratch/<token>`, limpia únicamente su propio directorio (`clear_own_scratch`) y poda los directorios de sesiones abandonadas por **edad** (`prune_stale_sessions`, umbral declarado de 24 h, un `stat` por vecino, sin recorrer el árbol). `conftest.py` declara el token en import time —antes de que cualquier módulo de test lo pida— y lo exporta por entorno para que un proceso hijo adopte su sesión en vez de inventar otra; una sesión sin token se **rechaza** en lugar de recibir un directorio compartido. En el runtime, `GitState` gana `git_available` y `observe()` eleva `ObservationError` cuando el CLI está disponible y el root existe pero el repositorio no se lee, conservando el `GAP` declarado para el CLI ausente y sin convertir un timeout en `None`. `I-7`: `_RECOVERY_ACTIONS` quedó reducido a `RUN_REVALIDATION` —la rama de recuperación de la derivación, alcanzada cuando el anchor A1 está stale para el contenido corriente— con la razón declarada en el código. `I-8`: `findings_autonomously_corrected` se deriva de los registros `RECORD_FINDING_CORRECTION` del journal mediante `findings_corrected_autonomously`, y cuando el conteo es cero el resumen **declara la frontera** en una nota en lugar de presentar una constante como valor derivado. `I-2`/`I-3`/`I-4`: los headers de los Planes 143 y 144 pasaron a `Executed` con la fecha y la referencia a este Plan; la fila del Plan 137 y su título de serie quedaron en `Executed` sin «preparación» y su §Objetivo declara el estado corriente con nota de reconciliación en `## Criterio de entrada`; el backlog evidenciado del plan 19 recibió un banner de registro histórico, las filas `B-4`/`B-7`/`B-8` quedaron anotadas como resueltas y un párrafo de resolución corriente nombra la RFC-79 y el Plan 142 (11.6.0). `I-5`: `PC-72.1` registra el estado real del enforcement autorizado —librería de tabla de reglas materializada por el Plan 131, **no integrada** y advisory— y §23/§24 distinguen enforcement como obligación operativa de realización mecánica. `I-6`: `test_placement_contract_drift.py` entró al conjunto anclado (14 filas) y la fila de `test_pytest_isolation.py` declara la propiedad de sesión.

**Observaciones resueltas dentro del Change.** (a) Una edición al Placement Contract introdujo el par `` `PC-76` `E-6` `` y `test_placement_contract_drift.py` falló con `IndexError` en `_declared_namespaces`: la guarda leyó el contrato real y detectó el drift, que se corrigió a `§22 `PC-76`, invariant E-6`. Es la guarda funcionando como está diseñada, registrada aquí y no como finding. (b) Git advierte la normalización LF→CRLF en los archivos tocados; es comportamiento preexistente del entorno en Windows, no un defecto de este Change, y no se modificó la configuración de fin de línea.

**Verificación.** Seis checkers canónicos PASS (`check_protocol_invariants` 215 archivos / 10334 referencias, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` con los warnings de tags esperados en `dev`); `python -m pytest tests/` **1147 passed, 0 failed** (los 27 tests nuevos sobre los 1120 del baseline); `python -m pytest protocol/.agents/harness/tests/ -q` **109 passed**; las tres suites afectadas **120 passed**; los checkers específicos `check_ears_coverage.py` (`N/A=1, VALID=3`) y `check_discovery_output.py` (`N/A=1`) PASS; las tres suites de placement **46 passed**; C-1 `VALID=50, GAP=0, ANOMALY=0`, C-2 `VALID=49, GAP=1, ANOMALY=0` y C-3 `VALID=27, GAP=0, ANOMALY=0`. El `GAP` de C-2 sobre el Plan 116 es el histórico, sigue emitiéndose por contrato y **no se reabre**.

**Falsación por ejecución.** `I-1`: 12 regresiones nuevas ejecutadas contra la implementación anterior (revirtiendo `conftest.py` y `tests/pytest_isolation.py`, con las regresiones en el árbol) fallaron todas y pasan contra la nueva; la corrida concurrente de una sesión larga (127 tests de las suites SAE) junto a tres sesiones cortas que limpiaban su propio scratch terminó **sin interferencia**, y cada sesión dejó su propio directorio. `I-7`/`I-8`: 9 regresiones nuevas ejecutadas contra la implementación anterior de `autonomy.py` fallaron todas —las de `I-8` porque el valor era siempre `0`— y pasan contra la nueva; en una corrida real por el host, el resumen pasó de `Recoveries: 3` con cero stops a `Recoveries: 0`, y el conteo de correcciones autónomas responde a la evidencia del journal en lugar de ser una constante.

**Fronteras respetadas.** No se creó ningún mecanismo, policy, checker, estado, registry, authority class, taxonomy ni workflow nuevos; `protocol/.agents/`, `dist/`, `ROADMAP.md` y `docs/adr/` quedan con **0 diff**; no se tocó ningún artefacto cerrado fuera de la metadata evolucionable y los espejos declarados en el `## Scope`; no se marcó retrospectivamente ninguna casilla de criterio de entrada; no se alteró ninguna observación, commit, árbol o resultado histórico; no se tocó el inventario externo `MASTER_PENDING_WORK_INVENTORY.md`; no se promovió, taggeó, publicó ni empujó.
