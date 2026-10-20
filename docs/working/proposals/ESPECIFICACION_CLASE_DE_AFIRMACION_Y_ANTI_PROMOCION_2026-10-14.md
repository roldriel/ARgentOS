# Especificación — Clase de afirmación y regla anti-promoción (PRIORITY §0.1)

**Naturaleza documental:** Working / proposal — **no normativo**; puede ser provenance, nunca autoridad.
**Fecha:** 2026-10-14
**Origen:** `PRIORITY.md:0.1. Contrato de verdad de ARgentOS`
**Estado:** `PROPUESTA` — 0 cambios estructurales; ninguna fase autorizada ni ejecutada.
**Autoridad:** ninguna. Este documento no decide, no autoriza, no crea trabajo y no modifica ningún artefacto del repositorio.
**Destinatario declarado:** segunda opinión independiente (revisión adversarial) previa a solicitar autorización.

---

## 0. Cómo leer este documento

Este documento responde a `PRIORITY.md:0.1`, que pide identificar las afirmaciones fundamentales que ARgentOS hace sobre sí mismo, clasificarlas por naturaleza (`definición`, `comportamiento especificado`, `capacidad implementada`, `propiedad verificada`, `hipótesis`, `aspiración`, `evidencia experimental`) y poder determinar qué evidencia respalda cada una, **para evitar que documentación, diseño o lenguaje conceptual presenten como hechos capacidades no demostradas**.

Contiene: el problema (§1), el estado actual verificado (§2), la decisión de diseño y por qué descarta la lectura literal de §0.1 (§3), la especificación de los entregables (§4), la resolución de placement (§5), la autoridad requerida por fase (§6), el plan de verificación (§7), los contraargumentos y las condiciones de falsificación (§8), y las decisiones que quedan reservadas al mantenedor (§9).

**Qué NO es.** No es un Plan, no es una RFC, no es un ADR, no es normativo y no crea entidad, registry, namespace, lifecycle state, gate ni autoridad. No está aprobado.

**§8 existe para ser atacado.** Quien dé la segunda opinión debe empezar por §8.6.

---

## 1. Problema

### 1.1 El pedido, descompuesto

`PRIORITY.md:0.1` contiene cuatro preguntas distintas:

| # | Pregunta | Naturaleza |
|---|---|---|
| Q1 | ¿Cuáles son las afirmaciones fundamentales que ARgentOS hace sobre sí mismo? | inventario / alcance |
| Q2 | ¿Cómo se clasifica cada una **según su naturaleza**? (7 categorías) | vocabulario |
| Q3 | ¿Qué evidencia respalda cada una? | trazabilidad |
| Q4 | Evitar que documentación, diseño o lenguaje conceptual presenten como hechos capacidades no demostradas | **regla de conducta** |

Q4 es el objetivo declarado. Q1–Q3 son el instrumento propuesto. **Se puede satisfacer Q4 sin construir el artefacto que Q1–Q3 sugieren**, y §3 argumenta que conviene hacerlo.

### 1.2 Las siete categorías no son un solo eje

Leídas como clasificación única por afirmación, las siete categorías de §0.1 son mutuamente excluyentes de forma artificial: la misma afirmación puede ser especificada, implementada y verificada a la vez. Descompuestas, resultan **dos ejes de cuatro y tres valores**:

| Categoría de §0.1 | Eje |
|---|---|
| `definición` | **naturaleza** |
| `comportamiento especificado` | **naturaleza** |
| `hipótesis` | **naturaleza** |
| `aspiración` | **naturaleza** |
| `capacidad implementada` | **soporte** |
| `propiedad verificada` | **soporte** |
| `evidencia experimental` | **soporte** |

Falta un tercer eje que ARgentOS ya usa y §0.1 no nombra: **alcance** (`PROTOCOL` / `DEV` / `BOTH`), porque la misma afirmación puede pertenecer al producto o al repositorio que lo construye.

### 1.3 El fallo es empírico, no hipotético

Dos casos verificados:

1. **«Zero hallucinations» se presentaba como garantía y era una aspiración.** Registrado en `docs/working/audits/AUDITORIA_SISTEMA_2026-08-16.md:382`. La corrección **no** fue clasificarla: fue redefinirla operacionalmente — «every claim emitted by the protocol is evidence-cited, or explicitly marked as an attestation or inference» (`protocol/.agents/harness/INDEX.md:164`, §Claims rule).
2. **`ROADMAP.md` afirmaba «Trabajo activo: ninguno»** mientras el Plan 165 estaba `Aprobado para ejecución` con diseño sin commitear. Registrado en `docs/planificacion-argentos-diseno-2026-10-13.md:1298` (§K.10.5).

El caso 1 muestra además el patrón que funciona: **redefinir operacionalmente, no etiquetar**. El caso 2 muestra que el fallo ocurre en superficies de estado, no en registros.

---

## 2. Estado actual verificado

### 2.1 Vocabularios vigentes que ya clasifican afirmaciones

Ocho vocabularios solapados; ninguno subsume a otro.

