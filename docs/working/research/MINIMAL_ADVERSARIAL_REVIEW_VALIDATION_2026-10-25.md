# Minimal Adversarial Review — informe de validación (experimento MAR-VALID-01)

> **Clase documental:** Working / Research — **no normativo** (`docs/AGENTS.md:Naturaleza documental`). Evidencia experimental; nunca autoridad.
> **Estado:** `EXPERIMENTO EJECUTADO — RESULTADO: REJECT` (decisión experimental según la regla congelada; no modifica el Protocol, no crea autoridad, no promueve la capacidad).
> **Origen:** plan 179 (`docs/plans/179-minimal-adversarial-review.md`); diseño y preregistro congelado v2 (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md:9. PREREGISTRO CONGELADO del experimento de validación (v2 — corregido antes de ejecutar)`); FRAME congelado (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md`); prototipo (`runtime/adversarial_review/`).
> **Etiquetas:** `OBSERVED`, `MEASURED`, `INFERRED`, `HYPOTHESIS`, `RECOMMENDATION`.
> **Evidencia de orden:** Commit 1 `ca492ca1969a32841638ca6913251c83502a7e70` materializa el preregistro, el FRAME y el prototipo **antes** de ejecutar. Los artefactos crudos y el ledger del experimento viven en staging no versionado (objetos internos, no citables como provenance); sus hashes y el ledger se resumen aquí, que es el registro versionado de los valores medidos.

---

## 1. Resumen ejecutivo

**`FINAL_DECISION = REJECT`** — aplicando la regla congelada del preregistro (§9.7), fila 4: `VALUE_RETENTION = 6,67 % < 0,40`.

| Métrica congelada | Valor medido | Umbral de la regla | Resultado |
|---|---:|---|---|
| `FULL_SET` (findings materiales nuevos del mecanismo completo retenidos por operación) | **15** | — | — |
| `MIN_SET` (findings materiales nuevos de MAR) | **2** (`P1-F4`, `P1-F5`) | `|MIN_SET| = 0` ⇒ `REJECT` | no dispara |
| `RETAINED` (pares válidos del mapa `FULL→MIN`) | **1** (`P-7a → P1-F5`) | — | — |
| **`VALUE_RETENTION`** | **6,67 %** (1/15) | ≥ 60 % para `ADOPT`; < 40 % ⇒ `REJECT` | **`REJECT`** |
| `IMPACTFUL_FULL` / `IMPACTFUL_MIN` / `IMPACT_RETENTION` | 5 / 1 / **20,0 %** | ≥ 60 % (o N/A) | no alcanzado |
| **`COST_RATIO` (`EFFECTIVE`, `TWO_PASS` ejecutada)** | **1,28×** (SELF 1,283; LEAD 0,980) | ≤ 2,0× | **cumplido** |
| `SPURIOUS_SHARE` (MAR, corpus distinto) | **10,0 %** (1/10) | ≤ 15 % | cumplido |
| `DUPLICATE_SHARE` (MAR) | **60 %** (6/10; convención de etiquetas del adjudicador: 70 %) | — | informativo |
| `EXPERIMENT_INTEGRITY` | `VALID_WITH_LIMITATIONS` | sin D3 | válido |

**Lectura:** la reducción **sí alcanzó el objetivo de coste** (1,28× ≤ 2,0×; frente a 4,01×/5,21× de la campaña y 2,32× del mecanismo completo en este mismo caso), pero **destruyó la mayor parte del valor material**: conservó 1 de los 15 findings materiales nuevos del mecanismo completo (6,67 %) y 1 de los 5 con impacto atribuido (20 %), muy por debajo del 60 % preregistrado. El coste bajo no compensa la pérdida de valor. La hipótesis negativa `M-H5` queda **confirmada para esta configuración** (dos pasadas acotadas a ≤700 palabras/≤6 findings + síntesis ≤500 palabras).

