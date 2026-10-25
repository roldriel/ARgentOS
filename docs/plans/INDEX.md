# Índice de planes — ARgentOS

> **Migración (RFC-69, Plan A):** este registro vive ahora en
> `docs/plans/INDEX.md`. Las convenciones normativas se migraron a
> `docs/CONVENTIONS.md`; el registro de RFCs vive en `docs/rfc/INDEX.md`.
> Las secciones `## Convenciones` y `## Serie de RFCs (documentos canónicos)`
> se conservan como anclas de navegación para referencias históricas.

Estado al 2026-10-25. El Plan 178 está **`Executed`** con condición derivada **`Closed`** (auditoría de continuidad de integración y coherencia evolutiva —Priority 3.6— ejecutada sobre el repositorio @ `759f005`: 16 capacidades clasificadas —9 `INTEGRATED`, 2 `PARTIALLY_INTEGRATED` (Memory: seam sin consumidor que suministre el store; Change Governance Artifact: semánticas diferidas y materializador sólo consumido por tests), 5 `INTENTIONALLY_ISOLATED`, 0 `ORPHANED`, 0 `CONFLICTING`—, consumidores y ausencias verificados por código, policies, entry points y tests; evaluación de la hipótesis con lo demostrado, lo sugerido y lo no evidenciado; findings F-01/F-02/F-03 abiertos/deferred sin reparaciones ejecutadas; batería canónica PASS, `pytest tests/` 1535 passed, C-1/C-2/C-3 sin `ANOMALY`; **RFC-56 Class: N/A**, Change Level L2, DEV-only, docs-only, sin payload y sin release por RFC-69; renumerado desde `177` por `<PLAN-178>:C-1`) y el Plan 177 está **`Executed`** con condición derivada **`Closed`** (rediseño completo del `README.md` como puerta de entrada al proyecto: definición del producto antes de la estructura interna, TL;DR, diagrama del ciclo de trabajo, conceptos en lenguaje llano —Change Lifecycle y Theoretical Execution como capacidades DEV, deliberación adversarial como capacidad opcional del payload, Integration Surface como idea no implementada—, un cambio de extremo a extremo, límites declarados, distinción Protocol/DEV, adopción y navegación; **RFC-56 Class: N/A**, Change Level L1, DEV-only, docs-only, sin payload y sin release por RFC-69). El Plan 176 está **`Executed`** con condición derivada **`Closed`** (cierre de Theoretical Execution **DEV complete**: reconstrucción independiente del alcance, matriz de gaps A–Q con clasificación por gap, y delta `REQUIRED` `D-1`…`D-7` —determinismo de CH-3/CH-7 sobre el commit base, registro `checks[]` y re-derivación en `--validate`, fingerprint de no-progress verificado, etiqueta de corrida determinista, CH-9 de integridad de declaración, documentación y versionado del contrato—; Gate TE del propio Plan 176 en `GAP` con `TF-01`/`TV-01`, revisión adversarial de los diez ataques y dos findings resueltos `F-1`/`F-2`; **RFC-56 Class: N/A**, Change Level L2, DEV-only, sin payload y sin release). El Plan 175 está **`Executed`** con condición derivada **`Closed`** (Implementation Plan de Theoretical Execution DEV v1: `runtime/theoretical/`, policy operativa, tests y documentación; **RFC-56 Class: N/A**, Change Level L2, DEV-only, sin payload y sin release; TE y autorización de ejecución registradas; Gate B `CONVERGED`; Validation Anchor y Checkpoint registrados en `f613147`; la fila de este INDEX se corrige **por referencia** en el Plan 176, sin editar el Plan cerrado). El Plan 174 está **`Executed`** con condición derivada **`Closed`** (materialización y cierre de Priority 3 —modelo RFC-56 / A-B-C—: RFC-56 enmendada con el modelo de payload delta, multi-clase, ruta efectiva, N/A, semántica de Class C y checker como evidencia; `docs/CONVENTIONS.md`, `docs/plans/_TEMPLATE.md`, `docs/VERSIONING.md`, `AGENTS.md` y la capa operativa `.agents/` alineados; **RFC-56 Class: N/A**, DEV-only, docs-only, sin release por RFC-69; Centésima primera serie). El Plan 173 está **`Executed`** con condición derivada **`Closed`** (corrección del cierre inválido de Phase 0.4: 11 ítems `MISCLASSIFIED`/`INSUFFICIENT_EVIDENCE` llevados a estado terminal genuino —9 implementados y 2 resueltos—, 22 residuales genuinos preservados, R5 de C-2, INDEX→archivo en `check_plan_structure`, checker `ENF-001`…`ENF-003`, tres tests de idempotencia del payload como Clase C y reconciliación completa de `docs/VERSIONING.md` §9; **Clase B + C tests-only**, publicada en `12.3.1`). El Plan 172 está **`Executed`** con condición derivada **`Closed`** (cierre de la deuda heredada de Phase 0: inventario completo con estado terminal por ítem, materialización de `E1-G2`…`E1-G5` de ADR-20, clasificación terminal de los gaps de Priority 0.2 y de las decisiones `D-0.3-12`/`D-0.3-23` de Priority 0.3, y reconciliación de los registros derivados; **Clase B** de RFC-56, DEV-only sin release; su identidad de cierre se corrige por referencia en el Plan 173). El Plan 171 está **`Executed`** con condición derivada **`Closed`** (implementación acotada del contrato de Priority 0.3). El Plan 170 está **`Executed`** con condición derivada **`Closed`** (materialización del catálogo canónico de 15 entradas —12 invariantes y 3 properties— en `docs/INVARIANTS.md` y `protocol/.agents/standards/INVARIANTS.md` con bloque **idéntico byte a byte** verificado por sha256, registro de la segunda excepción aprobada a `Single-source documentation policy` y payload a `12.2.0`; **Clase A** de RFC-56, creado por la aceptación de RFC-84, con Validation Anchor A1 y Checkpoint registrados; sin implementar los gaps de enforcement, que quedan como trabajo futuro). El Plan 165 está **`Executed`** con condición derivada **`Closed`** (implementación de `F-C` —frontera de autonomía— ejecutada y cerrada el 2026-10-13 con verificación interna, sin release: `Change Level` **L3**, `IN SCOPE`/`OUT OF SCOPE` heredados literalmente del alcance canónico 1B de `OD-1` —actor real con provider/modelo, aislamiento/sandbox con la posibilidad prevista de declarar la garantía que no se ofrece, Memory como contexto, objetivo multi-Change, `C-02` y `C-26`—, criterios `FC-1`…`FC-10` sin reducción, y las ocho decisiones de implementación `ID-1`…`ID-8`: **`ID-1`/`ID-3`/`ID-5` cerradas por acto del mantenedor del 2026-10-13** (`ID-1` actor **agnóstico** —el agente lo aporta el entorno del adoptante; no se incorpora ni prescribe provider/modelo/SDK/CLI—, `ID-3` **declara ausencia** de aislamiento proporcionado por ARgentOS, sin sandbox ni garantía nueva, `ID-5` semántica `Objetivo → Change → evaluación → siguiente Change` con evaluación explícita tras cada Change), con `ID-2`/`ID-4`/`ID-6`/`ID-7`/`ID-8` **resueltas durante la ejecución**; **`F-C` = `CLOSED`** (recuento de counterproofs con un residuo que el Plan 167 registra como finding `F-03`, reconciliado por referencia); registro de efectos declarados: `network` autorizado, `install`/`remote_git`/`destructive`/`write_outside_project` **no** declarados ni autorizados; **Nonagésima tercera serie**, ejecutada). **Estado al 2026-10-14:** el Plan 169 está **`Aprobado para ejecución`** (regularización de `81bbde1` y reconciliación de las siete pending obsoletas de los planes 161/164/165 por referencia, más la aclaración de la vía de acción directa en `.agents/AGENTS.md`; **Clase B**, sin efecto de payload). El Plan 168 está **`Executed`** con condición derivada **`Closed`** y **`Released = TRUE`** (release **`12.1.0`**: promovió `dev` → `master` por fast-forward y creó el tag anotado `12.1.0` sobre el commit `45809c1`, publicando el payload acumulado de los planes 156 —RFC-82— y 166 —RFC-83— y absorbiendo el número `12.0.1` que nunca se publicó; la **publicación remota** sigue pendiente por decisión del mantenedor). El Plan 167 está **`Executed`** con condición derivada **`Closed`** (reconciliación documental del cierre de `F-C` —propuesta del mantenedor del 2026-10-14 y **Clase B** de RFC-56, **ejecutada**: `Change Level` **L2**, alcance `IN`/`OUT` en su propio artefacto, cuatro findings evidenciados `F-01`…`F-04` —estado narrativo del modelo de autonomía, mapa operativo, registros del plan cerrado 165 **por referencia** y trazabilidad de la evidencia de auditoría—, `## Validation anchor` y `## Checkpoint / cierre` **vacíos**, sin condición derivada por su sola creación, y dos pending decisions: aprobación de ejecución y destino de los artefactos de auditoría; DEV-only `docs/` + `ROADMAP.md`, sin release; **Nonagésima cuarta serie**, ejecutada). El Plan 164 está `Executed` con condición derivada `Closed` (acto de autorización de ejecución de `F-C`: transcribe el acto del mantenedor del 2026-10-13 —autoriza la ejecución bajo el alcance 1B y la creación/formalización del Plan de ejecución con `Aprobado para ejecución`, `Change Level ≥ L3` y `FC-1`…`FC-10`, sin extender el scope ni incorporar `C-16`/`C-17`/`C-21`—, resuelve y anota de forma aditiva la pending decision del Plan 163 (regla `PC-1`), reconcilia `ROADMAP.md` (retiro del blocker de autorización; `F-C` aprobado y pendiente de ejecución) y registra que **no** se implementa `F-C` en ese Change; DEV-only docs-only, sin release; **Nonagésima tercera serie**, ejecutada). El Plan 163 está `Executed` con condición derivada `Closed` (acto de autoridad que **resuelve `OD-1`**: el mantenedor adoptó la interpretación **`B`** —`F-C` **es** la iniciativa «Complete ARgentOS Autonomy» (Etapa B) **delimitada por el resultado de la Etapa A a la frontera de autonomía**, con actor con provider/modelo, aislamiento/sandbox, Memory como contexto y objetivo multi-Change dentro, `C-02` y `C-26` como condiciones, y las brechas del payload `C-16`/`C-17`/`C-21` **fuera**— y el registro normativo **sin ADR**; el alcance canónico se registra por adición en `docs/CONVENTIONS.md` (subsección «Modelo de autonomía — alcance canónico de `F-C`») y se reconcilian `ROADMAP.md` (`F-C` en `NEXT` con alcance resuelto y **sin** autorización de ejecución; brechas del payload explícitamente fuera; blocker de ejecución no autorizada), `docs/plans/161-…md` (anotación aditiva de la resolución de la pending, regla `PC-1`) y `CHANGELOG.md`; **nada implementado**: 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`, sin Plan de `F-C` autorizado; DEV-only docs-only, sin release; **Nonagésima segunda serie**, ejecutada). El Plan 162 está `Executed` con condición derivada `Closed` (instrumento de decisión de `OD-1` —alcance canónico de `F-C`—: la verificación de autoridad concluye que la resolución es una **decisión de alcance reservada al mantenedor** y que **no está presente en el repositorio**, por lo que el Plan registra `OD1_BLOCKED` y materializa el material mínimo para ejercer el acto —lo que la evidencia de Etapa A **sí** determina (D-1…D-7), las interpretaciones `R1`/`R2`/`R3` con su soporte y su tensión, lo que **no** determina, la pregunta `Q-a`…`Q-d` con sus consecuencias, la protección contra inferencias indebidas, el registro exigido y los criterios de cierre `AC-1`…`AC-12`— sin decidir, sin definir `F-C`, sin crear un Plan de `F-C`/Etapa B y sin modificar `docs/CONVENTIONS.md` ni ADRs; DEV-only docs-only sobre `docs/plans/`, `ROADMAP.md` y `CHANGELOG.md`, sin release; **Nonagésima primera serie**, ejecutada). El Plan 161 está `Executed` con condición derivada `Closed` (autorización **y ejecución** de Etapa A: el acto del mantenedor del 2026-10-12 resolvió `PC-1` del Plan 160 y designó el Plan 161 como artefacto de ejecución; la retrospectiva produjo el **Capability & Guarantee Matrix** —`docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`, registrado en `docs/working/audits/INDEX.md`— sobre las 28 capacidades del alcance conceptual mínimo declarado por el Plan 149, con las 9 dimensiones por capacidad (252 celdas, 0 vacías) y los 8 niveles de madurez como vocabulario cerrado; distribución: `dogfoodeado` 11 · `testeado` 6 · `parcialmente demostrado` 4 · `dependiente de una condición externa` 3 · `no demostrado` 2 · `limitado por un boundary conocido` 1 · `implementado` 1 · `demostrado bajo condiciones reales` 0; `DC-1`…`DC-10` PASS y Validation Anchor A1; hallazgo central: las condiciones de uso pretendidas de buena parte del sistema —proyecto adoptante, proveedor real, CI— no son observables desde el repositorio, lo que acota la garantía máxima acreditable; `F-C`/Etapa B permanecen no iniciadas y `OD-1` sin resolver (`F-C scope = TO BE REVIEWED`); DEV-only docs-only sobre `docs/working/` y `docs/`, sin release; **Nonagésima serie**, ejecutada). El Plan 160 está `Executed` con condición derivada `Closed` (cierre de las decisiones inmediatas `OD-2` —derivación parcial: la decisión efectiva es `D-6b = NO`, la superficie está descartada y no diferida— y `OD-6` —`work_type`: el criterio de admisión y la política de declaración ya estaban canonizados por el Plan 152, de modo que se retira del ROADMAP el blocker obsoleto y `P-5` permanece `GAP` por caso—, más la preparación de la autorización de Etapa A: contrato, alcance, criterios de cierre, dependencias y Change aplicable determinados, y el acto de autorización faltante registrado como pending decision bloqueante con owner mantenedor; DEV-only docs-only sobre `docs/CONVENTIONS.md`, `docs/adr/19-autonomy-envelope-authority.md`, `ROADMAP.md`, este INDEX y `CHANGELOG.md`, sin release; **Octogésima novena serie**, ejecutada). El Plan 159 está `Executed` con condición derivada `Closed` (materialización del envelope de autonomía `F-B`: cierra `OPD-1` —adopción del vocabulario DEV de clases de efecto ya materializado en `tools/check_session_artifacts.py`— y `OPD-2` —techo de recurso como guarda operativa de terminación, nunca autorización— e implementa los dos bloqueantes del relevamiento de cierre: `BLK-1` admisión de efectos antes de delegar, con `Effect` ortogonal a `Scope`, y `BLK-2` terminación por recurso con consumo acumulado desde el journal y supervivencia a reinicio; DEV-only `runtime/orchestrator/` + `tests/` + `.agents/policies/` + `docs/`, sin release; **Octogésima octava serie**, ejecutada). El Plan 158 está `Executed` con condición derivada `Closed` (simplificación radical del ROADMAP: reduce `ROADMAP.md` de 367 a 99 líneas aplicando *reduce, not reorganize* — elimina del documento el capability inventory, el informe de autonomía, el índice documental y el manual de gobernanza, que ya tienen artefacto dueño, sin crear documentos nuevos; DEV-only `ROADMAP.md` + `docs/plans/` + `CHANGELOG.md`, sin release; **Octogésima séptima serie**, ejecutada). El Plan 157 está `Executed` con condición derivada `Closed` (contrato canónico y ROADMAP visual estratégico: establece el contrato documental del ROADMAP en `docs/CONVENTIONS.md`, reemplaza su estructura por una representación visual `NOW → NEXT → LATER` con dominio/prioridad/status por iniciativa, registra el término en el glosario y reconcilia referencias cruzadas; DEV-only `ROADMAP.md` + `docs/` + `README.md` + `AGENTS.md` + `CHANGELOG.md`, sin release; **Octogésima sexta serie**, ejecutada). El Plan 146 está `Executed` (Change de release: promoción de `dev` a
`master` y release del rango `11.3.0`–`11.6.1`, con los tags anotados `11.3.0`, `11.4.0`,
`11.5.0`, `11.6.0` y `11.6.1` sobre el commit de promoción y `dist` regenerado por
`publish-dist`; DEV-only sobre `CHANGELOG.md`, `docs/VERSIONING.md`, este INDEX y su propio
artefacto, sin efecto en `protocol/.agents/`, por lo que RFC-56 no aplica; Change Level L2
con impacto de release 2; Septuagésima séptima serie). El Plan 156 está `Executed` con condición derivada `Closed` (reconciliación
documental del payload con el layout canónico `.argentos/`, implementación de RFC-82 `Accepted`: bootstrap real
`.argentos/.agents/INDEX.md` y adapter no normativo, frontera de artefactos bajo el layout canónico, enumeración de los
ocho módulos stdlib distribuidos y distinción `dist` vs layout materializado; **PATCH** de payload, con promoción
pendiente de autorización separada; **Octogésima quinta serie**, ejecutada). El Plan 155 está `Executed` con condición derivada `Closed` (refresh documental
post-autonomía e integración de clientes: reconstrucción del estado real, auditoría de la documentación contra ese
estado, reconciliación del drift de versión al release publicado `12.0.0`, y materialización de `docs/behavior-patterns.md`;
DEV-only `docs/` + `README.md` + `CHANGELOG.md` + `ROADMAP.md`, sin release; **Octogésima cuarta serie**, ejecutada). El
Plan 145 está `Executed` con condición derivada `Closed` (cierre
integral del backlog accionable DEV `I-1`…`I-8`: aislamiento del pytest harness por sesión,
frontera de observación que no confunde un recurso vital ilegible con uno ausente, semántica
corregida de `recoveries` y derivación real de `findings_autonomously_corrected`, y la
reconciliación de los espejos documentales de los Planes 137/143/144, el backlog evidenciado
`B-4`/`B-7`, el Placement Contract y el conjunto anclado de `tests/AGENTS.md`; DEV-only
`tests/` + `runtime/` + `conftest.py` + `docs/` + `.agents/policies/`, sin release;
Septuagésima sexta serie). El Plan 144 está `Executed` con condición derivada `Closed` (higiene
documental y de tests del backlog DEV residual: la tabla del conjunto anclado de
`tests/AGENTS.md` pasa de 8 a 13 módulos, se eliminan las dos sentencias `sys.path.insert`
redundantes de `tools/` en las suites de discovery y se reconcilian tres espejos
documentales —fila de RFC-75 en `docs/rfc/INDEX.md`, registro de investigaciones y registro
de auditorías—; DEV-only `tests/` + `docs/`, sin release; Septuagésima quinta serie). El Plan 143 está `Executed` con condición derivada `Closed` (payload
con release pendiente; vaciado del backlog operativo residual: resolución final de
`HD-10`/plan 25, implementación de la verificación de la H13 regla 11 en
`tools/check_taxonomy_coherence.py`, transición CL-8 de `<PLAN-136>:F-1`/`<PLAN-142>:F-2` y
formalización del `C-2 GAP` histórico del plan 116 como `HISTORICAL / NON-ACTIONABLE /
RESOLVED`; `Clase B` para el registro faltante de `PROTOCOL_TAXONOMY.md`, que produce la
versión 11.6.1 PATCH; Septuagésima cuarta serie). El Plan 142 está `Executed` con condición derivada `Closed`
(payload con release pendiente; remisión a la RFC-79: materializa las siete decisiones de
los residuos normativos —`F-14`, `F-17`, `F-16`, `B-8` residual, `F-18`, `F-4` y la
metadata contractual de taxonomía— con `VERSION` 11.6.0 MINOR; Clase A y B;
Septuagésima tercera serie). El Plan 141 está `Executed` con condición derivada `Closed`
(resolución del backlog de decisiones humanas `HD-1`…`HD-12`: ejecución del Plan 137 y
reconciliación de `ROADMAP.md`, decisiones de payload enrutadas por RFC-79, transiciones de
estado de findings y pending decisions, y correcciones de registro en RFC-69/72/74 y en este
INDEX; DEV-only `docs/` + `ROADMAP.md` + `CHANGELOG.md` + `tests/` + `tools/`, sin release;
Septuagésima tercera serie). El Plan 140 está `Executed` con condición derivada `Closed`
(Governance Residual Closure: cierre de `<PLAN-136>:PC-5` como `superseded` y de
`<PLAN-139>:F-1` como `resolved`, determinación de `B-2`/EARS como satisfecho sin
residual, reconciliación del `Roadmap Impact` del Plan 137 a `DEFERRED` con
`<PLAN-137>:PC-1` como pending decision que lo gobierna, clasificación de
`<PLAN-138>:PC-2` como `DEFERRED` no accionable y del `C-2 GAP` del Plan 116 como
histórico/no accionable, con `OPEN / ACTIONABLE = 0`; DEV-only `docs/plans/` +
`CHANGELOG.md` + un test anclado, sin release; Septuagésima segunda serie). El Plan 139 está `Executed` con condición derivada `Closed`
(SAE Governance Boundary Closure: cierre formal de `<PLAN-136>:F-3` como `resolved`,
de `<PLAN-138>:PC-1` como `resuelta` —la regla `Impact classification !=
authorization`— y de `<PLAN-138>:PC-2` como `deferred` —no se introduce ningún
mecanismo autónomo de Scope Expansion—; DEV-only `docs/` + policies `.agents/`, sin
release; Septuagésima primera serie). El Plan 138 está `Executed` con condición derivada `Closed`
(SAE Scope & Authority Hardening: enforcement previo al efecto del Scope/Authority
de Supervised Autonomous Execution a partir del incidente `<PLAN-136>:F-3` — la
determinación de cierre no amplía el Scope autorizado, la escritura fuera de Scope
se detiene **antes** del efecto y el contrato de autorización no se puede reescribir
retroactivamente; DEV-only `runtime/` + `tests/` + policies `.agents/`, sin release;
Septuagésima serie). El Plan 137 está `Executed`
(EARS Structural Validator: ejecutado por el Plan 141 el 2026-09-21 — guarda DEV de
paridad `tools/check_ears_coverage.py` y tres suites, 91 tests, R3/R4/R5 `VALID` sobre el
payload real y R1/R2 `N/A` por ausencia de corpus versionado de `TASK_SPECIFICATION.md`;
**hallazgo: el validador ya existía** — plan 66/RFC-57 — y `B-2` quedó determinado como
**satisfecho sin residual** por el Plan 140; DEV-only `tools/` + `tests/`, sin release;
Sexagésima novena serie).
El Plan 136 está `Executed` con condición derivada `Closed`
(D01 Mechanical Checker: checker DEV del subconjunto mecánico de D01 — estructura
y procedencia resoluble —; DEV-only `tools/` + `tests/`, sin release;
Sexagésima octava serie). El Plan 135 está `Executed` con condición derivada `Closed`
(Supervised Autonomous Execution para el DEV Autonomous Orchestrator; DEV-only,
sin release; Sexagésima séptima serie). El Plan 134 está `Executed` con condición derivada `Closed`
(integridad de la evidencia de cierre: modelo del estado de cierre vs. árbol
material del commit y contrato de C-2; docs-only + tooling DEV, sin release;
Sexagésima sexta serie). El Plan 133 está `Executed` con condición derivada `Closed`
(formalización del Roadmap Impact en el Change Lifecycle DEV y barrido documental
integral; docs-only, sin release; Sexagésima quinta serie). El Plan 132 está `Executed` con condición derivada `Closed`
(actualización del Roadmap al estado real; docs-only, sin release; Sexagésima
cuarta serie). El Plan 131 está `Executed` con condición derivada `Closed`
(implementación mecánica del Placement Contract como resolver determinista; DEV
`runtime/` + `tests/`, sin release; Sexagésima tercera serie). El Plan 130 está
`Executed` con condición derivada `Closed`
(corrección nomenclatural de Plan 129; docs-only, sin release; Sexagésima segunda
serie). El Plan 129 está `Executed` con condición derivada `Closed`
(cierre de `PLAN-129:DEC-1/DEC-2/DEC-3` del Placement Contract; docs-only, sin release;
Sexagésima primera serie). El Plan 128 está `Executed` con condición derivada
`Closed` (materialización del Placement Contract; docs-only, sin release;
Sexagésima serie). El Plan 127 está `Executed` con condición derivada `Closed`
(**diseño cerrado**; `Placement Contract: NOT CREATED` en ese momento; sin
release; Quincuagésima novena serie). El Plan 126 está `Executed` con condición
derivada `Closed` (Quincuagésima octava serie, materialización de las decisiones
C–K; Clase B; release pendiente); el Plan 125 está `Executed` con condición
derivada `Closed` (docs-only, sin release; Quincuagésima séptima serie,
decisiones arquitectónicas de estructura del repositorio); el Plan 124 está `Executed` con condición
derivada `Closed` (docs-only, sin release; Quincuagésima sexta serie, cierre de
hallazgos de arquitectura de `tests/`); el resto de los planes numerados están
`Executed`, y la última serie ejecutada con anterioridad es la Quincuagésima
quinta (Plan 123, 15 sep 2026). El
protocolo publicado es `11.2.0` (`master`/`dist`, tags anotados `11.0.0`,
`11.0.1`, `11.1.0` y `11.2.0`); `dev` lleva los releases en curso
`11.3.0`–`11.5.0` sin publicar (ver `docs/VERSIONING.md` §9, que es el
snapshot vigente de versiones; este header no lo duplica). La **serie de
remediación de la auditoría 2.0.1** está completa: RFC-29…56 `Accepted` (las 23
RFCs de la serie 32…54 se revisaron una por una vía RFC-56, plan 57). El 12 ago
2026 se completó la remediación de la auditoría de documentación
(`docs/AUDITORIA_DOCUMENTACION.md`, fuera del payload): AGENTS.md raíz
operativo, plantillas de plan/RFC + `tools/check_plan_structure.py`, tests
centralizados en `tests/`, batería en CI sin path filters, disolución de `dev/`
(`tools/`, `runtime/`, `docs/` en raíz) y `tools/check_dist_sync.py`. El 14 ago
2026 se agregó el tracker de remediación del sistema
(`docs/working/audits/AUDITORIA_SISTEMA.md`, cerrado el 14 ago 2026 según su
propio status) y se unificó la definición de batería en `docs/VERSIONING.md`
§4.1. El 14–15 ago 2026 se ejecutaron los planes 58–68 (remediación de la
auditoría de sistema, cierre de backlog B-6 y validador obligatorio F1-B,
versiones 3.9.0–3.19.0). Los planes de construcción del protocolo (dominios,
taxonomía, discovery) están implementados; sus versiones históricas viven en
`archive/`.

## Plan 177 — README como puerta de entrada al proyecto (24 oct 2026)

Change DEV **docs-only** (`RFC-56 Class: N/A`, Change Level L1) que reescribe completo el
EntryPoint público del repositorio (`README.md`, naturaleza EntryPoint según
`docs/AGENTS.md:Folder → class map`). El README vigente abría con payload, `dist` y layout del
adoptante; no enunciaba el producto en una frase ni incluía TL;DR, visual, ejemplo o
destinatario; y dedicaba la mayor parte de sus 177 líneas a mecanismos de desarrollo que ya
tienen documento propio. El rediseño aplica el orden **producto → modelo mental → vocabulario
→ ejemplo → distinción Protocol/DEV → límites → adopción → navegación → documentación
profunda**, y explica cada concepto en lenguaje llano antes de nombrarlo. Mantiene la
exactitud de estado: Change Lifecycle y Theoretical Execution se presentan como capacidades
**DEV-only**; la deliberación adversarial como capacidad **opcional y advisory** del payload
(RFC-77, plan 120), con el modelo de jurado declarado como investigación; `Integration
Surface` se declara idea no implementada; Evidence, Authority y Knowledge se explican desde
sus fuentes normativas, sin fusionar los modelos de Protocol y DEV. Se conserva el encabezado
`## Developing in this repository` para que resuelva la cita viva de
`docs/plans/113-decision-making-compass-materialization.md`; todos los enlaces relativos y
anchors resuelven. DEV-only (`README.md` + este Plan + INDEX + `CHANGELOG.md`), sin payload,
sin `VERSION` y sin release (RFC-69); batería canónica, `pytest tests/` y gates C-1/C-2/C-3
en verde.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `177-readme-entry-point-redesign.md` | — (vía plan; DEV-only; RFC-56 N/A) | Executed | **README como puerta de entrada al proyecto.** Reescritura completa del EntryPoint: definición del producto en una frase, TL;DR, problema, diagrama del ciclo de trabajo, conceptos explicados en llano antes de su nombre técnico, ejemplo de un cambio de extremo a extremo, distinción Protocol/DEV/repositorio, límites declarados, adopción y mapas de repositorio y documentación. State honesto de cada mecanismo (Change Lifecycle/TE DEV-only; deliberación adversarial opcional del payload; Integration Surface no implementado). Preserva la cita viva `README.md:Developing in this repository`; enlaces y Mermaid verificados; sin cambios en `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/` ni `.agents/`; sin release. | active |

## Novena serie: remediación de la auditoría de sistema 3.1 (16 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `69-remediacion-bloque-0.md` | — (vía plan, Clase B) | Executed | Bloque 0 de `AUDITORIA_SISTEMA_2026-08-16.md`: conteo de scripts del harness, literal de discovery budget, snapshot del INDEX, `[Unreleased]` del changelog, conteos de auditorías previas y modelo produced_by/consumed_by de contratos de discovery. Versión 3.20.0. | active |
| `70-remediacion-bloque-1.md` | — (vía plan, Clase B) | Executed | Bloque 1 de `AUDITORIA_SISTEMA_2026-08-16.md`: alineación del contrato de verificación con H06 (campo `evidence` opcional), reconciliación de salidas de discovery (workflows + taxonomía, naming de contratos por entrada) y chequeo mecánico bidireccional de salidas de state machines en el checker de coherencia taxonómica. Versión 3.21.0. | active |
| `71-remediacion-bloque-2.md` | — (vía plan, Clase B) | Executed | Bloque 2 de `AUDITORIA_SISTEMA_2026-08-16.md`: validador estructural profile-aware para H04 (camino trivial, F-A), declaración del gate trivial en H00 e INDEX (F-B) y cobertura bidireccional de gates en el checker de coherencia taxonómica. Versión 3.22.0. | active |
| `72-remediacion-bloque-3-parte-1.md` | — (vía plan, Clase B) | Executed | Bloque 3 parte 1 de `AUDITORIA_SISTEMA_2026-08-16.md`: evidencia determinista de tests en el validador H06, registro de desviaciones documentadas en `HARNESS_REPORT.md`/`harness/INDEX.md` con validación en el checker de sesión, y tool dev-only de auditoría post-hoc de gates. Versión 3.23.0. | active |
| `73-remediacion-bloque-3-parte-2.md` | RFC-59 | Executed | Bloque 3 parte 2 de `AUDITORIA_SISTEMA_2026-08-16.md` (ítems 13/14/16): recovery context con derivación/registro de variables de las tablas, ranking de destinos múltiples de recovery y procedimiento de reanudación de sesión. Versión 3.24.0. | active |
| `74-remediacion-bloque-4.md` | RFC-60 | Executed | Bloque 4 de `AUDITORIA_SISTEMA_2026-08-16.md` (ítems 19/20/21): contabilidad mecánica del Context Budget (estado measured + tool de medición), modelo de confianza de métricas (clases Derived/Recorded/Verified + `--audit` del agregador) y endurecimiento de la superficie de bypass del hook (deny de Write/Edit sin target). Versión 3.25.0. | active |

## Décima serie: consentimiento y visibilidad del discovery (24 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `75-discovery-consent-visibility.md` | RFC-61 | Executed | Gate de consentimiento del discovery (`discovery_require_consent`), scope `lite`, sección "Qué aprendimos" en el cierre de tarea y skill `/discovery`. Versión 3.26.0. | active |

## Undécima serie: decisiones arquitectónicas post-auditoría (25 ago 2026)

RFCs de modelo conceptual derivadas de `ARCHITECTURAL_DECISION_MODEL.md` (basado en
`ARCHITECTURAL_PROBLEM_MODEL.md`). RFC-62 `Accepted` (plan 76); RFC-63
`Accepted` (plan 77); RFC-64 tiene plan de ejecución redactado (plan 78, gated
a `Accepted` — Clase A de RFC-56); RFC-65 `Accepted` (plan 79); RFC-66
`Accepted` (plan 80); RFC-67 `Accepted` (plan 81); ninguna RFC habilita
modificar `protocol/.agents/` hasta su plan de ejecución con la vía de
autorización completa.

| RFC | Status | Descripción | Vigencia |
|---|---|---|---|
| `rfc/62-guarantee-model-and-enforcement-boundaries.md` | Accepted (plan 76) | Garantías clasificadas y matriz de enforcement (D0, D11). | active |
| `rfc/63-state-and-artifact-lifecycle-model.md` | Accepted (plan 77) | Dimensiones de estado, lifecycle de artefactos y semántica de COMPLETED (D1, D2, D3). | active |
| `rfc/64-execution-record-model.md` | Proposal (plan 78) | Identidad, registros, temporalidad y observabilidad de la ejecución (D5, D6, D7, D10). | active |
| `rfc/65-evidence-and-verification-model.md` | Accepted (plan 79) | Clases de evidencia y regla VERIFIED (D4, D12). | active |
| `rfc/66-authorization-and-capability-model.md` | Accepted (plan 80) | Frontera de efectos y bloque `effects` (D8, D11). | active |
| `rfc/67-knowledge-lifecycle-model.md` | Accepted (plan 81) | Lifecycle mínimo de conocimiento (D9). | active |

## Duodécima serie: modelo de garantías y fronteras de enforcement (25 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `76-guarantee-model-enforcement-boundaries.md` | RFC-62 | Executed | Catálogo cerrado de garantías con cinco clases, matriz de enforcement por capa en el payload y la guía de adopción, regla operacional de claims (evidencia o atestación/inferencia), reemplazo de "zero hallucinations" como garantía técnica y celdas External en los checkers dev. Versión 4.0.0 (MAJOR). | active |

## Decimotercera serie: modelo de estado y lifecycle de artefactos (25 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `77-state-artifact-lifecycle-model.md` | RFC-63 | Executed | Dimensiones de estado con entidad propia (Task State, Gate State, Artifact Lifecycle) y cuatro derivadas (Execution, Verification, Approval, Plan), lifecycle de artefactos derivado del registro de gates (nunca escrito a mano), semántica de COMPLETED relativa al alcance confirmado con `Deferred Items`, y resolución del review gate como Gate State sobre REVIEW_REPORT. Versión 5.0.0 (MAJOR). | active |

## Decimocuarta serie: modelo de registro de ejecución (25 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `78-execution-record-model.md` | RFC-64 | Executed | Identidad de ejecución por composición (`execution_id = (session_id, iteration)`), roles disjuntos de los cuatro registros, alcance de `state.json` (gates de transición H00–H07, H11 + status terminal), semántica temporal UTC con `clock` declarado, event keys en ENTRY/METRIC (`iteration`/`seq`), reconciliación bidireccional y de timestamps en `--audit`, y registro obligatorio de `context_budget` por delegación con budget. RFC-64 `Accepted` (plan 103, 2026-09-03; Clase A, RFC-56). Rebase 2026-09-04 contra el estado 10.3.0 (versión objetivo 11.0.0, guard `>= 11.0.0` + fixtures legacy 7.0.0–10.3.0, METRICS schema 1.2.0 → 2.0.0, MIGRATION §13, integración de la declaración de `state.json`). **Ejecución (2026-09-04):** implementado en `dev` — commits C1 `d94f33a` (contenido: contratos schema 2.0.0, Execution records en `harness/INDEX.md`, runner con `TRANSITION_TRIGGERS`/UTC-`Z`, pairing de `context_budget`, audit `(iteration, trigger)` + tolerancia 60 s, guard `>= 11.0.0`, MIGRATION §13, VERSION/CHANGELOG `[11.0.0]`) y C2 (registro/cierre); pytest `445 passed`; checkers canónicos PASS; C-1/C-2/C-3 sin ANOMALY; Validation Anchor V1 (T1 `3e016ed…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (version-producing, release pendiente); `<PLAN-78>:F-1` resuelto vía `<PLAN-78>:C-1` (ancla semántica del runtime); sin push, sin tag. | active |

## Decimoquinta serie: modelo de evidencia y verificación (25 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `79-evidence-and-verification-model.md` | RFC-65 | Executed | Clases de evidencia mínimas (`observation`/`measurement`/`attestation`/`assertion`/`reference`), bloques `[[evidence]]` con `class`/`claim_id`/`ref` en VERIFICATION_REPORT y en los ENTRY de HARNESS_REPORT, reglas de suficiencia por ítem `[gate]`/`[agent]`, invariante VERIFIED (evidencia distinta de atestación o término ATESTADO) y detección de atestaciones sin marca en `audit_gates.py` y el validador estructural H06. Versión 7.0.0 (MAJOR). | active |

## Decimosexta serie: modelo de autorización y capacidades (25 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `80-authorization-and-capability-model.md` | RFC-66 | Executed | Distinción formal de Capability/Permission/Authorization/Execution/Effect, frontera por defecto (red/HTTP, git remoto, instalaciones, cambios destructivos y escrituras fuera del proyecto requieren autorización), bloque `effects` en TASK_SPECIFICATION con `authorized_by`/`evidence_ref`/`status`, checks de autorización en H01/H04/H05, registro de efectos ejecutados en EXECUTION_SUMMARY, estados AUTHORIZED/UNAUTHORIZED/AUTHORIZATION_UNDETERMINED sin inferir UNAUTHORIZED por ausencia de registro. Versión 8.0.0 (MAJOR). | active |

## Decimoséptima serie: modelo de lifecycle de conocimiento (25 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `81-knowledge-lifecycle-model.md` | RFC-67 | Executed | Tipos de conocimiento (`snapshot`/`claim`/`lesson`), frescura por claim con proveniencia resoluble, invalidación post-ejecución (`invalidated_facts` en EXECUTION_SUMMARY) con revalidación scoped por pipeline, lessons del cierre con `session_id`/`protocol_version`/evidencia, y `kind`/`path` en KB_RECOMMENDATION. Versión 9.0.0 (MAJOR). | active |

## Decimoctava serie: workflow de evolución arquitectónica (25 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `82-architecture-evolution-workflow.md` | RFC-68 | Executed | Fase 1 de la RFC-68: capability de evolución arquitectónica en dos niveles, módulo `orchestrators/architecture/` (state machine + contratos PROJECT_REGISTRY/SESSION_REGISTRY/EVIDENCE_SNAPSHOT/EVIDENCE_SET/ARCHITECTURAL_CHANGE_SET/ARCHITECTURE_MANIFEST), checker de trazabilidad, Import Workspace `sessions/` gitignored y backfill de refs. Versión 9.1.0 (MINOR). | active |

## Decimonovena serie: gobernanza ADR del repo fuente (27 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `83-adr-governance-backfill.md` | RFC-69 | Executed | Plan B de la RFC-69: `docs/adr/` materializado con 14 ADRs individuales (ADR-01…ADR-14 ↔ D0–D13 preservadas como identidad histórica), matriz `D# ↔ ADR ↔ RFC ↔ plan` en `docs/adr/INDEX.md`, template `_TEMPLATE.md`, ciclo de status ADR en `docs/CONVENTIONS.md` y cobertura de `docs/adr/` en los checkers de estructura y citas. Cambio docs-only: ítem en `[Unreleased]`, sin `VERSION` bump ni tag (RFC-69). | active |

## Vigésima serie: eliminación de artefactos de contexto manuales en favor de la KB de discovery (28 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `84-remove-project-context-artifacts.md` | RFC-70 | Executed | Elimina `project-map.md` y `technical-analysis.md` como artefactos del protocolo y `PROJECT_ARTIFACTS.md` por completo (incluidas las plantillas de dominio): su contenido ya vive en la KB de discovery; consumidores y adopción realineados. Versión 10.0.0 (MAJOR). | active |

## Vigésima primera serie: corrección de la guía de adopción (29 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `85-adopcion-sin-subtree.md` | — (vía plan) | Executed | Reemplaza el flujo `git subtree --prefix=.` de `docs/ADOPTION.md` (incompatible con un `dist` que solo trae `.agents/` + `AGENTS.md`) por la copia del payload desde `dist` vía git (fetch + `git checkout FETCH_HEAD`) o sin git, con manejo de archivos eliminados entre versiones; `check_plan_citations.py` exime citas históricas a artefactos eliminados (restaura la batería tras 10.0.0). Cambio docs-only: ítem en `[Unreleased]`, sin `VERSION` bump ni tag (RFC-69). | active |

## Vigésima segunda serie: modelo de context persistence y cacheability (29 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `86-context-persistence-cacheability-model.md` | RFC-71 | Executed | Formaliza la RFC-71 como modelo semántico de Context Persistence y Cacheability (vocabulario, segmentos Core/Project/Worker, identidades compuestas, ortogonalidad de atributos, invalidación por identidad, invariantes I-001…I-012): RFC-71 pasa a `Accepted`, con Amendment Log, INDEX de RFCs y changelog. Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); RFCs 72–74 y la implementación quedan fuera. **Resolución (2026-08-29):** aceptación docs-only conservada como histórico; la implementación normativa de la RFC-71 es el plan 88 (`88-rfc71-implementation.md`). | active |
| `87-provider-prompt-cache-capability.md` | RFC-72 | Executed | Formaliza la RFC-72 como modelo de la capacidad de Provider Prompt Cache (frontera `SemanticContextIdentity`/`MaterializationIdentity`/`ProviderCacheReference`, dimensiones de `MaterializationIdentity`, Canonical Materialization e I-MAT-001, Ordering Contract con orden OPEN/DEFERRED, Stable Prefix, capacidad abstracta del provider, Provider Adapter Boundary, hit/miss, invalidación en tres dominios, admisión e invariantes I-MAT-001…I-MAT-012): RFC-72 pasa a `Accepted`, con Amendment Log, INDEX de RFCs y changelog. Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); RFCs 73–74 y la implementación quedan fuera. **Resolución (2026-08-29):** sin operación aplicable según el ciclo de status de planes (`docs/VERSIONING.md:7. Estados de planes y RFCs`): no existe `delete`/`cancel` y `Superseded` exige un plan reemplazante que no existe; se conserva `Aprobado para ejecución` con su dependencia (plan 86) válida. **Ejecución (2026-08-31):** RFC-72 pasa a `Accepted (plan 87, 2026-08-29)` con entrada en su Amendment Log, INDEX de RFCs y changelog; plan marcado `Executed`. Sin cambios en `protocol/.agents/`; RFCs 73–74 intactas en `Proposal`. | active |

## Vigésima tercera serie: implementación normativa de RFC-71 (29 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `88-rfc71-implementation.md` | RFC-71 | Executed | Materializa en `protocol/.agents/` la parte normativa de la RFC-71 sobre standards existentes: clasificación estable/dinámico, segmentos Core/Project/Worker, identidades compuestas (`SegmentContentIdentity`/`SegmentIdentity`/`SemanticContextIdentity`), scope, aislamiento semántico, separación correctness/lifecycle/almacenamiento y frontera de cache en `CONTEXT.md`, `KNOWLEDGE_LIFECYCLE.md`, `PROTOCOL_BOUNDARIES.md` y `BUDGET_MATERIALIZATION.md`; el resto de la RFC-71 permanece RFC-only y las RFCs 72–74 (Proposal) quedan fuera. Clase A (RFC-71 `Accepted`); versión 10.1.0 (MINOR). | active |

## Vigésima cuarta serie: implementation plans de las RFCs 72–74 (30 ago 2026)

Planes de implementación de las RFCs 72–74 generados sobre el estado real del
repo (RFC-71 `Accepted`, plan 88 `Executed`, protocolo 10.1.0). Ninguno se
ejecuta en esta iteración: los tres están `Aprobado para ejecución` con gate
de gobernanza — RFC-72/73/74 permanecen `Proposal` (RFC-56: una RFC en
`Proposal` no habilita tocar el payload). RFC-72 tiene vía de aceptación
registrada (plan 87, `Aprobado para ejecución`); las vías de aceptación de
RFC-73 y RFC-74 quedan registradas en la Vigésima quinta serie (planes 92/93,
`Aprobado para ejecución`).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `89-rfc72-provider-prompt-cache-implementation.md` | RFC-72 | Executed | Implementa la capacidad de Provider Prompt Cache en el runtime de referencia: `MaterializationIdentity` (reglas condicionales), Canonical Materialization con I-MAT-001 verificable, Ordering Contract v1 del runtime (orden de facto de los renderers; no resuelve el OPEN/DEFERRED normativo), Stable Prefix, capacidad abstracta del provider + Provider Adapter Boundary, `ProviderCacheReference` opaca, flujo lookup/hit/miss/request/reference update con invalidación en tres dominios y admisión sin umbrales. Sin cambios en `protocol/.agents/` (runtime de referencia): sin `VERSION` bump ni changelog de protocolo; gate de gobernanza = RFC-72 `Accepted` (plan 87). **Ejecución (2026-08-31):** U1–U6 completados (identity, canonical, provider_cache, cache_coordinator, README, tests I-MAT-001…I-MAT-012); gate RFC-72 `Accepted` cumplido (plan 87 `Executed`); batería canónica en verde y pytest 279 passed; `protocol/.agents/`, VERSION y CHANGELOG intactos. | active |
| `90-rfc73-project-persistence-implementation.md` | RFC-73 | Executed | Implementa la persistence semántica de proyecto: Project Segment derivado sobre la KB existente (namespace = `ProjectIdentity` sin identidad nueva; `SegmentContentIdentity`/`SegmentIdentity(project)`), reuse eligibility (`FRESH`/`STALE`/`UNKNOWN`) con non-equivalencia de los hashes de discovery, store derivado `.project/knowledge/project_segment.json` (filesystem, atómico, rebuildable, no autoritativo) y regla aditiva en `PROTOCOL_BOUNDARIES.md`. Clase A; versión 10.2.0 (MINOR). **Blocker arquitectónico resuelto (2026-08-31):** `project_namespace` = `PROJECT_REGISTRY.project_id` (única identidad lógica existente); sin Project ID ⇒ sin store (KB persiste como artifacts). **Ejecución (2026-08-31):** U1–U6 completados (project_segment, project_store, PROTOCOL_BOUNDARIES, standards/INDEX, 37 tests, gobernanza); gate RFC-73 `Accepted` cumplido (plan 92 `Executed`); batería canónica en verde y pytest 316 passed; `protocol/.agents/VERSION` → 10.2.0 (MINOR) y changelog `[10.2.0]`; commit atómico en `dev` (`feat(runtime): implement project context persistence (plan 90, RFC-73)`); Discovery persistence reutilizada (mecanismo existente, sin cambios); revalidation = pipeline preexistente + cómputo de reuse eligibility; sin integración automática con Context Composition. Commit atómico: `bf63b21` — `feat(runtime): implement project context persistence (plan 90, RFC-73)` (registrado por corrección del Plan 141, `HD-12 F-6`/`F-8`). | active |
| `91-rfc74-cache-observability-implementation.md` | RFC-74 | Executed | Implementa la medición y economía del cache: eventos `reuse_event`/`provider_cache_event` en `METRICS.md` (schema 1.2.0, aditivo), catálogo `### Reuse and cache` + invariantes I-ECO en `PROTOCOL_METRICS.md` (sin thresholds), agregación en `tools/aggregate_metrics.py` con derivación de Discovery reuse y productores de los planes 89/90 expuestos como metadata/estado con seam host/orchestrator documentado (U1–U5; sin writer de referencia). Clase A (RFC-74 `Accepted`, plan 93); versión 10.3.0 (MINOR). **Ejecución (2026-08-31):** U1–U5 completados (METRICS.md 1.2.0 con `reuse_event`/`provider_cache_event`; catálogo `Reuse and cache` + economía I-ECO; agregador con agregación por capa y sin doble conteo; derivación de Discovery reuse; metadata/estado de productores consumido sin duplicación); batería canónica en verde y pytest 331 passed (basetemp fresco por ACL de `pytest-of-rolda` en sandbox Windows); `protocol/.agents/VERSION` → 10.3.0 (MINOR) y changelog `[10.3.0]`; RFC-74 con Amendment Log e "Impacto en el protocolo" corregidos; sin pricing, thresholds ni telemetry backend. Commit atómico: `9dd8703` — `feat(protocol): implement RFC-74 observability and economics (plan 91, RFC-74)` (registrado por corrección del Plan 141, `HD-12 F-8`; el plan 91 registra **331 passed** en su `Nota de ejecución`, no 316). | active |

## Vigésima quinta serie: aceptación de las RFCs 73–74 (30 ago 2026)

Planes de aceptación/formalización docs-only de las RFCs 73–74, siguiendo el
patrón normativo de los planes 86/87 (RFC-71/72). No implementan ninguna
capacidad: solo `Proposal → Accepted` (status, Amendment Log, INDEX de RFCs,
changelog bajo `[Unreleased]` y registro del plan). Sin `VERSION` bump ni tag
(RFC-69). No se ejecutan en esta iteración; dejan los gates de los planes
90/91 resueltos en cuanto a vía de aceptación.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `92-rfc73-acceptance.md` | RFC-73 | Executed | Formaliza la RFC-73 (Project & Discovery Context Persistence) como modelo de persistence del contexto de proyecto y Discovery (Project Knowledge, isolation por `ProjectIdentity`, hashes de discovery ≠ `SegmentContentIdentity`, frescura/revalidación, invariantes I-PROJ-001…I-PROJ-012): RFC-73 pasa a `Accepted`, con Amendment Log, INDEX de RFCs y changelog. Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); la implementación queda en el plan 90 (gated a RFC-73 `Accepted`). **Ejecución (2026-08-31):** RFC-73 pasa a `Accepted (plan 92, 2026-08-30)` con entrada en su Amendment Log, INDEX de RFCs y changelog; plan marcado `Executed`. Sin cambios en `protocol/.agents/`, `runtime/` ni `tests/`; RFCs 71/72/74 intactas; plan 90 seguía sin ejecutar en ese momento (gate de RFC-73 `Accepted` cumplido después) y se ejecutó con el commit `bf63b21` (aclarado por el Plan 141, `HD-12 F-6`). | active |
| `93-rfc74-acceptance.md` | RFC-74 | Executed | Formaliza la RFC-74 (Cache Observability & Economics) como modelo de medición y economía del cache (capas de economía, avoided work, eventos de reuse, taxonomía de misses, invariantes I-ECO-001…I-ECO-006): RFC-74 pasa a `Accepted`, con Amendment Log, INDEX de RFCs y changelog. Depende de RFCs 71–73 `Accepted` (planes 86/87/92). Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); la implementación queda en el plan 91 (`Aprobado para ejecución`, NO ejecutado). **Ejecución (2026-08-31):** RFC-74 pasa a `Accepted (plan 93, 2026-08-31)` con entrada en su Amendment Log, INDEX de RFCs y changelog; plan marcado `Executed`. Sin cambios en `protocol/.agents/`, `runtime/`, `tests/` ni `tools/`; RFCs 71–73 intactas; plan 91 seguía sin ejecutar en ese momento (gate de RFC-74 cumplido) y se ejecutó con el commit `9dd8703` (aclarado por el Plan 141, `HD-12 F-6`). | active |

## Vigésima sexta serie: Master Action Plan del Change Lifecycle DEV (01 sep 2026)

Mapa maestro del Change Lifecycle de ARgentOS DEV derivado de RFC-75
(`Accepted`, 2026-09-01) y de los ADR-15/16. **No es un Plan de implementación
ejecutable**: define la estrategia incremental sobre los **seis incrementos
conceptuales de RFC-75** (0–5), agrupados en **unidades de implementación
iniciales** (A: 0; B: 1+3 en batch operacional; C: 2; D: 4), con el Incremento 5
como track futuro deferido; es la base de derivación para los planes de
implementación futuros (95+). Este MAP es docs-only (sin cambios en
`protocol/.agents/`, `runtime/`, `tests/` ni `tools/`, sin `VERSION` bump ni
tag, RFC-69); los incrementos derivados no lo son todos (el Incremento 4
incorpora tooling y tests).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `94-change-lifecycle-master-action-plan.md` | RFC-75 | Executed | Master Action Plan del Change Lifecycle de ARgentOS DEV: estado real contrastado con git/checkers; modelo de lifecycle y condiciones derivadas (Verified/Executed/Committed/Closed/Promoted/Released); frontera DEV vs Protocol; inventario del workflow actual; mapeo RFC-75 → mecanismos; modelo de autoridad (ADR-16); economía de Change Levels L0–L3; decisión de no-state-machine; estrategias de skills/artifacts/policies/checkers/Git/telemetría; continuidad entre agentes (handoff fuera de alcance); roadmap incremental con seis incrementos conceptuales (0–5) agrupados en unidades de implementación A–D (1+3 en batch operacional) y "usable at every phase"; dogfooding; grafo de dependencias; riesgos; ADR candidates; deuda no bloqueante; validación (incluye política de "batería verde" §24.1); criterios de salida; retrospectiva RFC-71..74; preguntas abiertas; auditoría adversarial; veredicto READY FOR IMPLEMENTATION PLANNING. Entregable producido, corregido y verificado (checkers en verde; fallo de pytest preexistente como desviación documentada) sin ejecutar incrementos; `Executed` sin `Closed` (checkpoint/commit pendiente del mantenedor). | active |

## Vigésima séptima serie: Change Lifecycle DEV — Unidad A / Incremento 0 (02 sep 2026)

Primer Implementation Plan ejecutable derivado del Master Action Plan 94.
Implementa exclusivamente la **Unidad A = Incremento conceptual 0** de RFC-75:
semántica y vocabulario del Change Lifecycle DEV (condiciones derivadas
Verified/Executed/Committed/Closed/Promoted/Released), modelo de Change Levels
(ejes + `max` + L0 provisional, independiente de la clase RFC-56), frontera
DEV/Protocol, serie como identidad derivada y observability schema baseline de
las cuatro métricas permanentes (sin medición operacional ni machinery nueva).
Cambio docs-only sobre `docs/CONVENTIONS.md`, `docs/VERSIONING.md`,
`AGENTS.md`, `docs/AGENTS.md`, `CHANGELOG.md:[Unreleased]` y el registro del
plan en este INDEX; sin `VERSION` bump ni tag (RFC-69). No implementa anchors,
checkpoints, findings, pending, checkers ni series registries (Incrementos 1–5
quedan para las unidades B/C/D y el track deferido). Plan redactado, registrado
y ejecutado (2026-09-02) con verificación de checkers en verde y pytest
`339 passed, 1 failed` (fallo temporal preexistente como desviación
documentada); `Executed` sin `Closed` (OPEN-2 resuelto el 2026-09-02 por
decisión explícita del mantenedor — corrección independiente del test, commit
`865e3ad`, pytest `340 passed, 0 failed`, checkers PASS — sin aceptar
desviación vigente; cierre formal pendiente del mecanismo de checkpoint del
Incremento 3).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `95-change-lifecycle-unit-a-increment-0.md` | RFC-75 | Executed | Plan de implementación de la Unidad A (Incremento 0) del Change Lifecycle DEV: escribe en las fuentes de verdad la semántica del lifecycle (condiciones derivadas y vocabulario Verified/Executed/Committed/Closed/Promoted/Released/Abandoned), el modelo de Change Levels (ejes + `Level = max(...)` + L0 provisional, independiente de la clase RFC-56), la frontera DEV/Protocol, la serie como identidad derivada y el observability schema baseline de las cuatro métricas permanentes de RFC-75 (validation anchor coverage, finding lineage coverage, stale validation rate, Git closure anomalies) sin fingir medición; preserva la regla transversal target semantics vs operationalización (VC-1/GC-1/LC-1/PC-1 exigibles solo desde sus incrementos 1/3/2). Cambio docs-only: `docs/CONVENTIONS.md` (subsecciones de alcance DEV-only, Change Levels y regla transversal), `docs/VERSIONING.md` (§7 semántica de condiciones derivadas + §11 métricas), `AGENTS.md` raíz (`Task lifecycle`, frontera en `Do NOT`), `docs/AGENTS.md` (`Identity`: serie derivada), ítem `(plan 95, RFC-75)` en `CHANGELOG.md:[Unreleased]`; sin `VERSION` bump ni tag (RFC-69); sin campos de template, checkers, anchors, checkpoints, findings, pending, skills ni state machines. Derivado de RFC-75 `Accepted` y ADR-15/16 (plan 94 como mapa maestro, Unidad A); veredicto PLAN 95 READY FOR IMPLEMENTATION. **Ejecución (2026-09-02):** U1–U5 aplicados y verificados (checkers en verde; pytest `339 passed, 1 failed` con el fallo temporal preexistente reportado como desviación documentada, sin modificarlo); status `Executed` sin `Closed` (mecanismo de checkpoint del Incremento 3; OPEN-2 resuelto el 2026-09-02 por decisión explícita del mantenedor vía la corrección independiente del test — commit `865e3ad`, pytest `340 passed, 0 failed` — sin aceptar desviación vigente; cierre formal pendiente del mecanismo de checkpoint del Incremento 3). Sin cambios en `protocol/`, `runtime/`, `tests/`, `tools/`, VERSION, ADRs ni RFCs. | active |

## Vigésima octava serie: Change Lifecycle DEV — Unidad B / Incrementos 1+3 (02 sep 2026)

Segundo Implementation Plan ejecutable derivado del Master Action Plan 94.
Implementa la **Unidad B = Incremento conceptual 1 + Incremento conceptual 3**
de RFC-75 como una única unidad de ejecución planificada (el Incremento 3 no
se renumera ni se absorbe dentro del 1): Validation Anchors operativos (VC-1)
con campos de anchor y algoritmo de Scoped Content Identity v1 (tree id +
delta identity por primitivas git), intake fallback con `Change Level` en el
primer artifact (L0 provisional y triggers), serie como identidad derivada
(declaración `Serie:` + relaciones verificables, sin registry) y Git
closure/checkpoint operativo (GC-1) con registro de checkpoint, consistencia
anchor↔checkpoint antes de `Closed`, multi-commit/multi-RFC y docs-only sin
release. Cambio docs-only (ejecución futura) sobre
`docs/plans/_TEMPLATE.md`, `docs/rfc/_TEMPLATE.md`, `docs/CONVENTIONS.md`,
`docs/VERSIONING.md`, `AGENTS.md`, `docs/AGENTS.md`, Amendment Log de RFC-75,
`CHANGELOG.md:[Unreleased]` e INDEX; sin `VERSION` bump ni tag (RFC-69); sin
checkers, tests, skills, entidades, registries ni state machines (Incrementos
2/4/5 quedan diferidos). Plan redactado y registrado (2026-09-02) con Change
Level L2 (prospectivo, dogfooding) y veredicto PLAN 96 READY FOR
IMPLEMENTATION. **Ejecución (2026-09-02):** implementado sobre `dev`
(E3–E14 + registros de cierre); el propio plan produjo y verificó el primer
Validation Anchor (state identity `b8add7d7…`; delta `a818ed4f…`) y el primer
Checkpoint (consistencia C1 `9e4192f` ↔ anchor PASS; revalidación V2 sobre C2
antes de `Closed`); status `Executed`; condición derivada `Closed` (docs-only,
sin release).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `96-change-lifecycle-unit-b-increments-1-3.md` | RFC-75 | Executed | Plan de implementación de la Unidad B (Incrementos 1+3) del Change Lifecycle DEV: materializa VC-1 (Validation Anchors con campos de anchor — declared scope, command-set, effective inputs, observed dependencies, environmental factors, Scoped Content Identity v1 por `git write-tree`/`ls-files`/`hash-object` — en template de Plan y Amendment Log de RFC) y GC-1 (Git closure/checkpoint: registro de la relación closure↔estado Git con commits de cierre, tree id, consistencia anchor↔checkpoint y condición derivada `Closed`; `Committed ≠ Closed ≠ Released`; multi-commit/multi-RFC; docs-only sin release); intake fallback con `Change Level` en el primer artifact (L0 provisional, triggers, downgrade justificado) y serie como identidad derivada (declaración + relaciones; sin registry). Cambio docs-only: templates (`_TEMPLATE.md` de planes y RFCs), `docs/CONVENTIONS.md` (reglas operativas), `docs/VERSIONING.md` (§7/§10/§11), `AGENTS.md`, `docs/AGENTS.md`, Amendment Log de RFC-75, ítem `(plan 96, RFC-75)` en `CHANGELOG.md:[Unreleased]` y espejo en este INDEX; sin `VERSION` bump ni tag (RFC-69); sin checkers/tests/skills/entidades/registries/state machines (Incrementos 2/4/5 diferidos). Derivado de RFC-75 `Accepted` y ADR-15/16 (plan 94 Unidad B; plan 95 Incremento 0); Change Level L2 (coordinación 1, scope 1, impacto arquitectónico 1, release 1, duración 2). **Ejecución (2026-09-02):** implementación E3–E14 verificada (checkers PASS; pytest `340 passed, 0 failed`); commits C1 `9e4192f` (contenido) y C2 (registros de cierre): primer Validation Anchor real (state identity `b8add7d74a41b907627b7faa4f10909af599ef2b`; delta `a818ed4ffe683faad9cde368f4a0718112f40f62983c63d1e459dcdd947a0d14`) y primer Checkpoint (consistencia C1↔anchor PASS; revalidación V2 sobre C2 antes de `Closed`); status `Executed`; condición derivada `Closed` (docs-only, sin release). Sin cambios en `protocol/`, `runtime/`, `tests/`, `tools/`, VERSION, ADR-15/16, RFC-56/69 ni planes 94/95. | active |

## Vigésima novena serie: Change Lifecycle DEV — Unidad C / Incremento 2 (02 sep 2026)

Tercer Implementation Plan ejecutable derivado del Master Action Plan 94.
Operacionaliza para artifacts nuevos la **Unidad C = Incremento conceptual 2**
de RFC-75: findings con refs calificadas `<artifact>:F-<n>` y estados,
corrections con registro de provenance `C-<n>` y alcance de revalidación,
lineage formal `F-n`/`C-n` (namespace por artifact, sin registries), modelo de
revalidación A1/A2 de la Decisión B, pending decisions per-artifact (PC-1),
condiciones no resueltas, lineage post-close y estructuras documentales
(CONVENTIONS, templates, VERSIONING, AGENTS.md, Amendment Log de RFC-75,
INDEX, changelog) que el Incremento 4 consumirá como datos. Cambio
exclusivamente documental (sin `protocol/`, `runtime/`, `tools/`, `tests/`,
VERSION ni `dist/`; sin `VERSION` bump ni tag, RFC-69); no implementa el
Incremento 4 ni crea el Plan 98; no toca `docs/adr/*` ni los Planes 94/95/96.
Derivado de RFC-75 `Accepted` y ADR-15/16 (plan 94 Unidad C; plan 95 Incremento
0; plan 96 Incrementos 1+3, `Closed`; Decisión B `fc52c88`); Change Level L2.
Plan redactado a partir del Planning Report v2 aprobado (2026-09-02),
creado y registrado el 2026-09-02 (Status inicial `Aprobado para ejecución`,
sin implementar) y **ejecutado y cerrado el 2026-09-02**: Status `Executed`;
condición derivada `Closed` (docs-only, sin release) con Validation Anchor
(V1 sobre C1) y Checkpoint (revalidación V2 sobre C2) registrados; commits C1
`236735b` (contenido) y C2 (registros de cierre) en `dev`; pytest
`340 passed, 0 failed`; sin `VERSION` bump ni tag.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `97-change-lifecycle-unit-c-increment-2.md` | RFC-75 | Executed | Plan de implementación de la Unidad C (Incremento 2) del Change Lifecycle DEV: operacionaliza para artifacts nuevos findings (`<artifact>:F-<n>`, estados open/partially-resolved/resolved/deferred/superseded y reapertura por finding nuevo o metadata), corrections como registro de provenance (`C-<n>` ≠ fuente normativa; CL-6/CL-7), lineage formal por artifact sin registries globales, revalidación integrada a A1/A2 (A2 referencia A1 sin mutarlo; Decisión B `fc52c88`), pending per-artifact con metadata PC-1 (blocking/no-blocking, owner, escalación, resolución, evidencia, efecto downstream, ADR-worthiness), condiciones no resueltas, post-close por referencia (RFC-75 Mec. 12) y formatos deterministas que consumirá el Incremento 4. Cambio docs-only: `docs/CONVENTIONS.md` (subsecciones operativas LC-1/PC-1 y mapa de aplicabilidad), templates de Plan y RFC, `docs/VERSIONING.md` (§10 DoD + §11 campos de la métrica finding lineage coverage), `AGENTS.md` raíz, Amendment Log de RFC-75, ítem `(plan 97, RFC-75)` en `CHANGELOG.md:[Unreleased]` y espejo final en este INDEX; sin `VERSION` bump ni tag (RFC-69); sin checkers/tests/entidades/registries/state machines (Incrementos 4/5 diferidos). Derivado de RFC-75 `Accepted` y ADR-15/16 (plan 94 Unidad C; plan 95; plan 96 `Closed`); Change Level L2. **Creación (2026-09-02):** artifact creado y registrado sin ejecutar (Status `Aprobado para ejecución`, PLANNED / OPEN). **Ejecución (2026-09-02):** P2–P8 aplicados y verificados — CONVENTIONS, templates de Plan/RFC, VERSIONING §10/§11, AGENTS.md, Amendment Log de RFC-75, changelog e INDEX — checkers PASS (warnings esperados de `dev`); pytest `340 passed, 0 failed`; commits C1 `236735b` (contenido) y C2 (registros de cierre): Validation Anchor V1 (state identity T1 `0df8920c…`; delta `5d5ca643…`) y Checkpoint con revalidación V2 sobre C2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release). Dogfooding del propio plan: `No findings detected / N/A`; pending no-bloqueantes OQ-1…OQ-5 (owner mantenedor) documentados en §26 del plan. Sin cambios en `protocol/`, `runtime/`, `tests/`, `tools/`, VERSION, ADRs, RFC-46/56/69, `docs/AGENTS.md` ni planes 94/95/96. | active |

## Trigésima serie: Change Lifecycle DEV — Unidad D / Incremento 4 (02 sep 2026)

Cuarto Implementation Plan ejecutable derivado del Master Action Plan 94.
Implementa la **Unidad D = Incremento conceptual 4** de RFC-75 con el mínimo
viable demostrado por el corpus actual: automatización segura determinista y
factual (advisory) de **C-1 — lifecycle anchor validation** y **C-2 —
lifecycle checkpoint validation**, DEV-only sobre `tools/` + `tests/` (sin
incorporación inicial a la batería canónica, sin CI, sin F-n/C-n/stale/series/
métricas, sin registries, sin entidades, sin estado machine global). Consume
los campos de anchor/checkpoint v1 materializados por las unidades B/C
(planes 96/97) y respeta tree identity ≠ commit SHA, no-reachability desde
`dev`, GAP ≠ invalidación y la frontera DEV/Protocol. Plan creado y registrado
el 2026-09-02 (Status inicial `Aprobado para ejecución`, PLANNED / OPEN) y
**ejecutado y cerrado el 2026-09-02**: C-1 (`tools/check_lifecycle_anchor.py`
+ `tests/test_check_lifecycle_anchor.py`) y C-2
(`tools/check_lifecycle_checkpoint.py` +
`tests/test_check_lifecycle_checkpoint.py`) implementados con commits C1
`669a576` y C2 `9b5b8a1` en `dev`; pytest `380 passed, 0 failed`; checkers
canónicos PASS (warnings esperados de `dev`); dogfooding sobre planes 96/97/98
sin falsos positivos; Validation Anchor (V1 sobre C1) y Checkpoint
(revalidación V2 sobre el estado final antes del cierre) registrados; Status
`Executed`; condición derivada `Closed` (docs-only, sin release); sin `VERSION`
bump ni tag.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `98-change-lifecycle-unit-d-increment-4.md` | RFC-75 | Executed | Plan de implementación de la Unidad D (Incremento 4) del Change Lifecycle DEV: especifica la primera automatización operativa del lifecycle como mínimo viable C-1 (lifecycle anchor checker propuesto `tools/check_lifecycle_anchor.py` + `tests/test_check_lifecycle_anchor.py`: forma/completitud de anchors v1, distinción GAP advisory vs anomalía, sin autoridad normativa) y C-2 (lifecycle checkpoint checker propuesto `tools/check_lifecycle_checkpoint.py` + `tests/test_check_lifecycle_checkpoint.py`: relación closure↔estado Git con tree identity, consistencia GC-1 contra el anchor del estado de cierre, modelo A1/A2 de la Decisión B, SHA = locator, sin reachability desde `dev`); población del régimen nuevo por señales estructurales del artifact (secciones del template `## Validation anchor`/`## Checkpoint / cierre`) sin registry global ni entidad Change; legacy excluido sin backfill automático (RFC-75 Mec. 15); testing determinista con pytest `tmp_path` y git temporales (19 escenarios C-1 + 21 escenarios C-2); dogfooding sobre el repo real; commits C1/C2 separados; recovery/stop conditions; AC-01…AC-21; sin `VERSION` bump ni tag, sin CI y sin tocar `protocol/.agents/` ni `.agents/` raíz. **Creación (2026-09-02):** artifact creado y registrado sin ejecutar (Status `Aprobado para ejecución`, PLANNED / OPEN; veredicto GO WITH CONDITIONS C1–C4); checkers documentales en verde; sin commits; Plan 98 NO `Executed`/`Closed`. **Ejecución (2026-09-02):** C-1/C-2 implementados y verificados — pytest `359 passed` (GATE C-1) y `380 passed` (GATE C-2), checkers canónicos PASS (warnings esperados de `dev`), `git diff --check` limpio; commits C1 `669a576` y C2 `9b5b8a1` en `dev`; dogfooding C-1/C-2: planes 96/97 `VALID` (tree de C1 == T1 declarado), plan 98 `N/A` en PLANNED, legacy 01–95 `EXCLUDED`, GAP=0, ANOMALY=0; validación adversarial PASS (tree identity, A1→A2, no-reachability, legacy, GAP/anomalía); Validation Anchor V1 (state identity T1 `1a3e93e9…`; delta `9d523cce…`) y Checkpoint con revalidación V2 sobre el estado final antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release). Dogfooding del propio plan: `No findings detected / N/A`; resolución documentada de OQ-7 (variante de encabezado `## Checkpoint` del corpus 96). Sin cambios en `protocol/`, `runtime/`, VERSION, ADRs/RFCs, `docs/AGENTS.md` ni planes 94–97. | active |

## Trigésima primera serie: Change Lifecycle DEV — Corrección post-close F-1 (C-2/GC-1) (02 sep 2026)

Primer correction Plan post-close de la serie Change Lifecycle DEV (RFC-75),
derivado del **C1/C2 Read-Only Audit Report** posterior a la ejecución/cierre
de Plan 98. Corrige exclusivamente el defecto de materialización **F-1**
(MAJOR) en C-2 (`tools/check_lifecycle_checkpoint.py`): la selección del
Validation Anchor aplicable de GC-1 usa recencia ("latest A2 wins") y
pertenencia genérica del tree entre los commits de cierre, en lugar de
identificar el estado de cierre y seleccionar el anchor de la validación cuyo
estado validado corresponde a ese estado. La ejecución futura corrige
únicamente C-2 + los tests relacionados (`tests/test_check_lifecycle_checkpoint.py`)
con regresiones obligatorias (Casos A/B/C adversariales y 10 casos adicionales),
preservando tree identity ≠ SHA, no-reachability, GAP advisory ≠ ANOMALY,
A1 inmutable y A2 con lineage hacia A1, sin tocar C-1, F-2…F-9, `C-n`,
RFC-75/ADR-15/16 ni Plan 98 (que permanece CLOSED). Cambio DEV-only sin
`VERSION` bump ni tag (RFC-69); plan creado y registrado sin ejecutar
(2026-09-02, Status `Aprobado para ejecución`, PLANNED / OPEN; veredicto GO
WITH CONDITIONS); checkers documentales en verde; sin commits; sin implementar
F-1. **Ejecución (2026-09-02):** F-1 corregido en C-2
(`tools/check_lifecycle_checkpoint.py` + `tests/test_check_lifecycle_checkpoint.py`)
con selección del anchor por correspondencia de estado (sin "latest A2 wins"
ni pertenencia genérica del tree) y regresiones permanentes (Casos A/B/C +
T1–T12); commit C1 `42da250`; pytest `388 passed, 0 failed`; checkers
canónicos PASS; dogfooding 96/97/98 `VALID` y `ANOMALY=0`; Validation Anchor
V1 (T1 `e9b47b1c…`; delta `dfb76a4d…`) y Checkpoint con revalidación V2 antes
de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin
release); `<PLAN-99>:C-1` registrado; sin cambios en `protocol/`, `runtime/`,
C-1, VERSION, ADRs/RFCs ni Plan 98.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `99-change-lifecycle-f1-c2-gc1-correction.md` | RFC-75 | Executed | Correction Plan post-close de F-1 (C1/C2 Read-Only Audit Report posterior a Plan 98): corrige la materialización de GC-1 en C-2 (`tools/check_lifecycle_checkpoint.py` + `tests/test_check_lifecycle_checkpoint.py`) para seleccionar el anchor de la validación cuyo estado validado corresponde al estado de cierre (Tier 1 por tree identity; Tier 2 por revalidación declarada única sobre el cierre para el patrón corpus 96–98; sin recencia, sin pertenencia genérica del tree, sin SHA/reachability como identidad); reglas R-99-1…R-99-10; regresiones obligatorias Casos A/B/C + escenarios T1–T12; conserva GAP advisory ≠ ANOMALY, A1/A2 (Decisión B), anti-circularidad (estados validados solo desde la sección `## Validation anchor`), dogfooding sin regresiones sobre planes 96/97/98; `C-n` (`<PLAN-99>:C-1`) especificado y registrado al cerrar; anchor/checkpoint propios; cierre docs-only sin release; sin modificar RFC-75/ADR-15/16, C-1, Plan 98 (CLOSED), `protocol/.agents/` ni `.agents/`. **Creación (2026-09-02):** artifact creado y registrado sin ejecutar (Status `Aprobado para ejecución`, PLANNED / OPEN; veredicto GO WITH CONDITIONS C1–C4); checkers documentales en verde; sin commits; F-1 registrado como `<PLAN-99>:F-1` (open); Plan 99 NO `Executed`/`Closed`. **Ejecución (2026-09-02):** C-2 corregido y verificado — pytest `388 passed, 0 failed` (29 tests C-2: 21 existentes + 8 regresiones F-1), checkers canónicos PASS, `git diff --check` limpio; commit C1 `42da250` en `dev` (2 archivos; tree `e9b47b1c…`); dogfooding C-1/C-2: planes 96/97/98 `VALID` (anchor aplicable A2 declarado), plan 99 `N/A` pre-cierre y `VALID` tras su cierre, legacy 01–95 `EXCLUDED`, GAP=0, ANOMALY=0; adversarial review PASS (los 3 casos del bug original fallan sobre la implementación anterior y pasan sobre la corregida); Validation Anchor V1 (state identity T1 `e9b47b1c…`; delta `dfb76a4d…`) y Checkpoint con revalidación V2 sobre el estado final antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); `<PLAN-99>:C-1` registrado (F-1 `resolved`). Sin cambios en `protocol/`, `runtime/`, C-1, VERSION, ADRs/RFCs, `docs/CONVENTIONS.md`, `docs/VERSIONING.md` ni Plan 98; sin push. | active |

## Trigésima segunda serie: Change Lifecycle DEV — Continuación post-roadmap A–D (lineage integrity / LC-1, C-3) (02 sep 2026)

Primer Implementation Plan **posterior al roadmap A–D** de la serie Change
Lifecycle DEV (RFC-75): no es una unidad histórica del roadmap y no inventa un
"Incremento 5". Continúa la materialización del lifecycle automatizando la
siguiente capacidad que el estado factual del repo demuestra más madura:
**integridad de lineage de findings/corrections/revalidación (LC-1)**,
verificada por un checker determinista nuevo **C-3 — lifecycle lineage
checker** (propuesto `tools/check_lifecycle_lineage.py` +
`tests/test_check_lifecycle_lineage.py`): verifica forma, completitud mínima y
consistencia de los registros del Incremento 2 (`### Findings`/`### Correcciones`
del contenedor `## Findings / Correcciones / Pending`) — refs calificadas
`<artifact>:F-<n>`/`C-<n>` con namespace del artifact, vocabulario de estados,
elementos inmutables del finding (CL-8), provenance a origen y alcance de
revalidación de corrections (CL-6), trazabilidad de claims de revalidación a
evidencia declarada del propio artifact (CL-7), marcadores de ausencia y
contradicciones de resolución — con clasificaciones EXCLUDED/BOUNDARY/N/A/
VALID/GAP/ANOMALY, GAP advisory ≠ ANOMALY, sin autoridad normativa (ADR-16),
read-only, stdlib-only y sin Git en v1. Gate persist → observe → automate
satisfecho con datos reales (Plan 99: cadena `<PLAN-99>:F-1` → `<PLAN-99>:C-1`
→ V1/V2 → `resolved`; Plan 98: ausencia declarada `No findings detected /
N/A`). Cambio DEV-only (tooling + tests + registros de cierre) sin `VERSION`
bump ni tag (RFC-69); sin incorporación inicial a la batería canónica ni a CI;
sin F-3/F-2…F-9, sin pending (PC-1), sin C-1/C-2, sin RFC/ADR nuevos ni
modificación de Planes 94–99. **Creación (2026-09-02):** artifact creado y
registrado sin ejecutar (Status `Aprobado para ejecución`, PLANNED / OPEN;
veredicto GO WITH CONDITIONS C1–C4); checkers documentales en verde; sin
commits; Plan 100 NO `Executed`/`Closed`. **Ejecución (2026-09-02):** C-3
implementado (`tools/check_lifecycle_lineage.py` +
`tests/test_check_lifecycle_lineage.py`; reglas R-L1-1…R-L1-12; 40 tests:
matriz T01–T28 + 12 escenarios adversariales permanentes); pytest suite C-3
`40 passed` y pytest global `428 passed, 0 failed`; checkers canónicos PASS;
commits C1 `1ffe24c` (contenido) en `dev`; dogfooding C-3: planes 96/97
`EXCLUDED`, plan 98 `N/A`, plan 99 `VALID` (cadena `<PLAN-99>:F-1` →
`<PLAN-99>:C-1`), legacy 01–95 `EXCLUDED`, plan 100 lifecycle-stable
(`BOUNDARY` pre-C2 → `N/A` tras su cierre), GAP=0, ANOMALY=0; Validation
Anchor V1 (T1 `2f348f37…`; delta `e4f715ec…`) y Checkpoint con revalidación
V2 antes de `Closed`; status `Executed`; condición derivada `Closed`
(docs-only, sin release); sin cambios en `protocol/`, `runtime/`, C-1/C-2,
RFC-75/ADR-15/16, VERSION ni Planes 94–99; sin push.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `100-change-lifecycle-lineage-integrity.md` | RFC-75 | Executed | Plan de implementación de la continuación post-roadmap A–D del Change Lifecycle DEV: selecciona con evidencia la capacidad de integridad de lineage findings/corrections/revalidación (LC-1/CL-6/CL-7) y especifica C-3 — lifecycle lineage checker (`tools/check_lifecycle_lineage.py` + `tests/test_check_lifecycle_lineage.py` propuestos): población estructural del dominio del Incremento 2 (contenedor `## Findings / Correcciones / Pending`; subsecciones `### Findings`/`### Correcciones`; `### Pending decisions` fuera de v1), contrato de registros y refs calificadas `<artifact>:F-<n>`/`C-<n>` con namespace del artifact, vocabulario de estados (open/partially-resolved/resolved/deferred/superseded), elementos inmutables del finding (CL-8), provenance a origen y alcance de revalidación de corrections (CL-6), soporte declarado de claims de revalidación en el `## Validation anchor`/checkpoint del mismo artifact (CL-7), marcadores de ausencia (`No findings detected / N/A`) y contradicciones de resolución; clasificaciones EXCLUDED/BOUNDARY/N/A/VALID/GAP/ANOMALY con GAP advisory ≠ ANOMALY y sin autoridad normativa (ADR-16); read-only, stdlib-only, sin Git en v1, exit 0 salvo ANOMALY; matriz de tests T01–T28 (happy path, missing, malformed, conflicting, legacy, boundary `reopened`, no-retroactivity, determinismo, ejecución repetida, adversarial, dogfooding real, stdlib-only); dogfooding esperado Plan 98 `N/A`, Plan 99 `VALID`, planes 96/97 y legacy `EXCLUDED`, `ANOMALY=0`; sin F-3 (no bloqueante; GAP sin tie-break ante duplicados), sin F-2…F-9, sin pending/PC-1, sin C-1/C-2, sin RFC/ADR nuevos, sin incorporación a batería canónica/CI; commits C1/C2 al ejecutar; anchor/checkpoint propios; cierre docs-only sin release; RFC-75/ADR-15/16 y Planes 94–99 intactos. **Creación (2026-09-02):** artifact creado y registrado sin ejecutar (Status `Aprobado para ejecución`, PLANNED / OPEN; veredicto GO WITH CONDITIONS C1–C4); checkers documentales en verde; sin commits; Plan 100 NO `Executed`/`Closed`. **Ejecución (2026-09-02):** C-3 implementado y verificado — pytest suite C-3 `40 passed` (matriz T01–T28 + 12 adversariales permanentes) y pytest global `428 passed, 0 failed`; checkers canónicos PASS; commit C1 `1ffe24c` (contenido: tool + suite) en `dev`; dogfooding C-3: planes 96/97 `EXCLUDED`, plan 98 `N/A`, plan 99 `VALID` (cadena `<PLAN-99>:F-1` → `<PLAN-99>:C-1`), legacy 01–95 `EXCLUDED`, plan 100 `BOUNDARY` pre-C2 → `N/A` tras su cierre, GAP=0, ANOMALY=0; Validation Anchor V1 (T1 `2f348f37…`; delta `e4f715ec…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); sin cambios en `protocol/`, `runtime/`, C-1/C-2, RFC-75/ADR-15/16, VERSION ni Planes 94–99; sin push. | active |

## Trigésima tercera serie: Change Lifecycle DEV — Capa operacional `.agents/` (Plan 101) (02 sep 2026)

Implementation Plan **posterior al cierre de la serie A–D** del Change
Lifecycle DEV (RFC-75): formaliza la materialización futura de la **capa
operacional `.agents/` de ARgentOS DEV** en la raíz del repo fuente como
interfaz operacional permanente que un agente LLM lee para ejecutar el Change
Lifecycle (entry point `.agents/AGENTS.md` + workflow
`.agents/workflows/change-lifecycle.md` + policies de authority,
validation-closure y lifecycle-checkers), con integración mínima de
descubrimiento/taxonomía/frontera en `AGENTS.md` raíz, `docs/AGENTS.md` y
`docs/CONVENTIONS.md`; fuente de diseño = staging temporal gitignored
`sessions/agents-dev-layer/` (no versionado, no operacional), con transición
explícita staging → `/.agents/` y eliminación del staging tras materialización
verificada (sin duplicación operacional permanente). Reutiliza RFC-75,
ADR-15/16, C1/C2/C3, templates y convenciones sin crear autoridad normativa
nueva, sin state machines/registries/databases/tracker globales, sin copiar
`protocol/.agents/` (frontera DEV/Protocol intacta; `protocol/`, `dist/`,
`runtime/`, `tools/`, `tests/` excluidos), sin checkers nuevos ni modificación
de C1/C2/C3 salvo necesidad factual estrictamente imprescindible autorizada
por el propio alcance, sin F-3/F-2…F-9, sin RFC/ADR nuevos ni modificación de
RFC-75/ADR-15/16 ni Planes 94–100; gates G0–G7, criterios AC-101-01…AC-101-18,
dogfooding operacional, recovery con Git, commits C1/C2 al ejecutar, cierre
docs-only sin release (RFC-69). **Creación (2026-09-02):** artifact creado y
registrado sin ejecutar (Status `Aprobado para ejecución`, PLANNED / OPEN;
Planned YES; Executed NO; Committed NO; Verified NO; Closed NO; Released NO;
veredicto GO — CREATION ONLY; ejecución futura GO WITH CONDITIONS C1–C4);
checkers documentales en verde; C1/C2/C3 sin ANOMALY; sin commits; Plan 101 NO
`Executed`/`Closed`; `.agents/` NO materializado; staging intacto.
**Ejecución (2026-09-03):** Plan 101 ejecutado con autorización explícita del
mantenedor — capa `.agents/` materializada en la raíz (5 archivos: AGENTS.md +
workflow + 3 policies, 1:1 con el diseño staged verificado por hash),
integración mínima aplicada (`AGENTS.md` raíz con puntero de descubrimiento;
`docs/AGENTS.md` con taxonomía de la capa operacional; `docs/CONVENTIONS.md`
con frontera documental Producto vs DEV), dogfooding G7 PASS (cadena
`AGENTS.md` → `.agents/AGENTS.md` → workflow → policies sin cargar todo
`docs/`); pytest `428 passed, 0 failed`; checkers canónicos PASS; C1/C2/C3
GAP=0, ANOMALY=0; commit C1 `3706570` (contenido) + C2 (registro) en `dev`;
Validation Anchor V1 (T1 `74f96b14…`; delta `47c95eee…`) y Checkpoint con
revalidación V2 antes de `Closed`; status `Executed`; condición derivada
`Closed` (docs-only, sin release); staging `sessions/agents-dev-layer/`
eliminado tras materialización verificada; sin findings/corrections reales;
sin cambios en `protocol/`, `runtime/`, C-1/C-2/C-3, RFC-75/ADR-15/16,
VERSION ni Planes 94–100; sin push.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `101-change-lifecycle-agents-operational-layer.md` | RFC-75 | Executed | Plan de implementación posterior al roadmap A–D del Change Lifecycle DEV: autoriza la **materialización futura** de la capa operacional `.agents/` de ARgentOS DEV en la raíz del repo fuente (ubicación canónica `/.agents/`), como interfaz operacional permanente del agente LLM para ejecutar el Change Lifecycle — `.agents/AGENTS.md` (entry point operacional DEV; descubrible desde el `AGENTS.md` raíz), `.agents/workflows/change-lifecycle.md` (intake → estado Git → detección/clasificación → autorización → Plan → ejecución → evidencia → validación → findings/corrections/revalidation → checkpoint → Closed → post-close), `.agents/policies/authority.md` (FACTUAL/NORMATIVE/DECISION/RELEASE/DESCRIPTIVE + detect → classify → escalate → human decision → correct artifact → revalidate), `.agents/policies/validation-closure.md` (A1/A2/revalidation/anchor/closure state/checkpoint/Executed/Committed/Verified/Closed/Released/GAP/ANOMALY/stop conditions; GC-1 por correspondencia de estado validado→cierre, semántica corregida F-1 en C-2, sin latest A2 wins ni generic tree membership) y `.agents/policies/lifecycle-checkers.md` (C1/C2/C3: cuándo/input/VALID/GAP/ANOMALY/acción; deterministas, no normativos; sin copiar algoritmos) — más integración mínima de descubribilidad, entry point, taxonomía (`docs/AGENTS.md`) y frontera documental Product/Protocol vs DEV (`docs/CONVENTIONS.md`); fuente de diseño = staging temporal `sessions/agents-dev-layer/` (gitignored, no versionado, no operacional) con transición y eliminación del staging tras materialización exitosa (AC-101-09); sin autoridad normativa nueva (`.agents/` = operación sobre contratos existentes; `docs/` = autoridad/historia; `tools/` = verificación determinista); frontera DEV/Protocol intacta (sin copias de `protocol/.agents/`; `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/` excluidos); sin checkers nuevos, sin modificación de C1/C2/C3 salvo necesidad factual imprescindible autorizada, sin F-3/F-2…F-9, sin pending/PC-1 nuevos, sin RFC/ADR, sin state machines/registries/databases/trackers; gates G0–G7 y criterios AC-101-01…AC-101-18 verificables; dogfooding operacional (AGENTS.md → `.agents/AGENTS.md` → workflow → clasificación → autoridad → Plan → ejecución → C1/C2/C3 → validation → checkpoint → Closed) sin cargar todo `docs/`; recovery con Git (materialización parcial, paths incorrectos, divergencia staging/`.agents/`, modificación accidental de `protocol/.agents/`, root AGENTS incorrecto, docs incoherente, validación fallida, rollback); commits C1 (materialización/integración) y C2 (registro/cierre) al ejecutar en `dev`, sin push/tag/release/VERSION bump; anchor/checkpoint propios (V1/V2) al cerrar; cierre docs-only sin release (RFC-69); RFC-75/ADR-15/16 y Planes 94–100 intactos. **Creación (2026-09-02):** artifact creado y registrado sin ejecutar (Status `Aprobado para ejecución`, PLANNED / OPEN; Planned YES; Executed NO; Committed NO; Verified NO; Closed NO; Released NO; veredicto GO — CREATION ONLY; ejecución futura GO WITH CONDITIONS C1–C4); checkers documentales en verde (estructura, citas; C1/C2/C3 GAP=0, ANOMALY=0); sin commits; Plan 101 NO `Executed`/`Closed`; `.agents/` NO materializado en la raíz; staging `sessions/agents-dev-layer/` intacto. **Ejecución (2026-09-03):** capa `.agents/` materializada e integrada — commit C1 `3706570` (5 archivos `.agents/` + `AGENTS.md` + `docs/AGENTS.md` + `docs/CONVENTIONS.md`) y commit C2 (registro/cierre) en `dev`; pytest `428 passed, 0 failed`; checkers canónicos PASS; dogfooding C1/C2/C3 GAP=0, ANOMALY=0 (plan 101 `VALID` C-1/C-2, `N/A` C-3); Validation Anchor V1 (T1 `74f96b14…`; delta `47c95eee…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); staging eliminado; sin findings/corrections; sin cambios en `protocol/`, `runtime/`, C-1/C-2/C-3, RFC-75/ADR-15/16, VERSION ni Planes 94–100; sin push. | active |

## Trigésima cuarta serie: README — Repository Operational Model (Plan 102) (03 sep 2026)

Plan 102 (cambio DEV docs-only, RFC-75; sin efecto sobre
`protocol/.agents/`): agrega a `README.md` una sección breve
`## Repository Operational Model` que explica la separación operacional entre
`.agents/` (interfaz operacional del agente DEV), `docs/` (autoridad/historia/
documentación) y `tools/` (verificación determinista, sin autoridad normativa
propia), y la frontera con `protocol/.agents/` (dominio del Protocol; data, no
instrucciones DEV). Clasificación: clase RFC-56 — (sin payload), Change Level
L1, scope documental (README EntryPoint + artifacts de registro del plan).
Ejecución en `dev`: commit C1 `f6cf0a8` (contenido README) y commit C2
(registro/cierre) con anchor/checkpoint propios; cierre docs-only sin `VERSION`
bump ni tag (RFC-69). Sin cambios en `.agents/`, `protocol/`, `runtime/`,
`tests/`, `tools/`, `dist/` ni Planes 94–101.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `102-readme-repository-operational-model.md` | RFC-75 | Executed | Agrega a `README.md` la sección `## Repository Operational Model` (breve, en inglés, orientada a agentes/desarrolladores nuevos): `.agents/` es la interfaz operacional que un agente consulta para orientarse y ejecutar trabajo en DEV (instrucciones operacionales; la autoridad normativa vive en `docs/`); `docs/` contiene documentación, convenciones, decisiones y evidencia documental según su autoridad; `tools/` contiene mecanismos de verificación/chequeo y su output es evidencia factual, nunca autoridad normativa por sí mismo; `protocol/.agents/` pertenece al dominio del Protocol (entry `protocol/_AGENTS.md`) y no debe confundirse con el `.agents/` operacional de DEV. Cambio DEV docs-only: clase RFC-56 —, Change Level L1, sin `VERSION` bump ni tag (RFC-69); commits C1 `f6cf0a8` (contenido) + C2 (registro/cierre) en `dev`; Validation Anchor V1 (T1 `7da67a2f…`; delta `82b2e799…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections; sin cambios en `.agents/`, `protocol/`, `runtime/`, `tests/`, `tools/`, `dist/`, VERSION ni Planes 94–101; sin push. | active |

## Trigésima quinta serie: aceptación de la RFC-64 (03 sep 2026)

Plan de aceptación/formalización docs-only de la RFC-64 (Execution Record
Model), siguiendo el patrón normativo de los planes 92/93 (RFC-73/74) bajo el
régimen del Change Lifecycle DEV (RFC-75; anchors/checkpoints de los
incrementos 1+3/2). No implementa ninguna capacidad: solo `Proposal →
Accepted` (status, cuerpo `## Status`, Amendment Log con las tres lecturas de
implementación de la decisión humana, INDEX de RFCs, alineación de metadatos de
estado de ADR-06/07/08/11 + ADR INDEX, changelog bajo `[Unreleased]` y registro
del plan). Sin `VERSION` bump ni tag (RFC-69). La aceptación NO autoriza la
ejecución del plan 78 (permanece `Aprobado para ejecución` sin ejecutar; las
condiciones C3–C6 de su ejecución futura quedan preservadas como contexto en el
Amendment Log de la RFC-64).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `103-rfc64-acceptance.md` | RFC-64 | Executed | Formaliza la aceptación de la RFC-64 (Execution Record Model): identidad de ejecución por composición, roles disjuntos de los registros, alcance de `state.json`, semántica temporal UTC con fuente declarada y observabilidad de budget. RFC-64 pasa a `Accepted (plan 103, 2026-09-03)` con entrada en su `## Amendment Log` que preserva las tres lecturas de implementación de la decisión humana (`clock` implementa `agent_clock` sin renombrar a `source`; `seq` estrictamente monótono por sesión; TR-002 con tolerancia de 60 s y `timestamp_divergence.cause`) y las condiciones futuras del plan 78 como contexto (versión 11.0.0, guard/fixtures legacy, METRICS schema 1.2.0, declaración de `state.json`, C3–C6; NO ejecutadas); INDEX de RFCs actualizado; ADR-06/07/08/11 + ADR INDEX con metadatos de estado alineados (sin contenido normativo nuevo). Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); commits C1 `5d1c8e0` (contenido) + C2 (registro/cierre) en `dev`; Validation Anchor V1 (T1 `fd0a3db8…`; delta `8e72e9b4…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections; sin cambios en `protocol/.agents/`, `runtime/`, `tests/`, `tools/`, `dist/`, VERSION ni Planes 94–102; Plan 78 intacto y NO ejecutado; sin push. | active |

## Trigésima sexta serie: alineación documental y operacional post-Plan-78 (Plan 104) (05 sep 2026)

Plan 104 (cambio DEV docs-only autorizado por decisión humana del mantenedor
«Plan 104 — Documentation & Operational Alignment», 2026-09-05; régimen
RFC-69/RFC-75; sin RFC nueva, clase RFC-56 —): alinea la documentación
operacional/descriptiva con el estado real post-Plan-78 (`11.0.0` pre-release
en `dev`, sin promover). Scope: root `AGENTS.md` como entrypoint/puntero sin
espejo de la batería canónica (layout de `docs/` corregido con `docs/rfc/`,
`docs/adr/` y `docs/plans/` diferenciados); `.agents/AGENTS.md` permanece como
entrypoint (no `INDEX.md`) con la alineación factual mínima del `## Verification
battery`; `README.md` sin batería parcial duplicada; `docs/VERSIONING.md` §9
como snapshot 2026-09-05 coherente con git y §4.1 con ownership único de la
batería; `docs/CONVENTIONS.md` con rangos actualizados (RFCs hasta RFC-75;
ADRs hasta ADR-16); `docs/MIGRATION.md` con el link `../CHANGELOG.md` corregido;
`CHANGELOG.md` con `[Unreleased]` en la posición superior; modelos de
arquitectura preservados como snapshots históricos con banner mínimo (contenido
original intacto). Sin cambios en `protocol/.agents/`, `runtime/`, `tools/`,
`tests/`, `dist/`, `protocol/.agents/VERSION` (11.0.0), Deferred
(ROADMAP/audits/source-layout/ADOPTION) ni tags; sin promoción de `11.0.0`.
Ejecución en `dev`: commit C1 `a2c9c43` (contenido) y commit C2
(registro/cierre); Validation Anchor V1 (T1 `639c4fce…`; delta `792e1507…`) y
Checkpoint con revalidación V2 antes de `Closed`; C1/C2/C3 GAP=0, ANOMALY=0;
status `Executed`; condición derivada `Closed` (docs-only, sin release); sin
findings/corrections.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `104-documentation-operational-alignment.md` | — | Executed | Alineación documental y operacional post-Plan-78 (decisión humana 2026-09-05): root `AGENTS.md` como entrypoint/puntero a la batería canónica de `docs/VERSIONING.md` §4.1 con layout de `docs/` corregido (RFCs/ADRs/planes diferenciados); `.agents/AGENTS.md` intacto como entrypoint operacional (alineación factual mínima del `## Verification battery`: puntero, no espejo; sin `INDEX.md`); `README.md` sin batería parcial (puntero canónico); `docs/VERSIONING.md` §9 snapshot 2026-09-05 (master/dist `10.3.0`; dev `11.0.0` pre-release; tags hasta `10.3.0`) y §4.1 con ownership único; `docs/CONVENTIONS.md` con rangos actualizados (RFC-75/ADR-16); `docs/MIGRATION.md` link `../CHANGELOG.md` corregido; `CHANGELOG.md` con `[Unreleased]` reubicado arriba; banners históricos mínimos en `ARCHITECTURAL_PROBLEM_MODEL.md` y `ARCHITECTURAL_DECISION_MODEL.md` (contenido original preservado; materialización posterior respaldada por la matriz `docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`). Cambio DEV docs-only: clase RFC-56 —, Change Level L2, sin `VERSION` bump ni tag (RFC-69); commits C1 `a2c9c43` (contenido) + C2 (registro/cierre) en `dev`; Validation Anchor V1 (T1 `639c4fce…`; delta `792e1507…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections; sin cambios en `protocol/.agents/`, `runtime/`, `tests/`, `tools/`, `dist/`, `protocol/.agents/VERSION` (11.0.0), Deferred ni Planes 94–103; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Trigésima séptima serie: arquitectura terminológica y glosario (Plan 105) (05 sep 2026)

Plan 105 (cambio DEV docs-only autorizado por decisiones humanas del
mantenedor D1–D5, 2026-09-05; régimen RFC-69/RFC-75; sin RFC/ADR nuevo, clase
RFC-56 —): materializa la arquitectura terminológica aprobada: vocabularios
DEV/Protocol separados con puente descriptivo (`docs/glossary/`), glosario
`docs/glossary/INDEX.md` + `terms.md` como registro Inventory/DESCRIPTIVE no
normativo, reglas operacionales D1–D5 en `docs/CONVENTIONS.md`, semántica
AGENTS/INDEX/ENTRYPOINT y mapa de clase en `docs/AGENTS.md`, punteros de
descubrimiento en root `AGENTS.md` y `.agents/AGENTS.md`. Sin cambios en
`protocol/.agents/`, `runtime/`, `tools/`, `tests/`, `dist/`,
`protocol/.agents/VERSION` (11.0.0) ni tags; sin renames; sin checker nuevo.
Ejecución en `dev`: commit C1 `120f44e` (contenido) y C2 (registro/cierre);
Validation Anchor V1 (T1 `69f16b4f…`; delta `346ab984…`) y Checkpoint con
revalidación V2 antes de `Closed`; C1/C2/C3 GAP=0, ANOMALY=0; status
`Executed`; condición derivada `Closed` (docs-only, sin release); sin
findings/corrections.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `105-terminology-architecture-materialization.md` | — | Executed | Materialización docs-only de las decisiones humanas D1–D5 (terminología: vocabularios separados + puente descriptivo; glosario `docs/glossary/INDEX.md` + `terms.md` Inventory/DESCRIPTIVE no normativo; convención AGENTS/INDEX/ENTRYPOINT preservada; regla SCI; reglas de calificación; semántica documentada en `docs/AGENTS.md` y regla operacional en `docs/CONVENTIONS.md`). Cambio DEV docs-only: clase RFC-56 —, Change Level L2, sin `VERSION` bump ni tag (RFC-69); commits C1 `120f44e` (contenido) + C2 (registro/cierre) en `dev`; Validation Anchor V1 (T1 `69f16b4f…`; delta `346ab984…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); pending no bloqueante de elevación ADR futura; sin findings/corrections; sin cambios en `protocol/.agents/`, `runtime/`, `tests/`, `tools/`, `dist/`, `protocol/.agents/VERSION` (11.0.0) ni Planes 94–104; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Trigésima octava serie: corrección post-close del glosario (Plan 106) (05 sep 2026)

Plan 106 (cambio DEV docs-only autorizado por el mantenedor, 2026-09-05;
régimen RFC-69/RFC-75; sin RFC/ADR nuevo, clase RFC-56 —): corrige los
hallazgos F1–F5 del Fresh Agent Terminology Stress Test sobre los artifacts
del Plan 105 (glosario): referencias de autoridad malformadas (F1/F2/F3),
regla de cobertura/alta explícita (F4) y normalización del vocabulario de
`Status` con restricciones de uso modeladas por separado (F5). Sin cambios en
`protocol/.agents/`, `runtime/`, `tools/`, `tests/`, `dist/`,
`protocol/.agents/VERSION` (11.0.0), sin renames y sin reabrir el Plan 105
(post-close por referencia, RFC-75 Mecanismo 12).
Ejecución en `dev`: commit C1 `922931a` (contenido), C2 `d0ca838` y C3
`de53e29` (registro/cierre + residual) y C4 (alineación final del registro);
Validation Anchor V1 (T1 `b4a6c860…`; delta `24adc65f…`) y Checkpoint con
revalidación V2 antes de `Closed`; C1/C2/C3 GAP=0, ANOMALY=0; status
`Executed`; condición derivada `Closed` (docs-only, sin release); findings
`<PLAN-106>:F-1..F-5` resueltos vía `<PLAN-106>:C-1..C-5`; corrección residual
de referencias malformadas en `terms.md` (misma clase F1/F3) cubierta por V2.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `106-post-close-glossary-correction.md` | — | Executed | Corrección docs-only post-close F1–F5 sobre los artifacts del Plan 105 (glosario): F1 cita de autoridad malformada reparada; F2 `Authority Reference` restaurado; F3 referencia `path:section` reemplazada por heading real (+ referencias malformadas residuales en `terms.md`, misma clase); F4 sección «Cobertura y alta de entradas» (selectiva; ausencia ≠ defecto; alta por ambigüedad/gobernanza/cross-layer); F5 `current (restricted)` eliminado — restricciones de uso separadas del `Status`. Cambio DEV docs-only: clase RFC-56 —, Change Level L1, sin `VERSION` bump ni tag (RFC-69); commits C1 `922931a` (contenido) + C2 `d0ca838` + C3 `de53e29` (registro/cierre y residual) + C4 (alineación final) en `dev`; Validation Anchor V1 (T1 `b4a6c860…`; delta `24adc65f…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); findings `<PLAN-106>:F-1..F-5` resueltos vía `<PLAN-106>:C-1..C-5` (FACTUAL/TRACEABILITY); sin cambios en `protocol/.agents/`, `runtime/`, `tests/`, `tools/`, `dist/`, `protocol/.agents/VERSION` (11.0.0), Plan 105 (`Closed`) ni documentos históricos; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Trigésima novena serie: determinación DEV del estado terminal por ejecución (Plan 107) (05 sep 2026)

Plan 107 (cambio DEV de tooling + registros docs-only autorizado por el
mantenedor, 2026-09-05; régimen RFC-75/RFC-69; sin RFC/ADR nuevo, clase RFC-56
—): mecanismo DEV read-only que determina el estado terminal de cada ejecución
(`execution_id = (session_id, iteration)`) desde su Execution Record —
`state.json` `status` terminal (`ABORT`/`COMPLETED`), la verdad mecánica del
estado del protocolo por ejecución (RFC-64/RFC-63) — sin modificar el modelo
del Protocol, sin campos/estados/artifacts/categorías nuevas y sin inferir un
resultado cuando el registro no declara estado terminal (`no_gates_passed`,
`in_progress`), `state.json` falta o está corrupto (fail-closed). Sin cambios
en `protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION`
(11.0.0), sin release.
Ejecución en `dev`: commit C1 `5dbd5bd` (contenido: herramienta + 13 tests),
C2 (registro/cierre); Validation Anchor V1 (T1 `bf88ca4c…`; delta
`a68ae699…`) y Checkpoint con revalidación V2 antes de `Closed`; C-1/C-2/C-3
GAP=0, ANOMALY=0; status `Executed`; condición derivada `Closed` (docs-only,
sin release); sin findings/corrections/pending (`N/A`); sin push, sin merge,
sin tag; `11.0.0` sigue sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `107-determinacion-estado-terminal-ejecucion.md` | — | Executed | Mecanismo DEV de determinación/verificación del estado terminal por ejecución desde los Execution Records existentes: `tools/determine_execution_state.py` (determinismo sobre `state.json` `status`; no determinación declarada con razón para registros no terminales o `state.json` ausente/corrupto; salida JSON ordenada; stdlib-only, read-only) + `tests/test_determine_execution_state.py` (13 tests). Cambio DEV tooling + registros docs-only: clase RFC-56 —, Change Level L2, sin `VERSION` bump ni tag (RFC-69); commits C1 `5dbd5bd` (contenido) + C2 (registro/cierre) en `dev`; Validation Anchor V1 (T1 `bf88ca4c…`; delta `a68ae699…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections/pending (`N/A`); sin cambios en `protocol/.agents/`, `runtime/`, `tests/` legacy, `dist/`, `protocol/.agents/VERSION` (11.0.0) ni Planes 94–106; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Cuadragésima serie: consulta DEV de una ejecución específica por iteración (Plan 108) (05 sep 2026)

Plan 108 (cambio DEV de tooling + registros docs-only autorizado por el
mantenedor, 2026-09-05; régimen RFC-75/RFC-69; sin RFC/ADR nuevo, clase RFC-56
—): extiende el mecanismo DEV de determinación del estado terminal por
ejecución con la consulta de **una ejecución específica**: `--iteration`
(requiere `--session`; identificación inequívoca por `execution_id =
(session_id, iteration)`, RFC-64) devuelve únicamente la determinación de esa
ejecución, reutilizando la semántica existente (determinación para `status`
terminal `ABORT`/`COMPLETED`; no determinación con razón para status no
terminal o `state.json` ausente/corrupto; fail-closed sin inferencia) y sin
agregar campos/estados/artifacts/categorías ni mecanismo paralelo. La consulta
de sesión completa conserva su comportamiento actual; la iteración o sesión
inexistente produce report vacío (ausencia = no determinación), sin fabricar
entradas. Sin cambios en `protocol/.agents/`, `runtime/`, `dist/`,
`protocol/.agents/VERSION` (11.0.0), sin release.
Ejecución en `dev`: commit C1 `f612d26` (contenido: herramienta + 9 tests
nuevos; suite total 22), C2 (registro/cierre); Validation Anchor V1 (T1
`d49f5473…`; delta `6f28624d…`) y Checkpoint con revalidación V2 antes de
`Closed`; C-1/C-2/C-3 GAP=0, ANOMALY=0; status `Executed`; condición derivada
`Closed` (docs-only, sin release); sin findings/corrections/pending (`N/A`);
sin push, sin merge, sin tag; `11.0.0` sigue sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `108-consulta-especifica-de-ejecucion.md` | — | Executed | Consulta DEV de una ejecución específica por iteración sobre el mecanismo de determinación del estado terminal: `tools/determine_execution_state.py` agrega `--iteration` (requiere `--session`; `execution_id = (session_id, iteration)`) y devuelve únicamente la determinación de esa ejecución con la semántica existente (determinación para `ABORT`/`COMPLETED`; no determinación con razón para no terminal o `state.json` ausente/corrupto; iteración/sesión inexistente → report vacío fail-closed sin fabricar entradas; sin `--iteration` la consulta de sesión completa es idéntica) + `tests/test_determine_execution_state.py` (9 tests nuevos; 22 en la suite). Cambio DEV tooling + registros docs-only: clase RFC-56 —, Change Level L2, sin `VERSION` bump ni tag (RFC-69); commits C1 `f612d26` (contenido) + C2 (registro/cierre) en `dev`; Validation Anchor V1 (T1 `d49f5473…`; delta `6f28624d…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections/pending (`N/A`); sin cambios en `protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION` (11.0.0) ni Planes 94–107; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Cuadragésima primera serie: generador DEV de Scoped Content Identity para Validation Anchors (Plan 109) (05 sep 2026)

Plan 109 (cambio DEV de tooling + registros docs-only autorizado por el
mantenedor, 2026-09-05 — Dogfooding Test #3 —; régimen RFC-75/RFC-69; sin
RFC/ADR nuevo, clase RFC-56 —): tool read-only que **genera** la Scoped
Content Identity v1 que cada Validation Anchor registra (VC-1) y que el
Checkpoint verifica (GC-1): `tools/scoped_content_identity.py` computa la
Delta scoped identity (sha256 de la serialización canónica `scoped-v1` +
pares `path NUL blob NUL` sobre un scope declarado de paths repo-relative
ordenados) y la State identity (tree del index staged vía `git write-tree`, o
del ref vía `git rev-parse <ref>^{tree}` con `--ref`), reutilizando el
algoritmo v1 ya normado (plan 96 §13) y las primitivas git existentes sin
modificar C-1/C-2/C-3, sin agregar campos/estados/artifacts/categorías ni
mecanismo paralelo. Fail-closed (path fuera del repo/faltante/directorio, repo
no git, ref no resoluble → error determinista, exit 1, sin salida parcial);
salida JSON determinista; sin escrituras al working tree ni al index. Sin
cambios en `protocol/.agents/`, `runtime/`, `dist/`,
`protocol/.agents/VERSION` (11.0.0), sin release.
Ejecución en `dev`: commit C1 `d8bc464` (contenido: herramienta + 15 tests;
suite total 482), C2 (registro/cierre); Validation Anchor V1 (T1
`12cff4c9…`; delta `e0b10edb…`, generada con el propio tool — dogfooding —)
y Checkpoint con revalidación V2 antes de `Closed`; C-1/C-2/C-3 GAP=0,
ANOMALY=0; status `Executed`; condición derivada `Closed` (docs-only, sin
release); sin findings/corrections/pending (`N/A`); sin push, sin merge, sin
tag; `11.0.0` sigue sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `109-scoped-content-identity-generator.md` | — | Executed | Generador DEV determinista de la Scoped Content Identity v1 para Validation Anchors/Checkpoints: `tools/scoped_content_identity.py` (scope de paths repo-relative normalizado/deduplicado/ordenado; blob id por `git ls-files -s` o `git hash-object --path` para untracked; serialización `scoped-v1` + pares `path NUL blob NUL`; sha256 delta; state identity staged `write-tree` o `--ref <ref>^{tree}`; JSON determinista; fail-closed sin salida parcial; stdlib-only, read-only, sin red) + `tests/test_scoped_content_identity.py` (15 tests en repos git aislados). Cambio DEV tooling + registros docs-only: clase RFC-56 —, Change Level L2, sin `VERSION` bump ni tag (RFC-69); commits C1 `d8bc464` (contenido) + C2 (registro/cierre) en `dev`; Validation Anchor V1 (T1 `12cff4c9…`; delta `e0b10edb…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections/pending (`N/A`); sin cambios en `protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION` (11.0.0) ni Planes 94–108; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Cuadragésima segunda serie: inspección DEV de una ejecución concreta con identidad de su contenido (Plan 110) (06 sep 2026)

Plan 110 (cambio DEV de tooling + registros docs-only autorizado por el
mantenedor, 2026-09-06 — Dogfooding Test #4, GO H1=1 —; régimen
RFC-75/RFC-69; sin RFC/ADR nuevo, clase RFC-56 —): extiende la consulta de
una ejecución específica (`determine_execution_state.py --session S
--iteration N`, Plan 108) con `--content-identity`: la entrada de la ejecución
relaciona su determinación con la Scoped Content Identity v1 del contenido de
su Execution Record (`.project/<session>/<iteration>/`, archivos presentes
ordenados), computada por composición con el generador existente
(`tools/scoped_content_identity.py`, Plan 109) — importado sin modificar, sin
duplicar el algoritmo v1, sin escrituras, sin tracking causal ni relación
persistente Execution Record ↔ proyecto. Fail-closed: scope vacío, root sin
repo git u otro error del generador → `applicable: false` con razón
determinista, sin fabricar identidad; sesión/iteración inexistente → report
vacío; sin el flag la salida es exactamente la actual. Sin cambios en
`protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION` (11.0.0),
sin release.
Ejecución en `dev`: commit C1 `bccf229` (contenido: herramienta + 18 tests
nuevos; pytest `500 passed`), C2 (registro/cierre); Validation Anchor V1 (T1
`416587fc…`; delta `1857802e…`, generada con el propio tool — dogfooding —) y
Checkpoint con revalidación V2 antes de `Closed`; C-1/C-2/C-3 GAP=0,
ANOMALY=0; status `Executed`; condición derivada `Closed` (docs-only, sin
release); sin findings/corrections/pending (`N/A`); sin push, sin merge, sin
tag; `11.0.0` sigue sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `110-inspeccion-ejecucion-identidad-contenido.md` | — | Executed | Inspección DEV de una ejecución concreta relacionada con la identidad de su contenido: `tools/determine_execution_state.py` agrega `--content-identity` (con `--session` + `--iteration`) a la consulta de una ejecución específica; la entrada agrega `content_identity` = Scoped Content Identity v1 del scope del Execution Record de la iteración (`.project/<session>/<iteration>/`), computada por composición con `tools/scoped_content_identity.py` (import sin modificar; sin duplicar el algoritmo v1; JSON determinista; `applicable: false` con razón para scope vacío / root sin repo git / error del generador; sesión o iteración inexistente → report vacío fail-closed; sin el flag la salida es exactamente la actual) + `tests/test_determine_execution_state.py` (18 tests nuevos; 40 en la suite). Cambio DEV tooling + registros docs-only: clase RFC-56 —, Change Level L2, sin `VERSION` bump ni tag (RFC-69); commits C1 `bccf229` (contenido) + C2 (registro/cierre) en `dev`; Validation Anchor V1 (T1 `416587fc…`; delta `1857802e…`) y Checkpoint con revalidación V2 antes de `Closed`; status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections/pending (`N/A`); sin cambios en `protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION` (11.0.0) ni Planes 94–109; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Cuadragésima tercera serie: resumen por sesión y filtro de ejecuciones sin determinación terminal (Plan 111) (06 sep 2026)

Plan 111 (cambio DEV de tooling + registros docs-only autorizado por el
mantenedor, 2026-09-06 — Dogfooding Test #6, GO H1=1 —; régimen
RFC-75/RFC-69; sin RFC/ADR nuevo, clase RFC-56 —): extiende la consulta DEV
de Execution Records (`tools/determine_execution_state.py`, Planes 107–110)
con dos modos aditivos de inspección read-only y determinista sobre la
semántica existente de `determine_iteration`: `--session-summary` (reporte
agregado por sesión: `protocol_version` de fuentes existentes, total/
determinadas/indeterminadas y conteos `ABORT`/`COMPLETED`; con o sin
`--session`; sesión o `.project/` ausentes → vacío fail-closed sin fabricar
entradas) y `--undetermined` (restringe el reporte por ejecución a las
entradas sin determinación con su razón existente; combinable con `--session`;
incompatible con `--iteration` y con `--session-summary`). Sin flags nuevos la
salida es exactamente la actual. El plan se ejecuta en dos etapas por agentes
independientes (Etapa 1: U1 + V1; Etapa 2: U2 + revalidación A2 + cierre).
Sin cambios en `protocol/.agents/`, `runtime/`, `dist/`,
`protocol/.agents/VERSION` (11.0.0), sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `111-resumen-por-sesion-ejecuciones-indeterminadas.md` | — | Executed | Consulta DEV de resumen por sesión y de ejecuciones sin determinación terminal sobre `tools/determine_execution_state.py` (Planes 107–110): U1 `--session-summary` (reporte agregado por sesión con `protocol_version` de fuentes existentes, `executions`/`determined`/`undetermined` y conteos `terminal_abort`/`terminal_completed` derivados de la semántica existente de `determine_iteration`; con o sin `--session`; sesión o `.project/` ausentes → `sessions` vacío y `summary` en cero, fail-closed sin fabricar entradas) y U2 `--undetermined` (reporte por ejecución restringido a `determined: false` con razón `state_json_missing`/`state_json_corrupt`/`status_not_terminal`; combinable con `--session`; incompatible con `--iteration` y con `--session-summary`, error determinista). Sin flags nuevos la salida es exactamente la actual (regresión cero); read-only, stdlib-only, sin red, sin escrituras sobre `.project/`. Cambio DEV tooling + registros docs-only: clase RFC-56 —, Change Level L2, sin `VERSION` bump ni tag (RFC-69); ejecución en dos etapas por agentes independientes (Etapa 1: U1 + tests + V1; Etapa 2: U2 + tests + revalidación A2 + cierre `Closed` docs-only); sin cambios en `protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION` (11.0.0) ni Planes 94–110; sin push, sin merge, sin tag; `11.0.0` sigue sin release. **Creación (2026-09-06):** artifact creado y registrado sin ejecutar (Status `Aprobado para ejecución`, GO del mantenedor registrado en el plan como H1 = 1); Plan 111 NO `Executed`/`Closed`. **Ejecución de la Etapa 1 (2026-09-06):** U1 `--session-summary` implementada y validada — V1 sobre C1 `a596f69` (T1 `2f1855c3…`; delta `9bd8fa87…` generada con el propio tool); checkers PASS y pytest `514 passed`; commit de registro P `0ebd412` y commit de contenido C1 `a596f69` en `dev`; sin cambios fuera del alcance del GO; Etapa 2 (U2 `--undetermined` + tests, revalidación A2 y cierre `Closed` docs-only) pendiente; Plan 111 NO `Executed`/`Closed`. **Ejecución de la Etapa 2 y cierre (2026-09-06):** U2 `--undetermined` implementada y validada (filtro de entradas sin determinación con razones existentes; combinable con `--session`; excluyente con `--iteration` y `--session-summary`; guard API); 10 tests nuevos (64 en la suite del archivo); commits C2 `c7fd80a` (contenido) y R2 (registro/cierre) en `dev`; revalidación A2 sobre el estado final (checkers PASS; pytest `524 passed`; C-1 `VALID`, C-2 `VALID` — A2 declarado, GC-1 —, C-3 `N/A`; GAP=0, ANOMALY=0); status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections/pending (`N/A`); sin cambios en `protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION` (11.0.0) ni Planes 94–110; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Cuadragésima cuarta serie: alcance determinista del gate S00 sobre el health checklist (Plan 112) (06 sep 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `112-alcance-s00-health-determinista.md` | — (vía plan, Clase B) | Executed | Alcance determinista del gate S00 sobre el health checklist: el ítem 2 de `protocol/.agents/orchestrators/system/harness/policies/S00-system-ready.md` (`## Checklist`) pasa a declarar como alcance PASS el de la `## Decision` vigente de `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md` (ítems 1–6, 8–9 y 11–13; ítem 10 sólo con el flag `knowledge_base` habilitado; ítem 7 warning-only), sin duplicar el checklist y sin cambio de significado (single-source policy). Cambio Protocol Clase B (RFC-56), Change Level L1; versión `11.0.1` (PATCH; `protocol/.agents/VERSION` 11.0.0 → 11.0.1); sin RFC ni ADR; sin cambios en `master`/`dist`/tags/push/release. **Creación (2026-09-06):** artifact creado y registrado sin ejecutar (Status `Aprobado para ejecución`, GO del mantenedor registrado en el plan como H1 = 1). **Ejecución y cierre (2026-09-06):** ítem 2 de S00 reformulado (alcance PASS por referencia a la Decision de `PROTOCOL_HEALTH.md`), `protocol/.agents/VERSION` → `11.0.1`, sección `[11.0.1]` en `CHANGELOG.md`, y ancla `PROTOCOL_VERSION` de `runtime/toolcalls/canonical.py` alineada a `11.0.1` (requisito mecánico del checker de versión; fuera del payload); commits A `abe2b37` (registro), C1 `310e974` (contenido) y R2 (registro/cierre) en `dev`; V1 sobre C1 y revalidación A2 sobre el estado final (checkers PASS; pytest `524 passed`; C-1 `VALID`, C-2 `VALID` — A2 declarado, GC-1 —, C-3 `N/A`; GAP=0, ANOMALY=0); status `Executed`; condición derivada `Closed` (con release pendiente); sin findings/corrections/pending (`N/A`); sin cambios en otros archivos del payload ni en `master`/`dist`/tags; sin push, sin merge, sin tag; `11.0.1` y `11.0.0` siguen sin release. | active |

## Cuadragésima quinta serie: materialización de la brújula de decisiones en el AGENTS.md raíz (Plan 113) (07 sep 2026)

Plan 113 (cambio DEV docs-only autorizado por el mantenedor, 2026-09-07, GO
registrado en el plan como H1 = 1): materializa la «brújula de decisiones» de
ARgentOS — claridad sobre crecimiento; separación de responsabilidades
RFC/Plan/Git/INDEX/Glossary; calidad de decisión sobre volumen documental;
contención («no change» como resultado válido); calidad de decisión como
objetivo de evaluación — como sección canónica `## Decision-Making Compass`
en el `AGENTS.md` raíz (entrypoint de instrucción DEV, primera lectura del
agente), explícitamente no normativa y sin duplicar autoridades de `docs/`.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `113-decision-making-compass-materialization.md` | — | Executed | Materialización docs-only de la brújula de decisiones como sección `## Decision-Making Compass` en el `AGENTS.md` raíz (P1–P5: claridad sobre crecimiento; separación RFC/Plan/Git/INDEX/Glossary; calidad de decisión sobre volumen documental; contención con «no change» como resultado válido; calidad de decisión como objetivo de evaluación no demostrado aún), declarada explícitamente como principios de juicio no normativos y sin duplicar autoridades de `docs/`. Cambio DEV docs-only: clase RFC-56 —, Change Level L1, sin `VERSION` bump ni tag (RFC-69); sin RFC/ADR nuevo; sin cambios en `protocol/.agents/` (`protocol/.agents/VERSION` 11.0.0), `runtime/`, `tools/`, `tests/`, `harness`, `dist/`, `master` ni tags. **Creación (2026-09-07):** artifact creado y registrado sin ejecutar (Status `Aprobado para ejecución`, GO del mantenedor registrado en el plan como H1 = 1); Plan 113 NO `Executed`/`Closed`. **Ejecución y cierre (2026-09-07):** sección canónica insertada en el `AGENTS.md` raíz (entre `## Do NOT` y `## Development workflow`); commits A `012c7f1` (registro), C1 `6ff06f6` (contenido) y R2 (registro/cierre) en `dev`; V1 sobre C1 (T1 `6fe6ec68…`; delta `16ea77bd…`) y revalidación A2 sobre el estado final (checkers PASS; pytest `524 passed`; C-1 `VALID`, C-2 `VALID` — A2 declarado, GC-1 —, C-3 `N/A`; GAP=0, ANOMALY=0); status `Executed`; condición derivada `Closed` (docs-only, sin release); sin findings/corrections/pending (`N/A`); sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Cuadragésima sexta serie: MVP de deliberación adversarial DEV — convención Working y primer dogfooding (Plan 114) (09 sep 2026)

Plan 114 (cambio DEV docs-only autorizado por el mantenedor, 2026-09-09, GO
registrado en el plan como H1 = GO; régimen RFC-75/RFC-69; sin RFC/ADR nuevo,
clase RFC-56 —): implementa el MVP de deliberación adversarial mediante el
mínimo suficiente cerrado en D1–D3 — (i) una **convención Working no normativa**
(`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`) con marco
declarado, pasadas de evaluación atribuidas (postura, ejecutor, material
recibido/compartido, compromiso antes de revelación, conclusiones con razones
por criterio, premisas, supuestos e incertidumbres), reglas de síntesis
(permitido/prohibido, argumento material nuevo ⇒ nueva pasada, no supresión ni
reescritura, desacuerdo preservado), vocabulario de veredicto de
viabilidad/preferencia, recomendación advisory y boundary de autoridad;
(ii) el **registro embebido** del primer Trial real en el propio Plan, sobre la
decisión pendiente `<PLAN-105>` (elevación ADR de la arquitectura
terminológica), con dos perspectivas atribuidas, síntesis, veredicto con base
declarada y recomendación advisory; (iii) evidencia de valor frente al
baseline. Sin código, sin tool, sin skill, sin checker, sin registry, sin state
machine, sin entidad global y sin cambios de plantillas. Sin cambios en
`protocol/.agents/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `dist/`,
`master` ni tags; sin `VERSION` bump ni tag (RFC-69); sin push, sin merge, sin
tag; `11.0.0` sigue sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `114-adversarial-deliberation-mvp.md` | — | Executed | MVP DEV de deliberación adversarial: convención Working no normativa (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`) + registro embebido del primer Trial real sobre la decisión pendiente `<PLAN-105>` + evidencia de valor. Cambio DEV docs-only: clase RFC-56 —, Change Level L1, sin `VERSION` bump ni tag (RFC-69); sin RFC/ADR nuevo; boundaries DEV/Protocol intactas. **Creación (2026-09-09):** artifact creado como borrador en `sessions/drafts/` y promovido a `docs/plans/` con `Status` `Aprobado para ejecución` y GO del mantenedor registrado en el plan como H1 = GO; sin `CHANGELOG` (reservado al cierre). **Ejecución (2026-09-09):** convención Working creada y registrada en el INDEX de propuestas (sin alterar otras entradas) y primer Trial real ejecutado sobre `<PLAN-105>` con marco declarado, dos perspectivas atribuidas (`E-A` / `E-B`), compromiso antes de revelación, procedencia registrada, síntesis con desacuerdo preservado, veredicto `NOT_VIABLE` con base declarada y recomendación advisory; la decisión humana **no** fue tomada y quedó escalada al mantenedor; commits A `eecb62e` (registro del Plan), C1 `4f6a3a4` (convención + registro + Trial), C2 `7434167` (corrección `<PLAN-114>:C-1`) y R2 (registros de cierre) en `dev`; V1 sobre C1 (4 citas rotas → `<PLAN-114>:F-1`), V2 sobre C2 (checkers PASS; pytest `1 failed / 523 passed` → `<PLAN-114>:F-2`) y revalidación A2 sobre el estado de cierre (checkers PASS; `python -m pytest tests/` canónico `524 passed`; registros de lineage `VALID`, `GAP=0`, `ANOMALY=0`; C-3 sin anomalías); resultado del Plan **`MVP IMPLEMENTED — VALUE PARTIALLY DEMONSTRATED`** (valor de la disciplina adversarial con procedencia declarada; independencia **no** demostrada: mismo ejecutor, N=1; pregunta 6 no observable); findings `<PLAN-114>:F-1`/`F-2` (partially-resolved) y `F-3` (deferred, owner: mantenedor, causa raíz de F-2: el ejemplo `F-01`/`C-01` de `docs/plans/_TEMPLATE.md` frente al contrato del checker C-3), correcciones `C-1`/`C-2` y dos pending decisions de `<PLAN-114>` (resolución de `<PLAN-105>` y promoción/obligatoriedad de la convención); status `Executed (parcial)` y condición derivada **no `Closed`** — la decisión humana es acto separado pendiente (Step 9/Step 12); sin `CHANGELOG` (reservado al cierre); sin push, sin merge, sin tag; `11.0.0` sigue sin release. **Cierre (2026-09-09):** el mantenedor registró las dos decisiones humanas como acto separado — (i) `<PLAN-105>` **no** se eleva a ADR en este momento (el Plan 105 permanece `Closed` y sin modificar) y (ii) la Working Convention queda **`KEEP AS WORKING / CONTINUE DOGFOODING`**: experimental/Working, **no** promovida a gobernanza, **no** obligatoria, **no** incorporada al Change Lifecycle ni al Protocol y sin Plan nuevo; crate R3 y validación de cierre: checkers PASS, `python -m pytest tests/` `524 passed`, gates C-1/C-2/C-3 `VALID` (`GAP=0`, `ANOMALY=0`; C-2 con `A2 (declared)`), `git status` limpio salvo `.codegraph/`; los **16** criterios de salida satisfechos (el 12 con el registro de la decisión humana) → status `Executed` y condición derivada **`Closed` (docs-only, sin release)**; ítem `(plan 114, —)` agregado a `CHANGELOG.md:[Unreleased]`; residual declarado y no bloqueante: `F-1`/`F-2` permanecen `partially-resolved` con sus correcciones aplicadas y revalidadas, y `F-3` permanece `deferred` (owner: mantenedor), fuera de este cierre; sin push, sin merge, sin tag; `11.0.0` sigue sin release. | active |

## Cuadragésima séptima serie: Change Lifecycle Protocol — Change Governance Artifact (Plan 115) (12 sep 2026)

Plan 115 (cambio de payload Clase A autorizado por el mantenedor, 2026-09-12,
GO registrado en las decisiones N1–N4 de Phase 5.4 Stage 1; RFC-76 `Accepted` +
plan `Aprobado para ejecución`): materializa el modelo del Change Governance
Artifact del Protocol (RFC-76) — contrato `CHANGE_GOVERNANCE.md`, registro en
taxonomía y boundaries, RFC/plan/INDEXes, changelog `[11.1.0]`, migración §14 y
`VERSION` `11.1.0`. Sin state machine, rol, registry, identity service,
predicate, cardinalidad ni maquinaria DEV; elementos diferidos explícitos
(namespace value, canonical representation, closure predicate, reflexive
bootstrap, Task↔Change cardinality, GC, physical location). Cambio MINOR.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `115-change-governance-artifact-materialization.md` | RFC-76 | Executed | Materialización del Change Governance Artifact: contrato `CHANGE_GOVERNANCE.md` + taxonomía + boundaries + RFC/plan/INDEXes + changelog `[11.1.0]`/`[11.2.0]` + migración §14/§15 + `VERSION` `11.1.0` → `11.2.0` + ancla semántica del runtime (`PROTOCOL_VERSION`) + runtime de referencia `runtime/toolcalls/change_governance.py` + `tests/test_change_governance.py`. Cambio MINOR (aditivo, dos rondas); sin state machine/rol/registry/identity service. **Cierre (2026-09-12):** commits de contenido `14e7fc4` (`11.1.0`) y `b8c6ce0` (`11.2.0`); Validation Anchor con Scoped Content Identity completa (State identity T1 `0fe88fdf…`; delta `d8036076…`, scope de 18 paths) y Checkpoint con revalidación A2; `check_lifecycle_anchor.py` → C-1 `VALID`, `check_lifecycle_checkpoint.py` → C-2 `VALID` (A2 declared), `check_lifecycle_lineage.py` → `GAP=0`/`ANOMALY=0`; status `Executed`; condición derivada **`Closed` (con release pendiente)**; finding `<PLAN-115>:F-1` `resolved` vía `<PLAN-115>:C-1` (superficie real de 18 paths y elementos DEFERRED resueltos por la ronda `11.2.0` con autorización RFC-76 D-01/D-02/D-03); sin tag (release `11.1.0`/`11.2.0` autorizado por el mantenedor el 2026-09-12 — `MINOR_CONFIRMATION = CONFIRMED` y `RELEASE_AUTHORIZATION = AUTHORIZED`, resolución PC-1 registrada en `<PLAN-116>` Escenario C y en la pending decision de este Plan); sin push, sin merge. | active |

## Cuadragésima octava serie: cierre del MVP de deliberación adversarial DEV — dogfood final A/B/C y evaluación del closure predicate (Plan 116) (12 sep 2026)

Plan 116 (cambio DEV docs-only autorizado por el mantenedor, 2026-09-12, GO
registrado como H1 en el plan vía las decisiones D-1/D-2 del prompt de Phase 2;
régimen RFC-75/RFC-69; sin RFC/ADR nuevo, clase RFC-56 —): ejecuta el dogfood
final del MVP de deliberación adversarial conforme a la Working Convention no
normativa (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`):
Tres Trials reales — Escenario A (decisión real con ejecutores diferenciados y
decisión humana observable), Escenario B (resultado legítimo NO CHANGE) y
Escenario C (camino no canónico con confrontación acotada) — con registros
embebidos, decisiones humanas como acto separado (o pendientes escaladas con
owner), validación por la batería canónica y los gates de lifecycle existentes,
y evaluación letra por letra del closure predicate `A ∧ B ∧ C ∧ D ∧ E ∧ F ∧ G
∧ H ∧ I` (contract / architecture / implementation / integration / validation
/ verification / dogfood / documentation / governance). Sin código, tool,
checker, registry, state machine, entidad global, RFC, ADR ni cambios de
plantillas. Sin cambios en `protocol/.agents/`, `runtime/`, `tools/`, `tests/`,
`.agents/`, `dist/`, `master` ni tags; sin `VERSION` bump ni tag (RFC-69).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `116-adversarial-deliberation-mvp-closure.md` | — | Executed | Cierre del MVP de deliberación adversarial DEV (Adversarial Deliberation MVP Closure): dogfood final A/B/C sobre decisiones reales registradas del repositorio conforme a la convención Working, decisiones humanas separadas, validación (batería + C-1/C-2/C-3) y evaluación del closure predicate A–I. **Creación (2026-09-12):** artifact creado con `Status` `Aprobado para ejecución` y GO del mantenedor registrado en el plan como H1 (decisiones D-1/D-2 del prompt de Phase 2). **Ejecución (2026-09-12):** Tres Trials reales — A: reconocimiento formal de `<PLAN-114>:F-1`/`F-2` con ejecutores diferenciados (agente principal + subagente de deliberación, compromiso antes de revelación, sin afirmación de independencia epistemológica), veredicto `NOT_VIABLE` sobre la candidata tal como enunciada; B: intervención sobre `<PLAN-114>:F-3`, veredicto `NOT_VIABLE` con **NO CHANGE registrado como resultado legítimo** (sin diffs); C: release batch de `11.1.0`/`11.2.0` con camino no canónico de **confrontación acotada (§7)** terminada por criterio de valor, veredicto `NOT_VIABLE` (K-4: confirmación del usuario para MINOR no registrada); decisiones humanas registradas como pendientes escaladas con owner (PC-1; `Trial Verdict ≠ Recommendation ≠ Human Decision`); corrección factual declarada del marco C (el batch `11.0.0`/`11.0.1` ya estaba promovido en `2dfb99f`); validación: batería canónica PASS (A1 tree `cf0358b0…`, delta `835bd6c6…`; A2 sobre el estado final), C-1 `VALID`, C-3 `VALID` (`GAP=0`, `ANOMALY=0`), C-2 pendiente del commit del mantenedor, pierna `pytest` con la clase ambiental preexistente de permisos del sandbox (sin fallos nuevos; los tests content-sensitive T27/estructura pasan); status `Executed`. **Human Checkpoint y cierre (2026-09-12):** el mantenedor aceptó el cierre (`D-1 = ACCEPT CLOSURE OF THE DEV ADVERSARIAL DELIBERATION MVP`; `D-2 = ACCEPT FINAL DOGFOOD A/B/C`) y el commit atómico de cierre materializó la condición derivada **`Closed` (docs-only, sin release)** con `JURY_TRIAL_CLOSED = A ∧ B ∧ C ∧ D ∧ E ∧ F ∧ G ∧ H ∧ I` satisfecho (predicate I PASS por aceptación humana + commit); las decisiones deliberadas (F-1/F-2, F-3, release `11.1.0`/`11.2.0`) permanecen pendientes con owner y no forman parte de este cierre; la convención sigue Working/no normativa; la feature Protocol-native queda FUTURE / NOT STARTED / OUT OF SCOPE; sin cambios en `protocol/.agents/`, `runtime/`, `tools/`, `tests/`, `.agents/`, plantillas ni `docs/CONVENTIONS.md`/`docs/VERSIONING.md`; sin RFC/ADR, sin `VERSION` bump, sin tag, sin push, sin merge. **Resolución de la decisión de release (2026-09-12, Phase 6):** el mantenedor registró como acto humano separado `MINOR_CONFIRMATION = CONFIRMED` para `11.0.1 → 11.1.0` y `11.1.0 → 11.2.0` (cierra `K-4`) y `RELEASE_AUTHORIZATION = AUTHORIZED` para promover el delta completo de `dev` a `master` con los tags anotados `11.1.0` y `11.2.0`; la resolución quedó registrada en la pending decision de Escenario C de este Plan, **solo autoriza** el release y no ejecuta promoción, tag, `dist` ni `master`; Plan 116 no se reabre (evidencia histórica de los Trials intacta). | active |

## Cuadragésima novena serie: adopción de la feature DEV de deliberación adversarial (Plan 117) (12 sep 2026)

Plan 117 (cambio DEV docs-only autorizado por el mantenedor, 2026-09-12, GO
registrado como H1 en el plan vía las decisiones D-1…D-8 del prompt de Phase 5;
régimen RFC-75/RFC-69; sin RFC/ADR nuevo, clase RFC-56 —): materializa la
adopción de la feature DEV de deliberación adversarial (`Adversarial
Deliberation`) especificada en Phase 4 —`DEFINITION-B` aceptada— como capability
**Working, no normativa, disponible y reutilizable**: definición final de la
feature, contrato de adopción (15 elementos), frontera de autoridad, contrato de
independencia y de valor, límites, evidencia (cuatro Trials reales en dos
Planes), limitaciones declaradas y predicate `JURY_TRIAL_DEV_FEATURE_CLOSED` con
C1–C8; cierra el `GAP-02` (regla de record home) en la convención con el mínimo
texto derivado de PC-1/LC-1; actualiza el banner de la convención y la fila de
`docs/working/proposals/INDEX.md` con el standing adoptado (descriptivo, sin
lifecycle state nuevo); registra el acto humano de cierre como decisión separada
y deriva `JURY_TRIAL_DEV_FEATURE_CLOSED` (docs-only, sin release). Sin código,
tool, checker, registry, state machine, entidad `Trial`, ID global, telemetría,
métricas, routing operacional, integración al Change Lifecycle, dogfood
adicional ni cambios de plantillas. Sin cambios en `protocol/.agents/`,
`runtime/`, `tools/`, `tests/`, `.agents/`, `ROADMAP.md`, `AGENTS.md`, `dist/`,
`master` ni tags; sin `VERSION` bump ni tag (RFC-69).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `117-adversarial-deliberation-feature-adoption.md` | — | Executed | Adopción de la feature DEV de deliberación adversarial (Adversarial Deliberation Feature Adoption): materializa el contrato de adopción de Phase 4 —`DEFINITION-B` aceptada— y el predicate `JURY_TRIAL_DEV_FEATURE_CLOSED` con C1–C8, cierra el `GAP-02` (record home) en la Working Convention con el mínimo texto derivado de PC-1/LC-1, declara el standing `ADOPTED + WORKING + NON-NORMATIVE` (sin lifecycle state nuevo) y registra la decisión humana de cierre como acto separado. **Creación (2026-09-12):** artifact creado con `Status` `Aprobado para ejecución` y GO del mantenedor registrado como H1 (decisiones D-1…D-8 del prompt de Phase 5). **Ejecución (2026-09-12):** definición final de la feature, contrato de adopción de 15 elementos, frontera de autoridad, contratos de independencia y de valor, evidencia (cuatro Trials reales en dos Planes, dos configuraciones de ejecutor, confrontación acotada, NO CHANGE y reconstruibilidad) y limitaciones declaradas; validación A1 (tree `56e4407f…`, delta `f725d0c0…`) y segunda validación sobre el estado staged de cierre con los 6 checkers canónicos PASS, C-1 Plan 117 `VALID`, C-2 Plan 117 `VALID`, C-3 `N/A` (ausencia declarada, con `GAP=0` y `ANOMALY=0`), los tests content-sensitive `2 passed` y la pierna `pytest` con la clase ambiental preexistente sin fallos nuevos; tabla C1–C8 verificada con evidencia y `JURY_TRIAL_DEV_FEATURE_CLOSED = TRUE` derivado (no declarado); condición derivada **`Closed` (docs-only, sin release)** con commit atómico `feat(dev): adopt adversarial deliberation as a reusable DEV capability (plan 117)`. Sin code, tool, checker, registry, state machine, entidad `Trial`, ID global, telemetría, métricas, routing operacional, integración al Change Lifecycle, dogfood adicional ni arquitectura nueva; sin cambios en `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `ROADMAP.md`, `AGENTS.md`, plantillas, `docs/CONVENTIONS.md` ni `docs/VERSIONING.md`; sin RFC/ADR, sin `VERSION` bump, sin tag, sin push, sin merge. | active |

## Quincuagésima serie: cierre del MVP de Change Lifecycle DEV — reconciliación normativa de RFC-75 (Plan 118) (13 sep 2026)

Plan 118 (cambio DEV docs-only autorizado por el mantenedor, 2026-09-13: cierre
del MVP de Change Lifecycle DEV materializando la decisión humana H-1 mediante el
Plan P-1; régimen RFC-75/RFC-69; clase RFC-56 B; sin RFC/ADR nuevo): reconcilia
normativamente RFC-75 con el estado real alcanzado por sus Incrementos 0–4, sin
rediseñarla. Registra en su `## Amendment Log` las cuatro materializaciones que
ningún plan había autorizado a registrar (Incremento 4 / Unidad D, plan 98; F-1
sobre la selección del anchor aplicable en C-2, plan 99; C-3 lineage checker,
plan 100; capa operacional `.agents/`, plan 101), corrige el header `**Status:**`
que declaraba implementación pendiente y marca los diez criterios de aceptación
con evidencia rastreable (`ruta:sección`, plan y commit). Registra en
`docs/VERSIONING.md:4.1 Batería canónica de verificación` los gates de lifecycle
C-1/C-2/C-3 como conjunto **adicional advisory/factual** (no se agregan al bloque
de comandos de la batería ni a CI). Sin cambios de mecanismos, invariantes ni
decisiones de RFC-75; sin cambios en `protocol/`, `runtime/`, `tools/`, `tests/`,
`dist/`, `master` ni tags; sin `VERSION` bump ni tag (RFC-69).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `118-change-lifecycle-dev-mvp-closure.md` | RFC-75 | Executed | Cierre del MVP de Change Lifecycle DEV (reconciliación normativa de RFC-75, H-1/P-1): registra en el `## Amendment Log` las cuatro materializaciones posteriores no registradas (Incremento 4 `669a576`/`9b5b8a1`/`0d2d7fd`/`aa68704`; F-1 `42da250`/`51cabb2`; C-3 `1ffe24c`/`d93d234`; capa `.agents/` `3706570`/`7bcda08`), corrige el header que declaraba implementación pendiente y marca los diez criterios de aceptación con evidencia rastreable. Registra C-1/C-2/C-3 como gates adicionales advisory/factuales en `docs/VERSIONING.md:4.1`. Diff limitado a header, `## Criterios de aceptación` y `## Amendment Log` de RFC-75, más la regla de §4.1: ningún mecanismo, invariante ni decisión cambia. Validación: batería canónica PASS, C-1 Plan 118 `VALID`, C-2 Plan 118 `VALID`, C-3 `N/A` (sin registros de lineage; `GAP=0`/`ANOMALY=0`), citas resolubles. Condición derivada **`Closed` (docs-only, sin release)**. Sin RFC/ADR, sin `VERSION` bump, sin tag, sin push, sin merge. | active |

## Quincuagésima primera serie: cierre del MVP de Change Lifecycle Protocol — H-3 (deferral de append/current/governance_position) (Plan 119) (13 sep 2026)

Plan 119 (cambio de payload autorizado por el mantenedor, 2026-09-13: cierre del
MVP de Change Lifecycle Protocol materializando la decisión humana H-3 = OPTION B
mediante el Plan P-2; RFC-76 `Accepted` + plan `Aprobado para ejecución`; clase
RFC-56 B; cambio MINOR 11.2.0 → 11.3.0): declara **DEFERRED** la operación de
**append**, la derivación de **current** y la derivación de **governance_position**
para el MVP, y reconcilia el contrato `CHANGE_GOVERNANCE.md` con el runtime
existente, que no implementa ninguna de las tres. El contrato incorpora
`## Implemented scope (MVP)` (qué está implementado: materialización, identidad
RFC-71, persistencia, estructura de colecciones como historia acumulada, registro
de decisiones/autorizaciones/cierre provisto por el llamador, reconstrucción por
recomputación de identidad y lectura) y `## Deferred semantics` (las tres
semánticas diferidas + invariante nuevo `CGA-010`), y precisa que "append-only"
describe la **forma** del artifact y no una operación disponible: la acumulación
posterior se realiza por **re-materialización completa con historia acumulada**,
que **no es append**. RFC-76 registra la decisión en su `## Amendment Log`, marca
sus criterios de aceptación distinguiendo diseñado / implementado / verificado /
dogfoodeado / diferido, y `docs/MIGRATION.md:16` documenta el cambio como
compatible. **Dogfood del Change Lifecycle Protocol:** el Change se gobernó con un
Change Governance Artifact (`target` = `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`)
materializado **antes** de la ejecución, con decisión y autorización registradas y
`closure_decision` incorporada por re-materialización completa. Sin runtime,
campos, endpoints, eventos, estados, métodos, state machine, registry, identity
service, gate ni checker nuevos; `runtime/toolcalls/change_governance.py` y
`tests/test_change_governance.py` sin cambios. Release pendiente (tag en la
promoción).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `119-change-lifecycle-protocol-mvp-closure-h3-deferral.md` | RFC-76 | Executed | Cierre del MVP de Change Lifecycle Protocol (H-3/P-2): declara DEFERRED append, current y governance_position; reconcilia `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` con el runtime (sección `## Implemented scope (MVP)` + `## Deferred semantics` + `CGA-010`); registra la decisión en el `## Amendment Log` de RFC-76 y actualiza sus criterios de aceptación; `VERSION` 11.3.0, `CHANGELOG.md` `[11.3.0]`, `docs/MIGRATION.md:16`. Dogfood real del Change Lifecycle Protocol con Change Governance Artifact materializado antes del Change. Sin implementar append/current/governance_position; sin runtime nuevo. Validación: batería canónica PASS, `tests/test_change_governance.py` verde, `CGA-001`…`CGA-010` verificados, C-1/C-2/C-3 sin `ANOMALY`. Condición derivada **`Closed` (con release pendiente)**. Sin tag, sin push, sin merge. | active |

## Quincuagésima segunda serie: MVP Protocol-native de deliberación adversarial (Plan 120) (14 sep 2026)

Plan 120 (cambio de payload autorizado por RFC-77 `Accepted`, 2026-09-14; clase
RFC-56 A; Change Level L2): materializa la capacidad
**`adversarial-deliberation`** definida por RFC-77 como composición de una
Skill nueva (`skills/adversarial-deliberation/SKILL.md`), una subsección de
comportamiento del Orchestrator existente, un contrato de artefacto nuevo
(`contracts/DELIBERATION_REPORT.md`, sesión-scoped e `informational`) y los
registros mínimos (taxonomía `kind: artifact` + `kind: contract`, boundaries,
inventario de skills, punto de decisión `D7`). La deliberación es
**evidencia**, nunca autoridad: su resultado es una `attestation` /
recomendación advisory, con procedencia declarada
(`ejecutores: mismo | distinto`) y **sin** afirmación de independencia
epistemológica. Sin entidad, `kind`, rol, perfil, fase, estado, lifecycle
state, authority class, registry, ID global, primitive de identidad, feature
flag, gate, clasificador automático, voting, confrontación, Prompt Cache ni
rediseño del Change Lifecycle nuevos. Dogfood real: el propio Change que
materializa la feature, gobernado por su Change Governance Artifact desde el
inicio. **Autorización de ejecución del Plan pendiente** (el Plan se crea en
`Aprobado para redacción`; su entregable es de implementación, por lo que su
`Status` de ejecución requiere autoridad humana). **[Estado corriente, Plan 145,
2026-09-21: esa autorización se otorgó y el Plan 120 está `Executed`; la frase
anterior se conserva como el estado de redacción y no describe el estado de hoy.]**

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `120-adversarial-deliberation-materialization.md` | RFC-77 | Executed | Materialización del MVP Protocol-native de deliberación adversarial: contrato `DELIBERATION_REPORT.md` (`enforcement: informational`, sesión-scoped, sin lifecycle propio), Skill `adversarial-deliberation` (con condiciones de uso para candidatura por juicio y consumidor declarado), subsección de invocación y construcción de contextos en el rol del Orchestrator (dos pasadas con contextos distintos, compromiso previo a la revelación, comparación por criterio, preservación del desacuerdo, síntesis, veredicto, recomendación advisory opcional, interpretación), punto de decisión `D7`, entidades de taxonomía y boundaries, suite `tests/test_adversarial_deliberation.py` (75 tests: contrato, skill, orquestación, autoridad, contexto y negativos) y el dogfood real del propio Change con reconstrucción por un tercero y evaluación `J1..J11`. Baseline: 6 checkers canónicos PASS y `pytest` **535 passed / 0 failed**; resultado: batería 6/6 PASS y `pytest` **610 passed / 0 failed** (sin regresiones). **H-5 (2026-09-14):** autorizado para ejecución, alcance limitado a los 14 entregables; clasificación MINOR `11.3.0` → `11.4.0` confirmada. **H-6 (2026-09-14):** cierre aceptado por el mantenedor — `JURY_TRIAL_PROTOCOL_MVP_CLOSED = TRUE` (J1..J10 verificados; J11 por acto humano), aceptando como limitación declarada del MVP el hallazgo de contaminación entre pasadas del dogfood (Pass 2 con exposición potencial al path del reporte vivo que ya contenía la conclusión de Pass 1), sin autorizar enforcement, aislamiento, diversidad de modelo/proveedor ni confrontación adicionales. Condición derivada **`Closed` (con release pendiente)**. Sin tag, sin push, sin merge. | active |

## Quincuagésima tercera serie: stable prefix provider-bound de Prompt Cache Protocol (Plan 121) (14 sep 2026)

Plan 121 (cambio de payload autorizado por RFC-78 `Accepted (plan 121,
2026-09-14)` — gate satisfecho; clase RFC-56 A; Change Level L3):
materializa el **stable prefix provider-bound** Core + Worker decidido por las
decisiones humanas HD-1b/HD-1b-bootstrap/HD-2b/HD-3/HD-4/HD-5/HD-6/HD-7
(mantenedor, 2026-09-14). Alcance: resolución determinística del contenido
estable (workflow module, role, profile, harness policy, skills, worker
bootstrap); `OrderingContract` v2 con el paso `protocol-bootstrap` declarado
vacío y el prefijo estable antes del sufijo dinámico; reconciliación
`ExecutionContext` ↔ Delegation Payload (cierra F-1); corrección de completitud
de la derivación de identidad **sin** tocar `session_uuid` ni el aislamiento; y
corrección de F-2. Objetivo declarado: **INFRASTRUCTURE / READINESS MVP**, no
ahorro económico. **Sin** provider real, **sin** Project/KB como prefijo, **sin**
identidad/registry/estado/fase/authority class/cache database nuevos, **sin**
evidencia de provider simulada y **sin** release. Origen:
`docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md` (Phase 1) y el Phase 2
Report (`PHASE_2_STOPPED_AT_AUTHORIZATION_GATE`). **Ejecutado (2026-09-14)** con
autorización humana explícita del mantenedor y alcance limitado a los
entregables; commit atómico pendiente de la acción del mantenedor, por lo que la
condición derivada es `Executed` y el cierre requiere ese commit. La
autorización **no** incluye release, tag, promoción a `master` ni publicación.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `121-provider-bound-stable-prefix-readiness-mvp.md` | RFC-78 | Executed | Materialización del stable prefix provider-bound Core + Worker (readiness MVP): `runtime/toolcalls/segment_resolution.py` nuevo (resolución determinística del contenido estable, regla de pertenencia, orden por contrato, `SegmentResolutionError` ante elemento irresoluble y rechazo de rutas que escapan de `.agents/`), `ORDERING_CONTRACT_V2` (`protocol-bootstrap` como step declarado y **vacío**; prefijo estable antes del sufijo dinámico; `ORDERING_CONTRACT_V1` conservado), composición *banner de identidad → región estable → ancla SCI → sufijo dinámico* para que `stable_prefix_bytes` sea prefijo de bytes e invariante a `session_uuid`/task/artefactos y `stable_region` sea el contenido reusable idéntico entre variantes, reconciliación `ExecutionContext` ↔ Delegation Payload por HD-7 (`harness_policy`/`profile`/`input_artifacts` como referencias; `communication_style`/`technical_approach` metadata de ejecución), `content_contract_version` en `MaterializationVersion` para que dos conjuntos de contenido nunca compartan una `MaterializationIdentity`, corrección de completitud de la derivación de identidad con `session_uuid` y aislamiento intactos (cierra **F-1**), corrección de **F-2** (test parametrizado sobre los diez campos del contexto entregado), sección «Stable prefix (provider-bound materialization)» en `CONTEXT.md`, bump MINOR `11.4.0` → `11.5.0` con ancla `PROTOCOL_VERSION` sincronizada, `CHANGELOG.md` `[11.5.0]` y `docs/MIGRATION.md` §18, y dogfood de los diez puntos verificables sobre el payload real. Verificación: seis checkers canónicos PASS (`check_protocol_invariants` 215 files / 10227 references) y `pytest` **704 passed / 4 failed** — los 4 son ajenos al cambio (3 verificados contra el baseline sin el cambio: `3 failed / 607 passed`; el cuarto es el informe de Phase 1 sin commitear, target de citas, que cierra al commitear). Validation Anchor A1 (delta `f6841e23…`; tree `8acfd149…`); `check_lifecycle_anchor`/`check_lifecycle_checkpoint` → Plan 121 `VALID`; `check_lifecycle_lineage` `GAP=0`. Condición derivada **`Closed` (con release pendiente)**; `Committed` es estado del repositorio y el commit atómico en `dev` es acción del mantenedor. **Sin release, sin tag, sin promoción a `master`, sin `dist`.** Beneficio económico `UNKNOWN`; evidencia de provider **DEFERRED / NOT VERIFICABLE**; `NullProviderAdapter` permanece. | active |

## Quincuagésima cuarta serie: DEV Autonomous Orchestrator MVP (Plan 122) (14 sep 2026)

Plan 122 (vía plan; sin efecto en `protocol/.agents/`, por lo que RFC-56 no
aplica; régimen aplicable RFC-75, cuya sección `Preguntas abiertas` declara la
orquestación/handoff **fuera de su alcance** — el Plan **no** modifica ni reabre
RFC-75 y **no** reclama ser su Incremento 5, que sigue `Deferred / Future
Track` por decisión de la propia RFC; Change Level L2): materializa el **MVP del
DEV Autonomous Orchestrator**, el mecanismo que conduce un Change de ARgentOS DEV
de principio a fin después de la autoridad humana inicial. Frontera humana
declarada: «el humano no opera el workflow; el humano es la autoridad». Las dos
piezas ausentes identificadas por la investigación de autonomía: **M1 —
Execution Host** (`runtime/orchestrator/host.py`: loop
`observe → derive → authorize → delegate → execute → ingest → verify → decide →
continue/stop`, stop conditions explícitas, recovery sin memoria conversacional)
y **M4 — Persistent Worker Result** (contrato persistente y reconstruible con
los doce campos exigidos y la relación inequívoca
`delegation → worker result → ingestion → next action`). El host se implementa
como mecanismo de **DEV/runtime/host**, no como extensión del Change Lifecycle
conceptual: la conducción se **deriva** del estado, Git, artifacts, evidence,
authority, gates aplicables, pending decisions y stop conditions, sin state
machine nueva, sin segunda representación persistente del estado, sin registry,
sin base de datos global y sin autoridad nueva. Relación DEV ↔ Protocol:
**conformance + reference** (el host se conforma a los contratos de
comportamiento del Protocol — Orchestrator, Worker, delegation, Execution
Context, context assembly, recovery, frontera de autoridad — sin importar ni
compartir sus mecanismos). Diferencias obligatorias preservadas: `GAP` no detiene
el loop si no es bloqueante; `ANOMALY`/`BOUNDARY` escalan; `exit code 0` nunca se
interpreta como workflow completo; C-1/C-2/C-3 se interpretan por su
clasificación real; una recomendación del Worker **nunca** es autorización.
Dogfood real: el host conduce la ejecución de este mismo Change (Plan 122) con
`run → stop → restart → reconstruct → continue`, derivando `Closed` cuando las
condiciones se satisfacen y deteniéndose ante toda decisión que requiera
autoridad humana, sin ejecutar release. Autorizado para ejecución por el
mantenedor (2026-09-14) como unidad única; la autorización **no** incluye
release, tag, promoción a `master` ni publicación.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `122-dev-autonomous-orchestrator-mvp.md` | — (vía plan; RFC-56 no aplica) | Executed | MVP del DEV Autonomous Orchestrator: paquete nuevo `runtime/orchestrator/` (`contracts.py` con vocabularios cerrados y el contrato M4 —doce campos, validación, serialización determinista, `recommended_next_action` advisory ≠ autoridad—; `store.py` persistente append-only en `.project/orchestrator/` con escritura atómica y lecturas fail-closed; `observation.py` read-only del Change; `authority.py` con veredictos `AUTHORIZED_EXISTING`/`REQUIRES_HUMAN`/`FORBIDDEN` y release prohibido; `derivation.py` sin `next_state` persistido; `worker.py` con `CommandWorker` real que clasifica por señal y no por exit code; `governance.py` escritor mecánico acotado por sección e idempotente; `host.py` M1 con stop conditions y recovery; `__main__.py` CLI), suite determinista `tests/test_autonomous_orchestrator.py`, sección del host en `runtime/README.md`, policy operacional `.agents/policies/autonomous-orchestration.md`, y registro verbatim del dogfood real en `docs/working/audits/`. Sin payload, sin `VERSION`, sin tag, sin promoción, sin commit. **Ejecutado
(2026-09-14)** con autorización humana explícita del mantenedor y alcance
limitado a los entregables: el dogfood real condujo 19 iteraciones en cuatro
corridas del host (`run-01` validación + detección del defecto real
`<PLAN-122>:F-1`; `run-02` detención en `STOP_OPEN_FINDINGS` por autoridad
humana; `run-03` reanudación desde evidencia, revalidación A2 y `CLOSED_DERIVED`
tras la resolución humana del finding; `run-04` revalidación A2 que cubre el
registro durable del dogfood), sin que el humano transportara resultados entre
iteraciones. Verificación: seis checkers canónicos PASS, suite nueva **25
passed**, C-1 `VALID` / C-2 `VALID` con A2 / C-3 `VALID`; la pierna
`python -m pytest tests/` queda como **GAP** por clase ambiental declarada
(sandbox sin mecánica de directorios temporales de pytest), nunca como `PASS`.
Validation Anchor A1 + revalidaciones A2 (última delta `97d79196…`, tree
`a640c483…`). Condición derivada **`Closed` (con release pendiente)**; el commit
atómico consolidado de los Planes 122 + 123 se realizó como acción de repositorio
autorizada por el mantenedor (2026-09-15), identificado por su mensaje
(auto-referencia: el árbol no embebe su propia identidad), con revalidación A2
sobre el estado consolidado (delta `2de38ad8…`, tree `8576dea2…`). Sin release,
sin tag, sin promoción a `master`, sin `dist`. | active |

## Quincuagésima quinta serie: MVP del DEV Agent Worker (Plan 123) (15 sep 2026)

Plan 123 (vía plan; sin efecto en `protocol/.agents/`, por lo que RFC-56 no
aplica; régimen aplicable RFC-75, que declara la orquestación/handoff **fuera de
su alcance** — el Plan **no** modifica ni reabre RFC-75 y **no** reclama ser su
Incremento 5; Change Level L2): materializa el **MVP del DEV Agent Worker**, una
tercera implementación de la frontera `WorkerAdapter` que ya existe (junto a
`CommandWorker` y `NullWorker`), sin segunda arquitectura, sin state machine, sin
registry, sin `state.json` y sin autoridad nueva. Decisión humana H-1 consumida:
`AgentInvoker` = **protocolo inyectable + `NullAgentInvoker` por defecto** — sin
proveedor real, sin modelo, sin API keys, sin credenciales, sin red y sin
dependencia de servicios externos. El Worker recibe una `Delegation` válida
(extendida de forma **aditiva-optional** con `task` e `input_artifacts`),
reconstruye el `ExecutionContext` que el host entregó reutilizando
`runtime/toolcalls/context.py` y `render_prompt`, observa el repositorio por
contenido (no por claim), ejecuta la verificación externa declarada con
`worker.classify`, se corrige dentro de su autoridad y produce **exactamente un**
`WorkerResult` (contrato M4 intacto: `claims.self_reported_completion = false`,
`recommended_next_action` advisory con `action: None`). El host extiende la
derivación con `RUN_IMPLEMENTATION_TASK` (antes de la validación, para no validar
un estado que la implementación va a cambiar) y agrega **verificación de scope
determinista y externa al Worker** (`artifacts_modified ⊄ declared_scope` ⇒
`STOP_FORBIDDEN_ACTION` + `REQUIRES_HUMAN`). Dogfood real: el Agent Worker ejecuta
trabajo real del repositorio (endurecimiento del camino de recuperación del
propio host: el journal declara las líneas que no puede leer en vez de
descartarlas en silencio), con transcript persistido, `WorkerResult` persistido,
ingestión, verificación y reconstrucción por un tercero. Hallazgos reales
detectados por el dogfood y corregidos bajo la autorización del Plan:
`<PLAN-123>:F-01` (paths untracked no contaban como no committeados en
`_committed`), `<PLAN-123>:F-02` (una modificación del Worker a un path ya sucio
era invisible: la observación pasa a comparar **snapshots de contenido**),
`<PLAN-123>:F-03` (un resultado de implementación que no cambia nada en el estado
actual se re-derivaba indefinidamente), `<PLAN-123>:F-04` (tres defectos de los
registros de gobernanza: Plan equivocado en el anchor, idempotencia vacua de la
revalidación y auto-referencia del artefacto de gobernanza en la identidad de
contenido validada). Los cuatro hallazgos fueron **aceptados formalmente como
`resolved` por el mantenedor (2026-09-15)** sobre la base de las correcciones
`<PLAN-123>:C-1`..`C-4`, su evidencia y el lineage verificado, autorizando al
Orchestrator a continuar con la derivación del Change. Sin payload, sin `VERSION`,
sin tag, sin promoción; commit atómico consolidado de los Planes 122 + 123
(2026-09-15), identificado por su mensaje.

| Plan | RFC | Status | Descripción | active |
|---|---|---|---|---|
| `123-dev-agent-worker-mvp.md` | — (vía plan; RFC-56 no aplica) | Executed | MVP del DEV Agent Worker: `runtime/orchestrator/agent_worker.py` (**nuevo**: `AgentWorker` como implementación de `WorkerAdapter`, `AgentInvoker` protocolo inyectable, `NullAgentInvoker` default honesto con los tres resultados distinguibles —no disponible / incompleta / completada—, `AgentInvocationRequest`/`AgentInvocationResult` y `agent_invoker_from_environment()`), `contracts.py` (`Delegation.task`/`Delegation.input_artifacts` aditivos-optional + `RUN_IMPLEMENTATION_TASK` en el vocabulario cerrado de acciones ejecutables), `observation.py` (`parse_agent_task` para la sección `## Delegación agentiva`, `implementation_done_for_current_state`, `implementation_already_satisfied` y declaración de `GAP` para líneas de journal ilegibles), `derivation.py` (regla de implementación antes de la validación + `forbidden_scope_action`), `authority.py` (basis del Plan aprobado, sin autoridad nueva), `host.py` (Delegation agentiva, verificación de scope por snapshots de contenido, `_committed` que reconoce untracked, observabilidad del Worker Result), `worker.py` (`repository_snapshot`/`changed_paths`/`content_digests` compartidos), `store.py` (`read_journal_with_gaps` + `JournalRead`), `__main__.py` (`--worker agent`), suite determinista `tests/test_agent_worker.py`, sección del Agent Worker en `runtime/README.md`, policy `.agents/policies/autonomous-orchestration.md` y sección `## Delegación agentiva` documentada en `docs/plans/_TEMPLATE.md`. Sin payload, sin `VERSION`, sin tag, sin promoción; `**Status:** Executed` con condición derivada **`Closed`** (release pendiente), Validation Anchor A1 + revalidación A2 sobre el estado consolidado (delta `a33816da…`, tree `8576dea2…`), y hallazgos `<PLAN-123>:F-1`..`F-4` aceptados formalmente como `resolved` por el mantenedor (2026-09-15) sobre la base de `<PLAN-123>:C-1`..`C-4`. | active |

## Nonagésima octava serie: implementación de las correcciones de cierre de Priority 0.3 (Plan 171) (20 oct 2026)

Serie de un único Change DEV **Clase B** que materializa el contrato acotado de Priority 0.3: corrección local de `INV-07` y del vocabulario de enforcement, reconciliación del registro derivado de `docs/plans/INDEX.md`, registro post-close de las inconsistencias de 157/158 y de los findings `open` de 155/158/168/169, extensión de `check_plan_structure.py`, `check_lifecycle_lineage.py` y `check_invariants_equivalence.py`, incorporación de la equivalencia canónica al CI, tests positivos/negativos y una entrada de `CHANGELOG.md` sólo en `[Unreleased]` con el guard N-9. **No** toca `protocol/`, `runtime/` ni `dist/`, no crea invariantes, properties, gates, estados ni registries, y **no** implementa G-06, G-07, DEV Memory ni garantías semánticas/epistémicas. **Ejecutado y cerrado** (commit `0bcce23`; `**Status:** Executed` con condición derivada `Closed`, Validation Anchor y Checkpoint registrados; DEV-only sin release, RFC-69). El registro anterior de este INDEX decía «el Plan queda en `Aprobado para redacción` … no se ejecutó ni se cerró en la sesión de planificación»: describía el estado de planificación y quedó desactualizado al ejecutarse el Plan (corregido en Phase 0.4; el plan cerrado no se editó).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `171-priority-0-3-closure-implementation.md` | — (vía plan; DEV-only; RFC-56 no aplica) | Executed | **Implementación acotada de las correcciones de cierre de Priority 0.3.** Corrige `docs/INVARIANTS.md` (INV-07, vocabulario `session-hook`, estado de gaps), la fila del Plan 169 en el INDEX y crea el registro post-close de 157/158 y 155/158/168/169; extiende los tres checkers con reglas deterministas y tests; añade la equivalencia canónica al CI; actualiza `CHANGELOG.md` sólo en `[Unreleased]` con N-9. **11 AC · 9 N**; `DETECT` de FM-13 acotado a referencias DEV/Protocol y bloque canónico, no a duplicación semántica general. **Ejecutado y cerrado** (condición derivada `Closed`; DEV-only, sin release). | active |

## Nonagésima novena serie: cierre de la deuda heredada de Phase 0 (Phase 0.4, Plan 172) (20 oct 2026)

Change DEV **Clase B** que cierra la deuda heredada de Phase 0.1, 0.2 y 0.3: inventario completo con estado terminal por ítem (`RESOLVED`, `IMPLEMENTED`, `REJECTED_BY_DESIGN`, `ACCEPTED_RESIDUAL_RISK`, `NON_ACTIONABLE_HISTORICAL`), materialización de `E1-G2`…`E1-G5` de ADR-20 (autoridad de escritura derivada y verificada, distinción `Executed`/`Closed`, enforcement de cierre en los escritores y registro externo de ejecución separado), corrección del falso positivo de path legacy del checker de citas y de la resolución de headings numerados, reconciliación de `docs/VERSIONING.md` §9, `docs/plans/INDEX.md` y `docs/working/proposals/INDEX.md`, y registro del Amendment Log de ADR-20. **No** toca `protocol/`, `runtime/` ajeno al orquestador, `dist/` ni ningún plan/RFC/ADR cerrado en su contenido gobernante; sin release (RFC-69). Inventario y rationale: `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md`.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `172-phase-0-4-closure-implementation.md` | — (vía plan; DEV-only; RFC-56 no aplica) | Executed | **Cierre definitivo de la deuda heredada de Phase 0.** Inventario de los residuos de 0.1/0.2/0.3 con estado terminal y evidencia; implementa `E1-G2`, `E1-G3`, `E1-G4` y `E1-G5`; clasifica `G-04`, `G-07` y `G-08` como riesgo residual aceptado y `G-03`/`G-06` como rechazados por diseño; resuelve `D-0.3-12` como riesgo residual aceptado y `D-0.3-23` como rechazado por diseño; corrige los registros derivados desactualizados; 25 citas históricas rotas clasificadas como no accionables. Sin cambios de protocolo, runtime ajeno al orquestador ni `dist`. | active |

## Centésima serie: corrección del cierre de Phase 0.4 (Plan 173) (21 oct 2026)

Change DEV **Clase B** (+ sub-cambio **Clase C** tests-only del payload) que corrige la clausura inválida detectada por la auditoría adversarial de `f77cd3f`: los 9 ítems `MISCLASSIFIED` y los 2 `INSUFFICIENT_EVIDENCE` del inventario de Phase 0.4 pasan a estado terminal genuino —R5 de C-2 para la detección post-close no commiteada, INDEX→archivo en `check_plan_structure`, checker de declaraciones `ENF-001`…`ENF-003` en la batería y CI, tres tests de idempotencia del lifecycle (Clase C, sin `VERSION` ni tag) y reconciliación completa de `docs/VERSIONING.md` §9—, mientras los 22 residual risks genuinos se preservan sin cambios. Registra la corrección post-close de la identidad del Plan 172 por referencia (el Plan 172 no se edita) y las 18 iteraciones/hallazgos teóricos en `docs/working/proposals/PHASE_0_4_CLOSURE_CORRECTION_THEORY_2026-10-21.md`. Publicada en `12.3.1` (tag anotado sobre `master`; promovida desde `dev`).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `173-phase-0-4-closure-correction.md` | — (vía plan; DEV-only + Clase C tests-only; RFC-56 no aplica) | Executed | **Corrección del cierre inválido de Phase 0.4.** Implementa los 9 ítems reclasificados y corrige los 2 con evidencia insuficiente; preserva los 22 residual risks genuinos; corrige la identidad de cierre del Plan 172 por referencia; deja `MISCLASSIFIED = 0`, `INSUFFICIENT_EVIDENCE = 0`, `REAL_UNCLOSED_DEBT = 0`. El sub-cambio Clase C (tests del payload) se publicó en `12.3.1` (tag anotado; `dist` regenerada por CI). | active |

## Plan 176 — Theoretical Execution (DEV complete) (24 oct 2026)

Plan ejecutado que **cierra TE en DEV como capacidad integral**, sin tocar `protocol/`.
Reconstruye de forma independiente el alcance completo (historia, exclusiones de v1,
fronteras permanentes y áreas de otros componentes), lo registra con marcas
`FACT`/`INFERENCE`/`DECISION`, lo contrasta contra el árbol real en una matriz A–Q y
ejecuta el delta `REQUIRED` `D-1`…`D-7`: CH-3/CH-7 pasan a ser funciones del commit base
(no del working tree ni del índice), `TE_RESULT` schema 2 registra todos los checks y
`--validate` los re-deriva (un finding del engine ya no puede desaparecer), el fingerprint
de no-progress se verifica e incluye los checks, la etiqueta de corrida es determinista,
CH-9 detecta declaraciones de entregables irresolubles/escapadas y clases de efecto fuera
del vocabulario cerrado, y se versionan schema/tool/check-set. **RFC-56 Class: N/A** (sin
payload delta), Change Level L2, DEV-only; **sin cambios** en `protocol/`, `dist/`,
`VERSION`, `ExecutionHost` ni la batería canónica; **sin release** (RFC-69). Registra el
Gate TE del propio Plan 176 (productor + engine), la revisión adversarial de los diez
ataques y la corrección **por referencia** de la fila desactualizada del Plan 175 en este
INDEX.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `176-theoretical-execution-dev-complete.md` | — (vía plan; RFC-56 N/A) | Executed | **Theoretical Execution (TE) DEV complete.** Definición operativa de TE DEV COMPLETE, matriz de gaps A–Q con clasificación (`REQUIRED`/`OPTIONAL`/`OUT_OF_SCOPE_PERMANENT`/`OWNED_BY_OTHER_COMPONENT`/`DEFERRED`) y registro de exclusiones con razón verificable; delta implementado: determinismo de checks sobre la base, registro `checks[]` con re-derivación en `--validate`, fingerprint de no-progress verificado, identidad de corrida determinista, CH-9 de integridad de declaración y versionado del contrato. Sin payload, sin host, sin persistencia propia, sin release. | active |

## Plan 175 — Theoretical Execution (DEV v1) (24 oct 2026)

Plan ejecutado que implementa TE v1 exclusivamente en DEV: el engine
determinista (`runtime/theoretical/`: `DeclaredOverlay`, `InputIdentity`/`RunIdentity`, enumeración
de ítems, CH-1…CH-8, contrato, validación, `status` derivado, staleness y CLI `--emit/--validate/
--stale/--compare`), la policy operativa que define las dimensiones semánticas del productor y el
Gate B (productor + engine), y la suite de tests. **RFC-56 Class: N/A** (sin payload delta),
Change Level L2, DEV-only; **sin cambios** en `protocol/`, `dist/`, `VERSION`, `ExecutionHost`, la
batería ni el Protocol; **sin release** (RFC-69). El Plan resuelve tres ambigüedades del diseño:
Gate B no atribuye dimensiones semánticas al engine, la precedencia de `status` es única y
`--compare` no confunde divergencia con resolución. TE y autorización de ejecución
registradas; Gate B `CONVERGED`; cierre en curso (Validation Anchor/Checkpoint).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `175-theoretical-execution-dev-v1.md` | — (vía plan; RFC-56 N/A) | Executed | **Theoretical Execution (TE) DEV v1.** Engine determinista sobre un `DeclaredOverlay` de un Plan commiteado: enumeración, CH-1…CH-8, contrato `TE_RESULT` con `status` derivado, identidades `InputIdentity`/`RunIdentity`, obligaciones de verificación y CLI sin escritura. Dimensiones semánticas a cargo del productor; Gate B = productor + engine; `--compare` solo reporta diferencias observadas. Sin payload, sin host, sin persistencia, sin release. | active |

## Centésima primera serie: materialización y cierre del modelo RFC-56 / A-B-C (Plan 174) (23 oct 2026)

Change DEV **RFC-56 Class: N/A** (sin payload delta, docs-only) que materializa el modelo
conceptual ya resuelto de RFC-56 y del modelo A/B/C: la clasificación pertenece al **payload
delta** y no al Change, al Plan ni al documento que lo describe; un Change puede contener varios
deltas con clases distintas y su ruta efectiva la fija la **clase más estricta** presente
(`A > B > C > N/A`, sin clase `AB`); un Change sin efecto payload es **RFC-56 N/A**; **Class C**
es la transformación mecánica que preserva la semántica normativa y los contratos del payload, y
el checker es **evidencia factual, no autoridad**. Se enmienda `docs/rfc/56-governance-fast-track.md`
con el texto original conservado como registro histórico, y se alinean `docs/CONVENTIONS.md`,
`docs/plans/_TEMPLATE.md` (campo `**RFC-56 Class:**`, separado de `**Change Level:**`),
`docs/VERSIONING.md`, `AGENTS.md`, `.agents/AGENTS.md`, `.agents/workflows/change-lifecycle.md` y
`.agents/policies/validation-closure.md`; se elimina la formulación «todo payload touch →
Plan + RFC-56», que contradecía Class C. **TE** pre y post materialización sobre T1–T15 y
auditoría global de usos con los artefactos históricos preservados (RFC-46). **Sin cambios** en
`protocol/`, `runtime/`, `tools/`, `tests/`, `VERSION` ni `dist`; **sin release** (RFC-69).
Cierre registrado (`Closed`): Validation Anchor y Checkpoint GC-1.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `174-rfc56-payload-delta-model-materialization.md` | RFC-56 (enmienda; `N/A` como Change: sin payload delta) | Executed | **Materialización y cierre de Priority 3 — modelo RFC-56 / A-B-C.** Precisa la unidad de clasificación (payload delta), Class C por preservación semántica y de contratos, el checker como evidencia y no autoridad, los Changes multi-clase y la ruta efectiva por clase más estricta, `RFC-56 N/A` y la independencia respecto del Change Level; alinea RFC-56, CONVENTIONS, el template de Plan, VERSIONING y la capa operativa DEV; TE T1–T15, auditoría global y batería completa. **Sin payload, sin release.** | active |

## Centésima segunda serie: auditoría de continuidad de integración y coherencia evolutiva (Plan 178) (24 oct 2026; ejecutada 25 oct 2026)

Nueva serie de auditoría de Priority 3.6. El Plan 178 reconstruye la superficie de integración de las capacidades evolucionadas recientemente y distingue integración real, integración parcial, aislamiento deliberado, consumer diferido y evidencia desconocida. **Ejecutado el 2026-10-25 sobre `dev` @ `759f005`**: 16 capacidades auditadas (9 `INTEGRATED`, 2 `PARTIALLY_INTEGRATED`, 5 `INTENTIONALLY_ISOLATED`, 0 `ORPHANED`, 0 `CONFLICTING`), cada fila con camino de consumidor o frontera declarada y verificación; las dos parciales son **Memory** (seam `AgentWorker.memory_store` sin call site que lo suministre; RFC-80 Protocol `NOT IMPLEMENTED`) y **Change Governance Artifact** (materializador DEV sólo consumido por tests; `append`/`current`/`governance_position` diferidos). Confirma múltiples fronteras deliberadas —TE, Placement, DEV Skills, DEV Adversarial Deliberation y Architecture Evolution—. El gap preventivo principal es la ausencia de una `Integration Surface` declarativa en el template de Implementation Plans y de una taxonomía transversal de integración; **no se autoriza ni implementa ningún mecanismo**, y las reparaciones quedan fuera de alcance. La auditoría fue DEV-only, sin payload, sin release y sin cambios en `runtime/`; la validación dinámica (batería canónica + `pytest tests/` 1535 passed) se ejecutó en este repositorio. Hallazgos F-01/F-02/F-03 abiertos/deferred con dueño mantenedor. El 2026-10-25 el Plan fue renumerado de `177` a `178` al integrarse la divergencia `dev`/`origin/dev`: el número `177` corresponde al Plan del README, ya cerrado (`<PLAN-178>:C-1`).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `178-integration-continuity-audit.md` | — | Executed | **Auditoría de Priority 3.6 — continuidad de integración (ejecutada).** Inventario y clasificación con evidencia de consumidor de Discovery, Knowledge Lifecycle, Memory, Architecture Evolution, Skills, Autonomous Orchestrator, SAE, F-C, Adversarial Deliberation, Theoretical Execution, Placement, Change Lifecycle y RFC-56 A/B/C: 9 integradas, 2 parciales, 5 aisladas deliberadamente, 0 huérfanas, 0 conflictivas. Evaluación de la hipótesis y límites de evidencia declarados; findings F-01/F-02/F-03 abiertos/deferred. **Sin cambios en payload/runtime/tools/tests; sin release.** Renumerado desde `177` (`<PLAN-178>:C-1`); Validation Anchor y Checkpoint registrados en el Plan. | active |

## Nonagésima séptima serie: catálogo canónico de invariantes y properties transversales (Plan 170) (20 oct 2026)

Serie del Change que cierra Priority 0.2 en su fase de gobierno y materialización documental, **sin
implementar enforcement**. El diseño repository-backed había producido un catálogo de **15 entradas**
—**12 invariantes fundamentales** y **3 properties**— y una consecuencia que el repositorio no podía
resolver por sí mismo: el payload no puede citar `docs/`, de modo que una representación propia del
catálogo en el Protocol exigía una **segunda excepción aprobada** a `Single-source documentation
policy`. **RFC-84** (`Accepted` el 2026-10-20, Clase A de RFC-56) autoriza esa excepción **única y
acotada**: se duplica sólo el **bloque canónico** —`ID`, `NAME`, `FORMULATION`, `SCOPE`,
`OUT_OF_SCOPE`, `ENFORCEMENT_STATUS`, `LIMIT`— delimitado por los marcadores
`canonical-invariants-v1`, y las dos copias deben ser **idénticas byte a byte**; los campos fuera del
bloque —interpretación de dominio, mecanismos, verificación, límites locales— no se comparan y son la
parte que legítimamente difiere. Ninguna copia es autoridad de la otra y la definición común pertenece
a la decisión registrada en la RFC, de modo que **no hay dos autoridades semánticas**. Antes de
aceptar se normalizó la clasificación de enforcement —vocabulario cerrado de seis dimensiones y
recuento único **6/15 `ENFORCED`**, 2/15 `VALIDATED`, 7/15 `NONE`— y se corrigió el alcance de
«invariantes fundamentales» a «invariantes y properties», porque el bloque contiene tres properties.
La materialización añade `docs/INVARIANTS.md` (Policy DEV) y
`protocol/.agents/standards/INVARIANTS.md` (estándar del payload, autocontenido), registra la
excepción en `PROTOCOL_BOUNDARIES.md` y avanza el payload a **`12.2.0`** (MINOR: adición
compatible). **No implementa los 12 gaps de enforcement** —`E1-G1`…`E1-G5`, `G-03`…`G-09`—, que
quedan documentados con su propia vía de autorización.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `170-materialize-canonical-invariants-catalog.md` | RFC-84 (Clase A; **`Accepted`** 2026-10-20) | Executed | **Materialización del catálogo canónico de invariantes y properties transversales.** Bloque canónico de 15 entradas (12 invariantes + 3 properties) en `docs/INVARIANTS.md` y `protocol/.agents/standards/INVARIANTS.md` con equivalencia **byte a byte**, interpretación de dominio por entrada, `ENFORCEMENT_STATUS` y `LIMIT` obligatorios; segunda excepción aprobada en `PROTOCOL_BOUNDARIES.md` con sus cuatro condiciones; payload a `12.2.0`. **No implementa gaps de enforcement.** Cierre registrado (`Closed`): Validation Anchor y Checkpoint con `PC-1` resuelto. | active |

## Nonagésima sexta serie: regularización de `81bbde1` y reconciliación de pending decisions cerradas (Plan 169) (14 oct 2026)

Serie del Change que cierra los dos puntos accionables del inventario de pendientes **sin reescribir
nada publicado**. **Punto 1:** el commit `81bbde1` (`perf(runtime): reuse run() observation in
iterate`) modificó `runtime/orchestrator/host.py` y se publicó en `master` y en el tag `12.1.0`
**sin artefacto de autorización** —su propio mensaje declara el hueco—; el Plan lo **regulariza por
referencia**, con el informe del piloto como evidencia, y **no** lo reescribe ni le atribuye una
autorización ficticia. Su falta de entrada en el changelog **no** es defecto: `docs/VERSIONING.md`
§2 ata el changelog a los cambios de `protocol/.agents/` y ese commit no toca el payload.
**Punto 2:** tres planes **cerrados** (161, 164 y 165) registran **siete** decisiones como `PENDING`
ya resueltas por actos y planes posteriores (`ID-1`, `ID-3`, `ID-5`, `ID-6` e `ID-8` del 165; la
revisión de alcance de `F-C`/Etapa B del 161; las decisiones de implementación de `F-C` del 164),
de modo que su lectura actual muestra como pendiente lo que está cerrado: es un defecto de
**registro**, no semántico (los checkers dan `ANOMALY=0`), y se reconcilia **por referencia** sin
editar los artefactos cerrados. **Decisión de fondo registrada y resuelta** por el acto del
mantenedor del 2026-10-14: una **instrucción directa del mantenedor autoriza** el cambio que
nombra; su declaración pertenece al primer artefacto del cambio —el **mensaje del commit** cuando
no hay plan (RFC-75 Mecanismo 1)— y debe nombrar la vía y el alcance; y la aclaración se escribe en
`.agents/AGENTS.md` **dentro de la regla de autorización existente**, sin crear autoridad, estado,
excepción ni mecanismo nuevos. **Clase B** de RFC-56 (DEV-only y docs-only, sin efecto de payload;
si tocara `protocol/.agents/` sería Clase A), `Change Level` **L2**, sin release. Fuera de alcance:
reescribir `81bbde1`, el tag `12.1.0` o cualquier historia publicada; editar los planes cerrados; el
`GAP` **advisory** del Plan 116 (un `GAP` no es una invalidación); el documento de investigación
`docs/planificacion-argentos-diseno-2026-10-13.md` (decisión del mantenedor ya tomada); y Etapa C
(trabajo futuro, no deuda).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `169-regularizacion-de-81bbde1-y-reconciliacion-de-pendientes.md` | — (vía plan; **Clase B** de RFC-56; Clase A sólo si tocara `protocol/.agents/`) | Executed | **Regularización de `81bbde1` y reconciliación de pending decisions cerradas.** `Change Level` **L2** (`max(coordination=2, scope=2, architectural impact=0, release impact=0, duration/complexity=2)`). **`IN SCOPE`**: regularización **por referencia** de `81bbde1` con su finding y su evidencia; reconciliación **por referencia** de las siete pending obsoletas con el artefacto que resolvió cada una; registro de la decisión de fondo y su aclaración en `.agents/AGENTS.md`; y los registros de este Plan. `OUT OF SCOPE`: reescribir `81bbde1`, el tag `12.1.0`, `master` o cualquier historia publicada; editar los planes 161/164/165/166/167/168 cerrados; el `GAP` del Plan 116; el documento de investigación; Etapa C; y `protocol/.agents/`, `dist/`, `runtime/`, `tools/`, `tests/`. Findings `F-1` (`81bbde1` sin artefacto de autorización) y `F-2` (siete pending obsoletas en planes cerrados). Pending: vía de autorización de la acción directa, **`RESUELTA`** por el acto del 2026-10-14 con las tres afirmaciones. `## Delegación agentiva` sin `**Task:**` y `## Efectos declarados` con la fila negativa. `## Validation anchor` y `## Checkpoint / cierre` **vacíos**: el Plan se crea sin ejecutar y **no** declara condición derivada. | active |

## Nonagésima quinta serie: release `12.1.0` — absorción de `12.0.1` y publicación del payload de RFC-83 (Plan 168) (14 oct 2026)

Serie del Change que **publica** el estado verificado de `dev` como release **`12.1.0`**. Nace de
la decisión del mantenedor (2026-10-14) que resuelve el ítem de reconciliación de versión y adopta
la vía **A1**: **una sola release que absorbe el `12.0.1` no publicado**. El problema que corrige es
de clasificación y de trazabilidad: el Plan 156 asignó `12.0.1` (PATCH documental del payload) y
quedó `Closed` con `Released = FALSE` —su número nunca se publicó—, mientras que el Plan 166
modificó `protocol/.agents/contracts/` con la relación `Objective` multi-Change y la procedencia
declarada del actor **sin producir la versión propia** que `docs/VERSIONING.md` §3 exige («un plan
= una versión = un tag»), dejando ese payload apoyado sobre el `12.0.1` ajeno. Publicarlo como
`12.0.1` sería un PATCH transportando contenido **MINOR**; por eso la release se numera **`12.1.0`**
(§3: adiciones compatibles ⇒ MINOR, calculada desde la última versión publicada en `master`,
`12.0.0`), con la absorción de `12.0.1` declarada en el changelog. **No hay RFC**: el payload que
se publica no se modifica —sus dos cambios ya fueron autorizados por RFC-82 `Accepted` (Plan 156) y
RFC-83 `Accepted` (Plan 166)— y lo que se decide es metadata de release; la única escritura bajo
`protocol/` es `protocol/.agents/VERSION`. **DEV-only + payload de release**, `Change Level` **L2**
con `release impact` **3**. Alcance: sección `[12.1.0]` del changelog con los ítems de payload de
ambos planes, bump de `VERSION` y de `PROTOCOL_VERSION`, snapshot de `docs/VERSIONING.md` §9,
posición actual de `ROADMAP.md`, y **promoción fast-forward `dev` → `master` con tag anotado
`12.1.0`**, autorizada dentro del Plan y **condicionada a que la verificación salga íntegramente en
verde**. Fuera de alcance: modificar contenido de `protocol/.agents/` distinto de `VERSION`, editar
`dist/`, reabrir los planes 156/166/167, reescribir secciones publicadas del changelog y la
**publicación remota** (`push` + `publish-dist` en CI), registrada como pending decision con owner
mantenedor por efecto `remote_git` no declarado.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `168-release-12-1-0.md` | — (vía plan; el payload publicado ya está autorizado por RFC-82 y RFC-83; sólo se escribe `protocol/.agents/VERSION`) | Executed | **Release `12.1.0`: absorción de `12.0.1` y publicación del payload de RFC-83.** Publica el estado verificado de `dev` en `master` con tag anotado. `Change Level` **L2** (`max(coordination=2, scope=2, architectural impact=0, release impact=3, duration/complexity=1)`). **`IN SCOPE`**: sección `[12.1.0]` del changelog con los ítems de payload de los planes 156 y 166 y la absorción de `12.0.1` declarada; bump de `protocol/.agents/VERSION` y de `PROTOCOL_VERSION` a `12.1.0`; snapshot de `docs/VERSIONING.md` §9; `ROADMAP.md`; y **promoción fast-forward + tag anotado**, condicionados a la verificación. **`OUT OF SCOPE`**: contenido de `protocol/` distinto de `VERSION`, `dist/`, reapertura de los planes 156/166/167, secciones publicadas del changelog y publicación remota. Findings `F-1` (Plan 166 sin versión propia) y `F-2` (`12.0.1` nunca publicado). Pending: publicación remota (owner mantenedor, `remote_git` no declarado). `## Delegación agentiva` sin `**Task:**` y `## Efectos declarados` con la fila negativa. `## Validation anchor` y `## Checkpoint / cierre` **vacíos**: el Plan se crea sin ejecutar y **no** declara condición derivada. | active |

## Nonagésima cuarta serie: reconciliación documental del cierre de `F-C` (Plan 167) (14 oct 2026)

Serie del Change que restaura la coherencia documental del cierre de la feature de autonomía
(`F-C`). Nace de un pedido directo del mantenedor (2026-10-14) y se clasifica **Clase B** de
RFC-56 —mejora documental compatible— porque modifica lo que afirman documentos **vigentes**,
sin cambiar el significado del protocolo ni sus contratos: **DEV-only** y **docs-only**, sin
release. Corrige **exactitud documental, no decisiones**: no reabre `F-C`, no reabre el Plan 165
(que permanece `Executed` con condición derivada `Closed` y **no** se edita, `.agents/AGENTS.md`
regla 5), no cambia ninguna capacidad, contrato, estado de etapa ni condición derivada. Su
alcance es: el estado narrativo del modelo de autonomía en `docs/CONVENTIONS.md`; el mapa
operativo `ROADMAP.md` con **un solo** estado de `F-C`; los registros del Plan 165 (`ID-6`,
`ID-8` y la contabilidad de counterproofs de `FC-7`) reconciliados **por referencia**; y la
trazabilidad de la evidencia de auditoría declarada `active` en `docs/working/audits/INDEX.md`.
Registra cuatro findings evidenciados (`F-01`…`F-04`), dos pending decisions (aprobación de
ejecución; destino de los artefactos de auditoría) y deja **vacíos** su anchor y su checkpoint:
el Plan se crea **sin ejecutar** y su creación no declara ninguna condición derivada. Fuera de su
alcance quedan las correcciones mecánicas (Clase C), la historia publicada del `CHANGELOG.md`, la
reconciliación de versión del payload de RFC-83 (vía Clase A) y la regularización del código que
entró sin artefacto de plan.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `167-reconciliacion-del-cierre-de-f-c.md` | — (vía plan; **Clase B** de RFC-56; Clase A sólo si la ejecución tocara `protocol/.agents/`) | Executed | **Reconciliación del cierre de la feature de autonomía (`F-C`).** Restaura la coherencia entre el estado que declaran los documentos vigentes, el mapa operativo, los registros del plan que cerró `F-C` y la trazabilidad de su evidencia. `Change Level` **L2** (`max(coordination=2, scope=2, architectural impact=0, release impact=0, duration/complexity=2)`). `IN SCOPE`: (1) estado narrativo del modelo de autonomía en `docs/CONVENTIONS.md`; (2) mapa operativo `ROADMAP.md` con un único estado cerrado de `F-C`; (3) registros del Plan 165 (`ID-6`/`ID-8` y contabilidad de counterproofs de `FC-7`) reconciliados **por referencia**, sin editar el 165; (4) trazabilidad de la evidencia de auditoría. `OUT OF SCOPE`: reescribir o reabrir los planes 165/166; correcciones mecánicas (Clase C: formato en `ROADMAP.md` y encabezado de este INDEX); historia publicada del `CHANGELOG.md`; versión del payload de RFC-83 (Clase A); regularización del código sin plan; y `protocol/.agents/`, `dist/`, `runtime/`, `tools/`, `tests/` y `.agents/`. Findings `F-01`…`F-04` (estado narrativo, mapa operativo, registros del plan cerrado con `BOUNDARY` declarado, evidencia de auditoría no versionada). Pending: aprobación de ejecución (blocking) y destino de los artefactos de auditoría (owner mantenedor). `## Delegación agentiva` sin `**Task:**` (ausencia declarada) y `## Efectos declarados` con la fila negativa. `## Validation anchor` y `## Checkpoint / cierre` **vacíos**: el Plan se crea sin ejecutar y **no** declara condición derivada. | active |

## Nonagésima tercera serie: autorización de ejecución de `F-C` y creación de su Plan (Planes 164 y 165) (13 oct 2026)

Serie del Change que **autoriza la ejecución de `F-C`** y crea su **Plan de ejecución**, sin implementarla.
El mantenedor ejerció el acto del **2026-10-13**: autoriza la ejecución de `F-C` bajo el alcance canónico
**1B** establecido por `OD-1` y la creación/formalización de su Plan con `Status: Aprobado para ejecución`,
`Change Level ≥ L3` y criterios `FC-1`…`FC-10`, **sin extender el scope** más allá del `IN SCOPE` de
`OD-1` y **sin incorporar** `C-16`/`C-17`/`C-21`. El Plan 164 registra el acto (transcripción, autoridad,
fecha efectiva, alcance heredado, artefacto designado, efecto sobre el estado y límite explícito: la
autorización **no** habilita al agente a implementar `F-C` en ese Change), resuelve y anota de forma
**aditiva** la pending decision del Plan 163 (regla `PC-1`) y reconcilia `ROADMAP.md` retirando el blocker
de autorización ya otorgada. El Plan 165 es el **contrato operativo del Change de implementación**:
`Change Level` **L3** (`max(coordination=2, scope=3, architectural impact=3, release impact=0, duration/complexity=3)`),
`IN SCOPE`/`OUT OF SCOPE` heredados **literalmente** de `OD-1`, `FC-1`…`FC-10` sin reducción de garantías,
`## Efectos declarados` con `network` **autorizado** (provider/modelo, por el acto) y
`install`/`remote_git`/`destructive`/`write_outside_project` **no declarados ni autorizados**, y las
**ocho decisiones de implementación** (`ID-1`…`ID-8`) identificadas y clasificadas — tres de ellas
(`ID-1` provider/modelo concreto, `ID-3` implementar aislamiento o declarar la garantía que no se ofrece,
`ID-5` mecanismo del objetivo multi-Change) requieren **acto explícito del mantenedor**, e `ID-6` lo
requiere si la solución escala a `protocol/.agents/`— **sin resolverlas por inferencia**. → **Actualización (acto del mantenedor, 2026-10-13):** `ID-1`/`ID-3`/`ID-5` quedaron **cerradas** —`ID-1`: ARgentOS es **agnóstico** respecto de harness, provider, modelo, SDK, CLI o mecanismo de invocación, y el actor real lo aporta el entorno del adoptante, **sin** implementar cliente HTTP, SDK, integración de provider ni mecanismo propio de invocación; `ID-3`: se **declara ausencia** de aislamiento proporcionado por ARgentOS, **sin** sandbox y **sin** garantía nueva; `ID-5`: semántica `Objetivo → Change → evaluación → siguiente Change` hasta satisfacción, con evaluación explícita tras **cada** Change—, con `ID-2`/`ID-4`/`ID-6`/`ID-7`/`ID-8` por diseño durante la ejecución. **`F-C` = `READY_FOR_IMPLEMENTATION`** (entry criteria satisfechas), con **implementación no iniciada**. El Plan 165 se
crea **sin ejecutar**: su anchor y su checkpoint quedan vacíos y no se declara ninguna condición derivada
por su sola creación. **Nada implementado:** 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/`,
`protocol/` y `dist/`; el default de `--sae`, los techos de recurso, el vocabulario de efectos y el
envelope de `F-B` quedan sin cambio. Docs-only, sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `164-acto-autorizacion-ejecucion-f-c.md` | — (vía plan; docs-only, RFC-56 no aplica) | Executed | **Acto de autorización de ejecución de `F-C` y formalización de su Plan.** Registra el acto del mantenedor del **2026-10-13** con su transcripción literal —«Autorizo la ejecución de F-C bajo el alcance canónico 1B establecido por OD-1… `Status: Aprobado para ejecución`, `Change Level ≥ L3` y criterios `FC-1`…`FC-10`… no extiende el scope… ni incorpora C-16/C-17/C-21»—, la tabla `decisión → autoridad → fecha → alcance → artefacto designado → efecto → límite`, y el estado resultante (`OD1 = CLOSED`; `F-C_SCOPE = 1B / CLOSED`; `F-C_PLAN = CREATED`; `F-C_PLAN_STATUS = Aprobado para ejecución`; `F-C_CHANGE_LEVEL = L3`; `F-C_IMPLEMENTATION = NOT_STARTED`; `ETAPA_B = NOT_STARTED`). Resuelve la pending decision de `<PLAN-163>` («autorización de ejecución del Change de `F-C`») y la anota de forma **aditiva** en el artefacto que la posee (regla `PC-1`), reconciliando `ROADMAP.md` (retiro del blocker de autorización; `F-C` aprobado y pendiente de ejecución) y registrando las decisiones de implementación como pendientes del Plan 165. **No implementa `F-C`.** | active |
| `165-f-c-autonomy-frontier-implementation.md` | — (vía plan; RFC-56 Clase A **sólo** si la ejecución toca `protocol/.agents/`) | Executed | **`F-C`: implementación de la frontera de autonomía (cerrada).** Plan de ejecución de `F-C` (alcance canónico **1B**), creado y **no ejecutado**. Trazabilidad del acto en `## Autorización` (mantenedor, 2026-10-13, alcance autorizado, artefacto designado, estado y límite explícito). `Change Level` **L3** con el cálculo por ejes registrado. **`IN SCOPE`** (idéntico al de `OD-1`): actor real con provider/modelo; aislamiento/sandbox, incluida la posibilidad explícitamente prevista de **declarar** una garantía que no se ofrece; Memory como contexto; objetivo multi-Change con trigger explícito; `C-02` contención de autoridad fuera del host; `C-26` recuperación ante fallos reales. **`OUT OF SCOPE`**: `C-16`/`C-17`/`C-21`, derivación parcial, recurso como eje de autorización, default de `--sae`, concurrencia, telemetría con backend, evaluación comparativa y cualquier capacidad no listada. **Criterios de salida** `FC-1`…`FC-10` heredados del Plan 163 sin reducción (actor real; aislamiento demostrado o declarado; Memory como contexto; objetivo multi-Change; contención de autoridad; recuperación con fallos reales; falsaciones ejecutables; alcance respetado; cierre anclado; prohibiciones preservadas). **Decisiones de implementación** `ID-1`…`ID-8` clasificadas: `ID-1` provider/modelo, `ID-3` aislamiento (implementar o declarar) y `ID-5` mecanismo multi-Change **requieren acto explícito del mantenedor**; `ID-2` arquitectura del actor derivable de contratos existentes (`AgentInvoker`, `Delegation`, `WorkerResult`, `AE-7`); `ID-4` Memory, `ID-6` contención (`C-02`, con escalada a payload si toca `protocol/.agents/`), `ID-7` recuperación/retry e `ID-8` discrepancia declarada del retry se resuelven por diseño durante la ejecución, con registro obligatorio. `## Efectos declarados`: `network` **autorizado**; `install`, `remote_git`, `destructive` y `write_outside_project` **no** declarados ni autorizados (detienen la ejecución). `## Delegación agentiva` sin `**Task:**` (ausencia declarada). `## Validation anchor` y `## Checkpoint / cierre` **vacíos**: el Plan se crea sin ejecutar y **no** declara condición derivada. | active |
| `166-materialize-objective-and-actor-provenance.md` | RFC-83 (Clase A; **`Accepted`** 2026-10-13) | Executed | **Materialización del vehículo RFC-56 para las dos decisiones de F-C sobre el payload** (decididas por autoridad el 2026-10-13): (i) `Objective` **Protocol-native mínimo** — entidad **explícita** (nunca inferida del prompt) que asocia **uno o más Changes**, con estado `open`/`COMPLETED` y regla `Evaluation → no satisfecho ⇒ siguiente Change · satisfecho ⇒ terminación`, **sin** una segunda Change State Machine y **sin** tocar la gobernanza por Change de `CHANGE_GOVERNANCE.md` (RFC-76); y (ii) **procedencia declarada del actor** en `HARNESS_REPORT.md` (`actor`, `harness`, `mechanism`, `declared_by`), conservando `self-reported` y `enforcement = informational`, sin provider/model/SDK/CLI (ID-1) y sin afirmar verificación independiente. Alcance: `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` + `protocol/.agents/contracts/HARNESS_REPORT.md` + índices/referencias del payload directamente afectados. **No ejecutado**: condicionado a RFC-83 `Accepted`; `## Validation anchor` y `## Checkpoint / cierre` vacíos. | active |

## Nonagésima segunda serie: acto de autoridad de `OD-1` — alcance canónico de `F-C` (Plan 163) (12 oct 2026)

Serie del Change que **resuelve `OD-1`**. El mantenedor ejerció el acto sobre el instrumento
decision-ready del Plan 162 y adoptó la interpretación **`B`**: **`F-C` es la iniciativa «Complete
ARgentOS Autonomy» (Etapa B) delimitada por el resultado de la Etapa A a la frontera de autonomía** —
`F-C` y Etapa B **no** son dos iniciativas paralelas, sino una misma iniciativa con su alcance ya
reducido por el mandato del `ROADMAP.md`—, con registro normativo **sin ADR**. **Dentro de `F-C`:** actor
con provider/modelo; aislamiento/sandbox (o declaración explícita, verificable y publicada de la garantía
que **no** se ofrece); Memory como contexto (`AE-8`); objetivo multi-Change con mecanismo/trigger
explícito (`D-1`); y las condiciones relevadas por la Etapa A: contención de autoridad fuera del host
(`C-02`) y recuperación ante fallos reales, incluida la discrepancia declarada sobre el retry (`C-26`).
**Fuera de `F-C`, explícito:** las brechas del payload del Protocol (`C-16` Discovery, `C-17` Discovery
KB, `C-21` Skills), que siguen su propia vía; la superficie de derivación parcial (`D-6b = NO`); un eje de
recurso como autorización (`AE-6`/`D-3`); el default de `--sae` (decidido); y concurrencia, telemetría
con backend y evaluación comparativa (posteriores). **Boundaries:** `F-A` (capacidad de autonomía DEV) y
`F-B` (envelope: admisión de efectos, `Effect ⊥ Scope`, techo como terminación) son **precondiciones
cerradas** que `F-C` no reimplementa ni modifica. El acto registra **alcance**, no autorización de
ejecución: `F-C` queda **`SCOPED`**, con `FC-1`…`FC-10` como criterios de cierre requeridos de su futuro
Change, `Change Level` mínimo esperado **L3** y una pending decision **bloqueante** con owner mantenedor
para autorizar su ejecución. Se registra por **adición** en `docs/CONVENTIONS.md` (las subsecciones del
2026-10-07 y del 2026-10-11 no se modifican) y se anota de forma aditiva la resolución de la pending
`OD-1` en el artefacto que la posee (`<PLAN-161>`, regla `PC-1`). **Nada implementado:** 0 diff en
`runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`; sin Plan de `F-C` autorizado; el
envelope de `F-B`, los techos de recurso, el vocabulario de efectos y el default de `--sae` quedan sin
cambio. Docs-only, sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `163-acto-autoridad-od1-alcance-f-c.md` | — (vía plan; docs-only, RFC-56 no aplica) | Executed | **Acto de autoridad de `OD-1`: alcance canónico de `F-C`.** Registra el acto del mantenedor del 2026-10-12 con su trazabilidad completa —decisión (`OD-1`), autoridad (mantenedor), fecha, rationale, evidencia (instrumento del Plan 162, matriz de Etapa A, mandato de reducción del `ROADMAP.md`) y registro normativo (`docs/CONVENTIONS.md`, aditivo, sin ADR)— y la decisión por pregunta: **`Q-a` = `B`** (`F-C` = Etapa B delimitada por Etapa A a la frontera de autonomía; `R1` delimitada, no `R2`); **`Q-b`** = el resto de Etapa B (brechas del payload) **no** se conserva como iniciativa paralela y queda fuera de `F-C`; **`Q-c`** = dentro actor con provider/modelo, aislamiento/sandbox, Memory como contexto, objetivo multi-Change, más `C-02` y `C-26` como condiciones, y fuera `C-16`/`C-17`/`C-21`; **`Q-d`** = **sin ADR**. Define el **boundary** con `F-A` (capacidad DEV: host, vocabulario de acciones, frontera SAE, modelo de autoridad) y con `F-B` (envelope `AE-1`…`AE-10`, `Effect ⊥ Scope`, techo de recurso como guarda de terminación) como **precondiciones cerradas** que `F-C` no reimplementa ni modifica; declara lo que **no** debe inferirse (que `F-C` esté autorizada o iniciada, que la madurez baja implique pertenencia, que el acto habilite una etapa o cambie defaults o el envelope, que fronteras fuera de `IN SCOPE` se incorporen por simetría); registra **dependencias y precondiciones** (`F-A`/`F-B`/Etapa A `Closed`; autorización de ejecución pendiente; RFC-56 Clase A sólo si el trabajo toca `protocol/.agents/`); y **prepara el trabajo futuro sin ejecutarlo**: `FC-1`…`FC-10` como criterios de cierre requeridos, `Change Level` mínimo esperado **L3** y estado **`SCOPED`** con pending decision bloqueante para la autorización de ejecución. Reconciliación derivada: `ROADMAP.md` (`NEXT` con `F-C` y su alcance; brechas del payload en `LATER` explícitamente fuera; grafo de dependencias alineado; blocker de ejecución no autorizada), `docs/plans/161-…md` (anotación aditiva de la resolución de la pending `OD-1`, preservando su texto) y `CHANGELOG.md`. **`OD-1` = `RESOLVED`**; **`F-C` = `NOT_IMPLEMENTED`** (sin autorización de ejecución); **Etapa B** deja de existir como iniciativa paralela. | active |

## Nonagésima primera serie: instrumento de decisión de `OD-1` (alcance canónico de `F-C`) (Plan 162) (12 oct 2026)

Serie del Change que aborda `OD-1` —«¿cuál es el alcance canónico de `F-C`?»— y **no lo resuelve**: su
verificación de autoridad concluye que la resolución es una **decisión de alcance reservada al
mantenedor** (`.agents/policies/authority.md` `## Authority classes` y `## Stop conditions (authority)`;
`.agents/AGENTS.md` regla 3; `.agents/policies/supervised-autonomous-execution.md` §8; ADR-16 `AU-3`/`AU-5`/`AU-6`)
y que **no está presente en el repositorio**: todas las menciones vivas a `F-C` son exclusiones de alcance
o remisiones a una decisión futura, y `OD-1` persiste como pending decision **bloqueante** con owner
mantenedor en el Plan 161. El Plan registra `OD1_BLOCKED` y materializa el **material mínimo** para que el
acto pueda ejercerse: lo que la evidencia de Etapa A **sí** determina (D-1…D-7: `F-C` no iniciada; `F-A`
cubrió la capacidad DEV y `F-B` el envelope; quedan fuera actor con provider/modelo, aislamiento/sandbox,
Memory y objetivos multi-Change; la derivación parcial está descartada y no pertenece a `F-C`; el eje de
recurso como autorización está prohibido; Etapa A puede reducir el alcance de Etapa B; y `C-08`/`C-02`/`C-26`
son las capacidades que condicionan una autonomía más amplia sin demostrar), las interpretaciones
`R1`/`R2`/`R3` con su soporte documental y su tensión, lo que la evidencia **no** determina —el rótulo
`F-C` no está fijado por ninguna fuente—, la pregunta `Q-a`…`Q-d` con sus consecuencias, la protección
explícita contra inferencias indebidas (madurez baja ≠ pertenencia a `F-C`), el registro exigido
(acto del mantenedor + subsección aditiva en `docs/CONVENTIONS.md`, con ADR-worthiness resuelta) y los
criterios de cierre del acto `AC-1`…`AC-12`. No se decide, no se define `F-C`, no se crea un Plan de
`F-C`/Etapa B, no se modifica `docs/CONVENTIONS.md` ni ningún ADR, y `runtime/`, `tests/`, `tools/`,
`.agents/`, `protocol/` y `dist/` quedan con **0 diff**. Docs-only, sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `162-instrumento-decision-od1-alcance-f-c.md` | — (vía plan; docs-only, RFC-56 no aplica) | Executed | **Instrumento de decisión de `OD-1`: alcance canónico de `F-C`.** Verifica la autoridad aplicable y concluye **`OD1_BLOCKED`**: la resolución de `OD-1` es una decisión de alcance reservada al mantenedor y no está presente en el repositorio —`DECISION` = «the human maintainer» y prohibición de convertir inferencia en decisión (`.agents/policies/authority.md`); «a human decision is required → STOP at the gate, ask»; regla 3 del `AGENTS.md` raíz; frontera humana de SAE §8 («authorizing scope, and authorizing scope changes»); ADR-16 `AU-3`/`AU-5`/`AU-6`—, de modo que **no elige** entre las interpretaciones conocidas. Prepara la forma **decision-ready**: (i) lo que la evidencia **sí** determina —`F-C` no iniciada y fuera de alcance de todo lo ejecutado; `F-A` = capacidad de autonomía DEV y `F-B` = envelope, ambos `Closed`; quedan fuera actor con provider/modelo, aislamiento/sandbox, Memory y objetivos multi-Change; `D-6b = NO` descarta la derivación parcial y la excluye de `F-C`; `AE-6`/`D-3` prohíben el eje de recurso como autorización; Etapa A puede **reducir** el alcance de Etapa B; y `C-08` (actor real), `C-02` (contención de autoridad fuera del host) y `C-26` (recuperación con fallos reales) son las capacidades que condicionan una autonomía más amplia sin demostrar—; (ii) las interpretaciones `R1` (`F-C` = Etapa B completa), `R2` (`F-C` = residuo del envelope) y `R3` (subconjunto de frontera de autonomía, opción derivable **no adoptada**) con su soporte documental y la tensión que cada una deja abierta; (iii) lo que la evidencia **no** determina; (iv) la pregunta `OD-1` desagregada en `Q-a`…`Q-d` (relación `F-C`↔Etapa B; qué representa el resto de Etapa B; qué capacidades son condiciones de `F-C`; ADR-worthiness) con sus consecuencias; (v) las siete inferencias prohibidas (scope creep); (vi) el registro exigido del acto —sección `## Acto de autoridad registrado` en un Plan vehículo según el precedente de los Planes 151/152, subsección **aditiva** en `docs/CONVENTIONS.md`, ADR si `Q-d` lo determina—; y (vii) los criterios de cierre del acto `AC-1`…`AC-12`. **No decide**: `F-C` permanece `NOT_IMPLEMENTED`, Etapa B `NOT_STARTED` y `OD-1` `PENDING_AUTHORITY`; el pending no se duplica (su propiedad sigue en el Plan 161, regla `PC-1`). | active |

## Nonagésima serie: autorización de Etapa A y creación del Plan 161 (12 oct 2026)

Serie del Change que **formaliza el acto de gobierno que bloqueaba la Etapa A** y crea su artefacto de
ejecución. Resuelve `PC-1` del Plan 160 —la autorización faltante, registrada como pending decision
bloqueante con owner mantenedor— mediante el acto del mantenedor del 2026-10-12, que autoriza el
alcance de la retrospectiva de capacidades y garantías y designa el **Plan 161** como su Plan. La
trazabilidad completa queda `decisión → autoridad → alcance autorizado → Plan 161`, en el estado
canónico `Aprobado para ejecución` (`docs/VERSIONING.md` §7); no se introduce ningún estado nuevo. El
Plan 161 **materializa el contrato de Etapa A** ya declarado por el Plan 149 —unidad *capacidad +
garantía + evidencia*; pregunta central; alcance conceptual mínimo de veintiocho capacidades; ocho
niveles de madurez; **Capability & Guarantee Matrix** con nueve dimensiones por capacidad; regla
fundamental— en criterios de cierre verificables `DC-1`…`DC-10`, sin ampliar el alcance: cobertura
exacta, nueve dimensiones por capacidad, un nivel de madurez por capacidad, evidencia ejecutable para
toda afirmación positiva, condiciones no probadas declaradas, límites declarados, regla fundamental,
citas resolubles, disciplina de alcance y cierre anclado. El producto —el **Capability & Guarantee
Matrix**— se ubica en `docs/working/audits/` por determinación del contrato de placement (familia
*Working analysis*), **sin** crear clase, namespace, entidad ni RFC nuevos. La anotación de resolución
de `PC-1` se agrega en el artefacto que la posee (Plan 160), de forma **aditiva** y sin reescribir su
texto. **Etapa A no se ejecuta en este Change:** la retrospectiva queda autorizada y pendiente para el
Change siguiente. `F-C`/Etapa B permanecen no iniciadas y `OD-1` sin resolver; el Plan 161 registra
únicamente la dependencia `Etapa A → resultado de Etapa A → revisión del alcance de F-C/Etapa B`.
Docs-only, sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `161-etapa-a-capability-and-guarantee-retrospective.md` | — (vía plan; docs-only, RFC-56 no aplica) | Executed | **Etapa A: retrospectiva de capacidades y garantías (Capability & Guarantee Retrospective).** Plan de ejecución de la Etapa A, autorizado por el acto del mantenedor del 2026-10-12 que resuelve `PC-1` del Plan 160. Registra la trazabilidad `decisión → autoridad → alcance autorizado → Plan 161`; el **alcance** (`IN SCOPE`) es el declarado por el Plan 149 —las veintiocho capacidades del alcance conceptual mínimo (Change Lifecycle; Authority; Scope enforcement; Validation / Closure; C1/C2/C3; SAE; Autonomous Orchestrator; Agent Worker; WorkerResult; Delegation; Context engineering; Context identity; Materialization; Prompt Cache; Placement; Discovery; Discovery KB; Protocol gates; enforced mode / hooks; EARS; Skills; Deliberation; Change Governance; Metrics / health; Feature flags; recovery; CI / validation; y distribución y sincronización de `dist`)— con las nueve dimensiones por capacidad y los ocho niveles de madurez como vocabulario cerrado; su producto es el **Capability & Guarantee Matrix** en `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`, registrado en `docs/working/audits/INDEX.md` (placement: familia *Working analysis* de `docs/placement-contract.md` §6, sin clase ni namespace nuevos). **Criterios de cierre** `DC-1`…`DC-10` verificables y suficientes para `Closed`: cobertura exacta de las 28 capacidades, 9 dimensiones × 28 sin celdas vacías, un nivel de madurez válido por capacidad, evidencia ejecutable para toda afirmación positiva, condiciones no probadas y límites declarados, regla fundamental (no es limpieza documental ni auditoría de archivos), citas resolubles, 0 diff fuera del `Scope`, y cierre con `## Validation anchor` + `## Checkpoint / cierre` y las dos determinaciones de impacto. **`OUT OF SCOPE`:** implementar cualquier capacidad; definir `F-C`, resolver `OD-1` o iniciar/autorizar Etapa B; decidir por sí mismo la reducción del alcance de Etapa B; operacionalizar la matriz; tocar `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/` o `dist/`; limpieza documental, refactors o reorganización. **Dependencias registradas:** `F-A` `CLOSED`, `F-B` `CLOSED`, `OD-2` `CLOSED`, `OD-6` `CLOSED`, `OD-4` `ALREADY_CLOSED`, `OD-7` `ALREADY_CLOSED`; `PR-1`/`PR-2` absorbidos por `F-B`; el resultado de Etapa A impacta el alcance posterior de `F-C`/Etapa B, registrado como pending decision con owner mantenedor (`OD-1` permanece abierto). `## Delegación agentiva` sin `**Task:**` (ausencia declarada) y `## Efectos declarados` negativo. Sin `VERSION` bump ni tag. **Ejecución (2026-10-12):** la retrospectiva se ejecutó y el producto quedó registrado — `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` con **28** capacidades × **9** dimensiones = **252** celdas sin vacíos y **28** niveles de madurez válidos (distribución `dogfoodeado` 11 · `testeado` 6 · `parcialmente demostrado` 4 · `dependiente de una condición externa` 3 · `no demostrado` 2 · `limitado por un boundary conocido` 1 · `implementado` 1 · `demostrado bajo condiciones reales` **0**), registro en `docs/working/audits/INDEX.md`, `DC-1`…`DC-10` **PASS**, Validation Anchor **A1** (state identity `f92cb1424c42b78b743c8520ba8fa60b815d9247`; delta scoped identity `efe62f1d37a719715c4cfd0bd0748fe67c14172d043213bec3787accfe14278e`), checkpoint con condición derivada **`Closed`** y reconciliación de `ROADMAP.md`. Hallazgo central: **ninguna** capacidad alcanza `demostrado bajo condiciones reales` para la totalidad de su afirmación, porque las condiciones pretendidas de buena parte del sistema —proyecto adoptante, proveedor real, CI— no son observables desde el repositorio. Findings `<PLAN-161>:F-1`/`F-2` resueltos por `<PLAN-161>:C-1`/`C-2`. `F-C`/Etapa B permanecen no iniciadas y `OD-1` sin resolver: `F-C scope = TO BE REVIEWED`. | active |

## Octogésima novena serie: cierre de decisiones inmediatas y preparación de la autorización de Etapa A (Plan 160) (12 oct 2026)

Serie del Change que cierra las dos decisiones que el relevamiento de cierre de `F-C` identificó como
cerrables ahora y deja el repositorio preparado para el tramo siguiente, sin implementar `F-C` ni
Etapa B. **`OD-2` (derivación parcial):** la decisión efectiva es `D-6b = NO` —la superficie está
**descartada**, no diferida, y no pertenece al alcance de `F-C`—; la reconciliación se registra en el
Amendment Log de ADR-19 y en la viñeta «Fuera de este acto» de `docs/CONVENTIONS.md`, preservando
íntegro el texto de las entradas anteriores (RFC-46). **`OD-6` (`work_type`):** el criterio de admisión
y la política de declaración ya estaban canonizados por el Plan 152, de modo que el Change retira del
ROADMAP el blocker obsoleto —cuyo contenido tiene artefacto dueño— y deja `P-5` como `GAP` por caso.
**Etapa A:** se determinan su contrato vigente (retrospectiva de capacidades y garantías; unidad
*capacidad + garantía + evidencia*; producto: Capability & Guarantee Matrix), su alcance, sus
dependencias y el Change aplicable, y se registra el **acto de autorización faltante** como pending
decision bloqueante con owner (mantenedor); no se simula autorización, no se crea un artefacto con un
estado que afirme una aprobación inexistente y no se ejecuta trabajo de Etapa A. Docs-only, sin
release; `runtime/`, `tests/`, `tools/`, `.agents/` y `protocol/` con **0 diff**.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `160-cierre-decisiones-od-y-preparacion-etapa-a.md` | — (vía plan; docs-only, RFC-56 no aplica) | Executed | **Cierre de las decisiones inmediatas (`OD-2`, `OD-6`) y preparación de la autorización de Etapa A.** Cierra `OD-2` canonizando `D-6b = NO` (la superficie de derivación parcial está descartada, no diferida) mediante una entrada de Amendment Log en `docs/adr/19-autonomy-envelope-authority.md` y la corrección de la viñeta «Fuera de este acto» en `docs/CONVENTIONS.md`, sin crear capacidad, superficie, mecanismo ni autorización y sin reescribir historia (RFC-46). Cierra `OD-6` constatando que el criterio de admisión y la política de declaración de `work_type` ya están canonizados por el Plan 152 (`GOV-8`/`GOV-9`) y retirando de `ROADMAP.md` el blocker obsoleto «`work_type` sin criterio de admisión», cuyo contenido tiene artefacto dueño; `P-5` permanece `GAP` por caso y no se deriva ningún valor. Prepara Etapa A: determina su contrato (retrospectiva de capacidades y garantías; unidad *capacidad + garantía + evidencia*; producto: Capability & Guarantee Matrix), su alcance, su autorización requerida (acto del mantenedor; el roadmap declara que «requiere su propio Change»), sus criterios de cierre (no existen formalmente: los fija el Plan que la autorice), sus dependencias y el Change aplicable (número libre 161), y registra el acto de autorización faltante como pending decision bloqueante (`PC-1`) con owner mantenedor, escalación, evidencia y efecto downstream; precisa la fila de Etapa A en `ROADMAP.md` con el artefacto que posee el acto requerido. **No implementado, por directiva:** `F-C`/Etapa B, provider/modelo, aislamiento/sandbox, Memory, concurrencia, telemetría y retry; `OD-4` (`--sae` opt-in) y `OD-7` (`PR-1`/`PR-2` absorbidos por `F-B`) se tratan como ya decididos, sin cambio. Registro del Plan en el INDEX y de su par en `CHANGELOG.md:[Unreleased]`. Sin `VERSION` bump ni tag; sin citas rotas nuevas (el conteo de `check_plan_citations` se mantiene en **26**). | active |

## Octogésima octava serie: materialización del envelope de autonomía (Plan 159) (11 oct 2026)

Serie del Change que **materializa** el envelope de autonomía (`F-B`) que el ADR-19 decidió el
2026-10-07 y dejó sin implementar. Cierra las dos cuestiones que ese acto dejó expresamente fuera
—`OPD-1` vocabulario DEV de clases de efecto; `OPD-2` techo de recurso como guarda de terminación
y **no** como dimensión de autorización— y los dos bloqueantes del relevamiento de cierre: `BLK-1`
(adMisión de efectos antes de delegar, con `Effect` ortogonal a `Scope`) y `BLK-2` (terminación por
recurso, con consumo acumulado desde las delegaciones registradas en el journal y supervivencia a
reinicio). Dev-only, sin release; no abre `F-C`/Etapa B ni implementa provider, Memory, sandbox,
concurrencia, telemetría ni retry.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `159-autonomy-envelope-implementation.md` | — (vía plan; DEV-only, RFC-56 no aplica) | Executed | **Materialización del envelope de autonomía (`F-B`).** Adopta el vocabulario DEV de clases de efecto ya materializado y verificado en `tools/check_session_artifacts.py` (`network`, `remote_git`, `install`, `destructive`, `write_outside_project`; `AUTHORIZED_BY` ∈ {`user`, `unattended_default`}; `EFFECT_STATUS` ∈ {`authorized`, `not_authorized`, `pending_user_confirmation`}) y declara el techo de recurso como **guarda operativa de terminación, nunca autorización** (`AE-6`/`D-3` preservados). Implementa: `observation.py` (parser de `## Efectos declarados` con `DeclaredEffect`, `**Resource ceiling:**` en `## Delegación agentiva`, `declared_effects_unresolved`, `GAP` declarado para techo ilegible), `autonomy.py` (`EFFECT_KINDS`/`EFFECT_AUTHORIZED_BY`/`EFFECT_STATUSES`, `DeclaredEffectView`, `EffectAdmission`, `admit_declared_effects`, `declared_effects` en el envelope, `effects`/`effects_unresolved` en el candidato, ejes scope y efecto evaluados y reportados por separado, proyección `authorization-effects-v1` dentro del checkpoint, y `resource_stop`/`resource_ceiling`/`resource_consumed` en el resultado sin veredicto de autoridad), `host.py` (`_apply_autonomy_gate` extendido a efectos all-or-nothing antes de delegar, `_autonomy_effects`, `_resource_consumed` derivado de las delegaciones del journal, `_effects_executed_violations` para el efecto ejecutado no declarado, `STOP_MAX_ITERATIONS` mapeado como stop operativo), `worker.py`/`agent_worker.py` (`effect:<clase>` calificado en `effects_executed`, `classify_executed_effects`), suites nuevas `tests/test_autonomy_effects.py` (36 falsaciones: casos A–E, contra-prueba, techo de recurso, efectos de worker) y `tests/test_autonomy_effects_dogfood.py` (13 pruebas ancladas: policy ↔ enforcement, vocabulario único), reconciliación normativa en `.agents/policies/supervised-autonomous-execution.md` (§1.5, §3.1, §5, §10, §12), `docs/plans/_TEMPLATE.md`, `docs/CONVENTIONS.md` y ADR-19 (Amendment Log 2026-10-11, sin reescribir el acto del 2026-10-07). Findings `<PLAN-159>:F-01`/`F-02` resueltos por `C-01`/`C-02`. Sin `VERSION` bump ni tag. | active |

## Octogésima séptima serie: simplificación radical del ROADMAP (Plan 158) (11 oct 2026)

Serie del Change que **reduce** `ROADMAP.md` de 367 líneas a 99, corrigiendo la implementación del Plan 157: aquélla resolvió el problema estructural (secciones contradictorias, estados implícitos, historia dentro del área operativa) pero el documento seguía acumulando, bajo `NOW / NEXT / LATER`, un capability inventory, un informe de autonomía, un índice documental, un manual de gobernanza, un catálogo de dependencias y un registro de blockers. La estrategia de este Change es **REDUCE, NOT REORGANIZE**: cada bloque se somete a la regla de admisibilidad —permanece sólo si responde a *cuál es el destino / dónde estamos / qué viene ahora / qué viene después / qué puede cambiar ese camino*— y lo que no responde se **elimina del ROADMAP**, no se re-tabula. El contenido eliminado no se pierde ni se reubica en documentos nuevos (no se crean `CAPABILITIES.md`, `AUTONOMY.md`, `DECISIONS.md` ni `ROUTING.md`): **ya tiene artefacto dueño** en `docs/CONVENTIONS.md`, `docs/plans/INDEX.md`, `runtime/README.md`, `docs/adr/19-autonomy-envelope-authority.md`, `CHANGELOG.md` y el artefacto que posee cada decisión. El contrato del ROADMAP **no se modifica**: este Change hace que el documento lo cumpla. Docs-only, sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `158-radical-simplification-roadmap.md` | — (vía plan; docs-only, RFC-56 no aplica) | Executed | **Simplificación radical del ROADMAP.** Reduce `ROADMAP.md` de **367 → 99 líneas** (presupuesto visual: IDEAL <100, ACCEPTABLE <150, WARNING ≥150, FAIL ≥200). Estructura resultante: header de dos líneas con puntero al contrato; `## 🎯 Destino` (2–4 líneas); `## 🧭 Posición actual` (4 bullets + `### Estado del que parte este roadmap`); `## 🚦 Roadmap` con `NOW` (1 iniciativa: promover `12.0.1`), `NEXT` (1: Etapa A, retrospectiva de capacidades y garantías) y `LATER` (3: envelope de autonomía, Complete ARgentOS Autonomy/Etapa B, Etapa C), cada iniciativa como `[DOMINIO] PRIORIDAD — qué y por qué`; `## 🔗 Dependencias críticas` en un único grafo Mermaid (4 aristas); `## 🚧 Bloqueos que pueden cambiar el camino` (6 filas). **Eliminados del ROADMAP:** los dos inventarios de capacidades DEV/PROTOCOL, `## 🧭 Autonomy — mapa del caso` (3 tablas + 2 grafos + 2 avisos), `## 🗂️ Dónde consultar qué` (11 filas), `## 📐 Qué es y qué NO es este documento` con sus reglas de admisión y frescura, la lista de trece fronteras candidatas, la tabla de baseline de 5 filas y las 3 cards ASCII de 6 campos. Contrato, reglas y definiciones normativas **permanecen** en `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)`, que no se edita. Registro del Plan 158 en el INDEX y de su par en `CHANGELOG.md:[Unreleased]`. Sin `VERSION` bump ni tag; `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `docs/CONVENTIONS.md` y los planes cerrados con **0 diff**. Sin nuevos broken citations: el conteo de `check_plan_citations` pasa de 27 a **26** (se conserva `### Estado del que parte este roadmap`, que una fuente viva cita). | active |

## Octogésima sexta serie: contrato canónico y ROADMAP visual estratégico (Plan 157) (11 oct 2026)

Serie del Change que establece el **contrato documental del `ROADMAP.md`** y reemplaza su estructura por una representación estratégica, visual y orientada al futuro. El ROADMAP deja de ser un mapa operativo que acumulaba historia cerrada (tres de sus cinco secciones operativas contenían trabajo ejecutado o resuelto) y pasa a declarar su **responsabilidad única** —comunicar visualmente la dirección de evolución y el camino de alto nivel—, con el modelo `NOW → NEXT → LATER`, dominio `PROTOCOL`/`DEV`/`BOTH` por iniciativa, prioridad, status sin mezclar implementación con publicación, dependencias estratégicas y una tabla corta de blockers. El **contrato canónico** vive en `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)` (qué es, qué no es, dimensiones obligatorias, regla de admisión, regla de frescura y frontera con `Roadmap impact`), y el término se registra en `docs/glossary/terms.md:ROADMAP` + `docs/glossary/INDEX.md` **enrutando** a esa fuente sin duplicarla. No crea capability registry ni decision register: el ROADMAP **enruta** a los artefactos que poseen el estado. Docs-only, sin release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `157-canonical-visual-roadmap.md` | — (vía plan; docs-only, RFC-56 no aplica) | Executed | **ROADMAP canónico visual y estratégico.** Establece el contrato documental del ROADMAP y reemplaza su estructura: header con propósito/definición/frescura; **Visión / Destino**; **Posición actual** (payload publicado `12.0.0` sobre `78ca512`, `origin/dist` @ `1181db6`, PATCH `12.0.1` en `dev` sin promocionar, capacidades disponibles por dominio); **Roadmap at a Glance** con lanes `NOW → NEXT → LATER` y una card por iniciativa (`Objective`, `Domain`, `Priority`, `Status`, `Depends on`); **dependencias estratégicas** en Mermaid; **blockers/decisiones** en tabla corta con el artefacto dueño; el **caso Autonomy** en cuatro planos diferenciados (host autonomy, SAE, authority model implementados; envelope decidido-no-implementado; Etapas A/B futuras) con la precisión de que lo existente es DEV-only y **no** es Complete Autonomy; la tabla **«Dónde consultar qué»**; y la definición explícita **es / no es**. Contrato normativo en `docs/CONVENTIONS.md`; entrada `ROADMAP` en `docs/glossary/terms.md` + `docs/glossary/INDEX.md`; reconciliación de referencias cruzadas en `AGENTS.md`, `README.md`, `docs/AGENTS.md`; clasificación bloque por bloque del ROADMAP anterior con destino declarado (sin pérdida de información); registro del Plan 157 en el INDEX y de su par en `CHANGELOG.md:[Unreleased]`. Sin `VERSION` bump ni tag; `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, RFCs, ADRs, `docs/VERSIONING.md`, `docs/placement-contract.md` y los planes cerrados con **0 diff**. Hallazgo registrado: la consigna citaba `Texto pegado.txt` como input, que **no existe en el repositorio** (`<PLAN-157>:F-1`); el ROADMAP no crea registro agregado de decisiones pendientes y esa ausencia queda como finding. | active |

## Octogésima quinta serie: reconciliación documental del payload con el layout canónico (Plan 156, RFC-82) (11 oct 2026)

Serie del Change que corrige la **prosa descriptiva** del payload que la release `12.0.0` (Plan 154, RFC-81) volvió
inexacta. La auditoría del Plan 155 estableció, contra código y no contra documentación, cuatro inexactitudes: el
bootstrap del payload declaraba `AGENTS.md` en la raíz cuando el bootstrap real es `.argentos/.agents/INDEX.md` y el
`AGENTS.md` de la raíz es un adapter **no normativo**; la frontera de artefactos afirmaba que el único artefacto fuera de
`.agents/` y `.project/` era `AGENTS.md`, cuando la configuración activa (`features.toml`), el estado local
(`.project/`) y los backups (`.backup/`) viven fuera de `PAYLOAD_ROOT`; la superficie de dependencias declaraba «exactly
four scripts» cuando el payload distribuye **ocho** módulos stdlib; y la frontera de distribución no distinguía lo que
transporta `dist` (el payload `.agents/` + `AGENTS.md`) de lo que el adoptante **materializa**
(`.argentos/{features.toml,.agents/,.project/,.backup/}` + adapter). El cambio es **Clase B** y **PATCH** por
`docs/VERSIONING.md` §3: no cambia ningún contrato, gate, estado, transición ni skill, con 0 diff en
`orchestrators/`, `contracts/`, `delegation/`, `roles/`, `skills/` y en los scripts del harness. Requiere RFC-56
(efecto de payload): la autorización es RFC-82 `Accepted` más este Plan. `docs/source-layout.md` se actualiza porque su
lista de «prosa que describe el layout adoptado (no tocar)» perdía su premisa; la guarda de links del entry file y las
citas históricas se preservan. La promoción, el tag y la regeneración de `dist` quedan pendientes de autorización
separada.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `156-payload-layout-documentation-reconciliation.md` | RFC-82 | Executed | **Reconciliación documental del payload con el layout canónico `.argentos/`.** Corrige, sin cambiar comportamiento, `protocol/.agents/INDEX.md` (bootstrap real `.argentos/.agents/INDEX.md`; el `AGENTS.md` de la raíz es adapter no normativo), `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (qué vive dentro de `PAYLOAD_ROOT` y qué fuera: `features.toml`, `.project/`, `.backup/`, y en la raíz solo el adapter; inmutabilidad del payload intacta), `protocol/.agents/harness/INDEX.md` (enumeración de los **ocho** módulos stdlib — los cuatro históricos más `roots.py` y los tres del lifecycle — y distinción entre lo que transporta `dist` y lo que el adoptante materializa), `protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md` («exactly four» → ocho, política de stdlib pura intacta) y `docs/source-layout.md` (retiro de la premisa falsa con autorización registrada; protección de links rotos intencionales y citas históricas preservada). Produce una versión **PATCH** del payload (`protocol/.agents/VERSION` `12.0.0` → `12.0.1`, con el ancla semántica del runtime sincronizada) e ítem `(plan 156, RFC-82)` en `CHANGELOG.md`; Clase B (RFC-56) con RFC-82 `Accepted` como autorización, Change Level L2. Batería canónica verde, pytest 1267 passed, gates sin `ANOMALY`; 0 diff de comportamiento. Validation Anchor (A1 delta `8e281f4a…`, state identity T1 `2497ae8c…`; revalidado por **A2** sobre el estado de cierre: delta `fe0315d3…` / tree `40ee9cc4…`, por el cambio de `CHANGELOG.md` en la ronda de cierre del Plan 155) y Checkpoint (consistencia PASS contra A2); condición derivada **`Closed`** con release pendiente de autorización separada. | active |

## Octogésima cuarta serie: refresh documental post-autonomía e integración de clientes (Plan 155) (11 oct 2026)

Serie del Change documental que audita la documentación de ARgentOS contra el estado real del sistema **después** de
las features de autonomía (Planes 151–153, ADR-19) y de la integración/adopción de clientes (Plan 154, RFC-81, layout
canónico `.argentos/` y lifecycle `install`/`update`/`uninstall`/`doctor`). El Plan reconstruye primero el estado real
desde código, tests, configuración e historia Git; después audita la documentación existente contra ese estado
(*gaps*, *drift*, obsolescencia y documentación conceptual faltante); y recién entonces materializa los cambios
necesarios. Reconciliación principal: la versión publicada real es **`12.0.0`** (tag anotado sobre `78ca512`,
`origin/dist` publicado con `VERSION` = `12.0.0`), mientras `docs/VERSIONING.md` §9 y `ROADMAP.md` declaraban
`11.6.2` como estado vigente. Documento nuevo: `docs/behavior-patterns.md` (patrones de comportamiento observables —
estados y condiciones derivadas, gate pattern, autonomy loop, orchestration, human-in-the-loop, failure/recovery,
client interaction y lifecycle), resuelto por el Placement Contract §6 en la familia Normative policy (`docs/*.md`),
sin crear familia ni namespace. Sin efecto en `protocol/`, `runtime/`, `tools/`, `tests/` ni `.agents/`; docs-only, sin
`VERSION` bump ni tag (RFC-69). Change Level L2.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `155-documentation-refresh-behavior-patterns.md` | — (vía plan; RFC-56 no aplica) | Executed | **Refresh documental post-autonomía e integración de clientes.** Reconstruye el estado real y audita la documentación contra él antes de modificarla; clasifica los problemas en `CRITICAL`/`HIGH`/`MEDIUM`/`LOW` y produce el diagnóstico como primer entregable. Reconciliaciones materializadas: `README.md` (capacidades actuales, autonomía DEV real y adopción/lifecycle; dos afirmaciones inexactas corregidas), `CHANGELOG.md` (historia real; sin entradas inventadas), `ROADMAP.md` (el estado del que parte deja de declarar una versión publicada obsoleta), `docs/VERSIONING.md` §9 (snapshot current-state contra `git tag` + `protocol/.agents/VERSION` + `origin/dist`), `docs/AGENTS.md` (carta documental: clasificación del artefacto nuevo), `docs/placement-contract.md` (cita legacy corregida) y `tools/check_plan_citations.py` (el documento nuevo y `placement-contract.md` incorporados al conjunto verificado). Artefacto nuevo: `docs/behavior-patterns.md`, que documenta los patrones de comportamiento **observables** del sistema (estados y condiciones derivadas `Verified`/`Executed`/`Committed`/`Closed`/`Released`; *gate pattern* con su autoridad y qué ocurre al fallar; *autonomy loop* del host DEV con los veredictos `AUTHORIZED_EXISTING`/`REQUIRES_HUMAN`/`FORBIDDEN`; orquestación y responsabilidad por componente; human-in-the-loop y las decisiones reservadas al mantenedor; taxonomía de fallo `GAP`/`ANOMALY`/`BOUNDARY`/`FAIL`/`N/A`; interacción cliente ↔ protocolo ↔ runtime —con el hallazgo de que no existe un modelo de clientes—; y lifecycle del sistema), con diagramas Mermaid y ASCII, citando sus fuentes de verdad sin duplicarlas y sin documentar razonamiento privado. DEV-only: `docs/` + `README.md` + `CHANGELOG.md` + `ROADMAP.md`, sin `VERSION` bump ni tag. Finding propio `<PLAN-155>:F-1`/`F-2`/`F-3`/`F-4`/`F-6` con sus correcciones `<PLAN-155>:C-1`/`C-2`/`C-3`/`C-4`/`C-5`, y `<PLAN-155>:F-5` (`open`, deferred, owner mantenedor: la obligación de roadmap diferida por el Plan 151 —`ROADMAP_IMPACT = DEFERRED`— sigue abierta y no se resuelve en este Change). **Ronda de cierre posterior:** desambiguación de la autonomía en `ROADMAP.md` (qué existe hoy —capacidad implementada, publicada en el repositorio y DEV-only— y qué pertenece a la Etapa B), desambiguación en la entrada viva de `CHANGELOG.md` (conservando literal el ítem histórico del plan 153) y en `docs/behavior-patterns.md` §5.2 (tres clases de acción del vocabulario no alcanzables desde la derivación). Validation Anchor (A1 delta `4f80d772…` / tree `b865b8a4…`; revalidado por **A2** delta `bbbec57c…` / tree `46f6e76a…`; **A3** sobre el estado de cierre: delta `2a3f58b0…` / tree `40ee9cc4…` —literal corregido por `<PLAN-155>:C-5` tras la verificación post-commit; `c02eb49c…` fue la medición previa, conservada como historia—, medido sobre las nueve rutas de contenido y reproducible desde el estado commiteado) y Checkpoint (consistencia PASS contra A3); condición derivada **`Closed`** (docs-only, sin release). | active |

## Octogésima tercera serie: lifecycle de adopción ARgentOS — implementación de RFC-81 (Plan 154) (11 oct 2026)

Serie del Change que convierte RFC-81 `Accepted` (lifecycle, ownership y distribución de una instalación ARgentOS) en un Class A Implementation Plan. El Plan 154 deriva normativamente de RFC-81 y **no** rediseña: hereda D1–D8 e I1–I10 como restricciones, define las unidades U1–U14 con sus dependencias (U1 → U2 → U3 → U4; U4 → U5/U6/U7/U8; U4–U8 → U9; U1–U9 → U10 → U11 → U12 → U13; U4–U6 → U14), operacionaliza los 36 criterios de GATE 3 y los 17 de GATE 4 con unidad, evidencia, test y condiciones PASS/STOP, y preserva las fronteras `RFC Accepted ≠ Plan Approved ≠ implementación ≠ GATE 2 commit ≠ GATE 3/4 ≠ release ≠ publicación`. **Ejecutado el 2026-10-11** por autorización explícita de la sesión (`IMPLEMENTATION_AUTHORIZED = YES`, `VERIFICATION_AUTHORIZED = YES`): implementación del lifecycle en `protocol/.agents/harness/` (`lifecycle.py`, `lifecycle_contract.py`, `lifecycle_staging.py`) con suite de filesystem real, GATE 3 **36/36** evidenciado, GATE 4 **17/17** (verificado localmente salvo publicación autorizada), clasificación de los 51 cambios de GATE 2 (compatible y necesario). **Regularizado y publicado** en la sesión de promoción (2026-10-11; `GATE_2_COMMIT_AUTHORIZED`/`RELEASE_AUTHORIZED`/`PUBLICATION_AUTHORIZED`/`PROMOTION_TO_MASTER_AUTHORIZED = YES`): commit de contenido **C1** `2267155` + commit de registro **C2** en `dev`, `protocol/.agents/VERSION` `11.7.1` → **`12.0.0`** (MAJOR; sync del anchor semántico del runtime), promoción `dev`→`master`, tag anotado `12.0.0` y regeneración de `dist` por `publish-dist`; condición derivada **`Closed`** (consistencia checkpoint↔anchor PASS).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `154-argentos-lifecycle-implementation.md` | RFC-81 | Executed | **Implementación del lifecycle de adopción definido por RFC-81 `Accepted`.** Materializa `install`/`update`/`uninstall`/`doctor` (+ `recover`) dentro de `protocol/.agents/harness/` (D1 ratificada: `lifecycle.py`, `lifecycle_contract.py`, `lifecycle_staging.py`, stdlib, distribuidos), con I1–I10 y ownership por procedencia (`origin`) + estado verificado (la huella detecta divergencia; no acredita propiedad), schema de `install.json` (rutas relativas a `PROJECT_ROOT`, `origin`/`state`, escritura atómica, snapshot previo, esquema desconocido ⇒ STOP), bootstrap por staging (ref de git fijada + fallback copia local, `--project-root` explícito, rechazo de staging ambiguo), journal/backups/rollback con recuperación que **nunca** sobrescribe cambios posteriores (`recovery pending`), update idempotente que no oculta divergencia, uninstall conservador con `--purge` acotado a `origin==installed ∧ state==present`, doctor con estados diferenciados, lock de exclusión mutua, revalidación de raíz, rechazo de escape por symlink y estados de salida diferenciados. Suite de filesystem real en `protocol/.agents/harness/tests/test_lifecycle_*.py`; GATE 3 **36/36**, GATE 4 **17/17** (`VERIFIED_LOCALLY` / `PENDING_AUTHORIZED_PUBLICATION`); U10 clasificó los 51 cambios preexistentes de GATE 2 (compatible y necesario); U11 actualizó `docs/ADOPTION.md`/`docs/MIGRATION.md`/`README.md`. Clase A (RFC-56), Change Level L3; layout **MAJOR** por `docs/VERSIONING.md` §3. **Regularizado y publicado** en la sesión de promoción (2026-10-11): commit C1 `2267155` + C2 en `dev`, `VERSION` `11.7.1` → `12.0.0`, promoción `dev`→`master`, tag `12.0.0`, regeneración de `dist`. Validation Anchor (delta scoped identity `ebfb3385…`, state identity T1 `890b5330…`) y Checkpoint (consistencia PASS; condición `Closed`). | active |

## Octogésima segunda serie: cierre de autoridad del modelo de autonomía (Planes 151–153) (07 oct 2026)

Serie del Change que **registra y materializa** el acto humano de autoridad del modelo de autonomía de
ARgentOS. El Plan registra, para decisión explícita del mantenedor, trece decisiones —
`D-1` (unidad de aceptación), `D-2a`/`D-2b`/`D-2c`/`D-2d` (superficie, representación, enforcement
y relación con Scope de los efectos), `D-3` (eje de recurso), `D-4` (clase de actor autónomo),
`D-5` (semántica de conocimiento), `D-6a`/`D-6b` (autorización y derivación parciales), `D-ADR`
(ADR-worthiness de dos invariantes), `Q9` (disposición, por ítem, de la materialización normativa
introducida sin autorización trazable) y `Q9bis` (disposición, por regla, de una segunda
materialización en la misma condición)—, más la disposición de los registros `HD-*` afectados.
`DECISION_COUNT = 13`; `P-5`/`work_type` se resuelve como **campo derivado** condicionado a `Q9` y
no como decisión adicional. El Plan incorpora las matrices de decisiones, de consecuencias por
ítem, de disposición `HD-*` y de trazabilidad, el límite de ejecución (este acto materializa sólo
documentos normativos, template, índices, changelog y —condicionalmente— un ADR), y el hecho
verificado de que **no existe acto humano del 2026-10-05** (`HISTORICAL_AUTHORITY_ACT =
NOT_VERIFIED`; `B556741_STATUS = MATERIALIZED_NOT_AUTHORIZED`), por lo que ninguna autoridad se
retrodada. Plan 151 (vía plan; DEV-only, sin efecto en `protocol/.agents/`, por lo que RFC-56 no
aplica; Change Level L2). **Estado: `Executed`** — el acto de autoridad (2026-10-07) materializó las trece
decisiones y dejó diez filas `HD-*` sin disposición; el **acto de autoridad posterior del 2026-10-08**
(vehículo: Plan 153) resolvió esas diez filas por evidencia y decisión posterior, satisfizo el criterio de
salida 10 sobre esa base y fijó el `Status` en `Executed`, con condición derivada `Closed`. El acto original
y su matriz histórica permanecen íntegros (sin retroactividad).**

El **Plan 152** (`152-authority-decisions-gov-1-10.md`) es el instrumento del acto de autoridad sobre las
diez decisiones que el Plan 151 dejó sin disposición: `GOV-1`…`GOV-10`. Nomina las decisiones, presenta
sus opciones, tipa las dependencias y define la evidencia y las condiciones de cierre. **Estado:
`Executed` — el mantenedor ejerció el acto el 2026-10-07** con diez resultados nominados
(`GOV-1 = C`; `GOV-2`…`GOV-9 = A`; `GOV-10 = B`), registrados en el propio Plan; la materialización
derivada (Pasos 12–13) se ejecutó y el Plan quedó cerrado (condición derivada `Closed`). El Plan no modifica el Plan 151, no crea ADR (la
ADR-worthiness del acto quedó pendiente como `F-1`), no implementa nada y preserva `P-5 = GAP`.

El **Plan 153** (`153-plan-151-residual-closure.md`) es el **instrumento Class B** que permite decidir, en
un acto de autoridad **posterior y explícito**, el tratamiento de los remanentes del Plan 151 —las diez
filas `HD-*` que su acto del 2026-10-07 dejó `SIN DISPOSICIÓN`—, preservando íntegramente el acto
histórico y prohibiendo la retroactividad. **Estado: `Executed`** — el mantenedor ejerció el acto el
**2026-10-08**: `D-151-1 = B` (las diez filas `HD-*` del Plan 151 resueltas por evidencia y decisión
posterior), `D-151-2 = Executed` (el Plan 151 pasa a `Executed`, con condición derivada `Closed`) y
`D-151-3 = YES` (`CL-151-Q1 = RESOLVED_BY_CURRENT_AUTHORITY`; la opción retroactiva permaneció
prohibida y no se usó). `CL-151-Q5` queda `RESOLVED_CURRENT_RULE`: el paréntesis de `Executed (parcial: <qué falta>)` describe lo que falta y la
forma legacy del Plan 41 no está disponible. El Plan enumera las rutas A–F con sus precondiciones,
materializaciones, validaciones y condiciones de parada; exige el acto registrado
(`AUTHORITY_INFERRED = NO`, `HISTORICAL_AUTHORITY_REUSED = NO`) y una revalidación si se modifica el
Plan 151; **no** modifica el Plan 151 ni el Plan 152, **no** crea ADR y excluye runtime, `protocol/`,
`.agents/`, `dist/`, implementación de autonomía, `P-5`/`work_type` y release.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `151-autonomy-authority-decision-closure.md` | — (vía plan; DEV-only, sin efecto de payload) | Executed | **Cierre de autoridad del modelo de autonomía.** Registra y materializa un único acto humano con trece decisiones (`D-1`, `D-2a`…`D-2d`, `D-3`, `D-4`, `D-5`, `D-6a`, `D-6b`, `D-ADR`, `Q9`, `Q9bis`) y la disposición de los registros `HD-*`; cada ítem declara `AUTHORITY_DECISION_REQUIRED`, propuesta de análisis no adoptada, alternativas y consecuencia para `ADOPT` / `REJECT` (con alternativa nominada) / `DEFER`. Incorpora la matriz `HD-*`, la disposición por ítem de `Q9` y por regla de `Q9bis`, el tratamiento condicional obligatorio de `D-ADR` (materialización del ADR dentro del propio acto), la regla condicional de `P-5` (`CONDITIONED_ON_RELEVANT_Q9_ITEMS`; existencia por el ítem `Q9[1]` `premises(D)`; valor derivable sólo con el criterio de admisión adoptado —hoy **no** adoptado— → `GAP`/determinación reservada), el límite de ejecución explícito y las determinaciones de cierre (`DOCUMENTATION_IMPACT = REQUIRED`; `ROADMAP_IMPACT = DEFERRED`, sin modificar `ROADMAP.md`). Registra como hecho verificado que no existe evidencia primaria de un acto de autoridad del 2026-10-05. El acto de autoridad (mantenedor, 2026-10-07) materializa las reglas del envelope en `docs/CONVENTIONS.md`, la provenance del paso 9 de `docs/VERSIONING.md`, la superficie de efectos declarados de `docs/plans/_TEMPLATE.md`, el ADR-19 y la provenance de los índices de `docs/working/`; **no** implementa autonomía, Effects, Budget, Memory ni provider/modelo, y **no** toca `protocol/`, `dist/`, `runtime/`, `tests/` ni `.agents/`. **Cierre del remanente (acto de autoridad posterior del 2026-10-08, vehículo: Plan 153):** las diez filas `HD-*` fueron resueltas por evidencia y decisión posterior, el criterio de salida 10 quedó satisfecho sobre esa base y el `Status` pasó a `Executed`, con condición derivada `Closed`; el acto original del 2026-10-07 y su matriz histórica permanecen íntegros (sin retroactividad). | active |
| `152-authority-decisions-gov-1-10.md` | — (vía plan; DEV-only, sin efecto de payload) | Executed | **Acto de autoridad sobre las diez decisiones de cierre de autonomía.** Instrumento del acto de autoridad del **2026-10-07** (mantenedor) sobre diez decisiones atómicas (`GOV-1`…`GOV-10`): identidad de IDs divergentes y tratamiento de formulaciones históricas (`GOV-1`), provenance de actos históricos no verificados (`GOV-2`), artefacto `Note` (`GOV-3`) y su vía de autorización (`GOV-4`), campo `**Lifecycle:**` (`GOV-5`), campos de retiro (`GOV-6`), vista de vigencia en los INDEX (`GOV-7`), criterio de admisión de `work_type` (`GOV-8`) y su política de campo (`GOV-9`), y elevación normativa de `INV-1` e `INV-3` (`GOV-10`). El Plan **nomina** decisiones y **no decide por sí mismo**: los diez resultados son `AUTHORITY INPUT` del mantenedor (2026-10-07), la matriz conserva el estado pre-acto y ninguna materialización downstream fue ejecutada. No modifica `docs/CONVENTIONS.md`/`docs/VERSIONING.md`/`AGENTS.md`/`docs/plans/_TEMPLATE.md`, no crea ADR (ADR-worthiness pendiente, `F-1`), **no** cierra el Plan 151 y preserva `P-5 = GAP`. Insumos ANALYSIS: la investigación exploratoria de las diez filas `HD-*` sin disposición y el paquete de diseño que las consolidó en `GOV-1`…`GOV-10`. | active |
| `153-plan-151-residual-closure.md` | — (vía plan; DEV-only, sin efecto de payload) | Executed | **Instrumento Class B para el cierre residual del Plan 151.** Materializa el vehículo que permite decidir, en un acto de autoridad **posterior y explícito**, el tratamiento de los remanentes del Plan 151: las diez filas `HD-*` que su acto del 2026-10-07 dejó `SIN DISPOSICIÓN` (`HD-INT-A`, `-B`, `-C`, `-D`, `-E`, `-F`, `-H`, `-I`, `-J` y `HD-M4`) y la decisión pendiente que las registra. El Plan **no decide**: `D-151-1`, `D-151-2` y `D-151-3`/`CL-151-Q1` (¿puede un acto posterior satisfacer un criterio de salida anterior sin reescribir el acto?) permanecen `PENDING_AUTHORITY`, con la opción retroactiva expresamente prohibida; `CL-151-Q5` queda `RESOLVED_CURRENT_RULE` (el paréntesis de `Executed (parcial: <qué falta>)` describe lo que falta; la forma legacy del Plan 41 no está disponible). Define las rutas A–F con precondiciones, superficies de materialización, revalidación obligatoria si cambia el contenido en scope, criterios de salida, batería, matriz de riesgos y condiciones de parada (`RETROACTIVE_HISTORY_MUTATION = BLOCKED`); exige el acto registrado con `AUTHORITY_ACT = RECORDED`, `AUTHORITY_INFERRED = NO` y `HISTORICAL_AUTHORITY_REUSED = NO`. **No** modifica el Plan 151 ni el Plan 152, **no** crea ADR, **no** deriva `work_type` (`P-5 = GAP`) y excluye runtime, `protocol/`, `.agents/`, `dist/`, implementación de autonomía y release. | active |

## Octogésima primera serie: implementación de Memory System (Plan 150) (06 oct 2026)

Serie del Change que transforma RFC-80 `Accepted` en un Class A Implementation Plan de
Memory System. El Plan 150 deriva normativamente de RFC-80 (contrato arquitectónico
cerrado: Episodic/Semantic/Synthesis/Operational/Archive, extracción/curation, consolidation,
retrieval y migración) y define catorce fases (Phase 0–13) con dependencias, entregables,
verificación y riesgos. **Ejecutado:** `Aprobado para ejecución` (autorización humana
2026-10-06), placement `ADAPT` `.project/knowledge/`, Phases 0–13 implementadas
(`runtime/memory/` + estándar `MEMORY_SYSTEM.md` + checker + 63 tests), validación
completa PASS (batería canónica + 1249 tests), committeado en `d668775`.
Plan 150 (vía RFC-80; Class A; Change Level L3; `Closed` con release pendiente).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `150-memory-system-implementation.md` | RFC-80 | Executed | **Implementación de Memory System (RFC-80).** Deriva la arquitectura cerrada de RFC-80 en una estrategia incremental y gobernada: Phase 0 (gobernanza/placement), Phase 1 (primitivas de persistencia —reusa `store.py`, `project_store.py`, `identity.py`, `change_governance.py`—), Phase 2 (Episodic: Session/Observation/Evidence + inmutabilidad), Phase 3 (Semantic: Claim/lifecycle/epistemic/applicability), Phase 4 (extracción y cuarentena de candidatos), Phase 5 (relaciones/contradicción/supersession), Phase 6 (Synthesis versionada + lineage), Phase 7 (consolidación idempotente + verificación + publicación atómica + NO_OP), Phase 8 (Operational Memory reconstruible no-autoritativa), Phase 9 (retrieval progresivo y acotado), Phase 10 (Archive rehidratable), Phase 11 (migración dual-read/dual-write), Phase 12 (métricas sin targets), Phase 13 (cutover/deprecación). Mapea los 30 invariantes I-001…I-030 a verificación, y define migración, rollback, failure recovery, compatibilidad legacy y testing. Ejecutado: `runtime/memory/` (14 módulos) + `MEMORY_SYSTEM.md` + `tools/check_memory_store.py` + 63 tests; 30 invariantes verificados; commit `d668775`; `Closed` (con release pendiente). | active |

## Octogésima serie: roadmap estratégico de capacidades y autonomía — Etapas A → B → C (Plan 149) (22 sep 2026)

Serie del Change que materializa en `ROADMAP.md` el roadmap estratégico acordado por el
mantenedor, con tres etapas dependientes entre sí: **Etapa A — Capability & Guarantee
Retrospective** (revisión de las capacidades y garantías que ARgentOS afirma proporcionar,
con unidad de análisis *capacidad + garantía + evidencia*, niveles de madurez explícitos
—implementado / testeado / dogfoodeado / demostrado bajo condiciones reales / parcialmente
demostrado / dependiente de una condición externa / no demostrado / limitado por un boundary
conocido— y un Capability & Guarantee Matrix; no es una auditoría documental), **Etapa B —
Complete ARgentOS Autonomy** (comienza a partir de los resultados de A, sin lista rígida de
features, para cerrar las fronteras que impiden ejecutar un objetivo amplio de forma autónoma
bajo supervisión humana dentro de `Autonomy ⊆ Scope ∩ Authority`; sus fronteras —provider/model
real, persistencia y consumo de Worker Results, derivación de la siguiente acción, ejecución
multi-step, recuperación ante fallos reales, fallos del provider, salidas inválidas del
Worker, presupuestos de ejecución, garantías de terminación, ejecución multi-worker,
deliberación cuando aporte valor, integración real de Prompt Cache y persistencia de
Project/Knowledge— se declaran **candidatas, no compromisos de implementación**) y **Etapa C —
New Features** (subordinada al conocimiento obtenido en A y a las necesidades descubiertas en
B; ninguna feature entra por disponibilidad tecnológica o por simetría con otro sistema). El
Change es exclusivamente de planificación y documentación: no ejecuta ninguna etapa, no
construye la matriz, no implementa features ni autonomía, no crea RFCs, ADRs, checkers,
mecanismos, autoridades ni artefactos nuevos, y no reabre las iniciativas históricas (Planes
146–148, Change Lifecycle MVP, SAE MVP, Prompt Cache MVP, Jury Trial MVP, Placement Contract,
RFC-75, ADR-15, ADR-16). Plan 149 (vía plan; docs-only sobre `ROADMAP.md`, `CHANGELOG.md`,
`docs/plans/INDEX.md` y su propio artefacto, sin efecto en `protocol/.agents/`, por lo que
RFC-56 no aplica; Change Level L1).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `149-argentos-capability-and-autonomy-roadmap.md` | — (vía plan; docs-only, sin efecto de payload) | Executed | **ARgentOS Capability & Autonomy Roadmap.** `ROADMAP.md` declara el roadmap estratégico vigente y su dependencia explícita **A → B → C**, con la regla de que primero se determina qué capacidades y garantías están realmente demostradas, luego se completan las fronteras de autonomía y recién después se incorporan nuevas features basadas en las necesidades descubiertas. La **Etapa A** fija la unidad de análisis *capacidad + garantía + evidencia*, la pregunta central («¿qué puede afirmar ARgentOS que hace, qué mecanismo lo implementa y qué evidencia tenemos de que funciona bajo las condiciones en las que pretendemos utilizarlo?»), el alcance conceptual mínimo (Change Lifecycle; Authority; Scope enforcement; Validation / Closure; C1/C2/C3; SAE; Autonomous Orchestrator; Agent Worker; WorkerResult; Delegation; Context engineering; Context identity; Materialization; Prompt Cache; Placement; Discovery; Discovery KB; Protocol gates; enforced mode / hooks; EARS; Skills; Deliberation; Change Governance; Metrics / health; Feature flags; recovery; CI / validation; y distribución y sincronización de `dist`) y un **Capability & Guarantee Matrix** con las nueve dimensiones por capacidad (qué afirma, qué mecanismo, qué tests, qué dogfooding, qué condiciones se probaron y cuáles no, qué garantía está demostrada y cuál no, y qué limitaciones existen); su regla fundamental es que evalúa la validez de las garantías operacionales y no es una limpieza documental. La **Etapa B** parte de los resultados de A y expresa la dirección `Human → authorized objective / scope → ARgentOS Orchestrator` (observe, derive, plan, delegate, execute, ingest, verify, correct, revalidate, continue, stop), con las fronteras pendientes declaradas **candidatas** y la frontera humana explícita (decisiones normativas, ampliación de Scope o Authority, cambios de objetivos, decisiones de release y las reservadas al mantenedor). La **Etapa C** exige necesidad identificada, sustento en la retrospectiva o en experiencia operacional, justificación clara y contribución a una capacidad o garantía real. El documento declara además qué **no** es una entrada del roadmap (auditorías documentales, checkers, RFCs sin necesidad, capas de governance, state machines, registries, entidades globales, artefactos administrativos, métricas sin hipótesis, features copiadas e integraciones por disponibilidad) y el estado del que parte (Protocol `11.6.2`, DEV y Protocol como dominios separados, `dist` publicando el payload, sin feature de Protocol pendiente de publicación y sin divergencia de publicación que resolver). No se ejecutó ninguna etapa del roadmap. | active |

## Septuagésima novena serie: promoción de `dev` a `master` y release de gobernanza 11.6.2 (Plan 148) (22 sep 2026)

Serie del Change que publica el estado verificado de `dev` posterior al plan 147 como release de
gobernanza, ejecutando `release commit → dev → origin/dev → master → tag 11.6.2 → dist`. El
preflight detectó un conflicto de contrato: Plan 147 no tiene diff de contenido bajo `protocol/`,
de modo que `docs/VERSIONING.md` §3 prohibía una versión y un tag, mientras §1/§2 exigían un tag
para todo lo que entra a `master`; la rama se detuvo, se escaló y el mantenedor autorizó enmendar
§3 para admitir las releases de gobernanza como excepción de promoción. La release tiene además
una función de nivelación: el tag `11.6.1` quedó sobre `8dbd92e`, que no contiene el commit de
cierre del Plan 146 (`7a9d393`), y la promoción lo incorpora junto con los commits del plan 147,
de modo que `master` vuelve a contener toda la historia de `dev`. Plan 148 (vía plan; acto de
release, sin cambio de contenido de payload — la única escritura bajo `protocol/` es
`protocol/.agents/VERSION`, metadata de versión de la release; Change Level L2).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `148-promote-plan147-to-master-release-11-6-2.md` | — (vía plan; Change de release, sin cambio de contenido de payload) | Executed | **Promoción de `dev` a `master` y release de gobernanza `11.6.2`.** Versión determinada como **sucesora PATCH** de la última publicada en `master` (`11.6.1` → `11.6.2`) según la viñeta «Releases de gobernanza» que el propio Change incorpora a `docs/VERSIONING.md` §3 con autorización del mantenedor, tras detener la rama por el conflicto entre la prohibición de releases de gobernanza y la exigencia de tag para `master`. **No hay cambio de protocolo:** el diff `dev` vs `master` no contiene ninguna diferencia de contenido bajo `protocol/` (11 archivos, ninguno de payload salvo `VERSION`), de modo que la release publica la versión del repositorio y no una capacidad nueva; `VERSION` = `PROTOCOL_VERSION` = `11.6.2`. Contenido publicado: la corrección post-release del plan 147 (C-1, C-2, dogfoods SAE y resolución de segmentos, con CI verde en `8173e77`) y el registro de cierre del plan 146, que **nivela `master`** (el tag `11.6.1` quedó sobre `8dbd92e`, que no contiene `7a9d393`). Se registra el release intent antes de tocar cualquier referencia remota, se promueve por merge `dev` → `master` sin fast-forward artificial ni squash, se crea el tag anotado `11.6.2` sobre el commit de promoción y se materializa `dist` por `publish-dist`. Sin force-push, sin reescritura de historia, sin mover ni alterar tags existentes; `ROADMAP.md` con 0 diff. Resuelve `<PLAN-147>:PC-1`. | active |


## Septuagésima octava serie: integridad post-release y compatibilidad de CI (Plan 147) (22 sep 2026)

Serie del Change que corrige, en una única pasada autorizada, las cuatro causas raíz que
dejaron rojo el job `check-protocol` después de la release `11.6.1` (runs `35689196717` en
`dev`: 4 failed / 1143 passed, y `35688773540` en `master`: 5 failed / 1142 passed), más el
`GAP-3` que el plan 146 había declarado fuera de su scope: la clasificación de una identidad
diferida por C-1, la dependencia de objetos Git históricos en C-2 y en los dogfoods SAE, y el
guard de contención del resolver de segmentos, cuyo veredicto dependía de la plataforma. Plan
147 (vía plan; DEV-only sobre `tools/`, `tests/`, `runtime/toolcalls/`,
`.github/workflows/`, `.agents/policies/` y la documentación corriente, sin efecto en
`protocol/.agents/`, `protocol/_AGENTS.md` ni `dist`, por lo que RFC-56 no aplica; Change
Level L2).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `147-post-release-integrity-and-ci-compatibility.md` | — (vía plan; DEV-only, sin efecto de payload) | Executed | **Corrección post-release de integridad y compatibilidad de CI.** Separa cuatro causas raíz en vez de tratarlas como un único problema ambiental: (F1) el árbol publicado de `master` (`8dbd92e`, merge de `dc21458` y `54171d8`) contiene la revisión **previa** del Plan 146 —`7a9d393` no es ancestro de `master` (`git merge-base --is-ancestor` → exit 1) y el diff del artefacto es 74 inserciones / 28 borrados—, cuya `## Validation anchor` difiere los literales de identidad al checkpoint, y C-1 traducía esa ausencia declarada en `ANOMALY`; se corrige R-C1-4 para distinguir **ausencia declarada** (`GAP`, advisory) de **valor presente e inválido** (`ANOMALY`), sin aceptar ningún valor malformado (falsificación explícita); (F2) C-2 resuelve cada tree id con `git rev-parse --verify <sha>^{tree}` y con `fetch-depth: 1` degrada a `GAP=27` en vez de verificar; (F3) los dogfoods SAE leen los commits del Plan 138 con `git log --grep` y no encuentran ninguno; ambas se corrigen dando **historia completa** al job (`actions/checkout@v4` con `fetch-depth: 0`) en lugar de debilitar los checkers; (F4) `_relative_path` validaba con la clase de path nativa, de modo que en POSIX `C:/Windows/x.md` no es absoluto ni tiene componente `..` y el guard no lo rechazaba —el test `test_path_escaping_the_payload_is_rejected` fallaba sólo en Linux—, y se corrige validando con semántica POSIX (`PurePosixPath`) en toda plataforma, rechazando el separador foráneo y el identificador calificado por unidad. Verificación: matriz de traversal (módulo `.../../`, absoluto, unidad, separador alternativo, normalizado, anidado) y de casos válidos; regresiones de C-1 (diferido, malformado, divergencia con el árbol material); reproducción de las condiciones de CI con clon superficial (fallos F2/F3 reproducidos) e historia completa (verdes); y verificación POSIX real en WSL Ubuntu del veredicto del guard. Los planes cerrados 146, 134, 121 y 98 no se reescriben; `master`, los tags `11.3.0`–`11.6.1` y `dist` no se tocan. | active |


Serie del Change que cierra el ciclo de los 33 commits que `dev` tenía por delante de
`origin/dev`, ejecutando `dev → origin/dev → master → tag 11.6.1 → release 11.6.1` como una
única Change integral: reconstrucción uno por uno de los 33 commits desde Git, verificación
de la topología (`master` en `dc21458`, merge-base `f85b558`, árbol de `master` idéntico al
del merge-base), de la versión (`VERSION` = `PROTOCOL_VERSION` = `11.6.1`) y del changelog,
batería canónica completa, harness del protocolo y gates C-1/C-2/C-3, publicación de `dev`,
promoción a `master` por merge y creación de los tags anotados del rango no publicado
completo —`11.3.0`, `11.4.0`, `11.5.0`, `11.6.0` y `11.6.1`— sobre el commit de promoción,
con `dist` regenerado por `publish-dist`. Plan 146 (vía plan; DEV-only sobre `CHANGELOG.md`,
`docs/VERSIONING.md`, este INDEX y su propio artefacto, sin efecto en `protocol/.agents/`,
por lo que RFC-56 no aplica; Change Level L2 con impacto de release 2).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `146-release-promotion-11-6-1.md` | — (vía plan; Change de release, sin efecto de payload) | Executed | **Promoción de `dev` y release del protocolo 11.3.0–11.6.1.** Reconstruye los **33** commits de `origin/dev..dev` uno por uno (SHA, tipo, mensaje, plan, área y relación con el release) y verifica que ninguno queda fuera de la línea de desarrollo; verifica la topología completa —`master` en `dc21458`, merge-base `f85b558`, árbol de `master` idéntico al del merge-base, `dev` 42 commits por delante de `master` y 33 por delante de `origin/dev`, fast-forward imposible por diseño y estrategia documentada de merge (`docs/VERSIONING.md:4. Flujo por plan (playbook)`, paso 7)—, la versión (`VERSION` = `PROTOCOL_VERSION` = `11.6.1`, cadena de bumps `11.3.0`→`11.4.0`→`11.5.0`→`11.6.0`→`11.6.1` desde la última versión publicada `11.2.0`; sin fuentes de versión duplicadas ni divergentes), el `CHANGELOG.md` y el estado de los planes 135–145 (todos `Executed`, ninguno reabierto). Corre la batería canónica completa (**seis checkers PASS**, `pytest tests/` **1147 passed**, harness **109 passed**, C-1 `VALID=51, GAP=0, ANOMALY=0`, C-2 `VALID=50, GAP=1, ANOMALY=0` —el `GAP` histórico del Plan 116, conservado y no reabierto—, C-3 `VALID=27, GAP=0, ANOMALY=0`, `check_ears_coverage.py` y `check_discovery_output.py` PASS), registra el **release intent** antes de tocar cualquier referencia remota, publica `dev` en su upstream, promueve a `master` por merge de `dev` y crea los **tags anotados** `11.3.0`, `11.4.0`, `11.5.0`, `11.6.0` y `11.6.1` sobre el commit de promoción —el rango no publicado completo, porque el invariante versión ↔ changelog ↔ tag no admite dejar versiones sin tag en `master` y el precedente `dc21458` oficializó dos versiones en un solo commit de release—, con `dist` regenerado por `publish-dist`. Corrige las dos afirmaciones «Tag pendiente de promoción» de `[11.4.0]` y `[11.3.0]` que la promoción vuelve falsas y reconcilia el snapshot `docs/VERSIONING.md` §9 en el punto de promoción que su §5 declara. Sin force-push, sin force-tag, sin reescritura de historia y sin operaciones destructivas; `protocol/.agents/`, `dist/`, `ROADMAP.md` y `docs/adr/` con **0 diff**. Declara dos `GAP` preexistentes sin resolver: el plan 126 materializó payload sin bump de `VERSION` (exención declarada por ese artefacto cerrado) y el commit `65a1113` (plan 131) no cita su plan en el asunto. | active |

## Septuagésima sexta serie: cierre integral del backlog accionable DEV `I-1`…`I-8` (Plan 145) (21 sep 2026)

Serie del Change que resuelve, por causa y en una única iteración autorizada, los ocho
items accionables que dejó abiertos el inventario global posterior al Plan 144: el
aislamiento del pytest harness (`I-1`), los headers de los Planes 143/144 (`I-2`), la fila
y la autodescripción del Plan 137 (`I-3`), el backlog evidenciado `B-4`/`B-7` (`I-4`), el
estado corriente del Placement Contract (`I-5`), el conjunto anclado de `tests/AGENTS.md`
(`I-6`), la métrica `recoveries` (`I-7`) y la derivación de
`findings_autonomously_corrected` (`I-8`). Plan 145 (vía plan; DEV-only sobre `tests/`,
`runtime/`, `conftest.py`, `docs/` y `.agents/policies/`, sin efecto en `protocol/.agents/`,
por lo que RFC-56 no aplica; Change Level L2).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `145-integral-dev-backlog-closure.md` | — (vía plan, DEV-only) | Executed | **Cierre integral del backlog accionable DEV `I-1`…`I-8`.** **`I-1` — determinismo del harness:** el scratch root pasa de **compartido** a **propio de cada sesión** (`tests/pytest_isolation.py`: token declarado, `session_scratch_root`, `clear_own_scratch`, `prune_stale_sessions` por edad con umbral declarado de 24 h y un `stat` por vecino; `conftest.py`: token declarado en import time, exportado por entorno y limpieza de lo propio). La causa de la no-determinancia era que cada inicio de sesión ejecutaba `rmtree` sobre el scratch **compartido**, de modo que una segunda sesión (o una limpieza de temporales del sistema operativo) destruía los repositorios desechables que otra sesión seguía usando: en siete corridas completas de la suite, cuatro fallaron, cada una en un test distinto. Una sesión sin token se **rechaza** en vez de recibir un directorio compartido. En el runtime DEV, `GitState` gana `git_available` y `observe()` eleva `ObservationError` cuando el CLI está disponible y el root existe pero el repositorio no se lee, en vez de degradar a un estado indistinguible de «no existe»; el CLI ausente sigue siendo un `GAP` declarado y un `TimeoutExpired` nunca se convierte en `None`. **`I-7`:** `_RECOVERY_ACTIONS` queda reducido a `RUN_REVALIDATION` —la rama de recuperación de la derivación, alcanzada con el anchor A1 stale—, con lo que una corrida autónoma sin stops reporta `Recoveries: 0` en lugar de `3`. **`I-8`:** `findings_autonomously_corrected` se **deriva** de los registros `RECORD_FINDING_CORRECTION` del journal bajo la regla anti-fabricación de `findings_corrected_autonomously`, y cuando el conteo es cero el resumen **declara la frontera** (el host detiene la iteración ante un finding abierto en vez de conducir una corrección) en lugar de presentar una constante como valor derivado. **`I-2`/`I-3`/`I-4`:** headers de los Planes 143 y 144 a `Executed`; fila y serie del Plan 137 a `Executed` sin «preparación», con su §Objetivo reconciliado y nota de reconciliación en `## Criterio de entrada`; `## Backlog evidenciado - plan 19` con banner de registro histórico, `B-4`/`B-7`/`B-8` anotados como resueltos y párrafo de resolución corriente que nombra la RFC-79 y el Plan 142 (11.6.0). **`I-5`:** `PC-72.1` registra el estado corriente del enforcement autorizado —librería de tabla de reglas materializada por el Plan 131, **no integrada** y advisory— y §23/§24 distinguen enforcement como obligación operativa de realización mecánica. **`I-6`:** `test_placement_contract_drift.py` entra al conjunto anclado (14 filas) y la fila de `test_pytest_isolation.py` declara la propiedad de sesión. **Falsación**: 12 regresiones de `I-1` y 9 de `I-7`/`I-8` ejecutadas contra la implementación anterior fallan todas y pasan contra la nueva; corrida concurrente de una sesión larga (127 tests SAE) junto a tres sesiones cortas sin interferencia; corrida real por el host con `Recoveries: 0`. Suite **1147 passed**, harness **109 passed**, seis checkers canónicos PASS, C-1 `VALID=50, GAP=0, ANOMALY=0`, C-2 `VALID=49, GAP=1, ANOMALY=0` (el `GAP` histórico del Plan 116, no reabierto) y C-3 `VALID=27, GAP=0, ANOMALY=0`. `protocol/.agents/`, `dist/`, `ROADMAP.md` y `docs/adr/` con **0 diff**; sin mecanismos, policies, checkers, estados, registries, authority classes, taxonomías ni workflows nuevos; sin RFC, sin ADR, sin `VERSION` bump, sin tag, sin release, sin promoción y sin push. | active |

## Septuagésima quinta serie: higiene documental y de tests del backlog DEV residual (Plan 144) (21 sep 2026)

Serie del Change que resuelve los tres residuales accionables que dejó abiertos el inventario
read-only posterior al Plan 143: `AW-1` (el conjunto anclado declarado en `tests/AGENTS.md` no
representaba el corpus real), `AW-2` (dos suites repetían la manipulación de `sys.path` para
`tools/` que el bootstrap único de la sesión ya realiza) y `AW-3` (tres espejos documentales
describían un estado que su propia fuente contradice). Plan 144 (vía plan; DEV-only sobre
`tests/` y `docs/`, sin efecto en `protocol/.agents/`, por lo que RFC-56 no aplica; Change
Level L1).

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `144-dev-documentation-test-hygiene.md` | — (vía plan; DEV-only `tests/` + `docs/`) | Executed | **Higiene documental y de tests del backlog DEV residual.** **`AW-1`:** la tabla del conjunto anclado de `tests/AGENTS.md` pasa de **8 a 13** filas —se agregan `test_placement_dogfood.py`, `test_autonomous_scope_dogfood.py`, `test_sae_scope_enforcement_dogfood.py`, `test_discovery_output_dogfood.py` y `test_check_ears_coverage_dogfood.py`, los cinco anclados que **citan esa misma tabla como su contrato**— sin cambiar la definición de «anclado», sin retirar ninguna entrada previa y sin alterar las demás instrucciones; los tres módulos que se declaran `isolated` quedan fuera. **`AW-2`:** se eliminan las dos sentencias `sys.path.insert` redundantes de `tools/` (en `tests/test_check_discovery_output.py` y `tests/test_discovery_output_dogfood.py`), con el ajuste de imports que corresponde (`sys` deja de importarse donde quedó sin uso; `Path` se conserva donde se usa como anotación); las nueve inserciones restantes agregan la raíz del repositorio para importar `runtime/` y se verificaron **necesarias**, de modo que quedan intactas y el Change no hace un refactor generalizado. **`AW-3`:** se reconcilian tres espejos contra su fuente autoritativa sin tocar la fuente —la columna `Status` de la fila de RFC-75 en `docs/rfc/INDEX.md` (declaraba implementación pendiente; el header de la RFC declara los Incrementos 0–4 materializados y el Incremento 5 fuera de alcance), la fila faltante de `PROMPT_CACHE_PHASE_1_REPORT.md` en `docs/working/research/INDEX.md` (documento versionado y `Origen` de RFC-78) y la fila de `AUDITORIA_SISTEMA.md` en `docs/working/audits/INDEX.md` (declarada activa contra su propio banner de cierre del 2026-08-14)—. `docs/VERSIONING.md`, `ROADMAP.md`, `protocol/`, `runtime/`, `docs/adr/` y `dist/` con **0 diff**; sin mecanismos, policies, checkers, estados, registries, authority classes, taxonomías ni workflows nuevos; sin RFC, sin ADR, sin `VERSION` bump, sin tag, sin release, sin promoción y sin push. | active |

## Septuagésima cuarta serie: vaciado del backlog operativo residual (Plan 143) (21 sep 2026)

Serie del Change que resuelve definitivamente los cuatro residuos que permanecían en el
backlog operativo: `HD-10`/plan 25, `<PLAN-142>:F-1`, `<PLAN-142>:F-2` y el `C-2 GAP`
histórico del plan 116. Plan 143 (vía plan; DEV-only sobre `docs/`, `tools/`, `tests/`,
`ROADMAP.md` y `CHANGELOG.md`, con **una excepción de payload declarada y autorizada**:
la entidad `contract:CHANGE_GOVERNANCE.md` que la H13 regla 11 exige, `Clase B`, que
produce la versión 11.6.1 PATCH; Change Level L2).

**Plan 143 — los cuatro residuales, uno por uno.** **`HD-10`/plan 25:** la medición del
dogfood del perfil `trivial` no es una capacidad implementable del repositorio —exige una
versión promovida y una sesión real con el usuario, actos externos al lifecycle—, de modo
que se reclasifica como actividad de adopción/operación externa y deja de ser backlog;
`<PLAN-141>:PC-2` pasa a `resuelta`, `ROADMAP.md` deja de declararla pendiente y el espejo
de este INDEX corrige la fila del plan 25, que declaraba verificado el perfil `trivial`
con la simulación del modo enforced del plan 46. **`<PLAN-142>:F-1`:** la verificación de
la H13 regla 11 se implementa en el checker existente (`tools/check_taxonomy_coherence.py`,
check 9) —los cinco campos `domain`/`artifact`/`lifecycle`/`produced_by`/`consumed_by` en
las dos direcciones, con el conjunto de archivos que fija el `## Input` de la policy y sólo
dos normalizaciones representacionales declaradas— con 14 casos nuevos (metadata
divergente, entidad divergente, referencia inexistente, referencias múltiples, campos
opcionales y normalización) y falsación de los cinco campos; la corrida sobre el corpus
real revela una condición **preexistente**: `CHANGE_GOVERNANCE.md` declaraba
`kind: contract` sin entidad contractual desde el plan 115, invisibles para una batería que
nunca cubrió la regla 11. La escritura del payload es una frontera RFC-56 y el agente la
registró y la escaló: el mantenedor autorizó la entidad bajo este Change, declarada
`Clase B` con justificación documentada y `## Scope` ampliado **antes** del efecto
(`.agents/policies/supervised-autonomous-execution.md` §1.2), y el checker pasa a `exit 0` sobre el corpus
real. **`<PLAN-142>:F-2`/`<PLAN-136>:F-1`:** se ejecuta la transición CL-8 autorizada —
`<PLAN-136>:F-1` pasa a `resolved` por el destino cumplido (RFC-79 decisión 2 +
`"project_scan"` materializado y verificado por el Plan 142) y `<PLAN-142>:F-2` a
`resolved` como consecuencia— con elementos inmutables preservados verbatim y bloques
append-only. **`C-2 GAP` del plan 116:** se formaliza la clasificación del Plan 140
(`HISTORICAL / NON-ACTIONABLE`) y se resuelve el residual de backlog —`<PLAN-133>:F-1` pasa
a `resolved`—; el `GAP` **sigue emitiéndose** porque ese es el comportamiento contractual
vigente de `C-2`, y el plan 116 queda con **0 diff**. Sin mecanismos, policies, estados,
registries, authority classes, taxonomías ni workflows nuevos; sin reapertura del plan 116,
del plan 142, de RFC-56/75, de ADR-15/16 ni de C-2/CI; sin promoción, tag, release ni push.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `143-empty-remaining-backlog.md` | — (vía plan; `Clase B` de RFC-56 sólo para la entidad faltante de `PROTOCOL_TAXONOMY.md`) | Executed | **Vaciado del backlog operativo residual.** **`HD-10`/plan 25:** resolución final — el perfil `trivial` está declarado e implementado (`protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`: tres artefactos y gates `H00, H04, H06`; comportamiento profile-aware verificado en `protocol/.agents/harness/tests/test_gate_validator.py`), y la medición real se reclasifica como actividad externa de adopción/operación **no ejecutada** que sale del backlog; `<PLAN-141>:PC-2` → `resuelta`. **`<PLAN-142>:F-1`:** implementación de la H13 regla 11 en `tools/check_taxonomy_coherence.py` (check 9, bidireccional, cinco campos, dos normalizaciones declaradas) con 14 casos nuevos y falsación por campo; la corrida real revela que `CHANGE_GOVERNANCE.md` no tenía entidad `kind: contract` desde el plan 115, y el registro faltante se agrega con autorización explícita del mantenedor (`Clase B`, `Scope` ampliado antes del efecto), produciendo el PATCH 11.6.1 (`VERSION`, changelog y ancla `PROTOCOL_VERSION`). **`<PLAN-142>:F-2`/`<PLAN-136>:F-1`:** transición CL-8 a `resolved` por destino cumplido, con elementos inmutables verbatim y bloque append-only. **`C-2 GAP` del plan 116:** `HISTORICAL / NON-ACTIONABLE / RESOLVED` como residual de backlog (`<PLAN-133>:F-1` → `resolved`), sin modificar el plan 116 ni el contrato de `C-2`, y con el `GAP` aún emitido. `docs/VERSIONING.md` §4.1 alineado con la cobertura nueva; `ROADMAP.md` y este INDEX reconciliados. | active |

## Septuagésima tercera serie: resolución del backlog de decisiones humanas (Planes 141–142) (21 sep 2026)

Serie del Change que cierra el backlog de decisiones humanas `HD-1`…`HD-12` y de la vía de
autorización que abre para el trabajo de payload que decide. Plan 141 (vía plan; DEV-only —
`docs/`, `ROADMAP.md`, `CHANGELOG.md`, `tests/` y el registro del Plan 137, sin efecto en
`protocol/.agents/`; Change Level L2). Plan 142 (vía RFC-79; `Clase A` y `B`;
**ejecutado** el 2026-09-21 por autorización explícita del mantenedor —el acto Clase A que
RFC-56 exige— en la versión 11.6.0 MINOR; Change Level L2).

**Plan 141 — resolución de `HD-1`…`HD-12`.** `HD-1`: el Plan 137 **se ejecuta** —el retiro
no es expresable en el ciclo de status de planes y la guarda tiene valor propio: R3 y R5 no
están cubiertos por ningún otro artefacto, mientras que R4 ya lo cubre el test del payload—.
`HD-2`: `ROADMAP.md` retira del trabajo activo la entrada `EARS structural validator`, que
declaraba futuro un mecanismo existente desde el plan 66/RFC-57. `HD-3`…`HD-6`: las cuatro
representaciones de payload quedan **decididas y especificadas** en RFC-79 (siete decisiones,
incluidas `F-18`, la metadata de taxonomía que resuelve `<PLAN-126>:PC-1`, y la frontera de
composición de `F-4`), con el Plan 142 como vía de materialización; el mantenedor, consultado,
decidió **redactar sin aceptar**, de modo que esos elementos cierran **bloqueados** con el
blocker concreto de la aceptación RFC-56 Clase A. `HD-7`: catorce findings corregidos y nunca
transicionados pasan a `resolved` con autoridad humana registrada, preservando los elementos
inmutables, y `<PLAN-136>:F-1`/`F-2` conservan su residual exacto. `HD-8`: cada pending
decision del bundle recibe su determinación individual sin inventar taxonomía. `HD-9`/`HD-11`:
la premisa de RFC-72 §4 queda **refutada** —el orden normativo existe desde RFC-78 §5 y está
implementado y testeado— y la RFC se corrige por su `Amendment Log` junto con el enunciado
falso sobre el contrato de materialización canónica. `HD-10`: el dogfood del plan 26 queda
**satisfecho** (su RFC de origen admitía la simulación de fixtures, que el plan 46 ejecutó) y
el del plan 25 conserva un blocker externo demostrado. `HD-12`: `F-4` decidido y enrutado;
`F-6`/`F-8` corregidos en el espejo de este INDEX; `F-7` aclarado en el `Amendment Log` de
RFC-74 sin reescribir el plan 91. **Findings propios**: `<PLAN-141>:F-1` (el test anclado
`test_no_protected_path_moved` afirmaba como invariante corriente un hecho histórico del Plan
138 comparando el árbol de trabajo contra `HEAD`) corregido por `<PLAN-141>:C-1`, que verifica
el hecho sobre los commits del Plan 138 y preserva la protección. Sin mecanismos, policies,
checkers, estados, registries, authority classes, taxonomías ni workflows nuevos;
`protocol/`, `runtime/`, `.agents/`, `docs/adr/` y `dist/` con **0 diff**; sin `VERSION` bump
y sin tag.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `141-human-decision-backlog-resolution.md` | — (vía plan, DEV-only; RFC-79 como vía del payload decidido) | Executed | **Resolución del backlog de decisiones humanas `HD-1`…`HD-12`.** Ejecuta el Plan 137 (guarda EARS de paridad + tres suites, 91 tests) y reconcilia `ROADMAP.md`; decide las siete representaciones de payload en RFC-79 y abre su vía de materialización con el Plan 142 (bloqueada en la aceptación Clase A); transiciona catorce findings a `resolved` con autoridad humana y conserva el residual exacto de los dos que no tienen corrección; resuelve elemento por elemento el bundle de pending decisions de `HD-8`; corrige el `Amendment Log` de RFC-69/72/74 (`F-3`, §4, `F-7` y la evolución futura del checker de trazabilidad) y el espejo de este INDEX (`F-6`/`F-8`); determina que el dogfood del plan 26 está satisfecho y que el del plan 25 tiene blocker externo. Corrección autónoma `<PLAN-141>:C-1` sobre un test anclado dependiente del estado de Git. | active |
| `142-payload-normative-residuals.md` | RFC-79 (`Accepted`, plan 142) | Executed | **Materialización de RFC-79** en la versión **11.6.0** (MINOR, adiciones compatibles). **`F-14`**: `status: legacy` en la entrada de KB y `[entries] legacy` en el manifest, con las instrucciones de `discovery_orchestrator.md` e `init_worker.md` corregidas para que la orden sea expresable. **`F-17`**: valor reservado `project_scan` en `source_files` —válido sólo para ausencias y hechos de árbol, nunca en la entrada de entorno— con el ítem 5 de D01 ampliado y los tres contratos de ausencia/árbol fijándolo; el checker DEV acepta el valor y reporta `ANOMALY` —no `GAP`— para un `source_files` no resoluble y no reservado. **`F-16`**: shape `documentation` en el manifest, en las señales de `init_worker`, en `00-discovery-init.md`, en `EXECUTIVE_SUMMARY.md` y en la variante de `API_SURFACE.md`; el checker lo admite y sigue rechazando un valor fuera del enum. **`B-8` residual**: evento de sesión `session_risk` (`risk`, `mitigations`) en el catálogo de `METRICS.md` y su clase `Recorded` en `PROTOCOL_METRICS.md`, con la obligación del modo single-instance precisada en `orchestrator.md`. **`F-18`**: delimitador `+++` del front matter de KB entry declarado. **`F-4`**: el criterio 1 de `COMPOSITION_OPTIMIZATION.md` declara que gobierna la composición conceptual y no el orden provider-bound, citando sólo anclas internas del payload. **Metadata de taxonomía**: `KB_DISCOVERY_ENTRY.md` e `INTER_WORKER_MESSAGE.md` alinean `produced_by`/`consumed_by` con sus entidades (H13 regla 11), resolviendo `<PLAN-126>:PC-1`. Tooling DEV: `tools/check_discovery_output.py` y sus dos suites (62 passed). `CHANGELOG.md` con la sección `[11.6.0]`, `protocol/.agents/VERSION` → 11.6.0 y el ancla `PROTOCOL_VERSION` del runtime alineada. Sin promoción, tag, release ni push. | active |

## Septuagésima segunda serie: Governance Residual Closure (Plan 140) (20 sep 2026)

Plan 140 (vía plan; DEV-only — `docs/plans/` + `CHANGELOG.md` + un test anclado, sin
efecto en `protocol/.agents/`, RFC-56 no aplica; Change Level L1). **Cierra el
inventario de gobernanza sin crear gobernanza nueva**: los cinco pendientes conocidos
se reconcilian reutilizando las reglas y los mecanismos existentes, con la evidencia
del repositorio y sin forzar ningún estado. **`<PLAN-136>:PC-5` → `superseded`**: su
premisa («la política vigente no contempla la situación») queda superada porque la
regla vigente sí la define —una determinación de impacto es obligación de estado y
nunca autorización de escritura, con el artefacto fuera de `Scope` la vía es
`DEFERRED` con la pending decision existente, y un impacto diferido sin ella es una
condición bloqueante sin resolver—, sin cuestión independiente residual: su frontera
viva es `<PLAN-138>:PC-2`. **`<PLAN-139>:F-1` → `resolved`** con bloque append-only
de metadatos, preservando observación, evidencia, estado Git y provenance verbatim.
**`B-2` (EARS) satisfecho sin residual**: el validador EARS del payload
(`protocol/.agents/harness/gate_validator.py`, H01 `ears: True`, cinco patrones),
su suite de harness y el job `check-protocol` de CI son el mecanismo responsable, con
dogfood read-only del propio Change (PASS con bullet EARS, FAIL con el bullet no
aceptable del estándar); la guarda de paridad que el Plan 137 proponía es trabajo
nuevo no autorizado (el Plan sigue `Aprobado para redacción` y `Superseded` exige un
plan reemplazante inexistente), no un residual de `B-2`. **`Roadmap Impact` del Plan
137 → `DEFERRED`** por la regla que `REQUIRED` no autoriza escribir el artefacto que
nombra, con `<PLAN-137>:PC-1` (owner mantenedor) como continuidad y `ROADMAP.md` con
**0 diff**. **`<PLAN-138>:PC-2` y el `C-2 GAP` del Plan 116** quedan clasificados
`DEFERRED` / histórico-no-accionable con su razón y su evidencia, sin crear taxonomía
nueva y sin reabrir C-2/CI, Plan 121, R4, closure identity ni los planes 116 y 138.
**Findings propios**: `<PLAN-140>:F-1` (el test anclado del Plan 139 dejaba la suite
roja en el estado comprometido, corregido por `<PLAN-140>:C-1` con una invariante
independiente del estado de Git y un digest del contenido normativo del plan cerrado,
que **endurece** la protección) y `<PLAN-140>:F-2` (el checkpoint del Plan 139
declaraba como árbol material del commit de cierre un tree distinto del real,
corregido por registro en artefacto nuevo, `<PLAN-140>:C-2`, sin reabrir el plan
cerrado). **Inventario final**: `OPEN / ACTIONABLE = 0`; `DEFERRED` e
`HISTORICAL / NON-ACTIONABLE` enumerados con su continuidad. Sin mecanismo, policy,
checker, estado, registry, authority class ni workflow nuevos; sin RFC/ADR nuevo; sin
cambio de payload; sin `VERSION` bump y sin tag.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `140-governance-residual-closure.md` | — (vía plan, DEV-only) | Executed | **Cierre de los cinco pendientes de gobernanza accionables.** **A** `<PLAN-136>:PC-5` → `superseded` (campo `resolución` únicamente) y `<PLAN-139>:F-1` → `resolved` con bloque `## Metadatos de estado (evolucionables)` append-only, elementos inmutables preservados verbatim. **B** `B-2`/EARS determinado como **satisfecho sin residual**, con el mecanismo responsable (`protocol/.agents/harness/gate_validator.py`: `TRIGGERS["H01"]["ears"] = True`, `EARS_RE` con los cinco patrones, señal `ears` PASS/FAIL), su cobertura (`protocol/.agents/harness/tests/test_gate_validator.py`, job `check-protocol` de `.github/workflows/check-protocol.yml`) y dogfood read-only ejecutado en este Change; no se implementa nada nuevo y el Plan 137 no cambia de status. **C** `Roadmap Impact` del Plan 137 reclasificado de `REQUIRED` a `DEFERRED` (la determinación es obligación de estado, nunca autorización de escritura), con `<PLAN-137>:PC-1` como pending decision existente que la gobierna y `ROADMAP.md` con **0 diff**. **D** `<PLAN-138>:PC-2` clasificada `DEFERRED` y no accionable actualmente, sin introducir Scope Expansion ni taxonomía nueva. **E** `C-2 GAP` del Plan 116 clasificado histórico/no accionable (`GAP` advisory, `exit 0`, `ANOMALY=0`; causa: ambigüedad `Tier 2` del anchor de un plan cerrado bajo la convención anti-auto-referencia), sin reabrir C-2/CI, Plan 121, R4, closure identity ni el artefacto cerrado. **Findings**: `<PLAN-140>:F-1` (test anclado del Plan 139 rojo en el estado comprometido: afirmaba un diff contra `HEAD` que sólo existe sin commitear) corregido por `<PLAN-140>:C-1`, que reemplaza la aserción dependiente de Git por aserciones de contenido, la regla de que el bloque de metadatos es la última región del artefacto y un digest normalizado del contenido normativo (los valores de `estado` y `resolución` se canonicalizan por LC-1), endureciendo la protección; `<PLAN-140>:F-2` (el checkpoint del Plan 139 declaraba `e284f98d8915f8c3e917f40218420caf604328b2` como árbol material del commit de cierre, cuando el árbol real es `2bc144d76ffe2c17432638d1c1208525bc97f3f5` y difiere exactamente en el propio plan 139) corregido por `<PLAN-140>:C-2` mediante registro factual en artefacto nuevo, sin modificar el plan cerrado y sin afectar la correspondencia R2 del estado de cierre; `<PLAN-140>:F-3` (`deferred`, owner mantenedor) registra las transiciones de estado pendientes y las pending decisions abiertas del Plan 136, fuera de los cinco pendientes autorizados. **Inventario**: `OPEN / ACTIONABLE = 0`; `DEFERRED` (`<PLAN-137>:PC-1`, ejecución de la guarda EARS, `<PLAN-138>:PC-2`, PC-2/PC-3 del Plan 136, `B-8` residual, findings sin transición del Plan 136, `<PLAN-114>:F-1`/`F-2`/`F-3`, releases `11.1.0`/`11.2.0` y `11.3.0`–`11.5.0`) e `HISTORICAL / NON-ACTIONABLE` (`C-2 GAP` del Plan 116, `<PLAN-136>:C-3`, entry EARS del mapa, observaciones de frontera ya materializadas). Sin mecanismo, policy, checker, estado, registry, authority class ni workflow nuevos; `protocol/`, `runtime/`, `tools/`, `.agents/`, `ROADMAP.md`, RFCs, ADRs y los planes 116/138 con **0 diff**; batería canónica PASS, `pytest tests/` PASS, C-1/C-2/C-3 sin `ANOMALY`; sin RFC/ADR nuevo; sin `VERSION` bump y sin tag. | active |

## Septuagésima primera serie: SAE Governance Boundary Closure (Plan 139) (20 sep 2026)

Plan 139 (vía plan; DEV-only — `docs/` + policies `.agents/`, sin efecto en
`protocol/.agents/`, RFC-56 no aplica; Change Level L1). **Materializa decisiones
humanas ya tomadas, no toma ninguna nueva.** Cierra las tres decisiones que quedaron
abiertas por el incidente del Plan 136 y por el cierre del Plan 138, sin crear
mecanismo alguno (el enforcement ya existía y está verificado desde el Plan 138) y
sin tocar `ROADMAP.md` ni la evidencia histórica. **DEC-1**: `<PLAN-136>:F-3` pasa a
`resolved` —el incidente ocurrió; el Plan 138 corrigió el mecanismo preventivo; la
regresión demuestra que el intento equivalente se detiene antes de ejecutar al
Worker; la evidencia original queda verbatim— mediante un bloque de **metadatos de
estado (evolucionables)** agregado al Plan 136, que no toca ninguna sección
normativa, anchor ni checkpoint. **DEC-2**: `<PLAN-138>:PC-1` pasa a `resuelta` con
la regla `Impact classification != authorization`, generalizada en su lugar canónico
existente (`.agents/policies/validation-closure.md` §5.1/§5.2 y la policy SAE §1.1):
la autorización **no** se infiere por la clasificación, ni por proximidad semántica,
ni por dependencia documental, ni por requisito de cierre; con el artefacto fuera de
Scope la única vía es `DEFERRED` con la pending decision existente. **DEC-3**:
`<PLAN-138>:PC-2` pasa a `deferred` y la policy SAE gana §1.4, que declara que **no
existe ni se introduce** ningún mecanismo autónomo de Scope Expansion: ampliar
`Task`/`Scope`/`Authority` es frontera de autoridad humana y produce `STOP` /
`REQUIRES_HUMAN`, la vía legítima es una nueva decisión de alcance del mantenedor
—sin mecanismo nuevo— y inventar protocolo, comando, estado, registry, API, workflow,
authority class, entidad o estado de lifecycle queda prohibido. **Finding propio
registrado sin forzar a éxito**: `<PLAN-139>:F-1` —la premisa de
`<PLAN-136>:PC-5` («la política vigente no contempla la situación») queda superada
por la regla que DEC-2 materializa, pero PC-5 **no** es una de las tres decisiones de
este Plan y **no** se resuelve: se registra la supersesión para que el mantenedor
decida su estado formal—. **Verificación reutilizada, sin tests redundantes**: los
ocho puntos exigidos se mapean a la regresión del Plan 138 (`tests/test_sae_scope_enforcement.py`
y su dogfood), con `runtime/`, `tests/` y `tools/` en **0 diff**. **Determinaciones**:
`Documentation Impact: REQUIRED` (las dos policies + los registros de estado de los
Planes 136/138), `Roadmap Impact: DEFERRED` con `<PLAN-138>:PC-1` como pending
decision que lo gobierna —`ROADMAP.md` con **0 diff**, no se interpreta `REQUIRED`
como permiso—. Sin RFC/ADR nuevo, sin `VERSION` bump, sin tag, sin push, sin merge,
sin release y sin promotion.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `139-sae-governance-boundary-closure.md` | — (vía plan, DEV-only) | Executed | **Cierre formal de las tres decisiones de gobernanza del incidente F-3.** DEC-1: `<PLAN-136>:F-3` → `resolved`, con bloque `## Metadatos de estado (evolucionables)` en `docs/plans/136-d01-mechanical-checker.md` (elemento evolucionable por LC-1; observación, evidencia, estado Git y provenance originales preservados verbatim; nota explícita de no retroactividad: la transición no legitima la escritura de `ROADMAP.md` ni `<PLAN-136>:C-3`, que conserva su autorización **no** establecida). DEC-2: `<PLAN-138>:PC-1` → `resuelta` con la regla `Impact classification != authorization` materializada en `.agents/policies/validation-closure.md` §5.1/§5.2 (prohibición de inferir autorización por clasificación, proximidad semántica, dependencia documental o requisito de cierre; `DEFERRED` + pending decision existente como única vía con el artefacto fuera de Scope) y en `.agents/policies/supervised-autonomous-execution.md` §1.1. DEC-3: `<PLAN-138>:PC-2` → `deferred` con §1.4 nueva en la policy SAE (no existe ni se introduce mecanismo autónomo de Scope Expansion; `STOP`/`REQUIRES_HUMAN`; vía legítima sin mecanismo nuevo; prohibición de inventar protocolo, comando, estado, registry, API, workflow, authority class, entidad o estado de lifecycle). **Registros**: `docs/plans/INDEX.md` (serie + header), `CHANGELOG.md` (ítem `[Unreleased]`). **Verificación**: los ocho puntos exigidos por el pedido mapeados a la regresión existente del Plan 138 (autorización de un target en Scope, `REQUIRED` fuera de Scope rechazado, parada previa a la delegación, no ampliación retrospectiva de `Task`/`Scope`/`Authority`, `ROADMAP.md` sin modificar, Planes 136/138 históricamente consistentes, F-3 cerrado sin alterar su evidencia, PC-2 explícitamente diferido); sin tests nuevos (redundantes); `runtime/`, `tests/`, `tools/` y `protocol/` con **0 diff**; seis checkers canónicos PASS; C-1/C-2/C-3 sin `ANOMALY`; `pytest tests/` PASS. **Finding**: `<PLAN-139>:F-1` (supersesión de `<PLAN-136>:PC-5`, registrada y no resuelta). Sin mecanismo, entidad, authority class, state machine, registry, protocolo, comando, API ni workflow nuevos; sin RFC/ADR nuevo; sin cambio de payload; sin `VERSION` bump y sin tag. `Committed` (C1), `Closed`, `Promoted` = no, `Released` = no. | active |

## Septuagésima serie: SAE Scope & Authority Hardening (Plan 138) (20 sep 2026)

Plan 138 (vía plan; DEV-only — `.agents/`, `runtime/`, `tests/`, `docs/`, sin
efecto en `protocol/.agents/`, RFC-56 no aplica; Change Level L2). Nace del
incidente `<PLAN-136>:F-3` (exceso de Scope y auto-autorización retrospectiva
durante la ejecución del Plan 136) y de las decisiones humanas `<PLAN-136>:PC-4`
(a) y `<PLAN-136>:PC-5`. Formaliza cinco propiedades —P1 Scope precede a Impact,
P2 Scope como precondición operacional, P3 STOP antes de escribir, P4 no
retroactividad del contrato de autorización, P5 impacto no es autorización— y ubica
el enforcement en `ExecutionHost._apply_autonomy_gate`, **antes** de
`_execute_delegation`, que es el último punto en el que el efecto persistente
todavía no ocurrió. **Ejecutado y cerrado el 2026-09-20** (commits C1/C2 en `dev`;
pytest `1030 passed`; batería canónica PASS; C-1/C-2/C-3 `ANOMALY=0`; Validation
Anchor y Checkpoint registrados). `<PLAN-136>:F-3` **no** se cerró, el Plan 136 no
se modificó, `ROADMAP.md` quedó con **0 diff** y `<PLAN-136>:PC-5` no se resolvió
(se re-registró como `<PLAN-138>:PC-2`). El propio Change es la demostración de la
frontera: su obligación de Roadmap quedó `DEFERRED` con pending decision existente
en lugar de convertirse en una escritura fuera de Scope.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `138-sae-scope-authority-hardening.md` | — (vía plan, DEV-only) | Executed | **Enforcement de Scope/Authority antes del efecto.** Tres piezas sobre mecanismos existentes: **E1** precondición de escritura sobre el **conjunto completo** de write targets (all-or-nothing; target vacío o no resoluble ⇒ STOP) verificada contra el Scope que el Plan **declara** —`## Entregables` + el `Scope set` del anchor + el propio Plan— y **no** contra la declaración que se está verificando, que era la circularidad que volvía vacua la comprobación de un solo path (`host._autonomy_target_path` → `resolved[0]`); **E2** *checkpoint de autorización*: proyección canónica de `Task` + familia de status autorizante + `Scope` autorizado, registrada en el journal al autorizar y comparada en toda iteración posterior, con la proyección partida en dos mitades —contrato y scope— para que una reescritura que el bound de Scope filtra igual siga siendo visible como divergencia, y con el pin tomado de la autorización **más temprana** del plan (una reescritura entre corridas no se re-pinea); **E3** evidencia en el campo `autonomy` del registro de iteración que ya existe (targets, decisión de scope, decisión de autoridad, stop condition, checkpoint, `authorization_drift`) sin telemetría, store ni registry nuevos. **La detección posterior se conserva** como defensa en profundidad para la escritura que ocurre dentro del `AgentInvoker` —límite que el host no puede interponer y que se declara como tal, sin fingir una garantía que la arquitectura no da—. **Policies**: `.agents/policies/supervised-autonomous-execution.md` §1.1/§1.2/§1.3 (+ §5 stop conditions, §9 impacto, §10 observabilidad, §12 límites declarados), `.agents/policies/validation-closure.md` §5.1/§5.2 (`REQUIRED` no es autorización de escritura; §7 condiciones de stop) y `.agents/policies/autonomous-orchestration.md` §11.3 (prevención vs. detección; el punto de enforcement). **Regresión F-3**: artefacto excluido **parametrizado** (`docs/ROADMAP-LIKE.md`, nunca `ROADMAP.md` hardcodeado) con Plan temporal, `Scope` que lo excluye, obligación `REQUIRED` que lo nombra e invoker inyectado que realmente escribe; demuestra STOP previo, ausencia de delegación persistida, artefacto byte-idéntico, elementos de autorización byte-idénticos, evidencia reconstruible, no legitimación retrospectiva y que el caso **no** puede satisfacerse con el comportamiento previo (detección posterior con el artefacto ya modificado). **Falsificación**: 44 pruebas con target/acción permitidos y no permitidos, `REQUIRED` dentro y fuera de Scope, conjuntos múltiples con uno fuera, target vacío y no resoluble, reescritura retrospectiva de `Task` y de `Scope`, vaciado de la declaración, proximidad semántica (contenedor, descendiente, plural, prefijo, `./`, separadores, mayúsculas), `DEFERRED` sin pending decision gobernante, records legítimos del host y escritura dentro del worker. **Dogfood**: 12 pruebas ancladas (punto de enforcement, policies, Plan 136 y `ROADMAP.md` sin modificar, ausencia de registry/state machine/authority class nuevos, y el envelope del propio Plan 138 pasando su propia frontera) más dogfood funcional end-to-end del escenario F-3 y de la divergencia entre corridas. **Finding propio detectado y corregido**: `tests/test_sae_scope_enforcement_dogfood.py` figuraba en `## Scope` y en la `Delegación agentiva` pero **no** en `## Entregables` —exactamente la clase de divergencia que el Change detecta— y se corrigió dentro del Scope autorizado (`<PLAN-138>:F-1` / `<PLAN-138>:C-1`). **Sin** state machine, entidad, authority class, registry, lifecycle, sistema de permisos paralelo, mecanismo de Scope independiente ni caso especial para `ROADMAP.md`/`Documentation Impact`; `contracts.py`, `derivation.py`, `worker.py`, `agent_worker.py` y `observation.py` **sin cambios** (se reutiliza `STOP_SCOPE_VIOLATION`); sin RFC/ADR nuevo, sin `VERSION` bump, sin tag y sin push. **Determinaciones**: `Documentation Impact: REQUIRED` (policies de SAE/validation-closure/autonomous-orchestration + `runtime/README.md`, reconciliadas en la ejecución) y `Roadmap Impact: DEFERRED` con `<PLAN-138>:PC-1` (owner: mantenedor) — `ROADMAP.md` con 0 diff. **Pendientes**: `<PLAN-138>:PC-1` (registro/prioridad del trabajo en el mapa) y `<PLAN-138>:PC-2` (si SAE necesita un mecanismo de ampliación legítima de Scope), ambos no bloqueantes; **cerrados por el Plan 139** (2026-09-20): PC-1 → `resuelta` (regla `Impact classification != authorization`) y PC-2 → `deferred` (no se introduce mecanismo autónomo de Scope Expansion). | active |

## Sexagésima novena serie: EARS Structural Validator (Plan 137) (15 sep 2026; ejecutado el 21 sep 2026 por el Plan 141)

Plan 137 (vía plan; DEV-only — `tools/` + `tests/` + `docs/`, sin efecto en
`protocol/.agents/`, RFC-56 no aplica; Change Level L1). Redactado **sólo para
redacción** y **ejecutado** el 2026-09-21 por el Change del Plan 141: la guarda
`tools/check_ears_coverage.py` existe y sus tres suites la verifican. Reconstruye
el estado real de la validación EARS y su hallazgo
central es que **el validador estructural EARS ya existe en el payload**:
`protocol/.agents/harness/gate_validator.py` (plan 66, RFC-57) incluye el chequeo
EARS de H01 (`TRIGGERS["H01"]["ears"] = True`, regex con los cinco patrones),
cubierto por `harness/tests/test_gate_validator.py` y corriendo en CI
(`.github/workflows/check-protocol.yml`). La fricción `F-01` de `B-2` (contrato con
array TOML vs validador de bullets) está **resuelta** por plan 33/RFC-34, que
declaró los bullets Markdown como forma canónica.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `137-ears-structural-validator.md` | — (vía plan, DEV-only) | Executed | **Reconstrucción de la validación EARS**: estándar `protocol/.agents/standards/requirements/EARS.md` (cinco patrones + cinco reglas de redacción); forma canónica = bullets Markdown (`protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Acceptance Criteria`); validador real = `gate_validator.py` invocado por la policy H01 §Decision Criteria. **Subset mecánico establecido (R1–R5)**: R1 al menos un bullet; R2 cada bullet casa uno de los cinco patrones; R3 criterios sólo en el bloque TOML constituyen violación de forma; R4 el validador del payload realmente chequea EARS para H01; R5 paridad entre el conjunto declarado y el implementado. **Bloque B excluido por nombre**: especificidad y verificabilidad (`H01` ítem 10 `[agent]`), no-compoundidad (`H01` ítem 12 `[agent]`), negaciones y vocabulario modal (`protocol/.agents/standards/requirements/EARS.md:Writing rules` 2–3, sin marca `[gate]`, enunciado léxico no cerrado), adecuación al dominio y derivación desde assumptions (`[agent]`). **Diseño**: `tools/check_ears_coverage.py` (nuevo) como guarda DEV **sólo lectura** que **deriva** el conjunto del payload y **invoca** el validador existente —no lo reimplementa—, con el vocabulario de señales y el contrato de exit codes existentes (`GAP` advisory, sólo `ANOMALY` cambia el exit code), texto + `--json`, determinista, `N/A` ante ausencia declarada. **Reutilización justificada por compatibilidad de contrato** con el checker DEV de D01 (mismo patrón, sin compartir código) y con `testsupport`/`pytest_isolation`; **no** se acopla a D01. **Dogfood**: la validación EARS aplica a `TASK_SPECIFICATION.md`, artefacto de **sesión** en `.project/` (efímero, no versionado) y **no existe corpus real versionado** — limitación **declarada** que no se convierte en `PASS`; el dogfood real es la auditoría del payload y el ejercicio del validador sobre los especímenes que el propio estándar y contrato declaran. **Falsación**: incluye casos que la guarda **debe dejar pasar aunque sean malos** (compound, negación, `should`) y casos que **deben fallar aunque parezcan buenos**. **Scope de siete rutas**: el checker, tres suites (comportamiento, falsación, dogfood) y el registro documental. `ROADMAP.md` **fuera de Scope**: la obligación de reconciliación (`Roadmap Impact: REQUIRED`) queda **pendiente** en `<PLAN-137>:PC-1` por la decisión humana de `F-3` (`<PLAN-136>:PC-4`: `REQUIRED` no amplía el scope). Pendientes `PC-1` (reconciliación del roadmap), `PC-2` (ampliar el conjunto mecánico: cambio de payload, RFC-56) y `PC-3` (agregar la guarda a la batería canónica). Documentation impact `REQUIRED` (CHANGELOG, INDEX, el propio Plan; `docs/VERSIONING.md` §4.1 **no** autorizado; fuentes normativas **no** se tocan); Roadmap impact `REQUIRED`. Sin implementación, sin modificar `protocol/`, `runtime/`, `.agents/` ni `ROADMAP.md`, sin release ni tag. | active |

## Sexagésima octava serie: D01 Mechanical Checker, preparación (Plan 136) (15 sep 2026)

Plan 136 (vía plan; DEV-only — `tools/` + `tests/`, sin efecto en
`protocol/.agents/`, RFC-56 no aplica; Change Level L2). **Sólo preparación: no
implementa D01.** Redacta el Plan que materializa el **subconjunto mecánico y
determinista** de D01 (estructura y procedencia resoluble) como checker DEV,
reconstruyendo el estado actual de D01 desde el repositorio en lugar del diseño
histórico. Queda en `Aprobado para redacción`: la autorización de ejecución es una
decisión humana posterior (`<PLAN-136>:PC-1`). **[Estado corriente, Plan 145,
2026-09-21: `<PLAN-136>:PC-1` se resolvió, el Plan 136 está `Executed` con
condición derivada `Closed` y sus residuales están cerrados; la frase anterior
describe el estado de redacción, no el de hoy.]**

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `136-d01-mechanical-checker.md` | — (vía plan, DEV-only) | Executed | **Reconstrucción de D01**: es una harness policy del payload (trigger `D01`, `DISCOVERY_VALIDATE → DISCOVERY_READY`, único gate del dominio discovery) que cubre validación estructural **y** ground truth; el runner no existe y hoy sus 12 ítems son juicio `[agent]`; el propio contrato declara los ítems de estructura determinista como candidatos `[gate]`. Origen: `B-1` **derivado** (`F-11` resuelta por planes 40 y 47/RFC-48; modelo D01 aclarado por plan 60). **Once puntos deterministas** entran en el checker (existencia y no-vaciedad; front matter TOML y campos requeridos; `artifact`/`kind`; `#` ↔ `title`; `## Discovered Facts` y secciones por contrato de tipo; existencia de `source_files` con `system_probe` sólo para environment; `[entries] active` ↔ archivos; front matter ↔ manifest; `## Project Shape` primera sección de contenido y coincidente con el manifest; `distribution.md` condicional a shape `library`/`cli`). **Seis ítems de juicio quedan fuera por nombre** (stack real, dependencias reales, patrones con ejemplo, secretos, claims sin fuente, merge consistente, api↔shape): no se convierten artificialmente en checker. Requisitos resueltos **desde los contratos** (single-source, plan 47/RFC-48), nunca desde una lista propia. Reporte con el vocabulario de señales y el contrato de exit codes existentes (`GAP` advisory, sólo `ANOMALY` cambia el exit code); ausencia de KB = `N/A` válido. **Scope exacto de seis rutas**: `tools/check_discovery_output.py`, `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py`, este Plan, `docs/plans/INDEX.md` y `CHANGELOG.md`. **Fronteras registradas, no resueltas:** `F-1` (`F-17`: `source_files` sin valor de procedencia para ausencias y hechos de árbol → el checker reporta `GAP`, nunca `ANOMALY`, y la corrección de fondo es payload, `<PLAN-136>:PC-2`) y `F-2` (`F-11`: contradicción textual `artifact_validated: KB_DISCOVERY_ENTRY.md` vs las entradas reales, conservada como evidencia sin editar el payload). Pendientes `PC-1` (autorización de ejecución), `PC-2` (`F-17`) y `PC-3` (`F-16`). Documentation impact `REQUIRED` (CHANGELOG, INDEX, el propio Plan; `docs/VERSIONING.md` §4.1 deliberadamente **no** autorizado); Roadmap impact `REQUIRED` (la fila «Mechanical D01 subset» de `ROADMAP.md:Trabajo activo / dogfood` deja de estar activa y el orden de la secuencia de dogfood cambia; reconciliación **al ejecutar**, no ahora). Sin implementación, sin modificar `protocol/`, `runtime/`, `.agents/` ni `ROADMAP.md`, sin release ni tag. **Ejecutado** (`**Status:** Executed`, condición derivada **`Closed`**, DEV-only sin release): `tools/check_discovery_output.py` (checker del subconjunto mecánico: resolución de contratos desde el payload en sólo lectura, validación por entrada, validación del manifest, resolución de procedencia, reporte texto + `--json`, contrato de exit codes `0`/`1`/`2` con `GAP` advisory), `tests/test_check_discovery_output.py` (42 pruebas) y `tests/test_discovery_output_dogfood.py` (12 pruebas ancladas al payload real). Los once puntos deterministas implementados; los seis ítems de juicio **no** convertidos en checks. `F-17` reporta `GAP` y nunca `ANOMALY`, sin exención ad-hoc y sin tocar el payload; `F-16` acepta el enum y no decide el shape. Validation Anchor A1 (delta `d4547527…`, tree `5f6c4fab…`), consistencia PASS verificada por C-2, C-1 y C-3 `VALID`; `pytest tests/` 953 passed, 0 failed. Findings `F-3` a `F-6` (contradicción scope↔Roadmap Impact del propio Plan, mapeo de contratos por convención inexistente, status de entrada y cobertura de la rama `BOUNDARY`) corregidos por `C-3` a `C-6`; `PC-1` resuelta por la autorización humana explícita. `ROADMAP.md` fue modificado **fuera del `Scope` autorizado** del Plan: el mantenedor decidió (`<PLAN-136>:PC-4`) que `Roadmap Impact: REQUIRED` **no** autoriza por sí sola la escritura de un artefacto excluido del scope. Resuelto después en la sección «Resolución post-cierre de F-3 (A y B)» del Plan: **A** (retirada de la fila de D01) confirmado como reconciliación factual; **B1** (`EARS structural validator` pasa a `Próximo dogfood`) confirmado; **B2** (prioridad `Media` → `Alta`) **no sustentado** y restituido a `Media`. `<PLAN-136>:F-3` queda `ready for human resolution` (la transición a `resolved` es decisión humana, CL-8 / ADR-16 AU-3); **cerrada como `resolved` por el Plan 139** (2026-09-20), que materializó la decisión del mantenedor sin alterar la evidencia original del finding; el gap de gobernanza sobre `REQUIRED` + artefacto fuera de scope queda registrado como observación en `<PLAN-136>:PC-5`, sin modificar la gobernanza. Sin modificar `protocol/`, `runtime/` ni `.agents/` (0 diff), sin agregar el checker a la batería canónica, sin release ni tag. | active |

## Sexagésima séptima serie: Supervised Autonomous Execution (Plan 135) (15 sep 2026)

Plan 135 (vía plan; DEV-only — `.agents/`, `runtime/`, `tests/`, `docs/`, sin
efecto en `protocol/.agents/`, RFC-56 no aplica; Change Level L2). Formaliza y
materializa **Supervised Autonomous Execution (SAE)**: la política operacional
que permite al DEV Autonomous Orchestrator ejecutar, corregir, revalidar,
recuperar y continuar todo paso que ya esté dentro del scope y la autoridad
concedidos, deteniéndose exactamente ante una frontera de autoridad. Separa
explícitamente **Authority** (qué está autorizado), **Scope** (qué trabajo está
autorizado) y **Autonomy** (qué acciones puede ejecutar el host sin nueva
autorización), con la regla `autonomy ⊆ authorized scope ∧ autonomy ⊆ granted
authority`. Investiga primero si la arquitectura existente ya expresa SAE y
concluye que sí: no crea entidad, registry, state machine, lifecycle, authority
class, identity primitive, worker type, daemon, database ni sistema de tracing.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `135-supervised-autonomous-execution.md` | — (vía plan, DEV-only) | Executed | Supervised Autonomous Execution. **Policy nueva** `.agents/policies/supervised-autonomous-execution.md`: definición operacional de SAE, separación Authority/Scope/Autonomy, continuación autónoma, política de findings, findings bloqueados vs. branches independientes, stop conditions, human boundary, scope verification, determinaciones de impacto, recovery, evidencia, execution summary y métrica de autonomía (reusa artifacts existentes; no introduce sistema de métricas). **Runtime nuevo** `runtime/orchestrator/autonomy.py`: `AutonomyEnvelope` (derivado de lo que el Plan ya declara), `AutonomyCandidate`, `verify_action_scope` (pertenencia exacta; nunca por proximidad semántica), `evaluate_autonomy` (CONTINUE / STOP / REQUIRES_AUTHORITY / FORBIDDEN con justificación reconstruible) y `summarize_autonomy` (derivado del journal y de los Worker Results; distingue intervención operacional humana de decisión de autoridad humana). **Vocabulario cerrado ampliado** en `contracts.py` (corrección autónoma + condiciones de parada de frontera) y **gate opt-in** en `host.py` (sin envelope declarado el comportamiento es idéntico al actual) con el resumen de autonomía en el run report. **Suite nueva** `tests/test_autonomous_scope.py`: los catorce casos exigidos y la falsación explícita (scope expansion disfrazado, authority expansion, RFC/ADR implícito, cambio de Protocol, cambio de lifecycle, resolución autónoma de decisión humana, release/promotion, documentación normativa inventada). **Decisión de frontera** (`<PLAN-135>:PC-02`): la resolución de un finding —su transición de estado— permanece autoridad humana (CL-8, ADR-16 AU-3); SAE pre-autoriza la **acción de corregir** dentro del scope, que ya autoriza el Plan aprobado, de modo que no se adquiere autoridad nueva ni se modifica ninguna regla normativa. Findings `<PLAN-135>:F-01` (conflicto entre el pedido literal del Change y la regla vigente) corregido por `<PLAN-135>:C-01`. D01 queda habilitado como primer Change funcional ejecutable bajo SAE. `**Status:** Executed` con condición derivada **`Closed`** (docs-only, sin release), Validation Anchor A1 (delta `47042c06…`, tree `16a592c5…`), checkpoint con consistencia PASS verificada por C-2, C-1 `VALID` y C-3 `VALID` (F-1, F-2, C-1, C-2). Findings `<PLAN-135>:F-1` (frontera de autoridad de findings) y `<PLAN-135>:F-2` (registros de lineage no legibles por C-3, detectado por la batería, no por inspección del agente) corregidos por `C-1` y `C-2`, sin marcarlos `resolved` porque esa transición es decisión humana (CL-8, ADR-16 AU-3). Sin `VERSION` bump ni tag. | active |

## Sexagésima sexta serie: integridad de la evidencia de cierre (Plan 134) (15 sep 2026)

Plan 134 (vía plan; docs-only + tooling DEV, sin efecto en `protocol/.agents/`,
RFC-56 no aplica; Change Level L2). Determina la semántica exacta de la cadena de
evidencia de cierre del Change Lifecycle DEV —baseline, anchor, estado validado,
checkpoint, estado de cierre, árbol del commit de cierre, estado commiteado y
`Closed`— y corrige el mecanismo donde la evidencia demuestra defecto. El Plan
133 (`<PLAN-133>:F-5`) había detectado que el closure tree declarado no coincide
con el árbol material del commit de cierre.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `134-closure-evidence-integrity.md` | — (vía plan, docs-only + tooling DEV) | Executed | Integridad de la evidencia de cierre. **Modelo normativo** (nuevo, en `docs/CONVENTIONS.md`): «Estado de cierre, grafo de commit y árbol material» define que el **estado validado**, el **estado de cierre** (lo que el checkpoint certifica, por correspondencia GC-1 con el anchor aplicable) y el **árbol material del commit de cierre** (hecho de Git) son tres conceptos que no se colapsan; `A ≠ B` es **esperado** porque RFC-75 `Mecanismo 7 — Git Checkpoints` declara que el commit de cierre puede incluir governance (INDEX, CHANGELOG, ADR, docs), de modo que `Closed` **no** exige `validated tree == commit tree`; la auto-referencia de un artifact de cierre se resuelve declarativamente (scope fijo antes de escribir los registros; identidad del estado de cierre = par delta + state identity del anchor aplicable; commit localizable por mensaje). **Defecto confirmado (Resultado A) en C-2**: su contrato documentado decía «closure state = tree del commit de cierre final», relación que contradice RFC-75 y que además era **código muerto** en el corpus real —las entradas de commit de cierre de los Planes 120–133 no embeben SHA, así que `ordered_closing_commits` devuelve vacío y la rama de contradicción nunca se ejecutaba—, mientras la relación que sí aplicaba (identidad declarada vs. estado validado del anchor) solo estaba documentada como fallback. Contrato de C-2 fijado en R1–R4 (`docs/CONVENTIONS.md` + `.agents/policies/validation-closure.md:5`, `.agents/policies/lifecycle-checkers.md`, docstring del checker): la divergencia estado-de-cierre ↔ árbol-material es **GAP advisory con requisito de atribución**, no ANOMALY; el nivel ANOMALY del estado de cierre es R2 (correspondencia con un anchor registrado). C-1 y C-3 declarados **NOT_REQUIRED**. **12 Planes históricos (120, 123–133) clasificados CORRECT**: su declaración es la del estado validado, que es exactamente lo que GC-1 exige; no se modificó ninguno. Template de Plan con los tres conceptos separados. Corregidas 2 regresiones de la suite de C-2 que codificaban la semántica superada. Sin RFC/ADR nuevo, sin `VERSION` bump ni tag. | active |

## Sexagésima quinta serie: Roadmap Impact y barrido documental integral (Plan 133) (15 sep 2026)

Plan 133 (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no
aplica; Change Level L2). Formaliza en el Change Lifecycle DEV una determinación
de cierre nueva, **Roadmap impact**, independiente de **Documentation impact** y
con los mismos tres valores (`REQUIRED` / `NOT_REQUIRED` / `DEFERRED`), sin crear
segunda lifecycle, fase, estado, entidad, registry, tracker, checker ni campo
obligatorio nuevos. Además recorre el universo documental real del repositorio y
corrige únicamente la documentación de estado actual materialmente obsoleta,
dejando clasificado lo histórico, lo diferido y lo que requiere autoridad.
Cierra la continuidad de `<PLAN-132>:F-2` / `<PLAN-132>:PC-1`.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `133-roadmap-impact-and-documentary-sweep.md` | — (vía plan, docs-only) | Executed | Formalización del **Roadmap impact** en el Change Lifecycle DEV y barrido documental integral. **Mecanismo**: subsección normativa nueva en `docs/CONVENTIONS.md` (`### Change Lifecycle — Determinaciones de cierre: impacto documental e impacto de Roadmap (regla operacional)`), que además da fuente canónica al **Documentation impact** —que hasta ahora vivía sólo en la policy operativa y en el DoD—; semántica operativa en `.agents/policies/validation-closure.md` §5.2 (con §5.1 y la condición de stop ajustadas); `.agents/workflows/change-lifecycle.md:9. Closure and handoff` con las dos determinaciones; `docs/VERSIONING.md` §10 con las dos en el DoD; y campo `Roadmap impact` en el `## Checkpoint / cierre` de `docs/plans/_TEMPLATE.md`. Regla central: `Roadmap impact: REQUIRED` **no** significa editar `ROADMAP.md` — el artefacto a reconciliar se determina por ownership/source of truth, y `ROADMAP.md` sigue siendo un mapa operativo, no un changelog; las dos determinaciones son independientes en todas sus combinaciones. No se reclama el rótulo «Incremento 5» de RFC-75 (track de coordinación/handoff, fuera de alcance por decisión de la propia RFC). **Barrido y correcciones** (las cuatro confirmadas por el mantenedor): `CHANGELOG.md` header con rutas pre-disolución corregidas (`plans/20-release-adoption.md` → `docs/plans/`, `plans/rfc/` → `docs/rfc/`, `.agents/harness/policies/` y `.agents/orchestrators/*` → `protocol/.agents/…`); `docs/CONVENTIONS.md` con el ancla de migración (`plans/INDEX.md` → `docs/plans/INDEX.md`), la lista de la batería canónica completada a los **seis** checkers + pytest (antes enumeraba tres) y el path histórico de `archive/` explicitado; `docs/plans/INDEX.md` con la atribución de `B-7` corregida (planes 29 y 52; el Plan 43 corresponde a `B-4`, F-04) y el título de la sección del roadmap EC corregido a histórico (sus cuatro planes están `Executed` desde agosto 2026, no son «planes activos»). Documentos **no** modificados con razón verificable: `ROADMAP.md` (su mapa operativo no cambia), `README.md`, `AGENTS.md`, `.agents/AGENTS.md`, `runtime/README.md`, `tests/AGENTS.md`, `protocol/.agents/` completo, `docs/VERSIONING.md` §9 (sin release), RFCs, ADRs y planes cerrados. Sin ADR, sin migración, sin `VERSION` bump ni tag. | active |

## Sexagésima cuarta serie: actualización del Roadmap al estado real (Plan 132) (15 sep 2026)

Plan 132 (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no
aplica). Devuelve a `ROADMAP.md` su función de **mapa operativo actual**:
elimina la tabla histórica B-1…B-8 como backlog y separa explícitamente trabajo
derivado, pendiente arquitectónico que requiere autoridad y candidato futuro. No
implementa ninguna de las tareas que lista, no reabre ítems históricos y no crea
backlog.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `132-roadmap-current-state.md` | — (vía plan, docs-only) | Executed | Reescritura de `ROADMAP.md` como mapa operativo actual. **Desaparece** la tabla `Backlog resuelto` de B-1…B-8 y toda formulación que sugiera que los problemas originales siguen abiertos; `B-5` y `B-6` dejan de figurar como trabajo pendiente. **Trabajo activo / dogfood**: `Mechanical D01 subset — DEV checker for discovery output structure and provenance` (`B-1` **derivado**, próximo dogfood; el contrato D01 declara la validación mecánica como extensión futura inexistente) y `EARS structural validator` (`B-2` **derivado**, siguiente dogfood después de `B-1`; plan 33). **Pendientes que requieren autorización** (los tres afectan contratos del payload): `F-14`+`F-17` de discovery (`B-4` residual), `project_shape` para repositorios documentales/protocolo (`B-7` residual, `F-16`) y el slot de session risk de single-instance en el catálogo de `protocol/.agents/contracts/METRICS.md` (`B-8` residual, baja prioridad). **Candidato futuro**: checker mecánico de `.last_discovery` (`B-3` extensión, plan 50), no autorizado ni planificado. El Roadmap declara el criterio de prioridad —herencia del ítem histórico, salvo el orden de dogfood— y no recalifica prioridades sin evidencia nueva. Registró el hallazgo `<PLAN-132>:F-1` (el Plan 133 citado como evidencia principal **no existe**; la clasificación B-1…B-8 se re-verificó de forma independiente contra `docs/plans/INDEX.md`, el anexo A de bitácora de fricciones, el contrato D01 y `METRICS.md`; el mantenedor autorizó ejecutar el Change con el próximo número libre) y el hallazgo diferido `<PLAN-132>:F-2` (la atribución de `B-7` al Plan 43 en este mismo INDEX corresponde a `B-4`; no corregida aquí por scope, continuidad en `<PLAN-132>:PC-1`). Sin tareas nuevas, sin ADR, sin migración, sin `VERSION` bump ni tag. | active |

## Sexagésima tercera serie: implementación mecánica del Placement Contract (Plan 131) (15 sep 2026)

Plan 131 (vía plan; DEV `runtime/` + `tests/`, sin efecto en `protocol/.agents/`,
RFC-56 no aplica). Materializa `docs/placement-contract.md` como un resolver
determinista: `PLACE` con el namespace canónico y la regla que lo autoriza, o
`STOP` con el disparador que falta. Consume `PLAN-129:DEC-2` (enforcement
autorizado como dirección futura) y no reinterpreta el contrato.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `131-placement-contract-mechanical-implementation.md` | — (vía plan, DEV runtime/tests) | Executed | Implementación mecánica del Placement Contract. **Nuevo paquete `runtime/placement/`**: `rules.py` (realización de la tabla de familias del contrato §6 con la procedencia de sección de cada fila, el discriminante estructural `flat` de las formas `(root)`/`(flat)`, familias root-anchored y artefactos de path exacto), `resolver.py` (algoritmo §7 en su orden: identificación semántica → dominio → kind/familia dentro del dominio → namespace canónico → canonicality como cualificador → autoridad/lifetime como metadata → constraints → `PLACE`; más `verify_path()` para `§16 PC-51`), `__init__.py` (superficie pública). **Tres suites nuevas**: `tests/test_placement_resolver.py` (comportamiento y falsación de la propiedad central), `tests/test_placement_contract_drift.py` (guarda de deriva: namespaces, familias, disparadores de STOP, canonicalities y semántica de Git persistence sin interpretar prosa) y `tests/test_placement_dogfood.py` (módulo anclado al repo real, sólo lectura: evidencia `PLACE` citando §6 y `STOP` con lo requerido). Propiedad garantizada: `regla explícita → PLACE`; `sin regla / ambigua / información insuficiente → STOP`; `guess plausible → NUNCA PLACE`. `canonicality` nunca selecciona ni crea namespace; `kind` no es un enum global cerrado; las excepciones son entrada del llamador, no registry. **Es una librería, no un hook**: `PC-78`/`PC-79` excluyen el hook del Orchestrator y `PC-73` lo define como consumidor, así que no se integra en `runtime/orchestrator/`. Findings `F-1`..`F-3` (tabla realizada más amplia que el contrato; `historical` como licencia de ubicación; nombre de familia sin contrapartida) corregidos por `C-1`. `docs/placement-contract.md` con **0 diff**. Sin entidad/registry/ID/state machine/autoridad/lifecycle/taxonomía global nuevos; sin CI, hook, branch protection ni enforcement global; sin ADR; sin migración. Sin `VERSION` bump ni tag. | active |

## Sexagésima segunda serie: corrección nomenclatural de Plan 129 (Plan 130) (15 sep 2026)

Plan 130 (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica).
Corrige la colisión de identificadores detectada en `<PLAN-129>:F-2`: los
identificadores de decisión de Plan 129 pasan a `PLAN-129:DEC-1/2/3`, sin tocar
las etiquetas de regla del Placement Contract. No crea ADR, no introduce
convención global de nomenclatura, no migra nada y no altera ninguna semántica.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `130-nomenclature-fix-plan-129-identifiers.md` | — (vía plan, docs-only) | Executed | Corrección nomenclatural: renombra **únicamente** los identificadores de decisión de Plan 129 —`PC-1`/`PC-2`/`PC-3` → `PLAN-129:DEC-1`/`PLAN-129:DEC-2`/`PLAN-129:DEC-3`— para que el namespace textual de decisión deje de colisionar con las etiquetas de regla internas de `docs/placement-contract.md` (`PC-1`…`PC-80`, más `PC-31a`…`PC-31c`). El contrato queda **con 0 diff**: 80 reglas y 3 variantes intactas, sin renumerar ni cambiar contenido normativo. Marca `<PLAN-129>:F-2` como `resolved` y registra `<PLAN-129>:C-2`; retira el pending de nomenclatura. Alinea además dos referencias al pending de persistencia heredado del Plan 128 (`docs/plans/INDEX.md`, `CHANGELOG.md`) que usaban la misma etiqueta para la misma decisión. **No** generaliza la convención a otros planes. Semántica de `DEC-1`/`DEC-2`/`DEC-3` sin cambios. Sin `VERSION` bump ni tag. | active |

## Sexagésima primera serie: cierre de DEC-1, DEC-2 y DEC-3 del Placement Contract (Plan 129) (15 sep 2026)

Plan 129 (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica).
Cierra las tres decisiones pendientes del Repository/Artifact Placement Contract
como un único Change integral, sin implementar el enforcement. No crea ADR, no
migra nada y no modifica el Change Lifecycle.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `129-pc1-pc2-pc3-closure.md` | — (vía plan, docs-only) | Executed | **`PLAN-129:DEC-1` = CLOSED**: `.project/changes/` es **project-durable** y **Git-persisted**, con las tres propiedades separadas literalmente (`project-durable` = persistencia · `git-persisted` = preservación/versionado por Git · `git commit` = **operación** gobernada por el Change Lifecycle y su autoridad); sin auto-commit, sin `always`/`never commit`, sin `auto-ignore`; el contrato no adquiere autoridad para ejecutar commits ni modifica el Change Lifecycle (§6, §7 paso 6, §21 `PC-67`…`PC-71`). **`PLAN-129:DEC-2` = CLOSED con implementación diferida**: el enforcement mecánico y determinista queda **autorizado como dirección futura** con boundary `Contract = fuente normativa · Enforcement = realización mecánica · Orchestrator = consumidor`, prohibición de segunda fuente normativa, regla «si implementación y contrato discrepan, gobierna el contrato», y las ocho invariantes **E-1…E-8** (determinismo; placement explícito; STOP; no guessing; el enforcement no es source of truth; separación de autoridad; el Orchestrator no reinterpreta STOP como PLACE; escalado humano). **NO implementado**: sin checker, resolver, servicio, hook, integración CI, registry, schema, database ni state machine (§22 `PC-72`…`PC-77`, §23, §24 `PC-79`/`PC-80`). **`PLAN-129:DEC-3` = CLOSED**: las excepciones son **documentales por defecto**, sin representación estructurada ni identificadores, con el procedimiento localizar → verificar owner → interpretar → aplicar → STOP, y **sin** prohibición permanente de una representación futura (§9 `PC-31a`…`PC-31c`). Equivalencias del apéndice actualizadas (`project-durable ≠ git commit operation`, `exception ≠ registry`, `enforcement ≠ source of truth`, `STOP ≠ GUESS`). Registró como finding la colisión de etiquetas entre las decisiones de plan (`PC-1/2/3`) y las reglas internas del contrato (`PC-1`…`PC-80`), resuelta por el renombrado autorizado de Plan 130 a `PLAN-129:DEC-1/2/3`, sin renumerar las reglas del contrato ni generalizar la convención. Sin `VERSION` bump ni tag. | active |

## Sexagésima serie: materialización del Repository/Artifact Placement Contract (Plan 128) (15 sep 2026)

Plan 128 (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica).
Materializa el **Repository/Artifact Placement Contract** como documento normativo
independiente bajo `docs/`, derivado del diseño cerrado en Plan 127 y de las
decisiones humanas `OQ-2 = NO`, `OQ-3 = A`, `OQ-4 = NO`, con `DEC-1` (persistencia) mantenido
`OPEN / DEFERRED`. No crea registry, checker, schema, namespace, state machine,
clase de autoridad ni ADR; no integra enforcement en runtime/Orchestrator/CI; no
autoriza migración.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `128-placement-contract-materialization.md` | — (vía plan, docs-only) | Executed | Materializa `docs/placement-contract.md`: 22 secciones numeradas con reglas normativas `PC-1`..`PC-70` (purpose/scope, applicability, domain identification, kind/family, canonicality qualification, namespace selection con tablas domain-scoped, algoritmo de 8 pasos, STOP semantics, excepciones, move/rename, distribución, históricos, fixtures, scratch, generado/derivado, responsabilidades del agente, frontera de autoridad humana, relación con `AGENTS.md`, navegación INDEX, relación con ADR-17/ADR-18, `Deferred: PC-1` y non-goals). **OQ-2 = NO**: las excepciones se registran en el artefacto que posee la decisión, acotadas al artefacto o la familia, sin registry/schema/database/índice global/identity primitive, y sin prohibir que una decisión futura introduzca una representación machine-locatable. **OQ-3 = A**: documento independiente `docs/placement-contract.md`, sin namespace nuevo, con `AGENTS.md` sólo referenciándolo para discovery. **OQ-4 = NO**: sin ADR nuevo; el contrato materializa ADR-17 y ADR-18 y se declara downstream de ambos. **PC-1**: sección `Deferred: PC-1` que registra `project-durable ≠ git-committed` sin establecer política de Git. Regla central: *canonicality qualifies placement; it does NOT determine placement*; el algoritmo termina en `PLACE` o `STOP` y `GUESS` no es admisible. Sin `VERSION` bump ni tag. | active |

## Quincuagésima novena serie: cierre de diseño del Repository/Artifact Placement Contract (Plan 127) (15 sep 2026)

Plan 127 (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica).
Registra el cierre formal del **diseño** del Repository/Artifact Placement Contract y
persiste como traza versionada su modelo semántico corregido, su algoritmo de
resolución, su modelo de STOP y sus decisiones pendientes. El plan **no** materializa
el contrato, no crea registry, checker, schema, namespace ni ADR, y no autoriza
migración alguna. Depende de ADR-17 y ADR-18 como arquitectura upstream, que no
modifica. **`Design: CLOSED` · `Placement Contract: NOT CREATED` · `Migration: NOT STARTED`.**

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `127-repository-artifact-placement-contract-design.md` | — (vía plan, docs-only) | Executed | Diseño del Repository/Artifact Placement Contract: tesis central `domain/owner → kind/family → family rule → canonical namespace → canonicality qualification → constraints → PLACE \| STOP`; **dos discriminadores** (dominio/owner, kind/family) y **un cualificador** (canonicality), con la regla universal de que canonicality nunca selecciona ni crea namespace; `kind` **no** es enum global cerrado (tabla domain-scoped, alineada con ADR-18 `RS-11`); **15 familias canónicas + 3 reglas root-anchored + 2 no-familias**; modelo de canonicalidad corregido (`generated ≠ non-canonical`, `derived ≠ same namespace`; la ubicación proviene siempre de una regla explícita y su ausencia produce `STOP (UNDEFINED PLACEMENT)`, sin STOP nuevo); algoritmo de 8 pasos; 9 triggers de STOP mapeados al vocabulario existente (GAP / ANOMALY / `REQUIRES_HUMAN`) sin crear clase de autoridad, estado de lifecycle ni estado de state machine; modelo de excepciones acotado al artefacto que posee la decisión (sin registry); move/rename separado del placement nuevo (`RS-7`, RFC-46); distribución declarada **domain+namespace-scoped** (`protocol/.agents/` se distribuye; el `.agents/` de DEV nunca); lifetime semántico, sin topología (`RS-2`/`RS-5`); contrato del agente para 5 casos (nuevo, dudoso, no canónico pedido, familia nueva, cross-domain); tabla de machine-verifiability; integración con el Orchestrator como consulta (preflight antes de delegar, verificación de scope después, evidencia en el cierre) sin gate ni registry; current→target sin migración; y registro de las correcciones C1–C9 con BEFORE/AFTER/REASON. Recomendación (no decisión): variante **B — Structured placement**. Deja **explícitamente abiertas** `OQ-2` (excepciones machine-locatable), `OQ-3` (ubicación canónica del contrato), `OQ-4` (ADR-worthiness de la materialización) y `PC-1` (persistencia Git de `.project/changes/`). Sin `VERSION` bump ni tag. | active |

## Quincuagésima octava serie: materialización de las decisiones C–K (Plan 126) (15 sep 2026)

Plan 126 (vía plan, **Clase B** de RFC-56: mejora documental compatible). Materializa
las decisiones arquitectónicas C–K aceptadas por el mantenedor a partir de la
síntesis posterior a ADR-17, y deja el Repository/Artifact Placement Contract como
trabajo posterior no diseñado. No crea entidad, registry, estado de lifecycle,
clase de autoridad ni mecanismo nuevos; no migra artefactos.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `126-repository-architecture-decisions-ck.md` | — (vía plan, Clase B RFC-56) | Executed | Materialización de **C1** (los harness tests de `.agents/harness/tests/` son parte del payload distribuido y suite de regresión del harness; los cinco checkers de `tools/` siguen DEV-only: declarado en `.agents/harness/INDEX.md`), **D4** (el payload conserva sus dos citas de fuente normativa `docs/rfc/` mediante una excepción acotada al par (archivo citante, target exacto), explícita y auditable; `functional_writer.md` aclarado como carpeta del proyecto adoptante), **E1** (`docs` añadido al boundary declarado del checker existente —sin checker nuevo— más la allowlist de provenance, con 4 tests: `docs/` ordinario rechazado, provenance allowlisted aceptada, la allowlist no autoriza otros `docs/`, no aplica a archivo no listado), **G2+G1** (`tags` declarado vocabulario documentado y no cerrado; `tags.kind` no exhaustivo/extensible; `state_machine` y `taxonomy` añadidos; ningún consumidor reescrito), **H** derivada de A3+B4 (clasificación documental corregida **en el lugar**: `docs/architecture/` → Historical/`archived`, `docs/AUDITORIA_DOCUMENTACION.md` → Working/Audit de raíz, mapa folder→clase con columna de lifecycle; sin movimiento ni clases nuevas), **I** derivada de C1 (harness sin reestructurar), **J1** (INDEX opcional y semántico, nunca autoridad; ningún INDEX creado) y **K3** (`health_check.py` sin cambios; el directorio efímero del probe aceptado como correcto; clarificación documental mínima). Registrado en `docs/adr/18-payload-boundary-provenance-and-classification.md`. Sin `VERSION` bump ni tag. | active |

## Quincuagésima séptima serie: decisiones arquitectónicas de estructura del repositorio (Plan 125) (15 sep 2026)

Plan 125 (vía plan; docs-only, sin efecto en `protocol/.agents/`, por lo que
RFC-56 no aplica). Registra las decisiones arquitectónicas humanas tomadas por
el mantenedor sobre la estructura del repositorio, derivadas de la Repository
Structure Architecture Review (read-only, `dev` @ `4cd11ed`) y de su Repository
Architecture Decision Set (A–K, L). El plan **no** diseña el Repository/Artifact
Placement Contract, **no** migra artefactos, **no** resuelve las decisiones
abiertas C, D, E, G, H, I, J y K, y no introduce entidad, registry, estado de
lifecycle, clase de autoridad ni mecanismo de governance nuevos.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `125-repository-architecture-decisions.md` | — (vía plan; RFC-56 no aplica) | Executed | Registro formal de las decisiones humanas **A3** (lifetime permanece como propiedad semántica en `docs/`, sin dimensión física general del árbol; se admite separación física específica dentro de `.project/` entre estado durable y session-ephemeral), **B4** (arquitectura estructural compuesta por namespace/dominio; ninguna estrategia física global obligatoria; B4 no autoriza migración por sí mismo), **F1** (`.project/changes/` conserva su path; el contrato Protocol debe distinguir explícitamente project-durable de session-ephemeral; «durable» no implica Git-committed; sin mover, sin cambiar `.gitignore`, sin tocar runtime resolvers) y **L1** (A y B son ADR-worthy; materializado como `docs/adr/17-repository-lifetime-and-composite-structure.md` dentro del mismo Change, conforme a `docs/CONVENTIONS.md:Convenciones`). Incluye la sección explícita de decisiones **ABIERTAS** C/D/E/G/H/I/J/K con su autoridad requerida y dependencia, el límite del siguiente paso (Repository/Artifact Placement Contract, derivado de artifact/nature, owner/domain, authority, lifecycle, persistence, scope, consumption, creation, mutation, discovery, canonicality e historical status, **no diseñado**) y los pendientes `PC-1` (semántica de lifetime/persistence en el contrato Protocol → RFC-56), `PC-2` (separación física dentro de `.project/`) y `PC-3` (las ocho decisiones abiertas). Docs-only: sin `VERSION` bump ni tag (RFC-69). | active |

## Quincuagésima sexta serie: cierre de hallazgos de arquitectura de `tests/` (Plan 124) (15 sep 2026)

Plan 124 (vía plan; sin efecto en `protocol/.agents/`, por lo que RFC-56 no
aplica; régimen aplicable RFC-75). Cierra los tres hallazgos accionables de la
revisión integral de arquitectura de `tests/` (read-only, `dev` @ `4aa2617`),
cuyo veredicto global fue `KEEP + REFACTOR SELECTIVE`: la organización plana de
`tests/` es intencional y se conserva, `tests/fixtures/skills/` permanece donde
está (fixture sintético, no Skill canónica), `.agents/skills/` no se crea y no
se introduce split `unit/`/`integration/`/`contract/`. El plan **no** modifica el
payload, no reabre RFC/ADR/planes cerrados y no altera la arquitectura del
Change Lifecycle.

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `124-tests-architecture-findings.md` | — (vía plan; RFC-56 no aplica) | Executed | Cierre de F-01/F-02/F-03 de la revisión de arquitectura de `tests/`: mecanismo único de importación de `tools/` en la sesión de test (`conftest.py`) en lugar de `sys.path.insert` por archivo (18 archivos; F-01), corrección de `tests/AGENTS.md` para distinguir tests aislados de repositorio sintético frente a tests anclados intencionalmente al repositorio real y al dogfood sobre `protocol/` (F-02), y consolidación del chequeo «solo stdlib» duplicado en siete suites en un helper acotado `tests/testsupport.py` conservando el conjunto de módulos locales de cada caso, incluido el conjunto vacío de lineage (F-03). Verificación: seis checkers canónicos PASS, `pytest -k stdlib` 7 passed; la pierna completa `python -m pytest tests/` queda como **GAP** por clase ambiental declarada (sandbox sin mecánica de directorios temporales de pytest), nunca como `PASS`. Validation Anchor A1 (delta `64810a61…`, tree `192997ae…`); C-1/C-2/C-3 `VALID` sobre el árbol final. Condición derivada **`Closed`** (docs-only, sin release). Sin payload, sin `VERSION`, sin tag, sin promoción. | active |

## Serie de RFCs (documentos canónicos)

> Registro migrado a `docs/rfc/INDEX.md` (RFC-69). Las RFCs viven en
> `docs/rfc/`; esta sección se conserva como ancla de navegación para
> referencias históricas.

## Roadmap de implementación del Execution Context (histórico: planes 04–07, todos `Executed`)

> Sección histórica: es el roadmap del Execution Context Pipeline, cerrado en
> los planes 04–07 (agosto 2026). No es el mapa de trabajo activo —el mapa
> operativo actual es `ROADMAP.md`— y se conserva como traza de navegación.

```text
Nivel 1  Cierre del pipeline principal ──┐ (paralelizable)
Nivel 2  Especialización de Resolution ──┘ (solo depende de RFC-00YC)
   │
Nivel 3  Especialización de Composition  (requiere Nivel 1)
   │
Nivel 4  Materialización                 (requiere Nivel 1; conceptualmente Nivel 3)
```

| Plan | Status | Depende de | Descripción | Vigencia |
|---|---|---|---|---|
| `04-main-pipeline-closure.md` | Executed | — | RFC-00YD Composition + updates a RFC-00XZ y `feature.md` + regularización de status. | active |
| `05-resolution-specialization.md` | Executed | RFC-00YC | RFC-00YE Conflict Classification → 00YF/00YG/00YH + updates a RFC-00YC y `feature.md`. | active |
| `06-composition-specialization.md` | Executed | Nivel 1 | RFC-00YI Compression, RFC-00YJ Optimization. | active |
| `07-materialization.md` | Executed | Nivel 1 (+3 conceptual) | RFC-00YK Materialization → 00YL Prompt Rendering, 00YM Skill Materialization. | active |

## Segunda serie: explicitud de decisiones (después de 04–07)

```text
08  Correcciones transversales ─── ejecutable YA, en paralelo (no toca el roadmap EC)
09  Orchestrator Decision Model ── depende de 08
10  Failure & Recovery Taxonomy ── depende de 09
11  Delegation Validity Model ──── depende de 04–07
12  Selection Models ───────────── depende de 11 y 04–07
13  Session & Iteration Lifecycle ─ independiente, paralelizable
14  Declarative-Flag Compliance ── independiente, paralelizable
```

| Plan | Status | Depende de | Cierra | Vigencia |
|---|---|---|---|---|
| `08-correcciones-transversales.md` | Executed | — | Contradicción de bootstrap + fixes stale en `.agents/` (gaps 6 y 9). | active |
| `09-orchestrator-decision-model.md` | Executed | 08 | Catálogo conceptual de decisiones del Orchestrator + unificación de confianza (gaps 1 y 8). | active |
| `10-failure-recovery-taxonomy.md` | Executed | 09 | Clasificación de fallos y audiencia máquina/agente de policies (gap 5). | active |
| `11-delegation-validity-model.md` | Executed | 04–07 | Validez conceptual de payloads y return reports; resuelve el huérfano `context_budget: 4000` (gap 2). | active |
| `12-selection-models.md` | Executed | 11, 04–07 | Modelos de candidatura/selección de perfil y skill (gap 3). | active |
| `13-session-iteration-lifecycle.md` | Executed | — | Ciclo de vida de sesión, iteraciones y `<order>` (gap 4). | active |
| `14-declarative-flag-compliance.md` | Executed | — | Obligación y evidencia de flags `[declarative]` (gap 7). | active |

## Tercera serie: de protocolo explícito a protocolo operativo (después de 04–14)

```text
15  Policy Layer I (H15 + Budget materializado) ── depende de 11, 07
16  Policy Layer II (Resolution/Composition) ──── depende de 05, 06, 15
17  Protocol Metrics Model ────────────────────── depende de 09, 10; paralelo a 15
18  Segunda Materialización (MCP/tools/memoria) ─ depende de 07
19  Dogfooding End-to-End ─────────────────────── depende de 04–14 (+15, 17)
20  Release & Adoption ────────────────────────── depende de 19
```

| Plan | Status | Depende de | Descripción | Vigencia |
|---|---|---|---|---|
| `15-policy-layer-1-delegation-budget.md` | Executed | 11, 07 | Primera policy real del protocolo (H15) + materialización del Budget para el runtime prompt. | active |
| `16-policy-layer-2-resolution-composition.md` | Executed | 05, 06, 15 | Policies concretas de desempate, deduplicación, merge, compresión y optimización. | active |
| `17-protocol-metrics-model.md` | Executed | 09, 10 | Modelo de métricas del protocolo: registro, agregación y señales de salud. | active |
| `18-segunda-materializacion.md` | Executed | 07 | Prueba de fuego de la tesis runtime-independent: materialización no-prompt del Execution Context. Tesis verificada: modelo intacto; segunda materialización (tool calls) en `runtime/`. | active |
| `19-dogfooding-end-to-end.md` | Executed | 04–14 (+15, 17) | Proyecto real ejecutado por protocolo; backlog evidenciado de la siguiente generación. Anexos: `19-anexo-a-bitacora-fricciones.md`, `19-anexo-b-reporte-estado.md`. | active |
| `20-release-adoption.md` | Executed | 19 | Versionado, changelog, migración, onboarding y tag 1.0.0 del protocolo. | active |

## Cuarta serie: Core Skills Pack

| Plan | Status | Depende de | Descripción | Vigencia |
|---|---|---|---|---|
| `21-core-skills-pack.md` | Executed | RFC-16 Accepted | Implementación por tandas del Core Skills Pack definido en RFC-16 (`rfc/16-core-skills-catalog-model.md`). | active |
| `22-skills-pack-2.md` | Executed | 21 | Segundo pack: 16 Skills complementarias seleccionadas con los criterios C1–C4 de RFC-16 entre las candidatas no excluidas. | active |

## Quinta serie: de protocolo declarativo a protocolo enforced (5 ago 2026)

Serie derivada del análisis crítico de adopción (5 ago 2026): enforcement voluntario, validación solo estructural, coste operativo uniforme, skills huérfanas y duplicación policy↔contrato. Cada plan implementa su RFC homóloga (24–28, todas Proposal).

```text
23  Skill Lifecycle (cable-or-kill) ──── independiente, paralelizable
24  Single-Source Required-Sections ──── independiente, paralelizable
25  Task Profile Model ───────────────── recomienda 24
26  Hook-Based Enforcement ───────────── recomienda 25
27  Harness Coverage Closure ─────────── depende de 24
```

| Plan | Status | Depende de | Descripción | Vigencia |
|---|---|---|---|---|
| `23-skill-lifecycle.md` | Executed | — | Cable-or-kill de skills: ~30 skills huérfanas se cablean a fases/policies o se eliminan del catálogo activo (RFC-24). | active |
| `24-single-source-required-sections.md` | Executed | — | El runner resuelve `required_sections` del contrato por referencia (8 policies derivadas; 7 conservan override explícito); `sync_required_sections.py` eliminado (RFC-25). | active |
| `25-task-profile-model.md` | Executed (dogfood del perfil `trivial`: **actividad externa de adopción**, no backlog — determinación del Plan 143; el modo enforced del plan 26 sí quedó verificado por el plan 46) | recomienda 24 | Perfiles `trivial`/`standard`/`complex` con bifurcación de artefactos y gates; meta: tarea trivial ≤ 5 archivos, ≤ 3 gates (RFC-26). La **medición** real exige una versión promovida y una sesión con el usuario: se registra como actividad externa no ejecutada (`docs/plans/143-empty-remaining-backlog.md`); el perfil está declarado e implementado en `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`. | active |
| `26-hook-enforcement.md` | Executed (dogfooding verificado 12 ago 2026, plan 46) | recomienda 25 | `state.json` escrito solo por el runner + hooks bloqueantes `PreToolUse`/`Stop` compartidos entre CLIs, con defensa en capas (RFC-27). | active |
| `27-harness-coverage-closure.md` | Executed | 24 | Declaración `enforcement` en los 25 contratos + checks semánticos mecánicos (citas existentes, evidencia de tests) en el runner (RFC-28). | active |

Nota de status: los planes 23–27 usan `Proposed` como estado previo al ciclo vigente (el ciclo de planes definido en §Convenciones no contempla borradores; al aprobarse pasan a `Aprobado para ejecución` o `Aprobado para redacción` según entregable).

**Regularización de gobernanza (11 ago 2026, RFC-42/plan 41):** las RFC-24…28
pasan a `Accepted` retroactivamente, con evidencia en sus Amendment Logs (planes
23–27 `Executed` + `CHANGELOG.md` 2.0.0); el status `Proposal` era un desfase
documental, no una falta de aprobación. Regla vigente para el futuro: una
modificación de `.agents/` requiere **vía RFC Accepted** o **vía plan Aprobado
para ejecución** con justificación documentada; la referencia en
`ANTI_CIRCUMVENTION.md` queda pendiente de la aceptación de RFC-42 (plan 41
`Executed (parcial: ...)`).

## Sexta serie: remediación de la auditoría 2.0.1 (11 ago 2026)

Serie derivada de la auditoría de estado del protocolo 2.0.1 (2026-08-11). Cada
par RFC + plan corresponde a un subpunto de la auditoría; los defectos idénticos
detectados en más de una sección se cubren una sola vez (mapeo en la columna
"Origen"). Las RFCs están en `Proposal` y los planes en `Aprobado para
redacción`; según la regla de gobernanza (RFC-42), ningún cambio de `.agents/`
se ejecuta antes de que la RFC esté `Accepted` o el plan esté `Aprobado para
ejecución` con justificación. Excepción aplicada el 11 ago 2026: los planes
34–36 pasaron a `Aprobado para ejecución` por vía plan (RFC-42) tras la
auditoría de planes y quedaron `Executed`, con justificación documentada en
cada plan.

Estado al cierre del 11 ago 2026: RFC-29…31 `Accepted` y planes 28–30 `Executed`
por implementación autorizada explícitamente por el usuario; el resto de la serie
sigue en `Proposal` / `Aprobado para redacción` salvo los planes 34–36, que
pasan a `Aprobado para ejecución` el 11 ago 2026 tras la auditoría de planes;
los planes 34–36 quedaron `Executed` el 11 ago 2026 (RFC-35…37 permanecen en
`Proposal`, pendientes de regularización de gobernanza).

| Plan | RFC | Origen (auditoría 2.0.1) | Descripción | Vigencia |
|---|---|---|---|---|
| `28-h07-user-authorized-extra-work.md` | RFC-29 | 1.1 | H07: dos ramas de scope compliance (extra autorizado con evidencia). | active |
| `29-recovery-to-early-phases.md` | RFC-30 | 1.2 / 3.1 | Aristas de RECOVERY a fases tempranas + retry sin transición (F-02/F-03). | active |
| `30-abort-artifact-flow.md` | RFC-31 | 1.3 / 3.4 | ABORT en RECOVERY_REPORT, workflow 08 y hook de cierre. | active |
| `31-phase-02-profile-unification.md` | RFC-32 | 1.4 | Rol único `task_specification_writer` para la fase 02. | active |
| `32-execution-summary-steps-schema.md` | RFC-33 | 1.5 | Unificar la lista de pasos en `steps_executed`. | active |
| `33-ears-criteria-canonical-form.md` | RFC-34 | 2.1 | Bullets EARS como forma canónica (F-01). | active |
| `34-verify-workflow-inputs.md` | RFC-35 | 2.2 | Inputs y decisión del workflow 07. | active |
| `35-plan-workflow-inputs.md` | RFC-36 | 2.3 | Inputs del workflow 05. | active |
| `36-gather-context-h10-declaration.md` | RFC-37 | 2.4 | H10 como gate opcional de uso, no de transición. | active |
| `37-task-analysis-confidence-blocks.md` | RFC-38 | Executed (12 ago 2026, 3.1.0) | Semántica de los bloques de confianza del análisis. | active |
| `38-discovery-context-budget.md` | RFC-39 | Executed (12 ago 2026, 3.2.0) | Config de `context_budget` y muestreo (F-13). | active |
| `39-kb-discovery-entry-produced-by.md` | RFC-40 | Executed (12 ago 2026, 3.2.1) | Procedencia real de las entradas de KB. | active |
| `40-discovery-artifact-boundaries.md` | RFC-41 | Executed (12 ago 2026, 3.3.0) | Fronteras de intermedios + namespacing `<order>` (F-11/F-20). | active |
| `41-rfc-plan-status-governance.md` | RFC-42 | 2.9 | Gobernanza RFC Proposal vs planes Executed (23-28). **Regularización aplicada el 11 ago 2026** (RFC-24…28 → Accepted retroactivo); referencia en `ANTI_CIRCUMVENTION.md` cerrada por el plan 56 (12 ago 2026). | active |
| `42-h13-planned-cleanup.md` | RFC-43 | Executed (12 ago 2026, 3.3.1) | Limpieza de la regla de entidades `planned`. | active |
| `43-intent-reflection-auto-confirm.md` | RFC-44 | Executed (12 ago 2026, 3.3.2) | Estado productor de la reflexión HIGH (F-04). | active |
| `44-unattended-clarification.md` | RFC-45 | Executed (12 ago 2026, 3.4.0) | Modo desatendido de clarificación (F-05). | active |
| `45-historical-trace-policy.md` | RFC-46 | Executed (12 ago 2026, 3.4.1) | Versión de protocolo en trazas e interpretación histórica. | active |
| `46-enforced-mode-dogfooding.md` | RFC-47 | Executed (12 ago 2026, 3.7.0) | Dogfooding del modo enforced (state.json + hooks). | active |
| `47-discovery-per-entry-contracts.md` | RFC-48 | Executed (14 ago 2026, 3.8.0) | Contratos por entrada de discovery; single-source en D01. | active |
| `48-protocol-skill-mechanical-validation.md` | RFC-49 | Executed (12 ago 2026, 3.4.2) | Verificación mecánica dev-only de skills. | active |
| `49-delegation-single-instance-model.md` | RFC-50 | Executed (12 ago 2026, 3.5.0) | Modos de ejecución de delegaciones (F-09). | active |
| `50-discovery-kb-freshness.md` | RFC-51 | Executed (12 ago 2026, 3.6.0) | Frescura de KB, marcador único y revalidación por pipeline (F-12). | active |
| `51-worker-role-phase-catalog.md` | RFC-52 | Executed (12 ago 2026, 3.6.1) | Catálogo de fases y skills de los roles de worker. | active |
| `52-tooling-profile-candidacy.md` | RFC-53 | Executed (12 ago 2026, 3.6.2) | Candidatura tooling/CLI (F-06). | active |
| `53-discovery-contract-wording.md` | RFC-54 | Executed (12 ago 2026, 3.6.3) | Redacción de EXECUTIVE_SUMMARY y hash calculation (F-15/F-19). | active |

## Séptima serie: source containment del repo fuente (12 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `54-protocol-source-containment.md` | RFC-55 | Executed (12 ago 2026) | Payload del producto en `protocol/` (`protocol/.agents/` + `protocol/_AGENTS.md`), AGENTS.md raíz de desarrollo, tooling/CI con `--payload protocol`, y consolidación de `dev/` (README, ROADMAP, source-layout). `dist` no cambia. | active |
| `55-hook-setup-self-containment.md` | — (vía plan) | Executed (12 ago 2026) | Autocontención del setup de hooks en el payload; elimina la referencia a `ADOPTION.md` desde `harness/INDEX.md`. | active |
| `56-payload-immutability-anti-circumvention.md` | — (vía plan) | Executed (12 ago 2026) | Regla inline de inmutabilidad del payload en `ANTI_CIRCUMVENTION.md` (cierra el pendiente del plan 41). | active |
| `57-governance-classes-rollout.md` | RFC-56 | Executed (12 ago 2026) | Implementación de las clases A/B/C en las fuentes de verdad + revisión individual de RFC-32…54. | active |

## Octava serie: remediación de la auditoría de sistema (14 ago 2026)

| Plan | RFC | Status | Descripción | Vigencia |
|---|---|---|---|---|
| `58-remediacion-nivel-2.md` | RFC-30, RFC-54 | Executed | Alineación del payload con modelos Accepted: actor único de hashes (completa plan 53), enum de `RECOVERY_REPORT` con fases tempranas (completa plan 29), metadata de contratos de discovery. Versión 3.9.0. | active |
| `59-remediacion-nivel-3.md` | RFC-26 (enmendada), RFC-30 | Executed | Camino trivial legalizado (`ANALYZING_TASK → PLANNING` condicionada al perfil, inputs reducidos) y taxonomía `RECOVERY`/`ANALYZING_TASK` alineada con la máquina de estados. Versión 3.10.0. | active |
| `60-remediacion-nivel-6.md` | — (Clase B) | Executed | Lote fácil: excepción single-source, convención `[Unreleased]`, contrato de evento de hook, modelo D01 aclarado, semántica de `retry_count`. Versión 3.11.0. | active |
| `61-remediacion-p1-2.md` | — (Clase B) | Executed | Dominios canónicos de `produced_by` (contratos) y `profile` (workflows), con enforcement en el checker de coherencia taxonómica. Versión 3.12.0. | active |
| `62-remediacion-p2-1-p4-3.md` | — (Clase B) | Executed | Context Budget declarado advisory (P2.1) y contratos versionados con `schema_version` (P4.3), con enforcement en el checker. Versión 3.13.0. | active |
| `63-remediacion-p4-2.md` | — (Clase B) | Executed | Mapeo determinista de sesión CLI ↔ protocolo (`.project/.sessions.json`) en `hook_gate.py` + `runner_state.py link`. Versión 3.14.0. | active |
| `64-remediacion-f1-a.md` | — (Clase B) | Executed | Modelo de enforcement declarado en tres capas (enforced/reviewed/verified); rewordings de policies, HARNESS_REPORT y H13. Versión 3.15.0. | active |
| `65-remediacion-f7-f5.md` | — (Clase B) | Executed | Evidencia de flags declarada (expected/evidenced/unevidenced) y modelo de determinismo de contexto declarado. Versión 3.16.0. | active |
| `66-harness-structural-validator.md` | RFC-57 | Executed | Validador estructural opcional del harness (`gate_validator.py`) como soporte mecánico de los ítems `[gate]`. Versión 3.17.0. | active |
| `67-remediacion-b-6.md` | — (Clase B) | Executed | Soporte estructural de H15 en el runner (`validate-delegation`/`validate-return`). Versión 3.18.0. | active |
| `68-mandatory-structural-validator.md` | RFC-58 | Executed | Validador estructural obligatorio a nivel de gate (MUST antes del PASS; FAIL estructural bloquea salvo desviación documentada). Versión 3.19.0. | active |

## Backlog evidenciado - plan 19

(5 ago 2026.)

> **Registro histórico, no backlog abierto (reconciliado por el Plan 145, 2026-09-21).**
> Esta sección es la traza del backlog evidenciado por el dogfooding del plan 19 al
> 5 ago 2026 y **se conserva como historia** (RFC-46). No describe el trabajo
> pendiente de hoy: la resolución corriente de cada ítem está en la columna `Destino`
> de la tabla, en el párrafo «Resolución» y, sobre todo, en los planes que lo
> materializaron. Leer las filas de abajo como trabajo abierto es leer un registro
> de agosto contra el estado de septiembre.

Ítems derivados del dogfooding end-to-end (sesión `.project/d4ab6a93-8e75-4880-baf3-676fce992936/`). Priorización por frecuencia × costo observado, no por intuición; evidencia por ítem en `19-anexo-a-bitacora-fricciones.md` (IDs F-xx). No son planes redactados: son entradas priorizadas de las cuales se redactan planes al tomarlas.

| # | Ítem | Destino | Prioridad | Evidencia | Vigencia |
|---|---|---|---|---|---|
| B-1 | Gate D01 superable: especial-casing del runner para `KB_DISCOVERY_ENTRY.md` fuera de la iteración, o artefacto de sesión definido por el workflow de discovery | policy | Alta — se repite en cada discovery; hoy exige artefacto-puente | F-11 | active |
| B-2 | Recovery económico para fallos de formato: rama `RETRY_WORKER` en tablas de recovery (H01 primero) — implementada por el plan 29 (2026-08-11); alineación contrato↔validador EARS (bullets canónicos) cubierta por el plan 33 (2026-08-11) | policy | Alta — un fallo de formato cuesta una fase RECOVERY completa | F-01, F-02 | active |
| B-3 | Marcador `.last_discovery` único y canónico (ruta `.project/.last_discovery`, JSON de spec) + validación en health-check | policy | Media — dispara full discoveries evitables | F-12 | active |
| B-4 | Tanda de inconsistencias de contratos/policies: `discovery_context_budget` en features.toml, campos legacy en DISCOVERY_MANIFEST, "primera línea" de EXECUTIVE_SUMMARY, procedencia "observado por scan" en KB_DISCOVERY_ENTRY, delimitador de front matter, actor único de hash calculation, INTENT_REFLECTION auto-confirmada en la máquina de estados, mandato de KB en delegaciones condicionado a disponibilidad, namespacing de `<order>` por dominio — **resuelto**: los residuos `F-14` (marcado legacy), `F-17` (procedencia `source_files`) y `F-18` (delimitador del front matter) quedaron decididos por la RFC-79 `Accepted` y materializados por el plan 142 en la versión 11.6.0 | policy | Media (histórica) | F-04, F-07, F-13, F-14, F-15, F-17, F-18, F-19, F-20 | active |
| B-5 | Política de clarificación desatendida/asíncrona (defaults declarados + confirmación diferida) para sesiones sin usuario en línea | gap → plan nuevo | Media — toda ejecución automatizada choca con esto | F-05 | active |
| B-6 | Subcomandos del runner para H15 (`validate-delegation`, `validate-return`) | gap → plan nuevo (acotado) | Media — hoy requiere importar el módulo a mano | F-08 | active |
| B-7 | Enmiendas conceptuales: RFC-18 (recovery→fases tempranas en la máquina de estados), RFC-20 (candidatura de tareas de tooling/CLI), clasificación `project_shape` para repos documentales/de protocolo — **resuelto**: el shape `documentation` de `project_shape` fue decidido por la RFC-79 `Accepted` y materializado por el plan 142 en la versión 11.6.0 | modelo → enmienda RFC | Baja (histórica) | F-03, F-06, F-16 | active |
| B-8 | Modelo de ejecución de delegaciones en runtimes de contexto único + distinción "flag no aplica" vs "obligación ignorada" en métricas — **resuelto**: el evento de sesión `session_risk` fue decidido por la RFC-79 `Accepted` y materializado por el plan 142 en la versión 11.6.0 | gap → estudio/plan | Baja (histórica) | F-09, Anexo B §Métricas | active |

Descartados como ruido (con justificación en el anexo A): F-10 (deriva de reloj autor-reportado), F-21 (merge de KB legada funcionó según diseño).

Resolución: los ítems B-1…B-8 se redactan como pares RFC + plan en la **Sexta
serie** (tabla arriba); cada plan referencia su fricción F-xx. B-1 → plan 40
(y 47), B-2 → planes 29 y 33, B-3 → plan 50, B-4 → planes 37-43 y 53, B-5 →
plan 44, B-6 → planes 46 y 67 (tests del flujo enforced + subcomandos
validate-delegation/validate-return), B-7 → planes 29 y 52, B-8 → plan 49.
El actor único de hashes de B-4 (F-17) se completa con el plan 58.
El Plan 43 (`43-intent-reflection-auto-confirm.md`) corresponde a `B-4`
(`INTENT_REFLECTION` auto-confirmada sin estado productor, F-04), no a `B-7`;
la atribución anterior de `B-7` al Plan 43 era un error de trazabilidad,
corregido en el Plan 133 (`<PLAN-132>:F-2` / `<PLAN-132>:PC-1`, resueltos).

**Resolución corriente de los residuos de payload de B-4/B-7/B-8 (Plan 145,
2026-09-21).** La primera resolución describe la **Sexta serie** (los planes 37-58)
y es correcta como historia, pero quedó incompleta: los residuos de payload de
`B-4`, `B-7` y `B-8` **no** los cerró esa serie. Los cerró la **RFC-79**
(`Accepted`, `docs/rfc/79-payload-normative-residuals.md`) con su materialización
por el **plan 142** en la versión **11.6.0** (`protocol/.agents/VERSION`), y el
`ROADMAP.md:## Pendientes que requieren autorización` lo registra explícitamente:
`F-14` (el manifest no podía expresar marcado legacy), `F-17` (procedencia de
`source_files` para ausencias y hechos de árbol) y `F-18` (delimitador del front
matter de KB entry) quedaron **implementados** dentro de `B-4`; el shape
`documentation` de `project_shape` (**`B-7`**) y el evento de sesión
`session_risk` (**`B-8`** residual) también. Ninguno de ellos es trabajo abierto
hoy.

## Documentos de soporte

| Archivo | Estado | Rol | Vigencia |
|---|---|---|---|
| `skills-mechanism.md` | implementada | Diseño del mecanismo de skills (SKILL.md + references/); base de RFC-00XX e input de RFC-00YM. | active |
| `analisis-explicitud.md` | vigente | Catálogo de gaps de explicitud (1–9) con evidencia; referencia canónica de los planes 08–14. | active |
| `01-execution-context-model.md` | Executed | Cambios documentales de RFC-00XY en `.agents/` (trazabilidad). | active |
| `02-execution-context-assembly-process.md` | Executed | Cambios documentales de RFC-00XZ (trazabilidad). | active |
| `03-context-budget-model.md` | Executed | Cambios documentales de RFC-00YA (trazabilidad). | active |
| `docs/VERSIONING.md` | vigente | Política de versionado, changelog, tags y estados de planes. | active |

## Future Extensions sin nivel asignado

Anunciadas en RFCs aprobadas pero fuera del roadmap actual (decidir destino):

- Budget Estimation Model y Adaptive Prioritization Model (RFC-00YB).
- Budget Resource Model y Adaptive Budget Model (RFC-00YA).

## Convenciones

> Normativa migrada a `docs/CONVENTIONS.md` (RFC-69). Esta sección se
> conserva como ancla de navegación para referencias históricas; no contiene
> contenido normativo duplicado.

## Archivo

Nota (2 ago 2026): `plans/archive/` fue eliminado del working tree; estos archivos viven en la historia de git (`git show HEAD:plans/archive/<archivo>`).

| Archivo | Contenido | Vigencia |
|---|---|---|
| `archive/PLAN_*_v1.md` | Planes de construcción del protocolo (dominios, taxonomía, discovery) sobre estructura plana; reemplazados e implementados. | active |
| `archive/PLAN_05_CONTEXT_ENGINEERING.md` | Refactor de `.agents/standards/context/CONTEXT.md` (tags, presupuestos). Ejecutado (18 jul). | active |
| `archive/PLAN_06_PERFILES_WORKER.md` | Perfiles en `.agents/roles/profiles/` + campo `profile` del contrato de delegación. Ejecutado (18 jul). | active |
| `archive/PLAN_07_ARTEFACTOS_CONTEXTO.md` | Estándar `.agents/standards/context/PROJECT_ARTIFACTS.md`. Ejecutado (18 jul). | active |
| `archive/PLAN_08_PLANTILLAS_PROYECTO.md` | Plantillas de adopción en `templates/`. Descartado (28 jul): fuentes de `example/` ya no existen, solapa con las plantillas de `.agents/standards/context/PROJECT_ARTIFACTS.md` §9 y su plantilla de IDE era específica de Claude. Idea rescatable: plantillas de dominio como anexo de `.agents/standards/context/PROJECT_ARTIFACTS.md`. | active |

## Documento de visión

`docs/plans/ec-pipeline-vision.md` es el documento de visión del Execution Context Pipeline — ni un plan de ejecución ni un RFC. Vivió en la raíz como `feature.md` hasta el 12 ago 2026, cuando se movió a `plans/` con banner de cierre (visión completada: los 4 niveles ejecutados; el modelo vigente vive en las RFCs 00XX–00YM). Los planes `04`–`07` y las RFCs lo citan como `feature.md`; `check_plan_citations.py` resuelve ese path histórico con un mapeo legacy (`feature.md` → `docs/plans/ec-pipeline-vision.md`). **No reescribir las citas históricas**: son traza.