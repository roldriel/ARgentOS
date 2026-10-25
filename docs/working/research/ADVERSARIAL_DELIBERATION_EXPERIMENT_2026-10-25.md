# Adversarial Deliberation — protocolo experimental (registro Working)

> **Naturaleza:** Working / no normativo (`docs/AGENTS.md`: Audit, Research, Proposal bajo `docs/working/`). Es provenance y evidencia; nunca autoridad.
> **Origen:** documento de diseño aportado por el mantenedor el 2026-10-25 como protocolo de la investigación «Evolución del Juicio por Jurado hacia deliberación adversarial» (Priority 3.7; insumo local del mantenedor no versionado). Se registra tal como fue aportado, sin reinterpretarlo.
> **Uso:** es el protocolo bajo el cual se ejecutó `Trial #1`, registrado en `ADVERSARIAL_DELIBERATION_TRIAL_1_2026-10-25.md`.
> **Contención:** el insumo local no versionado del mantenedor no se cita como `ruta:sección` (RFC-69 I2; precedente `<PLAN-178>:F-2`).
> **Estado:** `INVESTIGACIÓN — EXPERIMENTAL DESIGN READY` (estado declarado por el propio protocolo). No promueve mecanismo, no modifica `protocol`, no modifica `.agents` y no crea autoridad.

---

# ARgentOS DEV — Adversarial Deliberation

## 1. Propósito

Investigar desde cero si el mecanismo de **Juicio por Jurado** puede evolucionar hacia una forma de **deliberación adversarial** que mejore de manera observable la calidad de decisiones y planes en ARgentOS DEV.

La investigación no parte de la premisa de que la evolución sea necesaria ni de que vaya a resultar beneficiosa.

La pregunta experimental es:

> **¿La deliberación adversarial permite detectar problemas materiales que el proceso normal no detecta, y lo hace con un coste y una complejidad justificables?**

La respuesta puede ser:

- sí;
- parcialmente;
- no;
- o incluso negativa: puede introducir más ruido que valor.

---

## 2. Qué estamos investigando

No vamos a intentar construir inicialmente un "Court" completo.

La hipótesis mínima es mucho más pequeña:

```text
CANDIDATE DECISION
        ↓
     DEFENSE
        ↓
   PROSECUTION
        ↓
   COMPARISON
        ↓
    SYNTHESIS
        ↓
     VERDICT
        ↓
   RECOMMENDATION
```

La deliberación debe producir **mejor información para decidir**, no convertirse en una nueva autoridad.

Por lo tanto:

```text
DELIBERATION
     ↓
EVIDENCE / ANALYSIS
     ↓
VERDICT / RECOMMENDATION
     ↓
EXISTING AUTHORITY
```

La última decisión permanece en la autoridad que ya correspondía al proceso.

---

## 3. Hipótesis

### H1 — Hipótesis positiva

> Para decisiones materialmente ambiguas o riesgosas, una segunda postura deliberadamente adversarial puede descubrir supuestos, riesgos, contradicciones o alternativas que el proceso normal no identifica.

La hipótesis queda demostrada únicamente si aparece evidencia observable.

No alcanza con que la deliberación produzca más texto.

### H2 — Hipótesis de independencia

> Separar la construcción del caso favorable de la construcción del caso contrario puede producir hallazgos diferentes de los obtenidos mediante una única evaluación.

Esto debe mantenerse separado de H1.

Dos perspectivas pueden ser útiles aunque sean producidas por el mismo agente.

Eso demuestra **adversarial reframing**, pero no demuestra independencia epistémica.

### H3 — Hipótesis negativa

> La deliberación adversarial puede agregar coste, complejidad y objeciones espurias sin mejorar materialmente la decisión.

Esta hipótesis es igual de importante.

Si se confirma, el resultado correcto del experimento es reducir o descartar la iniciativa.

---

## 4. Qué significa "adversarial"

No significa que una parte deba intentar "ganar".

Significa que cada postura recibe una función epistemológica diferente.

### Defense

Construir el **strongest case for** la propuesta.

Debe intentar demostrar:

- por qué la propuesta es válida;
- qué evidencia la respalda;
- bajo qué condiciones funciona;
- qué supuestos necesita;
- por qué las alternativas son inferiores;
- qué riesgos ya están controlados.

### Prosecution

Construir el **strongest case against** la misma propuesta.

Debe buscar:

- supuestos inválidos;
- evidencia insuficiente;
- contradicciones;
- casos límite;
- dependencias omitidas;
- efectos secundarios;
- integraciones inexistentes;
- autoridad mal asignada;
- alternativas superiores;
- condiciones bajo las cuales la propuesta deja de ser válida.

La prosecution no debe inventar hechos para producir una objeción.

---

## 5. El objeto de deliberación

La unidad mínima no debería ser simplemente "una opinión".

Debe existir un objeto explícito:

```text
DELIBERATION QUESTION
        +
CANDIDATE
        +
CRITERIA
        +
EVIDENCE
```

Ejemplo conceptual:

```text
QUESTION
¿Debemos adoptar X?

CANDIDATE
Implementar X mediante Y.

CRITERIA
- correctness
- integration
- authority
- maintainability
- cost
- reversibility

EVIDENCE
- repository evidence
- tests
- documentation
- observed behavior
```

Esto evita que la deliberación se convierta en:

> "A dice sí, B dice no."

El objeto real debe ser:

> "Dado este candidato, estas evidencias y estos criterios, ¿qué argumentos soportan o refutan la decisión?"

---

## 6. Commit-before-reveal

Una propiedad experimental importante será que Defense y Prosecution elaboren sus posiciones **antes de conocer la posición de la otra parte**.

```text
FRAME
  ↓
DEFENSE
  ↓
COMMIT
  ↓
PROSECUTION
  ↓
COMMIT
  ↓
REVEAL
```

Esto permite observar si realmente aparecen argumentos independientes.

Sin esta separación, existe riesgo de que la segunda postura simplemente reaccione a la primera.

---

## 7. Rebuttal

El rebuttal no debe ser obligatorio inicialmente.

Debe utilizarse cuando existe un desacuerdo material que necesita respuesta.

```text
DEFENSE
    ↓
PROSECUTION
    ↓
REBUTTAL
```

El objetivo no es producir una discusión infinita.

El rebuttal debe responder:

> ¿La objeción cambia materialmente la evaluación del candidato?

Si no puede responder eso, probablemente no aporta valor.

---

## 8. Synthesis

La síntesis no debe ser un "juez" con autoridad normativa.

Su función sería reconstruir:

- convergencias;
- contradicciones;
- argumentos materiales;
- argumentos débiles;
- evidencia compartida;
- evidencia faltante;
- dependencias;
- condiciones;
- desacuerdos;
- consecuencias.

Debe existir una regla estricta:

> **La síntesis no puede introducir evidencia externa o argumentos materiales que no aparecieron en las evaluaciones.**

Si aparece un argumento material nuevo, debe producirse una nueva evaluación.

## 9. Verdict

Inicialmente utilizaría un espacio deliberadamente pequeño:

```text
VIABLE
NOT_VIABLE
UNDETERMINED
```

No necesitamos veinte estados.

El verdict debe incluir siempre su fundamento.

```text
VERDICT
    +
BASIS
    +
MATERIAL_FINDINGS
    +
DISAGREEMENTS
```

---

## 10. Recommendation

El verdict y la recomendación deben permanecer separados.

Ejemplo:

```text
VERDICT = UNDETERMINED

RECOMMENDATION = GATHER_EVIDENCE
```

o:

```text
VERDICT = VIABLE

RECOMMENDATION = PROCEED
```

o:

```text
VERDICT = NOT_VIABLE

RECOMMENDATION = REVISE
```

La recomendación tampoco constituye autoridad.

---

## 11. Desacuerdo

El desacuerdo es un resultado válido.

No debemos resolverlo automáticamente mediante mayoría.

Por ejemplo:

```text
CRITERION              DEFENSE       PROSECUTION
-------------------------------------------------
Correctness             agree         agree
Integration             agree         disagree
Reversibility           disagree      agree
Evidence sufficiency    disagree      disagree
```

El resultado puede ser:

```text
VERDICT = UNDETERMINED
```

Eso es información útil.

Por ahora:

> **Argument provenance > vote count**

La votación queda como una hipótesis posterior, no como requisito del MVP.

---

## 12. Independencia

Hay tres conceptos diferentes:

### Attribution independence

¿Podemos saber qué postura produjo cada argumento?

Debe ser obligatorio.

### Procedural independence

¿Las evaluaciones fueron construidas separadamente?

Debe probarse mediante commit-before-reveal.

### Epistemic independence

¿Las evaluaciones realmente utilizan razonamientos diferentes?

No podemos garantizarla simplemente porque existan dos evaluadores.

El experimento debe medirla indirectamente mediante la diversidad y materialidad de los hallazgos.

---

