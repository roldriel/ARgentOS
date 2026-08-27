# RFC-42 — Gobernanza de status entre RFCs y planes de implementación

**Status:** Accepted (2026-08-12, revisión individual RFC-56; evidencia en su plan asociado)
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.9
**Pregunta:** ¿Qué relación de status habilita a un plan a modificar `.agents/` cuando su RFC asociada sigue en `Proposal`?
**Afectados:** `plans/INDEX.md`, `.agents/orchestrators/core/roles/orchestrator.md`, `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`.

## Problema

`plans/INDEX.md` declara que una RFC en `Proposal` NO habilita tocar `.agents/` (`plans/INDEX.md:Convenciones`), pero los planes 23-27 figuran `Executed` y modificaron `.agents/` (task profiles, hook enforcement, required_sections) mientras sus RFCs homólogas 24-28 siguen en `Proposal` (`plans/INDEX.md:Serie de RFCs (documentos canónicos)`). Queda sin documentar qué autoridad habilitó esos cambios, lo que deja una ambigüedad de gobernanza real.

## Decisión propuesta

1. Definir dos vías explícitas para tocar `.agents/`:
   - **Vía RFC**: una RFC `Accepted` habilita los cambios que declara.
   - **Vía plan**: un plan `Aprobado para ejecución` con justificación documentada habilita cambios cuando la RFC asociada no existe o sigue en `Proposal`; la justificación se registra en el plan y en `CHANGELOG.md`.
2. Regularizar el backlog: las RFC-24-28 pasan a `Accepted` si los planes 23-27 fueron aprobados formalmente, o los planes se marcan `Executed (parcial: gobernanza pendiente)` mientras las RFCs no se acepten; la decisión se registra en `plans/INDEX.md`.
3. La serie nueva (RFC-29-54, planes 28-53) se rige por la regla: ningún cambio de `.agents/` se ejecuta antes de que su RFC esté `Accepted` o su plan esté `Aprobado para ejecución` con justificación.

## Alternativas consideradas

- **Forzar RFC Accepted siempre**: bloquea cambios urgentes sin RFC; la vía plan cubre ese caso con registro.
- **Ignorar el desfase**: deja la ambigüedad y debilita la inmutabilidad declarada.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `plans/INDEX.md` | Regla de gobernanza y regularización del backlog 23-28. |
| `ANTI_CIRCUMVENTION.md` | Referencia a las dos vías de autorización. |

## Criterios de aceptación

- [ ] Toda modificación de `.agents/` tiene una vía de autorización documentada.
- [ ] El desfase RFC-24-28 vs planes 23-27 queda regularizado o explícitamente pendiente.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.9 |
| 2026-08-11 | Aplicación parcial por decisión del usuario: regularización retroactiva de RFC-24…28 (`Accepted`) y regla de gobernanza documentada en `plans/INDEX.md`; pendiente la referencia en `ANTI_CIRCUMVENTION.md` hasta la aceptación de esta RFC. | Decisión del usuario (2026-08-11) sobre el plan 41 |
| 2026-08-12 | Accepted (revisión individual, RFC-56/plan 57): la regla de dos vías quedó vigente y referenciada en el payload (plan 56, 3.0.7). Nota: RFC-56 la refina — agrega la Clase C y formaliza las clases A/B/C; no la desfasa. | Revisión de la serie Proposal (RFC-56) |
