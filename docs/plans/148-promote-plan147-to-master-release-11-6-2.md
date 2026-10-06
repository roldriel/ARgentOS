# Plan 148 — Promoción de `dev` a `master` y release de gobernanza 11.6.2

**Status:** Executed (2026-09-22; release commit, promoción a `master`, tag anotado `11.6.2` y `dist` ejecutados y verificados — ver `## Checkpoint / cierre` y `## Nota de ejecución`)
**Fecha:** 2026-09-22
**RFC:** — (Change de release/promoción; no introduce ningún cambio de contenido en `protocol/`: publica el estado ya verificado de `dev` y sólo escribe la metadata de versión de la release. RFC-56 no aplica a un acto de promoción)
**Clase:** — (acto de release; la única escritura bajo `protocol/` es `protocol/.agents/VERSION`, que es la metadata de versión de esta release)
**Change Level:** L2 (`max(coordination=1, scope=1, architectural=0, release=2, duration=1)`: un único Change integral cuyo eje es el **impacto de release** 2 —promueve `dev` a `master`, crea el tag anotado y regenera `dist`—; el impacto arquitectónico es 0 porque nada del modelo, de los contratos ni del contenido del payload cambia)
**Depende de:** plan 147 (corrección post-release, verificada por CI en `8173e77`), plan 146 (release 11.6.1 y su punto de cierre), `docs/VERSIONING.md` §3 (viñeta «Releases de gobernanza», enmendada por este Plan con autorización del mantenedor)
**Origen:** pedido directo del mantenedor (Change «PLAN 148 — Promote Plan147 to Master / Release», 2026-09-22), que autoriza explícitamente preparar el Change de promoción, determinar la versión, actualizar los archivos de versionado, crear los commits de release, promover `dev` a `master`, crear el tag, materializar `dist`, ejecutar las verificaciones post-promoción y cerrar el Change; y que, ante el conflicto detectado en el preflight, autorizó además **enmendar `docs/VERSIONING.md` §3** para admitir las releases de gobernanza como la vía de esta promoción

## Objetivo

Publicar el estado verificado de `dev` posterior al plan 147 como release de
gobernanza `11.6.2`, ejecutando la cadena completa

`release commit → dev → origin/dev → master → tag 11.6.2 → dist`

con cada gate registrado antes de tocar cualquier referencia remota, sin
reescribir historia, sin mover tags y sin ampliar el Scope.

La release tiene una segunda función, inseparable de la primera: **nivelar
`master`**. El tag `11.6.1` quedó sobre `8dbd92e`, que no contiene el commit de
cierre del Plan 146 (`7a9d393`); la promoción incorpora ese commit y los del
plan 147, de modo que `master` vuelve a contener toda la historia de `dev` y el
árbol publicado deja de conservar la revisión previa del artefacto del Plan 146.

## Autoridad y límites

El mantenedor autoriza, dentro de este Plan: preparar el Change, determinar la
versión, escribir `VERSION`/`PROTOCOL_VERSION`/`CHANGELOG.md`/`docs/VERSIONING.md`,
crear los commits de release, promover `dev` a `master` por el mecanismo
existente, crear el tag anotado, materializar `dist` con el workflow existente,
verificar post-promoción y cerrar el Change. Autoriza además la enmienda de
`docs/VERSIONING.md` §3 que esta promoción requiere.

Queda **fuera** de este Plan: force-push, reescritura de historia, borrado de
commits, alteración o movimiento de tags existentes, alteración de las releases
`11.3.0`–`11.6.1`, reescritura de los Planes 146/147 o de cualquier artefacto
cerrado, modificación de RFC-75/ADR-15/ADR-16, del Change Lifecycle, de SAE o
del contenido del payload, modificación de `ROADMAP.md`, invención de una
estrategia de release nueva, creación de una state machine o de una autoridad
nueva, y cualquier limpieza no relacionada con la release.

## Criterio de entrada

- [x] `dev` = `origin/dev` = `8173e773313585d1127643a9d2a71f2b7d370a4e`; árbol de trabajo sin modificaciones rastreadas.
- [x] CI **posterior** a los commits que se promueven: run `35759774259`, `headSha` = `8173e77…`, **success**.
- [x] Tags `11.3.0`–`11.6.1` presentes, anotados e intactos; `master` = `origin/master` = `8dbd92e0f006643412d21d562c5532be30f67647`.
- [x] Contrato de versionado leído y aplicado (`docs/VERSIONING.md` §1–§10).
- [x] Autorización explícita del mantenedor para la promoción y para la enmienda de §3.

