# Stock Service API

API para la gestión de inventario, incluyendo productos y categorías.

## 🧱 Tecnologías principales

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- Docker + Docker Compose
- Clean Architecture
- Uvicorn (ASGI server)
- `pytest` para testing
- `ruff`, `black`, `mypy` para calidad de código

## 📁 Estructura del proyecto

Esta plantilla sigue los principios de **Clean Architecture** para asegurar la separación de responsabilidades y la mantenibilidad.

```
back/
├── src/
│   ├── app/                # Capa de presentación
│   │   ├── api/           # Endpoints y rutas
│   │   │   ├── routes/    # Definición de rutas
│   │   │   └── schemas/   # Esquemas de validación
│   │   └── app_factory.py # Configuración de FastAPI
│   ├── core/              # Lógica de negocio central
│   │   └── auth.py        # Autenticación y autorización
│   ├── domain/            # Entidades y reglas de negocio
│   │   └── entities/      # Entidades del dominio
│   ├── infrastructure/    # Implementaciones de infraestructura
│   │   
│   ├── repositories/      # Capa de acceso a datos
│   │   
│   ├── use_cases/         # Casos de uso
│   │   
│   └── main.py           # Punto de entrada
├── tests/                # Tests unitarios y de integración
├── .env.example         # Ejemplo de variables de entorno
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

## ⚙️ Requisitos

- Docker
- Docker Compose
- `make` (GNU Make)
- Firebase project con Authentication y Firestore habilitados
- Credenciales de servicio de Firebase

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone <repository-url>
cd back
```

2. Configura las variables de entorno:
```bash
cp .env.example .env
```
Edita el archivo `.env` con tus credenciales de Firebase y configuración de la API.

3. Obtén las credenciales de servicio de Firebase:
   - Ve a la consola de Firebase
   - Selecciona tu proyecto
   - Ve a Configuración del proyecto > Cuentas de servicio
   - Genera una nueva clave privada
   - Copia los valores al archivo `.env`

## 🚀 Ejecución

### Usando Make

```bash
make up         # Levanta el servicio
make build      # Construir y levanta el servicio
make up-local   # Levanta usando .env.local
make down       # Detiene el servicio
make restart    # Reinicia todo limpio
make logs       # Muestra logs
make shell      # Ingresa al contenedor
```

La API estará disponible en `http://localhost:8000`

## 📚 Documentación de la API

La documentación interactiva está disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔌 Endpoints

### Usuarios

- `POST /v1/users` - Crear un nuevo usuario
- `GET /v1/users/me` - Obtener información del usuario actual
- `GET /v1/users/{user_id}` - Obtener información de un usuario específico
- `GET /v1/users` - Listar todos los usuarios (solo admin)
- `PUT /v1/users/{user_id}` - Actualizar un usuario
- `DELETE /v1/users/{user_id}` - Eliminar un usuario (solo admin)
- `POST /v1/users/{user_id}/activate` - Activar un usuario (solo admin)
- `POST /v1/users/{user_id}/deactivate` - Desactivar un usuario (solo admin)

## 🔐 Autenticación

La API utiliza Firebase Authentication para la autenticación de usuarios. Para acceder a los endpoints protegidos:

1. Obtén un token de Firebase Authentication
2. Incluye el token en el header de la petición:
```
Authorization: Bearer <token>
```

## 🧪 Testing y calidad de código

### Ejecutar tests
```bash
make test
```

### Formatear código
```bash
make format
```

### Verificar estilo
```bash
make lint
```

### Verificar todo
```bash
make check  # Ejecuta format + lint + test
```

### Pre-commit

Este proyecto incluye soporte para [pre-commit](https://pre-commit.com/) para evitar subir código con errores o sin formatear.

#### Activación:
```bash
make pre-commit-install
```

Cada vez que hagas `git commit`, se correrá automáticamente:
- `black`
- `flake8`
- `pytest`

## 🐳 Despliegue

### Cloud Run

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/agrup-api
gcloud run deploy agrup-api --image gcr.io/PROJECT_ID/agrup-api --platform managed
```

## 📝 Notas adicionales

- La API sigue los principios de Clean Architecture
- Cada caso de uso está separado en su propio archivo para mejor mantenibilidad
- Se utiliza Firebase Admin SDK para la autenticación y almacenamiento
- Los errores son manejados de forma consistente a través de la aplicación
- Se implementa CORS para permitir peticiones desde el frontend
