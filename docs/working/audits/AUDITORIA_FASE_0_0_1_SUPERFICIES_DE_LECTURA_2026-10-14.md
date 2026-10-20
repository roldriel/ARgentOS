# Auditoría Fase 0 — `PRIORITY.md:0.1` — Superficies de lectura y veredicto

> **Pregunta rectora.** ¿Cuál es la **intervención mínima** que hace que un tercero pueda confiar en que las afirmaciones relevantes de ARgentOS no exceden la evidencia disponible?

**Naturaleza documental:** Working / audit — **no normativo**; puede ser provenance, nunca autoridad.
**Fecha:** 2026-10-14
**Autoriza:** acto del mantenedor (2026-10-14) — Fase 0 de `PRIORITY.md:0.1`, según `docs/working/proposals/REVISION_ADVERSARIAL_ESPECIFICACION_0_1_2026-10-14.md` §3.
**Estado:** `EJECUTADA` — la auditoría se ejecutó; **0 modificaciones** a las superficies auditadas; el veredicto no autoriza trabajo alguno por sí mismo.
**Autoridad:** ninguna. Este documento no decide, no autoriza, no crea trabajo y no corrige nada.
**Método:** procedimiento de §3.2 de la revisión, aplicado literalmente; corrección §3.3 (especificación ≠ afirmación de hecho); casos límite de §3.4; regla de decisión de §3.6 **sin renegociar**.

**Restricciones respetadas:** no se modificó `PRIORITY.md`, `docs/CONVENTIONS.md`, el glosario, el payload, `protocol/.agents/`, ningún claims registry ni ningún checker; no se corrigió nada durante la recolección; no se amplió el alcance de la auditoría; no se introdujo vocabulario ni se justificó E-1.

---

## 0. Veredicto

# `MINIMAL_RULE`

**Con dos salvedades declaradas, que el mantenedor debe resolver antes de diseñar nada:**

1. **La causa común demostrada ya está cubierta por reglas existentes no aplicadas** (§4.4). "La regla que la causa exige" puede ser **ninguna regla nueva**. La aplicación literal de §3.6 da `MINIMAL_RULE`; su propio texto condiciona la regla a lo que la causa exija, y eso es una pregunta abierta, no una conclusión.
2. **Sensibilidad declarada** (§4.2): si se rechaza **D-1**, y además el cluster de S4 se cuenta como una sola unidad de corrección, el conteo baja a 2 → `CORRECT_EXISTING_CLAIMS`.

**Lo que la auditoría NO encontró, y es su resultado sustantivo más importante:** **cero instancias abiertas** de la clase de fallo que `PRIORITY.md:0.1` describe — presentar como hecho una aspiración, una especificación o una capacidad no demostrada. De 8 defectos materiales en 3 superficies, **ninguno es de esa clase**. Los 8 son de **otra** clase: *restatement sin re-derivación* — afirmaciones que eran correctas o propias cuando se escribieron y dejaron de serlo porque la fuente que copiaban cambió, sin que nadie re-derivara la copia.

---

## 1. Preflight de redundancia (F-1, F-2, F-4a–d)

Ejecutado **antes** de la auditoría, según §4 de la revisión.