| # | Vocabulario | Valores | Dónde | Ámbito |
|---|---|---|---|---|
| V1 | Clases de garantía | declarativa · verificable · mecánicamente enforceada · dependiente del juicio del agente · dependiente de actores externos | `protocol/.agents/harness/INDEX.md:100–110` (§Guarantee catalog) | Protocol; 12 garantías |
| V2 | Clases de evidencia | `observation` · `measurement` · `attestation` · `assertion` · `reference` | `protocol/.agents/standards/quality/EVIDENCE.md:11–25` | por criterio de sesión |
| V3 | Clases de claim | `verified` · `attested` · `inference` | `protocol/.agents/standards/quality/EVIDENCE.md:65–78` | por criterio de sesión |
| V4 | Invariante VERIFIED | `verified` ⇔ Gate PASS + evidencia de clase ≠ `attestation` | `protocol/.agents/standards/quality/EVIDENCE.md:80–91` | por criterio de sesión |
| V5 | `enforcement` (front matter) | `gated` · `informational` · `documented` | contratos del payload (front matter TOML) | por contrato |
| V6 | Niveles de madurez | `implementado` · `testeado` · `dogfoodeado` · `demostrado bajo condiciones reales` · `parcialmente demostrado` · `dependiente de una condición externa` · `no demostrado` · `limitado por un boundary conocido` | `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md:1.2` | por capacidad; 28 capacidades |
| V7 | Confianza | `HIGH` · `MEDIUM` · `LOW` | `protocol/.agents/standards/quality/CONFIDENCE.md` | por recomendación |
| V8 | Marcadores dispersos en prosa | `Future Extension` · `NOT_IMPLEMENTED` · `NOT_VERIFIED` · `hipótesis` · `declarativa` | sin dueño único | ambos |

### 2.2 Dónde llega cada uno y dónde no

V1–V5 **califican afirmaciones dentro de una sesión o de un Change**: criterios de aceptación, resultados de test, checks de gate, contratos. **Ninguno se aplica reflexivamente a las afirmaciones de ARgentOS sobre sí mismo.** V6 es el único intento de hacerlo para capacidades, y es un snapshot congelado de un Plan `Closed` (`docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md:Origen`), sin estado objetivo y sin definiciones, especificaciones, hipótesis ni aspiraciones.

**Hueco exacto:** no existe campo, archivo ni gate que clasifique una auto-afirmación del protocolo o del repositorio.

### 2.3 Hallazgos que condicionan el diseño

| ID | Hallazgo | Evidencia |
|---|---|---|
| **H-1** | Los dos entry points del payload — los archivos que todo adoptante y todo agente lee primero — **no llevan ninguna marca de clase**: enuncian en presente plano. | `protocol/_AGENTS.md:8` («delegates each phase to a worker»), `:43` («will not execute based on unconfirmed assumptions»); `protocol/.agents/INDEX.md:21` («The orchestrator will delegate each workflow phase to a **worker** invoked as a subagent»), `:25–29` («the only role authorized to…») |
| **H-2** | El payload **ya tuvo** un mecanismo para declarar una entidad cuya implementación no existe, lo **retiró** y **documentó la condición de reinstauración**. | `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:68–72`: «No entity carries `status: planned` anymore; if the mechanism is ever reintroduced, this rule is restored as: …» |
| **H-3** | «Verified» tiene **cuatro** significados vigentes. | V3 (`EVIDENCE.md:65–78`); `harness/INDEX.md:41–47` (checkers dev); `standards/runtime/PROTOCOL_METRICS.md:207–219` («corroborada por un segundo artefacto»); `standards/context/MEMORY_SYSTEM.md:81–86` (estado epistémico de un claim de KB) |
| **H-4** | El catálogo de garantías apunta en varias filas a verificadores **DEV-only**, que el payload declara que **nunca se entregan al adoptante**; la reformulación orientada al adoptante vive en `docs/ADOPTION.md` §6.4, que **no se distribuye**. | `harness/INDEX.md:112–125` (columna `Verified by`) + `:41–47` y `:49–62` (§Enforcement model, §Distribution boundary) |
| **H-5** | `G-001…G-005` / `ENF-001…003` se **citan** en archivos distribuidos y se **definen** sólo en `docs/rfc/62-guarantee-model-and-enforcement-boundaries.md:166–190`. Sustancia inline presente; hueco de **registro de IDs**. | `harness/INDEX.md:127–131`; `HARNESS_REPORT.md:105,113`; `METRICS.md:74`; `PROTOCOL_METRICS.md:228`; `PROTOCOL_HEALTH.md:40` |
| **H-6** | Los términos que §0.1 necesita están **indefinidos** en el glosario DEV: no hay entradas para `Claim`, `Guarantee`, `Evidence`, `Capability`, `Hipótesis`, `Aspiración`, `Invariant`, `Conformance`. | `docs/glossary/terms.md` (28 entradas) y `docs/glossary/INDEX.md:74–104` |
| **H-7** | El eje **alcance** de esta especificación depende de un vocabulario definido **sólo para el ROADMAP**, no canonizado como vocabulario general de dominio. | `docs/CONVENTIONS.md:785` (dimensión `Domain` del contrato del ROADMAP); `docs/planificacion-argentos-diseno-2026-10-13.md:1300` (R-7) |
| **H-8** | El propio payload declara límites honestos que los entry points no comunican: «This is the only machine-enforced part of the protocol»; `[gate]` items son «structurally checkable, not machine-enforced»; `HARNESS_REPORT.md` es «self-reported review trail, not independently verified evidence»; «hook systems are **fail-open**»; «There is no executable validation runner». | `harness/INDEX.md:27`, `:31–34`, `:415`, `:16` |

