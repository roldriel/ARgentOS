# Plan 158 — Simplificación radical del ROADMAP

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-11
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L2 (`max(coordination=0, scope=2, architectural impact=1, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, un dominio. *scope*: `ROADMAP.md` más su registro de gobernanza. *architectural impact*: **documental y acotado** — no crea entidad, registry, checker, taxonomía, estado ni autoridad; **reduce** un documento canónico a su responsabilidad única. *release impact*: ninguno (docs-only). *duration/complexity*: acotada a una sesión.
**Depende de:** plan 157 (su resultado es el objeto de este Change)
**Origen:** Directiva del mantenedor (2026-10-11), que califica la implementación del Plan 157 como corrección necesaria: mejoró la estructura formal pero **no logró que el ROADMAP sea inmediatamente legible como hoja de ruta**.

## Objetivo

Reducir `ROADMAP.md` de **367 líneas a menos de 100**, aplicando la estrategia **REDUCE, NOT REORGANIZE**: eliminar del ROADMAP la información que no responde a ninguna de las cinco preguntas de una hoja de ruta, en lugar de reorganizarla otra vez.

El Plan 157 resolvió el problema **estructural** (secciones contradictorias, estados implícitos, historia dentro del área operativa) pero dejó el problema **de fondo**: el documento sigue intentando explicar demasiado y acumula, bajo `NOW / NEXT / LATER`, un capability inventory, un informe de autonomía, un índice documental, un manual de gobernanza, un catálogo de dependencias y un registro de blockers. La reorganización no era suficiente.

```text
ANTES:  ROADMAP grande  →  ROADMAP grande mejor organizado     (Plan 157)
AHORA:  ROADMAP grande  →  selección estratégica  →  ROADMAP pequeño
```

El Change **no implementa ninguna capacidad, no resuelve ninguna decisión pendiente y no toca `protocol/` ni el runtime**.

## Regla de admisibilidad (criterio de cada decisión de este Plan)

Un bloque de contenido permanece en el ROADMAP **sólo si** responde claramente a una de estas preguntas:

```text
A. ¿Cuál es el destino?
B. ¿Dónde estamos?
C. ¿Qué viene ahora?
D. ¿Qué viene después?
E. ¿Qué puede cambiar ese camino?
```

Si no responde ninguna: `REMOVE FROM ROADMAP`. **No se conserva nada por completitud**, y no se crea un documento nuevo para alojar lo eliminado: todo lo eliminado ya tiene artefacto dueño.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Directiva del mantenedor (2026-10-11): simplificación radical del ROADMAP; `origin_type` = direct maintainer action | humano | consigna de intake de esta sesión |
| `P-2` Confianza de intención | `HIGH` — la consigna fija la estrategia (`REDUCE, NOT REORGANIZE`), la estructura objetivo, el límite de iniciativas, el presupuesto visual, los criterios de aceptación y el formato del informe | agente | `INTENT_CONFIDENCE` aplicado sobre la consigna |
| `P-3` Conjunto de contexto | `ROADMAP.md` (estado vigente, 367 líneas); `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)`; `docs/plans/157-canonical-visual-roadmap.md` (resultado del Change anterior); `AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/authority.md`; `docs/VERSIONING.md`; `docs/plans/INDEX.md`; `CHANGELOG.md`; `runtime/README.md`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/placement-contract.md`; `protocol/.agents/VERSION` | agente | lista de `ruta:sección` de este registro |
| `P-4` Derivabilidad | **Derivable.** El estado de Git y de versión es verificable (`75461e8`; `master` = `78ca512`; `protocol/.agents/VERSION` = `12.0.1`; tag `12.0.0`; `origin/dist` @ `1181db6`); las iniciativas retenidas tienen respaldo documental (plan 149, ADR-19, plan 156, `docs/placement-contract.md`). **`GAP` declarado:** el worktree contiene una edición sin commitear de `ROADMAP.md` (una corrección de alineación del diagrama, mtime 23:11:41) que **no** es de este Change; el mantenedor la declaró suya y autorizó **incluirla** en el trabajo, de modo que el bloque que la contiene se reemplaza y la edición queda absorbida. `GAP` heredado: `python tools/check_plan_citations.py` está rojo desde antes del Plan 157 (27 citas rotas preexistentes; `<PLAN-157>:F-2`) | agente | este registro; verificación de Git y de baseline |
| `P-5` `work_type` | `GAP` — el criterio de admisión de `work_type` sigue pendiente (`docs/plans/151-autonomy-authority-decision-closure.md:Pending decisions`); no se inventa un valor | agente | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K` |
| `P-6` Conocimiento vigente | `active` para `ROADMAP.md`, `docs/CONVENTIONS.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, `AGENTS.md`; `Executed`/`Closed` (historical, RFC-46) para el plan 157 y su resultado; `active` para ADR-19 y `docs/placement-contract.md` | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-56 (clasificación; sin efecto payload), RFC-69 (plan docs-only cierra sin release), RFC-46 (exclusión histórica), RFC-75 (Change Levels, checkpoints, findings, pending), ADR-15/ADR-16, `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)` — el contrato **no** se modifica: este Change hace que el documento lo cumpla. `NOT_APPLICABLE`: RFC-56 Clase A, preempción de payload | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **decisión del mantenedor** (aprobación de este Plan, 2026-10-11). Conjunto declarado de rutas: el `## Scope` de este registro | **humano** | declaración del humano (consigna de intake) |