| # | Verificación | Resultado | Consecuencia |
|---|---|---|---|
| **F-1** | ¿Existe un artefacto que enumere las afirmaciones de ARgentOS con su evidencia? | **NO VERIFICADA** | No cae la propuesta por duplicación. El más cercano es la matriz de Etapa A (28 capacidades, Working, congelada) — no cubre definiciones, especificaciones, hipótesis ni aspiraciones |
| **F-2** | ¿El vocabulario de §0.1 (aspiración / hipótesis) ya está definido en el payload? | **NO VERIFICADA** | Cero ocurrencias de `aspiration`/`hypothes`/`aspiraci`/`hipótesis` en todo `protocol/.agents/**`. El vocabulario no existe en el payload; el `GAP` de H-6 queda confirmado |
| **F-4a** | ¿La *claims rule* / `claim_class` del payload es invocada como norma por artefactos DEV? | **VERIFICADA** | `docs/adr/01-guarantee-model.md:44,56,77`; `docs/rfc/62-…md:59,71,217`; `docs/rfc/80-…md:35`; `docs/plans/76,77,78,79,80,81,150`; `docs/MIGRATION.md:156,224`; `docs/working/audits/architecture-capability-review.md:1885` |
| **F-4b** | ¿`NO_ASSUMPTIONS.md` ya prohíbe tratar lo no confirmado como hecho? | **VERIFICADA** | `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:17` — el agente MUST NOT asumir «Facts, context, or decisions invented to avoid clarification **or to keep the task "simple"**»; `:31` — «MUST NOT reduce rigor, omit required investigation, or invent details to make the task appear simpler than it is» |
| **F-4c** | ¿`CONFIDENCE.md` ya tiene regla anti-inflación? | **VERIFICADA** | `protocol/.agents/standards/quality/CONFIDENCE.md:5` — «a conclusion never claims more certainty than its evidence supports»; `:15–19` — «**The anti-inflation rule**»: declarar un nivel superior al que la evidencia sostiene «is a conduct violation: it MUST be recorded as a deviation» |
| **F-4d** | ¿`behavior-patterns.md` ya establece la asimetría de la evidencia? | **VERIFICADA** | `docs/behavior-patterns.md:507` — «**La ausencia de evidencia nunca se convierte en evidencia positiva.** Sólo `VALID` es evidencia positiva» |

**Lectura del preflight, declarada antes de auditar:** las cuatro verificaciones F-4 se confirman. **Cuatro mecanismos normativos vigentes ya prohíben presentar como hecho lo que la evidencia no sostiene**, uno de ellos con clase de violación de conducta (`CONFIDENCE.md:19`). La dimensión *claim vs evidencia* de E-1 es por tanto redundante. Lo que esos cuatro mecanismos **no** cubren es la deriva de una copia (§3.4).

---

## 2. Cobertura

| # | Superficie | Cobertura | Auditor |
|---|---|---|---|
| **S1** | `AGENTS.md` (raíz, 193 líneas) | **completa** | lead |
| **S2** | `.agents/AGENTS.md`, `.agents/policies/*` (5), `.agents/workflows/*` (1) — 1.813 líneas | `AGENTS.md` (104) + `lifecycle-checkers.md` (119) + `authority.md` (75) **completos**; los otros 4 archivos (1.515 líneas) por **barrido sistemático de enunciados** (verbos de logro, garantía y limitación), ~120 coincidencias revisadas | lead |
| **S3** | `README.md` (177) | **completa** | lead |
| **S4** | `ROADMAP.md` (115) | **completa**, con verificación de cada afirmación de estado contra git | lead |
| **S5** | `protocol/_AGENTS.md` (49) | **completa** | lead |
| **S6** | `protocol/.agents/INDEX.md` (51) | **completa** | lead |
| **S7** | `harness/INDEX.md` §Guarantee catalog + §Enforcement boundaries | **completa** | lead |
| **S8** | `docs/ADOPTION.md` (436) + `docs/MIGRATION.md` (613) | **completas** | delegado, revisado por el lead |
| **S9** | `docs/behavior-patterns.md` (699) | **completa** | delegado, revisado por el lead |
| **S10** | `protocol/.agents/standards/**` (**51** archivos `.md`; el brief declaraba 34) | **7 completos** (`INDEX.md` + `EVIDENCE`, `CONFIDENCE`, `NO_ASSUMPTIONS`, `PROTOCOL_HEALTH`, `PROTOCOL_METRICS`, `PROTOCOL_BOUNDARIES`); **44 muestreados**, ninguno sin examinar | delegado |
| **C1** | `docs/architecture/*` + `docs/working/**` (28 banners + 3 archivos en profundidad) | banners de los 28 + 3 completos + muestreo por secciones | delegado |
| **C2** | `CHANGELOG.md` (3.259 líneas) | cabeza (1–120), cola, 5 releases muestreadas, **barrido mecánico de los 257 bullets** de primer nivel | delegado |

