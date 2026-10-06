# Investigación focalizada — Modificación humana de un Plan/Note derivado y su autorización

**Clase documental:** Working / Research (provenance) — **no normativo**
(`docs/AGENTS.md:Folder → class map`; `docs/placement-contract.md:6. Namespace selection`,
familia `Working analysis` → `docs/working/{audits,research,proposals}/`).
**Naturaleza:** investigación y diseño `READ_ONLY` respecto del sistema. **Autoridad de este
documento: ninguna.** Registra evidencia, clasificación, evaluación de hipótesis y una
recomendación; no crea mecanismos, no modifica arquitectura, no autoriza trabajo y **no resuelve
ninguna decisión humana**.
**Fecha:** 2026-09-23
**Baseline (`dev` @ `820da21`):** `820da210cd4b6d4e5a5cb6a6639fd9a8a6fc7506` —
`docs(roadmap): declare the capability and autonomy roadmap A-B-C (plan 149)`;
`protocol/.agents/VERSION` = `11.6.2`.
**Predecesor inmediato:** `docs/working/research/INVESTIGACION_MODELO_INTENCION_DERIVACION_GOBERNANZA_Y_CONOCIMIENTO_2026-09-23.md`
(de aquí en adelante «la investigación previa»), que dejó abiertas `HD-INT-A`…`HD-INT-J` y del que esta
investigación **depende sin reabrirlo**.
**Alcance de escritura:** este trabajo escribió **un documento nuevo** (este archivo) y **una fila
de registro** en `docs/working/research/INDEX.md` (registro/navegación de su propia familia).
No modificó código, runtime, Protocol, policies, RFCs, ADRs, planes históricos, `ROADMAP.md`,
`CHANGELOG.md`, `VERSION`, Placement Contract, `dist`, INDEX de gobernanza, tests ni CI; no
archivó, movió ni reorganizó nada; no creó commits, tags, releases ni push; no creó Plan, RFC,
ADR, registry, entidad, state machine, clase de autoridad, primitive de identidad ni fuente
normativa.

---

## Leyenda de clasificación (obligatoria)

| Etiqueta | Significado |
|---|---|
| `FACT` | Hecho verificado por lectura directa o conteo mecánico reproducible; no expresa intención ni norma. |
| `IMPLEMENTED` | El mecanismo existe y **lo realiza un ejecutor** verificado en el artefacto que lo ejecuta. |
| `PARTIALLY_IMPLEMENTED` | Existe una parte mecánica y otra que depende de prosa o disciplina humana. |
| `DOCUMENTED_ONLY` | Existe como texto normativo o instrucción; **ningún ejecutor lo verifica**. |
| `GAP` | Ausencia de mecanismo, representación o información. |
| `CONTRADICTION` | Dos fuentes —o una fuente y el estado real— afirman cosas incompatibles. |
| `HYPOTHESIS` | Afirmación evaluada aquí, con el veredicto que la evidencia permite. |
| `DESIGN_OPTION` | Alternativa evaluada; **no** es recomendación aceptada ni regla. |

Regla de honestidad aplicada: una hipótesis no se convierte en decisión, y una recomendación no se
convierte en regla. Donde la evidencia no alcanza, se declara `GAP` o `PC-1` (`resolución: pendiente`).
Las citas usan `ruta:sección`; no se usan números de línea sobre archivos mutables.

---

## 1. Identity

| Dimensión | Valor |
|---|---|
| **Clasificación** | Working / Research (provenance). No normativo. Dominio DEV. |
| **Fecha** | 2026-09-23 |
| **Baseline** | `dev` @ `820da210cd4b6d4e5a5cb6a6639fd9a8a6fc7506`; `protocol/.agents/VERSION` `11.6.2` |
| **Scope de la investigación** | la frontera «modificación humana pre-autorización de un Plan/Note derivado → autorización». Nada más. |
| **Autoridad** | ninguna. El documento **no** autoriza, **no** decide y **no** crea norma. |
| **Archivos modificados** | `docs/working/research/INVESTIGACION_MODIFICACION_HUMANA_DERIVACION_2026-09-23.md` (creado) y `docs/working/research/INDEX.md` (una fila de registro). |
| **Restricciones respetadas** | sin implementación, sin Plan, sin RFC/ADR, sin cambio de policies, `CONVENTIONS.md`, runtime, tests, Protocol, índices de gobernanza ni CHANGELOG; sin clasificación retroactiva del corpus; sin commit/push/tag/merge/release. |
| **Limitaciones** | (a) el modelo de derivación al que se refiere HD-K **aún no existe como ejecutor**: es `DESIGN_OPTION` de la investigación previa, sujeta a `HD-INT-A`/`HD-INT-H`; por eso varias conclusiones son de diseño y no de comportamiento verificado. (b) Medición mecánica de este trabajo: `work_type`/`work-type` tiene **4 ocurrencias en todo el repositorio, las cuatro dentro de los documentos de investigación Working** (`docs/working/research/…2026-09-22.md`, `…2026-09-23.md` y `docs/working/research/INDEX.md`); **0 ocurrencias** en `docs/plans/`, `docs/rfc/`, `docs/adr/`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `.agents/`, `runtime/`, `tools/`, `tests/` y `protocol/.agents/`. La afirmación «0 ocurrencias» de la investigación previa §1.3 se confirma para el corpus de gobernanza y el código, y ya no para el repositorio entero. (c) Los tres artefactos preexistentes untracked (`MASTER_PENDING_WORK_INVENTORY.md`, `docs/architecture-capability-review.md`, la investigación previa) se citan como evidencia externa, no como gobernanza. (d) No se ejecutó ningún dogfood: todos los casos de §4 son lectura del corpus y del código. |

`FACT` — Estado Git al escribir: rama `dev`, HEAD `820da21`, tres rutas untracked preexistentes
más los dos archivos de este trabajo; sin commit.

---

## 2. Pregunta HD-K

**Formulación exacta (la del encargo):**

> **HD-K — ¿Qué efecto tiene una modificación humana sobre un Plan/Note derivado?**

Contexto ya decidido (premisas, no se debaten aquí):

```text
Intent → Context → Derivation → Plan/Note (proposed) → Human Authorization → SAE
```

Decisiones adoptadas que esta investigación **consume**: `HD-INT-A` (adoptar el modelo), `HD-INT-B`
(`Superseded` con motivo), `HD-INT-C` (lifecycle nuevo explícito), `HD-INT-D` (`Note` = Working artifact),
`HD-INT-E` (una intención puede autorizarse mediante `Note`), `HD-INT-F` (`work_type` derivado), `HD-INT-G`
(huérfanos no se regularizan retroactivamente), `HD-INT-H` (`CONVENTIONS.md` fuente normativa
inicial), `HD-INT-I` (lifecycle en INDEX como vista derivada), `HD-INT-E2` (Plan vs Note por criterios),
`HD-INT-J` (Plan/Note es siempre el artefacto gobernable; `proposed` = su situación previa a
autorización).

**Pregunta operativa que hay que poder responder con fundamento:**

> Cuando un humano modifica un Plan/Note `proposed`, ¿cuándo estamos ante una simple edición,
> cuándo ante una decisión humana explícita y cuándo la modificación invalida la derivación previa
> y exige una nueva derivación?

**Reformulación que la evidencia de §3–§5 hace necesaria** (declarada aquí porque cambia el objeto
de la pregunta, no su intención):

> HD-K no pregunta qué le ocurre a un artefacto marcado «derivado». No existe tal marca.
> Pregunta **qué le ocurre a una derivación `D` cuando cambia una de las premisas con las que `D`
> fue producida, antes de que su resultado sea autorizado.**

`FACT` — Justificación de la reformulación, en §3.6 y §9.2.

---

## 3. Modelo actual (qué hace ARgentOS hoy)

Esta sección describe **sólo** lo que HD-K necesita. No es un inventario del repositorio.

### 3.1 El gate de autorización ya existe y es exactamente binario

`IMPLEMENTED` — `runtime/orchestrator/derivation.py:derive_next_action (regla 1)`:

```text
if not observation.plan_present                  → STOP_PLAN_NOT_FOUND
if not status or status.startswith("Aprobado para redacción")
                                                 → STOP_AWAIT_PLAN_AUTHORIZATION
if status.startswith("Superseded")               → STOP_PLAN_SUPERSEDED
```

`FACT` — `runtime/orchestrator/observation.py:ChangeObservation.authorized_for_execution` acepta
`"Aprobado para ejecución"` y `"Executed"`. El ciclo de status aplicable es
`docs/CONVENTIONS.md:Convenciones` (ciclo de status de planes): `Aprobado para redacción` →
`Aprobado para ejecución` → `Executed` → `Superseded`, con `Executed (parcial: …)`.

`FACT` — El estado **`proposed` de `HD-INT-J` no es un valor de `**Status:**`**: su materialización
existente es `Aprobado para redacción`, que es el estado inicial que el propio template declara
(`docs/plans/_TEMPLATE.md:header`). `HD-INT-J` no introdujo un estado; usó el que ya existía
(investigación previa §12.4).

### 3.2 Autoridad: una sola clase decide, y el host no la crea

`DOCUMENTED_ONLY` — `.agents/policies/authority.md:Authority classes`: `FACTUAL`, `NORMATIVE`,
`DECISION`, `RELEASE`, `DESCRIPTIVE`. Sin jerarquía total. La clase `DECISION` es del mantenedor y
**nunca** se delega a inferencia. `.agents/policies/authority.md:Stop conditions (authority)`
ordena `STOP` cuando la autoridad normativa no existe o cuando se requiere una decisión humana.

`IMPLEMENTED` — `runtime/orchestrator/authority.py:AuthorityBoundary.evaluate` responde con
exactamente tres veredictos: `AUTHORIZED_EXISTING` / `REQUIRES_HUMAN` / `FORBIDDEN`, con `basis`
que **cita** la autoridad existente. `FORBIDDEN_ACTIONS` incluye `APPROVE_PLAN`, `CHANGE_SCOPE`,
`MODIFY_CLOSED_ARTIFACT`, `RELEASE`, `TAG`, `PROMOTE`.

`FACT` — Consecuencia directa para HD-K: **`CHANGE_SCOPE` y `APPROVE_PLAN` están en
`FORBIDDEN_ACTIONS`**. Ningún agente puede aprobar un plan ni cambiar su scope, sea antes o
después de la autorización. Lo único que un agente puede hacer es **proponer**.

### 3.3 La frontera SAE: el único mecanismo que hoy distingue «modificación legítima» de «modificación que detiene»

`IMPLEMENTED` — `.agents/policies/supervised-autonomous-execution.md:1.2 The authorization
checkpoint` y `runtime/orchestrator/autonomy.py:authorization_projection` /
`authorization_contract_projection` / `authorization_scope_projection` / `authorization_drift`:

```text
la proyección de autorización = Task + familia de status autorizante + presencia de la declaración
la proyección de scope        = conjunto de paths autorizados
authorization changed after the action was authorized  ⇒  STOP   (STOP_SCOPE_VIOLATION)
```

`IMPLEMENTED` — `runtime/orchestrator/host.py:_apply_autonomy_gate` fija (*pin*) la proyección en
la **primera iteración autorizada** y la compara en toda iteración posterior; `_pinned_autonomy_projection`
devuelve la **más temprana** registrada en el journal, para que un reinicio no pueda re-fijar una
declaración reescrita mientras el host estaba detenido.

`FACT` — **Este mecanismo tiene una frontera temporal explícita y verificada**: sólo observa
modificaciones **posteriores a la primera autorización de una acción**. Antes de ese momento no hay
*pin*, y `runtime/orchestrator/autonomy.py:authorization_drift` declara que `pinned is None`
significa «not pinned yet» y se reporta como ausencia de divergencia
(`tests/test_sae_scope_enforcement.py:test_a_not_yet_pinned_checkpoint_is_not_a_divergence`).

`FACT` — Por tanto: **HD-K vive exactamente en la ventana que el checkpoint de autorización no
cubre.** El mecanismo existente no es insuficiente; es *otro* momento. Ver §8.

