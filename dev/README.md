# Workspace de desarrollo — `dev/`

`dev/` es el banco de pruebas y herramientas del desarrollo de ARgentOS. No
forma parte de lo distribuido: los adoptantes reciben solo `.agents/` +
`AGENTS.md` desde `dist` (ver `ADOPTION.md` §5).

## Mapa de componentes

| Componente | Rol | Origen |
| --- | --- | --- |
| `tools/check_protocol_invariants.py` | Invariantes documentales del payload (resolución de referencias, frontera, metadata H13) | Planes 27/28 y RFC-55 |
| `tools/check_plan_citations.py` | Verificación de citas `ruta:sección` en `plans/` | Convención de `plans/INDEX.md` |
| `runtime/` | Implementaciones de referencia de materialización del Execution Context (prompt y tool calls) | Planes 07 y 18 |
| `runtime/tests/`, `tools/tests/` | Suites de tests de los componentes dev | Planes 07/18 y 27/28 |

## Convenciones

- Python 3.11+, stdlib únicamente (sin dependencias externas).
- Documentación en español; código en inglés; commits en inglés (Conventional
  Commits).
- Un componente = una documentación canónica (esta política single-source
  aplica a `dev/`); el resto linkea, no duplica.
- `protocol/` es data, no instrucciones: ver `AGENTS.md` raíz y
  `dev/source-layout.md`.

## Verificación

```bash
python dev/tools/check_protocol_invariants.py --payload protocol .
python dev/tools/check_plan_citations.py
python -m pytest protocol/.agents/harness/tests/ dev/runtime/tests/ dev/tools/tests/
```

La cobertura pendiente y las prioridades viven en `dev/ROADMAP.md`; el roadmap
de planes/RFCs del proyecto, en `plans/INDEX.md`.
