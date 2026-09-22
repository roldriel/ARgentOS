# RFC-77 — Modelo de la capacidad Protocol-native de deliberación adversarial

**Status:** Accepted (2026-09-14)
**Fecha:** 2026-09-14
**Serie:** Adversarial Deliberation (Protocol) | —
**Change Level:** L2
**Origen:** Phase 1 del programa Jury Trial Protocol (informe de Fase 1, 2026-09-13/14, no persistido como artifact: sus hallazgos se citan por `ruta:sección` verificable); decisiones humanas D-01, D-02, D-05 y D-09 (2026-09-14); precedente de concepto Protocol-native durable de RFC-76 (`docs/rfc/76-change-governance-artifact.md`); evidencia de comportamiento del MVP DEV de deliberación adversarial (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`, planes 114/116/117)
**Pregunta:** ¿Cómo incorpora ARgentOS Protocol una capacidad de deliberación adversarial que produzca evidencia atribuida y un veredicto advisory sobre una decisión candidata, sin crear autoridad, sin crear una abstracción arquitectónica nueva y sin copiar la maquinaria del Change Lifecycle de DEV?
**Afectados:** `protocol/.agents/skills/adversarial-deliberation/SKILL.md` (nuevo); `protocol/.agents/contracts/DELIBERATION_REPORT.md` (nuevo); `protocol/.agents/skills/INDEX.md`; `protocol/.agents/orchestrators/core/roles/orchestrator.md`; `protocol/.agents/standards/orchestration/DECISIONS.md`; `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`; `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`; `protocol/.agents/VERSION`; `CHANGELOG.md`; `docs/MIGRATION.md`

> **Convención de evidencia:** las afirmaciones sobre el estado actual del repo se
> citan con `ruta:sección`. Las decisiones humanas ya aceptadas se marcan
> **Decisión (aceptada)**; los elementos fuera de alcance se marcan **DEFERRED**.

---

## Problema

ARgentOS Protocol posee mecanismos de **verificación** (`VERIFICATION_REPORT.md`,
gates H06/H07), de **review por rúbrica** (`REVIEW_REPORT.md` + review gate) y de
**decisión** (catálogo `D1`–`D6` en `protocol/.agents/standards/orchestration/DECISIONS.md`),
pero **no posee ningún concepto de deliberación adversarial**: una búsqueda
transversal sobre `protocol/.agents/` por `jury`, `deliberat`, `adversarial`,
`adversar` no devuelve ninguna coincidencia.

Las capacidades más cercanas no cubren el problema:

- El rol `reviewer` (`protocol/.agents/roles/reviewer.md`) evalúa un **artefacto de fase**
  contra una **rúbrica nombrada** de un catálogo cerrado de 19 rúbricas
  (`protocol/.agents/standards/quality/RUBRICS.md`), y su resultado es un **Gate State**
  (`review_passed`/`review_failed`) registrado en `HARNESS_REPORT.md`
  (`protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement`). No existe rúbrica aplicable a una
  **decisión candidata arbitraria**, y su vocabulario (`APPROVE`/`REWORK`/`NEEDS_CLARIFICATION`)
  es de routing, no de viabilidad.
- El skill `critic` (`protocol/.agents/skills/critic/SKILL.md`) declara la única postura
  adversarial del payload ("stress-test a proposal adversarially"), pero no declara
  compromiso previo a la revelación, ni procedencia entre pasadas, ni contrato de salida:
  su formato es prosa dentro de un artefacto del invocador.
- El skill `self-review` (`protocol/.agents/skills/self-review/SKILL.md`) aporta la
  disciplina de falsación, pero es el **propio autor** auditándose.
- El patrón de "dos reformulaciones independientes" existe una sola vez, dentro del perfil
  `intent_reflector` (`protocol/.agents/roles/profiles/intent_reflector.md:Self-consistency check`),
  atado a un artefacto y a una fase, sin semántica adversarial ni compromiso.

El resultado es que, ante una decisión con dos direcciones materiales posibles, el
Protocol sólo puede producir una evaluación única atribuida al mismo agente que la
propone. La evidencia de comportamiento del MVP DEV demostró que una segunda pasada
forzada a atacar, con la conclusión comprometida antes de la revelación, **revirtió el
veredicto** respecto de una sola pasada en la totalidad de los cuatro Trials ejecutados
(`docs/plans/114-adversarial-deliberation-mvp.md:Evidencia de valor`, pregunta 5;
`docs/plans/116-adversarial-deliberation-mvp-closure.md:Registro del Trial — Escenario A`).

Este problema no se resuelve con más verificación: por RFC-62 y RFC-65, la salida de una
evaluación LLM es `attestation` y **nunca** satisface un ítem `[gate]`
(`protocol/.agents/standards/quality/EVIDENCE.md:Sufficiency rules`); y la independencia
de verificación está clasificada como *dependiente de actores externos*
(`protocol/.agents/harness/INDEX.md:Guarantee catalog`). El gap es de **calidad de
decisión**, no de certificación.

---

## Decisión propuesta

Se incorpora al Protocol la capacidad **`adversarial-deliberation`** — nombre canónico del
payload. **`Jury Trial` es el nombre del programa/feature únicamente** y **no** nombra
ninguna entidad, clase, `kind`, estado, rol o registro arquitectónico.

La capacidad es la composición de cuatro elementos, **sin abstracción arquitectónica
nueva**:

1. **Una Skill de Protocol**: `.agents/skills/adversarial-deliberation/SKILL.md`.
   Materializa la disciplina de una pasada de evaluación atribuida (postura declarada,
   material recibido, material compartido, compromiso, conclusión, razones por criterio,
   premisas, supuestos, incertidumbres). El skill **describe una capacidad y no otorga
   autoridad ni permisos** (`protocol/.agents/standards/orchestration/SKILLS.md:Authority hierarchy`).
2. **Comportamiento del Orchestrator**: una subsección nueva en
   `.agents/orchestrators/core/roles/orchestrator.md` que declara la invocación con motivo
   registrado, la construcción de **Execution Contexts distintos por pasada**, la
   asignación de pasadas, la exigencia de compromiso previo a la revelación, la
   recolección de resultados atribuidos, la comparación por criterio, la preservación del
   desacuerdo, la síntesis, el veredicto, la recomendación opcional, la materialización del
   artefacto y la interpretación del veredicto como **recomendación advisory**.
3. **Un contrato de artefacto**: `.agents/contracts/DELIBERATION_REPORT.md`, que define el
   registro estructurado y verificable de la deliberación. El artefacto es
   **sesión-scoped**, **informational** y **sin lifecycle propio**.
4. **Registros mínimos**: taxonomía (`kind: artifact` + `kind: contract`), boundaries,
   índices de skills y contrato, y el punto de decisión conceptual `D7` en
   `DECISIONS.md`.

### `D7` — Invocación de deliberación adversarial

Se agrega un punto de decisión al catálogo conceptual existente
(`protocol/.agents/standards/orchestration/DECISIONS.md`), con la misma estructura que
`D1`–`D6`:

- **Pregunta:** ¿esta decisión candidata amerita una deliberación adversarial?
- **Inputs conceptuales:** existencia de al menos dos direcciones materiales posibles;
  incertidumbre real sobre la viabilidad; desacuerdo no resuelto; riesgo alto; evidencia
  ambigua; pedido explícito del humano.
- **Autoridad:** el Orchestrator decide y **registra el motivo**. El humano puede
  solicitarla. **No existe clasificador automático** y la capacidad **no se autoconvoca**.

### Flow canónico (procedimiento, no workflow)

```text
1  Question / decision frame
2  Evidence and context assembly
3  Deliberation assignment
4  Separate Execution Context construction
5  Independent-before-revelation analysis
6  Commitment
7  Revelation
8  Comparative criterion evaluation
9  Disagreement preservation
10 Synthesis
11 Verdict
12 Optional advisory recommendation
13 Orchestrator interpretation
14 Human / existing authority decision
15 Evidence persistence
```

Este flow es un **procedimiento implementado con mecanismos existentes**. **No** es una
fase de workflow, **no** es una máquina de estados y **no** introduce ningún estado nuevo.

### Vocabulario cerrado del veredicto

```text
VIABLE | NOT_VIABLE | UNDETERMINED
```

Razones de terminación:

```text
VERDICT | UNDETERMINED | LIMIT | NO_VALUE | FAILURE
```

El modo del MVP es **`viability`**. El modo `comparative` y su vocabulario
(`PREFERRED(A)` | `PREFERRED(B)` | `TIE`) quedan **DEFERRED**.

### Artefacto `DELIBERATION_REPORT.md`

Contrato con secciones obligatorias: `## Header` (protocol version, sesión, order cuando
las convenciones existentes lo exijan, nombre canónico del artefacto, tipo de deliberación,
motivo de invocación, decisión/pregunta, alcance); `## Context` (marco, referencias de
evidencia, material compartido, material por pasada); `## Pass 1` y `## Pass 2`
(atribución de ejecutor, `ejecutores`, material recibido, material retenido, análisis,
evaluación por criterio, compromiso); `## Revelation` (cuándo cada pasada conoció la
conclusión de la otra); `## Comparative evaluation` (por criterio: posición de cada pasada,
acuerdo/desacuerdo, evidencia, desacuerdo no resuelto); `## Synthesis` (preserva desacuerdo
material, distingue acuerdo de conflicto no resuelto, **no introduce hechos ni evidencia
nuevos**, identifica provenance); `## Verdict`; `## Recommendation` (opcional, clasificada
explícitamente como advisory); `## Orchestrator interpretation` (separada de las
conclusiones crudas; explica la interpretación, lo no resuelto, si requiere escalación y si
requiere decisión humana); `## Limitations` (provenance, independencia, contexto,
modelo/proveedor, reconstrucción, causalidad no observable).

