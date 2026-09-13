# Plan 120 — Materialización del MVP Protocol-native de deliberación adversarial

**Status:** Executed
**Fecha:** 2026-09-14
**RFC:** RFC-77 (`docs/rfc/77-protocol-native-adversarial-deliberation.md`)
**Clase:** A (toca `protocol/.agents/`; ver RFC-56)
**Change Level:** L2 (`max(coordination, scope, architectural impact, release impact, duration/complexity)`; RFC-75 Mecanismo 2)
**Depende de:** RFC-77 `Accepted` (2026-09-14; H-1) — satisfecho
**Origen:** Fase 2 del programa Jury Trial Protocol; informe de Fase 1 (`docs/rfc/77-protocol-native-adversarial-deliberation.md`); decisiones humanas H-1/D-01, H-2/D-12, H-3/D-03, H-4/D-10 residual, D-02, D-05, D-09 (2026-09-14)

> **Estado de autorización.** **H-5 = GO (mantenedor, 2026-09-14):** el Plan queda
> autorizado para ejecución — `Status` `Aprobado para ejecución` — con alcance limitado
> **exactamente** a los 14 entregables de `## Entregables`. La autorización **no** constituye
> autorización de release, tag, promoción a `master` ni publicación, y **no** implica
> `JURY_TRIAL_PROTOCOL_MVP_CLOSED = TRUE`: esa condición se demuestra mediante `J1..J11` y
> el acto de cierre correspondiente. Se confirma la clasificación **MINOR** `11.3.0` → `11.4.0`
> (`docs/VERSIONING.md:3. Versionado`).

---

## Objetivo

Materializar en `protocol/.agents/` la capacidad `adversarial-deliberation` definida por
RFC-77 como composición de una Skill nueva, una subsección de comportamiento del
Orchestrator existente, un contrato de artefacto nuevo (`DELIBERATION_REPORT.md`) y los
registros mínimos; verificar la materialización con la batería canónica y una suite de tests
propia; ejecutar el dogfood real sobre este mismo Change gobernado por su Change Governance
Artifact; verificar la reconstrucción por un tercero; y evaluar `J1..J11` con evidencia.

El Plan **no** crea ninguna entidad, `kind`, rol, perfil, fase, estado, lifecycle state,
authority class, registry, ID global ni primitive de identidad nuevos (D-01, D-02).

## Criterio de entrada

- [ ] RFC-77 figura como `Accepted (2026-09-14)` en su header y en `docs/rfc/INDEX.md` — **satisfecho**.
- [ ] Existe el Change Governance Artifact de este Change, materializado **antes** de cualquier cambio de payload — **satisfecho**: `.project/changes/ec7a9d8af8a08c467601edf907e4e593c5a2572032f81339eb52a688b47abe0b.md`.
- [ ] Baseline de verificación registrado: 6 checkers canónicos PASS y `python -m pytest tests/` = **535 passed / 0 failed**.
- [ ] `protocol/.agents/VERSION` leído: `11.3.0` (el bump previsto es MINOR → `11.4.0`, y **requiere confirmación del usuario** para la clasificación, `docs/VERSIONING.md:3. Versionado`).
- [ ] **Autorización de ejecución del Plan conferida por la autoridad humana** (`Status` → `Aprobado para ejecución`). **PENDIENTE.**

## Entregables

1. `protocol/.agents/contracts/DELIBERATION_REPORT.md` — nuevo contrato de artefacto (`enforcement: informational`).
2. `protocol/.agents/skills/adversarial-deliberation/SKILL.md` — nueva Skill de Protocol.
3. `protocol/.agents/skills/INDEX.md` — fila de inventario del skill (sin fila en la tabla de activación: candidatura por juicio).
4. `protocol/.agents/orchestrators/core/roles/orchestrator.md` — subsección de invocación y construcción de contextos de deliberación.
5. `protocol/.agents/standards/orchestration/DECISIONS.md` — punto de decisión `D7`.
6. `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` — entidades `kind: artifact` y `kind: contract` para `DELIBERATION_REPORT.md`.
7. `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — declaración del artefacto y su ubicación sesión-scoped.
8. `tests/test_adversarial_deliberation.py` — suite de contrato, skill, orquestación, autoridad, contexto y negativos.
9. `protocol/.agents/VERSION` — `11.3.0` → `11.4.0` (MINOR; sujeto a confirmación).
10. `runtime/toolcalls/canonical.py` — `PROTOCOL_VERSION` (lo exige `tools/check_version_state.py`).
11. `CHANGELOG.md` — sección `## [11.4.0] — <fecha>` con el ítem `(plan 120, RFC-77)`.
12. `docs/MIGRATION.md` — sección de migración de la versión MINOR.
13. `docs/plans/120-*.md` (este archivo) + `docs/plans/INDEX.md` — registro del Plan.
14. `.project/<session-uuid>/<iteration>/<order>-DELIBERATION_REPORT.md` — el artefacto real del dogfood (artefacto de sesión, no versionado).

