# Priority 0.3 — Modelo de fallos, decisiones y contrato de implementación

**Naturaleza documental:** Working / design closure — **no normativo**. Puede ser provenance, nunca autoridad. No decide por sí mismo, no autoriza trabajo y no modifica el comportamiento del repositorio ni del protocolo.
**Fecha:** 2026-10-20
**Origen:** instrucción directa del mantenedor de esta sesión. Referencia de priorización: `PRIORITY.md:0.3. Modelo de fallos de ARgentOS` (archivo **untracked**; su texto relevante se reproduce en §2.1; **no** es provenance versionada ni autoridad).
**Autoridad de esta sesión:** diagnóstico, clasificación, decisión de alcance y preparación. **No** incluye implementar, añadir invariantes, añadir gates, cambiar el payload ni resolver decisiones reservadas al mantenedor.
**Estado:** `DIAGNÓSTICO CERRADO` · `DECISIONES CERRADAS O ESCALADAS` · `SCOPE DEFINIDO` · `CONTRATO DE IMPLEMENTACIÓN LISTO` · **`IMPLEMENTACIÓN NO INICIADA`**.
**Baseline:** rama `dev`; HEAD `b7e1b29858cf616bab9c655bfd07c7c751067d37`; upstream `origin/dev` sincronizado (`+0 −0`); worktree con dos archivos preexistentes sin trackear (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), preservados intactos, más este artefacto nuevo (sin trackear al momento de escribir).

---

## 0. Resultado

```text
RESULT = PRIORITY_0.3_READY_FOR_IMPLEMENTATION
```

La diagnosis está cerrada y el alcance es finito. La implementación **no** se ejecutó. El siguiente paso válido es un Change DEV Clase B (plan `Aprobado para ejecución`) que materialice las correcciones y las detecciones definidas en §12; no requiere RFC porque no toca `protocol/.agents/`, no cambia garantías normativas y no añade invariantes.

Las cinco conclusiones que sostienen el resultado:

1. **El fallo central de ARgentOS no es la ausencia de forma, sino la confusión entre forma y verdad.** Los controles existentes validan estructura, presencia, identidad y consistencia declarada; ninguno valida que una interpretación sea correcta, que una decisión sea verdadera o que la evidencia pruebe la afirmación. La cadena `interpretación incorrecta → decisión válida → plan válido → ejecución válida → verificación válida → evidencia válida → cierre válido → conocimiento persistente incorrecto` **es posible hoy** y está confirmada por instancias reales, no sólo por hipótesis.
2. **Priority 0.2 ya cubre el núcleo estructural y de trazabilidad.** El catálogo canónico (`INV-01`…`INV-12`, `PROP-01`…`PROP-03`) contiene las propiedades relevantes; 0.3 **no debe añadir invariantes**. Su aporte es el modelo de propagación, la clasificación de límites epistémicos y un conjunto acotado de correcciones y detecciones.
3. **La incertidumbre semántica se pierde en dos puntos concretos:** la declaración de evidencia (la clase la asigna el autor y una referencia no-atestión puede ser irrelevante) y el cierre (un estado procedural `Closed` se lee después como aval epistémico). `Closed` **no** implica que la decisión sea correcta; 0.3 lo declara explícitamente y no introduce una taxonomía nueva.
4. **La integridad histórica no está protegida; sólo es recuperable desde Git en el mejor caso.** El incidente de corrupción del `CHANGELOG.md` (33 entradas duplicadas, seis checkers en verde) demuestra que una corrupción estructuralmente válida atraviesa los gates. No hay pinning de contenido (1 de 178 artefactos), no hay detección de borrado y el borrado de un registro nunca commiteado es irrecuperable.
5. **La honestidad de enforcement tiene una instancia viva:** `docs/INVARIANTS.md` declara en su bloque canónico `INV-07 = ENFORCED:session-hook`, pero su interpretación local dice «Mecanismo: **ninguno**» y su tabla de vocabulario no define `session-hook`. El verificador de equivalencia pasa porque compara bytes, no semántica. Es exactamente el tipo de fallo que `INV-12` prohíbe y que 0.3 debe corregir y detectar.

---

## 1. Método, evidencia y límites

### 1.1 Qué se hizo

1. **Estado del repositorio:** rama, HEAD, upstream, worktree, tags, `master`, `origin/dist`, `protocol/.agents/VERSION`.
2. **Cierre de Priority 0.2:** RFC-84 `Accepted`, ADR-20/ADR-21 `Accepted`, Plan 170 `Executed`/`Closed`, `docs/INVARIANTS.md` y `protocol/.agents/standards/INVARIANTS.md` materializados; cierre de diseño con `DESIGN COMPLETE = YES` · `IMPLEMENTATION COMPLETE = NO`.
3. **Recuperación del material 0.3:** `PRIORITY.md:0.3`; auditoría 0.1 de superficies de lectura; matriz de Etapa A; catálogo 0.2 y sus 12 gaps; ADR-16/17/18/19/20/21; RFC-46/56/75/84; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `.agents/policies/*`; `docs/behavior-patterns.md`; `EVIDENCE.md`, `MEMORY_SYSTEM.md`, `KNOWLEDGE_LIFECYCLE.md`; checkers y tests.
4. **Verificación de instancias reales** de los fallos (no sólo plausibilidad): corrupción del `CHANGELOG.md`; anomalías de estado en planes cerrados; contradicción de `INV-07`; registros citados inexistentes; gaps de autorización/publicación; defectos de copia detectados por la auditoría 0.1.
5. **Ejecución de los checkers deterministas** y de los gates C-1/C-2/C-3 para obtener evidencia factual del baseline (§15).

### 1.2 Qué es hecho y qué es inferencia

- **Hecho:** todo lo que se cita con `ruta:sección`, comando, commit o salida de checker en §15.
- **Inferencia:** la atribución de un modo de fallo a una etapa del lifecycle, la estimación de potencial silencioso y la recomendación. Se declaran como tales; no se presentan como garantías.
- **Entrada no repository-backed:** las **cuatro clases** (structural / traceability / semantic / epistemic) y la lista de **catorce modos** provienen del diagnóstico previo aportado en la instrucción de esta sesión. **No existe un artefacto 0.3 previo en el repositorio**: la búsqueda en `docs/`, `docs/working/` y `PRIORITY.md` no encontró un modelo de fallos dedicado. Se tratan como *priors analíticos*, verificados uno por uno contra el repositorio. Ninguno se acepta por autoridad; dos se reclasifican (FM-09 y FM-12 como defectos vivos, no sólo riesgos) y varios se resuelven como límites epistémicos o trabajo ya poseído por 0.2.

### 1.3 Límites de esta sesión

- **Sí se ejecutaron ambas patas de `pytest` en esta sesión:** `tests/` → **1371 passed** en 314.75 s; `protocol/.agents/harness/tests/` → **204 passed, 1 skipped** en 10.06 s. La limitación histórica de `tmp_path` (`PermissionError [WinError 5]`) **no aplicó** bajo la política de archivos de esta sesión (`danger-full-access`); los planes previos la declararon bajo otra política, y esa declaración histórica no se invalida. Los checkers deterministas y los gates de lifecycle también se ejecutaron.
- No se auditó línea por línea todo el corpus de 174 planes, 85 RFCs y 21 ADRs. Se verificaron las superficies que el modelo de fallos necesita y las instancias que lo sostienen.
- No se modificó `PRIORITY.md` ni `docs/planificacion-argentos-diseno-2026-10-13.md`; siguen sin trackear y fuera de este Change.
- No se implementó, no se corrigió ningún defecto vivo y no se creó ningún gate. Las correcciones son **alcance de implementación**, no de esta sesión.

---

## 2. Recuperación del material Priority 0.3

### 2.1 La definición de la prioridad

`PRIORITY.md:0.3` pide analizar cómo ARgentOS puede fallar, especialmente de maneras no inmediatamente visibles, e identificar fallos sistémicos, no sólo bugs. Enumera once ejemplos: interpretación incorrecta, comprensión incorrecta del objetivo, planes incompletos, decisiones incorrectas pero coherentes, documentación obsoleta tomada como vigente, memoria incorrecta convertida en conocimiento persistente, evidencia insuficiente interpretada como confirmación, corrupción silenciosa de documentación, pérdida de contexto, estados inconsistentes y autoridad ejercida fuera de los límites.

El diagnóstico previo amplió esa lista a catorce modos y los agrupó en cuatro clases:

```text
1. Structural failures
2. Traceability failures
3. Semantic failures
4. Epistemic failures
```

### 2.2 Material existente que se reutiliza (y no se reescribe)

| Fuente | Qué aporta a 0.3 | Estado |
|---|---|---|
| `docs/INVARIANTS.md` + `protocol/.agents/standards/INVARIANTS.md` | Catálogo canónico de 15 entradas; `INV-03` evidencia, `INV-04` historia, `INV-11` registros, `INV-12` honestidad de enforcement, `PROP-02` no invención, `PROP-03` reconstrucción parcial | active; con una interpretación local desactualizada (§7.3) |
| `docs/working/proposals/PRIORITY_0_2_FINAL_DESIGN_CLOSURE_2026-10-20.md` | Modelo de garantías de siete dimensiones, límites y los 12 gaps; `IMPLEMENTATION COMPLETE = NO` | Working; histórico para 0.3 |
| `docs/adr/20-closed-artifact-governance-and-execution-records.md` | `E1-D1`…`E1-D4`: payload inmutable, run record externo, autoridad derivada, `Closed` terminal para contenido gobernante | Accepted |
| `docs/adr/21-attested-escape-evidence-refs-and-transitions.md` | G-03 rechazado, G-05 implementado, G-06 rechazado por diseño; `E21-1`…`E21-4` | Accepted |
| `docs/rfc/84-cross-domain-fundamental-invariants-exception.md` | Excepción cross-domain, bloque byte a byte, enmienda de E1-G1/G-09 | Accepted |
| `docs/working/audits/AUDITORIA_FASE_0_0_1_SUPERFICIES_DE_LECTURA_2026-10-14.md` | Evidencia empírica de 8 defectos de *restatement* sin re-derivación; `MINIMAL_RULE`; §3.7 publicación remota | Working / audit |
| `docs/behavior-patterns.md:7. Fallo y recuperación` | Taxonomía de señales `VALID/GAP/ANOMALY/BOUNDARY/FAIL/N/A`; límites declarados | Policy descriptiva |
| `protocol/.agents/standards/quality/EVIDENCE.md` | Cinco clases de evidencia, tres clases de claim, invariante VERIFIED, suficiencia | Protocol |
| `protocol/.agents/standards/context/MEMORY_SYSTEM.md` + `KNOWLEDGE_LIFECYCLE.md` | Estado epistémico del claim, contradicción, staleness, consolidación, `active != verified` | Protocol |
| `tools/check_plan_structure.py`, `check_lifecycle_lineage.py`, `check_lifecycle_checkpoint.py`, `check_invariants_equivalence.py` | Controles deterministas existentes y sus límites exactos | DEV tooling |

### 2.3 Lo que **no** existe

- No existe un artefacto 0.3 previo con el modelo de fallos, las decisiones o el contrato. La búsqueda no lo encontró; el diagnóstico previo es una entrada de sesión, no provenance del repositorio.
- No existe un registro de afirmaciones, un catálogo de fallos, una taxonomía de estados de fallo ni un motor de enforcement. `docs/behavior-patterns.md:7` declara explícitamente que el sistema tiene una taxonomía de **señales**, no de estados.
- No existe un mecanismo de memoria DEV; la memoria es una capacidad del Protocol (`MEMORY_SYSTEM.md`), con un runtime de referencia, no un sistema operativo de este repositorio.

---

## 3. Modelo de fallos final

### 3.1 Modelo de propagación

El lifecycle usado como modelo primario es el de `PRIORITY.md` y `AGENTS.md`:

```text
INTENCIÓN
  → COMPRENSIÓN
  → DECISIÓN
  → PLAN
  → EJECUCIÓN
  → VERIFICACIÓN
  → EVIDENCIA
  → CONOCIMIENTO
  → COMPACTACIÓN
  → SIGUIENTE DECISIÓN
```

La pregunta rectora de cada frontera es: **¿qué puede salir mal en esta frontera de modo que la siguiente la acepte como válida?** El modelo no supone que cada etapa sea un gate; supone que cada etapa produce un artefacto que la siguiente consume como premisa.

### 3.2 Matriz resumen

`Clase primaria`: S = structural, T = traceability, Sem = semantic, E = epistemic. `Silencioso`: potencial de que el fallo no se observe antes de convertirse en premisa. `Residual`: riesgo que queda tras los controles actuales.

| ID | Modo de fallo | Clase | Etapa | Silencioso | Residual | Decisión |
|---|---|---|---|---|---|---|
| FM-01 | Interpretación incorrecta de instrucciones u objetivo | Sem / E | Intención → Comprensión | **Alto** | **Alto** | D-0.3-17 aceptado |
| FM-02 | Plan formalmente válido pero incompleto | S / T | Plan | Medio-alto | Medio | D-0.3-17 aceptado; Priority 5 |
| FM-03 | La evidencia existe pero no prueba la afirmación | Sem / E | Verificación → Evidencia | **Alto** | **Alto** | D-0.3-04/05 no-garantía |
| FM-04 | Decisión internamente coherente pero incorrecta | Sem / E | Decisión | **Alto** | **Alto** | D-0.3-17 aceptado |
| FM-05 | Corrupción de documentación histórica | S / T | Conocimiento / Compactación | **Alto** | **Alto** | D-0.3-12 escalado |
| FM-06 | Mutación del payload | S | Ejecución | Medio | Medio | D-0.3-15 aceptado (E1-G1) |
| FM-07 | Desaparición de registros de gobernanza | S / T | Evidencia → Conocimiento | **Alto** | **Alto** | D-0.3-13 fuera de alcance (G-07) |
| FM-08 | Pérdida de contexto | E / T | Compactación → Siguiente decisión | **Alto** | **Alto** | D-0.3-16 fuera de alcance (Priority 14) |
| FM-09 | Estado inconsistente / transición invisible | S / T | Ejecución → Cierre | **Alto** | Medio-alto | D-0.3-09/10 corregir + detectar |
| FM-10 | Documentación obsoleta tomada como vigente | T / Sem | Conocimiento → Siguiente decisión | **Alto** | **Alto** | D-0.3-18 aplicar reglas + corregir instancias |
| FM-11 | Corrupción del conocimiento | Sem / E | Conocimiento / Compactación | **Alto** | **Alto** | D-0.3-05/06 no-garantía |
| FM-12 | Sobredeclaración de enforcement | T / E | Cualquier declaración | **Alto** | **Alto** | D-0.3-19 corregir + detectar |
| FM-13 | Contaminación DEV → Protocol | S / T | Ejecución → Conocimiento | Medio | Medio | D-0.3-20 equivalencia en CI |
| FM-14 | Autoridad/scope correctos aplicados al objetivo equivocado | E / T | Decisión → Ejecución | **Alto** | **Alto** | D-0.3-21 aceptado |

### 3.3 Detalle por modo de fallo

#### FM-01 — Interpretación incorrecta de instrucciones u objetivo

- **Trigger / causa:** instrucción ambigua, conflicto entre capas (DEV vs Protocol), lectura de una descripción como mandato, objetivo inferido en lugar de declarado, ausencia de reformulación.
- **Propagación:** premisa equivocada → decisión plausible → plan correcto para el problema equivocado → ejecución y verificación válidas → cierre → conocimiento equivocado.
- **Síntoma observable:** el plan satisface criterios que no corresponden al pedido; el usuario corrige tarde; el trabajo se repite.
- **Detección actual:** revisión humana; `premises(D)` (`P-1`/`P-2`) declara la intención y la confianza, pero no la contrasta; el hard boundary DEV/Protocol evita una clase de confusión de capas, no la interpretación del objetivo.
- **Prevención actual:** autorización humana del Plan; `INTENT_CONFIDENCE` como vocabulario; ninguna verificación semántica.
- **Recuperación actual:** finding/corrección; STOP; re-planificación.
- **Potencial silencioso:** **alto** — el sistema puede ser internamente consistente de punta a punta.
- **Riesgo residual:** **alto** (epistémico). No es mecanizable por completo.
- **Decisión:** D-0.3-17 — aceptado como riesgo residual; no se crea mecanismo en 0.3. La respuesta pertenece a `PRIORITY.md:11` (Understanding / Reflection Session), no a esta prioridad.

#### FM-02 — Plan formalmente válido pero incompleto

- **Trigger / causa:** cumplir la plantilla sin considerar dimensiones relevantes (rollback, migración, errores, casos límite, documentación, observabilidad); declarar `OUT OF SCOPE` lo que en realidad es un olvido.
- **Propagación:** la ejecución omite casos; la verificación valida sólo el subconjunto declarado; el cierre registra éxito; el conocimiento posterior asume cobertura total.
- **Síntoma observable:** findings post-cierre, retrabajo, tests que faltan, incidentes en casos no previstos.
- **Detección actual:** `check_plan_structure.py` valida forma, estado, placeholders, Amendment Log e presencia en el INDEX; **no** evalúa completitud. Revisión humana.
- **Prevención actual:** plantilla, Change Levels, revisión del mantenedor; ninguna lista de dimensiones obligatoria.
- **Recuperación actual:** finding/corrección/revalidación; plan nuevo.
- **Potencial silencioso:** medio-alto.
- **Riesgo residual:** medio.
- **Decisión:** D-0.3-17 — aceptado; la completitud de planes pertenece a `PRIORITY.md:5`, no a 0.3. 0.3 no crea una taxonomía de completitud.

#### FM-03 — La evidencia existe pero no prueba la afirmación

- **Trigger / causa:** la clase de evidencia la asigna el autor; una referencia `reference` puede ser durable pero irrelevante; una `attestation` puede ser honesta pero no demostrativa; la evidencia puede probar una versión más débil de la claim; el `ref` puede resolver a un objeto que no contiene la afirmación.
- **Propagación:** claim marcada `verified` → cierre → decisión futura la cita como premisa → conocimiento persistente.
- **Síntoma observable:** una afirmación sobrevive pese a hechos contrarios; una auditoría encuentra que la cita no sostiene la claim.
- **Detección actual:** `gate_validator.py` valida estructura; G-05 implementado resuelve `ref` contra el proyecto para clases durables; `audit_gates.py` detecta; ninguna herramienta evalúa **relevancia** ni **suficiencia semántica**.
- **Prevención actual:** *claims rule* del payload, clases V2/V3, `Sufficiency rules`, `NO_ASSUMPTIONS`, `CONFIDENCE.md`. Son reglas de conducta, no garantías.
- **Recuperación actual:** finding/corrección/revalidación; reclasificación de la claim.
- **Potencial silencioso:** **alto**.
- **Riesgo residual:** **alto**. `INV-03` declara explícitamente que la verdad de la evidencia queda fuera.
- **Decisión:** D-0.3-04 — **no se garantiza** que la evidencia pruebe la afirmación; se declara la no-garantía y se exige que toda claim nombre su clase y su referencia. No se crea un motor de relevancia.

#### FM-04 — Decisión internamente coherente pero incorrecta

- **Trigger / causa:** rationale plausible; alternativas no consideradas; supuesto oculto; autoridad humana que decide con información incompleta.
- **Propagación:** ADR/RFC/Plan → ejecución → evidencia → cierre → el artefacto se cita como autoridad en decisiones futuras.
- **Síntoma observable:** la realidad contradice la decisión; no hay contradicción interna que la detecte.
- **Detección actual:** revisión adversarial (disponible, no obligatoria); finding posterior; juicio humano.
- **Prevención actual:** alternativas, rationale, aprobación humana; ninguna verificación de verdad.
- **Recuperación actual:** superseder/enmendar el ADR/RFC; corrección; nuevo plan.
- **Potencial silencioso:** **alto** hasta que aparecen consecuencias.
- **Riesgo residual:** **alto** (epistémico).
- **Decisión:** D-0.3-17 — aceptado; no se mecaniza. 0.3 exige que las decisiones declaren supuestos y condiciones de invalidación cuando corresponda, sin crear un gate nuevo.

#### FM-05 — Corrupción de documentación histórica

- **Trigger / causa:** append/replace ingenuo sobre una línea que se repite; edición masiva; `git add -A`; operación de cierre que escribe en el artefacto equivocado; tool que reescribe historia.
- **Propagación:** la historia corrompida se lee como hecho → una decisión futura la cita → conocimiento persistente.
- **Síntoma observable:** entradas duplicadas o en la sección equivocada, registros de cierre mutados, contenido que sigue siendo estructuralmente válido.
- **Detección actual:** auditoría humana; `check_plan_citations.py` detecta citas rotas, no corrupción semántica; `check_plan_structure.py` valida forma; ningún checker compara el contenido de un artefacto cerrado con su estado de cierre.
- **Prevención actual:** prohibición RFC-46, regla «Closed is terminal», revisión; **sin pinning** (1 de 178 artefactos).
- **Recuperación actual:** Git si el estado corrupto fue commiteado; reflog local; commit de corrección. Si el registro nunca se commiteó, es irrecuperable.
- **Potencial silencioso:** **alto**. El incidente del `CHANGELOG.md` (33 entradas propagadas, seis checkers en verde) es la prueba.
- **Riesgo residual:** **alto**.
- **Decisión:** D-0.3-12 — **escalado**. Una garantía más fuerte (pinning de contenido o append-only enforceable) cambia el contrato de gobernanza y requiere decisión del mantenedor / RFC. 0.3 no la implementa.

#### FM-06 — Mutación del payload

- **Trigger / causa:** `Write`/`Edit` dentro de `.agents/` durante una sesión; hooks no instalados; hook fail-open; operación de release/RFC-56.
- **Propagación:** drift del payload → el adoptante recibe un contrato distinto → la frontera se erosiona.
- **Síntoma observable:** archivo del payload modificado en una sesión; divergencia detectada por `doctor`.
- **Detección actual:** en el proyecto adoptante, el hook de sesión deniega la escritura del payload (`hook_gate.py`, `test_payload_write_is_denied`); `doctor` advisory; `check_protocol_invariants.py` verifica referencias y frontera, no inmutabilidad. En DEV, `protocol/.agents/` se modifica por RFC-56/release, no por el hook.
- **Prevención actual:** E1-G1 implementado (hook, opt-in); RFC-56 para cambios legítimos; release.
- **Recuperación actual:** revertir; `recover`/`doctor`; release.
- **Potencial silencioso:** medio (sólo si no hay hooks instalados).
- **Riesgo residual:** medio; fail-open declarado.
- **Decisión:** D-0.3-15 — aceptado; el límite ya está escrito en `INV-07`. No se añade mecanismo.

#### FM-07 — Desaparición de registros de gobernanza

- **Trigger / causa:** borrado de findings/pending; sobrescritura de un registro; índice que apunta a un archivo ausente; registro que sólo existió en una sesión y nunca se commiteó.
- **Propagación:** la ausencia es indistinguible de que nunca existió → se pierde provenance → la decisión futura se apoya en un registro incompleto.
- **Síntoma observable:** cita a un artefacto inexistente; fila de INDEX sin archivo; acto de autoridad no verificable.
- **Detección actual:** `check_plan_citations.py` detecta targets ausentes; `check_discovery_output.py` verifica el manifest de discovery en ambas direcciones; ningún checker detecta el borrado de un finding/pending.
- **Prevención actual:** regla «findings nunca se borran»; Git; ninguna prohibición mecánica de borrado.
- **Recuperación actual:** Git si fue commiteado; si no, irrecuperable.
- **Potencial silencioso:** **alto**.
- **Riesgo residual:** **alto**.
- **Decisión:** D-0.3-13 — **fuera de alcance de 0.3**; el gap G-07 (detección de borrado) ya tiene dueño y autoridad (Plan Clase B) en el registro de 0.2. 0.3 no lo duplica.

