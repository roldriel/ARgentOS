# Etapa A — Retrospectiva de capacidades y garantías (Capability & Guarantee Matrix)

**Naturaleza documental:** Working / analysis — **no normativo**; puede ser provenance, nunca autoridad.
**Fecha:** 2026-10-12 · **Origen:** `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` (Plan 161, Etapa A)
**Estado:** active · **Autoridad:** ninguna (Working); la autoridad del trabajo es el Plan 161 aprobado.

**Unidad de análisis:** *capacidad + garantía + evidencia* — no el archivo ni la feature.
**Pregunta central:** ¿qué puede afirmar ARgentOS que hace, con qué mecanismo, y con qué evidencia funciona bajo las condiciones en las que se pretende utilizarlo?

## 1. Cómo leer esta matriz

### 1.1 Regla de evidencia

Una afirmación **positiva** requiere **evidencia ejecutable**: un test, un checker, código efectivamente ejecutado, un invariante verificado, un gate de lifecycle, un anchor/checkpoint registrado, o evidencia operacional equivalente. **La documentación explica una afirmación; no la sustituye.** Un nombre de archivo, de módulo o de función no es evidencia de comportamiento.

### 1.2 Vocabulario cerrado de niveles de madurez (ocho valores, uno por capacidad)

| Nivel | Qué significa en esta matriz |
|---|---|
| `implementado` | el mecanismo existe y es estructuralmente válido, pero **no** hay cobertura automatizada que lo ejercite ni consumo efectivo |
| `testeado` | existe cobertura automatizada que ejercita el mecanismo de forma aislada |
| `dogfoodeado` | el mecanismo fue **ejercitado en este repositorio** como parte de su propio desarrollo, con evidencia verificable (suites ancladas, planes, checkers sobre el corpus real) |
| `demostrado bajo condiciones reales` | además, la garantía se sostuvo bajo las condiciones de uso pretendidas **que el repositorio no controla o no reprodujo**: ejecución desatendida de duración no trivial, un proveedor real, un proyecto adoptante, o CI cubriendo la totalidad de la garantía |
| `parcialmente demostrado` | sólo un subconjunto de las condiciones pretendidas fue ejercitado |
| `dependiente de una condición externa` | la garantía depende de algo fuera del control de ARgentOS (un proveedor, un invoker inyectado, la infraestructura de CI) |
| `no demostrado` | existe (total o parcialmente) sin evidencia de que funcione; **equivalente a `NO PROBADO`** |
| `limitado por un boundary conocido` | funciona dentro de un límite declarado, y el límite es la garantía efectiva |

**Ninguna capacidad se clasifica por encima de su evidencia.** En particular, no se eleva un nivel porque la arquitectura lo permitiría, porque exista código parcial, porque exista documentación, porque exista una intención en el ROADMAP o porque exista un test aislado que no demuestre el contrato completo.

### 1.3 Estructura y convención de celdas

28 capacidades × 9 dimensiones = **252 celdas**. Cada capacidad tiene un bloque `C-NN` con: el **nivel de madurez asignado** (exactamente uno) y una tabla de **9 filas**, una por dimensión, con contenido no vacío. Una dimensión sin información se declara `GAP`/`N/A` **con su motivo**; nunca se omite.

Las nueve dimensiones son, en orden fijo: **1** qué afirma hacer · **2** qué mecanismo lo implementa · **3** qué tests existen · **4** qué dogfooding existe · **5** qué condiciones se probaron · **6** qué condiciones **no** se probaron · **7** qué garantía puede considerarse demostrada · **8** qué garantía permanece sin demostrar · **9** qué limitaciones existen.

### 1.4 Límites del levantamiento (declarados)

- **Evidencia externa no utilizada.** Existen sesiones de adopción reales en proyectos externos a este repositorio (`sessions/` contiene enlaces a `.project` de `BeaconRBX` y `HikariClub`). **No se usaron como evidencia**: están fuera del repositorio y fuera del alcance de inspección autorizado. En consecuencia, ninguna capacidad cuyas condiciones pretendidas sean un proyecto adoptante puede acreditar aquí condiciones reales.
- **Sin proveedor, modelo, red ni credenciales.** El repositorio los declara ausentes; toda garantía que requiera una invocación real de modelo queda fuera de lo demostrable (y así se registra en cada caso).
- **Registro ejecutable del levantamiento:** `python -m pytest tests/ -q` = **1316 passed**; `python -m pytest protocol/.agents/harness/tests/ -q` = **185 passed**; `check_protocol_invariants` = 216 archivos / 10457 referencias; gates C-1/C-2/C-3 ejecutados sobre 161 planes.
- **Citas.** Todas las citas de este documento son resolubles; las 26 citas rotas del corpus son **baseline histórico** (documentos históricos → secciones eliminadas del `ROADMAP.md` por los Planes 157/158) y no provienen de este documento.

## 2. Resumen — nivel de madurez por capacidad

| # | Capacidad | Dominio | Nivel de madurez |
|---|---|---|---|
| `C-01` | Change Lifecycle | DEV | `dogfoodeado` |
| `C-02` | Authority | DEV + PROTOCOL | `parcialmente demostrado` |
| `C-03` | Scope enforcement | DEV | `dogfoodeado` |
| `C-04` | Validation / Closure | DEV | `dogfoodeado` |
| `C-05` | C1/C2/C3 | DEV | `dogfoodeado` |
| `C-06` | SAE | DEV | `dogfoodeado` |
| `C-07` | Autonomous Orchestrator | DEV | `dogfoodeado` |
| `C-08` | Agent Worker | DEV | `dependiente de una condición externa` |
| `C-09` | WorkerResult | DEV | `dogfoodeado` |
| `C-10` | Delegation | DEV | `dogfoodeado` |
| `C-11` | Context engineering | BOTH | `testeado` |
| `C-12` | Context identity | BOTH | `testeado` |
| `C-13` | Materialization | BOTH | `testeado` |
| `C-14` | Prompt Cache | BOTH | `dependiente de una condición externa` |
| `C-15` | Placement | DEV | `limitado por un boundary conocido` |
| `C-16` | Discovery | PROTOCOL | `no demostrado` |
| `C-17` | Discovery KB | PROTOCOL | `no demostrado` |
| `C-18` | Protocol gates | PROTOCOL | `testeado` |
| `C-19` | enforced mode / hooks | PROTOCOL | `testeado` |
| `C-20` | EARS | PROTOCOL | `dogfoodeado` |
| `C-21` | Skills | PROTOCOL | `implementado` |
| `C-22` | Deliberation | PROTOCOL | `dogfoodeado` |
| `C-23` | Change Governance | PROTOCOL | `testeado` |
| `C-24` | Metrics / health | BOTH | `parcialmente demostrado` |
| `C-25` | Feature flags | PROTOCOL | `parcialmente demostrado` |
| `C-26` | recovery | DEV | `parcialmente demostrado` |
| `C-27` | CI / validation | DEV + PROTOCOL | `parcialmente demostrado` |
| `C-28` | distribución y sincronización de `dist` | PROTOCOL | `dependiente de una condición externa` |

**Distribución:** `dogfoodeado` 11 · `testeado` 6 · `parcialmente demostrado` 4 · `dependiente de una condición externa` 3 · `no demostrado` 2 · `limitado por un boundary conocido` 1 · `implementado` 1 · `demostrado bajo condiciones reales` **0**.

## 3. Matriz

### C-01 — Change Lifecycle (DEV)