## Pasos

1. **Autorización.** Verificar `Status: Aprobado para ejecución` y la autorización humana registrada. Sin ella, detenerse.
2. **Baseline.** `git status --short --branch`, `git rev-parse HEAD`, lectura de `protocol/.agents/VERSION`; registrar la clasificación (RFC-56 Clase A, Change Level L2).
3. **Contrato.** Crear `protocol/.agents/contracts/DELIBERATION_REPORT.md` con front matter `+++` (`schema_version`, `artifact`, `phase = "n/a"`, `produced_by = "orchestrator"`, `enforcement = "informational"`), bloque de metadata taxonómica (`kind: contract`, `domain: cross-cutting`, `artifact`, `lifecycle: null`, `produced_by`, `consumed_by`), y las secciones de RFC-77 `## Decisión propuesta` §"Artefacto `DELIBERATION_REPORT.md`" (RFC-77).
4. **Skill.** Crear `protocol/.agents/skills/adversarial-deliberation/SKILL.md` conforme al contrato de formato (`protocol/.agents/skills/README.md`): front matter con `name` == directorio, `description` con **capacidad y condiciones de uso** (RFC-21), `when_to_activate`, `when_not`; cuerpo con procedimiento, reglas, formato de salida, frontera de autoridad y requisitos de procedencia.
5. **Consumidor del skill.** Declarar la subsección del Orchestrator y/o la mención en `protocol/.agents/roles/worker.md`, satisfaciendo el requisito cable-or-kill (RFC-24).
6. **Registro del skill.** Añadir la fila al inventario de `protocol/.agents/skills/INDEX.md`.
7. **Comportamiento del Orchestrator.** Añadir la subsección de invocación de deliberación (motivo registrado; contextos distintos por pasada; asignación de pasadas; compromiso previo a la revelación; recolección atribuida; comparación por criterio; preservación del desacuerdo; síntesis; veredicto; recomendación opcional; materialización del artefacto; interpretación advisory) junto a las secciones existentes de reviewer y context discoverer.
8. **Punto de decisión.** Añadir `D7 — Invocación de deliberación adversarial` a `protocol/.agents/standards/orchestration/DECISIONS.md` con la estructura de `D1`–`D6`.
9. **Taxonomía y boundaries.** Registrar `DELIBERATION_REPORT.md` como `kind: artifact` y `kind: contract` en `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (con `produced_by`/`consumed_by` que resuelvan a estados existentes) y declararlo en `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`.
10. **Tests.** Crear `tests/test_adversarial_deliberation.py` cubriendo: contrato (payload válido; campos faltantes; provenance válida e inválida; veredicto válido e inválido; recomendación advisory), skill (descubribilidad, registro, front matter, consumidor, sincronía de INDEX), orquestación (dos pasadas; `mismo` y `distinto`; compromiso previo; ausencia de filtración; preservación del desacuerdo; síntesis; veredicto; recomendación opcional; interpretación), autoridad (el veredicto no transiciona estado, no satisface gate, no autoriza release, no se convierte en decisión normativa, no resuelve findings) y negativos (provenance faltante; `distinto` falso; afirmación de independencia epistemológica; compromiso faltante; filtración de la primera conclusión; veredicto malformado; decisión no autorizada; invocación recursiva; persistencia fallida).
11. **Versión.** Con confirmación humana de la clasificación MINOR: bump `protocol/.agents/VERSION` a `11.4.0`, `PROTOCOL_VERSION` en `runtime/toolcalls/canonical.py`, sección de `CHANGELOG.md` y sección de `docs/MIGRATION.md`.
12. **Validación.** Ejecutar la batería canónica (véase `## Verificación`) y la suite nueva.
13. **Dogfood real (D-09).** Verificar la legitimidad del Change bajo D-09; declarar el marco (problema, candidata, criterios obligatorios, modo `viability`, límites); registrar el motivo de invocación en `SESSION_LOG.md`; construir dos Execution Contexts distintos; ejecutar las dos pasadas atribuidas; registrar compromiso antes de revelación; revelar; comparar por criterio; sintetizar preservando el desacuerdo; emitir veredicto con base declarada y recomendación advisory separada; interpretar desde el Orchestrator; materializar el `DELIBERATION_REPORT.md`; registrar la decisión humana como acto separado o pendiente escalada (PC-1).
14. **Reconstrucción.** Verificar por un tercero (agente distinto, sin contexto conversacional) que el artefacto permite reconstruir los 15 puntos de RFC-77 `## Criterios de aceptación`, y declarar los límites de reconstrucción.
15. **Reevaluación de J1..J11** con evidencia por condición, sin redondear.
16. **Cierre.** Completar `## Validation anchor` (VC-1) y `## Checkpoint / cierre` (GC-1); correr C-1/C-2/C-3; evaluar `JURY_TRIAL_PROTOCOL_MVP_CLOSED`; registrar el acto humano de cierre si el lifecycle lo exige; declarar `MVP CLOSED != RELEASE AUTHORIZED`.

