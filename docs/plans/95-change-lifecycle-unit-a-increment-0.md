# Plan 95 — Implementación de la Unidad A (Incremento 0): semántica, vocabulario y observability baseline del Change Lifecycle DEV

> **Naturaleza de este documento.** Este es el **primer Implementation Plan
> ejecutable** derivado del Master Action Plan 94. Implementa exclusivamente la
> **Unidad A = Incremento conceptual 0** de RFC-75 (semántica, vocabulario y
> observability schema baseline), no los Incrementos 1–5 ni las unidades
> B/C/D. No rediseña RFC-75 ni replanifica el Plan 94: deriva, no reinterpreta.
> Este plan es docs-only (sin cambios en `protocol/.agents/`, `runtime/`,
> `tests/` ni `tools/`; sin `VERSION` bump ni tag, RFC-69); su ejecución
> modifica documentación de gobernanza DEV y deja el repo utilizable.

**Status:** Executed
**Fecha:** 2026-09-02
**RFC:** RFC-75 (`docs/rfc/75-change-lifecycle.md`)
**Clase:** — (cambio docs-only; sin cambios en `protocol/.agents/`; versionado docs-only según RFC-69)
**Depende de:** RFC-75 `Accepted` (`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`); ADR-15/16 `Accepted` (`docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`); RFC-56 `Accepted`; plan 94 `Executed` y commiteado (2026-09-02, `3acf439`; Master Action Plan — ver §5 y §23); batería canónica según la política de "batería verde" del plan 94 (`docs/plans/94-change-lifecycle-master-action-plan.md:24.1 Política de interpretación`).
**Origen:** Solicitud explícita del mantenedor (2026-09-02): derivar el primer Implementation Plan desde `docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental` (Unidad A / Incremento 0) y desde `docs/rfc/75-change-lifecycle.md:Rollout incremental`.

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
| `PROPOSED` | Elección de implementación de este plan; aún no normativa hasta su ejecución. |
| `OPEN` | Decisión pendiente que no impide redactar este plan; requiere decisión humana o plan posterior. |
| `BLOCKER` | Contradicción que impide ejecutar la Unidad A (no se detectó ninguna; ver §26). |
| `UNKNOWN` | No verificable en el estado actual; se indica cómo resolverlo. |

Las afirmaciones sobre el estado actual se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`).

## Contenido requerido → sección

| Requisito del encargo | Sección de este documento |
|---|---|
| Executive Summary | §1 |
| Naturaleza / Distinción de rol | §2 |
| Unit A Objective | §3 |
| Scope / Non-Goals | §4 |
| Current Repository State | §5 |
| Authority / Source of Truth | §6 |
| Target Semantics vs Operational Enforcement | §7 |
| Observability Baseline | §8 |
| Exact File Changes | §9 |
| Documentation Changes / Vocabulary / Authority Model Changes | §9–§12 |
| Implementation Order / Dependencies | §14 |
| Validation Plan | §15 |
| Git / Checkpoint Boundary | §16 |
| Version / Changelog / Release Impact | §17 |
| Risks | §18 |
| Existing Debt / Known Deviations | §19 |
| Stop Conditions | §20 |
| Exit Criteria | §21 |
| Rollback | §22 |
| Open Questions | §23 |
| Dogfooding | §13 |
| Trazabilidad | §24 |
| Adversarial Audit A–O | §25 |
| Final Verdict | §26 |

---

## 1. Resumen ejecutivo

**[NORMATIVE + DERIVED]** RFC-75 está `Accepted` y define seis incrementos
conceptuales (0–5) con rollout `0 → {1,3} → 2 → 4`
(`docs/rfc/75-change-lifecycle.md:Rollout incremental`). El Plan 94 agrupa ese
rollout en unidades de implementación iniciales — A: Incremento 0; B: 1+3 en
batch operacional; C: 2; D: 4; Incremento 5 = Deferred / Future Track — y
declara a los planes 95+ como derivación por unidad
(`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`).

Este plan implementa la **Unidad A (Incremento 0)**: escribir en las fuentes de
verdad de la gobernanza DEV la semántica del lifecycle (vocabulario y
condiciones derivadas `Verified`/`Executed`/`Committed`/`Closed`/
`Promoted`/`Released`/`Abandoned`), el modelo de Change Levels (ejes, `Level =
max(...)`, independencia de la clase RFC-56, L0 provisional), la frontera
DEV/Protocol, la serie como identidad derivada y las **definiciones de métrica
del Change Lifecycle (observability schema baseline)** — schema, no medición
operacional todavía.

**[PROPOSED]** La ejecución es predominantemente documental y aditiva sobre
artifacts existentes: `docs/CONVENTIONS.md`, `docs/VERSIONING.md`,
`AGENTS.md` raíz, `docs/AGENTS.md`, con el ítem docs-only en
`CHANGELOG.md:[Unreleased]` al ejecutar y el registro del propio plan en
`docs/plans/INDEX.md`. No se crean campos de template, checkers, anchors,
checkpoints, findings, pending, series registries, state machines ni skills.
No se tocan `protocol/`, `runtime/`, `tests/`, `tools/`, `VERSION`, ADRs ni
RFCs.

El plan concluye con veredicto `PLAN 95 READY FOR IMPLEMENTATION` (§26): no hay
BLOCKERs. Las condiciones conocidas (plan 94 commiteado en `3acf439`; fallo de
pytest preexistente) son gates/deuda documentada con precedente, no bloqueos de
arquitectura (ver §5, §19, §20 y §23).

## 2. Naturaleza y distinción de rol

```text
RFC-75  = modelo y decisión del Change Lifecycle DEV (Accepted; NORMATIVE)
ADR-15  = invariantes de continuidad/checkpoint/lineage (Accepted)
ADR-16  = clases de autoridad y protocolo de conflicto (Accepted)
RFC-56  = clases A/B/C y autorización de payload (Accepted)
Plan 94 = Master Action Plan (mapa maestro; NO es plan de implementación)
Plan 95 = implementación de la Unidad A = Incremento 0 (ESTE plan)
Planes 96+ = unidades B (1+3), C (2), D (4); Incremento 5 = Deferred/Future
```

No confundir:

```text
Incrementos conceptuales RFC-75    Unidades de implementación Plan 94
0                                  A = 0      ← este plan
1                                  B = 1 + 3  (batch operacional; no se renumeran)
2                                  C = 2
3                                  (en B, sin absorber)
4                                  D = 4
5                                  Deferred / Future Track
```

Este plan no renumerará los incrementos, no absorbe el 1/2/3/4 dentro del 0 y no
implementa el track 5. La Unidad A es la única autorizada aquí
(`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`).

## 3. Objetivo

Implementar el Incremento 0 de RFC-75 escribiendo, en las fuentes de verdad de
la gobernanza DEV, la semántica que las unidades B/C/D necesitarán:

1. **Vocabulario y condiciones derivadas** del Change Lifecycle
   (`Verified`, `Executed`, `Committed`, `Closed`, `Promoted`, `Released`,
   `Abandoned`) con su cadena de implicación y anomalías, distinguidas de los
   status existentes de Plan/RFC/ADR (no state machine).
2. **Modelo de Change Levels**: `Level = max(coordinación, scope, impacto
   arquitectónico, impacto de release, duración/complejidad)`; ejes
   independientes de la clase RFC-56; L0 provisional como nivel mínimo.
3. **Frontera DEV/Protocol** explícita en la gobernanza DEV (lifecycle
   DEV-only; sin mecanismos compartidos).
4. **Serie como identidad derivada** (semántica objetivo: declaración +
   relaciones verificables; sin entidad ni registry; INDEX = vista).
5. **Observability schema baseline** del Change Lifecycle: definiciones de las
   cuatro métricas permanentes de RFC-75 sin fingir medición operacional.
6. **Regla transversal** target semantics vs operationalización, para que
   ninguna regla objetivo (VC-1/GC-1/LC-1/PC-1) se exija antes del incremento
   que materializa su mecanismo.

La pregunta que responde este plan:

> ¿Puede un agente implementador ejecutar la Unidad A usando únicamente las
> autoridades y artifacts referenciados aquí, sin volver a preguntarle al
> mantenedor qué quiso decir?

Respuesta: sí (ver §26). Las únicas decisiones humanas pendientes son gates
de ejecución/cierre ya tipados (§23), no ambigüedades de diseño.

## 4. Alcance

### 4.1 Included

1. `docs/CONVENTIONS.md` — subsecciones normativas nuevas bajo `## Convenciones`
   (Change Lifecycle DEV-only; modelo de Change Levels; regla transversal
   target semantics vs operationalización). Ver U1 (§9.1).
