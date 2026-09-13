# RFC-75 — Change Lifecycle de ARgentOS DEV

**Status:** Accepted (2026-09-01; registro formal tras auditoría final de diseño; implementación materializada por los Incrementos 0–4 — planes 95–101, 2026-09-02/03 —, con el Incremento 5 fuera de alcance por decisión de la propia RFC)
**Fecha:** 2026-09-01
**Serie:** Change Lifecycle (gobernanza del repo fuente) | —
**Origen:** Serie de auditorías y scope definition v2 (2026-08-25..31), corregida hasta v5; evidencia RFC-71..74, G1, planes 86–93, spike de reconstrucción, auditorías adversariales independientes.
**Pregunta:** ¿Cómo debe funcionar el lifecycle de un cambio en ARgentOS DEV — desde el requerimiento/problema hasta el cierre (y eventual release) — de forma reproducible, auditable, continuable y escalable por impacto, sin entidades, máquinas de estados ni registros innecesarios?
**Afectados:** gobernanza del repo fuente (`AGENTS.md`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, templates, checkers dev); sin cambios de payload.

> Convención de evidencia: las afirmaciones sobre el estado actual del repo se
> citan con `ruta:sección`. Las decisiones de esta RFC se marcan como
> **Decisión**; los requisitos de implementación futura como
> **Requisito de implementación futura**.

## Problema

El lifecycle real de ARgentOS DEV pierde información en fronteras concretas:
validaciones sin anchor reproducible (G1), findings/correcciones sin lineage,
`Executed` sin semántica de cierre Git (planes 87/92/93/91), decisiones humanas
pendientes solo en conversación, series multi-plan/multi-RFC sin identidad
estable, y coordinación entre agentes dependiente del copy/paste del
mantenedor. La metodología observada en RFC-71..74 fue más rigurosa que el
lifecycle formal; esta RFC formaliza lo observado sin crear maquinaria
desproporcionada (CL-10).

## Contexto

- El repo se gobierna por `AGENTS.md` raíz + `docs/CONVENTIONS.md` +
  `docs/VERSIONING.md`; `protocol/.agents/` es data, no reglas para Dev.
- Autoridad previa: ADR-15 (CL-1..CL-10), ADR-16 (AU-1..AU-7), RFC-56
  (clases A/B/C y autorización de payload).
- Evidencia: RFC-71..74 (refinamiento adversarial, aceptación docs-only,
  release batch), G1 (fix + checker + tests sin lineage), plan 90 (decisión de
  implementación con alternativa rechazada persistida), AUDITORIA_SISTEMA
  (patrón de findings), releases batch (3.18+3.19; 3.20–3.25; 3.26–9.0;
  10.1–10.3).
- El spike de reconstrucción midió: contexto reconstruible 69% (control) → 84%
  (serie+vista); finding lineage y validaciones anclables 0% (datos ausentes);
  una vista derivada mejora descubrimiento pero no recupera información nunca
  persistida.

## Objetivos

1. Hacer reconstruible el estado de un cambio sin conversación (continuity,
   CL-1..CL-10).
2. Anclar toda validación registrada a un estado reproducible (CL-1/CL-2).
3. Preservar lineage finding→corrección→revalidación (CL-6/7/8) sin entidad
   Finding.
4. Definir el cierre de Plan por intención y trazabilidad Git, no por conteo de
   commits (CL-3/4/5).
5. Escalar machinery por impacto (CL-10), sin burocracia en L0/L1.
6. Resolver conflictos por autoridad humana (AU-3) sin jerarquía total.
7. Permitir incrementos implementables sin romper el lifecycle actual.

## No-objetivos

Fuera del alcance: entidad `Change`; ID universal de work item; Change State
Machine global; handoff artifact obligatorio; Skills obligatorias; orchestration
automática; release automation; anchors históricos fabricados; entidad/registry
de `Series`; entidad `Finding`; entidad `Decision`; tracker universal
obligatorio; lifecycle backend universal; lifecycle común Dev/Protocol. Si un
concepto se volviera indispensable, debe reabrirse la decisión mediante RFC/ADR;
ninguno lo hace en esta versión.

## Terminología

- **Change** (coloquial): una evolución del repo; no entidad.
- **Change Level**: eje de rigor/machinery (L0–L3).
- **RFC-56 class**: eje de autorización de payload (A/B/C); no aplica a cambios
  runtime/tools/tests-only.
- **Anchored validation**: validación con anchor reproducible.
- **Git checkpoint**: relación closure↔estado Git verificable.
- **Closed**: condición derivada (no status): Executed + governance + checkpoint.
- **Serie**: identidad derivada de declaraciones + relaciones; INDEX = vista.
- **Finding**: registro lógico de defecto dentro de un artifact, con ref
  calificada (no entidad arquitectónica).

## Sistema actual

