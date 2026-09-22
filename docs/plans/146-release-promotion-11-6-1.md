# Plan 146 — Promoción de `dev` y release del protocolo 11.3.0–11.6.1 (Release 11.6.1)

**Status:** Executed (2026-09-21; release intent registrado, promoción y tags ejecutados — ver `## Checkpoint / cierre`)
**Fecha:** 2026-09-21
**RFC:** — (Change de release/promoción; no modifica `protocol/.agents/`: la promoción transporta el payload ya autorizado por RFC-76/77/78/79 y sus planes, y este Plan no introduce ningún cambio de payload propio)
**Clase:** — (sin efecto de payload propio: las únicas modificaciones son `CHANGELOG.md`, `docs/VERSIONING.md`, `docs/plans/INDEX.md` y este artefacto; RFC-56 no aplica a un acto de promoción)
**Change Level:** L2 (`max(coordination=1, scope=1, architectural=0, release=2, duration=1)`: una única autorización y un único Change integral que cierra el ciclo de los 33 commits de `dev`, pero cuyo eje es el **impacto de release** 2 —publica `dev`, promueve a `master`, crea los tags anotados del rango no publicado y deja `dist` regenerado—; el impacto arquitectónico es 0 porque nada del modelo, de los contratos ni del layout cambia)
**Depende de:** plan 119 y RFC-76 (11.3.0), plan 120 y RFC-77 (11.4.0), plan 121 y RFC-78 (11.5.0), plan 142 y RFC-79 (11.6.0), plan 143 (11.6.1), plan 145 (cierre del backlog accionable DEV y baseline del release)
**Origen:** pedido directo del mantenedor (Change «PLAN 146 — Release 11.6.1», 2026-09-21), que autoriza explícitamente inspeccionar los 33 commits que separan `dev` de `origin/dev`, preparar y ejecutar la promoción de `dev` a `master`, publicar `dev` en su upstream, crear el tag del release y publicar el release por el mecanismo oficial existente

## Objetivo

Cerrar el ciclo de la línea de desarrollo actualmente contenida en `dev`, ejecutando la operación completa

`dev → origin/dev → master → tag 11.6.1 → release 11.6.1`

como una **única Change integral**, con la evidencia de cada gate registrada antes de tocar cualquier referencia remota, sin reescribir historia, sin operaciones destructivas y sin ampliar el Scope.

## Autoridad y límites

El mantenedor autoriza, dentro de este Plan: inspeccionar los commits de `dev`, verificar su coherencia, publicar `dev` en su upstream, promover a `master`, crear el tag del release y publicar el release por el mecanismo oficial existente.

Queda **fuera** de este Plan: modificar `protocol/` para hacer pasar un gate; modificar RFCs, ADRs o planes cerrados; reescribir commits o la historia de `dev`/`master`; usar `git push --force`, `--force-with-lease` o force-tag; cualquier operación destructiva; crear nueva autoridad, state machine, registry o Change mechanism; ocultar `FAIL`, `GAP` o `ANOMALY`; o ampliar el Scope autónomamente. Si aparece una condición que exija una decisión normativa nueva, una ampliación de Scope o una autoridad que este Plan no posee, la operación se detiene y el bloqueo se registra exactamente.

## Estado inicial verificado

Verificado con Git como fuente de verdad antes de cualquier modificación. Nada de este apartado se asumió: todos los valores se comprobaron en el árbol.

| Hecho | Valor verificado |
|---|---|
| Branch de trabajo | `dev` |
| `dev` (HEAD) | `a3efd411d8923668f0cadf25636bc6c9d9602d09` |
| Árbol de `dev` | `3da9162f35b36a38a677349a0ef07160c74523dc` |
| `origin/dev` | `4aa261774c034eba3bb6f4e51810513ce9e25933` |
| Commits `origin/dev..dev` | **33** (confirmado, no asumido) |
| `master` = `origin/master` | `dc21458c224cd60d9666c0026e79fc4fddd35fc8` |
| Commits `master..dev` | **42** |
| Commits `dev..master` | **9** (todos commits de release sobre la línea de `master`) |
| Merge-base `dev`/`master` | `f85b558ea56b6e5fabcb7f12d9b5716f618a9428` |
| Árbol de `master` vs árbol del merge-base | **idénticos** (`e76af36caf8ffd298d13af3c15cf792501cd24af`) |
| Árbol de trabajo | 0 modificaciones rastreadas; 1 archivo untracked **externo** (ver `## GAP declarado` y RG-2) |
| `protocol/.agents/VERSION` | `11.6.1` |
| `runtime/toolcalls/canonical.py` (`PROTOCOL_VERSION`) | `11.6.1` (coincide con `VERSION`) |
| Tags publicados del rango 11.x | `11.0.0`, `11.0.1`, `11.1.0`, `11.2.0` (todos anotados, todos sobre `dc21458`) |
| Tags ausentes | `11.3.0`, `11.4.0`, `11.5.0`, `11.6.0`, `11.6.1` |
| `origin/dist` | `93f50b9969dc42b4c565931a993339df3abbb068` (`dist: publish from master @ dc21458`) |
| Planes recientes | 135–145 `Executed`; Plan 137 `Executed` tras la reconciliación del Plan 145 |

## Reconstrucción de los 33 commits

Los 33 commits de `origin/dev..dev` se reconstruyeron uno por uno desde Git. Cada uno es explicable dentro de la línea de desarrollo: no hay commits locales fuera del conjunto, no hay feature branches y no hay commits de otras líneas.

