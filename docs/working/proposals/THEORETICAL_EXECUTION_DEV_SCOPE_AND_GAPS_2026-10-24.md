# Theoretical Execution (DEV) — reconstrucción de alcance, matriz de gaps y decisión de cierre

**Clase documental:** Working / Proposal — **no normativo**; provenance del diseño que
ejecuta el Plan 176. **Fecha:** 2026-10-24. **Base de la reconstrucción:** `f613147`
(`dev` = `master` = cierre del Plan 175). **Autoridad de este documento:** ninguna;
registra hechos, inferencias, hipótesis y la decisión de alcance que el Plan 176
materializa y ejecuta. No crea gate, lifecycle, registry, autoridad ni capacidad.

Marcas usadas: `FACT` (observado en el árbol o en Git), `INFERENCE` (derivación con
evidencia citada), `HYPOTHESIS` (conjetura sin evidencia suficiente), `DECISION`
(decisión nueva de esta misión, registrada en el Plan 176), `LIMIT` (límite declarado).

---

## 1. Corpus de evidencia

`FACT` — el corpus consultado es el árbol completo en `f613147`: `AGENTS.md`,
`.agents/` (workflow y policies), `docs/rfc/`, `docs/adr/`, `docs/plans/`,
`docs/working/`, `docs/glossary/`, `ROADMAP.md`, `CHANGELOG.md`, `runtime/`,
`tools/`, `tests/` y `protocol/`. La búsqueda de toda referencia a Theoretical
Execution se hizo con `Select-String` sobre `*.md`, `*.py`, `*.json`, `*.yaml`, sin
excluir `protocol/` ni `dist` (este último no existe como directorio de trabajo: es
la rama publicada).

`FACT` — todas las referencias a TE en el árbol vivo son: `docs/plans/175-…`,
`docs/plans/INDEX.md` (sección y fila del Plan 175),
`docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md`,
`.agents/policies/theoretical-execution.md`, `.agents/AGENTS.md` (una fila de
puntero), `runtime/README.md` (una sección), `CHANGELOG.md` (una viñeta) y las ocho
suites `tests/test_theoretical_*.py`. `docs/plans/174-…` menciona TE como **método
usado** (TE T1–T15 del Plan 174), no como capacidad definida. No existe ninguna otra.

`FACT` — no existe RFC que defina TE, ni ADR, ni iniciativa en `ROADMAP.md`, ni
entrada en `docs/glossary/`. La única evidencia de una mención en el payload es
`protocol/.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`, donde la
palabra «theoretical» califica a `LAYERED_ARCHITECTURE.md`: no es TE y no se
relaciona con esta capacidad.

`INFERENCE` — la definición operativa de TE vive, por lo tanto, en dos artefactos
DEV: el Plan 175 (diseño y criterios de aceptación) y su policy operativa. No hay
una definición normativa superior que la complete ni que la prohíba.

---

## 2. Historia de TE en el repositorio