H-1 y H-8 juntos son el caso más claro del problema de §0.1: **el payload sabe y declara sus límites, pero no en el punto de lectura donde se forma la expectativa.**

---

## 3. Decisión de diseño

### 3.1 Por qué NO se crea un registro de afirmaciones

| # | Razón | Fundamento |
|---|---|---|
| 1 | **No tiene placement.** No existe familia DEV cuyo *kind* sea «registro de afirmaciones / garantías / capacidades». Resolverlo termina en `STOP (NEW FAMILY)` y exige enmienda de §6 por acto humano. | `docs/placement-contract.md:PC-10`, `:PC-19`, `:PC-20`; `docs/placement-contract.md:§8` |
| 2 | **El fallo está en la emisión, no en el inventario.** Un registro documenta la sobre-afirmación después de ocurrida; H-1 muestra que el daño ocurre en la superficie de lectura. | §2.3 H-1, H-8; §1.3 caso 2 |
| 3 | **Ya fue rechazado por diseño.** Un registro global de capacidades con estado mutable por fila es el registry que las reglas vigentes prohíben. | `docs/AGENTS.md:Do NOT`; `docs/AGENTS.md:Naturaleza documental` (`AU-4`); `docs/planificacion-argentos-diseno-2026-10-13.md:1113` |
| 4 | **Duplicaría §2 y §4 de PRIORITY.** El producto de §0.1 es insumo de la auditoría de coherencia («requisitos que no tienen evidencia», «evidencia que no está vinculada a una afirmación concreta») y del ciclo de conocimiento. Construirlo aislado crea la segunda estructura que esa auditoría debe detectar. | `PRIORITY.md:2`, `PRIORITY.md:4` |
| 5 | **El patrón que ya funcionó no fue etiquetar, fue redefinir.** Y el vocabulario para hacerlo a nivel de sesión ya existe completo (V2/V3/V4). | §1.3 caso 1; `harness/INDEX.md:164` |

### 3.2 Qué se propone en su lugar

**Una regla, una tabla de traducción y una corrección de superficies.** Nada nuevo más allá de tres entradas de glosario que hoy faltan y tienen autoridad resoluble.

El hallazgo H-6 determina el orden: **el primer entregable no es sobre afirmaciones, es sobre las palabras que las clasifican.** Tres de las siete categorías de §0.1 (`hipótesis`, `aspiración`, y la noción de `capability`) no tienen hoy definición normativa.

---

## 4. Especificación

Cinco entregables en la Fase 1 (docs-only, DEV) y tres cambios de payload en la Fase 2 (Clase A, condicional).

### 4.1 E-1 — La regla (Fase 1)

**Destino:** `docs/CONVENTIONS.md`, subsección nueva `### Regla transversal — clase de afirmación y anti-promoción`, **insertada entre la actual línea 531 (fin de «Regla transversal — Evidence closure / anti-rework») y la línea 533 (`### Change Lifecycle — Intake y clasificación`)**. Es el molde de las dos subsecciones `Regla transversal —` ya existentes (`docs/CONVENTIONS.md:484`, `:508`).

**Texto propuesto:**

> Una afirmación de ARgentOS sobre sí mismo se enuncia con **tres propiedades independientes**, nunca fusionadas:
>
> - **naturaleza** — qué clase de enunciado es: `definición` | `especificado` | `hipótesis` | `aspiración`.
> - **alcance** — de quién es la afirmación: `PROTOCOL` | `DEV` | `BOTH` | `UNKNOWN`.
> - **soporte** — qué la sostiene: `implementado` | `verificado` | `evidencia experimental` | `no demostrado`.
>
> Reglas:
>
> 1. Ninguna superficie de estado, diseño o documentación presenta como hecho una afirmación cuya naturaleza sea `hipótesis` o `aspiración`, ni cuyo soporte sea `no demostrado`, sin la marca explícita de su clase.
> 2. Una afirmación positiva requiere evidencia localizable (`ruta:sección`, comando, test anclado) o la marca de `attestation`/`inference` conforme a `protocol/.agents/standards/quality/EVIDENCE.md:Claim classes`. **La documentación explica una afirmación; no la sustituye.**
> 3. Toda afirmación de estado declara qué la **invalidaría**.
> 4. La ausencia de evidencia no se convierte en evidencia positiva. Un `GAP` es falta de información, nunca confirmación.
> 5. **Esta regla es DEV.** No gobierna `protocol/.agents/` (`docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera`; `docs/rfc/75-change-lifecycle.md:Dev vs Protocol`). El equivalente en el payload es la *claims rule* de `protocol/.agents/harness/INDEX.md:164`, que opera a nivel de sesión.
> 6. La regla no crea clase de cambio, estado de lifecycle, gate, checker, registry ni autoridad, y no obliga a etiquetar artefactos históricos (RFC-46).

**Justificación de cada regla:** 1 ← Q4 y §1.3; 2 ← V2/V3/V4 y `protocol/.agents/standards/quality/EVIDENCE.md:Sufficiency rules`; 3 ← necesario para que una clasificación no envejezca silenciosamente (§2.2, matriz congelada); 4 ← `.agents/policies` y `docs/behavior-patterns.md:La ausencia de evidencia nunca se convierte en evidencia positiva`; 5 ← frontera DEV/Protocol; 6 ← `AGENTS.md:Decision-Making Compass`.

