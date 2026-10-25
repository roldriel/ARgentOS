# Trial #1 — Adversarial Deliberation (ARgentOS DEV)

> **Naturaleza:** Working / experimental (`docs/working/research/`). **No normativo.** Es evidencia y provenance, nunca autoridad.
> **Protocolo:** `ADVERSARIAL_DELIBERATION_EXPERIMENT_2026-10-25.md` (protocolo del mantenedor, registrado verbatim como Working).
> **Resultado:** **éxito fuerte marginal por la letra de §17 / beneficio sustantivo estrecho**; camino §24: **iterar / Trial #2 con hipótesis refinada**. El mecanismo **no** se adopta y ninguna conclusión de este registro autoriza cambios en `protocol/`, `.agents/` ni en el template.

## 0. Metadata, provenance y autorización

- **Trial:** #1 de la investigación «Adversarial Deliberation» (Priority 3.7; insumo local del mantenedor no versionado, no citado como `ruta:sección` por RFC-69 I2).
- **Fecha:** 2026-10-25 (America/Buenos_Aires).
- **Repositorio:** rama `dev`, HEAD `b6843bc9f13f61d94e89ad9e8bfb38b06d011095`. Árbol con dos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), preservados y **no** leídos como evidencia.
- **Objeto de deliberación:** decisión DEV real, abierta en el repositorio desde `<PLAN-178>`: incorporar o no una `Integration Surface` declarativa en `docs/plans/_TEMPLATE.md` (F-01, `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:9. Findings`). Se eligió por ambigüedad real, alternativas razonables, consecuencias verificables y evidencia disponible; no es una decisión trivial ni exige modificar el protocolo para experimentar.
- **Ejecutores:** cinco contextos `fresh` independientes + el Lead, mismo modelo (`deepseek-flash`), mismo repositorio: Lead (diseño del frame, revelación, evaluación y registro) + `baseline-analyst` (Result A) + `defense-advocate` + `prosecution-advocate` (commit-before-reveal) + `synthesis-analyst` (comparación/síntesis/veredicto) + `trial-evaluator` (evaluación experimental independiente, post-reveal). Baseline, DEFENSE y PROSECUTION declararon contextos independientes; DEFENSE y PROSECUTION no se vieron antes del reveal; la síntesis leyó sólo FRAME + las dos evaluaciones; la evaluación independiente se ejecutó después del reveal con todas las piezas. Ningún subagente modificó archivos versionados.
- **Artefactos de sesión** (`.project/case-01/`, gitignored por `.gitignore:13`; no versionados por diseño): `FRAME.md`, `ANALYSIS.md`, `DEFENSE.md`, `PROSECUTION.md`, `SYNTHESIS.md`, `EVALUATION.md`. Sus textos completos se conservan verbatim en los apéndices A–F de este registro; los hashes permiten verificar la identidad de lo comprometido antes del reveal.

| Artefacto | Rol | Palabras | Duración declarada | SHA-256 |
|---|---|---|---|---|
| `FRAME.md` | Objeto congelado | 836 | congelado 04:28:52 | `6EB8F04FE5E7B6DDEEAF61ED1DA84AA50B41B03879A69A2F6A2C47A15E8E679A` |
| `ANALYSIS.md` | Result A (baseline) | 2.385 | 5 min 48 s | `240685488404905FF43B5BB3F9735EB22D81E3EE511DC3661357111FB018E5C3` |
| `DEFENSE.md` | Pass a favor | 2.170 | 5 min 21 s | `A0A3D087123165138BB12D18CE058DCFE2FA16BF9A3BEF0CFC18AD7AF77348E9` |
| `PROSECUTION.md` | Pass en contra | 2.001 | 4 min 56 s | `E296BF9442968A9030E4EB1F097E17A7828E2C17E475B9F2A5CB1F6A32970A74` |
| `SYNTHESIS.md` | Result B (comparación/síntesis/veredicto) | 1.791 | 3 min 22 s | `789B1E1965545B28BE51D5A87ECF8D912CEDD87BD7000F65D5AFBFA0A15F0B2E` |
| `EVALUATION.md` | Evaluación experimental independiente | 2.099 | 6 min 12 s | `C180D4270C44D26A3662C9755C0E8A4B1F7142C6CB05CB8897D3DC6D7668E55C` |

- **Naturaleza de la evidencia:** `n=1`, un modelo, un repositorio. Las conclusiones son experimentales y no generalizables (§11).
- **Autorización y clasificación del Change:** instrucción directa del mantenedor (el protocolo aportado indica: «El próximo paso es ejecutar Trial #1 bajo este protocolo y registrar el resultado completo»). Clasificación declarada en el primer artifact del Change (`.agents/AGENTS.md` regla 2; RFC-75 Mecanismo 1): **Origen** = acción directa del mantenedor; **RFC-56 Class: N/A** (sin payload delta); **Change Level: L1** (coordination 0: un escritor; scope 1: un área documental, `docs/working/research/`; architectural 0; release 0; duration 0); **dominio** = DEV docs. No se creó Plan: la instrucción directa autoriza el cambio que nombra y el Change se registra por su primer artifact + el commit, precedente `docs(working): preserve change lifecycle provenance artifacts` (`2024bd1`, cuatro Working docs + INDEX, sin Plan). Si el mantenedor considera que requería Plan, el commit es reversible y un Plan posterior puede referenciar este registro sin reescribirlo (RFC-46).
- **Sin cambios fuera del registro:** `protocol/`, `.agents/`, `dist/`, `runtime/`, `tools/` y `tests/` quedan intactos; no se modifica ningún Plan, RFC, ADR ni el template.

## 1. Objeto de deliberación (FRAME)

Texto completo en **Apéndice A**. Resumen:

**QUESTION.** ¿Debe ARgentOS DEV adoptar una Integration Surface declarativa en `docs/plans/_TEMPLATE.md` para hacer verificable la continuidad de integración de las capacidades que un Change introduce o modifica?

**CANDIDATE (C-1).** Añadir al template una sección `## Integration Surface`, declarativa y sin checker ni gate, con siete campos: (1) capacidades/sistemas upstream; (2) contratos extendidos o consumidos; (3) conexiones de estado/lifecycle; (4) consumidores downstream previstos (ruta o punto de entrada); (5) evidencia de integración (comando o verificación); (6) aislamientos deliberados; (7) integraciones desconocidas o pendientes. Opcional pero esperada para Changes que introducen o modifican capacidad, mecanismo o contrato; `—`/`NO_APLICA` para Changes documentales o mecánicos. No crea estado, checker, gate, registro ni autoridad; aplica hacia adelante; reversible.

**CRITERIA.** 1) correctness / poder de detección; 2) integración con template/checkers/RFC-75/CONVENTIONS/INDEX; 3) authority; 4) maintainability; 5) cost; 6) reversibility.

**EVIDENCE BASE (14 ítems declarados).** Auditoría de continuidad de integración (`:3`, `:6`, `:7`, `:8`, `:9` F-01/F-02/F-03, `:10`, `:11`); `docs/plans/_TEMPLATE.md`; `tools/check_plan_structure.py`; `tools/check_plan_citations.py`; `docs/rfc/75-change-lifecycle.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md` §4.1/§7/§10; `.agents/workflows/change-lifecycle.md`; planes 175/176/178; `README.md`; `docs/plans/INDEX.md`; registro de gaps de TE; `docs/placement-contract.md`. Reglas: sólo lectura, evidencia anclada, prohibido citar los untracked del mantenedor, sin web, sin inventar hechos.

**Estado de partida declarado por la evidencia.** El template no contiene el campo (auditoría `:8.1`); la auditoría no autoriza ni implementa la propuesta (`:13. Conclusión`, `:15. Resultados finales`: 0 `ORPHANED`, 0 `CONFLICTING`, 2 `PARTIALLY_INTEGRATED`); `README.md:Integration Surface — an idea that is not a mechanism yet` declara el estado público; ningún checker exige esquema de secciones.

## 2. Resultado A — baseline (proceso normal)

Texto completo en **Apéndice B**. `baseline-analyst` recibió sólo el FRAME y el repositorio; no conocía el tratamiento ni otras evaluaciones.

- **DECISIÓN: `REVISE`.** Acepta la dirección del candidato con modificaciones obligatorias: (i) seis campos, con la evidencia explícitamente subordinada a `## Verificación`; (ii) el campo 7 desaparece como hogar propio y las integraciones desconocidas/pendientes se registran como pending decision existente (PC-1, `<PLAN-NN>:PC-n`); (iii) «opcional y **recomendada**» en lugar de «opcional pero esperada»; (iv) cláusula de no-autoridad/no-consumo; (v) inserción fuera del tramo leído por `tests/test_autonomy_effects_dogfood.py` (entre `## Criterios de salida` y `## Verificación`).
- **Razonamiento.** El gap F-01 es real y la auditoría demuestra que la integración es distinguible de la validación convencional (`:10.3`); hay declaraciones ad hoc en planes 165 (`:Puntos exactos de integración por capacidad`) y 175 (`:15. Integration`); no hay schema de secciones (`tools/check_plan_structure.py`) y `tools/check_plan_citations.py` solo verifica la resolución de citas (existencia, no conexión). Detecta solapamientos (campos 5/7, 1–3), y un dato que el FRAME no anticipaba: **el template no tiene `## Scope` aunque 33 planes usan `## Scope`/`## Alcance` ad hoc**.
- **Supuestos (6).** El template es lugar de una declaración por Plan, no de taxonomía; el disparador es juicio humano; el redactor declara `GAP`/PC-1 si no puede aportar evidencia; la verificación de citas es de existencia, no de conexión; el Change es docs-only (`RFC-56 Class: N/A`); la sección no reduce fallos por sí sola.
- **Riesgos (6).** Declaración decorativa; uso como prueba/autoridad de facto (precedente: `## Efectos declarados` es leída por `runtime/orchestrator/observation.py:parse_declared_effects`); segunda fuente para pendientes; aplicación inconsistente de «esperada»; drift de rutas; ruptura del test anclado; README obsoleto.
- **Alternativas (A–G).** Incluye: convención de auditoría sin template (complementaria); extender TE (rechazada); checker de integración (rechazada por ahora); piloto dentro del rollout; no hacer nada.
- **Plan (si se adopta).** Template + INDEX + README + CHANGELOG + Plan 179; verificación con checkers, `test_autonomy_effects_dogfood.py` y batería; rollout con evaluación tras 3–5 planes; ~1 sesión, 5 archivos.
- **GAP declarados.** GAP-1: la superficie no habría evitado las parciales (auditoría `:10.5`), el valor es diagnóstico; GAP-2: sin datos de adopción; GAP-3: el disparador es juicio humano; GAP-4: 33 planes usan `## Scope` ad hoc; GAP-5: impacto en adopción nulo (template DEV).
- **Hallazgo relevante del baseline sobre el FRAME:** el criterio 4 del FRAME citaba `## Scope` como sección existente del template; el template no la tiene. Error del frame registrado en §11 (desviación de protocolo), detectado por Result A y no por el tratamiento.

## 3. Resultado B — tratamiento

### 3.1 DEFENSE — `SUPPORT_WITH_CONDITIONS` (confianza MEDIUM)

Texto completo en **Apéndice C**. Ocho argumentos, cada uno con afirmación, evidencia `ruta:sección`, supuesto, criterio y materialidad:

- **D-1** el gap está demostrado y nombrado por evidencia primaria (auditoría `:8.1`, `:9` F-01, `:13 SYSTEMIC INTEGRATION-CONTINUITY GAP = YES`);
- **D-2** el contenido ya se produce ad hoc (plan 175 `:15. Integration`; matriz de gaps TE, filas `I`/`N`; plan 176), C-1 normaliza en lugar de crear;
- **D-3** el template es el punto de extensión probado (12 commits; RFC-75 `:Criterios de aceptación` cita secciones del template; `CONVENTIONS` admite omitir opcionales);
- **D-4** sin gate ni obligación; el campo de evidencia puede apoyarse en `check_plan_citations.py`;
- **D-5** un solo dueño (el Plan), sin registry ni segunda fuente (INDEX sin columna; `placement-contract.md:1`, `:23`; regla 8 de `.agents/AGENTS.md`);
- **D-6** los siete campos corresponden a la taxonomía de la auditoría (`:3`, `:6.1`, `:6.2`, `:7`);
- **D-7** precedente `## Efectos declarados` nacido opcional y hoy verificado por test/ADR-19;
- **D-8** reversibilidad y coste de la inacción (Plan 178 L2; Mecanismo 15).

**Límite explícito de la defensa:** la efectividad no está demostrada por experimento (auditoría `:10.6`); el aporte es de auditabilidad/reconstrucción, **no de detección** (`:10.5`); el template tiene 280 líneas y la ceremonia es un riesgo real; la prueba anclada recorta el texto entre `## Efectos declarados` y `## Criterios de salida`, por lo que la inserción debe caer fuera de ese tramo. Condiciones de validez: opcional no invalidante, sin checker/gate/schema/estado/registry/columna, evidencia anclable, sin duplicar `Scope`/`Efectos declarados`/`Verificación`, Plan DEV sin reescribir historia, evaluación de uso y retirada sin deuda si resulta vacía.

### 3.2 PROSECUTION — `OPPOSE_WITH_CONDITIONS` (confianza MEDIUM)

Texto completo en **Apéndice D**. Ocho objeciones (BLOCKING/MATERIAL/MINOR):

- **O-1 (BLOCKING)** el beneficio central está contradicho por la única evidencia empírica: declarar un consumidor esperado no prueba que exista; la ausencia del campo no causó las parciales; utilidad «sin experimento» (auditoría `:10.5`, `:10.6`, `:1`, `:15`);
- **O-2** la evidencia ya identifica una alternativa superior: convención de auditoría F-02, no una sección del template (`:10.5`, `:9` F-02);
- **O-3** duplicación material: campos 5 y 7 con `Verificación`/`Validation anchor` y `Findings`/`Riesgos`; 1–3 con `Depende de`/`RFC`/`Criterio de entrada`/`Lifecycle`; y **campo 6 con fronteras vivas** (`TE §13/§15`, `placement §22–§24`) que quedan históricas al `Executed`;
- **O-4** disparador indeterminable: «opcional pero esperada» sin vocabulario ni regla; sin entrada en glosario; la ausencia no distingue `NO_APLICA` de olvido; casos límite (Plan docs-only, `Tipo: Nota`, refactor sin consumer nuevo);
- **O-5** la declaración puede adquirir fuerza de aprobación o de evidencia verificada sin serlo; el Plan es el artefacto de autorización y `Scope` autoriza rutas de escritura; «previstos» sin cláusula que separe previsión de autorización;
- **O-6** dependencia omitida: `README.md` quedaría obsoleto y `change-lifecycle.md:9` exige impacto documental;
- **O-7** precedente adverso: Placement mantiene su enforcement diferido y una biblioteca sin consumidor (`placement-contract.md:22` `PC-72`/`PC-72.1`, `:24` `PC-75`; auditoría `:7`): la declaración sin mecanismo no se auto-corrige (analogía declarada);
- **O-8 (MINOR)** reversibilidad deja corpus mixto; nombre en inglés dentro de un template en español.

**Condiciones de validez de C-1** (PROSECUTION §6): requisito versionado con criterio de éxito; experimento acotado que demuestre detección de al menos una desconexión no detectada por verificación convencional; campos no duplicados, disparador determinista, semántica de ausencia, clase de evidencia y cláusula «predice, no autoriza ni verifica»; aislamiento con referencia viva; reconciliación README/glosario; F-02 primero.

## 4. REVEAL

- **Compromiso previo:** DEFENSE cerró a las `04:41:10.4677806-03:00`; PROSECUTION cerró a las `04:40:46.7727814-03:00`. Cada pasada declaró haber leído sólo `FRAME.md` dentro de `.project/case-01/` y no haber visto la otra evaluación ni comunicación entre agentes.
- **Reveal registrado por el Lead:** `2026-10-25T04:41:33.7724881-03:00`. En ese instante el Lead computó `SHA-256(DEFENSE.md) = A0A3D087…48E9` y `SHA-256(PROSECUTION.md) = E296BF94…70A4`, coincidentes con los reportados por cada pasada. La síntesis, en contexto separado, re-verificó ambos hashes a las `04:41:46` antes de leerlos.
- **Atribución:** cada argumento pertenece al documento que lo comprometió; no hubo reescritura de posiciones después del reveal.
- **Límite/GAP:** `.project/` está gitignored (`.gitignore:13`); la prueba de orden es autodeclarada (timestamps + hashes), sin attestación temporal externa. Las dos pasadas se ejecutaron en paralelo: PROSECUTION terminó a las `04:40:46` y DEFENSE a las `04:41:10`, por lo que la lectura cruzada era técnicamente posible en esos ~24 s; ambas lo niegan y no hay evidencia de contaminación. La independencia es **procesal**, no epistémica (mismo modelo, mismo frame, misma base de evidencia).

## 5. Comparación, síntesis y veredicto (Result B)

Texto completo en **Apéndice E**.

