# Plan 85 — Corrección de la guía de adopción: sin `git subtree --prefix=.`

**Status:** Executed
**Fecha:** 2026-08-29
**RFC:** —
**Clase:** — (cambio de repo sin tocar `protocol/.agents/`; versionado docs-only según RFC-69)
**Depende de:** —
**Origen:** reporte de sesión de adopción del 2026-08-29 en un proyecto
adoptante: `git subtree pull --prefix=.` sobre la rama `dist` abortado por
conflictos modify/delete sobre todo el proyecto; la instrucción que lo
originaba está en la sección §1.1 de `docs/ADOPTION.md` antes de esta
corrección.

## Objetivo

Corregir `docs/ADOPTION.md` §1 para que la instalación y actualización del
payload no use `git subtree` con `--prefix=.`, que es incompatible con un
`dist` que solo trae `.agents/` + `AGENTS.md` en la raíz: al tratar la raíz del
proyecto adoptante como el árbol del subtree, un `subtree pull` interpreta cada
archivo del adoptante que no vive en `dist` como eliminado y genera conflictos
modify/delete. El plan documenta el mecanismo soportado: copia del payload
desde `dist` vía git (fetch + `git checkout FETCH_HEAD -- .agents AGENTS.md`) o
sin git, con manejo explícito de archivos eliminados entre versiones. Es un
cambio docs-only: no toca `protocol/.agents/`, no produce versión de protocolo
ni tag (RFC-69, versionado docs-only). Además restaura la batería canónica,
roja desde 10.0.0: `check_plan_citations.py` reportaba 4 citas históricas a
`PROJECT_ARTIFACTS.md` (eliminado por el plan 84/RFC-70) como rotas; las citas
históricas a artefactos eliminados se eximen en el checker, sin reescribir las
trazas.

## Criterio de entrada

- [ ] Verificación de premisas contra el repo (paso 0): la rama `dist` contiene
      únicamente `.agents/` + `AGENTS.md` (`git ls-tree -r --name-only dist`) y
      `docs/ADOPTION.md:1. Instalación` describe los métodos de copia.
- [ ] Rama de trabajo `dev` (`docs/VERSIONING.md:1. Ramas y roles`).
- [ ] Batería canónica en verde previa a la ejecución (salvo `check_dist_sync`,
      roja en `dev` por diseño — `docs/VERSIONING.md:4.1 Batería canónica de verificación`).

## Entregables

1. `docs/ADOPTION.md` §1 corregido: sin `git subtree --prefix=.`; §1.1 vía git
   (fetch + `git checkout FETCH_HEAD -- .agents AGENTS.md`), §1.2 sin git, con
   manejo de archivos *Removed* y verificación de `.agents/VERSION`.
2. `docs/plans/85-adopcion-sin-subtree.md` (este plan) registrado en
   `docs/plans/INDEX.md`.
3. Ítem en `[Unreleased]` de `CHANGELOG.md` con `(plan 85)`, sección `Fixed`.
4. `tools/check_plan_citations.py` + `tests/test_check_plan_citations.py`:
   citas históricas a artefactos eliminados (`REMOVED_ARTIFACTS`) exentas;
   citas desde documentos vivos siguen reportándose.
5. Plan `Executed` con `Nota de ejecución` e INDEX actualizado.

## Pasos

1. **Editar `docs/ADOPTION.md:1. Instalación`:** reemplazar la sección §1.1
   (Git subtree) y la §1.2 (copia manual) por los métodos correctos; explicar
   por qué no usar `git subtree --prefix=.` (el `dist` es payload-only y un
   `subtree pull` con prefijo raíz interpreta los archivos del adoptante fuera
   del payload como eliminados). Actualizar la referencia del intro a
   §1.1/§1.2.
2. **Registrar el plan** en `docs/plans/INDEX.md` (nueva serie, fila
   `85-adopcion-sin-subtree.md`).
3. **Changelog:** agregar en `CHANGELOG.md` `[Unreleased]` → `### Fixed` el
   ítem de la corrección con `(plan 85)`.
4. **Checker:** en `tools/check_plan_citations.py` eximir las citas desde
   fuentes históricas (`docs/plans/`, `docs/rfc/`, `CHANGELOG.md`) a los
   artefactos de `REMOVED_ARTIFACTS` (el archivo eliminado por el plan 84),
   manteniendo el reporte para documentos vivos; cubrir ambos casos en
   `tests/test_check_plan_citations.py`.
5. **Verificación:** correr la batería canónica y dejar constancia en la
   `Nota de ejecución`.
6. **Cierre:** plan → `Executed` con `Nota de ejecución`; INDEX actualizado;
   commit atómico en `dev` (Conventional Commit en inglés).

## Criterios de salida

- [ ] `docs/ADOPTION.md` no contiene ninguna instrucción `git subtree` con
      `--prefix=.`.
- [ ] §1.1 y §1.2 documentan métodos de instalación y actualización que
      funcionan con un `dist` payload-only, incluido el manejo de archivos
      eliminados entre versiones.
- [ ] Plan registrado en `docs/plans/INDEX.md`, changelog con ítem `(plan 85)`
      en `[Unreleased]`, plan `Executed` con `Nota de ejecución`.
- [ ] Batería canónica en verde (checkers + pytest); `check_version_state.py`
      sin errores (warnings OK en `dev`).
- [ ] `check_plan_citations.py` reporta 0 citas rotas en el repo y los tests
      nuevos cubren la exención histórica y el reporte en documentos vivos.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

H13 por juicio. `check_dist_sync.py` solo tras la promoción en `master` (roja
en `dev` por diseño — `docs/VERSIONING.md:4.1 Batería canónica de verificación`).

## Riesgos

- **Reproducción local de `git subtree`:** en este entorno el script
  `git-subtree` del Git for Windows falla con exit 126 (instalación rota del
  contrib), así que el fallo se verificó estructuralmente (contenido de `dist`)
  y por el reporte de la sesión adoptante; el fix no depende de reproducirlo.
- **Citas del plan:** las citas a `docs/ADOPTION.md` usan la sección
  `1. Instalación`, que sobrevive a la edición, para no romper
  `check_plan_citations.py`.
- **Batería roja pre-existente:** el plan 84 (10.0.0) dejó 4 citas históricas
  a `PROJECT_ARTIFACTS.md` sin resolver; se corrige el checker (exención
  histórica) en lugar de reescribir las trazas, conforme a RFC-46/RFC-69.

## Nota de ejecución

**2026-08-29** — Ejecutado en `dev`. `docs/ADOPTION.md` §1 reescrito: sin
`git subtree --prefix=.`; §1.1 vía git (fetch + `git checkout FETCH_HEAD --
.agents AGENTS.md`) y §1.2 sin git, con manejo de archivos *Removed* y
verificación de `.agents/VERSION`. `check_plan_citations.py` exime citas
históricas a `PROJECT_ARTIFACTS.md` (`REMOVED_ARTIFACTS`), restaurando la
batería que estaba roja desde 10.0.0; tests nuevos en
`tests/test_check_plan_citations.py`. Batería canónica en verde: checkers OK y
`243 passed` (pytest con `--basetemp` temporal y `-p no:cacheprovider` por
permisos del sandbox sobre el tmp dir por defecto de pytest). Plan registrado
en `docs/plans/INDEX.md`; changelog con ítem `(plan 85)` en `[Unreleased]`;
sin `VERSION` bump ni tag (RFC-69).
