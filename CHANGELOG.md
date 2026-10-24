# Changelog — Protocolo ARgentOS

Todos los cambios notables del protocolo `.agents/` se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el protocolo sigue [Semantic Versioning](https://semver.org/lang/es/) de forma
conceptual, según lo definido en `docs/plans/20-release-adoption.md` §A:

- **MAJOR**: cambios del modelo conceptual o contratos incompatibles con versiones anteriores.
- **MINOR**: adiciones compatibles (nuevas policies, contratos nuevos que no rompen los existentes, skills nuevas).
- **PATCH**: fixes documentales (correcciones de redacción, enlaces, ejemplos).

## Estructura de cada entrada

Cada versión se agrupa en secciones según el tipo de cambio:

- **Added** — capacidades, contratos, policies o documentos nuevos.
- **Changed** — modificaciones compatibles a comportamiento o documentos existentes.
- **Deprecated** — capacidades que se mantienen pero serán eliminadas.
- **Removed** — capacidades o contratos eliminados (siempre MAJOR).
- **Fixed** — correcciones de errores documentales o de contratos.
- **Modelo conceptual** — RFCs aceptadas o enmendadas (viven en `docs/rfc/`; se listan aquí porque gobiernan el significado de `.agents/`).

Regla de trazabilidad: cada ítem del changelog referencia la policy, el plan o la
RFC que originó el cambio. Los planes viven en `docs/plans/`, las RFCs en
`docs/rfc/` y las policies del harness en
`protocol/.agents/harness/policies/` y
`protocol/.agents/orchestrators/*/harness/policies/`.

La política de migración entre versiones vive en [`docs/MIGRATION.md`](docs/MIGRATION.md).
La política de versionado, changelog, tags y estados de planes vive en
[`docs/VERSIONING.md`](docs/VERSIONING.md).

---

## [Unreleased]

### Added

- **Theoretical Execution (TE) DEV v1** (Plan 175, DEV-only; **RFC-56 Class: N/A**, sin payload delta, sin release por RFC-69): `runtime/theoretical/` implementa la evaluación no mutativa de un Implementation Plan commiteado —`DeclaredOverlay` trivaluado (path declarado → desconocido; no declarado → commit base; nunca working tree), `InputIdentity`/`RunIdentity`, enumeración de entregables/pasos/criterios/efectos/premisas, CH-1…CH-8, contrato `TE_RESULT` con `status` derivado, staleness por `InputIdentity`, comparación estructural sin `resolved`/`reopened`, y CLI `--emit/--validate/--stale/--compare` sin escritura, shell, red ni modelo—; `.agents/policies/theoretical-execution.md` define el reparto productor/engine (completeness/consistency/adversarial atestiguadas por el productor; authority/verification mecánicas) y la frontera teórico/factual; `runtime/README.md`, `.agents/AGENTS.md`, `tests/AGENTS.md` y la suite `tests/test_theoretical_*.py` quedan alineados. El primer dogfood es un run del productor sobre el Plan 175 registrado en `docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md`; una fixture etiquetada no es evidencia de un TE real. Sin cambios en `protocol/`, `dist/`, `VERSION`, `ExecutionHost` ni la batería.

- **Phase 0.4 — cierre de la deuda heredada de Phase 0** (Plan 172, DEV-only, sin efecto payload, sin release por RFC-69): inventario completo de los residuos materiales de Phase 0.1, 0.2 y 0.3 (**65 ítems**, cada uno con estado terminal —15 `RESOLVED`, 7 `IMPLEMENTED`, 4 `REJECTED_BY_DESIGN`, 31 `ACCEPTED_RESIDUAL_RISK`, 8 `NON_ACTIONABLE_HISTORICAL`—, evidencia y rationale; `UNCLASSIFIED = 0`) en `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md`; materialización de `E1-G2`…`E1-G5` de ADR-20 (autoridad de escritura derivada del artefacto y verificada en el escritor, `Executed` ≠ `Closed`, rechazo de escritura sobre contenido gobernante cerrado y registro externo de ejecución separado del plan, con `## Amendment Log` en ADR-20); corrección de un falso positivo de path legacy y de la resolución de headings numerados en `tools/check_plan_citations.py`; reconciliación de `docs/VERSIONING.md` §9 (estado actual a `12.3.0`), `docs/plans/INDEX.md` (estado del Plan 171), `docs/working/proposals/INDEX.md` (filas 0.2/0.3) y de la interpretación local de `INV-08` en `docs/INVARIANTS.md`. `protocol/`, `dist/` y el contenido gobernante de planes/RFC/ADRs cerrados no se modifican.

### Changed

- **Modelo RFC-56 / A-B-C materializado y cerrado** (Plan 174, DEV-only; **RFC-56 Class: N/A**, sin payload delta, sin release por RFC-69): `docs/rfc/56-governance-fast-track.md` queda **enmendada** —la clasificación A/B/C pertenece al **payload delta** y no al Change, al Plan ni al documento que lo describe; un Change puede contener varios deltas con clases distintas y su ruta efectiva la fija la **clase más estricta** presente (`A > B > C > N/A`, sin clase `AB`); un Change sin efecto payload es **RFC-56 N/A**; **Class C** es la transformación mecánica que **preserva la semántica normativa y los contratos** del payload; el **checker es evidencia factual, no autoridad**— con el texto original conservado como registro histórico. Se alinean `docs/CONVENTIONS.md`, `docs/plans/_TEMPLATE.md` (campo `**RFC-56 Class:**` separado de `**Change Level:**`), `docs/VERSIONING.md`, `AGENTS.md`, `.agents/AGENTS.md`, `.agents/workflows/change-lifecycle.md` y `.agents/policies/validation-closure.md`, y se elimina la formulación «todo payload touch → Plan + RFC-56», que contradecía Class C. TE pre y post materialización (T1–T15) y auditoría global con artefactos históricos preservados (RFC-46). Sin cambios en `protocol/`, `runtime/`, `tools/`, `tests/`, `VERSION` ni `dist`.

## [12.3.3] — 2026-10-23

### Fixed

- **Root binding del lifecycle (GATE 3 #32, RFC-81/Plan 154; implementación `8566edd`)** — `protocol/.agents/harness/lifecycle.py` deja de basar la garantía en una identidad revalidada y pasa a ligar cada mutación al objeto validado mediante el nuevo `protocol/.agents/harness/lifecycle_root.py`: descriptor relativo (`openat`/`dir_fd`) en POSIX y handle de directorio sin `FILE_SHARE_DELETE` en Windows. Un root reemplazado en la ventana check→write ya no recibe payload, journal, manifest ni rollback; si no puede establecerse el binding fuerte, las operaciones mutantes fallan cerrado en lugar de usar el fallback `realpath + st_dev + st_ino`. Los tests de transacción cubren C-1/C-2/C-3, el fallback, la ventana pre-lock y update/uninstall/recovery. Sin cambio del contrato #32; el binding POSIX rechaza symlinks en paths gestionados (más estricto que el rechazo de escape) y el binding Windows sólo reclama volúmenes locales (los remotos/UNC fallan cerrado). PATCH: corrección de seguridad/corrección compatible, sin nueva capacidad ni cambio de contrato.

> El tag git `12.3.3` se crea como entregable del release al promover `dev` → `master`.

## [12.3.2] — 2026-10-23

### Fixed

- **Referencias al `AGENTS.md` raíz bajo el layout adoptado** (commit `3ba3533`; Clase C de RFC-56 bajo instrucción directa del mantenedor, sin cambio de contrato): `protocol/.agents/standards/conduct/OPERATIONAL_RULES.md` y `protocol/.agents/standards/quality/PREFLIGHT_CHECKLIST.md` corrigen sus links de `../../../AGENTS.md` a `../../../../AGENTS.md`. Con el payload materializado en `.argentos/.agents/`, la ruta anterior resolvía a `.argentos/AGENTS.md` (que no existe ni debe crearse) y la nueva resuelve al `AGENTS.md` de la raíz del proyecto adoptante. El checker de invariantes valida ahora esa resolución adoptada y la suite de adopción simula `dist/.agents/` → `project/.argentos/.agents/` para impedir la regresión; `docs/source-layout.md` documenta la profundidad y la guarda. Sin cambios de comportamiento del protocolo ni del contrato de adopción.

> El tag git `12.3.2` se crea como entregable del release al promover `dev` → `master`.

## [12.3.1] — 2026-10-21

### Fixed

- **Corrección del cierre de Phase 0.4** (plan 173; Clase B DEV + Clase C tests-only): los **9 ítems `MISCLASSIFIED`** y los **2 `INSUFFICIENT_EVIDENCE`** de la auditoría adversarial pasan a estado terminal genuino —R5 de C-2 detecta la modificación no commiteada del contenido gobernante de un plan cerrado (`P03-D-0.3-12`/`FM-05`/`R-03`); `check_plan_structure` verifica INDEX→archivo en planes/RFC/ADR (`G-07`/`FM-07`/`D-0.3-13`/`R-04`); `tools/check_enforcement_declarations.py` verifica `ENF-001`…`ENF-003` y entra en la batería y CI (`G-04`); tres tests de idempotencia del lifecycle en la suite del payload (`G-08`, Clase C); `docs/VERSIONING.md` §9 reconciliado completo (`FM-10`/`DOC-04`)—, se preservan los **22 residual risks genuinos** y se corrige la identidad de cierre del Plan 172 **por referencia** (tree `58cee8…` y delta `c2492e83…` de `f77cd3f`), sin editar el Plan 172. El bump de `VERSION`, la regeneración de `dist` y el tag `12.3.1` corresponden a esta publicación; los límites de R5 (modificación no commiteada) y del checker ENF (verifica la declaración, no la verdad de la clase) quedan declarados.

### Added

- **Cobertura de idempotencia del lifecycle** (plan 173; Clase C de RFC-56, tests-only): la suite del payload incorpora tres pruebas —segundo `uninstall` como `NOOP` sin reescritura, `doctor` determinista y sin efectos sobre el árbol, y segundo/tercer `recover` como `NOOP` tras una recuperación exitosa—. Sin cambio de comportamiento, de contrato ni del resultado de ningún checker; se publica en `12.3.1` porque es contenido del payload distribuido.

> El tag git `12.3.1` se crea como entregable del release.
- **Priority 0.3 — correcciones de cierre implementadas** (Plan 171, DEV-only, sin efecto payload): se corrigió la interpretación local de `INV-07` y el vocabulario `ENFORCED:session-hook` en `docs/INVARIANTS.md`; se reconcilió la fila del Plan 169 en `docs/plans/INDEX.md` y se registró por referencia el estado de 157/158 y de los findings `open` de 155/158/168/169; `check_plan_structure`, `check_lifecycle_lineage` y `check_invariants_equivalence` incorporan las reglas deterministas y sus tests; la equivalencia canónica corre en CI; y `CHANGELOG.md` sólo cambió en esta entrada `[Unreleased]` (N-9). Sin cambios en `protocol/`, `runtime/` ni `dist/`.
- **F-C (Autonomy Frontier) cerrado** (Plan 165 `Executed`/`Closed`; decisión del mantenedor del 2026-10-13): `FC-1`…`FC-10` quedan **implementados y verificados internamente** (`FC-4` = `IMPLEMENTED + INTERNALLY VERIFIED`; `FC-6`/`FC-7` con su recuperación y sus counterproofs internos; `FC-8`/`FC-10` verificados por diff y checkers). **La demostración con un harness externo autenticado no es requisito de cierre:** ARgentOS es un protocolo documental, agnóstico respecto de harness/provider/modelo/SDK/CLI (ID-1), no invoca ni autentica harnesses, y su superficie de adopción es `AGENTS.md` + `.agents/`; `AgentInvoker` permanece como infraestructura DEV interna. Verificación: `pytest tests/` **1358 passed** · `check_protocol_invariants` PASS (216/10476) · `check_plan_structure` PASS · `check_plan_citations` 26 (baseline) · `check_taxonomy_coherence` OK · C-1 `GAP=0/ANOMALY=0` · C-3 `GAP=0`. Plan 166 cerrado con su Validation Anchor y Checkpoint. Sin `VERSION` bump ni tag en esta etapa.
- **Acto de autorización de ejecución de `F-C` y formalización de su Plan** (plan 164, vía plan; DEV-only,
  docs-only sobre `docs/plans/`, `ROADMAP.md` y este changelog, sin efecto en `protocol/`, `runtime/`,
  `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no aplica): el mantenedor autorizó el **2026-10-13**
  la ejecución de `F-C` bajo el alcance canónico **1B** establecido por `OD-1` y la creación/formalización
  de su Plan con `Status: Aprobado para ejecución`, `Change Level ≥ L3` y criterios `FC-1`…`FC-10`, **sin
  extender el scope** más allá del `IN SCOPE` de `OD-1` y **sin incorporar** `C-16`/`C-17`/`C-21`. El Plan
  164 registra el acto con su transcripción literal, autoridad, fecha efectiva, alcance heredado, artefacto
  designado, efecto sobre el estado y límite explícito —la autorización **no** habilita al agente a
  implementar `F-C` en ese Change—, resuelve la pending decision de `<PLAN-163>` y la anota de forma
  **aditiva** en el artefacto que la posee (regla `PC-1`), y reconcilia `ROADMAP.md` retirando el blocker
  de autorización ya otorgada. **Plan 165 creado (`Status: Aprobado para ejecución`, `Change Level` L3):**
  contrato operativo del Change de implementación, con `IN SCOPE`/`OUT OF SCOPE` heredados **literalmente**
  de `OD-1` —dentro: actor real con provider/modelo, aislamiento/sandbox (incluida la posibilidad prevista
  de declarar la garantía que no se ofrece), Memory como contexto, objetivo multi-Change, `C-02` y `C-26`;
  fuera: `C-16`/`C-17`/`C-21`, derivación parcial, recurso como eje de autorización, default de `--sae`,
  concurrencia, telemetría con backend y evaluación comparativa—, `FC-1`…`FC-10` sin reducción de
  garantías, efectos declarados (`network` autorizado; `install`, `remote_git`, `destructive` y
  `write_outside_project` **no** declarados ni autorizados) y las **ocho decisiones de implementación**
  (`ID-1`…`ID-8`) identificadas y clasificadas sin resolverlas por inferencia: `ID-1` provider/modelo
  concreto, `ID-3` implementar aislamiento o declarar la garantía que no se ofrece e `ID-5` mecanismo del
  objetivo multi-Change **requieren acto explícito del mantenedor**; `ID-6` lo requiere si la solución
  escala a `protocol/.agents/` (RFC-56 Clase A); `ID-2`, `ID-4`, `ID-7` e `ID-8` se resuelven por diseño
  durante la ejecución con registro obligatorio, incluida la resolución de la discrepancia declarada entre
  la política de retry y su implementación. **No implementado:** `F-C` **no** se ejecuta; el Plan 165 se
  crea sin ejecutar (anchor y checkpoint vacíos, sin condición derivada), y 0 diff en `runtime/`, `tests/`,
  `tools/`, `.agents/`, `protocol/` y `dist/`; el default de `--sae`, los techos de recurso, el vocabulario
  de efectos y el envelope de `F-B` quedan sin cambio. `OD1 = CLOSED` · `F-C_SCOPE = 1B / CLOSED` ·
  `F-C_PLAN = CREATED` · `F-C_PLAN_STATUS = Aprobado para ejecución` · `F-C_CHANGE_LEVEL = L3` ·
  `F-C_IMPLEMENTATION = NOT_STARTED` · `ETAPA_B = NOT_STARTED`. Sin `VERSION` bump ni tag; sin citas rotas
  nuevas (el conteo de `check_plan_citations` se mantiene en **26**, el baseline).

- **Acto de autoridad de `OD-1` — alcance canónico de `F-C`** (plan 163, vía plan; DEV-only, docs-only
  sobre `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/` y este changelog, sin efecto en `protocol/`,
  `runtime/`, `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no aplica): **resuelve `OD-1`**. El
  mantenedor ejerció el acto sobre el instrumento decision-ready del Plan 162 y adoptó la interpretación
  **`B`** —**`F-C` es la iniciativa «Complete ARgentOS Autonomy» (Etapa B) delimitada por el resultado de
  la Etapa A a la frontera de autonomía**; `F-C` y Etapa B no son dos iniciativas paralelas— con registro
  normativo **sin ADR** (`Q-d = No`). **`Q-b`:** el resto de Etapa B —las brechas de capacidad del payload
  del Protocol— **no** se conserva como iniciativa paralela y queda **fuera** de `F-C`. **`Q-c` — dentro
  de `F-C`:** actor con provider/modelo; aislamiento/sandbox (o declaración explícita, verificable y
  publicada de la garantía que **no** se ofrece); Memory como contexto (`AE-8`); objetivo multi-Change con
  mecanismo/trigger explícito (`D-1`); y las condiciones relevadas por la Etapa A: contención de autoridad
  fuera del host (`C-02`) y recuperación ante fallos reales, incluida la discrepancia declarada sobre el
  retry (`C-26`). **Fuera de `F-C`, explícito:** `C-16` Discovery, `C-17` Discovery KB y `C-21` Skills
  (payload, con su propia vía); la superficie de derivación parcial (`D-6b = NO`); un eje de recurso como
  autorización (`AE-6`/`D-3`); el default de `--sae` (decidido); y concurrencia, telemetría con backend y
  evaluación comparativa (posteriores). **Boundaries:** `F-A` y `F-B` —incluido el envelope `AE-1`…`AE-10`—
  son **precondiciones cerradas** que `F-C` no reimplementa ni modifica. **Registro normativo:** subsección
  **aditiva** «Modelo de autonomía — alcance canónico de `F-C` (acto del 2026-10-12)» en
  `docs/CONVENTIONS.md`, preservando íntegras las subsecciones del 2026-10-07 y del 2026-10-11.
  **Preparación sin ejecución:** `FC-1`…`FC-10` como criterios de cierre requeridos del futuro Change de
  `F-C`, `Change Level` mínimo esperado **L3** y estado **`SCOPED`** con pending decision **bloqueante**
  (owner mantenedor) para autorizar su ejecución. **No realizado:** implementar cualquier capacidad de
  `F-C` (provider/modelo, aislamiento/sandbox, Memory, multi-Change, contención de autoridad,
  recuperación/retry), autorizar su ejecución, crear un Plan de `F-C` con estado `Aprobado para ejecución`,
  iniciar Etapa B, o cambiar defaults de autonomía, el envelope de `F-B`, los techos de recurso o el
  vocabulario de efectos. Reconciliación derivada: `ROADMAP.md` (`F-C` en `NEXT` con alcance resuelto y sin
  autorización; brechas del payload en `LATER`, explícitamente fuera; grafo de dependencias alineado;
  blocker de ejecución no autorizada), anotación **aditiva** de la resolución de la pending `OD-1` en
  `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` (regla `PC-1`) y registro en
  `docs/plans/INDEX.md`. **`OD-1` = `RESOLVED`**; **`F-C` = `NOT_IMPLEMENTED`**; 0 diff en `runtime/`,
  `tests/`, `tools/`, `.agents/`, `protocol/` y `dist/`. Sin `VERSION` bump ni tag; sin citas rotas nuevas
  (el conteo de `check_plan_citations` se mantiene en **26**, el baseline).

- **`OD-1` — instrumento de decisión del alcance canónico de `F-C`** (plan 162, vía plan; DEV-only,
  docs-only sobre `docs/plans/`, `ROADMAP.md` y este changelog, sin efecto en `protocol/`, `runtime/`,
  `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no aplica): aborda `OD-1` y **no lo resuelve**.
  **Verificación de autoridad → `OD1_BLOCKED`.** La resolución de `OD-1` es una decisión de **alcance**
  reservada al mantenedor (`.agents/policies/authority.md`: `DECISION` = «the human maintainer» y «a human
  decision is required → STOP at the gate, ask»; `.agents/AGENTS.md` regla 3; frontera humana de SAE §8;
  ADR-16 `AU-3`/`AU-5`/`AU-6`) y **no está presente en el repositorio**: todas las menciones vivas a `F-C`
  son exclusiones de alcance o remisiones a una decisión futura, y `OD-1` persiste como pending decision
  **bloqueante** con owner mantenedor en el Plan 161. El agente **no elige** entre `R1` (`F-C` = Etapa B
  completa), `R2` (`F-C` = residuo del envelope) y `R3` (subconjunto de frontera de autonomía). **Material
  decision-ready preparado:** lo que la evidencia de Etapa A **sí** determina (D-1…D-7), las tres
  interpretaciones con su soporte documental y su tensión, lo que **no** determina, la pregunta desagregada
  en `Q-a`…`Q-d` con sus consecuencias, las siete inferencias prohibidas (la madurez baja de una capacidad
  **no** la vuelve parte de `F-C`), el registro exigido del acto (Plan vehículo con `## Acto de autoridad
  registrado`, subsección **aditiva** en `docs/CONVENTIONS.md`, con ADR-worthiness resuelta) y los
  criterios de cierre `AC-1`…`AC-12`. **No realizado:** definir `F-C`, crear un Plan de `F-C`/Etapa B,
  modificar `docs/CONVENTIONS.md` o ADRs, o implementar cualquier capacidad. `F-C` = `NOT_IMPLEMENTED`,
  Etapa B = `NOT_STARTED`, `OD-1` = `PENDING_AUTHORITY`. Sin `VERSION` bump ni tag; sin citas rotas nuevas
  (el conteo de `check_plan_citations` se mantiene en **26**, el baseline).

- **Autorización de Etapa A y creación del Plan 161** (plan 161, vía plan; DEV-only, docs-only sobre
  `docs/plans/`, `docs/working/audits/INDEX.md` (registro) y este changelog, sin efecto en `protocol/`,
  `runtime/`, `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no aplica): formaliza el acto de
  gobierno que bloqueaba la Etapa A —la pending decision bloqueante `PC-1` del Plan 160— y crea su
  artefacto de ejecución. **Acto de autorización:** el mantenedor (2026-10-12) autoriza el alcance de
  la retrospectiva de capacidades y garantías y designa el **Plan 161**, con trazabilidad completa
  `decisión → autoridad → alcance autorizado → Plan 161` y estado canónico **`Aprobado para ejecución`**
  (`docs/VERSIONING.md` §7); no se introduce ningún estado nuevo y la resolución de `PC-1` se anota de
  forma **aditiva** en el artefacto que la posee (Plan 160). **Plan 161:** materializa el contrato de
  Etapa A declarado por el Plan 149 —unidad *capacidad + garantía + evidencia*, alcance conceptual
  mínimo de veintiocho capacidades, ocho niveles de madurez, **Capability & Guarantee Matrix** con
  nueve dimensiones por capacidad— en criterios de cierre verificables `DC-1`…`DC-10`, sin ampliar el
  alcance; su producto se ubica en `docs/working/audits/` por el contrato de placement (familia
  *Working analysis*), sin clase ni namespace nuevos. **Etapa A no se ejecuta en este Change**: queda
  autorizada y lista para el Change siguiente. `F-C`/Etapa B permanecen no iniciadas y `OD-1` sin
  resolver; sólo se registra la dependencia `Etapa A → resultado → revisión del alcance de F-C/Etapa B`.
  Sin `VERSION` bump ni tag; sin citas rotas nuevas (el conteo de `check_plan_citations` se mantiene en
  **26**, el baseline). **Ejecución (2026-10-12):** la retrospectiva se ejecutó y produjo el
  **Capability & Guarantee Matrix** —`docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`,
  registrado en `docs/working/audits/INDEX.md`— con **28** capacidades × **9** dimensiones = **252** celdas
  sin vacíos y **28** niveles de madurez del vocabulario cerrado (`dogfoodeado` 11 · `testeado` 6 ·
  `parcialmente demostrado` 4 · `dependiente de una condición externa` 3 · `no demostrado` 2 ·
  `limitado por un boundary conocido` 1 · `implementado` 1 · `demostrado bajo condiciones reales` **0**),
  `DC-1`…`DC-10` **PASS** y Validation Anchor **A1** con condición derivada **`Closed`**. Las únicas
  escrituras fueron el producto, su registro y los artefactos de gobernanza del cierre: `runtime/`,
  `tools/`, `tests/`, `.agents/` y `protocol/` fueron inspeccionados como evidencia con **0 diff**. Las
  citas rotas se mantienen en el baseline (**26**) y los findings `<PLAN-161>:F-1` (forma de cuatro citas
  `ruta:sección`) y `<PLAN-161>:F-2` (conteo de pruebas del harness: 185, no 179) quedaron resueltos por
  `<PLAN-161>:C-1`/`C-2`. **Hallazgo central:** ninguna capacidad alcanza `demostrado bajo condiciones
  reales` para la totalidad de su afirmación, porque las condiciones de uso pretendidas de buena parte del
  sistema —un proyecto adoptante, un proveedor real, la infraestructura de CI— no son observables desde el
  repositorio; `C-16` Discovery, `C-17` Discovery KB y `C-21` Skills quedan `no demostrado`. **No resuelto
  por diseño:** `OD-1` permanece abierto, `F-C`/Etapa B no se definen ni se inician y `F-C scope =
  TO BE REVIEWED`; el resultado de Etapa A es insumo de la revisión posterior, no una decisión.

- **Cierre de las decisiones inmediatas (`OD-2`, `OD-6`) y preparación de la autorización de Etapa A**
  (plan 160, vía plan; DEV-only, docs-only sobre `docs/CONVENTIONS.md`,
  `docs/adr/19-autonomy-envelope-authority.md`, `ROADMAP.md`, `docs/plans/INDEX.md` y este changelog,
  sin efecto en `protocol/`, `runtime/`, `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no aplica):
  cierra las dos decisiones que el relevamiento de cierre de `F-C` identificó como cerrables ahora.
  **`OD-2` — derivación parcial: `D-6b = NO` es la decisión efectiva.** Se corrige la viñeta «Fuera de
  este acto» de `docs/CONVENTIONS.md` —que enumeraba la «superficie de derivación parcial» entre los
  elementos diferidos del acto del 2026-10-11— y se agrega una entrada de Amendment Log en ADR-19
  (2026-10-12) que registra la reconciliación **hacia adelante**, preservando íntegro el texto de las
  entradas anteriores (RFC-46): la superficie de derivación parcial está **descartada**, no diferida, y
  no pertenece al alcance de `F-C`. No se crea capacidad, superficie, mecanismo ni autorización.
  **`OD-6` — `work_type`: criterio y política ya canonizados.** El criterio de admisión y la política de
  declaración adoptados por el Plan 152 (`GOV-8`/`GOV-9`, en `docs/CONVENTIONS.md`) seguían vigentes
  mientras `ROADMAP.md` conservaba un blocker **obsoleto** («`work_type` sin criterio de admisión»); la
  fila se retira del mapa operativo porque su contenido tiene artefacto dueño (`docs/CONVENTIONS.md` y el
  Plan 152) y `P-5` permanece `GAP` como estado por caso, no como bloqueo.
  **Etapa A — preparación, no ejecución.** Se determina su contrato vigente (retrospectiva de
  capacidades y garantías; unidad *capacidad + garantía + evidencia*; producto: Capability & Guarantee
  Matrix), su alcance, sus dependencias y el Change aplicable (número libre 161), y se registra el
  **acto de autorización que falta** como pending decision bloqueante con owner (mantenedor),
  precisando la fila correspondiente de `ROADMAP.md`. No se simula autorización, no se crea un
  artefacto con un estado que afirme una aprobación inexistente y no se ejecuta trabajo de Etapa A.
  **No implementado, por directiva:** `F-C`/Etapa B, provider/modelo, aislamiento/sandbox, Memory,
  concurrencia, telemetría y retry. Sin `VERSION` bump ni tag; sin citas rotas nuevas (el conteo de
  `check_plan_citations` se mantiene en **26**, el baseline preexistente).

- **Materialización del envelope de autonomía (`F-B`) — admisión de efectos y techo de recurso** (plan 159, vía plan;
  DEV-only sobre `runtime/orchestrator/`, `tests/`, `.agents/policies/`, `docs/plans/_TEMPLATE.md`, `docs/adr/19`,
  `docs/CONVENTIONS.md`, `docs/plans/INDEX.md` y este changelog, sin `VERSION` bump ni tag, RFC-69): el acto de
  autoridad del 2026-10-11 cierra las dos cuestiones que el acto del Plan 151 (2026-10-07) había dejado expresamente
  fuera y materializa los dos bloqueantes del relevamiento de cierre (`BLK-1` admisión de efectos fuera de frontera;
  `BLK-2` terminación por recurso). **`OPD-1` — vocabulario DEV de clases de efecto: adoptado.** Las clases son
  `network`, `remote_git`, `install`, `destructive`, `write_outside_project`, con `AUTHORIZED_BY` ∈ {`user`,
  `unattended_default`} y `EFFECT_STATUS` ∈ {`authorized`, `not_authorized`, `pending_user_confirmation`}: es
  **un solo vocabulario**, el que el repositorio ya había materializado y verificado para sus artefactos de sesión del
  Protocol (`tools/check_session_artifacts.py`), verificado por dogfood anclado contra el runtime. No se crea taxonomía
  paralela. **`OPD-2` — techo de recurso: guarda operativa de terminación.** El Plan declara `**Resource ceiling:**`
  en `## Delegación agentiva`; el runtime lo lee, acumula el consumo desde las **delegaciones efectivamente
  registradas** en el journal (nunca desde la numeración de iteraciones), sobrevive un reinicio de proceso porque el
  host no tiene estado, y al agotarse detiene la autonomía con `STOP_MAX_ITERATIONS`. **`resource ceiling ≠
  authorization`**: el techo no entra en `AutonomyEnvelope.declared`, no produce veredicto `AUTHORIZED_EXISTING` y no
  amplía autoridad — `AE-6` y `D-3` se preservan sin excepción, y `PR-2` del audit de capacidades queda resuelto como
  frontera de **terminación**, no como eje de **autorización**. **Implementación:** `observation.py` (parser de
  `## Efectos declarados` con `DeclaredEffect`, lectura de `**Resource ceiling:**`, `declared_effects_unresolved` y
  `GAP` declarado para un techo ilegible), `autonomy.py` (`EFFECT_KINDS`/`EFFECT_AUTHORIZED_BY`/`EFFECT_STATUSES`,
  `DeclaredEffectView`, `EffectAdmission`, `admit_declared_effects`, `declared_effects` en el envelope, `effects` y
  `effects_unresolved` en el candidato, ejes de scope y de efecto evaluados y **reportados por separado** —un efecto
  sin `write-target` es admisible, que es la lectura operativa de `AE-3`—, proyección `authorization-effects-v1`
  dentro del checkpoint de autorización, y `resource_stop`/`resource_ceiling`/`resource_consumed` en el resultado sin
  veredicto de autoridad), `host.py` (`_apply_autonomy_gate` extendido a los efectos **antes** de delegar,
  all-or-nothing; `_autonomy_effects`; `_resource_consumed` derivado de las delegaciones del journal;
  `_effects_executed_violations` para el efecto ejecutado que el Plan no declaró, registrado como finding y con
  `STOP_FORBIDDEN_ACTION`; `STOP_MAX_ITERATIONS` mapeado como stop **operativo** y no de autoridad) y
  `worker.py`/`agent_worker.py` (`effect:<clase>` calificado en `effects_executed` y `classify_executed_effects`, de
  modo que una narrativa nunca se lea como una clase de efecto). **Pruebas:** `tests/test_autonomy_effects.py` (36
  falsaciones: casos A–E del gate —declarado+autorizado, no declarado, declarado sin autorización, clase desconocida,
  efecto sin path—, la contra-prueba de que sin el gate el invoker **sí** escribe y con el gate el artefacto queda
  byte-idéntico, el techo de recurso con consumo acumulado y supervivencia a reinicio, la falsación explícita
  `resource exhausted → STOP → NEVER AUTHORIZED`, y la consistencia `declared_effects` ↔ `effects_executed`) y
  `tests/test_autonomy_effects_dogfood.py` (13 pruebas ancladas: policy ↔ enforcement, un solo vocabulario, la frontera
  fuera del envelope de autonomía y el Plan 159 leyéndose con su propio parser). **Reconciliación normativa:**
  `docs/adr/19-autonomy-envelope-authority.md` (Amendment Log 2026-10-11 y estado de implementación por invariante,
  **sin reescribir** el acto del 2026-10-07), `docs/CONVENTIONS.md` (subsección aditiva «vocabulario de efectos y techo
  de recurso»), `docs/plans/_TEMPLATE.md`, `.agents/policies/supervised-autonomous-execution.md` (§1.5 admisión de
  efectos, §3.1 techo de recurso, §2/§5/§10/§12), `tests/AGENTS.md` (registro del módulo anclado) y la
  `Octogésima octava serie` del INDEX. **Fuera de alcance por decisión:** `--sae` sigue `opt-in` (`OPD-3`), y no se
  implementan provider/modelo, aislamiento/sandbox, Memory, concurrencia, telemetría, retry ni `F-C`/Etapa B.

- **Simplificación radical del ROADMAP** (plan 158, vía plan; DEV-only, docs-only sobre `ROADMAP.md` (reducido),
  `docs/plans/158-radical-simplification-roadmap.md`, `docs/plans/INDEX.md` y este changelog, sin efecto en
  `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/` ni `docs/CONVENTIONS.md`, por lo que RFC-56 no aplica):
  corrige la implementación del plan 157 —que resolvió el problema estructural pero dejó el ROADMAP acumulando, bajo
  `NOW / NEXT / LATER`, un capability inventory, un informe de autonomía, un índice documental, un manual de
  gobernanza, un catálogo de dependencias y un registro de blockers— aplicando la estrategia **REDUCE, NOT
  REORGANIZE**. `ROADMAP.md` pasa de **367 a 99 líneas** (presupuesto visual: IDEAL <100, ACCEPTABLE <150, WARNING
  ≥150, FAIL ≥200). Cada bloque se sometió a la regla de admisibilidad —permanece sólo si responde a *cuál es el
  destino / dónde estamos / qué viene ahora / qué viene después / qué puede cambiar ese camino*— y lo que no
  responde se **eliminó del ROADMAP** en lugar de re-tabularse. Estructura resultante: header de dos líneas con
  puntero al contrato; `## 🎯 Destino`; `## 🧭 Posición actual` (baseline publicado `12.0.0` sobre `78ca512`, payload
  publicado en `origin/dist` @ `1181db6`, PATCH `12.0.1` en `dev` sin tag, trabajo activo ninguno, y la constancia
  de que las capacidades existentes no se reabren); `## 🚦 Roadmap` con `NOW` (promover `12.0.1`), `NEXT` (Etapa A,
  retrospectiva de capacidades y garantías) y `LATER` (envelope de autonomía, Complete ARgentOS Autonomy/Etapa B,
  Etapa C), cada iniciativa expresada como `[DOMINIO] PRIORIDAD — qué y por qué`; `## 🔗 Dependencias críticas` en
  **un único** grafo Mermaid; `## 🚧 Bloqueos que pueden cambiar el camino` (6 filas). **Eliminados del ROADMAP:**
  los dos inventarios de capacidades DEV/PROTOCOL, el mapa de autonomía completo (3 tablas, 2 grafos y 2 avisos), la
  tabla `Dónde consultar qué` (11 filas), la sección `Qué es y qué NO es este documento` con sus reglas de admisión
  y frescura, la lista de trece fronteras candidatas, la tabla de baseline y las tres cards ASCII de seis campos.
  **No se creó ningún documento nuevo** (`CAPABILITIES.md`, `AUTONOMY.md`, `DECISIONS.md`, `ROUTING.md`): todo lo
  eliminado ya tiene artefacto dueño en `docs/CONVENTIONS.md`, `docs/plans/INDEX.md`, `runtime/README.md`,
  `docs/adr/19-autonomy-envelope-authority.md`, `CHANGELOG.md` y el artefacto que posee cada decisión. El contrato
  canónico del ROADMAP **no se modifica**: este Change hace que el documento lo cumpla. Sin `VERSION` bump ni tag
  (RFC-69); **cero citas rotas nuevas** —el conteo de `check_plan_citations` se mantiene en 27, el baseline
  preexistente—.

- **Patrones de comportamiento — cómo trabaja ARgentOS** (plan 155, vía plan; DEV-only, docs-only sobre
  `docs/behavior-patterns.md` (nuevo), `README.md`, `ROADMAP.md`, `docs/VERSIONING.md` §9, `docs/AGENTS.md`,
  `docs/plans/INDEX.md` y este changelog, sin efecto en `protocol/`, `runtime/`, `tools/`, `tests/` ni `.agents/`,
  por lo que RFC-56 no aplica): se agrega el documento que explica el **comportamiento observable** del sistema —
  patrón de estado (nada se almacena, todo se deriva; estados afirmados vs condiciones derivadas
  `Verified`/`Executed`/`Committed`/`Closed`/`Released`), *gate pattern* (la autoridad precede al efecto; los cuatro

- **ROADMAP canónico visual y estratégico — contrato documental y reestructuración** (plan 157, vía plan; DEV-only,
  docs-only sobre `ROADMAP.md` (reestructurado), `docs/CONVENTIONS.md`, `docs/glossary/terms.md`,
  `docs/glossary/INDEX.md`, `docs/AGENTS.md`, `README.md`, `AGENTS.md`, `docs/plans/INDEX.md` y este changelog, sin
  efecto en `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, RFCs, ADRs ni `docs/VERSIONING.md`, por lo que
  RFC-56 no aplica): se establece el **contrato canónico del `ROADMAP.md`** y se reemplaza su estructura por una
  representación estratégica, visual y orientada al futuro. El documento pasa a declarar su **responsabilidad
  única** —comunicar visualmente la dirección de evolución de ARgentOS y el camino de alto nivel para alcanzarla—,
  con **Visión / Destino**, **Posición actual** (protocolo publicado `12.0.0` sobre `78ca512`, payload publicado en
  `origin/dist` @ `1181db6`, PATCH `12.0.1` en `dev` sin promocionar y sin tag, trabajo activo: ninguno),
  **Roadmap at a Glance** con lanes `NOW → NEXT → LATER` y una card por iniciativa (`Objective`, `Domain`,
  `Priority`, `Status`, `Depends on`), **dependencias estratégicas** en Mermaid, una **tabla corta de
  blockers/decisiones** con el artefacto dueño de cada una, y el **caso Autonomy** en cuatro planos diferenciados
  —host autonomy, SAE y authority model implementados y testeados; envelope de autonomía decidido (`AE-1`…`AE-10`)
  pero **no implementado**; Etapas A y B futuras— con la precisión explícita de que lo existente es **DEV-only**,
  no viaja en `dist` y **no** es «Complete ARgentOS Autonomy». El contrato normativo vive en
  `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)`: qué es, qué **no** es (backlog, changelog,
  capability registry, decision register, especificación, evidencia), dimensiones obligatorias (`Domain`
  `PROTOCOL`/`DEV`/`BOTH`, horizonte `NOW`/`NEXT`/`LATER`, prioridad, status sin fusionar implementación con
  publicación, dependencias), **regla de admisión**, **regla de frescura** y frontera con la determinación de
  cierre `Roadmap impact`, cuya semántica **no** se modifica. El término se registra en
  `docs/glossary/terms.md:ROADMAP` y `docs/glossary/INDEX.md` **enrutando** a esa fuente sin duplicar la
  definición (single-source del glosario). No se crea ningún capability registry ni decision register: el ROADMAP
  **enruta** a `docs/plans/INDEX.md`, `runtime/README.md`, `docs/adr/INDEX.md` y `.agents/policies/` en lugar de
  absorber su estado. Se reconciliaron las referencias cruzadas que describían el ROADMAP como «project
  priorities» (`AGENTS.md`, `README.md`, `docs/AGENTS.md`). El contenido del ROADMAP anterior se clasificó bloque
  por bloque con destino declarado, sin pérdida de información: el detalle histórico pasó a los artefactos que lo
  poseen y el mapa conserva dirección, posición, iniciativas, orden, dependencias y bloqueos. Docs-only, sin
  `VERSION` bump ni tag (RFC-69).

### Changed
  `docs/behavior-patterns.md` (nuevo), `README.md`, `ROADMAP.md`, `docs/VERSIONING.md` §9, `docs/AGENTS.md`,
  `docs/plans/INDEX.md` y este changelog, sin efecto en `protocol/`, `runtime/`, `tools/`, `tests/` ni `.agents/`,
  por lo que RFC-56 no aplica): se agrega el documento que explica el **comportamiento observable** del sistema —
  patrón de estado (nada se almacena, todo se deriva; estados afirmados vs condiciones derivadas
  `Verified`/`Executed`/`Committed`/`Closed`/`Released`), *gate pattern* (la autoridad precede al efecto; los cuatro
  gates; prevención ≠ detección), orquestación (una responsabilidad por componente; delegación y contrato M4; el
  patrón de escritura de gobernanza con un único escritor), *autonomy loop* (el ciclo real con sus dos versiones —
  frontera SAE `opt-in`—, qué **no** existe, cómo termina y la métrica de autonomía con sus dos conteos humanos no
  fusionables), human-in-the-loop (qué decide el sistema y qué retiene el humano; obligación ≠ permiso; no existe
  expansión autónoma de scope), fallo y recuperación (taxonomía de **señales**, no de estados) y client interaction
  (los dos flujos —adoptante y DEV— y el hallazgo de que **no existe un modelo de clientes**: sólo tres superficies
  de integración). El documento cita sus fuentes de verdad sin duplicarlas y no documenta razonamiento privado. La
  auditoría que lo precede reconcilió además el estado real: versión publicada `12.0.0` (tag sobre `78ca512`,
  `origin/dist` con `VERSION` = `12.0.0`), `docs/VERSIONING.md` §9 y `ROADMAP.md` actualizados, y dos afirmaciones
  inexactas del `README.md` corregidas (la sonda **no** deriva su project root de su propia ubicación — lo recibe por
  `--project-root`/`ARGENTOS_PROJECT_ROOT` — y la superficie del lifecycle incluye `recover` y exit codes
  deterministas 0/10/20/30). **Clasificación:** Clase B, Change Level L2; docs-only, sin `VERSION` bump ni tag
  (RFC-69).

### Changed

- **Reconciliación del snapshot de versión y del roadmap al release real** (plan 155, vía plan; DEV-only, docs-only):
  `docs/VERSIONING.md` §9 pasa de declarar la release de gobernanza `11.6.2` (2026-09-22) a declarar el estado
  verificado (`master` = `12.0.0`, tag sobre `78ca512`, `origin/dist` publicado con `VERSION` = `12.0.0`, `dev` =
  `master` sin divergencia abierta), e incorpora la sucesión de puntos de reconciliación omitida (`11.7.1` y `12.0.0`)
  más la advertencia operativa de que la **ref local** `dist` puede quedar por detrás de `origin/dist` y no debe
  citarse sin resolver el remoto. `ROADMAP.md:### Estado del que parte este roadmap` deja de declarar `11.6.2` como
  versión publicada, registra el trabajo posterior a su tabla que ya está cerrado (lifecycle de adopción, Memory
  System) y actualiza el inventario de estado histórico del que parte (Planes 146–154, ADR-17/18/19).
  **Lectura correcta de la autonomía (desambiguación; la historia se conserva literal).** Los planes 151–153
  cerraron las **decisiones de autoridad del envelope** de autonomía y su remanente registral: **no** la capacidad
  de autonomía del host —implementada antes en `runtime/orchestrator/` y las policies SAE, y presente en el estado
  publicado del repositorio como capacidad **DEV-only**, fuera del payload que distribuye `dist`— y **no** la
  Etapa B (`Complete ARgentOS Autonomy`), que sigue siendo trabajo futuro con su propia autorización. La
  formulación «cierre de la feature de autonomía» del ítem del plan 153 es la transcripción de la instrucción del
  acto de autoridad (`AUTHORITY_EVIDENCE` de `docs/plans/151-autonomy-authority-decision-closure.md`) y **no** se
  reescribe (RFC-46); esta entrada fija su interpretación vigente, y la evidencia de lo que permanece pendiente
  está en `docs/adr/19-autonomy-envelope-authority.md:Estado de implementación`.
- **Cierre residual del Plan 151 — ejecución del Plan 153 (acto de autoridad del 2026-10-08)** (plan 153,
  vía plan; DEV-only, docs-only sobre `docs/plans/151-autonomy-authority-decision-closure.md`, el Plan 153,
  `docs/plans/INDEX.md` y este changelog, sin efecto en `protocol/`, `runtime/`, `tools/`, `tests/` ni
  `.agents/`, por lo que RFC-56 no aplica): el mantenedor ejerció la autoridad residual sobre el remanente
  del Plan 151 y se materializó el cierre de la feature de autonomía — `D-151-1 = B` (las diez filas `HD-*`
  que el acto del 2026-10-07 dejó sin disposición quedan resueltas **por evidencia y decisión posterior**,
  preservando íntegro el acto original), `D-151-2 = Executed` (el Plan 151 pasa de `Executed (parcial: …)` a
  `Executed`, con condición derivada `Closed`) y `D-151-3 = YES`
  (`CL-151-Q1 = RESOLVED_BY_CURRENT_AUTHORITY`: un acto de autoridad posterior puede satisfacer un criterio
  de salida pendiente sin reescribir ni reinterpretar la historia). Revalidación `A2` PASS sobre el estado de
  cierre; el Plan 152 permanece sin cambios y su espejo del INDEX queda alineado; `P-5` permanece `GAP` (sin
  `work_type` inventado); sin ADR nuevo y sin autoridad retroactiva.
- **Instrumento Class B para el cierre residual del Plan 151** (plan 153, vía plan; DEV-only, docs-only
  sobre el Plan 153 y `docs/plans/INDEX.md`, sin efecto en `protocol/`, `runtime/`, `tools/`, `tests/`
  ni `.agents/`, por lo que RFC-56 no aplica): se materializa el vehículo que permite decidir, en un acto
  de autoridad **posterior y explícito**, el tratamiento de los remanentes del Plan 151 —las diez filas
  `HD-*` que su acto del 2026-10-07 dejó `SIN DISPOSICIÓN`—, preservando íntegramente el acto histórico y
  prohibiendo la retroactividad (`RETROACTIVE_HISTORY_MUTATION = BLOCKED`). El Plan queda `Aprobado para
  redacción` y **no decide**: `D-151-1` (tratamiento de las diez filas), `D-151-2` (estado residual) y
  `D-151-3`/`CL-151-Q1` (¿puede un acto posterior satisfacer un criterio de salida anterior sin reescribir
  el acto?) permanecen `PENDING_AUTHORITY`, con la opción retroactiva expresamente prohibida; `CL-151-Q5`
  queda `RESOLVED_CURRENT_RULE` (el paréntesis de `Executed (parcial: <qué falta>)` describe lo que falta
  y la forma legacy del Plan 41 no está disponible). Define las rutas A–F con sus precondiciones de
  autoridad (`AUTHORITY_ACT = RECORDED`, `AUTHORITY_INFERRED = NO`, `HISTORICAL_AUTHORITY_REUSED = NO`),
  la revalidación obligatoria si cambia el contenido en scope y la fórmula vigente de `Closed`. No
  modifica el Plan 151 ni el Plan 152, no crea ADR, no deriva `work_type` (`P-5 = GAP`) y no ejecuta
  ninguna decisión de autoridad.
- **Materialización del acto de autoridad del Plan 152 — `GOV-1`…`GOV-10`** (plan 152, vía plan;
  DEV-only, docs-only sobre `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/plans/_TEMPLATE.md`,
  `docs/rfc/_TEMPLATE.md`, `docs/adr/_TEMPLATE.md`, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`,
  `docs/adr/INDEX.md`, `docs/working/proposals/INDEX.md` y el Plan 152, sin efecto en `protocol/`,
  `runtime/`, `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no aplica): se materializaron las
  consecuencias de las diez decisiones del acto de autoridad del 2026-10-07 —
  `GOV-1` (reconciliación de identidad de los IDs divergentes, con las formulaciones históricas
  conservadas), `GOV-2` (ausencia de evidencia de los actos del 2026-10-02/2026-10-05 y no
  retroactividad), `GOV-3` (`Note` como forma dentro de la familia `Plan`, con `**Tipo:**` y registro
  propio), `GOV-4` (vía normativa de autorización por `Note` con los criterios `C-1`…`C-13` y las
  prohibiciones `N-1`…`N-7`), `GOV-5` (`**Lifecycle:**` por artefacto: valores, default `active` por
  ausencia, no-fusión con `**Status:**`, guarda hacia adelante, alcance Plan/RFC/ADR), `GOV-6`
  (`**Superseded por:**` y `**Motivo de retiro:**`; `Abandoned` como condición derivada, sin estados
  nuevos), `GOV-7` (columna `Vigencia` derivada en los tres INDEX de gobernanza; `HEADER = fuente`,
  `INDEX = vista`), `GOV-8` (criterio de admisión de `work_type`) y `GOV-9` (política de declaración de
  `work_type`)—. `GOV-10` queda **diferida** por la propia decisión
  (`COMMITMENT_NOW` / `MATERIALIZATION_LATER`): `INV-1` e `INV-3` **no** se elevan a norma en este
  cambio. `P-5` permanece `GAP` (no se derivó ningún `work_type`); **no** se creó ADR ni se enmendó el
  ADR-19 (ADR-worthiness `AU-6` no ejercida; queda como finding abierto); el Plan 151 **no** se modifica.
- **Cierre de autoridad del modelo de autonomía — D-1…D-6b, D-ADR, Q9 y Q9bis** (plan 151, vía plan;
  DEV-only, docs-only sobre `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/plans/_TEMPLATE.md`,
  este changelog, el Plan 151, `docs/plans/INDEX.md`, `docs/adr/19-autonomy-envelope-authority.md`,
  `docs/adr/INDEX.md` y los índices de `docs/working/`, sin efecto en `protocol/`, `runtime/`,
  `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no aplica): el mantenedor ejerció **un único
  acto de autoridad** (2026-10-07) que resolvió trece decisiones —`D-1` (unidad de aceptación = el
  Change; objetivo global diferido), `D-2a`/`D-2b`/`D-2c`/`D-2d` (frontera de efectos DEV;
  declaración en el Plan; enforcement antes de delegar; `Effect` ortogonal a `Scope`), `D-3` (sin eje
  de recurso), `D-4` (actor acotado; provider/modelo diferido), `D-5` (`P-6` documental; Memory =
  contexto), `D-6a` (sin autorización parcial), `D-6b` (sin derivación parcial), `D-ADR` (ADR-19),
  `Q9` (ocho disposiciones: `premises(D)`, `HD-K3`, `HD-M5`, `MK-3`, `HD-K1`, `HD-K2`, `HD-K4` y el
  claim `HD-INT-G`) y `Q9bis` (regla de evidence closure; paso 9 de sincronización)—, y que
  **corrigió la provenance** de las dos materializaciones normativas sin autorización trazable
  (`b556741`, `d8bd284`): su autoridad nace en este acto y **no** se afirma ningún acto humano del
  2026-10-05 (`HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`). `DECISION_COUNT = 13`; `P-5`/`work_type`
  permanece `DERIVED_FIELD` (condicionado a los ítems Q9 relevantes; sin valor derivado, porque el
  criterio de admisión no fue adoptado). Plan 151 queda `Executed (parcial: HD-INT-A…HD-INT-J y
  HD-M4 sin disposición autorizada; commit de cierre pendiente del mantenedor)`.
- **Roadmap estratégico de capacidades y autonomía — Etapas A → B → C** (plan 149, vía plan;
  docs-only sobre `ROADMAP.md`, este changelog, el Plan 149 y `docs/plans/INDEX.md`, sin
  efecto en `protocol/`, `runtime/`, `tools/`, `tests/` ni `.agents/`, por lo que RFC-56 no
  aplica): `ROADMAP.md` declara el roadmap estratégico vigente y su dependencia explícita
  **A → B → C**. **Etapa A — Capability & Guarantee Retrospective:** revisión de las
  capacidades y garantías que ARgentOS afirma proporcionar, con unidad de análisis
  *capacidad + garantía + evidencia* y un **Capability & Guarantee Matrix** que separa
  implementado / testeado / dogfoodeado / demostrado bajo condiciones reales / parcialmente
  demostrado / dependiente de una condición externa / no demostrado / limitado por un
  boundary conocido; no es una auditoría documental. **Etapa B — Complete ARgentOS
  Autonomy:** comienza a partir de los resultados de A, sin lista rígida de features, para
  cerrar las fronteras que impiden ejecutar un objetivo amplio de forma autónoma bajo
  supervisión humana dentro de `Autonomy ⊆ Scope ∩ Authority`; las fronteras enumeradas
  —provider/model real, persistencia de Worker Results, derivación de la siguiente acción,
  ejecución multi-step, recuperación y fallos reales, budgets, terminación, multi-worker,
  deliberación, Prompt Cache y persistencia Project/Knowledge— se declaran **candidatas, no
  compromisos de implementación**. **Etapa C — New Features:** subordinada al conocimiento
  obtenido en A y a las necesidades descubiertas en B; ninguna feature entra por
  disponibilidad tecnológica. El Change no implementa ninguna etapa, no ejecuta la
  retrospectiva, no crea RFCs, ADRs, checkers, mecanismos ni features, y no reabre las
  iniciativas históricas (Planes 146–148, Change Lifecycle MVP, SAE MVP, Prompt Cache MVP,
  Jury Trial MVP, Placement Contract, RFC-75, ADR-15, ADR-16).
- **Promoción de release: release de gobernanza `11.6.2`** (plan 148, vía plan — Change de
  release, sin efecto de payload): promueve a `master` el estado verificado de `dev` tras el
  plan 147, publicando los artefactos de gobernanza y de tooling DEV que `master` no tenía y
  nivelando el artefacto del plan 146, cuya revisión previa había quedado en el árbol
  publicado por el tag `11.6.1`. **No hay cambio de protocolo:** el payload bajo
  `protocol/` es idéntico entre `dev` y `master` y `protocol/.agents/VERSION` es `11.6.1` en
  ambos, de modo que la release publica la versión **del repositorio**, no una versión nueva
  del protocolo; el bump a `11.6.2` y su tag son la excepción de promoción que
  `docs/VERSIONING.md` §3 declara («Releases de gobernanza»), con la justificación registrada
  por el mantenedor. El contenido publicado es: la corrección post-release del plan 147
  (C-1, C-2, dogfoods SAE y resolución de segmentos) y el registro de cierre del plan 146.
  Sin force-push, sin reescritura de historia, sin mover ni alterar tags existentes;
  `ROADMAP.md` y `protocol/` con 0 diff.

### Added

- **Promoción de `dev` y release del protocolo 11.3.0–11.6.1** (plan 146, vía plan;
  Change de release — no toca `protocol/.agents/`, por lo que RFC-56 no aplica): cierra el
  ciclo de los 33 commits que `dev` tenía por delante de `origin/dev` con la operación
  `dev → origin/dev → master → tag 11.6.1 → release 11.6.1`, ejecutada como una única
  Change integral. Se reconstruyeron los 33 commits uno por uno desde Git y se verificó que
  ninguno queda fuera de la línea de desarrollo; se verificó la topología completa
  (`master` en `dc21458`, merge-base `f85b558`, árbol de `master` idéntico al del
  merge-base y `dev` 42 commits por delante), la versión (`VERSION` = `PROTOCOL_VERSION` =
  `11.6.1`, calculada desde la última versión publicada `11.2.0` por la cadena de bumps de
  los planes 119/120/121/142/143), el changelog y el estado de los planes 135–145; y se
  corrió la batería canónica completa, el harness del protocolo, los gates C-1/C-2/C-3 y
  los checkers específicos de release. El release oficializa el rango no publicado completo
  —`11.3.0`, `11.4.0`, `11.5.0`, `11.6.0` y `11.6.1`— con tags anotados sobre el commit de
  promoción de `master` y `dist` regenerado por `publish-dist`: el invariante
  versión ↔ changelog ↔ tag no admite dejar versiones sin tag en `master`, y el precedente
  de la promoción anterior oficializó dos versiones en un solo commit de release. Se
  corrigen además las dos afirmaciones «Tag pendiente de promoción» que la promoción vuelve
  falsas y se reconcilia el snapshot `docs/VERSIONING.md` §9 en el punto de promoción que su
  §5 declara. Sin force-push, sin force-tag, sin reescritura de historia y sin operaciones
  destructivas; `protocol/.agents/`, `dist/`, `ROADMAP.md` y `docs/adr/` con 0 diff. Quedan
  declarados sin resolver dos `GAP` preexistentes: el plan 126 materializó payload sin bump
  de `VERSION` (exención declarada por ese artefacto cerrado) y el commit `65a1113` no cita
  su plan en el asunto. El SHA de promoción, los tags, la publicación de `dist` y la
  verificación post-release se registran en el artefacto de cierre del Plan 146
  (`docs/plans/146-release-promotion-11-6-1.md`).

- **Integral Closure of the Actionable DEV Backlog `I-1`…`I-8`** (plan 145, vía plan;
  DEV-only sobre `tests/`, `runtime/`, `conftest.py`, `docs/` y `.agents/policies/`, sin
  efecto en `protocol/.agents/`, por lo que RFC-56 no aplica): los ocho items accionables
  del inventario posterior al Plan 144 se resuelven por **causa**, cada uno con su
  regresión y su falsación. **`I-1` — aislamiento del pytest harness:** el scratch root
  deja de ser compartido y pasa a ser **propio de cada sesión** —`tests/pytest_isolation.py`
  declara un token explícito, resuelve `scratch_root` bajo `scratch/<token>`, limpia sólo
  su propio directorio y poda por **edad** los de sesiones abandonadas (umbral declarado
  de 24 h, un `stat` por vecino)—, y `conftest.py` declara el token en import time y lo
  exporta por entorno para que un proceso hijo adopte su sesión en vez de inventar otra;
  una sesión sin token se **rechaza** en lugar de recibir un directorio compartido. En el
  runtime DEV, `GitState` gana `git_available` y `observe()` eleva `ObservationError`
  cuando el CLI está disponible y el root existe pero el repositorio no se lee, en lugar
  de degradar a un estado indistinguible de «no existe»; el CLI ausente sigue siendo un
  `GAP` declarado y un `TimeoutExpired` nunca se convierte en `None`. **`I-7`:** la
  métrica `recoveries` deja de contar conducción ordinaria —`_RECOVERY_ACTIONS` queda
  reducido a `RUN_REVALIDATION`, la rama de recuperación de la derivación—, de modo que
  una corrida autónoma sin stops reporta `Recoveries: 0` en lugar de `3`.
  **`I-8`:** `findings_autonomously_corrected` deja de ser una constante y se **deriva**
  de los registros de corrección del journal bajo la regla anti-fabricación existente,
  con la frontera corriente declarada en una nota del resumen en lugar de disimulada.
  **`I-2`…`I-6`:** los headers de los Planes 143 y 144 se transicionan a `Executed`; la
  fila y la serie del Plan 137 en `docs/plans/INDEX.md` y su autodescripción corriente se
  reconcilian; el backlog evidenciado del plan 19 deja de presentar `B-4`/`B-7`/`B-8` como
  abiertos y nombra a la RFC-79 y al Plan 142 como quienes materializaron esos residuos;
  `docs/placement-contract.md` registra `PC-72.1` con el estado corriente del enforcement
  autorizado —librería de tabla de reglas materializada por el Plan 131, **no integrada** y
  advisory— y distingue esa realización mecánica de un enforcement como obligación
  operativa; y `tests/AGENTS.md` completa su conjunto anclado (14 filas) con
  `test_placement_contract_drift.py` y declara la propiedad de sesión del scratch. Sin
  mecanismos, policies, checkers, estados, registries, authority classes, taxonomías ni
  workflows nuevos; `protocol/.agents/`, `dist/`, `ROADMAP.md` y `docs/adr/` con **0 diff**;
  sin RFC, sin ADR, sin `VERSION` bump, sin tag, sin release, sin promoción y sin push.
  Suite **1147 passed** (27 tests nuevos sobre los 1120 del baseline).

- **Empty Remaining Backlog — resolución final de los cuatro residuales del backlog
  operativo** (plan 143, vía plan; DEV-only sobre `docs/`, `tools/`, `tests/`,
  `ROADMAP.md` y `CHANGELOG.md`, con **una excepción de payload declarada y autorizada**:
  la entidad que la H13 regla 11 exige, publicada como PATCH **11.6.1**; ver más abajo el
  apartado `Fixed`): **`HD-10`/plan 25** queda resuelto —la medición del dogfood del perfil
  `trivial` **no es una capacidad implementable del repositorio**: exige una versión
  promovida y una sesión de protocolo real con el usuario, actos externos al lifecycle
  autónomo, de modo que se reclasifica como **actividad de adopción/operación externa** y
  sale del backlog; el perfil está declarado e implementado
  (`protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles` con
  gates `H00, H04, H06` y comportamiento profile-aware verificado en
  `test_gate_validator.py`), la sesión real permanece **no ejecutada** y `<PLAN-141>:PC-2`
  pasa a `resuelta`—. **`<PLAN-142>:F-1`** se implementa: la verificación de la H13 regla
  11 entra en el checker existente de la batería (`tools/check_taxonomy_coherence.py`, check
  9) comparando los cinco campos que la regla nombra en las dos direcciones, con catorce
  casos nuevos y falsación por campo; la corrida sobre el corpus real revela una condición
  preexistente —`CHANGE_GOVERNANCE.md` declaraba `kind: contract` sin entidad contractual
  desde el plan 115—, invisible para una batería que nunca cubrió la regla 11, y su
  registro se autoriza explícitamente bajo este Change (`Clase B`, `Scope` ampliado antes
  del efecto). **`<PLAN-142>:F-2`/`<PLAN-136>:F-1`** se transicionan por CL-8 a `resolved`
  —el destino declarado (RFC-79 decisión 2 + Plan 142) está cumplido—, con sus elementos
  inmutables verbatim. **`C-2 GAP` del plan 116** queda `HISTORICAL / NON-ACTIONABLE /
  RESOLVED` como residual de backlog (`<PLAN-133>:F-1` → `resolved`), sin modificar el plan
  116 ni el contrato de `C-2` y con el `GAP` aún emitido. Sin mecanismos, policies, estados,
  registries, authority classes, taxonomías ni workflows nuevos; sin reapertura de RFC-56/75,
  ADR-15/16 ni C-2/CI; sin promoción, tag, release ni push.

- **Human Decision Backlog Resolution — cierre del backlog `HD-1`…`HD-12` y apertura de
  la vía de payload de RFC-79** (plan 141, vía plan; DEV-only sobre `docs/`,
  `ROADMAP.md`, `CHANGELOG.md`, `tests/` y `tools/`; RFC-79 y plan 142 como vía de
  autorización del trabajo de payload que este Change **decide** y **no ejecuta**): se
  procesan los doce elementos del backlog uno por uno contra el repositorio. **`HD-1`**:
  el Plan 137 **se ejecuta** —el retiro no es expresable en el ciclo de status de planes
  y la guarda tiene valor propio: R3 (coherencia de la forma canónica del contrato) y R5
  (paridad del conjunto de patrones entre `EARS.md` y `EARS_RE`) no están cubiertos por
  ningún otro test, mientras que R4 ya lo cubre
  `protocol/.agents/harness/tests/test_gate_validator.py` (test `test_non_ears_bullet_fails`)— y
  crea `tools/check_ears_coverage.py` y tres suites (91 tests, R3/R4/R5 `VALID` sobre el
  payload real, R1/R2 `N/A` por ausencia de corpus versionado de `TASK_SPECIFICATION.md`).
  **`HD-2`**: `ROADMAP.md` retira del trabajo activo la entrada `EARS structural
  validator`, que declaraba futuro un mecanismo existente desde el plan 66/RFC-57.
  **`HD-3`…`HD-6`** (`F-14`, `F-17`, `F-16`, `B-8` residual) más `F-18`, la metadata
  contractual de taxonomía y el `F-4` de `HD-12`: las representaciones quedan
  **decididas y especificadas** en `docs/rfc/79-payload-normative-residuals.md` (siete
  decisiones: `status: legacy` + `[entries] legacy`; valor reservado `"project_scan"` con
  endurecimiento del checker de `GAP` a `ANOMALY`; shape `documentation`; evento de sesión
  `session_risk`; delimitador `+++` del front matter de KB entry; frontera
  composición↔materialización en `COMPOSITION_OPTIMIZATION.md`; metadata contractual
  alineada con `PROTOCOL_TAXONOMY.md`), con
  `docs/plans/142-payload-normative-residuals.md` como vía de materialización; el
  mantenedor, consultado, decidió **redactar sin aceptar**, de modo que esos elementos
  cierran **bloqueados** con el blocker concreto de la aceptación RFC-56 Clase A.
  **`HD-7`**: catorce findings corregidos y nunca transicionados pasan a `resolved` con
  autoridad humana registrada, preservando verbatim sus elementos inmutables, y
  `<PLAN-136>:F-1`/`F-2` conservan su residual exacto. **`HD-8`**: cada pending decision
  del bundle recibe su determinación individual sin inventar taxonomía. **`HD-9`/`HD-11`**:
  la premisa de RFC-72 §4 queda refutada —el orden normativo existe desde la RFC-78 §5 y
  está implementado y testeado— y la RFC se corrige por su `Amendment Log` junto con el
  enunciado falso sobre el contrato de materialización canónica. **`HD-10`**: el dogfood
  del plan 26 queda satisfecho (su RFC de origen admitía la simulación de fixtures, que el
  plan 46 ejecutó) y el del plan 25 conserva un blocker externo demostrado. **`HD-12`**:
  `F-4` decidido y enrutado; `F-6`/`F-8` corregidos en el espejo de `docs/plans/INDEX.md`;
  `F-7` aclarado en el `Amendment Log` de RFC-74 sin reescribir el plan 91. Sin `VERSION`
  bump y sin tag (DEV-only, RFC-69).

- **Governance Residual Closure — cierre del inventario de gobernanza accionable**
  (plan 140, vía plan; DEV-only, sin efecto en `protocol/.agents/`): se redacta y
  **ejecuta** el Plan 140, que revisa, reconcilia y clasifica los cinco pendientes de
  gobernanza conocidos **sin crear gobernanza nueva** — sin mecanismos, estados,
  registries, checkers, workflows ni authority classes nuevos, y sin modificar
  `ROADMAP.md`, `protocol/`, `runtime/`, `tools/`, `.agents/`, RFCs, ADRs ni los planes
  116 y 138. **A — `<PLAN-136>:PC-5` → `superseded` y `<PLAN-139>:F-1` → `resolved`**:
  la premisa de `PC-5` («la política vigente no contempla qué ocurre cuando una
  determinación de cierre obliga a reconciliar un artefacto excluido del `Scope`»)
  queda superada por la regla vigente, que sí lo define
  (`.agents/policies/validation-closure.md` §5.1/§5.2 y §7;
  `.agents/policies/supervised-autonomous-execution.md` §1.1/§1.4), y no subsiste
  cuestión independiente: la continuidad de la frontera vive en `<PLAN-138>:PC-2`.
  Sólo se actualiza metadata **evolucionable** (LC-1) —el campo `resolución` de `PC-5`
  y el estado de `F-1` más un bloque `## Metadatos de estado (evolucionables)`
  append-only—, preservando observación, evidencia, estado Git y provenance verbatim.
  **B — `B-2` (EARS) satisfecho sin residual**: el mecanismo responsable ya existe en
  el payload (`protocol/.agents/harness/gate_validator.py` con
  `TRIGGERS["H01"]["ears"] = True` y `EARS_RE` con los cinco patrones del estándar),
  con cobertura en `protocol/.agents/harness/tests/test_gate_validator.py` y ejecución
  en el job `check-protocol` de CI; `F-01` quedó resuelta por el plan 33/RFC-34 (bullets
  canónicos) y `F-02` por el plan 29. El dogfood read-only de este Change lo confirma
  (un bullet EARS produce `ears` PASS; el bullet no aceptable del estándar produce
  `ears FAIL`). La guarda de paridad que el Plan 137 proponía **no** es un residual de
  `B-2` sino trabajo nuevo no autorizado (el Plan sigue `Aprobado para redacción`, y
  `Superseded` exige un plan reemplazante inexistente): **no se implementa nada
  nuevo**. **C — `Roadmap Impact` del Plan 137 → `DEFERRED`**: la obligación de
  reconciliar `ROADMAP.md` se gobierna con la pending decision existente
  `<PLAN-137>:PC-1` (owner mantenedor), porque una determinación de impacto es
  obligación de estado y **nunca** autorización de escritura; `ROADMAP.md` queda con
  **0 diff**. **D — `<PLAN-138>:PC-2` clasificada `DEFERRED` y no accionable
  actualmente**, sin introducir Scope Expansion y sin inventar una taxonomía nueva.
  **E — `C-2 GAP` del Plan 116 clasificado histórico/no accionable**: es un `GAP`
  advisory (`exit 0`, `ANOMALY=0`) causado por la ambigüedad `Tier 2` del anchor de un
  plan cerrado bajo la convención anti-auto-referencia; resolverlo exigiría reescribir
  un artefacto cerrado o cambiar el contrato de C-2, ambos prohibidos, y no bloquea
  ningún lifecycle. **Findings propios, corregidos dentro del Scope**: `<PLAN-140>:F-1`
  —el test anclado que el Plan 139 dejó en `tests/test_sae_scope_enforcement_dogfood.py`
  afirmaba que el plan cerrado debía mostrar un diff contra `HEAD`, invariante que sólo
  valía sin commitear, de modo que la suite y CI quedaban rojos en el estado
  comprometido— corregido por `<PLAN-140>:C-1`, que reemplaza la aserción dependiente
  del estado de Git por aserciones de contenido, la regla de que el bloque de metadatos
  es la última región del artefacto y un digest normalizado del contenido normativo
  (los valores de `estado` y `resolución` se canonicalizan por LC-1), **endureciendo**
  la protección en lugar de relajarla; y `<PLAN-140>:F-2` —el `## Checkpoint / cierre`
  del Plan 139 declaraba `e284f98d8915f8c3e917f40218420caf604328b2` como árbol material
  del commit de cierre, cuando el árbol real es
  `2bc144d76ffe2c17432638d1c1208525bc97f3f5` y difiere exactamente en el propio registro
  de gobernanza del cierre— corregido por `<PLAN-140>:C-2` mediante registro factual en
  artefacto nuevo (el plan cerrado no se reabre) y sin afectar la correspondencia R2 del
  estado de cierre. **`<PLAN-140>:F-3`** (`deferred`, owner mantenedor) registra las
  transiciones de estado pendientes y las pending decisions abiertas del Plan 136, fuera
  de los cinco pendientes autorizados. **Inventario final**: `OPEN / ACTIONABLE = 0`,
  con `DEFERRED` e `HISTORICAL / NON-ACTIONABLE` enumerados con su razón, su evidencia y
  su continuidad. Batería canónica PASS; `pytest tests/` PASS; C-1/C-2/C-3 sin
  `ANOMALY`; `ROADMAP.md` con **0 diff**. Sin RFC/ADR nuevo, sin cambio de payload, sin
  `VERSION` bump y sin tag (DEV-only, RFC-69).

- **SAE Governance Boundary Closure — cierre formal de las tres decisiones del
  incidente F-3** (plan 139, vía plan; DEV-only, sin efecto en
  `protocol/.agents/`): se redacta y **ejecuta** el Plan 139, que **materializa
  decisiones humanas ya tomadas** —DEC-1, DEC-2 y DEC-3— sin tomar ninguna nueva,
  sin crear mecanismo alguno y sin tocar `ROADMAP.md`. El enforcement que resuelve
  las decisiones ya existía y está verificado desde el plan 138; lo que faltaba era
  el registro formal y la frase normativa general. **DEC-1 —
  `<PLAN-136>:F-3` → `resolved`**: el incidente ocurrió (el Plan 136 escribió
  `ROADMAP.md` fuera de su `Scope`); el plan 138 corrigió el mecanismo preventivo con
  enforcement **previo a la delegación** basado en el Scope autorizado; la regresión
  específica demuestra que el intento equivalente se detiene **antes** de ejecutar al
  Worker (`test_f3_regression_stops_before_the_write_and_leaves_everything_identical`:
  sin delegación persistida, sin Worker Result, artefacto excluido byte-idéntico,
  invoker nunca alcanzado; y
  `test_the_old_single_path_check_would_have_authorized_this_action`, que fija la
  ceguera estructural que produjo el incidente); la evidencia histórica **no** se
  modifica. La transición se materializa con un bloque nuevo
  `## Metadatos de estado (evolucionables)` en
  `docs/plans/136-d01-mechanical-checker.md` —metadata **evolucionable** según
  `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional;
  LC-1, Incremento 2)`—, preservando verbatim identidad, observación, evidencia,
  estado Git observado y provenance originales, y sin tocar `## Scope`, `Task`,
  Delegación agentiva, tabla de artefactos, anchor, checkpoint ni Nota de ejecución;
  incluye nota explícita de **no retroactividad**: la transición no legitima la
  escritura de `ROADMAP.md` ni `<PLAN-136>:C-3`, que conserva su autorización **no**
  establecida. **DEC-2 — `<PLAN-138>:PC-1` → `resuelta`** con la regla
  `Impact classification != authorization`: `Roadmap Impact: REQUIRED` **no autoriza**
  `write outside authorized Scope`; `Scope`/`Task`/`Authority` tienen precedencia
  sobre cualquier clasificación de Impact; la autorización **no** puede inferirse por
  proximidad semántica, dependencia documental ni requisito de cierre; con el
  artefacto fuera de Scope la única vía es `DEFERRED` con la pending decision
  existente (PC-1). Se materializa en el lugar canónico **existente**, sin policy
  paralela ni duplicación: `.agents/policies/validation-closure.md` §5.1/§5.2 (la
  prohibición de inferir autorización se generaliza a las cuatro vías, referenciando
  el incidente y `<PLAN-136>:PC-4`) y `.agents/policies/supervised-autonomous-execution.md`
  §1.1. **DEC-3 — `<PLAN-138>:PC-2` → `deferred`**: **no existe ni se introduce**
  ningún mecanismo autónomo de Scope Expansion. La policy SAE gana §1.4, que declara
  que el Orchestrator no puede ampliar autónomamente `Task`/`Scope`/`Authority`; que
  una necesidad de ampliarlos es frontera de autoridad humana y produce `STOP` /
  `REQUIRES_HUMAN`; que la vía legítima **no requiere mecanismo nuevo** (decisión
  humana de alcance + reautorización del trabajo que habilita); y que inventar
  protocolo, comando, estado, registry, API, workflow, authority class, entidad o
  estado de lifecycle para ello queda prohibido. **Verificación reutilizada, sin
  tests redundantes**: los ocho puntos exigidos por el Change se mapean a la
  regresión del plan 138 (`tests/test_sae_scope_enforcement.py` y
  `tests/test_sae_scope_enforcement_dogfood.py`), con `runtime/`, `tests/`, `tools/`
  y `protocol/` en **0 diff**. **Finding propio registrado sin forzar a éxito**:
  `<PLAN-139>:F-1` — la premisa de `<PLAN-136>:PC-5` («la política vigente no
  contempla la situación») queda superada por la regla que DEC-2 materializa, pero
  PC-5 no es una de las tres decisiones de este Change y **no** se resuelve: se
  registra la supersesión para que el mantenedor decida su estado formal—.
  **Determinaciones**: `Documentation Impact: REQUIRED` (las dos policies, los
  registros de estado de los planes 136/138, INDEX y CHANGELOG; `docs/CONVENTIONS.md`
  **no** se toca: la regla es operacional y ya tiene lugar canónico);
  `Roadmap Impact: DEFERRED` gobernado por `<PLAN-138>:PC-1` (owner: mantenedor) —
  `ROADMAP.md` con **0 diff**, sin interpretar `REQUIRED` como permiso de escritura—.
  Sin mecanismo, entidad, authority class, state machine, registry, protocolo,
  comando, API ni workflow nuevos; sin RFC/ADR nuevo; sin cambio de payload; sin
  `VERSION` bump, sin tag, sin push, sin merge, sin release y sin promotion.

- **SAE Scope & Authority Hardening — enforcement previo al efecto** (plan 138,
  vía plan; DEV-only, sin efecto en `protocol/.agents/`): se implementa el
  endurecimiento del enforcement de Scope/Authority de Supervised Autonomous
  Execution a partir del incidente `<PLAN-136>:F-3`, y se redacta y **ejecuta** el
  Plan 138. **El defecto**: el gate de SAE del Plan 135 verificaba **un solo**
  target resuelto de la misma declaración de la que salía el Scope
  (`host._autonomy_target_path` → `resolved[0]`), de modo que la comprobación era
  circular y autorizaba la delegación sin demostrar que la escritura fuera interna
  al Scope; la única verificación real (`_scope_violations`) corría **después** de
  la delegación y por eso **detectaba** pero no **impedía**.
  **Enforcement (tres piezas sobre mecanismos existentes, sin vocabulario nuevo
  —se reutiliza `STOP_SCOPE_VIOLATION`— y sin tocar `contracts.py`,
  `derivation.py`, `worker.py`, `agent_worker.py` ni `observation.py`)**:
  **E1** `verify_write_targets` aplica la regla al **conjunto completo** de write
  targets (all-or-nothing; target vacío o no resoluble ⇒ STOP) contra el Scope que
  el Plan **declara** —`## Entregables` + el `Scope set` del anchor + el propio
  Plan, vía `_plan_authorized_scope`— y no contra la declaración que se verifica;
  **E2** *checkpoint de autorización* (`authorization_projection`,
  `authorization_contract_projection`, `authorization_scope_projection`,
  `authorization_drift`): la proyección canónica de `Task` + familia de status
  autorizante + `Scope` autorizado se registra en el journal al autorizar y se
  compara en toda iteración posterior, partida en dos mitades —contrato y scope—
  para que una reescritura que el bound de Scope filtra siga siendo visible como
  divergencia, con el pin tomado de la autorización **más temprana** del plan
  (`host._pinned_autonomy_projection`) de modo que una reescritura entre corridas
  no se re-pinea; **E3** evidencia en el campo `autonomy` del registro de
  iteración que ya existe (targets, decisión de scope, decisión de autoridad, stop
  condition, checkpoint, `authorization_drift`), sin telemetría, store ni registry
  nuevos. **Punto de enforcement**: `ExecutionHost._apply_autonomy_gate`, invocado
  desde `iterate` **antes** de `_execute_delegation`. **La detección posterior se
  conserva** como defensa en profundidad para la escritura que ocurre dentro del
  `AgentInvoker` —límite que el host no puede interponer y que se declara como tal,
  sin fingir una garantía que la arquitectura no proporciona—.
  **Policies reconciliadas** (`Documentation Impact: REQUIRED`):
  `.agents/policies/supervised-autonomous-execution.md` §1.1 (Scope precede a toda
  obligación de estado/cierre), §1.2 (checkpoint de autorización y prohibición de
  retroactividad), §1.3 (una escritura se autoriza entera) más §5 (nuevas stop
  conditions), §9 (impacto fuera de Scope ⇒ `DEFERRED` con PC-1, nunca escritura),
  §10 (prevención vs. detección) y §12 (límites declarados);
  `.agents/policies/validation-closure.md` §5.1/§5.2 (`REQUIRED` es obligación de
  estado, **nunca** autorización de escritura; `Roadmap Impact: REQUIRED` no amplía
  el `Scope`, con `<PLAN-136>:PC-4` como origen) y §7 (nuevas condiciones de
  stop); `.agents/policies/autonomous-orchestration.md` §11.3 (prevención vs.
  detección y punto de enforcement); `runtime/README.md` (sección SAE).
  **Regresión F-3** en `tests/test_sae_scope_enforcement.py`: artefacto excluido
  **parametrizado** (`docs/ROADMAP-LIKE.md`, nunca `ROADMAP.md` hardcodeado) con
  Plan temporal, `Scope` que lo excluye, obligación `REQUIRED` que lo nombra e
  invoker inyectado que **realmente escribe**; demuestra `STOP_SCOPE_VIOLATION` /
  `REQUIRES_HUMAN` previo, **ausencia de delegación persistida**, artefacto
  byte-idéntico, elementos de autorización (Scope/Task/Authority) byte-idénticos,
  evidencia reconstruible y no legitimación retrospectiva; y deja registrado que el
  comportamiento previo **no** satisface el caso (detección posterior con el
  artefacto ya modificado). **Falsificación**: matriz completa en la misma suite
  (target/acción permitidos y no permitidos, `REQUIRED` dentro y fuera de Scope,
  conjuntos múltiples con uno fuera, target vacío y no resoluble, reescritura
  retrospectiva de `Task` y de `Scope`, vaciado de la declaración, proximidad
  semántica —contenedor, descendiente, plural, prefijo, `./`, separadores,
  mayúsculas—, `DEFERRED` sin pending decision gobernante, records legítimos del
  host y escritura dentro del worker). **Dogfood** en
  `tests/test_sae_scope_enforcement_dogfood.py`: 12 pruebas que anclan el punto de
  enforcement, las policies, la ausencia de registry/state machine/authority class
  nuevos, el Plan 136 y `ROADMAP.md` **sin modificar**, el envelope del propio Plan
  138 pasando su propia frontera, más un dogfood funcional end-to-end del escenario
  F-3 y de la divergencia entre corridas (con el límite declarado de que el
  repositorio no tiene provider ni modelo: H-1 del Plan 123, y el invoker inyectado
  sustituye al modelo, no al efecto). **Finding propio detectado y corregido**
  (`<PLAN-138>:F-1` / `<PLAN-138>:C-1`): `tests/test_sae_scope_enforcement_dogfood.py`
  figuraba en `## Scope` y en la `Delegación agentiva` pero **no** en
  `## Entregables` —exactamente la clase de divergencia que este Change detecta— y
  se corrigió dentro del Scope autorizado. **Validación**: pytest `1009 passed`;
  seis checkers canónicos PASS; C-1/C-2/C-3 `ANOMALY=0`; Validation Anchor y
  Checkpoint registrados; `**Status:** Executed` con condición derivada `Closed`
  (`Documentation Impact: REQUIRED` reconciliado; `Roadmap Impact: DEFERRED` con
  `<PLAN-138>:PC-1`, owner mantenedor). `<PLAN-136>:F-3` **no** se cerró, el Plan
  136 no se modificó, `ROADMAP.md` quedó con **0 diff**, `<PLAN-136>:PC-5` no se
  resolvió (se re-registró como `<PLAN-138>:PC-2`, no bloqueante) y EARS no avanzó.
  Sin state machine, entidad, authority class, registry, lifecycle, sistema de
  permisos paralelo, mecanismo de Scope independiente ni caso especial para
  `ROADMAP.md`/`Documentation Impact`; sin RFC/ADR nuevo, sin Amendment Log de
  RFC-75, sin cambio de payload, sin `VERSION` bump, sin tag, sin push, sin merge,
  sin release y sin promotion.

- **EARS Structural Validator — preparación del Plan 137 (auditoría de cobertura
  EARS)** (plan 137, vía plan; DEV-only, sin efecto en `protocol/.agents/`): se
  redacta el Plan 137 y **no se implementa nada**. **Hallazgo central**: el
  validador estructural EARS **ya existe en el payload** —
  `protocol/.agents/harness/gate_validator.py` (plan 66, RFC-57) activa el chequeo
  EARS de H01 (`TRIGGERS["H01"]["ears"] = True`, regex con los cinco patrones),
  está cubierto por `protocol/.agents/harness/tests/test_gate_validator.py`
  (`test_valid_h01_passes`, `test_non_ears_bullet_fails`) y corre en el job
  `check-protocol` de CI; verificado por ejecución (un bullet `should` produce
  `ears FAIL` con `decision: FAIL`). La fricción `F-01` de `B-2` (contrato con
  array TOML vs validador de bullets) está **resuelta** por el plan 33/RFC-34, que
  declaró los bullets Markdown como forma canónica. **Subset mecánico
  establecido**: R1 al menos un bullet en `## Acceptance Criteria`; R2 cada bullet
  casa uno de los cinco patrones; R3 criterios sólo en el bloque TOML constituyen
  violación de forma; R4 el validador del payload realmente chequea EARS para H01;
  R5 paridad entre el conjunto declarado en el estándar y el implementado.
  **Bloque no mecánico excluido por nombre**: especificidad y verificabilidad
  (`[agent]`), no-compoundidad (`[agent]`), negaciones y vocabulario modal
  (`protocol/.agents/standards/requirements/EARS.md:Writing rules` 2–3, sin marca `[gate]`), adecuación al dominio y
  derivación desde assumptions (`[agent]`). **Diseño**: guarda DEV de sólo lectura
  `tools/check_ears_coverage.py` que **deriva** el conjunto del payload e
  **invoca** el validador existente —no lo reimplementa—, con las convenciones de
  señales y exit codes vigentes. **Limitación declarada**: la validación EARS
  aplica a `TASK_SPECIFICATION.md`, artefacto de sesión en `.project/` (efímero, no
  versionado), y **no existe corpus real versionado**; la limitación se declara y
  no se convierte en `PASS`. **`ROADMAP.md` fuera de `Scope`**: la obligación de
  reconciliación (`Roadmap Impact: REQUIRED`) queda **pendiente** en
  `<PLAN-137>:PC-1`, conforme a la decisión humana de `F-3`
  (`<PLAN-136>:PC-4`: `Roadmap Impact: REQUIRED` no amplía el scope autorizado).
  Pendientes `PC-1` (reconciliación del roadmap), `PC-2` (ampliar el conjunto
  mecánico: cambio de payload, RFC-56) y `PC-3` (agregar la guarda a la batería
  canónica). Sin modificar `protocol/`, `runtime/`, `.agents/` ni `ROADMAP.md`
  (0 diff), sin RFC/ADR nuevo, sin `VERSION` bump y sin tag.

- **D01 Mechanical Checker — subconjunto mecánico de D01 como checker DEV**
  (plan 136, vía plan; DEV-only, sin efecto en `protocol/.agents/`): materializa
  como verificación reproducible la parte de D01 que es objetivamente chequeable,
  dejando el juicio donde está. **`tools/check_discovery_output.py`** (nuevo)
  inspecciona `.project/knowledge/discovery/` y valida **once puntos
  deterministas**: existencia y no-vaciedad; front matter TOML delimitado y
  parseable; campos requeridos del entry con su tipo; `artifact` =
  `KB_DISCOVERY_ENTRY.md` y `kind` = `snapshot`; coincidencia del `#` con `title`;
  secciones requeridas; resolución de cada path de `source_files` con
  `system_probe` admitido sólo para la entrada de environment; coherencia
  bidireccional `[entries] active` ↔ archivos presentes; coherencia de front
  matter entrada ↔ manifest; `## Project Shape` presente, primera sección de
  contenido y coincidente con el manifest; `distribution.md` presente cuando el
  shape es `library` o `cli`. Los requisitos se resuelven **desde los contratos
  del payload**, leídos como datos de sólo lectura: el mapeo contrato → artefacto
  runtime se lee de la sección `## Location` de cada contrato (18 contratos
  per-entry) y las secciones requeridas de las declaraciones de cada contrato, sin
  lista propia ni tabla de artefactos, preservando el single-source del plan
  47/RFC-48. Reporte en texto y `--json`; contrato de exit codes existente (`0` sin
  `ANOMALY`, `GAP` advisory, `1` ante `ANOMALY`, `2` ante error de lectura); un
  proyecto sin KB es `N/A` y no un fallo; sólo lectura (nada se escribe, repara ni
  archiva). **Los seis ítems de juicio de D01 quedan fuera por nombre** (stack
  real, dependencias reales, patrones con ejemplo, secretos, claims sin fuente,
  merge consistente, api↔shape) y un test de frontera verifica que el checker no
  los reporta. **Fronteras de payload respetadas sin resolverlas:** `F-17`
  (`source_files` sin valor de procedencia para ausencias y hechos de árbol) se
  reporta `GAP` advisory y **nunca** `ANOMALY`, sin exención ad-hoc; `F-16`
  (`project_shape` de repos documentales) acepta los seis valores del enum y no
  decide el shape correcto — ambos quedan como pendientes de payload (`PC-2`,
  `PC-3`). **Suites nuevas**: `tests/test_check_discovery_output.py` (42 pruebas:
  positivos, negativos, falsación, fronteras, determinismo, ausencia, invalidez,
  sólo-lectura, stdlib-only y CLI) y `tests/test_discovery_output_dogfood.py` (12
  pruebas ancladas al payload real, sólo lectura). **No** se agregó el checker a
  la batería canónica: `docs/VERSIONING.md` §4.1 intacto, porque hacerlo crearía
  una obligación de gobernanza sobre todo Change futuro y el Plan no la autorizó.
  `ROADMAP.md` fue modificado **fuera del `Scope`** autorizado: el mantenedor
  determinó que `Roadmap Impact: REQUIRED` no autoriza por sí sola la escritura de
  un artefacto excluido del scope (`<PLAN-136>:PC-4`). La resolución posterior
  (`<PLAN-136>:F-3`, sección «Resolución post-cierre de F-3 (A y B)») confirmó la
  retirada de la entrada `Mechanical D01 subset` como reconciliación factual y que
  `EARS structural validator` pasa a próximo dogfood, y **restituyó `Media`** a su
  prioridad, que la ejecución había cambiado a `Alta` sin evidencia documental.
  Sin entidad,
  registry, state machine, authority, identity ni subsistema de ejecución nuevos;
  sin RFC/ADR nuevo, sin cambio de payload, sin `VERSION` bump y sin tag.

- **Higiene documental y de tests del backlog DEV residual** (plan 144, vía plan;
  DEV-only sobre `tests/` y `docs/`, sin efecto en `protocol/.agents/`, por lo que
  RFC-56 no aplica): resuelve los tres residuales accionables que dejó abiertos el
  inventario read-only posterior al Plan 143. **`AW-1`** — la tabla del conjunto
  anclado de `tests/AGENTS.md` pasa de **8 a 13** filas: se agregan
  `test_placement_dogfood.py`, `test_autonomous_scope_dogfood.py`,
  `test_sae_scope_enforcement_dogfood.py`, `test_discovery_output_dogfood.py` y
  `test_check_ears_coverage_dogfood.py`, los cinco módulos anclados que **citan esa
  misma tabla como su propio contrato**; la definición de «anclado» del contrato
  vigente se aplica, no se reescribe, ninguna fila previa se retira y las demás
  instrucciones del archivo quedan intactas. **`AW-2`** — se eliminan las dos
  sentencias `sys.path.insert` redundantes de `tools/` (`tests/test_check_discovery_output.py`
  y `tests/test_discovery_output_dogfood.py`), duplicación que el bootstrap único de
  la sesión (la raíz `conftest.py`) ya realiza y que `tests/AGENTS.md:Rules` declara
  como tal; se ajustan los imports (`sys` deja de importarse donde quedó sin uso,
  `Path` se conserva donde se usa como anotación) y **no** se toca ninguna de las
  nueve inserciones restantes: agregan la raíz del repositorio para importar
  `runtime/`, se verificaron necesarias y quedan fuera del alcance. **`AW-3`** — se
  reconcilian tres espejos documentales contra su fuente autoritativa, sin tocar la
  fuente: la columna `Status` de la fila de RFC-75 en `docs/rfc/INDEX.md` (declaraba
  implementación pendiente; el header de la RFC declara los Incrementos 0–4
  materializados y el Incremento 5 fuera de alcance), la fila faltante de
  `PROMPT_CACHE_PHASE_1_REPORT.md` en `docs/working/research/INDEX.md` (documento
  versionado y `Origen` de RFC-78) y la fila de `AUDITORIA_SISTEMA.md` en
  `docs/working/audits/INDEX.md` (declarada activa contra su propio banner de cierre
  del 2026-08-14). `docs/rfc/75-…`, `docs/rfc/78-…`, el informe de Phase 1 y la
  auditoría de sistema quedan con **0 diff**. Sin payload, sin `runtime/`, sin
  `docs/adr/`, sin `dist/`, sin `ROADMAP.md`, sin `docs/VERSIONING.md`, sin RFC/ADR
  nuevo, sin `VERSION` bump, sin tag y sin push.

### Modelo conceptual
- **Supervised Autonomous Execution (SAE) para el DEV Autonomous Orchestrator**
  (plan 135, vía plan; DEV-only, sin efecto en `protocol/.agents/`): política
  operacional nueva `.agents/policies/supervised-autonomous-execution.md` que
  formaliza que el host ejecuta, corrige, revalida, recupera y continúa **todo
  paso ya dentro del scope y la autoridad concedidos**, deteniéndose exactamente
  ante una frontera de autoridad. Separa explícitamente **Authority** (qué está
  autorizado), **Scope** (qué trabajo está autorizado) y **Autonomy** (qué
  acciones puede ejecutar el host sin pedir autorización de nuevo), con la regla
  `autonomy ⊆ authorized scope ∧ autonomy ⊆ granted authority`: la autonomía
  nunca amplía scope ni autoridad. Materialización determinista en
  `runtime/orchestrator/autonomy.py` — función pura, sin I/O: `AutonomyEnvelope`
  derivado de lo que el Plan **ya declara** (`## Delegación agentiva`), verificación
  de scope por **pertenencia exacta** (nunca por proximidad semántica: una ruta
  contenedora, descendiente, plural o de nombre parecido queda fuera),
  `evaluate_autonomy` (CONTINUE o parada que nombra la frontera y la autoridad que
  decide en su lugar), `evaluate_finding_resolution` (corrección autónoma bajo las
  once condiciones declaradas; una corrección estructural —RFC, ADR, Protocol,
  payload, authority, lifecycle, decisión normativa— escala) y `summarize_autonomy`
  (resumen derivado del journal y de los Worker Results; vista, no sistema de
  métricas). Vocabulario cerrado ampliado en `contracts.py` y gate **opt-in** en
  `host.py` / CLI `--sae`: sin él el loop se comporta exactamente como antes.
  **Frontera de findings** (decisión del mantenedor, `<PLAN-135>:PC-02`): el Plan
  pre-autoriza la **acción de corregir** dentro del scope —mecanismo ya vigente:
  la corrección la autoriza el Plan aprobado y `C-<n>` es factual, no normativo— y
  el humano conserva la **transición de estado** del finding (`resolved`/
  `deferred`/`superseded`), que es decisión humana con evidencia (CL-8, ADR-16
  `AU-3`); no se adquiere autoridad nueva ni se modifica ninguna regla normativa.
  Un finding bloqueado no bloquea trabajo independiente autorizado. Suite nueva
  `tests/test_autonomous_scope.py` con los catorce casos exigidos y la falsación
  explícita (scope expansion disfrazado, authority expansion, RFC/ADR implícito,
  cambio de Protocol, cambio de lifecycle, resolución autónoma de decisión humana,
  release/promotion, documentación normativa inventada). Sin entidad, registry,
  state machine, lifecycle, authority class, identity primitive, worker type,
  daemon, database ni sistema de tracing nuevos; sin RFC/ADR nuevo, sin cambio de
  payload, sin `VERSION` bump y sin tag.

### Modelo conceptual

- **Cierre formal de Closure Evidence Integrity y baseline para D01** (plan 134,
  cierre documental, docs-only): verificación término por término del estado ya
  ejecutado —baseline, existencia y materialización del Plan 134, working tree,
  C-1/C-2/C-3, los seis checkers canónicos, `C-2 ANOMALY=0`, el `GAP` preexistente
  del Plan 116, ausencia de cambios pendientes, `protocol/` intacto y Planes
  históricos 120–133 sin tocar— y una única corrección documental mínima: el
  registro de cierre no enunciaba una por una las seis condiciones derivadas
  (`Promoted` no aparecía; `Released` sólo incidentalmente), de modo que el estado
  de cierre no era reconstruible sin inferencia; se agregó la tabla
  `Verified/Executed/Committed/Closed/Promoted/Released` con valor y evidencia
  (`<PLAN-134>:F-5` resuelto por `<PLAN-134>:C-3`). La verificación detectó además
  que el **estado validado por A1 no era reconstruible desde el commit**
  (`e415e03e…` era un objeto git válido pero nunca árbol de ningún commit, y su
  delta no reproducía desde el estado commiteado): A1 queda `stale` sin mutarse y
  se registra la **revalidación A2** sobre el estado reconstruible
  (`751d7c7d…` / `b580f894…`), que es el que el checkpoint certifica
  (`<PLAN-134>:F-6` resuelto por `<PLAN-134>:C-4`); es la misma clase de defecto
  que `<PLAN-133>:F-5` y una limitación del procedimiento vigente —identidades
  medidas sobre el índice staged—, no del modelo. **No** se modificó el modelo
  semántico, **no** se alteró R4, **no** se tocó el Plan 116, **no** se agregó el
  SHA del commit de cierre como requisito del template y **no** se modificó ningún
  Plan histórico. **Pendientes preservados explícitamente:** (1) *R4 / locator del
  commit de cierre* — pending decision, owner mantenedor, scope cambio futuro de
  procedimiento (registrar el SHA del cierre, mantener R4 opcional u otra forma de
  locator reproducible: **no se eligió opción**); (2) *Plan 116* — `GAP`
  preexistente de C-2 por ambigüedad de revalidaciones múltiples, boundary de
  interpretación humana que **no bloquea el cierre** bajo las reglas actuales. Se
  registra además que la consigna de cierre describía el Change anterior con
  `<PLAN-134>:F-5`/`C-*` cuando el `F-5`/`C-4` reales pertenecen al **Plan 133**:
  la premisa confundía los namespaces de dos Planes y el repositorio era y es
  coherente (no se cambió nada para hacerla coincidir). Sin `VERSION` bump ni tag;
  sin push, merge, release ni promoción.
- **Integridad de la evidencia de cierre y contrato de C-2** (plan 134,
  docs-only + tooling DEV): el Change Lifecycle DEV gana un **modelo normativo**
  que separa tres conceptos que no deben colapsarse —el **estado validado** (lo
  que la validación consumió), el **estado de cierre** (lo que el checkpoint
  certifica, por correspondencia GC-1 con el anchor aplicable) y el **árbol
  material del commit de cierre** (un hecho de Git)— y establece que
  `validated tree == commit tree` **no es un requisito**: RFC-75
  `Mecanismo 7 — Git Checkpoints` autoriza que el commit de cierre incluya
  governance (INDEX, CHANGELOG, ADR, docs), por lo que `A ≠ B` es esperado, no
  una violación de GC-1. La **auto-referencia** del artifact de cierre se resuelve
  de forma declarativa (el scope se fija antes de escribir los registros; la
  identidad del estado de cierre es el par delta + state identity del anchor
  aplicable; el commit se localiza por su mensaje) sin introducir identidad,
  estado ni registry nuevos. **Defecto confirmado y corregido**: el contrato
  documentado de C-2 declaraba «closure state = tree id del commit de cierre
  final», relación que contradecía la normativa y que además era **inalcanzable
  en el corpus real** —las entradas «Commits de cierre» de los Planes 120–133
  identifican el commit por mensaje y sin SHA, así que la rama de contradicción
  nunca se ejecutaba—; el contrato se fija ahora en R1–R4
  (`.agents/policies/validation-closure.md:5`,
  `.agents/policies/lifecycle-checkers.md` y el docstring del checker) y la
  divergencia estado-de-cierre ↔ árbol material pasa a **GAP advisory con
  requisito de atribución** en lugar de ANOMALY, preservando R2 (correspondencia
  con un anchor registrado) como el nivel ANOMALY. El registro de cierre del
  template separa «estado de cierre (identidad)» de «árbol material del commit».
  **Los 12 Planes históricos examinados (120, 123–133) se clasificaron
  `CORRECT`** y no se modificó ninguno: declaran el estado validado, que es
  exactamente lo que GC-1 exige. C-1 y C-3 declarados `NOT_REQUIRED`. No cambia
  `Committed`, `Closed`, `Released` ni la condición derivada `Closed`; sin RFC ni
  ADR nuevos, sin `VERSION` bump ni tag.

- **Roadmap Impact en el Change Lifecycle DEV y barrido documental integral**
  (plan 133, docs-only): el Change Lifecycle DEV gana una determinación de cierre
  nueva, **Roadmap impact**, **independiente** de **Documentation impact** y con
  los mismos tres valores (`REQUIRED` / `NOT_REQUIRED` / `DEFERRED`). Regla
  central: `Roadmap impact: REQUIRED` **no** significa editar `ROADMAP.md` —el
  artefacto a reconciliar se determina por *ownership/source of truth*
  (`ROADMAP.md` como mapa operativo, `docs/plans/INDEX.md`, los índices de
  RFC/ADR, un plan activo o la documentación operativa que posee el estado)— y
  `ROADMAP.md` sigue siendo un mapa operativo, nunca un changelog. Las dos
  determinaciones no se fusionan ni se sustituyen: `Documentation impact:
  REQUIRED` con `Roadmap impact: NOT_REQUIRED` es válido, y también lo son
  `REQUIRED`/`REQUIRED` y `NOT_REQUIRED`/`REQUIRED`. Se formaliza como
  subsección normativa en `docs/CONVENTIONS.md`, semántica operativa en
  `.agents/policies/validation-closure.md` §5.2 (con §5.1 y la condición de stop
  ajustadas), `.agents/workflows/change-lifecycle.md:9. Closure and handoff`,
  `docs/VERSIONING.md` §10 y el campo del `## Checkpoint / cierre` del template
  de plan. Sin segunda lifecycle, fase, estado, entidad, registry, tracker,
  checker ni campo obligatorio nuevos; no se reclama el rótulo «Incremento 5» de
  RFC-75 (track de coordinación/handoff fuera de alcance por decisión de la RFC).
  **Barrido documental:** se corrigieron cuatro defectos de documentación de
  estado actual —rutas pre-disolución en el header de `CHANGELOG.md` (`plans/`,
  `plans/rfc/`, `.agents/harness/…` → `docs/plans/`, `docs/rfc/`,
  `protocol/.agents/…`), el ancla de migración y la lista incompleta de la
  batería canónica en `docs/CONVENTIONS.md` (enumeraba tres de los seis
  checkers), la atribución de `B-7` al Plan 43 en `docs/plans/INDEX.md` (es
  `B-4`, F-04; el residuo de `B-7` son los planes 29 y 52) y el título
  «planes activos» de la sección del roadmap del Execution Context (sus cuatro
  planes están `Executed` desde agosto 2026)—. Cierra la continuidad de
  `<PLAN-132>:F-2` / `<PLAN-132>:PC-1`. `protocol/.agents/`, `dist/`, los RFCs,
  los ADRs, los planes cerrados y `ROADMAP.md` sin cambios; documentación
  histórica no reescrita (RFC-46). Sin ADR, sin migración, sin `VERSION` bump ni
  tag.
- **Actualización del Roadmap al estado real** (plan 132, docs-only): `ROADMAP.md`
  deja de presentar como backlog activo la tabla histórica B-1…B-8 —cuyos
  problemas originales están resueltos— y pasa a ser un **mapa operativo
  actual** con las categorías separadas: trabajo activo/dogfood, pendientes que
  requieren autorización, candidatos futuros e histórico resuelto. Se registran
  como trabajo **derivado nuevo** el checker D01 mecánico (próximo dogfood) y el
  validador estructural EARS (siguiente), sin reabrir `B-1`/`B-2`; como
  **pendientes de payload que requieren RFC-56** el residuo de `B-4` (`F-14`,
  `F-17`), la clasificación `project_shape` para repositorios documentales/de
  protocolo de `B-7` (`F-16`) y el slot de session risk de single-instance en el
  catálogo de métricas (`B-8`); y como **candidato futuro** el checker mecánico
  de `.last_discovery` (`B-3`). `B-5` y `B-6` dejan de figurar como pendientes.
  El registro histórico permanece en `docs/plans/INDEX.md`, los planes y las
  RFCs; el Roadmap no lo duplica. Sin tareas nuevas, sin cambios en
  `protocol/.agents/`, `runtime/`, `tools/` ni `tests/`; sin ADR, sin migración,
  sin `VERSION` bump ni tag.
- **Implementación mecánica del Placement Contract** (plan 131, DEV `runtime/` +
  `tests/`, sin efecto en el payload): `docs/placement-contract.md` se materializa
  como un **resolver determinista** — `PLACE` con el namespace canónico y la regla
  que lo autoriza, o `STOP` con el disparador que falta — de modo que un agente
  deja de tener que **adivinar** dónde va un artefacto. Propiedad garantizada:
  `regla explícita y aplicable → PLACE`; `sin regla aplicable / regla ambigua /
  información insuficiente → STOP`; `camino plausible → NUNCA PLACE`. Nuevo
  paquete `runtime/placement/` (`rules.py` realiza la tabla de familias del
  contrato §6 con la procedencia de cada fila; `resolver.py` implementa el
  algoritmo §7 y la verificación de ubicación de `§16 PC-51`), con tres suites:
  comportamiento y falsación, guarda de deriva contra el contrato y *dogfood*
  anclado al repositorio real. `canonicality` **nunca** selecciona ni crea
  namespace (es un cualificador); `kind` no es un enum global cerrado (el
  vocabulario es domain-scoped y un kind sin regla devuelve `NEW_FAMILY`); las
  excepciones son una **entrada** del llamador, no un registry. **El enforcement
  se materializa como librería, no como hook**: `docs/placement-contract.md`
  §23/§24 (`PC-78`/`PC-79`) excluyen el hook del Orchestrator y §22 (`PC-73`) lo
  define como consumidor, así que no se integra en `runtime/orchestrator/`. El
  contrato queda **con 0 diff**: 80 reglas y 3 variantes intactas. Sin entidad
  `Placement`, registry, base de datos, ID, state machine, clase de autoridad,
  lifecycle, taxonomía global de artefactos ni identidad universal nuevos; sin CI,
  hook de pre-commit, branch protection ni enforcement global; sin ADR; sin
  migración. Sin `VERSION` bump ni tag.
- **Corrección nomenclatural de Plan 129** (plan 130, docs-only): se corrige la
  colisión de identificadores registrada en `<PLAN-129>:F-2`. Los identificadores
  de decisión de Plan 129 pasan de `PC-1`/`PC-2`/`PC-3` a **`PLAN-129:DEC-1`**,
  **`PLAN-129:DEC-2`** y **`PLAN-129:DEC-3`**, de modo que dejan de colisionar con
  las etiquetas de regla internas de `docs/placement-contract.md`
  (`PC-1`…`PC-80`, más `PC-31a`…`PC-31c`). El Placement Contract queda **con 0
  diff**: no se renumeran sus reglas ni cambia su contenido normativo. `<PLAN-129>:F-2`
  pasa a `resolved` y se registra `<PLAN-129>:C-2`. Ninguna semántica cambia: la
  decisión de persistencia de `.project/changes/`, la dirección autorizada del
  enforcement y el carácter documental de las excepciones permanecen idénticos.
  No se crea ADR, no se introduce una convención global de nomenclatura, no hay
  migración. Sin `VERSION` bump ni tag.
- **Cierre de `PLAN-129:DEC-1`, `PLAN-129:DEC-2` y `PLAN-129:DEC-3` del Placement Contract** (plan 129, docs-only):
  se cierran las tres decisiones pendientes de `docs/placement-contract.md`.
  **`PLAN-129:DEC-1`**: `.project/changes/` es **project-durable** y **Git-persisted**, y el
  contrato separa tres propiedades que no deben conflacionarse —
  `project-durable` (persistencia), `git-persisted` (preservación/versionado por
  Git) y `git commit` (**operación** gobernada por el Change Lifecycle y su
  autoridad). No se autoriza auto-commit ni se establece `always`/`never commit`
  ni `auto-ignore`; el contrato no adquiere autoridad para ejecutar commits y no
  modifica el Change Lifecycle. **`PLAN-129:DEC-2`**: el **enforcement mecánico y
  determinista** del contrato queda **autorizado como dirección de
  implementación futura**, con el boundary `Contract = fuente normativa ·
  Enforcement = realización mecánica · Orchestrator = consumidor`, la prohibición
  de convertirse en segunda fuente normativa, la regla «si implementación y
  contrato discrepan, gobierna el contrato», y las ocho invariantes **E-1…E-8**
  (determinismo; placement explícito; STOP; no guessing; el enforcement no es
  source of truth; separación de autoridad; el Orchestrator no reinterpreta STOP
  como PLACE; escalado a autoridad humana). **El enforcement NO está
  implementado**: sin checker, resolver, servicio, hook del Orchestrator,
  integración CI, registry, schema, database ni state machine. **`PLAN-129:DEC-3`**: las
  excepciones son **documentales por defecto**, sin representación estructurada
  ni identificadores, con el procedimiento localizar → verificar owner →
  interpretar → aplicar → STOP, y sin prohibición permanente de una
  representación futura. Sin migración, sin ADR nuevo, sin `VERSION` bump ni tag.
- **Materialización del Repository/Artifact Placement Contract** (plan 128,
  docs-only): se crea `docs/placement-contract.md` como documento normativo
  independiente que determina dónde debe ubicarse un artefacto nuevo en este
  repositorio, o exige detenerse. Regla central: *canonicality qualifies
  placement; it does NOT determine placement*; el algoritmo resuelve
  `domain/owner → kind/family → family rule → canonical namespace → canonicality
  qualification → constraints → PLACE | STOP`, y `GUESS` no es un resultado
  admisible. Decisiones humanas materializadas: **OQ-2 = NO** (las excepciones
  se registran en el artefacto que posee la decisión, acotadas al artefacto o la
  familia; sin registry, schema, database, índice global ni identity primitive,
  y sin prohibir una representación machine-locatable futura); **OQ-3 = A**
  (documento independiente bajo `docs/`, sin namespace nuevo, referenciado desde
  `AGENTS.md` sólo para discovery); **OQ-4 = NO** (sin ADR nuevo; el contrato
  materializa ADR-17 y ADR-18 y queda downstream de ambos). La persistencia Git de
  `.project/changes/` permanece
  `OPEN / DEFERRED`: se registra `project-durable ≠ git-committed` sin
  establecer política de Git para `.project/changes/`. Sin registry, checker,
  schema, state machine, clase de autoridad, integración de enforcement ni
  migración. Sin `VERSION` bump ni tag.
- **Cierre de diseño del Repository/Artifact Placement Contract** (plan 127,
  docs-only): se registra como traza versionada el diseño del contrato de
  placement y su corrección final. Tesis: `domain/owner → kind/family →
  family rule → canonical namespace → canonicality qualification → constraints
  → PLACE | STOP`, con **dos discriminadores** (dominio/owner, kind/family) y
  **un cualificador** (canonicality). Regla central: *canonicality cualifica
  placement; no lo determina*; la ubicación proviene siempre de una regla
  explícita y su ausencia produce **STOP**, nunca inferencia. `generated` no
  implica estar fuera del repositorio, fuera del canonical state, ignorado,
  branch ni non-canonical; `derived` no implica compartir namespace con su
  fuente. `kind` no es un enum global cerrado (tabla domain-scoped, ADR-18
  `RS-11`). Inventario: 15 familias canónicas + 3 reglas root-anchored + 2
  no-familias. Distribución declarada **domain+namespace-scoped**
  (`protocol/.agents/` se distribuye; el `.agents/` de DEV nunca). Sin registry,
  sin checker, sin schema, sin namespace nuevo, sin state machine, sin clase de
  autoridad, sin ADR adicional y sin migración. Quedan **abiertas** `OQ-2`
  (excepciones machine-locatable), `OQ-3` (ubicación canónica del contrato),
  `OQ-4` (ADR-worthiness de la materialización) y la persistencia Git de
  `.project/changes/`. **Design: CLOSED · Placement Contract: NOT CREATED ·
  Migration: NOT STARTED · Release: NOT AUTHORIZED.** Sin `VERSION` bump ni tag.
- **Frontera del payload, provenance y clasificación** (plan 126, ADR-18; Clase B
  de RFC-56): se materializan las decisiones arquitectónicas C–K. Los tests del
  harness (`.agents/harness/tests/`) quedan declarados **parte del payload
  distribuido**, como suite de regresión de los scripts que sí se distribuyen,
  mientras los cinco checkers de `tools/` permanecen DEV-only; el payload puede
  conservar sus dos citas de **fuente normativa** en `docs/rfc/` mediante una
  excepción acotada al par (archivo citante, target exacto); el checker de frontera
  incorpora `docs` como segmento prohibido —la regla pasa a ser aplicable, no sólo
  declarada— con allowlist de provenance y cobertura de tests; `tags` se documenta
  como **vocabulario no cerrado** y `tags.kind` como no exhaustivo, con
  `state_machine` y `taxonomy` añadidos; la clasificación documental DEV se
  corrige **en el lugar** (`docs/architecture/` → Historical, la auditoría de raíz
  → Working/Audit) sin reorganizar `docs/`; un INDEX es **opcional y semántico**;
  y la creación de `.project/` por el health probe se acepta como correcta, sin
  cambio de comportamiento. Sin migración, sin `VERSION` bump ni tag.
- **Decisiones arquitectónicas de estructura del repositorio** (plan 125,
  ADR-17): se registran las decisiones humanas del mantenedor sobre la estructura
  del repo fuente, derivadas de la Repository Structure Architecture Review
  (read-only) y de su Decision Set. **A3**: lifetime permanece como propiedad
  semántica en `docs/` y no se convierte en una dimensión física general del
  árbol; se admite separación física específica dentro de `.project/` entre
  estado durable y session-ephemeral. **B4**: arquitectura estructural compuesta
  por namespace/dominio, sin una única estructura física global obligatoria; B4
  no autoriza migración por sí mismo. **F1**: `.project/changes/` conserva su
  path, el contrato Protocol debe distinguir explícitamente project-durable de
  session-ephemeral y «durable» no implica Git-committed. **L1**: A y B son
  ADR-worthy, materializado en `docs/adr/17-repository-lifetime-and-composite-structure.md`.
  Las decisiones de placement C, D, E, G, H, I, J y K permanecen **abiertas**.
  El Repository/Artifact Placement Contract queda como trabajo posterior
  (downstream), no diseñado. Sin cambio de mecanismos, invariantes ni autoridad;
  cambio docs-only: sin `VERSION` bump ni tag (RFC-69).
- **Cierre del MVP de Change Lifecycle DEV — reconciliación normativa de RFC-75**
  (plan 118, RFC-75): RFC-75 reconcilia su registro con el estado real alcanzado
  por sus Incrementos 0–4, sin rediseño. Su `## Amendment Log` registra las cuatro
  materializaciones posteriores que ningún plan había autorizado a registrar
  (Incremento 4 / Unidad D — plan 98; F-1 sobre la selección del anchor aplicable
  en C-2 — plan 99; C-3 lineage checker — plan 100; capa operacional `.agents/` —
  plan 101); se corrige el header que declaraba implementación pendiente y se
  marcan los diez criterios de aceptación con evidencia rastreable.
  `docs/VERSIONING.md:4.1` registra los gates de lifecycle C-1/C-2/C-3 como
  conjunto adicional advisory/factual (fuera del bloque de comandos y de CI).
  Sin cambio de mecanismos, invariantes ni decisiones; cambio docs-only: sin
  `VERSION` bump ni tag (RFC-69).
- **Revisión de la serie Proposal completada** (plan 57, RFC-56): las 23 RFCs
  de la serie 32–54 quedaron `Accepted` y sus planes asociados (31–53) están
  `Executed`. Sin cambio de payload; solo estados y traza de gobernanza.
- **Modelo de Context Persistence y Cacheability** (plan 86, RFC-71): la RFC-71
  pasa a `Accepted` como modelo semántico de reutilización del Execution
  Context (vocabulario normativo, segmentos Core/Project/Worker, identidades
  compuestas, ortogonalidad de scope/persistence/cacheability/memoization/
  isolation/lifecycle, invalidación por identidad e invariantes I-001…I-012);
  formaliza la fuente de verdad previa a las RFCs 72–74 (provider prompt
  cache, persistence de proyecto y telemetría/economía), que siguen en
  `Proposal`. Cambio docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).
- **Modelo de la capacidad de Provider Prompt Cache** (plan 87, RFC-72): la
  RFC-72 pasa a `Accepted` como modelo de la capacidad de materialización y
  prompt caching del provider (`MaterializationIdentity` con sus reglas
  condicionales, Canonical Materialization e I-MAT-001, Ordering Contract con
  orden OPEN/DEFERRED, Stable Prefix como propiedad de la materialización,
  Provider Prompt Cache Capability, Provider Adapter Boundary,
  `ProviderCacheReference` opaca, semántica de hit/miss, invalidación en tres
  dominios, admisión como policy e invariantes I-MAT-001…I-MAT-012); formaliza
  la frontera de materialización sobre el modelo semántico de la RFC-71; las
  RFCs 73–74 (persistence de proyecto y telemetría/economía) siguen en
  `Proposal`. Cambio docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).
- **Modelo de persistence del contexto de proyecto y Discovery** (plan 92,
  RFC-73): la RFC-73 pasa a `Accepted` como modelo de persistence del contexto
  de proyecto y Discovery (Project Knowledge como abstracción arquitectónica,
  isolation por `ProjectIdentity`, hashes de discovery ≠ `SegmentContentIdentity`,
  frescura/revalidación, provenance e invariantes I-PROJ-001…I-PROJ-012);
  formaliza la fuente de verdad de persistence previa a la implementación
  (plan 90, gated a RFC-73 `Accepted`); la RFC-74 sigue en `Proposal`. Cambio
  docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3).
- **Modelo de economía del cache, telemetría y evidencia de admisión** (plan 93,
  RFC-74): la RFC-74 pasa a `Accepted` como fuente de verdad de medición (capas
  de economía no confluibles, avoided work, vocabulario de eventos de reuse,
  taxonomía de misses, experimentos e invariantes I-ECO-001…I-ECO-006; sin
  thresholds ni pricing); formaliza la capa de medición de las RFCs 71–73 sin
  redefinirlas. Aceptación docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3); no implica implementación — la implementación
  (eventos/catálogo/agregador) queda en el plan 91, `Aprobado para ejecución`.
- **Modelo de registro de ejecución** (plan 103, RFC-64): la RFC-64 pasa a
  `Accepted` como modelo de identidad de ejecución por composición
  (`execution_id = (session_id, iteration)`), roles disjuntos de los cuatro
  registros (state.json, HARNESS_REPORT, SESSION_LOG, METRICS), alcance de
  `state.json` (gates de transición H00–H07, H11 + status terminal), semántica
  temporal UTC con fuente declarada (`clock`), correlación por event keys
  (`trigger`/`seq`) y registro obligatorio de `context_budget` por delegación
  con budget (invariantes EI-001…EI-003, TR-001…TR-005, TM-001…TM-003,
  OBS-001…OBS-003). La decisión humana de aceptación incorpora tres lecturas de
  implementación que forman parte de la decisión: `clock` implementa la fuente
  `agent_clock` (sin renombrar a `source`); `seq` estrictamente monótono por
  sesión para EI-003/TR-004; TR-002 con tolerancia de 60 segundos y
  divergencias que deben registrar `timestamp_divergence.cause`. Aceptación
  docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3); no
  implica implementación — el plan 78 permanece `Aprobado para ejecución` sin
  ejecutar (sus condiciones conocidas de ejecución futura quedan preservadas
  como contexto, no ejecutadas).