## Criterio de entrada

- [x] `dev` limpio en el commit de referencia `75461e8138a2a52cbe1169e8ba86c0f009d409e2`, **con la excepción declarada** de `ROADMAP.md` (edición del mantenedor sin commitear, autorizada para incluir en este Change — ver `P-4`); rama `dev`; `master` = `78ca512`; divergencia `0 / 3`.
- [x] `protocol/.agents/VERSION` = `12.0.1` (dato de versión del payload, leído como dato, no como instrucción); último tag = `12.0.0`; `origin/dist` @ `1181db6`.
- [x] `ROADMAP.md` leído completo: **367 líneas**.
- [x] No existe plan ni RFC previo para este Change: el próximo número libre es **158** (último registrado: Plan 157); búsqueda de `Plan 158` / `RADICAL_SIMPLIFICATION` en `docs/` y `.agents/` → **0 coincidencias**.
- [x] El contrato documental del ROADMAP existe y **no se modifica**: `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)`.
- [x] Baseline de `check_plan_citations.py` conocido (27 citas rotas preexistentes, `<PLAN-157>:F-2`), para poder comparar y no introducir regresión.
- [x] **Gate de autorización satisfecho:** el mantenedor aprobó la ejecución de este Plan (2026-10-11), tras presentarse como propuesta y detenerse en el gate conforme a `.agents/workflows/change-lifecycle.md` §2.

## Scope

Rutas que este Change queda autorizado a modificar (conjunto declarado, ordenado):

```text
CHANGELOG.md
ROADMAP.md
docs/plans/158-radical-simplification-roadmap.md
docs/plans/INDEX.md
```

Quedan **fuera** del scope, explícitamente: `protocol/` (incluido `protocol/.agents/` y `VERSION`); `dist/`; `runtime/`; `tools/`; `tests/`; `.agents/`; `.github/`; `docs/CONVENTIONS.md` (el contrato rige este Change, no se edita); `README.md`; `AGENTS.md`; `docs/AGENTS.md`; `docs/glossary/**`; `docs/VERSIONING.md`; `docs/placement-contract.md`; `docs/rfc/**`; `docs/adr/**`; `docs/working/**`; y todo plan cerrado (RFC-46).

## Entregables