**Nivel de madurez: `dogfoodeado`** — el ciclo completo se ejecutó sobre este repositorio más de ciento sesenta veces con gates y checkers, pero su **automatización** (Incremento 4) y sus **métricas operacionales** no existen, y los gates de lifecycle no corren en CI.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Un pipeline único `authorize → execute → verify → close → commit → promote` con estados derivados (`Executed ≠ Committed ≠ Closed ≠ Released`) y evidencia anclada por Change. |
| 2 | Qué mecanismo lo implementa | `docs/rfc/75-change-lifecycle.md`, `.agents/workflows/change-lifecycle.md`, `.agents/policies/authority.md`, `.agents/policies/validation-closure.md`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md` §7; herramientas: `tools/check_plan_structure.py`, `tools/check_plan_citations.py`, `tools/check_version_state.py`, `tools/check_lifecycle_anchor.py`, `tools/check_lifecycle_checkpoint.py`, `tools/check_lifecycle_lineage.py`, `tools/scoped_content_identity.py`; escritura del registro de gobernanza por `runtime/orchestrator/governance.py`. |
| 3 | Qué tests existen | `tests/test_check_plan_structure.py` (21), `tests/test_check_plan_citations.py` (37), `tests/test_check_version_state.py` (8), `tests/test_check_lifecycle_anchor.py` (23), `tests/test_check_lifecycle_checkpoint.py` (32), `tests/test_check_lifecycle_lineage.py` (36), `tests/test_determine_execution_state.py` (69), `tests/test_scoped_content_identity.py` (17), `tests/test_repo_containment.py` (dogfood, 1). |
| 4 | Qué dogfooding existe | El propio corpus: C-1 inspecciona **161** planes (VALID=66, N/A=1, GAP=0, ANOMALY=0); C-2 VALID=65 con el `GAP` histórico del Plan 116; C-3 VALID=34. Los Planes 149–161 se ejecutaron y cerraron a través de este pipeline. |
| 5 | Qué condiciones se probaron | Corpus real completo con historia Git completa; estados derivados sobre contenido staged real; identidad de contenido scoped reproducible (`scoped-v1`); anti-auto-referencia del cierre. |
| 6 | Qué condiciones **no** se probaron | Ejecución de los gates de lifecycle **en CI** (no están en `.github/workflows/check-protocol.yml`); automatización mecánica del Incremento 4; medición operacional de las métricas del ciclo; cierres con dependencias ambientales adversas. |
| 7 | Qué garantía puede considerarse demostrada | Que toda validación registrada en este corpus tiene anchor y que el cierre registra checkpoint con correspondencia verificada: C-1/C-2 lo comprueban sobre los 161 planes, con `ANOMALY=0`. |
| 8 | Qué garantía permanece sin demostrar | Que el ciclo **no pueda** cerrarse sin anchor/checkpoint. La derivación de `Closed` es una determinación declarada y verificada *a posteriori*; ningún gate la **bloquea** en el momento del commit, y `GAP` es advisory y nunca cambia el exit code. |
| 9 | Qué limitaciones existen | Los gates son locales y factuales (evidencia, no autoridad — ADR-16); 94 planes legacy quedan `EXCLUDED` sin backfill (RFC-75 Mecanismo 15); el corpus sólo cubre condiciones de este repositorio; el Enforcement del Incremento 4 está diferido por la propia RFC-75. |

### C-02 — Authority (DEV + PROTOCOL)

**Nivel de madurez: `parcialmente demostrado`** — la derivación de autoridad está implementada y probada dentro del host, pero la contención de autoridad frente a código que el host no controla no está demostrada y está declarada como no garantizada.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Ninguna acción se ejecuta sin una base de autoridad existente; la autoridad no se infiere por presencia documental, proximidad semántica ni clasificación de impacto; hay reservas humanas explícitas. |
| 2 | Qué mecanismo lo implementa | `.agents/policies/authority.md` (clases RFC-56, conflicto, document discovery), `.agents/policies/validation-closure.md` §5.1/§5.2 (la obligación no es autorización), `docs/adr/16-change-lifecycle-authority.md`, `runtime/orchestrator/authority.py`, ADR-19 `AE-9` (`docs/adr/19-autonomy-envelope-authority.md:Invariantes`). |
| 3 | Qué tests existen | `tests/test_autonomous_scope.py` (58), `tests/test_sae_scope_enforcement.py` (38), `tests/test_autonomy_effects.py` (36) ejercitan veredictos de autoridad (`CONTINUE`/`STOP`/`REQUIRES_AUTHORITY`/`FORBIDDEN`) y la alcanzabilidad de las condiciones de parada; `tests/test_autonomy_effects_dogfood.py` (13) fija policy ↔ enforcement. |
| 4 | Qué dogfooding existe | `tests/test_sae_scope_enforcement_dogfood.py` (13) y `tests/test_autonomous_scope_dogfood.py` (7) sobre el repositorio real, incluida la historia del incidente `<PLAN-136>:F-3`. |
| 5 | Qué condiciones se probaron | Vocabulario cerrado de acciones; prohibición de ampliar `Scope`; conversión de un `STOP` en `CONTINUE`; efectos declarados/no autorizados; la obligación de impacto no autoriza escritura. |
| 6 | Qué condiciones **no** se probaron | Contención de autoridad frente a un `AgentInvoker` inyectado que ejecute su propio código (el host **no puede** interponerse: declarado en `.agents/policies/supervised-autonomous-execution.md` §12); autoridad bajo aislamiento/sandbox real (no existe). |
| 7 | Qué garantía puede considerarse demostrada | Que dentro del bucle del host ninguna acción se delega sin base de autoridad registrada, y que las condiciones de parada por autoridad son alcanzables y verificadas por test. |
| 8 | Qué garantía permanece sin demostrar | Que la autoridad esté contenida **fuera** del host (en el worker o en el invoker): la política declara expresamente que la prevención sólo cubre los efectos que el host controla. |
| 9 | Qué limitaciones existen | DEV-only; sin provider/modelo/red/credenciales; el invoker inyectado **no** es garantía de aislamiento (ADR-19 `AE-7`); los checkers son evidencia factual, nunca autoridad. |

### C-03 — Scope enforcement (DEV)

**Nivel de madurez: `dogfoodeado`** — con evidencia fuerte de prevención y detección sobre el repositorio real, pero sin un invoker real (la condición pretendida de producción) ni enforcement por defecto (`--sae` es opt-in).

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Ninguna escritura fuera del `Scope` declarado por el Plan: prevención **antes** de delegar donde el host controla el efecto, y detección **después** donde no lo controla. |
| 2 | Qué mecanismo lo implementa | `runtime/orchestrator/host.py` (`_apply_autonomy_gate` invocado en `iterate()` antes de `_execute_delegation`; verificación de scope por snapshots de contenido), `runtime/orchestrator/derivation.py` (`forbidden_scope_action`), `.agents/policies/supervised-autonomous-execution.md` §1.1–§1.3. |
| 3 | Qué tests existen | `tests/test_sae_scope_enforcement.py` (38), `tests/test_autonomy_effects.py` (36, incluida la contra-prueba «sin el gate el invoker **sí** escribe»), `tests/test_agent_worker.py` (41), `tests/test_autonomous_scope.py` (58). |
| 4 | Qué dogfooding existe | `tests/test_sae_scope_enforcement_dogfood.py` (13) y `tests/test_autonomous_scope_dogfood.py` (7): el punto de enforcement, la historia intacta del plan del incidente y `ROADMAP.md`, y el rechazo end-to-end antes del efecto. |
| 5 | Qué condiciones se probaron | Escritura dentro y fuera de `Scope`; path declarado y no declarado; efecto sin `write-target` (ortogonalidad `Effect ⊥ Scope`); artefacto byte-idéntico cuando el gate rechaza; verificación independiente del relato del worker. |
| 6 | Qué condiciones **no** se probaron | Interposición **dentro** de la invocación (declarada imposible); un worker real con proveedor; el modo por defecto (sin `--sae`, sólo corre la detección posterior). |
| 7 | Qué garantía puede considerarse demostrada | Prevención efectiva donde el host controla el efecto (probada por contra-prueba) y detección de la escritura no declarada desde el `WorkerResult` persistido, registrada como finding. |
| 8 | Qué garantía permanece sin demostrar | Que una escritura no autorizada **no pueda** ocurrir: la política declara que la garantía es prevención *o* detección, nunca prevención en todos los casos. |
| 9 | Qué limitaciones existen | DEV-only; `--sae` opt-in (no cambia el comportamiento por defecto); un path ya modificado antes de la delegación se detecta por snapshot, no por diff sucio; sin aislamiento. |

### C-04 — Validation / Closure (DEV)

**Nivel de madurez: `dogfoodeado`** — la disciplina de anchor y checkpoint se sostiene sobre 161 planes reales, con la limitación de que su enforcement es local y advisory.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Toda validación registrada tiene un **Validation Anchor** (alcance, command-set, insumos efectivos, factores ambientales, identidad de contenido scoped, validez) y todo cierre tiene un **checkpoint** que certifica el estado validado y su consistencia. |
| 2 | Qué mecanismo lo implementa | `.agents/policies/validation-closure.md` (VC-1, CL-2, GC-1, §5.1/§5.2), `docs/CONVENTIONS.md` (secciones de anchors y checkpoint), `tools/scoped_content_identity.py`, `tools/check_lifecycle_anchor.py`, `tools/check_lifecycle_checkpoint.py`. |
| 3 | Qué tests existen | `tests/test_check_lifecycle_anchor.py` (23), `tests/test_check_lifecycle_checkpoint.py` (32), `tests/test_scoped_content_identity.py` (17), `tests/test_determine_execution_state.py` (69). |
| 4 | Qué dogfooding existe | Los anchors y checkpoints de los Planes 96–161, incluidos A1/A2 de los Planes 151, 159, 160 y 161; C-1 `VALID=66`, C-2 `VALID=65` con `ANOMALY=0`. |
| 5 | Qué condiciones se probaron | Revalidación A2 sobre estado nuevo sin mutar A1; identidad delta vs. state identity; divergencia legítima `validated tree ≠ commit tree`; convención anti-auto-referencia; estado de cierre por **correspondencia**, no por recencia. |
| 6 | Qué condiciones **no** se probaron | Ejecución de estos gates en CI (no están cableados); enforcement en el momento del commit; el `GAP` histórico del Plan 116 permanece sin resolver por decisión. |
| 7 | Qué garantía puede considerarse demostrada | Que en este corpus todo cierre tiene anchor con identidad de contenido scoped y checkpoint con correspondencia verificada, y que los anchors previos nunca se mutan al revalidar. |
| 8 | Qué garantía permanece sin demostrar | Que un cierre sin anchor/checkpoint sea **imposible**: la ausencia se reporta como `GAP` advisory (nunca invalida) y el gate no corre en CI. |
| 9 | Qué limitaciones existen | `GAP` no cambia el exit code; los anclajes dependen de factores ambientales declarados por el autor; el snapshot de `docs/VERSIONING.md` §9 — se reconcilia sólo en promoción; 94 planes legacy fuera del régimen. |

### C-05 — C1/C2/C3 (DEV)

**Nivel de madurez: `dogfoodeado`** — tres checkers deterministas, con 91 pruebas y dogfoods anclados sobre el corpus real; su debilidad es que **no corren en CI**.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Tres gates factuales: C-1 verifica los anchors, C-2 la relación cierre↔Git y la correspondencia con el anchor aplicable, C-3 el lineage de findings/correcciones. Salida: `VALID`/`N/A`/`EXCLUDED`/`BOUNDARY`/`GAP`/`ANOMALY`. |
| 2 | Qué mecanismo lo implementa | `tools/check_lifecycle_anchor.py`, `tools/check_lifecycle_checkpoint.py`, `tools/check_lifecycle_lineage.py`; contrato en `.agents/policies/lifecycle-checkers.md` y `docs/VERSIONING.md` §4.1. |
| 3 | Qué tests existen | 23 + 32 + 36 = **91** funciones de test, con escenarios deterministas sobre repositorios temporales, `tmp_path` y git temporales, más validación adversarial. |
| 4 | Qué dogfooding existe | Tres suites ancladas sobre el corpus real (`test_real_repo_expected_classifications` ×2 y `test_t27_real_repo_dogfooding`), que fijan clasificaciones por plan y exigen `ANOMALY=0` y `GAP=0` en C-3. |
| 5 | Qué condiciones se probaron | Exit codes (`GAP`→0, `ANOMALY`→1); legacy `EXCLUDED`; `N/A` de un miembro del régimen sin validación registrada; correspondencia A1/A2; identidades de árbol reales. |
| 6 | Qué condiciones **no** se probaron | Ejecución en CI (los workflows no los invocan); corpus de un proyecto adoptante; comportamiento con historia Git incompleta en CI (documentado como degradación silenciosa que obligó a `fetch-depth: 0`). |
| 7 | Qué garantía puede considerarse demostrada | Determinismo y correctitud de la clasificación sobre el corpus real y sobre escenarios adversariales, con `ANOMALY=0` en los tres gates. |
| 8 | Qué garantía permanece sin demostrar | Que una anomalía real de lifecycle **detenga** algo: son gates locales, advisory, que nadie ejecuta automáticamente en el pipeline de este repositorio. |
| 9 | Qué limitaciones existen | Evidencia factual ≠ autoridad (ADR-16); no forman parte del bloque canónico §4.1 (son gates adicionales); el `GAP` histórico del Plan 116 persiste; un plan sin contenedores de plantilla queda `EXCLUDED` por legacy. |

### C-06 — SAE (DEV)

**Nivel de madurez: `dogfoodeado`** — frontera de autonomía implementada, con 145 pruebas de frontera y cuatro suites ancladas; no alcanza condiciones reales porque nunca operó con un worker real ni con `--sae` como default.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Define qué acciones puede ejecutar el host sin volver a preguntar: `autonomy ⊆ authorized scope ∩ granted authority`, con verificación antes del efecto, vocabulario cerrado de acciones, condiciones de parada y frontera humana. |
| 2 | Qué mecanismo lo implementa | `.agents/policies/supervised-autonomous-execution.md` (§1–§12), `runtime/orchestrator/autonomy.py` (`AutonomyEnvelope`, `AutonomyCandidate`, `admit_declared_effects`, `evaluate_autonomy`, `evaluate_candidate`, `summarize_autonomy`), gate opt-in `--sae` en `runtime/orchestrator/host.py`; `docs/adr/19-autonomy-envelope-authority.md`. |
| 3 | Qué tests existen | `tests/test_autonomous_scope.py` (58), `tests/test_sae_scope_enforcement.py` (38), `tests/test_autonomy_effects.py` (36), `tests/test_autonomous_scope_dogfood.py` (7), `tests/test_sae_scope_enforcement_dogfood.py` (13), `tests/test_autonomy_effects_dogfood.py` (13). |
| 4 | Qué dogfooding existe | Las cuatro suites ancladas anteriores: policy ↔ enforcement, vocabulario único compartido con `tools/check_session_artifacts.py`, el Plan 159 leído con su propio parser, y la frontera fuera del envelope. |
| 5 | Qué condiciones se probaron | Admisión de efectos declarados (all-or-nothing); efecto desconocido ⇒ `REQUIRES_HUMAN`; efecto sin path admisible; techo de recurso acumulado desde el journal y superviviente a reinicio; techo ≠ autorización; alcanzabilidad de todas las condiciones de parada. |
| 6 | Qué condiciones **no** se probaron | SAE con un worker/proveedor real; SAE como comportamiento por defecto (`OPD-3` lo dejó opt-in por directiva); duración no trivial en operación desatendida. |
| 7 | Qué garantía puede considerarse demostrada | Que con el gate activo una acción no admitida no delega, no invoca y deja el artefacto byte-idéntico; y que el agotamiento de recurso produce `STOP` sin veredicto de autoridad. |
| 8 | Qué garantía permanece sin demostrar | Que la autonomía sea segura bajo ejecución real de efectos fuera del proyecto: la frontera se ejerció sobre invocadores inyectados, no sobre un actor con proveedor, red o credenciales. |
| 9 | Qué limitaciones existen | `--sae` opt-in; el host no puede interponerse dentro de la invocación; no hay provider/modelo/red/credenciales; la resolución del estado de un finding sigue siendo autoridad humana (`CL-8`, ADR-16 `AU-3`). |

### C-07 — Autonomous Orchestrator (DEV)

**Nivel de madurez: `dogfoodeado`** — corrida real documentada y bucle probado sobre git real, con la limitación estructural de no tener proveedor.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Conduce un Change ya autorizado: observa, deriva la próxima acción, autoriza, delega, ejecuta, ingiere, verifica y decide continuar o parar — sin almacenar estado propio. |
| 2 | Qué mecanismo lo implementa | `runtime/orchestrator/{__main__,host,observation,derivation,store,contracts,authority,governance}.py`, `runtime/README.md` §DEV Autonomous Orchestrator, `.agents/policies/autonomous-orchestration.md`; CLI `python -m runtime.orchestrator --plan N`. |
| 3 | Qué tests existen | `tests/test_autonomous_orchestrator.py` (31), `tests/test_determine_execution_state.py` (69), `tests/test_agent_worker.py` (41), más las suites SAE; runner determinista con basetemp externo (`tests/pytest_isolation.py`, 22). |
| 4 | Qué dogfooding existe | `docs/working/audits/DEV_AUTONOMOUS_ORCHESTRATOR_DOGFOOD_2026-09-14.md` (corrida real con journal, estados y señales de gate) y las suites ancladas de autonomía. |
| 5 | Qué condiciones se probaron | Reconstrucción del estado desde el repositorio y el journal (sin memoria); derivación determinista como función pura; delegación y verificación de scope fuera del worker; reanudación tras reinicio. |
| 6 | Qué condiciones **no** se probaron | Operación desatendida de duración no trivial; ejecución con proveedor real; concurrencia (inexistente por diseño); un objetivo multi-Change (fuera de alcance, `D-1`). |
| 7 | Qué garantía puede considerarse demostrada | Que el bucle es reconstruible y auditable: cada iteración deja evidencia suficiente para reconstruir qué se observó, derivó, autorizó, ejecutó, verificó y por qué se detuvo. |
| 8 | Qué garantía permanece sin demostrar | Que el host conduzca trabajo real de principio a fin sin intervención operacional humana; y que su frontera resista un actor con capacidad real de efectos. |
| 9 | Qué limitaciones existen | DEV-only, no viaja en `dist`; un Change por corrida; ejecución secuencial; sin provider/modelo; `--worker agent` sólo construye el default honesto (`NullAgentInvoker`). |

### C-08 — Agent Worker (DEV)

**Nivel de madurez: `dependiente de una condición externa`** — el worker está implementado y probado (41 pruebas) y su dogfood corrió, pero su valor real depende de un `AgentInvoker` que **este repositorio no provee**.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Ejecuta el trabajo semántico delegado y devuelve un `WorkerResult` honesto, distinguiendo *no disponible* / *incompleta* / *completada*, sin fabricar pasos, comandos ni transcripciones, y sin autoproclamar finalización. |
| 2 | Qué mecanismo lo implementa | `runtime/orchestrator/agent_worker.py` (`AgentWorker`, `AgentInvoker`, `NullAgentInvoker`, `agent_invoker_from_environment`, `classify_executed_effects`), `runtime/orchestrator/worker.py`; contrato de rol en `runtime/README.md` §DEV Agent Worker. |
| 3 | Qué tests existen | `tests/test_agent_worker.py` (41), más `tests/test_autonomy_effects.py` (36) y `tests/test_autonomous_orchestrator.py` (31) sobre persistencia y verificación de sus resultados. |
| 4 | Qué dogfooding existe | `docs/working/audits/DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md` (corrida real, con hallazgos `<PLAN-123>:F-01`/`F-02` sobre snapshots y `_committed()`). |
| 5 | Qué condiciones se probaron | Los tres resultados distinguibles con invocadores inyectados; `claims.self_reported_completion = false`; `recommended_next_action` advisory; verificación de scope independiente del relato del worker; clasificación de efectos ejecutados. |
| 6 | Qué condiciones **no** se probaron | Una invocación real de modelo: no hay provider, modelo, red ni credenciales (declarado en el propio módulo y en `runtime/README.md`); tampoco consumo de skills (deliberadamente ausente en el MVP). |
| 7 | Qué garantía puede considerarse demostrada | Que el worker no puede convertirse en autoridad: no aprueba, no cambia scope, no resuelve decisiones humanas, y su recomendación nunca es una autorización. |
| 8 | Qué garantía permanece sin demostrar | Que produzca trabajo útil real: sin invoker provisto por el entorno, el resultado honesto es «no disponible»; la utilidad depende de un componente externo. |
| 9 | Qué limitaciones existen | Sin provider/modelo/red; sin skills ni perfiles (ausencia deliberada); el bucle interno del worker es worker-local y no es una máquina de estados de ARgentOS; su transcripción es evidencia, nunca autoridad. |

### C-09 — WorkerResult (DEV)

**Nivel de madurez: `dogfoodeado`** — contrato persistido y consumido con evidencia sobre corridas y dogfoods reales.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Registra el resultado de una delegación como evidencia persistente, reconstruible y no auto-certificada, ingerible por el host para verificar, clasificar y decidir. |
| 2 | Qué mecanismo lo implementa | Contrato M4 en `runtime/orchestrator/contracts.py`, persistencia y lectura con `GAP` declarado en `runtime/orchestrator/store.py`, clasificación en `runtime/orchestrator/worker.py`, consumo en `runtime/orchestrator/host.py`. |
| 3 | Qué tests existen | `tests/test_agent_worker.py` (41), `tests/test_autonomous_orchestrator.py` (31), `tests/test_autonomy_effects.py` (36) y los escenarios de journal con líneas ilegibles de `tests/test_determine_execution_state.py`. |
| 4 | Qué dogfooding existe | `DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md` y `DEV_AUTONOMOUS_ORCHESTRATOR_DOGFOOD_2026-09-14.md`, donde los resultados y su ingesta quedan registrados en journal y reportes. |
| 5 | Qué condiciones se probaron | Persistencia y relectura; `GAP` declarado para líneas ilegibles del journal (nunca descarte silencioso); efectos ejecutados clasificados; verificación de scope contra los resultados. |
| 6 | Qué condiciones **no** se probaron | Resultados producidos por un worker con proveedor real; volumen y duración de una operación desatendida; coste/tokens (no hay telemetría económica). |
| 7 | Qué garantía puede considerarse demostrada | Que el resultado es reconstruible desde el artefacto persistido y que el host no confía en la auto-certificación del worker. |
| 8 | Qué garantía permanece sin demostrar | Que la evidencia de un worker real sea suficiente para reconstruir *qué hizo*: hoy depende del invoker y de que declare sus efectos. |
| 9 | Qué limitaciones existen | Contrato DEV-only, no distribuido; sin telemetría ni coste; `claims.self_reported_completion` siempre `false` por diseño; el journal es efímero (`.project/`). |

### C-10 — Delegation (DEV)

**Nivel de madurez: `dogfoodeado`** — delegación declarada por el Plan, leída y verificada por el host, con dogfood real; limitada a una delegación por vez y sin worker real.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | El Plan declara la unidad de trabajo delegable (`Task` + `Scope` + techo de recurso) y el host la materializa en una `Delegation` verificable, sin inventar trabajo cuando la sección falta. |
| 2 | Qué mecanismo lo implementa | `contracts.py` (`Delegation` con `task`/`input_artifacts` aditivos-optional; `RUN_IMPLEMENTATION_TASK` en el vocabulario cerrado), `runtime/orchestrator/observation.py` (`parse_agent_task`), `host.py` (derivación y verificación), `docs/plans/_TEMPLATE.md` §Delegación agentiva. |
| 3 | Qué tests existen | `tests/test_agent_worker.py` (41), `tests/test_autonomous_orchestrator.py` (31), `tests/test_autonomy_effects.py` (36). |
| 4 | Qué dogfooding existe | Los planes 159/160/161 declaran (o declaran la ausencia de) delegación, y el dogfood del Agent Worker y del Orchestrator ejerció el camino completo. |
| 5 | Qué condiciones se probaron | Sección ausente ⇒ ausencia declarada (no falla, no delega); techo de recurso leído; verificación de scope post-delegación por snapshot; persistencia compatible con delegaciones previas al Plan 123. |
| 6 | Qué condiciones **no** se probaron | Delegación paralela o multi-worker (ejecución secuencial por diseño); delegación a un actor real con efectos externos. |
| 7 | Qué garantía puede considerarse demostrada | Que la delegación se deriva de la declaración autorizada del Plan y que su efecto es verificable fuera del worker. |
| 8 | Qué garantía permanece sin demostrar | Que la instrucción declarada sea la que efectivamente se ejecutó: el host verifica efectos y scope, no la fidelidad semántica de la ejecución. |
| 9 | Qué limitaciones existen | Una delegación por iteración; sin concurrencia; sin skills/perfiles; el techo de recurso es guarda operativa, nunca autorización (`AE-6`). |

### C-11 — Context engineering (BOTH)

**Nivel de madurez: `testeado`** — presupuesto de contexto semántico medido y materialización verificada por pruebas, sin consumo real por un modelo.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Construye y acota el contexto que se materializa, con un presupuesto medido y unidades declaradas, y con presupuestos por subsistema (p. ej. discovery). |
| 2 | Qué mecanismo lo implementa | `runtime/toolcalls/context.py`, `runtime/toolcalls/budget.py`, `tools/measure_context_budget.py`, `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md`, `protocol/.agents/features.toml` (`discovery_context_budget`). |
| 3 | Qué tests existen | `tests/test_measure_context_budget.py` (6), `tests/test_toolcalls.py` (12), `tests/test_canonical_materialization.py` (41), `tests/test_canonical_materialization_v2.py` (42). |
| 4 | Qué dogfooding existe | `GAP` — no hay una suite anclada al repositorio para esta capacidad; la evidencia es de pruebas aisladas sobre entradas construidas. |
| 5 | Qué condiciones se probaron | Medición de presupuesto sobre entradas de prueba; determinismo de la medición; unidad declarada (tokens estimados). |
| 6 | Qué condiciones **no** se probaron | Correspondencia entre el presupuesto estimado y el consumo real de un modelo (no hay provider); comportamiento ante ventanas de contexto reales; presión de contexto en operación. |
| 7 | Qué garantía puede considerarse demostrada | Que existe una medición determinista del presupuesto semántico y que su unidad está declarada. |
| 8 | Qué garantía permanece sin demostrar | Que el presupuesto **contenga** efectivamente el contexto: sin provider no hay verificación de límite real; el propio audit de capacidades lo registró como «Context Budget **semántico** medido». |
| 9 | Qué limitaciones existen | Sin budget de costo ni de wall-clock; sin telemetría (RFC-74); el presupuesto se declara en caracteres/tokens estimados, no en consumo facturado. |

### C-12 — Context identity (BOTH)

**Nivel de madurez: `testeado`** — identidad semántica determinista con cobertura amplia; sin verificación contra un proveedor.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Identifica de forma determinista y reproducible el contenido semántico del contexto, separando identidad semántica, de materialización y de proveedor. |
| 2 | Qué mecanismo lo implementa | `runtime/toolcalls/identity.py` (`SemanticContextIdentity`), `runtime/toolcalls/canonical.py`, `docs/rfc/72-provider-prompt-cache-capability.md` (tres dominios no conflacionables). |
| 3 | Qué tests existen | `tests/test_canonical_materialization.py` (41), `tests/test_canonical_materialization_v2.py` (42), `tests/test_toolcalls.py` (12), `tests/test_scoped_content_identity.py` (17) para la identidad de contenido scoped del lifecycle. |
| 4 | Qué dogfooding existe | `tests/test_scoped_content_identity.py` se ejerce sobre el repositorio real al medir el scope declarado de cada Plan; la identidad semántica de contexto no tiene dogfood anclado. |
| 5 | Qué condiciones se probaron | Determinismo (mismo contenido ⇒ misma identidad); independencia del orden de descubrimiento; no conflación entre los tres dominios. |
| 6 | Qué condiciones **no** se probaron | Estabilidad de la identidad frente a cambios de proveedor o de versión de modelo; identidad bajo contenido real de una sesión completa. |
| 7 | Qué garantía puede considerarse demostrada | Que la identidad es determinista y que los dominios semántico/materialización/proveedor no se mezclan. |
| 8 | Qué garantía permanece sin demostrar | Que la identidad se corresponda con la del proveedor real: el runtime declara explícitamente que no dice nada sobre si el proveedor efectivamente usa la caché. |
| 9 | Qué limitaciones existen | Sin provider API; la identidad es de ARgentOS, no del proveedor; sin telemetría que la correlacione con el uso real. |

### C-13 — Materialization (BOTH)

**Nivel de madurez: `testeado`** — la materialización canónica está implementada y probada en dos generaciones de contrato, sin invocación de proveedor (declarado: «implementa la capacidad, no su uso»).

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Produce, desde el contexto semántico, una materialización canónica y estable (prompt + tool calls) apta para un proveedor, con contrato de orden. |
| 2 | Qué mecanismo lo implementa | `runtime/toolcalls/canonical.py`, `runtime/toolcalls/prompt_rendering.py`, `runtime/toolcalls/toolcalls_rendering.py`, `runtime/README.md` §Canonical materialization contract; `docs/rfc/72-provider-prompt-cache-capability.md` y `docs/rfc/78-provider-bound-stable-prefix-materialization.md`. |
| 3 | Qué tests existen | `tests/test_canonical_materialization.py` (41), `tests/test_canonical_materialization_v2.py` (42) —incluido el Ordering Contract v2—, `tests/test_toolcalls.py` (12). |
| 4 | Qué dogfooding existe | `GAP` — sin suite anclada al repositorio; la evidencia es de pruebas aisladas contra entradas construidas. |
| 5 | Qué condiciones se probaron | Forma canónica; orden estable (prefijo estable provider-bound); determinismo; separación respecto de la identidad semántica. |
| 6 | Qué condiciones **no** se probaron | Materialización consumida por un proveedor real; estabilidad del prefijo a través de versiones reales del proveedor; latencia y coste. |
| 7 | Qué garantía puede considerarse demostrada | Que la materialización es determinista y respeta el contrato de orden declarado, verificado por pruebas. |
| 8 | Qué garantía permanece sin demostrar | Que la materialización **produzca** el efecto pretendido (hit de caché, ahorro, formato aceptado) en un proveedor: el repositorio declara que no invoca ninguno. |
| 9 | Qué limitaciones existen | Sin provider API, sin pricing, sin TTL/eviction, sin telemetría; el `ProviderAdapter` de RFC-72 es frontera de Prompt Cache y **no** se reutiliza como mecanismo de invocación de modelo. |

### C-14 — Prompt Cache (BOTH)

**Nivel de madurez: `dependiente de una condición externa`** — la capacidad está implementada y dogfoodeada sobre el payload real, pero su garantía (que el caché se use) pertenece al proveedor.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Materializa el prefijo estable y expone las piezas abstractas de la capacidad de Prompt Cache (referencia opaca propiedad del proveedor, coordinación), sin afirmar que el caché se use. |
| 2 | Qué mecanismo lo implementa | `runtime/toolcalls/provider_cache.py`, `runtime/toolcalls/cache_coordinator.py`, `docs/rfc/72-provider-prompt-cache-capability.md`, `docs/rfc/78-provider-bound-stable-prefix-materialization.md`, `runtime/README.md` §Provider adapter boundary. |
| 3 | Qué tests existen | `tests/test_prompt_cache_dogfood.py` (18), `tests/test_canonical_materialization_v2.py` (42), `tests/test_toolcalls.py` (12). |
| 4 | Qué dogfooding existe | `tests/test_prompt_cache_dogfood.py` verifica los diez puntos de RFC-78/Plan 121 **sobre el payload real** `protocol/`; es dogfood anclado y está en la tabla del conjunto anclado de `tests/AGENTS.md`. |
| 5 | Qué condiciones se probaron | Los diez puntos verificables del contrato sobre el payload real; frontera del adaptador; que no se invoca proveedor ni se escribe telemetría. |
| 6 | Qué condiciones **no** se probaron | Un proveedor real: hit de caché, TTL, evicción, ahorro de costo, latencia. El runtime declara que no dice nada sobre si ARgentOS intenta usar el caché ni si el proveedor lo usa (`I-MAT-008/009`). |
| 7 | Qué garantía puede considerarse demostrada | Que ARgentOS produce el prefijo estable correcto y mantiene la frontera del proveedor, verificado por dogfood anclado. |
| 8 | Qué garantía permanece sin demostrar | El beneficio de la capacidad: uso efectivo del caché y su efecto económico. Depende enteramente del proveedor. |
| 9 | Qué limitaciones existen | Sin provider API, pricing, TTL/eviction ni telemetría en el repositorio; la referencia de caché es opaca y propiedad del proveedor; la economía es RFC-74 (fuera de alcance). |

### C-15 — Placement (DEV)

**Nivel de madurez: `limitado por un boundary conocido`** — el resolver y el contrato están implementados, testeados y dogfoodeados, pero el **enforcement mecánico está diferido por declaración**: la garantía efectiva es la resolución, no el cumplimiento.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Determina canónicamente dónde vive un artefacto en el repositorio (familias, namespaces, clase documental) y resuelve o exige detenerse. |
| 2 | Qué mecanismo lo implementa | `runtime/placement/resolver.py`, `runtime/placement/rules.py`, `docs/placement-contract.md`, `docs/plans/131-placement-resolver-implementation.md`; convención en `docs/AGENTS.md`. |
| 3 | Qué tests existen | `tests/test_placement_resolver.py` (31), `tests/test_placement_contract_drift.py` (9, anclado), `tests/test_placement_dogfood.py` (6, anclado). |
| 4 | Qué dogfooding existe | `test_placement_dogfood.py` verifica que el resolver coincide con el árbol real (namespaces canónicos, sus propios artefactos ubicados por sus reglas, y el área generada que el host usa) y `test_placement_contract_drift.py` mantiene el contrato y `runtime/placement/rules.py` en lockstep. |
| 5 | Qué condiciones se probaron | Resolución de las familias realizadas; deriva contrato↔reglas; vocabulario `kind` no leído como enum cerrado; ubicación real del propio corpus. |
| 6 | Qué condiciones **no** se probaron | Aplicación mecánica del placement en el momento de escribir: el `Enforcement deferred` del contrato de placement (`docs/placement-contract.md`, §24) declara que el enforcement mecánico **no está implementado** y que su consumo por el Orchestrator exige un Change propio. |
| 7 | Qué garantía puede considerarse demostrada | Que la ubicación canónica es determinable y que el resolver no contradice al contrato (drift verificado). |
| 8 | Qué garantía permanece sin demostrar | Que un artefacto mal ubicado sea **impedido** o detectado automáticamente. La garantía es de resolución y conformidad del resolver, no de cumplimiento del repositorio. |
| 9 | Qué limitaciones existen | Enforcement diferido por decisión (`PC-2`/plan 129, cerrado como decisión con implementación diferida); materialización parcial en el plan 131 registrada como `PC-72.1`, sin promoción a enforcement por inferencia; la persistencia de Project/Knowledge depende de la semántica de lifetime del contrato Protocol (plane 125, abierto). |

### C-16 — Discovery (PROTOCOL)

**Nivel de madurez: `no demostrado`** — el subsistema existe como especificación completa (políticas, roles, estados, 22 contratos) y su subconjunto mecánico está validado por checker con dogfood anclado, pero **no hay evidencia de que una discovery real se haya ejecutado y producido su resultado**.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Un subsistema de orquestación que descubre el estado de un proyecto adoptante y produce un cuerpo documental de descubrimiento (KB entry/report y contratos por dominio). |
| 2 | Qué mecanismo lo implementa | `protocol/.agents/orchestrators/discovery/` (`harness/policies/D00-discovery-init.md`, `D01-discovery-output.md`, `roles/discovery_orchestrator.md`, `roles/workers/*`, `states/`, `workflow/`, 22 contratos en `contracts/`), gate de consentimiento `discovery_require_consent` en `protocol/.agents/features.toml`, detección por el Orchestrator core. |
| 3 | Qué tests existen | `tests/test_check_discovery_output.py` (48) y `tests/test_discovery_output_dogfood.py` (14, anclado) validan el **checker** del subconjunto mecánico D01 contra los contratos reales y el payload real. **No hay suite que ejercite una ejecución de discovery.** |
| 4 | Qué dogfooding existe | Sólo el del checker (`test_discovery_output_dogfood.py`): paridad entre el subconjunto mecánico y los contratos reales. Ninguna corrida de discovery sobre un proyecto real está registrada **en este repositorio**. |
| 5 | Qué condiciones se probaron | Forma y metadata de los artefactos de salida declarados por D01, contra los contratos reales; activación del checker sobre el payload. |
| 6 | Qué condiciones **no** se probaron | Una ejecución real de discovery (detección, consentimiento, workers, estados, producción de KB); operación con un proyecto adoptante; comportamiento del orquestador de discovery bajo LLM real. |
| 7 | Qué garantía puede considerarse demostrada | Que los artefactos de salida declarados tienen una forma verificable mecánicamente y que el checker no contradice los contratos del payload. |
| 8 | Qué garantía permanece sin demostrar | Que Discovery **descubra**: que produzca un cuerpo de conocimiento correcto sobre un proyecto. No hay evidencia ejecutable de ello. |
| 9 | Qué limitaciones existen | Depende de agentes con LLM (fuera del repositorio); el checker cubre sólo el subconjunto mecánico; `llm_discovery`/`discovery_orchestrator`/`discovery_require_consent` son flags **declarativos**, leídos por agentes y no impuestos por código; la evidencia de adopción real vive fuera del repositorio y no se usó aquí. |

### C-17 — Discovery KB (PROTOCOL)

**Nivel de madurez: `no demostrado`** — la persistencia y la resolución de la KB de proyecto están implementadas y probadas, pero **no hay evidencia de una KB real producida y consumida** por el subsistema de discovery o por agentes.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Persiste el conocimiento de proyecto (namespace `ProjectIdentity`) y lo resuelve por segmentos, de modo que el descubrimiento de un proyecto quede disponible para su consumo posterior. |
| 2 | Qué mecanismo lo implementa | `runtime/toolcalls/project_store.py`, `runtime/toolcalls/project_segment.py`, `runtime/toolcalls/segment_resolution.py`, contratos `KB_DISCOVERY_ENTRY.md`/`KB_DISCOVERY_REPORT.md` del subsistema discovery, `docs/rfc/73-project-persistence.md` (plan 90). |
| 3 | Qué tests existen | `tests/test_project_segment.py` (37), `tests/test_segment_resolution.py` (24), `tests/test_check_discovery_output.py` (48). |
| 4 | Qué dogfooding existe | `GAP` — no hay suite anclada al repositorio ni KB real versionada; las pruebas construyen segmentos y entradas en aislamiento. |
| 5 | Qué condiciones se probaron | Derivación de segmentos sobre la KB existente; resolución por namespace y precedencia; forma de los contratos de KB entry/report. |
| 6 | Qué condiciones **no** se probaron | Una KB real producida por discovery y consumida por agentes; enforcement de su persistencia; el placement de la KB en un proyecto adoptante. |
| 7 | Qué garantía puede considerarse demostrada | Que la persistencia semántica de proyecto es determinista y verificable sobre entradas construidas. |
| 8 | Qué garantía permanece sin demostrar | Que el conocimiento descubierto esté efectivamente disponible y sea usado: sin una KB real y sin consumo, la garantía de «disponibilidad del conocimiento» no está demostrada. |
| 9 | Qué limitaciones existen | La semántica de lifetime/persistence en el contrato Protocol sigue abierta (`docs/plans/125-repository-architecture-decisions.md`); el enforcement de placement y persistencia está diferido (`docs/placement-contract.md` §24); sin consumo por el Orchestrator DEV. |

### C-18 — Protocol gates (PROTOCOL)

**Nivel de madurez: `testeado`** — el validador de gates y el gate de hooks tienen cobertura amplia y se ejecutan en CI, pero no hay evidencia en este repositorio de su comportamiento en una sesión de adopción real.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Verifica que cada transición de la máquina de estados del Protocol satisface sus condiciones (gates H00–H15 y policies asociadas) y veta cuando no. |
| 2 | Qué mecanismo lo implementa | `protocol/.agents/harness/gate_validator.py`, `protocol/.agents/harness/policies/*`, `protocol/.agents/orchestrators/*/harness/policies/*`, `harness/INDEX.md`. |
| 3 | Qué tests existen | `protocol/.agents/harness/tests/test_gate_validator.py` (55) y `protocol/.agents/harness/tests/test_hook_gate.py` (25), entre 179 funciones de test en 12 módulos del harness. |
| 4 | Qué dogfooding existe | `GAP` para el repositorio DEV: el harness se prueba como producto, no se ejercita sobre este repositorio (que **no** sigue el Protocol como adoptante). La corrida en CI (`check-protocol.yml`) es regresión del producto, no dogfood del repo. |
| 5 | Qué condiciones se probaron | Decisiones de gate sobre fixtures; coherencia seccional de H00 (AL-004); gates de hooks; el flujo enforced end-to-end. |
| 6 | Qué condiciones **no** se probaron | Una sesión de adopción real con agentes y LLM; validación de gates sobre artefactos producidos por agentes reales; concurrencia de hooks en un proyecto adoptante. |
| 7 | Qué garantía puede considerarse demostrada | Que el validador veta conforme al contrato declarado en sus policies, verificado por tests deterministas y ejecutado en CI en cada push. |
| 8 | Qué garantía permanece sin demostrar | Que el Protocol **se cumpla** en una adopción real: la evidencia de sesiones adoptantes existe fuera de este repositorio y no se usó. |
| 9 | Qué limitaciones existen | Producto (payload), no DEV; los gates son mecánicos sobre forma/coherencia, no sobre corrección semántica del trabajo; dependen del runner y del estado del proyecto adoptante. |

### C-19 — enforced mode / hooks (PROTOCOL)

**Nivel de madurez: `testeado`** — el ciclo de instalación, estado y salud de los hooks tiene cobertura amplia y corre en CI; no hay evidencia de instalación y operación en un proyecto adoptante real dentro de este repositorio.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Instala los hooks de control, mantiene el estado del runner, aplica límites operativos y limpia/actualiza/desinstala el andamiaje de forma transaccional y verificable. |
| 2 | Qué mecanismo lo implementa | `protocol/.agents/harness/{hook_gate,runner_state,lifecycle,lifecycle_contract,lifecycle_staging,roots}.py`, `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md`, `protocol/.agents/harness/health_check.py`. |
| 3 | Qué tests existen | `test_enforced_flow.py` (3), `test_runner_state.py` (33), `test_lifecycle_install.py` (15), `test_lifecycle_update_uninstall.py` (11), `test_lifecycle_transaction.py` (7), `test_lifecycle_limits.py` (4), `test_lifecycle_contract.py` (7), `test_roots.py` (8), `test_operational_invocations.py` (6) = **94** funciones; más `test_health_probe.py` (5). |
| 4 | Qué dogfooding existe | `GAP` — el andamiaje se prueba sobre proyectos construidos en `tmp_path`; la sonda de salud crea y limpia `protocol/.project` sin dejar artefactos, pero no hay instalación real en un adoptante registrada aquí. |
| 5 | Qué condiciones se probaron | Instalación, actualización, desinstalación y límites; transaccionalidad; resolución de raíces (`ARGENTOS_ROOT` vs `PROJECT_ROOT`); round-trip de estado; el probe de salud no infiere el root de su propia ubicación. |
| 6 | Qué condiciones **no** se probaron | Adopción real con hooks activos en un proyecto de usuario; comportamiento bajo runners distintos; concurrencia de sesiones en un mismo proyecto. |
| 7 | Qué garantía puede considerarse demostrada | Que el ciclo de vida del andamiaje es transaccional y verificable, y que el modo enforced veta en el flujo probado; ejecutado también en CI. |
| 8 | Qué garantía permanece sin demostrar | Que el modo enforced **no pueda** ser eludido fuera del canal (por ejemplo, edición directa de `.agents/`): el Protocol lo declara como desviación que invalida el payload y exige `RECOVERY`, pero no lo impide mecánicamente. |
| 9 | Qué limitaciones existen | Producto, no DEV; depende del runner y del sistema operativo del adoptante; el estado vive en `.project/` del proyecto adoptante (efímero por diseño); sin backend de observabilidad. |

### C-20 — EARS (PROTOCOL)

**Nivel de madurez: `dogfoodeado`** — las tres fuentes de verdad del payload real están en paridad verificada por una suite anclada, más una suite de falsificación.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Verifica que los requisitos redactados en forma EARS sigan el patrón canónico y estén cubiertos, activando la validación EARS en la fase H01 correspondiente. |
| 2 | Qué mecanismo lo implementa | `tools/check_ears_coverage.py`, el estándar de requisitos del payload (patrones EARS), el contrato canónico de forma y la activación de `ears` para H01 en `protocol/.agents/harness/gate_validator.py`. |
| 3 | Qué tests existen | `tests/test_check_ears_coverage.py` (38), `tests/test_check_ears_coverage_falsification.py` (25, falsificación adversarial) y `tests/test_check_ears_coverage_dogfood.py` (18, anclado). |
| 4 | Qué dogfooding existe | `test_check_ears_coverage_dogfood.py` verifica la paridad de las **tres** fuentes de verdad del payload real: los patrones del estándar, la forma canónica del contrato y la activación del validador para H01. |
| 5 | Qué condiciones se probaron | Conformidad de forma; cobertura; paridad entre las tres fuentes reales; casos de falsificación (patrones inválidos, cobertura incompleta). |
| 6 | Qué condiciones **no** se probaron | Requisitos EARS producidos en una adopción real; ampliación del conjunto mecánico (el ROADMAP declara que hacerlo es un cambio de contrato del payload y exige RFC-56 Clase A). |
| 7 | Qué garantía puede considerarse demostrada | Que el conjunto mecánico verificado está en paridad con las fuentes de verdad reales del payload y que la falsificación adversarial no lo rompe. |
| 8 | Qué garantía permanece sin demostrar | Que la validación cubra **todos** los patrones EARS utilizables por un adoptante: el conjunto es explícitamente acotado. |
| 9 | Qué limitaciones existen | Conjunto mecánico acotado (su ampliación es Clase A); valida forma/cobertura, no la calidad semántica del requisito; el estándar es del payload, no del DEV. |

### C-21 — Skills (PROTOCOL)

**Nivel de madurez: `implementado`** — el catálogo existe y es estructuralmente válido (invariantes y taxonomía lo cubren), pero **no hay consumidor**: DEV no consume skills y no hay evidencia ejecutable de una skill ejecutándose.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Provee capacidades invocables (skills) que un agente del Protocol puede usar para tareas específicas (extracción, validación, formato, revisión, deliberación, etc.). |
| 2 | Qué mecanismo lo implementa | `protocol/.agents/skills/` (**34** skills, cada una con `SKILL.md`), el mecanismo de skills documentado en `docs/plans/skills-mechanism.md`, el renderizado de tool calls en `runtime/toolcalls/toolcalls_rendering.py` y la validación estructural del payload (`tools/check_protocol_invariants.py`, `tools/check_taxonomy_coherence.py`). |
| 3 | Qué tests existen | `tests/test_toolcalls.py` (12) renderiza tool calls con **fixtures** de skills (`tests/fixtures/skills/`), no con las 34 skills del payload; la estructura del payload la cubren `check_protocol_invariants` (216 archivos, 10457 referencias) y `check_taxonomy_coherence`. **No hay suite que ejecute una skill del payload.** |
| 4 | Qué dogfooding existe | `GAP` — ninguna skill del payload se ejecutó en este repositorio; `runtime/orchestrator/agent_worker.py` declara explícitamente que skills y perfiles están ausentes del MVP por diseño («DEV has no skill consumer»). |
| 5 | Qué condiciones se probaron | Existencia y estructura del catálogo (invariantes de payload, coherencia taxonómica); renderizado de tool calls sobre fixtures; registro de la skill `adversarial-deliberation` y su contrato. |
| 6 | Qué condiciones **no** se probaron | Ejecución de una skill; selección/invocación por un agente; efecto de una skill sobre un artefacto; interoperabilidad con un proveedor. |
| 7 | Qué garantía puede considerarse demostrada | Que el catálogo existe, es estructuralmente válido y no rompe los invariantes del payload. |
| 8 | Qué garantía permanece sin demostrar | Que una skill **haga** lo que declara: no hay evidencia ejecutable de comportamiento. |
| 9 | Qué limitaciones existen | Sin consumidor en DEV (ausencia declarada en el MVP del Agent Worker); las skills son datos del payload, no instrucciones del workspace DEV; su efecto real depende de un agente con LLM. |

### C-22 — Deliberation (PROTOCOL)

**Nivel de madurez: `dogfoodeado`** — la capacidad se dogfoodeó a sí misma (Plan 120) y tiene 49 pruebas; su registro de dogfood vive en un directorio efímero y su límite de independencia está declarado y aceptado.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Producir un juicio adversarial trazable mediante pasadas atribuidas con compromiso previo a la revelación, proveniencia declarada y un veredicto cerrado, sin crear autoridad. |
| 2 | Qué mecanismo lo implementa | `docs/rfc/77-protocol-native-adversarial-deliberation.md`, `protocol/.agents/skills/adversarial-deliberation/SKILL.md`, el comportamiento de invocación del Orchestrator core y el contrato `DELIBERATION_REPORT.md` (`DEL-001`…`DEL-012`). |
| 3 | Qué tests existen | `tests/test_adversarial_deliberation.py` (**49** funciones), entre ellas los escenarios adversariales de proveniencia y contaminación entre pasadas. |
| 4 | Qué dogfooding existe | El propio Change del Plan 120: `.project/1fe5a73f-d064-4d1d-8f5c-9d8b0f2a7c31/01/09-DELIBERATION_REPORT.md`, con la limitación de contaminación entre pasadas aceptada por el acto humano `H-6` y declarada como riesgo, no como no-evento. |
| 5 | Qué condiciones se probaron | Forma del reporte y self-checks `DEL-001`…`DEL-012`; compromiso antes de la revelación; proveniencia declarada; veredicto cerrado; recomendación advisory; persistencia de sesión. |
| 6 | Qué condiciones **no** se probaron | Independencia epistémica real: el MVP **no** la reclama («atestiguada, no impuesta»); separación técnica garantizada; diversidad de modelo/proveedor; consumo de la deliberación por el orquestador DEV. |
| 7 | Qué garantía puede considerarse demostrada | Que la deliberación deja un registro trazable y auditable, con compromiso previo y proveniencia declarada, verificado por 49 pruebas y por su propio dogfood. |
| 8 | Qué garantía permanece sin demostrar | Que las conclusiones de la deliberación sean independientes o libres de contaminación cruzada. El acto de cierre lo declara explícitamente como limitación aceptada. |
| 9 | Qué limitaciones existen | Persistencia **de sesión** e informativa: el registro del dogfood vive en `.project/` (efímero, no versionado); el MVP nunca debe reclamar independencia epistémica ni separación técnicamente garantizada; no se autorizó enforcement, aislamiento ni diversidad de modelo. |

### C-23 — Change Governance (PROTOCOL)

**Nivel de madurez: `testeado`** — contrato y escritor implementados y probados; los artefactos reales existen sólo en el directorio efímero del proyecto, sin versión.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Registra de forma append-only las decisiones, autorizaciones y cierres de un cambio del Protocol, con identidad de cambio derivada del contenido y del namespace, sin fusionar registro con autoridad. |
| 2 | Qué mecanismo lo implementa | `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`, `runtime/toolcalls/change_governance.py`, `runtime/orchestrator/governance.py` (escritor del registro autorizado por el Plan, con reemplazo puro o append marker-guarded). |
| 3 | Qué tests existen | `tests/test_change_governance.py` (11), más los escenarios de gobernanza de `tests/test_determine_execution_state.py` (69). |
| 4 | Qué dogfooding existe | Tres artefactos de gobernanza reales en `.project/changes/` (Planes 119 y 120), **efímeros**: `.project/` no está versionado. El dogfood del Plan 120 es el más completo (decisiones, autorizaciones y cierre con evidencia). |
| 5 | Qué condiciones se probaron | Entradas append-only; derivación de `change_identity`; escritura marker-guarded; el registro no se escribe si la autoridad no existe. |
| 6 | Qué condiciones **no** se probaron | Persistencia durable y versionada del registro (vive en `.project/`); uso del mecanismo en la capa DEV para los Changes recientes (los Planes 149–161 usan el lifecycle DEV, no `CHANGE_GOVERNANCE.md`). |
| 7 | Qué garantía puede considerarse demostrada | Que el registro es append-only y derivable, y que su escritura está subordinada a la autoridad existente (no se escribe gobernanza sin autorización). |
| 8 | Qué garantía permanece sin demostrar | Que el registro sea reconstruible después de una limpieza de sesión: sin versionado, la evidencia no sobrevive al entorno efímero. |
| 9 | Qué limitaciones existen | Producto, no DEV; persistencia en `.project/` (efímero); el registro nunca es autoridad; sin backend ni registro global. |

### C-24 — Metrics / health (BOTH)

**Nivel de madurez: `parcialmente demostrado`** — la agregación y el chequeo de salud funcionan y están probados, pero la **medición operacional** de las métricas del lifecycle está declarada como perteneciente al Incremento 4, que no está materializado.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Agrega métricas de sesión, valida los bloques de métricas de los artefactos de sesión y verifica la salud del protocolo en un proyecto adoptante (incluido un round-trip de almacenamiento de estado). |
| 2 | Qué mecanismo lo implementa | `tools/aggregate_metrics.py`, `docs/VERSIONING.md` §11 (schema baseline), `tools/check_session_artifacts.py` (bloques `ENTRY`/`METRIC`), `protocol/.agents/harness/health_check.py` y `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md`, `protocol/.agents/features.toml` (`[health_check] ttl_hours`). |
| 3 | Qué tests existen | `tests/test_aggregate_metrics.py` (32), `tests/test_check_session_artifacts.py` (60), `protocol/.agents/harness/tests/test_health_probe.py` (5, en CI), `tests/test_memory_migration_metrics_cutover.py` (6). |
| 4 | Qué dogfooding existe | El probe de salud crea y limpia `protocol/.project` sin dejar artefactos (round-trip real); `check_session_artifacts` es OK sobre el repositorio real (`Session artifacts OK`). No hay serie histórica de métricas producida por el DEV. |
| 5 | Qué condiciones se probaron | Agregación sobre entradas de prueba; validación de bloques de métricas; round-trip de escritura/lectura/borrado del probe; exit codes del probe. |
| 6 | Qué condiciones **no** se probaron | Medición **operacional** de las métricas del Change Lifecycle (queries/agregación sobre el corpus): el schema declara explícitamente «sin medición operacional hasta el Incremento 4»; sin backend, sin writer obligatorio, sin thresholds, sin gate de release; 0 registros = `not applicable`. |
| 7 | Qué garantía puede considerarse demostrada | Que los campos que alimentan las métricas existen desde los Incrementos 1+2+3 y que la agregación y la validación de bloques funcionan sobre entradas reales y de prueba. |
| 8 | Qué garantía permanece sin demostrar | Que las métricas **midan** algo del ciclo real (cobertura de anchors, tasa de validaciones stale, anomalías de cierre): no hay serie ni agregación operacional. |
| 9 | Qué limitaciones existen | Sin backend, sin thresholds, sin gate de release; la observabilidad del DEV se apoya en la reconstruibilidad, no en telemetría (`RFC-74` fuera de alcance); el probe de salud es del producto y no forma parte de la batería canónica. |

### C-25 — Feature flags (PROTOCOL)

**Nivel de madurez: `parcialmente demostrado`** — el catálogo existe, el harness resuelve flags y el ciclo de instalación lo materializa, pero la mayoría de las flags son **declarativas** (obligación de comportamiento leída por agentes) y no hay verificación de que se cumplan.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Declara el catálogo de flags del Protocol (booleanas e integer, algunas declarativas) y permite que el comportamiento del sistema dependa de la configuración activa del adoptante. |
| 2 | Qué mecanismo lo implementa | `protocol/.agents/features.toml` (plantilla **inerte** del payload), el catálogo canónico en `protocol/.agents/standards/INDEX.md` §Feature flags, y los consumidores del harness `protocol/.agents/harness/{gate_validator,hook_gate,lifecycle_contract,lifecycle,roots}.py`; la única configuración activa es `ARGENTOS_ROOT/features.toml`. |
| 3 | Qué tests existen | Cobertura indirecta en `protocol/.agents/harness/tests/` (materialización y contrato del ciclo de instalación: `test_lifecycle_install.py` 15, `test_lifecycle_contract.py` 7, `test_roots.py` 8) y en `tests/test_change_governance.py` (11). No hay suite dedicada a la semántica de cada flag. |
| 4 | Qué dogfooding existe | `GAP` — el repositorio DEV no tiene `features.toml` activo ni consume flags; la verificación es del producto en proyectos construidos en pruebas y en CI. |
| 5 | Qué condiciones se probaron | Existencia del catálogo y su carácter de plantilla inerte; resolución del archivo activo desde `ARGENTOS_ROOT`; materialización por el ciclo de instalación; consumo por el harness. |
| 6 | Qué condiciones **no** se probaron | Cumplimiento de las flags **declarativas** (rubrics, knowledge_base, caveman, llm_discovery, discovery_orchestrator, discovery_require_consent, prácticas técnicas, `architecture_contract=false`): crean una obligación de comportamiento para los agentes, y **ningún código las impone**; tampoco se probó el override por configuración del adoptante. |
| 7 | Qué garantía puede considerarse demostrada | Que el catálogo canónico existe, que la plantilla del payload nunca es la configuración activa y que el harness resuelve flags desde la raíz del proyecto correcta. |
| 8 | Qué garantía permanece sin demostrar | Que una flag declarativa **cambie** efectivamente el comportamiento: sin enforcement mecánico, la garantía es una expectativa sobre el agente. |
| 9 | Qué limitaciones existen | Producto, no DEV; las declarativas dependen del agente; sin verificación de conformidad; el archivo del payload debe tratarse siempre como dato, nunca como configuración. |

### C-26 — recovery (DEV)

**Nivel de madurez: `parcialmente demostrado`** — la recuperación dentro del mismo envolvente está implementada y probada, pero no existe el mecanismo de retry que la política nombra, y no se probó con fallos reales de un actor externo.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Ante un fallo dentro del `Scope` y la autoridad, el host diagnostica, corrige/reintenta, verifica y continúa —con el mismo envelope, dejando evidencia y sin ocultar la recuperación—; ante un fallo que exige nuevo scope/autoridad, se detiene. |
| 2 | Qué mecanismo lo implementa | `.agents/policies/supervised-autonomous-execution.md` §4, §7, `runtime/orchestrator/host.py` (bucle de iteración, `RUN_REVALIDATION`), `runtime/orchestrator/autonomy.py` (`evaluate_finding_resolution`), `runtime/orchestrator/store.py` (journal con `GAP` declarado). |
| 3 | Qué tests existen | `tests/test_autonomous_scope.py` (58), `tests/test_autonomous_orchestrator.py` (31), `tests/test_autonomy_effects.py` (36), `tests/test_determine_execution_state.py` (69). |
| 4 | Qué dogfooding existe | `DEV_AUTONOMOUS_ORCHESTRATOR_DOGFOOD_2026-09-14.md` (recuperación y revalidación observadas con señales de gate `GAP`/`VALID` sobre el repositorio real). |
| 5 | Qué condiciones se probaron | Revalidación sobre contenido cambiado (`A1 → A2`) sin reemplazar A1; fallo dentro del scope que continúa; fallo que exige autoridad que se detiene; detección de escritura no declarada; `GAP` por líneas ilegibles del journal. |
| 6 | Qué condiciones **no** se probaron | Fallos reales de un actor externo: fallos de proveedor (no hay proveedor), salidas inválidas de un worker real, caídas de red o de herramientas; recuperación multi-nivel. |
| 7 | Qué garantía puede considerarse demostrada | Que la recuperación ocurre dentro del mismo envelope, que se registra como evidencia y que un fallo de autoridad detiene el ciclo en lugar de ampliarlo. |
| 8 | Qué garantía permanece sin demostrar | El **retry** como mecanismo declarado: `docs/behavior-patterns.md` §5.2 — registra que la política lo enumera y el código **no** implementa ningún mecanismo de reintento —un fallo que exige rehacer trabajo se conduce como una nueva derivación—. Es una discrepancia **declarada**, no un silencio. |
| 9 | Qué limitaciones existen | Sin recuperación multi-nivel; la «recovery» que el sistema cuenta es estrecha (reconducción por anchor stale); la corrección autónoma de findings no está cableada al loop y detenerse en un finding abierto es el comportamiento actual. |

### C-27 — CI / validation (DEV + PROTOCOL)

**Nivel de madurez: `parcialmente demostrado`** — CI ejecuta la mayor parte de la batería y la regresión del producto, pero **no** los gates de lifecycle, y `check_dist_sync` es local-only.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Verifica de forma automatizada y repetible el repositorio: invariantes del payload, citas, estructura, coherencia taxonómica, versión, artefactos de sesión, suites de test y regresión del harness del producto. |
| 2 | Qué mecanismo lo implementa | `.github/workflows/check-protocol.yml` (con `fetch-depth: 0` obligatorio para que C-2 y los dogfoods resuelvan objetos Git), `.github/workflows/publish-dist.yml`; definición canónica de la batería en `docs/VERSIONING.md` §4.1. |
| 3 | Qué tests existen | La propia batería cubre `tests/` (54 módulos, **1316** pruebas) y `protocol/.agents/harness/tests/` (12 módulos, **185** pruebas ejecutadas por parametrización sobre 179 funciones de test), ambos ejecutados por el workflow. |
| 4 | Qué dogfooding existe | El repositorio verifica su propio corpus: `check_protocol_invariants` recorre 216 archivos del payload y 10457 referencias; `check_plan_structure` valida 161 documentos; la batería corre en cada push a `dev`/`master` y en PRs. |
| 5 | Qué condiciones se probaron | Ejecución local completa de la batería y de las dos suites (1316 + 185 en verde); degradación conocida y corregida de un checkout shallow (documentada en el propio workflow). |
| 6 | Qué condiciones **no** se probaron | Los gates de lifecycle C-1/C-2/C-3 **no** están en CI (sólo se mencionan en un comentario del workflow); `check_dist_sync` es local-only y se espera verde sólo en `master`; el enforcement mecánico del Incremento 4 no existe. |
| 7 | Qué garantía puede considerarse demostrada | Que el repositorio tiene una batería única y ejecutable que cubre payload, gobernanza documental, taxonomía, versión, sesiones y test suites, y que corre automáticamente en CI. |
| 8 | Qué garantía permanece sin demostrar | Que CI cubra **todas** las garantías verificables del repositorio: tres gates de lifecycle y la sincronización de `dist` quedan fuera, de modo que una regresión en ellos no la detecta CI. |
| 9 | Qué limitaciones existen | Depende de GitHub Actions (servicio externo) y de `fetch-depth: 0`; el baseline de citas rotas (26) es rojo por diseño y no bloquea; `check_dist_sync` rojo en `dev` por diseño. |

### C-28 — distribución y sincronización de `dist` (PROTOCOL)

**Nivel de madurez: `dependiente de una condición externa`** — la publicación de `dist` depende de CI y de un acto humano de promoción, y la verificación es local-only; el repositorio no puede demostrar la sincronización por sí mismo.

| # | Dimensión | Contenido |
|---|---|---|
| 1 | Qué afirma hacer | Publica el payload adoptable como rama `dist` (sólo `.agents/` y `AGENTS.md` en la raíz), regenerada desde `master`, nunca editada a mano, y permite verificar su sincronización. |
| 2 | Qué mecanismo lo implementa | `.github/workflows/publish-dist.yml` (se dispara con push a `master` que toque `protocol/**`; renombra `_AGENTS.md` → `AGENTS.md`), la rama `dist`, `tools/check_dist_sync.py` (local-only) y `docs/VERSIONING.md` §1/§3. |
| 3 | Qué tests existen | `tests/test_check_dist_sync.py` (7). La publicación en sí no tiene suite: es un workflow de CI. |
| 4 | Qué dogfooding existe | El repositorio declara el estado publicado (`origin/dist` @ `1181db6`) y advierte que la ref local `dist` está rezagada; el chequeo se ejecuta localmente cuando el mantenedor lo corre. |
| 5 | Qué condiciones se probaron | Lógica del comparador de sincronización sobre casos construidos; invariantes de versión↔changelog↔tag (8 pruebas) que sostienen la publicación. |
| 6 | Qué condiciones **no** se probaron | Una ejecución real de `publish-dist` verificada por el repositorio: CI **no** corre `check_dist_sync`, y el chequeo se espera verde sólo en `master` (en `dev` es rojo por diseño); la promoción es un acto del mantenedor no ejercido. |
| 7 | Qué garantía puede considerarse demostrada | Que el mecanismo de publicación está declarado y acotado (sólo `protocol/**` en `master` lo dispara) y que existe una herramienta determinista de verificación de sincronización. |
| 8 | Qué garantía permanece sin demostrar | Que `dist` esté efectivamente sincronizado en todo momento: la verificación no es automática, la ref local puede estar rezagada y la sincronización depende de CI y de la promoción. |
| 9 | Qué limitaciones existen | Depende de GitHub Actions y del acto humano de promoción; `check_dist_sync` es local-only y CI no lo fetchea; el payload publicado `12.0.0` y el PATCH `12.0.1` en `dev` sin tag reflejan que la promoción está pendiente. |

## 4. Resultado de Etapa A — evidencia para la revisión posterior

> **Esto es resultado y evidencia, no decisión.** Ninguna afirmación de esta sección crea un Change, autoriza una implementación, modifica `F-C` ni resuelve `OD-1`. Se registra para que la revisión humana del alcance posterior disponga de insumo verificable.

### 4.1 Hallazgo principal

**Ninguna de las 28 capacidades alcanza `demostrado bajo condiciones reales` para la totalidad de su afirmación.** Once alcanzan `dogfoodeado` (ejercitadas en este repositorio con evidencia verificable), seis `testeado`, cuatro `parcialmente demostrado`, tres `dependiente de una condición externa`, una `limitado por un boundary conocido`, una `implementado` y dos `no demostrado`. La causa es estructural y recurrente: las condiciones de uso pretendidas de buena parte del sistema son **un proyecto adoptante** o **un proveedor real**, y ninguna de las dos cosas es observable desde este repositorio.

### 4.2 Capacidades sin garantía demostrada de su afirmación central

| Capacidad | Qué no está demostrado |
|---|---|
| `C-16` Discovery | Que descubra: no hay corrida real; sólo el checker del subconjunto mecánico está validado. |
| `C-17` Discovery KB | Que el conocimiento descubierto quede disponible y se use: no hay KB real ni consumo. |
| `C-21` Skills | Que una skill haga lo que declara: no hay consumidor ni ejecución. |
| `C-08` Agent Worker | Que produzca trabajo real: depende de un invoker que el repositorio no provee. |
| `C-14` Prompt Cache | El beneficio (uso efectivo del caché): depende del proveedor. |
| `C-28` dist | La sincronización efectiva: depende de CI y de la promoción. |

### 4.3 Límites estructurales que acotan garantías (recurrentes)

1. **Sin provider/modelo/red/credenciales.** Acota `C-08`, `C-11`, `C-12`, `C-13`, `C-14`, `C-06`, `C-02` y `C-26`.
2. **Enforcement parcial.** `C-15` (placement: enforcement diferido), `C-04`/`C-05` (gates advisory, no bloquean), `C-27` (tres gates fuera de CI), `C-25` (flags declarativas sin imposición), `C-19` (elusión fuera de canal posible).
3. **Persistencia efímera.** `C-22` y `C-23` apoyan parte de su evidencia en `.project/`, no versionado.
4. **Cobertura mecánica acotada.** `C-16`/`C-17` (subconjunto D01), `C-20` (conjunto EARS acotado, ampliarlo es Clase A), `C-18` (forma y coherencia, no semántica).
5. **Evidencia de adopción no disponible en el repositorio.** Afecta a `C-16`, `C-17`, `C-18`, `C-19`, `C-25` y `C-28`: las condiciones reales ocurren en proyectos externos y no se usaron aquí.
6. **Discrepancias declaradas** (no silencios): retry nombrado por la política y ausente del código (`C-26`), corrección autónoma de findings no cableada al loop (`C-26`), telemetría/economía fuera de alcance (`C-24`).

### 4.4 Insumo para la revisión del alcance de `F-C` / Etapa B

- De las fronteras candidatas de la Etapa B, `PR-1`/`PR-2` ya fueron absorbidas por `F-B`; esta retrospectiva **no** introduce ninguna frontera nueva.
- Las capacidades con menor madurez (`C-16`, `C-17`, `C-21`) pertenecen al payload del Protocol y su garantía depende de una adopción real, no de trabajo de autonomía del DEV.
- Las capacidades que condicionan una autonomía más amplia y que permanecen sin demostrar son `C-08` (actor real), `C-02` (contención de autoridad fuera del host) y `C-26` (recuperación con fallos reales) — exactamente el terreno que la reconnaissance asoció a `F-C`.
- **`F-C` scope = `TO BE REVIEWED`.** La disposición de este insumo corresponde a la revisión posterior (`OD-1`), con su propia autorización.
- Sin cambios en `F-C`/Etapa B por este documento: `F-C = NOT_IMPLEMENTED`, `Etapa B = NOT_STARTED`, `OD-1 = NOT YET RESOLVED`.

### 4.5 Ruta de decisión (registrada, no ejecutada)

```text
Etapa A (este documento)
   ↓  evidencia + gaps + límites
revisión humana/canónica del alcance de F-C        ← Change propio, no autorizado aún
   ↓
OD-1 (qué es F-C)
   ↓
F-C / Etapa B
```

## 5. Límites declarados de esta retrospectiva

1. **No es una auditoría de archivos ni una limpieza documental:** evalúa garantías operacionales; no propone refactors, renombrados ni reorganización.
2. **Documentación ≠ implementación.** Ninguna afirmación positiva se sostiene sólo en prosa; donde no hubo evidencia ejecutable se registró `no demostrado`, `parcialmente demostrado` o el límite correspondiente.
3. **Ausencia de evidencia ≠ evidencia de ausencia.** `no demostrado` significa «no hay evidencia ejecutable de que funcione», no «se demostró que no funciona».
4. **La evidencia externa al repositorio no se usó** (proyectos adoptantes, CI remoto, proveedores). Es el límite más importante de esta matriz y la causa de que ninguna capacidad alcance `demostrado bajo condiciones reales`.
5. **Un nivel por capacidad** por exigencia del contrato: la riqueza está en las nueve dimensiones y en las garantías «sin demostrar», no en el nivel.
6. **Sin autoridad normativa.** Este documento no decide, no autoriza y no crea trabajo; es insumo de la revisión posterior.
