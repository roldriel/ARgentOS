# Plan de Implementación 08 — Plantillas de Proyecto

> **Origen:** Punto 8 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Proveer plantillas reutilizables para acelerar la adopción del protocolo en nuevos proyectos.
> **Restricción:** No se modifica ningún archivo dentro de `.agents/`. Las plantillas viven fuera del protocolo.

---

## 1. Objetivo del plan

Crear un directorio `templates/` en la raíz del repositorio con:

1. `templates/README.md` — guía de uso de las plantillas.
2. `templates/claude-settings.json` — plantilla de configuración local para Claude, basada en el archivo real del proyecto ejemplo.
3. `templates/domain-overview-template.md` — plantilla de resumen de dominio.
4. `templates/domain-cheatsheet-template.md` — plantilla de cheatsheet de dominio.

Las plantillas son puntos de partida para copiar y adaptar en cada proyecto. No son estándares del protocolo y no se sincronizan automáticamente con `.agents/`.

---

## 2. Alcance

### Incluido
- Lectura de `example/.claude/settings.local.json` como fuente real de configuración de Claude.
- Lectura de `example/.agents/roles/func_writer/DOMAIN_CHEATSHEET.md` como fuente de cheatsheet de dominio.
- Lectura de `example/.agents/roles/_common/DOMAIN_OVERVIEW.md` como fuente de resumen de dominio.
- Creación de plantillas genéricas y reutilizables en `templates/`.
- Documentación de uso en `templates/README.md`.
- Validación sintáctica de `templates/claude-settings.json`.
- Verificación de que las plantillas no contienen datos específicos del proyecto ejemplo.

### Excluido
- No se incluyen archivos específicos del IDE dentro de `.agents/`.
- No se generan configuraciones reales del proyecto actual (solo plantillas).
- No se modifica `.agents/` bajo ninguna circunstancia.
- No se documentan IDEs para los que no se cuenta con un archivo fuente real o un formato verificado.

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `templates/README.md` | Guía de uso del catálogo de plantillas. |
| `templates/claude-settings.json` | Plantilla de settings para Claude, copia adaptada de `example/.claude/settings.local.json`. |
| `templates/domain-overview-template.md` | Plantilla de resumen de dominio. |
| `templates/domain-cheatsheet-template.md` | Plantilla de cheatsheet de dominio. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/.claude/settings.local.json` | Fuente original de configuración de Claude. |
| `example/.agents/roles/func_writer/DOMAIN_CHEATSHEET.md` | Fuente de cheatsheet de dominio. |
| `example/.agents/roles/_common/DOMAIN_OVERVIEW.md` | Fuente de resumen de dominio. |

### Archivos a modificar
Ninguno. Este plan no modifica archivos existentes, solo crea archivos nuevos en `templates/`.

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuentes

1. Leer `example/.claude/settings.local.json`.
2. Leer `example/.agents/roles/func_writer/DOMAIN_CHEATSHEET.md`.
3. Leer `example/.agents/roles/_common/DOMAIN_OVERVIEW.md`.
4. Identificar qué configuraciones son genéricas y cuáles son específicas del proyecto ejemplo.
5. No leer `.agents/features.toml` ni otros archivos de `.agents/`, porque no son relevantes para crear plantillas de texto.

### Paso 2 — Diseño del directorio de plantillas

Estructura a crear:

```text
templates/
├── README.md
├── claude-settings.json
├── domain-overview-template.md
└── domain-cheatsheet-template.md
```

Ubicación: raíz del repositorio. No bajo `.agents/`.

### Paso 3 — Creación de `README.md`

Contenido mínimo:
- Propósito del directorio `templates/`.
- Advertencia: las plantillas son copias iniciales, no se sincronizan con `.agents/`.
- Cómo copiar y adaptar cada plantilla a un proyecto nuevo.
- Tabla de plantillas con descripción y destino sugerido.
- Instrucción: no editar las plantillas en `templates/` directamente; copiarlas al proyecto y adaptarlas allí.
- Nota sobre IDEs: por ahora solo se incluye plantilla para Claude, que es el único IDE con archivo fuente real en el ejemplo.

### Paso 4 — Creación de `claude-settings.json`

A partir de `example/.claude/settings.local.json`, crear una plantilla genérica que respete el esquema real. El contenido base es:

```json
{
  "language": "spanish",
  "permissions": {
    "allow": [
      "Bash(python -m py_compile:*)",
      "Bash(python -m pytest:*)",
      "Bash(python -m pylint:*)",
      "Bash(python -m black:*)",
      "Bash(python -m mypy:*)",
      "Bash(python -m isort:*)",
      "Bash(python -m flake8:*)",
      "Bash(grep:*)",
      "Bash(find:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(findstr:*)",
      "Bash(tree:*)",
      "Bash(python:*)",
      "Bash(set PYTHONPATH=src:*)",
      "Bash(pip install:*)",
      "Bash(cd:*)"
    ]
  },
  "tools": {
    "enabled": [
      "Bash"
    ]
  }
}
```

Notas obligatorias a documentar en `README.md`:
- El campo `language` debe adaptarse al idioma del proyecto.
- Las herramientas de calidad (`pylint`, `black`, `mypy`, `isort`, `flake8`) son opcionales y dependen del stack del proyecto.
- El permiso `Bash(pip install:*)` permite instalar paquetes. Revisar caso por caso.
- El permiso `Bash(set PYTHONPATH=src:*)` es específico de la estructura del ejemplo. Adaptar o eliminar si el proyecto no usa `src/`.
- No incluir rutas absolutas ni nombres de proyecto.
- El archivo debe copiarse a `.claude/settings.local.json` del proyecto destino.

### Paso 5 — Creación de `domain-overview-template.md`

Estructura base, derivada de `example/.agents/roles/_common/DOMAIN_OVERVIEW.md`. Debe incluir placeholders genéricos y secciones obligatorias:

```markdown
# Domain Overview: <Nombre del dominio>