### 3.4 El mecanismo ya distingue representación de significado — pero sólo dentro de su ventana

`IMPLEMENTED` + `FACT` — `runtime/orchestrator/autonomy.py:_canonical_text` normaliza *runs* de
espacios a un espacio: «Re-wrapping a field or re-indenting it is the *same* declaration, so it must
not read as a change of authorization. Every other change of the words does.»
`tests/test_sae_scope_enforcement.py:test_rewrapping_a_field_is_not_a_change_of_authorization`
verifica exactamente eso.

`FACT` — Es el **precedente más fuerte del repositorio** para la frontera que HD-K necesita
(editorial vs semántico, §5.1), con dos matices que hay que declarar:

1. el precedente es **textual, no semántico**: normaliza forma, no significado. Una aclaración que
   cambia el significado de una frase **sí** es divergencia para este mecanismo;
2. el precedente opera **después** de la autorización, con la consecuencia opuesta a la de HD-K:
   allí una divergencia **detiene**; aquí, antes de autorizar, una modificación humana es el acto
   que **forma** la autorización.

### 3.5 Qué datos son derivados, declarados, confirmados o invariantes

`DOCUMENTED_ONLY` — La investigación previa §12.1–§12.2 fija el contrato de clasificación del Plan
derivado, con cuatro categorías y una lista cerrada de «forbidden to infer»:

| Categoría | Definición (investigación previa §12.2) |
|---|---|
| **Derivado** | el sistema puede producirlo con fuente citable y determinación única |
| **Declarado** | debe venir explícitamente de la intención/autorización humana; el agente **nunca** lo completa por defecto |
| **Confirmado** | ARgentOS lo propone y el humano confirma; el default es propuesta, nunca aceptación tácita |
| **Forbidden to infer** | nunca puede inferirse; su ausencia **detiene** (lista `FI-1`…`FI-10`) |

`FACT` — Reparto de campos por categoría, según esa misma fuente (investigación previa §12.1), que
HD-K necesita entero:

| Campo del Plan | Categoría |
|---|---|
| `**Change Level:**` | Derivado |
| `**Clase:**` (A/B) | Derivado + Confirmado |
| `**RFC:**` | Derivado + Confirmado |
| `**Origen:**` | **Declarado** |
| `**Fecha:**`, `**Depende de:**` | Derivado |
| `## Objetivo` | Confirmado |
| `## Criterio de entrada` | Derivado |
| `## Entregables` | Derivado |
| `## Pasos` | Derivado |
| `## Delegación agentiva → Task` | **Declarado** |
| `## Delegación agentiva → Scope` | **Declarado** |
| `## Criterios de salida` | Derivado + Confirmado |
| `## Verificación` | Derivado (+ confirmación si hay juicio) |
| `## Riesgos` | Confirmado |
| `## Trazabilidad` | Derivado |
| `**Status:**` inicial | Derivado = `Aprobado para redacción` |
| `work_type` | Derivado |
| lifecycle de las fuentes citadas | Derivado |
| veredicto de derivabilidad y su evidencia | Derivado |

`FACT` — **`Task` y `Scope` son `Declarado`, es decir `FI-2`/`FI-3`**: el humano los declara, el
agente no los infiere. La investigación previa los clasifica así porque
`.agents/policies/supervised-autonomous-execution.md:1.4` prohíbe cualquier ampliación autónoma y
`FI-2` prohíbe suponer el scope «y menos por proximidad de path». Ver §8.2.

`FACT` — Vocabulario de «Confirmado» **ya existente en el Protocol** (no inventado):
`protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Recording user decisions` distingue
`user_confirmed: true` de `false`, y `:Unattended mode` declara que un default aplicado se marca
`PENDING_USER_CONFIRMATION` y que «unreviewed default is never treated as user-confirmed».
`protocol/.agents/standards/runtime/AUTHORIZATION.md:AUTH-002`: `user_confirmed=false` **nunca**
constituye autorización.

`FACT` — Las **premisas** de una derivación son, según la investigación previa §12.1, exactamente
seis entradas más el scope declarado: intención `E-0`, confianza `E-1`, contexto `E-2`, veredicto de
derivabilidad `E-3`, `work_type`, conocimiento vigente, reglas aplicables, y autoridad/scope
humanos. Es la lista sobre la que §13 opera.

### 3.6 Qué ocurre **hoy** si esos datos cambian

`FACT` — Tres cosas distintas, según el momento, y ninguna de ellas es «invalidar una derivación»:

| Momento | Qué ocurre hoy | Evidencia |
|---|---|---|
| Antes de la primera autorización de una acción | **Nada.** El artefacto es texto no autorizado; el gate simplemente lee el estado actual y se detiene en `STOP_AWAIT_PLAN_AUTHORIZATION` mientras el status no autorice | `runtime/orchestrator/derivation.py:derive_next_action (regla 1)`; `authorization_drift(None, …)` |
| Después de la primera autorización, durante la ejecución | `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`, sin efecto persistente, con el checkpoint original preservado | `runtime/orchestrator/host.py:_apply_autonomy_gate`; `tests/test_sae_scope_enforcement.py:test_the_host_stops_when_the_contract_is_rewritten_after_authorization` |
| Después de una corrección real del contenido | El anchor queda `stale` y la derivación exige **revalidación A2** sobre el nuevo estado; A1 **nunca** se muta | `runtime/orchestrator/derivation.py (reglas 9)`; `.agents/workflows/change-lifecycle.md:7. Findings, corrections and revalidation` |

`FACT` — **Lo que no ocurre hoy, en ninguna capa**: nada registra que un Plan fue **derivado**, ni
de qué premisas, ni si su contenido cambió respecto de la derivación. El artefacto es la única
representación, y su procedencia no se declara en ningún campo. Los conteos que lo sostienen,
medidos en este trabajo: **0 marcas de procedencia por derivación** (`derivado por`,
`generado por derivación`, `Plan derivado`) en los **153** archivos de `docs/plans/` y en
`docs/rfc/`/`docs/adr/`; **0 ocurrencias** de `work_type` fuera de los documentos de investigación
Working; campo de vigencia en el header de un artefacto de gobernanza: **0**
(investigación previa §1.3).

`FACT` — Existe, eso sí, un precedente **manual** de la disciplina que falta: la columna
`Verificación de la premisa` de `docs/plans/141-human-decision-backlog-resolution.md` (§`HD`) hace
exactamente lo que §13 propone, pero a mano, sobre premisas de encargo y no de derivación del
artefacto.

---

## 4. Evidencia: casos concretos encontrados

Cada caso declara qué demuestra y qué **no** demuestra.

### 4.1 E-1 — Plan 136: autorización por directiva con el artefacto sin actualizar

`FACT` — `docs/plans/136-d01-mechanical-checker.md` nació `**Status:** Aprobado para redacción`;
su `## Criterio de entrada` exigía `Aprobado para ejecución`. El mantenedor autorizó la ejecución
**por directiva**, sin que el artefacto se actualizara. Registro: `<PLAN-136>:F-5` (`resolved`) y
`<PLAN-136>:PC-1`: «el Plan estaba `Aprobado para redacción` y la autorización de ejecución es una
decisión humana explícita que el agente no puede tomar … la decisión humana existió y quedó
registrada».

**Qué demuestra:** (a) la autorización es un **acto humano separado** del texto del artefacto;
(b) el repositorio ya resolvió este caso **sin inventar un estado intermedio** — llevó el status a
`Executed` al cerrar y registró la decisión como pending decision resuelta y como finding;
(c) una discrepancia entre el artefacto y la decisión humana se **registra**, no se infiere.

**Qué no demuestra:** no hubo modificación del *contenido* del Plan, sólo del *status* leído por el
criterio de entrada. HD-K pregunta por el contenido.

### 4.2 E-2 — Plan 137: propuesto, con `Roadmap Impact: REQUIRED` inejecutable, clasificado y no forzado

`FACT` — `docs/plans/137-ears-structural-validator.md` quedó `Aprobado para redacción`; su
`## Criterio de entrada` exigía `Aprobado para ejecución`; la guarda que declaraba tiene valor
propio (`R3`/`R5` sin cobertura por otro test). `docs/plans/140-governance-residual-closure.md`
(§tabla de resoluciones) concluye: «el plan 137 no fue autorizado para ejecución
(`Aprobado para redacción`) y `Superseded` exige un plan reemplazante que no existe — queda
clasificado, **no forzado**». Finalmente el Plan 141 autorizó su ejecución
(`docs/plans/145-integral-dev-backlog-closure.md:I-3`, que además corrigió la fila stale del INDEX).

**Qué demuestra:** (a) un artefacto `proposed` puede **permanecer sin autorizar** indefinidamente y
eso es un resultado legítimo, no un defecto; (b) el sistema **no** completa por default lo que falta
para poder avanzar; (c) la autorización posterior es un acto humano registrado.

### 4.3 E-3 — Plan 138 y el incidente de scope (F-3): el caso «modificación durante la ejecución»

`FACT` — `docs/plans/136-d01-mechanical-checker.md` (`<PLAN-136>:F-3`) declaró un `Scope` que
**excluía** `ROADMAP.md` y, a la vez, `Roadmap Impact: REQUIRED` nombraba ese artefacto como lo que
debía reconciliarse. La ejecución escribió fuera del scope. `docs/plans/138-sae-scope-authority-hardening.md`
(§Causa arquitectónica §4) identifica la causa real: **posibilidad de autorización retrospectiva** —
«El artifact del Plan es a la vez el contrato de autorización y el registro mutable de la ejecución.
Un agente que puede reescribir `## Scope`, `Task` y la tabla de artefactos afectados puede hacer que
una escritura fuera de Scope parezca autorizada desde el inicio».

`IMPLEMENTED` — La corrección (plan 138, E1–E3) fue: precondición all-or-nothing sobre el conjunto
completo de write targets, **checkpoint de autorización no retroactivo**, y evidencia en el registro
de iteración. `docs/plans/138-sae-scope-authority-hardening.md:PC-2` quedó `deferred`:
`.agents/policies/supervised-autonomous-execution.md:1.4` declara que **no existe ni se introduce**
mecanismo autónomo de Scope Expansion, y que la vía legítima es «una decisión humana de alcance —
aprobar o actualizar el plan, o emitir una nueva autorización — seguida de la reautorización del
trabajo que habilita».

**Qué demuestra:** (a) el repositorio ya tiene resuelto, con mecanismo y con norma, el caso
**posterior** a la autorización; (b) la vía legítima de ampliación **no necesita mecanismo nuevo**;
(c) la respuesta correcta a una modificación semánticamente relevante **no** es «re-derivar sin más»:
depende del momento.

**Qué no demuestra:** nada sobre la ventana pre-autorización. El incidente es, literalmente, el caso
opuesto: la escritura ya había ocurrido bajo una autorización vigente.

### 4.4 E-4 — `_canonical_text`: el repositorio ya distingue forma de significado

`IMPLEMENTED` — `runtime/orchestrator/autonomy.py:_canonical_text` (docstring citado en §3.4) más
`tests/test_sae_scope_enforcement.py:test_rewrapping_a_field_is_not_a_change_of_authorization`.

**Qué demuestra:** la distinción «editorial vs semántico» **no es una taxonomía nueva que HD-K deba
introducir**: ya existe, ya tiene implementación, y su criterio es declarado — la *representación*
no cuenta, las *palabras* sí.

**Qué no demuestra:** que ese criterio alcance para HD-K. Es textual y opera post-autorización; una
aclaración textual que cambia significado no la detecta (declarado por el propio docstring).

### 4.5 E-5 — El Protocol ya tiene el vocabulario de «decisión humana registrada»

`FACT` — `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Recording user decisions`:
`assumption: <text>` con `user_confirmed: true`; `:Unattended mode`: `PENDING_USER_CONFIRMATION`,
`source: unattended_default`, «unreviewed default is never treated as user-confirmed».
`protocol/.agents/standards/runtime/AUTHORIZATION.md:AUTHORIZATION_UNDETERMINED` («no sufficient
record to decide») y `AUTH-004` («`AUTHORIZATION_UNDETERMINED` is never reported as
`UNAUTHORIZED`»).