**COMPARISON por criterio.** Criterio 1 (correctness/detección): DISAGREE — ambas aceptan el hecho empírico de `:10.5` y discrepan sobre si el criterio exige detección o basta auditabilidad. Criterio 2 (integración): DISAGREE — misma evidencia leída en sentidos opuestos (aditivo vs duplicación). Criterio 3 (authority): PARTIAL — ambas ven el riesgo; discrepan sobre si los controles lo neutralizan. Criterio 4 (maintainability): DISAGREE — normalizar una forma vs reproducir el modo de fallo. Criterio 5 (cost): PARTIAL — coste bruto bajo; desacuerdo de alcance. Criterio 6 (reversibility): AGREE.

**Agreements (6):** declarar un consumidor no prueba que exista y la utilidad no está demostrada; ningún checker exige esquema de secciones; retirada reversible con legado tolerado (Mecanismo 15); la auditoría es diagnóstica y no autoriza; riesgo de declaración ritual o falso positivo; la práctica actual ya declara integración en prosa.

**Disagreements preservados (5):** DG-1 auditabilidad vs detección (criterio 1); DG-2 duplicación vs distinción semántica; DG-3 «opcional» vs obligación social; DG-4 orden F-02 → template vs template ahora; DG-5 coste docs-only vs coste documental ampliado. **Contradicciones sin arbitraje (4):** K-1 segunda fuente; K-2 campo 5 verificable; K-3 coste; K-4 ausencia interpretable.

**MATERIAL FINDINGS de la síntesis (13) + 2 `REQUIRES_NEW_EVALUATION` excluidos** (efecto de `docs/VERSIONING.md` §4.1/§7/§10; clasificación RFC-56/release del Change al template). La síntesis no introdujo evidencia nueva ni dirimió por mayoría.

**VERDICT: `UNDETERMINED`.**
**BASIS:** el gap F-01 está documentado, pero ninguna pasada demuestra que la ausencia del campo lo causara; no hay evidencia repo-anclada de detección; no habría enforcement mecánico y es reversible sin deuda; hay objeciones materiales ancladas y no refutadas (duplicación de campos, disparador indeterminable, deriva de autoridad, coste documental omitido); DEFENSE acota el beneficio a auditabilidad y declara GAP la efectividad. No hay base para `VIABLE` (criterio 1 incumplido y objeciones ancladas) ni para `NOT_VIABLE` (el bloqueo ataca una tesis que DEFENSE no sostiene; el caso estructural está en gran medida incontestado; coste bajo y reversible).
**RECOMMENDATION (advisory, no autoritativa): `GATHER_EVIDENCE`.** Experimento acotado (1–2 planes candidatos con criterio de éxito versionado) y/o convención F-02 primero; reevaluar C-1 después. No adoptar tal cual ni rechazar el concepto.

## 6. Evaluación experimental

### 6.1 Método

La evaluación la produjo `trial-evaluator` en un contexto independiente que leyó las cinco piezas del caso y verificó anclajes en el repositorio (texto en **Apéndice F**). El Lead había formado una evaluación provisional antes de encargarla; ambas coincidieron en la clasificación y el resultado, con las diferencias menores registradas en §6.7. Definiciones aplicadas literalmente:

- `DUPLICATE`: el mismo hallazgo factual (o su consecuencia material) ya está en `ANALYSIS.md`, aunque cambie la formulación.
- `MATERIAL`: nuevo (no en baseline) y, si verdadero, cambia decisión, plan, condición de aceptación o veredicto, con cambio concreto.
- `NON_MATERIAL`: nuevo y verdadero sin ese efecto.
- `SPURIOUS`: sin soporte o confusión semántica.

### 6.2 Clasificación de los 16 findings

| ID | Pass | Clase | Fundamento (ancla) |
|---|---|---|---|
| D-1 | DEFENSE | `DUPLICATE` | F-01, el gap y las parciales ya en `ANALYSIS.md:3`/§5 (auditoría `:8.1`, `:10.3`). |
| D-2 | DEFENSE | `DUPLICATE` | Declaraciones ad hoc ya en `ANALYSIS.md:3` y §5 (planes 165/175); 176/TE añaden fuentes, no el hallazgo. |
| D-3 | DEFENSE | `NON_MATERIAL` | Refuerzo: 12 commits de template, RFC-75 cita secciones del template, `CONVENTIONS` admite omitir opcionales; el baseline ya asumió el plan docs-only. |
| D-4 | DEFENSE | `DUPLICATE` | Ausencia de schema y valor del checker de citas ya en `ANALYSIS.md:3`/§5; «su evidencia queda cubierta» es overclaim (resolver citas ≠ verificar integración). |
| D-5 | DEFENSE | `DUPLICATE` | Un dueño, sin registry ni segunda fuente ya en baseline (INDEX sin columna; supuesto 1). |
| D-6 | DEFENSE | `NON_MATERIAL` | Mapeo campos↔taxonomía (auditoría `:3`, `:6.1`, `:6.2`, `:7`): detalle de diseño; el baseline ya atribuye la ganancia a los campos 4–5. |
| D-7 | DEFENSE | `DUPLICATE` | Precedente `## Efectos declarados` (runtime, test dogfood, ADR-19 `AE-4`): mismo hecho que el baseline usa como advertencia, uso inverso. |
| D-8 | DEFENSE | `DUPLICATE` | Reversibilidad sin deuda ya en baseline; Plan 178/L2 añade cuantía al mismo argumento. |
| O-1 | PROSECUTION | `DUPLICATE` | Núcleo textual idéntico a `ANALYSIS.md:3`/`GAP-1` («declarar un consumer esperado no prueba que exista»; `:10.5`). Misma evidencia, distinto peso. |
| O-2 | PROSECUTION | `DUPLICATE` | Convención F-02 es la alternativa C del baseline; «F-02 primero» es reponderación. |
| O-3 | PROSECUTION | **`MATERIAL` (marginal)** | Mayormente duplicado (campos 5, 7, 1–3 ya en baseline). **El campo 6 sí es nuevo**: los aislamientos viven en fuentes vivas (`TE §13 Boundaries`, `placement PC-72.1/PC-75`) y el Plan queda traza histórica al `Executed`; reenunciarlos los duplica y congela. Cambio concreto: referencia a la fuente viva. El sub-claim «campo 3 se confunde con `**Lifecycle:**`» es débil (ese campo es lifecycle del artefacto, `_TEMPLATE.md:12`). |
| O-4 | PROSECUTION | `DUPLICATE` | «Esperada» sin criterio ya en baseline (riesgo 3, plan iii); glosario sin entrada es cierto pero sin regla que obligue (descriptivo). |
| O-5 | PROSECUTION | `DUPLICATE` | Riesgo de lectura como aprobación/prueba ya en baseline y cubierto por la cláusula de no-autoridad; «previstos ≠ autorizados» queda dentro de esa cláusula. |
| O-6 | PROSECUTION | `DUPLICATE` | Reconciliación del README ya en baseline (paso 3 del plan, misma cita); `change-lifecycle.md:9` respalda el mismo coste. |
| O-7 | PROSECUTION | `DUPLICATE` | Precedente Placement ya citado por el baseline (§5: «precedente de declarar dirección sin mecanismo»); misma analogía, uso adverso. |
| O-8 | PROSECUTION | `NON_MATERIAL` | Corpus mixto ya en la reversibilidad del baseline; idioma débil (el template ya usa encabezados técnicos en inglés y el nombre lo fija el FRAME). |

**Conteo:** 1 `MATERIAL` (marginal), 3 `NON_MATERIAL`, 12 `DUPLICATE` (**75 %**), 0 `SPURIOUS`. Además: 1 overclaim (D-4), 2 sub-claims débiles/contestables (O-3 campo 3; O-8), 1 error de magnitud no decisivo en DEFENSE §4 («280 líneas y diez secciones»; son 280 líneas y 15 secciones `##`).

### 6.3 Material findings missed by baseline

**MF-E1 (único).** El campo 6 del candidato («aislamientos deliberados») duplica fronteras ya declaradas en fuentes normativas vivas —`.agents/policies/theoretical-execution.md:13. Boundaries` y `:15. Integration with DEV`; `docs/placement-contract.md:22` (`PC-72`, `PC-72.1`) y `:24` (`PC-75`)— y, como el Plan se convierte en traza histórica al `Executed` (`docs/AGENTS.md:Folder → class map`; RFC-46), el reenunciado no se mantiene actualizado: el campo debe **referenciar la fuente viva**, no reenunciarla.

- **Evidencia suficiente:** verificada en el HEAD por el Lead y por el evaluador independiente.
- **Ausencia en baseline:** `ANALYSIS.md:3` solo identifica solapamientos de los campos 5, 7 y 1–3; su plan (`:9`) conserva el campo 6 como «Aislamiento deliberado (frontera declarada)» sin regla de referencia; su riesgo 4 cubre drift de rutas, no de fronteras.
- **Materialidad:** `MATERIAL` marginal — cambia una fila del plan de implementación del candidato (regla de referencia), **no** la decisión, el veredicto ni la recomendación.

### 6.4 Dirección inversa: hallazgos del baseline que el tratamiento no encontró

| ID | Hallazgo de Result A | Clase (miss del tratamiento) |
|---|---|---|
| R-1 | El template no tiene `## Scope` aunque 33 planes usan ad hoc `## Scope`/`## Alcance` (verificado: 33 archivos) | `NON_MATERIAL`; relevante al criterio 4 |
| R-2 | Plan 175 `P-3` incluye un insumo local no versionado del mantenedor en su contexto | `NON_MATERIAL` (drift documental) |
| R-3 | H-11: espejo de INDEX desactualizado del cierre de TE | `NON_MATERIAL` (drift) |
| R-4 | Alternativa de extender TE, rechazada con auditoría `:10.5`/`:14` | `NON_MATERIAL` (cobertura de alternativas) |
| R-5 | Enrutar integraciones desconocidas a PC-1 | `NON_MATERIAL` (diseño) |

Ningún miss del tratamiento es material. El baseline también detectó el error del FRAME sobre `## Scope`.

### 6.5 RESULT A vs RESULT B (§14)

| Dimensión | Result A (baseline) | Result B (tratamiento) | ¿Información nueva o reponderación? |
|---|---|---|---|
| Nuevos hallazgos | F-01 + 4 defectos de forma + GAP-1…5 | 16 argumentos: 12 duplicados, 3 no materiales, 1 material (MF-E1) | Solo MF-E1 es nuevo y material. |
| Supuestos invalidados | — | Ninguno de A invalidado | Ninguno. |
| Riesgos descubiertos | 6 (decorativo, segunda fuente, aplicación, drift, test anclado, README) | Los mismos + obsolescencia del campo 6 + idioma/glosario débiles | Solo MF-E1. |
| Evidencia adicional | Plan 175 `P-3` untracked, H-11, extensión del template, `## Scope` ad hoc | 12 commits del template, RFC-75, ADR-19, ataques del Plan 176, TE `:13/:15`, PCs de Placement, glosario | De apoyo; solo TE/Placement habilita MF-E1. |
| Cambios de plan | Plan concreto: template + INDEX + README + CHANGELOG + Plan 179; 6 campos; verificación; rollout 3–5 planes | Sin plan; veredicto + condiciones (i)–(vi) y `GATHER_EVIDENCE` | B aporta 1 cambio (MF-E1); el resto no nace de hallazgos nuevos. |
| Cambio de veredicto | `REVISE` | `UNDETERMINED` | **Reponderación** del criterio 1 sobre la misma evidencia (`:10.5`). |
| Cambio de recomendación | Revisar y evaluar tras 3–5 planes | `GATHER_EVIDENCE` (experimento 1–2 planes y/o F-02 primero) | **Reponderación**, en gran parte redundante con la evaluación post-rollout que A ya incluía. |
| Desacuerdos | Decide por juicio | Preserva DG-1…DG-5 sin dirimir | DG-1/3/5 son de umbral/alcance; DG-2/4, relecturas de la misma evidencia. |

**Lectura.** El tratamiento no descubre información que cambie el veredicto del baseline: 12/16 argumentos reproducen hallazgos del baseline y su evidencia adicional es de refuerzo salvo TE/Placement, que habilita el refinamiento del campo 6. El cambio `REVISE → UNDETERMINED/GATHER_EVIDENCE` se explica por **reponderación** del criterio 1 (auditabilidad vs detección), no por información nueva. Result A es más ejecutable; Result B es más conservador y preserva desacuerdos. Convergen en lo sustantivo: no adoptar tal cual, coste bajo, reversibilidad alta, falta evidencia decisiva.

### 6.6 Hipótesis del protocolo

- **H1 (positiva): apoyada de forma mínima.** Aparece 1 problema material no detectado por el baseline (MF-E1), con evidencia suficiente y no espurio. Pero no cambia la decisión ni el veredicto: su efecto es de plan, marginal. H1 no puede declararse demostrada a nivel de decisión con `n=1`.
- **H2 (independencia): parcialmente apoyada como *adversarial reframing*.** La construcción separada produjo contenido distinto: DEFENSE aportó precedentes que el baseline no usó (extensión del template, RFC-75, ADR-19) y PROSECUTION produjo el único hallazgo material nuevo (O-3/campo 6). Pero el 75 % de los argumentos duplicó al baseline y todas las pasadas compartieron modelo, frame y evidencia: **no** se demuestra independencia epistémica.
- **H3 (negativa): parcialmente confirmada.** Se confirma la redundancia y el coste: 2,35× tiempo y 2,50× palabras para 1 hallazgo marginal; 75 % de duplicación. No se confirma el daño: 0 objeciones espurias estrictas, 0 cambios de plan innecesarios y el resultado no empeoró; el veredicto distinto no es un error, es una reponderación legítima. El balance es «coste y redundancia reales; valor material estrecho», no «más ruido que valor».

### 6.7 Reconciliación Lead ↔ evaluación independiente

- **Acuerdo:** clasificación (1 material / 3 no materiales / 12 duplicados / 0 espurios), MF-E1 como único hallazgo material, divergencia A→B por reponderación, resultado «fuerte marginal por la letra, estrecho en sustancia», camino de segundo trial con hipótesis refinada.
- **Diferencias y correcciones:** (a) el evaluador fijó el precedente Placement (O-7) como `DUPLICATE` porque el baseline ya lo citaba; el Lead concuerda tras verificar `ANALYSIS.md:5`. (b) El evaluador reportó `_TEMPLATE.md` con 222 líneas; la verificación del Lead da **280 líneas y 15 secciones `##`**. (c) El Lead añade que el sub-claim de O-3 sobre `**Lifecycle:**` es una confusión semántica (lifecycle del artefacto vs conexión de estado del sistema), sin alterar la clase del finding. (d) DEFENSE §4 reporta «diez secciones»; son 15. Ninguna de estas diferencias altera la clasificación ni el resultado.

## 7. Métricas (§16)

### 7.1 Beneficio

| Métrica | Resultado |
|---|---|
| Material findings missed by baseline | **1** (MF-E1; plan-level, marginal) |
| Invalid assumptions detected | 0 |
| Plan changes | **1** (regla de referencia del campo 6) |
| Verdict changes | 1 (`REVISE` → `UNDETERMINED`), por reponderación, no por información nueva |
| Recommendation changes | 1 (`REVISE` con plan → `GATHER_EVIDENCE`), por reponderación |
| New evidence requirements | 2 (criterio de éxito versionado; experimento acotado) |
| Integration gaps discovered | 0 |

### 7.2 Coste

| Pasada | Duración (metadata) | Palabras | Llamadas (autodeclaradas) |
|---|---|---|---|
| A — baseline | 5 min 48,1 s (348,1 s) | 2.385 | ~40 |
| D — defense | 5 min 20,8 s (320,8 s) | 2.170 | ~45 |
| P — prosecution | 4 min 55,5 s (295,5 s) | 2.001 | ~15 |
| S — synthesis | 3 min 22,3 s (202,3 s) | 1.791 | ~17 |
| **B — tratamiento** | **13 min 38,6 s agente (818,6 s)**; D y P concurrentes | **5.962 (2,50× A)** | **~77 (1,93× A)** |
| Evaluador independiente (overhead, no tratamiento) | 6 min 12 s (372 s) | 2.099 | ~26 |

- **Evaluaciones adicionales:** 3 (2 posiciones + 1 síntesis) frente a 1 baseline.
- **Trabajo adicional de síntesis:** 3 min 22 s, ~17 llamadas, 1.791 palabras.
- **Coste total del experimento medido:** 1.538,7 s de agente (25 min 39 s), 10.446 palabras, ~143 llamadas; reloj de pared desde la congelación del FRAME hasta el cierre de la evaluación: 23 min 41 s.
- **Caveat:** duración y llamadas son autodeclaradas en los artefactos; no hay telemetría de tokens/contexto (GAP).

### 7.3 Ruido

| Métrica | Resultado |
|---|---|
| Objeciones espurias estrictas | 0 |
| Argumentos duplicados | 12 de 16 (**75 %**) |
| Objeciones irrelevantes / sub-claims débiles | 2 (O-8; O-3 campo 3) |
| Overclaims | 1 (D-4) |
| Contradicciones falsas | 2 de 4 (K-2: ambos hechos son compatibles; K-3: diferencia de alcance, no conflicto) |
| Cambios de plan innecesarios | 0 |
| Cambio de decisión sin hallazgo material que lo respalde | 1 (la reponderación REVISE → GATHER_EVIDENCE) |

