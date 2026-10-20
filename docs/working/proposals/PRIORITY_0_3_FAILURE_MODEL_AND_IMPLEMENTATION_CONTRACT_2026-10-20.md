# Priority 0.3 — Definitive Decision Closure

**Naturaleza documental:** Working / decision closure — **no normativo**. Puede ser provenance, nunca autoridad. No decide por sí mismo ni modifica el comportamiento del repositorio.
**Fecha:** 2026-10-20 (revisión definitiva).
**Estado:** **CANÓNICO para Priority 0.3**. Esta revisión **supersede** la revisión del 2026-10-20 registrada en el commit `8e30d4f`; la revisión anterior permanece en la historia de Git como evidencia y no se reescribe.
**Origen:** instrucción directa del mantenedor de esta sesión. Referencia de priorización: `PRIORITY.md:0.3` (archivo **untracked**; su contenido se refleja en §B; **no** es provenance versionada ni autoridad).
**Autoridad de esta sesión:** diagnóstico, normalización de decisiones, clasificación de autoridad, alcance y contrato. **No** incluye implementar, añadir invariantes, añadir gates, cambiar el payload ni aceptar riesgos en nombre del mantenedor.
**Baseline de la sesión:** rama `dev`; HEAD inicial `8e30d4f` (que contiene la revisión previa de este artefacto); upstream `origin/dev`; worktree con dos archivos preexistentes sin trackear (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), preservados intactos.

---

## A. Executive conclusion

```text
STATUS = READY FOR IMPLEMENTATION
SCOPE  = the bounded 0.3 implementation defined in §F
```

La frontera de razonamiento de Priority 0.3 está cerrada: los 15 modos de fallo tienen una disposición única; las 23 decisiones materiales tienen exactamente un estado terminal; las dos decisiones que requieren autoridad superior están identificadas con su pregunta y su impacto exactos; los dos riesgos residuales que se declaran aceptados tienen un acto de autoridad real (RFC-84 y ADR-21); el resto de los riesgos se declara **no aceptado** (escalado, diferido, fuera de alcance o registrado); y el contrato de implementación es finito, con criterios de aceptación y de no-aceptación objetivas.

`READY` significa que **no queda ninguna decisión de 0.3 que un implementador deba redescubrir o reinterpretar**. **No** significa que la implementación esté autorizada: el Change de implementación requiere un Plan DEV Clase B `Aprobado para ejecución`, y esa autorización **no ha sido ejercida**. Es una puerta del Change Lifecycle, no una decisión 0.3 pendiente.

Lo que 0.3 **no** promete: que una interpretación sea correcta; que un plan sea completo; que la evidencia pruebe la verdad; que una decisión sea objetivamente correcta; que el conocimiento persistente sea verdadero; que la historia esté protegida contra corrupción; que los registros no puedan desaparecer; que el contexto se recupere; que las transiciones se validen. Esos límites se declaran en §E y §K, no se disfrazan de garantías.

Las cinco conclusiones que sostienen el resultado:

1. **El fallo central no es la ausencia de forma, sino la confusión entre forma y verdad.** Los controles actuales validan estructura, presencia, identidad y consistencia declarada; ninguno valida que una interpretación sea correcta, que una decisión sea verdadera o que la evidencia pruebe la afirmación.
2. **Priority 0.2 ya cubre el núcleo estructural y de trazabilidad.** El catálogo canónico `INV-01`…`INV-12` y `PROP-01`…`PROP-03` contiene las propiedades relevantes; 0.3 **no añade invariantes**.
3. **La incertidumbre semántica se pierde en dos puntos:** la declaración de evidencia (la clase la asigna el autor; una referencia no-atestión puede ser irrelevante) y el cierre (`Closed` es procedural y se lee después como aval epistémico).
4. **La integridad histórica no está protegida; sólo es recuperable desde Git en el mejor caso.** El incidente del `CHANGELOG.md` (33 entradas duplicadas, seis checkers en verde) demuestra que una corrupción estructuralmente válida atraviesa los gates. No hay pinning de contenido (1 de 178 artefactos), no hay detección de borrado y un registro nunca commiteado es irrecuperable.
5. **La honestidad de enforcement tiene una instancia viva:** `docs/INVARIANTS.md` declara `INV-07 = ENFORCED:session-hook` en el bloque canónico, pero su interpretación local dice «Mecanismo: **ninguno**» y su tabla de vocabulario no define `session-hook`. El verificador de equivalencia pasa porque compara bytes, no semántica.

---

## B. Final failure model

### B.1 Modelo de propagación

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

La pregunta de cada frontera es: **¿qué puede salir mal aquí de modo que la siguiente frontera lo acepte como válido?** El modelo no supone que cada etapa sea un gate; supone que cada etapa produce un artefacto que la siguiente consume como premisa.

### B.2 Matriz final de fallos y disposiciones

`Disposición` usa exactamente el vocabulario de §B.4. `Riesgo` remite a §E.

| ID | Modo de fallo | Clase | Etapa | Disposición | Decisión | Riesgo |
|---|---|---|---|---|---|---|
| FM-01 | Interpretación incorrecta de instrucciones u objetivo | Sem / E | Intención → Comprensión | **OUT OF SCOPE** | D-0.3-17 | R-01 |
| FM-02 | Plan formalmente válido pero incompleto | S / T | Plan | **OUT OF SCOPE** | D-0.3-17 | R-01 |
| FM-03 | La evidencia existe pero no prueba la afirmación | Sem / E | Verificación → Evidencia | **OUT OF SCOPE** | D-0.3-04/05 | R-01 |
| FM-04 | Decisión internamente coherente pero incorrecta | Sem / E | Decisión | **OUT OF SCOPE** | D-0.3-17 | R-01 |
| FM-05 | Corrupción de documentación histórica | S / T | Conocimiento / Compactación | **ESCALATE** | D-0.3-12 | R-03 |
| FM-06 | Mutación del payload (fail-open sin hooks) | S | Ejecución | **ACCEPT RESIDUAL RISK** | D-0.3-15 | R-10 |
| FM-07 | Desaparición de registros de gobernanza | S / T | Evidencia → Conocimiento | **DEFER** | D-0.3-13 | R-04 |
| FM-08 | Pérdida de contexto | E / T | Compactación → Siguiente decisión | **OUT OF SCOPE** | D-0.3-16 | R-05 |
| FM-09 | Estado inconsistente: status, INDEX o findings desactualizados | S / T | Ejecución → Cierre | **FIX NOW** | D-0.3-09/10 | R-09 |
| FM-10 | Documentación obsoleta en superficies vivas | T / Sem | Conocimiento → Siguiente decisión | **FIX NOW** | D-0.3-18 | R-06 |
| FM-11 | Corrupción del conocimiento | Sem / E | Conocimiento / Compactación | **OUT OF SCOPE** | D-0.3-05/06 | R-01 |
| FM-12 | Sobredeclaración de enforcement | T / E | Cualquier declaración | **FIX NOW** | D-0.3-19 | R-07 |
| FM-13 | Contaminación DEV → Protocol: duplicación/confusión semántica, con detección estructural acotada | S / T | Ejecución → Conocimiento | **DETECT** (sólo manifestaciones estructurales) | D-0.3-20 | R-08 |
| FM-14 | Autoridad/scope correctos aplicados al objetivo equivocado | E / T | Decisión → Ejecución | **OUT OF SCOPE** | D-0.3-21 | R-02 |
| FM-15 | Transición invisible: no se persiste el estado actual ni se valida la transición | S / T | Ejecución → Cierre | **ACCEPT RESIDUAL RISK** | D-0.3-14 | R-11 |

**FM-15 se separa de FM-09** para que cada modo tenga una sola disposición: FM-09 es la inconsistencia de registros, que 0.3 corrige y detecta; FM-15 es la ausencia de validación de transiciones, que ADR-21 rechazó por diseño. El diagnóstico previo agrupaba ambos; la separación es una corrección de clasificación, no un hallazgo nuevo.

### B.3 Detalle por modo de fallo

#### FM-01 — Interpretación incorrecta de instrucciones u objetivo

- **Trigger / causa:** instrucción ambigua, conflicto de capas DEV/Protocol, lectura de una descripción como mandato, objetivo inferido en lugar de declarado.
- **Etapa:** Intención → Comprensión.
- **Propagación:** premisa equivocada → decisión plausible → plan correcto para el problema equivocado → ejecución/verificación válidas → cierre → conocimiento equivocado.
- **Síntoma:** el plan satisface criterios que no corresponden al pedido; corrección tardía; retrabajo.
- **Detección actual:** revisión humana; `premises(D)` declara intención/confianza, no la contrasta; el hard boundary evita confusión de capas, no de objetivo.
- **Prevención actual:** autorización humana del Plan; `INTENT_CONFIDENCE` como vocabulario.
- **Recuperación actual:** finding/corrección; STOP; re-planificación.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto (epistémico).
- **Decisión / disposición:** D-0.3-17; **OUT OF SCOPE** de 0.3; pertenece a `PRIORITY.md:11` (Understanding/Reflection). R-01.

#### FM-02 — Plan formalmente válido pero incompleto