1. `ROADMAP.md` — **reducido a menos de 100 líneas**, con la estructura objetivo: header de una línea más puntero, `Destination`, `Current position`, `Roadmap` con `NOW`/`NEXT`/`LATER`, `Critical dependencies` (una sola representación) y `Path-changing blockers`.
2. `docs/plans/158-radical-simplification-roadmap.md` — este registro.
3. `docs/plans/INDEX.md` — fila + serie + encabezado de estado.
4. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 158), conforme a RFC-69.

**No se crea ningún documento nuevo.** El plan **no** produce `CAPABILITIES.md`, `AUTONOMY.md`, `DECISIONS.md` ni `ROUTING.md`: todo el contenido eliminado ya tiene artefacto dueño (ver `## Redirección del contenido eliminado`).

## Pasos

1. **Fijar el baseline** de `check_plan_citations.py` sobre el estado de partida (27 citas rotas) para poder acreditar que el Change no introduce regresión.
2. **Reducir el ROADMAP aplicando la regla de admisibilidad** bloque por bloque, según la tabla de `## Redirección del contenido eliminado`. Escribir el documento objetivo con el presupuesto visual de `## Presupuesto visual`.
3. **Reparar únicamente las citas rotas** cuya fuente sea un documento **vivo** y cuyo destino sea una sección eliminada; las citas desde documentos **históricos** no se tocan (RFC-46) y quedan gobernadas por `<PLAN-157>:PC-1`.
4. **Registrar el Change**: este Plan, `docs/plans/INDEX.md` y `CHANGELOG.md`.
5. **Validar**: batería canónica, suite `tests/`, gates C-1/C-2/C-3, y las tres pruebas de comprensión (`30-second`, `scan`, `SRP`).
6. **Cerrar**: Validation Anchor, `## Checkpoint / cierre` con las dos determinaciones de impacto, `## Nota de ejecución` y condición derivada.

## Redirección del contenido eliminado

Todo lo que sale del ROADMAP **ya existe** en un artefacto dueño. No hay pérdida de información y no se crea nada nuevo.

| Contenido del ROADMAP vigente | Veredicto | Destino |
|---|---|---|
| Header «Qué es / Qué NO es» extenso | **RECORTAR** a 2 líneas + puntero | `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)` |
| `## 🎯 Visión / Destino` | **RETENER** (2–4 líneas) | — |
| `## 📍 Posición actual` — tabla de baseline | **RETENER** como 3–5 bullets | — |
| `### Capacidades ya disponibles` (2 tablas + preámbulo) | **ELIMINAR** | `docs/plans/INDEX.md`; `runtime/README.md` |
| `### Estado del que parte este roadmap` | **ELIMINAR** | `CHANGELOG.md`; `docs/plans/INDEX.md` |
| `## 🚦 Roadmap at a Glance` — 3 cards ASCII con 6 campos | **REEMPLAZAR** por listas de una línea por iniciativa, con dominio y prioridad compactos | — |
| «Fronteras candidatas de la Etapa B» (13 ítems) | **ELIMINAR** | `docs/plans/149-argentos-capability-and-autonomy-roadmap.md` |
| `## 🔗 Dependencias estratégicas` | **RETENER** (un solo grafo Mermaid, 3–8 aristas) | — |
| `## 🚧 Blockers` (6) + `### ⏸️ Pendientes` (4) | **REDUCIR** a 3–6 estratégicos | el artefacto dueño de cada decisión (PC-1) |
| `## 🧭 Autonomy — mapa del caso` (3 tablas + 2 grafos + 2 avisos) | **ELIMINAR**; la autonomía queda como **una iniciativa** | `docs/adr/19-autonomy-envelope-authority.md`; `runtime/README.md`; `.agents/policies/supervised-autonomous-execution.md` |
| `## 🗂️ Dónde consultar qué` (11 filas) | **ELIMINAR** | `docs/AGENTS.md:Folder → class map`; los INDEX de `docs/` |
| `## 📐 Qué es y qué NO es este documento` + reglas de admisión y frescura | **ELIMINAR del ROADMAP** | `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)` |
| Edición sin commitear del mantenedor (alineación del diagrama) | **ABSORBIDA** | el bloque que la contenía se reemplaza |

