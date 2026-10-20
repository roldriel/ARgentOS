# Revisión adversarial — Especificación §0.1: auditoría de superficies y mínima intervención

> **Pregunta rectora.**
> ¿Cuál es la **intervención mínima** que hace que un tercero pueda confiar en que las afirmaciones relevantes de ARgentOS no exceden la evidencia disponible?

**Naturaleza documental:** Working / adversarial review — **no normativo**; puede ser provenance, nunca autoridad.
**Fecha:** 2026-10-14
**Revisa a:** `docs/working/proposals/ESPECIFICACION_CLASE_DE_AFIRMACION_Y_ANTI_PROMOCION_2026-10-14.md` (en adelante **v1**)
**Origen:** `PRIORITY.md:0.1. Contrato de verdad de ARgentOS` + segunda opinión adversarial del mantenedor (2026-10-14)
**Estado:** `REVISIÓN` — 0 cambios estructurales; la auditoría que especifica **no fue ejecutada**.
**Autoridad:** ninguna. Este documento no decide, no autoriza, no crea trabajo y no modifica ningún artefacto objetivo.
**Postura declarada:** este documento es adversarial **contra la v1**. No la defiende; la reduce.

---

## 0. Veredicto de la revisión

**La v1 se adelantó a la evidencia.** Diseñó infraestructura conceptual —una regla, una tabla de traducción de tres ejes, una gramática inline, tres entradas de glosario y tres cambios de payload— sobre hallazgos que **nunca fueron dimensionados** y que, re-examinados adversarialmente, **confunden especificación con sobre-afirmación** (§2.5).

El problema que §0.1 describe es real en su formulación general. **Su magnitud actual es desconocida**, y ese desconocimiento es el único hallazgo que hoy justifica trabajo.

### 0.1 Disposición de los entregables de la v1

| v1 | Disposición | Razón |
|---|---|---|
| E-1 regla transversal | **Condicional** — se reduce de 6 reglas a **1 regla posible**, y sólo si la auditoría devuelve `MINIMAL_RULE` o `MODEL_REQUIRED` | No hay problema demostrado que la requiera |
| E-2 tabla de traducción de 3 ejes | **Eliminado del alcance** | Canoniza vocabulario para un problema no medido, y depende del vocabulario de dominio no canonizado (H-7) |
| E-3 forma calificada inline | **Condicional**, subordinado a E-1 | Es la materialización de E-1; sin E-1 no existe |
| E-4 tres entradas de glosario | **Diferido** (secundario) | Su justificación era circular: los términos faltan, pero sólo importan si la solución los necesita |
| E-5 `GAP` de cinco términos | **Diferido** (secundario) | Ídem |
| E-6 marca de aspiración en el Destino | **Condicional** — sólo si la auditoría encuentra un caso `ASPIRATION-AS-FACT` en esa superficie | Sin caso, no hay corrección que hacer |
| E-7a/b/c cambios de payload | **Diferido** — y su premisa H-1 debe sobrevivir primero al test de §3.3 | RFC-56 Clase A para un problema no demostrado |
| Los tres ejes `naturaleza/alcance/soporte` | **Hipótesis de diseño no adoptada** (§6.2) | El eje `alcance` depende de un vocabulario sin autoridad general resuelta (H-7) |

### 0.2 Correcciones a mis propios hallazgos

Una revisión adversarial que no corrige sus propios hallazgos no es adversarial.

| Hallazgo v1 | Estado tras la revisión |
|---|---|
| **H-1** entry points sin marca | **Debilitado como defecto.** `protocol/_AGENTS.md:8,43` y `protocol/.agents/INDEX.md:21,25–29` son mayormente **especificaciones** —qué debe hacer el agente—, no afirmaciones de hecho. Una especificación no se falsifica por incumplimiento: se **viola** y se registra como violación. Sobrevive sólo la parte que un lector pueda interpretar como garantía, y **eso debe determinarse caso por caso en la auditoría, no asumirse en bloque**. |
| **H-2** `status: planned` retirado | **Sobrevive como restricción, no como problema.** Es un antecedente que encarece cualquier propuesta de marcador de estado; no es un defecto del estado actual. |
| **H-3** «verified» con 4 acepciones | **Sobrevive, pero hoy no es accionable.** Es ambigüedad de vocabulario: sólo importa si la solución necesita el término. Si la intervención mínima es corregir frases, H-3 es irrelevante. |
| **H-4** verificadores DEV-only en el catálogo de garantías | **Candidato, no defecto confirmado.** La tabla **no es falsa**: declara quién verifica. Es un problema de **accionabilidad para el adoptante**, no de sobre-afirmación. Debe pasar el test de §3.4. |
| **H-5** IDs `G-`/`ENF-` sin registro distribuido | **Higiene menor.** La sustancia está inline; probablemente no material (sin consecuencia para el lector). |
| **H-6** términos sin definición normativa | **Se degrada a circular.** Sólo es problema si la solución necesita los términos. Diferido por principio 9. |
| **H-7** vocabulario de dominio no canonizado | **Sobrevive como bloqueo duro.** Ningún eje `alcance` puede ser dependencia de la solución. |
| **H-8** límites honestos declarados en el payload | **Sobrevive y juega CONTRA la premisa de §0.1.** El payload declara sus límites con precisión (`harness/INDEX.md:16`, `:27`, `:31–34`, `:415`). Es evidencia de que la disciplina que §0.1 pide **ya existe en la capa Protocol**. La pregunta de la auditoría es si existe en la capa DEV y en las superficies de lectura. |