**Qué demuestra:** el repositorio ya sabe representar «el humano confirmó X», «el sistema propuso X
y nadie confirmó» y «no hay registro suficiente para decidir», sin inventar categorías. La
categoría **Confirmado** de §3.5 es reutilización, no invención.

### 4.6 E-6 — `AU-5`: un Plan no puede modificar en silencio la decisión que implementa

`DOCUMENTED_ONLY` — `.agents/policies/authority.md:Authority classes`, regla: «A Plan implements a
normative decision; it may not silently modify the decision it implements (AU-5)».

**Qué demuestra:** la asimetría que HD-K necesita ya está enunciada en la capa de autoridad: el
objeto que **implementa** no puede alterar en silencio lo que lo **autoriza**. Una modificación
humana de un Plan derivado es, por definición, **no silenciosa** (es un acto del humano), y ése es
el criterio por el que puede convivir con `AU-5` sin excepción.

### 4.7 E-7 — No hay caso de un Plan marcado como derivado

`FACT` — Búsqueda sobre el corpus DEV de marcas de procedencia por derivación (`derivado por`,
`generado por derivación`, `Plan derivado`, `derivó`) en `docs/plans/`, `docs/rfc/`, `docs/adr/`:
**0 artefactos de gobernanza** la declaran. Las coincidencias son (a) la investigación previa, que
propone el modelo; (b) `docs/plans/138-…` y los dogfoods, donde «derivó» describe lo que hace el
host en ejecución; (c) `docs/rfc/73-…`, donde «derivó» describe `generated_at` de discovery.

`FACT` — `tests/test_plan_structure.py:test_real_repo_has_no_violations` mantiene el corpus
estructuralmente verde, y ningún checker exige ni lee una marca de derivación.

**Qué demuestra:** HD-K es **vocacionalmente prospectiva**. La única forma de una modificación
humana que el repositorio ha ejercido es la de un Plan **redactado por humano** (o por agente
actuando como redactor), no la de un Plan derivado por un derivador que aún no existe.

`FACT` — Consecuencia, y es la más importante de §4: **el problema de HD-K no es un problema de
marca en el artefacto; es un problema de procedencia de las premisas.** Un artefacto «derivado» y
uno «redactado» se comportan igual frente a una modificación humana; lo que difiere es si existe
una derivación cuya validez pueda quedar comprometida. Ver §9.2.

### 4.8 E-8 — Corrección medida: la contención **no** alcanza a `docs/working/`

`FACT` — Medición de este trabajo, reproducible con `tools/check_plan_citations.py:scan_documents`:
la función construye su universo de fuentes con `docs/plans`, `docs/rfc`, `docs/adr` y los
`ROOT_DOCS`; **no** recorre `docs/working/`. Verificación directa: de las 220 fuentes escaneadas,
**ninguna** es de `docs/working/`.

`CONTRADICTION` — Esto **corrige una afirmación de la investigación previa** (`HD-INT-G`): allí se dice
que `tests/test_repo_containment.py` «exige que ningún target de cita versionada exista sólo como
archivo untracked», y que «al citarlos desde este documento y desde la investigación anterior, la
contención ya aplica si se versionan las citas». Medido: los documentos Working **no son fuentes**
del checker de contención, de modo que citar `docs/architecture-capability-review.md`,
`MASTER_PENDING_WORK_INVENTORY.md` o cualquiera de las investigaciones **desde otro Working
document** no activa la invariante RFC-69 I2.

`FACT` — Verificación cruzada: `python -m pytest tests/test_repo_containment.py
tests/test_check_plan_citations.py -q` → **53 passed** sobre el estado actual, con las cuatro rutas
untracked presentes.

`FACT` — Lo que esto **no** cambia y lo que sí:

| Afirmación | Estado tras la medición |
|---|---|
| Citar un Working untracked desde un Working no rompe la contención | `FACT` (medido) |
| Citar un Working untracked desde `docs/plans/`, `docs/rfc/`, `docs/adr/` **sí** rompería la contención | `FACT` (esos directorios **son** fuentes del checker) |
| `HD-INT-G` sigue siendo una decisión humana pendiente | `FACT` — pero por una razón más débil que la que `HD-INT-G` declara: el problema de los artefactos huérfanos es de **localizabilidad y gobernanza**, no de contención mecánica |
| `HD-INT-J` (el commit del propio documento) sigue siendo acto del mantenedor | `FACT`, sin cambio |

`FACT` — Pertinencia para HD-K, y por eso se registra aquí: el registro de procedencia de una
derivación (`premises(D)`) sería **precisamente** el tipo de dato que la contención no puede
proteger, porque viviría en un artefacto de gobernanza (`docs/plans/`) que **sí** es fuente del
checker y que cita fuentes Working. Cuando `HD-K3` se decida, la relación entre ese registro y
`tests/test_repo_containment.py` es una consecuencia directa, no un detalle.

`FACT` — Esta corrección **no se materializa**: no se modifica la investigación previa (es un
Working no normativo y su `HD-INT-G` es una decisión humana abierta), no se modifica el checker, y no
se abre una investigación paralela. Se registra como hallazgo de esta investigación, con su
evidencia, porque afecta la fundamentación de `HD-INT-G` y de `HD-K3`.

---

## 5. Clasificación de modificaciones

La clasificación del encargo (editorial / declarativa / invalidante) se evalúa aquí contra la
evidencia. Se conserva, con **un cambio de fundamento** que la vuelve decidible.

### 5.1 Clase 1 — Modificación editorial

`FACT` — Criterio, tomado del mecanismo existente y no inventado
(`runtime/orchestrator/autonomy.py:_canonical_text`): *la representación cambia, el significado no*.

| Ejemplo | ¿Editorial? | Por qué |
|---|---|---|
| Re-envolver un campo, re-indentar, normalizar espacios | **Sí** | `_canonical_text` lo declara «the *same* declaration»; test dedicado |
| Corrección tipográfica que no altera términos ni cifras | **Sí** | la proyección canónica resultante es idéntica |
| Reordenar ítems de una lista de scope o de entregables | **Sí**, y además la proyección de scope es insensible al orden (`authorization_scope_projection` ordena) |
| Reordenar `## Pasos` cuando el orden es secuencia operativa | **No** | el orden *es* significado en una secuencia; cambia el significado, no la forma |
| «Aclaración textual que no cambia significado» | **Sí, sólo si es verificable como tal** | es una afirmación sobre el significado; §5.4 fija cómo se decide |
| Corrección de un path mal escrito (p. ej. `tools/foo.py` → `tools/fooo.py` donde sólo existe el segundo) | **No** | cambia el referente; es un cambio de valor, no de representación |

`FACT` — **Veredicto:** una modificación editorial **puede aceptarse sin re-derivación**, y el
repositorio ya tiene el criterio exacto. **No** puede aceptarse por ser «textual»: el criterio es
semántico, y el ejemplo del path mal escrito lo demuestra. La formulación correcta es:

```text
editorial  ⇔  canonical_text(antes) == canonical_text(después)   para cada campo afectado
```

`FACT` — Límite declarado: `_canonical_text` normaliza **whitespace**, no puntuación, no sinónimos,
no voz verbal. Por eso el criterio de §5.1 es una **cota inferior** verificable, no la definición
completa de «editorial»: hay cambios editoriales legítimos (una coma, una tilde) que este criterio
no reconoce como idénticos. Declararlos editoriales es juicio, y §5.4 dice cómo se registra un
juicio. **No** se propone extender `_canonical_text`: sería cambiar un mecanismo de autorización
para resolver un problema de clasificación editorial.

### 5.2 Clase 2 — Modificación declarativa humana

`DESIGN_OPTION` — El encargo pide evaluar si puede representarse como `Derived: X` /
`Human-confirmed: Y` sin que el sistema lea `Y` como una nueva derivación. **La evidencia dice que
sí, y que la representación ya existe** — con una precisión que la hipótesis B no hace:

`FACT` — La representación correcta no es `Derived: X` + `Human-confirmed: Y` sobre el **mismo
campo**. Es que **cada campo tiene una sola categoría**, y la categoría dice quién lo posee
(§3.5):

```text
campo Derivado          → lo produce el derivador; si el humano lo cambia, deja de ser derivado
campo Confirmado        → ARgentOS propone; el humano confirma (user_confirmed: true)
campo Declarado         → el humano lo declara; el derivador no lo completa nunca
campo Forbidden-to-infer→ su ausencia detiene; el humano lo provee
```

`FACT` — Por tanto **`Human-confirmed: Y` no es una segunda derivación: es la categoría `Declarado`
o `Confirmado` del campo `Y`**, y el repositorio ya tiene su vocabulario
(`user_confirmed: false` / `PENDING_USER_CONFIRMATION`).
`protocol/.agents/standards/runtime/AUTHORIZATION.md:AUTH-002` ya declara que un ítem no confirmado
**no autoriza**; la lectura simétrica es la que HD-K necesita: un ítem confirmado **sí** es la
declaración del humano, y **no** necesita ser re-derivado porque nunca fue del derivador.

`DESIGN_OPTION` — Campos que pueden modificarse de esta manera, **según la categoría de §3.5**:

| Campo | Se puede modificar declarativamente | ¿Invalida la derivación? |
|---|---|---|
| `**Origen:**` (Declarado) | Sí | Sólo si cambia la intención de la que se derivó → §8.2 |
| `## Delegación agentiva → Task` / `Scope` (Declarado) | Sí, por el humano | **Sí**, cuando el derivador los usó como premisa de otro campo → §8.2 |
| `## Objetivo`, `## Riesgos`, criterios de salida y de verificación con juicio (Confirmado) | Sí, confirmando o sustituyendo la propuesta | **Sí**, si el valor confirmado difiere del propuesto y de él se derivaron otros campos |
| `**Clase:**`, `**RFC:**` (Derivado + Confirmado) | Sí, en su mitad confirmatoria | **Sí**: la mitad derivada quedó producida con otro valor → §8.3 |
| `**Change Level:**`, `**Fecha:**`, `**Depende de:**`, `## Criterio de entrada`, `## Entregables`, `## Pasos`, `## Trazabilidad` (Derivado) | **No** como acto declarativo puro | **Sí**: son salida del derivador; cambiarlos a mano es exactamente el caso de §5.3 |

`FACT` — El criterio que separa «decido» de «invalido» **no es el campo, es su posición en el
grafo de la derivación** (§13). Un campo `Declarado` que **no** fue premisa de ningún campo derivado
se modifica sin invalidar nada; uno que **sí** lo fue, invalida. `Task`/`Scope` son el caso más
claro: son `Declarado` **y** premisa de `Entregables`, `Pasos`, `Verificación` y `work_type`.

### 5.3 Clase 3 — Modificación que invalida la derivación

`HYPOTHESIS` — El encargo enumera: cambia `work_type`; cambia Plan ↔ Note; cambia las reglas
aplicables; cambia una restricción normativa; amplía scope introduciendo nuevas reglas; cambia la
autoridad requerida; introduce un efecto no contemplado; modifica una condición que el derivador
usó como premisa.

`FACT` — Evaluadas una por una, **todas menos dos son el mismo caso**, y el caso es único: *el valor
modificado es una de las entradas con las que se produjo la derivación* (investigación previa
§12.1). Las dos excepciones tienen tratamiento propio:

| Modificación | ¿Es cambio de premisa? | Tratamiento |
|---|---|---|
| cambia `work_type` | **Sí** (premisa de obligaciones y entregables) | re-derivación (§8.3, §11) |
| cambia Plan ↔ Note | **Sí**, y es un cambio de forma del artefacto, no de contenido | decisión humana + re-derivación, con la restricción de `HD-INT-D`/`HD-INT-E` (§9.4, §11) |
| cambian las reglas aplicables | **Sí**, pero normalmente **no por edición del Plan**: porque cambió el repositorio | re-derivación, y **no** hay nada que el humano haya decidido |
| cambia una restricción normativa | **Sí**, y es `REQUIRES_HUMAN`/`FORBIDDEN` | detener y escalar; el humano decide la norma (§8.4) |
| amplía scope introduciendo nuevas reglas | **Sí** | re-derivación de reglas aplicables + re-derivación del resto |
| cambia la autoridad requerida | **Sí**, y es `FI-3` | detener y escalar (clase RFC-56, ¿RFC? ¿ADR?) |
| introduce un efecto no contemplado | **Sí**, y es `FI-1`/`FI-4` | detener y escalar |
| modifica una condición que el derivador usó | **Sí, por definición** | re-derivación |

