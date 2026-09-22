# Plan 149 — ARgentOS Capability & Autonomy Roadmap

**Status:** Executed (2026-09-22; roadmap estratégico A → B → C materializado en `ROADMAP.md` y verificado — ver `## Checkpoint / cierre` y `## Nota de ejecución`)
**Fecha:** 2026-09-22
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=0, release impact=0, duration/complexity=0)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, un dominio. *scope*: área acotada —una capa DEV (`ROADMAP.md` y su registro documental)—. *architectural impact*: **0** —el Change **declara** una dirección estratégica pero no crea ni modifica estructura: sin entidad, registry, state machine, autoridad, checker, contrato, seam ni código; la representación del mapa es documental. *release impact*: ninguno (docs-only, sin `VERSION`, sin tag). *duration/complexity*: menos de una sesión.
**Depende de:** — (no depende de un plan previo; los Planes 146/147/148 y las iniciativas históricas son el punto de partida que este roadmap no reabre)
**Origen:** pedido directo del mantenedor (Change «Plan 149 — ARgentOS Capability & Autonomy Roadmap», 2026-09-22), que autoriza actualizar `ROADMAP.md` con el roadmap estratégico acordado.

## Objetivo

Plasmar en `ROADMAP.md` el roadmap estratégico acordado por el mantenedor —tres
etapas, A → B → C, con dependencia explícita y orden de ejecución— integrándolo
con el estado actual del documento y preservando su estructura y sus
convenciones. El objetivo estratégico que el documento debe reflejar es el
cambio de enfoque: primero determinar qué capacidades y garantías de ARgentOS
están realmente demostradas; luego completar las fronteras necesarias para
alcanzar una autonomía operacional mayor; recién después incorporar nuevas
features basadas en las necesidades descubiertas.

El Change es **exclusivamente de planificación y documentación**: no implementa
features, no ejecuta la retrospectiva, no audita el repositorio, no modifica
runtime, `protocol/`, tests, CI, RFCs ni ADRs, y no crea mecanismos, autoridades
ni artefactos de gobernanza nuevos. Su único efecto es la representación del
roadmap y su registro.

## Alcance y límites

Dentro del Scope: materializar en `ROADMAP.md` el roadmap estratégico de las
Etapas A, B y C con su dependencia, reconciliar localmente el resto del
documento con esa dirección (sin reescribirlo) y registrar el Change (este Plan,
`docs/plans/INDEX.md`, `CHANGELOG.md`).

Fuera del Scope, explícitamente:

- ejecutar la Etapa A, la Etapa B o la Etapa C; hacer la retrospectiva; construir
  el Capability & Guarantee Matrix;
- implementar autonomía, ejecución de provider/model o cualquier feature;
- crear RFCs, ADRs, checkers, policies, workflows, state machines, registries,
  entidades globales, métricas o artefactos administrativos;
- modificar `protocol/` (incluido `protocol/.agents/`), `runtime/`, `tools/`,
  `tests/`, CI, `.agents/`, RFCs, ADRs o planes cerrados;
- reabrir Plan 146, Plan 147, Plan 148, Change Lifecycle MVP, SAE MVP, Prompt
  Cache MVP, Jury Trial MVP, Placement Contract, RFC-75, ADR-15 o ADR-16;
- actualizar `CHANGELOG.md` salvo la entrada que el workflow vigente exige para
  un plan docs-only;
- actualizar cualquier otro documento sólo por simetría, y reclamar una supuesta
  divergencia de publicación entre `dev` y el Protocol.

## Criterio de entrada