### 0.3 Prior registrado (antes de la auditoría)

Declarado ahora para impedir racionalización posterior:

| Resultado posible | Probabilidad que asigno hoy |
|---|---|
| `CORRECT_EXISTING_CLAIMS` | 40 % |
| `NO_STRUCTURAL_CHANGE` | 35 % |
| `MINIMAL_RULE` | 20 % |
| `MODEL_REQUIRED` | 5 % |

**Y una condición explícita:** si la auditoría devuelve `MODEL_REQUIRED`, **la v1 no se reinstaura automáticamente**. Exigiría su propia re-derivación desde la evidencia nueva, porque fue construida para un problema distinto del que la evidencia haya podido mostrar.

---

## 1. El problema, separado de la solución

### 1.1 Qué pide §0.1

`PRIORITY.md:23–37` pide identificar las afirmaciones fundamentales de ARgentOS, clasificarlas por naturaleza (7 categorías) y poder determinar qué evidencia respalda cada una, **para evitar que documentación, diseño o lenguaje conceptual presenten como hechos capacidades no demostradas**.

### 1.2 Reformulación del objetivo

> **Evitar la sobre-afirmación y establecer la verdad observable de ARgentOS.**

Es lo que §0.1 persigue. Todo lo demás en §0.1 —categorías, clasificación, inventario— es **medios propuestos**, no el objetivo.

### 1.3 Qué NO es el objetivo

Taxonomías, ejes, registros, inventarios, gramáticas de marcado, entradas de glosario y checkers son **medios potenciales**. Ninguno es el objetivo. Ninguno está justificado hasta que exista un problema demostrado que lo requiera, y cada uno tiene coste: obliga a decidir una clase, crea vocabulario que compite con el existente (`protocol/.agents/standards/quality/EVIDENCE.md`, `CONFIDENCE.md`, `MEMORY_SYSTEM.md`), y envejece.

### 1.4 Instrumento de la auditoría (provisional, no vocabulario)

Para poder **contar** casos hace falta un test que decida qué cuenta. Se define aquí, se declara **desechable** y **no se propone** como vocabulario:

Una afirmación `S` de una superficie de lectura es **materialmente sobre-afirmada** si se cumplen las tres condiciones:

1. **Lectura de hecho.** `S` se lee como afirmación sobre lo que ARgentOS **hace, garantiza o ya logró** — no como una regla que el protocolo impone al agente.
2. **Soporte no alcanzable.** El soporte de `S` no es alcanzable desde la misma superficie (sin cita, test, checker o anchor localizable).
3. **Consecuencia.** Una creencia falsa del lector tiene consecuencia (adoptar, confiar, invertir, no verificar).

**La condición 3 es la que hace material.** Sin ella no hay defecto: hay una imprecisión de redacción.

Etiquetas locales, **sólo para clasificar durante la auditoría**:

| Etiqueta | Significado | ¿Defecto? |
|---|---|---|
| `SPEC` | requisito del sistema (MUST / enunciado normativo) | **No.** Un requisito no se falsifica por incumplimiento |
| `CLAIM-SUPPORTED` | afirmación de hecho con soporte alcanzable | No |
| `CLAIM-UNSUPPORTED` | afirmación de hecho sin soporte alcanzable | **Candidato** |
| `CLAIM-CONDITIONAL-UNMARKED` | verdadera sólo bajo una condición no declarada en la superficie | **Candidato** |
| `ASPIRATION-AS-FACT` | dirección presentada como logro | **Candidato** |

Estas etiquetas se descartan al cerrar la auditoría. No se registran, no se canonizan, no se citan después.

---

## 2. La evidencia: qué sabemos y qué no

### 2.1 Lo que sabemos que está mal **hoy**

**Nada confirmado.** Ninguna afirmación ha sido verificada como materialmente sobre-afirmada y abierta a la fecha de esta revisión.

Los dos casos conocidos son de naturaleza distinta:

1. **Corregido.** «Zero hallucinations» se presentaba como garantía y era una aspiración (`docs/working/audits/AUDITORIA_SISTEMA_2026-08-16.md:382`). Fue **corregido** en 2026-08 por redefinición operacional (`protocol/.agents/harness/INDEX.md:164`). No es un caso abierto.
2. **Reportado, no verificado, y de otra clase.** La afirmación «Trabajo activo: ninguno» de `ROADMAP.md` mientras el Plan 165 estaba aprobado, registrada en `docs/planificacion-argentos-diseno-2026-10-13.md:1298`. Es (a) una afirmación de **estado**, no de capacidad, y (b) reportada por un documento **no trackeado y sin verificación independiente**. `ROADMAP.md:35` hoy dice «Trabajo activo: ninguno» junto a «Último trabajo cerrado: la release 12.1.0 (plan 168)» — posiblemente correcto hoy.