| # | SHA | Tipo | Mensaje | Plan | Área principal | Relación con el release |
|---|---|---|---|---|---|---|
| 1 | `13096fb` | `fix` | fix(tests): consolidate tools imports and stdlib checks | 124 | `conftest.py`, `tests/`, `docs/` | Higiene DEV previa; sin efecto de payload |
| 2 | `4cd11ed` | `docs` | docs(plans): record human resolution of plan 124 findings | 124 | `docs/` | Registro de gobernanza |
| 3 | `bbc45a6` | `docs` | docs(architecture): record repository structure decisions A3/B4/F1/L1 | 125 | `docs/`, `CHANGELOG.md` | Registro de decisiones arquitectónicas |
| 4 | `50771b6` | `feat` | feat(protocol): materialize repository architecture decisions C-K | 126 | `protocol/`, `docs/`, `tools/`, `tests/` | Payload documental Clase B **sin bump de `VERSION`** (ver `## GAP declarado`) |
| 5 | `a70f1c6` | `docs` | docs(plans): close plan 127 repository artifact placement contract design | 127 | `docs/` | Registro de gobernanza |
| 6 | `0bc4e67` | `docs` | docs(placement): materialize repository artifact placement contract | 128 | `docs/`, `AGENTS.md` | Contrato de placement (DEV) |
| 7 | `4608176` | `docs` | docs(placement): close PC-1, PC-2 and PC-3 of the placement contract | 129 | `docs/` | Cierre de decisiones |
| 8 | `b888ad9` | `docs` | docs(plans): fix plan 129 decision identifiers to remove namespace collision | 130 | `docs/` | Corrección de identificadores |
| 9 | `65a1113` | `feat` | feat(runtime): implement the placement contract as a deterministic resolver | 131 | `runtime/`, `tests/`, `docs/` | Tooling DEV (el mensaje no cita el plan; ver `## GAP declarado`) |
| 10 | `35ef6d` | `docs` | docs(roadmap): update the roadmap to the real project state | 132 | `docs/`, `ROADMAP.md` | `ROADMAP.md` reconciliado |
| 11 | `c7ac44e` | `docs` | docs(dev): formalize roadmap impact and sweep documentation | 133 | `.agents/`, `docs/` | Policy DEV |
| 12 | `b007214` | `docs` | docs(plans): correct the plan 133 closure-state declaration | 133 (C-4) | `docs/` | Corrección de closure state |
| 13 | `f6884c5` | `fix` | fix(dev): correct closure evidence integrity and the C-2 contract | 134 | `.agents/`, `tools/`, `tests/`, `docs/` | Integridad de evidencia de cierre |
| 14 | `8489b89` | `docs` | docs(plans): close the plan 134 record and ground its closure state | 134 | `docs/` | Cierre del Plan 134 |
| 15 | `7c4fec3` | `feat` | feat(runtime): materialize supervised autonomous execution | 135 | `.agents/`, `runtime/`, `tests/`, `docs/` | SAE (DEV) |
| 16 | `f0d9c03` | `docs` | docs(plans): draft the plan 136 for the D01 mechanical checker | 136 | `docs/` | Redacción del Plan 136 |
| 17 | `3b94611` | `feat` | feat(tools): implement the D01 mechanical checker for discovery output | 136 | `tools/`, `tests/`, `ROADMAP.md`, `docs/` | Checker DEV |
| 18 | `1d0a536` | `docs` | docs(plans): record the human decision on F-3 (roadmap impact vs scope) | 136 | `docs/` | Decisión humana registrada |
| 19 | `c9cec35` | `docs` | docs(plans): resolve F-3 changes A and B independently | 136 | `docs/`, `ROADMAP.md` | Resolución de findings |
| 20 | `ebdbfad` | `docs` | docs(plans): draft the plan 137 for the EARS structural validator | 137 | `docs/`, `CHANGELOG.md` | Redacción del Plan 137 |
| 21 | `b11e4a3` | `docs` | docs(plans): draft the plan 138 for the SAE scope and authority hardening | 138 | `docs/`, `CHANGELOG.md` | Redacción del Plan 138 |
| 22 | `b0e37a5` | `feat` | feat(runtime): enforce SAE scope and authority before the effect | 138 | `.agents/`, `runtime/`, `tests/`, `docs/` | Endurecimiento de SAE (DEV) |
| 23 | `9998894` | `docs` | docs(plans): close the plan 138 record | 138 | `docs/` | Cierre del Plan 138 |
| 24 | `8727b60` | `docs` | docs(governance): close the SAE governance boundary decisions | 139 | `.agents/`, `tests/`, `docs/` | Cierre de decisiones |
| 25 | `3b0a321` | `docs` | docs(governance): close the governance residual inventory | 140 | `docs/`, `tests/`, `CHANGELOG.md` | Inventario de residuales |
| 26 | `73eed8c` | `docs` | docs(governance): resolve the human decision backlog HD-1..HD-12 | 141 | `docs/`, `tools/`, `tests/` | Resolución del backlog humano; abre RFC-79 |
| 27 | `923c32f` | `feat` | feat(protocol): materialize the payload normative residuals | **142** (RFC-79) | `protocol/` (16 archivos) + `VERSION` + runtime | **Produce `11.6.0` (MINOR)** |
| 28 | `5484763` | `fix` | fix(protocol): empty the remaining operational backlog | **143** | `protocol/` (2 archivos) + `VERSION` | **Produce `11.6.1` (PATCH)** |
| 29 | `6a433d1` | `docs` | docs(governance): correct the recorded test-count attribution | 143 (C-3) | `docs/` | Corrección de atribución |
| 30 | `f0171fa` | `docs` | docs(dev): resolve the DEV documentation and test hygiene backlog | 144 | `tests/`, `docs/`, `CHANGELOG.md` | Higiene documental y de tests |
| 31 | `a90e507` | `docs` | docs(plans): record the plan 144 closure checkpoint | 144 (C-1) | `docs/` | Checkpoint del Plan 144 |
| 32 | `c313122` | `fix` | fix(dev): close the actionable DEV backlog I-1..I-8 | 145 | `tests/`, `runtime/`, `conftest.py`, `.agents/`, `docs/` | Cierre del backlog accionable DEV |
| 33 | `a3efd41` | `docs` | docs(plans): record the plan 145 closure checkpoint | 145 (C-1) | `docs/` | Checkpoint del Plan 145 |

**Lectura de conjunto.** La línea es coherente y promocionable: 31 de los 33 commits son DEV-only (`docs/`, `tests/`, `runtime/`, `tools/`, `.agents/`) y exactamente **2** producen versión de protocolo (`923c32f` → 11.6.0 MINOR por RFC-79; `5484763` → 11.6.1 PATCH por el registro de taxonomía que la H13 regla 11 exige). Los commits 1–26 y 29–33 no tocan el payload salvo el commit 4, que se analiza como `GAP` en su propio apartado.

## Integridad de Git

- **`dev` contiene la historia esperada:** 33 commits lineales sobre `origin/dev`, todos registrados en `docs/plans/INDEX.md` o en el `CHANGELOG.md`; sin merges internos, sin force-push previo y sin ramas por feature.
- **`origin/dev` es el upstream correspondiente:** `dev` está configurado sobre `origin/dev` (`git branch -vv`: `[origin/dev: ahead 33]`) y el dry-run de push confirma `4aa2617..a3efd41 dev -> dev` sin rechazo.
- **`master` tiene una posición compatible:** `master` = `dc21458` es un **commit de merge** cuya segunda parent es `f85b558`, el tip de `dev` en la promoción anterior (`11.1.0`/`11.2.0`); su árbol es **idéntico** al árbol de ese merge-base.
- **No hay divergencia inesperada:** los 9 commits de `dev..master` son exactamente los commits de release históricos (`9cb448b`, `3a87ff1`, `75f591f`, `9d73799`, `98c8c8c`, `cac6bde`, `70a4736`, `2dfb99f`, `dc21458`), todos con su tag o con el tag de su batch.
- **La promoción no requiere reescritura.** El fast-forward **no** es posible (por diseño: `master` acumula merges de promoción además de la línea de `dev`), y la estrategia documentada del repositorio es el **merge** de `dev` sobre `master` (`docs/VERSIONING.md:4. Flujo por plan (playbook)`, paso 7: «merge `dev` → `master` y creación del **tag anotado** `X.Y.Z`»). Como el árbol de `master` es idéntico al del merge-base, el merge es contenido-trivial: su resultado es el árbol de `dev`, sin conflictos y sin merge artificial de contenido.
- **No hay cambios sin commit:** `git status --porcelain` no reporta ninguna modificación rastreada; el índice está limpio.
- **No hay tags incompatibles:** los tags 11.x existentes (`11.0.0`, `11.0.1`, `11.1.0`, `11.2.0`) tienen su sección `## [X.Y.Z]` en `CHANGELOG.md` y apuntan a `dc21458`; ninguno colisiona con el rango a publicar.

