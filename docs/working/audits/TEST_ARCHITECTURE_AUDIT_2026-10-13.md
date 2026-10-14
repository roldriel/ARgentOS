# Test Architecture Audit — ARgentOS DEV

```text
RESULT = TEST_ARCHITECTURE_AUDIT
SCOPE = tests/ (57 files), protocol/.agents/harness/tests/ (12 files), conftest.py,
        tests/pytest_isolation.py, tests/testsupport.py, tests/fixtures/,
        tools/ (20 production scripts), runtime/ (43 modules),
        protocol/.agents/harness/ (8 production modules), CI workflows
TEST_FILES = 69
TEST_COUNT = 1543 collected (1358 DEV + 185 protocol harness); 1542 passed, 1 skipped
SLOWEST_GROUPS = tests/test_autonomous_orchestrator.py (97.30 s / 31),
                 tests/test_agent_worker.py (73.53 s / 41),
                 tests/test_sae_scope_enforcement.py (60.42 s / 44),
                 tests/test_autonomy_effects.py (50.93 s / 36),
                 tests/test_check_lifecycle_checkpoint.py (30.06 s / 32)
PRIMARY_CONCENTRATION = runtime/orchestrator/ (autonomy.py, host.py, agent_worker.py)
                        — 184 tests in 5 files = 11.9 % of tests, 77.6 % of call time
PRIMARY_COST_DRIVERS = throw-away git repository construction per test (254 builder
                       call sites), real subprocess effects inside the host loop, and
                       per-test interpreter launches (23 sys.executable sites)
ISOLATION_CANDIDATES = 24 files labelled POSSIBLE SPLIT / 2 POSSIBLE ISOLATION, but only
                       6 files with genuinely separable pure-logic halves; the 4 dominant
                       files cannot be de-integrated without losing their guarantee
OPTIMIZATION_CANDIDATES = tests/test_autonomous_orchestrator.py, test_agent_worker.py,
                          test_sae_scope_enforcement.py, test_autonomy_effects.py
                          (git-repo setup repeated per test), tests/test_check_lifecycle_checkpoint.py,
                          tests/test_check_plan_citations.py / test_check_lifecycle_lineage.py
                          (per-test interpreter launches for exit codes)
TARGETED_SELECTION_READINESS = high for 47 of 69 files (import-coupled, synthetic fixtures);
                               requires a declared global category for 22 files
ARCHITECTURE_RECOMMENDATION = keep the single canonical battery for CI and release; add a
                              TARGETED level by path plus a declared ANCHORED category; do not
                              introduce markers, coverage-based selection or new dependencies
NEXT_STEP = decide whether to (1) split the pure-logic halves of the 6 isolatable files,
            (2) attack the git-repo setup cost in the 4 dominant files, or (3) do neither —
            this audit authorises nothing and recommends no change on its own
```

**Clase documental:** Working / Audit (provenance) — **no normativo**.
**Naturaleza:** auditoría estructural (diagnóstico) de la arquitectura de la suite de tests.
**Autoridad de este documento:** ninguna. Registra hechos, mediciones, inferencias e
hipótesis. No crea mecanismos, no modifica la suite, no autoriza trabajo, no decide
política de testing y no reduce la suite canónica.
**Fecha:** 2026-10-13 · **Rama:** `dev` · **HEAD:** `fb0786a0b9b872796e5e4b223cf92bc011c22139`
**Restricción cumplida:** no se modificó código productivo, tests, fixtures, `conftest.py`,
configuración de pytest, CI, dependencias, scripts, estructura de directorios ni
documentación normativa. Este informe y su registro en el INDEX son los únicos archivos
creados.

**Relación con `TEST_SUITE_AUDIT_2026-10-13.md`.** Ese documento es un relevamiento de
*estrategia y costo* (medición, blast radius, viabilidad de selección, coverage). Este
documento es una auditoría *estructural* distinta: clasifica el nivel real de cada archivo,
mapea `test → comportamiento → componente`, detecta solapamiento y responsabilidades
cruzadas, y evalúa aislamiento y selección targeted. **Los dos conjuntos de cifras son
independientes y coinciden**: la recolección de pytest da exactamente los mismos totales
(1358 + 185 = 1543) y el tiempo total medido hoy (408.95 s de reloj, 402.31 s de fase
`call`) es consistente con los 397.91 s de aquel informe dentro del ruido de máquina. El
sujeto medido no cambió.

**Marcas usadas en todo el documento**

| Marca | Significado |
|---|---|
| `HECHO` | observado directamente en el repositorio (lectura, glob, grep, AST) |
| `MEDICIÓN` | obtenido ejecutando la suite o un micro-benchmark en esta máquina |
| `INFERENCIA` | conclusión derivada de hechos/mediciones, no observada directamente |
| `HIPÓTESIS` | conjetura explícita, no verificada |
| `RECOMENDACIÓN` | propuesta de acción, **no implementada** |

**Reproducibilidad.** Todos los números de este informe se reproducen con:

```text
# 1. recolección y conteo exacto por archivo
python -m pytest tests/ --collect-only -q
python -m pytest protocol/.agents/harness/tests/ --collect-only -q

# 2. corrida completa con duración por test (fase call/setup/teardown)
python -m pytest tests/ protocol/.agents/harness/tests/ -q -p no:cacheprovider \
    --durations=0 --durations-min=0

# 3. inventario estático (imports de producción, fixtures, uso de git/subprocess/tmp_path)
#    y mapeo test → comportamiento → componente: análisis por AST de los 69 archivos
#    contra los 71 módulos de producción. Ningún dato de este informe depende de
#    coverage ni de una herramienta nueva.
```

---

## 1. Executive Summary

`MEDICIÓN` La suite completa (los dos legs) corrió en **408.95 s**; la fase `call`
acumuló **402.31 s**, `setup` **1.71 s** y `teardown` **0.01 s**. Resultado:
`1542 passed, 1 skipped` (el skip es `tests/test_pytest_isolation.py:159:
cacheprovider disabled for this session`, causado por `-p no:cacheprovider`).

`MEDICIÓN` **5 de 69 archivos (7.2 %) contienen 184 de 1543 tests (11.9 %) y consumen
312.24 s = 77.6 % del tiempo de la fase `call`.** Diez archivos explican el 91.3 %; veinte
explican el 97.4 %. La mediana por test es **0.000 s** y el p95 es **1.12 s**: el costo no
está distribuido, está concentrado, y **18 archivos no registran duración alguna**.

`HECHO` La concentración **no** es un problema de cantidad de tests ni de cobertura: es
**costo de montaje dentro de cada test**. Los 4 archivos dominantes construyen un
repositorio git nuevo por test (`make_repo`/`build_repo`: 23, 32, 14 y 16 sitios de llamada
respectivamente) y luego ejecutan el host completo, que a su vez lanza subprocesos reales
de verificación. `MEDICIÓN` del primitivo en esta máquina: `git init` + `add` + `commit` de
un repositorio vacío cuesta **0.340 s** (media de 8), mientras que el arranque de un
intérprete Python cuesta **0.050 s** (media de 5). El costo dominante es **creación de
procesos `git`**, no cómputo ni arranque de intérprete.

`HECHO` La clasificación honesta de niveles contradice parcialmente la intuición de que
"los tests del orquestador son unitarios" — pero también contradice la intuición opuesta:

| Nivel real | Archivos | Tests | Tiempo `call` |
|---|---:|---:|---:|
| COMPONENT | 28 | 707 | 41.23 s |
| **MIXED** | **20** | **585** | **337.44 s** |
| INTEGRATION | 5 | 78 | 16.17 s |
| DOCUMENT_CERTIFICATION | 5 | 26 | 6.13 s |
| UNIT | 5 | 41 | 0.03 s |
| CONTRACT | 4 | 95 | 0.01 s |
| END_TO_END | 1 | 3 | 1.30 s |

`INFERENCIA` **La mayoría de la suite ya está en el nivel correcto.** 609 tests en 23
archivos son COMPONENT y cuestan 10.64 s en total; 41 tests en 5 archivos son UNIT puros y
cuestan 0.03 s. El problema no es que "todo sea integración": es que **20 archivos contienen
dos niveles en uno** — una mitad de lógica pura y una mitad de integración real — y esa
mezcla es lo que impide seleccionar, aislar y optimizar con precisión.

`INFERENCIA` **El aislamiento es una palanca menor de lo que sugiere el conteo de
candidatos.** 24 archivos están etiquetados `POSSIBLE SPLIT`, pero sólo 6 tienen una mitad
pura genuinamente separable con ganancia real, y **ninguno de los 4 archivos dominantes es
de-aislable**: su garantía (`Closed` derivado de evidencia real, violación de scope detenida
*antes* del efecto, techo de recursos leído del journal) existe sólo cuando hay un
repositorio real, un journal real y un host real cableados.

`INFERENCIA` **La palanca real es doble y asimétrica.** Para los 4 archivos dominantes
(312.24 s → visiblemente reducible reutilizando el montaje del repositorio, sin tocar
ninguna aserción): es *optimización*. Para los 2 archivos con interpretadores por test
(`test_check_lifecycle_lineage.py`: ~40 lanzamientos; `test_check_plan_citations.py`: 3):
es *aislamiento de la frontera de proceso*. Para todo lo demás: es *selección targeted*.

`RECOMENDACIÓN` Tres conclusiones, ninguna implementada aquí: (a) **no** convertir tests de
integración en unitarios — la integración es la garantía en los 5 archivos que la necesitan;
(b) separar la mitad pura de los 6 archivos de nivel mixto que sí la tienen, para que la
selección por path sea precisa; (c) atacar el costo de montaje de los 4 archivos dominantes
antes que cualquier mecanismo de selección, porque la selección **no ayuda** en el área que
domina el reloj.

---

## 2. Inventario

### 2.1 Composición de la suite (`HECHO` + `MEDICIÓN`)

| Leg | Archivos | Tests recogidos | Tiempo `call` | Comando |
|---|---:|---:|---:|---|
| **DEV** (`tests/`) — batería canónica | 57 | **1358** | 395.26 s | `python -m pytest tests/` |
| **PROTOCOL HARNESS** (`protocol/.agents/harness/tests/`) | 12 | **185** | 7.05 s | `python -m pytest protocol/.agents/harness/tests/` |
| **Total** | **69** | **1543** | **402.31 s** | ambos legs |

`HECHO` No hay un tercer conjunto: `pytest --collect-only` sin argumentos recolecta 1358
(el directorio `.agents` empieza con punto y el `norecursedirs` por defecto excluye
directorios ocultos, por lo que el leg del harness no se autodescubre desde la raíz).

### 2.2 Taxonomía operativa usada en esta auditoría

Se distinguen las categorías que el pedido exige, **derivadas de evidencia y no de la
ubicación** (ver §3 para el método):

| Categoría | Definición operativa | Archivos | Tests |
|---|---|---:|---:|
| **UNIT** | función pura, sin colaborador real, sin proceso | 5 | 41 |
| **COMPONENT** | un módulo por su API pública con colaboradores reales (filesystem/`tmp_path`), sin proceso externo | 28 | 707 |
| **CONTRACT** | un contrato publicado, un esquema, o una interfaz *entre* artefactos (incluye detección estática de wiring) | 4 | 95 |
| **DOCUMENT/CERTIFICATION** | el estado documental canónico del repositorio real (planes, RFC, INDEX, payload, versión) | 5 | 26 |
| **INTEGRATION** | varios módulos productivos reales cableados en proceso, con efectos reales | 5 | 78 |
| **END_TO_END** | de entrada real a efecto observable, cruzando fronteras de proceso | 1 | 3 |
| **MIXED** | el archivo contiene genuinamente más de un nivel | 20 | 585 |

`HECHO` **65 de 69 archivos** importan al menos un módulo productivo. Los 4 que no lo hacen
no son un defecto: 3 de ellos validan **documentos** (texto) y 1 valida un **contrato
estático de wiring**; su vínculo con la producción es textual o por firma, no por import.

### 2.3 Inventario por archivo

Claves: `tests` = casos recogidos por pytest; `call_s` = tiempo de fase `call` medido;
`mec` = mecanismo de integración dominante (`—` ninguno; `FS` filesystem/`tmp_path`;
`GIT` repositorio git; `TREE` árbol real del repositorio; `PROC` subproceso/CLI;
`MM` varios módulos productivos en proceso); `nivel` = nivel real (§2.2).

**Leg DEV — `tests/` (57 archivos, 1358 tests, 395.26 s)**