Statuses de Plan: `Aprobado para redacción`, `Aprobado para ejecución`,
`Executed`, `Executed (parcial)`, `Superseded`. RFC `Proposal → Accepted →
Superseded`; ADR `Proposal → Accepted → Superseded` (16 ADR). Checkers dev
(batería canónica + CI); INDEX descriptivos; invariante versión↔changelog↔tag
(check_version_state); `dist` regenerado por CI. Gaps: §Problema.

## Principios arquitectónicos

- `FACTUAL ≠ NORMATIVE ≠ DECISION ≠ RELEASE ≠ DESCRIPTIVE` (ADR-16).
- Continuity es propiedad del lifecycle; handoff es mecanismo transversal que la
  consume (fuera del alcance de esta RFC).
- Persistir ≠ materializar; una vista derivada nunca es autoridad.
- Los mecanismos se definen como **relaciones/campos/vistas** sobre artifacts
  existentes; no familias nuevas.
- Persist → observe → automate.
- Garantía ≠ evidencia: "registrado" no implica "verdadero"; PASS es evidencia
  de ejecución dentro de un entorno declarado, no garantía de corrección
  semántica.

## Modelo de lifecycle

```text
intake → classification → [RFC → ADR?] → acceptance → Plan → execution
→ validation → [finding → correction → revalidation] → Git checkpoint
→ closure → [promotion → release] → [post-close finding → impact assessment
→ new action]
```

**Condiciones derivadas (no state machine; los únicos status son los existentes
de Plan/RFC/ADR):**

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
Released sin Verified = violación de gobernanza. Closed ≠ release;
execution parcial ≠ closure exitoso.

## Mecanismo 1 — Intake

- **Decisión:** todo cambio (feature/bug/problem/debt/audit finding/observation/
  acción directa del mantenedor/propuesta de agente) se clasifica en su tracker
  de origen (backlog/auditoría/roadmap); sin tracker, la clasificación se
  registra en el **primer artifact del cambio** (borrador de RFC, Plan, Nota o
  mensaje de commit). Sin ID universal; los IDs locales son metadata.
- **Clasificación:** origen/tipo; clase RFC-56 (cuando aplique); Change Level;
  scope; RFCs/Plans afectados; riesgo; coordinación. La clasificación es mutable
  (CL-10): upgrade obligatorio al descubrir complejidad; downgrade con
  justificación documentada.
- **L0 provisional:** un cambio que inicia como L0 deja de serlo al activarse un
  trigger (finding, revalidación requerida, decisión ADR-worthy, múltiples RFCs,
  impacto release-critical, impacto arquitectónico); el Level se recomputa
  antes de continuar. **Toda validación citada como evidencia es una validación
  registrada → el anchor aplica** (CL-1), independientemente del Level.

## Mecanismo 2 — Change Levels

**Decisión:** `Level = max(coordination, scope, architectural impact, release
impact, duration/complexity)`. El número de commits no es dimensión. RFC-56
A/B/C (autorización de payload) y Change Level (rigor del lifecycle) son ejes
independientes: una Clase A pequeña puede ser L2; una Clase C grande puede ser
L2/L3 por scope; runtime-only tiene Level sin clase.

Umbrales coarse por dimensión (0–3):

| Dimensión | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| coordination | 1 agente, 1 sesión | 1 agente, multi-sesión | multi-agente o planes paralelos | cross-RFC / serie orquestada |
| scope (superficie) | 1 archivo | área acotada (una capa del repo) | multi-área (≥2 capas: docs/runtime/tools/tests/payload) | multi-área + contratos |
| architectural impact | sin cambio estructural | cambio estructural local, aditivo/reversible | cambio estructural entre límites (nuevo módulo/seam) | cambio de semántica de modelo/contratos/invariantes, irreversible |
| release impact | sin versión | changelog-only | MINOR | MAJOR / batch |
| duration/complexity | <1 sesión | 1 sesión | multi-sesión | multi-semana |

**Fronteras de architectural impact:** ≠ RFC-56 class (mide profundidad
estructural/footprint/irreversibilidad, no autorización); ≠ scope (profundidad
vs superficie: refactor masivo sin cambio semántico = scope 2–3, impacto 1–2);
≠ release impact (refactor profundo sin cambio de contrato = impacto 2–3,
release 1). La calibración fina de umbrales es decisión de Plan; los umbrales
coarse de esta tabla determinan el Level antes de crear el Plan.

## Mecanismo 3 — RFC lifecycle

- **Decisión:** los estados existentes son suficientes
  (`Proposal → Accepted → Superseded`); no se crea máquina nueva.
- Refinamiento/auditoría = **actividad** dentro de Proposal, registrada en el
  Amendment Log; **cada ronda de auditoría es una validación sujeta a CL-1/CL-2**
  con anchor = estado del draft de la RFC + estado del repo + scope de
  validación. El Amendment Log es lineage semántico; Git es la fuente de
  versionado (sin versionado paralelo).
- **Aceptación:** batería verde, citas resolubles, findings bloqueantes cerrados,
  findings no bloqueantes registrados como observations, decisión humana (AU-3).