## VERSION

`protocol/.agents/VERSION` = **`11.6.1`**, y el ancla semántica del runtime (`runtime/toolcalls/canonical.py`, `PROTOCOL_VERSION`) vale **`11.6.1`**. Las dos fuentes de versión del protocolo coinciden; no hay una tercera.

Contraste contra `docs/VERSIONING.md:3. Versionado`:

- La versión se calcula siempre desde la **última versión publicada en `master`** (`11.2.0`) y la cadena de bumps por plan es `11.3.0` (plan 119, MINOR) → `11.4.0` (plan 120, MINOR) → `11.5.0` (plan 121, MINOR) → `11.6.0` (plan 142, MINOR) → `11.6.1` (plan 143, PATCH).
- `11.6.1` es PATCH porque la única modificación de payload del plan 143 es una **adición documental compatible** (el registro de taxonomía que la H13 regla 11 exige), declarada `Clase B` de RFC-56.
- Cada versión tiene su sección en `CHANGELOG.md`: `[11.6.1]` y `[11.6.0]` (2026-09-21), `[11.5.0]` y `[11.4.0]` (2026-09-14), `[11.3.0]` (2026-09-13).
- `11.6.1` **no** fue impuesto por este Plan: es la versión que el repositorio ya determinó en el commit `5484763` y que `docs/VERSIONING.md` §2/§3 hacen derivar de las reglas vigentes. Coincide con la expectativa del Change, y la coincidencia está verificada, no asumida.

No hay `VERSION` duplicado ni divergente: los únicos literales de versión de protocolo del repositorio son `protocol/.agents/VERSION` y `PROTOCOL_VERSION`, y `tools/check_version_state.py` los verifica en cada corrida de la batería.

## CHANGELOG

`CHANGELOG.md` representa correctamente el release:

- `[Unreleased]` está arriba (Keep a Changelog) y acumula los ítems de gobernanza/modelo no asignados a una versión, exactamente como manda `docs/VERSIONING.md:5. Changelog`.
- Las secciones de versión están en orden descendente y las cinco versiones no publicadas tienen su sección fechada con el ítem `(plan N, RFC-N)` que las produjo.
- No hay cambios inventados: cada ítem cita su plan y su RFC (o la vía por plan), y el contenido coincide con los commits 27 y 28 de la tabla anterior.
- **Corrección current-state aplicada por este Plan (§5 de VERSIONING):** las dos afirmaciones «Tag pendiente de promoción» de `[11.4.0]` y `[11.3.0]` quedaban contradichas por la promoción que este mismo Change ejecuta, de modo que se sustituyen por la constancia de que el tag se crea como entregable del release. Es la única corrección de `CHANGELOG.md` y se limita a esas dos frases; no se reescribe ningún ítem, ninguna fecha ni ningún contenido histórico.
- El único `GAP` detectado en esta superficie es ajeno al contenido del changelog y se registra abajo.

## Estado de Changes y Plans

Se verificaron los planes que forman realmente parte del conjunto promovido, no sólo por su número:

| Plan | Status | Executed | Closure / checkpoint | FAIL | ANOMALY | Blocker |
|---|---|---|---|---|---|---|
| 135 | `Executed` | sí | `Closed` (C-2 `VALID`) | no | no | no |
| 136 | `Executed` | sí | `Closed` (C-2 `VALID`; `F-1` transicionado a `resolved` por el Plan 143) | no | no | no |
| 137 | `Executed` | sí | `Closed` (ejecutado por el Plan 141; estado corriente reconciliado por el Plan 145) | no | no | no |
| 138 | `Executed` | sí | `Closed` (C-2 `VALID`) | no | no | no |
| 139 | `Executed` | sí | `Closed` (C-2 `VALID`) | no | no | no |
| 140 | `Executed` | sí | `Closed` (C-2 `VALID`) | no | no | no |
| 142 | `Executed` | sí | `Closed` con release pendiente; produce 11.6.0 | no | no | no |
| 143 | `Executed` | sí | `Closed` con release pendiente; produce 11.6.1 | no | no | no |
| 144 | `Executed` | sí | `Closed` (checkpoint registrado en `a90e507`) | no | no | no |
| 145 | `Executed` | sí | `Closed` (checkpoint registrado en `a3efd41`) | no | no | no |

Planes 141 y 131, también dentro del conjunto, están igualmente `Executed`. Ningún plan se reabrió, ninguna evidencia histórica se modificó y ninguna metadata de un artefacto cerrado se tocó en este Change: las únicas escrituras sobre artefactos existentes son las dos frases current-state de `CHANGELOG.md` y el snapshot §9 de `docs/VERSIONING.md`, ambas explícitamente determinadas por las reglas vigentes y necesarias para el release.

## Release gates

| Gate | Resultado | Evidencia |
|---|---|---|
| **RG-1 — Git integrity** | **PASS** | 33 commits lineales `origin/dev..dev`; `master` en `dc21458` = merge del tip de `dev` de la promoción anterior; árbol de `master` idéntico al merge-base; los 9 commits de `dev..master` son todos commits de release |
| **RG-2 — Working tree** | **PASS** (con nota declarada) | 0 modificaciones rastreadas y 0 staged. Nota: 1 archivo **untracked** `MASTER_PENDING_WORK_INVENTORY.md`, deliverable externo que se autodeclara no-artefacto del repositorio y que ya estaba presente en el baseline del Plan 145. No se toca, no se ignora y no se commitea |
| **RG-3 — Version** | **PASS** | `VERSION` = `PROTOCOL_VERSION` = `11.6.1`; cadena de bumps desde `11.2.0` conforme a VERSIONING §3; sección `[11.6.1]` presente |
| **RG-4 — Changelog** | **PASS** | Secciones descendentes, `[Unreleased]` arriba, ítems trazables, sin contenido inventado; dos afirmaciones «tag pendiente» corregidas por §5 |
| **RG-5 — Change lifecycle** | **PASS** | Planes 135–145 `Executed`; `I-1`…`I-8` resueltos; ningún plan cerrado reabierto |
| **RG-6 — Tests** | **PASS** | `python -m pytest tests/` → **1147 passed, 0 failed**; `python -m pytest protocol/.agents/harness/tests/ -q` → **109 passed**. La definición normativa de «verde» es la batería canónica local (`docs/VERSIONING.md:4.1 Batería canónica de verificación`), que pasa íntegra. El job de CI `check-protocol` está rojo por causas ambientales ajenas a este Change: ver `GAP-3` |
| **RG-7 — Canonical validation** | **PASS** | Seis checkers canónicos OK; C-1 `VALID=51, GAP=0, ANOMALY=0`; C-2 `VALID=50, GAP=1, ANOMALY=0` (el `GAP` histórico del Plan 116, conservado y no reabierto); C-3 `VALID=27, GAP=0, ANOMALY=0` |
| **RG-8 — Protocol integrity** | **PASS** | `git diff HEAD --name-only -- protocol/ dist/ ROADMAP.md docs/adr/` → vacío (0 diff); ningún archivo de `protocol/.agents/` se modifica en este Change |
| **RG-9 — Release artifacts** | **PASS** | `VERSION`, ancla `PROTOCOL_VERSION`, secciones del changelog, los planes 119/120/121/142/143 `Executed`, el workflow `publish-dist.yml` y la rama `dist` presentes y coherentes. Verificado en el estado publicado: `publish-dist` **completed / success** (run `35688773541`) con `origin/dist` = `c07abdd9ca50c459f7df5b075057f7b8d5f9762b`, y `python tools/check_dist_sync.py` sobre `master` → **«dist is in sync with protocol/»** |
| **RG-10 — Tag** | **PASS** | Convención real verificada: tag **anotado** con el nombre semver desnudo `X.Y.Z` sobre `master` (`docs/VERSIONING.md:6. Tags`). Ninguno de los cinco tags del rango existía antes de crearlo; los cinco se crearon sin conflicto y sin force-tag, todos apuntando al commit de promoción `8dbd92e0f006643412d21d562c5532be30f67647` (ver `## Verificación post-release`) |
| **RG-11 — Promotion topology** | **PASS** | Promoción por **merge** `dev` → `master` (playbook §4 paso 7), no destructiva; árbol de `master` idéntico al merge-base, de modo que el merge es contenido-trivial |
| **RG-12 — Release cleanliness** | **GAP declarado** | No hay blockers nuevos que impidan el release. Se declaran **3 GAP preexistentes / ambientales** (`GAP-1`, `GAP-2`, `GAP-3`) y **1 límite declarado** (GitHub Releases no es parte del mecanismo de este repositorio). Ver `## GAP declarado` |