#### FM-08 — Pérdida de contexto

- **Trigger / causa:** compactación de sesión; fin de sesión; `.project/` efímero y no versionado; ausencia de memoria DEV; el agente no sabe qué olvidó.
- **Propagación:** se pierden restricciones, decisiones y preguntas abiertas → se re-decide o se contradice una decisión previa → el conocimiento persistente queda incompleto.
- **Síntoma observable:** el agente vuelve a preguntar lo ya decidido; reabre un cierre; omite una restricción.
- **Detección actual:** ninguna automática; los planes, anchors y checkpoints son la memoria externa; lectura humana.
- **Prevención actual:** artefactos de gobernanza + Git; `PROP-03` declara reconstrucción parcial; no hay recuperación activa de contexto.
- **Recuperación actual:** releer artefactos y Git; reconstrucción parcial por path.
- **Potencial silencioso:** **alto** (el agente no percibe lo que perdió).
- **Riesgo residual:** **alto**.
- **Decisión:** D-0.3-16 — **fuera de alcance**; pertenece a `PRIORITY.md:14` (Context Recovery) y `:4` (DEV Memory). 0.3 no crea memoria ni recuperación.

#### FM-09 — Estado inconsistente / transición invisible

- **Trigger / causa:** edición manual del status; condición derivada no materializada; INDEX no actualizado; cierre declarado con findings abiertos; estado actual no persistido (`state.json`).
- **Propagación:** un plan parece cerrado sin serlo; un lector futuro confía en el status; la decisión siguiente se apoya en un estado falso.
- **Síntoma observable:** status del header ≠ INDEX; `Closed` declarado con `Status: Aprobado para ejecución`; findings `open` en un plan cerrado.
- **Detección actual:** `check_plan_structure.py` valida vocabulario de status y presencia en el INDEX, **no** igualdad; C-2/C-3 validan forma; ninguno comprueba que un plan que declara `Closed` esté `Executed` ni que no tenga findings abiertos.
- **Prevención actual:** reglas de lifecycle; humano; ninguna transición verificable (G-06 rechazado por diseño).
- **Recuperación actual:** corrección; post-close por referencia.
- **Potencial silencioso:** **alto**.
- **Riesgo residual:** medio-alto. Hay **instancias vivas**: 3 desajustes status/INDEX (planes 157, 158, 169) y 4 planes con condición `Closed` y findings con estado `open` (155, 158, 168, 169). En 155 el finding está `open (deferred, owner: mantenedor)`; en 158/168/169 la resolución o la corrección está en prosa pero el estado del finding no se actualizó. El Plan 152 también tiene findings `open`, pero su condición derivada es `Executed`, no `Closed`; no se cuenta como inconsistencia de cierre.
- **Decisión:** D-0.3-09 y D-0.3-10 — reconciliar registros y extender los checkers existentes. No se reabre G-06: la transición **no** se persiste por diseño (ADR-21).

#### FM-10 — Documentación obsoleta tomada como vigente

- **Trigger / causa:** *restatement* sin re-derivación; el dueño del hecho cambia; el resumen de un artefacto cerrado no se actualiza; snapshot con cadencia declarada; falta de ownership o de protocolo de actualización.
- **Propagación:** la copia vieja se lee como actual → decisión equivocada → conocimiento persistente.
- **Síntoma observable:** dos superficies dicen cosas distintas; la fuente citada contradice la copia; el número/estado cambió.
- **Detección actual:** `check_plan_citations.py` detecta citas rotas; auditorías humanas; ningún checker detecta una afirmación obsoleta que sigue resolviendo.
- **Prevención actual:** one-source-of-truth; regla de anclaje `ruta:sección`; regla de frescura del ROADMAP; determinaciones de impacto documental. Ninguna es verificable mecánicamente.
- **Recuperación actual:** corrección; re-derivación; auditoría.
- **Potencial silencioso:** **alto**.
- **Riesgo residual:** **alto**.
- **Decisión:** D-0.3-18 — **no** se crea un mecanismo de sincronización. Se aplican las reglas existentes y se corrigen las instancias vivas. La distinción documento/verificado/current/historical/derived/reconstructed vive en `docs/AGENTS.md` a nivel de artefacto; no se inventa un marcador por afirmación.

#### FM-11 — Corrupción del conocimiento

- **Trigger / causa:** consolidación de una claim incorrecta; pérdida de provenance en la síntesis; generalización no soportada; contradicción no declarada; cierre de una decisión equivocada que luego se cita.
- **Propagación:** conocimiento persistente incorrecto → recuperación futura → decisión futura.
- **Síntoma observable:** conocimiento confiado pero falso; contradicciones suprimidas; procedencia irresoluble.
- **Detección actual:** `PROP-01` gate de no-regresión en consolidación (2 de 8 dimensiones); invariantes de Memory (`I-003`…`I-021`); auditoría. En DEV no hay Memory; el "conocimiento" son los artefactos de gobernanza.
- **Prevención actual:** clases de claim, estados epistémicos (`active`, `stale`, `contradicted`, `verified`), provenance, consolidación versionada.
- **Recuperación actual:** invalidar/superseder; rebuild desde la fuente de verdad; en DEV, corrección por referencia.
- **Potencial silencioso:** **alto**.
- **Riesgo residual:** **alto**.
- **Decisión:** D-0.3-05/06 — **no se garantiza** la verdad del conocimiento; se declara que `active != verified` y que `Closed` no es un estado epistémico. No se construye DEV Memory en 0.3.

#### FM-12 — Sobredeclaración de enforcement

- **Trigger / causa:** una etiqueta declara más enforcement del que existe; el vocabulario no está cerrado; un checker valida forma y se lee como validación semántica; el alcance (`opt-in`, `dev-ci`) se omite.
- **Propagación:** el lector confía en una garantía inexistente → decisión → conocimiento.
- **Síntoma observable:** `ENFORCED` sin mecanismo; etiqueta usada y no definida; recuento que no coincide; interpretación local que contradice el bloque canónico.
- **Detección actual:** **ninguna** que verifique la exactitud de la clase (`INV-12` es meta y no auto-verificable); `check_invariants_equivalence.py` compara bytes, no semántica.
- **Prevención actual:** vocabulario cerrado, `LIMIT` obligatorio, `INV-12`; revisión humana.
- **Recuperación actual:** corrección; reclasificación; finding.
- **Potencial silencioso:** **alto**.
- **Riesgo residual:** **alto**.
- **Instancia viva:** `docs/INVARIANTS.md:79` dice «Mecanismo: **ninguno**» para `INV-07`, mientras el bloque canónico dice `ENFORCED:session-hook`; la tabla de vocabulario (`:39-47`) no define `session-hook`. El hook sí deniega la escritura (`hook_gate.py`, `test_payload_write_is_denied`), de modo que la interpretación local es la desactualizada; el bloque canónico es correcto con su `LIMIT` de hooks instalados.
- **Decisión:** D-0.3-19 — corregir la interpretación local y la tabla de vocabulario; añadir una verificación determinista de que toda etiqueta usada está definida; no se crea un invariante nuevo.

#### FM-13 — Contaminación DEV → Protocol

- **Trigger / causa:** copiar una regla DEV al payload; citar `docs/` desde el payload; duplicar contenido más allá de la excepción aprobada; aplicar una convención de este repositorio como si fuera del producto.
- **Propagación:** el payload depende de DEV o incorpora supuestos de DEV → el adoptante recibe algo que no es el contrato → la frontera se erosiona.
- **Síntoma observable:** `check_protocol_invariants.py` falla por referencia a `docs/`; bloque canónico divergente; regla duplicada.
- **Detección actual:** `check_protocol_invariants.py` (referencias Markdown y allowlist por par exacto); `check_invariants_equivalence.py` (bloque canónico, byte a byte); **no** detecta duplicación semántica fuera del bloque.
- **Prevención actual:** hard boundary, RFC-56, single-source, excepción acotada de RFC-84.
- **Recuperación actual:** revertir; corregir; RFC.
- **Potencial silencioso:** medio.
- **Riesgo residual:** medio.
- **Decisión:** D-0.3-20 — añadir `check_invariants_equivalence.py` a CI (ya está en la batería de `docs/VERSIONING.md` §4.1, no en el workflow); no se crea un detector de duplicación semántica.

#### FM-14 — Autoridad/scope correctos aplicados al objetivo equivocado

- **Trigger / causa:** la pregunta "¿puedo escribir esto?" se responde que sí, pero no se responde "¿es esto lo que hay que hacer?"; una determinación de impacto se lee como autorización; una publicación ocurre sin acto registrado; el scope se cumple y el objetivo no.
- **Propagación:** ejecución formalmente válida de un objetivo equivocado → evidencia → cierre → conocimiento.
- **Síntoma observable:** trabajo correcto que no resuelve el problema; hallazgo posterior; autorización ausente o no verificable.
- **Detección actual:** revisión humana; findings; auditoría. `SAE` contiene scope y autoridad, no corrección del objetivo.
- **Prevención actual:** aprobación del Plan, `Autonomy ⊆ Scope ∩ Authority`, separación de autoridad; ninguna verificación del objetivo.
- **Recuperación actual:** finding/corrección; re-plan; revertir.
- **Potencial silencioso:** **alto**.
- **Riesgo residual:** **alto**.
- **Evidencia:** `<PLAN-169>:F-1` (commit `81bbde1` publicado en `master` y en el tag `12.1.0` sin artefacto de autorización); `<PLAN-136>:F-3` (una determinación `Roadmap impact: REQUIRED` leída como autorización de escritura); `AUDITORIA_FASE_0_0_1…:§3.7` (publicación remota de `12.1.0` no verificada).
- **Decisión:** D-0.3-21 — aceptado como residual; la corrección del objetivo es autoridad humana. Los casos de publicación/autorización se rutean a `PRIORITY.md:10`, no a 0.3.

### 3.4 Modos descartados o reclasificados

- **«Añadir más invariantes»** no es una respuesta automática. Los invariantes existentes cubren el núcleo; el fallo está en la aplicación y en la interpretación, no en la falta de una propiedad. Añadir uno nuevo crearía una segunda fuente y violaría la dirección del `AGENTS.md:Decision-Making Compass`.
- **«Validación de transiciones» (G-06)** no es un gap abierto: ADR-21 lo cerró como `REJECTED / BY DESIGN`. Un validador comprobaría la transición entre estados **declarados por el mismo agente**, no el juicio. Presentarlo como enforcement sería una sobredeclaración. Se acepta el límite de `INV-02`.
- **«Attested escape» (G-03)** no es una capacidad pendiente: ADR-21 lo rechazó. `attested` declara un límite, no habilita una excepción.
- **«Evidencia por hash»** no se adopta: ADR-21 `E21-3` prohíbe declarar integridad por hash mientras el contrato no defina bytes, algoritmo y momento. 0.3 no lo reintroduce.
- **«Registro de afirmaciones / fallos»** no tiene placement y sería un registry: `docs/placement-contract.md` `PC-10`/`PC-20`; `docs/AGENTS.md` y AU-4 lo prohíben. 0.3 no lo crea.

---

## 4. La cadena de propagación

### 4.1 La cadena, con los controles que la atraviesan