- Contradicción con ADR → escalar (AU-3). Cambio tras Accepted → enmienda vía
  Amendment Log + nuevo plan; nunca reescritura silenciosa.

## Mecanismo 4 — ADR integration

- **Decisión:** ADR-worthiness (ADR-16) se evalúa en la aceptación de la RFC, en
  la aprobación del Plan y ante hallazgos durante ejecución/validación
  (elevación retrospectiva). Una decisión requiere ADR si (a) es consumida fuera
  de la RFC que la originó, (b) supersede o modifica un ADR existente (incluidas
  consecuencias), o (c) es un invariante arquitectónico persistente.
- **Reglas duras:** un Plan nunca modifica un ADR silenciosamente (AU-5); un ADR
  no autoriza payload (AU-2; RFC-56).

## Mecanismo 5 — Plan lifecycle

Statuses existentes preservados; semántica:

- `Aprobado para redacción`: entregables documentales.
- `Aprobado para ejecución`: autorizado a ejecutar cuando los criterios de
  entrada se cumplen; si no, se documenta el gate pendiente como aclaración
  (sin status nuevo).
- `Executed` = implementación + validación (CL-4); puede existir sin commit.
- `Executed (parcial: <falta>)`: entregables incompletos.
- `Superseded`: semántica existente.
- **`Closed` (condición derivada)** = `Executed` + governance aplicable +
  checkpoint + consistencia checkpoint↔anchor. `Closed ≠ Released`.

**Matriz de governance (aplicabilidad derivada de características declaradas
del Plan):**

| Tipo de Plan | Governance (always / when applicable / not required) |
|---|---|
| docs-only | documentación + INDEX si aplica (always); checkpoint (always) |
| runtime/tools/tests-only | Plan/Nota + validación (always); checkpoint (always) |
| version-producing | documentación + CHANGELOG + VERSION según reglas existentes (always); checkpoint (always) |
| RFC-related | Amendment Log del RFC si corresponde (when applicable); RFC/INDEX coherentes (always) |
| ADR-worthy | ADR registrado si la decisión fue elevada (when applicable) |
| findings pendientes | resueltos o explícitamente diferidos con destino/ownership (always) |

**Closed es terminal para ese Plan:** un problema posterior genera artifacts
nuevos (Plan/RFC/ADR/corrección) que referencian al cerrado; la historia no se
reescribe (RFC-46).

## Mecanismo 6 — Validation Anchors

**Decisión:** el anchor representa el estado relevante de una validación
concreta. Conceptos distintos:

- **declared scope** — intención del autor (qué afirma cubrir la validación);
  no es evidencia de que todo fue ejecutado.
- **validation command-set** — los comandos exactos que constituyen la
  validación.
- **effective inputs** — los inputs que el command-set efectivamente consume
  (contenido del repo y fuera de él), determinados por observación cuando el
  tooling lo permite o declarados con evidencia; la evidencia es auditable
  (un sucesor puede re-ejecutar con instrumentación).
- **observed dependencies** — subconjunto de effective inputs descubierto por
  instrumentación.
- **environmental factors** — inputs fuera del repo consumidos (tool versions,
  env vars, servicios externos, imagen Docker, intérprete, DB, red).
- **Scoped Content Identity** — identidad sobre los effective inputs que son
  contenido del repo (no whole-tree; la relevancia es propiedad del
  command-set, no del repo: un test puntual → relevancia pequeña; una
  herramienta que escanea todo → relevancia grande).
- **validation validity** — relativa al anchor (CL-2): `anchor changed ≠
  semantic validity changed`; evaluar aplicabilidad; revalidar o marcar stale.

**Límite explícito:** el lifecycle no puede garantizar corrección frente a
dependencias desconocidas nunca detectadas/declaradas; es un límite aceptable y
una responsabilidad del autor de la validación (regla de evidencia), con
revalidación como backstop. No se introduce mecanismo para eliminarlo.

## Mecanismo 7 — Git Checkpoints

- **Decisión:** checkpoint = relación closure↔estado Git verificable (no
  artifact); **checkpoint ≠ validation anchor** (el commit de cierre puede
  incluir governance: INDEX, CHANGELOG, ADR, docs).
- **Consistencia checkpoint↔anchor:** `Closed` exige que la **identidad scoped**
  del estado de cierre sea igual a la del anchor **y que los factores
  ambientales declarados no hayan cambiado**; si difiere cualquiera →
  revalidación antes de Closed. Factores irrelevantes (no consumidos) y
  desconocidos no invalidan automáticamente (CL-2/CL-10); un factor relevante
  consumido pero no declarado es una anomalía auditable.
- **Git semantics:** commit SHA = locator, no identidad semántica; ante
  rebase/cherry-pick/amend con contenido scoped idéntico no hay invalidación
  automática; con contenido distinto → stale → revalidar. Rollback = versión
  nueva; tags inmutables.

## Mecanismo 8 — Findings / Corrections / Revalidation

