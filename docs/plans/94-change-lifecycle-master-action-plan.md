# Plan 94 — Master Action Plan: Change Lifecycle de ARgentOS DEV

> **Naturaleza de este documento.** Este es un **Master Action Plan** (mapa
> maestro), no un Plan de implementación ejecutable: no se ejecuta ningún
> incremento del Change Lifecycle en esta iteración. Su entregable es la
> estrategia incremental derivada de RFC-75 para que planes futuros (95+)
> implementen cada incremento. No modifica `protocol/.agents/`, `runtime/`,
> `tests/` ni `tools/`; no produce bump de `VERSION` ni tag (docs-only,
> RFC-69). Este documento (el MAP) es docs-only; los incrementos que deriva
> (§18) no lo son todos: el Incremento 4 incorpora tooling y tests.

**Status:** Executed
**Fecha:** 2026-09-01
**RFC:** RFC-75 (`docs/rfc/75-change-lifecycle.md`)
**Clase:** — (no toca `protocol/.agents/`; cambio docs-only, `docs/VERSIONING.md:3. Versionado`)
**Depende de:** RFC-75 `Accepted` (`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`); ADR-15/16 `Accepted` (`docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`); RFC-56 `Accepted`; batería canónica en verde.
**Origen:** Solicitud explícita del mantenedor (2026-09-01); registro formal de RFC-75 (commit `352ad18`); ADR-15/16 (commit `c166520`); evidencia RFC-71..74 y planes 86–93.

---

## Convención de evidencia

Este documento distingue, en cada conclusión importante:

| Marca | Significado |
|---|---|
| `OBSERVED` | Evidencia directa del repositorio (git, archivos, checkers). |
| `DERIVED` | Conclusión lógica basada en evidencia citada. |
| `PROPOSED` | Propuesta de diseño/implementación de este plan maestro. |
| `OPEN` | Cuestión aún no decidida; se resuelve en un Plan de implementación posterior o requiere decisión humana. |
| `BLOCKER` | Contradicción que impide continuar (no se detectó ninguna; ver §Veredicto). |

Las afirmaciones sobre el estado actual se anclan con `ruta:sección`
(`docs/CONVENTIONS.md:Convenciones`).

## Contenido requerido → sección

| Requisito del encargo | Sección de este documento |
|---|---|
| Executive Summary | §1 |
| Current State | §2 |
| Problem Statement | §3 |
| Lifecycle Model | §4 |
| DEV vs Protocol Boundary | §5 |
| Existing Workflow Analysis | §6 |
| RFC-75 → Mechanism Mapping | §7 |
| Authority Model | §8 |
| Change Level Economics | §9 |
| State Machine Decision | §10 |
| Skills Strategy | §11 |
| Artifacts Strategy | §12 |
| Policies Strategy | §13 |
| Harness/Checker Strategy | §14 |
| Git/Checkpoint Strategy | §15 |
| Agent Continuity/Handoff Strategy | §16 |
| Telemetry Strategy | §17 |
| Incremental Implementation Roadmap | §18 |
| Dogfooding Strategy | §19 |
| Dependency Graph | §20 |
| Risk Register | §21 |
| ADR Candidates | §22 |
| Existing Debt / Non-blocking Findings | §23 |
| Validation Strategy | §24 |
| Exit Criteria for the Master Plan | §25 |
| Retrospectiva RFC-71..74 | §26 |
| Open Questions | §27 |
| Auditoría adversarial interna | §28 |
| Veredicto final | §29 |

---

## 1. Resumen ejecutivo

RFC-75 (`docs/rfc/75-change-lifecycle.md`) está `Accepted` y con implementación
pendiente. Su registro (commit `352ad18`) no creó ningún plan de
implementación. Este Master Action Plan convierte RFC-75 en una estrategia
incremental ejecutable, con los siguientes resultados principales:

- **[OBSERVED]** El lifecycle real de ARgentOS DEV pierde información en
  fronteras concretas: validaciones sin anchor reproducible, `Executed` sin
  semántica de cierre Git, findings sin lineage, decisiones pendientes solo en
  conversación y series multi-plan/multi-RFC sin identidad estable
  (`docs/rfc/75-change-lifecycle.md:Problema`).
- **[DERIVED]** Todo lo necesario para cerrar esos gaps es **relaciones,
  campos y vistas sobre artifacts existentes**; RFC-75 no requiere entidades
  nuevas, state machine global, tracker universal ni backend
  (`docs/rfc/75-change-lifecycle.md:No-objetivos`).
- **[DERIVED]** RFC-75 define **seis incrementos conceptuales** (0, 1, 2, 3, 4,
  5); su rollout `0 → {1,3} → 2 → 4` se traduce en **cuatro unidades de
  implementación iniciales** (A: Incremento 0; B: Incrementos 1+3 en batch
  operacional, sin renumerar ni absorber el 3; C: Incremento 2; D: Incremento 4)
  más el **track futuro deferido** (Incremento 5: coordinación/handoff, fuera
  de alcance). Los incrementos 0–3 son predominantemente documentales
  (templates y documentación); el Incremento 4 incorpora tooling/checkers y
  sus tests. Cada unidad deja el repo utilizable y habilita dogfooding del
  siguiente.
- **[PROPOSED]** El primer incremento (0: semántica + vocabulario +
  observabilidad baseline) es el punto correcto para comenzar: no depende de
  maquinaria nueva, se valida con la batería existente y crea el lenguaje que
  los planes 95+ usarán para implementar anchors, checkpoints, findings y
  automatización.

El plan maestro termina con veredicto
`READY FOR IMPLEMENTATION PLANNING` (§29): no se detectaron BLOCKERs, no se
registran ADRs nuevos (solo candidatos) y la deuda conocida (un test con
timestamp fijo) no bloquea la planificación, pero sí condiciona el criterio de
"batería verde" de las unidades que lo exijan, según la política de §24.1.

## 2. Estado actual

### 2.1 Estado del repositorio

**[OBSERVED]** Verificado con git y los checkers al 2026-09-01:

| Dato | Valor observado |
|---|---|
| Branch | `dev` |
| HEAD | `352ad18` (`docs(rfc): register change lifecycle RFC`) |
| Working tree | limpio al inicio de esta tarea (este plan agrega el plan 94 + su registro en INDEX) |
| Respecto a `origin/dev` | ahead 2 (commits `c166520` ADR-15/16 y `352ad18` RFC-75 sin push) |
| VERSION del protocolo | `10.3.0` (`protocol/.agents/VERSION`) |
| RFC-75 | `Accepted` (2026-09-01; registro formal; implementación pendiente) (`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`) |
| ADR-15/16 | `Accepted` (2026-08-31) (`docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`) |
| Plan de implementación de RFC-75 | no existía al inicio de esta tarea; este plan 94 es el mapa maestro (no una implementación ejecutable) |
| Batería de checkers | en verde (`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` con warnings esperados de dev) |
| pytest `tests/` | 1 fallo preexistente conocido (§23) + errores de ACL del sandbox con basetemp por defecto; no se reporta como batería verde total (§24.1) |

### 2.2 Mapa de gobernanza DEV existente

**[OBSERVED]** El repo fuente no tiene `.agents/` propio: el `AGENTS.md` raíz,
`docs/CONVENTIONS.md`, `docs/VERSIONING.md` y `docs/AGENTS.md` (taxonomía)
constituyen la gobernanza DEV. El payload del producto vive en `protocol/`
(`protocol/.agents/` + `protocol/_AGENTS.md`) y es **data, no reglas** para el
desarrollo (`docs/source-layout.md`; `docs/CONVENTIONS.md:Convenciones`).
No existen policies, skills, harnesses ni state machines de DEV fuera de esos
documentos; las 33 skills del producto (`protocol/.agents/skills/`) son
capacidades del Protocol, no mecanismos de DEV (§11).

### 2.3 Evidencia operacional de los problemas

**[OBSERVED]** Evidencia concreta, verificada en el repo:

- Planes 86/87/92/93: `Executed` en el working tree **pendientes de commit del
  mantenedor** (`docs/plans/86-context-persistence-cacheability-model.md:Nota de ejecución`,
  `docs/plans/87-provider-prompt-cache-capability.md:Nota de ejecución`,
  `docs/plans/92-rfc73-acceptance.md:Nota de ejecución`,
  `docs/plans/93-rfc74-acceptance.md:Nota de ejecución`).
- Plan 91: `Executed` con **commit atómico pendiente de decisión del
  mantenedor** por archivos de gobernanza entrelazados
  (`docs/plans/91-rfc74-cache-observability-implementation.md:Nota de ejecución`).
- G1 (`fcf6ce1`): fix + checker + tests sin finding lineage; el ADR-15 lo
  documenta como pérdida de provenance (`docs/adr/15-change-lifecycle-continuity.md:Contexto`).
- Plan 90: documenta una decisión de implementación con alternativa rechazada
  persistida (`docs/plans/90-rfc73-project-persistence-implementation.md:Nota de ejecución`),
  patrón que RFC-75 formaliza como pending/decision lineage.
- Tracker de findings de auditoría: patrón existente con resolución y
  evidencia (`docs/working/audits/AUDITORIA_SISTEMA.md:Findings tracker (F1–F7)`),
  que RFC-75 extiende a refs calificadas en artifacts.

## 3. Declaración del problema

**[OBSERVED + DERIVED]** El problema central no es falta de herramientas, sino
pérdida de información en fronteras del lifecycle existente
(`docs/rfc/75-change-lifecycle.md:Problema`):

1. **Validaciones sin anchor reproducible.** La batería y pytest se reportan en
   notas de ejecución sin commit/VERSION de referencia
   (`docs/adr/15-change-lifecycle-continuity.md:Contexto`); el spike de
   reconstrucción midió 0% de validaciones anclables
   (`docs/rfc/75-change-lifecycle.md:Contexto`).
2. **`Executed` sin semántica de cierre Git.** Los planes 87/92/93/91 quedaron
   `Executed` sin commit; el status mezcló implementación + validación con
   cierre, contradiciendo el DoD (`docs/adr/15-change-lifecycle-continuity.md:Contexto`).
3. **Findings/correcciones sin lineage.** G1 es el caso ejemplar
   (`docs/rfc/75-change-lifecycle.md:Contexto`).
4. **Decisiones humanas pendientes solo en conversación.** La decisión del
   mantenedor sobre el commit del plan 91 es el caso vigente
   (`docs/plans/91-rfc74-cache-observability-implementation.md:Nota de ejecución`).
5. **Series multi-plan/multi-RFC sin identidad estable.** La serie
   RFC-71..74 / planes 86–93 existe de facto (`Serie:` en headers), pero no
   como identidad derivada verificable.
6. **El humano funciona como "bus".** La coordinación entre agentes depende
   del copy/paste del mantenedor (`docs/rfc/75-change-lifecycle.md:Problema`).

El objetivo del Master Plan es responder:

> ¿Cómo pasamos del workflow actual de ARgentOS DEV a un Change Lifecycle
> operativo, verificable, progresivamente adoptado y capaz de reducir la
> dependencia del humano como bus, sin crear maquinaria desproporcionada?

## 4. Modelo de lifecycle

### 4.1 Lifecycle conceptual completo

**[DERIVED]** A partir de `docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`,
el lifecycle completo es:

```text
intake → classification → [RFC → ADR?] → acceptance → Plan → execution
→ validation → [finding → correction → revalidation] → Git checkpoint
→ closure → [promotion → release] → [post-close finding → impact assessment
→ new action]
```

### 4.2 Condiciones derivadas (no state machine)

**[DERIVED]** Los únicos status son los existentes de Plan/RFC/ADR; las
condiciones del lifecycle son derivadas (`docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`):

```text
Verified   = ∃ validation(PASS, anchor)
Executed   = Plan.status == "Executed" (impl + validación; CL-4)
Committed  = estado del repositorio (CL-5), no status de Plan
Closed     = Executed ∧ governance-checklist ∧ ∃ checkpoint ∧ consistencia
Promoted   = ∃ merge dev→master verificado
Released   = ∃ tag inmutable
Abandoned  = Plan Superseded con motivo
```

Cadena de implicación: `Verified ⊆ Executed ⊆ Closed ⊆ Promoted ⊆ Released`.
Anomalías: Closed sin Verified = inválido; Promoted sin Closed = anomalía;
Released sin Verified = violación de gobernanza. `Closed ≠ release`; execution
parcial ≠ closure exitoso.

### 4.3 Qué existe, qué falta, qué se formaliza

| Etapa | Estado actual | Formalización requerida (RFC-75) |
|---|---|---|
| Intake / clasificación | Parcial: trackers (backlog/auditoría/roadmap) y headers de Plan/RFC (`Serie`, `RFC`, `Clase`, `Depende de`, `Origen`) | Clasificación con Change Level + regla L0 provisional + fallback al primer artifact (`Mecanismo 1 — Intake`) |
| RFC | Existe (`Proposal → Accepted → Superseded` + Amendment Log) | Auditoría como validación anclada; acceptance con batería + findings + decisión humana (`Mecanismo 3 — RFC lifecycle`) |
| ADR | Existe (ADR-15/16; criterio ADR-worthiness) | Evaluación en aceptación/aprobación/ejecución; elevación retrospectiva (`Mecanismo 4 — ADR integration`) |
| Plan | Existe (status + template + INDEX) | Semántica de `Executed` vs `Closed`; matriz de governance; checkpoint (`Mecanismo 5 — Plan lifecycle`) |
| Validación | Existe (batería) pero sin anchor | Anchor con scoped identity + factores ambientales (`Mecanismo 6 — Validation Anchors`) |
| Git | Existe (dev/master/dist, tags) sin closure | Checkpoint ≠ anchor; consistencia; multi-commit (`Mecanismo 7 — Git Checkpoints`) |
| Findings / correcciones | Parcial (tracker de auditoría) | Refs calificadas `artifact:F-n`, N:M, estados, revalidación (`Mecanismo 8 — Findings / Corrections / Revalidation`) |
| Decisiones pendientes | Informal (conversación / Nota) | Per-artifact con dueño, escalación, resolución (`Mecanismo 9 — Pending Decisions`) |
| Series | Declarada (`Serie:`) sin verificación | Identidad derivada: declaración + relaciones verificables (`Mecanismo 11 — Series / Continuity`) |
| Post-close | Existe de facto (plan nuevo) | Tabla de acciones post-close (`Mecanismo 12 — Post-close Changes`) |
| Observabilidad | Métricas de proceso existentes | Métricas de lifecycle derivadas de campos (`Mecanismo 13 — Observability`) |
| Automatización | Checkers existentes | Safe automation gated en observabilidad (`Mecanismo 14 — Automation`) |
| Migración/legacy | n/a | Nada se migra obligatoriamente; backfill opcional; discriminador de legacy (`Mecanismo 15 — Migration / Legacy`) |

## 5. Frontera DEV vs Protocol

**[DERIVED]** Esta distinción es normativa para todo el plan maestro
(`docs/rfc/75-change-lifecycle.md:Dev vs Protocol`):

