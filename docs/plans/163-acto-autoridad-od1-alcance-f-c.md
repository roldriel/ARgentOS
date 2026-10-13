# Plan 163 — Acto de autoridad de `OD-1`: alcance canónico de `F-C`

**Status:** Executed
**Fecha:** 2026-10-12
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only, docs-only, sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=0, release impact=0, duration/complexity=0)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, una capa. *scope*: área acotada — cinco rutas de gobernanza. *architectural impact*: **0** — registra una decisión de **alcance** y su contenido normativo; no crea capacidad, entidad, estado, autoridad, contrato ni mecanismo. *release impact*: ninguno. *duration/complexity*: menos de una sesión.
**Depende de:** plan 162 (instrumento decision-ready de `OD-1`), plan 161 (resultado de Etapa A), plan 159 (`F-B`), `docs/adr/19-autonomy-envelope-authority.md` (envelope), plan 160 (autorización de Etapa A)
**Origen:** acto del mantenedor (2026-10-12) que ejerce la decisión preparada por el Plan 162 y resuelve `OD-1`
**Work type:** `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change; no se deriva ni se inventa.

## Acto de autoridad registrado (2026-10-12)

| Campo | Contenido |
|---|---|
| **Decisión** | `OD-1` — «¿Cuál es el alcance canónico de `F-C`?» |
| **Autoridad** | **Mantenedor** (acto del 2026-10-12; decisión ejercida sobre el instrumento decision-ready del Plan 162) |
| **`Q-a` — interpretación adoptada** | **`B`** — «`F-C` = Etapa B **delimitada por Etapa A** a la frontera de autonomía». **`R1` delimitada**, no `R2` y no una tercera lectura: `F-C` y Etapa B **no** son dos iniciativas paralelas; `F-C` es el nombre de trabajo de la iniciativa «Complete ARgentOS Autonomy» con su alcance ya **reducido** por el resultado de la Etapa A |
| **`Q-b` — qué representa el resto de Etapa B** | El resto **no** se conserva como iniciativa paralela: la parte de Etapa B que no es frontera de autonomía (brechas de capacidad del **payload del Protocol**) queda **fuera de `F-C`** y sigue su propia vía, con su propia decisión de alcance |
| **`Q-c` — capacidades/condiciones** | **Dentro**: actor con provider/modelo · aislamiento/sandbox (o declaración explícita de la garantía que **no** se ofrece) · Memory como contexto · objetivo multi-Change · más las **condiciones** `C-02` (contención de autoridad fuera del host) y `C-26` (recuperación ante fallos reales, incluida la discrepancia declarada sobre el retry). **Fuera**: `C-16` Discovery, `C-17` Discovery KB y `C-21` Skills |
| **`Q-d` — ADR** | **No** — registro normativo **aditivo** en `docs/CONVENTIONS.md` (subsección del modelo de autonomía); sin ADR nuevo y sin enmienda de ADR-19 |
| **Rationale (fuente: el acto)** | Es la única formulación que usa el mandato de reducción que el propio `ROADMAP.md` declara («su resultado puede **reducir** el alcance de la Etapa B») sin convertir una inferencia en decisión; `R2` obligaba a leer `(F-C/Etapa B)` de ADR-19 como dos cosas distintas, contra las cinco menciones vivas que los equiparan; la evidencia de Etapa A muestra que las brechas de menor madurez (`C-16`/`C-17`/`C-21`) son del **payload** y su garantía depende de una adopción real, no de trabajo de autonomía del DEV |
| **Evidencia** | El propio acto (decisión del mantenedor sobre `Q-a`/`Q-d`); el instrumento `docs/plans/162-instrumento-decision-od1-alcance-f-c.md` (opciones, soporte y tensión); `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` (evidencia primaria); `ROADMAP.md` (mandato de reducción) |
| **Registro normativo** | `docs/CONVENTIONS.md` → subsección **«Modelo de autonomía — alcance canónico de `F-C` (acto del 2026-10-12)»**, aditiva; las subsecciones del 2026-10-07 y del 2026-10-11 **no se modifican** |
| **Efecto sobre `OD-1`** | **`RESUELTA`** — la pending decision del `<PLAN-161>` deja de bloquear (se anota su resolución en el artefacto que la posee, de forma aditiva) |

```text
OD1          = RESOLVED (acto del mantenedor, 2026-10-12)
F-C          = SCOPED — alcance canónico resuelto; ejecución NO autorizada
ETAPA_B      = delimitada dentro de F-C (no existe como iniciativa paralela)
F-C_IMPL     = NOT_IMPLEMENTED (sin autorización de ejecución)
```

## Objetivo

Formalizar el acto que resuelve `OD-1` y dejar la definición canónica de `F-C` incorporada a la gobernanza: interpretación adoptada, definición precisa, relación `F-C` ↔ Etapa B, boundary con `F-A` y con `F-B`, capacidades y hallazgos dentro, exclusiones explícitas, lo que **no** debe inferirse, y dependencias y condiciones previas de la futura implementación.

El Change **no** implementa ninguna capacidad de `F-C`, **no** autoriza su ejecución, **no** inicia Etapa B, **no** modifica `runtime/`, `tests/`, `tools/`, `.agents/` ni `protocol/`, y **no** altera defaults de autonomía, el envelope de `F-B` ni los techos de recurso.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | El mantenedor resuelve `OD-1` sobre el instrumento del Plan 162: adopta la interpretación **`B`** (`F-C` = Etapa B delimitada a la frontera de autonomía) y el registro normativo **sin ADR**. `origin_type` = direct maintainer action | humano | el acto de esta sesión (respuesta del mantenedor a `Q-a`/`Q-d`) |
| `P-2` Confianza de intención | `HIGH` — el acto nombra la opción adoptada entre opciones cerradas y ya documentadas, y la vía de registro; el objeto y el efecto están fijados por el Plan 162 | agente | `INTENT_CONFIDENCE` aplicado sobre el acto |
| `P-3` Conjunto de contexto | `docs/plans/162-instrumento-decision-od1-alcance-f-c.md`; `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md`; `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/adr/16-change-lifecycle-authority.md`; `docs/CONVENTIONS.md`; `ROADMAP.md`; `docs/plans/159-autonomy-envelope-implementation.md`; `CHANGELOG.md`; `docs/VERSIONING.md` §7 | agente | las citas de cada fila |
| `P-4` Derivabilidad | `derivable` sin señal bloqueante: la decisión existe, es explícita, su objeto estaba preparado y su registro está determinado. **No** hay `REQUIRES_HUMAN` pendiente: el acto humano ya se ejerció | agente | el acto; `docs/plans/162-instrumento-decision-od1-alcance-f-c.md:Pregunta de decisión (a ejercer por el mantenedor)` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`) |
| `P-6` Conocimiento vigente | `Plan 159`, `160`, `161` y `162` `Executed`; `ADR-19` y `ADR-16` `Accepted`; `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md` activos; el producto de Etapa A es Working (`active`, no normativo) | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (Change Lifecycle DEV), RFC-69 (taxonomía documental), ADR-16 (`AU-3`/`AU-5`/`AU-6`), ADR-19 (envelope, como precondición cerrada), `docs/VERSIONING.md` §4/§4.1/§7, VC-1/GC-1/LC-1/PC-1. `NOT_APPLICABLE`: RFC-56 (sin efecto payload), RFC-46 (la anotación de la pending es aditiva; no se reescribe historia) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **acto del mantenedor (2026-10-12)**. Scope declarado: `docs/plans/163-acto-autoridad-od1-alcance-f-c.md` (este artefacto), `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` y `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` (anotación **aditiva** de la resolución de la pending `OD-1` en el artefacto que la posee) | **humano** | el acto |