- **Decisión:** los findings son **relaciones de lineage** (origin → observation
  → correction → revalidation → result) con refs calificadas
  `<artifact>:F-<n>` (p. ej. `RFC-74:F-01`, `PLAN-91:F-03`); el namespace
  pertenece al artifact del registro. Sin entidad arquitectónica `Finding`.
- **N:M:** 1 finding → N corrections; N findings → 1 correction; 1 correction →
  N revalidations.
- **Estados (metadata):** `open`, `partially-resolved`, `resolved`, `deferred`
  (postergado con owner/destino), `superseded` (sustituido/duplicado; ≠
  resolved; nunca borrado silenciosamente). Un finding `resolved` demostrado
  incorrecto se reabre mediante un nuevo finding que referencia al original
  (o metadata `reopened`).
- **Movimiento:** la ref original permanece históricamente válida; el artifact
  sucesor referencia la original; registro local nuevo solo si se necesita.
- **Post-close/post-release:** la corrección se registra en el artifact que la
  posee con ref explícita al Plan cerrado y al finding original
  (p. ej. `PLAN-94:C-01` → `PLAN-91:F-03`); destino según la tabla de
  post-close. Sin entidad global de Correction.
- **Tracker:** condicionado a criterios (cross-plan/RFC, estado consultable,
  acumulación); decisión de Plan con datos de observabilidad; no universal.

## Mecanismo 9 — Pending Decisions

- **Decisión:** la decisión pendiente se registra en el **artifact que posee la
  decisión** (el que requiere la resolución), con refs a todos los artifacts
  bloqueados; metadata: blocking/no-blocking, owner, escalación, resolución,
  evidencia, efecto downstream, ADR-worthiness. Sin entidad `Decision`.
- **Ownership:** si el owner se supersede/elimina/cierra → transferir al
  sucesor o escalar al humano; **nunca desaparece**. Si dos artifacts reclaman
  ownership → el humano decide; refs a todos los reclamantes (AU-3).
- **Persistencia de la decisión humana:** decisión + evidencia + artifacts
  afectados + resolución, registrada en los artifacts afectados y en el registro
  del pendiente.

## Mecanismo 10 — Authority / Conflict Resolution

- **Decisión (ADR-16):** clases FACTUAL (Git/checkers/tags), NORMATIVE (RFC
  Accepted, ADR, Plan aprobado), DECISION (humano), RELEASE (tag/dist),
  DESCRIPTIVE (INDEX, nunca autoritativa). Sin jerarquía universal
  RFC > ADR > Plan > Git.
- **Protocolo:** detect → classify → escalate → human decision → correct
  artifact → revalidate. Los agentes detectan y escalan; nunca resuelven
  conflictos normativos por autoridad propia. Medios de detección ejemplares:
  git diff, citation checker, structural checker, cross-artifact review, human
  review. `checker output = factual evidence ≠ normative authority`.

## Mecanismo 11 — Series / Continuity

- **Decisión:** la serie es una **identidad derivada** de declaraciones
  (`Serie:` en RFC; `Serie:` opcional en Plan) + relaciones verificables
  (RFC↔Plan, release). La membresía requiere declaración coincidente **+**
  verificación de relaciones (la coincidencia textual aislada no basta). INDEX =
  vista derivada (AU-4); sin entidad/registry/artifact de Series.
- **Bordes:** serie sin release (posible, docs-only); multi-release (posible);
  supersession de miembros (la serie sobrevive); renombrado (cambio de
  declaración con historia); RFC en más de una evolución (`Serie:` repetible o
  declaración a nivel Plan); Plan sin `Serie:` (derivada de su RFC + release);
  conflicto de declaraciones → detect → escalar → humano corrige.

## Mecanismo 12 — Post-close Changes

| Situación | Acción |
|---|---|
| corrección trivial | correction + revalidation |
| cambio que requiere Plan | nuevo Plan |
| cambio que altera modelo RFC | nueva/enmendada RFC |
| decisión arquitectónica persistente | ADR (ADR-worthiness) |
| cambio de payload/versionado | RFC-56 + versión correspondiente |
| post-release correction | nueva acción/versión según impacto |

Límites derivados de RFC-56 + ADR-15/16. `Closed` nunca se reabre; la nueva
acción referencia al cerrado.

## Mecanismo 13 — Observability

Métricas permanentes (SHOULD; calculadas de campos existentes; sin backend ni
writer obligatorio): validation anchor coverage; finding lineage coverage;
stale validation rate; Git closure anomalies. **Legacy excluido del
denominador**; 0 registros = not applicable / insufficient sample, no "0%
compliance". Métricas de coordinación (cross-agent, handoffs, cross-RFC,
pending count, revalidation frequency): EXPERIMENTAL/DEFERRED (solo si el track
de coordinación inicia).

## Mecanismo 14 — Automation

- **Safe automation (mecánica):** checks de citas, consistencia de status,
  presencia de anchor, existencia de ref Git, derivación de INDEX, detección de
  stale (anchor vs estado actual).
- **Human-required:** conflicto normativo, ADR-worthiness, severidad, escalación
  de scope, autorización de release, materiality ambiental.