> Contexto funcional del dominio. Reemplazar `<Nombre del dominio>`.

## 1. Modelo de acceso
> Cómo se accede al sistema: actores, autenticación, aislamiento de datos.

## 2. Concepto principal
> Definición del objeto o proceso central del dominio.

## 3. Creación / inicio del proceso
> Datos requeridos, validaciones y pasos para iniciar el proceso.

## 4. Restricciones de negocio
> Reglas horarias, monetarias, de formato, de volumen, etc.

## 5. Estados válidos
> Lista de estados posibles.

## 6. Transiciones permitidas
> Diagrama o lista de transiciones válidas entre estados.

## 7. Procesos principales
> Flujo principal, flujos alternativos, reintentos, cierre.

## 8. Integraciones externas
> Proveedores, servicios, callbacks, webhooks.

## 9. Invariantes globales
> Atributos o reglas que nunca pueden violarse.

## 10. Reglas críticas de dominio
> Advertencias y reglas que, si se omiten, dejan el sistema lógicamente inconsistente.

## 11. Glosario
> Términos específicos del dominio y sus definiciones.

## 12. Notas
> Advertencias para agentes o desarrolladores.
```

Cada sección debe incluir instrucciones breves de qué incluir. No debe contener referencias a `Pay Back`, `Preorder`, `Flask`, `SQLAlchemy` ni términos del ejemplo.

### Paso 6 — Creación de `domain-cheatsheet-template.md`

Estructura base, derivada de `example/.agents/roles/func_writer/DOMAIN_CHEATSHEET.md`:

```markdown
# Domain Cheatsheet: <Nombre del dominio>

> Referencia rápida para workers. Mantener actualizado.

## Estados válidos
1.
2.
3.

## Transiciones permitidas
```
<estado> → <estado>
<estado> → <estado>
```

## Reglas de negocio clave
| Regla | Valor / Condición |
|-------|-------------------|
| | |

## Invariantes globales
- 

## Anti-patrones
- 

## Decisiones frecuentes
| Situación | Decisión estándar | Excepciones |
|-----------|-------------------|-------------|
| | | |

