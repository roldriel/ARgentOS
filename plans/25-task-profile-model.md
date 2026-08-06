# Plan 25 — Task Profile Model

**Status:** Executed (dogfooding medido pendiente, ver §Status de ejecución)

**Depends on:** Plan 24 recomendado (los decision trees y policies se tocan aquí; conviene hacerlo sobre la fuente única de `required_sections`), no obligatorio.

**Referencia:** `plans/rfc/26-task-profile-model.md` (Proposal); evidencia: sesión de dogfooding `.project/d4ab6a93…/00/` con ~23 archivos, 10 gates, ~52 min para una tarea.

---

# Objetivo

Introducir los perfiles de tarea `trivial` / `standard` / `complex` con asignación en la fase 01 y bifurcación de artefactos y gates por perfil, de modo que una tarea trivial genere ≤ 5 archivos y ≤ 3 gates.

---

# Contenido

## A. Campo de perfil en TASK_ANALYSIS

- Contrato `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`: nueva sección/campo obligatorio `task_profile: trivial|standard|complex` + justificación (criterios objetivos: n° estimado de archivos, ambigüedad, decisiones de diseño, impacto en interfaces).
- Policy H00: validar presencia del perfil y coherencia básica de la justificación (sección requerida nueva; se hereda del contrato si el plan 24 ya está aplicado, o se agrega al TOML si no).

## B. Matriz perfil → ciclo

- Definir en la máquina de estados (`AGENT_STATE_MACHINE.md`) y en `.agents/orchestrators/core/workflow/` el subconjunto obligatorio por perfil, según RFC-26 §Definitions:
  - `trivial`: TASK_ANALYSIS, EXECUTION_PLAN, VERIFICATION_REPORT; gates H00, H05, H10; sin discovery, sin workers de contexto.
  - `standard`: ciclo vigente sin cambios.
  - `complex`: ciclo completo + REVIEW_REPORT + discovery si aplica.
- Regla de escalado solo ascendente + reclasificación ante NEEDS_CLARIFICATION, documentada inline en la máquina de estados (frontera documental: sin mencionar la RFC).

## C. Bifurcación en el runner

- `run_trigger` lee el perfil desde el TASK_ANALYSIS validado (o desde `state.json` si el plan 26 ya existe; si no, del artefacto).
- Gates no obligatorios para el perfil: se registran en `HARNESS_REPORT.md` como `skipped: profile` (cambio pequeño en el reporte del runner + contrato de HARNESS_REPORT).
- Decision trees TOML: agregar la rama de perfil donde corresponda (H00 principalmente; H05/H10 permanecen en todos los perfiles).

## D. Verificación

- Tests nuevos del harness: perfil trivial pasa con solo sus 3 gates; gates omitidos quedan registrados como `skipped: profile`; reclasificación ascendente fuerza artefactos faltantes.
- Dogfooding medido: una tarea trivial real con `METRICS.md` — criterio de éxito: ≤ 5 archivos, ≤ 3 gates, tiempo notablemente menor al baseline de ~52 min.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Campo `task_profile` en contrato + policy H00 | `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`, policy H00 |
| 2 | Matriz perfil → artefactos/gates | `AGENT_STATE_MACHINE.md`, workflow |
| 3 | Bifurcación + registro `skipped: profile` | `runner_validators.py`, contrato HARNESS_REPORT |
| 4 | Tests + dogfooding trivial medido | `.agents/harness/tests/`, `.project/<sesión>/` |

# Status de ejecución

Ejecutado el 2026-08-06 (rama `dev`): entregables 1–3 completos; tests nuevos en `.agents/harness/tests/test_task_profiles.py` (suite 357 passed, 2 skipped; health-check PASS).

**Pendiente:** el dogfooding medido de una tarea trivial (§D, entregable 4 en `.project/<sesión>/`). No se ejecutó en esta pasada porque requiere una sesión de protocolo real con el usuario; queda como verificación diferida con el criterio de éxito de §D (≤ 5 archivos, ≤ 3 gates, tiempo notablemente menor al baseline de ~52 min).

# Fuera de alcance

- Clasificación automática por heurísticas de código (Future Extension de RFC-26).
- Perfiles por tipo de tarea (bugfix/feature).
- Persistencia del perfil en `state.json` (plan 26).