- **Regla:** `checker output = factual evidence ≠ normative authority`;
  "anchor missing" = GAP, no "validation invalid"; la aplicabilidad es juicio.
  Persist → observe → automate.

## Mecanismo 15 — Migration / Legacy

- **Decisión:** nada se migra obligatoriamente. Legacy: RFC-71..74, planes
  86–93, ADR-01..16, validaciones/findings históricos. Backfill opcional
  (ejemplares): relación G1; serie de RFC-71..74. Prohibido fabricar anchors
  históricos no demostrables.
- **Coexistencia:** un artifact nuevo puede referenciar uno legacy; el legacy no
  se reescribe para cumplir metadata nueva; el legacy se excluye de métricas
  nuevas salvo backfill explícito. **Discriminador:** la ausencia de campos
  nuevos (anchor, refs) indica legacy, no invalidez. In-flight Plan durante un
  incremento: puede terminar bajo reglas previas (marcado legacy) o adoptar las
  nuevas; el trabajo nuevo adopta las reglas nuevas.

## Dev vs Protocol

```text
DEV Change Lifecycle ≠ Protocol Lifecycle
```

- Esta RFC gobierna cómo se desarrolla/evoluciona ARgentOS DEV; no gobierna
  automáticamente la evolución del Protocol.
- Un cambio con efecto payload sigue RFC-56 (RFC Accepted + plan). No se crean
  workflow/policy/state machine/artifact/skill compartidos; no hay herencia
  automática. Principios transferibles (revalidación ante continuidad;
  persistir ≠ materializar; separación evidencia factual / autoridad normativa)
  quedan como principios, no mecanismos: si un principio debe volverse normativo
  en el Protocol, lo hará por el lifecycle propio del Protocol.

## Rollout incremental

`0 → {1,3} → 2 → 4` (incremento 5 de coordinación/handoff fuera del alcance).

- **0** — semántica + vocabulario + observabilidad baseline (documental; sin
  machinery).
- **1** — anchor (scoped identity + factores), intake fallback, serie.
- **3** — Git closure (checkpoint ≠ anchor; consistencia). 1 y 3 se introducen
  en el mismo batch (el checkpoint necesita anchors para ser significativo).
- **2** — findings (refs calificadas, N:M), pending (dueño), revalidación.
- **4** — automatización segura (gated en observabilidad).

Cada incremento deja ARgentOS DEV utilizable y más gobernado; rollback = revert
el cambio del incremento (los registros con campos nuevos se tratan como legacy
si se revierte el incremento).

## Modos de fallo

Resumen: todo fallo se resuelve con detect → classify → escalate (normativo) o
revalidar (factual); nunca invalidación automática por cambio de anchor, nunca
reescritura de historia, nunca resolución normativa por código. Casos: anchor
missing/stale; working tree dirty; rebase/cherry-pick; RFC vs ADR; Plan vs RFC;
INDEX vs fuente; finding sin resolver; post-close; pending; Level subestimado o
escalado; planes/RFCs superpuestos; release batch; legacy sin metadata; agente
desaparece; agente propone decisión normativa.

## Seguridad e integridad

- Trazas inmutables (RFC-46): Amendment Logs, tags, histórico de sesión no se
  reescriben.
- Autoridad por clase (ADR-16): nada fabrica evidencia; los checkers son
  evidencia factual re-ejecutable; los claims requieren evidencia o atestación
  explícita.
- Git identity: commit SHA ≠ identidad semántica (locator); identidad relevante
  = scoped content identity.
- Límite declarado: dependencias ambientales desconocidas no son verificables
  por el lifecycle; responsabilidad del autor + revalidación.

## Alternativas consideradas

- Identidad: entidad `Change` (rechazada) vs continuidad relation-based
  (elegida).
- Findings: entidad (rechazada) vs relaciones + tracker condicional (elegida).
- Decisions: registry universal (rechazada) vs per-artifact (elegida).
- Git closure: commit-based (insuficiente, multi-commit) vs relation-based
  checkpoint (elegida).
- Series: registry/entidad (rechazadas, AU-4) vs declaración + relaciones
  (elegida).
- State: máquina global (rechazada, derivabilidad) vs derived conditions
  (elegida).
- Automation: automation-first (rechazada, riesgo RFC-74) vs
  persist → observe → automate (elegida).
- Change Level: extensión de RFC-56 (rechazada, colisión de ejes) vs eje
  independiente que compone (elegida).
- Anchor: whole-tree identity (rechazada, falsos stale) vs scoped content
  identity (elegida); manual declaration sin evidencia (rechazada) vs
  declaration + evidence + revalidation (elegida).

## Compatibilidad

Statuses, templates, checkers, INDEX, VERSIONING existentes: sin ruptura;
adiciones incrementales. ADR-01..16, RFCs y planes existentes: legacy
compatibles. Batería canónica permanece como definición de verde.

## Preguntas abiertas

