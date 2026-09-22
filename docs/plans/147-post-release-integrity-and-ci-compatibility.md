# Plan 147 — Integridad post-release y compatibilidad de CI

**Status:** Executed
**Fecha:** 2026-09-22
**RFC:** — (vía plan; DEV-only sobre `tools/`, `tests/`, `runtime/toolcalls/`,
`.github/workflows/`, `.agents/policies/` y la documentación corriente; sin
efecto en `protocol/.agents/`, `protocol/_AGENTS.md` ni `dist`, por lo que
RFC-56 no aplica)
**Clase:** B
**Change Level:** L2 (coordinación 2: cuatro causas raíz independientes;
scope 2: cinco superficies DEV; impacto arquitectónico 0: ninguna decisión de
modelo, payload, autoridad, state machine ni mecanismo nuevo; impacto de
release 1: corrige `dev` después de la release `11.6.1` sin publicar una nueva;
duración/complejidad 2)
**Depende de:** plan 146 (Change de release cuyas cuatro fallas de CI este Plan
corrige); planes 98/134 (contratos de C-1/C-2); plan 121 (contrato de
resolución de segmentos)
**Origen:** ejecución de CI posterior a la release `11.6.1` — run
`35689196717` (`dev`, `7a9d393`: **4 failed, 1143 passed**) y run `35688773540`
(`master`, `8dbd92e`: **5 failed, 1142 passed**) —, más el `GAP-3` declarado por
el plan 146 (`.md:208-209`) y `<PLAN-146>:GAP-3`; autorizado por el mantenedor
como Change único de corrección post-release.

## Objetivo

Dejar `dev` corregido y reproducible: que las cuatro causas raíz que mantienen
rojo el job `check-protocol` queden reparadas en la causa y no en el síntoma, y
que la batería canónica y la batería de CI se ejecuten con el mismo contrato en
todas las plataformas.

El Change no reabre la release ni la promoción: no toca `master`, ni los tags
`11.3.0`–`11.6.1`, ni `dist`, ni ningún artefacto cerrado. Donde el defecto no
es corregible dentro de esa frontera, el Plan lo registra como hecho factual y
como pending decision en vez de inventar autoridad.

## Criterio de entrada

- [x] `dev` en `7a9d393`, árbol de trabajo sin modificaciones rastreadas
      (`git status --porcelain` → sólo `MASTER_PENDING_WORK_INVENTORY.md`
      untracked, artefacto externo declarado por el plan 146).
- [x] Las cuatro causas raíz reproducidas con evidencia factual antes de
      escribir código (§§ siguiente).
- [x] Contratos vigentes leídos: `tools/check_lifecycle_anchor.py` (C-1),
      `tools/check_lifecycle_checkpoint.py` (C-2),
      `runtime/toolcalls/segment_resolution.py`, `.github/workflows/check-protocol.yml`,
      `.agents/policies/lifecycle-checkers.md`.
- [x] Autorización del mantenedor para ejecutar el Change completo.

## Diagnóstico (causa raíz, no correlación)

### F1 — C-1 clasifica `ANOMALY` el artefacto del Plan 146 en `master`

**No es un problema de checkout superficial.** C-1 es un checker de texto puro
(sin git) y en `dev` clasifica el Plan 146 `VALID`. La diferencia es de
**contenido del árbol**:

- `master` = `8dbd92e`, merge de `dc21458` y `54171d8`.
- `7a9d393` (el commit de cierre del Plan 146, que transcribe los literales de
  identidad) **no es ancestro de `master`**: `git merge-base --is-ancestor
  7a9d393 8dbd92e` → exit 1.
- `git show 54171d8:docs/plans/146-release-promotion-11-6-1.md` difiere de
  `git show 7a9d393:…` en 74 inserciones / 28 borrados (los literales).

El árbol publicado con tag `11.6.1` contiene por tanto la revisión **previa** del
Plan 146, cuya `## Validation anchor` **difiere** los literales al checkpoint
(«resuelta sobre el árbol del commit de este Change — ver `## Checkpoint / cierre`»).

