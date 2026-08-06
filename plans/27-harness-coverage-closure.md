# Plan 27 — Harness Coverage Closure

**Status:** Proposed

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