### Changed

- **Corrección post-close del glosario — F1–F5** (plan 106): reparadas en
  `docs/glossary/` las referencias de autoridad malformadas (F1/F2), la
  referencia `path:section` no determinista (F3); agregada la regla explícita
  de cobertura selectiva y alta de entradas (F4); normalizado el vocabulario
  de `Status` con restricciones de uso modeladas por separado (F5). Cambio
  docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3); sin
  cambios en el payload del Protocol ni en el Plan 105 (permanece `Closed`).
- **Arquitectura terminológica y glosario** (plan 105): vocabularios
  DEV/Protocol separados con puente descriptivo; glosario
  `docs/glossary/INDEX.md` + `terms.md` como registro Inventory/DESCRIPTIVE no
  normativo (término → scope → status → autoridad, sin definiciones
  duplicadas); reglas D1–D5 (convención AGENTS/INDEX/ENTRYPOINT preservada;
  `SCI` desnudo prohibido en texto cross-layer nuevo; calificación obligatoria
  de términos overloaded) en `docs/CONVENTIONS.md`; semántica de archivos y
  mapa de clase en `docs/AGENTS.md`; punteros de descubrimiento en root
  `AGENTS.md` y `.agents/AGENTS.md`. Cambio docs-only: sin `VERSION` bump ni
  tag (ver `docs/VERSIONING.md` §3); sin cambios en el payload del Protocol.
