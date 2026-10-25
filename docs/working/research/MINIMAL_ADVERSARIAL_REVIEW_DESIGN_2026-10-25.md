# Minimal Adversarial Review (MAR) — diseño experimental y preregistro

> **Clase documental:** Working / Research — **no normativo** (`docs/AGENTS.md:Naturaleza documental`). Es evidencia y provenance; nunca autoridad.
> **Estado:** `EXPERIMENTAL — DISEÑO CONGELADO / PREREGISTRO CONGELADO (v2)`. La v2 incorpora la revisión independiente pre-ejecución y su registro de corrección (§14); ninguna pasada se ejecutó antes. No promueve mecanismo, no modifica `protocol/` ni `.agents/`, no crea gobernanza, no crea estado, no crea autoridad y no reemplaza la deliberación adversarial existente.
> **Origen:** solicitud directa del mantenedor del 2026-10-25 (insumo local no versionado; no se cita como `ruta:sección`, contención RFC-69 I2, precedente `<PLAN-178>:F-2`). Reduce la hipótesis de la campaña previa de Adversarial Deliberation (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:8. Decisión de la campaña`) a un mecanismo mínimo y a un experimento de validación.
> **Artefactos relacionados:** FRAME congelado del caso (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md`); evidencia de campaña T1–T3 (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md`, `docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md`, `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md`); condición previa de la capacidad (`docs/rfc/77-protocol-native-adversarial-deliberation.md`, `docs/plans/114-adversarial-deliberation-mvp.md`, `docs/plans/116-adversarial-deliberation-mvp-closure.md`, `docs/plans/117-adversarial-deliberation-feature-adoption.md`, `docs/plans/120-adversarial-deliberation-materialization.md`); estado de integración (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md`); plan del Change (`docs/plans/179-minimal-adversarial-review.md`); prototipo (`runtime/adversarial_review/`); informe de validación (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_VALIDATION_2026-10-25.md`, creado después de ejecutar el experimento).
> **Etiquetas de evidencia usadas en este documento:** `OBSERVED` (registrado en un artefacto), `MEASURED` (conteo o duración medida), `INFERRED` (derivación aritmética o lógica a partir de evidencia registrada), `HYPOTHESIS` (afirmación a validar) y `RECOMMENDATION` (propuesta no autoritativa). El documento no convierte `INFERRED` ni `HYPOTHESIS` en `OBSERVED`.

---

## 1. Problema y pregunta

La campaña de **T2/T3** estableció que la deliberación adversarial completa produce valor material reproducible pero cuesta 4,01× y 5,21× el baseline, por encima del umbral congelado de 3,0× (umbral fijado para esa campaña, no para T1), y que el coste no proviene de la longitud decorativa sino de **cuatro pasadas completas** que replican el tamaño de un análisis normal (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§4.3`; `:§8`). T1 midió 2,35× tiempo / 2,50× palabras con taxonomy y método previos al preregistro, y **no se poolea** (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md:§7.2`). La decisión de campaña fue `REFORMULATE`, no `ADOPT` ni `REJECT`.

La pregunta de esta iniciativa es:

> **¿Puede una revisión adversarial mínima, selectiva, advisory y presupuestada conservar una fracción significativa del descubrimiento material observado en T2/T3, reduciendo el coste hasta un presupuesto razonable (objetivo experimental ≤ 2,0× baseline), sin convertirse en autoridad, gate ni estado nuevo?**

La respuesta admisible no es "sí" por construcción: puede ser `ADOPT_DEV_EXPERIMENT`, `REFINE`, `REJECT` o `DEFER` (§9.7). El diseño existe para que el resultado sea medible y falsable.

**Lo que esta iniciativa no hace:** no reabre la investigación T1–T3, no la re-ejecuta, no asume que el mecanismo anterior sea correcto, no implementa Court/Jury/voting/Judge, no modifica el Protocol y no promueve la capacidad DEV existente.

---

## 2. Evidencia disponible (T1–T3)

Esta sección es una **síntesis citada**, no una re-ejecución. Los números se toman de los artefactos congelados.

### 2.1 Tabla resumen

| Trial | Caso | `DISTINCT_MATERIAL_NEW` | Duplicación | Espurias | Impacto atribuido | Coste | Clase |
|---|---|---:|---:|---:|---|---:|---|
| #1 | `Integration Surface` en el template (F-01 de `<PLAN-178>`) | 1 `MATERIAL` marginal (taxonomía híbrida, no comparable) | 75 % (12/16) | 0 | 0 decisional; 1 cambio de plan | 2,35× tiempo / 2,50× palabras | positivo marginal |
| #2 | Memory como dependencia estándar del Execution Host | **9** (4 `NEW` + 5 `DERIVED`) | 45,8 % | 4,2 % | 0 `DECISIONAL`; 2 `PLAN`; 2 `EVIDENCE` | **4,01×** | `POSITIVE_BUT_COSTLY` |
| #3 | ADR-worthiness del acto de autoridad del Plan 152 | **8** (8 `NEW`) | 13,0 % | 30,4 % | 2 `DECISIONAL` (bundle `D-1`+`D-4`); 5 `PLAN` | **5,21×** | `POSITIVE_BUT_COSTLY` |

Fuente: `docs/working/research/ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md:§6.2,§7.2`; `docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§4.1,§4.2,§4.3`; `:Apéndice H §2,§5`; `:Apéndice N §2,§5`. `MEASURED` salvo la taxonomía de T1, que es híbrida y no se poolea (`:§6.1`; `:§9`).

**Lectura `OBSERVED`:** hay descubrimiento material nuevo reproducible 2/2 en T2/T3; el impacto decisional atribuible es advisory y aparece 1/2; la duplicación y la espuriedad varían mucho por caso; el coste es 2/2 superior al umbral.

### 2.2 Atribución por operación (evidencia decisiva para el mínimo)

| Operación | `DMN` aportados (T2+T3; T1 no pooleable) | Impacto atribuido | Coste (T2+T3) | Juicio soportado por la evidencia |
|---|---:|---|---:|---|
| **PROSECUTION / falsificación dirigida** | **11/17** | T1 (fuera del pool): el único material; T2: todo el impacto atribuido (2 `PLAN` + 2 `EVIDENCE`); T3: 4 de 5 filas `PLAN` | 326 s + 612 s | **Núcleo del valor** |
| **DEFENSE / caso favorable** | 4/17 | T3: los 2 `DECISIONAL` (bundle `D-1`+`D-4`); 0 en T2; origen de la única `SPURIOUS` de T2 | 422 s + 241 s | **Condicional**: necesario para un cambio decisional; débil para condiciones/contradicciones |
| **SYNTHESIS + criterion comparison** | 0/17 | reweighting/`NO ATRIBUIDO` en T2; set-level en T3 | 277 s + 430 s (24–30 % del tratamiento) | **Reducible**: no produjo findings materiales contados; su función útil es comparar y citar IDs, no producir contenido |
| **REBUTTAL** | 2/17 | 0 cambios de veredicto/recomendación en 2/2; en T3 refutó materialmente P-4a (que ya era `SPURIOUS`) | 130 s + 145 s (≈11 %) | **Eliminable** en el mínimo |

Fuente: `docs/working/research/ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md:§6.2,§6.3,§6.5`; `docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§4.1,§7.F,§8.3`; `:Apéndice G §4,§6`; `:Apéndice M §4,§6`. `MEASURED` (los conteos y duraciones), `INFERRED` (el juicio "núcleo del valor", que es lectura del Lead de esta iniciativa, no una afirmación de la campaña).

### 2.3 Coste: composición

El multiplicador es **aditivo sobre cuatro pasadas de tamaño comparable al baseline**, no un efecto de "texto extra" (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§4.3`; `:Apéndice H §4.1`; `:Apéndice N §4`):

| Pasada | T2 (s / ×baseline) | T3 (s / ×baseline) |
|---|---:|---:|
| DEFENSE | 422 / 1,465 | 241 / 0,880 |
| PROSECUTION | 326 / 1,132 | 612 / 2,234 |
| SYNTHESIS | 277 / 0,962 | 430 / 1,569 |
| REBUTTAL | 130 / 0,451 | 145 / 0,529 |
| **Total** | **1 155 / 4,01×** | **1 428 / 5,21×** |

`INFERRED` (aritmética sobre lo medido; **ninguna variante se ejecutó**): `D+P` = 2,60× / 3,11×; `P` solo = 1,13× / 2,23×; `D` sola = 1,47× / 0,88×; `D+S` = 2,43× / 2,45×; `P+S` = 2,09× / 3,80×. Conclusión `INFERRED` decisiva: **el objetivo ≤ 2,0× no se alcanza quitando pasadas de las existentes mientras se conserven dos posiciones más una comparación; requiere pasadas más baratas, no solo menos pasadas** (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§8.3`; `:§9`). Ese es el `GAP` que este experimento mide.

Además, el coste registrado es un **rango por trial** porque la provenance del baseline no está auditada en el ledger (`:§4.3,§5`, desviaciones D-g/D-l): T2 `SELF` 4,01× y `LEAD`-consistente 4,46× (con `LEAD` declarado 3,12×); T3 `SELF` 5,21× y `LEAD`-consistente 5,29×. Toda comparación debe reportar rango y método.

### 2.4 Decisión de campaña y estado de las hipótesis

`OBSERVED` (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§7,§8`). Etiquetas de campaña: **`C-H#`** (no confundir con las hipótesis `M-H#` de esta iniciativa, §3):