**Qué no significa `REJECT`:** no significa que "toda revisión adversarial mínima sea inútil", ni que Jury deba desaparecer, ni que voting no sirva, ni que el Protocol deba cambiar. Significa que **esta** configuración mínima, bajo estas condiciones y este presupuesto, no conserva suficiente valor. Una reducción distinta (p. ej. falsificación a profundidad completa sin caps) es una `HYPOTHESIS` futura **no probada aquí** y **no implementada**.

---

## 2. Experimento ejecutado

- **Caso:** `MAR-VALID-01` — cierre derivado del host (`CLOSED_DERIVED`) y registro `## Checkpoint / cierre` frente a las determinaciones de impacto de cierre §5.1/§5.2/§7. FRAME congelado en `docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md`; evidencia verificada a `ac7f680`; ejecución sobre `ca492ca`.
- **Condiciones:** BASELINE (análisis normal, congelado antes del tratamiento), FULL (DEFENSE + PROSECUTION aisladas con commit-before-reveal + SYNTHESIS + REBUTTAL condicional), MAR (PASS 1 falsificación + PASS 2 caso favorable aisladas + síntesis corta), EVALUACIÓN independiente, ADJUDICACIÓN independiente, INTEGRIDAD.
- **FULL ejecutó 3 pasadas:** la síntesis decidió `NO_REBUTTAL` (el desacuerdo decisivo —si §7 "Closure" es condición derivada o acto— requiere una decisión normativa, no más argumento/evidencia; una réplica que la produjera usurparía autoridad). El preregistro §9.2 hacía el REBUTTAL condicional exactamente a esta situación; se registra como condición ejecutada, no como desviación.
- **Recepción de material:** declarada y simétrica (§9.2/FRAME); BASELINE cerrado recibido por ambas síntesis; las pasadas de evaluación de FULL y MAR recibieron solo el FRAME; los ejecutores declararon `material_received`/`withheld_material` y la integridad auditó la exposición.
- **Pared dura de orden:** cumplida. El BASELINE terminó y se congeló (`19:52:55`, hash registrado) **80,18 s antes** del primer START del tratamiento (`19:54:15`). Commit 1 precede al baseline.
- **Integridad:** `VALID_WITH_LIMITATIONS`; **ningún D3**; desviaciones `D2`: (I-01) el paréntesis de la base de evidencia del FRAME sobre `runtime/README.md` es falso — el README sí contiene "Documentation impact"/"Roadmap impact" en L350–351, aunque el hecho sustantivo (ningún código las lee) se sostiene y fue verificado por todas las condiciones; (I-03) materialidad de defectos de ancla excluida del cómputo por instrucción; (I-04) un finding candidato solo-síntesis declarado y excluido del primario. `D1` (instrumento/medición): preimagen del ledger sin `|` final y normalización ASCII en dos entradas, palabras ±1–14, LEAD de etapa paralela contado una vez, no doble-ciego, `TWO_PASS` predeclarado, exposición declarada del grep del FRAME y de `git diff --stat`, orden atestiguado (ledger en staging), reloj de la adjudicación. **Frontera declarada:** si se leyera que cualquier falsedad de la base de evidencia del FRAME es "punto material", I-01 sería D3 ⇒ `DEFER`; el informe mantiene D2 porque no afecta a la pregunta, la candidata, los criterios ni a ninguna conclusión de las pasadas (el hecho sustantivo se verificó de forma independiente en todas ellas).

---

## 3. Coste medido

Método congelado (§8/§9.4): `SELF` = reloj del ejecutor; `LEAD` = reloj del Lead; `EFFECTIVE = max(RATIO_SELF, RATIO_LEAD)`; primario = `EFFECTIVE` de `TWO_PASS` ejecutada; evaluación/adjudicación/integridad = overhead de investigación, fuera del ratio. `LEAD` de etapas paralelas contado una vez (cota inferior de wall-clock).