- **Taxonomía documental y layout del repo fuente** (Plan A, RFC-69): la
  documentación se reorganiza bajo `docs/` (`rfc/`, `plans/`, `architecture/`,
  `working/`), se crea `docs/CONVENTIONS.md` con la normativa, los INDEX pasan
  a ser registro/navegación, los checkers se migran al layout nuevo y los
  working docs quedan contenidos y versionados. Cambio docs-only: sin `VERSION`
  bump ni tag (ver `docs/VERSIONING.md` §3).
- **Gobernanza ADR del repo fuente** (plan 83, RFC-69): `docs/adr/` materializado
  con 14 ADRs individuales (ADR-01…ADR-14 ↔ D0–D13 preservadas como identidad
  histórica), matriz `D# ↔ ADR ↔ RFC ↔ plan` en `docs/adr/INDEX.md`, template
  `_TEMPLATE.md`, ciclo de status ADR en `docs/CONVENTIONS.md` y cobertura de
  `docs/adr/` en los checkers de estructura y citas. Cambio docs-only: sin
  `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3).
- **Change Lifecycle de ARgentOS DEV — Master Action Plan** (plan 94, RFC-75):
  define la estrategia incremental del Change Lifecycle del repo fuente
  (seis incrementos conceptuales 0–5 de RFC-75 agrupados en unidades de
  implementación iniciales A: 0; B: 1+3 en batch operacional; C: 2; D: 4, con
  el Incremento 5 deferido), derivada de RFC-75 `Accepted` y de los ADR-15/16:
  semántica de Verified/Executed/Committed/Closed/Promoted/Released, modelo de
  Change Levels, frontera DEV/Protocol, dogfooding y roadmap para los planes de
  implementación 95+. Plan docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).
- **Change Lifecycle de ARgentOS DEV — Unidad A / Incremento 0** (plan 95,
  RFC-75): la gobernanza DEV incorpora la semántica aprobada del Change
  Lifecycle (condiciones derivadas y vocabulario
  Verified/Executed/Committed/Closed/Promoted/Released/Abandoned, modelo de
  Change Levels con ejes independientes de RFC-56 y L0 provisional, frontera
  DEV/Protocol, serie como identidad derivada) y el observability schema
  baseline de las métricas de lifecycle en `docs/CONVENTIONS.md`,
  `docs/VERSIONING.md`, `AGENTS.md` y `docs/AGENTS.md`. Sin machinery nueva
  (anchors, checkpoints, findings, pending y checkers quedan para los
  Incrementos 1–4). Cambio docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).
- **Change Lifecycle de ARgentOS DEV — Unidad B / Incrementos 1+3** (plan 96,
  RFC-75): la gobernanza DEV materializa los mecanismos operativos de los
  Incrementos 1 y 3 — Validation Anchor (VC-1) con campos (declared scope,
  validation command-set, effective inputs, observed dependencies,
  environmental factors y Scoped Content Identity v1 por primitivas git) en el
  template de Plan y el Amendment Log de RFC; intake fallback con `Change
  Level` en el primer artifact (L0 provisional y triggers); serie como
  identidad derivada (declaración + relaciones RFC↔Plan); checkpoint de cierre
  (GC-1) con consistencia anchor↔checkpoint antes de `Closed`,
  multi-commit/multi-RFC y docs-only sin release — en `docs/CONVENTIONS.md`,
  `docs/VERSIONING.md` (§7/§10/§11), `AGENTS.md`, `docs/AGENTS.md` y los
  templates de Plan/RFC. El propio plan 96 registró el primer anchor y el
  primer checkpoint reales (dogfooding). Cambio docs-only: sin `VERSION` bump
  ni tag (ver `docs/VERSIONING.md` §3).
- **Change Lifecycle de ARgentOS DEV — Unidad C / Incremento 2** (plan 97,
  RFC-75): la gobernanza DEV operacionaliza para artifacts nuevos findings y
  corrections con refs calificadas `<artifact>:F-<n>`/`C-<n>` (LC-1) y pending
  decisions per-artifact (PC-1): subsecciones operativas en
  `docs/CONVENTIONS.md` (findings/corrections, pending, mapa de aplicabilidad),
  sección opcional en el template de Plan y guía de refs en el template de RFC,
  DoD y schema de métricas actualizados en `docs/VERSIONING.md` (§10/§11),
  `AGENTS.md` raíz alineado y Amendment Log de RFC-75 con la entrada de
  materialización del Incremento 2. El propio plan 97 registró su Validation
  Anchor y Checkpoint (dogfooding: `No findings detected / N/A`) y cerró
  docs-only. Sin machinery nueva (checkers/automatización → Incremento 4).
  Cambio docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3).
- **Change Lifecycle de ARgentOS DEV — Unidad D / Incremento 4** (plan 98,
  RFC-75): primera automatización operativa determinista y advisory del Change
  Lifecycle DEV — `tools/check_lifecycle_anchor.py` (C-1: verifica forma y
  completitud de los Validation Anchors v1 en artifacts del régimen nuevo,
  distinguiendo GAP advisory de anomalía, población por señales estructurales
  sin registry y legacy excluido sin backfill) y `tools/check_lifecycle_checkpoint.py`
  (C-2: verifica la relación closure↔estado Git del checkpoint contra el
  anchor aplicable — GC-1 con A1/A2 — usando tree identity como identidad
  material, commit SHA como locator y sin exigir reachability desde `dev`), con
  sus suites deterministas en `tests/` (19 + 21 tests, pytest `tmp_path` y git
  temporales). DEV-only / local invocation: no se incorporan a la batería
  canónica, no hay CI ni pre-commit; sin F-n/C-n/stale/series/métricas,
  registries, entidades ni state machine globales. El propio plan 98 registró
  su Validation Anchor y Checkpoint (dogfooding: planes 96/97 `VALID`, legacy
  `EXCLUDED`, `No findings detected / N/A`) y cerró sin `VERSION` bump ni tag
  (tooling DEV + registros docs-only; RFC-69; ver `docs/VERSIONING.md` §3).
- **Change Lifecycle de ARgentOS DEV — Continuación post-roadmap A–D (C-3 —
  lifecycle lineage checker)** (plan 100, RFC-75): primer checker determinista
  de integridad de lineage findings/corrections/revalidación (LC-1) —
  `tools/check_lifecycle_lineage.py` (C-3) verifica forma, completitud mínima
  y consistencia de los registros del contenedor `## Findings / Correcciones /
  Pending` (`### Findings`/`### Correcciones`) con clasificaciones
  EXCLUDED/BOUNDARY/N/A/VALID/GAP/ANOMALY (GAP advisory ≠ ANOMALY y sin
  autoridad normativa, ADR-16), refs calificadas con namespace del artifact,
  vocabulario de estados, elementos inmutables del finding (CL-8), provenance
  a origen y alcance de revalidación de corrections (CL-6), claims de
  revalidación con soporte declarado en el Validation Anchor/checkpoint del
  propio artifact (CL-7), marcadores de ausencia y contradicciones de
  resolución; read-only, stdlib-only y sin Git en v1; suite
  `tests/test_check_lifecycle_lineage.py` con la matriz T01–T28 y los
  escenarios adversariales permanentes del §20 (40 tests). DEV-only /
  invocación local: sin incorporación a la batería canónica ni a CI; sin F-3
  (ambigüedad → GAP sin tie-break), sin pending/PC-1, sin C-1/C-2. El propio
  plan 100 registró su Validation Anchor y Checkpoint (dogfooding: 96/97
  `EXCLUDED`, 98 `N/A`, 99 `VALID`, legacy `EXCLUDED`, GAP=0, ANOMALY=0) y
  cerró sin `VERSION` bump ni tag (tooling DEV + registros docs-only; RFC-69;
  ver `docs/VERSIONING.md` §3).
