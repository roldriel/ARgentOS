# Plan 11 — Delegation Validity Model

**Status:** Aprobado para redacción.

**Depends on:** planes 04–07 (consume los conceptos de Context Budget, candidates y materialización de la serie de Execution Context).

**Referencia:** análisis de explicitud (gap 2); `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`; `plans/rfc/03-context-budget-model.md` (RFC-00YA).

---

# Objetivo

Definir conceptualmente qué hace **válida** una delegación más allá del schema del payload — y qué hace válido un return report — de modo que exista un gate conceptual entre "payload bien formado" y "payload ejecutable".

---

# Contenido

## A. RFC — Delegation Validity Model

- **Pregunta que responde:** ¿Qué condiciones conceptuales debe cumplir una delegación para ser válida?
- **Condiciones a modelar** (hoy ninguna tiene gate):
  1. **Resolubilidad de perfil:** el valor de `profile` debe ser resoluble en el catálogo de `.agents/roles/profiles/`.
  2. **Resolubilidad de skills:** cada entrada de `skills` debe ser resoluble bajo `.project/skills/` o `.agents/skills/` (precedencia ya definida en SKILLS.md).
  3. **Coherencia de Budget:** el `context_budget` del payload debe ser coherente con el modelo de Context Budget (RFC-00YA). **Caso concreto a resolver:** el contrato hardcodea `context_budget: 4000`, pero RFC-00YA define el Budget sin unidades ni límites — hoy es un huérfano sin modelo. La RFC debe decidir conceptualmente qué es ese número (¿una materialización del Budget por el runtime actual? ¿una policy?) y dejar la relación explícita.
  4. **Existencia de artefactos:** los input artifacts referenciados deben existir en la sesión.
  5. **Return report:** validez conceptual del reporte de retorno (schema + clases de la taxonomía del plan 10 si ya existe).
- **Gate conceptual:** definir el punto del flujo donde la validez se evalúa (pre-delegation, pre-execution, post-return) y qué clase de fallo genera cada violación (consume la taxonomía del plan 10 si está disponible; si no, dejar el hook declarado).

## B. Aplicación

- Enmendar `WORKER_DELEGATION_CONTRACT.md`: reemplazar el `4000` hardcodeado por la referencia conceptual decidida en A.3.
- Declarar la futura policy de harness (p. ej. H15) como Future Extension; **no** implementarla en este plan.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Delegation Validity Model | `plans/rfc/` (número libre) |
| 2 | Contrato de delegación enmendado (budget) | `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` |

# Fuera de alcance

- Implementación de la policy de validación en el runner.
- Modelos de selección de perfil/skill (→ plan 12): este plan define qué hace *válida* una selección ya hecha, no cómo se elige.
