# Investigación Arquitectónica Integral — Modelo Operativo, Gobernanza, Conocimiento y Autonomía

**Clase documental:** Working / Research (provenance) — **no normativo** (`docs/AGENTS.md:Folder → class map`; `docs/placement-contract.md:6. Namespace selection`, familia `Working analysis` → `docs/working/{audits,research,proposals}/`).
**Naturaleza:** investigación `READ_ONLY` respecto del sistema. **Autoridad de este documento:** ninguna. Registra hallazgos, evidencia e hipótesis evaluadas; no crea mecanismos, no modifica arquitectura, no autoriza trabajo y **no resuelve ninguna decisión**.
**Fecha:** 2026-09-22
**Baseline:** `dev` @ `820da21` (`docs(roadmap): declare the capability and autonomy roadmap A-B-C (plan 149)`); `protocol/.agents/VERSION` = `11.6.2`; `docs/VERSIONING.md:9. Estado actual` vigente.
**Estado Git al iniciar:** `git status --short --branch` → `## dev...origin/dev [ahead 1]`; dos rutas untracked **preexistentes y ajenas** a esta investigación: `MASTER_PENDING_WORK_INVENTORY.md` y `docs/architecture-capability-review.md`.
**Alcance de escritura:** esta investigación escribió **un único archivo**, este documento. No modificó código, políticas, contratos, Placement Contract, RFCs, ADRs, planes, ROADMAP, CHANGELOG, VERSION, INDEX, tests, CI ni el payload; no archivó, movió ni reorganizó nada; no creó commits, tags, releases ni push; no cerró findings ni convirtió hipótesis en decisiones.

---

## Leyenda de clasificación (obligatoria)

Cada hallazgo relevante lleva exactamente una etiqueta:

| Etiqueta | Significado |
|---|---|
| `FACT` | Hecho verificado por lectura directa o por conteo mecánico reproducible; no expresa intención ni norma. |
| `IMPLEMENTED` | El mecanismo existe y **lo hace cumplir código** (checker, resolutor, host, validador, gate) — verificado en el artefacto que lo ejecuta. |
| `PARTIALLY_IMPLEMENTED` | Existe una parte mecánica y otra que depende de prosa, juicio o disciplina humana; la frontera entre ambas está identificada. |
| `DOCUMENTED_ONLY` | Existe como texto normativo, política, rol, contrato en prosa o instrucción de prompt; **ningún ejecutor lo verifica**. |
| `GAP` | Ausencia de mecanismo, de representación o de información. No es un defecto demostrado por sí mismo: es una capacidad faltante con impacto declarado. |
| `CONTRADICTION` | Dos fuentes del repositorio —o una fuente y el estado real— afirman cosas incompatibles. |
| `HYPOTHESIS` | Afirmación evaluada en esta investigación, con el veredicto que la evidencia permite. |
| `DESIGN_OPTION` | Alternativa de diseño evaluada; **no** es una recomendación aceptada ni una regla. |
| `HUMAN_DECISION_REQUIRED` | Conflicto o elección que esta investigación **no** resuelve por inferencia y que requiere autoridad humana. |

Regla de honestidad aplicada en todo el documento: **una hipótesis no se convierte en decisión, y una recomendación no se convierte en regla normativa.** Donde la evidencia no alcanza, se declara la incertidumbre y se escala.

---

## 1. Executive Summary

**Respuesta a la pregunta central.** ARgentOS ya posee el modelo de autoridad, el modelo de incertidumbre y el modelo de evidencia que la pregunta supone, y los tiene en un grado poco común: la frontera humana es explícita, el conflicto normativo **no se resuelve por precedencia inventada**, la evidencia faltante (`GAP`) no se confunde con contradicción (`ANOMALY`), y la autonomía está declarada como `autonomy ⊆ authorized scope ∩ granted authority`. Lo que **no** posee es la capacidad de **derivar**, a partir de una intención acotada, las tres cosas que hoy el humano escribe a mano: **(i) qué trabajo es** (kind), **(ii) qué conocimiento del repositorio es vigente**, y **(iii) qué obligaciones le aplican**. Sin esas tres derivaciones, un prompt como «Implementá X» no puede iniciar trabajo legítimo, no porque falte ejecutor, sino porque el sistema no puede construir la autorización que necesita.

1. **`FACT` — El cuello de botella de la concisión no está en el ejecutor, está en la derivación y en el intake.** La revisión de capacidad existente (`docs/architecture-capability-review.md`) identificó dos fronteras del *ejecutor* (`PR-1` admisión de efectos; `PR-2` presupuesto de recurso) y concluyó, con evidencia, que el modelo de autonomía es internamente completo. Esta investigación **confirma esa conclusión y la desplaza**: las fronteras que impiden la intención concisa son anteriores al ejecutor — son de **derivación** (qué reglas aplican, qué conocimiento rige, qué tipo de trabajo es) y de **autorización** (el intake exige un Plan aprobado por un humano, y hoy el Plan es un documento que se escribe a mano).

2. **`FACT` — Todo cambio no mecánico requiere autorización humana previa, y esa autorización es un artefacto redactado.** `.agents/workflows/change-lifecycle.md:2. Authorization gate` es determinista: sin Plan `Aprobado para ejecución` (o RFC `Accepted` para payload, `docs/rfc/56-governance-fast-track.md:Decisión propuesta`), el agente **STOP**ea y *propone* el plan; nunca lo crea ni lo ejecuta. Las únicas vías sin plan son Clase C (corrección mecánica, «cero cambio de significado») y el nivel L0 (`docs/plans/94-change-lifecycle-master-action-plan.md:9.2 Matriz operacional L0–L3`, «Mínima: clasificación en el primer artifact; **sin Plan obligatorio**»), ambos acotados a un archivo y sin cambio estructural ni de versión.

3. **`FACT` — El propio estándar que decide «preguntar o avanzar» mide la forma del prompt, no la derivabilidad del faltante.** `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md` puntúa cuatro criterios positivos y cuatro negativos **sobre el texto del pedido** (tecnología nombrada, verbo de acción, entidad, criterio de éxito) y mapea `score < 6` a `CONFIRMING_INTENT`. Un pedido «Implementá X» obtiene, en el mejor caso, `+2` (verbo) `+2` (entidad) = `4` → `MEDIUM` → **confirmación obligatoria**, aunque `X` esté inequívocamente determinado por contratos, políticas y estado del repositorio. El estándar no pregunta «¿puedo derivarlo?», pregunta «¿el humano lo escribió?». `FACT`/`GAP`.

4. **`HYPOTHESIS` evaluada — «Un prompt como *Implementá X* podría ser suficiente cuando X está inequívocamente determinado por el contexto y la autoridad disponible»: parcialmente verdadera, y hoy no ejecutable.** Verdadera en el plano conceptual: el repositorio sí contiene, para una clase acotada de cambios, todo lo necesario para derivar objetivo, alcance, obligaciones y verificación (Clase C/L0; o un cambio cuyo Plan ya existe y está aprobado). Falsa en el plano operativo por **cuatro razones independientes y verificadas**: (a) el intake exige un Plan que ningún mecanismo deriva; (b) `INTENT_CONFIDENCE` bloquea por forma del prompt; (c) no existe taxonomía de *tipo de trabajo* (verificado: **0 coincidencias** de `work_type`/`work-type`/`tipo de trabajo` en todo el repositorio), de modo que el conjunto de artefactos y gates obligatorios no se deriva del contenido; (d) la vigencia del conocimiento no es legible: **149 de 149 planes numerados están `Executed` y 80 de 80 RFCs están `Accepted`** (conteo mecánico, §7), de modo que ningún campo de estado distingue conocimiento vigente de histórico.

5. **`IMPLEMENTED` — La regla de incertidumbre que la investigación propone como hipótesis ya existe, y está mejor formulada que la hipótesis.** «Cuando las reglas no determinan legítimamente la acción, escalar en lugar de inventar precedencia» está implementada explícitamente en **cinco** lugares independientes: `.agents/policies/authority.md:Conflict protocol` («RFC vs ADR disagreement: **no automatic winner**; governance anomaly → escalate»), `docs/rfc/75-change-lifecycle.md:Mecanismo 10 — Authority / Conflict Resolution` («Sin jerarquía universal RFC > ADR > Plan > Git»), `.agents/policies/supervised-autonomous-execution.md:§5` («conflict between normative sources | no source wins automatically»), `docs/placement-contract.md:PC-22/PC-23` («**GUESS is never a valid outcome**») y, en el Protocol, `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md` + `standards/context/RESOLUTION_UNRESOLVABLE_CONFLICTS.md` («the Orchestrator must not guess») + `standards/orchestration/DECISIONS.md:D3` («biases toward `NEEDS_CLARIFICATION` whenever proceeding would require assuming»). La hipótesis queda **confirmada como regla existente**, con una precisión: el repositorio no necesita la regla, necesita que la regla **no sea la única respuesta** — hoy escala tanto la incertidumbre legítima como la certeza derivable.

6. **`PARTIALLY_IMPLEMENTED` — El caso de estudio (el Change que produjo `docs/architecture-capability-review.md`, en adelante «el caso del review») confirma el modelo y expone su límite exacto.** El review registra que su ubicación fue fijada por instrucción explícita del mantenedor, que esa ruta **no** es la que el contrato de placement habría resuelto para su clase (`Working analysis` → `docs/working/...`), que `docs/architecture/` está declarado `archived`, y que la divergencia se **registra y no se resuelve por reinterpretación** (`PC-75`), con `PC-75` como pending decision y `REQUIRES_HUMAN_DECISION` explícito para su registro en gobernanza. Es decir: **la frontera funcionó** (no hubo inferencia), y por eso mismo el artefacto quedó fuera de toda estructura de registro: no hay Plan 150, no hay fila en `docs/plans/INDEX.md`, no hay entrada de changelog, y el archivo está **untracked**. Un conflicto legítimo produjo conocimiento legítimo **sin hogar de gobernanza**. No fue un error del agente; fue un límite del modelo.

7. **`GAP` — La excepción legítima no es descubrible.** `docs/placement-contract.md:PC-31a/PC-31b` declara las excepciones **documentales por defecto** y exige que el agente las *localice*, *verifique el owner*, las *interprete* y las *aplique* — o STOP. El mismo contrato declara (`PC-27`) que la excepción «MUST ... be recorded in the artifact that already owns the decision ... **not** in a central store». La consecuencia verificable es que la excepción del review vive **dentro del artefacto que la necesita**, y un agente que mañana deba resolver la ubicación de otro artefacto de la misma clase no tiene forma de encontrarla. Es una decisión de diseño declarada (`PC-31c`: la machine-locatability «is **not prohibited**; it is simply not decided in favour of here»); esta investigación **no la reabre**: la registra como límite con evidencia de primera mano.

8. **`CONTRADICTION` — El estado de los artefactos de gobernanza no codifica vigencia, pero la gobernanza razona como si lo hiciera.** Los ciclos de estado existen y son correctos (`docs/CONVENTIONS.md:Convenciones`: RFC `Proposal → Accepted → Superseded`; ADR ídem; Plan `Aprobado para redacción | Aprobado para ejecución | Executed | Executed (parcial) | Superseded`), pero en la práctica **no se usan**: 80/80 RFCs `Accepted`, 0 `Superseded`; 149/149 planes `Executed`, 0 `Superseded`, 0 `Aprobado *`. La supersesión real del corpus se registra en **prosa** (banners «⚠ Enmienda pendiente», `## Amendment Log`, «superado por RFC-68») y en campos de *pending decisions*. Y hay un caso peor: **retirar** un plan no es representable — `Superseded` «exige indicar el plan reemplazante», y cuando no existe ninguno, el ciclo no ofrece salida (registrado de forma independiente en `docs/plans/INDEX.md` fila del plan 88, `docs/plans/137-ears-structural-validator.md`, `docs/plans/140-governance-residual-closure.md` y `MASTER_PENDING_WORK_INVENTORY.md:HD-1`). La documentación de estado existe; el estado real del corpus no la obedece.

9. **`CONTRADICTION` — El mismo INDEX es simultáneamente documentación de estado actual e historia congelada.** `.agents/policies/validation-closure.md:5.1` enumera `docs/plans/INDEX.md` entre los documentos de **estado actual** que deben permanecer correctos; `docs/AGENTS.md:Folder → class map` y `docs/rfc/46-historical-trace-policy.md` tratan los planes cerrados como **traza histórica que no se actualiza**. El INDEX es, al mismo tiempo, espejo mecánico del corpus histórico y fuente de navegación de estado actual — y `MASTER_PENDING_WORK_INVENTORY.md:§7` documenta **más de veinte filas stale** detectadas por lectura cruzada, con la batería en verde. La consecuencia arquitectónica es precisa: **el espejo se verifica por forma, no por verdad.**

10. **`GAP` — No hay detección de obsolescencia; hay determinación de obligaciones.** ARgentOS tiene dos determinaciones de cierre (`Documentation impact`, `Roadmap impact`), ambas declaradas de gobernanza y **sin checker semántico** por decisión explícita (`validation-closure.md:5.1/5.2`, «no checker interprets prose or decides whether a document is up to date, and no checker is added for this»). Lo que no tiene es el paso anterior: **detectar** qué conocimiento quedó afectado. Ese paso **ya está diseñado y explícitamente diferido** dentro de ARgentOS: `docs/rfc/68-architecture-evolution-workflow.md:Phase 2 — Deferred` nombra «**Propagación mecánica de impacto** (delta engine sobre el índice de trazabilidad)» con gates de entrada declarados (telemetría P0, índice de trazabilidad verde sobre sesiones reales, correlación validada sobre ≥2 conjuntos multi-proyecto). Es decir: la pregunta «¿necesita ARgentOS un mecanismo general de impacto/reconciliación?» **ya fue respondida «sí» por RFC-68 y su implementación ya fue diferida con criterio**. La investigación aporta la lectura de que esa respuesta **no** colisiona con `Documentation/Roadmap impact`, porque son operaciones distintas (detectar ≠ determinar ≠ escribir).

11. **`FACT` — El inventario más completo de trabajo pendiente del repositorio vive fuera del repositorio.** `MASTER_PENDING_WORK_INVENTORY.md` (untracked, declarado «external deliverable, not a repository artifact») contiene 2 ítems `ACTIONABLE NOW`, 12 decisiones humanas, 22 diferidos, 26 registros colapsados y 21 contradicciones documentales, muchas de ellas **invisibles para la herramienta del repositorio** con la batería en verde (su propia §9 lo dice: «the four most consequential defects ... were found by cross-reading the repository, **not** by its own tooling»). Para la pregunta central esto es evidencia directa: ARgentOS **no puede responder por sí mismo** «¿qué está pendiente?» ni «¿qué sigue vigente?».

12. **`DESIGN_OPTION` (recomendación principal, sujeta a decisión humana).** El modelo futuro no necesita entidades nuevas; necesita **tres derivaciones explícitas y una frontera**: (a) una **resolución de reglas aplicables** con el mismo patrón que ya funciona para placement (`PLACE | STOP` determinista, `docs/placement-contract.md:PC-21/PC-22`, materializado en `runtime/placement/resolver.py`), extendida de «dónde va» a «qué obliga»; (b) una **declaración de tipo de trabajo** por Change/Plan, derivada del contenido y de la autoridad, que seleccione el conjunto de artefactos y gates obligatorios — el patrón ya existe en el Protocol (`AGENT_STATE_MACHINE.md:Task Profiles`) y en DEV (`Change Level`) pero **no** existe como tipo de trabajo; (c) una **vigencia declarada** por artefacto usando el vocabulario que ARgentOS **ya declaró** (`docs/AGENTS.md:Lifecycle`: `active`/`archived`/`superseded`/`deprecated`) y que hoy ninguna cabecera escribe; (d) la **frontera de autorización del intake** tratada explícitamente: hoy derivar la intención no alcanza para ejecutar, porque ejecutar requiere un Plan aprobado — y ese es el punto donde la concisión del prompt se gana o se pierde.

13. **`HUMAN_DECISION_REQUIRED`.** Esta investigación no resuelve, entre otras: si el vocabulario de vigencia de `docs/AGENTS.md` se materializa en cabeceras; si el ciclo de planes gana una salida para trabajo retirado o abandonado; si el corpus histórico (149 planes + 80 RFCs + 19 ADRs) se clasifica por vigencia o se deja como está; si `INTENT_CONFIDENCE` se rebasa sobre derivabilidad; si se autoriza la Fase 2 de RFC-68; y cómo se registra en gobernanza el Change del review (y esta investigación). Detalle en §15.

---

## 2. Current Model

### 2.1 Las tres capas y su frontera

`FACT` (`AGENTS.md:Repository layout`; `docs/AGENTS.md:Naturaleza documental`; `docs/placement-contract.md:3. Domain / owner identification`):

| Capa | Qué es | Autoridad de cambio | Dónde vive |
|---|---|---|---|
| **DEV** | la gobernanza, operación, verificación, runtime, tests e historia **de este repositorio** | un Change DEV (plan / lifecycle RFC-75) | `docs/`, `.agents/`, `tools/`, `runtime/`, `tests/`, raíz |
| **Protocol** | el payload distribuido a adoptantes | RFC-56 (`docs/rfc/56-governance-fast-track.md`) | `protocol/.agents/` + `protocol/_AGENTS.md` |
| **Git** | el hecho de lo que ocurrió | no aplica (es factual) | ramas `dev`/`master`/`dist`, tags |

`FACT` — La frontera es **dura y deliberada**: `docs/CONVENTIONS.md:Frontera operacional (DEV)` declara que `.agents/` «no crea autoridad normativa nueva, no es fuente superior de verdad y no importa mecanismos del Producto»; `AGENTS.md:Do NOT` prohíbe «share lifecycle machinery between DEV and the Protocol»; `docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera` lo repite («No se crean workflow/policy/state machine/artifact/skill compartidos entre DEV y Protocol; **no hay herencia automática**»). Consecuencia para la pregunta central (`IMPLEMENTED`): **toda derivación de contexto y autoridad debe existir dos veces, una por capa**; no hay un lugar único donde poner «el resolvedor de reglas aplicables».

### 2.2 Modelo de autoridad (DEV)

`IMPLEMENTED`/`DOCUMENTED_ONLY` según columna. Fuente: `.agents/policies/authority.md`; `docs/adr/16-change-lifecycle-authority.md`; `docs/rfc/75-change-lifecycle.md:Mecanismo 10`.

| Clase | Qué es | Quién la produce | Nunca |
|---|---|---|---|
| `FACTUAL` | lo que realmente ocurrió | Git, tests, checkers, tags | significado normativo |
| `NORMATIVE` | lo que debería ser | RFC `Accepted`, ADR, Plan aprobado | auto-resolución de conflictos |
| `DECISION` | autoridad final para resolver conflictos | el mantenedor humano | delegación a inferencia del agente |
| `RELEASE` | estado publicado e inmutable | tags anotados en `master`, `dist` regenerado | edición a mano |
| `DESCRIPTIVE` | vistas/navegación | INDEX | convertirse en autoridad por existir (`AU-4`) |

Cuatro reglas duras que sostienen el modelo (`DOCUMENTED_ONLY`, en prosa, sin enforcement de código):

- un INDEX nunca se vuelve autoridad (`AU-4`): «Verify premises against the artifacts and git, never against INDEX» (`authority.md:16-20`);
- el output de un checker es evidencia factual, nunca autoridad normativa (`authority.md:21-22`; `docs/rfc/75-change-lifecycle.md:Mecanismo 14`);
- un Plan implementa una decisión normativa; **no puede modificarla en silencio** (`AU-5`, `authority.md:23`);
- **un agente nunca convierte su propia inferencia en una decisión humana** (`authority.md:24`; `.agents/AGENTS.md` regla 3).

### 2.3 Change Lifecycle (DEV) — mecanismos existentes

`FACT` (`docs/rfc/75-change-lifecycle.md`; operacionalizado en `.agents/workflows/change-lifecycle.md` y `.agents/policies/*`):

| Mecanismo | Qué resuelve | Estado real |
|---|---|---|
| **1 Intake** | clasificar todo cambio (origen/tipo, clase RFC-56, Change Level, scope, riesgo, coordinación) en el primer artifact o en el mensaje de commit | `PARTIALLY_IMPLEMENTED`: la clasificación es prosa en el Plan; **no existe entidad `Change` ni tracker** («There is no `Change` entity, no global tracker, no intake workflow», `change-lifecycle.md:43-44`) |
| **2 Change Levels** | rigor proporcional al impacto, `Level = max(coordination, scope, architectural impact, release impact, duration/complexity)` | `DOCUMENTED_ONLY`: declarado en el header del Plan; el host DEV **parsea** `change_level` y no lo usa (auditoría de runtime, §3.3) |
| **3 RFC lifecycle** | `Proposal → Accepted → Superseded` + Amendment Log | `PARTIALLY_IMPLEMENTED`: `Superseded` y `Proposal` **no se usan** en el corpus (0/80) |
| **4 ADR integration** | ADR-worthiness (a) consumida fuera de su RFC, (b) supersede/modifica un ADR, (c) invariante persistente | `DOCUMENTED_ONLY`: es juicio humano declarado (`AU-6`) |
| **5 Plan lifecycle** | estados y condiciones derivadas (`Executed` sin commit; `Committed` no es status; `Closed` derivado) | `IMPLEMENTED` en lo verificable: C-1/C-2/C-3 + `derive_next_action` |
| **6 Validation Anchors** | toda validación registrada lleva anchor (scope declarado, command-set, inputs, factores ambientales, Scoped Content Identity, stale) | `IMPLEMENTED`: `tools/check_lifecycle_anchor.py` (C-1), `runtime/orchestrator/governance.py` |
| **7 Git Checkpoints** | relación cierre ↔ estado Git verificable; `A ≠ B` esperado | `IMPLEMENTED`: `tools/check_lifecycle_checkpoint.py` (C-2) |
| **8 Findings/Corrections/Revalidation** | refs calificadas `<artifact>:F-<n>`/`C-<n>`, elemento inmutable, estado evolucionable, N:M | `IMPLEMENTED`: `tools/check_lifecycle_lineage.py` (C-3) |
| **9 Pending Decisions** | decisión pendiente **en el artifact que la posee**; bloqueante nunca desaparece (PC-1) | `PARTIALLY_IMPLEMENTED`: registros en prosa + revisión en C-3; sin entidad |
| **10 Authority/Conflict** | detect → classify → escalate → human decision → correct → revalidate | `DOCUMENTED_ONLY`: el host tiene 3 veredictos y stop conditions, pero **no lee policies ni RFCs** |
| **11 Series/Continuity** | identidad derivada de declaraciones + relaciones verificables; sin registry | `PARTIALLY_IMPLEMENTED`: `Serie:` en headers + filas del INDEX |
| **12 Post-close Changes** | problema posterior al cierre → artifact nuevo que referencia al cerrado | `DOCUMENTED_ONLY` (regla) + `IMPLEMENTED` parcialmente vía `<artifact>:C-<n>` |
| **13 Observability** | métricas del lifecycle (schema baseline) | `DOCUMENTED_ONLY`: «sin backend, sin writer obligatorio, sin thresholds y sin gate de release» (`docs/VERSIONING.md:11`) |
| **14 Automation** | checker output = evidencia factual ≠ autoridad | `IMPLEMENTED` como contrato; la frontera se respeta en el código de los gates |
| **15 Migration/Legacy** | ausencia de campos nuevos = legacy, no invalidez | `IMPLEMENTED` en los tres gates (`EXCLUDED`) |

### 2.4 Condiciones derivadas y su enforcement

`IMPLEMENTED` (`.agents/policies/validation-closure.md:6`; `docs/VERSIONING.md:7`):

```text
Verified   = ∃ validation(PASS, anchor)
Executed   = implementación + validación (status de Plan; legal sin commit)
Committed  = estado del repositorio (commit atómico en dev); NUNCA un status
Closed     = Executed ∧ governance aplicable ∧ ∃ checkpoint ∧ consistencia
             checkpoint↔anchor ∧ evidencia PASS para el estado de cierre  (derivada)
Released   = promovido a master y taggeado (acto del mantenedor)
```

`FACT` — Las cuatro son **condiciones derivadas, no una state machine**, por decisión explícita (ADR-15 rechazó el tri-estado como máquina; `docs/plans/94-change-lifecycle-master-action-plan.md:10`). Esto es relevante para la pregunta central: el sistema **ya sabe derivar** condiciones a partir de hechos — pero lo hace sobre el **cierre**, no sobre la **apertura**. No existe la derivación simétrica «qué trabajo es esto y qué obliga».

### 2.5 Modelo de incertidumbre (Protocol)

`IMPLEMENTED`/`DOCUMENTED_ONLY` según el caso. Fuente: `protocol/.agents/standards/`.