**Límites declarados.** (a) S2 no se leyó íntegro: 3 de 7 archivos completos, el resto por barrido de patrones; un defecto que no use un verbo de logro/garantía podría no haberse detectado. (b) S10: 7 de 51 archivos completos y 44 muestreados; el riesgo residual principal es el cuerpo de datos de `PROTOCOL_TAXONOMY.md` (3.017 líneas), muestreado sólo en su bloque de reglas, y las colas de `MEMORY_SYSTEM.md`, `ARCHITECTURE_CONTRACT.md`, `ORCHESTRATION_GUIDE.md` §10 y los cinco archivos SOLID. C1: ~40 % de la matriz de Etapa A y ~25 % de `PROMPT_CACHE_PHASE_1_REPORT.md`, más muestreo por secciones. C2: cabeza, cola, 5 releases y barrido mecánico de los 257 bullets, no cada línea. (c) Ningún auditor ejecutó la batería ni las suites: las afirmaciones que descansan en que un test *pase* se verificaron sólo como test existente y localizable. (d) La verificación no fue mecánica: `tools/check_plan_citations.py:194–210` no recorre `docs/working/` ni `protocol/.agents/`. (e) Cero enunciados fueron corregidos durante la recolección, por regla. (f) El brief de S10 declaraba 34 archivos; el conteo real es **51**. La discrepancia se registra porque afecta la confianza en la cobertura: 44 archivos quedaron en muestreo, no en lectura completa.

---

## 3. Resultado

### 3.1 Tabla de defectos materiales

| # | Superficie | Enunciado (verbatim) | Cita | Clase | Consecuencia | Corrección propuesta |
|---|---|---|---|---|---|---|
| **D-1** | S1 | «They **never** depend on the `protocol/` payload and never include the harness tests; see `tests/AGENTS.md`» | `AGENTS.md:24–26` | `CLAIM-CONDITIONAL-UNMARKED` | Un agente que evalúe si un Change de payload puede romper `tests/` concluye que no y omite esa comprobación; los dogfoods de payload están diseñados para moverse con él | Calificar con la excepción declarada por la autoridad que ya cita (una cláusula) |
| **D-2** | S8 | «Solo cuatro scripts lo usan: `hook_gate.py` … `runner_state.py` … `health_check.py` … y `gate_validator.py`» | `docs/ADOPTION.md:156–160` | `CLAIM-UNSUPPORTED` | El adoptante dimensiona mal la superficie Python del árbol instalado (la mitad) e infiere que los scripts del lifecycle — §1.2 del mismo archivo — no cuentan | Declarar ocho módulos, o acotar a los cuatro de sesión y nombrar los cuatro que materializan el layout |
| **D-3a** | S4 | «**Payload publicado:** `origin/dist` @ `1181db6`» | `ROADMAP.md:29` | `CLAIM-UNSUPPORTED` | El lector apunta a un commit superado | Reconciliar con el estado liberado |
| **D-3b** | S4 | «**Todavía corresponde a `12.0.0`**» | `ROADMAP.md:30–32` | `CLAIM-UNSUPPORTED` | El lector cree que el payload disponible para adoptantes es `12.0.0` | Ídem |
| **D-3c** | S4 | «la publicación remota de `12.1.0` … es un acto **no autorizado**» | `ROADMAP.md:30–32` | `CLAIM-UNSUPPORTED` | El lector cree pendiente y no autorizada una publicación ya ocurrida | Ídem |
| **D-3d** | S4 | «**[PROTOCOL] HIGH — Promover `12.0.1`**» | `ROADMAP.md:55–57` | `CLAIM-UNSUPPORTED` | Directiva superada: `12.0.1` fue absorbido por `12.1.0` | Ídem |
| **D-3e** | S4 | Bloqueo «Autorización de la publicación remota de `12.1.0` \| cuándo llega a `dist`» | `ROADMAP.md:108` | `CLAIM-UNSUPPORTED` | Un bloqueo resuelto sigue figurando como vigente | Ídem |
| **D-3f** | S4 | «_Protocolo publicado: `12.0.0`_» | `ROADMAP.md:115` | `CLAIM-UNSUPPORTED` | Contradice la línea 28 del mismo documento («Protocolo publicado: `12.1.0`») y el hecho: el lector no puede saber cuál es la versión publicada | Ídem |

### 3.2 Evidencia de cada defecto