| Archivo | tests | call_s | ms/test | mec | nivel | candidato |
|---|---:|---:|---:|:--:|---|---|
| `tests/test_autonomous_orchestrator.py` | 31 | 97.30 | 3138.7 | GIT | MIXED | POSSIBLE SPLIT |
| `tests/test_agent_worker.py` | 41 | 73.53 | 1793.4 | GIT | MIXED | POSSIBLE SPLIT |
| `tests/test_sae_scope_enforcement.py` | 44 | 60.42 | 1373.2 | GIT | MIXED | POSSIBLE SPLIT |
| `tests/test_autonomy_effects.py` | 36 | 50.93 | 1414.7 | GIT | MIXED | POSSIBLE SPLIT |
| `tests/test_check_lifecycle_checkpoint.py` | 32 | 30.06 | 939.4 | GIT | COMPONENT | KEEP AS INTEGRATION |
| `tests/test_autonomous_scope.py` | 67 | 14.68 | 219.1 | GIT | MIXED | POSSIBLE SPLIT |
| `tests/test_scoped_content_identity.py` | 17 | 12.65 | 744.1 | PROC | INTEGRATION | KEEP AS INTEGRATION |
| `tests/test_sae_scope_enforcement_dogfood.py` | 13 | 11.90 | 915.4 | GIT | MIXED | POSSIBLE SPLIT |
| `tests/test_determine_execution_state.py` | 69 | 11.29 | 163.6 | FS | MIXED | POSSIBLE SPLIT |
| `tests/test_check_lifecycle_lineage.py` | 35 | 4.71 | 134.6 | PROC | COMPONENT | POSSIBLE SPLIT |
| `tests/test_autonomous_scope_dogfood.py` | 7 | 4.70 | 671.4 | TREE | DOC_CERT | KEEP AS CONTRACT |
| `tests/test_check_dist_sync.py` | 7 | 4.23 | 604.3 | GIT | MIXED | KEEP AS INTEGRATION |
| `tests/test_autonomy_effects_dogfood.py` | 13 | 3.05 | 234.6 | TREE | MIXED | KEEP AS CONTRACT |
| `tests/test_pytest_isolation.py` | 22 | 3.04 | 138.2 | MM | MIXED | POSSIBLE SPLIT |
| `tests/test_check_ears_coverage_dogfood.py` | 18 | 2.21 | 122.8 | TREE | MIXED | POSSIBLE SPLIT |
| `tests/test_check_discovery_output.py` | 48 | 1.42 | 29.6 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_check_lifecycle_anchor.py` | 23 | 1.39 | 60.4 | TREE | MIXED | POSSIBLE SPLIT |
| `tests/test_repo_containment.py` | 1 | 1.11 | 1110.0 | GIT | DOC_CERT | KEEP AS CONTRACT |
| `tests/test_discovery_output_dogfood.py` | 14 | 0.86 | 61.4 | TREE | MIXED | POSSIBLE SPLIT |
| `tests/test_check_session_artifacts.py` | 60 | 0.79 | 13.2 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_check_plan_structure.py` | 28 | 0.67 | 23.9 | FS | MIXED | KEEP AS COMPONENT |
| `tests/test_check_protocol_invariants.py` | 30 | 0.66 | 22.0 | PROC | MIXED | POSSIBLE SPLIT |
| `tests/test_check_ears_coverage.py` | 38 | 0.66 | 17.8 | MM | COMPONENT | KEEP AS COMPONENT |
| `tests/test_check_taxonomy_coherence.py` | 28 | 0.64 | 22.9 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_check_plan_citations.py` | 37 | 0.48 | 13.7 | FS | MIXED | POSSIBLE SPLIT |
| `tests/test_measure_context_budget.py` | 6 | 0.37 | 61.7 | PROC | MIXED | POSSIBLE SPLIT |
| `tests/test_check_ears_coverage_falsification.py` | 25 | 0.33 | 13.8 | — | MIXED | POSSIBLE SPLIT |
| `tests/test_root_contract.py` | 10 | 0.32 | 32.0 | TREE | DOC_CERT | POSSIBLE SPLIT |
| `tests/test_aggregate_metrics.py` | 32 | 0.31 | 9.7 | FS | COMPONENT | POSSIBLE SPLIT |
| `tests/test_canonical_materialization_v2.py` | 42 | 0.21 | 5.0 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_project_segment.py` | 37 | 0.11 | 3.0 | MM | MIXED | POSSIBLE SPLIT |
| `tests/test_segment_resolution.py` | 56 | 0.08 | 1.4 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_check_architecture_traceability.py` | 8 | 0.03 | 3.8 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_memory_store.py` | 9 | 0.03 | 3.3 | FS | UNIT | KEEP AS UNIT |
| `tests/test_fc_flow.py` | 22 | 0.02 | 0.9 | MM | INTEGRATION | POSSIBLE SPLIT |
| `tests/test_prompt_cache_dogfood.py` | 18 | 0.02 | 1.1 | TREE | COMPONENT | POSSIBLE ISOLATION |
| `tests/test_check_version_state.py` | 8 | 0.02 | 2.5 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_fc_host_integration.py` | 5 | 0.01 | 2.0 | MM | CONTRACT | KEEP AS CONTRACT |
| `tests/test_check_memory_store.py` | 7 | 0.01 | 1.4 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_change_governance.py` | 11 | 0.01 | 0.9 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_memory_operational_retrieval_archive.py` | 7 | 0.00 | 0.0 | — | COMPONENT | KEEP AS COMPONENT |
| `tests/test_audit_gates.py` | 10 | 0.00 | 0.0 | — | COMPONENT | POSSIBLE ISOLATION |
| `tests/test_fc_isolation_declaration.py` | 4 | 0.00 | 0.0 | TREE | DOC_CERT | KEEP AS CONTRACT |
| `tests/test_memory_synthesis_consolidation.py` | 10 | 0.00 | 0.0 | MM | COMPONENT | KEEP AS COMPONENT |
| `tests/test_fc_recovery_alignment.py` | 4 | 0.00 | 0.0 | TREE | DOC_CERT | KEEP AS CONTRACT |
| `tests/test_toolcalls.py` | 12 | 0.00 | 0.0 | FS | COMPONENT | KEEP AS COMPONENT |
| `tests/test_adversarial_deliberation.py` | 75 | 0.00 | 0.0 | — | CONTRACT | POSSIBLE SPLIT |
| `tests/test_placement_contract_drift.py` | 9 | 0.00 | 0.0 | TREE | CONTRACT | KEEP AS CONTRACT |
| `tests/test_placement_dogfood.py` | 6 | 0.00 | 0.0 | TREE | CONTRACT | KEEP AS CONTRACT |
| `tests/test_canonical_materialization.py` | 51 | 0.00 | 0.0 | MM | MIXED | POSSIBLE SPLIT |
| `tests/test_placement_resolver.py` | 31 | 0.00 | 0.0 | — | COMPONENT | KEEP AS COMPONENT |
| `tests/test_memory_migration_metrics_cutover.py` | 6 | 0.00 | 0.0 | MM | COMPONENT | KEEP AS COMPONENT |
| `tests/test_memory_extraction_relations.py` | 8 | 0.00 | 0.0 | MM | UNCLEAR | UNCLEAR |
| `tests/test_memory_semantic.py` | 9 | 0.00 | 0.0 | — | UNIT | KEEP AS UNIT |
| `tests/test_legacy_paths.py` | 9 | 0.00 | 0.0 | — | UNIT | KEEP AS UNIT |
| `tests/test_memory_episodic.py` | 7 | 0.00 | 0.0 | — | UNIT | KEEP AS UNIT |
| `tests/test_fc_actor_provenance.py` | 7 | 0.00 | 0.0 | — | UNIT | KEEP AS UNIT |

**Leg PROTOCOL HARNESS — `protocol/.agents/harness/tests/` (12 archivos, 185 tests, 7.05 s)**

| Archivo | tests | call_s | ms/test | mec | nivel | candidato |
|---|---:|---:|---:|:--:|---|---|
| `test_lifecycle_install.py` | 15 | 1.59 | 106.0 | GIT | INTEGRATION | POSSIBLE SPLIT |
| `test_lifecycle_update_uninstall.py` | 11 | 1.33 | 120.9 | MM | INTEGRATION | KEEP AS INTEGRATION |
| `test_enforced_flow.py` | 3 | 1.30 | 433.3 | PROC | END_TO_END | KEEP AS END-TO-END |
| `test_operational_invocations.py` | 6 | 0.88 | 146.7 | PROC | MIXED | POSSIBLE SPLIT |
| `test_gate_validator.py` | 55 | 0.59 | 10.7 | FS | COMPONENT | KEEP AS COMPONENT |
| `test_lifecycle_transaction.py` | 13 | 0.58 | 44.6 | FS | INTEGRATION | KEEP AS INTEGRATION |
| `test_lifecycle_limits.py` | 4 | 0.24 | 60.0 | MM | COMPONENT | POSSIBLE SPLIT |
| `test_hook_gate.py` | 25 | 0.18 | 7.2 | FS | COMPONENT | KEEP AS COMPONENT |
| `test_runner_state.py` | 33 | 0.18 | 5.5 | FS | COMPONENT | KEEP AS COMPONENT |
| `test_health_probe.py` | 5 | 0.11 | 22.0 | — | MIXED | KEEP AS COMPONENT |
| `test_lifecycle_contract.py` | 7 | 0.07 | 10.0 | — | COMPONENT | POSSIBLE SPLIT |
| `test_roots.py` | 8 | 0.00 | 0.0 | — | COMPONENT | KEEP AS COMPONENT |

`INFERENCIA` Los dos legs tienen perfiles **cualitativamente distintos**: el leg del harness
es 185 tests en 7.05 s (38 ms/test) y **ninguno de sus archivos supera 1.6 s**; el leg DEV es
1358 tests en 395.26 s (291 ms/test) y 9 de sus archivos superan 10 s. El leg del harness es,
por lejos, el mejor cociente test/segundo del repositorio.

### 2.4 Agregado por área funcional (`HECHO` sobre la clasificación de §3)

| Área funcional | Archivos | Tests | call_s | ms/test |
|---|---:|---:|---:|---:|
| `runtime/orchestrator/` (host, worker, autonomía, F-C, SAE) | 12 | 284 | 327.29 | 1152 |
| Checkers DEV (`tools/check_*.py`) | 12 | 342 | 41.13 | 120 |
| `tools/` (métricas, gates, identidad, placement aux) | 7 | 111 | 12.97 | 117 |
| `runtime/toolcalls/` (materialización, segmentos) | 6 | 225 | 0.44 | 2 |
| Documento / certificación (dogfood + contratos documentales) | 11 | 112 | 15.28 | 136 |
| `runtime/memory/` | 8 | 63 | 0.04 | 1 |
| Contratos de repositorio y de producto | 6 | 141 | 3.51 | 25 |
| Harness del producto (protocol) | 12 | 185 | 7.05 | 38 |
| `runtime/placement/` | 2 | 37 | 0.00 | 0 |
| Infraestructura de test (`pytest_isolation`) + contención | 2 | 23 | 4.15 | 180 |
| **TOTAL** | **69** | **1543** | **402.31** | **261** |

`INFERENCIA` El área `runtime/orchestrator/` tiene **1152 ms por test**, 4.4× la mediana del
repositorio y ~30× el área de checkers. `runtime/memory/` y `runtime/placement/` tienen 1 ms
y 0 ms por test respectivamente.

### 2.5 Fixtures compartidas (`HECHO`)

`HECHO` Hay **26 definiciones de fixture** en 8 archivos (≈13 únicas, contadas dos veces por
el análisis al recorrer cada archivo dos veces). **No existe `conftest.py` en `tests/`**: la
única `conftest.py` de tests es `protocol/.agents/harness/tests/conftest.py`, que aporta
`payload`, `project`, `staging_parent`, `make_engine` y `make_junction`. Fuera de eso, las
fixtures usadas son las de pytest (`tmp_path` en 614 firmas de test, `monkeypatch` en 68,
`capsys` en 65, `pytestconfig`, `tmp_path_factory`) más fixtures locales por archivo
(`payload_root`, `context`, `contract`, `adopted`, `adopted_project`, `session`, `project`).

`HECHO` **1274 de 2820 funciones de test (45.2 %) no piden ninguna fixture**: son aserciones
en proceso sobre datos construidos en el cuerpo del test. Esto es coherente con la
clasificación de §2.2: casi la mitad de las funciones de test no tocan el mundo exterior.

`INFERENCIA` **No hay fixtures globales costosas.** El `setup` total de la corrida completa
es **1.71 s** y el `teardown` **0.01 s**, sobre 402.31 s de `call`. Todo el costo está
*dentro* de cada test. Cualquier política de fixtures de sesión es irrelevante para el reloj;
lo que importa es lo que cada test hace en su cuerpo.

### 2.6 Marcadores, skips y estados especiales (`HECHO`)

- **No hay markers propios declarados** en ningún archivo (no hay `markers =`, no hay
  `pytest.ini`/`pyproject.toml`/`setup.cfg`/`tox.ini`).
- **No hay `xfail`.** Hay **3 `pytest.mark.skipif` a nivel de módulo**:
  `tests/test_check_dist_sync.py:24` (requiere rama `dist`), `tests/test_check_lifecycle_checkpoint.py:35`
  y `tests/test_scoped_content_identity.py:30` (requieren `git`). En la corrida medida
  ninguno se activó: el único skip efectivo es el de `cacheprovider`.
- **25 decoradores `parametrize`** en 11 archivos; los que más expanden son
  `tests/test_check_plan_citations.py` (18 argumentos), `test_adversarial_deliberation.py` (12),
  `test_segment_resolution.py` (10) y `test_check_plan_structure.py` (8). La diferencia entre
  1410 funciones `def test_*` (AST) y 1543 casos recogidos (133 casos, +9.4 %) se explica por
  esos `parametrize`.
- **Sin clases de test**: las clases definidas son helpers (`RecordingInvoker`,
  `WritingInvoker`, `Evicting…`, `NullProviderAdapter`); ninguna empieza con `Test`.

---

## 3. Test → Comportamiento → Componente

### 3.1 Método (`HECHO`)

Para cada uno de los 69 archivos se determinó, leyendo el archivo completo: el
**comportamiento protegido** (la garantía que se pierde si el archivo desaparece), el
**componente primario bajo prueba**, los **componentes secundarios** tocados, el
**mecanismo** que fuerza la integración, y el **nivel real**. El mapeo se verificó de forma
independiente contra: (a) el docstring y las secciones del propio archivo, (b) el grafo de
imports por AST contra los 71 módulos productivos, (c) los conteos de fixtures y de
primitivas de proceso. **La ubicación del archivo no se usó como criterio.**

### 3.2 La pregunta fundamental, respondida por archivo

> ¿El comportamiento que este test pretende garantizar pertenece realmente al componente
> que actualmente termina ejecutándolo?

`HECHO` **En 57 de 69 archivos la respuesta es sí**: el sujeto bajo prueba declarado coincide
con el componente que ejecuta la aserción. En **12 archivos la respuesta es no**, y esos son
los hallazgos de esta sección.

### 3.3 Casos detectados

**(a) Tests cuyo verdadero sujeto está oculto detrás de integración** — `HECHO`

| Archivo | Sujeto declarado | Sujeto real de parte del archivo |
|---|---|---|
| `tests/test_agent_worker.py` | Agent Worker | el **host loop**: 31 tests llaman `make_repo` y `ExecutionHost.run()`; `test_*journal_gaps*` (963-1007) prueban `store.read_journal_with_gaps` / `observation.journal_gaps`; 1058-1071 prueba `worker.repository_snapshot` |
| `tests/test_sae_scope_enforcement.py` | frontera de scope (autonomía) | **`host.py`**: 962-971 y 1037-1045 asertan propiedades del host (sus propios targets de governance están autorizados; la enforcement es del host, no del worker); el archivo alcanza API privada del host (`_pinned_autonomy_projection` 309, `_scope_violations` 1023) |
| `tests/test_autonomous_scope.py` | frontera SAE | **`autonomy.summarize_autonomy`**: tres secciones (344-378, 628-762) protegen los contadores de correcciones/recuperaciones y su render — una responsabilidad distinta que puede fallar con todas las pruebas de frontera en verde |
| `tests/test_determine_execution_state.py` | `tools/determine_execution_state.py` | **`tools/scoped_content_identity.py`**: 23 tests de `--content-identity` construyen repos git reales y usan `sci.compute` como oráculo |
| `tests/test_segment_resolution.py` | `runtime/toolcalls/segment_resolution.py` | **`runtime/toolcalls/canonical.py`**: 2 tests (352-374) asertan `ORDERING_CONTRACT_V2`, `DECLARED_EMPTY_STEPS` y el rechazo de `encode_stable_region` |
| `tests/test_project_segment.py` | `runtime/toolcalls/project_store.py` | **`runtime/toolcalls/budget.py`**: `test_context_budget_not_bypassed` asertа `estimate_tokens`, que pertenece a `test_toolcalls.py` |
| `tests/test_fc_flow.py` | `runtime/orchestrator/fc_flow.py` | **`runtime/memory/`** (5 tests con `MemoryStore` real) y **`worker.classify_executed_effects`** (1 test de lockstep) |
| `tests/test_check_ears_coverage.py` | `tools/check_ears_coverage.py` | **el propio guard como constantes declaradas**: varios tests asertan `MECHANICAL_SUBSET`, `EXCLUDED_SUBSET` y `MECHANICAL_SUBSET == {R1..R5}` — autoconsistencia, no comportamiento |
| `tests/test_audit_gates.py` | `tools/audit_gates.py` sobre el gate validator | **el stub**: `_run_validator` está monkeypatcheado en 9 de 10 tests; el validador real nunca corre |
| `tests/test_fc_actor_provenance.py` | actor provenance | **funciones puras** de `agent_worker` (`classify_actor_evidence`, `actor_evidence_is_real`) — es UNIT legítimo pero el archivo insinúa un flujo |
| `tests/test_check_version_state.py` | `tools/check_version_state.py` | **nada de git**: `cvs.get_tags` se reemplaza por un lambda a nivel de módulo (línea 33), sin `monkeypatch`, y **nunca se restaura** |
| `tests/test_autonomous_orchestrator.py` | el host | **contrato de `WorkerAdapter`**: 3 tests (668-779) parsean el **texto de `host.py`** con `ast` y lo ligan a `inspect.signature(WorkerAdapter.execute)` — es CONTRACT dentro de un archivo de comportamiento |

**(b) Tests que combinan múltiples responsabilidades en un archivo** — `HECHO`

`HECHO` Los 20 archivos MIXED son exactamente esto. Los más relevantes por costo o por
fragilidad de clasificación:

| Archivo | Responsabilidades que contiene | Niveles presentes |
|---|---|---|
| `tests/test_agent_worker.py` | contrato de delegación · vocabulario de invocación · boundary de autoridad · contrato M4 · host loop sobre git real · scope sobre árbol sucio · journal gaps | UNIT + CONTRACT + INTEGRATION |
| `tests/test_autonomous_orchestrator.py` | derivación · boundary de autoridad · exit codes como señal · contrato `WorkerAdapter` por AST · M4 · loop Closed/recovery/no-progress · observation sobre errores | CONTRACT + COMPONENT + INTEGRATION |
| `tests/test_sae_scope_enforcement.py` | frontera pura de proximidad (≈30 tests) · secuencias de host sobre git real (13 tests) · detección post-hoc | COMPONENT + INTEGRATION |
| `tests/test_autonomy_effects.py` | admisión de efectos pura · techo de recursos puro · gate del host sobre git real | COMPONENT + INTEGRATION |
| `tests/test_autonomous_scope.py` | frontera pura (≈60 tests) · contadores/`summarize_autonomy` · 4 tests de integración con host | COMPONENT + INTEGRATION |
| `tests/test_check_lifecycle_anchor.py` | 14 tests sintéticos + 1 certificación del corpus real | COMPONENT + DOC_CERT |
| `tests/test_check_protocol_invariants.py` | 27 tests sintéticos + 1 CLI por subproceso + 1 lectura del árbol real | COMPONENT + E2E + DOC_CERT |
| `tests/test_check_plan_citations.py` | helpers puros de string · resolución sobre árbol falso · 3 CLI por subproceso | UNIT + COMPONENT + E2E |
| `tests/test_autonomy_effects_dogfood.py` | lockstep de vocabulario en proceso · pins de texto fuente · lectura del árbol real | CONTRACT + DOC_CERT |
| `tests/test_operational_invocations.py` (harness) | 4 smoke tests de CLI por subproceso · 2 guards sobre el payload real | E2E + DOC_CERT |
| `tests/test_pytest_isolation.py` | higiene del árbol real · semántica de biblioteca de sesiones/tokens | INTEGRATION + UNIT |
| `tests/test_canonical_materialization.py` | primitivas de identidad · materialización canónica · `cache_coordinator` | UNIT + COMPONENT (dos módulos) |

**(c) Tests que parecen unitarios pero son integration tests** — `HECHO`

- `tests/test_check_lifecycle_checkpoint.py` es la trampa más clara: **COMPONENT** por
  imports (un solo módulo productivo) pero necesita **colaboradores VCS reales**. Sus
  fixtures construyen repositorios con `git init/add/commit/rev-parse`, fabrican **empty
  commits con el mismo tree**, ramas temporales que luego se **borran** (553-568), y la regla
  central del archivo — *mismo tree, distinto SHA* — existe sólo dentro de un repositorio
  real. Un VCS falso testearía el fake. Está correctamente etiquetado `KEEP AS INTEGRATION`.
- `tests/test_determine_execution_state.py` parece un test de herramienta de estado
  (`state.json`, fail-closed) pero **23 de sus 69 tests** construyen repos git reales.
- `tests/test_pytest_isolation.py` se declara a sí mismo "la regresión" de una propiedad de
  infraestructura y efectivamente **hace `os.walk` de todo el repositorio**, crea
  directorios probe bajo el `tmp_root` y el `cache_root` de la sesión, y lanza un `git init`
  y un intérprete Python.
- `tests/test_audit_gates.py` se llama "gates" pero **sustituye el validador**; su garantía
  es la contabilidad de `audit_gates`, no el acuerdo con el validador real.

**(d) Tests de integración que aportan una garantía inalcanzable de otro modo** — `HECHO`

Estos **deben** permanecer integrados, y su costo está justificado:

| Archivo | Garantía que sólo existe con la integración |
|---|---|
| `tests/test_autonomous_orchestrator.py` | `Closed` derivado de un anchor y un checkpoint reales que concuerdan (920-943); continuidad tras reinicio (762-789); guard de no-progreso (1009-1067) |
| `tests/test_sae_scope_enforcement.py` | la negativa ocurre **antes** del efecto: identidad byte a byte del artefacto excluido, ausencia de delegación persistida, `invoker.requests == []` (318-401) |
| `tests/test_autonomy_effects.py` | el techo se lee del **journal real** y sobrevive un reinicio (630-687) |
| `tests/test_check_lifecycle_checkpoint.py` | selección A1/A2 por **correspondencia** de identidad de árbol, no por recencia (206-219) |
| `tests/test_scoped_content_identity.py` | el algoritmo byte a byte contra primitivas git recomputadas independientemente (`ls-files -s`, `hash-object`, `write-tree`) y códigos de salida fail-closed |
| `tests/test_repo_containment.py` | el **estado de tracking git** del repositorio real: una cita cuyo target existe sólo como archivo no versionado |
| `protocol/.agents/harness/tests/test_enforced_flow.py` | la secuencia cross-proceso *deny → registrar PASS → allow* medida en códigos de salida reales |

**(e) Assertions débiles o inertes detectadas** — `HECHO`

No todas son defectos (algunas son deliberadas), pero afectan la lectura de la cobertura:

- `tests/test_sae_scope_enforcement.py:1034`: `assert _digest(root / EXCLUDED) == _digest(root / EXCLUDED)`
  compara un valor consigo mismo y **no puede fallar nunca** (el test hermano 1029-1033 hace
  la comparación antes/después real, así que la garantía sobrevive).
- `tests/test_sae_scope_enforcement.py` (6) en 394-396 compara el checkpoint registrado con
  `plan_before_projection(root)`, que **recomputa** con las mismas funciones privadas de
  producción: autoconsistencia, no expectativa independiente.
- `tests/test_check_ears_coverage_falsification.py:414`:
  `assert set(document['counts']) <= set(document['counts'])` — tautológico; y `:370`
  `assert judgement` sólo documenta la parametrización.
- `tests/test_change_governance.py`: `test_governance_state_excluded_from_identity` asertа
  `identity == identity`; `test_filename` asertа `filename(i) == filename(i)`.
- `tests/test_project_segment.py`: `test_project_namespace_is_logical_not_physical` compara
  una llamada consigo misma.
- `tests/test_legacy_paths.py:72-78`: `test_unique_resolution_for_every_legacy_prefix` arma la
  sonda **desde la propia tabla** `LEGACY_PATHS` y sólo verifica que resuelva a algo distinto;
  los 17 targets podrían apuntar a documentos inexistentes y el archivo seguiría verde.
- `tests/test_check_plan_citations.py:209-216`: la aserción positiva de CLI acepta cualquier
  salida cuya primera línea no contenga `"roken"` ni falle por `"no" in stdout.lower()`, así
  que el mensaje de confirmación está efectivamente sin certificar.
- `tests/test_check_plan_structure.py:137,153,167`: los tests parametrizados por ciclo de
  status sólo asertan que ninguna violación tenga `rule == 'status'`, de modo que un checker
  que dejara de validar statuses por completo seguiría pasando.
- `tests/test_autonomy_effects.py:469-491`: cierra con una disyunción
  (`outcome.stop_condition is None or "scope" in outcome.scope_reason`) que pasa por
  cualquiera de las dos ramas; `test_an_exhausted_ceiling_stops_even_when_no_action_would_be_delegated`
  (689-704) **nunca construye un host ni asertа un stop**, sólo que `Resource ceiling: 0` se
  convierte en un observation gap.
- `tests/test_autonomous_scope.py:589-598`: `test_every_stop_condition_is_reachable` asertа
  igualdad de conjuntos con `STOP_CONDITIONS`, así que **agregar un miembro al vocabulario
  rompe el test sin que nada esté roto**.
- `tests/test_check_lifecycle_lineage.py:675`: el test adversarial de variantes de formato
  sólo asertа `clasificación != VALID` y `returncode in {0,1}`; nunca puede detectar una
  elección equivocada entre GAP y ANOMALY.
- `tests/test_check_version_state.py:33`: `cvs.get_tags = lambda ...` **sin `monkeypatch`**:
  el parche se filtra al resto de la sesión y deja el camino real de tags sin cobertura.
- `tests/test_memory_extraction_relations.py:test_contradiction_and_supersession_are_distinct`
  es casi tautológico (compara dos literales distintos).
- **`REPO_ROOT` declarado y nunca usado** en 7 archivos: `test_aggregate_metrics.py:9`,
  `test_audit_gates.py:8`, `test_check_session_artifacts.py:8`, `test_check_taxonomy_coherence.py:7`,
  `test_check_version_state.py:7`, `test_determine_execution_state.py:14`, `test_legacy_paths.py:7`.
  `HECHO` Ninguno de esos 7 lee el árbol del repositorio: son tests aislados que declaran una
  constante muerta. Importa porque un selector basado en "¿este test lee el repo real?"
  detectaría falsos positivos si se guiara por la constante en vez de por su uso.

**(f) Cobertura de CLI / exit codes faltante** — `HECHO`

`HECHO` De los 20 `tools/*.py`, que se invocan como `python tools/check_*.py` en la batería y
en CI, **8 no tienen ninguna prueba de CLI ni de exit code**:
`check_architecture_traceability.py`, `check_memory_store.py`, `check_taxonomy_coherence.py`,
`check_version_state.py`, `aggregate_metrics.py`, `check_session_artifacts.py`,
`determine_execution_state.py` (su `main()` se llama **en proceso** con `capsys`, nunca por
subproceso) y `audit_gates.py`. `INFERENCIA` esto es una brecha de *garantía*, no de costo:
el argparse, el stdout real y el camino de salida del proceso no están protegidos.

`HECHO` Simétricamente, el harness **sí** cubre sus CLI, pero de forma desigual:
`test_enforced_flow.py` (3 tests, 7 lanzamientos) es el único END_TO_END; `lifecycle.py main()`
y su argparse **nunca se ejecutan** (ni `--purge`, ni `--restore`, ni `--project-root`).

---

## 4. Distribución y Concentración

### 4.1 Concentración cuantificada (`MEDICIÓN`)

| Corte | Archivos | Tests | % tests | call_s | % call_s |
|---|---:|---:|---:|---:|---:|
| top 1 | 1 | 31 | 2.0 % | 97.30 | **24.2 %** |
| top 3 | 3 | 116 | 7.5 % | 231.25 | **57.5 %** |
| top 5 | 5 | 184 | 11.9 % | 312.24 | **77.6 %** |
| top 10 | 10 | 390 | 25.3 % | 367.47 | **91.3 %** |
| top 20 | 20 | 557 | 36.1 % | 391.73 | **97.4 %** |
| resto (49) | 49 | 986 | 63.9 % | 10.58 | 2.6 % |

`MEDICIÓN` `tests/test_autonomous_orchestrator.py` (31 tests, **2.0 %** de la suite) consume
**24.2 %** del tiempo. Los **4 archivos dominantes** (152 tests, 9.9 %) consumen
**70.2 %** (282.18 s).

### 4.2 Distribución de la duración por test (`MEDICIÓN` sobre 1486 nodos)

| Estadístico (fase `call`) | Valor |
|---|---:|
| n | 1486 de 1543 |
| total | 402.31 s |
| media | 0.271 s |
| **mediana** | **0.000 s** |
| p90 | 0.500 s |
| **p95** | **1.120 s** |
| p99 | 6.180 s |
| máx | 19.95 s |

`INFERENCIA` **El 95 % de la suite no influye en el reloj.** Con mediana 0, el costo es
enteramente una cola: 20 tests superan 4.7 s y suman ~136 s; el top 40 suman ~220 s.

### 4.3 Concentración por módulo productivo (`HECHO`, primary component)

| Componente primario | Archivos | Tests | call_s |
|---|---:|---:|---:|
| `runtime/orchestrator/autonomy.py` | 5 | 167 | 133.78 |
| `runtime/orchestrator/host.py` | 3 | 49 | 109.21 |
| `runtime/orchestrator/agent_worker.py` | 2 | 48 | 73.53 |
| `protocol/.agents/harness/lifecycle.py` | 4 | 43 | 3.74 |
| `runtime/toolcalls/canonical.py` | 3 | 111 | 0.23 |
| `tools/check_ears_coverage.py` | 3 | 91 | 3.20 |
| `tools/check_discovery_output.py` | 2 | 62 | 2.28 |
| `runtime/placement/resolver.py` | 2 | 37 | 0.00 |
| `protocol/.agents/harness/gate_validator.py` | 1 | 55 | 0.59 |
| `proc…/runner_state.py` | 1 | 33 | 0.18 |

`INFERENCIA` La concentración **en cantidad** es sana: 47 de 71 módulos productivos tienen
1–3 archivos de test directos, sin solapamiento anómalo. La concentración **en tiempo** es
extrema y se explica por un solo factor: **tres módulos** (`autonomy.py`, `host.py`,
`agent_worker.py`) están cableados en los 4 archivos dominantes, y esos 4 archivos pagan la
construcción de un mundo por test. **`HECHO` Los tres módulos tienen 8, 7 y 6 archivos de
test que los tocan, y todos los tests que los tocan caros son los mismos 4–5.**

### 4.4 Diagnóstico de la causa (opciones A–F del pedido)

| Opción | Evidencia | Veredicto |
|---|---|---|
| **A. Justificada por la complejidad del componente** | `host.py` 1185 líneas, `autonomy.py` 1769, `agent_worker.py` 706, `observation.py` 1052. Los tests cubren transiciones, no líneas. | **Parcialmente SÍ** — el volumen de casos se justifica; el tiempo por caso, no. |
| **B. Consecuencia de pruebas indirectas** | 12 archivos prueban otro componente como sujeto real (§3.3a). | **SÍ, en grado menor** — explica desenfoque, no costo masivo. |
| **C. Consecuencia de integración excesiva** | 254 sitios de llamada a constructores de repositorio; 4 archivos dominantes construyen 1 repo por test. | **SÍ, es la causa dominante del reloj.** |
| **D. Consecuencia de duplicación** | No hay duplicación literal. 3 conjuntos de solapamiento de *intención* (§5). | **NO** — el solapamiento encontrado es deliberado y no explica el costo. |
| **E. Arquitectura de tests que mezcla niveles** | 20 archivos MIXED, 585 tests, 337.44 s (83.9 % del tiempo). | **SÍ, es la causa dominante de la *imposibilidad de seleccionar***, no del tiempo. |
| **F. Combinación** | C + E son ortogonales y ambos presentes. | **F: C para el costo, E para la granularidad.** |

`INFERENCIA` La distinción importa: **C se arregla optimizando** (reutilizar el montaje) y
**E se arregla redistribuyendo** (separar la mitad pura). Ninguna de las dos se arregla con
selección targeted, porque la selección no cambia cuánto cuesta el archivo que hay que correr.

---

## 5. Redundancia y Solapamiento

### 5.1 Resultado principal (`HECHO` + `INFERENCIA`)

`HECHO` **No existe duplicación literal.** `tests/testsupport.py` documenta que la única
duplicación byte a byte conocida (`assert_tool_imports_only_stdlib` repetida en siete suites)
ya fue extraída en el plan 124/144.

`HECHO` Se identificaron **6 grupos de solapamiento de intención**. Ninguno justifica
eliminar un test; todos son clasificables y la mayoría son **complementarios por diseño**.

### 5.2 Grupos

**Grupo 1 — `tools/check_ears_coverage.py` (3 archivos, 91 tests, 3.20 s)** — `HECHO`

| Archivo | Qué protege | Clase |
|---|---|---|
| `test_check_ears_coverage.py` (38) | contrato del guard sobre payload sintético: R1–R5, señales, exit 0/1/2, GAP nunca VALID, forma del JSON, determinismo, read-only, sin `__pycache__`, stdlib-only, set mecánico derivado del estándar | base |
| `test_check_ears_coverage_falsification.py` (25) | la misma tabla negativa (sin bullets, sección ausente, TOML-only, bullet sin match, estándar/contrato ausente, `ears` ausente, patrón ensanchado/eliminado/sexto, forma canónica contradicha) + citas y la prueba estructural de que el subconjunto excluido no es expresable | **REDUNDANT** en ~10 casos; **única** en citas (133-184) y en la prueba estructural (373-417) |
| `test_check_ears_coverage_dogfood.py` (18) | las tres fuentes de verdad del payload **real** en paridad + read-only sobre él | **COMPLEMENTARY / CERTIFICATION** |

`INFERENCIA` El solapamiento 1↔2 es real y deliberado. **Garantía adicional que aporta la
falsificación:** la demostración de que ninguna de las cinco reglas puede expresar el
subconjunto de juicio (compuestidad, negación, should/must/will/may, especificidad,
supuestos) — eso **no** está en el archivo base. **Riesgo si se eliminara:** se pierde la
prueba de no-vacuidad del límite, que es el argumento central del plan 137.
**Riesgo si se fusionaran:** se pierde la legibilidad de la tabla de falsificación, y el
archivo base ya hace de biblioteca de fixtures para el otro (`import test_check_ears_coverage as base`).
**Depende de integración real: no** (ambos son in-process sobre payload sintético).

**Grupo 2 — `tools/check_lifecycle_{anchor,checkpoint,lineage}.py` (3 archivos, 90 tests)** — `HECHO`

C-1, C-2 y C-3 sobre el mismo corpus: los tres comparten la gramática `## Validation anchor`
/ `## Checkpoint / cierre`, los tres mantienen **su propia** lista de clasificaciones
esperadas sobre planes reales (94/95 `EXCLUDED`, 96/97 `VALID`, 98 `N/A`, 146 y 100
tolerantes), y los tres tienen un test anclado. Clase: **COMPLEMENTARY** en las reglas,
**CERTIFICATION** en las dogfood. **Sin solapamiento de aserciones**: los códigos y reglas
son disjuntos (C-1 población/identidad, C-2 cierre/GC-1, C-3 linaje/findings).
`INFERENCIA` El riesgo real **no** es redundancia sino **acoplamiento de mantenimiento**: las
tres listas esperadas deben actualizarse juntas cuando cambia el corpus, y ese acoplamiento
no está expresado en ningún lugar.

**Grupo 3 — `runtime/orchestrator/` (5 archivos dominantes + 4 dogfood)** — `HECHO`

`test_agent_worker.py` y `test_autonomous_orchestrator.py` protegen el **mismo host loop**
por dos ejes (AgentWorker vs CommandWorker), el **mismo contrato M4** de `WorkerResult` y
las **mismas** lecturas de journal. `test_sae_scope_enforcement.py` y `test_autonomy_effects.py`
son las dos fronteras del **mismo** `autonomy.py` por ejes distintos (write-targets vs
effects/resource). Clase: **COMPLEMENTARY** en los ejes, **REGRESSION-SPECIFIC** en los
bloques que nombran el estado pre-fix, **INTEGRATION SAFETY NET** entre dogfood y sintético.
`INFERENCIA` **Esto no es redundancia: es cobertura por ejes ortogonales.** Eliminar cualquiera
de los cuatro dejaría un eje sin cubrir. El costo no viene del solapamiento sino de que **los
cuatro pagan independientemente el montaje**.

**Grupo 4 — `runtime/placement/` (2 archivos, 37 tests)** — `HECHO`
`test_placement_resolver.py` (31, sin filesystem) y `test_placement_dogfood.py` (6, contra el
árbol real). Solapamiento en la tabla kind→namespace y en el namespace del run-log:
**REDUNDANT** en esas filas concretas, **COMPLEMENTARY** en el resto (el dogfood verifica que
los namespaces reportados **existen** en el árbol y que el resolver cita
`docs/placement-contract.md`). **Garantía del dogfood que el resolver no da:** que la regla
publicada corresponde a directorios reales.

**Grupo 5 — `check_session_artifacts` / `aggregate_metrics` / `measure_context_budget` (3 archivos)** — `HECHO`
La aritmética del `context_budget` se asertа **tres veces** en tres implementaciones
independientes (`test_check_session_artifacts.py:92-104`, `test_measure_context_budget.py:39-50`,
`test_aggregate_metrics.py:127-140`). La regla de evidencia-o-attestation se implementa y
asertа en `test_check_session_artifacts.py` (242-251, 491-503) y de nuevo en
`test_audit_gates.py`. Clase: **REDUNDANT a nivel de regla**, con cada archivo siendo la
**única** cobertura de su propio módulo. `INFERENCIA` Es duplicación de *regla*, no de
*código*; eliminarla dejaría un módulo sin cobertura o un módulo sin cobertura de esa regla.
**No hay nada que eliminar.**

**Grupo 6 — `test_health_probe.py` ↔ `test_operational_invocations.py` (harness)** — `HECHO`
Ambos lanzan el CLI de `health_check.py` por subproceso y asertan PASS + exit 0. Clase:
**REDUNDANT**. Es el único caso del repositorio donde un mismo contrato de proceso se prueba
dos veces en dos archivos distintos del mismo leg. `INFERENCIA` Riesgo de eliminarlo: nulo
(el otro test cubre exactamente lo mismo); riesgo de mantenerlo: un lanzamiento de
intérprete de más. **Costo del grupo completo: 0.99 s — irrelevante para el reloj.**

**Solapamiento por diseño no problemático** — `HECHO` `tests/AGENTS.md:73-91` declara
explícitamente **18 tests anclados** al estado canónico, con su contrato de estabilidad. Esa
duplicación de *sujeto* (varios archivos leen el mismo payload o el mismo corpus) es
**CERTIFICATION**, no redundancia, y el repo ya la tiene documentada.

### 5.3 Veredicto

`INFERENCIA` **No hay redundancia que eliminar.** El repositorio tiene 6 grupos de
solapamiento, de los cuales 1 es REDUNDANT puro (harness, 0.99 s) y 5 son
COMPLEMENTARY/CERTIFICATION con garantías adicionales identificables. La afirmación
"hay tests redundantes" **no está sostenida por la evidencia** en este repositorio, y este
informe no la hace.

---

## 6. Costo de Ejecución

### 6.1 Correlación entre mecanismo y tiempo (`MEDICIÓN` + `HECHO`)

| Mecanismo de integración dominante | Archivos | Tests | call_s | % del tiempo | ms/test |
|---|---:|---:|---:|---:|---:|
| **REAL_GIT_REPO** | 9 | 272 | **344.16** | **85.6 %** | 1265 |
| SUBPROCESS_CLI | 6 | 102 | 20.57 | 5.1 % | 202 |
| FILE_SYSTEM_CONTRACT | 22 | 688 | 19.84 | 4.9 % | 29 |
| REAL_REPO_TREE | 11 | 126 | 12.55 | 3.1 % | 100 |
| MULTI_MODULE_IN_PROCESS | 10 | 179 | 5.01 | 1.2 % | 28 |
| NONE | 10 | 168 | 0.18 | 0.04 % | 1 |

`INFERENCIA` **La correlación es prácticamente determinista: 9 archivos (13 %) que usan
repositorios git reales consumen 85.6 % del tiempo.** No es la cantidad de módulos
productivos (10 archivos con varios módulos cableados cuestan 5.01 s en total), no es el
filesystem (22 archivos, 19.84 s), no es la cantidad de tests (688 tests de filesystem por
19.84 s). **Es `git`.**

### 6.2 El primitivo, medido (`MEDICIÓN`)

```text
git init -q && git add -A && git commit --allow-empty -m init
  n=8   media 0.340 s   min 0.309 s   max 0.390 s
python -c pass
  n=5   media 0.050 s por arranque
```

`HECHO` Repeticiones de ese primitivo por archivo (sitios de llamada a constructores de
repositorio, contados por AST):

| Archivo | sitios de construcción de repo | sitios `subprocess.*` | tokens `git` | `sys.executable` | coste medido |
|---|---:|---:|---:|---:|---:|
| `tests/test_agent_worker.py` | 32 | 1 | 1 | 0 | 73.53 s |
| `tests/test_check_lifecycle_checkpoint.py` | 31 | 3 | 3 | 1 | 30.06 s |
| `tests/test_check_plan_citations.py` | 29 | 1 | 0 | 1 | 0.48 s |
| `tests/test_check_protocol_invariants.py` | 28 | 2 | 0 | 2 | 0.66 s |
| `tests/test_autonomous_orchestrator.py` | 23 | 4 | 4 | 0 | 97.30 s |
| `tests/test_check_lifecycle_anchor.py` | 22 | 1 | 0 | 1 | 1.39 s |
| `tests/test_scoped_content_identity.py` | 17 | 2 | 2 | 1 | 12.65 s |
| `tests/test_autonomy_effects.py` | 16 | 2 | 2 | 0 | 50.93 s |
| `tests/test_sae_scope_enforcement.py` | 14 | 1 | 1 | 0 | 60.42 s |
| `tests/test_autonomous_scope.py` | 5 | 3 | 3 | 0 | 14.68 s |
| `tests/test_check_dist_sync.py` | 4 | 2 | 2 | 1 | 4.23 s |
| `tests/test_determine_execution_state.py` | 3 | 2 | 2 | 0 | 11.29 s |

`INFERENCIA` **La cantidad de sitios de construcción de repositorio no predice el costo por
sí sola** — `test_check_plan_citations.py` tiene 29 y cuesta 0.48 s, mientras
`test_agent_worker.py` tiene 32 y cuesta 73.53 s. La diferencia es que **"constructor de
repo" en los checkers es escribir un árbol de markdown en `tmp_path`**, no ejecutar `git`.
`HECHO` Los archivos que realmente ejecutan `git` son los que declaran `_GIT_ENV`, `git(...)`,
`_git(...)`, `init_repo`, `empty_commit`, `run_tool` con `git`: `test_check_lifecycle_checkpoint.py`
(31 repos reales), `test_scoped_content_identity.py` (17), `test_determine_execution_state.py`
(3 + `ls-files`/`write-tree` por test), los 4 dominantes (23+32+16+14) y
`test_check_dist_sync.py` (4 repos con ~6 invocaciones cada uno).

### 6.3 Descomposición del costo por grupo

`MEDICIÓN` Descomposición del tiempo de los grupos caros y su causa dominante:

| Grupo | call_s | Descomposición inferida | Causa principal |
|---|---:|---|---|
| 4 archivos dominantes de `orchestrator` | 282.18 | ~85 repos git construidos (≈29 s de `git init/add/commit` puro) + el resto en **ejecuciones del host**: cada `host.run()` itera y por iteración lanza los `check_lifecycle_*` (3 scripts) y `python src/check_ok.py` como subprocesos, y `test_revalidation_is_recorded_as_a2` corre 4 + 12 iteraciones | **repetición de una misma preparación** (el repositorio) + **subprocess dentro del bucle** |
| `test_check_lifecycle_checkpoint.py` | 30.06 | 31 repos + `rev-parse`/`write-tree`/empty commits/branch delete; el test anclado (`test_real_repo_expected_classifications`) solo cuesta 4.14 s | repos git + `sys.executable` |
| `test_scoped_content_identity.py` | 12.65 | ~19 instalaciones de git + ~20 lanzamientos del intérprete + un submodule copiado con `copytree` | subprocess + repos + copia |
| `test_sae_scope_enforcement_dogfood.py` | 11.90 | 2 repos sintéticos + ~4 `host.run()` + 2 escaneos de `git log` sobre el repositorio **real** + 9 lecturas reales | repos + árbol real |
| `test_determine_execution_state.py` | 11.29 | 23 tests de content-identity, cada uno 1 repo + `ls-files -s` por archivo scopado + `write-tree` | repos git |
| `test_check_lifecycle_lineage.py` | 4.71 | **~40 lanzamientos de `sys.executable`** (`run_tool` en ~30 tests) para aserciones de exit code que ya están implícitas en la llamada en proceso | **`sys.executable` por test** |

`HECHO` `MEDICIÓN` de corroboración: 402.31 s de `call` con `setup` 1.71 s y `teardown`
0.01 s. Una corrida completa previa de esta auditoría midió ~45 s de CPU sobre ~400 s de
reloj. **El régimen es I/O y creación de procesos, no cómputo.**

### 6.4 Lo que NO es el problema (`HECHO`)

- **No son las fixtures compartidas**: 1.71 s de `setup` sobre 402.31 s (0.4 %).
- **No son los `parametrize`**: expanden 1410 funciones a 1543 casos (+9.4 %) y los archivos
  más parametrizados (`test_check_plan_citations.py`, `test_adversarial_deliberation.py`,
  `test_check_plan_structure.py`) están entre los más baratos.
- **No es la cantidad de módulos importados**: 10 archivos con varios módulos cableados
  cuestan 5.01 s en total.
- **No es el volumen de aserciones**: `test_check_session_artifacts.py` tiene 60 tests y
  cuesta 0.79 s; `test_autonomous_orchestrator.py` tiene 31 y cuesta 97.30 s.
- **No es el filesystem**: 688 tests de contrato de filesystem cuestan 19.84 s.

---

## 7. Aislamiento

### 7.1 Regla aplicada

> No convertir automáticamente tests de integración en unitarios. Determinar primero qué
> garantía aporta la integración.

`HECHO` Se aplicó en este orden: identificar el nivel real → identificar qué garantía
depende del mecanismo de integración → sólo entonces evaluar si la mitad pura puede
separarse **conservando su garantía**.

### 7.2 Clasificación completa

| Candidato | Archivos | Tests | call_s |
|---|---:|---:|---:|
| KEEP AS UNIT | 5 | 41 | 0.03 |
| KEEP AS COMPONENT | 23 | 609 | 10.64 |
| KEEP AS CONTRACT | 8 | 49 | 8.87 |
| KEEP AS INTEGRATION | 5 | 80 | 48.85 |
| KEEP AS END-TO-END | 1 | 3 | 1.30 |
| POSSIBLE SPLIT | 24 | 725 | 332.60 |
| POSSIBLE ISOLATION | 2 | 28 | 0.02 |
| UNCLEAR | 1 | 8 | 0.00 |

`INFERENCIA` El rótulo `POSSIBLE SPLIT` es **generoso a propósito**: significa "el archivo
contiene más de un nivel", no "el archivo debería partirse". De los 24, sólo **6** tienen una
mitad pura separable con ganancia medible.

### 7.3 `POSSIBLE ISOLATION` — detalle

**`tests/test_audit_gates.py` (10 tests, 0.00 s)** — `HECHO`
- **Qué podría aislarse:** los 9 tests de `audit_gates.audit()` ya están aislados: el
  validador está monkeypatcheado.
- **Qué dependencia provoca la integración:** `_run_validator` es un **stub** en 9 de 10 tests.
- **Garantía que se conserva:** la contabilidad de gates (violación, override, skip,
  attestation) sobre árboles `tmp_path`.
- **Garantía que se pierde:** **ninguna hoy, porque ya se perdió**: el acuerdo con el
  validador real, la construcción de `argv` y el contrato de retorno real **no están cubiertos**.
- **¿Debe mantenerse además un test de integración?** **Sí, y hoy falta**: un test que drive
  el validador real por subproceso sobre un `.project` real. Esto es una **brecha**, no un
  candidato de aislamiento.
- **Clase real:** ya está en el nivel correcto; el hallazgo es cobertura faltante.

**`tests/test_prompt_cache_dogfood.py` (18 tests, 0.02 s)** — `HECHO`
- **Qué podría aislarse:** las propiedades de cache/identidad (prefijo estable, ordering,
  sufijo dinámico, aislamiento por proyecto/sesión, no-fuga del provider).
- **Dependencia:** lee el payload **real** (`protocol_root=protocol/`) ~24 veces.
- **Se conserva:** las invariantes de identidad y de cache, ya cubiertas en
  `test_canonical_materialization.py` y `..._v2.py` con fixtures.
- **Se pierde:** la certificación RFC-78/plan 121 **sobre el payload real**, incluida la
  resolución real de workflow, policy y rol Worker.
- **¿Mantener un test de integración?** **Sí**: al menos un test sobre el payload real.
- **Clase real:** KEEP AS COMPONENT sobre fixtures **+** una certificación mínima. **Costo
  actual: 0.02 s — no hay urgencia alguna.**

### 7.4 `POSSIBLE SPLIT` con ganancia real — los 6 archivos

| Archivo | call_s | Mitad pura separable | Mitad que debe quedar integrada | Garantía perdida si se aislara la mitad integrada |
|---|---:|---|---|---|
| `tests/test_agent_worker.py` | 73.53 | contrato de delegación, `parse_agent_task`, vocabulario `NullAgentInvoker`/`AgentInvocationResult`, `AuthorityBoundary.evaluate`, lista M4 + `validate_worker_result`/`from_dict` (303-394, 493-506, 923-955) | `artifacts_modified` sobre un árbol ya sucio (1015-1055) y la violación de scope detectada por el host (548-565) — son afirmaciones sobre `git status`/snapshot de contenido | la atribución de cambios a un repositorio real: sin repo, el sujeto pasa a ser el fake |
| `tests/test_autonomous_orchestrator.py` | 97.30 | los 3 tests `test_worker_adapter_*` (668-779) y `test_incomplete_worker_result_is_rejected_by_the_contract` (826) + la trilogía de observation con `tmp_path`/`monkeypatch` (1109-1151) | `Closed` derivado de anchor+checkpoint reales (920-943), continuidad tras reinicio (762-789), guard de no-progreso (1009-1067) | que la condición derivada provenga del estado real y no de un stub |
| `tests/test_sae_scope_enforcement.py` | 60.42 | ~30 tests de frontera pura (secciones 2, 3, 5-pura, 6, 7, 10: 504-542, 596-620, 669-738, 885-904, 912-954, 1053-1081) | la negativa **antes** del efecto (318-401) y la detección post-hoc (992-1045) | la afirmación de que nada se escribió y que el invoker nunca fue alcanzado |
| `tests/test_autonomy_effects.py` | 50.93 | sección 1 sin los 2 `build_repo` (365-366), sección 2 (376-537), sección 5 (758-768), los 2 casos de recurso de `evaluate_autonomy` (725-750) | el gate antes de la delegación (545-599) y el techo acumulado en el journal real (630-650) | que el techo venga de la evidencia y no de memoria del host |
| `tests/test_autonomous_scope.py` | 14.68 | todo salvo los 4 tests de host (86-773: ~60 tests puros de frontera + los contadores de `summarize_autonomy`) | los 4 tests de host (899-954) | que el gate sea aditivo, conduzca trabajo autorizado y detenga cuando falta la declaración |
| `tests/test_determine_execution_state.py` | 11.29 | ~46 tests de determinación/summary/undetermined sin git (84-317, 386-575) | los 23 tests de `--content-identity` (341-1161) | el acuerdo real entre el scope del record y el blob de git (`ls-files -s`, `write-tree`) |

`INFERENCIA` **Ganancia esperada por los 6 splits:** los archivos se vuelven seleccionables
con precisión (un cambio en `tools/scoped_content_identity.py` ya no obliga a correr los 69
tests de `determine_execution_state`), y la mitad pura se vuelve trivialmente rápida. **No
reduce el tiempo total de la suite completa** — mueve tests, no los elimina.

### 7.5 `POSSIBLE SPLIT` con ganancia marginal — los 18 restantes

`HECHO` Los otros 18 archivos etiquetados `POSSIBLE SPLIT` tienen una mitad pura, pero
**cuestan ≤ 3.04 s cada uno** y su partición es una decisión de layout, no de nivel:
separar el test anclado del resto (`test_check_lifecycle_anchor.py`, `test_root_contract.py`,
`test_check_ears_coverage_dogfood.py`, `test_discovery_output_dogfood.py`,
`test_operational_invocations.py`), separar la frontera de proceso
(`test_check_plan_citations.py`, `test_measure_context_budget.py`, `test_check_lifecycle_lineage.py`,
`test_check_protocol_invariants.py`), o separar responsabilidades dentro de un mismo nivel
(`test_aggregate_metrics.py`, `test_canonical_materialization.py`, `test_project_segment.py`,
`test_adversarial_deliberation.py`, `test_fc_flow.py`, `test_pytest_isolation.py`,
`test_lifecycle_install.py`, `test_lifecycle_limits.py`, `test_lifecycle_contract.py`).

`INFERENCIA` Dos de estos sí tienen valor **de garantía**, no de costo:
- `tests/test_check_lifecycle_lineage.py`: ~40 lanzamientos de `sys.executable` para exit
  codes que `verify_all` ya implica. Reemplazarlos por `main()` + `capsys` (como hace la
  suite EARS) conserva la garantía y elimina ~30 arranques de intérprete.
- `tests/test_check_plan_citations.py`: idem con 3 lanzamientos, pero **uno debe quedar**:
  `test_runs_from_other_cwd` prueba la independencia del cwd, que sólo existe en un proceso
  nuevo.

### 7.6 `UNCLEAR` — 1 archivo

`tests/test_memory_extraction_relations.py` (8 tests, 0.00 s): el análisis devolvió el nivel
en el campo de mecanismo y viceversa, señal de que el archivo **no cae limpio en una
categoría**: cubre `extraction.py` (4 tests) y `relations.py` (4 tests) con el mismo peso,
sin fixture compartido. `INFERENCIA` Es un archivo de dos módulos, ambos puros; el nivel es
UNIT/COMPONENT en ambos mitades y la ambigüedad es del etiquetado, no del contenido.
**No requiere acción.**

---

## 8. Relación con la Selección Targeted

> "Modifiqué X. ¿Qué tests debo ejecutar?"

### 8.1 Qué información se necesita, y qué existe hoy

| Información necesaria | ¿Existe hoy? | Evidencia |
|---|---|---|
| archivo productivo → tests (dependencia directa) | **Sí**, por import real | `HECHO` 65 de 69 archivos importan ≥1 módulo productivo; el bootstrap de `sys.path` es único y declarado (`conftest.py:73-75`) |
| dependencia indirecta (módulo → módulo → tests) | **Sí**, derivable del grafo de imports, con re-exports de paquete resueltos | `HECHO` `runtime/orchestrator/` es un grafo denso: `host.py` importa 8 módulos, `__main__.py` 8, `__init__.py` 5 |
| tests que invocan producción **sin importarla** (por subprocess) | **Parcialmente**: detectable por análisis textual de `tools/*.py`, no por imports | `HECHO` 21 archivos usan subproceso; 8 invocan un `tools/*.py` por texto (`test_check_dist_sync.py`, `test_check_lifecycle_*`, `test_determine_execution_state.py`, `test_scoped_content_identity.py`, `test_measure_context_budget.py`, `test_check_protocol_invariants.py`, `test_operational_invocations.py`) |
| tests que leen el **árbol real** del repositorio | **No** por imports: requiere categoría explícita | `HECHO` 20 archivos (398 tests, 356.71 s) tienen el árbol real o un repo git real como dependencia dominante; 11 leen el árbol real |
| tests de contrato / interfaz entre artefactos | **No** por imports (leen texto por `inspect.getsource`/`read_text`) | `HECHO` `test_fc_host_integration.py` (5 tests, detecta wiring por texto), `test_autonomy_effects_dogfood.py` (pins de texto fuente), `test_fc_isolation_declaration.py` / `test_fc_recovery_alignment.py` (leen documentos) |
| tests de certificación documental | **Sí, declarados** | `HECHO` `tests/AGENTS.md:73-91` declara **18** tests anclados con su contrato de estabilidad |
| tests que dependen de **infraestructura de test compartida** | **Sí, pero de alcance total** | `HECHO` `conftest.py` + `tests/pytest_isolation.py` afectan a **toda** la suite; `test_pytest_isolation.py` es su regresión; el plan 145 ya causó fallos por esto |
| tests cuyo vínculo **no puede** inferirse | **Sí, y están enumerados** | 4 archivos sin import de producción: `test_adversarial_deliberation.py` (75), `test_fc_isolation_declaration.py` (4), `test_fc_recovery_alignment.py` (4), `test_fc_host_integration.py` (5) |

### 8.2 Qué se puede seleccionar por cada método

**PATH-BASED** (recomendado como base) — `INFERENCIA` fundada
- Funciona con precisión para **47 de 71 módulos** con mapa 1:1 módulo→archivo.
- `HECHO` Es lo que los planes ya hacen en la práctica (137, 144, 145 citan command-sets por archivo).
- Requiere enumerar a mano cuando el cambio cae en un util compartido
  (`runtime/orchestrator/host.py` → 8 archivos; `protocol/.agents/harness/roots.py` → 13).

**DEPENDENCY-BASED** (útil como cálculo del path-set, no como política)
- `HECHO` Viabilidad técnica alta y ya demostrada: el grafo de imports es completo.
- `INFERENCIA` Su valor real es **no olvidar los indirectos** y no enumerar a mano.
- **No captura**: subprocess, lecturas del árbol real, contratos por texto.

**EXPLICIT CONTRACT MAP** (necesario para el residuo)
- `INFERENCIA` Es la única vía para los 4 archivos sin import, los 11 con lectura del árbol
  real y los pins de texto. Existe parcialmente: `tests/AGENTS.md:73-91` **ya es** un mapa de
  contrato para los 18 anclados.

### 8.3 Lo que **siempre** exige una categoría global

`HECHO` Estas categorías no son seleccionables por path ni por dependencias y deben
ejecutarse en bloque:

1. **Infraestructura de test compartida** — cambio en `conftest.py`, `tests/pytest_isolation.py`
   o el bootstrap de `sys.path` → **toda** la suite. `HECHO` plan 145 modificó exactamente
   esos dos archivos.
2. **Estado canónico documental** — cambio en cualquier plan, RFC, ADR, INDEX, doc del
   payload, `VERSION` o `CHANGELOG` → los **18 archivos anclados** más los dogfood del
   harness. `HECHO` 20 archivos, 398 tests, 356.71 s dependen de esto (aunque la mayor parte
   de ese tiempo es de los 4 archivos dominantes, cuyo repositorio es **throw-away**: su
   dependencia del repo real es de *código*, no de *estado*).
3. **Vocabulario compartido entre capas** — cambio en el conjunto de efectos, stop
   conditions, `EFFECT_KINDS`/`AUTHORIZED_BY`/`STATUSES`, `LEGACY_PATHS`, `PROTOCOL_VERSION`
   → archivos en tres áreas distintas a la vez (`test_autonomy_effects_dogfood.py`,
   `test_check_session_artifacts.py`, `test_legacy_paths.py`, `test_check_version_state.py`).
4. **La batería canónica misma** — su definición vive en `docs/VERSIONING.md` §4.1 y es la
   identidad certificada por el Validation Anchor. `HECHO` cualquier command-set distinto por
   contexto cambia lo que el anchor certifica.

### 8.4 Readiness

```text
PATH-BASED                    listo para usar hoy, sin tooling nuevo    →  47/69 archivos
PATH + DEPENDENCY (calculado)  técnico, exige decidir el cierre transitivo →  +14 archivos
EXPLICIT CONTRACT MAP         parcialmente existe (tests/AGENTS.md)      →  +8 archivos
GLOBAL CATEGORY (siempre)     no derivable                               →  4 conjuntos
```

`INFERENCIA` `TARGETED_SELECTION_READINESS = ALTA` para el 88 % de los archivos, con **dos
excepciones declaradas y no eliminables**: los 18 anclados y la infraestructura de test
compartida. **Lo que falta no es información: es una decisión de gobernanza** (§11, §13).

---

## 9. Modelo de Capas Propuesto

### 9.1 Confirmación, modificación o descarte del modelo de 4 capas

`INFERENCIA` Las cuatro capas del pedido (L0 UNIT / L1 COMPONENT-CONTRACT / L2 INTEGRATION /
L3 END-TO-END-CERTIFICATION) **son correctas en su eje vertical** — la evidencia las separa
limpiamente (§7.2) — pero **insuficientes por sí solas**, porque la evidencia muestra un
segundo eje que corta a las cuatro: **si el test depende de estado del mundo o sólo de su
propio fixture**. Sin ese eje, tres archivos de niveles distintos (un UNIT de documento, un
COMPONENT y un CONTRACT) quedan en el mismo saco operativo aunque tengan requisitos de
ejecución y contratos de estabilidad completamente distintos.

`RECOMENDACIÓN` Modelo de **4 niveles × 2 regímenes**.

### 9.2 Las capas

**L0 — UNIT**
- **Propósito:** una función o dataclass en aislamiento; vocabularios cerrados, invariantes
  algebraicas, serialización.
- **Costo esperado:** ~0.001 s/test. `MEDICIÓN` hoy: 41 tests, 0.03 s, 5 archivos.
- **Frecuencia:** en cada iteración, siempre.
- **Cambios que la disparan:** el módulo productivo de esa función.
- **Qué no debe duplicar:** nada de L1; no debe re-asertar contratos de esquema publicados.
- **Qué debe permanecer exclusivamente aquí:** el cierre de vocabularios (`CLAIM_TYPES`,
  `EVIDENCE_CLASSES`, `RELATION_TYPES`, `LIFECYCLE_STATES`) y la pureza de las funciones de
  identidad (hash, `SegmentIdentity`).

**L1 — COMPONENT / CONTRACT**
- **Propósito:** un módulo por su API pública con colaboradores reales (filesystem,
  `tmp_path`), y los contratos entre artefactos (esquemas, políticas publicadas, wiring).
- **Costo esperado:** ≤ 50 ms/test. `MEDICIÓN` hoy: 609 tests COMPONENT en 10.64 s
  (17 ms/test) + 95 tests CONTRACT en 0.01 s. **Ya está en presupuesto.**
- **Frecuencia:** en cada iteración del área; obligatorio en CI.
- **Cambios que la disparan:** el módulo del tema, su contrato publicado, o el documento
  normativo que el contrato cita (`docs/placement-contract.md`).
- **Qué no debe duplicar:** la existencia de los archivos que el contrato nombra (eso es L3).
- **Qué debe permanecer exclusivamente aquí:** la regla de negocio con sus códigos
  (`AEW-002`, `R1–R5`, `C-1/C-2/C-3`, exit codes), y la detección de wiring entre módulos.

**L2 — INTEGRATION**
- **Propósito:** varios módulos productivos reales cableados, con efectos reales; la
  secuencia de estados del sistema, no la línea de código.
- **Costo esperado:** 0.1–1 s/test. `MEDICIÓN` hoy: 78 tests en 16.17 s (207 ms/test) para
  los que no usan git, pero **272 tests en 344.16 s (1265 ms/test)** para los que construyen
  repositorios.
- **Frecuencia:** antes de integrar; no en cada iteración de edición.
- **Cambios que la disparan:** `host.py`, `worker.py`, `autonomy.py`, `agent_worker.py`,
  `derivation.py`, `observation.py`, `store.py`, `lifecycle.py`.
- **Qué no debe duplicar:** la regla pura (L1) — debe asertar la **secuencia**, no el código
  de la regla.
- **Qué debe permanecer exclusivamente aquí:** `Closed` derivado de anchor+checkpoint reales;
  la negativa **antes** del efecto con el árbol idéntico; el techo de recursos leído del
  journal y sobreviviente al reinicio; `mismo tree distinto SHA`; el pipeline de lifecycle
  con interrupción y rollback.

**L3 — END-TO-END / CERTIFICATION**
- **Propósito:** dos familias que comparten "no se puede construir con un fixture": (a) el
  paso por la frontera de proceso real (CLI, exit codes, stdout, hook) y (b) el estado
  canónico del repositorio real (planes, RFC, INDEX, payload, versión, tracking git).
- **Costo esperado:** (a) 0.1–0.5 s/test; (b) dominado por el tamaño del árbol.
  `MEDICIÓN` hoy: 3 tests END_TO_END en 1.30 s; 26 tests de certificación en 6.13 s.
- **Frecuencia:** en CI y en release; en local sólo si el sujeto canónico cambió.
- **Cambios que la disparan:** un `tools/*.py` (por su CLI), el árbol documental, el payload.
- **Qué no debe duplicar:** la regla (L1) — debe certificar **el estado**, no la regla.
- **Qué debe permanecer exclusivamente aquí:** los exit codes reales de los CLI que la
  batería ejecuta; el contrato de estabilidad de los 18 anclados; la contención de tracking
  git (`test_repo_containment.py`); la secuencia cross-proceso deny→PASS→allow (harness).

### 9.3 El segundo eje: regímenes de dependencia del mundo

| Régimen | Definición | Archivos | Tests | Consecuencia operativa |
|---|---:|---:|---:|---|
| **SELF-CONTAINED** | el test construye todo lo que necesita (`tmp_path`, payload sintético, fixtures vendorizadas) | 49 | 1145 | seleccionable por path/dependencia; portable; se puede aislar |
| **ANCHORED** | el test lee el estado canónico del repositorio o el árbol real **a propósito** | 20 | 398 | **no** seleccionable por path; contrato de estabilidad propio; estrictamente read-only |

`HECHO` El régimen ANCHORED **ya existe y ya está declarado** para 18 entradas en
`tests/AGENTS.md:73-91`. La contribución de este modelo es hacerlo **un eje de primera clase
en paralelo al nivel**, no una lista de excepciones.

`INFERENCIA` La matriz 4×2 explica por qué la selección pura por path falla: dos archivos
del mismo nivel y del mismo leg pueden diferir en si un cambio de documento los invalida.

### 9.4 Matriz nivel × régimen (`HECHO`)

| | SELF-CONTAINED | ANCHORED |
|---|---|---|
| **L0 UNIT** | 5 archivos (41) | 0 |
| **L1 COMPONENT/CONTRACT** | 23 + 4 archivos (704) | 4 archivos (14) |
| **L2 INTEGRATION** | 5 archivos (78) | 6 archivos (86) |
| **L3 E2E/CERT** | 4 archivos (44) | 10 archivos (298) |

---

## 10. Relación Costo / Valor

### 10.1 Clasificación

`INFERENCIA` Construida cruzando el tiempo medido con la garantía identificada en §3–§4.
**"Tiempo de ejecución" no se usó como sinónimo de "bajo valor".**

**HIGH VALUE / LOW COST** — el 76 % de la suite
- 609 tests COMPONENT en 10.64 s: cada `tools/check_*.py` por su API, sobre payload sintético.
- 41 tests UNIT en 0.03 s: vocabularios cerrados, puridad de identidad.
- 95 tests CONTRACT en 0.01 s: lockstep contract↔rules↔policy.
- 26 tests de certificación documental en 6.13 s: el estado canónico, con costo dominado por
  el tamaño del árbol y no por la repetición.
- `INFERENCIA` Este bloque es el mejor cociente del repositorio y **no debe tocarse**.

**HIGH VALUE / HIGH COST** — 5 archivos, 312.24 s, 77.6 % del reloj
- `test_autonomous_orchestrator.py` (97.30 s): `Closed` derivado de evidencia real; el guard
  de no-progreso; la continuidad tras reinicio.
- `test_agent_worker.py` (73.53 s): atribución de cambios sobre un árbol real; el contrato M4.
- `test_sae_scope_enforcement.py` (60.42 s): la negativa **antes** del efecto — la regresión
  reproducible de un incidente real.
- `test_autonomy_effects.py` (50.93 s): admisión all-or-nothing y techo desde evidencia.
- `test_check_lifecycle_checkpoint.py` (30.06 s): `mismo tree distinto SHA`; A1/A2 por
  correspondencia y no por recencia.
- **Veredicto:** `INFERENCIA` **alto valor, costo justificado en la garantía, no en el
  montaje.** La parte del costo que es garantía debe quedarse; la parte que es preparación
  repetida es el candidato legítimo de optimización (§13 C).

**LOW VALUE / LOW COST** — irrelevante para el reloj, relevante para el mantenimiento
- `test_health_probe.py::test_probe_cli_exit_code_and_json` (duplica `test_operational_invocations.py`).
- Assertions tautológicas enumeradas en §3.3e (≈12 sitios): no consumen tiempo, **consumen
  confianza** al inflar la lectura de cobertura.
- `HECHO` 7 archivos con `REPO_ROOT` muerto.
- 8 `tools/*.py` sin cobertura de CLI — el caso inverso: **HIGH VALUE ausente**, no low value.

**LOW VALUE / HIGH COST** — investigado explícitamente, según lo pedido

`HECHO` **Candidatos examinados y DESCARTADOS como low-value:**

| Candidato | Por qué parece low-value | Por qué NO lo es |
|---|---|---|
| `test_check_lifecycle_checkpoint.py` (30.06 s) | es "sólo" un checker de documentos | `empty_commit` + rama borrada prueban que la identidad material es el **tree id**, no el SHA: es la defensa contra un falso `Closed`. No reproducible sin git. |
| `test_check_dist_sync.py` (4.23 s, 7 tests) | un test cuesta 4.23 s para una comparación de bytes | `test_crlf_working_tree_does_not_fool_the_check` es el **único** test que detecta si la herramienta compara el árbol de trabajo en vez de los blobs. |
| `test_scoped_content_identity.py` (12.65 s) | recalcula lo que el tool ya calcula | recomputa con **primitivas git independientes** (`hash-object`, `ls-files -s`, `write-tree`): es un oráculo, no una repetición. |
| `test_repo_containment.py` (1.11 s por **1** test) | un test de un segundo | es el único que garantiza que una cita no apunta a un archivo **no versionado**; el `git ls-files` real es el sujeto. |
| `test_sae_scope_enforcement_dogfood.py` (11.90 s) | dogfood: parece duplicar el sintético | añade los pins documentales, el digest del plan del incidente y el escaneo de `git log` del repo real. |
| `test_enforced_flow.py` (1.30 s, 3 tests, 7 subprocesos) | 10 subprocesos para 3 aserciones | es el **único** END_TO_END del harness: la secuencia deny→PASS→allow medida en exit codes reales. |

`INFERENCIA` **No se encontró ningún grupo LOW VALUE / HIGH COST.** El costo alto está
siempre acompañado de una garantía que sólo existe con esa integración. Esta es una
conclusión negativa y es un resultado: **la suite no tiene grasa costosa; tiene montaje
costoso.**

### 10.2 La distinción que importa

```text
COSTO = GARANTÍA        →  los 5 archivos de L2/ANCHORED. NO optimizar la integración.
COSTO = PREPARACIÓN     →  el repositorio git reconstruido por test. SÍ optimizable.
COSTO = FRONTERA DE PROCESO por una aserción que ya existe en proceso
                        →  test_check_lifecycle_lineage.py, test_check_plan_citations.py.
                           SÍ aislable sin perder garantía.
```

`MEDICIÓN` Y la cuantificación del margen: los 4 archivos dominantes construyen ~85
repositorios git (≈29 s de `git init/add/commit` puro sobre 282 s). **El resto del costo de
esos archivos es ejecución real del host, no preparación** — lo que confirma que la palanca
de optimización es acotada y hay que medirla antes de prometerla.

---

## 11. Propuesta de Arquitectura Objetivo

### 11.1 La estructura

`RECOMENDACIÓN` La estructura del pedido
(`LOCAL → TARGETED → CI → FULL CANONICAL → RELEASE → FULL + CERTIFICATION/GATES`) es
**apropiada en su forma** y la evidencia no la contradice. Requiere **dos modificaciones**
basadas en evidencia: (1) `TARGETED` debe operar por **dos filtros ortogonales** (path y
régimen), no por uno; (2) `CI` y `FULL CANONICAL` deben ser **el mismo conjunto** — hoy no
hay diferencia y no hay evidencia que justifique crearla.

```text
LOCAL  ──────────────────────────────────────────────────────────────────────
  Un solo archivo tocado, en cualquier área.
  Regla: el/los archivos de test de esa área (path) + el smoke evergreen de contratos.
  Costo objetivo: < 15 s.
  MEDICIÓN de referencia: EARS 3.23 s · runtime/toolcalls 0.56 s
                          runtime/memory 0.26 s · runtime/placement 0.01 s
                          smoke de contratos+checkers 13.3 s (343 tests)
                    ↓
TARGETED ───────────────────────────────────────────────────────────────────
  Alcance determinable con seguridad.
  Regla: (módulos productivos tocados → cierre transitivo de imports → archivos de test)
         ∪ (contratos que el docstring/AGENTS.md declare para esos módulos)
  SIEMPRE añade, sin importar el path:
    · los archivos de test del/los módulos tocados y de los que dependen de ellos
    · los archivos con vínculo por subprocess textual al módulo tocado
  Costo objetivo: < 90 s. No pretende completitud.
                    ↓
CI ──────────────────────────────────────────────────────────────────────────
  Objetivo: detectar regresiones en cada push y cada PR.
  Regla: FULL CANONICAL. Sin excepción y sin reducción.
  Es exactamente lo que CI hace hoy (check-protocol.yml:35-46).
                    ↓
FULL CANONICAL ──────────────────────────────────────────────────────────────
  Objetivo: verde = la batería que define verde.
  Regla: python -m pytest tests/  (1358)
         python -m pytest protocol/.agents/harness/tests/  (185)
  Costo medido: 408.95 s (hoy) — 6 min 49 s.
  Este nivel NO se reduce como consecuencia de esta auditoría.
                    ↓
RELEASE ─────────────────────────────────────────────────────────────────────
  Objetivo: promover dev → master.
  Regla: FULL CANONICAL + los 7 comandos de la batería + gates C1/C2/C3
         + checkers específicos del área (lo que los planes 146/148 ya hacen).
  Sin reducción de alcance.
                    ↓
FULL + CERTIFICATION / GATES ────────────────────────────────────────────────
  Objetivo: certificar el estado canónico publicado.
  Regla: RELEASE + la categoría ANCHORED completa (los 20 archivos) ejecutada
         sobre el commit promovido + check_dist_sync.py en master.
  Aquí es donde el régimen ANCHORED se vuelve obligatorio en bloque.
```

### 11.2 Qué debe ejecutarse en cada contexto

**Desarrollo local — tras un cambio localizado**

| Se tocó | Ejecutar | Costo medido/estimado |
|---|---|---|
| un módulo de `runtime/memory/` | su archivo de test | 0.26 s (63 tests, 8 archivos) |
| un módulo de `runtime/toolcalls/` | sus archivos de test | 0.56 s (111 tests medidos) |
| `runtime/placement/` | sus 3 archivos | 0.01 s (46 tests) |
| `tools/check_ears_coverage.py` | sus 3 archivos | 3.23 s (91 tests) |
| cualquier `tools/check_*.py` sin CLI cubierto | su archivo + revisar §3.3f | 0.01–1.42 s |
| `runtime/orchestrator/*` | **el área completa** — no hay subconjunto útil | 306 s → **aquí la selección no ayuda** |
| `conftest.py` o `tests/pytest_isolation.py` | **FULL CANONICAL** | 408.95 s |

**Cambios transversales — alcance no determinable**

`RECOMENDACIÓN` Default conservador explícito y escrito, no inferido: si el alcance no se
puede determinar con seguridad, **FULL CANONICAL**. Casos que caen aquí por evidencia:
- cualquier cambio en un util compartido (`runtime/orchestrator/host.py` → 8 archivos;
  `protocol/.agents/harness/roots.py` → 13);
- cualquier cambio en un vocabulario compartido entre capas (§8.3.3);
- cualquier cambio en `docs/VERSIONING.md` §4.1, `docs/CONVENTIONS.md`,
  `docs/placement-contract.md` o `tests/AGENTS.md`;
- cualquier cambio en el estado canónico documental → los 20 archivos ANCHORED.

**CI** — `RECOMENDACIÓN` sin cambios: FULL CANONICAL en cada push y cada PR. Es lo que ya
ocurre y la evidencia no justifica ni un subconjunto ni una ampliación.

**Release** — `RECOMENDACIÓN` sin cambios respecto de la práctica de los planes 146/148,
más la ejecución **en bloque** de la categoría ANCHORED sobre el commit promovido.

### 11.3 Garantías que cada capa debe conservar en exclusiva

| Garantía | Capa donde debe vivir exclusivamente |
|---|---|
| Cierre de vocabularios y pureza de identidad | L0 |
| Reglas con código (`AEW-*`, `R1–R5`, `C-1/C-2/C-3`, exit codes de checker) | L1 |
| Secuencia de estados del host y del lifecycle | L2 |
| `mismo tree distinto SHA`; A1/A2 por correspondencia | L2 |
| Negativa **antes** del efecto con el árbol byte-idéntico | L2 |
| Exit codes reales de los CLI de la batería | L3 |
| Contrato de estabilidad y contenido de los 18 anclados | L3 |
| Contención de tracking git de las citas | L3 |
| Secuencia cross-proceso deny→PASS→allow | L3 |

`INFERENCIA` **Ninguna de estas garantías se duplica hoy entre capas** — el solapamiento
encontrado en §5 es de *sujeto* (varios archivos miran el mismo corpus) y de *regla*
(tres implementaciones del mismo presupuesto), no de *garantía*. El modelo de capas no
necesita eliminar duplicación: necesita hacer explícito el nivel real para poder seleccionar.

---

## 12. Riesgos

| # | Riesgo | Evidencia / base | Severidad |
|---|---|---|---|
| R1 | **False confidence por selección incompleta.** Un subconjunto verde con la suite completa en rojo. | `HECHO` 4 archivos no importan producción y sí la validan; 11 leen el árbol real; 8 invocan un tool por subprocess | **CRITICAL** |
| R2 | **Tests documentales no detectables por imports.** Un cambio de plan/RFC/INDEX/payload invalida archivos que no importan nada. | `HECHO` 20 archivos ANCHORED, 398 tests: `test_adversarial_deliberation.py`, `test_fc_isolation_declaration.py`, `test_fc_recovery_alignment.py`, `test_root_contract.py`, los dogfood | **HIGH** |
| R3 | **Infraestructura de test compartida de alcance universal.** | `HECHO` `conftest.py` + `tests/pytest_isolation.py` afectan a toda la suite; el plan 145 causó fallos no deterministas por exactamente esto | **HIGH** |
| R4 | **Pérdida de cobertura de integración al "aislar" por impulso.** | `HECHO` los 4 archivos dominantes no son de-aislables: su garantía es la integración. Convertirlos sería destruir la garantía, no optimizarla | **HIGH** |
| R5 | **Optimización que introduce flakiness.** | `HECHO` plan 145 ya endureció el scratch por no-determinismo; `HECHO` el fixture del repositorio dentro del test es *deliberado* (docstring: "no usan `tmp_path` a propósito"). Compartir el repositorio entre tests es exactamente el patrón que el plan 145 eliminó | **HIGH** |
| R6 | **Selección incorrecta por nombre de archivo.** Asumir que el prefijo determina el nivel. | `HECHO` `test_check_lifecycle_checkpoint.py` es COMPONENT por imports y L2 por dependencia; `test_audit_gates.py` es un teste del stub; `test_pytest_isolation.py` hace `os.walk` del repo | **HIGH** |
| R7 | **Deriva silenciosa del mapa de selección.** Un archivo nuevo cuya producción no se mapea no se ejecuta nunca. | `INFERENCIA` hoy el mapa vive en `tests/AGENTS.md` (sólo anclados) y en la cabeza del agente | **MEDIUM** |
| R8 | **Reducción aparente sin reducción real.** Para cambios en orchestrator, seleccionar no ahorra. | `MEDICIÓN` 294 tests / ~306 s para el área; 97.30 s para un solo archivo | **MEDIUM** |
| R9 | **Excesiva fragmentación por splits.** 24 archivos `POSSIBLE SPLIT` → hasta 48 archivos. | `INFERENCIA` `HECHO` `tests/` ya es plano con 57 archivos sin subdirectorios; duplicar la cantidad empeora la navegación sin reducir un segundo de la suite completa | **MEDIUM** |
| R10 | **Aumento de la complejidad de mantenimiento.** Tres listas de clasificaciones esperadas deben actualizarse juntas (C-1/C-2/C-3). | `HECHO` §5.2 grupo 2 | **MEDIUM** |
| R11 | **Estado global / orden implícito.** | `HECHO` `test_check_version_state.py:33` parchea `cvs.get_tags` **sin `monkeypatch`** y lo deja filtrado; `HECHO` `test_pytest_isolation.py` hace `clear_own_scratch` y crea directorios probe en la sesión viva. Hoy el orden por defecto lo enmascara | **MEDIUM** |
| R12 | **El verde del harness no es el verde del adoptante.** | `HECHO` `test_operational_invocations.py` y `test_root_contract.py` leen el árbol **del repositorio DEV** para certificar el payload; en un proyecto adoptante esos caminos no existen | **MEDIUM** |
| R13 | **Cobertura de CLI ausente en 8 tools.** | `HECHO` §3.3f | **MEDIUM** |
| R14 | **Umbral de coverage como criterio de selección.** | `MEDICIÓN` la suite es I/O-bound; instrumentarla es impracticable y la cobertura mide *lo ejecutado antes*, no *lo que puede fallar* | **LOW** (riesgo de mala política, no de estado actual) |

---

## 13. Recomendaciones Priorizadas

`RECOMENDACIÓN` **Ninguna de estas recomendaciones está implementada.** Este informe no
autoriza trabajo; cada una requiere su vía de gobernanza (RFC-56) si se decide ejecutarla.

### A. NO CAMBIAR

**A-1. El leg del protocolo harness, tal como está.**

```text
PROBLEM      Ninguno. 185 tests en 7.05 s es el mejor cociente del repositorio.
EVIDENCE     MEDICIÓN §2.1; ningún archivo del leg supera 1.6 s; 4 archivos en INTEGRATION/
             END_TO_END y todos son agregados, no duplicaciones (salvo un caso, D-4).
PROPOSED DIRECTION   Ninguna. No fusionar con la batería canónica ni fragmentar.
EXPECTED BENEFIT     Preservar el mejor cociente test/segundo y la separación producto/DEV.
RISK                 Ninguno identificado.
CONFIDENCE           HIGH
```

**A-2. Las 28 archivos COMPONENT y los 5 UNIT.**

```text
PROBLEM      Ninguno. 609 tests en 10.64 s (17 ms/test) y 41 tests en 0.03 s.
EVIDENCE     MEDICIÓN §4.1; §7.2. Cada uno es la única cobertura de su módulo.
PROPOSED DIRECTION   Ninguna.
EXPECTED BENEFIT     Mantener el 76 % de la suite dentro de presupuesto.
RISK                 Ninguno identificado.
CONFIDENCE           HIGH
```

**A-3. Las 5 garantías que exigen integración real.**

```text
PROBLEM      Costo alto, pero el costo ES la garantía.
EVIDENCE     HECHO §3.3d y §10.2: mismo tree distinto SHA; negativa antes del efecto con
             árbol idéntico; techo desde journal y sobreviviente al reinicio; Closed desde
             anchor+checkpoint reales; contenido con git tracking real.
PROPOSED DIRECTION   Ninguna conversión a unitario. Conservar la integración.
EXPECTED BENEFIT     Evitar el riesgo R4 (pérdida de garantía) y R5 (reintroducir flakiness).
RISK                 Ninguno; no actuar es aquí la acción correcta.
CONFIDENCE           HIGH
```

**A-4. La batería canónica como definición de verde en CI.**

```text
PROBLEM      Ninguno en CI. Correr todo en cada push es correcto y ya ocurre.
EVIDENCE     HECHO check-protocol.yml:35-46 ejecuta ambos legs en cada push y PR.
PROPOSED DIRECTION   Ninguna reducción. Esta auditoría no reduce la suite canónica.
RISK                 Ninguno.
CONFIDENCE           HIGH
```

### B. REDISTRIBUIR / REESTRUCTURAR

**B-1. Separar la mitad pura de los 6 archivos de nivel mixto con ganancia real.**

```text
PROBLEM      Seis archivos contienen una mitad de lógica pura y una mitad de integración real.
             La mezcla impide la selección precisa y oculta el sujeto de cada test.
EVIDENCE     HECHO §7.4: test_agent_worker.py (contrato M4/delegación vs host sobre git);
             test_autonomous_orchestrator.py (contrato WorkerAdapter por AST vs loop real);
             test_sae_scope_enforcement.py (~30 tests de frontera vs 13 de host);
             test_autonomy_effects.py (secciones 1/2/5 puras vs gate del host);
             test_autonomous_scope.py (~60 puros vs 4 de host);
             test_determine_execution_state.py (~46 sin git vs 23 con git).
PROPOSED DIRECTION   Extraer la mitad pura a un archivo propio por sujeto, dejando el archivo
             de integración con la mitad que sólo existe con el mundo real. Mantener en
             TODOS los casos una prueba de integración para la mitad extraída.
EXPECTED BENEFIT     Selección por path precisa; la mitad pura corre en milisegundos; el
             sujeto bajo prueba se vuelve explícito. Habilita B-3 sobre el mismo trabajo.
RISK         HIGH — es el cambio de mayor superficie del informe. Toca 6 archivos de test,
             mueve cientos de líneas y puede introducir acoplamiento de fixtures compartidas.
             Debe hacerse archivo por archivo, no en bloque.
CONFIDENCE   HIGH en el diagnóstico; MEDIUM en que el beneficio justifique el costo hoy.
```

**B-2. Hacer explícito el régimen ANCHORED como eje de primera clase.**

```text
PROBLEM      El régimen ANCHORED existe y está declarado para 18 entradas en tests/AGENTS.md,
             pero como lista de excepciones, no como eje paralelo al nivel. Dos archivos del
             mismo nivel difieren en si un cambio de documento los invalida, y eso no se ve.
EVIDENCE     HECHO §9.3: 20 archivos (398 tests) dependen del estado canónico o del árbol
             real; HECHO tests/AGENTS.md:73-91 declara 18. Diferencia: test_root_contract.py
             y los dogfood del harness no están en la tabla aunque sí leen el árbol real.
PROPOSED DIRECTION   Reconocer el régimen en la documentación de tests con el nivel real de
             cada archivo, extendiendo la tabla existente en lugar de crear un mecanismo
             nuevo. Documento de navegación, no checker.
EXPECTED BENEFIT     La selección targeted deja de depender de la memoria del agente; el
             contrato de estabilidad queda explícito para los 20 y no para 18.
RISK         MEDIUM — toca documentación de tests (permitido sólo con la vía de gobernanza)
             y añade un artefacto que puede derivar (R7).
CONFIDENCE   MEDIUM
```

**B-3. Reemplazar lanzamientos de intérprete por llamadas en proceso donde la garantía se conserva.**

```text
PROBLEM      test_check_lifecycle_lineage.py lanza sys.executable ~40 veces para aserciones
             de exit code que verify_all ya implica; test_check_plan_citations.py 3 veces.
EVIDENCE     HECHO §7.5; MEDICIÓN arranque de intérprete 0.050 s; el archivo cuesta 4.71 s
             para 35 tests.
PROPOSED DIRECTION   Usar main() + capsys como hacen las suites EARS, CONSERVANDO un test de
             proceso real por archivo (en lineage, para el contrato de CLI; en citations,
             test_runs_from_other_cwd, que sólo existe con un proceso nuevo).
EXPECTED BENEFIT     Elimina ~30 arranques de intérprete; conserva íntegra la garantía de
             exit code y de independencia de cwd.
RISK         LOW — patrón ya probado en 3 suites del mismo repositorio (EARS y dogfood).
CONFIDENCE   HIGH
```

**B-4. Corregir las assertions que no pueden fallar y los parches filtrados.**

```text
PROBLEM      ~12 aserciones tautológicas o inertes (§3.3e) y un parche de módulo no
             restaurado (test_check_version_state.py:33) que deja el camino real de git tags
             sin cobertura para el resto de la sesión.
EVIDENCE     HECHO §3.3e: assert x == x en test_sae_scope_enforcement.py:1034,
             test_change_governance.py, test_project_segment.py,
             test_check_ears_coverage_falsification.py:414, test_legacy_paths.py:72-78.
PROPOSED DIRECTION   Reemplazar por la aserción que el nombre promete, o eliminar la línea.
             En version_state, usar monkeypatch para el stub de get_tags.
EXPECTED BENEFIT     Recupera confianza real sin cambiar el reloj. Impacto directo sobre R1
             (false confidence): hoy un verde puede significar que la aserción era inerte.
RISK         LOW técnico. MEDIUM de gobernanza: toca archivos de test.
CONFIDENCE   HIGH
```

**B-5. Cubrir la frontera de CLI ausente en 8 tools.**

```text
PROBLEM      8 de 20 tools/*.py no tienen ninguna prueba de CLI ni de exit code, aunque la
             batería y CI los invocan precisamente como scripts.
EVIDENCE     HECHO §3.3f: check_architecture_traceability, check_memory_store,
             check_taxonomy_coherence, check_version_state, aggregate_metrics,
             check_session_artifacts, determine_execution_state, audit_gates.
PROPOSED DIRECTION   Un test de CLI por tool, siguiendo el patrón de test_measure_context_budget.py
             y test_check_plan_citations.py: argv, exit code, stdout.
EXPECTED BENEFIT     Cierra una brecha de garantía real sobre el contrato que CI consume.
RISK         LOW. Costo añadido: ~8 lanzamientos de intérprete, menos de 1 s.
CONFIDENCE   HIGH
```

### C. OPTIMIZAR

**C-1. Atacar el costo de montaje del repositorio en los 4 archivos dominantes.**

```text
PROBLEM      4 archivos (152 tests) consumen 282.18 s. Cada test construye su propio
             repositorio git: 32 + 23 + 16 + 14 = 85 construcciones, a 0.340 s el primitivo
             medido (git init + add + commit) = ~29 s sólo de creación de repositorio.
             El resto del costo es ejecución real del host, que no debe eliminarse.
EVIDENCE     MEDICIÓN §6.2 y §6.3; HECHO 254 sitios de llamada a constructores de repositorio
             en toda la suite; HECHO los docstrings de los 2 archivos mayores declaran que
             NO usan tmp_path a propósito.
PROPOSED DIRECTION   Investigar primero, optimizar después: (a) medir cuánto de los 282 s es
             montaje y cuánto es ejecución real del host, por test; (b) sólo si el montaje es
             dominante, evaluar reutilizar una plantilla de repositorio copiada por test
             (no compartida entre tests) o un repositorio pre-inicializado clonado.
             NO compartir un repositorio mutable entre tests: es el patrón que el plan 145
             eliminó.
EXPECTED BENEFIT   Techo medible: si el montaje fuese el 100 % de los 85 repositorios,
             ~29 s. La promesa realista es del orden de 20–60 s sobre 408.95 s (−5 % a −15 %),
             NO la reducción del 52 % que estima el informe de costo previo, que atribuye a
             montaje un costo que la evidencia localiza en la ejecución del host.
RISK         HIGH — el aislamiento por test es deliberado (plan 145). Cualquier plantilla
             compartida reintroduce el no-determinismo que ese plan eliminó (R5). Requiere
             lectura previa del plan 145.
CONFIDENCE   MEDIUM en el diagnóstico; LOW en que la ganancia justifique el riesgo.
```

**C-2. Medir el costo del host loop antes de prometer cualquier reducción.**

```text
PROBLEM      No hay medición de cuánto de los 282 s corresponde a iteraciones del host y a
             subprocesos de verificación lanzados dentro del bucle.
EVIDENCE     HECHO test_revalidation_is_recorded_as_a2 corre 4 + 12 iteraciones (19.95 s);
             HECHO cada iteración lanza los 3 check_lifecycle_* y check_ok.py como subprocesos;
             HECHO test_full_loop_derives_closed_from_real_evidence hasta 12 iteraciones.
PROPOSED DIRECTION   Instrumentar (sin modificar tests) el número de iteraciones y de
             subprocesos por test en una corrida de diagnóstico, y decidir con ese número.
EXPECTED BENEFIT   Convierte C-1 de hipótesis en decisión medida. Evita una optimización que
             ataque el 10 % del costo creyendo atacar el 80 %.
RISK         LOW — es medición, no cambio.
CONFIDENCE   HIGH
```

**C-3. Smoke evergreen para el bucle de desarrollo local.**

```text
PROBLEM      El bucle local necesita un conjunto que quepa en el presupuesto de feedback y
             que no dependa de juicio por cambio.
EVIDENCE     MEDICIÓN: checkers DEV + contratos ≈ 343 tests en 13.3 s (suma de duraciones);
             EARS 3.23 s; toolcalls 0.56 s; memory 0.26 s; placement 0.01 s.
PROPOSED DIRECTION   Un conjunto de paths fijo (12–15 archivos de contrato y checkers) como
             primer comando del bucle local, ANTES del conjunto targeted. Son paths, no markers.
EXPECTED BENEFIT   Feedback en ~13 s para cualquier cambio, independiente del alcance.
RISK         LOW — es un subconjunto explícito, no una afirmación de completitud.
CONFIDENCE   HIGH
```

### D. SELECCIONAR

**D-1. Adoptar TARGETED por path como primer filtro.**

```text
PROBLEM      Hoy todo cambio corre 408.95 s, incluyendo cambios en áreas que tardan 0.01–3.23 s.
EVIDENCE     MEDICIÓN §11.2: memory 0.26 s, toolcalls 0.56 s, placement 0.01 s, EARS 3.23 s.
             HECHO los planes 137/144/145 ya citan command-sets por archivo: la práctica existe.
PROPOSED DIRECTION   Regla escrita: los archivos de test del área tocada, más el smoke de C-3.
             Sin markers, sin coverage, sin tooling nuevo.
EXPECTED BENEFIT     −79 % a −99.9 % en el 60–88 % de los cambios (los que caen fuera de
             runtime/orchestrator). Cero ahorro en runtime/orchestrator (R8), y eso debe
             declararse, no ocultarse.
RISK         HIGH — R1 (false confidence). Requiere el default conservador de D-3.
CONFIDENCE   HIGH en la viabilidad; el beneficio depende de la mezcla real de cambios.
```

**D-2. Calcular el cierre transitivo de imports en lugar de enumerar a mano.**

```text
PROBLEM      El mapa módulo→tests vive en la cabeza del agente; deriva (R7).
EVIDENCE     HECHO 65 de 69 archivos importan ≥1 módulo productivo; HECHO el bootstrap de
             sys.path es único y declarado (conftest.py:73-75); HECHO 47 de 71 módulos tienen
             1–3 archivos directos.
PROPOSED DIRECTION   Derivar el path-set del grafo de imports en vivo (AST), con re-exports
             de paquete resueltos y detección textual de subprocess a tools/*.py. No
             versionar el mapa: computarlo.
EXPECTED BENEFIT     Deja de olvidar los indirectos: host.py arrastra 8 archivos,
             roots.py 13.
RISK         MEDIUM — la semántica del cierre transitivo debe decidirse (¿roots.py arrastra
             todo el harness?). Sin ella, sobre-selecciona.
CONFIDENCE   HIGH técnicamente; requiere decisión de semántica.
```

**D-3. Declarar el default conservador y las dos categorías globales.**

```text
PROBLEM      Sin regla escrita, la selección falla en silencio en los casos no cubiertos.
EVIDENCE     HECHO §8.3: infraestructura de test compartida (conftest.py, pytest_isolation.py);
             estado canónico documental (20 archivos); vocabulario compartido entre capas.
PROPOSED DIRECTION   Regla explícita, escrita y no inferida:
             · cambio en conftest.py, tests/pytest_isolation.py o el bootstrap → FULL.
             · cambio en plan/RFC/ADR/INDEX/payload/VERSION/CHANGELOG → ANCHORED completo.
             · cambio no mapeado → FULL.
RISK         MEDIUM de gobernanza — cambiar el command-set cambia lo que el Validation Anchor
             certifica (docs/VERSIONING.md §4.1). Es una decisión humana, no de tooling.
CONFIDENCE   HIGH en la necesidad; la decisión es del mantenedor.
```

**D-4. Unificar el único caso de duplicación literal del harness.**

```text
PROBLEM      test_health_probe.py::test_probe_cli_exit_code_and_json y
             test_operational_invocations.py::test_health_check_documented_invocation lanzan
             el mismo CLI y asertan lo mismo (PASS + exit 0).
EVIDENCE     HECHO §5.2 grupo 6. Es el ÚNICO caso de REDUNDANT puro detectado en 1543 tests.
PROPOSED DIRECTION   Conservar la versión en test_operational_invocations.py (que además
             prueba el layout adoptado) y dejar el probe en test_health_probe.py a nivel
             componente. Decisión de gusto, no de costo.
EXPECTED BENEFIT     Elimina 1 lanzamiento de intérprete. Irrelevante para el reloj.
RISK         LOW.
CONFIDENCE   HIGH en el diagnóstico; LOW en que valga una intervención.
```

---

## 14. Conclusión Ejecutiva

**1. ¿La distribución actual de tests es arquitectónicamente razonable?**
`INFERENCIA` **En cantidad, sí; en niveles, parcialmente.** 47 de 71 módulos productivos
tienen 1–3 archivos directos sin solapamiento anómalo; no hay duplicación literal; el 76 %
de la suite (609 COMPONENT + 41 UNIT + 95 CONTRACT + 26 de certificación) corre en 16.8 s y
está correctamente nivelado. Lo que no es razonable es que **20 archivos (585 tests, 337.44 s)
contengan dos niveles distintos**, porque eso hace imprecisa cualquier selección y oculta el
sujeto real de parte de cada archivo.

**2. ¿Dónde existe concentración injustificada?**
`MEDICIÓN` **La concentración de tiempo no está injustificada; la de mezcla de niveles, sí.**
5 archivos = 77.6 % del reloj, y cada uno protege una garantía que exige integración real
(§3.3d). **No hay concentración injustificada de tests.** Lo que hay es (a) 12 archivos donde
parte de los tests prueban otro componente como sujeto real (§3.3a) y (b) 8 `tools/*.py` sin
cobertura de CLI (§3.3f) — concentración *desplazada*, no excesiva.

**3. ¿Qué tests deberían permanecer integrados?**
`HECHO` Los 5 archivos que declaran `KEEP AS INTEGRATION` (80 tests, 48.85 s) más la mitad
integrada de los 6 archivos de §7.4. En particular, y sin excepción: `mismo tree distinto SHA`
(`test_check_lifecycle_checkpoint.py`), la negativa **antes** del efecto con árbol
byte-idéntico (`test_sae_scope_enforcement.py`), el techo leído del journal
(`test_autonomy_effects.py`), `Closed` desde anchor+checkpoint reales
(`test_autonomous_orchestrator.py`), la contención de git tracking (`test_repo_containment.py`)
y la secuencia cross-proceso deny→PASS→allow (`test_enforced_flow.py`).

**4. ¿Qué tests podrían aislarse?**
`INFERENCIA` **La mitad pura de 6 archivos** (§7.4): `test_agent_worker.py`,
`test_autonomous_orchestrator.py`, `test_sae_scope_enforcement.py`, `test_autonomy_effects.py`,
`test_autonomous_scope.py`, `test_determine_execution_state.py`. Más dos intervenciones
puntuales de frontera de proceso: `test_check_lifecycle_lineage.py` (~40 → 1 lanzamiento) y
`test_check_plan_citations.py` (3 → 1). **Nada más**: los otros 18 `POSSIBLE SPLIT` son
reorganización de nivel idéntico sin ganancia y con riesgo de fragmentación (R9).

**5. ¿Cuáles son los principales candidatos de optimización?**
`MEDICIÓN` (a) El **montaje de repositorio git** en los 4 archivos dominantes: 85
construcciones × 0.340 s ≈ **29 s** de costo puro de preparación, dentro de 282.18 s.
(b) Los **lanzamientos de intérprete por aserción en proceso** en
`test_check_lifecycle_lineage.py` (~30 innecesarios). (c) **Nada más**: la medición de §6.4
descarta fixtures, parametrize, cantidad de módulos, volumen de aserciones y filesystem.

**6. ¿Cuánto del costo actual podría reducirse sin eliminar garantías?**
`INFERENCIA` **Del orden de 30–60 s sobre 408.95 s: un 7–15 %.**
- Efecto de B-3 (intérprete en proceso): ~1.5 s.
- Efecto de C-1 (plantilla de repositorio): ~29 s como **techo absoluto**, realista 15–25 s,
  con riesgo alto por R5.
- Efecto de nada en la selección targeted sobre la suite completa (mueve tests, no los elimina).
`INFERENCIA` **La reducción grande no existe en el estado actual.** El informe de costo
previo estimó −52 % asumiendo que los 290 s son montaje; la evidencia de este informe
localiza la mayor parte de ese tiempo en **ejecución real del host** (iteraciones y
subprocesos de verificación), y **C-2 propone medirlo antes de prometerlo**. La palanca
grande es la **selección** (que no reduce la suite completa, reduce el bucle local) y es de
−79 % a −99.9 % en el 60–88 % de los cambios.

**7. ¿Qué parte del problema debe resolverse mediante selección targeted?**
`INFERENCIA` **El bucle local.** Para cambios fuera de `runtime/orchestrator/` —que según
`MEDICIÓN` incluyen `tools/`, `runtime/memory/`, `runtime/toolcalls/` y
`runtime/placement/`— el costo de validación baja dos a tres órdenes de magnitud (de 408.95 s
a 0.01–13.3 s). Para `runtime/orchestrator/`, la selección **no aporta** (el área entera
cuesta ~306 s y un solo archivo 97.30 s) y eso debe declararse explícitamente para no crear
la ilusión de un gate liviano (R8).

**8. ¿Qué parte debe resolverse optimizando los propios tests?**
`INFERENCIA` **Tres cosas concretas y acotadas:** (a) el montaje de repositorio en los 4
archivos dominantes — tras medirlo (C-1 + C-2); (b) los lanzamientos de intérprete
redundantes en 2 archivos (B-3); (c) las ~12 aserciones inertes y el parche filtrado (B-4),
que no son un problema de tiempo sino de **confianza** (R1).

**9. ¿Qué parte requiere redistribución arquitectónica?**
`INFERENCIA` **La separación de la mitad pura de los 6 archivos de nivel mixto (B-1)** y la
**explicitación del régimen ANCHORED como eje paralelo al nivel (B-2)**. Lo primero habilita
que la selección por path sea precisa; lo segundo evita que la selección falle en silencio
sobre los 20 archivos que dependen del estado canónico (R2). Ninguna de las dos cambia *qué*
se prueba.

**10. ¿Cuál debería ser el orden correcto de implementación?**
`RECOMENDACIÓN` El orden que la evidencia impone, de menor a mayor riesgo y de mayor a menor
certeza de beneficio:

```text
0. Decisión de gobernanza (no técnica): ¿se quiere un comando distinto por contexto?
   Sin esto, nada de lo demás puede implementarse — docs/VERSIONING.md §4.1 define la batería.
        ↓
1. B-4 (corregir aserciones inertes y el parche filtrado)   — riesgo LOW, recupera confianza.
2. B-5 (cobertura de CLI en los 8 tools)                    — riesgo LOW, cierra brecha real.
3. C-2 (medir iteraciones y subprocesos por test)           — riesgo NULO, habilita C-1.
4. B-3 (intérprete en proceso donde la garantía se conserva) — riesgo LOW, patrón ya probado.
5. C-3 (smoke evergreen) + D-1 (TARGETED por path)          — riesgo MEDIO, mayor beneficio local.
6. D-3 (default conservador y categorías globales)          — riesgo MEDIO, imprescindible antes de confiar en D-1.
7. D-2 (cierre transitivo por AST)                          — riesgo MEDIO, elimina la deriva del mapa.
8. B-2 (régimen ANCHORED explícito)                         — riesgo MEDIO, documentación.
9. B-1 (separar la mitad pura de los 6 archivos mixtos)     — riesgo HIGH, archivo por archivo.
10. C-1 (plantilla de repositorio en los 4 dominantes)      — riesgo HIGH, SÓLO con el número
    de C-2 en la mano y tras leer el plan 145.
```

`RECOMENDACIÓN` **Los pasos 1–4 son seguros y de beneficio cierto.** Los pasos 5–7 son el
grueso del valor para el bucle local y exigen la decisión de gobernanza del paso 0. Los pasos
8–10 son los de mayor riesgo: **no deben iniciarse sin que C-2 haya medido primero**, porque
la evidencia de este informe no sostiene que el montaje domine el costo de los archivos que
dominan el reloj.

**No hacer nada también es un resultado válido.** La suite no tiene grasa costosa, no tiene
duplicación que eliminar y no tiene tests de bajo valor: tiene un problema de **granularidad
de niveles** (selección) y un problema de **costo de montaje localizado en 4 archivos**
(optimización) que la evidencia acota a un 7–15 % de techo y que conviene medir antes de
perseguir.

---

## Anexo A — Trazabilidad de las afirmaciones de evidencia

| Afirmación | Fuente |
|---|---|
| 1543 tests, 1542 passed 1 skipped | `MEDICIÓN` corrida completa, §1 |
| 408.95 s / 402.31 s call / 1.71 s setup / 0.01 s teardown | `MEDICIÓN` `--durations=0` |
| 5 archivos = 77.6 % del call time | `MEDICIÓN` agregación por archivo |
| 20 archivos ANCHORED, 398 tests, 356.71 s | `HECHO` clasificación de dependencia + `tests/AGENTS.md:73-91` |
| 254 sitios de construcción de repositorio | `HECHO` análisis AST |
| git init+add+commit = 0.340 s; intérprete = 0.050 s | `MEDICIÓN` micro-benchmark, §6.2 |
| 1274 de 2820 funciones sin fixture | `HECHO` análisis AST de firmas |
| 26 definiciones de fixture en 8 archivos | `HECHO` análisis AST |
| 12 archivos prueban otro componente como sujeto | `HECHO` lectura completa de los 69 archivos |
| 8 tools sin cobertura de CLI | `HECHO` grep de `main(`/subprocess por archivo |
| 4 archivos sin import de producción | `HECHO` análisis AST de imports |
| 7 archivos con `REPO_ROOT` muerto | `HECHO` grep + verificación de uso |
| Único skip: `cacheprovider disabled` | `MEDICIÓN` `-rs` |
| Ningún grupo LOW VALUE / HIGH COST | `INFERENCIA` §10.1, con los 6 candidatos examinados |
| Techo de optimización 7–15 % | `INFERENCIA` §14.6, a partir de §6.2–6.3 |

## Anexo B — Preguntas abiertas

1. **¿Cuánto de los 282 s de los 4 archivos dominantes es montaje y cuánto ejecución del
   host?** `HECHO` no medido. Es el prerrequisito de C-1 y la única forma de convertir el
   techo de optimización de estimación en número.
2. **¿El plan 145 permite reutilizar el montaje del repositorio entre tests?** `HECHO` ese
   plan eliminó precisamente el scratch compartido por no-determinismo. Requiere lectura
   antes de proponer nada.
3. **¿Cuál es el presupuesto de feedback aceptable en el bucle local?** `HECHO` no hay target
   declarado en ningún documento del repositorio. Sin número, C-3 y D-1 no se pueden
   dimensionar.
4. **¿Cuál es la mezcla real de alcance de los cambios?** `INFERENCIA` determina el ahorro
   ponderado de D-1: con ~60 % de los cambios fuera de `runtime/orchestrator`, el ahorro
   ponderado del bucle local es del orden del 50–60 %; con el 20 %, es mucho menor.
5. **¿`runtime/orchestrator/__main__.py` (200 líneas, 0 archivos de test) necesita cobertura?**
   `HECHO` es el único módulo productivo de `runtime/` sin ningún archivo de test asociado
   (junto con `protocol/.agents/harness/lifecycle_staging.py`, tocado sólo transitivamente).
6. **¿La categoría ANCHORED debe incluir `test_root_contract.py` y los dogfood del harness?**
   `HECHO` leen el árbol real, pero `test_root_contract.py` no está en la tabla de
   `tests/AGENTS.md:73-91`. La tabla actual tiene 18 entradas y el análisis identifica 20.
7. **¿El costo medido en Windows es representativo?** `MEDICIÓN` todas las cifras son de esta
   máquina (Windows, OneDrive). `HIPÓTESIS` en Linux el costo de creación de procesos git es
   sensiblemente menor, lo que reduciría tanto el costo de los 4 archivos dominantes como el
   beneficio de C-1.