## Criterio de entrada

- [x] Instrumento decision-ready leído y vigente (`docs/plans/162-instrumento-decision-od1-alcance-f-c.md`, `Executed`).
- [x] Evidencia primaria de Etapa A disponible (matriz 28 × 9, `Closed`).
- [x] `F-A`, `F-B` y Etapa A `Closed`; `OD-2`/`OD-4`/`OD-6`/`OD-7` resueltas o ya decididas.
- [x] Acto del mantenedor ejercido sobre `Q-a` (`B`) y `Q-d` (`No` ADR).
- [x] Baseline verificada (rama `dev`, `HEAD` `5dc2e72`, worktree limpio) y baseline de citas rotas (**26**).

## Alcance

### IN SCOPE

1. Registrar el **acto** y su trazabilidad (`decisión → autoridad → fecha → evidencia → registro`).
2. La **definición canónica de `F-C`**: interpretación adoptada, definición, relación con Etapa B, boundary con `F-A` y con `F-B`, capacidades y condiciones dentro, exclusiones explícitas, lo que no debe inferirse, y dependencias y precondiciones.
3. El **registro normativo aditivo** en `docs/CONVENTIONS.md` (modelo de autonomía).
4. La **preparación del trabajo futuro**: criterios de cierre requeridos del Change de `F-C`, Change Level mínimo esperado, dependencias y estado correcto (**sin** crear ni autorizar su Plan de ejecución).
5. La reconciliación derivada: `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` y la anotación aditiva de la pending `OD-1` en `<PLAN-161>`.