- `C-H1 DISCOVERY = REPLICATED 2/2`;
- `C-H2 RE-EVALUATION = NOT ESTABLISHED AS DISTINCT VALUE` (y la independencia epistemológica tampoco está establecida en la numeración del protocolo original);
- `C-H3 DECISIONAL IMPACT = 1/2` (advisory, bundle);
- `C-H4 COST = FAILED` (4,01×/5,21× contra umbral congelado 3,0×);
- `C-H5 NEGATIVE`: la campaña describe el fenómeno negativo como **presente pero no predominante** (coste alto en 2/2 y espuriedad alta en T3); el resumen del mantenedor lo etiqueta `PARTIALLY CONFIRMED`, pero **ningún trial fue `NEGATIVE` ni la campaña `REJECT`** y la operacionalización congelada de la hipótesis negativa (clase de trial/campaña) no se alcanzó;
- `FINAL_DECISION = REFORMULATE` por el trigger congelado **R4 — coste desproporcionado**;
- `CAMPAIGN_INTEGRITY = VALID_WITH_LIMITATIONS` (14 desviaciones: 8 `D2`, 6 `D1`, **0 `D3`**).

### 2.5 Qué **no** sabemos (GAPs que condicionan el diseño)

`INFERRED` a partir de los artefactos:

1. **Ninguna variante mínima fue medida**: todos los costes de configuraciones reducidas son extrapolación aritmética.
2. **La tensión ≤ 2,0× vs "dos pasadas + comparación"** (2,60×/3,11× a las duraciones medidas) exige pasadas más cortas; ese diseño no tiene evidencia.
3. **Los casos T2/T3 estaban pre-analizados** (auditoría previa / decisión pendiente previa): el techo de descubrimiento es bajo por diseño y no se puede generalizar.
4. **La atribución decisional de T3 es a nivel de bundle** (`D-1`+`D-4`); la retención debe puntuarse también sobre los findings con impacto registrado, no solo sobre `DMN` bruto.
5. **La puerta de orden baseline→tratamiento falló** en T2/T3 (D2): el experimento nuevo debe cortarla con una pared dura.
6. **No hay instrumentación de coste/tokens**; las duraciones son auto-declaradas y el baseline tiene provenance débil.
7. **El veredicto/recomendación aportaron información atribuible solo en 1/3**; el valor observado está en condiciones, contradicciones y evidencia requerida.
8. **La espuriedad depende del troceado atómico**; un umbral fijo es frágil.
9. **La forma "regla declarada sin realización en el ejecutor" reaparece** en el caso elegido para validar; el diseño debe declararlo, no ocultarlo.

---

## 3. Hipótesis de esta iniciativa

Las hipótesis se definen antes de ejecutar; el experimento de §9 las evalúa. No son afirmaciones. Se namespacan **`M-H#`** (iniciativa) para no colisionar con las de campaña **`C-H#`** (§2.4).

- **`M-H1` — Value retention.** La revisión mínima produce findings materiales nuevos respecto del baseline, y conserva una fracción significativa de los findings materiales nuevos del tratamiento completo sobre el mismo caso. *Operacionalización:* `VALUE_RETENTION = |RETAINED| / |FULL_SET|` (§9.6); éxito si ≥ 0,60 y `|MIN_SET| ≥ 1`.
- **`M-H2` — Cost reduction.** La revisión mínima reduce el coste del mecanismo completo hasta un presupuesto razonable. *Operacionalización:* `COST_RATIO` según el método congelado de §9.4 (EFFECTIVE = max(SELF, LEAD)) de la condición `TWO_PASS` **ejecutada**; objetivo experimental **≤ 2,0×**, medido, contra 4,01×/5,21× de T2/T3. `HYPOTHESIS`: el objetivo es alcanzable con pasadas acotadas; puede fallar.
- **`M-H3` — Decision relevance.** Al menos un finding conservado e **independientemente atribuido en la condición MAR** modifica justificadamente plan, recomendación, evidencia requerida o decisión (taxonomía de impacto §9.5), con atribución estricta y bundle permitido si se declara.
- **`M-H4` — Selectivity.** La revisión solo se ejecuta cuando hay suficiente materialidad/ambigüedad/riesgo para justificar su coste, y el trigger distingue niveles de profundidad (una vs dos pasadas) sin convertirse en gate ni clasificador automático. *Operacionalización parcial:* recomendación del trigger sobre las siete señales declaradas + decisión de invocación independiente registrada; **el experimento §9 no valida H4** (solo tests unitarios de la regla; precisión/recall reales quedan en §10 ítem 6).
- **`M-H5` — Negative.** Reducir el mecanismo puede eliminar el componente que producía valor (prosecution/defense) o aumentar objeciones espurias; el resultado puede ser negativo (`REFINE`/`REJECT`).

**Fuera de hipótesis (explícito):** no se afirma independencia epistemológica; la separación es procedural. No se evalúa voting. No se evalúa el veredicto como autoridad. No se modifica Theoretical Execution.

---

## 4. Mecanismo mínimo propuesto (HYPOTHESIS de diseño)

### 4.1 Principio

Conservar **una sola función epistemológica por pasada**, con **presupuesto explícito por pasada**, y sustituir la deliberación completa por el mínimo conjunto que la evidencia asocia a valor: **falsificación dirigida** (núcleo), **caso favorable** (condicional a reversión decisional) y **una comparación corta y trazable por criterio** que no introduce findings nuevos. Nada de rebuttal, nada de veredicto como entidad, nada de voting, nada de juez.

### 4.2 Flujo y dos niveles

```text
DECLARED SELECTIVITY  (recomendación advisory; el invocador declara decisión y motivo)
        ↓
FRAME (congelado: question / candidate / criteria / evidence / limits / baseline ref)
        ↓
PASS 1 — TARGETED FALSIFICATION      (bounded; posture: strongest case against)
        ↓  commitment hash
PASS 2 — STRONGEST CASE FOR          (bounded; solo en TWO_PASS)
        ↓  commitment hash
SHORT CRITERION-MAPPED SYNTHESIS      (bounded; NO puede introducir findings materiales)
        ↓
ADVISORY RESULT
  findings + condiciones + contradicciones + evidencia requerida
  + impact type por finding + desacuerdos preservados
  + recomendación advisory con base citada
        ↓
EXISTING AUTHORITY (humano / autoridad que ya correspondía) decide
```

- **Tier `SINGLE_PASS`** — PASS 1 solamente, con el resultado registrado por el invocador. Coste mínimo; conserva la función que aportó 11/17 `DMN`. Sin comparación por criterio (limitación declarada).
- **Tier `TWO_PASS`** — PASS 1 + PASS 2 + síntesis corta. Se usa cuando el trigger recomienda profundidad por reversión/irreversibilidad/ambigüedad alta. `MAX_PASSES = 2` aplica a **pasadas de deliberación**; la síntesis es consolidación, no una tercera pasada de evaluación.
- **Sin `REBUTTAL`**, **sin `VERDICT` como entidad separada**, **sin segunda ronda**: la evidencia no los sostiene (§2.2).

### 4.3 Operaciones: conservar, reducir, eliminar

