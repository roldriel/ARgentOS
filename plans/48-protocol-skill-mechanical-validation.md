# Plan 48 — Validación mecánica de skills del protocolo

**Status:** Aprobado para redacción
**Fecha:** 2026-08-11
**RFC:** RFC-49 (`plans/rfc/49-protocol-skill-mechanical-validation.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 4.4

## Objetivo

Agregar verificación mecánica dev-only de las skills del protocolo y corregir la atribución de validación en `.project/skills/README.md`.

## Criterio de entrada

- [ ] RFC-49 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: estado actual del checker y del README de skills.

## Entregables

1. Invariante de skills en `dev/tools/check_protocol_invariants.py`.
2. Tests del invariante en `dev/tools/tests/`.
3. `.project/skills/README.md` con atribución corregida.
4. Nota en `.agents/skills/README.md`.

## Pasos

1. Implementar el invariante (front matter, `name` == directorio, referencias citadas, inventario INDEX ↔ directorios).
2. Agregar casos de test (skill inválida, referencia rota, INDEX desincronizado).
3. Corregir `.project/skills/README.md` (ítem 7 del health checklist).
4. Actualizar `.agents/skills/README.md` (verificación dev-only).
5. Ejecutar `python dev/tools/check_protocol_invariants.py .` y `python -m pytest dev/tools/tests/`.

## Criterios de salida

- [ ] El invariante detecta cada clase de fallo diseñada.
- [ ] La suite de tests pasa.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Prueba negativa manual: romper temporalmente una skill en una copia y confirmar la detección.

## Riesgos

- Bajo: cambio dev-only; el runtime no cambia.

## Trazabilidad

- RFC-49; punto 4.4 de la auditoría.
