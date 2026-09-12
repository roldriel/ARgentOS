# Convención de deliberación adversarial (Working Convention)

> **Clase documental: Working · no normativa · pre-canónica · sin autoridad.**
> Este documento **no es gobernanza**, **no es un estándar** y **no es fuente normativa**.
> Su carácter normativo podrá evaluarse posteriormente mediante evidencia; esa
> promoción queda **fuera del Plan 114**.
>
> **Declaración de naturaleza de sus reglas.** Las reglas de este documento
> (`MUST`, `PROHIBITED`, "debe", "no puede", y las condiciones de procedencia,
> compromiso, síntesis y preservación del desacuerdo) son **condiciones y
> convenios de ejecución del experimento/MVP**. Son **instrucciones para quienes
> decidan utilizar esta Working Convention**, **no** para el workspace:
>
> - **no** son obligaciones generales de ARgentOS DEV;
> - **no** crean gates;
> - **no** crean lifecycle states;
> - **no** crean governance;
> - **no** modifican la autoridad existente (el mecanismo sigue sin decidir,
>   autorizar, aprobar ni descartar);
> - **no** son requisitos para trabajos DEV que no utilicen esta convención.
>
> El uso interno de `MUST`/`PROHIBITED` es, por tanto, **interno al experimento**:
> quien no invoque esta convención no queda alcanzado por ninguna de sus reglas.
>
> **Estado de la convención (decisión del mantenedor, 2026-09-09).** Tras la
> evidencia del primer dogfooding (Plan 114, `<PLAN-105>`), la decisión humana
> registrada es **`KEEP AS WORKING / CONTINUE DOGFOODING`**: este documento
> **permanece experimental/Working**. **No** se promueve a gobernanza, **no** se
> convierte en obligatoriedad general, **no** se incorpora al Change Lifecycle
> como requisito, **no** se incorpora al Protocol, **no** se transforma en
> RFC/ADR y **no** se vuelve regla normativa general de DEV. La evidencia
> disponible es positiva pero insuficiente para promoción amplia (N=1, mismo
> ejecutor en ambas perspectivas, independencia epistemológica no demostrada,
> una dimensión de valor no observable). El registro de la decisión vive en el
> Plan 114 (`### Decisión humana — fuera del mecanismo` y `### Pending
> decisions`); no se crea un Plan nuevo para continuar el dogfooding.
>
> **Estado de la evaluación de cierre (Plan 116, 2026-09-12).** El dogfood
> final A/B/C del MVP DEV se ejecutó y quedó registrado en
> `docs/plans/116-adversarial-deliberation-mvp-closure.md` (Escenario A:
> decisión real con ejecutores diferenciados; Escenario B: NO CHANGE como
> resultado legítimo; Escenario C: camino no canónico con confrontación
> acotada), con decisiones humanas registradas como actos separados o
> pendientes escaladas con owner. El closure predicate
> (contract/architecture/implementation/integration/validation/verification/
> dogfood/documentation/governance) quedó evaluado letra por letra con evidencia
> en ese Plan y **`JURY_TRIAL_CLOSED` quedó satisfecho**: el mantenedor aceptó el
> cierre del MVP DEV (Human Checkpoint, 2026-09-12: `D-1 = ACCEPT CLOSURE OF THE
> DEV ADVERSARIAL DELIBERATION MVP`; `D-2 = ACCEPT FINAL DOGFOOD A/B/C`) y el
> cierre se materializó con el commit atómico del Plan 116. La convención
> **permanece Working/no normativa** (naturaleza sin cambios): no se promueve a
> gobernanza, no se convierte en RFC/ADR, no se incorpora al Change Lifecycle ni
> al Protocol, y no adquiere autoridad. La feature Protocol-native sigue
> **FUTURE / NOT STARTED / OUT OF SCOPE**.
>
> **Estado del MVP (2026-09-12).** `Adversarial Deliberation MVP — DEV`:
> **CLOSED** (docs-only, sin release). Las decisiones deliberadas durante el
> dogfood (reconocimiento de `<PLAN-114>:F-1`/`F-2`, resolución de
> `<PLAN-114>:F-3`, release de `11.1.0`/`11.2.0`) permanecen pendientes con
> owner (mantenedor) y son independientes de este cierre.

---

## 1. Purpose

Obtener **evidencia adversarial trazable** sobre una decisión candidata antes de
que la decisión se tome: someter una solución candidata a una evaluación que
intente sostenerla y a otra que intente refutarla, y consolidar el resultado en
un **veredicto con base declarada** cuyas razones y desacuerdos sean
reconstruibles por un tercero.

Este documento **no es gobernanza** y **no es un paso obligatorio** de ningún
proceso. Su producto es una **recomendación advisory**; la decisión pertenece a
la autoridad DEV existente.

## 2. Scope

**Decisiones apropiadas:** aquellas con al menos **dos direcciones materiales
posibles**, o cuya **viabilidad esté en duda real**; y donde el resultado pueda
cambiar lo que se hará (no una decisión ya determinada por un criterio fijado).

**Decisiones inapropiadas:**

