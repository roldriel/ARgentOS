# Propuesta: mecanismo de skills con references/ lazy-loaded

Fecha: 2026-07-24
Estado: implementada (ver `.agents/skills/`, `.agents/standards/orchestration/SKILLS.md` y RFC-00XX `plans/rfc/00-skill-capability-model.md`)
Origen: análisis cruzado con `example/` (proyecto BeaconRBX), punto 3.

## Objetivo

Incorporar a ARgentOS el formato *skill* como unidad de capacidad reutilizable:
un procedimiento acotado, con entrada y salida, empaquetado como `SKILL.md` +
`references/` de carga perezosa, activable por tarea, en dos niveles
(protocolo y proyecto), sin inflar el contexto ni el núcleo del protocolo.

Problema que resuelve: hoy las capacidades del protocolo se expresan como
estándares globales por flag (reglas ambientales, todo o nada) o perfiles de
worker (rol/conducta, conocimiento monolítico). No existe una unidad de
*procedimiento* que el orchestrator active según la tarea y cuyo conocimiento
denso se pague solo cuando se usa.

---

## Decisiones cerradas (7)

### D1. Definición y frontera con perfiles

- **Perfil** = rol/conducta persistente durante la fase (`backend_engineer`,
  `qa_engineer`, etc.). Define *quién* es el worker.
- **Skill** = procedimiento acotado con entrada y salida
  (suggest-conventional-commit, memory, migración de DB, release SemVer).
  Define *qué capacidad puntual* ejecuta.
- Un worker puede tener un perfil y cero o más skills activos; son
  ortogonales, no compiten.

### D2. Activación: lógica A con un toque de B

- **A (determinista)**: tabla declarativa de activación, auditable, mantenida
  en el índice de skills. Su eje de clasificación NO es una tipología de
  tareas nueva: usa decisiones que el orchestrator ya toma — **fase del
  workflow + perfil seleccionado** (ej. `06-execute` + `database_engineer`
  → skill migración-db), igual que `ORCHESTRATION_GUIDE.md` guía la elección
  de `profile`. Así la tabla queda anclada a la mecánica existente y no
  introduce una taxonomía paralela que mantener.
- **Toque de B (juicio)**: el orchestrator puede activar un skill fuera de la
  tabla si la `description` del frontmatter lo justifica, y debe registrar la
  activación (y su motivo) en `SESSION_LOG.md`.
- El orchestrator selecciona skills durante `ANALYZING_TASK`/`PLANNING`, igual
  que hoy selecciona `profile` y `knowledge_entries`, y los pasa en un campo
  nuevo `skills: [...]` del payload de delegación.
- **Sin feature flag**: el mecanismo de skills no se gobierna por flag en
  `features.toml`. A diferencia de los estándares ambientales (que inyectan
  reglas globales por el solo hecho de estar activos), un skill no activado
  no inyecta contexto ni conducta: su costo en reposo es cero. La tabla de
  activación (D2-A) cumple el rol de compuerta que el flag cumple para los
  estándares; agregar un flag sería una segunda compuerta sobre una capacidad
  que ya está apagada por defecto.

### D3. Dos niveles de ubicación

- **Skills del protocolo**: `.agents/skills/<nombre>/` — generales, genéricos,
  inmutables como el resto de `.agents/`.
- **Skills del proyecto**: `.project/skills/<nombre>/` — específicos del
  proyecto, persistentes junto a `knowledge/` (NO dentro de
  `<session-uuid>/`: un skill no es un artefacto de sesión).
- **Precedencia**: si un skill de proyecto y uno del protocolo tienen el mismo
  nombre, gana el del proyecto (la especificidad vence; es la única vía de
  "patchear" el protocolo sin violar la inmutabilidad de `.agents/`).

### D4. Validación híbrida por nivel

- **Protocolo**: validación ligera, SIN entrar a `PROTOCOL_TAXONOMY.md`.
  Índice propio `.agents/skills/INDEX.md` + un test estructural simple en la
  suite existente: todo skill del índice existe, tiene frontmatter con
  `name`/`description`, y sus `references/` citadas existen en disco.
  (~30 líneas de test; no es un validador nuevo del harness.)