```text
INTERPRETACIÓN INCORRECTA
   │  control: revisión humana, premises(D), hard boundary DEV/Protocol
   │  límite: ninguno verifica que la interpretación sea correcta
   ▼
DECISIÓN VÁLIDA
   │  control: RFC/ADR, autoridad, alternativas
   │  límite: coherencia interna ≠ verdad
   ▼
PLAN VÁLIDO
   │  control: plantilla, Change Level, check_plan_structure
   │  límite: forma ≠ completitud
   ▼
EJECUCIÓN VÁLIDA
   │  control: scope/SAE, payload hook, revisión
   │  límite: ejecutar bien lo equivocado sigue siendo válido
   ▼
VERIFICACIÓN VÁLIDA
   │  control: gates, tests, C-1/C-2/C-3
   │  límite: verifica lo especificado, no lo correcto
   ▼
EVIDENCIA VÁLIDA
   │  control: clases V2/V3, ref resuelto, claims rule
   │  límite: la clase la asigna el autor; relevancia no verificada
   ▼
CIERRE VÁLIDO
   │  control: anchor, checkpoint, C-2, determinaciones de impacto
   │  límite: el cierre es procedural; no es una validación semántica
   ▼
CONOCIMIENTO PERSISTENTE INCORRECTO
   │  control: Memory (Protocol) / artefactos de gobernanza (DEV)
   │  límite: el conocimiento se cita como autoridad en la decisión siguiente
   ▼
DECISIÓN FUTURA EQUIVOCADA
```

### 4.2 Las siete preguntas

| # | Pregunta | Respuesta verificada |
|---|---|---|
| 1 | ¿La propagación es posible hoy? | **Sí.** Ningún control de la cadena compara la interpretación con el objetivo ni la evidencia con la verdad de la claim. Las instancias de FM-09, FM-10 y FM-12 demuestran que artefactos estructuralmente válidos pueden ser semánticamente falsos. |
| 2 | ¿Qué controles la interrumpen? | La **revisión humana** (autorización del Plan, aprobación de RFC/ADR, resolución de findings), la **contradicción** detectada por un finding o una auditoría, el **STOP** por `ANOMALY` y la **revalidación**. Son controles de juicio o de contradicción, no de verdad. |
| 3 | ¿Qué controles sólo validan forma? | `check_plan_structure` (forma y presencia), `check_plan_citations` (resolución de citas), `check_invariants_equivalence` (bytes), C-1 (campos del anchor), C-2 (relaciones declaradas), C-3 (forma del lineage). Ninguno decide si el contenido es correcto. |
| 4 | ¿Dónde se pierde la incertidumbre semántica? | **(a)** En la evidencia: la clase la asigna el autor y una referencia no-atestión puede ser irrelevante. **(b)** En el cierre: `Closed` es una condición derivada procedural que se lee después como aval epistémico. **(c)** En la consolidación: una síntesis puede perder la distinción entre `verified`, `inferred` y `assumed`. |
| 5 | ¿El sistema distingue conocido / verificado / inferido / reconstruido / asumido / desconocido? | **Parcialmente, y sólo en el Protocol.** `EVIDENCE.md` distingue `observation`, `measurement`, `attestation`, `assertion`, `reference` y `verified`/`attested`/`inference`. `MEMORY_SYSTEM.md` distingue `active`, `stale`, `contradicted`, `verified` y declara `active != verified`. **DEV no tiene ese vocabulario para sus propias afirmaciones de gobernanza**: tiene `GAP/ANOMALY/FAIL`, `Executed/Closed` y `verified` por anchor, pero no una marca de «inferido», «reconstruido» o «asumido» en la prosa de estado. |
| 6 | ¿0.3 debe introducir o formalizar esas distinciones? | **No como taxonomía nueva.** Debe **mapear** a los vocabularios existentes y declarar que `Closed` no es un estado epistémico. Crear un vocabulario DEV paralelo duplicaría `EVIDENCE.md`/`MEMORY_SYSTEM.md` y violaría el single-source. Si se quisiera una garantía positiva (no sólo una declaración), sería una decisión normativa de mayor autoridad. |
| 7 | ¿Es una decisión de implementación o de protocolo? | La **declaración de no-garantía** y el mapeo son DEV (Clase B). La **garantía positiva** de que la evidencia prueba la claim o de que el conocimiento es verdadero es una decisión de protocolo/garantía (Clase A/C) y **no** se toma aquí; se escala como opción, no como bloqueo. |

### 4.3 La distinción que 0.3 fija

```text
VERIFICADO (procedural)  ≠  VERDADERO (semántico)  ≠  CONOCIDO (epistémico)
```

- `Verified` = existe una validación PASS con anchor para un estado. **No** dice que la proposición sea verdadera.
- `Closed` = `Executed` + governance + checkpoint + consistencia + PASS. **No** dice que la decisión sea correcta.
- `active` (Memory) = la claim está vigente. **No** dice que esté verificada (`I-005`).
- La única evidencia positiva es `VALID` en el vocabulario de señales; la ausencia de evidencia es `GAP`, nunca confirmación.

Esta distinción **no crea un estado ni un invariante**; hace explícito lo que las definiciones ya implican y evita que un lector futuro las colapse.

---

## 5. Integridad histórica

### 5.1 Los casos reales

| Caso | Qué pasó | ¿Estructuralmente válido? | ¿Detectado por un gate? | Recuperación |
|---|---|---|---|---|
| Corrupción del `CHANGELOG.md` | `f75d70a` (plan 166) agregó un bullet a una línea que existía 33 veces; escribió la misma entrada 34 veces, de `[1.0.0]` a `[12.0.0]`. Corregido por `ce91a37` (Clase C, 33 líneas eliminadas). | **Sí** — las 70 secciones y sus headings quedaron intactos | **No** — seis checkers deterministas en verde; se detectó por revisión humana | Git + commit de corrección; la historia publicada no se reescribió |
| `INV-07` en `docs/INVARIANTS.md` | El bloque canónico dice `ENFORCED:session-hook`; la interpretación local dice «Mecanismo: **ninguno**»; el vocabulario no define la etiqueta | **Sí** — el bloque es byte-idéntico a la copia Protocol y el checker pasa | **No** — la equivalencia es byte a byte; nadie compara la interpretación local | Corrección pendiente (D-0.3-08); no se reescribe el bloque |
| Estado de planes 157/158/169 | 157 y 158 declaran `Closed` en el cuerpo pero su `Status` es `Aprobado para ejecución`; 169 está `Executed` pero el INDEX dice `Aprobado para ejecución` | **Sí** — `check_plan_structure` pasa | **No** — sólo valida vocabulario y presencia | Corrección por referencia / INDEX (D-0.3-09) |
| Registros citados inexistentes | RFC-84 citaba auditorías A/B/C y una matriz de cobertura que **no existen ni son recuperables**; fueron retiradas en la reformulación del 2026-10-20 | **Sí** — la cita era sintácticamente válida | **No** — `check_plan_citations` sólo resuelve citas con forma `path:section`; una mención por nombre no se detecta | Retiro declarado; no se reconstruye |
| `HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED` | Actos humanos del 2026-10-02/05 citados en Working docs no están verificados; el Plan 151 adoptó algunas decisiones | **Sí** — el registro existe | **No** — no hay verificación de actos | Declarado como no verificado; no se inventa autorización |
| `81bbde1` / publicación remota | `81bbde1` se publicó en `master` y en el tag `12.1.0` sin artefacto de autorización; además, la publicación remota de `12.1.0` ocurrió y el Plan 168 la declaró fuera de su alcance | **Sí** | **No** — el gate de autorización no cubre el acto de publicación | Finding abierto `<PLAN-169>:F-1`; registro factual, no autorización retroactiva |

### 5.2 Las tres garantías que no son equivalentes

```text
RECUPERABLE DESDE HISTORIA  ≠  PROTEGIDO CONTRA CORRUPCIÓN  ≠  DETECTADO ANTES DE PROPAGAR
```

- **Recuperable:** Git conserva el estado anterior si el objeto fue commiteado. `reflog` es local y caduca; un registro nunca commiteado no es recuperable.
- **Protegido:** sólo si algo impide la escritura o la detecta antes de que se lea. Hoy no hay pinning de contenido (1 de 178 artefactos) ni append-only enforceable.
- **Detectado antes de propagar:** requiere un checker que compare el estado actual con el estado de cierre, o una revisión humana antes de citar. No existe.

### 5.3 Decisión

D-0.3-12: **no se implementa una garantía más fuerte en 0.3.** Se escala la pregunta (contenido pinneado, append-only, o chequeo de diff de artefactos cerrados) al mantenedor porque cambia el contrato de gobernanza y requiere RFC/ADR. El riesgo residual se declara: la historia es **recuperable en el mejor caso**, no protegida ni detectada antes de propagar. Git no es una garantía de integridad.

---

## 6. Documentación obsoleta

### 6.1 La distinción de seis términos

| Término | Qué significa | Dónde existe hoy | ¿Se puede confundir con «vigente»? |
|---|---|---|---|
| **DOCUMENTED** | hay un enunciado en un artefacto | cualquier `.md` | Sí, es el estado por defecto |
| **VERIFIED** | el enunciado tiene evidencia y anchor para el estado | planes/RFC con `## Validation anchor` | Sí, si no se lee el alcance del anchor |
| **CURRENT** | el artefacto está en lifecycle `active` y su dueño lo mantiene | `docs/AGENTS.md:Lifecycle` | Sí, `active` no implica que cada frase sea actual |
| **HISTORICAL** | artefacto cerrado/archivado o snapshot fechado | planes cerrados, RFC/ADR, `docs/VERSIONING.md:9` (snapshot) | Sí, se cita con frecuencia como si fuera estado |
| **DERIVED** | vista regenerable (INDEX) | `docs/plans/INDEX.md`, `docs/*/INDEX.md` | Sí, un INDEX desactualizado parece autoridad |
| **RECONSTRUCTED** | estado inferido desde artefactos y Git | `PROP-03` | Sí, se puede presentar como total |

Estas seis etiquetas son **analíticas de este documento**, no estados de lifecycle nuevos ni un vocabulario normativo. El lifecycle normativo por artefacto sigue siendo `active` / `archived` / `superseded` / `deprecated` (`docs/AGENTS.md:Lifecycle`).

### 6.2 Lo que existe y lo que no

- **Existe** una taxonomía de naturaleza y lifecycle por **artefacto** (`docs/AGENTS.md`), y una regla de anclaje `ruta:sección` (`docs/AGENTS.md:Idiomas y citas`) y de frescura del ROADMAP (`docs/CONVENTIONS.md:Contrato del ROADMAP`).
- **No existe** una marca por **afirmación** que distinga «esto es una copia de un hecho cuyo dueño es otro» de «esto es una re-derivación». La auditoría 0.1 encontró 8 defectos de esa clase y concluyó que la causa era *restatement sin re-derivación*, no falta de disciplina.
- **No existe** un checker que detecte una copia obsoleta que todavía resuelve. `check_plan_citations` detecta citas rotas; una cita válida a un hecho viejo pasa.
- **No existe** un protocolo de actualización por documento más allá de la determinación de cierre `Documentation impact`, que es prosa y no tiene checker (`docs/CONVENTIONS.md:899-902`).

### 6.3 Instancias vivas (no hipótesis)

| Instancia | Evidencia | Clasificación |
|---|---|---|
| `docs/INVARIANTS.md:79` contradice el bloque canónico sobre `INV-07` | Bloque `:24`; interpretación `:79`; vocabulario `:39-47` | Documento **CURRENT** con una copia obsoleta; corregir |
| `docs/INVARIANTS.md:127` enumera los 12 gaps sin distinguir los ya implementados/rechazados | E1-G1/G-09 implementados (RFC-84 Amendment 2026-10-20); G-03/G-06 rechazados y G-05 implementado (ADR-21) | Documento **CURRENT** con estado obsoleto; corregir |
| `docs/plans/INDEX.md` fila 169 dice `Aprobado para ejecución` | El header del plan dice `Executed` y el cuerpo `Closed` | **DERIVED** desactualizado; corregir el INDEX |
| Planes 157/158 declaran `Closed` con `Status: Aprobado para ejecución` | `157:3`, `157:238`; `158:3`, `158:244` | **HISTORICAL** con transición invisible; documentar/corregir por referencia |
| `docs/working/proposals/INDEX.md` fila 0.2 dice 6/15 `ENFORCED` | El bloque canónico y la enmienda de RFC-84 dicen 7/15 | **DERIVED** (registro descriptivo) desactualizado; anotar como histórico |
| `docs/VERSIONING.md:9` dice `dev = 12.1.0` y «no queda payload sin publicar» | `protocol/.agents/VERSION` = `12.3.0`; `master`/`dist` = `12.1.0` | **HISTORICAL/DERIVED** snapshot con cadencia declarada; **no** es defecto, pero no debe citarse como estado corriente |