### OUT OF SCOPE

1. **Implementar** cualquier capacidad de `F-C` (provider/modelo, aislamiento/sandbox, Memory, multi-Change, contención de autoridad, recuperación/retry) o de cualquier otro tramo.
2. **Autorizar la ejecución de `F-C`** o crear su Plan de ejecución con estado `Aprobado para ejecución`.
3. **Iniciar Etapa B**; **modificar** `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` o `dist/`.
4. Cambiar defaults de autonomía, activar `--sae`, modificar el envelope de `F-B`, los techos de recurso o el vocabulario de efectos.
5. **Incorporar** a `F-C` las brechas del payload (`C-16`/`C-17`/`C-21`) o cualquier capacidad fuera de `IN SCOPE`, por simetría, madurez baja o disponibilidad tecnológica.
6. Resolver decisiones que pertenezcan a la implementación futura (elección de proveedor, diseño de aislamiento, esquema de Memory, forma del objetivo multi-Change).
7. Limpieza documental lateral, refactors o reorganización.

### DEPENDENCIES

```text
F-A       = CLOSED            (precondición de F-C)
F-B       = CLOSED            (precondición de F-C; envelope intocable por F-C)
Etapa A   = CLOSED            (evidencia que delimita F-C)
OD-1      = RESOLVED          (este acto)
OD-2/OD-6 = CLOSED · OD-4/OD-7 = ALREADY_CLOSED
F-C       = SCOPED · NOT IMPLEMENTED · ejecución NO autorizada
Etapa B   = delimitada dentro de F-C (no existe como iniciativa paralela)
```

## Criterios de cierre requeridos del Change de `F-C`

*Establecidos por este acto como contenido obligatorio del Plan que ejecute `F-C`. Son criterios de la futura implementación, no trabajo de este Change.*