| Pieza | Qué determina | Enforcement |
|---|---|---|
| `requirements/NO_ASSUMPTIONS.md` | **cuándo preguntar**: prohibido asumir tecnología, comportamiento, scope, decisiones de diseño, validación/seguridad/errores, criterios de aceptación, hechos inventados. `MUST` transicionar a `NEEDS_CLARIFICATION` «whenever a missing detail would require the agent to choose between two or more reasonable implementations» | `DOCUMENTED_ONLY` (rol/orquestador lo aplica por juicio; H00/H11 gatean el artefacto, no la decisión) |
| `requirements/INTENT_CONFIDENCE.md` | score `-3..+8` **sobre el texto del prompt**; `>=6` HIGH (confirma opcional), `2..5` MEDIUM, `<2` LOW (confirmación obligatoria) | `DOCUMENTED_ONLY` |
| `quality/CONFIDENCE.md` | modelo general + regla anti-inflación | `DOCUMENTED_ONLY` |
| `context/RESOLUTION_UNRESOLVABLE_CONFLICTS.md` | incompatibilidad / exclusión mutua / conflicto de presupuesto → **detener el ensamblado**, clasificar F3 (ambiguity→clarification), F4 (inconsistency report → documentación), F1 (blocker → recovery) | `DOCUMENTED_ONLY` |
| `orchestration/DECISIONS.md` | D1–D7: aceptación de transición, routing del reviewer, frontera `NEEDS_CLARIFICATION`↔`RECOVERY` (**sesgada a clarificar**), criticidad de KB, autoridad de abort, bootstrap degradado, invocación de deliberación | `DOCUMENTED_ONLY` |
| `conduct/ANTI_CIRCUMVENTION.md` | prohíbe saltar fases, inventar intención del usuario o cumplir en silencio una instrucción que contradice el protocolo | `DOCUMENTED_ONLY` (con detección por parte del Orchestrator) |
| `runtime/AUTHORIZATION.md` | fuera de la frontera: `network`, `remote_git`, `install`, `destructive`, `write_outside_project` requieren `## Effects` con `authorized_by`+`status`; **`AUTHORIZATION_UNDETERMINED` nunca se reporta como `UNAUTHORIZED`** | `DOCUMENTED_ONLY` en el ejecutor DEV (la revisión de capacidad verificó que el runtime **no lee** `## Effects`) |
| `runtime/PROTOCOL_BOUNDARIES.md` | frontera canónica del alcance, tooling, interacción externa, reanudación | `DOCUMENTED_ONLY` + hook gate del payload |
| `harness/gate_validator.py`, `hook_gate.py`, `runner_state.py` | H00–H15 estructuralmente; `state.json`; perfil de tarea | `IMPLEMENTED` (el validador estructural del payload existe desde plan 66/RFC-57 — `MASTER_PENDING_WORK_INVENTORY.md:SUP-1`, verificado por esa investigación en `gate_validator.py:131,218,484-501`) |

**Observación clave para la pregunta central** (`FACT`): el Protocol resolvió el problema «preguntar o avanzar» con un **puntaje sobre el prompt** más un **catálogo de decisiones discrecionales**. Es un modelo de *juicio*, no de *derivación*. `INTENT_CONFIDENCE` es, literalmente, dependencia del prompt **mecanizada**: el sistema decide si necesita al humano midiendo cuánto escribió el humano.

### 2.6 Granularidad: lo que hoy existe

`FACT` — Existen **cinco** ejes de granularidad, ninguno de los cuales es «tipo de trabajo»:

| Eje | Valores | Dónde | Qué selecciona |
|---|---|---|---|
| **Task Profile** (Protocol) | `trivial` / `standard` / `complex` | `AGENT_STATE_MACHINE.md:Task Profiles`; validado por H00 | artefactos y gates obligatorios, y qué estados se recorren (`trivial` salta `CONFIRMING_INTENT`, `BUILDING_TASK_SPECIFICATION`, `TASK_READY`, `GATHERING_CONTEXT`, `VALIDATING_CONTEXT`) |
| **Fase del workflow** (Protocol) | 00–08 (analyze → confirm intent → task spec → gather context → validate context → plan → execute → verify + recovery) | `orchestrators/core/workflow/` | posición en el ciclo; **no** un tipo declarado |
| **RFC-56 class** (DEV, solo payload) | `A` (modelo/contractos → RFC `Accepted`), `B` (mejora documental → plan aprobado), `C` (mecánica → commit directo) | `docs/rfc/56-governance-fast-track.md:Decisión propuesta` | vía de autorización |
| **Change Level** (DEV) | `L0`–`L3` por `max(coordination, scope, architectural impact, release impact, duration/complexity)` | `docs/rfc/75-change-lifecycle.md:Mecanismo 2`; `docs/plans/94-...:9.2` | maquinaria requerida (L0: sin Plan obligatorio; L3: machinery completa) |
| **Plan status** (DEV) | `Aprobado para redacción` (entregables documentales) vs `Aprobado para ejecución` (implementación) vs `Executed`/`Superseded` | `docs/CONVENTIONS.md:Convenciones` | **el único eje que hoy distingue *qué* se está haciendo**, y es binario |

`FACT` — **No existe taxonomía de tipo de trabajo.** Verificación: búsqueda de `work_type`, `work-type`, `tipo de trabajo` sobre todo el repositorio → **0 coincidencias**; búsqueda de `work_type`/`task_type` en `runtime/` → **0 coincidencias**. Los términos `investigation`, `design`, `decision`, `specification`, `implementation`, `verification`, `dogfood`, `documentation`, `release` aparecen como **palabras de prosa** (títulos de planes, secciones de RFC), nunca como enumeración de código o como campo de un artefacto.

`FACT` — «Feature» **no existe como concepto en DEV**. Lo que existe con ese nombre es `protocol/.agents/features.toml`: **flags de capacidad declarativos**, no unidades de trabajo (`docs/architecture-capability-review.md:2.3`). Es una colisión de nombres que conviene registrar: si alguien introduce «Feature» como unidad de trabajo en DEV, el término ya está tomado con otro significado en el payload.

### 2.7 Modelo documental (DEV) y su lifecycle declarado

`FACT` (`docs/AGENTS.md`; `docs/rfc/69-documentation-taxonomy-and-layout.md`):

- **Naturaleza** (rol normativo): `EntryPoint`, `Policy`, `Governance`, `Inventory`, `Working`. `Product` y `Tooling` no son naturalezas: son capas físicas. `Operational` tampoco: `.agents/` es interfaz de operación.
- **Lifecycle** (estados con transiciones, **no** una cadena lineal): `active` → `archived` (congelado con banner; sigue siendo significado histórico) → `superseded` (reemplazado por otro de la misma clase) → `deprecated` (fuera de uso sin reemplazo); pueden coexistir (`superseded ∧ archived`).
- **Identidad**: `RFC-N`, `ADR-N`, `plan NN`, `D#`, `P#`, `CG#`, `RC#` son identidades estables; **identidad ≠ path**. No hay registry global de IDs: los INDEX cumplen el rol de mapa ID → path → status.
- **Referencias** (cinco clases): Normative, Documentary, Provenance/Evidence, Historical, Informational. Solo Normative y Documentary «rompen CI si no resuelven».
- **Canonical ≠ immutable**: canonical = referente normativo para verificación y derivación (puede ser mutable); immutable = traza congelada.

`CONTRADICTION` (parcial) — Este vocabulario de lifecycle **existe y está declarado pero no se escribe en ninguna cabecera de artefacto**. Un `archive` es un banner escrito a mano; un `superseded` es un campo `**Status:**` que el corpus no usa; un `deprecated` no aparece en el corpus. La taxonomía declara el modelo; la práctica lo sustituye por prosa.

### 2.8 SAE — la frontera de autonomía

`IMPLEMENTED` (`.agents/policies/supervised-autonomous-execution.md`; `runtime/orchestrator/autonomy.py`; `.agents/policies/autonomous-orchestration.md`):

```text
AUTHORITY   lo que está autorizado         ← RFC Accepted, ADR, Plan aprobado, clase DECISION del mantenedor
SCOPE       qué trabajo está autorizado    ← la declaración `## Delegación agentiva` del Plan (Task + Scope)
AUTONOMY    qué acciones el host ejecuta sin preguntar de nuevo
autonomy ⊆ authorized scope   ∧   autonomy ⊆ granted authority
```

- El envolvente **se deriva** de declaraciones que el Plan aprobado ya posee; **no hay superficie de declaración nueva, ni registry, ni segunda fuente de verdad** (§3 de la policy).
- Ausencia honesta: *«no declaration ⇒ no autonomy»*; un Plan sin `## Delegación agentiva` **no delega trabajo semántico**.
- Refusal rule: si la pertenencia no se puede establecer con evidencia suficiente → **STOP**; la autorización **nunca** se asume por proximidad semántica (nombre similar, prefijo, plural, precedente, «obviedad»).
- Veredictos exactamente tres: `AUTHORIZED_EXISTING`, `REQUIRES_HUMAN`, `FORBIDDEN`; release/promotion/tag son `FORBIDDEN` incondicionalmente.
- `§1.1` **una obligación de estado nunca es una autorización de escritura** (`REQUIRED`/`DEFERRED` no autorizan); `§1.2` **no retroactividad** (una reescritura posterior de `Scope`/`Task`/status es divergencia, no aclaración); `§1.3` **una escritura se autoriza como un todo** (un target fuera de scope detiene la acción completa; un conjunto de targets no establecible también); `§1.4` **no existe ampliación autónoma de scope** y crearla está prohibido.
- Métrica (§11): `autonomous_steps / authorized_steps`, con la distinción estricta `human_operational_intervention` (costo de autonomía incompleta) ≠ `human_authority_decision` (la frontera funcionando; **no** es un fallo de autonomía).

**Esta distinción es la brújula de la pregunta central**: el objetivo de un prompt conciso es reducir `human_operational_intervention` (cuánto tiene que *especificar* el humano), **no** `human_authority_decision` (cuánto tiene que *decidir*). Cualquier diseño que reduzca el segundo degrada la gobernanza.

---

## 3. Evidence

### 3.1 Método

`FACT` — La investigación trabajó sobre la arquitectura y documentación real del repositorio, y solo usó implementación y tests para distinguir contrato documentado de comportamiento implementado. Método:

1. **Lectura normativa completa** de la gobernanza DEV: `AGENTS.md`, `.agents/AGENTS.md`, `.agents/policies/{authority,validation-closure,lifecycle-checkers,autonomous-orchestration,supervised-autonomous-execution}.md`, `.agents/workflows/change-lifecycle.md`, `docs/{AGENTS,CONVENTIONS,VERSIONING,placement-contract}.md`, `docs/rfc/{46,56,63,67,68,75}.md`, `docs/adr/{03,10,16,INDEX}.md`, `ROADMAP.md`, `docs/plans/{_TEMPLATE,94,149}.md`, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/glossary/INDEX.md`, `MASTER_PENDING_WORK_INVENTORY.md`, `docs/architecture-capability-review.md`.
2. **Lectura del payload** relevante: `protocol/.agents/standards/{requirements/NO_ASSUMPTIONS,requirements/INTENT_CONFIDENCE,context/KNOWLEDGE_LIFECYCLE,context/KNOWLEDGE_CURATION,context/RESOLUTION_UNRESOLVABLE_CONFLICTS,orchestration/DECISIONS,conduct/OPERATIONAL_RULES,conduct/ANTI_CIRCUMVENTION,runtime/AUTHORIZATION}.md`, `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`, `protocol/.agents/standards/context/CONTEXT.md` (por referencia).
3. **Conteo mecánico reproducible** de estados del corpus (comandos y resultados en §7).
4. **Auditorías delegadas de implementación y corpus** (cinco lecturas independientes y de solo lectura sobre `runtime/`, `tools/`, `docs/plans/`, `docs/rfc/`, `protocol/.agents/`), usadas para distinguir contrato documentado de comportamiento implementado y para clasificar el corpus.
5. **Reconstrucción de la cadena de autoridad** de los dos artefactos externos preexistentes (`MASTER_PENDING_WORK_INVENTORY.md`, `docs/architecture-capability-review.md`) contra Git y contra el registro de planes.

### 3.2 Clases de evidencia usadas y su límite

| Clase | Qué se usó | Límite declarado |
|---|---|---|
| `REPO_CODE` | `runtime/`, `tools/`, `protocol/.agents/harness/` | se leyó, **no se ejecutó** la batería completa (la investigación es read-only y no la requiere); los resultados de checkers citados provienen de documentos del repositorio que los registran, no de una corrida propia |
| `REPO_DOC` | RFCs, ADRs, planes, policies, contratos | un documento puede estar desactualizado respecto del código; donde eso ocurre se registra como `CONTRADICTION` con ambas fuentes |
| `MECHANICAL_COUNT` | conteos sobre `docs/plans/` y `docs/rfc/` | conteo por expresión regular sobre la línea `**Status:**`; no distingue matices de prosa dentro del estado |
| `GIT_FACT` | `git status`, `git log` | estado al momento del inicio; `dev` está 1 commit adelante de `origin/dev` |
| `EXTERNAL` | **no usado** | esta investigación **no** incorporó evidencia externa. Justificación: la pregunta es de *derivación interna* (qué puede derivar ARgentOS de su propio corpus); el análisis comparativo externo ya fue hecho con rigor en `docs/architecture-capability-review.md` §3/§12.2, y adoptar patrones externos por analogía es exactamente lo que `ROADMAP.md:Qué no es una entrada de este roadmap` prohíbe («features copiadas de otros proyectos»). Toda afirmación de este documento es del repositorio o inferencia declarada. |
| `INFERENCE` | marcada explícitamente cuando aparece | no es evidencia |

### 3.3 Hallazgos de la auditoría de implementación (`runtime/`)

Estos hallazgos provienen de una lectura de solo lectura de `runtime/` (§3.1 punto 4) y son la base de la distinción contrato/prosa que el resto del documento usa.

- `FACT` — `runtime/` tiene dos mitades casi independientes: `runtime/toolcalls/` materializa RFC-71/72/73/76/78 (identidad, materialización canónica, frontera de prompt cache) y `runtime/orchestrator/` es el host DEV del Change Lifecycle (planes 122/123/135/138). `runtime/placement/` es un tercer componente, **puro y autónomo**. El orquestador **no importa nada** de `runtime/placement` y solo usa `toolcalls.context.ExecutionContext` + `toolcalls.prompt_rendering.render_prompt`: la materialización canónica v2, `segment_resolution` y `project_store` nunca son invocados por el host.
- `IMPLEMENTED` — Autoridad, scope y autonomía **sí** están mecánicamente implementados y son deterministas (`runtime/orchestrator/authority.py`, `autonomy.py` + `host.py:_apply_autonomy_gate`), y la escritura no autorizada se **refusa antes del efecto** sobre el conjunto completo de write-targets.
- `GAP` — **La fuente de verdad de la autorización, en código, es solo**: la línea `**Status:**` del plan + `## Delegación agentiva` (Task/Scope) + `## Entregables` + `docs/plans/INDEX.md` + el `Scope set` del anchor registrado + Git. **Ningún código lee `.agents/policies/`, `docs/rfc/` ni `docs/CONVENTIONS.md`**: se citan como strings. Consecuencia: la clase RFC-56 (`A`/`B`/`C`), la exigencia de «RFC `Accepted`», las obligaciones de cierre y los stop conditions de la policy son **prosa en el prompt**, no reglas evaluadas. `change_level` y `rfc` se parsean y **no se usan**.
- `GAP` — **Ningún código parsea `Documentation Impact` ni `Roadmap Impact`**: aparecen únicamente en prosa (`runtime/README.md`, `.agents/policies/*`, planes, `CHANGELOG.md`).
- `FACT` — `runtime/placement/rules.py` contiene tablas **muertas** que `resolve()` nunca consulta (`ROOT_ANCHORED`, `EXACT_ARTIFACTS`, `find_exact_artifact`), sin uso en `runtime/` ni en `tests/`.
- `PARTIALLY_IMPLEMENTED` — La resolución de placement **no es total**: devuelve `STOP` con una negativa estructurada y **no tiene estado de escalación humana**; el STOP es un resultado, y la escalación existe solo en el contrato (`PC-23`/`PC-25`: `STOP → human authority`).
- `FACT` — `runtime/` tiene **cero** marcadores `TODO`/`FIXME`/`XXX`/`HACK` (solo dos coincidencias léxicas: el string de error «is not implemented» en `runtime/toolcalls/canonical.py` y un docstring «placeholder»). Es consistente con `MASTER_PENDING_WORK_INVENTORY.md:§4` («0 hits» en `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/`).

### 3.4 Hallazgos de la auditoría de checkers y enforcement

- `FACT` — La **batería canónica** es única y está definida en `docs/VERSIONING.md:4.1`: `check_protocol_invariants.py --payload protocol .`, `check_plan_citations.py`, `check_plan_structure.py`, `check_taxonomy_coherence.py`, `check_session_artifacts.py`, `check_version_state.py`, `pytest tests/`. `check_dist_sync.py` es local-only y se espera **rojo en `dev` por diseño**.
- `FACT` — Los tres gates de lifecycle **no** pertenecen a la batería ni a CI: son «advisory, factual, DEV-only», se corren en los momentos que fija `.agents/policies/lifecycle-checkers.md`, y su exit code solo se vuelve no-cero ante `ANOMALY` (`GAP` nunca cambia el exit code). `check_architecture_traceability.py` es dev-only y su entrada a CI está diferida (`docs/rfc/69-documentation-taxonomy-and-layout.md:Future Evolution`).
- `IMPLEMENTED` — La **detección de identidad de contenido obsoleta** existe y es el único mecanismo mecánico de obsolescencia del sistema: `anchor_stale` compara la Scoped Content Identity validada contra la actual, y una identidad actual desconocida **no** se lee como fresca (es `GAP` declarado).
- `GAP` — **Ningún checker valida vigencia, supersesión, duplicación o contradicción semántica.** `check_plan_citations` verifica que las citas `ruta:sección` **resuelvan** (existencia), no que sean verdaderas; `check_taxonomy_coherence` verifica que las referencias taxonómicas **resuelvan**, no que **coincidan** (el `MASTER_PENDING_WORK_INVENTORY.md:CON-8` documenta dos contratos del payload cuyo metadata YAML no coincide con la taxonomía **con la batería en verde**); `check_lifecycle_lineage` verifica forma y consistencia interna del lineage, no la verdad de la resolución.
- `PARTIALLY_IMPLEMENTED` — La coherencia INDEX↔artefacto se verifica **por forma** (`check_plan_structure.py` exige que todo plan numerado tenga fila), no por contenido: `MASTER_PENDING_WORK_INVENTORY.md:§7` encontró **más de veinte filas stale** con la batería verde.
- `CONTRADICTION` — `docs/VERSIONING.md:4.1` se declara «única definición» de la batería, pero seis scripts de `tools/` (`audit_gates.py`, `aggregate_metrics.py`, `determine_execution_state.py`, `measure_context_budget.py`, `scoped_content_identity.py`, `legacy_paths.py`) más `check_architecture_traceability.py` no están ni en la batería ni declarados fuera de ella por ningún texto normativo (`MASTER_PENDING_WORK_INVENTORY.md:CON-10`).

### 3.5 Hallazgos de la auditoría del corpus y del payload

Los hallazgos de corpus están integrados en §7; los del payload, en §2.5, §4.2 y §8.2. Tres hechos del payload merecen figurar aquí porque son la evidencia directa de la pregunta central:

- `FACT` — `protocol/.agents/standards/context/KNOWLEDGE_CURATION.md:Inclusion rules` establece que una entrada del KB «is only justified when it records knowledge that **cannot be inferred from the repository itself**», con el test explícito para una lesson: *«does the agent now know something it could not have derived from `git log`, the code, or existing docs?»*. Es la formulación más nítida que el repositorio tiene del criterio «derivable ≠ adivinable», y aplica a **conocimiento**, no a **reglas aplicables**.
- `FACT` — `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` separa tres dominios de invalidación que **no** son intercambiables: semántica (correctness, solo por cambio de identidad), expiración de frescura (lifecycle/eligibilidad de reuso; `stale` **no** implica inválido), y borrado físico (storage, no afecta identidad semántica). Y declara la distinción `Historical knowledge` (snapshots y lessons pasados, conservados como traza) vs `Current knowledge` (claims frescos con provenance resoluble, elegibles para reuso), «declared through the `kind` tag; nothing is reclassified retroactively».
- `FACT` — El Protocol **sí tiene** un lifecycle de conocimiento con detección de invalidación post-ejecución: `invalidated_facts` en `EXECUTION_SUMMARY.md`, y `KN-004`/`KN-006`: «Every execution that changes discovered facts declares `invalidated_facts`» y «Knowledge-base entries are updated only through the discovery pipeline».

Esto es decisivo para §9: **ARgentOS ya resolvió el problema de reconciliación de conocimiento en el dominio del Protocol (Project Knowledge), y no lo resolvió en el dominio DEV (documentación de gobernanza).** La asimetría es la carencia.

### 3.6 Hallazgos de mayor valor de las auditorías de implementación, checkers y payload

Estos hallazgos no estaban en la lectura documental y son los que más cambian el diagnóstico. Cada uno está verificado en el artefacto citado.

**a. El prompt que el host entrega al worker no contiene ninguna regla del protocolo ni de la gobernanza.** `FACT` — `runtime/orchestrator/agent_worker.py:302-327` construye el contexto con `skills=()`, `knowledge_entries=()`, `harness_policy=()` y `profile=None` **hardcodeados**, y `render_prompt` (`runtime/toolcalls/prompt_rendering.py:26-45`) emite seis líneas: session, state, phase, role, task, context_budget. El `task` es la cadena del Plan; el `scope` y los `verification_commands` viajan como **datos**, y `authority_basis` se registra en el resultado pero **nunca se envía**. Consecuencia directa sobre la pregunta central: **hoy no hay ningún lugar donde el sistema ponga el conocimiento operativo que debería derivar**, ni siquiera el que ya tiene en mano. La autonomía no puede depender de un prompt más corto porque el prompt del ejecutor no contiene el conocimiento operativo en absoluto: el host lo aplica *alrededor* de la invocación (frontera SAE, gate previo al efecto, verificación post-delegación) y no *dentro*.

**b. La consistencia del cierre es una atestación que el propio host escribe y vuelve a leer como evidencia.** `FACT` — `runtime/orchestrator/governance.py:190` escribe literalmente `- **Consistencia checkpoint↔anchor:** PASS — …`; `runtime/orchestrator/observation.py:585-587` la lee de vuelta (`consistency_pass = bool(consistency_match and "PASS" in …)`); y `runtime/orchestrator/host.py:1016-1031` deriva `Closed` con esa lectura. Del mismo modo, `governance.py:159` escribe `- **Validity / stale:** vigente` de forma incondicional y `governance.py:136` fija la cadena de `Observed dependencies`. Mitigación existente y verificada: la derivación de `Closed` también exige igualdad de `state_identity` y re-lee los gates (`derivation.py:418-453`). `PARTIALLY_IMPLEMENTED` con un `GAP` de calidad de evidencia: **una cadena de evidencia no debería contener un valor que el propio escriba y luego consuma como prueba de su propia consistencia**. Es exactamente el patrón que `protocol/.agents/harness/INDEX.md:151-160` prohíbe al payload («A claim may be called "verified" only when it cites evidence of a class other than attestation»).

**c. La derivación cierra un Change sin consultar las determinaciones de impacto, mientras la policy las declara condición de stop.** `CONTRADICTION` — `.agents/policies/validation-closure.md:345-346` hace ilegal el cierre «without an explicit Documentation impact determination … or without an explicit Roadmap impact determination», pero `runtime/orchestrator/derivation.py:407-466` alcanza `CLOSED_DERIVED` verificando solo status, anchor, checkpoint y gates, y `host.py:1025-1031` define `Closed` sin consultar ningún impacto. Ningún código parsea `Documentation Impact` ni `Roadmap Impact`. Es la brecha exacta entre la regla declarada y el ejecutor, y es la que hace que «qué obligaciones aplican» no sea derivable hoy.

**d. Hay clases de acción declaradas en el vocabulario de autonomía que el bucle no puede alcanzar.** `FACT` — `UPDATE_DOCUMENTATION_AUTHORIZED` (`autonomy.py:101,113`), `SYNC_REPOSITORY_STATE` (`:93`) y `RECOVER_IN_SCOPE` (`:102`) no figuran en `_AUTONOMY_CLASS_BY_ACTION` (`host.py:129-141`), de modo que son construibles solo en tests. Y `RECORD_FINDING_CORRECTION`/`RECORD_FINDING_DETECTED` están en el vocabulario y en `_AUTONOMY_PLAN_WRITES` (`host.py:161-162`) pero `_apply_record` no tiene rama para ellos (`host.py:775-830`); el propio código lo admite (`autonomy.py:1449-1458`). Es decir: **la capacidad de registrar una corrección autónoma existe como código y no es alcanzable desde el bucle**.

**e. El resolutor de placement documenta más de lo que resuelve.** `FACT`/`GAP` — `runtime/placement/rules.py` contiene `ROOT_ANCHORED` (`:251-255`), `EXACT_ARTIFACTS` (`:258-271`) y `find_exact_artifact` (`:293-299`) con **cero referencias** en `runtime/` y en `tests/`: `resolve()` nunca las consulta. Los artefactos anclados a la raíz del contrato (`AGENTS.md`, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `LICENSE`, `conftest.py`, `runtime/README.md`, `.github/workflows/`) están documentados y **no son resolubles**. Y el resolutor, aunque determinista, **no es total**: devuelve `STOP` con 11 motivos estructurados (`resolver.py:36-54,107-162`) y **no tiene estado de escalación humana**; la escalación existe solo en el contrato (`PC-23`/`PC-25`) y **nada invoca el resolutor** (`PC-72.1`: «nothing invokes it automatically»).

**f. La cobertura de detección mecánica está mapeada con precisión, y sus huecos son exactamente los que la pregunta central necesita.** `GAP` — Verificado sobre los 20 scripts de `tools/`:

| Señal que el sistema necesitaría detectar | ¿Detectable hoy? | Frontera exacta |
|---|---|---|
| cita `path:sección` rota (backtick) en planes/RFC/ADR/12 docs raíz | **sí** | `check_plan_citations.py:211-231`; el mapeo legacy puede enmascarar un path equivocado; `.project/` exento |
| referencia rota dentro del payload | **sí** | `check_protocol_invariants.py:302-349`; **los `#fragment` se descartan** (`:314`) |
| link markdown `[x](y)` roto fuera del payload | **no** | ningún tool parsea `](` fuera de `protocol/.agents/` — medido: 70 links rotos en `docs/adr/`, 23 en `docs/rfc/` (escritos como paths desde la raíz del repo; `check_plan_citations` los resuelve contra la raíz, así que son **citas legales y navegación rota**) |
| artefacto `Superseded` que no nombra a su sucesor (o sucesor inexistente) | **no** | `superseded` es solo vocabulario de estado; C-3 declara que no tiene regla de contenido (`check_lifecycle_lineage.py:37-38`) |
| contradicción semántica entre documentos | **no** | imposible por diseño declarado (`docs/CONVENTIONS.md:587-590`) |
| documento que ya no describe el sistema | **no** | ídem; `docs/VERSIONING.md:385`: «no hay checker semántico» |
| trabajo abandonado (plan retirado en silencio) | **no** | un `Superseded` sería legal e invisible; un no-miembro es `EXCLUDED` y un miembro sin cerrar es `N/A` |
| fila del INDEX que contradice el header del artefacto | **no** | el espejo se verifica por **substring del nombre** (`check_plan_structure.py:153-159`); las celdas nunca se parsean |
| duplicado de artefacto / identidad reutilizada | **parcial** | solo claves de entidades taxonómicas, refs de lineage y nombres de efecto; **no** números de plan/RFC/ADR ni filenames |
| identidad de contenido declarada (delta SCI) incorrecta | **no** | C-1 verifica solo el **formato** 40-hex/64-hex (`check_lifecycle_anchor.py:286-313`); **nada recalcula** y compara |
| cierre con estado de cierre sin validación correspondiente | **sí** | C-2 R2 → `ANOMALY` (`check_lifecycle_checkpoint.py:581-585`), herramienta advisory, fuera de CI |
| payload modificado sin autorización RFC-56 | **no** | ningún tool lee `Clase:` ni la vía de autorización |
| `dist` desincronizado | **sí, local-only** | `check_dist_sync.py`; rojo en `dev` por diseño |

**g. El contrato documentado del cierre es más fuerte que su implementación.** `CONTRADICTION` — `.agents/policies/lifecycle-checkers.md:74-77` incluye en el `ANOMALY` de C-2 «declared closure state contradicting a declared materialized commit tree», y el docstring de `tools/check_lifecycle_checkpoint.py:16-18` todavía lo lista; la implementación lo degradó a `GAP` advisory (`:597-620`, y `anomaly_prefixes` en `:621-628` no contiene ese mensaje). `docs/validation-closure.md:142` describe una versión más débil que ambas. Tres formulaciones de la misma relación, ninguna idéntica al código.

**h. La batería tiene dos definiciones dentro del mismo documento y nueve scripts sin declaración.** `CONTRADICTION` — `docs/VERSIONING.md:135-138` llama a §4.1 «única definición», y `:115-119` (§4 paso 3) enumera un conjunto distinto que agrega `check_dist_sync.py` y H13 por juicio. Además, nueve scripts (`audit_gates`, `aggregate_metrics`, `determine_execution_state`, `measure_context_budget`, `scoped_content_identity`, `legacy_paths`, `check_architecture_traceability`, `check_discovery_output`, `check_ears_coverage`) no están ni en la batería ni declarados fuera de ella; su única protección de regresión es `pytest tests/`, que CI sí corre, de modo que están cubiertos **como código** y nunca se ejecutan **contra el corpus real** en CI.

**i. El payload tiene su propio modelo de conocimiento y su propio artefacto de gobernanza, ninguno de los cuales está operativo.** `FACT` — `protocol/.agents/contracts/KNOWLEDGE_INDEX.md:4-6,30-32` se declara a sí mismo `enforcement = "informational"`: «The automated indexer is not implemented yet». Y `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:70-72` declara su propio artefacto `enforcement = "documented"`: «no runtime gate, harness gate or validation gate enforces this artifact», con `append`, la derivación de «current» y de `governance_position` **diferidas** (`:206-241`). Es decir: **el Protocol tampoco puede representar hoy «qué conocimiento es el vigente»**, y su propio RFC-76 lo dejó explícitamente fuera del MVP. La asimetría con DEV no es que el Protocol lo tenga resuelto: es que el Protocol lo tiene **declarado como diferido** y DEV lo tiene **resuelto a mano por convención**.

**j. El corpus es de un tamaño que ninguna sesión puede leer.** `FACT` — `docs/plans/` = 43.160 líneas / 3.374.034 caracteres (41.296 / 3.121.957 sin el INDEX) ≈ **840.000 tokens** a 4 chars/token; `docs/rfc/` = 17.428 líneas / 1.028.312 caracteres; `protocol/` = 238 archivos, 226 de texto, 25.431 líneas. El corte de gobernanza puro (`CONVENTIONS` + `VERSIONING` + plantilla + `docs/AGENTS.md` + `AGENTS.md` + `placement-contract`) son ~2.159 líneas ≈ 18k tokens y sí es legible. Consecuencia para la pregunta central: **un agente no puede reconstruir el estado vigente leyendo; tiene que poder consultarlo.**

**k. Los títulos del corpus mienten por sistema, y hay un caso de dos planes que afirman lo contrario sobre el mismo hecho.** `CONTRADICTION` — `docs/plans/136-...md:17` afirma «El runner del harness **no existe** (plan 60)» y `docs/plans/137-...md:19` afirma «**El validador estructural ya existe**»; el repositorio confirma 137 (`protocol/.agents/harness/gate_validator.py` existe y su trigger H01 corre el chequeo EARS). Ambos planes están `Executed`. Un lector que lea solo el 136 vuelve a planificar trabajo existente — y eso es exactamente lo que le pasó al roadmap según `137:13` («lo que el roadmap describe como trabajo futuro ya existe en el payload»).

**l. El payload tiene 13 contradicciones internas verificadas.** `CONTRADICTION` — Entre ellas, las cuatro más relevantes para esta investigación: (1) `protocol/.agents/orchestrators/discovery/INDEX.md` **no existe** aunque `INDEX.md:32` y `_AGENTS.md:32` lo prometen; (2) la máquina de estados de discovery exige `DISCOVERY_STACK → DISCOVERY_MERGE` mientras el workflow y su índice exigen `DISCOVERY_STACK → DISCOVERY_FRAMEWORK`, de modo que **ningún camino de scope puede alcanzar el merge legalmente**; (3) el lector de `state.json` es *fail-closed* (`runner_state.py:9,279-283`) y el hook es *fail-open* (`hook_gate.py:25-27`), y el payload **nunca reconcilia** ambas afirmaciones sobre el mismo artefacto; (4) el perfil de flags por `AGENTS_FEATURE_<FLAG>` que el checklist de H01 exige no existe en el validador ni en el runner (`gate_validator.py:323-332` lee solo `features.toml`).

---

## 4. Prompt Dependency Analysis

### 4.1 El catálogo de lo que hoy hay que escribir

`FACT`/`PARTIALLY_IMPLEMENTED` — Para cada pieza de conocimiento operativo, cuál es su fuente real hoy y quién la aporta:

| Conocimiento operativo | Fuente real hoy | Quién lo aporta hoy | ¿Derivable de contratos/políticas/lifecycle/autoridad/contexto? |
|---|---|---|---|
| Clase de cambio RFC-56 (A/B/C) | `docs/rfc/56-governance-fast-track.md` | **el humano o el agente en prosa**; ningún código lo evalúa | `PARTIALLY`: la regla es determinista pero requiere juicio de «cambio de significado»; el host lo parsea y no lo usa |
| Change Level L0–L3 | `docs/rfc/75-change-lifecycle.md:Mecanismo 2` | el agente, declarado en el header | `PARTIALLY`: los ejes son verificables por contenido del diff; la calibración fina es juicio |
| Vía de autorización (¿hace falta Plan? ¿RFC?) | `.agents/workflows/change-lifecycle.md:2`; RFC-56 | el agente, por derivación | `IMPLEMENTED` como regla (`DOCUMENTED_ONLY` como código): se deriva de clase + dominio; **pero el artefacto que autoriza hay que redactarlo** |
| `Task` y `Scope` de la delegación | `## Delegación agentiva` del Plan | **el humano/agente redacta el Plan** | `NO` hoy: no hay lugar del que derivar «qué trabajo y qué rutas», salvo los `## Entregables` que el propio Plan declara |
| Obligaciones aplicables (anchor, checkpoint, C-1/C-2/C-3, determinaciones de cierre, changelog, series) | `validation-closure.md`, `lifecycle-checkers.md`, `VERSIONING.md:10` | el agente, leyendo policies | `PARTIALLY`: las reglas existen; no hay resolución determinista de *cuáles aplican a este cambio* |
| Documentos de estado actual afectados | `validation-closure.md:5.1` lista + «cualquier otro documento que el propio Change identifique» | **juicio del Change** | `NO`: la lista es abierta por diseño |
| Conocimiento vigente del repositorio | no hay fuente única | **el agente leyendo prosa** | `NO` hoy: los estados no codifican vigencia (§7) |
| Reglas del Protocol aplicables a un cambio de payload | RFC `Accepted` correspondiente (sin índice temático) | el agente, buscando en 80 RFCs | `PARTIALLY`: `docs/rfc/INDEX.md` da la «pregunta que responde» cada RFC, sin mapeo a rutas del payload |
| Qué trabajo es (kind) | inexistente | **el humano, por el título del pedido** | `NO`: no hay taxonomía (§2.6) |
| Criterios de aceptación | el pedido o la RFC | **el humano** | `NO` por diseño correcto: no se derivan criterios de aceptación (`NO_ASSUMPTIONS.md` los prohíbe asumir) |

### 4.2 El punto exacto donde la dependencia del prompt está mecanizada

`FACT` — `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md`:

| Criterio positivo | Peso | Criterio negativo | Peso |
|---|---|---|---|
| el prompt nombra al menos una tecnología/framework/librería/tool concreta | +2 | términos vagos («algo», «cosas», «lo de siempre», «etcétera») | −2 |
| el prompt incluye al menos un verbo de acción medible | +2 | contradicciones explícitas entre requisitos | −3 |
| el prompt define la entidad u objeto principal del trabajo | +2 | falta sujeto, acción o objeto principal | −2 |
| el prompt declara un criterio de éxito o salida esperada | +2 | múltiples tareas sin prioridad ni relación | −1 |

`score >= 6` → `HIGH` (confirmación **opcional**); `2..5` → `MEDIUM` (confirmación **requerida**); `< 2` → `LOW` (confirmación requerida, mensaje detallado).

`FACT` — «Implementá X» (con X una entidad nombrada) obtiene `+2` (verbo) `+2` (entidad) = **4 → MEDIUM → `CONFIRMING_INTENT` obligatorio**. Si se añade la tecnología y el criterio de éxito, sube a 8 y la confirmación se vuelve *opcional*.

**Lectura arquitectónica (`GAP`)**: el estándar mide la **exhaustividad del pedido**, no la **determinabilidad del faltante**. Un pedido puede ser brevísimo y estar completamente determinado por contratos y estado del repositorio, y el estándar lo mandará igual a `CONFIRMING_INTENT`. La causa es estructural: el score se calcula **antes** de la fase de contexto y no tiene acceso a la derivación (fase 03–04 del workflow). Es decir, el sistema pregunta *antes* de intentar derivar, porque su criterio de confianza no depende del repositorio.

`DESIGN_OPTION` (no recomendación aceptada) — Un criterio alternativo, compatible con el modelo existente: mantener `INTENT_CONFIDENCE` como señal de **forma** del pedido y añadir, después de `GATHERING_CONTEXT`/`VALIDATING_CONTEXT`, una condición distinta — «¿el faltante es derivable de fuentes autorizadas?» — con tres resultados posibles, calcados del vocabulario que ya existe: `DERIVED` (una sola interpretación sustentada por una fuente normativa o factual), `UNDETERMINED` (dos o más lecturas razonables; **no** es lo mismo que «el humano no lo escribió»), `NOT_DERIVABLE` (requiere decisión humana). El mapeo natural es al vocabulario existente de `AUTHORIZATION_UNDETERMINED` y a `DECISIONS.md:D3`. Coste: una condición y un registro, no una entidad.

### 4.3 Qué información debería poder inferirse legítimamente

`FACT` + `DESIGN_OPTION` — Criterio propuesto, derivado de lo que el repositorio ya declara:

**Inferencia legítima** (la conclusión se sigue de una fuente autorizada, sin elegir entre alternativas):

1. **La vía de autorización** de un cambio: dominio + clase RFC-56 + efecto sobre payload ⇒ `RFC Accepted + plan` / `plan aprobado` / `commit directo`. Regla determinista ya escrita (`change-lifecycle.md:2`; RFC-56).
2. **El conjunto de obligaciones del lifecycle** aplicables por Change Level, tal como `docs/plans/94-...:9.2` ya lo tabula (L0 mínimo; L1 plan + anchor + checkpoint; L2 plan completo + findings/pending + revalidación; L3 machinery completa).
3. **El scope de escritura** cuando el cambio es Clase C/L0 (un archivo, declarado por la corrección misma).
4. **La ubicación de un artefacto nuevo**, por el contrato de placement: `PLACE | STOP` determinista.
5. **El estado derivado del cierre** (`Verified`/`Executed`/`Closed`) a partir de anchor, checkpoint y consistencia.
6. **La obsolescencia por identidad de contenido**: si la Scoped Content Identity cambió respecto del anchor aplicable, la validación es `stale`.
7. **La resolución de citas y referencias**: existencia y resolución.
8. **Qué conocimiento es «derivable del repositorio»** — criterio ya enunciado para el KB del Protocol (`KNOWLEDGE_CURATION.md`): lo derivable de `git log`, del código o de docs existentes **no** merece ser conocimiento registrado.

**Nunca inferible** (requiere autoridad o decisión humana; lista derivada de `NO_ASSUMPTIONS.md:Rule`, `ANTI_CIRCUMVENTION.md:Rule`, `AUTHORIZATION.md:Default frontier` y `supervised-autonomous-execution.md:§5`):

1. Elecciones de tecnología, comportamiento, alcance (inclusiones/exclusiones), decisiones de diseño o arquitectura.
2. Comportamiento de validación, seguridad o manejo de errores.
3. **Criterios de aceptación** (`NO_ASSUMPTIONS.md:16`: «Acceptance criteria»).
4. Hechos, contexto o decisiones inventados para evitar clarificar.
5. La autorización de un efecto fuera de la frontera (`network`, `remote_git`, `install`, `destructive`, `write_outside_project`) — `AUTHORIZATION.md:AUTH-001`/`AUTH-002`.
6. La resolución de un conflicto normativo (`authority.md:Conflict protocol`).
7. La resolución o transición de estado de un finding (`CL-8`; `AU-3`).
8. ADR-worthiness (`AU-6`).
9. Release, promoción, tag (incondicionalmente `FORBIDDEN`).
10. La ampliación de `Task`, `Scope` o `Authority` (§1.4).
11. Un `STOP` de placement convertido en `PLACE` (`PC-22`: «GUESS is never a valid outcome»).
12. La interpretación de una excepción de placement que no puede localizarse (`PC-30`).

`FACT` — El criterio «derivable ≠ adivinable» **ya está formulado** en el repositorio, dos veces y con precisión: `NO_ASSUMPTIONS.md:25-27` («MAY proceed without clarification only when the missing detail has **exactly one** reasonable interpretation given the context») y `KNOWLEDGE_CURATION.md` («cannot be inferred from the repository itself»). La carencia no es el criterio: es que **el criterio se aplica a una lectura humana del prompt y no a una resolución contra fuentes**.

### 4.4 Cuándo continuar autónomamente y cuándo detenerse

`FACT` (fuentes citadas) — El sistema actual lo responde así:

| Situación | Regla hoy | Fuente |
|---|---|---|
| El paso está dentro de `autonomy ⊆ scope ∩ authority` y el checkpoint de autorización no divergió | continuar sin pedir nada; «The host **does not** ask a human to confirm a step it is already authorized to take» | `supervised-autonomous-execution.md:§4` |
| Falta un detalle con **exactamente una** interpretación razonable dado el contexto | avanzar sin clarificar | `NO_ASSUMPTIONS.md:25-31` |
| El detalle es sintáctico/formato y no afecta comportamiento | avanzar sin clarificar | ídem |
| El usuario ya confirmó una decisión equivalente **en la misma sesión** | avanzar sin clarificar | ídem |
| `INTENT_CONFIDENCE < 6` | `CONFIRMING_INTENT` | `INTENT_CONFIDENCE.md:37-41` |
| El faltante obliga a elegir entre dos o más implementaciones razonables | `NEEDS_CLARIFICATION` | `NO_ASSUMPTIONS.md:21` |
| Conflicto irresoluble entre candidatos de contexto (incompatibilidad / exclusión mutua / presupuesto) | detener el ensamblado; F3 clarificación, F4 reporte de inconsistencia, F1 blocker | `RESOLUTION_UNRESOLVABLE_CONFLICTS.md:19-29` |
| Conflicto entre fuentes normativas | `no source wins automatically` → escalar | `authority.md:33`; `supervised-autonomous-execution.md:§5` |
| Incertidumbre de placement | `STOP` + decisión requerida | `placement-contract.md:PC-23/PC-24` |
| Efecto fuera de frontera sin registro | `AUTHORIZATION_UNDETERMINED`, **nunca** `UNAUTHORIZED` | `AUTHORIZATION.md:AUTH-004` |
| No hay Plan aprobado y el cambio no es C/L0 | **STOP** y proponer el plan | `change-lifecycle.md:46-64` |

`FACT` — El patrón es coherente y conservador: **el sistema prefiere detenerse**. La consecuencia medible para la pregunta central: hoy la frontera de parada se activa **mucho antes** de lo que la incertidumbre real exige, porque (a) el intake exige un artefacto redactado y (b) la confianza se mide sobre el prompt.

### 4.5 Veredicto sobre la hipótesis «Implementá X»

`HYPOTHESIS` — *«Un prompt como "Implementá X" podría ser suficiente para iniciar un trabajo cuando X está inequívocamente determinado por el contexto y la autoridad disponible.»*

**Veredicto: `CONFIRMED AS DESIRABLE, REJECTED AS CURRENTLY REACHABLE` — con una excepción acotada y verificada.**

Lo que la evidencia sostiene:

- `IMPLEMENTED` — Existe un camino real, hoy, desde un pedido brevísimo hasta un commit sin más intervención humana: **Clase C** (typo, formato, link, whitespace; «cero cambio de significado») con la batería verde y registro en el changelog de la próxima versión. Y **L0** («1 agente, 1 sesión, 1 archivo, sin cambio estructural, sin versión, <1 sesión»; «sin Plan obligatorio»). Para ese subconjunto, «Implementá X» **es** suficiente.
- `GAP` — Fuera de ese subconjunto, y por **cuatro razones independientes ya enumeradas** (§1 punto 4), no lo es: falta la derivación del tipo de trabajo, la del conocimiento vigente, la de las obligaciones aplicables, y sobra el requisito de que un humano redacte y apruebe un Plan.
- `HYPOTHESIS` (evaluada, aceptada con matiz) — La condición «cuando X está inequívocamente determinado por el contexto y la autoridad disponible» es **exactamente la condición correcta** y el repositorio ya tiene el vocabulario para expresarla (`exactly one reasonable interpretation given the context`, `NO_ASSUMPTIONS.md:26`). El problema no es la condición: es que **hoy nadie la evalúa contra el repositorio**.

`INFERENCE` (declarada) — Extender el conjunto «prompt brevísimo suficiente» más allá de C/L0 no requiere ejecutor nuevo. Requiere que el sistema pueda **construir la autorización** a partir de la intención. `INFERENCE`, no hecho: esta investigación no probó el mecanismo porque no lo implementa.

---

## 5. Governance and Uncertainty Model

### 5.1 La hipótesis evaluada

`HYPOTHESIS` — *«Cuando las reglas existentes no permiten determinar legítimamente la acción, ARgentOS debe escalar a la autoridad humana en lugar de inventar una precedencia o resolver el conflicto por inferencia.»*