| Condición | SELF (s) | LEAD (s) | palabras | llamadas | pasadas | RATIO_SELF | RATIO_LEAD | EFFECTIVE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BASELINE | 391,14 | 450 (ventana) | 5 088 | ~59 | — | 1,00 | 1,00 | 1,00 |
| FULL (D+P+S) | 908 | 659 | 9 744 | ~148 | 3 | 2,321 | 1,464 | **2,32×** |
| MAR `TWO_PASS` (P1+P2+S) | 501,7 | 339 | 1 842 | 88 | 2 | 1,283 | 0,753 | **1,28×** |
| MAR `SINGLE_PASS` (solo P1) — sensibilidad | 163,0 | 160 | 669 | 35 | 1 | 0,417 | 0,356 | 0,42× |
| EVALUACIÓN (overhead) | 475,4 | 480 | 8 464 | ~60 | — | n/a | n/a | n/a |
| ADJUDICACIÓN (overhead) | 323,9 | 330 | 4 809 | ~35 | — | n/a | n/a | n/a |
| INTEGRIDAD (overhead) | 613,0 | 620 | 5 884 | ~80 | — | n/a | n/a | n/a |

`MEASURED`. Referencias de campaña: T2 4,01×/T3 5,21× (`SELF`), T1 2,35× (método/taxonomía previos, no pooleable). **El multiplicador de coste no es portable entre casos y métodos**: aquí el BASELINE fue mucho más largo (5 088 palabras / 391 s) que los baselines de la campaña (≈2 198 palabras / ≈288 s), de modo que el "mecanismo completo" costó 2,32× en este caso frente a 4,01×–5,21× en T2/T3. Por eso el informe reporta también valores absolutos (agent-seconds y palabras) y no solo ratios.

**H2 (coste):** la configuración MAR cumple el objetivo ≤ 2,0× (`EFFECTIVE` 1,28×; `SINGLE_PASS` 0,42× como sensibilidad). La reducción de coste frente al mecanismo completo en el mismo caso es 908 → 501,7 s (‑44,7 %) y 9 744 → 1 842 palabras (‑81,1 %). El objetivo de coste **no fue la restricción vinculante**; la restricción que falló fue la retención de valor.

---

## 4. Valor: findings, retención e impacto

### 4.1 Sets congelados

- **`FULL_SET` = 15** findings distintos `(NEW|DERIVED)+MATERIAL` de FULL DEFENSE+PROSECUTION: `D-4, D-7, D-10, D-11, P-4, P-5, P-6, P-7a, P-7b, P-8, P-9, P-10, P-11, P-12, P-13`. (`FULL_SET_ALL` = 16 con un candidato solo-síntesis `M-9` declarado y excluido del primario; no hay rebuttal-only porque FULL no ejecutó rebuttal.)
- **`MIN_SET` = 2**: `P1-F4` (el acto operativo es la escritura del registro — E1-D4 congela el Plan; `derive_next_action` es lectura pura) y `P1-F5` (no existe cierre del host bajo las determinaciones: n=0; los dos cierres reales son legacy).
- **Corpus MAR:** 12 findings en bruto → **10 átomos distintos** (fusiones por contenido: `P1-F3≡P2-F3`, `P1-F6≡P2-F6`). Duplicados 6 (60 %), espurias 1 (10 %: `P1-F1`, confusión "no es una entidad-gate" ⇔ "no puede leerse como precondición", inferencia no sostenida), no materiales 1 (defecto de ancla del FRAME), materiales nuevos 2.

### 4.2 Mapa de retención (conservador)

Un par es válido solo si el finding de MAR **afirma explícitamente el mismo hecho y la misma consecuencia concreta** del finding FULL (cita textual). Resultado: **1 par válido** — `P-7a → P1-F5` (mismo hecho: cierres del host anteriores a §5.1/§5.2; misma consecuencia: "modo de fallo no observado / materialidad prospectiva no demostrada"). Los otros 14 `FULL_SET` quedaron sin par; near-misses declarados y rechazados: `P-12→P1-F3`, `P-10→P1-F4`, `P-5→P1-F2` (fallan "misma consecuencia explícita"). Sin bundles.

