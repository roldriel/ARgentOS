# Plan 96 — Implementación de la Unidad B (Incrementos 1+3): anchors de validación, intake fallback, serie e identidad derivada; Git closure/checkpoint del Change Lifecycle DEV

> **Naturaleza de este documento.** Este es el **segundo Implementation Plan
> ejecutable** derivado del Master Action Plan 94. Implementa la **Unidad B =
> Incremento conceptual 1 + Incremento conceptual 3** de RFC-75 como una única
> unidad de ejecución planificada (el Incremento 3 **no se renumera ni se
> absorbe** dentro del 1; RFC-75 los agrupa porque el checkpoint necesita
> anchors para ser significativo). No implementa los Incrementos 2/4/5 ni
> rediseña RFC-75 o Plan 94: deriva, no reinterpreta
> (`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`).
> El cambio es **predominantemente documental** (gobernanza DEV, templates y
> registro), sin cambios en `protocol/.agents/`, `runtime/`, `tests/`,
> `tools/`, VERSION ni `dist/`; no produce `VERSION` bump ni tag (docs-only,
> RFC-69). **La presente iteración es solo de planificación**: crea este
> archivo y su registro en `docs/plans/INDEX.md`; no ejecuta el plan.

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-02
**RFC:** RFC-75 (`docs/rfc/75-change-lifecycle.md`)
**Clase:** — (no toca `protocol/.agents/`; cambio docs-only según
`docs/VERSIONING.md:3. Versionado`)
**Change Level:** L2 (clasificación prospectiva de dogfooding, declarada al
crear el plan; ver §26)
**Depende de:** RFC-75 `Accepted` (`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`);
ADR-15/16 `Accepted` (`docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`); RFC-56
`Accepted`; RFC-69 `Accepted`; Plan 94 `Executed` y commiteado (2026-09-02,
`3acf439`); Plan 95 `Executed` y commiteado (2026-09-02, `bc21978` + `865e3ad`
+ `dc7425f`); batería canónica en verde al cierre del estado verificado
(2026-09-02: `340 passed, 0 failed`).
**Origen:** Solicitud explícita del mantenedor (2026-09-02): preparar el
siguiente Plan de implementación del Change Lifecycle DEV — Incremento 1
(Validation Anchors, intake fallback, series/identidad derivada) + Incremento 3
(Git Closure/Checkpoint y relación closure↔estado Git) implementados como una
única unidad de ejecución — siguiendo la hoja de ruta ya aprobada en el Plan 94
(Unidad B) y el rollout incremental de RFC-75.

---

## Convención de evidencia

Este documento distingue, en cada conclusión importante, las marcas definidas
por el encargo y compatibles con la convención del repositorio
(`docs/CONVENTIONS.md:Convenciones`):

| Marca | Significado |
|---|---|
| `OBSERVED` | Verificado en el repositorio (git, archivos, checkers, pytest). |
| `NORMATIVE` | Impuesto por RFC `Accepted`, ADR `Accepted`, plan aprobado o convención vigente. |
| `DERIVED` | Deducción necesaria a partir de evidencia citada. |
| `PROPOSED` | Elección operativa de este plan (formato de campos, wording, algoritmo); no es normativa hasta ejecutarse. |
| `OPEN` | Decisión pendiente que no impide redactar el plan; requiere decisión humana o plan posterior. |
| `BLOCKER` | Contradicción que impide ejecutar la Unidad B (no se detectó ninguna; ver §39). |
| `UNKNOWN` | No verificable en el estado actual; se indica cómo resolverlo. |

Las afirmaciones sobre el estado actual se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`).

## Contenido requerido → sección

| Requisito del encargo | Sección de este documento |
|---|---|
| Executive Summary | §1 |
| Authority & Inputs | §2 |
| Current State | §3 |
| Problem Statement | §4 |
| Scope | §5 |
| Out of Scope | §6 |
| Increment 1 Scope | §7 |
| Increment 3 Scope | §8 |
| Semantic Model | §9 |
| Existing Mechanism Inventory | §10 |
| Reuse / Extension / New Mechanism Matrix | §11 |
| Anchor Model | §12 |
| Scoped Content Identity | §13 |
| Intake Fallback | §14 |
| Series Identity | §15 |
| Checkpoint Model | §16 |
| Closure Model | §17 |
| Anchor ↔ Checkpoint Consistency | §18 |
| Git Semantics | §19 |
| Legacy / Migration | §20 |
| Artifact Changes | §21 |
| Tool / Checker Changes | §22 |
| Test Strategy | §23 |
| Telemetry | §24 |
| Dogfooding | §25 |
| Change Level | §26 |
| DEV / Protocol Boundary | §27 |
| Skills Decision | §28 |
| State Machine Decision | §29 |
| Dependency Graph | §30 |
| Implementation Sequence | §31 |
| Rollback / Containment | §32 |
| Validation Matrix | §33 |
| Acceptance Criteria | §34 |
| Risks | §35 |
| Open Questions | §36 |
| Human Decisions | §37 |
| Adversarial Audit | §38 |
| Final Verdict | §39 |

---

## 1. Resumen ejecutivo

**[NORMATIVE + DERIVED]** RFC-75 está `Accepted` y define seis incrementos
conceptuales (0–5) con rollout `0 → {1,3} → 2 → 4`
(`docs/rfc/75-change-lifecycle.md:Rollout incremental`). El Plan 94 agrupa ese
rollout en unidades de implementación iniciales — A: Incremento 0; B: 1+3 en
batch operacional; C: 2; D: 4; Incremento 5 = Deferred / Future Track — y el
Plan 95 implementó la Unidad A (Incremento 0). Este plan implementa la
**Unidad B (Incrementos 1+3)** y es, por derivación, el **Plan 96** de la
serie de planes (`docs/plans/95-change-lifecycle-unit-a-increment-0.md:2. Naturaleza y distinción de rol`).

Objetivo operativo de la Unidad B:

1. **Incremento 1 — Validation Anchors (VC-1 operativo):** toda validación
   registrada queda anclable a un estado reproducible mediante campos de anchor
   (declared scope, validation command-set, effective inputs, observed
   dependencies, environmental factors, Scoped Content Identity) persistidos
   en el artifact que registra la validación (template de Plan, Nota de
   ejecución, Amendment Log de RFC).
2. **Incremento 1 — Intake fallback:** clasificación del cambio en el primer
   artifact (header de Plan con `Change Level`; header de RFC opcional cuando
   la RFC es el primer artifact; mensaje de commit para Clase C/L0), con L0
   provisional y triggers de upgrade, sin entidad `Change`.
3. **Incremento 1 — Serie:** identidad derivada de declaraciones `Serie:` +
   relaciones verificables (RFC↔Plan), sin registry ni entidad de serie;
   INDEX sigue siendo vista descriptiva.
4. **Incremento 3 — Git closure/checkpoint (GC-1 operativo):** el cierre de un
   Plan queda definido como condición derivada con checkpoint verificable
   (relación closure↔estado Git, no artifact); consistencia checkpoint↔anchor
   (scoped identity + factores) antes de `Closed`; multi-commit, multi-RFC,
   docs-only sin release; `Committed ≠ Closed ≠ Released`.

**[PROPOSED]** La ejecución es documental y aditiva sobre artifacts
existentes: `docs/plans/_TEMPLATE.md`, `docs/rfc/_TEMPLATE.md`,
`docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `AGENTS.md` raíz,
`docs/AGENTS.md`, más una entrada en el Amendment Log de RFC-75, el ítem
docs-only en `CHANGELOG.md:[Unreleased]` y el registro/espejo en
`docs/plans/INDEX.md`. No se crean checkers, tests, skills, entidades,
registries ni state machines (todo eso queda diferido a los Incrementos 2/4 y
al track 5). El propio Plan 96 es el primer dogfooding del mecanismo: declara
su Change Level, registra su validation anchor al ejecutar y registra su
checkpoint al cerrar (§25).

El plan concluye con veredicto `PLAN 96 READY FOR IMPLEMENTATION` (§39): no hay
BLOCKERs; las decisiones humanas de ejecución/cierre quedan tipadas en §37 y
no son ambigüedades de diseño.

## 2. Autoridad e insumos

**[NORMATIVE]** Se aplica ADR-16 sin modificación
(`docs/adr/16-change-lifecycle-authority.md:Decisión`):

| Clase | Fuente | Rol en esta Unidad |
|---|---|---|
| FACTUAL | Git, checkers, pytest, `protocol/.agents/VERSION`, tags | Verifica el estado (§3) y la validación (§33); nunca autoridad normativa |
| NORMATIVE | RFC-75 `Accepted`, ADR-15/16 `Accepted`, RFC-56 `Accepted`, RFC-69 `Accepted`, Plan 94 `Executed`, Plan 95 `Executed` | Fuente del contenido a materializar (semántica y mecanismos) |
| DECISION | Humano/mantenedor | Autoriza la ejecución, el commit atómico y el cierre (§37) |
| RELEASE | Tag en `master`, `dist` | No aplica: Unidad B docs-only, sin release (§19) |
| DESCRIPTIVE | INDEX | Registro/navegación; nunca autoridad (`docs/AGENTS.md:INDEX y CONVENTIONS`) |

Lecturas obligatorias verificadas para redactar este plan (todas citadas en el
texto):

1. `AGENTS.md` (raíz) — `## Task lifecycle`, `## Do NOT`.
2. `docs/AGENTS.md` — `### Identity`, `### INDEX y CONVENTIONS`.
3. `docs/CONVENTIONS.md` — `## Convenciones` y el bloque Change Lifecycle
   (`### Change Lifecycle DEV — alcance y frontera`, `### Change Lifecycle —
   Change Levels (modelo objetivo)`, `### Regla transversal — target semantics
   vs operationalización`).
4. `docs/VERSIONING.md` — `## 7. Estados de planes y RFCs`, `## 10. Definition
   of Done`, `## 11. Métricas del Change Lifecycle (observability schema
   baseline)`.
5. `docs/rfc/75-change-lifecycle.md` — completo (modelo, mecanismos 1/2/3/5/6/
   7/11/13/14/15, rollout, invariantes VC-1/GC-1).
6. `docs/adr/15-change-lifecycle-continuity.md` — CL-1..CL-10.
7. `docs/adr/16-change-lifecycle-authority.md` — AU-1..AU-7.
8. `docs/rfc/56-governance-fast-track.md` — clases A/B/C.
9. `docs/rfc/69-documentation-taxonomy-and-layout.md` — versionado docs-only,
   semántica de INDEX y referencias.
10. `docs/plans/94-change-lifecycle-master-action-plan.md` — en particular
    `## 18. Planificación incremental` (Unidad B) y `## 15. Estrategia de Git y
    checkpoints`.
11. `docs/plans/95-change-lifecycle-unit-a-increment-0.md` — precedente de
    estructura, registro y dogfooding de un Implementation Plan.
12. `docs/plans/INDEX.md` — numeración y series (Vigésima sexta y séptima).
13. `CHANGELOG.md` — `[Unreleased]`.
14. Precedentes citados por Plan 94: RFC-71..74, planes 86–93, ADR-01..16
    (usados como evidencia, no como fuente de decisión nueva).

Reglas que este plan preserva (AU-5, ADR-16):

- Un Plan implementa una decisión normativa y no la modifica silenciosamente.
  Este plan materializa mecanismos de RFC-75/Plan 94; cualquier desvío real se
  escala como OPEN/BLOCKER (§36, §37).
- El checker produce evidencia factual, no autoridad normativa
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).
- INDEX es descriptivo; se actualiza después de los archivos fuente.
- No se crea una autoridad nueva ni un registro de decisiones nuevo.

## 3. Estado actual del repositorio (reconstrucción factual)

**[OBSERVED]** Verificado con git, checkers y pytest al 2026-09-02:

| Dato | Valor observado |
|---|---|
| Branch | `dev` |
| HEAD | `dc7425f` (`docs(plans): record plan 95 OPEN-2 resolution (plan 95, RFC-75)`) |
| Working tree | limpio (verificado con `git status --short --branch`; solo warnings de ACL del `.config/git/ignore` del entorno, no del repo) |
| Respecto a `origin/dev` | ahead 6 (commits `c166520` ADR-15/16, `352ad18` RFC-75, `3acf439` plan 94, `bc21978` plan 95, `865e3ad` fix de test, `dc7425f` registro OPEN-2; sin push) |
| `protocol/.agents/VERSION` | `10.3.0` |
| RFC-75 | `Accepted` (2026-09-01; implementación incremental pendiente) |
| ADR-15/16 | `Accepted` (2026-08-31) |
| Plan 94 | `Executed` + commiteado (`3acf439`) |
| Plan 95 | `Executed` + commiteado (`bc21978` + `865e3ad` + `dc7425f`) |
| Checkers canónicos | PASS: `check_protocol_invariants.py` (212 files, 9720 refs), `check_plan_citations.py`, `check_plan_structure.py`, `check_taxonomy_coherence.py`, `check_session_artifacts.py`, `check_version_state.py` (warnings esperados de `dev`: secciones 3.7.0–3.15.0 sin tag) |
| pytest `tests/` | `340 passed, 0 failed` (ejecución con permisos fuera del sandbox; dentro del sandbox el basetemp `pytest-of-rolda` falla por ACL — `116 passed, 224 errors` de `PermissionError` ambiental, documentado en planes 94/95 como ruido del entorno, no defecto del repo) |
| `check_dist_sync.py` | local-only; se espera roja en `dev` por diseño (no corre) |
| `protocol/` | sin cambios (diff vacío contra HEAD) |
| Plan siguiente | `96` (último plan numerado: `95`; numeración por orden cronológico de ejecución, nunca se reusa) |
| Series del INDEX | Vigésima sexta (plan 94) y Vigésima séptima (plan 95) registradas |
| `CHANGELOG.md:[Unreleased]` | existe (actualmente entre `[10.0.0]` y `[9.1.0]`, orden histórico del archivo; ítems de planes 94/95 presentes) |

**[DERIVED]** Implicaciones para la ejecución de la Unidad B:

- No hay dependencia Git pendiente previa: planes 94/95 commiteados y OPEN-2
  resuelto (fix `865e3ad`), por lo que la batería reporta `340 passed,
  0 failed` y no existe desviación vigente aceptada.
- Los archivos objetivo de esta Unidad (`docs/CONVENTIONS.md`,
  `docs/VERSIONING.md`, `AGENTS.md`, `docs/AGENTS.md`, ambos templates,
  `CHANGELOG.md`) están limpios hoy; el único cambio de working tree previsto
  en esta iteración de planificación es este plan + su registro en INDEX.
- Ningún plan anterior lleva campos de anchor/checkpoint: son legacy por
  ausencia de campos, no inválidos (§20).

## 4. Declaración del problema

**[OBSERVED + DERIVED]** Tras la Unidad A (Incremento 0), la semántica del
Change Lifecycle DEV está escrita en las fuentes de verdad, pero los
mecanismos operativos de los Incrementos 1 y 3 siguen sin materializar:

1. **Validaciones sin anchor reproducible (VC-1 solo objetivo).** Las
   validaciones registradas en notas de ejecución y rondas de auditoría siguen
   sin campos de anchor; no existe formato, hogar ni regla operativa
   (`docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors`).
2. **Clasificación informal (intake).** Ningún artifact declara Change Level;
   el campo no existe en el template de Plan; no hay regla operativa de
   primer-artifact ni de triggers L0
   (`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`).
3. **Series sin verificación operativa.** La serie es solo semántica objetivo
   en `docs/AGENTS.md:Identity`; falta la regla operacional de declaración +
   relaciones (`docs/rfc/75-change-lifecycle.md:Mecanismo 11 — Series / Continuity`).
4. **Cierre sin checkpoint (GC-1 solo objetivo).** `Closed` sigue sin
   mecanismo: los planes 94/95 están `Executed` + commiteados sin checkpoint;
   la semántica escrita en `docs/VERSIONING.md:7. Estados de planes y RFCs`
   declara el checkpoint como futuro del Incremento 3
   (`docs/adr/15-change-lifecycle-continuity.md:Decisión`, CL-3/CL-4/CL-5).
5. **Dogfooding bloqueado.** Ningún plan puede registrar el primer anchor ni el
   primer checkpoint real hasta que existan los campos y la regla; sin esos
   datos no hay insumo para el gate de observabilidad del Incremento 4
   (`docs/plans/94-change-lifecycle-master-action-plan.md:17. Estrategia de telemetría`).

La pregunta que responde este plan:

> ¿Puede un agente implementador ejecutar la Unidad B (Incrementos 1+3) usando
> únicamente las autoridades y artifacts referenciados aquí, sin reinterpretar
> la arquitectura ni inventar decisiones?

Respuesta: sí (ver §39). Las decisiones humanas pendientes son gates de
ejecución/cierre ya tipados (§37), no ambigüedades de diseño.

## 5. Alcance

### 5.1 Incluido (esta iteración de planificación)

1. Crear `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md` (este
   documento), Status `Aprobado para ejecución`.
2. Registrar el plan 96 en `docs/plans/INDEX.md` (nueva serie + fila espejo,
   requisito estructural de `tools/check_plan_structure.py`).

### 5.2 Incluido (ejecución futura del plan; NO se ejecuta en esta iteración)

1. `docs/plans/_TEMPLATE.md` — campo `**Change Level:**` en el header y
   secciones `## Validation anchor` y `## Checkpoint / cierre` (§21, E3–E5).
2. `docs/rfc/_TEMPLATE.md` — campo opcional `**Change Level:**` (intake
   fallback) y guía de anchor por entrada del `## Amendment Log` (§21, E6–E7).
3. `docs/CONVENTIONS.md` — reglas operativas de intake/clasificación, anchor
   (VC-1), serie e identidad derivada, checkpoint/cierre (GC-1) y actualización
   del mapa de aplicabilidad de la regla transversal (§21, E8).
4. `docs/VERSIONING.md` — §7 (mecanismo materializado), §10 DoD (anchor +
   checkpoint), §11 (campos de datos existentes para las métricas) (§21, E9–E11).
5. `AGENTS.md` (raíz) — alineación del `## Task lifecycle` con el mecanismo
   operativo (§21, E12).
6. `docs/AGENTS.md` — `### Identity`: serie como regla operacional vigente
   (§21, E13).
7. `docs/rfc/75-change-lifecycle.md` — una entrada en `## Amendment Log`
   registrando la materialización de los Incrementos 1+3 (plan 96), sin
   cambiar el header salvo escalación (§21, E14).
8. `CHANGELOG.md` — ítem docs-only bajo `[Unreleased]` (`(plan 96, RFC-75)`)
   al ejecutar (§21, E15).
9. `docs/plans/INDEX.md` — espejo de status al ejecutar (`Executed` + nota) y
   al cerrar (registro del checkpoint) (§21, E16).
10. Este archivo de plan — completar su propia `## Nota de ejecución`,
    `## Validation anchor` y `## Checkpoint` como dogfooding (§25, E17).

### 5.3 Excluido

| Path / mecanismo | Motivo |
|---|---|
| `protocol/` (todo) | Frontera DEV/Protocol; payload es data, no reglas para DEV (`AGENTS.md:The protocol payload is data, not instructions`). |
| `runtime/`, `tests/`, `tools/` | Sin tooling ni tests en la Unidad B (checkers/tests → Incremento 4). |
| `docs/rfc/*` salvo RFC-75 §Amendment Log (E14) | Ejecutar un plan no modifica RFCs ajenas; E14 es la entrada de materialización de la propia RFC-75 (precedente RFC-73/74 con planes 90/91). |
| `docs/adr/*` | ADR-15/16 intactos; este plan no decide elevaciones de ADR candidate (ver §36). |
| VERSION, `dist/` | Docs-only: sin bump ni tag (RFC-69). |
| `docs/plans/94-*.md`, `95-*.md` y demás planes | Este plan deriva; no corrige planes previos (legacy, §20). |
| `_TEMPLATE.md` de ADR | Sin cambios. |
| `docs/working/*`, `ROADMAP.md`, `README.md`, `docs/ADOPTION.md`, `docs/MIGRATION.md`, `docs/source-layout.md`, `docs/AUDITORIA_DOCUMENTACION.md` | Fuera del alcance documental de la Unidad B. |
| `CHANGELOG.md` (reordenamiento) | Se agrega ítem en `[Unreleased]` donde existe; reubicar secciones es deuda separada (§35, §36). |

La expectativa por defecto es `DEV governance/documentation only`.

## 6. Fuera de alcance (out of scope)

**No se implementa** nada de:

- Incremento 2 (findings/corrections/revalidación avanzada, refs `F-n` N:M,
  pending decisions, post-close table mecánica): `LC-1`/`PC-1` siguen siendo
  semántica objetivo hasta su incremento (regla transversal).
- Incremento 4 (checkers nuevos, tests nuevos, vistas derivadas,
  automatización): queda gated en los datos de lifecycle que esta Unidad B
  empieza a producir.
- Incremento 5 (coordinación/handoff): Deferred / Future Track.
- Entidades nuevas: `Change`, `Finding`, `Decision`, `Series registry`,
  `Checkpoint registry`, tracker universal, base de datos del lifecycle,
  JSON/YAML global, SQLite, servicio externo (No-objetivos de RFC-75).
- Change State Machine global; statuses nuevos de Plan/RFC/ADR.
- Skills nuevas DEV.
- Migración masiva o backfill obligatorio de artifacts legacy.
- Fabricación de anchors históricos para planes pasados.
- Reescritura de historia (RFC-46): Amendment Logs, tags, notas históricas.

## 7. Alcance del Incremento 1 (conceptual)

**[NORMATIVE + DERIVED]** Según la Unidad B del Plan 94
(`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`):

| Campo | Contenido para este plan |
|---|---|
| Objetivo | Hacer anclable toda validación registrada (VC-1): campos de anchor (declared scope, command-set, effective inputs, observed dependencies, environmental factors, Scoped Content Identity) en el template de Plan y en el Amendment Log de RFC; regla de intake fallback y clasificación (Change Level en el primer artifact; L0 provisional con triggers; downgrade con justificación); serie como declaración + relaciones. |
| Problema que resuelve | Validaciones sin estado reproducible (G1); clasificación informal; series sin identidad verificable. |
| Mecanismos | Campos de anchor (formato v1, §12–13); regla de intake (§14); regla de serie (§15); texto normativo en CONVENTIONS/VERSIONING/AGENTS (E8–E13). |
| Dependencias | Incremento 0 (Unidad A) materializado; RFC-75/ADR-15/16 Accepted. |
| Migración | Legacy sin campos nuevos sigue válido; backfill opcional sin fabricar anchors. |
| Validación | Batería canónica + H13 por juicio + suite de escenarios (§23). |
| Dogfooding | Plan 96 registra el primer anchor real (§25). |
| Criterios de salida | Templates con campos de anchor/intake; reglas operativas en CONVENTIONS/VERSIONING; batería según política de "verde" (§34). |
| Rollback | Revertir commits; registros con campos nuevos pasan a legacy si se revierte. |

## 8. Alcance del Incremento 3 (conceptual, batch con 1)

**[NORMATIVE + DERIVED]** Ídem, según la Unidad B del Plan 94:

| Campo | Contenido para este plan |
|---|---|
| Objetivo | Materializar `Closed` como condición derivada con checkpoint verificable (GC-1): checkpoint ≠ anchor; consistencia (scoped identity + factores) antes de `Closed`; multi-commit/multi-RFC; docs-only se cierra sin release; semántica en DoD de VERSIONING. |
| Problema que resuelve | Planes `Executed` sin commit (87/92/93/91); cierre sin estado Git verificable. |
| Mecanismos | Campos/registro de checkpoint (§16); regla de consistencia (§18); semántica de Closed/rollback/tags (§17, §19). |
| Dependencias | Incremento 0 + Incremento 1 (mismo batch; el 3 no se renumera ni absorbe). |
| Migración | Planes legacy siguen `Executed` sin `Closed`; backfill opcional. |
| Validación | Batería + verificación de consistencia en el cierre del propio plan 96 (§25). |
| Dogfooding | Plan 96 registra el primer checkpoint real (§25). |
| Criterios de salida | `Closed` definido con checkpoint y consistencia; DoD actualizado; batería según §34. |
| Rollback | Revertir commits; registros con campos nuevos pasan a legacy. |

## 9. Modelo semántico: ya decidido vs a implementar vs diferido

### 9.1 Ya decidido (semántica normativa; no se rediseña)

Proveniente de RFC-75 (`docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors`,
`docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`) y ADR-15:

- Validation Anchor con declared scope, command-set, effective inputs,
  observed dependencies, environmental factors, Scoped Content Identity y
  validez relativa al anchor (CL-1/CL-2, VC-1).
- `anchor changed ≠ semantic validity changed`; revalidación o marca de stale
  como backstop; límite explícito de dependencias ambientales desconocidas.
- Checkpoint = relación closure↔estado Git verificable (no artifact);
  checkpoint ≠ anchor; consistencia checkpoint↔anchor antes de `Closed`
  (GC-1).
- `Committed` = estado del repositorio (CL-5), no status de Plan; commit SHA =
  locator, no identidad semántica; multi-commit; docs-only cierra sin release.
- Serie = identidad derivada (declaración + relaciones; AU-4), sin registry.

### 9.2 A implementar ahora (mecanismos operativos de este plan)

| Mecanismo | Dónde se materializa (§21) |
|---|---|
| Formato de campos de anchor (v1) | Template de Plan (E3–E5), guía en CONVENTIONS (E8) |
| Hogar de la validación registrada y su anchor | Plan (sección `## Validation anchor` / Nota de ejecución); RFC (`## Amendment Log` con anchor por ronda de auditoría) |
| Algoritmo de Scoped Content Identity (v1) | Regla operativa en CONVENTIONS (E8); ejemplo en §13 |
| Intake fallback / clasificación | Campo `Change Level` en template de Plan (E3) y opcional en template de RFC (E6); regla en CONVENTIONS (E8) |
| Serie operacional | Regla en CONVENTIONS (E8) + actualización de `docs/AGENTS.md:Identity` (E13) |
| Registro de checkpoint y condición `Closed` | Sección de cierre en template de Plan (E5); DoD de VERSIONING (E9–E11); regla en CONVENTIONS (E8) |
| Consistencia anchor↔checkpoint | Regla en CONVENTIONS (E8) + DoD (E9–E11) + verificación manual en dogfooding (§18, §25) |

### 9.3 Todavía diferido

Incremento 2 (findings/corrections/revalidación avanzada, refs calificadas,
pending decisions, tabla post-close mecánica), Incremento 4 (checkers y tests
automáticos, vistas), Incremento 5 (handoff/coordinación), tracker condicional,
métricas de coordinación, elevación de ADR candidates, telemetría avanzada.

## 10. Inventario de mecanismos existentes

**[OBSERVED]** Inventario verificado en el repo (ninguna capacidad se afirma si
no existe):

| Mecanismo / artifact | Ubicación | Rol actual |
|---|---|---|
| Planes de ejecución + `Nota de ejecución` | `docs/plans/NN-*.md` | Registro de implementación y validación por plan |
| Template de Plan | `docs/plans/_TEMPLATE.md` | Estructura obligatoria de todo plan nuevo |
| Template de RFC | `docs/rfc/_TEMPLATE.md` | Estructura de RFCs (header con `Serie:`; `## Amendment Log`) |
| Amendment Log de RFC | `docs/rfc/*.md` | Lineage semántico de cada RFC |
| INDEX de planes / RFCs / ADRs | `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md` | Registro/navegación descriptivos; mirror mecánico (planes) |
| Convenciones normativas | `docs/CONVENTIONS.md` | Reglas de gobernanza DEV |
| Política de versionado / DoD | `docs/VERSIONING.md` | §7 estados; §10 DoD; §11 schema de métricas |
| Taxonomía documental | `docs/AGENTS.md` | Clases, lifecycle, identidad, referencias |
| Entry point de desarrollo | `AGENTS.md` (raíz) | Reglas de workspace + task lifecycle |
| Changelog | `CHANGELOG.md` | Traza de cambios; `[Unreleased]` para docs-only |
| Checkers dev (batería) | `tools/check_*.py` | Evidencia factual re-ejecutable (estructura, citas, invariantes, taxonomía, sesiones, versión, dist) |
| Tests del repo | `tests/` (suite pytest) | Verificación de tools/runtime |
| Runtime de referencia | `runtime/` | Materialización del contexto (producto de referencia) |
| Git CLI (plumbing) | `git` | `check_dist_sync.py` usa `git ls-tree`/`rev-parse`; `check_version_state.py` lista tags; primitivas reutilizables para identidad de contenido |
| Contratos/session del producto | `protocol/.agents/contracts/SESSION_LOG.md`, `HARNESS_REPORT.md`, `METRICS.md`; `orchestrators/core/contracts/VERIFICATION_REPORT.md`, `EXECUTION_SUMMARY.md`; `harness/runner_state.py` (`state.json`) | Artefactos del Protocol (producto), no de DEV |
| Infraestructura de sesión del producto | `.project/` (efímero, gitignored) | Estado de sesión del harness; excluido de DEV |
| Modelos de identidad del producto | `runtime/toolcalls/identity.py`, `project_segment.py`; RFC-71 (`SegmentContentIdentity`) | Concepto de identidad de contenido en el producto; patrón transferible, no mecanismo DEV |
| Tracker de auditorías | `docs/working/audits/` | Patrón de findings con resolución (provenance histórica) |

## 11. Matriz reutilización / extensión / mecanismo nuevo

| Existing mechanism | Reusable? | Extension needed? | New mechanism? | Reason |
|---|---|---|---|---|
| Plan file + `Nota de ejecución` | Sí (hogar del registro) | Sí (formato de anchor y checkpoint) | No | RFC-75 Mecanismo 5/6/7; el registro vive en el artifact que posee la validación/cierre |
| `docs/plans/_TEMPLATE.md` | Sí (base estructural) | Sí (header `Change Level` + secciones anchor/checkpoint) | No | Todo plan nuevo nace del template (convención Plantillas) |
| `docs/rfc/_TEMPLATE.md` | Sí (base estructural) | Sí (campo opcional `Change Level` + guía de anchor en Amendment Log) | No | Intake fallback cuando la RFC es el primer artifact; rondas de auditoría ancladas (RFC-75 Mecanismo 3) |
| RFC header `Serie:` | Sí (declaración existente) | No (regla operativa) | No | La declaración ya existe; falta la regla de membresía verificable (Mecanismo 11) |
| INDEX (planes/RFCs/ADRs) | Sí (vista descriptiva) | Sí (registro del plan 96 y espejo) | No | INDEX = vista derivada; nunca autoridad (AU-4) |
| `docs/CONVENTIONS.md` | Sí (normativa) | Sí (reglas operativas VC-1/GC-1/intake/serie) | No | Hogar normativo de la gobernanza DEV |
| `docs/VERSIONING.md` | Sí | Sí (§7/§10/§11) | No | Semántica y DoD |
| `AGENTS.md` raíz / `docs/AGENTS.md` | Sí | Sí (wording operativo) | No | Entry point + taxonomía |
| `CHANGELOG.md` | Sí | Sí (ítem docs-only) | No | Traza obligatoria (RFC-69) |
| Checkers existentes (`check_*.py`) | Sí (batería) | No en esta Unidad | No | Enforcing de anchor/checkpoint → Incremento 4 (persist → observe → automate) |
| `pytest tests/` | Sí (batería) | No en esta Unidad | No | Tests automáticos de mecanismos → Incremento 4 |
| Git CLI (`ls-tree`, `rev-parse`, `hash-object`, `write-tree`, `ls-files`) | Sí (primitivas de identidad) | No (se usan como están) | No | Mecanismo v1 de Scoped Content Identity (§13) usa primitivas ya empleadas por los checkers |
| `SESSION_LOG`, `HARNESS_REPORT`, `VERIFICATION_REPORT`, `EXECUTION_SUMMARY`, `METRICS`, `state.json` (producto) | No como mecanismo DEV | — | No | Frontera DEV/Protocol (RFC-75 `Dev vs Protocol`); solo principios transferibles, no herencia de mecanismo |
| `.project/` session infra | No para DEV | — | No | Efímero del producto; DEV persiste en docs versionados |
| `runtime/toolcalls/identity.py` / RFC-71 `SegmentContentIdentity` | No como mecanismo DEV | — | No | Precedente conceptual de identidad de contenido; DEV define su propia identidad scoped sin compartir machinery |
| Serie del INDEX (Vigésima X serie) | Sí (vista de batches de planes) | Sí (nueva serie para plan 96) | No | Eje descriptivo de numeración; distinto de la serie conceptual `Serie:` (§15) |

Conclusión: **ningún mecanismo nuevo de infraestructura**; solo campos, reglas y
vistas sobre artifacts existentes (`docs/rfc/75-change-lifecycle.md:No-objetivos`,
`docs/plans/94-change-lifecycle-master-action-plan.md:12. Estrategia de Artifacts`).

## 12. Modelo de anchor (formato v1)