**Veredicto: `CONFIRMED — IMPLEMENTED (como regla) en cinco lugares independientes; `DOCUMENTED_ONLY` (como código) en DEV, `IMPLEMENTED` parcialmente en el Protocol.**

Evidencia por fuente, con cita:

| # | Fuente | Formulación exacta | Clase |
|---|---|---|---|
| 1 | `.agents/policies/authority.md:Conflict protocol` | «conflict → detect → classify → escalate → human decision → resolve through the appropriate artifact/change → revalidate»; «RFC vs ADR disagreement: **no automatic winner**; governance anomaly → escalate»; «Factual vs normative conflict: escalate with evidence; the maintainer decides» | `DOCUMENTED_ONLY` |
| 2 | `docs/rfc/75-change-lifecycle.md:Mecanismo 10` | «Sin jerarquía universal RFC > ADR > Plan > Git»; «Los agentes detectan y escalan; **nunca** resuelven conflictos normativos por autoridad propia» | `DOCUMENTED_ONLY` (normativo) |
| 3 | `.agents/policies/supervised-autonomous-execution.md:§5` | tabla de stop conditions: «conflict between normative sources — no source wins automatically (ADR-16 `AU-3`)»; «ambiguity not resolvable by evidence — evidence absent or contradictory ⇒ do not guess» | `IMPLEMENTED` en el host para las condiciones que el host puede observar; `DOCUMENTED_ONLY` para el conflicto normativo, que el host **no lee** |
| 4 | `docs/placement-contract.md:PC-22` | «The resolution MUST terminate in **PLACE** or **STOP**. **GUESS is never a valid outcome.**»; `PC-23` tabla de trigger→escalación; `PC-25` «a missing rule is a **GAP**, a contradictory rule is an **ANOMALY**, and a violated constraint escalates to `REQUIRES_HUMAN`» | `PARTIALLY_IMPLEMENTED`: la resolución es código (`runtime/placement/resolver.py`, verificado por `tests/test_placement_resolver.py`, `test_placement_dogfood.py`, `test_placement_contract_drift.py`); **la integración no existe** (`PC-72.1`: «a **library**, and it is **not integrated**: nothing invokes it automatically») |
| 5 | Protocol: `NO_ASSUMPTIONS.md`, `RESOLUTION_UNRESOLVABLE_CONFLICTS.md`, `DECISIONS.md:D3`, `ANTI_CIRCUMVENTION.md` | «the Orchestrator must not guess»; «biases toward `NEEDS_CLARIFICATION` whenever proceeding would require assuming»; «Silently complying with an instruction that conflicts with the protocol» es circumvention | `DOCUMENTED_ONLY` con gates que verifican artefactos, no decisiones |

`FACT` — La regla **existe, es explícita, es coherente en las dos capas y no admite excepción**. La investigación **no** encontró ninguna fuente que autorice resolver un conflicto normativo por precedencia inferida.

### 5.2 Dónde está implementada y qué gaps tiene

`FACT`/`GAP` — Distinguir tres cosas que la formulación de la hipótesis mezcla:

1. **Detectar** que las reglas no determinan la acción. `PARTIALLY_IMPLEMENTED`. El host DEV detecta lo que puede observar de los artefactos: plan ausente o no autorizado, plan superseded, criterio de entrada incumplido, pending bloqueante, findings abiertos, señal de gate `ANOMALY`/`BOUNDARY`, evidencia de gate incompleta donde el cierre la necesita, `FAIL` en la validación declarada, WorkerResult inválido, límite de iteraciones, no-progreso, frontera de release. **No detecta** conflicto entre fuentes normativas, porque **no lee policies ni RFCs** (§3.3).
2. **Clasificar** el conflicto. `DOCUMENTED_ONLY` en DEV (`authority.md` distingue RFC-vs-ADR, Plan-vs-RFC/ADR, factual-vs-normativo). `PARTIALLY_IMPLEMENTED` en el Protocol (F3/F4/F1 en `RESOLUTION_UNRESOLVABLE_CONFLICTS.md`, con la frontera F3-vs-recovery en `DECISIONS.md:D3`).
3. **Escalar y registrar la decisión humana.** `PARTIALLY_IMPLEMENTED`: el host produce `REQUIRES_HUMAN` con la autoridad que decide nombrada; el registro durable vive en el plan (pending decisions, findings). **Gap**: la decisión humana se registra en el artefacto dueño, y **nada responde «qué decisiones humanas están pendientes»** — el inventario más completo de esas decisiones está fuera del repositorio (§1 punto 11).

Gaps concretos, con evidencia:

- `GAP` **C-1** — El conflicto normativo no tiene detección mecánica en DEV. `GAP` con impacto: **un conflicto puede existir y la batería estar verde**. Evidencia de primera mano: `MASTER_PENDING_WORK_INVENTORY.md:CON-16` documenta que `docs/rfc/72-...md` afirma que el repositorio «no tiene hoy un contrato de materialización canónica» mientras `runtime/toolcalls/canonical.py` implementa `ORDERING_CONTRACT_V1`/`V2` — una afirmación falsa dentro de una RFC `Accepted`, con la batería verde.
- `GAP` **C-2** — La escalación por incertidumbre **no distingue «no puedo determinarlo» de «puedo, pero no está escrito»**. Es el gap central de §4.2.
- `GAP` **C-3** — La excepción legítima (placement) es documental y no descubrible (§1 punto 7; `PC-27`/`PC-30`/`PC-31a`).
- `CONTRADICTION` **C-4** — `docs/placement-contract.md` afirma que el enforcement mecánico «is **not implemented**» y que «no checker, resolver, service … exists», mientras `runtime/placement/` y tres suites existen. Registrado y **deliberadamente no corregido** por el plan 131 (`MASTER_PENDING_WORK_INVENTORY.md:CON-13`, `DF-21`); `PC-72.1` lo reconcilia en la sección de enforcement pero la sección de non-goals sigue afirmando lo contrario.
- `GAP` **C-5** — El Protocol tiene una jerarquía de prevalencia **declarada** para sus propias fuentes internas («the canonical document prevails», `OPERATIONAL_RULES.md`), mientras DEV declara **no** tener jerarquía universal. Son dos modelos distintos de la misma pregunta, y la frontera impide compartirlos por diseño (`docs/CONVENTIONS.md`). Es correcto, pero significa que **cada capa debe resolver el mismo problema dos veces**.

### 5.3 Caso de estudio: el Change del review (`docs/architecture-capability-review.md`)

`FACT` — Reconstrucción verificada:

1. El artefacto existe, está **untracked**, y declara (§Placement, §11.8, §12.5): clase documental «Working / Analysis (provenance) — no normativo»; que se creó «en la ruta que el Change que lo autoriza especificó de **forma explícita**»; que por su clase la familia `Working analysis` de `docs/placement-contract.md:6` apunta a `docs/working/{audits,research,proposals}/` y que `docs/architecture/` está declarado `archived` en `docs/AGENTS.md:Folder → class map`; que «La instrucción explícita del mantenedor **prevalece** sobre la resolución automática»; que «la divergencia se **registra** y **no** se resuelve por reinterpretación del contrato (`PC-75`)»; y que si el mantenedor desea alinear ubicación y clase, «es una decisión con su propio Change».
2. Su baseline fue `dev` @ `820da21`, `protocol/.agents/VERSION` = `11.6.2` — **el mismo HEAD que el estado actual**. Es decir, el review es el artefacto **más reciente** del árbol de trabajo, posterior al plan 149.
3. Su §12.5 verifica `git status --porcelain` → `?? MASTER_PENDING_WORK_INVENTORY.md` + `?? docs/architecture-capability-review.md`, y `git diff --name-only HEAD` **vacío**.
4. Cierra con `REQUIRES_HUMAN_DECISION` sobre «cómo se registra este análisis en la gobernanza (¿Plan propio? ¿insumo del Change de la Etapa A? ¿`docs/plans/INDEX.md`?)» y declara que el análisis «queda entregado como artefacto de evidencia».

`FACT` — No existe **ningún** Plan numerado que corresponda a ese Change: el corpus va `01`–`149` con `149-argentos-capability-and-autonomy-roadmap.md` como último; no hay plan 150, ni fila en `docs/plans/INDEX.md`, ni entrada en `CHANGELOG.md`, ni RFC/ADR asociado. Verificación: búsqueda de `PLAN-150`/`Plan 150`/`plan 150` sobre todo el repositorio → **0 coincidencias relevantes** (solo dos coincidencias incidentales de la cadena `150-` dentro de citas de líneas de `INDEX.md`).

**Interpretación (con la disciplina de no convertir inferencia en decisión):**

- `PARTIALLY_IMPLEMENTED` — **Qué funcionó.** El conflicto entre una instrucción explícita del mantenedor y la resolución automática del contrato de placement **no se resolvió por inferencia**: se aplicó la instrucción (el mantenedor es la autoridad del dominio DEV, `PC-52`: «A request is **not** an authorization. If the requester holds the domain's authority, the correct action is to record the exception and then place»), se registró la divergencia y se declaró la decisión pendiente. Es exactamente el comportamiento que la hipótesis §5.1 prescribe. El caso **valida** el modelo.
- `GAP` — **Qué no funcionó.** El Change quedó **sin representación en la gobernanza**: sin Plan, sin fila, sin changelog. La regla `PC-52` exige «record the exception **and then place**»; el registro de la excepción existe **dentro del propio artefacto**, que es «el artefacto que ya posee la decisión» según `PC-27` — pero **no existe un artefacto de gobernanza que la posea**, porque el Change no tiene Plan. La excepción quedó registrada en el lugar correcto de una cadena que **no tiene eslabón de gobernanza**. Es el gap `C-3` visto en concreto.
- `HYPOTHESIS` (evaluada, con evidencia parcial) — *«El caso del review fue un error.»* **Veredicto: no.** La evidencia muestra: (a) una instrucción explícita de la autoridad del dominio, que `PC-52` obliga a honrar y a registrar como excepción; (b) el registro efectivo de la divergencia; (c) la declaración explícita de la decisión pendiente; (d) la verificación read-only del alcance; (e) contenido sustantivo con evidencia citable y autocorrecciones registradas (§3 nota 1–3; §12.3 I-1…I-5; §12.4 limitaciones). Un error habría sido **inferir** que la instrucción implícitamente autorizaba también el registro, o **reinterpretar** el contrato para que la ruta «encajara». No ocurrió ninguna de las dos.
- `HYPOTHESIS` — *«Fue una excepción legítima.»* **Veredicto: sí, y precisamente por eso es evidencia del límite.** La excepción fue legítima y aun así produjo un artefacto sin hogar: la legitimidad de la excepción no resuelve el problema de **dónde vive el Change que la autorizó**.
- `HYPOTHESIS` — *«Fue una deficiencia del modelo.»* **Veredicto: sí, en un punto acotado y nombrable.** La deficiencia no es la regla de conflicto ni la de placement: es que **el intake no tiene una vía para un Change cuya autorización es una instrucción directa del mantenedor y cuyo producto es un documento de análisis de un solo archivo**. Las vías existentes son: Plan (requiere que alguien lo redacte y lo apruebe) y Clase C/L0 (acotado a corrección mecánica / un archivo sin cambio estructural). Un análisis arquitectónico de un archivo **no es** una corrección mecánica (cambia significado: introduce hallazgos, conclusiones y decisiones pendientes), y por lo tanto **no califica** como C; y no tiene Plan. La clasificación correcta del caso, por la regla vigente (`change-lifecycle.md:1`, «Do not invent categories; reuse the origin/type vocabulary above»), es `origen/tipo = direct maintainer action` con Change Level L1 (una capa, aditivo, docs-only) — y para L1 la matriz de `docs/plans/94-...:9.2` exige «**Plan/Nota** (según clase RFC-56)». Existía entonces una vía declarada — una **Nota** — y no se usó. `INFERENCE`: la vía «Nota» existe en la matriz pero no tiene contrato, plantilla ni plantilla de registro; es el eslabón con nombre y sin forma.

### 5.4 Densidad de reglas vs densidad de registro

`FACT` — Un patrón que la investigación encontró repetido y que conviene nombrar, porque es el hallazgo de gobernanza más consecuente: **ARgentOS tiene una densidad de reglas muy alta y una densidad de registro baja**.

- Las reglas están declaradas con precisión y en varios niveles (Constitución: `AGENTS.md`; normativa: `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`, RFC/ADR; operación: `.agents/policies/*`, `.agents/workflows/*`; contrato y estándar del payload).
- El **registro** de lo que esas reglas producen vive en prosa dentro de artefactos que también son historia (planes), en INDEX que son espejos por forma, y en pending decisions dentro del artefacto dueño.
- Consecuencia verificada: los defectos más consecuentes del repositorio **no** fueron detectados por su herramienta (§1 punto 11; `MASTER_PENDING_WORK_INVENTORY.md:§9`), y la gobernanza tuvo que **regularizarse a sí misma** de forma recurrente (la propia crítica de `docs/AUDITORIA_DOCUMENTACION.md:Feedback crítico`: «la gobernanza escala peor que el protocolo … Cuando la gobernanza necesita regularizarse a sí misma cada dos semanas, la señal es que el proceso pide más ceremonia de la que el riesgo real justifica»). Esa crítica es de 2026-08-15 y el corpus creció de 58 RFCs/57 planes a 80 RFCs/149 planes desde entonces: **el diagnóstico sigue vigente y cuantitativamente agravado**.

---

## 6. Work Granularity Analysis

### 6.1 ¿Qué representa realmente un Plan en ARgentOS?

`FACT` — Un Plan es **siete cosas a la vez**, y esa es la causa raíz de que la granularidad sea confusa. Evidencia: `docs/plans/_TEMPLATE.md` y cualquier plan reciente (p. ej. `docs/plans/149-...`).

| Rol que cumple el Plan | Sección del template | Qué es en términos de gobernanza |
|---|---|---|
| Registro de intake y clasificación | header (`**Status:**`, `**Fecha:**`, `**RFC:**`, `**Clase:**`, `**Change Level:**`, `**Depende de:**`, `**Origen:**`) | el **primer artifact del cambio** (RFC-75 Mecanismo 1) |
| Declaración de intención | `## Objetivo` | propósito |
| Habilitación de ejecución | `**Status:** Aprobado para ejecución` + `## Criterio de entrada` | **la autorización** |
| Declaración de alcance delegable | `## Delegación agentiva` (`Task` + `Scope`) | **el envolvente de SAE** |
| Contrato de trabajo | `## Entregables`, `## Pasos`, `## Criterios de salida` | la especificación |
| Evidencia de validación | `## Verificación`, `## Validation anchor` | **el anchor** (VC-1) |
| Cierre y gobernanza derivada | `## Checkpoint / cierre` (commits, estado validado, identidad de cierre, consistencia, governance aplicada, **Documentation impact**, **Roadmap impact**, condición derivada) | **el checkpoint** (GC-1) + las determinaciones de cierre |
| Lineage | `## Findings / Correcciones / Pending` | el namespace de refs calificadas `<PLAN-NN>:F-n` / `C-n` / PC |
| Traza histórica | `## Nota de ejecución`, estados finales | el registro de lo que ocurrió |

`FACT` — Es decir: **el Plan es simultáneamente la unidad de autorización, la unidad de trabajo, la unidad de evidencia y la unidad de historia.** La afirmación del review de capacidad de que la «unidad ejecutable, identificable, delegable, persistible, verificable y recuperable» ya existe como `Plan + Delegation + WorkerResult + declared_scope + Validation Anchor + journal` (`docs/architecture-capability-review.md:§4.1`) es correcta, y esta investigación la precisa: la unidad **existe**, y está **sobrecargada por diseño**. El propio review ya advirtió que introducir una entidad `WorkUnit` sería «una segunda representación» prohibida por la regla de una sola fuente de verdad — conclusión que esta investigación **comparte** (§13, alternativa E).

**Respuesta a la pregunta principal de esta línea:** un Plan **no** es «un tipo de trabajo». Es **la autorización y el expediente de un Change**. Confundirlos es lo que hace que cambiar el tipo de trabajo exija redactar un Plan nuevo en lugar de derivar obligaciones distintas.

### 6.2 Evaluación crítica de la hipótesis «Feature/objetivo» + «Work Type»

`HYPOTHESIS` — *«Conviene separar Feature/objetivo ("qué estamos construyendo") de Work Type ("qué estamos haciendo respecto de esa Feature").»*

**Veredicto: la separación es conceptualmente correcta y hoy no es representable sin agregar vocabulario; el segundo eje es el que falta.**

- `FACT` — El eje «Feature/objetivo» **no existe en DEV** como entidad. Lo más cercano es: el `## Objetivo` de un Plan; la **serie** (`Serie:` en el header de RFC + relaciones RFC↔Plan verificables, RFC-75 Mecanismo 11: «identidad **derivada** … sin entidad/registry/artifact de Series»); y la agrupación por roadmap (Etapas A/B/C en `ROADMAP.md`). Es decir: **el repositorio ya tiene un mecanismo derivado y sin entidad para agrupar trabajo relacionado**, y ese mecanismo (serie) es el candidato natural a ocupar el lugar de «Feature» **sin crear nada**. `DESIGN_OPTION`.
- `FACT` — El eje «Work Type» **no existe en absoluto** (§2.6: 0 coincidencias). Su ausencia tiene una consecuencia precisa y verificable: **el conjunto de artefactos y gates obligatorios no depende de qué se está haciendo, sino de cuánto pesa** (Task Profile en el Protocol, Change Level en DEV). Un «análisis» y una «implementación» del mismo peso reciben el mismo tratamiento, aunque uno no produzca código y el otro no produzca decisión.
- `CONTRADICTION` (menor, pero real) — El **único** lugar donde DEV distingue cualitativamente el trabajo es el status del Plan: `Aprobado para redacción` = «entregables documentales: RFCs, estándares» vs `Aprobado para ejecución` = «entregables de implementación o cambios en el repo» (`docs/CONVENTIONS.md:Convenciones`). Es un eje de **dos valores** que mezcla «qué producto» con «si puedo tocar el repo», y que hoy **no se usa** (0 planes en ambos estados, §7). Existe un eje de tipo de trabajo, es binario, está declarado como parte del ciclo de status, y está inerte.

### 6.3 Evaluación de la taxonomía propuesta

`HYPOTHESIS` — *investigation / design / decision / specification / implementation / verification / dogfood / documentation / release.*

**Veredicto: la taxonomía es plausible, casi enteramente mapeable a artefactos existentes, y NO requiere un artefacto separado por tipo. Lo que falta no es la lista: es la declaración.**

Evidencia de que cada tipo ya tiene vehículo en ARgentOS:

| Tipo propuesto | Vehículo existente | Evidencia | ¿Necesita artefacto nuevo? |
|---|---|---|---|
| `investigation` | Working/Research, Working/Audit; discovery del Protocol | `docs/AGENTS.md:Folder → class map`; `docs/working/research/`, `docs/working/audits/`; `orchestrators/discovery/` | No |
| `design` | RFC (modelo y propuesta); `docs/architecture/` como provenance | `docs/AGENTS.md` (Governance/RFC) | No |
| `decision` | ADR; `DELIBERATION_REPORT.md` (veredicto advisory) | `docs/adr/`; RFC-77 | No |
| `specification` | contratos/estándares del payload; `TASK_SPECIFICATION.md`; EARS | `protocol/.agents/contracts/`, `standards/` | No |
| `implementation` | Plan `Aprobado para ejecución` + cambios | `.agents/workflows/change-lifecycle.md` | No |
| `verification` | Validation Anchor; `VERIFICATION_REPORT.md`; C-1/C-2/C-3; rúbricas | `validation-closure.md`; RFC-65 | No |
| `dogfood` | informes de dogfood en `docs/working/audits/`; dogfood de la batería | `docs/working/audits/DEV_*_DOGFOOD_*.md` | No |
| `documentation` | planes docs-only; RFC-69; determinación `Documentation impact` | `docs/VERSIONING.md:3` (docs-only sin versión) | No |
| `release` | promoción + tag; `docs/VERSIONING.md:6`; release de gobernanza (§3) | `docs/VERSIONING.md:1,3,6` | No |

`DESIGN_OPTION` — La conclusión práctica: si se adoptara una taxonomía, el lugar correcto **no** es un artefacto nuevo por tipo, sino **una declaración en el header del Plan** (junto a `**Change Level:**`, que ya se declara allí), de la que se deriven: (i) si el Change toca `protocol/.agents/` (clase RFC-56), (ii) qué determinaciones de cierre aplican, (iii) qué gates corren, (iv) si produce versión. Eso reutiliza el patrón «clasificación en el primer artifact» que RFC-75 Mecanismo 1 **ya exige** y que hoy solo cubre origen/tipo, clase, Level, scope, riesgo y coordinación — **no** tipo de trabajo.

`CONTRADICTION` (de vocabulario, a registrar) — `protocol/.agents/features.toml` usa «feature» para **flags de capacidad**, no para unidades de trabajo. Introducir «Feature» como unidad de trabajo en DEV sin calificar el término crearía exactamente el problema que `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (D1–D5)` previene (términos overloaded requieren calificación obligatoria en contexto cross-layer; y si el dominio no puede inferirse, «el agente **no debe asumir semántica**»).

### 6.4 ¿Deberían varios tipos de trabajo coherentes sobre el mismo objetivo formar una unidad gobernada?

`HYPOTHESIS` — *«Múltiples tipos de trabajo coherentes sobre una misma Feature deberían poder formar parte de una misma unidad de trabajo gobernada.»*

**Veredicto: SÍ en cuanto a gobernanza, con una precisión importante sobre las unidades.**

- `FACT` — La gobernanza **ya permite** que un objetivo coherente se materialice en varios artefactos y varios planes: RFC-75 Mecanismo 11 (serie: identidad derivada, «supersession de miembros no disuelve la serie»), checkpoint multi-commit y multi-Plan («cada Plan cierra con su propio checkpoint; sin registry»), y post-close por referencia (Mecanismo 12). También permite lo inverso: un Plan que abarca documentación + implementación + cierre (es el caso normal).
- `GAP` — Lo que **no** existe es una unidad que declare «este conjunto de trabajos distintos persigue un objetivo y comparte autorización y evidencia». La serie se acerca, pero es **descriptiva** (identidad derivada de declaraciones; el INDEX es «vista descriptiva, nunca autoritativa», `AU-4`) y **no confiere autorización**. Es decir: hoy la respuesta es «sí pueden agruparse para *navegar*, no para *autorizar*».
- `DESIGN_OPTION` — Tres formas evaluadas de dar unidad gobernada sin entidad nueva: (a) **una autorización, varios planes hijos**: el plan "madre" declara Task y Scope del conjunto y los hijos heredan por referencia; requiere una regla de herencia de scope que hoy **no existe** (y que `§1.2`/`§1.3` harían delicada: la autorización es del plan que la declara). (b) **una serie con declaración de autorización**: la serie deja de ser solo identidad derivada y pasa a declarar un objetivo común; cambia la semántica de un mecanismo existente (más invasivo). (c) **no agrupar**: mantener un Plan por Change y agrupar solo por navegación (estado actual). Ninguna de las tres está justificada por evidencia hoy: no hay un caso demostrado de trabajo multi-tipo coherente que hoy resulte ingobernable. `HUMAN_DECISION_REQUIRED` si se quisiera adoptar (a) o (b).

---

## 7. Plan/RFC Corpus Analysis

### 7.1 Conteo mecánico (reproducible)

`FACT` — Comandos y resultado (sobre `dev` @ `820da21`):

```text
docs/plans  : 158 archivos totales; 153 con nombre `NN-*`; números distintos: 149 (01..149);
              4 archivos anexos bajo los números 18 y 19 (18 x3, 19 x3).
docs/rfc    : 82 archivos; 80 RFCs (`00-`..`79-`) + `INDEX.md` + `_TEMPLATE.md`.
docs/adr    : 18 ADRs numerados + `_TEMPLATE.md` + `INDEX.md`.

Composición exacta del directorio (158 archivos):
  149 planes numerados (01..149, sin huecos) + INDEX.md + _TEMPLATE.md
  + 3 documentos de soporte sin número (analisis-explicitud.md, ec-pipeline-vision.md, skills-mechanism.md)
  + 4 anexos sin número que pertenecen a planes numerados (18-anexo-a, 18-anexo-b, 19-anexo-a, 19-anexo-b)

Estados de plan (línea `**Status:**`, normalizada quitando el paréntesis):
  Executed .......................... 151  = 149 planes numerados + los 2 anexos del plan 18
  Sin `**Status:**` ................. 2    (`19-anexo-a-bitacora-fricciones.md`, `19-anexo-b-reporte-estado.md`)
  Otros valores, solo en soporte .... 2    (`analisis-explicitud.md`: `vigente`; `ec-pipeline-vision.md`: `Vision Document — completada`)
  Único no-`Executed` entre los numerados: 1 (`41-rfc-plan-status-governance.md`: `Executed (parcial cerrado el 2026-08-12: …)`)
  → Los 149 planes numerados están en estado terminal `Executed`. 0 `Superseded`. 0 `Aprobado para redacción`.
    0 `Aprobado para ejecución`. 0 abandonados por estado. **Ningún estado no terminal sobrevive en el corpus.**

Cobertura de los campos del lifecycle (sobre los archivos con header de plan):
  `**Change Level:**` ...................... 55 de 156   (78, 96–149)
  `**Clase:**` (RFC-56) .................... 92 de 156   (58–149)
  `**Serie:**` en el header ................ 1 de 156    (115) — la serie es identidad derivada del campo `RFC:`
  `## Validation anchor` ................... 55 · `## Checkpoint( / cierre)` 53 · `## Findings / Correcciones / Pending` 53
  `## Delegación agentiva` ................. 13
  → 101 archivos no tienen ni anchor ni checkpoint ni Change Level: es **legacy declarado**, no invalidez (RFC-75 Mecanismo 15).

Estados de RFC (línea `**Status:**`):
  80 de 80 = `Accepted`. 0 `Proposal`. 0 `Superseded`. 0 `Rejected`. 0 `Draft`.
  (El único `Proposal` del árbol es `docs/rfc/_TEMPLATE.md`, que es plantilla.)

ADRs: 18 de 18 = `Accepted` (`docs/adr/INDEX.md`).

Búsqueda de taxonomía de tipo de trabajo (`work_type|work-type|tipo de trabajo`) en todo el repositorio: 0 coincidencias.
Búsqueda de `PLAN-150|Plan 150|plan 150` en todo el repositorio: 0 coincidencias relevantes.
Marcadores `TODO|FIXME|XXX|HACK` en `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/`: 0.
```

`FACT` — **Consecuencia central:** los campos de estado del corpus **no contienen información de vigencia**. Un lector —humano o agente— no puede distinguir, por estado, un RFC que rige de un RFC que fue reemplazado, ni un plan que describe el sistema actual de uno que describe un sistema que ya no existe. Todos dicen `Accepted` o `Executed`.

### 7.2 Clases de documentos realmente presentes en el corpus

`FACT` — Estas son las clases que la evidencia permite identificar, con ejemplos citados. **Ninguna se modifica ni se archiva en esta investigación.**

| Clase | Evidencia citada | ¿Distinguible mecánicamente hoy? |
|---|---|---|
| **Decisiones vigentes** | RFC-75 (Change Lifecycle), RFC-56 (clases del payload), RFC-63/67 (lifecycle de estado y de conocimiento), ADR-15/16/17/18, `docs/placement-contract.md` (deriva de ADR-17/18) | `PARTIALLY`: por ser citados desde documentos activos (`.agents/`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`), no por un campo |
| **Decisiones superseded (en prosa)** | RFC-68 reemplazó la propuesta `docs/working/proposals/WORKFLOW_PROPOSAL.md` (índice: «archived (superada por RFC-68, plan 82)»); `docs/rfc/01-...md:277` marca una sección como «quedó **superseded**»; `docs/plans/02-...md:11` «parcialmente superseded por RFC-00YB/00YC» | `NO`: prosa; 0 estados `Superseded` en el corpus |
| **Investigaciones** | `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md`, `PROMPT_CACHE_PHASE_1_REPORT.md`; `docs/working/audits/*`; el propio `docs/architecture-capability-review.md` | `PARTIALLY`: por carpeta (Working), y por el INDEX liviano de cada carpeta |
| **Propuestas** | `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` (adoptada como capability DEV, Working no normativa); `docs/rfc/*` en `Proposal` → **0 hoy** | `PARTIALLY` |
| **Implementaciones** | 149 planes `Executed` | `SÍ` por estado — pero sin información de vigencia |
| **Experimentos** | `docs/plans/114`/`116`/`117` (MVP de deliberación adversarial: «experimento MVP … **cerrado**», «Human Checkpoint», `JURY_TRIAL_CLOSED`) | `NO`: prosa dentro de planes `Executed` |
| **Decisiones rechazadas** | RFC-56 `Alternativas consideradas` («Solo dos clases (A y B): descartada»); ADR-03 «Opción A/B/C»; `WORKFLOW_PROPOSAL` → RFC-68 descartó la automatización total | `NO`: sección de prosa; el vocabulario `rejected` existe en ADR-03 como **evento**, no como estado de artifact |
| **Trabajo abandonado** | `docs/VERSIONING.md:7` «`Abandoned` = Plan `Superseded` con motivo» — **estado inalcanzable en la práctica** porque `Superseded` exige nombrar el reemplazante (`docs/plans/137-...md`; `docs/plans/140-...md`; `docs/plans/INDEX.md` fila 88) | `NO`, y **no representable** → `CONTRADICTION` (el ciclo lo declara; el ciclo no lo permite) |
| **Duplicados / ownership duplicado** | `MASTER_PENDING_WORK_INVENTORY.md:SUP-9` (`<PLAN-125>:PC-1` duplicada con `docs/adr/17`), `SUP-7`, y las resoluciones «ownership duplicado → `superseded`» de planes 128/130 determinadas por el plan 141 | `NO`: detectado por lectura cruzada |
| **Evidencia histórica** | `docs/architecture/ARCHITECTURAL_*_MODEL.md` (banner «⚠ Snapshot histórico — análisis preservado (2026-08-25)», «no es un documento vivo», «su contenido no debe leerse como estado normativo actual»), citados 65 veces desde documentos vivos | `SÍ` por banner + declaración de clase (`docs/AGENTS.md`: `docs/architecture/` = Historical `archived`) — **el mejor ejemplo del modelo funcionando** |
| **Documentación que ya no representa el estado actual** | **16 cabeceras de RFC** que leen «diseño aprobado, ejecución pendiente vía su plan» mientras sus planes están `Executed` (RFC-38→plan 37 … RFC-54→plan 53); `docs/plans/INDEX.md:210` («pytest 316 passed») vs plan 91 («331 passed»); `docs/rfc/72:129` afirmando que no existe contrato de materialización canónica; planes 92/93 afirmando que 90/91 no se ejecutaron; `docs/rfc/03` con banner de enmienda pendiente ya aplicada | `NO`: 20+ instancias documentadas en `MASTER_PENDING_WORK_INVENTORY.md:§7` (CON-13…CON-21), **con la batería en verde** |
| **Ítems de backlog nunca promovidos** | `docs/plans/19-anexo-a-bitacora-fricciones.md` §F-18 (delimitador del front matter de KB entry) «aparece en **ni** `ROADMAP.md` ni ningún CHANGELOG» (`MASTER_PENDING_WORK_INVENTORY.md:CON-15`, `DF-10`) | `NO` |
| **Ciclos de checkbox sin marcar** | 89 planes numerados tienen ≥1 casilla `- [ ]` sin marcar en `## Criterios de salida` mientras su header dice `Executed`; p. ej. plan 138: 17 sin marcar, 0 marcadas (`MASTER_PENDING_WORK_INVENTORY.md:CON-9`, `SUP-22`) | `SÍ` mecánicamente, y **ese es el punto**: es detectable y no se detecta |

`FACT` — El corpus contiene, entonces, **al menos once clases distintas de documento** bajo **dos estados** (`Accepted`, `Executed`). La clasificación existe; la representación no.

### 7.3 La contradicción estructural del ciclo de planes

`CONTRADICTION` — El ciclo de status de planes declara `Superseded` («reemplazado; **indicar por qué plan**») y `docs/VERSIONING.md:7` deriva `Abandoned = Plan Superseded con motivo`. Pero `Superseded` **exige** un plan reemplazante, y cuando el trabajo simplemente se retira no hay ninguno. La situación está registrada **cuatro veces** de forma independiente: `docs/plans/88-rfc71-implementation.md:648` («no existe `delete`/`cancel` en el ciclo de status y `Superseded` exige un plan»), `docs/plans/137-...md:366,387` («`Superseded` **no** es una salida disponible, porque … exige un plan reemplazante que no existe»), `docs/plans/140-...md:98`, y `MASTER_PENDING_WORK_INVENTORY.md:HD-1`. Y el plan 137 **quedó en `Aprobado para redacción` durante semanas** precisamente porque no había salida: ni ejecutar (no autorizado), ni retirar (estado inexistente). Finalmente se resolvió ejecutándolo (plan 141).

`FACT` — Consecuencia para la pregunta central: **el ciclo de vida de los artefactos de gobernanza no puede expresar «ya no se hará»**. Cualquier sistema que quiera que un agente no trate trabajo abandonado como trabajo pendiente necesita antes poder **nombrar** el abandono.

### 7.4 El espejo y su verificación

`PARTIALLY_IMPLEMENTED` — `docs/plans/INDEX.md` (1609 líneas) es el espejo descriptivo del corpus; `docs/AGENTS.md:INDEX y CONVENTIONS` declara que «registran todos los artefactos (mirror mecánico verificado por `tools/check_plan_structure.py`)». La verificación es **estructural** (nombre, status dentro del ciclo, ausencia de placeholders, Amendment Log en RFCs, registro en el INDEX) — `docs/CONVENTIONS.md:Plantillas`. **No** verifica que el contenido de la fila sea verdadero. Evidencia del efecto: `MASTER_PENDING_WORK_INVENTORY.md:§7` documenta 20+ filas stale, incluida una que presenta `F-14`, `F-17`, `F-18` como resueltos por planes 37–43/53/58 cuando el payload todavía muestra los tres gaps (`SUP-4`), y un mislabel de ID de fricción (`F-17` vs `F-19`, `SUP-5`).

`FACT` — El INDEX tiene además un problema de **roles acumulados**, ya diagnosticado internamente en 2026-08-15: «El INDEX carga demasiados roles: índice, backlog, convenciones, snapshot de estado, notas de regularización. Funciona, pero es frágil como fuente citada por todo el mundo» (`docs/AUDITORIA_DOCUMENTACION.md:Puntos débiles`). Parte se migró a `docs/CONVENTIONS.md` (RFC-69, plan A), pero el INDEX conserva todavía: prólogo de estado, series, tablas por serie, backlog evidenciado, documentos de soporte, extensiones futuras, anclas de convenciones históricas y archivo.

### 7.5 Qué hacer conceptualmente con el corpus (evaluación, no decisión)

`HYPOTHESIS` — *«Todos los documentos del corpus deben conservar su estatus actual.»* **Verdicto: FALSO, y el repositorio ya lo sabe.** El propio corpus declara que parte de su contenido dejó de representar el sistema (16 cabeceras de RFC, filas INDEX stale, afirmaciones falsas en RFC `Accepted`) y que el trabajo abandonado no es representable. Conservar el estatus **formal** (`Accepted`/`Executed`) es correcto y obligatorio (RFC-46: la traza no se reescribe). Conservar la **pretensión de vigencia** no lo es: es lo que produce la lectura equivocada.

`DESIGN_OPTION` (evaluado, no adoptado) — Tres grados de intervención, ordenados por coste y por reversibilidad:

- **A (mínimo): declarar vigencia sin tocar el contenido.** Cada artefacto de gobernanza gana un campo de vigencia **en su cabecera**, con el vocabulario **ya declarado** en `docs/AGENTS.md:Lifecycle` (`active`/`archived`/`superseded`/`deprecated`) y un puntero opcional al sustituto. No se reescribe nada; el campo es metadata evolucionable, exactamente como el estado de un finding (`LC-1`: «metadata de lifecycle (estado y resolución) puede evolucionar preservando el histórico»). Los 149+80+18 artefactos se clasifican una vez, con decisión humana donde haga falta; los nuevos nacen declarados.
- **B (intermedio): además, un índice de vigencia.** Una vista derivada —no un registry— que responda «qué rige hoy». Reutiliza el patrón «INDEX = vista descriptiva, nunca autoridad» (`AU-4`). Riesgo: agrega un artefacto a mantener, y `docs/AGENTS.md` ya declara que un INDEX es **opcional y semántico**, no obligatorio por simetría.
- **C (máximo): derivar la vigencia de las referencias.** Calcular la vigencia a partir de qué documentos citan a cuáles desde contexto activo. Es la opción más elegante y la más frágil: `check_plan_citations` ya verifica existencia, no verdad; derivar vigencia de la densidad de citas confundiría «muy citado» con «vigente» (un documento histórico muy citado —`docs/architecture/`, 65 citas— sería clasificado vigente). **Se descarta** con evidencia.

`FACT` — Un cuarto camino **ya está en uso y funciona**: el **banner de snapshot histórico** de `docs/architecture/*.md`, que declara explícitamente «no es un documento vivo», «no se actualiza retrospectivamente», «su contenido no debe leerse como estado normativo actual» y a qué estado del repo corresponde. Es exactamente el comportamiento que un modelo de vigencia necesita — y hoy es **artesanal**: se escribió a mano en dos archivos. `DESIGN_OPTION`: generalizar la *forma* del banner (no el mecanismo) al resto de las clases que hoy no la tienen es la intervención de menor coste con mayor efecto de lectura.

---

## 8. Knowledge Lifecycle Analysis

### 8.1 Cinco vocabularios de ciclo de vida, ninguno conectado

`FACT` — ARgentOS tiene hoy **cinco** modelos de lifecycle distintos, con vocabularios distintos, en dominios distintos, sin traducción entre ellos:

| # | Modelo | Estados / valores | Dónde está declarado | ¿Se usa? |
|---|---|---|---|---|
| 1 | **Documental DEV** | `active` / `archived` / `superseded` / `deprecated` (coexistencia permitida: `superseded ∧ archived`) | `docs/AGENTS.md:Lifecycle`; `docs/rfc/69-...md:117-125` | `PARTIALLY`: `archived` vía banner artesanal (2 archivos); los otros tres, no escritos |
| 2 | **Gobernanza DEV (RFC/ADR/Plan)** | RFC/ADR `Proposal → Accepted → Superseded`; Plan `Aprobado para redacción` / `Aprobado para ejecución` / `Executed` / `Executed (parcial)` / `Superseded` | `docs/CONVENTIONS.md:Convenciones`; `docs/VERSIONING.md:7` | `NO` para los estados no terminales (§7.1) |
| 3 | **Artifact Lifecycle del Protocol** | `draft` → `validated` → `superseded`; propiedades `archived`, `rejected`; eventos `produced`/`corrected`/`gate_passed`/`gate_failed` | `docs/rfc/63-...md:126-145`; `docs/adr/03-artifact-lifecycle.md`; `protocol/.agents/harness/INDEX.md:State dimensions` | `IMPLEMENTED`: **derivado** del Gate State, nunca escrito a mano (`AL-1`/`AL-2`); verificado por `gate_validator.py` y `check_session_artifacts.py` |
| 4 | **Conocimiento del Protocol (KB)** | tipos `snapshot` / `claim` / `lesson`; frescura por claim (TTL + provenance resoluble); `curation_status` `active` / `noisy` / `retired`; `kind` distingue `historical` de `current` | `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`; `KNOWLEDGE_CURATION.md`; `docs/adr/10-knowledge-lifecycle.md`; RFC-67 | `IMPLEMENTED` en el payload (payload 9.0.0: `KNOWLEDGE_LIFECYCLE`, `kind`/`path` en `KB_RECOMMENDATION`, `invalidated_facts` en `EXECUTION_SUMMARY`, checks en `gate_validator.py` y `check_session_artifacts.py`) |
| 5 | **Estado de término del glosario** | `current` / `historical` / `deprecated` / `superseded` / `forbidden` | `docs/glossary/INDEX.md:Status de un término` | `FACT`: todos los términos registrados están `current` (26 entradas) |

`FACT` — Y un sexto, **diseñado y diferido**: el modelo de estados del workflow de evolución arquitectónica de RFC-68 (`Change Kinds`: `NEW`/`MODIFIED`/`CONFIRMED`/`INVALIDATED`/`SUPERSEDED`/`UNAFFECTED`; `Analysis Status`: `NEW|ANALYZED|SUPERSEDED|REMOVED|INVALID`; `Evidence Set`: `OPEN → SEALED → SUPERSEDED`; `Session`: `NEW → ANALYZED → SUPERSEDED|REMOVED|INVALID`; estados de decisión `OPEN / PROVISIONALLY_DECIDED / DECIDED / SUPERSEDED / REJECTED`), con su Fase 1 entregada (contratos + `tools/check_architecture_traceability.py`) y su Fase 2 (propagación mecánica de impacto) **diferida**.

`CONTRADICTION` — El modelo #1 (documental DEV) y el modelo #2 (gobernanza DEV) describen **los mismos objetos** (un RFC es un documento de gobernanza *y* un artefacto documental) con vocabularios distintos y sin regla de traducción. Un RFC `Accepted` con un banner «⚠ Enmienda pendiente» es, simultáneamente, `Accepted` (modelo 2) y `superseded`-en-parte (modelo 1) y no lo dice en ninguno de los dos campos. `docs/rfc/03-context-budget-model.md:13` y `docs/rfc/INDEX.md:86` documentan el efecto: banners presentes con la enmienda ya aplicada, y estado del INDEX contradictorio con el header del propio RFC (`MASTER_PENDING_WORK_INVENTORY.md:CON-19`, 13 casos de status contradictorio).

### 8.2 Evaluación de las categorías propuestas

`HYPOTHESIS` — *categorías `CURRENT`, `SUPERSEDED`, `HISTORICAL`, `REJECTED`, `ABANDONED`, `INVALIDATED`, `DUPLICATE`.*

**Veredicto por categoría**, con el test que la investigación aplicó: *¿existe evidencia en el repositorio que permita determinar la transición, y es determinable mecánicamente o requiere decisión humana?*

| Categoría | ¿Necesaria? | Evidencia que permitiría determinarla | ¿Mecánica? | ¿Humana? |
|---|---|---|---|---|
| `CURRENT` | **Sí** | ser un documento enumerado como de estado actual (`validation-closure.md:5.1`) o estar citado como autoridad por un documento activo; no tener banner de cierre; ser el artefacto **de mayor identidad** de su serie | `NO` (la lista de `5.1` es abierta por diseño) | **Sí** para el borde («¿este documento describe el sistema actual?») |
| `SUPERSEDED` | **Sí** | status del ciclo + puntero al sustituto (header, banner de enmienda, `Amendment Log`, prosa «superado por») | `PARTIALLY`: detectable si existe puntero; **no** si no existe | **Sí** cuando no hay sustituto (hoy es el caso de `Abandoned`) |
| `HISTORICAL` | **Sí, y ya existe** | plan/RFC/ADR cerrado o `Superseded` (RFC-46: «traza histórica»), carpeta declarada `archived`, banner de snapshot | `SÍ` para la clase (status + carpeta); `NO` para el matiz | No para la clase; Sí para el matiz |
| `REJECTED` | **`DESIGN_OPTION`: probablemente no como estado de artifact** | el vocabulario ya existe en ADR-03 como **evento** (`rejected`) y en RFC-68 (decisiones `REJECTED`, análisis `INVALID`); en DEV, una propuesta rechazada es una sección de prosa («Alternativas consideradas … descartada») | `NO` | Sí |
| `ABANDONED` | **Sí, y hoy no es representable** | el ciclo lo define (`docs/VERSIONING.md:7`) pero `Superseded` exige reemplazante | `NO` | **Sí** — y es la carencia más limpia del conjunto |
| `INVALIDATED` | **Sí en Protocol, `DESIGN_OPTION` en DEV** | Protocol: cambio de `content_identity`/`semantic_version`, `invalidated_facts`, claim no fresco, provenance irresoluble (`KN-004`…`KN-006`). DEV: **no hay** vocabulario equivalente; lo más cercano es «la afirmación ya no es verdad» (CON-16…CON-18) | Protocol `IMPLEMENTED`; DEV `NO` | DEV: Sí |
| `DUPLICATE` | **Sí como** *relation*, `DESIGN_OPTION` como **estado** | ownership duplicado es un caso real y resuelto en el corpus (`SUP-9`, `<PLAN-127>:PC-4` vs `<PLAN-131>:PC-3`, `<PLAN-128>:PC-2` vs `<PLAN-131>:PC-1/2`): la resolución aplicada fue `superseded` **con referencia al dueño vivo** | `PARTIALLY`: detectable por comparación de sujeto/declaración, no por campo | Sí para declarar duplicación |

`FACT` — Un hallazgo transversal sobre estas categorías: **tres de las siete ya existen** en el repositorio con otro nombre y en otro dominio (`HISTORICAL` = RFC-46 + docs/AGENTS.md; `INVALIDATED` = Protocol `KNOWLEDGE_LIFECYCLE`; `REJECTED` = ADR-03 property + RFC-68 decision state). Y **dos** de las que faltan (`ABANDONED`, y `CURRENT` como afirmación explícita) son precisamente las que un sistema que deriva contexto necesita para no confundir conocimiento vigente con histórico.

**Conclusión de la evaluación:** la lista propuesta **no** debe adoptarse como lista cerrada y **no** debe crear un sexto vocabulario. La recomendación derivada es **reutilizar `docs/AGENTS.md:Lifecycle`** (`active`/`archived`/`superseded`/`deprecated`, que ya es el vocabulario declarado para artefactos documentales de DEV), **resolver `ABANDONED` dentro de `superseded` ampliando su semántica de puntero a «sustituto o motivo»** (decisión humana), y **mantener `INVALIDATED` y el resto de las categorías epistémicas donde ya viven** (Protocol KB y RFC-68), sin importarlas a DEV.

### 8.3 Trazabilidad: qué existe hoy y qué falta

`PARTIALLY_IMPLEMENTED` — Mecanismos de trazabilidad presentes:

| Relación | Mecanismo | Dirección | Limitación |
|---|---|---|---|
| plan ↔ RFC (normativa) | campo `**RFC:**` del plan; `Serie:`; par changelog `(plan N, RFC-N)` | plan → RFC | no hay índice inverso RFC → planes |
| ADR ↔ D# ↔ RFC ↔ plan | matriz many-to-many en `docs/adr/INDEX.md` | bidireccional por tabla | mantenida a mano |
| amendment | `## Amendment Log` de cada RFC (fecha → qué cambió → origen) | RFC → origen | no dice qué RFC la desplazó |
| supersesión | banner «⚠ Enmienda pendiente: …» bajo el header | documento → modelo vigente | prosa; 0 estados; no es descubrible |
| citas | `check_plan_citations.py` (`ruta:sección` resoluble) | documento → target | verifica existencia, no verdad |
| evidencia | Validation Anchor + `A1 → A2` (lineage histórico, A2 nunca muta A1) | validación → estado Git | por artifact; sin vista agregada |
| findings/correcciones | refs calificadas `<artifact>:F-n`/`C-n`, N:M, elemento inmutable + metadata evolucionable | artifact → origin/evidence | namespace por artifact; sin vista agregada |
| cierre | checkpoint (commits, estado validado, identidad de cierre, consistencia) | cierre → Git | por plan |
| análisis arquitectónico | `tools/check_architecture_traceability.py` (dev-only) + `ARCHITECTURAL_CHANGE_SET`/`EVIDENCE_SET`/manifest | Evidence→Finding→Problem→Decision→RFC | **Fase 1**; la propagación de impacto es Fase 2, diferida |
| series | `Serie(RFC)` = declaración; `Serie(Plan)` = propia ∪ series de su RFC | derivada | descriptiva, nunca autoritativa (`AU-4`) |

`GAP` — **No existe ninguna relación inversa consultable**: nada responde «¿qué documentos citan a este?», «¿qué reemplaza a este?», «¿qué se volvió obsoleto cuando cambié esto?». El único paso en esa dirección es `check_plan_citations`, que es de existencia y se ejecuta como gate, no como consulta. Es exactamente el sustrato que RFC-68 llama «**índice de trazabilidad**» y cuya explotación mecánica («delta engine») está diferida.

### 8.4 «Ya no es vigente» ≠ «ya no tiene valor histórico»

`FACT` — El repositorio **tiene esta distinción resuelta y la aplica**, en tres lugares:

1. `docs/AGENTS.md:Lifecycle`: `archived` = «congelado con banner; **sigue siendo significado histórico; no se borra**»; `deprecated` = «fuera de uso sin reemplazo; se declara antes de eliminar».
2. `docs/rfc/46-historical-trace-policy.md:Decisión propuesta` punto 2: «los artefactos de sesión son registros inmutables del protocolo vigente al momento de la sesión; **no se reescriben ni se regeneran** para "reproducir" con una versión nueva».
3. `.agents/policies/validation-closure.md:5.1` «**Historical exclusion.** Historical documentation is never updated merely because it describes an older state».

Y la formulación más útil para el modelo futuro está en el Protocol (`KNOWLEDGE_LIFECYCLE.md:Historical vs current knowledge`): «**Historical knowledge**: past snapshots and lessons, kept as trace. **Current knowledge**: fresh claims with resolvable provenance, eligible for reuse and recommendation», con la regla de que «the distinction is declared through the `kind` tag; **nothing is reclassified retroactively**».

`DESIGN_OPTION` — Esto último es el modelo a reutilizar conceptualmente en DEV: **declarar la clase, no reescribir el contenido**. La diferencia con el Protocol es que allí la distinción es por **claim** (frescura por claim, con TTL y provenance), y en DEV no hay unidad atómica de conocimiento documental: la unidad es el documento entero. Esa granularidad gruesa es la razón por la cual en DEV la vigencia se resuelve a mano (banner) y en el Protocol se resuelve por pipeline.

---

## 9. Obsolescence and Reconciliation Analysis

### 9.1 El pipeline propuesto, contrastado con lo que existe

`FACT` — El encadenamiento conceptual que la investigación debía evaluar

```text
Change → Impact analysis → Affected knowledge → Reconciliation → Current knowledge
```

**ya existe en ARgentOS, en dos lugares distintos y con dos estados de madurez distintos:**

| Tramo | Dónde está declarado | Estado |
|---|---|---|
| Change → impacto → conocimiento afectado → reconciliación, para **conocimiento arquitectónico** | `docs/rfc/68-architecture-evolution-workflow.md` (`## Change Set`: `RFC Impact` / `RFC Changes` / `Implementation Impact`, `Change Kinds` = `NEW/MODIFIED/CONFIRMED/INVALIDATED/SUPERSEDED/UNAFFECTED`, gates por clase de impacto LOW/MEDIUM/HIGH) + su origen `docs/working/proposals/WORKFLOW_PROPOSAL.md:§24 Impact Analysis` («E203 → Findings affected → Problems affected → Decisions affected → RFCs affected … RFC-A: unaffected / RFC-C: affected») | `PARTIALLY_IMPLEMENTED`: Fase 1 entregada (contratos + `tools/check_architecture_traceability.py`); **«Propagación mecánica de impacto (delta engine sobre el índice de trazabilidad)» es Fase 2, explícitamente diferida** (`RFC-68:1199-1223`) con gates de entrada declarados: telemetría P0, índice de trazabilidad verde sobre sesiones reales, correlación validada sobre ≥2 conjuntos multi-proyecto, decisión explícita sobre el namespace de versionado |
| Change → conocimiento afectado → reconciliación, para **conocimiento de proyecto** | `ADR-10` / RFC-67 / `KNOWLEDGE_LIFECYCLE.md`: `invalidated_facts` en `EXECUTION_SUMMARY.md` → revalidación scoped por el pipeline → entradas actualizadas | `IMPLEMENTED` en el payload (KN-004/KN-006; checks en `gate_validator.py` y `check_session_artifacts.py`) |
| Change → documentación de estado actual afectada → reconciliación, para **documentación DEV** | `Documentation impact` + `Roadmap impact` (`validation-closure.md:5.1/5.2`; `docs/CONVENTIONS.md:499-594`) | `DOCUMENTED_ONLY` **por decisión explícita**: «no checker interprets prose or decides whether a document is up to date, and no checker is added for this»; y el host **no la consulta al derivar `Closed`** (§3.6 c) |

`FACT` — La conclusión es precisa y tiene tres partes:

1. **El concepto general de impacto/reconciliación no hay que inventarlo: ARgentOS ya lo declaró necesario y ya lo diseñó** (RFC-68 Fase 2), con una decisión de secuenciación y unos gates de entrada basados en evidencia. Esta investigación **no** reabre esa decisión; registra que **existe** y que su ausencia no es un olvido.
2. **`Documentation impact` y `Roadmap impact` NO son ese mecanismo.** Son una *determinación de obligación*, hecha una vez por Change, en prosa, por el Change mismo. No detectan, no propagan y no consultan nada. Confundirlas con un mecanismo de impacto es el error de lectura que la evidencia desmiente: la propia policy declara que una `REQUIRED` es «una obligación de estado, nunca una autorización de escritura».
3. **La separación correcta es de tres operaciones distintas**, y esa separación **ya está parcialmente vigente** en ARgentOS: (i) **detectar** qué conocimiento quedó afectado — factual, y mecánicamente parcial (ver §3.6 f); (ii) **determinar** qué obliga — existe (`REQUIRED`/`NOT_REQUIRED`/`DEFERRED`); (iii) **reconciliar** — una escritura, que requiere autorización de scope (`§1.1`: la obligación no autoriza). La regla `Impact classification ≠ authorization` (plan 138/139) es exactamente esta separación entre (ii) y (iii). **Lo que falta es (i) como capacidad consultable**, y falta también que (ii) sea consultada por el ejecutor.

### 9.2 Señales de detección: qué es alcanzable con lo que ya existe

`DESIGN_OPTION` (evaluado, no adoptado) — Cada señal que la investigación debía investigar, con el mecanismo que ya existe y su límite real:

| Señal | Mecanismo existente reutilizable | Límite verificado |
|---|---|---|
| **supersession** | status `Superseded` (declarado en RFC/ADR/Plan) + puntero en header + banner de enmienda + `Amendment Log` | **0 usos en 80 RFCs, 0 en 149 planes, 0 en 18 ADRs**; `Superseded` exige reemplazante; ninguna herramienta verifica el puntero (§3.6 f) |
| **contradicción** | C-1/C-2/C-3 detectan contradicción **léxica dentro de registros de lifecycle** (campos duplicados con valores distintos, `Closed`+`FAIL`, `resolved`+FAIL, `deferred` sin owner, revalidación contra checkpoint FAIL) | la contradicción **semántica entre documentos** está declarada fuera de alcance (`CONVENTIONS.md:587-590`) |
| **duplicación** | claves de entidades taxonómicas, refs de lineage, nombres de efecto | no detecta números de plan/RFC/ADR reutilizados ni documentos que se reafirman; **sí** existe experiencia real de ownership duplicado resuelto a mano (`SUP-9`, `<PLAN-128>:PC-2`) |
| **referencias obsoletas** | `check_plan_citations` (existencia + resolución de sección) y `check_protocol_invariants` (payload) | ninguna de las dos lee links markdown fuera del payload; los `#fragment` se descartan; 93 links rotos medidos en `docs/adr/`+`docs/rfc/` |
| **decisiones reemplazadas** | `Amendment Log` por RFC + matriz `docs/adr/INDEX.md` (D#↔ADR↔RFC↔plan) many-to-many | mantenido a mano; la matriz **nunca se parsea**; 13 status contradictorios medidos (`CON-19`) |
| **artefactos que ya no describen el sistema** | **identidad de contenido**: `anchor_stale` compara la Scoped Content Identity validada contra la actual y una identidad desconocida no se lee como fresca (`observation.py:657-668`) — es el **único** mecanismo mecánico de obsolescencia del sistema | detecta que el **contenido cambió**, no que el documento **dejó de ser verdad**; y nada recalcula la identidad declarada (§3.6 f) |
| **frescura de conocimiento de proyecto** | `reuse_eligibility` → `FRESH`/`STALE`/`UNKNOWN` con TTL + provenance resoluble (`project_segment.py:153-211`), y consistencia manifest↔archivos en `check_discovery_output.py:801-843` | **el host DEV nunca lo invoca** (`orchestrator` no importa `project_segment`) y siempre envía `knowledge_entries=()` |
| **fila de índice vs artefacto** | `check_plan_structure.py:153-159` | verifica **substring del filename**, no el contenido de la fila: 20+ filas stale medidas con la batería verde |

`FACT` — El balance es nítido: **el sistema tiene cuatro mecanismos de obsolescencia reales** (identidad de contenido para validaciones; frescura por claim para conocimiento de proyecto; consistencia manifest↔archivos para el KB de discovery; `ARCHITECTURAL_CHANGE_SET` con `INVALIDATED`/`SUPERSEDED` para el modelo arquitectónico) — y **ninguno de ellos cubre la documentación de gobernanza de DEV**, que es exactamente el corpus que un agente necesita leer para saber qué rige.

### 9.3 Por qué el mecanismo general no debería diseñarse todavía

`HYPOTHESIS` — *«ARgentOS necesita un mecanismo general de detección y reconciliación de conocimiento afectado.»* **Verdicto: sí conceptualmente, y NO como trabajo inmediato, por la evidencia del propio repositorio.**

- RFC-68 Fase 2 fijó **gates de entrada basados en evidencia** (telemetría de costo, índice de trazabilidad verde sobre sesiones reales, correlación validada sobre ≥2 conjuntos). `FACT`: ninguno de esos gates se cumple hoy — no hay telemetría (`METRICS.md`: la dimensión de costo es `Unavailable`), no hay índice de trazabilidad operativo, y hay un solo repositorio fuente.
- El `MASTER_PENDING_WORK_INVENTORY.md` (§9) da la segunda razón con evidencia de primera mano: los cuatro defectos más consecuentes que encontró **no** eran detectables por la herramienta, y **sí** eran detectables por lectura cruzada. Eso sugiere que el cuello de botella inmediato no es la potencia del detector sino **la ausencia de una representación que haga la lectura cruzada innecesaria**.
- `FACT` — La tercera razón es de coste/beneficio y está en el propio corpus: la gobernanza ya se regulariza a sí misma de forma recurrente (`docs/AUDITORIA_DOCUMENTACION.md:Feedback crítico`; planes 140/141/143/144/145 son, todos, cierres de residuos de gobernanza). Añadir un motor de impacto antes de representar la vigencia agregaría mecanismo sin reducir la clase de problema dominante.

`DESIGN_OPTION` — La secuencia que la evidencia sugiere: **(1) representar la vigencia** (barato, reversible, sin entidad: un campo declarado por artefacto + un alcance acotado de «documentación de estado actual»); **(2) hacer que el ejecutor consulte las obligaciones que ya están escritas** (el host no lee policies, §3.6 c); **(3) recién entonces** evaluar la Fase 2 de RFC-68 con sus gates. Esta investigación **no** decide esa secuencia: la propone como opción con su justificación.

---

## 10. Current State vs Historical Knowledge

### 10.1 ¿Dónde está hoy el source of truth del conocimiento vigente?

`FACT` — **No hay un lugar único, y el repositorio lo declara así.** La respuesta por capa:

| Concepto | Source of truth declarado | Evidencia |
|---|---|---|
| Estado del **repositorio** | **Git** (+ tags) | `validation-closure.md:5.1`: «Git remains the authority on the effective state»; `docs/VERSIONING.md:280-282`: «La fuente inmutable de la verdad son `git tag` + `protocol/.agents/VERSION`» |
| **Autoridad normativa** | RFC `Accepted`, ADR, Plan aprobado (`docs/`), y la clase DECISION del mantenedor | `.agents/policies/authority.md:5-14`; `ADR-16` |
| **Instrucción operativa** | `.agents/` (policies, workflows) | `.agents/AGENTS.md:8-14`; `authority.md:49-56` |
| **Estado operativo del trabajo futuro** | `ROADMAP.md` (mapa operativo, no changelog) | `validation-closure.md:5.2` |
| **Navegación / registro** | los tres INDEX (planes, RFC, ADR) — **nunca autoridad** (`AU-4`) | `docs/AGENTS.md:INDEX y CONVENTIONS`; `docs/rfc/INDEX.md:3-5` |
| **Conocimiento de proyecto (Protocol)** | `.project/knowledge/entries/` + `INDEX.md` (**indexer no implementado**) y `.project/knowledge/discovery/` + manifest | `KNOWLEDGE_INDEX.md:4-6,30-32`; `KNOWLEDGE_LIFECYCLE.md` |
| **Estado de gobernanza de un Change de payload** | `.project/changes/<change_identity>.md` — `enforcement = "documented"` | `CHANGE_GOVERNANCE.md:41-52,70-72` |
| **Estado de ejecución DEV** | `.project/orchestrator/` (efímero, no versionado) + el artefacto del Plan (versionado) | `autonomous-orchestration.md:§8,§9` |

`FACT` — Y el conjunto de **documentos de estado actual** no está enumerado de forma cerrada: `validation-closure.md:5.1` da una lista («`docs/VERSIONING.md` §9, `docs/plans/INDEX.md`, `ROADMAP.md`, `README.md`, `AGENTS.md` / `.agents/AGENTS.md` cuando cambia una instrucción activa, las policies y workflows activos …, **más cualquier otro documento que el propio Change identifique como estado actual**»). **La pertenencia al conjunto se decide Change por Change, por juicio, sin registro.**

### 10.2 ¿Puede distinguirse el estado actual de la evidencia histórica?

`PARTIALLY_IMPLEMENTED` — Sí por **clase y por convención**, no por **campo ni por consulta**:

- `FACT` — La taxonomía documental **declara** el lifecycle (`docs/AGENTS.md:Lifecycle`: `active`/`archived`/`superseded`/`deprecated`) y el mapa carpeta→clase marca `docs/architecture/` como **Historical `archived`**. Funciona donde se escribió el banner: dos archivos (`ARCHITECTURAL_PROBLEM_MODEL.md`, `ARCHITECTURAL_DECISION_MODEL.md`) declaran «no es un documento vivo … no debe leerse como estado normativo actual» y a qué estado del repo corresponden, y son citados **65 veces** desde documentos vivos sin confundir a nadie.
- `CONTRADICTION` — Pero **los campos de estado del corpus no contienen información de vigencia**: 80/80 RFCs `Accepted`, 149/149 planes `Executed`, 18/18 ADRs `Accepted`, 0 `Superseded`, 0 `Rejected`, 0 abandonados. Los estados existen y no se usan; la vigencia real se expresa en prosa (banners, `Amendment Log`, «superado por»), y en 20+ casos documentados la prosa **contradice** el estado.
- `CONTRADICTION` — El **mismo INDEX es, simultáneamente, documentación de estado actual y espejo de historia congelada** (§1 punto 9). Es el caso más nítido: `docs/plans/INDEX.md` está en la lista de `5.1` como documento de estado actual, y su contenido es el registro de 149 cambios cerrados, con una fila por plan.

### 10.3 ¿Qué debe leer un worker para conocer el estado actual?

`FACT` — El propio repositorio lo enruta, y la ruta es razonable:

- **DEV**: `.agents/AGENTS.md` → `workflows/change-lifecycle.md` → `policies/*` según la tabla «When to read what»; autoridad e historia en `docs/` (RFC/ADR/Plan); evidencia factual en Git/`tests/`/`tools/`; historia en `docs/`. Regla de eficiencia declarada: «Fetching history is not required to operate: this repo's lifecycle is derived from artifacts, not from reading 100 plans» (`authority.md:58-63`).
- **Protocol**: `AGENTS.md` (entry) → `protocol/.agents/INDEX.md` (bootstrap) → la máquina de estados y el workflow de la fase → los contratos del artefacto → el KB (`entrypoint.md`, entradas de discovery) con frescura y provenance.

`GAP` — El problema no es la ruta, es que **la ruta no puede resolverse sin juicio en tres puntos**: (a) «¿cuál es el Plan activo?» — no hay índice de trabajo activo más allá de `ROADMAP.md` («Sin trabajo activo») y del status del plan; (b) «¿qué documentos de estado actual existen?» — la lista de `5.1` es abierta; (c) «¿este documento sigue siendo verdad?» — no hay campo ni consulta.

### 10.4 ¿Hace falta una representación explícita del estado actual?

`HYPOTHESIS` — *«Hace falta una representación explícita del estado actual del conocimiento.»* **Verdicto: hace falta una representación explícita de la VIGENCIA por artefacto, y NO hace falta un nuevo artefacto de estado actual.**

- La segunda mitad es firme por evidencia interna: un artefacto «estado actual del conocimiento» sería **una segunda fuente de verdad** sobre el mismo hecho, contra `.agents/AGENTS.md:8` («One source of truth per concept. No registry, global state, database or state machine lives in `.agents/`. Repository state = git + the governance artifacts + ephemeral session artifacts») y contra `ROADMAP.md:Qué no es una entrada de este roadmap` («nuevos registries», «nuevas entidades globales»). El review de capacidad ya rechazó por la misma razón `WorkUnit` y `Execution Graph`.
- La primera mitad se sostiene en que el vocabulario **ya está declarado y sin usar**: `docs/AGENTS.md:Lifecycle` define `active`/`archived`/`superseded`/`deprecated` con transiciones y coexistencia, y `docs/rfc/69:114-126` lo respalda. **No hay que inventar categorías: hay que escribir las que ya existen.** El modelo de banner de `docs/architecture/*.md` demuestra que la forma funciona; es artesanal, no general.
- `DESIGN_OPTION` — La forma mínima compatible con el modelo: **un campo de vigencia en el header del artefacto de gobernanza**, con el vocabulario existente y un puntero opcional al sustituto o al motivo; metadata **evolucionable** exactamente como el estado de un finding (`LC-1`: «metadata de lifecycle … puede evolucionar preservando el histórico de transiciones»), y **nunca** una reescritura del contenido (RFC-46). Eso convierte «vigente vs histórico» en una consulta de una línea sobre 247 artefactos, sin agregar entidad, registry ni estado global.

---

## 11. SAE Implications

### 11.1 La pregunta, partida en dos

`FACT` — La pregunta «qué parte de la autonomía falta porque el executor carece de capacidades y qué parte falta porque ARgentOS exige al humano especificar conocimiento derivable» tiene una respuesta con evidencia **para cada mitad**, y las dos son de naturaleza distinta.

**Mitad A — capacidades del ejecutor ausentes (ya identificadas por el review de capacidad):**

| Frontera | Qué falta | Evidencia | Impacto sobre la concisión del prompt |
|---|---|---|---|
| `PR-1` admisión de efectos | el host verifica **paths de escritura** contra el Scope, no **clases de efecto** contra autorización; `runtime/` no lee el bloque `## Effects` (verificado: `effects` aparece solo como campo de contrato y como auto-reporte del worker) | `AUTHORIZATION.md:44-111`; `contracts.py:303,428,453,487,541`; `agent_worker.py:473` | **ninguno directo** — es una frontera de seguridad para cuando existan efectos reales |
| `PR-2` presupuesto de recurso | `max_iterations = 8` + no-progress guard + `DEFAULT_MAX_STEPS = 24` son constantes, no un techo autorizado, acumulativo y persistente | `host.py:105,898-954`; `agent_worker.py:85-107` | **ninguno directo** — acota la ejecución desatendida, no la entrada |

**Mitad B — conocimiento que el humano debe especificar y el sistema podría derivar (hallazgo de esta investigación):**

| Elemento | Quién lo aporta hoy | ¿Derivable hoy? | Qué falta para derivarlo |
|---|---|---|---|
| **Tipo de trabajo** (investigación / diseño / decisión / especificación / implementación / verificación / documentación / release) | **el humano, por el enunciado** | **no** — 0 coincidencias de taxonomía en todo el repositorio | una declaración por Change + un mapeo kind → artefactos y gates obligatorios (patrón ya existente en `AGENT_STATE_MACHINE.md:Task Profiles`, que mide **peso**, no tipo) |
| **Plan** (objetivo, entregables, pasos, criterios de salida) | **el humano/agente lo redacta**; nada lo deriva | **no** | vía de autorización que acepte un objetivo acotado en lugar de un plan completo; **es la decisión de gobernanza más grande del conjunto** |
| **Task y Scope de la delegación** | redactados en `## Delegación agentiva` | **no** hoy; los `## Entregables` son la fuente natural | derivar `Scope` de los entregables + del contrato de placement, con la misma semántica de membresía exacta que ya existe |
| **Obligaciones aplicables** (anchor, checkpoint, gates, determinaciones de cierre, changelog, series) | el agente las lee de las policies | **parcial** — las reglas existen y están tabuladas por Change Level (`docs/plans/94-...:9.2`) | que **el ejecutor las consulte**: hoy ningún código lee `.agents/policies/` (§3.6 c) |
| **Conocimiento vigente** | el agente lo infiere leyendo prosa | **no** | vigencia declarada por artefacto (§10.4) |
| **Documentos de estado actual afectados** | juicio del Change, lista abierta | **no** por diseño | un alcance acotado y declarado del conjunto de estado actual |
| **Reglas del Protocol aplicables a un cambio de payload** | el agente busca entre 80 RFCs | **parcial** — `docs/rfc/INDEX.md` da la pregunta que cada RFC responde | mapeo RFC → rutas del payload que toca |
| **Criterios de aceptación** | **el humano** | **no, y no debe serlo** | nada: `NO_ASSUMPTIONS.md:16` lo prohíbe correctamente |

### 11.2 La frontera real: autorización, no longitud del prompt

`FACT` — El hallazgo decisivo para la pregunta central: **acortar el prompt no depende de la longitud del prompt.** Aunque el sistema derivara perfectamente el tipo de trabajo, las obligaciones, el alcance y el conocimiento vigente, seguiría sin poder ejecutar, porque `autonomy ⊆ authorized scope` y el scope proviene de un Plan aprobado por un humano (`change-lifecycle.md:2`; `supervised-autonomous-execution.md:§1-§2`). Las únicas vías sin Plan aprobado son **Clase C** (corrección mecánica, cero cambio de significado) y **L0** («1 agente, 1 sesión, 1 archivo, sin cambio estructural, sin versión, <1 sesión»; `docs/plans/94-...:9.2`: «sin Plan obligatorio»).

`INFERENCE` (declarada) — Por lo tanto, para que «Implementá X» ejecute trabajo no trivial, la única vía compatible con la gobernanza vigente es que **la autorización humana se exprese sobre una intención acotada** y que el sistema **construya** el Plan (artefacto de autorización + expediente) a partir de ella y de su propia derivación. Eso **no** requiere una entidad nueva: requiere (a) una forma de intención autorizable distinta de «Plan completo redactado a mano», y (b) que el sistema pueda derivar el contenido del Plan. Ambas son decisiones humanas, no deducciones (§15).

`FACT` — Y la consecuencia sobre la métrica de autonomía es la que el propio ARgentOS ya sabe leer: `human_operational_intervention` («un paso que el host no pudo conducir; el costo de una autonomía incompleta») debe bajar; `human_authority_decision` («una decisión que excede la autonomía otorgada; la frontera funcionando como se diseñó; **NO** es un fallo de autonomía») **no debe bajar**. Un modelo de intención concisa que reduzca el segundo sería una regresión de gobernanza, no una mejora.

### 11.3 Los nueve elementos evaluados, uno por uno

| Elemento | Estado hoy | Qué falta para la autonomía con intención concisa |
|---|---|---|
| **autoridad** | `IMPLEMENTED`: 3 veredictos, acciones `FORBIDDEN`, refusal antes del efecto, no retroactividad, no ampliación autónoma | que la autoridad se **lea** de sus fuentes: hoy el host solo lee el status del Plan, no RFC-56 ni las policies. La `Clase A/B/C` **no se evalúa** |
| **scope** | `IMPLEMENTED` y fuerte: membresía exacta, all-or-nothing sobre el conjunto completo de write-targets, detección post-delegación por content snapshots | que el scope pueda **derivarse** de los entregables en lugar de declararse a mano |
| **placement** | `IMPLEMENTED` como resolutor puro `PLACE|STOP` (11 motivos de STOP), **no integrado**, con tablas muertas, y sin equivalente en el payload | integrarlo como consulta (no como gate bloqueante) y declarar el STOP como escalación, no como resultado final |
| **work type** | **`GAP`** — no existe | declaración de tipo + mapeo a artefactos/gates |
| **applicable policies** | `DOCUMENTED_ONLY` en el ejecutor | que el host consulte las policies que hoy cita como strings |
| **knowledge lifecycle** | `IMPLEMENTED` en el Protocol (snapshot/claim/lesson, frescura, `invalidated_facts`); `PARTIALLY` en DEV (identidad de contenido); **vigencia documental: `GAP`** | representación de vigencia por artefacto |
| **impact / reconciliation** | `DOCUMENTED_ONLY` (determinaciones) + **Fase 2 de RFC-68 diferida** + el host no las consulta | detección como capacidad consultable; que el ejecutor consulte las determinaciones |
| **validation** | `IMPLEMENTED` y es lo más fuerte del sistema: anchor, Scoped Content Identity, checkpoint, gates C-1/C-2/C-3, `FAIL ≠ GAP ≠ ANOMALY` | dos atestaciones propias en la cadena (`Validity/stale` fijo y `Consistencia … PASS` escrito por el host y releído) que un tercero no debería consumir como evidencia |
| **human escalation** | `IMPLEMENTED` y correcta: `REQUIRES_HUMAN` con la autoridad nombrada, 21 acciones de stop, 13 de autoridad humana, salida `0` cuando el stop es el resultado correcto | que la escalación **no sea la única respuesta**: hoy escala tanto la incertidumbre legítima como la certeza derivable |

---

## 12. Architectural Gaps

`FACT` — Esta es la lista de carencias arquitectónicas que la evidencia sostiene. Cada una declara su etiqueta, su evidencia y por qué el modelo actual no alcanza. **Ninguna se propone como trabajo autorizado**: §15 y §17 las someten a decisión.

**G-1 — El intake no tiene vía desde una intención hasta trabajo autorizado.** `GAP`. Evidencia: `change-lifecycle.md:2` (sin Plan `Aprobado para ejecución` → STOP y proponer); `docs/plans/94-...:9.2` (solo L0/Clase C carecen de Plan); corpus con **0** planes en `Aprobado *` y 149 en `Executed`. Por qué no alcanza: cualquier cambio de peso L1+ exige que un humano redacte y apruebe un documento antes de que el sistema haga nada, de modo que el costo de entrada no depende de la dificultad técnica sino del peso del artefacto. Impacto sobre autonomía: alto y directo.

**G-2 — El ejecutor no deriva contexto ni obligaciones de las fuentes de autoridad.** `GAP`. Evidencia: ningún código de `runtime/` lee `.agents/policies/`, `docs/rfc/`, `docs/CONVENTIONS.md` ni `docs/VERSIONING.md`; `change_level` y `rfc` se parsean y no se usan; el prompt enviado al LLM no contiene ninguna regla (§3.6 a); la clase RFC-56 no se evalúa. Por qué no alcanza: el sistema tiene la regla escrita y no la aplica, de modo que «qué obliga» se resuelve por juicio del modelo en cada sesión, con deriva (16 cabeceras de RFC obsoletas, 20+ filas de INDEX stale, con la batería verde).

**G-3 — No existe un concepto de tipo de trabajo.** `GAP`. Evidencia: 0 coincidencias de `work_type`/`work-type`/`tipo de trabajo` en todo el repositorio; los dos ejes existentes miden peso (`Task Profiles` en el Protocol, `Change Level` en DEV); el único eje cualitativo (status del Plan `redacción`/`ejecución`) es binario y está inerte. Por qué no alcanza: el conjunto de artefactos y gates obligatorios no puede derivarse de qué se está haciendo, solo de cuánto pesa — y eso impide que un mismo objetivo se resuelva con obligaciones distintas según el trabajo.

**G-4 — La vigencia del conocimiento no es representable ni consultable.** `GAP`. Evidencia: 80/80 RFCs `Accepted`, 149/149 planes `Executed`, 18/18 ADRs `Accepted`, 0 `Superseded`/`Rejected`; el vocabulario `active/archived/superseded/deprecated` de `docs/AGENTS.md` no se escribe en ninguna cabecera; 16 cabeceras de RFC declaran «ejecución pendiente» con sus planes `Executed`; la lista de documentos de estado actual es abierta. Por qué no alcanza: ningún lector —humano o agente— puede responder «¿qué rige hoy?» sin leer prosa y juicio.

**G-5 — El trabajo retirado y el rechazado no son representables.** `GAP` + `CONTRADICTION`. Evidencia: `docs/VERSIONING.md:7` define `Abandoned = Plan Superseded con motivo`, y `Superseded` «exige indicar el plan reemplazante»; cuando no hay reemplazante no hay salida — registrado cuatro veces de forma independiente (planes 88, 137, 140, `MASTER:HD-1`). El plan 137 quedó **semanas** en `Aprobado para redacción` porque no existía la transición de retiro. Por qué no alcanza: un sistema que no puede nombrar el abandono no puede distinguirlo del trabajo pendiente, y el corpus tiene al menos tres casos reales (`INDEX.md:1836-1841` «Future Extensions … decidir destino»; Incremento 5 diferido sin owner; `PLAN_08_*` «Descartado» en el archivo).

**G-6 — Detección de obsolescencia ausente; determinación presente; reconciliación sin consulta del ejecutor.** `GAP` + `CONTRADICTION`. Evidencia: `validation-closure.md:5.1/5.2` declaran que no hay ni habrá checker semántico; `derivation.py:407-466` cierra sin consultar impacto mientras la policy lo hace condición de stop (`§3.6 c`); RFC-68 Fase 2 (propagación mecánica de impacto) diferida con gates incumplidos. Por qué no alcanza: el ciclo completo `Change → impacto → conocimiento afectado → reconciliación` existe en diseño y no en operación, y la única obsolescencia detectada mecánicamente es la **identidad de contenido de una validación**.

**G-7 — El INDEX cumple dos roles incompatibles y su espejo se verifica por forma.** `CONTRADICTION`. Evidencia: `validation-closure.md:5.1` lo lista como documentación de **estado actual**; RFC-46 y `docs/AGENTS.md` tratan los planes cerrados como **traza histórica que no se actualiza**; `check_plan_structure.py:153-159` verifica substring del filename; 20+ filas stale medidas por lectura cruzada con la batería verde; su propio header declara «Estado al 2026-09-21» con planes 147/148/149 ya registrados. Por qué no alcanza: el artefacto que todo el mundo cita como fuente de navegación puede contradecir a los artefactos que describe sin que nada lo detecte.

**G-8 — La excepción legítima no es descubrible.** `GAP` con decisión declarada. Evidencia: `PC-27` exige registrar la excepción «en el artefacto que ya posee la decisión — **not** in a central store»; `PC-31a/31b` declara las excepciones documentales y exige localizarlas e interpretarlas; `PC-31c` declara que la machine-locatability «is **not prohibited**; it is simply not decided in favour of here». Caso de primera mano: el review de capacidad registró su propia divergencia de placement **dentro del propio artefacto**, y hoy es indescubrible desde fuera (§5.3). Por qué no alcanza: la regla funciona, y su consecuencia —que cada excepción deba conocerse de antemano— no está resuelta por ningún mecanismo vigente.

**G-9 — Un Change cuya autorización es una instrucción directa no tiene hogar de gobernanza.** `GAP`. Evidencia: no existe plan 150; `docs/architecture-capability-review.md` está untracked, sin fila de INDEX, sin entrada de changelog, con `REQUIRES_HUMAN_DECISION` explícito sobre su registro; el mismo estado tiene `MASTER_PENDING_WORK_INVENTORY.md`, que además contiene **el inventario más completo de trabajo pendiente del repositorio**. La matriz de `docs/plans/94-...:9.2` sí prevé una **Nota** para L1, y no tiene contrato, plantilla ni forma de registro. Por qué no alcanza: los dos artefactos de análisis más útiles del repositorio —uno de ellos producido por una instrucción legítima del mantenedor— viven fuera de la gobernanza que los haría encontrables.

**G-10 — La cadena de evidencia contiene atestaciones propias presentadas como hechos.** `PARTIALLY_IMPLEMENTED` con `GAP` de calidad. Evidencia: `governance.py:159` escribe `Validity / stale: vigente` incondicionalmente; `governance.py:190` escribe `Consistencia checkpoint↔anchor: PASS` y `observation.py:585-587` la relee como evidencia para derivar `Closed` (`host.py:1016-1031`); `governance.py:136` fija `Observed dependencies`. Mitigación verificada: la igualdad de `state_identity` y la re-lectura de gates. Por qué no alcanza: el propio payload prohíbe que una claim se llame «verified» sin evidencia de clase distinta de la atestación (`harness/INDEX.md:151-160`), y el host DEV produce exactamente ese patrón en su registro más load-bearing.

**G-11 — La cobertura de detección mecánica tiene huecos exactos y medidos.** `GAP`. Evidencia: §3.6 f (matriz completa). Los huecos que importan: links markdown fuera del payload (93 rotos medidos en `docs/adr/` + `docs/rfc/`), `#fragment` descartados, celdas de INDEX no parseadas, supersesión y abandono no verificables, contradicción semántica imposible por diseño, identidad de contenido declarada nunca recalculada, `Clase:` nunca leída. Por qué no alcanza: los cuatro defectos más consecuentes que encontró la investigación externa **no eran detectables** por la herramienta, y la batería estaba verde.

**G-12 — Cinco (seis) vocabularios de lifecycle sin traducción.** `CONTRADICTION`. Evidencia: §8.1. Por qué no alcanza: un RFC es simultáneamente `Accepted` (modelo de gobernanza) y `superseded`-en-parte (modelo documental) y ninguno de los dos campos lo dice; la frontera DEV/Protocol prohíbe compartir el mecanismo, de modo que **cada capa debe resolver el mismo problema dos veces** — y el Protocol ya lo resolvió para su KB mientras DEV no lo resolvió para su documentación.

**G-13 — El propio modelo de gobernanza del Protocol está declarado y no operativo.** `FACT`/`GAP`. Evidencia: `CHANGE_GOVERNANCE.md:70-72` (`enforcement = "documented"`), `:206-241` (append, derivación de `current` y `governance_position` **diferidas**); `KNOWLEDGE_INDEX.md:4-6` («The automated indexer is not implemented yet»). Por qué importa: la asimetría DEV/Protocol no es «DEV atrasado, Protocol adelantado»; es que **ninguno de los dos puede hoy responder «qué conocimiento rige»**, y el Protocol lo tiene declarado como decisión diferida.

**G-14 — El payload no tiene equivalente del Placement Contract.** `GAP`. Evidencia: `PROTOCOL_BOUNDARIES.md:20-30` (Artifact Safety Rule: ubicación + convención de nombre dentro de `.project/<session-uuid>/<iteration>/`), `:87` («Those files MUST be written to their normal locations within the project structure» — **defiere, no decide**), `:85-105` (directorios de estado persistente), `:54` (namespacing por dominio), `:144-153` (inmutabilidad de `.agents/`). Por qué importa: la pregunta «¿dónde va este artefacto?» está resuelta de forma determinista solo del lado DEV; del lado adoptante es una convención, no una resolución.

---

## 13. Alternatives Considered

Cada alternativa se evalúa con la evidencia disponible y se **descarta o se conserva como opción**, sin adoptarla.

**A — Introducir una entidad `Feature`/`WorkUnit` y una taxonomía de tipos de trabajo con un artefacto por tipo.** `DESIGN_OPTION` → **descartada como entidad, conservada como declaración.** Evidencia: el review de capacidad ya concluyó que `WorkUnit` sería «una **segunda representación** de una relación que ya es explícita y persistida, y contradiría la regla de una sola fuente de verdad por concepto»; y los nueve tipos propuestos **ya tienen vehículo** (Working/Research, RFC, ADR, contratos, plan de ejecución, anchor, dogfood, docs-only, release). Además «Feature» colisiona con `features.toml` (flags de capacidad). Coste de la entidad: alta ceremonia sin garantía nueva.

**B — Dar a los artefactos de gobernanza un campo de vigencia con el vocabulario ya declarado.** `DESIGN_OPTION` → **conservada**, con decisión humana pendiente. Evidencia a favor: el vocabulario existe (`docs/AGENTS.md:Lifecycle`), el patrón de metadata evolucionable existe (`LC-1`), la forma funciona (banners de `docs/architecture/*`), no crea entidad ni registry, y es reversible. Coste: una clasificación inicial de 247 artefactos y una decisión sobre quién la emite. Riesgo: que se convierta en un campo que nadie actualiza — mitigable si el cierre lo exige solo para artefactos nuevos y la clasificación histórica se hace una vez.

**C — Construir ahora el motor general de impacto y reconciliación.** `DESIGN_OPTION` → **descartada por ahora.** Evidencia: RFC-68 Fase 2 fijó gates de entrada de evidencia (telemetría P0, índice de trazabilidad verde, correlación multi-proyecto) y **ninguno se cumple**; el diagnóstico del propio repositorio es que el problema dominante es de registro, no de detección (§9.3); añadirlo violaría el criterio de `ROADMAP.md` («no agregar features por disponibilidad tecnológica»).

**D — Archivar, mover o reclasificar el corpus histórico.** `DESIGN_OPTION` → **descartada.** Evidencia: RFC-46 (la traza no se reescribe), ADR-17 `RS-3`/`RS-4` (el repositorio no se reorganiza; la limpieza no es razón), `docs/placement-contract.md:10` («This contract never authorizes a move»), `PC-40` («Historical artifacts MUST NOT be relocated for tidiness»). Cualquier movimiento requeriría su propio Change autorizado y no resuelve el problema (el problema es de lectura, no de ubicación).

**E — Un artefacto único de «estado actual del conocimiento».** `DESIGN_OPTION` → **descartada.** Evidencia: sería una segunda fuente de verdad (`.agents/AGENTS.md:8`), y `ROADMAP.md` prohíbe nuevos registries y entidades globales. La alternativa B consigue el mismo efecto sin artefacto.

**F — Rebasar el criterio de confianza de intención sobre derivabilidad en lugar de sobre la forma del prompt.** `DESIGN_OPTION` → **conservada, con alcance acotado.** Evidencia: `INTENT_CONFIDENCE.md` mide cuatro propiedades del texto; `NO_ASSUMPTIONS.md:26` ya contiene el criterio correcto («exactly one reasonable interpretation given the context»); el vocabulario de tres valores ya existe en `AUTHORIZATION_UNDETERMINED`. Coste: una condición posterior a la fase de contexto y un registro. Riesgo declarado: no debe debilitar `NO_ASSUMPTIONS` — sigue siendo obligatorio preguntar cuando hay dos implementaciones razonables; lo que cambia es que la ambigüedad se evalúe **contra el repositorio**, no contra el prompt.

**G — No cambiar nada y confiar en la disciplina de prosa.** `DESIGN_OPTION` → **descartada, con evidencia de su coste.** Evidencia: 16 cabeceras de RFC que declaran ejecución pendiente con planes `Executed`; 20+ filas de INDEX stale; una afirmación falsa dentro de un RFC `Accepted` sobre el estado del propio repositorio (`CON-16`); 13 status contradictorios (`CON-19`); 93 links rotos; dos planes `Executed` afirmando lo contrario sobre el mismo hecho; y la batería verde en todos esos casos. La disciplina de prosa **no escala con el tamaño del corpus** (840k tokens).

**H — Extender el vocabulario de estados con `REJECTED`/`DUPLICATE`/`INVALIDATED` como estados de artefacto en DEV.** `DESIGN_OPTION` → **descartada.** Evidencia: tres de las siete categorías propuestas **ya existen** en algún dominio (`HISTORICAL` = RFC-46 + docs/AGENTS.md; `INVALIDATED` = Protocol `KNOWLEDGE_LIFECYCLE`; `REJECTED` = propiedad de ADR-03 y estado de decisión de RFC-68), y crear un sexto vocabulario empeora G-12. `DUPLICATE` se resuelve como **relación** (el corpus ya usó `superseded` + puntero al dueño vivo) y `ABANDONED` como **ampliación semántica de `superseded`** (sustituto **o** motivo).

**I — Hacer que el host DEV lea las policies y RFCs para derivar obligaciones.** `DESIGN_OPTION` → **conservada como la intervención de mayor relación efecto/coste, sujeta a decisión.** Evidencia: el host ya implementa el patrón correcto para placement (determinista, `PLACE|STOP`, nunca adivina) y ya tiene la tabla operacional de obligaciones por Change Level escrita; lo que falta es que la consulte. Riesgo: duplicar reglas en código — evitable si consulta el artefacto normativo en lugar de reimplementarlo (como `check_discovery_output.py` hace: **lee los requisitos de los contratos del payload** en lugar de copiarlos, `:212-313,859-965`). Ése es el precedente exacto de la forma correcta.

---

## 14. Proposed Target Model

`DESIGN_OPTION` — Modelo objetivo **propuesto como opción**, no adoptado. Se construye íntegramente con mecanismos que ARgentOS ya tiene, más una decisión de gobernanza (§15). **No introduce ninguna entidad, registry, state machine, autoridad ni namespace de IDs nuevo.**

### 14.1 Los cuatro componentes

```text
1. INTENCIÓN AUTORIZABLE          el humano expresa objetivo + autoridad, no procedimiento
        ↓
2. RESOLUCIÓN DE REGLAS APLICABLES  determinista: DERIVED | UNDETERMINED | NOT_DERIVABLE
        ↓
3. UNIDAD DE TRABAJO = CHANGE       (existe hoy, sin entidad) con tipo declarado + 1..N Planes
        ↓
4. VIGENCIA DEL CONOCIMIENTO        campo declarado por artefacto, vocabulario ya existente
```

**Componente 1 — Intención autorizable.** El humano sigue siendo la autoridad sobre objetivo, alcance y decisiones normativas (nada de esto cambia). Lo que cambia es **qué artefacto** expresa la autorización: hoy es un Plan completo redactado a mano; el modelo admite que la autorización se exprese sobre un objetivo acotado y que el Plan sea **derivado** y luego **autorizado**. Evidencia de que la forma existe: la matriz L0–L3 ya prevé «Plan/**Nota**» para L1; el corpus tiene 13 planes con `## Delegación agentiva` (el envolvente ya se declara, no se deriva); y la regla `PC-52` ya dice que «a request is not an authorization» — el modelo no la contradice, la respeta.

**Componente 2 — Resolución de reglas aplicables.** Un resolutor con la **misma forma** que el de placement: entradas declaradas, tabla de reglas derivada del artefacto normativo (no copiada), resultado determinista y **total**: `DERIVED` (una sola lectura sustentada por fuente autorizada), `UNDETERMINED` (dos o más lecturas razonables), `NOT_DERIVABLE` (requiere decisión humana). Precedente verificado de la forma correcta: `runtime/placement/resolver.py` (`PLACE|STOP`, 11 motivos, nunca adivina, no integrado) y `tools/check_discovery_output.py` (**lee los requisitos de los contratos del payload** en lugar de duplicarlos). Salidas mapeadas al vocabulario existente: `NOT_DERIVABLE` → `NEEDS_CLARIFICATION`/`REQUIRES_HUMAN`; `UNDETERMINED` → el mismo trato que `AUTHORIZATION_UNDETERMINED`, nunca resuelto por inferencia.

**Componente 3 — Unidad de trabajo.** El **Change** ya es la unidad real (`change-lifecycle.md:43-44` declara que no hay entidad `Change`, y el Plan es su registro). El modelo **no** crea la entidad: agrega al header del primer artefacto una **declaración de tipo de trabajo**, del mismo modo y en el mismo lugar donde RFC-75 Mecanismo 1 ya exige declarar origen/tipo, clase RFC-56 y Change Level. El **Plan** conserva su rol: autorización + contrato + expediente. La relación `Change 1..N Planes` ya existe vía serie (`Serie:`) y no necesita mecanismo nuevo.

**Componente 4 — Vigencia del conocimiento.** Un campo declarado por artefacto de gobernanza, con el vocabulario **ya existente** (`active`/`archived`/`superseded`/`deprecated`), puntero opcional al sustituto o motivo, tratado como **metadata evolucionable** (LC-1) y nunca como reescritura (RFC-46). Sin registry, sin índice nuevo, sin estado global.

### 14.2 Qué NO propone este modelo

- **Ninguna entidad nueva** (`Feature`, `WorkUnit`, `KnowledgeItem`, `Decision`): `AU-4`, `.agents/AGENTS.md:8`, `ROADMAP.md`.
- **Ningún registry, base de datos ni estado global**: ídem.
- **Ninguna state machine nueva**: ADR-15 y `docs/plans/94-...:10` ya rechazaron la máquina de estados del Change.
- **Ningún movimiento, archivado ni reescritura del corpus histórico**: RFC-46, ADR-17, `PC-40`.
- **Ninguna nueva clase de autoridad, gate o checker obligatorio**: cada adición mecánica propuesta es una **consulta**, no un gate bloqueante; y la batería no gana comandos sin decisión.
- **Ninguna ampliación autónoma de scope**: `§1.4` sigue vigente sin excepción.

### 14.3 Recomendaciones, con el análisis obligatorio

Cada recomendación declara los nueve campos exigidos. **Todas requieren decisión humana** salvo donde se indica; ninguna se convierte en regla por estar escrita aquí.

---

**R-1 — Declarar la vigencia de los artefactos de gobernanza con el vocabulario existente.**

- **Problema que resuelve:** el corpus no puede responder «¿qué rige hoy?»; 80/80 RFCs `Accepted` y 149/149 planes `Executed` no contienen información de vigencia (G-4).
- **Evidencia:** §7.1 (conteos), §8.1 (vocabulario declarado y sin usar), §7.5 (`docs/architecture/*` demuestra que la forma funciona), `docs/AGENTS.md:Lifecycle`, `docs/rfc/69:114-126`, `LC-1` (metadata evolucionable).
- **Por qué el modelo actual no alcanza:** la vigencia se expresa en prosa y la prosa contradice el estado en 20+ casos medidos; la lista de documentos de estado actual es abierta (`validation-closure.md:5.1`); el INDEX cumple dos roles incompatibles (G-7).
- **Alternativas consideradas:** B (esta), E (artefacto único de estado actual, descartada), C (derivar vigencia de las citas, descartada: confundiría «muy citado» con «vigente» — `docs/architecture/` tiene 65 citas), G (no cambiar nada, descartada).
- **Trade-offs:** agrega un campo que hay que mantener (riesgo de campo muerto); exige una clasificación inicial de 247 artefactos; si se emite por juicio, puede ser tan poco fiable como la prosa. Mitigación: exigirlo **solo** para artefactos nuevos y clasificar el histórico una vez, con decisión humana por lote.
- **Impacto sobre autonomía:** alto y habilitante — es la condición para que un agente pueda leer el estado vigente sin leer 840k tokens.
- **Impacto sobre gobernanza:** bajo — no crea autoridad, no cambia jerarquías, no agrega gates; reutiliza un vocabulario ya normativo.
- **Impacto sobre histórico/lineage:** nulo sobre el contenido (RFC-46 se respeta: se agrega metadata, no se reescribe); mejora la trazabilidad porque el puntero al sustituto hace explícita la cadena.
- **¿Requiere decisión humana?** **Sí** (adopción del campo, emisor, alcance, y si se incluye en el DoD).

---

**R-2 — Hacer que el ejecutor consulte las obligaciones y la autoridad desde sus fuentes normativas, sin duplicarlas.**

- **Problema que resuelve:** el host cierra un Change sin consultar las determinaciones de impacto que la policy declara condición de stop; no evalúa la clase RFC-56; no lee ninguna policy; y el prompt enviado al LLM no contiene ninguna regla (G-2, G-6).
- **Evidencia:** §3.6 a y c (`derivation.py:407-466` vs `validation-closure.md:345-346`; `agent_worker.py:320-325`); `observation.py:968-969` (`change_level`/`rfc` parseados y sin uso); precedente correcto de forma en `check_discovery_output.py:212-313`.
- **Por qué el modelo actual no alcanza:** la regla existe y el ejecutor no la aplica, de modo que la conformidad depende del juicio del modelo en cada sesión y deriva (evidencia de la deriva en §7.2, última fila y §3.6 k).
- **Alternativas consideradas:** I (esta), C (motor de impacto, descartada por gates incumplidos), G (disciplina de prosa, descartada por la deriva medida).
- **Trade-offs:** riesgo real de **duplicar la norma en código** — que es exactamente lo que `PC-75` prohíbe para placement («Enforcement MUST NOT become a second normative source»). Mitigación obligatoria: leer el artefacto normativo y no reimplementarlo; si el artefacto y el código discrepan, **el artefacto gobierna** y el defecto se escala.
- **Impacto sobre autonomía:** alto — sin esto, «qué obliga» no es derivable y toda obligación debe ser recordada por el humano o por el modelo.
- **Impacto sobre gobernanza:** medio — fortalece la conformidad; el riesgo de segunda fuente es el punto a vigilar, y `PC-75` da la regla.
- **Impacto sobre histórico/lineage:** nulo (no toca artefactos históricos); positivo si el cierre deja de poder declararse sin determinaciones.
- **¿Requiere decisión humana?** **Sí** (es un cambio de comportamiento del ejecutor y roza la frontera `PC-75`).

---

**R-3 — Declarar el tipo de trabajo en el primer artefacto del Change, y derivar de él el conjunto de obligaciones.**

- **Problema que resuelve:** no existe concepto de tipo de trabajo; los artefactos y gates obligatorios dependen solo del peso (G-3).
- **Evidencia:** §2.6 (0 coincidencias de taxonomía; `Task Profiles` mide peso; el status de Plan es binario e inerte); §6.3 (los nueve tipos ya tienen vehículo); RFC-75 Mecanismo 1 (el lugar de la declaración ya existe).
- **Por qué el modelo actual no alcanza:** un «análisis» y una «implementación» del mismo peso reciben el mismo tratamiento aunque uno no produzca código y el otro no produzca decisión; y el único eje cualitativo está en desuso.
- **Alternativas consideradas:** A (entidad + artefacto por tipo, descartada), H (vocabulario epistémico nuevo en DEV, descartada), R-3 como **declaración** (conservada).
- **Trade-offs:** una taxonomía es un vocabulario más que mantener, y el corpus muestra que los vocabularios declarados y no usados degeneran (G-4). Mitigación: declararla **solo** donde cambia algo (artefactos y gates obligatorios), no como etiqueta descriptiva; y no inventar tipos que ya tienen vehículo.
- **Impacto sobre autonomía:** alto — es la pieza que permite que «qué estamos haciendo» seleccione obligaciones en lugar de que las escriba el humano.
- **Impacto sobre gobernanza:** medio — puede simplificar el DoD (obligaciones por tipo) o complicarlo (más vocabulario). El riesgo depende enteramente de que el mapeo tipo→obligaciones sea corto.
- **Impacto sobre histórico/lineage:** nulo (aplica a artefactos nuevos; los históricos son legacy declarado, RFC-75 Mecanismo 15).
- **¿Requiere decisión humana?** **Sí** (adopción de la taxonomía y de su mapeo).

---

**R-4 — Resolver el vocabulario de intención con una condición de derivabilidad posterior al contexto.**

- **Problema que resuelve:** el estándar que decide «preguntar o avanzar» mide la forma del prompt, no la derivabilidad del faltante; un pedido brevísimo y completamente determinado se manda a `CONFIRMING_INTENT` (G-2, §4.2).
- **Evidencia:** `INTENT_CONFIDENCE.md:13-41` (cuatro criterios sobre el texto; `score<6` → confirmación); `NO_ASSUMPTIONS.md:25-31` (el criterio correcto ya existe: «exactly one reasonable interpretation given the context»); `AUTHORIZATION.md:AUTH-004` (el vocabulario de indeterminación existe y no se reporta como denegación); `DECISIONS.md:D3` (la frontera ya está modelada).
- **Por qué el modelo actual no alcanza:** el score se calcula **antes** de la fase de contexto y no tiene acceso al repositorio; por construcción no puede distinguir «no lo escribió el humano» de «no es determinable».
- **Alternativas consideradas:** F (esta), G (no cambiar nada, descartada: mantiene la dependencia del prompt mecanizada).
- **Trade-offs:** agrega una evaluación posterior al contexto y un registro de tres estados. Riesgo explícito: **no debe debilitar `NO_ASSUMPTIONS`**; la regla sigue siendo preguntar cuando hay dos implementaciones razonables, y `UNDETERMINED` no es un permiso para avanzar.
- **Impacto sobre autonomía:** alto y es el más directo sobre la pregunta central — es la pieza que hace que «Implementá X» sea una entrada legítima cuando X está determinado.
- **Impacto sobre gobernanza:** medio — si se implementa mal, erosiona la regla de no asumir; si se implementa bien, la refuerza porque exige **evidencia** de que la interpretación es única.
- **Impacto sobre histórico/lineage:** nulo.
- **¿Requiere decisión humana?** **Sí** (es un cambio de estándar del payload si toca `INTENT_CONFIDENCE`, y en DEV si toca el intake).

---

**R-5 — Dar al trabajo retirado y al rechazado una representación, dentro del ciclo existente.**

- **Problema que resuelve:** `Abandoned` está definido y es inalcanzable; no hay estado de retiro ni de rechazo; un plan puede quedar indefinidamente en `Aprobado para redacción` sin salida (G-5).
- **Evidencia:** `docs/VERSIONING.md:7` + `Superseded` «exige indicar el plan reemplazante»; cuatro registros independientes del problema (planes 88, 137, 140, `MASTER:HD-1`); tres casos reales de trabajo retirado (§7.2, G-5).
- **Por qué el modelo actual no alcanza:** un trabajo retirado en silencio es indistinguible de un trabajo pendiente para cualquier lector y para cualquier derivación; y el corpus deja de poder cerrarse.
- **Alternativas consideradas:** ampliar la semántica de `Superseded` a «sustituto **o** motivo»; agregar un estado nuevo; dejar todo como está. La tercera se descarta por el caso del plan 137 (semanas sin salida).
- **Trade-offs:** ampliar la semántica de un estado existente es menos invasivo que crear uno nuevo, pero cambia el significado de un estado normativo y exige una decisión explícita. Crear un estado nuevo contradice `docs/CONVENTIONS.md:81` («No invent states»).
- **Impacto sobre autonomía:** medio — permite que el sistema distinga «no hacer» de «hacer», que es la condición para no proponer trabajo muerto.
- **Impacto sobre gobernanza:** medio — toca el ciclo de status de planes, que es normativo; requiere RFC o plan según la clase.
- **Impacto sobre histórico/lineage:** positivo — el retiro queda trazable en lugar de silencioso.
- **¿Requiere decisión humana?** **Sí**, y es una de las dos decisiones de vocabulario del conjunto (la otra es R-1).

---

**R-6 — Registrar en gobernanza los Changes cuya autorización es una instrucción directa del mantenedor.**

- **Problema que resuelve:** un Change legítimo autorizado por instrucción directa puede producir un artefacto sin plan, sin fila de INDEX y sin changelog; el caso del review y el inventario externo lo demuestran (G-9).
- **Evidencia:** §5.3 (reconstrucción completa del caso); la matriz `docs/plans/94-...:9.2` que prevé una **Nota** para L1 sin contrato ni plantilla; `PC-52` («a request is not an authorization. If the requester holds the domain's authority, the correct action is to record the exception and then place»); `MASTER_PENDING_WORK_INVENTORY.md` como inventario más completo del repositorio y sin trackear.
- **Por qué el modelo actual no alcanza:** la vía existe con nombre y sin forma; el resultado es que los dos artefactos de análisis más útiles del repositorio quedan fuera de la gobernanza que los haría encontrables — y el inventario de pendientes del repositorio vive **fuera** del repositorio.
- **Alternativas consideradas:** usar la Nota ya prevista y darle forma mínima; exigir un Plan aun para L0/L1 (descartado: es la ceremonia que `docs/rfc/56-governance-fast-track.md:47-49` ya identificó como el motivo por el que la gente la salta informalmente); no hacer nada (descartado: el estado actual ya produjo dos artefactos huérfanos).
- **Trade-offs:** dar forma a la Nota agrega un artefacto al ciclo; no dársela deja el problema. El coste real es bajo (una plantilla y una fila de INDEX) comparado con el coste de no tener registro.
- **Impacto sobre autonomía:** bajo directo, medio indirecto — sin registro, el sistema no puede saber que ese trabajo existió y volverá a proponerlo.
- **Impacto sobre gobernanza:** medio — normaliza una vía que hoy se usa informalmente; reduce la necesidad de excepciones de placement.
- **Impacto sobre histórico/lineage:** positivo — convierte trabajo huérfano en traza.
- **¿Requiere decisión humana?** **Sí** (es gobernanza: forma del artefacto, registro y quién autoriza).

---

## 15. Human Decisions Required

`HUMAN_DECISION_REQUIRED` — Ninguna de estas decisiones se resuelve por inferencia en este documento. Para cada una se declara qué evidencia existe, qué falta y qué bloquea.

| ID | Decisión | Evidencia disponible | Qué falta | Bloquea |
|---|---|---|---|---|
| **HD-OPS-A** | ¿Se adopta un campo de **vigencia** en los artefactos de gobernanza, con el vocabulario `active/archived/superseded/deprecated` de `docs/AGENTS.md`? ¿Quién lo emite y cuándo? ¿Se clasifica el corpus histórico (247 artefactos) o solo los nuevos? | §10.4; `docs/AGENTS.md:Lifecycle`; `docs/rfc/69:114-126`; precedente de banner en `docs/architecture/*`; `LC-1` (metadata evolucionable) | la decisión de adopción, alcance y emisor. La forma es la de menor coste y mayor efecto del conjunto | R-1; y sin ella, toda derivación de «qué rige» sigue siendo lectura de prosa |
| **HD-OPS-B** | ¿`Superseded` amplía su semántica a «sustituto **o** motivo», o se crea una salida de retiro, o se decide explícitamente que el trabajo retirado **no** se representa? | §7.3 y G-5: cuatro registros independientes del problema; el plan 137 quedó semanas sin salida; `docs/CONVENTIONS.md:81` prohíbe inventar estados | la decisión. Las tres opciones son defendibles y **mutuamente excluyentes** | R-5; y mientras no se decida, el abandono sigue siendo invisible |
| **HD-OPS-C** | ¿Se admite una **vía de autorización** para un Change cuya autorización es una instrucción directa del mantenedor y cuyo producto es un artefacto de análisis (la «Nota» que `docs/plans/94-...:9.2` ya prevé para L1)? | §5.3 (el caso del review); G-9; `PC-52`; `docs/rfc/56:47-49` (por qué se salta la ceremonia) | la decisión de forma y registro. **No** falta evidencia de la necesidad: hay dos artefactos huérfanos | R-6; y el registro en gobernanza del Change que produjo el review |
| **HD-OPS-D** | ¿El sistema debe **derivar** el contenido del Plan a partir de una intención acotada autorizada, o la autorización humana seguirá expresándose sobre un Plan redactado? | §11.2 (`autonomy ⊆ authorized scope` y el scope viene del Plan); corpus con 0 planes en `Aprobado *`; `docs/plans/94-...:9.2` (L0 sin Plan obligatorio) | la decisión de gobernanza más grande del conjunto. **Esta investigación no puede tomarla**: cambia qué artefacto expresa la autorización | la posibilidad real de que «Implementá X» ejecute trabajo no trivial |
| **HD-OPS-E** | ¿Se rebasa el criterio de confianza de intención sobre la **derivabilidad** (posterior al contexto) en lugar de sobre la forma del prompt? | R-4; `INTENT_CONFIDENCE.md`; `NO_ASSUMPTIONS.md:25-31`; `AUTH-004`; `DECISIONS.md:D3` | la decisión, y el cuidado de no debilitar `NO_ASSUMPTIONS` | R-4 y, con ella, la hipótesis §4.5 |
| **HD-OPS-F** | ¿Se adopta la **declaración de tipo de trabajo** y cuál es el mapeo tipo → artefactos y gates? | R-3; §2.6; §6.3 (los nueve tipos ya tienen vehículo) | la decisión de adoptarla y, si se adopta, el mapeo (que debe ser corto para no repetir G-4) | R-3 |
| **HD-OPS-G** | ¿Se hace que el **ejecutor** consulte las obligaciones y la autoridad desde las fuentes normativas, y cómo se protege `PC-75` (que el enforcement no se vuelva una segunda fuente normativa)? | R-2; §3.6 c; `derivation.py:407-466` vs `validation-closure.md:345-346`; precedente de forma en `check_discovery_output.py` | la decisión, y la regla de precedencia si el código y el artefacto discrepan (existe: `PC-75`, «el contrato gobierna») | R-2; y la consistencia entre la policy de cierre y el cierre real |
| **HD-OPS-H** | ¿Cómo se **registra en gobernanza** el Change del review y esta investigación? ¿Plan propio? ¿insumo de la Etapa A? ¿fila del INDEX? | `docs/architecture-capability-review.md:1978-1982` (el propio review declara esta decisión pendiente); §5.3; G-9 | la decisión. **No** es deducible: crear, registrar o autorizar es autoridad del mantenedor | el destino de los dos artefactos untracked |
| **HD-OPS-I** | ¿Se abre la **Fase 2 de RFC-68** (propagación mecánica de impacto) o se mantienen sus gates de entrada? | §9.1/§9.3: los gates declarados (telemetría P0, índice de trazabilidad verde, correlación ≥2 conjuntos) **no se cumplen** | la decisión de secuencia: la propia RFC la difirió con criterio | R-2/R-6 en cuanto a detección; no bloquea HD-OPS-A/HD-OPS-C |
| **HD-OPS-J** | ¿Se decide algo sobre la **machine-locatability de las excepciones de placement** (`PC-31c`: «not prohibited, simply not decided in favour of here»)? | G-8; `PC-27`/`PC-30`/`PC-31a-c`; el caso del review como evidencia de primera mano de una excepción indescubrible | la decisión. Reabrirla es legítimo (`PC-31c` lo permite) y **no** es necesario para R-1 | R-1 en su variante de excepciones; no bloquea nada más |
| **HD-OPS-K** | ¿Se **corrigen** las afirmaciones falsas dentro de artefactos `Accepted` y las 16 cabeceras con «ejecución pendiente», o se dejan como traza histórica? | §7.2 (última fila), §3.6 k, `CON-16`…`CON-19`; RFC-46 prohíbe reescribir historia; `docs/VERSIONING.md:225` prohíbe retroceder estados | la decisión de política: ¿corrección post-close por referencia, o decisión explícita de no corregir? | la fiabilidad del corpus como fuente de lectura; el maestro de obra de R-1 |
| **HD-OPS-L** | ¿Se corrige `docs/placement-contract.md` para que su texto de non-goals coincida con el estado real de `runtime/placement/`? | `CON-13`/`DF-21`: el contrato afirma «not implemented» y «no checker, resolver, service … exists» mientras el resolutor y tres suites existen; `PC-72.1` lo reconcilia solo en la sección de enforcement | la decisión de autorizar un Change de reconciliación documental | la coherencia del contrato de placement; es un caso **menor** pero verificado |
| **HD-OPS-M** | ¿Se reconcilian las **13 contradicciones internas del payload** (§3.6 l), en particular la transición `DISCOVERY_STACK → DISCOVERY_FRAMEWORK` vs `→ DISCOVERY_MERGE` y el `enforcement = documented` del artefacto de gobernanza del Protocol? | §3.6 l con las 13 verificadas; dos de ellas afectan la legalidad de un camino de la máquina de estados | la decisión de si se corrige (payload ⇒ RFC-56) o se tolera | la corrección del payload; no bloquea las decisiones DEV |

`FACT` — Dos observaciones sobre este conjunto: (1) **solo HD-OPS-A, HD-OPS-C y HD-OPS-D habilitan el resto** — son las decisiones que convierten «derivar» en algo posible; (2) **ninguna requiere un mecanismo nuevo** para tomarse: son decisiones de vocabulario, de forma de artefacto y de alcance, todas expresables con la gobernanza vigente (RFC `Accepted` o plan `Aprobado para ejecución`, según la clase RFC-56).

---

## 16. Open Questions

`FACT` — Preguntas abiertas que la evidencia **no** permite cerrar. No son tareas: son incógnitas declaradas.

- **OQ-1 — ¿Cuál es el umbral real de utilidad de la vigencia declarada?** No hay evidencia de cuántos de los 247 artefactos cambiarían de lectura con un campo de vigencia. `INFERENCE`: los 16 RFC con «ejecución pendiente», las 20+ filas stale y los 3 casos de abandono se beneficiarían; el resto es desconocido.
- **OQ-2 — ¿La concisión del prompt mejora la calidad de la decisión o la degrada?** `NO_ASSUMPTIONS.md` existe porque la experiencia previa mostró que el agente adivinaba. No hay evidencia en el repositorio de un caso donde un prompt más corto **habría** producido una decisión peor o mejor; sin esa evidencia, cualquier ampliación del conjunto «prompt brevísimo suficiente» es una apuesta.
- **OQ-3 — ¿Cuánto de la dependencia del prompt es inevitable por el tipo de trabajo?** Un trabajo de investigación o de diseño exige que el humano declare el objetivo y el problema, y eso no es derivable de nada. La frontera exacta entre «objetivo, que sólo el humano tiene» y «contexto, que el sistema puede derivar» no está trazada en ninguna fuente, y esta investigación no la trazó.
- **OQ-4 — ¿El corpus histórico debe clasificarse por vigencia o basta con clasificar lo nuevo?** Ambas opciones son coherentes con RFC-46; no hay evidencia de coste real de la clasificación histórica.
- **OQ-5 — ¿Un tipo de trabajo declarado por el humano o derivado del contenido?** R-3 propone declararlo. No hay evidencia de que el sistema pueda derivarlo con fiabilidad, ni de que el humano lo declare con regularidad (el `Change Level` obligatorio se declara en 55 de 156 archivos).
- **OQ-6 — ¿Cuál es el efecto de la frontera DEV/Protocol sobre la duplicación de soluciones?** La frontera es deliberada (`docs/CONVENTIONS.md`), y la consecuencia es que G-2/G-3/G-4 deben resolverse dos veces. No hay evidencia de si conviene resolverlos primero en DEV, primero en Protocol, o de forma independiente.
- **OQ-7 — ¿La `Nota` prevista por `docs/plans/94-...:9.2` es la forma correcta, o el problema real es que la matriz de Change Levels no distingue «documento de análisis» de «corrección mecánica»?** El caso del review cayó entre C y L1 sin Plan; no hay evidencia de cuántos casos más existen.
- **OQ-8 — ¿Las atestaciones propias del host (G-10) son un defecto o un límite aceptado?** La policy de SAE declara honestamente que el enforcement es prevención donde el host controla el efecto y detección donde no puede interponerse (`§12`). No hay evidencia de si el mismo criterio de honestidad se aplicó, o debería aplicarse, a las **atestaciones del propio registro de cierre**.
- **OQ-9 — ¿Cuál es la magnitud real del costo de la gobernanza?** `docs/AUDITORIA_DOCUMENTACION.md:Feedback crítico` lo afirma («cada cambio chico paga un peaje burocrático alto») y los planes 140/141/143/144/145 son cinco cierres consecutivos de residuos de gobernanza. No hay medición: la dimensión de costo de las métricas está declarada `Unavailable` (`METRICS.md`).
- **OQ-10 — ¿Qué pasa con el inventario externo?** `MASTER_PENDING_WORK_INVENTORY.md` es el inventario más completo del trabajo pendiente del repositorio, no está trackeado, y su propio §5 deja 22 ítems diferidos y 12 decisiones humanas. Su destino (registrar, incorporar por referencia, mantener externo) no está decidido por ninguna fuente.

---

## 17. Recommended Next Work

`HUMAN_DECISION_REQUIRED` — Nada de lo que sigue está autorizado por este documento. Se presenta como **trabajo posterior propuesto**, ordenado por dependencia, con su clase RFC-56 estimada y la decisión que lo habilita. **No es una lista de tareas ejecutables: es la secuencia que la evidencia sugiere.**

```text
PASO 0 — Decidir  (HD-OPS-H)
  Registrar en gobernanza el Change del review y esta investigación.
  Sin esto, dos artefactos de análisis del repositorio siguen fuera de su gobernanza.
  Bloquea: el registro de todo lo demás como insumo.

PASO 1 — Decidir el vocabulario y la forma  (HD-OPS-A, HD-OPS-B)
  Vigencia por artefacto  ·  representación del retiro/abandono.
  Son decisiones de vocabulario; no requieren mecanismo nuevo.
  Habilitan R-1 y R-5.

PASO 2 — Decidir la vía de autorización  (HD-OPS-C, HD-OPS-D)
  La Nota para L1 (existe con nombre y sin forma)  ·  si el Plan se deriva de una
  intención autorizada o se sigue redactando.
  Es la decisión de mayor alcance: define si «Implementá X» puede ejecutar.

PASO 3 — Materializar lo barato y reversible
  R-1 (campo de vigencia)  ·  R-5 (retiro)  ·  R-6 (Nota registrada).
  Clase: docs/gobernanza DEV; sin payload; sin entidad nueva.

PASO 4 — Decidir y ejecutar la derivación en el ejecutor  (HD-OPS-G, HD-OPS-E)
  R-2 (el host consulta las fuentes normativas, sin duplicarlas)
  R-4 (confianza por derivabilidad, posterior al contexto).
  Clase: DEV (runtime + intake); R-4 toca el payload si cambia INTENT_CONFIDENCE.

PASO 5 — Decidir el tipo de trabajo  (HD-OPS-F)
  R-3, con un mapeo corto tipo → artefactos y gates.

PASO 6 — Recién entonces, evaluar detección de impacto  (HD-OPS-I)
  Fase 2 de RFC-68 con sus gates declarados, o una versión acotada a la
  documentación de gobernanza.  Hoy los gates no se cumplen.
```

`FACT` — Dos trabajos **independientes** del camino anterior, que la evidencia sostiene por sí sola y que no requieren ninguna de las decisiones de vocabulario:

- **Reconciliación de las contradicciones verificadas.** Las 13 del payload (§3.6 l), la discrepancia `docs/placement-contract.md` vs `runtime/placement/` (`HD-OPS-L`) y las afirmaciones falsas dentro de artefactos `Accepted` (`HD-OPS-K`). Son correcciones documentales o de payload con evidencia completa; cada una requiere su propia autorización, y su valor es que hoy **la lectura del repositorio puede engañar a un agente**.
- **Cierre de los huecos de detección de bajo coste.** `PC-75` no prohíbe mejorar la cobertura: links markdown fuera del payload, `#fragment`, celdas de INDEX. Son mejoras de tooling DEV, con precedente (`check_plan_structure`, `check_plan_citations`) y con evidencia de 93 links rotos medidos. **Advertencia explícita:** agregar un checker crea una obligación de gobernanza sobre todo Change futuro (`<PLAN-137>:PC-3` lo razonó así y no lo autorizó); la decisión es del mantenedor y **no** se toma aquí.

`FACT` — Y una recomendación de **no hacer**, que la evidencia sostiene: **no construir todavía un motor general de impacto/reconciliación** (alternativa C) ni **introducir ninguna entidad nueva** (alternativa A). Los dos movimientos agregarían mecanismo sin reducir la clase de problema dominante, que es la ausencia de representación de vigencia y la desconexión entre la regla escrita y el ejecutor.

---

## 18. Evidence Index

### 18.1 Cómo se produjo la evidencia

`FACT` — Cinco auditorías de solo lectura, independientes, además de la lectura directa del autor de este documento. Ninguna modificó archivo alguno; los comandos ejecutados fueron de lectura (`Get-ChildItem`, `Get-Content`, `Select-String`, `Measure-Object`, `git status`, `git log`, `git ls-files`) o la ejecución read-only de los checkers. **`pytest` no se ejecutó** en ninguna de las auditorías (crea cachés) y `check_ears_coverage.py` no se ejecutó en una de ellas (escribe un espécimen temporal fuera del repositorio).

| # | Auditoría | Alcance | Volumen leído |
|---|---|---|---|
| A1 | `runtime/` — implementación vs documentación | los 12 módulos de `runtime/orchestrator/`, los 3 de `runtime/placement/`, los 13 de `runtime/toolcalls/`, `runtime/README.md`, 17 suites de `tests/` | 12.000+ líneas de código; reporte de 12 secciones con `file:line` |
| A2 | `tools/` — enforcement mecánico | los 20 scripts de `tools/` en su totalidad, `docs/VERSIONING.md`, `docs/CONVENTIONS.md`, las dos plantillas, CI, 41 módulos de `tests/`; **ejecución read-only de los 6 checkers de la batería + C-1/C-2/C-3 + 4 herramientas** | 19.958 líneas de tests; matriz de detección de 23 señales |
| A3 | `docs/plans/` — caracterización del corpus | `INDEX.md` (1.864 líneas), `_TEMPLATE.md` (197), `docs/CONVENTIONS.md` (682), y 24 planes leídos directa o delegadamente incluyendo 01–10, 18, 19, 41, 57, 58, 69, 74, 76, 78, 83, 85, 86, 88, 91, 92, 94–97, 99, 100, 144, 146–149 | 43.160 líneas / 3.374.034 caracteres del directorio completo; tabla de 80+ filas y clasificación por clase |
| A4 | `docs/rfc/` + `docs/adr/` — caracterización del corpus | los 82 archivos de `docs/rfc/`, los 20 de `docs/adr/`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`; census de referencias RFC por capa | 17.428 + 1.707 líneas; tabla por RFC y tabla por ADR |
| A5 | `protocol/` — contratos, estándares, harness, orquestadores, skills | 226 archivos de texto del payload (25.431 líneas); `AUTHORIZATION.md`, `PROTOCOL_BOUNDARIES.md`, `CONTEXT.md`, `KNOWLEDGE_LIFECYCLE.md`, `KNOWLEDGE_CURATION.md`, `NO_ASSUMPTIONS.md`, `INTENT_CONFIDENCE.md`, `DECISIONS.md`, `ANTI_CIRCUMVENTION.md`, `AGENT_STATE_MACHINE.md`, los 11 contratos de core, los 12 policies H00–H15, `harness/{gate_validator,hook_gate,runner_state,health_check}.py` (2.259 líneas), los 9 contratos de architecture, discovery y system, y las 9 skills relevantes | 25.431 líneas; 13 gaps y 14 contradicciones del payload |

### 18.2 Evidencia del repositorio citada en este documento (por capa)

**Gobernanza DEV (normativa)**
`AGENTS.md` (191) · `docs/AGENTS.md` (189) · `docs/CONVENTIONS.md` (682) · `docs/VERSIONING.md` (432) · `docs/placement-contract.md` (468) · `docs/source-layout.md` (52) · `docs/AUDITORIA_DOCUMENTACION.md` (143) · `ROADMAP.md` (342) · `MASTER_PENDING_WORK_INVENTORY.md` (342, **untracked**) · `docs/architecture-capability-review.md` (1.986, **untracked**).

**Capa operacional DEV**
`.agents/AGENTS.md` (95) · `.agents/policies/authority.md` (75) · `.agents/policies/validation-closure.md` (362) · `.agents/policies/lifecycle-checkers.md` (119) · `.agents/policies/autonomous-orchestration.md` (252) · `.agents/policies/supervised-autonomous-execution.md` (514) · `.agents/workflows/change-lifecycle.md` (288).

**RFC / ADR**
`docs/rfc/INDEX.md` (91) · `docs/rfc/_TEMPLATE.md` (69) · RFC-46 (44) · RFC-56 (70) · RFC-63 (258) · RFC-67 (182) · RFC-68 (1.339) · RFC-69 (420) · RFC-75 (680) · `docs/adr/INDEX.md` (56) · ADR-03 (72) · ADR-10 (71) · ADR-15 (145) · ADR-16 (135) · ADR-17 (192) · ADR-18 (125).

**Planes**
`docs/plans/INDEX.md` (1.864) · `_TEMPLATE.md` (197) · 41 (54) · 88 (689) · 94 (1.092) · 96 (1.427) · 97 (1.115) · 99 (1.350) · 100 (1.277) · 136 (533) · 137 (453) · 144 (399) · 146 (360) · 148 (347) · **149 (189, leído completo)**.

**Tooling y tests**
`tools/` (20 scripts) · `.github/workflows/check-protocol.yml` (46) · `tests/AGENTS.md` (94) · 41 módulos de `tests/` (19.958 líneas, 1.059 `def test_`).

**Runtime**
`runtime/README.md` (448) · `runtime/orchestrator/{host 1153, autonomy 1523, contracts 612, derivation 543, observation 1001, governance 414, agent_worker 696, worker 625, store 304, authority 226, __main__ 227, __init__ 80}` · `runtime/placement/{resolver 468, rules 304, __init__ 39}` · `runtime/toolcalls/{canonical 415, identity 359, segment_resolution 296, project_store 269, project_segment 224, cache_coordinator 154, provider_cache 155, change_governance 167, toolcalls_rendering 145, context 124, prompt_rendering 95, budget 42, __init__ 7}`.

**Payload del Protocol**
`protocol/_AGENTS.md` · `protocol/.agents/VERSION` (`11.6.2`) · `INDEX.md` · `features.toml` · `contracts/{CHANGE_GOVERNANCE, KNOWLEDGE_INDEX, METRICS, HARNESS_REPORT, SESSION_BRIEF, SESSION_LOG, DELIBERATION_REPORT, REVIEW_REPORT, PROJECT_README}` · `delegation/WORKER_DELEGATION_CONTRACT.md` · `standards/{requirements/NO_ASSUMPTIONS, requirements/INTENT_CONFIDENCE, requirements/EARS, conduct/ANTI_CIRCUMVENTION, conduct/OPERATIONAL_RULES, quality/{EVIDENCE,CONFIDENCE,RUBRICS,PREFLIGHT_CHECKLIST}, context/{CONTEXT, KNOWLEDGE_LIFECYCLE, KNOWLEDGE_CURATION, RESOLUTION_*, BUDGET_MATERIALIZATION, COMPOSITION_*}, orchestration/{DECISIONS,ORCHESTRATION_GUIDE,SKILLS}, runtime/{AUTHORIZATION,PROTOCOL_BOUNDARIES,PROTOCOL_METRICS,PROTOCOL_TAXONOMY,PROTOCOL_HEALTH}}` · `orchestrators/core/{roles/orchestrator.md, states/AGENT_STATE_MACHINE.md, workflow/00–08 + INDEX, contracts/*10, harness/policies/H00–H15}` · `orchestrators/{architecture,discovery,system}/**` · `harness/{INDEX.md, gate_validator.py, hook_gate.py, runner_state.py, health_check.py, policies/H13}` · `skills/` (9 leídas + `INDEX.md`).

**Working (provenance)**
`docs/working/proposals/WORKFLOW_PROPOSAL.md` (1.499) · `docs/working/proposals/INDEX.md` · `docs/working/research/INDEX.md` · `docs/working/audits/INDEX.md` · `docs/architecture/{ARCHITECTURAL_PROBLEM_MODEL.md 885, ARCHITECTURAL_DECISION_MODEL.md 1129}` · `docs/glossary/INDEX.md` (136).

### 18.3 Inferencias registradas en este documento

`INFERENCE` — Registradas explícitamente para que no se lean como hechos:

| ID | Inferencia | Base |
|---|---|---|
| I-1 | Para que «Implementá X» ejecute trabajo no trivial, la autorización humana debe expresarse sobre una intención acotada y el sistema debe construir el Plan | Derivado de `autonomy ⊆ authorized scope` + el intake exige Plan; **no** verificado por implementación (no existe) |
| I-2 | El cuello de botella de la intención concisa es de derivación y de autorización, no de ejecutor | Derivado de la evidencia de A1/A2 (todo lo derivable del host ya funciona) + el corpus de 0 planes en estados no terminales |
| I-3 | La vía «Nota» de `docs/plans/94-...:9.2` es el eslabón con nombre y sin forma | La matriz la nombra; no tiene contrato, plantilla ni registro; **es lectura**, no declaración del repositorio |
| I-4 | Los dos artefactos untracked son el síntoma de G-9, no dos incidentes independientes | Ambos son análisis de un solo archivo, autorizados por instrucción directa, y ninguno tiene Plan ni fila de INDEX |
| I-5 | La clasificación por clase de los 149 planes (A3 §2d) es del auditor, no del repositorio | Derivada de headers + `Objetivo` + `Nota de ejecución`; los rangos no leídos directamente están marcados como inferidos por el propio auditor |
| I-6 | El patrón «regla escrita sin realización en el ejecutor» es el riesgo dominante de ARgentOS | Lectura de casos verificados (`PR-1`, `Documentation/Roadmap impact`, `Clase:` RFC-56, `PC-72.1`, `UPDATE_DOCUMENTATION_AUTHORIZED`); es una lectura de cinco casos, no una propiedad demostrada |

### 18.4 Límites de evidencia

`FACT` — Limitaciones declaradas, para que ninguna conclusión se lea con más fuerza de la que tiene:

1. **No se ejecutó `pytest`** en esta investigación ni en las auditorías; los conteos de tests citados (1.010 / 1.186 / 1.059 `def test_`) provienen de documentos del repositorio y de un `--collect-only` read-only, no de una corrida completa propia.
2. **Los checkers se ejecutaron read-only** en A2 y su estado registrado (todo verde, con un `GAP` advisory en el plan 116); el resto de las cifras de estado provienen de documentos que los registran (plan 149, `MASTER_PENDING_WORK_INVENTORY.md`).
3. **Conteos con dos metodologías.** `Measure-Object -Line` cuenta solo líneas no vacías y subreporta frente al conteo por saltos de línea; donde los dos difieren se usó el segundo (p. ej. `INDEX.md` 1.864 vs 1.609). Las cifras de §7.1 se verificaron con la misma expresión regular en dos lecturas independientes y coinciden en los valores de estado.
4. **No se auditó exhaustivamente ningún subsistema.** A1 no leyó los tests completos; A2 no ejecutó `pytest` ni `check_ears_coverage.py`; A3 no leyó directamente 60+ planes (usa header + INDEX, marcado como parcialmente inferido); A5 no leyó en profundidad `CAVEMAN.md`, `standards/development/design/*`, `standards/runtime/{EXTERNAL,PYTHON}_DEPENDENCIES.md` ni `standards/testing/TDD.md`.
5. **No se ejecutó ningún repositorio externo y no se incorporó evidencia externa** (§3.2). Toda comparación externa citada pertenece a `docs/architecture-capability-review.md`, que declara sus propias limitaciones en su §12.4.
6. **Dos incógnitas declaradas por las auditorías y no resueltas aquí:** la identidad exacta del único archivo con `Status: Proposal` en `docs/rfc/` (dos filtros distintos discrepan; el template es el candidato obvio y el recuento de RFC numerados es 80/80 `Accepted`), y el contenido de `docs/placement-contract.md` en una de las auditorías (se resolvió en la lectura directa del autor de este documento, que sí lo leyó completo).

### 18.5 Verificación de read-only

`FACT` — Comprobación final sobre el árbol de trabajo:

| Verificación | Resultado |
|---|---|
| `git status --short --branch` | `## dev...origin/dev [ahead 1]`; `?? MASTER_PENDING_WORK_INVENTORY.md`, `?? docs/architecture-capability-review.md` (**ambos preexistentes y ajenos**) y `?? docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md` (**el entregable de esta investigación**) |
| `git diff --name-only HEAD` | vacío — 0 modificaciones rastreadas |
| Modificaciones a código, políticas, contratos, Placement Contract, RFCs, ADRs, planes, `ROADMAP.md`, `CHANGELOG.md`, `VERSION`, INDEX, tests, CI, `dist` o payload | **ninguna** |
| Archivado, movimiento, renombrado o reorganización | **ninguno** |
| Commits, tags, releases, push | **ninguno** |
| Findings cerrados, pending decisions resueltas, hipótesis convertidas en decisiones | **ninguno** |

`HUMAN_DECISION_REQUIRED` — **Registro de este documento.** El contrato de placement resuelve su ubicación sin conflicto (clase `Working / Research` → familia `Working analysis` → `docs/working/research/`, `docs/placement-contract.md:6. Namespace selection`), a diferencia del review, cuya ruta fue fijada por instrucción explícita. Lo que **no** está resuelto y no se resuelve por inferencia: (a) si este documento debe registrarse en `docs/working/research/INDEX.md` — hacerlo sería una modificación de un artefacto existente, fuera de la autorización read-only de esta investigación; (b) si el Change que lo produjo debe registrarse como Plan o como Nota (HD-OPS-H/HD-OPS-C); (c) si su contenido habilita la Etapa A del roadmap o si debe volver al mantenedor como insumo. Las tres son autoridad del mantenedor.

---

**Fin del documento.** Esta investigación no cierra ninguna de las decisiones que declara: las deja explícitas, con su evidencia, para que la autoridad humana pueda pasar de `estado actual → problemas demostrados → hipótesis evaluadas → modelo propuesto → decisiones pendientes → trabajo posterior` sin reconstruir el análisis.