### Independencia y procedencia

**Decisión (aceptada, D-05):** la independencia es una **condición de procedencia
declarada**, nunca una garantía epistemológica. Cada pasada declara
`ejecutores: mismo | distinto`, material recibido, material compartido, material retenido
hasta el compromiso, el punto de compromiso y si la conclusión de la otra pasada estuvo
disponible antes de comprometer la propia.

Se distinguen explícitamente tres niveles:

```text
execution attribution   ≠   procedural separation   ≠   epistemic independence
```

**PROHIBITED:** afirmar independencia "porque hubo dos pasadas", "porque se usaron prompts
distintos", "porque las salidas difieren", o presentar la deliberación como
**verificación independiente**. Ejecutores distintos son condición **necesaria y no
suficiente** para declarar `distinto`, y **nunca** suficientes para afirmar independencia
epistemológica. La ejecución en instancia única es admisible, pero **debe** declararse
`ejecutores: mismo` y su resultado se trata como `attestation`, no como verificación
independiente (coherente con RFC-62 y con
`protocol/.agents/harness/INDEX.md:Guarantee catalog`).

### Autoridad

**Decisión (aceptada, D-03):** el resultado de la deliberación es una
**attestation / recomendación advisory**. **Nunca** es verificación independiente,
autoridad normativa, decisión humana, autorización, resolución de finding, transición de
estado, autorización de release ni autorización de gobernanza.

