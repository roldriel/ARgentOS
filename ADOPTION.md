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
  `git subtree pull --prefix=. <url> v1.0.0 --squash`.

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

Requisito de entorno: Python 3.11+ disponible como `python` (el harness usa
`tomllib`, de la stdlib). No hay dependencias externas para la verificación de
salud del protocolo; `pytest` solo se necesita para correr la suite de tests
del harness.

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
4. **Nada de IDE**: el protocolo no requiere configuración de IDE ni de
   herramientas externas; cualquier agente que lea `AGENTS.md` puede operarlo.

## 3. Validación inicial

En este orden, desde la raíz del proyecto:

```bash
python .agents/harness/health_check.py
python -m pytest .agents/harness/tests/
```

- La **verificación de salud** es la primera comprobación: la checklist de
  `.agents/standards/runtime/PROTOCOL_HEALTH.md` confirma que la estructura del
  protocolo quedó íntegra (directorios requeridos, archivos índice, front matter
  de contratos, rubrics, KB, estándares de prácticas técnicas) y la sonda de
  `health_check.py` confirma que `.project/` es escribible. Debe terminar en
  `PASS`.
- La **suite de tests** valida el harness completo. Debe terminar en verde.

Si ambas pasan, el protocolo está operativo. La primera sesión real arranca
dándole al agente la instrucción de leer `AGENTS.md`.

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
7. `.agents/harness/INDEX.md` — triggers del harness, runner, verificación de
   salud, recovery.

## 5. Qué NO forma parte de la adopción

- No se adopta `plans/` ni las RFCs: son el proceso de diseño del protocolo, no
  el protocolo.
- No se adopta `example/` ni `dev/` (`dev/tools/`, `dev/runtime/`): son bancos
  de prueba y herramientas del desarrollo.
- No hay soporte de múltiples versiones en paralelo: se adopta una versión y se
  migra siguiendo `MIGRATION.md`.

## 6. Modos de enforcement: declarativo (default) y enforced

El protocolo funciona en dos modos explícitos, sin zona gris:

- **Declarativo (default):** los gates del harness los invoca el orquestador
  por disciplina de prompt. Nada bloquea al agente si se los salta; el
  cumplimiento se audita post-hoc en `HARNESS_REPORT.md`. Es el modo activo
  cuando no hay hooks instalados (o el CLI no soporta hooks bloqueantes). El
  runner escribe igualmente `.project/<sesión>/<iteración>/state.json` en cada
  gate PASS: es inofensivo en este modo y habilita la auditoría post-hoc y el
  paso a enforced sin cambios de protocolo.
- **Enforced:** los gates críticos los impone el entorno. Un hook compartido
  (`python .agents/harness/hook_gate.py`, stdlib pura) lee el evento del CLI
  por stdin y bloquea (exit 2) dos situaciones: `PreToolUse` sobre
  `Write`/`Edit` a un deliverable del proyecto sin gate H04 (plan aprobado)
  PASS en `state.json`, y `Stop` sin cierre de iteración (sin H06 PASS ni
  `NEEDS_CLARIFICATION` registrado). El deny incluye la instrucción exacta de
  recuperación (el comando `runner.py` del gate faltante).

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
edite configs fuera de sesión. Mitigaciones en capas: script stdlib sin
dependencias con timeout corto, sonda que verifica escritura/lectura de
`state.json`, y detección post-hoc del runner (alerta en `HARNESS_REPORT.md`
cuando aparecen archivos modificados antes del PASS del gate de plan). Si el
entorno no tolera ese límite, quedarse en modo declarativo es igual de válido
— pero debe declararse como tal.