- **Trigger / causa:** cumplir la plantilla sin considerar dimensiones relevantes; declarar `OUT OF SCOPE` lo que es un olvido.
- **Etapa:** Plan.
- **Propagación:** ejecución omite casos; verificación valida el subconjunto declarado; cierre registra éxito; conocimiento posterior asume cobertura total.
- **Síntoma:** findings post-cierre, retrabajo, tests faltantes.
- **Detección actual:** `check_plan_structure.py` valida forma, no completitud; revisión humana.
- **Prevención actual:** plantilla, Change Levels, revisión del mantenedor.
- **Recuperación actual:** finding/corrección/revalidación.
- **Potencial silencioso:** medio-alto.
- **Riesgo residual:** medio.
- **Decisión / disposición:** D-0.3-17; **OUT OF SCOPE**; pertenece a `PRIORITY.md:5`. R-01.

#### FM-03 — La evidencia existe pero no prueba la afirmación

- **Trigger / causa:** clase de evidencia asignada por el autor; referencia durable pero irrelevante; `attestation` honesta pero no demostrativa; evidencia de una versión más débil de la claim.
- **Etapa:** Verificación → Evidencia.
- **Propagación:** claim `verified` → cierre → decisión futura la cita como premisa → conocimiento persistente.
- **Síntoma:** una afirmación sobrevive pese a hechos contrarios; la cita no sostiene la claim.
- **Detección actual:** `gate_validator.py` valida estructura; G-05 resuelve `ref`; `audit_gates.py` detecta; no hay evaluación de relevancia/suficiencia semántica.
- **Prevención actual:** *claims rule*, clases V2/V3, `Sufficiency rules`, `NO_ASSUMPTIONS`, `CONFIDENCE.md`.
- **Recuperación actual:** finding/corrección/revalidación; reclasificación.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto. `INV-03` declara que la verdad de la evidencia queda fuera.
- **Decisión / disposición:** D-0.3-04/05; **OUT OF SCOPE**; no se promete garantía semántica. R-01.

#### FM-04 — Decisión internamente coherente pero incorrecta

- **Trigger / causa:** rationale plausible, alternativas no consideradas, supuesto oculto, información incompleta.
- **Etapa:** Decisión.
- **Propagación:** ADR/RFC/Plan → ejecución → evidencia → cierre → se cita como autoridad futura.
- **Síntoma:** la realidad contradice la decisión; no hay contradicción interna.
- **Detección actual:** revisión adversarial (disponible, no obligatoria); finding posterior; juicio humano.
- **Prevención actual:** alternativas, rationale, aprobación humana; ninguna verificación de verdad.
- **Recuperación actual:** superseder/enmendar ADR/RFC; corrección.
- **Potencial silencioso:** alto hasta que aparecen consecuencias.
- **Riesgo residual:** alto (epistémico).
- **Decisión / disposición:** D-0.3-17; **OUT OF SCOPE**; no se mecaniza. R-01.

#### FM-05 — Corrupción de documentación histórica

- **Trigger / causa:** append/replace ingenuo sobre una línea repetida; edición masiva; `git add -A`; cierre que escribe en el artefacto equivocado.
- **Etapa:** Conocimiento / Compactación.
- **Propagación:** historia corrompida leída como hecho → decisión futura la cita → conocimiento persistente.
- **Síntoma:** entradas duplicadas/fuera de sección, registros mutados, contenido estructuralmente válido.
- **Detección actual:** auditoría humana; `check_plan_citations` detecta citas rotas, no corrupción; ningún checker compara un cerrado con su estado de cierre.
- **Prevención actual:** prohibición RFC-46, «Closed is terminal», revisión; sin pinning (1 de 178).
- **Recuperación actual:** Git si fue commiteado; reflog local; commit de corrección; si no se commiteó, irrecuperable.
- **Potencial silencioso:** alto. Evidencia: `ce91a37` (33 entradas propagadas, seis checkers verdes).
- **Riesgo residual:** alto.
- **Decisión / disposición:** D-0.3-12; **ESCALATE**. Una garantía más fuerte requiere decisión del mantenedor/RFC. R-03.

#### FM-06 — Mutación del payload (fail-open sin hooks)

- **Trigger / causa:** `Write`/`Edit` en `.agents/` del adoptante; hooks no instalados; hook fail-open; release/RFC-56 legítimo.
- **Etapa:** Ejecución.
- **Propagación:** drift del payload → el adoptante recibe un contrato distinto.
- **Síntoma:** archivo modificado en sesión; divergencia detectada por `doctor`.
- **Detección actual:** hook del proyecto adoptante deniega la escritura del payload (`hook_gate.py`, `test_payload_write_is_denied`); `doctor` advisory; `check_protocol_invariants` verifica referencias, no inmutabilidad. En DEV, `protocol/.agents/` se modifica por RFC-56/release, no por el hook.
- **Prevención actual:** E1-G1 (hook opt-in); RFC-56; release.
- **Recuperación actual:** revertir; `recover`/`doctor`; release.
- **Potencial silencioso:** medio (sólo sin hooks).
- **Riesgo residual:** medio; fail-open declarado.
- **Decisión / disposición:** D-0.3-15; **ACCEPT RESIDUAL RISK** con acto de autoridad RFC-84 `Accepted` (LIMIT de INV-07). R-10.

#### FM-07 — Desaparición de registros de gobernanza

- **Trigger / causa:** borrado de findings/pending; sobrescritura; índice que apunta a un archivo ausente; registro nunca commiteado.
- **Etapa:** Evidencia → Conocimiento.
- **Propagación:** ausencia indistinguible de no-existencia → pérdida de provenance → decisión futura incompleta.
- **Síntoma:** cita a artefacto inexistente; fila de INDEX sin archivo; acto no verificable.
- **Detección actual:** `check_plan_citations` detecta targets ausentes; `check_discovery_output` verifica manifest bidireccional; no hay detección de borrado de findings/pending.
- **Prevención actual:** regla «findings nunca se borran»; Git.
- **Recuperación actual:** Git si fue commiteado; si no, irrecuperable.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto.
- **Decisión / disposición:** D-0.3-13; **DEFER** por Plan 170 `PC-2` (G-07, owner mantenedor). R-04.

#### FM-08 — Pérdida de contexto

- **Trigger / causa:** compactación, fin de sesión, `.project/` efímero, ausencia de memoria DEV.
- **Etapa:** Compactación → Siguiente decisión.
- **Propagación:** se pierden restricciones/decisiones → se re-decide o contradice → conocimiento incompleto.
- **Síntoma:** el agente re-pregunta lo decidido, reabre un cierre, omite una restricción.
- **Detección actual:** ninguna automática; planes/anchors/checkpoints son memoria externa.
- **Prevención actual:** artefactos + Git; `PROP-03` declara reconstrucción parcial.
- **Recuperación actual:** releer artefactos/Git; reconstrucción parcial por path.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto.
- **Decisión / disposición:** D-0.3-16; **OUT OF SCOPE**; pertenece a `PRIORITY.md:14`/`:4`. R-05.

#### FM-09 — Estado inconsistente: status, INDEX o findings desactualizados

- **Trigger / causa:** edición manual de status; condición derivada no materializada; INDEX no actualizado; findings con estado `open` en un plan cerrado.
- **Etapa:** Ejecución → Cierre.
- **Propagación:** un plan parece cerrado sin serlo; un lector confía en el status; la decisión siguiente se apoya en un estado falso.
- **Síntoma:** status del header ≠ INDEX; `Closed` con `Status: Aprobado para ejecución`; findings `open` en un plan `Closed`.
- **Detección actual:** `check_plan_structure` valida vocabulario/presencia, no igualdad; C-2/C-3 validan forma, no el stop condition.
- **Prevención actual:** reglas de lifecycle; humano; ninguna transición verificable (FM-15).
- **Recuperación actual:** corrección; post-close por referencia.
- **Potencial silencioso:** alto.
- **Riesgo residual:** medio-alto. Instancias vivas: 3 desajustes status/INDEX (157, 158, 169); 4 planes `Closed` con findings en estado `open` (155, 158, 168, 169; 152 está `Executed`, no `Closed`).
- **Decisión / disposición:** D-0.3-09/10; **FIX NOW** (corregir registros + extender checkers). R-09.

#### FM-10 — Documentación obsoleta en superficies vivas

- **Trigger / causa:** *restatement* sin re-derivación; cambio del dueño del hecho; resumen de un cerrado no actualizado; falta de ownership.
- **Etapa:** Conocimiento → Siguiente decisión.
- **Propagación:** copia vieja leída como actual → decisión equivocada → conocimiento.
- **Síntoma:** dos superficies se contradicen; la fuente citada contradice la copia; número/estado cambió.
- **Detección actual:** `check_plan_citations` detecta citas rotas; auditorías humanas; no detecta una afirmación obsoleta que sigue resolviendo.
- **Prevención actual:** one-source-of-truth, anclaje `ruta:sección`, frescura del ROADMAP, determinaciones de impacto; ninguna verificable mecánicamente.
- **Recuperación actual:** corrección; re-derivación; auditoría.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto.
- **Decisión / disposición:** D-0.3-18; **FIX NOW** para las instancias identificadas (INV-07, gaps, INDEX 169, etc.); no se crea sincronizador general. R-06.

