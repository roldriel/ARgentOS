# Orchestration Guide — Team Coordinator

## Anexo A: Prompt Rápido de Orquestación

Para usar por el orquestador cuando recibe una tarea del usuario:

```markdown
1. ¿Qué dominio de negocio impacta? (preorder, payment, callback, api, common)
2. ¿Qué capas arquitectónicas se ven afectadas? (models, services, views, providers, etc.)
3. ¿Requiere cambio en la base de datos? → Involucrar DB Architect.
4. ¿Requiere integración con API externa? → Involucrar Integration Specialist.
5. ¿Impacta flujos de pago o estados de preorder? → Involucrar QA Engineer obligatoriamente.
6. ¿Es un refactor estructural o nuevo feature? → Involucrar Technical Writer.
7. ¿Cambia reglas de negocio perceptibles por el usuario final? → Involucrar Functional Writer.
```

## Anexo B: Checklist del Orquestador antes de Delegar

- [ ] Leí todos los módulos `_common/ARCHITECTURE_*.md` para validar que la tarea es arquitectónicamente viable.
- [ ] Identifiqué el dominio y las capas afectadas.
- [ ] Descompuse la tarea en subtareas atómicas si es necesario.
- [ ] Determiné el orden correcto de ejecución de los subagentes.
- [ ] Verifiqué que cada prompt incluya el contexto completo necesario.
- [ ] Planeé un punto de control (Gate) antes de entregar al usuario.

## Anexo C: Glosario de Capas

| Capa | Sufijo | Regla de Oro |
|------|--------|--------------|
| View | `View` | Solo HTTP. Sin lógica de negocio. |
| Validator | `Validator` | Solo validación de entrada. Sin acceso a BD ni servicios. |
| Schema | `Schema` | Solo forma y tipos de datos. |
| Service | `Service` | Lógica de negocio pura. Sin dependencias de Flask/HTTP. |
| Model | `(db.Model)` | Persistencia pura. Sin orquestación. |
| Provider | `Provider` | Adaptador a sistemas externos. Sin decisiones de negocio. |

## Reglas de Delegación

- **Nunca reenvíes el prompt original del usuario.** Siempre reescribe el prompt usando el template del rol destino.
- **Incluye la ruta absoluta del proyecto** cuando el subagente deba leer archivos.
- **Re-lee los archivos modificados** antes de pasar al siguiente subagente.
