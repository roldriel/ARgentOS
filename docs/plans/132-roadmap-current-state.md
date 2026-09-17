# Plan 132 — Actualización del Roadmap al estado real

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=0, architectural impact=1, release impact=0, duration/complexity=0)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, sesión única, un dominio. *scope*: un dominio DEV (documentación de estado actual en la raíz + gobernanza documental del propio plan). *architectural impact*: **acotado y documental** — no crea entidad, registry, taxonomía, autoridad, lifecycle, estado, checker ni tarea de implementación; **reclasifica** información de estado que hoy se presenta como trabajo pendiente cuando no lo es, que es una decisión de representación, no de arquitectura. *release impact*: ninguno (docs-only, sin `VERSION`, sin tag). *duration/complexity*: trivial.
**Depende de:** — (no depende de un plan previo). El baseline declarado en la consigna no se pudo confirmar: ver `<PLAN-132>:F-1`.
**Origen:** Directiva del mantenedor que autoriza corregir `ROADMAP.md` para que represente el trabajo **realmente** pendiente, el que requiere autoridad y el que es sólo candidato.

## Objetivo

Devolver a `ROADMAP.md` su función de **mapa operativo actual**: qué se trabaja ahora, qué sigue, qué problemas reales requieren autorización y qué es sólo candidato futuro. Hoy el documento presenta una tabla histórica B-1…B-8 —cuyos problemas originales **ya están resueltos**— con la apariencia de backlog activo, de modo que un lector no puede distinguir trabajo pendiente de historia cerrada sin consultar ocho planes.

El Change es **documental y deliberadamente pequeño**. No implementa ninguna de las tareas que lista, no reabre `B-1`/`B-2`/`B-3`/`B-5`/`B-6`, no convierte capacidades existentes en backlog, no inventa tareas nuevas y no toca `protocol/`, `runtime/`, `tools/`, `tests/` ni `.agents/`. La trazabilidad histórica permanece íntegra en `docs/plans/INDEX.md`, los planes y las RFCs; lo que desaparece es su **duplicación como si fuera trabajo abierto**.

Propiedad que este Change debe garantizar:

```text
histórico resuelto      ≠  trabajo derivado
trabajo derivado        ≠  pendiente arquitectónico
pendiente arquitectónico ≠  candidato futuro
```

## Criterio de entrada

- [x] `dev` limpio en `65a1113308022b89c29be9f728d670957c35838e` (verificado con `git status --porcelain=v1` y `git rev-parse HEAD`); rama `dev`.
- [x] `ROADMAP.md` leído: 44 líneas, con la tabla `## Backlog resuelto` de B-1…B-8 como contenido principal.
- [x] `docs/plans/INDEX.md` confirmado como fuente descriptiva de estado de los planes (§Backlog evidenciado - plan 19 y encabezado de estado).
- [x] Plan 131 presente y `Executed` con condición derivada `Closed` (`docs/plans/131-placement-contract-mechanical-implementation.md`).
- [ ] **No satisfecho — Plan 132 y Plan 133 no existen**: el plan 132 es este Change y el Plan 133, designado como evidencia principal en la consigna, no existe en el repositorio ni en la historia de git. Registrado como `<PLAN-132>:F-1`; la clasificación `B-1`…`B-8` se re-verificó de forma independiente contra el repositorio, y el mantenedor autorizó ejecutar este Change con el próximo número libre.

## Entregables

1. `ROADMAP.md` — reestructurado como mapa operativo actual (trabajo activo, pendientes que requieren autoridad, candidatos futuros), sin la tabla B-1…B-8 como backlog y sin `B-5`/`B-6` como trabajo pendiente.
2. `docs/plans/132-roadmap-current-state.md` (**este archivo**) — registro del Change.
3. `docs/plans/INDEX.md` — registro del Plan 132 (fila + serie) y encabezado de estado.
4. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 132), conforme a la regla de changelog para planes docs-only.

## Pasos