| # | Hecho | Evidencia |
|---|---|---|
| H-1 | TE nace como **ejecución hipotética no mutativa** de un Implementation Plan commiteado, antes de su materialización. | `docs/plans/175-theoretical-execution-dev-v1.md:Objetivo` |
| H-2 | El problema operacional que resuelve: evaluar una propuesta **sin ejecutarla**, sin escribir, sin producir evidencia factual, separando recomendación de autorización. | `docs/plans/175-theoretical-execution-dev-v1.md:1. Scope and non-scope`; `.agents/policies/theoretical-execution.md:1. What TE is and is not` |
| H-3 | El diseño cerrado fija: overlay declarado trivaluado, identidades factual/proyectada/input/run, cinco dimensiones (tres del productor, dos del engine), CH-1…CH-8, `status` derivado, `--emit/--validate/--stale/--compare`, sin persistencia propia. | `docs/plans/175-theoretical-execution-dev-v1.md:2. Architecture`; `docs/plans/175-theoretical-execution-dev-v1.md:8. Identity and provenance` |
| H-4 | El Gate B real fue un run del productor sobre el Plan 175: `CONVERGED`, 49/49 ítems, cinco dimensiones, 0 findings, 0 obligaciones. | `docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md` |
| H-5 | Durante el cierre del Plan 175 se detectaron y corrigieron dos problemas reales con TE: CH-7 comparaba la `State identity` del ancla con el tree del estado de cierre, y el parser del ancla descartaba archivos raíz (`CHANGELOG.md`). | `docs/plans/175-theoretical-execution-dev-v1.md:Findings`; `docs/plans/175-theoretical-execution-dev-v1.md:Nota de ejecución` |
| H-6 | El Plan 175 declara explícitamente **fuera de alcance** (de v1, no del universo TE): `protocol/`, `dist/`, `VERSION`, `ExecutionHost`, `derivation.py`, la batería, *discovery/audit/post-execution TE*, adaptador RFC, persistencia propia, `.project` store, provider/model/network/credentials, lifecycle/Change/findings/decisiones nuevos, `scenarios[]` y `ResultContentIdentity`. | `docs/plans/175-theoretical-execution-dev-v1.md:1. Scope and non-scope` |
| H-7 | La policy prohíbe de forma **permanente**: importar `ExecutionHost`, escribir `protocol/.agents/`, crear un segundo sistema de Change/findings/decisiones, autorizar/commitear/promover/releasear, y declarar garantías semánticas. | `.agents/policies/theoretical-execution.md:13. Boundaries` |
| H-8 | El Plan 175 declara «Discovery/audit/context recovery/orchestration: **sin integración**» y «Execution: TE no participa; el host no lee TE». | `docs/plans/175-theoretical-execution-dev-v1.md:15. Integration` |
| H-9 | El estado de TE v1 quedó verificado: 8 checkers PASS, `pytest tests/` 1481 PASS, C-1/C-2/C-3 sin `ANOMALY`, Gate B `CONVERGED`, `--validate`/`--stale`/`--compare` con los exit codes previstos. | `docs/plans/175-theoretical-execution-dev-v1.md:Validation anchor` |
| H-10 | El Plan 175 está `Executed` con condición derivada `Closed`; su anchor y checkpoint fueron commiteados en `f613147`. | `docs/plans/175-theoretical-execution-dev-v1.md:Checkpoint / cierre` |
| H-11 | `docs/plans/INDEX.md` sigue describiendo el cierre del Plan 175 como «cierre en curso (Validation Anchor/Checkpoint)» y «con Validation Anchor/Checkpoint pendientes», pese a que `f613147` los registró. | `docs/plans/INDEX.md` (sección y fila del Plan 175) vs `f613147` |

`FACT` — H-11 es una inconsistencia documental verificable: el espejo INDEX describe
un estado que el artefacto ya no tiene. No es un `ANOMALY` de gobernanza (el INDEX es
registro, no autoridad), pero es documentación current-state desactualizada.

`INFERENCE` — las exclusiones de H-6 son de **scope del Plan 175**: el propio
documento las enuncia como tales, y ningún artefacto del repositorio las convierte en
prohibición permanente. Las de H-7 son de otra naturaleza: son **fronteras
constitutivas** de TE (si TE ejecutara, autorizara o gobernara, dejaría de ser TE).

`HYPOTHESIS` — que las áreas excluidas por el Plan 175 deban estar en el alcance
completo de TE DEV. No hay evidencia documental que lo afirme; el prompt de la misión
lo plantea como pregunta abierta, no como hecho. Por eso se resuelve como `DECISION`
(§5), no como derivación.

---

## 3. Definición operativa: TE DEV COMPLETE

`DECISION` — **TE DEV COMPLETE** es la capacidad DEV, cerrada y verificable, que:

| Pregunta | Respuesta |
|---|---|
| Problema que resuelve | Atravesar una propuesta de cambio commiteada **antes** de materializarla, detectando inconsistencias mecánicas y dejando registrada la evaluación semántica del productor, sin ejecutar, escribir ni autorizar. |
| Entradas | (a) base factual: commit/tree resoluble; (b) propuesta: un `docs/plans/NN-*.md` commiteado en esa base, no `Superseded`; (c) check-set y `tool_version`; (d) opcional: resultado previo (para no-progress) y techo de revisión; (e) atestación del productor. |
| Salidas | Un valor `TE_RESULT` (JSON canónico) con: identidades, registro de los checks del engine, claims (una por ítem enumerado), dimensiones, findings, correcciones, obligaciones de verificación, escalaciones, riesgos residuales, límites, fingerprint y `status` **derivado**. |
| Capacidades incluidas | Overlay declarado; enumeración completa de la propuesta; CH-1…CH-9 deterministas; registro de checks recomputable; dimensiones semánticas atestiguadas; autoridad mecánica; obligaciones de verificación; validación de contrato; `status` derivado; staleness; comparación estructural; fingerprint de no-progress; CLI de solo lectura. |
| Capacidades excluidas | Ejecución real del Plan; post-ejecución como evidencia; autorización; governance; promoción/release; persistencia propia; store; `.project`; modelo/provider/red/credenciales; segundo lifecycle; segundo orquestador; `ResultContentIdentity`; `scenarios[]`. |
| Autoridad que posee | Observar, analizar, detectar, simular, proponer correcciones, derivar obligaciones, clasificar escalaciones, recomendar y detenerse. |
| Autoridad que no posee | Autorizar, aprobar, aplicar, commitear, cerrar, promover, releasear, resolver findings, crear decisiones pendientes, declarar verdad factual o garantía semántica. |
| Puede observar | Objetos Git de la base (commits, trees, blobs), el texto de la propuesta en la base, el registro que la propia corrida produce. |
| Puede simular | El estado proyectado **solo estructuralmente**: paths declarados desconocidos, contenido no fabricado, efectos declarados como clases. No simula la ejecución de los pasos. |
| Puede modificar | Nada. No abre archivos en modo escritura, no ejecuta shell, no toca el índice ni el working tree. |
| Evidencia que produce | Un valor teórico: identidad de inputs, registro determinista de checks, cobertura, findings, obligaciones. Es evidencia de **la evaluación**, no del mundo. |
| Evidencia que nunca produce | `PASS`, `VALID` de corrección, `VERIFIED`, `EXECUTED`, `COMMITTED`, `RELEASED`; ninguna evidencia factual sobre el resultado de materializar la propuesta. |
| Integración DEV | Capacidad **invocable** por CLI desde el Change que la necesite; el resultado, si se cita, se persiste en el artefacto que lo cita (Plan o Working). No es gate, no es fase, no es estado. |
| Recuperación | Sin estado parcial: se re-ejecuta desde los mismos inputs; el skeleton es recomputable y determinista; la aplicabilidad se reconstruye con `--stale`. |
| Siguiente paso | Lo determina el `status` derivado y la lectura humana: corregir la propuesta y re-ejecutar (no hay bucle en el engine), o escalar. |
| Terminación | Una pasada: no hay iteración interna. El techo de revisión y el fingerprint de no-progress son guardas declaradas, no autorizaciones. |
| No-progress | Fingerprint determinista de (ítems, checks, findings materiales, `status`) comparable con el de la corrida anterior declarada. |
| Stale | El resultado es aplicable a HEAD solo si su `InputIdentity` recompone en HEAD; si HEAD avanzó, es `stale` (aplicabilidad, no verdad). |
| Identidad | `InputIdentity` determinista gobierna staleness; `RunIdentity` es etiqueta; no hay identidad de contenido del resultado semántico. |
| Prueba | Suites unitarias, de integración, de contrato, de aislamiento, adversariales y un dogfood anclado sobre el Plan 175. |
| Auditoría | El `TE_RESULT` registra identidad, checks, cobertura, claims, findings, obligaciones y límites: es reconstruible por un tercero. |
| Documentación | La policy operativa describe exactamente lo que existe; el diseño y los criterios viven en el Plan 176 y en este registro. |

`DECISION` — TE DEV COMPLETE **no** incluye un modelo de ejecución hipotética por
pasos (simulación de operaciones). Simular operaciones exigiría un intérprete de
efectos, un modelo de estado mutable y una semántica de fallos: sería construir un
segundo engine de ejecución dentro de TE, contra `AGENTS.md:Decision-Making Compass` y
contra la frontera de `.agents/policies/theoretical-execution.md:13. Boundaries`.
La cobertura de escenarios se registra en `dimensions.adversarial.probed`, como ya
fija el Plan 175.

---

## 4. Matriz de gaps (dimensiones A–Q)

Clases: `REQUIRED` (entra en esta misión), `OPTIONAL`, `OUT_OF_SCOPE_PERMANENT`,
`OWNED_BY_OTHER_COMPONENT`, `DEFERRED`.

