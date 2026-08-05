# Guía de adopción — Protocolo ARgentOS

Cómo adoptar el protocolo ARgentOS en otro proyecto. ARgentOS es un protocolo
**documental**: no se instala como paquete; adoptarlo es copiar el directorio del
protocolo y configurar lo mínimo (fuera de alcance declarado:
`plans/20-release-adoption.md` §Fuera de alcance). Origen de esta guía:
`plans/20-release-adoption.md` §B.

La versión adoptada queda declarada en `.agents/VERSION`. Para actualizaciones
posteriores, seguir [`MIGRATION.md`](MIGRATION.md).

---

## 1. Qué copiar

Del repositorio de origen al proyecto adoptante:

| Copiar | Destino | Obligatorio |
|---|---|---|
| `.agents/` (completo) | `<proyecto>/.agents/` | Sí |
| `AGENTS.md` (raíz) | `<proyecto>/AGENTS.md` | Sí |

No hace falta copiar nada más: `.agents/` es autocontenido y no referencia
`plans/` ni RFCs (frontera documental, `plans/INDEX.md` §Convenciones). Los
documentos de diseño (`plans/`, `feature.md`) son historia del desarrollo del
protocolo, no parte del producto adoptado. `CHANGELOG.md` y `MIGRATION.md`
conviene conservarlos como referencia de versionado, pero no son requeridos por
el runtime.

Requisito de entorno: Python 3.11+ disponible como `python` (el harness usa
`tomllib`, de la stdlib). No hay dependencias externas para el health-check;
`pytest` solo se necesita para correr la suite de tests del harness.

## 2. Qué configurar

1. **`.gitignore` del proyecto**: agregar `.project/` (artefactos de sesión
   efímeros; el health-check los crea solo). `.agents/` se versiona completo.
2. **`.agents/features.toml`**: revisar los flags. Defaults seguros: los flags
   `[code]` (`decision_trees`, `rubrics`, `knowledge_base`, prácticas técnicas)
   vienen habilitados y el health-check los valida; `architecture_contract`
   viene deshabilitado. Cada flag puede apagarse por variable de entorno
   `AGENTS_FEATURE_<FLAG>` sin editar el archivo.
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
python .agents/harness/runner.py health-check
python -m pytest .agents/harness/tests/
```

- El **health-check** es la primera verificación: confirma que la estructura del
  protocolo quedó íntegra (directorios requeridos, archivos índice, front matter
  de contratos, decision trees, rubrics, KB, estándares de prácticas técnicas).
  Debe terminar en `PASS`.
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
7. `.agents/harness/INDEX.md` — triggers del harness, runner, health-check,
   recovery.

## 5. Qué NO forma parte de la adopción

- No se adopta `plans/` ni las RFCs: son el proceso de diseño del protocolo, no
  el protocolo.
- No se adopta `example/` ni `runtime/`: son bancos de prueba del desarrollo.
- No hay soporte de múltiples versiones en paralelo: se adopta una versión y se
  migra siguiendo `MIGRATION.md`.