1. Verificar baseline (`dev`, HEAD, árbol limpio), confirmar el contenido actual de `ROADMAP.md` y `docs/plans/INDEX.md` como fuentes, y confirmar la disponibilidad de la evidencia declarada.
2. Verificar, ítem por ítem, el estado real de `B-1`…`B-8` y de sus residuos contra el repositorio: `docs/plans/INDEX.md` §Backlog evidenciado - plan 19, el anexo A de bitácora de fricciones, el contrato D01 y `protocol/.agents/contracts/METRICS.md`.
3. Reclasificar cada `B-x` en una de las cuatro categorías —histórico resuelto, trabajo derivado, pendiente arquitectónico, candidato futuro— sin recalificar prioridades históricas sin evidencia.
4. Reescribir `ROADMAP.md` con la estructura operativa, citando el origen real de cada entrada y marcando explícitamente lo que requiere autorización de payload.
5. Registrar el Plan 132 en `docs/plans/INDEX.md` (fila + serie + encabezado) y el ítem del par en `CHANGELOG.md`.
6. Determinar el impacto documental conforme al mecanismo vigente y registrarlo en el cierre.
7. Ejecutar checkers documentales, gates de lifecycle y la verificación de este Change; registrar el Validation Anchor, el checkpoint y la nota de ejecución.

## Criterios de salida

- [ ] `ROADMAP.md` ya no contiene la tabla B-1…B-8 como backlog ni presenta `B-5` o `B-6` como trabajo pendiente.
- [ ] `B-1` y `B-2` figuran como **trabajo derivado nuevo** (dogfood próximo / siguiente), nunca como ítems reabiertos.
- [ ] `B-3` figura como **candidato futuro**, no como backlog reabierto.
- [ ] `B-4`, `B-7` y `B-8` figuran como **pendientes reales que requieren autorización de payload** (RFC-56), y `B-7` no se confunde con la corrección de trazabilidad de `docs/plans/INDEX.md`.
- [ ] Un lector de `ROADMAP.md` responde sin abrir planes históricos: qué se trabaja ahora, qué sigue, qué requiere RFC/autoridad, qué es candidato y qué ya está cerrado.
- [ ] Sin contradicciones con `docs/plans/INDEX.md`: `docs/plans/INDEX.md` sigue siendo la fuente descriptiva de estado y `ROADMAP.md` no duplica estados de planes.
- [ ] `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, los RFCs, los ADRs, los planes históricos, el Placement Contract y CI **sin cambios**.
- [ ] Ninguna tarea nueva agregada sin evidencia concreta en el repositorio.
- [ ] Batería canónica y gates de lifecycle registrados.

## Verificación

```text
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

La pierna `python -m pytest tests/` **no** se ejecuta como gate de este Change: es puramente documental, no toca `tools/` ni `runtime/`, y el entorno reproduce el GAP ambiental de temporales ya declarado por los Planes 121–131. Se sustituye por las comprobaciones factuales del §Verificación del cierre (citaciones de `ROADMAP.md` resueltas, ausencia de afirmaciones retiradas, 0 diff fuera de scope).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** la actualización documental del Roadmap y su registro: `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/132-roadmap-current-state.md`, `docs/plans/INDEX.md`. Total 4 paths.
- **Validation command-set:** `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; y la verificación factual de `ROADMAP.md` (citaciones resueltas, ausencia de las afirmaciones retiradas, 0 diff fuera de scope).
- **Effective inputs (repo content):** el scope declarado (4 paths) más las fuentes de evidencia consumidas para reclasificar `B-1`…`B-8` —`docs/plans/INDEX.md`, `docs/plans/19-anexo-a-bitacora-fricciones.md`, `docs/plans/33-ears-criteria-canonical-form.md`, `docs/plans/44-unattended-clarification.md`, `docs/plans/50-discovery-kb-freshness.md`, `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md` y `protocol/.agents/contracts/METRICS.md`— y el corpus que consumen los checkers canónicos (`docs/plans/`, `docs/rfc/`, `docs/adr/`, `tools/`, `protocol/.agents/`).
- **Observed dependencies:** `git` (identidad de contenido y estado); `python` (intérprete de los checkers). El resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.x; git 2.55.0.windows.5; sin red. **Clase ambiental declarada (GAP, no defecto del Change):** la pierna `python -m pytest tests/` **no** se ejecutó como gate de este Change: el Change es puramente documental, no toca `tools/` ni `runtime/`, y el entorno reproduce el GAP de temporales (`PermissionError [WinError 5]`) ya declarado por los Planes 121–131. No se reabre C-2/CI ni se modifica CI.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** ad5fe5e6e9b940e4e95a4d061d085260177cd0cd (tree id del índice staged del scope declarado).
  - **Delta scoped identity (scope S = los 4 paths del cambio, ordenados; serialización `scoped-v1`):** ebe7e574bb867d62a38b52bec6386622050c2161601d4299f764dbc19064e556.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/132-roadmap-current-state.md`, `docs/plans/INDEX.md`
