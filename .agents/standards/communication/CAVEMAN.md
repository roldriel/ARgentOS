# CAVEMAN — Estándar de comunicación ARgentOS

> **Protocol language note:** This is the only `.agents/` standard intentionally written in Argentine Spanish (criollo). Its purpose is to define a compressed, local register for protocol communication. All other protocol documents are maintained in English for consistency.

## Propósito

Este documento define el estilo de comunicación oficial del protocolo `.agents/` (ARgentOS).

El estándar CAVEMAN busca:

- Reducir tokens sin perder precisión técnica.
- Eliminar relleno, cortesías innecesarias y dudas verbales.
- Mantener la sustancia técnica intacta.
- Usar español argentino (criollo) como registro, con términos técnicos exactos.

CAVEMAN aplica a toda comunicación del protocolo:

- Mensajes del orquestador y los workers hacia el usuario.
- Texto libre dentro de los artifacts de sesión.
- Reportes de retorno entre worker y orquestador.
- Entradas de `SESSION_LOG.md` y `HARNESS_REPORT.md`.

## Principio central

> Sustancia técnica intacta. Relleno muere.

## Activación

CAVEMAN se activa mediante la feature flag `caveman` en `.agents/features.toml` o vía la variable de entorno `AGENTS_FEATURE_CAVEMAN`.

Cuando la flag está desactivada, el protocolo usa su estilo de comunicación base (sin CAVEMAN).

## Niveles

| Nivel | Descripción | Cuándo usar |
|---|---|---|
| **lite** | Sin relleno ni dudas. Mantiene artículos y oraciones completas. Profesional pero justo. | Comunicación formal con el usuario o documentación que debe ser fácil de leer. |
| **full** | Saca artículos de más, fragmentos OK, sinónimos cortos. CAVEMAN clásico en criollo. | Default. Artifactos, reportes internos y mensajes al usuario. |
| **ultra** | Abrevia todo (DB/auth/config/req/res/fn/impl), sin conjunciones, flechas para causalidad (X → Y), una palabra cuando alcanza. | Resúmenes, logs densos, mensajes donde el contexto ya es claro. |

El nivel default es **full**. El orquestador puede pasar otro nivel en el payload de delegación al worker.

## Reglas

### 1. Sacar lo que no suma

- Artículos de más (`el/la/los/las`) cuando no aportan claridad.
- Relleno: `che`, `mira`, `fijate`, `capaz`, `tipo`, `onda`, `básicamente`, `realmente`, `en realidad`.
- Cortesías: `con gusto`, `de nada`, `servido`, `por supuesto`, `un placer`.
- Dudas verbales: `probablemente`, `tal vez`, `posiblemente`, `parece ser`, `quizás`, `creo que`.

### 2. Usar sinónimos cortos

- `arreglá` en vez de `implementá una solución para`.
- `revisá` en vez de `realizá una revisión de`.
- `chequeá` en vez de `verificá la correctitud de`.
- `borrá` en vez de `eliminá de forma permanente`.

### 3. Mantener términos técnicos exactos

No abreviar nombres propios del proyecto ni términos que pierdan significado. Ejemplos de términos que se mantienen intactos:

- `TASK_ANALYSIS.md`, `EXECUTION_PLAN.md`
- `orchestrator`, `worker`, `harness`
- nombres de archivos, rutas, funciones, variables y errores

### 4. No tocar bloques de código

Los bloques de código, YAML, JSON, SQL y comandos de terminal se dejan tal cual. CAVEMAN aplica al texto que los rodea, no a su contenido.

### 5. Citar errores exactos

Cuando se reporta un error, se copia el mensaje o traceback exacto. No se parafrasea.

### 6. Patrón sugerido

```text
[cosa] [acción] [razón]. [siguiente paso].
```

Ejemplo:

> Bug en middleware de auth. Chequeo de token usa `<` no `<=`. Arreglá:
>
> ```python
> if expires_at <= now:
> ```

## Ejemplos por nivel

### Solicitud de clarificación

- **lite**: "Necesito saber si querés persistir el token en la base de datos o solo en memoria."
- **full**: "¿Token en DB o en memoria?"
- **ultra**: "Token → DB? memoria?"

### Reporte de artifact generado

- **lite**: "El artifact `02-CONTEXT_ARTIFACT.md` fue generado correctamente en la iteración actual."
- **full**: "Artifact `02-CONTEXT_ARTIFACT.md` generado. Listo para validación."
- **ultra**: "`02-CONTEXT_ARTIFACT.md` → OK."

### Descripción de un plan

- **lite**: "El plan consiste en agregar el campo `email` al schema de usuario, crear la migración correspondiente y actualizar el endpoint POST /users."
- **full**: "Plan: agregar `email` al schema, migrar DB, actualizar POST /users."
- **ultra**: "Schema +email → migración → POST /users."

### Reflejo de intención

- **lite**: "Entendí que querés un microservicio en Flask con CRUD de usuarios, persistiendo en SQLite. ¿Confirmás?"
- **full**: "Microservicio Flask + CRUD usuarios + SQLite. ¿OK?"
- **ultra**: "Flask CRUD users SQLite → confirm?"

## Excepciones de claridad

Dejar CAVEMAN (o volver a un registro más claro) para:

1. Warnings de seguridad.
2. Confirmaciones de acciones irreversibles.
3. Secuencias multi-paso donde el orden de fragmentos se pueda leer mal.
4. Cuando el usuario pide explicitamente clarificar o repetir algo.

Después de la parte clara, se vuelve a CAVEMAN.

Ejemplo:

> **Warning:** Esto borra permanentemente todas las filas de `users` y no se puede deshacer.
>
> ```sql
> DROP TABLE users;
> ```
>
> Verificá backup primero. Seguimos con caveman.

## Aplicación a contratos de artifacts

Todos los contratos de artifacts en `.agents/contracts/` siguen este estándar cuando la feature flag `caveman` está habilitada. Las secciones de texto libre de los artifacts deben escribirse en el nivel indicado; los bloques YAML, JSON y código deben permanecer intactos.

## Aplicación por tipo de comunicación

### User-facing (orquestador / worker hablando con el usuario)

Usar **full** por defecto. Cambiar a **lite** si el usuario lo pide o si el contexto es formal. Usar **ultra** solo cuando el usuario ya conoce el contexto.

Esto incluye el resumen final que el agente entrega al usuario al completar una tarea: debe ser corto, conciso y sin información extra fuera del scope solicitado.

### Artifacts de sesión

Usar **full** para las secciones de texto libre. Los bloques YAML/JSON/code quedan intactos.

### Reporte de retorno del worker al orquestador

Usar **full** o **ultra** según la complejidad. Ejemplo:

```text
Artifact generado: 05-EXECUTION_SUMMARY.md.
Cambios: app/schemas/user.py, app/routes/users.py.
Próximo estado: VERIFYING.
Blockers: ninguno.
```

### Logs de sesión y harness

Usar **ultra** para maximizar densidad de información:

```text
H01 → PASS | 12ms | TASK_SPECIFICATION.md OK
```

## Límites

- CAVEMAN no aplica a código fuente, commits, nombres de variables ni PRs del proyecto de usuario.
- CAVEMAN no justifica ambigüedad. Si una frase caveman puede interpretarse de dos formas, se reescribe con más claridad (aunque use más palabras).
- CAVEMAN no reemplaza a otros estándares (`EARS.md`, `RUBRICS.md`, `CONTEXT.md`). Los artifacts deben cumplir todos los estándares aplicables.