## Estado inicial verificado

Verificado con Git como fuente de verdad antes de cualquier modificación. Nada
de este apartado se asumió.

| Hecho | Valor verificado |
|---|---|
| Branch de trabajo | `dev` |
| `dev` (HEAD) | `8173e773313585d1127643a9d2a71f2b7d370a4e` |
| `origin/dev` | `8173e773313585d1127643a9d2a71f2b7d370a4e` (idéntico; `dev` no está adelante) |
| `master` = `origin/master` | `8dbd92e0f006643412d21d562c5532be30f67647` |
| Commits `master..dev` | **3** (`7a9d393`, `c901d56`, `8173e77`) |
| Commits `dev..master` | **10** (todos commits de release sobre la línea de `master`) |
| Diff `dev` vs `master` | **11 archivos**, ninguno bajo `protocol/` salvo `VERSION` |
| Payload de contenido `dev` vs `master` | **0 archivos** con diferencia bajo `protocol/` (excluida `VERSION`) |
| `protocol/.agents/VERSION` antes del release | `11.6.1` en `dev` y en `master` (idéntico) |
| `runtime/toolcalls/canonical.py` (`PROTOCOL_VERSION`) antes | `11.6.1` |
| Tags publicados | `11.0.0`, `11.0.1`, `11.1.0`, `11.2.0`, `11.3.0`, `11.4.0`, `11.5.0`, `11.6.0`, `11.6.1` (todos anotados) |
| `origin/dist` | `c07abdd9ca50c459f7df5b075057f7b8d5f9762b` |
| Árbol de trabajo | 0 modificaciones rastreadas; 1 archivo untracked **externo** (`MASTER_PENDING_WORK_INVENTORY.md`) |
| CI del HEAD a promover | run `35759774259` → **success** |

## Determinación de la versión

**Versión determinada: `11.6.2` (PATCH sucesor de `11.6.1`).**

Razonamiento, aplicando el contrato vigente y no una suposición:

1. **No hay cambio de protocolo que clasificar.** El diff `dev` vs `master` no
   contiene ninguna diferencia de contenido bajo `protocol/`; la única ruta de
   `protocol/` que este Plan escribe es `protocol/.agents/VERSION`, que es la
   metadata de versión de la release misma. Por lo tanto la tabla de
   `docs/VERSIONING.md` §3 (MAJOR/MINOR/PATCH por impacto en el payload) no
   tiene un cambio que clasificar, y `11.6.2` **no** es un PATCH de contenido:
   es la versión de la **release del repositorio**.
2. **La vía existe porque el contrato la declara.** El preflight detectó el
   conflicto: la viñeta «Cambios docs-only» de §3 prohíbe expresamente una
   release de gobernanza con tag, mientras §1 y §2 invariante 2 exigen un tag
   para todo lo que entra a `master`. Ambas reglas no pueden satisfacerse a la
   vez con este contenido, de modo que la rama se detuvo y se escaló. El
   mantenedor autorizó **enmendar §3** para admitir las releases de gobernanza
   como excepción de promoción; esa enmienda es el criterio vigente de esta
   release y está registrada en el propio documento.
3. **Sucesor PATCH y no otra cosa.** La enmienda fija que la versión de una
   release de gobernanza es la sucesora PATCH de la última publicada en
   `master` (`X.Y.(Z+1)`), nunca MINOR ni MAJOR, porque la release publica un
   correctivo y no una capacidad nueva. Última versión publicada: `11.6.1` →
   **`11.6.2`**. Se calcula desde `master`, no desde `dev` (§3).
4. **Las dos fuentes de versión se alinean.** El invariante versión ↔
   changelog ↔ tag (§2.1) y `tools/check_version_state.py` exigen que
   `PROTOCOL_VERSION` (`runtime/toolcalls/canonical.py`) coincida con
   `protocol/.agents/VERSION`: ambos pasan a `11.6.2`.

## Pasos

