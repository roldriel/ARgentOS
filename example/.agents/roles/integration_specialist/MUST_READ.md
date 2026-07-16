# Lecturas Obligatorias — Integration Specialist

## Obligatorio antes de cualquier tarea

| Archivo | Motivo |
|---------|--------|
| `roles/_common/OPERATIONAL_RULES.md` | Límites operacionales; §9 External Interaction Safety es crítica. |
| `roles/_common/EXECUTION_CONTEXTS.md` | Contextos de ejecución y logging. |
| `roles/_common/ARCHITECTURE_LAYERS.md` | §5.6 Providers y §6 Dependency Rules. |
| `roles/_common/ARCHITECTURE_DOMAIN.md` | Traducción de errores a excepciones de dominio. |
| `roles/_common/ARCHITECTURE_NAMING.md` | Convenciones de nombres (§3.9 Provider Naming). |
| `roles/_common/ARCHITECTURE_PROHIBITIONS.md` | Prohibiciones y auto-verificación. |
| `roles/_common/PREFLIGHT_CHECKLIST.md` | Checklist pre-vuelo. |
| `roles/_common/DOMAIN_OVERVIEW.md` | Entender qué se integra y por qué (flujos de pago, callbacks). |
| `roles/_common/COMMUNICATION_RULES.md` | Estilo técnico y neutro. |

## Opcional / Contextual

- Providers existentes del mismo dominio (para seguir patrones de retry y auth).
- `apps/<domain>/exceptions.py` existente.

## NO leer salvo instrucción explícita

- Documentación de testing exhaustivo.
- Manuales funcionales para usuarios finales.
