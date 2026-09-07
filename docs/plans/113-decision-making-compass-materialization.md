# Plan 113 — Materialización de la brújula de decisiones (Decision-Making Compass) en el AGENTS.md raíz

**Status:** Executed (2026-09-07; materialización ejecutada y cerrada
docs-only)
**Fecha:** 2026-09-07
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-75
`Accepted` — Change Lifecycle DEV —, RFC-69 `Accepted` — cambio DEV docs-only
sin `VERSION` bump ni tag — y RFC-46 `Accepted` — trazas históricas —)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica)
**Change Level:** L1 — `Level = max(coordination, scope, architectural
impact, release impact, duration/complexity)` (RFC-75
`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`): coordinación 0
(1 agente, 1 sesión); scope 1 (un documento canónico — `AGENTS.md` raíz — más
los artefactos de registro del propio plan: este artifact,
`docs/plans/INDEX.md` y `CHANGELOG.md`); impacto arquitectónico 0 (sección de
principios en un documento existente; sin mecanismos, estados, registries,
checkers ni workflows); release impact 0 (docs-only RFC-69: ítem en
`[Unreleased]`, sin `VERSION` bump ni tag); duración 0 (< 1 sesión)
**Depende de:** RFC-75 `Accepted` + ADR-15/16 `Accepted` (Change Lifecycle
DEV); RFC-69 `Accepted` (docs-only sin release); Plan 104 `Executed`/`Closed`
(alineación documental) y Planes 105/106 `Executed`/`Closed` (arquitectura
terminológica y glosario: semántica no normativa de INDEX y Glossary que la
brújula nombra sin duplicar); batería canónica en verde
(`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
**Origen:** Decisión humana del mantenedor (2026-09-07, GO registrado en
`## Creación`): requerimiento «Materialize the Decision-Making Compass»,
conclusión conceptual de la retrospectiva reciente y del dogfooding de RFCs de
seis sesiones — ARgentOS no debe seguir creciendo por acumulación de
mecanismos/artefactos/estados/checkers/registries/ceremonia de gobernanza; el
objetivo es claridad y calidad de decisión. Condiciones expresas del
requerimiento: mínimo cambio durable; una declaración canónica sin
duplicación; sin RFC/ADR salvo que la gobernanza DEV lo exija (no lo exige);
sin mecanismo/estado/clase/registry/tracker/workflow/checker nuevo; boundary
DEV/Protocol preservada; batería del repo; reporte final de placement,
autoridad, principios, discoverability, cambios, validación y boundary
verification.

## Objetivo

Materializar la brújula de decisiones de ARgentOS — claridad sobre crecimiento;
separación de responsabilidades RFC/Plan/Git/INDEX/Glossary; calidad de
decisión sobre volumen documental; contención con «no change» como resultado
válido; y calidad de decisión como objetivo de evaluación — en el punto de
descubrimiento más temprano y ya autoritativo para agentes DEV (el `AGENTS.md`
raíz; `docs/AGENTS.md:Glosario y semántica de archivos AGENTS / INDEX /
ENTRYPOINT`), como una sección canónica de principios de juicio
explícitamente no normativa. El cambio no crea documento, mecanismo ni
autoridad nueva: declara principios y enruta a las autoridades existentes
(`docs/`), que no se duplican.

## Criterio de entrada

- [x] Branch `dev`; working tree limpio; HEAD
      `5ef221ef80da1fe7eede6035b762c5637138fd31` (2026-09-07; verificado
      contra git).
- [x] GO del mantenedor (2026-09-07) con alcance exacto: materializar la
      brújula en un único documento canónico existente (`AGENTS.md` raíz),
      con registros docs-only del plan; sin RFC/ADR; sin tocar
      `protocol/.agents/`, `runtime/`, `tools/`, `tests/`, `harness`,
      `dist/`, `VERSION`, `master`, tags, merge, push ni release.
- [x] Número libre: 113 (último plan registrado: 112, Cuadragésima cuarta
      serie, 2026-09-06); próxima serie libre: Cuadragésima quinta.
- [x] Inspección de duplicación/conflicto completada: no existe texto previo
      con significado equivalente (verificado con búsqueda textual sobre
      `AGENTS.md`, `.agents/`, `docs/` y `README.md`; sin resultados); RFC-75
      (`docs/rfc/75-change-lifecycle.md:Principios arquitectónicos` y
      `docs/rfc/75-change-lifecycle.md:Dev vs Protocol`) contiene principios
      de diseño del mecanismo del Change Lifecycle, materialmente distintos de
      una brújula conceptual de evolución; ADR-14
      (`docs/adr/14-implementation-priority.md`) es una decisión histórica de
      secuencia (D13), no un equivalente.
- [x] Ubicación determinable sin decisión humana pendiente: `AGENTS.md` raíz
      es el entrypoint de instrucción DEV (primera lectura obligatoria antes
      de `.agents/` y `docs/`;
      `docs/AGENTS.md:Glosario y semántica de archivos AGENTS / INDEX /
      ENTRYPOINT`; `README.md:Developing in this repository`), de clase
      EntryPoint/instrucciones; alojar ahí la sección no altera la carta
      documental (`docs/AGENTS.md:Folder → class map`) ni crea una fuente
      normativa nueva.
- [x] Batería canónica en verde al inicio (2026-09-07): checkers PASS
      (protocol invariants 212 files/9882 refs, plan citations, plan
      structure, taxonomy coherence, session artifacts, version state) y
      pytest `524 passed` (basetemp local
      `.pytest_cache\basetemp-baseline`).

## Entregables

1. `docs/plans/113-decision-making-compass-materialization.md` — este Plan.
2. `AGENTS.md` (raíz) — sección canónica `## Decision-Making Compass`
   (principios de juicio, explícitamente no normativos).
3. `docs/plans/INDEX.md` — Cuadragésima quinta serie + fila del Plan 113.
4. `CHANGELOG.md` — ítem `(plan 113)` en `[Unreleased]` (cierre; docs-only).

## Pasos

1. Verificar el estado del repo (paso 0; contra git, no contra INDEX) y la
   batería previa.
2. Registrar este artifact en `docs/plans/INDEX.md` (Cuadragésima quinta
   serie, status `Aprobado para ejecución`), sin ejecutar contenido.
3. Enmendar `AGENTS.md` raíz: insertar la sección `## Decision-Making
   Compass` entre `## Do NOT` y `## Development workflow`, con una declaración
   canónica única que preserve: (P1) claridad sobre crecimiento; (P2)
   separación de responsabilidades RFC/Plan/Git/INDEX/Glossary sin que una
   capa tome la responsabilidad de otra; (P3) calidad de decisión sobre
   volumen documental; (P4) contención («no change» como resultado válido; la
   primera pregunta es si el modelo existente expresa o resuelve la necesidad
   con suficiente claridad); (P5) calidad de decisión como objetivo de
   evaluación, sin afirmar que ARgentOS ya la demuestra. Redacción sin
   requisitos artificiales (sin MUST/MUST NOT nuevos), con terminología
   existente y sin duplicar definiciones normativas de `docs/`.
4. Validación V1 sobre el commit de contenido C1: batería canónica completa +
   juicios manuales (no duplicación; sin nueva terminología cross-layer; la
   sección no crea mecanismos ni altera la carta documental; boundary
   DEV/Protocol intacta). Registrar el Validation Anchor de este plan
   (anti-circularidad: antes de agregar los registros de cierre; ver
   `## Validation anchor`) y correr C-1.
5. Cierre: completar `## Checkpoint / cierre`, marcar el plan `Executed`
   (header + espejo en INDEX), agregar el ítem `(plan 113)` en
   `CHANGELOG.md:[Unreleased]` bajo `### Changed`; revalidación A2 sobre el
   estado final (batería + C-1/C-2/C-3) antes de derivar la condición
   `Closed` (docs-only, sin release; RFC-69); commits de contenido y de
   registro en `dev`.

## Criterios de salida

- [ ] `AGENTS.md` raíz contiene la sección `## Decision-Making Compass` con
      P1–P5 y su carácter no normativo declarado; sin lenguaje de requisitos
      artificiales.
- [ ] La declaración canónica vive en un único lugar; no hay documento nuevo,
      ni copia larga duplicada en `.agents/`, `docs/` o `README.md`.
- [ ] No se modificó `protocol/.agents/`, `runtime/`, `tools/`, `tests/`,
      `harness`, `dist/`, `protocol/.agents/VERSION` (11.0.0) ni documentos
      de gobernanza cerrados; sin RFC/ADR nuevo.
- [ ] Plan registrado en `docs/plans/INDEX.md`; ítem `(plan 113)` en
      `CHANGELOG.md:[Unreleased]`; sin `VERSION` bump ni tag (RFC-69).
- [ ] Batería canónica en verde; C-1/C-2/C-3 sin ANOMALY; `git diff --check`
      limpio; working tree limpio al final (commits atómicos en `dev`).

**Resultado (2026-09-07):** todos los criterios cumplidos; ver
`## Validation anchor`, `## Checkpoint / cierre` y `## Nota de ejecución`.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/ -q --basetemp <ruta-escribible>
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
git diff --cached --check
```

La batería canónica es la de `docs/VERSIONING.md:4.1 Batería canónica de
verificación`; los gates C-1/C-2/C-3 corren según
`.agents/policies/lifecycle-checkers.md:Where they run in the workflow`.
Juicios manuales: la sección no duplica autoridades normativas ni introduce
terminología cross-layer nueva; no altera la carta documental
(`docs/AGENTS.md:Folder → class map`); la boundary DEV/Protocol permanece
intacta (el payload no referencia `AGENTS.md` raíz ni `docs/`).

## Validation anchor

Registrado al validar el Plan 113 (2026-09-07). La validación **V1** corrió
sobre el estado del commit de contenido C1 (`6ff06f6`), **antes** de agregar
los registros de esta sección (anti-circularidad; precedente Planes 96–112).

- Declared scope: contenido del commit C1 del Plan 113 — `AGENTS.md` raíz
  (sección `## Decision-Making Compass`) — + batería canónica del repo
  (checkers dev + pytest, incluida la suite completa) sobre ese estado.
- Validation command-set:
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `python -m pytest tests/ -q --basetemp .pytest_cache\basetemp-v1` (V1)
  - `python -m pytest tests/ -q --basetemp .pytest_cache\basetemp-a2` (A2)
  - `python tools/check_lifecycle_anchor.py` (C-1),
    `python tools/check_lifecycle_checkpoint.py` (C-2),
    `python tools/check_lifecycle_lineage.py` (C-3)
  - `git diff --cached --check`
- Effective inputs (repo content): contenido completo del repo en el estado
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`,
  `runtime/` y la raíz; pytest consume `tests/` + `tools/` + `runtime/`);
  representado por el State identity (tree id).
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación
  en esta ejecución); el consumo por comando se observa de la documentación
  de cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica
  de verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 11.0.0 (sin tag, esperado en
  `dev`); pytest ejecutado con basetemp local `.pytest_cache\basetemp-*` por
  ACL del basetemp `pytest-of-rolda` (ruido ambiental documentado en planes
  96–112); los writes de index/objetos del `.git` del repo real (`git add`,
  `git commit`) se ejecutaron con aprobación por ACL de solo lectura del
  `.git` (ruido ambiental; no es intervención humana sobre el contenido del
  cambio); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `6fe6ec68ca909001b6376ce08989aa31ec2e9448` (verificado con
    `git rev-parse '6ff06f6^{tree}'` y con el generador vía `--ref 6ff06f6`).
  - Delta scoped identity (scope S = `AGENTS.md`; serialización `scoped-v1` +
    pares `path NUL blob NUL`, generada con
    `tools/scoped_content_identity.py`):
    `16ea77bdf3eece86c233083a366135c978bc8965644e75cad504390ec38449d5`.
    Par path → blob (C1): `AGENTS.md` →
    `bc0ce4adb9da8054b2bf282f2562be3e31678dfb`.
- Validity / stale: `vigente` (V1, estado de C1); **revalidada por A2**
  (2026-09-07: batería canónica completa + pytest + gates sobre el estado
  final, incluidos los registros de cierre) antes de `Closed` (ver
  `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (GC-1;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se completa el 2026-09-07 tras la
revalidación A2 sobre el estado final y antes del commit de registro de
cierre R2.

- Commits de cierre:
  - A `012c7f1` — `docs(plans): register plan 113 decision-making compass
    materialization (plan 113)` (registro del plan, status `Aprobado para
    ejecución`).
  - C1 `6ff06f6` — `docs: materialize decision-making compass in root
    AGENTS.md (plan 113)` (contenido autorizado, validado por V1).
  - R2 — este commit de registro/cierre (`docs(plans): close plan 113 with
    validation anchor and checkpoint (plan 113)`); su SHA se identifica por el
    mensaje y el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan — V1 sobre el estado de
  C1 (State identity T1 =
  `6fe6ec68ca909001b6376ce08989aa31ec2e9448`; Delta scoped identity =
  `16ea77bdf3eece86c233083a366135c978bc8965644e75cad504390ec38449d5`) y
  revalidación **A2** (2026-09-07) sobre el estado final de la ejecución
  (incluidos los registros de cierre).
- Estado de cierre: tree id del último commit de cierre (R2) =
  `git rev-parse R2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación A2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `R2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1
    (`6fe6ec68ca909001b6376ce08989aa31ec2e9448`) → **PASS**.
  - Estado final (R2): difiere del estado de C1 únicamente en los registros de
    cierre (este artifact, INDEX de planes y changelog); **revalidación A2**
    (batería canónica completa + pytest + gates sobre el contenido final,
    ejecutada antes del commit R2) → PASS. GC-1 queda satisfecho por
    revalidación antes de `Closed` (el checkpoint se evalúa contra A2, que
    cubre el estado de cierre).
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 113)` en `CHANGELOG.md:[Unreleased]`; docs-only, sin `VERSION` bump
  ni tag (RFC-69; `docs/VERSIONING.md:3. Versionado`).
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (A/C1/R2 en `dev`), `Closed` (condición derivada con checkpoint
  y consistencia), `Released` (no aplica: sin promoción a `master` ni tag;
  `dist` no se regenera).

## Findings / Correcciones / Pending

### Findings

- `No findings detected / N/A`

### Correcciones

- `N/A`

### Pending decisions

- `N/A` (la decisión humana fue provista por el mantenedor en el GO del Plan
  113; no quedan decisiones pendientes de este artifact)

## Riesgos

- Que la sección se lea como normativa o como requisito nuevo: mitigado por la
  declaración explícita de su naturaleza (principios de juicio; sin estados,
  clases, registries, checkers, workflows ni reglas nuevas) y por su ubicación
  en el archivo de instrucciones DEV, no en la normativa de `docs/`.
- Que duplique autoridades existentes: mitigado con inspección previa,
  redacción propia de alto nivel y alcance de un solo archivo.
- Que la brújula se interprete como aplicable al payload del Protocol: no
  aplica; el texto vive en el repositorio DEV (`AGENTS.md` raíz), no
  referencia `protocol/.agents/` y el payload no la referencia (boundary
  DEV/Protocol; `docs/rfc/75-change-lifecycle.md:Dev vs Protocol`).

## Trazabilidad

Decisión humana del mantenedor (2026-09-07, «Materialize the Decision-Making
Compass») + RFC-75/69/46 + ADR-15/16 + Planes 104–106 `Executed`/`Closed`
→ Plan 113 (materialización docs-only de la brújula) → `AGENTS.md` raíz +
INDEX + changelog.

## Creación

2026-09-07 — GO del mantenedor registrado (H1 = 1): autoriza exactamente el
alcance de este Plan (un documento canónico existente, registros docs-only),
sin RFC/ADR, sin mecanismos, sin tocar `protocol/.agents/`, `runtime/`,
`tools/`, `tests/`, `harness`, `dist/`, `VERSION`, `master`, tags, merge,
push ni release, y condicionando la detención ante cualquier necesidad
normativa nueva o conflicto con un RFC/ADR aceptado. Status inicial
`Aprobado para ejecución`; sin ejecución de contenido en esta etapa.

## Nota de ejecución

2026-09-07 — Ejecución completa del Plan 113 bajo el GO del mantenedor
(2026-09-07, H1 = 1; requerimiento «Materialize the Decision-Making
Compass»). Clasificación: origen = decisión humana del mantenedor; clase
RFC-56 = — (sin payload); Change Level = L1; dominio = documentación/
gobernanza DEV. Estado inicial: branch `dev`, HEAD
`5ef221ef80da1fe7eede6035b762c5637138fd31`, working tree limpio; batería
canónica en verde al inicio (checkers PASS; pytest `524 passed`).
Implementación (commit C1 `6ff06f6`, contenido validado por V1): sección
`## Decision-Making Compass` insertada en el `AGENTS.md` raíz entre
`## Do NOT` y `## Development workflow`, con los principios P1–P5 (claridad
sobre crecimiento; separación de responsabilidades RFC/Plan/Git/INDEX/
Glossary; calidad de decisión sobre volumen documental; contención con «no
change» como resultado válido; calidad de decisión como objetivo de
evaluación, sin afirmar que ARgentOS ya la demuestra), declarada
explícitamente como guía de juicio no normativa (sin estados, clases,
registries, checkers, workflows ni reglas nuevas), sin lenguaje MUST/MUST NOT
artificial, sin documento nuevo y sin duplicar autoridades de `docs/`.
Verificación: V1 sobre C1 (checkers canónicos PASS; pytest `524 passed`) y
revalidación A2 sobre el estado final antes del commit R2 (checkers PASS;
pytest `524 passed`; C-1 `VALID`, C-2 `VALID` — A2 declarado, GC-1 —, C-3
`N/A`; GAP=0, ANOMALY=0); `git diff --cached --check` limpio. Juicios
manuales: sin duplicación ni conflicto con RFC-75 (`Principios
arquitectónicos`, `Dev vs Protocol`), ADR-14 ni documentos existentes;
terminología existente usada sin definiciones duplicadas; carta documental
intacta; boundary DEV/Protocol intacta (el payload no referencia el
`AGENTS.md` raíz ni `docs/`). Registro/cierre: este artifact, espejo en
`docs/plans/INDEX.md` (status `Executed`) e ítem `(plan 113)` en
`CHANGELOG.md:[Unreleased]`; condición derivada `Closed` (docs-only, sin
release). Sin findings/corrections/pending (`N/A`). Sin cambios en
`protocol/.agents/` (`protocol/.agents/VERSION` 11.0.0), `runtime/`,
`tools/`, `tests/`, `harness`, `dist/`, `master` ni tags; sin push, sin merge,
sin tag.