**Esta sección vacía es el hallazgo más importante de la revisión.** Significa que la carga de la prueba está enteramente en la auditoría, y que toda la v1 fue diseñada sin ella.

### 2.2 Lo que puede fallar **en el futuro**

| # | Riesgo | Base |
|---|---|---|
| R-1 | Un artefacto de dirección o estado presenta como logrado algo que es destino | §2.1 caso 1, ya ocurrido una vez |
| R-2 | Un agente nuevo lee una condición de borde (modo declarativo, single-instance, H09/H10 no integrados) como garantía incondicional | H-1 + H-8, **hipótesis de lectura, no observación** |
| R-3 | Un adoptante no puede ejecutar la verificación que el catálogo de garantías declara | H-4 |
| R-4 | La corrección de un caso se pierde porque nada la vuelve a comprobar | H-2 (precedente de retiro sin reemplazo) |

### 2.3 Lo que creemos que podría prevenirlo

Hipótesis, **no** conclusiones: una regla documental de marcado; corregir las frases concretas; anotar condiciones de borde en el punto de lectura; un checker. **Ninguna está respaldada por evidencia todavía.**

### 2.4 Lo que todavía no sabemos

1. **Cuántas afirmaciones materialmente sobre-afirmadas existen hoy.** Cero medido.
2. **Si son un patrón o casos aislados.** Sin esto, elegir entre corregir y diseñar es adivinar.
3. **Si las superficies de lectura son peores que las superficies que el propio repo declara no normativas** (ver §3.1 control).
4. **Si la regla propuesta en E-1 es redundante** con mecanismos existentes (§4, F-4 ampliada).
5. **Si H-1 sobrevive** al test de especificación vs afirmación (§3.3).
6. **Si las condiciones de borde del payload son alcanzables** por un lector que sólo lee el entry point (H-8).

**Estas seis preguntas son el objeto de la Fase 0. Nada más.**

### 2.5 Re-evaluación adversarial del inventario H-1…H-8

Resumen de §0.2: de ocho hallazgos, **sólo dos sobreviven intactos** (H-4 como candidato, H-7 como bloqueo). **Uno juega en contra de la premisa de §0.1** (H-8). **Uno se degrada a circular** (H-6). Los demás se debilitan o se reclasifican. El inventario de la v1 fue construido para sostener un diseño, y eso se nota al re-examinarlo.

---

## 3. La verificación decisiva: auditoría de superficies de lectura (F-3)

**F-3 se eleva a primera verificación decisiva.** Ninguna intervención se aprueba antes de su resultado.

### 3.1 Superficies incluidas

Criterio de inclusión: **aquellas donde un lector forma su expectativa sobre qué hace ARgentOS**, más un grupo de control.

| # | Superficie | Por qué | Cobertura |
|---|---|---|---|
| S1 | `AGENTS.md` (raíz) | lo primero que lee todo agente en este repositorio | completa |
| S2 | `.agents/AGENTS.md`, `.agents/policies/*`, `.agents/workflows/*` (7 archivos) | capa operacional DEV; describe cómo trabaja el sistema | completa |
| S3 | `README.md` | primera exposición humana | completa |
| S4 | `ROADMAP.md` | dirección **y** estado (§2.1 caso 2) | completa |
| S5 | `protocol/_AGENTS.md` | entry point del payload (publicado como `AGENTS.md` en `dist`) | completa |
| S6 | `protocol/.agents/INDEX.md` | bootstrap del payload | completa |
| S7 | `protocol/.agents/harness/INDEX.md` §Guarantee catalog + §Enforcement boundaries | la declaración de capacidades del propio protocolo | completa |
| S8 | `docs/ADOPTION.md` + `docs/MIGRATION.md` | superficie orientada al adoptante | completa |
| S9 | `docs/behavior-patterns.md` | **describe** cómo funciona el sistema: riesgo alto de afirmación de hecho | completa |
| S10 | `protocol/.agents/standards/**` (34 archivos) | superficie normativa del producto | `INDEX.md` + 6 estándares nombrados (EVIDENCE, CONFIDENCE, NO_ASSUMPTIONS, PROTOCOL_HEALTH, PROTOCOL_METRICS, PROTOCOL_BOUNDARIES) completos; resto por muestreo sistemático |
| **C1** | `docs/architecture/*` + `docs/working/**` | **control**: superficies que el propio repo declara históricas o no normativas | muestra |
| **C2** | `CHANGELOG.md` | **control**: registro histórico, sin riesgo de sobre-afirmación esperado | muestra |