- cambios mecánicos o triviales;
- decisiones reversibles de bajo impacto, donde el costo de deliberar supera el
  de decidir;
- casos cuyo bloqueo real es **falta de evidencia**: ahí la acción es obtener la
  evidencia, no deliberar;
- casos cuyo criterio ya está fijado por gobernanza vigente (no hay preferencia
  que discutir).

## 3. Invocation

- **Quién:** el agente DEV y/o el humano. Ninguno requiere autorización previa
  para invocarla, porque invocar no cambia ningún estado.
- **Por qué:** porque la decisión cae en §2 y el veredicto puede aportar algo que
  una evaluación simple no aportaría.
- **Registro:** la invocación MUST registrar **el motivo** (por qué se considera
  que la decisión lo amerita).
- **PROHIBITED:** un clasificador automático que decida invocar o elegir la
  profundidad. La elección es una decisión declarada y justificada.
- Invocar **no** crea obligaciones, no marca estados y no es un gate.

## 4. Declared Frame

Antes de evaluar, el marco MUST quedar declarado:

| Elemento | Contenido |
|---|---|
| Problema / cuestión | **referencia** a la cuestión declarada (p. ej. una decisión pendiente registrada, una pregunta de RFC/ADR). No se modela como entidad |
| Candidata(s) | etiqueta **local** (p. ej. `C-1`) + descripción de una línea. Sin identidad global |
| Criterios | **obligatorios** en viabilidad y en comparación (p. ej. `K-1..K-n`), cada uno enunciado de forma evaluable |
| Modo | `viability` (Problema × Candidata) o `comparative` (Problema × {A, B}) |
| Límites | máximo de pasadas de evaluación; si hay confrontación; número de síntesis |

## 5. Evaluation Pass

Cada evaluación (una "pasada") MUST registrar:

1. **etiqueta local** de la evaluación;
2. **postura/instrucción** declarada (qué se le pidió: sostener, atacar, evaluar
   sin dirección);
3. **ejecutor** (quién la produjo);
4. **material recibido** (qué artefactos y qué secciones leyó antes de concluir);
5. **material compartido** (encuadre, criterios, evidencia común);
6. **relación con conclusiones previas** (ninguna / conocía la conclusión X);
7. **condición de compromiso**: la conclusión se registra **antes** de que otra
   pasada conozca su contenido;
8. **conclusión**;
9. **razones por criterio**;
10. **premisas** citadas (`ruta:sección`);
11. **supuestos**;
12. **incertidumbres**.

Una evaluación **MUST NOT** presentar su juicio como verificación de la
candidata: es un análisis atribuido.

## 6. Independence / Provenance

**Independencia es una condición de procedencia, relacional y direccional:** una
evaluación es independiente **respecto de la conclusión de otra** si (a) la produjo
un **ejecutor distinto** y (b) la conclusión de la otra **no formó parte del
material que recibió** antes de comprometer la suya.

- **Ejecutores distintos es condición NECESARIA y NO SUFICIENTE.** Este documento
  **no garantiza** independencia epistemológica y **PROHIBITED** afirmarla.
- El registro MUST distinguir: **evaluación independiente** · **re-evaluación**
  (mismo ejecutor tras conocer una conclusión) · **contexto compartido** ·
  **visibilidad de conclusiones previas**.
- Si todas las pasadas las produce el mismo ejecutor, la base del veredicto MUST
  declararlo (`ejecutores: mismo`) y **no** puede hablarse de independencia; la
  convergencia o divergencia observada es interna a un mismo ejecutor.
- **MUST NOT** crearse aislamiento técnico, ACLs, sandboxing ni infraestructura
  multi-agente para sostener esta convención.

## 7. Optional Confrontation

La confrontación (intercambio donde la visibilidad mutua **es** el mecanismo) es
**opcional** y **acotada**.

- Su propósito MUST declararse.
- Cada intercambio MUST referir el argumento previo que responde y registrar qué
  aportó.
- **Criterio de valor:** un intercambio que no puede cambiar la base de evidencia
  ni introducir un contraargumento material **termina** la confrontación.
- **PROHIBITED:** infraestructura de rondas generalizada o configurable más allá
  del límite declarado en el marco.

## 8. Synthesis

**Puede (allowed):** resumir; reorganizar; derivar relaciones; identificar
contradicciones; identificar convergencias; identificar dependencias; identificar
condiciones; derivar consecuencias de premisas presentes; **discrepar** de una o
más evaluaciones.

**No puede (prohibited):** introducir hechos externos no soportados; introducir
evidencia nueva; introducir argumentos materiales no fundados en las evaluaciones
registradas; suprimir o reescribir retrospectivamente la conclusión de una
evaluación.

Reglas:

- Si la síntesis necesita aportar un **argumento material nuevo**, eso **no es
  síntesis**: MUST registrarse como **nueva pasada de evaluación** (con su postura
  y su ejecutor) o detenerse.
- Cada relación derivada MUST identificar **su origen** (evaluación, criterio o
  premisa de la que se deriva).
- Las conclusiones de **todas** las evaluaciones MUST permanecer visibles; la
  síntesis puede alcanzar un veredicto distinto y MUST registrar la divergencia.
