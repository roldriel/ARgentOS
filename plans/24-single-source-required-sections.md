# Plan 24 — Single-Source Required-Sections

**Status:** Proposed

**Depends on:** — (ninguno). Convive con cualquier orden respecto de los planes 23/25/26/27.

**Referencia:** `plans/rfc/25-single-source-required-sections.md` (Proposal); mecanismo actual verificado: `runner_policies.py:18` (parseo de front matter), `runner_validators.py:904-979` (`run_trigger` → `load_policy` → `validate_sections`); duplicación verbatim en 15 de 16 policies.

---

# Objetivo

Hacer que el runner derive `required_sections` del contrato citado por la policy (`artifact = "..."`), eliminando la copia TOML en las policies y el script `sync_required_sections.py`, sin cambiar el comportamiento observable de ningún gate.

---

# Contenido

## A. Pre-migración (línea base)

- Ejecutar `python .agents/harness/sync_required_sections.py --check` y confirmar drift cero (o sincronizar primero): la migración solo es inocua si las copias actuales reflejan los contratos.
- Suite verde antes de tocar nada: `python -m pytest .agents/harness/tests`.

## B. Resolución por referencia en el runner

- En `runner_policies.py`: nueva función `resolve_required_sections(policy)` que, dado `artifact = "X"` de la policy, localiza el contrato correspondiente (`.agents/orchestrators/*/contracts/X.md`, `.agents/contracts/X.md`), parsea sus encabezados `##` y devuelve la lista, excluyendo una lista única de secciones no normativas definida en ese módulo (`## Purpose`, según la convención vigente verificada en H00).
- Fail-closed: contrato inexistente o sin secciones parseables → error explícito de policy malformada (misma clase que un TOML inválido hoy).
- En `runner_validators.py` (`run_trigger`, ~línea 944): reemplazar `policy.get("required_sections", [])` por la resolución por referencia.

## C. Limpieza

- Quitar la clave `required_sections` del front matter TOML de las 15 policies que la declaran (H13 no la tiene: sin cambio).
- Eliminar `.agents/harness/sync_required_sections.py` y su test.
- Actualizar la prosa de las policies y de `.agents/harness/INDEX.md` donde se describa la sincronización manual.

## D. Tests

- Ajustar los tests que construyen policies con `required_sections` inline para que usen contratos de fixture.
- Test nuevo: la resolución falla cerrado ante contrato ausente.
- Test nuevo de paridad (transitorio, puede borrarse después): para cada policy real, la lista resuelta por referencia es idéntica a la copia TOML pre-migración (snapshot capturado en §A).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Resolución por referencia | `.agents/harness/runner_policies.py`, `runner_validators.py` |
| 2 | Policies sin `required_sections` | `.agents/harness/policies/` |
| 3 | Eliminación de sync script + test | `.agents/harness/` |
| 4 | Suite verde (354+ tests) | — |

# Fuera de alcance

- Cambios en el contenido o lista de secciones de los contratos.
- Derivación por referencia de otras claves TOML (scope, decision trees).
- Validación semántica de secciones (plan 27 / RFC-28).
