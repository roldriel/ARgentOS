# Plan 181 — DEV Memory Pilot

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-29
**Tipo:** Plan
**Lifecycle:** active
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L2
**Depende de:** Plan 180
**Origen:** decisión posterior al estudio comparativo; ejecutar primero el experimento de DEV Memory en `refactor`.
**Work type:** GAP

## Objetivo

Ejecutar un piloto controlado de **DEV Memory** para comprobar si una pequeña capa de conocimiento durable reduce el coste de recuperar conclusiones de ARgentOS sin convertirse en una segunda autoridad.

El piloto no implementa un sistema de memoria productivo, no modifica el payload de Protocol y no sustituye RFC/ADR/Plan/Git.

## Hipótesis

> Un conjunto pequeño de conclusiones durables, con alcance y provenance explícitos, permite responder preguntas recurrentes sobre ARgentOS con menos recuperación histórica que buscar directamente en múltiples artefactos.

Hipótesis secundaria:

> La memoria sigue siendo útil si permanece no autoritativa y remite a evidencia de origen.

## Diseño experimental

Se construirá un corpus inicial de 8 entradas, derivadas de los ocho estudios comparativos del Plan 180.

Cada entrada tendrá:

- ID estable del piloto;
- conclusión;
- tipo;
- alcance;
- aplicabilidad;
- no-aplicabilidad;
- evidencia de origen;
- fecha de observación;
- estado epistemológico;
- estado de lifecycle;
- relaciones de supersession/contradicción si aparecen.

Se usarán preguntas de recuperación que crucen varios análisis.

### Baseline A — recuperación directa

Responder cada pregunta consultando directamente los artefactos históricos pertinentes.

### Treatment B — DEV Memory

Responder primero desde el índice de memoria y consultar la evidencia de origen únicamente cuando sea necesario para validar, ampliar o resolver incertidumbre.

### Métricas

Se registrarán:

- artefactos fuente consultados;
- entradas de memoria consultadas;
- necesidad de rehidratación;
- cobertura de la respuesta;
- errores de alcance;
- claims no soportados;
- contradicciones detectadas;
- mantenimiento requerido.

No se presentarán tiempos de ejecución como evidencia si no fueron medidos bajo condiciones controladas.

## Criterios de éxito

El piloto es favorable si, frente al baseline:

1. reduce materialmente la cantidad de artefactos históricos necesarios para responder las preguntas;
2. no aumenta claims no soportados;
3. mantiene provenance resoluble;
4. evita convertir conclusiones históricas en autoridad;
5. permite identificar cuándo la memoria no es suficiente y exige rehidratación;
6. mantiene un corpus pequeño y mantenible.

## Criterios de rechazo

Rechazar o rediseñar el enfoque si:

- la memoria duplica demasiado contenido fuente;
- las respuestas requieren igualmente recuperar casi todos los artefactos;
- aparecen errores de alcance o generalización;
- provenance no permite rehidratar la conclusión;
- el índice se convierte de facto en autoridad;
- el mantenimiento supera el ahorro de recuperación observable.

## Scope

Incluido:

- DEV Memory;
- knowledge extraction;
- provenance;
- retrieval;
- applicability;
- contradiction/supersession semantics;
- compaction implications.

Excluido:

- `protocol/.agents/`;
- runtime implementation;
- automatic consolidation;
- automatic deletion;
- embeddings/vector DB;
- global relationship graph;
- production memory API.

## Artefactos

1. `docs/plans/181-dev-memory-pilot.md`
2. `DEV_MEMORY_PILOT.md`
3. `DEV_MEMORY_EXPERIMENT.md`

## Regla de interpretación

Este piloto mide una **hipótesis de retrieval/knowledge utility**, no demuestra que el modelo de Memory System definitivo deba tener esta representación.

Un resultado negativo es válido.

## Autorización

El trabajo se limita a la rama `refactor`, conforme a la instrucción explícita del mantenedor. No se modifica `dev`, `master`, `protocol/.agents/` ni `dist/`.
