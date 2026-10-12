# Plan 155 — Refresh documental post-autonomía e integración de clientes

**Status:** Executed
**Fecha:** 2026-10-11
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only, docs-only sobre `docs/`, `README.md`, `CHANGELOG.md`, `ROADMAP.md` y este artefacto; sin efecto en `protocol/`, `runtime/`, `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no aplica)
**Clase:** B (mejora documental compatible; `protocol/.agents/` no se toca, por lo que RFC-56 no aplica)
**Change Level:** L2 (`max(coordination=0, scope=2, architectural impact=1, release impact=0, duration/complexity=2)`; `docs/rfc/75-change-lifecycle.md:Mecanismo 2`). *coordination*: 1 agente, 1 sesión, un dominio — no hay coordinación multi-agente ni multi-sesión. *scope*: multi-área DEV (`README.md` + `CHANGELOG.md` + `ROADMAP.md` + `docs/VERSIONING.md` + un documento DEV nuevo + `docs/plans/INDEX.md`); sin tocar el payload. *architectural impact*: **1** — no crea mecanismo, entidad, registry, state machine, autoridad, checker ni contrato; declara conceptualmente patrones ya existentes y suma **un** documento DEV a una familia existente (Normative policy, `docs/*.md`), resuelto por el Placement Contract §6 sin enmienda. *release impact*: ninguno (docs-only sin efecto en `protocol/.agents/`; sin `VERSION` bump, sin tag, RFC-69). *duration/complexity*: una sesión de trabajo documental multi-archivo. El Level se recomputa si se activa un trigger.
**Depende de:** — (no depende de un plan abierto; los Planes 149–154 y el estado Git publicado son el punto de partida que este Change audita, no reabre)
**Origen:** pedido directo del mantenedor (Change «DOCUMENTATION REFRESH — POST AUTONOMY & CLIENT INTEGRATION», 2026-10-11), que autoriza explícitamente (a) crear y ejecutar este Plan como vehículo de gobernanza del refresh y (b) reconciliar el drift de versión contra el estado Git verificado (`12.0.0`)
**Superseded por:** —
**Motivo de retiro:** —

## Objetivo

Reconstruir el estado real de ARgentOS **después** de las features de autonomía
(Planes 151–153, modelo de autonomía y ADR-19) y de la integración/adopción de
clientes (Plan 154, RFC-81, layout canónico `.argentos/` y lifecycle), auditar
la documentación existente contra ese estado, y materializar los cambios que la
auditoría demuestre necesarios: reconciliar el drift, cerrar los gaps, y agregar
la pieza documental que explica **cómo trabaja** el sistema —estados,
orquestación, autonomía, gates, ejecución, clientes y ciclos de trabajo— sin
duplicar lo que ya vive en una fuente de verdad.

El Change es **exclusivamente documental**: no implementa features, no modifica
`protocol/` ni `runtime/` (el cambio de payload de este Change lo ejecuta el Plan
156 bajo RFC-82, no este Plan), no modifica `tests/` ni `.agents/`, no crea
mecanismos, autoridades ni artefactos de gobernanza nuevos, y no altera
comportamiento funcional. Su efecto sobre código se limita a **dos líneas
aditivas** en `tools/check_plan_citations.py` (`ROOT_DOCS`), que incorporan el
documento nuevo y `docs/placement-contract.md` al conjunto que el verificador de
citas comprueba: es una ampliación de cobertura de verificación, sin cambio de
comportamiento sobre ningún archivo existente. Los paths exactos que este Plan
queda autorizado a modificar son los del `## Declared scope` de su
`## Validation anchor`.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Actualización documental integral post-autonomía y post-integración de clientes: auditar contra el estado real, reconciliar drift/gaps/obsolescencia, y agregar documentación de patrones de comportamiento (estados, orquestación, autonomía, gates, ejecución, clientes, ciclos de trabajo) describiendo el sistema real | humano | pedido del mantenedor (2026-10-11), texto de la consigna |
| `P-2` Confianza de intención | `HIGH` — la consigna nombra el objetivo, el orden de los pasos (reconstruir → auditar → decidir → modificar → reauditar), las restricciones (no inventar información, preservar historia, no tocar `protocol/.agents/`) y el formato del entregable; el mantenedor resolvió además las dos decisiones estructurales por pregunta directa (autorización del Plan; confirmación de `12.0.0`) | agente | respuestas del mantenedor a las dos preguntas de gobernanza de esta sesión |
| `P-3` Conjunto de contexto | `AGENTS.md` raíz; `.agents/AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/{authority,validation-closure,autonomous-orchestration,supervised-autonomous-execution,lifecycle-checkers}.md`; `docs/{VERSIONING,CONVENTIONS,AGENTS,placement-contract,ADOPTION,MIGRATION,source-layout}.md`; `README.md`; `ROADMAP.md`; `CHANGELOG.md`; `docs/plans/INDEX.md`; `docs/plans/149-*`; `docs/plans/154-*`; estado Git real (`git tag`, `git branch`, `dist`) | agente | lecturas de esta sesión |
| `P-4` Derivabilidad | **Sin señal bloqueante** para la reconciliación documental: las dos ambigüedades estructurales (vehículo de autorización; versión publicada vigente) fueron resueltas por decisión explícita del mantenedor. `GAP` declarado y conservado: la bitácora de ejecuciones de CI no es observable desde el repositorio, de modo que la publicación efectiva de `dist` se verifica por su contenido Git (`origin/dist`), no por el log del workflow | agente | este registro; `git show origin/dist:.agents/VERSION` |
| `P-5` `work_type` | `GAP` — el criterio de admisión no está adoptado; no se inventa (precedente Planes 151/154: `P-5 = GAP`) | agente | `docs/plans/151-autonomy-authority-decision-closure.md`; `docs/plans/154-argentos-lifecycle-implementation.md` |
| `P-6` Conocimiento vigente | `docs/VERSIONING.md` (Policy, active); `docs/AGENTS.md` (Policy, active); `docs/placement-contract.md` (Policy, active); `README.md`, `ROADMAP.md`, `CHANGELOG.md` (EntryPoint, active); `.agents/*` (operational, active); `protocol/.agents/*` (Product payload, read-only data) | documento | headers de cada artefacto |
| `P-7` Reglas aplicables | `APPLIES`: RFC-69 (docs-only sin release), RFC-46 (traza histórica), Placement Contract `docs/placement-contract.md:6` (namespace del artefacto nuevo) y `:7` (autorización de escritura), RFC-75 (lifecycle/closure), RFC-56 `NOT_APPLICABLE` (no hay efecto de payload). `NOT_APPLICABLE`: RFC-81 (no se rediseña el lifecycle de adopción; se documenta su resultado) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | `Aprobado para ejecución` sobre este Plan y las rutas de su `## Alcance`; autoridad humana registrada. **No** autoriza tocar `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `dist`, ni artefactos de gobernanza cerrados | humano | autorización de esta sesión (pregunta de gobernanza, respuesta «Sí: crear y ejecutar el Plan 155») |

## Criterio de entrada

- [x] `dev` limpio; HEAD `78ca5127ba45371d77e2e16793e16dd5173a369c`; `git status --porcelain` sin modificaciones rastreadas.
- [x] Estado de release verificado: `dev` = `master` = `origin/dev` = `origin/master` = `78ca512`; tag anotado `12.0.0` sobre ese commit; `origin/dist` publicado desde `78ca512` con `VERSION` = `12.0.0`.
- [x] Autorización explícita del mantenedor para crear y ejecutar este Plan (respuesta directa, 2026-10-11).
- [x] Confirmación del mantenedor de que `12.0.0` es el estado real y de que el drift de `docs/VERSIONING.md` §9 y `ROADMAP.md` debe reconciliarse (respuesta directa, 2026-10-11).
- [x] Checkers documentales en verde antes de la creación (`check_plan_citations`, `check_plan_structure`, `check_version_state`).
- [x] Próximo número de plan libre confirmado: **155** (último registrado: Plan 154).
- [x] Sin contradicción de gobernanza pendiente.

## Alcance

Dentro del Scope, exclusivamente documentación DEV:

| Ruta | Operación |
|---|---|
| `README.md` | reconciliación contra el estado real (autonomía y adopción/lifecycle) |
| `CHANGELOG.md` | reconciliación contra la historia real de Git |
| `ROADMAP.md` | reconciliación del estado del que parte contra la versión publicada real |
| `docs/VERSIONING.md` | reconciliación del snapshot current-state (§9) |
| `docs/behavior-patterns.md` (**nuevo**) | documento de patrones de comportamiento |
| `docs/AGENTS.md` | carta documental: clasificar el artefacto nuevo y `docs/placement-contract.md` |
| `docs/placement-contract.md` | corrección de una cita legacy `.agents/…` a la forma canónica, hallada al incorporar el archivo al conjunto verificado |
| `docs/source-layout.md` | actualización del registro de layout fuente exigida por la corrección de payload de RFC-82 (retiro de la premisa falsa; guarda y citas históricas preservadas) |
| `tools/check_plan_citations.py` | **dos líneas aditivas** en `ROOT_DOCS`: incorporar `docs/behavior-patterns.md` y `docs/placement-contract.md` al conjunto verificado |
| `docs/plans/155-documentation-refresh-behavior-patterns.md` (**este archivo**) | registro del Change |
| `docs/plans/156-payload-layout-documentation-reconciliation.md` (registro) y `docs/plans/INDEX.md` | registro del Change y de su compañero de payload |
| `docs/rfc/82-payload-layout-documentation-reconciliation.md` (registro) y `docs/rfc/INDEX.md` | registro del vehículo RFC-56 del payload |

La autorización para modificar `docs/placement-contract.md`, `docs/source-layout.md`
y `tools/check_plan_citations.py` se amplió **dentro de la misma sesión
autorizada**: los dos primeros son consecuencia obligada de verificar y
reconciliar correctamente (una cita legacy en un documento vivo, y el registro de
layout que la corrección de payload de RFC-82 invalida), y el tercero es el
mecanismo que hace verificable el documento nuevo. Se registra como
`<PLAN-155>:F-2`/`C-2` y no como edición silenciosa.

Fuera del Scope, explícitamente:

- modificar `protocol/`, `protocol/.agents/` o `protocol/_AGENTS.md` **bajo este
  Plan** (el cambio de payload de este Change lo ejecuta el Plan 156 bajo
  RFC-82);
- modificar `runtime/`, `tests/`, `conftest.py` o CI; de `tools/`, **sólo** las
  dos líneas aditivas de `ROOT_DOCS` en `tools/check_plan_citations.py` que el
  `## Alcance` declara, y ninguna otra ruta de `tools/`;
- modificar `.agents/` (capa operacional DEV) — sus policies describen
  correctamente el comportamiento y este Change documenta, no cambia reglas;
- modificar `dist` (rama; se regenera por CI desde `master`);
- reescribir artefactos de gobernanza cerrados (Planes 149–154, RFCs, ADRs),
  documentación histórica o archivada (RFC-46);
- inventar features, capacidades, entradas de changelog o roadmap;
- crear una familia documental o un namespace nuevo;
- promover, taggear, publicar o bumpear `VERSION`.

## Entregables

1. `docs/behavior-patterns.md` — documento DEV nuevo: patrones de comportamiento
   observables (estados y condiciones derivadas, gate pattern, autonomy loop,
   orchestration, human-in-the-loop, failure/recovery, client interaction,
   lifecycle del sistema), con las fuentes de verdad citadas y sin duplicarlas.
2. `README.md` — reconciliado contra el estado real (secciones de autonomía DEV
   y de adopción/lifecycle; sin convertir el README en documentación exhaustiva).
3. `CHANGELOG.md` — reconciliado contra la historia real; sin entradas inventadas.
4. `ROADMAP.md` — reconciliado: el estado del que parte el roadmap deja de
   declarar una versión publicada obsoleta.
5. `docs/VERSIONING.md` — §9 reconciliado con el estado Git verificado.
6. `docs/AGENTS.md` — declaración del artefacto nuevo en la carta documental, si
   la clasificación lo requiere.
7. `docs/plans/INDEX.md` — serie + fila del Plan 155, y reconciliación del
   encabezado descriptivo.
8. `## Validation anchor` y `## Checkpoint / cierre` de este Plan completados al
   validar y cerrar.

## Pasos

1. **Preflight.** Registrar branch, HEAD, worktree, versión, último release,
   tags y commits recientes; verificar que el worktree está limpio. **No**
   modificar ni commitear en esta fase.
2. **Reconstruir el estado real.** Relevar código, tests, configuración, historia
   Git y documentación normativa para autonomía (`.agents/policies/autonomous-orchestration.md`,
   `.agents/policies/supervised-autonomous-execution.md`, `runtime/orchestrator/`,
   sus tests, ADR-19) y para clientes/adopción (`protocol/.agents/harness/lifecycle*`,
   `docs/ADOPTION.md`, `docs/MIGRATION.md`, RFC-81, Plan 154). Distinguir hecho
   verificado, inferencia y `GAP`.
3. **Inventario documental y matriz de auditoría.** Relevar los documentos de la
   raíz, `docs/`, `protocol/`, `.agents/` y `.agents/` operativo; clasificar cada
   uno por propósito, audiencia, naturaleza, lifecycle, fuente de verdad,
   actualidad y cambios necesarios; asignar prioridad `CRITICAL` / `HIGH` /
   `MEDIUM` / `LOW`.
4. **Fuentes de verdad y discrepancias.** Determinar la fuente de verdad por
   área (comportamiento → código + tests; protocolo → payload normativo;
   desarrollo → `AGENTS.md`/`.agents/`; versión → `protocol/.agents/VERSION` +
   `git tag`; releases → Git + `CHANGELOG.md`; roadmap → `ROADMAP.md` validado
   contra el estado real; arquitectura → documentación arquitectónica +
   implementación). Registrar y resolver las discrepancias según la jerarquía
   normativa.
5. **Diagnóstico (primer entregable).** Producir el informe de auditoría con
   *documentation gaps*, *documentation drift*, *documentación obsoleta*,
   *documentación conceptual faltante*, *documentación nueva propuesta* y la
   lista concreta de archivos a modificar con motivo, cambio esperado, evidencia
   y prioridad. Las decisiones estructurales se reportan antes de modificar.
6. **Materializar la reconciliación.** Aplicar los cambios de los entregables
   2–7 con cambios mínimos, sin duplicar contenido, sin inventar información y
   preservando la historia.
7. **Materializar `docs/behavior-patterns.md`.** Resolver su placement
   (`docs/placement-contract.md:6`, familia Normative policy, namespace
   `docs/*.md`), escribirlo contra el comportamiento real reconstruido en el
   paso 2, y declarar su clasificación en `docs/AGENTS.md` si corresponde.
8. **Verificar referencias cruzadas.** Resolver links, paths, anchors y
   referencias a versiones/features; actualizar los índices correspondientes.
   No crear documentación duplicada para resolver un link.
9. **Validar.** Ejecutar la batería canónica de
   `docs/VERSIONING.md:4.1 Batería canónica de verificación` y los gates de
   lifecycle C-1/C-2/C-3; registrar el Validation Anchor.
10. **Reauditar.** Revisión independiente de los documentos modificados contra
    el estado real, con la pregunta «¿un desarrollador nuevo obtendría una imagen
    correcta de qué es ARgentOS, qué puede hacer y cómo funciona?»; corregir los
    problemas objetivos que no exijan decisión arquitectónica.
11. **Cerrar.** Registrar el checkpoint, las dos determinaciones de impacto y la
    condición derivada; actualizar `CHANGELOG.md` `[Unreleased]` con el ítem
    `(plan 155)` y `docs/plans/INDEX.md`.

## Delegación agentiva

No se declara delegación: el Change es documental y su trabajo semántico
—decidir qué dice la documentación y redactarla— es el propio del Change. Las
tareas de recolección de evidencia de esta sesión fueron investigación bajo la
autoridad de este Plan, no delegación del DEV Autonomous Orchestrator (no hubo
`WorkerResult` persistido, ni host, ni verificación de scope por snapshots), y
no producen artefactos de gobernanza.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| Cambio documental DEV | Artefactos del `## Alcance` | Este Plan (`Aprobado para ejecución`, Clase B) | Autorizado para ejecutar |
| Publicación / release | `VERSION`, tag, `dist` | **No autorizado** — fuera del Scope | No ejecutado |
| Cambio de payload | `protocol/.agents/` | **No autorizado** — RFC-56 no aplica (no hay efecto de payload) | No ejecutado |

## Criterios de salida

- [x] El diagnóstico del paso 5 está producido con evidencia y prioridades.
- [x] `README.md` describe correctamente qué es ARgentOS, sus capacidades
      actuales, su autonomía real y la forma de adopción, sin volverse
      documentación exhaustiva.
- [x] `CHANGELOG.md` representa historia real y distingue publicado,
      implementado-no-publicado, en desarrollo y planificado; sin entradas
      inventadas.
- [x] `ROADMAP.md` no declara como publicado un estado superado y sigue siendo un
      mapa operativo, no un changelog.
- [x] `docs/VERSIONING.md` §9 está reconciliado con `git tag` +
      `protocol/.agents/VERSION`, y declara la divergencia local de `dist` si
      corresponde.
- [x] `docs/behavior-patterns.md` existe, describe comportamiento verificable,
      cita sus fuentes de verdad, no duplica documentación existente, no
      documenta chain-of-thought y no presenta hipótesis como hechos.
- [x] Los diagramas Mermaid y ASCII son correctos y cada uno responde una
      pregunta concreta.
- [x] `docs/plans/INDEX.md` registra el Plan 155 (serie + fila) y su encabezado
      no declara un estado obsoleto.
- [x] Sin diff fuera del Scope declarado: `.agents/`, CI, RFCs y ADRs cerrados,
      planes cerrados y `runtime/` intactos; de `tools/`, sólo las dos líneas
      aditivas de `ROOT_DOCS` en `tools/check_plan_citations.py`. (`protocol/` y
      `runtime/toolcalls/canonical.py` fueron modificados por el Plan 156 bajo
      RFC-82, no por este Plan.)
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

Más la verificación factual del Scope (`git status --porcelain`,
`git diff --name-only HEAD`) y la verificación de referencias cruzadas de los
documentos modificados.

## Validation anchor

Registrado al validar el Change (2026-10-11). El alcance validado es el **contenido** del Change; los registros de cierre de esta sección quedan fuera de la identidad declarada por la convención anti-auto-referencia (precedente Planes 96–102, 114/116/134/140–156): el scope declarado se fija **antes** de escribir los registros de cierre y el estado de cierre se declara contra el estado validado.

- **Declared scope:** nueve rutas — `CHANGELOG.md`, `README.md`, `ROADMAP.md`, `docs/VERSIONING.md` (§9), `docs/AGENTS.md`, `docs/placement-contract.md`, `docs/source-layout.md`, `docs/behavior-patterns.md` (nuevo) y `tools/check_plan_citations.py`. Quedan fuera del scope **medido** la governance del Change (los artefactos de Plan 155 y 156, y sus espejos en `docs/plans/INDEX.md` y `docs/rfc/INDEX.md`), de modo que escribir los registros de cierre no altera la identidad certificada.
- **Validation command-set:** la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (siete comandos) + los gates de lifecycle `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + la verificación factual del Scope (`git status --porcelain`, `git diff --name-only HEAD`) y la verificación de referencias cruzadas.
- **Effective inputs (repo content):** el scope declarado; `docs/plans/INDEX.md` y `docs/rfc/INDEX.md` como espejos descriptivos; `docs/VERSIONING.md` (batería, política de changelog, §9); RFC-75 (Change Levels y checkpoints); el corpus completo de `docs/plans/` como población de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada del checker de invariantes; y el estado Git de `dev`.
- **Observed dependencies:** `no instrumentado` (sin tooling de instrumentación); el consumo por comando se observa de la documentación de cada checker.
- **Environmental factors:** OS Windows; Python 3.14; git 2.55.x; sin red; `check_dist_sync.py` **no** aplica (se espera verde sólo en `master`, y este Change no promueve). Advertencia registrada: la **ref local** `dist` está por detrás de `origin/dist`; el payload publicado se verificó contra `origin/dist`.
- **Scoped Content Identity:**
  - **Delta scoped identity (A1; scope S = las nueve rutas del `## Declared scope`, orden lexicográfico; serialización `scoped-v1`):** `4f80d772fcc74007baaf83d8d7c45b42763a1701de77403b4abe111f009fb0e8`.
  - **State identity (A1; estado validado):** T1 = `b865b8a4f247fc4ce14beaba0da34c7af9fa2460` — tree id del índice **staged** al re-ejecutar la validación, resuelto por `tools/scoped_content_identity.py` (`source: staged`).
  - **Límite declarado:** el scope medido excluye la governance del Change; la identidad se computó **antes** de fijar estos registros. El protocolo anti-circularidad es explícito: el `## Declared scope` se cierra primero y la identidad del estado de cierre se declara como el par (delta, state identity) del anchor aplicable. El commit de cierre materializa ese estado sobre el mismo scope, con el delta declarado; el registro del checkpoint no altera el delta del scope medido.
- **Validity / stale:** `revalidada` (**A3** cubre el estado de cierre; A1 y A2 conservados como historia). El estado de cierre se validó con A1, con A2 tras la segunda auditoría independiente y con A3 tras la ronda de cierre posterior a la auditoría de documentación y autonomía; la explicación de por qué cada medición dejó de corresponder al estado de cierre está en las secciones de revalidación.

### Revalidación A2 (mismo contrato, estado nuevo)

Dos hechos hicieron que A1 dejara de corresponder al estado de cierre: (a) la segunda auditoría independiente cambió contenido **dentro** del scope medido (`docs/behavior-patterns.md`, `README.md`, `ROADMAP.md`, `docs/VERSIONING.md`), y (b) el `## Alcance` corregido amplió el scope declarado a once paths, incorporando `docs/plans/INDEX.md` y `docs/rfc/INDEX.md`, que la medición de A1 no cubría. A1 **no se muta**: conserva su significado histórico y sigue arriba.

- **Referencia a A1:** el anchor de arriba; su delta (`4f80d772…`) y su state identity (`b865b8a4…`) quedan como registro histórico de la primera medición.
- **Estado revalidado:** el estado de cierre, declarado por correspondencia GC-1 más abajo.
- **Command-set:** idéntico al de A1 (batería canónica + C-1/C-2/C-3 + verificación factual del Scope y de referencias cruzadas); no cambió.
- **Factores ambientales:** sin cambios respecto de A1.
- **Scoped Content Identity (A2; scope S2 = los once paths del `## Alcance` corregido, orden lexicográfico):**
  - **Delta scoped identity:** `bbbec57c465f9138e5146681458dcf26b141e1823b9bfce0d739cd81efc5060a`.
  - **State identity:** `46f6e76a4836be329edbf840b6c4bb8d30a7be87`.
- **Resultado:** PASS — la batería canónica y los gates se re-ejecutaron sobre el estado corregido y su salida es la registrada en la `## Nota de ejecución`.

### Revalidación A3 (mismo contrato, estado nuevo)

Tercera medición sobre el estado de cierre, exigida por la ronda de cierre posterior a la auditoría de documentación y autonomía: los tres ajustes de esa ronda —`ROADMAP.md`, `CHANGELOG.md` y `docs/behavior-patterns.md`, registrados como `<PLAN-155>:F-4` con su corrección `<PLAN-155>:C-4`— cambian contenido **dentro** del scope medido, de modo que A1 y A2 dejan de corresponder al estado de cierre. A1 y A2 **no se mutan**: conservan su significado histórico.

- **Referencia a A1/A2:** los anchors de arriba; sus deltas (`4f80d772…`, `bbbec57c…`) y sus state identities (`b865b8a4…`, `46f6e76a…`) quedan como registro histórico de sus mediciones.
- **Estado revalidado:** el estado de cierre, declarado por correspondencia GC-1 más abajo.
- **Command-set:** idéntico al de A1/A2 (batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + los gates de lifecycle C-1/C-2/C-3 + la verificación factual del Scope y de referencias cruzadas); no cambió.
- **Factores ambientales:** sin cambios respecto de A1/A2.
- **Scoped Content Identity (A3; scope S3 = las **nueve rutas de contenido** del `## Declared scope` —las que ese mismo registro declara **medidas**, con la governance del Change fuera: el `## Alcance` la excluye explícitamente—, en orden lexicográfico, serialización `scoped-v1`):**
  - **Delta scoped identity:** `2a3f58b0decc8eeb3a16a5bd012236ed99de656c5944cd176d00031e5b8c57b8`.
  - **State identity:** `40ee9cc4b4910fe6f9af48bbce87d7ccbdcf84d9` — tree id del índice **staged** en el momento de medir el delta (`source: staged`).
- **Corrección del literal del delta (post-commit; `<PLAN-155>:F-6`/`C-5`):** la primera medición de A3 dio `c02eb49c…`, valor **válido para el contenido de ese instante** pero medido **antes** de un ajuste de cita posterior dentro del scope medido (`docs/behavior-patterns.md`); el commit de cierre del Change (`docs(dev): close documentation refresh and payload prose reconciliation (plan 155, plan 156, RFC-82)`) materializó por tanto otro contenido y el literal quedó **stale** respecto de él. El valor de arriba es el recomputado sobre el contenido efectivamente commiteado, y es el que el checkpoint certifica. La medición previa se conserva aquí como historia (`c02eb49c…`) y no se borra.
- **Reproducibilidad (mejora registrada en `<PLAN-155>:F-4`; verificada tras la corrección `C-5`):** el **delta** de A3 es reproducible desde el estado commiteado —las nueve rutas de contenido no incluyen los registros de cierre, de modo que resolver la identidad contra el commit de cierre devuelve el mismo valor—. El **state identity** es una fotografía del índice completo al validar: incluye la governance del Change y por eso **no** es reproducible después del commit (límite declarado, idéntico al de A1/A2).
- **Corrección de la declaración de scope medida (F-4):** A2 había identificado el scope medido con los **once** paths del `## Alcance` corregido —incluyendo los espejos `docs/plans/INDEX.md` y `docs/rfc/INDEX.md`—, lo que contradecía el `## Declared scope` de este mismo anchor (que excluye la governance del Change) y hacía la identidad **no reproducible** por auto-referencia: la fila del INDEX contiene el literal de la propia identidad que se mide sobre ese archivo. A3 restablece la coherencia con el `## Declared scope` midiendo las nueve rutas de contenido.
- **Resultado:** PASS — la batería canónica y los gates se re-ejecutaron sobre el estado corregido y su salida es la registrada en la `## Nota de ejecución`.

## Checkpoint / cierre

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio del mantenedor ejecutada en esta ronda de cierre: `docs(dev): close documentation refresh and payload prose reconciliation (plan 155, plan 156, RFC-82)`. Se identifica por su mensaje (convención anti-circularidad: el árbol no embebe su propia identidad). Sin amend, sin merge, sin rebase, sin tag. **Un solo commit para los dos planes del Change, por atomicidad:** los Planes 155 y 156 son un único Change con un único estado validado compartido (los dos anchors se midieron sobre el mismo índice) y se referencian mutuamente —el `## Alcance` de este Plan registra el Plan 156 y RFC-82, y el Plan 156 declara su origen en esta auditoría—, de modo que partirlos en dos commits dejaría cada commit referenciando artefactos todavía no commiteados, es decir, no atómicos. Precedente de la forma: `e35b046` (un commit, tres planes de un Change) y `2267155` (plan 154 + RFC-81).
- **Estado validado (ref al Validation anchor):** A3 (revalidación sobre el estado de cierre; A1 y A2 conservados como historia), delta scoped identity `2a3f58b0…` y state identity `40ee9cc4…`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (**A3**, por correspondencia GC-1 — no por recencia): `2a3f58b0decc8eeb3a16a5bd012236ed99de656c5944cd176d00031e5b8c57b8` / `40ee9cc4b4910fe6f9af48bbce87d7ccbdcf84d9`. Es el estado que el checkpoint **certifica** (delta corregido por `<PLAN-155>:C-5`).
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de cierre incluye la governance del Change, que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7) y el árbol material queda verificable con `git log -1 --format=%T`.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió; verificado por C-2 (sin `ANOMALY`).
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 155 (serie + fila) y el Plan 156; `docs/rfc/INDEX.md` registra RFC-82; `CHANGELOG.md` registra el Change en `[Unreleased]`; `docs/behavior-patterns.md` clasificado como Policy en `docs/AGENTS.md`. Sin `VERSION` bump propio, sin tag, sin push (este Plan es docs-only; el bump PATCH pertenece al Plan 156).
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados y su aspecto: `docs/VERSIONING.md` §9 (el snapshot declaraba el punto de reconciliación `11.6.2`/2026-09-22 como vigente, omitiendo la sucesión `11.7.1` y `12.0.0`, de modo que la versión publicada real no era legible desde el snapshot; evidencia: el documento en el estado validado, contra `git tag` + `protocol/.agents/VERSION` + `origin/dist`); `ROADMAP.md` (la sección `### Estado del que parte este roadmap` declaraba `11.6.2` como versión publicada y omitía el trabajo ya cerrado posterior a su tabla; evidencia: el documento en el estado validado); `README.md` (dos afirmaciones inexactas: la sonda **no** deriva su project root de su propia ubicación, y la superficie del lifecycle omitía `recover` y los exit codes; evidencia: `protocol/.agents/harness/roots.py` y `lifecycle.py`, verificados por lectura directa); `docs/AGENTS.md` (la carta catalogaba como Policy siete documentos y omitía `placement-contract.md` y el artefacto nuevo); `docs/placement-contract.md` (una cita usaba path legacy `.agents/…` en un documento vivo, hallada al sumar el archivo al conjunto verificado); `tools/check_plan_citations.py` (el documento nuevo no estaba cubierto por el verificador de citas, de modo que sus 34 citas canónicas no se verificaban). `docs/behavior-patterns.md` es el artefacto nuevo promovido. `<PLAN-155>:F-1` registra el defecto propio detectado y corregido durante la validación.
- **Roadmap impact:** `NOT_REQUIRED` con razón verificable — el Change **no** altera el mapa operativo del trabajo futuro: no crea, completa, cancela, reclasifica ni re-prioriza trabajo, y no descubre trabajo nuevo. Su efecto sobre `ROADMAP.md` es correctivo (el estado del que parte el mapa dejaba de coincidir con la versión publicada real), que es una reconciliación de exactitud, no un movimiento del mapa. La ejecución del lifecycle de adopción y del Memory System ya estaban cerradas antes de este Change y se registran como estado histórico del que se parte, no como trabajo movido por él. El trabajo que este refresh **sí** descubre —el drift documental verificado fuera de su alcance— se gobierna en el Plan 156 y en el informe de auditoría de la sesión, no en el mapa.
- **Condición derivada:** `Closed` (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-155>:F-1` — estado: `resolved`; observación: el documento nuevo `docs/behavior-patterns.md` citaba la capa operacional DEV con paths **legacy** (`.agents/policies/…`, `.agents/AGENTS.md`), incluía una cita al entry root con una sección inexistente (`Frontera DEV/Protocol`, que no es un heading de `AGENTS.md`), y el propio documento no estaba incluido en el conjunto de fuentes que `tools/check_plan_citations.py` verifica, de modo que sus citas no se validaban; evidencia original: la salida del verificador al incorporar el archivo al conjunto verificado (`1 broken citation`, `18 new legacy references`) y el contenido del archivo antes de la corrección; estado git observado: `dev` en `78ca512`, con los cambios de este Change sin commitear en el índice; provenance original: verificación de referencias cruzadas del propio Change (paso 8 del Plan); resolución: corregidas las 18 rutas a la forma canónica repo-root-relative (`./.agents/…`), corregida la cita al heading real `Hard boundary: DEV vs Protocol` de `./.agents/AGENTS.md`, y añadido `docs/behavior-patterns.md` a `ROOT_DOCS` del verificador para que el documento quede **verificado** y no pueda divergir en silencio; la corrección correspondiente es `<PLAN-155>:C-1`. La resolución es una decisión humana con evidencia (ADR-16 AU-3): el agente registró, propuso y escaló; el mantenedor autorizó el alcance.

- `<PLAN-155>:F-2` — estado: `resolved`; observación: los registros de cierre escritos por primera vez en este Plan introdujeron dos defectos propios: (a) el registro `<PLAN-155>:F-1` no parseaba como registro de lineage porque usaba la etiqueta `observación original` en lugar de `observación` y separaba `resolución` con un punto en vez de un delimitador reconocido, con lo que C-3 lo clasificaba `GAP` (`R-L1-3`/`R-L1-5`); y (b) la `## Nota de ejecución` citaba dos casos de test con la forma de *pytest node id* (nombre de archivo, doble dos puntos, nombre del caso), que `tools/check_plan_citations.py` lee como una cita `path:sección` y reportaba como archivo inexistente; evidencia original: la salida de `tools/check_lifecycle_lineage.py` y `tools/check_plan_citations.py` sobre el primer estado de cierre; estado git observado: `dev` en `78ca512` con el Change en el índice; provenance original: revalidación de la ronda de cierre (pasos 9–10 del Plan); resolución: el registro se reescribió con la gramática de etiquetas y delimitadores del corpus (preservando el contenido inmutable: identidad, observación, evidencia, estado Git y provenance), y las referencias a los casos de test se reescribieron sin la forma de cita; la validación se re-ejecutó sobre el estado corregido. La resolución es una decisión humana con evidencia (ADR-16 AU-3): el agente registró, propuso y escaló.

- `<PLAN-155>:F-3` — estado: `resolved`; observación: la **segunda auditoría independiente** (revisión read-only de los documentos modificados contra el sistema real, pregunta principal «¿un desarrollador nuevo obtendría ahora una imagen correcta?») encontró defectos propios de este refresh no detectados por los checkers: **(C1)** `docs/behavior-patterns.md` §6 listaba «corregir» findings entre lo que el sistema decide solo, cuando la derivación se detiene ante cualquier finding abierto (`runtime/orchestrator/derivation.py`, `STOP_OPEN_FINDINGS`/`STOP_FINDING_REQUIRES_HUMAN`) y el propio código declara que un registro de corrección «cannot yet arise from the loop» — sobrestimación de autonomía y contradicción con §5.2 del mismo documento; **(H1)** la fila del Plan 155 en `docs/plans/INDEX.md` registraba el delta y el state identity **equivocados** (`04cf32e9…`/`2497ae8c…`, valores del primer corte de medición, uno de ellos perteneciente al Plan 156); **(H2/H3)** `ROADMAP.md` y `docs/VERSIONING.md` §9 quedaron contradiciéndose sobre si `dev` lleva payload sin publicar, como consecuencia de que el PATCH `12.0.1` del Plan 156 se introdujo **después** de reconciliar ambos documentos; **(H4)** `## Objetivo`, `## Alcance` y los criterios de salida del Plan 155 afirmaban no tocar `tools/` y listaban ocho paths cuando el `## Declared scope` y el cambio real incluían once; **(H5)** la afirmación «no hay retry» contradecía en silencio a la política citada, que sí enumera retry; más los defectos MEDIUM/LOW del informe (alias `--root` sobreafirmado, `.project/` sin el prefijo `.argentos/`, taxonomía de stops y de denegaciones del hook incompletas, resumen reducido a dos conteos, garantía de scope sobregeneralizada, gates «H00–H15» inexactos, y ausencia de la materialización del Execution Context en el README); evidencia original: el informe de la segunda auditoría con `path:line` por defecto, y su reproducción independiente de `tools/scoped_content_identity.py` sobre el scope declarado del Plan 155 (que devolvió `4f80d772…`, no `04cf32e9…`); estado git observado: `dev` en `78ca512` con el Change completo en el índice; provenance original: segunda auditoría independiente (paso 10 del Plan); resolución: los trece defectos se corrigieron en el lugar que correspondía —`docs/behavior-patterns.md` (C1 con una precisión explícita y su entrada en §5.2; H5 declarando la discrepancia en vez de resolverla por omisión; M2–M6; L1; L3), `docs/plans/INDEX.md` (H1 y L2), `ROADMAP.md` y `docs/VERSIONING.md` §9 (H2/H3), los registros de este Plan (H4) y `README.md` (M1, M7, M8)— y la batería y los gates se **re-ejecutaron** sobre el estado corregido; la corrección correspondiente es `<PLAN-155>:C-3`. Los trece defectos quedaron efectivamente corregidos y verificados por esa re-ejecución.

- `<PLAN-155>:F-4` — estado: `resolved` (vía `<PLAN-155>:C-4`); observación: la ronda de cierre posterior a la auditoría de documentación y autonomía identificó (a) una ambigüedad vigente en documentación de estado actual —`ROADMAP.md` presentaba «Etapa B — Complete ARgentOS Autonomy» como trabajo futuro sin declarar en ninguna parte el estado de la capacidad de autonomía ya implementada, y `CHANGELOG.md` conservaba la formulación «cierre de la feature de autonomía» del ítem del plan 153 (transcripción de la instrucción del acto de autoridad) sin desambiguar entre las decisiones de autoridad del envelope, la capacidad implementada del host y la Etapa B futura—, y (b) que `docs/behavior-patterns.md` §5.2 enumeraba lo que el loop **no** tiene y omitía que tres clases de acción del vocabulario (`SYNC_REPOSITORY_STATE`, `UPDATE_DOCUMENTATION_AUTHORIZED`, `RECOVER_IN_SCOPE`) no son alcanzables desde la derivación; evidencia original: el informe de la auditoría posterior y la verificación directa de `runtime/orchestrator/host.py` (`_AUTONOMY_CLASS_BY_ACTION`, once acciones mapeadas) contra `runtime/orchestrator/autonomy.py` (vocabulario de clases de acción); estado git observado: `dev` en `78ca512`, con el Change completo en el índice y sin commit; provenance original: pedido del mantenedor de cerrar el trabajo documental en `dev` (ronda de cierre, 2026-10-11); resolución: los tres ajustes se materializaron dentro del scope ya autorizado de este Plan (`ROADMAP.md`, `CHANGELOG.md`, `docs/behavior-patterns.md`), **sin** reescribir el ítem histórico del plan 153 (RFC-46: la desambiguación se fija en la entrada viva del Change y en el mapa, no en la traza ajena), y la validación se re-ejecutó como A3. Un tercer defecto, del propio anchor —la declaración de scope medida de A2 incluía los espejos `docs/plans/INDEX.md` y `docs/rfc/INDEX.md`, que contienen el literal de la identidad que se mide sobre ellos, contradiciendo el `## Declared scope` y haciendo la identidad no reproducible por auto-referencia—, se corrige en A3 midiendo las nueve rutas de contenido. La resolución es una decisión humana con evidencia (ADR-16 `AU-3`): el agente registró, propuso y escaló; el mantenedor autorizó el cierre.
- `<PLAN-155>:F-5` — estado: `open` (deferred, owner: mantenedor); observación: la obligación de roadmap diferida por el Plan 151 (`ROADMAP_IMPACT = DEFERRED`) sigue abierta y su registro no nombra por referencia la pending decision que la gobierna, como exige el mínimo de la determinación `DEFERRED` (`.agents/policies/validation-closure.md` §5.2); evidencia original: `docs/plans/151-autonomy-authority-decision-closure.md` (`## Checkpoint / cierre`, determinaciones de impacto, y la pending decision «trigger del objetivo global», `resolución: diferida`, owner mantenedor) y el espejo `docs/plans/INDEX.md`; estado git observado: `dev` en `78ca512`, con el Change completo en el índice y sin commit; provenance original: la auditoría de documentación y autonomía (2026-10-11); impacto: el mapa operativo no representa todavía el trabajo futuro que el Plan 151 difirió, y `### Pending decisions` está fuera del alcance del gate C-3, de modo que ningún checker lo detecta; bloquea: nada del cierre de este Change (el Plan 151 está `Closed` y no se reabre); owner: mantenedor. **No se resuelve aquí**: la ronda de cierre tiene prohibido implementar el mecanismo automático de documentación, la detección de impacto o el resto de los pendientes estructurales de la auditoría.

- `<PLAN-155>:F-6` — estado: `resolved` (vía `<PLAN-155>:C-5`); observación: el literal del delta de A3 se midió **antes** de un ajuste de cita posterior dentro del scope medido (`docs/behavior-patterns.md`: la cita a `./.agents/policies/validation-closure.md` se reescribió de la forma `:5.1 …` partida en dos líneas a la forma `§5.1`), de modo que el commit de cierre materializó contenido distinto del medido: el delta declarado (`c02eb49c…`) quedó **stale** y la afirmación de reproducibilidad del propio registro era **falsa** tal como quedó commiteada. Es el patrón que el anchor declara como límite —medir antes de escribir los registros—, pero aplicado a un cambio de **contenido** y no de registro, que ese límite no cubre; evidencia original: la medición del delta sobre el índice previo al ajuste (`c02eb49c…`) y la re-medición sobre el contenido commiteado (`2a3f58b0…`), con reproducción controlada del contenido previo que devuelve `c02eb49c…` y descarta cualquier otra causa; estado git observado: `dev` en `7e68127` (commit de cierre del Change), worktree limpio; provenance original: verificación post-commit de la reproducibilidad declarada (ronda de cierre, 2026-10-11); resolución: el literal se corrige al valor recomputado sobre el contenido commiteado en el `## Validation anchor` y en el `## Checkpoint / cierre`, la medición previa se conserva como historia sin borrarse, y la batería y los gates se re-ejecutan. La resolución es una decisión humana con evidencia (ADR-16 `AU-3`): el agente registró, propuso y escaló. Precedente de corrección de metadatos de un plan ya cerrado: `<PLAN-140>`, que corrige campos `resolución` y estados de artefactos ajenos por referencia.

### Correcciones

- `<PLAN-155>:C-1` — refs origen: `<PLAN-155>:F-1`; alcance de revalidación: las nueve rutas del `## Declared scope` (el cambio de las citas y del verificador altera contenido en scope medido); evidencia: la corrida de la batería canónica registrada en la `## Nota de ejecución`, con `check_plan_citations` en verde («All citations resolve») sobre el estado corregido. Registro FACTUAL/TRACEABILITY, no fuente normativa.
- `<PLAN-155>:C-2` — refs origen: `<PLAN-155>:F-2`; alcance de revalidación: las nueve rutas del `## Declared scope` (la reescritura del registro de lineage y de la nota de ejecución altera contenido en scope medido); evidencia: `check_lifecycle_lineage` con `GAP=0` para este Plan y `check_plan_citations` en verde sobre el estado corregido, registrados en la `## Nota de ejecución`. Registro FACTUAL/TRACEABILITY, no fuente normativa.
- `<PLAN-155>:C-3` — refs origen: `<PLAN-155>:F-3`; alcance de revalidación: los once paths del `## Alcance` corregido (el cambio afecta `docs/behavior-patterns.md`, `README.md`, `ROADMAP.md`, `docs/VERSIONING.md`, `docs/plans/INDEX.md` y los registros de este Plan, todos en scope medido); evidencia: la corrida final de la batería canónica y de los gates registrada en la `## Nota de ejecución`. Registro FACTUAL/TRACEABILITY, no fuente normativa.
- `<PLAN-155>:C-4` — refs origen: `<PLAN-155>:F-4`; alcance de revalidación: las nueve rutas de contenido del `## Declared scope` (los tres ajustes alteran `ROADMAP.md`, `CHANGELOG.md` y `docs/behavior-patterns.md`, todas en scope medido); evidencia: la corrida de la batería canónica y de los gates C-1/C-2/C-3 registrada en la `## Nota de ejecución`, y la revalidación **A3** del `## Validation anchor` con su identidad de contenido reproducible. Registro FACTUAL/TRACEABILITY, no fuente normativa.
- `<PLAN-155>:C-5` — refs origen: `<PLAN-155>:F-6`; alcance de revalidación: las nueve rutas de contenido del `## Declared scope` (la corrección altera los registros del Plan y su espejo `docs/plans/INDEX.md`, que están **fuera** del scope medido, de modo que la identidad de contenido no cambia y sigue siendo la del commit de cierre); evidencia: la corrida de la batería canónica y de los gates C-1/C-2/C-3 sobre el estado corregido, registrada en la `## Nota de ejecución`, y la verificación de que el delta declarado se reproduce contra el commit de cierre. Registro FACTUAL/TRACEABILITY, no fuente normativa.

### Pending decisions

No se registran pending decisions propias de este Plan: el Change no introduce ninguna decisión bloqueante dentro de su Scope. Los defectos documentales verificados fuera del Scope de este Plan se registran en su propio vehículo de gobernanza (Plan 156 / RFC-82) y en el informe de auditoría de la sesión, no aquí.

## Riesgos

- **Convertir el refresh en una reescritura.** Mitigación: cambios mínimos,
  localizados y aditivos; se preservan estructura, convenciones y terminología.
- **Duplicar documentación.** Mitigación: cada concepto vive en una sola fuente;
  el documento nuevo referencia y no copia.
- **Documentar el sistema esperado en vez del real.** Mitigación: el paso 2
  reconstruye desde código y tests; el paso 10 reaudita contra el estado real.
- **Borrar historia o reescribir artefactos cerrados.** Mitigación: fuera de
  Scope; la traza histórica se preserva (RFC-46).
- **Inventar capacidades o entradas.** Mitigación: prohibido por el `## Alcance`;
  lo no verificable se declara `GAP` o como inferencia.
- **Tocar la frontera DEV/Protocol.** Mitigación: `protocol/` está fuera del
  Scope; el documento nuevo es DEV y no se distribuye.

## Trazabilidad

Pedido del mantenedor (Change «DOCUMENTATION REFRESH — POST AUTONOMY & CLIENT
INTEGRATION», 2026-10-11) → **este Plan** → `docs/behavior-patterns.md`,
`README.md`, `CHANGELOG.md`, `ROADMAP.md`, `docs/VERSIONING.md` §9,
`docs/AGENTS.md`, `docs/plans/INDEX.md`. Estado histórico del que parte: Planes
149–154 (roadmap estratégico, Memory System, cierre de autoridad del modelo de
autonomía, lifecycle de adopción), RFC-81, RFC-75, ADR-15/16/17/18/19.

## Nota de ejecución

**2026-10-11 — Ejecutado en `dev`.** Estado de partida: branch `dev`, HEAD `78ca5127ba45371d77e2e16793e16dd5173a369c`, worktree limpio, `protocol/.agents/VERSION` = `12.0.0`, tag anotado `12.0.0` sobre `78ca512`, `origin/dist` publicado desde `78ca512`.

**Reconstrucción del estado real (pasos 1–2).** Se relevaron la capa DEV (`.agents/`), la capa Protocol (`protocol/.agents/`), `runtime/orchestrator/` y sus suites, `docs/` y el historial Git. El hallazgo estructural del preflight: **`docs/VERSIONING.md` §9 y `ROADMAP.md` declaraban `11.6.2` como estado vigente mientras el estado real era `12.0.0`** (tag anotado sobre `78ca512`, `origin/dist` con `VERSION` = `12.0.0`, `dev` = `master` sin divergencia). Se verificó además que la **ref local** `dist` estaba por detrás de `origin/dist` (11.7.1 vs 12.0.0): la afirmación de publicación del CHANGELOG es correcta, y la ref local no es evidencia válida sin resolver el remoto.

**Diagnóstico (paso 5).** La auditoría se ejecutó en dos rondas de evidencia independientes sobre código y tests, no sobre documentación. Resultado: *drift* en la documentación de versión (§9, ROADMAP) y en el `README.md`; *gap* de documentación conceptual (no existía ningún documento que explicara cómo **trabaja** el sistema: estados, gates, autonomía, orquestación, ciclos); y *drift* sustancial **fuera del alcance inicial** en `docs/ADOPTION.md`, `docs/MIGRATION.md` y prosa del payload. Los hallazgos fuera de alcance se elevaron al mantenedor, que autorizó ampliar el alcance; el cambio de payload recibió su propio vehículo RFC-56 (RFC-82 + Plan 156), de modo que este Plan permanece **docs-only**.

**Qué se materializó.** `docs/behavior-patterns.md` (nuevo, 10 secciones, 4 diagramas — dos Mermaid y dos ASCII —, clasificado Policy en `docs/AGENTS.md`); `README.md` (sección de autonomía DEV nueva, contrato de distribución aclarado, dos afirmaciones inexactas corregidas); `ROADMAP.md` (estado del que parte reconciliado al release real); `docs/VERSIONING.md` §9 (reconciliado al estado verificado, con la advertencia de la ref local); `docs/AGENTS.md` (clasificación del artefacto nuevo y de `placement-contract.md`); `docs/placement-contract.md` (una cita legacy corregida); `tools/check_plan_citations.py` (el documento nuevo y `placement-contract.md` incorporados al conjunto verificado); `CHANGELOG.md` (ítem `[Unreleased]`).

**Verificación realizada.** Batería canónica de `docs/VERSIONING.md:4.1` sobre el estado final: `check_protocol_invariants --payload protocol .` PASS (216 archivos, 10457 referencias verificadas); `check_plan_citations` PASS («All citations resolve»); `check_plan_structure` PASS; `check_taxonomy_coherence` PASS; `check_session_artifacts` PASS; `check_version_state` PASS con los warnings de tags esperados en `dev`; `python -m pytest tests/` → **1267 passed**, sin fallos. Gates de lifecycle: **C-1** `156 plans inspected; EXCLUDED=94, BOUNDARY=0, N/A=0, VALID=60, GAP=2, ANOMALY=0`; **C-2** `EXCLUDED=94, BOUNDARY=0, VALID=59, GAP=3, ANOMALY=0`; **C-3** `EXCLUDED=98, BOUNDARY=0, N/A=28, VALID=30, GAP=0, ANOMALY=0`. `check_dist_sync.py` no se ejecutó: es local-only y se espera verde sólo en `master`, y este Change no promueve.

**Defectos detectados y corregidos durante la verificación (no ocultados).** (1) `<PLAN-155>:F-1`: el documento nuevo citaba paths legacy y una cita no resolvía, y no estaba cubierto por el verificador de citas; corregido y **cerrado el gap de cobertura** añadiéndolo al conjunto verificado. (2) Al incorporar `docs/placement-contract.md` al conjunto verificado apareció una cita legacy preexistente en un documento normativo vivo; corregida. (3) Dos fallos de la suite (`tests/test_check_lifecycle_lineage.py`, caso `test_t27_real_repo_dogfooding`, por `GAP=2`; y `tests/test_repo_containment.py`, caso `test_no_citation_target_depends_on_working_tree`, por targets sin trackear) se diagnosticaron como artefactos de la escritura en curso, no del diseño: el primero por texto placeholder no reconocido como ausencia declarada (corregido con la forma del corpus), el segundo por los archivos nuevos aún sin trackear (resuelto al stagearlos, su estado normal pre-commit). Ambos en verde.

**Segunda auditoría independiente (paso 10).** Revisión read-only de los documentos modificados contra el sistema real, con la pregunta «¿un desarrollador nuevo obtendría ahora una imagen correcta de qué es ARgentOS, qué puede hacer y cómo funciona?». Veredicto: correcto en la separación DEV/Protocol, el patrón de estado derivado, el gate pattern, prevención-vs-detección, los exit codes del lifecycle, los ocho módulos stdlib, la semántica de `.gitignore`/adapter y la afirmación de que **no existe un modelo de clientes**; y **trece defectos** encontrados y corregidos, registrados como `<PLAN-155>:F-3` con su corrección `<PLAN-155>:C-3`. El más grave era de **sobrestimación de autonomía** (se atribuía al loop una corrección autónoma de findings que no está cableada); los demás, de integridad de registro (identidades de anchor equivocadas en el INDEX), de contradicción entre `ROADMAP.md` y `VERSIONING.md` §9 introducida por el PATCH posterior del Plan 156, de fidelidad del `## Alcance` del propio Plan, y de precisión en alias de CLI, layout, taxonomías de stops y denegaciones, y capacidades del runtime.

**Revalidación de la ronda de cierre.** Al escribir los registros de cierre se detectaron dos defectos propios y se registraron como `<PLAN-155>:F-2` con su corrección `<PLAN-155>:C-2`: (a) el registro `<PLAN-155>:F-1` no parseaba como registro de lineage (etiqueta `observación original` en lugar de `observación`, y `resolución` separada por un punto en vez de un delimitador reconocido), de modo que C-3 lo clasificaba `GAP`; y (b) la `## Nota de ejecución` citaba casos de test con la forma de *pytest node id*, que el verificador de citas lee como cita `path:sección`. Ambos se corrigieron y la batería y los gates se **re-ejecutaron sobre el estado resultante**: `check_plan_citations` PASS; `check_plan_structure` PASS; C-1 `EXCLUDED=94, VALID=62, GAP=0, ANOMALY=0`; C-2 `EXCLUDED=94, VALID=61, GAP=1, ANOMALY=0` (el `GAP` es el histórico del Plan 116, conservado, no de este Change); C-3 `EXCLUDED=98, N/A=27, VALID=31, GAP=0, ANOMALY=0`. Los defectos y la revalidación se registran en el Plan, no se ocultan.

**Ronda de cierre posterior (2026-10-11, instrucción del mantenedor).** Cerrado el trabajo en `dev` sin promoción: los tres ajustes que la auditoría de documentación y autonomía dejó como pertenecientes a este cierre se materializaron dentro del scope ya autorizado —`ROADMAP.md` (la Etapa B deja de ser indistinguible de la capacidad de autonomía ya implementada: se declara qué existe hoy, que está publicado en el repositorio y que es DEV-only, y qué pertenece a la Etapa B), `CHANGELOG.md` (desambiguación de la lectura de «cierre de la feature de autonomía», conservando **literal** el ítem histórico del plan 153) y `docs/behavior-patterns.md` §5.2 (tres clases de acción del vocabulario que no son alcanzables desde la derivación)—, y la validación se re-ejecutó como **A3** con su corrección de la declaración de scope medida. Se registran como `<PLAN-155>:F-4`/`C-4`. **No** se implementó nada de los pendientes estructurales de la auditoría (motor de actualización documental, detección de impacto, delta engine de RFC-68, gates de efectos, envelope de autonomía, Etapa B): quedan registrados como `<PLAN-155>:F-5` (deferred, owner mantenedor) y en el informe de cierre, no resueltos. El commit de cierre es **uno** para el Change completo (Planes 155 y 156 + RFC-82), por atomicidad: los dos planes comparten un único estado validado y se referencian mutuamente.

**Corrección post-commit (2026-10-11).** La verificación de reproducibilidad posterior al commit de cierre detectó que el delta de A3 se había medido **antes** de un ajuste de cita en `docs/behavior-patterns.md` (dentro del scope medido), de modo que el literal commiteado quedó `stale` y la afirmación de reproducibilidad era falsa tal como se commiteó. Se registró como `<PLAN-155>:F-6` con su corrección `<PLAN-155>:C-5`: el delta se recomputó sobre el contenido commiteado (`2a3f58b0…`), la medición previa (`c02eb49c…`) se conserva como historia sin borrarse, y la batería y los gates se re-ejecutaron sobre el estado corregido. **Ninguna** ruta de contenido cambió por esta corrección: los nueve paths medidos son los del commit de cierre. El defecto es propio de esta ronda de cierre y se registra, no se oculta.

**Alcance.** `git diff --name-only HEAD` limitado al `## Alcance`; `protocol/` tocado **sólo** por el Plan 156 (RFC-82), no por este Plan. Commit local en `dev`, **sin** push, **sin** tag, **sin** promoción, **sin** `dist`.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1; A3 sobre el estado de cierre).
Committed = TRUE  — commit atómico del Change en `dev`, `docs(dev): close documentation refresh and
                    payload prose reconciliation (plan 155, plan 156, RFC-82)`; se identifica por su
                    mensaje y su SHA se resuelve con `git log` (el artefacto no embebe su identidad).
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump propio, sin tag, sin promoción, sin `dist`.
```

`Closed = TRUE` con `Committed = FALSE` **no es una contradicción**: `Closed` es una condición derivada de `Executed` + governance + checkpoint + consistencia, y puede existir antes del commit; `Committed` es estado del repositorio, no un status de plan. El contrato de los gates lo declara explícitamente (`./.agents/policies/lifecycle-checkers.md:C-2 — Lifecycle checkpoint check`) y `docs/VERSIONING.md:7. Estados de planes y RFCs` fija `Executed ≠ Committed`.