**Justificación del control.** Si C1–C2 resultan **más** cuidadosos que S1–S9 en distinguir hecho de aspiración, el diagnóstico cambia: el problema no sería falta de disciplina general, sino una disciplina aplicada sólo donde se declaró no normativo. Eso sería un hallazgo mucho más accionable que «hay sobre-afirmación difusa».

**Excluidas:** `sessions/`, `.project/`, `dist`, `runtime/`, `tools/`, `tests/`. Justificación por superficie en el reporte de la auditoría.

### 3.2 Procedimiento por afirmación

```text
1. EXTRACCIÓN
   Enumerar los enunciados que un lector puede tomar como información sobre el sistema.
   Descartar inmediatamente: títulos, índices, tablas de contenido, metadatos, ejemplos de código.

2. TEST DE §1.4 CONDICIÓN 1 — ¿especificación o afirmación de hecho?
   ¿El enunciado impone una obligación al agente/protocolo, o afirma algo del sistema?
   Obligación  → SPEC        → FIN (no es defecto)
   Afirmación  → paso 3

3. TEST DE §1.4 CONDICIÓN 2 — ¿el soporte es alcanzable desde esta superficie?
   ¿Hay cita, test, checker, anchor o comando localizable en la propia superficie o a un salto?
   Sí          → CLAIM-SUPPORTED → FIN
   No          → paso 4

4. TEST DE VERDAD
   Verificar el enunciado contra el estado real del repositorio.
   Verdadero incondicional  → FIN (anotar como soporte ausente pero no material)
   Verdadero condicional    → CLAIM-CONDITIONAL-UNMARKED
   Falso                    → CLAIM-UNSUPPORTED
   Dirección como logro     → ASPIRATION-AS-FACT

5. TEST DE §1.4 CONDICIÓN 3 — materialidad
   ¿Una creencia falsa del lector tiene consecuencia? Describir la consecuencia.
   Sin consecuencia  → FIN (registrar como observación, no como defecto)
   Con consecuencia  → DEFECTO MATERIAL
```

### 3.3 Corrección a H-1: especificación ≠ afirmación

El paso 2 es el que la v1 no hizo. `protocol/_AGENTS.md:43` («The agent will not execute based on unconfirmed assumptions») es una **regla**; que un agente la incumpla es una violación, no una prueba de que la frase mienta. `protocol/.agents/INDEX.md:21` («will delegate each workflow phase to a worker invoked as a subagent») es una **especificación de arquitectura**; el modo single-instance es una **condición de borde declarada en otro artefacto**, y la pregunta legítima es si el lector del entry point puede alcanzarla (pregunta 6 de §2.4), no si la frase es falsa.

**Sin esta corrección, la auditoría habría contado como defectos docenas de especificaciones legítimas** y habría fabricado la justificación de E-1. Es el error más grave de la v1.

### 3.4 Criterio de materialidad — casos límite resueltos de antemano

| Caso | Veredicto pre-registrado |
|---|---|
| Enunciado normativo que el sistema no enforcea (modo declarativo) | `SPEC` **si** declara o hereda la advertencia de modo declarativo; `CLAIM-CONDITIONAL-UNMARKED` si el lector del punto de lectura no puede saberlo |
| Tabla que nombra un verificador que el lector no puede ejecutar (H-4) | material **sólo si** el lector adopta una expectativa de verificación disponible. Si la tabla dice «dev tool», no hay afirmación falsa |
| ID citado sin registro distribuido (H-5) | **no material** salvo que la sustancia del invariante no esté inline |
| Enunciado en futuro («will delegate», «will not execute») | `SPEC` por defecto; `CLAIM-CONDITIONAL-UNMARKED` sólo si describe una capacidad del sistema, no una obligación de conducta |
| Descripción en `behavior-patterns.md` que no coincide con el código | **material** — es una afirmación de hecho por definición |

### 3.5 Salida de la auditoría

1. Tabla de defectos materiales: `superficie | enunciado (cita) | etiqueta | consecuencia | corrección propuesta`.
2. **Conteo** y distribución por superficie.
3. Juicio sobre patrón: aislado / recurrente / compartido.
4. Respuesta a las seis preguntas de §2.4.
5. **Recomendación de intervención** según §3.6.

### 3.6 Regla de decisión pre-registrada

Declarada **antes** de la auditoría, para que el resultado no pueda acomodarse al diseño deseado:

| Resultado de la auditoría | Veredicto |
|---|---|
| 0 defectos materiales | **`NO_STRUCTURAL_CHANGE`** — el problema está suficientemente resuelto; se registra la evidencia y se cierra |
| 1–2 defectos materiales, sin causa común | **`CORRECT_EXISTING_CLAIMS`** — corregir los enunciados; sin regla, sin vocabulario, sin glosario |
| ≥3 defectos materiales **independientes** con **una causa común**, o **recurrencia tras corrección** | **`MINIMAL_RULE`** — una regla documental pequeña, y sólo la que la causa común exija |
| Defectos atribuibles a una **capacidad estructural ausente** (p. ej. ninguna superficie puede expresar verdad condicional) y la corrección por redacción **demostradamente** no lo resuelve | **`MODEL_REQUIRED`** — recién aquí se justifica una taxonomía o mecanismo |