#### FM-11 — Corrupción del conocimiento

- **Trigger / causa:** consolidación de una claim incorrecta; pérdida de provenance; generalización no soportada; contradicción no declarada.
- **Etapa:** Conocimiento / Compactación.
- **Propagación:** conocimiento persistente incorrecto → recuperación futura → decisión futura.
- **Síntoma:** conocimiento confiado pero falso; contradicciones suprimidas; procedencia irresoluble.
- **Detección actual:** `PROP-01` gate de consolidación (2 de 8 dimensiones); invariantes de Memory; auditoría. En DEV no hay Memory.
- **Prevención actual:** clases de claim, estados epistémicos, provenance, consolidación versionada.
- **Recuperación actual:** invalidar/superseder; rebuild desde la fuente de verdad; en DEV, corrección por referencia.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto.
- **Decisión / disposición:** D-0.3-05/06; **OUT OF SCOPE**; no se construye DEV Memory. R-01.

#### FM-12 — Sobredeclaración de enforcement

- **Trigger / causa:** etiqueta declara más enforcement del real; vocabulario no cerrado; checker de forma leído como validación semántica; alcance omitido.
- **Etapa:** Cualquier declaración.
- **Propagación:** lector confía en una garantía inexistente → decisión → conocimiento.
- **Síntoma:** `ENFORCED` sin mecanismo; etiqueta no definida; recuento inconsistente; interpretación local contra el bloque canónico.
- **Detección actual:** ninguna que verifique la exactitud de la clase (`INV-12` es meta y no auto-verificable); `check_invariants_equivalence` compara bytes, no semántica.
- **Prevención actual:** vocabulario cerrado, `LIMIT`, `INV-12`; revisión humana.
- **Recuperación actual:** corrección; reclasificación; finding.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto.
- **Instancia viva:** `docs/INVARIANTS.md:79` dice «Mecanismo: **ninguno**» para INV-07 mientras el bloque canónico dice `ENFORCED:session-hook`; el vocabulario (`:39-47`) no define `session-hook`; el hook sí deniega en el adoptante; la interpretación local es la desactualizada.
- **Decisión / disposición:** D-0.3-19; **FIX NOW** (corregir + check de vocabulario/recuento). R-07.

#### FM-13 — Contaminación DEV → Protocol: duplicación/confusión semántica

- **Failure mode conceptual:** una regla, concepto o supuesto DEV se copia o se confunde con el contrato del Protocol; el payload pasa a depender semánticamente de DEV o incorpora una duplicación que no está en la excepción aprobada.
- **Trigger / causa:** copiar una regla DEV al payload; citar `docs/`; duplicar contenido más allá de la excepción de RFC-84; aplicar una convención de este repositorio como si fuera del producto.
- **Etapa:** Ejecución → Conocimiento.
- **Propagación:** payload depende de DEV o incorpora supuestos DEV → el adoptante recibe un contrato distinto → la frontera se erosiona.
- **Síntoma estructural:** `check_protocol_invariants` falla por una referencia a `docs/`; el bloque canónico delimitado por `canonical-invariants-v1` diverge entre las dos copias; aparece una duplicación dentro del bloque autorizado.
- **Detección actual (acotada):** `check_protocol_invariants.py` verifica referencias Markdown y la allowlist por par exacto; `check_invariants_equivalence.py` compara **byte a byte** el bloque canónico y su forma. **No** detecta duplicación semántica general, paráfrasis, equivalencia conceptual ni reglas DEV replicadas con otras palabras.
- **Prevención actual:** hard boundary, RFC-56, single-source, excepción acotada de RFC-84.
- **Recuperación actual:** revertir; corregir; RFC.
- **Potencial silencioso:** medio.
- **Riesgo residual:** medio; R-08.
- **Alcance de la disposición `DETECT`:** se limita a (a) referencias DEV→Protocol y (b) divergencia del bloque canónico autorizado. `DETECT ≠ garantía de detección semántica completa`.
- **Decisión / disposición:** D-0.3-20; **DETECT** (equivalencia del bloque en CI); no se crea un detector semántico general. R-08.

#### FM-14 — Autoridad/scope correctos aplicados al objetivo equivocado

- **Trigger / causa:** se responde «¿puedo escribir esto?» pero no «¿es esto lo que hay que hacer?»; una determinación de impacto se lee como autorización; publicación sin acto registrado.
- **Etapa:** Decisión → Ejecución.
- **Propagación:** ejecución formalmente válida de un objetivo equivocado → evidencia → cierre → conocimiento.
- **Síntoma:** trabajo correcto que no resuelve el problema; hallazgo posterior; autorización ausente.
- **Detección actual:** revisión humana; findings; auditoría. SAE contiene scope/autoridad, no corrección del objetivo.
- **Prevención actual:** aprobación del Plan, `Autonomy ⊆ Scope ∩ Authority`; ninguna verificación del objetivo.
- **Recuperación actual:** finding/corrección; re-plan; revertir.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto.
- **Evidencia:** `<PLAN-169>:F-1` (81bbde1 publicado sin autorización); `<PLAN-136>:F-3` (impacto leído como autorización); `AUDITORIA_FASE_0_0_1…:§3.7` (publicación remota no verificada).
- **Decisión / disposición:** D-0.3-21; **OUT OF SCOPE**; corrección del objetivo es autoridad humana; publicación se rutea a PRIORITY 10. R-02.

#### FM-15 — Transición invisible: no se persiste el estado actual ni se valida la transición

- **Trigger / causa:** `state.json` persiste gates/status, no el estado actual; las máquinas de estado declaran transiciones en prosa; el juez es el mismo agente.
- **Etapa:** Ejecución → Cierre.
- **Propagación:** un salto de estado es invisible; el cierre se apoya en una transición no verificada.
- **Síntoma:** no hay campo de estado actual; una transición inválida no se detecta.
- **Detección actual:** ninguna ejecutable; las máquinas de estado son normativas, no datos.
- **Prevención actual:** juicio del agente; registro de gates.
- **Recuperación actual:** no aplica; el diseño no persiste el estado.
- **Potencial silencioso:** alto.
- **Riesgo residual:** alto.
- **Decisión / disposición:** D-0.3-14; **ACCEPT RESIDUAL RISK** con acto de autoridad ADR-21 `Accepted` (G-06 rechazado por diseño). R-11.

### B.4 Disposition vocabulary and summary

Cada modo de fallo tiene **exactamente una** disposición:

| Disposición | Significado | Modos |
|---|---|---|
| **FIX NOW** | 0.3 corrige las instancias identificadas y añade la detección determinista correspondiente | FM-09, FM-10, FM-12 |
| **DETECT** | 0.3 añade una detección determinista de una manifestación estructural acotada; no detecta equivalencia o duplicación semántica general | FM-13 |
| **ACCEPT RESIDUAL RISK** | un acto de autoridad real aceptó el límite; se cita el acto | FM-06 (RFC-84), FM-15 (ADR-21) |
| **DEFER** | una autoridad existente difirió el trabajo a otro Change con owner | FM-07 (Plan 170 `PC-2`) |
| **ESCALATE** | requiere autoridad superior; no hay decisión; se registra pregunta y autoridad | FM-05 (D-0.3-12) |
| **OUT OF SCOPE** | 0.3 no lo intenta; el riesgo permanece abierto y **no** se declara aceptado | FM-01, FM-02, FM-03, FM-04, FM-08, FM-11, FM-14 |

No hay modos huérfanos: los 15 aparecen exactamente en una fila de §B.2 y en una disposición de §B.4.

### B.5 Modos descartados o reclasificados

- **«Añadir más invariantes»** no es una respuesta automática. Los invariantes existentes cubren el núcleo; el fallo está en la aplicación/interpretación. Añadir uno nuevo crearía una segunda fuente y violaría el `AGENTS.md:Decision-Making Compass`.
- **Validación de transiciones (G-06)** no es un gap abierto: ADR-21 lo cerró como `REJECTED / BY DESIGN`; se acepta el límite de INV-02 (FM-15).
- **Attested escape (G-03)** no es capacidad pendiente: ADR-21 lo rechazó; `attested` declara un límite.
- **Evidencia por hash** no se adopta: ADR-21 `E21-3` prohíbe declarar integridad por hash sin bytes/algoritmo/momento definidos.
- **Registro de afirmaciones/fallos** no tiene placement y sería un registry: `docs/placement-contract.md` PC-10/PC-20; `docs/AGENTS.md` y AU-4 lo prohíben.

### B.6 Structural, semantic and epistemic correctness

| Nivel | Pregunta | Lo que 0.3 establece | Lo que 0.3 no establece |
|---|---|---|---|
| **Structural** | ¿Existen los campos, el estado y la estructura de evidencia requeridos? | Checks deterministas de forma, presencia, identidad y consistencia de registros; CI de equivalencia; hook de payload (opt-in) | Que el contenido sea correcto |
| **Semantic** | ¿La evidencia prueba la afirmación? | Clases de evidencia, `ref` resoluble, revisión humana, contradicción, auditoría | Que la evidencia entalle la verdad de la claim |
| **Epistemic** | ¿La creencia sobre el mundo es verdadera? | Autoridad humana, verificación independiente, contención, no consolidación sin soporte, riesgo residual declarado | Que el conocimiento persistente sea verdadero |

