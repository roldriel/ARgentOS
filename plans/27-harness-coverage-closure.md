# Plan 27 — Harness Coverage Closure

**Status:** Executed (ver §Cierre)

**Depends on:** Plan 24 (el runner ya parsea contratos para `required_sections`; leer `enforcement` del mismo parseo es incremental).

**Referencia:** `plans/rfc/28-harness-coverage-closure-model.md` (Proposal); evidencia: 13 de 25 contratos sin policy; precedente semántico: `tools/check_plan_citations.py`.

---

# Objetivo

Cerrar la cobertura del harness: declaración `enforcement: gated|informational` obligatoria en los 25 contratos, decisión explícita para los 13 sin policy, y primera capa de validación semántica mecánica (citas que existen, evidencia de tests) en el runner.

---

# Contenido

## A. Declaración de enforcement en contratos

- Agregar front matter `enforcement: gated|informational` (+ `gated_by: H-NN` cuando aplica) a los 25 contratos (`.agents/contracts/` ×7, `orchestrators/core/contracts/` ×10, `orchestrators/discovery/contracts/` ×8).
- Decisión por cada uno de los 13 sin policy actual (HARNESS_REPORT, SESSION_LOG, METRICS, KNOWLEDGE_INDEX, SESSION_BRIEF, PROJECT_README, REVIEW_REPORT, API_SURFACE, DEVELOPMENT_PATTERNS, DISCOVERY_MANIFEST, ENVIRONMENT_DISCOVERY, EXECUTIVE_SUMMARY, INTER_WORKER_MESSAGE): ¿policy nueva o `informational`? Registrar la tabla de decisión en este plan.
- Para los que resulten `gated`: crear la policy correspondiente (siguiendo el formato H0X existente, con decision tree TOML).

## B. Checks semánticos mecánicos en el runner

- **Citation resolution:** migrar la lógica de `tools/check_plan_citations.py` al runner (`runner_validators.py` o módulo nuevo): todo path citado en un artefacto gated se resuelve contra el filesystem; cita rota → FAIL con lista exacta. Activado en las policies de artefactos que citan archivos (TASK_ANALYSIS, EXECUTION_PLAN, VERIFICATION_REPORT, CONTEXT_ARTIFACT).
- **Test evidence (H10):** todo comando de test declarado en VERIFICATION_REPORT debe tener evidencia referenciada y existente (archivo de resultados o entrada de SESSION_LOG); comando sin evidencia → FAIL.
- Ambos checks deterministas, sin LLM, con razón de FAIL accionable.

## C. Invariante de cobertura en la suite

- Test nuevo del harness: todo contrato declara `enforcement`; todo `gated` tiene policy que lo cita y toda policy cita un contrato `gated` (correspondencia bidireccional). Un contrato nuevo sin declaración rompe el build.

## D. Verificación

- Suite completa verde con los tests nuevos.
- Dogfooding negativo: un VERIFICATION_REPORT que declara tests sin evidencia falla H10 con la razón exacta; un artefacto con path fantasma falla su gate.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Tabla de decisión de los 13 contratos | este plan, §Cierre |
| 2 | Front matter `enforcement` en 25 contratos | `.agents/**/contracts/` |
| 3 | Policies nuevas para los `gated` resultantes | `.agents/harness/policies/` |
| 4 | Checks citation resolution + test evidence | `.agents/harness/runner_validators.py` |
| 5 | Invariante de cobertura en suite | `.agents/harness/tests/` |

# Fuera de alcance

- Checks semánticos por LLM en el gate (quedan `[agent]`; mecanización vía hooks: Future Extension de RFC-27).
- Más checks mecánicos (IDs entre iteraciones, TTL de discovery KB): Future Extensions de RFC-28.
- Formato machine-readable de resultados de tests (Future Extension de RFC-28).

---

# Cierre

**Status:** Executed (2026-08-06)

## Tabla de decisión: los 13 contratos sin policy

Criterio aplicado: `gated` solo si existe una transición real del workflow cuya salida exija el artefacto validado por un gate; los artefactos de registro, trazabilidad o insumos intermedios son `informational` (destino legítimo y final, RFC-28 §Definitions).