## Presupuesto visual

```text
IDEAL      < 100 líneas   ← objetivo de este Plan
ACCEPTABLE < 150 líneas
WARNING    ≥ 150 líneas
FAIL       ≥ 200 líneas
```

El objetivo es `< 100`. **No se alcanza por compresión artificial de texto**: se alcanza eliminando contenido no esencial. Si el contenido estratégico legítimo exigiera más espacio, debe justificarse explícitamente en este registro.

## Criterios de salida

**Estructural**

- [ ] `ROADMAP.md` tiene una única responsabilidad: comunicar dirección estratégica y secuencia.
- [ ] Existe una secuencia `NOW → NEXT → LATER` inequívoca.
- [ ] `Destination` es breve (2–4 líneas) y `Current position` es breve (3–5 bullets).
- [ ] No existe capability inventory, autonomy report detallado, documentation index, manual de gobernanza, release history, decision register ni task/checklist tracker.

**Contenido**

- [ ] `NOW` contiene sólo iniciativas actuales (1–3); `NEXT` sólo posteriores (1–4); `LATER` sólo dirección futura (1–5).
- [ ] Cada iniciativa es estratégica y se expresa como `[qué] — [por qué / hacia dónde]`, no como tarea de implementación.
- [ ] Dependencias (3–8) y blockers (3–6) son estratégicos; existe **una sola** representación de dependencias.
- [ ] No hay información duplicada.
- [ ] Los estados son verdaderos y verificables; no se inventaron prioridades, fechas ni trabajo futuro.

**Visual**

- [ ] `Destination` se identifica inmediatamente; `NOW`/`NEXT`/`LATER` dominan visualmente.
- [ ] El documento no parece spreadsheet, audit report, documentation index ni technical design.

**Tamaño**

- [ ] `< 100 líneas` (objetivo); si superara 150, existiría justificación concreta en este registro.

**Comprensión**

- [ ] `30_SECOND_TEST = PASS`; `SCAN_TEST = PASS`; `SRP_TEST = PASS`.

**Repositorio**

- [ ] `check_plan_citations.py` no aumenta su conteo de citas rotas respecto del baseline (27).
- [ ] `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `docs/CONVENTIONS.md` y los planes cerrados: **0 diff**.
- [ ] Batería canónica, suite `tests/` y gates C-1/C-2/C-3 registrados; determinaciones de impacto declaradas.

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

**Pruebas de comprensión (criterio principal de aceptación).**

```text
30-SECOND TEST — lectura deliberadamente superficial:
  1. título · 2. Destination · 3. Current position
  4. NOW / NEXT / LATER · 5. dependencies / blockers
  Sin reconstruir significado desde secciones eliminadas.
  Debe responder: destino · dónde estamos · qué viene ahora ·
  qué viene después · hay bloqueo importante.

SCAN TEST
  A. Jerarquía visual: destacan Destination, NOW, NEXT, LATER
  B. No wall of text
  C. No registry smell (spreadsheet / inventory / tracker / audit)
  D. No portal smell (índice de documentación)

SRP TEST
  Una sola responsabilidad; ninguna otra identificable en el documento.