**D-1.** La autoridad que el propio enunciado cita declara la excepción y enumera los tests que la constituyen: `tests/AGENTS.md:9–14` («**The one deliberate exception** is the dogfood below, which reads the real payload on purpose»), `:62–69` («They read the live working tree **on purpose**»), `:80` (`test_prompt_cache_dogfood.py` = «the ten verifiable points of RFC-78 / plan 121 materialized **over the real `protocol/` payload**»), `:88–89` (dogfoods de discovery y EARS «against the **real** discovery contracts and the real payload»). Verificado además: 26 archivos de `tests/` referencian `protocol/`.

**D-2.** `protocol/.agents/harness/INDEX.md:16` — «**Eight** pure-stdlib Python modules ship: the four that enforce and validate during a session — `hook_gate.py`, `runner_state.py`, `health_check.py` and `gate_validator.py` — plus the four that make the layout materializable: `roots.py`, `lifecycle.py`, `lifecycle_contract.py` and `lifecycle_staging.py`». Y `CHANGELOG.md:1570–1574` documenta la corrección de `12.0.1` (RFC-82): los ocho módulos se enumeran «en lugar de declarar «exactly four»». **`docs/ADOPTION.md:156` conserva exactamente la formulación que esa corrección retiró.** Corroboración independiente (S10): `protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md:12` afirma «exactly eight modules» y el conteo real de `.py` bajo `.agents/harness/` es **8**. Es decir: **las dos superficies canónicas del payload dicen ocho; la superficie de adopción dice cuatro.**

**D-3.** Verificado contra Git:
- `git rev-parse --short origin/dist` → **`aebd0c4`** (2026-10-15, «dist: publish from master @ 45809c1»); `1181db6` (2026-10-11) es **ancestro** suyo, es decir superado.
- `git show origin/dist:.agents/VERSION` → **`12.1.0`**.
- Tag `12.1.0` (anotado) → `45809c1` = `master`. `protocol/.agents/VERSION` en `master` y en `dev` = `12.1.0`; `git diff dev master -- protocol/` **vacío**.
- `ROADMAP.md:115` declara «Última actualización: 2026-10-14»; el hecho que lo desmiente es de **2026-10-15**.
- `docs/plans/168-release-12-1-0.md:135` — «Empujar `master` y el tag a `origin` … queda **fuera** de este Plan»; `:142` — criterio de salida «`ROADMAP.md` declara la versión publicada» (**cumplido sólo en la línea 28**); `:193` — `Roadmap impact: REQUIRED` sobre la Posición actual, el bloqueo de autorización y `dev` sin cambios pendientes (**no cumplido** en 29–32, 55–57, 108, 115).

### 3.3 Conteo y distribución

| Métrica | Valor |
|---|---|
| Enunciados defectuosos | **8** |
| Superficies auditadas | **12** (S1–S10 + controles C1, C2) |
| Superficies con al menos un defecto | **3** (S1, S4, S8) |
| Unidades de corrección | **3** |
| Superficies sin ningún defecto | **9** (S2, S3, S5, S6, S7, S9, S10, C1, C2) |
| Concentración | **6 de 8 enunciados en una sola superficie** (S4, `ROADMAP.md`) |

**S10 devolvió cero defectos materiales** (veredicto propio: `NO_STRUCTURAL_CHANGE`), con verificación dirigida que resolvió cada garantía comprobable a un ancla existente o a un límite autodeclarado. **Corrobora D-2 de forma independiente:** `protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md:12` afirma «exactly eight modules» y el conteo real de `.py` bajo `.agents/harness/` es **8**.

### 3.4 Patrón

**No es un patrón de sobre-afirmación. Es un patrón de copia sin re-derivación.** Los 8 enunciados comparten **una causa común**:

> Una afirmación **restata** un hecho cuyo dueño es otra superficie, y **nada la re-deriva** cuando el dueño cambia.

| Defecto | Hecho copiado | Dueño real | Qué cambió sin que la copia se actualizara |
|---|---|---|---|
| D-1 | la regla de dependencia de `tests/` | `tests/AGENTS.md:9–14` | la excepción existe y la copia la omite |
| D-2 | el inventario de módulos Python del payload | `harness/INDEX.md:16`, `PYTHON_DEPENDENCIES.md` | la corrección de `12.0.1` (RFC-82) |
| D-3a–f | el estado de release | tags de Git + `protocol/.agents/VERSION` + `docs/VERSIONING.md` §9 | la regeneración de `origin/dist` (2026-10-15) |

