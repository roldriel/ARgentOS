# Plan 160 — Cierre de las decisiones inmediatas (`OD-2`, `OD-6`) y preparación de la autorización de Etapa A

**Status:** Executed
**Fecha:** 2026-10-12
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=0, release impact=0, duration/complexity=0)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, una capa (documentación de gobernanza DEV). *scope*: área acotada — cinco rutas de contenido de gobernanza más este artefacto. *architectural impact*: **0** — no crea estructura, capacidad, estado, autoridad, checker ni mecanismo; corrige prosa normativa vigente, remueve una fila obsoleta del mapa operativo y registra el acto de autorización que falta. *release impact*: ninguno (docs-only, sin `VERSION`, sin tag). *duration/complexity*: menos de una sesión.
**Depende de:** plan 149 (roadmap estratégico A → B → C), plan 151/152/153 (actos de autoridad del modelo de autonomía), plan 159 (materialización de `F-B`)
**Origen:** directiva del mantenedor (2026-10-12) de ejecutar el tramo «cierre de decisiones inmediatas + Etapa A» sin reabrir auditorías cerradas y sin adelantar `F-C`/Etapa B
**Work type:** `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change; el criterio de admisión adoptado (`docs/plans/152-authority-decisions-gov-1-10.md:Acto de autoridad registrado (2026-10-07)`) no se activa aquí y no se deriva un valor por conveniencia.

## Objetivo

Cerrar las dos decisiones que el relevamiento de cierre de `F-C` dejó identificadas como **cerrables ahora** y dejar el repositorio preparado para el tramo siguiente, sin implementar `F-C` ni Etapa B:

1. **`OD-2` — derivación parcial.** Canonizar la decisión ya adoptada (`D-6b = NO`) y corregir únicamente la documentación que la contradice, de modo que la superficie de derivación parcial **no** se lea como trabajo diferido de `F-C`. No se crea la capacidad, no se crea superficie y no se modifica la decisión.
2. **`OD-6` — `work_type`.** Constatar que el criterio de admisión y la política de declaración ya están canonizados (`GOV-8`/`GOV-9`, Plan 152) y reconciliar el mapa operativo, que todavía registra un blocker **obsoleto** («`work_type` sin criterio de admisión»). `P-5` permanece `GAP` como estado por caso, no como bloqueo.
3. **Etapa A.** Determinar su contrato vigente, alcance, criterios de cierre, dependencias y autorización requerida; y, al no estar autorizada, **registrar el acto de gobierno que falta** en el artefacto que lo posee. No se simula autorización, no se crea un artefacto con un estado que afirme una aprobación inexistente y no se ejecuta ningún trabajo de Etapa A.

El Change **no** implementa `F-C`/Etapa B, no toca `runtime/`, `tests/`, `tools/`, `.agents/` ni `protocol/`, y no altera el estado declarado de `F-A` ni de `F-B`.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Directiva del mantenedor (2026-10-12): cerrar las decisiones inmediatas (`OD-2`, `OD-6`), ejecutar Etapa A si la gobernanza lo permite y, si no, preparar el acto de autorización que falta; prohibido implementar `F-C`/Etapa B. `origin_type` = direct maintainer action | humano | consigna de intake de esta sesión |
| `P-2` Confianza de intención | `HIGH` — la consigna nombra las decisiones (`OD-2`, `OD-6`, `OD-4`, `OD-7`), el estado de referencia (`F-A`/`F-B` cerradas, `F-C` no iniciada), las prohibiciones explícitas, el resultado esperado (`ETAPA_A_EXECUTED` / `ETAPA_A_BLOCKED`) y el formato del informe | agente | `INTENT_CONFIDENCE` aplicado sobre la consigna |
| `P-3` Conjunto de contexto | `docs/plans/151-autonomy-authority-decision-closure.md` (`D-6b`, pending de derivación parcial); `docs/adr/19-autonomy-envelope-authority.md` (`Amendment Log`, `Estado de implementación tras el acto del 2026-10-11`); `docs/CONVENTIONS.md:Modelo de autonomía — decisiones de autoridad del Plan 151 (adoptadas 2026-10-07)` y `:Modelo de autonomía — vocabulario de efectos y techo de recurso (adoptado 2026-10-11)`; `docs/CONVENTIONS.md` (subsección «Change Lifecycle — Vigencia materializada, retiro y `work_type`»); `docs/plans/152-authority-decisions-gov-1-10.md`; `docs/VERSIONING.md` §4/§4.1/§7; `ROADMAP.md`; `docs/plans/INDEX.md`; `CHANGELOG.md`; `docs/plans/_TEMPLATE.md`; `docs/plans/149-argentos-capability-and-autonomy-roadmap.md`; plan 159; `.agents/policies/validation-closure.md` §5.1/§5.2; el relevamiento de cierre de `F-C` (provenance de la sesión de intake, **no** artefacto normativo) | agente | las citas de cada fila |
| `P-4` Derivabilidad | `derivable` con señal no bloqueante. La única condición bloqueante identificada —**Etapa A no autorizada**— no bloquea *este* Change: es precisamente el objeto de su registro como pending decision. Sin `ANOMALY`: la contradicción de `OD-2` se resuelve por la decisión vigente (`D-6b = NO`, 2026-10-07) frente a un texto posterior descriptivo, y la de `OD-6` por el canon vigente (`docs/plans/152-authority-decisions-gov-1-10.md:Acto de autoridad registrado (2026-10-07)`) frente a una fila obsoleta del mapa operativo | agente | `docs/plans/151-autonomy-authority-decision-closure.md:Pending decisions`; `docs/CONVENTIONS.md`; `ROADMAP.md:🚧 Bloqueos que pueden cambiar el camino` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change; el criterio de admisión adoptado no se activa y **no se inventa** un valor | agente | `docs/plans/152-authority-decisions-gov-1-10.md:Acto de autoridad registrado (2026-10-07)` (`GOV-8`/`GOV-9`; regla `HD-K2` de `docs/CONVENTIONS.md`) |
| `P-6` Conocimiento vigente | `ADR-19` `Accepted` (con Amendment Log); `Plan 151`/`152`/`153` y `Plan 159` `Executed`; `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` activos; `runtime/` es código vigente, no legacy | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (Change Lifecycle DEV), RFC-69 (taxonomía documental), ADR-16 (autoridad), ADR-19 (envelope de autonomía), `docs/VERSIONING.md` §4/§4.1/§7, VC-1/GC-1/LC-1/PC-1. `NOT_APPLICABLE`: RFC-56 (sin efecto payload), RFC-46 (no se reescriben artefactos históricos; la corrección es hacia adelante) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **directiva del mantenedor (2026-10-12)**, que autoriza cerrar `OD-2`/`OD-6` y preparar el registro de autorización de Etapa A. Scope declarado: `docs/CONVENTIONS.md`, `docs/adr/19-autonomy-envelope-authority.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` | **humano** | declaración del humano en la consigna de intake |

## Criterio de entrada

- [x] Baseline verificada: rama `dev`, `HEAD` = `64398ba15d739e88391d9eaf57baa6ecb3027cf7`, `git status --porcelain` vacío, `dev` ahead 8 de `origin/dev`.
- [x] `F-A` y `F-B` constan cerradas en los artefactos vigentes: `docs/plans/159-autonomy-envelope-implementation.md` (`Status: Executed`, condición derivada `Closed`) y `docs/adr/19-autonomy-envelope-authority.md:Estado de implementación tras el acto del 2026-10-11`.
- [x] El relevamiento de cierre de `F-C` está concluido y establece `F-C` = no iniciada, sin contrato y dependiente de Etapa A (provenance de la sesión de intake).
- [x] `D-6b = NO` y su pending `NOT_APPLICABLE` verificados en `docs/plans/151-autonomy-authority-decision-closure.md:Pending decisions` y `docs/CONVENTIONS.md:Modelo de autonomía — decisiones de autoridad del Plan 151 (adoptadas 2026-10-07)`.
- [x] Criterio de admisión y política de declaración de `work_type` verificados como adoptados en `docs/CONVENTIONS.md` (subsección «Change Lifecycle — Vigencia materializada, retiro y `work_type`») y en `docs/plans/152-authority-decisions-gov-1-10.md:Acto de autoridad registrado (2026-10-07)`.
- [x] Batería canónica de baseline registrada: `check_protocol_invariants` PASS (216 archivos, 10457 referencias); `check_plan_citations` **26 citas rotas** (baseline preexistente, documentos históricos) y **1** referencia legacy preexistente; `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts` y `check_version_state` PASS.
- [x] Etapa A verificada como **no autorizada**: `ROADMAP.md:🚧 Bloqueos que pueden cambiar el camino` («La Etapa A no está autorizada … requiere su propio Change»).
- [x] Autorización del mantenedor para este Change (consigna de intake, 2026-10-12).

## Entregables

1. `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` (**este archivo**) — registro del Change y vehículo de la preparación de Etapa A.
2. `docs/adr/19-autonomy-envelope-authority.md` — entrada de Amendment Log (2026-10-12) que registra la reconciliación de `OD-2`: la superficie de derivación parcial está **descartada** por `D-6b = NO`, no diferida. Sin reescribir las entradas anteriores.
3. `docs/CONVENTIONS.md` — corrección de la viñeta «Fuera de este acto» de la subsección adoptada el 2026-10-11, que enumeraba la superficie de derivación parcial entre lo diferido.
4. `ROADMAP.md` — retiro de la fila de blocker obsoleta de `work_type` (su contenido tiene dueño en `docs/CONVENTIONS.md` y en el Plan 152) y precisión de la fila de Etapa A con el artefacto que posee el acto de autorización requerido.
5. `docs/plans/INDEX.md` — serie **Octogésima novena**, fila del Plan 160 y encabezado de estado.
6. `CHANGELOG.md` — ítem `[Unreleased]` del Change.

## Pasos

1. **Paso 0 — preflight.** Registrar baseline (rama, `HEAD`, worktree, batería canónica) y confirmar que `F-A`/`F-B` figuran cerradas y que Etapa A no está autorizada.
2. **Paso 1 — `OD-2`.** Verificar `D-6b = NO` y su pending en `docs/plans/151-autonomy-authority-decision-closure.md:Pending decisions`; localizar los textos posteriores que lo contradicen; corregir `docs/CONVENTIONS.md` (viñeta «Fuera de este acto») y agregar la entrada de reconciliación en `docs/adr/19-autonomy-envelope-authority.md:Amendment Log`. Sin crear capacidad ni mecanismo.
3. **Paso 2 — `OD-6`.** Verificar el canon vigente de `work_type`; constatar que el blocker del mapa operativo es obsoleto; retirarlo de `ROADMAP.md:🚧 Bloqueos que pueden cambiar el camino` y registrar en este Plan el destino de su contenido (artefacto dueño).
4. **Paso 3 — Etapa A.** Determinar contrato, alcance, autorización requerida, criterios de cierre, dependencias y Change aplicable; registrar el acto de autorización faltante como pending decision (`PC-1`) con owner, escalación, evidencia y efecto downstream; precisar la fila de Etapa A en el ROADMAP con el artefacto que la posee.
5. **Paso 4 — registro.** Registrar el Change en `docs/plans/INDEX.md` (encabezado de estado, serie y fila) y en `CHANGELOG.md` `[Unreleased]`.
6. **Paso 5 — verificación.** Batería canónica completa, gates C-1/C-2/C-3 y verificación factual de scope (`git diff --name-only` ⊆ `## Delegación agentiva` → `Scope`); comparar el conteo de `check_plan_citations` contra el baseline (26).
7. **Paso 6 — cierre.** Registrar `## Validation anchor`, `## Checkpoint / cierre` y `## Nota de ejecución`; determinar los dos impactos de cierre (§5.1/§5.2 de `.agents/policies/validation-closure.md`); commit atómico en `dev`.

