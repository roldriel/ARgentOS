# RFC-49 — Validación mecánica de skills del protocolo

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 4.4
**Pregunta:** ¿Cómo se garantiza estructuralmente que las skills del protocolo sigan siendo válidas cuando cambian?
**Afectados:** `dev/tools/check_protocol_invariants.py`, `.agents/skills/README.md`, `.agents/standards/runtime/PROTOCOL_HEALTH.md`, `.project/skills/README.md`.

## Problema

La validación estructural de las skills del protocolo no es mecánica: el ítem 7 del health checklist cubre solo `.project/skills/` (`.agents/standards/runtime/PROTOCOL_HEALTH.md:Checklist`), y las skills de `.agents/skills/` dependen del juicio del agente (`.agents/skills/README.md:Enforcement`). La verificación actualmente pasa, pero no hay red de seguridad si un cambio futuro rompe front matter o referencias. Además, `.project/skills/README.md` atribuye la validación estructural a `health_check.py`, que es solo la sonda de almacenamiento de estado (`.project/skills/README.md:Rules`).

## Decisión propuesta

1. Extender `dev/tools/check_protocol_invariants.py` (dev-only, no distribuido) con un invariante de skills: cada `.agents/skills/<name>/SKILL.md` tiene front matter con `name` (igual al directorio) y `description`; `when_to_activate` recomendado; los `references/<file>` citados existen; y el inventario de `skills/INDEX.md` coincide con los directorios.
2. Corregir la atribución en `.project/skills/README.md`: la validación estructural de `.project/skills/` es el ítem 7 del health checklist (juicio del agente), no `health_check.py`.
3. Mantener la naturaleza no bloqueante en runtime: el checker es dev-only; el protocolo sigue evaluando por juicio.

## Alternativas consideradas

- **Dejar el juicio como única validación**: riesgo aceptado hoy, pero sin red de seguridad.
- **Reintroducir un validador en runtime**: contradice la dirección "menos Python" de 2.0.0.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `dev/tools/check_protocol_invariants.py` | Invariante de skills. |
| `.project/skills/README.md` | Atribución corregida. |
| `.agents/skills/README.md` | Nota de verificación dev-only. |

## Criterios de aceptación

- [ ] El checker detecta una skill sin front matter, con `name` incorrecto o con referencia rota.
- [ ] El checker detecta desincronización entre `skills/INDEX.md` y los directorios.
- [ ] `.project/skills/README.md` atribuye la validación al lugar correcto.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 4.4 |