### 4.2 E-2 — Descomposición en tres ejes y tabla de traducción (Fase 1)

**Destino:** la misma subsección de E-1, como contenido normativo. Sustituye la lectura literal de las siete categorías de §0.1 por dos ejes y las enruta a los vocabularios vigentes.

**Contenido propuesto (tabla):**

| Categoría de `PRIORITY.md:0.1` | Eje | Vocabulario vigente que la expresa | Dueño |
|---|---|---|---|
| `definición` | naturaleza | definición normativa del artefacto dueño + `docs/glossary/` (descriptivo, enruta) | estándares y contratos del payload |
| `comportamiento especificado` | naturaleza | V1 — clases de garantía `Declarative` / `Verifiable`; enunciados MUST y criterios EARS | `harness/INDEX.md:100–110` |
| `hipótesis` | naturaleza | V3 — `claim_class: inference` | `EVIDENCE.md:74–75` |
| `aspiración` | naturaleza | **sin vocabulario** → `GAP` declarado (§4.5) | — |
| `capacidad implementada` | soporte | V6 — nivel `implementado` | matriz Etapa A |
| `propiedad verificada` | soporte | V3 + V4 — `verified` bajo el invariante VERIFIED | `EVIDENCE.md:80–91` |
| `evidencia experimental` | soporte | V6 — `dogfoodeado` / `demostrado bajo condiciones reales` / `dependiente de una condición externa` | matriz Etapa A |
| — (eje ausente en §0.1) | **alcance** | `PROTOCOL` / `DEV` / `BOTH` | `docs/CONVENTIONS.md:785` (H-7: definido para el ROADMAP, **no canonizado** como vocabulario general) |

### 4.3 E-3 — Forma calificada inline (Fase 1)

**Destino:** la misma subsección de E-1. Gramática mínima para una afirmación, sin registro que la contenga:

```text
<afirmación>
  naturaleza: definición | especificado | hipótesis | aspiración
  alcance:    PROTOCOL | DEV | BOTH
  soporte:    implementado | verificado | evidencia experimental | no demostrado
  evidencia:  ruta:sección | comando | test anclado
  invalida:   la condición que la degradaría
```

**Regla de economía:** en prosa de estado, la marca es obligatoria **sólo** cuando `naturaleza ∈ {hipótesis, aspiración}` o `soporte = no demostrado`. Cuando la afirmación es `especificado` o `verificado` con evidencia citada, la cita misma es la marca. Esto acota el coste de la regla a los casos donde el fallo de §0.1 ocurre.

### 4.4 E-4 — Términos de glosario con autoridad resoluble (Fase 1)

Tres entradas nuevas, sólo para términos que hoy tienen `Authority Reference` resoluble. Cumplen el criterio de alta de `docs/glossary/INDEX.md:Cobertura y alta de entradas` (ambigüedad material + valor cross-layer).

**E-4a `Claim`** — en `docs/glossary/terms.md`, entre `## Change Lifecycle` (l. 41) y `## Checkpoint` (l. 52); fila correspondiente en `docs/glossary/INDEX.md` entre `Change Lifecycle` (l. 79) y `Checkpoint` (l. 80).

```markdown
## Claim

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** Protocol —
  `docs/rfc/65-evidence-and-verification-model.md:Terminology`;
  `protocol/.agents/standards/quality/EVIDENCE.md:Claim classes`
- **Qualification Rule:** `claim (report — clase V3)` vs `Claim (KB — entidad de
  knowledge)` (`protocol/.agents/standards/context/MEMORY_SYSTEM.md:Claim`) vs
  `check (fila de HARNESS_REPORT)`; calificar en texto cross-layer
- **Related Terms:** Evidence; Verification; Guarantee
- **Gloss (no normativo):** afirmación que se sustenta con evidencia de clase o
  se marca explícitamente como atestación o inferencia.
```

**E-4b `Evidence`** — entre `## EXECUTION_PLAN artifact` (l. 127) y `## Finding` (l. 136); fila entre `EXECUTION_PLAN artifact` (l. 87) y `Finding` (l. 88).

```markdown
## Evidence

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** Protocol —
  `docs/rfc/65-evidence-and-verification-model.md:Terminology`;
  `protocol/.agents/standards/quality/EVIDENCE.md:Evidence classes`
- **Qualification Rule:** `evidence entry (con clase V2)` vs `evidence field
  (texto libre)` vs `evidencia factual (output de checker DEV, no autoridad)`
  (`docs/CONVENTIONS.md:Regla transversal — target semantics vs
  operationalización`)
- **Related Terms:** Claim; Verification; Guarantee
```

**E-4c `Guarantee`** — entre `## Glossary` (l. 148) y `## INDEX` (l. 158); fila entre `Glossary` (l. 89) y `INDEX` (l. 90).

```markdown
## Guarantee

- **Scope:** Protocol
- **Status:** current
- **Authority Reference:** `docs/adr/01-guarantee-model.md:Decisión`;
  `docs/rfc/62-guarantee-model-and-enforcement-boundaries.md:Invariants`;
  `protocol/.agents/harness/INDEX.md:Guarantee catalog`
- **Qualification Rule:** `guarantee class (5 valores)` vs `garantía ofrecida
  (fila del catálogo)` vs `no-garantía declarada`
- **Related Terms:** Claim; Evidence
- **Gloss (no normativo):** propiedad que el protocolo ofrece, clasificada por
  quién la verifica.
```

