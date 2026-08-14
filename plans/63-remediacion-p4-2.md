# Plan 63 — Remediación P4.2 (mapeo determinista de sesión CLI ↔ protocolo)

**Status:** Executed
**Fecha:** 2026-08-14
**RFC:** —
**Clase:** B (mejora operacional compatible: mapeo determinista de sesión; la
semántica de los gates y el fail-open no cambian)
**Depende de:** plan 60 (contrato de hooks)
**Origen:** `AUDITORIA_SISTEMA.md` P4.2

## Objetivo

Reemplazar la resolución de sesión del hook basada solo en mtime por un mapeo
determinista persistido (`.project/.sessions.json`), con reglas de resolución
documentadas y un subcomando de vinculación explícita en `runner_state.py`.

## Criterio de entrada

- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `hook_gate.py`: resolución por mapeo → directorio exacto → sesión única →
   más reciente (primer evento, con registro del mapeo); escritura
   transaccional best-effort de `.project/.sessions.json`.
2. `runner_state.py`: subcomando `link --cli-session <id>`.
3. `harness/INDEX.md`: reglas de resolución y concurrencia actualizadas.
4. Tests del harness para mapeo y link.
5. `protocol/.agents/VERSION` = `3.14.0`; changelog; INDEX; tracker.

## Pasos

1. Editar `.agents/harness/hook_gate.py` (`_resolve_session` + helpers).
2. Editar `.agents/harness/runner_state.py` (`link_session` + acción `link`).
3. Editar `.agents/harness/INDEX.md` (Hook event schema, reglas de
   resolución).
4. Agregar tests del harness (`test_hook_gate.py`, `test_runner_state.py`).
5. Bump `3.14.0`, changelog, INDEX, tracker.

## Criterios de salida

- [ ] Dos CLI sessions concurrentes resuelven cada una su protocolo session de
      forma determinista tras su primer evento.
- [ ] La vinculación explícita (`runner_state.py link`) está documentada y
      testeada.
- [ ] Batería canónica en verde (incluye los tests del harness).

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/
```

## Riesgos

- Bajo: el mapeo es best-effort (fail-open intacto); la escritura del mapeo no
  bloquea la resolución.

## Trazabilidad

- `AUDITORIA_SISTEMA.md` P4.2.

## Nota de ejecución

Ejecutado el 2026-08-14. Versión `3.14.0` (MINOR: adición operacional
compatible). Verificación: invariantes OK, citas OK, estructura OK, taxonomía
OK, tests del repo OK, 44 tests del harness OK; `check_dist_sync` rojo en
`dev` por diseño.
