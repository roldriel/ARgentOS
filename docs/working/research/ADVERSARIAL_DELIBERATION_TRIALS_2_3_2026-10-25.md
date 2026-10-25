# Trials #2 y #3 — registro experimental autocontenido (Adversarial Deliberation, ARgentOS DEV)

> **Naturaleza:** Working / experimental (`docs/working/research/`). **No normativo.** Es evidencia y provenance; nunca autoridad.
> **Protocolo:** `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md`, congelado en el commit `d61e327` **antes** de ejecutar cualquier pasada. SHA-256 del preregistro en el árbol de ejecución: `0E166E8F10F7F06207063B5F2A0C7F9FD3C2639F7C078DDF066D9DA33B8B37AE`. Este registro **no** reescribe el protocolo: lo aplica y reporta sus resultados.
> **Estado:** ejecución cerrada; decisión de campaña `REFORMULATE`. Sin cambios en `protocol/`, `.agents/`, `runtime/`, `tools/`, `tests/`, `docs/VERSIONING.md`, `ROADMAP.md`, `CHANGELOG.md`, RFCs, ADRs ni planes.
> **Evidencia previa:** `ADVERSARIAL_DELIBERATION_EXPERIMENT_2026-10-25.md` y `ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md`, usados sólo como evidencia y para diseñar mejor las pruebas.

## 0. Metadata, provenance y autorización

- **Campaña:** Adversarial Deliberation — Trials #2 y #3. **Fecha:** 2026-10-25 (America/Buenos_Aires).
- **Repositorio:** rama `dev`. HEAD al congelar el preregistro: `e7bc8818afed903cfc327cb98a2fcfbf7a9789ee`; HEAD durante la ejecución: `d61e327` (commit 1 de esta campaña, docs-only). Árbol con dos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), preservados, no leídos como evidencia.
- **Ejecutores:** el Lead (diseño, frames, ledger, reveal, análisis cross-trial, decisión) y **contextos `fresh` independientes** para Baseline, Defense, Prosecution, Synthesis, Rebuttal (uno por trial), Evaluation (uno por trial), Adjudication (uno para ambos trials) e Integrity Audit (uno). Mismo modelo (`deepseek-flash`) en todas las pasadas.
- **Artefactos de sesión:** `.project/campaign/` (gitignored). Los textos completos se reproducen verbatim en los apéndices de este registro; los hashes SHA-256 y el ledger permiten verificar su identidad. El ledger es append-only con cadena de hashes (§12).
- **Autorización y clasificación (RFC-75 Mecanismo 1; `.agents/AGENTS.md`):** **Origen** = acción directa del mantenedor. **RFC-56 Class: N/A** (sin payload delta). **Change Level: L1** (un escritor de artefactos versionados; scope documental `docs/working/research/`; architectural 0; release 0). **Dominio:** DEV docs. **Sin Plan** (instrucción directa; precedente `e7bc881`). Este registro no crea autoridad, no adopta mecanismo y no propone cambios normativos.
- **Hashes de los frames congelados:** FRAME-2 `A64AE4ADBF1C550019A742F036FBA55AF797B926F87740EA5BAC80F359EBE0C2`; FRAME-3 `9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865`.

### 0.1 Artefactos y hashes finales

| Artefacto | Rol | Palabras | SHA-256 |
|---|---|---:|---|
| `FRAME-2.md` | Objeto Trial #2 (congelado) | 1.576 | `A64AE4AD…EBE0C2` |
| `BASELINE_2.md` | Result A Trial #2 | 2.198 | `3BA05908…848AE8F` |
| `DEFENSE_2.md` | Case FOR Trial #2 | 2.275 | `D46CE1EE…F05F772` |
| `PROSECUTION_2.md` | Case AGAINST Trial #2 | 2.277 | `B2DB9375…CD4EBE5` |
| `SYNTHESIS_2.md` | Comparación/verdict/recommendation | 2.994 | `34737E50…DB6644B` |
| `REBUTTAL_2.md` | Rebuttal Trial #2 | 1.481 | `4345A881…607AEFB` |
| `EVALUATION_2.md` | Clasificación/métricas independientes | 3.996 | `68789DC2…AAB37E41` |
| `FRAME-3.md` | Objeto Trial #3 (congelado) | 1.700 | `9674C3DF…D24476865` |
| `BASELINE_3.md` | Result A Trial #3 | 2.195 | `52B45433…B1B643` |
| `DEFENSE_3.md` | Case FOR Trial #3 | 2.296 | `23BA4084…39A00F837` |
| `PROSECUTION_3.md` | Case AGAINST Trial #3 | 2.300 | `08228EED…7D86143A5` |
| `SYNTHESIS_3.md` | Comparación/verdict/recommendation | 2.712 | `22338229…21B4AE` |
| `REBUTTAL_3.md` | Rebuttal Trial #3 | 1.485 | `81705E05…60002B98B` |
| `EVALUATION_3.md` | Clasificación/métricas independientes | 3.447 | `3FE78C28…E6D7C848E` |
| `ADJUDICATION.md` | Re-clasificación independiente | 2.500 | `2A0534C9…EE7BD6FB` |
| `INTEGRITY_AUDIT.md` | Auditoría de integridad | 2.486 | `3DFEA98E…24FC7CA20` |

**Palabras:** conteo determinista de tokens separados por whitespace (`Measure-Object -Word`), no conteo lingüístico. **Llamadas a herramientas:** `[SELF-DECLARED]`. **Tokens/contexto:** `GAP` estructural. Los hashes completos están en el ledger (Apéndice Q) y en cada artefacto de evaluación; la tabla usa forma abreviada sólo para lectura.

## 1. Protocolo aplicado (resumen)

El preregistro congelado fijó: dos trials con el mismo protocolo (`FRAME → BASELINE → DEFENSE → COMMIT → PROSECUTION → COMMIT → REVEAL → CRITERION COMPARISON → SYNTHESIS → VERDICT → RECOMMENDATION → EVALUATION/ADJUDICATION`); baseline cerrado antes del tratamiento (con la desviación registrada en §9); commit-before-reveal; no contaminación entre trials; taxonomía en dos dimensiones (`NEW`/`DERIVED`/`DUPLICATE` × `MATERIAL`/`NON_MATERIAL`/`SPURIOUS`); criterio de materialidad; métricas; método de costes; reglas de éxito/fracaso; y regla de decisión `ADOPT`/`REFORMULATE`/`INCONCLUSIVE`/`REJECT` con umbrales numéricos y disparadores R1–R4. No se modificó ninguna regla después de observar resultados (los cambios de caso y de rúbrica ocurrieron **antes** del commit 1; Apéndice C del preregistro).

**Casos:** Trial #2 = Case-02, **Memory como dependencia estándar del Execution Host DEV** (decisión de producto/runtime abierta por `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:9 F-03`). Trial #3 = Case-03, **ADR-worthiness del acto de autoridad del Plan 152** (`<PLAN-152>:F-1`, pending decision; blocker del `ROADMAP.md:68`). Ambos son decisiones DEV reales, materiales, ambiguas, verificables y acotadas; difieren en contenido/dominio (runtime de producto vs gobernanza/registro de autoridad) y son comparables en complejidad decisional (6 criterios, múltiples alternativas, evidencia disponible). Ambos son **pre-analizados** (una auditoría y un pending decision previos), lo que baja el techo de descubrimiento y se declara como limitación.

**Replicación controlada (Trial #2):** replica el **método** del Trial #1 sobre un caso nuevo, para probar si el fenómeno del Trial #1 (señal positiva estrecha con alta duplicación y cambio de verdict por reponderación) se reproduce con las ambigüedades metodológicas corregidas. No replica el caso ni el resultado del Trial #1.

## 2. Trial #2 — Case-02 (Memory como dependencia estándar del Execution Host)

### 2.1 Result A — baseline

`BASELINE_2` (2.198 palabras; 288 s de agente) leyó el FRAME y el repositorio, sin conocer el tratamiento. **Decisión: `REVISE`.** Dirección correcta, forma concreta rechazada: el destino «Memory como contexto estándar del Host DEV» es coherente con `ID-4`/`AE-8` y con `FC-3`, pero C-MEM literal cablea una ruta sin actor, usa un renderer que no habla el contrato, consolida el canal equivocado y, sin productor, declara estándar algo inerte sobre una base que Git no persiste. Propuso **C-MEM′** con cuatro condiciones: (R-1) punto de composición único CLI+embedding; (R-2) canal único `knowledge_entries` o renderer conforme al contrato; (R-3) declaración «cableada, inerte sin productor»; (R-4) corrección separada y previa de la fila `AE-8`. Baseline encontró, entre otros: ruta sin actor (`--worker agent` con `NullAgentInvoker`), desajuste `_record_text` (busca `context/text/summary/note`; el contrato usa `statement`/`description`), segundo canal de memoria frente a `knowledge_entries`, y la inexistencia de `.project/knowledge`.

### 2.2 Tratamiento

- **DEFENSE** (2.275 palabras; 422 s): `SUPPORT_WITH_CONDITIONS`, confianza 0,72. 8 argumentos: D-1 la ruta real contradice la ruta declarada; D-3 coste/reversión ≈ 0; D-4 placement resuelto con base plana; D-5 autoridad preservada estructuralmente; D-6 fallas degradan a contexto vacío; D-7 la alternativa multiplica puntos de construcción; D-2/D-8 condiciones de declaración. Declaró límites: sin productor, sin invoker real, sin `.project/knowledge`, GAP de durabilidad Git.
- **PROSECUTION** (2.277 palabras; 326 s): `OPPOSE`, confianza 0,85. 10 objeciones (9 `REAL`, 1 `SPECULATIVE`): P-1 (seam sin productor ni consumidor: no-op con apariencia de capacidad), P-2 (renderer no entiende el schema), P-3 (base plana colisiona con `project_segment.json`; sin filtro por `kind`), P-4 (ignora `retrieval.eligible`), P-5 (durabilidad no materializada; `rebuild` sin fuente), P-6 (presupuesto de contexto no contabilizado; frontera detecta, no previene), P-7 (invierte la semántica del test), P-8 (`FC-3` ya integrado sin wiring por defecto), P-9 (edición de `AE-8` = enmienda de gobernanza, no documental), P-10 (README no distribuido).
- **REVEAL** (13:56:30): hashes de DEFENSE y PROSECUTION registrados en el ledger **antes** de lanzar la síntesis. No hubo reescritura posterior (hash verificado al evaluar).
- **SYNTHESIS** (2.994 palabras; 277 s): **`VERDICT: NOT_VIABLE` para C-MEM tal como está especificado**; `F-03` permanece abierta. **`RECOMMENDATION: REVISE`** con C-MEM′ R-1…R-6. Bases: la ruta nombrada no tiene actor; no hay productor ni registro; el consumo estándar no entregaría el contenido canónico (renderer + elegibilidad); la base plana no está aislada; lo preservado no alcanza; la necesidad no está demostrada con la evidencia admitida. Preservó 3 desacuerdos (necesidad, namespace/remedio, atribución de durabilidad) y 4 contradicciones (D-3/P-7, D-1/P-8, D-4/P-3, B-7 del baseline). Retractó `B-7` del baseline (la fila `AE-8` es exacta en HEAD).
- **REBUTTAL** (1.481 palabras; 130 s): P-1 **no** cambia el verdict ni la recommendation; `NOT_VIABLE` está sobredeterminado por P-2/P-3/P-4/P-8; la parte P-1a es reparable con el punto de composición existente y P-1b (no-op sin productor) permanece material. Añadió R-1 (P-1 no portante), R-2 (P-1a reparable/P-1b no), R-3 (resolver P-1 endurece P-2/P-4/P-6).

### 2.3 Evaluación independiente y clasificación

`EVALUATION_2` (3.996 palabras; 452 s) aplicó la rúbrica congelada. **Conteos (occurrences = distinct = 24; sin dedupe cross-pass):** `NEW` 6, `DERIVED` 7, `DUPLICATE` 11; `MATERIAL` 17, `NON_MATERIAL` 6, `SPURIOUS` 1 (D-7); `NEW+MATERIAL` 4, `DERIVED+MATERIAL` 5, `DUPLICATE+MATERIAL` 8; **`DISTINCT_MATERIAL_NEW` 9** (Defense 2: D-4, D-6; Prosecution 6: P-3, P-5b, P-6a, P-7, P-8, P-9; Rebuttal 1: R-2). `DUPLICATE_SHARE` 0,458; `SPURIOUS_SHARE` 0,042. **Impacto:** `DECISIONAL_IMPACT` 0; `PLAN_IMPACT` 2 (P-3, P-6a); `EVIDENCE_IMPACT` 2; `DECISION_IMPACT` (H3) 1; `REWEIGHTING` 1 (veredicto `NOT_VIABLE` sobre bases duplicadas — strict §10: `NO ATRIBUIDO`); `NO ATRIBUIDO` 4. El veredicto es **sobredeterminado**: sobrevive al retiro de cada finding `NEW`/`DERIVED` porque las bases 2, 3 y 5 se apoyan en `DUPLICATE+MATERIAL`. **Clase del trial: `POSITIVE_BUT_COSTLY`** (`VALUE_CLASS = PLAN`; `COSTLY` = ratio 4,01 > 3,0). Sensibilidad: D-7 como `DUPLICATE+MATERIAL` no cambia la clase; atribuir el veredicto tampoco (sigue bloqueada por `COSTLY`).

**Adjudicación:** 2 discrepancias, ambas de novedad (`P-6a`, `P-8`: `NEW+MATERIAL` → `DERIVED+MATERIAL`); sin discrepancias de materialidad ni `SPURIOUS`; `DISTINCT_MATERIAL_NEW` 9; clase **sin cambio**.

## 3. Trial #3 — Case-03 (ADR-worthiness del acto de autoridad del Plan 152)

### 3.1 Result A — baseline

`BASELINE_3` (2.195 palabras; 274 s) leyó el FRAME y el repositorio. **Decisión: `REVISE` hacia la alternativa C** (no producir ADR-22): registrar `not ADR-worthy` en un artefacto nuevo post-cierre que referencie al Plan 152 y reconciliar `ROADMAP.md:68` por referencia. Fundamento: el acto ya está registrado con provenance en el Plan y el contenido normativo en Policy; ninguno de los tres criterios de ADR-worthiness se satisface con claridad y `(c)` no se cumple porque no hay invariante arquitectónico nuevo; la elevación retrospectiva está permitida y C no cierra puertas; el coste recurrente de un ADR redundante supera su valor. No B: el ADR-19 registra el envelope, no este acto.

### 3.2 Tratamiento

- **DEFENSE** (2.296 palabras; 241 s): `SUPPORT_WITH_CONDITIONS`, confianza 0,72. 8 argumentos: D-3 (ADR-16 admite elevación retrospectiva y el Plan 152 nombra el ADR como mecanismo aplicable), D-1 (criterio `(a)` ya satisfecho: `GOV-4`…`GOV-9` materializados y consumidos, p. ej. Plan 160), D-4 (RFC-75 Mecanismo 12 + post-close por referencia: única ruta compatible con el Plan cerrado y `F-1`), entre otros.
- **PROSECUTION** (2.300 palabras; 612 s): `OPPOSE`, confianza 0,82. 9 objeciones (8 `REAL`, 1 `SPECULATIVE`): P-1 (el acto no ejerció `AU-6`; el ADR-22 sería la primera decisión y la circularidad no se cura), P-3 (la premisa «Plan cerrado» está contradicha por el checkpoint del Plan 152 y por el Plan 171; sólo el INDEX/Plan 153 afirman `Closed`), P-6 (ADR-worthiness no demostrada: `(b)` excluida, `(c)` no satisfecha, `(a)` no argumentada), P-4 (inseparabilidad independiente/no duplicativo), P-2/P-5/P-7/P-8/P-9 (vehículo, agrupación, fecha/objeto, ROADMAP, especulativa).
- **REVEAL** (13:56:30): hashes registrados antes de la síntesis; sin reescritura posterior.
- **SYNTHESIS** (2.712 palabras; 430 s): **`VERDICT: VIABLE`** (advisory; no decide `AU-6` ni resuelve `F-1`); **`RECOMMENDATION: REVISE` sobre C-ADR**. El baseline recomendaba C (no ADR); la síntesis recomienda revisar C-ADR porque `(a)` tiene apoyo literal en el consumo posterior del Plan 160 y el vehículo ADR es el que RFC-75 Mecanismo 12 prevé. Preservó el desacuerdo de `(c)`/interpretación estricta de `(a)`; registró como contradicción real el estado de cierre del Plan 152 (checkpoint y Plan 171 dicen `Executed`; prosa del INDEX dice `Closed`; `057a4b2` existe). Correcciones: nombrar el acto que resuelve `F-1`; fechar el ADR en la resolución; acotar la propiedad 2; reconciliar por referencia el cierre del Plan 152; decidir la fila del ROADMAP; declarar `Plan: plan 152` o `Plan: —`.
- **REBUTTAL** (1.485 palabras; 145 s): P-4 **no** cambia el verdict (`VIABLE`) ni la recommendation (`REVISE`). Su pata fuerte («independiente y no duplicativo es insatisfacible») queda refutada por ADR-19 (Accepted, `Plan: plan 151`, puntero `Formalizada en`) y por ADR-16 punto 4; sólo «el rationale» de la propiedad 2 cruza la frontera y se corrige con una cláusula. Añadió R-1 (rationale único ítem duplicativo), R-2 (ADR-19 instancia el patrón), R-3 (la frontera estrecha refuerza B-8 sin invertir la recomendación).

### 3.3 Evaluación independiente y clasificación

`EVALUATION_3` (3.447 palabras; 418 s). **Conteos primarios (distinct = 23; occurrences = 24; dedupe declarado `P-4b ≡ R-1`):** `NEW` 13, `DERIVED` 7, `DUPLICATE` 3; `MATERIAL` 10, `NON_MATERIAL` 6, `SPURIOUS` 7; `NEW+MATERIAL` 8, `DERIVED+MATERIAL` 0, `DUPLICATE+MATERIAL` 2; **`DISTINCT_MATERIAL_NEW` 8** (Defense 2: D-1, D-4; Prosecution 5: P-1a, P-3, P-4b, P-7, P-8; Rebuttal 1: R-2). `DUPLICATE_SHARE` 0,130; `SPURIOUS_SHARE` 0,304. **Impacto:** `DECISIONAL_IMPACT` 2 (recomendación C → C-ADR; verdicto `VIABLE`), `PLAN_IMPACT` 5, `EVIDENCE_IMPACT` 2, `DECISION_IMPACT` sí; atribución con cita de IDs y cadena verificable (conjunto `D-1`+`D-4` para el cambio decisional). **Clase: `POSITIVE_BUT_COSTLY`** (`VALUE_CLASS = DECISION`; `SPURIOUS_HIGH` y `COSTLY` = 5,21 > 3,0; el orden de §13.2 hace que `COSTLY` decida antes que las clases 8/9). **Adjudicación:** 2 discrepancias de novedad (`P-4b` `NEW+MATERIAL`→`DUPLICATE+MATERIAL`; `R-1` `NEW+MATERIAL`→`DERIVED+MATERIAL`) y 1 de dedupe (refutó `P-4b≡R-1`; corpus 24 distinct). Con la versión adjudicada: `DUPLICATE_SHARE` 0,167; `SPURIOUS_SHARE` 0,292; `DISTINCT_MATERIAL_NEW` 8; **clase sin cambio** (`POSITIVE_BUT_COSTLY`, `COSTLY`). Discrepancia con la evaluación: la evaluación sostiene el dedupe; el adjudicador lo refuta; §8.3 aplica: clasificación primaria congelada + sensibilidad reportada; sin cambio de clase.

## 4. Métricas agregadas

### 4.1 Findings

| Métrica | Trial #2 | Trial #3 | Pooled |
|---|---:|---:|---:|
| total (occurrences) | 24 | 24 | 48 |
| distinct | 24 | 23 (24 adjudicado) | 47 (48) |
| `NEW` | 6 | 13 | 19 |
| `DERIVED` | 7 | 7 | 14 |
| `DUPLICATE` | 11 | 3 | 14 |
| `MATERIAL` | 17 | 10 | 27 |
| `NON_MATERIAL` | 6 | 6 | 12 |
| `SPURIOUS` | 1 | 7 | 8 |
| `NEW+MATERIAL` | 4 | 8 | 12 |
| `DERIVED+MATERIAL` | 5 | 0 | 5 |
| `DUPLICATE+MATERIAL` | 8 | 2 | 10 |
| **`DISTINCT_MATERIAL_NEW`** | **9** | **8** | **17** |
| `DUPLICATE_SHARE` (distinct) | 0,458 | 0,130 (0,167 adjudicado) | 0,298 |
| `SPURIOUS_SHARE` (distinct) | 0,042 | 0,304 (0,292 adjudicado) | 0,170 |
| Defense / Prosecution / Rebuttal (`DMN`) | 2 / 6 / 1 | 2 / 5 / 1 | 4 / 11 / 2 |

### 4.2 Impacto

| Métrica | Trial #2 | Trial #3 |
|---|---:|---:|
| `DECISIONAL_IMPACT` | 0 | 2 |
| `PLAN_IMPACT` | 2 | 5 |
| `EVIDENCE_IMPACT` | 2 | 2 |
| `DECISION_IMPACT` (H3) | sí (sólo plan) | sí (decisión + plan) |
| `REWEIGHTING` | 1 (veredicto) | 0 |
| `NO ATRIBUIDO` | 4 | 0 |

### 4.3 Coste

| Componente | Trial #2 | Trial #3 |
|---|---:|---:|
| Baseline `SELF_S` | 288 s | 274 s |
| Defense / Prosecution / Synthesis / Rebuttal `SELF_S` | 422 / 326 / 277 / 130 s | 241 / 612 / 430 / 145 s |
| `TREATMENT_SELF_S` | 1.155 s | 1.428 s |
| `ADDITIONAL_COST_RATIO_SELF` | **4,01×** | **5,21×** |
| `ADDITIONAL_COST_RATIO_LEAD` (aprox.) | 3,12× | 3,52× |
| `EFFECTIVE` (mayor) | **4,01×** | **5,21×** |
| Palabras baseline / tratamiento | 2.198 / 9.027 (**4,11×**) | 2.195 / 8.793 (**4,01×**) |
| `COSTLY` (> 3,0) | **SÍ** | **SÍ** |
| Evaluación / adjudicación / auditoría | 3.996 w / — / — | 3.447 w / 2.500 w / 2.486 w |

`[SELF-DECLARED]`: llamadas a herramientas. `GAP`: tokens/contexto; el `LEAD_WALL_S` del baseline (416 s) **no está en el ledger** (desviación D-g): con los timestamps de los artefactos (291/277 s) los ratios LEAD serían 4,46× y 5,29×; `COSTLY` y las clases no cambian. Se reporta el ratio SELF como medida primaria y el LEAD como aproximación no auditada.

**Eficiencia:** `DISTINCT_MATERIAL_NEW` por 1.000 s de coste adicional: 7,79 (Trial #2, SELF) y 5,60 (Trial #3); impactos decisionales atribuibles por 1.000 s: 0 (Trial #2) y 1,40 (Trial #3).

## 5. Desviaciones y validez

Clases: D1 no material; D2 material con trial válido y limitación; D3 invalida. Inventario completo: **14 desviaciones registradas (8 D2, 6 D1; ninguna D3)**; detalle y verificación en el Apéndice P:

| ID | Desviación | Clase | Efecto |
|---|---|---|---|
| D-a | **Solapamiento baseline→defensa:** las defensas arrancaron 77 s (T2) y 62 s (T3) antes del `FINISHED` del baseline; el hash final del baseline se registró en `[004]` (13:45:34), después de que ambas defensas cerraran. El `[003]` (13:37:01) había registrado hashes no finales. | **D2** (frontera literal D3; ver abajo) | Gate §17.1 incumplido en secuencia; sin contaminación demostrable; hashes finales usados para comparar; ratios y clases intactos. |
| D-b | `[003]`→`[004]`: baseline reescrito después de un hash registrado. | **D2** | Idem; `[003]` superseded, no editada; comparación con hash final. |
| D-c | Trial #3: `SYNTHESIS FINISHED` 14:04:30 > `REBUTTAL STARTED` 14:04:25, contra mtime 14:03:52 y hash verificado. | D1 | Orden verificado por hash; timestamp declarado erróneo. |
| D-d | DEFENSE-2: un `git grep` devolvió dos líneas del preregistro. | D1 | Declarado, no abierto ni citado. |
| D-e | REBUTTAL-2 leyó `DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md`, fuera de la base de 15 ítems. | D1 | Declarado; dentro de la clase admitida; ninguna conclusión depende. |
| D-f | FRAME-3 sobreafirma el cierre del Plan 152 («`Executed`/`Closed`; INDEX, fila 152»): la fila dice `Executed`; la prosa `Closed` contradice el checkpoint y el Plan 171. | **D2** | Premisa no unívoca trasladada a todas las pasadas; sostiene P-3/P-4; no invalida. |
| D-g | `LEAD_WALL_S` del baseline = 416 en ambos trials, contra 291/277 de los timestamps; no está en el ledger. | **D2** | Ratios EFFECTIVE subestimados; `COSTLY` y clase intactos. |
| D-h | REBUTTAL-3 `LEAD_WALL_S` 130 < `SELF_S` 145. | **D2** | Coste subestimado en 15 s; clase intacta. |
| D-i | Frames congelados sobre `e7bc881`, ejecución sobre `d61e327`. | D1 | Delta docs-only; sin cambio de evidencia. |
| D-j | Apéndice C.7 (tabla sintética) prometido y ausente del preregistro congelado. | **D2** | Control de exhaustividad no entregado; reconstruido por el Integrity Audit (8 casos + 2 variantes, todos PASS); sin efecto en métricas. |
| D-k | EVALUATION-3 dedupe erróneo `P-4b≡R-1` (refutado por el adjudicador). | **D2** | Corpus 23→24; `DUP` 0,130→0,167; `SPUR` 0,304→0,292; `DMN` 8→8; clase sin cambio. |
| D-l | EVALUATION-2 atribuye a BASELINE-2 una declaración de 416 que no existe. | D1 | Error de ancla documental; vinculado a D-g. |
| D-m | BASELINE-2 `B-7` da por inexacta la fila `AE-8`, que es exacta. | D1 | Retractado en SYNTHESIS-2; sin efecto de clase. |
| D-n | El ledger `[011]` y una versión en curso de este registro citaron el hash `69CDBA79…` y 1.724 palabras de la auditoría, cuando el artefacto todavía se estaba escribiendo; el hash final es `3DFEA98E…` y 2.486 palabras. | **D2** | Corregido por la entrada append-only `[012]`; `[011]` superseded, no editada; ítem P verbatim desde el archivo final. |

**Frontera D2/D3 de D-a/D-b (decisión del Lead).** El texto de §16 dice que un «artefacto reescrito después del hash» es D3. Literalmente, `[003]` registró un hash de un baseline que luego cambió. **No se clasifica D3** por estas razones, que se declaran explícitamente: (i) las pasadas del baseline no habían declarado `FINISHED` cuando se escribió `[003]`; el hash registrado era una observación prematura del Lead, no una atestación de cierre; (ii) el contenido final del baseline precede a la finalización de las defensas y **ninguna pasada de tratamiento recibió el baseline**; (iii) el hash usado para la comparación es el final, registrado antes del reveal; (iv) no hay contaminación demostrable ni evidencia inventada. **Lectura alternativa registrada:** si se aplicara literalmente D3, ambos trials serían `INVALID_TRIAL` y la campaña sería `CAMPAIGN_INVALID` → `INCONCLUSIVE`. La decisión de campaña se calcula con la lectura D2; la alternativa se reporta en §8.4. El objetivo del gate —que el baseline no sea influido por el tratamiento y que el tratamiento no sea informado por el baseline— se cumple en la sustancia; falla el registro de secuencia.

**Integridad global:** `CAMPAIGN_INTEGRITY = VALID_WITH_LIMITATIONS` (Apéndice P). PASS en hashes/ledger, no contaminación, trazabilidad Git y ledger; FAIL de secuencia baseline→defensa (D-a/D-b), FAIL de dedupe en Trial #3 (D-k), FAIL de procedencia de costes (D-g/D-h). Sin D3. El control sintético de exhaustividad de clases fue reconstruido por el auditor: 8 casos + 2 variantes, todos PASS; se detectó un hueco de redacción (`VALUE_CLASS` no cubre el caso con `DMN ≥ 1` y ningún impacto; la clase 10 `INCONCLUSIVE_TRIAL` lo captura, por lo que la lista de clases es exhaustiva).

## 6. Cross-trial: Trial #1 vs Trial #2 vs Trial #3

| Dimensión | Trial #1 | Trial #2 | Trial #3 |
|---|---|---|---|
| Caso | Integration Surface (template) | Memory estándar en el Host | ADR-worthiness del acto del Plan 152 |
| Dominio | docs/template | runtime/producto | gobernanza/registro de autoridad |
| Baseline | `REVISE` | `REVISE` (C-MEM′) | `REVISE` hacia C (no ADR) |
| Verdicción del tratamiento | `UNDETERMINED` | `NOT_VIABLE` (C-MEM literal) | `VIABLE` (C-ADR) |
| Recommendation | `GATHER_EVIDENCE` | `REVISE` | `REVISE` (objeto: C → C-ADR) |
| Duplicación | 75 % | 45,8 % | 13,0 % (16,7 % adjudicado) |
| `DISTINCT_MATERIAL_NEW` | 1 (marginal, plan) | 9 | 8 |
| Cambio decisional atribuible | 0 | 0 (sólo plan) | 2 (recommendation/verdict) |
| Reponderación | sí (`REVISE`→`UNDETERMINED`) | sí (verdict sobredeterminado) | no |
| Espurias | 0 | 1 (4,2 %) | 7 (30,4 %) |
| Coste adicional (SELF) | ≈2,35× | 4,01× | 5,21× |
| Clase | éxito fuerte marginal / parcial en sustancia | `POSITIVE_BUT_COSTLY` | `POSITIVE_BUT_COSTLY` |

**Patrones repetidos:** (1) el tratamiento encuentra información material nueva en los tres trials (H1 se replica); (2) la mayor parte del valor nuevo proviene de la pasada de falsificación (Prosecution: 11 de 17 `DMN` pooled) y de la construcción del caso favorable en el trial donde hubo cambio decisional (Trial #3: D-1/D-4); (3) el coste adicional es alto y creciente (2,35× → 4,01× → 5,21×) y nunca por debajo de 2,3×; (4) el cambio de verdict por reponderación aparece en los dos primeros trials y **no** en el tercero; (5) la duplicación es inversamente variable al coste y no es el modo de fallo dominante en Trials #2/#3; (6) las objeciones espurias son escasas en Trials #1/#2 y altas en Trial #3 (30 %), donde además la clasificación fue más disputada.

**Hallazgos únicos:** Trial #2: colisión de namespace `project_segment.json`/`kind` (P-3), presupuesto de contexto no contabilizado (P-6a), estado real de `FC-3` (P-8); Trial #3: consumo posterior de `GOV-8`/`GOV-9` por el Plan 160 (D-1), ruta post-close por referencia (D-4), contradicción del cierre del Plan 152 (P-3). **Falsos positivos:** D-7 (T2, grep mal leído), 7 `SPURIOUS` en T3 (incluida D-2 sobre `(c)` y P-2/P-5/P-9), corrección de B-7 y de P-7. **Tipo de valor producido:** descubrimiento de condiciones/contradicciones e integración (T2) y reevaluación con cambio de objeto de recomendación (T3); no votación, no autoridad.

## 7. Respuestas a las preguntas de campaña (§22)

### A. Discovery

**Sí, con evidencia consistente.** Trial #2: 4 `NEW+MATERIAL` + 5 `DERIVED+MATERIAL` (9 distintos); Trial #3: 8 `NEW+MATERIAL` (8 distintos). En ambos aparecen findings materiales que el baseline no había explicitado (`P-3`, `P-6a`, `P-8`; `D-1`, `D-4`). H1 se replica en 2/2.

### B. Re-evaluation

**Parcial, y no separable como valor propio.** Trial #1 y Trial #2 muestran cambios de verdict por reponderación (`REVISE`→`UNDETERMINED`; `NOT_VIABLE` sobredeterminado), pero esos cambios se apoyan en hallazgos duplicados y no en información nueva (Trial #2: `REWEIGHTING`, strict §10 `NO ATRIBUIDO`). Trial #3 no necesitó reponderación: el cambio de recomendación se atribuye a `D-1`/`D-4` (`NEW+MATERIAL`). La re-evaluación no se reproduce como mecanismo independiente con valor propio; el valor observado se explica por descubrimiento/condiciones.

### C. Decision impact

**Uno de dos, y en el límite de "decisión".** Trial #2: 0 `DECISIONAL_IMPACT`; sólo 2 `PLAN_IMPACT` + 2 `EVIDENCE_IMPACT`. Trial #3: 2 `DECISIONAL_IMPACT` (recomendación C → C-ADR; verdicto `VIABLE`) atribuidos a `D-1`+`D-4`; el label de recomendación sigue siendo `REVISE`, pero el objeto cambia. No hay cambio de decisión autoritativa: verdict/recommendation son advisory. H3 no se reproduce de forma consistente; el impacto decisional es **1/2 casos**, y su carácter es advisory.

### D. Cost

**El beneficio no compensa el coste.** Ratios adicionales de agente: 4,01× y 5,21× (SELF), con palabras 4,11× y 4,01×; `COSTLY` en ambos trials bajo el umbral congelado de 3,0×. La eficiencia es 7,79 y 5,60 `DMN` por 1.000 s, y 0 / 1,40 impactos decisionales por 1.000 s. H4 no se sostiene con los umbrales preregistrados.

### E. Reproducibility

**El fenómeno de valor nuevo se reproduce (2/2); el impacto decisional no (1/2); el coste se reproduce (2/2); la duplicación y las espurias varían (45,8 %/13,0 %; 4,2 %/30,4 %).** La reproducibilidad es parcial: hay señal consistente de descubrimiento material, pero no de mejora decisional consistente ni de eficiencia.

### F. Mechanism

El mecanismo que produjo valor fue, en orden de contribución: **`CONDITION DISCOVERY`** (condiciones de aceptación, namespace/kind, presupuesto, cierre post-close), **`CONTRADICTION DETECTION`** (FC-3 declarado vs ruta real; cierre del Plan 152; README vs CLI; `AE-8` prospectiva), **`NEW DISCOVERY`** (P-3, P-6a, P-8, D-1) e **`RE-EVALUATION`** (reponderación en T1/T2). No se observó valor de **voting** (no se usó), ni de **integración ausente** en el sentido del Trial #1 (T2 encontró una colisión estructural, no un consumer ausente), ni de independencia epistémica (mismo modelo/frame/evidencia). **`DUPLICATION`** fue alta en T1 (75 %) y moderada en T2 (46 %), baja en T3 (13 %); **`SPURIOUS OBJECTIONS`** fueron altas en T3 (30 %). El valor se concentró en la pasada de falsificación (11/17 `DMN`) con contribución decisiva de la defensa en el único caso con cambio decisional.

## 8. Decisión de la campaña

### 8.1 Cálculo con la regla congelada

- **Clases de trial:** `POSITIVE_BUT_COSTLY` (Trial #2) y `POSITIVE_BUT_COSTLY` (Trial #3), insensibles a las discrepancias evaluador↔adjudicador y a las sensibilidades declaradas.
- **`REJECT`:** no — no hay `CAMPAIGN_NONE`/`CAMPAIGN_NEGATIVE`; ambos trials tienen `DISTINCT_MATERIAL_NEW ≥ 1` (9 y 8) y no se cumple la condición 3.
- **`ADOPT`:** no — no hay `SUCCESS_STRONG` en ninguno; `COSTLY` en ambos; `DUPLICATE_SHARE` pooled 0,298 ≤ 0,50 (no es el bloqueo), pero §14.2 exige ambos `SUCCESS_STRONG`.
- **`REFORMULATE`:** **sí**. Disparador **R4**: ambos trials con `VALUE_CLASS ∈ {EVIDENCE, PLAN, DECISION}` (`PLAN` y `DECISION`) y `COST_RATIO > 3,0` en ambos (4,01× y 5,21×). R1 no aplica (la pasada dominante no alcanza 75 % en ningún trial: 6/9 y 5/8; ambas defensas aportan 2 `DMN` cada una). R2 no aplica (no ambos `EVIDENCE`). R3 no aplica (`DUPLICATE_SHARE` pooled 0,298 < 0,60).
- **Resultado de campaña:** `CAMPAIGN_REFORMULATED` → **`REFORMULATE`**.

### 8.2 Decisión e interpretación

**FINAL_DECISION = `REFORMULATE`.** Hay valor material reproducible (descubrimiento de condiciones/contradicciones en 2/2 trials, con un cambio decisional advisory en 1/2), pero el mecanismo evaluado —Defense + Prosecution + Synthesis + Rebuttal con verdict/recommendation— cuesta 4,0×–5,2× el baseline y no supera el umbral de coste congelado (3,0×). La evidencia **no** justifica un Jury/Court con votación ni una arquitectura multi-agent; justifica reformular hacia una **capacidad más simple de revisión adversarial**, cuyo valor observado se concentró en la falsificación dirigida, la extracción de condiciones y la detección de contradicciones, con la defensa aportando el caso favorable cuando hubo cambio decisional.

**Qué NO se concluye:** que Jury deba desaparecer; que Adversarial Deliberation deba ser parte del Protocol; que voting sea útil; que varios jurados sean necesarios; que los evaluadores sean epistémicamente independientes; que exista una arquitectura multi-agent necesaria; que el mecanismo garantice decisiones correctas; que el mecanismo no pueda ser valioso con otro coste. `n=2`, mismo modelo, casos pre-analizados, un solo Lead.

### 8.3 Recomendación arquitectónica (advisory, no autoritativa)

**RECOMMENDED = Adversarial Review (AR) mínima, advisory y acotada, en lugar de Court/Jury.** Propiedades que la evidencia soporta como hipótesis de diseño a validar (no como arquitectura adoptada):

1. **Trigger por riesgo:** aplicarla sólo a decisiones materiales/ambiguas (como los dos casos), no a todo Change.
2. **Dos pasadas, no cuatro:** una pasada que construya el caso favorable (Defense) y una de falsificación dirigida (Prosecution); ambas con commit-before-reveal y evidencia anclada. La síntesis se reduce a una comparación corta y trazable por criterio, con provenance de argumentos.
3. **Sin voting, sin Judge con autoridad, sin estados/gates nuevos:** el resultado sigue siendo advisory; la autoridad existente decide.
4. **Salida obligatoria:** supuestos, contradicciones, condiciones de aceptación, requisitos de evidencia y un `impact type` explícito (`decision/plan/evidence/none`); registrar el desacuerdo en vez de resolverlo por mayoría.
5. **Presupuesto de coste:** objetivo ≤ 2× el baseline en agent-time; si se excede, detener y registrar (el protocolo evaluado no lo tenía y costó 4–5×).
6. **Reserva epistémica:** mismo modelo ⇒ independencia procedural, no epistémica; si se busca diversidad, usar modelos/proveedores distintos y medirlo, lo que este experimento **no** testea.
7. **Theoretical Execution:** la relación `TE → adversarial` sigue **no testeada**; no se modifica la política de TE.

**Relación con la convención existente:** `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md` (Working, no normativa) ya describe una convención de deliberación adversarial. Estos resultados **no** la adoptan ni la modifican; sugieren que su MVP debería ser más barato y más selectivo, y que el valor esperado está en condiciones/contradicciones más que en verdicts. Cualquier materialización futura requiere su propia autorización (RFC/plan); este registro **no** la autoriza.

### 8.4 Sensibilidad y límites de la decisión

- **D2 vs D3:** con la lectura literal D3 de D-a/D-b, la campaña sería `INCONCLUSIVE` (`CAMPAIGN_INVALID`). Se adopta D2 con la justificación de §5; la alternativa queda registrada.
- **Atribución:** si el cambio decisional de Trial #3 se anulara (por su carácter advisory o por atribución de conjunto), `VALUE_CLASS` pasaría a `PLAN`; R4 seguiría disparando (`COSTLY` en ambos) → `REFORMULATE` igual.
- **Dedupe:** con la versión adjudicada de Trial #3, `DUPLICATE_SHARE` pooled ≈ 0,30 y `SPURIOUS_SHARE` pooled ≈ 0,17; ninguna clase cambia.
- **Coste:** con `LEAD` corregido (4,46×/5,29×) la conclusión no cambia (sigue `COSTLY`).
- **`H5`:** no predomina la duplicación (T2/T3), pero sí el coste alto en ambos y las espurias altas en T3; el resultado no es un `REJECT` porque hay valor material nuevo reproducible. Un cuarto trial con un caso **no pre-analizado** y un mecanismo barato (AR) sería el siguiente paso experimental; **no** forma parte de esta campaña y no se ejecuta aquí.

## 9. Limitaciones

1. `n=2` casos, no generalización estadística; casos **pre-analizados** (auditoría y pending decision previos), lo que deprime el descubrimiento y limita la conclusión a «valor sobre un baseline informado».
2. Mismo modelo/proveedor en todas las pasadas: errores correlacionados; independencia procedural, no epistémica.
3. Un solo Lead diseña, ejecuta y decide; mitigado por revisión pre-ejecución independiente, evaluadores/adjudicador independientes y regla congelada, no eliminado.
4. Sin attestación temporal externa: orden y no-lectura son *atested, not enforced*; el ledger es tamper-evident, no inmutable.
5. Costes: `[SELF-DECLARED]` para llamadas; `GAP` para tokens/contexto; duraciones con concurrencia y latencia del Lead; `LEAD_WALL_S` del baseline no auditado.
6. Errores y desviaciones registrados (§5): frame sobre Plan 152, dedupe de T3, baseline reescrito tras hash intermedio, Apéndice C.7 ausente. Ninguno cambia la clase de ningún trial.
7. La evaluación es post hoc no ciega respecto del orden; mitigado por adjudicación independiente, no eliminado.
8. El baseline es un agente instruido, no el proceso normal «en vivo»; puede ser más exhaustivo que una decisión normal.
9. TE no testeada; no se modifica la política de TE.
10. Relación con `protocol/`: ninguna; el payload ya contiene una capacidad de deliberación adversarial (`adversarial-deliberation`) que este experimento **no** evaluó ni modificó.

## 10. Artefactos, verificación y commits

- **Commit 1:** `d61e327` — `docs(working): preregister adversarial deliberation campaign trials 2-3` (preregistro + INDEX; 746 inserciones, 1 deleción). Creado antes de ejecutar (13:33:20; baselines lanzados 13:33:44).
- **Commit 2:** `docs(working): record adversarial deliberation trials 2 and 3` (este registro + INDEX). El árbol no embebe su propia identidad; el hash del commit 2 se informa en el reporte final de la campaña y no se añade retrospectivamente a este archivo.
- **Sin push, merge, tag ni release.** Sin cambios en `protocol/`, `.agents/`, `runtime/`, `tools/`, `tests/`, `docs/VERSIONING.md`, `ROADMAP.md`, `CHANGELOG.md`, RFCs, ADRs ni planes.
- **Verificación canónica:** `docs/VERSIONING.md:4.1` ejecutada sobre el árbol final antes del commit 2 (2026-10-25): 8 checkers PASS — `check_protocol_invariants` (217 archivos / 10.541 referencias), `check_plan_citations` (todas las citas resuelven), `check_plan_structure` (sin violaciones; 2 `GAP` advisory históricos de los planes 157/158, preexistentes), `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` (warnings de tags esperados en `dev`), `check_invariants_equivalence` (identidad canónica idéntica; 15 entradas), `check_enforcement_declarations` (`ENF-001`…`ENF-003`) — y `pytest tests/` → **1535 passed** en 587,62 s. `check_dist_sync.py` no se ejecuta (local-only; esperado rojo en `dev` sin promoción). C-1/C-2/C-3: `N/A` (no hay Plan, Validation Anchor ni Checkpoint en este Change). Los artefactos de `.project/` son gitignored y no forman parte de la batería.
- **Integridad:** `CAMPAIGN_INTEGRITY = VALID_WITH_LIMITATIONS` (Apéndice P); hashes finales verificados; ledger con cadena íntegra; sin contaminación cruzada detectable; sin D3 (con la frontera D2/D3 declarada).

## Apéndice A — FRAME-2 (congelado, verbatim)

# FRAME-2 — Caso 02 (congelado): Memory como dependencia estándar del Execution Host DEV

- **Caso:** Case-02 / Trial #2 de la campaña «Adversarial Deliberation» (ARgentOS DEV).
- **Fecha de congelación:** 2026-10-25 (America/Buenos_Aires).
- **Estado del repositorio:** rama `dev`, HEAD `e7bc8818afed903cfc327cb98a2fcfbf7a9789ee`. Árbol con dos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), que **no** son evidencia y no se citan.
- **Naturaleza:** Working / experimental. No normativo. Ninguna conclusión de este caso es autoridad.
- **Protocolo:** `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md` (congelado antes de ejecutar este caso).

Este FRAME es el objeto de deliberación. Es el mismo para todas las evaluaciones y **no se modifica** después de congelado.

---

## QUESTION

¿Debe ARgentOS DEV **adoptar Memory como dependencia estándar del Execution Host DEV** —suministrando un `MemoryStore` en el camino normal de construcción del worker y aplicando contexto de memoria por defecto en cada delegación— en lugar de mantener la integración actual como un *seam* opcional que ningún camino de producción conecta?

## CANDIDATE (C-MEM)

Adoptar Memory como **dependencia estándar del Execution Host DEV**, con estas propiedades declaradas:

1. **Wiring por defecto.** En la ruta normal de construcción del worker del host DEV (CLI `python -m runtime.orchestrator --worker agent`, `runtime/orchestrator/__main__.py`), construir y suministrar un `runtime.memory.MemoryStore` cuya base sea la ubicación canónica de conocimiento project-durable declarada por el Placement Contract (`.project/knowledge/`, **sin inventar un subdirectorio**: se usa la base plana que el Plan 150 ya emplea para registros, o la representación que resuelvan las reglas de placement —`PC-48`/`PC-52`— antes de implementar) y pasarlo a `AgentWorker(memory_store=...)`.
2. **Aplicación por defecto.** Con el store construido, `AgentWorker.execute` aplica `build_memory_context`/`with_memory_context` en cada delegación; la ausencia de registros es un estado normal (contexto vacío), nunca un error.
3. **Sin cambio de autoridad.** Memory sigue siendo **contexto** y nunca premisa ni autoridad (`ID-4`, plan 165; `AE-8`): no entra en `contain_actor_result`, no expande scope, no autoriza efectos y no modifica el veredicto de la frontera. Parte del alcance documental es **actualizar la evidencia de estado de `AE-8` en ADR-19** (hoy registra que `runtime/memory/` no se consume desde el orquestador), sin cambiar la norma `AE-8`; ese cambio documental se somete a la autoridad existente y no se ejecuta por inferencia.
4. **Declaración de capacidad estándar.** `runtime/README.md` (y el registro documental de estado que corresponda) declara Memory como capacidad estándar del Host DEV, no como capacidad latente; la declaración no crea autoridad ni obligación para el adoptante.
5. **Evidencia de integración.** Una prueba de integración ejercita la ruta por defecto (store suministrado ⇒ contexto de memoria en el prompt de la delegación; ausencia de store ⇒ no-op), sin compartir el store entre tests ni escribir en el repositorio.
6. **Superficie acotada.** Sin cambios en `protocol/`, `dist/`, `VERSION`, contratos de autoridad (salvo la actualización de **evidencia** de `AE-8` descrita en 3), `contain_actor_result`, envelope de autonomía ni batería canónica. El candidato **no crea un productor de registros**: no implementa consolidación, escritura ni curación de Memory; el beneficio es **condicional** a que existan registros (producidos por otro Change o preexistentes). Reversible: retirar el wiring devuelve el comportamiento actual (`AgentWorker().memory_store is None`).

**Alternativa explícita (no es el candidato):** resolver la condición de integración en sentido contrario —declarar Memory **opcional por diseño**, clasificarla como aislamiento deliberado y no conectar ningún camino estándar—. El baseline y el tratamiento pueden recomendar esta alternativa mediante `REVISE`; el veredicto se emite sobre C-MEM.

## CRITERIA

1. **correctness / necesidad** — ¿C-MEM cierra un gap real de integración o crea una capacidad que el sistema no requiere? ¿La evidencia demuestra que Memory **debe** ser estándar, o sólo que el seam existe y funciona? ¿Un wiring sobre un store sin productor aporta algo hoy, o es un no-op con apariencia de capacidad?
2. **integración** — ¿se acopla al host, al worker, a `fc_flow`, al Placement Contract, a los tests y a la documentación de estado sin duplicar, contradecir ni crear una segunda fuente?
3. **authority** — ¿preserva `ID-4`/`AE-8` (contexto, no autoridad) y la separación del veredicto de containment? ¿La declaración «capacidad estándar» adquiere fuerza normativa o de aprobación sin serlo? ¿La actualización de evidencia de ADR-19 es documental o encubre un cambio de decisión?
4. **maintainability** — ciclo de vida del store (quién lo posee, dónde vive, qué pasa si está vacío/corrupto/obsoleto), ausencia silenciosa, drift de path, carga por delegación, durabilidad real (el contrato declara Git-persisted pero el repositorio no lo materializa).
5. **cost** — esfuerzo de implementación, test, documentación y mantenimiento; coste de hacer la declaración coherente con evidencia real.
6. **reversibility** — ¿puede retirarse o corregirse sin deuda estructural, migración ni cambio de contrato?

## EVIDENCE BASE

Evidencia admitida: contenido versionado del repositorio en el HEAD declarado, leído en sólo lectura. Cada hallazgo debe anclarse a `ruta:sección` o a comando/observación reproducible. Base declarada:

1. `runtime/orchestrator/agent_worker.py` — `memory_store: object | None = None`; `execute()` aplica `build_memory_context`/`with_memory_context` sólo si el store no es `None`.
2. `runtime/orchestrator/__main__.py` — la CLI construye `AgentWorker()` **sin** store (`:188`); el host se construye con ese worker.
3. `runtime/orchestrator/host.py` — `ExecutionHost.__init__` recibe `worker` y no construye ningún `MemoryStore`.
4. `runtime/orchestrator/fc_flow.py` — `MemoryContext`, `build_memory_context`, `with_memory_context`; memoria renderizada como texto; «Absent or unreadable records are skipped: memory is optional context».
5. `runtime/memory/` — `MemoryStore` (store derivado, rebuildable; lecturas fail-closed) y sus suites (`tests/test_memory_store.py`, `tests/test_memory_operational_retrieval_archive.py`, `tests/test_check_memory_store.py`).
6. `tests/test_fc_host_integration.py` — detector de wiring de la ruta real; `test_memory_is_absent_by_default_and_therefore_a_no_op` afirma `AgentWorker().memory_store is None`; `test_the_frontier_still_cannot_be_reached_by_memory`.
7. `tests/test_fc_flow.py` — cubre las primitivas de `fc_flow`, incluida la memoria como contexto.
8. `docs/plans/165-f-c-autonomy-frontier-implementation.md` — `ID-4` («Memory entra como contexto del actor, jamás como premisa ni autoridad»; la frontera se calcula sin consultarla) y `AE-8`.
9. `docs/adr/19-autonomy-envelope-authority.md` — invariantes `AE-*`, `AE-8` «Memory como contexto, nunca autoridad» y su fila de evidencia («`runtime/memory/` no se consume desde el orquestador»); relación con `AU-6`.
10. `docs/rfc/80-memory-system.md` — arquitectura `Accepted`; su bloque de Status declara `Architecture status: CLOSED` e `Implementation status: NOT IMPLEMENTED` (alcance Protocol); la RFC no autoriza por sí sola tocar `protocol/.agents/`.
11. `docs/VERSIONING.md` §9 y `docs/plans/150-memory-system-implementation.md` — `11.7.0` (plan 150, RFC-80) publicó el «Memory System reference runtime» DEV; el Plan 150 figura `Executed` y usa `.project/knowledge/*.json` plano para registros.
12. `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md` — §6.1 (`Memory — seam latente`: `memory_store` sin call sites; default `None`); §9 F-03 («decisión de producto pendiente: ¿opcional por diseño o dependencia estándar del Host?»); §10.4–§10.5 (valor diagnóstico, no fallo crítico); `:176` (reconciliación de alcances RFC-80: Protocol `NOT IMPLEMENTED` vs reference runtime DEV).
13. `docs/placement-contract.md` — §6/§21: `.project/knowledge/` es la familia de estado project-durable que el contrato **declara** source-of-truth y Git-persisted; §22/§24: enforcement de placement diferido; `PC-48` (un `derived` no inventa representation namespace) y `PC-52` (excepciones); el contrato no asigna subdirectorio de memoria.
14. `runtime/README.md` — sección «F-C flow: memory as context…»: `FC-3` memoria como contexto, consumidor único `with_memory_context`; «The host, the WorkerAdapter boundary and the WorkerResult contract (M4) are unchanged»; no declara Memory como capacidad estándar.
15. `docs/plans/INDEX.md` — fila del Plan 178: Memory `PARTIALLY_INTEGRATED`, F-01/F-02/F-03 abiertos/deferred sin reparaciones ejecutadas.

## EVIDENCE STATE (verificado en el HEAD por el Lead antes de congelar)

- **HECHO:** `AgentWorker.memory_store` es opcional y por defecto `None`; la CLI construye `AgentWorker()` sin store; ningún módulo de producción bajo `runtime/` construye un `MemoryStore` (`git grep "MemoryStore("` sobre `runtime/` y `tools/` no devuelve coincidencias); sólo los tests lo construyen.
- **HECHO:** la ruta real sí consume `build_memory_context`/`with_memory_context` en `execute()` cuando el store está presente; **no hay consumidor que lo suministre en producción** ni **productor de registros en producción**: `runtime/memory/consolidation.py` es el único `MemoryStore.write` y sólo lo consumen tests.
- **HECHO:** Memory es contexto, nunca autoridad: `contain_actor_result` no acepta memoria; `ID-4`/`AE-8` lo fijan y `test_fc_flow`/`test_fc_host_integration` lo protegen. La fila de evidencia de `AE-8` en ADR-19 afirma que `runtime/memory/` no se consume desde el orquestador: C-MEM la dejaría obsoleta, y actualizarla es parte documental del alcance (sujeta a autoridad; no convierte a Memory en autoridad).
- **HECHO:** la auditoría de continuidad de integración (Plan 178) dejó F-03 **abierto**: la decisión «Memory opcional por diseño vs dependencia estándar» es explícitamente una decisión de producto pendiente.
- **RECONCILIACIÓN (no contradicción):** RFC-80 declara `Implementation status: NOT IMPLEMENTED` para el payload Protocol; la release `11.7.0` publicó el *reference runtime* DEV. La auditoría ya reconcilia ambos alcances (`:176`); el caso no inventa una contradicción.
- **GAP de durabilidad:** el Placement Contract **declara** `.project/knowledge/` project-durable y Git-persisted, pero en este HEAD `.project/` está gitignored (`.gitignore:13`) y `git ls-files .project` devuelve 0 archivos: la persistencia Git de `.project/knowledge/` **no está materializada** en el repositorio. C-MEM no puede asumirla y debe declararla.
- **GAP:** no existe una declaración de producto que determine si Memory debe ser estándar u opcional; no existe evidencia de uso de Memory en una corrida real del Host con un actor externo (`tests/test_fc_host_integration.py` declara que es un detector de wiring, no una corrida end-to-end). El beneficio de C-MEM es condicional a registros preexistentes o a un productor futuro.

## EVIDENCE RULES / CONSTRAINTS

- **Sólo lectura del repositorio.** No se modifica ningún archivo versionado; la única escritura permitida es el archivo de salida propio asignado bajo `.project/campaign/`.
- **Evidencia admitida:** únicamente contenido versionado del repositorio en el HEAD declarado y comandos de lectura. **No** se admite web, modelos externos, memoria de conversaciones previas ni conocimiento no anclado al repo.
- **`PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md` son insumos locales no versionados: NO son evidencia y no pueden citarse** (precedente `<PLAN-178>:F-2`, RFC-69 I2).
- **No inventar hechos.** Si falta evidencia para una afirmación, declarar `GAP` explícito; no rellenar con plausibilidad. Distinguir `OBSERVED`/`MEASURED`/`INFERRED`.
- **Idioma:** español (términos técnicos en inglés permitidos).
- **No autoridad:** el resultado de este caso es evidencia/advisory. No autoriza cambios, no crea un Plan y no modifica el runtime ni el repositorio.


## Apéndice B — FRAME-3 (congelado, verbatim)

# FRAME-3 — Caso 03 (congelado): ADR-worthiness del acto de autoridad del Plan 152

- **Caso:** Case-03 / Trial #3 de la campaña «Adversarial Deliberation» (ARgentOS DEV).
- **Fecha de congelación:** 2026-10-25 (America/Buenos_Aires).
- **Estado del repositorio:** rama `dev`, HEAD `e7bc8818afed903cfc327cb98a2fcfbf7a9789ee`. Árbol con dos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), que **no** son evidencia y no se citan, más el preregistro de esta campaña, que se commitea como commit 1 **antes** de ejecutar este caso y tampoco es evidencia para él.
- **Naturaleza:** Working / experimental. No normativo. Ninguna conclusión de este caso es autoridad.
- **Protocolo:** `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md` (congelado antes de ejecutar este caso).

Este FRAME es el objeto de deliberación. Es el mismo para todas las evaluaciones y **no se modifica** después de congelado.

---

## QUESTION

¿Debe ARgentOS DEV **registrar el acto de autoridad del 2026-10-07 del Plan 152 (`GOV-1`…`GOV-10`) como un ADR nuevo**, en lugar de dejarlo sólo registrado en el Plan, de no producir ADR, o de enmendar el ADR-19?

## CANDIDATE (C-ADR)

Producir un **ADR nuevo (ADR-22)** que registre el acto de autoridad del 2026-10-07 del Plan 152, con estas propiedades declaradas:

1. **Identidad y registro.** ADR-22 creado desde `docs/adr/_TEMPLATE.md` (número siguiente libre: 22), registrado en `docs/adr/INDEX.md` en el mismo commit; `Status: Accepted` sólo si media el acto de autoridad del mantenedor que resuelva la cuestión.
2. **Contenido.** Registra, sin reescribirlas: la fecha real (2026-10-07), el actor (mantenedor), la evidencia del acto, las diez decisiones `GOV-1`…`GOV-10` con sus resultados (`GOV-1 = C`; `GOV-2`…`GOV-9 = A`; `GOV-10 = B`), el rationale y la separación `AUTHORITY ACT ≠ EXECUTION ≠ MATERIALIZATION ≠ CLOSURE`; las decisiones del Plan siguen siendo la transcripción autorizada y el ADR **documenta**, no sustituye al Plan como autorización.
3. **Sin cambio de contenido.** No cambia ninguna decisión, no eleva `INV-1`/`INV-3` (siguen diferidas por `GOV-10 = B`), no modifica el Plan 152, no reabre `GOV-10` y no toca `protocol/`.
4. **No enmienda el ADR-19.** El candidato **no** enmienda `docs/adr/19-autonomy-envelope-authority.md`; si el juicio de ADR-worthiness conduce a enmendarlo, ésa es la alternativa B, no el candidato.
5. **Resolución administrativa.** Una vez autorizado, registra la resolución de `<PLAN-152>:F-1` (ADR-worthiness) y reconcilia el blocker correspondiente de `ROADMAP.md` **por referencia**; no reescribe el Plan 152 (cuya línea de `F-1` permanece textualmente `open`) ni usa el INDEX como registro de autoridad: la resolución vive en el artefacto nuevo y el Plan cerrado se referencia, no se reabre. No crea autoridad nueva ni ratifica retroactivamente nada.
6. **Superficie.** `docs/adr/22-<slug>.md` (nuevo; header `Plan: —` / `RFC: —` / `Lifecycle: active`, como registro directo del mantenedor), `docs/adr/INDEX.md` (1 fila, `Vigencia: active`), `ROADMAP.md` (1 fila de bloqueo, reconciliada por referencia) y, si corresponde, `CHANGELOG.md`; reversible por `Superseded` (ADR-16 `:Decisión` punto 5). Sin cambios en `protocol/`, `.agents/`, `runtime/`, `tools/`, `tests/` ni en `docs/CONVENTIONS.md` (salvo que el acto de autoridad decida otra cosa, que quedaría fuera del candidato).

**Alternativas explícitas (no son el candidato):**
- **B — Enmendar el ADR-19** para registrar el acto y/o los invariantes que el Plan 152 adoptó.
- **C — No producir ADR**: la decisión se registra como `not ADR-worthy` en un artefacto **nuevo** post-cierre que referencia al Plan 152 (p. ej. `Note`/plan/registro equivalente) y se reconcilia la fila del `ROADMAP.md:68` por referencia; no se edita el Plan 152 ni se usa el INDEX como registro de autoridad.
El baseline y el tratamiento pueden recomendar B o C mediante `REVISE`; el veredicto se emite sobre C-ADR.

## CRITERIA

1. **correctness / necesidad** — ¿el acto satisface los criterios de ADR-worthiness de `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 3): (a) consumido fuera de su RFC, (b) supersede/modifica un ADR, (c) invariante arquitectónico persistente auditable de forma independiente? ¿O el Plan ya es el registro suficiente y un ADR duplica?
2. **integración** — ¿se acopla al modelo ADR (`docs/adr/INDEX.md`, `_TEMPLATE.md`, ADR-16, RFC-69, `docs/CONVENTIONS.md`, `docs/AGENTS.md`) sin duplicar, contradecir ni crear una segunda fuente? ¿El blocker del ROADMAP queda reconciliado correctamente?
3. **authority** — ¿respeta que la ADR-worthiness es un juicio humano reservado (`AU-6`) y que crear un ADR no autoriza cambios de payload? ¿El ADR «documenta» sin ratificar retroactivamente ni sustituir al Plan como autorización? ¿Evita convertir una inferencia del agente en acto de autoridad?
4. **maintainability** — duplicación Plan↔ADR, riesgo de dos fuentes que deriven, carga de enmienda/supersesión, claridad para un lector futuro sobre dónde vive la decisión.
5. **cost** — esfuerzo de redacción, registro, reconciliación y mantenimiento; coste de hacer la ADR coherente con el acto real.
6. **reversibility** — ¿puede retirarse o supersederse sin deuda estructural ni reinterpretar autoridad? ¿Un ADR redundante crea una fuente histórica que luego hay que mantener?

## EVIDENCE BASE

Evidencia admitida: contenido versionado del repositorio en el HEAD declarado, leído en sólo lectura. Cada hallazgo debe anclarse a `ruta:sección` o a comando/observación reproducible. Base declarada:

1. `docs/plans/152-authority-decisions-gov-1-10.md` — `## Acto de autoridad registrado (2026-10-07)` (actor, fecha, evidencia, `GOV-1`…`GOV-10` con resultados, rationale, separación acto/ejecución/materialización/cierre); `### Pregunta estructurada de ADR` (el acto **no** ejerció ADR-worthiness; no se produce ADR; la cuestión queda como pending decision); `## Findings / Correcciones / Pending` (`<PLAN-152>:F-1` open, owner mantenedor); `### Pending decisions` (la decisión «ADR nuevo · enmienda del ADR-19 · no producir ADR» figura pendiente); `## Ejecución de la materialización (2026-10-07)`.
2. `docs/adr/16-change-lifecycle-authority.md` — `:Decisión` (punto 3: criterios de ADR-worthiness `(a)`, `(b)`, `(c)`; punto 5: ciclo `Proposal → Accepted → Superseded` y registro en INDEX; `AU-6` como juicio humano; `AU-2`: el ADR no autoriza payload).
3. `docs/adr/INDEX.md` — ADR-01…ADR-21; ADR-19 (envelope de autonomía, acto del Plan 151, 2026-10-07, `Accepted`); ADR-20 (closed artifact governance; registro directo del mantenedor, con el Plan 172 como materialización registrada en la fila); ADR-21 (attested escape, G-03/G-05/G-06, `Accepted`); formato de fila y `Vigencia`; próxima fila libre = ADR-22.
4. `docs/adr/19-autonomy-envelope-authority.md` — decisión registrada por el Plan 151, sus invariantes `AE-*` y el alcance declarado; relación con `AU-6` (ADR-16).
5. `docs/adr/_TEMPLATE.md` — campos obligatorios (`Status`, `Fecha`, `Lifecycle`, `Superseded por`, `Motivo de retiro`, `Decisión original`, `RFC`, `Plan`, `Clase de cambio`, `Problemas que resuelve`) y secciones (`Contexto`, `Alternativas`, `Decisión`, `Consecuencias`, `Invariantes`, `Relaciones`, `Estado de implementación`); regla de registro en INDEX en el mismo commit.
6. `docs/rfc/69-documentation-taxonomy-and-layout.md` — modelo ADR y taxonomía documental; `ADR-N` como identidad estable.
7. `docs/CONVENTIONS.md` — `Convenciones` (ciclo de status ADR y «status refleja la decisión registrada»; un ADR `Accepted` no habilita cambios de payload; todo ADR nuevo nace del template y se registra en el INDEX; `AU-6` = juicio humano; `C-4`: Plan + ADR si `AU-6`); regla de cambios post-cierre por referencia (RFC-46/RFC-75); el ADR documenta y no sustituye al Plan como autorización.
8. `docs/AGENTS.md` — mapa de carpetas: `docs/adr/` = Governance/ADR; el ADR nuevo nace del template y se registra en el INDEX en el mismo commit. (El ciclo `Proposal → Accepted → Superseded` vive en `docs/CONVENTIONS.md` y en ADR-16, no en `docs/AGENTS.md`.)
9. `ROADMAP.md` — `## 🚧 Bloqueos que pueden cambiar el camino`: fila «ADR-worthiness del acto de autoridad de autonomía | cómo se registra la decisión | docs/plans/152-authority-decisions-gov-1-10.md» (`:68`).
10. `docs/adr/16-change-lifecycle-authority.md` y `.agents/policies/supervised-autonomous-execution.md` — `AU-6` y el carácter humano del juicio de ADR-worthiness (`:336` en la policy SAE); `.agents/policies/authority.md` — clases de autoridad (ADR = NORMATIVE recorded decision; no autoriza payload).
11. `docs/plans/151-autonomy-authority-decision-closure.md` / `docs/adr/19-…` — precedente de un acto de autoridad registrado como ADR y su relación con un Plan.
12. `CHANGELOG.md` y `docs/VERSIONING.md` — reglas de cierre docs-only y de release (RFC-69), para evaluar el coste de registro.

## EVIDENCE STATE (verificado en el HEAD por el Lead antes de congelar)

- **HECHO:** el Plan 152 registra el acto de autoridad del 2026-10-07 con `AUTHORITY_ACT = RECORDED`, `AUTHORITY_ACTOR = mantenedor`, las diez decisiones con resultado nominado, su rationale y la separación `ACT ≠ EXECUTION ≠ MATERIALIZATION ≠ CLOSURE`.
- **HECHO:** el acto **no** ejerció ADR-worthiness; el Plan declara que no se produce ADR y remite la cuestión a `<PLAN-152>:F-1` (estado `open`, owner mantenedor), y `### Pending decisions` registra la decisión «ADR nuevo · enmienda del ADR-19 · no producir ADR» como pendiente. El Plan 152 está cerrado (`Executed`/`Closed`; `docs/plans/INDEX.md`, fila del Plan 152) y sus artefactos cerrados no se reescriben: la resolución de `F-1` se registra **por referencia** en un artefacto nuevo (RFC-46/RFC-75; `docs/CONVENTIONS.md:723-724`), no editando el Plan.
- **HECHO:** `ROADMAP.md` lista «ADR-worthiness del acto de autoridad de autonomía» como bloqueo que puede cambiar el camino, con detalle al Plan 152.
- **HECHO:** existen ADR-19 (acto del Plan 151, mismo día), ADR-20 y ADR-21 como precedentes de ADRs que registran decisiones de gobernanza/ejecución sin derivar del modelo D#; el próximo número libre es **ADR-22** (no existe `docs/adr/22-*.md`).
- **HECHO:** ADR-16 `:Decisión` (punto 3) fija los tres criterios de ADR-worthiness; el punto 5 prohíbe modificar silenciosamente un ADR `Accepted` (si la decisión cambia, se crea ADR nuevo + supersesión); `AU-6` es juicio humano y no se cierra por inferencia del agente.
- **HECHO:** un ADR «registra la decisión y no habilita cambios de payload» (ADR-16 `:Decisión` punto 4; `docs/CONVENTIONS.md`; `.agents/policies/authority.md` clase NORMATIVE).
- **GAP:** no hay decisión registrada que resuelva la ADR-worthiness del acto del Plan 152; no existe un ADR que registre específicamente ese acto. No se verifica en este frame cuál de las tres alternativas es la correcta: es exactamente la pregunta del caso.

## EVIDENCE RULES / CONSTRAINTS

- **Sólo lectura del repositorio.** No se modifica ningún archivo versionado; la única escritura permitida es el archivo de salida propio asignado bajo `.project/campaign/`.
- **Evidencia admitida:** únicamente contenido versionado del repositorio en el HEAD declarado y comandos de lectura. **No** se admite web, modelos externos, memoria de conversaciones previas ni conocimiento no anclado al repo.
- **`PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md` son insumos locales no versionados: NO son evidencia y no pueden citarse** (precedente `<PLAN-178>:F-2`, RFC-69 I2).
- **No se leen artefactos de trials** (ni el registro del Trial #1 ni artefactos de Trial #2): no son evidencia de este caso y podrían contaminar la evaluación. El protocolo previo de la investigación se registra como provenance, no como evidencia de hechos sobre el acto del Plan 152.
- **No inventar hechos.** Si falta evidencia para una afirmación, declarar `GAP` explícito; no rellenar con plausibilidad. Distinguir `OBSERVED`/`MEASURED`/`INFERRED`.
- **No autoridad:** el resultado de este caso es evidencia/advisory. No autoriza crear el ADR, no resuelve `F-1` y no modifica el repositorio; la decisión de ADR-worthiness pertenece al mantenedor (`AU-6`).
- **Idioma:** español (términos técnicos en inglés permitidos).


## Apéndice C — BASELINE_2 (verbatim)

# BASELINE-2 — Case-02 (Memory como dependencia estándar del Execution Host)

## Metadata

- Rol: baseline (Result A), contexto fresh independiente
- Frame verificado: SHA-256 = `A64AE4ADBF1C550019A742F036FBA55AF797B926F87740EA5BAC80F359EBE0C2` (`Get-FileHash -Algorithm SHA256`, 2026-10-25T13:33:47-03:00) — coincide con el valor exigido.
- STARTED: 2026-10-25T13:33:47-03:00
- FINISHED: 2026-10-25T13:38:35-03:00
- HEAD observado: `d61e327` (`dev`). El FRAME congela `e7bc8818afed903cfc327cb98a2fcfbf7a9789ee`; `git diff --stat e7bc881 d61e327 -- runtime/ docs/ tests/ tools/` devuelve sólo dos archivos de `docs/working/research/` (preregistro e INDEX). Base de evidencia sin cambios (`OBSERVED`).
- Archivos leídos (exacto): `.project/campaign/frames/FRAME-2.md`; `runtime/orchestrator/agent_worker.py` (L350–484); `runtime/orchestrator/fc_flow.py` (L30–109); `runtime/orchestrator/__main__.py` (L88–112, L170–215); `runtime/orchestrator/host.py` (grep `worker`); `runtime/memory/store.py` (L55–114); `runtime/memory/*.py` (inventario de símbolos); `runtime/toolcalls/prompt_rendering.py` (grep `knowledge_entries`); `tests/test_fc_host_integration.py` (L1–80); `tests/test_fc_flow.py` (grep forma de registro); `tools/check_memory_store.py` (L1–55); `docs/adr/19-autonomy-envelope-authority.md` (L1–30, grep `AE-8`); `docs/plans/165-f-c-autonomy-frontier-implementation.md` (grep); `docs/plans/150-memory-system-implementation.md` (grep); `docs/rfc/80-memory-system.md` (grep Status); `docs/placement-contract.md` (grep §6/§21/§22/§24, `PC-48`, `PC-52`); `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md` (grep); `docs/plans/INDEX.md` (grep 178); `docs/VERSIONING.md` (L359–370); `runtime/README.md` (grep memory); `.gitignore` (L10–17); `.agents/AGENTS.md` (grep gobernanza).
- No leídos (cumplimiento): preregistro, Trial #1, otros trials, `PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`.
- Llamadas a herramientas (aprox.): 24 [SELF-DECLARED]. No se ejecutó pytest ni la batería; sólo `git grep`/`Select-String` y lectura acotada.

## 1. Contexto y pregunta

El FRAME congela una decisión de producto que la auditoría de continuidad de integración dejó abierta (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:232-237`, F-03): Memory existe como implementación de referencia DEV, tiene seam en el worker y pruebas verdes, pero ningún consumidor del repositorio suministra un `MemoryStore`. La pregunta es si ARgentOS DEV debe convertir ese seam en **dependencia estándar del Execution Host** (construir el store en el camino normal del worker y aplicar contexto de memoria por defecto en cada delegación), o mantenerlo opcional por diseño.

Lo que está en juego no es «¿funciona Memory?» —funciona y está probado— sino **¿está conectada al sistema que debía consumirla, y debe estarlo?**. Un test verde prueba `WORKS`, no `IS INTEGRATED` (auditoría `:36`). El veredicto se emite sobre C-MEM; el baseline puede recomendar la alternativa opuesta vía `REVISE` (`FRAME-2.md:28`).

## 2. Evidencia disponible y verificada

**Seam sin consumidor (`OBSERVED`).** `AgentWorker.memory_store: object | None = None` (`runtime/orchestrator/agent_worker.py:373`); `execute()` aplica memoria sólo si el store no es `None` (`:427-430`). `git grep "MemoryStore("` sobre `runtime/` y `tools/` no devuelve coincidencias: ningún módulo de producción construye el store. `git grep "memory_store"` sólo devuelve la definición, el docstring y `tests/test_fc_host_integration.py:56-58`.

**Camino de construcción (`OBSERVED`).** La CLI construye `AgentWorker()` sin store (`runtime/orchestrator/__main__.py:188`), pero `--worker` tiene `default="command"` (`:100-108`): el `AgentWorker` **no** es el worker por defecto. El comentario del código declara que la CLI no puede construir un actor real y que el embedding inyecta su `AgentInvoker` (`:185-187`); el invoker por defecto es `NullAgentInvoker`, que no ejecuta nada (`agent_worker.py:364`). `ExecutionHost.__init__` recibe `worker` y cae a `CommandWorker()` (`host.py:414`, `:423`).

**Renderer vs contrato de registros (`OBSERVED`).** `build_memory_context` ordena ids, corta a 8 registros y 400 caracteres, y extrae texto probando `context`, `text`, `summary`, `note`; si ninguna existe usa `json.dumps(payload)[:400]` (`fc_flow.py:63-88`). El contrato canónico usa `KINDS = ("session","observation","evidence","claim","relation","synthesis")` con `statement` (claim), `description` (observation), etc. (`tools/check_memory_store.py:24-33`; `docs/plans/150-memory-system-implementation.md:546`). Los únicos registros ejercitados son inventados por tests con la clave `context` (`tests/test_fc_flow.py:70`, `:91-92`, `:123`).

**Productor (`OBSERVED`).** El único `MemoryStore.write` es `runtime/memory/consolidation.py:92` (`publish`), consumido sólo por tests; no hay productor de producción (`FRAME-2.md:62`).

**Durabilidad (`OBSERVED`).** `.project/` está gitignored (`.gitignore:13`); `git ls-files .project` devuelve 0. En este checkout `.project/knowledge` no existe (`Test-Path` → `False`; estado local, no evidencia versionada). `list_records()` devuelve `[]` si la base no es directorio (`runtime/memory/store.py:98-106`).

**Autoridad (`OBSERVED`).** `contain_actor_result` no acepta parámetro de memoria, verificado por `contains_memory_parameter` (`tests/test_fc_host_integration.py:71-74`); `ID-4` fija «Memory entra como contexto del actor, jamás como premisa ni autoridad» (`docs/plans/165-...:277`). La fila de evidencia de `AE-8` afirma «`runtime/memory/` no se consume desde el orquestador» (`docs/adr/19-autonomy-envelope-authority.md:165`).

**Estado documental.** RFC-80: `Implementation status: NOT IMPLEMENTED` (`docs/rfc/80-memory-system.md:15-16`, alcance Protocol); `11.7.0` (plan 150) publicó el reference runtime DEV (`docs/VERSIONING.md:366`). `runtime/README.md:452-473` describe `FC-3` como «memory as context» y no declara Memory capacidad estándar. `docs/plans/INDEX.md:1202-1204`: Plan 178 cerrado, F-03 abierto.

**Placement.** `.project/knowledge/` es la familia project-durable source-of-truth declarada Git-persisted (`docs/placement-contract.md:131`, §21 `:351`); `PC-48` prohíbe inventar namespace de representación (`:303`); el enforcement está diferido (`:376`, `:425`).

## 3. Interpretación

La evidencia sostiene una lectura que el FRAME no contiene y que cambia el peso de la decisión: **C-MEM cablearía memoria exactamente donde hoy no hay actor que consuma el prompt**. El `AgentWorker` que la CLI puede construir lleva `NullAgentInvoker`; el prompt con memoria se escribe en `agent-request.json` (`agent_worker.py:456-462`) y el transcript es «not-executed». El camino donde un actor real existe —`ExecutionHost(..., worker=AgentWorker(invoker=...))`— queda fuera de la propiedad 1 de C-MEM, que nombra sólo `__main__.py`: la «dependencia estándar» se declararía sobre la ruta que no la puede usar, y la ruta que sí podría quedaría sin cablear.

Segundo: hay **dos canales de contexto** y C-MEM consolida el equivocado. `ExecutionContext` ya tiene `knowledge_entries` y el materializador existente lo renderiza (`runtime/toolcalls/prompt_rendering.py:34-36`); `build_context` lo deja siempre vacío (`agent_worker.py:396`) mientras su docstring afirma que el prompt se produce por la materialización existente «never by a second renderer» (`:385-387`). `with_memory_context` añade texto **después** del render (`:424-430`): C-MEM convertiría esa desviación en estándar con el campo de primera clase vacío.

Tercero: el renderer no habla el idioma del contrato. Un `claim` canónico se renderiza como JSON truncado a 400 caracteres, no como su `statement`; con `limit=8` la aplicación por defecto inyectaría hasta ocho blobs por prompt, en un formato (`{"context": ...}`) que ningún productor del repositorio genera.

Cuarto: aun cableado, hoy el contexto sería vacío (`list_records()` sobre base inexistente → `[]`): C-MEM no entrega capacidad, entrega una conexión preparada. Eso no es un defecto por sí mismo, pero sí lo es **declararlo** «capacidad estándar».

## 4. Alternativas consideradas

- **A0 — statu quo (seam opcional).** Coste cero, conducta actual, F-03 abierto. No resuelve la ambigüedad señalada.
- **A1 — C-MEM literal.** Cableado en `__main__.py`, aplicación por defecto, declaración «capacidad estándar», test de integración. Coste bajo y reversible, pero arrastra los cuatro defectos de §3.
- **A2 — C-MEM′ (revisión del candidato).** Misma dirección, distinto punto de composición y de renderizado, declaración proporcional y corrección separada de `AE-8`. Es la que recomiendo.
- **A3 — Memory opcional por diseño** (alternativa explícita del FRAME `:28`): reclasificar F-03 como aislamiento deliberado. Coherente, pero deja el renderizado como código muerto de producción.

## 5. Supuestos

- S-1: el camino destinado a actores reales es el embedding con `AgentInvoker` inyectado, no la CLI sola (`INFERRED` de `__main__.py:185-187`).
- S-2: `.project/knowledge/` sigue siendo la base correcta, sin subdirectorio, por `PC-48` y el precedente del Plan 150 (`docs/plans/150-...:74`, `:546`).
- S-3: los registros canónicos son los del contrato de `check_memory_store.py`, no la forma `{"context": ...}` de los tests.

## 6. Riesgos y argumentos

**B-1 — El cableado apunta a una ruta sin actor.** C-MEM cablea el store sólo en `__main__.py`, donde `AgentWorker()` lleva `NullAgentInvoker` y `--worker` no es el default. Ancla: `__main__.py:100-108`, `:185-188`; `agent_worker.py:364`. Consecuencia: la capacidad declarada estándar no la consume ningún actor; el embedding real sigue sin store.

**B-2 — Renderer incompatible con el contrato de registros.** `_record_text` sólo reconoce `context/text/summary/note`; los kinds canónicos usan `statement`/`description` y caen en `json.dumps(...)[:400]`. Ancla: `fc_flow.py:63-88`; `check_memory_store.py:24-33`; `tests/test_fc_flow.py:70`. Consecuencia: la aplicación por defecto inyectaría JSON truncado en cada prompt; el estándar se entregaría como ruido que aumenta el coste de contexto sin información.

**B-3 — Sin productor, la dependencia estándar es inerte.** El único `write` es `consolidation.publish`, consumido sólo por tests. Ancla: `runtime/memory/consolidation.py:92`; `git grep "MemoryStore("` → 0; `FRAME-2.md:62`. Consecuencia: C-MEM no cambia ninguna conducta observable; declararla estándar afirma sobre la intención, no sobre el comportamiento (criterio 1: no-op con apariencia de capacidad).

**B-4 — La durabilidad declarada no está materializada.** `.project/` está gitignored y no tiene archivos versionados. Ancla: `.gitignore:13`; `git ls-files .project` → 0; `docs/placement-contract.md:131`, `:351`. Consecuencia: la dependencia estándar descansa sobre una base que Git no persiste; el store sería invisible para CI y otros clones, con drift y pérdida silenciosa como modo de fallo.

**B-5 — Segundo canal de contexto contra la invariante declarada.** `knowledge_entries` existe y se renderiza, pero `build_context` lo deja vacío y memoria entra como sufijo posterior al render mientras el docstring niega un segundo renderer. Ancla: `prompt_rendering.py:34-36`; `agent_worker.py:385-402`, `:424-430`. Consecuencia: se estandarizan dos canales y se vuelve falsa una afirmación del propio código; migrar después costará más que decidirlo ahora.

**B-6 — Falta de filtrado por lifecycle/epistemic.** `build_memory_context` toma los primeros 8 ids ordenados, sin consultar lifecycle, epistemic state ni `retrieval.eligible`. Ancla: `fc_flow.py:78-88`; `runtime/memory/retrieval.py:22`. Consecuencia: registros `stale`, `contradicted` o `retired` entrarían en todos los prompts; contexto obsoleto es peor que contexto ausente y actúa como premisa de facto sin ser autoridad.

**B-7 — La fila de evidencia de `AE-8` ya es inexacta, con o sin C-MEM.** ADR-19 afirma que `runtime/memory/` no se consume desde el orquestador, pero `execute` consume `build_memory_context` cuando recibe un store. Ancla: `docs/adr/19-autonomy-envelope-authority.md:165`; `agent_worker.py:427-430`; `docs/plans/165-...:420`. Consecuencia: la actualización documental del ítem 3 de C-MEM no deriva del wiring, es deuda de evidencia vencida; colgarla del cambio de diseño la posterga y deja el estado mal declarado.

**B-8 — La no-autoridad es estructural, no conductual.** La frontera no acepta memoria (`tests/test_fc_host_integration.py:71-74`), pero ninguna prueba en la ruta por defecto verifica que un registro hostil no altere el veredicto de efectos. Ancla: `fc_flow.py:91-95`; `tests/test_fc_flow.py:101-104`; `FRAME-2.md:25`. Consecuencia: riesgo acotado por diseño, pero la evidencia de que se mantiene bajo un store suministrado es estructural.

## 7. Incertidumbres y GAP

- **GAP 1:** no existe declaración de producto ni acto de autoridad que determine si Memory debe ser estándar u opcional; F-03 sigue abierto con dueño mantenedor (`docs/plans/INDEX.md:1202-1204`). Emito advisory.
- **GAP 2:** no hay corrida end-to-end con actor externo; `tests/test_fc_host_integration.py:8-9` declara que es detector de wiring. El valor de memoria en ejecución real es `INFERRED`, no `MEASURED`.
- **GAP 3:** el `Change Level` del Change que implemente C-MEM′ no está calculado; no lo infiero.

## 8. Decisión / recomendación

**REVISE** — la dirección de C-MEM es correcta; el candidato tal como está especificado debe revisarse antes de implementarse. No recomiendo `PROCEED` sobre C-MEM literal ni `GATHER_EVIDENCE` como decisión final: la evidencia alcanza para decidir la dirección y para rechazar la forma concreta.

Fundamento: el destino «Memory como contexto estándar del Host DEV» es coherente con `ID-4`/`AE-8` y con el plan 165 (que ya declaró `FC-3` integrado); el seam funciona y la frontera no admite memoria. Pero C-MEM cablea la ruta sin actor (B-1), usa un renderer que no habla el contrato (B-2), consolida el canal equivocado (B-5) y, sin productor, declara estándar algo inerte (B-3) sobre una base que Git no persiste (B-4). Implementarlo así produce una capacidad nominal: prompt más largo, ningún efecto observable, y una declaración que el comportamiento desmiente.

**C-MEM′ — condiciones de revisión (las cuatro necesarias):**

- **R-1 Punto de composición único.** Construir y suministrar el store en el punto compartido por CLI y embedding (factory de worker o parámetro de `ExecutionHost.__init__`), no sólo en `__main__.py`. Criterio: un adoptante con `AgentInvoker` propio recibe el store sin cableado adicional.
- **R-2 Canal único y renderer conforme al contrato.** Memoria entra por `ExecutionContext.knowledge_entries`, o `_record_text` mapea `statement`/`description`/`summary` y filtra por lifecycle/epistemic (`retrieval.eligible`). Criterio: un `claim` canónico se renderiza como su `statement` y un registro `retired` no aparece.
- **R-3 Declaración proporcional al comportamiento.** `runtime/README.md` y el registro de estado declaran «cableada al camino estándar, inerte mientras no exista productor», no «capacidad estándar» a secas. Criterio: la declaración no puede leerse como disponibilidad de memoria hoy.
- **R-4 Corrección de evidencia separada y previa.** Actualizar la fila `AE-8` como Change docs-only independiente, porque ya es inexacta en HEAD (B-7). Criterio: la fila distingue «consumido por el ejecutor cuando se suministra» de «ningún camino de producción lo suministra», sin tocar la norma.

Si R-1…R-4 no se aceptan, la alternativa preferible es **A3** (Memory opcional por diseño, F-03 reclasificado como aislamiento deliberado con justificación explícita), más honesta que un estándar inerte. Lo que no es defendible es el statu quo sin declaración: deja el renderizado como código de producción sin consumidor y una fila de ADR falsa.

## 9. Plan (si corresponde)

Secuencia recomendada, **no ejecutada** (resultado advisory; no autoriza cambios):

1. Acto de decisión de producto sobre F-03 (mantenedor): estándar-con-revisión vs opcional por diseño. Sin esto no hay Change.
2. Change docs-only de corrección de `AE-8` (R-4), independiente y previo.
3. Plan del Change de cableado (`Change Level` hoy `GAP`, `Scope` sobre `runtime/orchestrator/`, `tests/`, `runtime/README.md`); rige `.agents/AGENTS.md:50-55` (sin plan aprobado → STOP). RFC-56: **N/A**, `protocol/.agents/` intacto.
4. Implementación R-1/R-2, con test de integración en la ruta por defecto (store ⇒ contexto; sin store ⇒ no-op) y counterproof de registro hostil (B-8).
5. Declaración R-3 y validación con la batería canónica de `docs/VERSIONING.md` §4.1.

## 10. Qué evidencia cambiaría la decisión

- **Hacia `PROCEED` literal:** un productor de registros ya consumido en producción, o una corrida end-to-end con actor externo donde el contexto de memoria cambie una decisión de forma observable. Nada de eso existe en HEAD.
- **Hacia `PROCEED` sobre C-MEM′:** aceptación de R-1…R-4 como alcance del Change.
- **Hacia A3:** un acto de producto que declare la ausencia de consumidor como aislamiento deliberado, o evidencia de que mantener el wiring cuesta más que su valor.
- **Hacia `GATHER_EVIDENCE`:** sólo si el mantenedor exige medir valor antes de decidir (requiere productor + actor externo, hoy no disponibles).

Confianza en la decisión: **media-alta**. Alta en los hallazgos de código (B-1, B-2, B-5, B-7 son `OBSERVED` y reproducibles); media en la ponderación de producto, porque «debe ser estándar» es una decisión reservada que el repositorio no contiene.


## Apéndice D — DEFENSE_2 (verbatim)

# DEFENSE-2 — Case-02 (Memory como dependencia estándar del Execution Host)

## Metadata
- Rol: Defense (strongest case FOR), fresh independiente.
- Frame verificado: SHA-256 = `A64AE4ADBF1C550019A742F036FBA55AF797B926F87740EA5BAC80F359EBE0C2` (coincide; `Get-FileHash -Algorithm SHA256`).
- HEAD observado: `d61e327` (`dev`); el FRAME declara `e7bc881`. Entre ambos, `git diff --stat` sólo agrega el preregistro y toca `docs/working/research/INDEX.md`: `runtime/`, `tests/`, `tools/` y el `docs/` sustantivo no cambian. [OBSERVED]
- STARTED: 2026-10-25T13:37:18-03:00
- FINISHED: 2026-10-25T13:44:20-03:00
- Archivos leídos: `FRAME-2.md`; `runtime/memory/{store,__init__,consolidation}.py`; `runtime/orchestrator/{agent_worker,__main__,fc_flow}.py`; `runtime/README.md`; `tests/{test_fc_host_integration,test_fc_flow}.py`; `tools/check_memory_store.py`; `docs/placement-contract.md`; `docs/adr/{19,16}-*.md`; `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md`; sólo `Select-String` sobre `docs/plans/{165,150,INDEX}`, `docs/rfc/80-memory-system.md`, `docs/VERSIONING.md`, `runtime/orchestrator/host.py`, `.gitignore`.
- Llamadas a herramientas (aprox.): 55 [SELF-DECLARED]
- Declaración: no leí baseline, prosecution, preregistro ni el otro trial; un `git grep` devolvió dos líneas del preregistro, que no abrí, no usé como evidencia ni cito.

## 1. Tesis de la defensa

C-MEM no propone una capacidad nueva: propone que el Execution Host DEV tenga **una sola forma de construir su worker**, y que esa forma incluya Memory como contexto. El caso más fuerte se apoya en tres pilares verificables: (i) la ruta real contradice la ruta que el repositorio ya declara; (ii) el efecto actual es indistinguible de cero y la reversión es un call site, mientras la alternativa no produce evidencia nueva; (iii) `MEMORY ≠ AUTHORITY` es estructural y ejecutable, así que conectar el contexto por defecto no toca el veredicto de containment.

La defensa declara su flanco débil de entrada: **no hay productor de registros en producción, `.project/knowledge/` no existe en este HEAD y el host no tiene invoker real**. El argumento no es «Memory mejora el recall hoy» —sería falso— sino «Memory debe ser dependencia estándar y el recall es una condición, no la premisa». La alternativa no es más conservadora: es la misma ausencia, congelada y sin test.

## 2. Argumentos (D-1..D-8)

### D-1 — C-MEM vuelve verdadera la ruta que el repositorio ya declara
- **CLAIM:** el sistema documenta Memory como paso del flujo estándar y la ruta estándar nunca lo ejecuta; C-MEM alinea ejecución y declaración sin agregar arquitectura.
- **EVIDENCE:** `runtime/README.md:454-473` describe `build_memory_context + with_memory_context (FC-3)` como paso de `AgentWorker.execute` («part of `AgentWorker`, not a second architecture»), y `docs/plans/165-f-c-autonomy-frontier-implementation.md:368` describe ese flujo como materializado. Contra eso, `git grep "memory_store" -- runtime/` devuelve sólo definición (`agent_worker.py:373`) y uso condicional (`:427-430`), sin suministro; `__main__.py:188` construye `AgentWorker()` sin store. [OBSERVED]
- **ASSUMPTION:** la descripción de arquitectura de un flujo se lee como la ruta estándar que ese flujo toma, no como un gancho para terceros.
- **CRITERION:** 2 (integración).
- **CONSEQUENCE:** aceptar C-MEM hace que la documentación deje de describir un paso que la ruta nunca da. Rechazarlo obliga a corregirla (FC-3 como capacidad de embedding), mismo costo documental y sin evidencia nueva.
- **CONFIDENCE:** alta (0.85).

### D-2 — «Opcional por diseño» no está establecido por ninguna evidencia
- **CLAIM:** la alternativa se presenta como statu quo, pero el statu quo es una decisión pendiente; la evidencia es permisiva, no prohibitiva.
- **EVIDENCE:** `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:§6.1` (`:178-180`) descarta `ORPHANED` porque «no hay un consumidor requerido e incumplido demostrado», y cierra: el estado final es «una decisión de producto pendiente, no una inferencia»; `:§F-03` (`:232-237`) la deja abierta. `docs/adr/19-autonomy-envelope-authority.md:§Amendment Log` (`:137-138`) enumera «integración de Memory» entre lo que «requiere su propia autorización»: reserva, no prohibición. [OBSERVED]
- **ASSUMPTION:** una decisión pendiente debe resolverse con la opción que produce evidencia y puede revertirse, no con la que congela el estado que la auditoría diagnosticó.
- **CRITERION:** 1 (correctness / necesidad).
- **CONSEQUENCE:** sin C-MEM, F-03 se cierra con la misma ausencia que lo abrió; con C-MEM, con un cambio observable y una prueba, reversible y registrado.
- **CONFIDENCE:** media-alta (0.75).

### D-3 — Costo marginal y reversión: ambos ≈ 0
- **CLAIM:** aceptar hoy no hipoteca nada medible y cuesta una línea de producción; rechazar hoy hipoteca la decisión a otra ronda.
- **EVIDENCE:** `MemoryStore.__init__` no crea directorios (`runtime/memory/store.py:71-72`); `list_records` devuelve `[]` si la base no es directorio (`:98-106`); `read` es fail-closed (`:81-92`). Aquí `Test-Path .project/knowledge` = `False` y `git ls-files .project` = 0 [MEASURED]. Con base vacía, `build_memory_context` devuelve contexto vacío y `with_memory_context` devuelve el prompt intacto (`fc_flow.py:78-95`; `tests/test_fc_flow.py:80-85`). El campo conserva default `None` (`agent_worker.py:373`), así que las suites con `AgentWorker()`/`AgentWorker(invoker=...)` y el detector `tests/test_fc_host_integration.py:56-58` siguen pasando; `check_memory_store` no figura en la batería de `docs/VERSIONING.md:§4.1` (`Select-String` sin coincidencias). [OBSERVED]
- **ASSUMPTION:** bajo incertidumbre sobre la necesidad, la reversibilidad y el costo marginal son criterios de decisión, no detalles de implementación.
- **CRITERION:** 5 y 6 (cost / reversibility).
- **CONSEQUENCE:** retirar el wiring restaura el comportamiento y `AgentWorker().memory_store is None`, lo que promete la propiedad 6; 1 call site + 1 factory + 1 test + 2 documentos, sin migración, contrato ni dato que deshacer.
- **CONFIDENCE:** alta (0.85).

### D-4 — El placement ya está resuelto y C-MEM no lo reabre
- **CLAIM:** la base plana no es invención del candidato: es una decisión de placement ya autorizada, y un subdirectorio violaría el contrato.
- **EVIDENCE:** `docs/placement-contract.md:§6` (`:131`) declara `.project/knowledge/` en la familia project-durable; `PC-48` (`:303`) manda que un `derived` use el namespace canónico de su familia y prohíbe inventar representation namespace; `docs/plans/150-memory-system-implementation.md:74` registra `PLACEMENT_DECISION = ADAPT`, `TARGET = .project/knowledge/` (decisión humana 2026-10-06); `tools/check_memory_store.py:2,86-89` ya resuelve esa base plana y trata la ausencia como válida. [OBSERVED]
- **ASSUMPTION:** una decisión de placement registrada y autorizada sigue siendo la autoridad de ubicación; el consumidor no la re-litiga.
- **CRITERION:** 2 (integración).
- **CONSEQUENCE:** el cambio se reduce a construcción y consumo; «sin inventar un subdirectorio» es la única forma conforme con PC-48, y PC-53 impediría crear familia nueva.
- **CONFIDENCE:** alta (0.9).

### D-5 — La autoridad se preserva estructuralmente, no por convención
- **CLAIM:** conectar Memory por defecto no puede convertirla en premisa ni autoridad: la frontera no acepta memoria por construcción.
- **EVIDENCE:** `contain_actor_result` no tiene parámetro de memoria (`fc_flow.py:323-333`); `contains_memory_parameter` es la contraprueba ejecutable (`:381-393`); el veredicto se computa sólo desde comandos observados y scope (`agent_worker.py:521-527`); `tests/test_fc_flow.py:98-117` muestra que un registro hostil («pre-authorized every effect») no cambia el veredicto; el bloque se rotula «context, not authority» (`fc_flow.py:52-57`). [OBSERVED/MEASURED]
- **ASSUMPTION:** el containment se computa desde efectos observados y no desde el texto del prompt; el contenido de Memory no puede volverse autoridad.
- **CRITERION:** 3 (authority).
- **CONSEQUENCE:** `AE-8` e `ID-4` quedan intactos. Sólo cambia la fila de evidencia de `docs/adr/19-autonomy-envelope-authority.md:165`, y el ADR ya ofrece el mecanismo: Amendment Log aditivo que «agrega y preserva su texto íntegro» (`:110-115`), con precedente sobre esa misma tabla (`:154-168`).
- **CONFIDENCE:** alta (0.85).

### D-6 — El ciclo de vida ya está resuelto en el nivel que el consumidor necesita
- **CLAIM:** el wiring no crea problema de ownership porque el consumidor es read-only y toda falla degrada a contexto vacío.
- **EVIDENCE:** lecturas fail-closed y `list_records` que saltea corruptos (`runtime/memory/store.py:81-106`); escritura atómica y single-writer declarado (`:20-23`, `:40-60`); render acotado a `limit=8`, `max_chars=400` (`fc_flow.py:71-88`) ⇒ ≤ ~3.5 KB por delegación; `rebuild` determinista (`store.py:108-113`). [OBSERVED]
- **ASSUMPTION:** un consumidor que sólo lee no adquiere obligación de ownership; la posesión y la reconstrucción siguen siendo del productor y de `rebuild`.
- **CRITERION:** 4 (maintainability).
- **CONSEQUENCE:** vacío, corrupto u obsoleto no produce error ni autorización: produce contexto vacío o parcial acotado. El costo nuevo es un call site.
- **CONFIDENCE:** alta (0.8).

### D-7 — La alternativa multiplica el trabajo y lo deja sin verificación
- **CLAIM:** dejar Memory opcional traslada la construcción a cada embedder y mantiene la conducta del seam fuera de observación.
- **EVIDENCE:** `git grep "AgentWorker("` muestra dos puntos de construcción: la CLI (`__main__.py:188`) y el camino de embedding (`runtime/README.md:399`; `agent_worker.py:269-276`). Sin punto canónico, cada embedder resuelve base y store: N wirings con drift posible contra PC-48/PC-52, y ningún test fija la semántica. `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:§10.6` (`:270`) registra como no evidenciado «el comportamiento de Memory en un Host real con un `MemoryStore` suministrado». [OBSERVED]
- **ASSUMPTION:** una capacidad opcional sin punto de construcción canónico no es más simple, sólo más difusa.
- **CRITERION:** 1 (con apoyo en 4).
- **CONSEQUENCE:** C-MEM fija un punto de construcción y una semántica verificable; la alternativa externaliza ambas y deja el gap de §10.6 abierto por diseño.
- **CONFIDENCE:** media-alta (0.75).

### D-8 — La «apariencia de capacidad» se neutraliza declarando la condición
- **CLAIM:** el candidato no afirma que hoy haya recall; declara el beneficio como condicional, y esa declaración es lo que impide leer la capacidad como algo que no es.
- **EVIDENCE:** propiedades 4 (declaración que «no crea autoridad ni obligación») y 6 («no crea un productor… el beneficio es condicional»); el estado real es verificable: base inexistente (`Test-Path` falso) y sin productor de producción (`runtime/memory/consolidation.py:92` es el único `store.write`; `publish` no tiene consumidores fuera de `tests/test_memory_synthesis_consolidation.py`). [OBSERVED/MEASURED]
- **ASSUMPTION:** una declaración que nombra su condición es preferible a una ausencia que no declara nada, porque sólo la primera puede verificarse y refutarse.
- **CRITERION:** 1 (correctness / necesidad).
- **CONSEQUENCE:** con C-MEM, «¿esto aporta algo hoy?» tiene respuesta escrita y testeable («hoy no aporta recall; aporta ruta única, consumo observable y evidencia»); con la alternativa queda sin respuesta y sin test.
- **CONFIDENCE:** media (0.7).

## 3. Condiciones de validez del candidato

- **C-1 (placement).** Base plana `.project/knowledge/` resuelta por PC-48 y por el `ADAPT` del Plan 150; sin subdirectorio ni familia nueva; si el resolver diera otra representación, se re-resuelve antes de implementar.
- **C-2 (declaración honesta).** La declaración de capacidad estándar dice, en el mismo lugar, que el store puede estar vacío, que el contexto puede ser vacío y que este Change no produce registros. Sin esa cláusula, la propiedad 4 se convierte en la apariencia que el criterio 1 teme.
- **C-3 (un punto de construcción, testeable).** La construcción se factoriza en una función pura por root (`build_worker(root)`), usada por la CLI y reutilizable por un embedder; la prueba la ejerce con root temporal. Sin esto, el wiring cubre sólo la CLI con `NullAgentInvoker`.
- **C-4 (evidencia, no norma).** La fila de `AE-8` se actualiza **aditivamente** por Amendment Log, preservando la afirmación histórica; `AE-8` no cambia y se determina si la decisión satisface `AU-6` (ADR propio) o basta la enmienda. `docs/adr/16-change-lifecycle-authority.md:68-78` y `docs/adr/19-autonomy-envelope-authority.md:73-75` ya exigen autorización propia para la integración de Memory.
- **C-5 (ambas ramas probadas).** Store con registros ⇒ bloque de contexto en el prompt; store ausente/vacío ⇒ prompt idéntico; sin store compartido entre tests ni escritura al repositorio.
- **C-6 (durabilidad declarada).** No puede afirmarse durabilidad Git: `.gitignore:13` ignora `.project/` y `git ls-files .project` devuelve 0. [MEASURED] El wiring no depende de ello, pero la declaración no puede sugerirlo.
- **C-7 (cierre correcto de F-03).** «Consumidor estándar establecido, productor pendiente», no «integración completa».

## 4. Por qué la alternativa es inferior

1. **No decide: congela.** Deja F-03 en el estado que lo abrió y no produce evidencia para revisarlo (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:§F-03`).
2. **Multiplica el punto de decisión.** Sin constructor canónico, cada embedder resuelve base y store; el riesgo de inventar subdirectorio (PC-48) o excepción (PC-52) se distribuye en N lugares en vez de fijarse en uno.
3. **Deja la conducta sin observación.** El comportamiento que la auditoría declara no evidenciado (`:270`) seguiría sin evidencia por diseño; C-MEM al menos lo vuelve ejercitable en la ruta estándar.
4. **No ahorra documentación.** Declarar Memory opcional exige corregir `runtime/README.md:454-473` y la lectura de FC-3 en el Plan 165: mismo trabajo, sin test y sin capacidad.
5. **Asimetría del error.** Si Memory es innecesaria, C-MEM se retira con un call site; si es necesaria, la alternativa obliga a un segundo Change que reabre la decisión con menos información.

## 5. Límites que la defensa reconoce

- **L-1.** No hay beneficio hoy ni medición posible aquí: sin productor de producción, con `.project/knowledge/` inexistente y sin invoker real, el wiring es inerte hasta que existan registros y el beneficio externo no es medible (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:§10.6`). [MEASURED]
- **L-2.** La durabilidad Git de `.project/knowledge/` **no está materializada** (`.gitignore:13`; `git ls-files .project` = 0). Es un `GAP` del contrato, no del candidato, y C-MEM no puede asumirlo.
- **L-3.** La CLI sólo construye `NullAgentInvoker` (`agent_worker.py:285-304`); sin C-3, el wiring no alcanza al actor que realmente ejecuta.
- **L-4.** `_record_text` busca `context`/`text`/`summary`/`note` (`fc_flow.py:63-68`) mientras el contrato de registro usa `statement`/`description` (`tools/check_memory_store.py:26-33`): un registro canónico sin clave de texto se renderiza como JSON crudo acotado. Limitación preexistente del seam; debe declararse o refinarse.
- **L-5.** Memory no valida contenido al leer: un registro hostil entra al prompt como texto. No altera el veredicto (D-5), pero puede influir en la conducta del actor; la contención lo cubre como cualquier texto no confiable.
- **L-6.** La necesidad no está demostrada por uso: el caso se sostiene en coherencia arquitectónica, costo y reversibilidad, no en un defecto probado.

## 6. Compromiso

- **POSITION:** `SUPPORT_WITH_CONDITIONS`.
- **CONFIDENCE:** 0.72.
- **CONDITIONS UNDER WHICH THE CANDIDATE IS VALID:** C-1 a C-7 de §3: placement plano ya resuelto, declaración de condicionalidad, punto único de construcción por root, evidencia aditiva de `AE-8`, ambas ramas probadas sin escribir al repositorio y `GAP` de durabilidad declarado.
- **WHAT WOULD CHANGE MY POSITION:**
  - Un acto de autoridad que declare Memory opcional por diseño, o una lectura vinculante de RFC-80/ADR-19 que prohíba un consumidor estándar ⇒ `OPPOSE`.
  - Que la construcción no pueda factorizarse y el wiring quede limitado a la CLI con invoker nulo, sin prueba posible sin escribir en el repositorio ⇒ `OPPOSE_WITH_CONDITIONS`.
  - Que la implementación vuelva no determinista el prompt por defecto (registros variables entre delegaciones sin congelamiento por corrida) o rompa suites existentes ⇒ `OPPOSE` hasta acotarlo.
  - Que el placement exija subdirectorio o familia nueva ⇒ `OPPOSE` hasta resolver por autoridad (PC-48/PC-53).
  - Que se rechace declarar o refinar `_record_text` y quede JSON crudo sin declararlo ⇒ baja la confianza y el caso pasa a `OPPOSE_WITH_CONDITIONS`.


## Apéndice E — PROSECUTION_2 (verbatim)

# PROSECUTION-2 — Case-02 (Memory como dependencia estándar del Execution Host)

## Metadata

- **Rol:** Prosecution (strongest case AGAINST), contexto `fresh` independiente.
- **Frame verificado:** SHA-256 = `A64AE4ADBF1C550019A742F036FBA55AF797B926F87740EA5BAC80F359EBE0C2` (coincide).
- **STARTED:** 2026-10-25T13:45:48-03:00
- **FINISHED:** 2026-10-25T13:51:14-03:00
- **HEAD observado:** `d61e327` (`dev`); el FRAME se congeló contra `e7bc881`. `git diff --stat e7bc881..d61e327` = sólo preregistro e INDEX de working, sin cambios en `runtime/`, `tests/` ni `docs/` citados: la evidencia es idéntica (`OBSERVED`).
- **Archivos leídos íntegros:** `.project/campaign/frames/FRAME-2.md`; `runtime/orchestrator/agent_worker.py`; `runtime/orchestrator/__main__.py`; `runtime/orchestrator/fc_flow.py`; `runtime/memory/store.py`; `runtime/memory/consolidation.py`; `runtime/memory/retrieval.py`; `runtime/toolcalls/prompt_rendering.py`; `tests/test_fc_host_integration.py`; `tools/check_memory_store.py`.
- **Archivos consultados por sección/comando:** `tests/test_fc_flow.py` (:55-144); `runtime/memory/__init__.py` (:1-12); `docs/plans/165-f-c-autonomy-frontier-implementation.md` (`ID-4`, matriz `FC-*`, integración); `docs/plans/150-memory-system-implementation.md` (cabecera y `## Nota de ejecución`); `docs/adr/19-autonomy-envelope-authority.md` (`AE-8`, `Amendment Log`, tabla de evidencia); `docs/adr/INDEX.md`; `docs/placement-contract.md` (§6, §14-15, §21-22); `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md` (§1, §5.4, §6.1, §9, §10, §12); `docs/plans/INDEX.md`; `docs/rfc/80-memory-system.md`; `runtime/README.md`; `docs/VERSIONING.md` (§4.1); `docs/CONVENTIONS.md`; `docs/AGENTS.md`; `.gitignore`.
- **Comandos de lectura:** `git rev-parse`, `git log`, `git status`, `git diff --stat e7bc881..d61e327`, `git grep`, `git ls-files .project`, `Get-FileHash`, `Get-Content`, `Select-String`.
- **Llamadas a herramientas (aprox.):** 54 [SELF-DECLARED]
- **Declaración:** no leí baseline, defense, preregistro ni el otro trial; sólo `frames/FRAME-2.md` bajo `.project/campaign/`. No modifiqué archivos versionados ni usé `git add/commit/checkout/reset`.

## 1. Tesis de la acusación

C-MEM no conecta una capacidad: **convierte una decisión de producto pendiente en una apariencia de integración**. Memory tiene un seam correcto (`agent_worker.py:373,427-430`), primitivas sólidas (`store.py`) y semántica de retrieval (`retrieval.py`), pero no tiene productor en producción (`consolidation.py:77-93` es el único `MemoryStore.write` y sólo lo consumen tests) ni ruta que suministre el store. El candidato propone estandarizar el consumo de un store vacío, sobre un directorio compartido y no versionado, con un renderer que no entiende el schema ni la elegibilidad de retrieval. El resultado probable no es contexto estándar: es un no-op observable en el prompt, con apariencia de capacidad y costo documental y de gobernanza real.

La acusación no sostiene que Memory sea inútil ni que el seam esté mal diseñado. Sostiene que la pregunta abierta es **F-03** —«Memory opcional por diseño vs dependencia estándar»— (`INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:232-237`) y que C-MEM la responde por default de código sin resolverla. `FC-3` ya figura materializado y verificado sin wiring por defecto (`docs/plans/165-f-c-autonomy-frontier-implementation.md:359,420`): el candidato no cierra un gap registrado, crea una postura nueva.

## 2. Objeciones (P-1..P-10)

### P-1 — Estandariza un seam sin productor ni consumidor: no-op con apariencia de capacidad

- **OBJECTION:** El candidato declara «capacidad estándar» un camino que hoy no recibe store y cuyo único productor no tiene consumidor de producción. Admite que el beneficio es condicional (item 6) y, aun así, declara estándar el consumo.
- **TYPE:** REAL.
- **EVIDENCE:** `OBSERVED` — `runtime/memory/consolidation.py:77-93` (`publish` es el único `MemoryStore.write`); `git grep "MemoryStore(" -- runtime tools` = 0 coincidencias (sólo tests); `git grep "memory_store" -- runtime` = definición y uso en `agent_worker.py:373,427-430`, sin call site que lo suministre; `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:173-180` y `:232-237` (F-03 abierto).
- **TARGET:** criterio 1 (necesidad); item 6 («beneficio condicional»).
- **CONSEQUENCE:** en toda corrida actual el contexto es vacío y el único delta es el hash del prompt. Peor: `--worker agent` construye `NullAgentInvoker` (`__main__.py:184-188`), que no ejecuta nada; aun con registros, el prompt no llega a un actor. Declarar «estándar» convierte F-03 en una decisión tomada por apariencia.
- **CONFIDENCE:** 0.95.

### P-2 — El renderer de contexto no entiende el schema de los registros de Memory

- **OBJECTION:** `build_memory_context` busca las claves `context`/`text`/`summary`/`note`, que **no son campos de ningún `kind` del contrato de Memory**. Un registro conforme al contrato cae siempre al fallback `json.dumps(...)[:400]`: el «contexto» estándar sería JSON truncado a mitad de token.
- **TYPE:** REAL.
- **EVIDENCE:** `OBSERVED` — `fc_flow.py:63-68` (claves preferidas y fallback), `:82-88`; `tools/check_memory_store.py:24-33` (campos requeridos por kind: ninguno es `context/text/summary/note`); los tests de FC-3 usan `{"context": ...}` (`tests/test_fc_flow.py:69-77`), que `check_memory_store.py:62-64` rechazaría como `unknown kind`.
- **TARGET:** item 2 («aplica contexto de memoria»); criterio 1 (corrección).
- **CONSEQUENCE:** La prueba de FC-3 valida una forma de registro que el contrato de Memory no admite, y el camino estándar produce blobs ilegibles: el claim «contexto de memoria» no se sostiene sobre registros reales.
- **CONFIDENCE:** 0.90.

### P-3 — «Base plana sin subdirectorio» colisiona con otros artefactos project-durable, y el store no filtra por `kind`

- **OBJECTION:** El candidato prohíbe inventar subdirectorio y usa `.project/knowledge/` plano, la familia project-durable completa donde `runtime/toolcalls/project_store.py:3` designa `project_segment.json`. `MemoryStore.list_records` devuelve **todo** `*.json` legible y `build_memory_context` no filtra por `kind`; cualquier JSON ajeno se vuelve «memoria».
- **TYPE:** REAL.
- **EVIDENCE:** `OBSERVED` — `store.py:98-106` (glob `base/*.json` + `read`, sin filtro), `fc_flow.py:82-88` (sin `kind`); `placement-contract.md:131` (familia project-durable); `runtime/toolcalls/project_store.py:3` («`.project/knowledge/project_segment.json`»); `docs/rfc/80-memory-system.md:31`; `check_memory_store.py:86-100` (`rglob("*.json")` trata todo JSON de la familia como registro de Memory).
- **TARGET:** item 1 (placement «sin inventar subdirectorio»); `PC-48` (`placement-contract.md:303`: un `derived` no inventa namespace de representación).
- **CONSEQUENCE:** `project_segment.json` u otro JSON hermano entra al prompt como memoria; dos clases de artefacto comparten namespace con validadores incompatibles. «No inventar subdirectorio» no es neutral: delega una decisión de namespace a un glob.
- **CONFIDENCE:** 0.90.

### P-4 — El contexto por defecto ignora la semántica de retrieval de Memory

- **OBJECTION:** El candidato estandariza la lectura cruda del store, no el retrieval del Memory System. Quedan fuera la elegibilidad por lifecycle, la exclusión de contradicciones y la no reactivación de histórico: «un solo consumidor» se cumple en la forma y se rompe en la semántica.
- **TYPE:** REAL.
- **EVIDENCE:** `OBSERVED` — `retrieval.py:7-9,22-38` (sólo `active`; excluye `contradicted`, `candidate`, histórico; `I-008`/`I-014`/`I-025`); `runtime/memory/__init__.py:10-12` no exporta retrieval, por lo que el store duck-typed lo esquiva; `fc_flow.py:71-88` no consulta lifecycle; `docs/rfc/80-memory-system.md:609-620`; plan 150 Phase 9 registra retrieval como entregado.
- **TARGET:** criterio 2 (integración); item 2.
- **CONSEQUENCE:** el contexto estándar puede presentar como vigente un claim `superseded`, `retired`, `contradicted` o `archived`, exactamente lo que la arquitectura prohíbe en retrieval operacional.
- **CONFIDENCE:** 0.85.

### P-5 — Durabilidad declarada y no materializada; el store es «derived/rebuildable» sin fuente de rebuild en DEV

- **OBJECTION:** El candidato apoya una dependencia estándar en la «ubicación canónica project-durable». Esa persistencia Git está declarada por contrato pero no materializada, y el rebuild exige que el llamador aporte los registros: no hay fuente semántica en DEV.
- **TYPE:** REAL.
- **EVIDENCE:** `OBSERVED` — `placement-contract.md:131,351-372` (PC-67/68/70); `.gitignore:13` (`.project/`); `git ls-files .project` = 0 archivos; `store.py:17-23` (derivado, rebuildable, concurrencia no especificada), `:108-114` (`rebuild(records)` recibe el mapping); `consolidation.py:77-93`; `docs/rfc/80-memory-system.md:315-317,619` (I-011).
- **TARGET:** criterio 4 (durabilidad real); item 1 (ubicación canónica).
- **CONSEQUENCE:** Memory estándar depende de un directorio no versionado y no reconstruible; un clon o una pérdida de `.project/` produce contexto vacío **sin señal** (el read fail-closed devuelve `None` y `build_memory_context` lo salta en silencio). «Git-persisted» sigue siendo una declaración del contrato, no un hecho del repositorio.
- **CONFIDENCE:** 0.90.

### P-6 — Presupuesto e inyección: la memoria se agrega fuera de `context_budget`, y la frontera detecta, no previene

- **OBJECTION:** El contexto se anexa **después** de `render_prompt` y no se contabiliza contra el budget declarado. El contenido es JSON arbitrario de un directorio mutable; el frontier es memory-free (no concede autoridad) pero es posterior a la invocación: no impide que el actor obedezca instrucciones inyectadas dentro de su scope.
- **TYPE:** REAL (constantes observadas; riesgo del actor `INFERRED`).
- **EVIDENCE:** `OBSERVED` — `agent_worker.py:84` (`DEFAULT_CONTEXT_BUDGET = 8000`), `:427-430` (append posterior); `prompt_rendering.py:26-33,45` (el budget sólo se imprime, no se trunca); `fc_flow.py:53-56,71` (`limit=8`, `max_chars=400`). Cálculo sobre constantes: ~3,5–3,7k caracteres (~850–925 tokens estimados), sin contabilidad. `docs/plans/165...:278` (`ID-6`: la frontera no controla el interior) y `:265` (`FC-5`: detección).
- **TARGET:** criterio 4 (carga por delegación); criterio 3 (contexto ≠ autoridad).
- **CONSEQUENCE:** la memoria se vuelve un canal de instrucciones no contabilizado; `test_memory_cannot_authorize_an_effect` (`tests/test_fc_flow.py:98-117`) sólo prueba que el veredicto formal no cambia, no que el actor no actúe sobre el texto. `GAP`: no hay evidencia de comportamiento de un actor con memoria inyectada (`INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:270`).
- **CONFIDENCE:** 0.70.

### P-7 — El candidato invierte una propiedad que el repositorio ya verifica como contrato

- **OBJECTION:** La ausencia por defecto no es un descuido: está escrita como aserción verde y como criterio de no-op. C-MEM debe reescribir esa prueba; «reversible» cubre el código, no el contrato de test ni la postura documental.
- **TYPE:** REAL.
- **EVIDENCE:** `OBSERVED` — `tests/test_fc_host_integration.py:56-58` (`test_memory_is_absent_by_default_and_therefore_a_no_op`, `assert worker.memory_store is None`), `:48-53` (detector de wiring), `:41-42` (el detector sólo exige que el campo exista); `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:174` usa el default como evidencia de integración incompleta.
- **TARGET:** criterio 6 (reversibilidad); criterio 5 (costo); premisa de que no existe declaración de producto.
- **CONSEQUENCE:** el cambio no es aditivo: sustituye una garantía verificada por su opuesta. La reversibilidad declarada subestima el costo de test y de documentación.
- **CONFIDENCE:** 0.85.

### P-8 — `FC-3` ya está declarado materializado y verificado sin wiring por defecto: el candidato no cierra un gap registrado

- **OBJECTION:** El plan que define el criterio registra `FC-3` como materializado con el seam opcional; su falsación sólo exigía contexto presente y veredicto sin cambio. El wiring por defecto no es un criterio pendiente: es otra decisión de producto.
- **TYPE:** REAL.
- **EVIDENCE:** `OBSERVED` — `docs/plans/165...:359` (matriz: `FC-3` SÍ/SÍ/SÍ), `:420` (`memory_store` default `None` ⇒ no-op como forma integrada), `:263` (falsación), `:277` (`ID-4`); Plan 165 `Executed`/`Closed` (`docs/plans/INDEX.md:1347`); Plan 178 clasifica `PARTIALLY_INTEGRATED` y deja F-03 abierto (`docs/plans/INDEX.md:1208`; audit `:232-237`).
- **TARGET:** criterio 1 (necesidad); premisa de que el wiring cierra `FC-3`.
- **CONSEQUENCE:** presentar C-MEM como cierre de `FC-3` contradice el registro de verificación del propio plan. Lo abierto es el productor y la decisión de producto; el wiring es una preferencia, no una brecha demostrada.
- **CONFIDENCE:** 0.85.

### P-9 — La actualización de la evidencia de `AE-8` se presenta como documental, pero es una edición de gobernanza y su costo se subestima

- **OBJECTION:** `ADR-19` es un artefacto `Accepted` con `Amendment Log` propio (`CONVENTIONS:310-311,340`). La fila de evidencia de `AE-8` no es un comentario: registra el estado de la integración. Reemplazarla por «consumido por defecto» afirmaría una integración que el candidato declara condicional (item 6), mientras `--worker agent` sigue construyendo `NullAgentInvoker`. La edición corresponde al `Amendment Log`.
- **TYPE:** REAL.
- **EVIDENCE:** `OBSERVED` — `docs/adr/19...:88` (`AE-8`), `:156-165` (tabla de evidencia, fila `AE-8`), `:110-152` (`Amendment Log`); `docs/CONVENTIONS.md:310-311,340`; `agent_worker.py:427-430`; `__main__.py:184-188`.
- **TARGET:** criterio 3 (authority); item 3.
- **CONSEQUENCE:** o la fila nueva sobredeclara el consumo vacío como capacidad, o necesita una distinción explícita entre seam y producción; en ambos casos el cambio es de gobernanza. Llamarlo documental reduce el costo de autoridad percibido.
- **CONFIDENCE:** 0.75.

### P-10 — La declaración «capacidad estándar» no alcanza a ningún adoptante y su fuerza normativa es indemostrable

- **OBJECTION:** El candidato teme que la declaración adquiera fuerza normativa, pero `runtime/README.md` no se distribuye (el payload es `protocol/.agents/` + `AGENTS.md`); ni el beneficio ni el riesgo tienen evidencia de audiencia.
- **TYPE:** SPECULATIVE.
- **EVIDENCE:** `README.md:128` («DEV reference in `runtime/memory/` (not shipped)»); layout de `AGENTS.md` (dist publica el payload); `runtime/README.md:452-499` es documentación DEV. `GAP`: no hay evidencia de lectores ni de un consumidor que trate ese README como normativo; ningún test verifica sus afirmaciones.
- **TARGET:** criterio 3, en su pregunta sobre la fuerza normativa de la declaración.
- **CONSEQUENCE:** el item 4 sería costo sin efecto demostrado. No la pondero como apoyo a `OPPOSE` porque ambos lados carecen de ancla; la registro para no convertir una intuición en hecho.
- **CONFIDENCE:** 0.40.

## 3. Condiciones bajo las cuales el candidato sería viable

1. **Productor real antes que default.** Un camino de producción que escriba registros (`consolidation.publish` con una fuente semántica, no sólo tests) y una corrida que muestre recuperación útil. Sin eso, C-MEM sigue siendo un no-op declarado.
2. **Namespace decidido, no glob.** Subdirectorio designado conforme a `PC-48`, o filtro explícito por `kind`, para que `project_segment.json` no entre como memoria (P-3).
3. **Adaptador de schema o uso de retrieval.** Renderizar `statement`/`claim_id`/provenance de los registros conformes, o consumir `retrieval.eligible/retrieve`, en lugar del dump JSON (P-2, P-4).
4. **Durabilidad materializada.** `.project/knowledge/` versionado, o una declaración explícita de que Memory no es Git-persisted en DEV más una fuente de rebuild real (P-5).
5. **Presupuesto y política de inyección.** Contabilizar el contexto contra `context_budget`, truncar por registro y declarar el tratamiento de contenido no confiable (P-6).
6. **Entrada por opt-in.** Un flag `--memory` default off, como `--sae` (`__main__.py:122-131`); el audit acepta que «opt-in declarado no es integración parcial» (`:261`).
7. **Proceso de gobernanza.** Actualización de `ADR-19` por `Amendment Log`, y reescritura justificada del test de ausencia por defecto (P-7, P-9).

## 4. Alternativas superiores

- **A. Cerrar F-03 como «opcional por diseño»** (`INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:237`), la alternativa explícita del FRAME: cero código, cero deuda, decisión donde pertenece.
- **B. Opt-in declarado (`--memory`).** Precedente exacto del repo: `--sae` es off por defecto y su activación es explícita (`__main__.py:17-23,122-131`); el audit clasifica el opt-in declarado como integración suficiente para SAE (`:79`). Observabilidad real sin postura estándar.
- **C. Productor primero.** Conectar consolidation a una fuente semántica y reconstruir el store (`store.py:108-114`) antes de decidir el consumo; convierte la condicionalidad en evidencia.
- **D. Integrar en la capa de retrieval.** Usar `retrieval.eligible/retrieve` (`retrieval.py:22-38`) con un adaptador de render: respeta `I-008`/`I-014`/`I-025` y acota el budget.
- **E. No cambiar nada ahora.** El audit concluye valor **diagnóstico**, no fallo crítico (`:257`), y el Plan 178 registra `REPARACIONES EJECUTADAS = 0` (`:379`).

## 5. Compromiso

- **POSITION:** `OPPOSE`.
- **CONFIDENCE:** 0.85.
- **WHAT WOULD CHANGE MY POSITION:** (a) un productor con corrida real que demuestre mejora de contexto; (b) un renderer compatible con el schema de Memory y con la elegibilidad de retrieval; (c) un namespace designado y un tratamiento explícito de `project_segment.json`; (d) durabilidad materializada o declarada como no-Git con rebuild real; (e) contabilidad de budget y política de contenido no confiable; (f) actualización de `ADR-19` por `Amendment Log` y reescritura justificada del test de ausencia por defecto. Si el candidato se re-scopeara a opt-in con (a)–(c), abandonaría `OPPOSE` y evaluaría `OPPOSE_WITH_CONDITIONS`. Ninguna de estas condiciones se cumple en el HEAD `d61e327`.


## Apéndice F — SYNTHESIS_2 (verbatim)

# SYNTHESIS-2 — Case-02 (Memory como dependencia estándar del Execution Host)

## Metadata

- **Rol:** Synthesis, contexto `fresh` independiente. Resultado **advisory**: no autoriza cambios ni modifica el repositorio.
- **Hashes verificados** (`Get-FileHash -Algorithm SHA256`, 2026-10-25T13:57:23-03:00): frame `A64AE4ADBF1C550019A742F036FBA55AF797B926F87740EA5BAC80F359EBE0C2`; baseline `3BA05908330D170C8AAFD0DA5436E5B15C380657024A00F4C467C5258848AE8F`; defense `D46CE1EE75F2F7C704119A83B3A825D492B6FABDC2E90CF39B2B9A3B9F05F772`; prosecution `B2DB9375BB8045E4707FFD304A00DA5B2ED9D1FA56473D5F093841C182D4EBE5`. Los cuatro **coinciden** con los exigidos.
- **HEAD observado:** `d61e327` (`dev`). `git diff --stat e7bc881..d61e327` devuelve sólo el preregistro y `docs/working/research/INDEX.md`; la base de evidencia no cambia (`OBSERVED`).
- **STARTED:** 2026-10-25T13:57:23-03:00
- **FINISHED:** 2026-10-25T14:02:00-03:00
- **Archivos leídos (exacto):** `FRAME-2.md`; `BASELINE_2.md`; `DEFENSE_2.md`; `PROSECUTION_2.md`; `runtime/orchestrator/__main__.py`; `agent_worker.py`; `fc_flow.py`; `host.py`; `runtime/memory/store.py`; `retrieval.py`; `memory/__init__.py`; `runtime/toolcalls/project_store.py`; `prompt_rendering.py`; `runtime/placement/rules.py`; `tests/test_fc_host_integration.py`; `tools/check_memory_store.py`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/VERSIONING.md`; `docs/plans/165…md`; `README.md`; `runtime/README.md`; `.gitignore`. **No leídos:** auditoría (se cita vía las piezas), preregistro, Trial #1, otros trials, `PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`, cualquier otro archivo de `.project/campaign/`.
- **Llamadas a herramientas (aprox.):** 27 [SELF-DECLARED].

## 1. Criterion comparison (6 criterios)

### Criterio 1 — correctness / necesidad

- **Defense:** la ausencia de productor es condición, no premisa; C-MEM alinea la ruta con lo declarado y convierte F-03 en una prueba observable. “Opcional por diseño” no está establecido por ningún acto (`D-1`, `D-2`, `D-8`).
- **Prosecution:** estandariza el consumo de un store sin productor sobre una ruta sin actor (`--worker agent` ⇒ `NullAgentInvoker`); el Plan 165 ya registró `FC-3` materializado con el seam opcional, así que el wiring no cierra un gap registrado (`P-1`, `P-8`).
- **Evidencia compartida:** no hay `MemoryStore(` de producción (`git grep` = 0); `consolidation.publish` es el único `write` y sólo lo usan tests; `.project/knowledge` no existe; `--worker` default `command` (`__main__.py:100–108`); `--worker agent` ⇒ `AgentWorker()` con `NullAgentInvoker` (`:184–188`; `agent_worker.py:364`); Plan 165 `:359`, `:420`.
- **Estado:** `UNRESOLVED_DISAGREEMENT`.
- **Razón:** los hechos coinciden; el desacuerdo es evaluativo —si la falta de productor invalida declarar estándar el consumo o sólo condiciona su valor— y el acto de producto que lo resolvería no está en el repositorio (FRAME `:67`). Por provenance, `P-8` pesa más que `D-1`: el registro de verificación del Plan 165 es evidencia primaria, mientras `D-1` lee la prosa de `runtime/README.md:452–473` como si declarara suministro por defecto, y no lo hace. `D-2` refuta que el statu quo sea una decisión, pero es simétrico y no establece la afirmativa.

### Criterio 2 — integración

- **Defense:** el placement ya está resuelto (`.project/knowledge/`, Plan 150 `ADAPT`, `PC-48`); un punto único de construcción evita drift entre embedders (`D-4`, `D-7`). `L-4` concede que `_record_text` no habla el schema canónico, pero lo trata como limitación preexistente declarable.
- **Prosecution:** el renderer no reconoce `statement`/`description` y cae a JSON truncado (`P-2`); la base plana es donde se designa `project_segment.json` y `list_records` levanta todo `*.json` sin `kind` (`P-3`); el consumo crudo ignora `retrieval.eligible` y puede presentar registros no vigentes (`P-4`).
- **Evidencia compartida:** claves/fallback en `fc_flow.py:63–68`; campos por `kind` en `check_memory_store.py:26–33` (ninguno es `context/text/summary/note`); glob sin filtro en `store.py:98–106`; `project_store.py:3`; `retrieval.py:22–30`; `memory/__init__.py` no exporta retrieval; `check_memory_store.scan` usa `rglob("*.json")` y rechaza `unknown kind`.
- **Estado:** `PARTIAL_AGREEMENT`.
- **Razón:** hay acuerdo en la autoridad de placement y desacuerdo en la superficie. `P-2` y `P-4` son `OBSERVED` y no fueron rebatidos: `D-4` acredita dónde vive la base, no que el consumo sea correcto. `P-3` también es `OBSERVED`, pero su remedio (subdirectorio) choca con `PC-48` y con el resolver, que trata `.project/knowledge` como una sola familia (`runtime/placement/rules.py:240–242`); el remedio conforme es un filtro por `kind`/schema.

### Criterio 3 — authority

- **Defense:** `contain_actor_result` no acepta memoria por construcción; el veredicto sale de comandos y scope; `AE-8`/`ID-4` quedan intactos y la fila se actualiza por `Amendment Log` aditivo (`D-5`, `C-4`).
- **Prosecution:** la fila de `AE-8` no es un comentario: es una edición de gobernanza de un ADR `Accepted`; o sobredeclara el consumo vacío, o debe distinguir seam de producción (`P-9`).
- **Evidencia compartida:** `fc_flow.py:323–333`, `:381–393`; `tests/test_fc_host_integration.py:71–74`; `docs/adr/19…:165`; `Amendment Log` `:110–152`.
- **Estado:** `AGREEMENT`.
- **Razón:** ambos preservan la norma y aceptan el mismo mecanismo; `P-9` corrige la etiqueta del costo, no la conclusión. Dato no explotado por las piezas: en HEAD la fila de `AE-8` es **exacta** —ningún módulo de `runtime/orchestrator/` importa `runtime.memory`; sólo hay menciones en docstrings (`agent_worker.py:370`, `fc_flow.py:74`)—; la obsolescencia la crearía la adopción, no el estado actual (contradice al baseline, §6).

### Criterio 4 — maintainability

- **Defense:** consumidor read-only; lecturas fail-closed, registros corruptos salteados, render acotado (8×400) y `rebuild` determinista; vacío/corrupto/obsoleto degrada a contexto vacío o parcial sin error (`D-6`).
- **Prosecution:** sin filtro por lifecycle/epistemic (`P-4`); durabilidad Git no materializada y `rebuild(records)` exige los registros del llamador, sin fuente en DEV (`P-5`); la memoria se anexa tras `render_prompt` y no se contabiliza contra `context_budget` (`P-6`).
- **Evidencia compartida:** `store.py:81–114`; `.gitignore:13`; `git ls-files .project` = 0; `prompt_rendering.py:26–45` (el budget se imprime, no se trunca); `fc_flow.py:71` (`limit=8`, `max_chars=400`).
- **Estado:** `PARTIAL_AGREEMENT`.
- **Razón:** `D-6` es correcto pero incompleto: describe modos de falla, no responde por elegibilidad, persistencia ni presupuesto. `P-4`/`P-5`/`P-6` son `OBSERVED` en su núcleo; sólo el riesgo de que el actor obedezca texto inyectado es `INFERRED`. La defensa concede durabilidad (`L-2`) y renderer (`L-4`); el desacuerdo real es de atribución (GAP del contrato vs defecto del candidato) y severidad.

### Criterio 5 — cost

- **Defense:** 1 call site + 1 factory + 1 test + 2 documentos, sin migración (`D-3`).
- **Prosecution:** no es aditivo: cambia la semántica del test de ausencia y edita un ADR `Accepted`; la declaración no tiene audiencia demostrada (`P-7`, `P-9`, `P-10`).
- **Evidencia compartida:** `agent_worker.py:373` (default `None`); `test_fc_host_integration.py:56–58`; ADR-19 exige `Amendment Log`; `README.md:128` declara `runtime/memory/` “(not shipped)”.
- **Estado:** `PARTIAL_AGREEMENT`.
- **Razón:** el costo absoluto es bajo para ambos; discrepan en su composición. `P-7` acierta en el contrato semántico del test, pero no en que la aserción se rompa (criterio 6). `P-9` acierta en costear la enmienda del ADR. `P-10` se autodeclara `SPECULATIVE` y no se pondera. Costo bajo, no “≈ 0”: incluye un test que deja de proteger lo que su nombre declara.

### Criterio 6 — reversibility

- **Defense:** retirar el wiring restaura `AgentWorker().memory_store is None`, sin deuda ni migración (`D-3`).
- **Prosecution:** el cambio “sustituye una garantía verificada por su opuesta” y la reversibilidad subestima test y documentación (`P-7`).
- **Evidencia compartida:** default del dataclass (`agent_worker.py:373`); aserción (`test_fc_host_integration.py:56–58`); C-MEM pasaría el store en `__main__.py`, no en el constructor.
- **Estado:** `PARTIAL_AGREEMENT` (contradicción resuelta en parte).
- **Razón:** la reversibilidad de código se verifica: el default sigue `None` y la aserción sigue verde. La afirmación de `P-7` de que la prueba debe reescribirse es literalmente falsa. Lo que no se revierte con un call site es la semántica: el test deja de describir la ruta y las declaraciones de README/ADR permanecen. Reversibilidad alta, no total.

## 2. Las 9 preguntas de síntesis

**1. ¿Argumentos válidos?** Resisten, con evidencia `OBSERVED`: `D-3`, `D-4` (autoridad de placement, insuficiente para la superficie), `D-5`, `P-1`, `P-2`, `P-3`, `P-4`, `P-5`, `P-6` (su parte conductual es `INFERRED`), `P-8`, `P-9`. Parcialmente válidos: `D-1` (el gap documental es real, pero no prueba que la ruta deba suministrar el store), `D-2` (refuta el statu quo como decisión, no establece la afirmativa), `D-6` (correcto pero incompleto), `D-7` (presupone demanda), `D-8` (preferencia), `P-7` (acierta en semántica, yerra en la aserción). `P-10` no es apoyo válido.

**2. ¿Duplicados?** `D-2`/`D-8` (ambos responden al criterio 1 desde “no hay decisión”); `D-3`/`D-6` (misma evidencia de store acotado, fines distintos); `P-1`/`P-5` (store vacío ⇒ contexto vacío); `P-3`/`P-4` (misma causa —consumo crudo sin filtro—, ejes distintos: kind vs lifecycle); `D-7`/`D-1` (ausencia de punto canónico). `B-2`/`B-6` del baseline corresponden a `P-2`/`P-4`, y `B-5` a `P-6`.

**3. ¿Derivados?** `D-8`←`D-2`/`C-2`; `D-7`←`D-1`+`D-3`; `P-9`←`P-1` (sin consumo de producción, “consumido por defecto” sobredeclara); la parte conductual de `P-6`←`P-2`/`P-4`; la consecuencia de `D-1`←`D-4`. El baseline `B-7` derivaba de leer `fc_flow` como si consumiera `runtime.memory`; se retracta (§6).

**4. ¿Objeciones materiales?** Bloquean C-MEM literal: `P-1`, `P-2`, `P-3`, `P-4`. Afectan la forma pero no la dirección: `P-5`, `P-6`, `P-9`. `P-7` sólo en su parte semántica.

**5. ¿Espurias?** `P-10` (única `SPECULATIVE`, sin ancla); `D-8` es preferencia, no evidencia; la frase de `P-1` “el único delta es el hash del prompt” es imprecisa (con contexto vacío el prompt es idéntico, `fc_flow.py:91–95`); `D-7` presupone demanda no mostrada.

**6. ¿Contradicciones?** Reales: `D-3`/`P-7`, `D-1`/`P-8`, `D-4`/`P-3` (§3), más `B-7` contra el FRAME/repo. Falsas o aparentes: RFC-80 `NOT IMPLEMENTED` vs `11.7.0` (alcances distintos, ya reconciliados; FRAME `:65`); `D-5`/`P-9` (ambos aceptan `Amendment Log`; difieren en la etiqueta); `D-6`/`P-4` (`D-6` no afirma filtrado).

**7. ¿Incertidumbres?** F-03 sin acto de producto; sin corrida end-to-end con actor externo; sin productor ni registros canónicos; sin medición real de presupuesto; no se verificó si `project_segment.json` se escribe en DEV (la colisión es estructural, no activa); audiencia de `runtime/README.md` no demostrada.

**8. ¿Evidencia adicional?** Ver §8: corrida real con actor y registros, productor, medición de presupuesto, colisión activa. No se introduce evidencia nueva.

**9. ¿Qué cambió vs baseline?** Aquí hay veredicto (`NOT_VIABLE` sobre C-MEM literal) y `REVISE` sobre la dirección; se retracta `B-7`, se confirman `B-1`/`B-2`/`B-4`/`B-5`/`B-6`/`B-8` y se agregan R-3/R-5. Detalle en §6.

## 3. Contradicciones y desacuerdos preservados

### Contradicciones reales

**C-1 — `D-3` vs `P-7` (¿el test se rompe?).** `D-3` dice que las suites con `AgentWorker()` siguen pasando; `P-7`, que C-MEM debe reescribir el test de ausencia por defecto. Verificación: el test sólo afirma `AgentWorker().memory_store is None` (`tests/test_fc_host_integration.py:56–58`) y C-MEM suministra el store en `__main__.py`, no en el default (`agent_worker.py:373`). **Resuelta:** `D-3` correcto en la aserción; `P-7` correcto en que la prueba deja de proteger la propiedad de la ruta. El residuo (semántica del test) pasa a costo.

**C-2 — `D-1` vs `P-8` (¿qué declara el repo?).** `D-1` lee `runtime/README.md:454–473` como declaración de que Memory es paso del flujo estándar; `P-8` cita el Plan 165 (`:359`, `:420`), que registra `FC-3` materializado con default `None` y no-op como forma integrada. **Resuelta:** el repositorio declara el seam integrado, no el suministro por defecto; `P-8` tiene mayor provenance. `D-1` sobrevive sólo como gap documental: el README no muestra la guarda `if self.memory_store is not None` (`agent_worker.py:427`).

**C-3 — `D-4` vs `P-3` (placement resuelto ≠ consumo seguro).** `D-4` concluye que el cambio “se reduce a construcción y consumo”; `P-3` muestra que en la misma base se designa `project_segment.json` (`project_store.py:3`), que `list_records` levanta todo `*.json` sin `kind` (`store.py:98–106`) y que `check_memory_store.scan` rechaza ese JSON como `unknown kind` (`:62–64`, `:86–100`). **Resuelta en el hecho, abierta en el remedio:** la premisa de `D-4` es verdadera y su conclusión incompleta; la colisión es `OBSERVED` como riesgo estructural. El subdirectorio de `P-3` no es conforme; el filtro por `kind` sí. Persiste si el filtro basta para todos los kinds.

**C-4 — `B-7` vs FRAME/repositorio.** `B-7` afirma que la fila de `AE-8` “ya es inexacta”. Verificación: ningún módulo de `runtime/orchestrator/` importa `runtime.memory`; la fila (“`runtime/memory/` no se consume desde el orquestador”, ADR-19 `:165`) es **exacta** en HEAD, y el FRAME dice que C-MEM “la dejaría obsoleta” (`:63`). **Resuelta:** `B-7` se retracta; no hay Change docs-only previo.

### Desacuerdos preservados

**PD-1 — Necesidad (criterio 1).** Defense: la ausencia de productor condiciona, no invalida (`D-2`, `D-8`). Prosecution: declarar estándar un no-op es apariencia de capacidad (`P-1`, `P-8`). Evidencia: la misma. Razón: “¿debe ser estándar?” es decisión de producto ausente del repositorio; resolverla por inferencia violaría el FRAME.

**PD-2 — Namespace y remedio (criterio 2).** Defense: base plana ya autorizada (`D-4`). Prosecution: colisiona y el consumidor no filtra (`P-3`). Evidencia: `project_store.py:3`, `store.py:98–106`, `check_memory_store.py:86–100`, `placement/rules.py:240–242`. Razón: el defecto está establecido; si un filtro por `kind` basta —o si hace falta resolución de placement previa— no se decide sin un acto de placement.

**PD-3 — Atribución de la durabilidad (criterio 4).** Defense: el GAP es del contrato de placement; C-MEM sólo debe declararlo (`L-2`, `C-6`). Prosecution: una dependencia estándar sobre un directorio no versionado y sin fuente de rebuild es defecto del estándar (`P-5`). Evidencia: `.gitignore:13`, `git ls-files .project` = 0, `rebuild(records)`. Razón: ambos aciertan en su nivel; la atribución es una decisión de alcance que ninguna pieza puede imponer.

## 4. Verdict (VIABLE / NOT_VIABLE / UNDETERMINED) + BASIS

**VERDICT: `NOT_VIABLE` — para C-MEM tal como está especificado.** No es un veredicto sobre si Memory debe ser estándar u opcional: F-03 permanece abierta.

**BASIS:**

1. **La ruta nombrada no tiene actor.** `--worker` default `command`; `--worker agent` construye `AgentWorker()` con `NullAgentInvoker` (`__main__.py:100–108`, `:184–188`; `agent_worker.py:364`). El prompt se escribe como evidencia, pero no lo consume un actor: “dependencia estándar” sobre esa ruta es capacidad nominal (`P-1`; concedido por `L-3`).
2. **No hay productor ni registro preexistente.** Único `write`: `consolidation.publish`, sólo tests; `git grep "MemoryStore("` = 0; `.project/knowledge` no existe. Beneficio condicional, hoy no observable (`P-1`, `P-5`; `D-3`, `L-1`).
3. **El consumo estándar no entregaría el contenido canónico.** `_record_text` no reconoce `statement`/`description` y cae a JSON truncado (`P-2`); no se consulta lifecycle ni `retrieval.eligible` (`P-4`). Con registros reales, el “contexto” sería ruido u obsoleto.
4. **La base plana no está aislada.** `MemoryStore` levanta todo `*.json` de `.project/knowledge/`, donde ya se designa `project_segment.json`, y el validador de Memory lo rechaza (`P-3`).
5. **Lo preservado no alcanza.** `ID-4`/`AE-8` intactos (`D-5`), costo bajo (`D-3`) y placement autorizado (`D-4`) sostienen una dirección revisada, no la forma literal.
6. **La necesidad no está demostrada ni puede demostrarse con la evidencia admitida.** No hay acto de producto ni corrida con actor; `P-8` muestra que el wiring no era criterio pendiente de `FC-3`.

## 5. Recommendation (PROCEED / REVISE / GATHER_EVIDENCE)

**RECOMMENDATION: `REVISE`.**

**Qué cambió y por qué.** La dirección “Memory como contexto estándar del Host DEV” sigue siendo coherente con `ID-4`/`AE-8` y con `FC-3`; no resiste la forma: ruta sin actor, renderer incompatible, namespace compartido y elegibilidad ignorada. `PROCEED` literal produciría prompt más largo, ningún efecto observable y una declaración desmentida por el comportamiento (`P-1`, `P-2`, `P-3`, `P-4`). `GATHER_EVIDENCE` como decisión final no corresponde: hay evidencia para rechazar la forma; la que falta (actor, productor) no corrige defectos de implementación.

**Evidencia que lo justifica.** `P-1`–`P-4` son `OBSERVED` y reproducibles; `P-8` acredita el estado de `FC-3`; `D-5` que la frontera no se toca; `D-3`/`D-4` que la corrección es barata y el placement está autorizado.

**Condiciones (C-MEM′):**

- **R-1 — Punto único que alcance al actor.** Store en el punto compartido por CLI y embedding (factory o parámetro de `ExecutionHost.__init__`), no sólo en `__main__.py`; el embedding ya documenta `ExecutionHost(..., worker=AgentWorker(invoker=...))` (`__main__.py:185–187`; `runtime/README.md:399`).
- **R-2 — Schema y elegibilidad.** Renderizar `statement`/`description`/`summary` o consumir `retrieval.eligible`; excluir `stale`, `contradicted`, `superseded`, `retired`, `archived`, `candidate` (`P-2`, `P-4`).
- **R-3 — Namespace y filtro por `kind`.** Sin subdirectorio nuevo (PC-48); filtrar por `kind`/schema y declarar el tratamiento de `project_segment.json` (`P-3`).
- **R-4 — Declaración proporcional.** “Cableada al camino estándar, inerte mientras no exista productor”, no “capacidad estándar” a secas (`P-1`, `D-8`/`C-2`).
- **R-5 — Presupuesto y contenido no confiable.** Contabilizar o truncar contra `context_budget` y declarar el texto de Memory como dato no confiable (`P-6`).
- **R-6 — `AE-8` prospectiva.** Actualizar la fila por `Amendment Log` **sólo si** se adopta el wiring; en HEAD es exacta (`P-9`, `D-5`; retractación de `B-7`).

**Incertidumbre restante.** F-03, valor con actor real, productor y materialización Git de `.project/knowledge/` (PD-1, PD-3). Si R-1…R-5 no se aceptan, la alternativa preferible es **A3** (opcional por diseño, F-03 como aislamiento deliberado).

## 6. Cambios atribuibles vs baseline (con IDs)

- **Decisión/verdict:** el baseline no emitía veredicto; esta síntesis emite `NOT_VIABLE` para C-MEM literal y lo separa de F-03 (`P-1`, `P-2`, `P-3`, `P-4`; no se apoya en `P-10`).
- **Recommendation:** se mantiene `REVISE` (coincide con `BASELINE_2:§8`), pero cambia su contenido: se **retira** `R-4` del baseline (“corrección separada y previa de `AE-8`”) porque `B-7` no sobrevive. Se agregan R-3 (`P-3`) y R-5 (`P-6`); R-1 se refuerza con el embedding documentado; R-2 incorpora `P-4`.
- **Plan:** se elimina el paso “Change docs-only de corrección de `AE-8`”. Orden: (1) decisión de producto F-03; (2) resolución de placement/kind si R-3 no es trivial; (3) Change de wiring con R-1/R-2/R-4/R-5; (4) declaración y batería. `Change Level` sigue `GAP`.
- **Condiciones:** se agregan R-3 y R-5; R-4 pasa a R-6 prospectiva; R-1 se amplía al embedding; R-2 a lifecycle. Se conservan `C-1…C-7` de Defense en lo compatible (`D-4`, `D-5`, `D-6`) y se descartan `D-1`, `D-7`, `D-8` como fundamento.
- **Confirmados del baseline:** `B-1` (ruta sin actor; se agrava: default `command`), `B-2` (`P-2`), `B-4` (`P-5`), `B-5` (segundo canal: `build_context` deja `knowledge_entries=()` y la memoria se anexa tras el render, `agent_worker.py:396`, `:424–430`), `B-6` (`P-4`), `B-8` (no-autoridad estructural, no conductual).
- **ATTRITION:** `D-1` (la prosa no declara suministro por defecto), `D-4` como conclusión (“sólo construcción y consumo”), `D-7` (presupone demanda), `D-8` (preferencia), `P-7` en su literalidad, `P-10` (especulativo), la parte conductual de `P-6` (no verificable sin actor) y `B-7` del baseline.

## 7. Rebuttal recomendado (SI/NO) y por qué

**`REBUTTAL_RECOMMENDED: SI`.**

**Objeción material a resolver:** `P-1` — la única ruta nombrada por C-MEM (`python -m runtime.orchestrator --worker agent`) construye `AgentWorker()` con `NullAgentInvoker`, por lo que la “dependencia estándar” no alcanza a un actor y se declara sobre un no-op.

**Evidencia existente que bastaría (una):** el punto de composición ya existe y está documentado: `ExecutionHost.__init__` acepta `worker` (`host.py:408–423`) y el código declara que el embedding inyecta su invoker vía `ExecutionHost(..., worker=AgentWorker(invoker=...))` (`__main__.py:185–187`; `runtime/README.md:399`). Una factory única que construya `AgentWorker(invoker=..., memory_store=...)` y la usen CLI y embedder responde `P-1` sin evidencia nueva. Si C-MEM no puede cubrir ese punto, `P-1` queda confirmado. No se recomienda segunda ronda por `P-3`: su remedio ya se resolvió con evidencia existente (filtro por `kind`; `placement/rules.py:240–242`, `check_memory_store.py:26–33`).

## 8. Evidencia adicional necesaria / REQUIRES_NEW_EVIDENCE

- **`REQUIRES_NEW_EVIDENCE` — REQ-1 (necesidad/valor).** Corrida end-to-end con actor externo y al menos un registro canónico que muestre un cambio de decisión observable. No existe: `tests/test_fc_host_integration.py:8–9` es un detector de wiring, no una corrida (`P-1`, `L-1`).
- **`REQUIRES_NEW_EVIDENCE` — REQ-2 (productor).** Camino de producción que escriba registros (`consolidation.publish` con fuente semántica) o registros canónicos preexistentes. Hoy el único `write` lo consumen tests (`consolidation.py:92`; `git grep "MemoryStore("` = 0).
- **`REQUIRES_NEW_EVIDENCE` — REQ-3 (presupuesto).** Medición del prompt real con 8 registros canónicos (caracteres/tokens, efecto sobre `context_budget`), no el cálculo sobre constantes de `P-6`.
- **`REQUIRES_NEW_EVIDENCE` — REQ-4 (colisión activa).** Verificar si algún camino de DEV escribe `project_segment.json` en `.project/knowledge/`; en HEAD la base no existe y la colisión es estructural (`P-3`).

**No es evidencia, es decisión pendiente:** el acto de producto que resuelva F-03 (estándar vs opcional). Ninguna cantidad de evidencia lo sustituye; corresponde al mantenedor (`FRAME-2.md:67`; `P-8`, `D-2`).


## Apéndice G — REBUTTAL_2 (verbatim)

# REBUTTAL-2 — ¿P-1 cambia la evaluación?

## Metadata

- **Rol:** Rebuttal, contexto `fresh` independiente. Resultado **advisory**: no autoriza cambios ni modifica el repositorio.
- **Hashes verificados** (`Get-FileHash -Algorithm SHA256`, rama `dev`, HEAD `d61e327`): frame `A64AE4ADBF1C550019A742F036FBA55AF797B926F87740EA5BAC80F359EBE0C2`; baseline `3BA05908330D170C8AAFD0DA5436E5B15C380657024A00F4C467C5258848AE8F`; defense `D46CE1EE75F2F7C704119A83B3A825D492B6FABDC2E90CF39B2B9A3B9F05F772`; prosecution `B2DB9375BB8045E4707FFD304A00DA5B2ED9D1FA56473D5F093841C182D4EBE5`; synthesis `34737E508B1FC0DFD401A572F7A3853E1329A50BC234DED4D194CE5DBDB6644B`. **Los cinco coinciden** con los exigidos. `PROCECUTION_2.md` no existe; se verificó `PROSECUTION_2.md`.
- **STARTED:** 2026-10-25T14:04:25-03:00
- **FINISHED:** 2026-10-25T14:06:35-03:00
- **Archivos leídos (exacto):** `FRAME-2.md`; `BASELINE_2.md`; `DEFENSE_2.md`; `PROSECUTION_2.md`; `SYNTHESIS_2.md`; `runtime/orchestrator/__main__.py` (:95–200); `runtime/orchestrator/agent_worker.py` (:260–310, :344–356, :355–380, :420–435); `runtime/orchestrator/host.py` (:405–430); `runtime/orchestrator/fc_flow.py` (:45–100); `runtime/README.md` (:390–410); `tests/test_fc_host_integration.py` (:40–80); `docs/working/audits/DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md` (:1–45). Comandos: `Get-FileHash`, `git rev-parse`, `git grep`, `Get-Content`. **No leí** otros archivos de `.project/campaign/`, el preregistro, el Trial #1, `PRIORITY.md` ni los no versionados del FRAME. Un `git grep` devolvió líneas del preregistro (`docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md`): no lo abrí y no lo cito como evidencia.
- **Llamadas a herramientas (aprox.):** 15 [SELF-DECLARED].
- **Nota de IDs:** `R-n` aquí son *findings del rebuttal*; no deben confundirse con las **condiciones** `R-1`…`R-6` de `SYNTHESIS-2:§5`.

## 1. La objeción P-1 y qué afirma exactamente

`PROSECUTION-2:§P-1` empaqueta dos afirmaciones de distinto alcance:

- **P-1a (ruta/actor).** La única ruta que C-MEM nombra —CLI `python -m runtime.orchestrator --worker agent`— construye `AgentWorker()` con `NullAgentInvoker`; aun con registros, el prompt no llega a un actor. Verificado: `--worker` default `command` (`__main__.py:100–108`); `worker = AgentWorker()` (`:188`); `invoker: AgentInvoker = field(default_factory=NullAgentInvoker)` (`agent_worker.py:364`); `NullAgentInvoker.invoke` devuelve `INVOCATION_NOT_EXECUTED` sin transcript fabricado (`:296–307`). `OBSERVED`.
- **P-1b (no-op / apariencia).** Declarar «capacidad estándar» un consumo cuyo productor no tiene consumidor de producción convierte F-03 en una decisión tomada por apariencia. `OBSERVED` en su núcleo (FRAME `:62`, `:67`).

Qué **no** afirma P-1: no dice que el sistema carezca de camino con actor, ni que Memory no pueda cablearse a él. Su alcance preciso es la **propiedad 1 de C-MEM tal como está redactada**, que nombra sólo `__main__.py`. Imprecisión accesoria de P-1: «el único delta es el hash del prompt» es falso; con contexto vacío `with_memory_context` devuelve el prompt intacto (`fc_flow.py:91–95`): el delta es **cero**. No toca P-1b. `OBSERVED`.

## 2. Respuesta con evidencia existente

Aplico dos pruebas independientes.

**(A) Prueba de subsistencia: ¿el veredicto sobrevive sin P-1?** Sí. `SYNTHESIS-2:§4` apoya `NOT_VIABLE` en seis bases; el basis 1 es P-1, pero el 3 descansa en P-2/P-4 (renderer y elegibilidad) y el 4 en P-3 (namespace), ambos `OBSERVED` y no rebatidos —la defensa concede el renderer (`L-4`) y su propia `C-3` fuerza el punto único de construcción—, y el basis 6 en P-8 (Plan 165 `:359`, `:420`). Verifiqué P-2 en el código: `_record_text` sólo reconoce `context`/`text`/`summary`/`note` y cae a `json.dumps(...)[:400]` (`fc_flow.py:63–68`), con independencia de quién reciba el prompt. Retirar el basis 1 deja el veredicto en pie sobre 3, 4 y 6: **P-1 no es portante**.

**(B) Prueba de reparación: ¿P-1a se repara con evidencia existente?** Sí, y sin evidencia nueva. `ExecutionHost.__init__` recibe `worker` (`host.py:408–423`); `AgentWorker` es un `@dataclass` cuyos campos `invoker` y `memory_store` tienen default (`agent_worker.py:354`, `:364`, `:373`), así que `AgentWorker(invoker=..., memory_store=...)` es construible por keyword hoy; la forma de embedding está documentada dos veces (`runtime/README.md:392–399`; `__main__.py:185–187`); y CLI y embedder atraviesan el mismo tipo. Una factory única `build_worker(root)` usada por la CLI y documentada para embedders satisface P-1a sin evidencia nueva. La defensa ya la ofreció como `C-3` («Sin esto, el wiring cubre sólo la CLI con `NullAgentInvoker`», `DEFENSE-2:§3`) y la concedió en `L-3`. Matiz `OBSERVED`: `git grep "memory_store="` sobre `runtime/`, `tests/` y `tools/` no devuelve coincidencias: el camino por keyword existe por semántica del dataclass pero **no está ejercitado**; es cobertura, no viabilidad.

**(C) Qué no se repara.** P-1b sigue intacto y es independiente del actor: `build_memory_context` devuelve contexto vacío sobre una base vacía (`fc_flow.py:78–88`) y el único `write` de producción no existe (`PROSECUTION-2:§P-1`, `:§P-5`; FRAME `:62`). Cablear un actor a un store vacío sigue produciendo un no-op byte-idéntico. La parte **material** de P-1 —la que habla de necesidad— es P-1b, y ninguna evidencia existente la rebate.

**(D) Efecto contrario.** Resolver P-1a **endurece** P-2/P-4/P-6. Hoy el renderer defectuoso es inofensivo porque ningún actor lee el prompt; con un actor cableado, los blobs JSON truncados y los registros no elegibles alcanzan un consumidor real. El éxito del rebuttal de P-1 no mejora la posición de C-MEM: le quita el motivo por el que los demás defectos eran inertes.

## 3. ¿Cambia el VERDICT? (SI/NO + razón)

**NO.** Tres razones. (i) El veredicto se emite «para C-MEM **tal como está especificado**» (`SYNTHESIS-2:§4`): P-1a es un defecto de **especificación**, y su reparación produce C-MEM′, que no es el objeto del veredicto. (ii) El veredicto está **sobredeterminado**: sobrevive por sustitución al retiro del basis 1 (§2.A). (iii) `NOT_VIABLE` no decide F-03, y la reparación de P-1a responde a «quién recibe», no a «qué se entrega», que es el eje de las bases 3 y 4.

Preservo el desacuerdo: la acusación sostendría que el veredicto nunca necesitó P-1a y que la respuesta es trivialmente correcta; la defensa, que la refutación de P-1a demuestra que C-MEM es viable como **dirección** y que lo restante son defectos implementables —una tesis sobre `REVISE`, no sobre `NOT_VIABLE`—. Ambas lecturas conviven: lo que P-1 cambia es la **articulación de las bases**, no el resultado. Tratar la refutación de P-1 como suficiente para revisar el veredicto sería decidir por mayoría de uno.

## 4. ¿Cambia la RECOMMENDATION? (SI/NO + razón)

**NO.** `REVISE` ya contiene la reparación de P-1a como condición R-1 («Store en el punto compartido por CLI y embedding (factory o parámetro de `ExecutionHost.__init__`), no sólo en `__main__.py`») y la honestidad de P-1b como R-4 («cableada al camino estándar, inerte mientras no exista productor»). La recomendación **ya era la respuesta a P-1**. Lo que cambia es la justificación de R-1: deja de necesitarse «alcanzar al actor» (P-1a) y se sostiene por su motivo independiente —evitar drift entre embedders, núcleo superviviente de `D-7`—, de modo que R-1 no cae si P-1a se rebate. El orden de `SYNTHESIS-2:§6` tampoco cambia: la decisión de producto F-03 sigue primero porque P-1b está intacta, y `GATHER_EVIDENCE` sigue sin corresponder por la misma razón que antes.

Leer «P-1 resuelto ⇒ retirar R-1» sería un error. Una declaración conforme a P-1b debe nombrar **dónde** está cableada para ser verificable; suprimir R-1 reintroduciría la capacidad nominal que P-1b denuncia.

## 5. Findings nuevos (R-n) o REQUIRES_NEW_EVIDENCE

**R-1 — P-1 no es portante para `NOT_VIABLE`.**
`CLAIM`: el veredicto subsiste sin su basis 1; retirarlo no altera el resultado.
`EVIDENCE`: `SYNTHESIS-2:§4` bases 3, 4 y 6; `PROSECUTION-2` P-2, P-3, P-4, P-8 (`OBSERVED`); verificación propia de `fc_flow.py:63–68` y de que `runtime/orchestrator/` no importa `runtime.memory` —sólo docstrings en `agent_worker.py:370` y `fc_flow.py:74`—.
`CONSEQUENCE`: resolver P-1, aun favorablemente, no puede mover el veredicto. `SYNTHESIS-2:§7` eligió como objeto de rebuttal una objeción que no sostiene la decisión: una segunda ronda solo podría moverlo apuntando a P-2 o P-3.

**R-2 — P-1a es reparable; P-1b no.**
`CLAIM`: la parte «actor» es un defecto de redacción con remedio ya aceptado por ambas partes; la parte «no-op» es la material y permanece.
`EVIDENCE`: `host.py:408–423`; `agent_worker.py:354,364,373`; `runtime/README.md:392–399`; `__main__.py:185–187`; `git grep "memory_store="` = 0; `fc_flow.py:91–95`; FRAME `:62`, `:67`.
`CONSEQUENCE`: P-1 no habilita un pedido de evidencia nueva; habilita una enmienda de alcance (R-1/R-4 de `SYNTHESIS-2:§5`).

**R-3 — Resolver P-1 vuelve consecuentes los defectos hoy inertes.**
`CLAIM`: con actor cableado, P-2/P-4/P-6 dejan de ser inofensivos.
`EVIDENCE`: fallback JSON (`fc_flow.py:68`); elegibilidad no consultada (`PROSECUTION-2:§P-4`); `tests/test_fc_host_integration.py:48–53` es un detector de wiring, no una corrida.
`CONSEQUENCE`: el éxito del rebuttal de P-1 empeora la posición de C-MEM en los criterios 2 y 4. La conducta del actor frente al texto inyectado es `INFERRED`; el código es `OBSERVED`.

**`REQUIRES_NEW_EVIDENCE` — REQ-5 (embedder real en uso).** Para saber si la ruta con actor existe **en uso** —no sólo como API— hace falta evidencia ausente del repositorio: un embedder que construya `ExecutionHost(..., worker=AgentWorker(invoker=...))` en producción. El repositorio prueba la API y, **fuera de la base declarada de 15 ítems del FRAME**, registra un dogfood con invoker determinista inyectado que declara su límite (`docs/working/audits/DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md:23–45`: demuestra el ciclo, no razonamiento de un modelo). Lo registro en lugar de introducirlo en silencio; **ninguna conclusión de este rebuttal depende de él**, y el veredicto tampoco.

## 6. Compromiso (cambia/no cambia; confianza)

- **POSITION:** P-1 **no cambia** el VERDICT (`NOT_VIABLE` subsiste) ni la RECOMMENDATION (`REVISE`). **Cambia** su fundamento: P-1a (actor) sale de las bases y pasa a los defectos de forma que R-1 repara; P-1b (no-op sin productor) permanece como base material.
- **CONFIDENCE:** 0.85 en la no-portancia de P-1 (verificada por sustitución, no por ponderación); 0.70 en que la reparación de P-1a sea tan barata en la práctica como en la API, porque el camino por keyword no está ejercitado por ningún test.
- **WHAT WOULD CHANGE THIS:** (a) que P-2 o P-3 se refutaran con evidencia existente —entonces el veredicto pasaría a `UNDETERMINED` o a `REVISE` sobre C-MEM′, y P-1 sería material—; (b) un acto de producto sobre F-03, que cambia el marco, no este rebuttal; (c) que reparar P-1a exigiera un contrato nuevo CLI↔embedder: hoy no lo exige (mismo tipo, mismo constructor).


## Apéndice H — EVALUATION_2 (verbatim)

# EVALUATION-2 — clasificación y métricas

## Metadata

- **Rol:** Evaluation, contexto `fresh` independiente. Aplico la rúbrica congelada §8–§13. **No emito decisión de campaña** y **no leí el otro trial**.
- **Repositorio:** `dev`, HEAD `d61e327` (observado 2026-10-25T14:09:11-03:00). `git status --porcelain` = 2 untracked preexistentes del mantenedor, no leídos. El FRAME congela `e7bc881`; `git diff --stat e7bc881..d61e327` = 2 archivos de `docs/working/research/` (preregistro A, INDEX M), 746 inserciones: `runtime/`, `tests/`, `tools/` y el `docs/` sustantivo no cambian (verificado por mí).
- **Hashes verificados** (`Get-FileHash -Algorithm SHA256`): FRAME-2 `A64AE4AD…F359EBE0C2` ✓; BASELINE_2 `3BA05908…C5258848AE8F` ✓; DEFENSE_2 `D46CE1EE…B9A3B9F05F772` ✓; PROSECUTION_2 `B2DB9375…C182D4EBE5` ✓; SYNTHESIS_2 `34737E50…DBDB6644B` ✓; REBUTTAL_2 `4345A881…C23D4607AEFB` ✓. Los seis coinciden con los exigidos. Preregistro (fuente normativa, no exigido): `0E166E8F…33B8B37AE`.
- **STARTED:** 2026-10-25T14:09:07-03:00. **FINISHED:** 2026-10-25T14:16:39-03:00.
- **Archivos leídos (exacto):** los seis artefactos del trial; `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md` (§8–§18); `runtime/orchestrator/agent_worker.py`, `__main__.py`, `fc_flow.py`; `runtime/memory/store.py`, `retrieval.py`, `__init__.py`, `consolidation.py`; `runtime/toolcalls/project_store.py`, `prompt_rendering.py`; `runtime/placement/rules.py`; `tests/test_fc_host_integration.py`, `test_fc_flow.py`; `tools/check_memory_store.py`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/plans/165-f-c-autonomy-frontier-implementation.md`, `150-memory-system-implementation.md`, `INDEX.md`; `docs/placement-contract.md`; `docs/CONVENTIONS.md`; `docs/rfc/80-memory-system.md`; `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md`, `DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md`; `runtime/README.md`; `README.md`; `.gitignore`. Líneas exactas en §2/§3. Comandos: `git`, `Get-FileHash`, `Get-Content`, `Test-Path`; **no ejecuté `pytest`**.
- **Llamadas a herramientas:** 26 aprox. **[SELF-DECLARED]**, GAP.

## 1. Método de clasificación y deduplicación

**Referente de novedad.** Sólo `BASELINE_2.md`; la síntesis no se usa como referente (§8.3). Los errores del baseline (p. ej. `B-7`) se registran como `EVALUATOR_NOTE`, no reclasifican.

**Unidad atómica.** Separé **P-1 → P-1a/P-1b** (la acusación y el rebuttal §§1–2 las enuncian como «ruta/actor» y «no-op/apariencia»), **P-5 → P-5a/P-5b** (persistencia vs reconstrucción) y **P-6 → P-6a/P-6b** (presupuesto vs conducta). No separé D-3 (coste y reversión caen en la misma combinación), D-5, P-3 (una cadena causal: base compartida → glob sin filtro → JSON ajeno como memoria) ni P-9. Las separaciones dan 24 occurrences en vez de 21; la clase no cambia (§4.4).

**Desempate (§8.1).** Hecho y consecuencia material (mismo objeto + cambio especificado) en el baseline → `DUPLICATE`; hecho sí, consecuencia no → `DERIVED`; ninguno → `NEW`. Formulación, longitud, confianza declarada y soporte adicional no crean novedad. Una postura **opuesta** sobre el mismo hecho no es duplicado.

**Materialidad (§8.2/§9).** `MATERIAL` sólo con soporte verificable, consecuencia concreta con cambio especificado en un objeto de §9 y objeto identificado. Test operativo: consecuencia «nada cambia», preferencia normativa o hipótesis conductual sin medición → `NON_MATERIAL`. `SPURIOUS` es terminal y lo apliqué cuando la **evidencia mal leída sostiene la afirmación central**; las citas accesorias imprecisas se corrigen en §3 sin reclasificar.

**Deduplicación (distinct).** Criterio: **misma afirmación fáctica + misma consecuencia material** (mismo objeto y mismo cambio). Paráfrasis, distinto soporte o énfasis = mismo finding; no fusioné afirmaciones opuestas ni hallazgos con distinto objeto. Resultado: **sin duplicados cross-pass**: 24 occurrences = 24 distinct. No es supuesto: D-1/P-8, D-6/P-5, D-5/P-9 y D-3/P-7 se refutan entre sí, no se repiten. `DUPLICATE` se cuenta por la dimensión **novedad**, con independencia de la materialidad (matriz de 9 combinaciones, incluida `DUPLICATE+SPURIOUS`).

**Anclas.** Verifiqué en el HEAD, sólo lectura, cada finding `NEW`/`DERIVED`/`MATERIAL` (y los duplicados no triviales). `ANCHOR_VERIFIED: SI/NO/GAP` con corrección si el ancla es falsa. No modifiqué archivos versionados; mi única escritura es este archivo.

## 2. Tabla de findings

| ID | pass | claim corto | novelty | materiality | anchor | consequence | notas |
|---|---|---|---|---|---|---|---|
| D-1 | D | C-MEM alinea la ruta con lo que la documentación ya declara (FC-3 en `execute`); rechazarlo obliga a corregir la declaración igual | DUPLICATE | MATERIAL | SI: `runtime/README.md:454-473`; `__main__.py:188`; `agent_worker.py:427-430` | Cambio documental: si se rechaza, la declaración pasa a «capacidad de embedding» | Baseline §2 «Estado documental» + §8/A3: mismo hecho (README describe FC-3; ningún camino suministra store) y consecuencia («el statu quo… deja el renderizado como código de producción sin consumidor»). El README describe la estructura de `execute`, no un suministro por defecto |
| D-2 | D | «Opcional por diseño» no está establecido: F-03 es decisión pendiente; la evidencia es permisiva | DUPLICATE | NON_MATERIAL | SI: auditoría `:178-180`, `:232-237` | Preferencia por resolver F-03 con cambio observable; sin condición nueva | Baseline GAP 1 («no existe declaración de producto… F-03 sigue abierto») y A0. La afirmativa («con C-MEM F-03 se cierra») es tesis normativa sin ancla: la decisión está reservada (FRAME `:67`) |
| D-3 | D | Coste marginal y reversión ≈ 0 (1 call site + factory + test + 2 docs) | DUPLICATE | MATERIAL | SI: `store.py:71-72,81-106`; `agent_worker.py:373`; `test_fc_host_integration.py:56-58` | Fija el coste del plan (criterios 5/6) | Baseline A1: «Coste bajo y reversible». Los detalles (no crea directorios, fail-closed, suites verdes) son soporte, no consecuencia nueva |
| D-4 | D | Placement resuelto: base plana `.project/knowledge/` (ADAPT del Plan 150, PC-48), sin subdirectorio ni familia nueva | DERIVED | MATERIAL | SI: `placement-contract.md:131,303,315`; `plans/150:74`; `check_memory_store.py:86-100`; `placement/rules.py:240-242` | Restringe alcance: no hay decisión de placement y prohíbe subdirectorio | Premisas: baseline S-2 y §2 «Placement»; inferencia: el placement no añade trabajo ni bloqueo ⇒ «el cambio se reduce a construcción y consumo». El baseline lo tenía como supuesto, no como conclusión |
| D-5 | D | La no-autoridad es estructural; AE-8/ID-4 intactos y sólo cambia su fila de evidencia (Amendment Log aditivo) | DUPLICATE | MATERIAL | SI: `fc_flow.py:323-333,381-393`; `adr/19:88,110-152,165`. Caveat: `test_fc_flow.py:98-117` no prueba conducta | Confirma que authority no cambia y la edición es aditiva | Baseline B-7+B-8: mismo hecho (frontera memory-free; evidencia estructural, no conductual) y consecuencia (sólo la fila de evidencia cambia). El test llama `contain_actor_result` **sin** memoria |
| D-6 | D | Sin obligación nueva de ownership: consumidor read-only, fail-closed, `rebuild` determinista, render 8×400 | DERIVED | MATERIAL | SI: `store.py:20-23,66-92,98-113` | Fallas declaradas (vacío/corrupto/obsoleto ⇒ contexto vacío o parcial, sin error); coste = un call site | Premisas: baseline §2 «Durabilidad» (`list_records` ⇒ `[]`), B-4 y §3; inferencia: un lector no adquiere ownership y toda falla degrada a contexto vacío. No responde elegibilidad, persistencia ni presupuesto |
| D-7 | D | La alternativa multiplica puntos de construcción (N wirings con drift) y deja la conducta sin verificación | DUPLICATE | **SPURIOUS** | **NO**: `git grep "AgentWorker("` = un constructor de producción (`__main__.py:188`) + menciones documentales (`runtime/README.md:399`, `__main__.py:187`) + ~40 líneas de tests; `agent_worker.py:269-276` es el Protocol `AgentInvoker`; `git grep "memory_store="` = 0 | Sin consecuencia admisible: el hecho citado está mal leído | Baseline R-1 ya contiene la condición (punto compartido CLI↔embedding). «N embedders» presupone demanda no evidenciada (auditoría `:270`) |
| D-8 | D | La «apariencia de capacidad» se neutraliza declarando la condición (props. 4 y 6) | DUPLICATE | NON_MATERIAL | SI: FRAME `:24,:26`; `runtime/README.md:467-473` | Preferencia por declaración condicionada; sin cambio distinto | Baseline B-3 + R-3: mismo hecho (declarar estándar un no-op) y consecuencia («declaración proporcional al comportamiento»). Preferencia de redacción (§9) |
| P-1a | P | La ruta que C-MEM nombra construye `AgentWorker()` sin actor (`NullAgentInvoker`) | DUPLICATE | MATERIAL | SI: `__main__.py:100-108,184-188`; `agent_worker.py:364` | «Estándar» sobre ruta sin actor = capacidad nominal | Baseline B-1: mismo hecho y consecuencia («la capacidad declarada estándar no la consume ningún actor») |
| P-1b | P | Declarar estándar el consumo de un store sin productor convierte F-03 en decisión por apariencia | DUPLICATE | MATERIAL | SI: `consolidation.py:92`; grep `MemoryStore(` = 0; FRAME `:62,:67` | Bloquea la declaración de necesidad (criterio 1) | Baseline B-3: mismo hecho (único `write`, sólo tests) y consecuencia. Corrección: «el único delta es el hash del prompt» es falso; con contexto vacío el prompt es idéntico (`fc_flow.py:91-95`) |
| P-2 | P | `_record_text` no reconoce `statement`/`description`; un registro canónico cae a JSON truncado | DUPLICATE | MATERIAL | SI: `fc_flow.py:63-68,82-88`; `check_memory_store.py:24-33,62-64`; `test_fc_flow.py:70` | Ruido JSON en cada prompt; el test FC-3 valida una forma que el contrato rechaza | Baseline B-2: mismo hecho y consecuencia («JSON truncado… ruido que aumenta el coste de contexto sin información») |
| P-3 | P | La base plana colisiona con `project_segment.json` y `list_records` no filtra por `kind` | **NEW** | MATERIAL | SI: `project_store.py:3`; `store.py:98-106`; `check_memory_store.py:62-64,86-100`; `placement-contract.md:131`; `placement/rules.py:240-242` | Exige filtro por `kind`/schema o resolver namespace; validadores incompatibles | Evidencia ausente del baseline: no menciona `project_segment.json`, ni la ausencia de filtro por `kind`, ni la convivencia de validadores (sólo B-2, sobre el renderer). Colisión estructural, no activa (GAP) |
| P-4 | P | El consumo crudo ignora `retrieval.eligible`: `superseded`/`retired`/`contradicted`/`candidate` entran al prompt | DUPLICATE | MATERIAL | SI: `retrieval.py:7-9,22-30`; `fc_flow.py:71-88`; `memory/__init__.py:10-12` | Contexto obsoleto presentado como vigente: premisa de facto sin autoridad | Baseline B-6: mismo hecho («sin consultar lifecycle, epistemic state ni `retrieval.eligible`», `retrieval.py:22`) y consecuencia |
| P-5a | P | La durabilidad declarada no está materializada: `.project/` gitignored, 0 archivos versionados | DUPLICATE | MATERIAL | SI: `.gitignore:13`; `git ls-files .project` = 0; `placement-contract.md:131,351-372` | Base que Git no persiste: pérdida invisible a CI y a otros clones | Baseline B-4: mismo hecho y consecuencia (drift y pérdida silenciosa) |
| P-5b | P | `rebuild(records)` exige los registros del llamador: no hay fuente semántica de rebuild en DEV | **NEW** | MATERIAL | SI: `store.py:17-23,108-114`; `consolidation.py:77-93`; `rfc/80:315-319` | Store no reconstruible sin fuente externa: requisito de durabilidad/rebuild | Evidencia ausente del baseline: no menciona `rebuild` ni su firma (sólo `list_records` y `ls-files`). Solapa con B-4 en la pérdida; el hecho es nuevo |
| P-6a | P | La memoria se anexa tras `render_prompt` y no se contabiliza contra `context_budget` | **NEW** | MATERIAL | SI: `agent_worker.py:84,424-430`; `prompt_rendering.py:26-45`; `fc_flow.py:71` | Presupuesto no contabilizado (~3,5–3,7k caracteres por delegación): exigir contabilidad o truncamiento | Evidencia ausente del baseline: no menciona `context_budget` ni el orden render→append (B-5 describe el segundo canal, sin presupuesto). Cálculo sobre constantes (REQ-3) |
| P-6b | P | La frontera es posterior a la invocación: detecta, no previene; el actor podría obedecer texto inyectado | DERIVED | NON_MATERIAL | SI en código (`fc_flow.py:52-57`; `agent_worker.py:427-430`); GAP en conducta (`:270`) | Sin cambio verificable: riesgo conductual `INFERRED` | Premisas: B-8 (no-autoridad estructural, no conductual) + `ID-6`/`FC-5`; inferencia: el texto puede influir en el actor sin alterar el veredicto. Conducta no medible (§9) |
| P-7 | P | C-MEM invierte una propiedad verificada: el test de ausencia deja de proteger la ruta; la reversibilidad subestima test y documentación | DERIVED | MATERIAL | SI: `test_fc_host_integration.py:41-42,56-58`. NO en la predicción «debe reescribir la prueba» | Criterio de verificación: el test deja de describir la ruta por defecto aunque siga verde | Premisas: baseline §2 (el test afirma `memory_store is None`) y A1; inferencia: el cambio no es aditivo en semántica de test. La literalidad («sustituye la garantía por su opuesta») es falsa; sobrevive la deriva semántica |
| P-8 | P | `FC-3` ya figura materializado y verificado sin wiring por defecto; el wiring no era criterio pendiente | **NEW** | MATERIAL | SI: `plans/165:263,359,420`; `plans/INDEX:1208,1347`. Matiz: el row dice `Executed`, no «Closed» | Contradice la premisa de necesidad: lo abierto es productor y decisión de producto | Evidencia ausente del baseline: cita Plan 165 (`ID-4`) y `INDEX:1202-1204`, pero no la matriz `FC-3` SÍ/SÍ/SÍ, ni `:420` (default `None` = no-op integrado), ni la falsación `:263`, ni el estado del Plan 165 |
| P-9 | P | La actualización de la fila `AE-8` es edición de gobernanza (ADR `Accepted` + `Amendment Log`), no documental; coste de autoridad subestimado | DERIVED | MATERIAL | SI: `adr/19:110-152,156-165`; `CONVENTIONS:310-311,340`. La premisa de B-7 (fila inexacta) es falsa: la fila es exacta | Objeto authority: la edición debe clasificarse y registrarse como enmienda | Premisas: baseline B-7/R-4 (la fila se actualiza) + ADR-19 `Accepted` con `Amendment Log` + CONVENTIONS; inferencia: no es un Change docs-only, es enmienda con coste |
| P-10 | P | `runtime/README.md` no se distribuye: ni beneficio ni fuerza normativa tienen audiencia demostrada | **NEW** | NON_MATERIAL | SI: `README.md:128` («not shipped»). GAP en audiencia | Sin consecuencia concreta: la acusación no la pondera | Evidencia ausente del baseline: no menciona distribución del README ni audiencia. `SPECULATIVE` declarado, sin consecuencia especificada |
| R-1 | R | P-1 no es portante: el veredicto `NOT_VIABLE` subsiste sin su base 1 | **NEW** | NON_MATERIAL | SI (síntesis §4 bases 3/4/6; `fc_flow.py:63-68`) | Consecuencia = «no cambia»: sólo robustez | Evidencia ausente del baseline: no emite veredicto, no puede contener la no-portancia. No cumple §9 |
| R-2 | R | P-1a es reparable con evidencia existente (factory única); P-1b no | DERIVED | MATERIAL | SI: `host.py:408-423` (vía cita; no leído en crudo), `agent_worker.py:354,364,373`, `runtime/README.md:392-399`; `git grep "memory_store="` = 0 | Enmienda de alcance: conservar R-1/R-4 con justificación independiente (evitar drift) | Premisas: baseline S-1 (camino con actor = embedding) y R-1 (punto compartido); inferencia: la parte «actor» es defecto de redacción reparable; la «no-op» es material |
| R-3 | R | Resolver P-1 vuelve consecuentes los defectos hoy inertes (P-2/P-4/P-6) | DERIVED | NON_MATERIAL | SI: `fc_flow.py:68`; `test_fc_host_integration.py:48-53` | Eleva severidad de riesgos existentes; sin condición nueva | Premisas: baseline B-1/§3 (defectos inertes sin actor) + B-2/B-6; inferencia: con actor, renderer y elegibilidad alcanzan un consumidor real |

## 3. Anclas no verificadas / falsas

1. **D-7 — NO.** «`git grep "AgentWorker("` muestra dos puntos de construcción» es falso: hay **un** constructor de producción (`__main__.py:188`), dos menciones documentales (`runtime/README.md:399`, `__main__.py:187`), un comentario de módulo (`__main__.py:32`) y ~40 líneas de tests; `agent_worker.py:269-276` define el Protocol `AgentInvoker`; `git grep "memory_store="` = 0. El hecho de que baseline R-1 ya exige punto único se mantiene: `DUPLICATE` con ancla falsa. Apliqué `SPURIOUS` porque el ancla mal leída sostiene la afirmación central.
2. **P-1 — ancla accesoria falsa.** «El único delta es el hash del prompt» es incorrecto: con contexto vacío el prompt es idéntico (`fc_flow.py:91-95`); el delta es cero. Corregido, no reclasificado: P-1a/P-1b siguen verificados.
3. **P-7 — predicción falsa.** «Debe reescribir la prueba» es falso: la aserción `AgentWorker().memory_store is None` sigue verde porque el suministro ocurre en `__main__.py`, no en el default (`agent_worker.py:373`). Sobrevive la deriva semántica; no la declaré `SPURIOUS`.
4. **D-5 — over-read.** `tests/test_fc_flow.py:98-117` construye el prompt con un registro hostil y llama `contain_actor_result` **sin** memoria: prueba ausencia estructural del parámetro, no que un registro hostil no cambie el veredicto bajo store suministrado. La conclusión (AE-8/ID-4 intactos) sigue verificada por `contains_memory_parameter` (`fc_flow.py:381-393`).
5. **P-9 — premisa de B-7 falsa.** La fila `AE-8` es **exacta** en HEAD: ningún módulo de `runtime/orchestrator/` importa `runtime.memory` (`git grep` sólo devuelve docstrings en `agent_worker.py:370` y `fc_flow.py:74`). No invalida P-9 (coste de gobernanza de una edición **prospectiva**), pero sí la urgencia de B-7.

**GAP de ancla:** (a) P-3: colisión estructural — `.project/knowledge` no existe (`Test-Path` = False), `git ls-files .project` = 0, sin evidencia de escritura activa de `project_segment.json`; (b) P-6a: tamaño calculado sobre constantes (`limit=8`, `max_chars=400`), no medido; (c) R-2: `git grep "memory_store="` = 0, la ruta por keyword es viable por dataclass pero no está ejercitada; (d) P-10: audiencia no medible; (e) R-2 cita `host.py:408-423`, no leído en crudo (consistente con `__main__.py:185-187` y `runtime/README.md:392-399`, verificados).

**Contexto (no finding):** el FRAME congela `e7bc881` y la ejecución ocurrió en `d61e327`; el diff son 2 archivos de `docs/working/research/`, sin cambios en `runtime/`, `tests/`, `tools/` ni `docs/` sustantivo (§7, D-a).

## 4. Conteos y shares

**4.1 Costes (§11).** `TREATMENT_SELF_S` = 422+326+277+130 = **1155** ✓ (excluye baseline). `TREATMENT_LEAD_WALL_S` = 498+345+324+130 = **1297** ✓. `RATIO_SELF` = 1155/288 = **4,0104** → 4,01 ✓. `RATIO_LEAD` = 1297/416 = **3,1178** → 3,12 ✓. `EFFECTIVE` = mayor = **4,01** ✓. `COSTLY` = 4,01 > 3,0 → **SI** ✓. **Discrepancia:** `BASELINE_2` declara `LEAD_WALL_S` = 416 s, pero sus timestamps dan 13:33:44 → 13:38:35 = **291 s** (`SELF_S` = 288, 13:33:47 → 13:38:35, consistente). Con 291, `RATIO_LEAD` = 1297/291 = **4,457** y `EFFECTIVE` = **4,46**: `COSTLY` sigue SI y la clase no cambia, pero el ratio reportado (4,01) sólo es el conservador si se acepta 416. Las otras cuatro pasadas cuadran (422, 326, 277, 130). No resuelvo cuál cifra es la medida (no leí el ledger): GAP en §7. `WALL_CLOCK_RATIO` descriptivo: 13:37:18 → 14:02:00 = 1.482 s; /291 = **5,09**. Palabras: tratamiento = 2275+2277+2994+1481 = **9027** ✓; `WORDS_RATIO` = 9027/2198 = **4,1069** → 4,11 ✓ (incluir baseline daría 11.225 y 5,11: no es §11). Caracteres: baseline 17.521; tratamiento 68.825. Llamadas: `[SELF-DECLARED]`, GAP. Tokens/contexto: GAP. Iteraciones: 5 artefactos (1+4), exacto.

**4.2 Findings.** `TOTAL (occurrences)` = **24** = 8 D + 13 P (tras separar P-1, P-5, P-6) + 3 R. `DISTINCT` = **24**. Novedad: `NEW` = **6** (P-3, P-5b, P-6a, P-8, P-10, R-1); `DERIVED` = **7** (D-4, D-6, P-6b, P-7, P-9, R-2, R-3); `DUPLICATE` = **11** (D-1, D-2, D-3, D-5, D-7, D-8, P-1a, P-1b, P-2, P-4, P-5a). Materialidad: `MATERIAL` = **17**; `NON_MATERIAL` = **6** (D-2, D-8, P-6b, P-10, R-1, R-3); `SPURIOUS` = **1** (D-7). Combinaciones: `NEW+MATERIAL` = **4** (P-3, P-5b, P-6a, P-8); `DERIVED+MATERIAL` = **5** (D-4, D-6, P-7, P-9, R-2); `DUPLICATE+MATERIAL` = **8** (D-1, D-3, D-5, P-1a, P-1b, P-2, P-4, P-5a). `DISTINCT_MATERIAL_NEW` = **9**. Por pasada: Defense **2** (D-4, D-6); Prosecution **6** (P-3, P-5b, P-6a, P-7, P-8, P-9); Rebuttal **1** (R-2).

**4.3 Shares.** `DUPLICATE_SHARE` = 11/24 = **0,4583**; `SPURIOUS_SHARE` = 1/24 = **0,0417**; sobre occurrences, idénticas. `REDUNDANT` (>0,50) = **NO**; `VERY_REDUNDANT` (≥0,75) = **NO**; `SPURIOUS_HIGH` (>0,15) = **NO**; `>0,10` = **NO**.

**4.4 Sensibilidad.** (i) Sin separar: 21 occurrences, `DUP_SHARE` = 10/21 = 0,476, `SPUR_SHARE` = 0,048, `DMN` = 7; clase igual. (ii) D-7 como `DUPLICATE+MATERIAL`: `MATERIAL` 18, `SPURIOUS` 0, `DMN` = 9, shares 0,458/0; clase igual. (iii) P-7 `NON_MATERIAL`: `DMN` = 8; clase igual. (iv) Con 291 s: `EFFECTIVE` 4,46; clase igual.

**4.5 Eficiencia.** `DMN` por 1.000 s: 9/1.297 = **6,94** (LEAD), 9/1.155 = **7,79** (SELF). `NEW` por 1.000 s: 6/1.297 = **4,63**. Impactos decisionales atribuibles por 1.000 s: **0**.

## 5. Impacto y atribución

**Baseline:** sin veredicto; `REVISE`; condiciones R-1…R-4; plan de 5 pasos (paso 2 = corrección docs-only de `AE-8`). **Síntesis:** veredicto `NOT_VIABLE` (C-MEM literal); `REVISE`; R-1…R-6 (retira R-4, agrega R-3/R-5, R-4 → R-6 prospectiva); plan de 4 pasos (sin paso `AE-8`); `REQ-1…REQ-4`.

| Cambio | ¿Cita IDs? | Cadena | Contrafactual §10 | Clase |
|---|---|---|---|---|
| Veredicto `NOT_VIABLE` (nuevo) | Sí: `P-1`, `P-2`, `P-3`, `P-4`; bases 5/6 citan `D-5`, `D-3`, `D-4`, `P-8` | Verificada para `P-3`/`P-8`; `P-1`, `P-2`, `P-4` son `DUPLICATE+MATERIAL` | **Falla**: retirar `P-3` y/o `P-8` deja bases 2, 3 y 5 (P-1b/P-2/P-4) ⇒ no depende de un `NEW`/`DERIVED` | **REWEIGHTING** (strict §10 = **NO ATRIBUIDO**; no cuenta para H3) |
| Retiro del paso «Change docs-only de `AE-8`» | No cita IDs de tratamiento: retractación de `B-7` (verificación propia C-4) | Verifiqué la exactitud de la fila | Sin el retiro, el paso vuelve | **NO ATRIBUIDO** |
| Agrega **R-3** (namespace + `kind`) y paso 2 del plan | Sí: `P-3` (R-3; §6 «se agregan R-3 (`P-3`)») | Verificada: `P-3` → R-3 → orden | Sin `P-3` no hay condición de namespace ni paso de placement | **PLAN_IMPACT** |
| Agrega **R-5** (presupuesto + contenido no confiable) | Sí: `P-6` | Verificada: `P-6a` → R-5 (`P-6b` no material) | Sin `P-6a` no hay condición de budget | **PLAN_IMPACT** |
| **R-6** (`AE-8` sólo si se adopta) | Sí: `P-9`, `D-5` | Parcial: `P-9` aporta coste de gobernanza; `D-5` (duplicado) el mecanismo | Falla: sin `P-9`, `D-5` sostiene `Amendment Log` | **NO ATRIBUIDO** |
| Refuerzo de **R-1** con embedding documentado | Sí: `D-1` | Verificada, pero `D-1` es `DUPLICATE` | Sin `D-1`, R-1 ya existía | **NO ATRIBUIDO** |
| **R-2** + lifecycle y **R-4** proporcional | Sí: `P-4`, `P-1`, `D-8` | Verificada, pero los tres son `DUPLICATE` | Las condiciones del baseline cubren lo mismo | **NO ATRIBUIDO** |
| `REQ-3` (medir presupuesto real) | Sí: `P-6` | Verificada | Sin `P-6a`, no hay requisito | **EVIDENCE_IMPACT** |
| `REQ-4` (colisión activa) | Sí: `P-3` | Verificada | Sin `P-3`, no hay requisito | **EVIDENCE_IMPACT** |

**Recuento:** `DECISIONAL_IMPACT` = **0**; `PLAN_IMPACT` = **2** (`P-3`, `P-6a`); `EVIDENCE_IMPACT` = **2**; `DECISION_IMPACT` (H3) = **1**; `REWEIGHTING` = **1** (veredicto); `NO ATRIBUIDO` = **4** (retiro `AE-8`, R-6, refuerzo R-1, R-2/R-4 re-citados). El veredicto es **sobredeterminado**: sobrevive al retiro de cada finding `NEW`/`DERIVED` material porque las bases 2, 3 y 5 se apoyan en `DUPLICATE+MATERIAL`. La recomendación no cambia (`REVISE` → `REVISE`); los cambios de contenido son de plan y sólo dos son atribuibles.

## 6. VALUE_CLASS y clase del trial (§13.2)

Flags: `DISTINCT_MATERIAL_NEW` = **9** (≥1); `DECISIONAL_IMPACT` = **0**; `PLAN_IMPACT` = **2**; `EVIDENCE_IMPACT` = **2**; `COSTLY` = **SI** (4,01 > 3,0); `DUPLICATE_SHARE` = **0,4583**; `SPURIOUS_SHARE` = **0,0417**; `VERY_REDUNDANT` = **NO**; `SPURIOUS_HIGH` = **NO**.

`VALUE_CLASS`: no `NONE` (9 ≥ 1); no `DECISION` (`DECISIONAL_IMPACT` = 0); **`PLAN`** (`PLAN_IMPACT` ≥ 1, `DECISIONAL_IMPACT` = 0).

Orden de §13.2, primera que se cumple:
1. `INVALID_TRIAL` — **no**: hashes coincidentes, sin reescritura post-hash, sin contaminación detectada, deriva de HEAD docs-only. Sin D3 identificado.
2. `NEGATIVE` — **no**: `VERY_REDUNDANT` = NO; `VALUE_CLASS` ≠ `NONE`; ningún finding material verificado como falso en dirección errónea (D-7 es `SPURIOUS`, no material).
3. `SUCCESS_STRONG` — **no**: `VALUE_CLASS` ≠ `DECISION`.
4. `SUCCESS_PARTIAL` — **no**: `PLAN` ✓, `DUP` ≤ 0,60 ✓, `SPURIOUS` ≤ 0,10 ✓, pero **`COSTLY` = SI** ⇒ falla `¬COSTLY`.
5. `SUCCESS_EVIDENCE` — **no**: `VALUE_CLASS` ≠ `EVIDENCE`.
6. `NO_EVIDENCE` — **no**: `VALUE_CLASS` ≠ `NONE`.
7. **`POSITIVE_BUT_COSTLY`** — **sí**: `VALUE_CLASS` ∈ {EVIDENCE, PLAN, DECISION} ∧ `COSTLY`.

**Clase del trial propuesta: `POSITIVE_BUT_COSTLY`.**

**Ambigüedades declaradas:** (a) `BASELINE_2.LEAD_WALL_S` 416 vs 291 → ratio efectivo 4,01 vs 4,46; `COSTLY` y clase no cambian; (b) D-7 `SPURIOUS` vs `DUPLICATE+MATERIAL` no altera `DUPLICATE_SHARE` (0,458) ni la clase; (c) si el veredicto se atribuyera (`DECISIONAL_IMPACT` = 1), `VALUE_CLASS` = `DECISION` y la clase seguiría `POSITIVE_BUT_COSTLY` porque `COSTLY` bloquea `SUCCESS_*`; (d) las separaciones mueven ±3 occurrences y ~0,02 en shares, sin efecto en la clase; (e) la frontera `MATERIAL`/`NON_MATERIAL` de R-2, D-4, D-6 y D-8 es delgada.

## 7. GAP, desviaciones y notas del evaluador

**GAP.** (1) Tokens/contexto: estructural. (2) Llamadas: `[SELF-DECLARED]`. (3) `BASELINE_2.LEAD_WALL_S`: no leí el ledger; no resuelvo 416 vs 291. (4) `.project/` no versionado y `.project/knowledge` inexistente: la colisión de P-3 es estructural y el presupuesto de P-6a no es medible. (5) Sin corrida end-to-end con actor ni medición de retrieval: P-6b y el valor de Memory quedan `INFERRED`. (6) `check_memory_store` no está en la batería canónica (`git grep check_memory docs/VERSIONING.md` = 0), lo que sostiene a D-3, pero **no ejecuté `pytest`**: las «suites verdes» son de las pasadas, no medidas por mí. (7) `host.py:408-423` no leído en crudo (R-2).

**Desviaciones observadas (no resueltas).** (D-a) FRAME `e7bc881` vs ejecución `d61e327`: diff de 2 archivos de `docs/working/research/`; candidata a D1, no D3. (D-b) El rebuttal leyó `docs/working/audits/DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md`, fuera de la base declarada de 15 ítems pero dentro de la clase admitida («contenido versionado… en el HEAD declarado»); lo declaró y ninguna conclusión depende de él (§15 sólo penaliza evidencia nueva **silenciosa**). Si el Lead lo considera evidencia nueva, correspondería D2. (D-c) `BASELINE_2` contiene un error factual (`B-7`: la fila `AE-8` «ya es inexacta»; es exacta); la síntesis lo retracta (C-4). No es reclasificación de clase, pero es una corrección factual que el registro debería trazar. (D-d) P-1 incluye una afirmación accesoria falsa y P-7 una predicción falsa; corregidas en §3. (D-e) El rebuttal anota `PROCECUTION_2.md` inexistente: sin efecto. (D-f) El row del Plan 165 dice `Executed`, no «Closed»: imprecisión menor.

**EVALUATOR_NOTE (no cuentan como findings del tratamiento).**
- **E-1.** El baseline es inusualmente exhaustivo (B-1…B-8, R-1…R-4, A0…A3, S-1…S-3): deprime la novedad por diseño, coherente con §18 («casos pre-analizados»). El resultado no distingue «la deliberación no aporta» de «el baseline/frame ya contenía la respuesta».
- **E-2.** El valor nuevo material se concentra en `P-3`, `P-6a` y `P-8` (+`P-5b`, D-4/D-6); la base factual de la clase, no una decisión.
- **E-3.** El veredicto está sobredeterminado por hallazgos duplicados y por `P-8`: ningún `NEW`/`DERIVED` es condición necesaria. Es un hallazgo de **atribución**, no de corrección: el veredicto puede ser correcto y no atribuible.
- **E-4.** La fila `AE-8` es exacta en HEAD (sin import de `runtime.memory` desde el orquestador; sólo docstrings): contradice `B-7` y sostiene la lectura prospectiva de P-9/D-5.
- **E-5.** D-1, D-5 y D-7 leen documentación como si declarara comportamiento: patrón para el adjudicador, no finding.
- **E-6.** `DUPLICATE_SHARE` = 0,4583 está cerca de 0,50: una reclasificación de novedad lo deja en 0,50 (≤ 0,50); dos, en 0,5417. La clase no cambia porque `COSTLY` ya bloquea `SUCCESS_*`, pero el margen debe quedar declarado.


## Apéndice I — BASELINE_3 (verbatim)

# BASELINE-3 — Case-03 (ADR-worthiness del acto de autoridad del Plan 152)

## Metadata
- Rol: baseline (Result A), contexto fresh independiente
- Frame verificado: SHA-256 = `9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865` (coincide; `Get-FileHash -Algorithm SHA256 .project/campaign/frames/FRAME-3.md`)
- HEAD observado: `d61e327` (`dev`), padre `e7bc881` (el HEAD del FRAME); único delta, el preregistro que el FRAME declara previo (INFERRED: ningún archivo de evidencia del caso cambió). Árbol limpio salvo los dos untracked declarados, no leídos.
- STARTED: 2026-10-25T13:33:47-03:00
- FINISHED: 2026-10-25T13:38:21-03:00
- Archivos leídos: `FRAME-3.md`; `docs/plans/152-authority-decisions-gov-1-10.md` (completo); `docs/adr/16-change-lifecycle-authority.md`; `docs/adr/INDEX.md`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/adr/20-…-execution-records.md` (1–40); `docs/adr/_TEMPLATE.md`; `docs/plans/151-autonomy-authority-decision-closure.md` (header + coincidencias «ADR»); `docs/plans/INDEX.md` (fila 152); `docs/rfc/69-documentation-taxonomy-and-layout.md` (§Modelo ADR); `docs/CONVENTIONS.md` (§Convenciones ADR, §premises/HD-K, §autonomía, §Note, §Vigencia/retiro/work_type, §Checkpoint 700–755); `ROADMAP.md` (40–74); `CHANGELOG.md`. `docs/AGENTS.md` llegó como instrucción de workspace.
- Llamadas a herramientas (aprox.): 26 [SELF-DECLARED]. Sin pytest ni batería; sólo lectura y `git log/show/status`.

## 1. Contexto y pregunta

El Plan 152 registra, el 2026-10-07, un acto de autoridad del mantenedor que fija diez decisiones (`GOV-1 = C`; `GOV-2`…`GOV-9 = A`; `GOV-10 = B`). El acto **no** ejerció ADR-worthiness: declaró que no se produce ADR, no enmendó el ADR-19 y dejó la cuestión como `<PLAN-152>:F-1` (`open`, owner mantenedor). `ROADMAP.md:68` la lista como bloqueo vivo («ADR-worthiness del acto de autoridad de autonomía | cómo se registra la decisión»). El caso pregunta si ese acto debe registrarse en un **ADR nuevo (ADR-22)**, o si corresponde enmendar el ADR-19, o no producir ADR y registrar la determinación en un artefacto nuevo post-cierre que referencie al Plan 152.

La tensión no es «¿hay una decisión?» —la hay— sino **qué clase de registro exige**: el Plan ya contiene fecha, actor, evidencia, rationale y resultados. Resultado advisory: no resuelve `F-1` ni sustituye `AU-6`.

## 2. Evidencia disponible y verificada

1. **OBSERVED — el acto está íntegro en el Plan.** `docs/plans/152-…:Acto de autoridad registrado (2026-10-07)` fija `AUTHORITY_ACT = RECORDED`, fecha, actor, evidencia, los diez resultados con rationale y la separación `AUTHORITY ACT ≠ EXECUTION ≠ MATERIALIZATION ≠ CLOSURE`.
2. **OBSERVED — el acto declinó `AU-6`.** `docs/plans/152-…:Pregunta estructurada de ADR`: el acto «no ejerció» el juicio y «no se produce ADR»; `:Findings` registra `F-1` `open`; `:Pending decisions` deja pendiente «ADR nuevo · enmienda del ADR-19 · no producir ADR». Cerrado: commit `057a4b2` (2026-10-08) e INDEX `Executed`.
3. **OBSERVED — criterio.** `docs/adr/16-…:Decisión` punto 3: ADR si (a) se consume fuera de la RFC de origen, (b) supersede o modifica un ADR existente incluidas sus consecuencias, o (c) es invariante arquitectónico persistente auditable de forma independiente; la elevación **puede ser retrospectiva**, «no toda decisión arquitectónica necesita ADR». Punto 5: un `Accepted` no se modifica silenciosamente. `AU-2`: el ADR no autoriza payload. `AU-6`: juicio humano.
4. **OBSERVED — el contenido normativo vive en Policy.** `docs/CONVENTIONS.md:Change Lifecycle — Vía de autorización por Note (adoptado por el Plan 152, 2026-10-07)` (§390–440) y `:Change Lifecycle — Vigencia materializada, retiro y work_type (adoptado por el Plan 152, 2026-10-07)` (§447–476) materializan `GOV-3`…`GOV-9` con atribución al Plan 152. `HD-K4` (§260–262): se elevan «sin crear un RFC/ADR nuevo por defecto» y la elevación retrospectiva «no queda cerrada».
5. **OBSERVED — precedente.** `docs/adr/19-…` registra `AE-1`…`AE-10` del envelope adoptados por el acto del Plan 151 el mismo día (`Plan: plan 151`); `docs/plans/151-…:E-11` (`D-ADR`) muestra que allí la ADR-worthiness fue **decisión del acto**, planteada como «¿`D-2d` y `D-4` deben tener ADR por ser invariantes arquitectónicas persistentes?», resuelta `ADOPT`.
6. **OBSERVED — registro y coste.** `docs/adr/INDEX.md`: ADR-01…ADR-21; no existe `docs/adr/22-*.md`; próximo número libre 22. `docs/adr/_TEMPLATE.md` exige header completo (`Status`, `Fecha`, `Lifecycle`, `Superseded por`, `Motivo de retiro`, `RFC`, `Plan`…), siete secciones y registro en INDEX en el mismo commit. ADR-20/21: precedentes de ADRs de gobernanza sin `D#` y con `Plan: —`.
7. **OBSERVED — post-cierre por referencia.** `docs/CONVENTIONS.md` §722–724: un artefacto cerrado no se reescribe; la resolución se registra en un artefacto nuevo que lo referencia. `ROADMAP.md:68` es la fila a reconciliar.
8. **OBSERVED — `GOV-10` difiere la elevación.** `docs/plans/152-…:GOV-10 = B` (`COMMITMENT_NOW` / `MATERIALIZATION_LATER`): `INV-1`/`INV-3` se materializan con el Change de implementación; `docs/CONVENTIONS.md` §`INV-1`/`INV-3` — diferidos lo confirma.

## 3. Interpretación

El acto del Plan 152 es un **acto de autoridad registrado**, no una decisión arquitectónica nueva: sus diez resultados fijan gobernanza documental (identidad de IDs, provenance, artefacto `Note` y su vía, campo `Lifecycle`, campos de retiro, vista de vigencia en INDEX, criterio y política de `work_type`) y difieren la única elevación normativa. Aplicando ADR-16 punto 3 tal como está escrito:

- **(a) consumo fuera de origen:** lo consumido fuera del Plan no es el acto sino las reglas ya materializadas en `docs/CONVENTIONS.md`, Policy activa que atribuye su adopción al Plan 152. La auditabilidad independiente existe (`CONVENTIONS → Plan 152 → acto`); un ADR añade una tercera copia, no durabilidad.
- **(b) supersede o modifica un ADR:** no supersede ninguno; el acto declara no enmendar ADR-19 y sus `AE-*` no cambian. La única lectura de (b) sería que `GOV-3`/`GOV-4` o `GOV-5`/`GOV-6` extienden el modelo de ADR-16; es una calificación que el acto **no** hizo y que no decido por inferencia. Si aplicara, el contenedor sería ADR-16, no un ADR-22 que por construcción no lo toca.
- **(c) invariante arquitectónico persistente:** no se cumple. `ADR-19` (`AE-*`) y `ADR-17` son invariantes arquitectónicos; `GOV-1`…`GOV-9` son reglas del modelo documental sin mecanismo, entidad ni contrato nuevo (el Plan 152 declara `architectural impact: 2` por *resolución de gobernanza*, no por invariante). Contraste exacto con `E-11`/`D-ADR`: allí la pregunta se formuló sobre «invariantes arquitectónicas persistentes».

Conclusión: el Plan 152 es el **registro suficiente** del acto y `CONVENTIONS` el registro normativo de su contenido; un ADR-22 sería un registro de segundo grado sin decisión independiente. La simetría con ADR-19 es aparente: registra invariantes con consecuencia posterior, no la ceremonia de un acto.

## 4. Alternativas consideradas

- **C-ADR (PROCEED).** A favor: paridad formal con ADR-19 (mismo día, actor, diez decisiones) y visibilidad en la matriz ADR. En contra: duplicación Plan↔ADR, header completo, fila de INDEX y dos registros a mantener coherentes (ADR-16 punto 5).
- **B — enmendar ADR-19.** No se sostiene: los `AE-*` no cambian y el Plan 152 no pertenece al envelope salvo por origen administrativo; añadiría un acto ajeno a sus invariantes.
- **C — no ADR, determinación en artefacto nuevo post-cierre.** A favor: fuente única (Plan + CONVENTIONS), reconciliación de `ROADMAP.md:68` por referencia, no reescribe el Plan cerrado y deja abierta la elevación retrospectiva (ADR-16 punto 3; `HD-K4`). En contra: no hay fila en `docs/adr/` que un lector futuro recorra; mitigable con referencia cruzada.
- **Variante no ofrecida — registro anclado al ADR-16.** Si la preocupación fuera que `GOV-4` modifica el modelo de autoridad, el vehículo sería ese, no el ADR-19. Queda como GAP.

## 5. Supuestos

1. El acto del 2026-10-07 no contiene instrucción de ADR-worthiness (el repo sólo verifica que no la ejerció) — GAP §7.
2. `docs/CONVENTIONS.md` seguirá siendo la fuente normativa citada por plantillas y checkers, con atribución estable al Plan 152.
3. «Registro suficiente» = fecha, actor, evidencia, resultados y rationale recuperables de forma independiente y citable; el Plan 152 los provee.
4. La reconciliación de `ROADMAP.md:68` puede hacerse por referencia sin editar el Plan 152 ni usar el INDEX como registro de autoridad.

## 6. Riesgos y argumentos (B-1..B-8)

**B-1 (maintainability) — Duplicación sin ganancia de autoridad.** El Plan 152 contiene lo que C-ADR declara registrar (fecha, actor, evidencia, diez resultados, rationale, separación acto/ejecución). Ancla: `docs/plans/152-…:Acto de autoridad registrado` vs FRAME §CANDIDATE punto 2. Consecuencia: dos registros del mismo hecho a mantener coherentes; corregir un resultado obligaría a Amendment Log además del registro por referencia.

**B-2 (correctness) — El criterio (c) no se satisface.** No hay invariante arquitectónico nuevo; las diez decisiones son reglas documentales materializadas en Policy. Ancla: `docs/adr/16-…:Decisión` punto 3(c); contraste `docs/plans/151-…:E-11`. Consecuencia: un ADR-22 bajaría el listón de ADR y difuminaría la frontera ADR ↔ `docs/CONVENTIONS.md` (ADR-16 punto 4).

**B-3 (correctness) — El criterio (a) ya está cubierto por la vía normativa.** Lo consumido fuera del Plan son las reglas de `CONVENTIONS`, que declaran su adopción por el Plan 152. Ancla: `docs/CONVENTIONS.md` §390 y §447. Consecuencia: durabilidad y auditoría independiente ya existen; el ADR es redundante para (a).

**B-4 (timing) — `GOV-10` difiere la elevación: el criterio se activará después.** `INV-1`/`INV-3` se elevan con el Change de implementación. Ancla: `docs/plans/152-…:GOV-10 = B`; `docs/adr/16-…` («la elevación puede ser retrospectiva»); `HD-K4`. Consecuencia: un ADR hoy fija una parte operativa diferida y probablemente requiera enmienda o supersesión al llegar la implementación.

**B-5 (authority) — Crear el ADR ahora arriesga presentar una inferencia del agente como acto.** `F-1` sigue `open` y `AU-6` es juicio humano. Ancla: `docs/plans/152-…:Pregunta estructurada de ADR`, `:Findings` (`F-1`), `:Pending decisions`; `docs/adr/16-…` `AU-6`. Consecuencia: un `Status: Accepted` sólo es legítimo con un acto humano que resuelva la cuestión; tratar `PROCEED` como resolución reproduciría lo que el Plan 152 prohíbe (criterios de salida 4 y 9).

**B-6 (reversibility) — La asimetría favorece C.** C es reversible *hacia* ADR por elevación retrospectiva; el inverso (`Accepted` → retirarlo) exige `Superseded` + ADR nuevo + banner. Ancla: `docs/adr/16-…:Decisión` puntos 3 y 5. Consecuencia: C es la opción de bajo arrepentimiento; un ADR prematuro crea deuda histórica.

**B-7 (integración) — Si (b) aplicara, el contenedor sería ADR-16, no un ADR-22.** La vía `Note` y los campos de lifecycle extienden el modelo que ADR-16 registra; el candidato declara no enmendar ningún ADR. Ancla: `docs/CONVENTIONS.md` §390–440 y §447–476; `docs/adr/16-…:Decisión` punto 1. Consecuencia: C-ADR no puede ser «correcto» bajo (b): registra las decisiones sin registrar la modificación del modelo — argumento contra el candidato, no a favor de B (que apunta al ADR-19 equivocado).

**B-8 (cost) — Diferencia de coste pequeña; el diferencial real es el mantenimiento.** C-ADR exige template completo, header `Plan: —`/`RFC: —`, fila en INDEX y reconciliación de `ROADMAP.md:68`; C exige un artefacto nuevo que también reconcilia la fila. Ancla: `docs/adr/_TEMPLATE.md`; `ROADMAP.md:68`; `docs/CONVENTIONS.md` §722–724. Consecuencia: el ahorro inmediato es modesto; el coste recurrente del ADR decide.

## 7. Incertidumbres y GAP

- **GAP-1:** el contenido íntegro de la instrucción del mantenedor del 2026-10-07 no es verificable desde el repositorio; sólo se observa que el acto no ejerció `AU-6`. Si hubiera incluido una determinación de ADR-worthiness, el estado registrado sería inconsistente (no puedo afirmarlo ni descartarlo).
- **GAP-2:** no hay evidencia de consumo de las diez decisiones **fuera** de `CONVENTIONS`/plantillas; sin ese consumo, (a) se satisface sólo por la vía normativa.
- **GAP-3:** si `GOV-3`/`GOV-4` **modifican** el modelo de autoridad de ADR-16 es juicio humano no ejercido; no lo infiero.
- **GAP-4:** el vehículo para C (`Note` vs `Plan`) depende de `C-1`…`C-13`; `C-4` podría resultar `UNDETERMINED → humano` (§390–427). No lo decido aquí.
- **INFERRED:** el Plan 152 está cerrado (`057a4b2`; fila `Executed`); su `## Checkpoint / cierre` no deriva `Closed` en su propio texto porque el commit era acción del mantenedor, pero el commit existe.

## 8. Decisión / recomendación

**`REVISE`** — recomiendo la **alternativa C: no producir ADR-22**, y registrar la determinación `not ADR-worthy` en un artefacto nuevo post-cierre que referencie al Plan 152, reconciliando `ROADMAP.md:68` por referencia. No recomiendo B: el ADR-19 registra invariantes del envelope que este acto no toca.

Fundamento: (i) el acto ya está íntegramente registrado en un artefacto Governance y su contenido normativo en Policy, con provenance explícita; (ii) ninguno de los tres criterios se satisface con claridad y (c) —el discriminante— no se cumple; (iii) la elevación retrospectiva está permitida y `HD-K4` la deja abierta, de modo que C no cierra puertas; (iv) el coste recurrente de un ADR redundante supera su valor. La decisión final es del mantenedor (`AU-6`); este baseline no la ejerce. Si el mantenedor prefiere el ADR, el candidato es implementable como registro del acto con puntero al Plan 152, no como resolución de `F-1` sin su acto.

## 9. Plan (si corresponde)

1. Acto humano que resuelva `F-1` con determinación explícita; el agente no lo sustituye.
2. Crear el artefacto nuevo post-cierre (presumiblemente `Note`, sujeto a `C-1`…`C-13`) que: referencia el Plan 152 y `F-1`, registra `not ADR-worthy` con el análisis de (a)/(b)/(c), y **no** reescribe el Plan 152 (su línea de `F-1` permanece `open`) ni usa el INDEX como registro de autoridad.
3. Reconciliar `ROADMAP.md:68` por referencia a ese artefacto.
4. Verificación: checkers de citas/estructura en modo lectura y 0 diff fuera de la superficie declarada; sin batería completa.
5. Si se opta por ADR: ADR-22 desde `_TEMPLATE.md` (`Plan: plan 152`, `RFC: —`, `Lifecycle: active`), contenido limitado al acto + los diez IDs + separación `ACT ≠ EXECUTION ≠ MATERIALIZATION ≠ CLOSURE` + puntero al Plan 152, fila en INDEX en el mismo commit, retiro por `Superseded`.

## 10. Qué evidencia cambiaría la decisión

- Un acto humano explícito que ejerza `AU-6` y determine `ADOPT` (entonces `PROCEED`).
- Evidencia de consumo de las diez decisiones **fuera** de `CONVENTIONS` y de las plantillas (otro Plan, runtime o versión posterior que las cite directamente): activaría (a) y desplazaría la recomendación hacia C-ADR.
- La elevación efectiva de `INV-1`/`INV-3` en el Change de implementación: activaría (c) y haría que el ADR correspondiera a *ese* acto.
- Una contradicción verificable entre las reglas adoptadas y ADR-16 (p. ej. que la vía `Note` habilite autorización sin acto humano): activaría (b) y cambiaría el contenedor.
- Evidencia de que el Plan 152 no es citable de forma estable (p. ej. pérdida de resolución en checkers): debilitaría B-3 y favorecería un ADR independiente.


## Apéndice J — DEFENSE_3 (verbatim)

# DEFENSE-3 — Case-03 (ADR-worthiness del acto de autoridad del Plan 152)

## Metadata

- Rol: Defense (strongest case FOR), contexto fresh independiente
- Frame verificado: SHA-256 = `9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865` (coincide; 12.512 bytes, `Get-FileHash`)
- STARTED: 2026-10-25T13:37:19-03:00
- FINISHED: 2026-10-25T13:41:20-03:00
- Archivos leídos: `.project/campaign/frames/FRAME-3.md` (íntegro); `docs/plans/152-authority-decisions-gov-1-10.md` (íntegro); `docs/adr/16-change-lifecycle-authority.md` (íntegro); `docs/adr/19-autonomy-envelope-authority.md` (íntegro); `docs/adr/20-closed-artifact-governance-and-execution-records.md` (íntegro); `docs/adr/_TEMPLATE.md` (íntegro); `docs/adr/INDEX.md` (cabecera y filas ADR-15…ADR-21); `docs/adr/21-attested-escape-evidence-refs-and-transitions.md` (cabecera); `docs/rfc/69-documentation-taxonomy-and-layout.md:Modelo ADR`; `docs/rfc/75-change-lifecycle.md:Mecanismo 12`; `docs/CONVENTIONS.md` (líneas 245–274, 400–421, 690–744, 945–1004); `ROADMAP.md` (56–74); `docs/plans/INDEX.md` (filas 151, 152, 153, 160, 162, 163); `.agents/policies/supervised-autonomous-execution.md` (329–344); `.agents/policies/authority.md` (clases y `ADR-worthiness`)
- Comandos de lectura: `Get-FileHash`; `git rev-parse`; `git log`; `git diff --name-status`; `Get-ChildItem`; `Select-String`; `Get-Content`
- Llamadas a herramientas (aprox.): 30 [SELF-DECLARED]
- Declaración: no leí el baseline, la prosecution, el preregistro ni el otro trial.
- HEAD (OBSERVED): el frame se congeló sobre `e7bc8818`; esta sesión corre sobre `d61e327`. `git diff --name-status` entre ambos devuelve sólo los dos archivos del preregistro: `docs/adr/`, `docs/plans/`, `docs/CONVENTIONS.md` y `ROADMAP.md` son idénticos al estado congelado; `docs/adr/22-*.md` no existe.

## 1. Tesis de la defensa

El Plan 152 es suficiente como **transcripción del acto** y estructuralmente incapaz de hacer dos cosas que el repositorio exige. Primero, alojar la resolución de `<PLAN-152>:F-1`: el Plan está cerrado y su contenido gobernante no se reescribe (`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`, 722–724). Segundo, dar a las decisiones adoptadas una identidad que sobreviva al Plan, para que su cambio futuro sea auditable de forma independiente (`docs/adr/16-change-lifecycle-authority.md:Decisión`, punto 3, criterio `(c)`).

C-ADR no propone «un ADR porque hubo un acto». Propone la capa que falta: el acto ya salió de su origen —`GOV-4`…`GOV-9` fueron materializadas en `docs/CONVENTIONS.md`, `docs/VERSIONING.md` y las tres plantillas (`docs/plans/152-…md:Ejecución de la materialización (2026-10-07)`)— y sus reglas son invariantes del modelo documental (`GOV-5`, `GOV-6`, `GOV-7`, `GOV-8`), no procedimiento local. `ADR-16:Decisión` punto 3 admite la **elevación retrospectiva**, y el propio Plan 152 nombra el ADR como mecanismo aplicable «si el mantenedor lo decide» (`:Pregunta estructurada de ADR`).

La defensa sostiene que C-ADR es el vehículo correcto, no que el juicio esté hecho: el candidato sólo se vuelve `Accepted` si media el acto (propiedad 1). La autoridad permanece donde `AU-6` la pone.

## 2. Argumentos (D-1..D-8)

### D-1 — El acto satisface `(a)`: las decisiones ya se consumen fuera del Plan

- **CLAIM:** `GOV-4`…`GOV-9` no están scoped al Plan 152; son reglas vigentes que todo Change futuro consume. `(a)` se cumple hoy.
- **EVIDENCE:** `docs/plans/152-…md:Ejecución de la materialización (2026-10-07)` (tabla `GOV`→artefacto consumidor); `docs/adr/16-…md:Decisión` punto 3 `(a)`.
- **ASSUMPTION:** «consumida fuera de su origen» no exige un consumidor distinto ya existente: basta que la regla rija artefactos que el Plan no gobierna. Precedente: `docs/adr/20-…md:Alternativas consideradas` opción E fundó la ADR-20 en esa lectura.
- **CRITERION:** 1
- **CONSEQUENCE:** la decisión necesita un registro cuya identidad no dependa de un Plan cerrado.
- **CONFIDENCE:** alta (0,85)

### D-2 — El acto satisface `(c)`: produce invariantes persistentes auditables

- **CLAIM:** `HEADER = fuente / INDEX = vista` (`GOV-7`), `lifecycle ≠ status` con default por ausencia (`GOV-5`), `Superseded → existe sucesor / Abandoned → no existe sucesor` (`GOV-6`), el conjunto cerrado `C-1`…`C-13`/`N-1`…`N-7` (`GOV-4`) y el criterio de admisión de `work_type` (`GOV-8`) son invariantes del modelo documental.
- **EVIDENCE:** `docs/plans/152-…md:Acto de autoridad registrado (2026-10-07)`; `docs/CONVENTIONS.md:Change Lifecycle — Vía de autorización por Note (Plan/Note) (adoptado por el Plan 152, 2026-10-07)`, 390–421; `docs/adr/16-…md:Decisión` punto 3 `(c)`.
- **ASSUMPTION:** «invariante arquitectónico» cubre el modelo de gobernanza documental y no sólo el payload (`ADR-16`/`ADR-17`/`ADR-18` ya son ADRs de esa clase).
- **CRITERION:** 1
- **CONSEQUENCE:** sin ADR, auditar un cambio futuro de `GOV-7` sólo puede apuntar a un Plan cerrado e inmutable — lo que `(c)` excluye.
- **CONFIDENCE:** alta (0,8)

### D-3 — La elevación retrospectiva es el mecanismo previsto, y el Plan ya identificó el ADR

- **CLAIM:** C-ADR aplica la cláusula de elevación retrospectiva de `ADR-16` y el mecanismo que el Plan 152 declara aplicable si el mantenedor decide.
- **EVIDENCE:** `docs/adr/16-…md:Decisión` punto 3 («La elevación puede ser retrospectiva: una decisión inicialmente local puede requerir ADR posteriormente si comienza a satisfacer el criterio»); `docs/plans/152-…md:Pregunta estructurada de ADR` («Mecanismo vigente que se aplicaría si el mantenedor lo decide: ADR desde `docs/adr/_TEMPLATE.md`, registrado en `docs/adr/INDEX.md` en el mismo cambio»); `:Alcance` incluye `docs/adr/ (condicional)`.
- **ASSUMPTION:** «comienza a satisfacer el criterio» se verifica por el estado posterior al acto (materialización en normas y plantillas), no por una declaración del acto original.
- **CRITERION:** 1, 3
- **CONSEQUENCE:** crear el ADR-22 es el camino pre-identificado; «no producir ADR» no tiene cláusula equivalente y debe inventar su vehículo.
- **CONFIDENCE:** alta (0,85)

### D-4 — Única ruta compatible con el Plan cerrado y con `F-1`

- **CLAIM:** la resolución de `F-1` no puede escribirse en el Plan 152; el corpus ordena registrarla en un artefacto nuevo que referencia al cerrado, y para «decisión arquitectónica persistente» ese artefacto es el ADR.
- **EVIDENCE:** `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git`, 722–724; `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`, 961–964; `docs/rfc/75-change-lifecycle.md:Mecanismo 12 — Post-close Changes` (fila «decisión arquitectónica persistente → ADR»; «`Closed` nunca se reabre; la nueva acción referencia al cerrado»); `docs/plans/152-…md:Findings / Correcciones / Pending` (`F-1` textualmente `open`).
- **ASSUMPTION:** `F-1` no es corrección trivial sino la decisión de si la decisión merece ADR; cae en la fila «ADR», no en «correction + revalidation».
- **CRITERION:** 2
- **CONSEQUENCE:** la propiedad 5 del candidato sigue la regla en lugar de forzarla.
- **CONFIDENCE:** alta (0,85)

### D-5 — Simetría con ADR-19: el repositorio ya trató un acto de autoridad sobre un Plan como materia de ADR

- **CLAIM:** dos actos del mismo actor, fecha y forma recibirían tratamientos opuestos; esa asimetría es en sí un coste de auditabilidad.
- **EVIDENCE:** `docs/adr/19-…md` cabecera (`Fecha 2026-10-07`, `Plan: plan 151`) y `:Estado de implementación` («Decisión adoptada por el acto de autoridad del Plan 151»); `docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan` (fila ADR-19); `docs/plans/INDEX.md` fila del Plan 151 (acto con `D-ADR`, «materialización del ADR dentro del propio acto»).
- **ASSUMPTION:** el acto del Plan 152 es de la misma clase y alcance no menor (modelo documental, 11 archivos, frente al envelope de ADR-19).
- **CRITERION:** 1, 4
- **CONSEQUENCE:** la diferencia real es que el acto del 152 no incluyó su decisión `AU-6`; `F-1` es ese hueco.
- **CONFIDENCE:** media-alta (0,7) — `GAP`: el frame verifica el resultado (el ADR existe y se atribuye a ese acto), no el razonamiento.

### D-6 — Integra sin crear segunda fuente

- **CLAIM:** el ADR documenta el acto; el Plan sigue siendo transcripción autorizada y fuente de la autorización de ejecución.
- **EVIDENCE:** candidato, propiedades 2 y 3; `docs/plans/152-…md:Pregunta estructurada de ADR` (misma fórmula); `docs/adr/16-…md:Decisión` punto 4 y `AU-2`; `docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan` («El ADR no habilita cambios de payload»); `docs/adr/19-…md:Relaciones` («Formalizada en: plan 151»).
- **ASSUMPTION:** «documenta» es operacionalizable como metadata del acto + tabla de resultados + puntero al Plan, sin recopiar las diez decisiones.
- **CRITERION:** 2, 4
- **CONSEQUENCE:** la duplicación queda acotada por una regla de redacción exigible (§5), no por buena voluntad.
- **CONFIDENCE:** media (0,7)

### D-7 — Autoridad: no infiere, no ratifica, no convierte una inferencia del agente en acto

- **CLAIM:** el candidato es estructuralmente incapaz de usurpar `AU-6`: sólo es `Accepted` con el acto y no eleva `INV-1`/`INV-3`.
- **EVIDENCE:** candidato, propiedades 1, 3 y 5; `docs/plans/152-…md:Riesgos` riesgo 1 y `GOV-2 = A`; `.agents/policies/supervised-autonomous-execution.md` 336 («ADR-worthiness is a human judgement (ADR-16 `AU-6`)»); `docs/plans/152-…md:Criterios de salida` #9: es inválido «crear un ADR sin decisión de ADR-worthiness registrada en el acto» — la regla exige registrar la decisión, no prohíbe el ADR.
- **ASSUMPTION:** un documento que no puede declararse `Accepted` por sí mismo no ejerce autoridad.
- **CRITERION:** 3
- **CONSEQUENCE:** el modo de fallo que el frame teme queda excluido por construcción.
- **CONFIDENCE:** alta (0,85)

### D-8 — Coste acotado y reversión barata

- **CLAIM:** el candidato añade un archivo, una fila de INDEX y una de ROADMAP, sin payload, sin `VERSION` y sin tag; se retira por `Superseded`/`Motivo de retiro`.
- **EVIDENCE:** `docs/rfc/69-documentation-taxonomy-and-layout.md:Modelo ADR`; `docs/adr/_TEMPLATE.md` (`Lifecycle`, `Superseded por`, `Motivo de retiro`; INDEX en el mismo commit); `docs/adr/16-…md:Decisión` punto 5; `docs/adr/19-…md`/`docs/adr/21-…md` (ADR `Accepted`, docs-only, sin release).
- **ASSUMPTION:** el coste marginal de una fila más de ADR es menor que mantener un blocker abierto y un registro no-ADR específico.
- **CRITERION:** 5, 6
- **CONSEQUENCE:** el error simétrico —un ADR innecesario— se corrige con un archivo; no crearlo deja el blocker vivo y probablemente reabre el mismo trabajo.
- **CONFIDENCE:** alta (0,8)

## 3. Condiciones de validez del candidato

- **CO-1 (AU-6).** El mantenedor debe resolver `F-1` nombrando el ADR-22; sin ese acto el archivo no puede nacer `Accepted`.
- **CO-2 (identidad, no transcripción).** Registrar el acto (fecha, actor, evidencia, resultados, separación `AUTHORITY ACT ≠ EXECUTION ≠ MATERIALIZATION ≠ CLOSURE`) y **apuntar** al Plan para el contenido de las diez decisiones; recopiarlas completas desborda la duplicación y debilita D-6.
- **CO-3 (no retroactividad).** Declarar que documenta un acto del 2026-10-07 y que no autorizó la materialización ya ejecutada ese día (`GOV-2 = A`; `AU-2`).
- **CO-4 (Plan cerrado).** Mantener `F-1` textualmente `open` y resolver por referencia; reconciliar `ROADMAP.md:68` por referencia, sin editar el Plan ni usar el INDEX como registro de autoridad.
- **CO-5 (header).** `Plan: —` es defendible (patrón ADR-20/ADR-21) pero diverge de ADR-19 (`Plan: plan 151`); el Plan 152 debe quedar citado en `## Relaciones` y en la fila del INDEX para que la trazabilidad no dependa del header.
- **CO-6 (superficie).** Sin cambios en `protocol/`, `.agents/`, `runtime/`, `tools/`, `tests/`; `CHANGELOG.md` sólo si el playbook lo exige.

## 4. Por qué las alternativas son inferiores

**B — Enmendar el ADR-19.** Es la peor de las tres. (i) ADR-19 registra el envelope (`AE-1`…`AE-10`); las decisiones del Plan 152 son el modelo documental (`GOV-5`…`GOV-9`). Añadirlas allí convierte un «registro individual de una decisión» (`RFC-69:Modelo ADR`) en contenedor de actos y rompe la identidad que hace auditable cada invariante. (ii) Si la enmienda cambia el alcance de la decisión registrada, `ADR-16:Decisión` punto 5 y `AU-7` prohíben la modificación silenciosa y exigen ADR nuevo + supersesión: B colapsa en C-ADR **más** una supersesión, con más deuda. (iii) El `Amendment Log` preserva el texto pero agrava (i): ese log ya registra actos del 2026-10-08 y 2026-10-11 sobre el envelope; sumar un acto ajeno al tema lo vuelve un registro cronológico. (iv) B no resuelve el blocker: `ROADMAP.md:68` pregunta «cómo se registra la decisión», y una enmienda a ADR-19 no dice dónde vive la decisión del Plan 152.

**C — No producir ADR.** Es defendible y no la presento como imposible: `GOV-3` creó el artefacto `Note`, y el repositorio tiene al menos un acto de autoridad registrado sin ADR (`docs/plans/INDEX.md`, fila del Plan 163: «el registro normativo **sin ADR**»). Es inferior por tres razones. (i) La pregunta que C responde —«esto no es ADR-worthy»— es una decisión sobre el modelo ADR, y registrarla en la familia `Plan` produce la confusión de clases que la taxonomía separa (`docs/AGENTS.md:Rules`). (ii) Deja el juicio sin identidad estable: un lector futuro debe saber que la ADR-worthiness del Plan 152 se decidió en una `Note`, mientras `docs/adr/INDEX.md` —el mapa que el repositorio usa para descubrir decisiones— no lo muestra. (iii) No reduce el coste: `ADR-16` admite la elevación retrospectiva, así que el ADR puede ser necesario después y se habrá pagado la `Note` más el ADR.

## 5. Límites que la defensa reconoce

- **GAP de juicio.** No hay decisión registrada que declare el acto ADR-worthy; C-ADR propone el vehículo, no constata el juicio. Toda la defensa es condicional a `CO-1`.
- **El Plan ya registra el acto.** Contiene fecha, actor, evidencia, los diez resultados, rationale y la separación `ACTO ≠ EJECUCIÓN ≠ MATERIALIZACIÓN ≠ CIERRE`. La defensa no afirma que sea insuficiente como registro del acto, sino como registro de la **resolución** y como identidad **persistente** de los invariantes. Si el criterio del mantenedor fuera «basta la transcripción», C ganaría y el argumento decisivo sería D-2, no D-5.
- **Precedente contrario.** El Plan 163 registró un acto de autoridad sin ADR por decisión explícita; no vale el argumento categórico «todo acto merece ADR». La defensa se limita al contenido de este acto (`(a)` y `(c)`).
- **Superficie de duplicación.** La propiedad 2 pide registrar las diez decisiones con resultados y rationale; copiadas íntegramente son una segunda transcripción. El candidato sólo se sostiene con `CO-2`.
- **Retrospectividad.** El ADR nace después de la materialización del 2026-10-07; sin `CO-3` podría leerse como autorización retroactiva, que `GOV-2 = A` prohíbe.
- **Alcance.** No resuelve `F-1`, no crea el ADR y no tiene autoridad.

## 6. Compromiso

- **POSITION:** `SUPPORT_WITH_CONDITIONS`
- **CONFIDENCE:** 0,72
- **CONDITIONS UNDER WHICH THE CANDIDATE IS VALID:** que el mantenedor ejerza `AU-6` y resuelva `F-1` nombrando el ADR-22 (`CO-1`); que registre el acto y apunte al Plan sin recopiarlo (`CO-2`); que declare no retroactividad (`CO-3`); que respete el cierre del Plan y resuelva por referencia (`CO-4`); que la superficie se limite a `docs/adr/22-*.md`, `docs/adr/INDEX.md`, `ROADMAP.md` y, si corresponde, `CHANGELOG.md` (`CO-6`).
- **WHAT WOULD CHANGE MY POSITION:** (i) que el mantenedor resuelva que el acto no satisface `(a)` ni `(c)` —por ejemplo, que considere `GOV-1`…`GOV-10` procedimiento local y no invariantes del modelo documental—, lo que haría correcta la alternativa C; (ii) que la materialización del 2026-10-07 se reinterprete como acto completo que ya incluyó su registro de decisión, volviendo redundante el ADR (no es el caso: `F-1` sigue `open` y `docs/plans/152-…md:Checkpoint / cierre` declara que no se produjo ADR); (iii) que aparezca evidencia de que ADR-19 se produjo por una vía distinta de la ADR-worthiness de su acto, lo que debilitaría D-5 sin afectar D-1/D-2/D-4; (iv) que el coste de mantener el ADR-22 se demuestre mayor que el de una `Note`, lo que inclinaría la balanza hacia C.


## Apéndice K — PROSECUTION_3 (verbatim)

# PROSECUTION-3 — Case-03 (ADR-worthiness del acto de autoridad del Plan 152)

## Metadata

- Rol: Prosecution (strongest case AGAINST), contexto fresh independiente.
- Frame verificado: SHA-256 = `9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865` (coincide). HEAD observado: `d61e327`; el frame declara `e7bc881`.
- STARTED: `2026-10-25T13:45:48-03:00`
- FINISHED: `2026-10-25T13:56:00-03:00`
- Archivos leídos: `FRAME-3.md` (completo); `docs/plans/152-authority-decisions-gov-1-10.md` (parcial); `docs/adr/16-change-lifecycle-authority.md` (completo); `docs/adr/INDEX.md` (completo); `docs/adr/_TEMPLATE.md` (completo); `docs/adr/19-autonomy-envelope-authority.md` (completo); `docs/adr/20-closed-artifact-governance-and-execution-records.md` (parcial); `docs/adr/21-attested-escape-evidence-refs-and-transitions.md` (parcial); `docs/CONVENTIONS.md` (parcial); `docs/plans/171-priority-0-3-closure-implementation.md` (parcial); `docs/plans/153-plan-151-residual-closure.md` (parcial); `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` (parcial); `docs/plans/INDEX.md` (búsquedas); `ROADMAP.md` (1–74); `.agents/policies/authority.md` (36–75); `.agents/policies/supervised-autonomous-execution.md` (búsqueda `AU-6`).
- Llamadas a herramientas (aprox.): 55 [SELF-DECLARED]
- Declaración: no leí el baseline, la defense, el preregistro ni el otro trial. Salida advisory, sin autoridad; no resuelve `F-1` ni crea el ADR.

## 1. Tesis de la acusación

El candidato no es un registro neutral: decide la cuestión pendiente. Falla en tres planos que se refuerzan. **(i) Autoridad:** el acto del 2026-10-07 no ejerció `AU-6`; el ADR-22 sería el primer artefacto que declara ADR-worthy ese acto. La condición del candidato («`Status: Accepted` sólo si media el acto de autoridad…») no elimina la circularidad: si el acto ya existe, el ADR registra un acto nuevo, no el del 2026-10-07; si no existe, convierte una inferencia en autoridad. **(ii) Objeto:** excluye `INV-1`/`INV-3`, los únicos invariantes arquitectónicos persistentes, diferidos por `GOV-10 = B`, y registra decisiones documentales ya materializadas en `docs/CONVENTIONS.md`; no es el ADR que el Change de implementación necesitará. **(iii) Evidencia:** la premisa de que el Plan 152 está cerrado está contradicha por su propio checkpoint y por el registro post-close del Plan 171; el único apoyo a «cerrado» es el INDEX, que `AU-4` declara descriptivo. El resultado sería un ADR que apunta al Plan o lo duplica: no puede ser a la vez independiente y no duplicativo. La objeción no es que los ADR sean innecesarios, sino que **este** ADR no es registrable sin una decisión humana nueva que el candidato no define.

## 2. Objeciones (P-1..P-9)

**P-1 — El candidato ejerce la competencia que dice sólo documentar.**

- **OBJECTION:** El acto del 2026-10-07 no ejerció el juicio de ADR-worthiness: el Plan lo declara y deja la cuestión en `<PLAN-152>:F-1` (`open`), y su criterio de salida 9 prohíbe crear un ADR sin esa decisión. La condición «sólo si media el acto» no cura la circularidad: si el acto existe, el ADR documenta un acto nuevo, no el del 2026-10-07; si no existe, convierte una inferencia en autoridad, prohibida por `AU-6`.
- **TYPE:** REAL
- **EVIDENCE:** `docs/plans/152-authority-decisions-gov-1-10.md:### Pregunta estructurada de ADR`; `:## Criterios de salida` (punto 9); `:## Findings / Correcciones / Pending` (`F-1`); `:### Pending decisions`; `.agents/policies/authority.md:ADR-worthiness` y `:Stop conditions`.
- **TARGET:** el supuesto de que el acto ya es ADR-worthy.
- **CONSEQUENCE:** procedencia falsa o creación no autorizada; ambas violan el criterio 3 y `AU-5`/`AU-6`.
- **CONFIDENCE:** 0.90

**P-2 — La ausencia de ADR fue deliberada, no un olvido.**

- **OBJECTION:** El mismo actor, el mismo día, creó el ADR-19 para el Plan 151 (`Fecha: 2026-10-07`, `Plan: 151`, commit `cf91f0a`); para las `GOV-*` del Plan 152, el acto dice «no se produce ADR nuevo» y prohíbe sustituir la cuestión por una inferencia. La asimetría muestra una distinción deliberada que el candidato ignora.
- **TYPE:** REAL
- **EVIDENCE:** `docs/adr/19-autonomy-envelope-authority.md:3-9`; `git show --stat cf91f0a`; `docs/plans/152-authority-decisions-gov-1-10.md:### Pregunta estructurada de ADR`; `docs/plans/153-plan-151-residual-closure.md:## Relación Plan 151 → Plan 152 → Plan 153`.
- **TARGET:** la premisa de que el acto sólo dejó sin registrar una ADR que ya merecía.
- **CONSEQUENCE:** el ADR contradiría el registro del acto y convertiría un diferimiento en ratificación retroactiva.
- **CONFIDENCE:** 0.85

**P-3 — La premisa «Plan cerrado» está contradicha en el HEAD.**

- **OBJECTION:** El candidato apoya la resolución «por referencia» en un Plan cerrado. Pero el `## Checkpoint / cierre` del Plan 152 registra «Commits de cierre: `pendiente`» y deriva «**No** `Committed` …, **no** `Closed`». El Plan 171, en `## Post-close record`, afirma que su condición derivada es `Executed`, no `Closed`. El Plan 153 y el INDEX afirman `Closed`, y el INDEX es descriptivo (`AU-4`). El corpus es contradictorio y el candidato no lo resuelve.
- **TYPE:** REAL
- **EVIDENCE:** `docs/plans/152-authority-decisions-gov-1-10.md:## Checkpoint / cierre` y `:## Nota de ejecución`; `docs/plans/171-priority-0-3-closure-implementation.md:## Post-close record`; `docs/plans/153-plan-151-residual-closure.md:## Estado de partida`; `docs/adr/16-change-lifecycle-authority.md:Decisión` (`AU-4`); `git show 057a4b2`.
- **TARGET:** la premisa 5 (resolución sobre Plan cerrado) y la prohibición de editar el Plan.
- **CONSEQUENCE:** si es `Executed`, la regla de post-close no aplica; si es `Closed`, su checkpoint es falso. En ambos casos quedan `F-1` abierto, ADR `Accepted` y blocker retirado: tres registros inconsistentes.
- **CONFIDENCE:** 0.90

**P-4 — El ADR es puntero o duplicado; no puede ser las dos cosas.**

- **OBJECTION:** ADR-16 punto 4 exige que el ADR sobreviva independientemente de su RFC. Si ADR-22 sólo apunta al Plan 152, no añade registro y su `Accepted` es decorativo; si reproduce las diez decisiones, duplica el Plan y las reglas ya materializadas en `CONVENTIONS`. El candidato no define esa frontera.
- **TYPE:** REAL
- **EVIDENCE:** `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 4); `docs/plans/152-authority-decisions-gov-1-10.md:### Contenido de las decisiones (transcripción del acto)` y `:## Ejecución de la materialización`; `docs/CONVENTIONS.md:Change Lifecycle — Vía de autorización por Note` y `:Change Lifecycle — Vigencia materializada, retiro y work_type`.
- **TARGET:** criterio 4 (maintainability) y la afirmación de que el ADR no duplica.
- **CONSEQUENCE:** o no aporta valor de auditoría o crea una segunda fuente que puede derivar; la doble condición «independiente y no duplicativo» es insatisfacible.
- **CONFIDENCE:** 0.85

**P-5 — Un ADR único para diez decisiones atómicas y una diferida.**

- **OBJECTION:** El Plan verificó `ATOMICITY_STATUS = CONFIRMED` para diez decisiones. El candidato las empaqueta en un solo ADR `Accepted`, incluida `GOV-10 = B`, diferida. Por ADR-16 punto 5, cambiar cualquiera exige un ADR nuevo y superseder todo ADR-22; eso acopla decisiones independientes y crea deuda desproporcionada.
- **TYPE:** REAL
- **EVIDENCE:** `docs/plans/152-authority-decisions-gov-1-10.md:### Estado de atomicidad`; `:### GOV-10 = B — elevación con la implementación`; `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 5).
- **TARGET:** criterios 5 y 6 (coste, reversibilidad).
- **CONSEQUENCE:** cualquier ajuste de una sola regla `GOV-*` obliga a superseder todo el ADR; la reversibilidad invocada se vuelve costosa y artificial.
- **CONFIDENCE:** 0.82

**P-6 — La ADR-worthiness se afirma, no se demuestra.**

- **OBJECTION:** ADR-16 punto 3 exige `(a)`, `(b)` o `(c)`. `(b)` está excluida por el candidato. `(c)` no se satisface: `GOV-*` son provenance, identidad, forma, headers, vista de INDEX y admisión de `work_type`; los invariantes (`INV-1`/`INV-3`) quedan diferidos y excluidos. `(a)` está escrita para «la RFC que la originó»: el Plan 152 no tiene RFC y el candidato no argumenta que «otro Plan de evolución» —el Plan 160 consume `GOV-8`/`GOV-9`— baste. El candidato no identifica criterio.
- **TYPE:** REAL
- **EVIDENCE:** `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 3); `docs/plans/152-authority-decisions-gov-1-10.md` header (`RFC: —`) y `GOV-10`.
- **TARGET:** criterio 1 (correctness/necesidad).
- **CONSEQUENCE:** la premisa central no está argumentada contra el criterio que invoca; el caso falla en el primer criterio con independencia de la autoridad.
- **CONFIDENCE:** 0.80

**P-7 — El dilema de fecha y numeración.**

- **OBJECTION:** El template ordena numerar por fecha de decisión. ADR-19 es del 2026-10-07; ADR-20 y ADR-21, del 2026-10-20. Un ADR-22 decidido el 2026-10-07 quedaría fuera de orden; si su `Fecha` es la del acto que resuelve `F-1`, la decisión es ese acto, no el del 2026-10-07.
- **TYPE:** REAL
- **EVIDENCE:** `docs/adr/_TEMPLATE.md:3-10`; headers de `docs/adr/19-autonomy-envelope-authority.md`, `docs/adr/20-closed-artifact-governance-and-execution-records.md` y `docs/adr/21-attested-escape-evidence-refs-and-transitions.md`; candidato, premisa 2.
- **TARGET:** identidad del artefacto (premisas 1–2) e integración con el modelo ADR.
- **CONSEQUENCE:** si la fecha es 2026-10-07, se rompe la numeración; si es posterior, el ADR registra un acto nuevo (P-1).
- **CONFIDENCE:** 0.75

**P-8 — El impacto sobre el ROADMAP es retroactivo o no está determinado.**

- **OBJECTION:** El acto del Plan 152 registra `ROADMAP_IMPACT = NONE` y el checkpoint `NOT_REQUIRED` («no se editó `ROADMAP.md`»). El candidato reconcilia la fila del ROADMAP sin registrar las determinaciones de impacto del Change que la produce, que `CONVENTIONS` exige con rutas y evidencia; la ausencia es stop. Tampoco aclara si la fila se retira o se reescribe.
- **TYPE:** REAL
- **EVIDENCE:** `docs/plans/152-authority-decisions-gov-1-10.md:### Impacto determinado por el acto` y `:## Checkpoint / cierre`; `ROADMAP.md:🚧 Bloqueos que pueden cambiar el camino`; `docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de impacto documental y de Roadmap`; `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md:## Entregables` y `:## Pasos` (precedente: retiro de un blocker mediante un Plan).
- **TARGET:** criterio 2 (integración) y premisa 6.
- **CONSEQUENCE:** o se atribuye al acto un impacto que no tuvo, o se ejecuta un Change nuevo sin registrar su impacto; la fila queda mal conciliada y `F-1` la desmiente.
- **CONFIDENCE:** 0.78

**P-9 — Deriva de cita hacia una segunda fuente (especulativa).**

- **OBJECTION:** Una vez `Accepted`, ADR-22 podría citarse como fuente de las reglas `GOV-3`…`GOV-9` en lugar de `CONVENTIONS`, creando una segunda fuente de hecho aunque `AU-2` sólo diga que no autoriza payload. La aclaración «documenta, no sustituye» es prosa.
- **TYPE:** SPECULATIVE
- **EVIDENCE:** `docs/adr/16-change-lifecycle-authority.md:Decisión` (punto 4) e `:Invariantes` (`AU-2`); reglas ya materializadas en `docs/CONVENTIONS.md:Change Lifecycle — Vía de autorización por Note` y `:Change Lifecycle — Vigencia materializada, retiro y work_type`; ausencia de un mecanismo de precedencia de fuentes (INFERRED).
- **TARGET:** criterio 4, a largo plazo.
- **CONSEQUENCE:** si la deriva ocurre, el ADR pasa de registro a fuente de facto y gana la duplicación que el candidato quería evitar.
- **CONFIDENCE:** 0.45

## 3. Condiciones bajo las cuales el candidato sería viable

El candidato dejaría de ser inválido —no necesariamente correcto— si se cumplieran, todas juntas, estas condiciones:

1. **Acto nuevo, explícito y registrado.** Un acto del mantenedor posterior al 2026-10-07 que ejerza `AU-6`, elija `A` entre `A`/`B`/`C` y declare `AUTHORITY_ACT = RECORDED`, `AUTHORITY_INFERRED = NO`, `HISTORICAL_AUTHORITY_REUSED = NO`; debe fijar el objeto (acto histórico o `INV-1`/`INV-3`).
2. **Objeto y fecha coherentes.** Si el objeto es «registrar el acto del 2026-10-07», el acto nuevo debe aceptar que el ADR se fecha después y explicar por qué no se retrodada; si es la resolución de `F-1`, el ADR debe nombrarla como su decisión.
3. **Cierre reconciliado.** Resolver la contradicción sobre el Plan 152: o corregir por referencia su `Closed` sobre la base de la fórmula completa, o declararlo `Executed` y decidir que `F-1` se resuelve fuera. Sin esto, la regla de post-close no es aplicable.
4. **Criterio demostrado.** El ADR debe indicar `(a)`, `(b)` o `(c)` con evidencia; si es `(c)`, debe incluir `INV-1`/`INV-3` y no diferirlos; si es `(a)`, debe justificar la asimilación Plan↔RFC.
5. **Contenido acotado y no duplicativo.** Debe declarar una única fuente de verdad —el Plan para el acto, `CONVENTIONS` para las reglas— y limitarse a la decisión de ADR-worthiness y al registro del acto. No debe reproducir las diez decisiones ni crear una unidad de supersesión.
6. **Vehículo y efectos declarados.** Debe existir un Plan/Note o acción directa identificada, con `Documentation impact` y `Roadmap impact` determinados; la fila del ROADMAP debe retirarse o reescribirse citando su dueño; `F-1` debe reconciliarse por referencia.
7. **`Accepted` sólo después del acto.** El `Status` no puede preceder al acto que lo autoriza ni citarse como prueba de él.

## 4. Alternativas superiores

**C — No producir ADR, con registro nuevo.** Es la alternativa con más apoyo en el corpus. El Plan 153, al cerrar el remanente del Plan 151, concluye «ADR: no se requiere» y distingue el juicio `AU-6` del acto del Plan 152 como cuestión aparte. El Plan 160 retiró un blocker obsoleto del ROADMAP mediante un Plan y su artefacto dueño, no mediante un ADR. El Plan 171 usa un `## Post-close record` para registrar inconsistencias. Un `Note`/Plan nuevo que analice `(a)`/`(b)`/`(c)`, concluya `not ADR-worthy` con evidencia, resuelva `F-1` por referencia y reconcilie el ROADMAP cumple el objetivo con un artefacto, sin ADR `Accepted`, sin deuda de supersesión y sin duplicar el Plan. Es más barato y más reversible.

**B — Enmendar el ADR-19.** Sólo sería superior si las `GOV-*` modificaran el envelope o sus consecuencias, porque entonces el objeto correcto sería el ADR que ya registra el envelope, no un ADR nuevo sobre el acto. El ADR-19 tiene un `Amendment Log` operativo que permite agregar. Pero el corpus no muestra que `GOV-1`…`GOV-10` toquen los invariantes `AE-*`; el candidato, de hecho, excluye esa vía. Queda como alternativa condicional.

**ADR estrecho sobre los invariantes diferidos.** Si el mantenedor quiere un ADR, el objeto natural es el compromiso `GOV-10 = B` sobre `INV-1`/`INV-3`, a producir junto con el Change de implementación que los eleve. Ese ADR sí satisfaría `(c)` —invariante persistente auditable de forma independiente— y no requeriría registrar el acto ni duplicar reglas documentales.

## 5. Compromiso (POSITION / CONFIDENCE / WHAT WOULD CHANGE MY POSITION)

- **POSITION:** `OPPOSE`
- **CONFIDENCE:** 0.82
- **CONDITIONS UNDER WHICH THE CANDIDATE WOULD BE VIABLE:** las siete condiciones de la §3, en particular el acto nuevo que ejerza `AU-6`, el criterio demostrado y la reconciliación del cierre del Plan 152. Cumplidas, el candidato se convierte en una propuesta distinta —un acto nuevo más un ADR acotado—, no en el C-ADR evaluado.
- **WHAT WOULD CHANGE MY POSITION:**
  1. Un acto del mantenedor, fechado y registrado, que declare ADR-worthy el acto del 2026-10-07 y defina objeto y fecha del ADR. Entonces evaluaría el artefacto, no su existencia.
  2. Evidencia de que el Plan 152 satisface la fórmula completa de `Closed` y que su checkpoint se corrigió por referencia; eliminaría P-3.
  3. Una regla vigente que autorice tratar un Plan como artefacto originante para `(a)`, o una decisión que acepte la analogía; reduciría P-6.
  4. Un ADR acotado a `INV-1`/`INV-3` en el Change de implementación; probablemente lo apoyaría: es el invariante, no el acto.
  5. Una demostración de que ADR-22 no duplica el Plan ni `CONVENTIONS` (por ejemplo, un formato que sólo registre la decisión de ADR-worthiness y el actor); reduciría P-4 y P-5.

Mi objeción no es que el acto carezca de valor: es que el candidato decide por anticipado una cuestión reservada al mantenedor y registra el objeto equivocado sobre una premisa de cierre que el repositorio no sostiene.


## Apéndice L — SYNTHESIS_3 (verbatim)

# SYNTHESIS-3 — Case-03 (ADR-worthiness del acto de autoridad del Plan 152)

## Metadata

- **Rol:** Synthesis, contexto fresh independiente. Resultado advisory: no resuelve `<PLAN-152>:F-1`, no ejerce `AU-6` y no modifica ningún artefacto versionado.
- **Hashes verificados (coinciden los cuatro):** FRAME-3 `9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865`; BASELINE-3 `52B45433FBD68322F204C57E9530DEC0C17823F5C194C7CB9CC3FDE4B2F1B643`; DEFENSE-3 `23BA40844030D40A86F6121225E27E2AB59EA71208F5B8DC1ECDD6D39A00F837`; PROSECUTION-3 `08228EEDE7B044F90E2CC0C1759B400C2E3D761D1AC95657D2D36F3DF86143A5`. HEAD observado: `d61e327` (`dev`), padre `e7bc881`.
- **STARTED:** 2026-10-25T13:57:20-03:00; **FINISHED:** 2026-10-25T14:04:30-03:00.
- **Archivos leídos:** los cuatro artefactos completos (FRAME-3, BASELINE_3, DEFENSE_3, PROSECUTION_3). Repositorio (sólo lectura): `docs/plans/152-…md` (header, acto, impacto, materialización, atomicidad, criterios de salida, checkpoint, findings/pending); `docs/adr/16-…md`; `docs/adr/19-…md` (header, `AE-*`); headers de ADR-20/21; `docs/adr/INDEX.md`; `docs/adr/_TEMPLATE.md`; `docs/CONVENTIONS.md` (§390–440, §835–930, §948/§962); `docs/rfc/75-…md` (Mecanismo 12); `docs/plans/160-…md`; `docs/plans/171-…md` (post-close record); `docs/plans/153-…md` (estado de partida); `docs/plans/INDEX.md`; `ROADMAP.md`; `git show 057a4b2`/`cf91f0a`. No leí otros artefactos bajo `.project/campaign/`.
- **Llamadas a herramientas (aprox.):** 26 [SELF-DECLARED].

## 1. Criterion comparison (6 criterios)

### Criterio 1 — correctness / necesidad

- **Defense:** D-1: `(a)` se cumple porque `GOV-4`…`GOV-9` rigen Changes futuros; D-2: `(c)` se cumple porque `GOV-5`…`GOV-8` son invariantes del modelo documental; D-3 invoca la elevación retrospectiva. [D-1][D-2][D-3]
- **Prosecution:** P-6: `(a)` está escrita para una RFC originante y el Plan 152 tiene `RFC: —`; `(c)` falla porque los únicos invariantes arquitectónicos declarados (`INV-1`/`INV-3`) están diferidos por `GOV-10 = B`; P-1/P-2: la ADR-worthiness se afirma, no se ejerce. [P-6][P-1][P-2]
- **Evidencia compartida:** acto del Plan 152 (`GOV-1 = C`; `GOV-2`…`GOV-9 = A`; `GOV-10 = B`, `RFC: —`); `ADR-16` 3; `CONVENTIONS` §390–440/§447–476; Plan 160:19/43/61; ADR-19 (`AE-*`); ADR-20/21.
- **Clasificación:** `UNRESOLVED_DISAGREEMENT`.
- **Razón:** `(b)` está excluida y nadie la reclama. `(a)` es el punto decisivo: el Plan 160, posterior, consume `GOV-8`/`GOV-9` y retira un blocker sobre esa base, y `ADR-16` 3(a) enumera «otro Plan de evolución» como consumidor; pero la cláusula presupone una RFC originante y el Plan 152 no la tiene, así que la aplicabilidad a un origen-Plan es interpretativa. `(c)` no se demuestra: el Plan declara `architectural impact: 2` «sin crear mecanismo, entidad, state machine ni contrato nuevo» y difiere `INV-1`/`INV-3`. Es juicio (`AU-6`), no hecho. [D-1][P-6]

### Criterio 2 — integración

- **Defense:** D-4: la resolución de `F-1` no se escribe en el Plan; un artefacto nuevo lo referencia y, para una decisión persistente, ese artefacto es el ADR (RFC-75 Mecanismo 12). D-6/CO-4: el ADR documenta y el Plan sigue siendo la transcripción autorizada; INDEX y `## Relaciones` preservan la traza. [D-4][D-6][CO-4]
- **Prosecution:** P-3: la premisa «Plan cerrado» choca con el checkpoint (`Commits de cierre: pendiente`; «**No** `Closed`») y con el Plan 171, que registra `Executed`; el INDEX es descriptivo (`AU-4`). P-7: la numeración cronológica choca con fechar el ADR el 2026-10-07. P-8: no se determina si la fila del ROADMAP se retira o se reescribe ni se registran los impactos del Change. [P-3][P-7][P-8]
- **Evidencia compartida:** Plan 152 `## Checkpoint / cierre`; Plan 171 `## Post-close record`; Plan 153 `## Estado de partida`; INDEX de planes (152); `CONVENTIONS` §722–724/§948/§962; RFC-75 Mecanismo 12; `_TEMPLATE`; `ROADMAP.md:68`.
- **Clasificación:** `PARTIAL_AGREEMENT`.
- **Razón:** ambos aceptan no reescribir el Plan y reconciliar la fila por referencia; discrepan sobre si el candidato lo logra. La contradicción de cierre es real (§3.1) y P-8 es una omisión verificable, no una preferencia. [P-3][P-8]

### Criterio 3 — authority

- **Defense:** D-7: el candidato no puede usurpar `AU-6`: sólo es `Accepted` con el acto (propiedad 1) y no eleva `INV-1`/`INV-3` (propiedad 3); CO-1/CO-3 exigen el acto y prohíben la retroactividad. [D-7][CO-1][CO-3]
- **Prosecution:** P-1: circularidad — si el acto existe, el ADR registra un acto nuevo; si no, convierte una inferencia en autoridad; el criterio de salida 9 prohíbe crear un ADR sin decisión registrada. P-2: la ausencia fue deliberada (mismo actor y día, ADR-19 para el Plan 151) y el ADR ratificaría un diferimiento. [P-1][P-2]
- **Evidencia compartida:** Plan 152 `Pregunta estructurada de ADR`, criterio de salida 9, `F-1` `open`, `Pending decisions`; `AU-2`/`AU-6`; ADR-19 header (`Plan: plan 151`, `Fecha: 2026-10-07`).
- **Clasificación:** `PARTIAL_AGREEMENT`.
- **Razón:** ambos aceptan que sin acto humano nuevo no hay `Accepted` y que el ADR no autoriza payload. El candidato exige un acto externo, así que no se autoautoriza (D-7); la «circularidad» de P-1 presupone que el ADR sustituiría al acto, pero la elevación retrospectiva permite un acto nuevo que decide elevar y un ADR que lo registra y documenta el acto histórico. Falta nombrar el acto, su objeto y fecha (P-1/P-7).

### Criterio 4 — maintainability

- **Defense:** D-6/CO-2: la duplicación se acota por regla de redacción (registrar el acto y apuntar al Plan); D-8: un archivo y una fila. [D-6][CO-2][D-8]
- **Prosecution:** P-4: el ADR es puntero o duplicado, no ambas cosas; P-5: un ADR para diez decisiones atómicas acopla la supersesión; P-9: deriva de cita (especulativa). [P-4][P-5][P-9]
- **Evidencia compartida:** candidato propiedad 2 (resultados y rationale, «sin reescribirlas»); Plan 152 contenido; `CONVENTIONS` §390–440/§447–476; `ADR-16` 4/`AU-7`; ADR-19.
- **Clasificación:** `UNRESOLVED_DISAGREEMENT`.
- **Razón:** la propiedad 2 no define la frontera registro/copia, y de ella depende que el ADR sea registro o duplicado. D-6 sólo funciona con CO-2, condición de la defensa, no el candidato. Es decisión de redacción, no hecho. P-5 se debilita por ADR-19 (diez `AE-*` en un ADR) y queda acotada por `GOV-10` diferido.

### Criterio 5 — cost

- **Defense:** D-8: un archivo, una fila de INDEX y una de ROADMAP, sin payload ni versión; el error se corrige con un archivo. [D-8]
- **Prosecution:** P-5/P-8: dos registros, supersesión agrupada e impactos no previstos. [P-5][P-8]
- **Evidencia compartida:** `_TEMPLATE`; `INDEX`; `ROADMAP.md:68`; RFC-69; `ADR-16` 5; baseline B-8.
- **Clasificación:** `PARTIAL_AGREEMENT`.
- **Razón:** coste inmediato modesto; el diferencial real es el mantenimiento (B-8). P-8 añade trabajo verificable y D-8 lo subestima; el coste no decide el caso.

### Criterio 6 — reversibility

- **Defense:** D-8: se retira por `Superseded`/`Motivo de retiro`; un ADR innecesario se corrige con un archivo. [D-8]
- **Prosecution:** P-5: agrupar diez decisiones obliga a superseder todo el ADR ante cualquier cambio. [P-5]
- **Evidencia compartida:** `ADR-16` 5; `_TEMPLATE` (`Superseded por`, `Motivo de retiro`); ADR-19; baseline B-6 (asimetría C→ADR barata, ADR→C con supersesión).
- **Clasificación:** `PARTIAL_AGREEMENT`.
- **Razón:** ambos aceptan la vía de retiro; discrepan en granularidad. ADR-19 y la materialización de `GOV-1`…`GOV-9` reducen el riesgo; `GOV-10` lo acota. B-6 acierta en la asimetría, no prohíbe el ADR.

## 2. Las 9 preguntas de síntesis

**1. ¿Qué argumentos son válidos?** Defense: D-1 (conclusión, no la asunción), D-3, D-4 (parcial), D-6 (con CO-2), D-7 y D-8 (parcial). Prosecution: P-1 (precisión, no circularidad), P-3 (núcleo fáctico), P-4, P-7, P-8 y P-6 sólo en `(c)`. Baseline: B-6 y B-8; B-1/B-2 parcialmente; B-3 no. [D-1][D-3][D-4][D-6][D-7][D-8][P-1][P-3][P-4][P-7][P-8][P-6][B-6][B-8]

**2. ¿Duplicados?** P-1/P-7 (objeto y fecha del acto nuevo); P-1/P-2 (asimetría del mismo día); P-4/P-9 (la deriva es consecuencia de la duplicación); P-4/P-5 (coste de dos registros); D-1/D-2 (las decisiones escaparon del Plan, con criterios distintos); D-3/D-4 (el ADR como vía preidentificada); D-5 deriva de D-1/D-2; P-8 de la propiedad 6; B-7 de B-2. [P-1][P-7][P-2][P-4][P-9][P-5][D-1][D-2][D-3][D-4][D-5][P-8][B-7]

**3. ¿Derivados?** D-5 (simetría) no aporta un hecho nuevo: se explica por el `D-ADR` que el Plan 151 ejerció y el 152 no; P-9 deriva de P-4 sin evidencia propia; P-8 del diseño del candidato; B-7 de la lectura de `(b)`; B-6 del lifecycle de `ADR-16`. [D-5][P-9][P-8][B-7][B-6]

**4. ¿Objeciones materiales?** P-4 (frontera registro/copia), P-1/P-7 (acto, objeto y fecha), P-3 (cierre del Plan 152), P-8 (ROADMAP e impactos) y P-6(c) (`INV-1`/`INV-3` diferidos). También la corrección de B-3: `(a)` no exige auditabilidad —eso es `(c)`— sino consumo fuera del origen, y el Plan 160 lo documenta. [P-4][P-1][P-7][P-3][P-8][P-6][B-3][D-1]

**5. ¿Objeciones espurias?** P-9 (SPECULATIVE, 0.45; `AU-4` y la cláusula «documenta, no sustituye» bastan); P-5 (contradice ADR-19, que agrupa diez `AE-*`); la premisa final de P-2 (fue diferimiento: `F-1` `open` y pending registrada); D-5 como prueba de paridad; B-3 por leer `(a)` como `(c)`. [P-9][P-5][P-2][D-5][B-3]

**6. ¿Contradicciones?** La del cierre del Plan 152 (§3.1). No lo son: «no se produce ADR» vs ADR-22 (con acto nuevo es elevación retrospectiva); `Plan: —` vs el Plan 152 como objeto (elección de header, mitigable por `## Relaciones` e INDEX); `ROADMAP_IMPACT = NOT_REQUIRED` vs la fila viva (la fila registra lo no resuelto). [P-1][P-2][CO-5][P-8]

**7. ¿Incertidumbres?** (i) `(a)` con origen-Plan; (ii) «arquitectónico persistente» para `GOV-5`…`GOV-9`; (iii) `Closed` vs `Executed`; (iv) la instrucción del 2026-10-07 (GAP-1); (v) la decisión del mantenedor; (vi) `C-4` vs registro directo; (vii) `Fecha`/numeración. [P-6][D-2][P-3][P-7]

**8. ¿Evidencia adicional necesaria?** §8: acto humano, reconciliación del cierre y consumo de las diez decisiones más allá del Plan 160 si se mantiene la lectura estricta de `(a)`. [P-6][P-3]

**9. ¿Qué cambió respecto del baseline?** §6: el baseline recomendó C y trató `(c)` como no satisfecha y `(a)` como cubierta; esta síntesis halla apoyo literal para `(a)` (Plan 160) y viabilidad de C-ADR con revisiones. [D-1][D-3][B-2][B-3]

## 3. Contradicciones y desacuerdos preservados

### 3.1 Contradicción real: el estado de cierre del Plan 152

- **Criterio:** integración / premisa de resolución post-cierre.
- **Posiciones:** el Plan 152 declara `Commits de cierre: pendiente` y «**No** `Committed` …, **no** `Closed`» (`:## Checkpoint / cierre`); el INDEX dice «quedó cerrado (condición derivada `Closed`)»; el Plan 153 registra «`Closed` derivada»; el Plan 171 afirma que el Plan 152 «tiene findings `open`, pero su condición derivada es `Executed`, no `Closed`»; el FRAME lo da por cerrado. [P-3]
- **Evidencia:** Plan 152:629/645; INDEX (prosa 152); Plan 153:30; Plan 171 `## Post-close record`; `AU-4`; `git show 057a4b2` (commit de cierre existente).
- **Razón de no resolución:** el corpus contiene las dos lecturas y ninguna es autoritativa por sí sola: el INDEX es descriptivo (`AU-4`), el cuerpo del Plan y el registro posterior del Plan 171 favorecen `Executed`, pero el commit `057a4b2` existe (`Committed`). Resolverlo exige decisión o registro por referencia, no voto. La regla de post-cierre (`CONVENTIONS` §722–724/§948/§962) se invoca por analogía: el candidato no la necesita para no reescribir el Plan, pero sí para describir su premisa. [P-3][D-4]

### 3.2 Desacuerdo preservado: `(a)`/`(c)` en el criterio 1

- **Posiciones:** Defense D-1/D-2 (ambos); Prosecution P-6 (ninguno); baseline B-2/B-3 (sólo `(a)` «cubierta» por la vía normativa).
- **Evidencia:** `ADR-16` 3; Plan 152 (`RFC: —`, `GOV-10 = B`, `architectural impact: 2`); Plan 160:19/43/61; ADR-19 (`AE-*`); ADR-20/21.
- **Razón:** la aplicabilidad de `(a)` a un origen-Plan y la calificación «arquitectónica» del modelo documental son juicios (`AU-6`), no hechos; la evidencia apoya el consumo externo pero no cierra la interpretación. [D-1][D-2][P-6][B-2][B-3]

### 3.3 Desacuerdo preservado: registro vs copia (criterio 4)

- **Posiciones:** Defense D-6/CO-2 (registro acotado); Prosecution P-4 (puntero o duplicado).
- **Evidencia:** candidato propiedad 2; Plan 152 contenido; `CONVENTIONS` §390–440/§447–476; `ADR-16` 4.
- **Razón:** depende de una frontera de redacción que el candidato no define y que ninguna evidencia puede fijar; debe decidirla el Change. [D-6][CO-2][P-4]

## 4. Verdict

**VIABLE** (advisory; no decide `AU-6` ni resuelve `F-1`).

**BASIS:**

- `(a)` tiene base defendible: las decisiones se consumen fuera de su origen —el Plan 160, posterior, se apoya en `GOV-8`/`GOV-9` (`docs/plans/160-…:19/43/61`)— y `ADR-16` 3(a) enumera «otro Plan de evolución». Esto corrige B-3 y la parte `(a)` de P-6. [D-1][P-6][B-3]
- La elevación retrospectiva está permitida (`ADR-16` 3; `AU-6`) y el Plan 152 nombra el ADR como mecanismo «si el mantenedor lo decide»; la ausencia del juicio en 2026-10-07 no es barrera absoluta. [D-3]
- El candidato no usurpa autoridad: exige acto externo para `Accepted`, no eleva `INV-1`/`INV-3` y no toca `protocol/` ni el ADR-19; la circularidad de P-1 no se sostiene tal como está formulada. [D-7][CO-1][P-1]
- Hay patrón de ADRs de gobernanza no derivados de `D#` (ADR-20/21, `Plan: —`), lo que hace integrable el header y el registro directo. [D-4][CO-5]
- No es `NOT_VIABLE`: las objeciones que sobreviven (P-4, P-1/P-7, P-3, P-8) son defectos de redacción y reconciliación, no incompatibilidades estructurales. En el plano del vehículo tampoco es `UNDETERMINED`; lo indeterminado es `(c)` y la decisión humana, que se preservan. [P-4][P-1][P-7][P-3][P-8]

## 5. Recommendation

**REVISE** (C-ADR, antes de llevarlo al acto).

- **Qué cambió:** el baseline recomendaba `REVISE` hacia C (no ADR); esta síntesis recomienda `REVISE` sobre C-ADR, porque `(a)` tiene apoyo literal en el consumo posterior (Plan 160) y el vehículo ADR es el que RFC-75 Mecanismo 12 prevé para una decisión persistente. [D-1][D-3][D-4][B-3][P-6]
- **Por qué:** el candidato corregido registra la decisión sin sustituir al Plan y conserva `AU-6`; C no elimina el problema de fondo (deja la cuestión fuera del mapa de ADRs) y su vehículo (`Note`) es dudoso bajo `C-4` («decisión de diseño/arquitectura → Plan (+ ADR si `AU-6`)»). [D-4][D-6][D-7]
- **Evidencia:** Plan 160 (consumo), `ADR-16` 3/4/5, RFC-75 Mecanismo 12, ADR-20/21, `CONVENTIONS` §390–440 (`C-4`), `ROADMAP.md:68`, `docs/adr/INDEX.md` (libre 22). [D-1][D-4][D-6]
- **Correcciones:** (1) nombrar el acto nuevo que resuelve `F-1`, con objeto, fecha y `AUTHORITY_ACT = RECORDED`; (2) fechar el ADR en la resolución y llevar 2026-10-07 a `## Contexto`; (3) acotar la propiedad 2 a la decisión, los diez resultados y el puntero, declarando fuente única (Plan para acto/provenance; `CONVENTIONS` para reglas); (4) reconciliar por referencia el cierre del Plan 152; (5) decidir si la fila del ROADMAP se retira o reescribe y registrar impactos; (6) declarar `Plan: plan 152` o `Plan: —` con `## Relaciones` e INDEX. [P-1][P-7][P-4][P-3][P-8][CO-5]
- **Incertidumbre que permanece:** `(c)`, la lectura estricta de `(a)` y la decisión del mantenedor; el veredicto es advisory. [P-6][D-2]

## 6. Cambios atribuibles vs baseline

**WHAT CHANGED VS BASELINE**

- **Decisión/recomendación:** baseline → `REVISE` hacia C; síntesis → `REVISE` sobre C-ADR. Atribución: D-1/D-3 contra B-3 y P-6; P-4/P-1/P-7/P-8 como condiciones. [D-1][D-3][B-3][P-6][P-4][P-1][P-7][P-8]
- **Verdict:** baseline no declaró C-ADR viable; síntesis → `VIABLE` (advisory), por D-1, D-3, D-7 y ADR-20/21; no por D-2 ni D-5. [D-1][D-3][D-7][D-2][D-5]
- **Plan:** baseline → acto humano + `Note`/artefacto nuevo + ROADMAP; síntesis → acto humano + ADR-22 revisado + INDEX + ROADMAP + reconciliación del cierre. Atribución: D-4/D-6 y P-3/P-8. [D-4][D-6][P-3][P-8]
- **Condiciones:** se añaden fecha/objeto (P-1/P-7), frontera registro/copia (P-4), cierre (P-3) e impactos/fila (P-8). [P-1][P-7][P-4][P-3][P-8]
- **Premisa:** el baseline dio el Plan 152 por cerrado (`INFERRED`); el Plan 171 registra `Executed` y el INDEX `Closed`: la premisa queda inestable. [P-3]

**ATTRITION**

- **Defense:** D-2 no resiste (`INV-1`/`INV-3` diferidos; el Plan declara no crear mecanismo/entidad/contrato); D-5 no resiste como prueba (la asimetría se explica por el `D-ADR` del Plan 151); D-6 no resiste tal como está (la propiedad 2 pide rationale; sólo CO-2 lo salva); la asunción de D-1 no resiste, aunque su conclusión sí (Plan 160). [D-2][D-5][D-6][D-1]
- **Prosecution:** P-2 no resiste (fue diferimiento); P-5 no resiste (ADR-19 agrupa diez `AE-*`); P-9 no resiste (especulativa); P-6 no resiste en `(a)` (Plan 160 y la letra), sí en `(c)`; P-3 no resiste en su consecuencia («tres registros inconsistentes»: `F-1` `open` con resolución por referencia es el patrón), sí en el núcleo fáctico. [P-2][P-5][P-9][P-6][P-3]
- **Baseline:** B-3 no resiste (lee `(a)` como auditabilidad, que es `(c)`); B-1 queda debilitada (la identidad ADR y la supersesión independiente aportan); GAP-2 queda refutada en parte por el Plan 160 (`GOV-8`/`GOV-9`); B-6 y B-8 resisten. [B-3][B-1][B-6][B-8]

## 7. Rebuttal recomendado

**REBUTTAL_RECOMMENDED: SI.**

- **Objeción material:** P-4 — el ADR no puede ser simultáneamente independiente del Plan 152 y no duplicativo. Decide el criterio 4 y el candidato no la responde: la propiedad 2 pide resultados y rationale y a la vez no reescribirlos. [P-4]
- **Evidencia existente que bastaría (máximo 1):** candidato (propiedad 2) + CO-2 + `ADR-16` 4 + la separación de fuentes vigente (Plan 152 para acto/provenance; `CONVENTIONS` §390–440/§447–476 para reglas). Un rebate puede fijar la frontera: el ADR registra la decisión de elevación, los diez resultados y el puntero, sin reproducir el rationale. No requiere evidencia nueva ni autoridad. [P-4][CO-2][D-6]
- **Por qué no otras:** P-1/P-7 se resuelven con el acto y una convención de fecha; P-3 requiere reconciliación, no rebate; P-8 es redacción del Change. [P-1][P-7][P-3][P-8]

## 8. Evidencia adicional necesaria / REQUIRES_NEW_EVIDENCE

- **`REQUIRES_NEW_EVIDENCE` — acto humano que resuelva `F-1`.** No es evidencia del repositorio, pero es condición de validez: sin acto registrado del mantenedor (`AU-6`) que elija A/B/C y fije objeto y fecha, el ADR no puede nacer `Accepted`. No lo resuelvo. [D-7][P-1]
- **`REQUIRES_NEW_EVIDENCE` — reconciliación del cierre del Plan 152.** El corpus se contradice (`Executed` vs `Closed`); hace falta un registro por referencia o una decisión. [P-3]
- **`REQUIRES_NEW_EVIDENCE` — consumo de las diez decisiones más allá del Plan 160, si se mantiene la lectura estricta de `(a)`.** El Plan 160 documenta `GOV-8`/`GOV-9`; no las otras ocho. [P-6][D-1]
- **`REQUIRES_NEW_EVIDENCE` — calificación de «arquitectónico persistente» para `GOV-5`…`GOV-9`.** Es juicio (`AU-6`), no hecho verificable. [D-2][P-6]
- **No requiere evidencia nueva:** numeración (libre 22), header (ADR-20/21), no reescritura (`CONVENTIONS` §948/§962) y reconciliación del ROADMAP. [P-7][CO-5][D-4]


## Apéndice M — REBUTTAL_3 (verbatim)

# REBUTTAL-3 — ¿P-4 cambia la evaluación?

## Metadata

- **Rol:** Rebuttal, contexto fresh independiente. Advisory: no resuelve `AU-6`, no resuelve `<PLAN-152>:F-1`, no crea autoridad ni modifica el repositorio.
- **Hashes verificados (los cinco coinciden; `Get-FileHash -Algorithm SHA256`):** FRAME-3 `9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865`; BASELINE-3 `52B45433FBD68322F204C57E9530DEC0C17823F5C194C7CB9CC3FDE4B2F1B643`; DEFENSE-3 `23BA40844030D40A86F6121225E27E2AB59EA71208F5B8DC1ECDD6D39A00F837`; PROSECUTION-3 `08228EEDE7B044F90E2CC0C1759B400C2E3D761D1AC95657D2D36F3DF86143A5`; SYNTHESIS-3 `22338229273C36704F31E077364F4DD013F866C72B1B913286246C506721B4AE`.
- **Repositorio:** rama `dev`, HEAD `d61e327`; árbol con los dos untracked que el FRAME declara no-evidencia (no leídos).
- **STARTED:** 2026-10-25T14:04:25-03:00; **FINISHED:** 2026-10-25T14:06:50-03:00.
- **Archivos leídos:** los cinco artefactos del trial, completos. Repositorio (sólo lectura): `docs/adr/16-change-lifecycle-authority.md` (completo); `docs/adr/19-autonomy-envelope-authority.md` (completo); `docs/adr/_TEMPLATE.md` (completo); `docs/plans/152-authority-decisions-gov-1-10.md` (líneas 28–107 y 215–254, más búsqueda `transcripción|rationale`). No leí otros archivos bajo `.project/campaign/` ni el otro trial.
- **Llamadas a herramientas (aprox.):** 18 [SELF-DECLARED].

## 1. La objeción P-4 y qué afirma exactamente

P-4 (`PROSECUTION_3.md:46-53`) sostiene que ADR-16 punto 4 exige que el ADR sobreviva independientemente de su RFC, y de ahí deriva una disyuntiva: si ADR-22 sólo apunta al Plan 152, «no añade registro y su `Accepted` es decorativo»; si reproduce las diez decisiones, «duplica el Plan y las reglas ya materializadas en `CONVENTIONS`». Conclusión: la doble condición «independiente y no duplicativo» es **insatisfacible** (CONFIDENCE 0.85).

La objeción tiene dos patas: (i) una tesis **normativa** —qué exige ADR-16 punto 4—, y (ii) una tesis **lógica** —que sólo existen dos opciones y ambas fallan—. La segunda lleva el peso: si fuera cierta, C-ADR sería estructuralmente imposible y el `VIABLE` caería a `NOT_VIABLE`. La primera, sola, sólo mostraría una frontera de redacción mal definida: lo que la síntesis ya clasificó como `UNRESOLVED_DISAGREEMENT` (criterio 4).

## 2. Respuesta con evidencia existente

**(1) El candidato tiene un objeto propio que la disyuntiva no contempla.** El FRAME asigna a ADR-22 dos contenidos que el Plan 152 no tiene: la resolución de `<PLAN-152>:F-1` (propiedad 5) y la determinación de ADR-worthiness que el acto del 2026-10-07 **no ejerció**. La metadata del acto, los diez resultados y la separación `AUTHORITY ACT ≠ EXECUTION ≠ MATERIALIZATION ≠ CLOSURE` (propiedad 2) están en el Plan como transcripción, es decir, como provenance, no como registro autónomo. Un artefacto que registra la determinación de elevar y la identidad del acto no es «sólo un puntero»: registra una decisión que antes no existía.

**(2) Sólo un ítem de la propiedad 2 cruza realmente la frontera: `el rationale`.** El Plan 152 declara que la evidencia del acto incluye «rationale por decisión» (`docs/plans/152-…:## Alcance`, línea 232) y su `### Contenido de las decisiones (transcripción del acto)` (línea 41) es la transcripción autorizada, con la formulación de cada `GOV-*`. Si el ADR reproduce ese rationale por decisión, sí hay segunda transcripción. Los demás ítems no: los resultados son letras (`C`, `A`, `B`), la fecha y el actor son metadata de identidad, y la separación `ACT ≠ EXECUTION ≠ …` es una regla de lectura que el ADR necesita para no confundirse con autorización. Es decir: P-4 acierta en **un** ítem y generaliza a los seis. Ese acierto acotado genera `R-1`.

**(3) «Independiente» se mide contra la RFC, no contra el Plan.** ADR-16 punto 4 dice: «ADR = decisión arquitectónica que debe sobrevivir independientemente de **su RFC**» (`docs/adr/16-…:Decisión`, líneas 79-84); la palabra «Plan» no aparece. El template prescribe el puntero como campo propio: `Formalizada en: <RFC y plan, …>` (`docs/adr/_TEMPLATE.md:54-57`). La instancia existente es concluyente: ADR-19 está `Accepted`, declara `Plan: plan 151` y en `:Relaciones` (líneas 97-98) dice que registra las diez decisiones `D-1`…`D-6b` **del Plan 151**. Es la combinación que P-4 llama insatisfacible —registrar decisiones ya transcritas en un Plan, con puntero— y el corpus la aceptó sin tratarla como duplicación. La distinción es funcional: el ADR formula las decisiones como enunciados normativos con identidad estable (`AE-1`…`AE-10`) y el Plan conserva la transcripción y el rationale. Que esa distinción sea **suficiente** es juicio (`AU-6`); que sea **posible** no: ya existe. Esto genera `R-2`.

**(4) Consecuencia: la frontera se fija con una cláusula, no con una decisión estructural.** Basta sustituir en la propiedad 2 «el rationale» por «el rationale de la determinación de ADR-worthiness», o eliminarlo, dejando la transcripción y el rationale por decisión en el Plan. Eso es exactamente la corrección (3) de la síntesis y la condición CO-2 de la defensa. No requiere evidencia nueva, no requiere autoridad nueva y no altera la identidad del candidato: es redacción.

**Desacuerdo preservado.** P-4 sigue siendo `REAL`: la propiedad 2, tal como está escrita, contiene el germen de la duplicación y el candidato no fija la frontera en términos de enumeración. Un lector razonable puede sostener que, estrechada hasta ese punto, la renta marginal del ADR se reduce y que C sería más barato (B-8). Ese desacuerdo no se dirime aquí y no se dirime por conteo de posiciones.

## 3. ¿Cambia el VERDICT? (SI/NO + razón)

**NO.** El `VIABLE` se apoya en bases que P-4 no toca: el consumo externo de las decisiones (`(a)` con el Plan 160), la licitud de la elevación retrospectiva, la imposibilidad de que el candidato se autorice sin acto (`AU-6`) y la existencia de ADRs de gobernanza con `Plan: —`/`RFC: —`. P-4 ataca sólo el criterio 4, que la síntesis declara que «no decide el caso». La única vía para cambiar el veredicto es su tesis de insatisfacibilidad, refutada por una instancia `Accepted` del corpus (ADR-19). Lo que sobrevive es un defecto de redacción localizado: la categoría con la que la síntesis descarta `NOT_VIABLE`.

## 4. ¿Cambia la RECOMMENDATION? (SI/NO + razón)

**NO.** La recomendación ya es `REVISE` sobre C-ADR, y su corrección (3) ordena «acotar la propiedad 2 a la decisión, los diez resultados y el puntero, declarando fuente única». P-4 no añade una corrección de otra clase ni desplaza el objetivo hacia C: su forma operativa **es** la corrección (3). Lo que P-4 sí cambia es la precisión y la prioridad de esa corrección: de «acotar» a «excluir explícitamente el rationale por decisión y conservarlo en el Plan». Eso es refinamiento dentro de `REVISE`, no cambio de recomendación. Tampoco habilita volver a C: la elección del vehículo se apoyó en la visibilidad en `docs/adr/INDEX.md` y en la duda sobre el vehículo de C bajo `C-4`, y P-4 no aporta nada sobre ninguna de las dos. Si el Change ejecutara la corrección (3) sin excluir el rationale, la recomendación quedaría mal ejecutada, no invalidada.

## 5. Findings nuevos (R-n) o REQUIRES_NEW_EVIDENCE

**R-1 — `CLAIM`:** el único ítem de la propiedad 2 que produce duplicación es `el rationale` (por decisión); el resto son metadata de identidad, resultados nominados y una regla de separación, cuya presencia es lo que hace del ADR un registro y no un puntero. **`EVIDENCE`:** FRAME candidato propiedades 2 y 5; `docs/plans/152-…:## Alcance` (línea 232, «rationale por decisión»); `:### Contenido de las decisiones (transcripción del acto)` (línea 41). **`CONSEQUENCE`:** P-4 no puede concluir «insatisfacible»; su corrección es una cláusula. El defecto es real pero localizado, y no altera el veredicto.

**R-2 — `CLAIM`:** la combinación «registrar diez decisiones ya transcritas en un Plan + puntero al Plan» no es insatisfacible ni inédita: es el patrón de un ADR `Accepted` del corpus. **`EVIDENCE`:** `docs/adr/19-…` (header `Plan: plan 151`, `:Relaciones` líneas 97-98, `:Invariantes` `AE-1`…`AE-10`, `:Estado de implementación`); `docs/adr/16-…:Decisión` punto 4 (la independencia se predica de la RFC); `docs/adr/_TEMPLATE.md:54-57` (`Formalizada en: <RFC y plan, …>`). **`CONSEQUENCE`:** la pata lógica de P-4 cae; queda en pie su pata normativa, que es una exigencia de redacción. No se sigue de aquí que la frontera elegida sea la correcta: eso es juicio.

**R-3 — `CLAIM`:** estrechar la frontera reduce la renta marginal del ADR-22 y refuerza B-8, sin invertir la recomendación. **`EVIDENCE`:** B-8 (`BASELINE_3.md:69`); D-8 (`DEFENSE_3.md:88-95`); `PROSECUTION_3.md:130` (su condición 5); corrección (3) de la síntesis. **`CONSEQUENCE`:** `REVISE` sobre C-ADR sigue apoyada en el vehículo y la visibilidad, no en el volumen de contenido; el diferencial de mantenimiento que B-8 señala subsiste y debe declararse en el Change.

**`REQUIRES_NEW_EVIDENCE`:** **ninguno para esta respuesta.** La frontera es una decisión de redacción del Change; la aceptación del patrón ADR-19 como regla para ADR-22 es juicio reservado (`AU-6`), no evidencia faltante. La única pieza externa sigue siendo el acto humano que resuelva `F-1`, ya registrado como `REQUIRES_NEW_EVIDENCE` por la síntesis (§8); no la introduzco ni la sustituyo. No se usó evidencia nueva fuera de la base admitida por el FRAME (puntos 1, 2, 4 y 5).

## 6. Compromiso (cambia/no cambia; confianza)

- **VERDICT:** no cambia (`VIABLE`). **RECOMMENDATION:** no cambia (`REVISE` sobre C-ADR); sí se precisa la corrección (3), con exclusión explícita del rationale por decisión.
- **CONFIDENCE:** 0.78. Alta en que la insatisfacibilidad es falsa (hay instancia `Accepted`) y en que el defecto es de redacción; media en que el mantenedor acepte el corte estrecho como suficiente, que es donde P-4 conserva su fuerza.
- **QUÉ ME HARÍA CAMBIAR:** evidencia de que el ADR-19 no registra realmente las decisiones del Plan 151 sino sólo una formulación independiente (debilitaría `R-2`), o una decisión del mantenedor de que el ADR debe contener el rationale completo (convertiría la duplicación en estructural y reabriría el veredicto).


## Apéndice N — EVALUATION_3 (verbatim)

# EVALUATION-3 — clasificación y métricas

## Metadata

- **Rol:** Evaluation, contexto `fresh` independiente. Aplica §8–§13 del preregistro congelado. **No** emite la decisión de campaña (§14).
- **Fuente normativa:** `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md` (HEAD `d61e327`, `dev`), §8–§16.
- **Hashes verificados** (`Get-FileHash -Algorithm SHA256`; los seis coinciden):
  - `FRAME-3.md` = `9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865` ✓
  - `BASELINE_3.md` = `52B45433FBD68322F204C57E9530DEC0C17823F5C194C7CB9CC3FDE4B2F1B643` ✓
  - `DEFENSE_3.md` = `23BA40844030D40A86F6121225E27E2AB59EA71208F5B8DC1ECDD6D39A00F837` ✓
  - `PROSECUTION_3.md` = `08228EEDE7B044F90E2CC0C1759B400C2E3D761D1AC95657D2D36F3DF86143A5` ✓
  - `SYNTHESIS_3.md` = `22338229273C36704F31E077364F4DD013F866C72B1B913286246C506721B4AE` ✓
  - `REBUTTAL_3.md` = `81705E05F0B1BC74403651B5C2CB75EE34C7C1B5ED73F0F14D2966E60002B98B` ✓
- **STARTED:** 2026-10-25T14:09:07-03:00 · **FINISHED:** 2026-10-25T14:16:05-03:00
- **Archivos leídos:** los seis artefactos del trial, completos; el preregistro (§8–§16). Repositorio, sólo lectura: `docs/plans/152-…md` (header, acto, impacto, materialización, pregunta ADR, atomicidad, criterios de salida, checkpoint, findings/pending); `docs/adr/16-…md` (completo); `docs/adr/19-…md` (header, `AE-*`, Relaciones); headers de ADR-20/21; `docs/adr/INDEX.md`; `docs/adr/_TEMPLATE.md`; `docs/CONVENTIONS.md` (§390–429, §447–476, §690–729, §835–884, §933–964); `docs/rfc/75-…md:327–339`; `docs/plans/160-…md` (:16–22, :41–45, :59–63); `docs/plans/171-…md` (post-close record); `docs/plans/153-…md` (estado de partida); `docs/plans/151-…md` (`E-11`/`D-ADR`); `docs/plans/INDEX.md` (:9, :1550–1583); `ROADMAP.md` (:60–74); `.agents/policies/supervised-autonomous-execution.md:336`; `git log/show/merge-base`. **No** leí otros archivos de `.project/campaign/` ni el otro trial.
- **Llamadas a herramientas:** 34 **[SELF-DECLARED]**. Sin `pytest`; sólo lectura y Git de consulta.
- **Integridad:** `e7bc881..HEAD` contiene un único commit (`d61e327`, el preregistro) → ningún archivo de evidencia cambió tras congelar el FRAME; `057a4b2` es ancestro de HEAD; no existe `docs/adr/22-*.md`. **Única escritura:** este archivo; sin `git add/commit`.

## 1. Método de clasificación y deduplicación

**Separaciones declaradas (§8.3).** Separé grupos que mezclan afirmaciones con distinta verificabilidad o consecuencia: `D-3` → `D-3a` (elevación retrospectiva) / `D-3b` («no producir ADR no tiene cláusula»); `P-1` → `P-1a` (no se nombra el acto nuevo) / `P-1b` (circularidad); `P-4` → `P-4a` (insatisfacibilidad) / `P-4b` (la propiedad 2 duplica el rationale); `P-6` → `P-6a` ((c)) / `P-6b` ((a)). No inventé findings: cada fila de §2 es un `D-n`/`P-n`/`R-n` existente o una de estas separaciones.

**Deduplicación entre pasadas.** Son el mismo distinct si comparten la **misma afirmación** y la **misma consecuencia material**; nunca por tema, vocabulario o pasada. Apliqué el criterio una vez: `P-4b` (Prosecution) y `R-1` (Rebuttal) afirman lo mismo —el único elemento de la propiedad 2 que duplica es el `rationale`, y la frontera se fija con una cláusula— con la misma consecuencia (acotar la propiedad 2 / excluir el rationale) → **1 distinct, 2 ocurrencias**, atribuido a Prosecution por primera ocurrencia. No deduplicé `D-6`: afirma la *posibilidad* de un registro acotado (criterio 4 satisfacible), no la *ubicación* de la frontera ni la necesidad de corregir la propiedad 2. El resto son afirmaciones distintas aunque compartan tema (`D-2`/`P-6a` son inversas).

**Novedad.** Comparé contra `BASELINE_3` (no contra el FRAME ni el repositorio) con la regla de desempate de §8.1: hecho + consecuencia → `DUPLICATE`; hecho sin la consecuencia → `DERIVED`; ninguno → `NEW`. «Hecho» = contenido material, no formulación. Si el baseline tiene el hecho y una consecuencia **opuesta**, no es `DUPLICATE` (no hay «misma consecuencia material») sino `DERIVED`. Evidencia nueva ausente del baseline (consumo del Plan 160, estado del Plan 171, tabla de RFC-75, fechas de ADR-20/21) → `NEW`.

**Materialidad (terminal).** Apliqué las tres condiciones de §9: soporte anclado o medido; consecuencia concreta y especificada sobre un objeto de su lista; objeto identificado. Premisa central falsa, mal leída o con confusión semántica → `SPURIOUS` (sustituye a los otros dos). Soportado pero expositivo, de coste no especificado, ya cubierto por una condición del candidato o hipotético sin condición → `NON_MATERIAL`. Un `DUPLICATE` puede ser `MATERIAL` absoluto sin aportar valor nuevo.

**Anclas.** Verifiqué en el repositorio versionado (sólo lectura) todo `NEW`, `DERIVED` o `MATERIAL`, y todo finding que citara pasajes. `ANCHOR_VERIFIED: SI/NO/GAP`; si la cita existe pero la premisa es falsa, corregí en §3.

## 2. Tabla de findings

`ANCHOR` juzga la consecuencia; `n/a` = no exigido por §1.5.

| ID | pass | claim corto | novelty | materiality | anchor | consequence | notas |
|---|---|---|---|---|---|---|---|
| D-1 | Def | `(a)` se cumple: el Plan 160 consume `GOV-8`/`GOV-9` | `NEW` | `MATERIAL` | SI | registro con identidad independiente de un Plan cerrado | `BASELINE_3:74` (GAP-2) daba ese consumo por ausente |
| D-2 | Def | `(c)` se cumple: `GOV-5`…`GOV-8` son invariantes del modelo documental | `DERIVED` | `SPURIOUS` | SI (premisa falsa) | sin ADR sólo se puede apuntar a un Plan cerrado | falso: las reglas viven en `CONVENTIONS` (§390–421/§447–476), Policy activa; `152:7` niega mecanismo/entidad/contrato nuevo |
| D-3a | Def | la elevación retrospectiva (`ADR-16 §3`) es el mecanismo previsto | `DUPLICATE` | `MATERIAL` | SI | legalidad del vehículo ADR | `BASELINE_3:43/83` ya la usaba con la misma consecuencia |
| D-3b | Def | «no producir ADR» no tiene cláusula y debe inventar vehículo | `NEW` | `SPURIOUS` | **NO** | obliga a preferir ADR | falso: `CONVENTIONS §390–421` define `Plan`/`Note`; el FRAME ya define el artefacto nuevo |
| D-4 | Def | `RFC-75 Mec. 12` asigna ADR a la decisión arquitectónica persistente post-cierre | `NEW` | `MATERIAL` | SI | plan/vehículo: ADR en lugar de `Note` | depende de «arquitectónica persistente» (juicio) y de la premisa de cierre (`P-3`) |
| D-5 | Def | simetría con ADR-19: la asimetría es coste de auditabilidad | `DERIVED` | `NON_MATERIAL` | SI | ninguna concreta; `F-1` ya registrado | `BASELINE_3:24/37` ya trató y descartó la simetría |
| D-6 | Def | el ADR integra sin segunda fuente si se acota a metadata+tabla+puntero | `DERIVED` | `NON_MATERIAL` | SI | criterio 4 satisfacible | consecuencia ya cubierta por la propiedad 2 del candidato (§9); sólo `CO-2` la sostiene |
| D-7 | Def | el candidato no usurpa `AU-6` por construcción (props. 1/3/5) | `DERIVED` | `NON_MATERIAL` | SI | riesgo de autoridad excluido, sin cambio de objeto | `BASELINE_3:63` (B-5) ya exigía acto humano |
| D-8 | Def | coste acotado y reversión por `Superseded` | `DERIVED` | `NON_MATERIAL` | SI | coste/mantenimiento, sin objeto de §9 | `BASELINE_3:69` (B-8) ya lo daba por decisivo |
| P-1a | Pros | no se nombra el acto nuevo (objeto/fecha); criterio de salida 9 | `NEW` | `MATERIAL` | SI | condición/evidencia: acto registrado antes de `Accepted` | `152:530/572/656/676` |
| P-1b | Pros | circularidad irresoluble (acto existente vs inferencia) | `NEW` | `SPURIOUS` | **NO** | ninguna: dilema falso | presupone que el ADR sustituye al acto; `ADR-16 §3` admite acto nuevo que eleva |
| P-2 | Pros | la ausencia de ADR fue deliberada y el ADR ratificaría un diferimiento | `DERIVED` | `SPURIOUS` | **NO** | ninguna: no retroactividad ya en prop. 5 | mal leída: `F-1` `open` + pending = diferimiento (`152:155/530/656/676`) |
| P-3 | Pros | la premisa «Plan cerrado» está contradicha en el HEAD | `NEW` | `MATERIAL` | SI | condición: reconciliar el cierre antes de la regla post-close | `152:629/645`, `171:222`, `153:30/153`, `INDEX:1562` vs fila `Executed` |
| P-4a | Pros | «puntero o duplicado»: independiente y no duplicativo es insatisfacible | `NEW` | `SPURIOUS` | **NO** | ninguna: tesis lógica falsa | ADR-19 es instancia `Accepted` del patrón |
| P-4b ≡ R-1 | Pros/Reb | sólo el `rationale` por decisión duplica; la frontera es una cláusula | `NEW` | `MATERIAL` | SI | criterio de aceptación: excluir rationale, fuente única | **distinct único, 2 ocurrencias**; `R-1` ancla `152:41/232` |
| P-5 | Pros | un ADR para diez decisiones atómicas acopla la supersesión | `DERIVED` | `NON_MATERIAL` | SI | coste/reversibilidad no medido | ADR-19 agrupa diez `AE-*`; «desproporcionado» no se cuantifica |
| P-6a | Pros | `(c)` no se satisface: `INV-1`/`INV-3` diferidos, sin criterio | `DUPLICATE` | `MATERIAL` | SI | criterio 1: `(c)` no sostiene el ADR | duplica `BASELINE_3:57` (B-2), mismo hecho y consecuencia; `CONVENTIONS:471`, `152:7` |
| P-6b | Pros | `(a)` exige RFC originante y el Plan tiene `RFC: —` | `NEW` | `SPURIOUS` | **NO** | ninguna | mal leída: `ADR-16 §3(a)` enumera «otro Plan de evolución»; Plan 160 lo es |
| P-7 | Pros | fecha/numeración: template numera por fecha; acto 2026-10-07, ADR-20/21 2026-10-20 | `NEW` | `MATERIAL` | SI | identidad y campo `Fecha`; integración | `_TEMPLATE:4–5`; headers ADR-19/20/21 |
| P-8 | Pros | se reconcilia el ROADMAP sin impactos ni decisión retiro/reescritura | `NEW` | `MATERIAL` | SI | plan: dos determinaciones de impacto y decisión de fila | `CONVENTIONS §835` (título real «Determinaciones de cierre…»); `152:142–153/642–644` |
| P-9 | Pros | deriva de cita: ADR-22 podría sustituir a `CONVENTIONS` como fuente | `NEW` | `SPURIOUS` | n/a | hipotética sin condición | autoclasificada `SPECULATIVE` (0,45); §9 excluye «podría fallar» |
| R-2 | Reb | «registrar decisiones transcritas + puntero» ya existe `Accepted` (ADR-19) | `NEW` | `MATERIAL` | SI | viabilidad: cae la insatisfacibilidad | `ADR-19:4–6/92–96`, `ADR-16 §79–81`, `_TEMPLATE:57` |
| R-3 | Reb | estrechar la frontera refuerza B-8 sin invertir la recomendación | `DUPLICATE` | `NON_MATERIAL` | SI | ninguna nueva | duplica `BASELINE_3:69` (B-8) |

## 3. Anclas no verificadas / falsas

**3.1 Falsas o mal leídas (corrección incluida).**

1. **`D-3b` — NO.** «No producir ADR debe inventar su vehículo»: `CONVENTIONS §390–421` define la vía `Plan`/`Note` con `C-1`…`C-13`, y el FRAME (alternativa C) especifica el artefacto nuevo. Hay que elegir vehículo, no inventarlo.
2. **`P-1b` — NO.** El dilema presupone que el ADR sustituye al acto. `ADR-16 §74–78` permite la elevación retrospectiva y el candidato exige acto nuevo (prop. 1) **y** documentación del acto histórico (prop. 2).
3. **`P-2` — NO.** El Plan registra un **diferimiento**, no una decisión: «el acto no contiene el juicio», «la cuestión queda como `Pending Decision`», «sustituirla por una inferencia está prohibido» (`152:155/530`), `F-1` `open` (`:656`).
4. **`P-4a` — NO.** Omite la tercera posibilidad ya aceptada: ADR-19 registra las diez decisiones del Plan 151 con `Plan: plan 151` y `Formalizada en` (`ADR-19:4–6/92–96`).
5. **`P-6b` — NO.** `ADR-16 §3(a)` enumera «otra RFC, **otro Plan de evolución**, runtime, versión posterior» (`:68–70`); el Plan 160 es ese consumidor (`160:19/43/61`).

**3.2 Verificadas con corrección menor.**

- **Estado del Plan 152 (`P-3`, `D-4`).** `152:3` = `Status: Executed`; `:645` = condición derivada **`Executed`**, «No `Committed` … **no** `Closed`»; `:629` = «Commits de cierre: `pendiente`». Pero `057a4b2` («close plan 152 authority act», 2026-10-08) existe y es ancestro; `171:222` dice «su condición derivada es `Executed`, no `Closed`»; `153:30/153` dice «`Closed` derivada»; el INDEX en prosa dice «quedó cerrado (condición derivada `Closed`)» (`:1562`) mientras su tabla declara `Executed` (`:1582`). La contradicción es real: **`P-3` verificado**. Corrección al FRAME: afirma el cierre «(`Executed`/`Closed`; `INDEX`, fila 152)», pero la fila citada sólo dice `Executed`.
- **`AU-6` como «juicio humano».** El literal de `AU-6` (`ADR-16:118–119`) no usa «humano»; la lectura se ancla en `.agents/policies/supervised-autonomous-execution.md:336`, en `ADR-16 §76–78` («conserva juicio arquitectónico») y en la clase `DECISION` (`§52–53`). Las pasadas están soportadas, pero el ancla correcta es la policy.
- **`R-2` cita `ADR-19:97–98`**; `:Relaciones` está en `:92–96` (contenido correcto, línea desplazada).
- **`P-8` cita «Determinaciones de impacto documental y de Roadmap»**; el título real es «Determinaciones de **cierre**: impacto documental e impacto de Roadmap» (§835).
- **`D-1` invoca «tabla `GOV`→artefacto consumidor»**: `152:163–174` es tabla de **materialización**, no de consumidores; el consumo externo lo aporta el Plan 160.

**3.3 Verificadas correctamente (muestra).** `ROADMAP.md:68`; `ADR-16 §68–73/79–81/111–121`; `ADR-19` header (`Accepted`, `Fecha 2026-10-07`, `Plan: plan 151`); `ADR-20/21` (`Plan: —`, `Fecha 2026-10-20`); `ADR INDEX` (ADR-01…21, ocho columnas con `Vigencia`, sin 22); `_TEMPLATE:4–5` (numeración cronológica) y `:57`; `RFC-75:327–339` (Mec. 12: «decisión arquitectónica persistente → ADR»; «`Closed` nunca se reabre»); `CONVENTIONS §690–729` (fórmula de `Closed`, post-close `:722–724`), `§933–964`, `§835–884`, `§471` (`INV-1`/`INV-3` diferidos); `152:572` (criterio 9), `:535` (`ATOMICITY_STATUS = CONFIRMED`), `:232`, `:41`, `:642–644`; Plan 151 `:180` (`E-11`/`D-ADR` = `ADOPT`).

## 4. Conteos y shares

Occurrences = **24** (Def 9, Pros 12, Reb 3). Distinct = **23** (una deduplicación: `P-4b ≡ R-1`). Cifras primarias sobre distinct (§8.3).

| Métrica | Distinct | Occurrences |
|---|---|---|
| Findings | 23 | 24 |
| `NEW` | 13 | 14 |
| `DERIVED` | 7 | 7 |
| `DUPLICATE` | 3 | 3 |
| `MATERIAL` | 10 | 11 |
| `NON_MATERIAL` | 6 | 6 |
| `SPURIOUS` | 7 | 7 |
| `NEW+MATERIAL` | 8 | 9 |
| `DERIVED+MATERIAL` | 0 | 0 |
| `DUPLICATE+MATERIAL` | 2 | 2 |
| `DISTINCT_MATERIAL_NEW` | **8** | — |

`DISTINCT_MATERIAL_NEW_BY_PASS`: Def **2** (`D-1`, `D-4`), Pros **5** (`P-1a`, `P-3`, `P-4b`, `P-7`, `P-8`), Reb **1** (`R-2`). Filas: `D-1`, `D-4`, `P-1a`, `P-3`, `P-4b`/`R-1`, `P-7`, `P-8`, `R-2`.

`DUPLICATE_SHARE` = 3/23 = **0,130** (occ. 0,125) → `REDUNDANT` NO, `VERY_REDUNDANT` NO. `SPURIOUS_SHARE` = 7/23 = **0,304** (occ. 0,292) → `SPURIOUS_HIGH` **SI** (> 0,15 y > 0,10).

**Costes (§11).**

| Pasada | `SELF_S` | `LEAD_WALL_S` | Palabras |
|---|---|---|---|
| BASELINE-3 | 274 | 416 | 2195 |
| DEFENSE-3 | 241 | 254 | 2296 |
| PROSECUTION-3 | 612 | 635 | 2300 |
| SYNTHESIS-3 | 430 | 445 | 2712 |
| REBUTTAL-3 | 145 | 130 | 1485 |
| **TREATMENT** | **1428** | **1464** | **8793** |

`TREATMENT_SELF_S` = 241+612+430+145 = **1428** ✓; `TREATMENT_LEAD_WALL_S` = 254+635+445+130 = **1464** ✓; `RATIO_SELF` = 1428/274 = 5,2117 → **5,21** ✓; `RATIO_LEAD` = 1464/416 = 3,5192 → **3,52** ✓; `RATIO_EFFECTIVE` = max = **5,21** ✓; `COSTLY` = 5,21 > 3,0 → **SI** ✓; `WORDS_RATIO` = 8793/2195 = 4,006 → **4,01** ✓. **Sin discrepancia aritmética.**

Discrepancias de medición: (i) `REBUTTAL-3 LEAD_WALL_S` 130 < `SELF_S` 145 (delta −15 s, única negativa) — inconsistencia a explicar por el Lead. (ii) `WALL_CLOCK_RATIO` = **`GAP`**: falta el lanzamiento del tratamiento; indicativo **[SELF-DECLARED]** `DEFENSE STARTED` 13:37:19 → `SYNTHESIS FINISHED` 14:04:30 = 1631 s / 416 = 3,92 (descriptivo). (iii) Tokens = `GAP` estructural; llamadas = `[SELF-DECLARED]`.

`EFFICIENCY`: 8/1428×1000 = **5,60** (SELF) y 8/1464×1000 = **5,46** (LEAD); impactos decisionales 2 → 1,40/1,37; `NEW` distinct 13 → 9,10/8,88.

## 5. Impacto y atribución

`BASELINE_3`: `REVISE` hacia **C** (no ADR-22), sin verdicto. `SYNTHESIS_3`: verdicto **`VIABLE`** y `REVISE` **sobre C-ADR**. El label coincide, el **objeto** de la recomendación cambió (C → C-ADR): lo trato como cambio decisional y lo declaro.

| Cambio | Cita IDs | Cadena | Contrafactual | Clase |
|---|---|---|---|---|
| Recomendación: C → C-ADR | Sí: `D-1`/`D-3` vs `B-3`/`P-6` | Sí (`D-1`→Plan 160; `D-4`→RFC-75) | quitar `D-1`+`D-4` → vuelve C; quitar sólo `D-1` **no** colapsa | `DECISIONAL_IMPACT` (`D-1`,`D-4`) |
| Verdicto: — → `VIABLE` | Sí: `D-1`,`D-3`,`D-7` | Sí | quitar `D-1` → cae `(a)`; `D-4`/`D-7` sostienen viabilidad | `DECISIONAL_IMPACT` (parcial, `D-1`) |
| Vehículo: `Note` → ADR-22 | Sí: `D-4`,`D-6` | Sí | sin `D-4` → revierte a `Note` | `PLAN_IMPACT` (`D-4`) |
| Reconciliar el cierre del Plan 152 | Sí: `P-3` | Sí | sin `P-3` no hay paso | `PLAN_IMPACT` (`P-3`) |
| Acto nuevo con objeto/fecha; `Fecha` del ADR | Sí: `P-1`,`P-7` | Sí | sin ambos no hay corrección | `PLAN_IMPACT` (`P-1a`,`P-7`) |
| ROADMAP: retiro vs reescritura + impactos | Sí: `P-8` | Sí | sin `P-8` no hay paso | `PLAN_IMPACT` (`P-8`) |
| Acotar prop. 2 y fuente única | Sí: `P-4` | Sí (con `R-1`) | sin `P-4b` no hay corrección | `PLAN_IMPACT` (`P-4b`) |
| Evidencia: acto humano; consumo más allá del Plan 160 | Sí: `P-1`/`D-7`; `P-6`/`D-1` | Sí | — | `EVIDENCE_IMPACT` (`P-1a`,`D-1`) |

**Totales:** `DECISIONAL_IMPACT` **2** (recomendación, verdicto); `PLAN_IMPACT` **5**; `EVIDENCE_IMPACT` **2**; `DECISION_IMPACT` **SI**; `REWEIGHTING` **0** (la relectura de `B-3` está respaldada por `D-1`, no es reweighting); `NO ATRIBUIDO` **0**.

**Caveats (§10 estricta).** Hay cita de IDs y cadena verificable en todos los cambios; el contrafactual **por ID** sólo se cumple en los cambios de un solo apoyo (`D-4`, `P-3`, `P-7`, `P-4b`, `P-8`). En recomendación y verdicto se cumple **a nivel de conjunto** (`D-1`+`D-4`): eliminar `D-1` solo no revierte. No lo registro como `NO ATRIBUIDO` porque el conjunto citado contiene `NEW+MATERIAL` que enuncia la consecuencia y el conjunto vacío revierte el resultado. `D-3` (`DUPLICATE`) y `D-7` (`NON_MATERIAL`) figuran como argumentos pero no pueden fundar atribución.

**Sensibilidad.** Si «mismo label `REVISE`» se leyera como no-cambio, subsiste el verdicto (`D-1`) y `DECISION_IMPACT` sigue `SI`. Si se anulara toda atribución decisional, `VALUE_CLASS` pasaría a `PLAN`; **la clase del trial no cambia** (§6).

## 6. VALUE_CLASS y clase del trial (§13.2)

| Flag | Valor |
|---|---|
| `DISTINCT_MATERIAL_NEW` | 8 (≥ 1) |
| `DECISIONAL_IMPACT` | 2 (≥ 1) |
| `PLAN_IMPACT` / `EVIDENCE_IMPACT` | 5 / 2 |
| `DECISION_IMPACT` | SI |
| `DUPLICATE_SHARE` | 0,130 → `REDUNDANT` NO, `VERY_REDUNDANT` NO |
| `SPURIOUS_SHARE` | 0,304 → `SPURIOUS_HIGH` SI |
| `COST_RATIO` (EFFECTIVE) | 5,21 → **`COSTLY` SI** |

`VALUE_CLASS`: no `NONE` (8 ≥ 1); no `EVIDENCE` (`DECISION_IMPACT` ≠ 0); no `PLAN` (`DECISIONAL_IMPACT` ≥ 1); **`DECISION`** (`DECISIONAL_IMPACT ≥ 1`, con `PLAN_IMPACT` adicional).

Orden de §13.2: (1) `INVALID_TRIAL` **NO** (hashes coinciden, cinco artefactos, sin D3); (2) `NEGATIVE` **NO** (`VALUE_CLASS` ≠ `NONE`; ningún `MATERIAL` verificado como falso en dirección errónea); (3) `SUCCESS_STRONG` **NO** (`SPURIOUS_SHARE` 0,304 > 0,10 y `COSTLY`); (4) `SUCCESS_PARTIAL` **NO** (no es `PLAN`); (5) `SUCCESS_EVIDENCE` **NO**; (6) `NO_EVIDENCE` **NO**; (7) **`POSITIVE_BUT_COSTLY` SÍ** (`VALUE_CLASS ∈ {EVIDENCE,PLAN,DECISION}` ∧ `COSTLY`) → **primera clase que se cumple**.

**Clase del trial propuesta: `POSITIVE_BUT_COSTLY`.** Las clases 8/9 tendrían componentes satisfechos, pero §13.2 ordena y la 7 precede; el flag que decide es `COSTLY`. Sin ambigüedad que impida clasificar: la clase es insensible a la disputa de atribución y a `SPURIOUS_SHARE` > 0,15.

## 7. GAP, desviaciones y notas del evaluador

**7.1 `GAP`.** Tokens/contexto (estructural); llamadas `[SELF-DECLARED]`; lanzamiento del tratamiento no declarado → `WALL_CLOCK_RATIO` no primario. Del caso: la instrucción del 2026-10-07 no es verificable (`GAP-1`); el consumo de las diez decisiones sólo está documentado para `GOV-8`/`GOV-9` (Plan 160) (`GAP-2`); «arquitectónico persistente» es juicio `AU-6`, no hecho (`GAP-3`); se desconoce si `(a)`/`(c)` fueron considerados en el acto original (`GAP-4`).

**7.2 Desviaciones observadas (no resueltas; clasificación D1/D2/D3 del Lead).**

1. **Solapamiento baseline → defensa:** `BASELINE-3 FINISHED` 13:38:21 vs `DEFENSE-3 STARTED` 13:37:19 (62 s antes). §17.1 exige baseline cerrado antes del tratamiento. La defensa declara no haber leído el baseline y no cita su hash; el orden registrado no cumple. Con timestamps `[SELF-DECLARED]` no es concluyente → desviación de orden, candidata a D2.
2. **Solapamiento síntesis → rebuttal:** `SYNTHESIS FINISHED` 14:04:30 vs `REBUTTAL STARTED` 14:04:25 (5 s antes), aunque el rebuttal verifica el hash de la síntesis. Mismo tratamiento.
3. **`LEAD_WALL_S` < `SELF_S`** en REBUTTAL (130 < 145).
4. **FRAME congelado sobre `e7bc881`, ejecución sobre `d61e327`:** verifiqué que el único delta es el preregistro; sin cambio de evidencia (D1 declarada por las pasadas).
5. **No verificable:** la no-lectura de archivos prohibidos sólo está declarada; sin attestación externa.

**7.3 `EVALUATOR_NOTE` (no cuentan como findings del tratamiento).**

1. **El FRAME sobreafirma el cierre del Plan 152:** su `EVIDENCE STATE` lo da por cerrado «(`Executed`/`Closed`; `INDEX`, fila 152)», pero la fila citada dice `Executed`; el `Closed` proviene de prosa del INDEX y de los Planes 153/171, que contradicen el checkpoint del propio Plan. Traslada a todas las pasadas una premisa no unívoca.
2. **El INDEX se contradice internamente** para el Plan 152: prosa «cerrado (`Closed`)» vs tabla `Executed`. La resolución plausible en el HEAD es que `057a4b2` materializa el commit que el checkpoint daba por pendiente, pero el registro no se reconcilió.
3. **La síntesis apoya el cambio decisional en `D-3` (`DUPLICATE`)** (§6 «Atribución: D-1/D-3»), lo que §10 no permite; el cambio se sostiene por `D-1`/`D-4`.
4. **`P-6a` es `DUPLICATE+MATERIAL`:** la objeción de `(c)` no aporta valor nuevo; el aporte nuevo de la acusación en criterio 1 (`P-6b`) resultó `SPURIOUS`. En criterio 1, el valor nuevo válido es a favor (`D-1`, `D-4`), no en contra.
5. **El FRAME ya contenía la pregunta `(a)`/`(c)` y la alternativa C completa:** techo de descubrimiento bajo por diseño (§18); varios de los 8 `DISTINCT_MATERIAL_NEW` son precisión sobre material preexistente.

**7.4 Riesgos de clasificación (para el ADJUDICADOR).**

1. **`D-2 → SPURIOUS`** es la llamada más discutible (`(c)` es juicio). La sostengo porque su consecuencia («sólo un Plan cerrado») es falsa: las reglas viven en Policy activa. Si se re-clasificara `MATERIAL`, `SPURIOUS_SHARE` = 0,261 y la clase **no cambia**.
2. **Dedupe `P-4b ≡ R-1`:** si fueran dos distinct, corpus 24, `DISTINCT_MATERIAL_NEW` = 9, `SPURIOUS_SHARE` = 0,292; clase sin cambio. Si además se deduplicara `D-6`, corpus 22 y `DISTINCT_MATERIAL_NEW` = 8; clase sin cambio.
3. **Atribución decisional de conjunto:** si se anulara, `VALUE_CLASS` = `PLAN` en 4 pasos, pero `SPURIOUS_SHARE` 0,304 > 0,10 bloquea `SUCCESS_PARTIAL` y la clase sigue siendo `POSITIVE_BUT_COSTLY`. Robusta la clase; no así la etiqueta `DECISION` vs `PLAN`.
4. **`P-6b → SPURIOUS`** depende de leer el paréntesis de `ADR-16 §3(a)` como enumeración de consumidores; el texto lo respalda, pero la aplicabilidad de `(a)` a un origen-Plan sigue interpretativa (la síntesis la preserva como desacuerdo).
5. **`D-6`/`D-7` → `NON_MATERIAL`** por la cláusula de §9 (consecuencia ya cubierta por condición del candidato). Si fueran `MATERIAL`, `DISTINCT_MATERIAL_NEW` = 10; clase sin cambio.

**Alcance.** Clasifico, verifico anclas y computo métricas; **no** emito la decisión de campaña (§14). La clasificación es la primaria y se congela antes del análisis cross-trial (§8.3).


## Apéndice O — ADJUDICATION (verbatim)

# ADJUDICATION — re-clasificación independiente

## Metadata

- **Rol:** Adjudicador independiente. **STARTED:** 2026-10-25T14:18:37-03:00. **FINISHED:** 2026-10-25T14:24:51-03:00.
- **Archivos leídos:** preregistro §8–§18 (líneas 200–499); `FRAME-2.md` y `FRAME-3.md`; los seis artefactos de cada trial (Trial #2 y #3). Repositorio, sólo lectura: `runtime/orchestrator/{fc_flow,agent_worker,__main__}.py`; `runtime/memory/store.py`; `runtime/toolcalls/{project_store,prompt_rendering}.py`; `tests/{test_fc_host_integration,test_fc_flow}.py`; `tools/check_memory_store.py`; `docs/adr/{16,19}-*.md`; `docs/plans/{152,160,165}-*.md`; `docs/plans/INDEX.md`; `.gitignore`; `git grep`.
- **Llamadas a herramientas (aprox.):** 39 **[SELF-DECLARED]**. Sin `pytest`, sin web, sin `git add/commit`.
- **Declaración:** no conocí la decisión esperada de campaña, no leí el ledger, ni `review/`, ni el otro análisis cross-trial, ni artefactos de Trial #1. Clasifiqué cada trial tras leer sus seis artefactos y **antes** de abrir su `EVALUATION`; la comparación es posterior. Escritura: este archivo.

## 1. Método y muestra

Apliqué §8.1 (desempate: hecho + consecuencia = `DUPLICATE`; hecho sin consecuencia = `DERIVED`; ninguno = `NEW`), §8.2/§9 (`MATERIAL` = soporte + consecuencia concreta + objeto identificado; `SPURIOUS` terminal por falta de soporte, evidencia falsa/mal leída, confusión semántica o ataque a una versión no propuesta) y §8.3 (unidad atómica; distinct = misma afirmación + misma consecuencia; sin doble conteo). El desempate es competencia del ADJUDICADOR (§8.1, última frase), no del Lead.

**Universo y muestra.** Trial #2: 24 occurrences = 24 distinct; 18 classified by the evaluator in decisive categories (`NEW+MATERIAL`, `DERIVED+MATERIAL`, `DUPLICATE+MATERIAL`, `SPURIOUS`). Trial #3: 24 occurrences, 23 distinct declared by the evaluator; 17 decisive. Re-clasifiqué **todos** los decisivos y, como muestra declarada, **los 6 restantes de cada trial (100 %, > 25 % exigido)**, ordenados por ID: Trial #2 `D-2, D-8, P-6b, P-10, R-1, R-3`; Trial #3 `D-5, D-6, D-7, D-8, P-5, R-3`. Acepté las separaciones atómicas del evaluador (P-1a/b, P-5a/b, P-6a/b, D-3a/b, P-4a/b), salvo cuando alteran la identidad del finding (ver §6). No usé la síntesis como referente de novedad; sólo el baseline del mismo trial.

## 2. Trial #2: re-clasificación de categorías decisivas

| ID | Clase adjudicada | Ancla y razón |
|---|---|---|
| D-1 | `DUPLICATE+MATERIAL` | Baseline §2 «Estado documental» y §8/A3: README describe FC-3 y ningún camino suministra store; misma consecuencia (rechazar obliga a corregir la declaración). |
| D-3 | `DUPLICATE+MATERIAL` | Baseline A1: «Coste bajo y reversible»; D-3 añade soporte (fail-closed, suites), no una consecuencia distinta. |
| D-5 | `DUPLICATE+MATERIAL` | Baseline B-7+B-8: frontera memory-free, evidencia estructural y fila AE-8 (`ADR-19:165`); misma consecuencia. |
| P-1a | `DUPLICATE+MATERIAL` | Baseline B-1: `__main__.py:188` construye `AgentWorker()` con `NullAgentInvoker`; «estándar» sobre ruta sin actor. |
| P-1b | `DUPLICATE+MATERIAL` | Baseline B-3: único `write` en `consolidation.py:92`, sólo tests; declarar estándar un no-op. |
| P-2 | `DUPLICATE+MATERIAL` | Baseline B-2: `fc_flow.py:63-68` no reconoce `statement`/`description`; fallback JSON truncado. |
| P-4 | `DUPLICATE+MATERIAL` | Baseline B-6: sin lifecycle/epistemic ni `retrieval.eligible`; mismos registros no vigentes. |
| P-5a | `DUPLICATE+MATERIAL` | Baseline B-4: `.gitignore:13`, `git ls-files .project` = 0; pérdida invisible. |
| D-4 | `DERIVED+MATERIAL` | Baseline S-2/§2 «Placement» tiene las premisas; la conclusión «no añade trabajo» restringe alcance. `placement-contract.md:131,303`; `plans/150:74`. |
| D-6 | `DERIVED+MATERIAL` | Baseline B-4/§2 (`list_records` ⇒ `[]`); inferencia: lector read-only, sin ownership. `store.py:81-113`. Materialidad delgada: modos de falla, no elegibilidad. |
| P-7 | `DERIVED+MATERIAL` | Baseline §2 cita `test_fc_host_integration.py:56-58`; inferencia: deriva semántica del test. La predicción «debe reescribir» es falsa; sobrevive el criterio de verificación. |
| P-9 | `DERIVED+MATERIAL` | Baseline B-7/R-4 pide actualizar la fila; `ADR-19` es `Accepted` con `Amendment Log` (`:110-152`); inferencia: no es docs-only. Objeto authority. |
| R-2 | `DERIVED+MATERIAL` | Baseline S-1 y R-1 ya exigen punto compartido; inferencia: P-1a es reparable. `host.py` vía citas, `agent_worker.py:354,364,373`. |
| P-3 | `NEW+MATERIAL` | Ausente del baseline: `project_store.py:3` designa `project_segment.json` en la misma base; `store.py:98-106` levanta todo `*.json`; `check_memory_store.py:62-64,86-100` lo rechaza. Exige filtro `kind`/namespace. |
| P-5b | `NEW+MATERIAL` | Ausente del baseline: `rebuild(records)` (`store.py:108-114`) exige los registros del llamador; no hay fuente semántica en DEV. Requisito de durabilidad/rebuild. |
| **P-6a** | **`DERIVED+MATERIAL`** (evaluador: `NEW+MATERIAL`) | Baseline B-5 contiene el hecho: «memoria entra como sufijo posterior al render». Falta la consecuencia (no se contabiliza contra `context_budget`), no el hecho. `agent_worker.py:84,427-430`; `prompt_rendering.py:26-45`. |
| **P-8** | **`DERIVED+MATERIAL`** (evaluador: `NEW+MATERIAL`) | Baseline §8: «el plan 165 (que ya declaró FC-3 integrado)», más B-1 (ningún suministro). La inferencia «no era criterio pendiente» no estaba explicitada. `plan 165:359,420`. |
| D-7 | `DUPLICATE+SPURIOUS` | Baseline R-1 ya exige punto único. El ancla central es falsa: `git grep "AgentWorker("` da **un** constructor de producción (`__main__.py:188`); `agent_worker.py:269-276` es el Protocol `AgentInvoker`; «N embedders» es hipotético. Sin soporte ⇒ terminal. |

**Muestra restante (6/6):** D-2 `DUPLICATE+NON_MATERIAL` (baseline GAP-1/A0; preferencia normativa, sin condición nueva); D-8 `DUPLICATE+NON_MATERIAL` (B-3+R-3: declaración proporcional); P-6b `DERIVED+NON_MATERIAL` (B-8 + inferencia conductual no medida); P-10 `NEW+NON_MATERIAL` (`README.md:128` «not shipped»; sin consecuencia concreta; no la considero `SPURIOUS` porque su premisa está anclada); R-1 `NEW+NON_MATERIAL` (el baseline no emite veredicto; su consecuencia es «no cambia»); R-3 `DERIVED+NON_MATERIAL` (B-1/B-2/B-6; eleva severidad, sin condición nueva). Las seis coinciden con el evaluador.

## 3. Trial #3: re-clasificación de categorías decisivas

| ID | Clase adjudicada | Ancla y razón |
|---|---|---|
| D-1 | `NEW+MATERIAL` | Baseline GAP-2 daba el consumo externo por ausente; `plans/160:19,43,61` consume `GOV-8`/`GOV-9`. Base de `(a)`; cambia el registro exigido. |
| D-4 | `NEW+MATERIAL` | Baseline no cita `RFC-75 Mec. 12` (`:327-339`: decisión arquitectónica persistente post-cierre → ADR). Cambia el vehículo (`Note` → ADR). |
| P-1a | `NEW+MATERIAL` | Ausente del baseline la consecuencia: el candidato no nombra acto, objeto ni fecha; `plan 152:572` (criterio 9) y `:530`. Condición/evidencia de `Accepted`. |
| P-3 | `NEW+MATERIAL` | Baseline sólo tenía el checkpoint y lo resolvía por el commit; el corpus nuevo (`plan 171:222`, `plan 153:30`, INDEX prosa vs tabla) muestra contradicción. `plan 152:645` dice `Executed`, no `Closed`. |
| P-7 | `NEW+MATERIAL` | Ausente del baseline: `_TEMPLATE:4-5` numera por fecha; ADR-19 (2026-10-07) vs ADR-20/21 (2026-10-20). Afecta identidad y campo `Fecha`. |
| P-8 | `NEW+MATERIAL` | Ausente del baseline: `plan 152:642-644` registra `ROADMAP_IMPACT = NOT_REQUIRED`; el candidato reconcilia la fila sin determinaciones. `CONVENTIONS §835`. |
| R-2 | `NEW+MATERIAL` | Ausente del baseline como prueba: ADR-19 registra diez `AE-*` con `Plan: plan 151` (`:4-6,92-96`); refuta la insatisfacibilidad. |
| D-3a | `DUPLICATE+MATERIAL` | Baseline B-4/B-6 ya invoca la elevación retrospectiva con la misma consecuencia (legalidad del vehículo). `ADR-16:74-78`. |
| P-6a | `DUPLICATE+MATERIAL` | Baseline B-2: `(c)` no se satisface; mismos hechos (`INV-1`/`INV-3` diferidos, `plan 152:7`) y consecuencia (criterio 1). |
| **P-4b** | **`DUPLICATE+MATERIAL`** (evaluador: `NEW+MATERIAL`) | Restituido a su contenido en `PROSECUTION_3 §P-4`: «si reproduce las diez decisiones, duplica el Plan». Baseline B-1 ya afirma que el Plan contiene fecha, actor, resultados, rationale y separación, y deriva dos registros. La etiqueta del evaluador le atribuía la tesis de R-1 (sólo el rationale), que es la que **refuta** a P-4. |
| **R-1** | **`DERIVED+MATERIAL`** (evaluador: `NEW+MATERIAL`) | Baseline B-1 enumera el contenido que el Plan ya tiene (incluido rationale); la inferencia de R-1 —sólo el rationale duplica, el resto es metadata— y la corrección por cláusula no estaban explicitadas. `plan 152:41,232`. |
| D-3b | `NEW+SPURIOUS` | «No producir ADR no tiene cláusula y debe inventar vehículo» es falso: `CONVENTIONS §390-421` define `Plan`/`Note` y el FRAME C especifica el artefacto. |
| P-1b | `NEW+SPURIOUS` | Dilema falso: `ADR-16:74-78` permite acto nuevo que eleve retrospectivamente; el candidato exige acto (prop. 1) y documenta el histórico (prop. 2). |
| P-2 | `DERIVED+SPURIOUS` | El Plan registra un **diferimiento**, no una decisión: `plan 152:155,530,656`; `F-1` `open`. La no-retroactividad ya está en la prop. 5. |
| P-4a | `NEW+SPURIOUS` | La disyuntiva «puntero o duplicado» omite la instancia `Accepted` de ADR-19 (diez `AE-*` + `Plan: 151`). |
| P-6b | `NEW+SPURIOUS` | `ADR-16:68-70` enumera «otra RFC, **otro Plan de evolución**, runtime…»; el Plan 160 es ese consumidor. La premisa «(a) exige RFC originante» es falsa. |
| P-9 | `NEW+SPURIOUS` | Hipotética sin condición («podría sustituir»), autoclasificada `SPECULATIVE`; §9 excluye «podría fallar» sin condición. |
| D-2 | `DERIVED+SPURIOUS` | La consecuencia «sin ADR sólo se puede apuntar a un Plan cerrado» es falsa: las reglas viven en `CONVENTIONS` Policy activa (§390-421/§447-476) y `plan 152:7` niega mecanismo/entidad/contrato nuevo. Evidencia mal leída. Es la llamada más discutible del evaluador; la sostengo. |

**Muestra restante (6/6):** D-5 `DERIVED+NON_MATERIAL` (baseline B-5 ya exige acto humano; simetría sin objeto nuevo); D-6 `DERIVED+NON_MATERIAL` (consecuencia ya cubierta por la prop. 2 del candidato); D-7 `DERIVED+NON_MATERIAL` (B-5; sin cambio de objeto); D-8 `DERIVED+NON_MATERIAL` (B-8 ya trataba coste/mantenimiento); P-5 `DERIVED+NON_MATERIAL` (ADR-19 agrupa diez `AE-*`; «desproporcionado» no se cuantifica); R-3 `DUPLICATE+NON_MATERIAL` (B-8). Las seis coinciden.

## 4. Matriz de confusión y discrepancias

**Trial #2** (24 occurrences = 24 distinct). Filas = evaluador; columnas = adjudicador.

| EVAL \ ADJ | NEW+MAT | DER+MAT | DUP+MAT | NEW+NON | DER+NON | DUP+NON | SPURIOUS |
|---|---:|---:|---:|---:|---:|---:|---:|
| NEW+MAT | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| DER+MAT | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| DUP+MAT | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| NEW+NON | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| DER+NON | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| DUP+NON | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| SPURIOUS | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

**Trial #3** (24 occurrences; el evaluador contó 23 distinct por dedupe). Filas = evaluador; columnas = adjudicador.

| EVAL \ ADJ | NEW+MAT | DER+MAT | DUP+MAT | DER+NON | DUP+NON | SPURIOUS |
|---|---:|---:|---:|---:|---:|---:|
| NEW+MAT | 7 | 1 | 1 | 0 | 0 | 0 |
| DUP+MAT | 0 | 0 | 2 | 0 | 0 | 0 |
| DER+NON | 0 | 0 | 0 | 5 | 0 | 0 |
| DUP+NON | 0 | 0 | 0 | 0 | 1 | 0 |
| SPURIOUS | 0 | 0 | 0 | 0 | 0 | 7 |

**Discrepancias de clasificación (4) y de dedupe (1).**

1. **T2 `P-6a`:** `NEW+MATERIAL` → `DERIVED+MATERIAL`. Ancla: `BASELINE_2 §6 B-5` («memoria entra como sufijo posterior al render»). El hecho está; la no-contabilización del budget es la consecuencia, no un hecho ausente. Sin cambio de materialidad.
2. **T2 `P-8`:** `NEW+MATERIAL` → `DERIVED+MATERIAL`. Ancla: `BASELINE_2 §8` («el plan 165 (que ya declaró FC-3 integrado)») + B-1. La inferencia «no era criterio pendiente» es nueva; el hecho no. Sin cambio de materialidad.
3. **T3 `P-4b`:** `NEW+MATERIAL` → `DUPLICATE+MATERIAL`. Ancla: `BASELINE_3 §6 B-1` (el Plan contiene fecha, actor, evidencia, diez resultados, rationale y separación; dos registros). El evaluador le atribuyó la tesis de R-1, que es la refutación de P-4. Sin cambio de materialidad.
4. **T3 `R-1`:** `NEW+MATERIAL` → `DERIVED+MATERIAL`. Ancla: `BASELINE_3 §6 B-1` enumera el contenido del Plan (incluido rationale); la restricción «sólo el rationale duplica» y la cláusula son inferencia. Sin cambio de materialidad.
5. **T3 dedupe:** `P-4b ≠ R-1` (ver §6); corpus 24 distinct, no 23.

No hay discrepancias de materialidad ni de `SPURIOUS` en las decisivas; las cuatro de novedad no alteran `DISTINCT_MATERIAL_NEW`.

## 5. Impacto potencial sobre la clase de cada trial (§13.2)

**Trial #2.** Flags con mi clasificación: `DISTINCT_MATERIAL_NEW = 9` (P-3, P-5b, P-6a, P-8 + D-4, D-6, P-7, P-9, R-2); `DECISIONAL_IMPACT = 0`; `PLAN_IMPACT = 2` (P-3, P-6a); `EVIDENCE_IMPACT = 2`; `COSTLY = SÍ` (4,01; 4,46 con 291 s); `DUPLICATE_SHARE = 11/24 = 0,4583`; `SPURIOUS_SHARE = 1/24 = 0,0417`; `VERY_REDUNDANT = NO`; `SPURIOUS_HIGH = NO`. `VALUE_CLASS = PLAN`; orden §13.2: `SUCCESS_PARTIAL` falla por `COSTLY` ⇒ **`POSITIVE_BUT_COSTLY`**. Mis dos discrepancias mueven `NEW+MAT` 4→2 y `DERIVED+MAT` 5→7, pero no `DMN` ni las shares ni `COSTLY`: **la clase no cambia**.

**Trial #3.** Flags con mi clasificación: `DISTINCT_MATERIAL_NEW = 8` (D-1, D-4, P-1a, P-3, P-7, P-8, R-2 + R-1); `DECISIONAL_IMPACT = 2`; `PLAN_IMPACT = 5`; `EVIDENCE_IMPACT = 2`; `COSTLY = SÍ` (5,21); `DUPLICATE_SHARE = 4/24 = 0,1667`; `SPURIOUS_SHARE = 7/24 = 0,2917`; `VERY_REDUNDANT = NO`; `SPURIOUS_HIGH = SÍ`. `VALUE_CLASS = DECISION`; `SUCCESS_STRONG` falla por `SPURIOUS_SHARE` y `COSTLY` ⇒ **`POSITIVE_BUT_COSTLY`**. El dedupe refutado sube `DUPLICATE_SHARE` de 0,130 a 0,1667 y baja `SPURIOUS_SHARE` de 0,304 a 0,2917; ninguna clase cambia porque `COSTLY` ya bloquea `SUCCESS_*`. Sensibilidad: si `D-2` fuera `MATERIAL`, `DMN = 9` y `SPURIOUS_SHARE = 0,25`; si `P-4b` fuera `NON_MATERIAL`, `DMN = 7`; en ambos casos la clase sigue `POSITIVE_BUT_COSTLY`. **Ninguna discrepancia cambia la clase de ningún trial según §13.2.** No emito decisión de campaña.

## 6. Dedupe cross-pass

**Trial #2 — confirmo 0 dedupe cross-pass.** Comparé las 24 ocurrencias por «misma afirmación + misma consecuencia»: las parejas temáticamente próximas no son el mismo distinct: D-1/P-8 (documentación vs necesidad), D-5/P-9 (autoridad preservada vs coste de gobernanza), D-3/D-6 (coste/reversión vs ownership), P-1/P-5 (actor/productor vs durabilidad), P-2/P-4 (schema vs elegibilidad), P-3/P-4 (`kind` vs lifecycle). Las coincidencias con B-1…B-8 son duplicados de **novedad**, no cross-pass.

**Trial #3 — refuto `P-4b ≡ R-1`.** La etiqueta del evaluador («sólo el rationale por decisión duplica; la frontera es una cláusula») es la tesis de **R-1**, no la de P-4. P-4 afirma que, si el ADR reproduce las diez decisiones, duplica el Plan y `CONVENTIONS`; su consecuencia es la insatisfacibilidad. R-1 afirma lo contrario en alcance: sólo el rationale duplica y el resto es metadata de identidad, resultados y regla de separación; su consecuencia es que la insatisfacibilidad cae y la corrección es una cláusula. Afirmaciones y consecuencias distintas ⇒ **2 distinct, 2 occurrences**. Consecuencia: corpus 24 distinct; `P-4b = DUPLICATE+MATERIAL`, `R-1 = DERIVED+MATERIAL`. No encontré otros duplicados: D-6 no se fusiona con R-1 (D-6 afirma la posibilidad de un registro acotado; R-1 localiza la frontera en el rationale); P-1a/P-7 (objeto del acto vs fecha/numeración); D-1/D-4 (`(a)` vs vehículo); R-2/D-5 (prueba de patrón vs simetría). No hay dedupe cross-trial: son corpus separados y el preregistro no lo define.

## 7. Notas del adjudicador (no findings del tratamiento)

- **Exhaustividad del baseline.** Ambos baselines contienen B-1…B-8 y condiciones: el patrón que §18 anticipa («casos pre-analizados»). Deprime la novedad por diseño; el valor nuevo se concentra en P-3, P-5b/P-6a/P-8 (T2) y D-1/D-4/P-1a/P-3/P-7/P-8 (T3).
- **Frontera de materialidad delgada.** D-6, P-9 y R-2 en T2, y D-5/D-6/D-7/D-8 en T3, están cerca de `NON_MATERIAL`; ninguna es `SPURIOUS`. El `SPURIOUS_SHARE` de T3 (7/24) es sensible al desdoblamiento (P-1b, P-4a y P-6b son astillas de objeciones más amplias): no debe leerse como siete objeciones independientes. D-7 (T2) es el único `SPURIOUS` con ancla central falsa; P-10 (T2) es débil pero anclada, y no la convertí en `SPURIOUS`.
- **D-2 (T3).** Coincido con el evaluador en `SPURIOUS`: el fallo no es que `(c)` sea juicio, sino que su consecuencia ignora `CONVENTIONS` como fuente activa. Si fuera `NON_MATERIAL`, `SPURIOUS_SHARE = 0,25`; clase igual.
- **Anclas.** Verifiqué las de las discrepancias (ver tablas). Ningún `MATERIAL` resultó falso en la dirección errónea.
- **Límites.** No medí presupuesto real (P-6a se calcula sobre constantes), no hay corrida con actor (P-6b), la colisión de P-3 es estructural y los ratios de coste son los del evaluador, no re-medidos. No emito `ADOPT`/`REFORMULATE`/`INCONCLUSIVE`/`REJECT`.


## Apéndice P — INTEGRITY AUDIT (verbatim)

# INTEGRITY AUDIT — Campaign Trials 2-3

## Metadata

- **Rol:** Integrity Audit de la campaña «Adversarial Deliberation» Trials #2 y #3. Contexto `fresh`; sólo lectura; única escritura, este archivo. **No emito la decisión de campaña (§14)**; verifico integridad metodológica contra el preregistro congelado y el ledger.
- **Repositorio:** rama `dev`, HEAD `d61e327`, árbol con dos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), no leídos.
- **STARTED:** 2026-10-25T14:27:23-03:00. **FINISHED:** 2026-10-25T14:38:00-03:00.
- **Archivos leídos:** preregistro §0–§20 y Apéndices A–C; `ledger.md`, `ledger.ps1`, `metrics_raw.md`, `appendix_c.md`, `ADJUDICATION.md`; los doce artefactos de trial y los dos frames; `docs/working/research/INDEX.md`; `docs/plans/INDEX.md` (fila y prosa del Plan 152); `ROADMAP.md`; `.gitignore`; Git de consulta. **No** leí `review/` ni los untracked del mantenedor; sin `pytest`.
- **Llamadas a herramientas:** 45 aprox. **[SELF-DECLARED]**; sin web ni `git add/commit`.

## 1. Hashes y ledger

Recalculé SHA-256 de los quince artefactos congelados (doce de trial, dos frames, adjudicación). Todos coinciden con el ledger y los diez de `metrics_raw.md` con ese archivo.

| Artefacto | SHA-256 actual |
|---|---|
| BASELINE_2 | `3BA05908330D170C8AAFD0DA5436E5B15C380657024A00F4C467C5258848AE8F` |
| DEFENSE_2 | `D46CE1EE75F2F7C704119A83B3A825D492B6FABDC2E90CF39B2B9A3B9F05F772` |
| PROSECUTION_2 | `B2DB9375BB8045E4707FFD304A00DA5B2ED9D1FA56473D5F093841C182D4EBE5` |
| SYNTHESIS_2 | `34737E508B1FC0DFD401A572F7A3853E1329A50BC234DED4D194CE5DBDB6644B` |
| REBUTTAL_2 | `4345A881F81FD56BAC2BAD4875D412EB71E27D5CD96E58AB3427C23D4607AEFB` |
| EVALUATION_2 | `68789DC2159B4B1E06003B64383CDA7A0316070F90CFB9A93B7BA933AAB37E41` |
| BASELINE_3 | `52B45433FBD68322F204C57E9530DEC0C17823F5C194C7CB9CC3FDE4B2F1B643` |
| DEFENSE_3 | `23BA40844030D40A86F6121225E27E2AB59EA71208F5B8DC1ECDD6D39A00F837` |
| PROSECUTION_3 | `08228EEDE7B044F90E2CC0C1759B400C2E3D761D1AC95657D2D36F3DF86143A5` |
| SYNTHESIS_3 | `22338229273C36704F31E077364F4DD013F866C72B1B913286246C506721B4AE` |
| REBUTTAL_3 | `81705E05F0B1BC74403651B5C2CB75EE34C7C1B5ED73F0F14D2966E60002B98B` |
| EVALUATION_3 | `3FE78C28840394A67F2064B893E2CA481A75D19BFEA7096E9B86079E6D7C848E` |
| FRAME-2 / FRAME-3 | `A64AE4AD…F359EBE0C2` / `9674C3DF…BD24476865` |
| ADJUDICATION | `2A0534C94E39CEE605E90A9046AE5885FF14C0C547270ED94E3DDA63EE7BD6FB` |

**Caso `[003]`→`[004]`.** `[003]` (13:37:01) registró `967D855E…`/`80C0F6A5…`, 2.395/2.455 palabras y cierres 13:36:33/13:36:23; `[004]` (13:45:34) registra los finales `3BA05908…`/`52B45433…`, 2.198/2.195 palabras y cierres 13:38:35/13:38:21, y declara edición posterior a la primera escritura. La diferencia de palabras prueba que `[003]` no describía el artefacto final; `[003]` no se editó y `[004]` la supersede append-only. Correcto en forma, **pero el baseline fue reescrito después de un hash registrado** (§4).

**Hashes citados por las evaluaciones.** EVALUATION-2 y EVALUATION-3 citan los seis hashes de su trial y todos coinciden; SYNTHESIS/REBUTTAL ídem. ADJUDICATION no cita ninguno (**GAP-1**; §7 no lo exige).

**Cadena del ledger.** Recalculé SHA-256 de cada línea `[NNN]` (UTF-8, sin salto): los `hash=` registrados coinciden con el cálculo y el `prev` de `[002]`…`[011]` coincide con el hash de la entrada anterior. `[000]` calcula `6a4316…` y `[001]` lo registra como `LEDGER_HASH_000`; `[001]` carece de `prev`/`hash` propios, pero su hash (`5ef6f0…`) es el `prev` de `[002]`: el eslabón se verifica por contenido (**GAP-2**, forma).

**[011].** `[011]` (14:33:42, `INTEGRITY_AUDIT_CLOSED`) encadena bien con `[010]`, pero registra `integrity_sha256=69CDBA79…` y «`words=19050_bytes`» para un `INTEGRITY_AUDIT.md` que no existía al iniciar esta auditoría (14:27) y que hoy es otro contenido (2.486 palabras, SHA-256 informado al Lead). `trials_body.md:36` repite 1.724 palabras/`69CDBA79…`. **GAP-7 / D-n.**

**Ítem 1: PASS** (GAP-1, GAP-2, GAP-7).

## 2. Orden y commit-before-reveal

| Evento | Trial #2 | Trial #3 |
|---|---|---|
| Lanzamiento baselines | 13:33:44 [003] | 13:33:44 [003] |
| Baseline FINISHED | 13:38:35 | 13:38:21 |
| Defense STARTED / FINISHED | 13:37:18 / 13:44:20 | 13:37:19 / 13:41:20 |
| Prosecution STARTED / FINISHED | 13:45:48 / 13:51:14 | 13:45:48 / 13:56:00 |
| Reveal | 13:56:30 ([006] 13:57:06) | ídem |
| Synthesis STARTED / FINISHED | 13:57:23 / 14:02:00 | 13:57:20 / 14:04:30 (mtime 14:03:52) |
| Rebuttal STARTED / FINISHED | 14:04:25 / 14:06:35 | 14:04:25 / 14:06:50 |
| Evaluation / Adjudication | 14:09:07–14:16:39 / 14:18:37 | 14:09:07–14:16:05 |

- **FAIL — baseline→defensa:** la defensa arrancó 77 s (T2) y 62 s (T3) antes del `FINISHED` del baseline. El hash final no se registró hasta `[004]` (13:45:34), después de que ambas defensas cerraran; al lanzarlas, la única versión hasheada era `[003]`, no la final. §17.1 no se cumple.
- **PASS — defensa→prosecución:** ambas defensas cerraron antes de 13:45:48; las dos prosecuciones se lanzaron en el mismo batch, ya cerradas, en directorios separados.
- **PASS — reveal→síntesis:** reveal 13:56:30, entrada `[006]` 13:57:06, síntesis 13:57:20/23; ambas verifican los hashes de las posiciones.
- **PASS con anomalía — síntesis→rebuttal:** T2 14:02:00 < 14:04:25. En T3 la síntesis declara `FINISHED` 14:04:30, 5 s después del `STARTED` del rebuttal, pero su mtime es 14:03:52 y `[007]` registra su hash a las 14:04:14, antes del rebuttal: la anomalía es del timestamp declarado, no del orden.
- **PASS — sin reescritura posterior:** hash actual = registrado y todos los mtime preceden a su entrada de ledger (defensas 13:44:24 < 13:45:35; prosecution-2 13:51:17 < 13:57:06; síntesis-2 14:02:10 < 14:04:14; rebuttal-2 14:06:45 < 14:08:44; evaluaciones 14:16:45/14:15:59 < 14:18:37; adjudicación 14:25:06 < 14:27:23). Excepción: el baseline (`[003]`→`[004]`).

**Otras anomalías:** `[007]` precede al `FINISHED` de SYNTHESIS-3; SYNTHESIS-2: 14:02:00 vs mtime 14:02:10; typo `PROCECUTION_2.md`.

**Ítem 2: FAIL** (sólo baseline→defensa y registro del hash final; resto PASS).

## 3. No contaminación

- **Referencias cruzadas:** grep de los doce artefactos por `trial<otro>`, los artefactos del otro trial y `Trial #1`: **cero coincidencias**.
- **Declaraciones de lectura:** baseline-2 declara no leídos preregistro, Trial #1 y «otros trials»; defense-2 y prosecution-2, no leído el baseline ni la posición contraria; synthesis-2, sólo sus cuatro piezas; ídem en T3. Ningún `Archivos leídos` incluye `.project/campaign/trial<otro>/`.
- **Exposiciones declaradas, no silenciosas:** DEFENSE-2 declara que un `git grep` devolvió dos líneas del preregistro, que no abrió ni citó; REBUTTAL-2 declara haber leído `DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md`, fuera de los 15 ítems del FRAME pero dentro de la clase admitida y sin que ninguna conclusión dependa. Ninguna es lectura del otro trial.
- **No verificado:** la defensa declara no haber leído el baseline y no cita su contenido; *atested, not enforced* (§4.3) (**GAP-3**).

**Ítem 3: PASS** (GAP-3).

## 4. Baseline congelado y desviaciones

El contenido de comparación es el hash final (`[004]`), no modificado tras su registro (mtimes 13:38:31/13:38:23 < 13:45:34; hash coincide). **La congelación de contenido es correcta**; falla la **secuencia de cierre**: el baseline no quedó cerrado antes del tratamiento y su hash final se registró después.

**¿Invalida el trial?** Recomiendo **D2**, no D3: (i) el baseline (13:38:35/13:38:21) precede a la finalización de las defensas (13:44:20/13:41:20); (ii) ninguna pasada analítica lo recibió —sólo la síntesis, ya cerrado y hasheado—; (iii) el hash de comparación es el final, registrado antes del reveal (13:56:30). Es un defecto de registro/orden, no de contaminación. **Riesgo residual:** si el Lead lee literalmente §16 («artefacto reescrito después del hash» ⇒ D3), `[003]`→`[004]` activaría D3, ambos trials serían `INVALID_TRIAL` y la campaña `CAMPAIGN_INVALID`; es la única frontera D2/D3; debe registrarse.

**Ítem 4: FAIL en el gate de cierre; PASS en contenido congelado** (D2 recomendada).

## 5. Conteos, dedupe y doble conteo

**Trial #2.** 24 occurrences = 24 distinct (8 D + 13 P + 3 R). NEW 6 / DER 7 / DUP 11; MAT 17 / NON 6 / SPUR 1; NEW+MAT 4, DER+MAT 5, DUP+MAT 8; `DISTINCT_MATERIAL_NEW` 9 (Def 2, Pros 6, Reb 1). Shares 11/24 = **0,4583**; 1/24 = **0,0417**. Contra la tabla de EVALUATION-2: **PASS**; sin doble conteo (D-7 es `DUPLICATE+SPURIOUS`, permitido por la matriz 3×3 y contado una vez por dimensión).

**Trial #3, evaluador.** 24 occurrences, 23 distinct (`P-4b≡R-1`): NEW 13 / DER 7 / DUP 3; MAT 10 / NON 6 / SPUR 7; NEW+MAT 8, DER+MAT 0, DUP+MAT 2; DMN 8; shares 3/23 = **0,1304** y 7/23 = **0,3043**. Aritmética: **PASS**.

**Dedupe: el evaluador se equivocó; el adjudicador tiene razón.** P-4 concluye insatisfacibilidad («puntero o duplicado», PROSECUTION_3:46-53); R-1 sostiene lo contrario —sólo el `rationale` duplica— (REBUTTAL_3:40). El evaluador atribuyó a P-4b la tesis de R-1, que es su refutación. Corpus correcto: **24 distinct**; DUP+MAT 3, DER+MAT 1 (R-1), DMN 8; shares **4/24 = 0,1667** y **7/24 = 0,2917**. **Efecto: DMN 8→8, shares cambian, clase intacta.**

**Ítem 5: FAIL en T3 (dedupe); PASS en T2 y totales.**

## 6. Cálculos y costes

**Palabras:** los doce artefactos coinciden exactamente con `metrics_raw.md` (2.198/2.275/2.277/2.994/1.481; 2.195/2.296/2.300/2.712/1.485; evaluaciones 3.996/3.447; adjudicación 2.500). Tratamiento T2 = **9.027** (ratio 4,1069); T3 = **8.793** (4,0059). **PASS.**

**Ratios (§11).** Reportados: T2 SELF 4,0104 / LEAD 3,1178 (416) / EFFECTIVE 4,01; T3 5,2117 / 3,5192 (416) / 5,21. Con los timestamps reales (lanzamiento 13:33:44 → cierre 13:38:35/13:38:21): T2 LEAD 1.297/291 = **4,4570** y EFFECTIVE **4,46**; T3 LEAD 1.464/277 = **5,2852** y EFFECTIVE **5,29**. `COSTLY` sigue SI; **el reportado no es el conservador**: §11 exige el mayor y el LEAD supera al SELF.

**`416`.** No está en el ledger ni en los baselines (que no declaran `LEAD_WALL_S`); la afirmación de EVALUATION-2 de que «BASELINE_2 declara 416» es falsa. El mismo valor para cierres distintos es implausible. **GAP-4.**

**`LEAD_WALL_S < SELF_S`.** REBUTTAL-3: 130 < 145; 130 es idéntico al LEAD de REBUTTAL-2 (arrastre). Con 145, `TREATMENT_LEAD` = 1.479 y LEAD/277 = **5,339**; clase sin cambio. **D2.**

**Eficiencia:** 6,939/7,792 (T2) y 5,464/5,602 (T3) DMN por 1.000 s. **PASS.** **GAP-5:** las duraciones por pasada no están en el ledger; verifico contra los insumos, no contra el ledger.

**Ítem 6: PASS aritmético; FAIL de procedencia (416, datos no auditables)**.

## 7. Clases de trial y casos sintéticos

§13.2 en orden: **T2** (DMN 9, DECISIONAL 0, PLAN 2, DUP 0,4583, SPUR 0,0417, COSTLY): 1–6 no, **7 POSITIVE_BUT_COSTLY**. **T3** (DMN 8, DECISIONAL 2, PLAN 5, DUP 0,1304, SPUR 0,3043, COSTLY): 1–3 no (SPUR > 0,10 y COSTLY), 4–6 no, **7 POSITIVE_BUT_COSTLY**. Con los valores del adjudicador (T3 DUP 0,1667, SPUR 0,2917) idéntico: **es la primera clase que se cumple en ambos trials y con ambas clasificaciones.** **PASS.**

**Apéndice C.7: GAP-6.** El preregistro promete una «tabla de decisión sintética» (§13.2; §17.7; C.5-18), pero el Apéndice C termina en C.6: no existe C.7 en el documento congelado, `appendix_c.md` ni `prereg_body_v2.md`. El control comprometido **no fue entregado**; lo reconstruí. Casos (8 + 2 variantes), todos PASS:

| Caso | Entradas | Clase esperada | Resultado |
|---|---|---|---|
| S-1 | D3 declarada | INVALID_TRIAL | ✓ |
| S-2 | DMN 0, DUP 0,80, SPUR 0,20, COSTLY | NEGATIVE | ✓ |
| S-3 | DMN 3, DEC 2, DUP 0,40, SPUR 0,05 | SUCCESS_STRONG | ✓ |
| S-4 | DMN 4, PLAN 2, DUP 0,60, SPUR 0,10 | SUCCESS_PARTIAL | ✓ |
| S-5 | DMN 2, EVID 1, DUP 0,50, SPUR 0,10 | SUCCESS_EVIDENCE | ✓ |
| S-6 | DMN 0, DUP 0,20, SPUR 0 | NO_EVIDENCE | ✓ |
| S-7 | DMN 5, PLAN 1, DUP 0,70, COSTLY | POSITIVE_BUT_COSTLY | ✓ |
| S-8 | DMN 3, PLAN 1, DUP 0,20, SPUR 0,12 | POSITIVE_BUT_SPURIOUS | ✓ |
| S-4b | DMN 1, PLAN 1, DUP 0,65 | POSITIVE_BUT_REDUNDANT | ✓ |
| S-6b | DMN 1, sin impacto, DUP 0 | INCONCLUSIVE_TRIAL | ✓ |

S-6b expone un hueco: con `DISTINCT_MATERIAL_NEW ≥ 1` y los tres impactos en 0, §13.2 no asigna `VALUE_CLASS`; la clase 10 lo captura (`INCONCLUSIVE_TRIAL`), así que las clases son exhaustivas pero `VALUE_CLASS` no (**GAP-6b**).

**Ítem 7: PASS** con GAP-6/GAP-6b.

## 8. Inventario de desviaciones (D1/D2/D3 recomendada)

| # | Desviación | Clase | Efecto |
|---|---|---|---|
| D-a | Solapamiento baseline→defensa (T2 77 s, T3 62 s) y hash final del baseline registrado tras cerrar las defensas | **D2** | Gate §17.1 incumplido; sin contaminación demostrable; clase intacta; frontera D3 |
| D-b | `[003]`→`[004]`: baseline reescrito tras un hash registrado | **D2** | Idem; `[003]` superseded, no editada; comparación con hash final |
| D-c | T3: `SYNTHESIS FINISHED` 14:04:30 > `REBUTTAL STARTED` 14:04:25, contra mtime 14:03:52 y hash `[007]` 14:04:14 | D1 | Orden verificado por hash; timestamp declarado erróneo |
| D-d | DEFENSE-2: un `git grep` devolvió dos líneas del preregistro | D1 | Declarado, no abierto ni citado; sin traza en el artefacto |
| D-e | REBUTTAL-2 leyó `DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md`, fuera de la base de 15 ítems | D1 | Declarado; dentro de la clase admitida; ninguna conclusión depende |
| D-f | FRAME-3 sobreafirma el cierre del Plan 152 («`Executed`/`Closed`; INDEX, fila 152»): la fila dice `Executed`; la prosa `Closed` contradice el checkpoint | **D2** | Premisa no unívoca en todas las pasadas; sostiene P-3/P-4; no invalida |
| D-g | `LEAD_WALL_S` del baseline = 416 en ambos trials, contra 291/277 de los timestamps; no está en el ledger | **D2** | EFFECTIVE subestimado (4,01→4,46; 5,21→5,29); COSTLY y clase intactos |
| D-h | REBUTTAL-3 `LEAD_WALL_S` 130 < `SELF_S` 145 | **D2** | Coste de tratamiento subestimado en 15 s; clase intacta |
| D-i | Frames congelados sobre `e7bc881`, ejecución sobre `d61e327` | D1 | Delta docs-only (preregistro + INDEX); sin cambio de evidencia |
| D-j | Apéndice C.7 (tabla sintética) prometido y ausente | **D2** | Control no entregado; reconstruido; sin efecto en métricas |
| D-k | EVALUATION-3 dedupe erróneo `P-4b≡R-1` | **D2** | Corpus 23→24; DUP 0,130→0,167; SPUR 0,304→0,292; DMN 8→8 |
| D-l | EVALUATION-2 atribuye a BASELINE-2 una declaración de 416 que no existe | D1 | Error de ancla documental; vinculado a D-g |
| D-m | BASELINE-2 `B-7` da por inexacta la fila `AE-8`, que es exacta | D1 | Retractado en SYNTHESIS-2; sin efecto de clase |
| D-n | `[011]` y `trials_body.md` citan `69CDBA79…`/1.724 palabras para la auditoría; el artefacto entregado tiene 2.486 palabras y otro SHA-256 | **D2** | Registro irreproducible; corregir con entrada append-only y Apéndice P verbatim |

**Ningún D3.** Ninguna desviación invalida la campaña: no hay baseline contaminado, reveal violado, taxonomía inconsistente sin adjudicación, evidencia inventada ni reescritura posterior al hash **final**. D-a/D-b son la frontera D2/D3 y el Lead debe registrarla con su lectura.

**Ítem 8: PASS** (inventario completo y clasificado).

## 9. Trazabilidad Git

`git log --oneline -3` → `d61e327`, `e7bc881`, `b6843bc`. `d61e327` (13:33:20) contiene **sólo** el preregistro (744 líneas) y `docs/working/research/INDEX.md` (+2/−1; 746 inserciones, 1 deleción), lo declarado en §20.1; se creó 24 s antes de lanzar los baselines (13:33:44): congelamiento pre-ejecución. El hash del preregistro (working y blob) es `0E166E8F…` y coincide con `[000]`/`[002]`. `git status --porcelain` sólo muestra los dos untracked declarados; no hay archivos versionados modificados. `git diff --stat e7bc881 d61e327` = 2 archivos, 746/1, sin cambios en `runtime/`, `tests/`, `tools/` ni `docs/` sustantivo. **PASS.**

## 10. Veredicto de integridad

| Ítem | Resultado |
|---|---|
| 1 Hashes y ledger | PASS (GAP-1, GAP-2) |
| 2 Orden y commit-before-reveal | **FAIL** (baseline→defensa; hash final tardío) |
| 3 No contaminación | PASS (GAP-3) |
| 4 Baseline congelado | **FAIL** de secuencia (D2); contenido PASS |
| 5 Conteos y dedupe | **FAIL** en T3 (D-k); T2 y totales PASS |
| 6 Cálculos y costes | **FAIL** de procedencia (D-g, D-h); aritmética PASS |
| 7 Clases y sintéticos | PASS (GAP-6, GAP-6b) |
| 8 Desviaciones | PASS (14 inventariadas, sin D3) |
| 9 Trazabilidad Git | PASS |
| 10 Ledger | PASS (cadena íntegra) |

La campaña es **legible y reproducible**: hashes finales verificados, cadena del ledger íntegra, sin contaminación detectable, conteos y clases recomputados, y las discrepancias evaluador/adjudicador no alteran ninguna clase. Las limitaciones son de **registro y procedencia de costes**, no de identidad ni de la regla; incorporan la frontera D2/D3 del baseline, el control sintético ausente y el registro de auditoría divergente.

**CAMPAIGN_INTEGRITY = VALID_WITH_LIMITATIONS**


## Apéndice Q — Ledger de la campaña (snapshot append-only)

> Snapshot tomado al ensamblar este registro (entradas `[000]`–`[012]`). Las entradas posteriores del ledger —el cierre `[013]` con el hash del commit 2 y la corrección final `[014]` con el hash de este archivo— son append-only y viven en `.project/campaign/ledger.md` (gitignored); no se incorporan aquí para no introducir una segunda fuente ni una auto-referencia. El ledger original conserva la misma forma y la misma cadena `prev`/`hash`.

[000] 2026-10-25T13:33:14.2238100-03:00 | GENESIS | prereg_sha256=0E166E8F10F7F06207063B5F2A0C7F9FD3C2639F7C078DDF066D9DA33B8B37AE frame2_sha256=A64AE4ADBF1C550019A742F036FBA55AF797B926F87740EA5BAC80F359EBE0C2 frame3_sha256=9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865 prev=0000000000000000000000000000000000000000000000000000000000000000
[001] 2026-10-25T13:33:14.2238100-03:00 | LEDGER_HASH_000=6a431651b88df93513ceb6be8dda1ac5ee16c820fff7f8115f37a1ecd1e37bad
[002] 2026-10-25T13:33:30.7717977-03:00 | COMMIT_1 | prereg_commit=d61e3270cfa93c9bb62cdf6f68fc297e7043a1f2 prereg_working_sha256=0E166E8F10F7F06207063B5F2A0C7F9FD3C2639F7C078DDF066D9DA33B8B37AE | prev=5ef6f05378bfa6b59221df973ee4c1d9ac83bcd115973b61ef26fb3954924921
    hash=d45421059ab41c2c09a6673ce3dd9a2bc7e6ae59dfad4454f7ba77c388e6616c
[003] 2026-10-25T13:37:01.2810396-03:00 | BASELINES_CLOSED | launch=2026-10-25T13:33:44-03:00 baseline2_sha256=967D855E0D10E8B04849E9460808C83F169C72DDD293CB47ECB67A55BBDE3057 baseline2_words=2395 baseline2_finished=2026-10-25T13:36:33-03:00 baseline3_sha256=80C0F6A51A35E7F0BA840F8AECEF10437DFB1185C16A17C8BA6D35ADF7C2ABD7 baseline3_words=2455 baseline3_finished=2026-10-25T13:36:23-03:00 receipt_observed=2026-10-25T13:37:00-03:00 | prev=d45421059ab41c2c09a6673ce3dd9a2bc7e6ae59dfad4454f7ba77c388e6616c
    hash=0c50205913575dd045e323cb2170bf500c3de7f0e507bfffd9add1897167d8fd
[004] 2026-10-25T13:45:34.9960875-03:00 | BASELINES_FINAL_CORRECTION_D2 | correction: earlier entry [003] recorded pre-final hashes; passes continued editing after first write. FINAL baseline2_sha256=3BA05908330D170C8AAFD0DA5436E5B15C380657024A00F4C467C5258848AE8F words=2198 finished=2026-10-25T13:38:35-03:00; FINAL baseline3_sha256=52B45433FBD68322F204C57E9530DEC0C17823F5C194C7CB9CC3FDE4B2F1B643 words=2195 finished=2026-10-25T13:38:21-03:00; defense launch=2026-10-25T13:37:16-03:00 preceded baseline finalization; deviation D2 registered (baseline not modifiable by treatment; defenses blind to baseline; final baseline hashes used; stale entry [003] superseded, not edited) | prev=0c50205913575dd045e323cb2170bf500c3de7f0e507bfffd9add1897167d8fd
    hash=f155ff200fe505bc8914051f37ae5094316a7bdf323861c7bf3ea76b188146d7
[005] 2026-10-25T13:45:35.0211043-03:00 | DEFENSES_CLOSED | defense2_sha256=D46CE1EE75F2F7C704119A83B3A825D492B6FABDC2E90CF39B2B9A3B9F05F772 words=2275 finished=2026-10-25T13:44:20-03:00 position=SUPPORT_WITH_CONDITIONS; defense3_sha256=23BA40844030D40A86F6121225E27E2AB59EA71208F5B8DC1ECDD6D39A00F837 words=2296 finished=2026-10-25T13:41:20-03:00 position=SUPPORT_WITH_CONDITIONS; deviation D1: defense2 declares a git grep returned two lines of the preregistration; declares not used/cited | prev=f155ff200fe505bc8914051f37ae5094316a7bdf323861c7bf3ea76b188146d7
    hash=7caf4d90ad59bebeb246a9265881e4d0e704c5d6de5fc0d14eb823e33a105f54
[006] 2026-10-25T13:57:06.5091687-03:00 | REVEAL | reveal_ts=2026-10-25T13:56:30-03:00 trial2: defense_sha256=D46CE1EE75F2F7C704119A83B3A825D492B6FABDC2E90CF39B2B9A3B9F05F772 prosecution_sha256=B2DB9375BB8045E4707FFD304A00DA5B2ED9D1FA56473D5F093841C182D4EBE5; trial3: defense_sha256=23BA40844030D40A86F6121225E27E2AB59EA71208F5B8DC1ECDD6D39A00F837 prosecution_sha256=08228EEDE7B044F90E2CC0C1759B400C2E3D761D1AC95657D2D36F3DF86143A5; positions closed before reveal | prev=7caf4d90ad59bebeb246a9265881e4d0e704c5d6de5fc0d14eb823e33a105f54
    hash=27a601db5f642069fcfad7a8b8c3999d202ab188eb992843aa28ff1ce3950928
[007] 2026-10-25T14:04:14.5561044-03:00 | SYNTHESES_CLOSED | synthesis2_sha256=34737E508B1FC0DFD401A572F7A3853E1329A50BC234DED4D194CE5DBDB6644B words=2994 finished=2026-10-25T14:02:00-03:00 verdict=NOT_VIABLE recommendation=REVISE rebuttal=S_I(P-1); synthesis3_sha256=22338229273C36704F31E077364F4DD013F866C72B1B913286246C506721B4AE words=2712 finished=2026-10-25T14:04:30-03:00 verdict=VIABLE recommendation=REVISE rebuttal=S_I(P-4) | prev=27a601db5f642069fcfad7a8b8c3999d202ab188eb992843aa28ff1ce3950928
    hash=fe4761e14168871799df4a01710c6fec4093edec65fb738883a6cace7307d9ed
[008] 2026-10-25T14:08:44.4899019-03:00 | REBUTTALS_CLOSED | rebuttal2_sha256=4345A881F81FD56BAC2BAD4875D412EB71E27D5CD96E58AB3427C23D4607AEFB words=1481 finished=2026-10-25T14:06:35-03:00 changes_verdict=NO changes_recommendation=NO; rebuttal3_sha256=81705E05F0B1BC74403651B5C2CB75EE34C7C1B5ED73F0F14D2966E60002B98B words=1485 finished=2026-10-25T14:06:50-03:00 changes_verdict=NO changes_recommendation=NO | prev=fe4761e14168871799df4a01710c6fec4093edec65fb738883a6cace7307d9ed
    hash=7351a88a5f800adce713ce84cde7cf873e5fde93560a4e7948e16b350a045065
[009] 2026-10-25T14:18:37.6902047-03:00 | EVALUATIONS_CLOSED | evaluation2_sha256=68789DC2159B4B1E06003B64383CDA7A0316070F90CFB9A93B7BA933AAB37E41 words=3996 finished=2026-10-25T14:16:39-03:00 class=POSITIVE_BUT_COSTLY value=PLAN distinct_material_new=9 dup_share=0.458 spurious_share=0.042; evaluation3_sha256=3FE78C28840394A67F2064B893E2CA481A75D19BFEA7096E9B86079E6D7C848E words=3447 finished=2026-10-25T14:16:05-03:00 class=POSITIVE_BUT_COSTLY value=DECISION distinct_material_new=8 dup_share=0.130 spurious_share=0.304 | prev=7351a88a5f800adce713ce84cde7cf873e5fde93560a4e7948e16b350a045065
    hash=52dffb727ef3ecbf7c411f2a3f73f1c19f28dcc70f1a1cad44c50c23f2a08bd9
[010] 2026-10-25T14:27:23.8029959-03:00 | ADJUDICATION_CLOSED | adjudication_sha256=2A0534C94E39CEE605E90A9046AE5885FF14C0C547270ED94E3DDA63EE7BD6FB words=2500 finished=2026-10-25T14:24:51-03:00 discrepancies=T2:2(P-6a,P-8 NEW->DERIVED) T3:2 novelty(P-4b NEW->DUP,R-1 NEW->DERIVED)+1 dedupe(P-4b!=R-1) classes_unchanged=YES | prev=52dffb727ef3ecbf7c411f2a3f73f1c19f28dcc70f1a1cad44c50c23f2a08bd9
    hash=d3a4cc160788962ab3b4754ad3af98c445c97469b4fca6b563a5bca4bf7c0c76
[011] 2026-10-25T14:33:42.3234986-03:00 | INTEGRITY_AUDIT_CLOSED | integrity_sha256=69CDBA79F9ACB913E788347E41FB2179334847B80DD67565AC81D89E5DFCFCEB words=19050_bytes finished=2026-10-25T14:34:00-03:00 verdict=VALID_WITH_LIMITATIONS D2_recommended=D-a,D-b,D-f,D-g,D-h,D-j,D-k D3=NONE | prev=d3a4cc160788962ab3b4754ad3af98c445c97469b4fca6b563a5bca4bf7c0c76
    hash=eb4bba3e434ebcc2cc654cede5d95796b914c737b1e4ed959049573adcdd5533
[012] 2026-10-25T14:43:48.9116546-03:00 | INTEGRITY_AUDIT_HASH_CORRECTION_D2 | entry [011] recorded stale hash 69CDBA79F9ACB913E788347E41FB2179334847B80DD67565AC81D89E5DFCFCEB while the artifact was still being written; FINAL integrity_audit_sha256=3DFEA98E2A2E2DAEF4E7173371CCD6169DE69E1584E8A66BAFDF11424FC7CA20 words=2486 verdict=VALID_WITH_LIMITATIONS; [011] superseded, not edited; trials_body must cite final hash | prev=eb4bba3e434ebcc2cc654cede5d95796b914c737b1e4ed959049573adcdd5533
    hash=7c1238249b903005176b7010829fed7cfe2d16e13c5072063ff84d7bfd7550ce


