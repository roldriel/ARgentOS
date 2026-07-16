# Testing Rules — QA Engineer

## Alcance de Testing

- **Unitarios**: Services, Validators, Schemas, Providers (con mocks).
- **Integración**: Flujos de preorder completos, callbacks, y cierre de pagos.
- **Regresión**: Todo cambio en `preorder`, `payment` o `callback` debe incluir al menos un test de regresión.

## Patrones de Mock

- **Providers**: Mockear siempre. Nunca realizar requests HTTP reales.
- **Base de datos**: Usar sesión de test o mock de `db.session` según el proyecto.
- **Flask context**: Evitar dependencia de `current_app` en tests unitarios de services.

## Cobertura Mínima Esperada

- Lógica nueva en **Services**: ≥ 80 % cobertura.
- Transiciones de estado financiero: 100 % de escenarios críticos deben tener test.

## Prohibiciones

- NO ejecutar `pytest` a menos que el usuario lo instruya explícitamente (ver `_common/OPERATIONAL_RULES.md` §3).
- NO instalar dependencias de testing nuevas sin autorización.