## Etapa A — contrato vigente y autorización faltante

Determinación exigida antes de trabajar sobre la Etapa A (`ROADMAP.md:⏭️ NEXT` y
`docs/plans/149-argentos-capability-and-autonomy-roadmap.md`). La conclusión es **`ETAPA_A_BLOCKED`**: la
Etapa A no está autorizada y este Plan **no** la autoriza por inferencia.

1. **Contrato vigente.** Una **retrospectiva de capacidades y garantías** —no una auditoría documental ni
   una limpieza de archivos—: determina qué capacidades y garantías están realmente demostradas y con qué
   evidencia. Su unidad de análisis es *capacidad + garantía + evidencia*; su pregunta central es qué
   puede afirmar ARgentOS que hace, con qué mecanismo y con qué evidencia, bajo las condiciones en las
   que se pretende utilizarlo. Fuente: `ROADMAP.md:⏭️ NEXT` y la sección de Etapa A de
   `docs/plans/149-argentos-capability-and-autonomy-roadmap.md`.
2. **Alcance.** El alcance conceptual mínimo, los ocho niveles de madurez y la **Capability & Guarantee
   Matrix** (nueve dimensiones por capacidad) están declarados por el Plan 149; su materialización es
   documental y su resultado puede **reducir** el alcance de la Etapa B. No incluye implementar
   capacidades.
