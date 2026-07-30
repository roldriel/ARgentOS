# Plan 08 — Correcciones Transversales de `.agents/`

**Status:** Aprobado para ejecución. Independiente; puede ejecutarse **ya, en paralelo** a los planes 04–07 (no toca ningún documento del roadmap de Execution Context).

**Depends on:** — (ninguno).

**Referencia:** análisis de explicitud del protocolo (gaps 6 y 9).

---

# Objetivo

Eliminar las contradicciones y elementos stale detectados en `.agents/` que no requieren una serie conceptual: son fixes documentales acotados. Toda modificación de `.agents/` queda cubierta por este plan como acuerdo explícito documentado (política de inmutabilidad, `PROTOCOL_BOUNDARIES.md`).

---

# Alcance

## A. Contradicción de bootstrap (la única con impacto normativo)

- `orchestrators/system/states/SYSTEM_STATE_MACHINE.md` y la policy S00 **prohíben** entregar control al orchestrator con health-check en FAIL.
- `orchestrators/core/roles/orchestrator.md` §1 permite **continuar con autorización explícita del usuario** (loggeada como warning).

**Decisión recomendada:** la regla canónica es "FAIL bloquea el handoff; la única excepción es autorización explícita del usuario, registrada en `SESSION_LOG.md`". Aplicarla enmendando los documentos de system para admitir la excepción (es la regla que ya se practica). La modelización conceptual del "bootstrap degradado" queda para el plan 09 — aquí solo se elimina la contradicción textual.

## B. Fixes stale

1. `orchestrators/core/workflow/INDEX.md` fase 03: la nota de rol ("`context_gatherer` (o `context_discoverer` si `knowledge_base` está habilitado)") contradice `orchestrator.md` §4.2, donde el discoverer es un worker *pre-delegation* y el `context_gatherer` sigue ejecutando la fase. Alinear la nota con §4.2.
2. `orchestrators/core/roles/orchestrator.md`: dos secciones numeradas "4" (Feature Flag Awareness y la de 4.1/4.2/4.3). Renumerar.
3. `orchestrators/discovery/roles/`: la lista de scopes del rol omite `init_worker`/`synthesis_worker` que sí figuran en `DISCOVERY_STATE_MACHINE.md`. La state machine es canónica; corregir el rol.
4. `roles/profiles/README.md`: el catálogo lista 6 perfiles de ingeniería pero el directorio incluye `intent_reflector` e `intent_reflection_reviewer` (perfiles de fase fija). Explicitar la distinción en el catálogo.
5. Doble significado de "profile" (front-matter de fase vs. campo del payload): la nota existe en el contrato; agregar cross-reference desde `roles/profiles/README.md`.

## C. Verificación

```bash
python .agents/harness/runner.py health-check
python -m pytest .agents/harness/tests/ -q
```

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Regla canónica de bootstrap degradado aplicada | `orchestrators/system/` (state machine + policy S00) |
| 2 | Fixes B.1–B.5 aplicados | archivos existentes listados |

# Fuera de alcance

- Modelización conceptual de decisiones, bootstrap o confianza (→ plan 09).
- Cualquier cambio de comportamiento del runtime, contratos o state machines más allá de la enmienda A.
- Roadmap de Execution Context (planes 04–07).
