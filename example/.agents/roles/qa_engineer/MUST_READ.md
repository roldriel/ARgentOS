# Lecturas Obligatorias — QA & Testing Engineer

## Obligatorio antes de cualquier tarea

| Archivo | Motivo |
|---------|--------|
| `roles/_common/OPERATIONAL_RULES.md` | Límites operacionales; §3 Tooling Restrictions — no ejecutar pytest salvo instrucción. |
| `roles/_common/ARCHITECTURE_PRINCIPLES.md` | Fundamentos de organización por dominio. |
| `roles/_common/ARCHITECTURE_LAYERS.md` | Capas y reglas de dependencias (para mockear correctamente). |
| `roles/_common/ARCHITECTURE_DOMAIN.md` | Excepciones de dominio y reglas monetarias. |
| `roles/_common/ARCHITECTURE_NAMING.md` | Convenciones de nombres (para validar que el código bajo test las respeta). |
| `roles/_common/ARCHITECTURE_PROHIBITIONS.md` | Prohibiciones y auto-verificación. |
| `roles/_common/PREFLIGHT_CHECKLIST.md` | Checklist pre-vuelo. |
| `roles/_common/DOMAIN_OVERVIEW.md` | Estados, transiciones y flujos críticos de dinero. |
| `roles/_common/COMMUNICATION_RULES.md` | Estilo técnico y neutro. |
| `roles/qa_engineer/TESTING_RULES.md` | Alcance, patrones de mock y cobertura mínima. |

## Opcional / Contextual

- Archivos de producción que serán objeto de testing.
- `pytest.ini` para conocer configuración de tests.

## NO leer salvo instrucción explícita

- Detalles de implementación interna de providers que no alteren la interfaz pública a testear.
- Documentación de operaciones o manuales de usuario.
