# Diseño integral — Change único: Intent → Derivation → Plan/Note → Autorización → SAE

**Clase documental:** Working / Proposal (provenance) — **no normativo**
(`docs/AGENTS.md:Folder → class map`; `docs/placement-contract.md:6. Namespace selection`,
familia `Working analysis` → `docs/working/{audits,research,proposals}/`).
**Naturaleza:** diseño y planificación `READ_ONLY` respecto del sistema. **Autoridad de este
documento: ninguna.** No crea mecanismos, no modifica arquitectura, no autoriza trabajo y no
resuelve ninguna decisión normativa.
**Fecha:** 2026-09-23
**Baseline:** `dev` @ `820da21` (`docs(roadmap): declare the capability and autonomy roadmap A-B-C (plan 149)`);
`protocol/.agents/VERSION` = `11.6.2`.
**Fuentes principales (usadas como base, no sustituidas por conocimiento genérico):**
`docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md` (en adelante «I-22»),
`docs/working/research/INVESTIGACION_MODELO_INTENCION_DERIVACION_GOBERNANZA_Y_CONOCIMIENTO_2026-09-23.md` («I-23»),
`docs/working/research/INVESTIGACION_MODIFICACION_HUMANA_DERIVACION_2026-09-23.md` («I-23-HDK»).
**Alcance de escritura:** este trabajo escribe **un documento nuevo** (este archivo) y **una fila de
registro** en `docs/working/proposals/INDEX.md` (registro/navegación de su propia familia). No
modifica código, runtime, tests, Protocol, policies, RFCs, ADRs, planes históricos, `ROADMAP.md`,
`CHANGELOG.md`, `VERSION`, Placement Contract, `dist`, INDEX de gobernanza ni CI; no archiva, mueve
ni reorganiza nada; no crea commits, tags, releases ni push; no crea Plan, RFC, ADR, registry,
entidad, state machine, clase de autoridad, primitive de identidad, namespace ni fuente normativa.
**Objetivo:** entregar **un único Plan integral** que un Change posterior pueda ejecutar sin volver a
resolver las decisiones arquitectónicas fundamentales.

---

## Leyenda de clasificación (obligatoria)

| Etiqueta | Significado |
|---|---|
| `FACT` | Hecho verificado por lectura directa o conteo mecánico reproducible; no expresa intención ni norma. |
| `IMPLEMENTED` | El mecanismo existe y **lo realiza un ejecutor** verificado en el artefacto que lo ejecuta. |
| `PARTIALLY_IMPLEMENTED` | Existe una parte mecánica y otra que depende de prosa, juicio o disciplina humana; la frontera está identificada. |
| `DOCUMENTED_ONLY` | Existe como texto normativo, política o instrucción; **ningún ejecutor lo verifica**. |
| `GAP` | Ausencia de mecanismo, representación o información. |
| `CONTRADICTION` | Dos fuentes —o una fuente y el estado real— afirman cosas incompatibles. |
| `HYPOTHESIS` | Afirmación evaluada aquí, con el veredicto que la evidencia permite. |
| `DESIGN_OPTION` | Alternativa evaluada; **no** es recomendación aceptada ni regla. |
| `BOUNDARY` | Ambigüedad estructural: frontera declarada del modelo, no un defecto. |

Regla de honestidad aplicada: **una hipótesis no se convierte en decisión, y una recomendación no se
convierte en regla**. Donde la evidencia no alcanza se declara `GAP`/`UNDETERMINED`/`PC-1`
y se detiene el diseño en ese punto. Las citas usan `ruta:sección`; no se usan números de línea sobre
archivos mutables.

---

## 1. Executive Summary

`FACT` — ARgentOS ya posee las **cinco** piezas que el modelo necesita, y las posee en grado poco
común; lo que no posee es **el tramo que las conecta**. La mitad derecha de la cadena
(`autorización → SAE → verificación → cierre`) está implementada y endurecida por incidentes reales
(`<PLAN-136>:F-3`, plan 138, plan 139). La mitad izquierda (`intención → contexto → derivación →
Plan/Note propuesto`) **no existe en ninguna capa**: el host DEV no tiene punto de entrada
«intención» y su derivación arranca en el Plan (`runtime/orchestrator/derivation.py:derive_next_action (regla 1)`
empieza en `STOP_PLAN_NOT_FOUND`, y `runtime/orchestrator/observation.py:observe(root, plan, store)`
se construye **desde un número de plan**).

`FACT` — Por eso una intención breve como `Implementá X` **hoy no puede producir nada legítimo**, y no
por falta de ejecutor: el intake exige un Plan que ningún mecanismo deriva
(`.agents/workflows/change-lifecycle.md:2. Authorization gate`; `docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`).

`DESIGN_OPTION` — **Este diseño no crea una arquitectura paralela.** Define el tramo faltante como
**composición de mecanismos existentes** más **un único módulo de derivación puro**, y lo entrega como
**un solo Plan integral**. Las cuatro decisiones de arquitectura que lo sostienen son:

1. **La derivación es una función pura más, hermana de la que ya existe.** Se añade
   `runtime/orchestrator/intent.py` con `derive_change_candidate(...)`, con el mismo contrato que
   `runtime/orchestrator/derivation.py:derive_next_action`: función pura de la observación, sin
   estado, sin `next_state`, sin cursor, sin store nuevo. La asimetría se mantiene: la derivación
   **propone** un objeto no autorizado; **no** autoriza (M-1 de I-23 §5.1).
2. **`premises(D)` no es una entidad: es un registro de procedencia**, exactamente como `A1`/`A2`
   conservan validaciones y `C-<n>` conserva correcciones (I-23-HDK §9.2). Se materializa como una
   **sección nueva del template de Plan**, con una fila por clase de premisa y su evidencia citada.
3. **La frontera editorial/semántica no se inventa:** se reutiliza el criterio ya implementado
   `runtime/orchestrator/autonomy.py:_canonical_text` (proyección canónica idéntica), y el criterio de
   invalidación pasa de «semánticamente relevante» —que el repositorio **prohíbe** mecanizar
   (`.agents/policies/validation-closure.md:5.1 Enforcement`: «No checker interprets prose»)— a
   **pertenencia a `premises(D)`**, como exige I-23-HDK §7.3/§17.1.
4. **El resultado de una modificación humana tiene cinco salidas, no cuatro**, porque la propia
   investigación de HD-K dejó dos abiertas y la evidencia las resuelve de forma distinta: `R-1`
   editorial, `R-2` declaración sobre campo no-premisa, `R-3` declaración **añadida** que no era
   premisa (el complemento `D-4` obligatorio por el encargo), `R-4` cambio de premisa, y `R-5`
   **no decidible** (`premises(D)` no establecible → `UNDETERMINED / MISSING`). El encargo pide «no
   inventar nuevos resultados si los cuatro existentes cubren el modelo»; la evidencia demuestra que
   `R-3` y `R-5` **no son el mismo caso** que `R-2` y `R-4` (I-23-HDK §10.4 y §13.1), y por eso se
   declaran como los resultados que la investigación ya había nombrado por separado.

`FACT` — **Hallazgo del dogfood que cambia la forma del Change (§21).** El target dogfood
`Implementá Effect Admission para SAE` **no es derivable hoy a Plan completo**, y eso no es un defecto:
la resolución de contexto encuentra un **`GAP` localizado y una divergencia**, **no** un conflicto entre
fuentes vigentes (Fase 1, F5): el payload define la admisión por **efectos declarados**
(`protocol/.agents/standards/runtime/AUTHORIZATION.md:Effects block`: todo efecto fuera de frontera
exige entrada `[[effects]]` con `authorized_by` y `status`) y **no tiene ejecutor en el host DEV**
(`.agents/policies/supervised-autonomous-execution.md:1.3`: la admisión se hace por **paths de
escritura** y clases de acción, y `## Effects` no se consume). El payload **no es regla de DEV**
(`AGENTS.md`; `.agents/AGENTS.md`: «product data, not instructions»), de modo que no hay dos normas en
alcance que se contradigan: hay una norma del payload **sin realización** en DEV, una divergencia entre
implementación y fuente que se **escala y no se reconcilia** (`PC-75`; `RQ-5`) y una **decisión humana
reservada** sobre el dominio y la vía del cambio (`FI-3`). El veredicto correcto es **`NOT_DERIVABLE`**
con la reserva nombrada → escalar, **no elegir**. El dogfood se diseña por tanto en **dos
ejecuciones**: la primera **se detiene y pregunta** citando las dos fuentes y el punto exacto de
divergencia; la segunda parte de la decisión humana de alcance y **deriva el Plan completo**. Es el
experimento más fuerte del Change, porque falsifica a la vez la capacidad de derivar y la capacidad de
**no asumir**.

`DESIGN_OPTION` — **Recomendación final:** ejecutar **un único Change integral** (§22–§23), Clase A de
RFC-56 **si y sólo si** el alcance incluye `protocol/.agents/` (el dogfood demuestra que el punto de
admisión puede resolverse dentro de DEV, en cuyo caso el Change es Clase B/DEV y **no toca el payload**),
con **cinco invariantes nuevos en `docs/CONVENTIONS.md`** (§18) y **nueve decisiones humanas pendientes,
ninguna bloqueante para el diseño** (`HD-INT-G`, `HD-M2`, `HD-M3`, `HD-M4`, `HD-M5` en §25; `HD-K1`…`HD-K4`
en `HDK §16.2`), de las cuales `HD-M2` bloquea la **ejecución 2** del dogfood.

---

## 2. Current State

### 2.1 Medición mecánica del baseline (reproducible)

`FACT` — Conteos obtenidos en este trabajo sobre el baseline `820da21`:

| Dato | Valor | Operación |
|---|---|---|
| Planes numerados en `docs/plans/` | **153** | `Get-ChildItem docs/plans -File \| ? Name -match '^\d+.*\.md$'` |
| RFCs numeradas en `docs/rfc/` | **80** | ídem |
| ADRs numerados en `docs/adr/` | **18** | ídem |
| Ocurrencias de `work_type`/`work-type`/`tipo de trabajo` en gobernanza, código y tests | **0** | `Select-String` sobre `docs/{CONVENTIONS,VERSIONING,AGENTS,placement-contract}.md`, `docs/rfc/*.md`, `docs/adr/*.md`, `runtime/**/*.py`, `tools/*.py`, `tests/*.py`, `.agents/**/*.md` |
| Headers con campo de vigencia (`**Lifecycle:**`/`**Vigencia:**`) | **0** | `Select-String` sobre `docs/plans/*.md`, `docs/rfc/*.md`, `docs/adr/*.md` |
| Módulo de *intent* en `runtime/` | **ninguno** | `Get-ChildItem runtime -Recurse -Filter '*intent*'` |
| Module de derivación de cierre | existe | `runtime/orchestrator/derivation.py` |

`FACT` — La tabla de estado real de los 15 mecanismos de RFC-75 y de los tres ejes de granularidad
está medida en I-23 §1.3/§3.3 y en I-22 §3.3–§3.5. Este diseño **no la repite**: la usa.

### 2.2 Qué existen realmente los mecanismos relevantes (clasificados)

| Mecanismo | Artefacto real | Estado | Evidencia |
|---|---|---|---|
| Gate de autorización binario | `runtime/orchestrator/derivation.py:derive_next_action (regla 1)` | `IMPLEMENTED` | `STOP_PLAN_NOT_FOUND` → `STOP_AWAIT_PLAN_AUTHORIZATION` → `STOP_PLAN_SUPERSEDED` |
| Vocabulario cerrado de acciones y stops | `runtime/orchestrator/contracts.py:DERIVED_ACTIONS`, `STOP_ACTIONS`, `HUMAN_AUTHORITY_STOPS` | `IMPLEMENTED` | 21 stops; 8 acciones ejecutables/registrables |
| Frontera de autoridad (3 veredictos) | `runtime/orchestrator/authority.py:AuthorityBoundary.evaluate` | `IMPLEMENTED` | `AUTHORIZED_EXISTING`/`REQUIRES_HUMAN`/`FORBIDDEN`; `FORBIDDEN_ACTIONS` incluye `APPROVE_PLAN`, `CHANGE_SCOPE`, `MODIFY_CLOSED_ARTIFACT`, `RELEASE`, `TAG`, `PROMOTE` |
| Clases de acción autónomas vs escalación | `runtime/orchestrator/autonomy.py:AUTONOMOUS_ACTION_CLASSES`, `ESCALATION_ACTION_CLASSES` | `IMPLEMENTED` | 10 autónomas, 13 de escalación, cada una con `_ESCALATION_STOP` y `_ESCALATION_AUTHORITY` |
| Proyección de autorización + no retroactividad | `runtime/orchestrator/autonomy.py:authorization_projection`, `authorization_drift`; `runtime/orchestrator/host.py:_apply_autonomy_gate`, `_pinned_autonomy_projection` | `IMPLEMENTED` | el `pin` se toma en la **primera** iteración autorizada y se compara después; `pinned is None` se reporta como «no fijado aún» |
| Distinción representación/significado | `runtime/orchestrator/autonomy.py:_canonical_text` | `IMPLEMENTED` | normaliza *runs* de espacios; test dedicado `tests/test_sae_scope_enforcement.py` |
| Envelope de autonomía desde declaraciones del Plan | `runtime/orchestrator/autonomy.py:AutonomyEnvelope`, `envelope_from_observation` | `IMPLEMENTED` | se lee de `## Delegación agentiva`; ausencia = «no autonomía» |
| Verificación de scope all-or-nothing | `runtime/orchestrator/autonomy.py:verify_write_targets`; `host.py:_autonomy_targets`, `_plan_authorized_scope` | `IMPLEMENTED` | un target no autorizado detiene la acción completa; un set irresoluble detiene |
| Observación read-only y libre de inferencia | `runtime/orchestrator/observation.py:observe`, `ChangeObservation` | `IMPLEMENTED` | 30+ campos; `gaps`, `anchor_stale`, `scope_identity_unknown`; ausencia reportada como `GAP` |
| Condiciones derivadas | `runtime/orchestrator/derivation.py:CLOSED_DERIVED`; `runtime/orchestrator/contracts.py:DERIVED_CONDITIONS` | `IMPLEMENTED` | `Verified`/`Executed`/`Committed`/`Closed`/`Promoted`/`Released` |
| Anchors / checkpoints / lineage | `tools/check_lifecycle_anchor.py` (C-1), `check_lifecycle_checkpoint.py` (C-2), `check_lifecycle_lineage.py` (C-3); `runtime/orchestrator/governance.py` | `IMPLEMENTED` | advisory, DEV-only, fuera de la batería; `EXCLUDED` para legacy |
| Realización mecánica de una norma + guarda de divergencia | `runtime/placement/rules.py` + `resolver.py` + `tests/test_placement_contract_drift.py` | `IMPLEMENTED` | el **patrón** que este diseño reutiliza para reglas aplicables |
| Modelo de incertidumbre | `runtime/orchestrator/contracts.py:SIGNALS` (`VALID`/`GAP`/`ANOMALY`/`FAIL`/`BOUNDARY`/`N/A`/`EXCLUDED`) | `IMPLEMENTED` | `.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP` |
| Ciclo de status de Plan | `docs/CONVENTIONS.md:Convenciones` (planes); `docs/plans/_TEMPLATE.md` | `IMPLEMENTED` | `Aprobado para redacción` → `Aprobado para ejecución` → `Executed` → `Superseded` |
| Determinaciones de cierre | `docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de cierre…`; `.agents/policies/validation-closure.md:5.1/5.2` | `IMPLEMENTED` (prosa + stop condition) | `REQUIRED`/`NOT_REQUIRED`/`DEFERRED`; **ningún código las parsea** |
| Matriz de governance por tipo de Plan | `docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle` | `DOCUMENTED_ONLY` | grep de sus valores en `tools/` y `runtime/`: 0 coincidencias (I-23 §10.6) |
| `INTENT_CONFIDENCE` | `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md` | `DOCUMENTED_ONLY` (Protocol) | score sobre el texto del prompt; `Implementá X` → máx. 4 → `MEDIUM` → confirmación |
| Derivación de intención | — | **`GAP`** | no existe en ninguna capa (I-23 §4.1) |
| `work_type` | — | **`GAP`** | 0 ocurrencias (§2.1) |
| Resolución de reglas aplicables | `.agents/policies/authority.md:Document discovery` (tabla de enrutamiento en prosa) | `PARTIALLY_IMPLEMENTED` | es enrutamiento por **necesidad**, no por **trabajo** |
| Vigencia materializada | `docs/AGENTS.md:Lifecycle` (vocabulario) | `DOCUMENTED_ONLY` | 0 artefactos declaran un valor ≠ `active` |

`CONTRADICTION` — **Dos contradicciones reales, las dos ya registradas por la gobernanza, ninguna
introducida por este diseño:**

- **T-1 (`Superseded` sin sustituto):** `docs/VERSIONING.md:7. Estados de planes y RFCs` y
  `docs/CONVENTIONS.md:Convenciones` exigen indicar el reemplazante, mientras
  `docs/rfc/75-change-lifecycle.md:Modelo de lifecycle` ya nombra `Abandoned = Plan Superseded con
  motivo`. **Resuelto por decisión humana en este encargo** (§3, `HD-INT-B`): `Superseded` puede llevar
  replacement **o** reason.