- El **desacuerdo MUST preservarse** de forma explícita (idealmente a nivel de
  criterio). **PROHIBITED:** resolverlo por mayoría, por conteo o por preferencia
  del sintetizador.
- **La convergencia entre evaluaciones NO es evidencia adicional** y **MUST NOT**
  usarse para sostener un veredicto más fuerte que el que las condiciones
  permiten.

## 9. Verdict

Vocabularios (según el modo):

- **Viabilidad:** `VIABLE` | `NOT_VIABLE` | `UNDETERMINED`
- **Comparación:** `PREFERRED(A)` | `PREFERRED(B)` | `TIE` | `UNDETERMINED`

El veredicto MUST contener:

- **valor**;
- **base declarada**: ¿hubo ataque?; `ejecutores: mismo|distinto`; material
  compartido; criterios declarados; **qué quedó sin hacer**;
- **razones por criterio**;
- **desacuerdo** registrado;
- **relación con cada evaluación** (coincide / diverge);
- **limitaciones** declaradas;
- **razón de terminación** (§11).

`TIE` es una **conclusión** de igualdad bajo los criterios declarados;
`UNDETERMINED` es **ausencia** de conclusión y MUST llevar su razón.

**PROHIBITED:** presentar el veredicto como decisión; descartar automáticamente
la candidata; presentar convergencia como evidencia; afirmar independencia
epistemológica.

## 10. Recommendation

- **Opcional.** Si corresponde, se emite **separada** del veredicto y de la
  decisión.
- Es **advisory**: **MUST NOT** autorizar, aprobar, decidir ni modificar
  gobernanza.
- Si no corresponde emitirla, MUST registrarse la **ausencia deliberada**.

## 11. Termination

Toda ejecución termina registrando **una razón** (no un estado de lifecycle):

| Razón | Significado |
|---|---|
| `VERDICT` | se alcanzó un veredicto justificado |
| `UNDETERMINED` | no pudo alcanzarse un veredicto justificado (con su motivo) |
| `LIMIT` | se agotó un límite declarado antes de concluir |
| `NO_VALUE` | más ejecución no cambiaría la base (fundamento obligatorio) |
| `FAILURE` | un paso requerido no pudo ejecutarse |

Regla de continuación: se añade ejecución **solo si** puede plausiblemente
cambiar la base de evidencia, exponer un contraargumento material o resolver una
incertidumbre **de hecho**. Si el residuo es un **desacuerdo de criterio** (qué
priorizar), más ejecución **no** converge: MUST terminar y elevar la decisión a
la autoridad.

**PROHIBITED:** crear estados globales o una máquina de estados para representar
la terminación; "seguir deliberando" como respuesta por defecto.

## 12. Authority Boundary

**Puede:** evaluar; atacar; defender; sintetizar; emitir veredicto; emitir
recomendación; revelar material que el proceso DEV registre aparte como finding.

**No puede (PROHIBITED):** decidir; autorizar; aprobar; descartar candidatas;
resolver findings; cambiar el lifecycle; crear gobernanza; convertirse en gate;
reemplazar la validación; reemplazar la verificación.

`Verdict ≠ Recommendation ≠ Decision`. La decisión pertenece a la autoridad DEV
existente y se registra **fuera** de este mecanismo.

## 13. Canonical MVP Path

```
candidata
   → perspectiva A (atribuida, conclusión COMPROMETIDA)
   → perspectiva B (atribuida, conclusión COMPROMETIDA, sin conocer A)
   → revelación
   → síntesis (preserva desacuerdo, cita orígenes)
   → veredicto con base declarada
   → recomendación (opcional, advisory)
   → decisión humana (FUERA del mecanismo)
```

La segunda perspectiva **MUST NOT** recibir la conclusión de la primera antes de
comprometer la propia. Este camino **MUST NOT** convertirse en una máquina de
estados: es una secuencia de pasos registrados.

## 14. Degradation

| Situación | Qué se hace |
|---|---|
| Solo existe una perspectiva | Se declara explícitamente la **ausencia de segunda perspectiva**; la base del veredicto lo dice. **PROHIBITED:** simular independencia o presentar una pasada única como deliberación adversarial |
| Una perspectiva falla | Se registra la omisión; se declara si la base alcanza; si no alcanza → `UNDETERMINED` |
| Evidencia insuficiente | `UNDETERMINED(INSUFFICIENT_EVIDENCE)`; se registra qué falta y si es obtenible |
| Desacuerdo | `UNDETERMINED(DISAGREEMENT)` o veredicto **con desacuerdo declarado**; nunca se adjudica |
| La síntesis no puede resolver | `UNDETERMINED` con la divergencia registrada; **PROHIBITED** elegir un ganador |
| Se alcanza el límite | `UNDETERMINED(LIMIT)` si no había veredicto; el veredicto alcanzado si ya existía |
| Un ejecutor no puede completar una pasada | Reintentar en las mismas condiciones = el **mismo paso reintentado**; con condiciones nuevas = **paso nuevo** |
| Interrupción / reanudación | Se conserva lo comprometido; nada se reescribe; lo posterior es contenido nuevo que referencia lo anterior |
