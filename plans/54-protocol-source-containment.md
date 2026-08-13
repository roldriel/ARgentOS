# Plan 54 — Source containment: protocol payload in `protocol/`

**Status:** Executed (2026-08-12).

**RFC:** RFC-55 (`plans/rfc/55-protocol-source-containment.md`).

**Criterio de entrada:** autorización explícita del usuario (2026-08-12) y
checkers verdes al inicio.

## Objetivo

Contener el payload del protocolo en `protocol/` para que el repo fuente sea un
workspace de desarrollo (con `AGENTS.md` dev propio), sin cambiar el producto
distribuido en `dist`.

## Entregables

1. Move: `.agents/` → `protocol/.agents/`; `AGENTS.md` → `protocol/_AGENTS.md`.
2. Nuevo `AGENTS.md` raíz (dev): propósito, regla "protocol/ es data",
   workflow y verificación.
3. Tooling: `check_protocol_invariants.py` con `--payload protocol`, mapeo del
   entry file (`AGENTS.md` → `_AGENTS.md`) y tests; `check_plan_citations.py`
   con mapeo legacy (`.agents/...` → `protocol/.agents/...`) y tests; paths del
   runtime y tests del harness.
4. CI: `publish-dist.yml` (fuente `protocol/`, rename al publicar) y
   `check-protocol.yml` (paths y triggers).
5. Docs raíz: `README.md`, `VERSIONING.md`, `CHANGELOG.md` (entrada 3.0.5),
   `ADOPTION.md` (nota), `plans/INDEX.md`, bump de `protocol/.agents/VERSION`.
6. Consolidación dev: `dev/README.md` (índice), `dev/ROADMAP.md` (cobertura vs
   `plans/INDEX.md`), `dev/source-layout.md` (links rotos intencionales).
7. Limpieza: `.project/` (rescate opcional de KB, luego borrado) y caches.

## Verificación

- `python dev/tools/check_protocol_invariants.py --payload protocol .` → OK.
- `python dev/tools/check_plan_citations.py` → OK.
- `python -m pytest protocol/.agents/harness/tests/ dev/runtime/tests/ dev/tools/tests/` → OK.
- Build manual de `dist` en temp: layout `.agents/` + `AGENTS.md`; checksum de
  `AGENTS.md` == `protocol/_AGENTS.md`.
- Smoke de adopción en repo temp.

## Nota de ejecución

- Move y renombrado completados con renames registrados por git.
- Checkers: invariantes OK (186 archivos, 7268 referencias) y citas OK
  (`.project/` eximido por efimeridad, ver RFC 49/50/51).
- Tests: 105 passed (harness, runtime, tools).
- Build de `dist` en temp: layout `.agents/` + `AGENTS.md`; checksum del entry
  publicado == `protocol/_AGENTS.md`.
- KB de `.project/` respaldada en TEMP antes del borrado.
- Promoción a `master` + tags + `publish-dist` pendientes de autorización del
  usuario (VERSIONING §7/§9; regularización 3.0.2–3.0.4 pendiente).
- Cierre (2026-08-12): promoción, tags 3.0.2–3.0.5 y regeneración de `dist`
  ejecutados; registro en `VERSIONING.md` §9.