- [x] `dev` = `c8971dd48f23c4abee842026d9627c8536da1cf5`; `git status --porcelain` → 0 modificaciones rastreadas y 1 archivo untracked **externo** (`MASTER_PENDING_WORK_INVENTORY.md`, ajeno a este Change).
- [x] `ROADMAP.md` leído y su estructura relevada: mapa operativo (trabajo activo / dogfood, pendientes que requieren autorización, candidatos futuros, trazabilidad histórica, proceso).
- [x] `docs/plans/INDEX.md` confirmado como fuente descriptiva de estado; el próximo número libre es **149** (último registrado: Plan 148).
- [x] Convenciones del documento respetadas: español, afirmaciones ancladas con `ruta:sección`, tablas para el mapa y remisión a `docs/plans/INDEX.md` para el estado detallado.
- [x] Estado del que parte el roadmap verificado: `protocol/.agents/VERSION` = `11.6.2`; DEV y Protocol son dominios separados; `dist` publica el payload del Protocol.
- [x] Autorización explícita del mantenedor para materializar el roadmap acordado en `ROADMAP.md` (consigna del Change, 2026-09-22).

## Entregables

1. `ROADMAP.md` — sección `## Roadmap estratégico — Etapas A → B → C` con las tres etapas, su dependencia explícita, las fronteras candidatas (declaradas candidatas) y la regla de admisión de features, más la reconciliación localizada del resto del documento.
2. `docs/plans/149-argentos-capability-and-autonomy-roadmap.md` (**este archivo**) — registro del Change.
3. `docs/plans/INDEX.md` — registro del Plan 149 (serie + fila).
4. `CHANGELOG.md` — ítem `[Unreleased]` del Change, conforme a la regla de changelog para planes docs-only.

## Pasos

1. Verificar el baseline (`dev`, HEAD, árbol de trabajo) y confirmar `ROADMAP.md`, `docs/plans/INDEX.md` y `docs/VERSIONING.md` como fuentes.
2. Relevar la estructura de `ROADMAP.md` e identificar sus secciones y convenciones, sin reescribir el documento.
3. Materializar en `ROADMAP.md` el roadmap estratégico A → B → C: cambio de enfoque, dependencia, Etapa A (unidad de análisis, pregunta central, alcance conceptual, niveles de madurez, matriz y regla fundamental), Etapa B (objetivo, dirección, fronteras candidatas y resultado esperado con `Autonomy ⊆ Scope ∩ Authority`) y Etapa C (condiciones de admisión y subordinación).
4. Declarar en el mismo documento qué **no** es una entrada del roadmap y el estado del que parte (Protocol `11.6.2`, DEV/Protocol separados, `dist` publica el payload, sin feature de Protocol pendiente de publicación, iniciativas históricas no reabiertas).
5. Reconciliar localmente el resto del documento: trabajo activo (sin trabajo activo; Etapa A como próximo trabajo declarado, no autorizado por el documento) y la sección de proceso (las etapas no son trabajo ejecutable desde el mapa).
6. Registrar el Change: este Plan, `docs/plans/INDEX.md` y el ítem de `CHANGELOG.md`.
7. Ejecutar la batería canónica, los gates C-1/C-2/C-3 y la verificación factual del roadmap.
8. Registrar el Validation Anchor, el checkpoint y la nota de ejecución, y determinar los impactos (documentación / roadmap).

## Delegación agentiva

No se declara delegación: el Change es documental, de un solo artefacto de
contenido, y su trabajo semántico —redactar el roadmap en el documento— es el
propio del Change; no hay `Task` que delegar a un Agent Worker.

## Criterios de salida

- [x] Las tres etapas aparecen en el orden A → B → C y su dependencia (`A → B → C`) es explícita.
- [x] La Etapa A se presenta como revisión de garantías —unidad de análisis *capacidad + garantía + evidencia* y Capability & Guarantee Matrix— y no como auditoría documental ni limpieza de archivos.
- [x] La Etapa B declara que comienza a partir de los resultados de A y que sus fronteras son **candidatas**, no compromisos de implementación.
- [x] La Etapa C queda subordinada a las necesidades descubiertas en A y B; ninguna feature entra por disponibilidad tecnológica.
- [x] `ROADMAP.md` no agrega compromisos de implementación, no reabre iniciativas históricas y no reescribe lo que ya no es trabajo abierto.
- [x] Ninguna etapa del roadmap fue ejecutada; no se construyó la matriz; no se implementó ninguna feature.
- [x] 0 diff fuera del Scope: `protocol/`, `runtime/`, `tools/`, `tests/`, CI, `.agents/`, RFCs, ADRs y planes cerrados intactos.
- [x] Batería canónica y gates C-1/C-2/C-3 registrados con evidencia.