### 7.4 Métrica de titular

Unidad = una pasada de evaluación adicional. **1 hallazgo material plan-level por 3 pasadas adicionales ≈ 0,33/pasada; 0 hallazgos materiales que cambien la decisión/veredicto por 3 pasadas.** Equivale a ~1 hallazgo material por 818,6 s-agente adicionales o por 5.962 palabras adicionales. El beneficio no supera el coste de forma demostrada en este trial.

## 8. Resultado, clasificación de éxito y camino siguiente (§17/§24)

**Clasificación.** Por la letra de §17, **éxito fuerte marginal**: existe ≥1 problema material no detectado por el baseline (MF-E1), con evidencia suficiente, que debe cambiar el plan de implementación del candidato y no es espurio. En sustancia, el beneficio es **estrecho**: 1/16 hallazgos materiales, 0 cambios de decisión/veredicto atribuibles a información nueva, 75 % de duplicación y 2,35× coste; operativamente se acerca a **éxito parcial** («encuentra riesgos reales pero no cambia la decisión»).

**Camino §24:** `EVIDENCE POSITIVE (marginal) → ITERATE / SECOND TRIAL` con hipótesis refinada. El trial no es negativo ni estéril; tampoco justifica adoptar el mecanismo ni crear un Implementation Plan formal.

**Qué debe cambiar el Trial #2:**

1. **Hipótesis refinada:** este trial sugiere que la contribución observable de la deliberación es detectar **duplicación/obsolescencia de declaraciones** y afinar **condiciones de aceptación**, no detectar integraciones ausentes. El Trial #2 debe formular y medir esa hipótesis, no la original de «detección de gaps».
2. **Selección del caso:** elegir una decisión con consecuencias materiales y probabilidad real de que el baseline yerre (no un cambio docs-only barato, reversible y ya auditado, favorable a la convergencia).
3. **Pre-registro:** fijar antes de ejecutar el criterio de materialidad, los umbrales de éxito y el tamaño/forma de las pasadas.
4. **Corregir el FRAME:** verificar todos los hechos del frame contra el HEAD (el ejemplo `## Scope` era falso).
5. **Independencia:** usar modelos/proveedores distintos si están disponibles; como mínimo, instrumentar tokens/contexto y no depender de conteos autodeclarados.
6. **Rebuttal:** considerarlo sólo si hay un desacuerdo material concreto que pueda cambiar la evaluación; en el Trial #1 no se ejecutó (el desacuerdo DG-1 era de umbral/interpretación y la síntesis lo preservó).

**No se adopta ningún mecanismo.** No se modifica `protocol/`, `.agents/`, el template, ni se crea un Plan de implementación. La recomendación es advisory para el mantenedor.

## 9. Respuestas a las preguntas de salida (§25)

1. **¿Encuentra algo que el baseline no?** Sí: 1 hallazgo material de plan (MF-E1) y varios argumentos nuevos no materiales. También el baseline encontró cosas que el tratamiento no (§6.4).
2. **¿Ese algo es material?** Marginalmente: cambia una fila del plan de implementación del candidato, no la decisión ni el veredicto.
3. **¿La evidencia es verificable?** Sí: TE policy `:13`/`:15`, Placement `PC-72.1`/`PC-75`, template y `docs/AGENTS.md`, verificados en el HEAD.
4. **¿Cambia el plan o la decisión?** El plan del candidato sí (regla de referencia del campo 6); la decisión/veredicto no. La recomendación cambia por reponderación, no por información nueva.
5. **¿El beneficio supera el coste?** No demostrado en este trial: 2,35× tiempo y 2,50× palabras para 1 hallazgo marginal y 0 cambios de decisión.
6. **¿Genera ruido o falsos problemas?** No hay objeciones espurias estrictas ni cambios de plan innecesarios; sí 75 % de duplicación y 2 contradicciones falsas de 4. Ruido redundante, no dañino.
7. **¿La separación Defense/Prosecution aporta algo observable?** Sí, como *reframing*: la única pasada que produjo el hallazgo material fue PROSECUTION y DEFENSE aportó precedentes ausentes del baseline. No se demuestra que una única pasada no pudiera producirlo.
8. **¿Hace falta independencia entre agentes?** No demostrado: la independencia procesal bastó para producir el hallazgo; la independencia epistémica no está garantizada ni medida (mismo modelo, frame y evidencia).
9. **¿Hace falta voting?** No se usó ni se necesita para este MVP; el desacuerdo se preservó sin votos. Sigue siendo hipótesis posterior.
10. **¿Qué papel debería tener synthesis?** Reconstruir y preservar provenance/desacuerdo, no arbitrar: cumplió (sin evidencia nueva; 2 `REQUIRES_NEW_EVALUATION` excluidos), pero su veredicto `UNDETERMINED` fue casi una reformulación del desacuerdo central.
11. **¿Qué papel debería tener verdict?** Ser advisory y separado de la recomendación: `UNDETERMINED` fue informativo porque delimitó qué no está establecido; el vocabulario de 3 estados resultó suficiente aquí.
12. **¿Cómo debe tratarse el desacuerdo?** Preservarlo con provenance: funcionó (5 desacuerdos y 4 contradicciones registrados sin mayoría); falta definir qué haría accionable un desacuerdo de umbral como DG-1.
13. **¿Theoretical Execution mejora al combinarse?** **No testeado** en este MVP (fuera de alcance; §18 y §21). Queda como hipótesis para un trial posterior.
14. **¿Hay evidencia para una segunda iteración?** Sí, marginal: suficiente para refinar la hipótesis y repetir con mejor diseño y un caso más exigente; insuficiente para adoptar el mecanismo.

## 10. Qué NO se concluye (§23)

Este trial **no** permite concluir que: Jury deba desaparecer; Adversarial Deliberation deba convertirse en parte del Protocol; voting sea útil; varios jurados sean necesarios; los evaluadores sean epistémicamente independientes; exista una arquitectura multi-agent necesaria; el mecanismo deba ejecutarse en todos los planes; o que la deliberación garantice decisiones correctas. Tampoco permite concluir lo contrario (descartar el mecanismo): `n=1`, resultado positivo marginal, caso favorable a la convergencia.

## 11. Limitaciones, GAP y desviaciones de protocolo

1. **`n=1`**, sin réplica ni generalización.
2. **Mismo modelo/proveedor** en todas las pasadas: errores correlacionados; la deliberación no aporta diversidad epistémica.
3. **Independencia procesal, no epistémica:** commit-before-reveal evita contaminación declarada, pero comparten frame, repositorio y modelo; ventana de solapamiento de ~24 s entre el cierre de PROSECUTION y el de DEFENSE (lectura cruzada técnicamente posible, atestiguada como no ocurrida).
4. **Sin attestación temporal externa:** `.project/` es gitignored; los hashes son reproducibles, pero el orden y la autoría son autodeclarados.
5. **Coste autodeclarado:** duraciones y llamadas provienen de metadata interna; no hay telemetría de tokens/contexto (GAP).
6. **Desviación de protocolo (FRAME):** el criterio 4 citaba `## Scope` como sección existente del template; el template no la tiene (33 planes la usan ad hoc). El error pudo orientar a las pasadas; lo detectó el baseline, no el tratamiento. Corregido en este registro y a corregir en el Trial #2.
7. **Baseline simulado:** Result A lo produjo un agente instruido para analizar con rigor, no el proceso normal «en vivo»; pudo ser más exhaustivo que una decisión normal, lo que sesga en contra del valor del tratamiento. A la vez, recibió un FRAME formal (criterios/evidencia) que el proceso normal no siempre tiene.
8. **Caso favorable a la convergencia:** decisión docs-only, barata, reversible y ya auditada; techo bajo de descubrimiento material.
9. **Evaluación post hoc y no ciega:** el evaluador leyó A antes que B y conocía el orden; sin replicación externa.
10. **Sin rebuttal:** no se ejecutó (§7 del protocolo lo hace opcional); un desacuerdo de umbral (DG-1) quedó preservado, no direccionado.
11. **Errores menores de magnitud no decisivos:** DEFENSE «280 líneas y diez secciones» (son 15 secciones); EVALUATION «222 líneas» (son 280). No alteran ninguna conclusión.
12. **Sesgo de encuadre del Lead:** el frame, el candidato (7 campos) y la selección del caso los fijó el Lead; el Trial #2 debería pre-registrar el frame con revisión independiente.

## 12. Coste total del trial

| Componente | Valor |
|---|---|
| Pasadas de evaluación | 6 (FRAME no es pasada evaluativa; sí 1 baseline + 2 posiciones + 1 síntesis + 1 evaluación independiente + Lead) |
| Duración de pasadas medidas | 1.538,7 s (25 min 39 s) de agente |
| Palabras producidas por las pasadas | 10.446 |
| Reloj de pared (FRAME congelado → evaluación cerrada) | 23 min 41 s |
| Llamadas a herramientas (autodeclaradas) | ~143 |
| Escrituras en el repositorio por los subagentes | 5 (una por artefacto; 0 tracked modificados) |
| Commits del trial | 1 (el registro) |

El coste del protocolo, del registro y de la verificación del Lead no se midió con la misma instrumentación (GAP); es trabajo de escritura/validación, no pasadas de evaluación.

## 13. Clasificación del Change, verificación y commit

- **Change:** registro Working del Trial #1 (2 documentos nuevos + INDEX). **Origen:** acción directa del mantenedor. **RFC-56 Class: N/A** (sin payload delta). **Change Level: L1.** **Dominio:** DEV docs. **Autorización:** instrucción directa del mantenedor (el protocolo aportado ordena ejecutar el Trial #1 y registrar el resultado completo) + RFC-75 Mecanismo 1 (clasificación en el primer artifact y en el commit); precedente `2024bd1` para Working docs sin Plan. Sin Plan, sin RFC, sin ADR.
- **Superficie:** `docs/working/research/ADVERSARIAL_DELIBERATION_EXPERIMENT_2026-10-25.md` (nuevo), `docs/working/research/ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md` (nuevo), `docs/working/research/INDEX.md` (2 filas). Sin cambios en `protocol/`, `.agents/`, `dist/`, `runtime/`, `tools/`, `tests/`, `ROADMAP.md`, `CHANGELOG.md` ni planes/RFC/ADRs.
- **Documentation impact:** `NOT_REQUIRED` — el trial no deja obsoleta documentación de estado actual: confirma el estado que `README.md:Integration Surface — an idea that is not a mechanism yet` ya declara (idea registrada, no mecanismo); no se adopta nada y no hay nueva capacidad que documentar. El protocolo y el trial quedan registrados como Working.
- **Roadmap impact:** `NOT_REQUIRED` — no se crea, completa, cancela, reclasifica ni re-prioriza trabajo del mapa; la recomendación de un Trial #2 es evidencia para decisión del mantenedor, no una iniciativa declarada.
- **Verificación:** batería canónica de `docs/VERSIONING.md:4.1` sobre el árbol final (7 checkers + `pytest tests/`; `check_dist_sync.py` excluido por ser local-only y esperado rojo en `dev`). C-1/C-2/C-3: `N/A` (no hay Plan, Validation Anchor ni Checkpoint en este Change). `tests/test_repo_containment.py` incluido en pytest.

- **Resultado de la verificación (2026-10-25, árbol final con los dos documentos nuevos y el INDEX):** `check_protocol_invariants` PASS (217 archivos / 10.541 referencias); `check_plan_citations` PASS (todas las citas resuelven); `check_plan_structure` PASS (sin violaciones; 2 `GAP` advisory históricos de los Planes 157/158, preexistentes); `check_taxonomy_coherence` PASS; `check_session_artifacts` PASS; `check_version_state` PASS (warnings de tags esperados en `dev`); `check_invariants_equivalence` PASS (identidad canónica idéntica, 15 entradas); `check_enforcement_declarations` PASS (`ENF-001`…`ENF-003`); `python -m pytest tests/` → **1535 passed** (587,65 s); `tests/test_repo_containment.py` → 5 passed (re-ejecutado sobre el árbol final). `check_dist_sync.py` no se ejecuta: es local-only y se espera rojo en `dev` sin promoción. C-1/C-2/C-3: `N/A` (no hay Plan, anchor ni checkpoint). Las ediciones posteriores del propio registro (este bloque de resultados) no son leídas por la batería ni por la suite: son el registro de governance del Change, no contenido medido.

- **Commit:** un commit atómico en `dev`, `docs(working): record adversarial deliberation trial 1`, identificable por su mensaje (el árbol no embebe su propia identidad). Sin amend, merge, rebase, tag ni push. Los dos untracked preexistentes del mantenedor no se tocan.

## Apéndices — artefactos verbatim

Los apéndices A–F reproducen los artefactos de sesión tal como fueron comprometidos y usados en la evaluación. Son evidencia del trial, no autoridad. Cada bloque conserva el hash SHA-256 declarado en §0.

### Apéndice A — FRAME (objeto congelado)

# FRAME — Caso 01 (congelado)

- **Caso:** Case-01 / Trial #1 — investigación `Adversarial Deliberation` (ARgentOS DEV).
- **Fecha de congelación:** 2026-10-25 (America/Buenos_Aires).
- **Estado del repositorio:** rama `dev`, HEAD `b6843bc9f13f61d94e89ad9e8bfb38b06d011095` (árbol con dos untracked preexistentes del mantenedor: `PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md`).
- **Naturaleza:** Working / experimental. No normativo. Ninguna conclusión de este caso es autoridad.

Este FRAME es el objeto de deliberación. Es el mismo para todas las evaluaciones y **no se modifica** después de congelado.

---

## QUESTION

¿Debe ARgentOS DEV adoptar una **Integration Surface declarativa en el template de Implementation Plans** (`docs/plans/_TEMPLATE.md`) para hacer verificable la continuidad de integración de las capacidades que un Change introduce o modifica?

## CANDIDATE (C-1)

Incorporar en `docs/plans/_TEMPLATE.md` una sección nueva `## Integration Surface`, declarativa y **sin checker ni gate**, con siete campos:

1. capacidades / sistemas upstream que el Change extiende o de los que depende;
2. contratos extendidos o consumidos;
3. conexiones de estado / lifecycle;
4. consumidores downstream previstos (ruta o punto de entrada);
5. evidencia de integración (comando o verificación concreta);
6. aislamientos deliberados;
7. integraciones desconocidas o pendientes.

Propiedades declaradas de la propuesta:

- La sección es **opcional**, pero **esperada** cuando el Change introduce o modifica una capacidad, mecanismo o contrato; un Change puramente documental o mecánico puede declarar `—` / `NO_APLICA`.
- Es sólo documentación del Plan: **no** modifica el payload (`protocol/.agents/`), **no** crea estado de lifecycle, checker, gate, registro ni autoridad nueva.
- No modifica planes cerrados ni historia; aplica hacia adelante.
- Es reversible: retirar la sección del template no deja deuda estructural.

## CRITERIA

1. **correctness / poder de detección** — ¿hace verificable una propiedad que hoy se reconstruye manualmente? ¿distingue «la capacidad existe/funciona» de «la capacidad está conectada»?
2. **integration** — ¿se acopla al template vigente, al checker de planes, a RFC-75, a `docs/CONVENTIONS.md` y al INDEX sin duplicar, contradecir ni crear una segunda fuente?
3. **authority** — ¿crea obligación, gate o autoridad no otorgada? ¿La declaración podría adquirir fuerza normativa o usarse como aprobación?
4. **maintainability** — ceremonia por Plan, riesgo de declaraciones obsoletas o duplicadas (p. ej. `## Scope`, `## Efectos declarados`, `## Verificación`).
5. **cost** — esfuerzo de adopción y de mantenimiento, coste de hacer la declaración coherente con evidencia real.
6. **reversibility** — ¿puede retirarse o corregirse sin deuda estructural ni migración?

## EVIDENCE BASE

Evidencia admitida: contenido versionado del repositorio en el HEAD declarado, leído en sólo lectura. Base declarada (cada hallazgo debe anclarse a `ruta:sección` o comando/observación reproducible):

1. `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md` — §3 (taxonomía de integración), §6 (integraciones parciales Memory / Change Governance), §7 (aislamientos deliberados), §8 (gap transversal), §9 (F-01, F-02, F-03), §10 (evaluación de la hipótesis, 10.1–10.6), §11 (reparaciones no ejecutadas).
2. `docs/plans/_TEMPLATE.md` — template completo; en particular los precedentes de secciones opcionales (`## Delegación agentiva`, `## Efectos declarados`, `## Findings / Correcciones / Pending`).
3. `tools/check_plan_structure.py` — qué se exige mecánicamente a un Plan hoy (nombre, status, placeholders, espejo de INDEX; no exige esquema de secciones).
4. `tools/check_plan_citations.py` — resolución de citas `ruta:sección`/paths.
5. `docs/rfc/75-change-lifecycle.md` — contrato del Plan y mecanismos de declaración, Change Level y checkpoint (buscar las secciones pertinentes).
6. `docs/CONVENTIONS.md` — convención de plantillas, ciclo de status, `premises(D)`, Change Level, impacto documental/roadmap y cualquier requisito de secciones del Plan.
7. `docs/VERSIONING.md` §4.1 (batería canónica), §7 (estados derivados / cierre), §10 (DoD).
8. `.agents/workflows/change-lifecycle.md` — §1–§2 (clasificación y autorización), §9 (impacto documental y de roadmap).
9. `docs/plans/175-theoretical-execution-dev-v1.md` y `docs/plans/176-theoretical-execution-dev-complete.md` — planes recientes de capacidad: qué declaran sobre consumidores, integración y evidencia.
10. `docs/plans/178-integration-continuity-audit.md` — plan de auditoría reciente: declaración de scope, verificación y ausencia de declaración de consumidores.
11. `README.md` — sección «Integration Surface — an idea that is not a mechanism yet» (estado público declarado de la propuesta).
12. `docs/plans/INDEX.md` — registro de planes y columnas existentes (no hay columna de integración).
13. `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md` — gaps de TE (D-1…D-7) y filas sobre integración/autoridad/no-progress; evidencia de una capacidad reciente con gaps de integración declarados.
14. `docs/placement-contract.md` — frontera: ubicación de artefactos ≠ integración (para no confundir placement con continuidad de integración).