| Contrato | Decisión | Justificación |
| --- | --- | --- |
| HARNESS_REPORT | informational | Lo escribe el propio runner como salida de cada gate; gatearlo sería circular. |
| SESSION_LOG | informational | Log de auditoría continuo en todos los estados; ninguna transición lo exige validado. |
| METRICS | informational | Agregado de observabilidad; consumo humano/análisis. |
| KNOWLEDGE_INDEX | informational | Artefacto de bootstrap del system agent; S00 gatea el health-check, no el índice. |
| SESSION_BRIEF | informational | Briefing de reanudación para el orquestador; sin transición asociada. |
| PROJECT_README | informational | Documento de bootstrap. |
| REVIEW_REPORT | informational | Salida opcional del perfil `complex`; ningún módulo de workflow lo produce ni lo gatea (solo se menciona en `00-analyze-task.md`). |
| API_SURFACE | informational | Salida parcial de worker de discovery (`harness: []` en su módulo); alimenta el merge. |
| DEVELOPMENT_PATTERNS | informational | Ídem. |
| ENVIRONMENT_DISCOVERY | informational | Ídem. |
| INTER_WORKER_MESSAGE | informational | Formato de mensajería entre workers, no artefacto de fase. |
| DISCOVERY_MANIFEST | informational | Insumo de `DISCOVERY_VALIDATE`, cuyo gate D01 valida las KB entries y el ground truth del output; el merge (`harness: []`) no tiene transición gateada propia. |
| EXECUTIVE_SUMMARY | informational | Síntesis para consumo humano. |

Resultado: 0 policies nuevas. Los 12 contratos restantes quedaron `gated` con `gated_by` apuntando a sus policies reales (VERIFICATION_REPORT → `["H06", "H07"]`).

## Checks semánticos implementados

- **`runner_citations.py`** (módulo nuevo): `citation_resolution` y `test_evidence`, registrados en `SEMANTIC_VALIDATORS` y activados vía `semantic_checks` en el front matter de H00, H02, H04 (`citation_resolution`) y H06 (ambos). Esta vía se eligió sobre un flag `check_citations = true` nuevo porque reusa el mecanismo existente de `semantic_checks`, que ya falla cerrado ante nombres desconocidos.
- **Citation resolution:** tres formas de cita — `` `path:section` ``, `` `path` §section `` y los campos TOML `specification`/`execution_plan` (los campos de referencia del contrato de VERIFICATION_REPORT). Resolución contra raíz del repo, directorio de sesión y directorios de iteración; placeholders (`<...>`) se omiten. Desviación justificada respecto de `check_plan_citations.py`: los anchors puramente numéricos (referencias de línea, p. ej. archivo.py línea 102) y los anchors en archivos no-Markdown exigen solo existencia del archivo — son referencias de línea legítimas y no verificables mecánicamente; las menciones de paths en backticks sin sección tampoco se verifican (un EXECUTION_PLAN puede nombrar archivos a crear). FAIL lista cada cita rota con línea y razón.
- **Test evidence (H06):** cada entrada `[[test_results]]` con resultado distinto de `SKIPPED` exige evidencia existente: campo `evidence` apuntando a un archivo existente, o el comando exacto registrado en `SESSION_LOG.md`. El texto libre de `details` no cuenta como evidencia (es fabricable). FAIL lista los comandos sin evidencia.
- **Convivencia con `tools/check_plan_citations.py`:** se conserva — su dominio es `plans/`, que no es dominio del harness; el runner no lo invoca y la lógica migrada vive en `runner_citations.py` con las adaptaciones arriba.

## Invariante de cobertura

`.agents/harness/tests/test_enforcement_coverage.py`: todo contrato declara `enforcement` válido; todo `gated` declara `gated_by` no vacío y cada policy citada existe y declara el mismo `artifact =`; toda policy del runner cuyo `artifact` es artefacto de contrato exige coherencia bidireccional. Exentos: policies sin front matter TOML (H13, enforced por suite), sin `artifact` (H15) o cuyo artefacto no es contrato (S00).

## Verificación

- Suite: 450 passed, 2 skipped (`python -m pytest .agents/harness/tests/ runtime/tests/ tools/tests/ -q`).
- Health-check: PASS.
- Tests negativos nuevos (`test_semantic_checks.py`): VERIFICATION_REPORT con comando sin evidencia → FAIL H06 con el comando listado; artefacto con path fantasma → FAIL con la cita exacta (H06 y H02).

## Enforcement hacia adelante

El artefacto histórico `.project/d4ab6a93-…/00/11-VERIFICATION_REPORT.md` no cumple el nuevo check `test_evidence` (sus comandos no tienen campo `evidence` ni entradas en SESSION_LOG.md). No se modificó: el enforcement aplica hacia adelante; los artefactos de sesión históricos quedan como registro del protocolo vigente al momento de producirse.
