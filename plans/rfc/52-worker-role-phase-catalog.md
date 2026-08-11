# RFC-52 — Catálogo de fases y skills en los roles de worker

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 6.1
**Pregunta:** ¿El catálogo de roles de fase y sus skills en `worker.md` coincide con el workflow y con la tabla de activación?
**Afectados:** `.agents/roles/worker.md`, `.agents/roles/recovery_analyst.md`, `.agents/skills/INDEX.md`.

## Problema

El catálogo "Phase roles" de `worker.md` enumera las fases 00, 02-08 pero omite la fase 01 (`intent_reflector`, que aparece solo como perfil) (`.agents/roles/worker.md:Roles the Worker Can Adopt`). Además, el rol `recovery_analyst` declara solo `hypothesis-generator` como skill (`.agents/roles/recovery_analyst.md:Skills`), mientras la tabla de activación asigna `hypothesis-generator, risk-detector` a la fase 08 (`.agents/skills/INDEX.md:Activation table`). El catálogo de roles es la fuente que leen los workers para saber qué rol adoptar; la omisión y el desfase de skills generan delegaciones incompletas.

## Decisión propuesta

1. `worker.md` agrega la fase 01 a "Phase roles", con la nota de que `intent_reflector` es un perfil de fase (no un rol de archivo).
2. `recovery_analyst.md` alinea su lista de skills con la tabla de activación (`hypothesis-generator`, `risk-detector`).
3. Verificación transversal: la sección `Skills` de cada rol de fase coincide con la fila correspondiente de la tabla de activación.

## Alternativas consideradas

- **Dejar el catálogo como está**: las delegaciones de fase 01 quedarían sin documentación en `worker.md`.
- **Quitar `risk-detector` de la tabla**: pierde una skill relevante para recovery.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `worker.md` | Fase 01 en el catálogo. |
| `recovery_analyst.md` | Skills alineadas. |
| `skills/INDEX.md` | Sin cambio (fuente de verdad de la tabla). |

## Criterios de aceptación

- [ ] El catálogo de `worker.md` cubre las 9 fases.
- [ ] Cada rol de fase lista exactamente las skills de su fila en la tabla de activación.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 6.1 |