1. **Preflight** (read-only): refs, working tree, tags, CI del HEAD, contrato de versionado. → registrado arriba.
2. **Enmienda de `docs/VERSIONING.md` §3** (autorizada): viñeta «Releases de gobernanza» con la definición, el límite de contenido del payload, la regla de versión sucesora PATCH, los artefactos que produce y el precedente.
3. **Versión:** `protocol/.agents/VERSION` → `11.6.2` (sin salto de línea final, como el original) y `PROTOCOL_VERSION` → `11.6.2`.
4. **Changelog:** nueva sección `## [11.6.2] — 2026-09-22` con el ítem del Plan 147 movido desde `[Unreleased]`, e ítem del Plan 148 en `[Unreleased]` describiendo la promoción.
5. **Snapshot §9** de `docs/VERSIONING.md` reconciliado: `master`/`dev` = `11.6.2`, contenido del protocolo idéntico, divergencia del Plan 146 resuelta por esta promoción.
6. **Plan 148** y su registro en `docs/plans/INDEX.md`.
7. **Release commit** en `dev` con version bump, changelog, metadata de release, el Plan y su INDEX.
8. **Validación pre-promoción:** batería canónica, tests, harness, gates C-1/C-2/C-3, EARS, D01.
9. **Promoción:** merge `dev` → `master` (mecanismo documentado en `docs/VERSIONING.md` §4 paso 7), sin fast-forward artificial y sin squash.
10. **Tag anotado `11.6.2`** sobre el commit de promoción.
11. **Publicación:** push de `dev`, `master` y el tag; `publish-dist` para materializar `dist`.
12. **Verificación post-promoción** completa y **cierre** del Plan.

## Criterios de salida

- [x] Versión determinada conforme al contrato vigente y documentada.
- [x] Release commit creado en `dev`.
- [x] `dev` promovido a `master`.
- [x] Tag anotado `11.6.2` creado correctamente.
- [x] Tags anteriores intactos.
- [x] `dist` sincronizado y `check_dist_sync.py` verde en `master`.
- [x] Batería canónica post-promoción verde; `pytest` verde.
- [x] Sin cambios fuera del Scope; sin force-push; sin reescritura de historia.
- [x] Planes 146 y 147 intactos; `ROADMAP.md` sin modificación.
- [x] Working tree final limpio.

## Verificación

- Batería canónica (`docs/VERSIONING.md` §4.1): seis checkers + `python -m pytest tests/`.
- `python -m pytest protocol/.agents/harness/tests/`.
- Gates C-1/C-2/C-3, `tools/check_ears_coverage.py`, `tools/check_discovery_output.py`.
- `python tools/check_version_state.py` (invariante versión ↔ changelog ↔ tag) y, ya en `master`, `python tools/check_dist_sync.py`.
- Git: `git status`, `git rev-parse`, `git merge-base --is-ancestor`, `git log --graph`, `git ls-remote --tags origin`, `git push --dry-run`.

## Riesgos

- **Que el merge no sea contenido-trivial:** `master` no aporta contenido (su árbol es idéntico al del merge-base con la línea de release), de modo que el merge de `dev` es limpio por diseño; se revalida el estado real justo antes de ejecutarlo.
- **Que `publish-dist` no dispare:** el workflow se dispara con el push a `master` que toca `protocol/`; esta promoción **toca** `protocol/.agents/VERSION`, que es precisamente la condición de disparo. Si no disparara, se ejecuta por `workflow_dispatch` y se verifica contra `origin/dist`.
- **Que la enmienda de §3 se lea como una ampliación de autoridad:** la viñeta se limita a nombrar la excepción de promoción, mantiene la prohibición del cambio de contenido del payload y no habilita ninguna otra operación.

## Trazabilidad

`<PLAN-147>:PC-1` (nivelación de `master`) → plan 148 → release de gobernanza `11.6.2`. El plan 147 aporta el contenido que se publica; el plan 146 aporta el commit de cierre que se nivela. `docs/VERSIONING.md` §3 es la autoridad de la versión.

## Release intent

Registrado **antes** de modificar cualquier referencia remota. Ninguna operación
remota se ejecuta si el estado real deja de coincidir con este conjunto.

| Elemento | Valor |
|---|---|
| `dev` (SHA del release commit) | registrado por el commit de este Plan — ver `## Checkpoint / cierre` |
| `dev` (SHA previo) | `8173e773313585d1127643a9d2a71f2b7d370a4e` |
| `origin/dev` (SHA al inicio) | `8173e773313585d1127643a9d2a71f2b7d370a4e` |
| `master` (SHA al inicio) | `8dbd92e0f006643412d21d562c5532be30f67647` |
| Merge-base esperado | `8dbd92e0f006643412d21d562c5532be30f67647` (`master` es ancestro de `dev`) |
| Versión | `11.6.2` |
| Tag esperado del release | `11.6.2` (anotado, sobre el commit de promoción de `master`) |
| Árbol esperado tras la promoción | el árbol del release commit (`6f3b8a07…`): `master` no aporta contenido |
| Operaciones previstas | push de `dev`; merge `dev` → `master`; push de `master`; creación y push del tag anotado `11.6.2`; `publish-dist` |
| Resultado de los gates | batería canónica y checkers específicos `exit 0`; C-1/C-2/C-3 sin `ANOMALY`; `pytest` y harness verdes |