- **Proyecto**: puramente declarativos. Ningún test de `.agents/` puede
  validarlos (viven fuera del repo del protocolo). La validación es en
  runtime: si el orchestrator delega un skill inexistente o mal formado, el
  worker lo reporta como desviación en `SESSION_LOG.md`.
- Razón para no usar taxonomía completa: la taxonomía modela el *flujo*
  (estados, artefactos, triggers); un skill mal formado degrada una fase, no
  rompe la máquina. Mismo riesgo que un estándar mal escrito → mismo régimen.
  Si los skills se vuelven centrales, subir de régimen es incremental; bajar
  es costoso. Empezar liviano.
- **Cierre del hueco de fallo silencioso (nivel proyecto)**: el health-check
  del ArgentOS System Agent (`.agents/harness/health_check.py`) se extiende
  para validar estructuralmente `.project/skills/` **si la carpeta existe**:
  cada skill tiene `SKILL.md` con frontmatter `name`/`description`, y sus
  `references/` citadas existen. Skill inválido → warning en el reporte de
  health y exclusión de la tabla de activación para esa sesión. Es la misma
  validación estructural del nivel protocolo reutilizada en runtime, como
  extensión del health-check existente (no un validador nuevo del harness) y
  no bloqueante: no aborta la sesión, pero el error se detecta al inicio y no
  en medio de una fase.

### D5. Formato único, enforcement distinto

Mismo contrato en ambos niveles (el formato es obligatorio: la activación D2
depende de `name` + `description`; sin frontmatter el skill es invisible):

```
<skills-root>/<nombre>/
├── SKILL.md          # frontmatter: name, description, when_to_activate, when_not
│                     # cuerpo: workflow, reglas de seguridad, formato de salida,
│                     # tabla "si necesitás X, leé references/Y.md"
└── references/       # opcional; material denso de carga perezosa
```

- Protocolo: exigido por el test estructural (D4).
- Proyecto: exigido por convención documentada; skill mal formado = skill
  muerto (el orchestrator no lo activa) + desviación registrada.
- Documentación en dos lugares, por audiencia:
  - Norma formal en `PROTOCOL_BOUNDARIES.md` (o el doc de fronteras vigente).
  - `README.md` **in situ** en `.project/skills/`, para que cualquier agente
    LLM que descubra la carpeta explorando encuentre las instrucciones ahí
    mismo (mismo principio que el `AGENTS.md` raíz).

### D6. Coexistencia con skills externos del usuario

Hecho: el protocolo NO puede pausarlos técnicamente (los inyecta el CLI del
LLM). La solución es normativa. Distinción clave: **herramienta vs. regla**.

- Los skills externos funcionan como **herramientas**: un worker puede
  usarlos dentro de su fase si su efecto queda dentro de las fronteras del
  protocolo.
- **Nunca** funcionan como regla: si un skill externo define formato, conducta
  o flujo que contradice al protocolo, el protocolo gana.
- Tres riesgos y sus reglas:
  1. **Colisión de conducta** (ej. skill `caveman` de usuario vs. estándar
     `CAVEMAN.md` + flag): gana el estándar del protocolo en todo lo que el
     protocolo produce. La charla directa usuario-agente fuera de artefactos
     sigue las preferencias del usuario.
  2. **Colisión de efectos** (skill que escribe fuera de las rutas permitidas,
     ej. una memoria en `~/.agents/`): prohibido durante sesiones ARgentOS;
     la memoria del protocolo vive en `.project/`.
  3. **Colisión de trazabilidad** (uso invisible de un skill externo): el uso
     se registra en `EXECUTION_SUMMARY.md` o `SESSION_LOG.md`.
- Documentado como sección "Skill coexistence" en el documento de fronteras.
  Sin listas negras ni detección: sería fingir un control que el protocolo no
  tiene; `ANTI_CIRCUMVENTION.md` ya cubre el abuso desde la conducta.

### D7. Jerarquía de autoridad

```
1. Instrucción explícita del usuario (en la conversación, presente)
2. Protocolo ARgentOS (.agents/, sus estándares y flags)
3. Skills del proyecto (.project/skills/)
4. Skills del protocolo (.agents/skills/)
5. Skills externos del usuario (instalados en su CLI)
```