**Ninguno de los 8 es una aspiración presentada como logro, ni una especificación presentada como capacidad demostrada.** La clase que `PRIORITY.md:0.1` nombra no tiene instancia abierta en las 12 superficies auditadas.

**Concentración diagnóstico-relevante.** S4 aporta 6 de los 8 enunciados, y su propio contrato le prohíbe alojar ese contenido: `docs/CONVENTIONS.md:781` (el ROADMAP «no es … un release history»; «no registra evidencia») y `:807` («**Regla de frescura.** El ROADMAP se actualiza cuando cambia la dirección, la secuencia o las prioridades, **no** cuando se cierra una tarea»). El defecto de S4 es el **síntoma ya predicho** de esa violación de contrato, no un problema de disciplina de afirmaciones.

### 3.5 Respuestas a las seis preguntas que la auditoría debía responder

| # | Pregunta (§2.4 de la revisión) | Respuesta |
|---|---|---|
| 1 | ¿Cuántas afirmaciones materialmente sobre-afirmadas existen hoy? | **8**, en 3 de 12 superficies |
| 2 | ¿Patrón o casos aislados? | **Un patrón único con una causa común** (restatement sin re-derivación), concentrado en S4 |
| 3 | ¿Las superficies de lectura son peores que las no normativas? | **No: lo contrario.** C1 (`docs/architecture/`, `docs/working/`) y C2 (`CHANGELOG.md`) resultaron **más** cuidadosos. Se refuta la hipótesis de "ausencia de disciplina" |
| 4 | ¿E-1 es redundante? | **Sí en su dimensión de claim vs evidencia** (F-4a–d verificadas, cuatro mecanismos vigentes). **No** respecto de la causa demostrada: la deriva de copias no está cubierta por ninguno de los cuatro |
| 5 | ¿Sobrevive H-1 (entry points sin marca)? | **No.** S5 y S6 produjeron **cero** defectos; sus enunciados se clasificaron `SPEC` por §3.3. Ningún defecto encontrado es una omisión de marca de clase |
| 6 | ¿Las condiciones de borde del payload son alcanzables desde el entry point? | **Sí, por enrutamiento**: `protocol/_AGENTS.md:20–33` («Where the rules live») enruta cada tema a su artefacto dueño, y S5/S6 no contienen afirmaciones de capacidad que las condiciones contradigan |

### 3.6 Observaciones **no** contabilizadas

Registradas por transparencia; ninguna cumple las tres condiciones de §1.4.

| # | Observación | Por qué no cuenta |
|---|---|---|
| O-1 | `tests/AGENTS.md:9–14` dice «**The one deliberate exception**» y a continuación enumera **17** tests anclados (`:73–91`), varios sobre el payload real | Superficie **fuera de §3.1**. Es la fuente de D-1, no un defecto contable |
| O-2 | `docs/ADOPTION.md:332–355` — el bloque de §7 está insertado dentro de §6.4 y parte una frase | Anomalía de **forma**: el mismo hecho está intacto en `:290–301`. No induce creencia falsa |
| O-3 | `AGENTS.md:19–20` «the checkers run by CI» — CI ejecuta 7 de los ~18 de `tools/`; `check_dist_sync.py` no corre en CI | La excepción está documentada **en la misma superficie** (`AGENTS.md:178–181`): hereda la salvedad |
| O-4 | `AGENTS.md:183–186` describe el ROADMAP como conteniendo «current position» | Descripción **verdadera del artefacto**; la violación de contrato es del artefacto, no de la afirmación |
| O-5 | `G-001…G-005` / `ENF-001…003` citados en archivos distribuidos, definidos sólo en `docs/rfc/62-…md:166–190` | La sustancia de cada invariante está **inline** en el archivo que lo cita |
| O-6 | `AGENTS.md:190` «the `dist` branch … contains only `.agents/` and `AGENTS.md` at its root» | **Verdadero**, verificado: `git ls-tree origin/dist` → `.agents`, `AGENTS.md`. La divergencia con el layout `.argentos/` es **estado de release**, seguido en `ROADMAP.md:55–57` |
| O-7 | `docs/ADOPTION.md:156` convive con una formulación intacta del mismo hecho en otras superficies | Refuerza que D-2 es una copia rezagada, no una comprensión errónea generalizada |