`FACT` — **Conclusión de §5.3, y es la que vuelve decidible a la Clase 3:** la pertenencia a la
Clase 3 **no se decide por el tipo de cambio ni por el campo**, sino por una sola pregunta:

> ¿El valor modificado está en el conjunto de premisas con el que se produjo la derivación `D`?

`FACT` — Y esa pregunta **es decidible con la información que el modelo ya exige**: la
investigación previa §12.1 obliga al Plan derivado a declarar sus fuentes (`PD-5`: «el Plan
derivado cita sus fuentes; no las reescribe») y a registrar «el veredicto de derivabilidad y su
evidencia». Sin ese registro, la pregunta es `GAP` (§12).

### 5.4 La frontera que el encargo pide, y su límite honesto

`HYPOTHESIS` — El encargo pregunta si existe una frontera **mecánica** del tipo
`semantic-impact = false → modification accepted` / `semantic-impact = true → re-derive`.

`FACT` — **Existe, pero no sobre el texto, y no sin un dato que el sistema debe tener.** La frontera
mecánica correcta no compara el plan antes y después (eso exigiría versionado y volvería a
introducir la comparación de prosa que el repositorio ya rechazó:
`docs/plans/94-change-lifecycle-master-action-plan.md`; `.agents/policies/validation-closure.md:5.1`
y §4.8 punto 22 de la investigación previa). Compara **el conjunto de premisas registrado** contra
**el conjunto de premisas vigente**:

```text
premises(D) == premises(observed content)?   SÍ → D sigue siendo válida para ese contenido
                                             NO → D es inválida para ese contenido
```

`FACT` — **Su límite, declarado:** la frontera es mecánica **en la comparación**, no en la
**lectura** del cambio. Determinar *qué premisa* cambió cuando el humano reescribe prosa sigue
siendo una lectura semántica, y el repositorio **no tiene ni debe tener** un checker que interprete
prosa: `.agents/policies/validation-closure.md:5.1 Enforcement` lo declara («no checker interprets
prose»), `:5.2` lo repite, y la investigación previa §16 `A-22` descarta crear uno. Por eso:

> la frontera es **decidible cuando el derivador registró sus premisas**, y es `GAP`
> cuando no lo hizo — y `GAP` tiene un comportamiento propio (§12), no uno inventado.

`FACT` — No se introduce ningún scoring: la comparación de conjuntos es booleana, y la lista de
premisas está cerrada por la fuente citada (`PD-5` + §12.1 de la investigación previa).

---

## 6. Evaluación de la hipótesis B — modificación declarativa humana, conservando lo derivado y lo decidido

### 6.1 Qué afirma y qué acierta

`HYPOTHESIS` — B afirma: el humano modifica el `proposed`; el artefacto **conserva explícitamente**
qué fue derivado y qué fue decidido o modificado por el humano; el sistema **no** interpreta la
modificación como una nueva derivación.

| Dimensión | Veredicto | Evidencia |
|---|---|---|
| **Compatibilidad con `ADR-16`** | **Compatible, y ya enunciada en su dirección.** Una modificación humana es acto de la clase `DECISION`, que pertenece al mantenedor; `AU-5` prohíbe que el Plan modifique en silencio la decisión que implementa — una edición humana es, por definición, no silenciosa | `.agents/policies/authority.md:Authority classes`, `AU-5`; `runtime/orchestrator/authority.py` |
| **Compatibilidad con el Change Lifecycle** | **Compatible.** No crea estado: el artefacto sigue en `Aprobado para redacción` hasta la autorización, y `Executed` sigue significando implementación + validación | `docs/CONVENTIONS.md:Convenciones` (ciclo de planes); `.agents/workflows/change-lifecycle.md:3. Plan lifecycle` |
| **Compatibilidad con SAE** | **Compatible y reforzada.** B describe el momento pre-`pin`; SAE §1.2 gobierna el momento post-`pin`. No hay solapamiento ni contradicción: son ventanas disjuntas | `.agents/policies/supervised-autonomous-execution.md:1.2`; `authorization_drift(None, …)` |
| **`provenance`** | **Acierta en la necesidad.** El repositorio tiene procedencia para findings (`F-<n>`), correcciones (`C-<n>`), anchors (`A1`/`A2`) y checkpoints, y **ninguna** para «de dónde salió el contenido de este Plan». B nombra el hueco real | `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones`; `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity` |
| **`validation anchor`** | **Compatible, con una consecuencia que B no declara.** El anchor valida el **estado scoped** del contenido; si la modificación humana precedió a la validación, el anchor valida el resultado ya modificado y no dice nada sobre la derivación. El anchor **no** es un mecanismo de procedencia de derivación | `docs/CONVENTIONS.md:…Validation anchors… (VC-1)`; `runtime/orchestrator/observation.py:scoped_content_identity` |
| **`checkpoint`** | **Compatible.** El checkpoint de autorización fija la declaración vigente en la primera autorización; absorbe la modificación previa por construcción, y eso es correcto: lo que se autoriza es lo que existe **al** autorizar | `runtime/orchestrator/host.py:_pinned_autonomy_projection` |

### 6.2 Riesgos de B, evaluados

| Riesgo del encargo | ¿B lo introduce? | Análisis |
|---|---|---|
| una segunda autoridad | **No** | B no crea autoridad: registra un acto del mantenedor que `ADR-16` ya posee |
| una segunda state machine | **No** | no crea estados; usa `Aprobado para redacción`/`Aprobado para ejecución` |
| una segunda representación de Change | **No** | no crea entidad; el registro vive en el artefacto que ya lo posee (PC-1) |
| ambigüedad sobre qué fue derivado | **Sí, si B se implementa como dos anotaciones sobre el mismo campo** | `Derived: X` **y** `Human: Y` sobre un campo deja el campo con dos valores y ninguna regla de precedencia. La corrección es de §5.2: **una sola categoría por campo**, no dos anotaciones |
| pérdida de trazabilidad | **No, si se conserva la derivación anterior** | ver la condición de §6.3 |
| autorización implícita | **Riesgo real.** Si «el humano modificó» se trata como equivalente a «el humano autorizó», B colapsaría modificación y autorización | Se cierra con la regla explícita: **modificar ≠ autorizar** (§9.3). `PC-52` («a request is not an authorization») es el precedente literal |
| expansión silenciosa de scope | **Riesgo real, y es el caso del incidente F-3** | Se cierra porque ampliar `Scope` es `CHANGE_SCOPE` ∈ `FORBIDDEN_ACTIONS` para el host y requiere acto humano; y porque el checkpoint lo detecta si ocurre después del `pin` |
| deriva entre intención, derivación y objeto autorizado | **Es exactamente el riesgo que B no resuelve sola** | B registra, pero **no decide re-derivar**. Si la premisa cambió y nadie re-deriva, el objeto autorizado es coherente consigo mismo y **no** con su derivación. Es el hueco que cubre C (§7) |

### 6.3 Veredicto sobre B

`HYPOTHESIS` — **B es necesaria y verdadera en su núcleo, pero insuficiente por sí sola.**

- Verdadera: la modificación humana pre-autorización **es** un acto declarativo legítimo, no una
  violación; el repositorio ya tiene la categoría (`Declarado`/`Confirmado`, `user_confirmed`), y el
  sistema **no** debe leerla como nueva derivación.
- Insuficiente: B describe la **representación** del acto, no su **consecuencia**. Registra que el
  humano decidió, y deja sin respuesta la pregunta que el encargo hace en su §2: cuándo la
  modificación **invalida la derivación previa y exige una nueva derivación**.
- Corrección necesaria a B, y es la única que la evidencia impone: **una sola categoría por campo**
  (§5.2), y **conservación de la derivación anterior como procedencia**, no su borrado ni su
  mutación (§10).

---

## 7. Evaluación de la hipótesis C — re-derivación selectiva

### 7.1 Qué afirma

`HYPOTHESIS` — C afirma: determinados cambios semánticamente relevantes requieren re-derivación;
los puramente editoriales no.

### 7.2 Veredicto: C acierta en la dirección y **falla en el criterio declarado**

`FACT` — «Semánticamente relevante» **no es una frontera decidible** por sí misma, y la evidencia lo
demuestra en dos niveles:

1. **«Semántico» requiere interpretar prosa.** El repositorio declara explícitamente que ningún
   checker interpreta prosa: `.agents/policies/validation-closure.md:5.1 Enforcement` — «The
   obligation is governance, not a semantic validation. **No checker interprets prose** or decides
   whether a document is up to date» — y lo repite en `:5.2`. `docs/plans/94-change-lifecycle-master-action-plan.md:13. Estrategia de Policies` mantiene por eso
   las reglas de L0/L1 en prosa normativa y no en checkers obligatorios. Un
   criterio que exija decidir «¿esto cambió el significado?» hereda ese límite.
2. **«Semánticamente relevante» no distingue las tres cosas que el encargo separa.** Que un cambio
   sea semántico no dice si (a) invalida la derivación, (b) requiere una decisión humana, o
   (c) ambas. Y hay cambios semánticos que **no** invalidan nada: por ejemplo fijar en `## Objetivo`
   una redacción que el humano confirma y que **no** fue premisa de ningún campo derivado.

`FACT` — Y hay un segundo defecto, más importante: **C, tal como está enunciada, no dice quién
re-deriva ni cuándo.** «Re-derivar» en la ventana pre-autorización es trabajo del agente sobre una
propuesta; «re-derivar» después de la autorización es una ampliación de scope, que
`.agents/policies/supervised-autonomous-execution.md:1.4` prohíbe al host. Un criterio único para
ambos momentos sería el error que el encargo prohíbe explícitamente (§8 del encargo: «No mezcles
estos dos momentos»).

### 7.3 La frontera mecánica que sí existe

`DESIGN_OPTION` — Sustituto de la frontera subjetiva de C, con evidencia:

```text
premises(D)  = el conjunto de entradas con el que D fue producida,
               registrado por el derivador (PD-5) y enumerado en la investigación previa §12.1

modificación M de un campo F:

  F ∉ premises(D)  ∧  F es Declarado|Confirmado     →  M es decisión humana;  D sigue válida
  F ∈ premises(D)  ∧  M proviene del humano          →  D inválida para el nuevo contenido
  F ∈ premises(D)  ∧  M exige autoridad humana       →  STOP / REQUIRES_HUMAN (FI-1…FI-10)
  premises(D) no puede establecerse                  →  GAP (§12)
  canonical_text(F) == canonical_text(F')            →  editorial; nada que re-derivar (§5.1)
```

`FACT` — **Por qué esta frontera es mejor que «semántico»:** es una **pertenencia a un conjunto**
sobre datos que el modelo ya obliga a registrar, no un juicio sobre significado. Y donde el
conjunto no puede establecerse, **no adivina**: cae en `GAP`, que tiene comportamiento
propio.

`FACT` — **Límite, declarado sin adornos:** sigue habiendo un paso de lectura —determinar *cuál*
premisa tocó la modificación— cuando el humano reescribe prosa libre. Ese paso es humano o
asistido, y el sistema honesto es el que **lo declara y se detiene** en vez de inferirlo. No se
propone ningún scoring, ningún umbral y ninguna métrica de impacto.

### 7.4 Veredicto sobre C

`HYPOTHESIS` — **C es correcta en su conclusión y no utilizable en su criterio, tal como está
enunciada.**