## EVIDENCE RULES / CONSTRAINTS

- **Sólo lectura del repositorio.** No se modifica ningún archivo versionado ni se ejecuta ningún comando que cambie el árbol (nada de `git add/commit`, ni escrituras fuera del archivo de salida propio asignado).
- **Evidencia admitida:** únicamente contenido del repositorio en el HEAD declarado y comandos de lectura (`git grep`, `git log`, `git show`, lectura de archivos). **No** se admite web, modelos externos, memoria de conversaciones previas ni conocimiento no anclado al repo.
- **`PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md` son insumos locales no versionados del mantenedor: NO son evidencia del repositorio y no pueden citarse como `ruta:sección`** (precedente `<PLAN-178>:F-2`, RFC-69 I2). Si se los menciona, debe quedar como «insumo local no versionado», sin cita.
- **No inventar hechos.** Si falta evidencia para una afirmación, declarar `GAP` explícito; no rellenar con plausibilidad.
- **Idioma:** español (términos técnicos en inglés permitidos).
- **No autoridad:** el resultado de este caso es evidencia/advisory. No autoriza cambios, no crea un Plan, no modifica el template ni el repositorio.


### Apéndice B — Result A (baseline)

# Análisis de decisión — Caso 01 (Resultado A: baseline, proceso normal)

## 1. Metadata

- **Started:** `2026-10-25T04:29:21.5142329-03:00` (America/Buenos_Aires)
- **Finished:** `2026-10-25T04:35:09.5974213-03:00`
- **Repositorio:** rama `dev`, HEAD `b6843bc9f13f61d94e89ad9e8bfb38b06d011095` (verificado con `git rev-parse HEAD`; árbol limpio salvo los dos untracked declarados en el FRAME). Única escritura: este archivo; cero comandos de Git de escritura.
- **Contexto independiente:** no participé de la redacción del FRAME, de la auditoría del Plan 178 ni de conversación previa sobre el candidato. El análisis se produjo de cero contra el HEAD declarado, sin web, sin modelos externos y sin memoria de sesiones anteriores.
- **Evidencia leída (sólo lectura):** FRAME; `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md`; `docs/plans/_TEMPLATE.md`; `tools/check_plan_{structure,citations}.py`; `docs/rfc/75-change-lifecycle.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `.agents/workflows/change-lifecycle.md`; planes 165, 175, 176 y 178; `README.md`; `docs/plans/INDEX.md`; el registro de gaps de TE; `docs/placement-contract.md`; `tests/test_autonomy_effects_dogfood.py` (detalle en §5).
- **No citado como evidencia:** `PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md` (insumos locales no versionados del mantenedor).

## 2. Re-enunciado de la decisión

¿Se incorpora en `docs/plans/_TEMPLATE.md` una sección declarativa `## Integration Surface` —siete campos, opcional pero esperada, sin checker ni gate— para hacer verificable la continuidad de integración de las capacidades que un Change introduce o modifica? Es una decisión de gobernanza DEV (el template es documentación versionada, no `protocol/.agents/`), y su objeto es la sección y su contrato declarado, no una taxonomía de estados ni un enforcement (esos son hallazgos separados: F-02 y la «convención de auditoría»).

## 3. Razonamiento

**Correctness / poder de detección.** La propiedad se reconstruye hoy a mano: la auditoría la reconstruyó para 16 capacidades y encontró 2 integraciones parciales que la validación convencional no detecta (`INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.3 ¿Es distinguible de otras verificaciones existentes?`). Varios planes ya la escriben ad hoc y en formatos distintos (Plan 165 `Puntos exactos de integración por capacidad`; Plan 175 `15. Integration`). Un campo fijo —sobre todo «consumidores downstream (ruta o entry point)» y «evidencia de integración (comando)»— fuerza la distinción `FEATURE WORKS` vs `FEATURE IS INTEGRATED`. Pero **no es verificable mecánicamente**: `tools/check_plan_structure.py` no impone esquema de secciones, y una declaración no prueba que el consumidor exista; la propia auditoría lo advierte: «declarar un consumer esperado no prueba que exista» (`...:10.5`). Queda una ganancia real pero acotada: `tools/check_plan_citations.py` escanea todos los `.md` de `docs/plans/` y verifica que las citas `ruta:sección` resuelvan; con referencias citables, la **existencia** de contratos y entry points queda comprobada —no la conexión—.

**Integration con el corpus.** El template es el lugar canónico de declaración por Plan (`docs/CONVENTIONS.md:Convenciones`, viñeta «Plantillas»). Una sección declarativa no crea estado ni registry, coherente con RFC-75, que rechazó entidades y registries (`docs/rfc/75-change-lifecycle.md:Alternativas consideradas`) y con `persist → observe → automate` (`...:Mecanismo 14 — Automation`). Hay solapamientos verificables: el campo 5 duplica el propósito de `## Verificación`; el campo 7 duplica el hogar normado de las pending decisions (PC-1, `docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`); los campos 1–3 se solapan con `P-3` y con `Depende de`. Dato que el FRAME no anticipa: el template **no tiene** `## Scope`, aunque 33 planes usan `## Scope`/`## Alcance` ad hoc: el template ya no es exhaustivo.

**Authority.** El candidato no crea autoridad, pero el repositorio muestra que una sección declarativa del template puede adquirir consecuencias operativas sin estados nuevos: `## Efectos declarados` es leída por el runtime (`parse_declared_effects`, `declared_effects_section_present`; `tests/test_autonomy_effects_dogfood.py`) y el template advierte que un Plan sin ella «no ha declarado nada sobre efectos, y una acción que puede producirlos se detiene»; sin `## Delegación agentiva`, el Plan «no delega trabajo semántico». «Sin checker ni gate» es una propiedad **de este Change**, no de la sección: debe quedar declarada y defendida, o el riesgo de leerla como aprobación o prueba de integración no es hipotético.

**Maintainability.** Siete campos por Plan son ceremonia acotada; lo caro es la coherencia con evidencia real. Las declaraciones sin verificación derivan: el Plan 175 enumera en su `P-3` un insumo local no versionado dentro del conjunto de contexto (`docs/plans/175-theoretical-execution-dev-v1.md:Derivación y premisas`), y el INDEX arrastró un espejo desactualizado de su cierre (`THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md:2. Historia de TE en el repositorio`, H-11).


**Cost.** Bajo de adopción, medio de mantenimiento. Habría que reconciliar el README, que afirma que la Integration Surface «is an idea that is not a mechanism yet» y que no existe campo hoy (`README.md:Integration Surface — an idea that is not a mechanism yet`, `README.md:Key concepts`). El coste continuo es de autoría honesta y no hay verificación mecánica nueva.

**Reversibility.** Alta y es la propiedad más sólida: retirar la sección no deja deuda estructural (sin estado, registro, checker ni migración) y los planes cerrados conservan su texto como historia (`docs/CONVENTIONS.md:Convenciones`, viñeta «Trazas históricas (RFC-46)»).

**Síntesis.** La dirección está justificada (F-01 real; dos integraciones parciales invisibles a la validación convencional; declaraciones ad hoc ya existentes; reversibilidad total), pero la forma de siete campos tiene cuatro defectos corregibles: solapamiento con `## Verificación` y con PC-1, «esperada» sin criterio observable, y «sin gate» no blindado. Corresponde **REVISE**.

## 4. Supuestos explícitos

1. El template es el lugar de una declaración por Plan; no lo es de una taxonomía ni de un registry (F-02 es un Change separado).
2. Un Change que introduce o modifica capacidad, mecanismo o contrato es identificable por juicio humano al redactar el Plan; ningún checker lo decidirá.
3. El redactor puede aportar el campo de evidencia; si no puede, declara `GAP` y registra una pending decision existente, no inventa evidencia. Los planes cerrados no se reescriben: aplica sólo hacia adelante.
4. La ganancia de `check_plan_citations.py` se acepta como verificación de existencia de referencias, no como prueba de conexión.
5. Un Change docs-only sobre el template no tiene payload delta: `RFC-56 Class: N/A`; su coste de una sesión es asumible frente al valor diagnóstico ya demostrado.
6. No se asume que la sección reduzca fallos por sí sola; su utilidad futura es cualitativa.

## 5. Evidencia utilizada

| Evidencia (`ruta:sección`) | Qué muestra |
|---|---|
| `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:8.1 No existe una Integration Surface declarativa en Implementation Plans` y `:10.3 ¿Es distinguible de otras verificaciones existentes?` | Gap F-01: sin campo ni schema; Memory y Change Governance prueban que la distinción works/integrated es real. |
| `...:10.5 ¿Son adecuadas las categorías y la noción de Integration Surface?` (con `:11 Reparaciones no ejecutadas` y `:14 Relación con Theoretical Execution`) | **Contra-evidencia central:** la ausencia no causó las integraciones parciales; declarar un consumer no prueba que exista; el mínimo sugerido es convención de auditoría, no mecanismo; no tocar TE. |
| `...:7 Aislamientos deliberados` | Precedente de convención Working no consumida (DEV Adversarial Deliberation). |
| `docs/plans/_TEMPLATE.md:Delegación agentiva` / `:Efectos declarados` / `:Verificación` y `tests/test_autonomy_effects_dogfood.py` | Secciones opcionales con consecuencia si faltan; solapamiento del campo de evidencia; un test anclado lee el template por rango de encabezados. |
| `tools/check_plan_structure.py` y `tools/check_plan_citations.py` (docstrings) | Sin schema de secciones; pero las citas `ruta:sección` de todo `docs/plans/` sí se verifican. |
| `docs/rfc/75-change-lifecycle.md:Alternativas consideradas` / `:Mecanismo 14 — Automation` / `:Mecanismo 5 — Plan lifecycle` | Sin registries/entidades; automatización sólo tras observar; matriz de governance por tipo de Plan. |
| `docs/CONVENTIONS.md:Convenciones` y `:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)` | Template canónico y secciones opcionales omitibles; historia no se reescribe; hogar normado del campo 7. |
| `docs/VERSIONING.md:4.1 Batería canónica de verificación` / `:10. Definition of Done` y `.agents/workflows/change-lifecycle.md:2. Authorization gate` / `:9. Closure and handoff` | Verificación y DoD; Change docs-only con Plan autorizado (L1+) y dos determinaciones de impacto. |
| `README.md:Integration Surface — an idea that is not a mechanism yet` / `README.md:Key concepts` y `docs/plans/INDEX.md` (encabezados) | Estado público sin campo (a reconciliar si se adopta); INDEX sin columna de integración, que no debe crearse. |
| `docs/plans/165-…:Puntos exactos de integración por capacidad`, `docs/plans/175-…:15. Integration`, `docs/plans/176-…` (header) y `docs/plans/178-…` (Objetivo, Pasos) | Integración declarada a mano en formatos distintos; planes recientes declaran scope y verificación, no consumidores. |
| `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md:2. Historia de TE en el repositorio` y `docs/placement-contract.md:22. Enforcement` / `:24. Enforcement deferred` | H-11: drift documental; placement ≠ integración; precedente de declarar dirección sin mecanismo. |
| Búsquedas: `^#{1,4} .*[Ii]ntegra` en `docs/plans/` (16); `^## (Scope\|Alcance\|Integración\|Integration)\b` (34 encabezados, 33 planes); `Integration Surface` (26); `git rev-parse HEAD` / `git status --short` | Integración ad hoc; template sin `## Scope` pese a uso extendido; término ausente de `ROADMAP.md`; HEAD y untracked verificados. |

## 6. Riesgos / modos de fallo

1. **Declaración decorativa:** el campo de evidencia se llena con «los tests pasan» y reproduce el error que la auditoría señala (verde ≠ integrado). **Uso como prueba:** la sección se cita como evidencia de integración sin comprobar el consumidor (authority de facto).
2. **Segunda fuente para pending decisions:** el campo 7 compite con PC-1 y una integración desconocida puede quedar sin owner.
3. **Aplicación inconsistente:** «esperada» sin criterio observable produce omisiones indistinguibles de `N/A`, y los autores siguen usando `## Scope` ad hoc.
4. **Drift de rutas:** consumidores que se mueven dejan declaraciones falsas con formato correcto.
5. **Ruptura de test anclado:** insertar la sección en el rango que inspecciona `test_autonomy_effects_dogfood.py` es un fallo evitable.
6. **README obsoleto:** adoptar sin reconciliar contradice `README.md:Integration Surface — an idea that is not a mechanism yet`.

## 7. Alternativas consideradas

| Alternativa | Contenido | Valoración |
|---|---|---|
| **A. No hacer nada (REJECT)** | Statu quo; F-01 abierto. | Barata, pero deja la reconstrucción manual como única vía. |
| **B. Candidato tal cual (ADOPT)** | Siete campos. | Dirección correcta, forma con defectos: duplicaciones y «sin gate» no blindado. |
| **C. Convención de auditoría sin template** (auditoría §10.5) | Tabla aplicada en auditorías. | Complementaria; el precedente de convención Working no consumida es débil. |
| **D. Candidato revisado (REVISE)** | Seis campos + referencias PC-1; «recomendada» en vez de «esperada»; cláusula de no-consumo/no-authority; ubicación neutra. | Corrige los defectos con coste marginal; mantiene reversibilidad y evita mecanismo prematuro. **Elegida.** |
| **E. Extender TE para verificar consumidores** | TE leería la superficie y detectaría consumidores inexistentes. | Rechazada: TE es DEV-only y no-gate; mecanizaría una interpretación no resuelta y crearía autoridad (auditoría §10.5, §14). |
| **F. Checker de integración** | Verificación mecánica en la batería. | Rechazada por ahora: contradice «sin checker», viola `persist → observe → automate` y no hay criterio mecánico de «consumidor exigible». |
| **G. GATHER_EVIDENCE (piloto sin adopción)** | Aplicar de facto en 3–5 planes y decidir después. | El coste es tan bajo y la reversibilidad tan alta que el piloto cabe **dentro** del rollout. |

## 8. DECISIÓN: **REVISE**

Se adopta la dirección del candidato con modificaciones obligatorias: (i) seis campos, con la evidencia de integración explícitamente subordinada a `## Verificación` (referencia, no duplicación); (ii) el campo 7 desaparece como hogar propio: las integraciones desconocidas o pendientes se registran como pending decision existente (PC-1) y se referencian por `<PLAN-NN>:PC-n`; (iii) «opcional y **recomendada**» en lugar de «opcional pero esperada», sin defecto por omisión; (iv) cláusula de no-autoridad/no-consumo (ningún checker, host ni gate la consume sin un Change autorizado separado; no es aprobación ni prueba de integración); (v) ubicación que no altere los rangos leídos por tests anclados.

El valor está demostrado como **diagnóstico** (integración declarada hoy a mano y en formatos distintos; 2 integraciones parciales invisibles a la validación convencional), el coste es bajo y la sección no crea estado ni registro, por lo que se mantiene dentro del modelo de RFC-75. Las modificaciones responden a defectos verificables del corpus sin abandonar la dirección.

## 9. Plan de implementación

**Change:** DEV-only, docs. `RFC-56 Class: N/A` (sin payload delta). `Change Level: L1` (un agente, una sesión; template + README + CHANGELOG + Plan + INDEX; sin cambio estructural ni release). Autorización: Plan `Aprobado para ejecución` (`L1` exige Plan; `.agents/workflows/change-lifecycle.md:2. Authorization gate`).

1. **`docs/plans/_TEMPLATE.md`** — insertar `## Integration Surface` entre `## Criterios de salida` y `## Verificación` (evita el corte que lee el test anclado). Contenido: comentario que la declara opcional y recomendada, sin gate ni autoridad, con la cláusula de no-consumo; tabla de seis filas (`Upstream` · `Contrato extendido o consumido` · `Conexión de estado / lifecycle` · `Consumidor downstream (ruta o entry point real)` · `Evidencia de integración (comando o verificación concreta)` · `Aislamiento deliberado (frontera declarada)`); regla de evidencia con referencias citables y `GAP` + PC-1 cuando falte; ejemplo mínimo con citas que resuelvan.
2. **`docs/plans/INDEX.md`** — fila y serie del Plan nuevo; sin columna de integración.
3. **`README.md`** — actualizar `Key concepts` e `Integration Surface — an idea that is not a mechanism yet`: campo declarativo opcional, sin checker ni gate, no probado en uso (`Documentation impact: REQUIRED`).
4. **`CHANGELOG.md`** — ítem `[Unreleased]` `(plan N, RFC-56 N/A)`.
5. **Plan nuevo** `docs/plans/179-integration-surface-declarative.md` — header completo (`RFC-56 Class: N/A`, `Change Level: L1`, `Origen` = evaluación de F-01), `premises(D)`, criterios de entrada/salida, `## Verificación`, anchor, checkpoint con `Documentation impact: REQUIRED` y `Roadmap impact: NOT_REQUIRED` (el término no aparece en `ROADMAP.md`).