- Un skill no es fuente de autoridad, es contexto inyectado: **describe una
  capacidad, no otorga permisos**. "Siempre podés X" (skill) vs. "nunca X"
  (protocolo) → gana el protocolo, y el intento de invocar el skill como
  autorización se registra como desviación (`ANTI_CIRCUMVENTION.md`).
- Un skill instalado NO es una instrucción directa del usuario: es contexto
  instalado una vez. Tratarlo como voz del usuario sería dejar que una
  decisión vieja pise la voluntad actual.
- Resolución de conflictos declarada, nunca silenciosa: "este skill sugiere
  X, pero el protocolo lo prohíbe; sigo el protocolo".

---

## Cambios concretos (si se aprueba)

### Nuevos

1. `.agents/skills/INDEX.md` — índice + tabla de activación (D2-A).
2. `.agents/skills/README.md` — contrato del formato skill (D5) para skills
   del protocolo.
3. `.agents/standards/orchestration/SKILLS.md` (o sección en el guide) —
   mecánica de activación, precedencia, coexistencia (D2, D3, D6, D7).
4. Test estructural en `.agents/harness/tests/` para skills del protocolo
   (D4).
5. `.project/skills/README.md` — documentación in situ para el nivel proyecto
   (D5). Se crea con la primera sesión que use skills de proyecto.

### Modificados

6. `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` — campo `skills: [...]`
   en el payload (D2).
   > **Excepción declarada a la inmutabilidad de contratos**: este cambio
   > modifica un contrato, que es inmutable por defecto según
   > `PROTOCOL_BOUNDARIES.md`. Criterio aplicado: es un cambio **aditivo y
   > opcional** (campo nuevo que puede omitirse); no altera la semántica de
   > campos existentes ni rompe payloads previos. Queda documentado en esta
   > propuesta como la excepción acordada. Regla general que se establece con
   > este precedente: cambios aditivos-opcionales a contratos son aprobables
   > por propuesta documentada; cambios que alteran campos existentes
   > requieren versionado del contrato.
7. `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — nueva sección
   "Persistent project state" que reformula la Artifact Safety Rule para
   distinguir contenido efímero (`.project/<session-uuid>/<iteration>/`,
   regla vigente sin cambios) de contenido persistente entre sesiones, y
   regulariza las dos excepciones: `.project/knowledge/` (existente, hoy
   indocumentado en el doc de fronteras) y `.project/skills/` (nuevo, D3).
   Más la sección "Skill coexistence" (D6).
8. `.agents/orchestrators/core/roles/orchestrator.md` — responsabilidad de
   seleccionar skills y registrar activaciones fuera de tabla (D2).
9. `.agents/roles/worker.md` — cómo un worker consume un skill: leer SKILL.md
   al activarse, `references/` solo bajo demanda (D5).
10. `standards/INDEX.md` — entrada del nuevo estándar de skills.
11. `.agents/harness/health_check.py` — validación estructural de
    `.project/skills/` cuando la carpeta existe: warning + exclusión de la
    sesión para skills inválidos, no bloqueante (D4, cierre del hueco de
    fallo silencioso).

### Explícitamente fuera de alcance (primera iteración)

- Migrar perfiles o estándares existentes a formato skill.
- Skills concretos del protocolo (el de conventional-commit de `example/` es
  candidato natural para una segunda iteración, como piloto del mecanismo).
- Entidades `skill` en `PROTOCOL_TAXONOMY.md` (queda como opción futura si el
  mecanismo se vuelve central, ver D4).

## Esfuerzo estimado

| Cambio | Archivos | Esfuerzo |
| --- | --- | --- |
| Formato + índice + README (D5, índice D2) | 2-3 nuevos | Bajo |
| Estándar de activación/coexistencia (D2, D3, D6, D7) | 1 nuevo | Bajo-Medio |
| Test estructural (D4) | 1 nuevo + suite | Medio |
| Health-check de skills de proyecto (D4) | 1 editado (~20-30 líneas) | Bajo |
| Payload de delegación + roles (D2, D5) | 3 editados | Bajo |
| Fronteras + índices (D5, D6, regularización de `knowledge/`) | 2 editados | Bajo |

Orden sugerido: D5 formato → D4 test → D2 activación/payload → D3/D6/D7
fronteras y coexistencia → índices.

(El formato va primero porque el test, la activación y la documentación de
fronteras todos referencian el contrato del SKILL.md.)
