# Adversarial Deliberation Evolution — 2026-10-31

**Status:** Closed — REFORMULATE
**Scope:** DEV / refactor
**Related Plan:** 183
**Prior experiment:** Plan 179 — Minimal Adversarial Review, decision REJECT

## 1. Resultado

La investigación **no justifica implementar Court ni ampliar el Jury existente**.

Sí identifica una hipótesis más estrecha y experimentalmente aislable:

> La independencia estructurada de perspectivas puede aportar valor que una deliberación adversarial secuencial no captura.

Esto permanece como hipótesis. No es una decisión arquitectónica.

## 2. Evidencia interna

La campaña T1–T3 mostró valor material de la deliberación adversarial, pero también costes altos y duplicación. Trials #2 y #3 fueron clasificados como `POSITIVE_BUT_COSTLY`, con ratios efectivos de coste de 4,01× y 5,21× respectivamente.

El Plan 179 intentó reducir ese coste mediante Minimal Adversarial Review y lo rechazó: la configuración probada aumentó el trabajo de retrieval y no justificó promoción.

Por tanto, la evidencia disponible no sostiene:

- "más deliberación = mejor";
- "Court = solución";
- "12 jurados = requisito";
- "MAR necesita simplemente más agentes".

La pregunta útil restante es qué propiedad concreta explica el valor material y si puede obtenerse con menor coste.

## 3. Evidencia externa: Court Skill

La referencia externa analizada implementa una secuencia de prosecutor, defense, rebuttals, 12 jurados independientes y judge. Los jurados reciben perspectivas diferenciadas y votan sin ver los votos de los demás; el judge produce el resultado y condiciones que podrían revertirlo. La implementación pública describe además un coste de 17 llamadas de subagentes para un trial completo. citeturn542734search0

Lo relevante para ARgentOS no es la estructura "court", sino tres mecanismos separables:

1. **perspectivas explícitamente diferenciadas**;
2. **independencia entre evaluadores antes de conocer otros votos**;
3. **síntesis posterior de resultados independientes**.

El resto puede considerarse composición/orquestación del mecanismo, no una propiedad que ARgentOS deba adoptar.

## 4. Matriz final

| Mecanismo | Estado en ARgentOS | Aporte externo | Decisión |
|---|---|---|---|
| Caso FOR / AGAINST | existente en deliberación previa | también presente | conservar |
| Rebuttal | existente experimentalmente | explícito | no nuevo por sí mismo |
| Síntesis | existente conceptualmente | judge/synthesis | conservar separación advisory |
| Perspectivas heterogéneas | no aislado experimentalmente | explícito | **hipótesis candidata** |
| Evaluadores independientes | no demostrado como propiedad aislada | explícito | **hipótesis candidata** |
| Voto independiente | no demostrado como necesidad | explícito | deferir |
| Jury de 12 | no necesario demostrado | configuración concreta | rechazar como requisito |
| Judge con autoridad | incompatible con boundary actual | produce verdict | rechazar como autoridad |
| Evidence/provenance | governance fuerte en ARgentOS | no equivalente | conservar ARgentOS |
| Execution / lifecycle | separado | separado en referencia | conservar separación |

## 5. Por qué no implementamos ahora

Hay tres razones:

1. **El problema no está suficientemente especificado.** "Mayor diversidad" no es todavía una métrica.
2. **El experimento anterior ya mostró sensibilidad fuerte al coste.** Introducir más agentes sin aislar la variable sería repetir el error.
3. **La independencia es una hipótesis, no una capacidad requerida.** Primero debe demostrarse que produce findings materialmente nuevos o mejora una decisión.

## 6. Hipótesis para un posible experimento posterior

Comparar:

`single adversarial reviewer`

contra

`independent heterogeneous reviewers`

manteniendo constante:

- caso;
- evidencia disponible;
- presupuesto comparable;
- criterio de materialidad;
- evaluación independiente;
- authority boundary;
- ausencia de contaminación entre evaluadores.

Medir:

- findings materialmente nuevos;
- findings duplicados;
- findings espurios;
- impacto decisional;
- coste adicional;
- sensibilidad al número de perspectivas.

### Falsación

Cerrar la hipótesis si:

- no aparecen findings materialmente nuevos;
- los nuevos findings no tienen impacto;
- la independencia sólo aumenta ruido;
- el mismo valor se obtiene con un único reviewer mejor estructurado;
- el coste adicional supera la retención material de valor;
- no puede aislarse la variable independencia/heterogeneidad.

## 7. Decisión

**Plan 183: REFORMULATE.**

No se crea implementación, runtime, Protocol feature, nuevo Jury ni Court.

La siguiente acción, si se decide continuar esta línea, debe ser un **Plan experimental separado** y preregistrado para medir independencia de perspectivas.

Hasta entonces, la arquitectura actual permanece sin cambios.

## 8. Límites

Esta investigación no demuestra que la hipótesis candidata sea verdadera. Sólo demuestra que es la diferencia más concreta identificada en la referencia externa que merece una prueba separada.

La referencia externa se utiliza como fuente de mecanismos; no constituye autoridad sobre ARgentOS.