### 6.4 Decisión

D-0.3-18: **no se crea un mecanismo de sincronización.** El problema no es falta de una capacidad semántica imposible, sino **aplicación** de reglas existentes (anclaje, re-derivación, frescura, ownership por documento). 0.3 corrige las instancias vivas y deja el resto al dueño de cada documento. Un checker de «documentación actualizada» no es determinable y no se crea.

---

## 7. Honestidad de enforcement

### 7.1 El método de siete estados

Para cada garantía relevante se distinguen, sin colapsarlos:

```text
SPECIFIED  →  IMPLEMENTED  →  ENFORCED  →  TESTED  →  VALIDATED  →  OBSERVED  →  ASSUMED
```

- **SPECIFIED:** la norma existe.
- **IMPLEMENTED:** el código la respeta donde aplica.
- **ENFORCED:** un mecanismo **impide** la violación en su alcance.
- **TESTED:** hay un test que la afirma.
- **VALIDATED:** hay una validación registrada con anchor para el estado.
- **OBSERVED:** se ejercitó operacionalmente (dogfood/corrida real).
- **ASSUMED:** se cree sin evidencia.

### 7.2 Matriz de garantías (lectura de 0.3)

| Garantía | SPECIFIED | IMPLEMENTED | ENFORCED | TESTED | VALIDATED | OBSERVED | ASSUMED |
|---|---|---|---|---|---|---|---|
| Hook deniega escritura del payload | Sí (`INV-07`, `PROTOCOL_BOUNDARIES`) | Sí (`hook_gate.py`) | **Sí, opt-in** (hooks instalados; fail-open sin ellos) | Sí (`test_payload_write_is_denied`) | Parcial (tests del payload; no se localizó un anchor específico del hook en esta sesión) | Parcial | No |
| Frontera de referencias DEV/Protocol | Sí (`INV-06`) | Sí | **Sí, dev-ci** | Sí | Sí | Sí | No |
| Equivalencia del bloque canónico | Sí (RFC-84) | Sí (`check_invariants_equivalence.py`) | **No en CI**; manual en la batería | Sí (tests del checker) | Sí | Parcial | No |
| Anchors/checkpoints de validación | Sí (RFC-75/VC-1/GC-1) | Sí (C-1/C-2) | **Advisory**; se ejecutan en el gate local, **no** en CI | Sí | Sí | Sí | No |
| Findings: no borrado y resolución | Sí (LC-1, `.agents` regla 6) | Parcial (C-3 valida forma) | **No**; no detecta borrado ni `open` al cerrar | Parcial | Parcial | **No** (4 planes con `open` y `Closed`; el estado no refleja la resolución) | No |
| Transiciones de estado | Sí (máquinas de estado) | **No** (no persiste estado actual) | **No** (G-06 rechazado por diseño) | Parcial | No | No | No |
| Evidencia prueba la claim | Sí (claims rule) | Parcial (clase/ref) | **No** (juicio) | Parcial | No | No | Implícito en la lectura de «verified» |
| Conocimiento no se corrompe | Sí (Memory) | Parcial (2/8 dimensiones) | **No** | Parcial | Parcial | No | No |
| Registros de gobernanza no desaparecen | Sí (`INV-11`) | Parcial (discovery manifest) | **No** | Parcial | No | No | No |
| Historia cerrada no se corrompe | Sí (RFC-46) | Parcial (prohibición) | **No** (sin pinning) | No | Parcial | **No** (incidente CHANGELOG) | No |
| `Closed` no implica verdad | **No estaba declarado** | — | — | — | — | — | **Sí, implícitamente** |

### 7.3 La instancia viva de `INV-07`

Hecho verificado:

- El bloque canónico de `docs/INVARIANTS.md:24` y `protocol/.agents/standards/INVARIANTS.md:25` declara `INV-07 = ENFORCED:session-hook`, con el `LIMIT` «Sólo con hooks instalados; sin hooks el protocolo corre en modo declarativo (fail-open)».
- La interpretación DEV `docs/INVARIANTS.md:79` dice: «Mecanismo: **ninguno**; el hook permite escrituras en ese espacio y un test fija esa conducta. Verificación: ninguna».
- La tabla de vocabulario `docs/INVARIANTS.md:39-47` no define `session-hook`.
- El código `protocol/.agents/harness/hook_gate.py` deniega la escritura del payload **en un proyecto adoptante**; el test `test_payload_write_is_denied` lo verifica con rutas relativas, absolutas y traversal. En **este repositorio DEV**, `protocol/.agents/` se modifica por la vía RFC-56/release, no por ese hook; el hook protege el layout `.agents/` del adoptante.
- `check_invariants_equivalence.py` devuelve `IDENTICAL: YES` y `PASS`, porque sólo compara el bloque canónico.

**Clasificación:** `docs/INVARIANTS.md` es una Policy **CURRENT** con una interpretación local **obsoleta** y un vocabulario incompleto. El bloque canónico no está mal; la copia interpretativa sí. Es una violación de `INV-12` (una capa declara un enforcement distinto del real) y a la vez una demostración de que la equivalencia byte a byte no garantiza coherencia semántica.

**Corrección decidida (D-0.3-08):** actualizar la interpretación local de `INV-07` para reflejar el hook en el proyecto adoptante y su límite (fail-open sin hooks), y aclarar que en DEV la vía es RFC-56/release; añadir `ENFORCED:session-hook` a la tabla de vocabulario; reconciliar la lista de gaps. **No** se toca el bloque canónico ni la copia Protocol; la corrección es local y se registra como post-close respecto de Plan 170, con referencia al cambio que la autoriza.

### 7.4 Otras sobredeclaraciones o etiquetas obsoletas

- `docs/INVARIANTS.md:127` enumera los 12 gaps como trabajo pendiente sin distinguir los ya implementados (E1-G1, G-05, G-09) ni los rechazados (G-03, G-06). Es una afirmación de estado, no una garantía; se corrige en el mismo Change.
- `docs/working/proposals/INDEX.md` describe el cierre 0.2 con **6/15** `ENFORCED`; la enmienda posterior de RFC-84 y el bloque canónico dicen **7/15**. Es un registro descriptivo; se anota como histórico, no se reescribe el Working.
- `docs/INVARIANTS.md` dice «Materializar el catálogo no los implementa», cierto en general, pero el lector puede inferir que **ninguno** se implementó. La corrección precisa el estado.

### 7.5 Decisión

D-0.3-19: **corregir** las instancias y **añadir una verificación determinista** de que toda etiqueta `ENFORCED:*` usada en el bloque está definida en el vocabulario, y de que el recuento declarado coincide con el bloque. **No** se crea un invariante nuevo; `INV-12` ya existe. La verificación es de forma, no de verdad: no puede probar que un mecanismo realmente impide la violación, sólo que la declaración es internamente consistente. Eso se declara.

---

## 8. Límites epistémicos

### 8.1 Tres niveles

| Nivel | Pregunta | ¿Garantizable? | Qué puede hacer ARgentOS |
|---|---|---|---|
| **A. Corrección estructural** | ¿Existen los campos, el estado y la estructura de evidencia requeridos? | **Sí, en su alcance** | Checkers, gates, esquemas, anchors |
| **B. Corrección semántica** | ¿La evidencia prueba la afirmación? | **No de forma general** | Clases de evidencia, `ref` resoluble, revisión, contradicción, auditoría, declaración de incertidumbre |
| **C. Corrección epistémica** | ¿La creencia sobre el mundo es verdadera? | **No** | Autoridad humana, verificación independiente, no consolidar sin soporte, contener la propagación, declarar el riesgo residual |

### 8.2 Lo que 0.3 decide no garantizar

- Que una interpretación sea correcta.
- Que un plan sea completo.
- Que una decisión sea verdadera.
- Que la evidencia pruebe la claim.
- Que el conocimiento persistente sea verdadero.
- Que la historia no se corrompa.
- Que un registro no desaparezca.
- Que el contexto se recupere.
- Que una transición sea válida (diseño: no se persiste el estado).
- Que el objetivo sea el correcto aunque la autoridad y el scope lo sean.
- Que exista un motor universal de enforcement.

### 8.3 Lo que sí se puede hacer sin garantizar la verdad

| Control | Dónde existe | Qué aporta |
|---|---|---|
| Clasificación explícita de evidencia | `EVIDENCE.md` | Hace visible el tipo de soporte |
| Declaración de incertidumbre | `CONFIDENCE.md`, `premises(D)` | Evita presentar una inferencia como hecho |
| Provenance | anchors, `ref`, `source_files` | Permite reconstruir el origen |
| Calidad de evidencia | `Sufficiency rules`, `NO_ASSUMPTIONS` | Reduce la aceptación de soporte débil |
| Validación independiente | multi-agent / revisión humana | Introduce un segundo juicio |
| Detección de contradicción | `ANOMALY`, Memory `contradicts` | Impide consolidar una contradicción no resuelta |
| Autoridad humana | ADR-16, aprobación de Plan/RFC | Cierra lo que el agente no puede decidir |
| Contención | SAE, scope, hook | Limita el daño de un error |
| No propagación | `Closed` terminal, findings, no reescritura | Evita que un error se convierta en historia |
| Rechazo a consolidar | `PROP-01`, `I-008`, `I-017` | Evita generalizar sin soporte |
| Declaración de riesgo residual | este documento, `LIMIT`, `GAP` | Hace honesto lo que no se garantiza |

### 8.4 Decisión

D-0.3-04/05: **no se garantiza B ni C.** Se declaran como límites y se usan los controles de §8.3. La única garantía positiva que 0.3 mejora es **A** (estructura y consistencia de las declaraciones), más la detección de drift del bloque canónico. Cualquier garantía positiva sobre B/C es una decisión de mayor autoridad (ver E-0.3-2).

---

## 9. Clasificación de gaps y ownership existente

| Gap / modo | Tipo principal | ¿Ya tiene dueño? | Decisión de 0.3 |
|---|---|---|---|
| FM-01 interpretación | epistemic limitation | No; `PRIORITY.md:11` | Aceptado; no mecanismo |
| FM-02 plan incompleto | documentation/tooling gap | No; `PRIORITY.md:5` | Aceptado; no mecanismo |
| FM-03 evidencia no prueba | epistemic limitation + missing detection | Parcial: `INV-03`, G-05 cerrado | No-garantía; sin motor |
| FM-04 decisión incorrecta | epistemic limitation | No; autoridad humana | Aceptado |
| FM-05 corrupción histórica | missing enforcement + missing detection | Parcial: `INV-04`, ADR-20 | Escalado (D-12) |
| FM-06 mutación del payload | missing enforcement (opt-in) | E1-G1 implementado | Residual aceptado |
| FM-07 registros desaparecen | missing detection + recovery | **G-07** (0.2, Plan B) | Fuera de alcance; no duplicar |
| FM-08 pérdida de contexto | missing recovery + tooling | No; `PRIORITY.md:14` | Fuera de alcance |
| FM-09 estado inconsistente | missing enforcement + detection | Parcial: C-1/C-2/C-3 | **Corregir + detectar** |
| FM-10 documentación obsoleta | missing validation + ownership | Parcial: reglas existentes | **Aplicar + corregir instancias** |
| FM-11 conocimiento corrupto | epistemic limitation + missing enforcement | `PROP-01`, Memory | No-garantía; sin DEV Memory |
| FM-12 enforcement overclaim | governance gap + missing detection | `INV-12` (meta) | **Corregir + detectar** |
| FM-13 contaminación DEV→Protocol | protocol-design gap (excepción acotada) | `INV-06`, RFC-84 | Equivalencia en CI |
| FM-14 objetivo equivocado | authority-level (humano) | No; autoridad humana | Aceptado; rutear publicación a Priority 10 |