| Dim. | Capacidad | Estado actual (`FACT`) | Esperado en TE DEV completo | Gap | Clase | Acción | Racional | Verificación |
|---|---|---|---|---|---|---|---|---|
| A | Theoretical proposal | La propuesta es un Plan commiteado; se lee de la base y se enumera. | Igual, con enumeración completa y sin omisiones silenciosas. | Las líneas de `## Entregables` sin path resoluble y los paths que escapan se **descartan en silencio** (`proposal.py:_deliverables`/`_paths_from_text`). | `REQUIRED` | D-5: registrar y señalar (CH-9). | Un ítem declarado que no se enumera no puede recibir claim: la cobertura mentiría. | `test_theoretical_checks.py` CH-9; `test_theoretical_proposal.py` |
| B | Projection | Overlay trivaluado solo sobre objetos Git. | El estado proyectado no depende del índice ni del working tree. | CH-3 resuelve citas y estado del artefacto leyendo el **working tree** (`verify_citation`, `_artifact_status`); CH-7 recomputa el delta desde el **índice**. | `REQUIRED` | D-1: resolver ambos contra la base. | Dos corridas con el mismo `InputIdentity` pueden dar checks distintos: la identidad de inputs deja de gobernar el resultado. | `test_theoretical_checks.py` (independencia de working tree e índice) |
| C | Identity | `InputIdentity` determinista; `RunIdentity` etiqueta; sin `ResultContentIdentity`. | Igual, con etiqueta determinista y check-set versionado. | El nonce de `run_identity` usa `id(inputs)` (dirección de memoria): dos corridas con los mismos inputs y el mismo timestamp producen `te_id` distinto. | `REQUIRED` | D-4: nonce derivado de contenido. | Una etiqueta no reproducible impide reconstruir la corrida y no aporta nada. | `test_theoretical_identity.py` |
| D | Checks | CH-1…CH-8. | Checks suficientes para el alcance declarado, versionados. | No hay check de integridad de la declaración (entregable irresoluble/escape, clase de efecto fuera del vocabulario cerrado). | `REQUIRED` | D-5: CH-9 `declaration integrity`. | Es la superficie donde una propuesta puede ocultar trabajo sin mentir explícitamente. | `test_theoretical_checks.py` |
| E | Semantic dimensions | Tres del productor (atestiguadas) + dos del engine; el engine nunca las marca `PERFORMED`. | Igual. La separación productor/engine sigue siendo correcta. | Ninguno. | `OPTIONAL` (sin cambio) | — | El engine no tiene skill executor; atribuirle semántica sería una garantía falsa (Plan 175 §5.2). | `test_theoretical_isolation.py` |
| F | Findings | Nacen del engine (checks y gaps) o del productor; `TF-nn`, disposición `OPEN/ESCALATED/RESIDUAL`; corrección `applied:false`; revalidación = nueva corrida. | El finding del engine no puede desaparecer del resultado. | `--validate` no recomputa los checks: un productor puede **borrar** el finding de un `ANOMALY` y derivar `CONVERGED`. | `REQUIRED` | D-2: registro de checks + re-derivación. | Falsa convergencia: el riesgo central del mecanismo. | `test_theoretical_result.py` (finding eliminado/alterado) + `test_theoretical_adversarial.py` |
| G | Verification obligations | Derivadas por el engine o por claims `NOT_EVALUABLE`; `status: OPEN`; nunca satisfechas por TE. | Trazables y recomputables desde el resultado. | Sin registro de checks, las obligaciones del engine no son recomputables ni auditables; solo existen como lista declarada. | `REQUIRED` | D-2. | Una obligación que no se puede re-derivar es una afirmación del productor, no un puente. | `test_theoretical_result.py`; `test_theoretical_cli.py` |
| H | Authority | TE observa/analiza/recomienda; no autoriza; `accepted_by` resoluble; `applied:false`; `status` derivado. | Igual. | Ninguno funcional. La policy debe declararlo sin ambigüedad tras el delta. | `OPTIONAL` (documental) | D-6. | Preservar `recommendation ≠ authorization`. | `test_theoretical_adversarial.py` (authority) |
| I | Lifecycle | Capacidad invocable; no es gate, fase ni estado; el Change la usa si la necesita. | Igual. | Ninguno; añadir un gate sería una decisión de gobernanza que esta misión no tiene. | `OUT_OF_SCOPE_PERMANENT` (como gate) / `OPTIONAL` (invocación) | D-6: declararlo en la policy. | Un gate obligatorio exigiría autoridad y convertiría un análisis semántico en condición de cierre. | Revisión de la policy |
| J | Persistence | Sin store: el resultado es efímero; el registro durable lo escribe el Change (Plan o Working). | Igual; ownership explícito. | La policy lo dice, pero no formaliza la obligación del consumidor cuando cita el resultado. | `OWNED_BY_OTHER_COMPONENT` | D-6: regla de persistencia por el consumidor. | `INV-11` (`docs/INVARIANTS.md:INV-11 — Governance Record Persistence`) prohíbe que un registro desaparezca sin traza; TE no debe volverse un store para cumplirlo. | Revisión de la policy + `test_theoretical_isolation.py` |
| K | Context recovery | Re-ejecución desde los mismos inputs; sin resume. | Igual, con skeleton recomputable y determinista. | El nonce no determinista (C) impide que el skeleton sea reproducible byte a byte. | `REQUIRED` (por C) | D-4 + D-6. | La recuperación es por artefacto (resultado + inputs), nunca por memoria conversacional. | `test_theoretical_identity.py` |
| L | Discovery / audit | No soportado: la unidad es un Plan commiteado. | Fuera de TE. | Ninguno. | `OWNED_BY_OTHER_COMPONENT` | D-6: declarar la frontera. | Un problema sin propuesta no tiene propuesta que atravesar; el análisis pre-plan es del Change Lifecycle (`docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`) y de `docs/working/audits/`. Extender TE destruiría la separación teórico/factual. | Revisión de la policy |
| M | Execution / post-execution | TE no observa el resultado de una ejecución; comparar predicción con realidad es verificación. | Fuera de TE. | Ninguno. | `OUT_OF_SCOPE_PERMANENT` | D-6. | Ingerir evidencia factual convertiría a TE en verificador y rompería `theoretical ≠ factual`; la verificación tiene dueño (Change Lifecycle, obligaciones). | `test_theoretical_isolation.py`; policy |
| N | Orchestrator | Sin integración: el host no importa TE y TE no importa el host; TE solo es invocable por CLI. | Igual; frontera explícita. | Ninguno funcional. La frontera debe quedar declarada como contrato. | `OUT_OF_SCOPE_PERMANENT` (embebido) / `OPTIONAL` (invocación CLI) | D-6. | Un segundo orquestador o una dependencia host↔TE duplicaría responsabilidades y crearía autoridad implícita. | `test_theoretical_isolation.py` (dirección de importación) |
| O | No-progress / stop | Fingerprint `(ítems, findings, status)`; techo de revisión; sin bucle. | Fingerprint recomputable y verificado por `--validate`. | `no_progress.fingerprint` **no se valida** y no incluye los checks; `previous_te_id` y `input.previous_te_id` no se cruzan. | `REQUIRED` | D-2/D-3: incluir checks, verificar fingerprint y coherencia. | Un no-progress declarado por el productor y no verificado es una afirmación, no una guarda. | `test_theoretical_result.py`; `test_theoretical_adversarial.py` |
| P | Auditability | El resultado registra identidad, cobertura, claims, findings, límites; los checks solo como findings cuando fallan. | Todo el registro determinista reconstruible, incluidos los checks que pasan. | Los checks `VALID`/`N/A` no quedan registrados; un tercero no puede reconstruir qué se verificó. | `REQUIRED` | D-2. | Sin registro no hay auditoría: solo hay una narración del productor. | `test_theoretical_result.py` (checks obligatorios); dogfood |
| Q | CLI / API | Cuatro comandos; sin escritura; exit codes fijados. | Igual, más el fingerprint computado en el reporte de `--validate`. | El productor no tiene forma mecánica de obtener el fingerprint ni de saber que el suyo discrepa. | `REQUIRED` (menor) | D-3: `computed_fingerprint` en el reporte. | Es el único dato que el productor necesita para declarar no-progress sin adivinar. | `test_theoretical_cli.py` |