- [ ] **`FC-1` Actor real.** Ejecución efectiva del bucle con **provider/modelo** inyectado, manteniendo intacta la frontera de `F-A`/`F-B` (efectos admitidos **antes** de delegar; derivación de autoridad antes de la delegación).
- [ ] **`FC-2` Aislamiento.** Aislamiento/sandbox con garantía demostrada **o** declaración explícita, verificable y publicada de la garantía que **no** se ofrece (`AE-7`: el invoker inyectado no es garantía de aislamiento).
- [ ] **`FC-3` Memory como contexto.** Integración de Memory **sin** convertirla en premisa de derivación ni en autoridad (`AE-8`).
- [ ] **`FC-4` Objetivo multi-Change.** Mecanismo/trigger explícito para un objetivo que abarque más de un Change (`D-1`), preservando que la unidad primaria de aceptación sigue siendo el **Change**.
- [ ] **`FC-5` Contención de autoridad fuera del host.** Que la frontera no dependa de que el actor inyectado sea benigno (`C-02`).
- [ ] **`FC-6` Recuperación con fallos reales.** Recuperación/reintento ante fallos reales del actor, resolviendo la **discrepancia declarada** sobre el retry (la política lo nombra; el código no lo implementa) (`C-26`).
- [ ] **`FC-7` Falsaciones ejecutables.** Una falsación por garantía afirmada, verde, y batería canónica sin regresión de `F-A`/`F-B`.
- [ ] **`FC-8` Alcance respetado.** 0 incorporación de `C-16`/`C-17`/`C-21` y de cualquier capacidad fuera de `IN SCOPE`; 0 diff en `protocol/.agents/` salvo RFC-56 Clase A autorizada.
- [ ] **`FC-9` Cierre anclado.** `## Validation anchor` + `## Checkpoint / cierre`, condición derivada `Closed` y reconciliación de `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`.
- [ ] **`FC-10` Prohibiciones preservadas.** `--sae` opt-in sin cambio; techo de recurso como terminación, nunca autorización; envelope de `F-B` sin modificación; superficie de derivación parcial sin crear.

**Change Level mínimo esperado del Change de `F-C`:** **`L3`** (`architectural impact = 3`, `scope = 3`, `duration/complexity = 3`); el Plan de `F-C` lo computa en su intake (RFC-75 Mecanismo 2) y no puede declararlo menor sin justificación.

**Estado correcto del trabajo de `F-C`:** **`SCOPED`** — alcance canónico resuelto y **ejecución no autorizada**. Su Plan de ejecución se crea **sólo** con el acto que lo autorice (pending decision en `### Pending decisions`). No se registra como `Aprobado para ejecución`: ese estado es el marcador de la autorización de ejecución y no fue otorgado por este acto.

## Entregables

1. `docs/plans/163-acto-autoridad-od1-alcance-f-c.md` (**este archivo**) — registro del acto.
2. `docs/CONVENTIONS.md` — subsección aditiva **«Modelo de autonomía — alcance canónico de `F-C` (acto del 2026-10-12)»**.
3. `ROADMAP.md` — reconciliación del mapa: `F-C` con alcance resuelto y sin autorización de ejecución en `NEXT`; las brechas del payload explícitamente fuera de `F-C`; fila de blockers actualizada; grafo de dependencias alineado.
4. `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` — anotación **aditiva** de la resolución de la pending `OD-1` (el artefacto que la posee, regla `PC-1`).
5. `docs/plans/INDEX.md` — serie **Nonagésima segunda**, fila del Plan 163 y encabezado de estado.
6. `CHANGELOG.md` — ítem `[Unreleased]` del Change.

## Pasos

1. **Paso 0 — preflight.** Baseline, dependencias y baseline de checkers.
2. **Paso 1 — registrar el acto.** Fijar en este Plan la decisión, la autoridad, la fecha, el rationale, la evidencia y el registro normativo elegido.
3. **Paso 2 — registrar la norma.** Agregar la subsección aditiva en `docs/CONVENTIONS.md`: interpretación adoptada, definición, relación `F-C` ↔ Etapa B, boundary con `F-A` y `F-B`, `IN SCOPE`/`OUT OF SCOPE`, lo que no debe inferirse y las dependencias.
4. **Paso 3 — preparar el trabajo futuro.** Registrar los criterios de cierre requeridos (`FC-1`…`FC-10`), el Change Level mínimo esperado y el estado correcto (`SCOPED`, sin autorización de ejecución) como pending decision con owner.
5. **Paso 4 — reconciliar.** `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` y la anotación aditiva de la pending `OD-1` en `<PLAN-161>`.
6. **Paso 5 — verificar.** Batería canónica, gates C-1/C-2/C-3, coherencia de las menciones a `F-C`/Etapa B/`OD-1` (sin contradicciones) y verificación de scope.
7. **Paso 6 — cerrar.** `## Validation anchor`, `## Checkpoint / cierre`, nota de ejecución y commit atómico.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | Este Change no produce efectos fuera de la frontera inmediata: escribe únicamente paths locales dentro de su `Scope` declarado y no ejecuta red, git remoto, instalaciones ni cambios destructivos. | — (declaración negativa; no requiere autorización de efecto) | `authorized` |