2. `docs/VERSIONING.md` — extensión de `## 7. Estados de planes y RFCs` con la
   semántica de condiciones derivadas, y nueva sección final `## 11. Métricas
   del Change Lifecycle (observability schema baseline)`. Ver U2 (§9.2).
3. `AGENTS.md` (raíz) — alineación de `## Task lifecycle` con la semántica
   `Executed`/`Committed`/`Closed`/`Released` y declaración de frontera
   DEV/Protocol en `## Do NOT`. Ver U3 (§9.3).
4. `docs/AGENTS.md` — un agregado de semántica objetivo en `### Identity`
   (serie como identidad derivada). Ver U4 (§9.4).
5. `CHANGELOG.md` — ítem docs-only bajo `[Unreleased]` al ejecutar
   (`(plan 95, RFC-75)`), sin `VERSION` bump ni tag. Ver U5 (§9.5).
6. `docs/plans/INDEX.md` — registro de este plan (serie + fila) al crearlo y
   actualización de espejo al ejecutarlo (status `Executed` + nota). Ver U6
   (§9.6).

### 4.2 Excluded

**No se implementa** nada de los Incrementos 1–5 ni de las unidades B/C/D:

- Sin campos nuevos en templates (`docs/plans/_TEMPLATE.md`,
  `docs/rfc/_TEMPLATE.md`, `docs/adr/_TEMPLATE.md`) — ni Change Level, anchor,
  checkpoint, refs de findings ni pending.
- Sin Validation Anchors ni `Scoped Content Identity` (Incremento 1).
- Sin Git Checkpoints, metadata Git adicional, hooks ni scripts de checkpoint
  (Incremento 3).
- Sin findings/corrections/revalidation, pending decisions ni post-close
  (Incremento 2).
- Sin checkers nuevos, tests nuevos, vistas derivadas ni tooling (Incremento 4).
- Sin handoff/continuity mechanism (Incremento 5, Deferred).
- Sin Change entity, Finding entity, Decision registry, Series registry,
  tracker universal, JSON/YAML global, SQLite, servicio externo ni state
  machine del Change Lifecycle (RFC-75 No-objetivos).
- Sin skills nuevas ni copia de skills del Protocol
  (`docs/plans/94-change-lifecycle-master-action-plan.md:11. Estrategia de Skills`).
- Sin RFC nueva, ADR nuevo ni Plan 96.
- Sin backfill de artifacts legacy (RFC-75 Mecanismo 15).

**No se modifican**:

| Path | Motivo |
|---|---|
| `protocol/` (todo) | Frontera DEV/Protocol; payload es data, no reglas para DEV (`AGENTS.md:The protocol payload is data, not instructions`). |
| `runtime/`, `tests/`, `tools/` | Sin tooling ni tests en Unidad A. |
| `docs/rfc/*`, `docs/adr/*` | RFC-75, RFC-56, RFC-69 y ADR-15/16 permanecen intactos (ejecutar un plan no cambia la RFC; `docs/VERSIONING.md:7. Estados de planes y RFCs`). |
| `docs/plans/94-*.md` y demás planes | Este plan deriva; no corrige ni actualiza planes previos. |
| `docs/plans/_TEMPLATE.md`, `docs/rfc/_TEMPLATE.md`, `docs/adr/_TEMPLATE.md` | Campos de mechanismos → Incrementos 1–3. |
| `docs/architecture/*`, `docs/working/*`, `ROADMAP.md`, `README.md`, `docs/ADOPTION.md`, `docs/MIGRATION.md`, `docs/source-layout.md`, `docs/AUDITORIA_DOCUMENTACION.md` | Fuera del alcance documental de la Unidad A. |
| `protocol/.agents/VERSION` | Sin bump (docs-only, RFC-69). |
| `dist/` | Se regenera por CI en tags; no se edita a mano (`AGENTS.md:Do NOT`). |

La expectativa por defecto es `DEV governance/documentation only`.

## 5. Estado actual del repositorio (reconstrucción factual)

**[OBSERVED]** Verificado con git, checkers y pytest al 2026-09-02:

| Dato | Valor observado |
|---|---|
| Branch | `dev` |
| HEAD | `3acf439` (`docs(repo): add change lifecycle master action plan (plan 94, RFC-75)`) |
| Working tree | `M docs/plans/INDEX.md` (registro de este plan, Vigésima séptima serie) + `?? docs/plans/95-change-lifecycle-unit-a-increment-0.md` (este plan, sin commitear) |
| Respecto a `origin/dev` | ahead 3 (commits `c166520` ADR-15/16, `352ad18` RFC-75 y `3acf439` plan 94 sin push) |
| `protocol/.agents/VERSION` | `10.3.0` |
| RFC-75 | `Accepted` (2026-09-01; implementación pendiente) (`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`) |
| ADR-15/16 | `Accepted` (2026-08-31) (`docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`) |
| RFC-56 / RFC-69 | `Accepted` |
| Plan 94 | Commiteado (2026-09-02, `3acf439`): archivo + registro en `docs/plans/INDEX.md` + ítem `(plan 94, RFC-75)` en `CHANGELOG.md:[Unreleased]`; `**Status:** Executed` según su header (sin `Closed`: sin mecanismo de checkpoint) |
| Checkers | En verde al 2026-09-02: `check_protocol_invariants.py`, `check_plan_citations.py`, `check_plan_structure.py`, `check_taxonomy_coherence.py`, `check_session_artifacts.py`, `check_version_state.py` (warnings esperados de dev) |
| pytest `tests/` | Post-cierre (2026-09-02, plan 94 en HEAD): `339 passed, 1 failed` — solo el fallo preexistente y ajeno del test `test_store_rebuild_is_derived_and_deterministic` de `tests/test_project_segment.py` (timestamp fijo vs reloj real: `STALE` esperado `FRESH`); el test de contención `test_no_citation_target_depends_on_working_tree` vuelve a PASS (§15, §19) |
| Plan 95 | No existía al inicio de esta tarea; este documento lo crea; permanece sin commitear, status `Aprobado para ejecución` |

**[DERIVED]** Implicaciones para la ejecución de la Unidad A:

- La dependencia Git de este plan quedó resuelta: el plan 94 fue commiteado
  (2026-09-02, commit `3acf439`) junto con su registro en INDEX y su ítem en
  `[Unreleased]`; el commit no incluyó este plan (su archivo y su registro en
  INDEX permanecen en el working tree).
- Con el plan 94 en HEAD, el test de contención
  `test_no_citation_target_depends_on_working_tree` vuelve a PASS y el único
  fallo de pytest restante es el temporal preexistente (§15, §19). Histórico:
  mientras el plan 94 estuvo sin versionar se observó `338 passed, 2 failed`
  (timestamp + contención), condición ya resuelta.
- Los archivos que la Unidad A modifica (`docs/CONVENTIONS.md`,
  `docs/VERSIONING.md`, `AGENTS.md`, `docs/AGENTS.md`, `CHANGELOG.md`) no están
  sucios hoy: el único cambio de working tree además de este plan es su propio
  registro en `docs/plans/INDEX.md`.

## 6. Autoridad y fuentes de verdad