- **Validity / stale:** vigente

*Resultado real de la ejecución:* verification-01 (`check_plan_citations`): PASS (exit 0, "All citations resolve"); verification-02 (`check_plan_structure`): PASS (exit 0, "All numbered documents conform"); verification-03 (`check_protocol_invariants --payload protocol .`): PASS (exit 0, 215 files / 10256 references); verification-04 (`check_taxonomy_coherence`): PASS (exit 0); verification-05 (`check_session_artifacts`): PASS (exit 0); verification-06 (`check_version_state`): PASS (exit 0, con los warnings de tags esperados en `dev`); verification-07 (C-1 `check_lifecycle_anchor`): `VALID`; verification-08 (C-2 `check_lifecycle_checkpoint`): `VALID`; verification-09 (C-3 `check_lifecycle_lineage`): `VALID`. Verificación factual sobre `ROADMAP.md`: ninguna sección `## Backlog resuelto`, ninguna tabla B-1…B-8, `B-5` y `B-6` sin aparición como pendientes, `B-1`/`B-2` como trabajo derivado, `B-3` como candidato futuro y `B-4`/`B-7`/`B-8` marcados como payload que requiere autorización. `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, el Placement Contract, los RFCs, los ADRs y los planes históricos sin cambios (0 diff).

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio del mantenedor: `docs(roadmap): update the roadmap to the real project state (plan 132)`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), tree `ad5fe5e6e9b940e4e95a4d061d085260177cd0cd`, delta `ebe7e574bb867d62a38b52bec6386622050c2161601d4299f764dbc19064e556`.
- **Estado de cierre (tree id):** `ad5fe5e6e9b940e4e95a4d061d085260177cd0cd` — el árbol del índice staged del estado validado con el scope declarado (4 paths). El commit de cierre añade únicamente los registros de gobernanza que este propio artifact escribe al cerrar (el `## Validation anchor`, este `## Checkpoint / cierre` y la `## Nota de ejecución`); la diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120 y 123–131) y es verificable tras el commit con `git rev-parse HEAD^{tree}`.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); verificado con C-2, que clasificó este artifact `VALID`.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 132 (fila + serie, Sexagésima cuarta) y su encabezado de estado; `CHANGELOG.md` `[Unreleased]` registra el par (plan 132); `ROADMAP.md` reestructurado como mapa operativo actual; findings `<PLAN-132>:F-1` (`resolved`) y `<PLAN-132>:F-2` (`deferred`, con owner), corrección `<PLAN-132>:C-1` y pending `<PLAN-132>:PC-1` registrados; `**Status:** Executed`.
- **Documentation impact:** **REQUIRED** — documento afectado principal: `ROADMAP.md` (aspecto: presentaba la tabla histórica B-1…B-8 como backlog activo y no distinguía trabajo derivado, pendiente arquitectónico que requiere autoridad ni candidato futuro, de modo que describía un estado del proyecto que ya no era el vigente; actualización: reescritura como mapa operativo actual con las cuatro categorías separadas, `B-1`/`B-2` como trabajo derivado nuevo, `B-4`/`B-7`/`B-8` como pendientes de payload que requieren RFC-56, `B-3` como candidato futuro y `B-5`/`B-6` retirados como pendientes; evidencia: el documento en el árbol validado, con `check_plan_citations` y `check_plan_structure` en verde y sin las afirmaciones retiradas). Documentos afectados además por el registro del Change: `docs/plans/INDEX.md` (fila, serie y encabezado de estado) y `CHANGELOG.md` (ítem `[Unreleased]` del par). La sección del snapshot de versiones de `docs/VERSIONING.md` no se toca (sin release). `README.md`, `AGENTS.md`, `.agents/AGENTS.md`, `.agents/policies/` y `.agents/workflows/` no se modifican: ninguna instrucción activa cambia y la batería canónica no gana un comando obligatorio. **Impacto documental diferido y registrado:** la atribución incorrecta de `B-7` al Plan 43 en `docs/plans/INDEX.md` (`<PLAN-132>:F-2`) queda fuera del scope de este Change por decisión de la consigna, y su continuidad vive en `<PLAN-132>:PC-1` (owner: mantenedor). No se actualiza ningún documento histórico (RFC-46). Sin `VERSION` bump ni tag.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-132>:F-1` — estado: `resolved`; severidad: `high`; observación: el baseline de la consigna exigía confirmar que el Plan 132 estuviera committed y que el Plan 133 estuviera disponible como evidencia principal de la clasificación `B-1`…`B-8`; **ninguno de los dos existe** —no hay archivo en `docs/plans/`, ni objeto en `git log --all`, ni referencia en ningún documento—, de modo que la premisa de evidencia del Change era falsa y el próximo número libre de plan era 132, no 134; evidencia original: `git log --all --oneline` sin coincidencias para los planes 132/133, búsqueda de `Plan 132`/`Plan 133` en el corpus Markdown sin coincidencias, y el listado de `docs/plans/` cuyo máximo es `131-placement-contract-mechanical-implementation.md`; estado Git observado: `dev` @ `65a1113308022b89c29be9f728d670957c35838e`, working tree limpio; provenance original: baseline de este Change; resolución: **decisión humana del mantenedor** (2026-09-15) de ejecutar el Change como **Plan 132** —próximo número libre según la convención de numeración correlativa— y de sostener la clasificación `B-1`…`B-8` con la evidencia re-verificada de forma independiente: `docs/plans/INDEX.md` §Backlog evidenciado - plan 19, `docs/plans/19-anexo-a-bitacora-fricciones.md` (`F-14`, `F-16`, `F-17`), `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md` y `protocol/.agents/contracts/METRICS.md`.
- `<PLAN-132>:F-2` — estado: `deferred` (owner: mantenedor; destino: Change documental futuro de corrección de trazabilidad); severidad: `low`; observación: `docs/plans/INDEX.md` atribuye el ítem histórico `B-7` a los planes 29, **43** y 52, pero `docs/plans/43-intent-reflection-auto-confirm.md` es la corrección de `INTENT_REFLECTION` auto-confirmada sin estado productor, que corresponde a `B-4`; el residuo real de `B-7` es la clasificación de `project_shape` para repositorios documentales/de protocolo (`F-16`), que no tiene plan asociado; evidencia original: `docs/plans/INDEX.md` §Backlog evidenciado - plan 19 (línea de resolución de `B-7`), encabezado de `docs/plans/43-intent-reflection-auto-confirm.md` y `B-7`/`F-16` en `docs/plans/19-anexo-a-bitacora-fricciones.md`; estado Git observado: `dev` @ `65a1113308022b89c29be9f728d670957c35838e`; provenance original: lectura de fuentes durante este Change; resolución: **no corregida aquí** por decisión de scope (la consigna prohíbe mezclar la corrección de trazabilidad histórica con la actualización del Roadmap); el nuevo `ROADMAP.md` no repite esa atribución, de modo que el Roadmap queda factual sin tocar el registro histórico. Continuidad en `<PLAN-132>:PC-1`.

### Correcciones

- `<PLAN-132>:C-1` — refs origen: `<PLAN-132>:F-1`; alcance de revalidación: `docs/plans/132-roadmap-current-state.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`; evidencia (Git/commit/estado): la clasificación `B-1`…`B-8` se sostiene sobre evidencia del repositorio en lugar de sobre el Plan 133 ausente —`B-1` derivado (`D01-discovery-output.md` declara la validación mecánica como extensión futura), `B-2` derivado (plan 33, forma canónica EARS), `B-3` resuelto (plan 50) con el checker de `.last_discovery` como candidato, `B-4` residual (`F-14`, `F-17`), `B-5` resuelto (plan 44), `B-6` resuelto (planes 46 y 67), `B-7` residual (`F-16`), `B-8` residual (el catálogo de eventos de `protocol/.agents/contracts/METRICS.md` no tiene slot para el session risk de single-instance)—, verificada por los checkers documentales en verde sobre el estado de cierre.

### Pending decisions

- `<PLAN-132>:PC-1` — decisión: si y cuándo se corrige en `docs/plans/INDEX.md` la atribución del ítem histórico `B-7` al Plan 43, que corresponde a `B-4`. **No decidida aquí**: la consigna prohíbe mezclar la corrección de trazabilidad histórica con la actualización del Roadmap, y `docs/plans/INDEX.md` se toca únicamente para registrar el Plan 132; blocking: no; owner: mantenedor; escalación: nuevo Change documental de corrección de trazabilidad; resolución: pendiente; evidencia: `<PLAN-132>:F-2`.

## Riesgos

- **Convertir el Roadmap en un inventario histórico.** Mitigación: la tabla B-1…B-8 como backlog se elimina; la historia permanece en `docs/plans/INDEX.md`, los planes y las RFCs, y el Roadmap la menciona sólo como una frase de cierre.
- **Reabrir artificialmente un ítem histórico.** Mitigación: `B-1`/`B-2` figuran como trabajo **derivado nuevo** —con su origen declarado— y `B-3` como candidato futuro; ninguna entrada reintroduce el problema original.
- **Inventar backlog.** Mitigación: cada entrada del Roadmap cita el ítem histórico y la fuente verificable que la sostiene; no se agregan tareas sin evidencia en el repositorio.
- **Presentar como pendiente algo que ya funciona.** Mitigación: `B-5` (política de clarificación desatendida con enforcement) y `B-6` (subcomandos del runner para H15) no aparecen como trabajo; sus planes están `Executed`.
- **Marcar como implementable lo que requiere autoridad de payload.** Mitigación: `B-4`, `B-7` y `B-8` llevan la marca explícita `PENDIENTE — PAYLOAD / REQUIERE AUTORIZACIÓN` y se distinguen de la corrección documental de trazabilidad.
- **Contradecir `docs/plans/INDEX.md`.** Mitigación: el Roadmap no duplica estados de planes ni los recalifica; remite al INDEX como fuente descriptiva.

## Trazabilidad

Backlog evidenciado del plan 19 (`docs/plans/INDEX.md` §Backlog evidenciado - plan 19) → resolución de `B-1`…`B-8` como pares RFC+plan en la Sexta serie → **este Change** (reclasificación de lo que sigue realmente abierto, derivado o candidato) → `ROADMAP.md` como mapa operativo actual. Continuidad del hallazgo de trazabilidad: `<PLAN-132>:F-2` / `<PLAN-132>:PC-1`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `65a1113308022b89c29be9f728d670957c35838e`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica documental: seis checkers PASS (`check_plan_citations`, `check_plan_structure`, `check_protocol_invariants --payload protocol .` con 215 files / 10256 references, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` con los warnings de tags esperados en `dev`). Gates sobre el árbol final: **C-1 `VALID`, C-2 `VALID`, C-3 `VALID`** para el Plan 132. La pierna `python -m pytest tests/` se declara **no ejecutada por diseño**: el Change es puramente documental, no toca `tools/` ni `runtime/`, y el entorno reproduce el GAP ambiental de temporales ya declarado por los Planes 121–131. Verificación factual de `ROADMAP.md`: sin sección `## Backlog resuelto`, sin tabla B-1…B-8, sin `B-5` ni `B-6` como pendientes; `B-1`/`B-2` como trabajo derivado, `B-3` como candidato futuro y `B-4`/`B-7`/`B-8` marcados como payload que requiere autorización.