## Criterios de salida

- [ ] Los 14 entregables existen y son conformes a sus contratos.
- [ ] `check_protocol_invariants.py`, `check_plan_citations.py`, `check_plan_structure.py`, `check_taxonomy_coherence.py`, `check_session_artifacts.py` y `check_version_state.py` en verde.
- [ ] `python -m pytest tests/` sin regresiones respecto del baseline `535 passed / 0 failed`.
- [ ] **Cero** entidades, `kind`, roles, perfiles, fases, estados, lifecycle states, authority classes, registries, IDs globales o primitives de identidad nuevos; **cero** feature flag, gate, clasificador automático, voting, confrontación, Prompt Cache o rediseño del Change Lifecycle.
- [ ] El dogfood produjo un `DELIBERATION_REPORT.md` real con dos pasadas atribuidas, compromiso previo, procedencia, síntesis, veredicto, recomendación (si aplica) e interpretación del Orchestrator.
- [ ] La reconstrucción por un tercero está verificada y sus límites declarados.
- [ ] `J1..J11` evaluados individualmente con evidencia; ninguna condición redondeada.
- [ ] El acto humano de cierre registrado (J11); `MVP CLOSED != RELEASE AUTHORIZED` declarado.

## Verificación

Batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación`:

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

Más: H13 por juicio; gates de lifecycle C-1/C-2/C-3 (advisory/factuales, fuera de la batería y de CI); y la suite nueva `tests/test_adversarial_deliberation.py`.

Baseline declarado: 6/6 checkers PASS y **535 passed / 0 failed**. Cualquier fallo nuevo se trata como **regresión genuina**, salvo evidencia concreta en contrario.

## Validation anchor

- **Declared scope:** dos conjuntos declarados por separado.
  - **Superficie de contenido validada (S, 15 paths):** `CHANGELOG.md`, `docs/MIGRATION.md`, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/rfc/77-protocol-native-adversarial-deliberation.md`, `protocol/.agents/VERSION`, `protocol/.agents/contracts/DELIBERATION_REPORT.md`, `protocol/.agents/orchestrators/core/roles/orchestrator.md`, `protocol/.agents/skills/INDEX.md`, `protocol/.agents/skills/adversarial-deliberation/SKILL.md`, `protocol/.agents/standards/orchestration/DECISIONS.md`, `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, `runtime/toolcalls/canonical.py`, `tests/test_adversarial_deliberation.py`.
  - **Registro del cambio:** este Plan (el artifact que aloja este anchor). **Se declara fuera de S por construcción:** el anchor describe la identidad de la superficie de contenido, y no puede contener su propia identidad de contenido (auto-referencia no resoluble). El Plan es el registro del cambio, no el cambio. La superficie total del commit de cierre es la unión de ambos conjuntos: 16 paths.
- **Validation command-set:** la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + `python -m pytest tests/`.
- **Effective inputs (repo content):** el árbol staged de los 15 paths de S, más este Plan; el árbol resultante es `f1171b967385a41b0ae19319f2bb1ef056ca71cb`.
- **Observed dependencies:** `no instrumentado`.
- **Environmental factors:** Windows + OneDrive; Python 3.14; pytest 9.0.3; `git core.autocrlf=true` sin `.gitattributes` (los blobs se normalizan a LF en el índice); `.pytest_cache` no escribible (PermissionError preexistente y no relacionada — advertencia, no fallo).
- **Scoped Content Identity:**
  - State identity (estado validado = árbol de cierre): T1 = `27990f3da03ea969b88fc8fc6a545ac51325f600`.
  - Delta scoped identity (serialización `scoped-v1`, sobre S = los 15 paths de contenido ordenados, que excluyen este Plan): `5c93c9e55294c8c9538ec25d150854ddbf50fb30f6bbf698184cadea7ba3dc6d`.
  - **Nota de auto-referencia (declarada).** La State identity que este estándar define es el árbol del índice staged completo, que incluye el propio archivo que la registra: ningún archivo puede contener de forma consistente la identidad de contenido del estado que lo incluye. El valor T1 registrado arriba es por tanto el árbol del estado **inmediatamente anterior** a esta última escritura, no un punto fijo perfecto; se registra el valor real en lugar de un marcador, y la diferencia de una edición se declara aquí en vez de ocultarse. La identidad del estado de cierre se verifica de forma autoritativa desde el objeto del commit (`git rev-parse <commit>^{tree}`) y se persiste en el `closure_decisions[]` del Change Governance Artifact, que vive fuera del repositorio y por tanto fuera de la superficie hasheada. La delta de S sí es un valor estable y reproducible: editar este Plan no cambia ningún blob de S.
- **Validity / stale:** `vigente` — validación sobre el estado de contenido; el cierre se apoya en el `## Checkpoint / cierre`.