```text
Deliberation ≠ Authority ≠ Human Decision ≠ Release Authority ≠ Governance Authority
Verdict ≠ Recommendation ≠ Decision
```

No se introduce **ninguna** authority class. El Orchestrator conserva la autoridad que ya
tenía (`D1`/`D2`); el humano conserva scope, abort, autorización normativa y release;
la autoridad de gobernanza existente no cambia.

### Contexto e identidad

**Decisión (aceptada, D-01/D-05):** el Orchestrator es el **único** constructor de
contexto; los Workers **no** construyen su propio contexto
(`protocol/.agents/roles/worker.md:Constraints`). Las dos pasadas comparten el mismo marco
de decisión y la misma base de evidencia, y sólo difieren en material declarado específico
de la pasada y en la postura. La segunda pasada **no** puede recibir la conclusión de la
primera antes de su propio compromiso. Si la implementación no puede garantizarlo, **se
registra la limitación explícitamente** en lugar de afirmar independencia.

No se crea ninguna **identidad nueva**: no hay `DeliberationIdentity`, `TrialIdentity` ni
`JuryIdentity`. La identificación del registro usa `execution_id = (session_id, iteration)`
(RFC-64) más el `<order>` del artefacto y etiquetas locales de pasada. No se modifican
`SemanticContextIdentity`, `SegmentIdentity` ni `MaterializationIdentity`, y no se
introduce ningún primitive de identidad. El Execution Context no posee identidad propia
(`docs/rfc/01-execution-context-model.md:Taxonomy Impact`).

