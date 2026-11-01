# Adversarial Deliberation Evolution — 2026-10-31

**Status:** In progress
**Scope:** DEV / refactor
**Related Plan:** 183
**Prior experiment:** Plan 179 — Minimal Adversarial Review, decision REJECT

## 1. Pregunta

¿Existe una evolución útil del mecanismo de deliberación adversarial de ARgentOS que resuelva una carencia real que no haya quedado resuelta por el mecanismo existente ni por MAR?

La pregunta no es si Court Skill es mejor que ARgentOS. La pregunta es qué mecanismos concretos, si alguno, introducen una propiedad nueva y medible.

## 2. Evidencia previa

Plan 179 rechazó la configuración MAR experimental. Por tanto, esta investigación no parte de "MAR necesita más trabajo", sino de una pregunta más fuerte: si la reducción experimental eliminó precisamente una propiedad que podría ser valiosa.

La evidencia previa obliga a no confundir:

- existencia de deliberación;
- coste de deliberación;
- descubrimiento material;
- independencia epistémica;
- calidad de decisión;
- autoridad.

## 3. Referencia externa: Court Skill

La implementación pública de Court Skill descompone el proceso en prosecutor, defense, rebuttals, 12 jurors independientes y judge. Los jurados reciben perspectivas diferenciadas y no ven los votos de otros jurados antes de votar. El resultado incluye veredicto, razones y condiciones que podrían cambiarlo.

Referencia: https://github.com/alexyc9381/court-skill

Estas propiedades son mecanismos candidatos, no arquitectura que ARgentOS deba copiar.

## 4. Matriz inicial

| Mecanismo | ARgentOS actual | Court | ¿Propiedad nueva? | Estado |
|---|---|---|---|---|
| Caso contra | Sí, en deliberación adversarial previa | Sí | No demostrado | existente |
| Caso a favor | Sí | Sí | No demostrado | existente |
| Rebuttal | Parcial/según diseño experimental | Sí | Posible | investigar |
| Perspectivas heterogéneas explícitas | No demostrado como propiedad aislada | Sí | Sí, potencial | investigar |
| Voto independiente | No demostrado como mecanismo estable | Sí | Sí, potencial | investigar |
| Judge/synthesis | Síntesis/adjudicación existe conceptualmente | Sí | No demostrado | existente/parcial |
| Condiciones de reversión | Presente en experimentos previos como advisory | Sí | No demostrado | existente |
| Evidencia/provenance | Sí, con governance explícita | No es equivalente | ARgentOS es más fuerte aquí | conservar |
| Autoridad decisional | Separada de deliberación | Judge produce verdict | Debe preservarse separación | restricción |
| Ejecución | Separada | Separada | No aplica | restricción |

## 5. Hipótesis candidata

La única diferencia que parece suficientemente concreta para justificar investigación adicional es:

> **La independencia estructurada de perspectivas podría producir detección de desacuerdos o contraejemplos que una deliberación adversarial secuencial no detecta.**

Esto todavía es una hipótesis, no un hallazgo.

## 6. Falsación

La hipótesis debería rechazarse si un experimento futuro demuestra cualquiera de las siguientes condiciones:

1. las perspectivas independientes no producen hallazgos materialmente nuevos;
2. los hallazgos nuevos no cambian ninguna decisión ni condición de aceptación;
3. la diversidad de roles sólo añade ruido;
4. el mismo valor se obtiene con una sola revisión adversarial mejor estructurada;
5. el coste crece sin retención material de valor;
6. la independencia no puede aislarse de otras variables.

## 7. Lo que NO se concluye

No se concluye que:

- Court Skill sea adecuado para ARgentOS;
- un jury de 12 agentes sea necesario;
- el Jury actual deba reemplazarse;
- MAR deba reactivarse;
- deba crearse un nuevo runtime;
- la deliberación deba ser obligatoria;
- el judge deba adquirir autoridad;
- una votación sea evidencia de verdad.

## 8. Próximo paso condicionado

Sólo si la revisión de evidencia confirma que la independencia de perspectivas es una variable no cubierta y aislable, se justifica un experimento posterior pequeño.

Ese experimento debería comparar, como mínimo:

`single adversarial reviewer` vs `independent heterogeneous reviewers`

manteniendo constante el caso, evidencia, presupuesto comparable y criterio de evaluación.

Si esa comparación no puede aislarse limpiamente, la iniciativa debe cerrarse como `DEFER` o `REJECT`, no convertirse en infraestructura por intuición.

## 9. Estado

**Preliminar: REFORMULATE candidate.**

La evidencia disponible no justifica implementar Court ni un nuevo Jury. Sí justifica investigar una hipótesis más estrecha: independencia estructurada de perspectivas.