## Enlaces rápidos
- 
```

### Paso 7 — Revisión final

1. Validar que `templates/claude-settings.json` sea JSON válido con:
   ```bash
   python -m json.tool templates/claude-settings.json
   ```
2. Confirmar que las plantillas no contienen datos del proyecto ejemplo.
3. Validar que las plantillas sean fáciles de adaptar.
4. Asegurar que no haya referencias a:
   - `payback`, `Pay Back`, `pay_back`, `pay-back`
   - `Preorder`, `preorder`
   - `Flask`
   - `SQLAlchemy`
   - `CPE`, `barra`, `código de barras` (como concepto propio del ejemplo)
   - Cualquier otro término específico del dominio de pagos del ejemplo.

La verificación debe hacerse con búsqueda textual, no visualmente. Ejemplo:

```bash
grep -R -i -E "payback|pay_back|preorder|flask|sqlalchemy|cpe|barra" templates/
```

Si el comando no devuelve coincidencias, el requisito se cumple.

---

## 5. Criterios de aceptación

- [ ] Existe directorio `templates/` en la raíz del repositorio.
- [ ] Existe `templates/README.md` con guía de uso.
- [ ] Existe `templates/claude-settings.json` y es JSON válido.
- [ ] `templates/claude-settings.json` es una copia adaptada de `example/.claude/settings.local.json`, no un formato inventado.
- [ ] Existe `templates/domain-overview-template.md` con estructura clara y secciones genéricas.
- [ ] Existe `templates/domain-cheatsheet-template.md` con estructura clara y secciones genéricas.
- [ ] Las plantillas no contienen configuraciones específicas del proyecto actual ni del ejemplo.
- [ ] No se modifican archivos dentro de `.agents/`.
- [ ] No hay referencias a `Pay Back`, `Preorder`, `Flask`, `SQLAlchemy` ni términos del dominio de pagos del ejemplo.
- [ ] El JSON se validó con `python -m json.tool` sin errores.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Plantillas desactualizadas respecto al protocolo. | Documentar que las plantillas no se sincronizan automáticamente. Agregar una tarea de mantenimiento manual cuando `.agents/` cambie. |
| Usuarios modifiquen las plantillas en `templates/` en lugar de copiarlas. | Indicar claramente en `README.md` que deben copiarse y adaptarse en el proyecto destino. |
| Configuración de IDE demasiado permisiva. | Usar como punto de partida el archivo real del ejemplo, documentar cada permiso y marcar los que deben revisarse. |
| Duplicación con contratos de dominio. | Las plantillas son puntos de partida; los contratos de dominio son la especificación. No reemplazan a los contratos. |

---

## 7. Dependencias

- Acceso a `example/.claude/settings.local.json`.
- Acceso a `example/.agents/roles/func_writer/DOMAIN_CHEATSHEET.md`.
- Acceso a `example/.agents/roles/_common/DOMAIN_OVERVIEW.md`.
- Python disponible para validar JSON con `python -m json.tool`.

No hay dependencias de otros planes de implementación.

---

## 8. Orden relativo de ejecución

Este plan puede ejecutarse en cualquier momento, siempre que existan las fuentes del ejemplo. Al crear archivos solo en `templates/` y no modificar `.agents/`, no depende de la finalización de otros planes.

---

## 9. Notas adicionales

- No se requiere ejecutar código de aplicación en este plan.
- Sí se requiere ejecutar `python -m json.tool templates/claude-settings.json` para validar el JSON.
- Posibles plantillas futuras: `task-specification-template.md`, `adr-template.md`, `runbook-template.md`. No son parte del alcance actual.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `templates/claude-settings.json` | Plantilla de configuración de permisos y herramientas para Claude. | Configuraciones de otros IDEs, ni contenido de proyecto. |
| `templates/domain-overview-template.md` | Plantilla de resumen de dominio. | Detalles técnicos de implementación; eso va en `technical-analysis.md` del proyecto. |
| `templates/domain-cheatsheet-template.md` | Plantilla de referencia rápida de dominio. | Documentación extensa; eso va en `domain-overview-template.md` o en documentación funcional. |
| `templates/README.md` | Guía de uso del catálogo de plantillas. | Contenido de las plantillas. |

**Principio aplicado:** cada plantilla responde a una única necesidad de arranque. No son estándares del protocolo (que viven en `.agents/`); son puntos de partida para copiar y adaptar en cada proyecto.