### 3.7 Hallazgo de gobernanza **fuera del alcance de esta auditoría** (señalado, no contabilizado)

La auditoría de S4 puso a la vista un hecho que **no pertenece a §0.1** y que no debe silenciarse:

- `docs/plans/168-release-12-1-0.md:135` declara que empujar `master` y el tag a `origin` «queda **fuera** de este Plan: es un acto de **publicación remota no autorizado aquí**».
- `origin/dist` fue regenerado el **2026-10-15** desde `45809c1` («dist: publish from master @ 45809c1»), es decir: **la publicación remota ocurrió**.
- Plan 169 (`Aprobado para ejecución`, no ejecutado) trata la regularización de `81bbde1` y declara `Roadmap impact: NOT_REQUIRED`; no menciona la publicación remota.

**Estado: `NO VERIFICADO`.** No encontré, en las superficies auditadas, un acto que autorice la publicación remota; tampoco busqué fuera de ellas, porque hacerlo excede el alcance de esta Fase 0. No afirmo que la publicación haya sido no autorizada: afirmo que **no está verificada** y que corresponde a `PRIORITY.md:10` (integridad de releases), no a §0.1.

---

## 4. Aplicación de la regla de decisión §3.6 (sin renegociar)

### 4.1 Aplicación literal

| Fila de §3.6 | Condición | ¿Se cumple? |
|---|---|---|
| `NO_STRUCTURAL_CHANGE` | 0 defectos | No — hay 8 |
| `CORRECT_EXISTING_CLAIMS` | 1–2 defectos sin causa común | No — los defectos **sí** comparten causa |
| **`MINIMAL_RULE`** | **≥3 defectos independientes con una causa común, o recurrencia tras corrección** | **Sí** — 8 enunciados en 3 superficies independientes, con una causa común demostrada (§3.4) |
| `MODEL_REQUIRED` | capacidad estructural ausente y la corrección por redacción no lo resuelve | No — las tres correcciones son redaccionales y ninguna requiere una capacidad ausente |

**Veredicto: `MINIMAL_RULE`.** Y §3.6 lo restringe: «una regla documental pequeña, **y sólo la que la causa común exija**». Si la causa exigiera más de una regla, el resultado correcto sería volver a `MODEL_REQUIRED` con la evidencia — no acumular reglas.

### 4.2 Sensibilidad declarada

| Escenario | Conteo | Veredicto |
|---|---|---|
| Como se reporta (8 enunciados / 3 unidades) | 8 / 3 | `MINIMAL_RULE` |
| Se rechaza **D-1** y se cuentan unidades de corrección | 2 | `CORRECT_EXISTING_CLAIMS` |
| Se rechaza **D-1** pero se cuentan enunciados | 7 | `MINIMAL_RULE` |
| S10 aporta un defecto estructural | — | **cerrado**: S10 devolvió `NONE` (§3.3). No habilita `MODEL_REQUIRED` |

**El único juicio que puede mover el veredicto hacia abajo es D-1**, y es el más débil de los tres: la salvedad está a un salto citado de distancia, y §3.4 admite que un enunciado que "hereda la salvedad" no es defecto. Lo cuento porque la frase afirma «**never**» y su propia cita lo contradice, y porque la consecuencia (omitir la comprobación de `tests/` ante un Change de payload) es concreta; pero **lo marco como `MEDIUM-LOW`** y queda a la vista para que se revise.

### 4.3 Qué exige la causa, en términos de la pregunta rectora

La causa es *restatement sin re-derivación*. La intervención mínima que la cierra tiene dos partes, y la primera **no es una regla**:

1. **Corregir los 8 enunciados** (§3.1). Están demostrados, son redaccionales, y ninguno requiere autorización de payload — salvo la parte de `ROADMAP.md`, que sí es un Change.
2. **Una sola regla**, si se decide que hace falta: que una afirmación que restata un hecho cuyo dueño es otra superficie **cite ese dueño y se re-derive de él**, y que cuando el dueño cambie la copia se corrija en el mismo Change.