**[NORMATIVE]** Se aplica ADR-16 sin modificación
(`docs/adr/16-change-lifecycle-authority.md:Decisión`):

| Clase | Fuente | Rol en esta Unidad |
|---|---|---|
| FACTUAL | Git, checkers, pytest, `protocol/.agents/VERSION`, tags | Verifica el estado (§5) y la validación (§15); nunca autoridad normativa |
| NORMATIVE | RFC-75 `Accepted`, ADR-15/16 `Accepted`, Plan 94 `Executed`, convenciones | Fuente del contenido semántico a escribir en los docs de gobernanza |
| DECISION | Humano/mantenedor | Autoriza la ejecución y acepta la desviación documentada de pytest al cierre (§21); el commit del plan 94 quedó resuelto por el mantenedor (2026-09-02, `3acf439`) |
| RELEASE | Tag en `master`, `dist` | No aplica: Unidad A docs-only, sin release (§17) |
| DESCRIPTIVE | INDEX | Registro/navegación; nunca autoridad (`docs/AGENTS.md:INDEX y CONVENTIONS`) |

Reglas que este plan preserva:

- **No se crea una autoridad nueva ni un registro de decisiones nuevo.** Las
  decisiones de ejecución de la Unidad A viven en este plan y en los docs que
  modifica.
- **INDEX es descriptivo**; su actualización ocurre después de los archivos
  fuente, en el commit del plan (`docs/VERSIONING.md:7. Estados de planes y RFCs`).
- **El checker produce evidencia factual, no autoridad normativa**
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`); un fallo del
  checker se corrige contra la fuente, nunca declarando PASS.
- **Un plan no modifica silenciosamente la decisión normativa que implementa**
  (AU-5, ADR-16): la Unidad A escribe semántica derivada de RFC-75/Plan 94, no
  decisiones nuevas. Cualquier desvío real se escala como BLOCKER/OPEN (§20,
  §23).

## 7. Modelo objetivo vs operationalización

### 7.1 Regla transversal (se escribe en `docs/CONVENTIONS.md` en U1)

**[NORMATIVE]** Regla definida por Plan 94 y RFC-75:

> **Target semantics vs operationalization.** Una regla definida por RFC-75
> puede formar parte del modelo normativo objetivo antes de que exista su
> mecanismo de enforcement. Una regla del lifecycle se vuelve operacionalmente
> exigible solo después de que el incremento que materializa su mecanismo es
> aceptado. Ningún incremento anterior invalida artifacts legacy ni impone
> requisitos sin mecanismo.

### 7.2 Tabla de conceptos del Incremento 0

| Concepto | Target semantics | Mecanismo actual | Enforcement en A |
|---|---|---|---|
| Validation Anchor | Toda validación registrada lleva anchor (declared scope, command-set, effective inputs, observed dependencies, environmental factors, Scoped Content Identity); validez relativa al anchor (CL-1/CL-2, VC-1) | Ninguno (validaciones reportadas en notas sin anchor) | No — mecanismo en Incremento 1 (Unidad B); solo semántica objetivo |
| Git Checkpoint | `Closed` exige estado Git verificable con consistencia checkpoint↔anchor; `Committed` = estado del repo, no status (CL-3/4/5, GC-1) | Git existe; `Closed` no definido como condición derivada | No — mecanismo en Incremento 3 (Unidad B); solo semántica objetivo (§9.2, U2) |
| Finding / Correction / Revalidation | Refs calificadas `<artifact>:F-<n>`, N:M, estados, revalidación trazable (CL-6/7/8, LC-1) | Tracker de auditoría como patrón; sin refs en lifecycle | No — mecanismo en Incremento 2 (Unidad C) |
| Pending Decision | Decisión pendiente per-artifact con owner/escalación/resolución; nunca desaparece (PC-1) | Notas/conversación | No — mecanismo en Incremento 2 (Unidad C) |
| Change Level | `Level = max(5 dimensiones)`; eje independiente de RFC-56; L0 provisional (CL-10) | No declarado en artifacts | No — solo modelo escrito en `docs/CONVENTIONS.md` (U1); la clasificación operacional (intake fallback) es del Incremento 1 |
| Series | Identidad derivada de declaraciones + relaciones verificables; sin entidad/registry; INDEX = vista (AU-4) | Declarada informalmente (`Serie:` en headers) sin verificación | No — solo semántica objetivo en `docs/AGENTS.md:Identity` (U4); la regla operacional de declaración/verificación es del Incremento 1 |
| Condiciones derivadas (vocabulario) | `Verified ⊆ Executed ⊆ Closed ⊆ Promoted ⊆ Released`; `Closed ≠ release` | Status existentes de Plan/RFC/ADR | Semántica escrita en `docs/VERSIONING.md:7. Estados de planes y RFCs` (U2); sin status nuevos |

**[DERIVED]** La ausencia de enforcement en el Incremento 0 no contradice a
RFC-75 y no invalida artifacts legacy: los planes 86–93 y los RFCs 71–74 siguen
válidos con la semántica que tenían (ausencia de campos nuevos = legacy;
`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).

### 7.3 Vocabulario del Incremento 0

El vocabulario objetivo mínimo que la Unidad A debe habilitar (distinguir
siempre definición vs mecanismo):

| Concepto | Estado semántico | Hogar normativo |
|---|---|---|
| Change | Término coloquial; NO entidad | RFC-75 Terminología |
| Change Lifecycle / Change Level | Definidos; Level con ejes y L0 | RFC-75 Mecanismo 2; CONVENTIONS (U1) |
| intake / decision / execution / validation | Etapas del modelo; sin mecanismos nuevos | RFC-75 Modelo de lifecycle |
| RFC / ADR / Plan | Artifacts existentes con status propios | CONVENTIONS; VERSIONING §7 |
| checkpoint / closure | Semántica objetivo; mecanismo en Incremento 3 | VERSIONING §7 (U2) |
| anchor / finding / correction / revalidation / pending decision | Semántica objetivo; mecanismos en Incrementos 1/2 | VERSIONING §7 (U2) + RFC-75 |
| promotion / release | Relación con merge/tag; sin cambios | VERSIONING §1/§6 |
| series | Identidad derivada; regla operacional en Incremento 1 | docs/AGENTS.md Identity (U4) |
| continuity / handoff | Continuidad = propiedad; handoff fuera de alcance | RFC-75 Principios arquitectónicos |

No se presenta ninguna definición semántica como si ya tuviera enforcement.

## 8. Observability baseline (Incremento 0)

**[NORMATIVE]** RFC-75 define cuatro métricas permanentes (SHOULD, derivadas de
campos, sin backend ni writer obligatorio) y deja las métricas de coordinación
como EXPERIMENTAL/DEFERRED (`docs/rfc/75-change-lifecycle.md:Mecanismo 13 — Observability`).
El Plan 94 fija que el Incremento 0 establece las **definiciones / schema
baseline**, no mediciones operacionales
(`docs/plans/94-change-lifecycle-master-action-plan.md:17. Estrategia de telemetría`).

| Métrica | Definición (schema baseline) | Datos que la alimentarán | Dependencia | Estado en A |
|---|---|---|---|---|
| Validation anchor coverage | % de validaciones registradas con anchor reproducible sobre validaciones con campos registrables | Campos de anchor en notas/templates | Incremento 1 | Definida; sin medición |
| Finding lineage coverage | % de correcciones con ref de lineage origen→corrección→revalidación | Refs `artifact:F-n` | Incremento 2 | Definida; sin medición |
| Stale validation rate | % de validaciones ancladas cuyo anchor cambió sin revalidación/marca de stale | Anchor + revalidación | Incrementos 1+2 | Definida; sin medición |
| Git closure anomalies | % (o conteo) de cierres/planes con anomalías de closure (Executed sin commit, Promoted sin Closed, etc.) | Checkpoint + estados | Incremento 3 | Definida; sin medición |

Reglas del schema baseline que la sección nueva de `docs/VERSIONING.md` (U2)
debe declarar:

- **Schema ≠ medición**: la Unidad A no produce datos operacionales de estas
  métricas (dependen de campos de los Incrementos 1/3/2).
- **Legacy excluido del denominador**; 0 registros = `not applicable /
  insufficient sample`, no "0% compliance" (RFC-75 Mecanismo 13).
- **Ninguna métrica es gate de release**; solo informan.
- **Sin backend, sin writer obligatorio, sin thresholds**.
- Métricas de coordinación (cross-agent, handoffs, pending count, revalidación
  frequency): EXPERIMENTAL/DEFERRED, dependen del track del Incremento 5.
- El gate del Incremento 4 (automatización) se evalúa con los datos de
  lifecycle reales producidos por las unidades B/C, no con el schema del 0
  (no circular; `docs/plans/94-change-lifecycle-master-action-plan.md:17. Estrategia de telemetría`).

## 9. Cambios file-by-file

### 9.0 Tabla resumen

| File | Change | Reason | Authority | Risk | Validation |
|---|---|---|---|---|---|
| `docs/CONVENTIONS.md` | Modificar (agregar subsecciones bajo `## Convenciones`) | Escribir modelo de Change Levels, frontera DEV-only y regla transversal en la normativa del repo | RFC-75 (`Mecanismo 2 — Change Levels`, `Dev vs Protocol`); Plan 94 §13 | Duplicación con RFC-75 | `check_plan_citations.py`; revisión semántica |
| `docs/VERSIONING.md` | Modificar (§7 extendido + sección nueva §11) | Semántica de condiciones derivadas + observability schema baseline en la política de estados | ADR-15 (`Decisión`), RFC-75 (`Modelo de lifecycle`, `Mecanismo 13 — Observability`), Plan 94 §7/§17 | Reencuadre de estados; medición prematura | `check_plan_citations.py`; revisión semántica |
| `AGENTS.md` | Modificar (`## Task lifecycle`, `## Do NOT`) | Vocabulario operativo para agentes; frontera DEV/Protocol | RFC-75 (`Dev vs Protocol`); Plan 94 §18 Unidad A | Instrucciones confusas si no se marca operationalization | `check_plan_citations.py`; revisión semántica |
| `docs/AGENTS.md` | Modificar (`### Identity`) | Serie = identidad derivada (semántica objetivo) en la taxonomía | RFC-75 (`Mecanismo 11 — Series / Continuity`); Plan 94 §12 | Registry prematuro en Incremento 1 | `check_plan_citations.py` |
| `CHANGELOG.md` | Modificar al ejecutar (`## [Unreleased]`) | Ítem docs-only `(plan 95, RFC-75)` | RFC-69 (`Versionado`); `docs/VERSIONING.md:10. Definition of Done` | Ítem duplicado/omitido | Revisión manual; `check_version_state.py` |
| `docs/plans/INDEX.md` | Modificar (creación: serie + fila; ejecución: espejo status) | Registro estructural obligatorio del plan | `docs/plans/_TEMPLATE.md` (comentario de registro); `tools/check_plan_structure.py` | Registro fuera de orden de serie | `check_plan_structure.py` |

### 9.1 U1 — `docs/CONVENTIONS.md`

- **Path:** `docs/CONVENTIONS.md`.
- **Operación:** agregar al final del documento, bajo la sección existente
  `## Convenciones` (después del último bullet «Layout fuente (RFC-55)»), tres
  subsecciones nuevas (`###`) en español, con el estilo normativo del archivo y
  citas resolubles.

#### U1a — `### Change Lifecycle DEV — alcance y frontera`

Contenido requerido (párrafos/bullets):

- El Change Lifecycle (RFC-75) gobierna la evolución de ARgentOS DEV: `AGENTS.md`
  raíz, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, templates y checkers dev.
- No gobierna automáticamente la evolución del Protocol: un cambio con efecto
  payload sigue RFC-56 (clases A/B/C y autorización).
- No se crean workflow/policy/state machine/artifact/skill compartidos entre
  DEV y Protocol; no hay herencia automática. Principios potencialmente
  transferibles (revalidación ante continuidad; persistir ≠ materializar;
  separación evidencia factual / autoridad normativa) quedan como principios,
  no mecanismos (`docs/rfc/75-change-lifecycle.md:Dev vs Protocol`).

#### U1b — `### Change Lifecycle — Change Levels (modelo objetivo)`

Contenido requerido:

- `Level = max(coordination, scope, architectural impact, release impact,
  duration/complexity)`; el número de commits no es dimensión
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`).
- Los ejes y los umbrales coarse (0–3) son decisión de RFC-75; este documento
  los referencia sin duplicar la tabla.
- Change Level y clase RFC-56 son **ejes independientes**: una Clase A pequeña
  puede ser L2; una Clase C grande puede ser L2/L3 por scope; un cambio
  runtime-only tiene Level sin clase.
- L0 es el nivel mínimo (1 agente, 1 sesión, superficie de 1 archivo, sin
  cambio estructural, sin versión, <1 sesión) y es **provisional**: al activarse
  un trigger (finding, revalidación requerida, decisión ADR-worthy, múltiples
  RFCs, impacto release-critical o arquitectónico) el Level se recomputa antes
  de continuar (`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`).
- La maquinaria del lifecycle escala con el Level (CL-10); la matriz
  operacional L0–L3 y el reparto de decisiones viven en el Plan 94
  (`docs/plans/94-change-lifecycle-master-action-plan.md:9. Economía de Change Levels`),
  no se duplican aquí.
- La **clasificación operacional** (registro del Level en el primer artifact /
  tracker e intake fallback) se materializa en el Incremento 1; este punto es
  semántica objetivo, no exigencia vigente (regla transversal, U1c).

#### U1c — `### Regla transversal — target semantics vs operationalización`

Contenido requerido:

- Texto de la regla (§7.1), en español, con referencia normativa a
  `docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación incremental`
  y a `docs/rfc/75-change-lifecycle.md:Rollout incremental`.
- Mapa de aplicabilidad: VC-1 (anchor) → Incremento 1; GC-1 (checkpoint) →
  Incremento 3; LC-1/PC-1 (findings/pending) → Incremento 2. Ninguna regla
  objetivo se vuelve operacionalmente exigible antes del incremento que
  materializa su mecanismo.
- Ningún incremento anterior invalida artifacts legacy ni impone requisitos
  sin mecanismo; ausencia de campos nuevos = legacy, no invalidez
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).
- `checker output = factual evidence ≠ normative authority`; "anchor missing"
  es GAP, no "validation invalid" (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).

### 9.2 U2 — `docs/VERSIONING.md`

- **Path:** `docs/VERSIONING.md`.
- **Operación:** (a) extender `## 7. Estados de planes y RFCs`; (b) agregar una
  sección nueva al final del documento (después de `## 10. Definition of Done`),
  numerada `## 11. Métricas del Change Lifecycle (observability schema baseline)`,
  para no renumerar las secciones 8–10 ni romper citas existentes.

#### U2a — §7: condiciones derivadas y semántica de cierre

Agregar, al final de §7 (después del bullet del INDEX espejo), un bloque con
los siguientes contenidos (sin crear status nuevos):

- Los únicos status son los existentes de Plan/RFC/ADR; las condiciones del
  Change Lifecycle son derivadas, no una state machine
  (`docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`).
- `Executed` = implementación + validación (CL-4); puede existir sin commit.
- `Committed` es estado del repositorio, no un status de Plan (CL-5).
- `Closed` es una condición derivada: `Executed` + governance aplicable +
  checkpoint + consistencia checkpoint↔anchor (GC-1). El mecanismo de
  checkpoint se materializa en el Incremento 3; hasta entonces esta semántica
  es objetivo y el cierre operativo vigente sigue el DoD de §10
  (regla transversal, `docs/CONVENTIONS.md:Convenciones`).