**Por qué un solo tag y no un rango.** A diferencia de la promoción del plan 146
—que oficializó cinco versiones implementadas y sin tag—, aquí no hay ninguna
versión pendiente: `11.6.1` y todo el rango anterior ya tienen su tag, y la
única versión nueva es la de esta release de gobernanza.

## Validation anchor

- **Declared scope:** las cuatro rutas de contenido y metadata del release que la identidad de contenido mide — `CHANGELOG.md`, `docs/VERSIONING.md`, `protocol/.agents/VERSION` y `runtime/toolcalls/canonical.py`. Quedan fuera del scope **medido**: este artefacto de Plan y su registro en `docs/plans/INDEX.md` (governance del Change: el índice es espejo descriptivo, `docs/VERSIONING.md:7. Estados de planes y RFCs`, y su escritura no altera la identidad de la release; excluirlos rompe la auto-referencia de escribir el cierre dentro del propio estado medido, convención anti-auto-referencia, precedente Planes 114/116/134/140–147); `dist/` (materializado por el workflow, no commiteado en `dev`); `ROADMAP.md`, `docs/adr/`, `docs/rfc/` y `.agents/`; y el contenido de `protocol/` distinto de `VERSION`, que no cambia en este Change.
- **Validation command-set:** los 7 comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (`check_protocol_invariants --payload protocol .`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `python -m pytest tests/`) + `python -m pytest protocol/.agents/harness/tests/` + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + los checkers específicos `tools/check_ears_coverage.py` y `tools/check_discovery_output.py` + `python tools/check_dist_sync.py` (sólo sobre `master`, tras la promoción) + los checks de release: `git status --porcelain`, `git rev-parse` de `dev`/`origin/dev`/`master`/`origin/master`/`origin/dist`, `git merge-base --is-ancestor`, `git ls-remote --tags origin` y los dry-run de push.
- **Effective inputs (repo content):** el scope declarado; `protocol/.agents/VERSION` y `runtime/toolcalls/canonical.py` (las dos fuentes de versión, que el invariante exige iguales); `CHANGELOG.md` completo (la superficie de versiones, incluida la sección `[11.6.2]` nueva); `docs/VERSIONING.md` (contrato de versionado y snapshot §9); `docs/plans/INDEX.md` y los planes 116, 146, 147 y 148; el corpus completo de `docs/plans/` (148 artefactos) como población de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada del checker de invariantes; el estado Git de `dev`, `origin/dev`, `master`, `origin/master` y `origin/dist`; y `.github/workflows/publish-dist.yml` como definición del mecanismo de publicación de `dist`.
- **Observed dependencies:** stdlib únicamente; el CLI `git` disponible; el CLI `gh` autenticado para leer los runs de CI; conectividad con `https://github.com/roldriel/ARgentOS.git` para `git ls-remote`, los dry-run de push y la publicación de `dist`.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; pytest 9.0.3; repositorio bajo OneDrive (`C:\Users\rolda\OneDrive\Escritorio\Proyectos\ARgentOS`); `master` sin branch protection (decisión del owner registrada en `docs/VERSIONING.md:9. Estado actual (2026-09-22, release de gobernanza 11.6.2)`), de modo que el push no depende de rulesets server-side; la materialización de `dist` depende del runner de GitHub Actions y del token `DIST_PUSH_TOKEN` (o del `GITHUB_TOKEN` por defecto).
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `c7ba119ec20df26c36ee6889d9fceb519f80ee2f` (árbol del estado validado sobre las cuatro rutas del scope, resuelto con un índice aislado sobre el contenido del release commit; es la identidad de estado del scope medido, no el árbol completo del commit, que incluye el artefacto de Plan).
  - **Delta scoped identity (scope S = las cuatro rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `27f116874d232b763a9403771d933475856a08536827aa9299bc6a6424590324` (`python tools/scoped_content_identity.py` sobre las cuatro rutas, tras `git add` de los cambios del release — precondición de reproducibilidad de `tools/scoped_content_identity.py`, plan 96 §13.2).
  - **Límite declarado:** el scope excluye `dist/`, el contenido de `protocol/` distinto de `VERSION`, y la governance del Change (este artefacto y el `INDEX`), de modo que el registro del anchor y del checkpoint no altera la identidad del estado que el checkpoint certifica (convención anti-auto-referencia, precedente Planes 114/116/134/140–147).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/VERSIONING.md`, `protocol/.agents/VERSION`, `runtime/toolcalls/canonical.py`.
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

## Checkpoint / cierre

- **Commits de cierre:** dos (2) commits en `dev`: (1) el release commit `6f7dc7a9db14108aecee98548422e0f301b20666` (árbol `408137bd85eebcf6c86adb9996f270f1ca124a43`) —version bump a `11.6.2`, changelog, enmienda de §3, snapshot §9, el Plan 148 y su registro en el INDEX—; (2) el commit de registro de este checkpoint, que transcribe la promoción, el tag y la verificación post-promoción. GC-1 admite el cierre multi-commit; los SHA y los tree id quedan como locators, no como identidad.
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `27f116874d232b763a9403771d933475856a08536827aa9299bc6a6424590324` / `c7ba119ec20df26c36ee6889d9fceb519f80ee2f`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** el release commit (1) tiene árbol `408137bd85eebcf6c86adb9996f270f1ca124a43`, que incluye la governance del Change (este artefacto y el `INDEX`) además del estado medido, de modo que **no** coincide con la identidad del estado de cierre y no tiene por qué: `validated tree == commit tree` no es un requisito (RFC-75 `Mecanismo 7`). El commit de registro (2) modifica únicamente artefactos de governance excluidos del scope medido y por lo tanto no altera la identidad certificada.
- **Consistencia checkpoint↔anchor:** PASS — verificada por C-2 sobre el artefacto de este Plan en el estado de cierre.
- **Governance aplicada:** `docs/VERSIONING.md` §3 enmendado (viñeta «Releases de gobernanza») y §9 reconciliado en el punto de promoción que §5 declara; `CHANGELOG.md` con la sección `[11.6.2] — 2026-09-22` y el ítem de la promoción; `protocol/.agents/VERSION` y `PROTOCOL_VERSION` en `11.6.2`; `docs/plans/INDEX.md` registra el Plan y su serie. Sin RFC nueva, sin ADR, sin cambio de contenido de payload.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados: `docs/VERSIONING.md` §3 (la enmienda autorizada que da vía a la release de gobernanza) y §9 (snapshot corriente: `master`/`dev` en `11.6.2`, contenido del protocolo idéntico y divergencia del Plan 146 resuelta por esta promoción); `CHANGELOG.md` (sección de la release e ítem de la promoción). `docs/plans/INDEX.md` registra el Plan y su serie. `ROADMAP.md` **0 diff**: el procedimiento de release no lo exige. Los artefactos históricos (Planes 146 y 147, tags, releases anteriores) no se reescriben (RFC-46); la resolución de `<PLAN-147>:PC-1` se registra por referencia.
- **Roadmap impact:** `NOT_REQUIRED` — razón explícita: esta release publica estado ya existente de `dev` y no crea, completa, cancela, reclasifica, re-prioriza ni re-dependencia ningún trabajo del mapa operativo, ni mueve ítems entre candidato / activo / bloqueado. `ROADMAP.md` queda con **0 diff**.
- **GAPs declarados:** ninguno nuevo. El `GAP` histórico de C-2 del Plan 116 (`<PLAN-133>:F-1`, clasificado `HISTORICAL / NON-ACTIONABLE`) se conserva sin resolver y no bloquea ninguna operación de este Plan; ningún `GAP` se convierte en `PASS`.
- **Condición derivada:** `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor ∧ evidencia `PASS` para el estado de cierre. `Promoted` y `Released` se registran en `## Nota de ejecución` y en la verificación post-promoción.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-148>:F-1` — estado: `resolved`; resolución: corregido por `<PLAN-148>:C-1` (la transición de estado la registra el mantenedor, CL-8); observación: el contrato de versionado no tenía vía para publicar el estado de `dev` posterior al plan 147 — `docs/VERSIONING.md` §3 prohibía una versión y un tag para un cambio docs-only («no existe una "release de gobernanza" con tag sin versión»), mientras §1 y §2 invariante 2 exigen un tag para todo lo que entra a `master`, de modo que la promoción autorizada por el mantenedor no podía ejecutarse sin violar una de las dos reglas; evidencia original: `git diff --name-status 8dbd92e..dev` → 11 archivos, **0** bajo `protocol/`; `git diff 8dbd92e..dev -- protocol/.agents/VERSION` → vacío; preflight de este Plan, que detuvo la rama y escaló la decisión; estado Git observado: `dev` = `8173e77`, `master` = `8dbd92e`, `VERSION` = `11.6.1` en ambas ramas; provenance original: `docs/VERSIONING.md` §3 viñeta «Cambios docs-only (RFC-69)» y §1/§2.
- `<PLAN-148>:F-2` — estado: `resolved`; resolución: corregido por `<PLAN-148>:C-2`; observación: el `GAP-3`/`<PLAN-147>:PC-1` (el árbol publicado de `master` conservaba la revisión previa del artefacto del Plan 146 porque `7a9d393` no era ancestro de `master`) quedaba registrado como hecho factual sin vía de resolución, dado que nivelar `master` es una promoción; evidencia original: `git merge-base --is-ancestor 7a9d393 8dbd92e` → exit 1; `git show 54171d8:docs/plans/146-release-promotion-11-6-1.md` con los literales de identidad diferidos al checkpoint; estado Git observado: `master` = `8dbd92e` (el tag `11.6.1`), sin `7a9d393` en su historia; provenance original: `docs/plans/147-post-release-integrity-and-ci-compatibility.md:## Findings / Correcciones / Pending` (`<PLAN-147>:PC-1`).

### Correcciones

- `<PLAN-148>:C-1` — refs origen: `<PLAN-148>:F-1`; alcance de revalidación: `docs/VERSIONING.md` (viñeta «Releases de gobernanza» en §3 y snapshot §9) y `protocol/.agents/VERSION` + `runtime/toolcalls/canonical.py`; evidencia: el preflight dejó la rama detenida y el mantenedor autorizó la enmienda; tras la enmienda, `python tools/check_version_state.py` → exit 0 con `VERSION` = `PROTOCOL_VERSION` = `11.6.2`, y la batería completa verde en `dev` y en `master`; carácter: FACTUAL / TRACEABILITY (la acción la autoriza este Plan y la autorización explícita del mantenedor; no es fuente normativa).
- `<PLAN-148>:C-2` — refs origen: `<PLAN-148>:F-2`; alcance de revalidación: la promoción misma (`dev` → `master`) y el tag anotado; evidencia: `git merge-base --is-ancestor dev master` → exit 0 y `git rev-list --count master..dev` → **0** tras la promoción, de modo que `master` vuelve a contener toda la historia de `dev`; el árbol del commit de promoción `34cab97a…` (`408137bd…`) es idéntico al de `dev`; la afirmación del Plan 146 «`master` contiene toda la historia de `dev`» pasa a ser verdadera sin reescribir su artefacto.

### Pending decisions

No se registran pending decisions nuevas. `<PLAN-147>:PC-1` queda **resuelta por este Change** (su resolución se registra por referencia, sin reescribir el artefacto cerrado del Plan 147). Las pending decisions preexistentes de otros artefactos (`<PLAN-125>`, `<PLAN-126>`, `<PLAN-131>`, `<PLAN-132>`, `<PLAN-137>`, `<PLAN-138>` y la materialidad ambiental de `<PLAN-122>`/`<PLAN-123>` según el inventario del Plan 146) conservan su estado, su owner y su vía: ninguna está en el Scope de este Plan y ninguna bloquea la release.

## Nota de ejecución

**Fecha:** 2026-09-22. **Ejecución:** completa; la cadena
`release commit → dev → origin/dev → master → tag 11.6.2 → dist` se ejecutó y
se verificó.

**Preflight y decisión detenida.** El preflight (read-only) verificó refs,
working tree, tags, el CI **posterior** a los commits a promover —run
`35759774259` sobre `8173e77`, **success**— y el contrato de versionado. El
hallazgo decisivo fue que el diff `dev` vs `master` no contenía **ninguna**
diferencia de contenido bajo `protocol/` (11 archivos, 0 de payload; `VERSION`
idéntico en ambas ramas), de modo que §3 prohibía versión y tag mientras §1/§2
los exigían para `master`. La rama de release se **detuvo** y se escaló; el
mantenedor autorizó enmendar `§3` para admitir las releases de gobernanza, y esa
enmienda es el criterio vigente de la versión (`11.6.2`, sucesora PATCH de
`11.6.1`).

**Ejecución del release.** Registrado el release intent antes de tocar cualquier
referencia remota, se ejecutó cada paso de la secuencia autorizada:

1. **Release commit** en `dev`: `6f7dc7a9db14108aecee98548422e0f301b20666`
   (árbol `408137bd85eebcf6c86adb9996f270f1ca124a43`), con el version bump, la
   sección `[11.6.2] — 2026-09-22`, la enmienda de §3, el snapshot §9, el Plan
   148 y su registro en el INDEX. → **OK**.
2. **Push de `dev`**: `8173e77..6f7dc7a dev -> dev`. Sin force. → **OK**;
   `origin/dev` = `6f7dc7a9…` = `dev`.
3. **Promoción a `master`** por merge `--no-ff` de `dev`, revalidando antes el
   estado real: `master` = `8dbd92e0…`, `dev` = `6f7dc7a9…`, merge-base =
   `54171d86…`, **árbol de `master` = árbol del merge-base**
   (`bc280abd…`), de modo que el merge es contenido-trivial. → **OK**: merge
   commit **`34cab97a470f16709f762742eab2aad455e41703`**, padres `8dbd92e`
   (`master` anterior) y `6f7dc7a` (tip de `dev`), sin conflictos; árbol del
   merge = `408137bd…` = árbol de `dev`, exactamente el árbol esperado en el
   release intent.
4. **Push de `master`**: `8dbd92e..34cab97 master -> master`. Sin force. →
   **OK**; `origin/master` = `34cab97a…`; `git merge-base --is-ancestor dev
   master` → 0 y `git rev-list --count master..dev` → **0**.
5. **Tag anotado `11.6.2`** sobre el commit de promoción, con mensaje que cita
   la sección del changelog y los planes publicados. Sin force-tag. → **OK**:
   tag object `0e7da7890d71ef50c939088f8c511b9576749ac4` → `34cab97a…`;
   empujado (`* [new tag]`); los nueve tags anteriores intactos (mismos objetos
   que antes del Change).
6. **`dist`** regenerado por `publish-dist`, disparado por el push a `master`
   que toca `protocol/` (la promoción toca `protocol/.agents/VERSION`). →
   **OK**: run `35764055240` **completed / success**; `origin/dist` pasó de
   `c07abdd` a `f390ebddf3800e54be57f5c54b5eb2650e15f554`
   (`dist: publish from master @ 34cab97`), con `.agents/VERSION` = `11.6.2` y
   el layout `.agents/` + `AGENTS.md`; `python tools/check_dist_sync.py` sobre
   `master` → «dist is in sync with protocol/».
7. **Verificación post-promoción** de la cadena completa. → **OK**, tabla
   siguiente.

**Batería post-promoción (sobre `master`, HEAD `34cab97a…`).** Seis checkers
canónicos —`check_protocol_invariants` (`--payload protocol .`),
`check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`,
`check_session_artifacts`, `check_version_state`— **exit 0**;
`check_ears_coverage` y `check_discovery_output` **exit 0**;
`check_dist_sync` **exit 0**; `python -m pytest tests/` → **1185 passed,
1 skipped**; `python -m pytest protocol/.agents/harness/tests/` → **109
passed**. Gates: C-1 `EXCLUDED=94, VALID=54, GAP=0, ANOMALY=0`; C-2
`VALID=53, GAP=1, ANOMALY=0` (el `GAP` histórico del Plan 116, conservado);
C-3 `VALID=28, GAP=0, ANOMALY=0`.

**Intermitencia observada en los tests del host del orquestador (no atribuible
a este Change).** Durante las corridas de la batería bajo carga se observaron
**tres** fallos intermitentes, cada uno en una corrida distinta y nunca
repetidos:
`test_functional_dogfood_the_checkpoint_survives_a_rewrite_between_runs` de
`tests/test_sae_scope_enforcement_dogfood.py`,
`test_a_required_obligation_outside_the_scope_is_refused_and_changes_nothing`
de `tests/test_sae_scope_enforcement.py`
y, en la corrida sobre `master`, un tercero de la misma familia. La
caracterización es factual, no una dispensa:

- La suite completa **pasó** en la corrida de verificación final (`1185 passed,
  1 skipped`) sobre el mismo commit.
- Los tres tests pasan **aislados**: 12 corridas consecutivas de
  `tests/test_sae_scope_enforcement.py` + `tests/test_sae_scope_enforcement_dogfood.py`
  → **0 fallos**; los módulos del orquestador juntos → 152 passed.
- Los tres ejercitan `ExecutionHost(...).run(max_iterations=2)` y afirman sobre
  la secuencia exacta de acciones, de modo que dependen del número de
  iteraciones que el host conduce; las corridas que fallaron fueron las que
  corrieron **en paralelo** con otro proceso pesado de la batería.
- Ninguno toca los cuatro contratos que este Change y el plan 147 modificaron
  (C-1, la configuración de CI, los dogfoods de historia Git y la resolución de
  segmentos); no hay mecanismo que los conecte.
- No se silencia nada: no se agrega `xfail`, `skip`, `flaky` ni relajación de
  aserción. La intermitencia queda registrada como observación factual para un
  Change propio si vuelve a aparecer; no bloquea este release y no se oculta
  como `PASS`.

**Verificación post-promoción.**

| Elemento | Valor verificado |
|---|---|
| `dev` | `6f7dc7a9db14108aecee98548422e0f301b20666` |
| `origin/dev` | `6f7dc7a9db14108aecee98548422e0f301b20666` (idéntico) |
| `master` | `34cab97a470f16709f762742eab2aad455e41703` |
| `origin/master` | `34cab97a470f16709f762742eab2aad455e41703` |
| Commit de release | `6f7dc7a9db14108aecee98548422e0f301b20666`, mensaje `release: promote dev to master and publish governance release 11.6.2 (plan 148)` |
| Commit de promoción | `34cab97a470f16709f762742eab2aad455e41703` (merge de `8dbd92e` y `6f7dc7a`), mensaje `release: promote protocol governance release 11.6.2 (plan 148; plans 146-147)` |
| Árbol de `master` | `408137bd85eebcf6c86adb9996f270f1ca124a43` = árbol de `dev` |
| `dev` contenida en `master` | `git rev-list --count master..dev` = **0** |
| Tag `11.6.2` | tag object `0e7da7890d71ef50c939088f8c511b9576749ac4` → `34cab97a470f16709f762742eab2aad455e41703` |
| Tags anteriores | `11.0.0` (`f3dabdda…`), `11.0.1` (`d5076ace…`), `11.1.0` (`683a1cbd…`), `11.2.0` (`d7c853f6…`), `11.3.0` (`dd47e01f…`), `11.4.0` (`f6760524…`), `11.5.0` (`35371c33…`), `11.6.0` (`905941a2…`) y `11.6.1` (`06022f31…`) **intactos** |
| `dist` | `f390ebddf3800e54be57f5c54b5eb2650e15f554` (`origin/dist` = `dist` local), `VERSION` = `11.6.2` |
| `VERSION` / `PROTOCOL_VERSION` | `11.6.2` / `11.6.2` (coinciden) |
| `CHANGELOG` | secciones `[11.6.2]` (2026-09-22) y anteriores presentes y con tag |
| Working tree | `git status --porcelain` → sólo el artefacto externo untracked `MASTER_PENDING_WORK_INVENTORY.md` (0 modificaciones rastreadas) |
| CI de la promoción | `check-protocol` **success** (`35764055173`, `master`) y `35764030834` (`dev`); `publish-dist` **success** (`35764055240`) |

**Integridad.** Sin force-push, sin `--force-with-lease`, sin force-tag, sin
borrado de commits y sin reescritura de historia: los únicos movimientos de refs
fueron `dev` (fast-forward), `master` (fast-forward) y la creación del tag
`11.6.2`. `protocol/` con 0 diff de contenido (`VERSION` es metadata de la
release); `ROADMAP.md` con 0 diff; los Planes 146 y 147 intactos. La única
irregularidad operativa fue local y no afectó al repositorio: la primera corrida
de `check_dist_sync.py` comparó contra la rama local `dist` desactualizada
(`c07abdd`); tras `git fetch origin dist:dist` el check quedó verde contra
`f390ebd`.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1), Plan `Executed`.
Committed = TRUE  — commits atómicos en `dev` (`6f7dc7a` release, y este registro).
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Promoted  = TRUE  — merge `dev` → `master` verificado en `34cab97a…`, con `master..dev` = 0.
Released  = TRUE  — tag anotado `11.6.2` inmutable sobre el commit de promoción,
                    `dist` regenerado por `publish-dist` y CI verde en `master`.
```