**Regla de no duplicación.** 0.3 no reabre los gaps de 0.2: G-03/G-05/G-06 están cerrados por ADR-21; E1-G1/G-09 por RFC-84. `E1-G2`…`E1-G5`, `G-04`, `G-07` y `G-08` figuran en el registro de Plan 170 (`PC-2`) con su autoridad; esta sesión **no re-auditó** su estado individual y no los reimplementa. 0.3 los referencia como dependencias.

---

## 10. Registro de decisiones

Cada decisión termina en **un** estado: `RESOLVED`, `AUTHORIZED FOR IMPLEMENTATION`, `ESCALATED`, `EXPLICITLY DEFERRED`, `EXPLICITLY ACCEPTED AS RESIDUAL RISK`, `OUT OF SCOPE`, `BLOCKED`.

`Authority`: **A** = resoluble por esta sesión; **B** = derivable de gobernanza existente; **C** = requiere autoridad superior; **D** = no es una decisión (detalle de implementación).

| ID | Pregunta | Opciones | Recomendación | Authority | Estado | Consecuencia para 0.3 |
|---|---|---|---|---|---|---|
| D-0.3-01 | ¿Cuál es el alcance de 0.3? | A) los 14 modos con mecanismos; B) diagnóstico + correcciones/detecciones acotadas + no-garantías; C) ningún cambio | **B** | A | `RESOLVED` | Alcance finito §11 |
| D-0.3-02 | ¿Se aceptan las cuatro clases y los 14 modos del diagnóstico previo? | A) sí, como marco analítico verificado; B) sustituirlos por el catálogo 0.2; C) rechazarlos | **A**, con reclasificación de FM-09/FM-12 como defectos vivos | A | `RESOLVED` | §3 |
| D-0.3-03 | ¿0.3 añade invariantes? | A) añadir; B) no, mapear a los existentes; C) fusionar | **B** | B | `RESOLVED` | Sin invariantes nuevos |
| D-0.3-04 | ¿Se garantiza que la evidencia prueba la claim? | A) garantizar; B) no garantizar + clase/ref + juicio; C) ignorar | **B** | B | `RESOLVED` | No-garantía declarada |
| D-0.3-05 | ¿Se garantiza la verdad epistémica? | A) sí; B) no, fuera de alcance; C) intentarlo vía Memory | **B** | B | `RESOLVED` | No-garantía; sin DEV Memory |
| D-0.3-06 | ¿`Closed` implica verdad? | A) sí; B) no, es procedural; C) crear un estado nuevo | **B** | B | `RESOLVED` | Declaración explícita; sin estado nuevo |
| D-0.3-07 | ¿Se introduce una taxonomía epistémica nueva? | A) nueva; B) mapear a `EVIDENCE`/`MEMORY`/`GAP`; C) diferir | **B** | B | `RESOLVED` | Sin vocabulario paralelo |
| D-0.3-08 | ¿Se corrige la interpretación local de `INV-07`? | A) corregir interpretación + vocabulario; B) cambiar el bloque canónico; C) dejarlo | **A** | B | `RESOLVED` | Implementación Clase B |
| D-0.3-09 | ¿Se reconcilian los estados/INDEX y los findings abiertos? | A) post-close por referencia + INDEX; B) editar planes cerrados; C) dejarlo | **A** | B | `RESOLVED` | Implementación Clase B; no se edita contenido gobernante |
| D-0.3-10 | ¿Se añaden checks deterministas de consistencia? | A) extender `check_plan_structure` + `check_lifecycle_lineage`; B) checker nuevo; C) no | **A** | B | `RESOLVED` | Extensión de tooling existente |
| D-0.3-11 | ¿Se añade la equivalencia canónica a CI? | A) sí; B) dejarla manual; C) reemplazarla | **A** | B | `RESOLVED` | CI + test negativo |
| D-0.3-12 | ¿Se adopta una garantía más fuerte de integridad histórica? | A) pinning de contenido; B) append-only enforceable; C) no, aceptar + Git; D) RFC/ADR | **C ahora; D si se quiere A/B** | **C** | `ESCALATED` | Fuera del alcance de 0.3 |
| D-0.3-13 | ¿Se implementa detección de borrado (G-07)? | A) en 0.3; B) dejar a G-07; C) descartar | **B** | B | `OUT OF SCOPE` | Dependencia de 0.2 |
| D-0.3-14 | ¿Se implementa validación de transiciones (G-06)? | A) sí; B) aceptar el diseño; C) reabrir | **B** (ADR-21) | B | `EXPLICITLY ACCEPTED AS RESIDUAL RISK` | Sin mecanismo; el límite de `INV-02` se mantiene |
| D-0.3-15 | ¿Se añade enforcement de inmutabilidad del payload? | A) nuevo mecanismo; B) aceptar E1-G1 + fail-open; C) enforcement siempre | **B** | B | `EXPLICITLY ACCEPTED AS RESIDUAL RISK` | Sin mecanismo nuevo; el límite de `INV-07` se mantiene |
| D-0.3-16 | ¿Se construye recuperación de contexto / DEV Memory? | A) sí; B) aceptar + artefactos; C) otro | **B** | B | `OUT OF SCOPE` | Priority 14/4 |
| D-0.3-17 | ¿Se mecanizan interpretación, completitud y decisión correcta? | A) sí; B) aceptar + humano; C) ignorar | **B** | B | `EXPLICITLY ACCEPTED AS RESIDUAL RISK` | Sin mecanismo |
| D-0.3-18 | ¿Se crea un mecanismo de sincronización documental? | A) sí; B) aplicar reglas existentes + corregir instancias; C) no | **B** | B | `RESOLVED` | Sin mecanismo nuevo |
| D-0.3-19 | ¿Cómo se corrige la sobredeclaración de enforcement? | A) invariante nuevo; B) corregir + check de vocabulario + exigir scope/mecanismo/test; C) dejarlo | **B** | B | `RESOLVED` | Implementación Clase B |
| D-0.3-20 | ¿Cómo se controla la contaminación DEV→Protocol? | A) detector de duplicación; B) `INV-06` + equivalencia en CI; C) dejarlo | **B** | B | `RESOLVED` | Solo CI de equivalencia |
| D-0.3-21 | ¿Se detecta el objetivo equivocado con autoridad correcta? | A) checker de objetivo; B) autoridad humana + finding; C) ignorar | **B** | B | `EXPLICITLY ACCEPTED AS RESIDUAL RISK` | Sin mecanismo; rutear publicación |
| D-0.3-22 | ¿Cuál es el criterio de éxito de 0.3? | A) mejorar todas las garantías; B) correcciones/detecciones acotadas + no-garantías; C) sólo documentar | **B** | A | `RESOLVED` | §12, AC-1…AC-10 |

### 10.1 Escalaciones

#### E-0.3-1 — Garantía más fuerte de integridad histórica (deriva de D-0.3-12)

```text
QUESTION       ¿Debe ARgentOS garantizar que el contenido gobernante de un artefacto
               cerrado no pueda modificarse sin detección, en lugar de sólo ser
               recuperable desde Git?
WHY IT MATTERS El incidente del CHANGELOG demuestra que una corrupción estructuralmente
               válida atraviesa todos los gates; la historia es citable como autoridad.
EVIDENCE       ce91a37 (33 entradas duplicadas, seis checkers verdes);
               docs/INVARIANTS.md:67 (pinning en 1 de 178 artefactos);
               INV-04 = NONE; ADR-20 E1-D4 (Closed terminal para contenido gobernante).
OPTIONS        A) pinning por digest en el checkpoint (requiere resolver la
                  auto-referencia y el lugar del digest);
               B) append-only enforceable por un gate de diff sobre artefactos cerrados;
               C) no adoptar una garantía nueva: aceptar el riesgo y declararlo (recomendada);
               D) RFC/ADR que decida A o B con su alcance.
RECOMMENDED    C ahora; D sólo si el mantenedor quiere una garantía positiva.
CONSEQUENCES   A/B cambian el contrato de gobernanza y requieren RFC/ADR; C no mejora
               la garantía, pero evita una sobredeclaración.
WHAT MUST BE DECIDED  Si se adopta A/B, quién es el dueño del digest/ledger, dónde vive,
               qué bytes cubre y cómo se evita la auto-referencia.
```

#### E-0.3-2 — Garantía positiva sobre verdad semántica/epistémica (deriva de D-0.3-04/05)

```text
QUESTION       ¿Debe el protocolo garantizar que una claim marcada «verified» sea
               verdadera, o que el conocimiento consolidado sea correcto?
WHY IT MATTERS Es la diferencia entre una garantía declarativa y una garantía real;
               hoy la clase la asigna el autor y la evidencia no se evalúa por relevancia.
EVIDENCE       EVIDENCE.md:Sufficiency rules; INV-03 LIMIT («la verdad de la evidencia
               queda fuera»); ADR-21 G-03 (no hay escape) y G-05 (ref resuelto);
               MEMORY_SYSTEM.md:active != verified.
OPTIONS        A) garantía mecánica de relevancia (no es decidible en general);
               B) no garantizar y declarar el límite + auditoría humana (recomendada);
               C) garantía limitada a clases concretas (p. ej. measurement) con
                  condiciones explícitas.
RECOMMENDED    B; C sólo si se acota a una clase y se acepta que sigue sin probar la verdad.
CONSEQUENCES   A sería una promesa que el sistema no puede cumplir; B mantiene la
               honestidad y no bloquea 0.3; C añadiría una garantía parcial y un
               contrato nuevo.
WHAT MUST BE DECIDED  Si se quiere C, qué clase, qué condición y quién la valida.
```

#### E-0.3-3 — Corrección en sitio del `Status` de planes cerrados (deriva de D-0.3-09)

```text
QUESTION       ¿Puede corregirse el campo `Status` de un plan cerrado (157/158) que
               declara `Aprobado para ejecución` pero cuyo cuerpo declara `Closed`?
WHY IT MATTERS Determina si la reconciliación se hace por referencia (sin tocar el
               artefacto) o por edición del contenido de un artefacto cerrado.
EVIDENCE       ADR-20 §9: el contenido gobernante se congela; la metadata de lifecycle
               es evolucionable; RFC-46: la historia cerrada no se reescribe;
               .agents/AGENTS.md regla 5: «Closed is terminal».
OPTIONS        A) no editar; registrar el estado derivado por referencia en un artefacto
                  nuevo (recomendada);
               B) editar el `Status` como corrección de metadata con provenance;
               C) dejar el estado como está y no registrar nada.
RECOMMENDED    A; B sólo con un acto explícito del mantenedor que declare que el status
               es metadata evolucionable.
CONSEQUENCES   A preserva la historia y deja el header inconsistente; B lo corrige pero
               crea un precedente de edición de cerrados; C oculta el problema.
WHAT MUST BE DECIDED  Si el `Status` es contenido gobernante o metadata evolucionable.
```

### 10.2 Resumen de autoridad

- **A (resueltas):** D-01, D-02, D-22.
- **B (derivadas/resueltas):** D-03…D-11, D-13…D-21.
- **C (escaladas):** D-12 (E-0.3-1); opción positiva de D-04/05 (E-0.3-2); D-09 en su variante de edición en sitio (E-0.3-3).
- **Bloqueantes para 0.3:** **ninguna**. Las escalaciones son opciones de garantía o de corrección en sitio; el alcance acotado no depende de ellas.

