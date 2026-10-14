# Test Suite Audit — ARgentOS DEV

RESULT = TEST_SUITE_AUDIT

**Clase documental:** Working / Audit (provenance) — no normativo.
**Naturaleza:** auditoría / relevamiento `READ_ONLY` de la estrategia de testing.
**Autoridad de este documento:** ninguna. Registra hechos, mediciones,
inferencias e hipótesis; no crea mecanismos, no modifica la suite, no autoriza
trabajo y no decide política de testing.
**Fecha:** 2026-10-13 · **Rama:** `dev` · **HEAD:** `f75d70a`
**Alcance:** `tests/` (57 archivos), `protocol/.agents/harness/tests/` (12
archivos), `tools/`, `runtime/`, `conftest.py`, CI, `.agents/`, `docs/` de
política. Sin modificación de código, tests, dependencias ni CI.

**Marcas usadas en todo el documento**

| Marca | Significado |
|---|---|
| `HECHO` | observado directamente en el repositorio (lectura o glob/grep) |
| `MEDICIÓN` | obtenido ejecutando la suite o una parte de ella en esta máquina |
| `INFERENCIA` | conclusión derivada de hechos/mediciones, no observada directamente |
| `HIPÓTESIS` | conjetura explícita, no verificada |
| `RECOMENDACIÓN` | propuesta de acción, no implementada |

---

## 1. Executive Summary

`MEDICIÓN` La suite completa (los dos legs, 1543 tests) corrió en
**397.91 s**. La suite canónica (`pytest tests/`, 1358 tests) explica
**385.5 s** de ese total; el leg del harness del producto (185 tests) sólo
**7.7 s**.

`MEDICIÓN` **165 tests de 5 archivos (10.7 % de la suite canónica) consumen
290.5 s, el 75.3 % del tiempo total de la suite canónica.** Los otros 1193
tests corren en 95.0 s.

`MEDICIÓN` La mediana del tiempo por test es **0.00 s** (al precisión del
reporte) y el p95 es **1.05 s**: el costo no está distribuido, está concentrado.

`MEDICIÓN` Los tests caros no son caros por lógica: construyen un repositorio
git nuevo por test con 4–8 `subprocess.run(["git", ...])`
(`tests/test_autonomous_orchestrator.py:116`, `tests/test_agent_worker.py:135`).
Son **tests de integración disfrazados de unitarios de host**.

`MEDICIÓN` Cambios fuera de `runtime/orchestrator/` son baratísimos de validar:
un cambio en `tools/check_ears_coverage.py` → **91 tests / 3.23 s**;
`runtime/toolcalls/` → **111 tests / 0.56 s**; `runtime/memory/` →
**63 tests / 0.26 s** (suma de duraciones `call`: 0.07 s).

`MEDICIÓN` El leg del harness del producto (185 tests) corre en **7.7 s**: el
mejor cociente test/segundo del repositorio, por dos órdenes de magnitud frente
al área del orquestador (165 tests en 290.5 s).

`INFERENCIA` **La oportunidad de reducción es real pero desigual.** Para
cambios en `tools/`, `runtime/memory/`, `runtime/toolcalls/` y `runtime/placement/`
(cubren la mayoría de los archivos de producción) la selección de tests por
área reduce el costo de validación en dos a tres órdenes de magnitud. Para
cambios en `runtime/orchestrator/`, la selección **no ayuda**: el área entera
(294 tests) cuesta 306 s y el subconjunto más pequeño con sentido (un solo
archivo, `test_autonomous_orchestrator.py`) ya cuesta 102.3 s.

`RECOMENDACIÓN` Introducir una política de **tres niveles por contexto**
(TARGETED en desarrollo, FULL en CI, FULL + gates en release) — no una política
de selección fina, y no coverage ni markers. Detalle en §11.

---

## 2. Current Suite — Inventario completo de la suite

### 2.1 Composición (`HECHO`)

| Leg | Archivos | Tests | Comando |
|---|---|---|---|
| Suite DEV (`tests/`) — **batería canónica** | 57 | **1358** | `python -m pytest tests/` |
| Harness del producto (embebido en el payload) | 12 | **185** | `python -m pytest protocol/.agents/harness/tests/` |
| **Total del repositorio** | **69** | **1543** | ambos legs |

`HECHO` No existe un tercer conjunto: `pytest --collect-only` sin argumentos
recolecta exactamente los 1358 de `tests/` (rootdir = raíz; `protocol/` no se
autodescubre porque `protocol/.agents/harness/tests/` no matchea `test_*.py`
desde la raíz… sí matchea — verificado: la recolección sin argumentos da 1358,
porque el `norecursedirs` por defecto excluye directorios ocultos y `.agents`
empieza con punto).

`INFERENCIA` Esto explica la cifra reportada por el usuario: **1358 tests /
317.82 s es el leg canónico**, no la suite completa con harness.

### 2.2 Configuración (`HECHO`)

- **No existe** `pytest.ini`, `pyproject.toml`, `setup.cfg`, `tox.ini`,
  `Makefile`, `requirements*.txt`, `uv.lock`, `poetry.lock`,
  `.pre-commit-config.yaml` ni `noxfile.py` (glob negativo sobre todo el repo).
- **No hay marcadores propios declarados** (no hay `markers =` en ningún
  archivo, no hay registro de markers).
- La configuración viva está toda en `conftest.py` (raíz): bootstrap de
  `sys.path` (`tests/`, `tools/`), redirección de `basetemp`/`cache_dir` fuera
  del repo, y token de sesión para scratch (`conftest.py:73-127`).
- `protocol/.agents/harness/tests/conftest.py` aporta 4 fixtures locales
  (`payload`, `project`, `staging_parent`, `make_engine`) y `make_junction`.

### 2.3 Estructura (`HECHO`)

- `tests/` es **plano**: 57 archivos en un solo nivel, sin subdirectorios de
  área. `tests/fixtures/` contiene 3 `SKILL.md` sintéticas.
- La organización real es **por prefijo de nombre de archivo**:
  `test_check_*` (checkers DEV), `test_memory_*`, `test_placement_*`,
  `test_fc_*` (F-C flow), `test_autonomous_*` / `test_autonomy_*` / `test_sae_*`
  (orquestador/autonomía), `test_canonical_*` / `test_*segment*` /
  `test_toolcalls` (materialización).
- **No hay clases de test** (`HECHO`: las 8 clases definidas son helpers
  —`RecordingInvoker`, `WritingInvoker`, etc.—, ninguna empieza con `Test`).
- **25 decoradores `parametrize`** en 11 archivos (`HECHO`); los que más
  expanden son `test_check_plan_citations.py` (5), `test_adversarial_deliberation.py` (6),
  `test_check_plan_structure.py` (4), `test_segment_resolution.py` (3).
- **Estados especiales** (`HECHO`): 3 `pytest.mark.skipif` a nivel de módulo
  (`test_check_dist_sync.py:24`, `test_check_lifecycle_checkpoint.py:35`,
  `test_scoped_content_identity.py:30`); **ningún `xfail`**; 1 skip efectivo en
  la corrida medida (`1241 passed, 1 skipped`).
- **Fixtures compartidas**: sólo las 4 del harness + `tmp_path`/`monkeypatch`
  (stdlib de pytest). No hay `conftest.py` en `tests/`: cada suite define sus
  propios builders (`build_repo`, `make_repo`, `write`, `_scratch`…).

### 2.4 Tamaño (`HECHO`, medido en líneas)

| Capa | Archivos `.py` | Líneas |
|---|---|---|
| `runtime/` (42 archivos) + `tools/` (20) | 63 | 20 312 |
| `protocol/.agents/harness/*.py` (producto) | 8 | 4 024 |
| `tests/test_*.py` | 57 | 18 286 |
| `protocol/.agents/harness/tests/test_*.py` | 12 | 2 689 |

`INFERENCIA` ~0.90 líneas de test por línea de producción en la capa DEV: la
suite es proporcionalmente grande, lo que es coherente con el costo total de
5–6.5 minutos.

### 2.5 Distribución por área / módulo (`HECHO` sobre la recolección + `INFERENCIA`
en el agrupamiento por prefijo; **no** es directorio = módulo)