- **Capa operacional `.agents/` de ARgentOS DEV** (plan 101, RFC-75): el repo
  fuente materializa `.agents/` en la raíz como interfaz operacional del
  agente DEV para ejecutar el Change Lifecycle — entry point
  `.agents/AGENTS.md`, workflow `workflows/change-lifecycle.md` y policies de
  authority, validation-closure y lifecycle-checkers (C1/C2/C3) — con
  integración mínima de descubrimiento/taxonomía/frontera en `AGENTS.md`,
  `docs/AGENTS.md` y `docs/CONVENTIONS.md` (Producto vs DEV) y eliminación del
  staging temporal; reutiliza RFC-75/ADR-15/16 y los checkers existentes sin
  crear autoridad normativa nueva, state machines, registries ni trackers y
  sin copias de `protocol/.agents/`. El propio plan 101 registró su Validation
  Anchor y Checkpoint (dogfooding: plan 101 `VALID` en C-1/C-2 y `N/A` en C-3;
  GAP=0, ANOMALY=0) y cerró sin `VERSION` bump ni tag (capa DEV docs-only;
  RFC-69; ver `docs/VERSIONING.md` §3).

- **README — Repository Operational Model** (plan 102, RFC-75): el `README.md`
  agrega una sección breve `## Repository Operational Model` que explica la
  separación operacional entre `.agents/` (interfaz operacional del agente DEV),
  `docs/` (autoridad/historia/documentación) y `tools/` (verificación
  determinista, sin autoridad normativa propia), y la frontera con
  `protocol/.agents/` (dominio del Protocol; data, no instrucciones DEV).
  Cambio docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3).