- Correcta: hay cambios que exigen re-derivación y cambios que no.
- No utilizable: «semánticamente relevante» es un juicio sobre prosa que el repositorio prohíbe
  mecanizar, y no distingue los tres resultados que HD-K necesita (edición / decisión / invalidación).
- Reemplazo propuesto: **pertenencia al conjunto de premisas registrado** (§7.3), con
  `GAP` para el caso no decidible.

`FACT` — **Conclusión sobre B+C:** la hipótesis **no es suficiente tal como está formulada, y sí lo
es con dos correcciones**: (1) B pasa de «dos anotaciones por campo» a **una categoría por campo**
(§5.2); (2) C pasa de «semántico vs editorial» a **pertenencia a `premises(D)`** (§7.3). Con esas dos
correcciones, B+C es suficiente para las Clases 1 y 3, y **no** para la Clase 2 cuando el humano
introduce algo que no estaba en ninguna categoría — que es el caso de §10.4.

---

## 8. Analizar interacción con Scope (obligatorio)

### 8.1 La regla ya establecida

`FACT` — `.agents/policies/supervised-autonomous-execution.md:1.1`/`:1.3`/`:1.4`, y el contrato de
autorización que el Plan posee: «Scope y Task forman parte de la base de autorización y una
modificación no autorizada debe detener la ejecución». El repositorio lo declara como frontera
humana: «The human remains exclusively the authority for: authorizing scope, and authorizing scope
changes» (`:8. Human boundary`). Y `docs/plans/138-…:PC-2` está `deferred`: no existe mecanismo
autónomo de Scope Expansion.

### 8.2 Los dos momentos, separados

`FACT` — Son **momentos distintos**, con **mecanismos distintos**, y el encargo prohíbe mezclarlos:

```text
MOMENTO 1 — pre-autorización (HD-K)

  Scope declarado por el humano (Declarado, FI-2)
        ↓
  el derivador construye D usando Scope como premisa (Entregables, Pasos, Verificación, work_type)
        ↓
  el humano MODIFICA Scope  ← el acto humano que forma la autorización
        ↓
  premises(D) cambió  ⇒  D es inválida para el nuevo contenido
        ↓
  el agente RE-DERIVA  ⇒  Plan/Note proposed (nuevo contenido, misma identidad de artefacto)
        ↓
  el humano AUTORIZA  ⇒  Aprobado para ejecución
        ↓
  pin de la proyección de autorización  ← recién aquí empieza MOMENTO 2


MOMENTO 2 — durante la ejecución (ya resuelto por el repositorio)

  Scope autorizado + pin
        ↓
  Scope modificado durante la ejecución
        ↓
  STOP_SCOPE_VIOLATION + REQUIRES_HUMAN, sin efecto persistente, checkpoint original preservado
```

`FACT` — **Qué NO es un mecanismo nuevo en el Momento 1:** re-derivar. `CHANGE_SCOPE` es
`FORBIDDEN` para el host y por tanto **ningún agente cambia el scope**; el humano lo cambia y el
agente re-deriva lo que **depende** de él. Eso es exactamente lo que un agente ya hace hoy: proponer.
La prohibición de `approve_plan`/`CHANGE_SCOPE` no se toca (`.agents/policies/authority.md`;
`runtime/orchestrator/authority.py:FORBIDDEN_ACTIONS`).

### 8.3 `premises(D)` y el Scope: el punto exacto donde el Momento 1 se vuelve decidible

`FACT` — El Scope es `Declarado` **y**, a la vez, premisa del derivador. Es la única entrada con
esa doble condición, y es lo que hace de HD-K una pregunta no trivial. La consecuencia, explícita:

```text
el humano MODIFICA Scope antes de autorizar
   ⇒  NO es una violación (el humano es el dueño del scope)
   ⇒  NO es una autorización
   ⇒  ES un cambio de premisa  ⇒  la derivación previa queda inválida para el nuevo contenido
   ⇒  el agente re-deriva   ⇒  nuevo contenido proposed  ⇒  el humano autoriza
```

`FACT` — Y una asimetría que la evidencia obliga a declarar y que **no** puede resolverse por
inferencia:

| Modificación de `Scope` | ¿Cambia `premises(D)`? | ¿Re-derivación? |
|---|---|---|
| **Reducción** (quitar un path) | Puede, pero no necesariamente: puede no alterar ninguna obligación resuelta | Indeterminado por regla general ⇒ **se re-deriva igual**, porque la resolución de reglas aplicables es total y barata: re-derivar es la respuesta honesta cuando no puede demostrarse que nada cambió |
| **Ampliación** (agregar un path) | **Sí, siempre que el path nuevo traiga obligaciones**; y no puede demostrarse lo contrario sin re-resolver | **Sí, obligatoria** |

`PC-1:HD-K1` (`resolución: adoptada`, 2026-10-05) — Si una **reducción** de scope que no altera ninguna obligación
resuelta debe poder aceptarse **sin** re-derivación. La evidencia no permite decidirlo: `FI-9`
prohíbe leer una ausencia de regla como permiso, y `DV-2` (investigación previa §7.3) prohíbe llamar
«sin señal bloqueante» a un resultado con dos lecturas. La respuesta segura (re-derivar) está disponible y no
requiere decidir nada; **declarar aceptable la reducción sin re-derivación sí lo requiere.**

### 8.4 Cuando la modificación de scope *introduce* una regla o cambia la autoridad

`FACT` — El encargo nombra «amplía scope de forma que introduce nuevas reglas» y «cambia autoridad
requerida». Son categorías distintas y la evidencia las separa:

| Caso | Naturaleza | Comportamiento |
|---|---|---|
| El nuevo scope trae una regla aplicable que antes no aplicaba | cambio de premisa (**re-derivable**) | re-derivar; la regla nueva se **consulta** en su fuente, no se reescribe (patrón `PC-75`, investigación previa §2.7) |
| El nuevo scope exige una decisión normativa nueva | `FI-4` (**not derivable**) | `STOP` / `REQUIRES_HUMAN`: el humano decide la norma |
| El nuevo scope cambia la autoridad requerida (¿RFC? ¿ADR? ¿Clase A?) | `FI-3` (**not derivable**) | `STOP` / `REQUIRES_HUMAN`; `AU-6` declara ADR-worthiness como juicio humano |
| El nuevo scope toca `protocol/.agents/` | frontera de payload | `STOP_AUTHORITY_REQUIRED`: vía RFC-56 |

`FACT` — En los tres últimos casos la respuesta **no** es re-derivar: es detenerse. Re-derivar
sería convertir una decisión humana en inferencia, exactamente lo que `FI-3`/`FI-4` y
`.agents/policies/authority.md:Stop conditions (authority)` prohíben.

---

## 9. Interacción con lifecycle, identidad y autorización

### 9.1 Los cinco ejes no se mezclan

`FACT` — El encargo pide no confundirlos. Cada uno tiene dueño y vocabulario propios:

| Eje | Qué expresa | Vocabulario | Dueño |
|---|---|---|---|
| **Lifecycle del artefacto** | vigencia semántica | `active`/`archived`/`superseded`/`deprecated` (`docs/AGENTS.md:Lifecycle`) | documento (§9 de la investigación previa) |
| **Estado de gobernanza** | ciclo de status del Plan | `Aprobado para redacción`/`Aprobado para ejecución`/`Executed`/`Superseded` (`docs/CONVENTIONS.md:Convenciones`) | header del artefacto |
| **Estado de ejecución** | condiciones derivadas | `Verified`/`Executed`/`Committed`/`Closed`/`Promoted`/`Released` (`runtime/orchestrator/contracts.py:DERIVED_CONDITIONS`) | derivación sobre hechos |
| **Derivación** | de dónde salió el contenido | `Derivado`/`Declarado`/`Confirmado`/`Forbidden-to-infer` (§3.5) | **no materializado (§4.7)** |
| **Autorización** | quién autorizó y bajo qué contrato | status autorizante + proyección de autorización (`autonomy.py`) | acto humano + checkpoint |

`FACT` — Consecuencia directa, y responde la pregunta de §9 del encargo: **una modificación de un
`proposed` Plan/Note no debe producir ningún estado nuevo de lifecycle ni ningún cambio de status.**
El artefacto:

- **conserva identidad** (la identidad del Plan es su número: `docs/AGENTS.md:Identity`, «Identidad ≠
  path»);
- **no produce una nueva versión** (no existe versionado de Planes en el repositorio; no se
  introduce uno: `docs/AGENTS.md:Identity` declara que no hay registry global y que los INDEX son
  el mapa; y el encargo prohíbe crear primitives de identidad);
- **no produce un nuevo artefacto** (crear un artefacto intermedio fue explícitamente descartado:
  investigación previa §12.5 y §16 `A-14`);
- **invalida la derivación previa** cuando toca una premisa, y eso se registra **como procedencia**,
  no como estado;
- **registra una decisión humana** cuando es un acto declarativo.

### 9.2 Identidad: la derivación tiene identidad, el Plan no la necesita

`FACT` — La identidad que HD-K necesita **no es una nueva primitive**: es la que el repositorio ya
usa para anchors y correcciones. `A1`/`A2` (`docs/CONVENTIONS.md:…Validation anchors…`) son el
precedente exacto: dos validaciones distintas, la segunda **nunca** muta la primera, ambas
referenciadas, cada una con su propia identidad. `C-<n>` (`…Findings y correcciones…`) es el otro:
un registro factual de una corrección con provenance a su origen.

`DESIGN_OPTION` — Traducido a HD-K, **sin crear nada**:

```text
la derivación D es un registro con procedencia propia (premisas citadas, PD-5)
la modificación humana M es la provenance del valor que reemplaza al derivado
el Plan/Note P es el artefacto gobernable: mantiene su identidad de artefacto
la autorización A autoriza P tal como está al autorizar

  Intent → D1 → P (M1) → D2? → A1

D1 conserva su registro (no se borra: es procedencia)
M1 se registra como decisión humana en P, con su categoría de campo
D2 se produce sólo si premises(D1) cambió; si no, D1 sigue vigente y M1 es la decisión
A1 autoriza P en su estado final: la modificación previa a A1 queda absorbida por A1
```

`FACT` — **Respondiendo las preguntas de §10 del encargo:**

| Pregunta | Respuesta con evidencia |
|---|---|
| ¿Hay que distinguir `derived identity` de `authorized artifact identity`? | **No hace falta una distinción de identidad del artefacto** (es el mismo Plan, mismo número). **Sí** hace falta distinguir **la procedencia del contenido** (derivado vs declarado) de **la autorización** (el `pin`): son dos registros distintos y el segundo ya existe |
| ¿El objeto modificado sigue siendo el mismo Plan/Note? | **Sí.** Misma identidad de artefacto, mismo path, mismo número |
| ¿Hace falta versionado? | **No**, y no se introduce. La procedencia de la modificación se registra donde el repositorio ya registra procedencia: en el artefacto que la posee (PC-1) |
| ¿Ya existe un mecanismo suficiente? | Para la **autorización**: sí (`autonomy.py`). Para la **procedencia de la derivación**: **`GAP`** (§4.7) |
| ¿La identidad debe ser conceptual, material o ambas? | **Conceptual**: la identidad del artefacto es su número; la de la derivación es su conjunto de premisas. No se requiere identidad material (hash de la derivación) para decidir; y la identidad material del **contenido** ya existe donde importa: `Scoped Content Identity` en el anchor |
| ¿Qué debe quedar verificable al cerrar el Change? | (a) qué se autorizó y bajo qué contrato (`pinned_projection`); (b) qué estado se validó (`anchor`, `delta scoped identity`); (c) por qué el contenido autorizado es el que es — **(c) es el eslabón que hoy falta** |

### 9.3 Modificar ≠ autorizar (el riesgo que hay que cerrar explícitamente)

`FACT` — `PC-52` («A request is not an authorization») y `AUTH-002` (`user_confirmed=false` nunca
constituye autorización) ya enuncian la separación. El caso inverso —un acto humano declarativo
**no** es automáticamente la autorización— **no está enunciado**, y hay que declararlo porque es el
riesgo principal de B (§6.2):