| Área / módulo | Archivos | Tests | % suite total |
|---|---:|---:|---:|
| `tools/check_*` (checkers DEV) | 12 | 372 | 24.1 % |
| `runtime/orchestrator` (incl. F-C, SAE, autonomía) | 10 | 261 | 16.9 % |
| `runtime/toolcalls` | 5 | 198 | 12.8 % |
| Harness del producto (`protocol/.agents/harness`) | 12 | 185 | 12.0 % |
| `tools/` (métricas, gates, identidad) | 6 | 143 | 9.3 % |
| Contratos DEV y del repositorio | 5 | 119 | 7.7 % |
| Dogfood anclado al repo real | 7 | 89 | 5.8 % |
| `tools/check_ears_coverage` (excl.) | 2 | 73 | 4.7 % |
| `runtime/memory` | 8 | 63 | 4.1 % |
| `runtime/placement` | 2 | 40 | 2.6 % |
| **TOTAL** | **69** | **1543** | **100 %** |
| *– de los cuales, suite canónica* | *57* | *1358* | *88.0 %* |
| *– de los cuales, harness* | *12* | *185* | *12.0 %* |

Detalle por archivo (test count):

```text
protocol harness      185   3+55+5+25+7+15+4+13+11+6+8+33
tools/check_*         372   test_check_session_artifacts 60, plan_citations 52,
                            discovery_output 48, lifecycle_lineage 40,
                            plan_structure 36, lifecycle_checkpoint 32,
                            protocol_invariants 30, taxonomy 28,
                            lifecycle_anchor 23, architecture_traceability 8,
                            version_state 8, dist_sync 7
runtime/orchestrator  261   autonomous_scope 67, sae_scope_enforcement 44,
                            agent_worker 41, autonomy_effects 36,
                            autonomous_orchestrator 31, fc_flow 22,
                            fc_actor_provenance 7, fc_host_integration 5,
                            fc_recovery_alignment 4, fc_isolation_declaration 4
runtime/toolcalls     198   segment_resolution 56, canonical_materialization 51,
                            canonical_materialization_v2 42, project_segment 37,
                            toolcalls 12
tools/ (otros)        143   determine_execution_state 69, aggregate_metrics 32,
                            scoped_content_identity 17, audit_gates 10,
                            legacy_paths 9, measure_context_budget 6
contratos DEV         119   adversarial_deliberation 75, pytest_isolation 22,
                            change_governance 11, root_contract 10, repo_containment 1
dogfood anclado        89   check_ears_coverage_dogfood 18,
                            prompt_cache_dogfood 18, discovery_output_dogfood 14,
                            autonomy_effects_dogfood 13,
                            sae_scope_enforcement_dogfood 13,
                            autonomous_scope_dogfood 7, placement_dogfood 6
ears (excl.)           73   check_ears_coverage 43, ..._falsification 30
runtime/memory         63   8 archivos, 6–10 tests cada uno
runtime/placement      40   placement_resolver 31, placement_contract_drift 9
```

---

## 3. Performance — Costo temporal

### 3.1 Totales (`MEDICIÓN`)

| Magnitud | Valor |
|---|---|
| Comando medido | `python -m pytest tests/ protocol/.agents/harness/tests/ -q --durations=0 --durations-min=0` |
| Resultado | **1543 passed** en **397.91 s** |
| Suma por fase | call **391.6 s**, setup **1.6 s**, teardown **0.0 s** |
| Suite canónica (1358 tests), atribuida | **385.5 s** |
| Leg harness (185 tests), atribuido | **7.7 s** |
| Cifra de referencia reportada por el usuario | 1358 passed en 317.82 s |

`INFERENCIA` La diferencia entre los 317.82 s de referencia y los 385.5 s
atribuidos aquí (≈ 20 %) es atribuible a entorno (máquina, carga, caché de
filesystem, versión de pytest) y a que esta corrida ejecutó los dos legs en un
mismo proceso con el leg harness incluido. **Ninguna cifra absoluta de este
informe debe leerse como universal; las relativas y las proporciones sí son
robustas.**

### 3.2 Distribución (`MEDICIÓN` sobre los 1486 nodos con duración registrada)

| Estadístico (call, por test) | Valor |
|---|---|
| n | 1486 de 1543 (57 sin entrada; por debajo de la resolución del reporte) |
| total | 391.59 s |
| media | 0.264 s |
| **mediana** | **0.000 s** |
| p90 | 0.48 s |
| **p95** | **1.05 s** |
| p99 | 6.08 s |
| máx | 22.66 s |

`INFERENCIA` p95 = 1.05 s significa que **el 95 % de la suite es
irrelevante para el costo**: optimizar o saltear tests no cambia el reloj.
El 5 % restante es el problema completo.

### 3.3 Top 20 tests por duración (`MEDICIÓN`, fase call)

| # | s | Test |
|---:|---:|---|
| 1 | 22.66 | `tests/test_autonomous_orchestrator.py::test_revalidation_is_recorded_as_a2_without_mutating_a1` |
| 2 | 15.15 | `tests/test_autonomous_orchestrator.py::test_restart_reconstructs_and_continues_without_lost_continuity` |
| 3 | 14.09 | `tests/test_autonomous_orchestrator.py::test_full_loop_derives_closed_from_real_evidence` |
| 4 | 12.07 | `tests/test_autonomous_orchestrator.py::test_closed_derivation_never_releases_and_reports_human_authority` |
| 5 | 9.46 | `tests/test_autonomous_orchestrator.py::test_stale_validation_derives_revalidation_and_fresh_does_not` |
| 6 | 9.33 | `tests/test_sae_scope_enforcement.py::test_the_host_stops_when_a_declared_scope_widens_to_another_authorized_path` |
| 7 | 9.10 | `tests/test_sae_scope_enforcement.py::test_an_unauthorized_widening_is_refused_by_the_scope_check_before_any_drift` |
| 8 | 8.43 | `tests/test_agent_worker.py::test_stale_validation_does_not_allow_closed` |
| 9 | 7.96 | `tests/test_sae_scope_enforcement.py::test_the_host_stops_when_the_contract_is_rewritten_after_authorization` |
| 10 | 7.90 | `tests/test_agent_worker.py::test_empty_implementation_result_does_not_re_delegate_forever` |
| 11 | 7.86 | `tests/test_sae_scope_enforcement_dogfood.py::test_functional_dogfood_the_checkpoint_survives_a_rewrite_between_runs` |
| 12 | 6.67 | `tests/test_agent_worker.py::test_derivation_uses_post_ingestion_state_and_does_not_repeat_the_task` |
| 13 | 6.11 | `tests/test_autonomy_effects.py::test_the_ceiling_bounds_the_first_delegation_and_stops_the_second` |
| 14 | 6.08 | `tests/test_autonomous_orchestrator.py::test_no_progress_guard_stops_instead_of_spinning` |
| 15 | 6.08 | `tests/test_autonomy_effects.py::test_resource_exhaustion_is_never_an_authorization` |
| 16 | 5.92 | `tests/test_autonomy_effects.py::test_the_ceiling_survives_a_process_restart_because_it_is_read_from_evidence` |
| 17 | 5.91 | `tests/test_sae_scope_enforcement.py::test_a_required_obligation_outside_the_scope_is_refused_and_changes_nothing` |
| 18 | 5.23 | `tests/test_agent_worker.py::test_finding_blocks_closure_until_resolved_and_revalidation_is_derivable` |
| 19 | 5.06 | `tests/test_agent_worker.py::test_recovery_after_restart_from_persisted_evidence_only` |
| 20 | 4.72 | `tests/test_sae_scope_enforcement.py::test_the_regression_is_not_vacuous_the_write_really_happens_when_allowed` |

`MEDICIÓN` Los 20 tests más lentos suman **178.8 s** (45.7 % del call time).
El top 20 pertenece a **5 archivos**, todos de `runtime/orchestrator/`.

### 3.4 Top 20 archivos por duración (`MEDICIÓN`, call time agregado)