Ningún `GAP` se convirtió en `PASS` por interpretación, y ningún resultado incierto se declaró `PASS`.

## Verificación completa (batería)

Ejecutada sobre el estado del Change, con `git` como fuente de verdad. Todos los valores son resultado real de los comandos, no expectativas del baseline.

```text
python tools/check_protocol_invariants.py --payload protocol .  -> OK (215 files, 10334 references)  PASS
python tools/check_plan_citations.py                            -> OK                                  PASS
python tools/check_plan_structure.py                            -> OK                                  PASS
python tools/check_taxonomy_coherence.py                        -> OK                                  PASS
python tools/check_session_artifacts.py                         -> OK                                  PASS
python tools/check_version_state.py                             -> OK (warnings de tags esperados en dev)  PASS
python -m pytest tests/ -q                                      -> 1147 passed, 0 failed              PASS
python -m pytest protocol/.agents/harness/tests/ -q             -> 109 passed                         PASS
python tools/check_lifecycle_anchor.py                          -> 145 planes: EXCLUDED=94, VALID=51, GAP=0, ANOMALY=0   VALID
python tools/check_lifecycle_checkpoint.py                      -> 145 planes: EXCLUDED=94, VALID=50, GAP=1, ANOMALY=0   VALID
python tools/check_lifecycle_lineage.py                         -> 145 planes: EXCLUDED=97, N/A=21, VALID=27, GAP=0, ANOMALY=0  VALID
python tools/check_ears_coverage.py                             -> N/A=1, VALID=3                     PASS
python tools/check_discovery_output.py                          -> N/A=1                             PASS
git diff HEAD --name-only -- protocol/ dist/ ROADMAP.md docs/adr/  -> vacío                          0 diff
git push --dry-run origin dev                                   -> 4aa2617..a3efd41 dev -> dev        OK
git push --dry-run origin master                                -> Everything up-to-date              OK
```

El `GAP` de C-2 es el histórico del Plan 116 (`HISTORICAL / NON-ACTIONABLE / RESOLVED` desde el Plan 143): se sigue emitiendo por contrato, es advisory y **no** se reabre ni se reinterpreta. No apareció ningún `FAIL`, `ERROR`, `BOUNDARY` ni `ANOMALY` nuevos.

Tres observaciones de la corrida, registradas y no convertidas en gates: (a) el conteo de referencias del checker de invariantes es 10334 frente a las 10256 del inventario externo del Plan 140, porque entre ambos estados entraron los planes 141–145 — es crecimiento esperado, no una anomalía; (b) `check_dist_sync.py` es local-only y se espera verde **sólo en `master`** (`docs/VERSIONING.md:4.1 Batería canónica de verificación`), de modo que se ejecutó sobre el estado publicado y pasó — ver `## Verificación post-release`; (c) el job de CI `check-protocol` está rojo por causas ambientales y preexistentes, registradas como `GAP-3` y **no** como `PASS`.

## GAP declarado

### `GAP-1` — un plan cerró una modificación de payload sin versión propia

- **Hecho.** El commit `50771b6` (plan 126, «materialize repository architecture decisions C-K») modificó cuatro archivos de `protocol/.agents/` —`harness/INDEX.md`, `roles/profiles/functional_writer.md`, `standards/runtime/PROTOCOL_HEALTH.md`, `standards/runtime/PROTOCOL_TAXONOMY.md`— y **no** hizo bump de `protocol/.agents/VERSION`. Su ítem está registrado bajo `[Unreleased]` en `CHANGELOG.md` y la versión pasó de `11.5.0` a `11.6.0` en el commit `923c32f` (plan 142).
- **Regla aplicable.** `docs/VERSIONING.md:3. Versionado` establece «cada plan ejecutado que toca `protocol/.agents/` … produce una versión propia» y «un plan = una versión = un tag», y reserva la exención de versión para los cambios **docs-only** que no tocan el payload (`RFC-69`, §3).
- **Determinación del propio plan.** El plan 126 es `Clase B` de RFC-56 y declara en su header `**Change Level:**` que su impacto de release es «ninguno (la materialización de payload es compatible y **no requiere tag**)». Es decir, la exención fue **declarada** por el artefacto que la ejecutó, no omitida en silencio.
- **Clasificación.** `GAP` — información de gobernanza incompleta respecto de la regla general, no contradicción interna del estado actual y no violación mecánica. **No** es `ANOMALY`: no hay dos datos contradictorios sobre el mismo hecho, sino una exención declarada que la regla general no contempla explícitamente. **No** es `FAIL`: ningún checker de la batería lo detecta ni lo sanciona, y el repositorio mantiene su invariante versión ↔ changelog ↔ tag para toda versión publicada.
- **Materialidad para este release: no bloqueante.** Este Plan publica `11.6.1`, cuya sección de changelog existe y cuyo tag se crea sobre `master`; el contenido de payload del plan 126 viaja dentro de la línea `11.6.x` y no altera ninguna versión publicada. El `GAP` no impide ninguna operación autorizada de este Plan.
- **Qué NO se hace.** No se resuelve, no se reinterpreta y no se reabre el plan 126 (artefacto cerrado; `Plan 146 §16` lo prohíbe). Tampoco se modifica `CHANGELOG.md` ni `VERSION` para "absorber" el ítem. Su resolución —si el mantenedor la quiere— exige un Change autorizado propio que re-adjudique la regla de versión por plan para ese artefacto cerrado; queda escalada, no silenciada.

### `GAP-2` — cita de plan ausente en un mensaje de commit