Orden de inserción alfabético, siguiendo el orden aproximado del registro vigente (que ya tiene excepciones: `ROADMAP` antes de `Protocol`).

### 4.5 E-5 — `GAP` declarado de términos sin autoridad (Fase 1)

Los siguientes términos se usan como si fueran normativos y **no tienen hoy `Authority Reference` resoluble**; la regla D2 prohíbe crear la entrada sin ella. La misma subsección de E-1 los declara `GAP`:

| Término | Por qué es `GAP` |
|---|---|
| `Hipótesis` | tiene referencias en prosa (p. ej. `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md`, `:729` «es una hipótesis de diseño, no un hecho») pero ninguna definición normativa del concepto |
| `Aspiración` | idem; su única formulación operativa es la negación («zero hallucinations no es una garantía técnica») |
| `Capability` | el término se usa en `ROADMAP.md`, la matriz de Etapa A y el informe de planificación como si fuera normativo; su vocabulario de dominio (`PROTOCOL`/`DEV`/`BOTH`) está definido **sólo** para el ROADMAP — es el mismo `GAP` que R-7 (`docs/planificacion-argentos-diseno-2026-10-13.md:1300`) |
| `Invariant` | tiene **instancias** normativas (`G-001…G-005` en `docs/rfc/62-…md:166–190`; `EV-001…EV-004` y `REL-001…REL-003` en `protocol/.agents/standards/quality/EVIDENCE.md:100–114`) pero ninguna definición del concepto |
| `Conformance` | sin uso normativo en el repositorio; pertenece al ámbito de `PRIORITY.md:25` |

**Consecuencia declarada:** mientras estos términos sean `GAP`, el eje **alcance** de E-1 se aplica con la semántica del contrato del ROADMAP (`docs/CONVENTIONS.md:785`) y **no** con un vocabulario de dominio canonizado. Esta especificación **no** propone canonizarlo: es la decisión D-1 de `docs/planificacion-argentos-diseno-2026-10-13.md:1281`, reservada al mantenedor.

### 4.6 E-6 — Marca de aspiración en el Destino (Fase 1)

**Destino:** `ROADMAP.md` §Destino (`:9–22`).

**Cambio propuesto:** una línea que declare explícitamente que el Destino es **aspiración y dirección**, no una afirmación de capacidad demostrada, citando la regla de E-1. Modelo ya existente en `AGENTS.md:Decision-Making Compass`: «That is the direction and the evaluation objective — not a claim that ARgentOS has already demonstrated it».

**Por qué:** H-2 y §1.3 caso 2 muestran que los fallos ocurren en artefactos de dirección y estado, no en registros.

### 4.7 E-7 — Cambios de payload (Fase 2, condicional, Clase A)

No se proponen como parte de la Fase 1 y requieren RFC `Accepted`. Se registran aquí para que la decisión de alcance sea informada:

| # | Cambio | Destino | Resuelve |
|---|---|---|---|
| E-7a | Marcar clase en los entry points: distinguir allí lo especificado, lo implementado y lo condicional | `protocol/_AGENTS.md`, `protocol/.agents/INDEX.md` | H-1, H-8 |
| E-7b | Añadir al catálogo de garantías las columnas de **evidencia**, **invalidación** y **no garantiza** | `protocol/.agents/harness/INDEX.md:112–125` | H-4 parcialmente; §0.1 Q3 |
| E-7c | Resolver la columna `Verified by` cuando apunta a verificadores DEV-only, o declarar explícitamente que el adoptante no puede ejecutarlos | `protocol/.agents/harness/INDEX.md:112–125` | H-4 |

**Condición de entrada de la Fase 2:** que la Fase 1 esté materializada, porque la Fase 1 fija el vocabulario que el RFC va a usar. Y el payload no puede depender de DEV (`docs/adr/18-...md:RS-10`; `docs/placement-contract.md:PC-37`).

---

## 5. Placement

Resuelto con `docs/placement-contract.md:§5–§7`. **Ninguna pieza de la Fase 1 requiere familia nueva ni enmienda de §6.**

| Pieza | Familia (§6) | Namespace canónico | Canonicality | Autoridad / lifetime |
|---|---|---|---|---|
| E-1 regla, E-2 tabla, E-3 forma, E-5 `GAP` | Normative policy | `docs/CONVENTIONS.md` | `source-of-truth` | Policy activa; se enmienda en sitio |
| E-4a/b/c entradas + filas de INDEX | Inventory / descriptive registry | `docs/glossary/terms.md` + `docs/glossary/INDEX.md` | `source-of-truth` | descriptivo, nunca autoridad |
| E-6 | Root-anchored EntryPoint (no familia) | `ROADMAP.md` | `source-of-truth` | EntryPoint |
| Plan que autoriza la Fase 1 | Plan | `docs/plans/NN-<slug>.md` | `source-of-truth → historical` | se congela al `Executed` |
| E-7a/b/c | Payload spec/capability | `protocol/.agents/...` | `source-of-truth` | RFC-56 Clase A |
| Este documento | Working analysis | `docs/working/proposals/` | `source-of-truth` | Working; no normativo |