Vocabulario de fuerza, sin colapsarlo:

```text
mechanically enforceable   → checks estructurales, boundary, equivalencia en CI, hook opt-in
procedurally constrained   → cierre, anchors, findings, determinaciones de impacto
human-validated            → decisiones, relevancia de evidencia, aceptación de riesgo
experimentally evidenced   → tests, dogfoods, corridas reales
not guaranteed             → verdad semántica/epistémica, historia protegida, registros persistentes, contexto
```

### B.7 Enforcement honesty (siete estados)

`SPECIFIED ≠ IMPLEMENTED ≠ ENFORCED ≠ TESTED ≠ VALIDATED ≠ OBSERVED ≠ ASSUMED`.

| Propiedad / mecanismo | SPECIFIED | IMPLEMENTED | ENFORCED | TESTED | VALIDATED | OBSERVED | ASSUMED |
|---|---|---|---|---|---|---|---|
| Hook deniega escritura del payload (adoptante) | Sí (INV-07, PROTOCOL_BOUNDARIES) | Sí | **Sí, opt-in** (hooks instalados; fail-open sin ellos) | Sí | Parcial (tests del payload; sin anchor específico localizado) | Parcial | No |
| Frontera de referencias DEV/Protocol | Sí (INV-06) | Sí | **Sí, dev-ci** | Sí | Sí | Sí | No |
| Equivalencia del bloque canónico | Sí (RFC-84) | Sí | **No en CI** (manual en la batería; 0.3 la añade a CI) | Sí | Sí | Parcial | No |
| Anchors/checkpoints de validación | Sí (RFC-75/VC-1/GC-1) | Sí (C-1/C-2) | **Advisory**; gate local, no CI | Sí | Sí | Sí | No |
| Findings: no borrado y resolución | Sí (LC-1) | Parcial (C-3 valida forma) | **No**; no detecta borrado ni `open` al cerrar | Parcial | Parcial | **No** (4 planes con `open` y `Closed`) | No |
| Transiciones de estado | Sí (máquinas de estado) | **No** (no persiste estado actual) | **No** (G-06 rechazado por diseño) | Parcial | No | No | No |
| Evidencia prueba la claim | Sí (claims rule) | Parcial (clase/ref) | **No** (juicio) | Parcial | No | No | Implícito en la lectura de «verified» |
| Conocimiento no se corrompe | Sí (Memory) | Parcial (2/8 dimensiones) | **No** | Parcial | Parcial | No | No |
| Registros de gobernanza no desaparecen | Sí (INV-11) | Parcial (discovery manifest) | **No** | Parcial | No | No | No |
| Historia cerrada no se corrompe | Sí (RFC-46) | Parcial (prohibición) | **No** (sin pinning) | No | Parcial | **No** (incidente CHANGELOG) | No |
| `Closed` no implica verdad | **No estaba declarado** | — | — | — | — | — | **Sí, implícitamente** |

La lectura correcta es la más débil que la evidencia sostiene: un test que afirma una propiedad no la impide; un gate advisory no bloquea; un hook opt-in no protege sin hooks; una validación de forma no valida semántica. En particular, **FM-13**: sólo se detectan referencias DEV/Protocol y divergencia byte a byte del bloque canónico; la duplicación semántica general no está detectada ni garantizada.

---

## C. Final decision table

### C.1 Canonical table

Esta es la **única** tabla canónica de decisiones de Priority 0.3. Cualquier otra lista de decisiones en este artefacto es explicativa y no puede contradecir esta tabla. `Decision` contiene exactamente un estado terminal.

| ID | Question | Current State | Decision | Authority | Authority Exercised? | Evidence | Implementation Impact | Residual Risk |
|---|---|---|---|---|---|---|---|---|
| D-0.3-01 | ¿Cuál es el alcance de 0.3? | 15 modos; diagnóstico previo; riesgo de expansión | **RESOLVED** | A | **Yes** — this session, under the maintainer's instruction | §B–§F; `PRIORITY.md:0.3` | Defines §F; no code | R-01…R-11 |
| D-0.3-02 | ¿Se aceptan las cuatro clases y los 15 modos? | Cuatro clases y 14 modos previos; FM-15 separado | **RESOLVED** | A | **Yes** — this session | §B.2–§B.5 | None | R-01…R-11 |
| D-0.3-03 | ¿0.3 añade invariantes? | Catálogo 0.2 de 15 entradas | **RESOLVED** | B | **N/A** — derived from RFC-84/ADR-20/21 | `docs/INVARIANTS.md`; RFC-84 | No new invariant | R-01 |
| D-0.3-04 | ¿Se garantiza que la evidencia prueba la claim? | `INV-03` declara que la verdad queda fuera | **RESOLVED** | B | **N/A** — derived from `INV-03` | `EVIDENCE.md`; `INV-03` | No positive guarantee | R-01 |
| D-0.3-05 | ¿Se garantiza la verdad epistémica? | No hay oráculo de verdad; `PROP-02` | **RESOLVED** | B | **N/A** — derived from `PROP-02`/`INV-03` | `EVIDENCE.md`; `INVARIANTS.md` | No positive guarantee | R-01 |
| D-0.3-06 | ¿`Closed` implica verdad? | `Closed` es condición derivada procedural | **RESOLVED** | B | **N/A** — derived from `VERSIONING.md:7` and `validation-closure.md:6` | `docs/VERSIONING.md`; `.agents/policies/validation-closure.md` | Documentation clarification | R-01 |
| D-0.3-07 | ¿Se introduce una taxonomía epistémica nueva? | Vocabularios `EVIDENCE`/`MEMORY` ya existen | **RESOLVED** | B | **N/A** — derived from existing vocabularies | `EVIDENCE.md`; `MEMORY_SYSTEM.md` | No parallel taxonomy | R-01 |
| D-0.3-08 | ¿Se corrige la interpretación local de INV-07? | Contradicción viva: bloque `session-hook` vs interpretación «ninguno» | **RESOLVED** | B | **N/A** for the decision; implementation authorization not exercised | `docs/INVARIANTS.md:24,39-47,79`; `hook_gate.py` | Yes — correction of `docs/INVARIANTS.md` | R-07 |
| D-0.3-09 | ¿Se reconcilian status/INDEX y findings? | 3 desajustes status/INDEX; 4 planes `Closed` con findings `open` | **RESOLVED** | B | **N/A** for the decision; implementation authorization not exercised | Plan 169; Plans 155/158/168/169; INDEX | Yes — reconcile records by reference + INDEX 169 | R-09 |
| D-0.3-10 | ¿Se añaden checks deterministas de consistencia? | `check_plan_structure` no compara status; C-3 no mira findings `open` | **RESOLVED** | B | **N/A** for the decision; implementation authorization not exercised | `tools/check_plan_structure.py`; `check_lifecycle_lineage.py` | Yes — extend checkers + tests | R-09 |
| D-0.3-11 | ¿Se añade la equivalencia canónica a CI? | Checker existe; no está en CI | **RESOLVED** | B | **N/A** for the decision; implementation authorization not exercised | `docs/VERSIONING.md:157`; `.github/workflows/check-protocol.yml` | Yes — CI step + negative test | R-08 |
| D-0.3-12 | ¿Se adopta una garantía más fuerte de integridad histórica? | Sin pinning; 1 de 178; corrupción pasó gates | **ESCALATED** | C | **No** — maintainer decision pending | `ce91a37`; `INV-04`; ADR-20 | None for bounded scope; if adopted, RFC/ADR | R-03 |
| D-0.3-13 | ¿Se implementa detección de borrado (G-07)? | Deferred by Plan 170 `PC-2`; owner maintainer | **EXPLICITLY DEFERRED** | B | **Yes** — Plan 170 `PC-2` (deferred, owner maintainer) | `docs/plans/170…:PC-2` | None in 0.3 | R-04 |
| D-0.3-14 | ¿Se implementa validación de transiciones (G-06)? | ADR-21 lo rechazó por diseño | **EXPLICITLY ACCEPTED AS RESIDUAL RISK** | B | **Yes** — ADR-21 `Accepted` (maintainer, 2026-10-20) | `docs/adr/21…:Decision, Amendment Log` | None | R-11 |
| D-0.3-15 | ¿Se añade enforcement de inmutabilidad del payload? | Hook opt-in; fail-open sin hooks; INV-07 LIMIT | **EXPLICITLY ACCEPTED AS RESIDUAL RISK** | B | **Yes** — RFC-84 `Accepted` (maintainer, 2026-10-20) | `docs/rfc/84…:Amendment Log`; `INV-07` | None | R-10 |
| D-0.3-16 | ¿Se construye recuperación de contexto / DEV Memory? | `PROP-03` parcial; no hay DEV Memory | **OUT OF SCOPE** | B | **N/A** — no acceptance claimed | `PROP-03`; `PRIORITY.md:14,4` | None | R-05 |
| D-0.3-17 | ¿Se mecanizan interpretación, completitud y decisión correcta? | Límites epistémicos; no hay oráculo | **OUT OF SCOPE** | B | **N/A** — no acceptance claimed | `PRIORITY.md:5,11`; `INV-03` | None | R-01 |
| D-0.3-18 | ¿Se crea un mecanismo de sincronización documental? | Reglas existentes; no hay checker semántico | **RESOLVED** | B | **N/A** for the decision; implementation authorization not exercised | `docs/AGENTS.md`; `CONVENTIONS.md`; `AUDITORIA_FASE_0_0_1…` | Yes — correct instances; no synchronizer | R-06 |
| D-0.3-19 | ¿Cómo se corrige la sobredeclaración de enforcement? | INV-07 local contradice el bloque | **RESOLVED** | B | **N/A** for the decision; implementation authorization not exercised | `INV-12`; `docs/INVARIANTS.md:24,79` | Yes — correction + vocabulary/count check | R-07 |
| D-0.3-20 | ¿Cómo se controla la contaminación DEV→Protocol? | `INV-06` + excepción RFC-84; no hay detector semántico general | **RESOLVED** | B | **N/A** for the decision; implementation authorization not exercised | `INV-06`; RFC-84; `check_invariants_equivalence.py` | Yes — CI equivalence for the canonical block only; no general semantic detector | R-08 |
| D-0.3-21 | ¿Se detecta el objetivo equivocado con autoridad correcta? | Autoridad humana; SAE no corrige objetivo | **OUT OF SCOPE** | B | **N/A** — no acceptance claimed | `<PLAN-169>:F-1`; `<PLAN-136>:F-3` | None | R-02 |
| D-0.3-22 | ¿Cuál es el criterio de éxito de 0.3? | Sin criterio único | **RESOLVED** | A | **Yes** — this session | §G–§J | Defines completion | None |
| D-0.3-23 | ¿Es el `Status` de un plan cerrado contenido gobernante o metadata evolucionable? | 157/158 declaran `Closed` con `Status: Aprobado para ejecución`; 0.3 no edita cerrados | **ESCALATED** | C | **No** — maintainer governance decision pending | ADR-20 §9; RFC-46; `.agents/AGENTS.md` rule 5 | None for bounded scope; if “evolvable”, separate correction Change | R-09 |