### 4.4 Salvedad: la causa puede no exigir ninguna regla nueva

Dos reglas vigentes **ya cubren** parcialmente la causa, y los defectos las violan:

- `docs/AGENTS.md:Idiomas y citas` — «Las afirmaciones sobre el estado actual del repo se anclan con `ruta:sección`». D-2 y D-3 no anclan su hecho a ninguna fuente; D-1 ancla a una fuente que lo contradice.
- `docs/CONVENTIONS.md:807` — regla de frescura del ROADMAP; D-3 la viola.
- `.agents/AGENTS.md:74–76` — «**One source of truth per concept**»; principio vigente, aunque acotado a la capa `.agents/` (registries) y sin obligación de cita ni de corrección.

**Consecuencia honesta:** el `MINIMAL_RULE` de §3.6 podría resolverse como *aplicar reglas existentes* en lugar de escribir una nueva. Esa disyuntiva **no la resuelve esta auditoría** y es la primera pregunta del siguiente paso autorizable (§6). Registro además que la regla de decisión **no tenía una fila para este caso** — causa común ya cubierta por una regla no aplicada — como hallazgo de procedimiento (P-3).

---

## 5. Hallazgos sobre el propio procedimiento (§3.2/§3.6)

| # | Hallazgo | Efecto y manejo |
|---|---|---|
| **P-1** | §3.2 paso 3 clasifica como `SUPPORTED` un enunciado cuyo **soporte alcanzable lo contradice**. Es el caso de D-1 | Apliqué el test de verdad (paso 4) y lo registro en lugar de plegarme a la letra: tratar una cita auto-refutante como soporte habría producido un falso negativo. **La §3.2 necesita una rama "soporte alcanzable que contradice"** |
| **P-2** | §3.6 no tiene fila para "2 defectos con una causa común": caen en la fila de 1–2 "sin causa común" | Apliqué la letra y expuse la sensibilidad en §4.2 en lugar de renegociar el umbral |
| **P-3** | §3.6 no tiene fila para "causa común ya cubierta por una regla existente no aplicada" | Registrado en §4.4; determina la primera pregunta del siguiente paso |
| **P-4** | El procedimiento exige que la materialidad sea revisable por un tercero, y no lo es mecánicamente: ningún checker cubre `docs/working/` ni `protocol/.agents/` (`tools/check_plan_citations.py:194–210`) | Declarado como límite; cada enunciado cita su evidencia para permitir revisión manual |

---

## 6. Qué NO encontré, y por qué importa

1. **Cero instancias abiertas de la clase de §0.1.** Ninguna superficie auditada presenta una aspiración, una hipótesis o una especificación como capacidad demostrada. El único caso de esa clase es **histórico y ya corregido** (2026-08, «zero hallucinations» → `harness/INDEX.md:164`).
2. **Cero defectos en los entry points del payload** (S5, S6), donde la v1 ubicaba el problema principal (H-1). **H-1 no sobrevive** al test de §3.3.
3. **Cero defectos en el `README.md`** (S3), pese a ser la primera exposición humana: sus afirmaciones de capacidad más fuertes (códigos de salida del lifecycle `0/10/20/30`; ausencia de provider/modelo/red/credenciales; `--sae` opt-in) se verificaron **exactas** contra `lifecycle.py:55–61` y las policies.
4. **Cero defectos en `behavior-patterns.md`** (S9): cada afirmación factual verificada coincidió con código, contrato o policy citada.
5. **Las superficies declaradas no normativas son las más disciplinadas** (C1, C2). Esto **refuta** la hipótesis de que falte disciplina general y **confirma** que la disciplina existe; lo que falta es re-derivación de las copias.
6. **Cero defectos en los estándares del payload** (S10: **51** archivos `.md`, no los 34 del brief): cada garantía comprobable resolvió a un ancla existente o a un límite autodeclarado. Es la superficie normativa más extensa del producto y no aportó un solo enunciado sobre-afirmado.