- **T-2 (el intake tiene una rama «sin Plan» declarada y sin forma):** `docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`
  nombra «RFC, Plan, **Nota** o mensaje de commit»; `docs/plans/94-change-lifecycle-master-action-plan.md:9.2`
  escribe «Plan/**Nota**» para L1; `docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación`
  la nombra para cambios sin Plan. Y **no existe ningún archivo de Nota en el repositorio**. Esta
  contradicción **sí** toca este diseño y se resuelve en §10/§14 con una decisión humana bloqueante.

---

## 3. Target Model

### 3.1 La cadena objetivo, etapa por etapa, con dueño y estado

`DESIGN_OPTION` — Cadena pedida por el encargo, mapeada a piezas reales:

```text
[humano]  Intent                     ── texto del pedido; se registra en el primer artifact del Change
   ↓
[agente]  Context                    ── resolución contra el repositorio (§6, §12)
   ↓
[agente]  Intent Confidence          ── INTENT_CONFIDENCE sobre el TEXTO (§7.2); no se redefine
   ↓
[agente]  Derivability               ── sin señal bloqueante | GAP · ANOMALY/BOUNDARY | REQUIRES_HUMAN (§7)
   ↓
[agente]  Work Type                  ── mechanism | documentary | mechanical (§11)
   ↓
[agente]  Applicable Rules           ── APPLIES | NOT_APPLICABLE | UNDETERMINED | CONFLICT (§12)
   ↓
[agente]  Plan/Note proposed         ── Status: Aprobado para redacción; con premises(D) (§8, §13)
   ↓
[humano]  Human modification?        ── R-1…R-5 (§9); re-derivación si corresponde (§8.5)
   ↓
[humano]  Authorization              ── Status: Aprobado para ejecución (acto humano exclusivo, §14)
   ↓
[SAE]     Execution                  ── pin de la proyección de autorización; frontera intacta (§16)
```

| Etapa | Entrada | Salida | Dueño | Estado |
|---|---|---|---|---|
| Intake de intención | texto humano | intención normalizada, registrada en el primer artifact | humano → registro | `PARTIALLY_IMPLEMENTED` (el registro existe; la normalización no) |
| Contexto | intención + repositorio | conjunto de fuentes candidatas **con cita y con lifecycle** | agente (lectura) | `GAP` como resolución por trabajo |
| `INTENT_CONFIDENCE` | el texto | `HIGH`/`MEDIUM`/`LOW` + criterios aplicados | agente | `DOCUMENTED_ONLY` (Protocol); se **consume**, no se redefine |
| Derivabilidad | intención + contexto | condición, su señal y su evidencia | agente | **`GAP` → este diseño lo define** |
| `work_type` | rutas afectadas + naturaleza | `mechanism`/`documentary`/`mechanical` | agente | **`GAP` → este diseño lo define** |
| Reglas aplicables | sujeto del trabajo | 4 veredictos con cita | agente | **`GAP` → este diseño lo define** |
| Plan/Note propuesto | las seis entradas | artefacto `Aprobado para redacción` | agente (crea), humano (autoriza) | `PARTIALLY_IMPLEMENTED` (el objeto existe; su construcción por derivación no) |
| Modificación humana | el `proposed` + el acto | `R-1`…`R-5` | humano | **`GAP` por diseño; el precedente está en `_canonical_text`** |
| Autorización | `proposed` | `Aprobado para ejecución` | **humano exclusivo** | `IMPLEMENTED` |
| Ejecución | Plan autorizado | condiciones derivadas | SAE | `IMPLEMENTED` |

### 3.2 Estado de autoridad de las decisiones humanas (`HD-INT-*`, `HD-K*`)

`PC-1` — **Registro del estado de autoridad** (Fase 4). Las **nueve** decisiones
`HD-INT-A`, `HD-INT-B`, `HD-INT-C`, `HD-INT-D`, `HD-INT-E`, `HD-INT-F`, `HD-INT-H`, `HD-INT-I` y
`HD-INT-J` están **adoptadas por un acto humano explícito del mantenedor** (2026-10-02), cuya evidencia
es la instrucción de Fase 4 y cuyo **registro canónico** vive en el artefacto dueño:
`INVESTIGACION_MODELO_INTENCIA_DERIVACION_GOBERNANZA_Y_CONOCIMIENTO_2026-09-23.md §17.1` (I-23), con la
metadata de `PC-1` (decisión + evidencia + artifacts afectados). Las adoptadas **no se reabren**.

`FACT` — Estado de las catorce según ese acto: **nueve adoptadas**; `HD-INT-E2` es **consecuencia
derivada de `HD-INT-E`** y **no** una decisión humana independiente (sin autoridad propia); y `HD-K1`,
`HD-K2`, `HD-K3` y `HD-K4` **permanecen pendientes** — el acto **no** las adopta y no se infieren de la
adopción del núcleo `HD-INT-*`. Su registro y su metadata viven en su artefacto dueño
(`INVESTIGACION_MODIFICACION_HUMANA_DERIVACION_2026-09-23.md §16.4`, HDK).

| ID | Decisión | Consecuencia en este diseño | Fecha | Autoridad / origen | Evidencia / consumidores |
|---|---|---|---|---|---|
| `HD-INT-A` | Adoptar `Intent → Context → Derivation → Plan/Note → Human authorization → Execution` | el tramo izquierdo es el objeto del Change (§22) | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`); consumida por §22 y Plan §9.1 |
| `HD-INT-B` | `Superseded` puede representar sustitución **o** retiro con motivo; **sin** nuevo lifecycle state; `Abandoned` queda como **condición derivada** | §15.3: el campo es `Motivo de retiro`, obligatorio **sólo** cuando no hay sucesor; `Abandoned ⇔ superseded ∧ sin sucesor ∧ motivo` | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`); §15.3, Plan §21.2 |
| `HD-INT-C` | migración progresiva; **no** migración masiva del corpus | §15.4: default `active` por ausencia; cláusula legacy (RFC-75 Mecanismo 15) | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`); §15.4, Plan §9.1 |
| `HD-INT-D` | `Note` = **Working documental, dentro de la familia `Plan`**; **no** crear familia/namespace nuevo | §10/§14: la Nota vive dentro de la familia `Plan` ya declarada (`docs/placement-contract.md:6`) — **Opción A** | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`), que resuelve la opción A; §11.1/§14.3, Plan §10.3/§21.3 |
| `HD-INT-E` | la autorización puede producirse mediante una `Note`; no toda autorización requiere Plan | §14.2: dos formas de autorización, **una sola** autoridad | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`); §14.2, Plan §10.3 |
| `HD-INT-E2` | **Consecuencia derivada de `HD-INT-E`** (no decisión humana independiente): Plan vs Note se deriva por criterios, **no** por Change Level | §10: matriz de criterios binarios, sin mapeo a Level | — | derivada de `HD-INT-E` — **sin autoridad humana propia** | validez dependiente de la premisa `HD-INT-E`; §10, Plan §21.3 |
| `HD-INT-F` | `work_type` se deriva; no se convierte automáticamente en decisión humana | §11.5: derivado con campo sólo donde cambia una decisión | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`); §11.5, Plan §5 |
| `HD-INT-H` | los invariantes necesarios se elevan a `docs/CONVENTIONS.md` | §18: cinco invariantes, sin RFC/ADR nuevo | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`); §18, Plan §9.3 |
| `HD-INT-I` | la información de lifecycle en `INDEX` se deriva automáticamente | §15.5: el INDEX es espejo; no hay segundo estado manual | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`); §15.5, Plan D-6.5 |
| `HD-INT-J` | el Plan/Note **es** el artefacto gobernable; `proposed` es una situación pre-autorización, sin nueva máquina de estados | §13.5/§14.1: `proposed` = el estado existente `Aprobado para redacción` | 2026-10-02 | mantenedor (acto explícito) | acto del mantenedor (`I-23 §17.1`); §13.5/§14.1, Plan §1 |
| `HD-K1` | toda modificación de Scope —expansión **o reducción**— requiere re-derivación en el MVP | §9.3: **ninguna excepción**; `R-4` incondicional ante cambio de `Scope` | — | **PENDIENTE** — el acto del 2026-10-02 **no** la adopta | registro y metadata: `HDK §16.4` (artefacto dueño); §9.3, Plan §8.2 |
| `HD-K2` | `work_type` derivado; si `UNDETERMINED`, el humano puede establecerlo; **no** dos valores simultáneos bajo categorías distintas | §11.5 + §13.4: una sola categoría por campo | — | **PENDIENTE** — el acto del 2026-10-02 **no** la adopta | registro y metadata: `HDK §16.4`; §11.5/§13.4, Plan §5 |
| `HD-K3` | `premises(D)` **obligatorio** para una derivación completa; si no puede establecerse → `UNDETERMINED` | §8: sección obligatoria del artefacto; `R-5` cuando falta | — | **PENDIENTE** — el acto del 2026-10-02 **no** la adopta | registro y metadata: `HDK §16.4`; §8, Plan §8 |
| `HD-K4` | los invariantes de HD-K se elevan a `CONVENTIONS.md`; sin RFC/ADR nuevo | §18 | — | **PENDIENTE** — el acto del 2026-10-02 **no** la adopta | registro y metadata: `HDK §16.4`; §18, Plan D-1 |

`FACT` — **Ninguna** de estas decisiones reabre `C-2`/`CI`, Plan 121 ni R4; ninguna introduce una
segunda fuente normativa.

### 3.3 La regla de frontera que no se mueve

`FACT` — (`AGENTS.md:Task lifecycle`; `.agents/policies/supervised-autonomous-execution.md:1. The three separations`):

```text
autonomy ⊆ authorized scope  ∧  autonomy ⊆ granted authority
derived(Plan/Note)  ⇏  authorized(Plan/Note)
```

`DESIGN_OPTION` — Este diseño mueve **una sola** cosa: **quién construye** el objeto que se autoriza.
No mueve la frontera, no agrega autoridad y no relaja ningún stop condition existente.

---

## 4. Existing Mechanisms Reused

`DESIGN_OPTION` — Principio aplicado: **antes de proponer cualquier componente nuevo, se buscó
exhaustivamente qué mecanismo existente puede reutilizarse.** El resultado, componente por componente:

| Componente del modelo | Mecanismo existente reutilizado | Cómo se reutiliza | ¿Nuevo? |
|---|---|---|---|
| Intención | el **primer artifact del Change** (`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`) | la intención se registra ahí; **no** se crea entidad `Intent` | no |
| Registro de la clasificación | `**Change Level:**` + campos del header (`docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación`) | se añade `**Work type:**` en el mismo header, mismo patrón | campo nuevo, mecanismo existente |
| Confianza de intención | `INTENT_CONFIDENCE` (Protocol, leído como data) | se **consume** su vocabulario `HIGH`/`MEDIUM`/`LOW`; no se redefine ni se extiende | no |
| Derivabilidad | vocabulario de señales `VALID`/`GAP`/`ANOMALY`/`FAIL`/`BOUNDARY`/`N/A`/`EXCLUDED` (`runtime/orchestrator/contracts.py:SIGNALS`) + `NEEDS_CLARIFICATION` + protocolo de conflicto | el veredicto **se mapea** a esos vocabularios; no crea taxonomía de incertidumbre | mapeo, no taxonomía |
| Función de derivación | `runtime/orchestrator/derivation.py:derive_next_action` (función pura de la observación) | `runtime/orchestrator/intent.py:derive_change_candidate` con **el mismo contrato** | módulo nuevo, mismo patrón |
| Observación | `runtime/orchestrator/observation.py:observe` + `ChangeObservation` | la derivación de intención **también** es función pura de una observación; se extiende el dataclass | extensión aditiva |
| Resolución de reglas | patrón `docs/placement-contract.md:22. Enforcement` + `runtime/placement/rules.py` + `resolver.py` + `tests/test_placement_contract_drift.py` | **enrutamiento + cita + guarda de divergencia + escalación**; nunca precedencia inventada | realización nueva del patrón, sin registry |
| Ubicación de artefactos | `docs/placement-contract.md` + `runtime/placement/resolver.py` | el artefacto propuesto se ubica con el resolutor existente; si `STOP`, el diseño se detiene | no |
| `premises(D)` | `A1`/`A2` (anchors) y `C-<n>` (correcciones): registros de procedencia con identidad propia, que **nunca mutan su predecesor** | mismo patrón: `D1` se conserva, `D2` se añade por referencia | sección nueva del template, sin primitive de identidad |
| Criterio editorial | `runtime/orchestrator/autonomy.py:_canonical_text` | proyección canónica idéntica ⇒ nada que re-derivar | no |
| Invalidación por cambio de premisa | `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors…` (CL-2: `anchor changed ≠ semantic validity changed`) + `runtime/orchestrator/observation.py:anchor_stale` | mismo patrón: «cambió la premisa ≠ se borra la derivación»; se conserva como procedencia | no |
| Detección de divergencia de autorización | `runtime/orchestrator/autonomy.py:authorization_drift` + `host.py:_pinned_autonomy_projection` | **intacto**; el modelo nuevo opera **antes** del `pin` | no |
| Autorización | `**Status:** Aprobado para ejecución` + `STOP_AWAIT_PLAN_AUTHORIZATION` + `FORBIDDEN_ACTIONS` (`APPROVE_PLAN`, `CHANGE_SCOPE`) | **sin cambio**; se le da al gate existente un objeto derivado que autorizar | no |
| Frontera SAE | `.agents/policies/supervised-autonomous-execution.md` §1–§3; `runtime/orchestrator/autonomy.py:evaluate_autonomy` | **intacto** | no |
| Stops | `STOP_ACTIONS` (21 valores) + `HUMAN_AUTHORITY_STOPS` | los stops nuevos **reutilizan** el vocabulario existente; sólo se agrega el mapeo acción→stop | mínimo |
| Determinaciones de cierre | `docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de cierre…` (plan 133) | sin cambio; el Change las usa | no |
| Doc/roadmap impact | `.agents/policies/validation-closure.md:5.1/5.2` | sin cambio | no |
| Lifecycle del corpus | `docs/AGENTS.md:Lifecycle` (vocabulario) + `docs/AGENTS.md:Folder → class map` (vigencia por carpeta) | se materializa **por artefacto**; el vocabulario ya existe y no se reemplaza | campo nuevo, vocabulario existente |
| Legacy | `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy` | default `active` por ausencia ⇒ **0 ediciones** al corpus histórico | no |
| Guarda de forma | `tools/check_plan_structure.py` + los tres gates C-1/C-2/C-3 con `EXCLUDED` | se extiende el **patrón**, no se crea un gate nuevo de mayor jerarquía | extensión |
| Registro/espejo | `docs/plans/INDEX.md` (DESCRIPTIVE, `AU-4`) | la columna de vigencia es **vista derivada**; nunca autoridad | columna, no fuente |
| Nota | la familia `Plan` ya declarada en `docs/placement-contract.md:6` | `**Tipo:** Nota` dentro de la familia existente ⇒ **sin namespace nuevo** (`PC-10`/`PC-20` intactos) | forma nueva, familia existente |

`FACT` — **Nada de lo reutilizado se modifica en su semántica.** Lo único que cambia en artefactos
existentes es **aditivo**: secciones y campos nuevos en el template, un módulo nuevo en `runtime/`, un
mapeo nuevo en `contracts.py`, subsecciones nuevas en `CONVENTIONS.md`, y una columna nueva en los
INDEX de gobernanza. Ningún invariante existente se reescribe.

### 4.1 Lo que **no** se crea (evaluado y descartado con evidencia)

`DESIGN_OPTION` — Inventario explícito, exigido por el encargo:

| Candidato | Veredicto | Evidencia que lo descarta |
|---|---|---|
| Entidad `WorkUnit` / `Feature` | **no** | `docs/architecture-capability-review.md:4.1`; sería una segunda representación (I-23 §16 `A-2`) |
| Nueva entidad `Change` / tracker | **no** | `.agents/workflows/change-lifecycle.md:1` declara que su ausencia es una decisión |
| Registry (de reglas, de planes, de derivaciones, de Notas) | **no** | `docs/placement-contract.md:22. Enforcement` (`PC-75`); `.agents/AGENTS.md:Fundamental operating rules 8` |
| Nueva state machine | **no** | rechazada dos veces: `docs/rfc/75-change-lifecycle.md:No-objetivos`; `docs/adr/15-change-lifecycle-continuity.md:Alternativas consideradas` |
| Nueva authority class | **no** | `.agents/policies/supervised-autonomous-execution.md:5`: es decisión de arquitectura, no operación |
| Nueva primitive de identidad | **no** | `A1`/`A2` y `<artifact>:C-<n>` ya cumplen la función (I-23-HDK §9.2) |
| Segundo lifecycle | **no** | vocabulario único de `docs/AGENTS.md:Lifecycle`; `HD-INT-B` prohíbe estado nuevo |
| Segunda fuente normativa | **no** | `docs/placement-contract.md:22. Enforcement` (`PC-75`, `E-1`…`E-8`); `ADR-16` |
| Nuevo mecanismo de autorización | **no** | `**Status:**` + el gate existente alcanzan |
| Base de datos de derivaciones / durable execution / execution graph | **no** | `docs/architecture-capability-review.md:1. Executive Summary`; el repositorio se reconstruye desde Git + artefactos |
| `docs/notes/` (familia nueva) | **no** | `PC-10` prohíbe crear namespace; `PC-20` reserva la enmienda de §6 a la gobernanza |
| Jerarquía universal de fuentes | **no** | `.agents/policies/authority.md:Conflict protocol`; `ADR-16 AU-3`; `RQ-2` (§12.5) |
| `Intent` como entidad del payload | **no** | `AGENTS.md` (payload = data); `AGENTS.md:Do NOT` (frontera DEV/Protocol) |
| Checker semántico de prosa | **no** | `.agents/policies/validation-closure.md:5.1 Enforcement`: «No checker interprets prose» |

`HYPOTHESIS` — **El único componente genuinamente nuevo es un módulo de derivación pura**
(`runtime/orchestrator/intent.py`) más un puñado de campos y subsecciones. La justificación está en
§5.2: el requisito que lo exige, el mecanismo evaluado y por qué no alcanza.

---

## 5. Architectural Gaps

### 5.1 Los gaps, cada uno con su requisito y su impacto

`GAP` — Numerados `G-1`…`G-8`, con la evidencia de I-22/I-23/I-23-HDK y la verificación propia:

| ID | Gap | Evidencia | Impacto concreto |
|---|---|---|---|
| **G-1** | No existe derivación de la intención al Plan | I-23 §4.1; `derivation.py (regla 1)` arranca en `STOP_PLAN_NOT_FOUND`; `observe(root, plan, store)` exige un número de plan | `Implementá X` no tiene camino legítimo a trabajo |
| **G-2** | El criterio «preguntar o avanzar» mide la forma del prompt | I-23 §4.2; `INTENT_CONFIDENCE.md:Confidence levels`: `Implementá X` → 4 → `MEDIUM` → confirmación obligatoria | el sistema pide que el humano reescriba lo que el repositorio ya dice |
| **G-3** | No existe taxonomía de tipo de trabajo ni selección de obligaciones | §2.1 (`work_type`: 0 ocurrencias); I-23 §4.3 | la maquinaria aplicada fue despareja (14/153 planes con `## Delegación agentiva`) |
| **G-4** | No existe resolución de «¿qué me obliga?» | I-23 §4.6; `.agents/policies/authority.md:Document discovery` es enrutamiento por necesidad | el conjunto de obligaciones depende de que el humano o el LLM **recuerden** |
| **G-5** | La vigencia del conocimiento no es legible | §2.1 (0 headers con campo de vigencia); I-23 §4.4 | no se puede distinguir conocimiento vigente de histórico sin interpretar prosa |
| **G-6** | La Nota está nombrada tres veces y no tiene forma | I-23 §4.5; §2.2 (T-2) | dos artefactos huérfanos reales: `docs/architecture-capability-review.md` y la investigación I-22 |
| **G-7** | No hay procedencia de la derivación | I-23-HDK §4.7: 0 marcas de derivación en 153 planes, 80 RFCs y 18 ADRs | no se puede decidir si una modificación humana invalida una derivación |
| **G-8** | No está definida la granularidad del Change al **proponer** trabajo | I-23 §4.7; `.agents/policies/supervised-autonomous-execution.md:6.1` la define **después** de autorizar | la única granularidad disponible es «lo que el humano escribió» |

### 5.2 El único componente nuevo, justificado en los cinco puntos que el encargo exige

`DESIGN_OPTION` — Aplicando el formato obligatorio del encargo al módulo de derivación:

1. **Qué requisito lo exige.** `G-1` + `G-3` + `G-4`: hoy no existe ningún ejecutor que, a partir de
   una intención y del repositorio, produzca (a) un veredicto de derivabilidad, (b) un `work_type`,
   (c) un conjunto de reglas aplicables y (d) un artefacto gobernable **no autorizado**. El encargo
   pide exactamente eso como capacidad completa.
2. **Qué mecanismo existente fue evaluado.** (a) `runtime/orchestrator/derivation.py`: deriva la
   **próxima acción** de un Change **ya autorizado**; su entrada es un `ChangeObservation` construido
   desde un número de plan — no puede derivar el plan que ese número designa. (b)
   `runtime/placement/resolver.py`: resuelve **ubicación**, no obligaciones; su sujeto es un
   `PlacementRequest`, no un trabajo. (c) `.agents/policies/authority.md:Document discovery`: es una
   tabla de enrutamiento **por necesidad**, en prosa, sin ejecutor. (d) `INTENT_CONFIDENCE`: mide la
   forma del pedido, no la determinación por el repositorio.
3. **Por qué no alcanza.** Los cuatro presuponen el objeto que falta: (a) presupone el plan, (b)
   presupone el artefacto y su clase, (c) presupone que el lector ya sabe qué buscar, (d) presupone
   que la ambigüedad del texto es el problema real.
4. **Cuál es el mínimo diseño nuevo.** **Un** módulo (`runtime/orchestrator/intent.py`) con **una**
   función pura (`derive_change_candidate`) y **tres** estructuras de datos
   (`DerivabilityVerdict`, `ApplicableRule`, `DerivationPremise`), sobre el vocabulario cerrado que
   ya existe. Nada más: sin store, sin estado, sin registry, sin entidad.
5. **Qué complejidad introduce.** (a) un punto de entrada nuevo **antes** del host (el host no
   cambia de lógica); (b) una realización mecánica **read-only** del conjunto de fuentes normativas
   con guarda de divergencia, análoga a `runtime/placement/`; (c) campos aditivos en el template y
   en `ChangeObservation`; (d) cinco invariantes en `CONVENTIONS.md`. La complejidad **no**
   distribuida es deliberada: no hay un segundo sistema que mantener en sincronía.

`BOUNDARY` — **El módulo nuevo no decide autoridad.** Su salida es un veredicto de **derivabilidad**
y un artefacto **no autorizado**. Toda decisión de autoridad sigue pasando por
`runtime/orchestrator/authority.py:AuthorityBoundary.evaluate` y por el acto humano del status.

---

## 6. Intent Intake

### 6.1 Qué recibe ARgentOS cuando el humano proporciona sólo una intención

`DESIGN_OPTION` — El intake recibe **texto**, y nada más:

```text
IntakeRecord
  intent_text        el texto literal del humano                  (obligatorio; es la entrada)
  origin_type        vocabulario EXISTENTE de origin/type         (obligatorio)
                     (feature | bug | problem | debt | audit finding |
                      observation | direct maintainer action | agent proposal)
  declared_scope     rutas que el humano declaró, si las declaró   (OPCIONAL, y Declarado)
  record_artifact    el primer artifact del Change donde se registra (obligatorio)
```

`FACT` — **No se inventa una entidad `Intent`.** El repositorio ya eligió no tener entidades de
Change (`.agents/workflows/change-lifecycle.md:1`: «There is no `Change` entity, no global tracker, no
intake workflow»), y la intención **es** el texto del humano más su registro en el primer artifact
(`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`).

Razón estructural, con evidencia:
- la intención **no tiene identidad propia**: su identidad es la del artifact que la registra
  (`docs/AGENTS.md:Identity`: «Identidad ≠ path», y no hay registry global);
- la intención **no tiene lifecycle**: no se «resuelve» ni «cierra»; lo que tiene ciclo es el Change;
- crear una entidad `Intent` introduciría una **segunda representación** del mismo hecho, que es
  exactamente lo que `.agents/AGENTS.md:Fundamental operating rules 8` prohíbe.

### 6.2 Normalización (mínima, y declarada)

`DESIGN_OPTION` — La normalización **no interpreta**: extrae y conserva.

```text
normalize(intent_text) → 
   verb_phrase      la frase verbal, si existe            (no se completa si falta)
   object_phrase    el objeto/entidad del trabajo, si existe
   named_entities   rutas, IDs de gobernanza (RFC-N, plan N, ADR-N), mecanismos nombrados
   scope_hints      rutas explícitamente nombradas por el humano
   negations        lo que el humano excluyó explícitamente
   
   NUNCA:
     · completar un componente ausente
     · inferir scope a partir de «proximidad de path»           (FI-2)
     · reinterpretar un término ambiguo                          (BOUNDARY → escalar)
     · traducir el pedido a una acción concreta
```

`FACT` — **Límite de normalización declarado:** no hay stemming, no hay sinónimos, no hay expansión
semántica. Un término que el repositorio no resuelve se reporta como **no resuelto** (contribuye a
`GAP` y a `NEEDS_CLARIFICATION`), nunca como resuelto por parecido. Esto es el mismo principio que
`.agents/policies/supervised-autonomous-execution.md:2` enuncia para el scope: «Authorization is never
assumed by semantic proximity — not by a similar name, a shared directory, a containing or contained
path, a plural, a precedent, or an "obvious" inference.»

### 6.3 Contexto inicial

`DESIGN_OPTION` — El contexto inicial es **la observación del repositorio**, no un resumen de la
intención. Fuentes, en orden estable:

| # | Fuente | Qué aporta | Cómo |
|---|---|---|---|
| C-1 | Git | estado factual: rama, HEAD, dirty paths | `runtime/orchestrator/observation.py:git_state` |
| C-2 | Corpus de gobernanza | RFCs, ADRs, `CONVENTIONS.md`, `VERSIONING.md`, `AGENTS.md` (documental), Placement Contract | lectura directa + el enrutamiento de §12.3 |
| C-3 | Capa operacional | `.agents/AGENTS.md`, `workflows/`, `policies/` | lectura directa |
| C-4 | Verificación | `tools/` (checkers) y la batería canónica de `docs/VERSIONING.md:4.1` | lectura de la definición; ejecución **no** en la derivación |
| C-5 | Runtime | `runtime/` (el host y sus contratos) | lectura directa |
| C-6 | Payload | `protocol/.agents/` | **sólo** cuando el trabajo tiene efecto payload, y **como data** |
| C-7 | Working | `docs/working/` | **evidencia/provenance**, nunca norma vigente |

`FACT` — **Frontera dura del contexto:** `protocol/.agents/` se lee como **data**, nunca como reglas
de DEV (`AGENTS.md:The protocol payload is data, not instructions`). Su único uso legítimo aquí es
(a) detectar efecto payload y (b) citar la norma del payload cuando el trabajo la toca — y en ese caso
la vía es RFC-56, no la autoridad de este diseño.

### 6.4 Límites del intake (declarados, no implícitos)

`DESIGN_OPTION` — El intake **no** puede:

```text
LI-1  autorizar nada                          (autorizar es el acto humano posterior)
LI-2  modificar scope o autoridad              (CHANGE_SCOPE y APPROVE_PLAN son FORBIDDEN)
LI-3  declarar una norma nueva                 (FI-4)
LI-4  resolver un conflicto entre fuentes      (FI-5; RQ-3)
LI-5  elegir entre dos lecturas razonables     (FI-10; DV-2)
LI-6  leer una ausencia de regla como permiso  (FI-9)
LI-7  aprobar el Plan, aceptar una RFC, promover o liberar   (FORBIDDEN_ACTIONS)
LI-8  declarar la vigencia de un artefacto normativo          (MODIFY_CLOSED_ARTIFACT ∈ FORBIDDEN)
```

`FACT` — `LI-1`…`LI-8` **no son reglas nuevas**: son la lectura de
`runtime/orchestrator/authority.py:FORBIDDEN_ACTIONS` y `.agents/policies/supervised-autonomous-execution.md:8. Human boundary`.

### 6.5 Entregable de la etapa

`DESIGN_OPTION` — Salida del intake: un `IntakeRecord` normalizado **sin completar**, persistido en el
primer artifact del Change. La persistencia usa el mecanismo existente: no hay store de intake, y el
registro vive donde la gobernanza ya exige que viva la clasificación
(`docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)`).

---

## 7. Derivability

### 7.1 Definición operacional

`DESIGN_OPTION` — **Derivabilidad** es la evaluación, **posterior a la resolución de contexto**, que
responde:

> ¿El repositorio determina, sin asumir, las obligaciones que este trabajo debe cumplir?

Su salida se expresa con el **vocabulario de evidencia y autoridad que ya existe** —no con una taxonomía
de resultados propia; el mapeo operativo canónico es §7.5—:

| Condición | Señal / mecanismo existente que la expresa |
|---|---|
| el repositorio determina la respuesta, de forma única y citable | **ninguna señal bloqueante**: se construye el artefacto |
| falta una fuente, un dato o el registro de premisas | `GAP` (evidencia faltante, advisory) + `NEEDS_CLARIFICATION` |
| dos o más fuentes determinan valores incompatibles | `ANOMALY` + protocolo de conflicto |
| la intención admite ≥2 lecturas razonables | `BOUNDARY` |
| la respuesta exige una decisión que SÓLO el humano puede tomar | `REQUIRES_HUMAN` (+ `STOP_BLOCKING_PENDING_DECISION` si la decisión ya está registrada como pendiente, `PC-1`) |

`FACT` — Esta salida **no es vocabulario nuevo**: la distinción entre información ausente e información
contradictoria es la que el repositorio ya usa (`.agents/workflows/change-lifecycle.md:10. GAP vs
ANOMALY vs STOP`; `runtime/orchestrator/contracts.py:SIGNALS`), y la reserva de autoridad humana es la
que ya usan `runtime/orchestrator/authority.py:AUTHORITY_VERDICTS` y `.agents/policies/authority.md:Stop
conditions (authority)`. Las situaciones tienen **consecuencias opuestas**: unas se resuelven preguntando
(`GAP`/`BOUNDARY`), otras escalando (`ANOMALY`) y otras reservando la decisión (`REQUIRES_HUMAN`).

### 7.2 `INTENT_CONFIDENCE` **no** se reemplaza (responsabilidades distintas)

`DESIGN_OPTION` — Las dos evaluaciones responden preguntas distintas con evidencia distinta, y **no se
promedian**:

| | `INTENT_CONFIDENCE` | Derivabilidad |
|---|---|---|
| Pregunta | «¿entendí lo que el humano quiso decir?» | «¿el repositorio determina lo que hay que hacer y lo que obliga?» |
| Evidencia de entrada | **el texto** del pedido | **el repositorio** + la intención |
| Momento | al recibir el pedido | **después** de resolver contexto |
| Salida | `HIGH` / `MEDIUM` / `LOW` + criterios aplicados | «sin señal bloqueante» / `GAP` · `ANOMALY`/`BOUNDARY` / `REQUIRES_HUMAN` |
| Qué la consume | la confirmación de interpretación (fase temprana) | la construcción del Plan/Note, la aclaración, la escalación |
| Qué **no** puede hacer | no autoriza trabajo ni sustituye la derivabilidad | no sube la confianza sobre el texto ni sustituye la confirmación |

`DESIGN_OPTION` — Tabla de combinación (cada celda declara conducta; no es un promedio):

| `INTENT_CONFIDENCE` | sin señal bloqueante | `GAP` · `ANOMALY` · `BOUNDARY` | `REQUIRES_HUMAN` |
|---|---|---|---|
| `HIGH` | construir el artefacto **sin** confirmación de interpretación adicional | preguntar (`GAP`) o escalar (`ANOMALY`) | escalar la decisión, nombrando la reserva |
| `MEDIUM` | construir, **y** confirmar la interpretación reflejada antes de la autorización | preguntar o escalar | escalar |
| `LOW` | construir, **y** confirmación obligatoria detallada | preguntar o escalar | escalar |

`FACT` — La columna «sin señal bloqueante» es la que responde la pregunta central del encargo: si el repositorio
determina el trabajo y la confianza del texto alcanza, el sistema **deja de pedir que el humano
reescriba lo que el repositorio ya dice**, y le pide **una sola cosa**: autorizar. Y aun así
**la ausencia de señal bloqueante no evita la autorización** (M-1/V-5).

### 7.3 Función de decisión y orden de evaluación (el orden es normativo)

`DESIGN_OPTION` — La evaluación **no es un puntaje**: es una decisión determinista con orden
declarado. El orden no es negociable y su justificación está en I-23 §7.3.

```text
evaluate_derivability(intención, contexto):

  1. ¿el trabajo exige una decisión que SÓLO el humano puede tomar?
     (norma nueva · cambio de scope · autoridad/vía · aceptación · release/promoción ·
      resolución de conflicto · ADR-worthiness)
        SÍ → REQUIRES_HUMAN (+ STOP_BLOCKING_PENDING_DECISION)  [motivo + quién la posee + qué la bloquea]

  2. ¿dos o más fuentes determinan valores incompatibles para el mismo sujeto?
        SÍ → ANOMALY                               [TODAS las fuentes en conflicto, citadas]

  3. ¿la intención admite ≥2 lecturas razonables, dado el contexto?
        SÍ → BOUNDARY                              [lectura A + lectura B, ambas citadas]

  4. ¿falta una fuente, un dato, o el registro de premises(D) que el humano puede aportar?
        SÍ → GAP + NEEDS_CLARIFICATION             [qué falta, por qué se necesita, qué se leyó]

  5. ¿cada ítem derivable tiene EXACTAMENTE una fuente que lo determina, citable?
        SÍ → ninguna señal bloqueante: se construye el artefacto   [una cita ruta:sección por ítem]
        NO → GAP + NEEDS_CLARIFICATION             [no se encontró la fuente que lo determina]
```

`DESIGN_OPTION` — **Por qué este orden** (no es preferencia; cada paso evita un error concreto):

- **1 antes que todo:** una decisión humana pendiente no se vuelve derivable porque el repositorio sea
  internamente coherente. Es `.agents/policies/authority.md:Stop conditions (authority)` aplicado al intake.
- **2 y 3 antes que 4:** un conflicto o una ambigüedad **no son** «falta de información». Si se
  evaluaran después, un conflicto podría leerse como un dato faltante y resolverse «preguntando algo»
  en lugar de **escalar la contradicción** — exactamente la confusión que el encargo prohíbe.
- **4 antes que 5:** distingue «no sé» de «no hay» (`GAP`, no `ANOMALY`).

`DESIGN_OPTION` — **Invariantes de la derivabilidad** (lectura de normas existentes, ninguna nueva):

```text
DV-1  «ninguna señal bloqueante» ⇒ ∃ exactamente una fuente por ítem derivado, citable con ruta:sección
DV-2  dos interpretaciones razonables ⇒ NUNCA se construye el artefacto: la condición es BOUNDARY
DV-3  ANOMALY nunca se resuelve por especificidad, novedad, jerarquía ni «la más reciente»
DV-4  GAP nunca se resuelve asumiendo ni «por proximidad semántica»
DV-5  «ninguna señal bloqueante» no autoriza; sólo habilita construir un artefacto NO AUTORIZADO
DV-6  REQUIRES_HUMAN nunca se convierte en bloqueo silencioso: se registra y se nombra la reserva
```

### 7.4 Qué produce cada condición (contrato completo)

`DESIGN_OPTION` — Tabla completa, con el formato pedido por el encargo:

| Dimensión | deriva (sin señal bloqueante) | `GAP` (+ `NEEDS_CLARIFICATION`) | `ANOMALY` / `BOUNDARY` | `REQUIRES_HUMAN` |
|---|---|---|---|---|
| **Entradas** | intención + contexto suficiente | intención + contexto con una fuente o un dato ausente | intención + contexto con ≥2 fuentes incompatibles, o ≥2 lecturas | intención cuya ejecución exige una decisión humana |
| **Decisión** | construir el artefacto `proposed` | **preguntar** | **detenerse y escalar**; no elegir | **detenerse y escalar** la decisión |
| **Evidencia requerida** | una cita `ruta:sección` por ítem; estado Git del baseline | qué falta, por qué se necesita, qué se intentó leer | fuente A + fuente B + el punto exacto de incompatibilidad + impacto | qué decisión se requiere, quién la posee, qué la bloquea |
| **Veredicto de reglas asociado** | todas `APPLIES`/`NOT_APPLICABLE` | al menos una fuente con aplicabilidad indeterminada (`GAP`) | al menos dos `APPLIES` en conflicto | la reserva de autoridad aplicable |
| **Vocabulario existente** | — (construye) | `NEEDS_CLARIFICATION`; `GAP` | `ANOMALY`; `BOUNDARY`; protocolo de conflicto | `REQUIRES_HUMAN` |
| **Stop condition** | no | formulario de aclaración (`NO_ASSUMPTIONS`) | escalación de conflicto | escalación de autoridad |
| **Nunca** | convertirse en autorización | convertirse en asunción | convertirse en elección automática | convertirse en bloqueo sin registro |

### 7.5 Mapeo al vocabulario existente (sin taxonomía nueva)

`FACT` — **Este apartado es el mapeo operativo canónico.** El diseño **no crea** un vocabulario de
incertidumbre ni una taxonomía de derivación: la condición que decide cada paso se expresa con el
vocabulario y los mecanismos que ya existen.

| Condición evaluada | Vocabulario / mecanismo existente que la expresa | Qué produce |
|---|---|---|
| la derivación puede continuar | **ninguna señal bloqueante** (`BLOCKING_SIGNALS = {ANOMALY, BOUNDARY}`, `runtime/orchestrator/contracts.py:SIGNALS`) | se construye el artefacto, que nace en el status existente `Aprobado para redacción` |
| falta información | `GAP` (evidencia faltante, advisory) + `NEEDS_CLARIFICATION` (`protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:When to ask for clarification`) | pedido de aclaración con el formato de `NO_ASSUMPTIONS` |
| la información presente es **contradictoria** entre fuentes | `ANOMALY` (señal **bloqueante**) + protocolo de conflicto (`.agents/policies/authority.md:Conflict protocol`) | escalación con **todas** las fuentes citadas y el punto de incompatibilidad |
| la información presente es **ambigua por estructura** de la intención | `BOUNDARY` (señal **bloqueante**) | pedido de aclaración con las dos lecturas |
| la derivación **no puede continuar sin autoridad humana** | `REQUIRES_HUMAN` (`runtime/orchestrator/authority.py:AUTHORITY_VERDICTS`) + `STOP_BLOCKING_PENDING_DECISION` cuando la decisión humana ya está registrada como pendiente (`PC-1`: `resolución: pendiente`) | escalación de la decisión, con dueño y bloqueo nombrados |

`FACT` — **Vocabulario que deja de existir como taxonomía normativa (`PROVENANCE`).** Los nombres que
este documento usó durante su redacción para esas mismas condiciones —`DERIVED`; `UNDETERMINED` con sus
subcasos `MISSING` y `CONFLICT`; `NOT_DERIVABLE`; y la obligación de declarar un `subkind`— **no son
vocabulario vigente**. Se conservan únicamente como procedencia de la redacción, para poder leer los
apartados que todavía los nombran (§3.1, §7.1–§7.4, §13.4, §18.1, §20, §24). Ninguna obligación se
expresa con ellos, no se persisten como estado y no sustituyen a las señales de la tabla anterior.

`DESIGN_OPTION` — **Nota de vocabulario, obligatoria:** cada condición de la tabla es un **resultado de la
evaluación**, no un estado de un artefacto ni un miembro de un enum global. No crea state machine, no se
persiste como estado y no tiene transiciones propias: se **registra** como parte de la clasificación
del Change, igual que hoy se registra el intake.

### 7.6 Relación con `NO_ASSUMPTIONS`

`FACT` — `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:When to ask for clarification`
declara el criterio rector y este diseño **lo aplica con mejor evidencia de entrada**:

```text
NO_ASSUMPTIONS:  el agente PUEDE avanzar sin aclaración sólo cuando
                 «the missing detail has exactly one reasonable interpretation
                  given the context»
este diseño:     «el contexto» se hace operacional = las fuentes del repositorio

  ⇒ DERIVED ⇔ exactamente una fuente que determina cada ítem
  ⇒ DERIVED ⇏ el agente puede asumir              (DV-4/DV-5)
```

`FACT` — El diseño **no debilita** `NO_ASSUMPTIONS`: le da un contexto verificable. Una hipótesis no
se convierte en decisión; una ausencia no se convierte en permiso.

### 7.7 Enmienda al orden propuesto por I-23 (con evidencia)

`CONTRADICTION` — `HYPOTHESIS` — El orden de I-23 §7.3 coloca en el paso 3 «¿existe más de una
interpretación razonable?» → `UNDETERMINED / CONFLICT`. Medido contra el vocabulario del repositorio,
**la ambigüedad de la intención es `BOUNDARY` y la contradicción entre fuentes es `ANOMALY`**
(`.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP`: `ANOMALY` = «information present
but contradictory, or demonstrable violation»; `BOUNDARY` = «structural ambiguity (checker signal)» →
«human review; never guess or invent a tie-break»).

`DESIGN_OPTION` — **Veredicto:** el orden de I-23 se conserva íntegro; lo que este diseño **no**
hace es fusionar los dos subcasos: `CONFLICT` en el sentido de I-23 cubre dos cosas distintas
(contradicción entre fuentes = `ANOMALY`; ambigüedad de la intención = `BOUNDARY`), y ambas producen
el mismo comportamiento (detenerse y escalar) pero **evidencia distinta** y audiencia distinta. El
contrato de §7.4 exige declarar **cuál de los dos** es, en la evidencia requerida. Esto es aditivo:
no cambia el orden ni el veredicto.

---

## 8. `premises(D)`

`FACT` — Este es el elemento central del Change, y el encargo lo fija como obligatorio (`HD-K3`).
La propiedad buscada es exactamente:

```text
D₁ + premises(D₁) + modificación humana  →  determinación de si D₁ sigue siendo válida
```

### 8.1 Qué constituye una premisa

`DESIGN_OPTION` — Una **premisa** es una **entrada con la que la derivación `D` fue producida**, y
nada más. La lista es **cerrada** y proviene de las seis entradas que I-23 §12.1 ya enumera más el
scope/autoridad humanos:

| # | Clase de premisa | Qué es | Dueño | Cómo se cita |
|---|---|---|---|---|
| `P-1` | **Intención** | el texto normalizado del pedido + su `origin_type` | humano | identidad del artifact de intake |
| `P-2` | **Confianza de intención** | el nivel `HIGH`/`MEDIUM`/`LOW` y los criterios aplicados | agente | `INTENT_CONFIDENCE.md:Confidence levels` + el artifact que lo registra |
| `P-3` | **Conjunto de contexto** | las fuentes efectivamente leídas | agente | lista de `ruta:sección` |
| `P-4` | **Veredicto de derivabilidad** | `DERIVED` + su evidencia (una cita por ítem) | agente | el propio registro |
| `P-5` | **`work_type`** | el valor derivado y su criterio de admisión | agente | §11 |
| `P-6` | **Conocimiento vigente** | el lifecycle declarado de cada fuente citada | documento | §15 |
| `P-7` | **Reglas aplicables** | los veredictos `APPLIES`/`NOT_APPLICABLE` con su cita | agente | §12 |
| `P-8` | **Autoridad y scope** | la autoridad requerida y el conjunto declarado de rutas | **humano** | la declaración del humano |

`BOUNDARY` — **Límite declarado de la lista:** es **cerrada para el MVP**. Agregar una clase de
premisa es un cambio de modelo, no una operación; requiere la misma vía que este Change. La lista no
incluye el contenido de los campos derivados (esos son **salida** de `D`, no premisa), y por eso la
clase de una propiedad y su papel en el grafo son **dos cosas distintas** (§8.3).

### 8.2 Cómo se representa (el registro, no la entidad)

`DESIGN_OPTION` — `premises(D)` se materializa como **sección nueva del template de Plan**, con una
fila por clase y **evidencia citada**, más la declaración explícita de la **categoría de cada campo**
del artefacto (necesaria para `R-2`/`R-3`, §9.4):

```markdown
## Derivación y premisas

**Derivación:** D1
**Estado:** vigente | inválida para el contenido actual (D2) 
**Veredicto de derivabilidad:** DERIVED | UNDETERMINED (MISSING|CONFLICT) | NOT_DERIVABLE
**Evidencia del veredicto:** <una cita ruta:sección por ítem derivado>

| Clase | Valor | Fuente / evidencia | Categoría del campo | Vigente |
|---|---|---|---|---|
| P-1 Intención | <texto normalizado> | <artifact de intake> | Declarado | <lifecycle de la fuente> |
| P-2 Confianza | MEDIUM (+,+; criterios …) | `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md:Confidence levels` | Derivado | active |
| P-3 Contexto | <fuentes leídas> | <lista ruta:sección> | Derivado | — |
| P-4 Derivabilidad | DERIVED | <cita por ítem> | Derivado | — |
| P-5 `work_type` | mechanism | `docs/CONVENTIONS.md:…` | Derivado | active |
| P-6 Conocimiento | <fuentes citadas y su lifecycle> | `docs/AGENTS.md:Lifecycle` | Derivado | — |
| P-7 Reglas aplicables | APPLIES: … ; NOT_APPLICABLE: … | <cita de cada fuente> | Derivado | — |
| P-8 Autoridad y scope | <autoridad + rutas> | la declaración del humano | **Declarado** | — |
```

`FACT` — **Por qué una sección y no una entidad, un archivo o una base de datos:**
- `A1`/`A2` (`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors…`) y `<artifact>:C-<n>`
  (`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones`) son el precedente exacto: un
  registro de procedencia **vive en el artefacto que lo posee** (PC-1) y **no constituye entidad**;
- crear una base de datos de derivaciones o un archivo `premises.json` introduciría un **segundo
  lugar** donde vive el estado del Change, y `.agents/AGENTS.md:Fundamental operating rules 8` lo
  prohíbe;
- la sección viaja **con el artefacto**: si el artefacto se supersede, el registro se supersede con
  él; si se cierra, queda como traza (RFC-46), sin mecanismo adicional.

### 8.3 Cómo se identifica una premisa (y por qué no hace falta identidad nueva)

`DESIGN_OPTION` — Una premisa se identifica por **la tupla `(clase, fuente)`**, no por un ID nuevo:

```text
premisa := (clase ∈ {P-1 … P-8}, fuente = cita ruta:sección | identidad de artifact | declaración humana)
```

`FACT` — **No se inventa una primitive de identidad.** Las identidades existentes alcanzan:
- la **fuente** de una premisa es un artefacto con identidad estable (`RFC-N`, `ADR-N`, `plan NN`) o
  una declaración humana registrada;
- la **derivación `D`** se identifica por un locator local (`D1`, `D2`) **dentro del namespace del
  artefacto**, exactamente como `A1`/`A2` y `C-<n>` (`docs/CONVENTIONS.md:…Findings y correcciones…`:
  «el número es locator del registro, nunca autoridad normativa»);
- la **identidad material del contenido** ya existe donde importa (`Scoped Content Identity` del
  anchor) y **no se duplica** aquí.

`FACT` — Lo que **no** importa para decidir: un hash de la derivación. I-23-HDK §9.2 lo verifica:
«¿La identidad debe ser conceptual, material o ambas? **Conceptual**». La comparación de §8.4 es de
**conjuntos**, no de hashes.

### 8.4 Cómo se compara una derivación con sus premisas anteriores (la frontera mecánica)

`DESIGN_OPTION` — La comparación es **de conjuntos** y es **booleana**: no hay scoring, no hay
umbral, no hay métrica de impacto (el encargo los prohíbe, y `validation-closure.md:5.1` prohíbe al
checker interpretar prosa).

```text
premises_effective(D)  = el conjunto de premisas VIGENTES hoy
premises_recorded(D)   = el conjunto registrado cuando D se produjo

comparación:
  para cada clase P-i:
     recorded(P-i) == effective(P-i)   →  la premisa no cambió
     recorded(P-i) != effective(P-i)   →  la premisa CAMBIÓ  ⇒ D inválida para el contenido nuevo
     effective(P-i) NO establecible    →  UNDETERMINED (R-5), nunca asunción
```

`BOUNDARY` — **Límite declarado, sin adornos (I-23-HDK §5.4/§7.3, verificado por este diseño):** la
frontera es mecánica **en la comparación**, no en la **lectura**. Determinar *qué* premisa cambió
cuando el humano reescribe prosa libre sigue siendo una lectura humana o asistida, y el repositorio
**declara que ningún checker interpreta prosa** (`.agents/policies/validation-closure.md:5.1
Enforcement`, reiterado en `:5.2`). El sistema honesto es el que **lo declara y se detiene** en vez de
inferirlo: por eso existe `R-5`.

`FACT` — **Por qué esta frontera y no «semánticamente relevante»:** «semánticamente relevante» no es
decidible (I-23-HDK §7.2) y el encargo prohíbe usarlo como criterio mecánico. La pertenencia a un
conjunto registrado **sí** es decidible, y donde no lo es produce `UNDETERMINED`.

### 8.5 Qué se re-deriva cuando una premisa cambia

`DESIGN_OPTION` — Alcance de la re-derivación, decidido por evidencia y no por conveniencia:

| Situación | Re-derivación | Fundamento |
|---|---|---|
| `Scope` (P-8) cambia, **cualquier** dirección | **total, siempre** | `HD-K1` (**pendiente**, `PC-1`): **no** se introduce excepción para reducciones «inocuas» |
| Cualquier otra premisa `P-1`…`P-7` cambia | **total** | el grafo campo→premisa **no está declarado** hoy; la re-derivación local (`D-1` de I-23-HDK §10.1) sólo se vuelve decidible si el Change materializa el grafo, y este diseño **no** lo introduce en el MVP |
| `premises(D)` no establecible | **ninguna**: `R-5` → `UNDETERMINED` | §8.4 |

`DESIGN_OPTION` — **Lo que la re-derivación NO puede hacer, y es obligatorio por `DESIGN_OPTION D-4`
del encargo:** la re-derivación **no** reemplaza el contenido completo del artefacto. No puede borrar
declaraciones humanas que no formaban parte de `premises(D)`. Mecanismo: §9.5.

### 8.6 Localización de la definición (para no duplicar norma)

`DESIGN_OPTION` — `premises(D)` es definido **una sola vez** en `docs/CONVENTIONS.md` (§18, `INV-2`),
y el template lo referencia sin duplicar la lista. El template declara **el formato**; `CONVENTIONS.md`
declara **la obligación y la semántica**. Es el reparto que ya existe entre
`docs/plans/_TEMPLATE.md` (formato del anchor) y `docs/CONVENTIONS.md:Change Lifecycle — Validation
anchors…` (semántica de VC-1).

---

## 9. Human Modification

`DESIGN_OPTION` — El modelo distingue **cinco** resultados, y distingue **dos momentos** que no se
mezclan (I-23-HDK §8.2):

```text
MOMENTO 1 — pre-autorización (este diseño; HD-K)
  el humano modifica el artefacto `proposed`
  ⇒ R-1 … R-5
  ⇒ la modificación NO es violación (es dueño del scope), NO es autorización (PC-52) y
    NO cambia el status (el status es de gobernanza; la modificación es de contenido)

MOMENTO 2 — post-`pin` (SAE; este diseño NO lo toca)
  el humano modifica `Scope`/`Task`/status después de la primera autorización
  ⇒ authorization_drift ⇒ STOP_SCOPE_VIOLATION / REQUIRES_HUMAN, sin efecto persistente
  ⇒ el checkpoint original se preserva (`_pinned_autonomy_projection` devuelve el MÁS TEMPRANO)
```

`FACT` — La frontera temporal entre ambos momentos está **declarada y testeada**:
`runtime/orchestrator/autonomy.py:authorization_drift` documenta que `pinned is None` significa «not
pinned yet» y se reporta como ausencia de divergencia. **El diseño nuevo vive exactamente en la
ventana que el checkpoint no cubre, y no la extiende.**

### 9.1 Preguntas de decisión (las únicas cuatro)

```text
Pregunta 1 (editorial):   canonical_text(campo) es idéntico antes y después?
Pregunta 2 (premisa):     ¿qué campo(s) tocó la modificación, y alguno está en premises(D)?
Pregunta 3 (autoridad):   ¿lo que la modificación introduce cae en FI-1…FI-10?
Pregunta 4 (decidible):   ¿premises(D) pudo establecerse?
```

### 9.2 El criterio editorial (reutilizado, no inventado)

`FACT` — `runtime/orchestrator/autonomy.py:_canonical_text` normaliza *runs* de espacios:
«Re-wrapping a field or re-indenting it is the *same* declaration, so it must not read as a change of
authorization. Every other change of the words does.»
`tests/test_sae_scope_enforcement.py` verifica exactamente eso (y `authorization_scope_projection`
ordena, así que reordenar una lista de scope es editorial).

`DESIGN_OPTION` — Formulación correcta, con su límite declarado:

```text
editorial  ⇔  canonical_text(antes) == canonical_text(después)   para cada campo afectado
```

`BOUNDARY` — El criterio es una **cota inferior verificable**, no la definición completa: no normaliza
puntuación, sinónimos ni voz verbal, así que hay cambios editoriales legítimos (una coma, una tilde)
que no reconoce como idénticos. Declararlos editoriales es juicio, y un juicio se registra (no se
mecaniza). **No se propone extender `_canonical_text`:** sería cambiar un mecanismo de autorización
para resolver un problema de clasificación editorial.

`FACT` — **Caso que fija el límite y que el diseño debe declarar:** corregir un path mal escrito
(`tools/foo.py` → `tools/fooo.py` donde sólo existe el segundo) **no es editorial**, aunque sea
«textual»: cambia el **referente**, no la representación. Por eso el criterio es semántico y el
ejemplo demuestra por qué «textual» no sirve como regla.

### 9.3 Los cuatro casos del encargo, con su tratamiento

`DESIGN_OPTION` — Mapeo directo de los casos exigidos:

| Caso del encargo | Resultado | Efecto sobre la derivación anterior | Efecto sobre declaraciones humanas |
|---|---|---|---|
| **Cambio editorial** (no cambia la representación semánticamente relevante) | `R-1` | se **conserva** `D` (proyección canónica idéntica) | ninguna |
| **Cambio de una premisa** | `R-4` | `D` queda **inválida para el contenido nuevo**; se produce `D2` | se **conservan** todas |
| **Cambio cuyo impacto no puede determinarse** | `R-5` | **`UNDETERMINED`**; no se asume que sobrevive ni que murió | se conservan; se pide aclaración |
| **Nueva declaración humana** | `R-2` / `R-3` | `D` sigue válida para lo que produjo | se **registra** y se conserva (obligatorio por `DESIGN_OPTION D-4`) |

`FACT` — `HD-K1` (**pendiente**, `PC-1`) hace **incondicional** un caso que la investigación había dejado
abierto: **toda** modificación de `Scope` —expansión o reducción— requiere re-derivación, sin
excepción para reducciones «inocuas». Consecuencia: `R-4` aplica a cualquier cambio de `Scope`,
aunque no altere ninguna obligación resuelta.

### 9.4 Una sola categoría por campo (elimina la ambigüedad que B introducía)

`FACT` — I-23-HDK §5.2/§6.2 identificó el defecto real de registrar `Derived: X` **y**
`Human: Y` sobre el mismo campo: deja el campo con dos valores y ninguna regla de precedencia.

`DESIGN_OPTION` — La representación correcta es **una sola categoría por campo**, con cuatro
categorías y su regla de frontera:

| Categoría | Definición | Regla de frontera | Quién la posee |
|---|---|---|---|
| **Derivado** | el sistema lo produce con fuente citable y determinación única | sin fuente única → **no** es derivado (pasa a Confirmado o a `UNDETERMINED`) | el derivador |
| **Declarado** | debe venir explícitamente de la intención/autorización humana | el agente **nunca** lo completa por defecto (`PC-52`: «A request is not an authorization») | el humano |
| **Confirmado** | ARgentOS lo propone y el humano confirma | el default es **propuesta**, nunca aceptación tácita; la confirmación se registra | propuesta del agente, confirmación humana |
| **Forbidden-to-infer** | nunca puede inferirse legítimamente | su ausencia **detiene**; no se sustituye por un default | nadie: requiere humano |

`FACT` — «Confirmado» **no es vocabulario nuevo**: `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Recording user decisions`
distingue `user_confirmed: true` de `false`, y `:Unattended mode` declara que un default aplicado se
marca `PENDING_USER_CONFIRMATION` y que «unreviewed default is never treated as user-confirmed».
`protocol/.agents/standards/runtime/AUTHORIZATION.md:AUTH-002` declara que `user_confirmed=false`
**nunca** constituye autorización.

`FACT` — **Reparto de campos por categoría** (I-23 §12.1, adoptado y verificado contra
`docs/plans/_TEMPLATE.md`):

| Campo / sección | Categoría | Consecuencia en `R-*` |
|---|---|---|
| `**Change Level:**` | Derivado | cambiarlo a mano ≠ acto declarativo |
| `**Work type:**` (nuevo) | Derivado (con corrección humana sólo si `UNDETERMINED`, `HD-K2`) | `R-4` si fue premisa |
| `**Clase:**` (A/B) | Derivado + Confirmado | `R-4` si el derivado quedó producido con otro valor |
| `**RFC:**` | Derivado + Confirmado | ídem |
| `**Origen:**` | **Declarado** | `R-2`, o `R-4` si cambia la intención de la que se derivó |
| `**Fecha:**`, `**Depende de:**` | Derivado | — |
| `## Objetivo` | **Confirmado** | `R-2`, o `R-4` si de él se derivaron otros campos |
| `## Criterio de entrada` | Derivado | — |
| `## Entregables` | Derivado | — |
| `## Pasos` | Derivado | — |
| `## Delegación agentiva → Task` | **Declarado** | `R-2`/`R-3`; `R-4` porque es premisa de `work_type`, entregables, verificación |
| `## Delegación agentiva → Scope` | **Declarado** | **`R-4` incondicional** (`HD-K1`) |
| `## Criterios de salida` | Derivado + Confirmado | `R-2`, o `R-4` si fue premisa |
| `## Verificación` | Derivado (+ confirmación si hay juicio) | — |
| `## Riesgos` | Confirmado | `R-2` |
| `## Trazabilidad` | Derivado | — |
| `## Derivación y premisas` | Derivado | es el registro mismo; **nunca** se edita a mano sin `R-4` |
| `**Status:**` inicial | Derivado = `Aprobado para redacción` | — |

`FACT` — El criterio que separa «decido» de «invalido» **no es el campo, es su posición en
`premises(D)`** (I-23-HDK §5.2 in fine). Un campo `Declarado` que **no** fue premisa de ningún campo
derivado se modifica sin invalidar nada; uno que **sí** lo fue, invalida. `Task`/`Scope` son el caso
más claro: son `Declarado` **y** premisa de `Entregables`, `Pasos`, `Verificación` y `work_type`.

### 9.5 Por qué la re-derivación no puede borrar una declaración humana (invariante `INV-4`)

`DESIGN_OPTION` — Esta es la parte del diseño que cierra el riesgo real de toda re-derivación total, y
es **obligatoria** por `DESIGN_OPTION D-4`:

```text
REGLA DE PRESERVACIÓN
  el artefacto es la UNIÓN de dos capas:
      capa derivada      los campos cuya categoría es Derivado
      capa declarada     los campos/campos añadidos cuya categoría es Declarado o Confirmado

  una re-derivación D1 → D2:
      · REESCRIBE la capa derivada
      · NUNCA toca la capa declarada
      · NUNCA elimina un elemento `R-3` (declaración añadida que no era premisa)
      · si un elemento declarado debe cambiar para que D2 sea coherente,
        eso es una NUEVA decisión humana, no un efecto de la re-derivación
```

`FACT` — La regla se puede hacer **parcialmente mecánica** sin interpretar prosa: basta con que cada
elemento del artefacto lleve su categoría declarada y que el escritor de la re-derivación tenga
prohibido escribir sobre elementos marcados `Declarado`/`Confirmado` sin un acto humano registrado.
Es un **invariante de escritura**, no un checker semántico (§17 `E-5`).

`DESIGN_OPTION` — **Consecuencia de trazabilidad:** `D1` se conserva como procedencia. La secuencia
completa es `Intent → D1 → P (M1) → D2? → A1`, donde `D1` **nunca** se muta y `M1` queda registrada
como decisión humana con la categoría del campo que tocó. Es el patrón de `A1`/`A2`:

```text
A1 → A2   : la cadena es histórica, no una mutación
D1 → D2   : idem
M1        : provenance del valor que reemplazó al derivado
A1 (auth) : autoriza P tal como está al autorizar (absorbe M1 por construcción)
```

### 9.6 Modificar ≠ autorizar (el riesgo principal, cerrado explícitamente)

`FACT` — `docs/placement-contract.md` (`PC-52`: «a request is not an authorization») y
`protocol/.agents/standards/runtime/AUTHORIZATION.md:AUTH-002` enuncian una dirección. **La dirección
inversa no está enunciada**, y es el riesgo principal del modelo:

```text
MK-1  modificar(P) ⇏ autorizar(P)
      la autorización sigue siendo el acto que lleva el status a `Aprobado para ejecución`
```

`FACT` — Evidencia de que el repositorio ya respeta esta separación en la práctica: el **Plan 136**
nació `Aprobado para redacción` y el mantenedor autorizó **por directiva**, sin que el artefacto se
actualizara; el repositorio **no** lo leyó como un simple cambio de contenido, sino como una decisión
humana que hubo que registrar (`<PLAN-136>:F-5`, `<PLAN-136>:PC-1`).

### 9.7 Alternativas evaluadas y descartadas

`DESIGN_OPTION` — Evaluadas contra la evidencia; se registran para que no reaparezcan:

| Alternativa | Veredicto | Razón |
|---|---|---|
| Registrar la modificación como corrección `C-<n>` | **descartada** | `C-<n>` es la corrección de un finding sobre contenido **ejecutado** con alcance de revalidación (`docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones`); usarlo aquí crearía un finding ficticio |
| Prohibir la edición humana del `proposed` | **descartada** | un `proposed` no autorizado es texto; prohibirlo no protege nada que el gate no proteja, y contradice `AU-5` («no silenciosamente»: la modificación legítima **se registra**, no se prohíbe) |
| Versionado de Planes (D1 vs D2 como versiones) | **descartada** | el repositorio no versiona planes; `docs/AGENTS.md:Identity` declara que la identidad no es path ni versión; sería una primitive nueva |
| Extender la proyección del checkpoint para cubrir la ventana pre-`pin` | **descartada** | el checkpoint responde «¿cambió la declaración desde que autorizó?»; antes de autorizar no hay nada que comparar, y `authorization_drift(None, …)` lo declara correctamente |
| Scoring de impacto semántico | **descartada** | prohibido por el encargo; la comparación de conjuntos es booleana |
| Checker que decida si la modificación «cambió el significado» | **descartada** | `.agents/policies/validation-closure.md:5.1 Enforcement` declara que ningún checker interpreta prosa |

---

## 10. R-1…R-4

`DESIGN_OPTION` — **Los resultados del modelo son cinco.** El encargo pide «no inventar nuevos
resultados si los cuatro existentes cubren el modelo»; la evidencia demuestra que **no lo cubren**:
la investigación de HD-K dejó abiertos por separado `R-5` (rechazo por `FI-1…FI-10`) y `R-6`
(`premises(D)` no establecible), y `R-3` (declaración añadida, `DESIGN_OPTION D-4`) frente a `R-2`
(declaración sobre campo no-premisa). **Cuatro de esos cinco coinciden con los `R-1`…`R-4` del
encargo**; el quinto, `R-5`, es el rechazo por autoridad, que **no es un resultado de modificación
sino un stop**, y por eso se mantiene dentro de la tabla como **stop condition** y no como resultado
de aceptación. La tabla siguiente es la definitiva.

### 10.1 Tabla completa

| Dimensión | **`R-1` Editorial** | **`R-2` Decisión humana** | **`R-3` Declaración añadida** | **`R-4` Cambio de premisa** | **`R-5` No decidible** |
|---|---|---|---|---|---|
| **Condición** | `canonical_text` idéntico antes/después en cada campo afectado | toca un campo `Declarado`/`Confirmado` que **no** es premisa de ningún campo derivado, y no cae en `FI-1`…`FI-10` | **añade** un elemento que no estaba en `premises(D)` y no se deriva de ellas | toca **cualquier** campo que **es** premisa de `D` (incluye `Scope`/`Task`; `Scope` **siempre**, `HD-K1`) | `premises(D)` **no puede establecerse**, o hay dos lecturas |
| **Entrada** | el campo antes/después | el campo + su categoría + `premises(D)` | el elemento nuevo + `premises(D)` | el campo + `premises(D)` | el artefacto + `premises(D)` ausente/ambiguo |
| **Decisión** | **se acepta**; la derivación se conserva | **se acepta**; se registra como decisión humana | **se acepta** como declaración humana nueva | `D` **inválida para el contenido nuevo** | **`UNDETERMINED`**: se detiene y se pregunta |
| **Resultado** | `R-1` — nada que re-derivar | `R-2` — el artefacto ya no es sólo el resultado de `D` | `R-3` — el artefacto pasa a ser «`D` + la declaración» | `R-4` — `D2` | `R-5` — `UNDETERMINED / MISSING` |
| **Efecto sobre la derivación anterior** | **ninguno** (proyección idéntica) | **ninguno** | **ninguno** para lo que `D` produjo | **`D1` deja de ser válida** para el contenido nuevo; `D1` **se conserva** como procedencia | **no se asume** ni que sobrevive ni que murió |
| **Efecto sobre declaraciones humanas** | ninguna | se registra con su categoría | se registra con su categoría; **no puede ser eliminada** por una re-derivación (§9.5) | **se conservan todas** (§9.5) | se conservan; se pide aclaración |
| **¿Genera nueva derivación?** | **no** | **no** | **no** | **sí** (`D2`; total en el MVP, §8.5) | **no** hasta que se aclare |
| **¿Requiere humano?** | no (la modificación **ya** es humana) | no (es el acto humano) | no (es el acto humano) | **sí**, al final: la autorización (§14) | **sí**: aportar el dato o el registro de premisas |
| **Evidencia requerida** | la proyección canónica idéntica | la decisión + la categoría del campo + `premises(D)` que prueba que no era premisa | el elemento añadido + `premises(D)` que prueba que no era premisa | `premises(D1)` **y** `premises(D2)`, ambas citadas | qué falta, por qué se necesita, qué se intentó leer |
| **Stop condition** | ninguna | ninguna | ninguna | el artefacto vuelve a `proposed` (`Aprobado para redacción`) | `UNDETERMINED / MISSING` → aclaración con el formato de `NO_ASSUMPTIONS` |
| **Invariante que lo sostiene** | `MK-2` | `MK-1` | `MK-3` | `MK-4` | `MK-5` |

### 10.2 Stop separado (no es un resultado de aceptación)

`DESIGN_OPTION` — El encargo pide una cuarta situación además de B+C (editorial / declarativa /
invalidante). **La cuarta es `R-3`** (declaración añadida), y es exactamente el complemento `D-4` de
I-23-HDK §10.4: es el único caso en que «no re-derivar» es la respuesta **correcta**, y sin él el
sistema re-derivaría de más y borraría la declaración humana.

`DESIGN_OPTION` — **El rechazo por autoridad es un `STOP`, no un resultado.** Cuando lo introducido
cae en `FI-1`…`FI-10` (norma nueva, autoridad, efecto no contemplado, resolución de conflicto,
`protocol/.agents/`), el resultado **no** es `R-1`…`R-4`:

```text
STOP-1  lo introducido cae en FI-1…FI-10
        → STOP / REQUIRES_HUMAN, con la decisión que falta nombrada y quién la posee
        → evidencia: la reserva de autoridad aplicable
        → fuentes: FI-1…FI-10; runtime/orchestrator/authority.py; 
                   .agents/policies/authority.md:Stop conditions (authority); AU-6
```

`FACT` — **Por qué no es un quinto resultado:** un resultado describe qué le ocurre a la derivación;
un stop describe que la decisión **no es del agente**. `runtime/orchestrator/authority.py` ya tiene el
veredicto para eso (`REQUIRES_HUMAN`), y agregarlo como resultado mezclaría las dos cosas.

### 10.3 Invariantes del modelo de modificación

`DESIGN_OPTION` — Escritos en la forma del repositorio; **ninguno es nuevo**, son lectura de los
existentes:

```text
MK-1  modificar(P) ⇏ autorizar(P)                              (PC-52; AUTH-002)
MK-2  editorial ⇔ proyección canónica idéntica                 (autonomy.py:_canonical_text)
MK-3  una declaración humana añadida NO se elimina por una re-derivación   (DESIGN_OPTION D-4)
MK-4  premises(D) cambió ⇒ D inválida para el contenido nuevo  (HD-K3; CL-2 como precedente)
MK-5  premises(D) no establecible ⇒ UNDETERMINED, nunca asunción (AUTH-004 como precedente)
MK-6  post-pin, el camino es el existente (STOP_SCOPE_VIOLATION); este modelo NO lo toca
MK-7  re-derivar es proponer: no autoriza, no amplía scope, no cambia autoridad
MK-8  D1 se conserva como procedencia; nunca se muta ni se borra (A1/A2 y C-<n> como precedente)
MK-9  una sola categoría por campo                             (elimina «Derived: X + Human: Y»)
```

`FACT` — `MK-6` es la garantía de no interferencia: el checkpoint de autorización sigue siendo el
único mecanismo que gobierna la ventana post-`pin`, y su frontera temporal está declarada y testeada
(`runtime/orchestrator/host.py:_pinned_autonomy_projection`; `tests/test_sae_scope_enforcement.py`).

---

## 11. Plan vs Note

### 11.1 Principio

`FACT` — `HD-INT-E2` es **consecuencia derivada de `HD-INT-E`** (acto del mantenedor, 2026-10-02): la
selección entre **Plan** y **Note** se deriva mediante **criterios de gobernanza y trabajo**; **NO** se
determina mecánicamente a partir del Change Level, y **no** recibe autoridad humana propia.
`PC-1` (`resolución: adoptada`, 2026-10-02) — `HD-INT-E`: una `Note` puede autorizar; no toda autorización requiere un Plan.
`PC-1` (`resolución: adoptada`, 2026-10-02) — `HD-INT-D`: la `Note` es un artefacto **Working por naturaleza documental**
(`docs/AGENTS.md:Folder → class map`; **no** un artefacto de la familia `Working analysis`) y **no** se
crea una familia ni un namespace nuevo para ella: vive dentro de la familia `Plan` ya declarada
(**Opción A**, §14.3).

`DESIGN_OPTION` — **La separación que hace esto decidible (y que ya existe):** la investigación redujo
la elección a **una sola pregunta**, y esa pregunta es la misma que separa `work_type` (I-23 §11.9):

> **¿El trabajo cambia lo que el sistema HACE o PRESCRIBE, o sólo lo que se SABE o REGISTRA de él?**

`FACT` — Esa pregunta **no es una jerarquía de autoridad nueva**: es la lectura de la matriz de
gobernanza por tipo de Plan (`docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle`) y de la
definición de Clase C de RFC-56 («cero cambio de significado»,
`docs/rfc/56-governance-fast-track.md:Decisión propuesta`). No introduce nivel, rango ni precedencia.

### 11.2 Criterios (conjunto cerrado, evaluado sobre el trabajo derivado)

`DESIGN_OPTION` — Los criterios son los del encargo, cada uno con su consecuencia real. **Ninguno
introduce autoridad:** todos seleccionan **artefactos, gates o verificación**.

| # | Criterio | Pregunta | Si SÍ → | Fuente |
|---|---|---|---|---|
| `C-1` | **Implementación** | ¿el trabajo modifica código (`runtime/`, `tools/`, `tests/`)? | **Plan** | RFC-75 Mecanismo 5 (`runtime/tools/tests-only`) |
| `C-2` | **Contenido normativo** | ¿modifica `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`, un RFC, un ADR, una policy o un workflow activo? | **Plan** | I-23 §8.4.1; `AU-5` |
| `C-3` | **Payload** | ¿toca `protocol/.agents/`? | **Plan** + vía RFC-56 (el tipo **no** exime) | `docs/rfc/56-governance-fast-track.md:Reglas de borde` |
| `C-4` | **Decisión de diseño/arquitectura** | ¿requiere una decisión nueva de diseño o arquitectura? | **Plan** (+ ADR si `AU-6`) | `.agents/policies/authority.md:ADR-worthiness` |
| `C-5` | **Duración / múltiples sesiones** | ¿`duration/complexity` ≥ 2? | **Plan** | RFC-75 Mecanismo 2 |
| `C-6` | **Múltiples pasos / multi-capa** | ¿el scope abarca ≥2 capas del repo? | **Plan** | RFC-75 Mecanismo 2 (`scope`) |
| `C-7` | **Validación nueva** | ¿exige suites de verificación **nuevas** (no la batería canónica)? | **Plan** | `docs/VERSIONING.md:4.1` |
| `C-8` | **Findings / pending bloqueantes** | ¿genera findings o pending bloqueantes? | **Plan** | `docs/CONVENTIONS.md:Change Lifecycle — Pending decisions` (PC-1) |
| `C-9` | **Release** | ¿produce versión de protocolo? | **Plan** | `docs/VERSIONING.md:3. Versionado` |
| `C-10` | **Efectos** | ¿ejecuta efectos fuera de la frontera (`network`, `remote_git`, `install`, `destructive`, `write_outside_project`)? | **Plan** | `protocol/.agents/standards/runtime/AUTHORIZATION.md:Default frontier` |
| `C-11` | **Trazabilidad exigida** | ¿la obligación de trazabilidad (anchor + checkpoint + lineage) es exigible por el trabajo? | **Plan** | `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors…` (VC-1), GC-1, LC-1 |
| `C-12` | **Ejecución autónoma** | ¿se delega trabajo semántico a un Agent Worker (`## Delegación agentiva`)? | **Plan** | `docs/rfc/75-change-lifecycle.md:Mecanismo 5`; `.agents/policies/autonomous-orchestration.md:11` |
| `C-13` | **Basta un registro Working** | ¿una decisión o un registro en la familia `Working` alcanza? | **Note** | I-23 §11.9 |

`DESIGN_OPTION` — **Regla de decisión (determinista, sin mapeo a Level):**

```text
si algún criterio C-1 … C-12 es SÍ   → Plan
si C-13 es SÍ y C-1…C-12 son todos NO → Note
si la clasificación no es determinable → UNDETERMINED → HUMAN     (§11.4)
```

`FACT` — **Por qué ninguno de estos criterios es una nueva jerarquía de autoridad:**
(a) no asigna autoridad distinta a Plan y Note — **la autoridad es la misma** y sigue siendo el acto
humano del status; (b) no ordena fuentes; (c) no crea nivel, rango ni precedencia; (d) su efecto es
**qué artefactos y qué verificación** exige el trabajo, que es exactamente lo que ya hace la matriz de
gobernanza de RFC-75.

### 11.3 Lo que una Note **no** puede hacer

`DESIGN_OPTION` — Prohibiciones de la Note, cada una con su razón estructural:

```text
N-1  no puede contener una decisión normativa nueva            (FI-4)
N-2  no puede declarar un scope ampliado respecto de la autorización  (CHANGE_SCOPE es humano)
N-3  no puede sustituir una autorización que no existe         (PC-52)
N-4  no puede cerrarse salteando las determinaciones de impacto (stop condition)
N-5  no puede usarse cuando C-1…C-12 se cumple                 (§11.2)
N-6  no puede llevar `## Delegación agentiva` (⇒ delegación semántica ⇒ Plan, C-12)
N-7  no puede tocar `protocol/.agents/`                        (⇒ RFC-56, C-3)
```

`FACT` — **El test anti-abuso es estructural, no declarativo.** `N-1`…`N-7` no dependen de que el
autor declare el tipo: se determinan por las **rutas escritas** y por el **contenido**. Es la
mitigación del riesgo «la Nota es la vía para evitar controles» (I-23 §4.5).

### 11.4 Si no es determinable

`DESIGN_OPTION`:

```text
clasificación Plan/Note no determinable
   ⇒ el veredicto del ítem «forma del artefacto» es UNDETERMINED
   ⇒ se detiene y se pregunta al humano (formato de NO_ASSUMPTIONS: impacto + ≥2 opciones + opción libre)
   ⇒ NUNCA se elige por defecto
```

`FACT` — Caso real que cae aquí hoy: **`HD-INT-D`** (la forma exacta y el registro de la Note, §25). Mientras
esa decisión no esté cerrada, el sistema **puede derivar** «esto es `documentary`» y **no puede**
derivar «esto es una Note»; el resultado honesto es `UNDETERMINED` en ese ítem, no una elección.

### 11.5 Diferencias reales de gobernanza (la única tabla que importa)

`DESIGN_OPTION` — Las diferencias que **sí** existen, y ninguna más:

| Dimensión | Plan | Note |
|---|---|---|
| Artefacto | `docs/plans/NNN-*.md` con el template completo | forma mínima dentro de la familia `Plan` (§14.3) |
| Registro | `docs/plans/INDEX.md` (fila + serie) | fila del INDEX con `**Tipo:** Nota` |
| Anchor (VC-1) | exigible cuando hay validación registrada | **sólo si** cita una validación registrada |
| Checkpoint (GC-1) | exigible para `Closed` | exigible para `Closed` (docs-only, sin release) |
| Determinaciones de impacto | exigibles | exigibles |
| `## Delegación agentiva` | permitida | **no permitida** |
| Sección `## Derivación y premisas` | completa | **reducida** (mismas clases, sin las secciones del Plan que no existen) |
| Release | posible | **nunca** (docs-only, RFC-69) |

`FACT` — **Todas** las diferencias son de **artefactos y verificación**, ninguna de **autoridad**: en
los dos casos la autorización es el acto humano del status, y `STOP_AWAIT_PLAN_AUTHORIZATION` es el
mismo gate. **No se crea una segunda autoridad.**

---

## 12. `work_type`

### 12.1 Punto de partida verificado

`FACT` — `work_type` **no existe**: 0 ocurrencias en gobernanza, código y tests (§2.1). Lo que existe
son **tres ejes ortogonales** a la pregunta «¿qué exige este tipo de trabajo?»:

| Eje existente | Qué determina | Por qué no alcanza |
|---|---|---|
| Clase RFC-56 (A/B/C) | la **vía de autorización del payload** | **sólo existe cuando hay efecto payload**; un cambio DEV puro no tiene clase |
| Change Level (L0–L3) | el **rigor** del lifecycle | mide coordinación/superficie/impacto/release/duración, **no la naturaleza del entregable** |
| Task Profile (Protocol) | artefactos y gates obligatorios | es del **Protocol**; importarlo violaría `docs/CONVENTIONS.md:Frontera operacional (DEV)` |

### 12.2 Criterio de admisión (el test de `HD-INT-F`)

`DESIGN_OPTION` — Un tipo se admite **si y sólo si** modifica al menos una de estas cinco dimensiones.
Si no modifica ninguna, **no se crea**:

```text
admitido(tipo)  ⇔  cambia al menos una de:
   (i)   artefactos obligatorios
   (ii)  gates exigidos
   (iii) verificación exigida
   (iv)  comportamiento del registro y del cierre (documentation/roadmap impact)
```

### 12.3 El vocabulario acordado, con sus consecuencias **reales**

`DESIGN_OPTION` — Los tres tipos del encargo, cada uno con **sólo** las consecuencias que cambian una
decisión de governance, autorización, ejecución o validación. Ninguna consecuencia ornamental:

| Tipo | Definición operacional (binaria) | (i) Artefactos | (ii) Gates | (iii) Verificación | (iv) Cierre |
|---|---|---|---|---|---|
| **`mechanism`** | el trabajo modifica **comportamiento o contenido normativo**: código, contratos, estándares, políticas, el Placement Contract, el lifecycle | Plan completo + matriz de governance aplicable | C-1/C-2/C-3 cuando apliquen | batería canónica **+ suites del área**; revalidación A2 si el estado de cierre difiere | checkpoint + release si produce versión |
| **`documentary`** | el trabajo **registra, analiza, explica o corrige** documentación **sin cambiar lo que el sistema hace** | Nota o Plan ligero | C-1 sólo si hay validación registrada | batería canónica; **sin suites nuevas** | docs-only, sin release (RFC-69) |
| **`mechanical`** | el trabajo no cambia significado **ni** contenido semántico: typos, formato, links, whitespace | **ninguno** | ninguno específico | batería canónica en verde | registro en el changelog de la próxima versión |

`FACT` — **Los tres tipos no son una escala de rigor** (eso lo hace el Change Level). Son tres
**formas de gobernanza**: un `documentary` puede ser L2 (un análisis multi-área) y un `mechanism`
puede ser L1 (un cambio local en un archivo de código). Es la aplicación literal de `HD-INT-E2` extendida
a `work_type`.

### 12.4 Falsación: por qué tres y no dos ni cuatro

`DESIGN_OPTION` — Se aplicó el criterio de §12.2 a las fusiones y divisiones; el resultado es
falsable:

| Fusión / división evaluada | Veredicto | Dimensiones que difieren |
|---|---|---|
| `documentary` + `mechanical` | **no** | `mechanical` no exige registro ni anchor; `documentary` sí → difiere (i), (v) |
| `mechanism` + `documentary` | **no** | `mechanism` exige autorización de payload y release impact; `documentary` cierra sin release → difiere (i), (v) |
| `mechanism` + `mechanical` | **no** | `mechanical` no exige Plan; `mechanism` sí → difiere (i), (v) |
| dividir `mechanism` en «código» y «norma» | **no, todavía** | la diferencia ya la expresan la clase RFC-56 y el `release impact` del Change Level; crear dos tipos duplicaría esos ejes. **Reabrible con evidencia** |
| agregar `investigation` separado de `documentary` | **no, todavía** | una investigación **es** un documento (`docs/working/research/`); su diferencia la expresan los impactos de cierre. **Reabrible con evidencia** |

### 12.5 Derivación, registro y corrección humana (`HD-INT-F` + `HD-K2`)

`DESIGN_OPTION` — El valor se **deriva**, igual que el Change Level se computa:

```text
work_type = f(conjunto de rutas afectadas, naturaleza del cambio)
  · toca código o contenido normativo             → mechanism
  · sólo documenta o registra                     → documentary
  · no cambia significado                          → mechanical
```

`DESIGN_OPTION` — **Registro mínimo, y es la lectura estricta del test de `HD-INT-F`:** el valor que
**hace falta declarar** explícitamente es `documentary`, porque es el único cuyo registro (Nota vs
Plan) hoy no está determinado. `mechanism` ya se reconoce por la vía que **exige** (Plan + posible
Clase A/B) y `mechanical` por la vía del **commit directo**. Por eso:

```text
campo `**Work type:**` obligatorio en el header del Plan/Note
   ⇒ obligatorio cuando el valor es `documentary`          (cambia una decisión: forma del registro)
   ⇒ declarado también cuando es `mechanism`               (lo consume la matriz de governance, R-2 de I-23 §14.4)
   ⇒ `mechanical` no requiere Plan ni campo: su vía es el commit directo
ausencia en un artefacto legacy  ⇒ legacy, no invalidez    (RFC-75 Mecanismo 15)
```

`PC-1` (`resolución: pendiente`) — `HD-K2`: `work_type` es **derivado** cuando puede determinarse. Si resulta
`UNDETERMINED`, **el humano puede establecerlo o corregirlo**, y la corrección se registra con la
categoría `Declarado` **sobre ese campo y sólo ese** — es decir, el campo **deja de ser `Derivado`** y
pasa a `Declarado`, con su evidencia.

`FACT` — **La restricción que cierra la ambigüedad:** `HD-K2` prohíbe dos valores simultáneos del
mismo campo bajo categorías diferentes. Por eso `MK-9` (una sola categoría por campo) es el
mecanismo, y por eso un `work_type` establecido por el humano **no** puede seguir leyéndose como
`Derivado`: o es derivado (y lo produce el derivador) o es declarado (y lo establece el humano).

### 12.6 Qué el tipo **no** gobierna

`DESIGN_OPTION` — Límites explícitos:

| Límite | Razón |
|---|---|
| **No aplica al Protocol** | el Protocol tiene `Task Profile` (`trivial`/`standard`/`complex`) que determina artefactos y gates; importarlo violaría `docs/CONVENTIONS.md:Frontera operacional (DEV)` |
| **No reemplaza al Change Level** | rigor y naturaleza son ejes independientes |
| **No reemplaza a la clase RFC-56** | el tipo **no exime** de la vía de autorización del payload |
| **No es un artefacto ni una entidad** | es un valor derivado de la clasificación del Change |
| **No es una escala de rigor** | confundirlo con rigor duplicaría el Change Level |
| **No crea ni determina autoridad** | la vía de autorización la determina la **clase RFC-56** (`docs/rfc/56-governance-fast-track.md`); `authority.py:AUTHORITY_VERDICTS` sigue siendo el único veredicto de autoridad |

---

## 13. Applicable Rules

### 13.1 La pregunta y su lugar en el modelo

`DESIGN_OPTION` — La resolución responde: **¿qué reglas gobiernan este trabajo?**
**No es un mecanismo separado:** es la sub-evaluación de la resolución de contexto que produce una
parte del contexto, y su resultado **alimenta** el veredicto de derivabilidad (§7) sin sustituirlo.

### 13.2 El sujeto de la evaluación

`DESIGN_OPTION` — Se resuelve **por trabajo**, no por archivo ni por persona. El sujeto mínimo son
campos que el Change **ya declara hoy** (`.agents/workflows/change-lifecycle.md:1. Change detection and classification`):

```text
sujeto = ( origin_type , dominio(s) , work_type , Change Level , clase RFC-56 si aplica , scope declarado )
```

`FACT` — **No se crea un sujeto nuevo.** Son exactamente los campos del intake; la resolución de
reglas es la parte del intake que hoy se hace **por memoria**.

### 13.3 Fuentes consultables (conjunto cerrado)

`DESIGN_OPTION` — Las fuentes **no se inventan**: son las que `AGENTS.md:Repository layout` y
`.agents/policies/authority.md:Document discovery` ya declaran, y son **diez**:

| # | Fuente | Qué gobierna | Autoridad |
|---|---|---|---|
| `S-1` | `AGENTS.md` (raíz) | el pipeline de cambio y la política de ramas | `NORMATIVE` (instrucción DEV) |
| `S-2` | `.agents/AGENTS.md` + `.agents/workflows/` + `.agents/policies/` | la **operación**: clasificación, gates, stop conditions, frontera SAE | `NORMATIVE` operacional (no crea autoridad nueva) |
| `S-3` | `docs/CONVENTIONS.md` | convenciones de gobernanza: ciclos de status, intake, anchors, findings, pending, **y los invariantes de este Change** | `NORMATIVE` |
| `S-4` | `docs/VERSIONING.md` | versionado, changelog, tags, DoD, batería canónica | `NORMATIVE` |
| `S-5` | `docs/AGENTS.md` | taxonomía documental: naturaleza, lifecycle, identidad, referencias | `NORMATIVE` |
| `S-6` | `docs/rfc/`, `docs/adr/` | el modelo y las decisiones aceptadas | `NORMATIVE` |
| `S-7` | `docs/plans/` | autorización de implementación de **este** trabajo | `NORMATIVE` sólo para **su** Change |
| `S-8` | `docs/placement-contract.md` | ubicación de artefactos | `NORMATIVE` (Policy) |
| `S-9` | `tools/` (batería canónica) | verificación mecánica | `FACTUAL` (evidencia, **nunca** norma — `AU-4`) |
| `S-10` | `protocol/.agents/` | **sólo** cuando el trabajo tiene efecto payload, y **como data** | `NORMATIVE` del Protocol, con su vía RFC-56 |

`FACT` — El conjunto es **cerrado y enumerable**: diez entradas, nueve de ellas rutas de primer nivel
que `AGENTS.md:Repository layout` ya documenta. **No hay que inventar un registro.**

### 13.4 Los cuatro veredictos

`DESIGN_OPTION`:

| Veredicto | Significado |
|---|---|
| `APPLIES` | la fuente gobierna este trabajo y sus obligaciones se derivan de ella |
| `NOT_APPLICABLE` | la fuente existe y está en alcance, pero **no** gobierna este trabajo |
| `UNDETERMINED` | no puede decidirse si gobierna: falta la fuente, o su aplicabilidad depende de un dato ausente |
| `CONFLICT` | dos o más fuentes en alcance determinan obligaciones **incompatibles** |

`DESIGN_OPTION` — **Mapeo explícito a la derivabilidad (§7), sin vocabulario nuevo:**

| Veredicto de regla | Aporte al resultado de derivabilidad (§7.5) |
|---|---|
| `APPLIES` | el ítem tiene en esa fuente una fuente citable que lo determina |
| `NOT_APPLICABLE` | el ítem queda fuera del universo: también es una respuesta **determinada** ⇒ no impide construir el artefacto |
| `UNDETERMINED` | ⇒ `GAP` + `NEEDS_CLARIFICATION` |
| `CONFLICT` | ⇒ `ANOMALY` (nunca se elige) |

`FACT` — **«Ausencia de regla» no es un quinto veredicto.** Es la situación en que **ninguna** fuente
aplica; su comportamiento es el de `NOT_APPLICABLE` para todas, y **no habilita nada por sí misma**
(`FI-9`). Si la ausencia es de **mecanismo** (la política existe y ningún ejecutor la materializa),
se registra como `GAP` arquitectónico declarado (§13.7).

### 13.5 Orden de evaluación

`DESIGN_OPTION` — Determinista, en este orden:

```text
para cada fuente del conjunto (§13.3), en orden estable:
  1. ¿está en alcance por dominio y por clase?         NO → NOT_APPLICABLE
  2. ¿su lifecycle es vigente? (§15)                   NO (archived/deprecated) → NOT_APPLICABLE
                                                        superseded sin sucesor    → UNDETERMINED
  3. ¿declara obligaciones para este sujeto?           NO → NOT_APPLICABLE ; SÍ → APPLIES
  4. ¿falta la fuente que lo decidiría?                SÍ → UNDETERMINED
  5. ¿dos fuentes APPLIES determinan obligaciones
     incompatibles para el mismo sujeto?               SÍ → CONFLICT
```

`DESIGN_OPTION` — **Regla dura del paso 5**, tomada literalmente de la norma existente:

```text
RQ-1  CONFLICT nunca se resuelve por especificidad, novedad, jerarquía ni «la más reciente»
RQ-2  no existe jerarquía universal RFC > ADR > Plan (y NO debe crearse)
RQ-3  ante CONFLICT → protocolo de conflicto: detect → classify → escalate → human decision
RQ-4  el ejecutor CITA la fuente; nunca copia su contenido
RQ-5  si la implementación y la fuente discrepan, la fuente gobierna y el defecto de
      implementación se escala  (PC-75)
RQ-6  un Plan es fuente de reglas sólo para SU Change; nunca para otro trabajo  (AU-5)
RQ-7  protocol/.agents/ nunca se lee como reglas de DEV  (AGENTS.md)
```

`FACT` — `RQ-2` **no es una opinión de este documento**: está decidida en cinco lugares
(`.agents/policies/authority.md:Conflict protocol`; `docs/rfc/75-change-lifecycle.md:Mecanismo 10 — Authority / Conflict Resolution`;
`.agents/policies/supervised-autonomous-execution.md:5`; `docs/placement-contract.md:22. Enforcement`;
`protocol/.agents/standards/context/RESOLUTION_UNRESOLVABLE_CONFLICTS.md` + `…/orchestration/DECISIONS.md:D3`).

### 13.6 Qué es mecánico y qué requiere interpretación

`DESIGN_OPTION` — La parte **mecánica** es el **enrutamiento** (qué fuentes están en alcance por
dominio y por ruta) y la **detección de conflicto por cita** (dos fuentes `APPLIES` cuyo contenido
citado es incompatible). La parte que requiere **interpretación** es decidir si una fuente **prosa**
«declara obligaciones para este sujeto».

```text
MECÁNICO  (puede ser checker):
   · el conjunto de fuentes y su ruta             (tabla de rutas)
   · el alcance por dominio (prefijo de path → capa)
   · el lifecycle declarado de cada fuente        (lectura de campo, §15)
   · la EXISTENCIA de la cita `ruta:sección`      (ya lo hace `tools/check_plan_citations.py`)
   · la detección de que dos fuentes APPLIES citan obligaciones distintas  (comparación de las citas,
     no de su significado)

INTERPRETACIÓN (humano o agente, y SIEMPRE declarada):
   · si una fuente en prosa «declara obligaciones para este sujeto»
   · si dos obligaciones citadas son «incompatibles»
   · el veredicto final `DERIVED` de un ítem cuya fuente es prosa
```

`FACT` — **Consecuencia honesta:** el determinismo del veredicto es **menor** que el del Placement
Contract, porque sus fuentes son diez y de naturalezas distintas (tablas, prosa, código). El diseño lo
**declara** en lugar de prometer una determinación que la norma no da: los veredictos son
deterministas cuando la fuente declara su alcance explícitamente (p. ej. `docs/placement-contract.md:2`
«This contract applies to every artifact…») y son `UNDETERMINED` cuando no lo declara.
**No se inventa determinismo donde la norma no lo da.**

### 13.7 El caso «la política existe y ningún ejecutor la materializa」

`DESIGN_OPTION`:

```text
fuente APPLIES con enforcement declarado "documented" y ningún ejecutor que la materialice
   → se registra como GAP ARQUITECTÓNICO DECLARADO
   → el trabajo NO queda bloqueado por ello
   → la fuente SIGUE gobernando (es normativa); su verificación es humana
```

`FACT` — El vocabulario exacto ya existe: `GAP` es «required evidence absent / not verifiable» y es
**advisory, no bloqueante** (`.agents/workflows/change-lifecycle.md:10`), y el Mecanismo 14 declara
que el output de un checker es evidencia factual, no autoridad
(`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`). El Protocol ya marca el grado de
enforcement en el front matter de sus contratos (`enforcement = "documented"`), lo que da precedente
de cómo declararlo.

`FACT` — **Ejemplo real y no abstracto:** la matriz de governance de
`docs/rfc/75-change-lifecycle.md:Mecanismo 5` **gobierna** (es normativa) y **ningún ejecutor la
materializa** (grep de sus valores en `tools/` y `runtime/`: 0 coincidencias). Hoy, un trabajo
`mechanism` está gobernado por una matriz que sólo existe en prosa. Eso es un `GAP`, y este diseño lo
**declara** en lugar de inventar que no aplica. El Change (§23, `D-6`) lo cierra ejecutándola.

### 13.8 Cómo se detecta drift entre fuente normativa y realización mecánica

`DESIGN_OPTION` — Réplica del patrón ya probado para placement, que es la respuesta a «cómo se hace
esto sin crear una segunda fuente de verdad»:

```text
FUENTE NORMATIVA         docs/ + .agents/                     (texto; nadie lo duplica)
        ↓
REALIZACIÓN DERIVADA     tabla read-only de rutas de fuentes y enrutamiento por sujeto,
                         que CITA y NO COPIA
        ↓
GUARDA DE DIVERGENCIA    un test que falla si la tabla y las fuentes se desalinean
        ↓
CONSUMIDOR               la derivabilidad (§7) y el host
        ↓
DESACUERDO               la fuente gobierna; se escala; nunca se reinterpreta  (PC-75)
```

`FACT` — Precedente literal de cada eslabón: `docs/placement-contract.md:22. Enforcement` (`PC-72.1`,
`PC-75`, `PC-76` — invariantes `E-1`…`E-8`), `runtime/placement/rules.py`
(«does **not** own the placement rules: it realizes the rule table»),
`tests/test_placement_contract_drift.py` («not a second source of truth. If either side changes
without the other, these tests fail loudly»).

`DESIGN_OPTION` — **La guarda de divergencia concreta que el Change debe implementar** (§23 `D-7`):

```text
1. la tabla declara, por fuente: (ruta, capa(s), dominio, ruta:sección, vigencia declarada)
2. el test verifica que:
   a. toda ruta declarada EXISTE
   b. toda `ruta:sección` citada RESUELVE
   c. no hay fuente del conjunto §13.3 ausente de la tabla
   d. no hay ruta en la tabla que no pertenezca al conjunto §13.3
3. si (a)…(d) fallan → el test falla; la fuente gobierna y el defecto se ESCALA, no se reinterpreta
```

`FACT` — **Esto no es un checker semántico.** Verifica **existencia, resolución y cobertura de
rutas**: forma, no significado. No decide si una fuente «aplica» ni si dos obligaciones son
incompatibles. Es la diferencia exacta que `.agents/policies/validation-closure.md:5.1 Enforcement`
exige respetar.

### 13.9 Lo que la resolución **no** debe hacer

`DESIGN_OPTION`:

| Prohibición | Razón |
|---|---|
| Crear un registry de reglas, un índice global o una base de datos | `PC-75`; `.agents/AGENTS.md:Fundamental operating rules 8` |
| Reescribir el contenido de las fuentes en una forma propia | convertiría al ejecutor en segunda fuente normativa (`PC-75`) |
| Establecer jerarquía entre RFC, ADR y Plan | `ADR-16`; `RQ-2` |
| Tratar un Plan como fuente de reglas para **otro** trabajo | `AU-5`; `RQ-6` |
| Leer `protocol/.agents/` como reglas de DEV | `RQ-7`; `AGENTS.md` |
| Decidir por sí mismo que una fuente «ya no aplica» | la vigencia es una **declaración con autoridad** (§15.4), no una inferencia |
| Detectar y propagar impacto mecánicamente | **diferido**: RFC-68 Fase 2, con sus gates (§26) |

---

## 14. Plan/Note Contract

### 14.1 Contrato común del artefacto gobernable antes de autorización

`DESIGN_OPTION` — El artefacto gobernable es **uno solo**, con **una sola** situación previa a la
autorización (`HD-INT-J`), y con las cuatro categorías de §9.4 explícitas por propiedad:

```text
ARTEFACTO GOBERNABLE (Plan o Note)
  identidad        el número/identidad del artefacto (mecanismo existente; sin primitive nueva)
  status inicial   `Aprobado para redacción`   ← la situación `proposed` de HD-INT-J, sin estado nuevo
  forma            Plan completo | Nota (§11.5)
  clasificación    Change Level (existente) + `**Work type:**` (nuevo, §12.5) + clase RFC-56 si aplica
  registro         `## Derivación y premisas` (§8.2) — la procedencia de la derivación `D`
  categorías       cada propiedad del artefacto tiene EXACTAMENTE UNA categoría (§9.4)
  autorización     NO la posee: la recibe por acto humano posterior (§14.2)
```

`FACT` — **`proposed` no es un estado nuevo.** Su materialización existente es `Aprobado para
redacción`, que es el estado inicial que el template ya declara (`docs/plans/_TEMPLATE.md:header`) y
que `runtime/orchestrator/derivation.py:derive_next_action (regla 1)` ya detiene con
`STOP_AWAIT_PLAN_AUTHORIZATION`. `HD-INT-J` no introduce un estado: usa el que ya existe. **No se crea
una segunda state machine.**

### 14.2 Cómo se produce la autorización desde Plan y desde Note

`DESIGN_OPTION` — **Una sola autoridad, dos formas de artefacto:**

| | Desde `Plan` | Desde `Note` |
|---|---|---|
| Estado previo | `Aprobado para redacción` | `Aprobado para redacción` |
| Acto humano | el mantenedor lleva el `**Status:**` a `Aprobado para ejecución` | **idéntico** |
| Evidencia | el status en el artefacto + (si aplica) el registro de la decisión | ídem |
| Mecanismo que la consume | `runtime/orchestrator/derivation.py:derive_next_action (regla 1)` + `ChangeObservation.authorized_for_execution` | **idéntico** |
| Autoridad que la habilita | `DECISION` del mantenedor (`ADR-16`) | **idéntica** |

`FACT` — **No se crea una nueva autoridad ni un nuevo mecanismo de autorización.** `APPROVE_PLAN` y
`CHANGE_SCOPE` siguen en `FORBIDDEN_ACTIONS` (`runtime/orchestrator/authority.py`), y
`.agents/policies/supervised-autonomous-execution.md:8. Human boundary` sigue declarando que el humano
es la autoridad exclusiva para autorizar scope y sus cambios.

`FACT` — **Caso real ya resuelto por el repositorio, y que este diseño debe respetar:** el **Plan 136**
fue autorizado **por directiva** con el artefacto todavía en `Aprobado para redacción`; el repositorio
**no** lo leyó como un cambio de contenido, sino como una decisión humana que hubo que registrar
(`<PLAN-136>:F-5`, `<PLAN-136>:PC-1`). El diseño **conserva** ese comportamiento: la autorización es
un acto humano separado del texto, y una discrepancia entre el artefacto y la decisión se **registra**,
no se infiere.

### 14.3 Forma mínima de la Note (condicionada a `HD-INT-D` = Opción A)

`PC-1:HD-INT-D` (`resolución: adoptada`, 2026-10-02, Opción A) — **Dónde vive y cómo se registra la Note.** Es la única decisión que
bloquea la ejecución del Change, y **no es inferible**: `docs/placement-contract.md:6. Namespace
selection` (`PC-20`) declara literalmente «Adding a family to §6 is a governance change, not an agent
action», y `PC-10` prohíbe crear un namespace.

`DESIGN_OPTION` — Las tres opciones, con su impacto declarado:

| Opción | Descripción | A favor | En contra | Placement |
|---|---|---|---|---|
| **A (recomendada)** | la Note es una **forma** dentro de la familia `Plan`: vive en `docs/plans/`, nace del template con las secciones mínimas, se registra en `docs/plans/INDEX.md`, y su header declara `**Tipo:** Nota` | (a) usa la familia **ya declarada** en `docs/placement-contract.md:6` ⇒ **no** crea namespace ni familia, respeta `PC-10`/`PC-20`; (b) hereda **todos** los mecanismos existentes (status cycle, anchor, checkpoint, INDEX, C-1…C-3); (c) los checkers existentes ya la cubren; (d) explica por qué `docs/plans/94-…:9.2` escribe «Plan/Nota» como una sola familia | roza la letra de `HD-INT-D` («una Nota y no un Plan»); requiere que `**Tipo:** Nota` sea reconocido | `PLACE` — `docs/plans/` |
| **B** | la Note vive junto a su artefacto, dentro de la familia `Working analysis` (`docs/working/{audits,research,proposals}/`) | (a) es exactamente donde caen hoy los artefactos huérfanos; (b) es un `PLACE` inmediato sin tocar el contrato; (c) el INDEX de la carpeta la registra | (a) una familia **no normativa** pasaría a alojar un registro de gobernanza; (b) pierde el status cycle, el anchor y los gates C-1…C-3 ⇒ el cierre pierde soporte mecánico | `PLACE` — `docs/working/…` |
| **C** | familia nueva `docs/notes/` | máxima claridad de tipo | (a) viola `HD-INT-D` («no un segundo sistema paralelo»); (b) `PC-10`/`PC-20` exigen enmendar el contrato ⇒ **fuera del alcance de este Change**; (c) crea un cuarto espacio de identidad | `STOP (NEW FAMILY)` |

`DESIGN_OPTION` — **Recomendación: A**, con la divergencia declarada en voz alta: A interpreta «una
Nota y no un Plan» como **«no la ceremonia de un Plan completo»**, no como «un artefacto de otra
familia». Es la única opción que satisface simultáneamente las condiciones de `HD-INT-D` **juntas** —
mínima, registrable, trazable, explícita en autoridad/intención/scope/evidencia, integrada con la
gobernanza existente y no un segundo sistema— sin crear familia, namespace, identidad ni mecanismo.

`FACT` — **Consecuencia de no decidir `HD-INT-D`:** la elección Plan/Note queda `UNDETERMINED` para todo
trabajo `documentary` (§11.4), y el Change **no puede cerrarse**. Es una decisión de gobernanza con
dueño humano; este documento **no la resuelve**.

### 14.4 Contenido obligatorio de la Note (una vez decidida la forma)

`DESIGN_OPTION` — Si `HD-INT-D` = A, la Note declara como mínimo:

| # | Campo | Por qué es obligatorio |
|---|---|---|
| 1 | Identidad | identidad del artefacto + el commit; **no** hay serie numerada de Notas (no se crea un tercer espacio de identidad) |
| 2 | Fecha | trazabilidad temporal |
| 3 | `**Tipo:** Nota` | hace la forma legible por máquina y por humano |
| 4 | `**Origen:**` | `direct maintainer action` (`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`) |
| 5 | `**Work type:**` | `documentary` `\|` `mechanical` (§12.5) |
| 6 | `**Change Level:**` | la clasificación que el intake exige |
| 7 | **Autorización** | quién la autorizó y la referencia a la instrucción (la autorización es un hecho registrable: `PC-52`) |
| 8 | **Intención** | una frase: qué se quiso hacer |
| 9 | **Scope declarado** | el conjunto **completo** de rutas escritas (habilita la verificación de frontera) |
| 10 | `## Derivación y premisas` | el registro de procedencia (§8.2), en forma reducida |
| 11 | **Acción realizada + evidencia** | qué se hizo y el hecho que lo prueba |
| 12 | `## Validation anchor` | **sólo si** cita una validación registrada (VC-1) |
| 13 | `## Checkpoint / cierre` | las dos determinaciones de impacto, con `REQUIRED`/`NOT_REQUIRED`/`DEFERRED` y su razón — **nunca en blanco** |

### 14.5 Invariantes del artefacto gobernable

`DESIGN_OPTION`:

```text
PD-1  el artefacto nace NO AUTORIZADO (`Aprobado para redacción`)
PD-2  la derivación NO escribe el status de autorización
PD-3  cada parte `Confirmado` se registra como propuesta hasta su confirmación
PD-4  una parte Forbidden-to-infer ausente DETIENE la derivación (no se completa por default)
PD-5  el artefacto CITA sus fuentes; no las reescribe
PD-6  el artefacto no cambia de granularidad sin pasar por §17 (cohesión del Change)
PD-7  `premises(D)` es obligatorio para una derivación completa  (HD-K3)
PD-8  una propiedad tiene EXACTAMENTE UNA categoría  (MK-9)
PD-9  una re-derivación NO elimina una declaración humana  (MK-3)
```

### 14.6 Por qué no se necesita un artefacto intermedio

`DESIGN_OPTION` — Se evaluó proponer un «Plan propuesto» separado del Plan. **Se descarta:** el ciclo
de status ya tiene el estado inicial que expresa exactamente «redactado, no ejecutado», y crear un
artefacto intermedio obligaría a declarar su placement (familia nueva ⇒ `STOP (NEW FAMILY)`), su
relación con el Plan y su ciclo — **tres mecanismos nuevos** para expresar algo que un status ya
expresa. Es la aplicación del principio de reutilización del encargo.

---

## 15. Lifecycle

### 15.1 Integración del vocabulario (existente, no reemplazado)

`FACT` — El vocabulario es el de `docs/AGENTS.md:Lifecycle` y **no se reemplaza**:
`active` · `archived` · `superseded` · `deprecated`, combinables (`superseded ∧ archived`).
Este diseño **no** encontró semántica necesaria que ese vocabulario no pueda expresar, y por eso no
crea un valor nuevo.

### 15.2 Lifecycle ≠ status (regla de no fusión)

`DESIGN_OPTION` — El punto más delicado: no crear una segunda taxonomía frente a los ciclos de status.

| Dimensión | Qué responde | Valores | Fuente |
|---|---|---|---|
| **status** (de la clase) | ¿en qué punto de su ciclo propio está el artefacto? | RFC: `Proposal`→`Accepted`→`Superseded` · Plan: `Aprobado *`→`Executed`→`Superseded` · ADR: `Proposal`→`Accepted`→`Superseded` | `docs/CONVENTIONS.md:Convenciones`; `docs/VERSIONING.md:7` |
| **lifecycle (vigencia)** | ¿su contenido todavía **rige**? | `active` · `archived` · `superseded` · `deprecated` | `docs/AGENTS.md:Lifecycle` |

```text
status     = ciclo de vida del artefacto COMO ARTEFACTO  (documental)
lifecycle  = vigencia semántica de su CONTENIDO          (normativo)
lifecycle ≠ status ; ninguno se deriva del otro
```

`FACT` — Por qué son distintos y ambos necesarios, con evidencia del corpus: **80/80** RFCs están
`Accepted` y sin embargo no todas **rigen** (el corpus registra supersesiones reales en prosa:
«superado por RFC-68», banners `⚠ Enmienda pendiente`). Un solo campo no puede expresar «aceptada y
todavía vigente» frente a «aceptada y ya no vigente». Y a la inversa: un Plan `Executed` **sí** suele
seguir describiendo lo que se hizo (es traza), pero su contenido normativo puede haber dejado de aplicar.

### 15.3 `Superseded` con sustituto y sin sustituto (`HD-INT-B`, ya decidido)

`PC-1` (`resolución: adoptada`, 2026-10-02) — `HD-INT-B`: `Superseded` puede representar (1) sustitución por otro artefacto **o**
(2) retiro por una razón aunque no exista reemplazo. No se introduce un nuevo lifecycle state.
`Abandoned` permanece como **condición derivada**, no como nuevo estado primario.

`DESIGN_OPTION` — Representación mínima, **sin estado nuevo y sin máquina nueva**:

```text
SUPERSEDED CON SUSTITUTO
  **Status:** Superseded
  **Superseded por:** <RFC-NN | ADR-N | plan NN | ruta>          ← campo requerido hoy

SUPERSEDED SIN SUSTITUTO (el trabajo dejó de aplicar)
  **Status:** Superseded
  **Superseded por:** —
  **Motivo de retiro:** <razón explícita y verificable>          ← campo mínimo nuevo
  **Lifecycle:** superseded
```

`DESIGN_OPTION` — Relación con la condición derivada de RFC-75, explícita:

```text
RFC-75:  Abandoned = Plan Superseded con motivo
Modelo:  Abandoned ⇔ (status = Superseded) ∧ (sucesor ausente) ∧ (motivo presente)
```

`FACT` — **No se crea el estado `Abandoned`:** el repositorio ya tiene la **condición derivada**
`Abandoned` en `docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`, y `HD-INT-B` prohíbe crear un estado
nuevo. Lo que este diseño agrega es que la condición **pase a ser derivable** de un campo, en lugar de
vivir en prosa. `T-1` (§2.2) queda resuelto por decisión humana, y el bloqueo que registraron los
planes 137 y 140 deja de ser inevitable.

### 15.4 Materialización progresiva (sin migrar el corpus)

`PC-1` (`resolución: adoptada`, 2026-10-02) — `HD-INT-C`: migración progresiva; **no** migración masiva del corpus histórico.

`DESIGN_OPTION` — El mecanismo, con su cláusula de compatibilidad:

| Pieza | Exigencia | Por qué |
|---|---|---|
| Dónde vive | en el **header del propio artefacto**, junto a su status | `docs/CONVENTIONS.md:Convenciones` (statuses en el header); el artefacto es la fuente |
| Default | **ausencia ⇒ `active`** | no se escriben 153 headers para decir «vigente»; `Mecanismo 15`: la ausencia de campos nuevos es legacy, **no** invalidez |
| Cuándo se escribe | sólo cuando el valor **no** es `active` | consecuencia de coste deliberada: **0 ediciones** al corpus histórico |
| Alcance del enforcement | **hacia adelante** (artefactos creados después de la convención) | sin esto la guarda quedaría roja sobre 153 planes y 80 RFCs, y forzaría a tocar historia |
| Quién la cambia | el owner del artefacto, con **decisión humana** cuando cambia vigencia normativa | `ADR-16 AU-3`; `MODIFY_CLOSED_ARTIFACT` es `FORBIDDEN` para el host |
| Evidencia requerida | referencia al sucesor, **o** el motivo, **o** la decisión que congela | RFC-46; PC-1 |

`DESIGN_OPTION` — Matriz de transiciones (ninguna autónoma del agente):

| Transición | Autoridad | Evidencia |
|---|---|---|
| (ausencia) → `active` | implícita | ninguna (default) |
| `active` → `archived` | mantenedor o el Change que la posee | decisión registrada o regla de clase (`docs/AGENTS.md:Folder → class map`) |
| `active` → `superseded` (con sucesor) | el Change que produce el sucesor | referencia al sucesor |
| `active` → `superseded` (sin sucesor) | **mantenedor** | el motivo explícito (`Motivo de retiro`) |
| `active` → `deprecated` | **mantenedor** | declaración de fuera de uso, sin reemplazo |
| cualquier → `active` (reactivación) | **mantenedor** | decisión registrada |
| `deprecated` → eliminación | mantenedor, con la regla explícita | la transición de deprecación previa |
| **cualquier transición** | **nunca el agente** | `MODIFY_CLOSED_ARTIFACT` ∈ `FORBIDDEN_ACTIONS` |

`DESIGN_OPTION` — Invariante de honestidad, para que el filtro de vigencia no oculte conocimiento:

```text
LV-1  superseded/archived/deprecated NUNCA se borran ni se reescriben   (RFC-46)
LV-2  no vigente ≠ inexistente: la lectura histórica conserva todo
LV-3  no vigente ≠ falso: el artefacto decía lo correcto para su estado
LV-4  un artefacto no vigente nunca es fuente normativa de trabajo nuevo,
      pero SIEMPRE es evidencia citable
```

### 15.5 Cómo el INDEX obtiene el lifecycle sin una segunda fuente manual

`PC-1` (`resolución: adoptada`, 2026-10-02) — `HD-INT-I`: la información de lifecycle que deba aparecer en `INDEX` debe derivarse
automáticamente. **No** mantener un segundo estado manual independiente.

`DESIGN_OPTION` — El mecanismo:

```text
FUENTE      el header del artefacto (declaración del owner)                    NORMATIVE
   ↓
VISTA       una columna de vigencia en el INDEX, DERIVADA del header           DESCRIPTIVE
   ↓
VERIFICACIÓN  la coherencia columna ↔ header se verifica por FORMA (mecánico),
              igual que hoy `tools/check_plan_structure.py` verifica que todo plan
              numerado tenga fila
   ↓
REGLA DURA  el INDEX sigue sin ser autoridad (AU-4): la columna NO se edita a mano
              como fuente; se deriva
```

`FACT` — **Por qué no puede vivir sólo en el INDEX (evaluado y descartado):** el INDEX es
`DESCRIPTIVE` y «nunca se convierte en autoridad por existir» (`AU-4`;
`.agents/policies/authority.md:Authority classes`). Poner la **fuente de verdad** de la vigencia en un
registro descriptivo **invertiría la jerarquía** que `ADR-16` fija.

`FACT` — **Precedente de forma:** `docs/CONVENTIONS.md:Change Lifecycle — Serie e identidad derivada`
ya declara el patrón exacto («la serie es identidad **derivada**: `Serie(RFC)` = declaración `Serie:`
del header; … los INDEX la reflejan como vista descriptiva, nunca autoritativa»). Este diseño
**reutiliza** ese patrón, no lo inventa.

`HYPOTHESIS` — **Nota de coste:** la columna derivada requiere que la derivación sea **ejecutable**
(el Change la implementa como parte de `D-8`, §23). Si `HD-M4` (§25) decide no agregar la columna, el
lifecycle sigue siendo legible **por artefacto** (`**Lifecycle:**` en el header) y la navegación
pierde una comodidad, no una capacidad. **No es bloqueante.**

### 15.6 Cómo afecta la derivación

`DESIGN_OPTION`:

| Etapa | Efecto del lifecycle |
|---|---|
| Resolución de contexto | el lifecycle **filtra** el universo de fuentes: `active` son candidatas normativas; `archived`/`superseded`/`deprecated` son evidencia e historia, no norma vigente |
| Derivabilidad | si dos fuentes `active` se contradicen → `UNDETERMINED / CONFLICT` (paso 2). Si la única fuente que determina el ítem está `superseded`, el ítem **no** es derivable de ella: se busca el sucesor; si no hay sucesor y hay motivo, el ítem pasa a `NOT_DERIVABLE` con la decisión requerida |
| Construcción del artefacto | el artefacto cita la fuente **vigente** y registra la `superseded` sólo como **provenance** (columna `Vigente` de `premises(D)`) |
| Resolución de reglas | incluye `NOT_APPLICABLE` cuando la única fuente aplicable está `deprecated`, y `UNDETERMINED` cuando la única fuente aplicable está `superseded` sin sucesor |

---

## 16. SAE Integration

### 16.1 Dónde termina el mecanismo nuevo y dónde empieza SAE

`DESIGN_OPTION` — El corte es **exacto** y es una frontera temporal ya declarada y testeada:

```text
════════════════════ MECANISMO NUEVO (pre-autorización) ════════════════════
Intent → Context → Intent Confidence → Derivability → Work Type →
Applicable Rules → Plan/Note `proposed` → (modificación humana R-1…R-5 + re-derivación)
   · el host NO participa: es el derivador el que actúa
   · no hay delegación, no hay worker, no hay escritura de ejecución
   · la única escritura es el artefacto `proposed` y su registro de premisas
        ↓
[humano] AUTORIZACIÓN  ← el acto: `**Status:** Aprobado para ejecución`
        ↓
════════════════════ SAE (post-autorización; INTACTO) ══════════════════════
observe → derive_next_action → _apply_autonomy_gate → delegación →
   pin de la proyección de autorización (PRIMERA iteración autorizada)
   → execute → verify → correct/revalidate → continue → stop
```

`FACT` — El `pin` ocurre en la **primera iteración autorizada**, no antes
(`runtime/orchestrator/host.py:_apply_autonomy_gate`, `_pinned_autonomy_projection`), y lo que se
autoriza es lo que existe **al** autorizar. Por eso la modificación humana pre-autorización queda
**absorbida por la autorización por construcción**, y eso es correcto: no hay nada que comparar antes
del `pin` (`authorization_drift(None, …)` lo declara).

### 16.2 Lo que **no** cambia en SAE (enumeración explícita)

`DESIGN_OPTION` — Es la garantía de que el modelo no amplía nada:

```text
SAE-1  SAE sigue consumiendo un Plan/Note AUTORIZADO; el modelo no le da otro insumo
SAE-2  el envelope sigue derivándose de declaraciones que el artefacto ya posee (SAE §3)
SAE-3  el conjunto COMPLETO de escrituras se sigue verificando antes de delegar (SAE §1.3)
SAE-4  el checkpoint de autorización y la NO RETROACTIVIDAD no cambian (SAE §1.2)
SAE-5  no se crea ningún estado, entidad, registry ni métrica nueva (SAE §12)
SAE-6  release/promoción/tag siguen FORBIDDEN para el host (SAE §5)
SAE-7  la frontera humana de SAE §8 no se modifica en ningún punto
SAE-8  `STOP_SCOPE_VIOLATION`, `STOP_AUTHORITY_REQUIRED`, `STOP_FORBIDDEN_AUTONOMY`,
       `STOP_UNCLASSIFIABLE_ACTION` y `STOP_NO_AUTHORIZED_WORK` siguen siendo los stops de la frontera
SAE-9  el agente NO obtiene capacidad de ampliar Scope (SAE §1.4; `<PLAN-138>:PC-2` deferred)
```

`FACT` — `authorization_drift` conserva las dos mitades de la comparación (`contract` y `scope`),
porque fallan distinto: reescribir `Task` o revocar el status **falsifica** el contrato, mientras que
ampliar `Scope` es un cambio real de lo autorizado. **Este diseño no toca ninguna de las dos.**

### 16.3 Los dos cambios mínimos en el runtime

`DESIGN_OPTION` — El modelo es consumible por SAE con **dos** cambios, y **ninguno toca la lógica del
host**:

| Cambio | Qué es | Por qué es el mínimo |
|---|---|---|
| `R-1` | el host **consume** los campos nuevos del artefacto (`**Work type:**`; el lifecycle declarado de las fuentes citadas) en la `ChangeObservation` | son datos que el artefacto declara; el host **ya** parsea header y campos (`runtime/orchestrator/observation.py`) |
| `R-2` | la derivación **ejecuta** la matriz de governance aplicable en lugar de tratarla como prosa | hoy la matriz no tiene ejecutor; es el `GAP` de §13.7 y es lo que hace que `work_type` sea operacional y no una etiqueta |

`DESIGN_OPTION` — **Lo que NO hace falta:** una fase nueva en la máquina de estados del Orchestrator,
un `next_state`, un cursor, un store nuevo o un modo nuevo. La derivación sigue siendo una **función
pura** de la observación (`runtime/orchestrator/derivation.py`: «Nothing is persisted here: there is no
`next_state`, no cursor and no second representation of the change»).

### 16.4 Los boundaries humanos

`DESIGN_OPTION` — Boundaries, con su disparador y su evidencia, distinguiendo los que **ya existen** de
los **nuevos**:

| # | Boundary | Disparador | Evidencia que se registra | Estado |
|---|---|---|---|---|
| `HB-1` | Autorización del artefacto | artefacto derivado propuesto | la autorización y su referencia; `PC-52` | ya existe |
| `HB-2` | **Aclaración** | `UNDETERMINED / MISSING` | el formato de `NO_ASSUMPTIONS` (impacto + ≥2 opciones + opción libre) | **nuevo** (clasificación) |
| `HB-3` | **Resolución de conflicto** | `UNDETERMINED / CONFLICT` | fuentes A y B citadas + el punto exacto de incompatibilidad + impacto | **nuevo** (clasificación) |
| `HB-4` | **Decisión normativa / de autoridad** | `NOT_DERIVABLE` | qué decisión, quién la posee, qué la bloquea | **nuevo** (clasificación) |
| `HB-5` | Cambio de scope / autoridad | al ejecutar o al descubrir | `NA-1`/`NA-5`; SAE §1.4 | ya existe |
| `HB-6` | Aceptación / rechazo del resultado | al cerrar | `CL-8`; `ADR-16 AU-3` | ya existe |
| `HB-7` | Release / promoción / tag | si el Change produce versión | `FORBIDDEN` para el host | ya existe |
| `HB-8` | Resolución de un finding | finding abierto | `CL-8`; el host detecta, no resuelve | ya existe |
| `HB-9` | ADR-worthiness | decisión persistente | `AU-6` (juicio humano) | ya existe |

`FACT` — `HB-2`/`HB-3`/`HB-4` **no son stop conditions nuevas**: son la clasificación de **por qué**
se detiene, que hoy se pierde (un pedido por falta de información y una contradicción normativa
producen hoy el mismo registro). El mecanismo de detención sigue siendo el existente
(`REQUIRES_HUMAN` + el reporte con evidencia).

### 16.5 Cambio de granularidad al ejecutar

`FACT` — Es el `GAP` `G-8` y tiene solución existente, no una nueva:

`DESIGN_OPTION` — Los disparadores de §17.4 (nueva unidad de autorización) **ya están implementados**
como comportamiento o como stop conditions:
- `NA-4` (un finding que requiere autoridad que el Change no tiene) y `NA-7` (una obligación cuyo
  artefacto está fuera del scope) **ya están implementados**
  (`.agents/policies/supervised-autonomous-execution.md:6`, `:6.1`, `:9`);
- `NA-1`, `NA-2`, `NA-3`, `NA-5`, `NA-6` **ya están implementados** como stop conditions (`:5`).

Lo que el Change agrega es la **declaración** de que esos disparadores son también el **criterio de
granularidad al proponer** trabajo, no sólo al ejecutarlo.

---

## 17. Enforcement

### 17.1 Regla por regla: qué exige cada una

`DESIGN_OPTION` — Para cada regla nueva, el tipo de enforcement requerido. **Ninguna se implementa en
este trabajo.**

| # | Regla | runtime | checker | test | doc | derivation logic | host | CLI | workflow | índice derivado |
|---|---|---|---|---|---|---|---|---|---|---|
| `E-1` | Veredicto de derivabilidad + subcaso + su registro (`INV-1`) | — | — | — | sí | **sí** | — | — | sí | — |
| `E-2` | `premises(D)` obligatorio con sus ocho clases (`INV-2`) | — | **sí** (forma: sección presente cuando hay derivación) | sí | sí | sí | — | — | sí | — |
| `E-3` | Una sola categoría por campo (`INV-3`) | — | **sí** (forma: ningún campo con dos categorías) | sí | sí | — | — | — | — | — |
| `E-4` | Prohibición de eliminar declaración humana en re-derivación (`INV-4`) | parcial (escritor) | sí (forma: elementos `Declarado` presentes) | sí | sí | — | — | — | — | — |
| `E-5` | `work_type` derivado + campo donde cambia una decisión (`INV-5`) | — | sí (enum de 3 valores) | sí | sí | **sí** | **sí** (consume) | — | sí | — |
| `E-6` | Vigencia materializada + default `active` + legacy | — | **sí** (enum + `Superseded` sin sucesor ⇒ motivo) | sí | sí | — | — | — | — | **sí** (columna) |
| `E-7` | Conjunto de fuentes de §13.3 + guarda de divergencia | — | **sí** (rutas existen, citas resuelven, cobertura) | sí | sí | sí | — | — | — | — |
| `E-8` | Plan/Note por criterios + `UNDETERMINED → HUMAN` | — | sí (forma: `**Tipo:**` dentro del enum) | sí | sí | **sí** | — | — | sí | — |
| `E-9` | Matriz de governance ejecutada (no prosa) | — | — | sí | — | **sí** | **sí** | — | — | — |
| `E-10` | Cohesión del Change (5 cláusulas) al proponer | — | — | — | sí | **sí** | — | — | sí | — |
| `E-11` | `R-1`…`R-5` + `MK-1`…`MK-9` | parcial | forma | **sí** | sí | **sí** | — | — | sí | — |

`DESIGN_OPTION` — Lectura de la tabla, que es la parte que el encargo pide cuidar:

- **Lo que puede hacerse mecánico** es la **forma**: presencia de la sección de premisas, enum de
  `work_type`, enum del campo de vigencia, `Superseded` sin sucesor exige motivo, cobertura del
  conjunto de fuentes, coherencia de la columna derivada del INDEX, `**Tipo:**` dentro del enum. Nada
  de eso interpreta prosa.
- **Lo que NO puede hacerse mecánico** es el **significado**: si una fuente «aplica», si dos
  obligaciones son incompatibles, si `premises(D)` cambió por una reescritura de prosa, si una
  modificación «cambió el significado». Eso queda como **decisión del derivador con evidencia
  declarada**, y donde no alcanza → `UNDETERMINED`.
- **La frontera es la que el repositorio ya declaró:** `.agents/policies/validation-closure.md:5.1
  Enforcement` — «The obligation is governance, not a semantic validation. **No checker interprets
  prose** or decides whether a document is up to date» — y `:5.2` lo repite.

### 17.2 Reglas que se vuelven mecánicas sin interpretar prosa

`DESIGN_OPTION` — Las cinco más valiosas, por orden de retorno:

1. **`Superseded` sin sucesor exige `Motivo de retiro`** (`E-6`). Cierra `T-1` con una verificación
   puramente estructural. *Nota:* es exactamente el hallazgo residual de §25.
2. **Cobertura del conjunto de fuentes + guarda de divergencia** (`E-7`). Replica
   `tests/test_placement_contract_drift.py`; detecta una fuente que se mueve o desaparece.
3. **Enum de `work_type` y coherencia con las rutas escritas** (`E-5`). `mechanism` con sólo `docs/`
   tocados, o `documentary` con código tocado, es detectable por **rutas**, no por prosa.
4. **Sección `## Derivación y premisas` presente cuando el artefacto declara una derivación** (`E-2`).
   Es la diferencia entre `R-5` como excepción y `R-5` como regla (I-23-HDK §13.1).
5. **Coherencia columna ↔ header del INDEX** (`E-6`). Hoy el espejo se verifica por **substring del
   nombre** (`tools/check_plan_structure.py`); la columna se puede verificar por **valor derivado**.

### 17.3 Lo que **no** se convierte en checker

`DESIGN_OPTION` — Explícitamente, para que no reaparezca:

```text
NO CHECKER PARA:
  · decidir si una modificación humana «cambió el significado»          (A-22 de I-23 §16)
  · decidir si un documento «era un Plan» o «debía ser una Nota»        (validation-closure §5.1)
  · decidir si un documento está actualizado                            (validation-closure §5.1)
  · decidir si dos fuentes normativas se contradicen semánticamente     (docs/CONVENTIONS.md; A-22)
  · puntuar un impacto (scoring)                                        (prohibido por el encargo)
  · leer `.agents/policies/` o `docs/rfc/` para «aplicar» una regla     (se CITAN, no se ejecutan como prosa)
```

### 17.4 Dónde vive cada pieza

`DESIGN_OPTION` — Reparto de responsabilidades, respetando la arquitectura existente:

| Pieza | Dónde | Naturaleza |
|---|---|---|
| Norma de la derivabilidad, `premises(D)`, categorías, `work_type`, Plan/Note, vigencia | `docs/CONVENTIONS.md` (subsecciones nuevas de Change Lifecycle) | **norma** |
| Formato del registro de premisas, campos nuevos | `docs/plans/_TEMPLATE.md` | **formato** |
| Derivación (función pura) | `runtime/orchestrator/intent.py` (módulo nuevo) | **derivation logic** |
| Consumo por el host | `runtime/orchestrator/observation.py` (extensión aditiva), `derivation.py` (matriz), `contracts.py` (mapeo) | **runtime** |
| Realización read-only de fuentes + guarda de divergencia | `runtime/orchestrator/` o `runtime/governance/` (mismo estilo que `runtime/placement/`) + `tests/` | **checker + test** |
| Verificaciones de forma | extensión del patrón C-1/C-2/C-3 en `tools/`, con `EXCLUDED` para legacy | **checker** |
| Columna derivada | `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md` | **índice derivado** |
| Operación | `.agents/workflows/change-lifecycle.md`, `.agents/policies/authority.md` | **workflow** |
| CLI | `runtime/orchestrator/__main__.py` (modo `--intent` o equivalente) | **CLI** |

`DESIGN_OPTION` — **Nota sobre `.agents/`:** la capa operacional **no crea autoridad**; las
subsecciones que se le agreguen **rutan** a `docs/CONVENTIONS.md` y no duplican su semántica
(`docs/CONVENTIONS.md:Frontera operacional (DEV)`).

---

## 18. Normativa

`PC-1` (`resolución: adoptada`, 2026-10-02) — `HD-INT-H` — y `PC-1` (`resolución: pendiente`) — `HD-K4`: los invariantes necesarios se elevan a `docs/CONVENTIONS.md`.
**No** se crea una segunda fuente normativa y **no** se crea un RFC/ADR sólo para formalizar estas
reglas.

### 18.1 Los invariantes que deben entrar en `docs/CONVENTIONS.md`

`DESIGN_OPTION` — **Cinco** invariantes, y sólo los necesarios para que el comportamiento sea
normativo. Se elevan como **subsecciones nuevas de la sección Change Lifecycle** ya existente, en el
mismo estilo que las reglas operacionales vigentes (Incrementos 1–3 y plan 133).

| ID | Invariante | Texto normativo mínimo | Por qué es necesario |
|---|---|---|---|
| `INV-1` | **Derivabilidad** | «Una intención se evalúa, en el orden declarado y **después** de resolver contexto, contra el vocabulario de evidencia existente: sin señal bloqueante se construye el artefacto; la falta de información se registra como `GAP` (+ `NEEDS_CLARIFICATION`); la contradicción entre fuentes como `ANOMALY` y la ambigüedad estructural como `BOUNDARY`; y lo que exige una decisión que sólo el humano puede tomar, como `REQUIRES_HUMAN`. La condición resultante, con su señal y su evidencia, se registra en el primer artifact del Change. La ausencia de señal bloqueante no autoriza: habilita construir un artefacto **no autorizado**. `ANOMALY` nunca se resuelve por precedencia; `GAP` nunca se resuelve asumiendo.» | Es la capacidad central; sin norma, el comportamiento es discrecional y no exigible |
| `INV-2` | **`premises(D)`** | «Un Plan/Note derivado declara `## Derivación y premisas` con las ocho clases `P-1`…`P-8`, cada una con su valor y su fuente citada. Es **obligatorio** para una derivación completa; si no puede establecerse, falta información: `GAP` (+ `NEEDS_CLARIFICATION`). La derivación anterior se conserva como procedencia y **nunca** se muta ni se borra.» | Sin el registro, toda modificación humana queda indeterminada por falta de evidencia (`GAP`): `R-5` pasa de excepción a regla |
| `INV-3` | **Categorías por propiedad** | «Cada propiedad del artefacto gobernable tiene **exactamente una** categoría: `Derivado`, `Declarado`, `Confirmado` o `Forbidden-to-infer`. Dos categorías sobre la misma propiedad constituyen una ambigüedad de procedencia y son inválidas.» | Elimina la doble anotación que introduciría ambigüedad sobre qué fue derivado |
| `INV-4` | **Preservación de la declaración humana** | «Una re-derivación reescribe la capa derivada y **nunca** elimina ni altera una declaración humana. Un elemento `Declarado`/`Confirmado` que deba cambiar para que la nueva derivación sea coherente requiere una **nueva** decisión humana, no un efecto de la re-derivación.» | Es el riesgo real de toda re-derivación total; es la obligación `DESIGN_OPTION D-4` del encargo |
| `INV-5` | **`work_type` y forma del artefacto** | «`work_type` ∈ {`mechanism`, `documentary`, `mechanical`} **se deriva**; se declara en el header cuando el valor cambia una decisión (al menos `documentary` y `mechanism`). La forma Plan/Note se determina por los criterios declarados, **no** por el Change Level; si no es determinable, falta información (`GAP` + `NEEDS_CLARIFICATION`) y la decisión es humana. Los tres tipos **no** son una escala de rigor y **no** crean autoridad.» | Es el criterio que faltaba para elegir entre Plan y Nota y para seleccionar obligaciones |

`DESIGN_OPTION` — **Además** (no es un sexto invariante, es la materialización de `HD-INT-B` y `HD-INT-C`):
un párrafo que declare el campo de vigencia, sus cuatro valores, la regla de no-fusión con el status
(§15.2), el default `active` por ausencia, y que `Superseded` sin sucesor exige `Motivo de retiro`.
Vive en la subsección de lifecycle, y su enforcement es `E-6`.

### 18.2 Qué **no** se eleva (y por qué)

`DESIGN_OPTION` — Se deja **fuera** de `CONVENTIONS.md`, deliberadamente:

| No se eleva | Dónde vive | Razón |
|---|---|---|
| La tabla de las ocho clases de premisa con su formato | `docs/plans/_TEMPLATE.md` | es **formato**, no norma (mismo reparto que anchor: formato en el template, semántica en CONVENTIONS) |
| Los criterios Plan/Note como matriz | `.agents/workflows/change-lifecycle.md` | es **operación**; rutea a la norma sin duplicarla |
| El detalle de la resolución de reglas (las diez fuentes, el orden) | `.agents/policies/authority.md` (enrutamiento) + la realización read-only | es **operación + checker** |
| El texto de la investigación | — | **no se copia**: `CONVENTIONS.md` no es un resumen de la investigación |
| `DERIVED`/`UNDETERMINED` como enum de código | `runtime/orchestrator/contracts.py` | es **implementación** de la norma |

### 18.3 Separación norma / implementación / checker / documentación

`DESIGN_OPTION` — La separación explícita, que es lo que el encargo pide diferenciar:

```text
NORMA            docs/CONVENTIONS.md         qué debe ser verdad (INV-1 … INV-5)
IMPLEMENTACIÓN   runtime/orchestrator/*.py   qué hace el sistema (derivación, consumo, matriz)
CHECKER          tools/*.py + tests/         qué se verifica mecánicamente (forma, no prosa)
DOCUMENTACIÓN    .agents/*, docs/working/    cómo se opera y de dónde sale el diseño
```

`FACT` — **Ninguna de las cuatro reemplaza a otra.** En particular: el checker **no** es la norma
(Mecanismo 14: «checker output = evidencia factual ≠ autoridad»), y la documentación operacional
**no** crea autoridad (`docs/CONVENTIONS.md:Frontera operacional (DEV)`).

### 18.4 Ubicación exacta de las subsecciones

`DESIGN_OPTION` — Las subsecciones nuevas se agregan **dentro** de la sección Change Lifecycle de
`docs/CONVENTIONS.md`, junto a las reglas operacionales vigentes, con estos nombres:

```text
docs/CONVENTIONS.md:Change Lifecycle — Derivabilidad y registro de premisas (regla operacional; …)
docs/CONVENTIONS.md:Change Lifecycle — work_type y forma del artefacto gobernable (regla operacional; …)
docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada (regla operacional; …)
```

`FACT` — **Ningún documento nuevo de gobernanza.** No se crea RFC, no se crea ADR, no se crea una
sección paralela. Es la lectura literal de `HD-INT-H` y `HD-K4`.

---

## 19. Validation

### 19.1 Qué debe demostrar el Change

`DESIGN_OPTION` — El Change está terminado cuando **todas** estas condiciones son verificables:

```text
V-1   `Implementá X`, con X determinado por el repositorio, produce un artefacto gobernable
      COMPLETO y NO AUTORIZADO, sin que el humano escriba el artefacto
V-2   ese artefacto nace `Aprobado para redacción` y el host se detiene en
      STOP_AWAIT_PLAN_AUTHORIZATION
V-3   autorizado el artefacto, SAE ejecuta sin NINGÚN cambio de comportamiento respecto de hoy
V-4   una intención con dos lecturas razonables produce una PREGUNTA con ≥2 opciones, y NO un artefacto
V-5   un conflicto normativo produce una ESCALACIÓN con las DOS fuentes y el punto de incompatibilidad,
      y NO una elección
V-6   una intención fuera de autoridad se detiene y NOMBRA la reserva y a quién pertenece
V-7   una modificación humana editorial NO produce re-derivación y la derivación se conserva (`R-1`)
V-8   una modificación humana de una premisa produce re-derivación y la derivación anterior se
      conserva como procedencia (`R-4`)
V-9   una declaración humana añadida SOBREVIVE a una re-derivación (`R-3` + `INV-4`)
V-10  una modificación cuyo impacto no puede determinarse produce UNDETERMINED y se detiene (`R-5`)
V-11  el corpus histórico tiene 0 modificaciones (153 planes, 80 RFCs, 18 ADRs) y la batería sigue verde
V-12  no existe ninguna entidad, registry, namespace ni state machine nueva
V-13  el host NO adquiere ninguna autorización nueva y sus stop conditions no cambian
V-14  la guarda de divergencia FALLA si la regla documental y su realización mecánica se separan
V-15  el dogfood de §21 se ejecuta de punta a punta, incluida la ejecución 1 (que se DETIENE)
```

### 19.2 Cómo se verifica cada una

`DESIGN_OPTION` — Reparto por mecanismo, con el mínimo privilegio:

| Condición | Cómo se verifica | Tipo |
|---|---|---|
| `V-1`, `V-2` | test del camino de derivación contra un repositorio de fixture; aserción sobre el veredicto y sobre el status del artefacto creado | test |
| `V-3` | la suite existente de SAE (`tests/test_sae_scope_enforcement.py`, `tests/test_autonomous_scope.py`, `tests/test_autonomous_orchestrator.py`) sigue verde **sin modificación** | test |
| `V-4` | caso de falsación con intención ambigua; aserción: **no** se crea artefacto y se produce un pedido de aclaración con ≥2 opciones | test |
| `V-5` | caso de falsación con dos fuentes **en alcance** que determinan obligaciones incompatibles (**no** el caso de §21, que es `GAP` + divergencia); aserción: **no** se elige ninguna y se citan las dos fuentes | test |
| `V-6` | caso de falsación con intención que exige release; aserción: `NOT_DERIVABLE` + la reserva nombrada | test |
| `V-7`…`V-10` | matriz de falsación de §20, un test por caso | test |
| `V-11` | `git diff` del corpus + batería canónica de `docs/VERSIONING.md:4.1` | evidencia factual |
| `V-12` | búsqueda mecánica: ausencia de entidades/registries nuevos; revisión del diff de `contracts.py` (sólo adiciones a vocabularios existentes) | evidencia factual |
| `V-13` | `git diff` de `runtime/orchestrator/authority.py` y de `.agents/policies/supervised-autonomous-execution.md`: **sin cambios** | evidencia factual |
| `V-14` | el test de divergencia se rompe deliberadamente en un escenario sintético y debe fallar | test |
| `V-15` | registro del dogfood con sus dos ejecuciones y sus artefactos | evidencia documental |

### 19.3 Qué NO es validación

`DESIGN_OPTION`:

```text
NO es validación:
  · que el verificador verde sea evidencia de corrección semántica  (VC-1: PASS es evidencia de
    ejecución dentro de un entorno declarado, no una garantía semántica)
  · un checker interpretando prosa                                  (prohibido)
  · una métrica de autonomía alta                                    (SAE §11: la métrica observa, no incentiva)
  · auto-validación del derivador sobre su propia derivación         (misma trampa que la
    consistencia auto-escrita: la evidencia debe ser de otra clase)
```

`FACT` — La última línea es un hallazgo **real y medido** de I-22 §3.6 (b): `runtime/orchestrator/governance.py`
**escribe** `- **Consistencia checkpoint↔anchor:** PASS` y `runtime/orchestrator/observation.py` la
**lee de vuelta**, y `host.py` deriva `Closed` con esa lectura. I-22 lo clasifica
`PARTIALLY_IMPLEMENTED` con un `GAP` de calidad de evidencia, y cita la norma del payload que lo
prohíbe (`protocol/.agents/harness/INDEX.md`: «A claim may be called "verified" only when it cites
evidence of a class other than attestation»).

`DESIGN_OPTION` — **Pertinencia para este Change, y es directa:** el registro de `premises(D)` es
**atestación del derivador sobre su propia derivación**. Por eso el diseño **no** se apoya sólo en él:
`R-1` se decide con `_canonical_text` (proyección calculable, no declarada), y la invalidación se
evalúa **contra el repositorio** (el lifecycle de las fuentes, las rutas escritas, la existencia de la
cita), no contra la declaración del propio artefacto. Esto **no** se propone arreglar aquí (es un
hallazgo de I-22 sobre un mecanismo existente, fuera del alcance de este Change) pero **sí** condiciona
el diseño: **el registro de premisas nunca es la única evidencia de la validez de una derivación.**

### 19.4 Criterios de salida del Change

`DESIGN_OPTION` — El Change cierra cuando `V-1`…`V-15` están evidenciadas, la batería canónica está
verde, las dos determinaciones de impacto están declaradas (`.agents/policies/validation-closure.md:5.1/5.2`),
y el corpus histórico no tiene modificaciones.

---

## 20. Falsification Matrix

`DESIGN_OPTION` — Matriz de casos negativos. **Cada caso declara input, clasificación esperada,
acción esperada, stop condition esperada y evidencia.** Ninguno se ejecuta en este trabajo: se diseñan
para ser falsables por el Change.

| # | Input | Clasificación esperada | Acción esperada | Stop esperado | Evidencia |
|---|---|---|---|---|---|
| `F-1` | **Intención ambigua** (`Mejorá el sistema de ejecución.`) | `BOUNDARY` (≥2 lecturas de la intención) | **no** crear artefacto; producir pedido de aclaración con ≥2 opciones + opción libre | `NEEDS_CLARIFICATION` | las dos lecturas citadas (§15.2 de I-23 sirve de base) |
| `F-2` | **Contexto insuficiente** (`Implementá el mecanismo que falta.`) | `GAP` + `NEEDS_CLARIFICATION` | preguntar qué mecanismo; **no** adivinar por proximidad | `NEEDS_CLARIFICATION` | qué se buscó y no se encontró |
| `F-3` | **Dos interpretaciones razonables** (`Implementá la admisión.`, donde existen admisión de efectos y admisión de tarea) | `BOUNDARY` | detenerse y escalar con las dos lecturas | `REQUIRES_HUMAN` | lectura A + lectura B, ambas citadas |
| `F-4` | **Norma del payload sin ejecutor en DEV + divergencia** (el caso real de §21; **no** un conflicto entre fuentes vigentes) | `REQUIRES_HUMAN` con la reserva nombrada + `GAP` declarado (advisory) | **no** elegir una fuente ni «armonizar»; escalar citando las dos fuentes y el punto exacto | `REQUIRES_HUMAN` | fuente del payload + ejecutor DEV + punto exacto de divergencia + impacto |
| `F-5` | **`work_type` indeterminable** (rutas que no permiten decidir `mechanism` vs `documentary`) | `GAP` en el ítem `work_type` (+ `NEEDS_CLARIFICATION`); el ítem no puede quedar como «sin señal bloqueante» | preguntar; si el humano lo establece, el campo pasa a `Declarado` (`HD-K2`) | `NEEDS_CLARIFICATION` | las rutas consideradas y por qué no determinan |
| `F-6` | **Plan/Note indeterminable** | `GAP` en el ítem «forma» (+ `NEEDS_CLARIFICATION`) | preguntar; **nunca** elegir por defecto | `NEEDS_CLARIFICATION` | criterios `C-1`…`C-13` evaluados, con el criterio no decidible nombrado |
| `F-7` | **Scope modificado antes de autorizar** (cualquier dirección) | `R-4` **incondicional** (`HD-K1`) | re-derivar (`D2`); el artefacto vuelve a `proposed` | ninguno (re-derivación, no stop) | `premises(D1)` y `premises(D2)` con `P-8` distinto, ambas citadas |
| `F-8` | **Scope reducido** (quitar un path que no alteraba obligaciones) | `R-4` — **sin excepción** | re-derivar | ninguno | ídem; nota explícita de que `HD-K1` prohíbe la excepción «inocua» |
| `F-9` | **Scope expandido** | `R-4` | re-derivar; si el path nuevo exige autoridad nueva → `STOP-1` | `REQUIRES_HUMAN` si el path nuevo trae decisión normativa o de autoridad | `premises(D2)` + la regla nueva citada, o la reserva nombrada |
| `F-10` | **Premisa modificada** (p. ej. cambiar `Task`) | `R-4` | re-derivar | ninguno | `premises(D1)` vs `premises(D2)` |
| `F-11` | **Nueva declaración humana** (un criterio de salida propio que no era premisa) | `R-3` | aceptar; registrar la declaración; **no** re-derivar | ninguno | `premises(D)` que prueba que el elemento **no** era premisa |
| `F-12` | **Cambio editorial** (re-indentar, re-envolver, reordenar la lista de scope) | `R-1` | aceptar; **no** re-derivar | ninguno | `canonical_text(antes) == canonical_text(después)` |
| `F-13` | **Premisa no disponible** (`premises(D)` no registrado, artefacto legacy) | `R-5` = `GAP` + `NEEDS_CLARIFICATION` | **no** asumir que la derivación sobrevive ni que murió; preguntar | `NEEDS_CLARIFICATION` | declaración explícita de la ausencia (§8.4) |
| `F-14` | **Derivación anterior sin provenance suficiente** (registro presente pero sin `P-8` o sin `P-7`) | `GAP` — derivación **incompleta** | **no** construir el artefacto: `PD-4`/`PD-7` detienen | `NEEDS_CLARIFICATION` | qué clase de premisa falta |
| `F-15` | **Autorización ausente** (artefacto `Aprobado para redacción`) | — | el host **se detiene** | `STOP_AWAIT_PLAN_AUTHORIZATION` | el status observado |
| `F-16` | **Autorización incompatible** (el humano modifica `Task`/status **después** del `pin`) | — (no es HD-K: es Momento 2) | camino existente; **no** se re-deriva | `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN` | el `pin` original y la divergencia (`authorization_drift`) |
| `F-17` | **Intento de modificar Scope durante SAE** | — | idem `F-16`; **no** se amplía el scope | `STOP_SCOPE_VIOLATION` | `.agents/policies/supervised-autonomous-execution.md:1.4`; `<PLAN-138>:PC-2` deferred |
| `F-18` | **Intento de utilizar una regla no aplicable** (una fuente `deprecated`/`archived` como norma) | el veredicto de esa fuente es `NOT_APPLICABLE` | **no** usarla como norma; citarla sólo como provenance | `GAP` declarado (no bloqueante) | el lifecycle declarado de la fuente (§15) |
| `F-19` | **Intención que exige una reserva humana** (`Liberá la versión 12.0.0.`) | `REQUIRES_HUMAN` | derivar **todo lo demás**, separar la parte no derivable, **no** incluir el release en el artefacto, escalar | `REQUIRES_HUMAN` (y `FORBIDDEN` para el host si se intentara ejecutar) | `RELEASE` ∈ `FORBIDDEN_ACTIONS`; SAE §5 |
| `F-20` | **Introducción de algo que cae en `FI-1`…`FI-10`** (p. ej. una norma nueva en el `proposed`) | — | **detener**; **no** re-derivar | `STOP-1` / `REQUIRES_HUMAN` | la reserva nombrada + quién la posee |
| `F-21` | **Intención que toca `protocol/.agents/`** | efecto payload ⇒ **Clase A/B** | detener la vía DEV y seguir la vía RFC-56 | `STOP_AUTHORITY_REQUIRED` | `docs/rfc/56-governance-fast-track.md:Reglas de borde`; `RQ-7` |
| `F-22` | **Intención que pide algo diferido** (`Implementá la propagación de impacto entre artefactos.`) | `REQUIRES_HUMAN` | **no** construir artefacto; escalar citando los gates | `REQUIRES_HUMAN` | `docs/rfc/68-architecture-evolution-workflow.md:Non-Goals` (gates de Fase 2) |
| `F-23` | **`work_type` declarado que contradice las rutas** (`documentary` con escritura en `runtime/`) | inconsistencia detectable | rechazar el valor declarado; el derivado gobierna | `GAP`/`ANOMALY` según evidencia | rutas escritas vs enum (`E-5`) |
| `F-24` | **Doble categoría sobre la misma propiedad** (`Derived` + `Declarado`) | `INV-3` violado | inválido; se exige una sola categoría | `ANOMALY` | `MK-9`; formato del artefacto |
| `F-25` | **Re-derivación que intenta borrar una declaración humana** | `INV-4` violado | **rechazado**: el escritor no puede tocar la capa declarada | `ANOMALY` | el elemento `Declarado` presente y su decisión registrada |

`FACT` — Los 25 casos cubren **todos** los mínimos del encargo y añaden los que la evidencia impone
(`F-13`/`F-14` de `HD-K3`; `F-24`/`F-25` de `INV-3`/`INV-4`).

---

## 21. Dogfood

### 21.1 Diseño del dogfood (un único dogfood integral, dos ejecuciones)

`DESIGN_OPTION` — **Entrada:** `Implementá Effect Admission para SAE.`

`FACT` — **Hallazgo crítico y verificado:** esta intención **no es derivable hoy a un Plan completo**,
y el diseño **debe** detenerse. La resolución de contexto encuentra:

| Fuente | Qué dice | Veredicto |
|---|---|---|
| `protocol/.agents/standards/runtime/AUTHORIZATION.md:Effects block` y `:Authorization states` | un efecto fuera de frontera exige una entrada `[[effects]]` con `authorized_by`, `evidence_ref` y `status`; `AUTHORIZED`/`UNAUTHORIZED`/`AUTHORIZATION_UNDETERMINED`; `AUTH-004` | `NOT_APPLICABLE` **como regla de DEV** (el payload no es regla operativa: `AGENTS.md`; `.agents/AGENTS.md`); norma del dominio Protocol cuya **realización DEV falta** (`GAP`, evidencia) |
| `.agents/policies/supervised-autonomous-execution.md:1.3` y `:2. The two gates, in order` | la admisión del host se hace sobre **paths de escritura** y **clases de acción** (`_AUTONOMY_CLASS_BY_ACTION`); una acción sin entrada es `STOP_UNCLASSIFIABLE_ACTION`; el bloque `## Effects` **no se consume** | `APPLIES` (operación del host DEV) |
| `docs/architecture-capability-review.md:4.2 Capability Governance / capability admission` (Working, **untracked**) | registra la carencia como `ARCHITECTURAL_PREREQUISITE` (`PR-1`) y declara «DEV (realización) + PROTOCOL (norma)» | **evidencia**, no norma (`LV-4`) |

`CONTRADICTION` — **La situación (Fase 1, F5):** la norma del payload exige autorización **registrada
por efecto**; el ejecutor DEV admite por **path/clase de acción** y **no lee** `## Effects`. **No** es un
conflicto entre dos normas vigentes en alcance: es una **norma del payload sin ejecutor en DEV** (un
`GAP` arquitectónico, `PR-1`) **más** una divergencia entre implementación y fuente normativa que **no
debe resolverse por precedencia inventada** (`PC-75`; `RQ-5`) **más** la reserva humana de dominio y vía
(`FI-3`).

`DESIGN_OPTION` — Comportamiento correcto, paso a paso:

```text
E-1  INTENT_CONFIDENCE: +2 (verbo «Implementá») +2 (entidad «Effect Admission») +2 («SAE» nombrado)
                       = 6 → HIGH
     (con la variante `Implementá Effect Admission.`: 4 → MEDIUM → confirmación obligatoria)
E-2  contexto: se enumeran las fuentes candidatas CON su lifecycle
E-3  orden de evaluación:
       paso 1  ¿exige una decisión que sólo el humano puede tomar?  SÍ
               (el punto de admisión es una decisión de alcance/arquitectura: FI-3 + AU-6)
               → NOT_DERIVABLE
       (y aunque se evaluara sin el paso 1, la aplicabilidad de `S-10` daría
        `UNDETERMINED` sobre el dominio/vía — **no** `CONFLICT`: el payload
        no es regla de DEV, así que no hay dos normas en alcance que se contradigan)
E-4  NO se construye artefacto autorizable: se produce la PREGUNTA + la escalación
E-5  el humano decide el punto de admisión
E-6  con la decisión como fuente nueva se re-evalúa desde E-2 y se deriva el artefacto
```

### 21.2 Ejecución 1 — el sistema se detiene y pregunta (la prueba más fuerte)

`DESIGN_OPTION` — Registro obligatorio de la ejecución 1:

> **Veredicto:** `NOT_DERIVABLE` (reserva nombrada: el punto de admisión de un efecto; `GAP` declarado:
> el payload define la admisión por **efectos** y el host DEV no la ejecuta; **no** hay conflicto entre
> fuentes vigentes — Fase 1, F5).
>
> **Decisión requerida:** cuál es el punto de admisión de un efecto.
> **Dueño:** el mantenedor (`ADR-16`: clase `DECISION`; `AU-6`: ADR-worthiness es juicio humano).
> **Fuente A (norma del payload):** `protocol/.agents/standards/runtime/AUTHORIZATION.md:Effects block`
> y `:Authorization states` — todo efecto fuera de frontera exige `[[effects]]` con `authorized_by` y
> `status`; `AUTHORIZATION_UNDETERMINED` nunca se reporta como `UNAUTHORIZED` (`AUTH-004`).
> **Fuente B (operación del host DEV):** `.agents/policies/supervised-autonomous-execution.md:1.3` y
> `:2. The two gates, in order` — la admisión es sobre **paths de escritura** y **clases de acción**;
> `## Effects` es evidencia no consumida.
> **Punto exacto de incompatibilidad:** dos admisiones distintas para el mismo hecho (un efecto), una
> por efecto declarado y otra por path/clase de acción, sin que ninguna declare precedencia.
> **Impacto:** cualquier trabajo que ejecute efectos reales bajo SAE quedaría con dos admisiones
> incompatibles.
> **Opciones (formato `NO_ASSUMPTIONS`: impacto + ≥2 opciones + opción libre):**
> 1. **Sólo DEV** — la admisión de efectos se realiza en el host DEV (`runtime/orchestrator/`),
>    admitiendo el efecto antes de delegar, y `AUTHORIZATION.md` **no cambia**: es un cambio **DEV**,
>    L2, sin RFC-56 (no toca el payload), con verificación = batería canónica + suites de SAE.
> 2. **DEV + payload** — la admisión se realiza en el host DEV **y** se extiende
>    `AUTHORIZATION.md` con el punto de admisión: es **Clase A de RFC-56**, requiere RFC `Accepted`,
>    y **cambia lo que los adoptantes reciben**.
> 3. **Otra** (especificar).
>
> **Lo que el sistema NO hizo:** no eligió la fuente «más específica» (`AUTHORIZATION.md` lo es),
> no eligió la «más nueva», no creó jerarquía, no reinterpretó `PC-75` para «armonizar», y no asumió
> el alcance a partir de `docs/architecture-capability-review.md` (que es Working **untracked** y
> declara «DEV + PROTOCOL», pero es una **observación**, no una autorización: `PC-52` — a request is
> not an authorization).

`FACT` — **Por qué esta ejecución es la prueba más fuerte del Change:** un diseño que «siempre deriva
un Plan» fallaría aquí produciendo un Plan sobre una decisión que no es suya. El diseño correcto
**se detiene**, y con eso demuestra simultáneamente (a) que el contexto se resolvió de verdad, (b) que
la derivabilidad distingue conflicto de falta de información, y (c) que derivar no es autorizar.

### 21.3 Ejecución 2 — derivación completa tras la decisión humana

`DESIGN_OPTION` — Supuesto explícito: el humano elige la **opción 1** (sólo DEV). Ésta es la
derivación completa, y es la que verifica los 18 puntos exigidos por el encargo:

| Elemento | Valor derivado | Fuente |
|---|---|---|
| `work_type` | **`mechanism`** | toca `runtime/` (comportamiento del host) y `tests/` (§12.5) |
| Dominio | **DEV** (`runtime/`, `tests/`) | `docs/placement-contract.md:3. Domain / owner identification` |
| Clase RFC-56 | **ninguna** (no toca `protocol/.agents/`) | `docs/rfc/56-governance-fast-track.md:Reglas de borde` |
| Change Level | **L2** (multi-área: `runtime/` + `tests/`; cambio estructural entre límites) | `docs/rfc/75-change-lifecycle.md:Mecanismo 2` |
| Norma aplicable | `.agents/policies/supervised-autonomous-execution.md:1.3` y `:2`; `runtime/orchestrator/authority.py`; `runtime/orchestrator/autonomy.py` | `S-2` (§13.3) |
| Norma del payload | `protocol/.agents/standards/runtime/AUTHORIZATION.md` — **`NOT_APPLICABLE`** como regla de DEV (no se modifica), **evidencia** del modelo a realizar | `S-10` + `RQ-7` |
| Evidencia | `docs/architecture-capability-review.md:4.2` (Working untracked) — **provenance**, no norma | `LV-4` |
| Obligaciones | Plan + implementación en `runtime/orchestrator/` + tests + batería canónica | `docs/rfc/75-change-lifecycle.md:Mecanismo 5`; `docs/VERSIONING.md:4.1` |
| Verificación | batería canónica + `tests/test_sae_scope_enforcement*.py` + `tests/test_autonomous_scope*.py` + suite nueva del punto de admisión | `docs/VERSIONING.md:4.1` |
| Ubicación | `runtime/orchestrator/` (familia *Reference runtime*), `tests/` (familia *Test subsystem*) | `docs/placement-contract.md:6` + `runtime/placement/resolver.py` |
| Forma | **Plan** (criterios `C-1`, `C-2`, `C-7`, `C-11`, `C-12` = SÍ) | §11.2 |
| Autoridad requerida | Plan `Aprobado para ejecución`; **sin** RFC/ADR | §11.2 |
| Scope | `runtime/orchestrator/` (los archivos que la implementación requiera) + `tests/` + el Plan | **Declarado por el humano** (`P-8`) |
| `premises(D)` | `P-1`…`P-8` completas | §8.2 |
| Puntos que siguen indeterminados | **ninguno** de los 18; queda indeterminado únicamente el **conjunto exacto de archivos** dentro de `runtime/orchestrator/`, que es decisión de implementación dentro del scope declarado |

### 21.4 Verificación de los 18 puntos exigidos por el encargo

`DESIGN_OPTION` — El dogfood debe comprobar, como mínimo:

| # | Punto | Cómo lo comprueba el dogfood |
|---|---|---|
| 1 | Intake de intención | `IntakeRecord` con el texto literal y `origin_type = direct maintainer action` |
| 2 | Confidence | `INTENT_CONFIDENCE` calculado: **6 → HIGH** con «SAE» nombrado; **4 → MEDIUM** sin él (dos variantes del mismo input, ambas registradas) |
| 3 | Context | la tabla de fuentes de §21.1, **con lifecycle** de cada una |
| 4 | Derivability | `NOT_DERIVABLE` en la ejecución 1; `DERIVED` en la ejecución 2 (tras la decisión) |
| 5 | `work_type` | `mechanism`, con el criterio de admisión (rutas + naturaleza) |
| 6 | Applicable rules | `S-2` `APPLIES`; `S-10` `NOT_APPLICABLE` como regla de DEV; **conflicto detectado y escalado** en la ejecución 1 |
| 7 | Plan vs Note | **Plan**, con los cinco criterios que lo determinan nombrados |
| 8 | Scope | `runtime/orchestrator/` + `tests/` + el Plan, **Declarado** por el humano |
| 9 | `premises(D)` | las ocho clases, con valor, fuente, categoría y vigencia |
| 10 | Artefacto propuesto | el Plan, con `**Status:** Aprobado para redacción` y `## Derivación y premisas` |
| 11 | Autorización humana | el humano lleva el status a `Aprobado para ejecución` (acto separado, registrado) |
| 12 | SAE | el host observa, deriva, fija el `pin` y conduce; **sin cambio de lógica** |
| 13 | **Modificación humana pre-autorización** | **obligatoria**: el humano **modifica el Scope** declarado (agrega la ruta exacta de un módulo que el derivador no había incluido, o quita una) |
| 14 | Invalidación / re-derivación | `R-4` **incondicional** (`HD-K1`): `D1` queda inválida para el contenido nuevo; `D2` se produce; el artefacto vuelve a `proposed` |
| 15 | **Preservación de declaración humana** | en el mismo acto, el humano **añade** una declaración que no era premisa (p. ej. un criterio de salida propio) ⇒ `R-3`: `D1` sigue válida para lo que produjo, la declaración se registra y **sobrevive a la re-derivación `D2`** (`INV-4`) |
| 16 | Ejecución | SAE conduce el trabajo dentro del scope autorizado (batería + suites + la suite nueva) |
| 17 | Verificación | anchor (VC-1) con el command-set real; gates C-1/C-2/C-3 |
| 18 | Cierre | `Executed` + checkpoint + consistencia + las dos determinaciones de impacto; `Closed` derivado |

`FACT` — **El punto 13 y el 15 se ejecutan en el MISMO acto humano, y eso es deliberado:** un solo
acto del humano que (a) cambia una premisa y (b) añade una declaración nueva prueba a la vez `R-4` y
`R-3`, y prueba que la re-derivación **no borra** la declaración (el riesgo real de toda
re-derivación total). Si el dogfood ejecutara sólo uno, no falsaría `INV-4`.

### 21.5 Qué falsificaría el dogfood (criterio de fallo)

`DESIGN_OPTION`:

```text
FALLA si:
  · la ejecución 1 produce un Plan (en lugar de detenerse y preguntar)
  · la ejecución 1 elige una de las dos fuentes sin escalar
  · el artefacto derivado nace autorizado, o el derivador escribe el status de autorización
  · la modificación de Scope NO produce re-derivación
  · la declaración humana añadida desaparece tras la re-derivación
  · el host cambia su comportamiento, sus stops o sus autorizaciones
  · el corpus histórico cambia
  · se crea una entidad, registry, namespace o state machine
```

---

## 22. Change Scope

`DESIGN_OPTION` — Este es el **único Plan integral** que debe ejecutarse. No es una colección de
micro-Plans.

### 22.1 Objective

`DESIGN_OPTION` — **Materializar la capacidad completa** de recibir una intención humana breve,
derivar el trabajo gobernable que la evidencia permita, y detenerse exactamente donde siga siendo
necesaria autoridad humana — reutilizando al máximo los mecanismos existentes, sin crear una
arquitectura paralela, y **con la frontera SAE intacta**.

Criterio de éxito: un implementador posterior puede tomar este Plan y ejecutar **un único Change
integral** sin volver a resolver las decisiones arquitectónicas fundamentales.

### 22.2 Scope (qué puede modificarse)

`DESIGN_OPTION`:

```text
docs/CONVENTIONS.md                    subsecciones nuevas (INV-1 … INV-5 + vigencia)
docs/plans/_TEMPLATE.md                campos y secciones nuevas (Work type, Derivación y premisas, Tipo)
docs/VERSIONING.md:7                   sólo si el Change declara vigencia de artefactos propios
docs/AGENTS.md                         sólo referencia cruzada si hace falta (sin duplicar)
.agents/workflows/change-lifecycle.md  clasificación y criterios Plan/Note
.agents/policies/authority.md          enrutamiento al conjunto de fuentes §13.3 (sin duplicar norma)
runtime/orchestrator/intent.py         NUEVO módulo: derivación pura
runtime/orchestrator/observation.py    extensión ADITIVA de ChangeObservation
runtime/orchestrator/derivation.py     consumo de la matriz de governance (no de su lógica de cierre)
runtime/orchestrator/contracts.py      adiciones al vocabulario (nuevas acciones/stops si hicieran falta)
runtime/orchestrator/__main__.py       punto de entrada de la intención (CLI)
runtime/<realización de fuentes>       realización read-only + enrutamiento (mismo estilo que runtime/placement/)
tools/                                 extensiones de forma en el patrón C-1/C-2/C-3
tests/                                 suites nuevas + suites existentes SIN modificar
docs/plans/INDEX.md, docs/rfc/INDEX.md, docs/adr/INDEX.md   columna derivada de vigencia (si HD-M4 = sí)
CHANGELOG.md                           entrada [Unreleased] del propio Change
```

`FACT` — **Toda modificación de artefactos existentes es aditiva.** Ningún invariante existente se
reescribe; ninguna semántica vigente cambia.

### 22.3 Out of Scope (qué NO puede tocarse)

`DESIGN_OPTION`:

```text
NO  protocol/.agents/ ni protocol/_AGENTS.md  (salvo que el humano elija la opción 2 del dogfood,
     en cuyo caso el alcance cambia a Clase A de RFC-56 y este Plan se re-emite ANTES de ejecutar)
NO  dist/ (se regenera por CI en tags)
NO  el corpus histórico: 153 planes, 80 RFCs, 18 ADRs → 0 modificaciones
NO  migración o clasificación retroactiva de artefactos
NO  docs/CONVENTIONS.md:Convenciones (los ciclos de status existentes se preservan)
NO  docs/placement-contract.md (PC-10/PC-20: crear familia/namespace es cambio de gobernanza)
NO  runtime/orchestrator/authority.py (FORBIDDEN_ACTIONS y los tres veredictos quedan intactos)
NO  .agents/policies/supervised-autonomous-execution.md (la frontera SAE queda intacta)
NO  runtime/orchestrator/autonomy.py en su semántica (authorization_drift, _canonical_text, verify_write_targets)
NO  abrir RFC-68 Fase 2
NO  resolver las contradicciones del payload del Protocol
NO  tools/check_plan_citations.py (hallazgo residual independiente, §25)
NO  machine-locatability de excepciones de Placement
NO  crear entidades, registries, namespaces, state machines, authority classes ni primitive de identidad
NO  cerrar C-2/CI, no reabrir Plan 121, no reabrir R4
```

### 22.4 Deliverables (agrupados por funcionalidad, no por archivo)

`DESIGN_OPTION` — Siete grupos. **Un Plan = una unidad coherente de autorización y ejecución**: los
siete comparten objetivo, autoridad (`Plan Aprobado para ejecución`), scope (el de §22.2), criterios de
validación (§19) y frontera de riesgo (DEV docs + runtime DEV, sin release de protocolo).

| Grupo | Funcionalidad | Entregables |
|---|---|---|
| `D-1` | **Norma** | `INV-1`…`INV-5` + la regla de vigencia en `docs/CONVENTIONS.md` (subsecciones nuevas) |
| `D-2` | **Formato del artefacto** | `**Work type:**`, `**Tipo:**`, `## Derivación y premisas` en `docs/plans/_TEMPLATE.md`; campos de vigencia |
| `D-3` | **Derivación** | `runtime/orchestrator/intent.py`: veredicto de derivabilidad, `work_type`, forma Plan/Note, construcción del registro de premisas y del artefacto **no autorizado** |
| `D-4` | **Resolución de reglas aplicables** | realización read-only del conjunto de fuentes §13.3 + enrutamiento por sujeto + los cuatro veredictos, **citando sin copiar** |
| `D-5` | **Guarda de divergencia** | test que falla si la tabla de fuentes y las fuentes se desalinean (§13.8) |
| `D-6` | **Consumo y matriz** | extensión aditiva de `observation.py`; ejecución de la matriz de governance en `derivation.py`; mapeo en `contracts.py` |
| `D-7` | **Verificación de forma** | extensiones del patrón C-1/C-2/C-3 con `EXCLUDED` para legacy; enum de `work_type`; `Superseded` sin sucesor ⇒ motivo; coherencia columna↔header del INDEX |
| `D-8` | **Operación y registro** | subsecciones en `.agents/workflows/change-lifecycle.md` y `.agents/policies/authority.md`; columna derivada en los INDEX; entrada `[Unreleased]` en `CHANGELOG.md` |

`DESIGN_OPTION` — **Entrega explícitamente separada dentro del diseño (no como otro Plan):** si
durante la ejecución apareciera trabajo **independiente** (otro objetivo, otra autoridad, otro scope),
debe quedar **explícitamente separado dentro del diseño** (§17, criterio de cohesión) y **no** crear
automáticamente otro Plan. Los trabajos independientes se registran como `NA-*` (§17.4) y se escalan.

### 22.5 Dependencies (prerequisitos)

`DESIGN_OPTION`:

| Dependencia | Qué aporta | Estado |
|---|---|---|
| `HD-INT-A`…`HD-INT-J` (2026-10-02) y `HD-K1`…`HD-K4` (2026-10-05) resueltas | el alcance queda fijado | **`PC-1`**: `resolución: adoptada` (2026-10-02 y 2026-10-05; registros canónicos en `I-23 §17.1` y `HDK §16.2`) |
| `HD-INT-D` (forma y registro de la Note) | habilita `D-2` en su parte de Nota y la decisión Plan/Note | **adoptada** — Opción A (§3.2); era el duplicado `HD-M1` (Fase 1, F3) |
| `docs/plans/_TEMPLATE.md` + `docs/CONVENTIONS.md` | donde vive la norma y el formato | existen |
| `runtime/orchestrator/{observation,derivation,contracts,authority,autonomy,host}.py` | base del consumo y de la frontera | existen |
| `runtime/placement/{rules,resolver}.py` + `tests/test_placement_contract_drift.py` | **patrón** a replicar para reglas y guarda | existen |
| `tools/check_lifecycle_{anchor,checkpoint,lineage}.py` | patrón de forma a extender | existen |
| `tools/check_plan_structure.py` | verificador de forma de planes e INDEX | existe |

### 22.6 Normative changes

`DESIGN_OPTION` — Exactamente **cinco invariantes** más la regla de vigencia, en **una sola** fuente
normativa (`docs/CONVENTIONS.md`), sin RFC ni ADR nuevo (§18). **Nada** cambia en
`docs/placement-contract.md`, `docs/AGENTS.md:Lifecycle` (el vocabulario se reutiliza) ni en los
ciclos de status de `docs/CONVENTIONS.md:Convenciones`.

### 22.7 Runtime changes

`DESIGN_OPTION`:

```text
NUEVO      runtime/orchestrator/intent.py            derivación pura + tipos de resultado
NUEVO      realización read-only de fuentes + enrutamiento (mismo estilo que runtime/placement/)
ADITIVO    observation.py    campos nuevos en ChangeObservation (work_type, lifecycle de fuentes,
                             registro de premisas observado)
ADITIVO    derivation.py     consumo de la matriz de governance
ADITIVO    contracts.py      acciones/stops nuevos si el mapeo los requiere (vocabulario existente)
ADITIVO    __main__.py       punto de entrada de intención
SIN CAMBIO authority.py      FORBIDDEN_ACTIONS, HUMAN_ACTIONS y los tres veredictos
SIN CAMBIO autonomy.py       authorization_drift, _canonical_text, verify_write_targets, evaluate_autonomy
SIN CAMBIO host.py           _apply_autonomy_gate, _pinned_autonomy_projection (salvo consumo de campos)
```

`FACT` — **Ningún comportamiento existente cambia para un Plan de la forma actual.** El host sigue
funcionando exactamente igual con artefactos sin los campos nuevos (legacy).

### 22.8 Validation

`DESIGN_OPTION` — Lo de §19: `V-1`…`V-15`, con la batería canónica verde, las suites de SAE **sin
modificar**, el corpus histórico con **0 modificaciones**, y la guarda de divergencia funcionando.

### 22.9 Dogfood

`DESIGN_OPTION` — El de §21: `Implementá Effect Admission para SAE.`, en **dos ejecuciones**, con el
punto 13 (modificación de una premisa) y el 15 (preservación de la declaración humana) en el mismo
acto humano.

### 22.10 Stop conditions

`DESIGN_OPTION` — El Change **se detiene y escala** si:

```text
S-1   alguna decisión HD-* reaparece como no resuelta (en particular HD-INT-D)
S-2   el alcance exige Protocol (protocol/.agents/) → la vía cambia a RFC-56 Clase A: STOP y re-emitir
S-3   el alcance exige una authority class, entidad, registry, namespace o state machine nueva
S-4   el alcance exige tocar el Placement Contract (PC-10/PC-20)
S-5   el alcance exige reescribir historia (corpus histórico)
S-6   aparece una contradicción normativa que el modelo no puede resolver sin inventar precedencia
S-7   una modificación necesaria para implementar la norma cambia el comportamiento del host o de SAE
S-8   la derivación no puede producir un artefacto sin completar una parte Forbidden-to-infer
S-9   cualquier determinación de cierre resultaría `DEFERRED` sin una pending decision existente (PC-1)
```

### 22.11 Human decisions (sólo las que siguen abiertas)

`PC-1` (`resolución: pendiente`) — Cinco, **ninguna bloqueante para el diseño** (`HD-INT-G`, `HD-M2`, `HD-M3`,
`HD-M4`, `HD-M5`); `HD-M2` bloquea la **ejecución 2** del dogfood (§25).

---

## 23. Deliverables

`DESIGN_OPTION` — Orden interno de ejecución, con la razón de la secuencia (cada paso habilita la
verificación del siguiente):

```text
0.  DECISIÓN HUMANA HD-INT-D (forma y registro de la Note)                         ← bloqueante
1.  D-1 norma: INV-1 … INV-5 + vigencia en docs/CONVENTIONS.md
2.  D-2 formato: docs/plans/_TEMPLATE.md
3.  D-4 realización read-only de las fuentes §13.3 + enrutamiento
4.  D-5 guarda de divergencia (± tests)
5.  D-3 runtime/orchestrator/intent.py (derivación pura)
6.  D-6 consumo por el host + matriz de governance
7.  D-7 verificaciones de forma (patrón C-1/C-2/C-3)
8.  D-8 operación + columna derivada de INDEX + CHANGELOG
9.  DOGFOOD (§21), dos ejecuciones, con falsación de V-1 … V-15
10. cierre: anchor, gates, checkpoint, determinaciones de impacto, Closed
```

`DESIGN_OPTION` — **Orden justificado:** la norma precede a la implementación (si no, el ejecutor
sería fuente normativa); la realización precede a la derivación (la derivación cita, no copia); la
guarda precede al consumo (para que la divergencia se detecte antes de que el host dependa de la
tabla); el dogfood va **después** de todo (falsación, no desarrollo).

---

## 24. Stop Conditions

`DESIGN_OPTION` — Condiciones de parada del **Change** (§22.10) y de la **derivación** (§7.4),
separadas porque detienen cosas distintas:

| Quién se detiene | Condición | Qué produce | Qué NO hace |
|---|---|---|---|
| **La derivación** | `GAP` + `NEEDS_CLARIFICATION` | pedido de aclaración con el formato de `NO_ASSUMPTIONS` | no asume, no completa por defecto |
| **La derivación** | `ANOMALY` / `BOUNDARY` | escalación con **todas** las fuentes en conflicto y el punto de incompatibilidad | no elige, no jerarquiza, no «armoniza» |
| **La derivación** | `REQUIRES_HUMAN` | escalación de la decisión, con dueño y bloqueo | no bloquea en silencio, no registra sin nombrar la reserva |
| **La derivación** | `STOP-1` (`FI-1`…`FI-10`) | `STOP` / `REQUIRES_HUMAN` | no re-deriva una decisión que no es suya |
| **La derivación** | `R-5` | `GAP` + `NEEDS_CLARIFICATION` | no asume que la derivación sobrevive ni que murió |
| **El host** | `STOP_AWAIT_PLAN_AUTHORIZATION` | parada existente | **sin cambio** |
| **El host** | `STOP_SCOPE_VIOLATION` (post-`pin`) | parada existente | **sin cambio** |
| **El host** | los 21 stops de `contracts.py:STOP_ACTIONS` | parada existente | **sin cambio** |
| **El Change** | `S-1`…`S-9` (§22.10) | escalación con evidencia | no reinterpreta el alcance |

`FACT` — **Ninguna stop condition nueva reemplaza ni debilita una existente.** Las nuevas son de la
**derivación** (pre-autorización); las del **host** (post-autorización) quedan intactas.

---

## 25. Human Decisions Remaining

`PC-1` (`resolución: pendiente`) — Sólo las que **realmente** siguen abiertas, con la **evidencia que falta**
para cada una (Fase 1, F4). De las catorce del conjunto, **nueve están adoptadas** por el acto humano del
mantenedor (2026-10-02) y registradas en §3.2; `HD-INT-E2` es consecuencia **derivada** de `HD-INT-E`; y
`HD-K1`…`HD-K4` **permanecen pendientes** (metadata en `HDK §16.2`). `HD-INT-B` en particular está
**cerrada** por ese acto y este documento **no** la reabre.

| ID | Decisión | Por qué es humana | Evidencia faltante (Fase 1) | Impacto si no se decide | Dueño | Bloquea |
|---|---|---|---|---|---|---|
| **`HD-INT-G`** | **Registro en gobernanza de los artefactos ya producidos sin Plan** (`docs/architecture-capability-review.md`, el inventario externo y las investigaciones Working): ¿entran como artefacto registrado, como provenance versionada, o permanecen externos al repositorio? | `PC-52` («una petición no es una autorización») y `PC-27`/`PC-28` (la excepción de placement se registra en el artefacto que posee la decisión, y una segunda instancia de la misma desviación exige su propia autorización) | **nunca fue resuelta**: está declarada abierta por I-23 §16 y por `DEF-6` de este diseño, y ningún artefacto registra un acto de resolución | las citas Working del futuro artefacto de gobernanza no resuelven contra copia versionada (RFC-69 I2, `tests/test_repo_containment.py`); el análisis más útil del repositorio queda fuera de su gobernanza | mantenedor | no (condiciona el registro del Plan, no el diseño) |
| **`HD-M2`** | **Punto de admisión de un efecto** (`Effect Admission`): sólo DEV (opción 1), DEV + payload (opción 2), u otra | es una decisión de alcance/arquitectura: `FI-3` + `AU-6` (ADR-worthiness es juicio humano). El repositorio **no** la determina: el payload define la admisión por **efectos declarados** y el ejecutor DEV por **paths y clases de acción** — clasificación: `GAP` de ejecutor + divergencia (§21.1) | **ningún acto humano registrado**; la decisión de dominio y vía no es inferible de las fuentes | el dogfood no puede pasar de la ejecución 1; **no** bloquea el Change, bloquea **ese** trabajo | mantenedor | no (bloquea el dogfood de la **ejecución 2**) |
| **`HD-M3`** | **Vía de gobernanza del propio Change**: ¿basta el Plan con los invariantes en `docs/CONVENTIONS.md` (recomendado, `HD-INT-H`/`HD-K4`), o se eleva además un ADR por ser un invariante arquitectónico persistente (`AU-6`)? | `AU-6` declara ADR-worthiness como **juicio humano**, no como test mecánico; `PC-75`/`ADR-16` reservan la decisión | este Diseño la declaró **abierta**; el Plan §21.2 de la versión previa y `docs/working/proposals/INDEX.md` la afirman resuelta **sin acto fechado y sin figurar en §3.2** → falta el acto humano (o su confirmación registrada) | el Change se ejecuta por Plan; la decisión sólo afecta a si se registra además un ADR | mantenedor | no |
| **`HD-M4`** | **Columna de vigencia en los INDEX de gobernanza**: ¿se agrega la vista derivada en `docs/plans/INDEX.md` (y los de RFC/ADR), o el lifecycle queda sólo en el header? | `HD-INT-I` decidió que **si** aparece, sea derivada; **no** decidió si aparece. Toca INDEX (DESCRIPTIVE) y su verificador | este Diseño la declaró **abierta**; el Plan §21.2 de la versión previa y `docs/working/proposals/INDEX.md` la afirman resuelta **sin acto fechado y sin figurar en §3.2** → falta el acto humano (o su confirmación registrada) | sin la columna, la vigencia sigue siendo legible **por artefacto** pero no navegable en el espejo. No afecta la norma ni la derivación | mantenedor | no |
| **`HD-M5`** | **`premises(D)` en el artefacto o sólo referencia a fuentes**: ¿la sección se materializa con las ocho clases (recomendado, `HD-K3`), o basta citar fuentes en prosa? | `HD-K3` decidió que `premises(D)` es **obligatorio**; queda abierto el **grado de materialización** (ocho filas vs prosa) | este Diseño la declaró **abierta**; el Plan §21.2 de la versión previa y `docs/working/proposals/INDEX.md` la afirman resuelta **sin acto fechado y sin figurar en §3.2** → falta el acto humano (o su confirmación registrada) | con prosa, `R-5` pasa de excepción a regla (toda modificación humana sería `UNDETERMINED`) | mantenedor | no |

`FACT` — **Consolidación de identificadores (Fase 1, F3).** La fila que esta tabla declaraba abierta y
**bloqueante** bajo el id previo `HD-M1` era un **duplicado** de `HD-INT-D`: misma pregunta («dónde vive y
cómo se registra la Note»), mismas tres opciones (A `docs/plans/`, B `docs/working/…`, C familia nueva) y
misma resolución — **Opción A**. `HD-INT-D` es la decisión ya adoptada y registrada en §3.2, de modo que
su consecuencia de bloqueo queda sin efecto: la forma de la Note **es** decidible y su detalle mínimo
(§14.3) es un `DESIGN_OPTION` condicionado a esa Opción A. El id `HD-M1` se elimina y no se reutiliza.

`FACT` — Se verificó explícitamente que **ninguna** de estas cinco decisiones es inferible de una
norma existente sin inventar precedencia o sin crear un mecanismo, autoridad o entidad nueva.

`FACT` — **`HD-K1`…`HD-K4` permanecen pendientes** (acto del mantenedor, 2026-10-02): no fueron
adoptadas y **no** se infieren de la adopción del núcleo `HD-INT-*`. Su registro y su metadata `PC-1`
viven en su artefacto dueño (`INVESTIGACION_MODIFICACION_HUMANA_DERIVACION_2026-09-23.md §16.4`, HDK);
su estado de autoridad se registra en §3.2.

`FACT` — **Decisiones que este diseño NO reabre** (declarado para evitar ambigüedad): `HD-INT-B` (§3.2,
cerrada por el encargo), `HD-K1` (reducción de scope requiere re-derivación: **adoptada**, no se
introduce excepción), `C-2`/`CI`, Plan 121, R4, RFC-68 Fase 2, Placement Contract, `protocol/.agents/`.

---

## 26. Deferred Items

`DESIGN_OPTION` — Fuera de este Change, con su dueño y su razón:

| # | Ítem diferido | Dueño | Por qué queda fuera |
|---|---|---|---|
| `DEF-1` | **Re-derivación local (subgrafo afectado)** | este modelo, reabrible con evidencia | exige el **grafo de dependencias campo→premisa** declarado, que hoy no existe. Si `D-2`/`D-3` lo materializaran, `D-1` se vuelve decidible. En el MVP: re-derivación **total** |
| `DEF-2` | **Vigencia por sección** (artefactos con partes diferidas, como RFC-68 Fase 2) | RFC-68 / este modelo | hoy alcanza el mecanismo existente de **secciones diferidas declaradas**; no hay evidencia de más casos |
| `DEF-3` | **Detección y propagación mecánica de impacto** | RFC-68 **Fase 2** | ya decidida y **diferida con gates declarados** (telemetría, índice de trazabilidad verde sobre sesiones reales, correlación validada sobre ≥2 conjuntos multi-proyecto). Abrirla es decisión humana |
| `DEF-4` | **Machine-locatability de las excepciones de Placement** | Placement Contract | `PC-31c` declara que «is **not prohibited**; it is simply not decided in favour of here». No se reabre |
| `DEF-5` | **Contradicciones del payload del Protocol** | RFC-56 / RFC-79 | el Protocol tiene su propia gobernanza; `A-19` de I-23 §16 lo prohíbe como parte de este diseño |
| `DEF-6` | **Regularización retroactiva de artefactos huérfanos** (`docs/architecture-capability-review.md`, `MASTER_PENDING_WORK_INVENTORY.md`, las investigaciones Working) | mantenedor | `HD-INT-G` de I-23 sigue abierta; este diseño **no** la resuelve y **no** reclasifica nada retroactivamente. **Fase 1 (F6) — determinación registrada:** `docs/architecture-capability-review.md` es `Working / Analysis` → namespace canónico `docs/working/audits/` con fila en `docs/working/audits/INDEX.md`, y su ubicación actual en la raíz de `docs/` **no** tiene excepción registrada (`PC-52`/`PC-27`/`PC-28`; su cita de `PC-75` para esa excepción es improcedente); `MASTER_PENDING_WORK_INVENTORY.md` **no es un artefacto del repositorio** —lo declaran su propio header y siete planes commiteados (p. ej. `docs/plans/141-human-decision-backlog-resolution.md:326`: «no se modifica, no se commitea y no es autoridad»)— → sin fila de INDEX y sin commit. **La ejecución** de ambos (mover y registrar, o sacar del árbol de trabajo) queda reservada a `HD-INT-G` |
| `DEF-7` | **Registro de gobernanza del propio Change (el Plan que ejecute este diseño)** | el mantenedor al autorizar | crear un Plan es lo que este Change habilitará; crearlo **ahora** violaría la restricción del encargo |
| `DEF-8` | **Calidad de evidencia de la consistencia auto-escrita** (`governance.py` escribe `PASS` y `observation.py` lo relee) | I-22 §3.6(b) | es un hallazgo sobre un mecanismo **existente**, medido por I-22 y clasificado `PARTIALLY_IMPLEMENTED` con `GAP` de calidad. **No** se arregla aquí; sí condiciona el diseño (§19.3): el registro de premisas **nunca** es la única evidencia de la validez de una derivación |

### 26.1 Hallazgo separado: el checker de citas y `docs/working/`

`FACT` — I-23-HDK §4.8 (E-8) encontró, por medición reproducible, que
`tools/check_plan_citations.py:scan_documents` construye su universo de fuentes con `docs/plans`,
`docs/rfc`, `docs/adr` y los `ROOT_DOCS`, y **no recorre `docs/working/`**. Verificación de I-23-HDK:
de las 220 fuentes escaneadas, **ninguna** es de `docs/working/`.

`DESIGN_OPTION` — **Evaluación de si afecta directamente a este diseño.** Se evaluó y la respuesta es
**no, mientras el artefacto de gobernanza no cite fuentes Working untracked**:

| Pregunta | Respuesta | Consecuencia para este diseño |
|---|---|---|
| ¿El artefacto de gobernanza del Change vivirá en `docs/plans/` o `docs/rfc/`? | **sí** | esos directorios **sí** son fuentes del checker |
| ¿Citará fuentes Working? | **sí** — `docs/architecture-capability-review.md:4.2` y las tres investigaciones son provenance legítima (`LV-4`) | **consecuencia directa:** si esas fuentes estuvieran **untracked** al crear el artefacto de gobernanza, la contención (RFC-69 I2, `tests/test_repo_containment.py`) **sí** aplicaría |
| ¿Este diseño depende de que el checker recorra `docs/working/`? | **no** | el diseño no depende de la contención de Working desde Working |
| ¿El diseño depende de que las fuentes Working estén versionadas? | **sí, indirectamente** | `P-3`/`P-6` exigen citar la fuente de `docs/architecture-capability-review.md`; si está untracked al crear el artefacto de gobernanza, la contención puede fallar |

`DESIGN_OPTION` — **Registro como residual independiente, sin mezclarlo con el Change** (`DEF-9`):

```text
DEF-9  tools/check_plan_citations.py:scan_documents no recorre docs/working/
       Naturaleza: hallazgo residual de VERIFICACIÓN, independiente del Change.
       No se modifica el checker en este trabajo (restricción del encargo).
       Único efecto sobre el diseño: §22.2 debe exigir que las fuentes Working que el
       artefacto de gobernanza cite estén VERSIONADAS antes de crear ese artefacto
       (o que la cita se sustituya por una fuente versionada equivalente).
       No es un prerequisito del Change: es una condición de su registro de gobernanza.
```

`FACT` — Esta es la respuesta exacta a la instrucción «evaluá únicamente si afecta directamente al
diseño propuesto; si no afecta, registralo como residual independiente». **Afecta de forma acotada y
condicional** (a la contención de las citas del artefacto de gobernanza), y por eso se registra como
residual **con** su consecuencia concreta, sin abrir un Change paralelo ni tocar el checker.

---

## 27. Final Recommendation

### 27.1 Qué ya existe

`FACT`:

```text
· Change Lifecycle (RFC-75) con 15 mecanismos, 11 de ellos IMPLEMENTED o parcialmente operativos
· el gate de autorización binario y su vocabulario cerrado de 21 stops y 3 veredictos de autoridad
· la frontera SAE endurecida por incidentes reales: scope all-or-nothing, checkpoint no retroactivo,
  prohibición de scope expansion autónoma, verificación post-delegación como defensa en profundidad
· la distinción representación/significado ya implementada (_canonical_text) con su test
· anchors (A1/A2), checkpoints, lineage de findings/corrections, pending decisions per-artifact
· las condiciones derivadas (Verified/Executed/Committed/Closed/Promoted/Released)
· las determinaciones de cierre (documentation/roadmap impact) con su stop condition
· el patrón «fuente normativa → realización read-only → guarda de divergencia → escalación»
  probado para Placement
· el vocabulario de lifecycle documental (active/archived/superseded/deprecated) y la cláusula legacy
· el modelo de incertidumbre GAP/ANOMALY/FAIL/BOUNDARY/N-A/EXCLUDED
```

### 27.2 Qué falta

`GAP` — `G-1`…`G-8` de §5.1: derivación de la intención, criterio de derivabilidad post-contexto,
`work_type`, reglas aplicables, vigencia materializada, forma de la Nota, procedencia de la derivación,
y criterio de granularidad al **proponer**.

### 27.3 Qué se implementará

`DESIGN_OPTION` — Los ocho grupos de `D-1`…`D-8` (§22.4), en el orden de §23: cinco invariantes en
`docs/CONVENTIONS.md`; campos y secciones nuevas en el template; **un** módulo de derivación pura;
una realización read-only de las fuentes con su guarda de divergencia; el consumo por el host y la
matriz de governance; verificaciones de forma extendiendo el patrón C-1/C-2/C-3; operación y columna
derivada; y el dogfood de §21.

### 27.4 Qué **no** se implementará

`DESIGN_OPTION`:

```text
· ninguna entidad (Intent, WorkUnit, Feature, Change), ningún registry, ninguna base de datos
· ninguna state machine; `proposed` sigue siendo `Aprobado para redacción`
· ninguna authority class nueva; ninguna primitive de identidad
· ninguna segunda fuente normativa; ningún RFC ni ADR nuevo (los invariantes van a CONVENTIONS.md)
· ningún reemplazo de INTENT_CONFIDENCE (se conserva, mide el texto)
· ninguna migración del corpus histórico (153 planes, 80 RFCs, 18 ADRs: 0 modificaciones)
· ningún cambio de semántica en authority.py, autonomy.py ni SAE
· ninguna excepción para reducciones de scope «inocuas» (HD-K1)
· ningún checker que interprete prosa; ningún scoring de impacto semántico
· ningún namespace nuevo (ni `docs/notes/`)
· DEF-1…DEF-9 (§26): re-derivación local, vigencia por sección, RFC-68 Fase 2,
  machine-locatability de excepciones de Placement, contradicciones del payload,
  regularización retroactiva, el Plan del propio Change, la calidad de evidencia auto-escrita
  y el hallazgo del checker de citas
```

### 27.5 Qué decisiones siguen siendo humanas

`PC-1` (`resolución: pendiente`) — **Nueve**, ninguna bloqueante para el diseño: `HD-INT-G` (registro en
gobernanza de los artefactos producidos sin Plan), `HD-M2` (punto de admisión de un efecto; bloquea la
**ejecución 2** del dogfood), `HD-M3` (ADR además del Plan), `HD-M4` (columna de vigencia en los INDEX),
`HD-M5` (grado de materialización de `premises(D)`) —las cinco de §25— y `HD-K1`, `HD-K2`, `HD-K3`,
`HD-K4` (vía de gobernanza de los invariantes de HD-K; metadata en `HDK §16.2`), que el acto humano del
2026-10-02 **no** adopta.

### 27.6 Qué queda fuera

`DESIGN_OPTION` — El corpus histórico, el Protocol, el Placement Contract, la Fase 2 de RFC-68, la
regularización de huérfanos, la re-derivación local, la vigencia por sección y el checker de citas
(§26).

### 27.7 El único Change que debería ejecutarse posteriormente

`DESIGN_OPTION`:

> **Un único Change integral**, autorizado por **un Plan** `Aprobado para ejecución`, con
> **Clase B/DEV** (sin efecto payload) **si y sólo si** `HD-M2` se resuelve con la opción 1
> («sólo DEV»); con **Clase A de RFC-56** (RFC `Accepted` + plan) si `HD-M2` incluye el payload.
> El Plan debe declarar: `**Work type:** mechanism`, `**Change Level:** L2–L3` (multi-área:
> `docs/` + `runtime/` + `tools/` + `tests/`), `**Origen:**` esta propuesta + las tres
> investigaciones, y su sección `## Derivación y premisas` con las ocho clases — porque el propio
> Change es el primer consumidor de la norma que introduce.

**Condición de arranque:** `HD-INT-D` resuelta. **Condición de cierre:** `V-1`…`V-15` de §19 con el
dogfood de §21 ejecutado en sus dos ejecuciones, corpus histórico intacto y batería canónica verde.

### 27.8 Conclusión

`DESIGN_OPTION` — El modelo `Intent → Context → Derivation → Plan/Note → Human modification →
Re-derivation → Authorization → SAE` **puede implementarse** reutilizando al máximo los mecanismos
existentes, con **un** módulo nuevo, **seis** campos/secciones aditivas, **cinco** invariantes
normativos y **un** dogfood. No requiere una arquitectura paralela, no crea autoridad nueva, no toca
la frontera SAE y no modifica el corpus histórico. La parte más fuerte del diseño no es lo que deriva:
es **dónde se detiene**, y el dogfood elegido lo demuestra.

---

## Registro de no-modificación

`FACT` — Confirmación explícita, verificable con `git status --short`:

| Artefacto | Estado |
|---|---|
| `protocol/.agents/`, `protocol/_AGENTS.md`, `dist` | **no modificados** |
| `runtime/`, `tools/`, `tests/`, `.agents/` | **no modificados** |
| `docs/rfc/`, `docs/adr/`, `docs/plans/` (incluidos los 153 planes) | **no modificados** |
| `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/AGENTS.md`, `docs/placement-contract.md` | **no modificados** |
| `AGENTS.md` (raíz), `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `VERSION` | **no modificados** |
| INDEX de gobernanza | **no modificados** |
| CI (`.github/workflows/`) | **no modificado** |
| **Creado** | `docs/working/proposals/DISENO_CHANGE_INTEGRAL_INTENT_DERIVATION_PLAN_NOTE_AUTORIZACION_SAE_2026-09-23.md` (este documento) |
| **Modificado** | `docs/working/proposals/INDEX.md` — **una fila de registro** de la familia `Working analysis` |
| Commits, tags, releases, push, merges, promoción | **ninguno** |
| Registries, entidades, state machines, namespaces, authority classes, primitive de identidad | **ninguna** |
| Plan / RFC / ADR | **ninguno** (el Plan es el entregable **recomendado**, no creado) |