**Baseline no confirmado y decisión humana.** El baseline de la consigna exigía confirmar que el Plan 132 estuviera committed y que el Plan 133 estuviera disponible como evidencia principal. Ninguno de los dos existe: no hay archivo en `docs/plans/` (el máximo es el 131), no hay objeto en `git log --all` ni en el reflog, no hay entrada en stash ni en las ramas, y ningún documento del repositorio los menciona. El próximo número libre era, por lo tanto, **132**, no 134. Se detuvo el Change en el gate de baseline, se reportó el hueco con evidencia y el mantenedor decidió (2026-09-15) ejecutarlo como **Plan 132** con la clasificación `B-1`…`B-8` sostenida por evidencia del repositorio en lugar del Plan 133 ausente (`<PLAN-132>:F-1`, `<PLAN-132>:C-1`). El número 133 permanece libre y no se reusa.

**Clasificación resultante (evidencia por ítem).** `B-1` **resuelto** (planes 40 y 47); su derivado —checker mecánico del subconjunto D01— se registra como **próximo dogfood**, sostenido por el propio contrato, que declara la validación mecánica como extensión futura hoy inexistente. `B-2` **resuelto** (planes 29 y 33); su derivado —validador estructural EARS— se registra como **siguiente dogfood**. `B-3` **resuelto** (plan 50); el checker mecánico de `.last_discovery` queda como **candidato futuro**. `B-4` **resuelto** (planes 37–43, 53 y 58) con residuo `F-14`/`F-17` en contratos de discovery → **payload**. `B-5` **resuelto** (plan 44) y `B-6` **resuelto** (planes 46 y 67): retirados como pendientes. `B-7` **resuelto** (planes 29 y 52) con residuo `F-16` (`project_shape` documental/de protocolo) → **payload**. `B-8` **resuelto** (plan 49) con residuo limitado al catálogo de eventos de `protocol/.agents/contracts/METRICS.md` → **payload de baja prioridad**.