- **CAN DECIDE IN PLAN:** formato de campos; wording en CONVENTIONS/VERSIONING;
  checkers opcionales; calibración fina de umbrales; activación del tracker
  condicional (con datos de observabilidad); manejo de validaciones no
  deterministas (anclar la ejecución + revalidar si el set de inputs cambia).
- **IMPLEMENTATION:** queries de métricas; formato de refs.
- **EXPERIMENTAL:** vistas derivadas de continuidad; métricas de coordinación;
  revalidación selectiva.
- **OUT OF SCOPE:** handoff mechanism; orchestration; atribución de agente;
  work-item IDs unificados.

## Resumen de decisiones

- **INHERITED:** ADR-15 (CL-1..CL-10), ADR-16 (AU-1..AU-7), RFC-56 (A/B/C).
- **DERIVED:** vocabulario (Executed/Committed/Closed/Verified/Promoted/
  Released); serie como propiedad derivada; findings como relaciones de lineage.
- **DECIDED BY THIS RFC:** Change Levels (umbrales coarse + max); anchor con
  Scoped Content Identity y factores ambientales; checkpoint ↔ anchor
  (consistencia); refs calificadas de findings + hogar post-close; pending
  per-artifact con dueño; matriz de governance; métricas; rollout 0→{1,3}→2→4;
  límite explícito de entorno desconocido.
- **DEFERRED:** tracker condicional; automatización selectiva; métricas de
  coordinación; vistas/handoff.

## Invariantes

- CL-1..CL-10 y AU-1..AU-7 heredados (ADR-15/16).
- RFC-56: autorización de payload = RFC Accepted + Plan; Change Level no
  autoriza.
- VC-1: toda validación registrada tiene anchor (scoped identity + factores
  declarados).
- GC-1: todo Plan cerrado tiene checkpoint con consistencia (scoped + factores).
- LC-1: toda corrección enlaza a origen y revalidación con ref calificada.
- PC-1: toda decisión pendiente bloqueante persiste en el artifact que bloquea;
  nunca desaparece.

## Trazabilidad

- Origen: auditorías + scope definition v2 → v3 → v4 → v5 → esta RFC → futuros
  planes (incrementos 0→{1,3}→2→4) → implementación → validación → cierre.
- Relaciones normativas: ADR-15 (invariantes de continuidad/checkpoint/lineage);
  ADR-16 (autoridad/decision model); RFC-56 (autorización de payload).

## Impacto en el protocolo

Ninguno: esta RFC gobierna el Change Lifecycle de ARgentOS DEV (docs de
gobernanza, templates, checkers dev). No modifica `protocol/.agents/`; no
produce bump de `VERSION` ni tag; cambio docs-only (RFC-69).

## Criterios de aceptación

> **Convención de evidencia de esta lista.** Cada criterio se marca contra
> evidencia existente y verificable, citada con `ruta:sección` o con el plan y
> los commits que la materializaron. Los incrementos 0–4 se desplegaron como
> Unidades A–D (`docs/plans/94-change-lifecycle-master-action-plan.md:18.
> Planificación incremental`) y se registran en el `## Amendment Log` de esta
> RFC. Reconciliación normativa: Plan 118 (2026-09-13, H-1).

- [x] El lifecycle Dev queda definido: intake, classification, RFC, ADR cuando
      corresponde, Plan, execution, validation, findings/corrections,
      revalidation, checkpoint, closure, promotion/release cuando aplique.
      **Evidencia:** `## Modelo de lifecycle` y `## Mecanismo 1`–`## Mecanismo 15`
      de esta RFC; `docs/CONVENTIONS.md` (siete secciones operacionales del
      Change Lifecycle DEV); `docs/VERSIONING.md:7. Estados de planes y RFCs`
      (condiciones derivadas) y `:10. Definition of Done`. Materializado por los
      cuatro incrementos (planes 95–101) y operacionalizado en
      `.agents/workflows/change-lifecycle.md:Change Lifecycle — Operational
      Workflow (ARgentOS DEV)`.
- [x] `Level = max(dimensiones)` con umbrales coarse y ejes independientes de
      RFC-56. **Evidencia:** `## Mecanismo 2 — Change Levels` (tabla de umbrales
      coarse y fronteras con RFC-56 union); `docs/CONVENTIONS.md:Change Lifecycle
      — Change Levels (modelo objetivo)`;
      `.agents/workflows/change-lifecycle.md:1. Change detection and
      classification` (clasificación e intake);
      campo `**Change Level:**` en `docs/plans/_TEMPLATE.md`.
- [x] El anchor distingue declared scope / command-set / effective inputs /
      observed dependencies / environmental factors / Scoped Content Identity /
      validity; sin whole-tree por defecto. **Evidencia:** `## Mecanismo 6 —
      Validation Anchors` (definición de los siete conceptos y límite
      explícito del whole-tree); `docs/CONVENTIONS.md:Change Lifecycle —
      Validation anchors y Scoped Content Identity (regla operacional; VC-1,
      Incremento 1)`; `.agents/policies/validation-closure.md:1. Registered
      validation and anchors (VC-1)`; contenedor
      `## Validation anchor` de `docs/plans/_TEMPLATE.md`; generador
      `tools/scoped_content_identity.py`.