---

## 5. Registro de exclusiones (con razón verificable)

| Área | Clase | Razón verificable |
|---|---|---|
| Ejecución real del Plan | `OUT_OF_SCOPE_PERMANENT` | `runtime/theoretical/__main__.py` no abre shell ni escribe; la policy lo prohíbe (`13. Boundaries`). Si TE ejecutara, dejaría de ser teórico. |
| Post-ejecución como insumo de TE | `OUT_OF_SCOPE_PERMANENT` | Consumir resultados reales como evidencia es verificación; `theoretical ≠ factual` (Plan 175 §1). La verificación tiene dueño: `docs/rfc/75-change-lifecycle.md:Mecanismo 6 — Validation Anchors`. |
| Autorización / governance / promoción / release | `OUT_OF_SCOPE_PERMANENT` | Constitutivo: `recommendation ≠ authorization` (`.agents/policies/theoretical-execution.md:9. Authority`). |
| Persistencia propia / store / `.project` | `OWNED_BY_OTHER_COMPONENT` | El registro durable pertenece al Change que cita el resultado (Plan o Working); TE no puede ser store sin duplicar el lifecycle (Plan 175 §1). |
| Lifecycle propio / gates nuevos | `OUT_OF_SCOPE_PERMANENT` | Sería una decisión de gobernanza con autoridad propia; esta misión no la tiene y el Change Lifecycle ya existe (`docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle`). |
| Orquestador embebido / segundo orchestrator | `OUT_OF_SCOPE_PERMANENT` | El host DEV ya existe (`runtime/orchestrator/`); TE solo se invoca por CLI. |
| Discovery / audit como entrada de TE | `OWNED_BY_OTHER_COMPONENT` | Un problema sin propuesta no tiene propuesta que atravesar; el análisis pre-plan vive en el Change Lifecycle y en `docs/working/audits/`. |
| Simulación de operaciones por pasos | `OUT_OF_SCOPE_PERMANENT` | Exigiría un intérprete de efectos y un modelo mutable: un segundo engine de ejecución dentro de TE. Se cubre con `dimensions.adversarial.probed`. |
| `ResultContentIdentity` | `OUT_OF_SCOPE_PERMANENT` | Los findings dependen del productor; una identidad de contenido afirmaría una reproducibilidad que no existe (Plan 175 §8). |
| `scenarios[]` | `OPTIONAL` | Cubierto por `dimensions.adversarial.probed`; añadirlo duplicaría el registro sin agregar verificabilidad. |
| Adaptador RFC / evaluación de RFCs | `DEFERRED` | La propuesta de cambio DEV es el Plan; evaluar RFCs exigiría definir un modelo de propuesta para ellos. No hay evidencia de necesidad y no es TE DEV. |
| Chequeo mecánico de admisión de efectos (SAE) | `OWNED_BY_OTHER_COMPONENT` | La admisión previa a delegar vive en `runtime/orchestrator/authority.py` y `tools/check_session_artifacts.py`; TE solo señala el vocabulario inválido (CH-9). |
| Provider / modelo / red / credenciales | `OUT_OF_SCOPE_PERMANENT` | Prohibido por diseño y verificado por la suite de aislamiento. |