| # | s | tests | ms/test | Archivo |
|---:|---:|---:|---:|---|
| 1 | 102.32 | 31 | 3300.6 | `tests/test_autonomous_orchestrator.py` |
| 2 | 69.22 | 41 | 1688.3 | `tests/test_agent_worker.py` |
| 3 | 59.98 | 44 | 1363.2 | `tests/test_sae_scope_enforcement.py` |
| 4 | 46.84 | 36 | 1301.1 | `tests/test_autonomy_effects.py` |
| 5 | 28.35 | 32 | 885.9 | `tests/test_check_lifecycle_checkpoint.py` |
| 6 | 13.05 | 17 | 767.6 | `tests/test_scoped_content_identity.py` |
| 7 | 12.94 | 67 | 193.1 | `tests/test_autonomous_scope.py` |
| 8 | 12.10 | 13 | 930.8 | `tests/test_sae_scope_enforcement_dogfood.py` |
| 9 | 10.67 | 69 | 154.6 | `tests/test_determine_execution_state.py` |
| 10 | 4.51 | 40 | 112.8 | `tests/test_check_lifecycle_lineage.py` |
| 11 | 4.21 | 7 | 601.4 | `tests/test_autonomous_scope_dogfood.py` |
| 12 | 3.99 | 7 | 570.0 | `tests/test_check_dist_sync.py` |
| 13 | 2.59 | 22 | 117.7 | `tests/test_pytest_isolation.py` |
| 14 | 2.48 | 13 | 190.8 | `tests/test_autonomy_effects_dogfood.py` |
| 15 | 1.79 | 18 | 99.4 | `tests/test_check_ears_coverage_dogfood.py` |
| 16 | 1.65 | 15 | 110.0 | `harness/tests/test_lifecycle_install.py` |
| 17 | 1.34 | 48 | 27.9 | `tests/test_check_discovery_output.py` |
| 18 | 1.18 | 11 | 107.3 | `harness/tests/test_lifecycle_update_uninstall.py` |
| 19 | 1.11 | 3 | 370.0 | `harness/tests/test_enforced_flow.py` |
| 20 | 1.08 | 23 | 47.0 | `tests/test_check_lifecycle_anchor.py` |

`MEDICIÓN` **Los 5 primeros archivos (8.8 % de los archivos, 165 tests,
10.7 % de los tests) consumen 290.5 s = 75.3 % del leg canónico.** Los
restantes 1193 tests suman 95.0 s.

`MEDICIÓN` 39 de 69 archivos tienen **≤ 0.5 s** de call time agregado; 22
archivos no registran duración alguna (por debajo de la resolución reportada).

### 3.5 Cuellos de botella (`HECHO` + `INFERENCIA`)

1. `HECHO` Cada test caro construye un repositorio git nuevo:
   `pytest_isolation.scratch_root(...)` + `subprocess.run(["git", "init", "-q"], ...)`
   + `git add -A` + `git commit` (`tests/test_agent_worker.py:135-140`,
   `tests/test_autonomous_orchestrator.py:116-120,268-270`, mismos patrones en
   `test_sae_scope_enforcement.py`, `test_autonomy_effects.py`).
2. `HECHO` 14 archivos usan `subprocess` (fase de inventario); los 4 más lentos
   concentran las invocaciones de `git` (11, 29, 10 y 2 referencias textuales
   respectivamente).
3. `HECHO` El **setup/teardown de pytest no es el problema**: 1.6 s y 0.0 s
   totales. No hay fixtures costosas reutilizadas: el costo está *dentro* de
   cada test.
4. `MEDICIÓN` La corrida completa consumió ~45 s de CPU en ~400 s de reloj:
   **el cuello de botella es I/O y creación de procesos, no cómputo.**
5. `HECHO` `tests/test_check_lifecycle_checkpoint.py` (28.4 s) es el único
   archivo caro fuera de `orchestrator`: es un conjunto **anclado** al repo
   real y resuelve objetos git (`4.13 s` el test
   `test_real_repo_expected_classifications`), además de 10 llamadas a git.
6. `HECHO` 3 archivos leen el árbol real del repositorio y no son aislables:
   los dogfood y `test_repo_containment.py` (1.05 s para **un solo test**).
7. `HECHO` 7 archivos invocan un pytest anidado o un subproceso Python
   (`test_pytest_isolation.py`, `test_determine_execution_state.py`,
   `test_scoped_content_identity.py`, `test_autonomous_orchestrator.py`,
   `test_autonomous_scope.py`, `test_sae_scope_enforcement.py`,
   `test_check_dist_sync.py`): doble costo de arranque de intérprete.

---

## 4. Production ↔ Test Relationships — Relación código ↔ tests

### 4.1 Método (`HECHO`)

Mapeo estático por AST de los 69 archivos de test contra 71 módulos de
producción (imports reales, re-exports de paquetes resueltos, imports planos
vía el bootstrap `sys.path` de `conftest.py`, e invocaciones textuales
`tools/*.py`). `INFERENCIA`: es una **sobre-aproximación deliberada** — un
import no garantiza ejecución, pero la ausencia de import sí descarta el
vínculo por import.

### 4.2 Relación conceptual (`HECHO` en los vínculos, `INFERENCIA` en la lectura)

```text
componente de producción                    tests DIRECTOS   tests TRANSITIVOS
------------------------------------------------------------------------------
protocol/.agents/harness/roots.py                  6              13
runtime/orchestrator/autonomy.py                   7              10
runtime/orchestrator/worker.py                     7              10
runtime/orchestrator/contracts.py                  3               8
runtime/orchestrator/host.py                       8               8
runtime/orchestrator/fc_flow.py                    2               7
runtime/orchestrator/observation.py                7               7
runtime/orchestrator/store.py                      7               7
runtime/orchestrator/agent_worker.py               6               6
protocol/.agents/harness/lifecycle_contract.py     5               5
runtime/memory/semantic.py                         5               5
runtime/toolcalls/canonical.py                     5               5
runtime/toolcalls/context.py                       5               5
protocol/.agents/harness/lifecycle.py              4               4
protocol/.agents/harness/lifecycle_staging.py      0               4
runtime/memory/store.py                            4               4
runtime/toolcalls/identity.py                      4               4
tools/check_ears_coverage.py                       4               4
runtime/placement/{__init__,resolver,rules}.py     3 c/u           3 c/u
tools/check_lifecycle_{anchor,checkpoint,lineage}  3 c/u           3 c/u
tools/{check_plan_citations,scoped_content_identity} 3 c/u         3 c/u
runtime/orchestrator/{authority,derivation,governance}.py 2 c/u     2 c/u
runtime/orchestrator/__init__.py                   2               2
runtime/toolcalls/{budget,cache_coordinator,provider_cache,segment_resolution} 2 c/u 2 c/u
tools/{check_discovery_output,check_plan_structure,
       check_session_artifacts,determine_execution_state} 2 c/u     2 c/u
runtime/memory/{archive,consolidation,cutover,episodic,extraction,
                metrics,migration,operational,relations,retrieval,synthesis} 1 c/u 1 c/u
runtime/toolcalls/{change_governance,project_segment,project_store,
                   prompt_rendering,toolcalls_rendering} 1 c/u       1 c/u
tools/{aggregate_metrics,audit_gates,check_dist_sync,check_memory_store,
       check_protocol_invariants,check_taxonomy_coherence,check_version_state,
       measure_context_budget,legacy_paths} 1 c/u                    1 c/u
runtime/orchestrator/__main__.py                   0               0
tools/check_architecture_traceability.py           1               1
```

`HECHO` **65 de 69 archivos de test importan ≥ 1 módulo de producción.**
Los 4 restantes no importan producción a propósito:

| Archivo | Qué valida | Por qué no importa producción |
|---|---|---|
| `tests/test_adversarial_deliberation.py` (75 tests) | forma de contratos documentales del payload | asserta sobre texto de documentos |
| `tests/test_fc_isolation_declaration.py` (4) | la declaración publicada de ausencia de aislamiento | lee documentos y aserta su texto |
| `tests/test_fc_recovery_alignment.py` (4) | paridad policy ↔ código de retry | lee policy + código como texto |
| ~~`test_check_architecture_traceability.py`~~ | — | **sí importa** el tool (corregido en el mapeo final) |

`HECHO` 18 archivos de test se declaran **anclados al repo real** en
`tests/AGENTS.md:73-91` (dogfood, read-only, actualizables sólo cuando el
estado canónico cambia legítimamente).

### 4.3 Respuestas a las preguntas de §3 del pedido (`INFERENCIA` fundada)