3. **Autorización requerida.** Un **Change propio con su autorización**: `ROADMAP.md:🚧 Bloqueos que
   pueden cambiar el camino` declara «La Etapa A no está autorizada … requiere su propio Change», y
   `ROADMAP.md` registra el trabajo activo como **ninguno**. La vía aplicable es un Plan —Clase B por su
   naturaleza documental— **`Aprobado para ejecución`** por acto del mantenedor; si el producto
   requiriera tocar `protocol/.agents/`, la vía sería RFC-56 Clase A (RFC `Accepted` + plan). Ninguna
   fuente vigente contiene ese acto.
4. **Criterios de cierre (`DONE`).** **No existen formalmente.** El Plan 149 declara propósito, unidad de
   análisis y producto, pero no una lista de criterios de cierre verificables; fijarlos corresponde al
   Plan que autorice la Etapa A. Este Plan **no** los inventa: registra la ausencia como condición a
   resolver en ese acto.
5. **Plan/Change aplicable.** **No existe.** El Plan 149 declaró el roadmap y dejó la Etapa A como
   próximo Change **declarado, no autorizado**. Número libre: **161**.
6. **Dependencias.** Ninguna técnica: las fuentes del análisis (runtime, tests, `docs/`, checkers) ya
   existen, y `PR-1`/`PR-2` —dos fronteras candidatas de la Etapa B— fueron absorbidas por `F-B`, lo que
   **reduce** la superficie de la Etapa A. Las dependencias reales son de gobernanza: el acto de
   autorización y la fijación de los criterios de cierre.