C-1 aplicaba R-C1-4 y traducía esa **ausencia declarada** en
`invalid State identity format` + `invalid Delta scoped identity format` →
`ANOMALY` → exit 1. Es un defecto de contrato del checker, no del artefacto: la
ausencia de evidencia es `GAP` (advisory) y solo la evidencia **presente y
contradictoria** es `ANOMALY` (`.agents/AGENTS.md` regla 7;
`.agents/policies/lifecycle-checkers.md`). La convención anti-auto-referencia
del corpus (plan 96 §13; precedentes 114/116/134/140–146) hace que esa forma sea
legítima, y el literal vive en el `## Checkpoint / cierre` del mismo artefacto.

### F2 — C-2 depende de objetos Git que el checkout superficial no trae

C-2 resuelve cada tree id declarado con
`git rev-parse --verify --quiet <sha>^{tree}` desde la resolución de árbol de
`tools/check_lifecycle_checkpoint.py`. Con `fetch-depth: 1`
sólo existe el commit de `HEAD`, así que las anclas históricas son irresolubles y
C-2 degrada a `GAP` en vez de verificar: run de CI → `VALID=25, GAP=27` (contra
`VALID=50, GAP=1` con historia completa). Reproducido localmente con un clon
superficial (véase `## Verificación`).

### F3 — Los dogfoods SAE leen commits históricos

Los dogfoods SAE `test_the_roadmap_is_not_modified_by_this_change` y
`test_no_protected_path_moved` de `tests/test_sae_scope_enforcement_dogfood.py`
ejecutan `git log --format=%H --grep=(plan 138)`. Con `fetch-depth: 1` la salida
es vacía y ambos tests fallan con «the plan-138 commits are not in history».
Misma familia y misma causa que F2: historia Git incompleta, no semántica del
checker.

### F4 — La resolución de segmentos acepta rutas fuera del payload

La resolución del payload en `runtime/toolcalls/segment_resolution.py` (la
función que deriva la ruta relativa del segmento) validaba con la
clase de path **nativa** (`Path`). En POSIX `Path("C:/Windows/x.md")` no es
absoluto y no tiene componente `..`, así que el guard no lo rechazaba: el test
`test_path_escaping_the_payload_is_rejected`
(`tests/test_segment_resolution.py`) fallaba en el runner Linux
(`DID NOT RAISE SegmentResolutionError`)
y pasaba en Windows. El veredicto dependía de la plataforma, que es exactamente
lo que un guard de contención no puede permitirse. En Windows ocurría lo
simétrico: `..\..\evil.md` no era traversal para la clase nativa hasta que se
reparseaba la ruta ya unida.

## Entregables

1. `runtime/toolcalls/segment_resolution.py` — guard de contención
   independiente de la plataforma.
2. `tools/check_lifecycle_anchor.py` — R-C1-4 distingue ausencia declarada
   (`GAP`) de valor presente e inválido (`ANOMALY`).
3. `.github/workflows/check-protocol.yml` — historia completa para el job.
4. `tests/test_segment_resolution.py` — matriz de regresión de traversal.
5. `tests/test_check_lifecycle_anchor.py` — regresiones de identidad diferida,
   valor malformado y divergencia con el árbol material.