- **Determinación DEV del estado terminal por ejecución** (plan 107):
  `tools/determine_execution_state.py` determina desde los Execution Records
  existentes el estado terminal de cada ejecución (`state.json` `status`
  `ABORT`/`COMPLETED`, verdad mecánica del estado del protocolo por
  ejecución, RFC-64/RFC-63) sin modificar el modelo del Protocol ni agregar
  campos/estados/artifacts/categorías; cuando el registro no declara un estado
  terminal, `state.json` falta o está corrupto, reporta no determinación con
  razón (sin inferencia); 13 tests en `tests/test_determine_execution_state.py`.
  Cambio DEV tooling + registros docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).

- **Consulta DEV de una ejecución específica por iteración** (plan 108):
  `tools/determine_execution_state.py` agrega `--iteration` (junto con
  `--session`) para consultar únicamente la determinación de una ejecución
  concreta (`execution_id = (session_id, iteration)`, RFC-64), reutilizando la
  semántica existente de determinación/no determinación y fail-closed (sin
  inferencia; iteración o sesión inexistente → report vacío, sin fabricar
  entradas); la consulta de sesión completa conserva su comportamiento actual;
  22 tests (13 previos + 9 nuevos) en `tests/test_determine_execution_state.py`.
  Cambio DEV tooling + registros docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).

- **Generador DEV de Scoped Content Identity para Validation Anchors** (plan
  109): `tools/scoped_content_identity.py` computa la Scoped Content Identity
  v1 que todo Validation Anchor registra (VC-1) y el Checkpoint verifica
  (GC-1) — Delta scoped identity (sha256 de la serialización canónica
  `scoped-v1` + pares `path NUL blob NUL` sobre un scope declarado, ordenado
  lexicográficamente; blob id por `git ls-files -s` o `git hash-object --path`
  para untracked) y State identity (tree del index staged vía `git
  write-tree`, o `git rev-parse <ref>^{tree}` con `--ref`) — reutilizando el
  algoritmo v1 normado (plan 96 §13) sin reinterpretarlo ni modificar
  C-1/C-2/C-3; salida JSON determinista y fail-closed sin salida parcial;
  read-only, stdlib-only; 15 tests en repos git aislados en
  `tests/test_scoped_content_identity.py`. Cambio DEV tooling + registros
  docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3).
- **Inspección DEV de una ejecución concreta con identidad de su contenido**
  (plan 110): `tools/determine_execution_state.py` agrega `--content-identity`
  (con `--session` + `--iteration`) a la consulta de una ejecución específica:
  la entrada de la ejecución relaciona su determinación con la Scoped Content
  Identity v1 del contenido de su Execution Record
  (`.project/<session>/<iteration>/`, archivos presentes ordenados), computada
  por composición con el generador existente (`tools/scoped_content_identity.py`,
  Plan 109) — importado sin modificar, sin duplicar el algoritmo v1, sin
  escrituras, sin tracking causal ni relación persistente Execution Record ↔
  proyecto. Fail-closed: scope vacío, root sin repo git u otro error del
  generador → `applicable: false` con razón determinista, sin fabricar
  identidad; sesión/iteración inexistente → report vacío; sin el flag la
  salida es exactamente la actual (18 tests nuevos; 40 en la suite de
  `tests/test_determine_execution_state.py`). Cambio DEV tooling + registros
  docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3).
- **Resumen por sesión y filtro de ejecuciones sin determinación terminal**
  (plan 111): `tools/determine_execution_state.py` agrega `--session-summary`
  (reporte agregado por sesión del estado terminal declarado por cada
  ejecución — `protocol_version` de fuentes existentes,
  `executions`/`determined`/`undetermined` y conteos `terminal_abort`/
  `terminal_completed`, derivados de la semántica existente de
  `determine_iteration`; con o sin `--session`; sesión o `.project/` ausentes
  → `sessions` vacío y `summary` en cero, fail-closed sin fabricar entradas)
  y `--undetermined` (reporte por ejecución restringido a las entradas sin
  determinación con su razón existente `state_json_missing`/
  `state_json_corrupt`/`status_not_terminal`; combinable con `--session`;
  excluyente con `--iteration` y `--session-summary`, error determinista);
  sin flags nuevos la salida es exactamente la actual (regresión cero);
  read-only, determinista, fail-closed, sin inferencia; 24 tests nuevos
  (64 en la suite de `tests/test_determine_execution_state.py`). Cambio DEV
  tooling + registros docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).
- **Brújula de decisiones (Decision-Making Compass)** (plan 113): el
  `AGENTS.md` raíz incorpora la sección `## Decision-Making Compass` —
  claridad sobre crecimiento; separación de responsabilidades
  RFC/Plan/Git/INDEX/Glossary; calidad de decisión sobre volumen documental;
  contención («no change» como resultado válido); calidad de decisión como
  objetivo de evaluación (no demostrado aún) — como principios de juicio
  explícitamente no normativos, sin documento, mecanismo, estado, registry,
  checker ni regla nuevos y sin duplicar autoridades de `docs/`. Cambio
  docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3); sin
  cambios en el payload del Protocol.
- **MVP de deliberación adversarial DEV — convención Working y primer
  dogfooding** (plan 114, —): se agrega la Working Convention no normativa
  `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` (marco
  declarado, pasadas de evaluación atribuidas con compromiso antes de
  revelación, procedencia, reglas de síntesis con desacuerdo preservado,
  vocabulario de veredicto, recomendación advisory y boundary de autoridad) y
  se registra el primer Trial real sobre la decisión pendiente `<PLAN-105>`,
  con evidencia de valor frente al baseline: `MVP IMPLEMENTED — VALUE
  PARTIALLY DEMONSTRATED` (la segunda perspectiva cambió el veredicto de
  `VIABLE` a `NOT_VIABLE`, pero **no** se demostró independencia — mismo
  ejecutor, N=1 — y la pregunta 6 quedó no observable durante el experimento).
  Decisiones humanas del mantenedor registradas como acto separado
  (2026-09-09): `<PLAN-105>` **no** se eleva a ADR en este momento y la
  convención queda `KEEP AS WORKING / CONTINUE DOGFOODING` — permanece
  experimental/Working, **no** promovida a gobernanza, **no** obligatoria y
  **no** incorporada al Change Lifecycle ni al Protocol. Sin código, tool,
  checker, registry, state machine, entidad global ni cambios de plantillas;
  sin cambios en `protocol/.agents/`, `runtime/`, `tools/`, `tests/` ni
  `.agents/`. Cambio docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).
- **Cierre del MVP de deliberación adversarial DEV — dogfood final A/B/C y
  evaluación del closure predicate** (plan 116, —): Tres Trials reales conforme
  a la Working Convention no normativa
  (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`) —
  Escenario A (reconocimiento formal de `<PLAN-114>:F-1`/`F-2`: veredicto
  `NOT_VIABLE` sobre la candidata tal como estaba enunciada; dos perspectivas
  con ejecutores diferenciados — agente principal + subagente de deliberación,
  compromiso antes de revelación, sin afirmación de independencia
  epistemológica); Escenario B (intervención sobre `<PLAN-114>:F-3`: veredicto
  `NOT_VIABLE` y **NO CHANGE** registrado como resultado legítimo); Escenario C
  (release batch de `11.1.0`/`11.2.0`: camino no canónico con confrontación
  acotada §7, nunca antes ejercitada, terminada por criterio de valor; veredicto
  `NOT_VIABLE` por `K-4` — confirmación del usuario para MINOR no registrada) —
  con decisiones humanas registradas como actos separados o pendientes
  escaladas con owner (PC-1), validación (batería canónica + gates C-1/C-2/C-3)
  y evaluación letra por letra del closure predicate
  `A ∧ B ∧ C ∧ D ∧ E ∧ F ∧ G ∧ H ∧ I` (contract / architecture /
  implementation / integration / validation / verification / dogfood /
  documentation / governance); propuesta **`READY TO CLOSE`** para el MVP DEV.
  **Human Checkpoint (2026-09-12):** el mantenedor registró `D-1 = ACCEPT
  CLOSURE OF THE DEV ADVERSARIAL DELIBERATION MVP` y `D-2 = ACCEPT FINAL
  DOGFOOD A/B/C`; con la aceptación y el commit atómico de cierre el predicate I
  pasa a PASS y el MVP DEV queda **`CLOSED` (docs-only, sin release)** — las
  decisiones deliberadas (reconocimiento de F-1/F-2, resolución de F-3, release
  de `11.1.0`/`11.2.0`) permanecen pendientes con owner y no forman parte de
  este cierre. La Working Convention permanece no normativa. La feature
  Protocol-native queda **FUTURE / NOT STARTED / OUT OF SCOPE**. Sin código,
  tool, checker, registry, state machine, entidad global ni cambios de
  plantillas; sin cambios en `protocol/.agents/`, `runtime/`, `tools/`,
  `tests/` ni `.agents/`. Cambio docs-only: sin `VERSION` bump ni tag (ver
  `docs/VERSIONING.md` §3).
- **Adopción de la feature DEV de deliberación adversarial** (plan 117, —): la
  Working Convention no normativa
  (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`) queda
  **adoptada como capability disponible del entorno DEV** —reconocible,
  invocable y reutilizable— con standing `ADOPTED + WORKING + NON-NORMATIVE`,
  sin nuevo lifecycle state, sin promoción a gobernanza, sin obligatoriedad, sin
  gate y sin autoridad. Se materializa la definición final de la feature, el
  contrato de adopción (15 elementos), la frontera de autoridad, los contratos
  de independencia y de valor, las limitaciones declaradas y el predicate
  `JURY_TRIAL_DEV_FEATURE_CLOSED` con C1–C8 (el predicate `JURY_TRIAL_CLOSED`
  del MVP queda únicamente como precondition y no lo sustituye); se cierra el
  `GAP-02` (record home) en la convención con el mínimo texto derivado de
  PC-1/LC-1 —el registro pertenece al artifact que posee la decisión; si está
  cerrado, a un artifact nuevo que lo referencia, fuera de los contenedores de
  lineage— y se registra la decisión humana de cierre como acto separado. DEV
  only y Working/no normativa: sin cambio en el Protocol, sin código, tool,
  checker, registry, state machine, entidad `Trial`, ID global, telemetría,
  métricas, routing operacional, integración al Change Lifecycle, tests ni
  arquitectura nueva; sin cambios en `protocol/.agents/`, `runtime/`, `tools/`,
  `tests/`, `.agents/`, `ROADMAP.md`, `AGENTS.md` ni plantillas. Cambio
  docs-only: sin `VERSION` bump ni tag (ver `docs/VERSIONING.md` §3).

### Fixed


- **Guía de adopción sin `git subtree --prefix=.`** (plan 85): `docs/ADOPTION.md`
  ya no recomienda `git subtree` con prefijo raíz — el `dist` solo trae el
  payload (`.agents/` + `AGENTS.md`) y un `subtree pull` con `--prefix=.`
  genera conflictos modify/delete sobre el proyecto adoptante; se documenta la
  copia del payload desde `dist` vía git o sin git, con manejo de archivos
  eliminados entre versiones. Además, `check_plan_citations.py` exime las citas
  históricas a artefactos eliminados (`PROJECT_ARTIFACTS.md`, plan 84),
  restaurando la batería tras 10.0.0. Cambio docs-only: sin `VERSION` bump ni
  tag (ver `docs/VERSIONING.md` §3).
- **Corrección post-close de F-1 — selección del anchor aplicable en C-2
  (GC-1)** (plan 99, RFC-75): `tools/check_lifecycle_checkpoint.py` selecciona
  ahora el Validation Anchor de la validación cuyo estado validado corresponde
  al estado de cierre (tree del commit de cierre final o literal declarado;
  Tier 1 por tree identity; Tier 2 por revalidación declarada única sobre el
  cierre, patrón del corpus 96–98), eliminando la selección por recencia
  ("latest A2 wins") y la pertenencia genérica del tree entre los commits de
  cierre; GAP/ANOMALY, A1/A2 (Decisión B), tree identity ≠ SHA y
  no-reachability se preservan y el reporte identifica el anchor aplicable;
  regresiones F-1 permanentes en `tests/test_check_lifecycle_checkpoint.py`
  (Casos A/B/C adversariales y escenarios T1–T12). DEV-only: sin `VERSION`
  bump ni tag (RFC-69; ver `docs/VERSIONING.md` §3).

- **Alineación documental y operacional post-Plan-78** (plan 104): el root
  `AGENTS.md` pasa a puntero/resumen de la batería canónica (definición única
  en `docs/VERSIONING.md` §4.1) con el layout de `docs/` corregido y
  diferenciado (`docs/rfc/`, `docs/adr/`, `docs/plans/`); `.agents/AGENTS.md`
  permanece como entrypoint operacional (alineación factual mínima del
  `## Verification battery`; sin `INDEX.md`); `README.md` sin batería parcial
  duplicada; `docs/VERSIONING.md` §9 actualizado al estado real (2026-09-05:
  master/dist `10.3.0`, dev `11.0.0` pre-release sin promover) y §4.1 con
  ownership único; `docs/CONVENTIONS.md` con rangos actualizados (RFCs hasta
  RFC-75; ADRs hasta ADR-16); `docs/MIGRATION.md` con el link `../CHANGELOG.md`
  corregido; `CHANGELOG.md` con `[Unreleased]` en la posición superior; los
  modelos históricos de arquitectura preservados con banner de snapshot.
  Cambio docs-only: sin `VERSION` bump ni tag (RFC-69; ver
  `docs/VERSIONING.md` §3); sin promoción de `11.0.0`.

(los cambios docs-only se registran aquí bajo `[Unreleased]`; ver
`docs/VERSIONING.md` §3)

---

## [12.3.0] — 2026-10-20

### Added

- **Verificador de equivalencia del bloque canónico** (`PC-3`, RFC-84 / Plan 170): `tools/check_invariants_equivalence.py` compara la identidad sha256 del bloque `canonical-invariants-v1` en `docs/INVARIANTS.md` y `protocol/.agents/standards/INVARIANTS.md`, valida que el catálogo tenga 12 invariantes y 3 properties con identificadores únicos, y falla ante cualquier drift material. Se incorpora a la batería canónica de `docs/VERSIONING.md` §4.1.

### Changed

- **`INV-07` pasa de `NONE` a `ENFORCED:session-hook`** (`E1-G1`): el hook de sesión niega escribir dentro de `PAYLOAD_ROOT` (`PROTOCOL_BOUNDARIES: Protocol immutability`); el resto del espacio ARgentOS —estado de sesión, `features.toml` y backups— sigue escribible. Límite: exige hooks instalados; sin ellos rige el modo declarativo. El comportamiento anterior, que permitía escribir el payload y estaba fijado por un test, contradecía la norma: se corrigió el código y el test que lo fijaba.
- **`INV-08` cierra la ventana de crash** (`G-09`): la intención se registra en el journal **antes** de que el archivo exista, de modo que ninguna escritura puede quedar fuera del rollback; y una operación con journal abierto ya no responde `NOOP` — devuelve `recovery-pending` y exige `recover`. Recuento de enforcement del catálogo: **7/15 `ENFORCED`**, 2/15 `VALIDATED`, 6/15 `NONE`.

## [12.2.0] — 2026-10-20

### Added

- **Catálogo canónico de invariantes y properties transversales DEV/Protocol** (Plan 170, RFC-84 `Accepted`; Clase A de RFC-56): `protocol/.agents/standards/INVARIANTS.md` incorpora el **bloque canónico** de 15 entradas —12 invariantes (`INV-01`…`INV-12`) y 3 properties (`PROP-01`…`PROP-03`)— idéntico byte a byte a la representación de desarrollo, delimitado por los marcadores `canonical-invariants-v1`. Cada entrada declara `SCOPE`, `OUT_OF_SCOPE`, `ENFORCEMENT_STATUS` y `LIMIT`. El catálogo **no declara garantías implementadas** y no introduce ningún mecanismo de enforcement: recuento declarado 6/15 `ENFORCED`, 2/15 `VALIDATED`, 7/15 `NONE`, y ninguna entrada mecánicamente enforced para el protocolo distribuido.

### Changed

- **Dos excepciones aprobadas a la política de single-source** (Plan 170, RFC-84): `standards/runtime/PROTOCOL_BOUNDARIES.md` registra la segunda excepción —acotada al bloque canónico de las 15 entradas, con equivalencia byte a byte, actualización coordinada y sin autoridad semántica duplicada— y la frase que declaraba a `ANTI_CIRCUMVENTION` como única duplicación sancionada pasa a reconocer las dos.

### Modelo conceptual

- **RFC-84 `Accepted`** (2026-10-20, autorización explícita del mantenedor): autoriza la excepción cross-domain para el catálogo canónico de 12 invariantes y 3 properties. No modifica ningún contrato vigente ni introduce motor de enforcement; los doce gaps de enforcement (`E1-G1`…`E1-G5`, `G-03`…`G-09`) permanecen abiertos y requieren Changes propios.

## [12.1.0] — 2026-10-14

> **Absorción de `12.0.1`** (plan 168): el Plan 156 asignó `12.0.1` como PATCH documental del payload y
> quedó `Closed` con `Released = FALSE`; ese número **nunca se publicó** (`master` permaneció en `12.0.0`).
> Esta release **absorbe** ese número: su ítem de payload se transporta aquí, y el número pasa a `12.1.0`
> porque el contenido publicado incluye **adiciones compatibles** del Protocol (`docs/VERSIONING.md` §3:
> MINOR). La trazabilidad del Plan 156 se preserva en este mismo ítem; su artefacto cerrado no se edita.

### Added

- **Objective multi-Change y procedencia declarada del actor en el payload** (plan 166, RFC-83; Clase A de RFC-56 — RFC-83 `Accepted` + Plan 166 `Executed`/`Closed` como autorización de la modificación de `protocol/.agents/`): dos extensiones **aditivas** de la superficie publicada del Protocol. `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` incorpora `## Objective relation (multi-Change)`: un **Objective explícito** —declarado por el adoptante, **nunca inferido**— asocia **uno o más Changes**; cada Change conserva su identidad y su gobernanza en ese artefacto (RFC-76 intacta); cada Change recibe una `Evaluation` (`satisfied` / `not satisfied`) con `evidence_ref`; `not satisfied` deja el Objective **`open`** y habilita el siguiente Change, `satisfied` lo lleva a **`COMPLETED`**; **sin** segunda Change State Machine, sin lifecycle paralelo y sin replicar el runtime DEV. `protocol/.agents/contracts/HARNESS_REPORT.md` incorpora `## Declared actor provenance` (`actor`, `harness`, `mechanism`, `declared_by`), **declarada y no verificada**, conservando `self-reported` y `enforcement = "informational"`, sin afirmar autenticidad ni verificación independiente y sin provider/model/SDK/CLI (compatible con `ID-1`). El cierre de `F-C` (plan 165) no exige demostración con un harness externo autenticado; esa decisión es independiente de esta release. Verificación: `check_protocol_invariants` PASS (216 archivos / 10476 referencias) · `check_taxonomy_coherence` OK · `check_plan_structure` PASS · `check_plan_citations` 26 (baseline histórico, sin regresión). `VERSION` pasa a `12.1.0` y se sincroniza el ancla semántica del runtime (`runtime/toolcalls/canonical.py`), conforme al «modelo por plan» de `docs/VERSIONING.md` §3.

### Fixed

