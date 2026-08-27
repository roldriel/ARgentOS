# Plan 19 — Anexo B: Reporte de estado del protocolo post-dogfooding

**Fecha:** 2026-08-05. **Sesión de dogfooding:** `.project/d4ab6a93-8e75-4880-baf3-676fce992936/` (iteración `00`, 13 artefactos + SESSION_LOG + HARNESS_REPORT + METRICS + SESSION_BRIEF).
**Ejercicio:** proyecto real (`tools/check_plan_citations.py`, 19 tests) ejecutado estrictamente por protocolo, ciclo completo: discovery (scope full) → análisis → clarificación (×2) → especificación → contexto → validación → plan → review → ejecución TDD → verificación → `COMPLETED`, con 1 recovery real. Bitácora: `plans/19-anexo-a-bitacora-fricciones.md`.

## Métricas de la sesión (plan 17, `python .agents/harness/runner.py metrics --session …`)

| Métrica | Valor | Lectura |
|---|---|---|
| Gates H | 13 invocaciones, 1 FAIL (H01) | 92% PASS a la primera en gates core |
| Gates D | 3 invocaciones, 1 FAIL (D01) | el FAIL de D01 es el defecto F-11 (gate no superable tal como está spec'd) |
| Transiciones | 15 | incluye 2 loops de clarificación y 1 recovery |
| Recovery entries | 1 | disparado por un fallo de formato — costo desproporcionado (F-02/F-03) |
| Clarification entries | 2 | ambas resueltas en modo desatendido (F-05) |
| Reviewer retries | 0 | 1 reviewer invocation (APPROVE a la primera) |
| Failures por clase | F5: 1, F3: 1 | coherente con la bitácora |
| Delegaciones | 9, 0 violaciones de validez | H15 pre-delegation PASS en todas |
| Flags declarativos evidenciados | 5/16 | los no evidenciados son prácticas técnicas no aplicables a esta tarea; la métrica no distingue "no aplica" de "obligación ignorada" (dato para el modelo de métricas) |
| Iteraciones / duración | 1 iteración, ~52 min | incluye discovery full en paralelo |

## Veredicto por subsistema

### Core (orquestador, máquina de estados, workflow, contratos de fase) — **OPERATIVO CON FRICCIONES**

El pipeline completo se ejecutó sin atajos y produjo un deliverable real verificado (8/8 criterios EARS PASS, 19 tests). Las compuertas machine (H00–H07, H11) son rápidas y auditables. Las fricciones se concentran en tres puntos: (1) desalineación contrato↔validador en criterios EARS (F-01); (2) el lazo de recovery es inviable económicamente para fallos triviales de formato — el árbol no expresa retry y la máquina de estados no modela la vuelta a fases tempranas (F-02, F-03); (3) documentos normativos que se contradicen en bordes (INTENT_REFLECTION con HIGH, F-04). Ninguna impidió completar; todas quedaron registradas como dato.

### Discovery — **FUNCIONAL, CON UN GATE ROTO Y DEUDA DE CONTRATOS**

Pipeline full ejecutado: 7/7 workers, `DISCOVERY_READY`, KB refrescada (17 entradas, manifest, hashes, marcador en la ruta de spec). D00 PASS a la primera. D01 solo pasó con un artefacto-puente: el gate machine no es superable tal como está especificado (F-11, crítica). Contratos con inconsistencias menores acumuladas (F-13, F-14, F-15, F-17, F-18, F-19). El merge de KB legada funcionó como fue diseñado (F-21, señal positiva). El subsistema es usable pero su gate de salida requiere workaround en cada ejecución.

### System (bootstrap, health-check) — **SAN**

Health-check PASS (12:27Z), `.project/` inicializado, marcador dentro de TTL, sin intervención. Ninguna fricción observada en este subsistema durante la sesión. Dato menor: el health-check no valida el marcador `.last_discovery` (relacionado con F-12).

### Harness (runner, policies, árboles, métricas, H15) — **OPERATIVO, CON GAPS DE COBERTURA**

Runner estable y rápido; reportes acumulativos correctos; métricas agregadas por sesión coherentes con la bitácora. Decision trees: ejecutados en un caso real (H01) y su veredicto fue técnicamente correcto pero económicamente desproporcionado (F-02). H15: la evaluación machine existe y detecta violaciones reales (post-return FAIL→PASS), pero no está cableada al CLI (F-08). Cobertura: D01 es el único gate estructuralmente no superable (F-11). El agregador de métricas no distingue flags no aplicables de obligaciones ignoradas (dato, §Métricas).

## Estado agregado

El protocolo **se sostiene end-to-end en condiciones reales**: una tarea pequeña con ambigüedad deliberada recorrió el ciclo completo — incluidos recovery y dos clarificaciones — y terminó en `COMPLETED` con evidencia verificable en cada transición. El costo de fricción se concentra en (a) un gate discovery roto, (b) el lazo de recovery para fallos triviales, y (c) inconsistencias contrato↔runner de bajo costo unitario pero recurrentes. Nada de lo observado invalida el modelo conceptual; todo lo crítico es reparable con ajustes de policies/contratos y dos planes acotados. El backlog priorizado vive en `plans/INDEX.md` §Backlog evidenciado - plan 19.

## Dato de producto fuera de alcance (registrado, no actuado)

La primera ejecución real de la herramienta construida reporta **44 citas rotas en `plans/`** (anchors numéricos prohibidos, anchors a secciones inexistentes, archivos inexistentes) — ver `.project/d4ab6a93-8e75-4880-baf3-676fce992936/00/10-EXECUTION_SUMMARY.md` (§Steps Executed). Corregirlas es trabajo del dueño de `plans/`, fuera del alcance del plan 19 (§Fuera de alcance: "se mide el protocolo, no el artefacto").