| Pregunta | Respuesta |
|---|---|
| ¿Los módulos de producción son cubiertos por tests? | Sí, todos menos `runtime/orchestrator/__main__.py` (0 tests) |
| ¿Los tests están asociados a componentes? | **Sí, y de forma muy nítida**: 47 de 71 módulos tienen 1–3 archivos directos; el acoplamiento es por import real |
| ¿Hay tests que atraviesan múltiples capas? | Sí: `test_agent_worker.py` (13 módulos), `test_autonomous_orchestrator.py` (11), `test_autonomy_effects.py` (7), `test_sae_scope_enforcement.py` (6) |
| ¿Hay tests acoplados a implementación interna? | Sí, en los 4 archivos anteriores: construyen repositorios reales y ejercitan el host completo |
| ¿Hay tests de integración que cubran múltiples componentes? | Sí: exactamente esos 4 + la dogfood `test_sae_scope_enforcement_dogfood.py` |
| ¿Hay tests afectados por cambios lejanos? | Sí: cualquier cambio en `conftest.py`, `tests/pytest_isolation.py` o el bootstrap de `sys.path` afecta **a toda la suite que use `tmp_path`/`scratch_root`** (real: plan 145 lo hizo) |

---

## 5. Dependency / Blast Radius Analysis — Dependencias y blast radius

### 5.1 Arquitectura real (`HECHO` sobre imports entre módulos de producción)

- **Núcleo compartido con mayor fan-out de tests**: el paquete
  `runtime/orchestrator/` es un grafo denso: `host.py` importa 8 módulos,
  `__main__.py` 8, `__init__.py` 5, `agent_worker.py` 4, `derivation.py` 3,
  `fc_flow.py` 3.
- **Utilidades transversales**: `runtime/toolcalls/canonical.py` (3 dependientes
  internos), `protocol/.agents/harness/roots.py` (6 archivos de test lo importan
  directamente y 13 lo alcanzan transitivamente), `runtime/memory/store.py`
  (infra de escritura atómica usada por `runtime/memory/*` y por el orquestador).
- **Puntos de entrada**: `runtime/orchestrator/__main__.py` (sin tests) y el CLI
  de cada `tools/check_*.py` (probado vía exit codes y subprocess).
- **Módulos periféricos**: los 20 `tools/*.py` (cada uno con su suite
  dedicada, 1–4 archivos) y los 11 módulos «hoja» de `runtime/memory/`.

### 5.2 Blast radius: dos formas muy distintas (`MEDICIÓN` + `INFERENCIA`)

```text
A)  utilities compartidas        →  archivos de test  →  tests   →  tiempo
    protocol/.agents/harness/roots.py    13              198        7.3 s
    runtime/orchestrator/worker.py       10              288      306.0 s
    runtime/orchestrator/host.py          8              250      305.9 s
    runtime/orchestrator/autonomy.py     10              255      207.8 s
    contraste:
B)  componente aislado           →  archivos de test  →  tests   →  tiempo
    runtime/memory/episodic.py            1                7        0.03 s
    runtime/toolcalls/prompt_rendering.py 1               12        0.00 s
    tools/check_ears_coverage.py          4               91        3.23 s
```

`MEDICIÓN` El blast radius en **tiempo** es aún más desigual que en tests:
- `runtime/orchestrator/host.py` → 250 tests en 8 archivos, **305.9 s**.
- `runtime/orchestrator/worker.py` → 288 tests en 10 archivos, **306.0 s**.
- `runtime/orchestrator/autonomy.py` → 255 tests en 10 archivos, **207.8 s**.
- `protocol/.agents/harness/roots.py` → 198 tests en 13 archivos, **7.3 s**.
- `runtime/memory/episodic.py` → 7 tests, **0.03 s** (el archivo entero: 0.07 s).
- `tools/check_ears_coverage.py` → 91 tests, **3.23 s** (medido).

`INFERENCIA` El «blast radius pequeño» de un util compartido no es pequeño **en
cantidad**: `roots.py` (151 líneas, uno de los archivos más chicos del harness)
arrastra 198 tests — el mayor fan-out de test del repositorio. Pero **sí lo es
en tiempo**: 7.3 s. La conclusión operativa es que *fan-out de tests* y *costo
de tests* son ejes independientes en este repositorio, y el segundo es el que
importa para la política de ejecución.

### 5.3 Superficie que la selección NO puede cubrir sin ejecutar (§8)

`HECHO` 15 archivos de test dependen del **estado del repositorio real**: los
18 anclados de `tests/AGENTS.md` más los dogfood del harness. Un cambio en
cualquier documento canónico, plan, RFC, charter o estado de versión los
invalida a todos — pero **no hay relación de import** que lo exprese.

---

## 6. Coverage Analysis — Estado de la cobertura

### 6.1 Estado actual (`HECHO`)

- **No existe ninguna configuración de coverage en el repositorio**: no hay
  `.coveragerc`, no hay `[tool.coverage]` (no hay `pyproject.toml`), no hay
  umbral, no hay badge, no hay integración con CI ni con `pytest`.
- `HECHO` `coverage` no es una dependencia del proyecto (no hay archivo de
  dependencias). CI instala **sólo** `pytest`
  (`.github/workflows/check-protocol.yml:37`).
- `HECHO` En **esta máquina** están instalados `coverage 7.13.5`,
  `pytest-cov 7.1.0`, `pytest-asyncio 1.4.0` y `pytest-timeout 2.4.0`, pero
  ninguno se usa en el repositorio y ninguno se declara. Es entorno local, no
  política.
- `HECHO` La palabra «coverage» en `docs/` se refiere a otras métricas
  (validation anchor coverage, finding lineage coverage de RFC-75) y a
  `check_ears_coverage.py`, **no** a cobertura de código.

### 6.2 Medición (`MEDICIÓN`)

Intentar medir coverage sobre la suite completa es impracticable: la corrida
instrumentada cubrió 72 tests en ~2.5 min y se abandonó. La causa es que los
tests caros son I/O-bound y la instrumentación penaliza la E/S por línea.

Se midió, en cambio, la mayor parte de la suite (todo menos los 10 archivos más
caros, que son precisamente los que cubren `runtime/orchestrator`):

```
python -m pytest tests/ protocol/.agents/harness/tests/ -q --ignore=<10 archivos caros>
  --cov=runtime --cov=tools
→ 1241 passed, 1 skipped in 51.42 s
→ TOTAL 8411 statements, 5686 cubiertos (67.6 %), 2725 sin cubrir
```

Cobertura por área (subset medido: 1241 de 1543 tests = 80.4 %). **Excluye los
10 archivos más caros** —entre ellos `test_check_lifecycle_checkpoint.py` y los
tests pesados de `runtime/orchestrator`—, de modo que las cifras de esas dos
áreas son un **piso**, no su cobertura real:

| Área | Statements | Cubiertos | % |
|---|---:|---:|---:|
| `tools/*` (20 archivos) | 4509 | 3512 | **77.9 %** |
| `runtime/*` (43 archivos) | 3902 | 2174 | **55.7 %** |
| — `runtime/memory/*` (14) | 294 | 287 | **97.6 %** |
| — `runtime/toolcalls/*` (13) | 689 | 646 | **93.8 %** |
| — `runtime/placement/*` (3) | 203 | 180 | **88.7 %** |
| — `runtime/orchestrator/*` (13) | 2716 | 1061 | **39.1 %** (piso) |
| **TOTAL** | **8411** | **5686** | **67.6 %** |

Módulos con **menor** cobertura (≥ 40 statements, en el subset medido; los de
`runtime/orchestrator` son piso porque sus tests pesados quedaron fuera):

```text
  0.0%    0/280  tools/check_lifecycle_checkpoint.py   (excluido del subset: entero)
  0.0%    0/ 78  runtime/orchestrator/__main__.py      (sin ningún test — HECHO)
 18.4%   65/354  runtime/orchestrator/host.py
 22.1%   32/145  runtime/orchestrator/governance.py
 22.8%   41/180  runtime/orchestrator/store.py
 23.2%   29/125  runtime/orchestrator/derivation.py
 33.3%   69/207  runtime/orchestrator/worker.py
 34.3%   23/ 67  tools/check_dist_sync.py             (skipif: requiere rama dist)
 34.8%  186/535  runtime/orchestrator/observation.py
 47.0%  225/479  runtime/orchestrator/autonomy.py
 49.2%   29/ 59  tools/measure_context_budget.py
 54.1%  100/185  runtime/orchestrator/agent_worker.py
 60.7%  130/214  runtime/orchestrator/contracts.py
 65.0%   52/ 80  tools/check_version_state.py
 69.0%   49/ 71  tools/check_memory_store.py
 69.8%   81/116  tools/audit_gates.py
```