- `Closed ≠ Released`; un plan docs-only se cierra sin release (RFC-69).
- `Promoted` = merge `dev → master` verificado; `Released` = tag inmutable;
  `Abandoned` = Plan `Superseded` con motivo.
- Cadena de implicación `Verified ⊆ Executed ⊆ Closed ⊆ Promoted ⊆ Released`
  (semántica objetivo; la verificabilidad operacional de cada condición llega
  con el incremento que materializa su mecanismo) y
  anomalías: `Closed` sin `Verified` es inválido; `Promoted` sin `Closed` es
  anomalía; `Released` sin `Verified` es violación de gobernanza
  (`docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`).
- Semántica de `Aprobado para ejecución` (RFC-75 Mecanismo 5): autorizado a
  ejecutar cuando los criterios de entrada se cumplen; si no, el gate pendiente
  se documenta como aclaración, sin status nuevo.

#### U2b — §11: observability schema baseline

Contenido requerido de la sección nueva:

- Propósito: schema baseline de las métricas del Change Lifecycle; no produce
  medición operacional en el Incremento 0.
- Tabla de las cuatro métricas permanentes (definición, fuente de datos futura,
  incremento que la habilita, estado actual = schema) según §8.
- Reglas: legacy excluido del denominador; 0 registros = `not applicable /
  insufficient sample`; SHOULD, ninguna es gate; sin backend ni writer
  obligatorio; sin thresholds; métricas de coordinación EXPERIMENTAL/DEFERRED
  (Incremento 5).
- Referencias normativas: `docs/rfc/75-change-lifecycle.md:Mecanismo 13 — Observability`
  y `docs/plans/94-change-lifecycle-master-action-plan.md:17. Estrategia de telemetría`.

### 9.3 U3 — `AGENTS.md` (raíz)

- **Path:** `AGENTS.md`.
- **Operación:** ajustar `## Task lifecycle` y agregar un bullet a `## Do NOT`.
  El idioma del archivo es inglés; el texto nuevo debe escribirse en inglés.

#### U3a — `## Task lifecycle`

Requerimientos semánticos del texto resultante (se conserva el pipeline
autorizar → ejecutar → verificar → cerrar → commitear → promover, pero cada
etapa queda alineada con RFC-75):

- `Executed` (plan status) = implementación + validación; puede existir antes
  del commit.
- `Committed` = estado del repositorio (commit atómico en `dev`), no un status
  de Plan.
- `Closed` = condición derivada (plan `Executed` + governance + Git checkpoint +
  consistencia) como **semántica objetivo**: el mecanismo de checkpoint se
  materializa en el Incremento 3 del Change Lifecycle; hasta entonces el cierre
  operativo vigente sigue el DoD (`docs/VERSIONING.md:10. Definition of Done`)
  y el commit atómico es un hecho Git factual, no un registro de checkpoint.
- `Released` = promovido a `master` con tag anotado; `Closed ≠ Released`; un
  plan docs-only se cierra sin release.
- Se mantienen las frases finales actuales: "A plan is done when all of that is
  verified and committed; a version is published when it is also tagged on
  `master`", con la semántica precisa referenciada a `docs/VERSIONING.md` §7
  (estados) y `docs/CONVENTIONS.md:Convenciones` (normativa).

#### U3b — `## Do NOT`

Agregar un bullet que declare (en inglés):

- El Change Lifecycle DEV (RFC-75) gobierna este repositorio de desarrollo, no
  el Protocol: no se implementan sus mecanismos (anchors, checkpoints,
  findings, pending, series registries, state machines) dentro de
  `protocol/.agents/` ni se comparte machinery de lifecycle entre DEV y
  Protocol.

### 9.4 U4 — `docs/AGENTS.md`

- **Path:** `docs/AGENTS.md`.
- **Operación:** en `### Identity`, agregar un bullet (o una oración) que
  declare la semántica objetivo de serie, citando a RFC-75:
  - Una **serie** (p. ej. la serie «Change Lifecycle») no es un artifact ni un
    registry: es una identidad derivada de declaraciones en headers + relaciones
    verificables entre artifacts; los INDEX la reflejan como vista descriptiva,
    nunca autoritativa (`docs/rfc/75-change-lifecycle.md:Mecanismo 11 — Series / Continuity`).
  - La regla operacional (declaración `Serie:` + verificación de relaciones) se
    materializa en el Incremento 1; aquí solo queda fijada la semántica.

### 9.5 U5 — `CHANGELOG.md` (al ejecutar)

- **Path:** `CHANGELOG.md`.
- **Operación:** agregar el ítem del plan 95 bajo `## [Unreleased]`, en la
  subsección que el mantenedor use para cambios de gobernanza docs-only
  (precedente: plan 83 en `### Changed`), con el formato
  `**<Título del cambio>** (plan 95, RFC-75): <descripción>` y la nota
  "cambio docs-only: sin `VERSION` bump ni tag (RFC-69)".
- Contenido sugerido del ítem: semántica del Change Lifecycle DEV (condiciones
  derivadas, modelo de Change Levels, frontera DEV/Protocol, serie como
  identidad derivada) y observability schema baseline de las métricas de
  lifecycle en la gobernanza DEV.

### 9.6 U6 — Gobernanza y traza (al ejecutar)

- **Path:** `docs/plans/INDEX.md` + este archivo.
- **Operación:** al completar la ejecución y la validación:
  1. Actualizar el `**Status:**` de este plan a `Executed` y agregar `## Nota de
     ejecución` con fecha, verificación realizada, resultado real de pytest y
     estado Git.
  2. Actualizar la fila de este plan en `docs/plans/INDEX.md` (mirror
     descriptivo: status `Executed` + nota; después de los archivos fuente;
     `docs/VERSIONING.md:7. Estados de planes y RFCs`).
  3. No tocar RFC-75 (ejecutar un plan no cambia la RFC), ni ADRs, ni otros
     planes, ni otros INDEX.
  4. Commit atómico en `dev` (Conventional Commit en inglés, p. ej.
     `docs(repo): implement change lifecycle unit A semantics (plan 95, RFC-75)`),
     **solo si el working tree está libre de cambios ajenos** (§16): el plan 94
     ya está commiteado (`3acf439`), por lo que al ejecutar la Unidad A el
     commit atómico puede incluir este plan + su registro en INDEX + los docs
     de §9 + el ítem de `[Unreleased]`; hasta entonces este plan permanece
     `Aprobado para ejecución`, sin `Executed` ni `Closed` (dogfooding, §13).

## 10. Relaciones documentales

- **Registro de este plan:** serie nueva en `docs/plans/INDEX.md` (Vigésima
  séptima serie) con la fila `95-change-lifecycle-unit-a-increment-0.md`,
  status `Aprobado para ejecución`. Requisito estructural
  (`tools/check_plan_structure.py`) y de plantilla (`docs/plans/_TEMPLATE.md`).
- **Espejo al ejecutar:** la misma fila pasa a `Executed` con nota (§9.6).
- **Sin cambios** en `docs/rfc/INDEX.md`, `docs/adr/INDEX.md` ni INDEX de
  working.
- **Disciplina de cita:** cada concepto tiene un solo hogar normativo y los
  demás docs lo referencian; las secciones nuevas de `docs/VERSIONING.md`
  (§7 ampliado, §11) no renumeran secciones existentes para no romper citas
  vigentes (`docs/CONVENTIONS.md:Convenciones`). Las referencias de este plan
  resuelven contra el repo al momento de la redacción.

## 11. Vocabulario y terminología

Este plan usa el vocabulario de RFC-75 (`docs/rfc/75-change-lifecycle.md:Terminología`)
sin redefinirlo:

| Término | Uso en este plan |
|---|---|
| Change | Evolución del repo; coloquial, no entidad |
| Change Level | Eje de rigor/machinery L0–L3; `max(...)` |
| RFC-56 class | Eje de autorización de payload A/B/C; independiente del Level |
| Anchored validation | Validación con anchor (mecanismo futuro, Incremento 1) |
| Git checkpoint | Relación closure↔estado Git (mecanismo futuro, Incremento 3) |
| Closed | Condición derivada; no status |
| Serie | Identidad derivada; sin entidad/registry |
| Finding | Relación de lineage con ref calificada; sin entidad (Incremento 2) |