---

## 6. Delta REQUIRED (lo que esta misión implementa)

| Id | Cambio | Evidencia del defecto | Verificación |
|---|---|---|---|
| D-1 | CH-3 resuelve citas y estado de artefactos contra el **commit base**; CH-7 recomputa el delta de identidad con blobs del **commit base** (nuevo modo de `tools/scoped_content_identity.py`). | `runtime/theoretical/checks.py` (`_ch3` → `verify_citation(root)`, `_artifact_status(root)`; `_ch7` → `compute(root)`) | Tests: una edición no commiteada o staged de un documento citado no cambia el resultado; el delta del ancla se recomputa desde la base. |
| D-2 | `TE_RESULT` v2 registra `checks[]` (todos los checks, incluidos `VALID`/`N/A`); `--validate` recomputa los checks en la base y exige igualdad exacta, presencia del finding de cada check no válido y de su obligación. | `runtime/theoretical/result.py:validate_result` no recomputa checks | Tests de finding eliminado/alterado, obligación ausente, check faltante, check extra. |
| D-3 | `no_progress.fingerprint` se verifica contra el fingerprint computado (que ahora incluye los checks) y se cruza con `previous_te_id`/`input.previous_te_id`; `--validate` publica `computed_fingerprint`. | `runtime/theoretical/result.py:_PROGRESS_KEYS`/`validate_result` | Tests de fingerprint mentido, previous sin fingerprint, previous_te_id incoherente. |
| D-4 | Nonce de `RunIdentity` derivado de contenido (inputs + created_at + producer + plan), no de `id()`. | `runtime/theoretical/identity.py:run_identity` | Test de dos corridas con el mismo timestamp y los mismos inputs → mismo `te_id`. |
| D-5 | CH-9 `declaration integrity`: entregable declarado sin path resoluble (`GAP` + obligación), path que escapa del repositorio (`ANOMALY`), clase de efecto fuera del vocabulario cerrado (`ANOMALY`). | `runtime/theoretical/proposal.py:_deliverables`/`_paths_from_text` descartan en silencio | Tests positivo/negativo por señal. |
| D-6 | Policy, `runtime/README.md`, glosario y suites alineados con lo que existe; se corrige la fila del Plan 175 en `docs/plans/INDEX.md` (H-11) por referencia, sin tocar el Plan cerrado. | H-11; policy desactualizada tras el delta | Checkers de gobernanza; revisión de la policy. |
| D-7 | `TE RESULT` schema 2: `schema_version`, `tool_version` y check-set suben de versión; un resultado v1 es `INCOMPARABLE` para `--stale`. | Contrato v1 sin registro de checks | Tests de `--stale` sobre un resultado v1. |