7. **Qué puede ejecutarse ahora.** Nada material: no se ejecuta la retrospectiva, no se construye la
   matriz y **no** se crea el artefacto del Plan de Etapa A con un estado que afirme una aprobación
   inexistente (el ciclo de estados de `docs/VERSIONING.md` §7 no tiene un estado pre-aprobación). Queda
   preparado lo que sí es documentable: la **especificación** del Change (contrato, alcance, dependencias,
   número) y el registro del acto que falta, en `### Pending decisions` de este Plan.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | Este Change no produce efectos fuera de la frontera inmediata: escribe únicamente paths locales dentro de su `Scope` declarado y no ejecuta red, git remoto, instalaciones ni cambios destructivos. | — (declaración negativa; no requiere autorización de efecto) | `authorized` |

## Criterios de salida

- [x] `OD-2` cerrado: `D-6b = NO` es la decisión efectiva y ningún texto vigente describe la superficie de derivación parcial como trabajo diferido; la reconciliación queda registrada en ADR-19 y en `docs/CONVENTIONS.md`, sin reescribir historia (RFC-46) y sin crear capacidad.
- [x] `OD-6` cerrado: el criterio de admisión y la política de declaración de `work_type` constan canonizados; el blocker obsoleto ya no figura en el mapa operativo; `P-5` permanece `GAP` y no se deriva ningún `work_type`.
- [x] Etapa A: contrato, alcance, autorización requerida, criterios de cierre, dependencias y Change aplicable determinados y registrados; el acto de autorización faltante queda como pending decision bloqueante con owner.
- [x] `F-C` y Etapa B permanecen no implementadas: 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/`.
- [x] `OD-4` y `OD-7` tratados como ya decididos, sin cambio alguno.
- [x] Batería canónica en verde (con el rojo preexistente declarado) y sin aumento de citas rotas respecto del baseline (26).
- [x] `## Validation anchor` y `## Checkpoint / cierre` registrados; `Status: Executed` con condición derivada `Closed`.

