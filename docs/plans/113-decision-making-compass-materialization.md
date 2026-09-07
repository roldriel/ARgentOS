# Plan 113 — Materialización de la brújula de decisiones (Decision-Making Compass) en el AGENTS.md raíz

**Status:** Aprobado para ejecución
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

**Resultado (2026-09-07):** se completa al cerrar.

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

<!-- Se completa al validar (VC-1). V1 sobre el commit de contenido C1;
revalidación A2 sobre el estado final antes de `Closed`. -->

## Checkpoint / cierre

<!-- Se completa al cerrar (GC-1). -->

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

<!-- Se agrega al ejecutar (2026-09-07). -->