## Criterios de salida

- [x] El acto está registrado con decisión, autoridad, fecha, rationale, evidencia y registro normativo.
- [x] La definición canónica de `F-C` está en `docs/CONVENTIONS.md` y es **no ambigua**: interpretación, definición, relación con Etapa B, boundary con `F-A` y `F-B`, dentro, fuera, lo que no debe inferirse y dependencias.
- [x] `OD-1` queda **`RESOLVED`** y su pending en `<PLAN-161>` anotada de forma aditiva; `PC-1` preservado (la decisión persiste en el artefacto que la posee).
- [x] El trabajo futuro queda **preparado y no autorizado**: `FC-1`…`FC-10` registrados, Change Level mínimo esperado `L3`, estado `SCOPED` y pending decision bloqueante para la autorización de ejecución.
- [x] **Nada implementado**: 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`; sin Plan de `F-C` autorizado; `F-C = NOT_IMPLEMENTED`.
- [x] Envelope de `F-B`, techos de recurso, vocabulario de efectos y default de `--sae` **sin cambio**.
- [x] Coherencia de menciones: ninguna fuente viva presenta `F-C` como iniciada o autorizada, ni Etapa B como iniciativa paralela vigente.
- [x] Batería canónica en verde (con el rojo preexistente declarado) y sin aumento de citas rotas.
- [x] `## Validation anchor` y `## Checkpoint / cierre` registrados; condición derivada evaluada.

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