**Verificación:** `check_plan_structure`, `check_plan_citations` (las citas nuevas deben resolver), `pytest tests/test_autonomy_effects_dogfood.py`, la batería canónica de `docs/VERSIONING.md:4.1` y C-1/C-2/C-3 en el cierre. **Coste:** ~1 sesión, 5 archivos (uno nuevo), 0 archivos de código. **Rollout:** sólo hacia adelante; evaluar tras los primeros 3–5 planes que la incluyan (¿se completó?, ¿la evidencia fue comando ejecutable o prosa?, ¿detectó un seam invisible a la validación convencional?) y decidir en un Change posterior si se refuerza o se retira.

## 10. Incertidumbres / GAP

- **GAP-1:** no hay evidencia de que la superficie, por sí sola, hubiera evitado las dos integraciones parciales; la auditoría afirma lo contrario (`...:10.5`). La decisión se apoya en valor diagnóstico, no preventivo.
- **GAP-2:** sin experimento ni datos de adopción no puede estimarse la tasa real de declaraciones honestas ni el coste por Plan.
- **GAP-3:** «Change que introduce o modifica capacidad» es juicio humano; sin checker, la consistencia no es medible.
- **GAP-4:** se desconoce si los autores seguirán usando `## Scope`/`## Alcance` ad hoc (33 planes) en lugar de la sección.
- **GAP-5:** sin proyecto adoptante (el template es DEV, no payload), el impacto en adopción es nulo por construcción.

## 11. Coste del análisis

- **Duración:** `04:29:21.5142329` → `04:35:09.5974213` (America/Buenos_Aires) ≈ **5 min 48 s** de reloj de pared entre las dos marcas `Get-Date` (incluye latencia de las herramientas).
- **Herramientas:** ~40 llamadas (≈ 20 lecturas, 10 búsquedas, 7 comandos `git`/PowerShell, 2 escrituras, más gestión de la tarea compartida).
- **Archivos leídos:** 19 (+ 4 instrucciones de capa inyectadas: `AGENTS.md` raíz, `docs/AGENTS.md`, `.agents/AGENTS.md`, `tests/AGENTS.md`). **Escrituras:** 1. **Comandos de Git de escritura:** 0. **Archivos versionados modificados:** 0.


### Apéndice C — DEFENSE (commit-before-reveal)

# DEFENSE — Caso 01 / Trial #1 — Caso a favor del candidato C-1

## 0. Metadata

- **Started:** `2026-10-25T04:35:49.6597348-03:00`.
- **Finished:** `2026-10-25T04:41:10.4677806-03:00`.
- **Repositorio:** `dev`, HEAD `b6843bc9f13f61d94e89ad9e8bfb38b06d011095`, sin cambios trackeados. Los dos untracked preexistentes del mantenedor no se leyeron como evidencia ni se citan.
- **Evidencia leída:** `FRAME.md`; la auditoría `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md`; `docs/plans/_TEMPLATE.md`; `tools/check_plan_structure.py`; `tools/check_plan_citations.py`; `docs/rfc/75-change-lifecycle.md`; `docs/CONVENTIONS.md:Convenciones`; planes 175, 176 y 178; la propuesta TE (`§4-§5`); `.agents/workflows/change-lifecycle.md`; `docs/placement-contract.md`; `docs/plans/INDEX.md`; `README.md`; `tests/test_autonomy_effects_dogfood.py`; `docs/adr/19-autonomy-envelope-authority.md`. Comandos: `git rev-parse HEAD`, `git branch --show-current`, `git status --porcelain`, `git log --oneline -- docs/plans/_TEMPLATE.md`, `git grep` sobre `_TEMPLATE`.
- **Contexto independiente:** redactado sólo desde FRAME.md y el repositorio en HEAD. No se abrió `ANALYSIS.md`, `PROSECUTION.md`, `SYNTHESIS.md` ni ningún otro archivo de `.project/case-01/`; sin comunicación con otros agentes; sin web, modelos externos ni memoria. Posición committed antes de cualquier reveal.
- **Alcance:** advisory; no autoriza cambios, no crea Plan, no modifica el template.

## 1. Tesis

C-1 es una intervención pequeña, declarativa y reversible sobre el artefacto que el repositorio ya usa para declarar intención (el Plan), dirigida a un gap que la auditoría primaria nombró como F-01. Su caso no exige que la sección *detecte* nada: exige que hoy la continuidad de integración se reconstruye manualmente, caso por caso y a coste alto, y que C-1 fija ese contenido donde ya vive la autorización del Change, sin checker, gate, estado, registro ni autoridad.

## 2. Argumentos numerados