- [x] El límite de dependencias ambientales desconocidas está declarado sin
      mecanismo inventado. **Evidencia:** `## Mecanismo 6 — Validation Anchors`
      («Límite explícito»); `## Seguridad e integridad` («Límite declarado»);
      `.agents/policies/validation-closure.md:2. Validity is relative to the
      anchor (CL-2)` (responsabilidad del autor con
      revalidación como backstop).
- [x] Checkpoint ≠ anchor; Closed exige consistencia (scoped + factores).
      **Evidencia:** `## Mecanismo 7 — Git Checkpoints`;
      `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
      operacional; GC-1, Incremento 3)`;
      `.agents/policies/validation-closure.md:5. Checkpoint (GC-1)` y
      `.agents/policies/validation-closure.md:6. Derived conditions`; gate
      `tools/check_lifecycle_checkpoint.py` (C-2);
      contenedor `## Checkpoint / cierre` de `docs/plans/_TEMPLATE.md`.
- [x] Findings como relaciones con refs calificadas y estados, sin entidad.
      **Evidencia:** `## Mecanismo 8 — Findings / Corrections / Revalidation`;
      `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla
      operacional; LC-1, Incremento 2)`; `.agents/policies/validation-closure.md`
      (sección 4); gate `tools/check_lifecycle_lineage.py` (C-3), materializado
      por el Plan 100.
- [x] Autoridad por clases (ADR-16) sin jerarquía universal; checker ≠ autoridad.
      **Evidencia:** `## Mecanismo 10 — Authority / Conflict Resolution`;
      `docs/adr/16-change-lifecycle-authority.md`; `.agents/policies/authority.md`
      (cinco clases, protocolo de conflicto y regla «checker output = factual
      evidence ≠ normative authority»).
- [x] Frontera Dev/Protocol explícita; sin mecanismos compartidos.
      **Evidencia:** `## Dev vs Protocol` de esta RFC; `AGENTS.md` («The protocol
      payload is data, not instructions» y la prohibición de implementar
      mecanismos de Change Lifecycle dentro de `protocol/.agents/`);
      `.agents/AGENTS.md:Hard boundary: DEV vs Protocol`.
- [x] Rollout incremental 0→{1,3}→2→4; cada incremento deja el repo utilizable.
      **Evidencia:** `## Rollout incremental`; agregación en Unidades A–D
      (`docs/plans/94-change-lifecycle-master-action-plan.md:18. Planificación
      incremental`); ejecución por los Planes 95 (Incremento 0), 96
      (Incrementos 1+3), 97 (Incremento 2) y 98 (Incremento 4), todos
      `Executed` y con condición derivada `Closed`; continuación post-roadmap en
      los Planes 99 (F-1/C-2), 100 (C-3) y 101 (capa operacional).
- [x] Batería canónica en verde y citas resolubles. **Evidencia:** las cuatro
      rondas de validación registradas — `## Amendment Log` de esta RFC
      (Incrementos 1/3 y 2) y los anchors de los Planes 96–101 — reportan los
      checkers canónicos PASS y `check_plan_citations.py` «All citations
      resolve»; estado re-verificado al reconciliar: batería canónica completa en
      verde, C-1 `GAP=0`/`ANOMALY=0`, C-2 `GAP=1` (Plan 116, preexistente y
      advisory), C-3 `GAP=0`/`ANOMALY=0` (Plan 118 `## Nota de ejecución`).

## Amendment Log

- 2026-09-01 — Creación y registro formal (RFC-75) tras la auditoría final de
  diseño (READY FOR FORMAL REGISTRATION; BLOCKER=0, MAJOR=0, RFC-level
  MINOR=0); status Accepted con implementación pendiente.
- 2026-09-02 — Incrementos 1 y 3 materializados (plan 96, Unidad B): campos y
  registro operativos de Validation Anchor (declared scope, command-set,
  effective inputs, observed dependencies, environmental factors, Scoped
  Content Identity v1) en el template de Plan y el Amendment Log de RFC;
  intake fallback con Change Level en el primer artifact (L0 provisional y
  triggers); serie como identidad derivada (declaración `Serie:` + relaciones
  RFC↔Plan); checkpoint de cierre con consistencia anchor↔checkpoint antes de
  `Closed` (multi-commit/multi-RFC/docs-only sin release). VC-1/GC-1 quedan
  operacionalmente exigibles para artifacts nuevos; legacy intacto (ausencia
  de campos = legacy, no invalidez). Cambio docs-only: sin `VERSION` bump ni
  tag (RFC-69).