```text
el humano modifica el Plan/Note proposed     ⇏     el humano autorizó el Plan/Note
la autorización sigue siendo el acto que lleva el status a Aprobado para ejecución
```

`FACT` — La evidencia de que esta separación ya se respeta en la práctica: Plan 136 (§4.1), donde
el mantenedor autorizó por directiva y el repositorio **no** lo leyó como un simple cambio de
contenido, sino como una decisión humana que hubo que registrar como pending decision resuelta.

### 9.4 Plan ↔ Note: la única modificación de forma

`FACT` — Cambiar Plan ↔ Note **no es un campo del Plan**: es un cambio de **forma del artefacto**,
y su tratamiento no lo puede decidir esta investigación:

- `HD-INT-D` (**resuelta**, acto del mantenedor 2026-10-02: Opción A) decide **dónde vive y cómo se
  registra** la Nota (opciones A/B/C con impacto en el Placement Contract, `PC-20`).
- `HD-INT-E` (**resuelta**, acto del mantenedor 2026-10-02) decide **la vía de autorización** del trabajo
  sin Plan y su frontera con Clase C/L0.
- `HD-INT-E2` (**consecuencia derivada de `HD-INT-E`**, sin autoridad propia) fija que Plan vs Note se
  deriva **por criterios**, no por mapeo a Change Level.

`FACT` — Consecuencia para HD-K: la transformación Plan ↔ Note es, por `HD-INT-E2`, **un resultado
derivado**. Si el humano la cambia, es un cambio de premisa del derivador y cae en §7.3 (re-derivar
con el criterio nuevo, si `HD-INT-E` ya lo fijó). **Qué es exactamente una Note** sigue dependiendo de
`HD-INT-D`: no se puede decidir aquí sin resolver `HD-INT-D` por inferencia, y eso está prohibido.

`GAP` — Mientras `HD-INT-D`/`HD-INT-E` estén abiertas, la Clase 3 «cambia Plan ↔ Note» **no tiene
comportamiento decidible**: el sistema no puede comparar «¿sigue siendo Plan?» contra un criterio que
no existe.

---

## 10. Alternativas adicionales (sólo las justificadas por la evidencia)

Se evaluaron tres. Sólo la primera se sostiene.

### 10.1 `DESIGN_OPTION` D-1 — Re-derivación local: re-derivar sólo el subgrafo afectado

**Justificación:** la derivación es un grafo campo → premisas (investigación previa §12.1). Cambiar
`Scope` no invalida `## Objetivo`, que no depende de `Scope`.

**Ventajas:** menos trabajo; menos riesgo de que una re-derivación total altere campos que el humano
ya había confirmado.

**Riesgos:** exige conocer el grafo de dependencias, que **no está declarado** en ningún artefacto
(la tabla de §12.1 de la investigación previa es un `DESIGN_OPTION` de esa investigación, no un
campo del Plan). Sin ese grafo, «re-derivación local» es una inferencia.

**Veredicto:** **compatible en principio, no decidible hoy.** Si el Change de implementación
materializa el grafo de premisas como parte de `PD-5`, D-1 se vuelve decidible. Mientras no, la
re-derivación total es la respuesta honesta.

### 10.2 `DESIGN_OPTION` D-2 — Registrar la modificación como «corrección» (`C-<n>`)

**Justificación:** el repositorio ya tiene `C-<n>` para correcciones con provenance.

**Por qué se descarta:** `C-<n>` es un registro de la corrección de un **finding** sobre el
**contenido ejecutado**, con alcance de revalidación
(`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (LC-1)`). Usarlo para una
modificación de la propuesta pre-autorización sería (a) forzar un mecanismo a un caso que no es el
suyo, (b) crear un finding ficticio, y (c) sugerir que hubo una corrección cuando puede haber sido
una decisión de alcance. El registro correcto es el que el artefacto ya posee: la decisión en el
propio Plan (`PC-1`).

### 10.3 `DESIGN_OPTION` D-3 — Prohibir la modificación humana del `proposed` (sólo re-derivar)

**Justificación:** si toda modificación humana de un plan derivado exigiera una re-derivación
completa desde una intención nueva, el artefacto derivado nunca se editaría a mano.

**Por qué se descarta, con evidencia:** (a) contradice el acto mismo de autorización tal como el
repositorio lo ejerce — Plan 136 (§4.1) autorizó *fuera* del texto del artefacto; (b) convierte la
edición humana en una sospecha en lugar de un acto, contra `AU-5` («no silenciosamente», es decir:
la modificación legítima se registra, no se prohíbe); (c) un `proposed` **no autorizado** es texto:
prohibir su edición no protege nada que el gate de autorización no proteja ya.

### 10.4 `DESIGN_OPTION` D-4 — Un tercer resultado: la modificación **añade** una premisa que el derivador no consideró

**Justificación, y por qué es la alternativa que la evidencia sí exige:** hay un caso que ni B ni C
cubren. `FI-2` prohíbe al agente **suponer** scope. Pero el humano puede añadir al `proposed` un
elemento que **no era premisa de nada** (p. ej. un criterio de salida propio, un riesgo que el
derivador no consideró). Eso no invalida `premises(D)` — no fue entrada — y **no** es una simple
confirmación de una propuesta.

```text
M añade a P un elemento E que no estaba en premises(D) y no se deriva de ellas
    ⇒  D sigue siendo válida para lo que D produjo
    ⇒  E es una declaración humana nueva, con su categoría (Declarado)
    ⇒  P ya no es "el resultado de D": es "el resultado de D más la declaración E"
    ⇒  la autorización A1 autoriza ese conjunto, y la procedencia de E queda registrada
```

**Ventajas:** es el único caso en que «no re-derivar» es la respuesta **correcta**, y sin esta
categoría el sistema re-derivaría de más y posiblemente **borraría** la declaración humana (el
riesgo real de toda re-derivación total).

**Riesgos:** que la categoría se use para introducir por la puerta de atrás algo que requería
decisión humana. Se acota con `FI-1`…`FI-10`: si `E` cae en la lista, no es D-4, es `STOP`.

**Veredicto:** **es el complemento que B+C necesita** (§7.4), y es la razón por la que el modelo
recomendado de §9.5 tiene cuatro resultados y no tres.

---

## 11. Modelo recomendado

`DESIGN_OPTION` — **No es una decisión y no la toma esta investigación.** Es la lectura que la
evidencia sostiene, con su justificación por paso.

### 11.1 El flujo exacto

```text
[humano]   Intent
              ↓
[agente]   Context  →  Derivation D1  →  Plan/Note P (proposed, Aprobado para redacción)
              ↓                                   ↓
              ↓                       ┌───────────┴────────────┐
              ↓                       ↓                        ↓
              ↓            el humano MODIFICA P        el humano no modifica
              ↓                       ↓                        ↓
              ↓            ┌──────────┴──────────┐             ↓
              ↓            ↓          ↓          ↓             ↓
              ↓        editorial   declarativa  premisa        ↓
              ↓            ↓          ↓          ↓             ↓
              ↓       P se corrige  se registra  premises(D1)  ↓
              ↓       (D1 intacta)  la decisión  cambió → D1   ↓
              ↓            ↓        humana       inválida      ↓
              ↓            ↓          ↓          ↓             ↓
              ↓            └──────────┴──────────┴─────────────┘
              ↓                                   ↓
              ↓                       [agente] re-deriva el subgrafo
              ↓                       afectado (D-1) o D2 completo
              ↓                                   ↓
              ↓                       P actualizado (sigue proposed)
              ↓                                   ↓
[humano]   AUTORIZACIÓN  ← el acto humano: Status = Aprobado para ejecución
              ↓
           pin de la proyección de autorización   ← recién aquí empieza SAE
              ↓
[SAE]      ejecución: observe → derive → delegate → execute → verify →
           correct/revalidate → continue → stop
```

### 11.2 Justificación de cada paso

| Paso | Por qué |
|---|---|
| La modificación humana ocurre **antes** de la autorización, sobre un artefacto sin autorizar | es texto propuesto: `runtime/orchestrator/derivation.py (regla 1)` detiene cualquier ejecución en ese estado |
| La modificación **no** cambia el status | el status es de gobernanza; la modificación es de contenido (§9.1) |
| La modificación **no** amplía autoridad ni scope autónomamente | `CHANGE_SCOPE`/`APPROVE_PLAN` ∈ `FORBIDDEN_ACTIONS`; `:1.4` no admite scope expansion |
| La re-derivación la hace el **agente** | derivar es proponer; el agente ya propone (`M-1`: derivar ≠ autorizar) |
| La autorización la hace **el humano**, después | es el único acto que crea autoridad (`ADR-16`, clase `DECISION`) |
| El `pin` ocurre en la **primera acción autorizada**, no antes | es el comportamiento actual y correcto: lo que se autoriza es lo que existe **al** autorizar |
| Toda modificación **posterior** al `pin` sigue el camino existente | `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`; **no** se toca |

### 11.3 Por qué este modelo no introduce nada de lo prohibido

| Prohibición del encargo | Por qué no se viola |
|---|---|
| una segunda autoridad | sólo el mantenedor autoriza; el agente sigue sin poder aprobar ni cambiar scope |
| una segunda state machine | ningún estado nuevo; `Aprobado para redacción`/`Aprobado para ejecución`/`Executed` alcanzan |
| una segunda representación de Change | el registro vive en el artefacto que lo posee (PC-1); no hay entidad |
| ambigüedad sobre qué fue derivado | una **sola categoría por campo** (§5.2) elimina la doble anotación |
| pérdida de trazabilidad | D1 se conserva como procedencia; `A1`/`A2` son el precedente |
| autorización implícita | «modificar ≠ autorizar» explícito (§9.3) |
| expansión silenciosa de scope | `CHANGE_SCOPE` es humano y `FORBIDDEN` para el host; el `pin` detecta lo posterior |
| deriva intención ↔ derivación ↔ objeto autorizado | la comparación `premises(D)` vs premisas vigentes (§7.3) la detecta, y `GAP` detiene cuando no puede |

---

## 12. Reglas de decisión

`DESIGN_OPTION` — Tabla operativa: **una sola pregunta de entrada**, cuatro salidas.

```text
Entrada: una modificación humana M sobre un Plan/Note P en estado proposed.
Pregunta 1 (editorial):  canonical_text(campo) es idéntico antes y después?
Pregunta 2 (premisa):    ¿qué campo(s) tocó M, y alguno está en premises(D)?
Pregunta 3 (autoridad):  ¿lo que M introduce cae en FI-1…FI-10?
Pregunta 4 (decidible):  ¿premises(D) pudo establecerse?
```

| # | Cuándo | Resultado | Se registra | Evidencia que lo sostiene |
|---|---|---|---|---|
| **R-1** | la modificación es **editorial** (proyección canónica idéntica) | **Se acepta. La derivación se conserva.** No hay nada que re-derivar | nada nuevo (la proyección es idéntica) | `autonomy.py:_canonical_text`; `test_rewrapping_a_field_is_not_a_change_of_authorization` |
| **R-2** | toca un campo `Declarado`/`Confirmado` que **no** es premisa de ningún campo derivado, y no cae en `FI-1`…`FI-10` | **Se acepta. Se registra como decisión humana.** La derivación se conserva; el artefacto ya no es sólo el resultado de D | la decisión en el artefacto que la posee (PC-1), con la categoría del campo | §5.2; `NO_ASSUMPTIONS.md:Recording user decisions` (`user_confirmed: true`); `PC-52` |
| **R-3** | **añade** un elemento que no era premisa y no se deriva de ellas (D-4) | **Se acepta como declaración humana nueva.** D sigue válida para lo que produjo; el artefacto pasa a ser «D + la declaración» | la declaración, con su categoría | §10.4; `FI-2` (el scope se declara, no se supone) |
| **R-4** | toca un campo que **es** premisa de `D` (incluye `Scope`/`Task` que el derivador usó) | **La derivación `D` queda inválida para el contenido nuevo. Se re-deriva** (subgrafo afectado si el grafo está declarado; completo si no) | D1 como procedencia; D2 como nueva derivación; el artefacto vuelve a `proposed` | §7.3; §8.2; `PD-1`/`PD-5` |
| **R-5** | lo introducido cae en `FI-1`…`FI-10` (norma nueva, autoridad, efecto no contemplado, resolución de conflicto, `protocol/.agents/`) | **Se detiene.** `STOP` / `REQUIRES_HUMAN`, con la decisión que falta nombrada | la decisión requerida y quién la posee | `FI-1`…`FI-10`; `authority.py`; `.agents/policies/authority.md:Stop conditions`; `AU-6` |
| **R-6** | `premises(D)` **no puede establecerse** (el derivador no las registró, o hay dos lecturas) | **`GAP` (falta el registro) o `BOUNDARY` (dos lecturas)**: se detiene y se pide aclaración con el formato existente. **No** se asume que la derivación sobrevive ni que murió | qué falta y por qué se necesita | §13.4; `NO_ASSUMPTIONS.md:Clarification request format`; `AUTHORIZATION_UNDETERMINED` + `AUTH-004` (nunca reportar `UNAUTHORIZED` por ausencia) |
| **R-7** | la modificación ocurre **después** de la primera autorización de una acción | **No es HD-K.** Camino existente: `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`, sin efecto persistente | el `pin` original y la divergencia | `.agents/policies/supervised-autonomous-execution.md:1.2`; `tests/test_sae_scope_enforcement.py` |

