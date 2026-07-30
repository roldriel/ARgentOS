---
title: "Plan de implementación — Discovery Orchestrator: Environment worker"
version: "1.0.0"
created_at: "2026-07-21"
author: "ARgentOS Orchestrator"
status: "approved"
parent_plan: "plans/PLAN_DISCOVERY_ORCHESTRATOR.md"
depends_on: ["plans/PLAN_DISCOVERY_ORCHESTRATOR_01_CONTRACTS.md", "plans/PLAN_DISCOVERY_ORCHESTRATOR_02_EXECUTION.md"]
---

# Plan 03: Environment worker

## Objetivo

Definir el role y el procedimiento del `environment_worker`, el worker del Discovery Orchestrator encargado de detectar el entorno de ejecución de forma segura y portable.

## Alcance

- Crear `.agents/roles/discovery_workers/environment_worker.md`.
- Actualizar/crear `.agents/standards/context/ENVIRONMENT_PROBE.md`.
- Definir comandos por sistema operativo.
- Definir detección de shell real.
- Definir reglas de filtrado de secrets e información sensible.
- No implementar otros workers en este paso.

## Entrada del worker

```json
{
  "message_version": "1.0.0",
  "from_worker": "discovery_orchestrator",
  "to_worker": "environment_worker",
  "payload_type": "discovery_input",
  "payload": {
    "project_root": "/path/to/project",
    "scope": "env",
    "previous_environment_md": "..." // opcional
  }
}
```

## Salida del worker

```json
{
  "message_version": "1.0.0",
  "from_worker": "environment_worker",
  "to_worker": "discovery_orchestrator",
  "payload_type": "partial_output",
  "payload": {
    "environment.md": "..."
  },
  "provenance": {
    "source_files": ["system_probe"],
    "source_sessions": [],
    "confidence": "high"
  }
}
```

## Sistemas operativos soportados

- Windows 10/11
- Linux (distros comunes)
- macOS

## Comandos de detección por SO

### Windows

| Sección | Comandos |
|---------|----------|
| OS | `ver` o `powershell -Command "(Get-CimInstance Win32_OperatingSystem).Caption"` |
| Arquitectura | `powershell -Command "(Get-CimInstance Win32_OperatingSystem).OSArchitecture"` |
| Shell | `powershell -Command "$PSVersionTable.PSVersion"` + `$SHELL` si es Git Bash |
| Python | `where python`, `python --version` |
| Git | `git --version` |
| Node | `where node`, `node --version` |
| Docker | `where docker`, `docker --version` |
| Otros | `where npm yarn uv poetry cargo go make` |

### Linux / macOS

| Sección | Comandos |
|---------|----------|
| OS | `uname -a` |
| Arquitectura | `uname -m` |
| Shell | `echo $SHELL` y `$SHELL --version` |
| Python | `which python python3`, `python3 --version` |
| Git | `git --version` |
| Node | `which node`, `node --version` |
| Docker | `which docker`, `docker --version` |
| Otros | `which npm yarn uv poetry cargo go make pip pip3` |

## Detección del shell real

El shell real puede ser diferente del shell por defecto del sistema. El `environment_worker` debe:

1. Detectar el shell del proceso padre si es posible.
2. En Windows, identificar si el comando se ejecuta desde Git Bash, PowerShell o CMD.
3. En Kimi Code CLI, el shell por defecto en Windows suele ser Git Bash.
4. Registrar `primary_shell` y `fallback_shell`.

## Herramientas a detectar

Obligatorias: `python` / `python3`, `git`.
Opcionales: `node`, `npm`, `yarn`, `pnpm`, `docker`, `uv`, `poetry`, `pip`, `cargo`, `go`, `make`.

## Variables de entorno

### Reglas

- Solo documentar variables relevantes para la ejecución del agente.
- **Nunca incluir el valor** de la variable, solo indicar `present` / `absent`.
- Filtrar strings sensibles: `TOKEN`, `KEY`, `SECRET`, `PASSWORD`, `CRED`, `AUTH`, `PRIVATE`.
- Anonimizar paths personales si es posible.

## Timeouts

- Cada comando: 5 segundos.
- Si un comando falla, continuar con el siguiente.
- Registrar el fallo en `## Notes`.

## Reglas de seguridad

1. Solo comandos de lectura.
2. No instalar ni actualizar herramientas.
3. No modificar archivos del sistema.
4. No ejecutar scripts del proyecto.
5. Filtrar secrets y paths sensibles antes de escribir `environment.md`.

## Formato de salida

La salida debe cumplir `.agents/contracts/ENVIRONMENT_DISCOVERY.md`.

Ejemplo resumido:

```markdown
## Operating System
- **os**: Windows
- **version**: "11"
- **architecture**: AMD64

## Shell
- **primary_shell**: Git Bash
- **fallback_shell**: PowerShell 7

## Python Runtime
- **version**: 3.11.4
- **executable**: `C:\Python311\python.exe`
- **package_manager**: pip

## Available Tools
- **docker**: not available
- **node**: 20.10.0
- **npm**: 10.2.3
- **git**: 2.42.0

## Execution Recommendations
- Usar Git Bash para comandos shell.
- Python está disponible en `C:\Python311\python.exe`.
- No usar Docker; no está instalado.
```

## Fases de implementación

### Fase 1: Definir comandos

1. Escribir `.agents/standards/context/ENVIRONMENT_PROBE.md`.
2. Documentar comandos por SO, herramientas, timeouts.

### Fase 2: Definir reglas de seguridad

1. Lista de strings prohibidos.
2. Reglas de anonimización de paths.
3. Reglas de variables de entorno.

### Fase 3: Crear el role

1. Escribir `.agents/roles/discovery_workers/environment_worker.md`.
2. Integrar los comandos y reglas de seguridad.

### Fase 4: Verificar

1. Generar `environment.md` en Windows y Linux.
2. Verificar que no contenga secrets.

## Criterios de éxito

| # | Criterio | Cómo verificar |
|---|----------|----------------|
| 1 | Existe `.agents/roles/discovery_workers/environment_worker.md`. | `ls` |
| 2 | Existe `.agents/standards/context/ENVIRONMENT_PROBE.md`. | `ls` |
| 3 | El worker ejecuta solo comandos de lectura. | Revisar el role. |
| 4 | `environment.md` no contiene secrets. | Buscar strings prohibidos. |
| 5 | `environment.md` detecta shell real en Windows. | Generar en Windows y leer. |
| 6 | Los timeouts están definidos. | Revisar el role. |

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| `systeminfo` en Windows es lento | No usar `systeminfo`; usar `ver` o `Get-CimInstance` con timeout. |
| `which` no existe en Windows | Usar `where` en Windows; `which` solo en Unix. |
| Paths personales filtrados | Anonimizar o omitir. |
| Variables de entorno sensibles | Solo documentar presencia/ausencia; nunca valores. |
| Comandos de shell inseguros | Whitelist de comandos permitidos. |