## Verificación

```text
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Más la verificación factual del roadmap: orden A → B → C, dependencia explícita,
fronteras candidatas declaradas candidatas, ausencia de compromisos de
implementación, y 0 diff fuera del Scope (`git status --porcelain` y
`git diff --stat HEAD`).

## Validation anchor

- **Declared scope:** las dos rutas de contenido que la identidad de contenido mide — `CHANGELOG.md` y `ROADMAP.md`. Quedan fuera del scope **medido** la governance del Change (este artefacto de Plan y su registro en `docs/plans/INDEX.md`), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 114/116/134/140–148); no hay otros paths en el Change.
- **Validation command-set:** los siete comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + la verificación factual del roadmap y del Scope (`git status --porcelain`, `git diff --stat HEAD`, `git diff --name-only HEAD`).
- **Effective inputs (repo content):** el scope declarado; `docs/plans/INDEX.md` como espejo descriptivo; `docs/VERSIONING.md` (batería canónica, política de changelog, estados de planes y snapshot vigente); RFC-75 (Mecanismo 2 y Mecanismo 7); el corpus completo de `docs/plans/` como población de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada del checker de invariantes; y el estado Git de `dev`.
- **Observed dependencies:** stdlib únicamente; el CLI `git` disponible para las identidades de contenido y la resolución de objetos. Sin red.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; git 2.55.0.windows.5; repositorio bajo OneDrive; `check_dist_sync.py` **no** aplica (se espera verde sólo en `master`, y este Change no promueve). El archivo untracked externo `MASTER_PENDING_WORK_INVENTORY.md` no pertenece a este Change y se conserva sin tocar.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `a13d455cf8fe7fe2e956d4e96420e0d835263e42` — tree id del estado validado sobre el scope medido, resuelto con un índice aislado sobre el contenido staged de las dos rutas.
  - **Delta scoped identity (scope S = las dos rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `b3cad0cf694e3c1d197636ba77949595296e235b0e2093e0a53ab94eb4d171b0`.
  - **Límite declarado:** el scope medido excluye la governance del Change (este artefacto y `docs/plans/INDEX.md`); la identidad se computó antes de escribir los registros de cierre.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `ROADMAP.md`.
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

## Checkpoint / cierre

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio del mantenedor: `docs(roadmap): declare the capability and autonomy roadmap A-B-C (plan 149)`. Se identifica por su mensaje (convención anti-circularidad: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `a13d455cf8fe7fe2e956d4e96420e0d835263e42`, delta scoped identity `b3cad0cf694e3c1d197636ba77949595296e235b0e2093e0a53ab94eb4d171b0`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `b3cad0cf694e3c1d197636ba77949595296e235b0e2093e0a53ab94eb4d171b0` / `a13d455cf8fe7fe2e956d4e96420e0d835263e42`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de cierre incluye la governance del Change (este artefacto y `docs/plans/INDEX.md`), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7) y el árbol material queda verificable con `git log -1 --format=%T`.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió; verificado por C-2, que clasificó este artefacto `VALID`.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 149 (serie + fila); `CHANGELOG.md` `[Unreleased]` registra el Change; `ROADMAP.md` declara el roadmap estratégico A → B → C. Sin RFC, sin ADR, sin `VERSION` bump, sin tag, sin push.
- **Documentation impact:** `REQUIRED` — reconciliado. Documento afectado principal: `ROADMAP.md` (aspecto: no declaraba el roadmap estratégico vigente ni su orden de dependencia, de modo que la dirección del trabajo futuro no era legible desde el mapa operativo; actualización: sección `## Roadmap estratégico — Etapas A → B → C`, reconciliación del trabajo activo y de la sección de proceso; evidencia: el documento en el estado validado, con los checkers documentales en verde). Documentos afectados además por el registro del Change: `docs/plans/INDEX.md` y `CHANGELOG.md`. El snapshot de versiones de `docs/VERSIONING.md` **no** se toca: sin release no cambia y su política declara que se reconcilia en los puntos de promoción/release. `README.md`, `AGENTS.md`, `.agents/AGENTS.md` y las policies/workflows activos no se modifican: ninguna instrucción activa cambia y la batería canónica no gana comandos. No se actualiza ningún documento histórico (RFC-46).
- **Roadmap impact:** `REQUIRED` — el propio Change **es** la reconciliación del mapa operativo y de la dirección de trabajo futuro: declara las Etapas A, B y C, su orden de dependencia (A → B → C), las fronteras candidatas de autonomía y la regla de admisión de nuevas features; el artefacto que lo posee es `ROADMAP.md`, con el registro descriptivo en `docs/plans/INDEX.md`. No crea trabajo ejecutable desde el mapa: ninguna etapa queda autorizada por este documento.
- **Condición derivada:** `Closed` (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia: la ejecución no detectó ningún defecto propio dentro del Scope que exigiera una corrección posterior a la verificación.

### Correcciones

No findings detected / N/A — declaración de ausencia: no hubo corrección posterior a la verificación; el Change se materializó en una sola pasada.

### Pending decisions

No se registran pending decisions: el Change no introduce ninguna decisión bloqueante, no crea autoridad nueva y no deja trabajo abierto dentro de su Scope. La ejecución de la Etapa A es el próximo Change declarado por el mantenedor, no una pending decision de este Plan.

## Riesgos

- **Convertir el roadmap estratégico en un backlog de implementación.** Mitigación: las fronteras de la Etapa B se declaran **candidatas, no compromisos**; la Etapa C exige necesidad identificada; el documento explicita qué no es una entrada del roadmap.
- **Presentar A, B y C como tres iniciativas independientes.** Mitigación: la dependencia A → B → C se declara en el diagrama, en el texto y en la sección de proceso.
- **Convertir la Etapa A en una auditoría documental.** Mitigación: el documento fija la unidad de análisis (*capacidad + garantía + evidencia*), la pregunta central y la regla fundamental de que evalúa garantías operacionales.
- **Comprometer trabajo futuro desde un documento de estado.** Mitigación: ninguna etapa se autoriza desde `ROADMAP.md`; cada una es un Change propio y el mapa lo dice explícitamente.
- **Reabrir iniciativas cerradas.** Mitigación: los Planes 146–148, los MVP y RFC-75/ADR-15/ADR-16 figuran como estado histórico del que se parte, nunca como trabajo pendiente.
- **Reescribir el documento completo.** Mitigación: las secciones operativas existentes se preservan; el cambio es aditivo y localizado, más la reconciliación mínima del trabajo activo y del proceso.

## Trazabilidad

Decisión estratégica del mantenedor (Change «Plan 149 — ARgentOS Capability & Autonomy Roadmap», 2026-09-22) → **este Plan** → la sección `## Roadmap estratégico — Etapas A → B → C` de `ROADMAP.md` → próximo Change: ejecución integral de la Etapa A. Estado histórico que sirve de punto de partida: Planes 146/147/148, Change Lifecycle MVP, SAE MVP, Prompt Cache MVP, Jury Trial MVP, Placement Contract, RFC-75, ADR-15 y ADR-16.

## Nota de ejecución

*2026-09-22. Ejecutado en `dev` @ `c8971dd48f23c4abee842026d9627c8536da1cf5`, árbol de trabajo sin modificaciones rastreadas al inicio (1 archivo untracked externo, `MASTER_PENDING_WORK_INVENTORY.md`, ajeno a este Change).*

**Verificación realizada.** Batería canónica (`docs/VERSIONING.md:4.1 Batería canónica de verificación`): `check_protocol_invariants --payload protocol .` PASS (215 archivos, 10334 referencias verificadas); `check_plan_citations` PASS («All citations resolve»); `check_plan_structure` PASS («All numbered documents conform»); `check_taxonomy_coherence` PASS; `check_session_artifacts` PASS; `check_version_state` PASS con los warnings de tags esperados en `dev`; `python -m pytest tests/` → **1186 passed**, sin fallos. Gates de lifecycle sobre el árbol final: **C-1 `VALID`** (149 planes inspeccionados; `EXCLUDED=94, VALID=55, GAP=0, ANOMALY=0`), **C-2 `VALID`** para el Plan 149 contra el anchor aplicable A1 (`EXCLUDED=94, VALID=54, GAP=1, ANOMALY=0`, con el `GAP` histórico del Plan 116 conservado) y **C-3 `N/A`** por ausencia declarada (`EXCLUDED=97, N/A=23, VALID=29, ANOMALY=0`). `check_dist_sync.py` no se ejecutó: es local-only y se espera verde sólo en `master`, y este Change no promueve.

**Qué se materializó.** `ROADMAP.md` gana la sección `## Roadmap estratégico — Etapas A → B → C`: cambio de enfoque, diagrama de dependencia, Etapa A (unidad de análisis, pregunta central, alcance conceptual mínimo, los ocho niveles de madurez, Capability & Guarantee Matrix y regla fundamental), Etapa B (objetivo, dirección del Orchestrator, fronteras a investigar, las trece fronteras candidatas y el resultado esperado `Autonomy ⊆ Scope ∩ Authority` con la frontera humana), Etapa C (regla de admisión y subordinación), la lista de lo que **no** es una entrada del roadmap y el estado del que parte. La reconciliación del resto del documento es localizada: el encabezado declara la existencia del roadmap estratégico y su orden; la tabla de trabajo activo registra que ninguna etapa está en ejecución y que la Etapa A es el próximo trabajo declarado, no autorizado por el documento; y `## Proceso` gana el punto 4 con la regla de admisión. Las secciones operativas preexistentes —pendientes que requieren autorización, candidatos futuros y trazabilidad histórica— se preservan sin reescribirse.

**Verificación factual del roadmap.** Las tres etapas aparecen en el orden **A → B → C** (`### Etapa A`, `### Etapa B`, `### Etapa C`); la dependencia es explícita en el diagrama y en el texto («**B depende de A** y **C depende de los resultados de A y B**»); la Etapa A se define por garantías (`capacidad + garantía + evidencia`, la matriz y «no es una limpieza documental»); la Etapa B declara sus fronteras como «**candidatas, no compromisos de implementación**»; y la Etapa C declara «No agregar features por disponibilidad tecnológica». No se agregó ningún compromiso de implementación ni feature al mapa.

**Alcance.** Cuatro paths: `ROADMAP.md` (sección nueva más reconciliación localizada), `CHANGELOG.md` (ítem `[Unreleased]`), `docs/plans/INDEX.md` (serie Octogésima más fila) y `docs/plans/149-argentos-capability-and-autonomy-roadmap.md` (este registro). `git diff --name-only HEAD` → sólo `CHANGELOG.md`, `ROADMAP.md` y `docs/plans/INDEX.md`; el artefacto del Plan es nuevo. `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/`, RFCs, ADRs y planes cerrados con **0 diff**. El único archivo untracked ajeno al Change (`MASTER_PENDING_WORK_INVENTORY.md`) se conserva sin tocar.

**No realizado (por diseño).** No se ejecutó ninguna etapa del roadmap; no se hizo la retrospectiva; no se construyó el Capability & Guarantee Matrix; no se implementó autonomía, ejecución de provider/model ni ninguna feature; no se creó ninguna RFC, ADR, checker, policy, workflow, state machine, registry, entidad, métrica ni artefacto administrativo; no se modificó `CHANGELOG.md` más allá del ítem que el workflow exige para un plan docs-only; y no se reabrió ninguna iniciativa histórica.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1).
Committed = TRUE  — commit atómico en `dev`, identificado por su mensaje.
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump, sin tag, sin promoción a `master`, sin `dist`.
```