## Checkpoint / cierre

- **Commits de cierre:** **ninguno al momento de esta validación.** El Plan queda materializado y verificado en el working tree; el commit atómico de los 14 entregables es la acción de repositorio autorizada por H-6 y se realiza inmediatamente después de esta validación, que es por tanto la **validación del estado de cierre** (validar-then-commit). El commit resultante queda registrado en el `closure_decisions[]` del Change Governance Artifact (`.project/changes/ec7a9d8af8a08c467601edf907e4e593c5a2572032f81339eb52a688b47abe0b.md`), que es la fuente autoritativa del cierre de este Change.
- **Estado validado (ref al Validation anchor):** el `## Validation anchor` de este Plan (State identity T1 y delta de S registradas allí; ver la nota de auto-referencia).
- **Estado de cierre (tree id):** `27990f3da03ea969b88fc8fc6a545ac51325f600` — el árbol del estado validado, verificado desde el objeto del commit atómico de cierre (`git rev-parse <commit>^{tree}`) y persistido en el `closure_decisions[]` del Change Governance Artifact. Véase la nota de auto-referencia del anchor: por la imposibilidad de que un archivo contenga la identidad del estado que lo incluye, este valor corresponde al estado inmediatamente anterior a la última escritura de esta misma línea, y la diferencia de una edición se declara en lugar de ocultarse.
- **Consistencia checkpoint↔anchor:** **PASS** sobre la parte verificable: la delta de S registrada en el anchor es la del estado de contenido efectivamente validado, y el estado de cierre no difiere en ningún blob de S (el único cambio posterior a la validación es este registro, que vive fuera de S). La State identity del estado de cierre se verifica desde el commit y se registra en el `closure_decisions[]` del Change Governance Artifact.
- **Governance aplicada:** RFC-77 `Accepted` (H-1); autorización de ejecución del Plan (H-5) con alcance limitado a los 14 entregables; clasificación MINOR `11.3.0` → `11.4.0` confirmada; `CHANGELOG.md` y `docs/MIGRATION.md` actualizados; `VERSION` y `PROTOCOL_VERSION` bumpados; INDEX de planes y de RFC registrados.
- **Condición derivada:** **`Closed` (con release pendiente).** `Executed` (status) + gobernanza aplicada + checkpoint con consistencia anchor↔estado de cierre (PASS) + `JURY_TRIAL_PROTOCOL_MVP_CLOSED = TRUE` por el acto humano de cierre H-6 (2026-09-14). **`Closed ≠ Released`:** `MVP CLOSED != RELEASE AUTHORIZED`; sin tag `11.4.0`, sin push, sin promoción a `master`, sin publicación. El estado `Closed` es terminal para este Plan; los cambios posteriores son artifacts nuevos que lo referencian.


