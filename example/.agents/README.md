# Agentes Especializados de `pay_back`

Este directorio contiene la configuración, contratos y contexto para los agentes de IA que operan sobre el proyecto `pay_back`.

## Estructura

```
.agents/
├── README.md                          # Este archivo
└── roles/
    ├── _common/                       # Módulos compartidos (no son monolitos)
    │   ├── COMMUNICATION_RULES.md
    │   ├── OPERATIONAL_RULES.md
    │   ├── EXECUTION_CONTEXTS.md
    │   ├── ARCHITECTURE_PRINCIPLES.md
    │   ├── ARCHITECTURE_LAYERS.md
    │   ├── ARCHITECTURE_DOMAIN.md
    │   ├── ARCHITECTURE_NAMING.md
    │   ├── ARCHITECTURE_PROHIBITIONS.md
    │   ├── PREFLIGHT_CHECKLIST.md
    │   ├── DOMAIN_OVERVIEW.md
    │   └── OUTPUT_EFFICIENCY.md
    ├── backend_python/
    │   ├── ROLE.md
    │   ├── PROMPT.md
    │   └── MUST_READ.md
    ├── database_mysql/
    │   ├── ROLE.md
    │   ├── PROMPT.md
    │   └── MUST_READ.md
    ├── integration_specialist/
    │   ├── ROLE.md
    │   ├── PROMPT.md
    │   └── MUST_READ.md
    ├── qa_engineer/
    │   ├── ROLE.md
    │   ├── PROMPT.md
    │   ├── MUST_READ.md
    │   └── TESTING_RULES.md
    ├── tech_writer/
    │   ├── ROLE.md
    │   ├── PROMPT.md
    │   └── MUST_READ.md
    ├── func_writer/
    │   ├── ROLE.md
    │   ├── PROMPT.md
    │   ├── MUST_READ.md
    │   └── DOMAIN_CHEATSHEET.md
    └── coordinator/
        ├── ROLE.md
        ├── PROMPT.md
        ├── MUST_READ.md
        ├── ORCHESTRATION_GUIDE.md
        └── CONTEXT_ENGINEER.md
```

## Convención de archivos por rol

Cada subdirectorio de `roles/` contiene:

| Archivo | Propósito |
|---------|-----------|
| `ROLE.md` | Perfil, responsabilidades y restricciones del agente. |
| `PROMPT.md` | Plantilla de prompt optimizada para este rol. El orquestador la usa como base al delegar. |
| `MUST_READ.md` | Lista de archivos obligatorios vs. opcionales, con resumen de secciones críticas y qué **no** debe leer. |
| `*.md` adicionales | Material específico (cheatsheets, reglas de testing, guías de orquestación, compresión de contexto). |

## Regla de oro

> **Ningún agente debe leer información que no le compete.**
>
> El Orquestador (`coordinator`) es responsable de inyectar en cada prompt únicamente los archivos que el agente destinatario necesita para cumplir su tarea.
>
> Los módulos en `_common/` están modularizados por tema (operacional, capas, dominio, naming, checklist) para que cada rol consuma solo los que su `MUST_READ.md` indique.

## Portabilidad entre IAs

Esta estructura está diseñada para ser usable por diferentes sistemas de agentes (Kimi, Claude, etc.). Cada carpeta de rol es **self-contained** en su configuración, y no depende de herramientas propietarias.