- 2026-09-02 — Incremento 2 materializado (plan 97, Unidad C): reglas
  operativas de findings (`<artifact>:F-<n>`, estados, N:M, post-close por
  referencia), corrections como registro de provenance (`C-<n>`; registro
  factual/traceability, no fuente normativa) y pending decisions per-artifact
  (PC-1), para artifacts nuevos, con guías en `docs/CONVENTIONS.md` y en los
  templates de Plan y RFC. LC-1/PC-1 pasan de semántica objetivo a
  operacionalmente exigibles para artifacts nuevos; legacy intacto (ausencia de
  campos = legacy, no invalidez). Cambio docs-only: sin `VERSION` bump ni tag
  (RFC-69).
- 2026-09-02 — **Incremento 4 materializado** (plan 98, Unidad D): automatización
  segura mínima sobre los datos de lifecycle producidos por las Unidades B/C
  (`## Mecanismo 14 — Automation`, sin automatización completa). Herramientas
  `tools/check_lifecycle_anchor.py` (C-1, chequeo de presencia y consistencia del
  Validation Anchor, VC-1) y `tools/check_lifecycle_checkpoint.py` (C-2, chequeo
  del checkpoint y su consistencia con el anchor aplicable, GC-1), con sus
  contratos de exit code — `GAP` advisory nunca cambia el exit code; solo
  `ANOMALY` lo hace — y sus suites en `tests/`. Commits `669a576` (C-1),
  `9b5b8a1` (C-2) y `0d2d7fd` (estabilización del dogfooding sobre el repo real);
  registro del Plan en `aa68704`. Cambio DEV tools/tests-only: sin `VERSION` bump
  ni tag.
- 2026-09-02 — **F-1 corregido** (plan 99): el chequeo C-2 seleccionaba el anchor
  aplicable por recencia en lugar de por correspondencia con el estado de cierre,
  lo que producía ambigüedad ante revalidaciones múltiples. La corrección
  establece la semántica ya normada en `## Mecanismo 7 — Git Checkpoints` y en
  `.agents/policies/validation-closure.md:5. Checkpoint (GC-1)`: la selección es por
  **correspondencia** del estado validado con el estado de cierre — nunca por
  recencia («latest A2 wins») ni por pertenencia genérica al árbol. Commit
  `42da250`; registro del Plan en `51cabb2`. Cambio DEV tools/tests-only: sin
  `VERSION` bump ni tag.
- 2026-09-02 — **C-3 materializado** (plan 100): tercer gate determinista
  `tools/check_lifecycle_lineage.py` (C-3), que verifica forma, completitud
  mínima y consistencia interna del lineage de findings, correcciones y
  revalidaciones (LC-1) en el contenedor `## Findings / Correcciones / Pending`:
  refs calificadas `<artifact>:F-<n>`/`C-<n>`, vocabulario de estados, elementos
  inmutables del finding, provenance y alcance de revalidación de la corrección,
  marcadores de ausencia y consistencia de resolución; `### Pending decisions`
  queda fuera del alcance v1. Commit `1ffe24c` (checker + suite); registro del
  Plan en `d93d234`. Cambio DEV tools/tests-only: sin `VERSION` bump ni tag.
- 2026-09-03 — **Capa operacional DEV materializada** (plan 101): `.agents/` como
  interfaz de operación del Change Lifecycle para agentes — `AGENTS.md` (reglas
  operativas fundamentales y ruteo de lectura bajo demanda),
  `workflows/change-lifecycle.md` (ejecución paso a paso del lifecycle:
  intake, clasificación, gate de autorización, plan, ejecución, evidencia,
  anchors, findings/correcciones, checkpoint, cierre y GAP/ANOMALY/STOP),
  `policies/authority.md` (clases de autoridad, protocolo de conflicto,
  ADR-worthiness, discovery documental y stop conditions),
  `policies/validation-closure.md` (VC-1, CL-2, A2, LC-1, GC-1, condiciones
  derivadas y stop conditions) y `policies/lifecycle-checkers.md` (integración y
  vocabulario de los gates C-1/C-2/C-3). La capa es **operacional, no normativa**:
  enruta a la autoridad de `docs/` y no la duplica ni la reemplaza. Commit
  `3706570`; registro del Plan en `7bcda08`. Cambio DEV docs-only: sin `VERSION`
  bump ni tag.
- 2026-09-13 — **Reconciliación normativa de cierre del MVP** (plan 118,
  decisión humana H-1 autorizada por el mantenedor): se registran en este
  `## Amendment Log` las cuatro materializaciones posteriores que ningún plan
  había autorizado a registrar (Incremento 4, F-1, C-3 y capa operacional
  `.agents/`), se corrige el header — que declaraba implementación pendiente — y
  se marcan los diez criterios de aceptación con su evidencia rastreable.
  `docs/VERSIONING.md:4.1 Batería canónica de verificación` registra además los
  gates de lifecycle C-1/C-2/C-3 como conjunto adicional advisory/factual. Esta
  entrada **no cambia ningún mecanismo, invariante ni decisión** de la RFC:
  reconcilia su registro con el estado real ya alcanzado. Cambio DEV docs-only:
  sin `VERSION` bump ni tag (RFC-69).
