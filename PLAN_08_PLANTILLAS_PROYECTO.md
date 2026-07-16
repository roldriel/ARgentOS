# Plan de Implementación 08 — Plantillas de Proyecto

> **Origen:** Punto 8 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Proveer plantillas reutilizables para acelerar la adopción del protocolo en nuevos proyectos.

---

## 1. Objetivo del plan

Crear un directorio `.agents/templates/` con:

1. `.agents/templates/claude-settings.json` — plantilla de configuración de permisos y herramientas para Claude.
2. `.agents/templates/domain-overview-template.md` — plantilla de resumen de dominio.
3. `.agents/templates/domain-cheatsheet-template.md` — plantilla de cheatsheet de dominio.

Además, actualizar `.agents/standards/INDEX.md` y crear un `README.md` en `.agents/templates/` que explique el uso de cada plantilla.

---

## 2. Alcance

### Incluido
- Extracción de `example/.claude/settings.local.json`.
- Extracción de `example/.agents/roles/func_writer/DOMINIO_CHEATSHEET.md` o equivalente.
- Creación de plantillas genéricas y reutilizables.
- Documentación de uso.
- Actualización del índice de estándares.

### Excluido
- No incluir archivos específicos del IDE del usuario en el core del protocolo.
- No generar configuraciones reales del proyecto actual.
- No modificar `.agents/` más allá de la creación del directorio `templates/`.

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/templates/README.md` | Guía de uso de plantillas. |
| `.agents/templates/claude-settings.json` | Plantilla de settings para Claude. |
| `.agents/templates/domain-overview-template.md` | Plantilla de resumen de dominio. |
| `.agents/templates/domain-cheatsheet-template.md` | Plantilla de cheatsheet de dominio. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/standards/INDEX.md` | Indexar plantillas. |
| `.agents/standards/runtime/IDE_CONFIGURATION.md` (opcional) | Documentar uso de plantilla de IDE. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/.claude/settings.local.json` | Fuente original de configuración. |
| `example/.agents/roles/func_writer/DOMINIO_CHEATSHEET.md` | Fuente de cheatsheet de dominio. |

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuentes
1. Leer `example/.claude/settings.local.json`.
2. Buscar en `example/` cualquier cheatsheet o template de dominio.
3. Identificar qué configuraciones son genéricas y cuáles específicas de proyecto.
4. Revisar `.agents/features.toml` para entender flags relevantes.

### Paso 2 — Diseño del directorio de plantillas
Estructura:

```
.agents/templates/
├── README.md
├── claude-settings.json
├── domain-overview-template.md
└── domain-cheatsheet-template.md
```

### Paso 3 — Creación de `README.md`
Contenido mínimo:
- Propósito del directorio.
- Cómo copiar y adaptar cada plantilla.
- Advertencia: no modificar archivos en `.agents/templates/` directamente; copiarlos al proyecto.
- Tabla de plantillas con descripción y destino sugerido.

### Paso 4 — Creación de `claude-settings.json`
A partir de `example/.claude/settings.local.json`, crear una plantilla genérica:

```json
{
  "permission": {
    "allow": {
      " tools": ["ReadFile", "WriteFile", "StrReplaceFile", "Shell", "Grep", "Glob"],
      "commands": ["python", "pytest", "git status", "git diff"]
    },
    "deny": {
      "commands": ["git push", "git reset", "git rebase", "rm -rf /"]
    }
  },
  "agents": {
    "must_read": [
      "AGENTS.md",
      ".agents/standards/conduct/OPERATIONAL_RULES.md"
    ]
  }
}
```

Notas:
- No incluir rutas absolutas ni nombres de proyecto.
- Incluir comentarios en campos que el usuario debe adaptar.
- Documentar que debe copiarse a `.claude/settings.local.json` del proyecto.

### Paso 5 — Creación de `domain-overview-template.md`
Estructura propuesta:

```markdown
# Domain Overview: <Nombre del dominio>

## 1. Propósito
## 2. Actores
## 3. Procesos principales
## 4. Entidades y relaciones
## 5. Reglas de negocio críticas
## 6. Eventos
## 7. Excepciones y errores
## 8. Glosario
## 9. Notas
```

Cada sección debe incluir instrucciones breves de qué incluir.

### Paso 6 — Creación de `domain-cheatsheet-template.md`
Estructura propuesta:

```markdown
# Domain Cheatsheet: <Nombre del dominio>