6. `.agents/policies/lifecycle-checkers.md` — contrato de C-1 actualizado.
7. `docs/plans/147-post-release-integrity-and-ci-compatibility.md` — este Plan.
8. `docs/plans/INDEX.md` — registro del Plan y su serie.
9. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 147)`.
10. `docs/VERSIONING.md` §9 — reconciliación del snapshot corriente.

## Pasos

1. **WS-C — endurecer el resolver.** Validar el identificador entregado con
   semántica POSIX (`PurePosixPath`) en toda plataforma, rechazar el separador
   foráneo `\` y el identificador calificado por unidad (`C:`, `C:/`, `C:x`), y
   devolver `PurePosixPath` para que la ruta no se reparseе bajo reglas nativas.
   Preservar todos los casos válidos actuales.
2. **WS-A — corregir R-C1-4.** Clasificar la identidad diferida declarada como
   `GAP`; mantener `ANOMALY` para un valor presente que no cumple el formato.
   La discriminación es «el subcampo declara un valor tras su etiqueta», no la
   forma del token: un literal malformado tampoco trae hex, así que una prueba
   de ancho sola no separaría un valor inválido de una diferición legítima.
3. **WS-B — historia completa en CI.** `actions/checkout@v4` con
   `fetch-depth: 0` en `check-protocol.yml`, con la razón declarada en el
   workflow. No se debilita ningún checker ni se hace que un test detecte CI.
4. **WS-D — regresiones y documentación.** Matriz de traversal; regresiones de
   C-1; contrato de C-1 en `.agents/policies/lifecycle-checkers.md`; snapshot
   corriente en `docs/VERSIONING.md` §9; ítem de changelog; registro en el INDEX.
5. **Validación integral.** Batería canónica, `pytest tests/` completo, harness
   del producto, gates C-1/C-2/C-3, falsificación negativa y reproducción de las
   condiciones de CI (clon superficial vs historia completa; POSIX vs Windows).
6. **Checkpoint y cierre.** Ancla, checkpoint, determinaciones de impacto,
   status `Executed` y commit atómico en `dev`.

## Criterios de salida

- [x] C-1 clasifica el Plan 146 sin `ANOMALY` tanto en el árbol de `dev`
      (`VALID`) como en el árbol publicado de `master` (`GAP`), y C-1 conserva
      sus invariantes: `ANOMALY=0` sobre el corpus real.
- [x] C-2 y los dogfoods SAE pasan con la historia que el job ahora provee.
- [x] El test de path traversal pasa porque el resolver rechaza el escape, en
      POSIX y en Windows, con el mismo veredicto.
- [x] Ningún caso válido de resolución de segmentos queda roto.
- [x] `pytest tests/` completo verde; seis checkers canónicos exit 0.
- [x] Ningún Plan cerrado reescrito; ningún tag ni objeto histórico alterado;
      ninguna modificación fuera del scope declarado.

## Verificación

- Batería canónica completa (`docs/VERSIONING.md` §4.1): los seis checkers +
  `python -m pytest tests/`.
- `python -m pytest protocol/.agents/harness/tests/`.
- Gates de lifecycle: `tools/check_lifecycle_anchor.py` (C-1),
  `tools/check_lifecycle_checkpoint.py` (C-2),
  `tools/check_lifecycle_lineage.py` (C-3).
- Checkers específicos: `tools/check_ears_coverage.py`,
  `tools/check_discovery_output.py`.
- Reproducción de CI: clon superficial (`git clone --depth 1 --no-tags`) →
  fallos F2/F3 reproducidos; historia completa → verdes. POSIX real (WSL
  Ubuntu) → el guard rechaza `C:/Windows/x.md`.

## Riesgos

- **Falso positivo del guard:** rechazar una forma legítima del layout. Mitigado
  con la matriz de casos válidos (workflow, policy, rol, perfil, skill, rol
  anidado) y con el corpus de planes, que no cambia de clasificación.
- **Debilitar C-1:** aceptar un valor inválido. Mitigado con la falsificación
  explícita: un literal malformado sigue siendo `ANOMALY` incluso cuando el
  ancla también declara la diferición.
- **Dependencia accidental del workspace local:** que la solución verde en local
  no lo sea en CI. Mitigado reproduciendo el clon superficial y comparando los
  recuentos de clasificación de C-2.

## Trazabilidad

`<PLAN-146>:GAP-3` (job de CI rojo, declarado fuera del scope del plan 146) →
plan 147 → entregables 1–10. Los planes 98/134 fijan el contrato de C-1/C-2 y el
plan 121 el de resolución de segmentos; ninguno se modifica.

## Validation anchor

- **Declared scope:** las nueve rutas de código, configuración y documentación
  corriente que este Change modifica — `.agents/policies/lifecycle-checkers.md`,
  `.github/workflows/check-protocol.yml`, `CHANGELOG.md`, `docs/VERSIONING.md`,
  `docs/plans/INDEX.md`, `runtime/toolcalls/segment_resolution.py`,
  `tests/test_check_lifecycle_anchor.py`, `tests/test_segment_resolution.py` y
  `tools/check_lifecycle_anchor.py`. No incluye este artefacto de Plan (convención
  anti-auto-referencia: el scope se fija antes de escribir el cierre, de modo que
  la identidad del estado de cierre no puede cambiar por el propio registro), ni
  `protocol/.agents/`, `protocol/_AGENTS.md`, `dist/`, `master`, `ROADMAP.md`,
  `docs/adr/`, `docs/rfc/` ni ningún plan cerrado.
- **Validation command-set:** los 7 comandos de
  `docs/VERSIONING.md:4.1 Batería canónica de verificación`
  (`check_protocol_invariants --payload protocol .`, `check_plan_citations`,
  `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`,
  `check_version_state`, `python -m pytest tests/`) + `python -m pytest
  protocol/.agents/harness/tests/` + los gates `tools/check_lifecycle_anchor.py`
  (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y
  `tools/check_lifecycle_lineage.py` (C-3) + los checkers específicos
  `tools/check_ears_coverage.py` y `tools/check_discovery_output.py` + la
  falsificación negativa y la reproducción de CI descritas en
  `## Nota de ejecución`.