```

## Riesgos

| Riesgo | Severidad | Mitigación |
|---|---|---|
| Perder información al eliminar bloques | media | Cada bloque eliminado tiene destino declarado en `## Redirección del contenido eliminado`; **0 documentos nuevos** y **0 información sin dueño** |
| Romper citas de documentos vivos | alta | Baseline medido antes de editar; reparación sólo de fuentes vivas; las históricas quedan por RFC-46 y bajo `<PLAN-157>:PC-1` |
| Recaer en «reorganizar» en lugar de «reducir» | alta | Regla de admisibilidad aplicada bloque por bloque; presupuesto visual `< 100` líneas como control de regresión |
| Crear un monolito alternativo | alta | Prohibido por el Plan: no se crean `CAPABILITIES.md`, `AUTONOMY.md`, `DECISIONS.md` ni `ROUTING.md` |
| Perder precisión sobre autonomía | alta | La autonomía queda como iniciativa con puntero a ADR-19 y `runtime/README.md`; no se afirma que Complete Autonomy esté completa |
| Inventar prioridad, fecha o trabajo futuro | media | Sólo se retiene lo sustentado por documentación del repositorio; la ambigüedad se marca, no se resuelve inventando |
| Confundir `protocol/.agents/` con la capa DEV | media | `protocol/` es payload de sólo lectura; el alcance es documentación DEV |

## Trazabilidad

Plan 157 (contrato canónico y reestructuración del ROADMAP) → su resultado es **insuficiente como hoja de ruta** → directiva del mantenedor (2026-10-11) → **este Plan** → `ROADMAP.md` reducido.