**`VALUE_RETENTION = 1/15 = 6,67 %`.** Sensibilidad declarada: con la lectura "estricta" de materialidad (solo consecuencias que cambian un objeto de decisión; no admisible según la definición congelada) `FULL_SET` sería 5 y `VALUE_RETENTION` 20 %; con `FULL_SET_ALL` 1/16 = 6,25 %. **Ninguna variante alcanza 40 %.** El umbral de 60 % es una elección a priori del Lead (declarada, no derivada de T1–T3) y queda muy por encima de lo medido.

### 4.3 Impacto atribuido (estricto)

- `IMPACTFUL_FULL` = 5: `P-8` (DECISIONAL), `P-9`, `P-10`, `P-13` (PLAN), `P-7a` (EVIDENCE).
- `IMPACTFUL_MIN` = 1: `P1-F5` (EVIDENCE_IMPACT, atribución independiente en la condición MAR: la síntesis MAR lo cita y el contrafáctico sostiene "gather evidence").
- **`IMPACT_RETENTION = 1/5 = 20 %`** (no N/A).
- **Corrección verificada:** la síntesis MAR declaró 4 `DECISIONAL_IMPACT`; bajo atribución estricta **0/4 sobrevive** (3 son duplicados y `P1-F4`/`P2-F5` no se citan en la base de la recomendación). El único impacto MAR verificado es un requisito de evidencia. Esto es exactamente el tipo de sobreafirmación que la regla estricta de la campaña evita.

### 4.4 Prototipo aplicado al registro real

El prototipo `runtime/adversarial_review/` se aplicó al registro MAR compuesto con los artefactos del experimento (staging) y devolvió: `validate` → `ok: true`, **0 issues** (provenance, vocabularios, presupuesto de palabras, desacuerdos preservados, sin campos de autoridad/voto/juez); `review_metrics` → `distinct_material_new = 2`, `cost_multiplier = 1,2827`, `budget.status = WITHIN_TARGET`, `words_multiplier = 0,3620`; `retention_metrics` → `value_retention = 0,0667`, `impact_retention = 0,20`, `unmatched_full` = 14 IDs; `selectivity` con las señales declaradas → `REVIEW_TWO_PASS` (advisory). El registro del experimento pasó la validación determinista del prototipo sin ediciones de clasificación. Esta es la primera aplicación del prototipo a datos reales (dogfood del instrumento, no del mecanismo).

---

## 5. Evaluación, adjudicación e integridad

- **EVALUACIÓN independiente:** 37 clasificaciones de materialidad/novedad/impacto; `FULL_SET` 15, `MIN_SET` 2, retención 1/15; tres incertidumbres declaradas (U1 `P1-F1` espuria vs material; U2 lectura estricta de materialidad; U3 `P-5` novedad).
- **ADJUDICACIÓN independiente:** 37/37 clasificaciones de materialidad aceptadas, 0 rechazadas, 5 correcciones de **etiqueta de novedad** (sin cambio de sets), mapa confirmado (1 par válido, 14 rechazos confirmados, sin bundles). Resolvió U1 (`SPURIOUS` confirmado), U2 (la lectura estricta no es la definición congelada; sensibilidad 20 % declarada), U3 (`P-5` no duplicado; etiqueta `DERIVED`). **Ninguna disputa es insoluble ni decision-critical**: `VALUE_RETENTION` 6,67 % (<40 %), `IMPACT_RETENTION` 20 % (<60 %), `SPURIOUS_SHARE` 10 % (≤15 %) en todas las variantes plausibles; el techo estructural de `IMPACT_RETENTION` es 50 % y ninguna variante alcanza 60 % de retención.
- **INTEGRIDAD:** `VALID_WITH_LIMITATIONS`; hashes 9/9 reproducen; cadena del ledger encadenada (con dos defectos de instrumentación D1, corregidos como errata append-only); anclas del FRAME verificadas contra `ac7f680` y sin drift entre `ac7f680` y `ca492ca`; exposiciones declaradas y auditadas (ninguna lectura prohibida acreditada); conteos de la evaluación recomputados y consistentes; desviaciones clasificadas (sin D3).