**`STOP` declarados (no resueltos aquí, requieren acto humano):**

| `STOP` | Objeto | Regla |
|---|---|---|
| `NEW FAMILY` | una superficie de afirmaciones («registro de garantías/capacidades/afirmaciones») | `PC-10`, `PC-20` — enmienda de §6 |
| `AMBIGUOUS KIND` / a resolver con el mantenedor | hogar de `PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md`: la familia es Working analysis, pero `PRIORITY.md` es una directiva de priorización y no encaja limpiamente en `docs/working/{audits,research,proposals}/` | `PC-11`, `PC-19` |
| `AUTHORITY UNRESOLVED` | canonización del vocabulario de dominio (`PROTOCOL`/`DEV`/`BOTH`), de la que depende el eje alcance de E-1 | `PC-23`; ADR-16 `AU-3`; D-1 del informe de planificación |

**Verificado como no-problema:** ninguna pieza de la Fase 1 afecta lo que reciben los adoptantes (`§11`), no crea dependencia del payload respecto de DEV, y no requiere INDEX universal (`PC-63`) salvo la fila de glosario que la propia familia exige.

---

## 6. Autoridad y clases de cambio (RFC-56)

| Fase | Contenido | Clase | Autorización requerida |
|---|---|---|---|
| **Fase 0** | Verificaciones factuales: por qué se retiró `status: planned` (H-2); desambiguar las cuatro acepciones de «verified» (H-3); dimensionar las afirmaciones de los entry points (H-1) | sin cambio | ninguna — es análisis |
| **Fase 1** | E-1…E-6 | **Clase B** (mejora documental, sin efecto payload) | Plan **`Aprobado para ejecución`** |
| **Fase 2** | E-7a/b/c | **Clase A** (modelo/contratos del payload) | **RFC `Accepted`** + plan |
| **Fase 3** | Superficie de estado de capacidad / afirmaciones | acto humano | acto de autoridad; `PC-20` si crea familia |
| **Fase 4** | Checker | diferido | — |

**Restricción explícita:** la Fase 1 **no** modifica `protocol/.agents/`, `runtime/`, `tools/` ni `tests/`.

---

## 7. Plan de verificación

**Fase 1** — la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` en su totalidad (nueve checkers + ambas suites de tests), más verificación específica:

| # | Verificación específica | Método |
|---|---|---|
| V-1 | Las tres entradas de glosario apuntan a un `Authority Reference` **resoluble** | resolución manual de cada `ruta:sección` citada + el checker de coherencia de taxonomía de la batería |
| V-2 | Cada entrada nueva tiene su fila en `docs/glossary/INDEX.md` **en el mismo cambio** | diff del cambio |
| V-3 | Ninguna definición normativa se duplica en el glosario (regla D2) | lectura de las tres entradas contra sus fuentes |
| V-4 | La subsección nueva no afirma autoridad sobre el payload | lectura contra `docs/rfc/75-change-lifecycle.md:Dev vs Protocol` |
| V-5 | `git diff --name-only` ⊆ el `Scope` declarado del Plan | comparación con `## Alcance` |
| V-6 | 0 diff en `protocol/`, `runtime/`, `tools/`, `tests/` | `git diff --name-only` |

**No verificable mecánicamente en la Fase 1 (declarado):** que la regla de E-1 se *cumpla* en la prosa del repositorio. Es juicio; su verificabilidad mecánica es la Fase 4 y está diferida deliberadamente (precedente: el campo `Avanza:` en `docs/planificacion-argentos-diseno-2026-10-13.md:1171`).

**Límite de verificación de este propio documento (verificado, no supuesto):** `tools/check_plan_citations.py:scan_documents` (`:194–210`) recorre únicamente `docs/plans/`, `docs/rfc/`, `docs/adr/` y los `ROOT_DOCS`; **no** recorre `docs/working/`. Las ~40 citas `ruta:sección` del Anexo A de este documento **no están cubiertas por ningún checker**, y su verificación fue manual. Ejecutado el checker sobre el estado de este cambio: `Broken citations: 26` + `Legacy references from live sources: 1`, **idéntico al baseline preexistente** — este cambio no rompió ninguna cita, y tampoco puede ser validado por él. `tools/check_taxonomy_coherence.py` pasa (`Taxonomy coherence OK`, exit 0). Es una instancia menor del problema de §0.1: afirmaciones fuera de la superficie verificada.

**Fase 2** — la batería canónica + `python -m pytest protocol/.agents/harness/tests/` + `tools/check_protocol_invariants.py --payload protocol .` en verde, dado que la Fase 2 toca el payload.

---

## 8. Contraargumentos y condiciones de falsificación

Se enuncian con la respuesta provisional de este documento. **§8.6 es el punto de entrada para la segunda opinión.**

### 8.1 «Esto es burocracia: una regla más que nadie va a aplicar»

**Respuesta provisional:** la regla no crea obligación universal — E-3 la acota a los casos donde `naturaleza ∈ {hipótesis, aspiración}` o `soporte = no demostrado`. Es una regla de excepción, no un formulario. **Réplica posible:** aun así requiere que un agente decida la clase de cada afirmación, y esa decisión es juicio no verificable (declarado en §7). Si eso se considera inaceptable, la alternativa es la opción «no crear nada» y limitarse a corregir las afirmaciones falsas — que deja Q1 y Q3 sin responder.

