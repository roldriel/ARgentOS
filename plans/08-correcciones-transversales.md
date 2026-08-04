# Plan 08 — Correcciones Transversales de `.agents/`

**Status:** Aprobado para ejecución. Independiente; puede ejecutarse **ya, en paralelo** a los planes 04–07 (no toca ningún documento del roadmap de Execution Context).

**Depends on:** — (ninguno).

**Referencia:** `plans/analisis-explicitud.md` (gaps 6 y 9).

---

# Objetivo

Eliminar las contradicciones y elementos stale detectados en `.agents/` que no requieren una serie conceptual: son fixes documentales acotados. Toda modificación de `.agents/` queda cubierta por este plan como acuerdo explícito documentado (política de inmutabilidad, `PROTOCOL_BOUNDARIES.md`).

---

# Alcance

## A. Contradicción de bootstrap (la única con impacto normativo)

- `orchestrators/system/states/SYSTEM_STATE_MACHINE.md` (regla de `BOOTSTRAP_FAILED`) y la policy S00 **prohíben** entregar control al orchestrator con health-check en FAIL.
- `orchestrators/system/workflow/00-bootstrap.md` repite la misma prohibición (paso 5: "stop"; estado `BOOTSTRAP_FAILED`: "Do not hand control to the core Orchestrator").
- `orchestrators/core/roles/orchestrator.md` (§"1. Session Management") permite **continuar con autorización explícita del usuario** (loggeada como warning).

**Decisión recomendada:** la regla canónica se define en un único documento (`orchestrators/system/states/SYSTEM_STATE_MACHINE.md`, regla de `BOOTSTRAP_FAILED`): "FAIL bloquea el handoff; la única excepción es autorización explícita del usuario, registrada en `SESSION_LOG.md`". S00, `00-bootstrap.md` y `orchestrator.md` la referencian con esa misma formulación, sin reformularla (single-source, `standards/runtime/PROTOCOL_BOUNDARIES.md` §"Single-source documentation policy"). La modelización conceptual del "bootstrap degradado" queda para el plan 09 — aquí solo se elimina la contradicción textual.

## B. Fixes stale

1. `orchestrators/core/workflow/INDEX.md` fase 03: la nota de rol ("`context_gatherer` (o `context_discoverer` si `knowledge_base` está habilitado)") contradice `orchestrator.md` §4.2, donde el discoverer es un worker *pre-delegation* y el `context_gatherer` sigue ejecutando la fase. Alinear la nota con §4.2.
2. `orchestrators/core/roles/orchestrator.md`: la sección "### 7. Scope and Autonomy Enforcement" queda separada de las secciones 1–6 por el H2 "## Recovery decision tree mapping" intercalado. Reubicar ese H2 (p. ej. como subsección de "### 6. Decision Making", cuyo contenido complementa) para que la numeración de responsabilidades sea continua.
3. `orchestrators/discovery/roles/`: la lista de scopes del rol omite `init_worker`/`synthesis_worker` que sí figuran en `DISCOVERY_STATE_MACHINE.md`. La state machine es canónica; corregir el rol.
4. `roles/profiles/README.md`: el catálogo ya lista los ocho perfiles, pero no distingue conceptualmente los perfiles de ingeniería (seleccionables vía ORCHESTRATION_GUIDE) de los de fase fija. Agregar una columna o nota que marque `intent_reflector` e `intent_reflection_reviewer` como perfiles de fase fija (fase 01), no seleccionables por ORCHESTRATION_GUIDE.
5. Doble significado de "profile" (front-matter de fase vs. campo del payload): la nota existe en el contrato; agregar cross-reference desde `roles/profiles/README.md`.

## C. Verificación

```bash
python .agents/harness/runner.py health-check
python -m pytest .agents/harness/tests/ -q
```

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Regla canónica de bootstrap degradado aplicada | `orchestrators/system/` (state machine + policy S00 + workflow `00-bootstrap.md`) |
| 2 | Fixes B.1–B.5 aplicados | archivos existentes listados |

# Fuera de alcance

- Modelización conceptual de decisiones, bootstrap o confianza (→ plan 09).
- Cualquier cambio de comportamiento del runtime, contratos o state machines más allá de la enmienda A.
- Roadmap de Execution Context (planes 04–07).
