# RFC-43 — Limpieza de la regla de entidades `planned` en H13

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.10
**Pregunta:** ¿Qué tratamiento reciben las entidades marcadas `status: planned` en la taxonomía cuando ya no existen?
**Afectados:** `.agents/harness/policies/H13-protocol-taxonomy.md`, `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`.

## Problema

La regla 9 de H13 describe el tratamiento de entidades `status: planned` citando como ejemplo `D01-discovery-output` y los roles/workers de discovery (`.agents/harness/policies/H13-protocol-taxonomy.md:Rules`). El diccionario maestro ya no contiene ninguna entidad con `status: planned`: la verificación mecánica de la taxonomía no encontró ninguna, y todos los archivos de discovery existen. La regla es código muerto que sugiere un estado del protocolo que no existe.

## Decisión propuesta

1. Eliminar la regla 9 de H13 o convertirla en una nota histórica: "las entidades `planned` fueron un mecanismo de rollout de discovery; hoy no existen; si se reintroduce, la regla se restaura".
2. Verificar que `PROTOCOL_TAXONOMY.md` no tenga referencias residuales al mecanismo `planned` fuera de esa nota.

## Alternativas consideradas

- **Mantener la regla**: conserva texto muerto que un auditor puede interpretar como un estado vigente.
- **Mantenerla como nota histórica**: preserva el contexto sin sugerir estado vigente; se adopta.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `H13-protocol-taxonomy.md` | Regla 9 convertida en nota histórica. |
| `PROTOCOL_TAXONOMY.md` | Verificación de ausencia de `planned`. |

## Criterios de aceptación

- [ ] Ninguna regla vigente de H13 presupone entidades `planned`.
- [ ] El diccionario maestro no declara entidades `planned`.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.10 |