Verificación factual adicional: coherencia de las menciones a `F-C`, Etapa B y `OD-1` en las fuentes vivas (grep dirigido, sin contradicciones); `git diff --name-only HEAD` ⊆ `Scope`; 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`.

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** las cinco rutas que la identidad de contenido mide — `CHANGELOG.md`, `ROADMAP.md`, `docs/CONVENTIONS.md`, `docs/plans/INDEX.md` y `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md`. Queda fuera del scope **medido** la governance del propio Change (este artefacto), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 149/155–162). El scope autorizado por `P-8` tiene una ruta más: este artefacto.
- **Validation command-set:** los siete comandos de `docs/VERSIONING.md` §4.1 + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + la verificación factual del Change: coherencia de las menciones vivas a `F-C`, Etapa B y `OD-1` (sin contradicciones materiales), confirmación de que `F-A`/`F-B`/Etapa A permanecen `Closed` y verificación de scope.
- **Effective inputs (repo content):** el scope declarado; el instrumento del Plan 162; la pending `OD-1` del Plan 161 (anotada); la matriz de Etapa A (`docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`); `docs/adr/19-autonomy-envelope-authority.md` y `docs/adr/16-change-lifecycle-authority.md`; el corpus completo de `docs/plans/`, `docs/rfc/` y `docs/adr/` como población de `check_plan_citations` y de C-1/C-2/C-3; el payload de `protocol/.agents/` (216 archivos, 10457 referencias) como entrada de `check_protocol_invariants`; y el estado Git de `dev`.
- **Observed dependencies:** stdlib únicamente; el CLI `git`; `pytest` con basetemp externo al repositorio (`tests/pytest_isolation.py`). Sin red.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.3; `pytest` 9.0.3; repositorio bajo OneDrive. **Clase ambiental declarada:** `check_dist_sync.py` **no** aplica (local-only, verde sólo en `master`); `check_plan_citations.py` sigue rojo por las **26** citas rotas históricas, **sin aumento**. No se consumió red, provider ni credenciales.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `c7f6736f539257f58145ba8dc6175c9852c63bdb` — tree id del índice staged del scope medido (`tools/scoped_content_identity.py`, source `staged`), computado antes de escribir los registros de cierre.
  - **Delta scoped identity (scope S = las cinco rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `c10d620f0b24f2b5c4faa4387953473bdcf934b86ea71d3a128d5c55badd23c0`.
  - **Scope set (repo-relative paths, ordenados):** `CHANGELOG.md`, `ROADMAP.md`, `docs/CONVENTIONS.md`, `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md`, `docs/plans/INDEX.md`
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): **PASS** (216 archivos, 10457 referencias); verification-02 (`check_plan_citations`): **FAIL preexistente** — 26 citas rotas, sin aumento; verification-03 (`check_plan_structure`): **PASS**; verification-04 (`check_taxonomy_coherence`): **PASS**; verification-05 (`check_session_artifacts`): **PASS**; verification-06 (`check_version_state`): **PASS**; verification-07 (`python -m pytest tests/`): **PASS** — `1316 passed` en 375,07 s; verification-08 (C-1): **ANOMALY=0**; verification-09 (C-2): **ANOMALY=0**; verification-10 (C-3): **GAP=0**, `ANOMALY=0`. Verificación factual: `OD-1` resuelto y registrado; ninguna fuente viva presenta `F-C` como iniciada o autorizada ni Etapa B como iniciativa paralela vigente; las entradas históricas que describen `OD-1` como abierto se conservan como traza (RFC-46); `git diff --name-only` ⊆ el scope de `P-8`; **0 diff** en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio del mantenedor: `docs(governance): resolve OD-1 with the canonical scope of F-C (plan 163)`. Se identifica por su mensaje (convención anti-circularidad). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `c7f6736f539257f58145ba8dc6175c9852c63bdb`, delta scoped identity `c10d620f0b24f2b5c4faa4387953473bdcf934b86ea71d3a128d5c55badd23c0`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `c10d620f0b24f2b5c4faa4387953473bdcf934b86ea71d3a128d5c55badd23c0` / `c7f6736f539257f58145ba8dc6175c9852c63bdb`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de cierre incluye la governance del Change (este artefacto), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); C-2 clasificó el corpus sin `ANOMALY`.
- **Governance aplicada:** `docs/CONVENTIONS.md` (subsección aditiva del alcance canónico de `F-C`, preservando las subsecciones previas); `ROADMAP.md` (reconciliación del mapa: `F-C` con alcance resuelto y sin autorización en `NEXT`, brechas del payload explícitamente fuera en `LATER`, grafo de dependencias alineado y blocker de ejecución no autorizada); `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` (anotación **aditiva** de la resolución de `OD-1`, regla `PC-1`); `docs/plans/INDEX.md` (encabezado de estado y serie **Nonagésima segunda** + fila); `CHANGELOG.md` `[Unreleased]`; `**Status:** Executed`. Sin RFC-56 (0 diff en `protocol/`), sin ADR nuevo (el acto resolvió `Q-d = No`), sin `VERSION` bump ni tag.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados y su aspecto: `docs/CONVENTIONS.md` (aspecto: el alcance canónico de `F-C` no existía como norma, de modo que un futuro agente habría tenido que reinterpretarlo; actualización: subsección aditiva con interpretación, definición, relación con Etapa B, boundaries, `IN SCOPE`/`OUT OF SCOPE`, lo que no debe inferirse y dependencias; evidencia: el diff y la verificación de citas). `ROADMAP.md` (aspecto: el mapa situaba `OD-1` como blocker abierto y a Etapa B como iniciativa `LATER` paralela; actualización: `F-C` en `NEXT` con su alcance y sin autorización de ejecución, brechas del payload en `LATER` explícitamente fuera, grafo de dependencias alineado y blocker de ejecución no autorizada; evidencia: el diff y el conteo de líneas del presupuesto visual). `docs/plans/161-…md` (aspecto: su pending `OD-1` quedaba `PENDING` aunque la decisión ya existía; actualización: anotación aditiva de la resolución preservando el texto original; evidencia: el diff). `docs/plans/INDEX.md` y `CHANGELOG.md` por el registro del Change. **No** se actualiza ningún documento histórico (RFC-46): los Planes 149/151–162, ADR-19 y las entradas previas del `CONVENTIONS` quedan intactos.
- **Roadmap impact:** `REQUIRED` — reconciliado en el artefacto que posee el estado. Ítems afectados: `OD-1` **se resuelve** (su fila de blocker se retira); **`F-C` entra en `NEXT`** con alcance canónico resuelto y **sin** autorización de ejecución, con fila de blocker propia; la línea `LATER` «Complete ARgentOS Autonomy (Etapa B)» se retira —`F-C` es esa iniciativa, delimitada— y en su lugar se registran las brechas de capacidad del payload (`C-16`/`C-17`/`C-21`) **explícitamente fuera de `F-C`**; el grafo de dependencias pasa a `A → F-C ← E` y `F-C → Etapa C`. `NOW` no cambia. No se autoriza ninguna etapa desde este Change.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Correcciones

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Pending decisions

- `<PLAN-163>` — decisión: **autorización de ejecución del Change de `F-C`** (crear su Plan desde `docs/plans/_TEMPLATE.md` con `Status: Aprobado para ejecución`, alcance derivado de `IN SCOPE`, criterios `FC-1`…`FC-10` y `Change Level ≥ L3`); blocking: **sí** para iniciar `F-C`; **no** para el resto del repositorio; owner: **mantenedor**; escalación: acto explícito registrado en ese Plan; resolución: **`PENDING_AUTHORITY`** — el acto del 2026-10-12 resolvió el **alcance** y **no** la ejecución, y este Plan **no** la autoriza por inferencia; evidencia: el acto registrado arriba y `docs/CONVENTIONS.md` (subsección «Modelo de autonomía — alcance canónico de `F-C` (acto del 2026-10-12)»); efecto downstream: habilita la implementación de `F-C` bajo su propio Plan; ADR-worthiness: **resuelta por el acto** (`Q-d = No`).

## Riesgos

1. **Convertir el alcance resuelto en autorización de ejecución.** Mitigación: estado `SCOPED` explícito; pending decision bloqueante para la autorización; ningún Plan de `F-C` creado; `OUT OF SCOPE` ítem 2.
2. **Scope creep hacia las brechas del payload.** Mitigación: `C-16`/`C-17`/`C-21` declaradas **fuera** de `F-C` en la norma y en el mapa; `FC-8`.
3. **Leer `F-C` como autorización de Etapa B.** Mitigación: la norma declara la relación `F-C` ↔ Etapa B sin ambigüedad (delimitada, no paralela) y `## Qué NO debe inferirse`.
4. **Alterar el envelope o los defaults de autonomía al registrar el alcance.** Mitigación: `OUT OF SCOPE` ítem 4 y criterio `FC-10`; ADR-19 y `docs/CONVENTIONS.md` (subsecciones previas) se preservan íntegros.
5. **Reescribir historia.** Mitigación: la subsección de `CONVENTIONS` es **aditiva**; la anotación en `<PLAN-161>` es aditiva y preserva el texto original; no se tocan ADRs, RFCs ni planes cerrados salvo esa anotación exigida por `PC-1`.