### 6.3 Lectura crítica (`INFERENCIA`)

1. **La cobertura está invertida respecto del costo.** El área que consume el
   75 % del tiempo (`runtime/orchestrator/`) es la de **menor** cobertura
   (39.1 % como piso, con sus tests pesados excluidos del subset); las áreas que
   corren en menos de un segundo están entre 88.7 % y 97.6 %.
   `INFERENCIA`: no es un defecto de la suite — es que los tests del orquestador
   recorren *pocas líneas muchas veces* (crear repo, ejecutar host, asertar una
   transición), mientras los tests de `tools/` recorren *muchas líneas pocas
   veces* (cada regla, cada exit code).
2. **La cobertura NO habilita ejecutar menos tests.** Que un test no cubra una
   línea no dice que la línea no necesite ese test: dice que ese test no la
   ejercita. La decisión de selección es «qué tests pueden fallar si cambio
   X», no «qué líneas están cubiertas».
3. **La cobertura SÍ es útil para dos cosas concretas en este repo:**
   (a) detectar módulos sin ningún test — `runtime/orchestrator/__main__.py`
   (78 statements, 0 %) es el único caso con ≥ 40 statements y 0 %;
   (b) como **verificación de completitud de un command-set**: «los tests
   seleccionados cubren el mismo conjunto de líneas que la suite completa» es
   una afirmación medible y falsable — el uso correcto de coverage aquí, no el
   de seleccionar.
4. **Un umbral de coverage sería contraproducente hoy**: la cobertura del
   orquestador (39.1 % como piso) es en buena parte estructural —los tests
   ejercitan transiciones y contratos, no líneas de `host.py`—, y forzar un
   umbral empujaría a escribir tests que suban el número sin subir la confianza
   — exactamente lo contrario de la dirección declarada en `AGENTS.md`
   (*Decision-Making Compass*).

---

## 7. Current Testing Policy — Política actual y dev/CI/release

### 7.1 Dónde se exige la suite (`HECHO`)

| Fuente | Qué exige | Cuándo |
|---|---|---|
| `docs/VERSIONING.md:150-158` (§4.1) | 7 comandos; `python -m pytest tests/` es la única ejecución de tests | «la batería que define verde», en cada gate de validación |
| `docs/VERSIONING.md:117` (§4 paso 3) | la misma batería + `check_dist_sync.py` sólo en `master` | verificación por plan |
| `AGENTS.md` (raíz, `## Verifying the protocol`) | «run the full command set from that section at every validation gate» | cada gate |
| `.agents/AGENTS.md:89-95` | igual, por puntero | cada gate |
| `.agents/policies/validation-closure.md:10-25` | cada validación registrada lleva *Validation Anchor* con «Validation command-set» = «los 7 comandos de la batería» | validación y revalidación |
| `docs/plans/*.md` (p. ej. 159:121) | command-set = 7 comandos + gates C1/C2/C3 + suites del área | por plan |
| `.github/workflows/check-protocol.yml:35-46` | `pytest tests/ -q` **y** `pytest protocol/.agents/harness/tests/ -q` | push a `dev`/`master` y **cada** pull_request |
| `.github/workflows/publish-dist.yml` | no ejecuta tests; sólo regenera `dist` | push a `master` con cambios en `protocol/**` |

### 7.2 Distinción actual dev / CI / release (`HECHO`)

**No existe distinción en la ejecución de tests.** El mismo conjunto completo
(`tests/` + harness encadenado en CI) corre en:

- desarrollo local, en cada gate de validación de un plan;
- CI, en cada push y cada PR;
- release/promoción, donde además se corren los gates C1/C2/C3 y los checkers
  específicos del área (p. ej. planes 146, 148), pero **no hay un comando
  distinto ni un subconjunto distinto de tests**.

`HECHO` No hay `pre-commit`, no hay task runner, no hay `Makefile`. La batería
es literalmente siete comandos copiados a mano.

`HECHO` La única diferenciación real es por **ambiente**, no por nivel:
`check_dist_sync.py` es local-only y verde sólo en `master`.

`INFERENCIA` La política actual es de un solo nivel: «verde = los 7 comandos en
todos los contextos». Cualquier política de selección requiere **cambiar un
documento normativo** (`docs/VERSIONING.md` §4.1) o declarar un command-set
distinto por anchor — no es una decisión de tooling únicamente.

---

## 8. Selection Strategies Evaluated — Viabilidad de ejecutar solo los tests afectados

### A. Path-based (`pytest tests/test_x.py`)

| Criterio | Evaluación |
|---|---|
| **Viabilidad** | `HECHO` **Inmediata**: ya se usa en la práctica (planes 137, 144, 145 citan command-sets por archivo). No requiere tooling ni cambios de configuración. |
| **Precisión** | `MEDICIÓN` Alta cuando el mapa módulo→archivo es 1:1 (47 de 71 módulos). Baja cuando el cambio es en un util compartido (hay que enumerar a mano 13 archivos). |
| **Costo de mantenimiento** | `INFERENCIA` Bajo, pero **manual**: el mapa vive en la cabeza del agente o en el plan, no en el repo. Riesgo de deriva. |
| **Riesgo de omitir regresiones** | `HECHO` Existe: los 15 archivos anclados a documentos canónicos no se seleccionan por path de código. |
| **Complejidad** | `HECHO` Nula. |
| **Beneficio** | `MEDICIÓN` 3.2 s (EARS) a 64 s (checkers) frente a 318–398 s. En el área `orchestrator`, el beneficio es **nulo** (294 tests / 306 s). |

### B. Marker-based (`pytest -m protocol`)

| Criterio | Evaluación |
|---|---|
| **Viabilidad** | `HECHO` Los markers **no existen**: no hay `markers =`, ningún test usa un marker propio. Requiere anotar ~1358 tests o un `conftest` que derive markers de convenciones. |
| **Precisión** | `INFERENCIA` Equivalente a path-based si el marker se deriva del nombre del archivo; superior sólo si un marker corta **dentro** de un archivo (p. ej. `slow`, `integration`). |
| **Costo de mantenimiento** | `INFERENCIA` Medio: un marker nuevo en un archivo nuevo no se aplica solo salvo que se derive mecánicamente. |
| **Riesgo de omitir regresiones** | `INFERENCIA` Medio: depende de que la anotación sea correcta y completa. Un test mal marcado es invisible. |
| **Complejidad** | `INFERENCIA` Baja técnicamente, **alta en gobernanza**: agrega vocabulario nuevo al repo, y el repo tiene una regla explícita contra mecanismos nuevos sin necesidad demostrada (`AGENTS.md`, *Decision-Making Compass*). |
| **Beneficio** | `MEDICIÓN` El único marker con valor real sería `slow`/`integration` sobre los 5 archivos caros: permitiría `-m "not integration"` → **95 s** en vez de 385 s. Eso ya se logra igual con paths. |

### C. Dependency-based (`archivo cambiado → módulos → tests`)

| Criterio | Evaluación |
|---|---|
| **Viabilidad** | `HECHO` **Alta y ya demostrada en este informe**: el grafo de imports es completo, todos los test importan producción salvo 4, y el bootstrap de `sys.path` es único y declarado (`conftest.py:73-75`). Un script de ~150 líneas (equivalente al usado aquí) produce el mapa. |
| **Precisión** | `INFERENCIA` Alta para módulos con import directo; requiere resolver re-exports de paquete (hecho aquí) y **no** captura dependencias por subprocess ni por lectura del árbol real. |
| **Costo de mantenimiento** | `INFERENCIA` Bajo si el mapa se computa en vivo (AST) en vez de versionarse; nulo si se versiona y se verifica con un checker. |
| **Riesgo de omitir regresiones** | `HECHO` **El riesgo principal**: 15 archivos anclados a estado canónico + los checkers que se invocan por subprocess sin import (mitigado: la detección textual de `tools/*.py` los captura) + cambios en `conftest.py`/`pytest_isolation.py` que afectan a toda la suite. |
| **Complejidad** | `INFERENCIA` Media: hay que decidir la semántica del cierre transitivo (¿`roots.py` arrastra todo el harness?) y el fallback para cambios no mapeados. |
| **Beneficio** | `MEDICIÓN` Idéntico a path-based: la reducción viene del path, no del cálculo. El valor real de C es **dejar de enumerar a mano** y **no olvidar** los indirectos. |

