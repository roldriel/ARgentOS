# Lecturas Obligatorias — Functional Documentation Writer

## Obligatorio antes de cualquier tarea

| Archivo | Motivo |
|---------|--------|
| `roles/_common/DOMAIN_OVERVIEW.md` | Fuente primaria de verdad del dominio de negocio. |
| `roles/func_writer/DOMAIN_CHEATSHEET.md` | Resumen ejecutivo de estados, transiciones y reglas. |
| `roles/_common/COMMUNICATION_RULES.md` | Estilo técnico y neutro. |

## Opcional / Contextual

| Archivo | Motivo |
|---------|--------|
| `roles/_common/ARCHITECTURE_PRINCIPLES.md` | Entender la organización por dominio para navegar el código cuando sea necesario validar información. |
| `src/apps/preorder/models/preorder.py` | Validar descripciones contra la implementación. |
| `src/apps/preorder/models/preorder_status.py` | Validar transiciones de estado. |
| `src/apps/callback/services/payment_closure.py` | Validar flujos de cierre. |

## NO leer salvo instrucción explícita

- `roles/_common/PREFLIGHT_CHECKLIST.md` técnico.
- Reglas de tooling y ejecución.
- Detalles de arquitectura de capas que no impacten la descripción funcional.