## Verificación

```bash
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

Verificación factual adicional: `git diff --name-only HEAD` ⊆ `Scope`; conteo de citas rotas = baseline (26); 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/` y `protocol/`.

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** las cinco rutas que la identidad de contenido mide — `CHANGELOG.md`, `ROADMAP.md`, `docs/CONVENTIONS.md`, `docs/adr/19-autonomy-envelope-authority.md` y `docs/plans/INDEX.md`. Queda fuera del scope **medido** la governance del propio Change (este artefacto), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 114/116/134/140–149/155–159). El scope autorizado por `P-8` tiene una ruta más: este artefacto. No se declara `## Delegación agentiva` (ausencia declarada: no hay trabajo semántico delegado).
- **Validation command-set:** los siete comandos de `docs/VERSIONING.md` §4.1 + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + la verificación factual de scope (`git diff --cached --name-only` ⊆ el scope de `P-8`) y del conteo de citas rotas contra el baseline del `## Criterio de entrada`.
- **Effective inputs (repo content):** el scope declarado; `docs/plans/151-autonomy-authority-decision-closure.md` (`D-6b` y su pending); `docs/plans/152-authority-decisions-gov-1-10.md` (`GOV-8`/`GOV-9`); `docs/plans/149-argentos-capability-and-autonomy-roadmap.md`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `ROADMAP.md`; `docs/plans/INDEX.md`; `CHANGELOG.md`; `docs/plans/_TEMPLATE.md`; el corpus completo de `docs/plans/` y `docs/rfc/` como población de `check_plan_citations` y de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada de `check_protocol_invariants`; y el estado Git de `dev`.
- **Observed dependencies:** stdlib únicamente; el CLI `git` para las identidades de contenido y la resolución de objetos; `pytest` con basetemp externo al repositorio (`tests/pytest_isolation.py`). Sin red.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; `pytest` 9.0.3; repositorio bajo OneDrive. **Clase ambiental declarada:** `check_dist_sync.py` **no** aplica (local-only, verde sólo en `master`; este Change no promueve). `check_plan_citations.py` sigue rojo por las **26** citas rotas preexistentes de documentos históricos a secciones eliminadas del ROADMAP (`<PLAN-157>:F-1`/`<PLAN-158>:F-2`), **sin aumento** respecto del baseline registrado en el `## Criterio de entrada`. No se consumió red, provider ni credenciales.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `b79f8e13f6529e71dc790ea5afaa6abfc1039f37` — tree id del índice staged del scope medido (`tools/scoped_content_identity.py`, source `staged`), computado antes de escribir los registros de cierre.
  - **Delta scoped identity (scope S = las cinco rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `cffd1cc70b0ac3cb07b0cefb55063dc28a08ee875b0a4080da20600ff7a18fda`.
  - **Límite declarado:** el scope medido excluye la governance del Change (este artefacto); la identidad se computó antes de escribir los registros de cierre.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `ROADMAP.md`, `docs/CONVENTIONS.md`, `docs/adr/19-autonomy-envelope-authority.md`, `docs/plans/INDEX.md`
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): **PASS** (216 archivos, 10457 referencias); verification-02 (`check_plan_citations`): **FAIL preexistente** — 26 citas rotas, sin aumento respecto del baseline; verification-03 (`check_plan_structure`): **PASS**; verification-04 (`check_taxonomy_coherence`): **PASS**; verification-05 (`check_session_artifacts`): **PASS**; verification-06 (`check_version_state`): **PASS** (warnings de tags esperados en `dev`); verification-07 (`python -m pytest tests/`): **PASS** — `1316 passed` en 444,87 s; verification-08 (C-1): **ANOMALY=0**; verification-09 (C-2): **ANOMALY=0**; verification-10 (C-3): **ANOMALY=0**. Verificación factual: `git diff --cached --name-only` ⊆ el scope de `P-8`; **0 diff** en `runtime/`, `tests/`, `tools/`, `.agents/` y `protocol/`; conteo de citas rotas = baseline (26).

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio del mantenedor: `docs(governance): close immediate decisions and prepare the Stage A authorization (plan 160)`. Se identifica por su mensaje (convención anti-circularidad: el árbol no embebe su propia identidad). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `b79f8e13f6529e71dc790ea5afaa6abfc1039f37`, delta scoped identity `cffd1cc70b0ac3cb07b0cefb55063dc28a08ee875b0a4080da20600ff7a18fda`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `cffd1cc70b0ac3cb07b0cefb55063dc28a08ee875b0a4080da20600ff7a18fda` / `b79f8e13f6529e71dc790ea5afaa6abfc1039f37`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de cierre incluye la governance del Change (este artefacto y sus registros), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); C-2 clasificó el corpus sin `ANOMALY`.
- **Governance aplicada:** `docs/adr/19-autonomy-envelope-authority.md` (entrada de Amendment Log 2026-10-12, sin reescribir las entradas anteriores); `docs/CONVENTIONS.md` (corrección de la viñeta «Fuera de este acto»); `ROADMAP.md` (retiro del blocker obsoleto de `work_type` y precisión de la fila de Etapa A); `docs/plans/INDEX.md` (encabezado de estado y serie **Octogésima novena** + fila); `CHANGELOG.md` `[Unreleased]`; `**Status:** Executed`. Sin RFC-56 (0 diff en `protocol/`), sin ADR nuevo, sin `VERSION` bump ni tag.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados y su aspecto: `docs/adr/19-autonomy-envelope-authority.md` (aspecto: la entrada del 2026-10-11 enumeraba la «superficie de derivación parcial» entre lo que dejaba fuera, contradiciendo `D-6b = NO`; actualización: entrada de Amendment Log 2026-10-12 que la declara **descartada**, no diferida, preservando el texto anterior íntegro; evidencia: el diff de este Change). `docs/CONVENTIONS.md` (aspecto: la viñeta «Fuera de este acto» listaba la superficie de derivación parcial entre los elementos diferidos; actualización: la excluye explícitamente y cita la reconciliación; evidencia: el diff). `ROADMAP.md` (aspecto: registraba un blocker **obsoleto** —«`work_type` sin criterio de admisión»— y una fila de Etapa A sin artefacto dueño; actualización: la fila obsoleta se retira porque su contenido tiene artefacto dueño en `docs/CONVENTIONS.md` (subsección «Change Lifecycle — Vigencia materializada, retiro y `work_type`») y en `docs/plans/152-authority-decisions-gov-1-10.md`, y la fila de Etapa A nombra el artefacto que posee el acto requerido; evidencia: el diff). `docs/plans/INDEX.md` y `CHANGELOG.md` por el registro del Change. **No** se actualiza ningún documento histórico (RFC-46): los Planes 149/151/152/153/159 y las entradas previas del Amendment Log quedan intactos.
- **Roadmap impact:** `REQUIRED` — reconciliado en el artefacto que posee el estado. Ítems afectados: el blocker obsoleto de `work_type` se **retira** del mapa operativo (su contenido conserva dueño) y la fila de Etapa A se precisa con el artefacto dueño del acto de autorización requerido. No se crea, completa, cancela ni re-prioriza ninguna iniciativa: `NOW`, `NEXT` y `LATER` conservan sus ítems y `F-C`/Etapa B permanecen en `LATER` sin cambio de estado, prioridad ni dependencia.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-160>:F-01` — estado: `resolved`; severidad: `low`; observación: el Plan citaba el criterio de admisión de `work_type` con la forma `ruta:sección` apuntando al heading de la subsección de vigencia y `work_type` de `docs/CONVENTIONS.md`, que **no resuelve** como cita: el heading real contiene backticks alrededor de `work_type` y esa forma rompe la cita `path:section` del checker (con lo cual el Change habría aumentado las citas rotas del baseline). Evidencia original: el heading real de `docs/CONVENTIONS.md` y la verificación de citas previa a la validación; estado git observado: worktree de `dev` sobre `64398ba15d739e88391d9eaf57baa6ecb3027cf7`, sin commit; provenance original: verificación de este Plan durante la ejecución (Paso 1/Paso 2); resolución: `resolved` por `<PLAN-160>:C-01` — las cuatro ocurrencias se sustituyeron por la cita resoluble al acto que adoptó el criterio (`docs/plans/152-authority-decisions-gov-1-10.md:Acto de autoridad registrado (2026-10-07)`) y por una referencia en prosa a la subsección de `docs/CONVENTIONS.md`.

### Correcciones

- `<PLAN-160>:C-01` — refs origen: `<PLAN-160>:F-01`; alcance de revalidación: `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` (cuatro ocurrencias: `P-3`, `P-4`, `P-5` y `## Criterio de entrada`), sin efecto sobre el scope medido por el Validation anchor; evidencia: la batería canónica final registra **26** citas rotas — el baseline auditado en el `## Criterio de entrada` — con **cero** citas rotas nuevas.