**Base del umbral de recurrencia:** el propio repositorio usa la segunda ocurrencia como señal de que la regla de familia está mal — `docs/placement-contract.md:PC-28`: «A second instance of the same deviation requires its own authorization. An exception is permanent **as a record**, never as a rule. Recurrence of exceptions is evidence that the family rule is wrong». Aplicar el mismo criterio aquí es coherente con la casa.

**Restricción añadida:** `MINIMAL_RULE` autoriza **una** regla. Si la causa común exigiera más de una, el resultado correcto es volver a `MODEL_REQUIRED` con la evidencia, no acumular reglas.

### 3.7 Esfuerzo

**Estimación declarada, no medida:**

| Actividad | Estimación |
|---|---|
| S1–S9, C1–C2 completas | ~11 superficies, ~2.000 líneas de prosa |
| S10: `INDEX.md` + 6 estándares completos, resto muestreado | ~1.500 líneas |
| Enunciados candidatos | ~250–400 |
| Descarte por paso 2 (specification) | esperado > 80 % |
| Casos que llegan al paso 5 | esperado < 20 |
| Coste | una sesión de trabajo acotada; **sin cambios en el repositorio hasta el veredicto** |

### 3.8 Qué invalidaría la auditoría misma

- Que el paso 2 se aplique con criterio laxo y produzca una inflación de candidatos (riesgo principal; mitigado por §3.4).
- Que la extracción dependa de una lectura no reproducible. Mitigación: el reporte cita `ruta:sección` por enunciado.
- Que el juicio de materialidad (paso 5) no pueda ser revisado por un tercero. Mitigación: cada caso declara su consecuencia explícitamente.
- **Que `docs/working/` no esté cubierto por `tools/check_plan_citations.py`** (verificado: `:194–210` recorre sólo `docs/plans/`, `docs/rfc/`, `docs/adr/` y `ROOT_DOCS`). Las citas del reporte de auditoría **no serán verificadas mecánicamente**; su verificación es manual y debe declararse como tal.

---

## 4. Verificaciones F-1 / F-2 / F-4, ampliadas

La v1 tenía F-1 y F-2 y una F-4 de una sola línea. La F-4 se amplía porque la **redundancia es el riesgo más probable** de toda la propuesta: si un mecanismo existente ya cubre el caso, la regla nueva es ruido.

| # | Verificación | Cómo | Si se verifica… |
|---|---|---|---|
| **F-1** | Ya existe un artefacto que enumera y clasifica las afirmaciones de ARgentOS con su evidencia | búsqueda en `docs/`, `protocol/.agents/`, `docs/working/` | la propuesta cae entera |
| **F-2** | El vocabulario de §0.1 ya está definido en algún estándar del payload | lectura completa de `protocol/.agents/standards/**` buscando definiciones de definición / especificación / hipótesis / aspiración | E-2 y E-4 caen |
| **F-4a** | La *claims rule* del payload ya es invocada como norma por algún artefacto DEV | `protocol/.agents/harness/INDEX.md:164`; búsqueda de su invocación en `docs/` y `.agents/` | E-1 es parcialmente redundante |
| **F-4b** | `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md` ya prohíbe tratar lo no confirmado como hecho | lectura del estándar | E-1 puede ser redundante en su parte de «no afirmar sin evidencia» |
| **F-4c** | `protocol/.agents/standards/quality/CONFIDENCE.md` ya tiene regla anti-inflación | lectura del estándar | ídem |
| **F-4d** | `docs/behavior-patterns.md` ya establece «la ausencia de evidencia nunca se convierte en evidencia positiva» | `docs/behavior-patterns.md` | E-1 puede ser redundante en su parte de «no convertir GAP en confirmación» |

**Lectura anticipada, declarada como tal:** si F-4a–F-4d se verifican las cuatro, la parte sustantiva de E-1 **ya existe** en el repositorio, y lo único que faltaría es su aplicación al material DEV. Eso reduciría la intervención a `CORRECT_EXISTING_CLAIMS` incluso si la auditoría encontrara defectos.

---

## 5. Catálogo de intervenciones posibles (ninguna adoptada)

| # | Intervención | Problema demostrado que resolvería | Se activa si | Coste |
|---|---|---|---|---|
| **I-0** | No hacer nada | ninguno | 0 defectos materiales → `NO_STRUCTURAL_CHANGE` | cero |
| **I-1** | Corregir los enunciados concretos | los defectos de la auditoría | 1–2 defectos sin causa común | mínimo; docs-only |
| **I-2** | **Una** regla documental mínima | una causa común recurrente | ≥3 defectos independientes con causa común, o recurrencia | un Plan Clase B; una subsección |
| **I-3** | Ejes / taxonomía de clasificación | incapacidad estructural de expresar la clase de una afirmación | `MODEL_REQUIRED`, con re-derivación | alto; vocabulario nuevo que compite con 8 existentes |
| **I-4** | Cambios de payload | defecto confirmado **en** el payload | `MODEL_REQUIRED` + RFC-56 Clase A `Accepted` | alto |
| **I-5** | Checker | recurrencia tras I-2 | sólo tras 10–15 usos reales de I-2 | alto; congela formato |