**Counts:** 23 decisions: **15 RESOLVED**, **2 ESCALATED**, **1 EXPLICITLY DEFERRED**, **2 EXPLICITLY ACCEPTED AS RESIDUAL RISK**, **3 OUT OF SCOPE**, **0 BLOCKED**, **0 AUTHORIZED FOR IMPLEMENTATION**. `AUTHORIZED FOR IMPLEMENTATION` is not used because the implementation Change has not been authorized; that is a lifecycle gate, not a 0.3 decision.

**Failure-mode mapping.** D-0.3-01…D-0.3-11, D-0.3-18, D-0.3-22 and D-0.3-23 are **governance/documentation infrastructure** decisions. The remaining decisions map to failure modes: D-12→FM-05, D-13→FM-07, D-14→FM-15, D-15→FM-06, D-16→FM-08, D-17→FM-01/02/04, D-19→FM-12, D-20→FM-13, D-21→FM-14. No decision is left without either a failure mode or an explicit infrastructure classification.

### C.2 Authority model

Definitions: **A** = agent-resolvable within existing governance; **B** = derivable from existing governance; **C** = requires higher human/governance authority; **D** = not a decision (implementation detail). Authority classification is independent of decision status.

For each material decision, the canonical table answers:

| Question | Where it is answered |
|---|---|
| A. What is the question? | `Question` column |
| B. What is the current factual state? | `Current State` column + §M evidence |
| C. What decision is required? | `Decision` column |
| D. Who has authority? | `Authority` + `Authority Exercised?` |
| E. Has it been exercised? | `Authority Exercised?` |
| F. Where is the record? | `Evidence` column |
| G. What remains outstanding? | `ESCALATED` / `DEFERRED` rows |
| H. Does it block implementation? | `Implementation Impact` column |

**Authority acts actually exercised (records):**

- **RFC-84 `Accepted`** (maintainer, 2026-10-20) — accepts the canonical catalog and the INV-07 `ENFORCED:session-hook` limit (fail-open without hooks). This is the authority record for D-0.3-15.
- **ADR-21 `Accepted`** (maintainer, 2026-10-20) — rejects G-03 (no attested escape) and G-06 (no transition validation) by design. This is the authority record for D-0.3-14.
- **ADR-20 `Accepted`** — closed-artifact governance (`E1-D1`…`E1-D4`); it defines governing content vs lifecycle metadata but does **not** decide whether `Status` is evolvable. That is D-0.3-23.
- **Plan 170 `Executed`/`Closed` + `PC-2`** — records the deferral of the remaining 0.2 enforcement gaps, including G-07, with owner maintainer. This is the authority record for D-0.3-13.
- **Plan 169** — records `<PLAN-169>:F-1` (81bbde1 published without authorization artifact) and `<PLAN-169>:F-2` (stale pending records) as open findings; it does not authorize the publication retroactively.

**Implementation authorization:** **not yet exercised.** The bounded 0.3 implementation requires a Plan DEV Clase B `Aprobado para ejecución` approved by the maintainer. No RFC is required because the contract does not touch `protocol/.agents/`, `runtime/` or `dist/`, and adds no invariant, gate, state or normative guarantee.

### C.3 Escalations and deferred decision detail

#### E-0.3-1 = D-0.3-12 — Stronger historical-integrity guarantee

```text
STATUS              = ESCALATED
AUTHORITY REQUIRED  = maintainer (governance decision; RFC/ADR if adopted)
QUESTION            = ¿Debe ARgentOS garantizar que el contenido gobernante de un
                      artefacto cerrado no pueda modificarse sin detección, en lugar
                      de sólo ser recuperable desde Git?
AUTHORITY EXERCISED = No. No existe acto que adopte pinning de contenido ni append-only.
EVIDENCE            = ce91a37 (33 entradas duplicadas, seis checkers verdes);
                      INV-04 = NONE; docs/INVARIANTS.md:67 (pinning 1 de 178);
                      ADR-20 E1-D4 (Closed terminal para contenido gobernante).
IMPLEMENTATION IMPACT = None for the bounded 0.3 implementation. If adopted, it requires
                      an RFC/ADR and a separate Change; it does not gate §F.
```

#### E-0.3-3 = D-0.3-23 — `Status` of a closed plan: governing content or evolvable metadata?

```text
STATUS              = ESCALATED
CLASSIFICATION      = governance decision (closed-artifact boundary); not a
                      documentation correction and not an implementation decision.
AUTHORITY REQUIRED  = maintainer (governance decision; interpretation of ADR-20 E1-D4)
QUESTION            = ¿Es el campo `Status` de un plan cerrado contenido gobernante
                      (no editable) o metadata de lifecycle evolucionable (editable
                      con provenance)?
AUTHORITY EXERCISED = No. ADR-20 §9 distingue contenido gobernante de metadata de
                      lifecycle, pero no enumera `Status`; RFC-46 prohíbe reescribir
                      historia cerrada; .agents/AGENTS.md regla 5 dice «Closed is terminal».
EVIDENCE            = ADR-20 §9; RFC-46; .agents/AGENTS.md regla 5;
                      docs/plans/157…:3,238; docs/plans/158…:3,244.
IMPLEMENTATION IMPACT = None for the bounded 0.3 implementation. 0.3 records the
                      derived state by reference and does not edit 157/158. If the
                      maintainer decides “evolvable”, a separate correction Change
                      may edit the field; if “governing”, the current record stands.
```

#### D-0.3-13 — Deferred decision detail (G-07)

```text
STATUS              = EXPLICITLY DEFERRED
DEFERRED BY         = Plan 170 `PC-2` (owner: maintainer; destino: Changes propios)
REASON              = G-07 (deletion detection) is an enforcement gap owned by the
                      Priority 0.2 gap register; 0.3 does not duplicate it.
UNBLOCK CONDITION   = a G-07 Change with its own authorization (Class B plan) is approved.
IMPLEMENTATION IMPACT = None for the bounded 0.3 implementation.
```

**No other open escalations exist.** E-0.3-2 from the previous revision (positive semantic/epistemic guarantee) is **not** an escalation: 0.3 explicitly chooses not to pursue it, so it is `OUT OF SCOPE` under D-0.3-04/05. It is not represented as an unresolved decision.

### C.4 Single-ledger rule

- This §C.1 is the only canonical decision ledger for Priority 0.3.
- The previous revision (`8e30d4f`) contained 22 decisions, 3 escalations, and `EXPLICITLY ACCEPTED AS RESIDUAL RISK` entries for D-0.3-17 and D-0.3-21 without an authority act. **This revision supersedes those states**: D-0.3-17 and D-0.3-21 are `OUT OF SCOPE`; E-0.3-2 is removed as an escalation; E-0.3-3 is D-0.3-23 with `ESCALATED`.
- No other 0.3 artifact exists. The proposals INDEX points to this file.

---

## D. Authority model — closed from first principles

### D.1 Authority classes