| Operación del mecanismo completo | Decisión MAR | Justificación (evidencia) |
|---|---|---|
| FRAME (question, candidate, criteria, evidence, limits) | **Conservar**, congelado | Es la unidad de comparabilidad; sin frame no hay atribución (`docs/working/research/ADVERSARIAL_DELIBERATION_EXPERIMENT_2026-10-25.md:§5`). |
| DEFENSE (strongest case for) | **Conservar condicionalmente** (solo `TWO_PASS`) | Única operación con cambio decisional atribuido (T3 `D-1`+`D-4`); 0 impacto atribuido en T2; origen de la única espuria de T2 (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§8.3`; `:Apéndice H §2,§3.1`). |
| PROSECUTION (targeted falsification) | **Conservar como núcleo** (siempre) | 11/17 `DMN` pooled (T2+T3); único source del material de T1 (fuera del pool) y de todo el impacto atribuido de T2; 4/5 `PLAN_IMPACT` de T3 (`:§4.1,§7.F`). |
| Commit-before-reveal | **Conservar como declaración verificable por hash** | Compró atribución y tamper-evidence, **no** mejora medida; no se afirma independencia (`:§7.B`; `docs/working/research/ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md:§6.6`). |
| REVEAL | **Conservar** como acto de auditoría del registro | Permite reconstruir el orden; no es un paso de razonamiento adicional. |
| CRITERION COMPARISON | **Absorber en la síntesis corta** | 0 `DMN` propio; su función útil es mapear criterios y citar IDs; como pasada independiente costó 24–30 % del tratamiento. |
| SYNTHESIS (pasada completa con artifact propio) | **Reducir a comparación corta (≤500 palabras) con IDs** | 0 `DMN` en 3/3; veredicto `NO ATRIBUIDO` o set-level; el coste era 0,96×/1,57× baseline (`:§4.3`; `:§8.3` ítem 2). |
| VERDICT | **Eliminar como entidad**; la recomendación advisory + base es suficiente | Información atribuible en 1/3; el vocabulario cerrado del payload no se toca (`docs/rfc/77-protocol-native-adversarial-deliberation.md:Non-Goals / DEFERRED`). |
| RECOMMENDATION | **Conservar, advisory, con `impact type`** | El valor observado es condiciones/contradicciones/evidencia; la recomendación es la forma mínima de transmitir un resultado advisory con base (`:§8.2,§8.3` ítem 4; `:§7.C`). |
| REBUTTAL | **Eliminar** | 0 cambios de veredicto/recomendación en 2/2; 11 % del coste; en T3 refutó materialmente P-4a, pero P-4a ya era `SPURIOUS`, así que no cambió el resultado (`:Apéndice G §4,§6`; `:Apéndice M §4,§6`). |
| Segunda ronda / N pasadas | **Prohibido por presupuesto** (`MAX_PASSES=2`) | Deliberación indefinida sin evidencia de valor; `M-H5`. |
| Voting / N jurados / Judge / Court | **No implementar** | La campaña no evaluó voting y no demostró valor de panel; el payload prohíbe entidades de jurado (`docs/rfc/77-protocol-native-adversarial-deliberation.md:Non-Goals / DEFERRED`; `README.md:### Adversarial deliberation — more than one evaluation before a decision`). |

### 4.4 Contrato experimental del registro

Forma mínima que el prototipo valida **en un subconjunto declarado** (schema `1`; el prototipo valida estructura, vocabularios, provenance, caps de palabras, coste y presupuesto; **no** valida el cap de findings atómicos ni los campos marcados opcionales; detalle en `runtime/adversarial_review/`):

```text
ReviewRecord
├── schema_version, frame {question_ref, candidate, criteria[], evidence_refs[],
│     mode="viability", baseline_ref?, contamination_note?,
│     trigger_recommendation, declared_invocation_reason, declared_by,
│     commit_before_reveal: true}          # declaración; el prototipo avisa si falta
├── passes[1..2] {pass_id, posture, executor, material_received[], withheld_material[],
│     commitment_hash (sha256 hex), evaluation_ref,
│     findings[] {finding_id, source, claim, criterion, direction, evidence_refs[],
│       novelty, materiality, impact, consequence?, discarded_reason?},
│     cost {agent_seconds, words, calls}}
├── synthesis {method="CRITERION_MAPPED_SHORT", evaluation_ref, findings_kept[],
│     new_material_findings=[] (obligatorio vacío),
│     disagreements[] {criterion, state, position_a, position_b}, cost}
├── advisory_result {recommendation, basis[] (IDs), impact_summary?, limitations?,
│     authority="ADVISORY_ONLY"}
├── limitations[]
└── cost {baseline_agent_seconds, baseline_words, target_multiplier=2.0}
```

Vocabularios cerrados: `posture ∈ {TARGETED_FALSIFICATION, STRONGEST_CASE_FOR}`; `novelty ∈ {NEW, DERIVED, DUPLICATE}`; `materiality ∈ {MATERIAL, NON_MATERIAL, SPURIOUS}`; `impact ∈ {DECISIONAL_IMPACT, PLAN_IMPACT, EVIDENCE_IMPACT, NONE}`; `direction ∈ {SUPPORTS, OPPOSES, NEUTRAL}`; `recommendation ∈ {ADVISE_PROCEED, ADVISE_REVISE, ADVISE_GATHER_EVIDENCE, ADVISE_STOP, NO_RECOMMENDATION}`; `disagreement.state ∈ {AGREEMENT, PARTIAL_AGREEMENT, UNRESOLVED_DISAGREEMENT}`. Ningún campo de votación, juez, corte o autorización puede existir en el registro; el prototipo lo verifica mecánicamente.

### 4.5 Caps y presupuesto

| Límite | Valor | Estado |
|---|---|---|
| `MAX_PASSES` (pasadas de deliberación) | **2** | decisión de diseño; HYPOTHESIS de minimalidad |
| `TARGET_COST` | **≤ 2,0× baseline** | hipótesis experimental derivada de la campaña; **no** verdad arquitectónica |
| Findings atómicos por pasada | ≤ 6 | cap de salida; HYPOTHESIS de coste |
| Palabras por pasada | ≤ 700 | cap; HYPOTHESIS de coste (las pasadas completas medían ~2 300 palabras) |
| Palabras de síntesis | ≤ 500 | cap; HYPOTHESIS de coste |
| Coste declarado por pasada | obligatorio (`agent_seconds`, `words`, `calls`) | medición, no instrumentación de tokens |
| Regla de parada por presupuesto | si la pasada 1 ya consume ≥ 1,0× el baseline, el mecanismo **no inicia la pasada 2**: entrega `SINGLE_PASS` y registra `BUDGET_EXCEEDED` | evita deliberación indefinida; en el experimento §9 se corre `TWO_PASS` completo para medir retención y coste real, y se calcula el contrafáctico de la regla |

**Semántica de los caps (congelada).** Los caps son **instrucciones a la pasada** y variables de tratamiento no medidas previamente (`HYPOTHESIS` de coste), no reglas de poda del evaluador:

- Una pasada debe producir como máximo 6 findings atómicos y 700 palabras; la síntesis, 500 palabras. Si el material excede el cap, la pasada **prioriza** los hallazgos y declara el exceso como sobrepaso (`OVERRUN`); **todos** los findings que produce se clasifican (no se poda en la evaluación). Un sobrepaso se registra como desviación **D2** con su coste.
- Conteo de palabras: tokens separados por espacios en blanco del cuerpo de la evaluación (método de la campaña, `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md:§11`).
- El prototipo valida los caps de palabras y de coste declarado; el cap de 6 findings lo verifica **la evaluación del experimento**, no el prototipo (§6.3).

**Por qué el objetivo ≤ 2,0×:** es la reducción de la referencia T2/T3 (4,01×/5,21×) hasta un presupuesto que un Change DEV pueda absorber sin convertir la revisión en un segundo proceso. Es una **hipótesis**, no una constante del repositorio; si la evidencia justifica otro umbral, se documenta explícitamente antes de cambiarlo (§9.9).

### 4.6 Commit-before-reveal: qué se conserva y qué no se afirma

Cada pasada:
1. recibe el FRAME y su material declarado;
2. produce su evaluación y calcula `sha256` de su cuerpo;
3. declara `material_received` / `withheld_material` y el hash **antes** de que el invocador revele la otra pasada;
4. la revelación es un acto de auditoría del registro (hashes y orden), no una garantía técnica.

`INFERRED` (a partir de evidencia registrada): el compromiso previo compró atribución/tamper-evidence, no una mejora medida de la evaluación (`docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§7.B`). Lo `OBSERVED` es que hashes y orden quedaron registrados; la conclusión sobre lo que "compró" es `INFERRED`. El registro MAR declara la limitación: el orden y la no lectura son **atestiguados, no impuestos técnicamente**.

### 4.7 Autoridad

```text
ADVERSARIAL REVIEW
        ↓
EVIDENCE / ANALYSIS
        ↓
ADVISORY RESULT
        ↓
EXISTING AUTHORITY
```

Invariantes (verificadas por el prototipo y por el diseño, no por un gate normativo):

- la review **no autoriza**, **no ejecuta**, **no cambia governance**, **no redefine policy** y **no puede elevar su propio resultado a autoridad**;
- no existe figura de Judge ni campo de autorización;
- el resultado es `ADVISORY_ONLY`; la decisión pertenece a la autoridad existente (mantenedor / Change authority);
- `Closed`/`Executed`/`Released` u otros estados del lifecycle **nunca** son escritos por la review;
- el registro puede citarse como evidencia en un Plan por referencia, como cualquier evidencia Working; no crea estado.

### 4.8 Provenance

Todo finding debe permitir distinguir y reconstruir:

| Pregunta | Campo / mecanismo |
|---|---|
| ¿Quién/qué lo produjo? | `source` (`PASS_FALSIFICATION`/`PASS_ADVOCACY`), `posture`, `executor`, `pass_id` |
| ¿Qué evidencia lo sustenta? | `evidence_refs[]` (`ruta:sección` o comando reproducible) |
| ¿Es nuevo o derivado? | `novelty ∈ {NEW, DERIVED, DUPLICATE}` relativo al baseline declarado |
| ¿Es material y por qué? | `materiality`, `consequence` (obligatoria si `MATERIAL`) |
| ¿Fue descartado y por qué? | `discarded_reason` |
| ¿Qué impacto tiene? | `impact ∈ {DECISIONAL_IMPACT, PLAN_IMPACT, EVIDENCE_IMPACT, NONE}` |
| ¿Quién lo conservó en la síntesis? | `synthesis.findings_kept[]` (IDs) — la síntesis no crea findings |

**Namespacing:** IDs locales por pasada (`P1-F1…`, `P2-F1…`), nunca un ID global ni una identidad de finding del Change Lifecycle; los findings de la review **no** son `<artifact>:F-<n>`. Reutilización: subconjunto del contrato `DELIBERATION_REPORT.md` (`docs/rfc/77-protocol-native-adversarial-deliberation.md`; `protocol/.agents/contracts/DELIBERATION_REPORT.md:Required sections`) en su forma documental, sin copiar al payload ni crear una infraestructura paralela. La retención se registra con un **mapa declarado por el evaluador** (`FULL_ID → MIN_ID`), no por matching automático de texto.

### 4.9 Desacuerdo

El desacuerdo es un resultado válido. La síntesis corta **preserva** posiciones; **no** resuelve por mayoría, votación, autoridad ficticia ni eliminación del argumento minoritario. Estados: `AGREEMENT` | `PARTIAL_AGREEMENT` | `UNRESOLVED_DISAGREEMENT`. Si dos findings materiales de pasadas distintas comparten criterio con dirección opuesta (`SUPPORTS` vs `OPPOSES`), el registro **debe** contener una entrada de desacuerdo para ese criterio (regla mecánica del prototipo); no hacerlo es un registro inválido, no una decisión tomada.

### 4.10 Trigger / selectivity (advisory)

Señales declaradas por el invocador (no inferidas por un clasificador): **materialidad potencial, ambigüedad, riesgo, impacto, incertidumbre, irreversibilidad, coste esperado de equivocarse**, cada una `LOW|MEDIUM|HIGH|UNKNOWN`.

Regla determinista experimental (`runtime/adversarial_review/selectivity.py`):

1. cualquier señal `UNKNOWN` → `INSUFFICIENT_SIGNALS` (no se inventa el disparo);
2. `materiality_potential = LOW` → `NO_REVIEW`;
3. materialidad `MEDIUM|HIGH` y alguna de `ambiguity|irreversibility|error_cost|risk = HIGH` → `REVIEW_TWO_PASS`;
4. materialidad `MEDIUM|HIGH` y alguna de `ambiguity|risk|impact|uncertainty|irreversibility|error_cost = MEDIUM` → `REVIEW_SINGLE_PASS`;
5. en otro caso → `NO_REVIEW`.

El trigger es **advisory**: recomienda una profundidad y explica; **no invoca, no enruta, no bloquea y no elige por sí mismo**. El invocador registra una **decisión de invocación independiente y su motivo** en el FRAME; esa decisión puede diferir de la recomendación y el registro lo muestra (D7 `PROHIBITED` para clasificadores automáticos que deciden invocación, profundidad o postura: `protocol/.agents/standards/orchestration/DECISIONS.md:D7 — Deliberation invocation`; convención Working: `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md:3. Invocation`). La regla es `HYPOTHESIS` (`M-H4`) y **no se mide en §9** (solo tests unitarios); un trigger conservador está bien, un trigger que se convierte en gate está prohibido.

---

## 5. Alternativas descartadas

| Alternativa | Por qué se descarta (en esta iniciativa) |
|---|---|
| Deliberación completa con rebuttal y veredicto | 4,01×–5,21× medidos; rebuttal sin cambios de veredicto/recomendación; `REFORMULATE` de campaña. |
| `Prosecution` sola siempre | 11/17 `DMN` pero 0 cambios decisionales fuera del caso donde Defense aportó `D-1`+`D-4`; se conserva como tier `SINGLE_PASS`, no como único tier. |
| `Defense` sola | 4/17 `DMN`, 0 impacto en T1/T2; pierde la falsificación que concentra el valor. |
| Síntesis como "juez" con veredicto | 0 `DMN` propio; información atribuible 1/3; crearía una figura de autoridad no justificada. |
| Voting / N jurados / panel / Court / Judge | No evaluado; la evidencia no demuestra valor; prohibido por el encuadre de esta iniciativa y por el payload. |
| Rebuttal acotado "solo si cambia el veredicto" | El veredicto se elimina; la condición no tendría objeto. Queda como hipótesis futura documentada, no implementada. |
| Tercera pasada / segunda ronda | `MAX_PASSES=2`; si se necesitara más, es evidencia contra la minimalidad. |
| Integración con `protocol/.agents/` (nuevo contrato/skill/campo) | Requiere RFC-56 Clase A; prohibido por esta iniciativa y sin evidencia suficiente. |
| Campo `Integration Surface` en el template de planes | Idea no implementada (audit F-01); introducirlo sería un cambio de gobernanza no autorizado (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:9. Findings`). |
| Integración con Theoretical Execution como paso | No existe interfaz de entrada de review; TE lee el commit base; modificar su policy no está autorizado. |
| Clasificador/auto-trigger de invocación | `PROHIBITED` (D7); la review debe ser una decisión declarada. |
| Nuevo estado/lifecycle/registry/ID global | Destruye la propiedad advisory y crea infraestructura sin evidencia. |
| Medir solo coste (sin retención) | El coste bajo no es éxito si se pierde el valor material (§9.6). |
| Reutilizar T2/T3 como casos de validación | Ya deliberados; el experimento necesita un caso no deliberado para medir retención de forma no circular. |

---

## 6. Integración: superficie real y superficie experimental

### 6.1 No hay punto de integración limpio hoy (`OBSERVED`)

La capacidad de deliberación adversarial existe como **payload documental** (`protocol/.agents/contracts/DELIBERATION_REPORT.md`, skill `adversarial-deliberation`, punto de decisión `D7`, subsección del rol Orchestrator) y como **prior art DEV aislado** (convención Working, planes 114/116/117 cerrados, campaña 2026-10-25). No hay implementación en `runtime/`, no hay checker en `tools/`, no hay hook en el Orchestrator y los tests existentes validan fixtures vendorizados, no un seam del payload (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:4. Matriz principal` filas 10–11; `:7. Aislamientos deliberados`). Theoretical Execution emite `TE_RESULT` por stdout sin lector de review y lee el commit base, no el working tree (`.agents/policies/theoretical-execution.md:2. Unit, inputs and outputs`; `:3. Declared overlay and determinism`; `:11. CLI, persistence and recovery`). El campo `Integration Surface` no existe en el template (audit F-01).

Por lo tanto: **no se inventa una integración**. MAR se ejecuta como **capacidad experimental invocada manualmente**, con registro Working/sesión, sin consumidor automático.

### 6.2 Superficie experimental candidata (lenguaje experimental, no contrato del Protocol)

| Dimensión | Candidato MAR | Estado |
|---|---|---|
| Upstream inputs | candidato declarado por referencia (Plan commiteado + commit base, o decisión registrada); evidencia `ruta:sección`; baseline opcional; `TE_RESULT` opcional por path/hash | experimental |
| Contrato | `ReviewRecord` (§4.4), schema `1`, documentado en el prototipo | experimental, no payload |
| Lifecycle / state | **ninguno**: se invoca, produce evidencia y termina | deliberadamente ausente |
| Downstream consumers | humano/mantenedor; autor del Plan que revisa; re-run de TE tras nuevo commit | sin consumidor automático |
| Aislado deliberadamente | `protocol/`, `.agents/`, Orchestrator host, SAE, template de planes, batería canónica, `tools/`, CI | no se modifica |
| Integraciones desconocidas | descubrimiento del registro en sesiones futuras (sin índice/registro), ingesta de `TE_RESULT` sin schema reader, instrumentación de coste | GAP declarado |

El término **`Integration Surface`** se usa aquí solo como lenguaje experimental para describir esta frontera; **no** se introduce como contrato obligatorio del Protocol ni del template de planes por esta iniciativa.

### 6.3 Prototipo (`runtime/adversarial_review/`)

**Placement** (`docs/placement-contract.md:DEV families`; `PC-21`): dominio **DEV**; familia **Reference runtime** → `runtime/<package>/`; tests en `tests/`. Precedente: `runtime/placement/` (librería read-only, sin consumidor, `docs/placement-contract.md:PC-72.1`).

**Qué es:** una librería determinista, read-only, advisory-only, que (i) modela y valida el `ReviewRecord` (subconjunto de campos declarado en §4.4), (ii) calcula la recomendación de selectivity, (iii) evalúa presupuesto de palabras/coste declarado, (iv) calcula métricas de valor/impacto/coste/retención; más un CLI read-only (`validate`, `selectivity`, `metrics`). **No valida el cap de 6 findings atómicos** (lo verifica la evaluación del experimento) ni los campos marcados opcionales en §4.4.

**Qué no es:** no es un gate, no es un checker de la batería, no es un hook, no es un estado, no crea autoridad, no escribe archivos, no importa el host ni el payload, no tiene consumidor.

---

## 7. Theoretical Execution — hipótesis, no integración

La secuencia posible `PLAN → THEORETICAL EXECUTION → ADVERSARIAL REVIEW → REVISED PLAN` se mantiene como **HYPOTHESIS**. Hoy **no** es integrable limpiamente: TE emite JSON por stdout y no conserva nada; no existe lector de `TE_RESULT` como entrada de review; TE evalúa el commit base, por lo que un plan revisado solo es reevaluable tras un commit nuevo; y TE ya tiene una dimensión productor-atestiguada `adversarial` (`PENDING`) que no debe repurposarse (`.agents/policies/theoretical-execution.md:5. The five dimensions`; `:13. Boundaries`; `docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md:§8.3` cláusula 7). **No se modifica la policy de TE.** MAR puede leer, sin nueva interfaz, el plan commiteado y el `TE_RESULT` como evidencia documental por path/hash.

---

## 8. Presupuesto y medición de coste (método congelado v2)

**Método (`MEASURED`; v2 corrige `PRE-F02`).** Se miden dos relojes por ejecución y se combinan como en la campaña (`EFFECTIVE = max(SELF, LEAD)`; `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md:§11`):

- **`SELF`** — duración pared-reloj declarada por el propio ejecutor: primera y última acción del ejecutor son leer el reloj (`Get-Date -Format o`) y reportar ambos instantes; incluye su latencia de herramientas.
- **`LEAD`** — duración pared-reloj observada por el Lead para la llamada del ejecutor. Cuando dos pasadas corren en paralelo, el `LEAD` de la etapa es el de la llamada batch (no se duplica); por eso `LEAD` es una **cota inferior de wall-clock** de las etapas paralelas y `SELF` es la medida de agent-seconds.
- **`RATIO_SELF`** = suma de `SELF` del tratamiento / `SELF` del baseline. **`RATIO_LEAD`** = suma de `LEAD` del tratamiento (etapas seriales sumadas; etapa paralela contada una vez) / `LEAD` del baseline. **`EFFECTIVE = max(RATIO_SELF, RATIO_LEAD)`**.
- **`COST_RATIO` (primario, congelado)** = `EFFECTIVE` de la condición **`TWO_PASS` ejecutada** (PASS 1 + PASS 2 + síntesis). El `SINGLE_PASS` (sólo PASS 1) se reporta como **sensibilidad declarada** calculada con las duraciones medidas; **no puede sustituir** al primario en §9.7.
- Se reportan además palabras (`words_ratio`, ratio de tokens separados por espacios), llamadas, pasadas y palabras por pasada. La evaluación, adjudicación e integridad son **overhead de investigación**: se reportan aparte y no entran en `COST_RATIO`.
- Todas las duraciones se registran en el **ledger** (§9.10) con hashes. La medición tiene un solo observador y latencia de herramientas: se reporta como valor medido con esa limitación (§9.9).

**Objetivo:** `COST_RATIO ≤ 2,0×` (`HYPOTHESIS`). Referencias: T1 2,35× (método/taxonomía previos al preregistro, no pooleable); T2 `SELF` 4,01× / `LEAD`-consistente 4,46×; T3 `SELF` 5,21× / `LEAD`-consistente 5,29×. La comparación con T2/T3 es de orden de magnitud declarado, no method-identical: se reporta junto al método. El experimento mide y reporta; **no ajusta el umbral después de ver el resultado**.

---

## 9. PREREGISTRO CONGELADO del experimento de validación (v2 — corregido antes de ejecutar)

> **v2 congelada el 2026-10-25 antes de ejecutar cualquier pasada del experimento**, tras la revisión independiente pre-ejecución. v1 → v2: correcciones `PRE-F01`…`PRE-F20` con disposición registrada en §14. Cualquier cambio posterior a esta v2 se registra como **desviación** con su efecto sobre la validez; no se reescribe para acomodar resultados. La evidencia de orden es el commit del Change que contiene este documento (Commit 1), previo a la ejecución, más el ledger definido en §9.10.

### 9.1 Caso y FRAME (v2)

- **Caso:** `MAR-VALID-01` — el cierre derivado del host (`CLOSED_DERIVED`) y el registro `## Checkpoint / cierre` frente a las determinaciones de impacto de cierre (§5.1/§5.2/§7). Decisión real, abierta, material y verificable, con tres resoluciones materialmente distintas (A ejecutor / B norma / C límite) y sin resolución registrada en ningún plan/ADR/RFC/policy.
- **FRAME congelado:** el objeto congelado es `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md` (v2, Git-verificable en Commit 1; su sha256 se registra en el ledger y en el informe; si la copia operativa de staging discrepa, gobierna el archivo versionado). HEAD de evidencia congelado: `ac7f68074edbb9d67a1f231fac99c9e543a301aa`; HEAD de ejecución: el commit del Change (Commit 1). La verificación de anclas se hace con `git show ac7f680:<path>` o comprobando que los archivos ancla no cambiaron en el árbol de ejecución; es ítem de la auditoría de integridad.
- **Techo de contaminación (declarado):** el **hecho** está pre-diagnosticado en `docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md:3.6 c` (`CONTRADICTION`) y ese mismo documento Working contiene una **inclinación previa** hacia que el ejecutor consulte las obligaciones ya escritas (`:9.1 FACT 3`; `:9.3 DESIGN_OPTION` propuesta (2); `:HD-OPS-G`), compatible con la opción A y no neutral. La **decisión** no está resuelta en ningún plan/ADR/RFC/policy. El valor medido es sobre un **baseline informado**; la dirección de la inclinación se declara para no leer el resultado como descubrimiento independiente.
- **Señales del trigger (declaradas antes de ejecutar):** `materiality_potential=HIGH`, `ambiguity=HIGH`, `risk=MEDIUM`, `impact=HIGH`, `uncertainty=MEDIUM`, `irreversibility=MEDIUM`, `error_cost=HIGH` → recomendación de la regla: `REVIEW_TWO_PASS`.
- **Invocación declarada:** el Change experimental (plan 179) invoca la review para validar el mecanismo; el motivo se registra en el FRAME; la review no decide nada sobre el caso.
- **Material prohibido y recepción de material:** ver el FRAME congelado `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md`, régimen aplicable a todas las condiciones. En resumen: ningún ejecutor de BASELINE/FULL/MAR lee el diseño/preregistro, el plan 179, la campaña previa (`ADVERSARIAL_DELIBERATION_*`), el staging `sessions/` ni los insumos no versionados del mantenedor; recibe solo el FRAME y su postura. La exposición se audita.

### 9.2 Condiciones del experimento (v2)

| Condición | Contenido | Ejecución y material |
|---|---|---|
| **BASELINE** | Análisis normal del FRAME (sin instrucción adversarial): razonamiento, supuestos, evidencia, riesgos, alternativas, decisión/recomendación con plan y evidencia requerida | 1 ejecutor fresco; recibe FRAME; se **congela** (hash) antes de iniciar el tratamiento |
| **FULL** (comparador de retención) | Réplica del mecanismo completo T2/T3 **sobre el mismo caso nuevo** (no re-ejecución de T2/T3): DEFENSE + PROSECUTION (paralelas, aisladas, commit-before-reveal) → SYNTHESIS con comparación por criterio → REBUTTAL **solo si** la síntesis identifica un desacuerdo material que pueda cambiar el veredicto/recomendación | 4 ejecutores frescos; síntesis recibe FRAME + BASELINE cerrado + D + P; rebuttal recibe los artefactos cerrados + la objeción |
| **MAR** (tratamiento) | PASS 1 falsificación + PASS 2 caso favorable (paralelas, aisladas, commit-before-reveal) → síntesis corta (≤500 palabras, sin findings nuevos, desacuerdos preservados, conditions/contradictions/evidence + `impact type`) → resultado advisory | 3 ejecutores frescos; síntesis recibe FRAME + BASELINE cerrado + PASS 1 + PASS 2; sin rebuttal, sin verdict |
| **EVALUACIÓN** | Evaluador independiente: clasificación `NEW/DERIVED/DUPLICATE × MATERIAL/NON_MATERIAL/SPURIOUS`, dedupe, atribución de impacto, mapa de retención `FULL→MIN`, conteos y costes | 1 ejecutor fresco; recibe FRAME + todas las condiciones cerradas + costes; no recibe el diseño ni las hipótesis del Lead |
| **ADJUDICACIÓN** | Adjudicador independiente: re-clasifica categorías decisivas y una muestra declarada; resuelve disputas de **clase** y de **mapping** (no el Lead); registra la variante adjudicada y la sensibilidad | 1 ejecutor fresco; recibe evaluación + hallazgos disputados + definiciones congeladas |
| **INTEGRIDAD** | Auditor independiente: hashes/orden, no contaminación entre pasadas/condiciones, baseline congelado antes del tratamiento, exposición a material prohibido, clases de desviación, consistencia de conteos, verificación de anclas del FRAME | 1 ejecutor fresco; recibe ledger + artefactos crudos + declaraciones de material |

**Recepción de material declarada y simétrica** (FRAME congelado `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md`): FULL y MAR reciben el mismo material salvo el conjunto de operaciones; ambos reciben el BASELINE cerrado solo en su síntesis.

### 9.3 Orden, aislamiento y validez (v2)

1. **BASELINE primero y congelado**: su hash se registra en el ledger antes de que arranque cualquier pasada del tratamiento (pared dura; corrige D-a/D-b de T2/T3). Violarlo es **D3** (invalidante).
2. PASS 1 y PASS 2 del tratamiento (y DEFENSE/PROSECUTION del comparador) corren **sin acceso a la conclusión de la otra**; cada uno compromete un hash de su evaluación antes de la revelación. La coordinación del Lead puede lanzarlas en paralelo (no hay lectura cruzada); el orden declarado se audita.
3. La **síntesis** (FULL y MAR) recibe el FRAME, el **BASELINE cerrado** y las dos evaluaciones **después** de los hashes; no puede introducir findings materiales nuevos. Esta recepción del baseline es la que hace aplicable la regla de atribución estricta (diferencia con baseline) y es simétrica entre FULL y MAR.
4. REBUTTAL (solo FULL) se ejecuta únicamente si la síntesis identifica un desacuerdo material; si no hay desacuerdo, FULL termina en la síntesis y el rebote no cuenta como pasada.
5. La evaluación, la adjudicación y la integridad se hacen **después** de que todas las condiciones estén congeladas; no modifican artefactos de las condiciones.
6. El baseline no se reconstruye retroactivamente ni se "arregla" con información del tratamiento.

**Desviaciones y su clase** (pre-decididas): `D1` = desviación sin efecto sobre la comparación; `D2` = desviación con efecto declarado y analizado (no invalida por sí sola; se reporta y se evalúa sensibilidad); `D3` = rompe la comparación (baseline no congelado antes del tratamiento, contaminación cruzada demostrada, evidencia del FRAME falsa en un punto material, exposición a material prohibido que afecte a una pasada decisiva). Cualquier `D3` ⇒ experimento `INVALID` ⇒ `DEFER` (§9.7).

### 9.4 Medición de coste (congelada; desarrolla §8)

Por ejecución se registran: `SELF` (reloj del ejecutor), `LEAD` (reloj del Lead), palabras del resultado (tokens separados por espacios), llamadas (`1`) y `tokens = GAP`. Se calculan `RATIO_SELF`, `RATIO_LEAD` y `EFFECTIVE = max`; el **primario** de §9.7 es `EFFECTIVE` de la condición `TWO_PASS` ejecutada. La condición `SINGLE_PASS` (sólo PASS 1) se reporta como **sensibilidad** con las duraciones medidas y **no puede sustituir** al primario. Se reporta el `words_ratio` y el coste por pasada; evaluación/adjudicación/integridad se reportan aparte.

### 9.5 Taxonomía, materialidad e impacto (reutiliza la congelada de T2/T3)

Se reutilizan **sin cambios** las definiciones, umbrales y reglas de `NEW`/`DERIVED`/`DUPLICATE`; `MATERIAL`/`NON_MATERIAL`/`SPURIOUS`; materialidad en tres condiciones (soporte verificable + consecuencia concreta + objeto identificado); novedad no requisito de materialidad; dedupe por contenido; atribución estricta (diferencia con baseline + cita del ID + verificación de la cadena + contrafáctico); y `VALUE_CLASS`/clases de trial, de `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md:§8.1,§8.2,§8.3,§9,§10,§13.1,§13.2`.

- **`SPURIOUS_SHARE` (definición congelada y citada):** `SPURIOUS` distintos / findings distintos totales (`:§13.1`). En el experimento se computa sobre la **condición MAR**, corpus de **todos** los findings distintos de MAR (incluidos `NON_MATERIAL` y `DUPLICATE`), y se reportan conteos y empates. Se declara la fragilidad de denominador pequeño: con cap de 6 findings, 1 espuria = 1/6 ≈ 0,167 > 0,15; por eso 0,15 es un **umbral duro de la regla congelada** (ligado a `M-H5`/`C-H5`, no a coste), y se reporta también el conteo absoluto.
- **Niveles de evaluación vs campos del registro:** `REWEIGHTING`, `NO ATRIBUIDO` y `DECISION_IMPACT` (H3) son **resultados de atribución a nivel de evaluación**, que se registran en el informe de validación, **no** campos del `ReviewRecord` (cuyo vocabulario por finding es `DECISIONAL_IMPACT|PLAN_IMPACT|EVIDENCE_IMPACT|NONE`).
- **Adjudicación:** la clasificación primaria es del evaluador independiente; las disputas de clase **y de mapping** que puedan cambiar `VALUE_RETENTION`, `IMPACT_RETENTION` o `SPURIOUS_SHARE` las resuelve el **ADJUDICADOR** independiente (no el Lead), con la variante adjudicada y la sensibilidad registradas. Una disputa insoluble que pueda cambiar la decisión ⇒ `DEFER` (D2), no elección del Lead.

### 9.6 Retención: definición congelada (v2; **antes de ejecutar**)

- **`FULL_SET` (primario)** = findings **distintos** `(NEW|DERIVED) + MATERIAL` producidos por las operaciones que MAR conserva en la condición FULL: **DEFENSE + PROSECUTION** (y la síntesis si produjera alguno material; por evidencia 0). **Quedan excluidos** los findings producidos **solo** por REBUTTAL, porque MAR no tiene esa operación por diseño; se declara que esto fija el **techo estructural** de retención (en la campaña, R-2 aportó 1 `DMN` por trial de 4 pasadas; ≈2/17 pooled). Como **sensibilidad**, se computa `VALUE_RETENTION_ALL` con `FULL_SET_ALL` = `FULL_SET` + findings materiales nuevos solo de REBUTTAL, y se reporta el techo.
- **`MIN_SET`** = findings distintos `(NEW|DERIVED)+MATERIAL` producidos por la condición MAR (PASS 1 + PASS 2; síntesis no produce).
- **`MAPPING`** = mapa declarado `FULL_ID → MIN_ID` que afirma **el mismo hecho y la misma consecuencia material**. Regla conservadora operacionalizada: el par es válido solo si el finding de MAR **cita explícitamente** el hecho del finding FULL y **su consecuencia concreta** (se cita el pasaje); pares por similitud de tema se **excluyen** y se listan como inválidos. Los bundles (varios `FULL_ID` → un `MIN_ID`) se reportan, pero un `MIN_ID` **no** acredita consecuencias que no afirma.
- **`RETAINED`** = entradas válidas de `MAPPING` con `FULL_ID ∈ FULL_SET` y `MIN_ID ∈ MIN_SET`.
- **`VALUE_RETENTION = |RETAINED| / |FULL_SET|`**. Si `|FULL_SET| = 0`: no se calcula ratio, se reporta el valor absoluto de MAR y el experimento es `DEFER` para la decisión (no `REJECT`, salvo `|MIN_SET| = 0`). Si `|FULL_SET| < 3`: ratio demasiado grueso para decidir; se reportan conteos y `DEFER` (declarado a priori).
- **`IMPACTFUL_FULL`** = subconjunto de `FULL_SET` que una fila de impacto **atribuido** de FULL cita (bundle permitido). **El mapa NO transfiere impacto:** para cada par retenido, el evaluador registra si el finding de MAR satisface **independientemente** la atribución estricta (`:§10`) **en la condición MAR**; **`IMPACTFUL_MIN` = pares retenidos con `FULL_ID ∈ IMPACTFUL_FULL` y atribución independiente verificada** (así el numerador queda restringido al denominador y `IMPACT_RETENTION ≤ 1`). Un impacto MAR fuera de `IMPACTFUL_FULL` se reporta aparte y **no** cuenta para `IMPACT_RETENTION`. `IMPACT_RETENTION = |IMPACTFUL_MIN| / |IMPACTFUL_FULL|` (si `IMPACTFUL_FULL` está vacío, la condición de impacto es **N/A**, no incumplida).
- **"Suficiente valor" (a priori, no derivado de T1–T3):** `VALUE_RETENTION ≥ 0,60` **y** (`IMPACT_RETENTION ≥ 0,60` **o** `IMPACTFUL_FULL = ∅`) **y** ≥ 1 finding retenido con `impact ≠ NONE` atribuido **independientemente en MAR**. El 0,60 es un umbral experimental elegido a priori por el Lead, **no** una derivación de la campaña; se reporta junto a conteos absolutos y el techo estructural. Reducir mucho el coste perdiendo todo el valor material es **fracaso**, no éxito.

### 9.7 Regla de decisión congelada y **total** (v2; prioridad en este orden)

Vocabulario: `RETENTION` = `VALUE_RETENTION` (cuando se nombran ambas, son ambas).

```text
 0. PRECONDICIÓN: disputa de clase o de mapping insoluble que pueda cambiar
    VALUE_RETENTION / IMPACT_RETENTION / SPURIOUS_SHARE / la decisión → DEFER
    (prevalece sobre cualquier fila posterior; D2)
 1. D3 / experimento INVALID                                    → DEFER
 2. |MIN_SET| = 0                                                → REJECT
 3. |FULL_SET| = 0 (o |FULL_SET| < 3)                            → DEFER (con anexo de valor absoluto)
 4. VALUE_RETENTION < 0,40                                       → REJECT
 5. VALUE_RETENTION ≥ 0,60 ∧ IMPACTFUL_FULL ≠ ∅
      ∧ IMPACT_RETENTION < 0,60                                  → REFINE
 6. VALUE_RETENTION ≥ 0,60 ∧ (IMPACT_RETENTION ≥ 0,60 ∨ IMPACTFUL_FULL = ∅)
      ∧ ≥1 finding retenido con impacto atribuido en MAR
      ∧ COST_RATIO ≤ 2,0 ∧ SPURIOUS_SHARE ≤ 0,15                 → ADOPT_DEV_EXPERIMENT
 7. VALUE_RETENTION 0,40–0,59 ∧ COST_RATIO ≤ 2,0                 → REFINE
 8. VALUE_RETENTION 0,40–0,59 ∧ COST_RATIO > 2,0                 → DEFER
 9. VALUE_RETENTION ≥ 0,60 ∧ (COST_RATIO > 2,0 ∨ SPURIOUS_SHARE > 0,15) → REFINE
10. otro caso                                                    → DEFER
```

`COST_RATIO` = `EFFECTIVE` de la condición `TWO_PASS` ejecutada (§9.4); el `SINGLE_PASS` es sensibilidad y **no** sustituye. `SPURIOUS_SHARE` según §9.5. La fila 0 es una **precondición** que prevalece; las filas 1–10 son exhaustivas y excluyentes por orden.

- `ADOPT_DEV_EXPERIMENT`: adoptar el **experimento DEV**, no el Protocol; capacidad experimental/advisory; se propone (no se ejecuta) su continuidad.
- `REFINE`: el mecanismo funciona pero requiere otra iteración (coste, ruido o retención parcial).
- `REJECT`: la reducción destruye el valor material o no hay valor.
- `DEFER`: evidencia insuficiente (incluye regla no aplicable y disputa insoluble).
- Ningún resultado modifica el Protocol, crea autoridad ni obliga. **No se cambia la regla después de ver resultados.**

### 9.8 Comparaciones de referencia (v2)

- **Contra FULL en el mismo caso:** retención primaria y `_ALL` (sensibilidad), duplicación/espuriedad, impacto, coste.
- **Contra T2/T3:** `COST_RATIO` (`EFFECTIVE`) vs 4,01×/5,21× (`SELF`) con la comparabilidad declarada (§8), y objetivo ≤ 2,0×. T1 se cita como 2,35× pero **no** se poolea. Los trials previos no se re-ejecutan.
- **Eficiencia:** `DMN` por 1 000 agent-seconds y por 1 000 palabras (comparables solo con la misma taxonomía).
- **Trigger:** recomendación sobre las siete señales declaradas + decisión de invocación registrada. **`M-H4` no se mide en §9**: solo hay tests unitarios de la regla; precisión/recall reales quedan en §10 ítem 6. No se presenta como validación de H4.

### 9.9 Desviaciones declaradas de antemano (v2)

1. **Ejecución completa de `TWO_PASS`** aunque la regla de parada por presupuesto habría detenido el mecanismo tras PASS 1: necesario para medir retención y coste real; el contrafáctico `SINGLE_PASS` se reporta como sensibilidad.
2. **FULL es una réplica del mecanismo T2/T3 sobre un caso nuevo**, no una re-ejecución de T2/T3; REBUTTAL es condicional.
3. **Caps no medidos previamente:** ≤6 findings/pasada, ≤700 palabras/pasada, ≤500 síntesis son variables de tratamiento `HYPOTHESIS`; un sobrepaso se registra como D2 y las palabras/findings reales se reportan. FULL es el comparador sin cap.
4. **Evaluadores/adjudicador/integridad no son doble-ciego:** conocen la identidad de las condiciones y el caso (no el orden ni las hipótesis del Lead), y no se afirma independencia; mitigación = instrucciones congeladas, mapa completo publicado, adjudicación independiente.
5. **Un solo caso** (`n=1`): no se generaliza; `ADOPT_DEV_EXPERIMENT` solo justifica continuar experimentando.
6. **Mismo modelo/proveedor:** separación procedural, no independencia epistémica.
7. **Sin instrumentación de tokens:** coste en agent-seconds y palabras; `SELF` incluye latencia de herramientas.
8. **El caso reaparece la forma de T2** (regla declarada sin realización en el ejecutor) y tiene pre-análisis con inclinación declarada; no invalida la comparación FULL vs MAR sobre el mismo caso, pero limita la generalización y el descubrimiento absoluto.
9. **La FRAME y el ledger viven en staging antes de Commit 1**; la FRAME se commitea como `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md` (Git-verificable) y el ledger se define en §9.10.

### 9.10 Evidencia de orden, ledger y protección contra razonamiento motivado (v2)

- **Preregistro:** este documento se commitea antes de ejecutar (orden verificable por Git).
- **FRAME:** el texto de `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md` (v2) es el objeto congelado Git-verificable; su sha256 se registra en el ledger y en el informe. El archivo de staging es copia operativa; si discrepa, **gobierna el archivo versionado**.
- **Ledger (definido):** registro **append-only y encadenado por hash**, en `sessions/minimal-adversarial-review/LEDGER.md` (staging no versionado, PC-44/PC-45). Entradas: SHA del Commit 1; sha256 del FRAME; para BASELINE: inicio/fin, `SELF`, `LEAD`, sha256 del artefacto, registrado **antes** de cualquier pasada del tratamiento; para cada pasada: condición, inicio/fin, `SELF`, `LEAD`, palabras, sha256 del artefacto, hash de compromiso; desviaciones con clase. Cada entrada incluye el hash de la entrada anterior. El ledger se reproduce resumido en el informe de validación; al no ser versionado, la evidencia de orden es **atestiguada** con hashes y se declara esa limitación.
- **Anti-razonamiento motivado:** no se re-clasifican findings después de ver la retención; clasificación primaria congelada antes de calcular ratio; mapa completo y pares inválidos publicados; adjudicación independiente para disputas; cualquier cambio de método es desviación con efecto declarado.


---

## 10. Qué evidencia justificaría una promoción futura

`RECOMMENDATION` no autoritativa. Antes de proponer cualquier adopción DEV (y mucho antes de tocar el Protocol) se necesitaría:

1. **Replicación** en ≥ 2 casos adicionales **no pre-analizados**, con evaluación independiente y el mismo preregistro.
2. **Retención** ≥ 0,60 (`VALUE_RETENTION` e `IMPACT_RETENTION`) en cada caso, con mapas auditables.
3. **Coste** ≤ 2,0× en cada caso (o un umbral alternativo justificado con evidencia y documentado antes de cambiarlo).
4. **Ruido** `SPURIOUS_SHARE ≤ 0,15` y `DUPLICATE_SHARE` no superior a la del mecanismo completo en el mismo caso.
5. **Impacto** ≥ 1 finding con impacto atribuido en al menos un caso, con bundle declarado.
6. **Trigger** con precisión/recall medidos sobre casos reales y sintéticos; nunca un clasificador automático.
7. **Sin violaciones de autoridad/estado** (verificadas por el prototipo y por auditoría) y sin consumidores automáticos no autorizados.
8. Solo entonces: propuesta de adopción DEV con su plan autorizado; la promoción al Protocol exige su propio camino RFC-56 (Clase A) y evidencia adicional; no se infiere de este experimento.

---

## 11. Respuestas a las preguntas de la iniciativa (§21)

1. **¿Cuál es el mecanismo mínimo?** FRAME congelado → 1–2 pasadas adversariales acotadas (falsificación siempre; caso favorable condicional) → síntesis corta por criterio que no crea findings → resultado advisory con impacto y desacuerdo preservado. Sin rebuttal, sin veredicto como entidad, sin voting.
2. **¿Qué partes de la deliberación completa son necesarias?** PROSECUTION es el núcleo (11/17 `DMN`); DEFENSE solo es necesaria para una reversión decisional advisory (T3); SYNTHESIS/CRITERION COMPARISON no produjo findings y se reduce a comparación; REBUTTAL no cambió veredictos/recomendaciones y se elimina; VERDICT no se sostiene como entidad.
3. **¿Qué valor conserva?** `HYPOTHESIS` a medir en §9: `VALUE_RETENTION ≥ 0,60` sobre el `FULL_SET` primario (operaciones que MAR conserva; rebuttal-only excluido), `IMPACT_RETENTION ≥ 0,60` o `IMPACTFUL_FULL = ∅`, y ≥ 1 finding retenido con impacto **atribuido independientemente en MAR**; se reporta además la sensibilidad `_ALL` y el techo estructural. No se afirma antes de medir.
4. **¿Cuánto cuesta?** `HYPOTHESIS` ≤ 2,0× (`EFFECTIVE` de `TWO_PASS` ejecutada); referencia completa 4,01×/5,21× (`SELF` T2/T3). El experimento mide `COST_RATIO`, reporta `RATIO_SELF`/`RATIO_LEAD` y el contrafáctico `SINGLE_PASS` como sensibilidad.
5. **¿Cuándo debería activarse?** Solo cuando las señales declaradas lo justifiquen (materialidad/ambigüedad/riesgo/irreversibilidad/coste del error); recomendación advisory + decisión de invocación independiente registrada; nunca gate ni clasificador automático. **`M-H4` no se valida en §9** (solo tests unitarios; precisión/recall quedan en §10 ítem 6).
6. **¿Qué autoridad tiene?** Ninguna: evidencia advisory; la autoridad existente decide; no escribe estados, no autoriza, no ejecuta.
7. **¿Cómo se preserva provenance?** Un finding por afirmación con fuente/pasada/ejecutor, evidencia, novedad, materialidad, impacto, consecuencia y motivo de descarte; IDs locales; mapa de retención declarado; sin IDs globales ni findings del lifecycle.
8. **¿Cómo se conserva el disagreement?** Estados explícitos y posiciones preservadas; la síntesis no resuelve por mayoría ni elimina la minoría; el prototipo hace inválido un registro que pierde un desacuerdo material.
9. **¿Cómo se integra con DEV?** No hay punto de integración limpio; se ejecuta manualmente y se registra como Working/sesión; el prototipo es una librería read-only sin consumidor; la integración es documental (provenance por referencia), sin estado/registry/gate.
10. **¿Qué evidencia justificaría su promoción?** §10: replicación en casos no pre-analizados, retención y coste en cada caso, ruido acotado, impacto, trigger medido, sin violaciones de autoridad; y aun así, promoción DEV con plan autorizado y Protocol solo por RFC-56.

---

## 12. Estado, límites y no-conclusiones

- **Estado:** experimental, Working, no normativo, sin autoridad. El prototipo no está integrado ni consumido.
- **No se concluye:** que la deliberación adversarial "mejora las decisiones"; que Jury deba desaparecer; que voting no sirva; que los evaluadores sean epistémicamente independientes; que el mecanismo deba ejecutarse en todos los Changes; que el Protocol deba cambiar.
- **Conclusión correcta actual (heredada y no ampliada):** la evidencia disponible **no justifica** Court/Jury con voting y **apunta experimentalmente** hacia una revisión adversarial mínima; si el experimento §9 no conserva valor, la conclusión correcta será reducir o descartar también el mínimo.
- **Limitaciones globales:** `n=1` para el experimento de validación; mismo modelo/proveedor; casos con pre-análisis; coste en agent-seconds (sin tokens); sin aislamiento técnico de pasadas; el baseline es un agente instruido.
- **Riesgo principal:** construir un mecanismo pequeño que parezca barato porque dejó de mirar lo que producía el valor. El experimento mide retención, no solo coste.

---

## 13. Trazabilidad

`Priority 3.7` (insumo local del mantenedor, no versionado) → campaña T1–T3 (`docs/working/research/ADVERSARIAL_DELIBERATION_EXPERIMENT_2026-10-25.md`; `..._TRIAL_1_2026-10-25.md`; `..._PREREGISTRATION_2_3_2026-10-25.md`; `..._TRIALS_2_3_2026-10-25.md`) → decisión `REFORMULATE` y recomendación de Adversarial Review mínima (`..._TRIALS_2_3_2026-10-25.md:8.3`) → esta iniciativa (plan 179) → este diseño + preregistro → prototipo `runtime/adversarial_review/` → experimento de validación (§9) → informe `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_VALIDATION_2026-10-25.md` → decisión experimental (`ADOPT_DEV_EXPERIMENT` | `REFINE` | `REJECT` | `DEFER`) → posible trabajo futuro (nuevo plan autorizado; Protocol solo por RFC-56).

**Contención:** este documento no cita insumos locales no versionados como `ruta:sección` y no cita artefactos de staging (`sessions/`) como provenance. El experimento tiene dos objetos internos que viven en staging durante la ejecución —la copia operativa del FRAME y el ledger—: el FRAME **se versiona** como `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md` (objeto congelado) y el ledger se describe en §9.10 y se resume en el informe de validación, que es la fuente versionada de los valores medidos.

---

## 14. Registro de corrección pre-freeze (v1 → v2, 2026-10-25)

Esta sección registra la revisión independiente pre-ejecución (artefacto de staging, no citable como provenance; PC-44/PC-45) y su disposición, para que la corrección no sea silenciosa. **Ninguna pasada se ejecutó antes de la v2.** El registro de disposición es el siguiente (aceptado = incorporado; parcial = incorporado con alcance declarado; rechazado = no incorporado, con razón):

| Finding | Severidad | Disposición | Dónde se corrigió |
|---|---|---|---|
| `PRE-F01` regla de decisión no total | BLOCKING | **Aceptado** | §9.6 (denominador/impacto/N-A/min-denominador), §9.7 (regla exhaustiva y excluyente) |
| `PRE-F02` coste no congelado a un run/método | BLOCKING | **Aceptado** (v2: `SELF`/`LEAD`/`EFFECTIVE`; primario = `EFFECTIVE` de `TWO_PASS` ejecutada; `SINGLE_PASS` solo sensibilidad) | §8, §9.4, §9.7 |
| `PRE-F03` recepción de material indefinida; síntesis sin baseline | BLOCKING | **Aceptado** | §9.2 tabla de condiciones, §9.3 punto 3, FRAME v2 `## RECEPCIÓN DE MATERIAL` |
| `PRE-F04` techo de contaminación incompleto; Commit 1 crea exposición; HEAD ≠ HEAD | BLOCKING | **Aceptado** | §9.1, FRAME v2 `## MATERIAL PROHIBIDO Y EXPOSICIÓN`, `## CONTAMINATION CEILING` |
| `PRE-F05` ledger indefinido; FRAME no versionado; claim Git; plan paso 8 | BLOCKING | **Aceptado** | §9.10 (ledger append-only hash-chained), FRAME versionado (`..._FRAME_01_2026-10-25.md`), plan 179 pasos 7–8 corregidos |
| `PRE-F06` denominador incluye rebuttal-only | REQUIRED | **Aceptado** (primario excluye rebuttal-only; `_ALL` y techo reportados) | §9.6 |
| `PRE-F07` semántica de caps indefinida / cap no validado | REQUIRED | **Aceptado** (caps = instrucción a la pasada; no poda; sobrepaso D2; prototipo no valida el cap de findings) | §4.5, §6.3, §9.9 item 3 |
| `PRE-F08` sin adjudicador para clase/mapping | REQUIRED | **Aceptado** (pasada `ADJUDICACIÓN` independiente; disputa insoluble ⇒ `DEFER`) | §9.2, §9.5, §9.7 fila 10 |
| `PRE-F09` `SPURIOUS_SHARE` sin definir ni citar | REQUIRED | **Aceptado** | §9.5 (definición, cita `:§13.1`, corpus MAR, fragilidad de denominador pequeño) |
| `PRE-F10` el mapa puede transferir impacto; "conservador" indefinido | REQUIRED | **Aceptado** (el mapa no transfiere impacto; atribución independiente en MAR; regla conservadora operacionalizada) | §9.6 |
| `PRE-F11` asimetría/tautología del trigger; conflicto con D7 | REQUIRED | **Aceptado** (regla 4 incluye `error_cost = MEDIUM`; `M-H4` no medida en §9; wording advisory + decisión independiente) | §4.10, §3, §9.8, §11 Q5 |
| `PRE-F12` etiquetas H1–H5 solapadas | REQUIRED | **Aceptado** (namespacing `C-H#` campaña / `M-H#` iniciativa) | §2.4, §3, §4.3, §4.5, §9.8 |
| `PRE-F13` etiquetas y citas de evidencia | REQUIRED | **Aceptado** (corregido en §1, §2.2, §2.3, §2.4, §4.3, §4.6) | las secciones citadas |
| `PRE-F14` deriva §4.4 ↔ prototipo | REQUIRED | **Aceptado** (campo `commit_before_reveal`, campos opcionales marcados, alcance de validación declarado, cap fuera del prototipo) | §4.4, §6.3 |
| `PRE-F15` plan 179 ↔ diseño/FRAME | REQUIRED | **Aceptado** | plan 179 pasos 7–9, delegación, efectos, D-3 |
| `PRE-F16` ceguera del evaluador | ADVISORY | **Aceptado** (declarado no doble-ciego en §9.9 item 4) | §9.9 |
| `PRE-F17` dónde se registran `REWEIGHTING`/`NO ATRIBUIDO`/`DECISION_IMPACT` | ADVISORY | **Aceptado** (nivel de evaluación, no campos del registro) | §9.5 |
| `PRE-F18` lenguaje "Integration Surface" y contención | ADVISORY | **Aceptado** (sigue siendo lenguaje experimental no contractual; §13 corregido) | §6.2, §13 |
| `PRE-F19` anclas de la FRAME | ADVISORY | **Aceptado** (behavior-patterns §2.2; superficies hipotéticas sin autorización) | FRAME v2 |
| `PRE-F20` umbral 0,60 y denominador pequeño | ADVISORY | **Aceptado** (0,60 declarado a priori, no derivado; conteos absolutos; `|FULL_SET| < 3` ⇒ `DEFER`) | §9.6, §9.7 |

**Delta v1 → v2 (resumen):** preregistro total y excluyente; método de coste congelado con primario y sensibilidad; recepción de material declarada y simétrica con baseline en las síntesis; FRAME versionado con techo de contaminación completo y material prohibido; ledger definido; denominador de retención sin techo estructural oculto; impacto no heredado por el mapa; adjudicación independiente; trigger corregido y H4 declarada no medida; etiquetas de hipótesis separadas; correcciones de etiquetas/citas de evidencia; alineación diseño↔prototipo↔plan.

**Declaraciones de pre-ejecución incorporadas** (checklist del revisor): ledger y hashes (§9.10); commits/HEAD y verificación de anclas (§9.1); recepción de material (§9.2/FRAME); material prohibido y no doble-ciego (§9.1/FRAME/§9.9); techo de contaminación corregido (§9.1); evaluador/adjudicador (§9.2/§9.5/§9.9); semántica de caps y conteo de palabras (§4.5/§9.4); método de coste (§8/§9.4); regla total (§9.7); denominador de retención (§9.6); FULL como réplica y rebuttal condicional (§9.2); trigger y no-validación de H4 (§9.1/§9.8); no-claims (§12); y este registro de disposición.