### 8.2 «Es un registro encubierto»

**Respuesta provisional:** no hay registro: E-2 es una tabla de **traducción** (estable, no crece con el corpus) y E-3 una gramática; ni una ni otra enumeran afirmaciones concretas. **Réplica posible:** la tabla de E-2 podría crecer hasta funcionar como registro de facto si cada categoría se subdivide. **Condición de falsificación:** si al implementar E-2 aparece la tentación de añadir filas por afirmación en lugar de por categoría, la objeción es correcta y el diseño debe cambiar.

### 8.3 «La regla no es determinable por un tercero»

**Respuesta provisional:** es correcto y está declarado. El objetivo de Q4 se satisface *reduciendo* la sobre-afirmación, no *prohibiéndola mecánicamente*. **Réplica posible:** sin determinabilidad, la regla tiene la misma debilidad que `Roadmap impact` —27 aplicaciones en prosa, sin checker, cuatro decisiones humanas derivadas (`docs/planificacion-argentos-diseno-2026-10-13.md:1297`). **Es la objeción más fuerte de este documento.** Si se acepta, la consecuencia es que la Fase 4 (checker) no debería diferirse tanto, o que la Fase 1 no debería aprobarse sin un criterio de admisión determinable.

### 8.4 «Toca el payload sin necesidad»

**Respuesta provisional:** la Fase 1 no toca el payload; la Fase 2 es condicional y posterior. **Réplica posible:** el problema más agudo (H-1) está **en** el payload, de modo que una solución que difiere la Fase 2 deja el caso principal sin resolver. Es correcto: la Fase 1 mejora la capacidad de *nombrar* el problema; la Fase 2 lo corrige en el punto de lectura. El orden es deliberado, no una postergación.

### 8.5 «Duplica el modelo de confianza del protocolo»

**Respuesta provisional:** E-1 enruta a V2/V3/V4 en vez de redefinirlos, y su regla 5 declara que es DEV y no gobierna el payload. **Réplica posible:** usar en DEV los mismos nombres (`verificado`, `atestación`, `inferencia`) que el payload define para sesiones crea colisión de vocabulario cross-layer, que D5 obliga a calificar. **Si la objeción se acepta**, la corrección es calificar cada uso (`clase de afirmación (DEV)` vs `claim_class (Protocol)`) — lo que debe incorporarse a E-1 antes de aprobar.

### 8.6 Cómo refutar esta especificación

Los siguientes enunciados, si se verifican, **invalidan** la propuesta y deben comprobarse antes de aprobarla:

| # | Enunciado cuya verdad invalidaría la propuesta | Cómo comprobarlo |
|---|---|---|
| F-1 | Ya existe un artefacto que enumera y clasifica las afirmaciones de ARgentOS sobre sí mismo con su evidencia | búsqueda de un registro equivalente en `docs/`, `protocol/.agents/` y `docs/working/` |
| F-2 | El vocabulario de §0.1 ya está definido en algún estándar del payload y este documento lo ignora | lectura completa de `protocol/.agents/standards/` (34 archivos) buscando definiciones de definición/especificación/hipótesis/aspiración |
| F-3 | El fallo que §1.3 documenta ya no ocurre: las superficies de estado no sobre-afirman | auditar `ROADMAP.md`, `README.md`, `protocol/_AGENTS.md`, `protocol/.agents/INDEX.md` contra el estado real del repositorio |
| F-4 | E-1 es redundante con la *claims rule* del payload, que ya se aplica al material DEV | verificar si algún artefacto DEV invoca `protocol/.agents/harness/INDEX.md:164` como norma propia |
| F-5 | Las tres entradas de E-4 no cumplen el criterio de alta del glosario (ambigüedad material, significado de gobernanza o valor cross-layer) | `docs/glossary/INDEX.md:Cobertura y alta de entradas` |
| F-6 | Existe un hogar ya resuelto para una superficie de afirmaciones que evita el `STOP (NEW FAMILY)` | resolución de placement con `docs/placement-contract.md:§7` sobre una descripción alternativa del artefacto |

**F-3 es la verificación más barata y la más decisiva.** Si las superficies no sobre-afirman hoy, el problema de §0.1 es de riesgo futuro y no de daño presente, y la prioridad relativa de esta propuesta cambia.

---

## 9. Decisiones reservadas al mantenedor

| # | Decisión | Opciones |
|---|---|---|
| **D-A** | ¿Se aprueba la Fase 1 tal como está especificada? | (a) sí, completa; (b) sí, sólo E-1+E-2 sin glosario; (c) sí, sólo corrección de afirmaciones falsas; (d) no |
| **D-B** | ¿Se aprueba la Fase 2, y con qué alcance? | (a) sí, E-7a+b+c; (b) sólo E-7a (entry points); (c) diferir hasta ver la Fase 1 materializada |
| **D-C** | ¿Se canoniza el vocabulario de dominio (`PROTOCOL`/`DEV`/`BOTH`) del que depende el eje alcance? | (a) canonizar; (b) redefinir en dos capas; (c) suprimir; es D-1 de `docs/planificacion-argentos-diseno-2026-10-13.md:1281` |
| **D-D** | ¿Se crea alguna vez una superficie de afirmaciones? | (a) no; (b) sí, acotada a garantías y capacidades P; (c) sí, como sección de un artefacto existente; es D-2/D-3 de `docs/planificacion-…md:1282–1283` |
| **D-E** | ¿Se reinstaura el marcador de estado de implementación retirado por H-2? | (a) no — prosa calificada + catálogo de garantías; (b) sí, con la condición documentada en `H13:71–72`; (c) otra forma |
| **D-F** | Hogar de `PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md` | (a) `docs/working/proposals/`; (b) otro subdirectorio Working; (c) permanecen sin trackear (**recomendado no**: precedente `MASTER_PENDING_WORK_INVENTORY.md`, y el incidente del Apéndice 2 de ese informe) |