Continuidad de gobernanza no reabierta: `<PLAN-157>:F-2` y `<PLAN-157>:PC-1` (citas rotas preexistentes), planes 132/133/149/155/156, RFC-75, ADR-15/16.

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** las tres rutas que la identidad de contenido mide — `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/INDEX.md`. Queda fuera del scope **medido** la governance del propio Change (este artefacto), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 114/116/134/140–149/157). El `## Scope` autorizado tiene cuatro rutas: las tres medidas más `docs/plans/158-radical-simplification-roadmap.md`.
- **Validation command-set:** los siete comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + las tres pruebas de comprensión (`30-second`, `scan`, `SRP`) + la verificación factual de scope y de fuente de verdad.
- **Effective inputs (repo content):** el scope declarado; `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)` (contrato que este Change **no** modifica); `docs/plans/157-canonical-visual-roadmap.md`; `docs/VERSIONING.md` (batería, changelog, snapshot); `docs/plans/156-payload-layout-documentation-reconciliation.md`; `docs/plans/149-argentos-capability-and-autonomy-roadmap.md`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/plans/151-autonomy-authority-decision-closure.md`; `docs/plans/152-authority-decisions-gov-1-10.md`; `docs/plans/125-repository-architecture-decisions.md`; `docs/placement-contract.md`; el corpus completo de `docs/plans/` y `docs/rfc/` como población de `check_plan_citations` y de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada de `check_protocol_invariants`; y el estado Git de `dev`.
- **Observed dependencies:** stdlib únicamente; el CLI `git` para las identidades de contenido, la resolución de objetos y la verificación de fuente de verdad. Sin red.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.x; git 2.55.0.windows.5; repositorio bajo OneDrive. **Clase ambiental declarada:** `check_dist_sync.py` **no** aplica (local-only, verde sólo en `master`; este Change no promueve). `check_plan_citations.py` sigue rojo por las citas preexistentes de documentos históricos (`<PLAN-157>:F-2`), pero su conteo **baja** de 27 a 26. Estado de partida declarado: el worktree contenía una edición sin commitear de `ROADMAP.md` (del mantenedor, autorizada para incluir), absorbida por el reemplazo del bloque que la contenía.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `bfa5d0ea87fed3a4c98aab52ba5e6f5811f6641a` — tree id del índice staged del scope medido (`tools/scoped_content_identity.py`, source `staged`).
  - **Delta scoped identity (scope S = las tres rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `cae1a902adb6682226ca8b41bd8b14e038e6a4822d5dd1337baa677396b72357`.
  - **Límite declarado:** el scope medido excluye la governance del Change (este artefacto); la identidad se computó antes de escribir los registros de cierre.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/INDEX.md`
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): **PASS** (exit 0, 216 files / 10457 references); verification-02 (`check_plan_citations`): **FAIL preexistente** (exit 1, **27** citas rotas, idénticas al baseline de **27** — cero introducidas; en la medición intermedia, antes de escribirse este registro, el conteo bajó a 26 al conservarse `### Estado del que parte este roadmap`); verification-03 (`check_plan_structure`): **PASS**; verification-04 (`check_taxonomy_coherence`): **PASS**; verification-05 (`check_session_artifacts`): **PASS**; verification-06 (`check_version_state`): **PASS**; verification-07 (`python -m pytest tests/`): **PASS**, **1267 passed** en 387,03 s; verification-08 (C-1): `ANOMALY=0 GAP=0 VALID=64`; verification-09 (C-2): `ANOMALY=0 VALID=63 GAP=1` (histórico del Plan 116, intacto); verification-10 (C-3): `ANOMALY=0 GAP=0`, con este artefacto `VALID`. Verificación factual: `git diff --cached --name-only` ⊆ `## Scope`; verdad de fuente verificada contra Git (tag `12.0.0` → `78ca512` = `master`; `origin/dist` = `1181db6` con `VERSION` `12.0.0`; `12.0.1` **sin tag**); todos los artefactos citados existen y sus secciones resuelven. Pruebas de comprensión: `30_SECOND_TEST = PASS`, `SCAN_TEST = PASS`, `SRP_TEST = PASS` (ver `## Nota de ejecución`).

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio del mantenedor: `docs(roadmap): reduce the roadmap to its strategic path (plan 158)`. Se identifica por su mensaje (convención anti-circularidad). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `bfa5d0ea87fed3a4c98aab52ba5e6f5811f6641a`, delta scoped identity `cae1a902adb6682226ca8b41bd8b14e038e6a4822d5dd1337baa677396b72357`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `cae1a902adb6682226ca8b41bd8b14e038e6a4822d5dd1337baa677396b72357` / `bfa5d0ea87fed3a4c98aab52ba5e6f5811f6641a`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit incluye la governance del Change (este artefacto), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); C-2 clasificó el corpus sin `ANOMALY` (el `GAP=1` es el histórico del Plan 116).
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 158 (serie Octogésima séptima + fila + encabezado); `CHANGELOG.md` `[Unreleased]` registra el par (plan 158); `ROADMAP.md` reducido de 367 a 99 líneas; `docs/CONVENTIONS.md` **no** se modifica (el contrato rige, no se edita); finding `<PLAN-158>:F-1` registrado; `**Status:** Executed`.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados y su aspecto: `ROADMAP.md` (aspecto: acumulaba un capability inventory, un informe de autonomía, un índice documental y un manual de gobernanza, de modo que no se leía como hoja de ruta; actualización: reducción a 99 líneas con `Destino`, `Posición actual`, `NOW`/`NEXT`/`LATER`, un grafo de dependencias y una tabla de bloqueos estratégicos; evidencia: el documento en el estado validado, con las tres pruebas de comprensión en PASS y el conteo de citas rotas sin aumento). `docs/plans/INDEX.md` (fila, serie y encabezado) y `CHANGELOG.md` (ítem `[Unreleased]`) por el registro del Change. `docs/CONVENTIONS.md` **examinado y sin cambio**: el contrato canónico del ROADMAP sigue vigente y este Change hace que el documento lo cumpla (razón verificable, no omisión). `AGENTS.md`, `README.md`, `docs/AGENTS.md` y `docs/glossary/**` **no** se tocan: no describen secciones que este Change elimine. No se actualiza ningún documento histórico (RFC-46).
- **Roadmap impact:** `REQUIRED` — el propio Change **es** la reconciliación del mapa estratégico: reduce la representación del trabajo futuro a su camino, sin crear, cancelar ni re-priorizar trabajo. El artefacto que lo posee es `ROADMAP.md`, con el registro descriptivo en `docs/plans/INDEX.md`. **No** crea trabajo ejecutable: ninguna iniciativa queda autorizada por este documento.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-158>:F-1` — estado: `resolved`; severidad: `low`; observación: el worktree contenía una edición **sin commitear** de `ROADMAP.md` (corrección de alineación del diagrama: `───▶ │` → `───▶│`), posterior al commit `75461e8` y **ajena** a este Change; evidencia original: `git status --porcelain=v1` en el preflight y `git diff HEAD -- ROADMAP.md` (1 inserción, 1 borrado; mtime 23:11:41); estado Git observado: `dev` @ `75461e8138a2a52cbe1169e8ba86c0f009d409e2`, worktree con `ROADMAP.md` modificado sin commitear; provenance original: verificación de preflight de este Plan; resolución: **decisión humana del mantenedor** (2026-10-11) de considerarla propia y autorizar su inclusión en este Change; el bloque que la contenía (el diagrama ASCII de tres cards) fue reemplazado por el ROADMAP reducido, de modo que la edición quedó **absorbida** y no se perdió ningún cambio del mantenedor.
- `<PLAN-158>:F-2` — estado: `open`; severidad: `low`; observación: la reducción **repara** una cita y podría haber roto otra: al eliminar secciones del ROADMAP, las citas de fuentes vivas a esas secciones dejarían de resolver; evidencia original: baseline medido de `check_plan_citations` (27) contra el estado de cierre (27, con la cita del propio Plan ya corregida); estado Git observado: `dev` @ `75461e8138a2a52cbe1169e8ba86c0f009d409e2`; provenance original: verificación de este Plan; resolución: **no requiere corrección adicional** — se conservó `### Estado del que parte este roadmap` precisamente porque su destino (`CHANGELOG.md`) es un documento vivo, y la referencia a `docs/placement-contract.md:Enforcement deferred` se escribe fuera de celda de tabla, de modo que no se introdujo ninguna cita rota nueva. Las citas de documentos **históricos** a secciones removidas siguen sin repararse (RFC-46) y quedan gobernadas por `<PLAN-157>:PC-1`.