**Lo que esto significa para `PRIORITY.md:0.1`:** el riesgo que §0.1 describe sigue siendo legítimo como **riesgo futuro** (R-1 de la revisión: ya ocurrió una vez), pero **no tiene daño presente medido en las 12 superficies auditadas**. Los 8 defectos encontrados son de otra clase, y su causa — copias que no se re-derivan — es la misma que el informe de planificación ya había diagnosticado como R-1/R-5 (estado duplicado sin dueño verificable).

---

## 7. Recomendación

1. **Aceptar el veredicto `MINIMAL_RULE`** tal como lo da §3.6, con las dos salvedades de §0.
2. **Autorizar como siguiente paso, y nada más, la respuesta a una pregunta:** ¿la causa demostrada exige **una regla nueva**, o basta **aplicar** `docs/AGENTS.md:Idiomas y citas` + `docs/CONVENTIONS.md:807` + `.agents/AGENTS.md:74–76`? Si exige regla, debe ser **una sola**, derivada de la causa, y **no** una reutilización de E-1.
3. **Las 3 correcciones de §3.1 quedan demostradas** por esta auditoría y no dependen de la decisión anterior. La de `ROADMAP.md` es la de mayor efecto y la de mayor valor: elimina 6 de los 8 enunciados y, además, retira del ROADMAP el estado que su contrato le prohíbe alojar.
4. **No** diseñar taxonomía de clases de afirmación, **no** tocar el payload, **no** crear registro, **no** añadir vocabulario, **no** escribir checker. Nada de eso está justificado por la evidencia obtenida.
5. **Rutear §3.7 por separado**, bajo `PRIORITY.md:10`, con su propia verificación.
6. **Cerrar `PRIORITY.md:0.1` con esta evidencia** en lo que respecta a su objetivo declarado (Q4): el fallo que §0.1 teme no tiene instancia abierta; lo que queda es una causa distinta, ya dimensionada.

---

## Anexo A — Trazabilidad

| Afirmación | Evidencia |
|---|---|
| F-1: no existe artefacto equivalente | búsqueda en `docs/`, `protocol/.agents/`, `docs/working/`, `tools/` |
| F-2: vocabulario ausente en el payload | barrido de `protocol/.agents/**` por `aspiration\|hypothes\|aspiraci\|hipótesis` → 0 coincidencias |
| F-4a: `claim_class` invocado por DEV | `docs/adr/01-guarantee-model.md:44,56,77`; `docs/rfc/62-…md:59`; `docs/MIGRATION.md:156,224`; `docs/working/audits/architecture-capability-review.md:1885` |
| F-4b | `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:17,31` |
| F-4c | `protocol/.agents/standards/quality/CONFIDENCE.md:5,15–19,23` |
| F-4d | `docs/behavior-patterns.md:507–508` |
| D-1 | `AGENTS.md:24–26`; `tests/AGENTS.md:9–14,62–69,80,88–89`; 26 archivos de `tests/` con `protocol/` |
| D-2 | `docs/ADOPTION.md:156–160`; `protocol/.agents/harness/INDEX.md:16`; `CHANGELOG.md:1570–1574` |
| D-3a–f | `ROADMAP.md:29,30–32,55–57,108,115`; `git rev-parse origin/dist` = `aebd0c4`; `git show origin/dist:.agents/VERSION` = `12.1.0`; `git merge-base --is-ancestor 1181db6 origin/dist` = 0; tag `12.1.0` → `45809c1` = `master`; `git diff dev master -- protocol/` vacío; `docs/plans/168-release-12-1-0.md:135,142,193` |
| Contrato del ROADMAP violado por S4 | `docs/CONVENTIONS.md:781,807` |
| O-1 | `tests/AGENTS.md:9–14,73–91` |
| O-6 | `git ls-tree --name-only origin/dist` → `.agents`, `AGENTS.md` |
| §3.7 | `docs/plans/168-release-12-1-0.md:135`; `git log -1 origin/dist` = `aebd0c4` 2026-10-15; `docs/plans/169-…md:170` |
| Cobertura y límites | `tools/check_plan_citations.py:194–210` |

---

_Fin del reporte de auditoría. La Fase 0 termina con evidencia y veredicto, no con implementación. Ninguna superficie fue modificada. No se ejecutó ninguna fase posterior._
