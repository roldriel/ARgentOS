# RFC-29 — H07: Trabajo extra autorizado por el usuario

**Status:** Accepted
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.1
**Pregunta:** ¿Cómo expresa el protocolo el trabajo extra explícitamente autorizado por el usuario sin que la verificación de alcance lo convierta en un fallo?
**Afectados:** `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`, `.agents/orchestrators/core/harness/policies/H07-scope-compliance.md`, `.agents/standards/quality/RUBRICS.md`, `.agents/orchestrators/core/roles/orchestrator.md`.

## Problema

El contrato `VERIFICATION_REPORT.md` define `user_authorized_extra_work` como un campo cuyo propósito es registrar aprobación escrita del usuario para trabajo fuera del plan (`.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md:Scope Compliance`). Sin embargo, la policy H07 exige, para que el gate pase, que `scope_respected` sea `true`, que `unplanned_changes` esté vacío y que `user_authorized_extra_work` sea `false` (`.agents/orchestrators/core/harness/policies/H07-scope-compliance.md:Gate Checklist`).

Consecuencia: una sesión en la que el usuario autorizó por escrito trabajo adicional **no puede pasar H07 por diseño**, aunque el campo exista exactamente para documentar esa situación. La rúbrica agrava la contradicción: el nivel `EXCEEDS` del criterio Scope Compliance de `VERIFICATION_REPORT_RUBRIC` premia "verificar autorización explícita para cualquier trabajo extra" (`.agents/standards/quality/RUBRICS.md:6. VERIFICATION_REPORT_RUBRIC`). El contrato, la policy y la rúbrica dicen cosas incompatibles.

La fricción es estructural, no de redacción: el modelo de scope compliance trata "trabajo fuera del plan" y "trabajo autorizado" como una misma condición, cuando son dos conceptos ortogonales.

## Decisión propuesta

Separar dos conceptos en el modelo de scope compliance:

1. **`scope_respected`**: el trabajo ejecutado está dentro de la tarea asignada, donde la tarea incluye las ampliaciones que el usuario autorizó explícitamente por escrito durante la sesión. `scope_respected = false` es fallo de alcance en ambas ramas.
2. **`user_authorized_extra_work`**: existe trabajo fuera del plan aprobado que el usuario autorizó explícitamente por escrito durante la sesión.
3. **`unplanned_changes`**: lista todo cambio fuera del plan aprobado (autorizado o no); vacío en Rama A, lista los cambios en Rama B.

El gate H07 pasa cuando se cumple una de dos ramas:

- **Rama A (sin extra)**: `scope_respected = true`, `unplanned_changes = []`, `user_authorized_extra_work = false`.
- **Rama B (extra autorizado)**: `scope_respected = true`, `unplanned_changes` lista los cambios, `user_authorized_extra_work = true`, y la autorización escrita está evidenciada en `SESSION_LOG.md` o en un artefacto de la sesión y citada en el reporte. La evidencia la juzga el Orchestrator al evaluar H07, pudiendo activar la skill `decision-extractor` para recuperar la decisión confirmada del usuario; el verifier la declara en el reporte.

La Rama B elimina la imposibilidad actual sin abrir la puerta al trabajo no autorizado: sin evidencia escrita no hay Rama B. La coherencia exige actualizar también la sección `Decision Criteria` de H07 (hoy exige "no unplanned changes are reported"), no solo la Checklist y el Gate Checklist.

## Alternativas consideradas

- **Eliminar el campo `user_authorized_extra_work`**: pierde trazabilidad; la rúbrica y el propio contrato lo exigen para registrar aprobaciones.
- **Hacer H07 informativo**: degrada la única gate de alcance del protocolo.
- **Tratar el extra autorizado como una enmienda del plan**: válido cuando la autorización precede a la ejecución, pero no cubre autorizaciones durante la ejecución.

Se adopta la Rama B porque conserva la gate, mantiene el registro y resuelve la contradicción con la rúbrica.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `VERIFICATION_REPORT.md` | Reescribir la semántica de `Scope Compliance` para las dos ramas. |
| `H07-scope-compliance.md` | Checklist (ítems 3, 5-6), `Decision Criteria` y Gate Checklist (ítems 4-5): aceptar Rama B con evidencia; ninguna sección exige `unplanned_changes = []` ni `user_authorized_extra_work = false` incondicionalmente. |
| `RUBRICS.md` | Alinear el criterio Scope Compliance con las dos ramas. |
| `orchestrator.md` | Instrucción de validación de evidencia escrita en la Rama B. |

## Criterios de aceptación

- [ ] Un `VERIFICATION_REPORT.md` con `user_authorized_extra_work = true` y evidencia puede pasar H07.
- [ ] Un `VERIFICATION_REPORT.md` con trabajo no autorizado sigue fallando H07.
- [ ] La rúbrica y el contrato describen las mismas dos ramas.
- [ ] H07 no exige `unplanned_changes = []` ni `user_authorized_extra_work = false` incondicionalmente en ninguna sección.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 1.1 |
| 2026-08-11 | Correcciones de auditoría: semántica de `scope_respected`/`unplanned_changes` para la Rama B, H07 `Decision Criteria`, rol de `decision-extractor` (Orchestrator) | Auditoría de planes 28-30 |
| 2026-08-11 | Aceptada (Accepted): implementación del plan 28 autorizada explícitamente por el usuario | Plan 28 Executed |