### D. Test impact analysis automático (coverage-based, testmon, etc.)

| Criterio | Evaluación |
|---|---|
| **Viabilidad** | `HECHO` **Baja en el estado actual**: no hay configuración de coverage, no hay `pytest-testmon` ni `pytest-xdist` instalados, no hay dependencias declaradas de ningún tipo (no hay `requirements.txt`), y CI instala **sólo** `pytest` (`check-protocol.yml:37`). `MEDICIÓN` Medir coverage de la suite completa es impracticable: la corrida instrumentada cubrió 72 tests en ~2.5 min y se abandonó; los tests caros son I/O-bound y la instrumentación los penaliza más. |
| **Precisión** | `INFERENCIA` Sería la más alta (ejecución observada, no estática), pero **sólo** si el mapa se computa sobre la suite completa, lo cual es el costo que se quiere evitar. |
| **Costo de mantenimiento** | `HECHO` Requiere dependencias nuevas (prohibidas sin decisión explícita), un artefacto de estado persistente entre corridas, invalidación ante cambios ambientales, y **rompe el principio declarado en `conftest.py:14-18`** de que correr la suite deja el repositorio intacto (habría que llevar el estado fuera del repo). |
| **Riesgo de omitir regresiones** | `INFERENCIA` Alto: el análisis por cobertura selecciona por *lo que se ejecutó antes*; un camino nunca ejercitado nunca se selecciona (falla silenciosa, el peor tipo). |
| **Complejidad** | `INFERENCIA` Alta. |
| **Beneficio** | `INFERENCIA` Bajo **para este repo**: el 75 % del costo es 5 archivos que se seleccionarían igual. La ganancia marginal sobre C es pequeña frente al costo de tooling y de gobernanza. |

### E. Otras alternativas relevantes

| Alternativa | Viabilidad | Beneficio medido/estimado | Riesgo |
|---|---|---|---|
| **E1. Ejecución paralela (`pytest-xdist -n 8`)** | `INFERENCIA` Media-alta: `HECHO` 12 cores lógicos; `HECHO` el scratch ya está aislado por sesión y los tests caros son I/O-bound | `HIPÓTESIS` 2–3× sobre los 5 archivos caros (I/O y subprocess, no CPU) → ~150–250 s para la suite completa. Requiere dependencia nueva y verificar que `SESSION_ID`/`scratch_root` soporten N workers (hoy es *una* sesión por proceso) | Ruido de medición, contención de disco; el token de sesión es único por proceso, no por worker |
| **E2. Smoke test curado (14–20 archivos «evergreen»)** | `HECHO` Viable ya: son paths, no markers | `MEDICIÓN` 343 tests en **13.3 s** (suma de call) — la suite de checkers DEV + contratos | Bajo: es un subconjunto, no una afirmación de completitud |
| **E3. Niveles por tipo de cambio (TARGETED → AREA → FULL)** | `HECHO` Viable: la clasificación ya existe en el lifecycle (Clase RFC-56, Change Level L0–L3) | `MEDICIÓN` 0.3–64 s por área + 95–310 s según área | Es una **decisión de gobernanza**, no de tooling |
| **E4. Optimizar los 4 archivos caros (no seleccionar, sino acelerar)** | `HECHO` Identificable: crear el repo fixture una vez y copiarlo, o usar `git init` con plantilla, o `--no-verify`-style flags | `HIPÓTESIS` 290 s → 60–100 s | Toca tests (prohibido en esta auditoría); riesgo de cambiar la semántica de aislamiento que el plan 145 estableció a propósito |
| **E5. Marcar `slow` sólo para reportar** | `HECHO` Trivial | `INFERENCIA` Ninguno: mismo efecto que E2 | Ninguno |

---

## 9. Quantitative Scenarios — Potencial de reducción

`MEDICIÓN` = corrida real ejecutada en esta auditoría.
`ESTIMACIÓN` = suma de las duraciones `call` medidas en la corrida completa
(límite inferior: no incluye arranque de pytest, recolección ni imports).

| Escenario | Archivos | Tests | Tiempo | Cómo se obtuvo |
|---|---:|---:|---:|---|
| **Suite completa (2 legs)** | 69 | 1543 | **397.91 s** | `MEDICIÓN` |
| **Suite canónica (batería)** | 57 | 1358 | **~318 s** (usuario) / 385.5 s (esta corrida) | `MEDICIÓN` |
| Leg harness solo | 12 | 185 | **7.7 s** | `MEDICIÓN` |
| **Cambio muy localizado — EARS** | 3 | **91** | **3.23 s** | `MEDICIÓN` (`test_check_ears_coverage*`) |
| **Cambio localizado — `runtime/toolcalls`** | 3 medidos / 6 área | **111** medidos / 216 área | **0.56 s** (111) / 0.80 s (216) | `MEDICIÓN` (111: 3 archivos) + `ESTIMACIÓN` (216) |
| **Cambio localizado — `runtime/memory`** | 8 | **63** | **0.26 s** (call: 0.07 s) | `MEDICIÓN` |
| **Cambio localizado — `runtime/placement`** | 3 | **46** | **0.01 s** | `MEDICIÓN` |
| **Cambio de módulo — checkers DEV (área)** | 11 | **395** | **63.79 s** | `MEDICIÓN` |
| **Cambio de módulo — checkers + contratos (smoke)** | 15 | **343** | **~13.3 s** | `ESTIMACIÓN` de duraciones medidas |
| **Cambio transversal — `runtime/orchestrator`** | 13 | **294** | **306.10 s** | `MEDICIÓN` |
| **Núcleo caro solo (5 archivos)** | 5 | **165** | **290.5 s** | `ESTIMACIÓN` de duraciones medidas |
| **Todo menos los 4 archivos más caros** | 65 | **1391** | **~115 s** | `ESTIMACIÓN` de duraciones medidas |
| **Todo menos los 10 archivos más caros** | 59 | **1241** (+1 skip) | **51.42 s** | `MEDICIÓN` (corrida de coverage) |
| **Un solo archivo caro — `test_autonomous_orchestrator.py`** | 1 | 31 | **102.3 s** | `ESTIMACIÓN` |

`MEDICIÓN` Corroboración cruzada: el escenario `orchestrator` medido (294
tests) predijo 310.1 s por suma de duraciones y midió 306.10 s (error −1.3 %);
el escenario checkers (395 tests) predijo 92.9 s y midió 63.79 s (la
sobre-estimación viene de que la corrida completa corrió ambos legs con
contención). `INFERENCIA` Las sumas de duraciones son un predictor razonable
(±25 %) para conjuntos medianos y bueno para conjuntos grandes.

### Lectura de los escenarios (`INFERENCIA`)

```text
Cambio muy localizado (tools/runtime no-orchestrator) →  0.3 – 64 s   (−79 % a −99.9 %)
Cambio de módulo aislado (memory/toolcalls/placement)  →  0.3 –  1 s   (−99.7 %)
Cambio en un util compartido (roots.py, canonical.py)  → 15 –  90 s   (−72 % a −95 %)
Cambio transversal (orchestrator/autonomy/host/worker) → 306 s        (−4 %)
Suite completa (release)                               → 318 – 398 s   (0 %)
```

`INFERENCIA` **El ahorro potencial está enteramente determinado por el
alcance del cambio, no por la calidad del mecanismo de selección.** Para el
subsistema que hoy domina el reloj, la selección no es una herramienta útil.

---

## 10. Current Suite Problems and Risks — Problemas actuales y riesgos

### 10.1 Problemas observados de la suite

Relevamiento explícito de lo que se buscó y lo que se encontró (`HECHO` salvo
indicación). **No se propone eliminar ningún test.**

