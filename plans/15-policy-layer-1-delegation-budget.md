# Plan 15 — Policy Layer I: Delegation Validity + Budget Materialization

**Status:** Aprobado para redacción.

**Depends on:** plan 11 (Delegation Validity Model) y plan 07 (Materialization). Es el primer plan del protocolo que implementa policies concretas: hasta aquí todo fue conceptual.

**Referencia:** `plans/11-delegation-validity-model.md` (Future Extension H15); `plans/rfc/03-context-budget-model.md` (RFC-00YA); `.agents/harness/RUNNER.md`.

---

# Objetivo

Convertir el Delegation Validity Model en una **policy de harness real** (H15) que gatea delegaciones antes de ejecutarlas, y definir la **materialización concreta del Context Budget** para el runtime actual — la primera unidad de Budget del protocolo.

---

# Contenido

## A. Policy H15 — delegation-validity

Implementar en el harness la validación pre-delegation declarada por el plan 11:

1. **Resolubilidad de perfil:** el valor de `profile` existe en `.agents/roles/profiles/`.
2. **Resolubilidad de skills:** cada entrada de `skills` resuelve bajo `.project/skills/` o `.agents/skills/` (precedencia de SKILLS.md).
3. **Existencia de artefactos:** los input artifacts referenciados existen en `.project/<session-uuid>/<iteration>/`.
4. **Coherencia de Budget:** el `context_budget` del payload es coherente con la materialización definida en B.
5. **Return report:** validación estructural del reporte de retorno contra el schema del contrato.
6. **Clasificación de fallos:** cada violación reporta con la clase de la taxonomía del plan 10 (si el plan 10 está cerrado; si no, con las clases provisionales declaradas por el plan 11).
7. Policy file con front matter TOML + checklist + decision tree, siguiendo el formato de H01–H13, y marcado machine/agente por ítem (convención del plan 10).

## B. Budget Materialization (runtime prompt)

- RFC o estándar de runtime que define, para el runtime basado en prompts: la **unidad** del Context Budget (tokens estimados), cómo se **estima** el costo de un candidato, y qué significa el `4000` actual del contrato (¿default? ¿techo? ¿por categoría?).
- Debe respetar RFC-00YA: la unidad pertenece al runtime, el concepto no cambia. Documentar la relación explícitamente (este es el primer ejercicio real de la frontera protocolo/runtime del plan 07).
- Enmendar `WORKER_DELEGATION_CONTRACT.md` si el `4000` cambia de significado.

## C. Verificación

- Tests del runner para H15 (casos válidos, perfil inexistente, skill irresoluble, artefacto faltante).
- Health-check + suite completa en verde.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Policy H15 + decision tree + tests | `.agents/harness/` |
| 2 | Budget Materialization del runtime prompt | `plans/rfc/` o estándar de runtime (decidir) |
| 3 | Contrato de delegación actualizado | `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` |

# Fuera de alcance

- Policies de resolución/compresión de contexto (→ plan 16).
- Validación semántica del contenido de artefactos (H15 valida existencia y schema, no calidad).