**Ninguna se adopta aquí.** El veredicto de §3.6 determina cuál, si alguna.

---

## 6. Qué ocurre con E-1…E-6 y con los tres ejes

### 6.1 Disposición con justificación por hallazgo

La v1 exigía que cada entregable justificara su existencia mediante un hallazgo concreto. Aplicado estrictamente, **casi ninguno lo hace**:

| Entregable v1 | Hallazgo que lo justificaba | ¿Sobrevive? | Disposición |
|---|---|---|---|
| E-1 regla | ninguno propio; se apoyaba en H-1 y en Q4 como objetivo | H-1 debilitado (§3.3) | **Condicional** — 1 regla, sólo con `MINIMAL_RULE` |
| E-2 tres ejes | H-6 (términos sin definir) | circular (§0.2) | **Eliminado** |
| E-3 forma inline | E-1 | depende de E-1 | **Condicional** |
| E-4 glosario | H-6 | circular | **Diferido** |
| E-5 `GAP` de términos | H-6 | circular | **Diferido** |
| E-6 marca en Destino | §2.1 caso 1 (ya corregido) y caso 2 (no verificado) | sin caso abierto | **Condicional** — sólo si la auditoría encuentra el caso |
| E-7a/b/c payload | H-1 (debilitado), H-4 (candidato) | H-1 no pasa el test de §3.3 | **Diferido** |

### 6.2 Los tres ejes: hipótesis de diseño **no adoptada**

`naturaleza / alcance / soporte` se conserva **como hipótesis**, con sus condiciones de refutación explícitas:

| Eje | Hipótesis | Qué la confirmaría | Qué la refuta |
|---|---|---|---|
| `naturaleza` | un lector necesita distinguir definición / especificado / hipótesis / aspiración | que la auditoría encuentre casos donde la ambigüedad de naturaleza **causa** la sobre-afirmación | que los defectos se corrijan reescribiendo sin clasificar |
| `alcance` (`PROTOCOL`/`DEV`/`BOTH`) | la misma afirmación pertenece a dominios distintos | imposible de confirmar hoy | **H-7**: el vocabulario no tiene autoridad general resuelta (definido sólo para el ROADMAP, `docs/CONVENTIONS.md:785`; R-7 en `docs/planificacion-argentos-diseno-2026-10-13.md:1300`). **No puede ser dependencia de la solución** |
| `soporte` | hace falta graduar cuánto sostiene una afirmación | que la auditoría encuentre casos de gradación mal representada | que los 8 valores de V6 y las clases de V2/V3 basten |

**Consecuencia normativa de esta revisión:** los tres ejes **no se escriben en `docs/CONVENTIONS.md`**, no se añaden al glosario y no se usan como estructura de ningún entregable. La v1 proponía lo contrario (§4.2 de la v1).

### 6.3 Por qué E-2 y E-4 se eliminan o difieren aunque parezcan inofensivos

Porque **no son inofensivos**:

1. **E-2 canoniza vocabulario en competencia.** Añadir `naturaleza/alcance/soporte` a un repositorio con **ocho** vocabularios solapados (V1–V8, §2.1 de la v1) aumenta la superficie de incoherencia que `PRIORITY.md:2` quiere auditar. La v1 diagnosticó ese solapamiento y luego propuso un noveno vocabulario.
2. **E-2 introduce una dependencia no autorizada.** El eje `alcance` necesitaría el vocabulario de dominio, que no está canonizado (H-7). La v1 lo reconoció en E-5 y aun así lo usó en E-1, E-2 y E-3.
3. **E-4 es circular.** Los términos faltan, pero sólo importan si la solución los necesita; y la solución no está justificada. Además, crear una entrada de glosario sin autoridad resoluble viola la regla D2 —que es exactamente lo que la v1 dijo que no haría.
4. **El coste no es cero.** Cada entrada de glosario es deuda de mantenimiento y una afirmación más que auditar en el futuro.

---

## 7. Condiciones de falsificación

Conservadas de la v1, revisadas, y ampliadas con las condiciones que harían concluir **menos** trabajo.

### 7.1 Condiciones que invalidan la propuesta (heredadas, revisadas)