## 13. Baseline

Necesitamos comparar contra algo.

El baseline será:

```text
QUESTION
   ↓
NORMAL ANALYSIS
   ↓
DECISION / PLAN
```

Debe conservarse el resultado **antes** de introducir deliberación adversarial.

Registrar:

- propuesta;
- razonamiento;
- supuestos;
- evidencia;
- riesgos;
- decisión;
- incertidumbres.

No debemos reconstruir el baseline retrospectivamente si podemos evitarlo.

---

## 14. Tratamiento experimental

La misma cuestión será sometida a:

```text
BASELINE
   ↓
RESULT A
```

y luego:

```text
ADVERSARIAL DELIBERATION
   ↓
RESULT B
```

Se compararán:

- nuevos hallazgos;
- supuestos invalidado;
- riesgos descubiertos;
- evidencia adicional;
- cambios del plan;
- cambios del verdict;
- cambios de recomendación;
- desacuerdos;
- costes adicionales.

---

## 15. Qué cuenta como hallazgo material

Para evitar "adversarial theater", un hallazgo sólo cuenta como material si cambia potencialmente la decisión.

Clasificación inicial:

```text
MATERIAL
NON_MATERIAL
SPURIOUS
DUPLICATE
```

Un hallazgo es material si, por ejemplo:

- invalida una premisa;
- descubre una dependencia necesaria;
- demuestra una integración ausente;
- cambia una condición de aceptación;
- introduce un riesgo que requiere mitigación;
- obliga a modificar el plan;
- cambia el verdict;
- cambia la recomendación.

Un argumento interesante pero irrelevante para la decisión no demuestra valor.

---

## 16. Métricas

### Beneficio

Medir:

```text
material findings missed by baseline
invalid assumptions detected
plan changes
verdict changes
recommendation changes
new evidence requirements
integration gaps discovered
```

### Coste

Medir:

```text
additional evaluations
additional tokens / context
execution time
additional synthesis work
```

### Ruido

Medir:

```text
spurious objections
duplicate arguments
irrelevant objections
false contradictions
unnecessary plan changes
```

La métrica más importante no será cantidad de argumentos.

Será:

> **material decision-relevant findings per unit of additional cost.**

---

## 17. Criterios de éxito

### Éxito fuerte

La deliberación encuentra uno o más problemas materiales que:

1. el baseline no detectó;
2. tienen evidencia suficiente;
3. cambian o deberían cambiar el plan/decisión;
4. no son objeciones espurias.

### Éxito parcial

Encuentra riesgos reales pero no cambia la decisión.

Esto puede demostrar valor preventivo, aunque menor.

### Sin evidencia de valor

Defense y Prosecution terminan esencialmente en el mismo resultado sin nuevos hallazgos materiales.

### Resultado negativo

La deliberación:

- produce principalmente ruido;
- genera objeciones falsas;
- no encuentra problemas nuevos;
- aumenta significativamente el coste;
- o empeora el resultado del análisis.

En ese caso debemos considerar que la hipótesis falló.

## 18. Primer MVP experimental

El MVP debe tener solamente:

```text
FRAME
  ├─ question
  ├─ candidate
  ├─ criteria
  └─ evidence

DEFENSE
  └─ committed evaluation

PROSECUTION
  └─ committed evaluation

REVEAL

COMPARISON
  ├─ agreements
  ├─ disagreements
  └─ material findings

SYNTHESIS

VERDICT
  └─ basis

RECOMMENDATION
  └─ optional

AUTHORITY
  └─ existing decision mechanism
```

Fuera del MVP:

- N jurors;
- voting;
- juez con autoridad;
- nuevo state machine;
- infraestructura multi-agent;
- aislamiento técnico obligatorio;
- nuevo governance layer;
- integración normativa con `protocol`;
- ejecución automática;
- gates automáticos.

---

## 19. Primer experimento

El primer experimento debería utilizar una decisión DEV real, no un ejemplo artificial.

Debe cumplir:

- tener ambigüedad real;
- tener más de una alternativa razonable;
- tener consecuencias suficientes para que una objeción importe;
- disponer de evidencia verificable;
- no requerir modificar el protocolo para poder experimentar.

Idealmente debería estar relacionado con una decisión de arquitectura, evolución o implementación donde exista riesgo de asumir incorrectamente cómo se conecta una capacidad con el sistema existente.

No debemos elegir un caso trivial.

Tampoco uno tan complejo que sea imposible determinar qué produjo el resultado.

---

## 20. Registro experimental