---

## 11. Alcance de Priority 0.3

### 11.1 MUST IMPLEMENT IN 0.3

1. **Corrección de la interpretación local de `INV-07` y del vocabulario de enforcement** en `docs/INVARIANTS.md` (sin tocar el bloque canónico ni la copia Protocol). Incluye reconciliar la lista de gaps con el estado real (E1-G1/G-05/G-09 cerrados; G-03/G-06 rechazados; resto con referencia a Plan 170 `PC-2` y ADR-21).
2. **Reconciliación de registros de estado:** corregir la fila del Plan 169 en `docs/plans/INDEX.md`; registrar por referencia los estados inconsistentes de 157/158 y los 4 planes cerrados con findings `open` (155, 158, 168, 169; el 152 está `Executed`, no `Closed`, y no se cuenta); **no** editar el contenido gobernante de planes cerrados.
3. **Detección determinista de consistencia**, extendiendo los checkers existentes:
   - `check_plan_structure.py`: status del header vs INDEX (base), con un conjunto declarado de casos legacy (157/158) que no se corrige en sitio; la fila 169 sí se corrige porque el INDEX es descriptivo.
   - `check_lifecycle_lineage.py`: findings `open` en un plan que declara `Closed`, con el mismo criterio legacy.
   - `check_invariants_equivalence.py` (o un test asociado): toda etiqueta `ENFORCED:*` usada en el bloque está definida; el recuento declarado coincide con el bloque.
4. **CI:** añadir `python tools/check_invariants_equivalence.py` al workflow `check-protocol.yml` y un test negativo que pruebe que falla si una copia diverge.
5. **Documentación de no-garantías:** el presente artefacto (o una sección de una Policy existente, si el mantenedor lo prefiere) declara que `Closed`/`Verified` son procedurales y que la verdad semántica/epistémica no se garantiza. **No** se crea un invariante nuevo.
6. **Evidencia:** batería canónica completa (7 checkers + ambas patas `pytest`; `check_plan_citations` conserva su baseline preexistente, sin aumento), C-1/C-2/C-3, anchor y checkpoint, `git diff --name-only` dentro del scope.

### 11.2 SHOULD IMPLEMENT IF CAPACITY ALLOWS

- Añadir a `docs/CONVENTIONS.md` o `docs/VERSIONING.md` una frase de interpretación que remita a este artefacto para la distinción `Verified ≠ verdadero` y `Closed ≠ epistémico` (si no se considera ya suficientemente claro).
- Añadir un test de regresión que fije el recuento **7/15 · 2/15 · 6/15** del bloque canónico y el conjunto de etiquetas.
- Añadir un caso de falsificación al checker de lineage: un plan sintético con `Closed` y un finding `open` debe fallar.

### 11.3 DOCUMENT ONLY

- El modelo de fallos, la cadena de propagación y los límites epistémicos (este documento).
- La clasificación de los 14 modos y su ownership.
- Las escalaciones E-0.3-1…E-0.3-3.

### 11.4 TEST ONLY

- Los tests de los checkers extendidos y el test negativo de equivalencia.
- El test de vocabulario/recuento.

### 11.5 TOOLING ONLY

- `tools/check_plan_structure.py`, `tools/check_lifecycle_lineage.py`, `tools/check_invariants_equivalence.py` y `.github/workflows/check-protocol.yml`.
- No se crea un checker nuevo si una extensión de los existentes es suficiente.

### 11.6 PROTOCOL CHANGE

- **Ninguno.** No se toca `protocol/.agents/`, `protocol/_AGENTS.md` ni `dist/`.

### 11.7 RUNTIME CHANGE

- **Ninguno.** No se toca `runtime/`.

### 11.8 GOVERNANCE CHANGE

- **Ninguno.** No se cambia el modelo de autoridad, el lifecycle, las garantías ni los invariantes. Las correcciones son post-close por referencia y la reconciliación de INDEX es descriptiva.

### 11.9 DEFER

- Integridad histórica fuerte (D-12 / E-0.3-1).
- Corrección en sitio del `Status` de planes cerrados (E-0.3-3).
- Garantía positiva semántica/epistémica (E-0.3-2).
- Detección de borrado (G-07, 0.2).
- Validación de transiciones (G-06, rechazada por diseño).
- Context recovery / DEV Memory (Priority 14/4).
- Completitud de planes (Priority 5).
- Understanding/Reflection (Priority 11).

### 11.10 OUT OF SCOPE

- Cualquier cambio en `protocol/.agents/`, `runtime/`, `dist/`.
- Cualquier invariante, propiedad, gate o estado nuevos.
- Cualquier garantía positiva de verdad semántica o epistémica.
- Cualquier registro global de afirmaciones, fallos o decisiones.
- Cualquier mecanismo de sincronización documental automática.
- Cualquier reescritura de historia cerrada.

---

## 12. Contrato de implementación

### 12.1 Qué problema se resuelve

La documentación viva de gobernanza puede contradecir su propia fuente de verdad y los registros de estado pueden ser inconsistentes sin que ningún control lo detecte, mientras el sistema declara garantías que no tiene. 0.3 corrige las instancias demostradas y añade las detecciones deterministas mínimas para que esas clases no vuelvan a pasar silenciosamente.

### 12.2 Por qué

Porque la diagnosis demostró que:
- la equivalencia byte a byte no garantiza coherencia semántica;
- el cierre procedural no garantiza verdad;
- los gates actuales validan forma, no consistencia de estado;
- la honestidad de enforcement es una meta-propiedad sin verificación;
- el coste de corregir estas clases es bajo y no requiere tocar el protocolo.

### 12.3 Failure modes in scope

- FM-09 (estado inconsistente / transición invisible): corrección de registros + detección.
- FM-10 (documentación obsoleta): corrección de las instancias vivas + aplicación de reglas existentes.
- FM-12 (enforcement overclaim): corrección de `INV-07` + check de vocabulario/recuento.
- FM-13 (contaminación DEV→Protocol): equivalencia canónica en CI.

### 12.4 Failure modes explicitly out of scope

- FM-01, FM-02, FM-03, FM-04, FM-05 (garantía fuerte), FM-06 (nuevo mecanismo), FM-07, FM-08, FM-11, FM-14.
- Cualquier pretensión de garantizar verdad semántica o epistémica.

### 12.5 Guarantees that must improve

| ID | Garantía | Estado actual | Estado objetivo | Cómo se prueba |
|---|---|---|---|---|
| G-0.3-1 | Las etiquetas de enforcement usadas están definidas y el recuento coincide | Roto (`INV-07`, vocabulario incompleto) | Consistente | Test/checker + corrección |
| G-0.3-2 | Los estados de plan y los INDEX no se contradicen | Sin detección; 3 casos vivos | Detectado en CI/batería para planes nuevos; legacy declarado | Test con fixture + corrección de la fila 169 |
| G-0.3-3 | Un plan que declara `Closed` no tiene findings `open` | Sin detección; 4 casos vivos | Detectado para cierres nuevos; legacy declarado | Test con fixture + corrección por referencia |
| G-0.3-4 | El bloque canónico no puede divergir sin detección | Checker existe; no en CI | Detectado en CI | Workflow + test negativo |
| G-0.3-5 | Las superficies corregidas no afirman un enforcement superior al real | Instancia viva | Corregida; no se repite en las superficies corregidas | Diff + revisión |

### 12.6 Guarantees that must NOT be claimed

- Que la evidencia prueba la claim.
- Que una decisión es verdadera.
- Que el conocimiento persistente es correcto.
- Que la historia está protegida contra corrupción.
- Que los registros no pueden desaparecer.
- Que el contexto se recupera.
- Que las transiciones se validan.
- Que la interpretación del objetivo es correcta.
- Que existe un motor universal de enforcement.

### 12.7 Artifacts that must change

| Artefacto | Cambio | Autorización |
|---|---|---|
| `docs/INVARIANTS.md` | Interpretación local de `INV-07`; vocabulario `session-hook`; estado de gaps | Plan Clase B + post-close por referencia a Plan 170 |
| `docs/plans/INDEX.md` | Fila 169: `Aprobado para ejecución` → `Executed` | Plan Clase B (INDEX es descriptivo) |
| `tools/check_plan_structure.py` | Regla status/INDEX | Plan Clase B (tooling) |
| `tools/check_lifecycle_lineage.py` | Regla `Closed` + findings `open` | Plan Clase B (tooling) |
| `tools/check_invariants_equivalence.py` | Regla vocabulario/recuento | Plan Clase B (tooling) |
| `.github/workflows/check-protocol.yml` | `check_invariants_equivalence.py` | Plan Clase B (CI) |
| `tests/test_check_plan_structure.py` | Fixture de desajuste | Plan Clase B (tests) |
| `tests/test_check_lifecycle_lineage.py` | Fixture de `Closed` + `open` | Plan Clase B (tests) |
| `tests/test_check_invariants_equivalence.py` | Fixture de etiqueta/recuento + negativo | Plan Clase B (tests) |
| `CHANGELOG.md` | Entrada `[Unreleased]` `(plan N)` | Cierre docs-only (RFC-69) |
| `docs/working/proposals/INDEX.md` | Registro de este artefacto | Este Change |

### 12.8 Runtime / tooling / protocol changes required

- **Runtime:** ninguno.
- **Protocol:** ninguno.
- **Tooling:** las tres extensiones y el workflow de CI.
- **Tests:** los tres fixtures de falsificación.

### 12.9 Required evidence

- Salida de los checkers deterministas (los 7 de `docs/VERSIONING.md` §4.1, incluido `check_invariants_equivalence.py`). `check_plan_citations.py` conserva su baseline preexistente (26 citas rotas históricas + 1 referencia legacy); el Change no debe aumentarlo.
- C-1/C-2/C-3 con `ANOMALY=0` (los `GAP` legacy se declaran).
- `python -m pytest tests/` y `python -m pytest protocol/.agents/harness/tests/` — ejecutar ambas patas; si el entorno de implementación no lo permite, **GAP ambiental declarado**, nunca PASS.
- `git diff --name-only` dentro del scope declarado.
- Anchor y checkpoint con la identidad del estado de cierre.

### 12.10 Acceptance criteria

| AC | Criterio | Verificación |
|---|---|---|
| AC-1 | `docs/INVARIANTS.md` no usa ninguna etiqueta `ENFORCED:*` sin definirla; `INV-07` coincide con el bloque y con el hook; la lista de gaps está reconciliada | Test/checker + lectura contra `hook_gate.py` y RFC-84 |
| AC-2 | `check_invariants_equivalence.py` corre en CI y falla si una copia diverge | Workflow + test negativo |
| AC-3 | `check_plan_structure.py` detecta status/INDEX divergentes; la fila 169 está corregida; 157/158 están declarados legacy | Test con fixture + `git diff` |
| AC-4 | `check_lifecycle_lineage.py` detecta `open` en un plan que declara `Closed`; los 4 casos legacy están declarados | Test con fixture + registro por referencia |
| AC-5 | Este artefacto está registrado en `docs/working/proposals/INDEX.md` y no rompe citas | `check_plan_citations.py` + diff |
| AC-6 | 0 cambios en `protocol/.agents/`, `protocol/_AGENTS.md`, `dist/`, `runtime/` | `git diff --name-only` |
| AC-7 | 0 invariantes/properties nuevos; bloque canónico byte-idéntico | `check_invariants_equivalence.py` + diff |
| AC-8 | El artefacto declara las no-garantías y `Closed` procedural | Lectura de §8/§12.6 |
| AC-9 | Batería canónica ejecutada (7 checkers + ambas patas `pytest`; `check_plan_citations` sin aumento sobre su baseline), C-1/C-2/C-3 `ANOMALY=0`, anchor/checkpoint | Salidas registradas |
| AC-10 | Un lector puede implementar sin re-derivar el modelo de fallos | Checklist §13 + revisión |

