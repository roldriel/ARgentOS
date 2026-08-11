# Guía de adopción — Protocolo ARgentOS

Cómo adoptar el protocolo ARgentOS en otro proyecto. ARgentOS es un protocolo
**documental**: no se instala como paquete; adoptarlo es vendorizar el directorio
del protocolo y configurar lo mínimo (fuera de alcance declarado:
`plans/20-release-adoption.md` §Fuera de alcance). Origen de esta guía:
`plans/20-release-adoption.md` §B.

La versión adoptada queda declarada en `.agents/VERSION`. Para actualizaciones
posteriores, seguir §1.2 y [`MIGRATION.md`](MIGRATION.md).

---

## 1. Instalación

El repositorio publica la rama **`dist`**, que contiene únicamente `.agents/` y
`AGENTS.md` en su raíz — nada más del repo de desarrollo. Es el único punto de
consumo soportado. Hay dos métodos:

### 1.1. Git subtree (recomendado)

Vendoriza `dist` dentro del proyecto adoptante, con sincronización posterior por
`pull`:

```bash
# Instalación (una vez, desde la raíz del proyecto adoptante)
git subtree add --prefix=. https://github.com/roldriel/ARgentOS.git dist --squash

# Actualización a la última versión publicada
git subtree pull --prefix=. https://github.com/roldriel/ARgentOS.git dist --squash
```

- `--prefix=.` coloca `.agents/` y `AGENTS.md` en la raíz del proyecto (la
  estructura de `dist` ya viene así).
- El repo es privado: el `pull` usa las credenciales git habituales.
- **`.agents/` es read-only en el adoptante**: los cambios se hacen en el repo
  fuente (rama `dev` → `master` → CI publica en `dist`); el próximo
  `subtree pull` pisa cualquier edición local.
- Para pinearse a una versión en vez de seguir `dist`, usar el tag publicado:
  `git subtree pull --prefix=. <url> v3.0.1 --squash`.

### 1.2. Copia manual (alternativa sin git)

Copiar desde la rama `dist` del repositorio de origen al proyecto adoptante:

| Copiar | Destino | Obligatorio |
|---|---|---|
| `.agents/` (completo) | `<proyecto>/.agents/` | Sí |
| `AGENTS.md` (raíz) | `<proyecto>/AGENTS.md` | Sí |

Sin subtree no hay mecanismo de actualización: cada upgrade es una copia nueva
(seguir `MIGRATION.md` entre versiones).

No hace falta copiar nada más: `.agents/` es autocontenido y no referencia
`plans/` ni RFCs (frontera documental, `plans/INDEX.md` §Convenciones). Los
documentos de diseño (`plans/`, `feature.md`) son historia del desarrollo del
protocolo, no parte del producto adoptado. `CHANGELOG.md` y `MIGRATION.md`
conviene conservarlos como referencia de versionado, pero no son requeridos por
el runtime.

Requisitos de entorno, por modo de adopción (§6):

- **Modo declarativo (default): ninguno.** El protocolo es puro Markdown; los
  gates del harness los evalúa el orquestador por juicio contra las checklists
  de cada policy. No se necesita Python ni ninguna herramienta externa.
- **Modo enforced: Python 3.x disponible como `python`, stdlib pura** (sin
  `pip` ni dependencias externas). Solo tres scripts lo usan: `hook_gate.py`
  (hook del CLI), `runner_state.py` (registro transaccional de `state.json`)
  y `health_check.py` (sonda de almacenamiento de estado).
- `pytest` solo se necesita para **desarrollar el protocolo** (suite reducida
  de tests del harness en `.agents/harness/tests/`); no es un requisito de
  adopción.

## 2. Qué configurar

1. **`.gitignore` del proyecto**: agregar `.project/` (artefactos de sesión
   efímeros; el agente de sistema los crea solo). `.agents/` se versiona completo.
2. **`.agents/features.toml`**: revisar los flags. Defaults seguros: los flags
   (`rubrics`, `knowledge_base`, prácticas técnicas, flags declarativos)
   vienen habilitados y la checklist de salud del protocolo
   (`.agents/standards/runtime/PROTOCOL_HEALTH.md`) valida sus estándares;
   `architecture_contract` viene deshabilitado. Cada flag puede apagarse por
   variable de entorno `AGENTS_FEATURE_<FLAG>` sin editar el archivo.
3. **Artefactos de contexto del proyecto**: crear en la raíz del proyecto
   `project-map.md` y `technical-analysis.md` siguiendo el estándar
   `.agents/standards/context/PROJECT_ARTIFACTS.md` (plantillas en su §9). Si el
   proyecto tiene un dominio de negocio propio, usar además las plantillas de
   dominio del mismo §9 (overview + cheatsheet) para dar a los workers contexto
   funcional.
4. **Nada de IDE ni de runtime**: el protocolo no requiere configuración de
   IDE ni de herramientas externas; cualquier agente que lea `AGENTS.md` puede
   operarlo. En modo declarativo (§6) tampoco requiere Python.

## 3. Validación inicial