### Pending decisions

- `<PLAN-160>` — decisión: **acto de autorización de la Etapa A** (retrospectiva de capacidades y garantías); blocking: **sí** para iniciar Etapa A —y, por dependencia declarada, para `F-C` y Etapa B—; owner: **mantenedor**; escalación: acto de autoridad explícito registrado en el Change de Etapa A; resolución: **`PENDING_AUTHORITY`** — `ROADMAP.md:🚧 Bloqueos que pueden cambiar el camino` declara que la Etapa A «requiere su propio Change» y `ROADMAP.md` registra el trabajo activo como **ninguno**; ninguna fuente vigente autoriza la Etapa A, y este Plan **no** la autoriza por inferencia; evidencia: `ROADMAP.md:⏭️ NEXT` y `ROADMAP.md:🚧 Bloqueos que pueden cambiar el camino`; efecto downstream: habilita la creación del Plan de Etapa A (número libre **161**) y, con ella, el cierre de `OD-1` sobre el alcance de `F-C`; ADR-worthiness: no evaluada (no hay decisión arquitectónica que registrar).

## Riesgos

1. **Ampliar el alcance hacia `F-C`/Etapa B.** Mitigación: `## Efectos declarados` negativo; criterios de salida acotados a `OD-2`/`OD-6` y al registro del acto faltante; 0 diff declarado en `runtime/`, `tests/`, `tools/`, `.agents/` y `protocol/`.
2. **Corregir la decisión en lugar de la documentación.** Mitigación: `D-6b = NO` no se modifica y no se crea superficie; la corrección es de prosa y se registra como reconciliación fechada.
3. **Simular autorización de Etapa A.** Mitigación: no se crea un artefacto de Etapa A con un estado que afirme aprobación; el acto faltante se registra como pending decision con owner.
4. **Reescribir historia.** Mitigación: en ADR-19 se **agrega** una entrada de Amendment Log; el texto de las entradas anteriores se preserva íntegro; `docs/plans/151`, `152`, `153` y `159` no se modifican.
5. **Convertir una fila obsoleta en una pérdida de información.** Mitigación: el contenido retirado del ROADMAP se registra con su artefacto dueño (`docs/CONVENTIONS.md` y Plan 152) en `## Checkpoint / cierre` → `Documentation impact`.

