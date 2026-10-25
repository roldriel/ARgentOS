# Preregistro congelado — Campaña «Adversarial Deliberation», Trials #2 y #3

> **Naturaleza:** Working / experimental (`docs/working/research/`). **No normativo.** Es protocolo experimental y provenance; nunca autoridad.
> **Origen:** instrucción directa del mantenedor del 2026-10-25 (campaña de replicación controlada Trial #2 + Trial #3, posterior al Trial #1 registrado en `ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md`).
> **Estado:** `PREREGISTRO CONGELADO` en el commit 1, que se crea **antes** de ejecutar cualquier pasada de Trial #2 o Trial #3 (evidencia: orden de commits de Git). El estado `DRAFT` y la revisión independiente pre-ejecución quedan registrados en el Apéndice C.
> **Contención:** este documento no modifica `protocol/`, `.agents/`, el runtime ni `docs/VERSIONING.md`; no crea mecanismos, estados, gates, governance ni autoridad. Es evidencia experimental.
> **Regla de oro:** ninguna regla de este documento se adapta después de observar resultados. Ver §14.1 y §16.

## 0. Metadata, autorización y clasificación del Change

- **Campaña:** Adversarial Deliberation — Trials #2 y #3 (replicación controlada de método + caso independiente).
- **Fecha de congelación:** `2026-10-25` (America/Buenos_Aires), antes de la primera pasada de evaluación de cualquiera de los dos trials.
- **Repositorio:** rama `dev`, HEAD `e7bc8818afed903cfc327cb98a2fcfbf7a9789ee`. Árbol con dos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), preservados y **no** leídos como evidencia.
- **Protocolo previo:** `ADVERSARIAL_DELIBERATION_EXPERIMENT_2026-10-25.md` (protocolo del mantenedor, Working) y `ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md` (resultado del Trial #1). Este preregistro **no** reescribe el Trial #1; lo usa sólo como evidencia para diseñar mejor las pruebas.
- **Ejecutores:** el Lead (diseño, frames, revelación, ledger, análisis cross-trial, decisión) y pasadas en **contextos `fresh` independientes** (sin historia de conversación) para BASELINE, DEFENSE, PROSECUTION, SYNTHESIS, REBUTTAL (si se dispara), EVALUATION, ADJUDICATION e INTEGRITY AUDIT de cada trial. Mismo modelo (`deepseek-flash`) en todas las pasadas; la limitación se declara (§18).
- **Artefactos de sesión:** `.project/campaign/` (gitignored por `.gitignore:13`), no versionados por diseño. Los textos completos se incorporan verbatim como apéndices del registro de trials; los hashes SHA-256 permiten verificar la identidad de lo comprometido.
- **Artefactos versionados de la campaña:** este preregistro (commit 1, antes de ejecutar) y el registro `ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md` (commit 2, después de ejecutar), más las filas correspondientes en `docs/working/research/INDEX.md`.
- **Hashes de los frames congelados** (los mismos que se entregan a las pasadas; los frames verbatim están en Apéndices A y B):

```text
FRAME-2 (Case-02, Memory)                 SHA-256 = A64AE4ADBF1C550019A742F036FBA55AF797B926F87740EA5BAC80F359EBE0C2
FRAME-3 (Case-03, ADR-worthiness)         SHA-256 = 9674C3DF6BBDDEFAF48BCC90269EC9E15914C6873EDCBA330700E6BD24476865
```

- **Autorización y clasificación (RFC-75 Mecanismo 1; `.agents/AGENTS.md`):** **Origen** = acción directa del mantenedor (la instrucción describe la campaña completa e indica ejecutarla). **RFC-56 Class: N/A** (sin payload delta). **Change Level: L1** (coordination 0: un escritor de artefactos versionados, el Lead, con escrituras delegadas sólo en `.project/` gitignored; scope 1: un área documental, `docs/working/research/`; architectural 0; release 0; duration 0: una sesión de trabajo, con ejecución paralela acotada). **Dominio:** DEV docs. **Sin Plan**: la instrucción directa autoriza el Change que nombra y el Change se registra por su primer artifact + commits (precedente del Trial #1, commit `e7bc881`).
- **Sin cambios fuera del registro:** `protocol/`, `.agents/`, `dist/`, `runtime/`, `tools/`, `tests/`, `docs/VERSIONING.md`, `ROADMAP.md`, `CHANGELOG.md`, RFCs, ADRs y planes quedan intactos. Los subagentes tienen prohibido escribir fuera de su archivo de salida bajo `.project/campaign/`.

## 1. Objetivo de la campaña

Responder experimentalmente:

> **¿La deliberación adversarial aporta valor adicional, reproducible y suficientemente relevante sobre un proceso baseline, y ese valor justifica su coste y complejidad?**

El objetivo **no** es demostrar que Jury debe evolucionar hacia Court/Adversarial Deliberation ni que el mecanismo deba adoptarse. El resultado válido puede ser la hipótesis negativa (H5). La prioridad es obtener evidencia confiable, no validar la hipótesis.

La campaña separa explícitamente:

```text
DISCOVERY
    ↓
MATERIALITY
    ↓
DECISIONAL IMPACT
```

Un finding nuevo pero irrelevante no equivale a una mejora decisional.

## 2. Evidencia previa (Trial #1) y correcciones metodológicas

El Trial #1 se trata sólo como evidencia previa no concluyente: `n=1`; 16 findings (1 `MATERIAL` marginal, 3 `NON_MATERIAL`, 12 `DUPLICATE`, 0 `SPURIOUS`); 0 cambios de decisión y de verdict atribuibles a información nueva; 1 cambio de verdict por **reponderación** (`REVISE` → `UNDETERMINED`/`GATHER_EVIDENCE` sobre la misma evidencia); coste ≈2,35× tiempo de agente y 2,50× palabras; 75 % de duplicación. Sus limitaciones declaradas se abordan así:

| Limitación del Trial #1 | Corrección en esta campaña |
|---|---|
| Clasificación insuficientemente preregistrada | §8–§9 fijan definiciones operacionales, árbol de decisión, unidad atómica, reglas de conteo y procedimiento de adjudicación **antes** de ejecutar. |
| Ausencia de taxonomía explícita de novedad | §8 separa `NEW`/`DERIVED`/`DUPLICATE` de `MATERIAL`/`NON_MATERIAL`/`SPURIOUS` (validez terminal), con árbol de decisión y citas obligatorias. |
| Costes parcialmente autodeclarados | §11 usa timestamps del Lead (ledger) como medida primaria y los de la pasada como desglose autodeclarado; palabras por conteo determinista; llamadas `[SELF-DECLARED]`; tokens/contexto `GAP`. |
| Desviación del FRAME respecto del template real | §6 exige verificación de todo hecho contra el HEAD por el Lead **y** por un revisor independiente pre-ejecución; los errores se corrigen antes de congelar (Apéndice C). |
| `n=1` | Dos trials independientes bajo el mismo protocolo congelado (Trial #2 y Trial #3). |
| Mismo modelo | Se mantiene el mismo modelo para aislar el mecanismo (no la diversidad de modelos); se declara como límite y no se afirma independencia epistémica. |
| Independencia procedural, no epistemológica | Se conserva `commit-before-reveal`, se ejecutan Defense y Prosecution **secuencialmente** por trial y en directorios separados; se declara que sólo prueba independencia **procedural** (atested, no enforced externamente). |
| Evaluación post hoc no ciega | Evaluador `fresh` por trial + **adjudicador independiente** posterior para las categorías decisivas; el Lead no reclasifica clases (sólo corrige errores de ancla verificado), y toda disputa se reporta. |
| Caso favorable a la convergencia | §5 fija criterios por materialidad y ambigüedad, no por polaridad esperada; la selección se documenta antes de ejecutar y se declara el techo de casos pre-analizados. |
| Sesgo de encuadre del Lead | El frame se revisa independientemente antes de congelar (§6, Apéndice C); las pasadas declaran qué leyeron; el Lead no participa como pass de tratamiento. |
| Sin rebuttal | §15 fija un disparador explícito y acotado (máximo 1 rebuttal por trial). No es obligatorio. |
| Sin telemetría de tokens | `GAP` estructural del entorno; no se presentan estimaciones como mediciones exactas. |

## 3. Hipótesis y su operacionalización

- **H1 — Discovery.** La deliberación adversarial encuentra información material que el baseline no encuentra.
  *Operacionalización:* en el trial, ≥1 finding **distinto** `NEW + MATERIAL` o `DERIVED + MATERIAL` (con ancla verificable y consecuencia concreta) que no esté en el baseline. Se reporta por trial y agregado.
- **H2 — Re-evaluation.** La deliberación produce una reevaluación justificada de la conclusión aun sin nueva evidencia.
  *Operacionalización:* ≥1 cambio de verdict o recommendation entre baseline y tratamiento clasificado como **`REWEIGHTING`** (justificado criterion-based, sin depender de un finding `NEW`/`DERIVED`). Se registra aparte de H1/H3.
- **H3 — Decision impact.** Los findings de la deliberación modifican justificadamente el plan, una decisión, un verdict, una recomendación, una condición de ejecución o un requisito de evidencia.
  *Operacionalización:* ≥1 cambio **atribuible** (según §10) a un finding `NEW + MATERIAL` o `DERIVED + MATERIAL`, en `DECISIONAL_IMPACT` o `PLAN_IMPACT`. Los cambios de sólo `EVIDENCE_IMPACT` se reportan aparte.
- **H4 — Cost effectiveness.** El valor obtenido es suficientemente significativo respecto del coste adicional.
  *Operacionalización:* `ADDITIONAL_COST_RATIO_EFFECTIVE ≤ 3,0` (§11) **y** ≥1 finding material treatment-only con impacto decisional atribuible en el trial. Se reportan también las métricas de eficiencia sin usarlas como criterio único.
- **H5 — Negative hypothesis.** La deliberación produce principalmente duplicación, objeciones espurias, sobreanálisis, coste adicional o complejidad sin mejorar materialmente la decisión.
  *Operacionalización:* el trial cae en `NEGATIVE` o `NO_EVIDENCE` (§13.2), o el patrón agregado de ambos trials es `CAMPAIGN_NONE`/`CAMPAIGN_NEGATIVE` (§14.5). H5 puede ser el resultado de la campaña.

Las hipótesis no se maximizan. El resultado válido puede ser H5.

## 4. Diseño experimental

### 4.1 Condiciones y secuencia

Para cada trial `i ∈ {2, 3}`:

```text
FRAME-i (hash verificado por la pasada y por el Lead)
      ↓
BASELINE-i (Result A)
      ↓  [BASELINE CERRADO: hash en ledger antes de lanzar el tratamiento]
DEFENSE-i ── COMMIT ──┐
                      │  (secuencial por trial: DEFENSE termina y se hashea
PROSECUTION-i ─ COMMIT┘   antes de lanzar PROSECUTION; sin verse entre sí)
      ↓
REVEAL (Lead registra hashes y orden en el ledger)
      ↓
CRITERION COMPARISON + SYNTHESIS-i (recibe el baseline ya cerrado)
      ↓
VERDICT-i + RECOMMENDATION-i
      ↓
EVALUATION-i (contexto independiente, rúbrica congelada)
      ↓
ADJUDICATION (contexto independiente, re-clasifica categorías decisivas de ambos trials)
      ↓
MÉTRICAS-i + CLASIFICACIÓN-i
```

Batches de ejecución (el Lead lanza cada batch y registra timestamps y hashes en el ledger antes del siguiente):

1. `BASELINE_2` y `BASELINE_3` en paralelo (contextos y directorios separados).
2. `DEFENSE_2` y `DEFENSE_3` en paralelo.
3. `PROSECUTION_2` y `PROSECUTION_3` en paralelo (después de que ambas defensas estén cerradas y hasheadas).
4. Reveal: los hashes de `DEFENSE_i`/`PROSECUTION_i` se registran antes de lanzar las síntesis.
5. `SYNTHESIS_2` y `SYNTHESIS_3` en paralelo (cada una recibe **sólo** su FRAME, su BASELINE cerrado y sus dos posiciones).
6. `REBUTTAL_i` sólo si se dispara (§15), en contexto `fresh`.
7. `EVALUATION_2` y `EVALUATION_3` en paralelo (cada una recibe **sólo** los artefactos cerrados de su trial).
8. `ADJUDICATION` e `INTEGRITY_AUDIT` (contextos independientes, no reciben instrucciones del Lead sobre el resultado esperado).
9. El Lead calcula la decisión con las reglas congeladas.

El baseline se cierra **antes** de lanzar Defense/Prosecution. El baseline no se modifica retrospectivamente. Synthesis recibe el baseline (ya cerrado) porque el protocolo exige comparar contra él; recibirlo después del reveal no puede contaminar el baseline. **Synthesis es una pasada de tratamiento anclada al baseline cerrado**: su coste se incluye en `TREATMENT_COST_S` (§11) y no puede alterar el baseline.

### 4.2 Pasadas y qué recibe cada una

| Pasada | Recibe | No recibe | Escribe |
|---|---|---|---|
| `BASELINE-i` | FRAME-i + repositorio (sólo lectura) | Tratamiento, otro trial | `trial<i>/baseline/BASELINE_i.md` |
| `DEFENSE-i` | FRAME-i + repositorio (sólo lectura) | Baseline, Prosecution, otro trial | `trial<i>/defense/DEFENSE_i.md` |
| `PROSECUTION-i` | FRAME-i + repositorio (sólo lectura) | Baseline, Defense, otro trial | `trial<i>/prosecution/PROSECUTION_i.md` |
| `SYNTHESIS-i` | FRAME-i + `BASELINE_i` + `DEFENSE_i` + `PROSECUTION_i` (cerrados) | Otro trial; nada más | `trial<i>/synthesis/SYNTHESIS_i.md` |
| `REBUTTAL-i` (opcional, §15) | FRAME-i + los cuatro artefactos cerrados + objeción concreta | Otro trial | `trial<i>/rebuttal/REBUTTAL_i.md` |
| `EVALUATION-i` | FRAME-i + los cinco artefactos cerrados + datos de coste del ledger | Otro trial | `trial<i>/evaluation/EVALUATION_i.md` |

Cada pasada es un contexto `fresh`: no hereda la conversación del Lead ni de otras pasadas. Cada pasada declara al inicio qué archivos leyó, verifica el hash del FRAME que recibió y registra `STARTED`/`FINISHED` (ISO 8601 con offset) y llamadas a herramientas `[SELF-DECLARED]`.

### 4.3 Independencia y no contaminación

- **Defense y Prosecution se ejecutan secuencialmente dentro de cada trial** y en directorios distintos; ninguna ve la posición de la otra antes del reveal. La separación prueba **independencia procedural**, no epistémica (mismo modelo, mismo frame, misma evidencia, mismo repositorio). No se afirma independencia de razonamiento.
- **Commit-before-reveal:** al recibir cada posición, el Lead calcula su SHA-256 y lo registra en el ledger **antes** de lanzar la siguiente pasada. Los hashes permiten detectar reescrituras; no son attestación temporal externa (limitación declarada).
- **No contaminación entre trials:** cada trial tiene `BASELINE_i` y `TREATMENT_i` propios; ningún artefacto del Trial #2 se entrega a ninguna pasada del Trial #3. Los directorios y las instrucciones lo garantizan (los subagentes tienen prohibido leer `.project/campaign/trial<otro>/`). El Lead ejecuta ambos trials y conoce el orden, pero **no escribe ninguna pasada analítica** del Trial #3; el FRAME-3 se congeló antes de ejecutar el Trial #2. El análisis comparativo ocurre **después** de cerrar ambos trials (§12 del registro).
- **Límite declarado:** la no contaminación y el orden son *atested, not enforced*; no existe attestación temporal externa ni log write-once fuera del control del Lead. El ledger con cadena de hashes (§17) hace la manipulación detectable, no imposible. La conclusión no se apoya en una independencia que no se puede garantizar.

## 5. Selección de casos

### 5.1 Criterios de selección (fijados antes de ejecutar)

Un caso es admisible si cumple **todos**:

1. **Real:** es una decisión DEV abierta registrada en el repositorio versionado (no inventada para el experimento).
2. **Material:** sus consecuencias afectan al menos a uno de: decisión, plan, alcance, riesgo relevante, criterio de aceptación, condición necesaria, evidencia requerida, integración, autoridad, seguridad de ejecución o necesidad de revisión. No es una trivialidad ni una mejora cosmética.
3. **Ambiguo:** la evidencia admite ≥2 resoluciones defendibles; no existe una decisión vinculante que haya cerrado ya el asunto.
4. **Verificable:** dispone de evidencia repo-anclada suficiente (código, tests, documentos) para que los findings puedan anclarse a `ruta:sección` o comando reproducible.
5. **Acotado:** afecta a un componente/contrato/decisión como máximo; puede evaluarse en una sesión sin ejecutar cambios.
6. **No predeterminado:** la selección no se hace mirando qué caso parece más favorable a la deliberación adversarial; se documenta la razón antes de ejecutar.
7. **Sin cambio de protocolo:** evaluarlo no exige modificar `protocol/` ni el runtime.
8. **Independiente:** los dos casos difieren en contenido/dominio y no comparten el mismo objeto de decisión.
9. **Comparable:** complejidad decisional comparable (mismo número de criterios, múltiples alternativas, evidencia disponible, consecuencias materiales).
10. **No cerrado:** no existe una decisión vinculante que lo resuelva. Se admite un caso **pre-analizado** (con auditorías o análisis previos que lo enmarcan) siempre que el techo de descubrimiento se declare en el análisis y en las limitaciones (§18): la conclusión se limita a «valor adicional sobre un baseline informado por ese análisis previo», no a «valor sobre un baseline ingenuo».

### 5.2 Casos seleccionados

- **Trial #2 — Case-02: Memory como dependencia estándar del Execution Host DEV.** Decisión de producto/runtime explícitamente abierta por la auditoría de continuidad de integración (`INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:9 F-03`: «decidir si Memory es opcional por diseño o dependencia estándar del Host; no cambiar runtime por inferencia»). Es material (conecta o no una capacidad al camino real de ejecución; afecta a la declaración pública de capacidad, a tests y a la semántica de contexto), ambiguo (el seam existe y funciona, pero ningún consumidor lo suministra y no existe productor de registros; el wiring sería hoy un no-op con apariencia de capacidad), verificable (código, tests, auditoría, ADR-19) y acotado. **Razón documentada antes de ejecutar:** el Trial #1 sugirió que la contribución observable de la deliberación puede ser detectar duplicación/obsolescencia de declaraciones y afinar condiciones de aceptación, no descubrir integraciones ausentes; Case-02 permite medir esa hipótesis sobre una decisión de integración real con consecuencias de producto, sin elegirla por su polaridad esperada.
- **Trial #3 — Case-03: ADR-worthiness del acto de autoridad del Plan 152.** Decisión de gobernanza explícitamente abierta: el acto del 2026-10-07 (`GOV-1`…`GOV-10`) **no** ejerció el juicio de ADR-worthiness (`AU-6`); el Plan remite la cuestión a `<PLAN-152>:F-1` (`open`, owner mantenedor) y registra como pending decision «ADR nuevo · enmienda del ADR-19 · no producir ADR»; `ROADMAP.md` lista el bloqueo. Es material (cómo se registra una decisión de autoridad reservada; afecta al blocker del roadmap y a la trazabilidad futura), ambiguo (el Plan ya registra el acto verbatim; la ADR puede duplicar o puede ser la vía de registro independiente que `AU-6` exige), verificable (Plan 152, ADR-16, INDEX, template, ROADMAP) y acotado. **Razón documentada antes de ejecutar:** es un caso independiente en contenido/dominio (gobernanza/registro de autoridad, no runtime de producto) con complejidad decisional comparable; no se eligió por su polaridad esperada.
- **Definición de «replicación controlada» (Trial #2):** replica el **método** del Trial #1 (mismo protocolo de pasadas y criterios) sobre un caso nuevo, para probar si el **fenómeno observado** en el Trial #1 (señal positiva estrecha con alta duplicación y cambio de verdict por reponderación) se reproduce con las ambigüedades metodológicas corregidas. No replica el caso ni el resultado del Trial #1.

### 5.3 Comparabilidad Trial #2 ↔ Trial #3

Se consideran comparables porque: (a) ambos son decisiones DEV reales y abiertas; (b) ambos tienen consecuencias materiales y evidencia verificable; (c) ambos admiten ≥2 resoluciones defendibles; (d) ambos se evalúan con los mismos 6 criterios, el mismo frame de 4 partes (`QUESTION`/`CANDIDATE`/`CRITERIA`/`EVIDENCE`) y el mismo protocolo de pasadas; (e) ambos son acotados a un componente/contrato/decisión; (f) ambos difieren en contenido/dominio (runtime de producto vs gobernanza/registro de autoridad), lo que reduce el riesgo de que el resultado sea propiedad accidental de un único problema. No son comparables en hechos de dominio ni en magnitud de consecuencias; la comparación es de **fenómeno y mecanismo**, no de contenido. Ambos son **pre-analizados** (una auditoría reciente y un pending decision previo, respectivamente), lo que baja el techo de descubrimiento y se declara como limitación.

### 5.4 Casos considerados y excluidos (documentado antes de ejecutar)

- **Integration Surface / F-01 / F-02 del Plan 178:** es el objeto del Trial #1; reutilizarlo contaminaría la replicación y no es independiente.
- **Piloto de la segunda observación de `ExecutionHost`:** ya implementado en el HEAD (`iterate(iteration, observation)` recibe la observación y su docstring declara la lectura única); no queda decisión abierta.
- **Delta REQUIRED de Theoretical Execution (`D-1`…`D-7`):** implementado por el Plan 176 (`Executed`/`Closed`); no queda decisión abierta.
- **Enforcement de placement:** explícitamente diferido por una decisión cerrada (`PLAN-129:DEC-2`; `docs/placement-contract.md:§22/§24`); evaluarlo sería una decisión de scheduling/autoridad más que de sustancia, con riesgo de resultado predeterminado.
- **Verificación selectiva (`TARGETED`) en el bucle local:** excluida **antes de ejecutar** por dos razones: (i) dos auditorías previas (`TEST_ARCHITECTURE_AUDIT_2026-10-13.md:§13 D-1`; `TEST_SUITE_AUDIT_2026-10-13.md:§11`) ya recomiendan el candidato y enumeran sus prerequisitos, por lo que el techo de descubrimiento es muy bajo y el resultado mediría una asimetría de información del frame; (ii) el candidato no era admisible sin decidir antes su lugar canónico, la autoridad del command-set, la semántica del cierre de imports y el formato del mapa —decisiones que el repositorio no tiene y que el frame no puede inventar—. Se sustituyó por Case-03 (ADR-worthiness) **antes de congelar**; la sustitución y su razón se registran en el Apéndice C.
- **Split de los 6 archivos de test con ganancia real:** la auditoría ya identificó los 6 y el riesgo R9; es una intervención más mecánica y con menos ambigüedad de decisión que una práctica de verificación completa.
- **Mejoras de `README.md`/`ROADMAP.md` o documentación cosmética:** no cumplen el criterio de materialidad.
- **Añadir checkers a la batería canónica o cambiar CI:** material, pero la decisión D-3 es de gobernanza del mantenedor y su evaluación exigiría datos de uso que el repositorio no tiene; se excluye para no evaluar una decisión sin evidencia verificable.
- **Casos truncados por falta de evidencia:** no se consideró ningún caso sin decisión abierta verificada; si durante la ejecución se descubre que un caso estaba cerrado, se registra como desviación (§16) y se detiene su tratamiento.

**Declaración de no sesgo:** los dos casos se seleccionaron por materialidad, ambigüedad verificada y disponibilidad de evidencia, no por la probabilidad percibida de producir un resultado favorable a la deliberación adversarial. Ambos admiten una recomendación contraria al candidato sin que el experimento quede inválido. El pool considerado y las razones de exclusión están arriba.

## 6. Objeto de deliberación: FRAME congelado y verificación

Cada trial tiene un FRAME congelado e idéntico para todas sus pasadas, con `QUESTION`, `CANDIDATE` (con propiedades declaradas y alternativa explícita), `CRITERIA` (6), `EVIDENCE BASE` y `EVIDENCE RULES`. Los textos completos están en **Apéndice A (FRAME-2)** y **Apéndice B (FRAME-3)**; son los mismos que se entregan a las pasadas y sus hashes están en §0. Cada pasada debe verificar el hash del frame que recibe y registrarlo; una discrepancia detiene la pasada (D2).

**Verificación pre-congelación:** el Lead verificó cada hecho del frame contra el HEAD antes de congelar. Además, un revisor independiente en contexto `fresh` auditó el preregistro y los frames contra el HEAD y contra los requisitos metodológicos de la campaña; su informe, sus correcciones y el reemplazo de Case-03 se registran en **Apéndice C**. Una segunda verificación independiente y acotada se ejecutó sobre el FRAME-3 de reemplazo. Cualquier afirmación no verificable se degradó a `GAP` o se retiró antes de congelar.

**Propiedad del frame:** el frame no se modifica después de congelado. Si una pasada detecta un error factual del frame, se registra como desviación (§16) y la pasada debe continuar con el frame tal como está; el error no se corrige retroactivamente.

## 7. Instrucciones congeladas por pasada

Las instrucciones completas entregadas a cada subagente se conservan en el registro de trials (Apéndice D: contrato de pasadas). Reglas comunes:

1. **Sólo lectura del repositorio.** La única escritura permitida es el archivo de salida propio bajo `.project/campaign/`. Prohibido `git add/commit/checkout/reset`, prohibido escribir archivos versionados y prohibido leer otros directorios de trial o posiciones no asignadas.
2. **Evidencia admitida:** sólo contenido versionado en el HEAD declarado, comandos de lectura y, si se declara, ejecución acotada de tests de sólo lectura. Prohibido web, modelos externos, memoria de conversaciones previas y citar los untracked del mantenedor.
3. **No inventar hechos.** Si falta evidencia, declarar `GAP`. Distinguir `OBSERVED`/`MEASURED`/`INFERRED`/`RECOMMENDED` (con `GAP` para la ausencia). Toda afirmación material debe anclarse a `ruta:sección`, a un comando reproducible o a una observación declarada.
4. **Idioma:** español (términos técnicos en inglés permitidos).
5. **No autoridad:** el resultado es advisory; no autoriza cambios.
6. **Presupuesto:** cada pasada produce **4–10 findings atómicos** como guía de coste; si produce más, se clasifican **todos** (no se poda). No se premia el volumen; el objetivo es calidad de argumento. El denominador de las métricas es el número de findings enumerados, no una cuota.
7. **Metadata obligatoria:** `STARTED`, `FINISHED`, hash del FRAME recibido, archivos leídos y llamadas a herramientas estimadas `[SELF-DECLARED]`. Cada finding lleva ID (`B-n` baseline, `D-n` defense, `P-n` prosecution, `R-n` rebuttal).
8. **Procedencia:** cuando una pasada sostiene un cambio de decisión, verdict o recommendation, debe **citar los IDs de los findings** que lo sustentan (`[D-3]`, `[P-2]`). Sin cita, el cambio no es atribuible (§10).

Instrucciones específicas:

- **BASELINE:** producir el resultado del proceso normal: contexto, pregunta, evidencia disponible, interpretación, alternativas, decisión/recomendación, plan si corresponde, riesgos, incertidumbres y supuestos. Debe decidir y comprometerse (`PROCEED`/`REVISE`/`GATHER_EVIDENCE` u otra decisión explícita). No conoce el tratamiento.
- **DEFENSE:** construir el *strongest case FOR* el candidato: defender la interpretación, identificar evidencia favorable, justificar supuestos, identificar condiciones bajo las cuales es válido y evitar argumentos que sólo puedan construirse después de conocer Prosecution. Debe comprometer su posición (`SUPPORT` / `SUPPORT_WITH_CONDITIONS` / `OPPOSE_WITH_CONDITIONS` / `OPPOSE`) y su confianza antes del reveal.
- **PROSECUTION:** construir el *strongest case AGAINST* el candidato: intentar falsar supuestos, evidencia, inferencias, dependencias, integraciones, condiciones, consecuencias y puntos débiles del plan. Distinguir `REAL OBJECTION` vs `SPECULATIVE OBJECTION`. No inventar hechos. Debe comprometer su posición y confianza antes del reveal.
- **SYNTHESIS:** comparar Defense y Prosecution **criterio por criterio**, responder las 9 preguntas del protocolo (válidos/duplicados/derivados/materiales/espurios/contradicciones/incertidumbres/evidencia adicional/qué cambió), no resolver por mayoría, preservar desacuerdos, no introducir evidencia nueva y citar IDs por cada cambio propuesto. Emite `VERDICT` (`VIABLE`/`NOT_VIABLE`/`UNDETERMINED`) y `RECOMMENDATION` (`PROCEED`/`REVISE`/`GATHER_EVIDENCE`), separados.
- **EVALUATION:** aplicar la rúbrica congelada (§8–§13) a todas las piezas; clasificar cada finding; medir impacto y coste con los datos del ledger; recomputar conteos; registrar discrepancias y GAP. No conoce la decisión final del Lead ni el otro trial.
- **ADJUDICATION:** contexto independiente que recibe los dos trials completos y re-clasifica **todas** las categorías decisivas (`NEW+MATERIAL`, `DERIVED+MATERIAL`, `DUPLICATE+MATERIAL`, `SPURIOUS`) y una muestra aleatoria declarada del resto; reporta coincidencias y discrepancias con el evaluador, sin conocer la decisión esperada. No cambia artefactos.
- **INTEGRITY AUDIT:** contexto independiente que verifica hashes del ledger, orden baseline→defensa→prosecución→reveal→synthesis, ausencia de referencias cruzadas Trial #2↔Trial #3, consistencia de conteos y cálculos, y que los apéndices verbatim coincidan por hash; reporta PASS/FAIL por ítem y GAP.

## 8. Taxonomía y protocolo de clasificación

### 8.1 Dimensión 1 — Novedad (respecto del baseline del mismo trial)

- **`NEW`** — introduce información, relación, contradicción, condición o implicación que **no estaba presente** en el baseline. Cita obligatoria: evidencia que no aparece en `BASELINE_i` y búsqueda que lo verifica.
- **`DERIVED`** — no introduce un hecho completamente nuevo, pero **deriva una conclusión válida que el baseline no había explicitado** y que posee relevancia propia. Cita obligatoria: premisas del baseline + paso de inferencia.
- **`DUPLICATE`** — reproduce sustancialmente un finding, riesgo, condición o conclusión que **ya estaba presente en el baseline**, aunque cambie la formulación o el peso. Cita obligatoria: pasaje del baseline que contiene el mismo hecho **y** la misma consecuencia material (no sólo el mismo tema).

**Regla de desempate (fijada antes de ejecutar):** si el baseline contiene el hecho **y** la consecuencia → `DUPLICATE`; si contiene el hecho pero **no** la consecuencia/conclusión → `DERIVED`; si no contiene ni el hecho ni la consecuencia → `NEW`. La clasificación se decide por contenido, no por formulación ni por longitud. Las discrepancias sobre el desempate se resuelven por el ADJUDICADOR con esta regla; no por el Lead.

### 8.2 Dimensión 2 — Validez y materialidad (terminal)

Después de la novedad, cada finding recibe **un** valor de esta dimensión:

- **`MATERIAL`** — soportado (ancla verificable o medición declarada) **y** con consecuencia concreta sobre al menos un objeto de §9. Es material en términos absolutos, aunque sea `DUPLICATE` (en ese caso no aporta valor nuevo).
- **`NON_MATERIAL`** — soportado, pero sin consecuencia concreta; relevancia expositiva, de estilo o de alcance nulo.
- **`SPURIOUS`** — **terminal**: sin soporte, con evidencia falsa o mal leída, con confusión semántica, o que ataca una versión del candidato que el frame no propone. Un `SPURIOUS` **no puede ser `MATERIAL` ni `NON_MATERIAL`**; el valor `SPURIOUS` reemplaza a los otros dos.

La matriz resultante es `{NEW, DERIVED, DUPLICATE} × {MATERIAL, NON_MATERIAL, SPURIOUS}`; las nueve combinaciones son posibles. `DUPLICATE + MATERIAL` se registra y cuenta como materialidad absoluta, pero **no** como valor nuevo. **`DISTINCT_MATERIAL_NEW`** = findings `(NEW | DERIVED) + MATERIAL` **distintos**. Las combinaciones `MATERIAL+SPURIOUS` son imposibles por construcción.

### 8.3 Unidad atómica, conteo y doble conteo

- **Finding atómico** = una afirmación con una consecuencia concreta. Si una pasada agrupa varias, el evaluador las separa y las cuenta por separado (declarándolo).
- **Corpus primario (distinct):** los findings se deduplican **por contenido** entre pasadas (misma afirmación + misma consecuencia = 1 finding distinto); las **ocurrencias** se reportan como métrica secundaria. `DUPLICATE_SHARE` y `SPURIOUS_SHARE` primarias se calculan sobre el corpus distinct; también se reportan sobre ocurrencias.
- **Agregado de campaña:** **pooled** = suma de numeradores / suma de denominadores de ambos trials (no promedio de proporciones). Se reportan además los valores por trial.
- **Cero findings:** shares = 0 por definición; el trial es `NO_EVIDENCE` si `DISTINCT_MATERIAL_NEW = 0`.
- **Prohibido doble conteo:** un finding no se cuenta dos veces en la misma pasada; la síntesis no re-cuenta findings de Defense/Prosecution; `NEW+MATERIAL` y `DERIVED+MATERIAL` no se suman dos veces para el mismo finding.
- **Sin reclasificación post-resultado:** la clasificación del EVALUATION es la primaria y se congela antes del análisis cross-trial. El Lead **no** reclasifica clases: sólo puede corregir un **error factual de ancla** (una cita que no existe o un valor medido falso), verificado contra el repo, y debe reportar la clasificación anterior y la corregida y recalcular. Las disputas de clase van al ADJUDICADOR; si persiste una discrepancia que cambia la clase del trial, se reportan ambas y la decisión se calcula con la primaria **más** un análisis de sensibilidad con la alternativa; si el resultado de la campaña cambia, se declara `INCONCLUSIVE` (D2) en lugar de elegir.

### 8.4 Procedimiento

1. `EVALUATION_i` clasifica, verifica anclas y computa métricas.
2. `ADJUDICATION` re-clasifica las categorías decisivas de ambos trials y la muestra; produce coincidencias/discrepancias.
3. `INTEGRITY_AUDIT` verifica hashes, orden, ausencia de contaminación, conteos y cálculos.
4. El Lead aplica la regla congelada a las cifras verificadas; registra cualquier corrección factual (sólo ancla) con su efecto.
5. La clasificación final y los totales quedan congelados antes de la decisión de campaña.

## 9. Criterio operacional de MATERIAL

Un finding es `MATERIAL` sólo si cumple **las tres** condiciones:

1. **Soporte:** tiene ancla verificable en el HEAD (ruta:sección, comando reproducible) o una medición declarada; no es una conjetura.
2. **Consecuencia concreta:** declara al menos un cambio observable en uno de estos objetos, con el cambio especificado (no vago): decisión; plan; alcance; riesgo relevante; criterio de aceptación; condición necesaria; evidencia requerida; integración; autoridad; seguridad de ejecución; necesidad de revisión.
3. **Objeto identificado:** el finding dice **qué** cambia (qué paso, qué campo, qué condición, qué evidencia, qué decisión), no sólo que «algo podría ser distinto».

No es `MATERIAL`: un argumento bien escrito sin consecuencia; una preferencia estética; una reafirmación de un riesgo ya presente (sería `DUPLICATE`); una objeción hipotética sin ancla; un «podría fallar» sin condición ni consecuencia; una consecuencia que ya está cubierta por una condición del candidato (en ese caso se declara `NON_MATERIAL` o se rechaza como objeción).

**Novelty no es requisito de materialidad:** un `DUPLICATE` puede ser `MATERIAL` en términos absolutos, pero no cuenta como valor nuevo (`DISTINCT_MATERIAL_NEW`).

## 10. Definiciones de impacto y atribución

- **`DECISIONAL_IMPACT`** = cambio atribuible en **decisión**, **verdict** o **recommendation** (la conclusión del proceso).
- **`PLAN_IMPACT`** = cambio atribuible en **plan**, **alcance**, **condición de aceptación/validez** o **criterio de verificación** (incluye pasos/campos/orden/verificación).
- **`EVIDENCE_IMPACT`** = requisito de **evidencia nueva** atribuible, **sin** cambio de plan ni de conclusión.
- **`DECISION_IMPACT` (para H3)** = `DECISIONAL_IMPACT ∨ PLAN_IMPACT`. Los `EVIDENCE_IMPACT` solos no cuentan como impacto decisional, pero sí como valor material.
- **`REWEIGHTING`** = cambio de decisión/verdict/recommendation **sin** finding `NEW`/`DERIVED` que lo respalde, justificado por una relectura de la misma evidencia. Cuenta para H2, nunca para H1/H3.

**Atribución (regla estricta):** un cambio es **atribuible a la deliberación** sólo si se cumplen las cuatro:

1. El resultado del baseline difiere.
2. `SYNTHESIS_i` (o el veredicto/recommendación que produce) **cita el ID** del finding `NEW+MATERIAL` o `DERIVED+MATERIAL` que enuncia la consecuencia.
3. El evaluador verifica la cadena finding → cita → cambio.
4. El contrafactual declarado es «si se elimina el finding, el cambio no se sostiene». Si el cambio persiste sin el finding, es `NO ATRIBUIDO`.

Sin cita, sin cadena verificada o sin contrafactual, el cambio se registra como `NO ATRIBUIDO` y no cuenta para H3/H4. `REWEIGHTING` se registra aparte con su justificación criterion-based.

## 11. Método de medición de costes

| Métrica | Método | Calidad |
|---|---|---|
| `LEAD_WALL_S` (primaria) | timestamp del Lead al lanzar cada pasada y al recibir su artefacto, registrados en el ledger (`Get-Date -Format o`); incluye la latencia del entorno y del Lead | Medida por el Lead, aproximada; auditables en el ledger |
| `SELF_S` (secundaria) | `STARTED`/`FINISHED` que la propia pasada escribe | **`[SELF-DECLARED]`** |
| Palabras | tokens separados por whitespace (`Measure-Object -Word`); se reportan también caracteres | Medida determinista del artefacto; no es conteo lingüístico |
| Llamadas a herramientas | declaradas por la pasada | **`[SELF-DECLARED]`** |
| Tokens / contexto | no disponible en el entorno | **`GAP` estructural** |
| Iteraciones / pasadas | conteo de artefactos | Medida exacta |

Definiciones:

- `BASELINE_COST_S` = `LEAD_WALL_S` de `BASELINE_i`.
- `TREATMENT_COST_S` = suma de `LEAD_WALL_S` de `DEFENSE_i` + `PROSECUTION_i` + `SYNTHESIS_i` (+ `REBUTTAL_i` si existe). Las pasadas concurrentes cuentan por separado (esfuerzo de agente, no reloj).
- `ADDITIONAL_COST_RATIO_LEAD` = `TREATMENT_COST_S / BASELINE_COST_S`.
- `ADDITIONAL_COST_RATIO_SELF` = el mismo cociente con `SELF_S`.
- `ADDITIONAL_COST_RATIO_EFFECTIVE` = **el mayor** de los dos ratios anteriores. Si discrepan, decide el conservador; se reportan ambos.
- `WALL_CLOCK_RATIO` = reloj desde el lanzamiento del tratamiento hasta la recepción de la síntesis / reloj del baseline; se reporta como descriptivo.
- `WORDS_RATIO` = palabras del tratamiento / palabras del baseline.
- `EFFICIENCY` = `DISTINCT_MATERIAL_NEW` por 1.000 s de coste adicional (`TREATMENT_COST_S` y también `LEAD_WALL_S`); cambios decisionales atribuibles / coste adicional; findings nuevos / coste adicional. Se reportan las tres; ninguna es criterio absoluto.

No se presentan estimaciones como mediciones exactas. Toda cifra autodeclarada se marca.

**Concurrencia:** las pasadas pueden ejecutarse en paralelo (Baseline #2/#3; Defense #2/#3; Prosecution #2/#3; Synthesis #2/#3; Evaluation #2/#3). Las duraciones son de reloj e incluyen contención del entorno compartido; se comparan como **ratios** medidos en la misma campaña, no como tiempos absolutos de CPU. La concurrencia se declara como factor de variación.

## 12. Métricas obligatorias del registro

Por trial y agregadas (pooled):

```text
Findings: total (occurrences), distinct, NEW, DERIVED, DUPLICATE, MATERIAL,
          NON_MATERIAL, SPURIOUS, NEW+MATERIAL, DERIVED+MATERIAL, DUPLICATE+MATERIAL,
          DISTINCT_MATERIAL_NEW, DISTINCT_MATERIAL_NEW_BY_PASS
Impact:   DECISIONAL_IMPACT, PLAN_IMPACT, EVIDENCE_IMPACT, DECISION_IMPACT,
          REWEIGHTING, NO ATRIBUIDO; cada uno con IDs de finding y cita
Cost:     LEAD_WALL_S por pasada y total, SELF_S por pasada [SELF-DECLARED],
          palabras (exactas), caracteres, llamadas [SELF-DECLARED], tokens (GAP),
          iteraciones/pasadas, ratios LEAD/SELF/EFFECTIVE
Efficiency: DISTINCT_MATERIAL_NEW / coste adicional; impactos decisionales / coste
          adicional; findings nuevos / coste adicional
Disagreement: AGREEMENT / PARTIAL_AGREEMENT / UNRESOLVED_DISAGREEMENT por criterio,
          con posición Defense, posición Prosecution, evidencia y razón de no resolución
```

## 13. Umbrales y clasificación por trial

### 13.1 Umbrales (fijados antes de ejecutar)

- `DUPLICATE_SHARE` = findings `DUPLICATE` del corpus **distinct** / findings distinct totales del tratamiento.
- `SPURIOUS_SHARE` = findings `SPURIOUS` distinct / findings distinct totales.
- `COST_RATIO` = `ADDITIONAL_COST_RATIO_EFFECTIVE` (§11).
- `COSTLY` = `COST_RATIO > 3,0`.
- `REDUNDANT` = `DUPLICATE_SHARE > 0,50` (para `DECISION`), `> 0,60` (para `PLAN`/`EVIDENCE`).
- `VERY_REDUNDANT` = `DUPLICATE_SHARE ≥ 0,75`.
- `SPURIOUS_HIGH` = `SPURIOUS_SHARE > 0,15` (se reporta también `> 0,10`).
- Los umbrales son **inclusivos** en el límite (`≥`/`≤` se aplican literalmente); los empates se reportan explícitamente.
- Con 0 findings: shares = 0 y `DISTINCT_MATERIAL_NEW = 0`.

### 13.2 Clase por trial (exhaustiva y mutuamente excluyente)

Primero se calcula `VALUE_CLASS`:

- **`NONE`** = `DISTINCT_MATERIAL_NEW = 0`.
- **`EVIDENCE`** = `DISTINCT_MATERIAL_NEW ≥ 1`, `DECISION_IMPACT = 0`, `EVIDENCE_IMPACT ≥ 1`.
- **`PLAN`** = `PLAN_IMPACT ≥ 1` y `DECISIONAL_IMPACT = 0`.
- **`DECISION`** = `DECISIONAL_IMPACT ≥ 1` (aunque también haya `PLAN_IMPACT`).

Luego se aplica, **en este orden**, la primera clase que se cumpla:

1. **`INVALID_TRIAL`** — D3 (§16) o artefacto faltante que impide la comparación.
2. **`NEGATIVE`** — (`VERY_REDUNDANT` ∧ `VALUE_CLASS = NONE` ∧ (`SPURIOUS_HIGH` ∨ `COSTLY`)) **o** el tratamiento produce ≥1 finding clasificado como material y verificado como **falso** que habría cambiado la decisión en la dirección errónea.
3. **`SUCCESS_STRONG`** — `VALUE_CLASS = DECISION` ∧ `DUPLICATE_SHARE ≤ 0,50` ∧ `SPURIOUS_SHARE ≤ 0,10` ∧ ¬`COSTLY`.
4. **`SUCCESS_PARTIAL`** — `VALUE_CLASS = PLAN` ∧ `DUPLICATE_SHARE ≤ 0,60` ∧ `SPURIOUS_SHARE ≤ 0,10` ∧ ¬`COSTLY`.
5. **`SUCCESS_EVIDENCE`** — `VALUE_CLASS = EVIDENCE` ∧ `DUPLICATE_SHARE ≤ 0,60` ∧ `SPURIOUS_SHARE ≤ 0,10` ∧ ¬`COSTLY`.
6. **`NO_EVIDENCE`** — `VALUE_CLASS = NONE` (y no `NEGATIVE`).
7. **`POSITIVE_BUT_COSTLY`** — `VALUE_CLASS ∈ {EVIDENCE, PLAN, DECISION}` ∧ `COSTLY`.
8. **`POSITIVE_BUT_REDUNDANT`** — `VALUE_CLASS ∈ {PLAN, DECISION}` ∧ ¬`COSTLY` ∧ `DUPLICATE_SHARE > 0,60` (PLAN) o `> 0,50` (DECISION); `VALUE_CLASS = EVIDENCE` con `DUPLICATE_SHARE > 0,60`.
9. **`POSITIVE_BUT_SPURIOUS`** — `VALUE_CLASS ∈ {PLAN, DECISION, EVIDENCE}` ∧ ¬`COSTLY` ∧ `SPURIOUS_SHARE > 0,10` (y no redundant/costly).
10. **`INCONCLUSIVE_TRIAL`** — cualquier caso restante (p. ej., clasificación ambigua declarada, D2 que impide leer una categoría decisiva).

La exhaustividad se controla con una tabla de decisión sintética en el Apéndice C (casos numéricos worked-out) y con el INTEGRITY AUDIT.

### 13.3 Resultado de campaña

- **`CAMPAIGN_STRONG`** — ambos trials `SUCCESS_STRONG` y se cumplen las condiciones de `ADOPT` (§14.2).
- **`CAMPAIGN_REFORMULATED`** — no `CAMPAIGN_STRONG` y se cumple al menos un disparador `R1`–`R4` (§14.3).
- **`CAMPAIGN_SIGNAL_SINGLE`** — señal material en un trial (clase `SUCCESS_*` o `POSITIVE_BUT_*`) y `NONE`/`NO_EVIDENCE`/`NEGATIVE` en el otro.
- **`CAMPAIGN_NONE`** — ambos trials `NO_EVIDENCE` (sin valor nuevo material).
- **`CAMPAIGN_NEGATIVE`** — ambos trials `NEGATIVE`, o uno `NEGATIVE` y el otro `NO_EVIDENCE`.
- **`CAMPAIGN_INVALID`** — algún trial `INVALID_TRIAL` o desviación D3 que impide la comparación.

Cada etiqueta se mapea a una decisión en §14.5; no hay etiquetas sin decisión.

## 14. Regla de decisión de la campaña

### 14.1 Regla de no adaptación

Este preregistro, sus umbrales y esta regla quedan **congelados** antes de ejecutar. Después de observar resultados:

- **No** se cambian definiciones, umbrales, criterios de materialidad ni esta regla.
- **Sí** se registran desviaciones y correcciones factuales de ancla de forma append-only, con su efecto declarado.
- Un cambio de regla invalida la campaña: exigiría un preregistro nuevo y trials nuevos; no se reclasifica el resultado para que encaje.

### 14.2 Condiciones de `ADOPT`

`ADOPT` sólo si se cumplen **todas**:

1. Ambos trials `SUCCESS_STRONG`.
2. `DUPLICATE_SHARE` pooled ≤ 0,50.
3. `COST_RATIO ≤ 3,0` en ambos trials.
4. Ningún disparador de `REFORMULATE` (§14.3).
5. Sin `INVALID_TRIAL` ni desviación D3.

### 14.3 Condiciones de `REFORMULATE`

`REFORMULATE` si no se cumple `ADOPT` y se cumple **al menos uno** (se evalúan en orden y se registra el disparador aplicado):

- **R1 — Asimetría de contribución.** Sólo aplicable si `DISTINCT_MATERIAL_NEW` pooled ≥ 4. En ambos trials, ≥75 % de los `DISTINCT_MATERIAL_NEW` provienen de una sola pasada (Defense **o** Prosecution), la misma en ambos trials, y la otra pasada aporta 0 `DISTINCT_MATERIAL_NEW`. Lectura: lo que aporta valor es **una** revisión adversarial, no la estructura de dos posiciones.
- **R2 — Valor sin impacto decisional.** Ambos trials con `VALUE_CLASS = EVIDENCE` (sólo requisitos de evidencia/condiciones, sin cambio de plan ni de conclusión). Lectura: reformular a una revisión adversarial de **condiciones y evidencia**, no a una deliberación completa con verdict.
- **R3 — Redundancia con valor estrecho.** `DUPLICATE_SHARE` pooled ≥ 0,60 **y** ambos trials con `VALUE_CLASS ∈ {PLAN, DECISION}` (o uno `PLAN`/`DECISION` y el otro `EVIDENCE`). Lectura: conservar el componente que produce valor nuevo (chequeo adversarial dirigido), no el proceso completo.
- **R4 — Coste desproporcionado.** Ambos trials con `VALUE_CLASS ∈ {EVIDENCE, PLAN, DECISION}` y `COST_RATIO > 3,0` en al menos uno. Lectura: un mecanismo más barato (una sola pasada adversarial o una lista de condiciones) antes que deliberación completa.

### 14.4 Condiciones de `INCONCLUSIVE`

`INCONCLUSIVE` si no se cumple `ADOPT`, `REJECT` ni `REFORMULATE`, incluyendo: `CAMPAIGN_SIGNAL_SINGLE`; `POSITIVE_BUT_SPURIOUS`; discrepancia de clasificación material no resuelta que no cambia la clase del trial; desviación D2 que impide comparar; evidencia prometedora pero insuficiente para elegir entre mecanismos; o discrepancia entre evaluador y adjudicador que, con la alternativa, cambia la decisión de campaña.

### 14.5 Condiciones de `REJECT` y mapeo de etiquetas

`REJECT` si:

1. `CAMPAIGN_NONE` (ambos `NO_EVIDENCE`), **o**
2. `CAMPAIGN_NEGATIVE` (ambos `NEGATIVE`, o uno `NEGATIVE` y el otro `NO_EVIDENCE`), **o**
3. En ambos trials el tratamiento no aporta ningún finding material nuevo atribuible (`DISTINCT_MATERIAL_NEW = 0`) y no hay impacto decisional, con independencia de las shares.

Mapeo explícito:

| Resultado de campaña (§13.3) | Decisión |
|---|---|
| `CAMPAIGN_STRONG` | `ADOPT` (si además se cumplen §14.2; si no, `REFORMULATE`/`INCONCLUSIVE` según corresponda) |
| `CAMPAIGN_REFORMULATED` | `REFORMULATE` |
| `CAMPAIGN_SIGNAL_SINGLE` | `INCONCLUSIVE` |
| `CAMPAIGN_NONE` | `REJECT` |
| `CAMPAIGN_NEGATIVE` | `REJECT` |
| `CAMPAIGN_INVALID` | `INCONCLUSIVE` |

`REJECT` es un resultado válido y se documenta como tal.

### 14.6 Prioridad

Se evalúa en este orden: `INVALID_TRIAL`/D3 → `REJECT` → `ADOPT` → `REFORMULATE` → `INCONCLUSIVE`. El resultado se declara con evidencia de las métricas, no por impresión cualitativa.

## 15. Rebuttal

Opcional. Disparador único: la síntesis identifica un desacuerdo **material** (que afectaría verdict o recommendation) cuya resolución requiere una respuesta de una de las posiciones, y la respuesta puede construirse con evidencia **ya existente** en el frame/repositorio.

- Máximo **1** rebuttal por trial; lo ejecuta una pasada `fresh` que recibe los cuatro artefactos cerrados y la objeción concreta.
- Toda nueva afirmación material del rebuttal debe estar sustentada por evidencia existente **o** generar explícitamente una necesidad de nueva evidencia/evaluación (registrada como `REQUIRES_NEW_EVIDENCE`). Sus findings se clasifican con la misma rúbrica y llevan ID `R-n`.
- No se permite evidencia nueva silenciosa: si aparece, el rebuttal se marca inválido para la decisión y se registra (D2).
- El rebuttal cuenta en `TREATMENT_COST_S` y en las métricas de coste.
- Si no hay disparador, no se ejecuta y se declara `REBUTTAL = NOT_TRIGGERED`.

## 16. Desviaciones, contingencias y validez

Toda desviación se registra en el ledger y en el registro de trials con: qué se desvió, cuándo, por qué, qué evidencia se vio antes y su efecto. Clases:

- **D1 — no material:** no afecta a ninguna métrica ni clasificación (p. ej. un error de conteo corregido).
- **D2 — material, trial válido con limitación:** afecta a una métrica o a la interpretación, pero la comparación sigue siendo válida; se declara y se reporta el resultado con y sin el dato afectado si es posible.
- **D3 — invalida el trial:** baseline contaminado, reveal violado, taxonomía aplicada de forma inconsistente sin posibilidad de adjudicación, artefacto reescrito después del hash, o evidencia inventada. Si ocurre en Trial #2: **detener Trial #3** hasta determinar si el protocolo sigue siendo válido; no corregir en silencio. Si el protocolo no puede aplicarse, la campaña se declara `INCONCLUSIVE` o se repropone con un preregistro nuevo.

Contingencias:

- **Pasada fallida sin artefacto:** se registra D2 y se reintenta **una** vez en contexto fresco, con nuevo `STARTED`; el coste incluye ambos intentos. Si el segundo intento falla, se registra D3 si el artefacto es esencial para la comparación.
- **Pasada con 0 findings:** es un resultado válido; shares 0; el trial puede ser `NO_EVIDENCE`. No se reintenta para «obtener findings».
- **Pasada con >10 findings:** se clasifican todos; no se poda (el cap es guía de coste, no regla de conteo).
- **Artefacto modificado después del hash:** discrepancia → D3.
- **Pasada que lee archivos prohibidos (declarado o detectado):** D2; si leyó el otro trial o una posición no asignada antes del reveal → D3.
- **Datos de coste incompletos:** `GAP`; si falta `BASELINE_COST_S`, no se puede computar el ratio → el trial no puede ser `SUCCESS_*` por coste y se declara; la decisión usa la evidencia cualitativa y el límite se reporta.
- **Caso que se descubre cerrado:** se detiene su tratamiento y se registra D3 (selección inválida); no se sustituye a mitad de campaña.

## 17. Verificación de integridad (checklist pre-cierre)

Antes de emitir la decisión final se verifica:

1. El baseline de cada trial quedó cerrado (hash en el ledger) antes del tratamiento; ningún baseline incorpora findings del tratamiento.
2. `commit-before-reveal`: cada posición registró hash al cerrar, **antes** de lanzar la siguiente; el reveal ocurrió después; no hubo reescritura posterior (hash verificado al recibir y al evaluar).
3. Trial #3 no recibió ningún artefacto, finding ni resumen del Trial #2; el INTEGRITY AUDIT verifica referencias cruzadas y directorios.
4. Clasificación consistente entre trials: misma rúbrica, mismas definiciones, mismo procedimiento; evaluador + adjudicador independientes; el Lead sólo corrigió errores de ancla verificados.
5. Ningún finding contado dos veces; totales recomputados desde las tablas del evaluador y contrastados con la lista de findings; deduplicación distinct/occurrences declarada.
6. Cálculos y costes recomputados por script; unidades y fórmulas declaradas; cifras autodeclaradas marcadas; `ADDITIONAL_COST_RATIO_EFFECTIVE` calculado con la regla del mayor.
7. Toda desviación está registrada y clasificada D1/D2/D3.
8. La conclusión no depende de reclasificar resultados después de conocerlos; si hubo correcciones de ancla, están trazadas y la decisión se recalculó con las reglas congeladas; el análisis de sensibilidad está reportado.
9. Los hashes SHA-256 de los artefactos de sesión, de los frames y del preregistro están registrados; la identidad de los apéndices verbatim se verifica por hash.
10. El ledger es append-only con cadena de hashes: cada entrada incluye el hash de la anterior; su hash final se registra en el registro de trials. Es **tamper-evident dentro de la buena fe del Lead**, no attestación externa (limitación declarada).
11. Los mecanismos usados son los que el repositorio tiene (Git, SHA-256, timestamps, `.project/` gitignored); no se inventan mecanismos de integridad.

## 18. Límites y qué NO se concluye

- `n=2` casos; no generalización estadística. Mismo modelo y proveedor en todas las pasadas: errores correlacionados; la deliberación no aporta diversidad epistémica demostrada.
- Independencia **procedural** (commit-before-reveal, ejecución secuencial D→P, directorios separados), no epistémica; no se afirma independencia de razonamiento. No hay attestación temporal externa; el ledger es tamper-evident, no inmutable.
- **Casos pre-analizados:** ambos casos tienen análisis previos (una auditoría y un pending decision) que el frame entrega a todas las pasadas; el techo de descubrimiento es bajo por diseño. La conclusión se limita a «valor adicional sobre un baseline informado por ese análisis previo»; un resultado negativo **no** distingue «la deliberación no aporta» de «el frame ya contenía la respuesta».
- **Un solo Lead:** el Lead diseña el frame, conoce las hipótesis y ejecuta ambos trials; la revisión independiente pre-ejecución, los evaluadores/adjudicador independientes y la regla congelada reducen el sesgo, no lo eliminan.
- El baseline es un agente instruido para analizar con rigor, no el proceso normal «en vivo»; puede ser más exhaustivo que una decisión normal (sesgo en contra del valor del tratamiento) y a la vez recibir un frame formal que el proceso normal no siempre tiene.
- Coste con `GAP` de tokens/contexto; llamadas autodeclaradas; duraciones con concurrencia y latencia del Lead.
- La relación con Theoretical Execution **no se testea** aquí (§19).
- No se concluye que Jury deba desaparecer, que Adversarial Deliberation deba ser parte del Protocol, que voting sea útil, que varios jurados sean necesarios, que exista una arquitectura multi-agent necesaria, ni que el mecanismo garantice decisiones correctas. Tampoco lo contrario: `n=2` y evidencia acotada.

## 19. Relación con Theoretical Execution (hipótesis no asumida)

La pregunta «¿la deliberación adversarial agrega valor cuando se aplica después de una Theoretical Execution?» se registra como **hipótesis no testeada** en esta campaña. Ninguno de los dos casos es un plan de implementación ejecutable por TE (Case-02 es una decisión de producto/runtime; Case-03 es una decisión de gobernanza/registro), por lo que no hay `THEORETICAL EXECUTION FINDINGS → ADVERSARIAL FINDINGS → OVERLAP → NEW VALUE` que medir. No se modifica la política de TE ni se infiere nada sobre ella.

## 20. Plan de artefactos y commits

1. **Commit 1 (antes de ejecutar):** `docs/working/research/ADVERSARIAL_DELIBERATION_PREREGISTRATION_2_3_2026-10-25.md` (este documento, con Apéndices A–C) + fila en `docs/working/research/INDEX.md`. Mensaje: `docs(working): preregister adversarial deliberation campaign trials 2-3`.
2. **Ejecución** de Trial #2 y Trial #3 con artefactos de sesión en `.project/campaign/` (gitignored), ledger append-only y revisión/adjudicación/integridad.
3. **Commit 2 (después de ejecutar):** `docs/working/research/ADVERSARIAL_DELIBERATION_TRIALS_2_3_2026-10-25.md` (registro autocontenido: protocolo, selección de casos, Trial #2, Trial #3, métricas, desviaciones, limitaciones, análisis cross-trial, conclusión, recomendación arquitectónica, apéndices verbatim) + fila en `INDEX.md`. Mensaje: `docs(working): record adversarial deliberation trials 2 and 3`.
4. Sin push, sin merge, sin tag, sin release. Sin cambios en `protocol/`, `.agents/`, `runtime/`, `tools/`, `tests/`, `docs/VERSIONING.md`, `ROADMAP.md`, `CHANGELOG.md`, RFCs, ADRs ni planes.

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


## Apéndice C — Revisión independiente pre-ejecución y correcciones

# Apéndice C — Revisión independiente pre-ejecución y correcciones

**Estado de este apéndice:** se incorpora **antes** del commit 1 y antes de ejecutar cualquier pasada. Registra la revisión independiente del borrador y las correcciones aplicadas al congelar. No es un resultado experimental.

## C.1 Revisión independiente del borrador

- **Revisor:** subagente en contexto `fresh`, sin acceso a resultados de Trial #2/Trial #3 (no existían). No ejecutó trials ni la suite completa de pytest, no modificó archivos versionados y no usó web.
- **Objeto:** borrador del preregistro y sus Apéndices A/B (FRAME-2/FRAME-3), contrastados contra el HEAD `e7bc8818afed903cfc327cb98a2fcfbf7a9789ee`.
- **Veredicto del borrador:** `NOT_READY` (defectos corregibles antes de ejecutar; no un veredicto sobre el valor de la investigación).
- **Hechos verificados:** 60 filas — 41 `CONFIRMADO`, 18 `CORREGIR`, 1 `NO VERIFICABLE`.
- **Findings BLOCKING:** F-01 (taxonomía/materialidad contradictoria), F-02 (regla de decisión no determinista), F-03 (FRAME-3 con hechos falsos e incompletos), F-04 (independencia no verificable), F-05 (FRAME-2: durabilidad Git y subdirectorio no soportados).
- **Findings MATERIAL:** F-06 (ADR-19/RFC-80/productor), F-07 (costes), F-08 (reclasificación post hoc), F-09 (conteo), F-10 (atribución), F-11 (replicación/techo), F-12 (Case-03 sin lugar/autoridad/semántica), F-13 (contingencias/hashes), F-14 (taxonomía de campaña).
- **Findings MINOR:** F-15–F-18.
- **Límites declarados por el revisor:** verificación estática; no re-midió los tiempos de la auditoría; no puede verificar la ejecución futura; la revisión es adversarial y puede sobreponderar defectos corregibles.

## C.2 Disposición de los findings (aplicada antes de congelar)

| Finding | Disposición | Corrección aplicada |
|---|---|---|
| F-01 taxonomía contradictoria | **ACEPTADO** | §8 reescrito: novedad (`NEW`/`DERIVED`/`DUPLICATE`) con árbol de desempate y citas obligatorias; eje terminal de validez (`MATERIAL`/`NON_MATERIAL`/`SPURIOUS`, `SPURIOUS` reemplaza a los otros dos); `DUPLICATE+MATERIAL` definido como material absoluto sin valor nuevo; `DISTINCT_MATERIAL_NEW` definido; matriz 3×3 documentada. |
| F-02 regla no determinista | **ACEPTADO** | §10/§13/§14 reescritos: `DECISIONAL_IMPACT`/`PLAN_IMPACT`/`EVIDENCE_IMPACT` separados; clases de trial exhaustivas y mutuamente excluyentes (10 clases, tabla order); shares pooled; R1 con N≥4; H5 alineada con `NEGATIVE`/`NO_EVIDENCE`; «material falso» reclasificado como `SPURIOUS`; mapeo etiqueta↔decisión explícito. |
| F-03 FRAME-3 falso/incompleto | **ACEPTADO** | Se **reemplazó el caso** (ver C.3): el candidato de test selection se excluyó antes de ejecutar por evidencia falsa/incompleta y por no ser admisible sin decisiones de diseño ausentes. Nuevo FRAME-3 (ADR-worthiness) verificado contra el HEAD (C.4). |
| F-04 independencia no verificable | **ACEPTADO (parcial)** | Defense y Prosecution pasan a ejecutarse **secuencialmente** por trial y en directorios separados; el Lead hashea cada artefacto al recibirlo en un **ledger append-only con cadena de hashes**; se añade `INTEGRITY AUDIT` independiente; se declara «atested, not enforced» y se elimina la afirmación de verificación fuerte (§4.3, §17). Synthesis se declara pasada de tratamiento anclada al baseline cerrado y su coste se incluye (§4.1, §11). |
| F-05 FRAME-2 durabilidad/subdirectorio | **ACEPTADO** | FRAME-2 corregido: el contrato **declara** la persistencia y el repositorio **no la materializa** (GAP de durabilidad); el candidato usa la base plana de `.project/knowledge/` y no inventa subdirectorio (representación sujeta a `PC-48`/`PC-52` antes de implementar). |
| F-06 ADR-19/RFC-80/productor | **ACEPTADO** | FRAME-2 añade ADR-19 y su fila de evidencia `AE-8`; la actualización de evidencia se declara parte documental del alcance; RFC-80 se presenta como reconciliación de alcances (auditoría `:176`), no como contradicción; se añade la ausencia de productor y el beneficio condicional. |
| F-07 costes autodeclarados | **ACEPTADO** | §11: timestamps del Lead (ledger) primarios; `SELF_S` secundario `[SELF-DECLARED]`; dos ratios y regla del mayor (`EFFECTIVE`); palabras descritas como tokens por whitespace; `EFFICIENCY` sobre coste adicional; `TOTAL_COST_RATIO` eliminado; concurrencia declarada. |
| F-08 reclasificación post hoc | **ACEPTADO** | §8.3/§4.1: evaluación primaria congelada; el Lead sólo corrige errores de ancla verificados; disputas de clase al ADJUDICADOR; análisis de sensibilidad; discrepancia que cambia la campaña → `INCONCLUSIVE`. |
| F-09 conteo | **ACEPTADO** | §8.3: corpus primario distinct (dedupe cross-pass), ocurrencias secundarias; agregado pooled; cap eliminado como regla de conteo (4–10 guía; se clasifican todos); `DISTINCT_MATERIAL_NEW_BY_PASS`. |
| F-10 atribución | **ACEPTADO** | §10: cita obligatoria de IDs por cada cambio en synthesis/verdict/recommendation; verificación de cadena; contrafactual explícito; sin cita/contrafactual → `NO ATRIBUIDO`. |
| F-11 replicación/techo | **ACEPTADO** | §5.2 define «replicación controlada» como replicación de **método** con caso nuevo; §5.1.10 admite pre-analizados con techo declarado; §18 limita la conclusión a «baseline informado»; §5.4 documenta el pool y las exclusiones. |
| F-12 Case-03 sin lugar/autoridad/semántica | **ACEPTADO** | El candidato de test selection se **excluyó** (C.3). El nuevo Case-03 (ADR-worthiness) tiene objeto, lugar (ADR-22 + INDEX + ROADMAP), autoridad (`AU-6`, mantenedor) y alcance definidos en el frame. |
| F-13 contingencias/hashes | **ACEPTADO** | §16 añade contingencias (fallo/reintento/0 findings/>10 findings/artefacto modificado/lectura prohibida/costes incompletos/caso cerrado); §0 y §6 registran hashes de frames; el ledger se define en §17; Apéndice C incorporado antes del commit 1. |
| F-14 taxonomía de campaña | **ACEPTADO** | §13.3 define `CAMPAIGN_STRONG/REFORMULATED/SIGNAL_SINGLE/NONE/NEGATIVE/INVALID`; §14.5 mapea explícitamente cada etiqueta a una decisión. |
| F-15 anclas/nomenclatura | **ACEPTADO** | Correcciones de anclas en C.5 (`PLAN-129:DEC-2`, §7/§10, bootstrap único, 57/12 y 70/13, 395,26/408,95, separación Plan 178/Trial #1). |
| F-16 exclusión ADR-worthiness | **ACEPTADO** | El caso se **seleccionó** en lugar de excluirse; la razón de exclusión anterior era falsa y quedó eliminada del pool. |
| F-17 fórmulas | **ACEPTADO** | §11 corregido (TOTAL eliminado, EFFICIENCY sobre coste adicional, palabras/caracteres). |
| F-18 etiquetas/umbrales/cero | **ACEPTADO** | §7/§16 usan `OBSERVED`/`MEASURED`/`INFERRED`/`RECOMMENDED` + `GAP`; §13.1 define umbrales inclusivos y shares con 0 findings. |

## C.3 Reemplazo de Case-03 (corrección pre-freeze)

El borrador proponía como Case-03 la adopción de verificación selectiva (`TARGETED-BY-PATH`) en el bucle local. La revisión independiente demostró que: (i) el frame contenía afirmaciones factuales falsas sobre el grep y sobre los conteos de la auditoría; (ii) omitía `TEST_SUITE_AUDIT_2026-10-13.md:§11`, que ya recomienda el candidato; y (iii) el candidato no era evaluable sin decidir de antemano su lugar canónico, la autoridad del command-set, la semántica del cierre de imports y el formato del mapa —decisiones ausentes en el repositorio—. Se **excluyó el caso y se sustituyó por Case-03 (ADR-worthiness del acto del Plan 152)** antes de congelar y antes de ejecutar cualquier pasada. La sustitución no se hizo después de observar resultados (no existían) y no cambia el protocolo ni las reglas; cambia el objeto de un trial. Se registra aquí para que el lector pueda auditar la decisión.

## C.4 Verificación del FRAME-3 de reemplazo

Se ejecutó una verificación independiente y acotada del FRAME-3 de reemplazo contra el HEAD (mismos límites que la revisión principal: sólo lectura, sin trials, sin web, sin suite completa). Resultado: **`READY_WITH_CORRECTIONS`** — 0 `BLOCKING`, 2 `MATERIAL`, 8 `MINOR`; 8 puntos `CONFIRMADO`, 1 `CORREGIR`, 0 `NO VERIFICABLE`. El núcleo quedó confirmado: el acto del 2026-10-07 (`GOV-1 = C`, `GOV-2`…`GOV-9 = A`, `GOV-10 = B`, actor mantenedor, separación acto/ejecución/materialización/cierre), `F-1` abierto (owner mantenedor), la pending decision de ADR-worthiness, el blocker del ROADMAP, los criterios de ADR-16, ADR-19/20/21 `Accepted` y **ADR-22 libre**; el caso está abierto y el candidato no está materializado.

Correcciones aplicadas antes de congelar:

- **M-1 (MATERIAL):** la alternativa C («no producir ADR») no puede cerrarse «en el propio Plan/INDEX» (el Plan 152 está cerrado y un INDEX no es autoridad). Reescrita como: registro de `not ADR-worthy` en un artefacto **nuevo** post-cierre que referencia al Plan 152, más reconciliación de la fila del ROADMAP por referencia, sin editar el Plan.
- **M-2 (MATERIAL):** el protocolo citado estaba untracked en el momento del chequeo. Queda resuelto por el **commit 1**, que versiona este preregistro antes de ejecutar cualquier pasada; el frame lo declara y las pasadas reciben el hash del protocolo congelado.
- **MINOR:** se declaran los tres untracked (dos del mantenedor + el preregistro, que se commitea antes de ejecutar); se corrige la atribución del ciclo ADR (`docs/CONVENTIONS.md`/ADR-16, no `docs/AGENTS.md`); se reemplazan las anclas `§3/§4/§5` de ADR-16 (sin secciones numeradas) por `:Decisión`; se ancla el cierre del Plan 152 en `docs/plans/INDEX.md` + `docs/CONVENTIONS.md:723-724`; se aclara que `AU-6` se ancla en ADR-16 y en la policy SAE (no en `authority.md`); se precisa ADR-20 como registro directo del mantenedor; se precisan el header de ADR-22 y la resolución de `F-1` por referencia; se excluyen los artefactos de trials de la base de evidencia.

La verificación independiente del FRAME-3 no reemplaza la revisión principal: ambas se hicieron **antes** de congelar y antes de ejecutar resultados.

## C.5 Correcciones factuales del borrador

Las 18 correcciones de hechos del revisor se aplicaron en las secciones correspondientes. Las principales:

1. `.project/knowledge/` **declarado** Git-persisted por el contrato pero **no materializado** en el HEAD (`.gitignore:13`; `git ls-files .project` = 0): degradado a `GAP` de durabilidad (FRAME-2).
2. La «tensión» RFC-80 (`NOT IMPLEMENTED`) vs `11.7.0`/Plan 150 se registra como **reconciliación de alcances** (payload Protocol vs reference runtime DEV), según `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:176`.
3. La ubicación de Memory no inventa subdirectorio: base plana de `.project/knowledge/` (Plan 150) o representación resuelta por `PC-48`/`PC-52` antes de implementar.
4. Se añade la ausencia de **productor** de registros en producción (`consolidation.py` sólo consumido por tests) y el beneficio condicional de C-MEM.
5. Se añade ADR-19 y su fila de evidencia `AE-8` al FRAME-2 y al alcance documental del candidato.
6. `git grep -i "targeted"` no era como el borrador decía; el caso fue excluido, no corregido.
7. Conteos de la auditoría de tests: **57 archivos DEV + 12 harness** en la medición; HEAD **70 DEV + 13 harness**; corrida canónica DEV **395,26 s** (el total de ambos legs es 408,95 s).
8. El `1535 passed` del Plan 178 (`759f005`) se separa de la duración `587,65 s` registrada en el Trial #1 (`e7bc881`); no se atribuye la duración al Plan 178.
9. `tests/AGENTS.md`: **bootstrap único con dos entradas** (`tests/`, `tools/`), no «doble bootstrap».
10. `PC-2` → **`PLAN-129:DEC-2`** para el enforcement de placement (colisión de namespaces registrada como `<PLAN-129>:F-2`).
11. `docs/VERSIONING.md`: §7 estados/condiciones derivadas; §10 DoD; §5 changelog.
12. La exclusión de «ADR-worthiness» como caso se elimina (el caso se selecciona); el error anterior se reconoce.
13. `58`/`70` y demás conteos del borrador se corrigen a los valores medidos/verificados.
14. Las etiquetas de evidencia se unifican (`OBSERVED`/`MEASURED`/`INFERRED`/`RECOMMENDED` + `GAP`).
15. Se añaden al registro los hashes de los frames y la regla de verificación por la pasada.
16. Estado del documento: `DRAFT` → `PREREGISTRO CONGELADO` sólo en el commit 1, tras esta revisión.
17. Se elimina la afirmación de que el Lead «verifica» la no contaminación; se declara «atested, not enforced» + ledger + auditoría.
18. Se añade la tabla de decisión sintética en el INTEGRITY AUDIT para controlar exhaustividad de §13.2.

## C.6 Declaración del Lead

Apliqué las correcciones **antes** de congelar y antes de ejecutar cualquier pasada. No observé resultados de Trial #2 ni de Trial #3 antes de este apéndice (no existían). Las reglas de §8–§14 quedaron fijadas en este documento y no se modificarán después de observar resultados; cualquier desviación se registrará según §16. La revisión independiente no reemplaza la responsabilidad del Lead: donde no acepté una sugerencia, lo registré (no hubo rechazos: F-01…F-18 fueron aceptados; F-04 se aceptó parcialmente porque la attestación externa no existe en el entorno, y así se declara).


