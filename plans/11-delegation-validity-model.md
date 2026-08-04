# Plan 11 — Delegation Validity Model

**Status:** Aprobado para redacción.

**Depends on:** nada estructural (el caso concreto se apoya en RFC-00YA, ya existente, y en definiciones inline ya presentes en `orchestrator.md` §"5. Worker Delegation"); se recomienda ejecutar después de 04–07 por terminología. Dependencia blanda del plan 10 (ver A.5 y el gate conceptual).

**Referencia:** `plans/analisis-explicitud.md` (gap 2); `.agents/orchestrators/core/contracts/WORKER_DELEGATION_CONTRACT.md`; `plans/rfc/03-context-budget-model.md` (RFC-00YA).

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
  5. **Return report:** validez conceptual del reporte de retorno (schema + hook a la taxonomía de fallos: la clase de fallo se declara como placeholder `FAILURE_CLASS_TBD`, que el plan 10 —o el 15— reemplaza al cerrarse).
- **Gate conceptual:** definir el punto del flujo donde la validez se evalúa (pre-delegation, pre-execution, post-return) y qué clase de fallo genera cada violación (mismo hook determinista: placeholder `FAILURE_CLASS_TBD`, sin doble forma del entregable).

## B. Aplicación

- Enmendar `WORKER_DELEGATION_CONTRACT.md`: reemplazar el `4000` hardcodeado por la referencia conceptual decidida en A.3.
- Declarar la futura policy de harness como Future Extension; **no** implementarla en este plan. La próxima policy se numera H15 (asignada al plan 15); H14 queda sin asignar y su omisión debe documentarse en `.agents/harness/INDEX.md` junto a H08/H12 al crear H15.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Delegation Validity Model | `plans/rfc/` (a partir de `rfc/16`) |
| 2 | Contrato de delegación enmendado (budget) | `.agents/orchestrators/core/contracts/WORKER_DELEGATION_CONTRACT.md` |

# Fuera de alcance

- Implementación de la policy de validación en el runner.
- Modelos de selección de perfil/skill (→ plan 12): este plan define qué hace *válida* una selección ya hecha, no cómo se elige.