## Trazabilidad

```text
relevamiento de cierre de F-C (provenance de la sesión de intake)
        │
        ▼
OD-2 (derivación parcial) ──► ADR-19 (Amendment Log 2026-10-12) · CONVENTIONS.md
OD-6 (work_type)          ──► ROADMAP.md (retiro de blocker obsoleto)
Etapa A                   ──► pending decision bloqueante (owner: mantenedor)
        │
        ▼
Plan 160 ──► INDEX (Octogésima novena serie) · CHANGELOG [Unreleased]
        │
        ▼
próximo paso: acto de autorización de Etapa A → Plan 161
```

## Nota de ejecución

*2026-10-12. Ejecutado en `dev` @ `64398ba15d739e88391d9eaf57baa6ecb3027cf7` (baseline del preflight: worktree limpio; `dev` ahead 8 de `origin/dev`; `VERSION` del payload `12.0.1` sin tag; `python -m pytest tests/ -q` = **1316 passed** en 444,87 s; batería canónica con el rojo preexistente declarado —**26** citas rotas— y el resto en verde).*

Una sola pasada, en el orden del `## Pasos`:

1. **Preflight** — rama `dev`, `HEAD` `64398ba`, worktree limpio; `F-A`/`F-B` confirmadas cerradas; Etapa A confirmada **no autorizada**; baseline de checkers registrado en el `## Criterio de entrada`.
2. **`OD-2`** — verificado `D-6b = NO` en `docs/CONVENTIONS.md` y su pending `NOT_APPLICABLE` en `docs/plans/151-autonomy-authority-decision-closure.md:Pending decisions`; corregida la viñeta «Fuera de este acto» de `docs/CONVENTIONS.md` y agregada la entrada de Amendment Log 2026-10-12 en `docs/adr/19-autonomy-envelope-authority.md`, que declara la superficie de derivación parcial **descartada** (no diferida) y preserva íntegro el texto anterior (RFC-46).
3. **`OD-6`** — constatado que el criterio de admisión y la política de declaración de `work_type` ya estaban canonizados (`GOV-8`/`GOV-9`, Plan 152); retirada de `ROADMAP.md` la fila de blocker **obsoleta** —cuyo contenido conserva artefacto dueño— y precisada la fila de Etapa A con el artefacto que posee el acto de autorización requerido. `P-5` permanece `GAP`.
4. **Etapa A** — determinados contrato, alcance, autorización requerida, criterios de cierre (inexistentes formalmente: los fija el Plan que la autorice), dependencias y Change aplicable (número libre 161); registrado el acto de autorización faltante como pending decision bloqueante con owner. **No** se creó un artefacto de Etapa A con un estado que afirmara una aprobación inexistente y **no** se ejecutó trabajo de Etapa A.
5. **Registro** — `docs/plans/INDEX.md` (encabezado de estado + Octogésima novena serie + fila) y `CHANGELOG.md` `[Unreleased]`.
6. **Verificación** — batería canónica completa (verification-01…07) y gates C-1/C-2/C-3 (verification-08…10), sin `ANOMALY`; verificación factual de scope y de citas rotas contra el baseline.
7. **Cierre** — `## Validation anchor` A1 con state identity `b79f8e13f6529e71dc790ea5afaa6abfc1039f37` y delta scoped identity `cffd1cc70b0ac3cb07b0cefb55063dc28a08ee875b0a4080da20600ff7a18fda`; checkpoint, determinaciones de impacto y commit atómico.

**Un finding real, resuelto dentro de la ejecución y declarado en `## Findings`:** `<PLAN-160>:F-01` — una cita `ruta:sección` a un heading que contiene backticks no resuelve; se sustituyó por la cita al acto que adoptó el criterio, y el conteo de citas rotas se mantiene en el baseline.

**Fuera de alcance por directiva:** `F-C`/Etapa B, provider/modelo, aislamiento/sandbox, Memory, concurrencia, telemetría, retry autónomo y cualquier capacidad clasificada como tramo posterior. `OD-4` (`--sae` opt-in) y `OD-7` (`PR-1`/`PR-2` absorbidos por `F-B`) se tratan como ya decididos, sin cambio.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1).
Committed = TRUE  — commit atómico en `dev`, identificado por su mensaje.
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump, sin tag, sin promoción a `master`, sin `dist`.
```

**Próximo paso exacto.** El mantenedor ejerce el **acto de autorización de Etapa A** (`### Pending decisions`); con él se crea el Plan de Etapa A (número **161**) desde `docs/plans/_TEMPLATE.md`, con su scope, sus criterios de cierre y su `## Delegación agentiva` si corresponde. `F-C` no se define antes de ese resultado.