---

## 6. Aplicación de la regla congelada (§9.7)

| Fila | Condición | Resultado |
|---|---|---|
| 0 (precondición) | disputa insoluble decision-critical | No (adjudicación: ninguna) |
| 1 | D3 / INVALID | No (integridad: ningún D3) |
| 2 | `|MIN_SET| = 0` | No (2) |
| 3 | `|FULL_SET| = 0` o < 3 | No (15) |
| 4 | **`VALUE_RETENTION < 0,40`** | **Sí (6,67 %)** ⇒ **`REJECT`** |

Regla aplicada literalmente, sin cambios después de ver resultados. `REJECT` = la reducción destruye el valor material o no hay valor: se conservó 6,67 % del valor material nuevo y 20 % del impacto atribuido. **No se cambia el umbral ni la regla para convertirlo en `REFINE`**: `REFINE` está reservado a retención 40–59 % con coste ≤2,0× o a ≥60 % con coste/ruido fuera de rango; no es el caso.

---

## 7. Hipótesis

- **`M-H1` Value retention — NO SOSTENIDA.** El mecanismo mínimo produce findings materiales nuevos (2) que el baseline no explicitaba, pero conserva solo 6,67 % del `FULL_SET` (umbral 60 %) y 20 % del impacto atribuido (umbral 60 %).
- **`M-H2` Cost reduction — SOSTENIDA (parcialmente).** `COST_RATIO` 1,28× ≤ 2,0× (y 0,42× en el tier de una pasada); reducción de 44,7 % en agent-seconds y 81,1 % en palabras frente al mecanismo completo en el mismo caso. Pero el mecanismo completo de este caso ya costaba 2,32× (no 4–5×): el objetivo ≤2,0× se cumple, y aun así el valor no se conserva.
- **`M-H3` Decision relevance — NO SOSTENIDA.** Solo 1 finding conservado tiene impacto atribuido y es `EVIDENCE_IMPACT`; 0 `DECISIONAL_IMPACT` y 0 `PLAN_IMPACT` sobreviven a la atribución estricta en la condición MAR (los 4 `DECISIONAL` declarados por la síntesis MAR no la resisten).
- **`M-H4` Selectivity — NO MEDIDA.** Solo tests unitarios de la regla; el experimento no ejecutó los tiers `SINGLE_PASS`/`NO_REVIEW` como condiciones ni mide precisión/recall del trigger. El trigger emitió `REVIEW_TWO_PASS`, coherente con las señales declaradas; eso no valida H4.
- **`M-H5` Negative — CONFIRMADA para esta configuración.** Reducir el mecanismo (caps de 700 palabras/6 findings + síntesis corta) eliminó el componente que producía valor: las pasadas completas (≈3 000–3 900 palabras) capturaron 15 findings materiales nuevos; las acotadas (669/693 palabras) produjeron 2, de los cuales solo 1 empareja con el mecanismo completo. La objeción espuria se mantuvo baja (10 %), de modo que el fallo es de **pérdida de valor**, no de ruido.

---

## 8. Comparación con T1–T3 y qué descubrimos

### 8.1 Comparación de coste