- **A — agent-resolvable:** the repository's existing authority model gives this session enough authority to decide. Used for scope, acceptance of the verified failure model, and success criteria.
- **B — derivable:** the answer already follows from an existing normative rule, invariant, RFC, ADR or established policy. Used for no-new-invariants, no-positive-guarantee, `Closed` procedural, no-new-taxonomy, the correction path, and the accepted limits of RFC-84/ADR-21.
- **C — higher authority:** changes protocol semantics, normative guarantees, adoption behavior, public contract, governance rules, authority boundaries, fundamental architecture or project policy. Used for stronger historical integrity and the `Status` governance question.
- **D — not a decision:** implementation detail already constrained by policy. Used only for the choice of mechanism inside the contract (e.g., extending an existing checker rather than creating a new one); it is not listed as a material decision.

### D.2 Authority exercised, not assumed

| Act | Date | Authority | What it decided | Used for |
|---|---|---|---|---|
| RFC-84 `Accepted` | 2026-10-20 | Maintainer | Canonical catalog; cross-domain exception; INV-07 `session-hook` with fail-open limit | D-0.3-15; D-0.3-03/04/05 |
| ADR-20 `Accepted` | 2026-10-20 | Maintainer | Closed artifacts; execution records; authority derived; `Closed` terminal for governing content | D-0.3-06; D-0.3-23 evidence |
| ADR-21 `Accepted` | 2026-10-20 | Maintainer | G-03 rejected; G-05 implemented; G-06 rejected by design | D-0.3-14; D-0.3-03 |
| Plan 170 `Executed`/`Closed` | 2026-10-20 | Maintainer (plan) | Materialized catalog; `PC-2` deferred the remaining 0.2 gaps, including G-07 | D-0.3-13 |
| Plan 169 `Executed`/`Closed` | 2026-10-14 | Maintainer (plan) | Recorded 81bbde1 and stale pending records; no retroactive authorization | FM-14 evidence |

**Not exercised:** stronger historical integrity (D-12); `Status` field interpretation (D-23); implementation authorization (Class B plan). None is invented.

### D.3 Current derived record vs historical closed record

```text
CURRENT DERIVED RECORD          HISTORICAL CLOSED RECORD
INDEX / proposals INDEX         Plans, RFCs, ADRs once Closed/Accepted
mutable, descriptive            governing content frozen (RFC-46, ADR-20 E1-D4)
correction allowed              correction only by new artifact referencing the closed one
```

Rules for this closure:

- `docs/plans/INDEX.md` is a **current derived record**: its Plan 169 row may be corrected to `Executed`; it is not a rewrite of history.
- Plans 157/158 are **historical closed records**: their `Status` field is the subject of D-0.3-23; 0.3 **does not edit them**. It records the derived state by reference.
- `docs/working/proposals/INDEX.md` is a **current derived record**: it is updated to point to this canonical artifact; the previous row remains in Git history.
- No RFC, ADR, closed plan or changelog history is edited by this session.

### D.4 Implementation authorization

The bounded implementation is **not authorized** by this session. It requires:

```text
CHANGE CLASS      = DEV Clase B (documentary + tooling + tests; no payload effect)
AUTHORIZATION     = Plan `Aprobado para ejecución` by the maintainer
RFC REQUIRED      = No (no protocol/.agents/, runtime/ or dist/ changes)
PAYLOAD EFFECT    = None
```

This is a lifecycle gate, not an unresolved 0.3 decision. The 0.3 reasoning boundary is closed; the plan approval is the next Change.

---

## E. Residual-risk register

Only risks with an actual authority act are marked **ACCEPTED**. The others remain **NOT ACCEPTED** and are either escalated, deferred, or out of scope; they are not disguised as accepted.

| Risk ID | Failure mode | Why not eliminated | Current control | Exposure | Impact | Owner / authority | Acceptance status | Reopen trigger |
|---|---|---|---|---|---|---|---|---|
| R-01 | FM-01/02/03/04/11 | Semantic/epistemic limits; no truth oracle; no general relevance check | Human review, evidence classes, provenance, audits, contradiction detection | High | High | Maintainer | **NOT ACCEPTED** — out of 0.3 scope | A material wrong interpretation/decision survives closure, or an audit finds evidence that does not support the claim |
| R-02 | FM-14 | Objective correctness is not mechanizable; authority checks scope, not purpose | Plan approval; human authority; findings | High | High | Maintainer | **NOT ACCEPTED** — out of 0.3 scope | A scope-valid action is found to miss the authorized objective |
| R-03 | FM-05 | No content pinning; 1 de 178; no diff-vs-closure check | RFC-46 prohibition; advisory checkers; Git recovery | High | High | Maintainer | **NOT ACCEPTED** — escalated D-0.3-12 | A closed artifact is mutated without detection, or a corruption passes all gates |
| R-04 | FM-07 | No deletion detection; absence is indistinguishable from never-existed | Git if committed; discovery manifest; rules | High | High | Maintainer / G-07 | **NOT ACCEPTED** — deferred by Plan 170 `PC-2` | A cited governance record disappears or an INDEX row has no target |
| R-05 | FM-08 | Context is ephemeral; no DEV Memory; no active recovery | Plans, anchors, checkpoints, Git | High | High | Maintainer / Priority 14 | **NOT ACCEPTED** — out of 0.3 scope | A session loses a material constraint or reopens a closed decision |
| R-06 | FM-10 | Stale copies can still resolve; no semantic checker | Corrections of identified instances; citation/freshness rules | Medium | High | Document owners / maintainer | **NOT ACCEPTED** — partially mitigated | A live document contradicts its source of truth |
| R-07 | FM-12 | Enforcement honesty is a meta-property; not auto-verifiable | Closed vocabulary; LIMIT; vocabulary/count check | Medium | High | Maintainer | **NOT ACCEPTED** — partially mitigated | An `ENFORCED` claim lacks a mechanism, scope or test |
| R-08 | FM-13 | Semantic duplication beyond the canonical block is not detected | INV-06 boundary checker; CI equivalence of the block | Medium | Medium | Maintainer | **NOT ACCEPTED** — partially mitigated | A DEV concept appears in the payload outside the sanctioned block |
| R-09 | FM-09 / D-0.3-23 | Legacy status/finding inconsistencies are recorded, not corrected in place; closed-plan edit authority unresolved | Post-close records; INDEX correction; checker extensions | Medium | Medium | Maintainer | **NOT ACCEPTED** — recorded; D-0.3-23 escalated | A legacy closed plan is cited as authoritative for a new decision |
| R-10 | FM-06 | Hook is opt-in; fail-open without hooks | RFC-84 LIMIT; hook in adopted project | Medium | Medium | Maintainer | **ACCEPTED** — RFC-84 `Accepted`, 2026-10-20 | A session without hooks mutates the payload |
| R-11 | FM-15 | No persisted current state; no transition validation | ADR-21 design decision; gate records | Medium | High | Maintainer | **ACCEPTED** — ADR-21 `Accepted`, 2026-10-20 | A state transition is claimed valid without a persisted source state |

**Counts:** 11 risks: **2 accepted** (R-10, R-11), **9 not accepted** (R-01…R-09). No risk is marked “accepted” without the cited act.

---

## F. Implementation contract

### F.1 IN SCOPE

1. Correct `docs/INVARIANTS.md` local interpretation of INV-07, add `ENFORCED:session-hook` to its vocabulary, and reconcile its gap-status statement. **Do not touch the canonical block or the Protocol copy.**
2. Correct the `docs/plans/INDEX.md` Plan 169 row to `Executed`; create a post-close record that records the factual inconsistency in Plans 157/158 (body declares `Closed`; `Status` says `Aprobado para ejecución`) and the derived state declared by the body, **without deciding D-0.3-23**, plus the four `Closed` plans with findings in state `open` (155, 158, 168, 169). **Do not edit closed plans.**
3. Extend `tools/check_plan_structure.py` to compare the plan header's base `**Status:**` with the base status in its `docs/plans/INDEX.md` row. Plans 157/158 are reported as **`GAP` (declared legacy)**, not `ANOMALY`; every other numbered plan must match, and Plan 169 is corrected first.
4. Extend `tools/check_lifecycle_lineage.py` to report **`ANOMALY`** when a plan contains a `## Checkpoint / cierre` record declaring `Condición derivada: **Closed**` (or equivalent `Closed` declaration) and a finding entry whose state is `open`. Plans 155/158/168/169 are reported as **`GAP` (declared legacy)**, not `ANOMALY`; all other plans follow the rule.
5. Extend `tools/check_invariants_equivalence.py` (or an associated test) to parse the `ENFORCEMENT_STATUS` column of the canonical block and the local vocabulary table in `docs/INVARIANTS.md`: every `ENFORCED:*` label used must be defined in the table, and the declared count `7/15 ENFORCED · 2/15 VALIDATED · 6/15 NONE` must match the block. A missing label or count mismatch is a failure.
6. Add `check_invariants_equivalence.py` to `.github/workflows/check-protocol.yml`.
7. Add the tests for 3–5, including a negative equivalence case.
8. Do **not** create a parallel non-guarantee document: this artifact is the canonical statement. If a Policy clarification is chosen, it must be bounded to a reference to this artifact and must not change the guarantees.
9. Produce the evidence in §I.

### F.2 OUT OF SCOPE