- El Change Lifecycle gobierna **ARgentOS DEV**: `AGENTS.md` raíz,
  `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, templates, checkers dev.
- No gobierna automáticamente la evolución del **Protocol**
  (`protocol/.agents/`): un cambio con efecto payload sigue RFC-56 (RFC
  `Accepted` + plan; `docs/rfc/56-governance-fast-track.md:Decisión propuesta`).
- No se crean workflow/policy/state machine/artifact/skill compartidos entre
  DEV y Protocol; no hay herencia automática.
- Principios transferibles (revalidación ante continuidad; persistir ≠
  materializar; separación evidencia factual / autoridad normativa) quedan
  como principios, no mecanismos.

**[OBSERVED]** Ningún mecanismo propuesto en §18 escribe en
`protocol/.agents/`, `protocol/_AGENTS.md`, `protocol/.agents/VERSION`, `dist/`
ni en el runtime del Protocol. Los únicos toques al payload son lecturas
normativas (p. ej., verificar `protocol/.agents/VERSION` contra anchors) o la
verificación de la batería (`tools/check_protocol_invariants.py --payload protocol .`),
que son tooling DEV existente, no modificaciones del payload.

## 6. Análisis del workflow existente

**[OBSERVED]** Inventario por etapa del lifecycle actual, contrastado con el
repo. Ninguna capacidad se afirma si no existe.

| Etapa | Evidencia | Autoridad | Automatización | Dependencia humana | Continuidad | Reproducibilidad | Problemas | Invariante RFC-75 |
|---|---|---|---|---|---|---|---|---|
| Intake / clasificación | Trackers (`docs/working/audits/`, `ROADMAP.md`), headers de Plan/RFC | Mantenedor (decisión); agente (propuesta) | Nula (no hay campos de Change Level) | Clasificación informal | Por conversación/Nota | Baja (sin registro canónico de clasificación) | Level no declarado; L0 provisional no definido | CL-10; `Mecanismo 1` |
| RFC | `docs/rfc/75-change-lifecycle.md`, Amendment Log, INDEX | Humano (acceptance; AU-3) | Citas + estructura (checkers) | Aceptación, ADR-worthiness | Amendment Log + git | Alta (docs versionados) | Rondas de auditoría sin anchor | CL-1/CL-2; `Mecanismo 3` |
| ADR | `docs/adr/15-change-lifecycle-continuity.md`, matriz INDEX | Humano (decisión registrada) | Citas + estructura | Criterio ADR-worthiness | INDEX + git | Alta | Extracción retrospectiva sin criterio operativo (resuelto por ADR-16) | AU-6; `Mecanismo 4` |
| Plan | `docs/plans/90-rfc73-project-persistence-implementation.md`, template, INDEX | Humano (aprobación) | Citas + estructura | Aprobación | Plan + Nota de ejecución | Alta (docs) / media (estado real) | `Executed` sin commit; Nota sin anchor/checkpoint | CL-3/4/5; `Mecanismo 5` |
| Ejecución | Working tree sobre `dev`; commits por plan | Agente (bajo Plan aprobado) | Batería | Juicio de alcance/calidad | Nota de ejecución | Media | Ejecuciones en working tree sin commit (planes 86/87/92/93) | CL-4 |
| Validación | `docs/VERSIONING.md:4.1 Batería canónica de verificación` | Factual (checkers) + humano (H13/juicio) | Checkers | Juicio semántico | Reporte en Nota | Baja (sin anchor) | Anchor ausente; entorno no declarado | CL-1/2; VC-1 |
| Findings / correcciones | Tracker de auditoría (`AUDITORIA_SISTEMA.md`) | Humano (severidad, resolución) | Citas | Clasificación/resolución | Tracker + refs | Media | Sin refs `artifact:F-n` en lifecycle; N:M ausente | CL-6/7/8; LC-1 |
| Commit | Git (`dev`), Conventional Commits | Mantenedor / agente autorizado | Git | Decisión de commit | Git | Alta | `Executed` sin commit; planes 87/92/93/91 pendientes | CL-5 |
| Promoción / release | `docs/VERSIONING.md:1. Ramas y roles`, tags, `publish-dist` | Humano (autorización) + CI | Merge/tag/publish | Autorización MAJOR/MINOR | Tags inmutables | Alta | Release batch sin checkpoint por plan | CL-3; `Mecanismo 12` |
| Cierre | INDEX + changelog + estados | Mantenedor | Checkers de estructura/versión | Decisión de cierre | INDEX (descriptivo) | Media | `Closed` no definido; consistencia checkpoint↔anchor ausente | GC-1 |
| Feedback / learning | Lessons del protocolo; changelog | Agente + mantenedor | n/a | Priorización | KB/lessons | Media | Aprendizajes no ligados a findings post-close | `Mecanismo 12` |

## 7. Mapeo RFC-75 → mecanismos

**[DERIVED]** Matriz que conecta cada mecanismo/invariante de RFC-75 con el
mecanismo futuro. No todo requiere artifact, skill, policy o checker: el
principio rector es `persist → observe → automate`
(`docs/rfc/75-change-lifecycle.md:Principios arquitectónicos`).

| Concepto / invariante RFC-75 | Mecanismo requerido | Artifact candidato | Skill candidata | Policy candidata | Checker/tool candidato | Incremento |
|---|---|---|---|---|---|---|
| CL-1/VC-1 — anchor | Campos de anchor en validación registrada | Template de Plan (sección Verificación), Nota de ejecución, Amendment Log de RFC | Ninguna | `docs/CONVENTIONS.md`, `docs/VERSIONING.md` | Checker de presencia de anchor (incremento 4) | 1 |
| CL-2 — validez relativa | Regla de aplicabilidad/revalidación | `docs/VERSIONING.md:10. Definition of Done` | Ninguna | `docs/CONVENTIONS.md` | Checker de stale (incremento 4) | 1 |
| CL-3/GC-1 — checkpoint | Campos de checkpoint + consistencia | Template de Plan (cierre), Nota de ejecución | Ninguna | `docs/VERSIONING.md:10. Definition of Done` | Checker de consistencia checkpoint↔anchor (incremento 4) | 3 |
| CL-4/CL-5 — Executed/Committed | Semántica escrita en fuentes de verdad | `docs/VERSIONING.md:7. Estados de planes y RFCs` | Ninguna | `docs/CONVENTIONS.md:Convenciones` | `check_version_state` existente (extendible) | 0 |
| CL-6/7/8/LC-1 — findings | Refs calificadas `artifact:F-n` + estados + N:M | Nota de ejecución / secciones de corrección en Plan y RFC | Ninguna | `docs/CONVENTIONS.md` | Checker de formato de refs (incremento 4) | 2 |
| PC-1 — pending decisions | Campos per-artifact (blocking, owner, resolución) | Nota de ejecución / sección Pending en Plan | Ninguna | `docs/CONVENTIONS.md` | Checker de ownership/presencia (incremento 4) | 2 |
| CL-9 / AU-6 — decision lineage | Regla de elevación y registro | ADR (elevación condicional) | Ninguna | `docs/CONVENTIONS.md` (ADR-worthiness ya en ADR-16) | Ninguno (juicio arquitectónico) | 0 |
| CL-10 — escala por impacto | Change Levels + matriz de maquinaria | Template de Plan (campo Change Level) | Ninguna | `docs/CONVENTIONS.md` | Checker opcional de coherencia Level↔machinery (incremento 4) | 0 |
| AU-1/2/3/5/7 — autoridad | Clases + protocolo de conflicto (ya normado) | `docs/adr/16-change-lifecycle-authority.md` | Ninguna | Referencia desde CONVENTIONS | Ninguno (checker = evidencia factual, nunca autoridad) | 0 |
| AU-4 — INDEX descriptivo | Regla: INDEX = vista, nunca autoridad | INDEX existentes | Ninguna | `docs/AGENTS.md:INDEX y CONVENTIONS` | Checkers de mirror existentes (estructura) | 0 |
| Serie — identidad derivada | Declaración `Serie:` + verificación de relaciones | Headers de RFC/Plan + INDEX | Ninguna | `docs/CONVENTIONS.md` | Checker de membresía de serie (incremento 4) | 1 |
| Post-close | Tabla de acciones | `docs/rfc/75-change-lifecycle.md:Mecanismo 12 — Post-close Changes` + CONVENTIONS | Ninguna | `docs/CONVENTIONS.md` | Ninguno | 2 |
| Observabilidad | Métricas derivadas de campos | `docs/VERSIONING.md` (sección de métricas) o docs de gobernanza | Ninguna | SHOULD (no gate) | Script de consulta (incremento 4) | 0 |
| Safe automation | Checkers opcionales gated en observabilidad | `tools/` (nuevos scripts dev) | Ninguna | Checker = evidencia factual | Nuevos checkers (incremento 4) | 4 |
| Handoff/coordinación | Fuera de alcance (RFC-75); solo persistir hechos | Campos de anchor/pending/checkpoint (incrementos 1–3) | Ninguna (prohibidas skills obligatorias) | Documentar frontera | Ninguno | 5 (deferido) |

### 7.1 Criterios por mecanismo

Para cada mecanismo del §7 se aplican las siguientes preguntas (respuesta
resumida por familia):

| Pregunta | Respuesta |
|---|---|
| ¿Por qué existe? | Resuelve una pérdida observada (§3): anchor, closure, lineage, pending, serie. |
| ¿Qué problema resuelve? | Reconstruibilidad sin conversación; validación reproducible; cierre verificable. |
| ¿Qué evidencia produce? | Campos registrados (anchor, checkpoint, refs) que un sucesor puede auditar. |
| ¿Quién lo consume? | Agentes sucesores, mantenedor, checkers (incremento 4), métricas. |
| ¿Qué nivel de cambio lo necesita? | Regla objetivo: toda validación registrada → anchor (VC-1) sin importar el Level; checkpoint → todo Plan cerrado (GC-1); refs/pending → cuando existen findings/decisiones; el resto escala con L0–L3 (§9). Operacionalmente exigible solo desde el incremento que materializa el mecanismo (Regla transversal, §18). |
| ¿Puede derivarse de información existente? | Sí, en su mayoría: los hechos ya ocurren; falta persistirlos en los artifacts correctos. |
| ¿Puede automatizarse? | La verificación mecánica de presencia/consistencia/refs sí (incremento 4); la aplicabilidad y severidad no (juicio). |
| ¿Requiere decisión humana? | Aceptación, ADR-worthiness, severidad, escalación, release, materialidad ambiental (AU-3). |

## 8. Modelo de autoridad

**[DERIVED]** Se aplica ADR-16 sin modificación
(`docs/adr/16-change-lifecycle-authority.md:Decisión`). Las transiciones del
lifecycle se clasifican así:

| Transición / decisión | Clase | ¿Automatizable? | ¿Checker puede bloquear? | ¿Requiere humano? | Artifact |
|---|---|---|---|---|---|
| Estado factual (tests, checkers, git, tags) | FACTUAL | Sí | Sí (evidencia) | No | Git, checkers, tests |
| Clasificación / Change Level | DECISION (inicial) / FACTUAL (revisión) | Parcial (umbrales coarse) | No (solo recomendar) | Sí (upgrade obligatorio, downgrade con justificación) | Primer artifact del cambio |
| Aceptación de RFC | NORMATIVE + DECISION | No | Sí (batería, citas, findings bloqueantes) | Sí | RFC + Amendment Log |
| ADR-worthiness | DECISION (juicio arquitectónico) | No (solo evidencia estructural) | No | Sí | ADR (si eleva) |
| Aprobación de Plan | NORMATIVE + DECISION | No | Sí (estructura, citas, gates) | Sí | Plan + INDEX |
| Ejecución | NORMATIVE (Plan aprobado) | Parcial | No (batería al cierre) | Juicio de alcance | Working tree + commits |
| Validación PASS | FACTUAL | Sí (checkers) / juicio (semántica) | Sí | Juicio de aplicabilidad | Nota de ejecución + anchor |
| Cierre (`Closed`) | DERIVED (FACTUAL + NORMATIVE) | Parcial | Sí (consistencia checkpoint↔anchor) | Decisión final | Plan + INDEX + git |
| Promoción / release | RELEASE | Parcial (merge/tag) | Sí (invariante versión↔changelog↔tag) | Sí (autorización MAJOR/MINOR) | master + tag + dist |
| Conflicto normativo | DECISION (AU-3) | No | Detecta y escala | Sí (resuelve) | Artifact correspondiente |
| Serie (membresía) | DESCRIPTIVE + FACTUAL | Sí (declaración + relaciones) | No (coincidencia textual aislada no basta) | Corrección de declaraciones | Headers + INDEX |
| Pending (owner, resolución) | DECISION | No (presencia sí) | Puede señalar ausencia | Sí (escalación) | Artifact que bloquea |

Regla transversal: `checker output = factual evidence ≠ normative authority`
(`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`); "anchor missing"
es GAP, no "validation invalid".

## 9. Economía de Change Levels

**[DERIVED]** RFC-75 decide los ejes, los umbrales coarse y `Level = max(...)`;
la calibración fina queda para Plan; nada de esto es configurable vía
feature-flags del repo hoy (no existe tal mecanismo).

### 9.1 Umbrales coarse (decisión de RFC-75, no se rediseña)

[OBSERVADO en `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`]

| Dimensión | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| coordination | 1 agente, 1 sesión | 1 agente, multi-sesión | multi-agente o planes paralelos | cross-RFC / serie orquestada |
| scope (superficie) | 1 archivo | área acotada (una capa) | multi-área (≥2 capas) | multi-área + contratos |
| architectural impact | sin cambio estructural | local, aditivo/reversible | entre límites (nuevo módulo/seam) | semántica de modelo/contratos/invariantes, irreversible |
| release impact | sin versión | changelog-only | MINOR | MAJOR / batch |
| duration/complexity | <1 sesión | 1 sesión | multi-sesión | multi-semana |

El número de commits **no** es dimensión. Change Level ≠ RFC-56 class (ejes
independientes: una Clase A pequeña puede ser L2; una Clase C grande puede ser
L2/L3 por scope; runtime-only tiene Level sin clase).

### 9.2 Matriz operacional L0–L3

| Level | Coordination | Scope | Architectural impact | Release impact | Duration/complexity | Machinery requerida |
|---|---|---|---|---|---|---|
| **L0** | 1 agente, 1 sesión | 1 archivo | sin cambio estructural | sin versión | <1 sesión | **Mínima:** clasificación en el primer artifact; sin Plan obligatorio (Clase C puede commit directo); toda validación registrada lleva anchor (VC-1) como regla objetivo, operacionalmente exigible desde el Incremento 1 (Regla transversal, §18). |
| **L1** | 1 agente, multi-sesión | área acotada (una capa) | local, aditivo/reversible | changelog-only o docs-only | 1 sesión | Plan/Nota (según clase RFC-56) + validación anclada + checkpoint al cerrar; sin findings/pending si no existen. |
| **L2** | multi-agente o planes paralelos | multi-área (≥2 capas) | entre límites | MINOR | multi-sesión | Plan completo + matriz de governance aplicable + findings/pending si surgen + revalidación; serie si es multi-RFC/plan. |
| **L3** | cross-RFC / serie orquestada | multi-área + contratos | semántica de modelo/contratos/invariantes | MAJOR / batch | multi-semana | Machinery completa del §7 (anchors, checkpoint, findings, pending, serie, post-close, métricas); RFC/ADR según corresponda. |

### 9.3 Reparto de decisiones

| Categoría | Contenido |
|---|---|
| Ya decidido por RFC-75 | Ejes, umbrales coarse, `Level = max`, L0 provisional, independencia de RFC-56. |
| A decidir en Plan de implementación | Formato de campos; wording en CONVENTIONS/VERSIONING; calibración fina de umbrales; checkers opcionales; activación del tracker condicional. |
| Configurable | Nada hoy (no hay config); si algún umbral se vuelve configurable, será decisión de Plan con evidencia (RFC-75 no lo pide). |
| Requiere nueva decisión arquitectónica | Elevación de Change Levels a ADR (candidato, §22); tracker condicional (con datos de observabilidad); handoff (fuera de alcance; track futuro deferido, Incremento 5). |

## 10. Decisión de state machine

**[DERIVED — DECISIÓN]** **No se introduce ninguna state machine nueva.**
RFC-75 rechaza explícitamente la "Change State Machine global"
(`docs/rfc/75-change-lifecycle.md:No-objetivos`) y ADR-15 rechazó el
tri-estado `Executed/Committed/Closed` como máquina por derivabilidad y
fricción en cambios pequeños (`docs/adr/15-change-lifecycle-continuity.md:Alternativas consideradas`).

Análisis requerido por el encargo:

1. **¿Existe una state machine necesaria?** No: las transiciones del lifecycle
   son derivables de status existentes + gates + Git; no se observaron
   transiciones ilegales que exijan máquina.
2. **¿Una sola o varias?** Ninguna. Si maquinaria de estados fuese necesaria en
   el futuro, debe aparecer como hipótesis con evidencia (RFC/ADR), no por
   defecto.
3. **¿Qué dimensiones son realmente estados?** Plan.status, RFC.status,
   ADR.status (existentes); `state.json` del harness (producto, no DEV).
4. **¿Qué son artifacts o eventos y no estados?** Anchor (metadata),
   checkpoint (relación closure↔Git), finding (relación de lineage), validación
   PASS (evento/evidencia), serie (identidad derivada), INDEX (vista).
5. **¿Qué transiciones son mecánicamente verificables?** Presencia de anchor,
   consistencia checkpoint↔anchor, formato de refs, versión↔changelog↔tag,
   citas, estructura, mirror de INDEX.
6. **¿Qué transiciones requieren autoridad humana?** Aceptación, ADR-worthiness,
   severidad, escalación, release, materialidad ambiental (AU-3).
7. **¿Qué estados son terminales?** `Closed` es terminal para un Plan
   (`docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle`); los
   problemas posteriores generan artifacts nuevos que referencian al cerrado.
8. **¿Qué estados permiten volver atrás?** Los status de Plan/RFC/ADR no
   retroceden sin justificación documentada (`docs/CONVENTIONS.md:Convenciones`);
   findings pueden reabrirse con ref al original; la
   revalidación es el mecanismo de recuperación factual.
9. **¿Cómo representar bloqueos/rechazo/revisión/revalidación?** Como
   condiciones derivadas + campos (pending blocking/no-blocking; anchor
   stale; finding `deferred`/`superseded`; revalidación con refs), no como
   transiciones de una máquina.
10. **¿Cómo evitar burocracia L0/L1?** La maquinaria se activa por Level y por
    trigger (L0 provisional: cualquier trigger de upgrade recomputa el Level);
    los cambios triviales no pagan el ciclo completo (§9.2).

## 11. Estrategia de Skills

**[OBSERVED]** El workspace DEV **no tiene skills propias** (no existe
`.agents/` en la raíz; la gobernanza DEV son documentos). Las 33 skills de
`protocol/.agents/skills/` (p. ej. `planner`, `reference-resolver`,
`consistency-checker`, `execution-plan-reviewer`) son **capacidades del
Producto**, materializadas en proyectos adoptantes; el `AGENTS.md` raíz las
excluye como reglas del workspace de desarrollo.

Clasificación requerida por el encargo:

| Clase | Resultado |
|---|---|
| Existentes y reutilizables | Ninguna como mecanismo DEV: las skills del producto no se reutilizan para gobernar el desarrollo. |
| Existentes pero necesitan evolución | Ninguna (evolucionar skills del producto sería cambiar el Protocol, fuera de alcance). |
| Nuevas skills necesarias | **Ninguna.** RFC-75 prohíbe skills obligatorias (`No-objetivos`) y la guía de lifecycle se materializa en documentos/policies (CONVENTIONS/VERSIONING/AGENTS.md), no en skills. |
| Mecanismos que NO deberían ser skills | Anchor computation, checkpoint consistency, refs validation, serie derivation, stale detection: son deterministas → scripts/checkers (`tools/`). |

Si en el futuro se quisiera una skill de "guía de lifecycle" (LLM-driven,
asistencia en clasificación), debe tratarse como hipótesis con evidencia y por
el ciclo DEV correspondiente; no es requisito de ningún incremento.

## 12. Estrategia de Artifacts

**[DERIVED]** Principios: `persistir ≠ materializar`; una vista derivada nunca
es autoridad; INDEX es DESCRIPTIVE, nunca AUTHORITY
(`docs/AGENTS.md:INDEX y CONVENTIONS`); no se convierte INDEX en
almacenamiento autoritativo.

### 12.1 Clasificación de artifacts

| Clase | Artifacts |
|---|---|
| Reutilizar sin cambios | `docs/rfc/75-change-lifecycle.md`, `docs/adr/16-change-lifecycle-authority.md`, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md`, `CHANGELOG.md`, checkers existentes, `docs/working/audits/` (provenance). |
| Extender | `docs/plans/_TEMPLATE.md` (campos Change Level / anchor / checkpoint / pending / refs), `docs/CONVENTIONS.md` (semántica Executed/Closed, intake fallback, serie, findings, pending), `docs/VERSIONING.md` (closure + checkpoint en DoD, métricas de lifecycle), `AGENTS.md` raíz (task lifecycle), `docs/AGENTS.md` (taxonomía si hace falta), Nota de ejecución (anchor + checkpoint), Amendment Log de RFC (anchor por ronda de auditoría). |
| Reemplazar | Ninguno. |
| Crear nuevo | Ninguno por ahora: los mecanismos son **campos/relaciones/vistas** sobre artifacts existentes. Un script de vista derivada (opcional, `tools/`) solo si la observabilidad lo justifica (incremento 4). |
| No crear (derivable) | Entidad `Change`, `Finding`, `Decision`, `Series` registry, tracker universal, base de datos del lifecycle, orchestrator paralelo. |