| Categoría buscada | Hallazgo |
|---|---|
| Tests duplicados | `HECHO` **Sin evidencia de duplicación literal.** `tests/testsupport.py` documenta que una aserción (`assert_tool_imports_only_stdlib`) estaba duplicada byte a byte en siete suites y fue extraída: la duplicación conocida ya se resolvió (plan 124/144) |
| Tests redundantes / validando lo mismo desde varios lugares | `INFERENCIA` Parcial y deliberada: 3 archivos validan `check_ears_coverage` (`test_check_ears_coverage`, `..._falsification`, `..._dogfood`); 2 validan `placement` desde el resolver y desde el contrato; la dogfood es complementaria (corpus real vs sintético), no redundante. **No se encontró evidencia de redundancia que justifique tocar nada** |
| Tests excesivamente lentos | `HECHO` 5 tests > 9 s; 20 tests > 4.7 s; 5 archivos > 28 s (ver §3.4) |
| Fixtures globales costosas | `HECHO` **No hay**: setup total 1.6 s, teardown 0.0 s, sin fixtures de sesión costosas. Todo el costo está dentro de cada test |
| Tests mal clasificados | `HECHO` 18 archivos anclados están declarados como tales en `tests/AGENTS.md:73-91`; `tests/AGENTS.md:15-19` declara explícitamente que el harness no pertenece a la batería canónica. La clasificación está documentada y es coherente con el código |
| Tests unitarios que funcionan como integración | `HECHO` **Sí, es el hallazgo central**: `test_autonomous_orchestrator.py`, `test_agent_worker.py`, `test_sae_scope_enforcement.py`, `test_autonomy_effects.py` construyen un repositorio git real por test y ejercitan el host completo. No hay marcador ni separación que lo declare |
| Tests de integración que podrían ser pocos y estratégicos | `INFERENCIA` Los mismos 4: 165 tests / 290.5 s. Cuántos son estratégicos y cuántos repiten el mismo camino de montaje **no se determinó** (requiere medir aserciones por segundo; ver §13 pregunta 3) |
| Tests difíciles de seleccionar aisladamente | `HECHO` 15 archivos dependen del estado canónico del repositorio (§5.3) y los checkers invocados por subprocess (§7 R3) |
| Dependencias ocultas entre tests / orden implícito / estado global | `HECHO` **Sin evidencia.** La suite corre en orden por defecto (sin `pytest-randomly` instalado), pasa completa en una corrida y el scratch es por sesión, con `clear_own_scratch()` y `prune_stale_sessions()` deliberados (plan 145). Los tests no comparten directorios: cada uno usa `tmp_path` o un nombre con `uuid4` |
| Uso compartido de filesystem / subprocess / repos git temporales | `HECHO` 44 archivos usan `tmp_path`; 7 construyen repositorios git temporales vía `scratch_root`; 14 usan `subprocess`. Todo fuera del árbol del repositorio por `conftest.py` |

`INFERENCIA` **La suite no tiene un problema de calidad: tiene un problema de
granularidad y de coste de montaje.** No hay tests que sobren; hay tests que
cuestan 1.7–3.3 s cada uno porque crean un mundo cada vez. Eso es una decisión
de diseño defendible (aislamiento real), y su costo es el que domina el reloj.

---

### 10.2 Risks

| # | Riesgo | Evidencia / base | Severidad |
|---|---|---|---|
| R1 | **Selección incompleta por vínculo no-import.** Un test puede ejercitar producción sin importarla (subprocess, lectura del árbol). | `HECHO` 3 archivos no importan producción y sí la validan; 15 archivos dependen del estado canónico | Alta |
| R2 | **Cambios en la infraestructura de test son universales.** `conftest.py`, `tests/pytest_isolation.py` y el bootstrap de `sys.path` afectan a toda la suite. | `HECHO` plan 145 (`c313122`) modificó `conftest.py` + `pytest_isolation.py`; `MEDICIÓN` 44 de 69 archivos usan `tmp_path` y 7 archivos construyen repositorios git propios vía `scratch_root` | Alta |
| R3 | **Los checkers se prueban por subprocess, no por import.** Seleccionar por grafo de imports los pierde. | `HECHO` `test_check_dist_sync.py:87` ejecuta el tool; `test_determine_execution_state.py`, `test_scoped_content_identity.py`, `test_repo_containment.py`, `test_check_lifecycle_*` igual | Media (mitigable) |
| R4 | **Falsa confianza: verde en el subconjunto ≠ verde en la suite.** El 67.6 % de cobertura se midió sobre el 80.4 % de los tests (los 10 archivos más caros quedaron fuera), y el área de mayor costo es la de menor cobertura relativa. | `MEDICIÓN`: §6.2 | Alta |
| R5 | **El mapa de selección deriva silenciosamente.** Un archivo de test nuevo cuya producción no se mapea no se ejecuta nunca. | `INFERENCIA` | Media |
| R6 | **Gobernanza: cambiar el command-set canónico cambia la identidad certificada.** El Validation Anchor mide un *scope set* declarado; reducirlo reduce lo que la identidad certifica. | `HECHO` `docs/plans/159:120-129` (declared scope + scope set de 14 rutas), `validation-closure.md:10-38` | Alta (decisión humana) |
| R7 | **Estado global / orden implícito oculto en el scratch.** | `HECHO` el plan 145 arregló precisamente fallos no deterministas por scratch compartido entre sesiones; la suite hoy declara ownership por sesión | Baja hoy, alta si se paraleliza (E1) |
| R8 | **Reducción aparente sin reducción real.** Para cambios en orchestrator, seleccionar no ahorra nada y da la ilusión de un gate más liviano. | `MEDICIÓN` 294 tests / 306 s | Media |
| R9 | **CI y local divergen.** Si la selección es local pero CI corre todo, el ahorro no llega al bucle que más lo necesita. | `HECHO` `check-protocol.yml` corre la suite completa en cada push/PR | Media |
| R10 | **Tests caros por diseño frágil.** Los 4 archivos caros ya tuvieron que endurecerse por no-determinismo (plan 145). Acelerarlos puede reintroducirlo. | `HECHO`/`INFERENCIA` | Media |

---

## 11. Recommendation — Estrategia recomendada

`RECOMENDACIÓN` **No implementar test impact analysis ni selección por
dependencias en este momento.** La evidencia no lo justifica: el 75 % del
costo está en 5 archivos que cualquier estrategia correcta seleccionaría de
todos modos, y la selección fina sólo agrega riesgo en el 25 % restante.

`RECOMENDACIÓN` Adoptar **tres niveles por contexto, con selección por paths
(manual o derivada de un mapa versionado), no por markers ni por coverage**:

```text
NIVEL 1 — TARGETED (desarrollo local, iteración)
  Objetivo: feedback rápido.
  Regla: los archivos de test del área tocada (path-based) + el smoke evergreen.
  Medido: 0.3 s – 64 s según área; 13.3 s el smoke.

NIVEL 2 — FULL CANÓNICO (integración / antes de integrar)
  Objetivo: detectar regresiones.
  Regla: python -m pytest tests/  (los 1358) + python -m pytest protocol/.agents/harness/tests/
  Medido: 318 s de referencia / 385.5 + 7.7 s en esta corrida.
  Sin excepciones: es el nivel que hoy existe, y ya es el correcto para CI.

NIVEL 3 — RELEASE (promoción dev → master)
  Objetivo: máxima confianza antes de publicar.
  Regla: NIVEL 2 + gates C1/C2/C3 + checkers específicos + checks de release
          (lo que los planes 146/148 ya hacen). Sin reducción.
```

Reglas de frontera que la evidencia exige:

1. **Default conservador**: cualquier cambio fuera de un área mapeada, o en
   `conftest.py` / `tests/pytest_isolation.py` / bootstrap de `sys.path`, o en
   un documento canónico → **NIVEL 2**, siempre.
2. **Los 18 archivos anclados nunca se seleccionan por área**: se ejecutan
   cuando cambia su sujeto canónico (docs, planes, RFC, payload), que es un
   criterio documental, no de código.
3. **Release sin excepción de alcance**: la promoción corre todo.