## Findings / Correcciones / Pending

### Pending decisions

- `<PLAN-120>` — decisión: **autorización de ejecución del Plan 120** (`Status` → `Aprobado para ejecución`); blocking: **sí** para toda materialización del payload; owner: mantenedor; escalación: mantenedor; resolución: **RESUELTA (2026-09-14) — H-5 = GO del mantenedor**: Plan autorizado para ejecución con alcance limitado a los 14 entregables de `## Entregables`; confirmada la clasificación MINOR `11.3.0` → `11.4.0`; la autorización no constituye autorización de release, tag, promoción ni publicación, y no implica `JURY_TRIAL_PROTOCOL_MVP_CLOSED = TRUE`; evidencia: `## Estado de autorización` de este Plan y la fila de `docs/plans/INDEX.md`; efecto downstream: habilita el Step 3 y siguientes, sin ampliar alcance.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Que el veredicto se consuma como autoridad (R1 de Fase 1) | Declaración explícita en el contrato + restricciones del skill + test negativo dedicado |
| Filtración de la conclusión de la primera pasada (R3) | Regla de composición de contexto + campo de material recibido por pasada + test negativo |
| Afirmación de independencia epistemológica (R2) | `ejecutores: mismo\|distinto` obligatorio + prohibición explícita + test negativo |
| Crecimiento de alcance "mientras estamos aquí" | Los 14 entregables son la superficie autorizada; cualquier path fuera de ellos detiene la ejecución |
| Clasificación MINOR sin confirmación | El bump de versión queda sujeto a confirmación humana explícita |

## Trazabilidad

Decisiones humanas H-1/D-01/D-02/D-03/D-04/D-05/D-06/D-09/D-10/D-12 (2026-09-14) → RFC-77 `Accepted` → este Plan 120 → 14 entregables → validación → dogfood → reconstrucción → `J1..J11` → acto humano de cierre → `JURY_TRIAL_PROTOCOL_MVP_CLOSED`. La release queda declarada como acto separado y no autorizado.

## Nota de ejecución

**2026-09-14 — ejecución del Plan 120 (H-5 = GO, alcance limitado a los 14 entregables).**

