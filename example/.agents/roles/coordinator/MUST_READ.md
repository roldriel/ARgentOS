# Lecturas Obligatorias — Team Coordinator

## Obligatorio antes de cualquier tarea

El coordinador debe conocer **todos** los módulos comunes y los archivos de configuración de cada rol para poder inyectar el contexto correcto en cada prompt.

### Módulos comunes (obligatorios)

| Archivo | Motivo |
|---------|--------|
| `roles/_common/OPERATIONAL_RULES.md` | Debe entender todos los límites operacionales para no delegar tareas prohibidas. |
| `roles/_common/EXECUTION_CONTEXTS.md` | Para detectar errores de contexto en los entregables. |
| `roles/_common/ARCHITECTURE_PRINCIPLES.md` | Para validar diseños a alto nivel. |
| `roles/_common/ARCHITECTURE_LAYERS.md` | Para detectar violaciones de capas y dependencias. |
| `roles/_common/ARCHITECTURE_DOMAIN.md` | Para validar modelado de dominio y excepciones. |
| `roles/_common/ARCHITECTURE_NAMING.md` | Para validar nombres y documentación. |
| `roles/_common/ARCHITECTURE_PROHIBITIONS.md` | Para aplicar prohibiciones y auto-verificación. |
| `roles/_common/PREFLIGHT_CHECKLIST.md` | Para verificar mentalmente que los entregables cumplan el checklist. |
| `roles/_common/DOMAIN_OVERVIEW.md` | Para descomponer tareas de dominio correctamente. |
| `roles/_common/COMMUNICATION_RULES.md` | Para supervisar el estilo de salida de los subagentes. |

### Archivos de cada rol (obligatorios)

| Archivo | Motivo |
|---------|--------|
| `roles/backend_python/ROLE.md` | Saber qué puede/debe hacer el backend dev. |
| `roles/database_mysql/ROLE.md` | Saber qué puede/debe hacer el DB architect. |
| `roles/integration_specialist/ROLE.md` | Saber qué puede/debe hacer el integration specialist. |
| `roles/qa_engineer/ROLE.md` + `TESTING_RULES.md` | Saber alcance de testing. |
| `roles/tech_writer/ROLE.md` | Saber alcance de documentación técnica. |
| `roles/func_writer/ROLE.md` + `DOMAIN_CHEATSHEET.md` | Saber alcance de documentación funcional. |

### Guías de orquestación (obligatorias)

| Archivo | Motivo |
|---------|--------|
| `roles/coordinator/ORCHESTRATION_GUIDE.md` | Anexos A, B, C de orquestación rápida. |
| `roles/coordinator/CONTEXT_ENGINEER.md` | Técnicas de compresión de prompt y minimización de tokens antes de delegar. |

## NO delegar sin autorización explícita

- Cambios que violen los contratos arquitectónicos.
- Instalación de paquetes o modificación del entorno.
- Ejecución de `pytest` salvo que el usuario lo haya solicitado explícitamente.