> Referencia rápida para workers. Mantener actualizado.

## Términos
| Término | Significado | Sinónimos |
|---------|-------------|-----------|
| | | |

## Reglas de oro
1. 
2. 
3. 

## Anti-patrones
- 

## Decisiones frecuentes
| Situación | Decisión estándar | Excepciones |
|-----------|-------------------|-------------|
| | | |

## Enlaces rápidos
- 
```

### Paso 7 — Actualización del índice
1. Añadir sección "Templates" en `.agents/standards/INDEX.md`.
2. Listar las tres plantillas.

### Paso 8 — Documentación opcional de IDE
1. Si se decide crear `.agents/standards/runtime/IDE_CONFIGURATION.md`:
   - Explicar que las configuraciones de IDE son plantillas en `.agents/templates/`.
   - Incluir instrucciones para Claude, Kimi, Cursor, etc.
2. Si no se crea, añadir una nota en `README.md` de templates.

### Paso 9 — Revisión final
1. Verificar que `claude-settings.json` sea válido JSON.
2. Confirmar que las plantillas no contienen datos de proyecto.
3. Validar que las plantillas sean fáciles de adaptar.
4. Asegurar que no haya referencias a `pay_back`, Flask ni dominio específico.

---

## 5. Criterios de aceptación

- [ ] Existe directorio `.agents/templates/`.
- [ ] Existe `README.md` con guía de uso.
- [ ] Existe `claude-settings.json` válido y genérico.
- [ ] Existe `domain-overview-template.md` con estructura clara.
- [ ] Existe `domain-cheatsheet-template.md` con estructura clara.
- [ ] `.agents/standards/INDEX.md` indexa las plantillas.
- [ ] Las plantillas no contienen configuraciones específicas del proyecto actual.
- [ ] No se modifican archivos fuera de `.agents/templates/` y el índice.
- [ ] No hay referencias a `pay_back`, Flask ni dominio de pagos.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Plantillas desactualizadas respecto al protocolo. | Revisarlas cuando cambien estándares core. |
| Usuarios modifiquen las plantillas en `.agents/templates/`. | Documentar claramente que deben copiarse al proyecto. |
| Configuración de IDE demasiado permisiva o restrictiva. | Usar valores conservadores y marcar campos a adaptar. |
| Duplicación con contratos de dominio. | Las plantillas son puntos de partida; los contratos son la especificación. |

---

## 7. Dependencias

- Plan 01 completado (la plantilla de IDE puede referenciar `OPERATIONAL_RULES.md`).
- Plan 07 completado (las plantillas de dominio complementan `PROJECT_MAP.md` y `TECHNICAL_ANALYSIS.md`).
- Acceso a `example/.claude/settings.local.json`.
- Acceso a cualquier cheatsheet de dominio en `example/`.

---

## 8. Orden relativo de ejecución

Este plan debe ejecutarse **último** dentro de la propuesta de integración ordenada, ya que utiliza y complementa todos los planes anteriores.

---

## 9. Notas adicionales

- Considerar añadir más plantillas en el futuro: `task-specification-template.md`, `adr-template.md`, `runbook-template.md`.
- No se requiere ejecutar código en este plan.
- Validar el JSON de `claude-settings.json` con un parser si es posible.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `claude-settings.json` | Plantilla de configuración de permisos y herramientas para Claude. | Configuraciones de otros IDEs, ni contenido de proyecto. |
| `domain-overview-template.md` | Plantilla de resumen de dominio. | Detalles técnicos de implementación; eso va en `TECHNICAL_ANALYSIS.md` del proyecto. |
| `domain-cheatsheet-template.md` | Plantilla de referencia rápida de dominio. | Documentación extensa; eso va en `domain-overview-template.md` o en documentación funcional. |
| `README.md` de templates | Guía de uso del catálogo de plantillas. | Contenido de las plantillas. |

**Principio aplicado:** cada plantilla responde a una única necesidad de arranque. No son estándares del protocolo (que viven en `.agents/standards/`); son puntos de partida para copiar y adaptar en cada proyecto.