---

## 10. Fuera de alcance

- El modelo de fallos (`PRIORITY.md:0.3`), los invariantes y sus tests (`:0.2`), la auditoría de coherencia global (`:2`), DEV Memory (`:4`) y la revisión de RFC-56 (`:3`). Esta propuesta produce **insumos** para ellos y no los preempta.
- El modelo de garantías del payload más allá de H-4: no se propone cambiar las cinco clases ni las doce garantías.
- La reconciliación del layout del payload (`protocol/.agents/INDEX.md:5` nombra `.argentos/.agents/INDEX.md` mientras `protocol/_AGENTS.md:7` nombra `.agents/...`): pertenece al plan 156 y se registra aquí sólo como observación.
- `docs/behavior-patterns.md`, `docs/VERSIONING.md` y el enforcement de placement (`docs/placement-contract.md:Enforcement deferred`).

---

## Anexo A — Trazabilidad de las afirmaciones de este documento

| Afirmación | Evidencia |
|---|---|
| §0.1 pide clasificar por naturaleza y determinar evidencia | `PRIORITY.md:23–37` |
| Las siete categorías están enunciadas literalmente | `PRIORITY.md:27–34` |
| V1 cinco clases de garantía | `protocol/.agents/harness/INDEX.md:100–110` |
| V1 doce garantías con columna `Verified by` | `protocol/.agents/harness/INDEX.md:112–125` |
| V1 `ENF-001/002/003` | `protocol/.agents/harness/INDEX.md:127–131` |
| Claims rule | `protocol/.agents/harness/INDEX.md:164–173` |
| V2/V3/V4 | `protocol/.agents/standards/quality/EVIDENCE.md:11–25`, `:65–78`, `:80–91` |
| V6 ocho niveles y 28 capacidades | `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md:1.2`, `:2` |
| V6 es snapshot de un Plan `Closed` y no normativo | ídem, encabezado y `:Origen` |
| H-1 entry points sin marca | `protocol/_AGENTS.md:8,43,47`; `protocol/.agents/INDEX.md:21,25–29` |
| H-2 `status: planned` retirado con condición | `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:68–72` |
| H-3 cuatro acepciones de «verified» | `EVIDENCE.md:65–78`; `harness/INDEX.md:41–47`; `standards/runtime/PROTOCOL_METRICS.md:207–219`; `standards/context/MEMORY_SYSTEM.md:81–86` |
| H-4 verificadores DEV-only y frontera de distribución | `harness/INDEX.md:41–47`, `:49–62`; `docs/ADOPTION.md:§6.4` |
| H-5 IDs citados y definidos sólo en DEV | `harness/INDEX.md:127–131`; `docs/rfc/62-guarantee-model-and-enforcement-boundaries.md:166–190` |
| H-6 términos ausentes del glosario | `docs/glossary/terms.md`; `docs/glossary/INDEX.md:74–104` |
| H-7 vocabulario de dominio definido sólo para el ROADMAP | `docs/CONVENTIONS.md:785`; `docs/planificacion-argentos-diseno-2026-10-13.md:1300` |
| H-8 límites honestos declarados en el payload | `harness/INDEX.md:16`, `:27`, `:31–34`, `:415` |
| §1.3 caso 1 («zero hallucinations» como aspiración) | `docs/working/audits/AUDITORIA_SISTEMA_2026-08-16.md:382` |
| §1.3 caso 2 (afirmación falsa del ROADMAP) | `docs/planificacion-argentos-diseno-2026-10-13.md:1298` |
| Placement: familias y reglas | `docs/placement-contract.md:§6`, `PC-10`, `PC-11`, `PC-19`, `PC-20`, `PC-37`, `PC-63` |
| Glosario: clases, campos y regla de alta | `docs/AGENTS.md:Naturaleza documental`; `docs/glossary/INDEX.md:31–40`, `:59–70` |
| Prohibición de registry y de mecanismos DEV/Protocol compartidos | `AGENTS.md:Do NOT`; `docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera`; `docs/rfc/75-change-lifecycle.md:Dev vs Protocol` |
| Ausencia de evidencia ≠ evidencia positiva | `docs/behavior-patterns.md:La ausencia de evidencia nunca se convierte en evidencia positiva` |
| Patrón «Regla transversal —» | `docs/CONVENTIONS.md:484`, `:508` |
| Batería canónica | `docs/VERSIONING.md:4.1 Batería canónica de verificación` |
| Precedente de checker diferido | `docs/planificacion-argentos-diseno-2026-10-13.md:1171` |

---

_Fin de la especificación. Ninguna modificación estructural fue realizada. Este documento es Working, no normativo, y no autoriza ninguna de las fases que describe._