## Trazabilidad

```text
Etapa A (Plan 161, Closed) → matriz de 28 capacidades (evidencia)
        │
        ▼
Plan 162 (instrumento decision-ready, Closed) → Q-a…Q-d sin decidir
        │
        ▼
ACTO DEL MANTENEDOR (2026-10-12) → Q-a = B · Q-d = No ADR
        │
        ▼
Plan 163 → CONVENTIONS (alcance canónico de F-C) · ROADMAP · INDEX · CHANGELOG
        │
        ▼
OD-1 = RESOLVED  →  pending: autorización de ejecución de F-C
        │
        ▼
Change de F-C (con su propia autorización)  →  Etapa C
```

## Nota de ejecución

*2026-10-12. Ejecutado en `dev` @ `5dc2e72` (baseline del preflight: worktree limpio; `dev` ahead 14 de `origin/dev`; `VERSION` del payload `12.0.1` sin tag; batería canónica en verde).*

Una sola pasada, en el orden del `## Pasos`:

1. **Paso 0 — preflight.** Baseline, dependencias (`F-A`/`F-B`/Etapa A `Closed`; `OD-1` pendiente con owner mantenedor) y baseline de citas rotas registrado (**26**).
2. **Paso 1 — acto registrado.** Fijados decisión (`OD-1`), autoridad (mantenedor), fecha (2026-10-12), rationale, evidencia y registro normativo elegido (`Q-d = No` ADR).
3. **Paso 2 — norma registrada.** Subsección **aditiva** «Modelo de autonomía — alcance canónico de `F-C` (acto del 2026-10-12)» en `docs/CONVENTIONS.md`: interpretación adoptada (`B`), definición, relación `F-C` ↔ Etapa B, boundary con `F-A` y `F-B`, `IN SCOPE`/`OUT OF SCOPE`, lo que no debe inferirse y dependencias. Las subsecciones del 2026-10-07 y del 2026-10-11 quedan intactas.
4. **Paso 3 — trabajo futuro preparado, no ejecutado.** Registrados `FC-1`…`FC-10`, el `Change Level` mínimo esperado (`L3`) y el estado **`SCOPED`**, con pending decision **bloqueante** para la autorización de ejecución.
5. **Paso 4 — reconciliación.** `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` y la anotación **aditiva** de la resolución de `OD-1` en `<PLAN-161>` (artefacto que posee la pending, regla `PC-1`).
6. **Paso 5 — verificación.** Batería canónica (`1316 passed`), seis checkers en verde con **26** citas rotas (baseline), gates C-1/C-2/C-3 sin `ANOMALY`, coherencia de las menciones a `F-C`/Etapa B/`OD-1` y verificación de scope (0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`).
7. **Paso 6 — cierre.** `## Validation anchor` A1, `## Checkpoint / cierre`, esta nota y commit atómico.

**Resultado.** `OD-1` **resuelto**: `F-C` es la iniciativa «Complete ARgentOS Autonomy» (Etapa B) **delimitada por el resultado de la Etapa A a la frontera de autonomía**, con registro normativo aditivo y **sin ADR**; `OD-1` deja de bloquear y el alcance canónico queda en `docs/CONVENTIONS.md`. **Nada implementado:** no se creó ni autorizó un Plan de `F-C`, no se inició Etapa B y no se tocó `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` ni `dist/`. No hubo findings: los checkers y los gates quedaron verdes en la primera pasada.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1).
Committed = TRUE  — commit atómico en `dev`, identificado por su mensaje.
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump, sin tag, sin promoción a `master`, sin `dist`.
```

`OD-1 = RESOLVED` · `F-C = SCOPED` (alcance canónico; ejecución **no** autorizada) · `F-C = NOT_IMPLEMENTED` · `Etapa B` delimitada dentro de `F-C`.

**Próximo paso exacto.** El mantenedor autoriza la **ejecución** de `F-C` creando su Plan desde `docs/plans/_TEMPLATE.md` con `Status: Aprobado para ejecución`, alcance derivado de `IN SCOPE`, criterios `FC-1`…`FC-10` y `Change Level ≥ L3` (`### Pending decisions`); sólo entonces comienza la implementación.