**[NORMATIVE + PROPOSED]** RFC-75 define los conceptos
(`docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors`); este plan
decide el formato de campos (autorizado: "CAN DECIDE IN PLAN — formato de
campos", `docs/rfc/75-change-lifecycle.md:Preguntas abiertas`).

### 12.1 Qué es una "validación registrada"

Regla operativa (se escribe en CONVENTIONS, E8): una **validación registrada**
es toda validación citada como evidencia en un artifact de gobernanza DEV
(resultado PASS/FAIL de checkers, pytest o juicio H13 en una Nota de ejecución,
en una ronda de auditoría de una RFC o en el cierre de un Plan). Toda
validación registrada lleva su **Validation Anchor** (VC-1) desde el Incremento
1. Las afirmaciones sin validación (p. ej., "se revisó por juicio") no exigen
anchor, pero si citan un resultado de ejecución lo son.

### 12.2 Campos del anchor (qué forma parte del anchor)

| Campo | Rol semántico | ¿Parte del anchor? | Ejemplo (plan 96) |
|---|---|---|---|
| Declared scope | Intención del autor sobre lo que la validación cubre | Sí | "Batería canónica del repo en el estado del plan 96" |
| Validation command-set | Comandos exactos ejecutados | Sí | `python tools/check_plan_citations.py` … |
| Effective inputs (repo content) | Contenido del repo que el command-set consume | Sí | Paths/globs consumidos por cada comando |
| Observed dependencies | Subconjunto de effective inputs confirmado por instrumentación | Sí (cuando existe; si no, `no instrumentado`) | "check_plan_citations consume `docs/plans/*.md`, `docs/rfc/*.md`, `docs/adr/*.md` y docs raíz (observado por scan del checker)" |
| Environmental factors | Inputs fuera del repo consumidos | Sí | Python 3.14, pytest, git, OS, flags, `protocol/.agents/VERSION` |
| Scoped Content Identity | Identidad semántica sobre effective inputs repo | Sí | `tree=<git tree id>` + delta `path→blob` (§13) |
| Validity / stale | Aplicabilidad actual del anchor | Sí (metadata del anchor) | `vigente` / `stale (motivo)` / `revalidada` |
| Fecha / autor / sesión | Cuándo y quién registró | No (metadata del registro) | 2026-09-02; agente implementador |
| Commit SHA del momento | Locator del estado, no identidad | No (locator; metadata) | `dc7425f…` (solo si aplica) |
| ID local del plan/RFC | Identidad del artifact que posee la validación | No (locator/ref calificada) | `plan 96` / `RFC-75` |

No se inventan campos: cada fila deriva de RFC-75 Mecanismo 6 (declared scope,
command-set, effective inputs, observed dependencies, environmental factors,
Scoped Content Identity, validity) o de la convención de refs del repo
(`ruta:sección`, `docs/CONVENTIONS.md:Convenciones`).

### 12.3 Hogar, productores y consumidores

| Pregunta | Respuesta |
|---|---|
| ¿Qué se persiste? | El bloque `Validation anchor` (con los campos de §12.2) en el artifact que registra la validación |
| ¿Dónde? | Plan: sección `## Validation anchor` del template (E3–E5) o dentro de la `## Nota de ejecución`; RFC: dentro de la entrada correspondiente del `## Amendment Log` (E6–E7) |
| ¿Quién lo produce? | El agente que ejecuta el Plan / registra la validación; el mantenedor si registra una decisión con validación |
| ¿Quién lo consume? | Agentes sucesores (continuidad), mantenedor, checkers futuros (Incremento 4), métricas (Incremento 4) |
| ¿Cómo se valida? | Manualmente en esta Unidad (reproducibilidad del identity, §23); mecánicamente en el Incremento 4 |

### 12.4 Validez relativa al anchor (CL-2)

- `anchor changed ≠ semantic validity changed`: si el estado cambia, se evalúa
  si la validación sigue aplicando; si aplica y no se revalida, la validación
  se marca `stale`; si se re-ejecuta, se registra un anchor nuevo (o se
  actualiza el existente con nota) y la validación queda `revalidada`.
- Límite declarado: dependencias ambientales desconocidas nunca detectadas no
  son verificables por el lifecycle; es responsabilidad del autor de la
  validación y la revalidación es el backstop (RFC-75 Mecanismo 6).

## 13. Scoped Content Identity (algoritmo v1)

**[PROPOSED]** Identidad semántica = función determinista del **contenido** de
los effective inputs repo, nunca del commit SHA (locator) ni del path solo.

### 13.1 Primitivas (git existente, sin código nuevo)

```text
git ls-files -s -- <path>          # blob id del contenido en el index (path en staged state)
git hash-object --path=<path> <path>  # blob id como se stagearía (para archivos nuevos/untracked)
git write-tree                     # tree id de todo el index (estado completo reproducible)
git rev-parse <commit>^{tree}      # tree id del estado commiteado
git ls-tree -r <commit> -- <paths> # blob ids por path en un commit
```

Estas primitivas ya son vocabulario del repo (`tools/check_dist_sync.py` usa
`git ls-tree`/`rev-parse`; `tools/check_version_state.py` lista tags).

### 13.2 Definición

Para una validación con scope set `S` (paths repo-relative, orden
lexicográfico estable):

1. **Precondición de reproducibilidad:** el working tree contiene solo los
   cambios del Plan sobre un HEAD conocido (verificado con `git status
   --porcelain`).
2. **Delta scoped identity:** para cada `p ∈ S` (ordenado), el blob id
   `b(p)` = `git ls-files -s` (tras `git add`) o `git hash-object --path=p p`
   para archivos sin stagear. Serialización canónica:
   `scoped-v1` + `p1\0b(p1)\0p2\0b(p2)\0…`; identidad = `sha256` de la
   serialización.
3. **State identity (cuando el command-set consume el repo completo, p. ej. la
   batería):** `git add` de todos los cambios intencionales + `git write-tree`
   → `tree=<tree id>`. El tree id es la identidad de contenido del estado
   completo (los tree objects de git son content-addressed: contenido igual →
   tree id igual, independiente de la historia).
4. El anchor registra ambos: `Delta scoped identity` (cambio relevante) y
   `State identity` (estado validado), cuando corresponda.

### 13.3 Semántica

| Situación | Resultado |
|---|---|
| Mismo contenido en S | Mismo delta identity y mismo tree id |
| Cambio de contenido relevante (en S) | Delta identity diferente |
| Cambio fuera de S | Delta identity igual; tree id puede cambiar → evaluación de aplicabilidad (CL-2), no invalidación automática |
| Rebase/cherry-pick/amend con contenido idéntico | Tree id y delta identity iguales → sin invalidación automática (RFC-75 Mecanismo 7) |
| Cambio de versión del payload (`protocol/.agents/VERSION` dentro de S) | Identity cambia → evaluar/revalidar |

### 13.4 Qué NO es identidad

- Commit SHA = locator (`docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`).
- Path solo (el path es locator físico).
- Lista de archivos sin contenido.
- Hash de un único archivo como si fuera del scope completo.

## 14. Intake fallback (regla operacional)

**[NORMATIVE + PROPOSED]** RFC-75 Mecanismo 1 decide que la clasificación se
registra en el primer artifact del cambio cuando no hay tracker. Este plan
operacionaliza:

### 14.1 Artifact reutilizado/extendido

- Se **extiende** `docs/plans/_TEMPLATE.md` con el campo `**Change Level:**`
  (header) y la guía de cómputo en su comentario (E3). El Plan es el primer
  artifact de la mayoría de los cambios planificados.
- Se **extiende** `docs/rfc/_TEMPLATE.md` con el campo **opcional**
  `**Change Level:**` para el caso en que la RFC es el primer artifact del
  cambio (intake fallback; E6).
- Se **reutilizan** los campos de header existentes: `Origen` (origen/tipo),
  `Clase` (RFC-56 cuando aplica), `RFC`, `Depende de`, `Serie`, y las secciones
  de scope/riesgo/coordinación del cuerpo del Plan.
- Para **Clase C / acción directa sin Plan**: la clasificación se registra en
  el mensaje de commit (convención existente de Conventional Commits +
  `(plan N, RFC-N)`) y/o en la Nota correspondiente.

No se crea un documento de intake nuevo, ni un tracker, ni una entidad
`Change`: el primer artifact del cambio es el hogar.

### 14.2 Regla (texto a escribir en CONVENTIONS, E8)

1. Todo cambio declara su clasificación en el primer artifact: origen/tipo
   (campo `Origen` o commit), clase RFC-56 cuando aplique (campo `Clase`),
   **Change Level** (campo nuevo), scope, RFCs/Plans afectados, riesgo y
   coordinación cuando existan secciones para ello.
2. `Level = max(coordination, scope, architectural impact, release impact,
   duration/complexity)` según RFC-75 Mecanismo 2; el número de commits no es
   dimensión; Change Level ≠ clase RFC-56 (ejes independientes).
3. **L0 es provisional:** al activarse un trigger (finding, revalidación
   requerida, decisión ADR-worthy, múltiples RFCs, impacto release-critical o
   arquitectónico) el Level se recomputa antes de continuar; si el cambio deja
   de ser L0, pasa por la vía de Plan correspondiente.
4. **Downgrade** con justificación documentada en el artifact que lo posee.
5. La clasificación es mutable (CL-10): upgrade obligatorio al descubrir
   complejidad; el campo se actualiza con nota.

## 15. Identidad de serie (regla operacional)

**[NORMATIVE + PROPOSED]** RFC-75 Mecanismo 11 y ADR-16 (AU-4):

### 15.1 Derivación

```text
Serie(RFC)  = declaración `Serie:` del header (canonical label)
Serie(Plan) = declaración `Serie:` del header SI existe
            ∪ { Serie(RFC) : Plan.RFC = RFC }   (derivación por relación)
INDEX       = vista derivada (nunca fuente de membresía)
```

- La membresía de una RFC es por declaración propia.
- La membresía de un Plan sin `Serie:` se deriva de la serie de su(s) RFC(s)
  referenciada(s) en el campo `RFC` (relación verificable); si referencia
  varias RFCs de series distintas, pertenece a todas.
- La coincidencia textual de un nombre aislado **no** basta: se exige la
  relación (RFC↔Plan) y la coherencia de los artifacts (campos resueltos,
  INDEX espejo).
- Sin entidad ni registry de series; sin IDs mutables; el label declarado es
  identidad (con historia en git/Amendment Log ante renombrados).

### 15.2 Casos

| Caso | Comportamiento |
|---|---|
| Serie sin release (docs-only) | Posible (p. ej., serie Change Lifecycle sin tag) |
| Multi-release | Posible (una serie puede cruzar releases) |
| Supersession de un miembro | La serie sobrevive; el miembro queda con su historia |
| Renombrado | Cambio de declaración con historia; las refs antiguas siguen resolviendo (identidad ≠ path, RFC-69) |
| Plan sin `Serie:` | Se deriva de su RFC (caso planes 94/95/96 → serie Change Lifecycle vía RFC-75) |
| Conflicto de declaraciones | detect → escalar → humano corrige (AU-3) |
| Proyectos distintos | La serie es repo-scoped: no hay namespace global; dos repos pueden declarar el mismo label sin colisión (no hay consumo cruzado) |
| Legacy sin `Serie:` | Ausencia = legacy; sin membresía derivable, no invalidez |

### 15.3 Distinción con las series del INDEX

Las secciones "Vigésima X serie" de `docs/plans/INDEX.md` son la vista
descriptiva de **batches de planes por numeración/registro**, un eje distinto
de la serie conceptual `Serie:` de RFC-75. Ambas conviven; ninguna es
autoritativa.

## 16. Modelo de checkpoint (registro de la relación, no artifact)

**[NORMATIVE + PROPOSED]** RFC-75: "checkpoint = relación closure↔estado Git
verificable (no artifact)" (`docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`).
Este plan materializa el **registro de esa relación** en el artifact de cierre
del Plan (sección `## Checkpoint / cierre` del template, E5; completada en la
Nota de ejecución al cerrar).

### 16.1 Campos del registro de checkpoint

| Campo | Contenido | Dato que proviene de |
|---|---|---|
| `Commits de cierre` | Lista de SHAs (C1…Cn) en `dev` que constituyen el Plan | Git (locators) |
| `Estado validado` | Anchor de la validación que soporta el cierre: ref calificada a la sección `## Validation anchor` + `State identity` (tree id) y `Delta scoped identity` | Validation anchor (§12–13) |
| `Estado de cierre` | Tree id del último commit de cierre (`git rev-parse C^{tree}`) | Git |
| `Consistencia` | Comparación: `State identity(cierre) == State identity(anchor)` ∧ factores ambientales declarados sin cambio; resultado + evidencia | Anchor + Git |
| `Gobernanza aplicada` | Checklist: Plan `Executed`, INDEX espejo, ítem changelog, Amendment Log de RFC(s) si corresponde, estado de VERSION | Artifacts de gobernanza |
| `Condición derivada` | `Closed` (docs-only sin release) o `Closed` con release pendiente; explícitamente `Committed ≠ Closed ≠ Released` | Derivación (§17) |

### 16.2 Respuestas a las preguntas del encargo

1. **Qué artifact registra el checkpoint:** el Plan (su sección de
   cierre/Nota), que ya es el artifact del closure; no existe artifact
   `Checkpoint`.
2. **Qué campos:** §16.1.
3. **Quién lo genera:** el agente que ejecuta el cierre, una vez que el commit
   atómico existe (o el mantenedor; §37); nunca antes del commit.
4. **Qué datos provienen de Git:** SHAs, tree id, diff del commit, estado de
   rama.
5. **Qué datos provienen del validation anchor:** scoped identity, factores
   ambientales, ref del anchor.
6. **Cómo se determina la consistencia:** comparación de tree ids + factores
   (§18).
7. **Cómo se detecta un checkpoint inválido:** §16.3.
8. **Si el repo cambia después:** el checkpoint queda válido para el estado que
   nombra; los cambios posteriores son acciones nuevas que referencian al
   cerrado (RFC-46; RFC-75 Mecanismo 12 — no se reescribe historia).
9. **Múltiples commits:** el registro lista C1…Cn; la consistencia se evalúa en
   el estado final (tree del último commit de cierre); ningún conteo de
   commits es condición de cierre.
10. **Múltiples RFCs:** la gobernanza aplica por RFC (Amendment Log de cada una
    cuando corresponda); el checkpoint no depende del número de RFCs.
11. **Múltiples Plans:** cada Plan cierra con su propio checkpoint; la serie se
    deriva y no centraliza checkpoints.
12. **Docs-only:** se cierra sin release (checkpoint igual; sin `Promoted`/
    `Released`).
13. **Closure sin release:** la condición derivada se registra como `Closed`
    (docs-only) y la ausencia de release es explícita.

### 16.3 Detección de checkpoint inválido (manual en esta Unidad)

- SHA de cierre que no resuelve en `git log` / no está en `dev`.
- Tree id de cierre ≠ tree id del anchor sin evidencia de revalidación.
- Factores ambientales declarados cambiados sin revalidación.
- Plan sin `Executed`, o governance incompleta (sin INDEX/changelog/Amendment
  Log cuando aplica).
- Anchor ausente o sin identity computable: GAP de evidencia; el cierre queda
  bloqueado hasta revalidar o evaluar (no invalida la validación misma).

La mecanización de estas detecciones es del Incremento 4 (§22).

## 17. Modelo de cierre (Closed)

**[NORMATIVE]** RFC-75 Mecanismo 5 y ADR-15 CL-3/4/5:

```text
Closed = Plan.status == Executed
       ∧ governance aplicable (matriz de governance)
       ∧ ∃ checkpoint registrado
       ∧ consistencia checkpoint↔anchor
```

- `Closed` es condición derivada; el status del Plan sigue siendo `Executed`;
  no hay status nuevo (`docs/VERSIONING.md:7. Estados de planes y RFCs`).
- `Closed ≠ Released`; un Plan docs-only se cierra sin release (RFC-69).
- `Closed` es terminal para ese Plan: un problema posterior genera artifacts
  nuevos que referencian al cerrado.
- Representación de "closure sin release": el registro de checkpoint declara
  `Condición derivada: Closed (docs-only, sin release)` y la cadena de
  implicación `Verified ⊆ Executed ⊆ Closed ⊆ Promoted ⊆ Released` queda con
  los eslabones finales ausentes por diseño.

Matriz de governance aplicable a este plan (docs-only + RFC-related):

| Regla | Aplica |
|---|---|
| documentación + INDEX (mirror) | siempre |
| checkpoint | siempre (GC-1, Incremento 3) |
| ítem changelog `[Unreleased]` `(plan 96, RFC-75)` | siempre (RFC-69) |
| Amendment Log de la RFC (RFC-75) | cuando corresponde (materialización) → E14 |
| VERSION bump / tag | no (docs-only) |

## 18. Consistencia anchor ↔ checkpoint

**[NORMATIVE]** Regla operativa (se escribe en CONVENTIONS, E8; se aplica en el
dogfooding del plan 96, §25):

```text
consistent(anchor, checkpoint) :=
    State identity del estado de cierre == State identity del anchor
    ∧ factores ambientales declarados del anchor sin cambio
```

- Si difiere cualquiera → **revalidación antes de `Closed`** (GC-1); no se
  declara cierre con diferencia sin revalidar.
- Factores irrelevantes (no consumidos) y factores desconocidos no invalidan
  automáticamente (CL-2/CL-10); un factor relevante consumido pero no declarado
  es anomalía auditable.
- Procedimiento de comparación (manual en esta Unidad):
  1. Reconstruir el anchor del cierre: ref a la sección `## Validation anchor`.
  2. `git rev-parse <ultimo-commit-de-cierre>^{tree}` → tree de cierre.
  3. Comparar contra el tree id registrado en el anchor.
  4. Re-ejecutar si difiere; registrar la revalidación con anchor nuevo.

## 19. Semántica Git

**[NORMATIVE + PROPOSED]** De RFC-75 Mecanismo 7 y ADR-15:

| Concepto | Regla |
|---|---|
| Secuencia de cierre | `implementation → validation → anchor → Git state (commit) → checkpoint → closure`; el commit **no** precede a la validación; `Executed` puede existir sin commit (CL-4); el cierre exige estado Git verificable (CL-3) |
| Commit SHA | Locator, no identidad semántica |
| Rebase/cherry-pick/amend | Contenido scoped idéntico (mismo tree id) → sin invalidación automática; contenido distinto → stale → revalidar |
| Múltiples commits | Permitidos; el registro de checkpoint lista todos |
| Rama | Todo en `dev`; sin ramas por feature (`AGENTS.md:Development workflow`) |
| Tags | Anotados, inmutables, solo en `master`; rollback = versión nueva, nunca reescribir tags |
| Working tree | Precondición de validación reproducible: solo los cambios del Plan sobre HEAD conocido |
| Commit de registro (C2) | Precedente `dc7425f`: los registros de cierre/resolución pueden committearse como commit de registro separado, con `(plan N, RFC-N)`, sin alterar el contenido validado (C1) — ver §25 |
| `Committed` | Estado del repositorio (CL-5), no status de Plan |

## 20. Legacy / migración

**[NORMATIVE]** RFC-75 Mecanismo 15:

- **No se migra nada obligatoriamente.** Planes 94/95 y anteriores, RFCs
  existentes (incluida RFC-75), ADR-01..16, validaciones históricas y sesiones
  pasadas permanecen como están.
- **Discriminador:** la ausencia de campos nuevos (anchor, checkpoint, Change
  Level) indica legacy, no invalidez. Un artifact legacy no se reescribe para
  cumplir metadata nueva.
- **Backfill opcional** (no parte de esta Unidad; decisión del mantenedor,
  §36/§37): relación G1, serie RFC-71..74, planes `Executed` sin commit.
  Prohibido fabricar anchors históricos no demostrables.
- **Plan en vuelo:** este plan 96 es el único plan en vuelo al momento de la
  Unidad B; adopta las reglas nuevas al ejecutarse (creado `Aprobado para
  ejecución` bajo el régimen previo y ejecutado bajo el régimen nuevo, con su
  Change Level declarado prospectivamente).
- **Exclusión de métricas:** legacy excluido del denominador; 0 registros =
  not applicable / insufficient sample, no "0% compliance"
  (`docs/VERSIONING.md:11. Métricas del Change Lifecycle (observability schema baseline)`).

## 21. Cambios de artifact (inventario exacto)

**[PROPOSED]** Cada fila especifica path, sección, cambio, autoridad y
validación. "Momento": `PLAN` = esta iteración (crear/registrar el plan);
`EJEC` = ejecución futura del plan.

| # | File (path exacto) | Sección | Cambio esperado | Why | Authority | Validation | Momento |
|---|---|---|---|---|---|---|---|
| E1 | `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md` | todo el archivo | Crear este Implementation Plan ejecutable (Unidad B) | Plan 96 es el siguiente plan legítimo de la serie (numeración cronológica; `docs/CONVENTIONS.md:Convenciones`); no puede reutilizarse un plan existente (uno por cambio, conservados como traza) | RFC-75; Plan 94 §18; solicitud del mantenedor | `check_plan_structure.py` (registro en INDEX), `check_plan_citations.py` | PLAN |
| E2 | `docs/plans/INDEX.md` | nueva sección "Vigésima octava serie" + fila | Registrar plan 96 con status y descripción | Mirror mecánico obligatorio de planes | `docs/AGENTS.md:INDEX y CONVENTIONS`; `tools/check_plan_structure.py` | `check_plan_structure.py` | PLAN (+ espejo EJEC) |
| E3 | `docs/plans/_TEMPLATE.md` | header + comentario inicial | Agregar campo `**Change Level:**` con guía de cómputo | Intake fallback: clasificación en el primer artifact (RFC-75 Mecanismo 1; Plan 94 Unidad B) | RFC-75 | structure/citations; uso en el próximo plan | EJEC |
| E4 | `docs/plans/_TEMPLATE.md` | nueva sección tras `## Verificación` | Agregar `## Validation anchor` con campos y guía | VC-1 operativo: hogar del anchor en todo plan nuevo | RFC-75 Mecanismo 6; ADR-15 CL-1 | structure/citations | EJEC |
| E5 | `docs/plans/_TEMPLATE.md` | nueva sección tras `## Validation anchor` | Agregar `## Checkpoint / cierre` con campos y guía | GC-1 operativo: registro del checkpoint en todo plan que cierra | RFC-75 Mecanismo 7; ADR-15 CL-3 | structure/citations | EJEC |
| E6 | `docs/rfc/_TEMPLATE.md` | header | Agregar campo opcional `**Change Level:**` (solo si la RFC es el primer artifact del cambio) | Intake fallback para cambios RFC-first | RFC-75 Mecanismo 1 | structure/citations | EJEC |
| E7 | `docs/rfc/_TEMPLATE.md` | `## Amendment Log` | Guía: entradas que registran rondas de auditoría/validación llevan anchor (scope, command-set, inputs, factores, identity) | Rondas de auditoría son validaciones registradas (RFC-75 Mecanismo 3, CL-1/CL-2) | RFC-75 Mecanismo 3 | structure/citations | EJEC |
| E8 | `docs/CONVENTIONS.md` | bloque Change Lifecycle (tras `### Change Lifecycle — Change Levels (modelo objetivo)` y `### Regla transversal`) | Agregar subsecciones operativas: `Intake y clasificación`, `Validation anchors (VC-1)`, `Serie e identidad derivada`, `Checkpoint y cierre Git (GC-1)`; actualizar el mapa de aplicabilidad de la regla transversal y la frase de clasificación operacional | Materializa las reglas de RFC-75 en la normativa DEV (hogar único) | RFC-75 Mecanismos 1/5/6/7/11; ADR-15/16 | `check_plan_citations.py` (refs), revisión H13/juicio | EJEC |
| E9 | `docs/VERSIONING.md` | `## 7. Estados de planes y RFCs` | Sustituir el párrafo "hasta entonces el cierre operativo vigente… no se exige checkpoint" por la declaración de mecanismo materializado (anchor VC-1 + checkpoint GC-1 para planes nacidos bajo las reglas nuevas; legacy intacto) | Semántica y DoD | RFC-75; ADR-15 | structure/citations | EJEC |
| E10 | `docs/VERSIONING.md` | `## 10. Definition of Done` | Agregar bullets: validación registrada con Validation Anchor (VC-1) y checkpoint con consistencia antes del cierre (GC-1), con cláusula de legacy | DoD operativo | RFC-75; Plan 94 Unidad B | structure/citations | EJEC |
| E11 | `docs/VERSIONING.md` | `## 11. Métricas del Change Lifecycle…` | Ajustar el estado de las filas anchor coverage / Git closure anomalies: campos existentes desde Incrementos 1/3; medición/agregación sigue en Incremento 4 | Schema ≠ medición | RFC-75 Mecanismo 13 | structure/citations | EJEC |
| E12 | `AGENTS.md` (raíz) | `## Task lifecycle` | Actualizar el párrafo de semántica: el mecanismo de anchor/checkpoint ya no es "futuro (Incremento 3)"; validaciones registradas llevan anchor y el cierre registra checkpoint con consistencia; legacy intacto | Entry point en inglés alineado con la norma | RFC-75; Plan 94 | `check_plan_citations.py` | EJEC |
| E13 | `docs/AGENTS.md` | `### Identity` (párrafo de serie) | Reemplazar "la regla operacional … pertenece a un incremento posterior (Incremento 1)" por la regla vigente (declaración + relaciones; INDEX = vista; detalle en CONVENTIONS) | Serie operacional | RFC-75 Mecanismo 11 | citations | EJEC |
| E14 | `docs/rfc/75-change-lifecycle.md` | `## Amendment Log` | Agregar entrada: "2026-09-02 — Incrementos 1 y 3 materializados (plan 96): anchors/intake/serie y checkpoint/closure; VC-1/GC-1 operativos para artifacts nuevos; legacy intacto" (sin cambiar el header; si el sufijo "implementación pendiente" del status se considera inconsistencia factual, escalar al mantenedor, §37) | Materialización de la RFC; precedente RFC-73/74 (planes 90/91) | RFC-75 Mecanismo 3/5 | citations | EJEC |
| E15 | `CHANGELOG.md` | `[Unreleased]` → `### Changed` | Ítem docs-only `(plan 96, RFC-75)` describiendo la Unidad B | Traza obligatoria de planes docs-only | RFC-69 | `check_version_state.py` | EJEC |
| E16 | `docs/plans/INDEX.md` | fila del plan 96 | Espejo: status `Executed` + nota al ejecutar; mención del checkpoint al cerrar | Mirror mecánico | `docs/AGENTS.md:INDEX y CONVENTIONS` | `check_plan_structure.py` | EJEC |
| E17 | este plan (archivo E1) | `## Nota de ejecución`, `## Validation anchor`, `## Checkpoint` | Completar al ejecutar con el dogfooding real (§25) | Registro de ejecución | RFC-75; convención | battery | EJEC |

### 21.1 Archivos nuevos

| Path | Propósito | Por qué no reutiliza uno existente |
|---|---|---|
| `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md` | Plan de implementación ejecutable de la Unidad B | Cada Plan es un artifact de gobernanza único, numerado por orden cronológico y conservado como traza; el template no es un Plan y no se numera |

Ningún otro archivo nuevo: los mecanismos son campos/relaciones sobre artifacts
existentes.

## 22. Cambios de tools / checkers

**[NORMATIVE + DERIVED]** **Ningún cambio de tooling en esta Unidad.** La
batería existente se reutiliza tal cual; el enforcement mecánico de anchor y
checkpoint pertenece al Incremento 4, gated en observabilidad
(`docs/plans/94-change-lifecycle-master-action-plan.md:14. Estrategia de Harnesses/Checkers`).

Candidatos evaluados (para el Incremento 4; no obligatorios aquí):

| Checker candidato | 1. ¿Qué hecho mecánico verifica? | 2. Fuente de verdad | 3. False positive posible | 4. False negative posible | 5. ¿Determinista? | 6. ¿Qué artifact necesita? | 7. ¿Obligatorio en esta Unidad? |
|---|---|---|---|---|---|---|---|
| Anchor validity (presence + identity computable) | Presencia de bloque `Validation anchor` con identity y factores en validaciones registradas | Artifacts de gobernanza (Plan/RFC) | Anchor presente pero con scope mal declarado (juicio) | Validación registrada en texto no detectado por el parser | Sí (estructura) | Plan/RFC con validación registrada | No (Incremento 4; en B: verificación manual §23/§25) |
| Anchor completeness | Presencia de los campos requeridos del anchor | Template/formato de CONVENTIONS | Campos completos con contenido vacío semántico | Campos opcionales legítimos ausentes | Sí (estructura) | Mismo | No |
| Checkpoint validity | Existencia del registro de checkpoint y SHAs resolubles en `dev` | Plan + Git | Registro con SHA válido pero relación mal declarada | Registro en commit de registro no parseado | Sí | Plan cerrado | No |
| Anchor ↔ checkpoint consistency | Igualdad de tree ids / delta identity + factores entre anchor y cierre | Anchor + `git rev-parse ^{tree}` | Rebase con contenido idéntico pero factor no declarado | Consistencia semántica no capturada por identity | Sí | Anchor + checkpoint | No (en B: comparación manual en el cierre del plan 96) |
| Git state consistency | `git status` limpio según protocolo; commits en `dev`; tags solo en `master` | Git | Warnings del entorno (ACL) mal interpretados | Estados no cubiertos por el parser | Sí | Repo | No (parcialmente cubierto por `check_version_state.py`) |
| Stale detection | Comparación de identity actual vs anchor registrado | Git + anchor | Cambio fuera del scope declarado como stale (depende de scope) | Dependencia no declarada nunca detectada (límite aceptado) | Sí (con scope declarado) | Anchor + estado actual | No (en B: escenarios manuales §23) |
| Series consistency | Coherencia declaración `Serie:` + relaciones RFC↔Plan | Headers + campos RFC/Plan + INDEX | Series homónimas legítimas en repos distintos (repo-scoped: no aplica) | Relaciones no declaradas no derivables | Parcial | Headers | No (en B: regla + escenarios manuales §23) |

Regla transversal: "anchor missing" = GAP, no invalidación; checker output =
evidencia factual, nunca autoridad normativa
(`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).

## 23. Estrategia de tests

**[PROPOSED]** La Unidad B no agrega tests pytest (pertenecen al Incremento 4).
Define una **suite de escenarios de validación** ejecutada manualmente por el
implementador, con procedimiento y resultado esperado. Los escenarios que
mutan un repo corren en un repo scratch temporal (`git init` en un directorio
efímero fuera del working tree) o son read-only sobre el repo real; no dejan
artifacts en el árbol.

### 23.1 Anchors

| ID | Escenario | Procedimiento | Resultado esperado |
|---|---|---|---|
| A-1 | Mismo estado → mismo identity | Computar `Delta scoped identity` y `State identity` dos veces sobre el mismo árbol (mismos archivos) | Identidades idénticas (determinismo) |
| A-2 | Cambio de contenido relevante → identity diferente | Modificar un archivo de `S` (p. ej., un doc del plan) y recomputar | Delta identity y/o tree id diferentes |
| A-3 | Cambio fuera del scope → comportamiento correcto | Modificar un archivo fuera de `S` y recomputar | Delta identity igual; tree id cambia; evaluación de aplicabilidad documentada (no invalidación automática) |
| A-4 | Effective inputs | Declarar para cada comando de la batería los inputs que consume (verificado por lectura del comando/checker) | Tabla de inputs coherente con el código real |
| A-5 | Environmental factors | Registrar python/pytest/git/OS/flags al validar y volver a comparar | Factores reproducibles y comparables |
| A-6 | Version changes | Incluir `protocol/.agents/VERSION` en `S` y simular bump | Identity cambia → evaluar/revalidar |
| A-7 | Stale / revalidation | Comparar identity actual vs anchor registrado; marcar `stale`; re-ejecutar y registrar anchor nuevo | Flujo stale → revalidación documentado |

### 23.2 Checkpoints

| ID | Escenario | Procedimiento | Resultado esperado |
|---|---|---|---|
| C-1 | Commit único | Cerrar un plan de prueba con un solo commit y registrar checkpoint | Consistency PASS; `Closed` derivado |
| C-2 | Múltiples commits | Cerrar un plan de prueba con dos commits (impl + registro) | Checkpoint lista ambos; consistencia en el estado final |
| C-3 | Docs-only | Plan docs-only (como el 96) | `Closed` sin `Released`; representación explícita |
| C-4 | Múltiples RFCs | Plan que referencia dos RFCs (formato existente "RFC-30, RFC-54") | Gobernanza por RFC; checkpoint no depende del conteo |
| C-5 | Múltiples Plans | Planes 94/95/96 con estados distintos | Cada plan con su propio registro; sin registry |
| C-6 | Repo modificado después del checkpoint | Commit posterior al cierre en repo scratch | El checkpoint previo no se invalida |
| C-7 | Checkpoint inconsistente | Registrar cierre con tree id ≠ anchor sin revalidación | Cierre NO declarado; se requiere revalidación |
| C-8 | Anchor inconsistente | Anchor ausente o con identity distinta en el cierre | Cierre bloqueado (GAP) hasta revalidar/evaluar |

### 23.3 Series

| ID | Escenario | Procedimiento | Resultado esperado |
|---|---|---|---|
| S-1 | Misma serie → misma identidad | Derivar serie de RFC-75 y de planes 94/95/96 por relación | Todos resuelven a "Change Lifecycle" de forma consistente |
| S-2 | Orden / cambios derivados | Marcar un miembro `Superseded` en scratch | La serie sobrevive; sin registry |
| S-3 | Ausencia de registry | Inventariar artifacts que representan la serie | Solo headers y relaciones; ningún artifact de serie nuevo |
| S-4 | Aislamiento entre proyectos | Dos repos scratch con el mismo label de serie y distinta membresía | Sin colisión: derivación repo-scoped |

Los casos que requieran automatización durable se registran como requisitos del
Incremento 4 (no se implementan aquí).

## 24. Telemetría

**[NORMATIVE + DERIVED]** RFC-75 Mecanismo 13: definición ≠ persistencia ≠
medición ≠ automatización.

| Métrica (schema §11 VERSIONING) | Definición | Persistencia (esta Unidad) | Medición | Automatización |
|---|---|---|---|---|
| Validation anchor coverage | % de validaciones registradas con anchor | Sí: campos de anchor en Plan/RFC (Incremento 1) | Manual/observacional desde ahora; queries → Incremento 4 | Incremento 4 |
| Git closure anomalies | Conteo/% de cierres o planes con anomalías de closure | Sí: registro de checkpoint + condiciones derivadas (Incremento 3) | Manual desde ahora (plan 96 como primer dato) | Incremento 4 |
| Stale validation rate | % de validaciones ancladas con anchor cambiado sin revalidación | Parcial: campo `Validity/stale` en el anchor (Incremento 1) | Manual desde ahora; completo con revalidación formal (Incremento 2) | Incremento 4 |
| Finding lineage coverage | % de correcciones con lineage trazable | No: refs `F-n` → Incremento 2 | No | Incremento 4 |

Eventos/campos nuevos que comienzan a existir con esta Unidad: presencia y
contenido de anchors, tree ids y delta identities, registros de checkpoint,
consistencia PASS/FAIL, declaraciones `Change Level`, membresías de serie.
Métricas de coordinación: EXPERIMENTAL/DEFERRED (Incremento 5). Ninguna métrica
es gate de release; legacy excluido del denominador.

## 25. Dogfooding

**[PROPOSED]** El propio Plan 96 es el primer sujeto de los mecanismos que
implementa:

1. **Intake:** el plan declara `**Change Level:** L2` (§26) y su clasificación
   en el primer artifact (este archivo).
2. **Serie:** la membresía se deriva de RFC-75 (`Serie: Change Lifecycle`) vía
   la relación `RFC:` del header (§15); sin campo `Serie:` en el plan.
3. **Validation anchor:** al ejecutar, después de aplicar E3–E16 (antes de
   commitear), se corre la batería sobre el árbol exacto y se registra el
   `## Validation anchor` en este plan: declared scope, command-set, effective
   inputs, observed dependencies, environmental factors, `State identity`
   (`git write-tree`) y `Delta scoped identity`.
4. **Git state:** commit atómico C1 (plan + docs + changelog + INDEX espejo,
   `(plan 96, RFC-75)`).
5. **Checkpoint:** tras C1, se verifica `git rev-parse C1^{tree}` == tree del
   anchor y factores sin cambio; el registro de checkpoint se agrega en un
   commit de registro C2 (precedente `dc7425f`) con los SHAs y la condición
   derivada; los checkers de docs se re-ejecutan sobre C2 (PASS) como
   verificación del registro.
6. **Closure:** condición derivada `Closed` (docs-only, sin release) registrada
   en la Nota/checkpoint; plan 96 queda `Executed` + `Closed` (derivado), sin
   cambiar su status.

**Qué no puede dogfoodearse todavía:** refs de findings/revalidación formal
(Incremento 2); verificación automática (Incremento 4); release (no aplica).

**Anti-circularidad:** el mecanismo se materializa (E3–E16) antes de registrar
el anchor final; el anchor se computa sobre el working tree sin necesitar
commits (`git write-tree`); el registro de checkpoint (C2) es metadata posterior
al contenido validado (C1) y se verifica por separado, sin reclamar que C2
estaba dentro del scope validado de C1. No hay dependencia del mecanismo sobre
sí mismo: `Closed` del plan 96 se apoya en el anchor de C1 y en la verificación
de C2, ambos derivables sin recursión.

## 26. Change Level

**[DERIVED]** Aplicación del modelo de RFC-75 Mecanismo 2
(`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`) y de la matriz
operacional del Plan 94 (`docs/plans/94-change-lifecycle-master-action-plan.md:9. Economía de Change Levels`):

| Dimensión | Valor | Justificación |
|---|---|---|
| coordination | 1 | 1 agente, multi-sesión (diseño del plan en una sesión; implementación y cierre en sesiones posteriores) |
| scope (superficie) | 1 | Área acotada: una capa del repo (gobernanza/documentación DEV: templates, CONVENTIONS, VERSIONING, AGENTS, INDEX, changelog). No toca runtime/tools/tests/protocol |
| architectural impact | 1 | Cambio estructural local, aditivo y reversible: campos y reglas sobre artifacts existentes; sin nuevos módulos ni seams entre límites |
| release impact | 1 | docs-only / changelog-only: ítem en `[Unreleased]`, sin `VERSION` bump ni tag (RFC-69) |
| duration/complexity | 2 | multi-sesión: redacción, ejecución documental, dogfooding (anchor + checkpoint) y cierre exigen más de una sesión |

```text
Level = max(1, 1, 1, 1, 2) = 2  (L2)
```

**Notas:**

- Change Level ≠ clase RFC-56: este plan no toca el payload y no tiene clase
  (`Clase: —`); el eje RFC-56 no aplica.
- El número de commits no es dimensión (aunque el cierre use C1 + C2).
- L2 no significa crear machinery nueva aquí: este plan es precisamente el que
  instala los mecanismos de L1 (anchor + checkpoint) en la gobernanza; la
  clasificación describe el cambio, no la machinery que instala.
- No es L3: no es cross-RFC orquestado (implementa una única RFC-75 con su
  plan), no es multi-área con contratos y no es irreversible.

## 27. Frontera DEV / Protocol

**[NORMATIVE]** Esta Unidad es **DEV-only**:

- No modifica `protocol/.agents/`, `protocol/_AGENTS.md`,
  `protocol/.agents/VERSION`, `dist/` ni el runtime del Protocol.
- No agrega mecanismos del Change Lifecycle al payload.
- No subordina las reglas del Protocol a este lifecycle: RFC-75 gobierna la
  evolución de ARgentOS DEV; un cambio con efecto payload sigue RFC-56 (RFC
  `Accepted` + plan) (`docs/rfc/75-change-lifecycle.md:Dev vs Protocol`).
- Los principios transferibles (revalidación ante continuidad; persistir ≠
  materializar; evidencia factual ≠ autoridad normativa) quedan como
  principios, sin herencia de mecanismo.
- Ningún cambio propuesto escribe en `protocol/`; los únicos toques al payload
  serían lecturas normativas del anchor (p. ej., incluir
  `protocol/.agents/VERSION` como factor/input), no modificaciones.
- Si alguna propuesta de este plan requiriera tocar `protocol/`, sería una
  contradicción con RFC-75 y debe detenerse y escalarse (BLOCKER, §34).

## 28. Decisión de skills

**[NORMATIVE]** **No se crean skills DEV nuevas.**

- RFC-75 prohíbe skills obligatorias (No-objetivos) y Plan 94 determina que los
  mecanismos deterministas (anchor computation, checkpoint consistency, refs,
  serie derivation, stale detection) son **scripts/checkers** (`tools/`), no
  skills (`docs/plans/94-change-lifecycle-master-action-plan.md:11. Estrategia de Skills`).
- No hay evidencia nueva y fuerte que justifique una skill: la guía de
  clasificación se materializa como texto normativo en CONVENTIONS + campos de
  template (mecanismo determinista en su parte formal; juicio humano en la
  calibración fina).
- Una eventual skill LLM de asistencia a clasificación sería una hipótesis
  futura con evidencia, por el ciclo DEV correspondiente.

## 29. Decisión de state machine

**[NORMATIVE]** **No se crea ninguna Change State Machine global.**

- Intake, Anchor, Validation, Commit, Checkpoint y Closure siguen siendo
  condiciones/mecanismos/artifacts según RFC-75; no son estados de una máquina
  nueva (`docs/rfc/75-change-lifecycle.md:No-objetivos`; Plan 94 §10).
- Los únicos status existentes (Plan/RFC/ADR) se conservan; las condiciones
  derivadas (Verified/Executed/Committed/Closed/Promoted/Released/Abandoned)
  ya están escritas en `docs/VERSIONING.md:7. Estados de planes y RFCs`.
- Este plan solo materializa los *registros* de anchor y checkpoint que
  alimentan la derivación; no agrega transiciones.

## 30. Grafo de dependencias

**[DERIVED]** Derivado del rollout real de RFC-75 y de los artifacts del repo:

```text
RFC-75 (Accepted) ── ADR-15/16 ── RFC-56 ── RFC-69
        │
        ▼
Unidad A (Incremento 0) ── Plan 95 (Executed, bc21978/865e3ad/dc7425f)
        │
        ▼
Unidad B (Incrementos 1+3) ── Plan 96 (ESTE plan; batch operacional, el 3 no
        │                      se renumera ni absorbe)
        │
        ├──────────────────────────────┐
        ▼                              ▼
Unidad C (Incremento 2) ── Plan 97     Unidad D (Incremento 4) ── Plan 98
        │                              (gated en datos de A–C)
        ▼
Incremento 5 (Deferred / Future Track)
```

Dependencias operativas de ejecución: Python 3.14 + pytest disponibles; git en
`dev` con HEAD `dc7425f` y árbol limpio; autorización del mantenedor para el
commit atómico y el cierre (§37). No hay dependencias de herramientas nuevas.

## 31. Secuencia de implementación

**[PROPOSED]** Orden y fases (cada fase deja el repo utilizable y verificable).
Los Incrementos conceptuales 1 y 3 se ejecutan en el mismo batch operacional
(Plan 94), por lo que las fases se ordenan por **artifact** (para no re-tocar
archivos y no dejar citas a secciones inexistentes), no por incremento; el
alcance por incremento queda definido en §7/§8 y el mapeo mecanismo → paso en
§9.2/§21:

```text
Fase 0 (premisas)  → verificar estado (git status/HEAD; checkers; pytest real)
Fase 1 (normativa base)
   E8 CONVENTIONS (subsecciones operativas: intake/clasificación, validation
      anchors VC-1, serie e identidad derivada, checkpoint/cierre GC-1;
      actualizar regla transversal y clasificación operacional)
Fase 2 (templates y taxonomía)
   E3–E5 template de Plan (Change Level + Validation anchor + Checkpoint)
   E6–E7 template de RFC (Change Level opcional + anchor en Amendment Log)
   E13 docs/AGENTS.md Identity (serie operacional)
Fase 3 (políticas y entry point)
   E9–E11 VERSIONING §7/§10/§11 (anchor + checkpoint + DoD + métricas)
   E12 AGENTS.md (task lifecycle: anchor + checkpoint operativos)
Fase 4 (registro normativo)
   E14 RFC-75 Amendment Log (materialización; sin header salvo escalación)
Fase 5 (cierre del plan 96)
   E15 changelog [Unreleased] (ítem plan 96)
   E16 INDEX espejo (Executed + nota)
   E17 completar en este plan: Nota de ejecución + Validation anchor
      (dogfooding)
   Batería canónica completa (checkers + pytest real)
Fase 6 (checkpoint / closure)
   Commit atómico C1 (aprobación del mantenedor; §37)
   Verificación de consistencia (§18) → registro de checkpoint (C2)
   Condición derivada Closed (docs-only) registrada
```

Reglas de orden: no dejar estados intermedios donde un doc cite una sección
inexistente de otro; E8 (CONVENTIONS) precede a los templates que lo referencian
(E3–E7); los templates se actualizan antes de que cualquier plan nuevo los use;
la batería corre al final de cada fase con el diff acotado; si una fase deja
warnings esperados de `dev`, se documentan y no se declaran PASS falsos (§34).
El commit atómico C1 de la Fase 6 incluye todo el diff de las Fases 1–5.

## 32. Rollback / contención

**[DERIVED]**

- **Contención del cambio:** el diff se limita a los archivos de §21; cualquier
  cambio ajeno detectado durante la ejecución (working tree sucio con archivos
  no documentados) detiene la ejecución (BLOCKER, §34).
- **Rollback documental:** `git revert` de C1/C2 (o revert manual de los
  cambios de §21); los docs vuelven al estado previo; sin datos que migrar.
- **Registros con campos nuevos** si se revierte el incremento: se tratan como
  legacy (ausencia de mecanismo no invalida; `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).
- **Sin efectos de release:** no hay tag, VERSION ni `dist`.
- **Concurrencia:** lección de los planes 87/92/93/91: serializar por archivo
  compartido; ningún otro plan debe tocar CONVENTIONS/VERSIONING/templates
  mientras la Unidad B esté en vuelo (`docs/VERSIONING.md:8. Ejecución en paralelo`).

## 33. Matriz de validación

| Requisito | Método | Evidencia | Resultado esperado |
|---|---|---|---|
| Semántica implementada | Revisión de diff contra RFC-75/Plan 94 | Diff de §21 | Solo mecanismos derivados; cero decisiones normativas nuevas |
| Artifacts correctos | `check_plan_structure.py` + `check_plan_citations.py` | Salida PASS | Sin violaciones |
| Anchors reproducibles | Escenarios A-1/A-2/A-3 | Salida de git write-tree/hash-object | Determinismo verificado |
| Stale detectable | Escenario A-7 | Registro stale → revalidación | Flujo documentado |
| Checkpoint verificable | Escenario C-1..C-8 + dogfooding | Registro del plan 96 | Consistencia PASS |
| Closure verificable | Derivación de §17 sobre plan 96 | Nota + checkpoint | `Closed` (docs-only) |
| Git state consistente | `git status`, `git log`, tree ids | Salidas | Árbol limpio al cierre; commits en `dev` |
| Tests completos | Suite de escenarios §23 + pytest real | Reporte | Todos PASS |
| Checkers completos | Batería canónica | Salidas PASS (warnings esperados de dev) | Sin regressions |
| Legacy compatible | Revisión de planes 94/95 sin cambios | Diff | Intactos y válidos |
| DEV/Protocol intacto | `git diff` sin `protocol/`, `runtime/`, `tests/`, `tools/` | Diff | Sin cambios de esas capas |
| Sin regressions | `python -m pytest tests/` (permisos reales) | `340 passed, 0 failed` (o desviación documentada aceptada) | PASS real |

## 34. Criterios de aceptación

### 34.1 BLOCKER (impide ejecutar o continuar)

- Estado material distinto del §3 (branch, HEAD, árbol sucio, pytest con fallos
  de código no ambientales) sin explicación.
- Contradicción objetiva entre RFC-75, Plan 94/95 y este plan sobre el
  contenido de la Unidad B.
- Necesidad de tocar `protocol/`, `runtime/`, `tests/`, `tools/` o `VERSION`
  fuera del alcance declarado.
- Necesidad de una entidad/registry/state machine/skill/checker no autorizado.
- Working tree con cambios ajenos no documentados.
- Necesidad de decidir arquitectura nueva no cubierta por RFC-75/Plan 94.

### 34.2 FAIL (implementación no aceptable)

- Template/CONVENTIONS/VERSIONING sin los campos/reglas de §21 (E3–E16).
- Se declara `Closed` sin checkpoint, sin consistencia o con test FAILED
  ocultado (política de "batería verde" del Plan 94 §24.1).
- Se modifica legacy para cumplir metadata nueva o se fabrican anchors
  históricos.
- Se filtra scope hacia Incrementos 2/4/5 (findings/pending/checkers/skills).
- Se contamina la frontera DEV/Protocol (cualquier diff en las capas
  excluidas).
- Checkers aplicables en rojo sin desviación documentada aceptada.

### 34.3 WARNING (aceptable sin bloquear)

- Warnings esperados de `dev` en `check_version_state.py` (secciones sin tag).
- ACL del sandbox en pytest: requiere ejecución con permisos reales (ruido
  ambiental documentado; nunca se reporta PASS con errores de fixture).
- Intro de `docs/plans/INDEX.md` y §9 de VERSIONING con snapshots
  desactualizados (deuda descriptiva conocida, sin acción en esta Unidad).
- Posición histórica de `[Unreleased]` en el changelog (sin reordenar en esta
  Unidad).
- `dev` ahead 6 de `origin/dev` (sin push; decisión del mantenedor).

### 34.4 HUMAN DECISION (exclusivas del maintainer)

- Autorización para ejecutar la Unidad B (Aprobado para ejecución → ejecución).
- Autorización del commit atómico C1 y del commit de registro C2.
- Aceptación del cierre (`Closed` derivado) con la batería real reportada.
- Si el sufijo "implementación pendiente" del status de RFC-75 se considera
  inconsistencia factual tras E14: decidir si se ajusta el header (vía Amendment
  Log) o se deja como histórico.
- Backfill opcional de legacy (G1, serie RFC-71..74, planes sin commit).
- Elevación de ADR candidates (Change Level, Scoped Content Identity) cuando
  haya primer consumo o disputa (§36).

## 35. Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación | Detección |
|---|---|---|---|---|
| Duplicación normativa (RFC-75 ya define el modelo) | Media | Terminología divergente | Hogar único por concepto en CONVENTIONS; citas en vez de copia | Revisión de diff; `check_plan_citations.py` |
| Circularidad en el primer anchor/checkpoint | Media | Cierre bloqueado o inconsistente | Protocolo C1/C2 + tree id sobre working tree (§25); registro en commit posterior | Escenarios C-1..C-8 |
| Falsos stale por uso de SHA como identidad | Media | Revalidaciones innecesarias | Regla §13: tree id/delta identity, SHA solo locator | Escenarios A-1..A-3 |
| Burocracia L0/L1 | Media | Fricción en cambios triviales | L0 provisional sin Plan obligatorio; campos opcionales por nivel; enforcement mecánico en Incremento 4 | Revisión §14 |
| Scope inflation hacia Incrementos 2/4 | Media | Plan no derivable | Guard de §6; exclusiones explícitas | Auditoría adversarial §38 |
| Checker como autoridad | Baja | Conflictos mal resueltos | Regla ADR-16 en §22 | Revisión |
| Contaminación DEV/Protocol | Baja | Payload modificado | Frontera §27; scope guard | `git diff` sin capas excluidas |
| Legacy interpretado como inválido | Media | Planes 94/95 reescritos | Discriminador §20; sin backfill | Revisión §20 |
| Paralelismo sobre archivos compartidos | Baja | Conflictos de edición | Serialización §32; lección planes 87/92/93/91 | `git status` |
| pytest ambiental (ACL sandbox) | Alta (entorno) | Falsa señal roja | Ejecución con permisos reales; reporte honesto (§34.3) | Resultado real |

## 36. Preguntas abiertas

| # | Pregunta / decisión | Clasificación | Resolución propuesta |
|---|---|---|---|
| OPEN-1 | Wording exacto (idioma/posición) de los textos nuevos E3–E16 | CAN DECIDE IN PLAN | El agente redacta en el idioma de cada doc (español en CONVENTIONS/VERSIONING/docs-AGENTS/templates; inglés en AGENTS.md raíz) según §21 |
| OPEN-2 | Posición exacta de la sección `## Validation anchor` / `## Checkpoint / cierre` en el template | CAN DECIDE IN PLAN | Después de `## Verificación` (E4/E5) |
| OPEN-3 | ¿Registrar C2 como commit de registro separado o como parte del commit de cierre? | CAN DECIDE IN PLAN | Commit de registro C2 (precedente `dc7425f`), porque el SHA de C1 no puede citarse dentro de C1 |
| OPEN-4 | ¿El header de RFC-75 requiere ajuste del sufijo "implementación pendiente"? | HUMAN | Escalar al mantenedor tras E14 (§34.4); no decidirlo unilateralmente |
| OPEN-5 | ¿Backfillear ejemplares (relación G1, serie RFC-71..74)? | HUMAN | No en esta Unidad; opcional posterior (RFC-75 Mecanismo 15) |
| OPEN-6 | ¿Elevar ADR candidate "Scoped Content Identity" / "Change Level"? | HUMAN | Trigger: primer consumo o disputa (§22 de Plan 94); no ahora |
| OPEN-7 | ¿La suite de escenarios §23 se documenta en este plan o en un anexo? | CAN DECIDE IN PLAN | En este plan (resultados en la Nota de ejecución) |

## 37. Decisiones humanas

| Decisión | Owner | Cuándo |
|---|---|---|
| Autorizar la ejecución de la Unidad B | Mantenedor | Al aprobar este plan para ejecución |
| Autorizar commit atómico C1 y registro C2 en `dev` | Mantenedor (práctica del repo) | Fase 6 |
| Aceptar el resultado de la batería (PASS real) para declarar cierre | Mantenedor | Fase 6 |
| Decidir sobre OPEN-4 (header de RFC-75) | Mantenedor | Tras E14 si surge |
| Decidir backfills opcionales y elevaciones de ADR candidates | Mantenedor | Fuera de esta Unidad |

Los agentes detectan, proponen y registran; no resuelven conflictos normativos
ni deciden cierres por autoridad propia (AU-3, ADR-16).

## 38. Auditoría adversarial

| Criterio | Verdict | Evidencia / mitigación |
|---|---|---|
| A. Authority | PASS | Toda decisión operativa deriva de RFC-75/ADR-15/16/Plan 94/95 (§2, §9, §21); no se inventó decisión normativa nueva; formato de campos autorizado por RFC-75 "CAN DECIDE IN PLAN" |
| B. Anchor identity | PASS | Locator (SHA/path) separado de identidad semántica (tree id / delta identity) (§13); SHA nunca es identidad |
| C. Scope | PASS | Cambio fuera del scope: delta identity igual; tree id puede cambiar → evaluación, no invalidación automática (§13.3, A-3) |
| D. Git | PASS | Commit ≠ checkpoint; SHA = locator; checkpoint = relación con registro (§16, §19); rebase/amend con contenido idéntico no invalida |
| E. Closure | PASS | `Closed` exige Executed + governance + checkpoint + consistencia (§17); sin condiciones suficientes no se declara |
| F. Multi-commit | PASS | Registro lista C1…Cn; consistencia en el estado final (§16.2.9, C-2) |
| G. Multi-RFC | PASS | Gobernanza por RFC; checkpoint no depende del conteo (§16.2.10, C-4) |
| H. Multi-Plan | PASS | Checkpoint por Plan; sin registry (§16.2.11, C-5) |
| I. Docs-only | PASS | `Closed` sin release representado explícitamente (§17, C-3) |
| J. Legacy | PASS | Ausencia de campos = legacy, no invalidez; sin migración ni anchors fabricados (§20) |
| K. DEV/Protocol | PASS | Cero cambios en capas del Protocol (§27); principios ≠ mecanismos |
| L. State machine | PASS | Sin Change State Machine; condiciones derivadas sobre status existentes (§29) |
| M. Entities | PASS | Sin Change/Finding/Decision/Series/Checkpoint registry ni entidades nuevas (§6, §11) |
| N. Skills | PASS | Sin skills nuevas; mecanismos deterministas → tools (Incremento 4) (§28) |
| O. Circularity | PASS | El mecanismo se materializa antes del anchor final; tree id no requiere commit; C2 es registro posterior (§25) |
| P. Determinism | PASS | Identity v1 por primitivas git (write-tree/ls-files/hash-object); reproducible (§13, A-1) |
| Q. Stale | PASS | Comparación de identity + factores; marca stale y revalidación manual en esta Unidad (§12.4, A-7) |
| R. Human authority | PASS | Gates y decisiones humanas tipadas (§34.4, §37); agentes detectan/escalan, no deciden |

Resultado: 18 PASS, 0 FAIL, 0 BLOCKED.

## 39. Veredicto final

**`PLAN 96 READY FOR IMPLEMENTATION`**

- **Nombre:** Plan 96 — Implementación de la Unidad B (Incrementos 1+3):
  anchors de validación, intake fallback, serie e identidad derivada; Git
  closure/checkpoint del Change Lifecycle DEV.
- **Alcance:** Unidad B = Incrementos conceptuales 1 y 3 de RFC-75 en batch
  operacional (el 3 no se renumera ni se absorbe); docs-only; sin machinery de
  código; sin cambios de payload.
- **Autoridades:** RFC-75 `Accepted`; ADR-15/16 `Accepted`; RFC-56 `Accepted`;
  RFC-69 `Accepted`; Plan 94 `Executed` (mapa maestro, Unidad B); Plan 95
  `Executed` (Incremento 0).
- **Cambios principales (ejecución):** E3–E17 según §21 (templates, CONVENTIONS,
  VERSIONING, AGENTS.md, docs/AGENTS.md, Amendment Log de RFC-75, changelog,
  INDEX) incluido el dogfooding del propio plan (anchor + checkpoint).
- **Gates de ejecución/cierre:** autorización del mantenedor (Aprobado para
  ejecución → ejecución; commit C1/C2; aceptación del cierre). Ninguno es
  blocker de diseño.
- **Deuda no bloqueante:** `dev` ahead 6; snapshots de INDEX/VERSIONING;
  posición de `[Unreleased]`; ACL del sandbox en pytest (ruido ambiental).
- **Próximo paso:** ejecutar la Unidad B (Fases 0–6 de §31) sobre `dev`,
  validar con la batería real y cerrar con anchor + checkpoint (dogfooding),
  habilitando la Unidad C (Incremento 2, Plan 97) y el gate de observabilidad
  del Incremento 4.

## Trazabilidad

```text
Origen (mantenedor, 2026-09-02)
  → RFC-75 Accepted (rollout incremental: Incrementos 1 y 3 en batch)
  → ADR-15/16 (invariantes y autoridad)
  → Plan 94 (Unidad B: 1+3 en batch operacional)
  → Plan 95 (Unidad A / Incremento 0, Executed)
  → Plan 96 (ESTE plan; Unidad B)
  → Ejecución documental (E1–E17)
  → Validación (batería real + suite de escenarios)
  → Cierre (anchor + checkpoint; dogfooding)
  → Unidad C (Incremento 2, Plan 97) y Unidad D (Incremento 4, Plan 98);
    Incremento 5 = Deferred / Future Track
```

Este plan no autoriza cambios de payload (RFC-56).

## Nota de ejecución

<!-- Se completa al ejecutar (Fases 5/6 de §31): fecha, verificación real
(checkers + pytest), Validation anchor (State identity + Delta scoped
identity + factores), registro de checkpoint (C1/C2 + consistencia) y
condición derivada Closed (docs-only, sin release). El Status pasa a
`Executed` en esa fase; esta iteración de planificación no ejecuta. -->