`FACT` — **Invariantes del modelo recomendado** (escritos en la forma del repositorio, y ninguno
nuevo: son lectura de los existentes):

```text
MK-1  modificar(P) ⇏ autorizar(P)          (PC-52 / AUTH-002)
MK-2  una sola categoría por campo          (§5.2)
MK-3  premises(D) cambió ⇒ D inválida para el contenido nuevo
MK-4  editorial ⇔ proyección canónica idéntica  (autonomy.py:_canonical_text)
MK-5  premises(D) no establecible ⇒ GAP (o BOUNDARY si hay dos lecturas), nunca asunción
MK-6  post-pin, el camino es el existente (STOP_SCOPE_VIOLATION); HD-K no lo toca
MK-7  re-derivar es proponer; no autoriza, no amplía scope, no cambia autoridad
MK-8  D1 se conserva como procedencia; nunca se muta ni se borra (A1/A2, C-<n>)
```

---

## 13. Resolver la incertidumbre con el vocabulario existente

`FACT` — El encargo pide usar el vocabulario existente sin inventar categorías. Las señales vigentes son
`GAP`/`ANOMALY`/`FAIL`/`BOUNDARY` y `REQUIRES_HUMAN`; los términos de veredicto (`DERIVED`/`UNDETERMINED`/
`NOT_DERIVABLE`/`MISSING`/`CONFLICT`) fueron **eliminados** como taxonomía (quedan como provenance, abajo).
Estado real de cada término:

| Término | Origen | Estado | Uso en HD-K |
|---|---|---|---|
| `DERIVED` / `UNDETERMINED` / `NOT_DERIVABLE` (eliminados) | investigación previa §7.1 | **provenance** — sin vigencia normativa | reemplazados por las señales existentes: sin señal bloqueante · `GAP` · `ANOMALY`/`BOUNDARY` · `REQUIRES_HUMAN` |
| `MISSING` / `CONFLICT` (eliminados) | subcasos de la taxonomía retirada (investigación previa §7.1) | **provenance** | la distinción la expresan hoy `GAP` (falta el registro) y `BOUNDARY` (dos lecturas) |
| `GAP` / `ANOMALY` / `FAIL` / `BOUNDARY` | `.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP` | `IMPLEMENTED` como vocabulario de señales (`runtime/orchestrator/contracts.py:SIGNALS`) | `GAP` = falta el registro; `ANOMALY` = dos fuentes se contradicen; `BOUNDARY` = ambigüedad estructural |
| `REQUIRES_HUMAN` | `runtime/orchestrator/authority.py` | `IMPLEMENTED` | resultado de `R-5` |
| `AUTHORIZATION_UNDETERMINED` + `AUTH-004` | `protocol/.agents/standards/runtime/AUTHORIZATION.md:Authorization states` | `IMPLEMENTED` en el Protocol | precedente literal de `R-6` |

### 13.1 La respuesta exacta a la pregunta de §12 del encargo

> Si el humano modifica un campo y ARgentOS no puede determinar si la modificación preserva la
> derivación, ¿qué resultado corresponde?

`DESIGN_OPTION` — **`GAP` + `NEEDS_CLARIFICATION`**, y el comportamiento es **pedir la aclaración con el
formato existente**, no asumir en ninguna dirección. La justificación, con evidencia:

- `AUTH-004` establece el principio general: la falta de registro **no** se reporta como un veredicto
  negativo. Simétricamente, aquí no se reporta que la derivación murió.
- `NO_ASSUMPTIONS.md:When to ask for clarification` exige exactamente una interpretación razonable
  para poder avanzar; con dos, no se avanza.
- `.agents/workflows/change-lifecycle.md:10` distingue `GAP` (falta evidencia) de `ANOMALY`
  (contradicción): el caso «no se registraron las premisas» es `MISSING`/`GAP`; «dos lecturas
  razonables del mismo cambio» es `CONFLICT`, y su tratamiento existente es `ANOMALY`/`BOUNDARY` +
  escalación.

`FACT` — **Y una consecuencia importante:** el hecho de que `R-6` sea alcanzable **no** es un
defecto del modelo; es el argumento a favor de `PD-5` (el Plan derivado cita sus fuentes). Un modelo
que obliga a registrar las premisas hace que `R-6` sea excepcional; uno que no, lo hace la regla.

### 13.2 Lo que HD-K **no** puede tomar de la investigación previa por inferencia

`FACT` — `DERIVED`/`UNDETERMINED`/`NOT_DERIVABLE` eran `DESIGN_OPTION` de la investigación previa
(histórico: ya **eliminados** como taxonomía; `HD-INT-A`/`HD-INT-H` fueron adoptados). HD-K **no** los
adopta: su modelo queda gobernado por las señales existentes y las reglas HD-K adoptadas (2026-10-05).

---

## 14. Evaluación de la regla de invalidación por premisas (§13 del encargo)

`HYPOTHESIS` — El encargo propone: «Una modificación humana que cambia cualquier dato utilizado como
premisa de una derivación invalida esa derivación.»

### 14.1 Veredicto

`HYPOTHESIS` — **Es correcta como regla, con tres precisiones que la evidencia impone.**

1. **«Premisa» debe ser enumerable y registrada.** Sin registro, la regla es inaplicable (→ `R-6`).
   La lista existe como `DESIGN_OPTION` (investigación previa §12.1: intención, confianza, contexto,
   veredicto de derivabilidad, `work_type`, conocimiento vigente, reglas aplicables, autoridad/scope).
2. **«Invalida» no significa «borra».** Significa: `D` deja de ser válida **para el contenido
   nuevo**; `D` se conserva como procedencia (`A1`/`A2` y `C-<n>` son el precedente de
   conservación).
3. **La regla es asimétrica respecto del momento.** Vale para la ventana pre-autorización. **Después
   del `pin` no se aplica**: allí no se re-deriva, se **detiene** (`.agents/policies/
   supervised-autonomous-execution.md:1.2`/`:1.4`). Aplicarla post-`pin` sería exactamente el
   «scope expansion autónoma» que `:1.4` prohíbe.

### 14.2 Las preguntas de §13 del encargo, respondidas

