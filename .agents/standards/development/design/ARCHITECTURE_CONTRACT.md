# Architecture Contract

## 1. Propósito y alcance

Este documento es un **contrato operativo** que convierte los principios arquitectónicos definidos en otros estándares del protocolo en reglas aplicables por los workers durante la generación o modificación de código.

- No reemplaza ni duplica la teoría arquitectónica de `LAYERED_ARCHITECTURE.md`, `CLEAN_ARCHITECTURE.md`, `SCREAMING_ARCHITECTURE.md` ni `DDD_TACTICAL.md`; las consume y operativiza.
- Es **opt-in**: el proyecto gobernado debe declarar explícitamente que lo adopta (ver [Activación](#2-activación)).
- Aplica a todo código generado o modificado por workers mientras el contrato esté activo.
- Si una tarea no puede completarse sin violar este contrato, el worker debe detenerse, explicar el conflicto y solicitar aclaración o autorización explícita.

---

## 2. Activación

El contrato se activa cuando **al menos una** de las siguientes condiciones se cumple:

1. El feature flag `architecture_contract` está habilitado en `.agents/features.toml`:
   ```toml
   [features]
   architecture_contract = true
   ```
2. La variable de entorno `AGENTS_FEATURE_ARCHITECTURE_CONTRACT` está configurada como `true`.
3. El `TASK_SPECIFICATION.md` declara explícitamente:
   ```markdown
   ## Arquitectura
   Este proyecto adopta `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.
   ```

> **Nota:** El proyecto puede adaptar las capas concretas al activar el contrato, pero debe documentar la equivalencia de responsabilidades, sufijos y reglas de dependencia. No puede reducir la lista mínima de sufijos ni eliminar las reglas duras de dependencia.

---

## 3. Capas arquitectónicas

El contrato define las siguientes capas por defecto. Un proyecto adoptante puede mapearlas a su estructura propia siempre que preserve las responsabilidades y restricciones.

| Capa | Responsabilidad | Sufijos |
|------|-----------------|---------|
| **Views** | Interfaz de entrada. Recibe solicitudes, delega validación y lógica de negocio. | `View` |
| **Validators** | Validación de entrada y contexto. Coordina uno o más schemas. | `Validator` |
| **Schemas** | Serialización, deserialización y validación estructural de datos. | `Schema` |
| **Services** | Lógica de negocio, reglas y orquestación de casos de uso. | `Service` |
| **Models** | Entidades de persistencia y contratos de datos de infraestructura. | `Model` |
| **Providers** | Adaptadores externos. Aíslan APIs, protocolos y sistemas de terceros. | `Provider` |
| **Domain Errors** | Excepciones que modelan estados inválidos del dominio. | `Error`, `Exception` |

### Responsabilidades generales por capa

- **Views**: manejar únicamente preocupaciones de entrada/salida; no contienen lógica de negocio.
- **Validators**: validar solicitudes; no acceden a persistencia, servicios ni providers.
- **Schemas**: definir forma y tipos de datos; no contienen lógica de negocio.
- **Services**: implementar reglas de negocio; no dependen de frameworks de infraestructura.
- **Models**: representar contratos de persistencia; no contienen flujos de negocio.
- **Providers**: adaptar sistemas externos; no contienen lógica de negocio ni acceden directamente a models.
- **Domain Errors**: expresar estados de dominio inválidos de forma explícita.

---

## 4. Reglas de dependencia

Las dependencias permitidas entre capas son:

```text
Views → Validators → Schemas
Views → Services → Models
Services → Providers → External APIs
```

### Dependencias prohibidas

- Views → Models
- Views → Providers
- Validators → Services
- Validators → Providers
- Schemas → Validators
- Schemas → Services
- Providers → Models
- Models → cualquier capa superior

### Matriz de dependencias

| Desde / Hacia | Views | Validators | Schemas | Services | Models | Providers |
|---------------|-------|------------|---------|----------|--------|-----------|
| **Views**     | -     | Permitido  | No      | Permitido| Prohibido| Prohibido |
| **Validators**| No    | -          | Permitido| Prohibido| Prohibido| Prohibido |
| **Schemas**   | No    | No         | -       | No       | No     | No        |
| **Services**  | No    | No         | No      | -        | Permitido| Permitido |
| **Models**    | No    | No         | No      | No       | -      | No        |
| **Providers** | No    | No         | No      | No       | Prohibido| -        |

### Reglas adicionales

- Los providers actúan como adaptadores: no contienen lógica de negocio ni acceden directamente a models.
- La lógica de negocio no puede depender de frameworks de infraestructura.
- Cualquier solución que requiera una dependencia prohibida es arquitectónicamente inválida.

---

## 5. Naming suffixes

Cada archivo/clase debe tener un sufijo que indique su capa arquitectónica.

### Lista mínima obligatoria

| Capa | Sufijo |
|------|--------|
| View | `View` |
| Validator | `Validator` |
| Schema | `Schema` |
| Service | `Service` |
| Provider | `Provider` |
| Domain Error | `Error` o `Exception` |

### Reglas

- El proyecto puede extender la lista de sufijos, pero **no puede reducirla**.
- Los nombres deben ser explícitos, en inglés y revelar intención.
- Están prohibidos los nombres genéricos sin sufijo como `Manager`, `Helper`, `Processor`, `Util`, `Handler`, `Common` para clases principales.
- Los nombres de archivo usan `snake_case`; los nombres de clase usan `PascalCase`.

### Ejemplos

| Componente | Nombre de archivo | Nombre de clase |
|------------|-------------------|-----------------|
| Vista de pago | `payment_view.py` | `PaymentView` |
| Validador de creación | `payment_create_validator.py` | `PaymentCreateValidator` |
| Schema de entrada | `payment_create_schema.py` | `PaymentCreateSchema` |
| Servicio de pago | `payment_service.py` | `PaymentService` |
| Provider externo | `bind_payment_provider.py` | `BindPaymentProvider` |
| Error de dominio | `invalid_amount_error.py` | `InvalidAmountError` |

---

## 6. File identity

Cada archivo del proyecto gobernado debe incluir como **primera línea** un comentario con su ruta relativa desde la raíz del proyecto.

```python
# apps/payments/services/payment_service.py
```

### Reglas

- La ruta declarada debe coincidir con la ubicación real del archivo.
- Todos los imports deben ser **absolutos desde la raíz del proyecto**.
- Los imports relativos están **prohibidos**.
- Cada archivo debe tener **una responsabilidad principal**.

---

## 7. Prohibiciones

Quedan explícitamente prohibidas las siguientes prácticas:

1. Mezclar lógica de capas en un mismo archivo.
2. Importar infraestructura desde capas de dominio o servicios.
3. Usar nombres genéricos sin sufijo (`Manager`, `Helper`, `Utils`, `Handler`, `Processor`, `Common`) como clase principal.
4. Bypassear validadores desde views.
5. Acceder a models directamente desde views.
6. Realizar refactors arquitectónicos implícitos.
7. Mezclar patrones arquitectónicos dentro de una misma tarea.
8. Introducir dependencias prohibidas entre capas.
9. Introducir alternativas arquitectónicas una vez que se decidió un patrón para la tarea.

---

## 8. Auto-verificación

Antes de generar o modificar código, el worker debe ejecutar el siguiente checklist:

- [ ] Identificar la capa arquitectónica del archivo.
- [ ] Verificar que sus dependencias solo apuntan a capas permitidas.
- [ ] Confirmar que el nombre del archivo y de la clase cumple con el sufijo obligatorio.
- [ ] Confirmar que la línea 1 del archivo contiene el `file identity` con la ruta desde la raíz del proyecto.
- [ ] Revisar que no se viole ninguna prohibición del contrato.
- [ ] Asegurar que la lógica de negocio no dependa de frameworks de infraestructura.

Si algún ítem falla, el worker debe detenerse, documentar el conflicto y solicitar aclaración o autorización explícita antes de continuar.

---

## 9. Relación con otros estándares

Este contrato consume y unifica los principios definidos en:

- `LAYERED_ARCHITECTURE.md`: principios teóricos de capas horizontales.
- `CLEAN_ARCHITECTURE.md`: principios de independencia de frameworks y dependencias hacia adentro.
- `SCREAMING_ARCHITECTURE.md`: organización del proyecto por dominio.
- `DDD_TACTICAL.md`: entidades, value objects, agregados y servicios de dominio.

Este contrato las une en reglas aplicables a la generación de código. **En caso de conflicto entre este contrato y un estándar canónico correspondiente, prevalece el estándar canónico.**

---

## 10. Ejemplos

### 10.1 Archivo bien estructurado

```python
# apps/payments/services/payment_service.py
from apps.payments.providers.bind_payment_provider import BindPaymentProvider
from apps.payments.models.payment_model import PaymentModel
from apps.payments.errors.invalid_amount_error import InvalidAmountError


class PaymentService:
    """Orchestrates payment creation and binds it to an external provider."""

    def __init__(self, provider: BindPaymentProvider):
        self._provider = provider

    def create_payment(self, amount: int, currency: str) -> PaymentModel:
        """Create a payment after validating business rules."""
        if amount <= 0:
            raise InvalidAmountError("Payment amount must be positive")
        return self._provider.bind_payment(amount, currency)
```

### 10.2 Dependencia permitida

```python
# apps/payments/views/payment_view.py
from apps.payments.validators.payment_create_validator import PaymentCreateValidator
from apps.payments.services.payment_service import PaymentService


class PaymentView:
    def post(self, payload: dict) -> dict:
        validator = PaymentCreateValidator()
        validated = validator.validate(payload)
        service = PaymentService()
        return service.create_payment(**validated)
```

### 10.3 Violación y corrección

#### Violación: view accediendo directamente a un model

```python
# apps/payments/views/payment_view.py
from apps.payments.models.payment_model import PaymentModel  # Prohibido


class PaymentView:
    def post(self, payload: dict) -> dict:
        payment = PaymentModel.create(payload)  # Violación
        return {"id": payment.id}
```

#### Corrección: delegar en un service

```python
# apps/payments/views/payment_view.py
from apps.payments.validators.payment_create_validator import PaymentCreateValidator
from apps.payments.services.payment_service import PaymentService


class PaymentView:
    def post(self, payload: dict) -> dict:
        validator = PaymentCreateValidator()
        validated = validator.validate(payload)
        service = PaymentService()
        payment = service.create_payment(**validated)
        return {"id": payment.id}
```