En los docs que la Unidad A modifica, los términos se escriben con la misma
distinción: definición de RFC-75 ≠ mecanismo materializado ≠ regla
operacionalmente exigible.

## 12. Cambios al modelo de autoridad

**[NORMATIVE]** Ninguno. La Unidad A no crea autoridad nueva, no modifica
ADR-16, no convierte INDEX en autoridad y no hace que checkers decidan
normativamente (§6). Los textos nuevos citan a RFC-75/ADR-15/16 como fuente
normativa; `docs/CONVENTIONS.md` y `docs/VERSIONING.md` son los hogares de
política, no nuevas autoridades.

## 13. Dogfooding

**[OBSERVED + DERIVED]** El propio repositorio demuestra el vocabulario que la
Unidad A escribe:

```text
RFC-75 (Accepted, NORMATIVE)
  ↓
Plan 94 (Executed → Committed 2026-09-02, commit 3acf439 → no Closed:
         sin mecanismo de checkpoint hasta el Incremento 3)
  ↓
Plan 95 (Aprobado para ejecución → al ejecutar Executed → Committed en su
         commit atómico; Closed solo cuando exista checkpoint, Inc. 3)
```

- RFC-75 está `Accepted` (implementación pendiente): la aceptación normativa no
  implica ejecución (`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`).
- El Plan 94 está `Executed` y **commiteado** (2026-09-02, `3acf439`): bajo la
  semántica que él mismo define, `Committed` es estado del repositorio y, sin
  checkpoint (Incremento 3), no es `Closed`
  (`docs/plans/94-change-lifecycle-master-action-plan.md:Nota de ejecución`).
- El Plan 95 será el segundo sujeto: no puede declararse `Closed` hasta que el
  Incremento 3 materialice el checkpoint; su ejecución lo dejará `Executed` y
  su commit atómico lo dejará `Committed`.
- El vocabulario se usa de inmediato al redactar los planes 96+ (unidades B/C/D)
  y en las notas de ejecución de este propio plan
  (`docs/plans/94-change-lifecycle-master-action-plan.md:19. Estrategia de dogfooding`).

Ningún estado futuro se declara como ocurrido: las afirmaciones de estado en
este documento son las del §5.

## 14. Orden de implementación y dependencias

Dependencias derivadas del repo (no un orden genérico):

```text
Paso 0 (premisas) → U1 CONVENTIONS (normativa base)
                  → U2 VERSIONING §7 + §11 (semántica de estados + métricas)
                  → U3 AGENTS.md (task lifecycle, frontera)
                  → U4 docs/AGENTS.md (Identity: serie)
                  → U5 CHANGELOG [Unreleased] (ítem docs-only)
                  → U6 gobernanza/INDEX/status del plan + Nota de ejecución
                  → Validación (batería + pytest real + consistencia)
                  → Cierre (gate del mantenedor; commit atómico si el árbol
                    está limpio; §16)
```

Orden recomendado de redacción: gobernanza (U1–U2) → instrucciones (U3) →
taxonomía (U4) → traza (U5–U6) → validación y consistencia. No hay
dependencias cruzadas entre archivos que obliguen a otro orden; la restricción
real es no dejar estados intermedios donde un doc cite una sección inexistente
de otro.

## 15. Plan de validación

Al ejecutar, correr exactamente:

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

Reglas:

- **Nunca declarar PASS si pytest devuelve FAILED.** Reportar el resultado real
  como desviación documentada aceptada por el mantenedor, jamás como batería
  verde total (`docs/plans/94-change-lifecycle-master-action-plan.md:24.1 Política de interpretación`).
  Estado post-cierre (2026-09-02, plan 94 commiteado): `339 passed, 1 failed`
  (solo el fallo de timestamp preexistente; el test de contención vuelve a
  PASS). Histórico: con el plan 94 sin versionar se observó
  `338 passed, 2 failed` (timestamp + contención); ya resuelto. Ningún
  resultado con FAILED se reporta como PASS.