| Referencia | Multiplicador | Método/caso |
|---|---:|---|
| T2 | 4,01× | `SELF`; baseline ≈2 198 palabras |
| T3 | 5,21× | `SELF`; baseline ≈2 195 palabras |
| **MAR-VALID-01 FULL** | **2,32×** | `SELF`; baseline 5 088 palabras; 3 pasadas (sin rebuttal) |
| **MAR-VALID-01 MAR** | **1,28×** | `SELF`; misma base; 3 llamadas (2 pasadas + síntesis) |

`INFERRED`: los multiplicadores no son portables entre casos porque dependen de la longitud/ritmo del baseline y del número de pasadas efectivas. La comparación honesta es por valores absolutos y por método declarado; el ratio sirve solo dentro del mismo experimento.

### 8.2 Qué no sabíamos antes de T1–T3 vs qué añade este experimento

**Ya establecido por T1–T3 (`OBSERVED` allí):** hay descubrimiento material reproducible (T2=9, T3=8 `DMN`); el valor se concentra en la falsificación (11/17 `DMN` pooled); la defensa solo aportó un cambio decisional en T3; síntesis y rebuttal no aportaron findings/decisiones atribuibles; el coste completo era 4,01×–5,21×; la recomendación era reformular hacia una revisión mínima **como hipótesis**.

**Nuevo en este experimento (`MEASURED` aquí):**

1. **La receta mínima recomendada por la campaña, implementada tal cual, no conserva el valor.** Dos pasadas + comparación corta, con caps de 700 palabras/6 findings, alcanzan el presupuesto (1,28×) pero retienen 6,67 % del `FULL_SET` y 20 % del impacto atribuido. El "≤2,0×" **no era la restricción vinculante**; los caps de profundidad sí.
2. **El valor observado en T1–T3 dependía de pasadas de profundidad completa.** Aquí las pasadas completas (≈3 000–3 900 palabras) produjeron 15 findings materiales nuevos; las acotadas (≈670–690 palabras) produjeron 2. El mecanismo mínimo no falla por "ruido" (espurias 10 %) sino por **no mirar lo suficiente**.
3. **La capa de veredicto/recomendación vuelve a no ser atribuible:** la síntesis MAR declaró 4 `DECISIONAL_IMPACT`; 0/4 sobrevive a la atribución estricta. La única relevancia decisional verificada es un requisito de evidencia, no un cambio de decisión.
4. **El coste del mecanismo completo depende del caso más de lo que sugerían T2/T3:** en un caso con baseline largo, el mecanismo completo costó 2,32×, no 4–5×. Los umbrales de coste deben fijarse con el método y el caso a la vista, o medirse en valores absolutos.
5. **La integridad de la evidencia del FRAME importa y es detectable:** todas las condiciones encontraron el mismo defecto de ancla del FRAME (paréntesis sobre `runtime/README.md`) sin que cambiara ninguna conclusión; un FRAME con evidencia mal descrita es una fuente de desviaciones `D2` que debe presupuestarse.
6. **El instrumento funciona como instrumento:** el prototipo validó determinísticamente el registro real (0 issues), calculó presupuesto y retención, y aplicó la regla sin intervención del Lead. Es read-only, advisory y sin consumidor —un prototipo viable como *instrumento experimental*, no como mecanismo integrado.

**Ninguna de estas lecciones justifica promover nada al Protocol.** La conclusión correcta es más pequeña: **para este caso y esta configuración, el mecanismo mínimo no conserva suficiente valor; el coste objetivo es alcanzable, pero no es el problema.**

---

## 9. Limitaciones