| # | Enunciado | Efecto | Estado tras la revisión |
|---|---|---|---|
| F-1 | ya existe un artefacto equivalente | cae la propuesta entera | pendiente |
| F-2 | el vocabulario ya está definido en el payload | caen E-2/E-4 | pendiente |
| **F-3** | **las superficies no sobre-afirman materialmente** | **cae todo salvo `NO_STRUCTURAL_CHANGE`** | **ahora es la verificación decisiva (§3)** |
| F-4a–d | E-1 es redundante con cuatro mecanismos existentes | cae E-1 | pendiente (§4) |
| F-5 | las entradas de E-4 no cumplen el criterio de alta del glosario | caen E-4/E-5 | diferido con ellos |
| F-6 | existe un hogar resuelto que evita el `STOP (NEW FAMILY)` | irrelevante mientras no se cree superficie | sin objeto tras §6.1 |

### 7.2 Condiciones nuevas

| # | Enunciado | Efecto |
|---|---|---|
| **F-7** | el test de §3.3 (especificación ≠ afirmación) reduce los candidatos a < 3 | `NO_STRUCTURAL_CHANGE` o `CORRECT_EXISTING_CLAIMS` |
| **F-8** | las superficies de control C1–C2 son **más** cuidadosas que S1–S9 | el diagnóstico cambia: es disciplina mal aplicada, no ausencia de disciplina → favorece I-1 sobre I-2 |
| **F-9** | los dos casos de §2.1 eran ambos corregibles por redacción, sin regla | `CORRECT_EXISTING_CLAIMS` — precedente de que la corrección basta |
| **F-10** | la disciplina de la capa Protocol (H-8) no tiene equivalente DEV **por decisión**, no por omisión | `MINIMAL_RULE` — hay una causa común identificable |

### 7.3 Cómo esta revisión puede concluir **menos** trabajo

Es el resultado **esperado**, no el excepcional. Con el prior de §0.3, la combinación más probable es `CORRECT_EXISTING_CLAIMS` o `NO_STRUCTURAL_CHANGE` (75 %). Si la auditoría lo confirma:

- la v1 se archiva como Working histórico (RFC-46: no se reescribe);
- `PRIORITY.md:0.1` se registra como **resuelto por auditoría**, con su evidencia;
- los entregables E-2, E-4, E-5 y E-7 se retiran;
- el trabajo restante es `I-1`, docs-only, mínimo.

**Y la revisión puede concluir más trabajo:** si la auditoría devuelve `MODEL_REQUIRED` con casos estructurales, el alcance se amplía — pero entonces la justificación será la evidencia, no el diseño previo.

---

## 8. Lo que NO se decide ahora (diferido por principio)

Ninguno de estos se resuelve en la Fase 0 ni se usa como dependencia de ella:

| Diferido | Por qué |
|---|---|
| Glosario: `Claim`, `Evidence`, `Guarantee` | secundario; E-4 diferido |
| `Conformance`, `Invariant`, `Capability`, `Aspiración`, `Hipótesis` | secundarios; E-5 diferido; el glosario ya declara que la ausencia de un término no es defecto (`docs/glossary/INDEX.md:65–66`) |
| Canonización de `PROTOCOL`/`DEV`/`BOTH` | es D-1 de `docs/planificacion-argentos-diseno-2026-10-13.md:1281`, decisión del mantenedor; **no puede ser dependencia** (H-7) |
| Todo cambio en `protocol/.agents/` | E-7 diferido; exigiría RFC-56 Clase A |
| Checker | I-5; sólo tras 10–15 usos reales de I-2 |
| Superficie de afirmaciones / registro | descartado (v1 §3.1, conservado); sin evidencia que lo invalide |
| Desambiguación de «verified» (H-3) | sólo importa si la solución necesita el término |
| Reconciliación del layout del payload (`.argentos/` vs `.agents/`) | pertenece al plan 156 |

---

## 9. Decisiones reservadas al mantenedor

| # | Decisión | Opciones |
|---|---|---|
| **D-1** | ¿Se autoriza la **auditoría de §3** como el único trabajo de la Fase 0? | (a) sí, con el alcance de §3.1; (b) sí, reducida a S4–S9; (c) no |
| **D-2** | ¿Se acepta la regla de decisión pre-registrada de §3.6, incluido `NO_STRUCTURAL_CHANGE` como resultado válido? | (a) sí; (b) sí, con otro umbral (especificar); (c) no |
| **D-3** | ¿Se acepta la corrección de §3.3 (especificación ≠ afirmación) como criterio de conteo? | (a) sí; (b) no — lo que multiplicaría los candidatos y requeriría re-discutir la materialidad |
| **D-4** | ¿Se archiva la v1 como Working histórico cuando la auditoría concluya? | (a) sí; (b) no |
| **D-5** | ¿Se ejecutan F-1/F-2/F-4a–d dentro de la misma auditoría? | (a) sí; (b) no, por separado |
| **D-6** | Hogar de `PRIORITY.md` y `docs/planificacion-argentos-diseno-2026-10-13.md` | sigue pendiente de la v1; **no** se resuelve aquí |

---

## Anexo A — Correcciones a la v1, una por una