| Pregunta | Respuesta | Evidencia |
|---|---|---|
| ¿Cómo identificar las premisas? | Son las entradas enumeradas por el contrato de derivación; el Plan derivado las **cita** (PD-5, «cita sus fuentes; no las reescribe») | investigación previa §12.1, §12.4 `PD-5` |
| ¿Existe información suficiente hoy? | **No.** El contrato de derivación es `DESIGN_OPTION` y nada lo registra; `work_type` tiene 0 ocurrencias | investigación previa §1.3; §4.7 de este documento |
| ¿Qué campos son derivados de esas premisas? | Todos los marcados **Derivado**/**Confirmado** en §3.5, que son salida del derivador; el resto es `Declarado` | investigación previa §12.1 |
| ¿Qué ocurre si la dependencia no puede determinarse? | `R-6`: `GAP` + `NEEDS_CLARIFICATION` → aclaración con el formato existente; nunca asunción | §13.1 |
| ¿Requiere re-derivación completa o parcial? | **Depende de si el grafo de dependencias está declarado.** Si lo está, parcial (`D-1`); si no, completa | §10.1 |

`FACT` — La regla **no se implementa aquí** (restricción del encargo). Se describe, se evalúa y se
deja condicionada a `HD-INT-A`/`HD-INT-H`.

---

## 15. Impacto sobre

`FACT` — Ninguno de estos impactos se materializa en este trabajo. Se declaran como consecuencia
**del modelo recomendado**, sujeto a las decisiones humanas de §16.

| Objeto | Impacto | Estado |
|---|---|---|
| **Plan** | conserva identidad y status; el contenido puede cambiar antes de autorizar; su procedencia de derivación pasa a ser un dato que el artefacto debe poder citar | `DESIGN_OPTION` |
| **Note** | **mismo tratamiento**, por `HD-INT-D` (Working artifact) y `HD-INT-J` (Plan/Note es siempre el artefacto gobernable); su forma exacta depende de `HD-INT-D` | `GAP` mientras `HD-INT-D` esté abierta |
| **`work_type`** | es `Derivado` (`HD-INT-F`): modificarlo a mano es `R-4`; si el derivador lo usó como premisa, re-derivar; si no, es decisión humana con la restricción de que **un `work_type` modificado a mano que no coincida con el derivado deja de ser `Derivado`** | `HUMAN_DECISION_REQUIRED:HD-K2` |
| **scope** | `Declarado` **y** premisa; ampliación ⇒ `R-4`; lo posterior al `pin` sigue en `STOP_SCOPE_VIOLATION`; reducción sin cambio de obligaciones ⇒ `HD-K1` | §8, §16 |
| **applicable rules** | se **consultan**, no se reescriben; un cambio de scope puede introducir reglas (`R-4`) o exigir una decisión normativa (`R-5`) | `DESIGN_OPTION`; patrón `PC-75` |
| **authority** | no cambia: `CHANGE_SCOPE`/`APPROVE_PLAN` siguen `FORBIDDEN` para el host; lo posterior al `pin` sigue deteniendo | `IMPLEMENTED` (sin cambio) |
| **lifecycle** | **sin cambio**: ningún estado nuevo, ningún status nuevo (§9.1) | `FACT` |
| **SAE** | **sin cambio de lógica**. `MK-6`: el camino post-`pin` es el existente. El modelo recomendado sólo describe la ventana anterior, que SAE no ve | `FACT` |
| **validation** | el anchor valida el contenido **ya modificado**; no es ni debe ser un registro de procedencia de derivación | `FACT` |
| **checkpoint** | absorbe la modificación previa por construcción (`pin` en la primera autorización); sin cambio | `IMPLEMENTED` |
| **lineage** | es donde está el hueco real: no hay registro de procedencia de la derivación; `F-<n>`/`C-<n>`/`A1`-`A2` son el precedente de forma, no de derivación | `GAP` |

---

## 16. Human Decisions Required

`PC-1` — **HD-K no podía cerrarse desde esta investigación** (resuelta después por acto humano, 2026-10-05; ver §16.2). Su
núcleo conceptual sí queda respondido (§11, §12), pero dos de sus resultados dependen de decisiones
que no son suyas, y aparece una decisión nueva.

### 16.1 Lo que HD-K **sí** resuelve con la evidencia disponible

| # | Respuesta | Fundamento |
|---|---|---|
| 1 | Qué tipos de modificación existen | cuatro resultados: editorial, decisión humana, declaración añadida, cambio de premisa (§12, `R-1`…`R-4`) |
| 2 | Cuáles son puramente editoriales | proyección canónica idéntica (`_canonical_text`), con el límite declarado en §5.1 |
| 3 | Cuáles representan una decisión humana | las que tocan campos `Declarado`/`Confirmado` fuera de `premises(D)`, sin caer en `FI-1`…`FI-10` (`R-2`, `R-3`) |
| 4 | Cuáles invalidan la derivación | las que tocan `premises(D)` (`R-4`) |
| 5 | Cuándo corresponde re-derivar | `R-4`, en la ventana pre-autorización, por el agente, como propuesta |
| 6 | Qué sucede con Scope | `Declarado` + premisa: el humano lo modifica (no es violación ni autorización); si cambió una premisa, se re-deriva; post-`pin`, `STOP_SCOPE_VIOLATION` (§8) |
| 7 | Qué sucede con `work_type` | `Derivado`: modificarlo es `R-4`; el caso «declarado a mano» es `HD-K2` |
| 8 | Qué sucede con applicable rules | se consultan; un cambio de scope puede introducir reglas (`R-4`) o exigir decisión normativa (`R-5`) |
| 9 | Qué sucede con authority | sin cambio: `CHANGE_SCOPE`/`APPROVE_PLAN` siguen `FORBIDDEN`; `FI-3` detiene |
| 10 | Cómo queda preservada la trazabilidad | `D1` como procedencia, una categoría por campo, «modificar ≠ autorizar», `pin` en la autorización (§9.2, §9.3) |
| 11 | Qué sucede si la modificación no puede clasificarse | `R-6`: `GAP` + `NEEDS_CLARIFICATION` → aclaración con el formato existente; nunca asunción (§13.1) |
| 12 | Si B+C es suficiente | **No tal como está formulado.** Sí con dos correcciones: una categoría por campo (B) y `premises(D)` en lugar de «semántico» (C); más el complemento D-4 (§7.4, §10.4) |

### 16.2 Decisiones nuevas

| ID | Decisión | Por qué es humana | Impacto si no se decide | Dueño |
|---|---|---|---|---|
| **HD-K1** | Si una **reducción** de scope que no altera ninguna obligación resuelta puede aceptarse **sin** re-derivación | `FI-9` prohíbe leer una ausencia de regla como permiso; `DV-2` prohíbe declarar «sin señal bloqueante» a un resultado con dos lecturas. La respuesta segura (re-derivar) está disponible; declarar aceptable la reducción **es** una decisión | se re-deriva siempre ante cualquier cambio de scope, incluso reducciones inocuas: coste, sin riesgo | mantenedor |
| **HD-K2** | Si `work_type` es **declarable por el humano** o estrictamente derivado; y si un `work_type` modificado a mano conserva la categoría `Derivado` | `HD-INT-F` decidió que `work_type` **se deriva**; `HD-K` necesita saber si una modificación humana de ese campo es `R-2`/`R-3` (decisión) o `R-4` (cambio de premisa). La evidencia no permite decidirlo: un `work_type` a mano que **no** coincida con el derivado es, por definición, un campo derivado con valor no derivado | el campo queda con dos procedencias posibles y sin regla, que es exactamente la ambigüedad «sobre qué fue derivado» que el encargo prohíbe | mantenedor |
| **HD-K3** | Si el **registro de premisas** (`premises(D)`) es un dato obligatorio del Plan/Note derivado (materialización de `PD-5`) o basta citar fuentes en prosa | sin el registro, `R-6` (`GAP`) pasa de excepción a regla (§13.1). Materializarlo toca `docs/plans/_TEMPLATE.md` y `docs/CONVENTIONS.md` → depende de `HD-INT-H` | toda modificación humana queda con información faltante (`GAP`): el sistema tendrá que preguntar siempre, o asumir | mantenedor |
| **HD-K4** | Si la regla `MK-3` (premisa cambiada ⇒ derivación inválida) es **norma** o **lectura operacional** | es la pregunta de vía que `HD-INT-H` ya planteó para el modelo: ¿`CONVENTIONS.md` o RFC/ADR? `PC-75`/`ADR-16` reservan esa decisión | la regla queda como recomendación no exigible | mantenedor |

**Metadata `PC-1` de las cuatro** (`docs/CONVENTIONS.md:652-676`). Registrada al materializar el acto
humano del mantenedor (2026-10-02), que **no** las adoptó; **actualizada** por el acto humano explícito
del checkpoint Human Authority (2026-10-05), que **las adopta**:

| ID | blocking | owner | escalación | resolución | evidencia | efecto downstream | ADR-worthiness |
|---|---|---|---|---|---|---|---|
| `HD-K1` | no (resuelta) | mantenedor | mantenedor | **adoptada (2026-10-05)** — `R-4` incondicional; sin excepción «inocua» | acto humano explícito del checkpoint Human Authority (2026-10-05) | `DISENO §9.3`; `PLAN §8.2` | no determinado (`ADR-16 AU-6`; `HD-M3` pendiente) |
| `HD-K2` | no (resuelta) | mantenedor | mantenedor | **adoptada (2026-10-05)** — `work_type` derivado cuando determinable; si no, decisión humana; sin función de autoridad | acto humano explícito (2026-10-05) | `DISENO §11.5`/`§13.4`; `PLAN §5` | idem |
| `HD-K3` | no (resuelta) | mantenedor | mantenedor | **adoptada (2026-10-05)** — `premises(D)` obligatorias; premisa faltante ⇒ `GAP` | acto humano explícito (2026-10-05) | `DISENO §8`; `PLAN §8`, `D-2.4` | idem |
| `HD-K4` | no (resuelta) | mantenedor | mantenedor | **adoptada (2026-10-05)** — `MK-3` se eleva a `CONVENTIONS.md`; sin RFC/ADR nuevo | acto humano explícito (2026-10-05) | `DISENO §18`; `PLAN D-1` | idem |

`FACT` — La determinación de `blocking` **no** se toma aquí: `docs/CONVENTIONS.md:652-676` reserva esa
determinación al humano cuando la normativa la requiere.

### 16.3 Dependencias heredadas (no se resuelven aquí)

`FACT` — HD-K **no puede implementarse antes** de que se resuelvan:

| Dependencia | Por qué bloquea a HD-K |
|---|---|
| `HD-INT-A` (adoptar el modelo y su vía) | sin derivación no hay `D` cuya validez pueda invalidarse |
| `HD-INT-D` / `HD-INT-E` (forma y vía de autorización de la Note) | «cambia Plan ↔ Note» no es decidible sin el criterio de `HD-INT-E2` materializado (§9.4) |
| `HD-INT-H` (elevación normativa de la derivabilidad) | `MK-3` depende de dónde viva la norma |
| `HD-INT-F` (materialización de `work_type`) | `HD-K2` presupone el campo |

---

## 17. Recomendación

`DESIGN_OPTION` — Separada explícitamente de los hechos de §3–§5, y **no vinculante**.

### 17.1 Recomendación arquitectónica

> **Adoptar B+C con dos correcciones y un complemento, y no introducir ningún mecanismo nuevo.**
>
> 1. **La modificación humana de un `proposed` Plan/Note no es una anomalía, no es una violación y
>    no requiere autorización adicional: es el modo normal en que el humano forma la autorización.**
>    El repositorio ya la ejerce (Plan 136) y ya tiene el vocabulario para registrarla
>    (`Declarado`/`Confirmado`, `user_confirmed`).
> 2. **Una sola categoría por campo.** `Derived: X` + `Human: Y` sobre el mismo campo reintroduce la
>    ambigüedad que el encargo prohíbe. El campo pasa a `Declarado`/`Confirmado`, o no se toca.
> 3. **Reemplazar «semánticamente relevante» por «pertenece a `premises(D)`».** Es la única frontera
>    mecánica disponible que no exige interpretar prosa y que no necesita un scoring. Donde no puede
>    establecerse, el resultado es `GAP`, no una asunción.
> 4. **Conservar la derivación anterior como procedencia**, exactamente como `A1`/`A2` conservan las
>    validaciones y `C-<n>` conserva las correcciones. Nunca mutarla ni borrarla.
> 5. **Declarar explícitamente que modificar no es autorizar.** Es el riesgo principal de B y hoy
>    no está enunciado en esa dirección.
> 6. **No tocar SAE ni el checkpoint de autorización.** HD-K es la ventana anterior al `pin`; el
>    mecanismo existente ya resuelve la posterior, y su frontera temporal está declarada y testeada.
> 7. **No crear nada**: ni estado, ni entidad, ni versionado, ni primitive de identidad, ni clase de
>    autoridad, ni fuente normativa. El modelo recomendado es enteramente composición de mecanismos
>    existentes más un dato de procedencia cuya materialización es `HD-K3`.

### 17.2 Lo que la evidencia recomienda **no** hacer

| No hacer | Por qué |
|---|---|
| Introducir versionado de Planes | el repositorio no lo tiene y `docs/AGENTS.md:Identity` declara que la identidad no es path ni versión; sería una primitive nueva |
| Un checker que interprete si la modificación «cambió el significado» | `.agents/policies/validation-closure.md:5.1 Enforcement` declara que **ningún** checker interpreta prosa; la investigación previa §16 `A-22` descarta agregar uno |
| Un scoring de impacto semántico | prohibido por el encargo, y no hace falta: la comparación de conjuntos es booleana |
| Prohibir la edición humana del `proposed` | un `proposed` no autorizado es texto; prohibirlo no protege nada y contradice `AU-5` |
| Extender la proyección del checkpoint para cubrir la ventana pre-`pin` | el checkpoint responde «¿la declaración cambió desde que autorizó?»; antes de autorizar no hay nada que comparar, y `authorization_drift(None, …)` lo declara correctamente |
| Usar `C-<n>` para registrar la modificación | es el registro de la corrección de un finding sobre contenido ejecutado, no de la formación de una propuesta |

### 17.3 Condición de suficiencia de la recomendación

`DESIGN_OPTION` — La recomendación queda **condicionada**: (a) `HD-INT-A`/`HD-INT-H` deciden si el modelo de
derivación es norma; (b) `HD-K3` decide si `premises(D)` se materializa; (c) `HD-K1`/`HD-K2` cierran
los dos huecos que la evidencia no permite resolver. Sin (b) y (c), el modelo es correcto pero
`R-6` (`GAP`) será el resultado frecuente en lugar del excepcional.

---

## Registro de verificación y no-modificación

`FACT` — Este trabajo:

- **creó** `docs/working/research/INVESTIGACION_MODIFICACION_HUMANA_DERIVACION_2026-09-23.md`;
- **agregó una fila** a `docs/working/research/INDEX.md` (registro/navegación de su propia familia);
- **no modificó** runtime, `protocol/.agents/`, policies, RFCs, ADRs, planes históricos,
  `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`, `docs/AGENTS.md`,
  lifecycle, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `ROADMAP.md`, `CHANGELOG.md`, `VERSION`,
  tests, tools, CI ni `dist`;
- **no creó** Plan, RFC, ADR, registry, entidad, state machine, clase de autoridad, primitive de
  identidad ni fuente normativa;
- **no clasificó retroactivamente** ningún artefacto del corpus;
- **no resolvió** ninguna decisión humana: `HD-K1`…`HD-K4` quedan abiertas, y `HD-INT-A`/`HD-INT-D`/`HD-INT-E`/
  `HD-INT-F`/`HD-INT-H` se consumen como premisas sin reabrirlas;
- **no ejecutó** commit, push, tag, merge ni release.

`FACT` — Verificación ejecutada durante este trabajo, **read-only** y sin dejar residuo en el
repositorio: `python -m pytest tests/test_repo_containment.py tests/test_check_plan_citations.py -q`
→ `53 passed`. Sustenta §4.8. No se corrió la batería canónica completa: este Change no modifica
código, tooling, tests ni gobernanza, y el encargo prohíbe modificar la batería.

`FACT` — La única operación de escritura fuera de este archivo fue la fila de registro en el INDEX
de su familia, requerida para que el artefacto sea localizable
(`docs/AGENTS.md:Glosario y semántica de archivos AGENTS / INDEX / ENTRYPOINT`: los INDEX de
`docs/working/` son registros livianos de navegación/status).