### Invocación

**Decisión (aceptada, D-02/D-06):** la invocación es **explícita y controlada**. Se origina
en (a) un pedido explícito del humano, o (b) una decisión del Orchestrator con **motivo
registrado** en `SESSION_LOG.md`. **No** existe clasificador automático, routing
automático ni invocación autónoma. La capacidad **no** crea obligación, **no** es un gate y
**no** cambia estado.

### Persistencia y lifecycle

**Decisión (aceptada, D-10):** el artefacto es **sesión-scoped**, **inmutable dentro de la
sesión** e **informational**. Vive en
`.project/<session-uuid>/<iteration>/<order>-DELIBERATION_REPORT.md`, conforme a la Artifact
Safety Rule (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Artifact Safety Rule`),
siguiendo el precedente del artefacto de review (`protocol/.agents/roles/reviewer.md:Outputs`).
Hereda el **Artifact Lifecycle de RFC-63** (`draft → validated → superseded`), derivado del
registro de gates y nunca escrito por el autor. **No** tiene closure propio, **no** tiene
lifecycle propio, **no** tiene registry, **no** tiene ID global, **no** se crea categoría
durable en `.project/`, **no** se escribe en `.project/changes/` y **no** se introduce
cleanup automático, garbage collection ni scheduler de retención.

---

## Alcance

Cubre: el nombre canónico y el vocabulario del payload; la Skill y su disciplina de pasada;
el comportamiento de invocación y construcción de contexto del Orchestrator; el punto de
decisión `D7`; el contrato `DELIBERATION_REPORT.md` y sus secciones obligatorias; la semántica
de procedencia y la prohibición de afirmar independencia epistemológica; la frontera de
autoridad; la materialización sesión-scoped; la verificabilidad estructural y la suite de
tests; la relación con RFC-62/63/64/65/71/75/76 y con los contratos de Skill, Worker,
Orchestrator y Contexto; y el dogfood del propio Change.

No cubre (ver Non-Goals): confrontación, modo `comparative`, votación, N jurados, diversidad
obligatoria de modelo/proveedor, persistencia durable, registry, ID global, rol/perfil
nuevo, feature flag, gate, estado o fase nuevos, enforcement semántico, sandbox, telemetría,
economía, Prompt Cache, rediseño del Change Lifecycle y deduplicación cross-project.

---

## Alternativas consideradas

1. **Reusar `REVIEW_REPORT.md` y el review gate como artefacto canónico de deliberación.**
   Descartada. `REVIEW_REPORT.md` exige `## Rubric` de un catálogo cerrado de 19 rúbricas de
   artefactos de fase y prácticas técnicas (`protocol/.agents/standards/quality/RUBRICS.md:Rubrics`),
   y su resultado es un **Gate State** sobre el artefacto
   (`protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement`). Reusarlo obligaría a inventar una
   rúbrica de decisión, contaminaría el vocabulario de routing con un veredicto de
   viabilidad y convertiría una deliberación advisory en un gate. Viola el criterio C2 de
   no-duplicación de RFC-16 y crea autoridad donde no debe haberla.
2. **Crear un rol `deliberator` o un worker profile.** Descartada para el MVP. La vía de
   perfil exige siete pasos de wiring sancionados
   (`protocol/.agents/roles/profiles/README.md:How to add a new profile`) y un `kind: worker` en la
   taxonomía, y `H15` trata un perfil no resoluble como violación **F1 bloqueante**. No
   aporta ninguna capacidad que el skill más la delegación genérica no den. La
   **Decisión (aceptada, D-04)** ratifica que **no** se crea rol ni perfil
   (`jury_worker`, `jury_profile`, `adversarial_deliberator`, `juror_role` y equivalentes
   quedan prohibidos), y el Skill es el punto de extensión sancionado
   (`protocol/.agents/standards/orchestration/SKILLS.md`, `protocol/.agents/skills/README.md`).
3. **Crear una fase nueva del workflow o un estado `DELIBERATING`.** Descartada. Exigiría
   estado nuevo, transiciones, entradas en la máquina de estados, workflow module, contrato
   y registros, y cambiaría la superficie auditada de `state.json` (ST-005). Contradice el
   objetivo de no agregar estados y la prohibición de D-01.
4. **Crear un `kind` nuevo de taxonomía (p. ej. `kind: deliberation`).** Descartada. La
   taxonomía declara exactamente ocho `kind`
   (`protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, bloque `entities:`,
   campo `tags.kind`); `module`,
   `capability` y `facet` **no** son clases arquitectónicas del Protocol (`facet` tiene cero
   ocurrencias; `capability` aparece sólo como prosa en tres sentidos distintos). Un `kind`
   nuevo sería la abstracción nueva que D-01 prohíbe.
5. **Promover la Working Convention DEV a estándar del Protocol.** Descartada. Su banner
   declara sus `MUST`/`PROHIBITED` internos al experimento y sin carácter normativo
   (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`, banner
   «Declaración de naturaleza de sus reglas»),
   y RFC-75 `Dev vs Protocol` prohíbe mecanismos compartidos entre DEV y Protocol
   ("no se crean workflow/policy/state machine/artifact/skill compartidos; no hay herencia
   automática"). La convención DEV entra como **evidencia de comportamiento**, no como texto
   fuente.
6. **Implementar confrontación acotada en el MVP.** Descartada en esta ronda. Exige
   infraestructura de rondas, visibilidad mutua y criterio de terminación; su aporte
   observado en DEV fue precisar un criterio ya identificable. **DEFERRED** — requiere diseño
   propio.
7. **Implementar votación (mayoría, ponderada, consenso, ranking).** Descartada. Contaría
   pasadas como votos e ignoraría la calidad por criterio; DEV la excluyó por diseño y nunca
   la necesitó. La estrategia adoptada es juicio comparativo por criterio con desagregación
   preservada.
8. **Garantizar diversidad de modelo o proveedor.** Descartada por falta de base normativa:
   ninguna RFC ni ADR del repositorio gobierna la diversidad de modelo/proveedor para un
   segundo evaluador. **DEFERRED** y declarada como limitación.
9. **Implementar un gate propio para la deliberación.** Descartada. Convertiría una
   capacidad advisory en un control de hecho; y `ST-005` impide que un gate no-transicional
   se registre en `state.json`, con lo cual no bloquearía nada de todos modos. El artefacto
   nace `informational`.
10. **Gobernar la capacidad con una feature flag.** Descartada.
    `protocol/.agents/standards/orchestration/SKILLS.md:No feature flag` establece que el
    mecanismo de skills **no** se gobierna por flag porque un skill inactivo inyecta cero
    contexto y cero conducta; una flag sería un segundo gate sobre algo apagado por defecto.
11. **No hacer nada.** Descartada. El gap es real y está medido: el Protocol no tiene ningún
    mecanismo de deliberación adversarial, y la evidencia DEV muestra que la segunda pasada
    revirtió el veredicto en 4 de 4 Trials.

---

## Impacto en el protocolo

Cambio **aditivo compatible (MINOR)**. Se agregan:

| Path | Cambio |
|---|---|
| `protocol/.agents/skills/adversarial-deliberation/SKILL.md` | Nuevo. Skill con front matter (`name` == directorio, `description` con capacidad **y** condiciones de uso, `when_to_activate`, `when_not`), procedimiento, reglas, formato de salida, frontera de autoridad y requisitos de procedencia. |
| `protocol/.agents/contracts/DELIBERATION_REPORT.md` | Nuevo. Contrato con `schema_version`, bloque de metadata taxonómica, secciones obligatorias, vocabulario cerrado, reglas de decisión, invariantes y limitaciones. |
| `protocol/.agents/skills/INDEX.md` | Fila en el inventario. Sin fila en la tabla de activación: la candidatura es **por juicio**, vía `description` (no está atada a `fase + perfil`). |
| `protocol/.agents/orchestrators/core/roles/orchestrator.md` | Subsección nueva de invocación y construcción de contextos de deliberación, junto a las secciones de reviewer y context discoverer. |
| `protocol/.agents/standards/orchestration/DECISIONS.md` | Punto de decisión `D7 — Invocación de deliberación adversarial`. |
| `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` | Entidades `kind: artifact` y `kind: contract` para `DELIBERATION_REPORT.md`. Sin `kind` nuevo. |
| `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` | Declaración del artefacto y su ubicación sesión-scoped. |
| `protocol/.agents/VERSION` | `11.3.0` → `11.4.0` (MINOR; requiere confirmación del usuario para MINOR). |
| `CHANGELOG.md`, `docs/MIGRATION.md` | Entrada de versión y nota de migración. |
| `runtime/toolcalls/canonical.py` | `PROTOCOL_VERSION` (`check_version_state.py` lo exige). |

**No** se toca: `AGENT_STATE_MACHINE.md`; ningún `workflow/*.md`; ninguna
`harness/policies/H*.md` obligatoria; `runtime/toolcalls/` más allá del ancla de versión;
`SemanticContextIdentity`/`SegmentIdentity`/`MaterializationIdentity`; la maquinaria del
Change Lifecycle DEV; las RFC 62/63/64/65/71/75/76 (sólo cross-reference).

**Qué deja de ser válido:** nada. No se redefine ningún campo existente y no se rompe ningún
payload previo. La adición sigue el precedente de cambio **aditivo-optional** ya sancionado
para el campo `skills` (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:skills`).

**Deriva descriptiva NO corregida oportunistamente** (registrada como dependencia, no
resuelta aquí): la salida de `core:VERIFYING` en la taxonomía declara dos artefactos
mientras `workflow/07-verify.md` declara uno; y la tabla de activación de skills usa el
perfil `qa_engineer` para la fase 07 mientras el perfil por defecto de esa fase es
`verifier`. Ninguna de las dos afecta a la registración de esta feature.

---

## Relación con RFCs existentes

| RFC | Relación |
|---|---|
| **RFC-56** | Esta RFC es **Clase A** (modelo conceptual y contratos). Su materialización requiere RFC `Accepted` (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`). Una RFC en `Proposal` **no** habilita tocar el payload. |
| **RFC-62** | **Restringe.** La independencia de verificación es *dependiente de actores externos*; en instancia única se declara `attestation`. Esta RFC **no** reclama ninguna garantía que RFC-62 clasifique como no interna, y prohíbe explícitamente afirmar independencia epistemológica. |
| **RFC-63** | **Reutiliza.** El artefacto hereda el Artifact Lifecycle derivado (`draft → validated → superseded`) y no declara estados por escrito del autor. |
| **RFC-64** | **Reutiliza.** Identificación por `execution_id = (session_id, iteration)`; el actor se registra como `(role_id, mode)`; no se persiste identidad de instancia de worker, por lo que la procedencia `distinto` se declara, no se prueba por identidad. |
| **RFC-65** | **Restringe.** El veredicto es `attestation` marcada (actor + statement) y **no** satisface ningún ítem `[gate]`. Las reglas de suficiencia no se modifican. |
| **RFC-71** | **No se modifica.** No se crean segmentos, scopes ni identidades nuevas; no se altera la semántica de aislamiento ni de invalidación. |
| **RFC-75** | **Frontera.** Es el Change Lifecycle de DEV; esta feature no comparte mecanismo, workflow, policy ni state machine con él. Principios transferibles usados como principios, no como mecanismos: separación evidencia factual / autoridad normativa. |
| **RFC-76** | **Precedente directo.** Es el único ejemplo trabajado de concepto Protocol-native durable. Esta RFC imita su disciplina: reutilizar primitivas, no crear state machine/rol/registry/identity service, declarar `enforcement`, y listar lo diferido. A diferencia de RFC-76, esta feature **no** introduce categoría durable. |
| **RFC-16** | **Criterio de admisión.** C2 (no duplicación) se satisface: la capacidad no duplica el modelo de decisiones del Orchestrator ni el review por rúbrica; la deliberación usa el skill como sustrato de razonamiento y deja la decisión al Orchestrator. |
| **RFC-17** | **Extiende.** `D7` se agrega al catálogo conceptual existente con la misma estructura; la autoridad sobre recomendaciones no cambia. |
| **RFC-19** | **Sujeto.** Cada pasada es una delegación y queda sujeta a las condiciones de validez V1–V5. |
| **RFC-21 / RFC-24** | **Restringen la registración.** La `description` debe declarar capacidad **y** condiciones de uso (candidatura por juicio), y el skill necesita al menos un consumidor declarado (cable-or-kill). |
| **RFC-28** | **Obliga.** El contrato declara `enforcement: informational`; no hay tercer estado. |
| **RFC-50** | **Restringe.** Las mitigaciones de instancia única están `Accepted` con ejecución pendiente; esta RFC **no** diseña como si ya existieran y declara `ejecutores: mismo` en ese caso. |
| **RFC-57 / RFC-58** | **Delimitan.** El validador estructural cubre sólo el subconjunto `[gate]`; los ítems `[agent]` siguen siendo juicio. Esta feature no agrega trigger al validador. |
| **RFC-61** | **Precedente de invocación.** El trabajo no pedido con costo material requiere consentimiento por evento; aquí la invocación es explícita y con motivo registrado. |

---

## Compatibilidad y migración

Adición compatible MINOR. No se rompen contratos existentes, no se redefinen campos y no se
invalidan payloads previos. `MIGRATION.md` recibe una sección que declara: la capacidad nueva,
su nombre canónico, su frontera de autoridad y su carácter no obligatorio.

**VERSION:** el cambio es MINOR y requiere confirmación del usuario para la clasificación
(`docs/VERSIONING.md:3. Versionado`). El bump de `VERSION` y la nota de migración forman
parte del Definition of Done del plan; la **promoción y el tag son un acto separado** que
requiere autorización de release.

```text
MVP CLOSED != RELEASE AUTHORIZED
```

---

## Criterios de aceptación

- [ ] Existe `protocol/.agents/skills/adversarial-deliberation/SKILL.md` con front matter
      válido (`name` == directorio, `description` con capacidad **y** condiciones de uso,
      `when_to_activate`, `when_not`), procedimiento, frontera de autoridad y requisitos de
      procedencia; listado en `skills/INDEX.md`; referenciado por al menos un consumidor.
- [ ] Existe `protocol/.agents/contracts/DELIBERATION_REPORT.md` con las secciones
      obligatorias, el vocabulario cerrado del veredicto y de la razón de terminación, las
      reglas de decisión, los invariantes y las limitaciones; con `enforcement: informational`.
- [ ] `DELIBERATION_REPORT.md` está registrado en `PROTOCOL_TAXONOMY.md` como
      `kind: artifact` **y** `kind: contract`, con `produced_by`/`consumed_by` que resuelven
      a estados existentes, y declarado en `PROTOCOL_BOUNDARIES.md`.
- [ ] El Orchestrator declara la invocación con motivo registrado, la construcción de
      Execution Contexts distintos por pasada, la exigencia de compromiso previo a la
      revelación, y la interpretación del veredicto como recomendación advisory.
- [ ] `DECISIONS.md` contiene `D7` con pregunta, inputs conceptuales y autoridad, coherente
      con `D1`–`D6`.
- [ ] **No** existe ningún rol, perfil, `kind`, estado, fase, lifecycle state, authority
      class, registry, ID global ni primitive de identidad nuevos.
- [ ] **No** existe clasificador automático, feature flag, gate ni enforcement semántico.
- [ ] La suite de tests cubre contrato, skill, orquestación, autoridad, contexto y negativos
      (provenance faltante, `distinto` falso, afirmación de independencia epistemológica,
      compromiso faltante, filtración de la primera conclusión, veredicto malformado,
      decisión no autorizada, invocación recursiva, persistencia fallida).
- [ ] La batería canónica de verificación pasa; el validador estructural de taxonomía
      confirma coherencia.
- [ ] El dogfood se ejecutó sobre este mismo Change, gobernado por su Change Governance
      Artifact desde el inicio, y produjo un `DELIBERATION_REPORT.md` real.
- [ ] La reconstrucción por un tercero sin contexto conversacional es posible desde los
      artefactos persistidos, y las limitaciones de reconstrucción están declaradas.
- [ ] Las limitaciones están declaradas: sin independencia epistemológica, sin diversidad de
      modelo/proveedor garantizada, sin enforcement, sin telemetría, sin medición de costo,
      modo único, confrontación diferida, sin atribución causal.
- [ ] `JURY_TRIAL_PROTOCOL_MVP_CLOSED = J1 ∧ … ∧ J11` evaluado condición por condición con
      evidencia, y `MVP CLOSED != RELEASE AUTHORIZED` declarado.

---

## Non-Goals / DEFERRED

**Fuera del alcance de esta RFC:** confrontación y rondas de confrontación; modo
`comparative`; votación, mayoría, consenso, ranking, ponderación y quórum; N jurados
configurable; reputación o scoring de jurado; diversidad obligatoria de modelo o proveedor;
garantías de independencia epistemológica; afirmaciones de verificación independiente;
sandbox, ACL o aislamiento técnico; persistencia durable o global; registry; ID global de
Trial/Jury; máquina de estados; fase de workflow; estado; lifecycle state; gate propio;
enforcement semántico; clasificador automático o invocación autónoma; feature flag;
telemetría; optimización de costo o economía; implementación de Prompt Cache; rediseño del
Change Lifecycle; deduplicación cross-project; UI; scheduling a escala de producción;
importación de la maquinaria DEV (anchors, checkpoints, findings, corrections, pending,
series, DEV Change state machines).

**Explicitamente prohibido por esta RFC:** `JURY_TRIAL_REGISTRY`, `DELIBERATION_REGISTRY`,
`TRIAL_ID`, `JURY_ID`, `DeliberationIdentity`, `TrialIdentity`, `JuryIdentity`, `jury_worker`,
`jury_profile`, `adversarial_deliberator`, `juror_role` y equivalentes.

---

## Amendment Log

- 2026-09-14 — Creación como `Proposal` (Fase 2 del programa Jury Trial Protocol). Materializa
  las decisiones humanas D-01, D-02, D-03, D-04, D-05, D-06, D-10 y D-09; las decisiones D-07
  y D-11 quedan determinadas por D-02 (sin feature flag, sin gate). Pendiente: aceptación
  humana para pasar a `Accepted` y habilitar la modificación del payload (RFC-56 Clase A).
- 2026-09-14 — **Aceptación (H-1).** El mantenedor acepta RFC-77 **tal como está escrita**
  (`ACCEPTED AS WRITTEN`), sin rediseño ni ampliación de alcance. `Status` pasa de `Proposal`
  a `Accepted (2026-09-14)`, lo que habilita la modificación del payload por vía RFC-56 Clase A
  (`docs/CONVENTIONS.md:Convenciones`). La aceptación se registra junto con las decisiones
  H-2 (= D-12: `JURY_TRIAL_PROTOCOL_MVP_CLOSED = J1 ∧ … ∧ J11`, con `MVP CLOSED != RELEASE
  AUTHORIZED`), H-3 (= D-03: el resultado es `attestation`/recomendación advisory, nombre
  canónico `adversarial-deliberation`, sin authority class nueva) y H-4 (= D-10 residual:
  `DELIBERATION_REPORT.md` sesión-scoped, inmutable en la sesión, `informational`, con el
  artifact lifecycle existente y sin lifecycle, cleanup, GC ni persistencia global propios).
  Esta aceptación **no** autoriza release, tag, promoción a `master`, publicación, ni ningún
  elemento fuera del `## Alcance` de esta RFC.