- **Reconciliación documental del payload con el layout canónico `.argentos/`** (plan 156, RFC-82; Clase B —  RFC-82 `Accepted` + Plan 156 como autorización de la modificación de `protocol/.agents/`): se corrige la **prosa
  descriptiva** del payload que la release `12.0.0` (plan 154, RFC-81) volvió inexacta. No cambia ningún contrato,
  gate, estado, transición, skill ni capacidad: 0 diff en `orchestrators/`, `contracts/`, `delegation/`, `roles/`,
  `skills/` y en los scripts del harness. Correcciones: (a) `protocol/.agents/INDEX.md` declara el bootstrap
  normativo real (`.argentos/.agents/INDEX.md`) y al `AGENTS.md` de la raíz como **adapter no normativo**, en lugar
  de nombrarlo entry point; (b) `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` describe la frontera de
  artefactos bajo el layout canónico — el payload vive en `PAYLOAD_ROOT` (`.argentos/.agents/`), y fuera de él pero
  dentro de `ARGENTOS_ROOT` viven la configuración activa (`features.toml`), el estado local (`.project/`) y los
  backups (`.backup/`), con `AGENTS.md` como único artefacto en la raíz — en lugar de afirmar que el único artefacto
  fuera de `.agents/` y `.project/` era `AGENTS.md`; la inmutabilidad del payload no se debilita; (c)
  `protocol/.agents/harness/INDEX.md` y `protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md` enumeran los
  **ocho** módulos stdlib que el payload distribuye — los cuatro que aplican durante una sesión (`hook_gate.py`,
  `runner_state.py`, `health_check.py`, `gate_validator.py`) más los cuatro que hacen materializable el layout
  (`roots.py`, `lifecycle.py`, `lifecycle_contract.py`, `lifecycle_staging.py`) — en lugar de declarar «exactly
  four»; la política de stdlib pura queda intacta; y (d) `protocol/.agents/harness/INDEX.md` distingue lo que
  **transporta** `dist` (el payload `.agents/` + `AGENTS.md`) de lo que el adoptante **materializa**
  (`.argentos/{features.toml,.agents/,.project/,.backup/}` + adapter en la raíz), en lugar de presentar el payload
  como si fuera el layout. Del lado DEV se actualiza `docs/source-layout.md`: su lista de «prosa que describe el
  layout adoptado (no tocar)» perdía su premisa (asumía que `dist` publicaba `AGENTS.md` como entry, cuando con
  RFC-81 es un adapter no normativo); se registra la corrección autorizada por RFC-82 y se preservan la guarda de
  links del entry file, los links rotos intencionales y las citas históricas de `docs/plans/`. `VERSION` pasa de
  `12.0.0` a `12.0.1` (PATCH por `docs/VERSIONING.md` §3: fixes documentales) y se sincroniza el ancla semántica del
  runtime (`runtime/toolcalls/canonical.py`). La promoción, el tag y la regeneración de `dist` no fueron
  ejecutados por ese plan: su número `12.0.1` quedó sin publicar y fue **absorbido** por la release
  `12.1.0` (plan 168).

> Nota: el tag git `12.1.0` se crea como entregable de esta release al promover `dev` → `master` (plan 168).

## [12.0.0] — 2026-10-11

### Added

- **Lifecycle de adopción ARgentOS — `install`/`update`/`uninstall`/`doctor`** (plan 154, RFC-81; Clase A —
RFC-81 `Accepted` + Plan 154 como autorización): se implementa el ciclo de vida de una instalación en un
proyecto adoptante dentro de la familia distribuida existente `protocol/.agents/harness/` (D1), con
`lifecycle.py` (CLI), `lifecycle_contract.py` (schema de `install.json`, seguridad de rutas, seis estados de
ownership, escritura atómica + snapshot) y `lifecycle_staging.py` (staging por ref de git fijada + fallback
copia local). Ownership por **procedencia** (`origin`) **+ estado verificado**: la huella detecta divergencia
y **no** acredita autoría. El adapter `AGENTS.md` se genera solo si no existe (opt-in `--replace-agents-md` con
backup verificable y comprobación de no-cambio); `.gitignore` **no** se modifica. `uninstall` preserva por
defecto `.project/`, `.backup/` y la configuración activa; `--purge` se limita a artefactos
`origin==installed ∧ state==present`. Journal durable + backups + rollback que **nunca** sobrescribe cambios
posteriores del adoptante (`recovery pending`); lock de exclusión mutua, revalidación de `PROJECT_ROOT` antes
de cada escritura, rechazo de escapes por symlink y estados de salida deterministas
(success/no-op/conflict/recovery-pending).

### Changed

- **Layout canónico del adoptante (MAJOR)** — `docs/VERSIONING.md` §3: el payload se materializa en
`<project-root>/.argentos/` (`features.toml`, `.agents/`, `.project/install.json`, `.backup/`) y la raíz solo
conserva el adapter no normativo `AGENTS.md` que apunta a `.argentos/.agents/INDEX.md`; **no** existe
`.argentos/AGENTS.md`. Es incompatible con el layout histórico (`.agents/` + `AGENTS.md` en la raíz) y
requiere migración; ver `docs/MIGRATION.md` §19 (detección ≠ autorización; preservación por defecto).
`protocol/.agents/VERSION` pasa de `11.7.1` a `12.0.0`. Documentación alineada en `docs/ADOPTION.md`,
`docs/MIGRATION.md` y `README.md`. Verificación: batería canónica en verde; `pytest
protocol/.agents/harness/tests/` 185 passed; `pytest tests/` 1266 passed + 1 skipped; GATE 3 36/36 y GATE 4
17/17 documentados en el Plan 154.

> Nota: el tag git `12.0.0` se crea como entregable del release al promover `dev` → `master`.

## [11.7.1] — 2026-10-08

### Changed

- **Release de gobernanza 11.7.1 — promoción de `master` al estado verificado de `dev`** (plan 151,
  plan 152, plan 153; excepción de promoción de `docs/VERSIONING.md` §3, autorizada por el mantenedor):
  nivelación de `master` con el estado verificado de `dev`, que publica los artefactos de gobernanza del
  cierre de autoridad del modelo de autonomía (Planes 151–153) y el cierre residual del Plan 151.
  **El contenido del protocolo no cambia**: 0 diff bajo `protocol/` salvo `protocol/.agents/VERSION`
  —metadata de la release misma—, que pasa de `11.7.0` a `11.7.1` (sucesora PATCH de la última versión
  publicada en `master`). Sin RFC nueva, sin ADR nuevo, sin reapertura de planes cerrados y sin cambio
  de contenido de payload.

## [11.7.0] — 2026-10-06

### Added

- **Memory System** (plan 150, RFC-80): nuevo estándar
  `protocol/.agents/standards/context/MEMORY_SYSTEM.md` que define el Memory System
  project-scoped — cinco capas (Episodic/Semantic/Synthesis/Operational/Archive),
  entidades (Session/Observation/Evidence/Claim/Decision/Lesson), lifecycle y estado
  epistémico separados, applicability, provenance, relaciones, contradicción y
  supersession explícitas, consolidation con semantic non-regression, proyección
  operacional reconstruible no-autoritativa, retrieval acotado y archive (≠ delete).
  Adición compatible (MINOR); no modifica los estándares de conocimiento existentes
  (`KNOWLEDGE_LIFECYCLE.md`, `KNOWLEDGE_CURATION.md`).

## [11.6.2] — 2026-09-22

### Fixed

- **Integridad post-release y compatibilidad de CI** (plan 147, vía plan; DEV-only sobre
  `tools/`, `tests/`, `runtime/toolcalls/`, `.github/workflows/`, `.agents/policies/` y la
  documentación corriente, sin efecto en `protocol/.agents/`, `protocol/_AGENTS.md` ni
  `dist`, por lo que RFC-56 no aplica): corrige, en la causa y no en el síntoma, las cuatro
  causas raíz que dejaron rojo el job `check-protocol` después de la release `11.6.1` (runs
  `35689196717` en `dev`: 4 failed / 1143 passed, y `35688773540` en `master`: 5 failed /
  1142 passed). **C-1:** el árbol publicado por el tag `11.6.1` (`master` = `8dbd92e`, merge
  de `dc21458` y `54171d8`) contiene la revisión **previa** del Plan 146 —`7a9d393`, que
  transcribe los literales de identidad, no es ancestro de `master`—, y su
  `## Validation anchor` difiere los literales al checkpoint por la convención
  anti-auto-referencia del corpus; R-C1-4 traducía esa **ausencia declarada** en `ANOMALY`
  («invalid State identity format», «invalid Delta scoped identity format»). Ahora distingue
  ausencia declarada (`GAP`, advisory) de valor presente e inválido (`ANOMALY`), sin aceptar
  ningún literal malformado (falsificación explícita). **C-2 y dogfoods SAE:** C-2 resuelve
  cada tree id declarado con `git rev-parse --verify <sha>^{tree}` y los dogfoods leen los
  commits del Plan 138 con `git log --grep`; con el checkout superficial por defecto
  (`fetch-depth: 1`) C-2 degradaba a `GAP=27` y los dogfoods reportaban «the plan-138 commits
  are not in history». Se da **historia completa** al job (`actions/checkout@v4` con
  `fetch-depth: 0`) en lugar de debilitar los checkers. **Resolución de segmentos:** el guard
  de contención validaba con la clase de path nativa, de modo que en POSIX
  `C:/Windows/x.md` no es absoluto ni tiene componente `..` y no se rechazaba —el test
  `test_path_escaping_the_payload_is_rejected` fallaba sólo en el runner Linux—; ahora valida
  con semántica POSIX (`PurePosixPath`) en toda plataforma y rechaza además el separador
  foráneo `\` y el identificador calificado por unidad (`C:`, `C:/`, `C:x`). Sin reescribir
  ningún plan cerrado, sin tocar `master`, los tags `11.3.0`–`11.6.1` ni `dist`. Se publica
  como **release de gobernanza** `11.6.2` del plan 148: es una promoción de release, no un
  cambio del protocolo, de modo que el payload transportado sigue siendo `11.6.1`
  (`docs/VERSIONING.md` §3, viñeta «Releases de gobernanza»).

## [11.6.1] — 2026-09-21

### Fixed

- **Registro de taxonomía del contrato `CHANGE_GOVERNANCE.md`** (plan 143, vía
  plan; `Clase B` de RFC-56 — adición documental compatible, sin cambio de
  significado ni de compatibilidad): la regla 11 de
  `protocol/.agents/harness/policies/H13-protocol-taxonomy.md` exige que todo
  archivo de contrato tenga una entidad `kind: contract` cuyos `domain`,
  `artifact`, `lifecycle`, `produced_by` y `consumed_by` coincidan con su bloque
  de metadata, en las dos direcciones. `CHANGE_GOVERNANCE.md` sólo estaba
  registrado en la sección `# Artifacts` (`kind: artifact`, con puntero
  `contract:`) desde el plan 115, de modo que el archivo declaraba
  `kind: contract` sin entidad contractual que lo respaldara: la entidad
  `contract:CHANGE_GOVERNANCE.md` se registra con los mismos valores que el
  contrato y su entidad de artefacto ya declaraban. El hueco era invisible para
  la batería porque ninguna verificación mecánica cubría la regla 11; la
  cobertura se agrega en el mismo Change a `tools/check_taxonomy_coherence.py`
  (checker DEV, no distribuido). Sin cambio de contenido en el contrato ni en
  ninguna otra parte del payload.

## [11.6.0] — 2026-09-21

### Added

- **Residuales normativos del payload** (plan 142, RFC-79): se materializan las
  siete decisiones con las que la RFC-79 cierra los residuos normativos
  registrados por `ROADMAP.md` y por la bitácora de fricciones del plan 19.
  **`F-14` — marcado legacy:** `status` de la entrada de KB admite `legacy`
  (entrada heredada sin campos de procedencia y no revalidada: se trata como
  confianza baja hasta que un worker la revalide o la invalide) y el manifest
  gana la lista `[entries] legacy`, con la misma forma que `active` y `stale`; las
  instrucciones de `discovery_orchestrator.md` e `init_worker.md` se corrigen para
  que la orden sea expresable —el estado por entrada vive en la entrada y el
  manifest lo indexa— y se retira la mención a un campo `confidence` que el
  manifest no tiene ni necesita. **`F-17` — procedencia de ausencias y hechos de
  árbol:** `source_files` admite el valor reservado `"project_scan"` (el hecho se
  estableció escaneando el árbol del proyecto), válido sólo para una ausencia o un
  hecho de árbol y nunca en una entrada de entorno, del mismo modo que
  `"system_probe"` sólo es válido para entradas de entorno; el ítem 5 de D01
  amplía su excepción y los contratos `CONTAINERS.md`, `DATABASE.md` y
  `FILE_MAP.md` fijan el valor para esa clase. **`F-16` — `project_shape`
  documental:** el enum gana `documentation` (producto documental, de estándares o
  de datos de protocolo, sin librería, CLI, servicio ni aplicación propias; el
  tooling interno no cambia la forma) con su variante en `API_SURFACE.md`, de modo
  que un repositorio determinable deja de clasificar `unknown`. **`B-8` residual —
  riesgo de sesión:** el catálogo de `METRICS.md` gana el evento de sesión
  `session_risk` (`risk`, `mitigations`; valor declarado hoy
  `single_instance_delegation`) y `PROTOCOL_METRICS.md` registra su clase de
  verifiabilidad, de modo que la mitigación (c) del modo single-instance de
  `orchestrator.md` deja de apuntar a un contrato sin lugar donde registrarla.
  **`F-18` — delimitador:** el front matter de una entrada de KB queda declarado
  como delimitado por `+++`, que es lo que la práctica y el checker ya usaban.
  **Frontera composición ↔ materialización:** el criterio 1 de
  `COMPOSITION_OPTIMIZATION.md` declara que gobierna la composición conceptual del
  payload y **no** el orden de la materialización provider-bound, cuya región
  estable primero y sufijo dinámico después es una capa distinta
  (`protocol/.agents/standards/context/CONTEXT.md:Identity and ordering`); el runtime y el contrato de orden quedan
  intactos. **Metadata contractual:** `KB_DISCOVERY_ENTRY.md` e
  `INTER_WORKER_MESSAGE.md` alinean su `produced_by`/`consumed_by` con sus
  entidades de `PROTOCOL_TAXONOMY.md` (H13 regla 11), resolviendo
  `<PLAN-126>:PC-1` con la lectura contractual de `tags.kind`. Clase A en seis
  decisiones y Clase B en dos; cambio **aditivo**: ningún valor admitido se
  retira y ninguna sección desaparece. Versión 11.6.0 (MINOR).

### Changed

- `tools/check_discovery_output.py` (plan 142, RFC-79): el checker DEV de D01
  implementa las decisiones 2 y 3. Acepta `"project_scan"` como procedencia
  resuelta —y lo reporta `ANOMALY` en la entrada de entorno, que es la clase de
  `"system_probe"`—, admite el shape `documentation`, y **deja de tratar un
  `source_files` no resoluble y no reservado como frontera declarada**: con el
  contrato capaz de expresar la clase de ausencia y hecho de árbol, ese caso es
  una violación del ítem 5 de D01 y se reporta `ANOMALY` en lugar de `GAP`. La
  ausencia de evidencia sigue siendo `GAP` advisory y no cambia el exit code. Las
  suites `tests/test_check_discovery_output.py` y
  `tests/test_discovery_output_dogfood.py` cubren los casos positivos, negativos y
  de frontera nuevos, y el dogfood verifica los valores declarados en el payload
  real.

## [11.5.0] — 2026-09-14

### Added

- **Stable prefix provider-bound** (plan 121, RFC-78): el Protocol define el
  **stable prefix** de la materialización dirigida al provider — la porción
  inicial de la representación canónica que contiene el Contexto Estable
  resuelto y ningún contenido dinámico. Se incorpora a
  `standards/context/CONTEXT.md` («Stable prefix (provider-bound
  materialization)»): la **regla de pertenencia** (Stable Context ∧ scope de la
  delegación ∧ consumido demostrablemente por el Worker o resoluble
  determinísticamente del Delegation Payload), el **alcance Core + Worker** del
  prefijo, el paso **`protocol-bootstrap` declarado y vacío** en el scope del
  Worker (la secuencia de bootstrap carga rol de sistema, state machine y rol
  del orquestador en el **Orchestrator**; el contrato de ejecución del Worker no
  dirige al Worker a leer ningún documento de bootstrap), la exclusión
  **deliberada y diferida** del segmento **Project/KB** (su freshness/lifecycle
  introduce una dinámica de invalidación distinta), la frontera con las policies
  de composición (Compression y Optimization gobiernan la forma del payload del
  protocolo; el prefijo es la representación que el runtime produce a partir de
  él) y las no-equivalencias (Stable Context ≠ Stable Prefix; Stable Prefix ≠
  Segment ≠ identity ≠ persistence ≠ autorización de reuso; resolver contenido ≠
  cache hit del provider). Un elemento estable irresoluble se reporta como
  desviación y el runtime **nunca inventa su contenido**. El orden pertenece a la
  materialización (`ordering_contract_version`), no a la identidad semántica; no
  se introduce identity primitive nueva, no se modifica
  `SemanticContextIdentity` y el prefijo no altera los límites semánticos del
  Context Budget. Cambio aditivo y compatible; el Protocol **no** implementa
  prompt cache del provider ni declara ahorro alguno.

## [11.4.0] — 2026-09-14

### Added

- **Capacidad Protocol-native `adversarial-deliberation`** (plan 120, RFC-77):
  incorpora al Protocol la deliberación adversarial como una **capacidad**, nunca
  como autoridad. Compuesta por: la Skill
  `protocol/.agents/skills/adversarial-deliberation/SKILL.md` (una pasada de
  evaluación atribuida, con postura declarada, material recibido, compromiso
  previo a la revelación, y las reglas de síntesis, desacuerdo y frontera de
  autoridad); el contrato de artefacto
  `protocol/.agents/contracts/DELIBERATION_REPORT.md` (secciones obligatorias,
  vocabulario cerrado, invariantes `DEL-001`…`DEL-012`, sesión-scoped e
  `informational`); el punto de decisión `D7 — Invocación de deliberación
  adversarial` en `protocol/.agents/standards/orchestration/DECISIONS.md`; y la
  subsección §4.4 *Deliberation Invocation* del rol del Orchestrator (invocación
  con motivo registrado, construcción de Execution Contexts distintos por pasada,
  exigencia de compromiso previo a la revelación, comparación por criterio,
  preservación del desacuerdo, síntesis, veredicto y recomendación advisory
  opcional, e interpretación). Registros: entidades `kind: artifact` y
  `kind: contract` en `PROTOCOL_TAXONOMY.md`, declaración del artefacto en
  `PROTOCOL_BOUNDARIES.md`, y fila de inventario en `skills/INDEX.md` (sin fila en
  la tabla de activación: la candidatura es por juicio). Suite de verificación
  `tests/test_adversarial_deliberation.py` (contrato, skill, orquestación,
  autoridad, contexto y negativos). Cambio MINOR aditivo: sin entidad, `kind`,
  rol, perfil, fase, estado, lifecycle state, authority class, registry, ID
  global, primitive de identidad, feature flag, gate, clasificador automático,
  voting, confrontación, Prompt Cache ni rediseño del Change Lifecycle nuevos. La
  independencia es una **condición de procedencia declarada**
  (`ejecutores: mismo | distinto`), nunca una garantía epistemológica; el
  resultado es `attestation`/recomendación advisory y no satisface ningún ítem
  `[gate]`. `MVP CLOSED != RELEASE AUTHORIZED`. El tag anotado `11.4.0` se
  crea como entregable del release en la promoción del Plan 146.

## [11.3.0] — 2026-09-13

### Changed

- **Change Governance Artifact — alcance del MVP: append, current y
  governance_position DEFERRED** (plan 119, RFC-76; decisión H-3, OPTION B): el
  contrato declara explícitamente qué está implementado en el MVP
  (materialización del artifact, identidad RFC-71, persistencia, estructura de las
  colecciones como historia acumulada, registro de decisiones/autorizaciones/cierre
  provisto por el llamador, reconstrucción por recomputación de identidad y
  lectura del archivo) y qué queda **DEFERRED** (la operación de **append**, la
  derivación de **current** y la derivación de **governance_position**), con el
  invariante nuevo `CGA-010`. "Append-only" pasa a describir la **forma** del
  artifact y no una operación disponible: la acumulación posterior de historia se
  realiza por **re-materialización completa con historia acumulada**, que **no es
  append**, con la consecuencia declarada de que los estados intermedios del
  artifact no se preservan. Sin runtime, campos, endpoints, eventos, estados ni
  métodos nuevos; `runtime/toolcalls/change_governance.py` sin cambios. Cambio
  MINOR (11.2.0 → 11.3.0); el tag anotado `11.3.0` se crea como entregable del
  release en la promoción del Plan 146.

## [11.2.0] — 2026-09-12

### Changed

- **Change Governance Artifact — namespace, canonical representation y
  ubicación** (plan 115, RFC-76; decisiones D-01/D-02/D-03): resuelve los
  elementos diferidos de identidad y persistencia. `namespace` =
  `project_identity`; canonical representation por cuatro líneas ordenadas
  (UTF-8, SHA-256; `declaration` con trim, `target` verbatim); ubicación física
  `.project/changes/<change_identity>.md` (content-addressed, sin registry).
  Permanecen DEFERRED: closure predicate, reflexive bootstrap, Task↔Change
  cardinality, GC semantics.

## [11.1.0] — 2026-09-12

### Added

- **Change Governance Artifact** (plan 115, RFC-76): nuevo contrato
  `CHANGE_GOVERNANCE.md` — representación durable Protocol-native del governance
  state de un Change del payload. Identidad derivada vía `SegmentIdentity`
  (RFC-71); identity inputs `{target, declaration, protocol_version, namespace}`
  inmutables; governance collections append-only (`decisions[]`,
  `authorizations[]`, `closure_decisions[]`) con current derivado; Change
  authorization semánticamente distinta de RFC-66; cierre v1 por decisión humana
  explícita; `declaration` frozen con revisión de propuesta sin cambio de
  identidad; supersession por Artifact Lifecycle RFC-63; relación con executions
  por referencia; retrieval content-addressed con locator = Change Identity (sin
  registry). Sin state machine, rol, registry ni identity service nuevos.

### Modelo conceptual

- **RFC-76** (plan 115): `Accepted` — modelo del Change Governance Artifact
  (Protocol Change Lifecycle nativo, sin importar maquinaria DEV).

## [11.0.1] — 2026-09-06

### Fixed

- **Alcance determinista del gate S00 sobre el health checklist** (plan 112):
  el ítem 2 de `protocol/.agents/orchestrators/system/harness/policies/S00-system-ready.md`
  (`## Checklist`) declara explícitamente que el alcance PASS del gate es el de
  la `## Decision` vigente de
  `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md` (ítems 1–6, 8–9 y
  11–13; ítem 10 sólo con el flag `knowledge_base` habilitado; ítem 7
  warning-only), citándola como fuente de verdad sin duplicar el checklist.
  Clase B (RFC-56): mejora documental compatible; sin cambio de significado
  del health checklist ni del modelo del Protocol.

---

## [11.0.0] — 2026-09-04

### Added

- **Modelo de registro de ejecución — identidad y event keys** (plan 78,
  RFC-64): identidad de ejecución por composición
  (`execution_id = (session_id, iteration)`) sin UUIDs nuevos; roles disjuntos
  de `state.json`, `HARNESS_REPORT.md`, `SESSION_LOG.md` y `METRICS.md`;
  correlación de gates por `(execution_id, trigger)`, de métricas por
  `(execution_id, seq)` y de delegaciones por `(execution_id, phase,
  attempt#)`; sección "Execution records" en `.agents/harness/INDEX.md`.
- **METRICS con `seq`/`iteration`/`clock`** (plan 78, RFC-64): todo evento
  METRIC lleva `seq` (estrictamente creciente por sesión), `timestamp` y
  `clock`; los eventos por ejecución llevan `iteration`, incluidos
  `reuse_event` y `provider_cache_event` del catálogo 1.2.0 (10.3.0);
  `delegation` puede declarar `context_budget` y `attempt`; pairing
  obligatorio delegación ↔ evento `context_budget` (OBS-001).

### Changed

- **Alcance de `state.json` y `gate_ts` canónico** (plan 78, RFC-64):
  `state.json` registra gates de transición H00–H07/H11 + status terminal
  únicamente; `runner_state.py` rechaza triggers no transicionales y
  normaliza los timestamps a UTC con sufijo `Z`; `detect_bypass` devuelve un
  flag de confiabilidad y avisa cuando el `gate_ts` no es UTC-normalizado.
- **ENTRY con `iteration`/`clock` obligatorios** (plan 78, RFC-64):
  `HARNESS_REPORT.md` declara `timestamp` como `event_ts` del trail y
  `timestamp_divergence.cause` para divergencias con el `gate_ts` (TR-002,
  tolerancia 60 s); `SESSION_LOG.md` registra `Execution` y el marcador
  `Clock` cuando el heading no es UTC-normalizado.
- **`schema_version` 2.0.0** (plan 78, RFC-64): los contratos
  `HARNESS_REPORT.md`, `METRICS.md` y `SESSION_LOG.md` pasan a
  `schema_version` 2.0.0 (obligaciones nuevas para sesiones nuevas).
- **Reconciliación dev** (plan 78, RFC-64): `--audit` correlaciona por
  `(iteration, trigger)` para sesiones `>= 11.0.0` y compara timestamps con
  tolerancia de 60 s; las trazas previas sin `iteration` mantienen la
  correlación por `trigger` (RFC-46); `check_session_artifacts.py` aplica el
  modelo de registro solo a sesiones `>= 11.0.0`.
- **Medidor de budget** (plan 78, RFC-64): `measure_context_budget.py` acepta
  `--phase`/`--iteration` opcionales en el reporte JSON.

### Removed

- **Registro de gates no transicionales en `state.json`** (plan 78, RFC-64):
  D*/H09/H10/H15/S00/REVIEW dejan de ser registrables en `state.json`
  (solo `HARNESS_REPORT.md`); las trazas históricas no se reescriben.

### Modelo conceptual

- **RFC-64 implementada** (plan 78): el Execution Record Model pasa de modelo
  aceptado (plan 103) a materialización en `11.0.0`, preservando las tres
  lecturas Accepted (`clock` implementa `agent_clock` sin renombrar; `seq`
  estrictamente monótono por sesión; TR-002 con tolerancia de 60 s y
  `timestamp_divergence.cause`).

## [10.3.0] — 2026-08-31

### Added

- **Observabilidad y economía del cache — eventos de reuse/provider** (plan 91,
  RFC-74): el contrato `METRICS.md` pasa a `schema_version` 1.2.0 con los tipos
  de evento `reuse_event` (vocabulario lookup/eligibility/reuse/lifecycle por
  capa; hit/miss nunca implica validez semántica) y `provider_cache_event`
  (estado del cache del provider reportado por el adapter; sin pricing ni costo
  monetario — dimensión `Unavailable`); `PROTOCOL_METRICS.md` agrega el
  catálogo `Reuse and cache` con clases de evidencia
  (Observed/Estimated/Derived/Unavailable), métricas por capa y la sección de
  economía con los invariantes I-ECO-001…I-ECO-006 sin umbrales; el agregador
  dev `tools/aggregate_metrics.py` procesa los eventos nuevos con agregación
  layer-specific y sin doble conteo, y deriva las oportunidades de Discovery
  reuse (clase Derived) desde `.last_discovery` + manifest; los productores del
  runtime (planes 89/90) quedan expuestos como metadata/estado; el registro de
  los eventos en `METRICS.md` es responsabilidad del Orchestrator/host (seam
  arquitectónico documentado; sin writer de referencia en este repositorio).
  MINOR: adiciones compatibles (los eventos desconocidos siguen ignorados por
  agregadores viejos); sin thresholds, sin pricing, sin telemetry backend, sin
  cambios en Discovery ni en state machines.

### Modelo conceptual

- **RFC-74 implementada** (plan 91): la RFC-74 pasa de modelo aceptado
  (plan 93) a materialización parcial de la medición/economía del cache
  (eventos de reuse/cache, catálogo y agregador), versión 10.3.0.

## [10.2.0] — 2026-08-31

### Added

- **Persistence semántica de proyecto — Project Segment derivado** (plan 90,
  RFC-73): el runtime de referencia deriva el Project Segment de RFC-71 sobre
  la KB de discovery existente (namespace = `ProjectIdentity` desde
  `PROJECT_REGISTRY.project_id`, sin identidad nueva ni fallback path-derived),
  con `SegmentContentIdentity`/`SegmentIdentity(project)`, reuse eligibility
  (`FRESH`/`STALE`/`UNKNOWN`; stale ≠ invalid; hashes de discovery ≠ content
  identity) y store derivado `.project/knowledge/project_segment.json`
  (filesystem, escritura atómica, rebuildable, nunca autoritativo), más la
  regla operativa aditiva en `PROTOCOL_BOUNDARIES.md`. MINOR: adiciones
  compatibles; sin cambios en Discovery, state machines ni RFC-72/74.

### Modelo conceptual

- **RFC-73 implementada** (plan 90): la RFC-73 pasa de modelo formal a
  materialización parcial de la persistence de proyecto (Project Segment
  derivado + store) en el runtime de referencia, versión 10.2.0; la
  telemetría/economía del cache (RFC-74) sigue en `Proposal`.

## [10.1.0] — 2026-08-29

### Added

- **Context Persistence & Cacheability — materialización normativa** (plan 88,
  RFC-71): clasificación estable/dinámico del Execution Context, segmentos
  Core/Project/Worker como dominios semánticos, identidades compuestas
  (`SegmentContentIdentity`/`SegmentIdentity`/`SemanticContextIdentity`),
  scope, aislamiento semántico, separación de invalidación
  semántica/frescura/almacenamiento, frontera persistence ≠ provider prompt
  cache y no-modificación del Context Budget por caching/persistence (I-010),
  en `CONTEXT.md`, `KNOWLEDGE_LIFECYCLE.md`, `PROTOCOL_BOUNDARIES.md` y
  `BUDGET_MATERIALIZATION.md`. MINOR: adiciones compatibles; sin cambios de
  contratos, state machines ni workflows. Las RFCs 72–74 permanecen en
  `Proposal` y fuera de alcance.

### Modelo conceptual

- **RFC-71 implementada parcialmente** (plan 88): la RFC-71 pasa de fuente
  conceptual a materialización normativa parcial en la versión 10.1.0; la
  implementación de materialización/provider (RFC-72), persistence de proyecto
  (RFC-73) y telemetría/economía (RFC-74) sigue en `Proposal`.

## [10.0.0] — 2026-08-28

### Removed

- **Artefactos de contexto del proyecto manuales** (plan 84, RFC-70):
  `project-map.md` y `technical-analysis.md` dejan de ser artefactos del
  protocolo y el estándar `PROJECT_ARTIFACTS.md` se elimina (incluidas sus
  plantillas de dominio); el contexto estructural y técnico del proyecto se
  obtiene de la Knowledge Base de discovery
  (`.project/knowledge/discovery/`, `executive_summary.md` como entrada
  read-first), con frescura por claim y provenance.

## [9.1.0] — 2026-08-27

### Added