- **Hecho.** El commit `65a1113` («feat(runtime): implement the placement contract as a deterministic resolver») implementa el plan 131 y no cita el número de plan en el asunto, a diferencia del resto de la línea, que sí lo hace (Conventional Commits con `(plan N)`).
- **Clasificación.** `GAP` de trazabilidad **cosmético y no bloqueante**: el plan 131 existe, está `Executed` y su cierre está registrado; la asociación commit → plan se reconstruye desde `docs/plans/131-placement-contract-mechanical-implementation.md` y desde el índice.
- **Qué NO se hace.** No se reescribe el mensaje del commit (reescritura de historia, prohibida por este Plan). Queda registrado como observación.

### `GAP-3` — el job de CI `check-protocol` está rojo por causas ambientales

- **Hecho.** El job `check-protocol` (`.github/workflows/check-protocol.yml`) falla tanto en el push de `dev` (run `35688754598`) como en el de `master` (run `35688773540`) con **5 failed, 1142 passed**. Las cinco fallas son ambientales, no de contenido: (a) `actions/checkout@v4` corre con `fetch-depth: 1` —verificado en el log del run (`fetch-depth: 1`, `git fetch --no-tags … --depth=1`)—, de modo que los tests que resuelven identidades de árbol históricas o buscan commits en la historia no encuentran los objetos. Es el caso del test `test_real_repo_expected_classifications` de `tests/test_check_lifecycle_checkpoint.py` (C-1 con `ANOMALY=1` y C-2 con `GAP=27` por anclas irresolubles) y de los tests `test_the_roadmap_is_not_modified_by_this_change` y `test_no_protected_path_moved` de `tests/test_sae_scope_enforcement_dogfood.py` («the plan-138 commits are not in history»); y (b) el test `test_path_escaping_the_payload_is_rejected` de `tests/test_segment_resolution.py` falla en el runner Linux (`DID NOT RAISE SegmentResolutionError`) y pasa localmente en Windows — una diferencia de semántica de paths entre plataformas.
- **Preexistencia verificada.** Las dos fallas que ya existían el 2026-09-15 (run `35010230360`) son exactamente las mismas dos clases: el test `test_real_repo_expected_classifications` de `tests/test_check_lifecycle_checkpoint.py` y el test `test_path_escaping_the_payload_is_rejected` de `tests/test_segment_resolution.py`. El job está rojo en todas las corridas de `dev` visibles del historial de Actions, incluidas las de planes muy anteriores a este Change. Las tres fallas restantes corresponden a tests anclados que se incorporaron después de esa corrida (planes 136–138) y son de la misma clase: dependen de historia que el checkout shallow no trae.
- **Clasificación.** `GAP` ambiental **no bloqueante y no causado por este Change**. La definición normativa de «verde» del repositorio es la **batería canónica local** (`docs/VERSIONING.md:4.1 Batería canónica de verificación`), que pasa íntegra, incluido `python -m pytest tests/` con **1147 passed**. El propio repositorio documenta que no hay branch protection y que la mitigación aceptada es la batería local más el job de CI (`docs/VERSIONING.md:9. Estado actual (2026-09-21)`), de modo que el job no es el verificador normativo de este release.
- **Qué NO se hace.** No se modifica el workflow, ni los tests, ni `fetch-depth`, ni `docs/VERSIONING.md` §4.1 para hacer pasar el job: cambiar el verificador para que el gate pase está prohibido por este Plan. Tampoco se declara `PASS`: el job está rojo y así queda registrado. Su corrección —historia completa en el checkout y/o expectativa de path multiplataforma— requiere un Change autorizado propio, fuera del Scope de este Plan.

### Límite declarado — superficie de release

El **mecanismo oficial de publicación de releases de este repositorio** es el que define `docs/VERSIONING.md` (§1 ramas y roles, §6 tags, §10 Definition of Done): promover a `master` mediante merge, crear el **tag anotado** `X.Y.Z` sobre `master`, y dejar que el workflow `publish-dist` regenere `dist` desde `master`. Una versión está publicada cuando se cumplen esas tres condiciones. **GitHub Releases no forma parte de ese mecanismo:** el repositorio tiene **0** releases (`gh api repos/roldriel/ARgentOS/releases` → `0`), ningún workflow de release y ninguna mención a GitHub Releases en su documentación. Este Plan **no inventa** ese mecanismo: ejecuta el mecanismo documentado y registra aquí el límite, sin declarar ninguna publicación que no haya verificado.

## Release intent

Registrado **antes** de modificar cualquier referencia remota. Ninguna operación remota se ejecuta si el estado real deja de coincidir con este conjunto.

| Elemento | Valor |
|---|---|
| `dev` (SHA esperado) | `a3efd411d8923668f0cadf25636bc6c9d9602d09` |
| `origin/dev` (SHA esperado al inicio) | `4aa261774c034eba3bb6f4e51810513ce9e25933` |
| `master` (SHA esperado al inicio) | `dc21458c224cd60d9666c0026e79fc4fddd35fc8` |
| Merge-base esperado | `f85b558ea56b6e5fabcb7f12d9b5716f618a9428` |
| Versión | `11.6.1` |
| Rango no publicado a oficializar | `11.3.0`, `11.4.0`, `11.5.0`, `11.6.0`, `11.6.1` |
| Tag esperado del release | `11.6.1` (anotado, sobre el commit de promoción de `master`) |
| Árbol esperado tras la promoción | el árbol de `dev` en el commit de este Change (`master` no aporta contenido: su árbol es idéntico al merge-base) |
| Resultado de los gates | RG-1…RG-11 `PASS`; RG-12 con 3 `GAP` preexistentes/ambientales declarados (`GAP-1`, `GAP-2`, `GAP-3`) y 1 límite declarado; ningún `ANOMALY` |
| Operaciones previstas | push de `dev`; merge `dev` → `master`; push de `master`; creación y push de los tags anotados del rango |
| Resultado de la ejecución | **las cuatro operaciones se ejecutaron y se verificaron** — ver `## Ejecución del release` y `## Verificación post-release` |

**Por qué el release intent abarca cinco tags y no sólo `11.6.1`.** La convención real del repositorio no admite dejar versiones sin tag en `master`: `docs/VERSIONING.md` §2 invariante 1 exige que toda versión publicada tenga tag, §3 establece «un plan = una versión = un tag», y §10 enumera el tag anotado como condición de publicación. El precedente directo es la promoción anterior, que oficializó **dos** versiones en un solo commit de release (`dc21458` lleva los tags `11.1.0` y `11.2.0` y su mensaje dice «promote protocol 11.1.0-11.2.0»). Taggear sólo `11.6.1` dejaría `11.3.0`–`11.6.0` con sección de changelog, versión implementada y **sin** tag en `master`, rompiendo exactamente el invariante que RG-3/RG-4 verifican. La cadena `dev → origin/dev → master → tag 11.6.1` del Change se cumple íntegra; el rango completo es la lectura que la regla vigente impone.

## Ejecución del release

Secuencia autorizada y resultado real de cada paso:

1. **Push de `dev`** a su upstream. Sin force. → **OK**: `4aa2617..54171d8 dev -> dev`; tras el push, `origin/dev` = `54171d86…` = `dev` y `git rev-list --count origin/dev..dev` = **0**.
2. **Promoción a `master`** por merge de `dev`, revalidando antes `dev`, `master`, la ancestría y este release intent. Revalidación registrada justo antes del merge: `dev` = `54171d86…`, `master` = `dc21458c…`, merge-base = `f85b558e…`, árbol de `master` = `e76af36c…` = árbol del merge-base. Mensaje del commit de promoción siguiendo la convención existente: `release: promote protocol 11.3.0-11.6.1 (plans 119-121, 142, 143; RFCs 76-79)`. → **OK**: merge commit **`8dbd92e0f006643412d21d562c5532be30f67647`**, padres `dc21458` (master anterior) y `54171d8` (tip de `dev`), sin conflictos; árbol del merge = `bc280abdec836e2286562f2fe0390aef9bac81cc` = árbol de `dev`, exactamente el árbol esperado en el release intent.
3. **Push de `master`.** Sin force. → **OK**: `dc21458..8dbd92e master -> master`; `origin/master` = `8dbd92e0…`.
4. **Tags anotados** `11.3.0`, `11.4.0`, `11.5.0`, `11.6.0`, `11.6.1` sobre el commit de promoción, con el mensaje que cita la sección del changelog y los planes/RFC incluidos. Sin force-tag. → **OK**: cinco tag objects creados y empujados (`* [new tag]` × 5), los cinco apuntando a `8dbd92e0…`; los tags preexistentes `11.0.0`/`11.0.1`/`11.1.0`/`11.2.0` intactos.
5. **Regeneración de `dist`** por el workflow `publish-dist` (se dispara con el push a `master` que toca `protocol/`), verificada contra `origin/dist`. → **OK**: run `35688773541` **completed / success** (16 s); `origin/dist` pasó de `93f50b9` a `c07abdd9ca50c459f7df5b075057f7b8d5f9762b`; `python tools/check_dist_sync.py` sobre `master` → «dist is in sync with protocol/».
6. **Verificación post-release** de la cadena completa. → **OK**: ver `## Verificación post-release`.

Ninguna operación se ejecutó después de que el estado real dejara de coincidir con el release intent, y ninguna requirió force.

## Verificación post-release

Cadena completa `dev → origin/dev → master → tag 11.6.1 → release 11.6.1` verificada tras la publicación:

| Elemento | Valor verificado |
|---|---|
| `dev` | `54171d8637a922f65f86f36647e62829d42a73d5` |
| `origin/dev` | `54171d8637a922f65f86f36647e62829d42a73d5` (idéntico; `dev` no está adelante) |
| `master` | `8dbd92e0f006643412d21d562c5532be30f67647` |
| `origin/master` | `8dbd92e0f006643412d21d562c5532be30f67647` |
| Commit de promoción | `8dbd92e0f006643412d21d562c5532be30f67647` (merge de `dc21458` y `54171d8`), mensaje `release: promote protocol 11.3.0-11.6.1 (plans 119-121, 142, 143; RFCs 76-79)` |
| Árbol de `master` | `bc280abdec836e2286562f2fe0390aef9bac81cc` = árbol de `dev` |
| `dev` contenida en `master` | `git rev-list --count master..dev` = **0**: `master` contiene toda la historia de `dev` |
| Tag `11.3.0` | tag object `dd47e01f33f3eacd169901b0d05a8c501595ebe1` → `8dbd92e0f006643412d21d562c5532be30f67647` |
| Tag `11.4.0` | tag object `f67605241be0201941ec4c73fcce0f7a4803be9a` → `8dbd92e0f006643412d21d562c5532be30f67647` |
| Tag `11.5.0` | tag object `35371c3300ad5254cd63cfc5565a503a0b64e24f` → `8dbd92e0f006643412d21d562c5532be30f67647` |
| Tag `11.6.0` | tag object `905941a208c17035bef537e685bdc3d41b3a4056` → `8dbd92e0f006643412d21d562c5532be30f67647` |
| **Tag `11.6.1`** | tag object **`06022f31889b759143699aa4fc0c8475f8131c01`** → **`8dbd92e0f006643412d21d562c5532be30f67647`** |
| Tags preexistentes | `11.0.0`, `11.0.1`, `11.1.0`, `11.2.0` intactos (mismos objetos que antes de este Change) |
| `dist` | `c07abdd9ca50c459f7df5b075057f7b8d5f9762b` (`origin/dist` = `dist` local), regenerado por `publish-dist` desde `master` |
| `VERSION` | `11.6.1` (`protocol/.agents/VERSION`) y `PROTOCOL_VERSION` = `11.6.1` |
| `CHANGELOG` | secciones `[11.6.1]`, `[11.6.0]`, `[11.5.0]`, `[11.4.0]` y `[11.3.0]` presentes y ya con tag; ninguna afirmación «tag pendiente» |
| Working tree | `git status --porcelain` → sólo el artefacto externo untracked `MASTER_PENDING_WORK_INVENTORY.md` (0 modificaciones rastreadas) |
| CI del release | `publish-dist` **success** (`35688773541`); `check-protocol` **failure** (`35688773540` en `master`, `35688754598` en `dev`) por `GAP-3` |

La tabla se construyó con `git status`, `git branch -vv`, `git log`, `git rev-parse`, `git describe`, `git ls-remote --tags origin` y `gh run list`. Ninguna referencia remota quedó en un estado distinto del release intent, y `check_dist_sync.py` —el check que `docs/VERSIONING.md:4.1 Batería canónica de verificación` declara verde sólo en `master`— pasa sobre el estado publicado.

## Validation anchor