- Any change to `protocol/.agents/`, `protocol/_AGENTS.md`, `runtime/`, `dist/`.
- Any new invariant, property, gate, lifecycle state, registry, namespace or authority.
- Any positive guarantee of semantic or epistemic truth.
- Any stronger historical-integrity guarantee (D-0.3-12).
- Any in-place edit of a closed plan/RFC/ADR (D-0.3-23).
- G-07 deletion detection (D-0.3-13).
- G-06 transition validation (D-0.3-14).
- Context recovery / DEV Memory (D-0.3-16).
- General documentation synchronization (D-0.3-18).
- Plan completeness (Priority 5), Understanding/Reflection (Priority 11), release/publication authority (Priority 10).

### F.3 REQUIRED CHANGES

| Artifact | Change | Authority |
|---|---|---|
| `docs/INVARIANTS.md` | INV-07 interpretation; `session-hook` vocabulary; gap-status reconciliation | Class B plan + post-close reference to Plan 170 |
| `docs/plans/INDEX.md` | Plan 169 row: `Aprobado para ejecución` → `Executed` | Class B plan (INDEX is descriptive) |
| New post-close record (in the implementing plan) | Factual inconsistency of 157/158 (no D-0.3-23 decision) and 155/158/168/169 findings | Class B plan |
| `tools/check_plan_structure.py` | Status/INDEX rule + legacy set | Class B plan (tooling) |
| `tools/check_lifecycle_lineage.py` | `Closed` + `open` finding rule + legacy set | Class B plan (tooling) |
| `tools/check_invariants_equivalence.py` | Vocabulary/count check | Class B plan (tooling) |
| `.github/workflows/check-protocol.yml` | Equivalence checker step | Class B plan (CI) |
| `tests/test_check_plan_structure.py` | Status/INDEX fixture | Class B plan (tests) |
| `tests/test_check_lifecycle_lineage.py` | `Closed` + `open` fixture | Class B plan (tests) |
| `tests/test_check_invariants_equivalence.py` | Vocabulary/count + negative fixture | Class B plan (tests) |
| `CHANGELOG.md` | **Only** the `[Unreleased]` entry `(plan N)`; N-9 guard | Docs-only closure (RFC-69) |

### F.4 FORBIDDEN CHANGES

- Any edit to `protocol/.agents/`, `protocol/_AGENTS.md`, `runtime/` or `dist/`.
- Any new invariant/property/gate/state/registry/namespace.
- Any rewrite of governing content of a closed plan/RFC/ADR.
- Any change to the canonical invariants block or the Protocol copy.
- Any positive semantic/epistemic guarantee.
- Any edit of `PRIORITY.md` or the pre-existing untracked planning document.
- Any change to a historical `CHANGELOG.md` release: modification, reordering, duplication, insertion, deletion or mass reformatting; any hunk outside `[Unreleased]` (N-9).
- Any `git add -A` or bulk staging that includes unrelated files.
- Any commit of `.project/` artifacts.

### F.5 DEPENDENCIES

- RFC-84 `Accepted`; ADR-20 `Accepted`; ADR-21 `Accepted`; Plan 170 `Executed`/`Closed` (`PC-2`).
- A Class B plan `Aprobado para ejecución` (not yet exercised).
- No dependency on D-0.3-12, D-0.3-23, G-07, G-06, Priority 5/11/14/10.
- No dependency on the untracked user files.

### F.6 AUTHORITY REQUIREMENTS

- **Maintainer:** approval of the Class B plan; any decision to adopt D-0.3-12 or D-0.3-23; acceptance of any risk not already accepted by RFC-84/ADR-21.
- **Agent:** execute the approved plan; no authority to accept risks, edit closed history, change the payload or add invariants.
- **RFC:** none for §F; RFC-56 does not apply because there is no payload effect.

### F.7 Acceptance criteria

See §G. The contract is satisfied only if all AC-1…AC-11 pass.

### F.8 Negative acceptance criteria

See §H. The contract fails if any N-1…N-9 occurs.

### F.9 Verification commands

See §I.

### F.10 Expected evidence

Anchor + checkpoint with closure-state identity; outputs of the seven repository checkers; both `pytest` legs; C-1/C-2/C-3; `git diff --name-only` within scope; no diff under `protocol/`, `runtime/`, `dist/`; the N-9 CHANGELOG guard.

### F.11 Completion condition

See §J.

---

## G. Acceptance criteria

| AC | Criterion | Verification |
|---|---|---|
| AC-1 | `docs/INVARIANTS.md` uses no undefined `ENFORCED:*` label; INV-07 matches the block and the adopted-project hook; the gap list distinguishes implemented/rejected/pending | Test/checker + reading against `hook_gate.py`, RFC-84, ADR-21 |
| AC-2 | `check_invariants_equivalence.py` runs in CI and fails when one copy diverges | Workflow + negative test |
| AC-3 | `check_plan_structure.py` detects status/INDEX divergence; Plan 169 row is `Executed`; 157/158 are declared legacy | Fixture + `git diff` |
| AC-4 | `check_lifecycle_lineage.py` detects `open` in a plan declaring `Closed`; the four legacy cases are recorded | Fixture + post-close record |
| AC-5 | This artifact is the canonical 0.3 artifact; the proposals INDEX points to it; no **new** broken citations (the pre-existing 26 + 1 baseline is unchanged) | `check_plan_citations` baseline + diff |
| AC-6 | 0 changes under `protocol/.agents/`, `protocol/_AGENTS.md`, `dist/`, `runtime/` | `git diff --name-only` |
| AC-7 | 0 new invariants/properties; canonical block byte-identical | `check_invariants_equivalence.py` + diff |
| AC-8 | The artifact states the non-guarantees and `Closed` procedural | Reading of §A/§K |
| AC-9 | Validation battery executed with the taxonomy of §I: seven repository checkers (six pass + `check_plan_citations` baseline), both `pytest` legs, and C-1/C-2/C-3 with `ANOMALY=0`; anchor/checkpoint | Recorded outputs |
| AC-10 | A reader can implement §F without re-deriving the failure model or decision states | Checklist §C.1 + review |
| AC-11 | `CHANGELOG.md` is modified only inside `[Unreleased]`; no historical release is modified, reordered, duplicated, inserted or reformatted; the historical heading sequence is unchanged | `git diff -U0 -- CHANGELOG.md` + the N-9 guard in §I |

---

## H. Negative acceptance criteria

| N | Must NOT happen |
|---|---|
| N-1 | Any change under `protocol/.agents/`, `protocol/_AGENTS.md`, `runtime/` or `dist/` |
| N-2 | Any new invariant, property, gate, lifecycle state, registry or namespace |
| N-3 | Any edit to the canonical invariants block or the Protocol copy |
| N-4 | Any rewrite of governing content of a closed plan/RFC/ADR |
| N-5 | Any positive semantic/epistemic guarantee |
| N-6 | Any `EXPLICITLY ACCEPTED AS RESIDUAL RISK` without a cited authority act |
| N-7 | Any `AUTHORIZED FOR IMPLEMENTATION` without an approved Class B plan |
| N-8 | Any `git add -A` / bulk staging; any commit of `.project/` or the untracked user files |
| N-9 | Any modification of `CHANGELOG.md` outside the intentional `[Unreleased]` entry; no historical release may be modified, reordered, duplicated, inserted, deleted or reformatted |

---

## I. Verification

### I.1 Validation taxonomy (no ambiguous "checkers")

The prior wording "six of seven checkers pass" counted only the **repository checkers** of the canonical battery. To remove the ambiguity, the categories are:

| Category | Exact members | What it proves | What it does not prove |
|---|---|---|---|
| **Repository checkers (7)** | `check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `check_invariants_equivalence` | Structural/documentary invariants of the repository | Semantic truth, completeness or correctness of a decision |
| **Lifecycle checks (3)** | C-1 `check_lifecycle_anchor`, C-2 `check_lifecycle_checkpoint`, C-3 `check_lifecycle_lineage` | Presence/form/consistency of anchors, checkpoints and findings lineage | Truth of the validated content; C-2 does not require the declared closure state to equal the closing commit tree |
| **Tests (2 legs)** | `pytest tests/`; `pytest protocol/.agents/harness/tests/` | Behaviour specified by the tests | Properties not covered by a test; semantic truth |
| **Auxiliary** | `git diff --check`, `git diff --name-only`, `git status --porcelain=v2 --branch`, `git diff -U0 -- CHANGELOG.md` | Diff cleanliness, scope containment and CHANGELOG immutability | Correctness of the content |

Therefore, **"six of seven repository checkers pass"** means: of the seven repository checkers, six exit 0 and `check_plan_citations` keeps its pre-existing baseline (26 broken historical citations + 1 legacy reference). It does **not** count C-1/C-2/C-3, the two `pytest` legs or the auxiliary commands. Those are reported separately.

### I.2 Exact commands

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_invariants_equivalence.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_lineage.py
python tools/check_lifecycle_checkpoint.py
git diff --check
git diff --name-only <baseline>..HEAD
git status --porcelain=v2 --branch
```

Expected results for the implementation Change:

- Six of the seven **repository checkers** pass; `check_plan_citations.py` keeps its pre-existing baseline (26 broken historical citations + 1 legacy reference) and must not increase it.
- Both `pytest` legs pass (or a declared environmental GAP if the execution environment changes; never a false PASS).
- C-1/C-2/C-3: `ANOMALY=0`; legacy `GAP`s declared.
- `git diff --name-only` contains only the §F.3 artifacts.
- No diff under `protocol/.agents/`, `runtime/`, `dist/`.
- N-9 passes: `CHANGELOG.md` has no hunk outside `[Unreleased]` and its historical heading sequence is unchanged.

### I.3 N-9 objective CHANGELOG check

The check is a diff guard, not a visual review. Reference algorithm (run with the repository's Python, from the repository root):

```text
1. Read CHANGELOG.md at HEAD and in the working tree.
2. In each version, locate the `## [Unreleased]` heading and the next `## [` heading.
   Allowed region = lines strictly after `## [Unreleased]` and before the next `## [`.
3. Parse `git diff -U0 -- CHANGELOG.md`.
   For every hunk `@@ -a,b +c,d @@`, require:
     - every old line in [a, a+b) is inside the old allowed region; and
     - every new line in [c, c+d) is inside the new allowed region.
4. Compare the ordered list of `## [` headings, excluding `## [Unreleased]`,
   between HEAD and the working tree. It MUST be identical.
5. If any hunk falls outside the allowed region, or the historical heading list
   differs, the check is FAIL (N-9).
```

The implementing plan must include an executable reference script for this algorithm and record its output as evidence. The check is **not** a new repository checker or gate: it is a validation command of the Change.

For this closure session, no `CHANGELOG.md` change was made, so N-9 is not exercised here; it is exercised by the implementation Change.

For this closure session, the executed results are in §M.

---

## J. Completion condition

Priority 0.3 implementation is **COMPLETE** when **all** of the following are observably true:

```text
[ ] The implementing Plan is `Executed` and its `Closed` condition is derived with a Validation Anchor, a Checkpoint and PASS evidence.
[ ] AC-1…AC-11 pass, including the checker outputs and both test legs.
[ ] `docs/INVARIANTS.md` has no undefined `ENFORCED:*` label and its INV-07 interpretation matches the block and the adopted-project hook.
[ ] `docs/plans/INDEX.md` Plan 169 row is `Executed`; the post-close record covers 157/158 and the four legacy finding cases.
[ ] `check_plan_structure.py`, `check_lifecycle_lineage.py` and `check_invariants_equivalence.py` include the new rules and tests.
[ ] `check_invariants_equivalence.py` runs in CI and the negative test fails on divergence.
[ ] `CHANGELOG.md` satisfies N-9: only the `[Unreleased]` entry changed; historical headings and releases are unchanged.
[ ] No change exists under `protocol/.agents/`, `protocol/_AGENTS.md`, `runtime/` or `dist/`.
[ ] No new invariant, property, gate, state, registry or namespace exists.
[ ] The implementation commit (or closure state) is on `dev`; `Closed` is derived only with the checkpoint and PASS evidence.
```

If any item is false, 0.3 implementation is **not complete**.

---

## K. Explicit exclusions

Priority 0.3 does **not** attempt to:

- prove that an interpretation is correct;
- prove that a plan is complete relative to reality;
- prove that evidence entails truth;
- prove that a decision is objectively correct;
- prove that persistent knowledge is true;
- protect closed history from corruption beyond Git recovery (D-0.3-12);
- detect deletion of governance records (D-0.3-13);
- validate state transitions (D-0.3-14);
- enforce payload immutability without hooks (D-0.3-15);
- recover session context or build DEV Memory (D-0.3-16);
- synchronize documentation automatically (D-0.3-18);
- detect a wrong objective chosen under correct authority/scope (D-0.3-21);
- detect general semantic duplication or conceptual equivalence DEV→Protocol beyond the structural boundary references and the byte-identical canonical block (FM-13);
- edit closed plans in place (D-0.3-23);
- create a global registry, claims ledger or failure registry;
- replace human authority with inference.

---

## L. Superseded material and canonical location

- **Canonical artifact:** this file.
- **Superseded revision:** the 2026-10-20 revision committed at `8e30d4f` (`docs(priority-0.3): close the failure-model diagnosis and implementation contract`). It remains in Git history; it is not rewritten. Its decision states that conflict with §C.1 are superseded: the 22-decision/3-escalation count; `EXPLICITLY ACCEPTED AS RESIDUAL RISK` for D-0.3-17 and D-0.3-21; E-0.3-2 as an escalation; E-0.3-3 as both escalation and deferral.
- **No other 0.3 artifact exists.** The proposals INDEX points to this file.
- **Historical evidence preserved:** the failure-model details, the 0.1 audit evidence, the CHANGELOG incident, the 0.2 closure records and the closed plans are referenced, not rewritten.

---

## M. Evidence, baseline and validation

### M.1 Baseline and prior state

- Branch `dev`; starting HEAD `8e30d4f` (prior 0.3 revision); upstream `origin/dev`.
- Worktree at session start: clean except `PRIORITY.md` and `docs/planificacion-argentos-diseno-2026-10-13.md`, both untracked and preserved.
- Priority 0.2: RFC-84 `Accepted`; ADR-20/21 `Accepted`; Plan 170 `Executed`/`Closed`; both invariant representations materialized; `DESIGN COMPLETE = YES`, `IMPLEMENTATION COMPLETE = NO` (gaps deferred). Subsequent closures: E1-G1/G-09 (`16224ce`), G-05 (`77c49bb`, `05f60a2`), G-03/G-06 rejected (ADR-21), fixture repair (`b7e1b29`).

### M.2 Facts from this closure session

- `docs/INVARIANTS.md:24` and `protocol/.agents/standards/INVARIANTS.md:25` declare `INV-07 = ENFORCED:session-hook`; `docs/INVARIANTS.md:79` says «Mecanismo: **ninguno**»; `docs/INVARIANTS.md:39-47` does not define `session-hook`.
- `check_invariants_equivalence.py`: `IDENTICAL: YES`, `PASS`.
- 3 status/INDEX mismatches: 157, 158, 169.
- 4 `Closed` plans with findings in state `open`: 155, 158, 168, 169; Plan 152 is `Executed`, not `Closed`.
- `CHANGELOG.md` incident: `ce91a37` removed 33 duplicated entries introduced by `f75d70a`; six checkers were green at the time.
- RFC-84 withdrew the A/B/C audit citations because those artifacts do not exist and are not recoverable (`docs/rfc/84…:8,180`).
- `81bbde1` and the remote publication of `12.1.0` are recorded as facts, not as authorized acts (`<PLAN-169>:F-1`; `AUDITORIA_FASE_0_0_1…:§3.7`).

### M.3 Executed validation for this closure

The counts use the taxonomy of §I.1: **repository checkers** are the seven commands of `docs/VERSIONING.md` §4.1; lifecycle checks (C-1/C-2/C-3) and the two `pytest` legs are reported separately and are not part of the "seven".

| Command | Result |
|---|---|
| `python tools/check_protocol_invariants.py --payload protocol .` | `217 files checked, 10537 references verified`, exit 0 |
| `python tools/check_plan_structure.py` | all numbered documents conform, exit 0 |
| `python tools/check_taxonomy_coherence.py` | `Taxonomy coherence OK`, exit 0 |
| `python tools/check_session_artifacts.py` | `Session artifacts OK`, exit 0 |
| `python tools/check_version_state.py` | `Version state OK`, exit 0; warning `changelog section [3.9.0] has no tag` is expected on `dev` before promotion |
| `python tools/check_invariants_equivalence.py` | `IDENTICAL: YES`, `PASS`, exit 0 |
| `python tools/check_plan_citations.py` | 26 broken historical citations + 1 legacy reference, exit 1 (pre-existing baseline, unchanged) |
| `python tools/check_lifecycle_anchor.py` | `VALID=76`, `GAP=0`, `ANOMALY=0` |
| `python tools/check_lifecycle_lineage.py` | `VALID=41`, `GAP=0`, `BOUNDARY=1`, `ANOMALY=0` |
| `python tools/check_lifecycle_checkpoint.py` | `VALID=75`, `GAP=1` (legacy plan 116), `ANOMALY=0` |
| `python -m pytest tests/` | **1371 passed** (314.75 s) |
| `python -m pytest protocol/.agents/harness/tests/` | **204 passed, 1 skipped** (10.06 s) |
| `git diff --check` | clean |

The `pytest` legs were executable in this session under the `danger-full-access` file policy; the historical `tmp_path` limitation declared by earlier plans did not apply and is not invalidated.

---

## N. What this document does not do

- It does not implement any correction.
- It does not modify `docs/INVARIANTS.md`, `docs/plans/INDEX.md`, the checkers, CI, `protocol/`, `runtime/` or `dist/`.
- It does not add invariants, properties, gates, states, registries or authority.
- It does not reopen Priority 0.2 or rewrite its closed artifacts.
- It does not resolve D-0.3-12 or D-0.3-23.
- It does not accept any residual risk not already accepted by RFC-84 or ADR-21.
- It does not declare a positive semantic or epistemic guarantee.

**End of the canonical Priority 0.3 artifact.** The next step is a Class B Plan `Aprobado para ejecución` that implements §F and satisfies §G–§J; no further 0.3 diagnosis is required.