- **Architecture Evolution Workflow** (plan 82, RFC-68): capability de
  evolución arquitectónica en dos niveles con frontera de tres capas, cadena
  canónica y diez stages con contratos; módulo nuevo
  `orchestrators/architecture/` (state machine, rol `architecture_evolver` y
  contratos PROJECT_REGISTRY, SESSION_REGISTRY, EVIDENCE_SNAPSHOT,
  EVIDENCE_SET, ARCHITECTURAL_CHANGE_SET y ARCHITECTURE_MANIFEST).
- **Trazabilidad verificable** (plan 82, RFC-68): checker dev-only
  `tools/check_architecture_traceability.py` (AEW-001…004) y refs resolubles en
  los modelos arquitectónicos y las RFC-62…68.
- **Import Workspace** (plan 82, RFC-68): `sessions/<project-key>/.project/`
  como staging de entrada gitignored (salvo `.gitkeep`); los `.project/`
  importados no se versionan.

### Changed

- **Material de evidencia** (plan 82, RFC-68): el raw de BeaconRBX se movió de
  `reference/.project/` a `sessions/BeaconRBX/.project/` (gitignored) y las
  citas de los modelos raíz se actualizaron.

### Modelo conceptual

- RFC-68 `Accepted` (plan 82): Architecture Evolution Workflow — Fase 1.

  `Executed`. Sin cambio de payload; solo estados y traza de gobernanza.

(sin ítems de payload por ahora — los cambios de repo que no tocan el payload no se
listan; ver `docs/VERSIONING.md` §5)

---

## [9.0.0] — 2026-08-25

### Added

- **Modelo de lifecycle de conocimiento** (plan 81, RFC-67):
  `.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` define los tipos
  `snapshot`/`claim`/`lesson`, la frescura por claim con proveniencia
  resoluble, los disparadores de invalidación (incluida la post-ejecución) y
  la revalidación scoped por el pipeline de discovery; `standards/INDEX.md` lo
  referencia.
- **`kind`/`path` en KB_RECOMMENDATION** (plan 81, RFC-67): cada entrada
  recomendada declara `kind` (`discovery`|`knowledge`|`lesson`) y `path`
  resoluble (schema `2.0.0`); `session_uuid` queda como proveniencia, no como
  ubicación.
- **`invalidated_facts` en EXECUTION_SUMMARY** (plan 81, RFC-67): sección
  `## Invalidated Facts` con `fact`/`entry`/`reason` (schema `4.0.0`),
  obligatoria cuando la ejecución cambió hechos descubiertos; el pipeline
  revalida las entradas afectadas con el scope que las posee.
- **Checks mecánicos de conocimiento** (plan 81, RFC-67): `gate_validator.py`
  valida la forma de `invalidated_facts` (H05) y de `kind`/`path` (H10);
  `check_session_artifacts.py` aplica los checks a sesiones `>= 9.0.0` y
  valida la provenance de lessons (`kind: lesson`).

### Changed

- **Frescura por claim con proveniencia resoluble** (plan 81, RFC-67, MAJOR):
  `KB_DISCOVERY_ENTRY.md` declara `kind: snapshot` y semántica de claims por
  hecho; la Freshness Rule del discovery evalúa por claim y excluye de
  recomendaciones/consumo las claims vencidas o sin proveniencia;
  `DISCOVERY_STATE_MACHINE.md` agrega la condición de invocación
  post-ejecución y la medición previa para cambios de TTL; `docs/MIGRATION.md`
  §10 documenta la migración y las trazas históricas.
- **Lessons con proveniencia en el cierre** (plan 81, RFC-67, MAJOR): el
  Closing Feedback persiste lessons con `kind: lesson`, `session_id`,
  `protocol_version` y evidencia (RFC-65); `KNOWLEDGE_CURATION.md` y
  `context_discoverer.md` alineados.

### Removed

- **Reutilización de claims vencidas o con proveniencia no resoluble** (plan 81,
  RFC-67, MAJOR): deja de ser válida en entradas y recomendaciones nuevas; sin
  etiqueta de tipo no se mezclan snapshot/current/historical knowledge.

### Modelo conceptual

RFC-67 aceptada (plan 81, 2026-08-25): lifecycle mínimo de conocimiento (D9).

---

## [8.0.0] — 2026-08-25

### Added

- **Estándar de autorización** (plan 80, RFC-66):
  `.agents/standards/runtime/AUTHORIZATION.md` define el vocabulario
  Capability/Permission/Authorization/Execution/Effect, la frontera por
  defecto, quién autoriza y los estados AUTHORIZED/UNAUTHORIZED/
  AUTHORIZATION_UNDETERMINED; `standards/INDEX.md` lo referencia.
- **Bloque `effects` en el payload** (plan 80, RFC-66):
  `TASK_SPECIFICATION.md` gana la sección `## Effects`
  (`name`/`kind`/`authorized_by`/`evidence_ref`/`status`, schema `3.0.0`)
  obligatoria cuando hay efectos fuera de frontera; `EXECUTION_SUMMARY.md` gana
  `## Effects Executed` (`effect`/`executed`/`authorization_ref`, schema
  `3.0.0`); `SESSION_BRIEF.md` registra `[[effects]]` para autorizaciones de
  clarificación o default desatendido.
- **Checks mecánicos de autorización** (plan 80, RFC-66): `gate_validator.py`
  valida la forma del bloque `effects` (H01) y rechaza una sección `Effects`
  propia en EXECUTION_PLAN (H04); `check_session_artifacts.py` clasifica los
  efectos ejecutados para sesiones `>= 8.0.0`.

### Changed

- **Policies H01/H04/H05 con autorización** (plan 80, RFC-66, MAJOR): H01/H04
  exigen autorización registrada para efectos fuera de frontera y rechazan
  suposiciones no confirmadas como autorización; H05 verifica el registro de
  efectos ejecutados; `NO_ASSUMPTIONS.md` y `PROTOCOL_BOUNDARIES.md` usan el
  vocabulario del estándar.
- **Frontera verificable** (plan 80, RFC-66, MAJOR): la frontera por defecto se
  mantiene pero cada efecto fuera de frontera se vincula a una entrada de
  autorización; `docs/MIGRATION.md` §9 documenta la migración y las trazas
  históricas.

### Removed

- **Efectos fuera de frontera con suposición no confirmada sin registro**
  (plan 80, RFC-66, MAJOR): dejan de ser válidos en specs nuevos; sin registro
  la traza es AUTHORIZATION_UNDETERMINED, nunca UNAUTHORIZED por ausencia.

### Modelo conceptual

RFC-66 aceptada (plan 80, 2026-08-25): modelo de autorización y capacidades
(D8, D11).

---

## [7.0.0] — 2026-08-25

### Added

- **Clases de evidencia y estándar EVIDENCE** (plan 79, RFC-65):
  `.agents/standards/quality/EVIDENCE.md` define las cinco clases
  (`observation`/`measurement`/`attestation`/`assertion`/`reference`), el
  esquema `[[evidence]]` (`class`/`claim_id`/`ref`) y los invariantes
  EV-001…EV-004 / REL-001…REL-003; `standards/INDEX.md` y `harness/INDEX.md`
  lo referencian.
- **Bloques `[[evidence]]` en el payload** (plan 79, RFC-65):
  `VERIFICATION_REPORT.md` gana la sección `## Evidence` y `claim_id` en
  criterios/resultados (`schema_version` 3.0.0); los ENTRY de
  `HARNESS_REPORT.md` pueden registrar el array `evidence` con clase por check.
- **Checks mecánicos de evidencia** (plan 79, RFC-65): `gate_validator.py`
  (H06) valida las entries y rechaza un criterio PASS sin evidencia con clase
  válida; `audit_gates.py` marca atestaciones sin etiquetar y checks `verified`
  sin evidencia no-atestación; `check_session_artifacts.py` aplica los checks a
  sesiones `>= 7.0.0`.

### Changed

- **Policies H05/H06/H07 con evidencia con clase por ítem** (plan 79, RFC-65,
  MAJOR): los checklists citan evidencia con clase por ítem; H06 agrega el ítem
  `[gate]` de `## Evidence`/VERIFIED; H07 exige `reference`/`assertion` para la
  autorización escrita de la Rama B.
- **Significado de PASS/"verificado"** (plan 79, RFC-65, MAJOR): un claim es
  `verified` solo con una entrada de evidencia de clase distinta de
  `attestation`; un ítem `[gate]` se satisface con observación/medición/
  referencia o desviación documentada; `docs/MIGRATION.md` §8 documenta la
  migración y las trazas históricas.

### Removed

- **"Verificado" sin entrada de evidencia** (plan 79, RFC-65, MAJOR): la
  declaración "verificado" sin entrada de evidencia con clase deja de ser
  válida en reportes nuevos; el término permitido es "atestado".

### Modelo conceptual

RFC-65 aceptada (plan 79, 2026-08-25): clases de evidencia y regla VERIFIED
(D4, D12).

---

## [5.0.0] — 2026-08-25

### Added

- **Dimensiones de estado y lifecycle de artefactos** (plan 77, RFC-63): el
  payload declara tres dimensiones con entidad propia (Task State, Gate State,
  Artifact Lifecycle) y cuatro derivadas (Execution, Verification, Approval,
  Plan) con sus fuentes de verdad en `harness/INDEX.md` (§State dimensions); el
  Artifact Lifecycle (`draft`/`validated`/`superseded`) es derivado del registro
  de gates y nunca se escribe a mano.
- **`Deferred Items` y review gate** (plan 77, RFC-63):
  `VERIFICATION_REPORT.md` gana la sección `## Deferred Items` (aprobaciones
  humanas diferidas con confirmación) y `SESSION_BRIEF.md` registra los
  diferidos; para `complex` con `rubrics` habilitado, el review sobre
  `REVIEW_REPORT.md` es un Gate State obligatorio (`review_passed` /
  `review_failed`) registrado en `HARNESS_REPORT.md` (trigger `REVIEW`).
- **Checks mecánicos de lifecycle** (plan 77, RFC-63): `gate_validator.py`
  rechaza secciones en conflicto (H00/H03), `complex` sin `REVIEW_REPORT.md` y
  `Deferred Items` inválidos; `check_session_artifacts.py` detecta campos
  manuales de estado y COMPLETED sin gates in-scope para sesiones `>= 5.0.0`.

### Changed

- **Semántica de COMPLETED relativa al alcance** (plan 77, RFC-63, MAJOR):
  COMPLETED exige gates en-scope PASS, sin criterios FAIL/PENDING y aprobaciones
  completadas o diferidas con confirmación; H05/H06/H07 citan la dimensión de
  cada check en sus Gate Checklists; `protocol/.agents/orchestrators/core/roles/orchestrator.md`
  §4.1 hace determinista el review gate.

### Removed

- **Campos manuales de estado** (plan 77, RFC-63, MAJOR): `status` (Metadata),
  sección `## State`, `validation.complete` y `approved` (Plan Decision)
  desaparecen de los siete contratos de artefactos; `schema_version` 2.0.0.

### Modelo conceptual

RFC-63 aceptada (plan 77, 2026-08-25): dimensiones de estado, lifecycle de
artefactos y semántica de COMPLETED (D1, D2, D3).

---

## [4.0.0] — 2026-08-25

### Added

- **Catálogo de garantías y matriz de enforcement** (plan 76, RFC-62): `harness/INDEX.md` declara el catálogo cerrado de 12 garantías clasificadas en cinco clases (declarativa, verificable, mecánicamente enforceada, juicio del agente, actores externos) y la matriz por capa (agente / harness / runtime / externo / humano) con las invariantes ENF-001…ENF-003; `docs/ADOPTION.md` §6.4 la expone para adoptantes.
- **Regla de claims y campos de clase** (plan 76, RFC-62): "zero hallucinations" deja de ser una garantía técnica; todo claim es evidencia-citado o está marcado como atestación/inferencia. Los checks de `HARNESS_REPORT.md` y los criterios/resultados de `VERIFICATION_REPORT.md` ganan `claim_class` (`verified` / `attested` / `inference`); `clock` (`utc` | `agent_clock`) en los ENTRY y en los eventos de `METRICS.md`; `Evidence` opcional en `SESSION_LOG.md`; checklist de `PROTOCOL_HEALTH.md` con presencia de registros raíz, identidad de sesión y reloj.
- **Checkers dev de las celdas External** (plan 76, RFC-62): `check_session_artifacts.py` valida presencia/versión/UUID de sesión, atestaciones sin marca y timestamps UTC para sesiones `>= 4.0.0`; `aggregate_metrics.py --audit` reconcilia `state.json` ↔ `HARNESS_REPORT.md` en ambas direcciones para los gates de estado.

### Changed

- **Significado declarado de "verificado"** (plan 76, RFC-62, MAJOR): un claim es `verified` solo con evidencia de clase distinta de atestación; sin evidencia el término es `attested`. Las policies H01/H06/H07 citan evidencia con clase en sus Gate Checklists; `docs/MIGRATION.md` §6 documenta la migración y las trazas históricas.

### Modelo conceptual

RFC-62 aceptada (plan 76, 2026-08-25): modelo híbrido de garantías y fronteras de enforcement (D0, D11).

---

## [3.26.0] — 2026-08-24

### Added

- **Consentimiento del discovery** (plan 75, RFC-61): flag declarativo `discovery_require_consent` (default `true`) que convierte la detección automática del discovery en una consulta No-Assumption al usuario (condición disparada, opciones `full`/`lite`/sin discovery + opción libre); ante silencio o respuesta vaga se pide clarificación (sin default), en sesión no interactiva no se ejecuta y el bypass queda registrado en `SESSION_LOG.md`; con `false` se restaura la invocación automática.
- **Scope `lite` de discovery** (plan 75, RFC-61): `init_worker` + `environment_worker` + `stack_worker` + `framework_worker` + `synthesis_worker`, respetando el grafo de dependencias; figura en la tabla de scopes, en la invocación y en el marcador `.last_discovery`.
- **Skill `/discovery`** (plan 75, RFC-61): skill user-invoked fuera de la activation table; `/discovery` y `/discovery full` ejecutan `full`, `/discovery lite` ejecuta `lite`; reporta entradas escritas/actualizadas, stale marcados y duración.
- **Evento de métricas `discovery_consent`** (plan 75, RFC-61): catálogo del contrato `METRICS.md` con `condition`, `options`, `decision`; métrica `discovery.consent_by_decision` de clase Recorded en `PROTOCOL_METRICS.md`.

### Changed

- **Cierre de tarea con "What we learned"** (plan 75, RFC-61): el feedback de cierre posterior a `VERIFYING → COMPLETED` (gated por H06/H07) incluye la sección condicional "Qué aprendimos" con el conocimiento persistido en `.project/knowledge/entries/`, informativa y sin acción requerida del usuario; `VERIFICATION_REPORT.md` no se modifica.

## [3.20.0] — 2026-08-16

### Fixed

- **Conteo de scripts del harness y literal de budget de discovery** (plan 69,
  bloque 0 de la auditoría de sistema 3.1): `harness/INDEX.md` pasa de "three
  pure-stdlib scripts" a cuatro (incluye `gate_validator.py`); el ejemplo de
  invocación al Discovery Orchestrator en `orchestrator.md` usa
  `context_budget: 32000`, alineado con `discovery_context_budget` de
  `features.toml`.
- **Modelo produced_by/consumed_by de contratos de discovery** (plan 69,
  Clase B): la taxonomía refleja los productores reales de
  `INTER_WORKER_MESSAGE.md` y `KB_DISCOVERY_ENTRY.md` (los workers por scope),
  coherente con el front matter TOML de los contratos.
- **Snapshot del índice y conteos de auditorías previas** (plan 69): header de
  `plans/INDEX.md` alineado con el estado real (3.19.0, `dev` en sync),
  `[Unreleased]` del changelog sin claims stale, y conteos de tests de
  `docs/AUDITORIA_DOCUMENTACION.md` / `AUDITORIA_SISTEMA.md` actualizados.

## [3.21.0] — 2026-08-16

### Added

- **Chequeo mecánico de salidas de state machines** (plan 70):
  `check_taxonomy_coherence.py` compara los "Required Output Artifacts" de
  cada state machine contra los `output_artifacts` del workflow mapeado
  (bidireccional, con normalización de prefijos de orden). Sobre el payload
  previo a esta versión detecta 21 mismatches de discovery; tras la
  alineación queda en verde.

### Changed

- **Contrato de verificación y H06 alineados** (plan 70): `[[test_results]]`
  de `VERIFICATION_REPORT.md` declara el campo opcional `evidence` (archivo
  existente o comando en `SESSION_LOG.md`); el ítem 7 del Gate Checklist de
  H06 verifica el campo cuando está declarado, con fallback a `SESSION_LOG.md`.
- **Listas de salidas de discovery completas y con paths reales** (plan 70):
  los front matters de los workflows 01–06 de discovery y sus entidades en la
  taxonomía usan los nombres de archivo de KB reales (`environment.md`,
  `development_patterns.md`, etc.) e incluyen todas las entradas de KB por
  estado; la entidad de estado `discovery:DISCOVERY_INIT` corrige su
  `artifacts_output` (incluye `discovery_input.json`, `invalidation_report.json`
  y `file_map.md`; elimina el `KB_DISCOVERY_ENTRY.md` erróneo).
- **Convención de naming de contratos por entrada** (plan 70):
  `KB_DISCOVERY_ENTRY.md` documenta que el nombre del contrato (p.ej.
  `ENVIRONMENT_DISCOVERY.md`) no es el path del artefacto (p.ej.
  `environment.md`).

## [3.22.0] — 2026-08-16

### Added

- **Cobertura bidireccional de gates en el checker** (plan 71):
  `check_taxonomy_coherence.py` verifica que el origen de cada gate coincide
  con el `state` declarado por su policy y que el header TOML `transition` y
  los `gates:` de cada policy nombran las mismas transiciones, con tests.

### Fixed

- **Validador estructural profile-aware para H04** (plan 71, F-A): para tareas
  de perfil `trivial`, `gate_validator.py` ya no exige `## Context Reference`
  (el contrato de `EXECUTION_PLAN.md` la omite en el ciclo reducido); el perfil
  se lee de `TASK_ANALYSIS.md` de la sesión, con tests de producto del camino
  trivial.
- **Gate trivial declarado en H00** (plan 71, F-B): el front matter de H00
  (header `transition` y `gates:`) y la tabla de triggers de `harness/INDEX.md`
  declaran `ANALYZING_TASK → PLANNING` (solo perfil trivial), alineados con la
  máquina de estados.

## [3.23.0] — 2026-08-16

### Added

- **Auditoría post-hoc de gates** (plan 72): nuevo tool dev-only
  `tools/audit_gates.py` que recomputa el subconjunto estructural de los PASS
  registrados en `HARNESS_REPORT.md` invocando el validador del producto y
  reporta los PASS que el validador rechaza sin desviación registrada.

### Changed

- **Evidencia determinista de tests en H06** (plan 72): `gate_validator.py`
  valida el bloque `[[test_results]]` de `VERIFICATION_REPORT.md` — resultados
  no `SKIPPED` deben declarar `evidence` que resuelva a un archivo existente o
  tener el comando `test` en `SESSION_LOG.md` (semántica del contrato 3.21.0 y
  de H06 ítem 7); sin bloque TOML el chequeo es SKIP.
- **Registro de desviaciones documentadas** (plan 72): `HARNESS_REPORT.md`
  define el campo opcional `deviation` (cause + evidence) en los ENTRY como
  única vía para que un FAIL estructural se registre como PASS, y
  `harness/INDEX.md` declara su regla (nunca silenciosa, no afecta el fail-open
  de los hooks, auditable post-hoc); `check_session_artifacts.py` valida la
  forma del objeto.

## [3.24.0] — 2026-08-16

### Modelo conceptual

- **Recovery context, ranking de destinos múltiples y continuidad de sesión**
  (plan 73, RFC-59): definidas la derivación de las variables de las recovery
  decision tables (mecánicas desde el validador/filesystem; de juicio con
  evidencia al momento del fallo) y su registro como objeto `recovery` en la
  entrada FAIL de `HARNESS_REPORT.md`; el ranking de destinos de recovery (fase
  más temprana con artefacto inválido, un destino por entrada,
  `pending_artifacts` en `RECOVERY_REPORT.md`); y el procedimiento de
  reanudación de iteraciones parciales ("artefacto intacto" + 5 pasos) en
  `PROTOCOL_BOUNDARIES.md`.

## [3.25.0] — 2026-08-17

### Modelo conceptual

- **Contabilidad del Context Budget y clases de confianza de métricas**
  (plan 74, RFC-60): el Budget materializado pasa de advisory a measured —
  `consumed` se computa con la regla de estimación sobre los excerpts de
  `knowledge_entries`, se registra en el evento `context_budget` y los overruns
  post-compresión son desviaciones registradas; `PROTOCOL_METRICS.md` declara
  las clases Derived / Recorded / Verified para el catálogo y el agregador gana
  el modo `--audit` (gates de `state.json` vs entradas de `HARNESS_REPORT.md`).

### Changed

- **Superficie de bypass del hook endurecida** (plan 74, ítem 20): `Write`/
  `Edit` cuyo `tool_input` es un dict sin target (`file_path`/`path`/
  `filename`) pasan de fail-open a deny (exit 2); `tool_input` ausente y los
  errores internos siguen fail-open; `Read`/`Glob`/`Grep`/`Bash` siguen sin
  gate, con la cobertura por el scan post-hoc documentada en
  `harness/INDEX.md` (§Bypass surface and coverage).

### Added

- **Tool de medición del budget** (plan 74): `tools/measure_context_budget.py`
  computa `consumed` desde un payload de delegación y falla en overrun.

## [3.19.0] — 2026-08-15

### Changed

- **Validador estructural obligatorio en los gates** (plan 68, RFC-58, F1-B):
  para los triggers soportados (H00–H07, H09–H11, D00) el Orchestrator MUST
  invocar `gate_validator.py` antes de juzgar PASS; un FAIL estructural
  bloquea el PASS salvo desviación documentada. El fail-open de los hooks y
  los ítems `[agent]` no cambian.

---

## [3.18.0] — 2026-08-15

### Added

- **Soporte estructural de H15 en el runner** (plan 67, B-6):
  `runner_state.py validate-delegation` y `validate-return` validan el payload
  de delegación y el return report contra el contrato (campos requeridos,
  tipos, enums de `profile`, `context_budget` finito positivo, prefijos de
  clase en `deviations`). El gate H15 sigue siendo juicio del Orchestrator;
  los subcomandos son soporte mecánico de schema.

---

## [3.17.0] — 2026-08-15

### Added

- **Validador estructural opcional del harness** (plan 66, RFC-57):
  `.agents/harness/gate_validator.py` implementa el subconjunto
  mecánicamente checkable de los ítems `[gate]` (existencia, secciones
  normativas, bloques TOML y enums, resolución de citas, EARS, rubricas
  estructurales) para H00–H07, H09–H11 y D00. Es soporte opcional de revisión:
  el juicio del Orchestrator sigue siendo el árbitro, nunca bloquea, y sus
  resultados se registran como evidencia en `HARNESS_REPORT.md`.

---

## [3.16.0] — 2026-08-14

### Changed

- **Evidencia de flags declarada (F7-A)** (plan 65): procedimiento canónico de
  evidencia en `standards/INDEX.md` (expected = `declarative_flags` de
  `session_start`; evidenced = eventos `flag_evidence`; unevidenced = expected
  − evidenced), con la agregación de métricas como mecanismo declarado y la
  honestidad de que los eventos son auto-reportados. La "unevidenced
  compliance" pasa a ser detectable.
- **Modelo de determinismo de contexto declarado (F5-A)** (plan 65):
  `CONTEXT.md` declara que la asamblea de contexto es juicio con criterios
  ordenados (determinismo procedimental, no machine-enforced), coherente con
  el budget advisory (P2.1); las "harness Future Extensions" quedan como
  posibilidades, no garantías.

---

## [3.15.0] — 2026-08-14

### Changed

- **Modelo de enforcement declarado honestamente** (plan 64, F1-A): el payload
  distingue tres capas — enforced (caparazón de hooks, fail-open), reviewed
  (gates por juicio del Orchestrator, trail auto-reportado) y verified
  (checkers de desarrollo, dev-only). `harness/INDEX.md` gana la sección
  "Enforcement model"; las policies dejan de decir que un ítem `[gate]` es
  machine-gateable ("structurally checkable"); `HARNESS_REPORT.md` pasa a ser
  el "review trail" auto-reportado; H13 nota los checkers dev-only.

---

## [3.14.0] — 2026-08-14

### Changed

- **Resolución determinista de sesión en el hook** (plan 63, P4.2):
  `hook_gate.py` resuelve la sesión del protocolo por mapeo persistido
  (`.project/.sessions.json`), directorio exacto, sesión única o —solo en el
  primer evento de una CLI session— la más reciente, registrando el mapeo.
  `runner_state.py link --cli-session <id>` permite la vinculación explícita
  (p. ej. al reanudar entre conversaciones CLI). El fail-open y la semántica
  de los gates no cambian.

---

## [3.13.0] — 2026-08-14

### Changed

- **Context Budget declarado advisory** (plan 62, P2.1): `context_budget` no se
  mide ni se trunca mecánicamente; el estado de enforcement queda declarado en
  el contrato de delegación, `BUDGET_MATERIALIZATION.md` y `CONTEXT.md`. La
  contabilidad declarado vs consumido sigue registrándose por el evento de
  métricas.
- **Contratos versionados con `schema_version`** (plan 62, P4.3): todo contrato
  declara `schema_version` (semver) en su front matter; el checker de
  coherencia taxonómica valida presencia y formato; `MIGRATION.md` documenta
  el uso para adoptantes. Adición compatible de metadata: los artefactos
  válidos previos siguen siendo válidos.

---

## [3.12.0] — 2026-08-14

### Changed

- **Dominio canónico de `produced_by` en contratos** (plan 61, P1.2):
  `produced_by` en el front matter TOML usa nombres canónicos de la taxonomía
  (actor, `role_id` o `worker_id`); los estados viven solo en el bloque YAML
  del taxonomy (`PROTOCOL_HEALTH.md` ítem 3). Contratos normalizados:
  `KNOWLEDGE_INDEX.md`/`PROJECT_README.md` (`system_agent`) y
  `KB_DISCOVERY_ENTRY.md` (roles de workers). Cierra la contradicción §18.9.
- **`profile` de workflows validado** (plan 61): nombre canónico de
  worker/rol o `null`; el checker de coherencia taxonómica valida
  `produced_by`, `profile` y el catálogo de perfiles ↔ taxonomía.

---

## [3.11.0] — 2026-08-14

### Changed

- **Convención de `[Unreleased]`** (plan 60): `[Unreleased]` vuelve a la cima
  del changelog (Keep a Changelog); las secciones con fecha sin tag en `dev`
  quedan definidas como releases en curso que se oficializan al promover
  (`docs/VERSIONING.md` §5).
- **Esquema de evento de hook documentado** (plan 60): `harness/INDEX.md`
  define el contrato JSON del evento de hook (enforced mode) y su semántica
  fail-open.
- **Semántica de `retry_count`** (plan 60): derivada de las entradas `FAIL`
  del `HARNESS_REPORT.md` por trigger e iteración; documentada en
  `harness/INDEX.md` y `orchestrator.md`.
- **Modelo D01 aclarado** (plan 60): hoy no hay runner ejecutable en el
  harness; la validación mecánica de D01 es una extensión futura posible, no
  parte del payload distribuido.

### Fixed

- **Contradicción de la política single-source (§18.6)** (plan 60):
  `PROTOCOL_BOUNDARIES.md` declara la excepción aprobada del restatement de
  inmutabilidad en `ANTI_CIRCUMVENTION.md`.

---

## [3.10.0] — 2026-08-14

### Changed

- **Camino trivial legalizado** (plan 59, RFC-26 enmendada):
  `ANALYZING_TASK → PLANNING` queda como transición permitida solo para el
  perfil `trivial`, con `TASK_ANALYSIS.md` como referencia de tarea y sin
  artefactos de contexto. Se alinean la máquina de estados (Task Profiles,
  No-Skip Rule), los workflows 00/05/06/07 y su INDEX, las policies
  H00/H04/H06 y los contratos `TASK_ANALYSIS`, `EXECUTION_PLAN` y
  `VERIFICATION_REPORT`. Adición compatible: los artefactos válidos previos
  siguen siendo válidos.
- **Taxonomía alineada con la máquina de estados** (plan 59, RFC-30):
  `core:RECOVERY.next` incluye las cuatro fases tempranas y
  `core:ANALYZING_TASK.next` incluye `PLANNING`; H13 documenta las
  transiciones condicionales por perfil.

### Fixed

- **Contradicciones §18.1 (taxonomía vs máquina de estados en RECOVERY) y
  §18.2 (ciclo trivial con transición e inputs indefinidos)** (plan 59):
  cerradas; el ciclo trivial es ejecutable sin transiciones ni inputs
  indefinidos.

---

## [3.9.0] — 2026-08-14

### Changed

- **RECOVERY_REPORT — destinos de fases tempranas** (plan 58, RFC-30):
  `corrective_action.recommended_next_state` admite `ANALYZING_TASK`,
  `BUILDING_TASK_SPECIFICATION`, `GATHERING_CONTEXT` y `VALIDATING_CONTEXT`,
  alineando el contrato con las aristas de recovery ya legales en la máquina
  de estados; `08-recovery.md` alinea la recomendación. Adición compatible:
  los reportes válidos previos siguen siendo válidos.

### Fixed

- **Actor único de hashes en discovery** (plan 58, RFC-54): `orchestrator.md`
  (sección 4.3) ya no instruye al core Orchestrator a computar hashes ni a
  transportarlos en el payload de invocación; los computa `init_worker`
  (`DISCOVERY_STATE_MACHINE.md`, sección Hash Calculation), completando la
  ejecución del plan 53.
- **Metadata de contratos de discovery** (plan 58): `INTER_WORKER_MESSAGE.md`
  declara `produced_by` con roles explícitos de los workers de discovery;
  `DISCOVERY_MANIFEST.md` aclara la relación contrato ↔ artefacto
  (`.discovery_manifest`).

---

## [3.8.0] — 2026-08-14

### Added