- **No modificar** `tests/test_project_segment.py` ni ningún otro test.
- `check_dist_sync.py` es local-only y se espera rojo en `dev` por diseño; no es
  parte de la batería de esta unidad (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
- H13 por juicio: no aplica cambios de estructura del payload; sí aplica la
  revisión semántica de los textos nuevos (vocabulario, frontera, autoridad).
- Consistencia documental: referencias resolubles, INDEX coherente,
  terminología única por concepto, autoridad sin cambios, versionado intacto,
  scope respetado (diff acotado a los archivos de §9).
- Evidencia Git al reportar: branch, HEAD, working tree, archivos cambiados,
  diff y estado final; sin hashes inventados.

## 16. Frontera Git y checkpoint

- La Unidad A **no implementa** Validation Anchors ni Git Checkpoints: no
  agrega metadata Git, no agrega hooks, no agrega scripts y no inventa formatos
  de anchor (`docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors`,
  `docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`).
- La semántica objetivo que se escribe (§9.2 U2a) no autoriza exigir anchors ni
  checkpoints en los planes 95+ hasta sus incrementos respectivos.
- Al reportar estado Git, se usan los valores reales: branch `dev`, HEAD
  actual (plan 94 commiteado en HEAD), working tree con los cambios de §9; sin
  inventar SHAs futuros.
- **Commit:** la convención exige commit atómico en `dev`
  (`docs/VERSIONING.md:10. Definition of Done`). La dependencia Git quedó
  resuelta: el plan 94 fue commiteado (2026-09-02, `3acf439`) con su registro
  en INDEX y su ítem en `[Unreleased]`, sin incluir este plan. Al ejecutar la
  Unidad A, el commit atómico incluye este plan + su registro en INDEX + los
  docs de §9 + el ítem de `[Unreleased]`; el agente no commitea si aparecen
  cambios ajenos no documentados (§5, §20).

## 17. Versión / changelog / release

- **Vía:** plan docs-only (no toca `protocol/.agents/`): no produce versión de
  protocolo; registra ítem en `CHANGELOG.md:[Unreleased]` con `(plan 95,
  RFC-75)`, sin `VERSION` bump ni tag (`docs/rfc/69-documentation-taxonomy-and-layout.md:Versionado`).
- **Sin promoción** `dev → master` en esta unidad: promoción/release es decisión
  del mantenedor y no parte del cierre de la Unidad A (`Closed ≠ Released`;
  `docs/VERSIONING.md:1. Ramas y roles`).
- El ítem de `[Unreleased]` del **plan 94** ya fue agregado en su commit de
  cierre (2026-09-02, `3acf439`): este plan no lo duplica (§19).

## 18. Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación | Detección |
|---|---|---|---|---|
| Duplicación de documentación (RFC-75 ya define el modelo) | Media | Terminología divergente | Hogar único por concepto (§10); citas en vez de copia de tablas | Revisión de diff; `check_plan_citations.py` |
| Terminology drift (términos con enforcement fingido) | Media | Planes futuros exigen machinery inexistente | Regla transversal escrita en CONVENTIONS (U1c) y en VERSIONING §7 (U2a) | Revisión semántica; auditoría adversarial (§25) |
| Authority ambiguity (INDEX/checker como autoridad) | Baja | Conflictos normativos mal resueltos | Sección de autoridad explícita (§6); ADR-16 sin cambios | Revisión; §25-A |
| Accidental DEV/Protocol coupling | Baja | Contaminación del payload | Scope guard (§4.2); frontera en AGENTS (U3b) | `git diff` sin `protocol/`; §25-C |
| Premature enforcement (exigir anchors/checkpoints) | Media | Burocracia y fricción L0/L1 | Regla transversal + mapa de incrementos (§7) | Revisión; §25-E |
| Premature automation (crear checker) | Baja | Checker sin datos | Out-of-scope explícito (§4.2); nada de `tools/`/`tests/` | `git diff` sin tools/tests; §25-F |
| Accidental scope expansion (Incremento 1+ en A) | Media | Plan no derivable | Unidad A estricta; tabla de exclusiones (§4.2) | §25-B/D |
| False-green validation (reportar PASS con test FAILED) | Media | Violación de la política | Regla §15; reporte `339 passed, 1 failed` | Resultado real de pytest en nota |
| Retroactive invalidation de legacy | Media | Planes/RFCs históricos reescritos | Legacy excluido (§7.2); sin backfill (§4.2) | Revisión; §25-N |
| Release/versioning side effects | Baja | Bump/tag sin autoridad | Docs-only declarado (§17); sin tocar VERSION | `check_version_state.py` |
| Renumeración de secciones de VERSIONING | Baja | Citas rotas | §11 nueva al final, sin renumerar 8–10 (§9.2) | `check_plan_citations.py` |
| Ítem changelog duplicado/omitido | Baja | Traza incompleta | U5 con formato y sección exactos (§9.5) | Revisión manual del diff |

## 19. Deuda existente y desviaciones conocidas

| Ítem | Estado | Impacto en esta unidad |
|---|---|---|
| El test `test_store_rebuild_is_derived_and_deterministic` de `tests/test_project_segment.py` (timestamp fijo vs reloj real) | Preexistente y ajeno (2026-09-02) | Condiciona el cierre: desviación documentada que requiere aceptación del mantenedor; NO se reporta como PASS (§15, §21) |
| Plan 94 sin commitear (histórico) | RESUELTO (2026-09-02): commit atómico `3acf439` con plan file + registro en INDEX + ítem `(plan 94, RFC-75)` en `[Unreleased]` | Ya no es gate: el test de contención volvió a PASS; este plan solo comparte el INDEX con su propio registro (§16) |
| `dev` ahead 3 de `origin/dev` (plan 94, RFC-75 y ADR-15/16 sin push) | Estado, no defecto | Resolver en el próximo push del mantenedor |
| Intro de `docs/plans/INDEX.md` con snapshot "Estado al 2026-08-16" desactualizado | Menor; INDEX descriptivo | Sin acción en esta unidad (registro de la serie sí se actualiza) |
| `docs/VERSIONING.md:9. Estado actual (2026-08-17)` desactualizado | Menor; snapshot de releases | Sin acción en esta unidad |

## 20. Condiciones de detención (stop conditions)

El agente implementador **se detiene y escala** (no continúa automáticamente)
si ocurre alguna de:

- Contradicción objetiva entre RFC-75 y Plan 94 sobre el contenido de la
  Unidad A.
- Autoridad normativa ambigua para un cambio requerido por este plan.
- Archivo objetivo inexistente cuando debería existir (p. ej., alguna de las
  secciones citadas en §9 no resuelve).
- Necesidad de un cambio fuera del scope DEV (protocol/, runtime/, tests/,
  tools/ o `VERSION`).
- Necesidad de una decisión arquitectónica nueva no cubierta por RFC-75/Plan 94.
- Necesidad de crear una entidad/registry/state machine/skill/checker no
  autorizado.
- Checker que contradice una decisión normativa (se corrige la implementación,
  nunca la fuente normativa sin vía).
- Working tree con cambios ajenos no documentados en §5 (distintos de este plan
  y de su registro en INDEX).
- Cualquier indicio de que reportar PASS requeriría ocultar el fallo de pytest.

Ante un blocker real, el plan permanece `Aprobado para ejecución` sin ejecutar
y se escala al mantenedor (`docs/VERSIONING.md:7. Estados de planes y RFCs`).

## 21. Criterios de salida

La Unidad A está completa cuando:

- [ ] Scope: solo Unidad A / Incremento 0; sin mecanismos de Incrementos 1–5
      (diff sin `_TEMPLATE.md`, `tools/`, `tests/`, `protocol/`, `runtime/`).
- [ ] `docs/CONVENTIONS.md` contiene U1a/U1b/U1c (frontera DEV-only, modelo de
      Change Levels, regla transversal).
- [ ] `docs/VERSIONING.md` §7 contiene la semántica de condiciones derivadas
      (U2a) y existe la sección §11 con el schema baseline de las cuatro
      métricas (U2b).
- [ ] `AGENTS.md` raíz alinea `## Task lifecycle` (U3a) y declara la frontera
      DEV/Protocol en `## Do NOT` (U3b).
- [ ] `docs/AGENTS.md:Identity` declara la serie como identidad derivada (U4).
- [ ] Ítem `(plan 95, RFC-75)` en `CHANGELOG.md:[Unreleased]` (U5); sin
      `VERSION` bump ni tag.
- [ ] Registro de espejo en `docs/plans/INDEX.md` (fila + serie, §9.6); este
      plan con `**Status:** Executed` y `Nota de ejecución`.
- [ ] Vocabulario consistente; authority model sin cambios; target semantics
      diferenciada de enforcement; observability baseline definida sin fingir
      medición.
- [ ] Checkers aplicables PASS; pytest reportado con resultado real (`339
      passed, 1 failed`, fallo de timestamp preexistente) como desviación
      documentada; tests preexistentes no modificados.
- [ ] Estado Git reproducible y reportado (branch, HEAD, working tree, diff
      acotado a §9); sin commits ni hashes inventados.
- [ ] Aceptación explícita del mantenedor de la desviación documentada de
      pytest (política §24.1 del plan 94; OPEN-2, §23) antes de declarar
      cierre. La dependencia Git del plan 94 quedó resuelta (OPEN-1).

## 22. Rollback

- **Documental:** `git revert` del commit del plan (o, si no hay commit propio,
  revertir manualmente los cambios de §9); los docs vuelven al estado previo.
- **Sin datos que migrar:** no hay campos nuevos, artifacts nuevos ni metadata.
- **Registros con vocabulario nuevo** si se revierte el incremento: se tratan
  como legacy (ausencia de mecanismo no invalida el texto revertido;
  `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).
- **Sin efectos de release:** no hay tag, VERSION ni `dist`.

## 23. Preguntas abiertas (OPEN)

| # | Pregunta / decisión | Clasificación | Resolución |
|---|---|---|---|
| OPEN-1 | Commit del plan 94 como condición de entrada para el commit atómico de la Unidad A | RESUELTO (2026-09-02) | Commit atómico `3acf439` creado (plan 94 + registro en INDEX + ítem `[Unreleased]`), sin incluir este plan; ya no es gate |
| OPEN-2 | Aceptación de la desviación documentada de pytest (`339 passed, 1 failed`) para cerrar la unidad | RESUELTO (2026-09-02) | Decisión explícita del mantenedor (2026-09-02): OPEN-2 se resuelve por la vía alternativa prevista por este OPEN (resolver el test como deuda independiente antes del cierre, en lugar de aceptar la desviación). Corrección commiteada en `865e3ad`; pytest `340 passed, 0 failed`; checkers PASS; no se aceptó ninguna desviación de la suite. La validación original (`339 passed, 1 failed`) permanece como evidencia histórica (§15, §19, Nota de ejecución), sin reescribirse. |
| OPEN-3 | Wording final (lenguaje exacto) de los textos nuevos de U1–U4 | CAN DECIDE IN PLAN | El agente redacta en el idioma de cada doc (español en CONVENTIONS/VERSIONING/docs-AGENTS; inglés en AGENTS.md raíz) según los requerimientos de §9 |
| OPEN-4 | Posición exacta del ítem del plan 95 dentro de `[Unreleased]` | CAN DECIDE IN PLAN | Subsección de gobernanza docs-only (precedente plan 83 en `### Changed`) |

Ningún OPEN impide redactar ni ejecutar la Unidad A; OPEN-1 y OPEN-2 quedaron
resueltos (2026-09-02), este último por decisión explícita del mantenedor y por
la vía alternativa prevista en el propio OPEN-2 (resolver el test como deuda
independiente antes del cierre: commit `865e3ad`; pytest `340 passed, 0
failed`; checkers PASS). No se convirtió una preferencia del agente en decisión
del proyecto, no se aceptó desviación vigente alguna y no se declaró cierre:
Plan 95 permanece `Executed` + commiteado, sin `Closed` — el mecanismo formal
de checkpoint (GC-1) pertenece al Incremento 3 y sigue pendiente.

## 24. Trazabilidad

```text
Origen (mantenedor, 2026-09-02)
  → RFC-75 Accepted (rollout incremental: Incremento 0)
  → ADR-15/16 (invariantes y autoridad)
  → Plan 94 (Unidad A / Incremento 0; §17 observability; §18 roadmap)
  → Plan 95 (ESTE plan; Unidad A)
  → Ejecución documental (U1–U6)
  → Validación (batería + pytest real)
  → Cierre (gate del mantenedor; commit)
  → Unidades B/C/D (planes 96+) y track 5 (deferido)
```

Relaciones normativas citadas: `docs/rfc/75-change-lifecycle.md` (modelo,
mecanismos 1/2/5/6/7/11/13/14/15, rollout, invariantes), `docs/adr/15-change-lifecycle-continuity.md`
(CL-1..CL-10), `docs/adr/16-change-lifecycle-authority.md` (AU-1..AU-7),
`docs/plans/94-change-lifecycle-master-action-plan.md` (unidades, dogfooding,
deuda, política de batería verde). Este plan no autoriza cambios de payload
(RFC-56).

## 25. Auditoría adversarial del Plan 95 (A–O)

| Criterio | Verdict | Evidencia / mitigación |
|---|---|---|
| A. Authority | PASS | Cada decisión normativa cita RFC-75/ADR-15/16/Plan 94 (§6, §9); sin autoridad nueva; INDEX descriptivo |
| B. Scope | PASS | Solo Unidad A/Incremento 0; exclusiones explícitas (§4.2); diff objetivo acotado (§9) |
| C. Boundary | PASS | Cero cambios en `protocol/`, `runtime/`, `tests/`, `tools/` (§4.2); frontera DEV-only en U1a/U3b |
| D. Increment leakage | PASS | Sin campos de template, anchors, checkpoints, findings, pending ni checkers (§4.2); mapeo de incrementos en §7 |
| E. Operationalization | PASS | Regla transversal escrita (U1c/U2a); tabla target semantics vs enforcement (§7.2) |
| F. Automation | PASS | Sin checkers ni tests nuevos; nada en `tools/` (§4.2, §15) |
| G. Artifacts | PASS | Ningún artifact nuevo fuera de este plan; se extienden 4 docs existentes (reusar/extender, Plan 94 §12) |
| H. State machine | PASS | Sin Change State Machine; condiciones derivadas sobre status existentes (§7, U2a) |
| I. Entity model | PASS | Sin Change/Finding/Decision/Series registry ni entidades (§4.2; RFC-75 No-objetivos) |
| J. Validation | PASS | Nunca PASS con test FAILED; resultado real reportado como desviación documentada — post-cierre `339 passed, 1 failed` (solo timestamp; contención PASS); histórico `338 passed, 2 failed` mientras el plan 94 estuvo sin versionar (§15, §19, §21) |
| K. Git | PASS | Sin hashes inventados; sin metadata/hooks/scripts de checkpoint (§16) |
| L. Versioning | PASS | Docs-only: ítem `[Unreleased]`, sin bump, sin tag, sin promoción (§17) |
| M. Dogfooding | PASS | El propio plan demuestra `Executed ≠ Committed ≠ Closed ≠ Released` con estado real (§13) |
| N. Future increments | PASS | B/C/D y track 5 preservados sin absorber; sin backfill (§2, §4.2, §7) |
| O. Implementability | PASS | Cambios file-by-file con sección exacta y contenido requerido (§9); criterios de entrada/salida verificables (§5, §21) |

Resultado: 15 PASS, 0 WARN bloqueante, 0 BLOCKER. El único gate humano de
cierre restante es OPEN-2 (desviación documentada de pytest); OPEN-1 quedó
resuelto.

## 26. Veredicto final

**PLAN 95 READY FOR IMPLEMENTATION**

- **Nombre:** Plan 95 — Implementación de la Unidad A (Incremento 0): semántica,
  vocabulario y observability baseline del Change Lifecycle DEV
  (`docs/plans/95-change-lifecycle-unit-a-increment-0.md`).
- **Alcance:** Unidad A = Incremento conceptual 0 de RFC-75; docs-only; sin
  machinery nueva; sin cambios de payload.
- **Autoridades:** RFC-75 `Accepted`; ADR-15/16 `Accepted`; RFC-56 `Accepted`;
  Plan 94 `Executed` (Master Action Plan); convenciones del repo.
- **Gates de ejecución/cierre:** la dependencia Git del plan 94 quedó resuelta
  (commit `3acf439`, 2026-09-02; OPEN-1); al cerrar la unidad queda la
  aceptación del mantenedor de la desviación documentada de pytest (OPEN-2,
  política §24.1 del plan 94). Ninguno es blocker de diseño.
- **Deuda no bloqueante:** fallo preexistente de pytest (timestamp);
  `dev` ahead 3; snapshots de INDEX/VERSIONING desactualizados (§19).
- **Próximo paso:** ejecutar la Unidad A (U1–U6) sobre `dev`, validar con la
  batería y cerrar con la política de "batería verde" del plan 94 (§24.1) y la
  aceptación del mantenedor de la desviación documentada (OPEN-2).

## Nota de ejecución

- 2026-09-02 — Ejecutada la Unidad A / Incremento 0 sobre `dev` (HEAD previo
  `3acf439`, plan 94 commiteado). U1–U5 aplicados: `docs/CONVENTIONS.md`
  (subsecciones de alcance DEV-only, modelo de Change Levels y regla
  transversal target semantics vs operationalización), `docs/VERSIONING.md`
  (§7 con las condiciones derivadas + §11 observability schema baseline),
  `AGENTS.md` raíz (`Task lifecycle` alineado + frontera DEV/Protocol en
  `Do NOT`), `docs/AGENTS.md` (`Identity`: serie como identidad derivada) e
  ítem `(plan 95, RFC-75)` en `CHANGELOG.md:[Unreleased]`.
  **Verificación:** checkers en verde (`check_plan_structure`,
  `check_plan_citations`, `check_protocol_invariants`, `check_taxonomy_coherence`,
  `check_session_artifacts`, `check_version_state` con warnings esperados de
  dev); pytest `339 passed, 1 failed` — el único fallo es
  `test_store_rebuild_is_derived_and_deterministic`, deuda temporal
  preexistente e independiente (PREEXISTING_INDEPENDENT_TEST_DEBT), no
  modificada. Sin cambios en `protocol/`, `runtime/`, `tests/`, `tools/`,
  VERSION, ADRs ni RFCs. Status: `Executed` sin `Closed` — el mecanismo formal
  de checkpoint pertenece al Incremento 3 y OPEN-2 (aceptación del mantenedor
  de la desviación documentada de pytest) queda pendiente para el cierre
  formal de la unidad.
- 2026-09-02 — Disposición formal (Governance Disposition Pass, decisión
  explícita del mantenedor): OPEN-2 queda RESUELTO por la vía alternativa
  prevista en §23 — resolución del test como deuda independiente antes del
  cierre (commit `865e3ad`; pytest `340 passed, 0 failed`; checkers PASS); no
  se aceptó desviación vigente alguna. La ejecución original de esta unidad
  (pytest `339 passed, 1 failed`) permanece como registro histórico, sin
  reescribirse. Plan 95 sigue `Executed` + commiteado, sin `Closed` (el
  mecanismo formal de checkpoint del Incremento 3 sigue pendiente).