- **Effective inputs (repo content):** el scope declarado; los cuatro artefactos
  de diagnóstico (`tools/check_lifecycle_anchor.py`,
  `tools/check_lifecycle_checkpoint.py`, `runtime/toolcalls/segment_resolution.py`,
  `.github/workflows/check-protocol.yml`); el corpus completo de
  `docs/plans/*.md` (147 artefactos numerados) como población de C-1/C-2/C-3; los
  árboles Git de `dev` (`7a9d393`), `master` (`8dbd92e`) y `54171d8` como
  evidencia de la divergencia F1; y el corpus anclado de `tests/` que los gates
  ejecutan.
- **Observed dependencies:** stdlib únicamente; el CLI `git` disponible y con la
  historia completa del repositorio; pytest; el CLI `gh` autenticado como
  `roldriel` para leer los logs de los runs de CI; y WSL Ubuntu como intérprete
  POSIX real para verificar el veredicto del guard de segmentos. Sin red en los
  tests.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; pytest
  9.0.3; repositorio bajo OneDrive
  (`C:\Users\rolda\OneDrive\Escritorio\Proyectos\ARgentOS`); verificación POSIX en
  Ubuntu (WSL). El runner de CI es `ubuntu-latest` con Python 3.12.14, y esa
  diferencia de plataforma e intérprete es precisamente el factor que reveló F4
  y que la corrección vuelve irrelevante.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `d53e96231da30f74fb906c4fad6b853d8a9ddab8` (árbol del índice staged sobre el scope declarado, `git write-tree` vía `tools/scoped_content_identity.py`).
  - **Delta scoped identity (scope S = las nueve rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `ef53919418d4f69b01b0f23a375252a0c77fdff4b299fd1aef32007dad4f4d3d` (`python tools/scoped_content_identity.py` sobre las nueve rutas).
  - **Límite declarado:** el scope excluye deliberadamente este artefacto, de modo que la escritura del ancla y del checkpoint no altera la identidad del estado que el checkpoint certifica (convención anti-auto-referencia, precedente Planes 114/116/134/140–146).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `.agents/policies/lifecycle-checkers.md`, `.github/workflows/check-protocol.yml`, `CHANGELOG.md`, `docs/VERSIONING.md`, `docs/plans/INDEX.md`, `runtime/toolcalls/segment_resolution.py`, `tests/test_check_lifecycle_anchor.py`, `tests/test_segment_resolution.py`, `tools/check_lifecycle_anchor.py`.
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

## Checkpoint / cierre

- **Commits de cierre:** dos (2) commits en `dev`, identificados por sus
  mensajes: (1) `fix(dev): correct post-release integrity and CI compatibility
  (plan 147)` —el Change: el contrato de C-1, la historia completa del job, el
  guard de contención, sus regresiones y la documentación corriente—; (2)
  `docs(plans): record the plan 147 closure checkpoint (plan 147, C-1)` —este
  registro de cierre, que transcribe el SHA y el tree id del primero. GC-1 admite
  el cierre multi-commit; los SHA y los tree id quedan como locators, no como
  identidad (precedente: Planes 138, 144, 145 y 146).
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `ef53919418d4f69b01b0f23a375252a0c77fdff4b299fd1aef32007dad4f4d3d` / `d53e96231da30f74fb906c4fad6b853d8a9ddab8`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** registrado por el commit de cierre (2), que transcribe el SHA y el tree id del commit (1); no es la identidad del estado de cierre, porque el commit incluye governance (este registro) y su árbol puede diferir legítimamente del estado validado (RFC-75 `Mecanismo 7`).
- **Consistencia checkpoint↔anchor:** PASS — verificada por C-2 sobre el artefacto de este Plan en el estado de cierre (`VALID`, o `N/A` mientras el ancla no esté registrada; nunca `ANOMALY`).
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 147 y su serie; `CHANGELOG.md` con el ítem `[Unreleased]` del Plan 147; `docs/VERSIONING.md` §9 reconciliado (divergencia `dev`/`master` del cierre del Plan 146 y requisito de historia completa en CI); `.agents/policies/lifecycle-checkers.md` con el contrato de C-1 actualizado; sin RFC nueva, sin ADR, sin cambio de payload, sin `VERSION` bump propio, sin tag.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados: `.agents/policies/lifecycle-checkers.md` (contrato de C-1: identidad diferida vs. valor inválido), `docs/VERSIONING.md` §9 (snapshot corriente: la afirmación de que `dev` estaba contenido en `master` era falsa para el commit de cierre del Plan 146, y se declara el requisito de historia completa en CI) y `CHANGELOG.md` (ítem de corrección). `docs/plans/INDEX.md` registra el Plan y su serie. Nada más se modifica **por decisión**: el artefacto del Plan 146, su registro de cierre y el artefacto del Plan 134 son trazas históricas y no se reescriben para describir un estado que cambió después (RFC-46); su corrección se registra aquí por referencia.
- **Roadmap impact:** `NOT_REQUIRED` — razón explícita: este Change no crea, completa, cancela, reclasifica, re-prioriza ni re-dependencia trabajo del mapa operativo, ni mueve ningún ítem entre candidato / activo / bloqueado. Es una corrección técnica interna (contrato de un checker, configuración de CI, un guard de contención) más documentación corriente, sin cambio de scope de trabajo futuro. `ROADMAP.md` queda con **0 diff**.
- **GAPs declarados:** `GAP-1` — la divergencia `dev`/`master` sobre el commit de cierre del Plan 146 (`7a9d393`) **no se corrige** en este Change: nivelar `master` es una promoción y el scope autorizado la excluye expresamente. Queda registrada como hecho factual verificable en `docs/VERSIONING.md` §9 y como pending decision en `## Findings / Correcciones / Pending`. Ningún `GAP` se convierte en `PASS` ni se silencia.
- **Condición derivada:** `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor ∧ evidencia `PASS` para el estado de cierre. `Closed` (docs-only/corriente, sin release: el Change no toca `protocol/.agents/` y no requiere bump de `VERSION` ni tag, `docs/VERSIONING.md` §3). El commit atómico en `dev` es la acción de repositorio del mantenedor.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-147>:F-1` — estado: `resolved`; resolución: corregido por `<PLAN-147>:C-1` (la transición de estado la registra el mantenedor, CL-8); observación: C-1 clasificaba `ANOMALY` el artefacto del Plan 146 en el árbol publicado de `master` por una identidad diferida declarada, convirtiendo una ausencia de evidencia en contradicción; evidencia original: run de CI `35688773540` (`master`, `8dbd92e`) → `146-release-promotion-11-6-1.md: ANOMALY — invalid State identity format | invalid Delta scoped identity format`, `ANOMALY=1`, y `FAILED tests/test_check_lifecycle_anchor.py::test_real_repo_expected_classifications`; estado Git observado: `master` = `8dbd92e` (merge de `dc21458` y `54171d8`), `7a9d393` no ancestro de `master`; provenance original: `GAP-3` declarado en `docs/plans/146-release-promotion-11-6-1.md:## GAP declarado`.
- `<PLAN-147>:F-2` — estado: `resolved`; resolución: corregido por `<PLAN-147>:C-2`; observación: C-2 degradaba a `GAP` todas las anclas históricas en el checkout superficial del job de CI en lugar de verificarlas, y los dogfoods SAE anclados no encontraban los commits del Plan 138; evidencia original: run `35689196717` (`dev`, `7a9d393`) → `VALID=25, GAP=27` y `FAILED tests/test_sae_scope_enforcement_dogfood.py::test_the_roadmap_is_not_modified_by_this_change` + `::test_no_protected_path_moved` con «the plan-138 commits are not in history»; estado Git observado: checkout `--depth 1` del job; provenance original: `GAP-3` del plan 146 y `.github/workflows/check-protocol.yml`.
- `<PLAN-147>:F-3` — estado: `resolved`; resolución: corregido por `<PLAN-147>:C-3`; observación: el guard de contención de la resolución de segmentos aceptaba en POSIX un identificador calificado por unidad porque validaba con la clase de path nativa, de modo que el mismo contrato daba veredictos distintos por plataforma; evidencia original: run `35689196717` → `FAILED tests/test_segment_resolution.py::test_path_escaping_the_payload_is_rejected — Failed: DID NOT RAISE SegmentResolutionError`; estado Git observado: `dev` = `7a9d393`, `runtime/toolcalls/segment_resolution.py` previo a la corrección; provenance original: preexistente (run `35010230360`, 2026-09-15) y declarada en `docs/plans/146-release-promotion-11-6-1.md:## GAP declarado` como «diferencia de semántica de paths entre plataformas».

### Correcciones

- `<PLAN-147>:C-1` — refs origen: `<PLAN-147>:F-1`; alcance de revalidación: `tools/check_lifecycle_anchor.py` y `tests/test_check_lifecycle_anchor.py` (la identidad diferida declarada se clasifica `GAP`, con falsificación de que un valor presente e inválido sigue siendo `ANOMALY`); evidencia: C-1 sobre el árbol de `master` → `146-…: GAP` y `ANOMALY=0`; sobre el árbol de `dev` → `VALID`; `pytest tests/test_check_lifecycle_anchor.py` → 23 passed.
- `<PLAN-147>:C-2` — refs origen: `<PLAN-147>:F-2`; alcance de revalidación: `.github/workflows/check-protocol.yml` (historia completa en el job; ningún checker modificado); evidencia: clon superficial → 3 fallos reproducidos; clon con historia completa → los 4 tests anclados pasan.
- `<PLAN-147>:C-3` — refs origen: `<PLAN-147>:F-3`; alcance de revalidación: `runtime/toolcalls/segment_resolution.py` y `tests/test_segment_resolution.py` (matriz de traversal y de casos válidos); evidencia: `pytest tests/test_segment_resolution.py` → 56 passed; veredicto idéntico verificado en POSIX real (WSL Ubuntu) y en Windows.

### Pending decisions

- `<PLAN-147>:PC-1` — decisión: si se nivela `master` con el commit de cierre del Plan 146 (`7a9d393`), que hoy no es ancestro de `master`; blocking: no — el repositorio queda verificable y verde sin esa nivelación, y la divergencia está registrada como hecho factual; owner: mantenedor; escalación: resolverla exige una promoción (`dev` → `master`; `docs/VERSIONING.md:4. Flujo por plan (playbook)`, paso 7) y el scope autorizado de este Plan excluye expresamente `master`; resolución: pendiente; evidencia: `git merge-base --is-ancestor 7a9d393 master` → falso, `git rev-list --count master..dev` → 1, `docs/VERSIONING.md:9. Estado actual (2026-09-22)`. Consecuencia: el árbol publicado con tag `11.6.1` conserva la revisión previa del artefacto del Plan 146, cuya afirmación «`master` contiene toda la historia de `dev`» no se cumple para ese commit.

## Nota de ejecución

**Fecha:** 2026-09-22. **Ejecución:** completa dentro del scope autorizado; sin
releases, sin promoción, sin tocar `master`, tags ni `dist`.

**Diagnóstico (paso 0).** Las cuatro causas raíz se separaron antes de escribir
código. F1 **no** es un problema de checkout: C-1 es un checker de texto puro y
clasificaba `VALID` en `dev`; la diferencia era de contenido de árbol —
`master` = `8dbd92e` es el merge de `dc21458` y `54171d8`, y `7a9d393` (el
commit de cierre del Plan 146) **no es ancestro de `master`**
(`git merge-base --is-ancestor` → exit 1; el artefacto difiere en 74
inserciones y 28 borrados entre esas dos revisiones). F2 y F3 comparten causa
(historia Git incompleta) y se corrigieron una sola vez. F4 es un defecto
funcional real del guard, no una diferencia ambiental.

**Reproducción de CI (equivalencia).**

- Clon superficial (`git clone --depth 1 --no-tags`) → 1 commit; el test anclado
  de C-2 falla con `VALID=25, GAP=27` y los dos dogfoods SAE fallan con «the
  plan-138 commits are not in history»: los mismos tres fallos del run de CI.
- Historia completa (el mismo clon sin `--depth`, 285 commits) → los 4 tests
  anclados (incluida C-1) pasan.
- Árbol de `master` extraído con `git archive 8dbd92e` y los checkers
  corregidos: C-1 → `146-…: GAP`, `ANOMALY=0`, exit 0; C-2 → `GAP=27`,
  `ANOMALY=0`, exit 0 (los `GAP` de C-2 desaparecen con historia, como muestra
  el punto anterior). Comprueba que el fallo de `master` queda corregido sin
  tocar `master`.
- POSIX real (`wsl -d Ubuntu`, clase `PosixPath`):
  `Path("C:/Windows/x.md").is_absolute()` es `False` —la causa de F4— y el guard
  corregido rechaza los 10 identificadores de escape y acepta los 5 casos
  válidos, con los mismos veredictos que la suite en Windows.

**Batería ejecutada (todo verde).**

- Seis checkers canónicos: `check_protocol_invariants` (`--payload protocol .`),
  `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`,
  `check_session_artifacts`, `check_version_state` — exit 0.
- `python -m pytest tests/` → **1185 passed, 1 skipped**.
- `python -m pytest protocol/.agents/harness/tests/` → **109 passed**.
- Gates: C-1 `EXCLUDED=94, N/A=1, VALID=52, GAP=0, ANOMALY=0` (exit 0); C-2
  `VALID=51, GAP=1, ANOMALY=0` (el `GAP` histórico del Plan 116, conservado);
  C-3 `VALID=27, GAP=0, ANOMALY=0`.
- `check_ears_coverage.py` y `check_discovery_output.py` — exit 0.
- `check_dist_sync.py` no se ejecuta: es local-only y rojo en `dev` por diseño
  (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).

**Falsificación negativa.** Un literal de identidad malformado sigue siendo
`ANOMALY` aun cuando el ancla también declara el diferimiento
(`test_deferral_falsification_malformed_literal_is_still_anomaly`); los 12
identificadores de escape de la matriz de traversal se rechazan y los 8 casos
válidos se aceptan (`test_every_payload_escaping_identifier_is_rejected`,
`test_valid_payload_relative_identifiers_are_accepted`).

**Objetos históricos.** `master` = `8dbd92e`, `origin/master` = `8dbd92e`,
`dev` = `7a9d393`, `origin/dist` = `c07abdd` y los tags `11.3.0`
(`dd47e01f…`), `11.4.0` (`f6760524…`), `11.5.0` (`35371c33…`), `11.6.0`
(`905941a2…`) y `11.6.1` (`06022f31…`) conservan exactamente los objetos que
registró el Plan 146. Ningún force-push, force-tag ni reescritura de historia.

**Reporte de la release.** No se publica una nueva release. La corrección es
corriente (código y documentación DEV: `tools/`, `tests/`, `runtime/`,
`.github/`, `.agents/`, `docs/`), no toca `protocol/.agents/` y por lo tanto no
requiere bump de `VERSION` ni tag (`docs/VERSIONING.md` §3). Que el job de CI
quede verde en `dev` **no** arregla el árbol ya publicado: el artefacto del Plan
146 en `master` sigue en su revisión previa, y su nivelación es
`<PLAN-147>:PC-1`.