**Modo declarativo (sin Python):** la verificación es la checklist documental
de `.agents/standards/runtime/PROTOCOL_HEALTH.md`, que aplica el system agent
en el bootstrap de la primera sesión. Confirma que la estructura del protocolo
quedó íntegra (directorios requeridos, archivos índice, front matter de
contratos, rubrics, KB, estándares de prácticas técnicas). Debe terminar en
`PASS`.

**Modo enforced (con Python):** además de la checklist documental, la sonda
mecánica confirma que `.project/` es escribible:

```bash
python .agents/harness/health_check.py
```

**Solo para desarrollo del protocolo** (no hace falta en un proyecto
adoptante): la suite reducida de tests del harness —

```bash
python -m pytest .agents/harness/tests/
```

Si la verificación correspondiente a tu modo pasa, el protocolo está
operativo. La primera sesión real arranca dándole al agente la instrucción de
leer `AGENTS.md`.

## 4. Orden de lectura recomendado

Para entender el protocolo adoptado, en este orden:

1. `AGENTS.md` — puerta de entrada; declara el bootstrap y las fronteras.
2. `.agents/INDEX.md` — secuencia de bootstrap (system agent → máquina de
   estados → orquestador).
3. `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — fronteras: qué vive en
   `.agents/`, qué vive en `.project/`, inmutabilidad.
4. `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` — estados y
   transiciones del ciclo de una tarea.
5. `.agents/orchestrators/core/roles/orchestrator.md` — el rol que gobierna.
6. `.agents/standards/INDEX.md` — mapa de estándares (flags, EARS, rubrics,
   contexto, TDD).
7. `.agents/harness/INDEX.md` — triggers del harness, estado de protocolo y
   hooks, verificación de salud, recovery.

## 5. Qué NO forma parte de la adopción

- No se adopta `plans/` ni las RFCs: son el proceso de diseño del protocolo, no
  el protocolo.
- No se adopta `example/` ni `dev/` (`dev/tools/`, `dev/runtime/`): son bancos
  de prueba y herramientas del desarrollo.
- No hay soporte de múltiples versiones en paralelo: se adopta una versión y se
  migra siguiendo `MIGRATION.md`.

## 6. Modos de enforcement: declarativo (default) y enforced

El protocolo funciona en dos modos explícitos, sin zona gris:

- **Declarativo (default):** los gates del harness los evalúa el orquestador
  por juicio, contra la checklist en prosa de cada policy. Nada bloquea al
  agente si se los salta; el cumplimiento se audita post-hoc en
  `HARNESS_REPORT.md` (que escribe el propio orquestador). Es el modo activo
  cuando no hay hooks instalados (o el CLI no soporta hooks bloqueantes). Sin
  requisitos de entorno: no se necesita Python.
- **Enforced:** los gates críticos los impone el entorno. Un hook compartido
  (`python .agents/harness/hook_gate.py`, stdlib pura) lee el evento del CLI
  por stdin y bloquea (exit 2) dos situaciones: `PreToolUse` sobre
  `Write`/`Edit` a un deliverable del proyecto sin gate H04 (plan aprobado)
  PASS en `state.json`, y `Stop` sin cierre de iteración (sin H06 PASS ni
  `NEEDS_CLARIFICATION` registrado). El orquestador sigue evaluando cada gate
  en prosa; cuando el gate da PASS, registra el resultado con
  `python .agents/harness/runner_state.py --session <uuid> --trigger <HXX>
  --iteration <N> pass`, que es el único escritor de `state.json` (escritura
  transaccional, fail-closed). El deny del hook incluye la instrucción exacta
  de recuperación. Requisito: Python 3.x stdlib, sin `pip`.

### 6.1. Configuración enforced — Kimi Code

En `~/.kimi-code/config.toml` (o el config del proyecto):

```toml
[[hooks]]
event = "PreToolUse"
matcher = "Write|Edit"
command = "python .agents/harness/hook_gate.py"
timeout = 5

[[hooks]]
event = "Stop"
command = "python .agents/harness/hook_gate.py"
timeout = 5
```

### 6.2. Configuración enforced — Claude Code

En `.claude/settings.json` del proyecto (commiteable):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python .agents/harness/hook_gate.py", "timeout": 5 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python .agents/harness/hook_gate.py", "timeout": 5 }
        ]
      }
    ]
  }
}
```

La opción fuerte en Claude Code son las *managed settings*
(`allowManagedHooksOnly` y deny sobre `.agents/` y las configs de hooks),
gestionadas fuera del repo: impiden que el propio agente desactive el hook.

### 6.3. Límite honesto: los hooks son fail-open

Todo CLI evaluado es **fail-open** ante crash o timeout del hook: si
`hook_gate.py` falla, la tool call pasa libre. El modelo protege contra
*omisión del agente*, no contra el hook fallando ni contra un usuario que
edite configs fuera de sesión. Mitigaciones en capas: scripts stdlib sin
dependencias con timeout corto, sonda que verifica escritura/lectura de
`state.json`, y detección post-hoc de bypass (`runner_state.py` alerta al
registrar el PASS de H04 si aparecen archivos modificados antes de ese PASS).
Si el
entorno no tolera ese límite, quedarse en modo declarativo es igual de válido
— pero debe declararse como tal.