### D-1. El gap está demostrado y nombrado por evidencia primaria
- **Afirmación:** C-1 no inventa un problema; el repositorio ya documentó la ausencia de una propiedad transversal de integración.
- **Evidencia:** `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:8. Gap transversal confirmado` §8.1 (el template no contiene campo `Integration Surface`; no hay campo, schema, checker ni plan que la implemente); `:9. Findings` F-01; `:13. Conclusión` (`SYSTEMIC INTEGRATION-CONTINUITY GAP = YES`); `:1. Veredicto`.
- **Supuesto:** la auditoría Working es evidencia diagnóstica válida (FRAME la declara base #1), no normativa; su fuerza es diagnóstica.
- **Criterio:** 1 y 5 (el diagnóstico ya está pagado).
- **Materialidad:** sin gap demostrado C-1 sería ceremonia; con F-01 es la respuesta mínima a un defecto registrado.

### D-2. El contenido ya se produce, disperso y ad hoc; C-1 lo normaliza y abarata
- **Afirmación:** los planes de capacidad ya declaran superficie de integración en prosa libre; C-1 traslada información existente a un lugar previsible en vez de crear trabajo nuevo.
- **Evidencia:** `docs/plans/175-theoretical-execution-dev-v1.md:15. Integration` declara upstream/downstream y aislamientos («Discovery/audit/context recovery/orchestration: **sin integración**»; «Execution: TE no participa; el host no lee TE») — campos 1, 4 y 6 de C-1; `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md:4. Matriz de gaps` filas `I` y `N` formalizan lo mismo en otra forma; `docs/plans/176-theoretical-execution-dev-complete.md:Revisión adversarial` verifica fronteras (`BOUNDARY_ATTACK`, `DEPENDENCY_ATTACK`) sin un campo donde declararlas.
- **Supuesto:** la población pertinente son planes de capacidad (base #9), no planes documentales.
- **Criterio:** 1 y 4 (una forma en lugar de N).
- **Materialidad:** si el contenido fuese netamente nuevo, el coste podría desproporcionar C-1; aquí se reduce a reubicarlo.

### D-3. El template es el instrumento vigente y probado; C-1 recorre una ruta ya usada
- **Afirmación:** añadir una sección opcional al template es operación rutinaria, docs-only y sin payload.
- **Evidencia:** `git log --oneline -- docs/plans/_TEMPLATE.md` muestra ≥11 commits de template (planes 96, 97, 122-123, 133, 159, 174); `docs/rfc/75-change-lifecycle.md:Criterios de aceptación` cita `**Change Level:**`, `## Validation anchor` y `## Checkpoint / cierre` **en el template** como evidencia de aceptación de RFC-75; `docs/CONVENTIONS.md:Convenciones` («Plantillas») permite omitir secciones opcionales; `.agents/workflows/change-lifecycle.md:3. Plan lifecycle` ordena nacer del template.
- **Supuesto:** C-1 se autoriza por la vía DEV ya usada (Plan, RFC-56 N/A, docs-only, sin `VERSION`/release por RFC-69).
- **Criterio:** 2, 5 y 6.
- **Materialidad:** el punto de extensión existe y el coste es un Change docs-only; no hace falta mecanismo ni negociación nuevos.

### D-4. No crea gate ni obligación, y su evidencia puede apoyarse en maquinaria existente
- **Afirmación:** nada convierte la sección en condición de validez, y el campo 5 («evidencia de integración: comando o verificación») queda cubierto por el checker de citas ya vigente.
- **Evidencia:** `tools/check_plan_structure.py` (docstring y `verify_all`) sólo exige nombre, status, placeholders, Amendment Log en RFCs y espejo de INDEX: **ninguna verificación de esquema de secciones**; el template no es documento numerado y queda fuera de `scan_documents`. `tools/check_plan_citations.py` escanea `docs/plans/` y resuelve `ruta:sección`, así que una evidencia anclada ya es verificable (`docs/CONVENTIONS.md:Convenciones`, «Citas verificables»). `docs/rfc/75-change-lifecycle.md:Mecanismo 10 — Authority / Conflict Resolution` y `.agents/AGENTS.md:Fundamental operating rules (always in force)` regla 3: un checker es evidencia factual, nunca autoridad.
- **Supuesto:** el texto usa la convención de citas y conserva el marcador `OPCIONAL`.
- **Criterio:** 3 (riesgo de objeción fatal) y 1 de forma derivada.
- **Materialidad:** distingue C-1 de un gate encubierto sin reducirla a prosa inerte.

### D-5. Un solo dueño —el Plan— y ninguna segunda fuente de verdad
- **Afirmación:** la sección vive donde ya vive la intención/autorización; no duplica INDEX, no crea registro ni estado.
- **Evidencia:** `docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle` (el Plan es el artefacto primario); `docs/plans/INDEX.md` (5 columnas: Plan, RFC, Status, Descripción, Vigencia; **sin columna de integración**); `docs/placement-contract.md:1. Purpose and scope` («does not define artifact content, authority, quality, review or lifecycle») y `:23. Non-goals`; `.agents/AGENTS.md:Fundamental operating rules (always in force)` regla 8 (sin registry/estado global).
- **Supuesto:** los campos referencian `**Scope:**` (en `docs/plans/_TEMPLATE.md:Delegación agentiva`), `:Efectos declarados` y `:Verificación`, sin copiarlos.
- **Criterio:** 2 y 3.
- **Materialidad:** la objeción más plausible contra un campo documental es la segunda fuente; aquí el dueño ya está asignado.

### D-6. Los siete campos corresponden a la taxonomía y a los fallos observados
- **Afirmación:** los campos reproducen la regla de evidencia de la auditoría y cubren sus dos integraciones parciales y sus cinco aislamientos deliberados.
- **Evidencia:** `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:3. Taxonomía aplicada`: `INTEGRATED` exige (a) contrato, (b) consumidor por ruta y (c) verificación → campos 1-2, 4 y 5; `:6.1` Memory y `:6.2` Change Governance se explicitan con campos 4 y 7; `:7. Aislamientos deliberados` es el campo 6.
- **Supuesto:** el autor conoce el sistema; si no, el campo 7 declara lo desconocido (disciplina `GAP`; `.agents/workflows/change-lifecycle.md:1. Change detection and classification`, «Do not invent categories»).
- **Criterio:** 1 (distingue existe/funciona de está conectada).
- **Materialidad:** convierte una lista genérica en plantilla calibrada contra errores de este repositorio.

### D-7. Preserva la opción de endurecimiento futuro sin comprometerse a él
- **Afirmación:** el repositorio ya recorrió «campo declarativo → soporte verificado» sin gate en la adopción; C-1 mantiene la opción sin gastar autoridad.
- **Evidencia:** `docs/plans/_TEMPLATE.md:Efectos declarados` nació opcional y hoy `tests/test_autonomy_effects_dogfood.py:test_the_template_declares_the_adopted_vocabulary_and_no_more` lo verifica contra política y runtime; `docs/adr/19-autonomy-envelope-authority.md` (`AE-4`) registra la declaración en el Plan; `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:11. Reparaciones no ejecutadas` deja el endurecimiento fuera de alcance por decisión.
- **Supuesto:** cualquier endurecimiento futuro tendría su propio Change autorizado.
- **Criterio:** 3 y 6.
- **Materialidad:** responde a «¿por qué no esperar un mecanismo completo?»: ya hay precedente de campo declarativo que precede a su verificación sin obligación prematura.

### D-8. Reversibilidad y relación coste/beneficio frente a la inacción
- **Afirmación:** retirar la sección no deja migración ni estado, y la inacción ya costó una reconstrucción completa.
- **Evidencia:** `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy` (ausencia de campos nuevos = legacy, no invalidez); `docs/CONVENTIONS.md:Convenciones` (planes ejecutados como traza; opcionales omitibles); `docs/plans/178-integration-continuity-audit.md:Validation anchor` documenta el esfuerzo manual de reconstruir consumidores (**Change Level L2**, 12 suites y búsquedas ad hoc) para un solo informe.
- **Supuesto:** mantenimiento acotado (una declaración por Plan de capacidad, reutilizando evidencia de `## Verificación`).
- **Criterio:** 6 y 5.
- **Materialidad:** la comparación relevante es C-1 contra el coste ya incurrido y contra el coste de un mecanismo con enforcement.

## 3. Supuestos necesarios

1. La sección es **opcional** y su ausencia nunca es invalidez (marcador `OPCIONAL`, como las otras secciones opcionales del template).
2. Sin checker, gate, schema ni columna de INDEX; verificación humana sobre la batería existente.
3. El campo 5 usa comandos concretos o `ruta:sección` resoluble.
4. Referencia cruzada —no copia— de `**Scope:**`, `## Efectos declarados` y `## Verificación`; el campo 1 distingue dependencia de capacidad/contrato de la secuencia que ya declara `**Depende de:**`.
5. «Esperada» sólo para Changes que introducen o modifican capacidad, mecanismo o contrato; documental/mecánico declara `—`/`NO_APLICA`.
6. Adopción por Plan DEV propio (RFC-56 N/A, docs-only), sin reescribir planes cerrados, y evaluación tras un número razonable de planes con retirada si resulta ceremonia vacía.

## 4. Evidencia de soporte y evidencia que limita

**Soporte:** la clase de problema existe y la validación convencional no la ve (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:8. Gap transversal confirmado`, `:10.3`, `:10.4`); el template es el punto de extensión estable (`docs/rfc/75-change-lifecycle.md:Criterios de aceptación`); el contenido ya se produce (D-2); la maquinaria existente no obstaculiza (D-4); el README ya declara que la idea no es mecanismo (`README.md:Integration Surface — an idea that is not a mechanism yet`), así que C-1 no promete nada nuevo hacia afuera.

**Límite declarado:** la misma auditoría acota: «la evidencia no demuestra que su ausencia haya causado las dos integraciones parciales» y «por sí sola no detectaría un seam latente: declarar un consumer esperado no prueba que exista» (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.5`); la utilidad a largo plazo figura entre lo no evidenciado (`:10.6`). C-1 mejora **auditabilidad y reconstrucción**, no detección. Además, el template tiene 280 líneas y diez secciones: la ceremonia por Plan es riesgo real (criterio 4), y la prueba anclada recorta el texto entre `## Efectos declarados` y `## Criterios de salida`, por lo que la inserción debe caer fuera de ese tramo. **GAP:** no existe experimento en el repositorio que mida si una Integration Surface declarativa mejora outcomes; esta defensa se apoya en diseño y precedentes, no en resultados medidos.

## 5. Por qué las alternativas inferiores pierden

- **A) Checker/gate de integración.** Crea obligación y autoridad no otorgadas (criterio 3) y la clasificación «no es completamente mecánica: requiere establecer qué consumidor era exigible» (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.2`); marcaría como huérfanos aislamientos deliberados (TE, Placement, Architecture Evolution) (§7). C-1 captura la auditabilidad sin ese riesgo.
- **B) Taxonomía transversal como mecanismo/registry.** El informe la destina a «convención de auditoría, no como state machine, registry ni autoridad nueva» (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:9. Findings` F-02) y `.agents/AGENTS.md:Fundamental operating rules (always in force)` regla 8 prohíbe registries en DEV.
- **C) Columna de integración en `docs/plans/INDEX.md`.** El INDEX es registro/navegación, nunca autoridad (`docs/CONVENTIONS.md:Convenciones`; `docs/AGENTS.md`) y su tabla sostiene el mirror de `tools/check_plan_structure.py`; la columna duplicaría la fuente.
- **D) Reparar primero Memory/Change Governance.** Fuera de alcance por decisión, con F-03 como decisión de producto pendiente (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:9. Findings`, `:11. Reparaciones no ejecutadas`); exigiría autoridad no otorgada. C-1 aplica hacia adelante sin prejuzgar F-03.
- **E) No hacer nada.** Ya se pagó: un Change L2 y una auditoría de 16 filas, cuyo resultado es un informe Working que no se repite por Plan (`docs/plans/178-integration-continuity-audit.md:Validation anchor`).
- **F) Elevar la auditoría Working a norma.** Un Working no es target normativo y no se actualiza por Plan; usarlo como formato obligatorio crearía autoridad fuera de lugar. C-1 toma la forma, no la autoridad.

## 6. Riesgos controlados y condiciones de validez

- **R-1 Deriva a obligación.** Controlado por supuestos 1-2 y por el precedente de secciones opcionales; *condición:* la governance no eleva la sección a requisito.
- **R-2 Declaración vacía.** Riesgo real; sólo parcialmente controlado por el supuesto 3 y el coste de escribir rutas. *Condición honesta:* C-1 no puede impedir una declaración ritual.
- **R-3 Duplicación** con `Scope`/`Efectos declarados`/`Verificación`. Controlado por el supuesto 4; semánticamente distinta (consumidores/contratos/conexiones vs. rutas/efectos/comandos).
- **R-4 Ceremonia por Plan.** Controlado por el supuesto 5 (N/A en una línea) y porque la información ya se escribe.
- **R-5 Quedar como «idea» permanente.** Señalado por README y auditoría; controlado por el supuesto 6, no eliminado.
- **R-6 Falsa sensación de verificación.** Controlado por el supuesto 2 y por regla 3 de `.agents/AGENTS.md`: la sección declara, no certifica.

## 7. COMMITMENT

**SUPPORT_WITH_CONDITIONS — confianza MEDIUM.**

El soporte estructural es fuerte (gap documentado; integración clara con template, autorización e INDEX; coste docs-only; reversibilidad real; sin gate ni autoridad). No es HIGH porque la **efectividad** no está demostrada por experimento (`docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.6`) y su contribución principal es de auditabilidad, no de detección (`:10.5`): hace visible y reconstruible la superficie, no prueba que la conexión exista.

**Condiciones de validez (si alguna falla, el soporte cae):** (1) sección opcional con ausencia no invalidante; (2) sin checker/gate/schema/estado/registry/columna de INDEX; (3) campo de evidencia con comandos o `ruta:sección` resolubles; (4) sin duplicar `Scope`/`Efectos declarados`/`Verificación`; (5) adopción por Plan DEV (RFC-56 N/A) sin reescribir historia; (6) evaluación de uso y retirada sin deuda si resulta vacía.

**Qué cambiaría el veredicto:** que la sección se volviera obligatoria o ganara enforcement sin autorización; que la evidencia del campo 5 no fuera anclable; que duplicara `Verificación`/`Scope`; o que un experimento mostrara que no mejora la reconstrucción actual.

## 8. Coste de esta evaluación

- **Duración:** ~5 min 20 s (04:35:49 → 04:41:10 America/Buenos_Aires), incluyendo lectura, redacción, ajuste de longitud y verificación.
- **Llamadas a herramientas:** ~45 (lecturas, búsquedas, `git` de sólo lectura, escritura, hash, cierre de tarea).
- **Archivos leídos directamente:** 16; más referencias por búsqueda (planes 114, 116, 123; ADR-19) y salidas de `git log`/`git grep`.
- **Escrituras:** sólo `.project/case-01/DEFENSE.md`; ningún archivo trackeado modificado; ningún comando de escritura Git.


### Apéndice D — PROSECUTION (commit-before-reveal)

# PROSECUTION — Caso 01 / Trial #1 (C-1, Integration Surface)

## 1. Metadata

- **Started:** `2026-10-25T04:35:51.2479233-03:00`
- **Finished:** `2026-10-25T04:40:46.7727814-03:00`
- **Rol:** PROSECUTION (caso en contra de C-1, `.project/case-01/FRAME.md`).
- **Repositorio:** rama `dev`, HEAD `b6843bc9f13f61d94e89ad9e8bfb38b06d011095` (`git rev-parse HEAD`).
- **Evidencia leída (sólo lectura):** la auditoría `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md` (completa); `docs/plans/_TEMPLATE.md` (completo); `tools/check_plan_structure.py`; `tools/check_plan_citations.py`; `docs/CONVENTIONS.md` (Plantillas y Vía de autorización por Note); `docs/AGENTS.md`; `docs/placement-contract.md` §22–§24; `docs/glossary/terms.md`; `README.md`; `docs/plans/INDEX.md`; Planes 175 (§15), 176 y 178; `docs/working/proposals/THEORETICAL_EXECUTION_DEV_SCOPE_AND_GAPS_2026-10-24.md`; `.agents/workflows/change-lifecycle.md` §9; `.agents/policies/theoretical-execution.md` §1/§13/§15.
- **Independencia:** contexto independiente. Sólo he leído `FRAME.md` dentro de `.project/case-01/`; **no** he leído `ANALYSIS.md`, `DEFENSE.md`, `SYNTHESIS.md` ni ningún otro archivo de ese directorio, ni he visto evaluación previa. El tablero de tareas anuncia su existencia, no su contenido. No me comuniqué con otros agentes.
- **Restricción cumplida:** no se citan `PRIORITY.md` ni `docs/planificacion-argentos-diseno-2026-10-13.md` como evidencia.

## 2. Objeciones numeradas

### O-1 — El beneficio central («hacer verificable la integración») está contradicho por la única evidencia empírica disponible. **BLOCKING**

- **(a) Afirmación:** C-1 no hace verificable la continuidad de integración: registra una intención. Declarar un consumidor esperado no prueba que exista.
- **(b) Evidencia:** `docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.5 ¿Son adecuadas las categorías y la noción de Integration Surface?` — «declarar un consumer esperado no prueba que exista»; y la ausencia del campo no causó las dos parciales. `:10.6 Qué queda sin evidencia suficiente` — utilidad «sin experimento». `:1. Veredicto` y `:15. Resultados finales`: 0 `ORPHANED`, 0 `CONFLICTING`; las parciales son Memory y Change Governance (seam/decisión, no declaración).
- **(c) Supuesto atacado:** que la falta de campo en el template es la causa del gap y que añadirlo acerca la verificación.
- **(d) Criterio afectado:** 1 (correctness / poder de detección).
- **(e) Materialidad:** es el criterio que define el valor. Con poder de detección demostrado nulo y otra vía recomendada por la evidencia, la decisión cambia de ADOPT a GATHER_EVIDENCE/REVISE.
- **(f) Severidad:** BLOCKING.

### O-2 — La evidencia ya identifica una alternativa superior: la convención de auditoría (F-02), no una sección del template. **MATERIAL**

- **(a) Afirmación:** el paso mínimo que la evidencia sí sugiere es una convención de auditoría con tabla `capacidad → contrato → lifecycle → implementación → consumer → verificación`, con evidencia por fila; adoptar primero el campo invierte el orden y preempta la taxonomía.
- **(b) Evidencia:** `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.5` («paso mínimo es una convención de auditoría…»), `:9. Findings` F-02 (taxonomía como convención, no state machine) y `docs/plans/178-integration-continuity-audit.md:12. Trazabilidad`.
- **(c) Supuesto atacado:** que el template es el vehículo correcto y suficiente, adoptable antes de la taxonomía.
- **(d) Criterio afectado:** 1 y 2.
- **(e) Materialidad:** la convención es más barata, no altera la estructura de todos los Planes nuevos y genera la evidencia faltante; cambia la recomendación.
- **(f) Severidad:** MATERIAL.

### O-3 — La sección duplica declaraciones existentes y compite con las fuentes vivas de aislamiento. **MATERIAL**

- **(a) Afirmación:** el campo 5 («evidencia de integración: comando o verificación») duplica `## Verificación` y el command-set del `## Validation anchor`; el 7 («integraciones desconocidas o pendientes») duplica `## Findings / Correcciones / Pending` (PC-1) y `## Riesgos`; los campos 1–2 se solapan con `**Depende de:**`, `**RFC:**` y `## Criterio de entrada`; el 3 se confunde con `**Lifecycle:**`; el 6 duplica fronteras vivas (policies/contracts/tests) que, declaradas sólo en un Plan, quedan históricas al `Executed`.
- **(b) Evidencia:** `docs/plans/_TEMPLATE.md:171 Verificación`, `:176 Validation anchor`, `:229 Findings / Correcciones / Pending`, `:269 Riesgos`, `:137 Efectos declarados`; `docs/AGENTS.md:Lifecycle`; `.agents/policies/theoretical-execution.md:13. Boundaries` y `:15. Integration with DEV`; `docs/placement-contract.md:22. Enforcement` (`PC-72`, `PC-72.1`, `PC-75`) y `:24. Enforcement deferred`.
- **(c) Supuesto atacado:** que la sección es aditiva sin duplicar («no crea una segunda fuente»).
- **(d) Criterio afectado:** 4 (duplicación/obsolescencia; el FRAME nombra `## Efectos declarados` y `## Verificación`) y 2.
- **(e) Materialidad:** reproduce exactamente el modo de fallo que el criterio 4 pide descartar: dos lugares para la «evidencia», dos para pendientes y una frontera viva duplicada en un plan histórico, sin checker que reconcilie; obliga a rediseñar el mapeo de campos.
- **(f) Severidad:** MATERIAL.

### O-4 — El disparador es indeterminable y la ausencia de la sección indistinguible de un olvido. **MATERIAL**

- **(a) Afirmación:** «opcional pero esperada cuando el Change introduce o modifica una capacidad, mecanismo o contrato» carece de vocabulario y de regla de derivación, a diferencia de los demás campos del header. Sin checker ni regla, la ausencia no significa nada: no se distingue `NO_APLICA` de omisión.
- **(b) Evidencia:** `docs/plans/_TEMPLATE.md:14`–`:26` (campos con regla explícita) frente a la propuesta; `tools/check_plan_structure.py` (checks 1–6: nombre, status, placeholders, Amendment Log, espejo y estado en INDEX; **ninguna verificación de secciones**); `docs/glossary/terms.md` sin entrada `Integration Surface` (`git grep` sin coincidencias); casos límite: Plan docs-only de governance (Plan 178), Plan `Tipo: Nota` con contenido mínimo cerrado (`docs/CONVENTIONS.md:Change Lifecycle — Vía de autorización por Note`), refactor sin consumer nuevo.
- **(c) Supuesto atacado:** que el autor puede decidir de forma reproducible si aplica y que la ausencia es interpretable.
- **(d) Criterio afectado:** 3 y 4.
- **(e) Materialidad:** sin disparador determinista el corpus futuro no es comparable ni auditable en la omisión; exige una regla de aplicabilidad y semántica de ausencia.
- **(f) Severidad:** MATERIAL.

### O-5 — La declaración puede adquirir fuerza de aprobación o de evidencia verificada sin serlo. **MATERIAL**

- **(a) Afirmación:** el Plan es el artefacto de autorización y `Scope` autoriza rutas de escritura. Añadir «consumidores downstream previstos (ruta)» sin cláusula que separe previsión de autorización, y «evidencia» sin clase de evidencia, invita a leer la sección como aprobación o verificación; la declaración es como máximo `attestation`, la clase más débil.
- **(b) Evidencia:** `docs/plans/_TEMPLATE.md:137 Efectos declarados` (declarar donde vive la autorización; `Effect` ortogonal a `Scope`) y `:104 Delegación agentiva`; `README.md:Key concepts` («or, weakest, the agent's own attestation»); `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.2` (la clasificación exige juicio, no es mecánica).
- **(c) Supuesto atacado:** que una sección declarativa sin gate no puede usarse como aprobación.
- **(d) Criterio afectado:** 3 (authority).
- **(e) Materialidad:** citada como evidencia produce un falso positivo estructural; leída como autorización produce autoridad no otorgada. Cualquiera cambia el criterio 3.
- **(f) Severidad:** MATERIAL.

### O-6 — Dependencia omitida: dejaría obsoleto el estado público que el repo declara hoy. **MATERIAL**

- **(a) Afirmación:** C-1 no menciona las actualizaciones documentales que su adopción exige; `README.md` declara hoy que Integration Surface es «an idea that is not a mechanism yet» y «only in untracked maintainer notes; not implemented».
- **(b) Evidencia:** `README.md:Integration Surface — an idea that is not a mechanism yet` y la fila de `README.md:Key concepts`; `.agents/workflows/change-lifecycle.md:9. Closure and handoff` (§9.2.a incluye `README.md` entre los documentos que deben quedar correctos; `Documentation impact: REQUIRED` no puede quedar vacío).
- **(c) Supuesto atacado:** que la adopción es un diff local del template sin efectos fuera de él.
- **(d) Criterio afectado:** 5 (cost) y 2.
- **(e) Materialidad:** amplía alcance y coste real (template + README + reconciliación en el mismo Change o `DEFERRED` con owner); ignorarlo contradice la regla de cierre.
- **(f) Severidad:** MATERIAL.

### O-7 — Precedente adverso: en este repo las superficies declarativas sin consumidor quedan diferidas, no verificadas. **MATERIAL (analogía declarada)**

- **(a) Afirmación:** el contrato de placement autorizó su enforcement como dirección futura, materializó una biblioteca de solo lectura y hoy sigue sin consumidor automático; el patrón «declaración sin integración» ya existe y no se auto-corrige.
- **(b) Evidencia:** `docs/placement-contract.md:22. Enforcement` (`PC-72`, `PC-72.1`: biblioteca no integrada; `PC-75`) y `:24. Enforcement deferred`; `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:7. Aislamientos deliberados` (Placement: `DEFERRED CONSUMER`).
- **(c) Supuesto atacado:** que una declaración opcional se mantiene viva sin mecanismo que la consuma.
- **(d) Criterio afectado:** 4 y 5.
- **(e) Materialidad:** si la mantenibilidad ya falló en el caso comparable más cercano, el criterio 4 no puede asumirse benigno. Es analogía, no prueba causal sobre C-1.
- **(f) Severidad:** MATERIAL.

### O-8 — Reversibilidad y forma. **MINOR / no decisiva**

- **(a) Afirmación:** retirar deja un corpus mixto (no hay migración, pero sí un período de aplicabilidad); además, `## Integration Surface` en inglés dentro de un template en español incumple la regla de idioma de `docs/plans/`.
- **(b) Evidencia:** `docs/AGENTS.md:Lifecycle`; convención de legado `RFC-75 Mecanismo 15` citada en `docs/plans/_TEMPLATE.md:229`; `docs/AGENTS.md:Idiomas y citas`.
- **(c) Supuesto atacado:** que retirar no deja rastro interpretativo y que el nombre es neutro.
- **(d) Criterio afectado:** 6 y 2.
- **(e) Materialidad:** baja; el repo absorbe el legado y el nombre es forma. No cambia la decisión por sí sola.
- **(f) Severidad:** MINOR.

## 3. Supuestos de C-1 que no se sostienen o no están probados

1. **«Declarar hace verificable»** — contradicho por `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.5`.
2. **«El gap F-01 causó las parciales» y «la adopción es barata»** — la auditoría niega lo primero (`:10.5`) y declara la utilidad sin experimento (`:10.6`); no hay caso repo-anclado de necesidad.
3. **«Es aditiva sin duplicar»** — falso para los campos 5 y 7 (O-3).
4. **«El disparador es determinable»** — sin vocabulario ni regla (O-4).
5. **«No crea obligación»** — `docs/CONVENTIONS.md:Convenciones` (bullet Plantillas): todo Plan nace del template con estructura completa y sólo las secciones opcionales pueden omitirse; «esperada» queda como obligación social no verificable. **GAP**: sin evidencia de cumplimiento.

## 4. Evidencia en contra (síntesis)

- Cero `ORPHANED`/`CONFLICTING`; valor diagnóstico no atribuible a la falta de declaración (`INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:1. Veredicto`, `:15. Resultados finales`).
- La auditoría no autoriza ni implementa la propuesta (`:13. Conclusión`); su única formulación vive en insumo no versionado (`:8.1`), sin criterio de éxito versionado.
- Ningún checker exige esquema de secciones (`tools/check_plan_structure.py`); las citas resuelven, pero no prueban consumidores (`tools/check_plan_citations.py`).
- La práctica actual ya declara integración en prosa cuando importa (`docs/plans/175-theoretical-execution-dev-v1.md:15. Integration`), sin campo del template.

## 5. Alternativas superiores

1. **Convención de auditoría F-02 en la validación/cierre** (tabla con evidencia por fila). Evidencia: `INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md:10.5`, `:9. Findings` F-02. No toca el template, define el vocabulario y produce la evidencia faltante.
2. **Experimento acotado**: aplicar la sección en 1–2 Planes candidatos (o borrador Working) y medir si revela una desconexión no detectada por verificación/auditoría convencional; luego decidir. Es el paso que `:10.6` declara faltante.
3. **No cambio**, resultado válido y honesto: README ya declara el estado real y `AGENTS.md:Decision-Making Compass` admite que no cambiar es un resultado respetado.
4. Si se quiere mecanismo, con la taxonomía estabilizada y autorización propia, no como efecto lateral del template.

## 6. Condiciones de validez / invalidez

**C-1 pasa a ser válido si:** (i) un artefacto versionado registra el requisito y su criterio de éxito (no un insumo untracked); (ii) un experimento acotado demuestra que la declaración detecta al menos una desconexión no detectada por `## Verificación`/auditoría; (iii) cada campo mapea a un concepto distinto (sin duplicar Verificación, Pending, Depende de, Efectos declarados), con disparador determinista, semántica de ausencia, clase de evidencia y cláusula «predice, no autoriza ni verifica»; (iv) el aislamiento deliberado referencia su fuente viva; (v) el Change reconcilia README/glossary con impacto documental; (vi) la taxonomía F-02 se define primero.

**C-1 deja de ser válido si:** se adopta como evidencia verificada; se adopta sin taxonomía; se convierte en requisito de facto sin regla de aplicabilidad; o se usan consumidores «previstos» como autorizados.

## 7. COMMITMENT

**OPPOSE_WITH_CONDITIONS** — confianza **MEDIUM**.

Fundamento: la propuesta no cumple el criterio 1 con la evidencia disponible (su único estudio empírico declara que la declaración no detecta seams y que la utilidad es GAP), duplica materialmente secciones existentes (criterio 4) y conlleva riesgo de autoridad/atestación (criterio 3), omitiendo costes de reconciliación (criterio 5). No es rechazo del concepto: es oposición a adoptarlo ahora y en la forma declarada. Confianza MEDIUM (no HIGH) porque el coste es bajo y reversible y una versión revisada (§6) podría ser defendible.

**Invalidación de esta posición:** retiro la oposición si aparece evidencia repo-anclada de un caso real donde una Integration Surface evitó o detectó una desconexión que la verificación convencional no detectaba, o si el mantenedor autoriza un experimento acotado con medición y reconciliación documental.

## 8. Coste de esta evaluación

- **Duración:** ~4 min 55 s (04:35:51 → 04:40:47, hora local).
- **Llamadas a herramientas:** ~15.
- **Archivos leídos:** 18, más búsquedas `git grep` sobre el corpus.
- **Escrituras:** únicamente este archivo; ningún archivo versionado modificado.


### Apéndice E — SYNTHESIS (comparación, síntesis y veredicto)

# SYNTHESIS — Caso 01 / Trial #1 (C-1, Integration Surface)

Síntesis comparativa y veredicto advisory sobre `.project/case-01/FRAME.md`. No decide, no autoriza, no crea Plan ni modifica el template.

## 1. Metadata

- **Started:** `2026-10-25T04:41:46.8852059-03:00`. **Finished:** `2026-10-25T04:45:25.0014524-03:00`.
- **Leídos:** `FRAME.md`, `DEFENSE.md`, `PROSECUTION.md`. No se abrió `.project/case-01/ANALYSIS.md` ni ningún otro archivo del caso.
- **SHA-256 (`Get-FileHash -Algorithm SHA256`):** `DEFENSE.md` = `A0A3D087123165138BB12D18CE058DCFE2FA16BF9A3BEF0CFC18AD7AF77348E9`; `PROSECUTION.md` = `E296BF9442968A9030E4EB1F097E17A7828E2C17E475B9F2A5CB1F6A32970A74`; `FRAME.md` = `6EB8F04FE5E7B6DDEEAF61ED1DA84AA50B41B03879A69A2F6A2C47A15E8E679A` (referencia). Los dos primeros coinciden con los declarados.
- **Reveal:** `2026-10-25T04:41:33-03:00`; DEFENSE Finished `2026-10-25T04:41:10.4677806-03:00` y PROSECUTION Finished `2026-10-25T04:40:46.7727814-03:00`, ambos anteriores.
- **Provenance:** `.project/` está excluido por `.gitignore:13` y no tiene commit Git; la constancia de compromiso previo se apoya en los hashes reproducidos y en los timestamps Finished. **GAP:** sin attestación temporal de terceros.
- **Contexto independiente:** sólo los tres archivos y comandos de sólo lectura; sin comunicación, web, modelos externos ni memoria previa; no se citan `PRIORITY.md` ni `docs/planificacion-argentos-diseno-2026-10-13.md`. Escritura: sólo este archivo.

## 2. REVEAL

Ambas posiciones estaban comprometidas antes del reveal: `DEFENSE.md` declara cierre a las 04:41:10 sin abrir `PROSECUTION.md`; `PROSECUTION.md` declara cierre a las 04:40:46, haber leído sólo `FRAME.md` y no haber visto evaluación previa. Ninguna pasada vio la otra; la atribución se hace por documento que autoriza cada argumento, y los hashes verificados coinciden con los registrados.

## 3. COMPARISON

| # | Criterio | DEFENSE | PROSECUTION | Valoración | Razón |
|---|---|---|---|---|---|
| 1 | correctness / detección | Cumple vía auditabilidad y reconstrucción; no detecta seams (§4). | Falla: registra intención, no prueba el consumidor (O-1, BLOCKING). | **DISAGREE** | Ambas aceptan el hecho empírico (§10.5) y discrepan sobre si el criterio exige detección o basta auditabilidad. |
| 2 | integration | Aditiva, un dueño, sin segunda fuente (D-3, D-5). | Duplica materialmente; F-02 primero (O-2, O-3). | **DISAGREE** | Mismo template y misma convención citados en sentidos opuestos. |
| 3 | authority | Sin gate ni obligación; `OPCIONAL` (D-4, D-7). | Obligación social, atestación y lectura como aprobación (O-4, O-5). | **PARTIAL** | Ambas ven el riesgo; difieren en si los controles lo neutralizan. |
| 4 | maintainability | Normaliza una forma; `—` en una línea; ceremonia real admitida (D-2, D-6). | Reproduce el modo de fallo: duplicación, disparador, precedente (O-3, O-4, O-7). | **DISAGREE** | Discrepan sobre el saldo neto; ambas reconocen ceremonia. |
| 5 | cost | Bajo, docs-only, contenido ya producido (D-3, D-8). | Mayor: template + README + glosario; coste de oportunidad (O-2, O-6). | **PARTIAL** | Acuerdo en coste bruto bajo; desacuerdo en alcance y comparación. |
| 6 | reversibility | Real, sin migración ni estado (D-8). | Reversible; deja corpus mixto (O-8, MINOR). | **AGREE** | Coinciden; la diferencia es menor y no decisiva. |

**Agreements.** A-1 (ambas): declarar un consumidor esperado no prueba que exista y la utilidad no está demostrada (§10.5, §10.6); DEFENSE la usa como límite, PROSECUTION como bloqueo. A-2 (ambas): ningún checker exige esquema de secciones. A-3 (ambas): retirada reversible sin migración; legado tolerado (RFC-75 Mecanismo 15). A-4 (ambas): la auditoría Working es diagnóstica y no autoriza. A-5 (ambas): riesgo de declaración ritual o de falso positivo estructural (DEFENSE R-2/R-6; PROSECUTION O-1/O-5). A-6 (ambas): la práctica actual ya declara integración en prosa.

**Disagreements.** DG-1 auditabilidad vs detección en el criterio 1. DG-2 duplicación vs distinción semántica de campos 5 y 7. DG-3 «opcional» vs obligación social. DG-4 orden: F-02 primero o template ahora. DG-5 coste docs-only vs coste documental ampliado.

**Contradicciones (sin arbitraje).** K-1 ¿segunda fuente? DEFENSE D-5 + supuesto 4 (referencia, no copia) vs PROSECUTION O-3; evidencia común `_TEMPLATE.md:171`, `:176`, `:229`, `:137`. K-2 ¿campo 5 verificable? DEFENSE D-4 (`check_plan_citations.py` resuelve el anclaje) vs PROSECUTION §4 (resolver citas no prueba consumidores). K-3 ¿coste docs-only? DEFENSE D-3 vs PROSECUTION O-6 (`change-lifecycle.md:9`, README). K-4 ¿ausencia interpretable? DEFENSE supuesto 1 (`OPCIONAL` como otras secciones) vs PROSECUTION O-4 (sin disparador no significa nada).

## 4. MATERIAL FINDINGS

1. **MF-1 [DEFENSE]** Gap documentado (auditoría §8.1, §9 F-01, §13). *Por qué:* sin gap, C-1 es ceremonia.
2. **MF-2 [PROSECUTION, BLOCKING]** Declarar no prueba que el consumidor exista; la ausencia no causó las parciales; utilidad «sin experimento» (§10.5, §10.6, §1, §15). *Por qué:* define el criterio 1.
3. **MF-3 [PROSECUTION]** Alternativa superior ya identificada: convención F-02 con tabla y evidencia por fila (§10.5, §9 F-02; plan 178 §12). *Por qué:* más barata y produce la evidencia faltante.
4. **MF-4 [PROSECUTION]** Duplicación: campos 5 y 7 con `Verificación`/`Validation anchor` y `Findings`/`Riesgos`; 1-3 con `Depende de`/`RFC`/`Lifecycle`; 6 con fronteras vivas que quedan históricas (O-3; template `:171`, `:176`, `:229`, `:269`, `:137`; TE policy §13/§15; placement `:22`/`:24`). *Por qué:* reproduce el fallo que el criterio 4 pide descartar.
5. **MF-5 [PROSECUTION]** Disparador indeterminable; sin entrada en glosario; la ausencia no distingue `NO_APLICA` de olvido (O-4; template `:14`-`:26`; checks de `check_plan_structure.py`; `CONVENTIONS` vía Nota). *Por qué:* corpus futuro no comparable.
6. **MF-6 [PROSECUTION]** Autoridad/atestación: «previstos» sin cláusula que separe previsión de autorización; «evidencia» sin clase (O-5; template `:137`, `:104`; `README:Key concepts`; auditoría §10.2). *Por qué:* falso positivo o autoridad no otorgada.
7. **MF-7 [PROSECUTION]** Dependencia omitida: `README.md` declara «not a mechanism yet»; `change-lifecycle.md:9.2.a` exige README e impacto documental (O-6). *Por qué:* amplía coste o contradice el cierre.
8. **MF-8 [PROSECUTION, analogía]** Placement: enforcement diferido, biblioteca sin consumidor, `DEFERRED CONSUMER` (O-7; placement `:22`/`:24`; auditoría §7). *Por qué:* declaración sin mecanismo no se auto-corrige; analogía, no prueba causal.
9. **MF-9 [DEFENSE]** Contenido ya producido en prosa: plan 175 §15, propuesta TE «I»/«N», plan 176 (D-2). *Por qué:* se reubica, no se crea.
10. **MF-10 [DEFENSE]** Template vigente y probado: ≥11 commits, RFC-75 cita secciones del template, `CONVENTIONS` admite omitir opcionales (D-3). *Por qué:* extensión docs-only.
11. **MF-11 [DEFENSE]** Campos calibrados a la taxonomía (§3, §6.1, §6.2, §7) y precedente `Efectos declarados` nacido opcional y hoy fijado por test dogfood/ADR-19 (D-6, D-7). *Por qué:* plantilla específica; responde a «¿por qué no esperar un mecanismo?».
12. **MF-12 [DEFENSE]** Reversibilidad y coste de inacción: Mecanismo 15; plan 178 `Validation anchor` mide reconstrucción manual (L2, 12 suites) (D-8). *Por qué:* comparación contra coste ya incurrido.
13. **MF-13 [DEFENSE]** Límite auto-declarado: causalidad y utilidad no evidenciadas; template de 280 líneas; inserción fuera del tramo de prueba anclada (§4, §7; §10.5, §10.6). *Por qué:* acota el beneficio a auditabilidad.

**Duplicados entre pasadas:** MF-13 comparte evidencia con MF-2 (§10.5/§10.6), función contraria; MF-1/MF-2 comparten auditoría (diagnóstico vs causalidad); MF-9/MF-3 comparten plan 175/TE/178; MF-10/MF-11 y MF-4/MF-5 comparten template y checkers. Ningún par redundante en función.

**REQUIRES_NEW_EVALUATION (excluidos del veredicto y del conteo):** RNE-1: el efecto de `docs/VERSIONING.md` §4.1/§7/§10 (FRAME #7) sobre una sección declarativa no fue evaluado por ninguna pasada; podría afectar criterios 2 y 5. RNE-2: la clasificación de autorización del Change al template (RFC-56, release) sólo figura como supuesto de DEFENSE (D-3, supuesto 6), sin evaluación independiente.

## 5. SYNTHESIS

- **Convergencias.** Ambas aceptan el gap documentado, la ausencia de enforcement y de deuda estructural, que la declaración no prueba por sí sola la conexión y el riesgo de declaración ritual o falso positivo. Ninguna afirma que exista experimento repo-anclado que demuestre el beneficio. La diferencia central no es de hechos sino de peso: §10.5 se lee como límite admitido o como refutación.
- **Contradicciones.** K-1 a K-4 no son resolubles con la evidencia admitida: no hay medición de solapamiento, ni prueba de que citas ancladas identifiquen consumidores, ni estimación del coste documental, ni regla de aplicabilidad.
- **Material vs débil.** Materiales MF-1 a MF-13, todos anclados. Débiles o condicionados: O-8 (el propio PROSECUTION lo marca MINOR); D-4 sobre el campo 5 «cubierto» (cierto en resolución, no en prueba); «coste rutinario» de D-3 (no responde a O-6); analogías D-7 y O-7, declaradas como tales.
- **Evidencia compartida.** Auditoría §10.5/§10.6 y §1/§15; secciones del template; ambos checkers; `CONVENTIONS:Plantillas`; planes 175 y 178; `README.md`. Alta coincidencia de fuentes, divergencia interpretativa.
- **Evidencia faltante (GAP).** (i) Experimento repo-anclado de detección; (ii) artefacto versionado con criterio de éxito —PROSECUTION señala que la formulación vive en insumo no versionado; (iii) medición del coste de mantenimiento por Plan; (iv) evidencia de cumplimiento de «esperada»; (v) materia de RNE-1/RNE-2.
- **Dependencias.** Aceptar que auditabilidad satisface el criterio 1; rediseñar campos 5 y 7; definir disparador y semántica de ausencia; reconciliar README y glosario; vía de autorización del Change (RNE-2, excluida).
- **Condiciones.** DEFENSE: opcional no invalidante; sin checker/gate/schema/estado/registry/columna; evidencia anclable; sin duplicar `Scope`/`Efectos declarados`/`Verificación`; Plan DEV sin reescribir historia; retirada si resulta vacía. PROSECUTION: requisito versionado; experimento acotado; disparador, semántica de ausencia, clase de evidencia y cláusula «predice, no autoriza ni verifica»; aislamiento con fuente viva; reconciliación documental; F-02 primero. Compatibles en el «qué», discrepan en el «cuándo».
- **Desacuerdos.** DG-1 a DG-5 abiertos; no se resuelven por número ni severidad.
- **Consecuencias.** Adoptar tal cual asume O-3 a O-6. No adoptar mantiene el coste ya medido por plan 178 y deja F-01 sin respuesta. Ambos caminos son reversibles y de coste acotado, luego el coste de equivocarse es bajo en cualquiera de las direcciones.

## 6. VERDICT

**UNDETERMINED**

**BASIS.** Establecen: (a) el gap está documentado (F-01), aunque ninguna pasada demuestra que la ausencia del campo lo causara; (b) ninguna evidencia repo-anclada demuestra que una sección declarativa detecte discontinuidades (ambas citan §10.5, §10.6); (c) no habría enforcement mecánico y es reversible sin deuda; (d) hay objeciones materiales ancladas y no refutadas: duplicación (campos 5 y 7), disparador indeterminable, deriva de autoridad y coste documental omitido; (e) DEFENSE acota el beneficio a auditabilidad y declara GAP la efectividad. No establecen: beneficio neto; si la duplicación es fatal o aceptable; si F-02 es superior (afirmado desde la misma auditoría, sin prueba comparativa); si «esperada» obliga de facto; ni si README cambia materialmente el coste (evidencia unilateral). No hay base para VIABLE (criterio 1 no cumplido y objeciones ancladas) ni para NOT_VIABLE (el bloqueo ataca una tesis que DEFENSE no sostiene; el caso estructural está en gran medida incontestado y el coste es bajo y reversible).

**DISAGREEMENTS (no resueltos).** DG-1 auditabilidad vs detección; DG-2 duplicación vs distinción semántica; DG-3 «opcional» vs obligación social; DG-4 orden F-02 → template vs template ahora; DG-5 coste docs-only vs coste documental ampliado. La atribución se preserva por documento y cada lado conserva su evidencia; no se dirime por votos.

## 7. RECOMMENDATION (advisory, no autoritativa)

**GATHER_EVIDENCE.** Ambas coinciden en que la evidencia decisiva falta y en que coste y reversibilidad son bajos; el paso más discriminante es el experimento acotado que PROSECUTION propone (1-2 planes candidatos, con criterio de éxito versionado) y/o la convención F-02 primero, que produce vocabulario y evidencia. Luego re-evaluar C-1. No adoptar tal como está (O-3 a O-6 sin respuesta) ni rechazar el concepto. Opinión fundada, no autoridad.

## 8. Coste de esta síntesis

- **Duración:** ~3 min 40 s (04:41:46 → `2026-10-25T04:45:25.0014524-03:00`).
- **Llamadas a herramientas:** ~17 (tarea, timestamps, hashes, lecturas, Git de sólo lectura, escritura, hash, cierre).
- **Palabras:** ~1.789.


### Apéndice F — EVALUATION (evaluación experimental independiente)

# EVALUACIÓN EXPERIMENTAL — Case-01 / Trial #1 (`Adversarial Deliberation`)

## 0. Metadata

- **Inicio:** `2026-10-25T04:46:21-03:00`; **Finished:** `2026-10-25T04:52:33.3046049-03:00` (America/Buenos_Aires).
- **Repositorio:** `dev`, HEAD `b6843bc9f13f61d94e89ad9e8bfb38b06d011095` (verificado). Sin cambios trackeados; dos untracked preexistentes (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), **no** leídos como evidencia.
- **Entradas:** `FRAME.md`, `ANALYSIS.md`, `DEFENSE.md`, `PROSECUTION.md`, `SYNTHESIS.md`. Verificación de anclajes en el repositorio en sólo lectura. Sin web, sin modelos externos, sin memoria previa. **Escritura:** sólo este archivo; 0 comandos Git de escritura.
- **Independencia:** no produje A ni B; esta medición es **post hoc** (vi A antes de medir). Independencia de rol, no epistémica (§7). **No autoridad.**
- **GAP-0:** el modelo de cada pasada no está registrado en los artefactos.

## 1. Clasificación finding por finding

Definiciones literales: `DUPLICATE` = mismo hallazgo factual (o su consecuencia material) ya en `ANALYSIS.md`; `MATERIAL` = nuevo **y**, si verdadero, cambia decisión, plan, condición de aceptación o veredicto, con cambio concreto; `NON_MATERIAL` = nuevo y verdadero sin ese efecto; `SPURIOUS` = sin soporte o confusión semántica. Verificado al HEAD: `docs/plans/_TEMPLATE.md` tiene **222 líneas** (no 280) y 15 secciones `##`.

| ID | Clase | Justificación y ancla |
|---|---|---|
| **D-1** | `DUPLICATE` | F-01, el gap y las 2 integraciones parciales ya en `ANALYSIS.md:3` y §5 (auditoría `:8.1`, `:10.3`); misma consecuencia. |
| **D-2** | `DUPLICATE` | Declaraciones ad hoc ya en `ANALYSIS.md:3` («Varios planes ya la escriben ad hoc… Plan 175 `15. Integration`») y §5; 176/TE añaden fuentes, no el hallazgo. |
| **D-3** | `NON_MATERIAL` | Refuerzo nuevo: 12 commits de template, RFC-75 `:Criterios de aceptación` cita secciones del template, `CONVENTIONS` admite omitir opcionales; A ya asumió el plan docs-only (`:4.5`, `:9`). Sin cambio. |
| **D-4** | `DUPLICATE` | Sin schema de secciones y valor del checker de citas ya en `ANALYSIS.md:3`, §5 y supuesto 4. «Su evidencia queda cubierta» es **overclaim** (resolver citas ≠ verificar integración). |
| **D-5** | `DUPLICATE` | Un dueño, sin registry ni segunda fuente ya en `ANALYSIS.md:3`, supuesto 1 y §5 (INDEX sin columna). |
| **D-6** | `NON_MATERIAL` | Mapeo campos↔taxonomía (auditoría `:3`, `:6.1`, `:6.2`, `:7`): detalle de diseño; A ya atribuye la ganancia a campos 4–5 y conserva seis campos (`:9`). |
| **D-7** | `DUPLICATE` | Precedente `## Efectos declarados` (runtime, `test_autonomy_effects_dogfood.py`, ADR-19 `AE-4`): misma evidencia que A `:3` usa como advertencia; mismo hecho, uso inverso. |
| **D-8** | `DUPLICATE` | Reversibilidad sin deuda ya en `ANALYSIS.md:3`; plan 178 L2/12 suites añade cuantía al mismo argumento que A ya citaba (§5). |
| **O-1** | `DUPLICATE` | Núcleo textual idéntico: «declarar un consumer esperado no prueba que exista» (`:10.5`) y «la ausencia no causó las dos parciales» están en `ANALYSIS.md:3` y `GAP-1`. Misma evidencia, distinto peso. |
| **O-2** | `DUPLICATE` | Convención F-02 (`:10.5`) es la alternativa **C** de `ANALYSIS.md:7`; «F-02 primero»/«preempta la taxonomía» es reponderación, no hecho nuevo. |
| **O-3** | `MATERIAL` (marginal) | Mayormente duplicado: campos 5, 7 y 1–3 ya en `ANALYSIS.md:3`. **Campo 6 sí es nuevo**: los aislamientos viven en fuentes vivas (`.agents/policies/theoretical-execution.md:13. Boundaries`; placement `:22/24`, `PC-72`/`PC-72.1`/`PC-75`) y el Plan pasa a traza histórica al `Executed` (`docs/AGENTS.md:Folder → class map`); reenunciar la frontera la duplica y congela. Cambio concreto: referencia a la fuente viva (PROSECUTION §6.iv). *Caveat:* «campo 3 se confunde con `**Lifecycle:**`» es débil (ese campo es lifecycle del artefacto, `_TEMPLATE.md:12`). |
| **O-4** | `DUPLICATE` | «Esperada» sin criterio observable ya en `ANALYSIS.md:3`/riesgo 3, resuelto en plan (iii). Glosario sin entrada es cierto (`docs/glossary/terms.md`) pero no hay regla que obligue (`CONVENTIONS` D1–D5: descriptivo): sub-punto no material. |
| **O-5** | `DUPLICATE` | Riesgo de lectura como aprobación/prueba ya en `ANALYSIS.md:3` («…no es hipotético») y plan (iv); «previstos ≠ autorizados» queda cubierto por esa cláusula. |
| **O-6** | `DUPLICATE` | Reconciliación del README ya en `ANALYSIS.md:3` y paso 3 del plan, con la misma cita (`README.md:132`, `:237`); `change-lifecycle.md:9.2.a` respalda el mismo coste. |
| **O-7** | `DUPLICATE` | Precedente placement (biblioteca sin consumidor, enforcement diferido) ya en la tabla §5 de A («precedente de declarar dirección sin mecanismo»). Misma analogía. |
| **O-8** | `NON_MATERIAL` | «Corpus mixto» ya en la reversibilidad de A. Idioma débil: `docs/AGENTS.md:Idiomas y citas` pide español en `docs/plans/`, pero el template ya usa encabezados técnicos en inglés (`:176 Validation anchor`, `:229 Findings…`) y el nombre lo fija el FRAME. Contestable, sin cambio concreto. |

**Conteo:** 1 `MATERIAL`, 3 `NON_MATERIAL`, 12 `DUPLICATE`, 0 `SPURIOUS`. Sin objeciones espurias estrictas; sí 1 weak/contestable (O-8), 1 overclaim (D-4) y 1 error de magnitud en DEFENSE §4 («280 líneas y diez secciones»), sin efecto en su conclusión.

## 2. Material findings missed by baseline

**MF-E1 (único).** El campo 6 duplica aislamientos ya declarados en fuentes normativas vivas (TE `:13. Boundaries`; placement `:22/24`) y, al quedar el Plan como traza histórica al `Executed`, no se mantiene actualizado: debe ser **referencia a la fuente viva**, no reenunciado. Evidencia: PROSECUTION `O-3(b)` (template `:137`, `:229`, `:269`; TE policy `:13`/`:15`; placement `PC-72`/`PC-72.1`/`PC-75`), verificada. Ausencia en baseline: `ANALYSIS.md:3` sólo nombra solapamientos de campos 5, 7 y 1–3; su plan (`:9`) conserva el campo 6 como «Aislamiento deliberado (frontera declarada)» sin regla de referencia; su riesgo 4 cubre drift de rutas, no de fronteras. **`MATERIAL` marginal**: cambia una fila del plan, no la decisión. Todo el resto con severidad alta en B (O-1 «BLOCKING») es duplicado.

## 3. RESULT A vs RESULT B

| Dimensión | Result A (baseline) | Result B (tratamiento) | ¿Información nueva o reponderación? |
|---|---|---|---|
| Nuevos hallazgos | F-01 + 4 defectos de forma + GAP-1…5 | 16 argumentos: 12 duplicados, 3 no materiales, 1 material (MF-E1) | Sólo MF-E1 es nuevo y material. |
| Supuestos invalidados | — | Ninguno de A invalidado | Ninguno. |
| Riesgos descubiertos | 6 (decorativo, segunda fuente, aplicación, drift, test anclado, README) | Los mismos + obsolescencia del campo 6 + idioma/glosario débiles | Sólo MF-E1. |
| Evidencia adicional | Plan 175 `P-3` untracked, H-11, TE-extensión, `## Scope` ad hoc | 12 commits template, RFC-75, ADR-19, ataques plan 176, TE `:13/:15`, PCs placement, glosario | De apoyo; sólo TE/placement habilita MF-E1. |
| Cambios de plan | Plan concreto: template + INDEX + README + CHANGELOG + plan 179, 6 campos, verificación y rollout 3–5 planes | Sin plan: veredicto + condiciones (i)–(vi) y `GATHER_EVIDENCE` | B aporta 1 cambio (MF-E1); (i) criterio versionado, (ii) experimento, (vi) F-02 primero no nacen de hallazgos nuevos. |
| Cambio de veredicto | `REVISE` | `UNDETERMINED` | **Reponderación**: ambos citan `:10.5`; A lee «auditabilidad sí, detección no» y revisa; B exige detección para el criterio 1 y se abstiene. |
| Cambio de recomendación | Revisar y evaluar tras 3–5 planes (alternativa G descartada) | `GATHER_EVIDENCE`: experimento 1–2 planes y/o F-02 primero | **Reponderación**, redundante en gran parte con la evaluación post-rollout que A ya incluía. |
| Desacuerdos | Decide por juicio (D: REVISE) | Preserva DG-1…DG-5 sin dirimir | DG-1/3/5 son de umbral/alcance; DG-2/4, relecturas de la misma evidencia. |

**Lectura.** B no descubre información que cambie el veredicto de A: 12/16 argumentos reproducen hallazgos de A y su evidencia adicional es de refuerzo salvo TE/placement, que habilita un refinamiento del campo 6. El cambio REVISE→UNDETERMINED/GATHER_EVIDENCE se explica por **reponderación** del criterio 1 —peso de auditoría frente a detección— sobre la **misma** evidencia, no por información nueva. B es más conservador y preserva desacuerdos; A es más ejecutable. Convergen en lo sustantivo: no adoptar tal cual, coste bajo, reversibilidad alta, falta evidencia decisiva.

## 4. Métricas

**Beneficio.** 16 argumentos: `MATERIAL` 1 (plan-level), `NON_MATERIAL` 3, `DUPLICATE` 12, `SPURIOUS` 0. Hallazgos materiales nuevos que cambian decisión/veredicto/recomendación: **0**. Que cambian el plan: **1** (MF-E1). Supuestos de A invalidados: 0. Evidencia adicional: ~8 ítems, ninguno decisivo. Desacuerdos preservados: 5.

**Coste.** (Duración por metadata; palabras por `Measure-Object -Word`; llamadas autodeclaradas, GAP.)

| Pasada | Duración | Palabras | Llamadas |
|---|---|---|---|
| A | 5 min 48 s (348,1 s) | 2.385 | ~40 |
| D | 5 min 21 s (320,8 s) | 2.170 | ~45 |
| P | 4 min 56 s (295,5 s) | 2.001 | ~15 |
| S | 3 min 38 s (218,1 s) | 1.791 | ~17 |
| **B total** | **13 min 54 s agente (834,4 s)**; **9 min 35 s reloj** (D y P concurrentes) | **5.962** (2,50× A) | **~77** (1,93× A) |

Evaluaciones adicionales: **3** (2 posiciones + 1 síntesis). Esfuerzo de síntesis: 3 min 38 s, ~17 llamadas, 1.791 palabras. **Ruido:** duplicados 75 %; espurias 0; sub-claims débiles/overclaim 2 (O-8, D-4); error de magnitud 1 (DEFENSE §4); **contradicciones falsas 2 de 4** (K-2: ambos hechos son compatibles; K-3: diferencia de alcance, no conflicto); cambio de decisión sin hallazgo material que lo respalde: 1; cambios de plan innecesarios: 0 concretos.

**Ratio de titular.** Unidad = **una pasada de evaluación adicional**. **1 hallazgo material (plan-level, marginal) por 3 pasadas adicionales ≈ 0,33/pasada; 0 hallazgos materiales que cambien la decisión/veredicto por 3 pasadas.** Coste: 2,40× segundos-agente (1,65× reloj); ≈1 hallazgo material por 834 s-agente adicionales.

## 5. Dirección inversa (A encontró y B no)

| ID | Hallazgo de A | Clase (miss del tratamiento) |
|---|---|---|
| R-1 | El template no tiene `## Scope` aunque 33 planes lo usan ad hoc: no es exhaustivo (`ANALYSIS.md:3`, §5, GAP-4; verificado: 33 archivos) | `NON_MATERIAL`; relevante al criterio 4 (un campo nuevo puede ser sorteado como `## Scope`) |
| R-2 | Plan 175 `P-3` incluye `PRIORITY.md` untracked en el contexto (`ANALYSIS.md:3`; verificado `175:26`) | `NON_MATERIAL` (drift documental) |
| R-3 | H-11: espejo de INDEX desactualizado del cierre de TE (`ANALYSIS.md:3`, §5) | `NON_MATERIAL` (drift) |
| R-4 | Alternativa E (extender TE para verificar consumidores), rechazada con auditoría `:10.5`/`:14` (`ANALYSIS.md:7`) | `NON_MATERIAL` (cobertura de alternativas) |
| R-5 | Enrutar integraciones desconocidas a PC-1 (`ANALYSIS.md:9.ii`) | `NON_MATERIAL` (diseño; B sólo señala duplicación) |

Ningún miss del tratamiento es material. **GAP de medición:** el conteo «16» de `ANALYSIS.md:5` no se reprodujo con mi patrón de sólo lectura (8 encabezados no-INDEX con `^#{2,4} .*[Ii]ntegra`); no se usa en conclusiones.

## 6. Resultado y camino siguiente

**Clasificación: éxito fuerte (marginal), por la letra del protocolo.** Se cumple: ≥1 hallazgo material no hallado por el baseline (MF-E1), con evidencia suficiente (TE `:13. Boundaries`, placement `PC-72.1`/`PC-75`, template y `docs/AGENTS.md` verificados), que **debe cambiar el plan** (regla de referencia del campo 6) y no es espurio. No lo es en magnitud: 1/16; 12/16 duplicados; 0 hallazgos materiales que cambien la decisión/veredicto; el veredicto distinto de B es reponderación; coste 2,40×.

**Camino siguiente: iterar / segundo trial, con hipótesis refinada.** El trial no es negativo ni estéril, pero el beneficio es demasiado estrecho para adoptar sin más o abandonar. El segundo trial debe (a) reformular la hipótesis: la deliberación adversarial aporta **detección de duplicación/obsolescencia de declaraciones y afilado de condiciones**, no detección de integraciones faltantes; (b) corregir la desviación del FRAME; (c) pre-registrar clases y umbral del criterio 1; (d) usar contextos más independientes e instrumentar llamadas/tiempos; (e) elegir una decisión donde el baseline tenga probabilidad real de errar (ésta era docs-only, barata y reversible, favorable a la convergencia).

## 7. Limitaciones y sesgos

1. **n=1**, sin réplica; no generalizable.
2. **Mismo modelo en todas las pasadas** (por diseño; identidad no registrada): errores correlacionados; la deliberación no añade diversidad epistémica.
3. **Independencia procesal, no epistémica:** commit-before-reveal evita contaminación cruzada, pero comparten frame, repositorio y modelo.
4. **Sin attestación temporal externa:** `.project/` gitignored (`.gitignore:13`); los SHA-256 se reproducen (verifiqué DEFENSE/PROSECUTION) pero no prueban orden ni autoría; timestamps autodeclarados.
5. **Desviación de protocolo (FRAME):** el criterio 4 cita `## Scope` como sección existente del template («p. ej. `## Scope`, `## Efectos declarados`, `## Verificación`»), pero el template **no tiene** `## Scope` (verificado) y 33 planes lo usan ad hoc. Error del frame que pudo orientar a las pasadas (A lo detectó; B no).
6. **Datos autodeclarados:** duraciones y llamadas provienen de metadata interna; conteo aproximado (GAP).
7. **Post hoc y no ciego:** orden de lectura (A antes que B) puede sesgar la búsqueda de duplicados; sin replicación externa.
8. **Vocabularios distintos:** A emite «decisión» y B «veredicto + recomendación»; comparación interpretativa.
9. **Caso favorable a la convergencia:** decisión docs-only, reversible y barata, con auditoría previa; techo bajo de descubrimiento material.

## 8. Coste de esta evaluación

- **Duración:** 04:46:21 → 04:52:33 (America/Buenos_Aires) ≈ **6 min 12 s** de reloj, incluyendo lectura de las 5 piezas del caso y ~12 inspecciones de verificación.
- **Llamadas a herramientas:** ~26; **escrituras:** 1; **archivos versionados modificados:** 0; **comandos Git de escritura:** 0.
- **Lecturas directas:** 8 (5 del caso + `docs/AGENTS.md`, `docs/CONVENTIONS.md`, `.agents/workflows/change-lifecycle.md`); el resto por comandos de sólo lectura.


