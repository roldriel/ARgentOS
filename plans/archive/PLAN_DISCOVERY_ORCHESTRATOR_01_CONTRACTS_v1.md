---
title: "Plan de implementación — Discovery Orchestrator: Contratos y formato"
version: "1.0.0"
created_at: "2026-07-21"
author: "ARgentOS Orchestrator"
status: "approved"
parent_plan: "plans/PLAN_DISCOVERY_ORCHESTRATOR.md"
depends_on: []
---

# Plan 01: Contratos y formato

## Objetivo

Definir los contratos formales de los artefactos del Discovery Orchestrator, incluyendo entradas KB, manifest, mensajes entre workers y el contrato de entrada KB base. Separar claramente las responsabilidades de H10 (estructura) y H12 (ground truth).

## Alcance

- Crear/actualizar contratos de KB.
- Crear contrato de mensaje entre workers.
- Actualizar `.agents/contracts/KB_DISCOVERY_ENTRY.md` para soportar procedencia.
- Ajustar `.agents/harness/policies/H10-kb-discovery-report.md` para validación estructural.
- No implementar roles ni workflows en este paso.

## Contratos de KB

### 1. `.agents/contracts/DISCOVERY_MANIFEST.md`

Define el formato del manifest del KB acumulativo.

```markdown
# DISCOVERY_MANIFEST Contract

## Location

`.project/knowledge/discovery/.discovery_manifest`

## Format

TOML.

## Required sections

[knowledge_base]
- version: string
- generated_at: ISO 8601
- updated_at: ISO 8601
- ttl_hours: integer
- role_version: string
- task_scope: string
- project_root: string

[hashes]
- config_files_hash: string
- sample_files_hash: string
- environment_hash: string

[entries]
- active: list of strings
- stale: list of strings

[workers]
- invoked: list of strings
- completed: list of strings

[runtime]
- model_used: string (optional)
- execution_time_seconds: float (optional)
```

## Example

```toml
[knowledge_base]
version = "1.0.0"
generated_at = "2026-07-21T05:00:00Z"
updated_at = "2026-07-21T05:00:00Z"
ttl_hours = 24
role_version = "discovery_orchestrator:v1"
task_scope = "full"
project_root = "/home/user/project"

[hashes]
config_files_hash = "sha256:abc123..."
sample_files_hash = "sha256:def456..."
environment_hash = "sha256:ghi789..."

[entries]
active = [
  "stack.md",
  "dependencies.md",
  "environment.md",
  "development_patterns.md",
  ...
]
stale = [
  "old_feature.md"
]

[workers]
invoked = ["environment_worker", "stack_worker", "framework_worker", "patterns_worker", "business_worker", "synthesis_worker"]
completed = ["environment_worker", "stack_worker", ...]
```
```

### 2. `.agents/contracts/DEVELOPMENT_PATTERNS.md`

Igual que en el plan anterior, pero cada patrón debe incluir `source_workers` y `source_sessions`:

```markdown
### Pattern: spacing-between-blocks

- **Category**: formatting
- **Description**: Dejar una línea en blanco entre bloques `if` y `else` consecutivos.
- **Example**:
  ```python
  if user.is_active:
      process(user)

  else:
      log_warning("inactive")
  ```
- **Source files**: `src/main.py`, `src/services/user.py`
- **Source workers**: `patterns_worker`
- **Source sessions**: `session-68c54119`
- **Confidence**: high
- **Applies to**: Python
```

### 3. `.agents/contracts/ENVIRONMENT_DISCOVERY.md`

Mismo formato base que en el plan anterior. Se agrega `source_workers = ["environment_worker"]` y `source_sessions` si aplica.

### 4. `.agents/contracts/INTER_WORKER_MESSAGE.md` (nuevo)

Define el formato de los mensajes que los workers se pasan entre sí.

```markdown
# INTER_WORKER_MESSAGE Contract

## Purpose

Estandarizar la comunicación entre workers del Discovery Orchestrator.

## Format

JSON.

## Required fields

| Field | Type | Description |
|-------|------|-------------|
| `message_version` | string | "1.0.0" |
| `from_worker` | string | Worker emisor. |
| `to_worker` | string | Worker receptor. |
| `generated_at` | ISO 8601 | Timestamp. |
| `payload_type` | string | "discovery_input", "partial_output", "invalidation_request", etc. |
| `payload` | object | Contenido específico del mensaje. |
| `provenance` | object | `source_files`, `source_sessions`, `confidence`. |

## Example

```json
{
  "message_version": "1.0.0",
  "from_worker": "stack_worker",
  "to_worker": "framework_worker",
  "generated_at": "2026-07-21T05:00:00Z",
  "payload_type": "partial_output",
  "payload": {
    "languages": ["Python"],
    "frameworks": ["Flask"],
    "config_files": ["src/app.py"]
  },
  "provenance": {
    "source_files": ["src/app.py", "requirements.txt"],
    "source_sessions": [],
    "confidence": "high"
  }
}
```
```

## Archivos a modificar

### 5. `.agents/contracts/KB_DISCOVERY_ENTRY.md`

Agregar campos opcionales al frontmatter:

- `updated_at`: ISO 8601.
- `source_workers`: list of strings.
- `source_sessions`: list of strings.
- `status`: `active` o `stale`.
- `previous_versions`: list of references (opcional).

Documentar que `source_files` puede incluir `"system_probe"` para entradas de entorno.

### 6. `.agents/harness/policies/H10-kb-discovery-report.md`

Responsabilidad exclusiva: validación estructural.

Verificar:

- Todas las entradas KB existen y cumplen el contrato base.
- Los headers TOML son válidos.
- Los campos obligatorios están presentes.
- El manifest está completo.
- Cada patrón tiene `source_files`, `confidence`, `example`.
- `environment.md` y `development_patterns.md` existen.

**No verificar** que `source_files` sean rutas reales; eso es H12.

## Fases de implementación

### Fase 1: Crear contratos nuevos

1. `.agents/contracts/DISCOVERY_MANIFEST.md`
2. `.agents/contracts/DEVELOPMENT_PATTERNS.md`
3. `.agents/contracts/ENVIRONMENT_DISCOVERY.md`
4. `.agents/contracts/INTER_WORKER_MESSAGE.md`

### Fase 2: Actualizar contratos existentes

1. `.agents/contracts/KB_DISCOVERY_ENTRY.md`
2. `.agents/harness/policies/H10-kb-discovery-report.md`

### Fase 3: Verificar

1. Revisar que no haya ambigüedades.
2. Asegurar coherencia con Plan 02 y Plan 04.
3. Validar que H10 no se solape con H12.

## Criterios de éxito

| # | Criterio | Cómo verificar |
|---|----------|----------------|
| 1 | Los 4 contratos nuevos existen. | `ls` |
| 2 | `KB_DISCOVERY_ENTRY.md` soporta `updated_at`, `source_workers`, `source_sessions`, `status`. | Leer el archivo. |
| 3 | H10 solo valida estructura. | Leer H10; no debe mencionar ground truth. |
| 4 | `INTER_WORKER_MESSAGE.md` define campos obligatorios. | Leer el archivo. |
| 5 | `DISCOVERY_MANIFEST.md` soporta `active` y `stale` entries. | Leer el archivo. |

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Contratos demasiado rígidos | Usar campos opcionales y secciones flexibles. |
| H10 y H12 vuelven a solaparse | Documentar frontera en ambos planes; revisar cruzadamente. |
| `system_probe` genera confusión | Documentar que es fuente válida solo para entorno. |
| Inter-worker message es ambiguo | Incluir ejemplos de cada tipo de payload. |