- **Intake y baseline:** `dev` @ `9572d2a`; working tree limpio salvo `.codegraph/` (untracked preexistente); `protocol/.agents/VERSION` = `11.3.0`; RFC-77 `Accepted (2026-09-14)`; CGA del Change materializado **antes** de la ejecución (`.project/changes/ec7a9d8af8a08c467601edf907e4e593c5a2572032f81339eb52a688b47abe0b.md`).
- **Steps 3–9 (materialización):** creado `protocol/.agents/contracts/DELIBERATION_REPORT.md` (secciones obligatorias, vocabulario cerrado, `DEL-001`…`DEL-012`, `enforcement: informational`); creado `protocol/.agents/skills/adversarial-deliberation/SKILL.md` (front matter con capacidad y condiciones de uso, procedimiento, reglas de seguridad, formato de salida, frontera de autoridad, referencias); registrado el skill en el inventario de `skills/INDEX.md` (sin fila en la tabla de activación: candidatura por juicio); añadida la subsección **§4.4 Deliberation Invocation** en `orchestrators/core/roles/orchestrator.md` (consumidor declarado del skill, requisito cable-or-kill de RFC-24); añadido el punto de decisión **`D7`** en `standards/orchestration/DECISIONS.md`; registradas las entidades `kind: artifact` y `kind: contract` de `DELIBERATION_REPORT.md` en `PROTOCOL_TAXONOMY.md` y su declaración como artefacto de sesión en `PROTOCOL_BOUNDARIES.md`.
- **Step 10 (tests):** creado `tests/test_adversarial_deliberation.py` — **75 tests** que codifican los invariantes del contrato como validador ejecutable (contrato, skill, orquestación, autoridad, contexto y negativos), con fixtures vendorizados para no depender del payload (`tests/AGENTS.md`). Autocontenido por construcción.
- **Step 11 (versión):** `protocol/.agents/VERSION` `11.3.0` → **`11.4.0`** (MINOR confirmado por H-5); `PROTOCOL_VERSION` en `runtime/toolcalls/canonical.py`; sección `## [11.4.0]` en `CHANGELOG.md`; sección `## 17` en `docs/MIGRATION.md`.
- **Step 12 (validación):** batería canónica **6/6 PASS**; `python -m pytest tests/` = **610 passed / 0 failed** (baseline 535 + 75 nuevos; **cero regresiones**). Se corrigieron 5 citas rotas introducidas por la materialización (en RFC-77 y en este Plan) y no se debilitó ningún checker.
- **Step 13 (dogfood real):** deliberación ejecutada sobre este mismo Change, con dos pasadas atribuidas y posturas declaradas (Pass 1 *sostener*, Pass 2 *atacar*), compromiso previo a la revelación, comparación por criterio, síntesis con desacuerdo preservado, veredicto `VIABLE` con base declarada, recomendación advisory separada e interpretación del Orchestrator. Artefacto: `.project/1fe5a73f-d064-4d1d-8f5c-9d8b0f2a7c31/01/09-DELIBERATION_REPORT.md`, conforme a `DEL-001`…`DEL-012`.
- **Step 14 (reconstrucción):** auditoría de reconstrucción por un tercero sin contexto conversacional. **Encontró cuatro defectos reales en el registro**, corregidos en una sección `## Corrections` propia del artefacto (no se alteró el veredicto, las evaluaciones por criterio, la síntesis ni el desacuerdo preservado): (C-1) `## Context` maldeclaraba el material por pasada; (C-2) el veredicto afirmaba una equivalencia no registrada por ninguna pasada; (C-3) **riesgo de contaminación entre pasadas subdeclarado** — Pass 2 recibió en su lista de contrato la ruta del `DELIBERATION_REPORT.md` **vivo**, que ya contenía la conclusión comprometida de Pass 1, y el Orchestrator no impidió la exposición; (C-4) el *carácter del resultado* de la sonda se usó en el razonamiento mientras el registro declaraba excluido el resultado. `C-3` es material: debilita `S-1` y convierte el artefacto en un ejemplo documentado del modo de fallo que `DEL-005` existe para prevenir.
- **Alcance:** `git status` contenido en los 14 entregables; **sin** entidad, `kind`, rol, perfil, fase, estado, lifecycle state, authority class, registry, ID global ni primitive de identidad nuevos; **sin** feature flag, gate, clasificador automático, voting, confrontación, telemetría, Prompt Cache ni rediseño del Change Lifecycle. `AGENT_STATE_MACHINE.md`, `workflow/**` y `harness/policies/**` sin cambios (verificado por `git diff --stat`).
- **Step 15 (J1..J11):** evaluados individualmente con evidencia. J1..J10 **TRUE** (contrato, capacidad, integración/lifecycle, autoridad, declaración de independencia, verificación, persistencia/reconstrucción, dogfood, descubribilidad, limitaciones declaradas). J11 **pendiente** del acto humano de cierre.
- **Step 16 (cierre):** **H-6 = acto humano de cierre (mantenedor, 2026-09-14)**: `JURY_TRIAL_PROTOCOL_MVP_CLOSED = TRUE` (J11 satisfecho por el acto), aceptación explícita de la limitación de contaminación entre pasadas del dogfood como limitación declarada del MVP — sin que el MVP pueda afirmar independencia epistemológica ni separación técnicamente garantizada —, aceptación de la corrección del artefacto y de la declaración de la limitación como evidencia válida, y constancia de que el hallazgo **no** autoriza enforcement adicional, aislamiento, sandbox, technical isolation, diversidad de modelo/proveedor ni confrontación. Registrada la `closure_decision` en el Change Governance Artifact (identidad preservada, re-materialización completa con historia acumulada). `Status` del Plan → **`Executed`**; condición derivada **`Closed` (con release pendiente)**. H-6 **no** constituye autorización de release: sin tag `11.4.0`, sin push, sin promoción a `master`, sin publicación.
- **Estado:** los 14 entregables materializados, verificados, dogfoodeados y cerrados. `JURY_TRIAL_PROTOCOL_MVP_CLOSED = TRUE`. `MVP CLOSED != RELEASE AUTHORIZED`: la release del payload permanece pendiente y no autorizada.