- **Contratos por entrada del discovery** (plan 47, RFC-48): 14 contratos
  nuevos en `.agents/orchestrators/discovery/contracts/` (FILE_MAP, STACK,
  DEPENDENCIES, CONTAINERS, DATABASE, DISTRIBUTION, ARCHITECTURE,
  CONFIGURATION, ENTRYPOINT, BUSINESS_RULES, PROJECT_FLOW, TECHNICAL_DEBT,
  KNOWN_ERRORS, GLOSSARY) con el formato base de `KB_DISCOVERY_ENTRY.md` más
  sus secciones específicas. Las 14 entidades quedaron registradas en
  `PROTOCOL_TAXONOMY.md`.

### Changed

- **D01 single-source** (plan 47, RFC-48): el ítem 12 de
  `D01-discovery-output.md` verifica las secciones contra los contratos por
  entrada y elimina el listado duplicado de secciones.

---

## [3.7.0] — 2026-08-12

### Added

- **Test de integración del modo enforced** (plan 46, RFC-47):
  `.agents/harness/tests/test_enforced_flow.py` verifica end-to-end el flujo
  `state.json` + hooks en layout adoptado (deny sin H04, allow con H04, deny
  de `Stop` sin cierre, allow con H06/terminal, alerta del scan de bypass).
  El modo enforced queda verificado empíricamente (dogfooding, F-09/B-6).

---

## [3.6.3] — 2026-08-12

### Fixed

- **Redacción de contratos de discovery** (plan 53, RFC-54): el
  `project_shape` se declara en sección explícita `## Project Shape`
  (elimina el requisito ambiguo de "primera línea", F-15) y el actor único
  del cálculo de hashes es `init_worker` (F-19).

---

## [3.6.2] — 2026-08-12

### Fixed

- **Candidatura de tareas tooling/CLI** (plan 52, RFC-53):
  `ORCHESTRATION_GUIDE.md` declara que tooling/CLI sin dominio cubierto
  produce candidatura vacía → worker genérico (resultado legítimo de Q7);
  enmienda menor registrada en RFC-20 (F-06).

---

## [3.6.1] — 2026-08-12

### Fixed

- **Catálogo de fases y skills de workers** (plan 51, RFC-52): `worker.md`
  agrega la fase 01 (`intent_reflector`, perfil de fase) al catálogo;
  `recovery_analyst.md` alinea sus skills con la tabla de activación
  (`hypothesis-generator`, `risk-detector`).

---

## [3.6.0] — 2026-08-12

### Added

- **Regla de frescura de la KB de discovery** (plan 50, RFC-51): las
  entradas se consumen solo frescas (verificación de TTL antes de delegar);
  las vencidas se marcan `[entries] stale` y se revalidan solo por pipeline;
  `.project/.last_discovery` es el marcador único (legado deprecado) y el
  health checklist lo valida (F-12).

---

## [3.5.0] — 2026-08-12

### Added

- **Modos de ejecución de delegaciones** (plan 49, RFC-50): modo subagente
  (recomendado) y modo single-instance (permitido con mitigaciones:
  verificación como pasada separada con evidencia escrita, prohibición de
  auto-aceptar recomendaciones sin evidencia, registro de riesgo en
  `METRICS.md`); el modo se declara en `SESSION_LOG.md` y `DECISIONS.md`
  aclara que la autoridad del orquestador es independiente del modo (F-09).

---

## [3.4.2] — 2026-08-12

### Fixed

- **Validación mecánica de skills del protocolo** (plan 48, RFC-49): el
  checker de invariantes del repo de desarrollo gana el invariante SKILLS
  (front matter, `name` == directorio, referencias citadas, inventario INDEX
  ↔ directorios); `skills/README.md` e `skills/INDEX.md` actualizan su
  Enforcement para declararlo (dev-only, no bloqueante).

---

## [3.4.1] — 2026-08-12

### Added

- **Versión de protocolo en trazas de sesión** (plan 45, RFC-46):
  `SESSION_LOG.md`, `METRICS.md` (`session_start`) y `HARNESS_REPORT.md`
  declaran `protocol_version`; las trazas son registros inmutables de la
  versión vigente (gates por runner antes de 2.0.0, por juicio desde 2.0.0).

---

## [3.4.0] — 2026-08-12

### Added

- **Modo desatendido de clarificación (opt-in)** (plan 44, RFC-45):
  `NO_ASSUMPTIONS.md` define el modo (política de defaults declarada,
  aplicación marcada, confirmación diferida — nunca asumir en silencio);
  `AGENT_STATE_MACHINE.md` lo integra en `NEEDS_CLARIFICATION`;
  `SESSION_BRIEF.md` gana `source: unattended_default` y `SESSION_LOG.md` el
  registro `PENDING_USER_CONFIRMATION` (F-05).

---

## [3.3.2] — 2026-08-12

### Fixed

- **Estado productor de INTENT_REFLECTION en confianza HIGH** (plan 43,
  RFC-44): `ANALYZING_TASK` declara la reflexión como salida opcional en la
  vía HIGH (auto-confirmada, H11 la gates antes de
  `BUILDING_TASK_SPECIFICATION`); `orchestrator.md` y el workflow 00
  describen ambas vías de producción (F-04).

---

## [3.3.1] — 2026-08-12

### Fixed

- **Regla muerta de entidades `planned` en H13** (plan 42, RFC-43): la regla
  9 de la policy pasa a nota histórica (el mecanismo `planned` ya no existe
  en la taxonomía; se documenta cómo restaurarla si se reintroduce).

---

## [3.3.0] — 2026-08-12

### Changed

- **Namespacing de artefactos de discovery y excepción de intermedios**
  (plan 40, RFC-41): `PROTOCOL_BOUNDARIES.md` declara la unicidad de
  `<order>` por dominio (discovery usa prefijo `D<order>-`) y la excepción de
  intermedios de discovery en `.project/<session-uuid>/discovery/`; la
  máquina de discovery numera su reporte con el prefijo. Resuelve las
  colisiones de `<order>` entre dominios (F-20) y el workaround del
  artefacto-puente (F-11). Guía en `MIGRATION.md` §3.2.

---

## [3.2.1] — 2026-08-12

### Fixed

- **Procedencia real de las entradas de discovery** (plan 39, RFC-40):
  `produced_by` de `KB_DISCOVERY_ENTRY.md` y de la taxonomía pasa a la lista
  de estados productores de la máquina de discovery (ENV, STACK, FRAMEWORK,
  PATTERNS, BUSINESS, MERGE); `DISCOVERY_INIT` deja de figurar como productor
  de las entradas generales.

---

## [3.2.0] — 2026-08-12

### Added

- **Configuración real de presupuesto y muestreo de discovery** (plan 38,
  RFC-39): `features.toml` define `discovery_context_budget` (estimated
  tokens) y `discovery_sample_size_per_language`; `init_worker` los
  materializa en `discovery_input.json` y los workers de discovery dejan de
  declarar defaults propios (fricción F-13).

---

## [3.1.0] — 2026-08-12

### Changed

- **Semántica de los bloques de confianza de TASK_ANALYSIS** (plan 37,
  RFC-38): el bloque `[confidence]` queda redefinido como confianza de la
  calidad del análisis (evidencia que sostiene sus afirmaciones), gobernado
  por `CONFIDENCE.md`; `intent_confidence` es el bloque canónico de la
  interpretación de intención, gobernado por `INTENT_CONFIDENCE.md`.
  Contrato y policy H00 alineados; los criterios de completitud nombran
  ambos bloques explícitamente.

---

## [3.0.7] — 2026-08-12

### Fixed

- **Inmutabilidad del payload declarada en anti-circumvention** (plan 56):
  `.agents/standards/conduct/ANTI_CIRCUMVENTION.md` ahora cuenta como
  circunvention modificar `.agents/` por fuera del cauce de releases (la
  versión publicada es la única unidad de cambio válida) y define la
  consecuencia en Enforcement (payload inválido hasta coincidir con una
  versión publicada; revert o `RECOVERY`). Regla inline, autocontenida.

---

## [3.0.6] — 2026-08-12

### Fixed

- **Autocontención del setup de hooks en el payload** (plan 55): la
  configuración de hooks por CLI (Kimi Code, Claude Code, managed settings)
  se trasladó de `ADOPTION.md` —que no se distribuye— a
  `.agents/harness/INDEX.md` (sección "Hook setup (enforced mode)"), y se
  eliminó la referencia del payload a `ADOPTION.md`. El modo enforced es
  configurable desde el payload solo; `ADOPTION.md` apunta a la sección del
  payload.

---

## [3.0.5] — 2026-08-12

**Source containment: protocol payload in `protocol/`** (plan 54, RFC-55):
el payload del protocolo se mueve a `protocol/` (`protocol/.agents/` +
`protocol/_AGENTS.md`) y el repo fuente pasa a ser un workspace de desarrollo
con `AGENTS.md` propio (dev). `dist` no cambia: sigue publicando `.agents/` +
`AGENTS.md` en la raíz del adoptante; el workflow renombra `_AGENTS.md` a
`AGENTS.md` al publicar. Incluye: nuevo AGENTS.md raíz (dev), tooling dev con
`--payload protocol` y mapeo legacy de citas, consolidación de `dev/`
(`README.md`, `ROADMAP.md`, `source-layout.md`), y actualización de CI y
documentación raíz. El contenido distribuido es semánticamente idéntico; el
entry file se renombra solo en el árbol fuente.

### Modelo conceptual

- RFC-55 (`plans/rfc/55-protocol-source-containment.md`) — `Accepted`.

---

## [3.0.4] — 2026-08-11

Release PATCH de la remediación de la auditoría 2.0.1 (plan 36, RFC-37):
declaración de H10 como gate opcional de uso en la fase 03. Cambio documental;
sin cambios en el modelo conceptual ni en el comportamiento opcional.

### Fixed

- **H10 como gate opcional de uso** (plan 36, RFC-37): el front matter de
  `03-gather-context.md` declara solo `H02-context-artifact` como gate de
  transición y el cuerpo documenta cuándo se evalúa H10 (recomendaciones de KB
  con `knowledge_base` habilitado); la policy H10 pasa a `gates: []` y su
  `Trigger` aclara que no protege transiciones; los entries `H10-kb-discovery-report`,
  `core:GATHERING_CONTEXT` y `workflow:03-gather-context` de
  `PROTOCOL_TAXONOMY.md` quedan alineados. Ejecutado por vía plan (RFC-42) con
  autorización explícita del usuario.

### Modelo conceptual

RFC-37 permanece en `Proposal` (regularización de gobernanza pendiente); el
plan 36 quedó `Executed`.

---

Nota: el tag git `3.0.4` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [3.0.3] — 2026-08-11

Release PATCH de la remediación de la auditoría 2.0.1 (plan 35, RFC-36):
inputs completos del workflow 05. Cambio documental; sin cambios en el modelo
conceptual.

### Fixed

- **Workflow 05 — inputs completos** (plan 35, RFC-36): el front matter de
  `05-plan.md` declara `CONTEXT_ARTIFACT.md` como input junto con
  `TASK_SPECIFICATION.md` y `CONTEXT_VALIDATION_REPORT.md`; el rol `planner`
  y los entries `workflow:05-plan`, `core:PLANNING` y el worker `planner` de
  `PROTOCOL_TAXONOMY.md` quedan alineados. Ejecutado por vía plan (RFC-42) con
  autorización explícita del usuario.

### Modelo conceptual

RFC-36 permanece en `Proposal` (regularización de gobernanza pendiente); el
plan 35 quedó `Executed`.

---

Nota: el tag git `3.0.3` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [3.0.2] — 2026-08-11

Release PATCH de la remediación de la auditoría 2.0.1 (plan 34, RFC-35):
inputs y decisión coherentes del workflow 07. Cambio documental; sin cambios
en el modelo conceptual.

### Fixed

- **Workflow 07 — inputs y decisión coherentes** (plan 34, RFC-35): el front
  matter de `07-verify.md` declara los tres inputs reales
  (`TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md`, `EXECUTION_SUMMARY.md`); el
  cuerpo gana la subsección `## Execution Summary`; la decisión final del
  reporte pasa de `FAILED` a `RECOVERY`, alineada con el contrato
  `VERIFICATION_REPORT.md` y el gate H06; el entry `workflow:07-verify` de
  `PROTOCOL_TAXONOMY.md` queda alineado. Ejecutado por vía plan (RFC-42) con
  autorización explícita del usuario.

### Modelo conceptual

RFC-35 permanece en `Proposal` (regularización de gobernanza pendiente); el
plan 34 quedó `Executed`.

---

Nota: el tag git `3.0.2` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [3.0.1] — 2026-08-11

Release PATCH de la remediación de la auditoría 2.0.1 (planes 31-33, RFC-32…34):
unificación del perfil de la fase 02, canonicalización de la lista de pasos de
`EXECUTION_SUMMARY.md` y forma canónica de los criterios de aceptación EARS.
Cambios documentales y de redacción de contratos/policies; sin cambios en el
modelo conceptual.

### Fixed

- **Perfil unificado de la fase 02** (plan 31, RFC-32): la tabla de activación
  de skills (`.agents/skills/INDEX.md`) y la guía de orquestación
  (`ORCHESTRATION_GUIDE.md` §7) ahora nombran el rol de fase
  `task_specification_writer` para `02-build-task-specification.md`, eliminando
  la contradicción con el front matter del workflow 02 y el uso de
  `functional_writer` fuera de su dominio (documentación funcional de fase 06).
- **Schema único de pasos en `EXECUTION_SUMMARY.md`** (plan 32, RFC-33):
  `[[steps_executed]]` es el único nombre de la lista de pasos (template del
  cuerpo y sección machine-readable); `[[steps]]` desaparece del contrato y los
  artefactos históricos que lo usen son no conformes (nota de migración en el
  contrato).
- **Forma canónica de Acceptance Criteria (EARS)** (plan 33, RFC-34): los
  bullets Markdown son la forma canónica de `## Acceptance Criteria` en
  `TASK_SPECIFICATION.md`; el bloque TOML `acceptance_criteria` queda como
  representación machine-readable opcional y derivada; H01 declara que los
  criterios presentes solo en TOML constituyen una violación de forma.

### Modelo conceptual

RFC-32…34 permanecen en `Proposal` (regularización de gobernanza pendiente,
mismo tratamiento que RFC-24…28); los planes 31-33 quedaron `Executed` con
autorización explícita del usuario.

---

Nota: el tag git `3.0.1` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [3.0.0] — 2026-08-11

Release MAJOR de la remediación de la auditoría 2.0.1 (planes 28-30, RFC-29…31):
H07 con dos ramas de scope compliance, recovery a fases tempranas con retry
acotado, y soporte de cierre por `ABORT` en artefacto, estado y hook.

### Changed

- **H07 — dos ramas de scope compliance** (plan 28, RFC-29): `VERIFICATION_REPORT.md`
  define la Rama A (sin extra) y la Rama B (trabajo extra autorizado por escrito
  con evidencia citada); H07 pasa con la Rama B solo si la evidencia existe y la
  juzga el Orchestrator; `RUBRICS.md` y `orchestrator.md` alineados. Cambio MAJOR
  de semántica.
- **Recovery a fases tempranas** (plan 29, RFC-30): `AGENT_STATE_MACHINE.md`
  agrega las aristas `RECOVERY → ANALYZING_TASK | BUILDING_TASK_SPECIFICATION |
  GATHERING_CONTEXT | VALIDATING_CONTEXT` y define `RETRY_WORKER` como acción
  correctiva sin transición; H01 gana una rama de retry acotado para fallos de
  formato; workflow 08 y H03 alineados. Cambio MAJOR del modelo de estados.
- **ABORT en el flujo de artefacto y de cierre** (plan 30, RFC-31):
  `RECOVERY_REPORT.md` admite `ABORT` en `corrective_action.recommended_next_state`
  (abort fundado); `runner_state.py` registra estado terminal
  (`terminal --state ABORT|COMPLETED`); `hook_gate.py` permite el cierre por
  `Stop` con estado terminal; `DECISIONS.md` D5 y `harness/INDEX.md` alineados.
  Cambio MAJOR de contrato.

### Modelo conceptual

RFCs aceptadas que gobiernan esta versión: RFC-29 (H07, trabajo extra autorizado
por el usuario), RFC-30 (recovery a fases tempranas) y RFC-31 (ABORT en el flujo
de artefacto y de cierre). Índice completo con status: `plans/INDEX.md` §Serie de
RFCs.

---

Nota: el tag git `3.0.0` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

---

## [2.0.1] — 2026-08-11

Release de mantenimiento documental tras la migración 2.0.0: restaura los
invariantes del protocolo en el propio repo y agrega verificación mecánica
dev-only para que no vuelvan a romperse. Origen: auditoría de referencias y
revisión de documentación (10–11 ago 2026).

### Added

- **Verificación mecánica de invariantes (dev-only)**: checker
  `dev/tools/check_protocol_invariants.py` (resolución de referencias, frontera
  `.agents/` autocontenido, metadata H13) con 50 tests, y workflow CI
  `check-protocol` que lo ejecuta en push/PR. No forma parte de lo distribuido
  a adoptantes (`dist`).

### Fixed

- **Metadata de taxonomía restaurada en los roles de fase**: `executor`,
  `planner`, `reviewer`, `verifier`, `task_analyst`, `task_specification_writer`,
  `recovery_analyst`, `context_discoverer`, `context_gatherer` y
  `context_validator` ahora llevan el bloque `taxonomy`/`kind`/`domain` que exige
  la policy H13, con campos alineados a sus entidades en
  `PROTOCOL_TAXONOMY.md`.
- **Frontera documental `.agents/` restaurada**: eliminada la referencia a
  `plans/rfc/24-...` en `.agents/skills/INDEX.md`; `.agents/` vuelve a ser
  autocontenido (solo `.agents/` + `AGENTS.md`).
- **Mención histórica corregida**: la nota sobre `technical_practices.py` en
  `.agents/standards/INDEX.md` ya no se escribe como una ruta inexistente.
- **`.project/README.md` creado** desde la plantilla del contrato, cumpliendo el
  rol del system agent en el bootstrap.

---

Nota: el tag git `2.0.1` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

## [2.0.0] — 2026-08-10

Segunda versión etiquetada del protocolo. Cierre de la migración "menos Python,
más texto": el runner de validación desaparece por completo y los gates del
harness se evalúan por juicio del orquestador contra checklists en prosa. El
Python sobreviviente son tres scripts stdlib (`hook_gate.py`, `runner_state.py`,
`health_check.py`); el modo declarativo no requiere Python. Origen:
`plans/26-hook-enforcement.md`, `plans/27-harness-coverage-closure.md` y los
commits `0fa9ce4` / `adb5b68`.

### Changed

- **Refactor "menos Python, más texto" del protocolo**: la lógica con forma de
  juicio sale del código Python y pasa a texto de protocolo; el Python restante
  solo verifica afirmaciones contra el filesystem. Criterio acordado: *Python
  verifies claims against the filesystem; the LLM verifies documents against
  documents*.
- **Recovery por tablas de decisión en Markdown**: los árboles de decisión TOML
  (H00–H07, H11, H15, D00, D01) se convierten en secciones
  «Recovery Decision Table» dentro de cada policy del harness
  (`.agents/orchestrators/*/harness/policies/`). El orquestador evalúa la tabla
  por juicio (primera regla que coincide); H09/H10 mantienen el fallback
  `RECOVERY_GENERIC`.
- **Verificación de salud del protocolo como checklist en prosa**: nuevo
  estándar `.agents/standards/runtime/PROTOCOL_HEALTH.md` aplicado por el
  system agent ArgentOS en el bootstrap. Solo la sonda de escritura/lectura de
  `state.json` queda mecánica (`health_check.py`, reducido a `probe()`). La
  regla TTL de `.project/.last_health_check` pasa a ser una regla en prosa
  (timestamp + `ttl_hours` de `features.toml`, default 24, override
  `AGENTS_HEALTH_CHECK_TTL_HOURS`).
- **Feature flags declarativos**: la resolución de flags se documenta en
  `.agents/standards/INDEX.md` (§"Feature flags") y la aplica el orquestador al
  evaluar la checklist de H01 (env `AGENTS_FEATURE_*` > `features.toml` >
  default). Se elimina el flag `decision_trees` (las tablas de recovery son
  siempre la policy). Los agentes leen `.agents/features.toml` directamente.
- **Métricas del protocolo por procedimiento en prosa**: la agregación pasa a
  `PROTOCOL_METRICS.md` §"Aggregation" como procedimiento aplicado por el
  agente bajo demanda (las métricas son advisory, nada las gatea).
- **Gates del harness evaluados en prosa; fin del runner de validación**:
  cada policy del harness declara ahora una sección «Gate Checklist» en prosa
  que el orquestador evalúa por juicio (secciones requeridas, EARS, citas,
  evidencia de tests, rúbricas, scope compliance, delegación H15). El estado
  del protocolo sigue siendo mecánico: tras un PASS juzgado por el orquestador,
  `python .agents/harness/runner_state.py --session <uuid> --trigger <HXX>
  --iteration <N> pass` registra el gate en `state.json` (escritura
  transaccional, único escritor, detección de bypass post-H04 incluida).
  `HARNESS_REPORT.md` pasa a escribirlo el orquestador (resuelve la
  contradicción latente entre el contrato y `harness/INDEX.md`). Requisitos de
  entorno por modo, documentados en `ADOPTION.md`: modo declarativo sin
  requisitos; modo enforced con Python 3.x stdlib pura (solo `hook_gate.py` +
  `runner_state.py` + `health_check.py`), sin `pip`.
- **Catálogo de prácticas técnicas en prosa**: la tabla flag → (rúbrica,
  estándar) pasa de `technical_practices.py` a `.agents/standards/INDEX.md`;
  la resolución de flags (env `AGENTS_FEATURE_*` > `features.toml` > default)
  la aplica el orquestador al evaluar H01.

### Removed

- `.agents/harness/runner.py` y los módulos `runner_models.py`,
  `runner_markdown.py`, `runner_policies.py`, `runner_artifacts.py`,
  `runner_validators.py`, `runner_citations.py`, `runner_profiles.py`,
  `runner_report.py`, `runner_paths.py` (sus validadores pasan a las
  checklists en prosa de las policies; `runner_state.py` sobrevive, reescrito
  autocontenido con un CLI mínimo de registro de estado).
- `.agents/harness/technical_practices.py` (catálogo movido a
  `.agents/standards/INDEX.md`).
- `.agents/harness/delegation_validity.py` (chequeos V1–V5 convertidos en la
  «Gate Checklist» de la policy H15).
- `.agents/harness/RUNNER.md` (documento del runner eliminado).
- Suite de tests reducida al trío sobreviviente (`test_hook_gate.py`,
  `test_runner_state.py`, `test_health_probe.py`); los tests de los módulos
  eliminados y los invariantes documentales basados en ellos se eliminan — sus
  invariantes pasan a las checklists en prosa.

- `.agents/harness/decision_tree_evaluator.py` y los árboles TOML
  `.agents/orchestrators/*/harness/decision_trees/`; subcomandos `decide`,
  `features`, `health-check` y `metrics` de `runner.py`.
- `.agents/harness/feature_flags.py` (reemplazado por la documentación
  declarativa de `.agents/standards/INDEX.md`; los flags los resuelve el
  orquestador al evaluar H01).
- `.agents/harness/runner_metrics.py` (reemplazado por el procedimiento de
  agregación de `PROTOCOL_METRICS.md`).
- `.agents/harness/skill_validation.py` (su chequeo esencial queda plegado en
  `PROTOCOL_HEALTH.md`, ítem 7).
- `.agents/task.py` (utilidad de desarrollo sin referencias en el protocolo).
- Tests de los módulos eliminados (incluida la suite `test_recovery_tables.py`);
  los invariantes pasan a las checklists en prosa y a la suite reducida del
  trío sobreviviente.

### Fixed

- **Referencias residuales al runner eliminadas**: citas a
  `runner.py`/`runner_validators`/`delegation_validity.py` y suites de test
  inexistentes en H13, H15, S00, D00, D01, `PROTOCOL_TAXONOMY`,
  `PYTHON_DEPENDENCIES`, `standards/INDEX`, `skills/INDEX`,
  `terminology-enforcer` y `features.toml`, alineadas con la evaluación por
  juicio (auditoría de referencias, 10 ago 2026).

---

Nota: el tag git `2.0.0` que fija esta versión se crea como entregable del
release; la rama `dist` se regenera desde `master` por el workflow
`publish-dist`.

## [1.0.0] — 2026-08-05

Primera versión etiquetada del protocolo. Punto de corte validado por dogfooding
end-to-end (`plans/19-dogfooding-end-to-end.md`, Executed): health-check verde,
suite de tests verde (335 passed, 2 skipped), changelog retroactivo completo.
Origen del release: `plans/20-release-adoption.md`.

Esta entrada consolida retroactivamente toda la construcción previa del protocolo,
hasta entonces sin versionar. Las fechas internas son las de la historia de git.

### Added

- **Construcción del protocolo por dominios** (22 jul 2026): reestructura de
  `.agents/` en dominios de orquestación (`core`, `discovery`, `system`), con el
  orquestador central, el system agent y la máquina de estados. Origen: planes de
  construcción archivados (`plans/archive/PLAN_*_v1.md`, hoy solo en historia de
  git) y el merge `PLAN_ORCHESTRATORS_DOMAIN`.
- **Taxonomía del protocolo** (22 jul 2026): diccionario maestro
  `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, bloques de metadatos
  taxonómicos en los archivos del protocolo y policy de validación
  `.agents/harness/policies/H13-protocol-taxonomy.md`.
- **Discovery orchestrator** (22 jul 2026): subsistema de discovery con
  Knowledge Base en `.project/knowledge/`, contratos
  `.agents/orchestrators/discovery/contracts/`, enriquecimiento de la KB
  (`project_shape`, executive summary, API surface, file map; 24 jul) y estándar
  de curación con ciclo de vida `curation_status` (24 jul).
- **Mecanismo de skills** (25 jul 2026): estándar de skills (`SKILL.md` +
  `references/`), campo `skills` del contrato de delegación, selección por el
  orquestador y consumo por el worker, validación estructural en health-check.
  Diseño: `plans/skills-mechanism.md`; conceptualización posterior en RFC-00XX
  (`plans/rfc/00-skill-capability-model.md`) y RFC-00YM
  (`plans/rfc/15-skill-materialization-model.md`).
- **Estándares de contexto y perfiles** (18 jul 2026): estándar de artefactos de
  contexto `.agents/standards/context/PROJECT_ARTIFACTS.md` y perfiles de worker
  en `.agents/roles/profiles/`. Origen: `plans/archive/PLAN_05_CONTEXT_ENGINEERING.md`,
  `PLAN_06_PERFILES_WORKER.md`, `PLAN_07_ARTEFACTOS_CONTEXTO.md` (historia de git).
- **Serie de RFCs del Execution Context** (25 jul – 5 ago 2026): modelo
  conceptual completo del pipeline de contexto — RFC-00XY (Execution Context
  Model), RFC-00XZ (Assembly Process), RFC-00YA (Budget), RFC-00YB
  (Prioritization), RFC-00YC (Resolution), RFC-00YD (Composition) y sus
  especializaciones RFC-00YE…00YM (conflicto, desempate, merge, deduplicación,
  compresión, optimización, materialización, prompt rendering, skill
  materialization). Documentos en `plans/rfc/00`–`15`; trazabilidad de
  implementación en `plans/01`–`07`.
- **Explicitud de decisiones** (segunda serie, `plans/08`–`14`): corrección de la
  contradicción de bootstrap (08), catálogo de decisiones del Orchestrator y
  confianza unificada (09, RFC-17), taxonomía de fallos y recovery (10, RFC-18),
  validez de delegaciones y return reports (11, RFC-19), modelos de selección de
  perfil y skill (12, RFC-20/21), ciclo de vida de sesión e iteración (13,
  RFC-22), cumplimiento de flags `[declarative]` (14, RFC-23). Catálogo de gaps:
  `plans/analisis-explicitud.md`.
- **Policy layer y métricas** (tercera serie, `plans/15`–`17`): primera policy
  real del protocolo H15 (validez de delegaciones) y Budget materializado para el
  runtime prompt (15); policies de desempate, deduplicación, merge, compresión y
  optimización (16); modelo de métricas del protocolo (17).
- **Segunda materialización** (plan 18): materialización no-prompt del Execution
  Context (tool calls) en `runtime/`; tesis runtime-independent verificada.
- **Core Skills Pack** (`plans/21`–`22`, RFC-16
  `plans/rfc/16-core-skills-catalog-model.md`): catálogo núcleo de skills del
  protocolo en `.agents/skills/` implementado en dos tandas.
- **Versionado y adopción** (este release): `.agents/VERSION`, este
  `CHANGELOG.md`, `MIGRATION.md`, `ADOPTION.md` y plantillas de dominio en
  `.agents/standards/context/PROJECT_ARTIFACTS.md` §9. Origen:
  `plans/20-release-adoption.md`.

### Changed

- **Corrección transversal del 2 ago 2026**: política anti-alucinación aplicada a
  todo `plans/` — citas verificables `ruta:sección`, normalización de status
  (`Approved` → `Accepted`), versionado completo de `plans/` en git, eliminación
  de `plans/archive/` del working tree y frontera documental `.agents/` ↛
  `plans/`. Origen: commit `4109deb` y `plans/INDEX.md` §Convenciones.
- **Carga de skills** (4 ago 2026): la activación de skills se describe como
  lectura del worker, no como inyección en el prompt (fix documental en
  `.agents/skills/`).

### Removed

- `plans/archive/` eliminado del working tree (2 ago 2026); su contenido sigue en
  la historia de git (`git log --diff-filter=D -- plans/archive/`).
- Extractor Python `project_discovery` deprecado, reemplazado por el discovery
  orchestrator (22 jul 2026).

### Modelo conceptual

RFCs aceptadas que gobiernan esta versión: RFC-00XX y RFC-00XY…RFC-00YM (serie
Execution Context), RFC-16…RFC-23 (skills núcleo, decisiones del orquestador,
fallos, delegaciones, selección, ciclo de vida, flags declarativos). Índice
completo con status: `plans/INDEX.md` §Serie de RFCs.

---

Nota: el tag git `1.0.0` que fija esta versión se crea como entregable del release
(`plans/20-release-adoption.md`, entregable 5).