**Hallazgo de trazabilidad diferido.** `docs/plans/INDEX.md` atribuye `B-7` al Plan 43, pero `docs/plans/43-intent-reflection-auto-confirm.md` corresponde a `B-4` (`INTENT_REFLECTION` auto-confirmada) y no guarda relación con `project_shape`. Se registró como `<PLAN-132>:F-2` en estado `deferred` con owner y continuidad en `<PLAN-132>:PC-1`; **no** se corrigió aquí porque la consigna prohíbe mezclar la corrección de trazabilidad histórica con la actualización del Roadmap. El nuevo `ROADMAP.md` no repite esa atribución, de modo que el mapa queda factual sin tocar el registro histórico.

**Alcance.** 4 paths: `ROADMAP.md` (reescrito), `docs/plans/132-roadmap-current-state.md` (este registro), `docs/plans/INDEX.md` (fila, serie y encabezado) y `CHANGELOG.md` (ítem `[Unreleased]`). Ningún artefacto movido, renombrado ni eliminado; sin carpetas nuevas.

**No realizado (por diseño).** Sin implementación de ninguna de las tareas listadas; sin reapertura de `B-1`/`B-2`/`B-3`/`B-5`/`B-6`; sin backlog inventado; sin recalificación de prioridades históricas sin evidencia. `protocol/`, `protocol/.agents/`, `runtime/`, `tools/`, `tests/`, `.agents/`, el Placement Contract, los ADRs, los RFCs históricos, los planes históricos y CI sin cambios.