- `n=1`, un solo caso, con pre-análisis y con inclinación declarada hacia la opción A (Working 2026-09-22) — el valor medido es sobre un baseline informado, no ingenuo.
- Mismo modelo/proveedor en todas las pasadas: separación **procedural**, no independencia epistémica.
- Evaluación, adjudicación e integridad no son doble-ciego; se mitiga con instrucciones congeladas, publicación del mapa completo y adjudicación independiente.
- Coste en agent-seconds y palabras (sin instrumentación de tokens); `SELF` incluye latencia de herramientas; `LEAD` de etapas paralelas es una cota inferior.
- FULL es una réplica del mecanismo T2/T3 sobre un caso nuevo, no una re-ejecución de T2/T3; ejecutó 3 pasadas porque la síntesis decidió `NO_REBUTTAL`.
- La evidencia de orden (ledger, basura de staging) es **atestiguada con hashes**, no impuesta técnicamente; el preregistro y el FRAME son Git-verificables en Commit 1.
- El defecto de ancla del FRAME (I-01) se clasifica D2; bajo la lectura de que cualquier falsedad de la base de evidencia es material, sería D3 ⇒ `DEFER`. No afecta a la pregunta, la candidata, los criterios ni a ninguna conclusión de las pasadas.
- `M-H4` (selectivity) **no se mide** en este experimento; el trigger solo se ejercitó como recomendación declarada y en tests unitarios.

---

## 10. Decisión experimental y siguiente paso

**`FINAL_DECISION = REJECT`** — se rechaza **esta** configuración de Minimal Adversarial Review (dos pasadas acotadas a ≤700 palabras/≤6 findings + síntesis ≤500 palabras) como mecanismo que conserve valor suficiente: cumple el presupuesto (1,28×) pero retiene 6,67 % del valor material nuevo y 20 % del impacto atribuido, por debajo de los umbrales preregistrados.

**Qué NO autoriza ni cambia:** no modifica el Protocol, no modifica `.agents/`, no modifica RFCs/ADRs/planes cerrados, no crea autoridad, no convierte la revisión en obligatoria, no reemplaza Jury y no concluye nada sobre voting. La capacidad DEV `Adversarial Deliberation` existente no se toca.

**Siguiente paso (`RECOMMENDATION`, no ejecutado):** si el mantenedor quiere continuar la línea, el siguiente experimento debería preregistrar una reducción **distinta** —por ejemplo, falsificación dirigida a profundidad completa sin caps (una sola pasada, ~1,1–2,2× según T2/T3) y, si acaso, la defensa condicional a una reversión decisional— y medir retención contra el mecanismo completo con el mismo diseño. Esa hipótesis no se ha probado aquí y no debe presentarse como resultado. Cualquier promoción DEV requeriría un plan autorizado; cualquier cambio del Protocol, su propio camino RFC-56.

---

## 11. Artefactos, evidencia y trazabilidad

- **Versionados:** diseño/preregistro (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md`), FRAME congelado (`docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_FRAME_01_2026-10-25.md`), este informe, plan 179, prototipo (`runtime/adversarial_review/`), suites (`tests/test_adversarial_review.py`, `tests/test_adversarial_review_isolation.py`), índices y `CHANGELOG.md`.
- **Staging (no versionado, no citable como provenance):** ledger append-only y artefactos crudos de BASELINE, FULL, MAR, EVALUACIÓN, ADJUDICACIÓN e INTEGRIDAD. Los valores medidos y el mapa completo están reproducidos en este informe; los hashes de los artefactos y el orden están en el ledger, que la integridad verificó.
- **Commits:** Commit 1 `ca492ca1969a32841638ca6913251c83502a7e70` (preregistro + FRAME + prototipo + tests, antes de ejecutar). Commit 2: ver plan 179 / `## Checkpoint / cierre` (cierre de esta iniciativa).
- **Verificación:** batería canónica y gates C-1/C-2/C-3 registrados en el plan 179 (`## Verificación`, `## Validation anchor`, `## Checkpoint / cierre`).
- **Trazabilidad:** `Priority 3.7` (insumo local del mantenedor, no versionado) → campaña T1–T3 → decisión `REFORMULATE` → plan 179 → diseño + FRAME + prototipo (Commit 1) → experimento → **este informe (`REJECT`)** → posible nuevo experimento autorizado (no creado por este informe) → Protocol solo por RFC-56.