### Correcciones

No findings detected / N/A — no hubo corrección posterior a la verificación; el Change se materializó en una sola pasada.

### Pending decisions

No se registran pending decisions nuevas. La continuidad de las citas rotas preexistentes vive en `<PLAN-157>:PC-1` (owner: mantenedor) y no se reabre aquí.

## Nota de ejecución

*2026-10-11. Ejecutado en `dev` @ `75461e8138a2a52cbe1169e8ba86c0f009d409e2`, con la edición declarada del mantenedor presente en el worktree (`<PLAN-158>:F-1`).*

**Gate de autorización.** La consigna de intake se presentó conforme a su §0: no existía artefacto de Plan 158 ni mención alguna en el corpus, de modo que se trataba de una **propuesta**. Se verificó el estado de Git, se presentó el plan y se **detuvo** la ejecución sin modificar archivos. El mantenedor autorizó la ejecución y declaró propia la edición sin commitear de `ROADMAP.md`.

**Verificación realizada.** Batería canónica: `check_protocol_invariants` PASS (216 archivos, 10457 referencias); `check_plan_structure` PASS; `check_taxonomy_coherence` PASS; `check_session_artifacts` PASS; `check_version_state` PASS; `python -m pytest tests/` → **1267 passed** (387,03 s). Gates: C-1 `ANOMALY=0 / GAP=0 / VALID=64`, C-2 `ANOMALY=0 / VALID=63 / GAP=1` (histórico del Plan 116), C-3 `ANOMALY=0 / GAP=0` con este artefacto `VALID`. `check_plan_citations`: **27** citas rotas, idénticas al baseline de **27** — cero introducidas; la reducción del ROADMAP bajó el conteo a 26 en la medición intermedia y este registro añadió una referencia propia que se corrigió antes del cierre, de modo que el resultado neto es neutro.