### 12.2 Especificación de artifacts nuevos/modificados

| Campo | Respuesta |
|---|---|
| Propósito | Persistir el hecho en el artifact que lo posee (anchor, checkpoint, ref, pending) para reconstruibilidad. |
| Autoridad | NORMATIVE (Convenciones/VERSIONING/AGENTS.md) + FACTUAL (campos verificables); INDEX nunca autoridad. |
| Producer | Agente que ejecuta el Plan / registra la validación / registra el cierre; mantenedor para decisiones. |
| Consumer | Agentes sucesores, mantenedor, checkers (incremento 4), métricas. |
| Lifecycle stage | Validación (anchor), cierre (checkpoint), ejecución (refs/pending), post-close (nueva acción). |
| Persistencia | Git (docs versionados); nada efímero (`.project/` sigue fuera). |
| Relación con Git | Anchor = estado scoped reproducido; checkpoint = commit/SHA de cierre; commit ≠ identidad semántica (locator). |
| Relación con validation anchor | El campo anchor (scoped identity + factores) es el vínculo directo. |
| Relación con findings | Refs calificadas `artifact:F-n` en el artifact que posee el registro. |
| Relación con decisions | Pending per-artifact con dueño/escalación/resolución; elevación ADR si aplica. |

## 13. Estrategia de Policies

**[DERIVED]** No toda regla se convierte en policy ni toda policy en checker.
Separación:

| Tipo | Ubicación | Reglas que aloja |
|---|---|---|
| Policy normativa | `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `AGENTS.md` raíz, `docs/AGENTS.md` | Semántica de Executed/Committed/Closed; anchor obligatorio para validaciones registradas (VC-1); checkpoint para Plan cerrado (GC-1); refs de findings (LC-1); pending nunca desaparece (PC-1); serie como identidad derivada; frontera DEV/Protocol; clasificación e intake fallback; Change Level como eje independiente. |
| Policy operacional | Templates + Nota de ejecución | Dónde y cómo se registran anchor, checkpoint, refs, pending (formato a decidir en Plan de implementación). |
| Checker | `tools/*.py` + `tests/` | Presencia/consistencia mecánica; evidencia factual, nunca autoridad normativa. |
| Documentación | `docs/AGENTS.md` (taxonomía), secciones de soporte | Naturaleza documental del MAP y futuras vistas; reglas de cita. |

Regla: una policy tiene responsabilidad clara y forma de enforcement o
evaluación; no se crea una policy por regla. Las reglas de L0/L1 se mantienen
en prosa normativa, no en checkers obligatorios.

## 14. Estrategia de Harnesses/Checkers

**[OBSERVED]** Checkers dev existentes: `check_protocol_invariants.py`,
`check_plan_citations.py`, `check_plan_structure.py`,
`check_taxonomy_coherence.py`, `check_session_artifacts.py`,
`check_version_state.py`, `check_dist_sync.py` (local-only), además de
`aggregate_metrics.py`, `audit_gates.py`, `measure_context_budget.py` y
`check_architecture_traceability.py` (tooling complementario). CI:
`.github/workflows/check-protocol.yml` corre checkers + `pytest tests/` +
tests del harness del producto.

Gaps y respuesta a "¿puede determinarse mecánicamente?":

| Gap (futuro campo) | ¿Mecánico? | Candidato | Incremento |
|---|---|---|---|
| Presencia de anchor en validaciones registradas | Sí (estructura) | Checker opcional de presence | 4 |
| Consistencia checkpoint↔anchor (scoped identity + factores) | Sí (si el identity se computa o declara) | Checker de consistencia | 4 |
| Formato de refs `artifact:F-n` / N:M / estados | Sí (sintaxis) | Checker de refs | 4 |
| Pending con owner presente / no desaparece | Parcial (presencia sí; resolución es juicio) | Checker de presence + escalación humana | 4 |
| Serie: membresía requiere declaración + relaciones | Parcial (relaciones verificables; coincidencia textual aislada no basta) | Checker de relaciones | 4 |
| Stale validation (anchor vs estado actual) | Sí (si el scoped identity es computable) | Checker de stale | 4 |
| Severidad / aplicabilidad / materialidad ambiental | No | Juicio del agente + humano | — |
| ADR-worthiness | No (solo evidencia estructural) | Juicio arquitectónico | — |

Todo checker futuro es **opcional** y gated en observabilidad (incremento 4):
antes de automatizar, la dogfooding de los incrementos 0–3 (unidades A–C) debe
producir datos de lifecycle reales (anchors, checkpoints, findings, pending)
que muestren qué checks evitan errores; sin esos datos no se automatiza.
Un checker nunca bloquea por autoridad normativa; produce evidencia
re-ejecutable (`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`).

## 15. Estrategia de Git y checkpoints

**[DERIVED]** De `docs/rfc/75-change-lifecycle.md:Mecanismo 7 — Git Checkpoints`
y `docs/adr/15-change-lifecycle-continuity.md:Decisión`:

| Concepto | Regla |
|---|---|
| Validation anchor | Representa el estado relevante de una validación: declared scope, command-set, effective inputs, observed dependencies, environmental factors, Scoped Content Identity. No es whole-tree por defecto. |
| Checkpoint | Relación closure↔estado Git verificable; **checkpoint ≠ anchor** (el commit de cierre puede incluir governance: INDEX, CHANGELOG, ADR, docs). |
| Consistencia para `Closed` | La identidad scoped del estado de cierre == la del anchor ∧ factores ambientales declarados sin cambio; si difiere → revalidación antes de Closed. |
| Commit SHA | Locator, no identidad semántica. Rebase/cherry-pick/amend con contenido scoped idéntico → sin invalidación automática; contenido distinto → stale → revalidar. |
| Multi-commit / multi-RFC | Un Plan puede requerir varios commits y afectar varias RFCs; `Closed` no depende del conteo. |
| Docs-only | Se cierra sin release; checkpoint igual (GC-1). |
| Promoción / release | Merge dev→master verificado + tag anotado inmutable (`docs/VERSIONING.md:1. Ramas y roles`); rollback = versión nueva, nunca reescribir tags. |
| Stale / revalidación | Cambio de anchor ≠ cambio de validez semántica; evaluar aplicabilidad; revalidar o marcar stale (CL-2). |

Implementación propuesta por incremento: campos en Nota de ejecución/template
(1 y 3), semántica en VERSIONING DoD (0 y 3), consistencia mecánica opcional
(4). No se fabrican anchors históricos para planes pasados
(`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).

## 16. Continuidad entre agentes / handoff

**[DERIVED]** RFC-75 deja el mecanismo de handoff **fuera de alcance**
(`docs/rfc/75-change-lifecycle.md:No-objetivos`) y trata la continuidad como
propiedad del lifecycle: "handoff es mecanismo transversal que la consume"
(`docs/rfc/75-change-lifecycle.md:Principios arquitectónicos`). Este plan
maestro define qué hechos deben persistir para que un mecanismo futuro pueda
eliminar el copy/paste del mantenedor, sin diseñar ese mecanismo.

### 16.1 Qué debe persistir

- **Decisiones:** en el artifact que posee la decisión (pending per-artifact:
  blocking/no-blocking, owner, escalación, resolución, evidencia, ADR-worthiness).
- **Findings:** como refs de lineage `<artifact>:F-<n>` con estados; nunca
  borrados silenciosamente (LC-1).
- **Validación / checkpoint:** anchor (scoped identity + factores) y
  checkpoint con consistencia.
- **Clasificación:** Change Level + origen/tipo en el primer artifact.
- **Serie:** declaración `Serie:` + relaciones verificables.

### 16.2 Qué representa continuidad y cómo se descubre

| Pregunta | Respuesta |
|---|---|
| ¿Qué artifact/context representa continuidad? | El conjunto de artifacts del cambio (RFC/Plan/ADR + INDEX) con sus refs y campos; no un artifact handoff nuevo. |
| ¿Qué debe poder descubrir el siguiente agente? | Los artifacts que poseen el cambio (vía INDEX descriptivo), las refs de findings/pending y el estado derivado (Verified/Executed/Closed). |
| ¿Qué debe ser derivable? | Serie, condiciones derivadas, métricas, listas de pendientes. |
| ¿Qué debe ser explícitamente handoff? | Transferencia de ownership de un pending; escalación; reasignación de un Plan (campo owner). |
| ¿Cómo evitar recibir todo el contexto? | Refs scoped + vistas derivadas; el agente carga solo los artifacts y campos relevantes. |
| ¿Qué parte podría ser Skill? | Guía LLM-driven de clasificación (opcional, futura); nada obligatorio. |
| ¿Qué parte requiere tooling? | Chequeo mecánico de presencia/consistencia (incremento 4); vistas derivadas (opcional). |
| ¿Qué pertenece al lifecycle vs runtime/orchestrator? | El lifecycle persiste los hechos; el runtime/orchestrator (host) consume esos hechos para entregar contexto a otro agente — fuera de alcance (Incremento 5, Deferred / Future Track). |

**Criterio anti-prematuro:** "eliminar copy/paste entre agentes" es un
problema/objetivo que el lifecycle aborda progresivamente (persistir los
hechos primero); no es un requisito de implementación de los incrementos 0–4.

## 17. Estrategia de telemetría

**[OBSERVED]** Existe telemetría de proceso del Protocol
(`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`; eventos en
`METRICS.md` 1.2.0 con `reuse_event`/`provider_cache_event`) y agregador dev
(`tools/aggregate_metrics.py`). No existe telemetría del lifecycle DEV
(anchors, checkpoints, findings, pending).

| Pregunta | Respuesta |
|---|---|
| ¿Qué métricas ya existen? | De proceso: transiciones, delegaciones, fallos, budget, flags, reuse/cache (catálogo). |
| ¿Qué falta medir? | Las 4 métricas permanentes de RFC-75 (SHOULD, derivadas de campos): validation anchor coverage; finding lineage coverage; stale validation rate; Git closure anomalies (`Mecanismo 13 — Observability`). |
| ¿Necesarias para evaluar el lifecycle? | Sí, las 4 anteriores, calculadas de campos existentes sin backend ni writer obligatorio. |
| ¿Necesarias antes de automatizar? | Sí: el Incremento 4 (unidad D) está **gated** en observabilidad/dogfooding: usa los datos de lifecycle producidos por los incrementos 1/3/2 (unidades B/C), no mediciones del Incremento 0, ni thresholds arbitrarios. |
| ¿Cuáles son solo observabilidad? | Todas inicialmente; ninguna métrica es gate de release. |
| ¿Cuáles deberían ser gates? | Solo la consistencia de stale en el cierre (GC-1: revalidar antes de Closed). Las métricas informan, no bloquean. |
| ¿Dependencias? | Las métricas de coordinación (cross-agent, handoffs, pending count, revalidación) son EXPERIMENTAL/DEFERRED: dependen del track de coordinación (Incremento 5, Deferred / Future Track), no se inventan datos antes. |

**Baseline de observabilidad (Incremento 0 / unidad A).** El Incremento 0
establece las **definiciones de métrica / observability schema baseline** de
las cuatro métricas permanentes, pero **no puede producir todavía mediciones
operacionales** de ellas: validation anchor coverage y stale validation rate
dependen de los campos de anchor (Incremento 1) y revalidación (Incremento 2);
Git closure anomalies depende del checkpoint (Incremento 3); finding lineage
coverage depende de las refs de findings (Incremento 2). La observabilidad
operacional se habilita progresivamente cuando existan los datos; el schema
baseline no finge medir. Esto hace que el gate del Incremento 4 no sea
circular: automatiza solo checks útiles y medibles sobre datos de lifecycle
reales (§18, unidad D).

Regla: legacy excluido del denominador; 0 registros = not applicable /
insufficient sample, no "0% compliance" (`docs/rfc/75-change-lifecycle.md:Mecanismo 13 — Observability`).

## 18. Planificación incremental

**[DERIVED]** RFC-75 define **seis incrementos conceptuales** (0, 1, 2, 3, 4, 5)
y el rollout `0 → {1,3} → 2 → 4`
(`docs/rfc/75-change-lifecycle.md:Rollout incremental`). Para reducir
dependencias y evitar estados intermedios sin sentido, este plan maestro los
agrupa en **unidades de implementación iniciales**:

| Unidad de implementación | Incremento(s) conceptual(es) | Despliegue |
|---|---|---|
| A | 0 | individual |
| B | 1 + 3 | batch operacional: el Incremento 3 **no se renumera ni se absorbe** dentro del 1; sigue siendo un incremento independiente de RFC-75 cuyo despliegue se agrupa con el 1 |
| C | 2 | individual |
| D | 4 | individual |
| — | 5 | Deferred / Future Track (fuera de alcance; arquitectura no decidida) |

Los planes de implementación (95+) se redactan por unidad al ejecutarse; este
documento define las unidades como derivación, sin renumerar RFC-75.

### Regla transversal — Target semantics vs operationalization

> **Target semantics vs operationalization.** A rule defined by RFC-75 may be
> part of the target normative model before its enforcement mechanism exists.
> A lifecycle rule becomes operationally enforceable only after the increment
> that materializes its required mechanism is accepted. Earlier increments
> must not retroactively invalidate legacy artifacts or impose unenforced
> requirements.

```text
RFC-75 target model → increment implemented → mechanism materialized
→ rule becomes operationally enforceable
```

Aplicación directa: las reglas objetivo (p. ej., VC-1: toda validación
registrada lleva anchor) pertenecen al modelo normativo desde RFC-75, pero
**no son operacionalmente exigibles hasta que el incremento que materializa su
mecanismo es aceptado** (VC-1 → Incremento 1; GC-1 → Incremento 3; LC-1/PC-1 →
Incremento 2). Ningún incremento anterior invalida legacy ni impone requisitos
sin mecanismo. Esta regla no modifica VC-1 ni RFC-75.

### Implementation Unit A — Incremento 0 (conceptual): Semántica, vocabulario y observabilidad baseline

| Campo | Contenido |
|---|---|
| Increment | 0 |
| Objective | Escribir en las fuentes de verdad DEV la semántica del lifecycle: vocabulario (Executed/Committed/Closed/Verified/Promoted/Released/Abandoned), Change Levels (ejes + max + L0 provisional), condiciones derivadas, frontera DEV/Protocol, series como identidad derivada, y las **definiciones de métrica / observability schema baseline** (schema, no mediciones operacionales todavía). Sin machinery nueva. |
| Problem solved | Status mezclados; `Executed` sin semántica de cierre; vocabulario ausente; nivel no declarado. |
| Scope | `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `AGENTS.md` raíz, `docs/AGENTS.md` (si aplica), definición de métricas de lifecycle en docs de gobernanza. |
| Out of scope | Campos nuevos en templates; checkers; findings; pending; anchors; checkpoint. |
| Mechanisms | Texto normativo (policies §13) + sección de métricas (SHOULD, derivadas de campos). |
| Dependencies | RFC-75 `Accepted`; ADR-15/16 `Accepted`; batería canónica según §24.1. |
| Migration | Ninguna (no hay campos nuevos que migrar). |
| Validation | Batería canónica + H13 por juicio; citas resolubles. |
| Dogfooding | El vocabulario se usa inmediatamente al redactar los planes 95+; el propio plan 94 es el primer caso: `Executed` sin commit ≠ `Closed` (ver `Nota de ejecución`). |
| Exit criteria | Semántica y vocabulario escritos en las 3–4 fuentes; definiciones de métrica/schema baseline sin backend y sin fingir medición operacional de las cuatro métricas (dependen de campos de los incrementos 1/3/2); batería canónica según §24.1. |
| Rollback | Revertir el/los commit(s) del incremento; los docs vuelven al estado anterior. |
| Enables | Unidad B (Incrementos 1 y 3: necesitan el lenguaje); C (Incremento 2: necesita semántica de cierre); D (Incremento 4: necesita el schema baseline, no mediciones del 0). |

### Implementation Unit B — Incremento 1 (conceptual): Anchors de validación, intake fallback y serie

| Campo | Contenido |
|---|---|
| Increment | 1 |
| Objective | Hacer anclable toda validación registrada (VC-1): campos de anchor (declared scope, command-set, effective inputs, factores ambientales, Scoped Content Identity) en el template de Plan y en el Amendment Log de RFC (rondas de auditoría); regla de intake fallback y clasificación (Change Level en el primer artifact; L0 provisional con triggers de upgrade; downgrade con justificación); serie como declaración + relaciones. |
| Problem solved | Validaciones sin estado reproducible (G1); clasificación informal; series sin identidad verificable. |
| Scope | `docs/plans/_TEMPLATE.md`, `docs/rfc/_TEMPLATE.md` (Amendment Log), `docs/CONVENTIONS.md`, `docs/VERSIONING.md` (referencias), headers de RFC/Plan (regla `Serie:`). |
| Out of scope | Checkpoint/closure (incremento 3); findings/pending (incremento 2); checkers (incremento 4). |
| Mechanisms | Campos de anchor; regla de intake; regla de serie; documento de guía de clasificación (sección en CONVENTIONS). |
| Dependencies | Incremento 0; RFC-71..74 como backfill opcional ejemplar (relación G1). |
| Migration | Los artifacts legacy sin campos nuevos siguen siendo válidos (ausencia = legacy, no invalidez); backfill opcional sin fabricar anchors históricos. |
| Validation | Batería + citas; verificación manual de un caso ejemplar (p. ej., re-anclar la validación de la batería en un Plan futuro). |
| Dogfooding | Los planes 95+ registran su primer anchor; la relación G1 se puede backfillear como ejemplo optativo. |
| Exit criteria | Template con campos de anchor; regla de intake/Level en CONVENTIONS; regla de serie; batería canónica según §24.1. |
| Rollback | Revertir commits; los registros con campos nuevos se tratan como legacy si se revierte. |
| Enables | Incremento 3 (mismo batch B: el checkpoint necesita anchors para ser significativo) y 2 (revalidación anclada). |

### Implementation Unit B — Incremento 3 (conceptual, desplegado en batch con 1): Git closure / checkpoint

| Campo | Contenido |
|---|---|
| Increment | 3 |
| Objective | Definir `Closed` como condición derivada con checkpoint verificable (GC-1): checkpoint ≠ anchor; consistencia (scoped identity + factores) antes de Closed; multi-commit/multi-RFC; docs-only se cierra sin release; semántica en el DoD de VERSIONING. |
| Problem solved | Planes `Executed` sin commit (87/92/93/91); cierre sin estado Git verificable. |
| Scope | `docs/VERSIONING.md:10. Definition of Done` (y §7), `docs/CONVENTIONS.md`, `docs/plans/_TEMPLATE.md` (sección de cierre/Nota de ejecución), `AGENTS.md` raíz (task lifecycle). |
| Out of scope | Refs de findings/pending (2); checkers de consistencia (4); migración forzada de planes pasados. |
| Mechanisms | Campos de checkpoint; regla de consistencia; semántica de Closed/rollback/tags inmutables. |
| Dependencies | Unidad A (Incremento 0) + Incremento 1 (batch operacional B: el checkpoint necesita anchors; el Incremento 3 no se renumera ni se absorbe). |
| Migration | Los planes legacy siguen `Executed` sin Closed; backfill opcional; ningún anchor histórico fabricado. |
| Validation | Batería + verificación de consistencia en el cierre del propio plan 3. |
| Dogfooding | Al cerrar el plan 3 (y los siguientes) se registra el primer checkpoint real; los planes 87/92/93/91 quedan como casos legacy documentados. |
| Exit criteria | `Closed` definido con checkpoint y consistencia; DoD actualizado; batería canónica según §24.1. |
| Rollback | Revertir commits; registros con campos nuevos tratados como legacy. |
| Enables | Unidad C (Incremento 2: post-close refiere planes cerrados; revalidación) y D (Incremento 4: checker de consistencia). |

### Implementation Unit C — Incremento 2 (conceptual): Findings, correcciones, revalidación y pending

| Campo | Contenido |
|---|---|
| Increment | 2 |
| Objective | Preservar lineage finding→corrección→revalidación con refs calificadas `<artifact>:F-<n>` (LC-1) y estados (open/partially-resolved/resolved/deferred/superseded, reopened); N:M; alcance de revalidación por corrección; pending per-artifact con dueño/escalación/resolución (PC-1); tabla de post-close. |
| Problem solved | G1 sin lineage; decisiones humanas solo en conversación; correcciones sin trazabilidad. |
| Scope | `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, template de Plan (sección findings/pending), `docs/rfc/75-change-lifecycle.md:Mecanismo 12 — Post-close Changes` como referencia normativa. |
| Out of scope | Tracker global (condicional, se decide con datos); entidades Finding/Correction/Decision; checkers (4). |
| Mechanisms | Convención de refs y estados; campos de pending; tabla post-close. |
| Dependencies | Unidades A y B (incrementos 0 y 1+3: cierre y anchors definidos). |
| Migration | Legacy sin refs válido; discriminador de ausencia; backfill opcional de G1 y de la decisión del plan 91. |
| Validation | Batería + caso de uso: registrar la decisión pendiente del mantenedor del plan 91 como primer pending formal (opcional) o el siguiente caso real. |
| Dogfooding | Los planes 95+ usan refs F-n y pending; el plan 91 queda como ejemplo de decisión pendiente persistida. |
| Exit criteria | Convención de refs/estados + pending + post-close en CONVENTIONS/template; batería canónica según §24.1. |
| Rollback | Revertir commits; refs nuevas pasan a legacy. |
| Enables | Unidad D (Incremento 4: checkers de refs/pending) y métricas de lineage con datos reales. |

### Implementation Unit D — Incremento 4 (conceptual): Automatización segura (gated en observabilidad)

| Campo | Contenido |
|---|---|
| Increment | 4 |
| Objective | Mecanizar solo lo observado como útil: presencia de anchor, formato de refs, consistencia checkpoint↔anchor, serie (relaciones), pending ownership, stale detection; vistas derivadas (índice de lifecycle) opcionales. |
| Problem solved | Errores humanos de registro; verificación manual costosa; consistencia no comprobable. |
| Scope | `tools/` (checkers dev nuevos) + `tests/` (suites stdlib con fixtures `tmp_path`) + `docs/VERSIONING.md:4.1 Batería canónica de verificación` (opcional/separado). |
| Out of scope | Autoridad normativa en checkers; umbrales de métricas; backend de telemetría; enforcement total. |
| Mechanisms | Checkers opcionales; script de consulta de métricas (derivadas de campos). |
| Dependencies | Unidades A–C (incrementos 0–3); **gate de observabilidad**: datos de lifecycle producidos por los incrementos 1/3/2 (no mediciones del Incremento 0) que muestren qué checks evitan errores (sin datos → no automatizar ese check). |
| Migration | Checkers solo sobre artifacts nuevos/registrados; legacy excluido. |
| Validation | Suites pytest de cada checker (estilo `tests/test_check_plan_citations.py`) + batería. |
| Dogfooding | Los checkers se corren sobre el propio repo; el plan 94 y planes 95+ son los primeros sujetos. |
| Exit criteria | Checkers opcionales implementados con tests; sin cambios normativos de autoridad; batería canónica según §24.1. |
| Rollback | Revertir checkers; nada normativo queda atado a ellos. |
| Enables | Enforcement parcial (§19); datos de lifecycle y observabilidad para decisiones futuras (tracker condicional, handoff). |

### Incremento 5 (conceptual) — Deferred / Future Track: Coordinación / handoff (fuera de alcance)

| Campo | Contenido |
|---|---|
| Increment | 5 |
| Objective | Habilitar la evaluación/diseño futuro de un mecanismo de continuidad y handoff multi-agente; no se asume un workflow u orchestrator determinados. |
| Problem solved | Copy/paste del mantenedor entre agentes. |
| Scope | Sin definir: requiere nueva decisión (RFC/ADR) con evidencia de los incrementos 0–4 (persistencia funcionando, métricas de coordinación EXPERIMENTAL). |
| Out of scope | Todo lo no decidido por RFC-75 (handoff, orchestration, atribución de agente, work-item IDs). |
| Mechanisms | Los hechos persistidos por las unidades A–D (incrementos 0–4) son los insumos; el mecanismo de entrega, si existe, pertenece al runtime/orchestrator, no al lifecycle. |
| Dependencies | Incrementos 0–4; datos de coordinación (deferidos). |
| Migration | n/a (no existe). |
| Validation | n/a hasta decidir alcance. |
| Dogfooding | n/a. |
| Exit criteria | RFC/ADR de alcance aprobados; no aplica a este plan maestro. |
| Rollback | n/a. |
| Enables | Evidencia persistida y observabilidad para la decisión futura de diseñar (o no) un mecanismo de handoff; el resultado no está predeterminado. |

### 18.1 Usable at every phase

| Si nos detenemos después de… | ¿ARgentOS DEV sigue funcional y desarrollable? | Justificación |
|---|---|---|
| Unidad A (Incremento 0) | Sí | Predominantemente documental; la batería existente define verde; el vocabulario nuevo no obliga a nada. |
| Unidad B (Incrementos 1+3) | Sí | Predominantemente documental; los campos nuevos son opcionales para legacy; solo los planes nuevos registran anchor/checkpoint. |
| Unidad C (Incremento 2) | Sí | Predominantemente documental; refs/pending solo aplican cuando existen findings/decisiones; nada obliga a usarlos en L0/L1. |
| Unidad D (Incremento 4) | Sí | Incorpora tooling/checkers y sus tests, todos opcionales; revertirlos no toca normativa. |

No hay fase que deje el repo en estado intermedio inutilizable: las unidades
son aditivas sobre artifacts existentes y se cierran según la política de
"batería verde" de §24.1 (batería realmente verde o desviación documentada
aceptada por el maintainer).

## 19. Estrategia de dogfooding

**[PROPOSED]** Progresión:

```text
observación → asistencia → recomendación → validación automática
→ enforcement parcial → workflow operativo
```

- **Unidad A (Incremento 0):** el vocabulario y las condiciones derivadas se usan de
  inmediato para redactar y cerrar los planes 95+; el plan 94 mismo es el
  primer sujeto (status `Executed` sin commit ≠ `Closed`).
- **Unidad B (Incrementos 1+3):** los planes 95+ registran anchor y checkpoint reales; el
  backfill ejemplar de la serie RFC-71..74 y de la relación G1 demuestra el
  mecanismo sin migrar nada.
- **Unidad C (Incremento 2):** la decisión pendiente del plan 91 (commit del mantenedor)
  es el candidato natural del primer pending formal; los findings de la
  auditoría 3.1 muestran el patrón a generalizar.
- **Unidad D (Incremento 4):** los checkers se corren sobre el propio repo; la
  decisión de automatizar usa los datos de lifecycle producidos por las
  unidades A–C (persist → observe → automate); no hay gate circular con el
  schema baseline del Incremento 0.
- **Enforcement total no es deseable al inicio:** L0/L1 siguen el camino corto;
  el enforcement parcial llega recién cuando la dogfooding lo justifica.

El lifecycle se usa para construir el lifecycle: el plan 94 (este documento)
es el primer artifact clasificado del cambio; su cierre documental y su
`Nota de ejecución` son el primer caso de la semántica que los incrementos
formalizan.

## 20. Grafo de dependencias

**[DERIVED]** Derivado del rollout real de RFC-75 y de las dependencias de
artifacts del repo (no copia de un grafo genérico):

```text
RFC-75 (Accepted) ── ADR-15/16 ── RFC-56
        │
        ▼
Unidad A ── Incremento 0 (semántica + vocabulario + schema de observabilidad)
        │
        ├─────────────────────────────────────┐
        ▼                                     ▼
Unidad B ── Incremento 1 (anchors + intake + serie)
Unidad B ── Incremento 3 (checkpoint/closure)   [batch operacional; el 3 no se renumera]
        └────────────┬────────────────────────┘
                     ▼
             Unidad C ── Incremento 2 (findings + pending + post-close)
                     │
                     ▼
             Unidad D ── Incremento 4 (safe automation, gated en los datos
                        de lifecycle producidos por A–C)
                     │
                     ▼
             Incremento 5 (Deferred / Future Track — handoff;
                           arquitectura no decidida)
```

El plan 94 es el nodo de derivación: los planes de implementación 95+ se
redactan desde este mapa maestro y de `docs/rfc/75-change-lifecycle.md`, no
reinventando arquitectura.

## 21. Registro de riesgos

| Riesgo | Mitigación |
|---|---|
| Burocracia en L0/L1 | Cambios triviales no pagan el ciclo (§9.2); L0 provisional; campos opcionales por nivel; sin checkers obligatorios antes de 4. |
| Checker como autoridad normativa | Regla ADR-16: `checker output = factual evidence ≠ normative authority`; "anchor missing" = GAP, no invalidación. |
| Scope inflation (RFC-75 → sistema gigante) | Lista de No-objetivos como guard; hipótesis no implementadas hasta demostrar necesidad; ADR candidates solo con criterio ADR-16. |
| Circularidad ("necesito el lifecycle para implementar el lifecycle") | Unidad A (Incremento 0) es predominantemente documental con la batería existente; dogfooding usa el repo real; no se depende de machinery nueva para empezar. |
| Human bottleneck persiste | Las unidades A–D (incrementos 0–4) persisten los hechos que un track futuro (Incremento 5) podría consumir; no se promete eliminación del bus sin ese mecanismo. |
| Stale validation silenciosa | Revalidación como backstop; consistencia checkpoint↔anchor antes de Closed (GC-1); límite declarado de entorno desconocido. |
| Contaminación del Protocol | Frontera DEV/Protocol (§5); ningún mecanismo escribe en `protocol/.agents/`; checkers dev-only. |
| Ejecución paralela sobre archivos compartidos | Lección de los planes 87/92/93/91 (archivos de gobernanza entrelazados): serializar por archivo compartido o reservar campos antes de tocar (regla de `docs/VERSIONING.md:8. Ejecución en paralelo`). |
| Legacy mal interpretado como inválido | Discriminador de ausencia de campos = legacy; legacy excluido de métricas; backfill opcional sin fabricar anchors. |
| Deuda de pytest vs "batería verde" | §23 + §24.1: resolver el test como deuda Clase C antes de cerrar unidades que exigen batería realmente verde, o registrar desviación documentada aceptada por el maintainer (precedente planes 86–93). |

## 22. Candidatos a ADR

No se crean ADRs en esta tarea. Se registran los candidatos que satisfacen
potencialmente el criterio de ADR-worthiness (`docs/adr/16-change-lifecycle-authority.md:Decisión`)
y cuya elevación debe decidirse en un Plan de implementación, no silenciosamente:

| Candidato | Criterio potencial (ADR-16) | Trigger de elevación | Decisión |
|---|---|---|---|
| **Change Level como eje normativo independiente de RFC-56** | (a) consumido fuera de la RFC originaria (todos los Planes futuros); (c) invariante arquitectónico persistente con riesgo de colisión con la clase RFC-56 | Cuando el primer Plan lo use para escalar machinery o haya una disputa de clasificación | `ADR CANDIDATE — REQUIRES FUTURE DECISION` |
| **Scoped Content Identity como identidad de correctness de validación DEV** | (c) invariante persistente que define validez/anclaje | Cuando se implemente el incremento 1 y se observe consumo cruzado (checkers, runtime DEV) | `ADR CANDIDATE — REQUIRES FUTURE DECISION` |
| **Frontera DEV/Protocol sin mecanismos compartidos** | (b)/(c) podría ser consumida por el lifecycle del Protocol en el futuro | Solo si el Protocol intenta heredar mecanismos DEV | `ADR CANDIDATE — REQUIRES FUTURE DECISION` (probablemente innecesario hoy: RFC-55 + RFC-75 la cubren) |

La semántica de `Closed`/checkpoint **no** es candidata: implementa ADR-15
(CL-3..CL-5) sin modificarla. La regla de serie no es candidata: implementa
AU-4 de ADR-16.

## 23. Deuda existente y hallazgos no bloqueantes

| Ítem | Estado | Impacto |
|---|---|---|
| El test `test_store_rebuild_is_derived_and_deterministic` de `tests/test_project_segment.py` falla (timestamp fijo vs reloj real: `STALE` esperado `FRESH`) | **[OBSERVED]** confirmado el 2026-09-01 | Preexistente, ajena a RFC-75. No bloquea la planificación; **sí condiciona** el criterio "batería verde" de las unidades B/C/D (incrementos 1/3/2/4) según la política de §24.1: batería realmente verde o desviación documentada aceptada por el maintainer. Resolver como deuda independiente (Clase C o plan B); no se presenta como PASS. |
| ~~Registro de RFC-75 y ADR-15/16 sin ítem en `CHANGELOG.md:[Unreleased]`~~ — **falso hallazgo, eliminado** | **[OBSERVED + DERIVED]** RFC-69 exige el ítem de `[Unreleased]` para **planes docs-only**, no para registros de RFC/ADR (`docs/rfc/69-documentation-taxonomy-and-layout.md:Versionado`); `Modelo conceptual` del changelog lista RFCs que gobiernan el significado de `.agents/`, y RFC-75 es gobernanza DEV sin impacto de protocolo; ADR-15/16 se registran en `docs/adr/INDEX.md`. Los commits `352ad18`/`c166520` fueron conformes al actualizar sus INDEX. | La obligación real de ítem en `[Unreleased]` recae sobre el propio plan 94 (plan docs-only) y se resuelve en su commit (decisión del mantenedor; ver §27 y `Nota de ejecución`). |
| `docs/plans/INDEX.md` intro con "Estado al 2026-08-16" desactualizado | **[OBSERVED]** | Menor; INDEX es descriptivo; actualizar cuando se registre la serie nueva. |
| `docs/VERSIONING.md:9. Estado actual (2026-08-17)` desactualizado | **[OBSERVED]** | Menor; es snapshot que se actualiza en releases; no bloquea. |
| `dev` ahead 2 de `origin/dev` (RFC-75 y ADR-15/16 sin push) | **[OBSERVED]** | Estado, no defecto; resolver en el próximo push del mantenedor. |
| Planes 87/92/93/91 `Executed` sin commit (y 91 con decisión pendiente) | **[OBSERVED]** | No es deuda a "arreglar": es la evidencia del problema que RFC-75 resuelve; cierre futuro opcional vía backfill (Mecanismo 15). |

## 24. Estrategia de validación

- **Definición de verde:** la batería canónica (`docs/VERSIONING.md:4.1 Batería
  canónica de verificación`) + H13 por juicio; `check_dist_sync.py` solo en
  `master`; tests del harness del producto en CI, no en la batería DEV.
  La interpretación de "verde" se define en §24.1.
- **Por incremento:** cada plan 95+ declara su propio criterio de entrada y
  salida con la template; los incrementos 1/3/2/4 exigen anchor y checkpoint en
  su propia Nota de ejecución (dogfooding).
- **Sin anchors fabricados:** ninguna validación histórica se re-ancla
  inventando estado (`Mecanismo 15 — Migration / Legacy`).
- **Consistencia:** antes de `Closed`, identidad scoped del cierre == anchor ∧
  factores declarados sin cambio; si difiere → revalidar (GC-1).
- **Evidencia factual:** los checkers son re-ejecutables; los claims requieren
  evidencia o atestación explícita (`docs/rfc/75-change-lifecycle.md:Seguridad e integridad`).

### 24.1 Política de interpretación de "batería verde"

El repositorio distingue la batería canónica (`docs/VERSIONING.md:4.1 Batería
canónica de verificación`), que incluye `pytest tests/`, del fallo preexistente
no relacionado (§23). Política de interpretación:

- **Batería realmente verde** = todos los checks de la batería canónica y todos
  los tests en PASS.
- **Fallo preexistente no relacionado** (p. ej., el test de timestamp fijo de
  §23) = **desviación documentada** cuando el criterio de cierre de una unidad
  lo requiera; **no se presenta como PASS** si el test está FAILED.
- La desviación documentada requiere **aceptación explícita del maintainer**
  para cerrar la unidad que la necesite. Es la terminología existente del repo
  (precedente: planes 86–93 reportaron fallos de pytest ajenos con nota y
  cerraron con batería "en verde" documentada como tal).
- Esta política no convierte la deuda en parte del Change Lifecycle: el test
  sigue siendo deuda preexistente independiente (§23), no un mecanismo del
  lifecycle, y no se inventa un sistema de estados nuevo.

## 25. Criterios de salida del Master Plan

El Master Action Plan está completo cuando:

- [ ] Reconstruye el lifecycle completo y lo contrasta con el estado real (§4).
- [ ] Inventaría el workflow actual sin inventar capacidades (§6).
- [ ] Mapea cada mecanismo/invariante de RFC-75 a su mecanismo futuro (§7).
- [ ] Aplica el modelo de autoridad de ADR-16 sin jerarquía total (§8).
- [ ] Define la economía L0–L3 distinguiendo lo decidido de lo pendiente (§9).
- [ ] Decide (con justificación) no introducir state machine (§10).
- [ ] Deriva estrategias de skills, artifacts, policies, checkers, Git y
      telemetría sin crear infraestructura prematura (§11–17).
- [ ] Propone unidades de implementación (sobre los incrementos conceptuales 0–5) con las 13 dimensiones, todas usables al detenerse (§18).
- [ ] Diseña dogfooding progresivo sin enforcement total inicial (§19).
- [ ] Incluye grafo de dependencias derivado del repo (§20), riesgos (§21),
      ADR candidates (§22), deuda (§23), validación (§24) y preguntas abiertas (§27).
- [ ] Pasa la auditoría adversarial interna (§28).
- [ ] Un agente distinto puede derivar planes 95+ sin reinventar la arquitectura.

## 26. Retrospectiva RFC-71..74 → invariantes

**[OBSERVED + DERIVED]** Matriz problema real → invariante RFC-75 → mecanismo
futuro → incremento, construida desde la evidencia citada en §2.3.

| Problema observado | Evidencia | Invariante RFC-75 | Mecanismo futuro | Incremento |
|---|---|---|---|---|
| Planes 86/87/92/93 `Executed` sin commit | Notas de ejecución citadas | CL-3/CL-4/CL-5 | Semántica Executed/Committed + checkpoint | 0 + 3 |
| Plan 91 `Executed` con decisión de commit pendiente del mantenedor | `Nota de ejecución` del 91 | PC-1 | Pending per-artifact con dueño | 2 |
| Validaciones reportadas sin commit/VERSION | `docs/adr/15-change-lifecycle-continuity.md:Contexto` | CL-1/CL-2, VC-1 | Anchor (scoped identity + factores) | 1 |
| G1 sin lineage finding→corrección→revalidación | `fcf6ce1`; ADR-15 Contexto | CL-6/7/8, LC-1 | Refs calificadas + estados + N:M | 2 |
| Serie RFC-71..74 / planes 86–93 sin identidad estable | `Serie:` en headers; INDEX | AU-4 | Serie derivada: declaración + relaciones | 1 |
| Decisiones de implementación (alternativa rechazada) solo en Nota | Plan 90 Nota de ejecución | CL-9 | Decision lineage + elevación ADR condicional | 0 + 2 |
| Coordinación entre agentes vía copy/paste | RFC-75 Problema | (handoff fuera de alcance) | Hechos persistidos (anchors/pending/checkpoint) → track futuro (Incremento 5) | 1–4 |
| Telemetría de proceso sin señales de reuse/cache | RFC-74; `PROTOCOL_METRICS.md` | Observability (Mecanismo 13) | Métricas de lifecycle derivadas de campos | 0 + 4 |

## 27. Preguntas abiertas

- **CAN DECIDE IN PLAN** (`docs/rfc/75-change-lifecycle.md:Preguntas abiertas`):
  formato de campos (anchor, checkpoint, refs); wording en CONVENTIONS/VERSIONING;
  checkers opcionales; calibración fina de umbrales; activación del tracker
  condicional (con datos); manejo de validaciones no deterministas.
- **IMPLEMENTATION:** queries de métricas; formato exacto de refs.
- **EXPERIMENTAL:** vistas derivadas de continuidad; métricas de coordinación;
  revalidación selectiva.
- **OUT OF SCOPE:** handoff mechanism; orchestration; atribución de agente;
  work-item IDs unificados.
- **Propias de este plan:** ¿elevar ya algún ADR candidate (§22) o al primer
  consumo? ¿Backfillear la relación G1 y la serie RFC-71..74 como ejemplares?
  ¿Registrar el ítem del plan 94 en `[Unreleased]` del changelog en el mismo
  commit del mantenedor?

## 28. Auditoría adversarial interna

| Criterio | Verdict | Evidencia / mitigación |
|---|---|---|
| Architectural leakage | OK | Ningún mecanismo propuesto usa artifacts/policies/skills del Protocol (§5); las skills del producto se excluyen (§11). |
| Scope inflation | OK | Los incrementos implementan solo los mecanismos de RFC-75; No-objetivos como guard (§18); ADR candidates sin decidir (§22). |
| Premature abstraction | OK | No hay entidades/state machines/databases/orchestrators nuevos (§10, §12); todo campo/relación sobre artifacts existentes. |
| Bureaucracy L0/L1 | OK | L0 sin Plan obligatorio; L1 = Plan/Nota + anchor + checkpoint; maquinaria por Level (§9.2); checkers no obligatorios antes de 4. |
| Authority confusion | OK | Clases de ADR-16 aplicadas (§8); INDEX descriptivo; checkers = evidencia factual. |
| Git confusion | OK | Executed/Committed/Closed/Promoted/Released diferenciados (§4.2, §15); multi-commit explícito. |
| Circular dependencies | OK | Unidad A (Incremento 0) predominantemente documental con batería existente; dogfooding incremental (§19). |
| Human bottleneck | OK | Los incrementos persisten los hechos que permiten reducir el bus; no se promete mecanismo de handoff en 0–4 (§16). |
| Protocol contamination | OK | Ninguna dependencia normativa sobre `protocol/.agents/` como regla DEV (§5). |
| Missing evidence | OK | Todo lo afirmado como estado actual tiene cita `ruta:sección` o verificación local (§2, §6). |
| Implementation ambiguity | OK | Un agente puede derivar planes 95+ desde §7/§9/§18 + `docs/rfc/75-change-lifecycle.md` sin reinventar la arquitectura. |

### Auditoría de consistencia post-corrección (A–J)

| Criterio | Verdict | Evidencia |
|---|---|---|
| A. RFC fidelity | OK | No se rediseñó RFC-75: rollout, invariantes y decisiones intactos; la distinción conceptual/unidades solo aclara terminología (§18). |
| B. ADR fidelity | OK | ADR-15/16 sin modificar; clases de autoridad y protocolo de conflicto aplicados (§8); sin jerarquía total. |
| C. Increment numbering | OK | Seis incrementos conceptuales 0–5; unidades A–D; 1+3 es batch operacional sin renumerar ni absorber el 3 (§18). |
| D. Operationalization | OK | Regla transversal Target semantics vs operationalization (§18); Incremento 0 no exige anchors operativamente (§9.2, §17). |
| E. Observability | OK | Incremento 0 define schema baseline sin fingir medición; gate del Incremento 4 no circular (§17, §18 D). |
| F. Validation | OK | "Verde" distingue PASS real de desviación documentada aceptada por el maintainer (§24.1); no se reporta PASS con test FAILED. |
| G. Scope | OK | Ningún mecanismo nuevo: solo terminología, política de interpretación y aclaraciones (§7–§18). |
| H. DEV/Protocol boundary | OK | Intacta: los mecanismos siguen sin tocar `protocol/.agents/` ni `dist/` (§5). |
| I. Increment 5 | OK | Deferred / Future Track; sin resultado predeterminado ni diseño de handoff (§18). |
| J. Implementation readiness | OK | Un agente puede derivar el plan 95 sin reinterpretar numbering, operationalization, observabilidad ni "verde" (§18, §24.1, §29). |

## 29. Veredicto final — Master Action Plan Verdict

**`READY FOR IMPLEMENTATION PLANNING`**

- **Nombre:** Plan 94 — Master Action Plan: Change Lifecycle de ARgentOS DEV
  (`docs/plans/94-change-lifecycle-master-action-plan.md`).
- **Incrementos conceptuales de RFC-75:** 6 (0–5). **Unidades de
  implementación iniciales:** 4 (A: Incremento 0; B: Incrementos 1+3 en batch
  operacional; C: Incremento 2; D: Incremento 4). Incremento 5 = Deferred /
  Future Track (fuera de alcance, arquitectura no decidida).
- **Principales dependencias:** RFC-75 `Accepted`; ADR-15/16; RFC-56; batería
  canónica según la política de §24.1 (PASS real o desviación documentada
  aceptada por el maintainer); resolución de la deuda de pytest (§23) antes de
  cerrar unidades con batería realmente verde; decisión del mantenedor sobre
  los planes `Executed` sin commit (backfill opcional).
- **Principales riesgos:** burocracia L0/L1; checker-como-autoridad; scope
  inflation; ejecución paralela sobre archivos compartidos (lección planes
  87/92/93/91); human bottleneck residual hasta que el track futuro (Incremento
  5) decida el mecanismo.
- **Decisiones pendientes:** formato de campos; wording; calibración fina;
  tracker condicional; checkers opcionales; elevación de ADR candidates.
- **ADR candidates:** Change Level como eje independiente; Scoped Content
  Identity; frontera DEV/Protocol (todos `REQUIRES FUTURE DECISION`).
- **Deuda no bloqueante:** test de timestamp fijo (condiciona "batería verde"
  según §24.1); ítem de `[Unreleased]` del propio plan 94 pendiente de decisión
  del mantenedor; INDEX/VERSIONING snapshots desactualizados; `dev` ahead 2.
- **Primer incremento recomendado:** **Unidad A (Incremento 0)** (semántica +
  vocabulario + observability schema baseline).
- **Por qué:** es predominantemente documental, no depende de machinery nueva,
  se valida con la batería existente, deja el repo plenamente usable y crea el
  lenguaje que las unidades B/C/D (incrementos 1/3/2/4) necesitan para
  implementar anchors, checkpoints, findings y automatización sin reinterpretar
  RFC-75.

## Trazabilidad

Origen → RFC-75 (`Accepted`, commit `352ad18`) → ADR-15/16 (`Accepted`, commit
`c166520`) → este Master Action Plan (plan 94) → planes de implementación
futuros (95+: unidades A–D sobre los incrementos conceptuales
0 → {1,3} → 2 → 4) → implementación → validación → cierre. Este plan no
autoriza cambios de payload (RFC-56); la autorización de los incrementos se
resuelve en cada Plan según su clase.

## Nota de ejecución

- 2026-09-01 — Entregado el Master Action Plan (plan 94) como documento único
  de esta tarea. **Alcance:** mapa maestro; no se ejecutó ningún incremento; no
  se modificaron `protocol/.agents/`, `runtime/`, `tests/`, `tools/` ni
  `CHANGELOG.md`; sin bump de `VERSION` ni tag (docs-only, RFC-69).
  **Registro:** plan 94 registrado en la Vigésima sexta serie de
  `docs/plans/INDEX.md` (requisito estructural del mirror,
  `tools/check_plan_structure.py`). **Verificación:** `check_plan_structure.py`
  y `check_plan_citations.py` en verde; `check_protocol_invariants.py`,
  `check_taxonomy_coherence.py`, `check_session_artifacts.py` y
  `check_version_state.py` en verde (warnings esperados de dev);
  el test `test_store_rebuild_is_derived_and_deterministic` (de
  `tests/test_project_segment.py`) confirmado como fallo preexistente ajeno a
  este plan (§23). **Estado según
  RFC-75:** plan 94 queda `Executed` (entregable producido y verificado) pero
  **no** `Closed` (sin checkpoint/commit todavía: el commit lo realiza el
  mantenedor, y con él el ítem en `CHANGELOG.md:[Unreleased]` que RFC-69 exige
  para planes docs-only, si así lo decide) — primer caso de dogfooding de la
  semántica definida en el propio plan.
- 2026-09-01 — **Correction pass final (sin rediseño).** Aplicadas las siete
  correcciones sobre el Plan 94: (1) los incrementos 0–3 son
  predominantemente documentales y el 4 incorpora tooling/checkers y tests (ya
  no se afirma "todos docs-only"); (2) se distinguen los **seis incrementos
  conceptuales de RFC-75** (0–5) de las **unidades de implementación
  iniciales** (A: 0; B: 1+3 en batch operacional sin renumerar; C: 2; D: 4),
  con el 5 como Deferred / Future Track; (3) regla transversal **Target
  semantics vs operationalization** en §18 (VC-1/GC-1/LC-1/PC-1 siguen siendo
  reglas objetivo hasta que su incremento materializa el mecanismo); (4) el
  Incremento 0 define **schema baseline de observabilidad** sin fingir
  medición de las cuatro métricas (dependen de campos de los incrementos
  1/3/2), y el gate del Incremento 4 usa datos de lifecycle reales (no
  circular); (5) falso hallazgo de CHANGELOG eliminado de §23: RFC-69 exige el
  ítem de `[Unreleased]` para **planes docs-only**, no para registros de
  RFC/ADR; la obligación real es del propio plan 94 en su commit; (6) política
  de "batería verde" en §24.1: PASS real vs desviación documentada aceptada
  por el maintainer, sin reportar PASS con test FAILED; (7) Incremento 5
  suavizado a track futuro sin resultado predeterminado. **Sin cambios en
  `protocol/`, `runtime/`, `tests/`, `tools/`, VERSION ni `CHANGELOG.md`; sin
  commit (decisión del mantenedor, práctica del repo).** Verificación:
  checkers estructurales y de citas en verde; pytest con el fallo preexistente
  reportado como desviación documentada, no como PASS (§24.1).