Cada trial debería conservar:

```text
TRIAL

QUESTION

CANDIDATE

CRITERIA

EVIDENCE

BASELINE
    analysis
    assumptions
    decision

DEFENSE
    arguments
    evidence
    assumptions
    commitment

PROSECUTION
    arguments
    evidence
    assumptions
    commitment

REVEAL

COMPARISON
    agreements
    disagreements
    material findings

SYNTHESIS

VERDICT

RECOMMENDATION

PLAN CHANGES

FINAL OUTCOME

COST

EVALUATION
```

La trazabilidad es esencial porque, de otro modo, después no podremos distinguir entre:

> "la deliberación encontró un problema"

y

> "la deliberación produjo mucho texto y posteriormente alguien encontró un problema."

---

## 21. Relación con Theoretical Execution

La combinación parece prometedora, pero todavía debe tratarse como hipótesis.

Una posible secuencia experimental es:

```text
IMPLEMENTATION PLAN
        ↓
THEORETICAL EXECUTION
        ↓
THEORETICAL FINDINGS
        ↓
ADVERSARIAL DELIBERATION
        ↓
DEFENSE / PROSECUTION
        ↓
SYNTHESIS
        ↓
VERDICT
        ↓
PLAN REVISION
        ↓
THEORETICAL EXECUTION AGAIN
        ↓
ACTUAL EXECUTION
```

La razón para repetir Theoretical Execution después de la deliberación es importante.

No queremos demostrar simplemente que la deliberación encontró problemas.

Queremos observar si:

> **la deliberación consigue producir un plan objetivamente mejor preparado para la ejecución posterior.**

---

## 22. Regla de no contaminación

Para que el experimento sea útil:

> El conocimiento producido durante Defense no debe contaminar la construcción inicial de Prosecution.

Y:

> El resultado de la deliberación no debe modificar retrospectivamente el baseline.

El baseline es una observación histórica del proceso normal.

---

## 23. Qué NO vamos a concluir

Incluso si el primer experimento funciona, no podremos concluir todavía que:

- Jury debe desaparecer;
- Adversarial Deliberation debe convertirse en parte del Protocol;
- voting es útil;
- varios jurados son necesarios;
- los evaluadores son epistemológicamente independientes;
- existe una arquitectura multi-agent necesaria;
- el mecanismo debe ejecutarse en todos los planes;
- la deliberación garantiza decisiones correctas.

El experimento sólo puede demostrar aquello que realmente mida.

---

## 24. Decisión posterior al experimento

Después del primer trial existen cuatro caminos legítimos:

```text
EVIDENCE POSITIVE
      ↓
ITERATE / SECOND TRIAL

EVIDENCE PARTIAL
      ↓
REFINE HYPOTHESIS

EVIDENCE NEGATIVE
      ↓
REDUCE / ABANDON

EVIDENCE INSUFFICIENT
      ↓
REDESIGN EXPERIMENT
```

Sólo después de esta etapa tendría sentido decidir si crear un Implementation Plan formal para evolucionar el mecanismo.

---

## 25. Criterio de salida de esta investigación

La investigación inicial puede considerarse concluida cuando podamos responder con evidencia:

1. ¿La deliberación adversarial encuentra algo que el baseline no encuentra?
2. ¿Ese algo es material?
3. ¿La evidencia es verificable?
4. ¿Cambia el plan o la decisión?
5. ¿El beneficio supera el coste?
6. ¿Genera ruido o falsos problemas?
7. ¿La separación Defense/Prosecution aporta algo observable?
8. ¿Hace falta realmente independencia entre agentes?
9. ¿Hace falta voting?
10. ¿Qué papel debería tener synthesis?
11. ¿Qué papel debería tener verdict?
12. ¿Cómo debe tratarse el desacuerdo?
13. ¿Theoretical Execution mejora cuando ambos mecanismos se combinan?
14. ¿Existe suficiente evidencia para justificar una segunda iteración?

La respuesta a estas preguntas, y no la sofisticación del mecanismo, determinará qué sigue.

---

## 26. Estado propuesto

**INVESTIGACIÓN — EXPERIMENTAL DESIGN READY**

No se propone todavía:

- modificar `protocol`;
- modificar `.agents`;
- introducir un nuevo mecanismo normativo;
- eliminar Jury;
- introducir voting;
- crear una infraestructura permanente.

El próximo paso es ejecutar **Trial #1** bajo este protocolo y registrar el resultado completo.

El resultado del trial debe considerarse evidencia experimental, no verdad normativa.