| # | Afirmación o diseño de la v1 | Corrección | Fundamento |
|---|---|---|---|
| 1 | «§0.1 pide clasificar; por tanto hay que resolver Q1–Q3» | No se sigue. Se puede satisfacer Q4 sin construir el instrumento de Q1–Q3. La v1 lo dijo y luego construyó el instrumento | §1.2, §1.3 |
| 2 | H-1 como defecto | Es mayormente especificación legítima | §3.3 |
| 3 | Tres ejes como base de E-1/E-2/E-3 | Hipótesis no adoptada; el eje `alcance` está bloqueado | §6.2, H-7 |
| 4 | E-2 tabla de traducción | Eliminada: canoniza un noveno vocabulario para un problema no medido | §6.3.1 |
| 5 | E-1 con seis reglas | Reducida a **una** regla posible, condicional a `MINIMAL_RULE` | §3.6, §6.1 |
| 6 | E-4/E-5 glosario y `GAP` de términos | Diferidos: justificación circular | §6.3.3 |
| 7 | E-7 cambios de payload | Diferidos: su premisa H-1 no sobrevive el test | §6.1 |
| 8 | §3.1 de la v1: «cinco razones para no crear un registro» | Correctas, pero se usaron para justificar **otra** estructura. Rechazar un registro e introducir regla + tabla + gramática + glosario + payload **no es «no añadir maquinaria»: es redistribuirla** | §0.1, §6.3 |
| 9 | La v1 no midió el problema antes de diseñar | Ésta es la corrección principal; §3 la sustituye por una auditoría con regla de decisión pre-registrada | §0, §3 |
| 10 | §7 de la v1 declaraba la no-verificabilidad mecánica como «límite declarado» | Se conserva y se amplía: `docs/working/` no está cubierto por el checker de citas, verificado en `tools/check_plan_citations.py:194–210` | §3.8 |

---

## Anexo B — Evidencia citada

| Afirmación | Evidencia |
|---|---|
| §0.1 pide clasificar y determinar evidencia | `PRIORITY.md:23–37` |
| El objetivo de §0.1 es evitar la sobre-afirmación | `PRIORITY.md:37` |
| El solapamiento de vocabularios es un problema declarado | `PRIORITY.md:128–137` |
| Caso 1: aspiración presentada como garantía, ya corregida | `docs/working/audits/AUDITORIA_SISTEMA_2026-08-16.md:382`; `protocol/.agents/harness/INDEX.md:164` |
| Caso 2: afirmación de estado, reportada sin verificación independiente | `docs/planificacion-argentos-diseno-2026-10-13.md:1298`; `ROADMAP.md:35` |
| H-1: enunciados de los entry points | `protocol/_AGENTS.md:8,43`; `protocol/.agents/INDEX.md:21,25–29` |
| H-2: `status: planned` retirado con condición de reinstauración | `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:68–72` |
| H-3: «verified» con cuatro acepciones | `protocol/.agents/standards/quality/EVIDENCE.md:65–78`; `harness/INDEX.md:41–47`; `standards/runtime/PROTOCOL_METRICS.md:207–219`; `standards/context/MEMORY_SYSTEM.md:81–86` |
| H-4: verificadores DEV-only y frontera de distribución | `protocol/.agents/harness/INDEX.md:112–125`, `:41–47`, `:49–62` |
| H-5: IDs citados, definidos sólo en DEV | `docs/rfc/62-guarantee-model-and-enforcement-boundaries.md:166–190` |
| H-6: términos ausentes del glosario, y que su ausencia no es defecto | `docs/glossary/terms.md`; `docs/glossary/INDEX.md:65–66`, `:74–104` |
| H-7: vocabulario de dominio definido sólo para el ROADMAP | `docs/CONVENTIONS.md:785`; `docs/planificacion-argentos-diseno-2026-10-13.md:1300` |
| H-8: límites honestos declarados | `protocol/.agents/harness/INDEX.md:16`, `:27`, `:31–34`, `:415` |
| Recurrencia como señal de regla estructural | `docs/placement-contract.md:PC-28` |
| Mecanismos que podrían hacer E-1 redundante | `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md`; `protocol/.agents/standards/quality/CONFIDENCE.md`; `docs/behavior-patterns.md` (ausencia de evidencia ≠ evidencia positiva); `protocol/.agents/harness/INDEX.md:164` |
| El checker de citas no cubre `docs/working/` | `tools/check_plan_citations.py:194–210` |
| Decisión D-1 sobre el vocabulario de dominio | `docs/planificacion-argentos-diseno-2026-10-13.md:1281` |
| Prohibición de registry | `docs/AGENTS.md:Do NOT`; `docs/placement-contract.md:PC-10`, `PC-20` |

---

_Fin de la revisión. La auditoría de §3 no fue ejecutada. Ninguna fase de implementación fue ejecutada. Este documento es Working, no normativo, y su conclusión puede ser que `PRIORITY.md:0.1` requiera menos trabajo del que la v1 propuso, más trabajo, o ningún cambio estructural._
