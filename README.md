# ARgentOS

Agent-based stateful orchestration protocol under `.agents/`.

## Ejemplo: microservicio Flask 3 (ABM de Usuarios)

Este repositorio incluye un microservicio de ejemplo generado siguiendo el protocolo `.agents`.

### Estructura

```text
src/
├── api/              # Blueprints y schemas (capa de presentación)
├── domain/           # Entidades y validadores (reglas de negocio)
├── infrastructure/   # Modelos SQLAlchemy, repositorio y DB
├── app.py            # Flask app factory
└── config.py         # Configuración
```

### Requisitos

- Python 3.10+
- Entorno virtual activado (ver `venv/`)
- Dependencias en `requirements.txt`

### Instalación

```bash
# Activar entorno virtual
source venv/Scripts/activate  # Windows Git Bash
# venv\Scripts\activate       # Windows CMD/PowerShell

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar

```bash
python run.py
```

La API queda disponible en `http://localhost:5000`.

### Endpoints

| Método | Endpoint       | Descripción           |
| ------ | -------------- | --------------------- |
| POST   | /users         | Crear usuario         |
| GET    | /users         | Listar usuarios       |
| GET    | /users/<uuid>  | Obtener usuario       |
| PUT    | /users/<uuid>  | Actualizar usuario    |
| DELETE | /users/<uuid>  | Eliminar usuario      |
| GET    | /health        | Health check          |

### Tests

```bash
pytest tests/ -v
```

### Datos del usuario

- `id`: UUID v4 generado automáticamente.
- `email`: formato válido, único.
- `username`: único, mínimo 3 caracteres.
- `password`: alfanumérico, mínimo 6 caracteres; se almacena hasheado.