### 12.11 What would constitute failure

- Añadir un invariante nuevo o cambiar el bloque canónico.
- Tocar `protocol/.agents/`, `runtime/` o `dist/`.
- Reescribir el contenido gobernante de un plan/RFC/ADR cerrado.
- Declarar una garantía semántica/epistémica positiva.
- Introducir un registro global de afirmaciones/fallos/decisiones.
- Añadir un gate que no tenga un caso de falsificación.
- Cerrar sin anchor/checkpoint o con un `GAP` presentado como `PASS`.
- Convertir este contrato en una autorización de implementación sin plan aprobado.

### 12.12 Secuencia de implementación

1. Crear el Plan Clase B con este artefacto como `Depende de`/provenance; declarar `Change Level` L2 y el scope exacto.
2. Corregir `docs/INVARIANTS.md` (interpretación/vocabulario/gaps) sin tocar el bloque canónico.
3. Corregir la fila 169 del INDEX; registrar por referencia 157/158 y los 4 casos de findings (155, 158, 168, 169).
4. Extender `check_plan_structure.py` + test.
5. Extender `check_lifecycle_lineage.py` + test.
6. Extender `check_invariants_equivalence.py` + test.
7. Añadir el checker a CI.
8. Ejecutar la batería, C-1/C-2/C-3, registrar anchor/checkpoint, `CHANGELOG.md` `[Unreleased]`, INDEX del plan.
9. Cerrar el Plan y materializar el commit atómico en `dev` conforme a la autoridad del Change (la acción de commit es del mantenedor o del Change autorizado, no de este contrato).

---

## 13. Readiness gate

### 13.1 Diagnostic completeness

- [x] Los 14 modos conocidos están clasificados.
- [x] Las rutas de propagación están entendidas y dibujadas.
- [x] Los caminos de fallo silencioso están identificados.
- [x] Las limitaciones conocidas están separadas de los gaps.
- [x] No queda evidencia contradictoria sin explicar; las contradicciones se registran como hallazgos (§14).

### 13.2 Decision completeness

- [x] Cada gap material tiene una decisión.
- [x] Cada decisión tiene clasificación de autoridad.
- [x] Las decisiones A están resueltas.
- [x] Las decisiones B están derivadas y cerradas.
- [x] Las decisiones C están escaladas.
- [x] Los riesgos residuales están aceptados o diferidos explícitamente.
- [x] No hay decisión material escondida en prosa.

### 13.3 Scope completeness

- [x] 0.3 tiene alcance finito (§11).
- [x] Lo fuera de alcance es explícito.
- [x] No se añadió arquitectura especulativa.
- [x] No se implementó nada.

### 13.4 Implementation readiness

- [x] Una sesión futura puede empezar sin redescubrir el modelo de fallos (este documento).
- [x] Los artefactos requeridos están identificados.
- [x] Los tests requeridos están identificados.
- [x] Los gates de validación están identificados.
- [x] La evidencia requerida está definida.
- [x] Los criterios de éxito son medibles.
- [x] Los límites de autoridad son claros.

**Veredicto del gate:** `PASS` para el alcance acotado. Las escalaciones E-0.3-1…E-0.3-3 no bloquean: son opciones de garantía o de corrección en sitio fuera del alcance elegido.

---

## 14. Hallazgos registrados por esta sesión

Identificadores locales de este Working (`F-0.3-N`); **no** son refs calificadas LC-1 `<artifact>:F-n` y no crean un namespace de gobernanza.

| ID | Hallazgo | Evidencia | Severidad | Routing |
|---|---|---|---|---|
| F-0.3-01 | `docs/INVARIANTS.md:79` contradice el bloque canónico sobre `INV-07`; `:39-47` no define `session-hook` | Bloque `:24`; interpretación `:79`; `hook_gate.py`; `test_payload_write_is_denied`; `check_invariants_equivalence` PASS | **Alta** (INV-12) | Corrección D-0.3-08/19 |
| F-0.3-02 | `docs/INVARIANTS.md:127` enumera los 12 gaps sin distinguir los ya implementados/rechazados | RFC-84 Amendment; ADR-21 | Media | Corrección D-0.3-08 |
| F-0.3-03 | `docs/plans/INDEX.md` fila 169 dice `Aprobado para ejecución`; el plan está `Executed`/`Closed` | `169:3`; `169:171`; INDEX fila 169 | Media | Corrección D-0.3-09 |
| F-0.3-04 | Planes 157/158 declaran `Closed` con `Status: Aprobado para ejecución` | `157:3,238`; `158:3,244` | Media | Registrar por referencia; D-0.3-09/E-0.3-3 |
| F-0.3-05 | 4 planes cerrados tienen findings con estado `open`: 155 (deferred con owner), 158/168/169 (resolución/corrección en prosa, estado no actualizado); el 152 está `Executed`, no `Closed` | `estado: open` + condición `Closed`; `.agents/policies/validation-closure.md` §7 | **Alta** (integridad del estado de cierre) | Registrar por referencia; checker D-0.3-10 |
| F-0.3-06 | El `CHANGELOG.md` recibió 33 entradas duplicadas en secciones históricas con gates verdes | `ce91a37`; mensaje de commit; checkers del momento | **Alta** | Escalación D-0.3-12 |
| F-0.3-07 | RFC-84 citaba auditorías A/B/C inexistentes; retiradas | `docs/rfc/84-cross-domain-fundamental-invariants-exception.md:8,180` | Media | Histórico; sin acción |
| F-0.3-08 | `HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`; actos humanos no verificados | `docs/working/proposals/INDEX.md:17-37` | Media | Histórico; no inventar autoridad |
| F-0.3-09 | `81bbde1` publicado en `master`/tag `12.1.0` sin artefacto de autorización | `<PLAN-169>:F-1`; `git merge-base --is-ancestor` | Media | `<PLAN-169>:F-1`; Priority 10 |
| F-0.3-10 | Publicación remota de `12.1.0` ejecutada y no verificada como acto autorizado | `AUDITORIA_FASE_0_0_1…:§3.7`; `docs/VERSIONING.md:9` | Media | Priority 10; no 0.3 |
| F-0.3-11 | `check_plan_structure` valida presencia en INDEX, no igualdad de estado | Docstring del checker; 3 casos | Media | D-0.3-10 |
| F-0.3-12 | `check_lifecycle_lineage` no detecta findings `open` en un plan cerrado | Docstring; 4 casos; C-3 `VALID` | **Alta** | D-0.3-10 |
| F-0.3-13 | `check_invariants_equivalence` no está en CI | `.github/workflows/check-protocol.yml`; `docs/VERSIONING.md:157` | Media | D-0.3-11 |
| F-0.3-14 | El snapshot de `docs/VERSIONING.md:9` no refleja `VERSION = 12.3.0` | `protocol/.agents/VERSION`; §9 | Baja (snapshot con cadencia declarada) | Documentar; no es defecto |

---

## 15. Evidencia ejecutada

### 15.1 Baseline

```text
git status --porcelain=v2 --branch
# branch.oid b7e1b29858cf616bab9c655bfd07c7c751067d37
# branch.head dev
# branch.upstream origin/dev
# branch.ab +0 -0
? PRIORITY.md
? docs/planificacion-argentos-diseno-2026-10-13.md

git tag --sort=-v:refname | head: 12.1.0 (latest)
git rev-parse --short master: 45809c1
git rev-parse --short origin/dist: aebd0c4
git show origin/dist:.agents/VERSION: 12.1.0
protocol/.agents/VERSION: 12.3.0
```

### 15.2 Checkers y gates (2026-10-20)

| Comando | Resultado |
|---|---|
| `python tools/check_invariants_equivalence.py` | `IDENTICAL: YES`, `PASS`, exit 0 |
| `python tools/check_plan_structure.py` | `All numbered documents conform`, exit 0 |
| `python tools/check_lifecycle_anchor.py` | `VALID=76`, `GAP=0`, `ANOMALY=0`, exit 0 |
| `python tools/check_lifecycle_lineage.py` | `VALID=41`, `GAP=0`, `BOUNDARY=1`, `ANOMALY=0`; plan 169 `VALID`, exit 0 |
| `python tools/check_lifecycle_checkpoint.py` | `VALID=75`, `GAP=1` (plan 116), `ANOMALY=0`; plan 169 `VALID`, exit 0 |
| `python tools/check_protocol_invariants.py --payload protocol .` | `217 files checked, 10537 references verified`, exit 0 |
| `python tools/check_taxonomy_coherence.py` | `Taxonomy coherence OK`, exit 0 |
| `python tools/check_plan_citations.py` | exit 1; 26 citas rotas históricas + 1 referencia legacy preexistente (baseline declarado) |
| `python -m pytest tests/` | **1371 passed** en 314.75 s, exit 0 |
| `python -m pytest protocol/.agents/harness/tests/` | **204 passed, 1 skipped** en 10.06 s, exit 0 (el skip es el caso de symlink que requiere privilegios en Windows) |

**Lectura:** los checkers verdes **no** detectan F-0.3-01…F-0.3-05 ni F-0.3-11/F-0.3-12. Esa es la evidencia central de 0.3: la forma está verde y la consistencia semántica/estado no.

### 15.3 Fuentes citadas

`AGENTS.md`; `.agents/AGENTS.md`; `.agents/policies/authority.md`; `.agents/policies/validation-closure.md`; `.agents/policies/lifecycle-checkers.md`; `.agents/workflows/change-lifecycle.md`; `docs/AGENTS.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `docs/placement-contract.md`; `docs/INVARIANTS.md`; `docs/adr/16-change-lifecycle-authority.md`; `docs/adr/17-repository-lifetime-and-composite-structure.md`; `docs/adr/18-payload-boundary-provenance-and-classification.md`; `docs/adr/19-autonomy-envelope-authority.md`; `docs/adr/20-closed-artifact-governance-and-execution-records.md`; `docs/adr/21-attested-escape-evidence-refs-and-transitions.md`; `docs/rfc/46-historical-trace-policy.md`; `docs/rfc/56-governance-fast-track.md`; `docs/rfc/75-change-lifecycle.md`; `docs/rfc/84-cross-domain-fundamental-invariants-exception.md`; `docs/plans/136-d01-mechanical-checker.md`; `docs/plans/157-canonical-visual-roadmap.md`; `docs/plans/158-radical-simplification-roadmap.md`; `docs/plans/169-regularizacion-de-81bbde1-y-reconciliacion-de-pendientes.md`; `docs/plans/170-materialize-canonical-invariants-catalog.md`; `docs/working/proposals/PRIORITY_0_2_FINAL_DESIGN_CLOSURE_2026-10-20.md`; `docs/working/audits/AUDITORIA_FASE_0_0_1_SUPERFICIES_DE_LECTURA_2026-10-14.md`; `docs/behavior-patterns.md`; `protocol/.agents/standards/quality/EVIDENCE.md`; `protocol/.agents/standards/context/MEMORY_SYSTEM.md`; `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`; `protocol/.agents/harness/hook_gate.py`; `protocol/.agents/harness/tests/test_hook_gate.py`; `tools/check_*.py`; `.github/workflows/check-protocol.yml`.

---

## 16. Lo que este documento no hace

- No implementa ninguna corrección.
- No modifica `docs/INVARIANTS.md`, `docs/plans/INDEX.md`, los checkers, CI, `protocol/`, `runtime/` ni `dist/`.
- No añade invariantes, properties, gates, estados, registros ni autoridad.
- No reabre Priority 0.2 ni reescribe sus artefactos cerrados.
- No resuelve las escalaciones E-0.3-1…E-0.3-3.
- No declara que ARgentOS garantice verdad semántica o epistémica.

**Fin del documento.** El siguiente paso es un Change DEV Clase B que materialice §11.1/§12 bajo un Plan `Aprobado para ejecución`.