`FACT` — el delta no agrega persistencia, lifecycle, gate, store, red, modelo ni
autoridad. No modifica `protocol/`, `dist/`, `VERSION`, `ExecutionHost`,
`runtime/orchestrator/derivation.py` ni la batería canónica.

---

## 7. Revisión adversarial (se completa con los resultados de la ejecución)

Ataques exigidos y resultado: ver `docs/plans/176-theoretical-execution-dev-complete.md`
(§Revisión adversarial). Este registro conserva el resultado agregado:

```text
SCOPE_ATTACK              = PASS (frontera declarada; no se absorbe discovery/audit/execution)
BOUNDARY_ATTACK           = PASS (no host, no payload, no store, no segundo lifecycle)
STATE_ATTACK              = PASS (una pasada; sin estado parcial; recuperación por re-ejecución)
AUTHORITY_ATTACK          = PASS (recommendation ≠ authorization; escape y residual verificados)
EVIDENCE_ATTACK           = PASS (ningún estado factual; PREDICTION no verificable)
IDENTITY_ATTACK           = PASS (checks función de InputIdentity; nonce determinista)
TEMPORAL_ATTACK           = PASS (stale por HEAD; checks independientes de working tree e índice)
DEPENDENCY_ATTACK         = PASS (dirección de importación; stdlib + runtime + tools)
NEGATIVE_PATH_ATTACK      = PASS (inputs malformados, campos desconocidos, estados inválidos)
HISTORICAL_INTEGRITY_ATTACK = PASS (no se reescribe el Plan 175; corrección del INDEX por referencia)
```

---

## 8. Límites declarados

`LIMIT` — la atestación semántica del productor no es verificable por el engine: puede
declarar dimensiones que no ejecutó. La mitigación es estructural (`producer` +
`probed` + `INV-03`), no una garantía.

`LIMIT` — los findings semánticos no son reproducibles: dos productores pueden
producir resultados distintos sobre el mismo `InputIdentity`; `--compare` reporta
diferencias observadas, nunca `resolved`/`reopened`.

`LIMIT` — la staleness es relativa a HEAD: el resultado sigue siendo válido para su
base, pero deja de ser aplicable cuando HEAD avanza, aunque el cambio sea ajeno.

`LIMIT` — TE no demuestra que la propuesta sea correcta, segura, completa ni
ejecutable: demuestra que el registro teórico está bien formado y que sus
condiciones declaradas son coherentes.

`LIMIT` — el registro de checks es recomputable solo mientras el `check_set` y el
`tool_version` coincidan; un cambio de semántica sin bump de versión produce
resultados no comparables (mitigado por el check-set versionado).