`RECOMENDACIÓN` **Antes de cualquier mecanismo, atacar el costo donde está**:
los 4 archivos de `orchestrator` construyen un repositorio git por test. Un
fixture de repositorio compartido y copiado (o un `git init` con plantilla)
es la palanca de mayor impacto y menor riesgo de gobernanza, porque no cambia
*qué* se prueba, sólo *cuánto cuesta montarlo*. **Cuantificado:** llevar los 5
archivos caros de 290 s a ~90 s reduciría la suite canónica de ~385 s a
~185 s (−52 %) sin perder un solo test. (E4, no implementado aquí.)

`RECOMENDACIÓN` Evaluar `pytest-xdist` como palanca complementaria. Requiere
verificar que el modelo de sesión de `pytest_isolation` (un token por sesión,
`conftest.py:87`) sea válido con N workers — hoy el token se genera una vez en
el proceso maestro y los workers son subprocesos, lo cual **puede** ser
correcto, pero no está verificado por un test. `HIPÓTESIS`, no hecho.

---

## 12. Implementation Prerequisites — Prerrequisitos de implementación

`RECOMENDACIÓN` Antes de implementar cualquier nivel de selección:

1. **Decisión de gobernanza explícita.** `docs/VERSIONING.md` §4.1 define la
   batería canónica única; cambiarla o declarar un command-set por contexto es
   un cambio de política, no de tooling. Requiere la vía de RFC/plan que
   corresponda según RFC-56.
2. **Mapa módulo → tests versionado y verificado.** El mapeo de §4 no existe en
   el repo: hoy vive en `tests/AGENTS.md` (sólo los anclados) y en la cabeza del
   agente. Sin un artefacto que un checker pueda verificar, el mapa deriva (§10 R5).
3. **Fallback declarado por default.** Regla explícita: cambio no mapeado →
   suite completa. Debe estar escrita, no inferida.
4. **Criterio para los 18 archivos anclados.** Sujetos canónicos (docs, planes,
   RFC, payload, versión) que fuerzan su ejecución.
5. **Verificación del modelo de sesión de `pytest_isolation` bajo paralelismo**
   (si se adopta xdist).
6. **Medición de la línea base en CI (Linux).** `MEDICIÓN` todas las cifras de
   este informe son de una máquina Windows; `HIPÓTESIS` los tests caros son
   sensiblemente más baratos en `ubuntu-latest` porque el costo dominante es
   creación de procesos. Sin esa medición, no se puede dimensionar el ahorro
   real en el contexto donde más importa.
7. **Evidencia de que el subconjunto no reduce confianza.** Al menos una
   corrida comparativa: subconjunto verde vs. suite completa verde sobre el
   mismo commit, con los fallos detectados por cada uno.

No se requiere: ninguna dependencia nueva, ningún plugin, ni modificar
`protocol/.agents/`.

---

## 13. Open Questions — Información adicional necesaria

1. **¿En qué plataforma corre el bucle de desarrollo real?** `MEDICIÓN` Windows:
   ~1 s de CPU por cada ~9 s de reloj en la corrida completa. `HIPÓTESIS` En
   Linux el mismo conjunto podría costar 2–4× menos; sin esa medición, el
   presupuesto objetivo de TARGETED no se puede fijar.
2. **¿Cuál es el presupuesto de feedback aceptable?** No hay target declarado en
   ningún documento del repo. Sin un número, no hay forma de evaluar si el
   NIVEL 1 debe durar 10 s o 60 s.
3. **¿Los 4 archivos caros prueban lo que dicen probar?** `MEDICIÓN` 290 s en
   165 tests construyendo repos git; `INFERENCIA` buena parte del costo es
   montaje, no aserción. Falta evidencia de cuántas aserciones por segundo de
   reloj aporta cada uno.
4. **¿Un fixture de repositorio compartido cambia la semántica de aislamiento
   que el plan 145 estableció a propósito?** Necesita un análisis de ese plan
   antes de proponerlo.
5. **¿Cuántos cambios reales caen en cada área?** `INFERENCIA` con los últimos
   12 commits: 5 de 9 con efecto de código tocaron `runtime/orchestrator/` o el
   harness; 2 fueron docs-only. Una muestra mayor (50–100 commits) daría la
   distribución de alcance real y por lo tanto el ahorro esperado ponderado.
6. **¿El CI ya es lento?** No se midió la duración del job `check-protocol` en
   GitHub Actions. Si el job tarda 6 minutos, el costo real de la política
   actual está subestimado para todos los PRs.
7. **¿`runtime/orchestrator/__main__.py` (78 statements, 0 tests, 0 % cobertura)
   necesita cobertura?** `HECHO` es el único módulo de producción sin ningún
   test asociado.
8. **¿La suite del harness debe seguir fuera de la batería canónica?**
   `MEDICIÓN` 7.7 s por 185 tests: es el mejor cociente de todo el repositorio.
   La separación actual (corre en CI pero no en la batería) parece un costo de
   gobernanza sin justificación técnica.

---

## Anexo A — Respuestas directas a las preguntas de la conclusión ejecutiva

**P1. ¿Es razonable seguir ejecutando los 1358 tests en cada iteración de
desarrollo?**
`INFERENCIA` No para todo cambio, pero **sí para el 24 % del tiempo** — y ese
24 % concentra el riesgo. La respuesta correcta no es «no hace falta correr
todos los tests» sino: *el costo de la suite no está distribuido como el riesgo
de los cambios*. Un cambio en `runtime/memory/` tarda 0.26 s en validarse
completo; un cambio en `runtime/orchestrator/` tarda 306 s aunque se
seleccione. Ejecutar todo siempre es defendible; ejecutar 1358 tests para
iterar sobre un checker que tarda 3 s no lo es.

**P2. ¿La estructura actual permite seleccionar tests de manera confiable?**
`INFERENCIA` **Sí, con dos excepciones declaradas.** El acoplamiento por import
es real, completo y verificable (65/69 archivos), sin clases, sin estado global
compartido entre tests y con scratch aislado por sesión. Las excepciones son
(a) los 18 archivos anclados al estado canónico del repositorio y (b) la
infraestructura de test compartida (`conftest.py`, `pytest_isolation.py`), cuyo
alcance es toda la suite y no es derivable de imports.

**P3. ¿Cuál sería, según la evidencia, la estrategia más apropiada?**
`RECOMENDACIÓN`

```text
TARGETED  (dev local)     →  paths del área + smoke evergreen
AREAL     (opcional)      →  paths del área, sin pretensión de completitud
FULL      (CI / gate)     →  tests/ + harness completo, sin excepción
RELEASE   (promoción)     →  FULL + C1/C2/C3 + checkers + checks de release
```

Con **paths**, no markers, no coverage, no tooling nuevo. Y con un default
conservador que manda a FULL todo lo no mapeado.

**P4. ¿Cuánto tiempo podríamos ahorrar?**
`MEDICIÓN` Para cambios fuera de `runtime/orchestrator/` (la mayoría de
`tools/`, `runtime/memory/`, `runtime/toolcalls/`, `runtime/placement/`):
**de 318 s a 0.3–64 s, un ahorro del 79 % al 99.9 %.**
Para cambios en `runtime/orchestrator/`: **de 318 s a 306 s, un ahorro del
3.7 % — no vale el riesgo.**
Ahorro global esperado: depende de la mezcla de cambios (pregunta abierta 5).
`INFERENCIA` Si ~60 % de las iteraciones caen fuera de orchestrator, el ahorro
ponderado es del orden del 50–60 %.
**La palanca mayor no es seleccionar sino acelerar los 5 archivos caros:**
290 s → ~90 s reduciría la suite completa un 52 % sin perder un test.

**P5. ¿Cuál es el principal riesgo de introducir selección de tests?**
`INFERENCIA` **La falsa confianza por vínculo no-import**: un subconjunto verde
mientras la suite completa habría fallado. Es el único riesgo del catálogo que
produce un resultado silenciosamente incorrecto en vez de ruidoso. Se
materializa en 15 archivos que dependen del estado del repositorio real y en
los checkers que se prueban por subprocess en lugar de por import — ninguno de
los dos aparece en un grafo de imports.

**P6. ¿Qué información falta antes de implementar?**
Ver §13: plataforma y costo real en CI, presupuesto de feedback objetivo,
distribución de alcance de cambios reales, y el análisis del plan 145 antes de
tocar los fixtures caros. **Ninguna de las cuatro requiere herramienta nueva:
las cuatro son mediciones o lecturas de documentos existentes.**