- **Declared scope:** las cuatro rutas de este Change — `CHANGELOG.md`, `docs/VERSIONING.md`, `docs/plans/146-release-promotion-11-6-1.md`, `docs/plans/INDEX.md`. No incluye ninguna ruta de `protocol/`, `dist/`, `ROADMAP.md`, `docs/adr/` ni `.agents/`.
- **Validation command-set:** los 7 comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `python -m pytest tests/`) + `python -m pytest protocol/.agents/harness/tests/` + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + los checkers específicos `tools/check_ears_coverage.py` y `tools/check_discovery_output.py` + los checks de release: `git status --porcelain`, `git rev-parse` de `dev`/`origin/dev`/`master`/`origin/dist`, `git merge-base`, `git ls-remote --tags origin`, `git push --dry-run` y la verificación de que ningún tag del rango existía antes de crearlo.
- **Effective inputs (repo content):** el scope declarado; `protocol/.agents/VERSION` y `runtime/toolcalls/canonical.py` (fuentes de versión); `CHANGELOG.md` completo (la superficie de versiones); `docs/plans/INDEX.md` y los planes 119–145; el payload de `protocol/.agents/` (215 archivos) como entrada del checker de invariantes; el estado Git de `dev`, `origin/dev`, `master`, `origin/master` y `origin/dist`; y `.github/workflows/publish-dist.yml` como definición del mecanismo de publicación.
- **Observed dependencies:** stdlib únicamente; el CLI `git` disponible; el CLI `gh` autenticado como `roldriel` con scope `repo` (verificado con `gh auth status`); conectividad con `https://github.com/roldriel/ARgentOS.git`, confirmada por `git ls-remote` y por los dry-run de push.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; pytest 9.0.3; repositorio bajo OneDrive (`C:\Users\rolda\OneDrive\Escritorio\Proyectos\ARgentOS`); `master` sin branch protection (decisión del owner registrada en `docs/VERSIONING.md:9. Estado actual (2026-09-21)`), de modo que el push no depende de rulesets server-side; la publicación de `dist` depende de que el runner de GitHub Actions y el token `DIST_PUSH_TOKEN` (o el `GITHUB_TOKEN` por defecto) funcionen.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `bc280abdec836e2286562f2fe0390aef9bac81cc` (`git rev-parse 54171d8637a922f65f86f36647e62829d42a73d5^{tree}`; idéntico al árbol del commit de promoción `8dbd92e0f006643412d21d562c5532be30f67647`, que es el árbol publicado).
  - **Delta scoped identity (scope S = las cuatro rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `db805eb222510f77929ed0c88eb42623d75328db87d23c6ee486a2f23b10064e` (`python tools/scoped_content_identity.py --ref 54171d8637a922f65f86f36647e62829d42a73d5 CHANGELOG.md docs/VERSIONING.md docs/plans/146-release-promotion-11-6-1.md docs/plans/INDEX.md`).
  - **Límite declarado:** las literales de identidad se transcriben en el commit de cierre una vez resuelto el SHA del commit del Change; esa transcripción es la única diferencia declarada entre el estado medido y el estado de cierre (convención anti-auto-referencia, precedente Planes 114/116/134/140/141/142/143/144/145).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/VERSIONING.md`, `docs/plans/146-release-promotion-11-6-1.md`, `docs/plans/INDEX.md`.
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

## Checkpoint / cierre

- **Commits de cierre:** dos (2) commits en `dev`, identificados por sus mensajes: (1) `docs(release): register the plan 146 release intent and release gates (plan 146)` —el Change de release: release intent, gates, corrección current-state del changelog y del snapshot de versiones y registro del Plan en el INDEX—, SHA `54171d8637a922f65f86f36647e62829d42a73d5`; (2) `docs(plans): record the plan 146 release checkpoint (plan 146, C-1)` —este registro de cierre, que añade la promoción, los tags, la publicación de `dist` y la verificación post-release. GC-1 admite el cierre multi-commit; los SHA y los tree id quedan como locators, no como identidad. El commit de promoción `8dbd92e0f006643412d21d562c5532be30f67647` vive en `master` —no es un commit de cierre de `dev`— y su árbol es idéntico al del commit (1).
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `db805eb222510f77929ed0c88eb42623d75328db87d23c6ee486a2f23b10064e` / `bc280abdec836e2286562f2fe0390aef9bac81cc`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** `bc280abdec836e2286562f2fe0390aef9bac81cc` (resuelto de `54171d8`; idéntico al árbol del commit de promoción `8dbd92e`). Es un hecho de Git y **no** la identidad del estado de cierre: el commit de cierre incluye governance (este registro), de modo que su árbol difiere legítimamente del estado validado.
- **Consistencia checkpoint↔anchor:** PASS — verificada por C-2 sobre el artefacto de este Plan en el estado de cierre.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 146 y su serie; `CHANGELOG.md` con el ítem `[Unreleased]` del Plan 146 y las dos constancias de tag; `docs/VERSIONING.md` §9 reconciliado en el punto de promoción; sin RFC nueva, sin ADR, sin cambio de payload, sin `VERSION` bump propio.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados: `docs/VERSIONING.md` §9 (snapshot de estado actual, reconciliado en el punto de promoción que la propia §5 declara) y `CHANGELOG.md` (las dos afirmaciones «tag pendiente» que la promoción vuelve falsas). `docs/plans/INDEX.md` registra el Plan y su serie. Nada más se modifica **por decisión**, no por omisión: las filas del INDEX de los planes 142 y 143 conservan su descripción de estado **al momento de su cierre** («payload con release pendiente»), que es exactamente el comportamiento que el repositorio ya mantiene para el plan 115 tras el release de `11.1.0`/`11.2.0` —su fila sigue diciendo «con release pendiente» y «sin tag, sin push, sin merge»—: el INDEX es un espejo descriptivo del cierre, nunca una segunda fuente de estado, y la autoridad del estado publicado es `git tag` + `protocol/.agents/VERSION` (`docs/VERSIONING.md:7. Estados de planes y RFCs` y `docs/VERSIONING.md:9. Estado actual (2026-09-21)`). Retocar esas filas retroactivamente sería reescribir la descripción histórica de un cierre ajeno a este Change.
- **Roadmap impact:** `NOT_REQUIRED` — razón explícita: `ROADMAP.md` no registra trabajo de release, promoción ni tag en ninguna de sus secciones (`## Trabajo activo / dogfood`, `## Pendientes que requieren autorización`, `## Candidatos futuros`, `## Trazabilidad histórica`, `## Proceso`), y este Change no altera el mapa operativo del trabajo futuro. `ROADMAP.md` queda con **0 diff**.
- **GAPs declarados:** `GAP-1` (ruleset de versión por plan del commit `50771b6`, exención declarada por el plan 126, no bloqueante, fuera de la autoridad de este Plan), `GAP-2` (cita de plan ausente en el mensaje de `65a1113`, cosmético, no bloqueante) y `GAP-3` (job de CI `check-protocol` rojo por checkout shallow y una expectativa de path no multiplataforma, ambiental y no bloqueante). Ninguno se convierte en `PASS` y ninguno se silencia.
- **Condición derivada:** `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor ∧ evidencia `PASS` para el estado de cierre. `Promoted` —merge `dev` → `master` verificado en `8dbd92e0f006643412d21d562c5532be30f67647`— y `Released` —tag inmutable `11.6.1` sobre ese commit, empujado a `origin`—, según `docs/VERSIONING.md:7. Estados de planes y RFCs`.

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia: la ejecución no detectó ningún defecto **propio** dentro del `Scope` que exigiera una corrección posterior a la verificación. Las tres observaciones que sí aparecieron (`GAP-1`, `GAP-2` y `GAP-3`) son condiciones **preexistentes o ambientales** de artefactos, commits y del job de CI, ajenas a este Change; se registran en `## GAP declarado` con su evidencia y su clasificación, y no se abren como findings de este Plan porque su resolución exigiría reabrir artefactos cerrados o cambiar el verificador, dos cosas que este Plan prohíbe.

### Correcciones

No findings detected / N/A — declaración de ausencia: no hubo corrección posterior a la verificación. Las dos correcciones documentales current-state (`CHANGELOG.md` §`[11.4.0]`/`[11.3.0]` y `docs/VERSIONING.md` §9) son parte de la ejecución normal del Change y están registradas en `## CHANGELOG` y en `## Documentation impact`, no como correcciones de un defecto verificado.

### Pending decisions

No se registran pending decisions nuevas. Este Change no abre ninguna decisión:

- la publicación de `dev`, la promoción a `master` y la creación de los tags no necesitan autoridad adicional: son exactamente lo que el mantenedor autorizó en el Change de origen;
- la corrección de las dos frases de tag y del snapshot §9 está determinada por `docs/VERSIONING.md` §5 y no cambia ninguna norma;
- `GAP-1` **no** se convierte en pending decision de este Plan: su resolución sería un Change autorizado propio sobre una regla de versionado de un artefacto cerrado, y este Plan no dispone de esa autoridad;
- `GAP-2` no requiere decisión: es una observación de trazabilidad cosmética cuya única corrección posible (reescribir el mensaje del commit) está prohibida aquí;
- `GAP-3` **no** se convierte en pending decision de este Plan: corregir el job de CI (historia completa en el checkout y/o expectativa de path multiplataforma) exige tocar el workflow y los tests, superficies fuera del `Scope` autorizado de este Change.

Las pending decisions que siguen abiertas en el repositorio (`<PLAN-125>:PC-1`/`PC-2`, `<PLAN-126>:PC-2`/`PC-3`, `<PLAN-131>:PC-1`/`PC-2`, `<PLAN-137>:PC-2`/`PC-3`, `<PLAN-138>:PC-2`, la materialidad ambiental de `<PLAN-122>`/`<PLAN-123>`) conservan su estado, su owner y su vía: ninguna está en el `Scope` de este Plan y este Plan no las resuelve por inferencia.

## Restricciones respetadas

- Ninguna modificación de `protocol/.agents/` ni de `protocol/_AGENTS.md`: **0 diff**. La promoción transporta payload ya autorizado, no lo edita.
- Ninguna RFC, ADR ni plan cerrado reabierto, reescrito o retransicionado.
- Ninguna reescritura de historia; ningún `git push --force`, `--force-with-lease` ni force-tag; ninguna operación destructiva.
- Ninguna autoridad, state machine, registry, Change mechanism, checker, metadata ni workflow nuevos.
- Ningún `FAIL`, `GAP` ni `ANOMALY` oculto: los tres `GAP` declarados son visibles en la tabla de gates y en su propio apartado.
- Ningún resultado incierto declarado `PASS`.
- `dist/` no se edita a mano: lo regenera el workflow.

## Resultado

**`RELEASED`.** El release `11.6.1` fue publicado y verificado por el mecanismo oficial del repositorio: `dev` publicado en su upstream, promovido a `master` por merge (`8dbd92e0f006643412d21d562c5532be30f67647`), con los tags anotados `11.3.0`–`11.6.1` sobre ese commit —incluido el tag del release, `11.6.1`— y `dist` regenerado por `publish-dist`, con `check_dist_sync.py` verde en `master`. La cadena completa `dev → origin/dev → master → tag 11.6.1 → release 11.6.1` está verificada en `## Verificación post-release`.

Estados finales, cada uno con su evidencia:

- **`Executed` = TRUE** — el Plan se ejecutó y se validó.
- **`Committed` = TRUE** — commits atómicos en `dev` (`54171d8` y este registro de cierre).
- **`Closed` = TRUE** — condición derivada: `Executed` + governance aplicada + checkpoint + consistencia checkpoint↔anchor.
- **`Promoted` = TRUE** — merge `dev` → `master` verificado.
- **`Released` = TRUE** — tag anotado `11.6.1` inmutable sobre el commit de promoción, empujado a `origin`, y `dist` regenerado desde `master`.

Tres `GAP` preexistentes/ambientales quedan declarados y **no** resueltos (`GAP-1`, `GAP-2`, `GAP-3`); ninguno bloquea el release y ninguno se declara `PASS`. **GitHub Releases** sigue siendo `N/A` como superficie del mecanismo de este repositorio (ver `### Límite declarado — superficie de release`): el release se publicó por el mecanismo documentado, no por un mecanismo inventado.

## Nota de ejecución

**Ejecutado el 2026-09-21** sobre el baseline `dev @ a3efd411d8923668f0cadf25636bc6c9d9602d09`, working tree sin modificaciones rastreadas salvo el artefacto externo untracked `MASTER_PENDING_WORK_INVENTORY.md`.

**Qué se hizo.** Se reconstruyeron los 33 commits de `origin/dev..dev` uno por uno desde Git (SHA, mensaje, tipo, plan, área y relación con el release) y se verificó que ninguno queda fuera de la línea de desarrollo. Se verificó la topología completa —`dev`, `origin/dev`, `master`, `origin/master`, `origin/dist`, merge-base, ancestría y la imposibilidad del fast-forward—, determinando que la estrategia documentada es el merge de promoción y que el árbol de `master` es idéntico al del merge-base, de modo que el merge es contenido-trivial. Se verificó la versión contra las reglas vigentes (`11.6.1`, con `PROTOCOL_VERSION` coincidente y sin fuentes duplicadas divergentes), el changelog (secciones, orden, trazabilidad, contenido no inventado) y el estado de los planes 135–145. Se corrió la batería canónica completa, el harness del protocolo, los gates C-1/C-2/C-3 y los checkers específicos de release. Se registró el release intent antes de tocar cualquier referencia remota. En la superficie documental se corrigieron las dos afirmaciones «Tag pendiente de promoción» que la propia promoción vuelve falsas y se reconcilió el snapshot de versiones `docs/VERSIONING.md` §9, que la §5 de esa política manda reconciliar exactamente en el punto de promoción; ambas son correcciones current-state determinadas por las reglas vigentes y acotadas a lo necesario. Se registró el Plan y su serie en `docs/plans/INDEX.md` y su ítem en `CHANGELOG.md`.

**Ejecución del release.** Con los gates satisfechos y el release intent registrado, se publicó `dev` (`4aa2617..54171d8`), se promovió a `master` por merge contenido-trivial (`8dbd92e`, árbol `bc280abd…` idéntico al de `dev`) y se empujó `master` (`dc21458..8dbd92e`). Se crearon y empujaron los cinco tags anotados del rango no publicado —`11.3.0`, `11.4.0`, `11.5.0`, `11.6.0` y `11.6.1`— sobre el commit de promoción. `publish-dist` regeneró `dist` (run `35688773541`, success; `origin/dist` = `c07abdd9…`) y `check_dist_sync.py` pasó sobre `master`. La cadena completa quedó verificada y el working tree quedó limpio (0 modificaciones rastreadas). No se usó force-push, force-tag ni ninguna operación destructiva, y `protocol/.agents/`, `ROADMAP.md` y `docs/adr/` quedaron con 0 diff propio de este Change.

**Observaciones registradas.** `GAP-1`: el plan 126 materializó cambios de payload sin bump de `VERSION`, con exención declarada por ese artefacto cerrado; no se resuelve ni se reabre. `GAP-2`: el commit `65a1113` (plan 131) no cita su plan en el asunto; no se reescribe el mensaje. `GAP-3`: el job de CI `check-protocol` está rojo por un checkout shallow (`fetch-depth: 1`) y una expectativa de path no multiplataforma; es preexistente, no lo causa este Change y no se toca el verificador para hacerlo pasar. Los tres quedan visibles y clasificados.

**Verificación.** Documentada completa en `## Verificación completa (batería)`, `## Ejecución del release` y `## Verificación post-release`, con los valores reales de cada comando.
