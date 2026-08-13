# ARgentOS (desarrollo) — estado y feedback crítico

**Fecha:** 2026-08-12

**Nota:** este archivo reemplaza al informe de auditoría de documentación del
2026-08-12 (disponible en la historia de git). El estado de remediación de esa
auditoría: 10 de 11 puntos cerrados; parciales el 3 (links Markdown genéricos
sin checker, riesgo bajo) y el 6 (queda la referencia de RFC-42 en el
payload, que requiere vía formal).

---

## Cómo funciona ahora

El repo se organiza en tres capas claras: `protocol/` es el producto (data,
intocable sin vía RFC/plan), `tools/` + `runtime/` son la instrumentación y la
implementación de referencia, y `plans/` es la historia de diseño que gobierna
todo cambio. Alrededor gira una batería de verificación (4 checkers + 114
tests) que corre igual en local y en CI. El flujo de trabajo es: RFC/plan
aprobado → ejecución en `dev` → verificación → cierre documental (estados,
changelog, VERSION) → commit atómico → promoción a `master` con tag → `dist`
regenerada por CI.

## Puntos fuertes

- **La gobernanza es real, no aspiracional.** Es el rasgo distintivo del
  proyecto: toda decisión tiene traza (RFC → plan → nota de ejecución →
  changelog), y gran parte es *mecánicamente enforceable* (estructura de
  planes, citas, invariantes del payload, sync de dist). Pocos repos pueden
  decir "la convención la hace cumplir un script".
- **La frontera producto/workspace está limpia.** La disolución de `dev/`
  eliminó la última ambigüedad conceptual: `protocol/` es data, el resto es
  tooling. Un agente nuevo lee un solo AGENTS.md operativo y tiene el mapa
  completo.
- **Dogfooding disciplinado.** El protocolo se usa para desarrollar el
  protocolo, y las fricciones se registran y remedian (la sexta serie entera
  nació de una auditoría).
- **Todo el trabajo de remediación quedó verificado**, no declarado: tests,
  checkers, y los cambios estructurales se hicieron con la batería corriendo
  al final de cada fase.

## Deuda técnica

- **23 RFCs en `Proposal` (RFC-32…54) con planes redactados pero no
  ejecutados.** Es la deuda grande: hay una serie completa de diseño
  aprobado-en-papel esperando aceptación. Algunas ya tienen planes `Executed`
  por vía plan con regularización pendiente — un patrón que resuelve el corto
  plazo pero acumula deuda de gobernanza (ya pasó con RFC-24…28 y hubo que
  regularizar retroactivamente).
- **`test_toolcalls.py` sigue acoplado al payload** (lee skills reales).
  Contradice la regla escrita en `tests/AGENTS.md` — señalado varias veces,
  sin cerrar.
- **El INDEX carga demasiados roles**: índice, backlog, convenciones, snapshot
  de estado, notas de regularización. Funciona, pero es frágil como fuente
  citada por todo el mundo; un día habrá que separar "convenciones" de
  "índice".
- **`feature.md`** es un documento de diseño temprano con citas rotas
  conocidas, fuera del scope de todos los checkers por decisión. Está en el
  limbo: ni traza histórica archivada ni documento vivo mantenido.

## Puntos débiles

- **El modelo versión↔plan acopla el versionado del protocolo a la cadencia
  de planes.** Cada plan ejecutado es una versión: funciona, pero versiones
  como 3.0.2–3.0.5 nacieron de regularizaciones, no de cambios de producto.
  El número de versión comunica poco al adoptante.
- **La verificación depende de disciplina de ejecución local.** Los checkers
  corren en CI, pero CI no bloquea nada visible en el flujo actual (no hay
  branch protection mencionada); un push directo a `dev` roto no se entera
  nadie hasta que alguien mira.
- **El punto 6 residual es un agujero de gobernanza conocido y abierto**:
  `ANTI_CIRCUMVENTION.md` no referencia la regla RFC-42 que hoy gobierna todos
  los cambios del payload. El documento que se llama "anti-circumvention" no
  cita la regla anti-circumvention vigente.
- **Harness sin cobertura en el repo.** Decisión del usuario, respetada, pero
  el costo real es: el código ejecutable del payload (`hook_gate.py`,
  `runner_state.py`) no tiene regresión automática en este repo; sus tests
  solo corren en proyectos adoptantes. Un plan que rompa el harness se
  detecta tarde.

## Cabos sueltos

1. Referencia RFC-42 en el payload (requiere plan aprobado — es el único
   pendiente con vía formal).
2. Push de `dev` (4 commits locales sin publicar) y eventual sync de
   `master`.
3. Links Markdown genéricos sin checker (riesgo bajo, decisión consciente).
4. Desacople de `test_toolcalls.py` (fixtures propias).
5. `AUDITORIA_DOCUMENTACION.md` no tiene hogar conceptual: ¿vive en raíz para
   siempre, se archiva en `plans/`, se borra cuando se cierre el punto 6?

## Feedback crítico

El proyecto tiene un riesgo estructural claro: **la gobernanza escala peor
que el protocolo**. Hay 55 RFCs y 54 planes para un producto que son, en
esencia, documentos Markdown. El aparato (ciclos de status, amendment logs,
citas verificables, checkers) es excelente para sostener calidad, pero cada
cambio chico paga un peaje burocrático alto, y la evidencia está a la vista:
regularizaciones retroactivas repetidas (RFC-24…28, planes 31–36, RFC-32…54
en Proposal permanente). Cuando la gobernanza necesita regularizarse a sí
misma cada dos semanas, la señal es que el proceso pide más ceremonia de la
que el riesgo real justifica. Los checkers ayudan (mecanizan el cumplimiento),
pero la pregunta que el proyecto eventualmente tiene que responder es: ¿qué
cambios del payload realmente necesitan RFC, y cuáles podrían pasar por
fast-track con checker verde? Mientras tanto, la prioridad honesta no es
seguir remendando el workspace —que hoy quedó sólido— sino destrabar la serie
Proposal: 23 diseños aprobados en papel que no ejecutan son 23 decisiones no
tomadas.