**Métricas de reducción.**

```text
ROADMAP_LINES_BEFORE = 367
ROADMAP_LINES_AFTER  =  99          (presupuesto IDEAL <100; no se comprimió texto)

INITIATIVES_NOW   = 1   (promover 12.0.1)
INITIATIVES_NEXT  = 1   (Etapa A: retrospectiva de capacidades y garantías)
INITIATIVES_LATER = 3   (envelope de autonomía · Complete Autonomy/Etapa B · Etapa C)

DEPENDENCIES        = 4 aristas en un único grafo Mermaid (una sola representación)
STRATEGIC_BLOCKERS  = 6

CAPABILITY_INVENTORY_REMOVED  = YES
AUTONOMY_REPORT_REMOVED       = YES
DOCUMENTATION_INDEX_REMOVED   = YES
GOVERNANCE_CONTRACT_REMOVED   = YES (del ROADMAP; permanece en docs/CONVENTIONS.md)
HISTORY_REMOVED               = YES

30_SECOND_TEST = PASS
SCAN_TEST      = PASS
SRP_TEST       = PASS
```

**Qué se eliminó.** Los dos inventarios de capacidades (DEV y PROTOCOL); `## 🧭 Autonomy — mapa del caso` completo (tres tablas, dos grafos y dos avisos); `## 🗂️ Dónde consultar qué` (once filas); `## 📐 Qué es y qué NO es este documento` con sus reglas de admisión y frescura; la lista de trece fronteras candidatas de la Etapa B; la tabla de baseline de cinco filas; y las tres cards ASCII de seis campos.

**Qué se retuvo.** El destino en tres párrafos breves; la posición actual en cuatro bullets más la constancia de que las capacidades existentes no se reabren; las cinco iniciativas repartidas en `NOW`/`NEXT`/`LATER` con dominio y prioridad compactos (`[DOMINIO] PRIORIDAD — qué y por qué`); un único grafo Mermaid con cuatro aristas; y seis bloqueos estratégicos.

**A qué se redirigió.** Sin crear ningún documento nuevo: el contrato y las reglas de admisión y frescura a `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)`; el detalle de la autonomía a `docs/adr/19-autonomy-envelope-authority.md`, `runtime/README.md` y `.agents/policies/supervised-autonomous-execution.md`; el estado de capacidades y planes a `docs/plans/INDEX.md` y `runtime/README.md`; el historial y las releases a `CHANGELOG.md`; la navegación documental a `docs/AGENTS.md:Folder → class map` y a los INDEX de `docs/`; y el detalle de cada decisión al artefacto que la posee (PC-1). No se crearon `CAPABILITIES.md`, `AUTONOMY.md`, `DECISIONS.md` ni `ROUTING.md`.

**Alcance.** Cuatro rutas: `ROADMAP.md` (reducido), `docs/plans/158-radical-simplification-roadmap.md` (este registro), `docs/plans/INDEX.md` y `CHANGELOG.md`. Ningún artefacto movido, renombrado ni eliminado; sin carpetas nuevas; sin documentos nuevos.

**No realizado (por diseño).** No se implementó ninguna capacidad; no se completó Autonomy ni el envelope; no se resolvió ninguna decisión pendiente; no se modificó `docs/CONVENTIONS.md`; no se creó ningún registro ni índice nuevo; `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/`, `README.md`, `AGENTS.md`, `docs/AGENTS.md`, `docs/glossary/**`, `docs/VERSIONING.md`, `docs/placement-contract.md`, RFCs, ADRs y planes cerrados con **0 diff**; sin `VERSION` bump, sin tag, sin promoción.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1).
Committed = TRUE  — commit atómico en `dev`, identificado por su mensaje.
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump, sin tag, sin promoción a `master`, sin `dist`.
```

